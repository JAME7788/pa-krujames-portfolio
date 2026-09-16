from pathlib import Path
import json
import shutil
from html import escape
from curate_current_web import Document

root = Path(__file__).resolve().parents[1]
albums = json.loads((root/'albums_data.json').read_text(encoding='utf-8'))
new = {
    'album-1-1': [
        ('course-overview.png', 'คำอธิบายรายวิชาเทคโนโลยี ป.1 และกำหนดการสอนใน Kru James Soncom'),
        ('course-units.png', 'โครงสร้างรายวิชา ป.1 จำนวน 4 หน่วย พร้อมตัวชี้วัด ภาระงาน และเวลาเรียน')],
    'album-2-1': [('information-dashboard.png', 'ระบบสารสนเทศ Kru James Soncom สรุปการใช้งานและข้อมูลแยกชั้นเรียน โดยไม่แสดงรายชื่อนักเรียน')]
}
source = (root/'index.html').read_text(encoding='utf-8')
d = Document(source)
for album in albums:
    if album['id'] not in new:
        continue
    album['items'] = [dict(src='assets/evidence-web-20260916/'+file, caption=caption,
        date='บันทึกหน้าจอ ๑๖ ก.ย. ๒๕๖๙', date_iso='2026-09-16',
        date_basis='วันที่บันทึกภาพหน้าจอ ไม่ใช่วันที่จัดกิจกรรม', evidence_kind='screenshot')
        for file, caption in new[album['id']]]
    album['cover'] = album['items'][0]['src']
    album['reviewed_at'] = '2026-09-16'
    album['desc'] = ('ภาพหน้าจอจริงจาก Kru James Soncom ตรวจเมื่อ 16 กันยายน 2569 '
        'เป็นหลักฐานระบบและเอกสารที่ปรากฏในวันตรวจ ไม่ใช้แทนผลการประเมินผู้เรียนหรือวันที่ดำเนินกิจกรรม')
    card = d.by_id(album['id'].replace('album-', 'ind-'))
    gallery = next(n for n in d.nodes if card.start < n.start < card.end and n.has('ind-gallery-grid'))
    figs = []
    for item in album['items']:
        caption, src = escape(item['caption']), escape(item['src'])
        action = escape('openLightbox('+json.dumps(item['src'])+','+json.dumps(item['caption'],ensure_ascii=False)+')',quote=True)
        figs.append(f'<figure class="gallery-item reviewed-photo"><button type="button" class="evidence-zoom" onclick="{action}" aria-label="ขยายภาพ {caption}"><img src="{src}" alt="{caption}" loading="lazy"></button><figcaption><strong>{caption}</strong><p>บันทึกหน้าจอ 16 ก.ย. 2569</p></figcaption></figure>')
    d.replace(gallery, '<div class="ind-gallery-grid">'+''.join(figs)+'</div>')
source = d.render()
marker = 'const ALBUMS_DATA = '
start = source.index(marker)+len(marker)
_, end = json.JSONDecoder().raw_decode(source[start:])
source = source[:start]+json.dumps(albums,ensure_ascii=False,separators=(',',':'))+source[start+end:]
for folder in [root,root/'website']:
    (folder/'index.html').write_text(source,encoding='utf-8')
    (folder/'albums_data.json').write_text(json.dumps(albums,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copytree(root/'assets/evidence-web-20260916',root/'website/assets/evidence-web-20260916',dirs_exist_ok=True)
rows = json.loads((root/'qa-pa/report-indicators.json').read_text(encoding='utf-8'))
for row in rows:
    if row['id']=='1.1':
        row.update(result='มีคำอธิบายรายวิชาเทคโนโลยี ป.1 และโครงสร้างรายวิชาใน Kru James Soncom แสดง 4 หน่วยการเรียนรู้ เชื่อมตัวชี้วัด ภาระงาน และเวลาเรียน พร้อมภาพหน้าจอจริงที่ตรวจเมื่อ 16 กันยายน 2569',quantity='โครงสร้าง ป.1 จำนวน 4 หน่วย รวม 40 ชั่วโมงตามระบบ',next='หลักสูตรฉบับอนุมัติและบันทึกผลการใช้หลักสูตร ภาพหน้าจอไม่ได้ใช้แทนเอกสารรับรอง')
    if row['id']=='2.1':
        row.update(result='มีระบบสารสนเทศ Kru James Soncom สำหรับจัดการผู้เรียน รายวิชา คะแนน และสรุปการใช้งานแยกชั้นเรียน แนบภาพหน้าจอสรุปที่ไม่เปิดรายชื่อนักเรียน ตรวจเมื่อ 16 กันยายน 2569 ส่วนงานดูแล ม.1 ใช้ Teacher Hub เป็นแหล่งข้อมูลแยกต่างหาก',quantity='ภาพหน้าจอระบบสารสนเทศ 1 ภาพ พร้อมลิงก์ระบบต้นทาง',next='รายงานจาก Teacher Hub สำหรับงานดูแล ม.1 และวันที่ตัดยอดของแต่ละชุดข้อมูล')
(root/'qa-pa/report-indicators.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added 3 verified screenshots to indicators 1.1 and 2.1')
