#!/usr/bin/env python3
"""Independently verify the published detached signature and immutable ZIPs."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FINGERPRINT = 'B9286C4A7CFF722E191D2D7566FB7D9AB51E417E'
RELEASES = {
    '20261113-r2': '7dd8eb16fc0c2dd4802ea6b1517c5642db51f217531be46567160deccc046cbb',
    '20261115-r1': 'a194d81afa3be6667a5e00c28d82ba189a1b7323565bbaf81682dd42f6b50f0f',
}
for version, EXPECTED_MANIFEST in RELEASES.items():
    RELEASE = ROOT / 'docs/releases' / version
    manifest = (RELEASE / 'manifest.txt').read_bytes()
    assert hashlib.sha256(manifest).hexdigest() == EXPECTED_MANIFEST
    rows = manifest.decode('ascii').splitlines()
    assert len(rows) == 3
    for line in rows:
        digest, name = line.split('  ')
        folder = 'alpha-' + version if name.startswith('plebum-tools-alpha-') else 'offline-' + version
        data = (ROOT / 'docs/testing' / folder / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest, name

    with tempfile.TemporaryDirectory() as temp:
        keyring = Path(temp) / 'public.gpg'
        args = ['gpg', '--no-options', '--homedir', temp, '--batch', '--no-autostart',
                '--no-auto-key-retrieve', '--auto-key-locate', 'clear']
        subprocess.run(args + ['--output', str(keyring), '--dearmor', str(RELEASE / 'plebum-public.asc')], check=True, capture_output=True)
        result = subprocess.run(args + ['--no-default-keyring', '--keyring', str(keyring), '--status-fd', '1',
                                '--verify', str(RELEASE / 'manifest.txt.asc'), str(RELEASE / 'manifest.txt')],
                                check=True, capture_output=True, text=True)
        valid = [line.split() for line in result.stdout.splitlines() if line.startswith('[GNUPG:] VALIDSIG ')]
        assert len(valid) == 1 and valid[0][2] == FINGERPRINT, result.stdout
        assert not any(flag in result.stdout for flag in ('EXPKEYSIG', 'REVKEYSIG', 'BADSIG', 'ERRSIG'))


vendor = ROOT / 'docs/assets/vendor/openpgp-6.3.2'
provenance = json.loads((vendor / 'PROVENANCE.json').read_text())
for name, digest in provenance['files'].items():
    assert hashlib.sha256((vendor / name).read_bytes()).hexdigest() == digest, name
print('PASS: GnuPG validates both pinned release signatures; all 6 ZIPs and vendored files match.')
