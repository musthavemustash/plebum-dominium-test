# Plebum Dominium: T6 completion record

**Result: PASS — one key plus passphrase rehearsal complete.**

**Closeout recorded:** November 17, 2026.

**Session dates:** November 15–16, 2026 (America/New_York; evidence naming retained).
**Run folder:** `T6-20261115-r1-clean`
**Tester:** Site owner
**Network:** Testnet4; disposable test coins only.

## What passed

| Check | Result and basis |
| --- | --- |
| Wallet setup and paper backup | Completed earlier in the supervised clean run, as recorded in the session history. |
| Missing and incorrect BIP39 passphrase checks | Recorded complete earlier in the session history. |
| Fresh paper restoration | Restored from the original 24-word paper backup and exact original passphrase in fresh offline Tails sessions. |
| Wallet identity | Single Signature HD, Native Segwit (P2WPKH), fingerprint `3d56e8c1`, derivation `m/84'/1'/0'`. |
| Address matching after recovery | Tester confirmed the first three receive addresses and first change address matched baseline screenshot 25. |
| Offline signing | Both transactions reviewed and signed in Tails with networking disabled; Sparrow 2.5.6 was the session's recorded version. No hardware signer was used. |
| USB transfer | Unsigned PSBTs and signed transaction files were saved and reopened during the walkthrough. |
| First payment | 100,000 test sats sent, 140-sat fee, 285,785 sats returned as change. Confirmation rechecked after the server switch. |
| Recovery payment | 285,675 test sats sent after another fresh paper restoration, 110-sat fee, no change output. Final screenshot shows 2 confirmations in block 161821. |
| Final balance | Final wallet screenshot shows 0 sats balance, 0 sats mempool, and three transactions. |
| Final evidence | Tester confirmed screenshots 88 and 89 were saved on the USB and reopened correctly. |
| Verification warning | Tester explicitly confirmed “Transaction Verification Refused” did not return after switching to mempool.space. |

## Transaction accounting

| Movement | Payment | Fee | Remaining wallet balance |
| --- | ---: | ---: | ---: |
| Faucet receipt | +385,925 sats | — | 385,925 sats |
| First payment | 100,000 sats | 140 sats | 285,785 sats |
| Recovery payment | 285,675 sats | 110 sats | 0 sats |

Total returned to the faucet: **385,675 test sats**. Total fees: **250 sats**.

Recovery transaction ID:
`295c7301917a90a9402ebad873e4c95f6c59c3bcee5deff26828681dcdf709f1`

Recipient used in both payments:
`tb1qerzrlxcfu24davlur5sqmgzzgsal6wusda40er`

Saved recovery transaction:
`T6-CLEAN-Testnet4-spend-02-signed.txn`

## Issues encountered and resolution

**Server verification warning.** The first payment initially displayed a confirmation at block 161805, followed by “Transaction Verification Refused.” That initial confirmation assessment was withdrawn. The connection was changed from `blackie.c3-soft.com` to Sparrow's `mempool.space` Testnet4 entry. The first payment subsequently showed 11 confirmations at block 161806. The tester has now confirmed that the warning did not return. The underlying cause was not established; retain the warning and server-switch evidence.

**Windows network selection.** On returning from Tails, the signed transaction was twice opened with Mainnet address rendering. Both times the walkthrough stopped before broadcast, Sparrow was restarted in Testnet4, and the transaction was reopened and reviewed there. Future instructions should explicitly confirm Testnet4 before opening the signed file inside Sparrow.

**Recovery transaction fee.** The initial unsigned draft had a 100-sat fee and a non-final size estimate. It was rebuilt with a 110-sat fee before export. The final signed screenshot shows 1.01 sats/vB.

**Confirmation wait.** The recovery payment remained unconfirmed for more than 20 minutes, then showed two confirmations. No replacement transaction was needed in the recorded walkthrough.

## Final evidence references

- `T6-CLEAN-20261116-88-Windows-second-spend-confirmed.png`
- `T6-CLEAN-20261116-89-Windows-final-zero-balance.png`
- Supporting session evidence: 65–68 for the server warning and switch; 75–84 for the fresh offline recovery and signing; 85–87 for network correction and broadcast.
- Final tester responses: “1 yes saved” and “2: not returned.”

## Scope and next milestone

This record closes the supervised T6 wallet rehearsal using the conversation's recorded checks, final screenshots, and tester confirmations. Earlier checks are carried forward from the session history; this is not a fresh audit of every saved evidence file or a certification of a specific release ZIP hash.

**T7, the three-key / 2-of-3 multisig rehearsal, remains the next wallet-testing milestone.** T6 completion alone does not authorize beta publication. Final release checks and explicit production approval still apply.

