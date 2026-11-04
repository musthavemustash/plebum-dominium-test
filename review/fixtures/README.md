# Public test fixtures

Retrieved November 4, 2026:

- `bip39-vectors.json`: eight English 256-bit entropy/mnemonic pairs selected from https://raw.githubusercontent.com/trezor/python-mnemonic/master/vectors.json . Other language sets, seed outputs and extended keys omitted. Upstream MIT license is included as `python-mnemonic-LICENSE`.
- `bip39-english.txt`: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt . Public BIP39 word list, used to compare all 2048 embedded entries. BIP39 specification: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki .

These are public examples, never wallets for real funds. Tests use fixture content checked into this commit; they perform no network retrieval. The JavaScript harness evaluates pure functions/library code with Node and WebCrypto, not a browser or a browser-security workaround.
