# Staging review — November 3, 2026 (Eastern)

Baseline: `3030e444ef7aaf0418c4db148ff5cc04495492d9`. PRs #3 and #4 are merged. Independently visited both public GitHub Pages handouts and exercised their UI. The public pages match the newer `docs/handouts/` variants, including the four Sparrow verification cards and Threat Model worksheet.

## Prioritized findings

| Priority | Finding | Status |
| --- | --- | --- |
| P1 | Rebuilding replaces `docs/` using older Markdown/templates and root assets. The interactive Threat Model layout is absent from the generator source; root and docs handouts also differ. Reviewed fixes can disappear on regeneration. | Open release blocker. Establish a single authoritative build path before production; do not run the legacy generator over the reviewed staging pages. |
| P1 | Sparrow overview still reduced verification to a first-address comparison, and said no seed touches the build despite later seed-entry steps. Threat Model said “lose two keys and the map,” obscuring independent failure conditions. | Corrected in the prepared patch where reviewed. Detailed independent cosigner verification warning retained. |
| P2 | At a 390px iframe viewport, live pages had 436px body width with 375px usable width. Header theme/status controls overflowed horizontally. | Fixed with a wrapping mobile header. Local checks at 320px and 390px pass without document overflow. |
| P2 | Closed mobile drawer remained in navigation/accessibility traversal; menu icon inherited a dark default color in dark theme. | Added inert closed state, drawer focus handling/Tab wrap, Escape return, and themed icon color. |
| P2 | Threat Model top Next link went to Terms, whereas bottom Next and main CTA went to Choose your path. | Top link corrected. |
| P2 | Two summary controllers updated the same live region. Checked cards also displayed a redundant custom indicator beside the native input. | Removed duplicate inline controller, retained shared summary, scoped the live status to changing text, removed redundant indicator. |
| P2 | Sparrow commands included literal `$` prompt characters copied by the generic copy handler. Instructions relied on red text as an error signal. | Removed prompt characters from commands; clarified command completion, launch behavior, and actual errors. No software was executed. |
| P3 | Sparrow overview said 9 sections but the rendered procedure has seven numbered steps. Site navigation numbers mix sheet counts and overall positions (Sparrow is sidebar 08 but Step 7 of 17). | Local step count corrected; site-wide numbering remains open. |
| P3 | Threat Model uses permanently dark panels in light theme; mobile metadata cards consume substantial vertical space. | Existing design retained pending visual preference. |

## Validation

- Public staging desktop browser: navigated home → Threat Model → Sparrow; selected concern/origin, expanded tradeoffs, activated command Copy (UI reported Copied). Terminal markup renders as four separate lines; revised verification cards are present.
- Public staging mobile: 390px iframe layout, menu open/Escape close, observed horizontal overflow and offscreen drawer exposure.
- Prepared patch: desktop at 1363px; mobile iframe widths 320px and 390px (305px and 375px usable after scrollbars). No document-wide horizontal overflow on checked pages; Sparrow cards stack to one column.
- Checked concern toggle by keyboard Space, origin radio selection, shared summary updates, mobile drawer open/Escape close, and light/dark appearance. Existing warning text and no-secret-input model retained.
- JavaScript syntax checks and `git diff --check` pass. Both handouts have unique IDs and all linked staging file paths exist locally.
- Browser preview is a local copy of staging docs. Narrow iframes test CSS layout and interactions, not physical iOS/Android browsers. Screen-reader software, full WCAG audit, print output, actual wallet creation/recovery, offline kit integrity, and all dependency/version claims were not validated. A complete custody walkthrough remains a release gate.

## Security reference

Sparrow’s own multisig backup dialog requires threshold signing seeds and all cosigner xpubs, recommending wallet-file or output-descriptor backup: https://github.com/sparrowwallet/sparrow/blob/master/src/main/java/com/sparrowwallet/sparrow/wallet/MultisigBackupDialog.java

## Release status

Prepared as a staging-only review branch. No production repository changes, production merge, tag, or deployment. Do not treat this patch as production-ready: generator alignment and end-to-end recovery validation remain outstanding.

Next options: review browser preview, deploy this bounded patch to staging, or refine the design.

## November 4 — independent-path batch

PR #6 / `995525c85152415beecc3b1cbd2ef9db1566d957` Pages deployment confirmed successful on this run. No open PR or newer main commit was found before editing.

