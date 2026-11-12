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
from reconcile_tool_downloads import CURRENT

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = '/plebum-dominium-test/'
DEST = 'testing/offline-20261112-r2'
OUT = DOCS / DEST
FULL = 'plebum-complete-offline-tester-20261112-r2.zip'
TOOLS = 'plebum-website-tools-only-20261112-r2.zip'
SENSITIVE = {'dice-converter.html', 'descriptor-tool.html', 'diceware-mapper.html'}
EXACT = SENSITIVE | {'fingerprint-checker.html', 'verify-file.html', 'kit/hash_checker.html'}
TOOL_NAMES = [
    'dice-converter.html', 'descriptor-tool.html', 'fingerprint-checker.html',
    'diceware-mapper.html', 'diceware.html', 'dice-rolls.html', 'quorum-demo.html',
    'descriptor-demo.html', 'dice-converter-demo.html', 'passphrase-demo.html',
    'step1-demo.html', 'tails-demo.html', 'verify-bundle-demo.html', 'verify-file.html',
]
PYTHON = ['bip39_dice_converter.py', 'descriptor_obfuscator.py', 'eff_large_wordlist.txt']
KIT_FILES = {'kit/' + n for n in PYTHON + ['VERIFY.md', 'hash_checker.html']}
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def link(path, label):
    return f'<a href="{BASE}{path}" download>{label}</a>'


