# Public testing release — November 5, 2026

The maintainer approved making the tools available for public testing. This authorizes a staging alpha, not real-wallet use or promotion to production.

Release: `alpha-20261105-7240f0d`. Canonical tool/fixture source: staging commit `7240f0def1fe1b06ba4c60bde423f96fd80ee2b0`. The complete local snapshot was checked against all 450 Git blobs in that source tree before assembly.

## Published scope

- Versioned ZIP under `docs/testing/alpha-20261105-7240f0d/`, containing the unchanged HTML/Python dice and map tools, EFF wordlist, public fixtures, expected results, results CSV, package checker and source manifest.
- Matching external archive/file manifest and SHA256SUMS; internal file checksums and readme.
- Downloads now says “Available for testing,” links directly to the ZIP and instructions, and distinguishes the alpha from the older kit and its manifest.
- Testing instructions use the existing feedback form. No messages sent and no form changes.
- Production, cryptographic implementations, original standalone tools, legacy bundles/manifests, and stable release gates are unchanged.

## Verification

- Rebuilding with the same source produces identical output bytes.
- Every archive member matches the external file manifest; canonical files match source byte-for-byte.
- Extracted package checker passes all 19 listed files; modified and missing tool files are rejected.
- Eight published BIP39 vectors pass in Python/JavaScript; wordlists, face mapping, checksum rejection, excess input and invalid input checks pass.
- Python/GPG and embedded OpenPGP.js cross-decryption, Unicode, wrong passwords, truncation and damaged ciphertext checks pass.
- 40 protocol/network-state combinations and asynchronous UI-state regressions pass in the existing test harness.
- Local references across all 96 site HTML pages resolve. Browser preview confirms the new download and instruction pages render and the instruction link navigates correctly.

## Existing validation failures and remaining work

`scripts/build.py` and `scripts/test_paths.py` still report pre-existing generator drift. Compared validation before and after this change: the exact same six differences remain in `paths/one/terms.html`, `paths/three/terms.html`, `paths/three/sparrow.html`, `paths/three/titanium.html`, and both route search indexes. Regeneration would remove the live quorum demo and recovery explanations; those pages were intentionally preserved. These full-site checks are not reported as passing.

Download-page browser preview is not offline tool validation. Actual browser/OS isolation, mobile tool behavior, physical Tails use and recovery validation remain incomplete. Public test data only. No stable/custody release approval is implied.

The older internal candidate builder remains available for its prior review workflow. This public alpha has separate packaging and manifests; it does not replace or relabel the legacy artifacts as verified.
