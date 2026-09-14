from pathlib import Path
import json, re
from io import BytesIO
import pymupdf
from PIL import Image
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
doc=Document(ROOT/'deliverables/รายงาน PA 2569 ฉบับตกแต่ง.docx')
pdf=pymupdf.open(ROOT/'deliverables/รายงาน PA 2569 ฉบับตกแต่ง.pdf')
out=ROOT/'tmp/indicator-evidence'
out.mkdir(parents=True,exist_ok=True)
verified=json.loads((ROOT/'qa-pa/photo-curation-20260913.json').read_text(encoding='utf-8'))['verified']
photos={p['id']:p for p in verified}
certificate='assets_drop/06_ภาพเกียรติบัตรและรางวัล/LINE_ALBUM_อนันตชัย_260712_1.jpg'
# Document excerpts are explicitly identified as report material, not independent proof.
mapping={
 '1.1':(15,70,390,'กำหนดการจัดการเรียนรู้และมาตรฐานที่ใช้ในรายงาน'),
 '1.2':(16,70,590,'แผนการจัดการเรียนรู้ที่ 5 และขั้นตอนกิจกรรม'),
 '1.3':'p1-code',
 '1.4':'p1-media',
 '1.5':(28,58,432,'บัญชีคะแนนก่อนและหลังเรียนที่บันทึกไว้ในรายงาน'),
 '1.6':(30,70,400,'บันทึกการช่วยเหลือผู้เรียนและวิธีติดตามรายบุคคล'),
 '1.7':'p1-practice',
 '1.8':(31,70,680,'แบบสังเกตคุณลักษณะและการช่วยเหลือผู้เรียนในรายงาน'),
 '2.1':(28,58,432,'ข้อมูลผู้เรียนและผลการเรียนรายบุคคลในรายงาน'),
 '2.2':(32,70,420,'แผนช่วยเหลือและภารกิจต่อยอดในชั้นเรียน ไม่ใช่หลักฐานเยี่ยมบ้าน'),
 '2.3':'clean-may',
 '2.4':'board-june',
 '3.1':'certificate',
 '3.2':'certificate',
 '3.3':'p1-media',
}
manifest=[]
for p in doc.paragraphs:
    if p.text=='ทะเบียนการพัฒนาตนเองและงานชุมชน':
        p.paragraph_format.page_break_before=True
for heading in list(doc.paragraphs):
    match=re.match(r'^([123]\.\d+) ',heading.text)
    if not match:continue
    key=match.group(1)
    table=heading._p.getnext()
    assert table.tag==qn('w:tbl'),key
    # One indicator per page keeps the written account and its image together.
    previous=heading._p.getprevious()
    if previous is not None and previous.tag==qn('w:p'):
        style=previous.find('w:pPr/w:pStyle',previous.nsmap)
        if style is not None and style.get(qn('w:val'),'').startswith('Heading'):
            from docx.text.paragraph import Paragraph
            Paragraph(previous,doc).paragraph_format.page_break_before=True
        else:heading.paragraph_format.page_break_before=True
    else:heading.paragraph_format.page_break_before=True
    item=mapping[key]
    if isinstance(item,tuple):
        page,y0,y1,title=item
        path=out/f'document-{key}.png'
        pdf[page-1].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(60,y0,540,y1)).save(path)
        caption=f'ภาพเอกสารประกอบข้อ {key} {title}'
        detail='ที่มา เอกสารประกอบในเล่มรายงานฉบับนี้ เป็นภาพสรุปข้อมูลเอกสาร ไม่ใช่ภาพถ่ายกิจกรรมหรือหลักฐานตรวจสอบอิสระ'
    elif item=='certificate':
        path=ROOT/certificate
        caption=f'ภาพหลักฐานข้อ {key} เกียรติบัตร AI Learning Hub และ OBEC Content Center'
        detail='วันที่ 7 มิถุนายน 2569 ออกโดย สพป.กำแพงเพชร เขต 2 ระบุชื่อนายอนันตชัย เพ็ชรรี่'
        if key=='3.2':detail+=' ใช้ประกอบการแลกเปลี่ยนเรียนรู้ออนไลน์ ไม่ยืนยันการเข้าร่วม PLC ในโรงเรียนหรือจำนวนชั่วโมง PLC'
    else:
        p=photos[item];path=ROOT/p['src']
        caption=f"ภาพหลักฐานข้อ {key} {p['title']}"
        detail=f"วันที่ {p['day']} เวลา {p['time']} {p['caption']}"
        if key=='3.3':detail+=' ใช้ประกอบการนำสื่อไปใช้เท่านั้น ไม่ยืนยันความเชื่อมโยงกับหลักสูตรอบรมโดยลำพัง'
    anchor=table
    p=doc.add_paragraph(caption)
    p.paragraph_format.space_before=Pt(8)
    p.paragraph_format.keep_with_next=True
    for r in p.runs:r.font.name='TH SarabunPSK';r.font.size=Pt(14);r.bold=True
    anchor.addnext(p._p);anchor=p._p
    im=Image.open(path);w,h=im.size
    stream=BytesIO();im.convert('RGB').save(stream,format='PNG');stream.seek(0)
    width=min(15.7,10.2*w/h)
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next=True
    p.add_run().add_picture(stream,width=Cm(width))
    anchor.addnext(p._p);anchor=p._p
    p=doc.add_paragraph(detail)
    p.paragraph_format.space_after=Pt(6)
    for r in p.runs:r.font.name='TH SarabunPSK';r.font.size=Pt(12);r.font.color.rgb=RGBColor(0,0,0)
    anchor.addnext(p._p)
    manifest.append({'indicator':key,'source':str(path.relative_to(ROOT)),'caption':caption,'limitation':detail})
assert len(manifest)==15
doc.save(ROOT/'deliverables/รายงาน PA 2569 พร้อมภาพรายตัวชี้วัด.docx')
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added evidence images for',len(manifest),'indicators')
