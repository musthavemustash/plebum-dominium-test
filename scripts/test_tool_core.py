"""Known-answer conversion and cross-implementation encryption tests; no browser QA."""
from pathlib import Path
import importlib.util,json,subprocess,contextlib,io,tempfile,os,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,ROOT/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def node(mode,**kw):
 return subprocess.run(['node',str(ROOT/'scripts/test_tool_core.cjs')],input=json.dumps(dict(mode=mode,**kw)),text=True,capture_output=True)
def main():
 dice=module('dice','docs/kit/bip39_dice_converter.py');enc=module('enc','docs/kit/descriptor_obfuscator.py')
 vectors=json.loads((ROOT/'review/fixtures/bip39-vectors.json').read_text())['english'];vectors=[v for v in vectors if len(v[0])==64]
 assert dice.WORDLIST==(ROOT/'review/fixtures/bip39-english.txt').read_text().split()
 inputs=[bin(int(v[0],16))[2:].zfill(256) for v in vectors]
 # Excess-bit behavior is this project's convention, not a BIP39 input format.
 extras=['10'*129,'1'+'01'*128,'01'*256];invalid=['','0'*255,'0'*256+'x','0'*256+'\u00a0'];inputs+=extras+invalid
 result=node('dice',inputs=inputs);assert result.returncode==0,result.stderr;js=json.loads(result.stdout)
 for i,bits in enumerate(inputs):
  try:
   with contextlib.redirect_stdout(io.StringIO()):words,_=dice.generate_mnemonic(bits)
  except ValueError:
   assert js[i]['words'] is None;continue
  assert words==js[i]['words']
  if i<len(vectors):assert ' '.join(words)==vectors[i][1]
  else:
   digest=hashlib.sha256(int(bits,2).to_bytes((len(bits)+7)//8,'big')).digest();b=''.join(f'{x:08b}' for x in digest)+f'{hashlib.sha256(digest).digest()[0]:08b}'
   assert words==[dice.WORDLIST[int(b[j:j+11],2)] for j in range(0,264,11)]
 print(f'PASS: {len(vectors)} published 256-bit BIP39 vectors in Python/JS; wordlists; face mapping; checksum rejection; 3 excess-input cases; 4 invalid inputs')
 # Isolated disposable GPG home; disable symmetric-key caching so wrong-password tests are meaningful.
 with tempfile.TemporaryDirectory(prefix='plebum-gpg-test-') as home:
  os.chmod(home,0o700);old=os.environ.get('GNUPGHOME');os.environ['GNUPGHOME']=home
  Path(home,'gpg.conf').write_text('no-symkey-cache\n')
  try:
   sample='PUBLIC TEST ONLY\nUnicode: café\nNo wallet secrets';password='public-fixture-password-not-for-use';pw=bytearray(password.encode())
   py=enc.encrypt_descriptor(sample,pw);assert enc.decrypt_descriptor(py,pw)==sample
   js=node('encrypt',text=sample,password=password);assert js.returncode==0,js.stderr
   assert enc.decrypt_descriptor(js.stdout,pw)==sample
   dec=node('decrypt',text=py,password=password);assert dec.returncode==0,dec.stderr;assert dec.stdout==sample
   for ciphertext in [py,js.stdout]:
    lines=ciphertext.splitlines(); idx=next(i for i,l in enumerate(lines) if re.fullmatch(r'[A-Za-z0-9+/]{20,}={0,2}',l)); lines[idx]=('A' if lines[idx][0]!='A' else 'B')+lines[idx][1:]; damaged='\n'.join(lines)
    for candidate,secret in [(ciphertext,'wrong-public-password'),(ciphertext[:len(ciphertext)//2],password),(damaged,password)]:
     try:enc.decrypt_descriptor(candidate,bytearray(secret.encode()))
     except RuntimeError:pass
     else:raise AssertionError('GPG accepted wrong password/truncation')
     assert node('decrypt',text=candidate,password=secret).returncode!=0
   print('PASS: Python/GPG and embedded OpenPGP.js cross-decryption, Unicode text, wrong-password, truncated-message and corrupted-payload rejection')
  finally:
   subprocess.run(['gpgconf','--homedir',home,'--kill','gpg-agent'],capture_output=True)
   if old is None:os.environ.pop('GNUPGHOME',None)
   else:os.environ['GNUPGHOME']=old
if __name__=='__main__':main()
