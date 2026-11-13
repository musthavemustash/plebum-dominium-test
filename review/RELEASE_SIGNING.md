# Release signing preparation

Status: **unsigned**. No author key or signature has been created or claimed.
The prepared manifest covers the three immutable 20261113-r2 ZIPs and nineteen
standalone tool/helper files. It does not sign this PR's live guide edits.
Those edits will be incorporated into a separately identified future package.
Signing r2 would authenticate its existing bytes, including its documented
instruction correction; it would not retroactively fix the archive or approve beta.

## Prepare the exact release

1. Finish review and the required physical tests for the release being signed.
2. Freeze its filenames and bytes. For a new version, make a new dated directory
   under `review/`, with `files.json` listing every intended ZIP and standalone
   executable/helper relative to `docs/`. Include verifier and wordlist files.
3. Generate a new list (creation refuses to overwrite an existing manifest):

   ```sh
   python3 scripts/release_checksums.py create --plan review/NEW-RELEASE/files.json --manifest review/NEW-RELEASE/SHA256SUMS
   python3 scripts/release_checksums.py check --plan review/NEW-RELEASE/files.json --manifest review/NEW-RELEASE/SHA256SUMS
   ```

For the prepared r2 inventory, run `python3 scripts/release_checksums.py check`.
This verifies coverage and file bytes, **not an OpenPGP signature**. Review the
inventory itself: an omitted intended artifact cannot be authenticated by it.
Recalculate the hashes on the owner's trusted signing computer from the actual
files before signing. Transfer public release material only to that computer.

## Owner-held signing key

Use an owner-controlled offline OpenPGP signing key, with its recovery/revocation
material kept privately. If there is no suitable key yet, choose and establish
one locally with the owner before continuing. Never create or upload the real
private key, its passphrase or recovery material in CI, this repository or chat.

On the owner's signing computer, substitute the independently recorded FULL
primary fingerprint for `YOUR_FULL_PRIMARY_FINGERPRINT` below. GnuPG selects
the usable signing key/subkey belonging to it. Review the selected identity.

```sh
gpg --fingerprint YOUR_FULL_PRIMARY_FINGERPRINT
gpg --armor --detach-sign --local-user YOUR_FULL_PRIMARY_FINGERPRINT --output SHA256SUMS.asc SHA256SUMS
gpg --armor --export YOUR_FULL_PRIMARY_FINGERPRINT > plebum-release-key.asc
gpg --verify SHA256SUMS.asc SHA256SUMS
```

Keep the private key offline. Return only the public key, full primary
fingerprint, detached signature and signed checksum file. Publish the full
fingerprint through a separate, already trusted channel such as the author's
established social account. A newly linked profile does not by itself establish
trust. Document key rollover/revocation through those channels if needed.

## Verify before publication

1. On a clean verification machine, inspect `gpg --show-keys --with-fingerprint
   plebum-release-key.asc`. Independently confirm the full primary fingerprint.
2. Import only the public key and run `gpg --verify SHA256SUMS.asc SHA256SUMS`.
   Check that the signing key/subkey belongs to the independently checked primary
   key. Reject nonzero exit status, unexpected identity, bad/expired/revoked
   signatures or unresolved validity warnings. An unknown ownertrust warning is
   not an identity check; the independent fingerprint comparison remains required.
3. Recheck every listed file using the reviewed release plan. On Linux, from the
   `docs/` file tree, `sha256sum --check /path/to/SHA256SUMS` must verify every line.
   Do not ignore missing entries in a full release review. Individual downloaders
   compare the exact filename/hash for the file they downloaded.
4. Save the signature verification output and full primary fingerprint with the
   review. Publish the exact checksum file, detached signature and public key
   together in a new versioned release directory. Re-fetch the public artifacts
   and repeat signature and hash verification before claiming it is signed.
5. Update Downloads and the reader signing note with the real links/fingerprint.
   Keep old release bytes and signatures unchanged. Production release still
   needs its separate approval; signing is not beta acceptance.

Reference workflow: https://bitcoincore.org/en/download/
