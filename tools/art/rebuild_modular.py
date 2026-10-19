"""Rebuild pinned Blender modules to a new repository folder; explicit --install optional."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', required=True)
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    output = (ROOT/args.output_root).resolve()
    output.relative_to(ROOT)
    if output.exists():
        raise ValueError('Use a new output directory to preserve earlier runs')
    lock = json.loads((ROOT/'config/blender.lock.json').read_text())
    binary = (ROOT/lock['binary_path']).resolve()
    binary.relative_to(ROOT)
    with binary.open('rb') as stream:
        assert hashlib.file_digest(stream,'sha256').hexdigest() == lock['binary_sha256']
    command = [str(binary),'--background','--factory-startup','--python-exit-code','1',
               '--python',str(ROOT/'tools/art/build_modular_blender.py'),'--','--output-root',str(output)]
    result = subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    if not output.is_dir():
        raise RuntimeError(result.stdout+result.stderr)
    (output/'build.stdout.log').write_text(result.stdout,encoding='utf-8')
    (output/'build.stderr.log').write_text(result.stderr,encoding='utf-8')
    if result.returncode or 'MODULAR_EXPORT' not in result.stdout:
        raise RuntimeError('Generation failed; inspect output build logs')
    metrics = json.loads((output/'modular_kit.metrics.json').read_text())
    if args.install:
        for item in metrics:
            name = item['id']
            for extension, directory in [('blend','art/source/modular'),('glb','art/export/blockout')]:
                target = ROOT/directory/(name+'.'+extension)
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(output/(name+'.'+extension),target)
            folder = ROOT/'scenes/environment/modules'
            folder.mkdir(parents=True,exist_ok=True)
            ids = ', '.join(json.dumps(m['name']) for m in item['meshes'] if m['collision'])
            endpoint = ', '.join(format(value, 'g') for value in item['sockets'][1])
            text = f'''[gd_scene load_steps=3 format=3]

[ext_resource type="PackedScene" path="res://art/export/blockout/{name}.glb" id="1_visual"]
[ext_resource type="Script" path="res://scripts/art/street_blockout.gd" id="2_collision"]

[node name="{name}" type="Node3D"]
script = ExtResource("2_collision")
collision_ids = PackedStringArray({ids})

[node name="Visuals" parent="." instance=ExtResource("1_visual")]

[node name="SocketStart" type="Marker3D" parent="."]

[node name="SocketEnd" type="Marker3D" parent="."]
position = Vector3({endpoint})
'''
            (folder/(name+'.tscn')).write_text(text,encoding='utf-8')
        shutil.copyfile(output/'modular_kit.metrics.json',ROOT/'art/export/blockout/modular_kit.metrics.json')
    print(json.dumps(dict(result='PASS',installed=args.install,modules=len(metrics),output_root=str(output))))


if __name__ == '__main__':
    main()