def offline_verifier_notice():
    # A verifier containing this archive's final hash must be saved separately.
    return '''<!-- download-verifier --><section id="verify-download" class="entry-card"><h3>Verify the ZIP before extracting</h3><p>Use the <a href="https://musthavemustash.github.io/plebum-dominium-test/verify-download.html">download verifier</a> to select your ZIP and compare it on your device. Save that verifier separately before disconnecting if you want to check offline. Then run the included <code>verify_package.py</code> for T1 after extraction.</p></section><!-- /download-verifier -->'''


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
<p>Both guide paths, navigation, local search, diagrams, website tools, Python helpers, wordlist, public fixtures and testing instructions in one ZIP. Legacy PDFs, slides and the recovery worksheet are excluded pending reconciliation. No internet connection or local server is needed to browse the extracted site.</p>
<div class="entry-actions">{link(DEST + '/' + FULL, 'Download complete offline tester ZIP →')}{link(DEST + '/' + TOOLS, 'Download website tools only ZIP →')}</div>
{offline_verifier_notice()}
<p><strong>Extract the entire ZIP, open the <code>plebum-offline</code> folder, then open <code>START.html</code>.</strong> For the T2–T5 tool checks, open <code>public-tests</code> inside that folder. Its <code>fixtures</code> folder holds the supplied test inputs: <code>plebum-offline/public-tests/fixtures/</code>. Use the matching HTML and Python tools beside that <code>fixtures</code> folder.</p>
<p>For T1, run <code>verify_package.py</code> from <code>plebum-offline</code> to check the whole offline package. Commands and paths in <code>public-tests/TESTING.txt</code> start from <code>public-tests</code>; open your terminal there for those checks. The focused tool ZIP instead uses <code>plebum-public-test/fixtures/</code>.</p>
<p><a href="{BASE}offline-folder-guide.html">Find the tools and fixtures</a> · <a href="{BASE}testing/session-guide/TESTING.txt">T1–T5 with screenshot checkpoints</a> · <a href="{BASE}testing/session-guide/EVIDENCE-CHECKLIST.txt">Save to USB before shutdown</a> · <a href="{BASE}testing/session-guide/FORM-REPORTING.txt">Submit screenshots and evidence links</a></p>
<p>Disconnect before testing sensitive tools. They must run as local files; keep their existing safeguards in place. Python helpers require Python 3; the Python wallet-map tool also requires GnuPG, installed separately before disconnecting.</p>
<p>The tools-only ZIP contains the site’s utilities, demos, Python helpers, wordlist and public fixtures, without the guides or legacy print documents. Neither ZIP includes Tails, Sparrow, Electrum or other external software. Feedback, external references, live prices and network transactions require internet access.</p>
<p><strong>Public testing only. Do not use real wallet secrets, passwords, entropy or funds.</strong></p>
<p><strong>Evidence for this revision.</strong> The four HTML tools have new SHA-256 hashes after label updates and new expected hashes in the Fingerprint checker. The recorded Windows and Tails R4 results apply to the original files and checks. The Python helpers, wordlist and fixtures match R4 byte for byte.</p>
<p>Run T1 on the exact ZIP you download. Record a focused Windows and physical Tails retest of the revised HTML tools, including names, file links, fingerprint matches and mismatches, offline controls and fixture results. Physical confirmation of the revised HTML files and automatic network isolation remain open.</p>
<p><a href="{BASE}{DEST}/README.txt">Setup and contents</a> · <a href="{BASE}{DEST}/SHA256SUMS.txt">ZIP checksums</a> · <a href="{BASE}{DEST}/manifest.json">Package manifests</a> · <a href="{BASE}test-the-site.html#tasks">Testing tasks and feedback</a></p>
</section><!-- /offline-downloads -->'''
    s = s.replace('<h1>Downloads</h1>', '<h1>Downloads</h1>' + section, 1)
    s = s.replace('The tools are open for public testing. Download the alpha, try the supplied test cases, and help us check the results.', 'Choose the complete offline tester, the website tools only, or individual files below. All downloads are for public testing.')
    s = s.replace('Download public test ZIP →', 'Download focused tool test ZIP →')
    path.write_text(s)
    subprocess.run([sys.executable, str(ROOT / 'scripts/render_paths.py')], check=True)


def offline_copy(name, data):
    if name in EXACT or name == 'offline-folder-guide.html' or not name.endswith(('.html', '.js', '.json', '.css')):
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
        # The ZIP verifier is saved separately, never included in its own archive.
        s = s.replace('href="' + prefix + 'verify-download.html"',
                      'href="https://musthavemustash.github.io/plebum-dominium-test/verify-download.html"')
        s = s.replace('testing/offline-20261106/', DEST + '/')
        s = s.replace('plebum-complete-offline-tester-20261106.zip', FULL).replace('plebum-website-tools-only-20261106.zip', TOOLS)
        s = s.replace('href="' + prefix + '"', 'href="' + prefix + 'index.html"')
        s = s.replace(DEST + '/' + FULL, 'START.html').replace(DEST + '/' + TOOLS, 'START.html')
        s = s.replace(DEST + '/README.txt', 'README.txt').replace(DEST + '/SHA256SUMS.txt', 'SHA256SUMS.txt').replace(DEST + '/manifest.json', 'package-manifest.json')
        if name == 'downloads.html':
            s = s.replace('Download complete offline tester ZIP →', 'Open offline start page →').replace('Download website tools only ZIP →', 'Open offline tools list →')
            # Replace after local-path rewriting so the absolute online link
            # stays intact. Never embed an archive's own checksum in itself.
            s = re.sub(r'<!-- download-verifier -->.*?<!-- /download-verifier -->',
                       lambda _: offline_verifier_notice(), s, flags=re.S)
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
    labels = {'dice-converter.html': 'Dice converter', 'descriptor-tool.html': 'Wallet-map tool',
              'diceware-mapper.html': 'Diceware mapper', 'fingerprint-checker.html': 'Fingerprint checker',
              'descriptor-demo.html': 'Wallet-map tool demo', 'passphrase-demo.html': 'Diceware mapper demo',
              'diceware.html': 'Diceware mapper demo', 'dice-converter-demo.html': 'Dice converter demo'}
    items += [(n, labels.get(n, n.replace('.html', '').replace('-', ' ').capitalize()) + ' (' + n + ')') for n in TOOL_NAMES]
    items += [('kit/' + n, n) for n in PYTHON]
    items += [('public-tests/TESTING.txt', 'T1–T5: steps and screenshot checkpoints'), ('public-tests/EVIDENCE-CHECKLIST.txt', 'Save to USB before shutdown'), ('public-tests/FORM-REPORTING.txt', 'Google Form fields and shareable evidence links'), ('public-tests/SESSION-NOTES.txt', 'Copyable session notes'), ('public-tests/RESULTS.csv', 'Record results'), ('README.txt', 'Setup instructions')]
    links = ''.join(f'<li><a href="{p}">{label}</a></li>' for p, label in items)
    return ('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plebum · Offline public tester</title><style>body{font:18px/1.6 system-ui;max-width:850px;margin:3rem auto;padding:0 1.5rem;background:#faf8f2;color:#192b2a}a{color:#00685e}li{margin:.5rem 0}strong{color:#84351f}code{overflow-wrap:anywhere}summary{cursor:pointer;font-weight:600}</style></head><body><h1>Plebum offline public tester</h1><p><strong>Public test data only. Not approved for real-wallet use.</strong></p>
<h2>Before you begin</h2>
<p><a href="offline-folder-guide.html">Illustrated folder guide: from the ZIP to the fixtures →</a></p>
<ol>
<li>Extract the entire ZIP. Open the extracted <code>plebum-offline</code> folder, then open <code>START.html</code> (this page). Do not run files inside the compressed ZIP.</li>
<li>For <strong>T1: check the whole package</strong>, open a terminal in <code>plebum-offline</code> and run <code>python3 verify_package.py</code> (Windows: <code>py verify_package.py</code>). Stop and report any mismatch before running tools.</li>
<li>For <strong>T2–T5: find the test tools</strong>, return to your file manager and open <code>public-tests</code> inside <code>plebum-offline</code>. Use the HTML and Python tools in that folder.</li>
<li>Inside <code>public-tests</code>, open <code>fixtures</code> for the supplied inputs. The full path from the extracted package is <code>plebum-offline/public-tests/fixtures/</code>. For example, the wallet-map fixture is <code>plebum-offline/public-tests/fixtures/public-map.txt</code>.</li>
<li>Read <a href="public-tests/TESTING.txt">TESTING.txt</a>. Open a terminal in <code>public-tests</code> for its commands: paths such as <code>fixtures/public-map.txt</code> start there. Its separate <code>verify_package.py</code> checks only the focused test subset.</li>
</ol>
<p>Disconnect before testing sensitive tools. If a tool blocks your environment, record the result without bypassing its controls.</p>
<h2>Save as you go</h2><p>Take a screenshot after each result, before clearing or continuing. Copy it to your separate test/data USB. Before reboot or shutdown, follow <a href="public-tests/EVIDENCE-CHECKLIST.txt">Save and check your evidence</a>: wait for copying, reopen an actual image and text file from the USB, then safely eject it and shut down.</p><p>After the offline session, use <a href="public-tests/FORM-REPORTING.txt">the Google Form field guide</a>. Attach screenshots if your selected task offers an upload section; otherwise use an evidence link. This guide shows how to upload public evidence to Drive, make a Viewer link and test access before submitting.</p><h2>Open the matching test files</h2>
<ul><li><a href="public-tests/dice-converter.html">Dice converter (dice-converter.html) for T2/T3/T5</a></li><li><a href="public-tests/descriptor-tool.html">Wallet-map tool (descriptor-tool.html) for T2/T4/T5</a></li><li><a href="public-tests/diceware-mapper.html">Diceware mapper (diceware-mapper.html)</a></li><li><a href="public-tests/fingerprint-checker.html">Fingerprint checker (fingerprint-checker.html)</a></li><li><a href="public-tests/fixtures/README.md">Fixture guide</a> · <a href="public-tests/fixtures/public-map.txt">Public wallet-map text</a> · <a href="public-tests/fixtures/password.txt">Public test password</a></li></ul>
<details><summary>Guide and additional utilities</summary><ul>''' + links + f'</ul></details><p>Feedback requires reconnecting after the offline session: <a href="{FORM}">Submit non-sensitive results</a>.</p></body></html>').encode()


