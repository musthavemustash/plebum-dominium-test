# Site audit and T6 closeout — November 17, 2026

The staging guide had fallen behind the completed T6 rehearsal. This change records that result, updates the two rehearsal procedures and their linked handouts, and supplies current instructions without replacing any signed or previously tested archive. T7 remains untested. This is a staging pull request for owner review, not a beta release or production deployment.

## Scope and baseline

- Repository: `musthavemustash/plebum-dominium-test`, baseline `0daf8ee0b8810f7f8f3d08152d007ad7e508e389`.
- Audited the published `docs/` tree, all 113 HTML documents, canonical handouts, generated one-key and three-key routes, search indexes, test instructions, download references, existing package guards and release metadata. Root/content/template copies are historical sources under the repository's existing source rules, not the deployed guide.
- All 113 live HTML responses matched the baseline checkout byte for byte. This confirms the audit started from what staging served; it does not claim that this proposed branch is already live.
- Scanned 136 inline scripts, HTML IDs, image alternatives, local references and external links. Reviewed changed content in a browser preview at the project's `/plebum-dominium-test/` base path.
- Production was only checked for its maintenance entry point. No production files, deployment settings or financial transactions were changed.

## Findings and repairs

| Finding | Resolution |
| --- | --- |
| Homepage, test page, run sheets and beta checklist still treated both wallet rehearsals as unfinished. | Record T6 PASS for the supervised November 15–16 clean rehearsal, with November 17 closeout. Keep T7 and final release review open. Date earlier results so their historical status remains understandable. |
| T6 directions did not reflect the actual fresh-boot recovery and file-transfer sequence. | Rewrite the run sheet around setup, paper checks, missing/wrong passphrases, restore before funding, first spend with change, another fresh recovery spend, and saved evidence. Use the photo → review → filename → native screenshot flow. |
| Opening `.txn` files from Windows launched Mainnet during the test. | Require explicit Testnet4 on every return, opening the transaction from inside the intended Sparrow window and reviewing it before broadcast. Explain that `tb1` does not distinguish Testnet4 from other test networks. |
| Unsigned fee-rate estimates and the refused confirmation proof were easy to misread. | Add shared transaction checks: every output and total fee, final transaction size, explicit status/block height, and pausing on verification refusal. A connection test or explorer alone does not resolve a wallet proof warning. No verification or TLS bypass is advised. |
| T7 lacked a sufficiently concrete transfer/recovery sequence. | Specify one secret per offline boot, partial PSBT after the first key, the one-key checkpoint before adding the second key, three separately confirmed signing pairs, unavailable-seed recovery and separate missing-working-map reconstruction. Preserve the existing T7 handover requirement. |
| Sparrow/testnet/signing handouts could lead testers to reuse generic or mainnet examples. | Clarify native Segwit Testnet4 settings and complete public origin records. Distinguish the multisig `m/48'/1'/0'/2'` account from T6's single-key path. Update canonical sheets and regenerate both routes and route search indexes. |
| Several tool handouts still described the November 13 candidate as the current release; the software table mixed observed versions with “latest” wording. | Point current instruction text at the signed November 15 release and label software versions as dated observations. Do not claim unperformed checks or certify today's upstream releases. |
| Signed ZIPs contain earlier instructions, so silently replacing their contents would invalidate prior evidence and signatures. | Keep their bytes intact. Publish a separately versioned, instruction-only notes ZIP, checksums and README; tell readers to extract it beside the verified package. Record exact live-source differences in the existing addendum inventory. |
| South Korean breach coverage had an obsolete scope and a source returning HTTP 410. Binance coverage missed a later company update. | Replace the dead source with the FSC's November 5 primary release and qualify the reported counts. Add Binance's November 13 company update with attribution. Refresh news cards, metadata, search text and repeated tickers. |
| The standalone entry-interaction test no longer modeled the current DOM behavior. | Repair its event/focus/selected-element test doubles and assertions; retain substantive inside/outside click and reset checks. Add it and the rehearsal-notes reproducibility check to CI. |

## T6 evidence and limits

The public completion record is `docs/testing/t6-20261116/RESULTS.md`. It carries the supervised session history forward and identifies which final facts are visible in the screenshots or explicitly confirmed by the tester. It is not a fresh inventory of every USB file.

The first payment sent 100,000 test sats with a 140-sat fee and left 285,785 sats. The later fresh-recovery payment sent 285,675 sats with a 110-sat fee and no change. Its transaction ID is `295c7301917a90a9402ebad873e4c95f6c59c3bcee5deff26828681dcdf709f1`; the final screenshot shows two confirmations at block 161821. The wallet view shows zero balance, zero mempool balance and three transactions. The tester confirmed the final screenshots were saved/reopened and that the verification warning did not return.

The original refused-proof observation remains in the record. A different same-network server supplied an accepted confirmation result; the root cause of the initial refusal is unknown. T6's 110-sat fee is an observation, not a recommended multisig fee. T6 does not certify a particular ZIP hash, all T1–T5 cases, T7 or use with real funds.

## Handouts, print material and archive boundaries

Current HTML handouts are the maintained printable source. Previously withdrawn PDFs, presentations and worksheet documents remain withdrawn; their removal inventory and anti-resurrection test remain enforced. No old PDF was republished or relabeled as current. The changed instructions appear in both generated guide paths.

