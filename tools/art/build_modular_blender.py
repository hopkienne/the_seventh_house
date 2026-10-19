"""Pinned Blender background generator. Four independent source/GLB modules, Godot metres.

Origin is ground/left endpoint, sockets at X=0 and X=2. Reorient with rotations,
never reflected scale. Config/seed are deterministic; no random geometry input.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
import bmesh

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-root', required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    output = (ROOT / args.output_root).resolve()
    output.relative_to(ROOT)
    output.mkdir(parents=True, exist_ok=False)
    config_path = ROOT / 'tools/art/modular_kit.json'
    config = json.loads(config_path.read_text())
    palette_path = (ROOT / config['palette_config']).resolve()
    palette_path.relative_to(ROOT)
    palette = json.loads(palette_path.read_text())['materials']
    width, height, depth = config['width_m'], config['wall_height_m'], config['wall_depth_m']
    opening, clearance = config['door_clear_width_m'], config['door_clear_height_m']
    assert width % config['grid_m'] == 0 and opening > 0.56 and clearance > 1.7
    manifests = []
    for module in config['modules']:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 1.0
        bpy.context.preferences.filepaths.save_version = 0
        origin = bpy.data.objects.new('ModuleRoot', None)
        bpy.context.collection.objects.link(origin)
        origin['asset_id'] = module['asset_id']
        records = []
        materials = {}
        for name in ['Wood', 'Plaster']:
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            mat.diffuse_color = palette[name]
            bsdf = mat.node_tree.nodes.get('Principled BSDF')
            bsdf.inputs['Base Color'].default_value = palette[name]
            bsdf.inputs['Roughness'].default_value = 0.9
            materials[name] = mat

        def box(name, size, at, material, collision=True):
            x, y, z = [v / 2 for v in size]
            points = [(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),
                      (-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
            faces = [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(0,1,5,4),(3,7,6,2)]
            mesh = bpy.data.meshes.new(name+'_Mesh')
            mesh.from_pydata([(vx, -vz, vy) for vx,vy,vz in points], [], faces)
            assert not mesh.validate(), name
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
            bm.to_mesh(mesh)
            bm.free()
            mesh.update()
            uv = mesh.uv_layers.new(name='UVMap')
            for polygon in mesh.polygons:
                axis = max(range(3), key=lambda i: abs(polygon.normal[i]))
                axes = [i for i in range(3) if i != axis]
                for loop in polygon.loop_indices:
                    v = mesh.vertices[mesh.loops[loop].vertex_index].co
                    uv.data[loop].uv = (v[axes[0]], v[axes[1]])
            obj = bpy.data.objects.new(name, mesh)
            bpy.context.collection.objects.link(obj)
            obj.parent = origin
            obj.location = (at[0], -at[2], at[1])
            mesh.materials.append(materials[material])
            obj['asset_id'] = module['asset_id']
            obj['collision'] = collision
            records.append(dict(name=name, material=material, collision=collision, triangles=12,
                                bounds_min=[round(at[i]-size[i]/2,6) for i in range(3)],
                                bounds_max=[round(at[i]+size[i]/2,6) for i in range(3)]))

        kind = module['kind']
        if kind == 'fence':
            for index, x in enumerate([0.05, width-0.05]):
                box('Post%02d'%index, (0.1,1.0,0.14), (x,0.5,0), 'Wood')
            for index, y in enumerate([0.35,0.65]):
                box('Rail%02d'%index, (width-0.2,0.12,0.1), (width/2,y,0), 'Wood')
            for index in range(7):
                x = 0.25 + index*0.25
                box('Picket%02d'%index, (0.075,0.9,0.08), (x,0.45,0.095), 'Wood')
        elif kind == 'wall':
            box('PlasterPanel', (width,height,depth), (width/2,height/2,0), 'Plaster')
        else:
            jamb = (width-opening)/2
            for name, x in [('Left',jamb/2),('Right',width-jamb/2)]:
                box('Jamb'+name, (jamb,clearance,depth), (x,clearance/2,0), 'Wood')
            box('Lintel', (width,height-clearance,depth), (width/2,(clearance+height)/2,0), 'Plaster')
            box('HeaderTrim', (opening,0.12,0.04), (width/2,clearance+0.06,depth/2+0.02), 'Wood')
            for name, sign in [('Left',-1),('Right',1)]:
                if kind == 'door_open':
                    x = width/2 + sign*(opening/2+0.06)
                    box('FoldedLeaf'+name, (0.06,clearance-0.06,opening/2),
                        (x,(clearance-0.06)/2,-opening/4), 'Wood')
                else:
                    x = width/2 + sign*opening/4
                    box('ClosedLeaf'+name, (opening/2,clearance-0.06,0.08),
                        (x,(clearance-0.06)/2,0), 'Wood')
                    box('Handle'+name, (0.035,0.17,0.04),
                        (width/2+sign*0.08,1.05,0.06), 'Wood', False)
        # Author sockets in source as well as Godot prefab for direct source reuse.
        for name, x in [('SocketStart',0),('SocketEnd',width)]:
            obj = bpy.data.objects.new(name, None)
            bpy.context.collection.objects.link(obj)
            obj.parent = origin
            obj.location.x = x
            obj.empty_display_type = 'ARROWS'
            obj.empty_display_size = 0.15
        bpy.context.view_layer.update()
        assert all(tuple(o.scale) == (1,1,1) and o.matrix_world.determinant() > 0
                   for o in bpy.data.objects)
        source = output/(module['id']+'.blend')
        runtime = output/(module['id']+'.glb')
        bpy.ops.wm.save_as_mainfile(filepath=str(source), compress=False, check_existing=False)
        bpy.ops.export_scene.gltf(filepath=str(runtime),export_format='GLB',export_yup=True,
                                  export_apply=True,export_animations=False,export_cameras=False,
                                  export_lights=False,export_extras=True,
                                  export_copyright='Original modular project geometry authored locally by Codex')
        record = dict(**module, generator_version=config['generator_version'],seed=config['seed'],
                      quality_state='BLOCKOUT',phase='SHARED',unit='metre',grid_m=config['grid_m'],
                      pivot=[0,0,0],sockets=[[0,0,0],[width,0,0]],meshes=records,
                      triangles=sum(x['triangles'] for x in records),
                      tool_version=bpy.app.version_string,config_sha256=sha(config_path),
                      palette_sha256=sha(palette_path))
        record['semantic_sha256'] = hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        record['glb_sha256'] = sha(runtime)
        manifests.append(record)
    (output/'modular_kit.metrics.json').write_text(json.dumps(manifests,indent=2)+'\n',encoding='utf-8')
    print('MODULAR_EXPORT '+json.dumps(dict(result='PASS',modules=len(manifests),triangles=sum(x['triangles'] for x in manifests))))


if __name__ == '__main__':
    main()
