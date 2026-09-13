"""Curate dated evidence without rewriting unrelated HTML formatting."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Node:
    def __init__(self, tag, attrs, start, opening, parent):
        self.tag, self.attrs, self.start, self.opening, self.parent = tag, dict(attrs), start, opening, parent
        self.end = start + opening

    def has(self, name):
        return name in self.attrs.get('class', '').split()


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.nodes, self.stack, self.edits = source, [], [], []
        self.lines = [0]
        for line in source.splitlines(keepends=True):
            self.lines.append(self.lines[-1] + len(line))
        self.feed(source)

    def position(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.position(), len(self.get_starttag_text()), self.stack[-1] if self.stack else None)
        self.nodes.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i].tag == tag:
                self.stack[i].end = self.source.index('>', self.position()) + 1
                self.stack = self.stack[:i]
                break

    def raw(self, n):
        return self.source[n.start:n.end]

    def replace(self, n, value):
        self.edits.append((n.start, n.end, value))

    def by_id(self, value):
        return next(n for n in self.nodes if n.attrs.get('id') == value)

    def render(self):
        # Parent replacements deliberately subsume edits to their descendants.
        selected = []
        for a, b, value in sorted(self.edits, key=lambda e: (e[0], -e[1])):
            if selected and a < selected[-1][1]:
                assert b <= selected[-1][1], 'Overlapping HTML edits'
                continue
            selected.append((a, b, value))
        result = self.source
        for a, b, value in reversed(selected):
            result = result[:a] + value + result[b:]
        return result


PHOTOS = [
    dict(id='p1-code', src='assets/evidence/media_pa/IMG_20260910_133441_1_.jpg', date='2026-09-10', time='13:34:41', day='10 กันยายน 2569', category='active-learning', indicators=['1.3'], title='ฝึกใช้เมาส์กับบล็อกคำสั่ง Code.org', caption='ผู้เรียนฝึกควบคุมเมาส์และจัดเรียงบล็อกคำสั่งบน Code.org ในห้องคอมพิวเตอร์ ภาพนี้เป็นการใช้สื่อภายนอก ไม่ใช่หลักฐานการสร้าง Code.org ขึ้นเอง'),
    dict(id='p1-media', src='assets/evidence/media_pa/IMG_20260910_133646.jpg', date='2026-09-10', time='13:36:46', day='10 กันยายน 2569', category='gamification', indicators=['1.4'], title='ใช้สื่อเกมฝึกเมาส์ Kru James Soncom', caption='หน้าจอเกมฝึกเมาส์บนเว็บไซต์ห้องเรียนครูเจมส์ขณะผู้เรียนใช้งาน ใช้ประกอบการรายงานการนำสื่อดิจิทัลไปใช้จัดกิจกรรม'),
    dict(id='p1-practice', src='assets/evidence/media_pa/IMG_20260910_133655.jpg', date='2026-09-10', time='13:36:55', day='10 กันยายน 2569', category='active-learning gamification', indicators=['1.3', '1.7'], title='ติดตามการใช้เมาส์ผ่านภารกิจดิจิทัล', caption='ผู้เรียนใช้เมาส์ทำกิจกรรมหน้าจอคอมพิวเตอร์ เป็นภาพการฝึกและติดตามทักษะวันที่ 10 กันยายน ไม่ใช่ภาพยืนยันคะแนนรายบุคคลหรือผลผ่านทั้งชั้น'),
    dict(id='board-june', src='assets_drop/2569_คณะกรรมการสถานศึกษา_สัมพันธ์ชุมชน/board_04.jpg', date='2026-06-18', time='17:34:16', day='18 มิถุนายน 2569', category='community', indicators=['2.4'], title='ประชุมคณะกรรมการสถานศึกษา', caption='การประชุมคณะกรรมการสถานศึกษา ณ โรงเรียนบ้านคลองมดแดง ใช้ประกอบการรายงานการประสานความร่วมมือกับเครือข่าย ไม่ใช้แทนภาพประชุมผู้ปกครองหรือเยี่ยมบ้าน'),
    dict(id='clean-may', src='assets/evidence/current-2569/volunteer-20260502.jpg', date='2026-05-02', time='09:46:01', day='2 พฤษภาคม 2569', category='volunteer', indicators=['2.3'], title='ร่วมทำความสะอาดอาคารสถานศึกษา', caption='ผู้ร่วมกิจกรรมช่วยกันล้างและทำความสะอาดพื้นที่อาคาร ใช้ประกอบงานสนับสนุนสถานศึกษาและจิตอาสา ไม่ใช้แทนการประชุม PLC'),
]


def figure(p, prefix='', gallery=False):
    src = prefix + p['src']
    cap = f"{p['title']} | {p['day']} | {p['caption']}"
    attrs = escape(json.dumps(src, ensure_ascii=False) + ', ' + json.dumps(cap, ensure_ascii=False), quote=True)
    cls = 'gallery-item reviewed-photo' if gallery else 'reviewed-photo'
    return f'''<figure class="{cls}" data-cat="{p['category']}" data-evidence-id="{p['id']}">
      <button type="button" class="evidence-zoom" onclick="openLightbox({attrs})" aria-label="ขยายภาพ {escape(p['title'])}">
        <img src="{escape(src)}" alt="{escape(p['title'])}" loading="lazy" width="1600" height="1200">
      </button>
      <figcaption><time datetime="{p['date']}">{p['day']}</time><strong>{escape(p['title'])}</strong>
      <p>{escape(p['caption'])}</p><small>ตัวชี้วัด {', '.join(p['indicators'])} · ตรวจวันจาก Google Photos</small></figcaption>
    </figure>'''


def lesson_content(prefix=''):
    rows = ''.join(f'<tr><td>{num}</td><td>{title}</td><td>{date}</td><td>50 นาที</td><td>สอนแล้ว</td></tr>' for num, title, date in [
        (5, 'จับเมาส์และเคลื่อนตัวชี้', '17 มิ.ย. 2569'), (6, 'คลิกหนึ่งครั้งและดับเบิลคลิก', '24 มิ.ย. 2569'),
        (7, 'ลากและวางวัตถุ', '1 ก.ค. 2569'), (8, 'เลื่อนหน้าและภารกิจเมาส์ครบชุด', '8 ก.ค. 2569')])
    return f'''<div class="reviewed-learning">
      <p class="evidence-source">ข้อมูลจากระบบห้องเรียนครูเจมส์ ตรวจเมื่อ 12 กันยายน 2569 · ป.1 ปีการศึกษา 2569 จำนวน 11 คน</p>
      <h3>แผนการจัดการเรียนรู้ 4 แผน รวม 200 นาที</h3>
      <div class="evidence-table-scroll"><table class="styled-table"><thead><tr><th>แผน</th><th>เรื่อง</th><th>วันที่ตามแผน</th><th>เวลา</th><th>สถานะในระบบ</th></tr></thead><tbody>{rows}</tbody></table></div>
      <p>วันที่ในตารางเป็นกำหนดการตามแผน ส่วนภาพติดตามการฝึกทักษะถ่ายวันที่ 10 กันยายน 2569 ไม่ใช้ภาพนั้นยืนยันวันสอนย้อนหลัง</p>
      <h3>ผลการเรียนรู้และการประเมิน</h3>
      <dl class="learning-facts"><div><dt>กลุ่มประเด็นท้าทาย</dt><dd>ผู้เรียน ป.1 ปัจจุบัน 11 คน</dd></div>
      <div><dt>ผลที่ระบบบันทึกในแผนที่ 8</dt><dd>ผ่านจุดประสงค์ 11 จาก 11 คน ตามหน้าระบบที่ตรวจอ่าน</dd></div>
      <div><dt>ข้อสังเกตจากครูผู้สอน</dt><dd>ผู้เรียนใช้เมาส์ได้ดีขึ้นทุกคน ตามข้อมูลที่ครูผู้สอนให้ไว้</dd></div>
      <div><dt>คะแนนก่อน–หลัง / ค่าเฉลี่ย K และ P</dt><dd>รอตรวจสอบคะแนนต้นฉบับ เนื่องจากค่าสรุปหน้าระบบและข้อความหลังสอนยังไม่ตรงกัน</dd></div></dl>
      <p>หลักฐานการประเมินประกอบด้วยแบบทดสอบความรู้ แบบสังเกตทักษะปฏิบัติ และบันทึกคุณลักษณะ ภาพกิจกรรมแสดงการลงมือทำ แต่ไม่ใช้อนุมานคะแนนหรือกำหนดระดับรูบริกของผู้เรียนแต่ละคน</p>
      <a href="https://krujamesoncom-website.vercel.app/admin" target="_blank" rel="noopener">แหล่งข้อมูล: ระบบครู (ต้องมีสิทธิ์เข้าถึง)</a>
      <div class="reviewed-photo-grid">{''.join(figure(p, prefix) for p in PHOTOS[:3])}</div>
    </div>'''


def update(path):
    source = path.read_text(encoding='utf-8')
    d = Document(source)
    slides = path.name != 'index.html'
    prefix = '../' if slides else ''
    if 'data-curation-version="2026-09-13"' in source:
        return
    approved = {p['src']: p for p in PHOTOS}
    removed = []
    for n in d.nodes:
        if n.tag != 'img':
            continue
        src = n.attrs.get('src', '').removeprefix('../')
        if not src or src.startswith('assets/images/') or '/mascots/' in src:
            continue
        wrapper = n
        ancestor = n.parent
        while ancestor and ancestor.tag not in ('section', 'body'):
            if any(ancestor.has(c) for c in ('ind-gallery-item', 'gallery-item', 'timeline-thumb-box', 'photo-frame', 'evidence-img-frame')):
                wrapper = ancestor
                break
            ancestor = ancestor.parent
        if src in approved:
            d.replace(wrapper, figure(approved[src], prefix))
        else:
            removed.append(src)
            d.replace(wrapper, '')
    if not slides:
        challenge = d.by_id('challenge')
        d.replace(challenge, '<section id="challenge" class="section-block"><div class="container"><div class="section-header"><div class="section-badge">ประเด็นท้าทาย</div><h2 class="section-title">พัฒนาทักษะการใช้เมาส์ ป.1</h2><p class="section-desc">Active Learning ร่วมกับสื่อเกมคอมพิวเตอร์</p></div>' + lesson_content() + '</div></section>')
        gallery = d.by_id('gallery')
        buttons = [('all', 'ทั้งหมด'), ('active-learning', 'การจัดการเรียนรู้'), ('gamification', 'การใช้สื่อ'), ('community', 'เครือข่ายชุมชน'), ('volunteer', 'งานสนับสนุนสถานศึกษา')]
        filters = ''.join(f'<button class="gallery-filter-btn {"active" if cat == "all" else ""}" onclick="filterGallery(\'{cat}\', this)">{label}</button>' for cat, label in buttons)
        d.replace(gallery, f'''<section id="gallery" class="section-block"><div class="container"><div class="section-header"><div class="section-badge">หลักฐานภาพกิจกรรม</div><h2 class="section-title">ภาพปฏิบัติงานในรอบประเมิน 2569</h2><p class="section-desc">1 ตุลาคม 2568 – 30 กันยายน 2569 · คัดภาพที่ตรวจวันและตรงกับกิจกรรมแล้ว</p></div><div class="gallery-filter-nav">{filters}</div><div id="gallery-container" class="reviewed-photo-grid">{''.join(figure(p, gallery=True) for p in PHOTOS)}</div><p class="evidence-source">ภาพเยี่ยมบ้าน ประชุมผู้ปกครอง การผลิตสื่อ และ PLC: รอคัดหลักฐานที่ยืนยันกิจกรรมและวันถ่าย ไม่ใช้ภาพจากคนละกิจกรรมทดแทน</p></div></section>''')
        cards = [n for n in d.nodes if n.has('indicator-card')]
        for i, card in enumerate(cards):
            groups = [n for n in d.nodes if n.has('ind-gallery-3') and card.start < n.start < card.end]
            chosen = {1: [0], 2: [1], 4: [2], 6: [3]}.get(i, [])
            for group in groups:
                html = '<div class="reviewed-photo-grid">' + ''.join(figure(PHOTOS[j]) for j in chosen) + '</div>' if chosen else '<p class="evidence-source">ใช้เอกสารและบันทึกงานประกอบตัวชี้วัดนี้ โดยไม่ใช้ภาพจากกิจกรรมอื่นแทนหลักฐาน</p>'
                d.replace(group, html)
    else:
        n = d.by_id('slide-challenge')
        d.replace(n, '<section id="slide-challenge" class="slide-page"><div class="slide-header-stripe"></div><div class="slide-inner"><h2 class="slide-title">ประเด็นท้าทาย: ทักษะการใช้เมาส์ ป.1</h2>' + lesson_content('../') + '</div></section>')
    # A single verified caption is used in the inline page and its lightbox.
    for n in d.nodes:
        if n.tag == 'script' and not n.attrs.get('src'):
            code = d.raw(n)
            if 'function hydrateCustomGallery' in code:
                code = code.replace("if (!Array.isArray(items) || items.length === 0) return;", "return; // Published evidence is curated in HTML; legacy CMS galleries are not evidence.", 2)
                d.replace(n, code)
            if 'function openLightbox(src, caption)' in code:
                start = code.index('      // Intercept and sanitize any outdated images / titles')
                end = code.index('      img.src = src;', start)
                code = code[:start] + '      // Keep the chosen image and its verified caption together.\n' + code[end:]
                d.replace(n, code)
    for n in d.nodes:
        if n.tag == 'head':
            end = n.end - len('</head>')
            d.edits.append((end, end, f'<link rel="stylesheet" href="{prefix}assets/evidence-report.css" data-curation-version="2026-09-13">\n<script defer src="{prefix}assets/evidence-report.js"></script>\n'))
    result = d.render().replace('รอบ ๓๐ ก.ย. ๒๕๖๘ – ๑ ต.ค. ๒๕๖๙', 'รอบ ๑ ต.ค. ๒๕๖๘ – ๓๐ ก.ย. ๒๕๖๙')
    result = result.replace('สไลด์ ๓๔ แผ่น', 'สไลด์นำเสนอ')
    path.write_text(result, encoding='utf-8', newline='\n')
    return sorted(set(removed))


if __name__ == '__main__':
    out = ROOT / 'assets/evidence/current-2569'
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path('C:/Users/KruJames/AppData/Local/Temp/browser-use/assets/02a21a0e-21cb-44bf-9232-bc1b86a30d32/c555e4a7035723d5'), out / 'volunteer-20260502.jpg')
    audit = {}
    for file in [ROOT / 'index.html', ROOT / 'embeds/canva-slides-krujames.html']:
        audit[str(file.relative_to(ROOT))] = update(file)
    (ROOT / 'qa-pa/photo-curation-20260913.json').write_text(json.dumps({'verified': PHOTOS, 'removed_from_display': audit}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: len(v or []) for k, v in audit.items()}, ensure_ascii=False))
