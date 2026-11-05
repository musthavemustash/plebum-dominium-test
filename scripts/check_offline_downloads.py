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
from publish_offline_downloads import DOCS, OUT, FULL, TOOLS, SENSITIVE


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
    manifest = json.loads((OUT / 'manifest.json').read_text())
    for item in manifest['packages']:
        archive = OUT / item['name']
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == item['sha256']
        with tempfile.TemporaryDirectory() as temp:
            with zipfile.ZipFile(archive) as z:
                assert z.testzip() is None
                z.extractall(temp)
            root = Path(temp) / 'plebum-offline'
            subprocess.run([sys.executable, str(root / 'verify_package.py')], check=True)
            for name in SENSITIVE:
                assert (root / name).read_bytes() == (DOCS / name).read_bytes()
            for page in root.rglob('*.html'):
                parser = References()
                parser.feed(page.read_text())
                for tag, ref in parser.refs:
                    url = urlsplit(ref)
                    if url.scheme or url.netloc:
                        assert tag not in ('script', 'img', 'iframe', 'source'), (page, 'network resource', ref)
                        continue
                    if not url.path:
                        continue
                    target = (page.parent / unquote(url.path)).resolve()
                    assert not url.path.startswith('/'), (page, ref)
                    assert target.is_relative_to(root) and target.exists(), (str(page.relative_to(root)), ref)
            if item['name'] == FULL:
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
