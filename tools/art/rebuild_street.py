"""Rebuild into a NEW repository directory; optional explicit installation of generated assets."""
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
        raise ValueError('Use a new output directory; do not overwrite prior evidence')
    lock = json.loads((ROOT/'config/blender.lock.json').read_text())
    binary = (ROOT/lock['binary_path']).resolve()
    binary.relative_to(ROOT)
    with binary.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != lock['binary_sha256']:
            raise ValueError('Blender binary differs from verified lock')
    command = [str(binary), '--background', '--factory-startup', '--python-exit-code', '1',
               '--python', str(ROOT/'tools/art/build_street_blender.py'), '--', '--output-root', str(output)]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
    if not output.is_dir():
        raise RuntimeError('Blender failed before creating output: '+process.stderr[-2000:])
    (output/'build.stdout.log').write_text(process.stdout, encoding='utf-8')
    (output/'build.stderr.log').write_text(process.stderr, encoding='utf-8')
    if process.returncode != 0 or 'STREET_EXPORT' not in process.stdout:
        raise RuntimeError('Blender generation failed; inspect output logs')
    metrics = json.loads((output/'blockout_street.metrics.json').read_text())
    if args.install:
        for directory, filename in [('art/source', 'blockout_street.blend'), ('art/export', 'blockout_street.glb'),
                                    ('art/export', 'blockout_street.metrics.json')]:
            target = ROOT/directory/filename
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(output/filename, target)
        prefab = ROOT/'scenes/environment/street_blockout.tscn'
        text = prefab.read_text(encoding='utf-8')
        before = text[text.index('collision_ids = '):text.index('\n\n[node name="Visuals"')]
        ids = ', '.join(json.dumps(o['name']) for o in metrics['meshes'] if o['collision'])
        prefab.write_text(text.replace(before, 'collision_ids = PackedStringArray('+ids+')'), encoding='utf-8')
    print(json.dumps({'result': 'PASS', 'output_root': str(output), 'installed': args.install,
                      'semantic_sha256': metrics['semantic_sha256'], 'glb_sha256': metrics['glb_sha256']}))


if __name__ == '__main__':
    main()
