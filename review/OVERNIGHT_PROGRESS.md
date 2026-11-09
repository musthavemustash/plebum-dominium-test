# Overnight revision progress

Target: November 4, 2026, 11:00 a.m. America/New_York. User authorized tested staging merges/deployments throughout the overnight revision. Production changes are forbidden.

## Completed

- PR #5 merged at `6fe693e3e16798796135a808c26f45046b1cd8e6`. GitHub Pages run 41775629841 succeeded. Public Threat Model top Next link and interactive summary verified; public Sparrow commands have no shell prompts and overview shows seven steps.
- Browser QA of Threat Model and Sparrow: desktop plus 320/390px iframe mobile layout. Details in STAGING_QA.md. Remaining actual device/recovery checks are not certified.
- Current batch makes `docs/` the authoritative static source. `scripts/build.py` now validates without deleting or rewriting content. Historical root copies and Markdown/templates are not staging build inputs. This resolves accidental regeneration regression without claiming all historical copies are aligned.
- Validated all 65 HTML pages for local reference destinations and staging base paths. Corrected six broken references across dice-easy, inheritance-one/easy, verify, and dice-rolls.
- Verified validation leaves every byte of `docs/` unchanged, and rejects production base, CNAME and missing required CSS.

## Next work

1. Confirm the preserve-reviewed-site PR merged and its Pages deployment succeeded. Do not duplicate its changes if still in progress.
2. Audit and revise the homepage, Choose your path and Terms. Preserve the site identity, use concise responsive sections and accessible interactions. Verify categorical security claims (especially “most secure” and resistance to compromised devices) before keeping them.
3. Continue in guide order: Checklist, Two boots, Check the files, Make the keys; then Practice spend, Metal and the map, Testnet, Encryption; then Inheritance, FAQ, Briefing, Recovery card, Single-sig, Two devices. Cover one/easy variants too. Some variants are legacy; inspect actual navigation rather than assuming all are active.
4. Review supporting pages and tools: downloads/verification, newcomer education, news accuracy, beyond, demos. Do not weaken offline enforcement or change cryptography without appropriate validation.
5. Finish site-wide navigation, mobile, keyboard, theme, search, download and print review. Keep factual custody uncertainties explicit. Check descriptor recovery and version-pinned instructions using authoritative references; actual wallet recovery has not been exercised.

## Work coordination

Use a staging branch per coherent batch and fresh main. Read this log and open PRs before starting. Update this file on each batch with verified results and next remaining pages. Do not overwrite parallel edits. No production deployment is authorized. Overnight task runs hourly midnight through 10 a.m.; a separate 11 a.m. report summarizes actual completion.

## Coverage inventory

Threat Model and Sparrow: reviewed and revised. Other pages: local link checks only unless a later entry says otherwise. A successful link check is not a content or visual review.

Observed during link QA: the Check the files page still has a production-domain-only warning on staging, a stale “Next, Two boots” sentence, inconsistent section count, and signature/hash trust explanations that need content review. These are not covered by the link-only repair. The repaired verify-page link was clicked in the local browser and opened the functional file-checker page.

## November 4 — independent-path batch, ready for staging PR

- Confirmed PR #6 is merged and its Pages run succeeded. Source/generator drift blocker is resolved for the reviewed docs; historical source files remain non-authoritative.
- Resumed the unfinished local `staging/independent-paths` work. No open PRs or newer remote main were found. User's correction is authoritative: Terms, Before you begin (Threat Model), Pick your path, then the existing guide order for the selected route.
- Added 12-page one-key/passphrase and 16-page three-key routes, route overviews, static Previous/Next and sidebars, correct variants, isolated completion keys, old-link resolution, and path-specific search indexes. Content is never hidden behind “not on your path.”
- Navigation source is `scripts/render_paths.py`; reviewed content remains `docs/handouts/` and the chooser. After any source edit, render paths and run build/test_paths checks. The build validator now rejects stale copies. Do not regenerate from historical Markdown/templates.
- Automated route checks and the 95-page local link validator pass. Browser preview was blocked by browser security policy; runtime/mobile/browser verification is still due. Do not report it as completed.
- The entry-page refresh is preserved separately in LOCAL branch `staging/entry-pages-refresh`, commit `584827b`, and is not deployed. Do not blindly cherry-pick its main.js or chooser changes over this navigation work. Integrate the homepage/glossary content selectively, keeping the new routes and user-requested order.

