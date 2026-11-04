# Tool investigation — November 4, 2026

Baseline: staging `aa06ea2f4d317acd39b0d863f36aa46c8f12774c`. Investigation only: tool code, bundled ZIP and published hashes have not been changed. No real seeds, keys or passphrases used. Downloads remain blocked for release; existing direct URLs are not quarantined.

## Provenance findings

| File | Finding | Decision |
|---|---|---|
| Python dice converter | Published hash matches historical commit `0dca9a6a1b7f`. Standalone differs from bundle only in version labels/pin filenames: Tails 7.13 → 7.16 and Electrum 4.8.2 → 4.8.3, but checksum values stayed identical. Change appears in `46d41f004c44`. | Conversion core passes tests. External software pins are not authenticated; do not approve the bundled verifier as a release gate. |
| HTML dice converter | Published hash matches `67ad2f85abc0`. Current code has stricter validation and removes active third-party network probes. Bundle still silently strips invalid characters from binary input and contains Google/gstatic image probes. | Current core is preferred over the older bundle, but offline/UI review remains required. Do not restore bundle over current source. |
| HTML descriptor tool | Published hash matches `67ad2f85abc0`. Bundle differs in network-probe/guard logic; embedded library and crypto controller match current standalone. | Cross-decryption passes; dependency provenance and UI/guard issues still block release. |
| File verifier HTML | Published hash matches `230fa3836878`. Current PINNED array contains obsolete dice/descriptor hashes and older Python hash. | Rebuild expectations only after intended sources are reviewed. |
| EFF wordlist | No published-hash match found in available file history. Direct HTTPS retrieval from EFF is exactly identical to current standalone and bundle: 108800 bytes, SHA-256 `addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e`. | Current wordlist identity confirmed; manifest value is stale. No manifest rewrite in this investigation. |

EFF URL: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt

The embedded library labels itself OpenPGP.js 6.3.2. Fetching `https://raw.githubusercontent.com/openpgpjs/openpgpjs/v6.3.2/dist/openpgp.min.js` returned 404. This alone does not establish a malicious or nonexistent release; it leaves that provenance check unresolved. Confirm an official release artifact and independently compare library bytes before certification.

## Tests performed

Run from repository root:

```
python3 scripts/test_tool_core.py
node scripts/test_tool_network.cjs
```

- Eight published English 256-bit BIP39 entropy/mnemonic vectors pass in both current Python and extracted HTML pure-code implementations. Both embedded BIP39 wordlists exactly match upstream English list.
- Dice mapping 1→00, 2→01, 3→10, 4→11, discard 5/6; bad mnemonic checksum rejected.
- Three excess-bit inputs (including non-byte-aligned input) agree with Python and an independent standard-library SHA-256 calculation. This preprocessing is a project convention, not a BIP39 standard input format.
- Empty, short, invalid-character and nonstandard-whitespace inputs are rejected consistently.
- Embedded OpenPGP.js using the shipped UI's four configuration statements and Python/GPG cross-decrypt in both directions. Unicode sample text roundtrips. Wrong passwords, truncated messages and altered armored payloads are rejected by both implementations.
- GnuPG 2.4.4 used an isolated temporary home with symmetric-key caching disabled. This is not certification for the guide's target Tails/GPG version. Temporary GPG agent stopped afterward.
- Extracted network-state functions block HTTP(S) regardless of navigator status and block local files when navigator.onLine is true. These are DOM-double logic tests, not browser tests.

## Remaining findings and limits

1. Both current tools permit local use if `navigator.onLine` is unavailable rather than explicitly false. Unknown status is not fail-closed. Neither navigator status nor a local URL proves physical isolation.
2. Descriptor reconnect `wipe()` clears textareas and `.pw` textContent, but actual passwords are `input[type=password]` without `.pw`. Password values therefore are not cleared by this handler. Verify a repair with UI-level tests before release.
3. Descriptor decrypt failure leaves an earlier successful plaintext/result visible. Clear stale output when starting a new operation and on failure; verify with UI tests.
4. Current application scripts contain no fetch, XMLHttpRequest, WebSocket, sendBeacon or Image probe calls and no external script tags. This is a targeted source scan, not proof of no egress. The vendored cryptographic library was not comprehensively audited and no real browser traffic was observed. The older bundle does contain active image probes.
5. Encryption UI trims input; Python decrypt strips leading/trailing whitespace. The test sample avoids intentional edge whitespace. Do not claim byte-for-byte preservation of arbitrary files.
6. UI prose says the HTML tool uses SHA-256 while current code configures SHA-512; prose also recommends deleting plaintext immediately after encryption. Correct those claims with the future repair.
7. HTML converter's excess-input notice reports the post-hash length (256), not the submitted length. Mnemonic calculation still passed tested cases; fix misleading reporting separately.

## Release decision and next repair

**Do not republish a reconciled tool bundle yet.** Core tests pass within the bounds above; provenance, external version pins, offline guards and UI state remain incomplete. Next: establish official OpenPGP artifact provenance and authenticate version-specific upstream pins; repair guard/password/stale-output handling with regression tests; complete browser/target-environment testing; then rebuild ZIP, full-hash manifest and verifier expectations atomically from the approved files. Keep known-answer tests as repeatable release checks. Do not replace manifest hashes merely to turn mismatches into matches.
