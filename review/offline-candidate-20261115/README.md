# November 15 offline candidate and signing handoff

The physical Tails run tested the complete **20261113-r2** archive. Its focused
preflight is closed; T6 wallet setup, signing and recovery and T7 remain
unstarted. See `docs/testing/tails-pre-t6-20261115/RESULTS.txt` for the evidence
scope, failed opening attempts and successful manual folder workaround.

The three **20261115-r1** ZIPs are new, unsigned candidates. This PR leaves
the signed r2 downloads, detached signature, public key and homepage verifier
intact. Candidate links are separate and explicitly unsigned. No merge into
production or beta approval is implied.

## What changed

- Current testing/download status and live run sheets incorporate the scoped
  November 15 results. Historical R3/R4 reports remain historical.
- `OPEN-IN-TAILS.py` grants temporary read access to only its extracted package
  folder using the command that succeeded in the physical run. It prints an
  encoded local file URL; it does not launch tools, serve HTTP, install software
  or change network/browser settings. The helper itself needs physical testing.
- START's inline instructions and the text/folder guides explain the recovery
  even when relative browser resources cannot be loaded. New-boot and file-path
  instructions distinguish ephemeral folder grants and Home extractions.
- New archives include current source, the recent results, reviewed tool bytes,
  helpers and per-file manifests. Out-of-package historical downloads link
  online instead of producing broken relative paths. Missing actual guide/tool
  links still fail the package check.
- The builder preserves existing archives, records a source commit and emits
  the exact unsigned manifest without promoting it into the signed verifier.

## Offline signing: the remaining release step

The handoff ZIP contains all three candidate archives, `manifest.txt`, the
existing public release key and these instructions. Extract it into a new
folder. Check the three archive hashes against `manifest.txt` before signing:

```sh
sha256sum -c manifest.txt
```

On the existing offline release-signing setup, sign the exact supplied bytes:

```sh
gpg --armor --detach-sign --local-user B9286C4A7CFF722E191D2D7566FB7D9AB51E417E --output manifest.txt.asc manifest.txt
gpg --verify manifest.txt.asc manifest.txt
```

Return **only the public `manifest.txt.asc`**. Do not send a private key,
passphrase or revocation certificate. Do not rename archives or edit the
manifest after signing. These commands assume the previously established
signing key; this package neither creates a key nor changes its trust settings.

After that detached signature is returned, verify it against the pinned public
key and exact manifest, publish a new versioned release directory, switch the
three current download links together and rebuild the signed verifier. Validate
all three ZIPs with GnuPG and the browser verifier before promotion. If any ZIP
changes, create a new version/manifest and sign again; never replace these bytes.

## Physical acceptance still required

On Tails with networking disabled: verify the new ZIP and extracted files;
run `python3 OPEN-IN-TAILS.py` from `plebum-offline`; paste its printed address
into Tor Browser. Check styled one-key and three-key pages, next/back links,
local search and a locked public-test tool. Repeat after a fresh Tails boot.
The automated helper, file-link and source checks do not prove this acceptance.
Use the same photo → review → filename → save flow; keep r2 evidence separate.

## Reproducing the candidate

`BUILD.json` records the source commit and exact output identities. From that
source commit, run this into a fresh scratch directory (not a published path):

```sh
python3 -B scripts/prepare_offline_candidate.py --source-commit FULL_SOURCE_COMMIT --output-root NEW_EMPTY_DIRECTORY
```

Run the repository's normal validation plus `python3 -B scripts/test_tails_offline.py`.
The latter checks the committed candidate archives and folder helper without
claiming a physical Tails run. `VALIDATION.txt` records the actual completed checks.