def manifest_files(files):
    return {name: {'sha256': digest(data), 'size': len(data)} for name, data in sorted(files.items())}


def package(full):
    files = {}
    for p in sorted(DOCS.rglob('*')):
        if p.suffix.lower() in {'.pdf', '.pptx', '.xlsx', '.pyc'}:
            continue  # Legacy documents await content reconciliation and print review.
        if not p.is_file() or p.is_relative_to(OUT) or '__pycache__' in p.parts:
            continue
        name = p.relative_to(DOCS).as_posix()
        if name.startswith('kit/') and name not in KIT_FILES:
            continue  # Do not reintroduce legacy bundles, instructions or pinned helpers.
        if name == 'verify-download.html':
            continue  # Generated after ZIPs; downloaded separately for offline use.
        if name.startswith('testing/') and not name.startswith((CURRENT.rsplit('/', 1)[0] + '/', 'testing/alpha-20261108-t5-r4/', 'testing/t4-20261106/', 'testing/t5-20261108/', 'testing/session-guide/', 'testing/tails-r4-20261109/', 'testing/windows-r4-20261108/')):
            continue
        if not full and not (name in TOOL_NAMES or name == 'offline-folder-guide.html' or name.startswith('assets/') or name in KIT_FILES):
            continue
        files[name] = offline_copy(name, p.read_bytes())
    alpha = DOCS / CURRENT
    with zipfile.ZipFile(alpha) as z:
        for name in z.namelist():
            if not name.endswith('/'):
                files['public-tests/' + name.split('/', 1)[1]] = z.read(name)
    files['START.html'] = start_page(full)
    if not full:
        # Reference-only return link in the dice reference has no guide in this ZIP.
        files['dice-rolls.html'] = files['dice-rolls.html'].replace(b'href="handouts/dice.html"', b'href="START.html"')
    files['README.txt'] = ('''PLEBUM DOMINIUM — OFFLINE PUBLIC TESTER — 2026-11-12 r2
PUBLIC TEST DATA ONLY. NOT APPROVED FOR REAL-WALLET USE.

FIND THE RIGHT FOLDER
1. Extract the entire ZIP. Open the extracted plebum-offline folder.
2. Open START.html in that folder for the offline starting page.
   For illustrated steps, open offline-folder-guide.html beside START.html.
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
The separate focused tool ZIP instead extracts to plebum-public-test;
its fixtures folder is plebum-public-test/fixtures/.

No installation, internet connection or local server is needed for HTML tools.
The complete package includes both guide paths and embedded local search.
Use the downloaded HTML files directly (file://) on a disconnected machine.
The public-session candidate may show a true browser flag in isolated Tails.
Complete OS checks before its acknowledgments. It cannot verify isolation or
reliably detect reconnection. Keep networking disabled; Lock and clear before
changing network settings. Automatic isolation acceptance remains unresolved.

The Python helpers require Python 3. descriptor_obfuscator.py also needs GnuPG.
Install those dependencies separately before disconnecting if testing Python.
Tails, Sparrow, Electrum, OS images and third-party installers are not bundled.
External references, feedback, live prices, testnet and network transactions
need a network connection and cannot be performed fully offline.

Read public-tests/TESTING.txt. Copy RESULTS.csv and SESSION-NOTES.txt into a
results folder before editing; keep packaged originals intact. Save each result
screenshot before the next input. Follow public-tests/EVIDENCE-CHECKLIST.txt
to transfer and reopen evidence on a separate data USB before Tails shuts down.
Read public-tests/FORM-REPORTING.txt for exact Google Form fields and evidence
sharing instructions. Upload only public-test evidence after the offline session.
The source tools in the package root retain their original sensitive controls.
public-tests contains the current focused alpha's matching tools and fixtures and its own README/manifest.
Tool names: Dice converter (dice-converter.html); Wallet-map tool
(descriptor-tool.html); Diceware mapper (diceware-mapper.html);
Fingerprint checker (fingerprint-checker.html).
Its instructions apply to that subfolder, not the complete package layout.
Legacy PDFs, slides and spreadsheets are excluded pending reconciliation
and print review. Use the current HTML guides for printable instructions.
Earlier candidate evidence is included in public-tests/TAILS-RETEST-RESULTS.txt.
This revision aligns tool names and filenames across the guide and tools.
The sensitive tools' executable code, Python helpers, wordlist and fixtures
are unchanged from R4. HTML labels and the checker's expected hashes changed.
No new physical Windows/Tails pass is claimed. Check T1 and tool names/hashes.
Record this ZIP filename and full SHA-256 in a new evidence folder. Keep earlier
ZIPs and results unchanged. Run T1 for the new ZIP. The
complete wallet rehearsals remain outstanding. Successful file checks do not
certify safety or recovery.

Tails extraction note: unzip was unavailable in the recorded Tails 7.16 run.
If it is unavailable in your environment, extract with Python:
python3 -m zipfile -e plebum-complete-offline-tester-20261112-r2.zip .
For the tools-only ZIP, substitute its filename in that command.

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
            if name.endswith('.html') and name not in EXACT:
                s = files[name].decode()
                if 'assets/js/main.js' in s:
                    prefix = os.path.relpath('.', str(Path(name).parent)).replace(os.sep, '/')
                    prefix = '' if prefix == '.' else prefix + '/'
                    s = s.replace('</head>', '<script src="' + prefix + 'assets/js/offline-indexes.js"></script></head>', 1)
                    files[name] = s.encode()
    for name in EXACT:
        assert files[name] == (DOCS / name).read_bytes(), 'Sensitive tool changed: ' + name
    files['package-manifest.json'] = (json.dumps({'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False, 'files': manifest_files(files)}, indent=2) + '\n').encode()
    files['SHA256SUMS.txt'] = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(files.items())).encode()
    archive = FULL if full else TOOLS
    with zipfile.ZipFile(OUT / archive, 'w') as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('plebum-offline/' + name, (2026, 11, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    return {'name': archive, 'sha256': digest((OUT / archive).read_bytes()), 'size': (OUT / archive).stat().st_size, 'files': manifest_files(files)}


def main():
    if any((OUT / name).exists() for name in (FULL, TOOLS)):
        raise SystemExit("Release files already exist. Choose a new release ID; never overwrite a published package.")
    from build_tool_fingerprints import build as update_fingerprints
    update_fingerprints()
    from reconcile_tool_downloads import build as reconcile
    reconcile()
    OUT.mkdir(parents=True, exist_ok=True)
    update_guides()
    packages = [package(True), package(False)]
    (OUT / 'manifest.json').write_text(json.dumps({'status': 'PUBLIC_TEST_ONLY', 'custody_approved': False, 'packages': packages}, indent=2) + '\n')
    (OUT / 'SHA256SUMS.txt').write_text(''.join(f'{p["sha256"]}  {p["name"]}\n' for p in packages) + f'{digest((OUT / "manifest.json").read_bytes())}  manifest.json\n')
    with zipfile.ZipFile(OUT / FULL) as z:
        (OUT / 'README.txt').write_bytes(z.read('plebum-offline/README.txt'))
    for p in packages:
        print(p['name'], p['size'], 'bytes;', len(p['files']), 'files;', p['sha256'])
    from build_download_verifier import build
    build()


if __name__ == '__main__':
    main()
