# November 13 Windows browser evidence and print correction

## Problem and change

The one-key Before you begin page printed its path label on a nearly blank
first page, with the heading starting on page 2. The global print rule forced
every h1 onto a new page; its first-child exception missed headings preceded
by a path label. Remove that forced break and keep the label and heading with
the following content. The shared print stylesheet serves both guide routes.

The testing page and Downloads now link the scoped Windows session report and
25-screenshot checklist. The report preserves the observed print failure,
original PDF identity, exact r2 ZIP identity and unperformed checks. Raw photos
and their unrelated device/profile details are not published.

## Validation

All 16 required repository checks passed locally:

- `python3 scripts/reconcile_tool_downloads.py --check`
- `python3 scripts/test_download_consistency.py`
- `node scripts/test_download_verifier.cjs`
- `node scripts/test_public_session_state.cjs`
- `node scripts/test_tool_network.cjs`
- `node scripts/test_dice_validation.cjs`
- `node scripts/test_search_focus.cjs`
- `node scripts/test_diceware_mapper.cjs`
- `node scripts/test_fingerprint_checker.cjs`
- `python3 scripts/test_tool_core.py`
- `python3 scripts/release_checksums.py check`
- `python3 scripts/test_release_checksums.py`
- `python3 scripts/build.py`
- `python3 scripts/test_paths.py`
- `python3 scripts/test_page_test_modules.py`
- `python3 scripts/check_offline_downloads.py`

- All 150 files already tracked under docs/testing at base commit
  6a36a219025a234ea9e9839fa6c1565f46b2bcaf remain byte-identical.
- The original failed print PDF still matches its recorded SHA-256.
- The corrected guide loads in the browser preview. The new results disclosure
  renders legibly and its anchor opens it. Ctrl+P did not expose a print dialog
  in this preview browser, so no corrected paginated output is claimed.
- The Windows print retest remains pending on both guide routes, with the same
  recorded settings and new RETEST evidence. The broader print audit is open.

## Package boundaries

The published r2 archives and their manifests/checksums are unchanged. A
scratch rebuild includes the corrected stylesheet and, in the complete package,
the new results. The cumulative live-addendum inventory pins the exact rebuilt
hashes and changed members (22 complete, 3 tools-only); existing packages do not
inherit the correction or new test claims. Package reproducibility and all
existing guardrails pass without rewriting a published ZIP.

This draft targets staging only. It does not merge, deploy, sign a release,
complete T1-T7, or authorize beta/production.
