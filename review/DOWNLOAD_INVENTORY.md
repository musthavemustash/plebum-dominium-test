# Download inventory evidence — November 4, 2026

Compared against staging main baseline 6c80cea7cdf754c3933fd3add96d8573a2c68783. No binaries, tools or hashes changed. Byte equality does not establish safety.

| File | Published SHA-256 | Actual SHA-256 | Result |
|---|---|---|---|
| tools-bundle.zip | 26223471d58a6f573fa25a3e189b9bc16f5c6b22a21e4b9fcaa58e5e22047945 | 26223471d58a6f573fa25a3e189b9bc16f5c6b22a21e4b9fcaa58e5e22047945 | MATCH |
| bip39_dice_converter.py | 7a14a2044eb90c45114336329e91fcdd9d98362fabdbdeadbc190b4478800330 | fcef80062b6c0a36c47acefda246fab56f9405d9e75033b4479ad7f61799674a | MISMATCH |
| descriptor_obfuscator.py | 35f8807c72241bcbe97318f7ffa4e4c6e211df180e67f85656e0429520466589 | 35f8807c72241bcbe97318f7ffa4e4c6e211df180e67f85656e0429520466589 | MATCH |
| dice-converter.html | 8febaebc3d548527d7158d2df0200aba7b8eaee53379d5bf2e6dd84683d90010 | 4a6e188fa4c65a1ac5b3aabe2cf5911b6cecd9360fa2d935241b352893d3cc6f | MISMATCH |
| descriptor-tool.html | 9b391a911cb5ba3a74a108321c12c37dc82d7a25b3707927958ccc46e9e30e61 | ae25bd656e0566ad7fcf7dfbbfe44b12a4895e9c81f49ff35350216ae2f56f17 | MISMATCH |
| verify-file.html | c875b25e241c259fca9c8c9f1e256e6489f3f03a11271b18c3033ae5d5f21106 | f148c4a6b5c067e12bc2f9cd0caaf60f39df8381cec73b25f77ff459f55fbeff | MISMATCH |
| hash_checker.html | 0e32bb36a531b02072c9d982697210554455e5c4955486629ea332106f68a816 | 0e32bb36a531b02072c9d982697210554455e5c4955486629ea332106f68a816 | MATCH |
| eff_large_wordlist.txt | d5bf5d37df25b50fe6eabf519e59c6cfeb62db627e4d9cfcb275dd7b082e930b | addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e | MISMATCH |
| verify_downloads.py | 8b819c8325cfb61e680de50cd04d37c04ad3c3d2bc3e46425ee732c54971cd45 | 8b819c8325cfb61e680de50cd04d37c04ad3c3d2bc3e46425ee732c54971cd45 | MATCH |

## Bundle comparison

- bip39_dice_converter.py: different bytes or no corresponding standalone file
- descriptor-tool.html: different bytes or no corresponding standalone file
- descriptor_obfuscator.py: same bytes
- dice-converter.html: different bytes or no corresponding standalone file
- eff_large_wordlist.txt: same bytes
- hash_checker.html: same bytes
- README.txt: different bytes or no corresponding standalone file

## Required follow-up

Identify intended audited versions from provenance; compare bundle versus standalone code; run public known-answer vectors and encryption roundtrips; rebuild only from those reviewed sources; then regenerate inventory, verifier expectations and archive together. Do not merely replace mismatched hashes with the observed values. Legacy PDFs/slides/worksheet remain unreviewed.