### Next run priority

1. Confirm this batch's PR and Pages deployment; verify the live routes in a browser if access becomes available. Test path switching, search, independent progress, mobile menu, and both complete Previous/Next chains.
2. Finish homepage and Terms refresh from the preserved work; keep navigation intact and rerender path copies.
3. Continue the outstanding handout/security and supporting-page inventory above. Neither full-site revision nor actual custody recovery testing is complete. No production changes are authorized.

## Independent-path deployment confirmed

PR #7 merged as `434f27b37f98c0a77f838730519f85d8ef3ef71a`. GitHub Pages run [41812171757](https://github.com/musthavemustash/plebum-dominium-test/actions/runs/41812171757) completed successfully on November 4. Published route overviews: https://musthavemustash.github.io/plebum-dominium-test/paths/one/index.html and https://musthavemustash.github.io/plebum-dominium-test/paths/three/index.html . Public web retrieval of both URLs returned a tool access error; live rendering and interaction are not independently confirmed. Browser testing remains the first next-run task. Local search-index checks additionally confirmed 12/16 entries, correct ordering, and route-local URLs.

## November 4 — homepage and glossary batch

- Confirmed PR #8 main and successful Pages deployment; no open PRs at batch start.
- Integrated preserved homepage and Terms content selectively. The homepage starts at Terms and uses readable cards with balanced tradeoffs; the glossary has 12 definitions and local filtering. The main navigation controller and user-requested page order remain intact.
- Corrected the key-threshold demo so it never claims three seeds automatically reconstruct all configuration. Removed unverified headline ticker from the homepage; news.html still requires its own factual audit.
- Fixed the remaining stale mobile position numbers in generated path pages and overview pages. All path copies/search indexes regenerated from the canonical handouts.
- `node scripts/test_entry_interactions.js` covers filter states and key demo/reset using DOM doubles; path checks and 95-page link/drift checks pass. These are NOT browser tests. Browser/mobile/live visual QA remains outstanding after the earlier policy block.
- The remaining content from local WIP `584827b` has now been considered for homepage/Terms; do not reapply its obsolete chooser or navigation code. Path-risk wording from that WIP remains to review.

Next: confirm this batch's PR/Pages status, then prioritize Check the files, Two boots, and key-generation handouts for safety accuracy and path-specific clarity. Remaining supporting pages, downloads, news, and tools still require review. Full-site completion and wallet recovery validation are NOT claimed.

## November 4 — verification and offline-session batch

- PR #9 merge `77b479ccb0fc1c1c9e8653c74acc31f49ee4e5b9` and successful Pages deployment confirmed. No open PR or overlapping remote batch found.
- Revised Check the files and Two boots with responsive cards, signer/source/integrity distinctions, explicit no-secret transfer rules, Tails Offline Mode, and shared-hardware/shutdown limitations. Removed stale prose Next destinations while preserving route order.
- Corrected dice and dice-one checksum/input-method explanations. dice-one no longer creates three seeds. Narrow correction only on legacy dice-easy. Both routes and their search indexes regenerated; navigation, link/drift, and existing interaction-logic checks pass. Browser/mobile and real custody execution remain unverified.
- Official Sparrow page now lists 2.5.6 while kit instructions pin 2.5.5. Do not silently update version labels without coordinating binaries, signatures, hashes and compatibility review. Tails installer page lists 7.16, while checklist variants contain older lower bounds.
- Cross-tool entropy equivalence is an outstanding validation requirement, not a proven procedure. Revised text says to stop if input methods cannot be matched. Cryptographic code and offline boundaries were not modified.

Next: confirm this batch deployment; review Checklist variants and backup/recovery/inheritance instructions. Downloads/kit versions, tools test vectors, news and remaining supporting pages still need their full reviews. Browser QA is outstanding for all batches after PR #6. Do not claim the site is fully revised or ready for production.

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

## November 4 — chooser shortcut removal

