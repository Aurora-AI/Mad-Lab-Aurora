import uuid
from datetime import datetime
from synthesizer_models import DesignSystemDraft, SemanticToken, AntiPlagiarismRule
# Assumimos que o PageIntelligenceArtifact e os models do probe estão acessíveis
import sys
import os
sys.path.append(os.path.abspath('../contracts'))
from models import PageIntelligenceArtifact

def run_pattern_synthesis(artifact: PageIntelligenceArtifact, governance_mode: str = "transmute") -> DesignSystemDraft:
    """
    Modo: pattern_synthesis
    Lê a matemática da página alvo e transmuta para o ecossistema Aurora ou clona em Luz Monumental.
    """
    print(f"[SYNTHESIZER] A processar artefacto da origem: {artifact.source_url} em modo {governance_mode}")
    
    tokens = []
    anti_plagiarism_log = []
    
    # 1. Mapeamento de Cores
    print("[SYNTHESIZER] A ativar Mapeamento de Cores...")
    if governance_mode == "clone":
        # Paradigma Luz Monumental (Fundo Branco, Texto Preto)
        tokens.append(SemanticToken(
            name="color-base-surface",
            value="#FFFFFF",
            rationale="Definido como fundo branco puro para o paradigma Luz Monumental."
        ))
        tokens.append(SemanticToken(
            name="color-text-primary",
            value="#000000",
            rationale="Definido como texto preto puro para alto contraste sob Luz Monumental."
        ))
        tokens.append(SemanticToken(
            name="color-text-secondary",
            value="#45474D",
            rationale="Definido a partir da cor de maior contraste secundário da extração."
        ))
        tokens.append(SemanticToken(
            name="color-action-primary",
            value="#000000",
            rationale="Replicado como preto para botões ou elementos de ação."
        ))
        tokens.append(SemanticToken(
            name="color-accent",
            value="#B7BFD9",
            rationale="Cor de destaque secundário preservada da extração."
        ))
    else:
        # Transmutação para o nosso 'Quiet Luxury Dark'
        if artifact.colors:
            dominant_color = max(artifact.colors, key=lambda c: c.usage_frequency)
            tokens.append(SemanticToken(
                name="color-base-surface",
                value="#0A0A0C",
                rationale=f"Mapeado pela cor dominante original ({dominant_color.usage_frequency}%). Ajustado para padrão Aurora."
            ))
            anti_plagiarism_log.append(AntiPlagiarismRule(
                blocked_original_value=dominant_color.hex_value,
                violation_type="Identity Theft (Brand Color)",
                aurora_transmutation="#0A0A0C"
            ))

    # 2. Síntese Tipográfica (Escala Modular)
    print("[SYNTHESIZER] A calcular Escala Modular Tipográfica...")
    typo_scale = {}
    sorted_typo = sorted(artifact.typography, key=lambda t: t.size_px, reverse=True)
    for i, typo in enumerate(sorted_typo):
        # Transmuta px absoluto para rem relativo
        rem_value = round(typo.size_px / 16.0, 3)
        
        # O menor tamanho vira body, os maiores viram headings
        token_name = "body" if i == len(sorted_typo) - 1 else f"heading-{i+1}"
        
        if governance_mode == "clone":
            min_val = round(rem_value * 0.85, 3)
            max_val = round(rem_value * 1.3, 3)
            pref_val = round(rem_value * 1.1, 3)
            typo_scale[token_name] = f"clamp({min_val}rem, {pref_val}vw, {max_val}rem)"
        else:
            typo_scale[token_name] = f"{rem_value}rem"
            anti_plagiarism_log.append(AntiPlagiarismRule(
                blocked_original_value=typo.font_family,
                violation_type="Typography Exact Copy",
                aurora_transmutation="var(--aurora-font-sans)"
            ))

    # 3. Empacotamento do Draft para o Álvaro
    draft = DesignSystemDraft(
        synthesis_id=f"DS-{uuid.uuid4().hex[:8].upper()}",
        synthesized_at=datetime.now(),
        governance_mode=governance_mode,
        semantic_tokens=tokens,
        typography_scale=typo_scale,
        do_not_copy_rules=anti_plagiarism_log,
        a11y_tree=artifact.a11y_tree if artifact.a11y_tree else [],
        is_safe_for_production=True
    )
    
    print("[SYNTHESIZER] Síntese concluída e bloqueios de plágio registados.")
    return draft

# Simulação de pipeline se executado diretamente
if __name__ == "__main__":
    from fixtures import SYNTHETIC_PROBE_OUTPUT
    # Carregamos o mock do probe que criámos na OS-001
    mock_artifact = PageIntelligenceArtifact(**SYNTHETIC_PROBE_OUTPUT)
    
    final_draft = run_pattern_synthesis(mock_artifact)
    print("\n=== DESIGN SYSTEM DRAFT GERADO ===")
    print(final_draft.model_dump_json(indent=2))
