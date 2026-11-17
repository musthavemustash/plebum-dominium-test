#!/usr/bin/env python3
"""Build/check the separately versioned instruction-only rehearsal addendum."""
from pathlib import Path
import argparse, hashlib, io, zipfile
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/testing/rehearsal-20261117'
NAME = 'plebum-rehearsal-notes-20261117.zip'
SHEETS = ('T6-RUN.txt', 'T7-RUN.txt', 'WALLET-TRANSFER-CHECKS.txt',
          'PHOTO-REVIEW-FLOW.txt', 'TAILS-OFFLINE.txt', 'SESSION-NOTES.txt')
README = '''PLEBUM DOMINIUM: NOVEMBER 17 REHEARSAL NOTES
Instructions only. No wallet tools, private keys or test coins are included.
This is NOT a signed tool release. Its SHA256SUMS.txt checks these notes against
this site's reference; it does not authenticate the publisher independently.
Use the signed complete 20261115-r1 tool ZIP and its own verifier separately.

Extract these notes BESIDE your verified plebum-offline folder, not into it.
Do not replace files covered by the signed package's manifest. For T6/T7 use
the updated run sheets here, then the guide inside your unchanged extraction.
T6 passed in the supervised November 15-16 run; T7 remains untested. The
completion record does not certify a particular release ZIP or all T1-T5 checks.

Keep only non-sensitive evidence. Never share seeds, passphrases or private keys.
Save native screenshots on the data USB and keep signing sessions offline
through full shutdown. Metal and hardware signers are not required for testing.

Current status: https://musthavemustash.github.io/plebum-dominium-test/test-the-site.html
'''
def outputs():
    files = {name: (ROOT / 'docs/testing/session-guide' / name).read_bytes() for name in SHEETS}
    files['T6-RESULTS.md'] = (ROOT / 'docs/testing/t6-20261116/RESULTS.md').read_bytes()
    files['README.txt'] = README.encode()
    checks = ''.join(hashlib.sha256(data).hexdigest() + '  ' + name + '\n' for name,data in sorted(files.items()))
    files['FILES-SHA256.txt'] = checks.encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo('plebum-rehearsal-notes-20261117/'+name,(2026,11,17,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,data)
    archive=buf.getvalue()
    return {NAME:archive,'SHA256SUMS.txt':(hashlib.sha256(archive).hexdigest()+'  '+NAME+'\n').encode(),'README.txt':README.encode()}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    data=outputs()
    if args.check:
        for name,expected in data.items():
            assert (DEST/name).read_bytes()==expected, 'Stale rehearsal notes: '+name
        print('PASS: instruction-only ZIP and file/ZIP checksums match current notes')
    else:
        DEST.mkdir(parents=True,exist_ok=True)
        for name,content in data.items():(DEST/name).write_bytes(content)
        print('Built',NAME,'(instructions only; no release signature)')
if __name__=='__main__':main()
