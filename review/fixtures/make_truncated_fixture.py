#!/usr/bin/env python3
"""Make a precisely truncated disposable ciphertext copy; never overwrite files."""
import hashlib
from pathlib import Path
import sys
if len(sys.argv) != 3:
    sys.exit('Usage: python3 make_truncated_fixture.py ORIGINAL.asc NEW-COPY.asc')
source, target = map(Path, sys.argv[1:])
data = source.read_bytes()
if not data.startswith(b'-----BEGIN PGP MESSAGE-----') or len(data) < 64:
    sys.exit('Expected a public-test armored PGP message (at least 64 bytes).')
copy = data[:len(data) // 2]
with target.open('xb') as out:
    out.write(copy)
for label, content in [('Original', data), ('Truncated copy', copy)]:
    print(f'{label}: {len(content)} bytes; SHA-256 {hashlib.sha256(content).hexdigest()}')
print('Saved the first half only. Original unchanged. Expected decryption result: failure.')
