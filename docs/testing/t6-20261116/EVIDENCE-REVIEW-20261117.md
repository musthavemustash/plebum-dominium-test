# T6 and supporting evidence review — November 17, 2026

**Result: the reviewed uploads support the existing T6 PASS.** They also identify the release used by the clean run more precisely than the original closeout alone.

Source: [T6-20261115-r1-clean](https://drive.google.com/drive/folders/1Gsm2n4tb5r10yYxuIXYJjXxiCKYWX9yU), within the tester's supplied evidence folder. The direct folder listing returned 93 files: 89 images and four public wallet/transaction artifacts. This was a metadata inventory of the whole direct folder and a visual review of **11 selected images**, not a review of every image or every raw transaction. File contents and sharing permissions were not changed.

## Package association

Image 01 displays `plebum-complete-offline-tester-20261115-r1.zip`, 2,399,740 bytes, with signature and checksum PASS. Its displayed SHA-256 is:

`4533b49dbd5f3bc4776f654c622bff09f9bc2111e75693ed6eb5099924b49c63`

That matches the repository's published signed complete ZIP. Image 03 records the clean extraction's 231-file verification PASS. This ties the recorded T6 run to that package. It is screenshot evidence of the verification performed during the run, not by itself a new computation over the tester's USB archive or certification of every tool case in it. The later USB-backup review below independently hashes the uploaded complete archive and finds it byte-identical to the published ZIP.

## Images reviewed

| Image | Visible result |
| --- | --- |
| [01: T6-CLEAN-20261115-01-Windows-signature-and-ZIP-PASS.png](https://drive.google.com/file/d/101HQuUxljlZDkCFbnZMkbKPljwaBRBrk/view) | The verifier displays release signature PASS and ZIP checksum PASS for the complete 20261115-r1 archive; the displayed SHA-256 matches the published hash below. |
| [03: T6-CLEAN-20261115-03-Windows-package-verifier-PASS.png](https://drive.google.com/file/d/180S1ml-x457-Gz-HXRkWZ_haZoO6rkGo/view) | PowerShell displays PASS: 231 files match from the clean run folder. |
| [25: T6-CLEAN-20261115-25-Tails-receiving-addresses-baseline.png](https://drive.google.com/file/d/1RoHsjUXVhwF58JWeseMWIDP98SBjhmzG/view) | Baseline first three receive addresses and first change address are fully visible. |
| [32: T6-CLEAN-20261115-32-Tails-recovery-addresses-match.png](https://drive.google.com/file/d/1J5PumiHn4VG8Df01ACCmtx9Wap-X7Ub2/view) | The first three receive addresses and first change address match image 25. |
| [33: T6-CLEAN-20261115-33-Tails-missing-passphrase-different-addresses.png](https://drive.google.com/file/d/1CGaZFIBGndt8usMMITCcvmgxZrqG126U/view) | The wallet labelled NO-PASSPHRASE displays addresses different from the baseline. |
| [34: T6-CLEAN-20261115-34-Tails-wrong-passphrase-different-addresses.png](https://drive.google.com/file/d/1lueBBNH2iV3SsaBE3htorP5apqYbe7E4/view) | The wallet labelled WRONG-PASSPHRASE displays addresses different from the baseline and the missing-passphrase wallet. |
| [68: T6-CLEAN-20261116-68-Windows-first-spend-after-server-switch.png](https://drive.google.com/file/d/1Jt5LStUlTVTdk56l7M2kfKeh1RmusW5I/view) | First spend displays Testnet4, 11 confirmations, block 161806 and a 140-sat fee after the recorded server switch. |
| [80: T6-CLEAN-20261116-80-Tails-second-signing-addresses-match.png](https://drive.google.com/file/d/1EH5TQVCNaBG1rxFr2Q0PcSDcDMpZ449T/view) | The second signing wallet displays the same first three receive addresses and first change address as images 25 and 32. |
| [84: T6-CLEAN-20261116-84-Tails-second-spen-sign-file-reopened.png](https://drive.google.com/file/d/1M1dDDH9P-733LemzhRvm2zBKKhaHn0pA/view) | The reopened signed .txn displays the recovery transaction ID, completed signature and payment of 285,675 test sats. |
| [88: T6-CLEAN-20261116-88-Windows-second-spend-confirmed.png](https://drive.google.com/file/d/18pycMctgj_PF4atX6jH-kLcCKNKT6jJi/view) | The same recovery transaction displays Testnet4, two confirmations, block 161821 and a 110-sat fee. |
| [89: T6-CLEAN-20261116-89-Windows-final-zero-balance.png](https://drive.google.com/file/d/1_UiG7uojNmgCvZi39MzKNGiE2Mh7Dvmi/view) | The watch-only wallet displays zero balance, zero mempool balance and three transactions. |

The passphrase images show the resulting public addresses; they do not reveal or independently prove the secret input used. The supervised session observations supply that context. A screenshot of an opened transaction supports the saved/reopened checkpoint together with the recorded action and tester confirmation; it does not independently prove where every copy resides.

The verification warning's absence over the later session remains an explicit tester confirmation. Image 68 supports the accepted first-spend status after the server switch; it does not identify the cause of the original refusal. No new network transaction or independent chain lookup was performed for this upload review.

## Archive notes and limits

- The four non-image files listed in this clean folder are the first unsigned PSBT, first signed `.txn`, second unsigned PSBT and watch-only text export. They were inventoried, not decoded or cryptographically validated in this follow-up.
- `T6-CLEAN-Testnet4-spend-02-signed.txn` was not found as a standalone uploaded file in the clean T6 folder or the focused filename search. The later data USB backup review covered selected earlier evidence/package folders, not an exhaustive search of every backup directory. Image 84 shows it reopened, and images 88/89 show the final result. This is an archive-completeness note, not a reason to reverse the recorded T6 pass; retain the original USB copy.
- The listing includes repeated filenames for checkpoints 55, 65 and 74, plus both a `20251116` and `20261116` name for checkpoint 78. These have not been deleted, renamed or asserted byte-identical. Numbering gaps alone do not establish missing required tests.
- The related Windows browser/verifier folder listed 26 files, including the original print failure PDF/screenshots. No later print-retest artifact was located there during this review. The two retest PDFs previously supplied in the conversation were subsequently retrieved and reviewed below; they close the specific first-page defect for both routes. Wider print acceptance remains separate.
- T7, unperformed T1–T5 checks, wider print review and final release acceptance remain separate. No claim is made that all shared files are safe for public redistribution or that anonymous Drive access was tested.

## Integrity references for the reviewed image copies

These hashes identify the image bytes retrieved for this review. They are not hashes of the wallet software, transaction validation or a release signature.

| Image filename | SHA-256 |
| --- | --- |
| `T6-CLEAN-20261115-01-Windows-signature-and-ZIP-PASS.png` | `a05a306942f8ca604e39853daee3d1bebcc24b854658702c48d1caecef2026c3` |
| `T6-CLEAN-20261115-03-Windows-package-verifier-PASS.png` | `e82755f89597a44dc81b2453e9a429282f76d36fc9dad63f498fc0b416584743` |
| `T6-CLEAN-20261115-25-Tails-receiving-addresses-baseline.png` | `157af17361ca317723f089f16a4dc39f969a4b0bba460eac9df1bf5d528f8f73` |
| `T6-CLEAN-20261115-32-Tails-recovery-addresses-match.png` | `934d8fd857c14ac196e9b0f9875ed041ea6e5330c4f2ef2096c8eb7b265b1f39` |
| `T6-CLEAN-20261115-33-Tails-missing-passphrase-different-addresses.png` | `b7834edf768454f56b50d12da5af6c263c3dc09a0160b66c0754031e360f61f7` |
| `T6-CLEAN-20261115-34-Tails-wrong-passphrase-different-addresses.png` | `a112991c8ad3495d17e8d5159b4b3c01da04cbcba9441f1f5bcf715973914d6c` |
| `T6-CLEAN-20261116-68-Windows-first-spend-after-server-switch.png` | `30a2936e3421010a37be92723c9f92e5ea3c6afeb515b52ec74bcb7d62a231aa` |
| `T6-CLEAN-20261116-80-Tails-second-signing-addresses-match.png` | `25fc8f899310a6feb8ae2d4df3e6991a97cde724a9c8165d2e9aa2976a6cbb5a` |
| `T6-CLEAN-20261116-84-Tails-second-spen-sign-file-reopened.png` | `f74cbc8bf82c64782645b4b90d0cf900cc88e082668b39f376383c873261833c` |
| `T6-CLEAN-20261116-88-Windows-second-spend-confirmed.png` | `40a245a3871a1cde8bc611cf748b8a4a1d9760556c9ac6b2ccc3be8e9c6e5471` |
| `T6-CLEAN-20261116-89-Windows-final-zero-balance.png` | `7f68f27735e98206155fc83f225a84465a4978e7f47589cf86b8e676599a503e` |

## Additional Testing Files and data USB backup

The second supplied folder contains earlier Windows preflight and R3 material. The last supplied folder is the tester's **Data USB Backup**, whose inspected directory metadata dates to November 15. Selected earlier evidence and release folders were inventoried; the entire backup was not recursively audited. One pre-T6 folder listing reached the 100-file response limit and is treated as partial. Wallet/key backup contents were not opened or republished, and no blanket link to the USB backup is published here.

Five additional Windows images and four November 15 Tails images were downloaded, hashed and visually reviewed, bringing this follow-up to **20 selected images**, plus the two print PDFs below. Earlier result files remain dated records. A filename containing PASS is not treated as proof without examining its contents.

| Evidence | Observed result and limit |
| --- | --- |
| [PRE-T6-15: Windows Sparrow installer](https://drive.google.com/file/d/1zqU4ZKliKRS1pM-I1EeCTIwAOvx12l2g/view) | Sparrow Verify Download displays Craig Raw's signature, matched manifest hash and Ready to install for Sparrow-2.5.6.msi. This is the recorded preflight, not a new installer verification. |
| [PRE-T6-16: Linux archive verified on Windows](https://drive.google.com/file/d/13qluU2ae3UTyKvlG_7iJHrXNQDNX3ge5/view) | The corresponding successful signature/hash result is visible for sparrowwallet-2.5.6-x86_64.tar.gz. |
| [PRE-T6-26: r2 USB hash](https://drive.google.com/file/d/1eLeRqMWQ3QsmAfzhzCoS9RUBqxPWcDzv/view) | PowerShell's SHA-256 equals the r2 hash in the table below. |
| [PRE-T6-27: r2 extracted package](https://drive.google.com/file/d/1OlNx-LhSD0mwUhnCFdMPYkM2wiEZ5YPy/view) | The bare verify_package.py command fails to launch; retrying with py verify_package.py reports PASS: 233 files match. The corrected command, not the failed launch, provides the result. |
| [R3-T4: restored public map](https://drive.google.com/file/d/1PHBP4hZehbqRMPXmbpaWg9S8vRYzO5mk/view) | compare_files.py reports byte-for-byte equality between the public fixture and restored file in the R3 path. Edge's sidebar icon is visible; this does not establish the exact browser build or resolve every earlier browser label. |
| [TAILS-05: complete package check](https://drive.google.com/file/d/1OHU79Ok4wTSLdPOd4Tu4bpOeHsZEKLxQ/view) | All three ZIP checks say OK; after a misspelled command fails, python3 verify_package.py reports 231 files match. The uploaded filename retains its original 202611115 typo. |
| [TAILS-17: reopened one-key guide](https://drive.google.com/file/d/1TG0l0PmVOYm4Hfgx367bkzuGItC9-A2y/view) | The styled one-key guide is visible at the document-portal path. Reboot context comes from the existing helper session record, not this single image alone. |
| [TAILS-19: release fingerprint](https://drive.google.com/file/d/1uC7aQN1I3X4SJrrXjsY7gOr9LCyVgiF5/view) | The displayed public fingerprint is B9286C4A7CFF722E191D2D7566FB7D9AB51E417E. No secret key bytes or passphrase are visible. |
| [TAILS-20: manifest signature](https://drive.google.com/file/d/1YKRltgQeLAU9GZB-TDRwI2ypUbn20xsF/view) | GnuPG displays Good signature with the established fingerprint and its identity-trust warning. All three ZIP hashes say OK. |

The saved PRE-T6-SESSION-NOTES.txt was read as a historical November 13–14 snapshot. Its statements that T6 had not started are correct for that earlier snapshot, not the current status. These uploads corroborate the existing [R3 results](../r3-20261112/RESULTS.txt), [r2 preflight](../tails-pre-t6-20261115/RESULTS.txt) and [Tails helper/signing results](../tails-helper-20261115/RESULTS.txt); they do not represent new physical test runs.

### Archive bytes checked independently

The two older complete ZIPs were retrieved from Testing Files. The three November 15 ZIPs, manifest and signature were retrieved from the data USB backup's signing bundle. Each downloaded file is byte-for-byte identical to its versioned repository copy. The existing release-signature check was rerun successfully with the pinned public key; the copied manifest and signature are identical to the validated published pair.

| Archive | Bytes | Computed SHA-256 |
| --- | ---: | --- |
| `plebum-complete-offline-tester-20261113-r2.zip` | 2,995,499 | `1fbd6c9d92fdcfdf615db9a5b542b0294814b232775b9e2ce66bf52c785fa706` |
| `plebum-complete-offline-tester-20261112-r3.zip` | 2,941,973 | `99237d48a93979cc4e5190e8a1583bda5f31503873fe8d1ec4d937dec42cbf3f` |
| `plebum-complete-offline-tester-20261115-r1.zip` | 2,399,740 | `4533b49dbd5f3bc4776f654c622bff09f9bc2111e75693ed6eb5099924b49c63` |
| `plebum-tools-alpha-20261115-r1.zip` | 303,958 | `8bf9de1a5fce0b760ee8fac92af60fdbcf10d640019cbf656925f5129c9d071b` |
| `plebum-website-tools-only-20261115-r1.zip` | 1,586,165 | `6ef478793c6c002945401600abe434576bf4153f1b7bcfd272167346ef27116b` |

The uploaded manifest is 322 bytes, SHA-256 `a194d81afa3be6667a5e00c28d82ba189a1b7323565bbaf81682dd42f6b50f0f`; the detached signature is 833 bytes, SHA-256 `d39ade753b88eff3eeb151f7dc3318d13e82fad57f034947ff752f72e98bb555`. This authenticates the reviewed release bytes against the pinned release key. It does not prove every extraction on the physical USB is unchanged or pass every test in those archives.

### Additional image hashes

| Image filename | SHA-256 |
| --- | --- |
| `PRE-T6-15-Windows-Sparrow-2.5.6-installer-VERIFIED.png` | `b8eb51e8938c7a0db53e43c0d6bc5a89adc765c18f3736e52adc92553b190473` |
| `PRE-T6-27-Windows-USB-r2-whole-package-PASS.png` | `4712bf5febe7d6778a343ac284f41e1184b66048865dc2a56221ef00a18d0f17` |
| `PRE-T6-26-Windows-USB-r2-ZIP-SHA256-MATCH.png` | `35f30eb38ba134bf8227ddc814e99586aae16dac72488ce40a4ca9025b2af8cf` |
| `PRE-T6-16-Windows-Sparrow-2.5.6-Linux-archive-VERIFIED.png` | `5dce5cc49394ea2cea9230035b0efe3210b2714237120654bd450dd6629ea53f` |
| `R3-T4-map-byte-match-Windows.png` | `2e094ee1f962a013f632002bd8b3435eaf4f7dc452af1e7da95ea4ee5b5ec402` |
| `TAILS-20261115-20-Tails-Manifest-Signature-PASS.png` | `8370af3b3a65eabab603519d1476063378f060abdd57e63c0191ef4088df1ec9` |
| `TAILS-20261115-19-Tails-Release-Key-Fingerprint-Match.png` | `546b77b99fe20fd6c4ed38dc3d515f61b19012f7a29a58b37e2446aa0f89242a` |
| `TAILS-20261115-17-Tails-Reboot-One-Key-Styled-PASS.png` | `dc6b8d138e05484e73da831d5895d662e9aef556446a05842b272c94095fd20e` |
| `TAILS-202611115-05-Tails-Complete-Package-231-PASS.png` | `7b20dd7f1bb56cae97f3addd27323694b7668d629b7b1a1821d4bc4a4cca51db` |

## Earlier print retests recovered and reviewed

The original Windows evidence folder did not contain the later PDFs, but both had previously been supplied in the conversation. Their actual bytes were retrieved and both pages of each rendered and inspected on November 17. These are evidence of the November 13 retest, not newly generated handouts.

| Saved PDF | Route | Pages | SHA-256 |
| --- | --- | ---: | --- |
| `WEB-16-Windows-Chrome-Print-RETEST.pdf` | `paths/one/threat-model.html` | 2 | `3ac3d9d09f05f19106f38fc5e69a820fb6dff0575f0930c2806cb13625c11a0e` |
| `WEB-28-Windows-Chrome-three-print-RETEST.pdf` | `paths/three/threat-model.html` | 2 | `389cd9d8aaf1622c28d8faf07d2fac1e2ad3e869b34fc1febdb0b19e3fa24fbc` |

**PASS for the specific first-page pagination defect in both saved PDFs:** the path label, Before you begin heading and main content appear together on page 1. Both PDFs contain two populated pages with no visible clipping or overlap in the inspected content. The route and November 13 print time are visible in each PDF's header/footer. The original failed PDF and original session report remain unchanged.

This closes the recorded blank-first-page defect for those saved-PDF retests. It does not establish a physical paper output, every handout, expanded disclosure content, every browser, or the final release's print acceptance. The disclosure is collapsed in both PDFs. The evidence PDFs are not republished as current downloadable handouts.
