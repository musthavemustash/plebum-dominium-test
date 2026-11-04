# Changelog

Production releases will use Semantic Versioning and follow the staging-first release policy in [RELEASE_POLICY.md](RELEASE_POLICY.md).

## Unreleased (staging only)

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
