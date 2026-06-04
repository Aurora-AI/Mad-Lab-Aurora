from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional, List
import sys
import os

# Ajuste de path para importação dos contratos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))
from factory_contracts import ComponentTree, UINode

MotionPrimitive = Literal["fade_in", "subtle_lift", "press_scale", "focus_reveal"]

class MotionConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    primitive: MotionPrimitive
    duration_ms: Optional[int] = Field(default=300, alias="durationMs")
    delay_ms: Optional[int] = Field(default=0, alias="delayMs")
    easing: Optional[Literal["ease-out", "ease-in-out", "spring"]] = Field(default="ease-out")
    intensity: Optional[Literal["low", "medium"]] = Field(default="medium")
    reduced_motion_fallback: Literal["none", "opacity", "static"] = Field(default="opacity", alias="reducedMotionFallback")

class MotionPrimitiveInjector:
    def __init__(self):
        # Mapeamento estrito das classes Tailwind usando prefixos padrão
        self.primitive_classes = {
            "fade_in": ["transition-opacity", "opacity-100"],
            "subtle_lift": ["transition-all", "hover:motion-safe:-translate-y-1", "hover:motion-safe:shadow-md"],
            "press_scale": ["transition-transform", "active:motion-safe:scale-95"],
            "focus_reveal": ["transition-all", "focus:motion-safe:ring-2", "focus:motion-safe:ring-offset-2"]
        }

    def _get_fallback_classes(self, config: MotionConfig) -> List[str]:
        """Aplica o fallback de reduced-motion conforme política de acessibilidade."""
        if config.reduced_motion_fallback == "opacity":
            return ["motion-reduce:transition-opacity", "motion-reduce:duration-100"]
        elif config.reduced_motion_fallback == "none":
            return ["motion-reduce:transition-none"]
        # static: sem classes adicionais
        return []

    def inject_node_motion(self, node: UINode, config: MotionConfig) -> UINode:
        """Valida a configuração e injeta as classes de motion correspondentes no nó."""
        # Garante validação pelo contrato tipado
        validated_config = MotionConfig.model_validate(config)
        
        # Coleta classes com base no primitive permitido
        classes = list(self.primitive_classes.get(validated_config.primitive, []))
        fallback_classes = self._get_fallback_classes(validated_config)
        
        # Adiciona duração e delay caso customizados
        if validated_config.duration_ms:
            classes.append(f"motion-safe:duration-{validated_config.duration_ms}")
        if validated_config.delay_ms:
            classes.append(f"motion-safe:delay-{validated_config.delay_ms}")
            
        # Adiciona easing
        if validated_config.easing == "ease-out":
            classes.append("motion-safe:ease-out")
        elif validated_config.easing == "ease-in-out":
            classes.append("motion-safe:ease-in-out")
        elif validated_config.easing == "spring":
            # Mapeia spring para uma curva de rebote cúbico rápida para CSS/Tailwind
            classes.append("motion-safe:ease-[cubic-bezier(0.34,1.56,0.64,1)]")
            
        # Insere as classes de motion no nó sem duplicidades
        current_classes = node.props.get("className", "").split()
        for cls in classes + fallback_classes:
            if cls not in current_classes:
                current_classes.append(cls)
                
        node.props["className"] = " ".join(current_classes)
        # Registra a configuração de motion nas props do nó
        node.props["motionConfig"] = validated_config.model_dump(by_alias=True)
        return node

    def inject_motion(self, tree: ComponentTree) -> ComponentTree:
        """Injeta motion default nos elementos correspondentes da árvore de componentes."""
        
        def _traverse(node: UINode):
            # Injeta fade_in se for a tag raiz ou main/section/AuroraContainer
            if node.component_name in ["main", "section", "AuroraContainer"]:
                config = MotionConfig(
                    primitive="fade_in",
                    durationMs=300,
                    reducedMotionFallback="opacity"
                )
                self.inject_node_motion(node, config)
            # Injeta press_scale se for botão/link
            elif node.component_name in ["button", "AuroraButton", "AuroraLink"]:
                config = MotionConfig(
                    primitive="press_scale",
                    durationMs=150,
                    reducedMotionFallback="static"
                )
                self.inject_node_motion(node, config)
                
            if node.children:
                for child in node.children:
                    _traverse(child)

        _traverse(tree.root_node)
        return tree
