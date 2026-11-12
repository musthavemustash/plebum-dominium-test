# Current public-test tool fingerprints

Public test data only. These fingerprints identify files; they do not approve
real-wallet use or independently authenticate the publisher.

Use verify-file.html to check an individual file. Use verify-download.html,
saved separately before disconnecting, to check a complete or tools-only ZIP.
After extraction, run verify_package.py from the plebum-offline folder.
For the preserved R4 test subset, use public-tests/TESTING.txt and its verifier.

The HTML tools and verify-file.html are at the site or package root. Python
tools, the wordlist, this file and hash_checker.html are in kit/.
These tool copies have the same bytes online and in the current offline ZIPs.

## File identities

```
File:     dice-converter.html
Size:     46387 bytes
SHA-256:  4f6949247291a95a37a1475b40f61e23de99f665fd0e3a5b9cd526b10e01e69c
```

```
File:     descriptor-tool.html
Size:     420868 bytes
SHA-256:  16efdc386a226849263529ca1660e32950bd95e87dfa2adb235162f653b6d0a0
```

```
File:     diceware-mapper.html
Size:     93464 bytes
SHA-256:  bbe8d349575e7f2d3ddd4caf0ffc7934d72b240c3b8858638a2ce4c198317aba
```

```
File:     fingerprint-checker.html
Size:     9833 bytes
SHA-256:  ae9488685d64b89be7631c5ab3332b281e39dcaa23fe689c193bb70646e89f18
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
Size:     8748 bytes
SHA-256:  7bd3db64d114a7e1dffd902ba535111cb60c81d9bdb9db22eb454b36a287de2f
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
