#!/usr/bin/env python3
"""Generate current tool references; --check detects drift without rewriting."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from build_tool_fingerprints import TOOLS

DOCS = Path(__file__).resolve().parents[1] / 'docs'
FILES = {
    'dice-converter.html': ('dice-converter.html', 'Dice converter HTML.'),
    'descriptor-tool.html': ('descriptor-tool.html', 'Wallet-map tool HTML.'),
    'diceware-mapper.html': ('diceware-mapper.html', 'Six-word Diceware mapper.'),
    'fingerprint-checker.html': ('fingerprint-checker.html', 'Three-tool fingerprint checker.'),
    'bip39_dice_converter.py': ('kit/bip39_dice_converter.py', 'Python dice converter.'),
    'descriptor_obfuscator.py': ('kit/descriptor_obfuscator.py', 'Python wallet-map tool, using GnuPG.'),
    'eff_large_wordlist.txt': ('kit/eff_large_wordlist.txt', 'EFF Long Wordlist, 7,776 words.'),
    'hash_checker.html': ('kit/hash_checker.html', 'Manual SHA-256 checker.'),
}

def identity(data):
    return {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def expected():
    checker = (DOCS / 'fingerprint-checker.html').read_text()
    for key, filename in TOOLS.items():
        digest = identity((DOCS / filename).read_bytes())['sha256']
        assert f"'{key}': '{digest}'" in checker, f'Stale fingerprint checker: {filename}'
    rows = [dict(name=name, **identity((DOCS / path).read_bytes()), blurb=blurb)
            for name, (path, blurb) in FILES.items()]
    page = (DOCS / 'verify-file.html').read_text()
    page, count = re.subn(r'var PINNED = \[.*?\];', lambda _: 'var PINNED = ' + json.dumps(rows) + ';', page)
    assert count == 1, 'Missing verifier reference table'
    outputs = {'verify-file.html': page.encode()}
    manifest = ('# Current public-test tool fingerprints\n\n'
        'Generated from the exact files served by the test site. Public fixtures only; '
        'not approval for real-wallet use. A matching hash confirms byte equality, '
        'not independent publisher authentication or tool safety.\n\n'
        'For versioned ZIPs, use their own SHA256SUMS.txt and the separate '
        '[download verifier](https://musthavemustash.github.io/plebum-dominium-test/verify-download.html), '
        'saved separately before disconnecting. Old archives retain their original hashes.\n\n'
        'For individual files, use [Verify a file](../verify-file.html) or compare '
        '`sha256sum FILENAME` (Linux/Tails) or `Get-FileHash .\\FILENAME -Algorithm SHA256` '
        '(Windows) with the full hash below. Check the verifier itself before relying on it.\n\n')
    for row in rows + [dict(name='verify-file.html', **identity(outputs['verify-file.html']))]:
        manifest += f"## {row['name']}\n\n```text\nFile:     {row['name']}\nSize:     {row['size']} bytes\nSHA-256:  {row['sha256']}\n```\n\n"
    manifest += ('## Historical files\n\n'
        'The old tools-bundle.zip, PDFs, slides and recovery worksheet are withdrawn '
        'from current downloads pending reconciliation. They are not described by '
        'these current tool fingerprints and are not included in the refreshed packages.\n')
    outputs['kit/VERIFY.md'] = manifest.encode()
    return outputs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = expected()
    for name, data in outputs.items():
        path = DOCS / name
        if args.check:
            assert path.read_bytes() == data, f'Stale tool verification reference: {name}'
        else:
            path.write_bytes(data)
    print('PASS: current tool hashes, sizes, both verification pages and VERIFY.md agree')

if __name__ == '__main__':
    main()
