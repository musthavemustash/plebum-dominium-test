// Structure and price failure checks; browser layout is verified separately.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const base = '/plebum-dominium-test/';
const docs = path.join(__dirname, '..', 'docs');
let count = 0;
function walk(dir) {
  for (const entry of fs.readdirSync(dir, {withFileTypes:true})) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) { walk(file); continue; }
    if (!file.endsWith('.html')) continue;
    const html = fs.readFileSync(file, 'utf8');
    if (!html.includes('<header class="site-header">')) continue;
    count++;
    const blocks = [...html.matchAll(/<nav class="news-ticker"[\s\S]*?<\/nav>/g)];
    assert.equal(blocks.length, 1, file);
    const ticker = blocks[0][0];
    assert.equal((ticker.match(/id="ticker-price"/g)||[]).length, 1);
    const duplicate = ticker.split('<span class="ticker-set" aria-hidden="true">')[1];
    assert.ok(duplicate);
    for (const match of duplicate.matchAll(/<a\s+([^>]+)>/g)) assert.match(match[1], /tabindex="-1"/);
    for (const match of ticker.matchAll(/href="([^"]+)"/g)) {
      assert.ok(match[1].startsWith(base), match[1]);
      const [rel, fragment] = match[1].slice(base.length).split('#');
      const target = fs.readFileSync(path.join(docs, rel), 'utf8');
      if (fragment) assert.ok(target.includes('id="'+fragment+'"'), match[1]);
    }
  }
}
walk(docs);
assert.equal(count, 82);
const main = fs.readFileSync(path.join(docs,'assets/js/main.js'),'utf8');
const code = main.slice(main.indexOf('/* Ticker price:'), main.indexOf('/* ---------- Ask the guide:'));
const flush = () => new Promise(resolve=>setImmediate(resolve));
async function scenario({protocol='https:', online=true, offlineRoot, present=true}={}) {
  const el = {hidden:true,textContent:''};
  const events = {}, intervals = [];
  let calls = 0, reply = {ok:true,json:async()=>({USD:75000})};
  const context = {document:{getElementById:()=>present?el:null},
    window:{PD_OFFLINE_ROOT:offlineRoot,addEventListener:(key,fn)=>events[key]=fn},
    location:{protocol},navigator:{onLine:online},AbortController,
    setTimeout:()=>1,clearTimeout:()=>{},setInterval:(fn,ms)=>intervals.push({fn,ms}),
    fetch:async(url,options)=>{calls++;assert.equal(url,'https://mempool.space/api/v1/prices');
      assert.equal(options.credentials,'omit');assert.equal(options.referrerPolicy,'no-referrer');
      if(reply instanceof Error)throw reply;return reply;}};
  vm.runInNewContext(code,context); await flush();
  return {el,context,events,intervals,get calls(){return calls;},set reply(value){reply=value;}};
}
(async()=>{
  for(const config of [{protocol:'file:'},{offlineRoot:'file:///guide/'},{present:false},{online:false}]) {
    const s=await scenario(config);assert.equal(s.calls,0);assert.equal(s.el.hidden,true);
  }
  const s=await scenario();assert.equal(s.el.textContent,'BTC $75,000');assert.equal(s.el.hidden,false);
  assert.equal(s.intervals[0].ms,60000);
  for(const reply of [new Error('Network unavailable'),{ok:false},{ok:true,json:async()=>({USD:'75000'})},
    {ok:true,json:async()=>({USD:NaN})},{ok:true,json:async()=>({USD:-1})}]) {
    s.reply=reply;await s.intervals[0].fn();assert.equal(s.el.hidden,true);assert.equal(s.el.textContent,'');
  }
  s.reply={ok:true,json:async()=>({USD:76000})};await s.events.online();assert.equal(s.el.hidden,false);
  s.events.offline();assert.equal(s.el.hidden,true);assert.equal(s.el.textContent,'');
  console.log('PASS: 82 static tickers, all destinations and fragments, non-focusable duplicates, price refresh/failure/reconnect, no local/offline price requests.');
})().catch(error=>{console.error(error);process.exitCode=1;});
