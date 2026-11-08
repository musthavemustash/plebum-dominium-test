// Public-test session contract. These are simulated events, not network-isolation tests.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const name of ['dice-converter','descriptor-tool','diceware-mapper']) {
 const html=fs.readFileSync('docs/'+name+'.html','utf8');
 const a=html.indexOf('function createPublicTestSession()');const b=html.indexOf('var testSession',a);
 assert(a>0&&b>a);const source=html.slice(a,b);
 for(const protocol of ['https:','http:','file:','blob:','chrome-extension:']) for(const flag of [true,false,undefined,null]) {
  const els={},events={};let wiped=0,tick;
  const el=id=>els[id]??={checked:false,handlers:{},addEventListener(n,f){this.handlers[n]=f;}};
  const c=vm.createContext({document:{getElementById:el},window:{addEventListener(n,f){events[n]=f;}},location:{protocol},navigator:{onLine:flag},setInterval(f){tick=f;}});
  vm.runInContext(source+'\nvar session = createPublicTestSession();',c);
  const click=()=>el('session-start').handlers.click();
  click();assert(!c.session.allowed());c.session.ready(()=>wiped++);click();assert(!c.session.allowed());
  el('confirm-offline').checked=true;click();assert(!c.session.allowed());
  el('confirm-public').checked=true;click();assert.equal(c.session.allowed(),protocol==='file:');
  if(protocol==='file:') {
   assert.match(el('browser-signal').textContent,/does not verify/);
   for(const event of ['online','offline','pagehide','pageshow']) {
    el('confirm-offline').checked=el('confirm-public').checked=true;click();const before=wiped;events[event]();assert(wiped>before);assert(!c.session.allowed());assert(el('tool-main').inert);assert(!el('confirm-offline').checked);
   }
   el('confirm-offline').checked=el('confirm-public').checked=true;click();c.navigator.onLine=flag===true?false:true;tick();assert(!c.session.allowed());
   el('confirm-offline').checked=el('confirm-public').checked=true;click();el('session-lock').handlers.click();assert(!c.session.allowed());
  }
 }
 console.log('PASS: '+name+' public-session protocol/acknowledgment matrix (20 cases), explicit isolation limit, observed-event clearing, manual lock');
}
