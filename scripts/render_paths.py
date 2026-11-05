#!/usr/bin/env python3
"""Render navigation-only path copies from canonical docs/handouts; --check rejects drift.
Never regenerates or overwrites the reviewed handouts themselves.
"""
import json, re, sys
from pathlib import Path
from html import escape, unescape
from urllib.parse import urljoin
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = '/plebum-dominium-test/'
PATHS = {
 'one': {'label': 'One key + passphrase', 'steps': [
 ('terms','Terms','terms'), ('threat-model','Before you begin','threat-model'), ('choose-path','Pick your path','../choose-path'),
 ('checklist','Checklist','checklist-one'), ('airgap','Two boots','airgap'),
 ('verify','Check the files','verify'), ('dice','Make one key','dice-one'),
 ('titanium','Back up your key','titanium-one'),
 ('inheritance','If I am gone','inheritance-one'), ('faq','If you get stuck','faq-one'),
 ('fire-card','Recovery card','fire-card-one'), ('single-sig','One key + passphrase','single-sig')]},
 'three': {'label': 'Three keys', 'steps': [
 ('terms','Terms','terms'), ('threat-model','Before you begin','threat-model'), ('choose-path','Pick your path','../choose-path'),
 ('checklist','Checklist','checklist'), ('airgap','Two boots','airgap'),
 ('verify','Check the files','verify'), ('dice','Make three keys','dice'),
 ('sparrow','Build the 2-of-3','sparrow'), ('signing','Practice spend','signing'),
 ('titanium','Metal and the map','titanium'), ('testnet','Rehearse on testnet','testnet'),
 ('encryption','Protect the wallet map','encryption'), ('inheritance','If I am gone','inheritance'),
 ('faq','If you get stuck','faq'), ('briefing','Tough questions','briefing'),
 ('fire-card','Recovery card','fire-card')]}}

def href(path, slug): return BASE + 'paths/' + path + '/' + slug + '.html'
def render(path, step):
 info = PATHS[path]; steps = info['steps']; slug, title, source = step; idx = steps.index(step)
 s = (DOCS / 'handouts' / (source+'.html')).read_text()
 # Resolve relative assets before relocating the document.
 s = re.sub(r'(href|src)="([^"#]+)"', lambda m: m[1]+'="'+urljoin(BASE+'handouts/'+source+'.html',m[2])+'"', s)
 s = s.replace('<body ', '<body data-guide-path="'+path+'" data-guide-slug="'+slug+'" ', 1)
 # URL path defines identity even if another tab last changed the saved preference.
 s = s.replace('</head>', '<script>document.documentElement.setAttribute("data-path", "'+('one' if path=='one' else 'full')+'");</script>\n</head>')
 for key in ('path-banner','path-gate'):
  s = re.sub(r'<div class="'+key+r'"[^>]*>.*?</div>', '', s, flags=re.S)
 label = escape(info['label']); position = f'Step {idx+1} of {len(steps)}'
 s = re.sub(r'<span class="header-sheet">.*?</span>', '<span class="header-sheet">'+position+'</span>',s)
 s = re.sub(r'<span class="mobilebar-pos">.*?</span>', '<span class="mobilebar-pos">'+position+'</span>',s)
 s = re.sub(r'<p class="kicker">.*?</p>', '<p class="kicker">'+label+' · '+position+'</p>',s,count=1)
 def navlink(i, cls, rel):
  if i < 0: return '<a class="'+cls+'" href="'+BASE+'">← Home</a>'
  if i >= len(steps): return '<a class="'+cls+'" href="'+BASE+'paths/'+path+'/index.html">Review this path →</a>'
  return '<a class="'+cls+'" rel="'+rel+'" href="'+href(path,steps[i][0])+'">'+('← ' if rel=='prev' else '')+str(i+1)+' · '+escape(steps[i][1])+(' →' if rel=='next' else '')+'</a>'
 top = '<nav class="step-banner" aria-label="'+position+'">'+navlink(idx-1,'step-nav','prev')+'<span class="step-pos"><strong>'+position+'</strong> · '+escape(title)+'</span>'+navlink(idx+1,'step-nav','next')+'</nav>'
 bottom = '<nav class="prevnext-row" aria-label="Previous and next sheets">'+navlink(idx-1,'prevnext prev','prev')+'<span class="step-pos-bottom">'+position+'</span>'+navlink(idx+1,'prevnext next','next')+'</nav>'
 if '<nav class="step-banner"' in s:
  s = re.sub(r'<nav class="step-banner".*?</nav>',top,s,flags=re.S)
 else:
  s = re.sub(r'(</h1>)',lambda m:m[0]+top,s,count=1)
 s = re.sub(r'<nav class="prevnext-row".*?</nav>',bottom,s,flags=re.S)
 sidebar = '<ul>'+''.join('<li><a href="'+href(path,t[0])+'" data-sheet="'+t[0]+'"'+(' class="active" aria-current="page"' if t[0]==slug else '')+'><span class="sheet-num">'+str(i+1).zfill(2)+'</span><span class="sheet-title">'+escape(t[1])+'</span><span class="sheet-check" aria-hidden="true">✓</span></a></li>' for i,t in enumerate(steps))+'</ul>'
 s = re.sub(r'(<nav class="sidebar".*?)(<ul>.*?</ul>)',lambda m:m[1]+sidebar,s,count=1,flags=re.S)
 s = re.sub(r'<p class="sidebar-path-note" id="path-count">.*?</p>','<p class="sidebar-path-note" id="path-count">'+label+' · '+str(len(steps))+' steps</p>',s)
 # Native links work without JS; switch to equivalent page or the other route's first page.
 def switch(m):
  target = 'one' if m[1]=='one' else 'three'; other = PATHS[target]['steps']
  dest = slug if any(t[0]==slug for t in other) else other[0][0]
  return '<a class="path-route-choice" href="'+href(target,dest)+'"'+(' aria-current="true"' if target==path else '')+'>'+escape(PATHS[target]['label'])+'</a>'
 s = re.sub(r'<button type="button" data-path="(one|full)"[^>]*>.*?</button>',switch,s,flags=re.S)
 # Inheritance instructions show only the current wallet setup in the sidebar.
 if slug == 'inheritance':
  current = '<div class="sidebar-path-seg"><span class="path-route-choice" aria-current="true">'+label+'</span><a class="path-route-choice" href="'+href(path,'choose-path')+'">Change path</a></div>'
  s = s.replace('<p class="sidebar-path-label">Choose a path</p>', '<p class="sidebar-path-label">Current path</p>', 1)
  s = re.sub(r'(<div class="sidebar-path"[^>]*>.*?)(<div class="sidebar-path-seg".*?</div>)',
             lambda m: m[1]+current,s,count=1,flags=re.S)
 # In-path cross references stay in this route, including legacy variant URLs.
 for t in steps:
  for name in {t[0],t[2],t[0]+'-one',t[0]+'-easy'}:
   s = s.replace(BASE+'handouts/'+name+'.html',href(path,t[0]))
 s = s.replace('href="'+BASE+'choose-path.html"', 'href="'+href(path,'choose-path')+'"') if idx > 0 else s
 s = s.replace('main.js?v=whytiers7','main.js?v=paths1')
 # Keep previously reviewed route-specific demo and recovery explanations.
 overrides = ROOT / 'scripts/reviewed_route_overrides.json'
 if overrides.exists():
  for rule in json.loads(overrides.read_text()).get(path+'/'+slug, []):
   if rule['from'] not in s:
    raise ValueError('Reviewed route override needs reconciliation: '+path+'/'+slug)
   s = s.replace(rule['from'], rule['to'], 1)
 return s

