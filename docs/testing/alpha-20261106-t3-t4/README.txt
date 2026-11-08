PLEBUM DOMINIUM — PUBLIC ALPHA TEST RELEASE
Release: alpha-20261106-t3-t4
Source: b49bc994223f7085c1a539133a10f9669725d0f7

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
   Do not bypass their safeguards if your browser reports the wrong state.
4. Record PASS, FAIL or NOT TESTED in RESULTS.csv. Submit non-sensitive results
   through the form after finishing the offline session: https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform

Python dice conversion needs Python 3. The Python map tool also needs GnuPG.
This package does not include Tails, a wallet application, or a full guide.
No installation or dependency download is performed by the package checker.

The packaged tools and public fixtures are byte-for-byte copies of the source
paths recorded in SOURCE.json. No cryptographic implementation was changed.
Browser/OS isolation, physical Tails operation and recovery remain unverified.
Older ZIPs and kit/VERIFY.md do not describe this alpha. Use this package's hashes.
Hashes detect changed bytes; they do not independently authenticate the publisher
or establish that a tool is safe. This alpha does not approve a stable release.
