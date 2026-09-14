"""Build a grouped catalog without moving or deleting original evidence files."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import quote
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [
    ('main', '01', 'รายงานผลการปฏิบัติงาน', [
        ('รายงานผลการพัฒนางาน PA ปีงบประมาณ 2569', 'รายงานภาพรวม ข้อมูลผู้รับการประเมิน ภาระงาน และผลการปฏิบัติงาน', ['รายงานผลการพัฒนางาน PA 2569 นายอนันตชัย เพ็ชรรี่.docx'], 'ควรตรวจข้อมูลและการลงนามก่อนเสนอประเมิน'),
    ]),
    ('standards', '02', 'ข้อตกลงและหลักฐานตามมาตรฐานตำแหน่ง', [
        ('แบบข้อตกลงในการพัฒนางาน PA 1', 'ข้อตกลงตามมาตรฐานตำแหน่งและประเด็นท้าทาย', ['แบบข้อตกลงในการพัฒนางาน ไม่มีวิทยฐานะ.docx'], 'ตรวจทานปีงบประมาณ: หัวเอกสารระบุ 2568 แต่ช่วงวันที่เป็น 1 ต.ค. 2568 ถึง 30 ก.ย. 2569'),
        ('ภาระงาน ภาคเรียนที่ 2 ปีการศึกษา 2568', 'รายการสอนและหน้าที่ที่ได้รับมอบหมายในภาคเรียนที่ระบุ', ['ภาระงานของนายอนันตชัย  เพ็ชรรี่ปีการศึกษา-22568.docx'], 'ต้นฉบับระบุรวมเวลาสอน 23 ชั่วโมงต่อสัปดาห์ ไม่ใช้แทนตารางสอนภาคเรียนอื่น'),
        ('แผนพัฒนาตนเองรายบุคคล ปีการศึกษา 2568', 'ID Plan ด้านสมรรถนะและการพัฒนาวิชาชีพ', ['ID plan 2568.docx'], 'เอกสารเดิมระบุตำแหน่งครูผู้ช่วย ใช้อ้างอิงตามปีที่จัดทำ'),
    ]),
    ('challenge-docs', '03', 'ประเด็นท้าทายและเครื่องมือประเมิน', [
        ('รายงานประเด็นท้าทาย ป.1 จำนวน 11 คน', 'รายงานพร้อมแผนการจัดการเรียนรู้ ใบงาน และเครื่องมือประเมิน', ['รายงาน PA 2569 ครูอนันตชัย ป1 11คน ฉบับปรับปรุง.pdf', 'รายงาน PA 2569 ครูอนันตชัย ป1 11คน ฉบับปรับปรุง.docx'], 'ข้อมูลผลดำเนินงานในเล่มถึง 10 กันยายน 2569 ผลคะแนนต้องตรวจร่วมกับต้นฉบับในระบบ'),
    ]),
    ('support-docs', '04', 'การมีส่วนร่วมและหลักฐานประกอบ', [
        ('รายงานโครงการส่งเสริมความสัมพันธ์ชุมชน', 'หลักฐานการดำเนินโครงการและความร่วมมือกับชุมชน', ['แบบรายงานผลการปฏิบัติงานตามโครงการสัมพันชุมชน.pdf'], ''),
        ('แฟ้มสะสมผลงานครูเจมส์', 'ประวัติ ผลงาน และหลักฐานประกอบในแฟ้มสะสมผลงาน', ['Portfolioครูเจมส์.pdf'], 'ตรวจช่วงปีของแต่ละหลักฐานก่อนใช้อ้างอิงในรอบประเมินนี้'),
    ]),
]
ARCHIVE = [
    ('รายงานผลตามข้อตกลง PA 69 ฉบับรวบรวมเดิม', 'มีข้อมูลภาระงานและรายวิชาต่างจากชุดรายงานปัจจุบัน ต้องตรวจเนื้อหาก่อนใช้อ้างอิง', ['รายงานผล_ตามข้อตกลง(PA)69_ครูอนันตชัย_เพ็ชรรี่.docx'], 'ไม่จัดเป็นเล่มหลัก'),
    ('รายงาน PA ป.1 ฉบับหลักฐานจริงเดิม', 'เก็บแยกจากฉบับปรับปรุงเพื่อป้องกันการเลือกผิดเวอร์ชัน', ['รายงาน PA ป1 ฉบับหลักฐานจริง 2569 นายอนันตชัย เพ็ชรรี่.docx'], 'ฉบับเดิมสำหรับตรวจเทียบ'),
]
manifest = []


def row(item, code):
    title, description, files, note = item
    actions = []
    for filename in files:
        file = ROOT / 'assets/docs' / filename
        assert file.is_file(), filename
        size = file.stat().st_size
        label = f'{size/1024/1024:.1f} MB' if size >= 1024*1024 else f'{size/1024:.0f} KB'
        fmt = file.suffix[1:].upper()
        attrs = 'target="_blank" rel="noopener noreferrer"' if fmt == 'PDF' else 'download'
        icon = 'file-text' if fmt == 'PDF' else 'download'
        actions.append(f'<a class="document-file" href="assets/docs/{quote(filename)}" {attrs} aria-label="{escape(title)} {fmt}"><i data-lucide="{icon}" aria-hidden="true"></i><span>{fmt}<small>{label}</small></span></a>')
        manifest.append({'code':code, 'title':title, 'file':str(file.relative_to(ROOT)).replace('\\','/'), 'bytes':size, 'note':note})
    return f'<li class="document-row"><span class="document-code">{code}</span><div class="document-copy"><h4>{escape(title)}</h4><p>{escape(description)}</p>{f"<p class=\"document-note\">{escape(note)}</p>" if note else ""}</div><div class="document-actions">{"".join(actions)}</div></li>'


nav = ''.join(f'<a href="#documents-{key}">{number} {escape(title)}</a>' for key,number,title,_ in GROUPS)
parts = ['<section id="downloads" class="section-block"><div class="container document-library"><div class="section-header"><div class="section-badge">เอกสารและหลักฐาน</div><h2 class="section-title">เอกสารประกอบการประเมิน PA</h2><p class="section-desc">รอบ 1 ตุลาคม 2568 ถึง 30 กันยายน 2569</p></div>', f'<nav class="document-index" aria-label="หมวดเอกสาร">{nav}</nav>']
for key, number, title, items in GROUPS:
    parts.append(f'<div class="document-group" id="documents-{key}"><h3><span>{number}</span>{escape(title)}</h3><ul class="document-list">')
    parts.extend(row(item, f'{number}.{i}') for i,item in enumerate(items,1))
    parts.append('</ul></div>')
parts.append('<details class="document-archive"><summary>ฉบับเดิมและไฟล์สำหรับตรวจเทียบ <span>2 รายการ</span></summary><ul class="document-list">')
parts.extend(row(item,f'เดิม {i}') for i,item in enumerate(ARCHIVE,1))
parts.append('</ul></details></div></section>')


class SectionRange(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.offsets = [0]
        for line in text.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1]+len(line))
        self.depth = 0
        self.match = None
        self.feed(text)
    def pos(self):
        line,col = self.getpos()
        return self.offsets[line-1]+col
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            if dict(attrs).get('id') == 'downloads':
                self.start = self.pos()
                self.depth = 1
            elif self.depth:
                self.depth += 1
    def handle_endtag(self, tag):
        if tag == 'section' and self.depth:
            self.depth -= 1
            if not self.depth:
                self.match = (self.start,self.pos()+len('</section>'))


path = ROOT/'index.html'
source = path.read_text(encoding='utf-8')
start,end = SectionRange(source).match
source = source[:start] + '\n'.join(parts) + source[end:]
if 'assets/document-library.css' not in source:
    source = source.replace('</head>', '<link rel="stylesheet" href="assets/document-library.css">\n</head>', 1)
path.write_text(source,encoding='utf-8')
shutil.copy2(path,ROOT/'website/index.html')
(ROOT/'qa-pa/document-catalog-20260914.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Organized {len(manifest)} files; all original paths preserved.')
