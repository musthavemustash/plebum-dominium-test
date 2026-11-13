#!/usr/bin/env python3
"""Decode binary snapshots only. Reviewed text files are authoritative as text."""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY_SUFFIXES = {'.pdf', '.pptx', '.xlsx', '.zip', '.png'}


def decode(root=ROOT):
    written = []
    retirement = root / 'review/RETIRED_PRINT_ARTIFACTS_20261113.json'
    retired = set()
    if retirement.exists():
        retired = {item['path'].removeprefix('docs/')
                   for item in json.loads(retirement.read_text())['artifacts']}
    for directory in ('kit', 'assets/img'):
        for source in sorted((root / 'kit-b64' / directory).glob('*.b64')):
            relative = Path(directory) / source.name.removesuffix('.b64')
            if relative.as_posix() in retired:
                continue  # Stale snapshots cannot republish withdrawn guidance.
            if relative.suffix.lower() not in BINARY_SUFFIXES:
                continue
            data = base64.b64decode(b''.join(source.read_bytes().split()), validate=True)
            for target in (root / relative, root / 'docs' / relative):
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or target.read_bytes() != data:
                    target.write_bytes(data)
                    written.append(str(target.relative_to(root)))
    return written


if __name__ == '__main__':
    print('Decoded binary changes:', ', '.join(decode()) or 'none')
