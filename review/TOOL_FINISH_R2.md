# Tool closure candidate — November 8, 2026, r2

Public-fixture candidate only. Production and beta designation are unchanged.

## Changes

- Diceware mapper: removed captured static rows that duplicated the six live rows;
  repaired invalid-input stale words and copy state; reject malformed/overflow
  paste as a whole; guard incomplete copy and late clipboard callbacks. Added
  the same file-only, acknowledged public-test session as the other sensitive
  tools. Downloads reset visible state and acknowledgments. EFF list unchanged.
- Wallet map: clear previous attempt/result/download messages on a new attempt,
  input change or mode switch; discard stale async success and failure callbacks;
  prevent an unreadable replacement file from leaving the old input in use.
  Crypto library, parameters and Python implementation unchanged.
- Individual fingerprint checker: regenerate three built-in hashes from the
  actual source files during packaging; validate hex; snapshot and invalidate
  pending checks so older results cannot overwrite the current selection.
- Package: add mapper, fingerprint checker, short retest, public-session contract
  and deterministic truncation helper to the focused public-tests folder.
  Advance current packages to r2; preserve older releases and evidence.

## Evidence

- Real local crypto core tests: eight published BIP39 vectors, invalid input,
  Python/GPG and embedded OpenPGP.js cross-decryption, Unicode preservation,
  wrong-password, truncated-message and corrupt-payload rejection passed.
- Shipped mapper controller with DOM doubles: all 7,776 EFF entries agree with
  the bundled reference, exactly six rows, invalid input/paste/overflow,
  incomplete copy, stale clipboard callback, clear/lock cases passed.
- Shipped map controller with DOM doubles and mocked crypto: status reset,
  invalid/missing input, late success/failure, FileReader clearing and lock passed.
- Three session controllers: 20 protocol/flag combinations each, acknowledgments,
  readiness, observed events and manual locking passed with simulated signals.
- Fingerprint checker: real SHA-256 against all three shipped source files,
  mismatch, malformed hex, stale result/error and cancellation passed.
- Cloud Chrome preview: mapper loaded code and remained locked over HTTP; visual
  gate inspection only. No local-file Windows or Tor/Tails runtime claim.
- Package, download-verifier, site and path checks are run on rebuilt archives.

## Acceptance boundary

See docs/testing/t5-20261108/PUBLIC-SESSION-CONTRACT.txt. The public-test procedure
uses OS-managed isolation, explicit acknowledgment, local-only operation and
visible-state clearing. A browser flag is not an air-gap attestation. Legacy
automatic connected/reconnected detection is not recorded as a pass. Final
beta review must accept the documented operating procedure and limitations.

Earlier physical Tails results remain attached to the exact candidate tested.
Fresh evidence for affected r2 behavior remains pending. Follow
TOOL-FINISH-RETEST.txt on Windows and Tails; do not repeat unchanged known-answer
cases without a regression. Full wallet setup, signing, recovery, backup and
inheritance rehearsals remain separate beta gates.

## r3 download correction

The standalone mapper download previously serialized a cleaned DOM, producing
bytes different from the published source fingerprint. r3 serves the original
blank HTML file through a normal download link instead. Runtime input is never
serialized. The download contract is covered in the mapper regression test.
The r2 package remains historical; use r3 for the focused physical retest.
