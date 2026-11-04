# Dependency and software-pin review — November 4, 2026

Scope: step one of the tool-release repair. Staging only. No tool, ZIP, published hash, version pin or production file changed. Prior baseline: `b4c37b9e35a962d677c942669a85a59228f4eb19`.

## Decision table

| Component | Result | Release implication |
|---|---|---|
| Embedded OpenPGP.js 6.3.2 | MATCH to published npm distribution after trimming only outer whitespace. Registry package integrity and both registry signatures verified. Official GitHub release v6.3.2 exists. | Prior missing-source-URL concern resolved at package identity level. This does not certify application code, dependency vulnerability status or target-browser behavior. |
| Sparrow 2.5.5 Linux x86_64 archive pin | MATCH to authenticated signed manifest. GPG verified full fingerprint against publisher's download instructions. GitHub release asset digest agrees. | Pin provenance established. Binary itself was not downloaded/hashed or executed; no automatic upgrade to current 2.5.6. |
| Tails 7.16 IMG and ISO pins | MISMATCH with Tails' official HTTPS installation metadata. | Existing pins are wrong for the observed 7.16 metadata; leave them blocked. Candidates below are not a completed image-signature verification or compatibility certification. |
| Electrum 4.8.3 AppImage pin | UNVERIFIED. Official site confirms version/file and signature links, but direct binary and signature requests return HTTP 403. | Do not approve or replace the carried-over hash without obtaining exact binary/signature and checking trusted signer identity. |
| Ian Coleman standalone page | Existing unversioned extra pin remains outside this requested four-component check. | Still needs a versioned source and provenance before certifying the converter's entire external-download verifier. |

## OpenPGP package identity

Official release: https://github.com/openpgpjs/openpgpjs/releases/tag/v6.3.2

Registry metadata: https://registry.npmjs.org/openpgp/6.3.2

Distribution: https://registry.npmjs.org/openpgp/-/openpgp-6.3.2.tgz

Registry keys: https://registry.npmjs.org/-/npm/v1/keys

- Registry metadata points to `https://github.com/openpgpjs/openpgpjs.git`.
- Tarball SHA-256: `3eeea348b6e02e81387af584a189eab5446f3df223382127bc17ac06b6ea77b7`.
- Tarball SHA-512 matched the integrity field preserved in `provenance/npm.json`.
- Both signatures verified using Node crypto ECDSA/SHA-256 against the registry key and message `openpgp@6.3.2:<integrity>`; public key response is preserved. This establishes registry-signed package metadata, not an independent maintainer signature on the embedded library.
- `package/dist/openpgp.min.js`: 395214 bytes; SHA-256 `e19bf4f04f34f24caded3ff3f3643099538b2674a0a94221e2faca75ac3e4aa1`.
- Trimmed official file and trimmed first inline script of `docs/descriptor-tool.html` match byte for byte. Trimmed SHA-256: `28891fa2ad3493312f42edfbd5efae3bb94878900dd864e9b9d647a1db0fd95b`.
- Earlier raw GitHub `dist` URL returned 404 because that URL was not a usable distribution source. It did not establish absence of the release.

## Sparrow signed pin

Publisher instructions: https://sparrowwallet.com/download/

Key linked by those instructions: https://keybase.io/craigraw/pgp_keys.asc

Release manifest and detached signature:
- https://github.com/sparrowwallet/sparrow/releases/download/2.5.5/sparrow-2.5.5-manifest.txt
- https://github.com/sparrowwallet/sparrow/releases/download/2.5.5/sparrow-2.5.5-manifest.txt.asc

Imported only this public key into a temporary GPG home. `gpg --status-fd 1 --verify` returned exit 0 and VALIDSIG for `D4D0D3202FC06849A257B38DE94618334C674B40`, matching the complete fingerprint on the publisher's instructions. Key trust remained undefined locally; no blanket trust was assigned. Preserved status output, key, manifest and signature in `provenance/`.

Authenticated manifest entry:

```
7e8a59bf7e7293bd924518dda8ea7747696634297de54878c1c5f5cdb528559d *sparrowwallet-2.5.5-x86_64.tar.gz
```

This matches the existing Python verifier pin. No archive execution or compatibility validation performed.

## Tails incorrect pins

Source retrieved directly: https://tails.net/install/v2/Tails/amd64/stable/latest.json

Snapshot preserved in `provenance/tails.json`; version field is 7.16. Metadata changes over time, so use this snapshot as evidence, not a permanent latest-version assertion.

| File | Existing pin | Official HTTPS metadata candidate |
|---|---|---|
| tails-amd64-7.16.img | `8c4e63c7c47a000335bf2e66158c0d062c063619599e45d717759d8f1621f468` | `7bef45b9aad430e6c2bbfd78c30c5a7ad2f143d498a002b96b88814a18c52a1d` |
| tails-amd64-7.16.iso | `cacb025f452ad010257dd5d3ba7bf7cb1bdfde50e8e583670d604d0bb6336682` | `db90cb147cbfa74a801ede758061a3dcf1393b102405bdeccab4708e2fdbd71e` |

Image sizes in metadata: IMG 1901068288 bytes; ISO 1891045376 bytes. No multi-gigabyte image download, detached-signature verification or boot test performed. Do not label these candidate hashes as signed/locally verified images. Next verification must obtain exact images and signatures via the official installation flow, validate signer identity and compare the bytes before changing a production-quality pin set.

## Electrum blocker

Official release page: https://electrum.org/

Release directory: https://download.electrum.org/4.8.3/

The official page identifies the AppImage and signatures and links signer public keys. Direct requests for both `https://download.electrum.org/4.8.3/electrum-4.8.3-x86_64.AppImage` and the same URL ending `.asc` returned HTTP 403. Directory was readable through web retrieval but the binary bytes were not obtained. The website deliberately emphasizes signatures rather than publishing binary hashes.

Existing pin `6310ebd0b7965196ecc3eb7e1bfead260cdc9033a8847204561b9762e62a87c0` remains unverified; file naming/version existence is not hash authentication. No third-party binary substituted. Complete on a machine with access to official downloads, preserving binary hash, signature verification results and full signer fingerprints for review.

## Next action

Proceed with the already identified offline/UI repairs while preserving the download block. Before repackaging, close Tails image verification, Electrum artifact access/signatures and the additional unversioned Ian Coleman pin. Maintain the distinction between matching a published dependency and certifying a complete custody workflow.

Follow-up: [OFFLINE_CONTROL_REPAIR.md](OFFLINE_CONTROL_REPAIR.md) records completed Tails image/signature verification and repaired offline/UI issues. Electrum, browser validation and packaging remain open.
