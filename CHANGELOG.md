# Changelog

Production releases will use Semantic Versioning and follow the staging-first release policy in [RELEASE_POLICY.md](RELEASE_POLICY.md).

## Unreleased (staging only)

- Added reproducible public-vector and encryption compatibility tests plus tool-provenance findings. Core tests pass; download release remains blocked by provenance, version pins and offline/UI issues.

- Removed the preselected-path shortcut above the chooser options on both routes.

- Revised FAQ variants, briefing, single-sig, optional two-device guide and path-risk comparison. Corrected 2-of-3 compromise and passphrase migration claims. Downloads now flags five manifest mismatches and legacy documents pending reconciliation.

- Revised signing, testnet rehearsal and map-encryption guides with responsive sections, complete transaction-output checks, disposable-wallet recovery practice and explicit encryption recovery limitations.

- Revised both paths’ checklists, durable backups, inheritance guidance and recovery cards into readable responsive sections. Clarified secrets versus configuration, safe backup checks and empty-wallet troubleshooting; removed automatic paper-destruction and backup-copy prohibitions.

- Proposed biweekly Tuesday release window (10:00 a.m. America/New_York).
- Proposed Semantic Versioning, batched cosmetic changes, and explicit approval before production merge.
- Added a reusable production release checklist.

**No production version has been assigned and no production release is authorized by this changelog.**

## Unreleased — staging QA patch

- Keep mobile header controls on screen and improve drawer keyboard access.
- Align Threat Model navigation and summary behavior; clarify recovery wording.
- Make Sparrow commands copyable without shell prompts and align the verification overview.
- Record browser QA and outstanding release blockers in `review/STAGING_QA.md`.

## Unreleased — preserve reviewed staging source

- Make the buildless `docs/` site authoritative; replace the obsolete destructive generator with non-mutating staging validation.
- Check local references across all 65 HTML pages, reject a custom-domain CNAME or non-staging base.
- Repair six malformed or incorrectly rooted references across dice-easy, inheritance variants, file verification and dice rolls.

## Unreleased — independent staging paths

- Add URL-addressable one-key/passphrase and three-key routes with matching sidebar, header, top/bottom navigation, and consecutive numbering.
- Preserve the requested Terms → Before you begin → Pick your path order; select the correct one-key variants, including Inheritance.
- Remove hidden-content path gates; old handout links resolve to a usable route or readable optional reference.
- Keep route selection in the URL, isolate completion records, and provide route-specific search results and numbering.
- Replace the path chooser's dynamic empty panel with native links and two readable cards; remove its unsupported incident anecdotes.
- Add a bounded path renderer and stale-copy validation without restoring the historical destructive generator.

## Unreleased — homepage and glossary

- Replace the dense homepage comparison with responsive cards, balanced custody tradeoffs, and a Terms-first entry point.
- Remove unverified news headlines from the homepage ticker; the separate news archive still needs review.
- Expand Terms to twelve definitions with local filtering, explicit recovery context, and BIP39/PSBT references.
- Correct the signing-threshold demo: retain verified wallet configuration even when all three seeds are available.
- Align the path pages' mobile position label with their existing route numbering; regenerate path copies and search indexes from reviewed sources.

## Unreleased — verification and offline-session guidance

- Rework Check the files and Two boots into readable responsive cards with native explanatory disclosures.
- Distinguish file integrity from signer identity and software trust; remove the production-domain-only safety claim.
- Clarify Tails Offline Mode, shared hardware risks, secret-free transfer files, and shutdown limitations.
- Fix one-key dice instructions that mistakenly requested three seeds; correct BIP39 last-word/checksum explanations and incompatible cross-tool input assumptions.
