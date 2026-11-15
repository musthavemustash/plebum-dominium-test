#!/usr/bin/env python3
"""Prepare an immutable unsigned rebuild without promoting signed downloads."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import prepare_public_test_release as focused
import publish_offline_downloads as publisher

ROOT = Path(__file__).resolve().parents[1]
RELEASE = '20261115-r1'


def configure(output_root, source_commit):
    publisher.RELEASE = RELEASE
    publisher.SOURCE_COMMIT = source_commit
    publisher.DEST = 'testing/offline-' + RELEASE
    publisher.OUT = output_root / publisher.DEST
    publisher.FULL = 'plebum-complete-offline-tester-' + RELEASE + '.zip'
    publisher.TOOLS = 'plebum-website-tools-only-' + RELEASE + '.zip'
    publisher.CURRENT = f'testing/alpha-{RELEASE}/plebum-tools-alpha-{RELEASE}.zip'
    publisher.FOCUSED_ARCHIVE = output_root / publisher.CURRENT


def build(output_root, source_commit):
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if source_commit != actual:
        raise ValueError('Use the current full source commit SHA.')
    subprocess.run(['git', 'diff', '--exit-code', source_commit, '--', 'docs', 'scripts', 'review/fixtures'],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    configure(output_root, source_commit)
    if publisher.OUT.exists() or publisher.FOCUSED_ARCHIVE.parent.exists():
        raise ValueError('Candidate output already exists. Never overwrite it; choose a new version.')
    alpha = focused.build(publisher.FOCUSED_ARCHIVE.parent, source_commit, 'alpha-' + RELEASE)
    publisher.OUT.mkdir(parents=True)
    packages = [publisher.package(True), publisher.package(False)]
    manifest = {'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False,
                'signature_status': 'AWAITING_OFFLINE_SIGNATURE',
                'release': 'offline-' + RELEASE, 'source_commit': source_commit,
                'packages': packages}
    path = publisher.OUT / 'manifest.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    (publisher.OUT / 'SHA256SUMS.txt').write_text(
        ''.join(f'{p["sha256"]}  {p["name"]}\n' for p in packages) +
        f'{hashlib.sha256(path.read_bytes()).hexdigest()}  manifest.json\n')
    import zipfile
    with zipfile.ZipFile(publisher.OUT / publisher.FULL) as archive:
        (publisher.OUT / 'README.txt').write_bytes(archive.read('plebum-offline/README.txt'))
    signing = output_root / 'signing' / RELEASE
    signing.mkdir(parents=True)
    # Exact LF/ASCII bytes, basename-only format compatible with Sparrow/GnuPG.
    rows = [alpha['archive'], *packages]
    (signing / 'manifest.txt').write_text(
        ''.join(f'{p["sha256"]}  {p["name"]}\n' for p in rows), encoding='ascii', newline='\n')
    print(json.dumps({'source_commit': source_commit, 'archives':
        [{k: p[k] for k in ('name', 'sha256', 'size')} for p in rows],
        'unsigned_manifest': str(signing / 'manifest.txt')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--output-root', type=Path, required=True,
                        help='New output tree; archives are under testing/; manifest under signing/')
    args = parser.parse_args()
    build(args.output_root.resolve(), args.source_commit)
