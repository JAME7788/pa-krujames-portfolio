from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw
import sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'tmp/reformat-pa/final-render'
out.mkdir(parents=True,exist_ok=True)
doc=pymupdf.open(ROOT/(sys.argv[1] if len(sys.argv)>1 else 'deliverables/จัดรูปเล่มใหม่-รายงาน PA 2569 ป1 11คน.pdf'))
for i,page in enumerate(doc):
    page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(out/f'page-{i+1}.png')
    text=page.get_text()
    blocks=[b for b in page.get_text('blocks') if 55<b[1]<760]
    print(i+1,len(text),'bottom',round(max((b[3] for b in blocks),default=0)),text[90:150].replace('\n',' '))
for start in range(0,len(doc),4):
    sheet=Image.new('RGB',(1000,1450),'#dfe4eb')
    draw=ImageDraw.Draw(sheet)
    for offset in range(4):
        if start+offset>=len(doc):break
        img=Image.open(out/f'page-{start+offset+1}.png')
        img.thumbnail((490,695))
        x=(offset%2)*500+5;y=(offset//2)*725+25
        sheet.paste(img,(x,y));draw.text((x,y-20),f'PAGE {start+offset+1}',fill='black')
    sheet.save(out/f'contact-{start//4+1}.png')
print('Pages',len(doc))
