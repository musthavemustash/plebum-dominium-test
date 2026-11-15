OpenPGP.js 6.3.2 (LGPL-3.0-or-later)

openpgp.min.js is the unmodified browser distribution from the official npm
package. Its npm SHA-512 integrity was verified before extracting the file.
PROVENANCE.json records upstream URLs and hashes of all redistributed files.

LICENSE contains LGPLv3; COPYING contains the incorporated GPLv3 terms.
openpgpjs-6.3.2-source.tar.gz contains the corresponding upstream source and
build instructions from the official v6.3.2 tag. No upstream code was changed.
https://github.com/openpgpjs/openpgpjs/tree/v6.3.2

The standalone verifier embeds the same library, followed by the separately
maintained Plebum adapter and UI scripts. To replace/relink it, put a compatible
browser distribution at openpgp.min.js and run:
  python3 scripts/build_download_verifier.py
  node scripts/test_download_verifier.cjs

No library download, CDN, keyserver, upload or network request is used when
checking a selected ZIP. The separate homepage can load its existing site assets.
