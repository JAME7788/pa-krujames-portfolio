from pathlib import Path
from curate_current_web import Document, ROOT, PHOTOS, figure
import shutil

for relative in ('index.html', 'embeds/canva-slides-krujames.html'):
    path = ROOT / relative
    d = Document(path.read_text(encoding='utf-8'))
    if relative.startswith('embeds/'):
        activities = d.by_id('slide-activities')
        d.replace(activities, '<section id="slide-activities" class="slide-page"><div class="slide-header-stripe"></div><div class="slide-inner"><h2 class="slide-title">ความร่วมมือและงานสนับสนุนสถานศึกษา</h2><p class="evidence-source">ภาพกิจกรรมที่ตรวจวันจาก Google Photos แล้ว ไม่ใช้แทนภาพเยี่ยมบ้านหรือประชุมผู้ปกครอง</p><div class="reviewed-photo-grid">' + ''.join(figure(p, '../') for p in PHOTOS[3:]) + '</div></div></section>')
    for n in d.nodes:
        if n.tag == 'script' and 'function hydrateCustomGallery' in d.raw(n):
            d.replace(n, '<!-- Published evidence uses reviewed HTML. Legacy local/cloud photo overrides are not applied. -->')
        if n.has('hero-thumb-strip'):
            d.replace(n, '')
        if n.has('stat-deck'):
            values = [('11', 'ผู้เรียน ป.1'), ('4', 'แผนฝึกเมาส์'), ('200', 'นาทีตามแผน'), ('5', 'ภาพตรวจสอบแล้ว')]
            d.replace(n, '<div class="stat-deck">' + ''.join(f'<div class="stat-tile"><div class="num">{v}</div><div class="lbl">{label}</div></div>' for v,label in values) + '</div>')
    text = d.render()
    replacements = {
      'ป.1 ผ่านทักษะปฏิบัติเมาส์ (ครบ ๑๑ คน)': 'ผ่านจุดประสงค์แผน 8 ตามระบบ (11/11 คน)',
      'พัฒนาทักษะเมาส์ด้วย Gamification + Active Learning สำเร็จ ๑๐๐% (๑๑ คน)': 'พัฒนาทักษะเมาส์ด้วย Gamification + Active Learning ป.1 จำนวน 11 คน; ระบบแผนที่ 8 บันทึกผ่าน 11 คน',
      'นักเรียนทั้ง ๑๑ คน (๑๐๐%) ผ่านเกณฑ์การประเมินรูบริกส์ ๔ ทักษะปฏิบัติ โดยสามารถใช้เมาส์ปฏิบัติงานได้ด้วยตนเองอย่างถูกต้องคล่องแคล่ว': 'ระบบแผนที่ 8 บันทึกผ่านจุดประสงค์ 11/11 คน ตรวจอ่าน 12 กันยายน 2569; ยังไม่สรุประดับรูบริกรายบุคคลหรือคะแนนก่อน–หลังจากภาพ',
      'นักเรียนชั้น ป.๑ ครบทั้ง ๑๑ คน (๑๐๐%) ผ่านเกณฑ์การประเมินระดับดีและปานกลาง สามารถบังคับเมาส์เข้าสู่บทเรียนและทำแบบฝึกปฏิบัติบนคอมพิวเตอร์ได้ด้วยตนเองอย่างมั่นใจ': 'ระบบแผนที่ 8 บันทึกผ่านจุดประสงค์ 11/11 คน ส่วนค่าเฉลี่ย K/P ยังต้องตรวจสอบกับคะแนนต้นฉบับ และครูผู้สอนรายงานว่าทักษะดีขึ้นทุกคน',
      'Gamification ป.1 ADDIE Model ผลลัพธ์รูบริกส์ 4 ทักษะ ผ่านเกณฑ์ 11/11 คน (100%)': 'Gamification ป.1 จำนวน 11 คน; ระบบแผนที่ 8 บันทึกผ่านจุดประสงค์ 11/11 คน (ตรวจ 12 ก.ย. 2569)',
      'มีร่องรอยและเอกสารราชการรองรับครบถ้วนสมบูรณ์ 100%': 'ตรวจสอบเอกสารต้นฉบับประกอบแต่ละตัวชี้วัดก่อนเสนอประเมิน',
    }
    for old,new in replacements.items():
        text = text.replace(old,new)
    text = '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'
    path.write_text(text, encoding='utf-8', newline='\n')

# Keep the existing website mirror aligned; no originals are deleted.
for relative in ('index.html', 'embeds/canva-slides-krujames.html', 'assets/evidence-report.css', 'assets/evidence-report.js', 'assets/evidence/current-2569/volunteer-20260502.jpg'):
    destination = ROOT / 'website' / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, destination)
print('Photo pages finalized and mirrored.')
