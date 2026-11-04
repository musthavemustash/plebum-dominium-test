# Tool release status — November 4, 2026

Baseline: c0a8e5a0964962218b5360986d339c204c23e1b5 (PR #17); Pages run 41917775493 succeeded. No open PRs at this batch's start. This report supersedes earlier pending Ian Coleman/Tails provenance entries; it does not approve a custody release.

| Step | Current status |
|---|---|
| 1. Authenticate upstream files | Partial: OpenPGP package identity, Sparrow signed manifest, both Tails images and Ian Coleman 0.5.6 verified. Electrum remains blocked. |
| 2. Offline/password controls | Implemented in PR #17; network-state and asynchronous UI regression tests pass. Actual browser/OS validation outstanding. |
| 3. Correct misleading messages | Implemented SHA-512, backup retention and excess-input corrections in PR #17. This batch replaces instructions to wipe the entire drive after a hash mismatch with stopping use of the mismatched file and preserving backups. |
| 4. Regression and offline tests | Automated core, UI-state, routing and source checks pass. Actual browser/mobile/Tails tests remain unperformed after the earlier browser policy block. |
| 5. Consistent packaging | Repeatable internal candidate assembled and checked. Published ZIP/manifest/verifier unchanged; downloads remain withheld until gates pass. |

## Ian Coleman 0.5.6

The official homepage https://iancoleman.io/ links the project https://github.com/iancoleman/bip39 and public key https://iancoleman.io/pubkey.txt . Retrieved these release assets:

- https://github.com/iancoleman/bip39/releases/download/0.5.6/bip39-standalone.html
- https://github.com/iancoleman/bip39/releases/download/0.5.6/signature.txt.asc

Downloaded HTML: 4555966 bytes; SHA-256 `129b03505824879b8a4429576e3de6951c8599644c1afcaae80840f79237695a`, matching the clear-signed release checksum. GPG verification exited 0, GOODSIG/VALIDSIG fingerprint `5AD5C88083708E93A2966FF49FF1B58CA7B9E6A5`. Signature dated August 1, 2023. Public key, signed checksum and verification status are preserved under `review/provenance/ian-*`. The isolated key import reported an agent-start error, but imported the public key and signature verification succeeded. No ultimate trust was assigned; key provenance is publisher HTTPS, not a separate personal trust path. Updated the Python verifier pin to these authenticated bytes. This does not certify browser operation or complete custody use of the upstream tool.

## Electrum remains blocked

Official AppImage and signature requests still returned HTTP 403:

- https://download.electrum.org/4.8.3/electrum-4.8.3-x86_64.AppImage
- https://download.electrum.org/4.8.3/electrum-4.8.3-x86_64.AppImage.asc

No artifact was obtained, no signature verified, and the existing hash was not replaced. The official version page cannot authenticate file bytes. To close this gate, obtain these two exact files through the official download flow on a machine with access (or supply those public files for review), verify against the publisher-linked signer keys with full fingerprint evidence, then hash the authenticated AppImage. Do not substitute a mirror solely to make this check pass.

## Candidate assembly and validation

`python3 scripts/prepare_tool_candidate.py /tmp/plebum-reviewed-candidate` builds an internal candidate outside the repository. It copies the canonical standalone files, builds a ZIP with fixed ordering/timestamps/permissions, derives verifier pins and a manifest from the same bytes, and checks bundled/standalone equality. The verifier is outside the ZIP to avoid a circular dependency between its bundle pin and ZIP hash. The manifest includes the generated verifier. Candidate warning and unresolved gates are included. There is no publication option; outputs inside the repository are rejected. No historical root files are used.

`python3 scripts/test_tool_packaging.py` passed: two builds byte-identical; altered standalone file rejected; repository output rejected. This is consistency evidence, not authentication of Electrum or approval to release. Rebuild after any further tool changes and repeat checks before eventually replacing the published artifacts together.

Other passing checks on this batch:

- `python3 scripts/test_tool_core.py`: eight public BIP39 vectors, wordlist/mapping/checksum checks, excess and invalid inputs, GPG/OpenPGP.js cross-decryption, Unicode, wrong-password and damaged-message rejection.
- `node scripts/test_tool_network.cjs`: 40 protocol/network-state cases.
- `node scripts/test_tool_ui_state.cjs`: stale result, password cleanup and delayed operation rejection.
- `python3 scripts/build.py`: 95 HTML pages and source/reference checks.
- `python3 scripts/test_paths.py`: 28 numbered steps and two independent route overviews.
- `node scripts/test_entry_interactions.js`: glossary/demo logic.

Node VM/DOM doubles are not a browser. Actual network egress, desktop/mobile interaction, OS offline isolation, Tails boot and recovery workflows remain unverified. Use public fixtures only when closing these gates; no real secrets. Published download warning must remain until these checks and Electrum authentication are complete. PDFs are still a separate unfinished task.
