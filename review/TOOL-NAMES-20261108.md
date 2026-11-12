# Tool names: PR #46 reconciled November 12, 2026

The Windows R4 run exposed two mismatches: the checker called the Diceware mapper “Passphrase mapper” and the Wallet-map tool “Descriptor tool”. This revision brings #46 onto current staging without restoring its obsolete download instructions or historical templates.

| Display name | Stable filename | Purpose |
| --- | --- | --- |
| Dice converter | dice-converter.html | 24-word seed from dice |
| Wallet-map tool | descriptor-tool.html | Encrypt and restore the wallet map |
| Diceware mapper | diceware-mapper.html | Six-word passphrase from dice |
| Fingerprint checker | fingerprint-checker.html | Compare file fingerprints |

Names agree in browser titles, headings, startup dialogs, checker choices, downloads, demos, guide references, START.html and public-tests. Filenames and URLs stay unchanged. Demo pages are explicitly labelled as demos.

## Package revision

New focused package: alpha-20261112-r1. New complete and tools-only packages: offline-20261112-r2. Their current tools and public-tests copies agree byte-for-byte. All prior versioned ZIPs, manifests and physical-test evidence remain untouched.

The four HTML files have new fingerprints. Their executable scripts match R4 exactly, with only the checker's expected fingerprint values normalized for comparison. Python files, wordlist and fixtures retain R4 bytes. The explicit reviewed file identities are recorded in TOOL_NAMES_20261112.json; the release validator checks them and rejects code changes, obsolete copies and stale fingerprints.

## Validation and remaining scope

Passed: current three-package SHA-256 catalogs (21/21 verifier checks), both root/subset verifiers, deterministic rebuilds, stale-copy rejection, independent R4 executable-code comparison and a negative case that tries to change code while updating its reviewed hash; all tool-state/network, 7,776 Diceware mapping, fingerprint, eight BIP39 vector and GPG/HTML interoperability checks; 112-page links, routes and page-test provenance. Static checks confirm titles, headings, startup dialogs, filenames, START links and identical root/public-tests copies. All pre-existing testing artifacts except the live session guide remain byte-identical.

Visual browser preview could not be completed: local Chromium execution failed on an environment socket restriction, and the cloud browser disallows file:// previews. No mobile/desktop visual certification or physical Windows/Tails result is claimed. A new package needs its own T1 and name/fingerprint checks on Windows and Tails. Historical passes keep their original scope; this change does not complete T5, T6/T7 or beta approval.

External Google Form wording/upload changes remain under issue #26. This PR updates the site's reporting instructions, not the external form. Production remains outside this change.

## Published candidate identities

- `plebum-tools-alpha-20261112-r1.zip`: 294285 bytes; SHA-256 `837bc3a6ea1d301049c3c56c537538021f24a028043d6361f8405341b689d799`.
- `plebum-complete-offline-tester-20261112-r2.zip`: 2934366 bytes; SHA-256 `49584d3df98b791af5452a9f7b11b54aa71376f289aede18b9db7c942fedebe5`.
- `plebum-website-tools-only-20261112-r2.zip`: 1568695 bytes; SHA-256 `7f1f0f9ae8c3b6f31e1c9f325e625c88d8b94e0cefee7259cf3d260a76190f47`.
