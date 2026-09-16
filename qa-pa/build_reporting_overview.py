from pathlib import Path
from html import escape
import json
from curate_current_web import Document

ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT/'qa-pa/report-indicators.json').read_text(encoding='utf-8'))
albums = json.loads((ROOT/'albums_data.json').read_text(encoding='utf-8'))
counts = {a['id']: len(a['items']) for a in albums}
source = (ROOT/'index.html').read_text(encoding='utf-8')
doc = Document(source)
for row in rows:
    card = doc.by_id('ind-' + row['id'].replace('.', '-'))
    nodes = [n for n in doc.nodes if card.start < n.start < card.end]
    strong = next(n for n in nodes if n.tag == 'strong' and ('ผลการปฏิบัติงาน' in doc.raw(n) or 'ผลที่มีหลักฐานประกอบ' in doc.raw(n)))
    doc.replace(strong.parent, '<div class="report-result"><strong>ผลที่มีหลักฐานประกอบ</strong><p>' + escape(row['result']) + '</p></div>')
    metrics = next(n for n in nodes if n.has('ind-metrics-row'))
    doc.replace(metrics, '<div class="ind-metrics-row"><div class="ind-metric-item"><strong>ข้อมูลเชิงปริมาณ</strong><span>' + escape(row['quantity']) + '</span></div><div class="ind-metric-item"><strong>หลักฐานที่ต้องตรวจเพิ่ม</strong><span>' + escape(row['next']) + '</span></div></div>')

source = doc.render().replace('ตัวชี้วัด (Indicators) ที่เกิดขึ้นกับผู้เรียน:', 'เกณฑ์เป้าหมายตามข้อตกลง (ไม่ใช่ผลที่ยืนยันแล้ว):')
nav = ''.join(f'<a href="#ind-{r["id"].replace(".","-")}"><b>{r["id"]}</b> {escape(r["title"])}</a>' for r in rows)
bars = ''.join(f'<div class="report-bar-row"><span>{r["id"]} {escape(r["title"])}</span><div class="report-bar-track"><i style="width:{counts["album-"+r["id"].replace(".","-")]/7*100:.3f}%"></i></div><b>{counts["album-"+r["id"].replace(".","-")]}</b></div>' for r in rows)
summary = f'''<section id="report-overview" class="section-block report-overview"><div class="container">
<header><p class="report-eyebrow">ภาพรวมรายงาน · ปรับปรุง 16 กันยายน 2569</p><h2>ผลการปฏิบัติงานและหลักฐาน PA</h2><p>รอบ 1 ตุลาคม 2568 – 30 กันยายน 2569 · ข้อมูลสิ้นสุดตามวันที่ของแต่ละแหล่ง ไม่รวมกิจกรรมในอนาคต</p></header>
<dl class="report-facts"><div><dt>หัวข้อมาตรฐานตำแหน่ง</dt><dd>15 <small>ตัวชี้วัด</small></dd></div><div><dt>กลุ่มประเด็นท้าทาย</dt><dd>ป.1 <small>11 คน</small></dd></div><div><dt>แผนฝึกทักษะเมาส์</dt><dd>4 <small>แผน / 200 นาที</small></dd></div><div><dt>ข้อมูลดูแลชั้น ม.1</dt><dd class="report-pending">รอข้อมูล <small>Teacher Hub</small></dd></div></dl>
<div class="report-chart-layout"><figure class="report-chart"><figcaption><h3>ผลผ่านจุดประสงค์แผนที่ 8 · ป.1</h3><p>หน่วย: คน · จากบันทึกหลังสอนที่ตรวจเมื่อ 12 ก.ย. 2569</p></figcaption><div class="report-pass-number">11 / 11 <small>คน</small></div><div class="report-pass-bar" role="img" aria-label="ผ่านจุดประสงค์ 11 คนจาก 11 คน คิดเป็นร้อยละ 100"></div><p>ผ่าน 11 คน (100%) · ไม่ผ่าน 0 คน</p><p class="report-source">เป็นผลผ่านจุดประสงค์ตามบันทึก ไม่ใช่คะแนนก่อน–หลังหรือผลรูบริกรายทักษะ จึงยังไม่แสดงกราฟความก้าวหน้าที่ไม่มีคะแนนต้นฉบับ</p><a href="#challenge">ตรวจรายละเอียดประเด็นท้าทาย</a><h3>ข้อมูลการเช็กและติดตาม ม.1</h3><p>แหล่งหลัก: Teacher Hub ของโรงเรียน ครอบคลุมการเช็กชื่อ โฮมรูม ชุมนุม นม แปรงฟัน และเงินออมตามเมนูที่ครูระบุ</p><p class="report-waiting">ยังไม่ได้อ่านยอดจากระบบ จึงไม่แสดงจำนวนผู้เรียน อัตรามาเรียน หรือผลดำเนินงานเป็นศูนย์แทนข้อมูลที่ขาด</p><a href="https://school-website-three-puce.vercel.app/teacher-hub" target="_blank" rel="noopener noreferrer">เปิด Teacher Hub (เฉพาะผู้มีสิทธิ์)</a></figure>
<figure class="report-chart"><figcaption><h3>ภาพประกอบแยกตามตัวชี้วัด</h3><p>หน่วย: ภาพ · จำนวนภาพที่คัดไว้ในเว็บ ไม่ใช่คะแนนหรือร้อยละความสำเร็จ</p></figcaption>{bars}<p class="report-source">0 ภาพหมายถึงยังไม่มีภาพตรงหัวข้อในชุดที่คัด ไม่ได้หมายความว่าไม่มีการปฏิบัติงาน เอกสารและข้อมูลระบบพิจารณาแยกจากภาพ</p></figure></div>
<nav class="report-indicator-nav" aria-label="เปิดรายงานครบ 15 ตัวชี้วัด">{nav}</nav>
<p class="report-source">แหล่งข้อมูล: แบบข้อตกลงและรายงานในแฟ้ม PA, บันทึกแผนที่ 8, คลังภาพที่ตรวจวันที่ 15 ก.ย. 2569 และคลังผลงานนักเรียน ข้อมูล ม.1 แยกจาก ป.1 และไม่เผยแพร่ข้อมูลสุขภาพ การเงิน หรือครัวเรือนรายบุคคล</p>
</div></section>'''
if 'id="report-overview"' in source:
    d = Document(source)
    d.replace(d.by_id('report-overview'), summary)
    source = d.render()
else:
    source = source.replace('  <section id="workload"', summary + '\n  <section id="workload"', 1)
assert 'id="report-overview"' in source
for file in ('index.html','website/index.html'):
    (ROOT/file).write_text(source, encoding='utf-8')
print('Updated 15 result summaries and reporting overview')
