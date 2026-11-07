// Execute both shipped scripts, including startup and real event handlers.
// DOM/network doubles exercise controller logic; this is not browser or air-gap QA.
const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '../docs/dice-converter.html'), 'utf8');
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);

function boot(protocol = 'file:', online) {
  if (arguments.length < 2) online = false;
  const elements = new Map(), windowEvents = {}, documentEvents = {}, pending = new Set();
  const timers = new Map();
  let timerId = 0;
  function element(tagName = 'DIV') {
    return {
      tagName, value: '', hidden: false, style: {}, children: [], handlers: {}, className: '',
      classList: {remove() {}, toggle() {}},
      addEventListener(name, fn) { this.handlers[name] = fn; },
      appendChild(child) { this.children.push(child); },
      get textContent() { return this._text || ''; },
      set textContent(value) { this._text = String(value); this.children = []; },
      get innerHTML() { return this._html || ''; },
      set innerHTML(value) { this._html = value; this.children = []; this._text = ''; },
    };
  }
  // Only real IDs from the shipped markup exist; missing IDs must fail startup.
  for (const match of html.matchAll(/<([a-z][\w-]*)\b[^>]*\bid="([^"]+)"/gi)) {
    const el = element(match[1].toUpperCase());
    elements.set(match[2], el);
  }
  const get = id => elements.get(id) || null;
  const buttons = [...html.matchAll(/<button\b[^>]*class="diebtn"[^>]*data-face="(\d+)"/g)]
    .map(match => Object.assign(element('BUTTON'), {getAttribute: name => name === 'data-face' ? match[1] : null}));
  assert.equal(buttons.length, 6);
  const document = {
    activeElement: element('BODY'), getElementById: get,
    querySelectorAll(selector) { assert.equal(selector, '.diebtn'); return buttons; },
    addEventListener(name, fn) { documentEvents[name] = fn; },
    createElement: tag => element(tag.toUpperCase()),
    createTextNode: text => ({textContent: String(text)}),
  };
  const context = vm.createContext({
    document, window: {addEventListener(name, fn) { windowEvents[name] = fn; }},
    location: {protocol}, navigator: {onLine: online},
    setTimeout(fn) { timers.set(++timerId, fn); return timerId; },
    clearTimeout(id) { timers.delete(id); },
  });
  // Track event-created promises too, even when the click handler doesn't return them.
  const instrumented = scripts[1].replace('async function addDie(face){',
    'function addDie(face){ return track(addDieImpl(face)); }\n  async function addDieImpl(face){');
  context.track = promise => { pending.add(promise); return promise; };
  vm.runInContext(scripts[0], context);
  vm.runInContext(instrumented, context); // No injected netBlocked value.
  async function settle() {
    await Promise.all([...pending]); pending.clear();
    await Promise.resolve();
  }
  return {
    get, context, document, buttons,
    counts(pairs, bits) {
      assert.equal(get('m-pairs').textContent, String(pairs));
      assert.equal(get('m-bits').textContent, String(bits));
    },
    async click(face) { buttons[face - 1].handlers.click(); await settle(); },
    async action(id) { await get(id).handlers.click(); await settle(); },
    async key(key, tag = 'BODY') {
      document.activeElement = element(tag);
      let prevented = false;
      documentEvents.keydown({key, preventDefault() { prevented = true; }});
      await settle(); return prevented;
    },
    async input(value) {
      get('pastebits').value = value; get('pastebits').handlers.input();
      for (const [id, fn] of [...timers]) { timers.delete(id); await fn(); }
      await settle();
    },
    async network(value, event = value === false ? 'offline' : 'online') {
      context.navigator.onLine = value;
      assert.equal(typeof windowEvents[event], 'function', 'network event registered at startup');
      await windowEvents[event](); await settle();
    },
    words() { return get('words').children.map(li => li.children[1].textContent); },
  };
}