User requested removal of the Continue with Three keys link above the path options. Removed its generator insertion for both routes, regenerated pages/search indexes, and verified absence on both chooser variants. Existing path-option links retained. 95-page validator and 28-step route regression passed. Browser visual verification remains unavailable. Staging only; confirm this batch Pages deployment on next run.

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

## November 4 — public tester task checklist

Added test-the-site.html with seven concrete tasks, expected results, PASS/FAIL/NOT TESTED reporting, a report example and direct questionnaire links. Linked from homepage and online guide footers. Clearly separates browser/read-only review from advanced physical Tails tests and calls for a refreshed candidate before advanced work. No offline tool or production changes. Static/source/route checks and JS syntax pass; full mobile testing remains outstanding.


## November 5 — public testing alpha

Published a separate, versioned tool-test ZIP with public fixtures, expected outputs, package checks and feedback instructions. Downloads now explicitly welcomes testing while retaining the real-wallet restriction. Source tool bytes and production are unchanged. Packaging and automated tool checks pass; six existing generated-route/index mismatches remain unchanged. See [PUBLIC_ALPHA_2026-11-05.md](PUBLIC_ALPHA_2026-11-05.md) for evidence and limitations.

## November 7 — visual file-verification guide

- Integrated the approved diagram preview into canonical Check the files, preserving site navigation and both custody paths. The three guide views explain the source/signer/contents checkpoints, the four example verification files, and stop/continue outcomes.
- Kept examples explicitly illustrative, including full 64-character hashes and an interactive mismatch. Publisher-key identity precedes reliance on signed checksums. Direct-file signatures remain a documented alternative; no success state certifies software safety or custody readiness.
- Scoped CSS and JavaScript to this sheet. Retained existing theme controls, added keyboard tab navigation, static instructions without JavaScript, paper-friendly styles, and separated public kit downloads from upstream verification instructions.
- Regenerated both route copies and search indexes. Local checks pass for 96 HTML pages, 28 route pages plus two overviews, and extracted complete/tools-only packages (202/71 checksum entries before the publication workflow refreshes alpha metadata). Offline checks preserve sensitive-tool bytes and close local links; diagram assets are local.
- Browser QA exercised guide views, file-role selection, mismatch and unknown-key outcomes, light/dark themes, both route navigation states, and a 390px mobile frame. Print styles and no-JavaScript fallbacks were source-reviewed, not physical print or device tests.
- User authorized test-site deployment only. Production is separate and unchanged. Main's existing publication workflow rebuilds current download packages and deploys Pages after merge; do not claim deployment until that run completes successfully.

## November 7 — optional page testing modules

- Added collapsed "Help test this page" panels to all 30 canonical handouts, Choose your path, all 28 numbered route pages, and both path overviews. The catalog defines 69 page-specific tasks with expected results and evidence suggestions; reused sheets retain stable task IDs across paths.
- Reporting links use the existing Google Form's General website feedback branch. They prefill the actual public page URL, task IDs, website source build, and an observation template. Outcomes, impact, feedback type, and repetition remain unselected. Full T1–T5 suites remain separate; site-build identity does not identify tool bytes, so tool reports also request the package filename and hash.
- Native details work without JavaScript. Scoped styles support light/dark themes, keyboard focus, and narrow layouts. Tasks use public fixtures or fictional records; the links never derive local file paths. Offline readers are told to finish testing before reconnecting to report.
- Validation passed: 96 static HTML pages, existing path/navigation checks, panel routing/idempotence checks, and both complete/tools-only offline package checks. The panel regression check also inspects all 61 panels in the rewritten complete offline ZIP for exact public URLs, build IDs, task IDs, and unselected outcomes. Sensitive tool bytes remain preserved by the existing package checker.
- Browser QA confirmed expansion, keyboard activation, readable desktop/light and 390px/dark layouts, the General feedback form branch, selected page area, prefilled public URL, and unselected feedback type/impact. No form response was submitted.
- Publication stamps the merged source commit once before rendering and packaging; rendering then reads that persisted stamp rather than the moving Git HEAD. Local validation used base 8a69215dae7d0646969eef61f4814ada0a709e9a; the staging publication workflow must regenerate final metadata and packages. User authorized deployment to the test site only.

## November 7 — rehearsal before durable backups

