# Otimização Canônica para React Three Fiber (WebGL)

O objetivo final de todo código gerado é ser renderizado a 60fps no navegador. Modelos devem ser entregues no formato `.glb`.

## Protocolo Rígido de Bake (Iluminação e Texturas)
Baking automático em scripts headless é propenso a falhas se o motor de renderização ou o mapa UV não estiverem configurados. O `ceo-3d` DEVE incluir este bloco de código antes de qualquer operação de Bake:

```python
# PASSO 1: Forçar Engine para CYCLES (Eevee não suporta bake nativo)
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'CPU' # Evita crash se não houver GPU no host

# PASSO 2: Garantir que o objeto alvo é o ativo e está selecionado
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# PASSO 3: Desdobramento UV Automático (Obrigatório para texturas não colidirem)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=1.15192) # 66 graus
bpy.ops.object.mode_set(mode='OBJECT')

# PASSO 4: Executar Bake e Exportar .GLB
# ... (lógica de bake aqui) ...
```

## Diretrizes de Otimização no Blender (`bpy`)
1. **Polygon Count (Contagem de Polígonos)**
   Aplica modificador *Decimate* programaticamente antes de exportar, se o payload orçamentário exigir (`poly_budget`).
2. **Formato de Exportação (glTF/GLB)**
   O formato OBRIGATÓRIO é `.glb` (binário).
3. **Escala e Eixos**
   O Blender usa Z-Up, o Three.js usa Y-Up. O exportador oficial glTF faz essa conversão automaticamente, contudo, garanta que a escala dos objetos esteja aplicada (`Ctrl+A -> Scale` visualmente; via código: `bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)`).
