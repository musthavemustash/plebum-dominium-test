"""Reject incomplete/tampered inventories, missing files and unsafe paths."""
import json
from pathlib import Path
import tempfile
from release_checksums import check, inventory

with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    (root / 'tool.py').write_bytes(b'public fixture\r\n')
    plan = root / 'files.json'
    plan.write_text(json.dumps({'files': ['tool.py']}))
    entries = inventory(root, plan)
    good = ''.join(f'{sha}  {name}\n' for name, sha in entries.items())
    manifest = root / 'SHA256SUMS'
    manifest.write_text(good)
    assert check(root, plan, manifest) == 1
    def rejects():
        try:
            check(root, plan, manifest)
        except ValueError:
            return
        raise AssertionError('Invalid release accepted')
    for bad in ['', good + good, good.replace('tool.py', 'extra.py'), 'not a manifest\n']:
        manifest.write_text(bad)
        rejects()
    manifest.write_text(good)
    (root / 'tool.py').write_bytes(b'tampered\n')
    rejects()
    (root / 'tool.py').unlink()
    rejects()
    (root / 'tool.py').symlink_to(plan)
    rejects()
    for names in [['../escape.py'], ['/tmp/file'], ['a/../tool.py'], ['tool.py', 'tool.py'], []]:
        plan.write_text(json.dumps({'files': names}))
        rejects()
print('PASS: release checks reject tampering, omission, duplicates, missing files, symlinks and traversal')
