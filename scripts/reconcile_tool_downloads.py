#!/usr/bin/env python3
"""Build/check current tool fingerprints without rewriting tested tools."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
R4 = 'testing/alpha-20261108-t5-r4/plebum-tools-alpha-20261108-t5-r4.zip'
R4_SHA256 = '6d5ab946970537b21249555507be65724061fd01d132cc02a1c8cb4b4938aec8'
CURRENT = 'testing/alpha-20261113-r2/plebum-tools-alpha-20261113-r2.zip'
NAMING_REVIEW = 'review/TOOL_REPAIR_20261113_R1.json'
TOOLS = {
    'dice-converter.html': 'Dice converter page.',
    'descriptor-tool.html': 'Wallet-map tool. Encrypt and restore a wallet map.',
    'diceware-mapper.html': 'Diceware mapper. Six-word passphrase from five-dice rolls.',
    'fingerprint-checker.html': 'Fingerprint checker. Compare file fingerprints.',
    'bip39_dice_converter.py': 'Python dice converter.',
    'descriptor_obfuscator.py': 'Python wallet-map tool. Requires GnuPG.',
    'eff_large_wordlist.txt': 'EFF Large Wordlist. 7,776 words.',
}
EXTRA = {'hash_checker.html': 'Manual SHA-256 checker.'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tool_path(name):
    return name if name in TOOLS and name.endswith('.html') else 'kit/' + name


def r4_files(docs):
    archive = docs / R4
    assert digest(archive.read_bytes()) == R4_SHA256, 'Historical R4 ZIP changed'
    with zipfile.ZipFile(archive) as z:
        return {n.split('/', 1)[1]: z.read(n) for n in z.namelist() if not n.endswith('/')}


def check_tools(root):
    docs = root / 'docs'
    baseline = r4_files(docs)
    review = json.loads((root / NAMING_REVIEW).read_text())
    reviewed = review['sha256']
    for name in TOOLS:
        path = tool_path(name)
        data = (docs / path).read_bytes()
        if name in reviewed:
            assert digest(data) == reviewed[name], f'Unreviewed tool bytes: docs/{path}'
            # Unchanged tools retain the R4 executable baseline. An explicit
            # separate script pin permits the reviewed dice UI repair only;
            # updating a whole-file fingerprint alone cannot authorize code.
            def scripts(value):
                text = value.decode()
                if name == 'fingerprint-checker.html':
                    text = re.sub(r"('(converter|descriptor|mapper)': ')[a-f0-9]{64}", r'\1HASH', text)
                return re.findall(r'<script\b[^>]*>(.*?)</script>', text, re.S)
            if name in review.get('script_sha256', {}):
                assert scripts(data)[0] == scripts(baseline[name])[0], f'Crypto implementation changed: {name}'
                code = json.dumps(scripts(data), ensure_ascii=False).encode()
                assert digest(code) == review['script_sha256'][name], f'Unreviewed tool logic: {name}'
            else:
                assert scripts(data) == scripts(baseline[name]), f'Tool logic changed: {name}'
        else:
            assert data == baseline[name], f'R4 tool changed: docs/{path}'
        if path.startswith('kit/'):
            assert (root / path).read_bytes() == baseline[name], f'R4 tool changed: {path}'
            snapshot = root / 'kit-b64' / (path + '.b64')
            if snapshot.exists():
                assert base64.b64decode(snapshot.read_bytes()) == baseline[name], f'Stale snapshot: {snapshot}'


def expected_outputs(root):
    docs = root / 'docs'
    entries = []
    for name, blurb in (TOOLS | EXTRA).items():
        data = (docs / tool_path(name)).read_bytes()
        entries.append(dict(name=name, size=len(data), sha256=digest(data), blurb=blurb))
    page = (docs / 'verify-file.html').read_text()
    page, count = re.subn(r'var PINNED = \[.*?\];', lambda _: 'var PINNED = ' + json.dumps(entries) + ';', page, flags=re.S)
    assert count == 1, 'Expected one file-verifier catalog'
    manifest = '''# Current public-test tool fingerprints

Public test data only. These fingerprints identify files; they do not approve
real-wallet use or independently authenticate the publisher.

Use verify-file.html to check an individual file. Use verify-download.html,
saved separately before disconnecting, to check a complete or tools-only ZIP.
After extraction, run verify_package.py from the plebum-offline folder.
For the current test subset, use public-tests/TESTING.txt and its verifier.

The HTML tools and verify-file.html are at the site or package root. Python
tools, the wordlist, this file and hash_checker.html are in kit/.
These tool copies have the same bytes online and in the current offline ZIPs.

## File identities

'''
    own = dict(name='verify-file.html', size=len(page.encode()), sha256=digest(page.encode()))
    for item in entries + [own]:
        manifest += f"```\nFile:     {item['name']}\nSize:     {item['size']} bytes\nSHA-256:  {item['sha256']}\n```\n\n"
    manifest += '''## Check on your computer

Linux / macOS / Tails, from the file's folder:

```bash
sha256sum descriptor_obfuscator.py
```

Windows PowerShell, from the file's folder:

```powershell
Get-FileHash .\\descriptor_obfuscator.py -Algorithm SHA256
```

Compare every character. Stop if the file differs. The Python wallet-map
tool also requires GnuPG, installed separately before disconnecting.

## Historical files

tools-bundle.zip, older PDFs, slides and the recovery worksheet are legacy
assets. They are excluded from the current offline ZIPs and this manifest.
Use the current HTML guide; PDF reconciliation and print review remain open.
Historical versioned ZIPs retain their own checksums and test results.
'''
    encoded = manifest.encode()
    return {
        'docs/verify-file.html': page.encode(),
        'docs/kit/VERIFY.md': encoded,
        'kit/VERIFY.md': encoded,
        'kit-b64/kit/VERIFY.md.b64': base64.encodebytes(encoded),
    }


def check_fingerprints(directory):
    """Check references against the files they actually describe, including ZIP copies."""
    manifest = (directory / 'kit/VERIFY.md').read_text()
    entries = re.findall(r'File:\s+(\S+)\nSize:\s+(\d+) bytes\nSHA-256:\s+([a-f0-9]{64})', manifest)
    assert {name for name, _, _ in entries} == set(TOOLS) | set(EXTRA) | {'verify-file.html'}
    for name, size, sha in entries:
        path = 'verify-file.html' if name == 'verify-file.html' else tool_path(name)
        data = (directory / path).read_bytes()
        assert len(data) == int(size) and digest(data) == sha, f'Fingerprint mismatch: {path}'
    page = (directory / 'verify-file.html').read_text()
    pinned = json.loads(re.search(r'var PINNED = (\[.*?\]);', page, re.S)[1])
    assert {item['name'] for item in pinned} == set(TOOLS) | set(EXTRA)
    for item in pinned:
        data = (directory / tool_path(item['name'])).read_bytes()
        assert len(data) == item['size'] and digest(data) == item['sha256'], item['name']


def build(root=ROOT, check=False):
    check_tools(root)
    for path, data in expected_outputs(root).items():
        target = root / path
        if check:
            assert target.read_bytes() == data, f'Stale generated fingerprints: {path}'
        else:
            target.write_bytes(data)
    check_fingerprints(root / 'docs')
    print('PASS: reviewed tool bytes/script pins, preserved crypto baseline, snapshots and file fingerprints')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(check=parser.parse_args().check)
