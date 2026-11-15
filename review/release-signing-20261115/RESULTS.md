# Signed release follow-up validation — November 15, 2026

The returned public `manifest.txt.asc` verifies against the exact 322-byte candidate manifest and the established release fingerprint `B9286C4A7CFF722E191D2D7566FB7D9AB51E417E`. All three referenced ZIPs match. The uploaded signature was copied byte for byte (SHA-256 `d39ade753b88eff3eeb151f7dc3318d13e82fad57f034947ff752f72e98bb555`).

No existing ZIP, candidate manifest, candidate build identity, previous release signature, or tool implementation was changed. Release status and later live instructions are separate from the immutable signed snapshots. The exact live-source differences are pinned in `review/SIGNED_RELEASE_LIVE_ADDENDUM_20261115.json`; this inventory does not authorize repackaging.

All 18 validation commands in `.github/workflows/offline-downloads.yml` passed locally:

- Tool reconciliation and download consistency, including deterministic scratch builds and rejection of unrecorded source drift.
- All 32 browser-verifier regressions, including real new-release ZIPs, invalid signatures, modified manifests, wrong keys and whitespace changes. The manifest-tamper fixture now changes the first digest character instead of relying on an r2-specific substring.
- Independent GnuPG validation of both r2 and r1 signatures, all six ZIP hashes and vendored verifier hashes, with automatic key lookup disabled.
- Public-session, network, dice, search-focus, Diceware mapper, fingerprint-checker and tool-core regressions.
- Release inventory and mutation checks; site build, path, page-test module, offline-download and Tails-helper checks.

After correcting the final old-package label, download consistency, static build, page-test modules and `git diff --check` were rerun and passed. The static build validated 113 pages without rewriting files.

Physical results and their limits are in `docs/testing/tails-helper-20261115/RESULTS.txt`. They derive from chat photo review and tester confirmations, not a separately uploaded native PNG inventory. They cover helper/navigation and fresh-boot reopening, not a full T1–T5 or T6/T7 pass. A graphical retest of the updated live homepage was not performed in this build environment.

The staging PR remains for Jake to review and merge. GitHub Actions must also pass on the published commit. No production deployment or beta approval is included.