An automated source/layout check is not a physical print test. The November 17 follow-up below resolves the specific first-page pagination defect from both saved-PDF retests. Wider handout and final-release print acceptance remain open. Similarly, tests against earlier R3/R4 archives retain their original package identity. Historical result files and signed archives were not rewritten to imply they contain these new instructions.

## Validation

All 24 final command checks passed; results are recorded in `SITE_AUDIT_20261117_CHECKS.json`. The final static scan also passed for all 113 HTML pages and 136 inline scripts. The workflow validates source/download consistency, signed manifests, tool behavior, generated paths, page-test modules, package structure, Tails helpers, the new notes ZIP and entry interactions. Additional ticker, UI-state and packaging checks supplement the workflow. Current signed ZIP hashes remain pinned, and deliberately altered bytes or unrecorded source drift are still rejected.

Baseline static checks found no duplicate IDs, missing image `alt` attributes or inline JavaScript syntax failures. Local references are checked by the repository build. Browser review covered the homepage test disclosure, the T6 closeout, T7 steps, the downloads addendum and the changed one-key/three-key handouts. No horizontal overflow appeared on the reviewed desktop signing page. Browser-extension metadata errors were observed; they were not attributed to the site's code. This was not a fresh mobile-device, screen-reader, Windows/Tails or physical-print session.

## Remaining work

1. Complete T7 with its own evidence: all three signing pairs, one-key refusal, both recovery scenarios and handover.
2. Reconcile outstanding T1–T5 cases and print evidence against the intended release. A T6 pass does not fill missing results.
3. The link audit attempted 123 external URLs: 55 returned successfully, 67 Google Form links returned HTTP 401 in this environment, and the one HTTP 410 source was replaced. Form access/submission could not be certified; preserve local notes and use the existing contact route if the form is unavailable. No form submissions or form edits were made.
4. Staging has no page-level `noindex` directive. Decide separately whether public staging search indexing is wanted; changing signed tool HTML solely for this purpose would require a new release process.
5. After review/merge, verify the staging deployment. Final package reconciliation/signing and explicit owner approval remain necessary before beta or any production release.

This is a site-wide content, consistency and regression audit. It is not an independent cryptographic certification or a guarantee that every external service, device or assistive technology works.

## Primary references checked

- [Sparrow quick start](https://sparrowwallet.com/docs/quick-start.html)
- [BIP48 account derivation specification](https://github.com/bitcoin/bips/blob/master/bip-0048.mediawiki)
- [Electrum protocol methods and transaction proof](https://electrum-protocol.readthedocs.io/en/latest/protocol-methods.html)
- [Financial Services Commission, November 5 update](https://www.fsc.go.kr/eng/pr010101/88092)
- [Binance, November 13 company update](https://www.binance.com/en/square/post/387666783762379)
- [Chainalysis incident updates](https://www.chainalysis.com/blog/security-incident-october-30/)

Version-specific Sparrow menu wording and the T6 outcomes come from the user's observed rehearsal, not an inference that all upstream documentation or software versions match it.


## Follow-up: uploaded evidence reviewed November 17

After the audit draft, the tester supplied an updated Drive folder. The clean T6 folder lists 93 files; 11 selected images were downloaded, hashed and visually reviewed. They support the existing T6 pass, including package verification, public address matching, missing/wrong-passphrase address differences and both final transaction statuses. Screenshot 01 identifies the complete signed 20261115-r1 ZIP and its published SHA-256; screenshot 03 displays the 231-file check. This resolves the earlier lack of direct package association in the closeout, without certifying all tool cases.

See `docs/testing/t6-20261116/EVIDENCE-REVIEW-20261117.md` for individual image links, observed scope, image hashes and archive notes. The second signed transaction file was not found in the clean T6 folder or focused filename search, although its reopened state and final confirmation are pictured. The related Windows folder contains the original print failure evidence. Both later retest PDFs were recovered from the earlier conversation and visually inspected: the first-page defect passes for both routes. T7 and wider print acceptance remain open. Original closeout and downloadable notes are retained unchanged; this is a separate evidence addendum.


The two further supplied folders add earlier Windows/Tails evidence and a data USB backup. This follow-up reviewed 20 selected images in total and both pages of each of two earlier print PDFs, not every uploaded file. Five downloaded ZIPs (two older complete packages and all three signed 20261115-r1 packages) match their archived repository files byte for byte. The USB backup's manifest and detached signature also match the published copies; the pinned-key signature check passed again. The helper/signing screenshots corroborate the existing November 15 record, rather than constituting a new test run. Wallet/key backup contents were not opened or republished; backup inventory was scoped and one large folder response was partial. The additional evidence does not pass T7 or all T1–T5 cases.

The testing page, Downloads and test notes now reflect the two saved-PDF retest passes. The original failure record and all signed archives remain unchanged. See the evidence addendum for package/image/PDF hashes, individual reviewed-image references and exact limits.

Follow-up validation: static build validates 113 HTML pages; download consistency, immutable release signatures/ZIPs and rehearsal-notes reproducibility pass; `git diff --check` is clean. The original 24-command report above describes the full audit before this evidence-only follow-up. No fresh physical run or release rebuild was performed.
