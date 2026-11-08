#!/usr/bin/env node
'use strict';

// Exercise the shipped browser script with real SHA-256 and a deliberately
// small DOM. This is a functional check, not a browser/layout substitute.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { webcrypto } = require('node:crypto');

const rootDir = path.resolve(__dirname, '..');
const sourcePath = path.join(rootDir, 'docs/assets/js/download-verifier.js');
const source = fs.readFileSync(sourcePath, 'utf8');
const baseUrl = 'https://musthavemustash.github.io/plebum-dominium-test/';
const nextTurn = () => new Promise(resolve => setImmediate(resolve));
const inputs = [];

function loadPublishedPackages() {
  const offlineDir = 'testing/offline-20261108-r1/';
  const focusedDir = 'testing/alpha-20261108-t5-r1/';
  const offline = JSON.parse(fs.readFileSync(path.join(rootDir, 'docs', offlineDir, 'manifest.json'), 'utf8'));
  const focused = JSON.parse(fs.readFileSync(path.join(rootDir, 'docs', focusedDir, 'manifest.json'), 'utf8'));
  const definitions = [
    ...offline.packages.map((p, index) => ({
      item: p, dir: offlineDir, id: index === 0 ? 'complete' : 'website-tools',
      label: index === 0 ? 'Complete offline tester' : 'Website tools only',
      release: 'offline-20261108-r1'
    })),
    { item: focused.archive, dir: focusedDir, id: 'focused', label: 'Focused public tests', release: focused.release }
  ];
  for (const def of definitions) {
    inputs.push({
      localPath: path.join(rootDir, 'docs', def.dir, def.item.name),
      checksumPath: path.join(rootDir, 'docs', def.dir, 'SHA256SUMS.txt'),
      entry: {
        id: def.id, label: def.label, name: def.item.name, release: def.release,
        sha256: def.item.sha256, bytes: def.item.size, current: true,
        checksumUrl: baseUrl + def.dir + 'SHA256SUMS.txt',
        downloadUrl: baseUrl + def.dir + def.item.name
      }
    });
  }
  return { schema: 1, packages: inputs.map(input => input.entry) };
}

const currentCatalog = loadPublishedPackages();
const abc = Buffer.from('abc', 'utf8');
const hello = Buffer.from('hello', 'utf8');
const abcHash = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad';
const helloHash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824';

function vectorEntry(overrides = {}) {
  return {
    id: 'known-vector', label: 'Known byte vector', name: 'known-vector.zip',
    release: 'node-fixture', sha256: abcHash, bytes: abc.length, current: true,
    checksumUrl: 'https://example.test/SHA256SUMS.txt',
    downloadUrl: 'https://example.test/known-vector.zip', ...overrides
  };
}

function catalogWith(...entries) {
  return { schema: 1, packages: [...currentCatalog.packages, ...entries] };
}

