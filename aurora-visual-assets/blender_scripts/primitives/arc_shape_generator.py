import bpy
import bmesh
import sys
import math
import os

# REGRA 01: Limpeza Absoluta
bpy.ops.wm.read_factory_settings(use_empty=True)

def create_torus_bmesh(bm, major_radius=0.9, minor_radius=0.22, segments_u=48, segments_v=24):
    verts = []
    for i in range(segments_u):
        u = 2 * math.pi * i / segments_u
        cos_u = math.cos(u)
        sin_u = math.sin(u)
        for j in range(segments_v):
            v = 2 * math.pi * j / segments_v
            cos_v = math.cos(v)
            sin_v = math.sin(v)
            
            x = (major_radius + minor_radius * cos_v) * cos_u
            y = (major_radius + minor_radius * cos_v) * sin_u
            z = minor_radius * sin_v
            
            verts.append(bm.verts.new((x, y, z)))
            
    bm.verts.ensure_lookup_table()
    
    for i in range(segments_u):
        i_next = (i + 1) % segments_u
        for j in range(segments_v):
            j_next = (j + 1) % segments_v
            
            idx1 = i * segments_v + j
            idx2 = i_next * segments_v + j
            idx3 = i_next * segments_v + j_next
            idx4 = i * segments_v + j_next
            
            bm.faces.new((verts[idx1], verts[idx2], verts[idx3], verts[idx4]))

def deform_mesh_noise(bm, amplitude=0.2, frequency=2.0, state_name=""):
    for v in bm.verts:
        pos = v.co
        # Ruído trigonométrico complexo para organicidade
        noise = math.sin(pos.x * frequency) * math.cos(pos.y * frequency) * math.sin(pos.z * frequency)
        # Adiciona harmônica secundária
        noise += 0.5 * math.sin(pos.y * frequency * 2.0) * math.cos(pos.z * frequency * 2.0)
        
        # Deslocamento
        if state_name == "ALERT_ACTIVE":
            # Deformação pulsante e irregular
            normal = pos.normalized()
            v.co += normal * (noise * amplitude)
        elif state_name == "GOAL_ACHIEVED":
            # Ondas suaves ao longo da geometria
            normal = pos.normalized()
            v.co += normal * (math.sin(pos.x * 3.0) * amplitude * 0.5)
        elif state_name == "BLOCKED_FLOW":
            # Ângulos pontiagudos
            normal = pos.normalized()
            v.co += normal * (math.copysign(amplitude, noise) * 0.4)
        else:
            # Padrão suave
            normal = pos.normalized()
            v.co += normal * (noise * amplitude)

def set_socket(bsdf, socket_name, value):
    socket = bsdf.inputs.get(socket_name)
    if socket:
        socket.default_value = value

def create_shape(state_name):
    mesh = bpy.data.meshes.new("ArcShapeMesh")
    obj = bpy.data.objects.new("ArcShape", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    if state_name == "GOAL_ACHIEVED":
        # Torus grande ondulado
        create_torus_bmesh(bm, major_radius=0.95, minor_radius=0.26)
        deform_mesh_noise(bm, amplitude=0.15, frequency=3.0, state_name=state_name)
    elif state_name == "ALERT_ACTIVE":
        # Cubo orgânico muito deformado
        bmesh.ops.create_cube(bm, size=1.6)
        # Subdivide para ter resolução para deformação
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=4, use_grid_fill=True)
        deform_mesh_noise(bm, amplitude=0.35, frequency=2.5, state_name=state_name)
    elif state_name == "BLOCKED_FLOW":
        # Icosaedro cristalino afiado
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.1)
        deform_mesh_noise(bm, amplitude=0.2, frequency=4.0, state_name=state_name)
    elif state_name == "STABLE_OPERATION":
        # Torus fino suave
        create_torus_bmesh(bm, major_radius=0.9, minor_radius=0.2)
        deform_mesh_noise(bm, amplitude=0.08, frequency=1.5, state_name=state_name)
    elif state_name == "NEUTRAL_OBSERVING":
        # Esfera perfeita
        bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    else:
        # Fallback: Torus básico
        create_torus_bmesh(bm, major_radius=0.9, minor_radius=0.22)
        deform_mesh_noise(bm, amplitude=0.1, frequency=2.0, state_name=state_name)
        
    bm.to_mesh(mesh)
    bm.free()
    
    # Suaviza faces
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # Cria material
    mat = bpy.data.materials.new(name="ArcMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    if bsdf:
        if state_name == "GOAL_ACHIEVED":
            # Ouro polido premium
            set_socket(bsdf, 'Base Color', (0.85, 0.65, 0.15, 1.0))
            set_socket(bsdf, 'Metallic', 1.0)
            set_socket(bsdf, 'Roughness', 0.12)
        elif state_name == "ALERT_ACTIVE":
            # Vermelho incandescente
            set_socket(bsdf, 'Base Color', (0.85, 0.05, 0.05, 1.0))
            set_socket(bsdf, 'Metallic', 0.2)
            set_socket(bsdf, 'Roughness', 0.3)
            # Tenta ativar emissivo
            set_socket(bsdf, 'Emission Color', (0.4, 0.0, 0.0, 1.0))
        elif state_name == "BLOCKED_FLOW":
            # Cristal roxo metálico escuro
            set_socket(bsdf, 'Base Color', (0.08, 0.02, 0.2, 1.0))
            set_socket(bsdf, 'Metallic', 0.8)
            set_socket(bsdf, 'Roughness', 0.15)
        elif state_name == "STABLE_OPERATION":
            # Verde/Teal seda
            set_socket(bsdf, 'Base Color', (0.05, 0.7, 0.45, 1.0))
            set_socket(bsdf, 'Metallic', 0.3)
            set_socket(bsdf, 'Roughness', 0.18)
        else: # NEUTRAL_OBSERVING
            # Aço escovado neutro
            set_socket(bsdf, 'Base Color', (0.35, 0.38, 0.42, 1.0))
            set_socket(bsdf, 'Metallic', 0.85)
            set_socket(bsdf, 'Roughness', 0.32)
            
    obj.data.materials.append(mat)
    
    # Configura engine Cycles para baking posterior
    bpy.context.scene.render.engine = 'CYCLES'
    
    # Garante seleção
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Smart UV Project
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.15192)
    bpy.ops.object.mode_set(mode='OBJECT')

def main():
    argv = sys.argv
    try:
        index = argv.index("--output")
        output_path = argv[index + 1]
    except (ValueError, IndexError):
        output_path = "arc_shape.glb"
        
    try:
        state_index = argv.index("--state")
        state_name = argv[state_index + 1]
    except (ValueError, IndexError):
        state_name = "NEUTRAL_OBSERVING"
        
    print(f"Iniciando geracao de forma do ARC para estado: {state_name}")
    create_shape(state_name)
    
    # Exporta em GLB
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_materials='EXPORT',
        export_normals=True,
        export_apply=True
    )
    print(f"Modelo GLB do ARC exportado em: {output_path}")

if __name__ == "__main__":
    main()
