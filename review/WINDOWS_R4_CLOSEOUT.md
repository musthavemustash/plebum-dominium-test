# Windows r4 closeout — November 9, 2026

The planned guided Windows short functional retest completed on November 8. The authoritative public scope is [RESULTS.txt](../docs/testing/windows-r4-20261108/RESULTS.txt); [TAILS-NEXT.txt](../docs/testing/windows-r4-20261108/TAILS-NEXT.txt) is the next-session handoff.

## Evidence reconciliation

- Reporting sheet rows 11–14 contain manual entries requested by the tester: T1, mapper, wallet map, then final dice/session checkpoint. No duplicate Form response is needed. Earlier partial statuses remain historical; row 14 is the combined closeout.
- Exact focused package: `plebum-tools-alpha-20261108-t5-r4.zip`, 292617 bytes, SHA-256 `6d5ab946970537b21249555507be65724061fd01d132cc02a1c8cb4b4938aec8`; verifier reported 34 matching files.
- Evidence source: the supplied Drive folder lists 62 files (59 PNGs, three public output files). Restored text opens and includes café. Per-track photograph archives and the original folder are linked privately through the existing report sheet; no raw personal photos are copied into this repository.
- Windows observations cover public-session gates/visible clear/reopen in all three tools, the six mapper examples and invalid-input handling, map saved-file equality/messages/retries/edited-input clearing/controlled truncation, and the HTML zero-bit fixture. USB evidence readability passed a spot-check.
- The focused-package PASS does not certify the larger offline archives, all-interface isolation, memory erasure, unperformed T3/T4 cases, Tails r4, beta, or production. Exact software versions were not newly captured. Previous Tails candidate evidence retains its original identity.

## Material updated

Downloads, current testing/stage/beta status, live instructions and assisted-reporting guidance now point to this bounded result and Tails next step. Historical candidate tables and versioned package contents are preserved. Existing ZIPs contain their original instructions; the new live notes are an explicit separate addendum.

The previous Pages workflow regenerated versioned r4 ZIPs on every documentation push. That would silently change the tested archive behind the same URL. It now validates and deploys the committed snapshots without rebuilding or committing packages. New releases must use new versioned paths, assemble all manifests/references together and pass package validation before publication. All existing validation commands remain. The separate naming-cleanup PR is not included.

## Remaining work

1. Physical Tails short changed-behavior retest using unchanged r4 bytes; retain older vectors/interoperability/reboot results with their original candidate.
2. Review acceptance of the documented OS-managed public-session procedure; legacy automatic connected/reconnect checks are not passed by acknowledgments.
3. Reconcile unperformed broader tool/package checks against exact supported releases and environments.
4. Complete both wallet setup, offline-software signing and recovery rehearsals, checked metal backups and inheritance. Hardware signers remain optional after checked metal backups.
5. Reconcile printable materials and final release packaging; independent beta review and explicit release-specific production approval remain required.

## Validation

Passed: static-site build (112 pages), both guide routes, page-test panels, complete/tools-only offline archive checks, download verifier (21 cases), public-session state, network matrix, all 7,776 mapper entries, fingerprint checks, eight BIP39 vectors and HTML/Python map interoperability. Existing package, manifest, checksum and sensitive tool bytes match the base commit. Browser layout review covers the updated status sections; these automated and preview checks are not physical Tails evidence.
