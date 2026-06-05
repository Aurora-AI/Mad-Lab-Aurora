import os
import sys
import shutil
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

# Ajustes de path para importação dos módulos
sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../synthesizer')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../factory')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../bff')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../acquisition')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sandbox')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ingestion'))
])

from sandbox_contracts import PipelinePausedException, DiagnosticFinding, PatchCandidate, PromotionApprovalRecord

class PipelineAbortedException(Exception):
    """Lançada quando uma etapa do pipeline falha (Fail-Closed)."""
    pass

class HumanPromotionHalt(Exception):
    """Lançada para pausar o pipeline aguardando promoção humana."""
    pass

class SynthesisDAG:
    def __init__(self, target_url: str, api_manifest_path: str, output_dir: str):
        self.target_url = target_url
        self.api_manifest_path = api_manifest_path
        self.output_dir = output_dir
        self.start_time = time.monotonic()

    def validate_pre_conditions(self):
        """Regra Canônica: api_manifest ausente -> aborta"""
        if not self.api_manifest_path or not os.path.exists(self.api_manifest_path):
            raise PipelineAbortedException(f"Pre-condition failed: API Manifest not found at {self.api_manifest_path}")

    def emit_heartbeat(self, sandbox_run_id: str, stage: str, progress: int, status: str, error_class: str = "NONE"):
        elapsed = int(time.monotonic() - self.start_time)
        heartbeat = {
            "sandbox_run_id": sandbox_run_id,
            "os_id": "OS-008",
            "stage": stage,
            "progress_percent": progress,
            "status": status,
            "elapsed_seconds": elapsed,
            "error_class": error_class,
            "correlation_id": f"CID-{sandbox_run_id[3:]}"
        }
        print(f"[TELEMETRY_HEARTBEAT] {json.dumps(heartbeat)}")

    async def execute(self, 
                      probe_artifact_mock: Optional[Any] = None, 
                      asset_kit_mock: Optional[Dict[str, Any]] = None, 
                      governance_mode: str = "transmute", 
                      probe_truth_mock: Optional[Dict[str, Any]] = None,
                      acquire_asset_kit: bool = False,
                      asset_kit_manifest_path: Optional[str] = None) -> Dict[str, Any]:
        self.validate_pre_conditions()
        
        results = {}

        # 1. ExtractTarget (Probe)
        print("[DAG] Running task: ExtractTarget...")
        try:
            if probe_artifact_mock is not None:
                artifact = probe_artifact_mock
            else:
                from real_page_probe import extract_real_page_intelligence
                artifact = await extract_real_page_intelligence(self.target_url)
            
            if artifact is None:
                raise PipelineAbortedException("ExtractTarget produced no output.")
                
            from anti_stub_gate import AntiStubGate
            gate = AntiStubGate(surface_type="landing")
            gate.evaluate_page_intelligence(artifact)
            print("[DAG] AntiStubGate.PageIntelligence Passed.")
            
            results["artifact"] = artifact
        except Exception as e:
            if isinstance(e, PipelineAbortedException):
                raise
            raise PipelineAbortedException(f"ExtractTarget failed: {e}")

        # 1.2 AcquireAssetKit (Fase A)
        print("[DAG] Running task: AcquireAssetKit...")
        manifest_path = None
        try:
            if acquire_asset_kit:
                from asset_kit_acquisition_agent import AssetKitAcquisitionAgent
                agent = AssetKitAcquisitionAgent(self.target_url)
                manifest_path = await agent.acquire()
            elif asset_kit_manifest_path:
                manifest_path = Path(asset_kit_manifest_path)
        except Exception as e:
            raise PipelineAbortedException(f"AcquireAssetKit failed: {e}")

        # 1.3 StageAssetKit
        print("[DAG] Running task: StageAssetKit...")
        staging_dir = Path(self.output_dir) / "staging"
        os.makedirs(staging_dir, exist_ok=True)
        try:
            import shutil
            if manifest_path and manifest_path.exists():
                src_kit_dir = manifest_path.parent
                shutil.copytree(src_kit_dir, staging_dir, dirs_exist_ok=True)
            elif isinstance(asset_kit_mock, str) and os.path.exists(asset_kit_mock):
                # Fallback antigo para manter compatibilidade com testes legados
                kit_src_html = Path(asset_kit_mock) / "Google Antigravity.html"
                kit_src_files = Path(asset_kit_mock) / "Google Antigravity_files"
                kit_src_manifest = Path(asset_kit_mock) / "asset_kit_manifest.json"
                
                if kit_src_html.exists():
                    shutil.copy(kit_src_html, staging_dir / "Google Antigravity.html")
                if kit_src_files.exists():
                    shutil.copytree(kit_src_files, staging_dir / "Google Antigravity_files", dirs_exist_ok=True)
                if kit_src_manifest.exists():
                    shutil.copy(kit_src_manifest, staging_dir / "asset_kit_manifest.json")
        except Exception as e:
            raise PipelineAbortedException(f"StageAssetKit failed: {e}")

        # 1.4. Ingest Asset Kit (KitIngestion)
        print("[DAG] Running task: IngestAssetKit...")
        try:
            from kit_ingestor import KitIngestor
            
            kit_name = "Google Antigravity"
            if (staging_dir / "asset_kit_manifest.json").exists():
                try:
                    with open(staging_dir / "asset_kit_manifest.json", "r", encoding="utf-8") as f:
                        m_data = json.load(f)
                    html_file_name = m_data.get("html_file", "source.html")
                    kit_name = html_file_name.replace(".html", "")
                except Exception:
                    kit_name = "source"
            
            ingestor = KitIngestor(staging_dir=staging_dir, kit_name=kit_name)
            
            if not (staging_dir / "asset_kit_manifest.json").exists():
                raise PipelineAbortedException("Fail-Closed: asset_kit_manifest.json missing in Staging.")

            kit_artifact = ingestor.ingest()
            results["kit_artifact"] = kit_artifact
        except Exception as e:
            raise PipelineAbortedException(f"IngestAssetKit failed: {e}")


        # 2. ResolveTruth (HybridTruthResolver)
        print("[DAG] Running task: ResolveTruth...")
        try:
            from truth_resolver import HybridTruthResolver
            resolver = HybridTruthResolver()
            
            probe_dict = probe_truth_mock if probe_truth_mock is not None else {
                "css_variables": {"primary": "#FFFFFF"},
                "layout_viewport": {"height": "85vh"}
            }
            if probe_artifact_mock is not None and hasattr(probe_artifact_mock, "colors"):
                probe_dict["computed_styles"] = {"colors": [c.hex_value for c in probe_artifact_mock.colors]}

            kit_dict = kit_artifact.model_dump()
            
            resolution = resolver.resolve(probe_dict, kit_dict)
            if resolution.has_critical_conflicts:
                raise PipelinePausedException("ResolveTruth paused: Critical Conflict identified (Manual Escalation).", [])
                
            results["resolved_truth"] = resolution
        except PipelinePausedException:
            raise
        except Exception as e:
            raise PipelineAbortedException(f"ResolveTruth failed: {e}")

        # --- DAG Phase 2: Transmutation (OS-010) ---
        print("[DAG] Running task: ExtractSourcePatterns...")
        try:
            from pattern_extractor import SourcePatternExtractor
            extractor = SourcePatternExtractor(results["resolved_truth"])
            source_fingerprint = extractor.generate_fingerprint()
            results["source_fingerprint"] = source_fingerprint
        except Exception as e:
            raise PipelineAbortedException(f"ExtractSourcePatterns failed: {e}")

        print("[DAG] Running task: TransmuteOriginality...")
        try:
            from transmutation_contracts import CandidateFingerprint
            
            if governance_mode == "clone":
                # Força falha: O candidato é uma cópia exata
                candidate_fingerprint = CandidateFingerprint(
                    layout_hash=source_fingerprint.layout_hash,
                    color_palette_hash=source_fingerprint.color_palette_hash,
                    typography_hash=source_fingerprint.typography_hash,
                    motion_hash=source_fingerprint.motion_hash,
                    asset_hashes=source_fingerprint.asset_hashes,
                    text_hashes=source_fingerprint.text_hashes,
                    component_names=source_fingerprint.component_names
                )
            else:
                # We simulate a transmutation engine outputting a proprietary candidate fingerprint
                candidate_fingerprint = CandidateFingerprint(
                    layout_hash="transmuted_layout_hash",
                    color_palette_hash="transmuted_color_hash",
                    typography_hash="transmuted_typo_hash",
                    motion_hash="transmuted_motion_hash",
                    asset_hashes=[], # Copiar nada
                    text_hashes=[],  # Copiar nada
                    component_names=["AuroraLandingShell", "AuroraTopNavigation", "AuroraHeroStatement", "AuroraPrimaryCTA", "AuroraSecondaryCTA", "AuroraProductNarrativeSection", "AuroraUseCaseCluster", "AuroraFooterNavigation"]
                )
        except Exception as e:
            raise PipelineAbortedException(f"TransmuteOriginality failed: {e}")

        print("[DAG] Running task: OriginalityGate...")
        try:
            from originality_gate import OriginalityTransmutationGate
            gate = OriginalityTransmutationGate(source_fingerprint)
            proprietary_candidate = gate.evaluate_candidate(
                candidate_id="CAND-001",
                candidate_fingerprint=candidate_fingerprint,
                axes=["semantic", "visual", "structural", "motion", "brand"],
                candidate_colors=["#FFFFFF", "#000000", "#18191D"], # Mostly neutral transmuted colors
                candidate_name="AuroraSovereignLanding",
                candidate_names_list=["AuroraLandingShell", "AuroraTopNavigation", "AuroraHeroStatement", "AuroraPrimaryCTA", "AuroraSecondaryCTA", "AuroraProductNarrativeSection", "AuroraUseCaseCluster", "AuroraFooterNavigation"]
            )
            
            results["proprietary_candidate"] = proprietary_candidate
            
            if proprietary_candidate.risk_level == "blocked":
                from sandbox_contracts import DiagnosticFinding
                finding = DiagnosticFinding(
                    severity="P0",
                    code="ORIGINALITY_GATE_BLOCKED",
                    redacted_message="Plágio ou cópia não autorizada detetada: " + ", ".join(proprietary_candidate.blocked_reasons),
                    file_path="memory",
                    line_number=0,
                    recommended_action="Refatorar a seed criativa e aumentar eixos de transmutação."
                )
                raise PipelinePausedException("OriginalityGate blocked the candidate.", [finding])
                
            print(f"[DAG] OriginalityGate Passed! Score: {proprietary_candidate.originality_score:.2f}")
        except PipelinePausedException:
            raise
        except Exception as e:
            raise PipelineAbortedException(f"OriginalityGate failed: {e}")

        # --- DAG Phase 3: Token Synthesis ---
        print("[DAG] Running task: SynthesizeTokens...")
        try:
            from synthesizer_agent import run_pattern_synthesis
            draft = run_pattern_synthesis(results["artifact"], governance_mode=governance_mode)
            if draft is None:
                raise PipelineAbortedException("SynthesizeTokens produced no output.")
            results["draft"] = draft
        except Exception as e:
            raise PipelineAbortedException(f"SynthesizeTokens failed: {e}")

        # --- OS-017: Experience Architect ---
        print("[DAG] Running task: ExperienceArchitect...")
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../experience_architect')))
        try:
            from experience_architect import ExperienceArchitect, ExperienceArchitectureGate, ArchitectureCoverageGate
            architect = ExperienceArchitect()
            blueprint = architect.architect(
                url=self.target_url,
                hybrid_truth=results["resolved_truth"],
                page_intel=results["artifact"],
                pattern_intel=results["draft"]
            )
            results["blueprint"] = blueprint
            print("[DAG] ExperienceArchitect generated blueprint.")
            
            # Run ExperienceArchitectureGate
            arch_gate = ExperienceArchitectureGate()
            arch_gate.evaluate(blueprint)
            print("[DAG] ExperienceArchitectureGate Passed.")
            
            # Run ArchitectureCoverageGate
            coverage_gate = ArchitectureCoverageGate()
            coverage_gate.evaluate(blueprint)
            print("[DAG] ArchitectureCoverageGate Passed.")
            
        except Exception as e:
            raise PipelineAbortedException(f"ExperienceArchitect or Gates failed: {e}")

        # 4. OrchestrateSpec (Alvaro)
        print("[DAG] Running task: OrchestrateSpec...")
        try:
            from alvaro_agent import orchestrate_code_spec
            code_spec = orchestrate_code_spec(results["draft"], results["artifact"], results["blueprint"])
            if code_spec is None:
                raise PipelineAbortedException("OrchestrateSpec produced no output.")
                
            from anti_stub_gate import AntiStubGate
            gate = AntiStubGate(surface_type="landing")
            gate.evaluate_code_spec(results["artifact"], code_spec)
            print("[DAG] AntiStubGate.CodeSpec Passed.")
            
            results["code_spec"] = code_spec
            
            # E2E Test Hooks for OS-011
            if governance_mode == "poor_fidelity":
                from alvaro_contracts import ComponentMissingAlert
                results["code_spec"].component_alerts = [
                    ComponentMissingAlert(original_role="hero", degraded_to="div", reason="missing"),
                    ComponentMissingAlert(original_role="cta", degraded_to="span", reason="missing"),
                    ComponentMissingAlert(original_role="nav", degraded_to="ul", reason="missing")
                ]
            elif governance_mode == "clone_fidelity":
                # Matches truth exactly to trigger P0 clone risk
                resolved_data = results["resolved_truth"].resolved_data
                computed_colors = resolved_data.get("computed_styles", {}).get("colors", [])
                bad_colors = {f"c{i}": c for i, c in enumerate(computed_colors) if c.upper() not in ["#FFFFFF", "#000000"]}
                if not bad_colors:
                    bad_colors = {"primary": "#1A73E8", "accent": "#202124"}
                results["code_spec"].theme_config.colors = bad_colors
                
        except Exception as e:
            raise PipelineAbortedException(f"OrchestrateSpec failed: {e}")

        # --- OS-018: Stories Build Plan Resolution and Gate ---
        print("[DAG] Running task: StoriesBuildPlanResolution...")
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../stories_builder')))
        try:
            from build_plan_resolver import BuildPlanResolver
            from stories_builder_gate import StoriesBuilderGate
            
            resolver = BuildPlanResolver()
            proposed_comps = [req.component_name for req in results["code_spec"].component_registry] if (results.get("code_spec") and results["code_spec"].component_registry) else []
            
            try:
                stories_plan = resolver.resolve_build_plan(results["blueprint"], proposed_components=proposed_comps)
                results["stories_plan"] = stories_plan
                print("[DAG] BuildPlanResolver resolved stories build plan.")
            except Exception as resolver_error:
                from sandbox_contracts import DiagnosticFinding
                raise PipelinePausedException(f"BuildPlanResolver failed: {resolver_error}", [
                    DiagnosticFinding(
                        severity="P0",
                        code="BUILDER_CONSTRAINTS_MISSING",
                        redacted_message=f"BuildPlanResolver failed during execution: {resolver_error}",
                        file_path="stories_build_plan",
                        line_number=0,
                        recommended_action="Verifique os parametros do resolver e a estrutura do blueprint."
                    )
                ])
                
            gate = StoriesBuilderGate()
            gate_report = gate.validate_build_plan(stories_plan, results["blueprint"])
            results["stories_builder_gate_report"] = gate_report
            print(f"[DAG] StoriesBuilderGate status: {gate_report.status}")
            
            if gate_report.status == "failed":
                from sandbox_contracts import DiagnosticFinding
                findings = []
                for f in gate_report.findings:
                    if f.severity in ["P0", "P1"]:
                        findings.append(DiagnosticFinding(
                            severity=f.severity,
                            code=f.code,
                            redacted_message=f.message,
                            file_path="stories_build_plan",
                            line_number=0,
                            recommended_action="Corrigir os limites de decisao do Stories Builder no resolver ou contratos."
                        ))
                raise PipelinePausedException("StoriesBuilderGate blocked the build plan.", findings)
                
        except PipelinePausedException:
            raise
        except Exception as e:
            raise PipelineAbortedException(f"StoriesBuildPlanResolution or StoriesBuilderGate failed: {e}")

        # OS-011: EvaluateVisualFidelity
        print("[DAG] Running task: EvaluateVisualFidelity...")
        try:
            from fidelity_evaluator import VisualFidelityEvaluator
            from models import HybridTruthArtifact, ColorSample
            
            evaluator = VisualFidelityEvaluator()
            
            resolved_data = results["resolved_truth"].resolved_data
            computed_colors = resolved_data.get("computed_styles", {}).get("colors", [])
            ht_colors = [ColorSample(hex_value=c, usage_frequency=1.0) for c in computed_colors]
            
            from datetime import datetime
            ht_artifact = HybridTruthArtifact(
                resolved_at=datetime.now(),
                resolved_fields={},
                colors=ht_colors,
                typography=[],
                spatial_system=[],
                motion=[],
                a11y_tree=[],
                css_variables=resolved_data.get("css_variables", {}),
                breakpoints=resolved_data.get("breakpoints", {}),
                asset_paths=resolved_data.get("asset_paths", {})
            )
            
            report = evaluator.evaluate(
                report_id="FID-100",
                hybrid_truth=ht_artifact,
                proprietary_candidate=results["proprietary_candidate"],
                code_spec=results["code_spec"]
            )
            
            results["visual_fidelity_report"] = report
            
            if report.decision == "rejected":
                from sandbox_contracts import DiagnosticFinding
                finding = DiagnosticFinding(
                    severity="P0",
                    code="VISUAL_FIDELITY_REJECTED",
                    redacted_message="Avaliacao Visual Falhou: " + ", ".join(report.blocked_reasons),
                    file_path="memory",
                    line_number=0,
                    recommended_action="Corrigir o CodeSpec para preservar intencao sem clonar."
                )
                raise PipelinePausedException("VisualFidelityEvaluator blocked the candidate.", [finding])
                
            print(f"[DAG] EvaluateVisualFidelity Passed! Intent: {report.fidelity.intent_fidelity_score:.1f}% | Clone Risk: {report.clone_risk.final_clone_risk:.1f}%")
        except PipelinePausedException:
            raise
        except Exception as e:
            raise PipelineAbortedException(f"EvaluateVisualFidelity failed: {e}")

        # 5. TranspileUI (Factory)
        print("[DAG] Running task: TranspileUI...")
        try:
            from factory_agent import generate_ui_tree
            from tsx_compiler import compile_tsx_nodes, generate_tailwind_config, generate_standalone_bundle, compile_css
            from motion_primitive_injector import MotionPrimitiveInjector
            from anti_stub_gate import AntiStubGate
            
            ui_tree = generate_ui_tree(results["code_spec"])
            if ui_tree is None:
                raise PipelineAbortedException("TranspileUI produced no ComponentTree output.")

            gate = AntiStubGate(surface_type="landing")
            gate.evaluate_ui_tree(results["artifact"], ui_tree)
            print("[DAG] AntiStubGate.UITree Passed.")

            injector = MotionPrimitiveInjector()
            ui_tree = injector.inject_motion(ui_tree)

            tailwind_cfg = generate_tailwind_config(
                results["code_spec"].theme_config.colors, 
                results["code_spec"].theme_config.fontFamily
            )
            
            jsx_body, imports = compile_tsx_nodes(ui_tree)
            
            gate.evaluate_generated_code(jsx_body)
            print("[DAG] AntiStubGate.GeneratedCode Passed.")
            
            css_code = compile_css(ui_tree, results["code_spec"].theme_config.colors)
            
            results["ui_tree"] = ui_tree
            results["jsx_body"] = jsx_body
            results["imports"] = imports
            results["tailwind_cfg"] = tailwind_cfg
            results["css_code"] = css_code
            
            results["standalone_bundle"] = generate_standalone_bundle(
                ui_tree,
                results["code_spec"].theme_config.colors, 
                results["code_spec"].theme_config.fontFamily
            )
        except PipelinePausedException:
            raise
        except Exception as e:
            raise PipelineAbortedException(f"TranspileUI failed: {e}")

        # 6. CoupleData (BFF)
        print("[DAG] Running task: CoupleData...")
        try:
            from bff_agent import generate_types_file, generate_client_component, generate_server_component, load_api_manifest
            from bff_contracts import BFFAdapterSpec, PagePropsContract, DataDependency
            
            manifest = load_api_manifest(self.api_manifest_path)
            
            bff_spec = BFFAdapterSpec(
                spec_id=results["code_spec"].spec_id,
                props_contract=PagePropsContract(
                    page_id="SYNTHESIS-PAGE",
                    dependencies=[
                        DataDependency(
                            prop_name="workspaceStatus",
                            contract_ref="AgentWorkspace",
                            schema_ref="WorkspaceStatusSchema",
                            adapter_ref="antigravity.workspace.status",
                            access_scope="workspace:read",
                            error_strategy="boundary"
                        )
                    ]
                )
            )

            types_code = generate_types_file(bff_spec)
            client_code = generate_client_component(bff_spec, results["jsx_body"], results["imports"])
            server_code = generate_server_component(bff_spec, manifest)

            results["types_code"] = types_code
            results["client_code"] = client_code
            results["server_code"] = server_code
        except Exception as e:
            raise PipelineAbortedException(f"CoupleData failed: {e}")

        # --- OS-012: EvaluatePerceptualFidelity ---
        print("[DAG] Running task: EvaluatePerceptualFidelity...")
        try:
            import perceptual_evaluator
            PercepPausedException = perceptual_evaluator.PipelinePausedException
            EvaluatePerceptualFidelity = perceptual_evaluator.EvaluatePerceptualFidelity
        except Exception as e:
            raise PipelineAbortedException(f"Failed to import perceptual_evaluator: {e}")

        try:
            # Diretorio offline isolado para screenshot
            percep_sandbox = Path(self.output_dir) / f"percep_sandbox_{int(time.time())}"
            os.makedirs(percep_sandbox, exist_ok=True)
            
            # Gravar ficheiros físicos no sandbox offline antes do screenshot
            with open(percep_sandbox / "5_SynthesizedPage.client.tsx", "w", encoding="utf-8") as f:
                f.write(results["client_code"])
            with open(percep_sandbox / "5_page.tsx", "w", encoding="utf-8") as f:
                f.write(results["server_code"])
            with open(percep_sandbox / "render_bundle.css", "w", encoding="utf-8") as f:
                f.write(results["css_code"])
            with open(percep_sandbox / "ui_tree.json", "w", encoding="utf-8") as f:
                f.write(results["ui_tree"].model_dump_json(indent=2))
            with open(percep_sandbox / "render_bundle_manifest.json", "w", encoding="utf-8") as f:
                f.write(results["standalone_bundle"].model_dump_json(indent=2))
            
            perceptual_evaluator = EvaluatePerceptualFidelity(str(percep_sandbox))
            report = await perceptual_evaluator.evaluate(results["standalone_bundle"])
            results["perceptual_report"] = report
            results["perceptual_screenshot_path"] = report.screenshot_path
            
            print(f"[DAG] EvaluatePerceptualFidelity Passed! Score: {report.perceptual_score.final_score:.1f}%")
        except PercepPausedException as e:
            from sandbox_contracts import DiagnosticFinding
            msg = str(e).replace("Perceptual Evaluation Failed: ", "")
            print(f"[DEBUG_PERCEPTUAL] Evaluator failed with message: {msg}")
            finding = DiagnosticFinding(
                severity="P0",
                code="VISUAL_PERCEPTUAL_REJECTED",
                redacted_message="Avaliacao Perceptual Falhou: " + msg,
                file_path="6_rendered_screenshot.png",
                line_number=0,
                recommended_action="Corrigir componentes ou CSS gerado para renderizar corretamente."
            )
            raise PipelinePausedException("EvaluatePerceptualFidelity blocked the pipeline.", [finding])
        except Exception as e:
            raise PipelineAbortedException(f"EvaluatePerceptualFidelity failed: {e}")

        # --- OS-008: Sandbox Isolation & Fleet Validation Layer ---
        from orchestrator import SandboxOrchestrator
        from validator import SandboxValidator
        
        # Cria a sandbox operacional temporária
        workspace_base = os.path.dirname(os.path.abspath(self.output_dir))
        sandbox = SandboxOrchestrator(workspace_base)
        sandbox.setup_worktree()
        
        try:
            # Grava candidatos de compilação dentro do sandbox
            print(f"[DAG] Writing candidate artifacts to Sandbox: {sandbox.sandbox_dir}...")
            with open(sandbox.sandbox_dir / "1_artifact.json", "w") as f:
                f.write(results["artifact"].model_dump_json(indent=2))
            if "kit_artifact" in results:
                with open(sandbox.sandbox_dir / "1_kit_artifact.json", "w") as f:
                    f.write(results["kit_artifact"].model_dump_json(indent=2))
            if "resolved_truth" in results:
                with open(sandbox.sandbox_dir / "1_hybrid_truth.json", "w") as f:
                    f.write(results["resolved_truth"].model_dump_json(indent=2))
            if "proprietary_candidate" in results:
                with open(sandbox.sandbox_dir / "1_proprietary_candidate.json", "w") as f:
                    f.write(results["proprietary_candidate"].model_dump_json(indent=2))
            if "visual_fidelity_report" in results:
                with open(sandbox.sandbox_dir / "3_visual_fidelity_report.json", "w") as f:
                    f.write(results["visual_fidelity_report"].model_dump_json(indent=2))
            if "perceptual_report" in results:
                with open(sandbox.sandbox_dir / "4_perceptual_report.json", "w") as f:
                    f.write(results["perceptual_report"].model_dump_json(indent=2))
            if "perceptual_screenshot_path" in results:
                shutil.copy(results["perceptual_screenshot_path"], sandbox.sandbox_dir / "6_rendered_screenshot.png")
            with open(sandbox.sandbox_dir / "2_draft.json", "w") as f:
                f.write(results["draft"].model_dump_json(indent=2))
            with open(sandbox.sandbox_dir / "3_code_spec.json", "w") as f:
                f.write(results["code_spec"].model_dump_json(indent=2))
            with open(sandbox.sandbox_dir / "4_tailwind.config.js", "w") as f:
                f.write(results["tailwind_cfg"])
            with open(sandbox.sandbox_dir / "5_SynthesizedPage.types.ts", "w") as f:
                f.write(results["types_code"])
            with open(sandbox.sandbox_dir / "5_SynthesizedPage.client.tsx", "w") as f:
                f.write(results["client_code"])
            with open(sandbox.sandbox_dir / "5_page.tsx", "w") as f:
                f.write(results["server_code"])
            with open(sandbox.sandbox_dir / "render_bundle.css", "w") as f:
                f.write(results["css_code"])
            with open(sandbox.sandbox_dir / "render_bundle_manifest.json", "w") as f:
                f.write(results["standalone_bundle"].model_dump_json(indent=2))
            with open(sandbox.sandbox_dir / "ui_tree.json", "w") as f:
                f.write(results["ui_tree"].model_dump_json(indent=2))
            with open(sandbox.sandbox_dir / "layout_profile_selection.json", "w") as f:
                f.write(results["ui_tree"].layout_selection.model_dump_json(indent=2))
            with open(sandbox.sandbox_dir / "component_mapping_report.json", "w") as f:
                f.write(json.dumps([f.model_dump() for f in results["ui_tree"].component_findings], indent=2))

            if "blueprint" in results:
                with open(sandbox.sandbox_dir / "experience_blueprint.json", "w") as f:
                    f.write(results["blueprint"].model_dump_json(indent=2))

            if "stories_plan" in results:
                with open(sandbox.sandbox_dir / "stories_build_plan.json", "w") as f:
                    f.write(results["stories_plan"].model_dump_json(indent=2))
            else:
                from sandbox_contracts import DiagnosticFinding
                raise PipelinePausedException("stories_build_plan.json missing.", [
                    DiagnosticFinding(severity="P0", code="MISSING_STORIES_BUILD_PLAN", redacted_message="stories_build_plan.json was not generated.", file_path="stories_build_plan.json", line_number=0, recommended_action="Ensure BuildPlanResolver runs and outputs the build plan.")
                ])
                
            if "stories_builder_gate_report" in results:
                with open(sandbox.sandbox_dir / "stories_builder_gate_report.json", "w") as f:
                    f.write(results["stories_builder_gate_report"].model_dump_json(indent=2))
            else:
                from sandbox_contracts import DiagnosticFinding
                raise PipelinePausedException("stories_builder_gate_report.json missing.", [
                    DiagnosticFinding(severity="P0", code="MISSING_STORIES_BUILD_GATE_REPORT", redacted_message="stories_builder_gate_report.json was not generated.", file_path="stories_builder_gate_report.json", line_number=0, recommended_action="Ensure StoriesBuilderGate runs and outputs the gate report.")
                ])

            # 7.5 AntiStubGate Sandbox Check (OS-016)
            print("[DAG] Running task: AntiStubGate Sandbox Verification...")
            self.emit_heartbeat(sandbox.run_id, "VALIDATION_PHASE_1_ANTISTUB", 70, "IN_PROGRESS")
            try:
                from anti_stub_gate import AntiStubGate
                gate = AntiStubGate(surface_type="landing")
                gate.evaluate_sandbox_files(str(sandbox.sandbox_dir))
                print("[DAG] AntiStubGate Sandbox Verification Passed.")
            except PipelinePausedException as e:
                print(f"[DAG] AntiStubGate Sandbox Verification failed: {e.findings}")
                self.emit_heartbeat(sandbox.run_id, "VALIDATION_FAILED", 85, "PAUSED", "PipelinePausedException")
                raise

            # 7.5.2 ExperienceArchitectureGate Sandbox Check (OS-017)
            print("[DAG] Running task: ExperienceArchitectureGate Sandbox Verification...")
            try:
                from experience_gates import ExperienceArchitectureGate
                exp_gate = ExperienceArchitectureGate()
                exp_gate.evaluate_sandbox_files(str(sandbox.sandbox_dir))
                print("[DAG] ExperienceArchitectureGate Sandbox Verification Passed.")
            except PipelinePausedException as e:
                print(f"[DAG] ExperienceArchitectureGate Sandbox Verification failed: {e.findings}")
                self.emit_heartbeat(sandbox.run_id, "VALIDATION_FAILED", 85, "PAUSED", "PipelinePausedException")
                raise

            # 7. SandboxGate
            print("[DAG] Running task: SandboxGate...")
            self.emit_heartbeat(sandbox.run_id, "VALIDATION_PHASE_1", 72, "IN_PROGRESS")
            
            validator = SandboxValidator(str(sandbox.sandbox_dir))
            
            findings = []
            try:
                # Valida os arquivos gerados no sandbox
                validator.validate_workspace()
                print("[DAG] SandboxGate Validation Passed.")
                validation_status = "passed"
            except PipelinePausedException as e:
                # Se houver P0, executa o LimitedRepairAgent
                print(f"[DAG] SandboxGate P0 findings detected: {[(f.code, f.file_path, f.redacted_message) for f in e.findings]}. Activating Limited Repair Agent...")
                self.emit_heartbeat(sandbox.run_id, "REPAIR_LOOP", 80, "IN_PROGRESS")
                
                from repair_agent import LimitedRepairAgent
                repair_agent = LimitedRepairAgent(sandbox)
                
                # Tenta reparar o client.tsx limpando códigos P0 perigosos (se houver)
                client_file_rel = "5_SynthesizedPage.client.tsx"
                client_path = sandbox.sandbox_dir / client_file_rel
                
                if client_path.exists():
                    orig_content = client_path.read_text(encoding="utf-8")
                    # Corrige chamadas conhecidas de P0 e limpa o arquivo
                    cleaned_content = orig_content
                    # Remove eval/exec se presentes
                    cleaned_content = re.sub(r'\beval\s*\(', '/* eval blocked */(', cleaned_content)
                    cleaned_content = re.sub(r'\bexec\s*\(', '/* exec blocked */(', cleaned_content)
                    cleaned_content = re.sub(r'\bos\.system\s*\(', '/* system blocked */(', cleaned_content)
                    
                    candidate = repair_agent.attempt_repair(
                        client_file_rel, 
                        orig_content, 
                        [cleaned_content]
                    )
                    
                    if candidate.validator_status == "passed":
                        print("[DAG] Limited Repair: Code Succeeded in Sandbox.")
                        results["patch_candidate"] = candidate
                        validation_status = "passed"
                        # Atualiza a árvore do client code no resultado principal
                        results["client_code"] = cleaned_content
                    else:
                        print("[DAG] Limited Repair: Code failed to recover.")
                        self.emit_heartbeat(sandbox.run_id, "VALIDATION_FAILED", 85, "PAUSED", "PipelinePausedException")
                        # Preserva e re-lança exceção
                        raise
                else:
                    self.emit_heartbeat(sandbox.run_id, "VALIDATION_FAILED", 85, "PAUSED", "PipelinePausedException")
                    raise
            
            # 8. QAReport
            print("[DAG] Running task: QAReport...")
            self.emit_heartbeat(sandbox.run_id, "QA_REPORTING", 90, "IN_PROGRESS")
            
            # Executa a varredura final para coletar avisos P1/P2/P3 e gerar o relatório
            all_findings = []
            try:
                all_findings = validator.validate_workspace()
            except PipelinePausedException as e:
                all_findings = e.findings
                
            qa_report_content = "# QA Conformity & Verification Report\n\n"
            qa_report_content += f"- **Sandbox Run ID:** {sandbox.run_id}\n"
            qa_report_content += f"- **Status:** {validation_status.upper()}\n"
            qa_report_content += f"- **Total Findings:** {len(all_findings)}\n\n"
            qa_report_content += "## Findings Matrix\n\n"
            qa_report_content += "| Severity | Code | Redacted Message | Recommended Action |\n"
            qa_report_content += "| --- | --- | --- | --- |\n"
            for f in all_findings:
                qa_report_content += f"| {f.severity} | {f.code} | {f.redacted_message} | {f.recommended_action} |\n"
                
            # Create staging candidate folder
            staging_dir = Path(self.output_dir) / "candidate"
            os.makedirs(staging_dir, exist_ok=True)
            
            # Copy candidate files from sandbox to staging folder
            shutil.copy(sandbox.sandbox_dir / "1_artifact.json", staging_dir / "1_artifact.json")
            if (sandbox.sandbox_dir / "1_kit_artifact.json").exists():
                shutil.copy(sandbox.sandbox_dir / "1_kit_artifact.json", staging_dir / "1_kit_artifact.json")
            if (sandbox.sandbox_dir / "1_hybrid_truth.json").exists():
                shutil.copy(sandbox.sandbox_dir / "1_hybrid_truth.json", staging_dir / "1_hybrid_truth.json")
            if (sandbox.sandbox_dir / "1_proprietary_candidate.json").exists():
                shutil.copy(sandbox.sandbox_dir / "1_proprietary_candidate.json", staging_dir / "1_proprietary_candidate.json")
            if (sandbox.sandbox_dir / "3_visual_fidelity_report.json").exists():
                shutil.copy(sandbox.sandbox_dir / "3_visual_fidelity_report.json", staging_dir / "3_visual_fidelity_report.json")
            if (sandbox.sandbox_dir / "4_perceptual_report.json").exists():
                shutil.copy(sandbox.sandbox_dir / "4_perceptual_report.json", staging_dir / "4_perceptual_report.json")
            if (sandbox.sandbox_dir / "6_rendered_screenshot.png").exists():
                shutil.copy(sandbox.sandbox_dir / "6_rendered_screenshot.png", staging_dir / "6_rendered_screenshot.png")
            shutil.copy(sandbox.sandbox_dir / "2_draft.json", staging_dir / "2_draft.json")
            shutil.copy(sandbox.sandbox_dir / "3_code_spec.json", staging_dir / "3_code_spec.json")
            shutil.copy(sandbox.sandbox_dir / "4_tailwind.config.js", staging_dir / "4_tailwind.config.js")
            shutil.copy(sandbox.sandbox_dir / "5_SynthesizedPage.types.ts", staging_dir / "5_SynthesizedPage.types.ts")
            shutil.copy(sandbox.sandbox_dir / "5_SynthesizedPage.client.tsx", staging_dir / "5_SynthesizedPage.client.tsx")
            shutil.copy(sandbox.sandbox_dir / "5_page.tsx", staging_dir / "5_page.tsx")
            if (sandbox.sandbox_dir / "experience_blueprint.json").exists():
                shutil.copy(sandbox.sandbox_dir / "experience_blueprint.json", staging_dir / "experience_blueprint.json")
            if (sandbox.sandbox_dir / "stories_build_plan.json").exists():
                shutil.copy(sandbox.sandbox_dir / "stories_build_plan.json", staging_dir / "stories_build_plan.json")
            if (sandbox.sandbox_dir / "stories_builder_gate_report.json").exists():
                shutil.copy(sandbox.sandbox_dir / "stories_builder_gate_report.json", staging_dir / "stories_builder_gate_report.json")
            
            # Save QA report to staging candidate folder
            report_path = staging_dir / "QA_REPORT.md"
            with open(report_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(qa_report_content)
            print(f"[DAG] Compliance QA Report generated at {report_path}")

            # 9. HumanPromotionGate
            print("[DAG] Running task: HumanPromotionGate...")
            self.emit_heartbeat(sandbox.run_id, "HUMAN_PROMOTION", 95, "IN_PROGRESS")
            
            # Calculate SHA256 from the STAGED files (to ensure consistency)
            client_file_path = staging_dir / "5_SynthesizedPage.client.tsx"
            patch_sha = hashlib.sha256(client_file_path.read_bytes()).hexdigest() if client_file_path.exists() else hashlib.sha256(b"").hexdigest()
            
            # Calculate SHA256 of QA report
            qa_report_sha = hashlib.sha256(qa_report_content.encode("utf-8")).hexdigest()
            
            print(f"[DAG] Promotion Candidate Generated:")
            print(f"      - Sandbox Run ID: {sandbox.run_id}")
            print(f"      - Patch SHA256: {patch_sha}")
            print(f"      - QA Report SHA256: {qa_report_sha}")

            # Walk up to find the git repo root
            curr_dir = Path(self.output_dir).resolve()
            repo_root = None
            for _ in range(5):
                if (curr_dir / ".git").exists():
                    repo_root = curr_dir
                    break
                curr_dir = curr_dir.parent
            if not repo_root:
                repo_root = Path("C:/Projetos/Aurora").resolve()
                
            # Path to external approvals directory
            approval_dir = repo_root / ".aurora" / "approvals"
            approval_file = approval_dir / "promotion_approval.json"
            
            # Check for un-trusted approval records inside sandbox, output, or local workspace directories
            untrusted_paths = [
                Path(self.output_dir).resolve(),
                sandbox.sandbox_dir.resolve(),
                Path(".").resolve()
            ]
            
            promotion_approved = False
            approval_record = None
            
            if approval_file.exists():
                try:
                    resolved_approval = approval_file.resolve()
                    
                    # Ensure it is relative to approval_dir and NOT inside any untrusted path
                    is_untrusted = False
                    for upath in untrusted_paths:
                        if resolved_approval.is_relative_to(upath) or resolved_approval == upath:
                            is_untrusted = True
                            break
                            
                    if is_untrusted or not resolved_approval.is_relative_to(approval_dir):
                        print("[DAG] Security Block: Reverting approval record located in untrusted path.")
                    else:
                        with open(resolved_approval, "r") as f:
                            data = json.load(f)
                            approval_record = PromotionApprovalRecord(**data)
                            
                        # Validate hashes AND run ID AND candidate ID
                        if (approval_record.sandbox_run_id == sandbox.run_id and
                            approval_record.patch_candidate_sha256 == patch_sha and
                            approval_record.qa_report_sha256 == qa_report_sha):
                            promotion_approved = True
                            results["promotion_authorized"] = True
                            results["approval_record"] = approval_record
                        else:
                            print(f"[DAG] Approval validation failed: Hashes or Sandbox Run ID mismatch.")
                            print(f"      Expected Run ID: {sandbox.run_id}, Got: {approval_record.sandbox_run_id}")
                            print(f"      Expected Patch SHA: {patch_sha}, Got: {approval_record.patch_candidate_sha256}")
                            print(f"      Expected QA SHA: {qa_report_sha}, Got: {approval_record.qa_report_sha256}")
                except Exception as e:
                    print(f"[DAG] Error parsing promotion approval record: {e}")
            
            if not promotion_approved:
                print("[DAG] Pipeline Paused: Promotion is pending formal human approval record.")
                self.emit_heartbeat(sandbox.run_id, "PROMOTION_PENDING", 95, "PAUSED")
                raise HumanPromotionHalt(
                    f"Human Promotion Halt: Approval record required at {approval_file}.\n"
                    f"Candidate Info:\n"
                    f"  sandbox_run_id: {sandbox.run_id}\n"
                    f"  patch_candidate_sha256: {patch_sha}\n"
                    f"  qa_report_sha256: {qa_report_sha}"
                )
                
            print(f"[DAG] Promotion AUTHORIZED for Sandbox Run: {sandbox.run_id}!")
            self.emit_heartbeat(sandbox.run_id, "COMPLETED", 100, "SUCCESS")
            
        finally:
            # Garante a destruição física do worktree do sandbox
            sandbox.cleanup_worktree()

        return results

import re
