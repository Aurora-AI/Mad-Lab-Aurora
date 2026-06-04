import re
from typing import Any, List, Dict
from sandbox_contracts import PipelinePausedException, DiagnosticFinding
from models import PageIntelligenceArtifact
from alvaro_contracts import FrontendCodeSpec
from factory_contracts import ComponentTree, UINode

class AntiStubGate:
    def __init__(self, surface_type: str = "landing"):
        self.surface_type = surface_type

    def _get_depth_threshold(self) -> float:
        if self.surface_type == "landing":
            return 0.45
        elif self.surface_type == "crm_surface":
            return 0.35
        elif self.surface_type == "minimal_source":
            return 0.30
        return 0.35 # Default

    def evaluate_page_intelligence(self, artifact: PageIntelligenceArtifact) -> None:
        """
        Valida que o artefato extraído da página real contém informação rica, não apenas um esqueleto vazio.
        """
        findings = []
        
        if not artifact.visible_texts:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="EMPTY_PAGE_INTELLIGENCE",
                redacted_message="A página origem não retornou textos visíveis. Não há contexto para transmutar.",
                file_path="memory",
                line_number=0,
                recommended_action="Verificar se o alvo está num iframe ou necessita de bypass de bot."
            ))
            
        if self.surface_type == "landing" and not artifact.headings:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="LANDING_NO_HEADINGS",
                redacted_message="Uma landing page foi submetida mas nenhum heading foi extraído.",
                file_path="memory",
                line_number=0,
                recommended_action="Certificar que a arquitetura da página origem expõe semântica H1-H6 ou role=heading."
            ))

        if findings:
            raise PipelinePausedException("AntiStubGate: Page Intelligence falhou na validação base.", findings)

    def evaluate_code_spec(self, page_artifact: PageIntelligenceArtifact, code_spec: FrontendCodeSpec) -> None:
        """
        Garante que o FrontendCodeSpec contém os componentes essenciais mapeados do PageIntelligence.
        """
        # Se a origem tinha botões/CTAs, o Spec deve ter pelo menos um componente iterável ou call to action.
        findings = []
        if page_artifact.buttons:
            has_cta_in_spec = any("Button" in comp.component_name or "CTA" in comp.component_name for comp in code_spec.component_registry)
            if not has_cta_in_spec:
                findings.append(DiagnosticFinding(
                    severity="P1",
                    code="SPEC_MISSING_CTA",
                    redacted_message="A página origem possui CTAs/Botões, mas nenhum componente equivalente foi requisitado no FrontendCodeSpec.",
                    file_path="memory",
                    line_number=0,
                    recommended_action="O Alvaro deve orquestrar botões se a intenção original possui botões."
                ))
                
        # Check 5: Botões repetidos sem label proprietário único devem gerar P1.
        cta_components = [c for c in code_spec.component_registry if "CTA" in c.component_name or "Button" in c.component_name]
        cta_labels = [c.label for c in cta_components if c.label]
        
        # If there are duplicates in labels
        duplicates = set([lbl for lbl in cta_labels if cta_labels.count(lbl) > 1])
        if duplicates:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="REPEATED_CTA_LABELS",
                redacted_message=f"Botões repetidos com labels não-únicos detetados: {duplicates}. Cada CTA deve ter função e label distintos.",
                file_path="3_code_spec.json",
                line_number=0,
                recommended_action="Injetar labels proprietários e funções únicas para cada botão/CTA."
            ))
                
        if findings:
            raise PipelinePausedException("AntiStubGate: FrontendCodeSpec falhou na cobertura de intenção.", findings)

    def _calc_ui_tree_depth(self, node: UINode, current_depth: int = 1) -> int:
        if not node.children:
            return current_depth
        return max(self._calc_ui_tree_depth(child, current_depth + 1) for child in node.children)

    def evaluate_ui_tree(self, page_artifact: PageIntelligenceArtifact, ui_tree: ComponentTree) -> None:
        """
        Avalia a métrica estrutural correta. Profundidade relativa e cobertura semântica.
        """
        findings = []
        
        ui_depth = self._calc_ui_tree_depth(ui_tree.root_node)
        max_dom_depth = max(page_artifact.dom_depth, 1) # Evita div por zero
        
        structural_depth_ratio = ui_depth / max_dom_depth
        threshold = self._get_depth_threshold()
        
        print(f"[DEBUG_ANTISTUB] ui_depth: {ui_depth}, max_dom_depth: {max_dom_depth}, ratio: {structural_depth_ratio:.2f}, threshold: {threshold:.2f}")

        if structural_depth_ratio < threshold:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="STRUCTURAL_INTENT_COLLAPSE",
                redacted_message=f"Profundidade estrutural gerada ({ui_depth}) vs origem ({max_dom_depth}) = {structural_depth_ratio:.2f}. Minimo esperado: {threshold:.2f}",
                file_path="memory",
                line_number=0,
                recommended_action="O site gerado está demasiado raso. Re-orquestrar mantendo a complexidade das seções."
            ))
            
        # 8. Cobertura semântica e Rácio de Labels únicos (OS-016)
        semantic_roles_in_source = set(node.role for node in page_artifact.a11y_tree if node.role)
        ui_roles = set()
        labels = []
        has_heading = False
        
        def collect_ui_metrics(node: UINode):
            nonlocal has_heading
            if node.semantic_role:
                ui_roles.add(node.semantic_role)
            if "Heading" in node.component_name or node.semantic_role == "heading":
                has_heading = True
            if node.text_content:
                labels.append(node.text_content.strip())
            for c in node.children:
                collect_ui_metrics(c)
                
        collect_ui_metrics(ui_tree.root_node)
        
        # Calcular semantic_coverage_ratio
        if semantic_roles_in_source:
            semantic_coverage_ratio = len(ui_roles.intersection(semantic_roles_in_source)) / len(semantic_roles_in_source)
        else:
            semantic_coverage_ratio = 1.0
            
        print(f"[DEBUG_ANTISTUB] semantic_coverage_ratio: {semantic_coverage_ratio:.2f}")
        if semantic_coverage_ratio < 0.5:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="POOR_SEMANTIC_COVERAGE",
                redacted_message=f"Cobertura semântica baixa ({semantic_coverage_ratio:.2f} < 0.5). A UI gerada não representa a semântica da origem.",
                file_path="ui_tree.json",
                line_number=0,
                recommended_action="Melhorar a transcrição dos componentes semânticos a partir da a11y_tree."
            ))
            
        # Calcular unique_label_coverage
        clean_labels = [l for l in labels if l]
        if clean_labels:
            unique_label_coverage = len(set(clean_labels)) / len(clean_labels)
        else:
            unique_label_coverage = 1.0
            
        print(f"[DEBUG_ANTISTUB] unique_label_coverage: {unique_label_coverage:.2f}")
        if unique_label_coverage < 0.6:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="POOR_UNIQUE_LABEL_COVERAGE",
                redacted_message=f"Rácio de labels únicos baixo ({unique_label_coverage:.2f} < 0.6). Indica repetição excessiva ou falta de copy proprietária.",
                file_path="ui_tree.json",
                line_number=0,
                recommended_action="Assegurar que cada nó de texto gerado possui copy única baseada na origem."
            ))

        if page_artifact.headings and not has_heading:
            findings.append(DiagnosticFinding(
                severity="P1",
                code="STRUCTURAL_INTENT_COLLAPSE",
                redacted_message="A intenção de Heading principal colapsou. A AST não possui Heading.",
                file_path="memory",
                line_number=0,
                recommended_action="Garantir que a hierarquia tipográfica foi preservada."
            ))

        if findings:
            raise PipelinePausedException("AntiStubGate: ComponentTree sofreu colapso de intenção estrutural.", findings)

    def evaluate_generated_code(self, tsx_body: str) -> None:
        """
        Inspeciona o código final buscando stubs e placeholders literais injetados no código (entre tags ou em aspas simples/duplas para atributos relevantes).
        """
        findings = []
        
        # Regexes mais seguros para não apanhar props/imports
        # Procura por "Button" apenas se for texto livre (ex: >Button<, ou aria-label="Button")
        blocked_terms = [
            r'>\s*Lorem ipsum.*?<',
            r'>\s*Hello World\s*<',
            r'>\s*Placeholder\s*<',
            r'>\s*Generated by pipeline\s*<',
            r'>\s*Automatically transformed candidate\s*<',
            r'>\s*transmuted_hero\s*<',
            r'>\s*aurora_cta\s*<',
            r'>\s*Título Principal\s*<',
            r'>\s*Ação\s*<',
            r'>\s*AuroraProprietaryDesign\s*<'
        ]
        
        # Especial para Button. Procura ">Button<" ou "> Button <"
        blocked_terms.append(r'>\s*Button\s*<')
        blocked_terms.append(r'aria-label=[\'"]Button[\'"]')
        
        for term in blocked_terms:
            if re.search(term, tsx_body, re.IGNORECASE):
                findings.append(DiagnosticFinding(
                    severity="P0",
                    code="PLACEHOLDER_INJECTED",
                    redacted_message=f"Termo proibido encontrado no código gerado: Matches {term}",
                    file_path="5_SynthesizedPage.client.tsx",
                    line_number=0,
                    recommended_action="Assegurar que o Alvaro gera texto proprietário baseado na função semântica, não mock estático."
                ))
                
        if findings:
            raise PipelinePausedException("AntiStubGate: TSX contém placeholders reprovados.", findings)

    def evaluate_rendered_dom_text(self, rendered_text: str) -> None:
        """
        Inspeciona o `document.body.innerText` final após renderização no Perceptual Evaluator.
        """
        findings = []
        
        exact_match_blocks = ["Lorem ipsum", "Placeholder", "Hello World", "Título Principal", "AuroraProprietaryDesign", "Automatically transformed candidate", "Generated by pipeline", "transmuted_hero", "aurora_cta"]
        for block in exact_match_blocks:
            if block.lower() in rendered_text.lower():
                findings.append(DiagnosticFinding(
                    severity="P0",
                    code="PLACEHOLDER_RENDERED",
                    redacted_message=f"Termo literal de stub/placeholder '{block}' foi detetado no texto visível renderizado no ecrã.",
                    file_path="render_bundle",
                    line_number=0,
                    recommended_action="O texto renderizado deve corresponder a copy final derivado da função original."
                ))
                
        # Regex para "Ação" com limites de palavra
        if re.search(r'\bAção\b', rendered_text, re.IGNORECASE):
            findings.append(DiagnosticFinding(
                severity="P0",
                code="PLACEHOLDER_RENDERED",
                redacted_message="Termo literal de stub/placeholder 'Ação' foi detetado no texto visível com limite de palavra.",
                file_path="render_bundle",
                line_number=0,
                recommended_action="O texto renderizado deve corresponder a copy final derivado da função original."
            ))

        # Regex para palavras soltas "Button"
        if re.search(r'\bButton\b', rendered_text, re.IGNORECASE):
            findings.append(DiagnosticFinding(
                severity="P0",
                code="PLACEHOLDER_RENDERED",
                redacted_message="A palavra solta 'Button' foi detetada no texto renderizado. O botão precisa de copy funcional real.",
                file_path="render_bundle",
                line_number=0,
                recommended_action="Fornecer copy funcional no lugar de 'Button'."
            ))

        if findings:
            raise PipelinePausedException("AntiStubGate: Rendered DOM contém placeholders P0.", findings)

    def evaluate_sandbox_files(self, sandbox_dir_path: str) -> None:
        """
        Escaneia todos os ficheiros candidatos na diretoria da sandbox para bloquear placeholders proibidos (OS-016).
        """
        import os
        from pathlib import Path
        
        sandbox_dir = Path(sandbox_dir_path)
        findings = []
        
        files_to_check = [
            "1_proprietary_candidate.json",
            "2_draft.json",
            "3_code_spec.json",
            "ui_tree.json",
            "5_SynthesizedPage.client.tsx"
        ]
        
        forbidden_placeholders = [
            "Título Principal",
            "Ação",
            "Placeholder",
            "Lorem ipsum",
            "Button",
            "Hello World",
            "AuroraProprietaryDesign",
            "Automatically transformed candidate",
            "Generated by pipeline",
            "transmuted_hero",
            "aurora_cta"
        ]
        
        for fname in files_to_check:
            fpath = sandbox_dir / fname
            if not fpath.exists():
                continue
                
            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
                
            for term in forbidden_placeholders:
                if term.lower() == "button":
                    pattern = r'"(?:label|text_content|transformed_text|text|generated_name|implementation_guidance|transformed_description)"\s*:\s*"[^"]*\bButton\b[^"]*"'
                    if re.search(pattern, content, re.IGNORECASE) or re.search(r'>\s*Button\s*<', content, re.IGNORECASE):
                        findings.append(DiagnosticFinding(
                            severity="P0",
                            code="PLACEHOLDER_INJECTED",
                            redacted_message=f"Placeholder proibido '{term}' encontrado no ficheiro '{fname}'.",
                            file_path=fname,
                            line_number=0,
                            recommended_action=f"Corrigir o ficheiro para usar texto real transmutado."
                        ))
                elif term.lower() == "ação":
                    if re.search(r'\bAção\b', content, re.IGNORECASE):
                        findings.append(DiagnosticFinding(
                            severity="P0",
                            code="PLACEHOLDER_INJECTED",
                            redacted_message=f"Placeholder proibido '{term}' encontrado no ficheiro '{fname}'.",
                            file_path=fname,
                            line_number=0,
                            recommended_action=f"Corrigir o ficheiro para usar texto real transmutado."
                        ))
                else:
                    if term.lower() in content.lower():
                        findings.append(DiagnosticFinding(
                            severity="P0",
                            code="PLACEHOLDER_INJECTED",
                            redacted_message=f"Placeholder proibido '{term}' encontrado no ficheiro '{fname}'.",
                            file_path=fname,
                            line_number=0,
                            recommended_action=f"Corrigir o ficheiro para usar texto real transmutado."
                        ))
                        
        if findings:
            raise PipelinePausedException("AntiStubGate: Ficheiros candidatos contêm placeholders P0.", findings)
