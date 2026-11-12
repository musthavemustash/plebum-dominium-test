# Tool release status — November 4, 2026

**Current status — November 9, 2026:** the focused r4 Windows short retest is complete, and the observed November 9 physical Tails checks passed on the complete r4 archive. Evidence reconciliation, T5 acceptance review, broader unperformed checks and beta work remain open. See [Tails r4 results](TAILS_R4_RESULTS.md) and [Windows r4 closeout](WINDOWS_R4_CLOSEOUT.md). Earlier statements below retain their historical candidate scope.

**November 5 update:** a separate [public testing alpha](PUBLIC_ALPHA_2026-11-05.md) is now available on staging. The blocked/withheld statements below describe the stable custody release and historical internal candidate; they do not prohibit the approved public-fixture alpha. Actual browser/Tails and recovery validation remain incomplete.

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

## November 4 — Electrum upload authenticated

User supplied Electrum 4.8.3 AppImage and detached signature. GPG verification returned exit 0 and five VALIDSIG results against keys retrieved through links on https://electrum.org/ . File: 93845696 bytes, SHA-256 `aabe3bb2c99ffca172a004b0fd6f4afdf1b204079f7691b65f23bc5b63a9de0c`. This differs from the old carried-over pin, which is now corrected. No AppImage execution. Public keys, detached signature and status/import receipts are in review/provenance/electrum/; binary is not committed. No ultimate trust assigned. Key provenance is publisher HTTPS; ThomasV and SomberNight fingerprints also match the complete values printed on the official site.

Valid signing fingerprints (primary fingerprint for Emzy additionally recorded in receipt):
- Emzy signing subkey: 637DB1E23370F84AFF88CCE03152347D07DA627C; primary 9EDAFF80E080659604F4A76B2EBB056FD847F8A7.
- Felix B.: AA0BC6824B397BBA99776E157ED8D82B37192688.
- SomberNight: 0EEDCFD5CAFB459067349B23CA9EEEC43DF911DC.
- Sebastian van Staa: 33C103B4B2794170546CCF7BCFB2C83C66CD792A.
- ThomasV: 6694D8DE7BE8EE5631BED9502BD5824B7F9470E6.

Key URLs: https://raw.githubusercontent.com/spesmilo/electrum/master/pubkeys/ with filenames ThomasV.asc, sombernight_releasekey.asc, Emzy.asc, felixb_f321x.asc and svanstaa.asc, each linked by the official site. Signature dates October 24, 2026. Import agent-start diagnostics did not prevent public key imports or signature verification.

This supersedes the Electrum HTTP403 blocker above. Step one's identified provenance checks are complete at their documented scope (Sparrow remains a signed-manifest pin check, not archive execution). Candidate builder now retains only actual browser/target-offline testing as a release blocker. Tool release remains withheld; ZIP/manifest/verifier not published.
