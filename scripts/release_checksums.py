#!/usr/bin/env python3
"""Prepare/check a complete release inventory. This does NOT verify signatures."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'review/release-signing-20261113/files.json'
MANIFEST = PLAN.with_name('SHA256SUMS')


def safe_path(root, name):
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_./-]+', name):
        raise ValueError('Unsafe release filename')
    parts = PurePosixPath(name).parts
    if not parts or name.startswith('/') or any(p in ('.', '..') for p in name.split('/')):
        raise ValueError('Release paths must be normalized and relative')
    path = root / name
    if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
        raise ValueError('Symlink in release path: ' + name)
    if not path.is_file():
        raise ValueError('Missing release file: ' + name)
    return path


def inventory(root, plan):
    names = json.loads(plan.read_text(encoding='utf-8'))['files']
    if not names or len(names) != len(set(names)):
        raise ValueError('Empty or duplicate release inventory')
    return {name: hashlib.sha256(safe_path(root, name).read_bytes()).hexdigest()
            for name in sorted(names)}


def check(root, plan, manifest):
    expected = inventory(root, plan)
    actual = {}
    for line in manifest.read_text(encoding='ascii').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_./-]+)', line)
        if not match or match[2] in actual:
            raise ValueError('Malformed or duplicate checksum line')
        actual[match[2]] = match[1]
    if actual != expected:
        raise ValueError('Release inventory or file checksum mismatch')
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['create', 'check'])
    parser.add_argument('--root', type=Path, default=ROOT / 'docs')
    parser.add_argument('--plan', type=Path, default=PLAN)
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    args = parser.parse_args()
    try:
        if args.action == 'create':
            entries = inventory(args.root.resolve(), args.plan)
            # Refuse to replace a reviewed or signed manifest accidentally.
            with args.manifest.open('x', encoding='ascii', newline='\n') as out:
                out.writelines(f'{sha}  {name}\n' for name, sha in entries.items())
            print(f'Created UNSIGNED checksum list for {len(entries)} files: {args.manifest}')
        else:
            count = check(args.root.resolve(), args.plan, args.manifest)
            print(f'PASS: {count} release files match. Signature NOT checked.')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'FAIL: {exc}\n')


if __name__ == '__main__':
    main()