- Reordered the three-key route: Build the 2-of-3 → Set up a test wallet → Practice spending and recovery → Back up your keys and wallet map → Protect the wallet map. Runtime/static navigation, numbering, overviews, search indexes, shared sidebars and canonical onward links follow the same sequence; existing page URLs remain stable.
- Narrowed test-wallet setup to the chosen network, disposable keys, temporary seed records and complete configuration. Moved recovery into the spending sheet, including distinct signer pairs and missing-seed/map scenarios using copies while preserving original test records.
- Clarified that the earlier build sheet explains the structure before hands-on test setup. Its fixed mainnet derivation example is labeled as a reference, and test-wallet users must follow their selected network's documented settings. Practice records remain available for the following backup/map exercises; later intended wallets need fresh keys and verification of their own records.
- Renamed the durable-backup and map-protection headings. Updated page-specific testing tasks to match the moved content, while preserving task IDs and the source-build reporting context. No signing or encryption tool implementation changed.
- Checks passed for 96 static pages, all route/navigation edges and runtime parity, all 61 page-testing panels and offline equivalents, both offline archive/link/preserved-tool checks, JavaScript syntax and whitespace. Independent content review found no remaining blocker after the record-retention fix.
- Browser QA followed Next from test-wallet setup through spending/recovery, durable backups and map protection. The updated labels and step positions were readable on desktop and a 390px frame. These are content/navigation checks, not executed wallet transactions or physical-device recovery tests.
- Deployment authorized for the test site only; final source stamp and offline packages are refreshed by the publication workflow after merge.

## November 7 — simpler tester-page introduction

- Made Before you begin the first section after the page title. Removed the early action-button stacks and jump-link row; preparation now uses inline links and distinguishes website feedback from tool testing.
- Wrapped each T1–T5 track and the stage update in separate native disclosures, all closed by default. General website feedback also starts collapsed. Preserved every original track Do/Report body; stage-update findings and evidence links remain available below the reporting section.
- Kept one primary reporting action near the bottom and repaired the contents links, including the old missing offline anchor. Native controls work without JavaScript and have visible keyboard focus.
- Validation passed for 96 static pages, both offline archive/link/preserved-tool checks, exact track-content preservation, first-section order, one primary action and closed disclosure states in both source and the complete offline ZIP. Mobile browser QA confirmed the first section, default closed states and keyboard expansion of T4 and the stage update.
- The cleaner mobile-navigation design is a separate downloadable preview; it is not included in this page-only test-site deployment. Production is unchanged.

## November 7 — approved compact page buttons

- Applied the approved actual-page preview to the in-page Previous/Next row: a small step count, equal destination cards on one mobile row, and a modest Mark as read action below. Full destination titles wrap; desktop link text is retained.
- Kept the existing header, sidebar, top step banner, path switch and bottom scrolling strip. Compared those HTML blocks across all 68 changed pages with the base commit: identical. main.css is unchanged, and main.js differs only in the two completion labels; completion storage and mobile navigation behavior are untouched.
- Scoped the new mobile rules with data-page-controls, refreshed asset versions, and regenerated both guide paths. First Home and final Review this path links preserve their original targets. No preview-only scripts, automatic scroll, export rewrites or demonstration content were deployed.
- Checks passed for 96 static pages, route edges/numbering/runtime parity, 61 live/offline page-testing panels, both offline archives and preserved tool bytes, JavaScript syntax, renderer idempotence and whitespace. Independent review found no blocker.
- Browser QA at 390px and 320px confirmed equal-width destination cards, full title wrapping, completion behavior, Next navigation, the unchanged bottom strip and equivalent-page switching to the other path. No custody-tool implementation changed. Deployment authorized for the test site only.

## November 7 — restored news ticker header

