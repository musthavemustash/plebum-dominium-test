# Windows website and download-verifier checks, November 13, 2026

This is a focused Windows browser session. It is not a complete T1-T5 pass,
an offline-isolation test, or a wallet rehearsal.

## Environment and evidence

- Windows 10 22H2, build 19045.6456.
- Google Chrome 157.0.8103.79, Official Build, 64-bit, Stable.
- Live staging website; the separately saved download verifier also ran as a
  local HTML file. Local-file operation does not establish offline operation.
- Source baseline for review: merged PR #72,
  `6a36a219025a234ea9e9839fa6c1565f46b2bcaf`. The screenshots are observations,
  not independent authentication of that deployed commit.
- Flow: one action, public photo, review, assigned filename, native screenshot
  saved to the session Evidence folder, then the next action.
- The tester confirmed all 25 named screenshots and the print-failure PDF are
  saved. Review used the supplied photos and the actual PDF. The native PNGs
  remain with the tester and have not been independently retrieved.
- `EVIDENCE.csv` maps each filename to its actual observation. WEB identifiers
  are session labels, not form question IDs or full verification-track passes.

## Observed passes

- Homepage and Downloads navigation; three-key and one-key path selection
  with 16 and 12 steps; the shared Before you begin page stays selected when
  switching from three keys to one key.
- Search for `passphrase` returns relevant results. Shift+Tab from the input
  wraps to the email link, Tab wraps back to the input, and Escape closes
  the panel and returns focus to Search.
- Light-mode readability in the inspected viewport and light-mode persistence
  when navigating to Downloads. This is not a whole-site contrast audit.
- The complete r2 download finishes with its identified filename. The local
  verifier reports the correct archive size and SHA-256 match.
- Local-verifier Reset clears file/result/hash state. A public PDF reports
  no matching published checksum in both the live Downloads verifier and the
  saved verifier. Selecting the good ZIP after the PDF replaces the mismatch
  with the correct filename and match result, without Reset.

The negative test established a checksum mismatch for an unrecognized file.
It did not establish a dedicated file-type rejection, corrupted-ZIP rejection,
or all verifier failure cases.

## Identified ZIP: archive check only

Filename: `plebum-complete-offline-tester-20261113-r2.zip`

Size: 2,995,499 bytes

SHA-256: `1fbd6c9d92fdcfdf615db9a5b542b0294814b232775b9e2ce66bf52c785fa706`

This is the ZIP-check portion of T1 only. No extraction or root/subset package
verifier was run in this session. The match does not authenticate an unsigned
publisher reference or approve the package for real-wallet use.

## Print finding: FAIL, Windows retest pending

Page: `paths/one/threat-model.html` (Before you begin, step 2 of 12).

Chrome produced three pages: page 1 contained the path label and browser
headers/footers, while the heading and main content started on page 2. The
visible content on page 3 ended without obvious clipping. The nearly blank
first page occurred with both the selected printer and Save as PDF.

Recorded printer settings: Letter, one page per sheet, Default margins,
Default scale, 300 dpi. The PDF is Letter; its preview showed Default margins,
headers/footers on and background graphics off.

Cause found in the source: `h1 { break-before: page; }` forced the heading
onto another page. The `h1:first-child` exception did not match because the
path label precedes the heading. The proposed source correction removes that
forced break and keeps the label/heading with the following content.

The original failed PDF remains unchanged. This result stays FAIL until the
corrected live page passes the tester's repeat print check. The existing r2
ZIPs retain their original print stylesheet; the correction belongs to live
source and a future separately versioned package.

## Not tested in this session

Extracted-file verification, Python/GnuPG tools, sensitive-tool session gates,
full T2-T4 suites, physical Tails/T5, T6/T7 wallet setup/signing/recovery,
automatic network isolation, true offline browsing, mobile layouts, all guide
print pages and expanded disclosure content, or release signatures.

Beta remains pending the outstanding evidence and explicit release approval.

## Next physical check after the correction is merged and deployed

1. Reload the live one-key Before you begin page in the recorded Windows
   browser. Keep the earlier evidence unchanged.
2. Open print preview with the same settings. The path label and heading
   should appear together on page 1, followed by guide content.
3. Inspect every page for clipped/overlapping content and preserve the new PDF
   and screenshots with RETEST in their names. Record the observed page count.
4. Check the equivalent three-key page too. Report each route separately;
   a developer preview does not replace this Windows retest.
