#!/usr/bin/env python3
"""Assemble a deterministic public alpha without changing reviewed tool bytes."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    **{name: 'docs/testing/session-guide/' + name for name in (
        'TESTING.txt', 'EVIDENCE-CHECKLIST.txt', 'SESSION-NOTES.txt', 'FORM-REPORTING.txt')},
    'fingerprint-checker.html': 'docs/fingerprint-checker.html',
    'diceware-mapper.html': 'docs/diceware-mapper.html',
    'TOOL-FINISH-RETEST.txt': 'docs/testing/t5-20261108/TOOL-FINISH-RETEST.txt',
    'PUBLIC-SESSION-CONTRACT.txt': 'docs/testing/t5-20261108/PUBLIC-SESSION-CONTRACT.txt',
    'make_truncated_fixture.py': 'review/fixtures/make_truncated_fixture.py',
    'compare_files.py': 'review/fixtures/compare_files.py',
    'T5-dice-reference-inputs.txt': 'review/fixtures/T5-dice-reference-inputs.txt',
    'TAILS-RETEST-RESULTS.txt': 'docs/testing/t5-20261108/TAILS-RETEST-RESULTS.txt',
    'RETEST-WINDOWS.txt': 'docs/testing/t4-20261106/RETEST-WINDOWS.txt',
    'VALIDATION.txt': 'docs/testing/t4-20261106/VALIDATION.txt',
    'dice-converter.html': 'docs/dice-converter.html',
    'descriptor-tool.html': 'docs/descriptor-tool.html',
    'bip39_dice_converter.py': 'docs/kit/bip39_dice_converter.py',
    'descriptor_obfuscator.py': 'docs/kit/descriptor_obfuscator.py',
    'eff_large_wordlist.txt': 'docs/kit/eff_large_wordlist.txt',
    **{'fixtures/' + name: 'review/fixtures/' + name for name in (
        'README.md', 'bip39-vectors.json', 'bip39-english.txt', 'python-mnemonic-LICENSE')},
}
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def build(output, source_commit):
    from build_tool_fingerprints import build as update_fingerprints
    update_fingerprints()
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('Supply the full reviewed source commit SHA')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    release = json.loads((ROOT / 'scripts/download_release.json').read_text())['focused']
    archive = 'plebum-tools-' + release + '.zip'
    files = {name: (ROOT / source).read_bytes() for name, source in SOURCES.items()}
    source_files = {name: {'source_path': source, 'sha256': sha(files[name]), 'size': len(files[name])}
                    for name, source in SOURCES.items()}
    files['SOURCE.json'] = (json.dumps({
        'release': release, 'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False,
        'source_repository': 'https://github.com/musthavemustash/plebum-dominium-test',
        'source_commit': source_commit, 'source_files': source_files,
        'outstanding': ['Target-environment evidence for the documented OS-managed public-test procedure', 'T1 checks for this refreshed ZIP; prior Windows/Tails evidence retains its r4 identity',
                        'Recovery-workflow validation', 'Stable release reconciliation'],
    }, indent=2) + '\n').encode()
    files['README.txt'] = f'''PLEBUM DOMINIUM — PUBLIC ALPHA TEST RELEASE
Release: {release}
Source: {source_commit}

AVAILABLE FOR TESTING. NOT APPROVED FOR REAL-WALLET USE.
Use the included public fixtures and disposable test data only. Never use real
seed phrases, private keys, entropy, passwords, wallet backups or funds.
This restriction also applies to any older custody instructions inside the tools.

1. Extract the entire ZIP. Open the extracted plebum-public-test folder.
   Tools, TESTING.txt and the fixtures folder are directly inside it.
   If using the complete offline or website-tools ZIP, open plebum-offline,
   then public-tests instead. Its fixtures are in public-tests/fixtures/.
   Do not launch tools inside the compressed archive.
2. Open a terminal in that test folder and read TESTING.txt. All commands
   and paths such as fixtures/public-map.txt start from that folder.
   Check this test subset with: python3 verify_package.py
   On Windows with Python installed, use: py verify_package.py
3. Open the HTML tools as local files on a disconnected test machine.
   HTTP/HTTPS and localhost are deliberately blocked by the sensitive tools.
   Complete the OS checks before the public-test acknowledgments. A stable
   browser flag of true may occur in isolated Tails. It is not proof either way.
   Keep networking disabled; Lock and clear before changing network settings.
4. Create a results folder. Copy RESULTS.csv and SESSION-NOTES.txt there before
   editing them; keep packaged originals intact. Save screenshots after each
   result, before clearing. Follow EVIDENCE-CHECKLIST.txt to copy and reopen
   evidence on the separate data USB before reboot, shutdown or a pause.
5. After the offline session is closed, read FORM-REPORTING.txt. It maps T1-T5
   to the live Google Form and explains uploading a public-only evidence folder
   and sharing a working viewer link. Submit your actual results: {FORM}

Python dice conversion needs Python 3. The Python map tool also needs GnuPG.
This package does not include Tails, a wallet application, or a full guide.
No installation or dependency download is performed by the package checker.

The packaged tools and public fixtures are byte-for-byte copies of the source
paths recorded in SOURCE.json. No cryptographic implementation was changed.
Earlier candidate Tails results are in TAILS-RETEST-RESULTS.txt.
This November 11 refresh reconciles instructions and verification references.
All seven tested HTML/Python/wordlist files match r4. Windows November 8 and
Tails November 9 short-run results remain associated with their original r4
packages. Check this new ZIP with T1; no new physical test result is claimed.
Browser isolation is not certified by this package. See PUBLIC-SESSION-CONTRACT.txt
for the public-test boundary and TOOL-FINISH-RETEST.txt for the remaining checks.
Complete wallet recovery remains unresolved.
Older ZIPs retain their original hashes. Use this package's SHA256SUMS.txt.
Hashes detect changed bytes; they do not independently authenticate the publisher
or establish that a tool is safe. This alpha does not approve a stable release.
'''.encode()
    files['fixtures/short-255.txt'] = ('0' * 255 + '\n').encode()
    files['fixtures/invalid-character.txt'] = ('0' * 255 + 'x\n').encode()
    files['fixtures/zeros-256.txt'] = ('0' * 256 + '\n').encode()
    files['fixtures/ones-256.txt'] = ('1' * 256 + '\n').encode()
    files['fixtures/public-map.txt'] = (ROOT / 'review/fixtures/t4-public-map.txt').read_bytes()
    files['fixtures/password.txt'] = b'public-test-only\n'
    results = io.StringIO(newline='')
    writer = csv.writer(results)
    writer.writerow(['release', 'task', 'result', 'date', 'OS', 'browser', 'Tails_version',
                     'steps', 'expected', 'actual', 'reproducible'])
    for task in ('T1', 'T2', 'T3', 'T4', 'T5'):
        writer.writerow([release, task, 'NOT TESTED'] + [''] * 8)
    files['RESULTS.csv'] = results.getvalue().encode()
    files['verify_package.py'] = b'''#!/usr/bin/env python3
"""Check package bytes only; does not authenticate or run the tools."""
from pathlib import Path
import hashlib
import sys
root = Path(__file__).resolve().parent
failures = []
rows = (root / 'SHA256SUMS.txt').read_text().splitlines()
for row in rows:
    expected, name = row.split('  ', 1)
    target = (root / name).resolve()
    if root not in target.parents or not target.is_file():
        failures.append(name)
    elif hashlib.sha256(target.read_bytes()).hexdigest() != expected:
        failures.append(name)
if failures:
    print('FAIL: ' + ', '.join(failures))
    sys.exit(1)
print(f'PASS: {len(rows)} files match package checksums. Public tests only; not custody approval.')
'''
    files['VERIFY.md'] = (f'# Public alpha checksums — {release}\n\n'
        'Use SHA256SUMS.txt in this folder, or run `python3 verify_package.py`.\n'
        'Checksums establish byte equality only; public test inputs only.\n').encode()
    files['SHA256SUMS.txt'] = ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(files.items())).encode()
    with zipfile.ZipFile(output / archive, 'w') as bundle:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('plebum-public-test/' + name, (2026, 11, 5, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
    manifest = {'release': release, 'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False,
                'source_commit': source_commit,
                'archive': {'name': archive, 'sha256': sha((output / archive).read_bytes()),
                            'size': (output / archive).stat().st_size},
                'files': {name: {'sha256': sha(data), 'size': len(data)} for name, data in sorted(files.items())}}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (output / 'SHA256SUMS.txt').write_text(''.join(
        f'{sha((output / name).read_bytes())}  {name}\n' for name in (archive, 'manifest.json')))
    for name in ('README.txt', 'TESTING.txt', 'EVIDENCE-CHECKLIST.txt', 'SESSION-NOTES.txt', 'FORM-REPORTING.txt'):
        (output / name).write_bytes(files[name])
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', help='new output directory')
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    result = build(args.output, args.source_commit)
    print(json.dumps(result['archive']))
