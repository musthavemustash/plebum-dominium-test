#!/usr/bin/env python3
"""Render optional, page-specific test panels and factual Google Forms prefills."""
import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = '/plebum-dominium-test/'
ORIGIN = 'https://musthavemustash.github.io'
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform'
STAMP = 'assets/data/page-tests-build.json'
CSS = BASE + 'assets/css/page-test-modules.css?v=1'
MARKER = r'\n?<!-- page-test-module -->.*?<!-- /page-test-module -->\n?'
AREAS = {'Getting Started / guides', 'Threat Model / security information',
         "If I'm Gone / inheritance guidance", 'Downloads / testing tools'}


def catalog():
    data = json.loads((ROOT / 'scripts/page_test_catalog.json').read_text())
    ids = []
    for slug, item in data.items():
        assert item['area'] in AREAS, slug
        assert 1 <= len(item['tasks']) <= 3, slug
        for task in item['tasks']:
            assert re.fullmatch(r'P-[A-Z0-9-]+-\d\d', task['id']), task
            assert all(task[k].strip() for k in ('try', 'expected', 'evidence')), task
            ids.append(task['id'])
    assert len(ids) == len(set(ids)), 'Duplicate page-task IDs'
    return data


def build_id(docs=DOCS):
    value = json.loads((docs / STAMP).read_text())['source_commit']
    if not re.fullmatch(r'[0-9a-f]{40}', value):
        raise ValueError('Page-test build must be a full source commit SHA')
    return value


def report_url(page_path, item, source_build):
    assert page_path.startswith(BASE) and page_path.endswith('.html'), page_path
    public_url = ORIGIN + page_path
    lines = ['Page: ' + public_url, 'Website content build: ' + source_build,
             'Mode tested (live website / offline copy):',
             'Tool/package filename and SHA-256, if applicable:', '']
    for task in item['tasks']:
        lines.extend([task['id'], 'Result (enter PASS, FAIL or NOT TESTED):',
                      'Expected: ' + task['expected'], 'Actual:',
                      'Steps or error messages:', ''])
    lines.append('Evidence link or output (public fixtures only):')
    # IDs read from the public form schema. No result, severity or feedback-type
    # choice is filled: a tester must supply their own observations and outcome.
    fields = {
        'usp': 'pp_url',
        'entry.460741145': 'General website feedback',
        'entry.1551279696': item['area'],
        'entry.1164893128': public_url,
        'entry.846110096': 'Website build ' + source_build,
        'entry.760527846': '\n'.join(lines),
    }
    return FORM + '?' + urlencode(fields)


def panel(slug, page_path, docs=DOCS):
    item = catalog()[slug]
    source_build = build_id(docs)
    tasks = []
    for task in item['tasks']:
        tasks.append('<li><p class="ptm-task-id"><code>' + escape(task['id']) + '</code></p>'
                     '<p class="ptm-try">' + escape(task['try']) + '</p>'
                     '<p><strong>Expected:</strong> ' + escape(task['expected']) + '</p>'
                     '<p class="ptm-evidence"><strong>Evidence:</strong> ' + escape(task['evidence']) + '</p></li>')
    count = len(item['tasks'])
    return ('<!-- page-test-module --><details class="page-test-module" id="help-test-page">'
            '<summary><span class="ptm-heading">Help test this page</span>'
            '<span class="ptm-count">Optional · ' + str(count) + (' check' if count == 1 else ' checks') + '</span></summary>'
            '<div class="ptm-body"><p class="ptm-intro">Try these checks and tell us what happened. '
            'Testing is optional for readers; reading this sheet does not complete a verification test.</p>'
            '<p class="ptm-public"><strong>Public examples only.</strong> Never use or share real seed words, '
            'private keys, passphrases, funds, wallet details, or personal recovery locations.</p>'
            '<ol class="ptm-tasks">' + ''.join(tasks) + '</ol>'
            '<p class="ptm-report-note">Record <strong>PASS, FAIL or NOT TESTED for each task</strong>. '
            'If a check is skipped or blocked, use NOT TESTED. Include your OS/browser versions and '
            'network state; attach output or a short recording where useful.</p>'
            '<p class="ptm-build">Website content build <code>' + source_build[:12] + '</code>. '
            'If you test a tool, also record its exact package filename and hash.</p>'
            '<a class="ptm-report" href="' + escape(report_url(page_path, item, source_build), quote=True) + '" '
            'target="_blank" rel="noopener noreferrer">Report results for this page <span aria-hidden="true">↗</span></a>'
            '<p class="ptm-form-note">Opens Google Forms with the public page URL, task IDs and website build filled in. '
            'Choose your own result. Use General website feedback for these page checks; '
            'the full T1–T5 tool suites have their own sections.</p>'
            '<p class="ptm-offline">Using an offline copy? Finish testing before reconnecting to report. '
            'Say “offline copy” and identify your downloaded package. The reporting link uses the public page URL, '
            'never your local file path.</p></div></details><!-- /page-test-module -->')


def with_page_test(html, slug, page_path, docs=DOCS):
    html = re.sub(MARKER, '', html, flags=re.S)
    html = re.sub(r'(?m)^[ \t]+$', '', html)
    block = '\n' + panel(slug, page_path, docs) + '\n'
    match = re.search(r'[ \t]*<nav class="prevnext-row"', html)
    if match:
        html = html[:match.start()] + block + html[match.start():]
    elif '</article>' in html:
        html = html.replace('</article>', block + '</article>', 1)
    else:
        raise ValueError('No guide article for page-test module: ' + page_path)
    if CSS not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="' + CSS + '">\n</head>', 1)
    return html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', help='Set the persisted source commit once during publication')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.build:
        if args.check or not re.fullmatch(r'[0-9a-f]{40}', args.build):
            parser.error('--build requires a full SHA and cannot be combined with --check')
        dest = DOCS / STAMP
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps({'source_commit': args.build}, indent=2) + '\n')
    pages = sorted((DOCS / 'handouts').glob('*.html')) + [DOCS / 'choose-path.html']
    changed = []
    for path in pages:
        relative = path.relative_to(DOCS).as_posix()
        old = path.read_text()
        new = with_page_test(old, path.stem, BASE + relative)
        if old != new:
            changed.append(relative)
            if not args.check:
                path.write_text(new)
    if args.check and changed:
        raise SystemExit('Stale page-test modules: ' + ', '.join(changed))
    print('Page-test panels:', len(pages), 'canonical pages', 'checked' if args.check else 'rendered')


if __name__ == '__main__':
    main()
