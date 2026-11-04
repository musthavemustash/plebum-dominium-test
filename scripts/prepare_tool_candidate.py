#!/usr/bin/env python3
"""Build an INTERNAL review candidate; never writes to docs or enables downloads."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'dice-converter.html': 'dice-converter.html',
    'descriptor-tool.html': 'descriptor-tool.html',
    **{name: 'kit/' + name for name in (
        'bip39_dice_converter.py', 'descriptor_obfuscator.py',
        'eff_large_wordlist.txt', 'hash_checker.html', 'verify_downloads.py',
        'verify_kit.sh')},
}
BLOCKERS = ['Actual browser and target offline environment tests incomplete']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def build(out):
    out = Path(out).resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Candidate must be outside repository; publication is blocked')
    out.mkdir(parents=True, exist_ok=False)
    files = {name: (ROOT / 'docs' / source).read_bytes() for name, source in SOURCES.items()}
    files['README.txt'] = ('INTERNAL REVIEW CANDIDATE — NOT APPROVED FOR CUSTODY USE\n'
        + '\n'.join(BLOCKERS) + '\nUse public test data only.\n').encode()
    for name, data in files.items():
        (out / name).write_bytes(data)
    # Fixed order, timestamp, permissions and compression: same input => same ZIP.
    with zipfile.ZipFile(out / 'tools-bundle.zip', 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    files['tools-bundle.zip'] = (out / 'tools-bundle.zip').read_bytes()
    rows = [{'name': name, 'size': len(data), 'sha256': digest(data),
             'blurb': 'Internal review candidate; release blocked.'}
            for name, data in sorted(files.items())]
    verifier = (ROOT / 'docs/verify-file.html').read_text()
    verifier, count = re.subn(r'var PINNED = \[.*?\];',
        'var PINNED = ' + json.dumps(rows) + ';', verifier, count=1)
    if count != 1:
        raise ValueError('Verifier pin declaration missing')
    verifier = verifier.replace('<body>', '<body><p role="alert">INTERNAL REVIEW CANDIDATE — RELEASE BLOCKED. Public test data only.</p>', 1)
    (out / 'verify-file.html').write_text(verifier)
    files['verify-file.html'] = verifier.encode()
    manifest = {name: {'size': len(data), 'sha256': digest(data)} for name, data in sorted(files.items())}
    (out / 'candidate-manifest.json').write_text(json.dumps(
        {'status': 'BLOCKED', 'blockers': BLOCKERS, 'files': manifest}, indent=2) + '\n')
    (out / 'VERIFY.md').write_text('# Internal candidate checksums — release blocked\n\n'
        + '\n'.join(f'{value["sha256"]}  {name}' for name, value in manifest.items()) + '\n')
    return manifest

def check(out):
    out = Path(out)
    manifest = json.loads((out / 'candidate-manifest.json').read_text())
    assert manifest['status'] == 'BLOCKED' and manifest['blockers'] == BLOCKERS
    for name, expected in manifest['files'].items():
        data = (out / name).read_bytes()
        assert len(data) == expected['size'] and digest(data) == expected['sha256'], name
    for name, source in SOURCES.items():
        assert (out / name).read_bytes() == (ROOT / 'docs' / source).read_bytes(), name
    with zipfile.ZipFile(out / 'tools-bundle.zip') as z:
        assert set(z.namelist()) == set(SOURCES) | {'README.txt'}
        for name in z.namelist():
            assert z.read(name) == (out / name).read_bytes(), name
    pins = json.loads(re.search(r'var PINNED = (\[.*?\]);', (out / 'verify-file.html').read_text()).group(1))
    assert {p['name'] for p in pins} == set(manifest['files']) - {'verify-file.html'}
    for pin in pins:
        assert {k: pin[k] for k in ('size', 'sha256')} == manifest['files'][pin['name']]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', help='new directory outside repository')
    args = parser.parse_args()
    build(args.output)
    check(args.output)
    print('PASS: candidate byte consistency; RELEASE BLOCKED:', '; '.join(BLOCKERS))
