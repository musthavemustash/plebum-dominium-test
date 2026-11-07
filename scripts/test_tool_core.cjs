// Pure-code tests, not browser execution. Inputs are public/disposable fixtures only.
const fs=require('fs'), vm=require('vm'), crypto=require('crypto');
const root=require('path').resolve(__dirname,'..');
const scripts=n=>[...fs.readFileSync(root+'/docs/'+n+'.html','utf8').matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]);
const req=JSON.parse(fs.readFileSync(0,'utf8'));
(async()=>{
if(req.mode==='dice'){
 const c=vm.createContext({});vm.runInContext(scripts('dice-converter')[0],c);
 const out=req.inputs.map(x=>c.wordsFromBitsInput(x));
 const wordlist=fs.readFileSync(root+'/review/fixtures/bip39-english.txt','utf8').trim().split(/\r?\n/);
 if(JSON.stringify(Array.from(c.WORDLIST))!==JSON.stringify(wordlist))throw Error('JS wordlist mismatch');
 if([1,2,3,4,5,6].map(x=>c.faceToBits(x)).join(',')!=='00,01,10,11,,')throw Error('dice face mapping');
 for(const v of out.filter(x=>x.words)){if(!c.validateWords(v.words).ok)throw Error('valid checksum rejected');}
 const bad=Array(24).fill('abandon');if(c.validateWords(bad).ok)throw Error('bad checksum accepted');
 process.stdout.write(JSON.stringify(out));
}else{
 const c=vm.createContext({btoa,atob,crypto:crypto.webcrypto,TextEncoder,TextDecoder,Uint8Array,ArrayBuffer,DataView,ReadableStream,WritableStream,TransformStream,setTimeout,clearTimeout,console});
 c.self=c;
 const parts=scripts('descriptor-tool');vm.runInContext(parts[0],c);
 // Use configuration statements directly from the shipped UI controller.
 const config=parts[1].match(/  openpgp\.config\.[^;]+;/g);if(!config||config.length!==4)throw Error('configuration extraction');
 vm.runInContext(config.join('\n'),c);const pgp=c.openpgp;
 if(req.mode==='encrypt')process.stdout.write(await pgp.encrypt({message:await pgp.createMessage({binary:new TextEncoder().encode(req.text)}),passwords:[req.password],format:'armored'}));
 else process.stdout.write(Buffer.from((await pgp.decrypt({message:await pgp.readMessage({armoredMessage:req.text}),passwords:[req.password],format:'binary'})).data));
}
})().catch(e=>{console.error(e.message);process.exitCode=1;});
