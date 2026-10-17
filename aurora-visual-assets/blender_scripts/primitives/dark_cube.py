import bpy
import bmesh
import sys

# REGRA 01: Limpeza Absoluta
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    # REGRA 02: Uso Obrigatório de bmesh
    mesh = bpy.data.meshes.new("DarkCubeMesh")
    obj = bpy.data.objects.new("DarkCube", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    
    # Cria o cubo usando bmesh puramente matemático
    bmesh.ops.create_cube(bm, size=2.0)
    
    # Escreve de volta para a malha
    bm.to_mesh(mesh)
    bm.free()

    # Aplicação do Material (Estilo Dark)
    mat = bpy.data.materials.new(name="DarkMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
    obj.data.materials.append(mat)

    # Otimização WebGL: Cycles Engine
    bpy.context.scene.render.engine = 'CYCLES'
    
    # Garante seleção
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # UV Smart Project (Obrigatório antes de Bakes/Texturas)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.15192)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Parseia o path de output enviado pelo executor
    argv = sys.argv
    try:
        index = argv.index("--output")
        output_path = argv[index + 1]
    except (ValueError, IndexError):
        output_path = "dark_cube.glb"

    # Exceção permitida: bpy.ops para exportação GLB
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_materials='EXPORT',
        export_normals=True,
        export_apply=True
    )
    
    print(f"Artefato exportado com sucesso: {output_path}")

except Exception as e:
    import traceback
    print("ERRO INTERNO NO SCRIPT DO BLENDER:", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)