(async () => {
  const ui = boot();
  ui.counts(0, 0); assert.equal(ui.get('netblock').hidden, true);
  for (let face = 1; face <= 6; face++) await ui.click(face);
  ui.counts(4, 8);
  assert.equal(ui.get('bits').textContent, '00011011');
  assert.equal(ui.get('strip').children.length, 6);
  assert.equal(ui.get('strip').children[4].children[1].textContent, 'skip');
  await ui.action('undo'); ui.counts(4, 8);
  await ui.action('clear'); ui.counts(0, 0);
  assert.equal(ui.get('strip').children.length, 0);
  for (const key of ['1', '2', '3', '4', '5', '6']) await ui.key(key);
  ui.counts(4, 8);
  await ui.key('1', 'TEXTAREA'); await ui.key('2', 'INPUT'); ui.counts(4, 8);
  assert.equal(await ui.key('Backspace'), true); ui.counts(4, 8);
  for (let i = 0; i < 4; i++) await ui.key('Backspace');
  ui.counts(1, 2);
  await ui.action('clear');
  for (let i = 0; i < 128; i++) await ui.click(1);
  ui.counts(128, 256);
  assert.equal(ui.words().join(' '), [...Array(23).fill('abandon'), 'art'].join(' '));
  await ui.click(2); ui.counts(128, 256);
  await ui.action('undo'); ui.counts(127, 254);
  assert.equal(ui.words().length, 0, 'undo below threshold clears stale mnemonic');
  assert.equal(ui.get('done256').hidden, true);
  await ui.click(1); ui.counts(128, 256); assert.equal(ui.words().length, 24);
  await ui.action('clear'); ui.counts(0, 0); assert.equal(ui.words().length, 0);
  await ui.action('testfill'); ui.counts(128, 256); assert.equal(ui.words().length, 24);
  await ui.action('clear');
  await ui.input('0'.repeat(256)); assert.equal(ui.words().at(-1), 'art');
  await ui.click(2); ui.counts(1, 2); assert.equal(ui.words().length, 0);
  await ui.input('1'.repeat(255)); assert.equal(ui.words().length, 0);
  await ui.input('0'.repeat(255) + 'x'); assert.equal(ui.words().length, 0);
  const vectors = JSON.parse(fs.readFileSync(path.join(__dirname, '../review/fixtures/bip39-vectors.json'), 'utf8')).english;
  for (const [hex, expected] of vectors) {
    await ui.input(BigInt('0x' + hex).toString(2).padStart(256, '0'));
    assert.equal(ui.words().join(' '), expected);
  }
  console.log('PASS: startup, six buttons, keyboard/focus, counters, skips, 256-bit cap, Undo/Clear, demo, paste/manual transition, invalid inputs, eight vectors');

  // Whole-controller boot across every supported/unsupported environment.
  for (const protocol of ['file:', 'http:', 'https:', 'blob:', 'chrome-extension:']) {
    for (const online of [false, true, undefined, null]) {
      const state = boot(protocol, online), allowed = protocol === 'file:' && online === false;
      assert.equal(state.get('netblock').hidden, allowed);
      await state.click(1); await state.key('2');
      if (allowed) state.counts(2, 4);
      else {
        state.counts(0, 0);
        await state.action('testfill'); state.counts(0, 0);
        await state.input('0'.repeat(256)); assert.equal(state.words().length, 0);
        state.get('valwords').value = vectors[0][1];
        await state.action('validate'); assert.equal(state.get('results').children.length, 0);
      }
    }
  }
  await ui.input('0'.repeat(256));
  ui.get('valwords').value = vectors[0][1]; await ui.action('validate');
  assert.equal(ui.get('results').children.length, 2);
  await ui.network(true);
  ui.counts(0, 0);
  for (const id of ['pastebits', 'valwords']) assert.equal(ui.get(id).value, '');
  assert.equal(ui.words().length, 0); assert.equal(ui.get('results').children.length, 0);
  assert.equal(ui.get('bits').textContent, ''); assert.equal(ui.get('strip').children.length, 0);
  await ui.click(1); await ui.key('1'); await ui.action('testfill'); ui.counts(0, 0);
  await ui.network(false); await ui.click(3); ui.counts(1, 2);
  // Missed offline event: a button tap rechecks the now-offline state.
  await ui.network(true); ui.context.navigator.onLine = false;
  await ui.click(4); ui.counts(1, 2);
  // Missed online event: a button tap blocks and wipes stale public output.
  ui.context.navigator.onLine = true; await ui.click(1); ui.counts(0, 0);
  assert.equal(ui.get('netblock').hidden, false);
  await ui.network(undefined); await ui.click(1); ui.counts(0, 0);
  console.log('PASS: 20 protocol/network startup combinations, blocked controls, reconnect wipe, resumed offline entry, missed-event checks, unknown state blocked');
})().catch(error => { console.error(error); process.exitCode = 1; });
