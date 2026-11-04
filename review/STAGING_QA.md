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
