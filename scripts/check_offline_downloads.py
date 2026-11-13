#!/usr/bin/env python3
"""Verify extracted packages, link closure, hashes and preserved safeguards."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile
from publish_offline_downloads import DOCS, OUT, FULL, TOOLS, EXACT, KIT_FILES
from reconcile_tool_downloads import TOOLS as REVIEWED_TOOLS, CURRENT, r4_files, tool_path, check_fingerprints, build as check_sources


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        key = 'src' if tag in ('script', 'img', 'iframe', 'source') else 'href'
        if tag in ('a', 'link', 'script', 'img', 'iframe', 'source') and attrs.get(key):
            if tag == 'link' and attrs.get('rel') in ('canonical', 'preconnect'):
                return
            self.refs.append((tag, attrs[key]))


def check():
    check_sources(check=True)
    r4_files(DOCS)  # Historical archive remains immutable.
    with zipfile.ZipFile(DOCS / CURRENT) as z:
        baseline = {n.split('/', 1)[1]: z.read(n) for n in z.namelist() if not n.endswith('/')}
    manifest = json.loads((OUT / 'manifest.json').read_text())
    for item in manifest['packages']:
        archive = OUT / item['name']
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == item['sha256']
        with tempfile.TemporaryDirectory() as temp:
            with zipfile.ZipFile(archive) as z:
                assert z.testzip() is None
                z.extractall(temp)
            root = Path(temp) / 'plebum-offline'
            assert not (root / 'verify-download.html').exists(), 'ZIP verifier must be saved separately'
            if (root / 'downloads.html').exists():
                offline_downloads = (root / 'downloads.html').read_text()
                assert 'pd-verify-catalog' not in offline_downloads, 'Circular archive hash reference'
                assert 'href="https://musthavemustash.github.io/plebum-dominium-test/verify-download.html"' in offline_downloads, 'Broken online verifier link'
            subprocess.run([sys.executable, str(root / 'verify_package.py')], check=True)
            for name in EXACT:
                assert (root / name).read_bytes() == (DOCS / name).read_bytes()
            assert {p.relative_to(root).as_posix() for p in (root / 'kit').rglob('*') if p.is_file()} == KIT_FILES
            for name, data in baseline.items():
                assert (root / 'public-tests' / name).read_bytes() == data, f'Current subset changed: {name}'
            subprocess.run([sys.executable, str(root / 'public-tests/verify_package.py')], check=True)
            for name in REVIEWED_TOOLS:
                assert (root / tool_path(name)).read_bytes() == baseline[name], f'Root/subset tools disagree: {name}'
            check_fingerprints(root)
            for page in root.rglob('*.html'):
                parser = References()
                parser.feed(page.read_text())
                for tag, ref in parser.refs:
                    url = urlsplit(ref)
                    if url.scheme == 'data':
                        continue  # Inline data URI, not a network resource.
                    if url.scheme or url.netloc:
                        assert tag not in ('script', 'img', 'iframe', 'source'), (page, 'network resource', ref)
                        continue
                    if not url.path:
                        continue
                    target = (page.parent / unquote(url.path)).resolve()
                    assert not url.path.startswith('/'), (page, ref)
                    assert target.is_relative_to(root) and target.exists(), (str(page.relative_to(root)), ref)
            if item['name'] == FULL:
                run_sheet = 'testing/session-guide/T6-RUN.txt'
                # The tested ZIP retains its original sheet. Live instruction
                # addenda are downloaded separately, without changing that ZIP.
                assert (root / 'T6-RUN.txt').read_bytes() == (root / run_sheet).read_bytes(), 'Packaged T6 sheets disagree'
                start = (root / 'START.html').read_text()
                assert 'href="test-the-site.html#t6"' in start and 'href="T6-RUN.txt"' in start
                assert 'href="paths/one/single-sig.html"' in start
                one_key = (root / 'paths/one/single-sig.html').read_text()
                assert 'For T6:' in one_key and 'Metal transfer is a later stage and is outside T6.' in one_key
                assert 'These tool files match the r4 files' not in one_key
                js = (root / 'assets/js/main.js').read_text()
                assert 'window.PD_OFFLINE_INDEXES[searchPath]' in js
                assert 'window.PD_OFFLINE_ROOT' in js
                assert 'Offline package: do not request live prices' in js
                subprocess.run(['node', '--check', str(root / 'assets/js/main.js')], check=True)
                subprocess.run(['node', '--check', str(root / 'assets/js/offline-indexes.js')], check=True)
                # Execute real embedded indexes and resolve every search result locally.
                probe = '''const fs=require('fs'),vm=require('vm');let root=process.argv[1];let ctx={window:{PD_OFFLINE_ROOT:'file://'+root+'/'},URL};vm.runInNewContext(fs.readFileSync(root+'/assets/js/offline-indexes.js','utf8'),ctx);for(let rows of Object.values(ctx.window.PD_OFFLINE_INDEXES)){for(let e of rows){if(!fs.existsSync(new URL(e.url)))throw Error(e.url);}}'''
                subprocess.run(['node', '-e', probe, str(root)], check=True)
            else:
                assert not (root / 'handouts').exists()
            print('PASS:', item['name'], 'integrity, local links, network subresources and preserved tools')


if __name__ == '__main__':
    check()
