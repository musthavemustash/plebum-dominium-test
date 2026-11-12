# Current public-test tool fingerprints

Public test data only. These fingerprints identify files; they do not approve
real-wallet use or independently authenticate the publisher.

Use verify-file.html to check an individual file. Use verify-download.html,
saved separately before disconnecting, to check a complete or tools-only ZIP.
After extraction, run verify_package.py from the plebum-offline folder.
For the current test subset, use public-tests/TESTING.txt and its verifier.

The HTML tools and verify-file.html are at the site or package root. Python
tools, the wordlist, this file and hash_checker.html are in kit/.
These tool copies have the same bytes online and in the current offline ZIPs.

## File identities

```
File:     dice-converter.html
Size:     46527 bytes
SHA-256:  f35fe817d19d67a599eb90c3ae271dd2363388efc66eaf77079fce5bd0a706dd
```

```
File:     descriptor-tool.html
Size:     421013 bytes
SHA-256:  3682e91c37fba4f95293971acb8d7b697077f534e2e008419cda24ecc475a941
```

```
File:     diceware-mapper.html
Size:     93596 bytes
SHA-256:  ae33ab800911ea26d512e4f92f1f1c9126fe995e6b07af4249d58945cf00d156
```

```
File:     fingerprint-checker.html
Size:     9986 bytes
SHA-256:  9b4f8e54de58247cafcc5f7ee70c26b249183d1ef7712b9171921f139e95bd22
```

```
File:     bip39_dice_converter.py
Size:     38169 bytes
SHA-256:  177b4b3554d7f7b5357e0f5389a3adf3e3e47daf2e0bcd44a338e56e7c72dd8d
```

```
File:     descriptor_obfuscator.py
Size:     5396 bytes
SHA-256:  deaf9a4277e775c961bbb577669ec99040d15e143c1f2838278d33c38ebbfa4a
```

```
File:     eff_large_wordlist.txt
Size:     108800 bytes
SHA-256:  addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e
```

```
File:     hash_checker.html
Size:     4747 bytes
SHA-256:  0e32bb36a531b02072c9d982697210554455e5c4955486629ea332106f68a816
```

```
File:     verify-file.html
Size:     8775 bytes
SHA-256:  7c4c04e50b50f931860dabb638152438b6e4a0019e293ca200ec556dd3721e03
```

## Check on your computer

Linux / macOS / Tails, from the file's folder:

```bash
sha256sum descriptor_obfuscator.py
```

Windows PowerShell, from the file's folder:

```powershell
Get-FileHash .\descriptor_obfuscator.py -Algorithm SHA256
```

Compare every character. Stop if the file differs. The Python wallet-map
tool also requires GnuPG, installed separately before disconnecting.

## Historical files

tools-bundle.zip, older PDFs, slides and the recovery worksheet are legacy
assets. They are excluded from the current offline ZIPs and this manifest.
Use the current HTML guide; PDF reconciliation and print review remain open.
Historical versioned ZIPs retain their own checksums and test results.
