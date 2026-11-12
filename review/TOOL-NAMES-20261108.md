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

Run existing package, fingerprint, tool-state, mapper, core interoperability, link, route and page-test checks. Preview titles, headings, startup dialogs, checker labels and hash matches at desktop and mobile widths. A new package needs its own T1 and name/fingerprint checks on Windows and Tails. Historical passes keep their original scope; this change does not complete T5, T6/T7 or beta approval.

External Google Form wording/upload changes remain under issue #26. This PR updates the site's reporting instructions, not the external form. Production remains outside this change.
