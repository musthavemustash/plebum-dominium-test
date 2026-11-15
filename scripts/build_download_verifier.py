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
SIGNED_RELEASE = '20261115-r1'
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
    if previous.get('schema') not in (1, 2) or not isinstance(previous.get('packages'), list):
        raise ValueError('Existing verifier has an invalid reference catalog')
    known = {(p['sha256'], p['bytes']) for p in catalog['packages']}
    # Old generated pages can contain labels from an intervening build. Keep
    # history only when a saved manifest and the actual archive agree, and get
    # its name/release from that manifest rather than copying stale labels.
    docs = previous_page.parent
    archived = {}
    for manifest_path in sorted((docs / 'testing').glob('*/manifest.json')):
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        for row in manifest.get('packages', [manifest.get('archive', {})]):
            if row.get('name') and row.get('sha256') and type(row.get('size')) is int:
                archived[(row['sha256'], row['size'])] = (manifest_path, manifest, row)
    counts = {package_id: 0 for _, package_id, _ in KINDS}
    for candidate in previous['packages']:
        package_id = candidate.get('id')
        size = candidate.get('bytes')
        digest = candidate.get('sha256', '')
        if package_id not in counts or type(size) is not int or not 0 < size <= MAX_BYTES or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('Existing verifier contains an invalid package reference')
        if (digest, size) in known or counts[package_id] >= 3:
            continue
        saved = archived.get((digest, size))
        if saved is None:
            continue  # No saved published package supports this old reference.
        manifest_path, manifest, row = saved
        archive = manifest_path.parent / row['name']
        prefix, actual_id, label = next((kind for kind in KINDS if row['name'].startswith(kind[0])), (None, None, None))
        if actual_id != package_id or archive.parent != manifest_path.parent:
            raise ValueError('Invalid historical package identity')
        sums = read_sums(manifest_path.parent / 'SHA256SUMS.txt')
        if (sums.get('manifest.json') != sha256_file(manifest_path) or
                sums.get(row['name']) != digest or archive.stat().st_size != size or
                sha256_file(archive) != digest):
            raise ValueError('Historical archive disagrees with its published references: ' + str(archive))
        relative = manifest_path.parent.relative_to(docs).as_posix() + '/'
        item = dict(id=actual_id, label=label, name=row['name'],
                    release=manifest.get('release', manifest_path.parent.name),
                    sha256=digest, bytes=size, current=False,
                    checksumUrl='https://github.com/musthavemustash/plebum-dominium-test/commits/main/docs/' + relative + 'SHA256SUMS.txt',
                    downloadUrl=ORIGIN + BASE + relative + row['name'])
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
    release_dir = docs / 'releases' / SIGNED_RELEASE
    signed_manifest = (release_dir / 'manifest.txt').read_bytes()
    sums = read_sums(release_dir / 'manifest.txt')
    if sums != {p['name']: p['sha256'] for p in packages}:
        raise ValueError('Signed manifest must cover exactly the current packages; obtain a new offline signature for a new release.')
    return {'schema': 2, 'packages': packages, 'signedRelease': {
        'release': SIGNED_RELEASE,
        'publicKey': (release_dir / 'plebum-public.asc').read_bytes().decode('ascii'),
        'manifest': signed_manifest.decode('ascii'),
        'signature': (release_dir / 'manifest.txt.asc').read_bytes().decode('ascii'),
    }}


def build(root=ROOT, require_archives=True):
    docs = root / 'docs'
    catalog = read_catalog(docs, require_archives)
    catalog = retain_previous_packages(catalog, docs / 'verify-download.html')
    # The reviewed docs page owns the markup. Never regenerate it from the
    # historical templates directory; only refresh its embedded assets/data.
    template = (docs / 'verify-download.html').read_text(encoding='utf-8')
    css = (docs / 'assets/css/download-verifier.css').read_text(encoding='utf-8')
    scripts = {
        'verifier-openpgp': 'assets/vendor/openpgp-6.3.2/openpgp.min.js',
        'verifier-signature': 'assets/js/download-signature.js',
        'verifier-ui': 'assets/js/download-verifier.js',
    }
    # JSON is data inside an HTML script element, never executable source.
    data = json.dumps(catalog, ensure_ascii=False, indent=2).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    if '</style' in css.lower():
        raise ValueError('Unexpected HTML closing tag in inline source')
    def replace_one(pattern, replacement, page):
        result, count = re.subn(pattern, lambda _: replacement, page, flags=re.S)
        if count != 1:
            raise ValueError('Expected exactly one embedded block: ' + pattern)
        return result
    page = replace_one(r'<style id="verifier-css">.*?</style>', '<style id="verifier-css">' + css + '</style>', template)
    page = replace_one(r'<script type="application/json" class="pd-verify-catalog">.*?</script>',
                       '<script type="application/json" class="pd-verify-catalog">' + data + '</script>', page)
    script_tags = []
    for element_id, relative in scripts.items():
        javascript = (docs / relative).read_text(encoding='utf-8')
        if '</script' in javascript.lower():
            raise ValueError('Unexpected HTML closing tag in inline source')
        page = replace_one(r'<script id="' + element_id + r'">.*?</script>',
                           '<script id="' + element_id + '">' + javascript + '</script>', page)
        version = hashlib.sha256(javascript.encode()).hexdigest()[:12]
        script_tags.append(f'<script src="{BASE}{relative}?v={version}" defer></script>')
    if re.search(r'\{\{[A-Z_]+\}\}', page):
        raise ValueError('Unresolved verifier template token')
    match = re.search(r'<!-- verifier-widget:start -->(.*?)<!-- verifier-widget:end -->', page, re.S)
    if not match:
        raise ValueError('Missing reusable widget markers')
    css_version = hashlib.sha256(css.encode()).hexdigest()[:12]
    widget = (START + '\n'
              f'<link rel="stylesheet" href="{BASE}assets/css/download-verifier.css?v={css_version}">\n'
              + match[1].strip() + '\n'
              + '\n'.join(script_tags) + '\n'
              + END)
    for name in ('downloads.html', 'index.html'):
        target = docs / name
        html = target.read_text(encoding='utf-8')
        if html.count(START) != 1 or html.count(END) != 1:
            raise ValueError(name + ' must contain exactly one verifier placeholder')
        html = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: widget, html, count=1, flags=re.S)
        target.write_text(html, encoding='utf-8')
    (docs / 'verify-download.html').write_text(page, encoding='utf-8')
    print(f'Updated shared signature + SHA-256 verifier for {len(catalog["packages"])} ZIP references.')
    return catalog


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-only', action='store_true',
                        help='Prepare a preview using published manifests; skip checking unavailable archive bytes.')
    arguments = parser.parse_args()
    build(require_archives=not arguments.metadata_only)
