#!/usr/bin/env python3
"""Fetch pinned portable Godot assets locally with official API SHA256 verification."""
import argparse
import concurrent.futures
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = '4.7.2-stable'


def fetch(url, headers=None):
    request = urllib.request.Request(url, headers={'User-Agent': 'TheSeventhHouse-Toolchain', **(headers or {})})
    return urllib.request.urlopen(request, timeout=45)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--templates', action='store_true')
    parser.add_argument('--resume', action='store_true', help='Explicitly resume an inspected partial via bounded byte ranges')
    args = parser.parse_args()
    with fetch(f'https://api.github.com/repos/godotengine/godot-builds/releases/tags/{VERSION}') as response:
        release = json.load(response)
    name = f'Godot_v{VERSION}_export_templates.tpz' if args.templates else f'Godot_v{VERSION}_win64.exe.zip'
    asset = next(a for a in release['assets'] if a['name'] == name)
    expected = asset['digest']
    if not expected.startswith('sha256:'):
        raise ValueError('Official SHA256 digest missing; refusing unverified executable')
    directory = ROOT / '.tools/godot' / VERSION
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / name
    if not destination.exists():
        partial = destination.with_suffix(destination.suffix + '.partial')
        if partial.exists() and not args.resume:
            raise FileExistsError(f'Inspect prior interrupted download before retry: {partial}')
        if args.resume:
            start = partial.stat().st_size if partial.exists() else 0
            if start > asset['size']:
                raise ValueError('Partial exceeds official asset length')
            ranges = [(offset, min(offset + 32 * 1024 * 1024, asset['size']) - 1)
                      for offset in range(start, asset['size'], 32 * 1024 * 1024)]

            def get_range(bounds):
                first, last = bounds
                part = directory / f'{name}.{first}-{last}.part'
                if part.exists() and part.stat().st_size == last - first + 1:
                    return part
                with fetch(asset['browser_download_url'], {'Range': f'bytes={first}-{last}'}) as response:
                    if response.status != 206 or not response.headers.get('Content-Range', '').startswith(f'bytes {first}-{last}/'):
                        raise ValueError('Server did not honor exact byte range')
                    with part.open('wb') as output:
                        while data := response.read(1024 * 1024):
                            output.write(data)
                if part.stat().st_size != last - first + 1:
                    raise ValueError('Range length mismatch')
                print(f'Fetched bytes {first}-{last}', flush=True)
                return part

            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
                parts = list(pool.map(get_range, ranges))
            with partial.open('ab') as output:
                for part in parts:
                    with part.open('rb') as source:
                        while data := source.read(1024 * 1024):
                            output.write(data)
        else:
            with fetch(asset['browser_download_url']) as response, partial.open('xb') as output:
                while data := response.read(1024 * 1024):
                    output.write(data)
        digest = hashlib.sha256(partial.read_bytes()).hexdigest()
        if digest != expected.removeprefix('sha256:'):
            raise ValueError('Download SHA256 mismatch; partial retained for inspection')
        partial.rename(destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    if digest != expected.removeprefix('sha256:'):
        raise ValueError('Cached download SHA256 mismatch')
    with zipfile.ZipFile(destination) as archive:
        members = archive.infolist()
        for member in members:
            path = (directory / member.filename).resolve()
            path.relative_to(directory.resolve())
            if not path.exists():
                archive.extract(member, directory)
    record = dict(version=VERSION, url=asset['browser_download_url'], archive=name,
                  expected_sha256=expected, observed_sha256=digest, verified=True,
                  extracted_files=[m.filename for m in members])
    (directory / (name + '.verified.json')).write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
