#!/usr/bin/env python3
"""Validate the authoritative, buildless staging site in docs/ without rewriting it.

The former Markdown generator is retained in Git history. It predates the reviewed
HTML and must not regenerate staging. Run python3 scripts/build.py before a PR.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STAGING_BASE = '/plebum-dominium-test/'


class References(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        key = 'src' if tag in ('script', 'img', 'iframe', 'source') else 'href'
        if tag in ('script', 'img', 'iframe', 'source', 'a', 'link') and attrs.get(key):
            self.references.append((self.getpos()[0], attrs[key]))


def validate(site_dir):
    site_dir = site_dir.resolve()
    errors = []
    for required in ('index.html', '.nojekyll', 'assets/css/main.css', 'assets/js/main.js',
                     'handouts/sparrow.html', 'handouts/threat-model.html'):
        if not (site_dir / required).is_file():
            errors.append(f'Missing required staging file: {required}')
    if (site_dir / 'CNAME').exists():
        errors.append('Staging must not contain a CNAME file that redirects to a custom domain.')
    pages = sorted(site_dir.rglob('*.html'))
    for page in pages:
        parser = References()
        try:
            parser.feed(page.read_text(encoding='utf-8'))
        except (UnicodeError, ValueError) as exc:
            errors.append(f'{page.relative_to(site_dir)}: cannot parse: {exc}')
            continue
        for line, ref in parser.references:
            url = urlsplit(ref)
            if url.scheme or url.netloc or not url.path:
                continue  # External URLs and fragment-only links are separate review checks.
            path = unquote(url.path)
            if path.startswith(STAGING_BASE):
                target = site_dir / path[len(STAGING_BASE):]
            elif path.startswith('/'):
                errors.append(f'{page.relative_to(site_dir)}:{line}: outside staging base: {ref}')
                continue
            else:
                target = page.parent / path
            target = target.resolve()
            if not target.is_relative_to(site_dir):
                errors.append(f'{page.relative_to(site_dir)}:{line}: escapes site directory: {ref}')
            elif not target.exists():
                errors.append(f'{page.relative_to(site_dir)}:{line}: missing local target: {ref}')
    return pages, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default=STAGING_BASE, help='Only the staging project base is allowed.')
    parser.add_argument('--site-dir', type=Path, default=ROOT / 'docs', help='Static directory to validate.')
    args = parser.parse_args(argv)
    if args.base != STAGING_BASE:
        parser.error(f'This staging repository only supports --base {STAGING_BASE}')
    pages, errors = validate(args.site_dir)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Validated {len(pages)} static HTML pages. No files rewritten. Staging base: {STAGING_BASE}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
