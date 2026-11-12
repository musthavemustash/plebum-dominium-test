# Staging currency review: November 12, 2026

Scope: the public staging site and the current offline testing packages. Production remains outside this change.

## Findings and corrections

- All 112 live HTML pages matched staging commit `1a61d9af4761c0ba065163c70ea1032e6231b18c` at the start of the sweep.
- Corrected the Downloads labels that still called the reconciled file verifier and `VERIFY.md` obsolete.
- Removed 19 dead table-of-contents anchors from retired route pages and repaired three links to the removed homepage introduction anchor. The validator now checks local section targets as well as files.
- Retired pages now ask testers to check their onward links instead of controls and content those pages no longer contain.
- Replaced obsolete test-site notes and kit README instructions that described a third active path, blocked off-path pages, and withdrawn print documents.
- Applied the accepted T6.7 finish step: review and save results, record unfinished work, and close the offline session. Another reader and an extra finishing screenshot are not required for T6. T7 retains its separately listed handover check. Metal remains outside both tests.
- Added exact-package evidence guidance and an explicit current-package status. Historical Windows/Tails results retain their original dates, files and scope.
- Updated the Chainalysis story and sitewide ticker to its November 10 restoration update. Refreshed affected footer dates, search content and page-test source provenance.
- Separated publisher-current software versions from previously reviewed/tested versions. No newer upstream binary is represented as authenticated or physically tested by this sweep.

## Source checks

Checked November 12, 2026:

| Software | Recorded version | Current publisher release | Source |
|---|---|---|---|
| Tails | 7.16 | 7.17 | https://blog.torproject.org/new-release-tails-7_17/ |
| Sparrow | 2.5.5 | 2.5.6 | https://sparrowwallet.com/download/ |
| Electrum | 4.8.3 | 4.8.4 | https://electrum.org/ |

Chainalysis: https://www.chainalysis.com/blog/security-incident-october-30/ now includes the November 10 Data Solutions restoration. The previously cited Binance and Mercado Bitcoin primary reports remain available at their recorded scope. This sweep is not an exhaustive independent investigation of every historical news claim.

## New immutable testing release

`offline-20261112-r1` packages the corrected guide. The seven R4 tool/wordlist files and all 35 `public-tests` files remain byte-identical to R4. All 85 previously tracked testing artifacts are unchanged.

| Archive | Bytes | SHA-256 |
|---|---:|---|
| plebum-complete-offline-tester-20261112-r1.zip | 2621132 | `7665d903895994abbfe4f287e0b5aa9d264c5786daed45b7b78dcb2d5fac4c3a` |
| plebum-website-tools-only-20261112-r1.zip | 1566661 | `92cdc8b249457a2c878394f1eb78fcc12704875e3d82f977d3691853e848490c` |

The publisher rejects an existing output version instead of overwriting it. Verifier tests now follow the current download links instead of a hard-coded release date.

## Validation

- Site validator: 112 HTML pages, local files and section anchors, and generated route freshness.
- Path checks: 28 numbered pages, two overviews, forward/back navigation and route state.
- Page-test checks: canonical panels, generated routes, public reporting URLs and packaged copies.
- Package checks: root verification passes for 216 complete-package files and 95 tools-only files; local links, embedded search, absent network subresources, exact R4 copies, reconciled file identities and excluded legacy assets.
- Deterministic package builds and rejection of obsolete tools, stale snapshots and altered checker identities.
- ZIP verifier: 21/21 checks, including actual current archive bytes, negative cases and asynchronous cancellation.
- Existing public-session, network-state, Diceware mapping and fingerprint-checker tests pass.
- Core public fixtures: eight BIP39 vectors, invalid inputs, GPG/OpenPGP.js interoperability, Unicode and decryption rejection cases pass.
- News ticker: 82 instances, valid destinations, duplicate accessibility behavior and offline price-request suppression pass.

These are source, package and automated checks, not a new physical Windows/Tails run or a visual browser certification. The new ZIPs require their own physical test evidence. T1–T5 evidence reconciliation, T6/T7 completion, PDF reconciliation/print review and final beta release review remain open. No beta or production approval is implied.
