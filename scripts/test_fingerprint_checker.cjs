// Execute shipped checker with DOM doubles and real WebCrypto.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),{webcrypto,createHash}=require('crypto');
const html=fs.readFileSync('docs/fingerprint-checker.html','utf8');
const els={};const el=id=>els[id]??={value:'',style:{},textContent:'',handlers:{},addEventListener(n,f){this.handlers[n]=f;}};
const c=vm.createContext({document:{getElementById:el},crypto:webcrypto,Uint8Array});
vm.runInContext([...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].at(-1)[1],c);
const choose=(key,file)=>{el('file-select').value=key;el('file-select').handlers.change();el('file-input').handlers.change({target:{files:file?[file]:[]}});};
const file=data=>({arrayBuffer:async()=>Buffer.from(data)});const click=()=>el('check-btn').handlers.click();
(async()=>{
 for(const [key,name] of Object.entries({converter:'dice-converter',descriptor:'descriptor-tool',mapper:'diceware-mapper'})) {
  const bytes=fs.readFileSync('docs/'+name+'.html');choose(key,file(bytes));assert.equal(el('expected').value,createHash('sha256').update(bytes).digest('hex'));await click();assert.match(el('verdict').textContent,/^MATCH/);
 }
 choose('mapper',file('wrong bytes'));assert.equal(el('result').style.display,'none');await click();assert.match(el('verdict').textContent,/^MISMATCH/);
 el('expected').value='z'.repeat(64);el('expected').handlers.input();assert(el('check-btn').disabled);assert.equal(el('result').style.display,'none');await click();assert.equal(el('computed').textContent,'');
 let resolve;choose('mapper',{arrayBuffer:()=>new Promise(r=>resolve=r)});const pending=click();choose('descriptor',file('new'));await click();const latest=el('computed').textContent;resolve(Buffer.from('old'));await pending;assert.equal(el('computed').textContent,latest);
 let reject;choose('mapper',{arrayBuffer:()=>new Promise((r,j)=>reject=j)});const failed=click();choose('mapper',null);reject(Error('late'));await failed;assert.equal(el('result').style.display,'none');assert(el('check-btn').disabled);
 choose('mapper',{arrayBuffer:async()=>{throw Error('read failed');}});await click();assert.match(el('verdict').textContent,/Error/);assert.equal(el('computed').textContent,'');
 console.log('PASS: three exact shipped fingerprints; mismatch; invalid hex; stale read/error/selection cancellation; read failure');
})().catch(e=>{console.error(e);process.exitCode=1});
