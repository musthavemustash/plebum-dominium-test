# Release-signing and rehearsal follow-up

Base: `1d0b3311267ccd78719224ef35117082cb7b2314` (merged PR #71).
Staging-only draft; the owner merges. This does not authorize production or beta.

## Changes

- Prepare a reproducible, unsigned SHA256SUMS inventory for three r2 ZIPs and
  nineteen standalone tools, helpers, verifiers and demos. Add complete-inventory
  checking to CI. Document detached signing, independent full-fingerprint checks,
  owner-held offline private keys and post-publication verification.
- State the current unsigned status plainly on Downloads. Explain that the live
  site uses GoatCounter, Google Fonts and mempool.space while the full offline
  guide strips those remote resources and disables price fetching.
- Label the offline signing and online watch-only roles in T6/T7, test-wallet
  setup and signing/recovery. Prohibit reuse of test seeds, passphrases or dice
  rolls for a real wallet. Keep the text in ordinary HTML, outside disclosures,
  without a JavaScript acknowledgement gate or reliance on colour.
- Add fixed public `wsh(multi(2,...))` and `tr(...,{...})` examples from a pinned
  Bitcoin Core source revision. Validate their eight-character checksums using
  the pinned, MIT-licensed reference helper; test byte-for-byte restoration in
  Python/GPG and OpenPGP.js in both directions, including CRLF export endings.
  No descriptor parsing, checksum rewriting or encryption behavior was changed.

## Immutable packages and evidence

All 142 existing versioned files under the tested package/evidence directories
are byte-identical to the base, including the three r2 ZIPs and the previously
emailed STATUS.txt. The current ZIPs do not contain these new live instructions.
Updated T6/T7 sheets explicitly say to save them beside the verified extraction.
The next separately versioned package can incorporate the changes.

The cumulative `AUDIT_4_LIVE_ADDENDUM_20261113.json` pins the exact complete-r2
scratch-rebuild difference (19 members, including manifests/search indexes).
The published full ZIP stays at
`1fbd6c9d92fdcfdf615db9a5b542b0294814b232775b9e2ce66bf52c785fa706`.
The tools-only rebuild still matches the published ZIP exactly. Unrecorded drift
and any modification to a tested archive continue to fail consistency checks.

## Verification

All 16 CI commands passed locally: the existing 14 staging checks, release
inventory validation (22 files), and negative release-inventory tests. Logs for
the staging checks are in `evidence-signing-followup-20261113/`; the tool-core
and release-check outputs are also recorded in that directory.

The release tests reject changed bytes, omitted/extra/duplicate manifest entries,
missing files, symlink inputs and traversal paths. The established tool-core
suite still rejects wrong passwords, truncated and corrupted encrypted messages.

Browser preview: inspected the three-key signing page at a desktop viewport.
The test-only text, role labels and existing navigation render correctly.
No claim of physical Windows/Tails, full mobile/print, wallet import or wallet
signing compatibility follows from that preview or the descriptor round trips.
T6/T7 and the outstanding release gates remain open.

## Owner action later

No release signing private key or detached signature was created. The manifest
is preparation only; see `RELEASE_SIGNING.md`. Before claiming a signed release,
the owner must authenticate the selected public key through an independent
channel, review/sign the exact checksum list offline and provide only public
verification artifacts. Existing upstream keys cannot sign a Plebum release.
