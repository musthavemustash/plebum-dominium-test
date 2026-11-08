#!/usr/bin/env python3
"""Build the local ZIP verifier from the final, published package checksums.

Run after packaging. The generated page and inline catalog must never be put
back inside the archives they describe, which would create a circular hash.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = '/plebum-dominium-test/'
ORIGIN = 'https://musthavemustash.github.io'
MAX_BYTES = 32 * 1024 * 1024
START = '<!-- download-verifier -->'
END = '<!-- /download-verifier -->'
KINDS = (
    ('plebum-complete-offline-tester-', 'complete', 'Complete offline tester'),
    ('plebum-website-tools-only-', 'tools', 'Website tools only'),
    ('plebum-tools-alpha-', 'focused', 'Focused dice and wallet-map tests'),
)


class DownloadLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        url = urlsplit(dict(attrs).get('href', ''))
        if url.netloc and (url.scheme != 'https' or url.netloc != 'musthavemustash.github.io'):
            return
        if url.path.startswith(BASE + 'testing/') and url.path.endswith('.zip'):
            path = url.path[len(BASE):]
            if '..' not in Path(path).parts and path not in self.paths:
                self.paths.append(path)


class EmbeddedCatalog(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'script' and 'pd-verify-catalog' in attributes.get('class', '').split():
            self.inside = True

    def handle_data(self, data):
        if self.inside:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.inside = False


def retain_previous_packages(catalog, previous_page):
    if not previous_page.is_file():
        return catalog
    parser = EmbeddedCatalog()
    parser.feed(previous_page.read_text(encoding='utf-8'))
    if not parser.parts:
        raise ValueError('Existing verifier has no reference catalog')
    previous = json.loads(''.join(parser.parts))
    if previous.get('schema') != 1 or not isinstance(previous.get('packages'), list):
        raise ValueError('Existing verifier has an invalid reference catalog')
    known = {(p['sha256'], p['bytes']) for p in catalog['packages']}
    counts = {package_id: 0 for _, package_id, _ in KINDS}
    for candidate in previous['packages']:
        package_id = candidate.get('id')
        size = candidate.get('bytes')
        digest = candidate.get('sha256', '')
        if package_id not in counts or type(size) is not int or not 0 < size <= MAX_BYTES or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('Existing verifier contains an invalid package reference')
        if (digest, size) in known or counts[package_id] >= 3:
            continue
        item = dict(candidate)
        item['current'] = False
        checksum = urlsplit(item['checksumUrl'])
        if checksum.netloc == 'musthavemustash.github.io' and checksum.path.startswith(BASE):
            item['checksumUrl'] = 'https://github.com/musthavemustash/plebum-dominium-test/commits/main/docs/' + checksum.path[len(BASE):]
        catalog['packages'].append(item)
        known.add((digest, size))
        counts[package_id] += 1
    return catalog


def sha256_file(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def read_sums(path):
    sums = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-fA-F]{64}) [ *](.+)', line)
        if not match or match[2] in sums:
            raise ValueError(f'Invalid or duplicate checksum row in {path}')
        sums[match[2]] = match[1].lower()
    return sums


def read_catalog(docs, require_archives=True):
    links = DownloadLinks()
    links.feed((docs / 'downloads.html').read_text(encoding='utf-8'))
    packages = []
    for prefix, package_id, label in KINDS:
        candidates = [p for p in links.paths if Path(p).name.startswith(prefix)]
        if len(candidates) != 1:
            raise ValueError(f'Expected one current {label} ZIP link, found {len(candidates)}')
        relative = candidates[0]
        archive = docs / relative
        directory = archive.parent
        manifest_path = directory / 'manifest.json'
        sums_path = directory / 'SHA256SUMS.txt'
        sums = read_sums(sums_path)
        if sha256_file(manifest_path) != sums.get('manifest.json'):
            raise ValueError(f'Manifest checksum mismatch: {manifest_path}')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest.get('status') != 'PUBLIC_TEST_ONLY' or manifest.get('custody_approved') is not False:
            raise ValueError(f'Unexpected package status: {manifest_path}')
        rows = manifest.get('packages', [manifest.get('archive', {})])
        matching = [p for p in rows if p.get('name') == archive.name]
        if len(matching) != 1:
            raise ValueError(f'Archive missing or duplicated in {manifest_path}: {archive.name}')
        item = matching[0]
        digest = item.get('sha256', '')
        size = item.get('size')
        if not re.fullmatch(r'[0-9a-f]{64}', digest) or digest != sums.get(archive.name):
            raise ValueError(f'Archive checksum mismatch between published references: {archive.name}')
        if type(size) is not int or not 0 < size <= MAX_BYTES:
            raise ValueError(f'Unsupported archive size: {archive.name}')
        if require_archives:
            if archive.stat().st_size != size or sha256_file(archive) != digest:
                raise ValueError(f'Archive bytes disagree with published references: {archive.name}')
        packages.append({
            'id': package_id,
            'label': label,
            'name': archive.name,
            'release': manifest.get('release', directory.name),
            'sha256': digest,
            'bytes': size,
            'checksumUrl': ORIGIN + BASE + sums_path.relative_to(docs).as_posix(),
            'downloadUrl': ORIGIN + BASE + relative,
            'current': True,
        })
    return {'schema': 1, 'packages': packages}


def build(root=ROOT, require_archives=True):
    docs = root / 'docs'
    catalog = read_catalog(docs, require_archives)
    catalog = retain_previous_packages(catalog, docs / 'verify-download.html')
    template = (root / 'templates/download-verifier.html').read_text(encoding='utf-8')
    css = (docs / 'assets/css/download-verifier.css').read_text(encoding='utf-8')
    javascript = (docs / 'assets/js/download-verifier.js').read_text(encoding='utf-8')
    # JSON is data inside an HTML script element, never executable source.
    data = json.dumps(catalog, ensure_ascii=False, indent=2).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    if '</script' in javascript.lower() or '</style' in css.lower():
        raise ValueError('Unexpected HTML closing tag in inline source')
    page = template.replace('{{VERIFIER_CSS}}', css).replace('{{VERIFIER_JS}}', javascript).replace('{{CATALOG_JSON}}', data)
    if re.search(r'\{\{[A-Z_]+\}\}', page):
        raise ValueError('Unresolved verifier template token')
    match = re.search(r'<!-- verifier-widget:start -->(.*?)<!-- verifier-widget:end -->', page, re.S)
    if not match:
        raise ValueError('Missing reusable widget markers')
    css_version = hashlib.sha256(css.encode()).hexdigest()[:12]
    js_version = hashlib.sha256(javascript.encode()).hexdigest()[:12]
    widget = (START + '\n'
              f'<link rel="stylesheet" href="{BASE}assets/css/download-verifier.css?v={css_version}">\n'
              + match[1].strip() + '\n'
              f'<script src="{BASE}assets/js/download-verifier.js?v={js_version}" defer></script>\n'
              + END)
    downloads_path = docs / 'downloads.html'
    downloads = downloads_path.read_text(encoding='utf-8')
    if downloads.count(START) != 1 or downloads.count(END) != 1:
        raise ValueError('Downloads must contain exactly one verifier placeholder')
    downloads = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: widget, downloads, count=1, flags=re.S)
    (docs / 'verify-download.html').write_text(page, encoding='utf-8')
    downloads_path.write_text(downloads, encoding='utf-8')
    print(f'Built local SHA-256 verifier for {len(catalog["packages"])} published ZIP packages.')
    return catalog


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-only', action='store_true',
                        help='Prepare a preview using published manifests; skip checking unavailable archive bytes.')
    arguments = parser.parse_args()
    build(require_archives=not arguments.metadata_only)
