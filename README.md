# Plebum Dominium — staging repository

This is the **test/staging** repository for PlebumBTC. It is not the production release source.

- [Staging website](https://musthavemustash.github.io/plebum-dominium-test/)
- [Production website](https://plebumbtc.io/)
- [Proposed release policy](RELEASE_POLICY.md)
- [Release checklist](RELEASE_CHECKLIST.md)
- [Changelog](CHANGELOG.md)

## Release governance

Standard release window: every other Tuesday at 10:00 a.m. Eastern, starting November 17, 2026 (proposed). Routine cosmetic changes are batched; versions follow Semantic Versioning. **Nothing may be merged to production without the maintainer's explicit, release-specific approval.** Staging changes never auto-promote to production.

This repository is a preview sandbox. Its site generator must use the GitHub Pages project base path `/plebum-dominium-test/` when generating a preview; do not assume the production root URL.

## Authoritative staging source

This is a buildless static site. **Edit `docs/` directly.** GitHub Pages publishes that directory, including its assets, handouts, path variants and tools. The root HTML, `content/`, `templates/`, and root `assets/` are historical inputs and are not used to regenerate staging. Do not copy them over the reviewed site. The former generator is available in Git history if needed for a deliberate future migration.

Run `python3 scripts/build.py` to validate local links, required files and the staging base path. It does not delete or rewrite files. `--base /plebum-dominium-test/` is accepted for compatibility; other base paths are rejected. The validator does not certify custody guidance, external links, accessibility, downloads or recovery: those require their own review.

Use the available browser preview workflow for `docs/` at the staging project base path. Commit verified changes to a staging PR, then confirm Pages deployment after merge. Track overnight progress in `review/OVERNIGHT_PROGRESS.md`.

### Independent path pages

`docs/handouts/` and `docs/choose-path.html` remain the reviewed source. `scripts/render_paths.py` creates only the navigation wrappers in `docs/paths/one/` and `docs/paths/three/`, plus route-specific search indexes. Edit the source handout, then run `python3 scripts/render_paths.py`; do not edit generated path copies. This renderer does not use the historical Markdown/templates. `scripts/build.py` rejects stale path copies without rewriting them. Run `python3 scripts/test_paths.py` to check every numbered navigation edge and runtime/static sequence parity.

Both routes preserve Terms → Before you begin (Threat Model) → Pick your path. The remaining sequence follows the existing guide order, omitting the other route's exclusive sheets. One-key variants are used for Checklist, Dice, Titanium, Inheritance, FAQ, and Recovery card. Two devices remains an optional reference, outside both numbered sequences. Per-route completion records intentionally do not import ambiguous historical checkmarks.

## Tested download snapshots

The November 8 r4 Windows short retest is closed; see [the closeout](review/WINDOWS_R4_CLOSEOUT.md). The November 9 physical Tails short run passed the observed checks on the complete r4 archive; see [its results and limits](review/TAILS_R4_RESULTS.md). The focused r4 ZIP and both larger r4 archives remain immutable snapshots. Current status and result notes are separate live addenda. Do not rebuild or overwrite a tested release ID to publish status changes.

The Pages workflow now validates and publishes committed site files and packages without invoking package builders or creating a bot commit. For a future package release, assign new versioned output paths in the builders, assemble and validate all archives/manifests/verifier references together, then commit them in the reviewed staging PR. New files do not inherit older physical-test passes. The unmerged naming cleanup remains separate.

## Content standard

Plebum Dominium teaches self-custody without a hardware wallet. Create and verify keys with offline software, record the backups on metal, verify recovery, and sign with offline software. Hardware wallets are optional signing tools only after the metal backups are complete and checked. Use the existing backed-up keys. Neither path may require a hardware purchase for setup, signing or recovery. This rule applies to guides, equipment lists, diagrams, downloads, metadata, search, news and future copy. **Testing scope clarified by the maintainer on November 9, 2026:** T6/T7 test setup, offline-software signing, recovery and handover with disposable paper records. Metal comes after testing; metal fabrication/read-back is not part of these tests or their beta pass criteria. Do not reintroduce a metal prerequisite into test instructions. The permanent-backup stage of the custody guide is separate from this public test. See [the content review record](review/SOFTWARE_FIRST_CONTENT.md).
