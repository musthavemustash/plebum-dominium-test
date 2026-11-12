#!/usr/bin/env python3
"""Regressions for the post-merge rollback and misleading packaged fingerprints."""
import base64
import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import zipfile

from decode_kit_binaries import decode
from reconcile_tool_downloads import ROOT, R4, TOOLS, EXTRA, NAMING_REVIEW, tool_path, build, check_fingerprints
import publish_offline_downloads as publisher


def rejected(action, message):
    try:
        action()
    except AssertionError:
        return
    raise AssertionError(message)


with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    # Stale text snapshots must never replace independently reviewed copies.
    for name in ('descriptor_obfuscator.py', 'README.md', 'VERIFY.md', 'hash_checker.html'):
        snapshot = root / 'kit-b64/kit' / (name + '.b64')
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(base64.encodebytes(b'stale text'))
        for directory in ('kit', 'docs/kit'):
            path = root / directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'reviewed ' + directory.encode())
    binary = root / 'kit-b64/kit/example.zip.b64'
    binary.write_bytes(base64.encodebytes(b'PK\x03\x04binary fixture'))
    assert len(decode(root)) == 2
    for name in ('descriptor_obfuscator.py', 'README.md', 'VERIFY.md', 'hash_checker.html'):
        for directory in ('kit', 'docs/kit'):
            assert (root / directory / name).read_bytes() == b'reviewed ' + directory.encode()
    assert (root / 'docs/kit/example.zip').read_bytes() == b'PK\x03\x04binary fixture'
    assert decode(root) == [], 'A second decode must be a no-op'
print('PASS: stale text snapshots cannot roll back tools, manifests or instructions')

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    paths = {NAMING_REVIEW, 'docs/' + R4, 'docs/verify-file.html', 'docs/kit/VERIFY.md',
             'kit/VERIFY.md', 'kit-b64/kit/VERIFY.md.b64'}
    for name in TOOLS | EXTRA:
        path = tool_path(name)
        paths.add('docs/' + path)
        if path.startswith('kit/') and name in TOOLS:
            paths.add(path)
            if (ROOT / 'kit-b64' / (path + '.b64')).exists():
                paths.add('kit-b64/' + path + '.b64')
    for path in paths:
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, dest)
    with contextlib.redirect_stdout(io.StringIO()):
        build(root, check=True)
    # Use the actual obsolete implementation that caused the Windows regression.
    with zipfile.ZipFile(ROOT / 'docs/kit/tools-bundle.zip') as legacy:
        obsolete = legacy.read('descriptor_obfuscator.py')
    path = root / 'docs/kit/descriptor_obfuscator.py'
    good = path.read_bytes()
    path.write_bytes(obsolete)
    rejected(lambda: build(root, check=True), 'Old standalone wallet-map tool accepted')
    path.write_bytes(good)
    path = root / 'kit-b64/kit/descriptor_obfuscator.py.b64'
    good = path.read_bytes()
    path.write_bytes(base64.encodebytes(obsolete))
    rejected(lambda: build(root, check=True), 'Old tool snapshot accepted')
    path.write_bytes(good)
    # Reproduce the old offline transformation of an otherwise correct checker.
    checker = root / 'docs/fingerprint-checker.html'
    checker.write_bytes(checker.read_bytes().replace(b'<head>', b'<head><script>window.PD_OFFLINE_ROOT="./";</script>'))
    rejected(lambda: check_fingerprints(root / 'docs'), 'Changed packaged checker accepted')
print('PASS: obsolete standalone tools, stale snapshots and altered checker fingerprints rejected')

# Rebuild only into scratch; immutable published files are never overwritten.
original_out = publisher.OUT
try:
    with tempfile.TemporaryDirectory() as temp:
        publisher.OUT = Path(temp)
        for full, name in ((True, publisher.FULL), (False, publisher.TOOLS)):
            publisher.package(full)
            first = (publisher.OUT / name).read_bytes()
            publisher.package(full)
            assert (publisher.OUT / name).read_bytes() == first, 'Nondeterministic package: ' + name
finally:
    publisher.OUT = original_out
print('PASS: both package builds are deterministic without overwriting any published package')