def outputs():
 out={}
 for path,info in PATHS.items():
  for step in info['steps']: out['paths/'+path+'/'+step[0]+'.html'] = render(path,step)
  # Route overview and finish destination; all stages remain revisitable.
  s=render(path,info['steps'][0])
  article='<article><p class="kicker">Your guide</p><h1>'+escape(info['label'])+'</h1><p>Follow these '+str(len(info['steps']))+' steps in order. You can revisit any step. Completing the reading does not certify a wallet or replace a recovery rehearsal.</p><ol>'+''.join('<li><a href="'+href(path,t[0])+'">'+escape(t[1])+'</a></li>' for t in info['steps'])+'</ol><p><a href="'+BASE+'choose-path.html">Compare or switch paths</a></p></article>'
  s=re.sub(r'<article[^>]*>.*?</article>',article,s,count=1,flags=re.S)
  s=re.sub(r'<aside class="toc-col".*?</aside>','',s,flags=re.S)
  s=s.replace('data-guide-slug="terms"','data-guide-slug="index"').replace('class="active" aria-current="page"','')
  s=re.sub(r'<span class="header-sheet">.*?</span>','<span class="header-sheet">Path overview</span>',s)
  s=re.sub(r'<span class="mobilebar-pos">.*?</span>','<span class="mobilebar-pos">Path overview</span>',s)
  s=re.sub(r'<title>.*?</title>','<title>'+escape(info['label'])+' · Plebum Dominium Test Site</title>',s)
  out['paths/'+path+'/index.html']=s
  entries=[]
  for i,(slug,title,source) in enumerate(info['steps']):
   page=out['paths/'+path+'/'+slug+'.html']
   article=re.search(r'<article[^>]*>(.*?)</article>',page,re.S)[1]
   article=re.sub(r'<script.*?</script>|<style.*?</style>','',article,flags=re.S)
   text=unescape(re.sub(r'<[^>]+>',' ',article))
   entries.append(dict(slug=slug,num=str(i+1).zfill(2),title=title,url=href(path,slug),text=' '.join(text.split())))
  out['paths/'+path+'/search-index.json']=json.dumps(entries,ensure_ascii=False,indent=2)+'\n'

 return out

def main():
 bad=[]
 for rel,content in outputs().items():
  p=DOCS/rel
  if '--check' in sys.argv:
   if not p.exists() or p.read_text()!=content: bad.append(rel)
  else:
   p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
 if bad: raise SystemExit('Stale path pages; run python3 scripts/render_paths.py: '+', '.join(bad))
 print('Path navigation: 12 one-key steps, 16 three-key steps, 2 overview pages '+('checked' if '--check' in sys.argv else 'rendered'))
if __name__=='__main__': main()