class ElementMock {
  constructor(tagName = 'div') {
    this.tagName = tagName.toUpperCase();
    this.nodeType = tagName === '#text' ? 3 : 1;
    this.dataset = {};
    this.style = {};
    this.attributes = new Map();
    this.listeners = new Map();
    this.children = [];
    this.selectors = new Map();
    this._text = '';
    this.hidden = false;
    this.disabled = false;
    this.open = false;
    this.value = '';
    this.files = [];
    this.parentNode = null;
    this.className = '';
    const classes = new Set();
    this.classList = {
      add: (...names) => names.forEach(name => classes.add(name)),
      remove: (...names) => names.forEach(name => classes.delete(name)),
      contains: name => classes.has(name),
      toggle: (name, force) => {
        const add = force === undefined ? !classes.has(name) : force;
        if (add) classes.add(name); else classes.delete(name);
        return add;
      }
    };
  }
  set textContent(value) { this._text = String(value ?? ''); this.children = []; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(''); }
  set innerHTML(value) {
    if (value !== '') throw new Error('Unsafe HTML insertion: the verifier must render untrusted values as text');
    this.textContent = '';
  }
  get innerHTML() { return this.textContent; }
  get firstChild() { return this.children[0] || null; }
  get childNodes() { return this.children; }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...children) {
    for (let child of children) {
      if (typeof child === 'string') { const node = new ElementMock('#text'); node.textContent = child; child = node; }
      this.appendChild(child);
    }
  }
  removeChild(child) { this.children.splice(this.children.indexOf(child), 1); child.parentNode = null; return child; }
  replaceChildren(...children) { this.textContent = ''; this.append(...children); }
  setAttribute(name, value) {
    this.attributes.set(name, String(value));
    if (name === 'disabled') this.disabled = true;
    if (name === 'hidden') this.hidden = true;
    if (name.startsWith('data-')) this.dataset[name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = String(value);
  }
  getAttribute(name) { return this.attributes.has(name) ? this.attributes.get(name) : null; }
  hasAttribute(name) { return this.attributes.has(name); }
  removeAttribute(name) {
    this.attributes.delete(name);
    if (name === 'disabled') this.disabled = false;
    if (name === 'hidden') this.hidden = false;
  }
  toggleAttribute(name, force) {
    const set = force === undefined ? !this.hasAttribute(name) : force;
    if (set) this.setAttribute(name, ''); else this.removeAttribute(name);
    return set;
  }
  querySelector(selector) { return this.selectors.get(selector) || null; }
  querySelectorAll(selector) { const item = this.querySelector(selector); return item ? [item] : []; }
  addEventListener(type, handler) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(handler);
  }
  removeEventListener(type, handler) {
    this.listeners.set(type, (this.listeners.get(type) || []).filter(item => item !== handler));
  }
  dispatch(type, fields = {}) {
    const event = { type, target: this, currentTarget: this, preventDefault() {}, stopPropagation() {}, ...fields };
    for (const handler of this.listeners.get(type) || []) handler.call(this, event);
  }
  click() { this.dispatch('click'); }
  focus() {}
}

function makeFile(bytes, name = 'download.zip', options = {}) {
  const payload = Buffer.from(bytes);
  let reads = 0;
  return {
    name, size: options.size ?? payload.length, type: 'application/zip',
    get reads() { return reads; },
    arrayBuffer() {
      reads++;
      if (options.error) return Promise.reject(options.error);
      if (options.deferred) return options.deferred.promise;
      return Promise.resolve(payload.buffer.slice(payload.byteOffset, payload.byteOffset + payload.byteLength));
    }
  };
}

function deferred() {
  let resolve, reject;
  const promise = new Promise((res, rej) => { resolve = res; reject = rej; });
  return { promise, resolve, reject };
}

