PLEBUM DOMINIUM — PUBLIC ALPHA TEST RELEASE
Release: alpha-20261113-r1
Source: 19eff35671ac096e2e0197531bd4dd97889bf98a

AVAILABLE FOR TESTING. NOT APPROVED FOR REAL-WALLET USE.
Use the included public fixtures and disposable test data only. Never use real
seed phrases, private keys, entropy, passwords, wallet backups or funds.
This restriction also applies to any older custody instructions inside the tools.

1. Extract the entire ZIP. Open the extracted plebum-public-test folder.
   Tools, TESTING.txt and the fixtures folder are directly inside it.
   If using the complete offline or website-tools ZIP, open plebum-offline,
   then public-tests instead. Its fixtures are in public-tests/fixtures/.
   Do not launch tools inside the compressed archive.
2. Open a terminal in that test folder and read TESTING.txt. All commands
   and paths such as fixtures/public-map.txt start from that folder.
   Check this test subset with: python3 verify_package.py
   On Windows with Python installed, use: py verify_package.py
3. Open the HTML tools as local files on a disconnected test machine.
   HTTP/HTTPS and localhost are deliberately blocked by the sensitive tools.
   Complete the OS checks before the public-test acknowledgments. A stable
   browser flag of true may occur in isolated Tails. It is not proof either way.
   Keep networking disabled; Lock and clear before changing network settings.
4. Create a results folder. Copy RESULTS.csv and SESSION-NOTES.txt there before
   editing them; keep packaged originals intact. Save screenshots after each
   result, before clearing. Follow EVIDENCE-CHECKLIST.txt to copy and reopen
   evidence on the separate data USB before reboot, shutdown or a pause.
5. After the offline session is closed, read FORM-REPORTING.txt. It maps T1-T5
   to the live Google Form and explains uploading a public-only evidence folder
   and sharing a working viewer link. Submit your actual results: https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform

Python dice conversion needs Python 3. The Python map tool also needs GnuPG.
This package does not include Tails, a wallet application, or a full guide.
No installation or dependency download is performed by the package checker.

The packaged tools and public fixtures are byte-for-byte copies of the source
paths recorded in SOURCE.json. No cryptographic implementation was changed.
Earlier candidate Tails results are in TAILS-RETEST-RESULTS.txt.
This revision fixes stale Dice converter validation after an input change.
The checksum/word derivation algorithm is unchanged. Browser-controller
regressions use public fixtures and DOM doubles; they are not physical Tails
or Windows evidence. Repeat the affected checks on this exact new candidate.
The other sensitive tools, Python helpers, wordlist and fixtures are unchanged.
Historical Windows/Tails results retain their original scope. Check this ZIP
with T1 and repeat the name/fingerprint checks; no new physical pass is claimed.
Browser isolation is not certified by this package. See PUBLIC-SESSION-CONTRACT.txt
for the public-test boundary and TOOL-FINISH-RETEST.txt for the remaining checks.
Complete wallet recovery remains unresolved.
Older ZIPs do not describe this alpha. Use this package's hashes.
Hashes detect changed bytes; they do not independently authenticate the publisher
or establish that a tool is safe. This alpha does not approve a stable release.
