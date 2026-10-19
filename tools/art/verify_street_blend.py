"""Read-only verification, run Blender --background SOURCE.blend --python this file."""
import json
import bpy
from mathutils import Vector


def bounds(name):
    obj = bpy.data.objects[name]
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    points = [(p.x, p.z, -p.y) for p in points]
    return ([min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)])


meshes = [o for o in bpy.data.objects if o.type == 'MESH']
left, right = bounds('DoorJambWest'), bounds('DoorJambEast')
header, street = bounds('DoorHeader'), bounds('StreetSlab')
width = right[0][0] - left[1][0]
height = header[0][1] - street[1][1]
corridor = street[1][2] - street[0][2]
assert len(meshes) == 56
assert abs(width - 1.25) < 1e-5 and abs(height - 2.25) < 1e-5
assert abs(corridor - 4.0) < 1e-5
assert bpy.context.scene.unit_settings.system == 'METRIC'
assert bpy.context.scene.unit_settings.scale_length == 1.0
assert all(len(o.data.uv_layers) and len(o.data.materials) and len(o.data.polygons) for o in meshes)
assert not bpy.data.libraries and not bpy.data.images
print('BLEND_SOURCE_REVIEW ' + json.dumps({'result': 'PASS', 'meshes': len(meshes),
       'door_width_measured': width, 'door_height_measured': height, 'corridor_width_measured': corridor,
       'external_libraries': len(bpy.data.libraries), 'external_images': len(bpy.data.images),
       'tool_version': bpy.app.version_string, 'source_path': bpy.data.filepath}))
