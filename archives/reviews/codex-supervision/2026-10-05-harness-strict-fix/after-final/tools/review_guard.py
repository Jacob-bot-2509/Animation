"""Structural math-DOM and real PDF verification for review artifacts."""
from html.parser import HTMLParser
from pathlib import Path
import re, shutil, subprocess

class MathDom(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.wrappers=[]; self.titles=[]; self.errors=0; self.containers=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); ignored=tag in ('script','style') or any(f['ignored'] for f in self.stack)
        f={'tag':tag,'ignored':ignored,'title':None,'wrapper':None}
        if not ignored:
            if tag=='title': f['title']=[]; self.titles.append(f['title'])
            c=a.get('class','').split()
            if (tag=='span' and 'math' in c) or (tag=='div' and 'math-block' in c):
                f['wrapper']={'kind':'display' if tag=='div' else 'inline','containers':0,'text':[]}; self.wrappers.append(f['wrapper'])
            if tag=='mjx-container':
                self.containers+=1
                for parent in self.stack:
                    if parent['wrapper'] is not None: parent['wrapper']['containers']+=1
            if tag=='mjx-merror' or a.get('data-mml-node')=='merror' or 'data-mjx-error' in a: self.errors+=1
            if a.get('data-mml-node')=='mtext' and (a.get('fill','').lower()=='red' or a.get('stroke','').lower()=='red' or re.search(r'(?:color|fill|stroke)\s*:\s*red\b',a.get('style',''),re.I)): self.errors+=1
        if tag not in ('meta','link','img','br','hr','input','wbr','source','area','base','embed','param','track','col'): self.stack.append(f)
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs); self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag: del self.stack[i:]; break
    def handle_data(self,text):
        if any(f['ignored'] for f in self.stack): return
        for f in self.stack:
            if f['title'] is not None: f['title'].append(text)
            if f['wrapper'] is not None: f['wrapper']['text'].append(text)
    def verify(self,expected_inline,expected_display):
        rendered=sum(w['containers']==1 and '$' not in ''.join(w['text']) for w in self.wrappers)
        inline=sum(w['kind']=='inline' for w in self.wrappers); display=len(self.wrappers)-inline
        if [''.join(t).strip() for t in self.titles]!=['MJDONE']: raise ValueError('actual title is not MJDONE')
        if self.errors or rendered!=len(self.wrappers) or (inline,display)!=(expected_inline,expected_display) or self.containers!=expected_inline+expected_display:
            raise ValueError(f'math DOM rejected: inline={inline}/{expected_inline}, display={display}/{expected_display}, rendered={rendered}, containers={self.containers}, errors={self.errors}')
        return 0,rendered,0

def verify_dom(dom,expected_inline,expected_display):
    parser=MathDom(); parser.feed(dom); parser.close(); return parser.verify(expected_inline,expected_display)

def poppler(name):
    exe=shutil.which(name)
    fallback=Path.home()/f'AppData/Local/Programs/MiKTeX/miktex/bin/x64/{name}.exe'
    if not exe and fallback.is_file(): exe=str(fallback)
    if not exe: raise ValueError(f'{name} is required to validate a PDF')
    return exe

def validate_pdf(path):
    data=Path(path).read_bytes()
    if not data.startswith(b'%PDF-') or b'%%EOF' not in data[-4096:]: raise ValueError('invalid PDF signature/EOF')
    cp=subprocess.run([poppler('pdfinfo'),str(path)],capture_output=True,timeout=60,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    match=re.search(rb'^Pages:\s+(\d+)\s*$',cp.stdout,re.M)
    if cp.returncode or not match or int(match.group(1))<1: raise ValueError('PDF has no valid nonempty page tree')
    return int(match.group(1))
