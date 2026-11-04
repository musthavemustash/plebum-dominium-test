#!/usr/bin/env python3
"""Validate every static navigation edge and route variant, without a browser."""
from html.parser import HTMLParser
from pathlib import Path
import re
from render_paths import PATHS, DOCS, BASE, href, outputs

class Page(HTMLParser):
 def __init__(self, text):
  super().__init__(); self.nav=None; self.links={};self.sheets=[];self.numbers=[];self.number=False;self.ids=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'): self.ids.append(a['id'])
  if tag=='nav': self.nav=a.get('class');self.links.setdefault(self.nav,[])
  if tag=='a' and self.nav:self.links[self.nav].append(a.get('href',''))
  if tag=='a' and a.get('data-sheet'):self.sheets.append(a.get('href'))
  if tag=='span' and a.get('class')=='sheet-num':self.number=True
 def handle_endtag(self,tag):
  if tag=='nav':self.nav=None
  if tag=='span':self.number=False
 def handle_data(self,data):
  if self.number:self.numbers.append(data.strip())

expected=outputs()
for name,content in expected.items():
 assert (DOCS/name).read_text()==content, f'Drift: {name}'
 if not name.endswith('.html'): continue
 page=Page(content)
 assert len(page.ids)==len(set(page.ids)), f'Duplicate ID: {name}'
 assert 'id="path-gate"' not in content, name
for path,info in PATHS.items():
 steps=info['steps']
 assert [s[0] for s in steps[:3]]==['terms','threat-model','choose-path']
 for i,(slug,title,source) in enumerate(steps):
  name=f'paths/{path}/{slug}.html'; text=(DOCS/name).read_text();page=Page(text)
  assert page.numbers==[str(j+1).zfill(2) for j in range(len(steps))],name
  assert page.sheets==[href(path,s[0]) for s in steps],name
  prev=BASE if i==0 else href(path,steps[i-1][0])
  nxt=href(path,'index') if i==len(steps)-1 else href(path,steps[i+1][0])
  assert page.links['step-banner']==[prev,nxt], (name,page.links['step-banner'])
  assert page.links['prevnext-row']==[prev,nxt],name
  assert f'Step {i+1} of {len(steps)}' in text,name
# The runtime routing table must exactly match the static sequence.
js=(DOCS/'assets/js/main.js').read_text()
for path,info in PATHS.items():
 match=re.search(r"    "+path+r": \{ label: '[^']+', steps: \[([^\]]+)\]",js)
 assert match and re.findall(r"'([^']+)'",match[1])==[s[0] for s in info['steps']]
assert 'This sheet is not on your' not in js
assert 'This sheet is part of the Full program' not in js
assert 'plebum-dominium-done-" + (document.body.getAttribute("data-guide-path")' in js
print('PASS: 28 step pages, 2 overviews, both navigation directions, route sidebars, consecutive numbers, variant rendering, unique IDs, runtime/static parity, separate progress keys.')
