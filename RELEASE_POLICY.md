# PlebumBTC release policy (staging proposal)

Status: **Proposed in test repository only.** This document does not authorize a production deployment.

## Release cadence
- Standard production release window: **every other Tuesday at 10:00 a.m. America/New_York**.
- First proposed window: **Tuesday, November 17, 2026**; subsequent windows every 14 days.
- The window is an opportunity, **not** an automatic deployment. Skip it when there are no approved, verified changes.
- No unattended scheduled production deployment.

## Versions
Use **Semantic Versioning**: `vMAJOR.MINOR.PATCH`. The initial baseline version is **TBD**, to be agreed after examining existing production tags; do not assume v1.0.0.
- MAJOR: incompatible behavior, verification format, or tool interfaces.
- MINOR: new features or substantial backward-compatible enhancements.
- PATCH: bug fixes, cosmetic changes, copy edits, and corrected educational guidance that do not change interfaces.
- Security urgency is independent of version increment. Record separately maintained tool versions where appropriate.
- Staging candidates may use `-rc.1` prerelease suffixes; only approved production releases get stable tags.

## Cosmetic changes
Bundle routine visual and editorial adjustments into the next standard release. Do not publish individually merely because they are complete.

## Exceptional releases
Critical security errors or unsafe custody guidance: expedite as soon as corrected and verified. Important functional failures: target 24–72 hours when feasible. Exceptions still require explicit maintainer approval, checks, and a production PR.

## Mandatory release gates
1. Implement and preview changes in **musthavemustash/plebum-dominium-test**. Confirm staging URLs and asset base path `/plebum-dominium-test/`.
2. Record scope and user-visible changes; group routine cosmetic edits.
3. Create a production release candidate from reviewed changes; verify content, build, downloads, hashes, offline behavior, and GitHub Actions checks.
4. Present a release summary, preview links, version, and rollback plan.
5. **Obtain explicit maintainer approval for that specific release before merging any production PR.** Approval of this policy is not approval of a release.
6. Merge only via protected production PR; GitHub Pages auto-deploys on production main merge.
7. Confirm live deployment, fingerprint integrity, and critical paths. Keep release tag, manifest, changelog, commit SHA, and a tested rollback procedure.

## Safety boundaries
- **Do not push, merge, tag, or deploy production without explicit approval.**
- No test repo change automatically syncs into production.
- Production deployment credentials must not be added to staging.
- Release schedule is documented policy, not a scheduled task or automation.
- Emergency releases still require explicit approval and evidence.
