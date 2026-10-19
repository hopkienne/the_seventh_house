"""Read-only world-bound inspection of an opened modular Blender source."""
import json
from pathlib import Path
import bpy
from mathutils import Vector


def bounds(obj):
    points = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
    # Convert Blender Z-up back to authored Godot Y-up coordinates.
    points = [(v.x, v.z, -v.y) for v in points]
    return ([min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)])


meshes = [o for o in bpy.data.objects if o.type == 'MESH']
assert meshes and not bpy.data.libraries and not bpy.data.images
assert bpy.context.scene.unit_settings.system == 'METRIC'
assert bpy.context.scene.unit_settings.scale_length == 1
assert tuple(bpy.data.objects['ModuleRoot'].location) == (0,0,0)
assert tuple(bpy.data.objects['SocketStart'].location) == (0,0,0)
assert tuple(bpy.data.objects['SocketEnd'].location) == (2,0,0)
for obj in bpy.data.objects:
    assert tuple(obj.scale) == (1,1,1) and obj.matrix_world.determinant() > 0
for obj in meshes:
    assert obj.data.uv_layers and obj.data.materials and len(obj.data.polygons)
boxes = [bounds(o) for o in meshes]
low = [min(b[0][i] for b in boxes) for i in range(3)]
high = [max(b[1][i] for b in boxes) for i in range(3)]
assert abs(low[0]) < 1e-5 and abs(low[1]) < 1e-5 and abs(high[0]-2) < 1e-5
report = dict(result='PASS',source=Path(bpy.data.filepath).name,meshes=len(meshes),
              bounds_min=low,bounds_max=high,pivot=[0,0,0],sockets=[[0,0,0],[2,0,0]],
              all_scales_identity=True,external_images=0,external_libraries=0)
if 'JambLeft' in bpy.data.objects:
    left, right = bounds(bpy.data.objects['JambLeft']), bounds(bpy.data.objects['JambRight'])
    report['door_frame_clear_width'] = right[0][0] - left[1][0]
    report['door_frame_clear_height'] = bounds(bpy.data.objects['Lintel'])[0][1]
    assert abs(report['door_frame_clear_width']-1.25) < 1e-5
    assert abs(report['door_frame_clear_height']-2.25) < 1e-5
print('MODULAR_SOURCE_REVIEW '+json.dumps(report))