- Restored the original scrolling news header on all 68 pages with the shared site header, using 38 canonical pages and regenerated route copies. Links remain inside the staging base; the beginner link targets the existing beginner page. The Binance headline uses the current staging article title rather than the older conflicting headline.
- Retained the existing mempool.space BTC/USD feed and one-minute refresh. Invalid responses, failed requests, timeout and offline events hide the quote. Local-file and extracted offline guides do not request prices. No new feed provider or third-party script was added.
- Preserved Motion on/off, light/dark themes and the existing bottom mobile navigation. All headlines remain horizontally reachable without animation; repeated animation links are excluded from the keyboard sequence and accessibility tree. The ticker is excluded from print.
- Checks passed: scripts/test_news_ticker.cjs (68 ticker instances, destinations/fragments, duplicate focus handling, price refresh/failure/reconnect/local/offline), scripts/build.py (96 pages), scripts/test_paths.py, scripts/test_page_test_modules.py, scripts/check_offline_downloads.py, JavaScript syntax and git diff --check. Both offline packages were rebuilt and checked locally; the existing publication workflow rebuilds final packages after merge.
- Browser QA: desktop and 390px iframe, light/dark, live price, running animation, Motion off, keyboard access and a headline's article destination. Physical touchscreen gestures and printed output were not separately tested. Existing article reporting was not re-researched as part of this header port.
- Scope: test repository only. Production remains unchanged. Confirm final Pages workflow and live ticker after merge.

## November 7 — refreshed security news

- Replaced the preliminary October 29 Binance story with its November 3 company report, retaining the existing article anchor. Added the November 7 Chainalysis restoration and credential-exposure update and the November 2 Mercado Bitcoin theft report. Each entry links to the primary source and dates company statements, estimates and preliminary findings.
- Updated the latest headlines across all 68 shared headers, with five recent stories and the existing beginner link. Preserved ticker behavior, price handling and duplicate-link accessibility. Updated global news search records and included those shared records in both generated route indexes so the actual search interface finds the new articles.
- Validation passed: 97-page static build, route navigation, 61 page-test modules, 68 tickers, fragment destinations and whitespace. Compared every other changed HTML page outside its ticker block against the base commit: identical. Browser preview confirmed layout, new search results and navigation to the article anchor. No CSS or custody-tool code changed.
- Test-site publication only; the existing workflow rebuilds and validates offline downloads before deploying. Confirm workflow completion and live headlines after merge.

## November 7 — editorial news front page

- Replaced the long news feed with a full-width front page: a lead Binance story, latest developments column, three illustrated reports, supporting headlines and a compact historical archive. Kept the site's warm palette, serif headlines, shared header, ticker, theme and Motion controls.
- Moved all 14 full reports into linked static article pages with source links, dates, breadcrumbs and return navigation. The former ticker anchors still resolve to their corresponding front-page stories. Search in either guide route now opens the full report directly. Verified every original article body and source link was preserved.
- Added an original decorative SVG vault illustration with a slowly rotating dial and moving dashed lines. Motion off stops all three animations; reduced-motion preferences suppress the new animation. Other illustrations are static, local SVG markup. No image or animation library, external media or network dependency was added.
- Validation passed: 111 static pages, route navigation, 61 page-test modules, 82 shared tickers, duplicate IDs, all article destinations, whitespace, both offline packages and preserved custody-tool bytes. Full reports are included in the complete offline ZIP. Browser checks confirmed desktop light/dark layouts, working full-report navigation, Motion on/off and mobile layouts at 390px and 320px without page overflow.
- Scope: test site only. Existing publication workflow rebuilds final packages and deploys after merge; verify its result and the live news page.

## November 9 — Windows r4 run closed

The November 8 guided Windows short run passed within its documented scope. See [WINDOWS_R4_CLOSEOUT.md](WINDOWS_R4_CLOSEOUT.md) and the linked public results/Tails handoff. Original evidence is linked in response-sheet rows 11–14; no duplicate Form submission is needed. Current downloads/testing pages distinguish the tested focused archive from larger packages and historical Tails results. Physical Tails is the next session. Tested r4 files stay unchanged, and publication no longer silently regenerates those release IDs. This update is staging only; the naming-cleanup PR and production remain separate.


## November 9 — Physical Tails r4 short results

The observed short-run checks passed using the complete r4 archive. See [TAILS_R4_RESULTS.md](TAILS_R4_RESULTS.md) for package identity, passed cases, evidence limits and remaining work. The tester confirmed saved-image/text readability on USB; shutdown and complete evidence reconciliation remain pending. Testing/download pages and live instruction addenda now reflect this run. Historical candidate records, all versioned package snapshots and tool bytes are preserved. T5 acceptance and both full wallet rehearsals remain open. This is a staging status update, not beta or production approval.
