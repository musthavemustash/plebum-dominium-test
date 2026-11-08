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
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('Supply the full reviewed source commit SHA')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    release = 'alpha-20261106-t3-t4'
    archive = 'plebum-tools-' + release + '.zip'
    files = {name: (ROOT / source).read_bytes() for name, source in SOURCES.items()}
    source_files = {name: {'source_path': source, 'sha256': sha(files[name]), 'size': len(files[name])}
                    for name, source in SOURCES.items()}
    files['SOURCE.json'] = (json.dumps({
        'release': release, 'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False,
        'source_repository': 'https://github.com/musthavemustash/plebum-dominium-test',
        'source_commit': source_commit, 'source_files': source_files,
        'outstanding': ['Actual browser and OS offline-isolation testing', 'Physical Tails testing',
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
   Do not bypass their safeguards if your browser reports the wrong state.
4. Record PASS, FAIL or NOT TESTED in RESULTS.csv. Submit non-sensitive results
   through the form after finishing the offline session: {FORM}

Python dice conversion needs Python 3. The Python map tool also needs GnuPG.
This package does not include Tails, a wallet application, or a full guide.
No installation or dependency download is performed by the package checker.

The packaged tools and public fixtures are byte-for-byte copies of the source
paths recorded in SOURCE.json. No cryptographic implementation was changed.
Browser/OS isolation, physical Tails operation and recovery remain unverified.
Older ZIPs and kit/VERIFY.md do not describe this alpha. Use this package's hashes.
Hashes detect changed bytes; they do not independently authenticate the publisher
or establish that a tool is safe. This alpha does not approve a stable release.
'''.encode()
    files['TESTING.txt'] = f'''PUBLIC TESTS ONLY — {release}

START IN THE TEST FOLDER
Complete offline or website-tools ZIP: extract it, open plebum-offline,
then open public-tests. Its fixtures are in public-tests/fixtures/.
Focused dice/map ZIP: extract it, then open plebum-public-test.
Its fixtures folder is directly inside plebum-public-test.
Use the matching HTML/Python tools in that test folder. Open your terminal
there: all commands and fixtures/... paths below are relative to it.
For the complete offline package's full T1 check, run verify_package.py
from plebum-offline first. The checker here verifies only this test subset.

Before each test, record release ID, OS/browser versions, date and file hashes.
Disconnect the test machine before opening HTML tools via file://. An offline
indicator is only a browser signal, not proof of network isolation. Use the OS
network controls too. Leave unsupported or unperformed checks as NOT TESTED.

T1 — Package integrity
Run python3 verify_package.py (Windows: py verify_package.py).
Expected: PASS for every listed file. Stop on a mismatch and download again.
The checker does not authenticate the download or run any custody tool.

T2 — Local/offline safeguards
On a connected machine, open the local HTML tools without entering any inputs.
Expected: sensitive operations blocked. On an offline machine, open local copies.
Expected: tools permit public-fixture tests only when the offline signal agrees.
If controls stay blocked, record the environment; do not bypass the safeguard.
If possible, reconnect after a public-fixture test. Expected: sensitive controls
block and stale sensitive output clears. Never perform this with real data.

T3 — Dice converter known-answer output
Paste fixtures/zeros-256.txt (256 zero bits) into the HTML binary-input box.
Expected: 24 words: 'abandon' repeated 23 times, followed by 'art'.
Repeat using python3 bip39_dice_converter.py; outputs must match.
Then use fixtures/ones-256.txt: 'zoo' repeated 23 times, followed by 'vote'.
Try 255 bits and a string containing x. Expected: rejection, no valid output.
The eight reference entropy/mnemonic pairs are in fixtures/bip39-vectors.json;
hex entropy must be converted to exactly 256 binary digits before input.
These are publicly known examples. Never fund a wallet derived from them.

T4 — Wallet-map encryption/decryption
For exact file-based Windows commands, read RETEST-WINDOWS.txt. Its fixture
uses password public-test-only; the fixture below uses password.txt instead.
Use fixtures/public-map.txt and the disposable password in fixtures/password.txt.
Encrypt, save the result, close/reopen, and decrypt. Expected: exact original
text, including Unicode and line breaks. Ciphertext bytes may differ per run.
Try a wrong password and a truncated COPY of the ciphertext. Expected: failure
without plaintext. Preserve your original fixture and encrypted test file.
Where GnuPG is available, cross-check HTML-encrypted text in the Python tool and
Python-encrypted text in the HTML tool. Report each direction separately.

T5 — Physical Tails (experienced volunteers)
Record Tails version and actual hardware. Boot with networking disabled, check
OS network state, open the extracted local HTML files and repeat T2–T4.
Record missing dependencies and browser restrictions. Close the tools and reboot;
record what remains on the removable drive and whether tools restart correctly.
Do not infer secure erasure or full recovery from a successful restart.

REPORTING
Use one response per task/failure. Include release, task ID, PASS/FAIL/NOT TESTED,
environment, steps, expected/actual result and whether it repeats. The existing
form accepts these details in its description; use general feedback if no tool
task is listed. Never submit private wallet data or credentials.
{FORM}
'''.encode()
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
    for name in ('README.txt', 'TESTING.txt'):
        (output / name).write_bytes(files[name])
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', help='new output directory')
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    result = build(args.output, args.source_commit)
    print(json.dumps(result['archive']))
