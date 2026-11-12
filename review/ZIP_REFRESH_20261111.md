# November 11 public-test ZIP refresh

Scope: test site only. Production and all previously published archives remain unchanged.

New packages:
- `offline-20261111-r1`: complete offline guide and website-tools-only archives.
- `alpha-20261111-r1`: focused public tools, fixtures and refreshed instructions.

The complete package includes the current homepage, both guide paths, offline search,
and the recorded Windows/Tails result addenda. Legacy print files and the withdrawn
`kit/tools-bundle.zip` are excluded. All seven tested HTML/Python/wordlist files are
byte-identical to the original r4 focused package, including both package roots and
`public-tests`. Earlier Windows/Tails evidence keeps its original package identity.
This release has no new physical Windows/Tails test result and does not approve beta.

The individual-file verifier and `docs/kit/VERIFY.md` now derive fingerprints and sizes
from the actual shipped tools. The three-tool checker remains byte-identical to r4.
CI rejects reference drift. The ZIP verifier is generated from the final archives and
saved separately, avoiding a circular archive hash. Historical ZIP verifier entries
remain available. Packagers refuse to overwrite an existing release directory.

Validation completed locally:
- 112 static HTML pages, both independent paths, all offline link targets.
- 219 complete-package and 95 tools-only file checks, plus each 34-file public subset.
- Every packaged public subset byte matches the focused archive.
- All three archives rebuild byte-for-byte deterministically.
- Recorded focused SOURCE.json file identities match Git commit
  `c2eb562cd5c55bb76a4ae646ffccfc5505f153ba`.
- 21 ZIP-verifier cases, including real archive bytes, mutation rejection, read failures,
  invalid catalogs and late-result cancellation.
- Fingerprint checker, 7,776 EFF mappings, public-session and network-control regressions.
- Eight BIP39 vectors, Python/HTML encryption interoperability, Unicode preservation,
  wrong-password, truncation and corruption rejection.
- Mutating a tool causes the new verification-drift check to fail.

Final archive SHA-256 values:

| Archive | SHA-256 |
| --- | --- |
| plebum-complete-offline-tester-20261111-r1.zip | ec78211598638b1975c0e8a97bd73318cdf47515e00866ab516c05403902a974 |
| plebum-website-tools-only-20261111-r1.zip | 976cee7dadf14d3529ccf5623f2c2520989d1bdc5bacc852b1fab7df16fda49d |
| plebum-tools-alpha-20261111-r1.zip | 3a61e6533ba1d963b67463b1d99669dcb21de11406dad9ab4958789eec5dd8b0 |

Rollback: revert the staging refresh PR to restore the r4 download entry points.
Do not rewrite r4 or any other historical archive; retain recorded checksums and evidence.
