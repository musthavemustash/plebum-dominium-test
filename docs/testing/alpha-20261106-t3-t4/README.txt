PLEBUM DOMINIUM — PUBLIC ALPHA TEST RELEASE
Release: alpha-20261106-t3-t4
Source: a8558e51eb0908af5b2422f2c65e817ae4f67bdf

AVAILABLE FOR TESTING. NOT APPROVED FOR REAL-WALLET USE.
Use the included public fixtures and disposable test data only. Never use real
seed phrases, private keys, entropy, passwords, wallet backups or funds.
This restriction also applies to any older custody instructions inside the tools.

1. Extract the entire ZIP. Do not launch tools inside the compressed archive.
2. Read TESTING.txt. Check the files with: python3 verify_package.py
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
