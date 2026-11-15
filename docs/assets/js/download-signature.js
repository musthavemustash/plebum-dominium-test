/* Public release verification. Vendored OpenPGP.js; no network or key discovery. */
(function (scope) {
  'use strict';
  var FINGERPRINT = 'B9286C4A7CFF722E191D2D7566FB7D9AB51E417E';

  function bounded(value, limit) {
    return typeof value === 'string' && value.length > 0 && value.length <= limit;
  }

  function parseManifest(manifest) {
    var rows = new Map();
    var lines = manifest.split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    if (!lines.length || lines.length > 32) throw new Error('Invalid manifest length.');
    lines.forEach(function (line) {
      var match = /^([a-f0-9]{64}) [ *]([A-Za-z0-9][A-Za-z0-9._-]*\.zip)$/.exec(line);
      if (!match || match[2].includes('..') || rows.has(match[2])) {
        throw new Error('Invalid or duplicate manifest entry.');
      }
      rows.set(match[2], match[1]);
    });
    return rows;
  }

  async function verify(release, now) {
    if (!scope.openpgp || !bounded(release && release.publicKey, 32768) ||
        !bounded(release.manifest, 16384) || !bounded(release.signature, 16384)) {
      throw new Error('Signature files or verifier unavailable.');
    }
    var date = now || new Date();
    var keys = await scope.openpgp.readKeys({ armoredKeys: release.publicKey });
    if (keys.length !== 1 || keys[0].isPrivate() ||
        keys[0].getFingerprint().toUpperCase() !== FINGERPRINT) {
      throw new Error('The public key does not match the Plebum release key.');
    }
    var key = keys[0];
    // Check the key today as well as the signature at its creation time.
    // An expired/revoked key or an incorrect device clock must not yield green.
    await key.verifyPrimaryKey(date);
    var signature = await scope.openpgp.readSignature({ armoredSignature: release.signature });
    if (signature.packets.length !== 1) throw new Error('Expected one detached signature.');
    var message = await scope.openpgp.createMessage({ binary: new TextEncoder().encode(release.manifest) });
    var result = await scope.openpgp.verify({ message: message, signature: signature,
      verificationKeys: key, date: date, format: 'binary' });
    var checked = await Promise.allSettled(result.signatures.map(function (item) { return item.verified; }));
    if (checked.length !== 1 || checked[0].status !== 'fulfilled' || checked[0].value !== true) {
      throw new Error('The release signature is not valid.');
    }
    // Parse only authenticated bytes, without normalizing or trimming the signed data.
    return { fingerprint: FINGERPRINT, hashes: parseManifest(release.manifest) };
  }

  scope.PlebumReleaseSignatures = Object.freeze({ fingerprint: FINGERPRINT, verify: verify });
}(typeof window !== 'undefined' ? window : globalThis));
