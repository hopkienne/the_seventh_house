"""Pinned process helpers. Software ICD selection is explicit and subprocess-scoped."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def lock():
    return json.loads((ROOT / 'config/toolchain.lock.json').read_text(encoding='utf-8'))


def engine():
    config = lock()
    path = (ROOT / config['console_path']).resolve()
    path.relative_to(ROOT)
    with path.open('rb') as source:
        if hashlib.file_digest(source, 'sha256').hexdigest() != config['console_sha256']:
            raise ValueError('Pinned Godot console checksum mismatch')
    editor = (ROOT / config['editor_path']).resolve()
    editor.relative_to(ROOT)
    with editor.open('rb') as source:
        if hashlib.file_digest(source, 'sha256').hexdigest() != config['editor_sha256']:
            raise ValueError('Pinned Godot editor checksum mismatch')
    return str(path)


def test_environment(software=False):
    env = os.environ.copy()
    if software:
        config = json.loads((ROOT / 'config/test_environment.json').read_text(encoding='utf-8'))
        icd = Path(config['software_vulkan_icd'])
        if not icd.is_file():
            raise FileNotFoundError('Configured test-only software Vulkan ICD is absent')
        if hashlib.sha256(icd.read_bytes()).hexdigest() != config['icd_sha256']:
            raise ValueError('Software ICD configuration changed; repeat capability audit')
        env['VK_ICD_FILENAMES'] = str(icd)
        env['VK_DRIVER_FILES'] = str(icd)
        env['PATH'] = str(icd.parent) + os.pathsep + env['PATH']
    return env


def run(arguments, timeout=90, software=False):
    return subprocess.run([engine(), '--path', str(ROOT), *arguments], cwd=ROOT,
                          env=test_environment(software), capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=timeout)
