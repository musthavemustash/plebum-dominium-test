// Evaluate shipped network-state functions with DOM doubles. No browser isolation claim.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
(async()=>{
for(const name of ['dice-converter','descriptor-tool']){
 const html=fs.readFileSync('docs/'+name+'.html','utf8');
 const start=html.lastIndexOf('  async function renderNet(){');
 const end=html.indexOf("  window.addEventListener('online'",start);
 assert(start>0&&end>start);const fn=html.slice(start,end);
 for(const protocol of ['https:','http:','file:'])for(const online of [true,false]){
  const elements={};const $=id=>elements[id]??=( {hidden:false,value:'PUBLIC TEST',textContent:'',innerHTML:'',classList:{remove(){},toggle(){}}});
  const c=vm.createContext({$,location:{protocol},navigator:{onLine:online},netBlocked:true,clearAll(){},wipe(){}});
  vm.runInContext(fn,c);await c.renderNet();
  assert.equal(c.netBlocked,protocol!=='file:'||online);
 }
 console.log('PASS: '+name+' blocks HTTP(S) and online local files in network-state logic');
 // Report rather than silently calling this a fail-closed guarantee for unknown states.
 const c=vm.createContext({$:()=>null,location:{protocol:'file:'},navigator:{},netBlocked:true,clearAll(){},wipe(){}});
 vm.runInContext(fn,c);await c.renderNet();
 console.log('LIMITATION: '+name+' navigator.onLine unavailable => blocked='+c.netBlocked);
}
})().catch(e=>{console.error(e);process.exitCode=1;});
