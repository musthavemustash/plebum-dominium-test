// Evaluate shipped network-state functions with DOM doubles. No browser isolation claim.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
(async()=>{
for(const name of ['dice-converter','descriptor-tool']){
 const html=fs.readFileSync('docs/'+name+'.html','utf8');
 const start=html.lastIndexOf('  async function renderNet(){');
 const end=html.indexOf("  window.addEventListener('online'",start);
 assert(start>0&&end>start);const fn=html.slice(start,end);
 for(const protocol of ['https:','http:','file:','blob:','chrome-extension:'])for(const online of [true,false,undefined,null]){
  const elements={};const $=id=>elements[id]??=( {hidden:false,value:'PUBLIC TEST',textContent:'',innerHTML:'',classList:{remove(){},toggle(){}}});
  const c=vm.createContext({$,location:{protocol},navigator:{onLine:online},netBlocked:true,clearTimeout,pasteT:null,clearAll(){},wipe(){}});
  vm.runInContext(fn,c);await c.renderNet();
  assert.equal(c.netBlocked,protocol!=='file:'||online!==false);
 }
 console.log('PASS: '+name+' permits only file: with explicit false network status (20 combinations)');

}
})().catch(e=>{console.error(e);process.exitCode=1;});