function setup(catalog = catalogWith(vectorEntry()), options = {}) {
  const widget = new ElementMock('section');
  const nodes = {};
  const names = ['file', 'reset', 'status', 'status-title', 'status-text', 'progress',
    'file-info', 'filename', 'filesize', 'hash-details', 'hash', 'reference',
    'packages', 'next', 'dropzone'];
  for (const name of names) {
    const node = new ElementMock(name === 'file' ? 'input' : name === 'reset' ? 'button' : 'div');
    nodes[name] = node;
    widget.selectors.set(`[data-verify-${name}]`, node);
    widget.appendChild(node);
  }
  const config = new ElementMock('script');
  config.textContent = JSON.stringify(catalog);
  widget.selectors.set('.pd-verify-catalog', config);
  widget.appendChild(config);
  const document = new ElementMock('document');
  document.readyState = 'complete';
  document.createElement = tagName => new ElementMock(tagName);
  document.createTextNode = text => { const node = new ElementMock('#text'); node.textContent = text; return node; };
  document.createDocumentFragment = () => new ElementMock('fragment');
  document.selectors.set('[data-zip-verifier]', widget);
  document.selectors.set('.pd-verify-catalog', config);
  document.documentElement = new ElementMock('html');
  const digests = [];
  const networkCalls = [];
  const rejectNetwork = (...args) => { networkCalls.push(args); throw new Error('Unexpected network request'); };
  function FileMock() {}
  if (!options.noArrayBuffer) FileMock.prototype.arrayBuffer = function () {};
  const crypto = options.noCrypto ? undefined : { subtle: { digest(algorithm, bytes) {
    const operation = options.digestError
      ? Promise.reject(options.digestError)
      : webcrypto.subtle.digest(algorithm, bytes);
    digests.push(operation);
    return operation;
  } } };
  const context = {
    document, crypto, File: FileMock, Blob, URL, URLSearchParams, Uint8Array, ArrayBuffer,
    TextEncoder, TextDecoder, console, setTimeout, clearTimeout, queueMicrotask,
    requestAnimationFrame: callback => setImmediate(callback), cancelAnimationFrame: clearImmediate,
    fetch: rejectNetwork, XMLHttpRequest: rejectNetwork, WebSocket: rejectNetwork,
    navigator: { sendBeacon: rejectNetwork },
    location: { href: baseUrl + 'verify-download.html', protocol: 'https:', origin: new URL(baseUrl).origin },
    isSecureContext: true, HTMLElement: ElementMock, Element: ElementMock,
    addEventListener: (...args) => document.addEventListener(...args)
  };
  context.window = context;
  context.self = context;
  vm.runInNewContext(source, context, { filename: sourcePath });
  const environment = {
    widget, nodes, networkCalls, digests,
    get state() { return widget.dataset.state; },
    choose(file, { click = true } = {}) {
      if (click) nodes.file.dispatch('click');
      nodes.file.files = file ? [file] : [];
      nodes.file.value = file ? 'C:\\fakepath\\' + file.name : '';
      nodes.file.dispatch('change');
    },
    reset() { nodes.reset.dispatch('click'); },
    async settle() {
      for (let i = 0; i < 6; i++) { await nextTurn(); await Promise.allSettled(digests); }
      assert.equal(networkCalls.length, 0, 'Selected-file data must stay local');
    },
    async waitForState(expected) {
      const started = Date.now();
      while (widget.dataset.state !== expected) {
        if (Date.now() - started > 2500) {
          throw new Error(`Expected state ${expected}; got ${widget.dataset.state}: ${nodes['status-title'].textContent} / ${nodes['status-text'].textContent}`);
        }
        await nextTurn();
      }
      assert.equal(networkCalls.length, 0, 'Selected-file data must stay local');
    }
  };
  return environment;
}

const cases = [];
const test = (name, run) => cases.push({ name, run });

test('current manifest entries agree with their published SHA256SUMS files', () => {
  assert.equal(currentCatalog.packages.length, 3);
  for (const input of inputs) {
    const sums = fs.readFileSync(input.checksumPath, 'utf8').trim().split(/\r?\n/);
    const entry = sums.map(line => line.match(/^([a-f0-9]{64})\s+\*?(.+)$/i))
      .find(match => match && match[2] === input.entry.name);
    assert.ok(entry, `Missing checksum for ${input.entry.name}`);
    assert.equal(entry[1].toLowerCase(), input.entry.sha256);
    assert.ok(Number.isSafeInteger(input.entry.bytes) && input.entry.bytes > 0);
  }
  const env = setup(currentCatalog);
  assert.equal(env.state, 'ready');
  assert.equal(env.nodes.file.disabled, false);
});

test('known SHA-256 abc vector matches by bytes regardless of filename', async () => {
  const env = setup();
  const file = makeFile(abc, 'renamed-by-my-browser (7).bin');
  env.choose(file);
  await env.waitForState('match');
  assert.equal(file.reads, 1);
  assert.equal(env.nodes['status-title'].textContent, 'Matches published package');
  assert.equal(env.nodes.filename.textContent, file.name);
  assert.equal(env.nodes.hash.textContent, abcHash);
});

test('second known SHA-256 hello vector is computed correctly', async () => {
  const env = setup(catalogWith(vectorEntry({ id: 'hello', sha256: helloHash, bytes: hello.length })));
  env.choose(makeFile(hello, 'any-name.zip'));
  await env.waitForState('match');
  assert.equal(env.nodes.hash.textContent, helloHash);
});

