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
