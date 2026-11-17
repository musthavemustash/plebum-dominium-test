// Logic checks using minimal DOM doubles; these do not replace browser/rendering QA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function element(text='') {
  const classes=new Set();
  return {textContent:text,innerHTML:'',hidden:false,value:'',events:{},attributes:{},
    classList:{add:x=>classes.add(x),remove:x=>classes.delete(x),contains:x=>classes.has(x),toggle(x,on){if(on===undefined)on=!classes.has(x);on?classes.add(x):classes.delete(x);return on;}},
    addEventListener(k,f){this.events[k]=f;},setAttribute(k,v){this.attributes[k]=v;},focus(){this.focused=true;}};
}
const source=fs.readFileSync('docs/handouts/terms.html','utf8');
const terms=[...source.matchAll(/<div class="term">(.*?)<\/div>/gs)].map(m=>element(m[1].replace(/<[^>]*>/g,' ')));
assert.equal(terms.length,12);
const filter=element(),count=element(),search=element();search.hidden=true;
vm.runInNewContext(fs.readFileSync('docs/assets/js/entry-pages.js','utf8'),{document:{getElementById:id=>({'term-filter':filter,'term-count':count}[id]),querySelector:()=>search,querySelectorAll:()=>terms}});
assert.equal(search.hidden,false);
filter.value='PSBT';filter.events.input();assert.equal(terms.filter(t=>!t.hidden).length,1);
filter.value='zzzzzz';filter.events.input();assert.equal(terms.filter(t=>!t.hidden).length,0);assert.match(count.textContent,/No matching/);
filter.value='  ';filter.events.input();assert.equal(terms.filter(t=>!t.hidden).length,12);
const main=fs.readFileSync('docs/assets/js/main.js','utf8');const code=main.slice(main.indexOf('/* --- hero keyring'),main.indexOf('/* ---------- motion:'));
const ids={};['keyring','keyring-lock','keyring-caption','keyring-descriptor','keyring-reset'].forEach(x=>ids[x]=element());
const keys=[element(),element(),element()];ids.keyring.querySelectorAll=selector=>selector==='.key.sel'?keys.filter(k=>k.classList.contains('sel')):keys;
const documentEvents={};ids.keyring.contains=target=>keys.includes(target);
vm.runInNewContext(code,{document:{getElementById:x=>ids[x],addEventListener:(type,fn)=>documentEvents[type]=fn}});
keys[0].events.click();assert.match(ids['keyring-caption'].innerHTML,/One key alone cannot spend/);
keys[1].events.click();assert.match(ids['keyring-caption'].innerHTML,/Two keys can sign/);assert.match(ids['keyring-descriptor'].textContent,/descriptor supplies/);
keys[2].events.click();assert.match(ids['keyring-descriptor'].textContent,/original 2-of-3 native SegWit setup/);
documentEvents.click({target:keys[0]});assert.equal(keys.filter(k=>k.classList.contains('sel')).length,3);
documentEvents.click({target:{}});assert.ok(keys.every(k=>k.attributes['aria-pressed']==='false'));
keys[0].events.click();ids['keyring-reset'].events.click();assert.equal(keys[0].focused,true);assert.ok(keys.every(k=>k.attributes['aria-pressed']==='false'));assert.equal(ids['keyring-reset'].hidden,true);
assert.equal((fs.readFileSync('docs/index.html','utf8').match(/<h1[ >]/g)||[]).length,1);
console.log('PASS: 12 glossary entries, matching/no-match/clear filtering; 1/2/3-key explanations and reset; single homepage H1. No browser rendering claimed.');
