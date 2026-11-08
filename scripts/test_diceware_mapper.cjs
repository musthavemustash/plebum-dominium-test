// Execute the shipped mapper controller with DOM doubles; not a browser/Tails test.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync('docs/diceware-mapper.html','utf8');
assert.match(html, /id="slots"><\/div>/, 'source must not contain saved dice inputs');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);assert.equal(new Set(ids).size,ids.length);
const elements={},events={};
function node(id='') {return {id,value:'',textContent:'',dataset:{},style:{},children:[],handlers:{},classList:{add(){},remove(){},toggle(){}},appendChild(n){this.children.push(n);return n;},addEventListener(n,f){this.handlers[n]=f;},setAttribute(){},removeAttribute(){},focus(){},select(){},set innerHTML(v){this.children=[];},get innerHTML(){return ''}};}
ids.forEach(id=>elements[id]=node(id));
const document={getElementById(id){assert(elements[id],'missing markup '+id);return elements[id];},createElement:()=>node(),createTextNode:text=>({textContent:text})};
let copied=[],rejectCopy;
const ctx=vm.createContext({document,window:{addEventListener(n,f){events[n]=f;}},navigator:{onLine:true,clipboard:{writeText(text){copied.push(text);return Promise.resolve();}}},location:{protocol:'file:'},setInterval(){},setTimeout(){}});
const code=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)][0][1];vm.runInContext(code,ctx);
const el=id=>elements[id];const start=()=>{el('confirm-offline').checked=el('confirm-public').checked=true;el('session-start').handlers.click();};
const input=(s,p,v)=>{const target=ctx.slotState[s].inputs[p];target.value=v;ctx.onInput({target});};
const paste=(s,p,text)=>{let prevented=false;ctx.onPaste({target:ctx.slotState[s].inputs[p],preventDefault(){prevented=true;},clipboardData:{getData:()=>text}});assert(prevented);};
const rows=fs.readFileSync('docs/kit/eff_large_wordlist.txt','utf8').trim().split(/\r?\n/);
assert.equal(rows.length,7776);for(const row of rows){const [roll,word]=row.split(/\s+/);assert.equal(ctx.lookup(roll),word,roll);}
assert(el('tool-main').inert);assert.equal(ctx.slotState.length,6);assert.equal(el('slots').children.length,6);
input(0,0,'1');assert.equal(ctx.slotState[0].inputs[0].value,'');start();assert(!el('tool-main').inert);
const fill=()=>{for(let s=0;s<6;s++)paste(s,0,'11111');assert(!el('copyBtn').disabled);};
(async()=>{
 fill();await el('copyBtn').handlers.click();assert.equal(copied[0],Array(6).fill('abacus').join(' '));
 for(const bad of ['0','7','x','12','１']){fill();input(0,0,bad);assert(el('copyBtn').disabled);assert.equal(ctx.slotState[0].wordEl.textContent,'·····');assert.equal(el('copyStatus').textContent,'');assert.match(ctx.slotState[0].hintEl.textContent,/Nothing was mapped/);}
 for(const bad of ['12x34','123456','1 2 3','0','']){fill();paste(0,0,bad);assert(el('copyBtn').disabled);assert.match(ctx.slotState[0].hintEl.textContent,/Nothing was pasted/);}
 fill();paste(0,4,'12');assert(el('copyBtn').disabled);paste(0,4,'6');assert.equal(ctx.slotState[0].wordEl.textContent,'ability');
 input(0,4,'');const before=copied.length;el('copyBtn').handlers.click();assert.equal(copied.length,before,'incomplete phrase must never copy');
 fill();ctx.navigator.clipboard.writeText=()=>new Promise((r,j)=>rejectCopy=j);el('copyBtn').handlers.click();el('clearBtn').handlers.click();rejectCopy(Error('blocked'));await Promise.resolve();await Promise.resolve();assert.equal(el('copyStatus').textContent,'','late copy rejection must not repopulate status or retry clipboard');
 fill();el('session-lock').handlers.click();assert(el('tool-main').inert);assert(el('copyBtn').disabled);assert(ctx.slotState.every(s=>s.inputs.every(i=>i.value==='')));assert(!el('confirm-public').checked);
 start();fill();events.pagehide();assert(el('tool-main').inert);assert(el('copyBtn').disabled);
 console.log('PASS: all 7,776 EFF mappings; six rows; invalid typing/paste/overflow; incomplete copy blocked; stale clipboard callback; clear and lock');
})().catch(e=>{console.error(e);process.exitCode=1;});
