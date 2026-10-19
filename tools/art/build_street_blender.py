"""Run with pinned Blender --background --factory-startup --python ... -- --output-root DIR.

Coordinates below are authored in Godot metres, X/Y/Z with Y up; convert to
Blender (X,-Z,Y). glTF Y-up export reverses that basis conversion.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='tools/art/street_blockout.json')
    parser.add_argument('--output-root', required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    config_path = (ROOT / args.config).resolve()
    config_path.relative_to(ROOT)
    config = json.loads(config_path.read_text(encoding='utf-8'))
    output = (ROOT / args.output_root).resolve()
    output.relative_to(ROOT)
    output.mkdir(parents=True, exist_ok=False)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.preferences.filepaths.save_version = 0
    origin = bpy.data.objects.new('StreetKit', None)
    bpy.context.collection.objects.link(origin)
    materials = {}
    records = []
    for name, color in config['materials'].items():
        material = bpy.data.materials.new(name)
        material.diffuse_color = color
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 0.9
        materials[name] = material

    def mesh(name, vertices, faces, at, material, collision=True):
        # Godot sanitizes punctuation in node names. Author the stable runtime
        # IDs directly so collider references cannot silently miss bench legs.
        name = re.sub(r'[^A-Za-z0-9_]', '_', name)
        data = bpy.data.meshes.new(name + '_Mesh')
        data.from_pydata([(x, -z, y) for x, y, z in vertices], [], faces)
        data.update()
        assert not data.validate(), 'Invalid generated topology: ' + name
        bm = bmesh.new()
        bm.from_mesh(data)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(data)
        bm.free()
        data.update()
        uv = data.uv_layers.new(name='UVMap')
        for polygon in data.polygons:
            axis = max(range(3), key=lambda i: abs(polygon.normal[i]))
            dimensions = [i for i in range(3) if i != axis]
            for loop in polygon.loop_indices:
                point = data.vertices[data.loops[loop].vertex_index].co
                uv.data[loop].uv = (point[dimensions[0]], point[dimensions[1]])
        obj = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(obj)
        obj.parent = origin
        obj.location = (at[0], -at[2], at[1])
        obj.data.materials.append(materials[material])
        obj['asset_id'] = config['asset_id']
        obj['collision'] = collision
        obj['quality_state'] = 'BLOCKOUT'
        godot_points = [[round(v[i] + at[i], 6) for i in range(3)] for v in vertices]
        records.append({'name': name, 'material': material, 'collision': collision,
                        'bounds_min': [min(v[i] for v in godot_points) for i in range(3)],
                        'bounds_max': [max(v[i] for v in godot_points) for i in range(3)],
                        'vertices': len(data.vertices), 'triangles': sum(len(p.vertices)-2 for p in data.polygons),
                        'uv_loops': len(data.uv_layers.active.data), 'scale': list(obj.scale)})
        return obj

    def box(name, size, at, material, collision=True):
        x, y, z = [v / 2 for v in size]
        return mesh(name, [(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),
                           (-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)],
                    [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(0,1,5,4),(3,7,6,2)], at, material, collision)

    street, house, roof = config['street'], config['house'], config['roof']
    assert street['clear_width'] >= 4 and house['door_width'] > 0.56 and house['door_height'] > 1.7
    box('StreetSlab', (street['length'], street['slab_depth'], street['clear_width']), (0,-0.1,0), 'StreetStone')
    box('HouseSlab', (8,0.2,5.6), (0,-0.1,-4.8), 'HouseFloor')
    box('NearCurb', (18,0.25,0.16), (0,0.125,2.08), 'StreetStone')
    box('WestCurb', (0.16,0.25,4.16), (-9.08,0.125,0), 'StreetStone')
    box('EastCurb', (0.16,0.25,4.16), (9.08,0.125,0), 'StreetStone')
    width, height, thickness = house['width'], house['wall_height'], house['wall_thickness']
    door, door_height = house['door_width'], house['door_height']
    front, back = house['front_z'], house['back_z']
    segment = (width - door) / 2
    for sign, side in [(-1,'West'),(1,'East')]:
        box('FrontWall'+side, (segment,height,thickness), (sign*(door/2+segment/2),height/2,front-thickness/2), 'Plaster')
        box('SideWall'+side, (thickness,height,front-back), (sign*(width/2-thickness/2),height/2,(front+back)/2), 'Plaster')
        box('DoorJamb'+side, (0.12,door_height,0.24), (sign*(door/2+0.06),door_height/2,front), 'Wood')
        box('OpenDoorLeaf'+side, (0.08,2.12,0.65), (sign*(door/2+0.16),1.06,front-0.38), 'Wood')
        box('WindowRecess'+side, (1.05,1.0,0.05), (sign*1.98,1.65,front+0.01), 'WindowDark')
        for k in range(5):
            box('WindowLouver'+side+str(k), (1.07,0.075,0.08), (sign*1.98,1.25+k*0.2,front+0.06), 'Wood', False)
    box('FrontLintelWall', (door,height-door_height,thickness), (0,(door_height+height)/2,front-thickness/2), 'Plaster')
    box('DoorHeader', (door+0.24,0.14,0.24), (0,door_height+0.07,front), 'Wood')
    box('BackWall', (width,height,thickness), (0,height/2,back+thickness/2), 'Plaster')
    for index, x in enumerate([-2.95,-1.42,1.42,2.95]):
        box('VerandaPost%02d'%index, (0.16,2.9,0.16), (x,1.45,-2.25), 'Wood')
    box('VerandaBeam', (6.7,0.18,0.22), (0,2.92,-2.25), 'Wood')
    half, rf, rb = roof['width']/2, roof['front_z'], roof['back_z']
    y, ridge, middle = roof['eave_y'], roof['ridge_y'], (rf+rb)/2
    mesh('ClayGableRoof', [(-half,y,rf),(-half,y,rb),(-half,ridge,middle),
                           (half,y,rf),(half,y,rb),(half,ridge,middle)],
         [(0,1,2),(3,5,4),(0,3,4,1),(0,2,5,3),(1,4,5,2)], (0,0,0), 'ClayRoof')
    box('RoofRidge', (roof['width']+0.12,0.13,0.18), (0,ridge+0.055,middle), 'RidgeClay')
    for side in [-1,1]:
        for k in range(6):
            x = side*(5.3+k*0.58)
            box('FencePost_%s_%s'%(side,k), (0.10,0.8,0.10), (x,0.4,2.15), 'Wood')
        box('FenceRail_%s'%side, (3.1,0.10,0.09), (side*6.75,0.58,2.15), 'Wood')
    box('BenchSeat', (1.4,0.09,0.42), (-4.7,0.45,-2.8), 'Wood')
    for x in [-0.52,0.52]:
        for z in [-0.12,0.12]:
            box('BenchLeg_%s_%s'%(x,z), (0.09,0.405,0.09), (-4.7+x,0.2025,-2.8+z), 'Wood')
    profile = [(0,0.18),(0.12,0.28),(0.48,0.3),(0.72,0.17)]
    vertices = [(radius*math.cos(i*math.tau/10),level,radius*math.sin(i*math.tau/10)) for level,radius in profile for i in range(10)]
    faces = [tuple(reversed(range(10))), tuple(range(30,40))]
    for row in range(3):
        for i in range(10): faces.append((row*10+i,row*10+(i+1)%10,(row+1)*10+(i+1)%10,(row+1)*10+i))
    mesh('EarthenJar', vertices, faces, (4.4,0,-2.85), 'EarthJar')
    # A slatted rear opening makes the house depth legible in the blockout.
    box('BackWindowPanel', (1.1,0.85,0.06), (0,1.65,back+0.2), 'Wood', False)
    bpy.context.view_layer.update()
    assert all(all(abs(v-1)<1e-8 for v in obj.scale) for obj in bpy.data.objects if obj.type=='MESH')
    blend = output/'blockout_street.blend'
    glb = output/'blockout_street.glb'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=False,check_existing=False)
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',export_yup=True,
                              export_apply=True,export_animations=False,export_cameras=False,export_lights=False,
                              export_extras=True,export_copyright='Original project geometry generated by Codex for The Seventh House')
    semantic = {'asset_id':config['asset_id'],'generator_version':config['generator_version'],
                'seed':config['seed'],'unit':'metre','scale_length':bpy.context.scene.unit_settings.scale_length,
                'quality_state':'BLOCKOUT','phase_membership':'SHARED','meshes':records,
                'measurements':{'corridor_width':street['clear_width'],'door_clear_width':door,'door_clear_height':door_height,
                                'player_capsule_height':1.7,'player_capsule_diameter':0.56}}
    semantic['semantic_sha256'] = hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    semantic['tool_version'] = bpy.app.version_string
    semantic['config_sha256'] = hashlib.sha256(config_path.read_bytes()).hexdigest()
    semantic['glb_sha256'] = hashlib.sha256(glb.read_bytes()).hexdigest()
    (output/'blockout_street.metrics.json').write_text(json.dumps(semantic,indent=2),encoding='utf-8')
    print('STREET_EXPORT '+json.dumps({'result':'PASS','meshes':len(records),'triangles':sum(m['triangles'] for m in records),'semantic_sha256':semantic['semantic_sha256']}))


if __name__ == '__main__':
    main()
