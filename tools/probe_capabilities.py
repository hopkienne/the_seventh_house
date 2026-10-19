#!/usr/bin/env python3
"""Record bounded local probes, preserving unknown capability separately from absent tools."""
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/tasks/T-010103'


def command_probe(name, executable, args):
    command = [executable, *args]
    record = dict(name=name, path=shutil.which(executable), command=command,
                  probe_timestamp=dt.datetime.now(dt.timezone.utc).isoformat())
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=20, cwd=ROOT)
        record.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
                      available=result.returncode == 0, timed_out=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        record.update(exit_code=None, stdout='', stderr=str(error), available=False,
                      timed_out=isinstance(error, subprocess.TimeoutExpired))
    record['version'] = record['stdout'].strip() if record['available'] else None
    return record


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    probes = [command_probe(name, exe, ['--version']) for name, exe in
              [('python', sys.executable), ('git', 'git'), ('godot', 'godot'),
               ('godot4', 'godot4'), ('blender', 'blender')]]
    probes.append(command_probe('git_lfs', 'git', ['lfs', 'version']))
    gpu = command_probe('gpu_inventory', 'powershell', ['-NoProfile', '-Command',
                        'Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion | ConvertTo-Json'])
    probes.append(gpu)
    url = 'https://api.github.com/repos/godotengine/godot-builds/releases/tags/4.7.2-stable'
    network = dict(url=url, available=None, status=None, error=None)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TheSeventhHouse-CapabilityAudit'})
        with urllib.request.urlopen(req, timeout=25) as response:
            release_bytes = response.read()
            network.update(available=True, status=response.status)
        (REPORT / 'godot_release.json').write_bytes(release_bytes)
        release = json.loads(release_bytes)
        network['tag'] = release.get('tag_name')
        network['assets'] = [{k: a.get(k) for k in ('name', 'size', 'browser_download_url', 'digest')}
                             for a in release.get('assets', [])
                             if any(x in a.get('name', '') for x in ('win64', 'export_templates', 'SHA512'))]
    except (OSError, ValueError) as error:
        network.update(available=False, error=str(error))
    raw = dict(probes=probes, network=network, host=platform.platform())
    (REPORT / 'probes.json').write_text(json.dumps(raw, indent=2)+'\n', encoding='utf-8')
    found = {p['name']: p['available'] for p in probes}
    capabilities = dict(
        schema_version=1, probe_timestamp=dt.datetime.now(dt.timezone.utc).isoformat(),
        tools=probes, native_os=platform.system(), host=platform.platform(),
        capabilities=dict(filesystem=True, python_cli=found['python'], git_cli=found['git'],
                          godot_cli=found['godot'] or found['godot4'], blender_cli=found['blender'],
                          native_windows=platform.system() == 'Windows', rendered_runtime=None,
                          gpu=None, gui_automation=None, physical_gamepad=None,
                          audio_playback_review=None, audio_capture=None,
                          network_official_github_api=network['available'],
                          image_generation_tool_declared=True, image_generation_probed=False,
                          subagent_tools_declared=True, subagent_execution_probed=False),
        limitations=[
            'Godot/Blender not found on PATH; bounded install-directory inspection also found none.',
            'GPU inventory alone does not prove Godot Forward+ render capability; runtime probe still required.',
            'Windows host identification is not a native game smoke test.',
            'GUI, physical gamepad, audible mix and image/subagent tools have not been exercised.',
            'No paid API or public upload authorized. Sequential single-agent execution uses self_review=true.'
        ],
        fallbacks=dict(godot='Download pinned free official portable binary and matching templates locally; verify hashes and --version before use.',
                       blender='Godot procedural mesh pipeline once Godot is verified; audit any Blender installation before use.',
                       render='Headless tests can cover logic only; rendered QA still required.',
                       gamepad='Synthetic focus/action tests only until a physical device is accessible.'),
        network_probe=network, raw_log='reports/tasks/T-010103/probes.json')
    (ROOT / 'config/agent_capabilities.json').write_text(json.dumps(capabilities, indent=2)+'\n', encoding='utf-8')
    permissions = dict(schema_version=1, local_repository_work=True, destructive_work=False,
                       paid_spend_limit=0, external_write=False, public_release=False,
                       publish_allowed=False, authorization_records=[],
                       basis='Current user request authorizes local production/testing; AGENTS.md and 12_RELEASE_AND_PERMISSIONS.md restrict paid/legal/public actions.')
    (ROOT / 'config/permissions.json').write_text(json.dumps(permissions, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(raw, indent=2))


if __name__ == '__main__':
    main()