test('same digest with a different published byte count does not match', async () => {
  const env = setup(catalogWith(vectorEntry({ bytes: abc.length + 1 })));
  env.choose(makeFile(abc));
  await env.waitForState('mismatch');
  assert.equal(env.nodes['status-title'].textContent, 'No matching published checksum');
});

test('one changed byte fails despite having the published filename and size', async () => {
  const env = setup();
  env.choose(makeFile(Buffer.from('abd'), 'known-vector.zip'));
  await env.waitForState('mismatch');
  assert.notEqual(env.nodes.hash.textContent, abcHash);
});

test('oversized file is rejected before arrayBuffer reads any bytes', async () => {
  const env = setup();
  const file = makeFile(abc, 'huge.zip', { size: 32 * 1024 * 1024 + 1 });
  env.choose(file);
  await env.waitForState('error');
  assert.equal(file.reads, 0);
  assert.equal(env.digests.length, 0);
});

test('file read errors cannot retain a previous match', async () => {
  const env = setup();
  env.choose(makeFile(abc));
  await env.waitForState('match');
  env.choose(makeFile(abc, 'unreadable.zip', { error: new Error('Fixture read failure') }));
  await env.waitForState('error');
  assert.notEqual(env.nodes['status-title'].textContent, 'Matches published package');
});

test('SHA-256 failures display an error rather than a comparison result', async () => {
  const env = setup(undefined, { digestError: new Error('Fixture digest failure') });
  env.choose(makeFile(abc));
  await env.waitForState('error');
  assert.notEqual(env.nodes['status-title'].textContent, 'Matches published package');
});

test('reset invalidates a pending read and clears its result', async () => {
  const env = setup();
  const pending = deferred();
  env.choose(makeFile(abc, 'pending.zip', { deferred: pending }));
  assert.equal(env.state, 'checking');
  env.reset();
  assert.equal(env.state, 'ready');
  pending.resolve(Uint8Array.from(abc).buffer);
  await env.settle();
  assert.equal(env.state, 'ready');
  assert.equal(env.nodes.hash.textContent, '');
  assert.equal(env.nodes.file.value, '');
});

test('a slower old selection cannot overwrite a newer result', async () => {
  const env = setup(catalogWith(vectorEntry(), vectorEntry({
    id: 'hello', label: 'New selection', name: 'new.zip', sha256: helloHash, bytes: hello.length
  })));
  const pending = deferred();
  env.choose(makeFile(abc, 'old.zip', { deferred: pending }));
  assert.equal(env.state, 'checking');
  env.choose(makeFile(hello, 'new.zip'));
  await env.waitForState('match');
  pending.resolve(Uint8Array.from(abc).buffer);
  await env.settle();
  assert.equal(env.state, 'match');
  assert.equal(env.nodes.filename.textContent, 'new.zip');
  assert.equal(env.nodes.hash.textContent, helloHash);
});

test('canceling the chooser invalidates a pending comparison', async () => {
  const env = setup();
  const pending = deferred();
  env.choose(makeFile(abc, 'old.zip', { deferred: pending }));
  env.nodes.file.dispatch('click');
  env.nodes.file.dispatch('cancel');
  pending.resolve(Uint8Array.from(abc).buffer);
  await env.settle();
  assert.equal(env.state, 'ready');
  assert.equal(env.nodes.hash.textContent, '');
});

test('HTML in a local filename is displayed only as text', async () => {
  const env = setup();
  const hostileName = '<img src=x onerror=alert(1)> & "download".zip';
  env.choose(makeFile(abc, hostileName));
  await env.waitForState('match');
  assert.equal(env.nodes.filename.textContent, hostileName);
  assert.equal(env.nodes.filename.children.length, 0);
});

