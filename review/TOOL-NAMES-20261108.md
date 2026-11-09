# Tool names: finding from the Windows r4 test

Status: prepared for the next versioned package; leave the active r4 release intact.

The tester could not find “Diceware mapper” because the fingerprint checker called it “Passphrase mapper (this site)”. The map tool also used “Descriptor tool” in its heading and dropdown but “Wallet-map tool” in its tab. This is a naming/usability defect; it does not invalidate an observed matching checksum.

| Standard display name | Stable filename | Meaning |
| --- | --- | --- |
| Dice converter | dice-converter.html | 24-word BIP39 test converter |
| Wallet-map tool | descriptor-tool.html | Encrypt and restore a wallet-map file |
| Diceware mapper | diceware-mapper.html | Six-word passphrase lookup |
| Fingerprint checker | fingerprint-checker.html | Compare file hashes |

Use these display names in tool headings, browser titles, checker choices, download labels, offline START links, instructions and Google Form descriptions. Show the exact stable filename beside checker choices and in the tools. Keep “descriptor” and “passphrase” when explaining the underlying concepts, not as alternate names for the same tool. A demo adds “demo” to the matching tool name.

The naming patch updates visible labels and the checker’s built-in hashes. Tool logic, wordlist and Python files stay unchanged. Existing URLs/filenames and historical screenshots remain valid. Current r4 instructions retain an explicit old-label mapping.

Before merging/publishing: allocate a new release directory/version and rebuild all archives/manifests. Do not overwrite r4 while its physical tests are in progress. Reconcile the static instruction version labels and current download links for that new release. Preserve r4 evidence, then verify the new package and repeat the fingerprint/label checks. No broad cryptographic retest is claimed by this patch.

Google Form wording should use the same display names and filenames. The form’s legacy T2 questions and upload-field placement are separate outstanding edits; this patch does not change the external form.
