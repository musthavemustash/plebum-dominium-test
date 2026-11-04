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
