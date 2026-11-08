#!/usr/bin/env python3
"""Add offline download entry points and assemble deterministic test packages.

Run on the authoritative docs/ checkout, then validate with scripts/build.py.
Only packaged guide copies receive local-file adaptations; sensitive tool bytes
and offline controls stay identical to their published source files.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = '/plebum-dominium-test/'
DEST = 'testing/offline-20261106'
OUT = DOCS / DEST
FULL = 'plebum-complete-offline-tester-20261106.zip'
TOOLS = 'plebum-website-tools-only-20261106.zip'
SENSITIVE = {'dice-converter.html', 'descriptor-tool.html'}
TOOL_NAMES = [
    'dice-converter.html', 'descriptor-tool.html', 'fingerprint-checker.html',
    'diceware-mapper.html', 'diceware.html', 'dice-rolls.html', 'quorum-demo.html',
    'descriptor-demo.html', 'dice-converter-demo.html', 'passphrase-demo.html',
    'step1-demo.html', 'tails-demo.html', 'verify-bundle-demo.html',
]
PYTHON = ['bip39_dice_converter.py', 'descriptor_obfuscator.py', 'eff_large_wordlist.txt']
FORM = 'https://forms.gle/UPp7q1tdvtTMjsQL7'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def link(path, label):
    return f'<a href="{BASE}{path}" download>{label}</a>'


def update_guides():
    links = {
        'dice': [('dice-converter.html', 'Dice converter HTML'), ('kit/bip39_dice_converter.py', 'Python dice converter')],
        'dice-one': [('dice-converter.html', 'Dice converter HTML'), ('kit/bip39_dice_converter.py', 'Python dice converter')],
        'verify': [('fingerprint-checker.html', 'Fingerprint checker'), (DEST + '/SHA256SUMS.txt', 'ZIP checksums')],
        'encryption': [('descriptor-tool.html', 'Wallet-map tool HTML'), ('kit/descriptor_obfuscator.py', 'Python wallet-map tool')],
        'single-sig': [('diceware-mapper.html', 'Diceware mapper'), ('kit/eff_large_wordlist.txt', 'EFF wordlist')],
        'two-devices': [('dice-converter.html', 'Dice converter HTML'), ('dice-rolls.html', 'Dice-roll reference')],
        'sparrow': [('quorum-demo.html', '2-of-3 demo')],
        'airgap': [(DEST + '/' + FULL, 'Complete offline tester ZIP')],
        'checklist': [(DEST + '/' + FULL, 'Complete offline tester ZIP'), (DEST + '/' + TOOLS, 'Website tools only ZIP')],
        'checklist-one': [(DEST + '/' + FULL, 'Complete offline tester ZIP'), (DEST + '/' + TOOLS, 'Website tools only ZIP')],
    }
    for slug, items in links.items():
        path = DOCS / 'handouts' / (slug + '.html')
        s = path.read_text()
        s = re.sub(r'\n?<!-- offline-downloads -->.*?<!-- /offline-downloads -->', '', s, flags=re.S)
        block = '<!-- offline-downloads --><section class="entry-card" aria-label="Offline testing downloads"><p class="guide-needs"><strong>You will need for offline testing:</strong> '
        block += ' · '.join(link(p, label) for p, label in items)
        block += f'</p><p>Save these files before disconnecting. Public test data only; tools remain under review. <a href="{BASE}downloads.html#offline-tester">Full offline kit and instructions →</a></p></section><!-- /offline-downloads -->'
        match = re.search(r'<p class="guide-needs">.*?</p>', s, re.S)
        if match:
            s = s[:match.end()] + '\n' + block + s[match.end():]
        else:
            s = re.sub(r'(</h1>)', lambda m: m[0] + '\n' + block, s, count=1)
        path.write_text(s)
    path = DOCS / 'downloads.html'
    s = path.read_text()
    s = re.sub(r'<!-- offline-downloads -->.*?<!-- /offline-downloads -->', '', s, flags=re.S)
    section = f'''<!-- offline-downloads --><section class="entry-card" id="offline-tester">
<p class="entry-label">Start here · Complete offline public tester</p>
<h2>Download the whole site for offline testing</h2>
<p>Both guide paths, navigation, local search, diagrams, website tools, Python helpers, wordlist, public fixtures and testing instructions in one ZIP. No internet connection or local server is needed to browse the extracted site.</p>
<div class="entry-actions">{link(DEST + '/' + FULL, 'Download complete offline tester ZIP →')}{link(DEST + '/' + TOOLS, 'Download website tools only ZIP →')}</div>
<p><strong>Extract the entire ZIP, open the <code>plebum-offline</code> folder, then open <code>START.html</code>.</strong> For the T2–T5 tool checks, open <code>public-tests</code> inside that folder. Its <code>fixtures</code> folder holds the supplied test inputs: <code>plebum-offline/public-tests/fixtures/</code>. Use the matching HTML and Python tools beside that <code>fixtures</code> folder.</p>
<p>For T1, run <code>verify_package.py</code> from <code>plebum-offline</code> to check the whole offline package. Commands and paths in <code>public-tests/TESTING.txt</code> start from <code>public-tests</code>; open your terminal there for those checks. The focused dice/map ZIP instead uses <code>plebum-public-test/fixtures/</code>.</p>
<p>Disconnect before testing sensitive tools. They must run as local files; keep their existing safeguards in place. Python helpers require Python 3; the Python wallet-map tool also requires GnuPG, installed separately before disconnecting.</p>
<p>The tools-only ZIP contains the site’s utilities, demos, Python helpers, wordlist and public fixtures, without the guides or legacy print documents. Neither ZIP includes Tails, Sparrow, Electrum or other external software. Feedback, external references, live prices and network transactions require internet access.</p>
<p><strong>Public testing only. Do not use real wallet secrets, passwords, entropy or funds.</strong> Browser and physical Tails validation remain incomplete.</p>
<p><a href="{BASE}{DEST}/README.txt">Setup and contents</a> · <a href="{BASE}{DEST}/SHA256SUMS.txt">ZIP checksums</a> · <a href="{BASE}{DEST}/manifest.json">Package manifests</a> · <a href="{BASE}test-the-site.html#advanced">Testing tasks and feedback</a></p>
</section><!-- /offline-downloads -->'''
    s = s.replace('<h1>Downloads</h1>', '<h1>Downloads</h1>' + section, 1)
    s = s.replace('The tools are open for public testing. Download the alpha, try the supplied test cases, and help us check the results.', 'Choose the complete offline tester, the website tools only, or individual files below. All downloads are for public testing.')
    s = s.replace('Download public test ZIP →', 'Download focused dice/map test ZIP →')
    path.write_text(s)
    subprocess.run([sys.executable, str(ROOT / 'scripts/render_paths.py')], check=True)


def offline_copy(name, data):
    if name in SENSITIVE or not name.endswith(('.html', '.js', '.json', '.css')):
        return data
    s = data.decode('utf-8')
    if name.endswith('.html'):
        # No network subresources in the extracted guide: use system fonts.
        s = re.sub(r'<script\b[^>]*\bsrc=["\'](?:https?:)?//[^>]*>.*?</script>', '', s, flags=re.S)
        s = re.sub(r'<link\b[^>]*\bhref=["\'](?:https?:)?//[^>]*>', '', s)
        prefix = os.path.relpath('.', str(Path(name).parent)).replace(os.sep, '/')
        prefix = '' if prefix == '.' else prefix + '/'
        # Inline bootstrap runs before theme/search/navigation scripts.
        boot = '<script>window.PD_OFFLINE_ROOT=new URL(' + json.dumps(prefix or './') + ',location.href).href;</script>'
        s = s.replace('<head>', '<head>' + boot, 1)
        s = s.replace(BASE, prefix)
        s = s.replace('href="' + prefix + '"', 'href="' + prefix + 'index.html"')
        s = s.replace(DEST + '/' + FULL, 'START.html').replace(DEST + '/' + TOOLS, 'START.html')
        s = s.replace(DEST + '/README.txt', 'README.txt').replace(DEST + '/SHA256SUMS.txt', 'SHA256SUMS.txt').replace(DEST + '/manifest.json', 'package-manifest.json')
        if name == 'downloads.html':
            s = s.replace('Download complete offline tester ZIP →', 'Open offline start page →').replace('Download website tools only ZIP →', 'Open offline tools list →')
    if name == 'assets/js/main.js':
        s = s.replace('function basePath() {', 'function basePath() {\n    if (window.PD_OFFLINE_ROOT) return window.PD_OFFLINE_ROOT;')
        s = s.replace("var BASE = '/plebum-dominium-test/';", 'var BASE = window.PD_OFFLINE_ROOT;')
        s = s.replace('  var el = document.getElementById("ticker-price");', '  return; // Offline package: do not request live prices.\n  var el = document.getElementById("ticker-price");')
        s = s.replace("    fetch(basePath() + 'paths/' + searchPath + '/search-index.json')", "    Promise.resolve({json: function () { return window.PD_OFFLINE_INDEXES[searchPath]; }})")
    if name.endswith('.json'):
        s = s.replace(BASE, '')
    return s.encode()


def start_page(full):
    items = ([('index.html', 'Open the complete offline guide'), ('paths/one/index.html', 'One key + passphrase'), ('paths/three/index.html', 'Three keys')] if full else [])
    items += [(n, n.replace('.html', '').replace('-', ' ').capitalize()) for n in TOOL_NAMES]
    items += [('kit/' + n, n) for n in PYTHON]
    items += [('public-tests/TESTING.txt', 'Testing tasks and expected results'), ('public-tests/RESULTS.csv', 'Record results'), ('README.txt', 'Setup instructions')]
    links = ''.join(f'<li><a href="{p}">{label}</a></li>' for p, label in items)
    return ('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plebum · Offline public tester</title><style>body{font:18px/1.6 system-ui;max-width:850px;margin:3rem auto;padding:0 1.5rem;background:#faf8f2;color:#192b2a}a{color:#00685e}li{margin:.5rem 0}strong{color:#84351f}code{overflow-wrap:anywhere}summary{cursor:pointer;font-weight:600}</style></head><body><h1>Plebum offline public tester</h1><p><strong>Public test data only. Not approved for real-wallet use.</strong></p>
<h2>Before you begin</h2>
<ol>
<li>Extract the entire ZIP. Open the extracted <code>plebum-offline</code> folder, then open <code>START.html</code> (this page). Do not run files inside the compressed ZIP.</li>
<li>For <strong>T1: check the whole package</strong>, open a terminal in <code>plebum-offline</code> and run <code>python3 verify_package.py</code> (Windows: <code>py verify_package.py</code>). Stop and report any mismatch before running tools.</li>
<li>For <strong>T2–T5: find the test tools</strong>, return to your file manager and open <code>public-tests</code> inside <code>plebum-offline</code>. Use the HTML and Python tools in that folder.</li>
<li>Inside <code>public-tests</code>, open <code>fixtures</code> for the supplied inputs. The full path from the extracted package is <code>plebum-offline/public-tests/fixtures/</code>. For example, the wallet-map fixture is <code>plebum-offline/public-tests/fixtures/public-map.txt</code>.</li>
<li>Read <a href="public-tests/TESTING.txt">TESTING.txt</a>. Open a terminal in <code>public-tests</code> for its commands: paths such as <code>fixtures/public-map.txt</code> start there. Its separate <code>verify_package.py</code> checks only the focused test subset.</li>
</ol>
<p>Disconnect before testing sensitive tools. If a tool blocks your environment, record the result without bypassing its controls.</p>
<h2>Open the matching test files</h2>
<ul><li><a href="public-tests/dice-converter.html">Dice converter for T2/T3/T5</a></li><li><a href="public-tests/descriptor-tool.html">Wallet-map tool for T2/T4/T5</a></li><li><a href="public-tests/fixtures/README.md">Fixture guide</a> · <a href="public-tests/fixtures/public-map.txt">Public wallet-map text</a> · <a href="public-tests/fixtures/password.txt">Public test password</a></li></ul>
<details><summary>Guide and additional utilities</summary><ul>''' + links + f'</ul></details><p>Feedback requires reconnecting after the offline session: <a href="{FORM}">Submit non-sensitive results</a>.</p></body></html>').encode()


def manifest_files(files):
    return {name: {'sha256': digest(data), 'size': len(data)} for name, data in sorted(files.items())}


def package(full):
    files = {}
    for p in sorted(DOCS.rglob('*')):
        if not p.is_file() or p.is_relative_to(OUT):
            continue
        name = p.relative_to(DOCS).as_posix()
        if name.startswith('testing/') and not name.startswith(('testing/alpha-20261106-t3-t4/', 'testing/t4-20261106/')):
            continue
        if not full and not (name in TOOL_NAMES or name.startswith('assets/') or name in ['kit/' + n for n in PYTHON]):
            continue
        files[name] = offline_copy(name, p.read_bytes())
    alpha = DOCS / 'testing/alpha-20261106-t3-t4/plebum-tools-alpha-20261106-t3-t4.zip'
    with zipfile.ZipFile(alpha) as z:
        for name in z.namelist():
            if not name.endswith('/'):
                files['public-tests/' + name.split('/', 1)[1]] = z.read(name)
    files['START.html'] = start_page(full)
    if not full:
        # Reference-only return link in the dice reference has no guide in this ZIP.
        files['dice-rolls.html'] = files['dice-rolls.html'].replace(b'href="handouts/dice.html"', b'href="START.html"')
    files['README.txt'] = ('''PLEBUM DOMINIUM — OFFLINE PUBLIC TESTER — 2026-11-06
PUBLIC TEST DATA ONLY. NOT APPROVED FOR REAL-WALLET USE.

FIND THE RIGHT FOLDER
1. Extract the entire ZIP. Open the extracted plebum-offline folder.
2. Open START.html in that folder for the offline starting page.
3. For T1, open a terminal in plebum-offline and run its verify_package.py:
   python3 verify_package.py (Windows: py verify_package.py).
   This checks the whole offline package. Stop and report any mismatch.
4. For T2-T5, open public-tests inside plebum-offline in your file manager.
   Use the matching HTML and Python tools in that public-tests folder.
5. Open fixtures inside public-tests for the supplied test inputs.
   Full fixture path: plebum-offline/public-tests/fixtures/
   Example: plebum-offline/public-tests/fixtures/public-map.txt
6. Open a terminal in public-tests for the commands in TESTING.txt and
   RETEST-WINDOWS.txt. Their paths such as fixtures/public-map.txt start
   from public-tests. Save comparison/output files there when instructed.
   Its separate verify_package.py checks only the focused test subset.

These paths apply to both the complete offline ZIP and tools-only ZIP.
The separate focused dice/map ZIP instead extracts to plebum-public-test;
its fixtures folder is plebum-public-test/fixtures/.

No installation, internet connection or local server is needed for HTML tools.
The complete package includes both guide paths and embedded local search.
Use the downloaded HTML files directly (file://) on a disconnected machine.
If your browser still reports online or a tool blocks, record NOT TESTED/FAIL;
do not bypass safeguards. An offline indicator alone does not prove isolation.

The Python helpers require Python 3. descriptor_obfuscator.py also needs GnuPG.
Install those dependencies separately before disconnecting if testing Python.
Tails, Sparrow, Electrum, OS images and third-party installers are not bundled.
External references, feedback, live prices, testnet and network transactions
need a network connection and cannot be performed fully offline.

Read public-tests/TESTING.txt; record results in public-tests/RESULTS.csv.
The source tools in the package root retain their original sensitive controls.
public-tests contains the current focused alpha's matching tools and fixtures and its own README/manifest.
Its instructions apply to that subfolder, not the complete package layout.
Legacy PDFs and spreadsheets in the full package remain unreconciled and are
provided as review material. The HTML guides are the current reviewed text.
Browser/OS isolation, cross-platform operation and physical Tails tests remain
incomplete. Successful file checks do not certify safety or recovery.

Check all extracted files: python3 verify_package.py (Windows: py verify_package.py).
Checksums establish byte equality, not independent publisher authentication.
''').encode()
    files['verify_package.py'] = b'''from pathlib import Path
import hashlib, sys
root = Path(__file__).resolve().parent
rows = (root / 'SHA256SUMS.txt').read_text().splitlines()
bad = []
for row in rows:
    expected, name = row.split('  ', 1)
    p = (root / name).resolve()
    if not p.is_relative_to(root) or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
        bad.append(name)
print('FAIL: ' + ', '.join(bad) if bad else f'PASS: {len(rows)} files match. Public testing only.')
sys.exit(bool(bad))
'''
    if full:
        indexes = {k: json.loads(files['paths/' + k + '/search-index.json']) for k in ('one', 'three')}
        payload = 'window.PD_OFFLINE_INDEXES=' + json.dumps(indexes, ensure_ascii=True) + ';\n'
        # Make search result URLs absolute local-file URLs from the package root.
        payload += 'Object.values(window.PD_OFFLINE_INDEXES).forEach(function(rows){rows.forEach(function(e){e.url=new URL(e.url,window.PD_OFFLINE_ROOT).href;});});\n'
        files['assets/js/offline-indexes.js'] = payload.encode()
        for name in list(files):
            if name.endswith('.html') and name not in SENSITIVE:
                s = files[name].decode()
                if 'assets/js/main.js' in s:
                    prefix = os.path.relpath('.', str(Path(name).parent)).replace(os.sep, '/')
                    prefix = '' if prefix == '.' else prefix + '/'
                    s = s.replace('</head>', '<script src="' + prefix + 'assets/js/offline-indexes.js"></script></head>', 1)
                    files[name] = s.encode()
    for name in SENSITIVE:
        assert files[name] == (DOCS / name).read_bytes(), 'Sensitive tool changed: ' + name
    files['package-manifest.json'] = (json.dumps({'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False, 'files': manifest_files(files)}, indent=2) + '\n').encode()
    files['SHA256SUMS.txt'] = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(files.items())).encode()
    archive = FULL if full else TOOLS
    with zipfile.ZipFile(OUT / archive, 'w') as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('plebum-offline/' + name, (2026, 11, 5, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    return {'name': archive, 'sha256': digest((OUT / archive).read_bytes()), 'size': (OUT / archive).stat().st_size, 'files': manifest_files(files)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    update_guides()
    packages = [package(True), package(False)]
    (OUT / 'manifest.json').write_text(json.dumps({'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False, 'packages': packages}, indent=2) + '\n')
    (OUT / 'SHA256SUMS.txt').write_text(''.join(f'{p["sha256"]}  {p["name"]}\n' for p in packages) + f'{digest((OUT / "manifest.json").read_bytes())}  manifest.json\n')
    with zipfile.ZipFile(OUT / FULL) as z:
        (OUT / 'README.txt').write_bytes(z.read('plebum-offline/README.txt'))
    for p in packages:
        print(p['name'], p['size'], 'bytes;', len(p['files']), 'files;', p['sha256'])


if __name__ == '__main__':
    main()
