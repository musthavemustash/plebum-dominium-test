// Execute the shipped controller and crypto with DOM doubles; not browser/Tails QA.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync('docs/dice-converter.html','utf8');
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const elements=new Map(),events={},timers=new Map();let nextTimer=0;
function el(tag='DIV'){return{tagName:tag,value:'',hidden:false,checked:false,style:{},children:[],handlers:{},classList:{add(){},remove(){},toggle(){}},addEventListener(n,f){this.handlers[n]=f},appendChild(x){this.children.push(x)},get textContent(){return this._text||''},set textContent(x){this._text=String(x);this.children=[]},get innerHTML(){return this._html||''},set innerHTML(x){this._html=x;this.children=[];this._text=''}}}
for(const m of html.matchAll(/<([a-z][\w-]*)\b[^>]*\bid="([^"]+)"/gi))elements.set(m[2],el(m[1].toUpperCase()));
const get=id=>elements.get(id)||null;
const buttons=[1,2,3,4,5,6].map(n=>Object.assign(el('BUTTON'),{getAttribute(){return String(n)}}));
const doc={activeElement:el('BODY'),getElementById:get,querySelectorAll:()=>buttons,addEventListener(n,f){events[n]=f},createElement:el,createTextNode:t=>({textContent:t})};
const ctx=vm.createContext({document:doc,window:{addEventListener(){}},location:{protocol:'file:'},navigator:{onLine:true},setInterval(){},setTimeout(f){timers.set(++nextTimer,f);return nextTimer},clearTimeout(id){timers.delete(id)}});
for(const s of scripts)vm.runInContext(s,ctx);
const click=id=>get(id).handlers.click();
const input=(id,value)=>{get(id).value=value;get(id).handlers.input()};
const result=()=>get('results').children.map(x=>x.textContent).join('\n');
const flush=()=>{for(const [id,f] of [...timers]){timers.delete(id);f()}};
const clearResult=()=>assert.equal(result(),'','old validation must disappear immediately');
function start(){get('confirm-offline').checked=get('confirm-public').checked=true;click('session-start')}
function compare(){get('valwords').value=get('words').children.map(x=>x.children[1].textContent).join(' ');click('validate');assert.match(result(),/24 of 24 match/)}
function rolls(){click('testfill');compare()}
assert(get('tool-main').inert);start();assert(!get('tool-main').inert);
rolls();click('undo');clearResult();assert.equal(get('m-bits').textContent,'254');assert.equal(get('words').children.length,0);
rolls();events.keydown({key:'Backspace',preventDefault(){}});clearResult();
rolls();click('clear');clearResult();assert.equal(get('words').children.length,0);
rolls();input('valwords','invalid public test words');clearResult();click('validate');assert.match(result(),/Need 24 words/);
rolls();input('pastebits','0'.repeat(256));clearResult();click('validate');assert.doesNotMatch(result(),/24 of 24 match/);flush();compare();
input('pastebits','1'.repeat(256));clearResult();flush();click('validate');assert.match(result(),/lists differ/);
compare();input('pastebits','x');clearResult();flush();click('validate');assert.doesNotMatch(result(),/24 of 24 match/);assert.equal(get('words').children.length,0);
input('pastebits','0'.repeat(256));flush();compare();buttons[0].handlers.click();clearResult();assert.equal(get('m-bits').textContent,'2');
rolls();input('pastebits','0'.repeat(256));click('clear');flush();assert.equal(get('words').children.length,0);clearResult();
rolls();input('pastebits','0'.repeat(256));click('session-lock');flush();assert(get('tool-main').inert);assert.equal(get('words').children.length,0);clearResult();
start();rolls();click('testfill');clearResult();compare();
console.log('PASS: dice validation invalidated on edits, undo, clear, refill and lock; pending/invalid pasted bits cannot compare stale words; fresh comparisons still pass');
