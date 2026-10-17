# Hard Constraints: Blender Headless Pipeline

A falta de uma `View3D` (interface gráfica) em modo headless faz com que 90% das funções da família `bpy.ops` quebrem com `RuntimeError: context is incorrect`.

## REGRA ESTRITA 01: Proibição de `bpy.ops` para Geometria
É estritamente proibido utilizar `bpy.ops.mesh.*` (ex: `bpy.ops.mesh.primitive_cube_add`) para gerar ou manipular geometria.

## REGRA ESTRITA 02: Uso Obrigatório de `bmesh`
Toda criação e manipulação espacial deve ser feita acessando a memória dos vértices através do módulo `bmesh`.

**Exemplo Mandatório (Como criar malhas em headless):**
```python
import bpy
import bmesh

# 1. Cria a malha e o objeto de dados limpos
mesh = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh)
bpy.context.collection.objects.link(obj)

# 2. Inicializa o bmesh
bm = bmesh.new()

# 3. Cria a geometria matematicamente (Ex: um plano)
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=2.0)

# 4. Escreve a geometria de volta para a malha do Blender e limpa a memória
bm.to_mesh(mesh)
bm.free()
```

## Exceções Permitidas para `bpy.ops`

Você só pode usar `bpy.ops` para:

1. Exportação (`bpy.ops.export_scene.gltf()`)
2. Operações de UV/Bake (mediante seleção explícita via código).
