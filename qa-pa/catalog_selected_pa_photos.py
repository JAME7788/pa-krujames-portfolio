from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags
import json, re, hashlib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'tmp/รูปที่ใช้ในpa'
OUT=ROOT/'tmp/selected-pa-review'
OUT.mkdir(parents=True,exist_ok=True)
START=datetime(2025,10,1); END=datetime(2026,9,30,23,59,59)

def date_for(path):
    m=re.search(r'(20\d{6})[_-]?(\d{6})?',path.stem)
    if m:
        try:return datetime.strptime(m.group(1)+(m.group(2) or ''),'%Y%m%d%H%M%S' if m.group(2) else '%Y%m%d')
        except ValueError:pass
    try:
        with Image.open(path) as im:
            exif=im.getexif()
            for tag in (36867,36868,306):
                if exif.get(tag):return datetime.strptime(str(exif[tag])[:19],'%Y:%m:%d %H:%M:%S')
    except Exception:pass
    return datetime.fromtimestamp(path.stat().st_mtime)

rows=[]
for path in sorted(SRC.rglob('*')):
    if path.suffix.lower() not in {'.jpg','.jpeg','.png','.webp'}:continue
    dt=date_for(path)
    with Image.open(path) as im:
        rows.append({'path':str(path.relative_to(ROOT)).replace('\\','/'),'name':path.name,'date':dt.isoformat(),
                     'width':im.width,'height':im.height,'in_period':START<=dt<=END})

eligible=[r for r in rows if r['in_period']]
font=ImageFont.load_default()
for start in range(0,len(eligible),24):
    sheet=Image.new('RGB',(1600,1200),'#dbe7f3');draw=ImageDraw.Draw(sheet)
    for j,r in enumerate(eligible[start:start+24]):
        path=ROOT/r['path'];im=Image.open(path).convert('RGB');im.thumbnail((250,230))
        x=(j%6)*266+8;y=(j//6)*300+8
        frame=Image.new('RGB',(250,230),'white');frame.paste(im,((250-im.width)//2,(230-im.height)//2));sheet.paste(frame,(x,y))
        label=f"{start+j+1:03d} {r['name'][:27]}\n{r['date'][:10]}"
        draw.multiline_text((x,y+234),label,fill='#0b2545',font=font,spacing=2)
    sheet.save(OUT/f'contact-{start//24+1:02d}.jpg',quality=90)
(OUT/'catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'all':len(rows),'eligible':len(eligible),'excluded':len(rows)-len(eligible),'sheets':(len(eligible)+23)//24},ensure_ascii=False))