User clarified that the order is Terms → Before you begin (Threat Model) → Pick your path. Both routes now follow that order, with the remaining sheets in the existing order. One-key has 12 numbered pages; three-key has 16. Two devices is an optional reference. A selected route is encoded in its URL rather than a local-storage gate. Switching routes keeps equivalent topics when available; otherwise it opens Terms. Old variant bookmarks resolve to usable route pages. Reading completion remains separate from custody/recovery verification.

Validation performed:

- `python3 scripts/test_paths.py`: all 28 numbered pages, 2 overview pages, consecutive sidebar numbering, exact sidebar destinations, both top/bottom Previous and Next destinations, unique IDs, absence of path gates, expected variant rendering, JS/static sequence parity, and separate completion-key code passed.
- `python3 scripts/build.py`: 95 HTML pages have valid local file references and staging base paths. Also checks generated page/search-index equality against current reviewed sources, without rewriting files.
- `python3 scripts/render_paths.py --check`, `node --check docs/assets/js/main.js`, and `git diff --check` passed.
- Search now loads a path-specific index and uses the same numbers as that route. Fixed the existing main-script base selector so cache-version query strings no longer break the search-index URL.
- Browser QA NOT performed for this batch: preview initially refused connection; after the managed preview restarted, browser security policy denied access. No alternate browser surface or bypass was attempted. Runtime clicks, mobile rendering, keyboard interaction, and live browser confirmation remain outstanding. Static checks do not certify these.
- No cryptographic implementation or offline-tool boundary was changed. Existing detailed handout custody guidance remains subject to the broader content audit. In particular, shared Two boots/Check the files content still needs review for path-specific explanations; this batch establishes independent navigation, not a complete rewrite of every procedure.

## November 4 — homepage and glossary batch

Baseline: PR #8 main `93131ec2f2555b5922e395eb48f94be329c5e347`, Pages success confirmed; no open PR at start. Integrated the preserved entry-page work selectively rather than overwriting the new navigation controller.

Homepage now uses responsive two-column/one-column cards in normal document flow, one H1, balanced setup tradeoffs, explicit test-site/no-secret warning, and Terms-first CTA. Removed the unverified headline ticker from this page only. Terms has twelve visible definitions without JavaScript and a progressive local filter when JavaScript runs. Corrected the demo's three-seed recovery claim and retained descriptor/configuration backup advice. Mobile position labels now agree with route numbers, including overview pages.

Primary references checked November 4: BIP39 https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039.mediawiki (entropy/checksum, mnemonic-to-seed, every passphrase produces a seed); BIP174 https://raw.githubusercontent.com/bitcoin/bips/master/bip-0174.mediawiki (portable transaction/signature information and offline signers). Multisig backup guidance also follows the Sparrow source recorded in the earlier security review; its raw-source re-fetch was unavailable during this run.

Validation: `node scripts/test_entry_interactions.js` passes glossary matching/no-match/clear behavior, all three key-demo states and reset, and the single homepage H1. These use DOM doubles and are not browser tests. Path traversal/parity tests, 95-page local-reference/source-drift validation, JavaScript syntax checks, and diff whitespace checks pass. No seed/private-key/passphrase inputs or cryptographic/offline-tool changes were introduced.

Browser/live appearance remains unverified following the earlier browser policy block; no workaround was used. Actual mobile/keyboard/theme/print rendering and screen-reader behavior still require browser review. Responsive CSS and print behavior are implemented but not visually certified.

## November 4 — verification/offline guidance batch

