#!/usr/bin/env python3
"""Check folder-grant boundaries and the new offline candidate; no physical Tails claim."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tails_opener', ROOT / 'docs/testing/session-guide/OPEN-IN-TAILS.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def helper_checks():
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary) / 'USB space # and $(literal)'
        folder.mkdir()
        for name in ('START.html', 'verify_package.py'):
            (folder / name).touch()
        exported = '/run/user/1000/doc/example/USB space # and $(literal)'
        with patch.object(helper.subprocess, 'run') as run:
            run.return_value.stdout = exported + '\n'
            url = helper.export_folder(folder)
            assert urlsplit(url).scheme == 'file' and not urlsplit(url).fragment
            assert unquote(urlsplit(url).path) == exported + '/START.html'
            command = run.call_args.args[0]
            assert command == ['flatpak', 'document-export', '--unique', '--transient',
                               '--app=org.boum.tails.TorBrowser', str(folder.resolve())]
            assert not run.call_args.kwargs.get('shell'), 'Folder path must never become shell code'
            assert run.call_args.kwargs['timeout'] == 30
            for bad in ('', 'relative/folder', '/one\n/two'):
                run.return_value.stdout = bad
                try:
                    helper.export_folder(folder)
                    raise AssertionError('Accepted a malformed portal response')
                except ValueError:
                    pass
        (folder / 'START.html').unlink()
        with patch.object(helper.subprocess, 'run') as run:
            try:
                helper.export_folder(folder)
                raise AssertionError('Exported an arbitrary parent folder')
            except ValueError:
                pass
            run.assert_not_called()
        for name in ('TESTING.txt', 'dice-converter.html'):
            (folder / name).touch()
        with patch.object(helper.subprocess, 'run') as run:
            run.return_value.stdout = exported
            assert helper.export_folder(folder).endswith('/dice-converter.html')
            run.side_effect = subprocess.CalledProcessError(1, 'flatpak', stderr='denied')
            try:
                helper.export_folder(folder)
                raise AssertionError('Hid a failed folder grant')
            except subprocess.CalledProcessError:
                pass
    print('PASS: scoped transient folder grant, encoded paths, focused layout and failure handling')


def candidate_checks():
    import prepare_offline_candidate as candidate
    import check_offline_downloads as checker
    import publish_offline_downloads as publisher
    metadata = json.loads((ROOT / 'docs/testing/offline-20261115-r1/manifest.json').read_text())
    assert metadata['signature_status'] == 'AWAITING_OFFLINE_SIGNATURE'
    candidate.configure(ROOT / 'docs', metadata['source_commit'])
    for name in ('OUT', 'FULL', 'TOOLS', 'CURRENT'):
        setattr(checker, name, getattr(publisher, name))
    checker.check()
    import zipfile
    for name in (publisher.FULL, publisher.TOOLS):
        with zipfile.ZipFile(publisher.OUT / name) as archive:
            for helper_name in ('OPEN-IN-TAILS.py', 'TAILS-OFFLINE.txt'):
                assert archive.read('plebum-offline/' + helper_name) == (ROOT / 'docs/testing/session-guide' / helper_name).read_bytes()
            start = archive.read('plebum-offline/START.html').decode()
            assert 'Unsigned candidate 20261115-r1' in start
            assert 'python3 OPEN-IN-TAILS.py' in start
            assert b'20261115-r1' in archive.read('plebum-offline/README.txt')
            assert json.loads(archive.read('plebum-offline/SOURCE.json'))['source_commit'] == metadata['source_commit']
    # The signed download selector must still cover exactly r2, not an unsigned candidate.
    from build_download_verifier import read_catalog
    catalog = read_catalog(ROOT / 'docs')
    assert len(catalog['packages']) == 3
    assert all('20261113-r2' in p['name'] for p in catalog['packages'])
    print('PASS: new helper packaged consistently; unsigned candidate cannot replace signed selector')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--helper-only', action='store_true')
    args = parser.parse_args()
    helper_checks()
    if not args.helper_only:
        candidate_checks()
