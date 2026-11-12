PLEBUM DOMINIUM — OFFLINE PUBLIC TESTER — 2026-11-12 r2
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
