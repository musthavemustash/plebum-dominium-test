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
