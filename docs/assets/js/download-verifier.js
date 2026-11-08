/* Plebum Dominium ZIP checksum comparison. No network, storage, or uploads. */
(function () {
  'use strict';

  var MAX_BYTES = 32 * 1024 * 1024;
  var CHECKSUM = /^[a-f0-9]{64}$/i;

  function text(value, maxLength) {
    return typeof value === 'string' && value.trim().length > 0 && value.length <= maxLength;
  }

  function httpsUrl(value) {
    if (!text(value, 2048)) return false;
    try {
      var url = new URL(value);
      return url.protocol === 'https:' && !url.username && !url.password;
    } catch (error) {
      return false;
    }
  }

  function parseCatalog(node) {
    if (!node) throw new Error('Missing package reference.');
    var data = JSON.parse(node.textContent);
    if (!data || data.schema !== 1 || !Array.isArray(data.packages) ||
        !data.packages.length || data.packages.length > 32) {
      throw new Error('Invalid package reference.');
    }
    return data.packages.map(function (entry) {
      if (!entry || !text(entry.id, 160) || !text(entry.label, 200) ||
          !text(entry.name, 255) || !text(entry.release, 160) ||
          typeof entry.sha256 !== 'string' || !CHECKSUM.test(entry.sha256) ||
          !Number.isSafeInteger(entry.bytes) || entry.bytes <= 0 || entry.bytes > MAX_BYTES ||
          !httpsUrl(entry.checksumUrl) || !httpsUrl(entry.downloadUrl) ||
          (entry.current !== undefined && typeof entry.current !== 'boolean')) {
        throw new Error('Incomplete package reference.');
      }
      return {
        id: entry.id, label: entry.label, name: entry.name, release: entry.release,
        sha256: entry.sha256.toLowerCase(), bytes: entry.bytes,
        checksumUrl: entry.checksumUrl, downloadUrl: entry.downloadUrl,
        current: entry.current !== false
      };
    }).sort(function (a, b) {
      return Number(b.current) - Number(a.current);
    });
  }

  function byteLabel(bytes) {
    if (bytes < 1024) return bytes + ' bytes';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KiB · ' + bytes + ' bytes';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MiB · ' + bytes + ' bytes';
  }

  function element(tag, className, content) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined) node.textContent = content;
    return node;
  }

  function initialize(root) {
    if (root.dataset.verifierInitialized === 'true') return;
    root.dataset.verifierInitialized = 'true';

    function find(name) { return root.querySelector('[data-verify-' + name + ']'); }

    var input = find('file');
    var resetButton = find('reset');
    var status = find('status');
    var statusTitle = find('status-title');
    var statusText = find('status-text');
    var progress = find('progress');
    var fileInfo = find('file-info');
    var filename = find('filename');
    var filesize = find('filesize');
    var hashDetails = find('hash-details');
    var hashOutput = find('hash');
    var reference = find('reference');
    var packageList = find('packages');
    var next = find('next');
    var dropzone = find('dropzone');
    var requestToken = 0;
    var packages;
    var available = false;
    var cryptoProvider = window.crypto;

    function show(state, title, detail) {
      root.dataset.state = state;
      root.setAttribute('aria-busy', state === 'checking' ? 'true' : 'false');
      statusTitle.textContent = title;
      statusText.textContent = detail;
      progress.hidden = state !== 'checking';
    }

    function clearResult() {
      requestToken += 1;
      progress.hidden = true;
      fileInfo.hidden = true;
      filename.textContent = '';
      filesize.textContent = '';
      hashDetails.hidden = true;
      hashDetails.open = false;
      hashOutput.textContent = '';
      reference.textContent = '';
      next.hidden = true;
      resetButton.disabled = true;
      root.setAttribute('aria-busy', 'false');
      if (dropzone) dropzone.classList.remove('is-dragover');
      return requestToken;
    }

    function ready() {
      show('ready', 'Ready to check', 'Choose a ZIP to compare it with the saved published references. Renamed copies are recognized by their contents.');
    }

    function reset(focus) {
      clearResult();
      input.value = '';
      if (available) ready();
      if (focus && available && typeof input.focus === 'function') input.focus();
    }

    function lock(state, title, detail) {
      available = false;
      root.dataset.enabled = 'false';
      input.disabled = true;
      resetButton.disabled = true;
      show(state, title, detail);
    }

    if (!input || !resetButton || !status || !statusTitle || !statusText || !progress ||
        !fileInfo || !filename || !filesize || !hashDetails || !hashOutput || !reference ||
        !packageList || !next) {
      if (input) input.disabled = true;
      if (resetButton) resetButton.disabled = true;
      root.dataset.enabled = 'false';
      root.dataset.state = 'error';
      if (statusTitle) statusTitle.textContent = 'Checker unavailable';
      if (statusText) statusText.textContent = 'This verifier is incomplete. Open the current verifier or use the published checksum list.';
      return;
    }

    clearResult();
    try {
      packages = parseCatalog(root.querySelector('.pd-verify-catalog'));
    } catch (error) {
      lock('error', 'Package references unavailable', 'This copy has no valid package references. Open the current verifier or use the published checksum lists. No verification has run.');
      return;
    }

    packageList.textContent = '';
    packages.forEach(function (entry) {
      var item = element('li');
      var heading = element('div', 'pd-verify-package-title');
      heading.appendChild(element('strong', '', entry.label));
      heading.appendChild(element('span', 'pd-verify-package-badge' + (entry.current ? '' : ' is-earlier'), entry.current ? 'Current reference' : 'Earlier reference'));
      item.appendChild(heading);
      item.appendChild(element('p', 'pd-verify-package-meta', entry.name + ' · ' + entry.release + ' · ' + byteLabel(entry.bytes)));
      item.appendChild(element('code', '', entry.sha256));
      var links = element('p', 'pd-verify-package-links');
      var checksumLink = element('a', '', entry.current ? 'Published checksum list' : 'Checksum history');
      checksumLink.href = entry.checksumUrl;
      links.appendChild(checksumLink);
      if (entry.current) {
        var downloadLink = element('a', '', 'Download package');
        downloadLink.href = entry.downloadUrl;
        links.appendChild(downloadLink);
      }
      item.appendChild(links);
      packageList.appendChild(item);
    });

    if (window.isSecureContext === false || !cryptoProvider || !cryptoProvider.subtle ||
        typeof cryptoProvider.subtle.digest !== 'function' ||
        typeof File === 'undefined' || !File.prototype || typeof File.prototype.arrayBuffer !== 'function') {
      lock('unsupported', 'Browser verification unavailable', 'This browser does not provide the required local SHA-256 tools here. Open the HTTPS verifier in a supported browser, or compare the published SHA-256 with a local file-hashing tool. No verification has run.');
      return;
    }

    available = true;
    root.dataset.enabled = 'true';
    input.disabled = false;
    ready();

    async function checkFile(file) {
      var token = clearResult();
      if (!available) return;
      if (!file) { ready(); return; }
      resetButton.disabled = false;
      fileInfo.hidden = false;
      filename.textContent = typeof file.name === 'string' ? file.name : 'Selected file';

      if (!Number.isSafeInteger(file.size) || file.size < 0 || typeof file.arrayBuffer !== 'function') {
        show('error', 'File could not be read', 'Select a regular downloaded ZIP file, then try again. No verification has run.');
        return;
      }
      filesize.textContent = byteLabel(file.size);
      if (file.size > MAX_BYTES) {
        show('error', 'File exceeds the 32 MiB limit', 'This checker is for the listed Plebum Dominium ZIP packages. The selected file was not read.');
        return;
      }
      if (file.size === 0) {
        show('mismatch', 'No matching published checksum', 'The selected file is empty. Choose the completed ZIP download, or download the package again.');
        return;
      }

      show('checking', 'Checking on your device…', 'Reading the selected file and calculating its SHA-256. Nothing is uploaded.');
      var bytes;
      var hash;
      try {
        bytes = await file.arrayBuffer();
        if (token !== requestToken) return;
        if (!bytes || bytes.byteLength !== file.size) {
          show('error', 'File could not be read completely', 'The bytes read do not match the selected file size. Select the completed ZIP again; no match has been confirmed.');
          return;
        }
        var digest = await cryptoProvider.subtle.digest('SHA-256', bytes);
        if (token !== requestToken) return;
        hash = Array.from(new Uint8Array(digest)).map(function (byte) {
          return byte.toString(16).padStart(2, '0');
        }).join('');
        if (!CHECKSUM.test(hash)) throw new Error('Invalid digest output.');
      } catch (error) {
        if (token !== requestToken) return;
        show('error', 'Could not complete the check', 'The browser could not read or hash this file. Select it again, or use a local SHA-256 tool with the published checksum list. No match has been confirmed.');
        return;
      } finally {
        bytes = null;
      }

      if (token !== requestToken) return;
      hashOutput.textContent = hash;
      hashDetails.hidden = false;
      var match = packages.find(function (entry) {
        return entry.sha256 === hash && entry.bytes === file.size;
      });
      if (!match) {
        reference.textContent = 'No saved reference matches both this SHA-256 and this file size.';
        show('mismatch', 'No matching published checksum', 'This file does not match the packages listed in this verifier. Check the selected ZIP and release, or download a fresh copy. An older offline verifier may not recognize a newer package.');
        return;
      }

      reference.textContent = match.name + ' · ' + match.release + ' · ' + byteLabel(match.bytes) + (match.current ? ' · Current reference in this copy' : ' · Earlier published reference');
      next.hidden = false;
      if (match.current) {
        show('match', 'Matches published package', match.label + ' · ' + match.release + '. The SHA-256 and file size match this copy’s published reference. Continue with the extracted-file check below.');
      } else {
        show('earlier', 'Matches an earlier published package', match.label + ' · ' + match.release + '. This is a recognized older ZIP. Keep its hash with an existing test run; download the current package if you are beginning new tests.');
      }
    }

    input.addEventListener('click', function () { reset(false); });
    input.addEventListener('cancel', function () { reset(false); });
    input.addEventListener('change', function () {
      if (input.files && input.files.length > 1) {
        clearResult();
        resetButton.disabled = false;
        show('error', 'Choose one ZIP at a time', 'Select a single downloaded package to check. No verification has run.');
        return;
      }
      checkFile(input.files && input.files[0]);
    });
    resetButton.addEventListener('click', function () { reset(true); });

    if (dropzone) {
      dropzone.addEventListener('dragover', function (event) {
        event.preventDefault();
        if (available) {
          dropzone.classList.add('is-dragover');
          if (event.dataTransfer) event.dataTransfer.dropEffect = 'copy';
        }
      });
      dropzone.addEventListener('dragleave', function () { dropzone.classList.remove('is-dragover'); });
      dropzone.addEventListener('drop', function (event) {
        event.preventDefault();
        dropzone.classList.remove('is-dragover');
        if (!available) return;
        input.value = '';
        var files = event.dataTransfer && event.dataTransfer.files;
        if (!files || files.length !== 1) {
          clearResult();
          resetButton.disabled = false;
          show('error', 'Choose one ZIP at a time', 'Drop a single downloaded ZIP file into the checker. No verification has run.');
          return;
        }
        checkFile(files[0]);
      });
    }
  }

  function start() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-zip-verifier]'), initialize);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
}());