test('a prior package snapshot is clearly reported as earlier', async () => {
  const env = setup(catalogWith(
    vectorEntry({ sha256: helloHash, bytes: hello.length }),
    vectorEntry({ current: false })
  ));
  env.choose(makeFile(abc, 'known-vector.zip'));
  await env.waitForState('earlier');
  assert.equal(env.nodes['status-title'].textContent, 'Matches an earlier published package');
  assert.notEqual(env.nodes['status-title'].textContent, 'Matches published package');
});

test('current entry wins if history has the identical digest and size', async () => {
  const env = setup(catalogWith(vectorEntry({ current: false }), vectorEntry()));
  env.choose(makeFile(abc));
  await env.waitForState('match');
  assert.equal(env.nodes['status-title'].textContent, 'Matches published package');
});

test('missing WebCrypto disables verification before any file read', async () => {
  const env = setup(undefined, { noCrypto: true });
  assert.equal(env.state, 'unsupported');
  assert.equal(env.nodes.file.disabled, true);
  const file = makeFile(abc);
  env.choose(file);
  await env.settle();
  assert.equal(file.reads, 0);
  assert.equal(env.state, 'unsupported');
});

test('missing File.arrayBuffer support disables verification', () => {
  const env = setup(undefined, { noArrayBuffer: true });
  assert.equal(env.state, 'unsupported');
  assert.equal(env.nodes.file.disabled, true);
});

test('invalid catalog checksum fails closed before file selection', () => {
  const env = setup({ schema: 1, packages: [vectorEntry({ sha256: 'not-a-sha256' })] });
  assert.equal(env.state, 'error');
  assert.equal(env.nodes.file.disabled, true);
});

const generatedPath = path.join(rootDir, 'docs/verify-download.html');
if (fs.existsSync(generatedPath)) {
  test('generated standalone catalog current entries match current manifests', () => {
    const html = fs.readFileSync(generatedPath, 'utf8');
    const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)];
    const embedded = scripts.find(match => /\bclass\s*=\s*["'][^"']*\bpd-verify-catalog\b/.test(match[1]));
    assert.ok(embedded, 'Generated standalone verifier needs an embedded catalog');
    const data = JSON.parse(embedded[2]);
    const normalized = packages => packages.filter(entry => entry.current !== false)
      .map(entry => ({ name: entry.name, sha256: entry.sha256, bytes: entry.bytes }))
      .sort((a, b) => a.name.localeCompare(b.name));
    assert.deepEqual(normalized(data.packages), normalized(currentCatalog.packages));
    const env = setup(data);
    assert.equal(env.state, 'ready');
  });
} else if (process.argv.includes('--require-generated')) {
  test('generated standalone catalog exists', () => assert.fail('Run the verifier generator before --require-generated'));
}

for (const input of inputs.filter(item => fs.existsSync(item.localPath))) {
  test(`actual published ZIP bytes: ${input.entry.name}`, async () => {
    const env = setup(currentCatalog);
    const file = makeFile(fs.readFileSync(input.localPath), 'renamed-local-copy.zip');
    env.choose(file);
    await env.waitForState('match');
    assert.equal(env.nodes.hash.textContent, input.entry.sha256);
    assert.equal(file.size, input.entry.bytes);
  });
}

(async () => {
  let failed = 0;
  for (const [index, item] of cases.entries()) {
    try { await item.run(); console.log(`ok ${index + 1} - ${item.name}`); }
    catch (error) { failed++; console.error(`not ok ${index + 1} - ${item.name}\n${error.stack || error}`); }
  }
  console.log(`${cases.length - failed}/${cases.length} verifier checks passed`);
  if (!fs.existsSync(generatedPath) && !process.argv.includes('--require-generated')) {
    console.log('Generated standalone catalog not yet present; rerun with --require-generated after generation.');
  }
  const archiveCount = inputs.filter(item => fs.existsSync(item.localPath)).length;
  if (archiveCount < inputs.length) console.log(`Actual ZIP byte checks available: ${archiveCount}/${inputs.length}; known-vector and current-manifest checks ran above.`);
  if (failed) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