Baseline `77b479ccb0fc1c1c9e8653c74acc31f49ee4e5b9` (PR #9); Pages success confirmed and no open PRs at start. Reworked canonical verify/airgap handouts and regenerated both routes. Check the files now separates source, integrity, authenticated signer, and verification records. Two boots explains Offline Mode, public-data-only transfer boundaries, hardware/firmware limits, and full shutdown without claiming it reverses compromise. One-key dice no longer asks for Seeds 2/3. Dice text clarifies fair independent rolls, exact entropy-method compatibility, and the final word's three entropy/eight checksum bits for 24-word BIP39.

Primary sources checked November 4:
- https://tails.net/doc/first_steps/welcome_screen/index.en.html — Offline Mode before starting the desktop.
- https://tails.net/doc/about/warnings/computer/index.en.html — compromised installation systems and hardware/firmware limitations.
- https://tails.net/install/index.en.html — current official installation/verification entry points; lists 7.16. No blanket future-version compatibility claim retained in revised airgap page.
- https://sparrowwallet.com/download/ — signed manifest, full signing fingerprint and local key-trust warnings. Current download is 2.5.6; existing kit pins 2.5.5. Updating pins/binaries is NOT part of this batch and requires coordinated verification.
- BIP39 specification checked in the preceding batch for entropy/checksum layout; no converter code was changed.

Checks passed: local file references/drift across 95 HTML pages, all 28 numbered navigation routes, glossary/demo logic regression, unique IDs on five touched canonical handouts, targeted assertions removing one-key three-seed instructions and unsafe verification/transfer claims, and diff whitespace checks. Existing tool files and offline enforcement were not modified. Browser/mobile/live rendering remains unverified after the prior policy block; no bypass attempted.

Outstanding: independently exercise the actual offline converters with public test vectors and matching entropy input settings before endorsing a specific cross-tool procedure. Existing instructions are now explicit to stop if equivalence cannot be established. No real seed material was used. dice-easy received only a narrow explanatory correction, not a full content review. Checklist versions and the pinned download inventory still need reconciliation; no compatibility upgrade is claimed.

## November 4 — backup and recovery batch

- Confirmed PR #10 merged as `e2798b8a8d8d2b7a94d07a6eccf22ccc281d04da`; Pages run 41826034173 succeeded. No open PRs at batch start.
- Revised checklist, titanium, inheritance and fire-card canonical handouts for both active paths (eight source pages), regenerated eight route pages and both search indexes. Preserved separate route order and navigation. Rebuilt section anchors/contents to match new headings.
- Removed blanket bans on extra backups, automatic paper destruction, assumptions that missing/wrong passphrases always yield empty wallets, and recovery-card sufficiency claims. Added complete configuration records, cautious backup verification without wiping the only signer, and stop/investigate guidance for an unexpected empty wallet.
- Recovery cards now describe private location pointers, with no form collecting secrets or real locations. Legacy downloadable PDFs are explicitly not reconciled with these revised pages. No wallet cryptography or offline-tool boundaries changed.
- References checked: Trezor https://trezor.io/guides/backups-recovery/advanced-wallets/what-is-a-passphrase and BIP 380 https://raw.githubusercontent.com/bitcoin/bips/master/bip-0380.mediawiki . Descriptors may contain private keys; do not treat every descriptor as public.
- Validation: 95-page link/base/drift check; all 28 route steps/2 overviews, independent navigation and numbering; existing glossary/demo logic checks; internal section anchors for all eight revised route pages; git diff whitespace check. Browser/mobile/print rendering remains unverified after the earlier browser-policy block. No funded-wallet or actual recovery execution performed.

Next: confirm this batch PR/Pages deployment; review remaining signing, testnet, encryption, FAQ variants, briefing, single-sig/two-devices, path risks, supporting pages and downloads/tools. Legacy easy variants and downloadable print packet still need reconciliation. Full-site completion is not claimed.

## November 4 — signing, testnet and encryption batch

- Baseline main `43094a3c33337af7af84925772320a9415768788` (PR #11); Pages run 41858924172 succeeded. No open PRs or conflicting remote work at start.
- Reworked Practice spend, Rehearse on testnet and Hide the wallet map into responsive document-flow cards. Regenerated the three-key copies and search index; preserved route ordering and independent one-key route.
- Signing now requires policy, recipient, amount, fee and change review for each signer, and distinguishes rebooting from independent hardware. Testnet now uses disposable keys, explicit network matching, full policy verification and recovery rehearsals rather than first-address-only assurance.
- Encryption now distinguishes public-only descriptors from exports containing private keys; removes guarantees about three seeds automatically restoring configuration and trash deletion erasing all copies. Describes documented Kleopatra encryption/decryption and verification before replacing backups. Bundled descriptor tool remains unchanged and explicitly pending independent compatibility/offline tests.
- Primary sources checked November 4: https://www.sparrowwallet.com/docs/faq.html (testnet setup); https://raw.githubusercontent.com/bitcoin/bips/master/bip-0174.mediawiki (PSBT); https://raw.githubusercontent.com/bitcoin/bips/master/bip-0380.mediawiki (descriptor configuration and key types); https://tails.net/doc/encryption_and_privacy/kleopatra/index.en.html (file encryption/decryption).
- Passed: 95-page link/base/source-drift validation, 28-step/two-overview route regression, existing glossary/demo logic, all six touched source/route page IDs and section anchors, whitespace checks. These are source/logic checks, not browser or wallet execution. No tool cryptography, secret input, or offline enforcement changed.
- Browser/mobile/print verification remains outstanding after the earlier policy block. Neither actual signing/recovery nor encryption interoperability was exercised. No production changes.

Next: confirm this batch deployment; continue FAQ variants, briefing, single-sig/two-devices, path risks and supporting pages. Downloads, PDFs, pinned version compatibility and offline tool vectors remain unresolved. Full-site completion is not claimed.

## November 4 — FAQ, supplementary guides and download triage

- Confirmed PR #12 main `6c80cea7cdf754c3933fd3add96d8573a2c68783` and successful Pages run 41866968884. No open PR or remote conflict at start.
- Revised FAQ/full, FAQ/one and legacy FAQ/easy; briefing; single-sig; optional two-devices; path-risks and downloads (eight sources). Regenerated active routes and route search indexes. Preserved independent numbering/order.
- Corrected a critical two-device claim: two compromised device keys can satisfy 2-of-3 without the dice key. Removed automatic backup destruction, original-device-as-required-secret claims, empty-wallet guarantees, false three-seed map reconstruction assurance and fresh-boot hardware isolation assumptions. Single-sig now explains that adding a passphrase selects another wallet and does not move existing funds.
- Path risks now compares both routes with ordinary visible sections and direct overview links; removed the obsolete instruction to escape gated pages by switching paths.
- Download triage found five of nine manifest entries mismatch actual files: Python dice converter, HTML dice converter, descriptor-tool HTML, verify-file HTML and EFF wordlist. Bundle hash matches, but several bundled tools differ from standalone copies. See DOWNLOAD_INVENTORY.md for exact expected/actual hashes and follow-up. No hashes or tool code were rewritten to mask mismatches. Downloads now exposes this blocker, withholds tool shortcuts and labels older PDFs/slides/worksheet as legacy/unreviewed. Direct tool URLs elsewhere still exist; do not claim site-wide quarantine.
- Primary sources: Trezor https://trezor.io/guides/backups-recovery/advanced-wallets/what-is-a-passphrase and BIP380 https://raw.githubusercontent.com/bitcoin/bips/master/bip-0380.mediawiki checked November 4. Hardware compromise limitation follows prior Tails warning review; this run's Tails refetch failed. No specific device pairing or recovery walkthrough certified.
- Passed: 95 HTML reference/base/source-drift checks; 28 route steps and two overviews; existing glossary/demo logic; IDs and internal section links on all eight revised sources; whitespace checks. Browser/mobile/print and actual signing/recovery remain unverified after the prior browser-policy block. Tool cryptography and offline enforcement unchanged.

Next: confirm PR/Pages status. Highest priority is tool provenance/hash/archive reconciliation and known-answer tests, then PDF regeneration and visual review. Remaining legacy easy handouts, chooser claims, supporting newcomer/news/beyond/demo pages and site-wide search/browser regression still need review. This batch completes the named web-page revisions but only triages downloads; full-site completion is not claimed.

## November 4 — tool provenance and repeatable tests

Baseline aa06ea2f4d317acd39b0d863f36aa46c8f12774c; no open PRs at start. Investigated all five mismatches and bundle differences. Four manifest hashes match older available Git versions. EFF direct download exactly matches current wordlist; manifest is stale. Python version labels changed without changing external software hashes. Bundle retains older permissive binary-input handling and active network probes.

Added public fixtures and repeatable Python/Node core tests: eight published 256-bit BIP39 vectors, embedded wordlists, mapping/checksum/input validation, excess-bit parity, Python/GPG↔embedded JS encryption with Unicode, wrong-password/truncation/corruption rejection. Network-state logic tested with DOM doubles. Found unknown-status permissiveness, reconnect password wipe mismatch, stale decrypt output, and unconfirmed embedded dependency provenance. See TOOL_VALIDATION.md for exact evidence and repair sequence.

No tools, hashes or ZIP modified; downloads remain blocked for release. No real secrets used. Browser/target-Tails execution and network egress not certified. Next: dependency and upstream-pin provenance, guard/UI repairs with tests, then atomic packaging only after passing the remaining gates. This investigation does not resolve all five release blockers merely because core algorithms pass.

## November 4 — dependency/pin provenance (step one)

Verified embedded OpenPGP.js matches npm 6.3.2 distribution after outer whitespace trimming, package SHA-512 and both registry signatures. Sparrow 2.5.5 pin matches its GPG-authenticated manifest and publisher's complete fingerprint. Tails 7.16 official HTTPS metadata differs from both existing pins; no images/signatures/boot tested. Electrum 4.8.3 binary and signature fetches returned HTTP 403; pin remains unverified. Added DEPENDENCY_PROVENANCE.md and source receipts. No tool/hash/ZIP changes. Next: close remaining artifact verification (including extra unversioned Ian Coleman pin) and perform offline/UI repairs before packaging. Downloads stay blocked.

## November 4 — offline controls and Tails verification

Repaired local-only/explicit-offline gating, reconnect password/results clearing, stale decrypt results and delayed crypto/FileReader repopulation. Corrected tool messages and dice input count. Core crypto tests, 40 network-state cases and shipped-controller DOM-double regressions pass. Both Tails 7.16 images downloaded, hashes matched official metadata and detached signatures verified with publisher-linked key; corrected IMG/ISO pins. Electrum official requests still return 403. See OFFLINE_CONTROL_REPAIR.md and signature receipts for limitations/import diagnostic. Browser/target-Tails testing, Electrum/Ian Coleman authentication and atomic packaging remain open. Bundle/manifest unchanged; downloads stay blocked.

## November 4 — Ian Coleman verification and candidate packaging

PR #17 Pages run 41917775493 succeeded; main c0a8e5a0964962218b5360986d339c204c23e1b5 and no open PRs at start. Ian Coleman 0.5.6 exact HTML hash matches authenticated release checksum; publisher-linked public key signature passed. Corrected its Python pin and replaced destructive wipe-drive advice with preserving backups. Electrum AppImage/signature requests still return HTTP 403; no authentication claimed. Added deterministic internal candidate builder and consistency/tamper tests; candidate stays outside published docs and downloads remain blocked. All available core/UI-state/network/routing/source checks pass. See REMAINING_TOOL_GATES.md for five-step status, provenance and exact limitations. Browser/mobile/target-Tails testing and Electrum remain release blockers; published ZIP/manifest/verifier are intentionally unchanged. Next: obtain official Electrum artifact/signature, complete actual browser/offline tests, rebuild candidate after any changes, then publish reviewed artifacts together. No production changes.

## November 4 — Electrum blocker resolved

Uploaded 4.8.3 AppImage verified successfully against all five official-site-linked signing keys. Corrected the stale SHA-256 pin to aabe3bb2c99ffca172a004b0fd6f4afdf1b204079f7691b65f23bc5b63a9de0c. Preserved keys/signature/GPG receipts; no binary execution or repository binary upload. See REMAINING_TOOL_GATES.md for scope and fingerprints. Removed Electrum from internal candidate blockers. Browser/target-Tails tests remain required before public bundle release; production untouched.

## November 4 — public-review warning and backup-message correction

Baseline 8af048577a4f1db6cc24b919b1b59a933b0b5f43; no open PRs. Replaced the standalone Python encryption tool's immediate deletion message with preserving the original until saved-file decryption and recovery backups are verified; bumped its displayed version. Added an above-the-introduction homepage public-review notice and removed the invitation to use test funds during this review. Updated Downloads to distinguish completed upstream provenance from outstanding browser/Tails testing and unreconciled published artifacts. Earlier emailed/community ZIPs are unchanged historical candidates and still contain the old message; they must not be represented as this revised standalone file. No archive/manifest republishing or production changes. Browser visual review remains outstanding.

## November 4 — feedback questionnaire

Created and published eight-question Google Form in the user-created form 11BcGn-gos7JW7a8DivaHDlAxadTYApSSjacR4rAzsy0. Required page, path, category and description; optional impact, device/browser, review coverage and follow-up contact. Email collection off, limit-to-one off, response summaries off. Public responder link: https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform . One labeled TEST RESPONSE submitted successfully and confirmation verified; exclude it from analysis. Added homepage link and HTTPS staging-only footer link through shared JS, with no third-party embed or background requests. Offline tools unchanged. Page-context prefilling is not implemented; questionnaire asks for page https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform/name. Source/path and JS checks pass; browser form submission verified, no full-site/mobile regression claimed. Production unchanged.
