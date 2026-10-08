from pathlib import Path
from html.parser import HTMLParser
import re,json
import pypdfium2 as pdfium
from PIL import Image,ImageDraw

out=Path('D:/code/tmp/pdfs')
class Plain(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,t,a):
        if t in ['script','style']: self.skip+=1
        if t in ['h1','h2','h3','p','li','div'] and not self.skip:self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ['script','style']: self.skip-=1
        if t in ['h1','h2','h3','p','li','div'] and not self.skip:self.parts.append('\n')
    def handle_data(self,s):
        if not self.skip:self.parts.append(s)
for name in ['data-test','dataset-eval']:
    parser=Plain();parser.feed(Path('D:/Animation-Model-Training/outputs/review/'+name+'.html').read_text(encoding='utf-8'))
    text=''.join(parser.parts)
    chunks=re.split(r'\n(?=(?:test|eval)-[a-z]+-\d{3} )',text)
    items=[]
    for chunk in chunks[1:]:
        chunk=chunk.split('动画要点')[0].split('思路展开')[0].strip()
        chunk=re.sub(r'\n{2,}','\n',chunk)
        items.append({'id':chunk.split(' ')[0],'text':chunk})
    (out/(name+'-full.txt')).write_text(text,encoding='utf-8')
    (out/(name+'-items.json')).write_text(json.dumps(items,ensure_ascii=False),encoding='utf-8')
    (out/(name+'-compact.txt')).write_text('\n\n'.join(x['text'] for x in items),encoding='utf-8')
    doc=pdfium.PdfDocument('C:/Users/Jacap/Desktop/'+name+'.pdf')
    for i in range(len(doc)):
        doc[i].render(scale=1.4).to_pil().convert('RGB').save(out/(name+'-'+str(i+1)+'.png'))
    for start in range(0,len(doc),4):
        sheet=Image.new('RGB',(1200,1740),'#cccccc');draw=ImageDraw.Draw(sheet)
        for j in range(start,min(start+4,len(doc))):
            im=Image.open(out/(name+'-'+str(j+1)+'.png'));im.thumbnail((590,830))
            x=(j-start)%2*600;y=(j-start)//2*870
            sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{name} page {j+1}',fill='black')
        sheet.save(out/(name+'-sheet-'+str(start//4+1)+'.png'))
    print(name,'items',len(items),'pages',len(doc))
