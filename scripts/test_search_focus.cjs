// Execute the shipped search controller with DOM doubles; not real-browser QA.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync('docs/assets/js/main.js','utf8');
const start=source.lastIndexOf('(function () {',source.indexOf('var btn = document.getElementById("ask-btn")'));
const controller=source.slice(start,source.indexOf('})();',start)+5);
async function run(fail=false){
 const events={},nodes={};let resolveIndex;
 function node(id){return nodes[id]={id,hidden:false,inert:false,disabled:false,tabIndex:0,value:'',children:[],handlers:{},classList:{toggle(){}},addEventListener(n,f){this.handlers[n]=f},focus(){document.activeElement=this},getClientRects(){return this.hidden?[]:[{}]},closest(){let n=this;while(n){if(n.inert)return n;n=n.parentElement}return null},getAttribute(n){return n==='href'?this.href:null}}}
 const body=node('body'),background=node('background'),preInert=node('pre-inert'),wrap=node('wrapper'),nestedSibling=node('nested-sibling'),backdrop=node('ask-backdrop'),btn=node('ask-btn'),input=node('ask-input'),results=node('ask-results');
 function children(parent,kids){parent.children=kids;kids.forEach(k=>k.parentElement=parent)}
 children(body,[background,preInert,wrap]);children(background,[btn]);children(wrap,[nestedSibling,backdrop]);children(backdrop,[input,results]);
 preInert.inert=true;backdrop.hidden=true;let links=[];
 Object.defineProperty(results,'innerHTML',{set(value){links=[...value.matchAll(/<a\b([^>]*)>/g)].map((m,i)=>Object.assign(node('link'+i),{href:(m[1].match(/href="([^"]*)"/)||[])[1],row:m[1].includes('ask-row')}));children(results,links)}});
 results.querySelectorAll=()=>links.filter(x=>x.row);backdrop.querySelectorAll=()=>[input,...links];
 const document={body,activeElement:btn,getElementById:id=>nodes[id],querySelector:()=>null,addEventListener(n,f){events[n]=f}};
 const window={location:{href:''}};
 const ctx=vm.createContext({document,window,localStorage:{getItem(){return 'one'}},fetch:()=>new Promise(r=>resolveIndex=r)});
 vm.runInContext(controller,ctx);
 function key(key,shiftKey=false){const e={key,shiftKey,preventDefault(){this.prevented=true}};events.keydown(e);return e}
 btn.handlers.click();assert.equal(document.activeElement,input);assert(background.inert&&nestedSibling.inert&&preInert.inert);assert(!wrap.inert&&!backdrop.inert);
 assert(key('Tab',true).prevented);assert.equal(document.activeElement,input); // loading: input only
 if(fail)resolveIndex({json(){throw Error('offline index unavailable')}});
 else resolveIndex({json:()=>Promise.resolve([{slug:'checklist',num:'01',title:'Checklist',text:'Public guide',url:'checklist.html'},{slug:'verify',num:'02',title:'Verify',text:'Check public files',url:'verify.html'}])});
 await new Promise(setImmediate);
 if(!fail){
  assert.equal(links.length,2);assert(key('Tab',true).prevented);assert.equal(document.activeElement,links.at(-1));
  assert(key('Tab').prevented);assert.equal(document.activeElement,input);assert(!key('Tab').prevented); // native forward traversal
  links[0].focus();assert(!key('Tab').prevented); // native interior traversal
  input.value='nothing matches';input.handlers.input();input.focus();key('Tab',true);assert.equal(document.activeElement,links.at(-1)); // fallback actions included
  links.at(-1).hidden=true;input.focus();key('Tab',true);assert.equal(document.activeElement,links[0]);
  btn.focus();key('Tab');assert.equal(document.activeElement,input); // recover focus outside modal
  input.value='verify';input.handlers.input();input.handlers.keydown({key:'ArrowDown',preventDefault(){}});input.handlers.keydown({key:'Enter',preventDefault(){}});assert.equal(window.location.href,'verify.html');
 }else{assert(key('Tab').prevented);assert.equal(document.activeElement,input)}
 key('Escape');assert(backdrop.hidden);assert(!background.inert&&!nestedSibling.inert);assert(preInert.inert);assert.equal(document.activeElement,btn);
 key('/');assert(!backdrop.hidden);backdrop.handlers.click({target:backdrop});assert(backdrop.hidden);assert.equal(document.activeElement,btn);assert(!background.inert&&preInert.inert);
}
(async()=>{await run();await run(true);console.log('PASS: search focus wraps in both directions, covers dynamic/fallback links, restores inert state and trigger focus, and preserves shortcuts')})().catch(e=>{console.error(e);process.exitCode=1});
