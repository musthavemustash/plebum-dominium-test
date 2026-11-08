// Shipped controller with DOM doubles and mocked async crypto; not browser QA.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync('docs/descriptor-tool.html','utf8');
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const els={},events={},readers=[];
const el=id=>els[id]??={id,value:'',textContent:'',style:{},hidden:false,disabled:false,handlers:{},classList:{add(){},remove(){},toggle(){}},addEventListener(n,f){this.handlers[n]=f;}};
const document={getElementById:el,addEventListener(){},querySelectorAll(sel){if(sel==='input[type="password"]')return ['enc-pass','enc-pass2','dec-pass'].map(el);if(sel==='textarea')return ['enc-text','enc-preview','enc-out','dec-text','dec-preview','dec-out'].map(el);if(sel==='.status')return ['enc','dec'].flatMap(m=>['1','2','3','r'].map(p=>el(m+'-status-'+p)));throw Error('unexpected selector '+sel);}};
const pgp={config:{},enums:{symmetric:{aes256:9},hash:{sha512:10}},createMessage:async x=>x,readMessage:async x=>x,encrypt:async()=> 'ciphertext',decrypt:async()=>({data:new TextEncoder().encode('PUBLIC SAMPLE')})};
const window={addEventListener(n,f){events[n]=f;}};
const ctx=vm.createContext({TextEncoder,TextDecoder,Uint8Array,document,window,location:{protocol:'file:'},navigator:{onLine:false},openpgp:pgp,FileReader:class{constructor(){readers.push(this);} readAsText(){} readAsArrayBuffer(){}},setTimeout,clearTimeout,setInterval(){return 1;}});
vm.runInContext(scripts[1],ctx);vm.runInContext(scripts[2],ctx);
function start(){el('confirm-offline').checked=el('confirm-public').checked=true;el('session-start').handlers.click();}
assert(el('tool-main').inert); start(); assert(!el('tool-main').inert);
(async()=>{
 el('dec-text').value='ciphertext';el('dec-pass').value='public-test';await el('dec-btn').handlers.click();assert.equal(el('dec-out').value,'PUBLIC SAMPLE');
 pgp.decrypt=async()=>{throw Error('bad password')};el('dec-pass').value='wrong';await el('dec-btn').handlers.click();assert.equal(el('dec-out').value,'');assert.equal(el('dec-result').hidden,true);assert.equal(el('dec-pass').value,'');
 assert.match(el('dec-status-3').textContent,/Decryption failed/);
 await el('dec-btn').handlers.click();assert.equal(el('dec-status-3').textContent,'');assert.equal(el('dec-status-2').textContent,'Enter a passphrase.');
 el('dec-pass').value='new';el('dec-pass').handlers.input();assert.equal(el('dec-status-2').textContent,'');
 el('dec-out').value='old';el('dec-result').hidden=false;el('dec-text').value='';await el('dec-btn').handlers.click();assert.equal(el('dec-out').value,'');assert(el('dec-result').hidden);
 let resolve;pgp.encrypt=()=>new Promise(r=>resolve=r);el('enc-text').value='PUBLIC SAMPLE';el('enc-pass').value=el('enc-pass2').value='public-test';const pending=el('enc-btn').handlers.click();await Promise.resolve();await Promise.resolve();
 ctx.navigator.onLine=true;await events.online();for(const id of ['enc-pass','enc-pass2','dec-pass','enc-text','dec-out'])assert.equal(el(id).value,'');assert(el('enc-result').hidden);
 assert(el('tool-main').inert);ctx.navigator.onLine=false;await events.offline();resolve('late ciphertext');await pending;assert.equal(el('enc-out').value,'');assert(el('enc-result').hidden);
 start();el('enc-file').files=[{name:'public-test.txt'}];el('enc-file').handlers.change();assert.equal(readers.length,1);ctx.navigator.onLine=true;await events.online();ctx.navigator.onLine=false;await events.offline();readers[0].result='late public sample';readers[0].onload();assert.equal(el('enc-text').value,'');
 ctx.navigator.onLine=undefined;await events.offline();el('dec-text').value='sample';await el('dec-btn').handlers.click();assert.equal(el('dec-out').value,'');assert(el('dec-result').hidden);
 start();let reject;pgp.decrypt=()=>new Promise((r,j)=>reject=j);el('dec-text').value='cipher';el('dec-pass').value='old';const stale=el('dec-btn').handlers.click();await new Promise(setImmediate);assert.equal(typeof reject,'function');
 el('session-lock').handlers.click();start();el('dec-pass').value='new input';reject(Error('late failure'));await stale;assert.equal(el('dec-status-3').textContent,'');assert.equal(el('dec-pass').value,'new input');
 start();el('enc-text').value='old sample';el('enc-file').files=[{name:'unreadable.txt'}];el('enc-file').handlers.change();assert.equal(el('enc-text').value,'');assert.equal(el('enc-preview').value,'');el('session-lock').handlers.click();readers.at(-1).onerror();assert.equal(el('enc-status-1').textContent,'');
 console.log('PASS: public-session startup and acknowledgement;  failed/empty decryption clears stale output; reconnect wipes passwords/results; late crypto/file results discarded; revoked-session operation rejected');
})().catch(e=>{console.error(e);process.exitCode=1});
