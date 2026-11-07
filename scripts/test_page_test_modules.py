#!/usr/bin/env python3
"""Check report routing, truthful prefills and local-path privacy in page panels."""
from html import unescape
import json
import re
from urllib.parse import parse_qs, urlsplit
from zipfile import ZipFile

from page_test_modules import BASE, DOCS, ORIGIN, STAMP, catalog, with_page_test
from render_paths import PATHS


def check_page(path, public_path, tasks, build, source=None):
    if source is None:
        source = path.read_text()
    blocks = re.findall(r'<!-- page-test-module -->(.*?)<!-- /page-test-module -->', source, re.S)
    assert len(blocks) == 1, (path, len(blocks))
    block = blocks[0]
    assert source.count('id="help-test-page"') == 1, path
    ids = re.findall(r'<code>(P-[A-Z0-9-]+-\d\d)</code>', block)
    assert ids == tasks, (path, ids, tasks)
    link = unescape(re.search(r'<a class="ptm-report" href="([^"]+)"', block)[1])
    url = urlsplit(link)
    assert (url.scheme, url.netloc) == ('https', 'docs.google.com'), path
    fields = parse_qs(url.query)
    assert fields['entry.460741145'] == ['General website feedback'], path
    assert fields['entry.1164893128'] == [ORIGIN + public_path], (path, fields)
    assert fields['entry.846110096'] == ['Website build ' + build], path
    assert all(t in fields['entry.760527846'][0] for t in tasks), path
    # No PASS/FAIL, severity, repetition or feedback-type selections are made for a tester.
    for key in ['entry.414350644', 'entry.490247074', 'entry.1497918313', 'entry.1715999097']:
        assert key not in fields, (path, key)
    assert not any('file://' in value or '/Users/' in value or 'C:\\' in value
                   for values in fields.values() for value in values), path
    assert '/plebum-dominium-test/' not in link, 'Public paths must stay encoded for offline packaging'


def main():
    data = catalog()
    build = json.loads((DOCS / STAMP).read_text())['source_commit']
    pages = sorted((DOCS / 'handouts').glob('*.html')) + [DOCS / 'choose-path.html']
    expected = {}
    for page in pages:
        expected[page.relative_to(DOCS).as_posix()] = [t['id'] for t in data[page.stem]['tasks']]
        check_page(page, BASE + page.relative_to(DOCS).as_posix(),
                   [t['id'] for t in data[page.stem]['tasks']], build)
        # Running the canonical renderer again must not create duplicates or whitespace drift.
        assert with_page_test(page.read_text(), page.stem, BASE + page.relative_to(DOCS).as_posix()) == page.read_text(), page
    count = 0
    for route, info in PATHS.items():
        for slug, _, source in info['steps']:
            name = 'paths/' + route + '/' + slug + '.html'
            expected[name] = [t['id'] for t in data[source.split('/')[-1]]['tasks']]
            check_page(DOCS / name, BASE + name,
                       [t['id'] for t in data[source.split('/')[-1]]['tasks']], build)
            count += 1
        name = 'paths/' + route + '/index.html'
        expected[name] = [t['id'] for t in data['path-overview']['tasks']]
        check_page(DOCS / name, BASE + name,
                   [t['id'] for t in data['path-overview']['tasks']], build)
    # Both routes must retain their own form URL; their encoded links cannot be
    # fixed by the route renderer's usual plain-string URL rewrites.
    one = (DOCS / 'paths/one/verify.html').read_text()
    three = (DOCS / 'paths/three/verify.html').read_text()
    assert 'paths%2Fone%2Fverify.html' in one
    assert 'paths%2Fthree%2Fverify.html' in three
    # Check the published offline artifact, after its base-path rewriting, too.
    archive = DOCS / 'testing/offline-20261106/plebum-complete-offline-tester-20261106.zip'
    with ZipFile(archive) as zipped:
        assert 'plebum-offline/assets/css/page-test-modules.css' in zipped.namelist()
        for name, tasks in expected.items():
            check_page(name, BASE + name, tasks, build,
                       zipped.read('plebum-offline/' + name).decode())
    print(f'PASS: {len(pages)} canonical panels, {count} route panels + 2 overviews, {len(expected)} offline panels; correct public URLs/build/task IDs; outcomes unselected; no local paths; idempotent rendering')


if __name__ == '__main__':
    main()
