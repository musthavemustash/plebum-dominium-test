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
