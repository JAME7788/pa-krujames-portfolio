"""Publish an explicit, visually reviewed photo selection; never infer events by date."""
from pathlib import Path
from html import escape
import hashlib
import json
import re
import shutil

from curate_current_web import Document

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'tmp/selected-pa-review'
CATALOG = json.loads((REVIEW / 'catalog.json').read_text(encoding='utf-8'))
ELIGIBLE = [p for p in CATALOG if p['in_period']]
THAI = str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙')
MONTHS = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']

# Numbers refer to the reviewed contact sheets, not to automatically inferred categories.
# Each activity has one primary home; related albums link to it instead of duplicating it.
SELECTION = {
    '1-1': [],
    '1-2': [(278, 'ครูอธิบายบทเรียนด้วยจอแสดงผลในห้องคอมพิวเตอร์'),
            (67, 'ครูอธิบายหน้าชั้นเรียนระหว่างกิจกรรมคอมพิวเตอร์')],
    '1-3': [(77, 'ครูแนะนำการใช้ชุดอุปกรณ์และโปรแกรมแก่ผู้เรียน'),
            (80, 'ผู้เรียนทดลองใช้อุปกรณ์ร่วมกับคอมพิวเตอร์'),
            (81, 'ผู้เรียนกลุ่มเล็กทำกิจกรรมร่วมกันที่คอมพิวเตอร์'),
            (145, 'ผู้เรียนทำงานประดิษฐ์จากกระดาษเป็นกลุ่ม'),
            (204, 'ผู้เรียนร่วมกันประกอบชุดอุปกรณ์บนพื้นห้องเรียน'),
            (275, 'ผู้เรียนร่วมเขียนงานบนกระดาษแผ่นใหญ่')],
    '1-4': [(196, 'หน้าจอสื่อเกมคำถามที่ใช้ในห้องคอมพิวเตอร์'),
            (94, 'ผู้เรียนตอบคำถามบนหน้าจอสัมผัส'),
            (121, 'ตัวอย่างบล็อกคำสั่งและภาพจากกล้องในโปรแกรม Scratch'),
            (186, 'ตัวอย่างฉากสามมิติในโปรแกรม CoSpaces'),
            (224, 'ผู้เรียนใช้คอมพิวเตอร์และหูฟังระหว่างกิจกรรมดิจิทัล'),
            (171, 'หน้าจอเว็บไซต์ห้องเรียนครูเจมส์ที่ผู้เรียนกำลังใช้งาน')],
    '1-5': [(236, 'ผู้เรียนทำงานบนกระดาษในห้องคอมพิวเตอร์'),
            (237, 'ผู้เรียนบันทึกคำตอบลงในกระดาษงานรายบุคคล'),
            (157, 'ผู้เรียนตอบคำถามในแบบฟอร์มออนไลน์')],
    '1-6': [(68, 'ครูให้คำแนะนำผู้เรียนขณะทำงานที่คอมพิวเตอร์'),
            (79, 'ครูเข้าช่วยเหลือผู้เรียนระหว่างใช้งานชุดอุปกรณ์')],
    '1-7': [(101, 'การจัดโต๊ะและคอมพิวเตอร์สำหรับกิจกรรมในห้องเรียน'),
            (55, 'บรรยากาศการทำงานเป็นกลุ่มย่อยในห้องคอมพิวเตอร์'),
            (246, 'ผู้เรียนใช้งานเครื่องคอมพิวเตอร์ที่จัดเรียงเป็นแถว')],
    '1-8': [(183, 'ครูพูดคุยกับผู้เรียนที่นั่งรวมกลุ่มบริเวณอาคารเรียน'),
            (151, 'ผู้เรียนร่วมพิธีไหว้ครู'),
            (259, 'ผู้เรียนเข้าร่วมกิจกรรมทางศาสนาในศาสนสถาน'),
            (53, 'ครูและผู้เรียนร่วมปลูกต้นไม้'),
            (169, 'ผู้เรียนแสดงความเคารพครูบริเวณอาคารเรียน')],
    '2-1': [],
    '2-2': [(285, 'เยี่ยมบ้านนักเรียนร่วมกับครอบครัว วันที่ 19 พฤษภาคม'),
            (288, 'เยี่ยมบ้านนักเรียน วันที่ 20 พฤษภาคม'),
            (290, 'พบผู้เรียนและครอบครัวระหว่างการเยี่ยมบ้าน'),
            (291, 'เยี่ยมบ้านและพบผู้ปกครอง วันที่ 21 พฤษภาคม'),
            (292, 'ติดตามผู้เรียนร่วมกับครอบครัวที่บ้าน'),
            (294, 'คณะครูพบครอบครัวนักเรียนระหว่างการเยี่ยมบ้าน'),
            (47, 'กิจกรรมบริจาคและส่งมอบเสื้อผ้าเพื่อการช่วยเหลือ')],
    '2-3': [(35, 'ครูดูแลอุปกรณ์บริเวณโต๊ะคอมพิวเตอร์'),
            (60, 'ครูตรวจอุปกรณ์คอมพิวเตอร์ในห้องเรียน'),
            (161, 'ครูทำความสะอาดแป้นพิมพ์และอุปกรณ์คอมพิวเตอร์'),
            (73, 'การจัดโต๊ะเอกสารและผลงานในห้องเรียน'),
            (28, 'ครูและนักเรียนร่วมทาสีอุปกรณ์บริเวณสนาม')],
    '2-4': [(265, 'ประชุมผู้ปกครองนักเรียน ภาคเรียนที่ 1 ปีการศึกษา 2569'),
            (268, 'ครูพบผู้ปกครองและผู้เรียนในห้องเรียนหลังการประชุม'),
            (240, 'ผู้ปกครองร่วมประชุมในอาคารของโรงเรียน'),
            (74, 'การส่งมอบสิ่งของสนับสนุนให้แก่สถานศึกษา')],
    '3-1': [],
    '3-2': [(270, 'คณะครูประชุมร่วมกันรอบโต๊ะในห้องประชุม'),
            (64, 'คณะครูเข้าร่วมประชุม วันที่ 5 มกราคม'),
            (89, 'การประชุมคณะครู วันที่ 9 กุมภาพันธ์'),
            (153, 'การประชุมคณะครู วันที่ 10 มิถุนายน'),
            (232, 'การประชุมครูโดยใช้จอแสดงข้อมูลประกอบ วันที่ 1 กันยายน')],
    '3-3': [(188, 'ผู้เรียนใช้โปรแกรมสร้างฉากสามมิติ CoSpaces'),
            (119, 'ผู้เรียนทำงานกับบล็อกคำสั่งในโปรแกรม Scratch'),
            (198, 'ผู้เรียนใช้สื่อเกมคำถามร่วมกันในห้องคอมพิวเตอร์')],
    'pa-p1': [(250, 'ผู้เรียนฝึกใช้เมาส์กับกิจกรรมบล็อกคำสั่ง Code.org'),
              (252, 'ผู้เรียนทำกิจกรรม Code.org ที่เครื่องคอมพิวเตอร์'),
              (253, 'ผู้เรียนใช้เมาส์ควบคุมกิจกรรมบนเว็บไซต์ห้องเรียนครูเจมส์')],
    'big-cleaning': [(260, 'ร่วมฉีดน้ำและกวาดทำความสะอาดทางเดินอาคาร'),
                     (262, 'คณะครูร่วมล้างพื้นภายในอาคารเรียน')],
    'science-day': [(206, 'ผู้เรียนร่วมกิจกรรมหน้าป้ายสัปดาห์วิทยาศาสตร์'),
                    (212, 'ครูกล่าวหน้าป้ายสัปดาห์วิทยาศาสตร์'),
                    (213, 'ภาพหมู่ผู้ร่วมกิจกรรมสัปดาห์วิทยาศาสตร์'),
                    (216, 'การแสดงบนเวทีสัปดาห์วิทยาศาสตร์')],
    'ict-project': [(208, 'ผู้เรียนฝึกตัดต่อวิดีโอด้วยโปรแกรมบนคอมพิวเตอร์'),
                    (210, 'ผู้เรียนทำงานตัดต่อวิดีโอร่วมกับอุปกรณ์บันทึกภาพ'),
                    (200, 'ผู้เรียนทำกิจกรรมเกี่ยวกับชิ้นส่วนอุปกรณ์คอมพิวเตอร์'),
                    (134, 'ผู้เรียนทดลองใช้งานชุดอุปกรณ์หุ่นยนต์'),
                    (174, 'ผู้เรียนแสดงงานบล็อกคำสั่ง Scratch บนหน้าจอ')],
    'career-skills': [(4, 'ครูและผู้เรียนฝึกจัดผ้าประดับโต๊ะ'),
                     (43, 'ครูและผู้เรียนร่วมดูแลพื้นที่ปลูกพืช'),
                     (92, 'ผู้เรียนร่วมขุดและเตรียมพื้นที่ดิน'),
                     (114, 'ผู้เรียนฝึกประกอบอาหารด้วยเตาถ่าน'),
                     (137, 'ครูและผู้เรียนร่วมดูแลแปลงปลูกพืช'),
                     (191, 'ผู้เรียนรดน้ำและดูแลพื้นที่แปลงปลูก')],
    'school-board': [(165, 'การประชุมคณะกรรมการสถานศึกษา วันที่ 18 มิถุนายน'),
                     (166, 'ผู้เข้าร่วมประชุมคณะกรรมการสถานศึกษาร่วมพิจารณาเอกสาร')],
    'ethics-volunteer': [(52, 'ครูและผู้เรียนร่วมกิจกรรมตักบาตร'),
                         (106, 'ผู้เรียนร่วมตักบาตรในกิจกรรมของโรงเรียน'),
                         (178, 'ขบวนกิจกรรมทางศาสนาในชุมชน'),
                         (179, 'ครูและผู้เรียนร่วมกิจกรรมทางศาสนา'),
                         (244, 'คณะครูร่วมกิจกรรมเกี่ยวกับถังคัดแยกขยะ'),
                         (10, 'ผู้เรียนร่วมดูแลพื้นที่และสนามของโรงเรียน')],
    'duty-scout': [(12, 'ครูดูแลผู้เรียนบริเวณทางเข้าโรงเรียน'),
                   (57, 'คณะผู้บังคับบัญชาลูกเสือในกิจกรรมค่าย'),
                   (59, 'ภาพรวมกิจกรรมชุมนุมลูกเสือกลางแจ้ง'),
                   (201, 'ครูในเครื่องแบบลูกเสือดูแลผู้เรียนบริเวณทางเข้า'),
                   (228, 'ผู้บังคับบัญชาลูกเสือและผู้เรียนร่วมกิจกรรมหน้าเสาธง')],
    'code-of-conduct': [(23, 'ครูลงนามในพิธีรำลึกภายในสถานศึกษา'),
                        (217, 'คณะครูร่วมพิธีรำลึกในอาคารโรงเรียน')],
    'awards': [],
}

DESCRIPTIONS = {
    '1-1': 'หลักฐานหัวข้อนี้ควรเป็นหลักสูตร โครงสร้างรายวิชา และคำอธิบายรายวิชาที่ใช้จริง ขณะนี้แสดงแบบข้อตกลงเป็นเอกสารอ้างอิง ยังไม่มีภาพเอกสารหลักสูตรที่ยืนยันได้ในชุดภาพที่ตรวจ',
    '1-2': 'ภาพประกอบการจัดการเรียนรู้หน้าชั้นเรียน ตรวจรายละเอียดการออกแบบกิจกรรมร่วมกับแผนการสอนในส่วนประเด็นท้าทาย',
    '1-3': 'กิจกรรมลงมือปฏิบัติ การใช้ชุดอุปกรณ์ และการทำงานร่วมกันของผู้เรียน',
    '1-4': 'ภาพการนำสื่อดิจิทัลมาใช้และตัวอย่างหน้าจอสื่อ การใช้โปรแกรมภายนอกไม่ได้ยืนยันว่าครูเป็นผู้สร้างโปรแกรมนั้น',
    '1-5': 'ภาพการทำงานรายบุคคลและตอบแบบฟอร์ม ใช้ประกอบการประเมินร่วมกับเครื่องมือและคะแนนต้นฉบับ ภาพเพียงอย่างเดียวไม่ยืนยันคะแนนก่อน–หลัง',
    '1-6': 'ภาพประกอบการช่วยเหลือผู้เรียนระหว่างปฏิบัติ ต้องพิจารณาร่วมกับบันทึกปัญหาและผลการวิเคราะห์ จึงจะยืนยันกระบวนการศึกษาและแก้ปัญหาได้',
    '1-7': 'การจัดพื้นที่ อุปกรณ์ และบรรยากาศในห้องคอมพิวเตอร์',
    '1-8': 'กิจกรรมอบรมผู้เรียน ไหว้ครู ศาสนา และการร่วมดูแลสิ่งแวดล้อม',
    '2-1': 'ตรวจหลักฐานข้อมูลผู้เรียนและรายวิชาจากระบบห้องเรียนครูเจมส์และสรุปผลที่รายงาน ภาพนักเรียนเล่นเกมไม่ได้ยืนยันการจัดทำระบบสารสนเทศ',
    '2-2': 'การเยี่ยมบ้านหลายครอบครัวและกิจกรรมช่วยเหลือด้วยการบริจาคเสื้อผ้า',
    '2-3': 'การดูแลคอมพิวเตอร์ การจัดแสดงเอกสาร และงานสนับสนุนสถานศึกษา',
    '2-4': 'การพบผู้ปกครอง การประชุมผู้ปกครอง และการรับสิ่งของสนับสนุนสถานศึกษา',
    '3-1': 'เกียรติบัตรการอบรมที่ระบุชื่อครูและชื่อหลักสูตร อ่านรายละเอียดได้จากภาพเอกสาร',
    '3-2': 'ภาพการประชุมคณะครูต่างวัน ใช้ประกอบการแลกเปลี่ยนเรียนรู้ โดยรายละเอียด PLC และชั่วโมงต้องอ้างอิงบันทึกการประชุม',
    '3-3': 'ภาพประกอบการใช้ความรู้ด้านเทคโนโลยีในชั้นเรียน การเชื่อมโยงกับหลักสูตรอบรมต้องพิจารณาร่วมกับแผนและบันทึกการนำไปใช้',
    'pa-p1': 'ภาพติดตามการฝึกใช้เมาส์วันที่ 10 กันยายน 2569 ใช้ประกอบกลุ่มประเด็นท้าทาย ป.1 จำนวน 11 คน โดยไม่ใช้ภาพอนุมานคะแนนรายบุคคล',
    'big-cleaning': 'กิจกรรมทำความสะอาดอาคาร วันที่ 2 พฤษภาคม 2569 เลือกภาพต่างบริเวณ',
    'science-day': 'กิจกรรมสัปดาห์วิทยาศาสตร์ วันที่ 10–11 สิงหาคม 2569 ตามป้ายกิจกรรมและชื่อไฟล์ภาพ',
    'ict-project': 'การปฏิบัติงานเทคโนโลยีของผู้เรียน ทั้งตัดต่อวิดีโอ Scratch และชุดอุปกรณ์หุ่นยนต์',
    'career-skills': 'การฝึกทักษะชีวิต งานประดิษฐ์ งานเกษตร และการประกอบอาหารตามกิจกรรมที่ปรากฏในภาพ',
    'school-board': 'การประชุมคณะกรรมการสถานศึกษา วันที่ 18 มิถุนายน 2569',
    'ethics-volunteer': 'กิจกรรมทางศาสนา จิตอาสา และการดูแลสิ่งแวดล้อมของโรงเรียน',
    'duty-scout': 'การดูแลผู้เรียนและกิจกรรมลูกเสือในช่วงรอบประเมิน',
    'code-of-conduct': 'ภาพประกอบการร่วมพิธีของสถานศึกษา การประเมินวินัยและจรรยาบรรณต้องใช้ข้อมูลการปฏิบัติงานร่วมด้วย',
    'awards': 'ประกาศผล เกียรติบัตร และสื่อประชาสัมพันธ์รางวัล แยกจากภาพกิจกรรมทั่วไป',
}


def photo(index, caption):
    p = ELIGIBLE[index - 1]
    y, m, d = map(int, p['date'][:10].split('-'))
    assert '2025-10-01' <= p['date'][:10] <= '2026-09-30'
    src = 'assets/evidence_pa_photos/' + p['name']
    assert (ROOT / src).exists(), src
    return dict(src=src, caption=caption, date=f'{d} {MONTHS[m-1]} {y+543}'.translate(THAI),
                date_iso=p['date'][:10], date_basis='ชื่อไฟล์ภาพ', evidence_kind='photo')


def document_image(src, caption, date):
    assert (ROOT / src).exists(), src
    return dict(src=src, caption=caption, date=date, evidence_kind='document')


def thumbnail(item, category='all'):
    args = escape(json.dumps(item['src'], ensure_ascii=False) + ', ' + json.dumps(item['caption'] + ' · ' + item['date'], ensure_ascii=False), quote=True)
    return f'''<figure class="gallery-item reviewed-photo" data-cat="{category}">
      <button type="button" class="evidence-zoom" onclick="openLightbox({args})" aria-label="ขยายภาพ {escape(item['caption'])}">
      <img src="{escape(item['src'])}" alt="{escape(item['caption'])}" loading="lazy"></button>
      <figcaption><strong>{escape(item['caption'])}</strong><p>{item['date']}</p></figcaption></figure>'''


def main():
    before = json.loads((ROOT / 'albums_data.json').read_text(encoding='utf-8'))
    backup = REVIEW / 'albums-before-review-20260915.json'
    if not backup.exists():
        backup.write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding='utf-8')
    albums = []
    for old in before:
        key = old['id'].removeprefix('album-')
        a = dict(old)
        a['items'] = [photo(i, caption) for i, caption in SELECTION[key]]
        a['desc'] = DESCRIPTIONS[key]
        a['reviewed_at'] = '2026-09-15'
        # These legacy Google Photos albums still contain the rejected photographs.
        a.pop('share_url', None)
        a['shared'] = False
        a.pop('links', None)
        a.pop('related', None)
        albums.append(a)
    lookup = {a['id'].removeprefix('album-'): a for a in albums}
    cert = 'assets_drop/06_ภาพเกียรติบัตรและรางวัล/'
    award = 'assets_drop/2569_รางวัลและผลงานดีเด่น/'
    lookup['3-1']['items'] = [
        document_image(cert + 'LINE_ALBUM_อนันตชัย_260712_1.jpg', 'เกียรติบัตรอบรม AI Learning Hub และ OBEC Content Center', '๗ มิ.ย. ๒๕๖๙'),
        document_image(cert + 'Picture1.png', 'เกียรติบัตรอบรมการจัดการเรียนรู้ปัญญาประดิษฐ์ ม.1–3 จำนวน 20 ชั่วโมง', '๗ พ.ค. ๒๕๖๙'),
        document_image(cert + 'Picture2.png', 'เกียรติบัตรอบรมการจัดการเรียนรู้ปัญญาประดิษฐ์ ป.4–6 จำนวน 8 ชั่วโมง', '๗ พ.ค. ๒๕๖๙'),
    ]
    lookup['awards']['items'] = [
        document_image(award + '02_ประกาศสพป_กำแพงเพชรเขต2_TheSchoolCEO_ชนะเลิศเหรียญทอง.jpg', 'ประกาศผล The School CEO ระดับ ม.1–3 โรงเรียนบ้านคลองมดแดง ได้รับรางวัลชนะเลิศระดับเหรียญทอง', 'ปีงบประมาณ ๒๕๖๙'),
        document_image(award + '01_รางวัลชนะเลิศเหรียญทอง_TheSchoolCEO_คลิปสั้นปั้นธุรกิจ.jpg', 'สื่อประชาสัมพันธ์รางวัล The School CEO ผลงานเสน่ห์ผ้าทอปกาเกอะญอ', 'ปี ๒๕๖๙'),
        document_image(award + '03_รางวัลเหรียญทอง_ScienceShow_ศิลปหัตถกรรมนักเรียน_ครั้งที่74.jpg', 'สื่อประชาสัมพันธ์รางวัลเหรียญทอง Science Show ป.4–6 งานศิลปหัตถกรรมนักเรียน ครั้งที่ 74', 'ปีการศึกษา ๒๕๖๙'),
        document_image(cert + 'messageImage_1783918653571.jpg', 'เกียรติบัตรครูผู้ฝึกสอนนักเรียนเข้าร่วมประกวดสร้างสื่อด้วย AI ม.1–3', '๒๖ มิ.ย. ๒๕๖๙'),
        document_image('assets/evidence/award_computer_design_gold_m13.jpg', 'สื่อประชาสัมพันธ์รางวัลเหรียญทอง การออกแบบสิ่งของเครื่องใช้ด้วยโปรแกรมคอมพิวเตอร์ ม.1–3', 'ปีการศึกษา ๒๕๖๙'),
        document_image(award + '04_รางวัลรองชนะเลิศอันดับ2_ภาพถ่ายต่อต้านการทุจริต_ราคาของการถูกลืม.jpg', 'สื่อประชาสัมพันธ์รางวัลรองชนะเลิศอันดับ 2 ภาพถ่ายต่อต้านการทุจริต ราคาของการถูกลืม', 'ปี ๒๕๖๙'),
        document_image(award + '05_รางวัลอันดับ5_ภาพยนตร์สั้นต่อต้านการทุจริต_TheFalseGoalประตูที่ถูกล็อก.jpg', 'สื่อประชาสัมพันธ์รางวัลอันดับ 5 ภาพยนตร์สั้นต่อต้านการทุจริต The False Goal', 'ปี ๒๕๖๙'),
        dict(src='assets_drop/2569_ภาพกิจกรรมจริง_GooglePhotos/IMG_20260903_085548.jpg', caption='ครูแสดงโล่และเกียรติบัตรรางวัล The School CEO ที่บูธผลงาน', date='๓ ก.ย. ๒๕๖๙', date_iso='2026-09-03', evidence_kind='photo'),
    ]
    lookup['1-8']['items'].append(document_image('assets/evidence/waikru_memo_page1.jpg', 'บันทึกขออนุญาตดำเนินกิจกรรมวันไหว้ครู (เอกสารยังไม่มีลายมือชื่อ)', '๔ มิ.ย. ๒๕๖๙'))
    lookup['school-board']['items'].append(document_image('assets/evidence/board_meeting_report_page1.jpg', 'หน้าแรกรายงานการประชุมคณะกรรมการสถานศึกษา ครั้งที่ 1/2569', '๒๐ ม.ค. ๒๕๖๙'))
    lookup['science-day']['title'] = 'สัปดาห์วิทยาศาสตร์ 10–11 สิงหาคม 2569'
    lookup['ict-project']['title'] = 'ผลงานและกิจกรรมเทคโนโลยีของผู้เรียน'
    lookup['career-skills']['title'] = 'งานเกษตรและทักษะชีวิต'
    lookup['3-2']['title'] = 'ข้อที่ ๓.๒ การแลกเปลี่ยนเรียนรู้และการประชุมครู'
    agreement = dict(title='แบบข้อตกลงในการพัฒนางาน (เอกสารอ้างอิง)', href='assets/docs/แบบข้อตกลงในการพัฒนางาน ไม่มีวิทยฐานะ.docx')
    challenge = dict(title='แผนและผลการดำเนินงานประเด็นท้าทาย ป.1', href='#challenge')
    student_work = dict(title='คลังผลงานนักเรียน ปี 2569: Scratch และงานส่ง ม.1–3', href='https://drive.google.com/drive/folders/1mHl2FFJxfAw5Ng1Hd_XAhmkqmtcrZyEw')
    lookup['1-1']['links'] = [agreement]
    lookup['1-2']['links'] = [challenge]
    lookup['1-5']['links'] = [challenge, student_work]
    lookup['1-6']['links'] = [challenge]
    lookup['2-1']['links'] = [challenge, dict(title='ระบบห้องเรียนครูเจมส์ (สำหรับผู้มีสิทธิ์)', href='https://krujamesoncom-website.vercel.app/admin')]
    lookup['1-3']['links'] = [student_work]
    lookup['ict-project']['links'] = [student_work]
    lookup['3-3']['related'] = ['album-3-1', 'album-1-4']
    lookup['2-4']['related'] = ['album-school-board', 'album-2-2']
    lookup['2-3']['related'] = ['album-big-cleaning']
    lookup['pa-p1']['links'] = [challenge]
    for a in albums:
        a['cover'] = a['items'][0]['src'] if a['items'] else ''
    selected = [i['src'] for a in albums for i in a['items']]
    assert len(selected) == len(set(selected)), 'Duplicate photo placements'
    hashes = [hashlib.sha256((ROOT / src).read_bytes()).hexdigest() for src in selected]
    assert len(hashes) == len(set(hashes)), 'Identical images under different filenames'
    data = json.dumps(albums, ensure_ascii=False, separators=(',', ':'))
    approved = {i['src']: i for a in albums for i in a['items']}
    static_removed = []
    for html_path in [ROOT / 'index.html', ROOT / 'website/index.html']:
        html = html_path.read_text(encoding='utf-8')
        marker = 'const ALBUMS_DATA = '
        start = html.index(marker) + len(marker)
        _, length = json.JSONDecoder().raw_decode(html[start:])
        html = html[:start] + data + html[start+length:]
        doc = Document(html)
        grid = doc.by_id('album-grid-container')
        for n in doc.nodes:
            if n.tag != 'button':
                continue
            target = re.search(r"openAlbumModal\('album-([^']+)'\)", n.attrs.get('onclick', ''))
            if target and target.group(1) in lookup:
                count = str(len(lookup[target.group(1)]['items'])).translate(THAI)
                doc.replace(n, re.sub(r'\([๐-๙0-9]+ (?:รายการ|ภาพ)\)', f'({count} ภาพ)', doc.raw(n)))
        replaced_ranges = [(grid.start, grid.end)]
        for key, a in lookup.items():
            if not re.fullmatch(r'\d-\d', key):
                continue
            card = doc.by_id('ind-' + key)
            for gallery in [n for n in doc.nodes if n.has('ind-gallery-grid') and card.start < n.start < card.end]:
                content = ''.join(thumbnail(i) for i in a['items'][:2])
                if not content:
                    content = f'<p class="album-document-note">{escape(a["desc"])}</p>'
                doc.replace(gallery, '<div class="ind-gallery-grid">' + content + '</div>')
                replaced_ranges.append((gallery.start, gallery.end))
        gallery = doc.by_id('gallery-container')
        categories = {'comp1-teach':'active-learning', 'comp1-support':'community', 'comp1-dev':'community', 'comp2':'volunteer', 'comp3':'volunteer'}
        content = ''.join(thumbnail(item, 'gamification' if a['id']=='album-1-4' else categories.get(a['category'], 'active-learning')) for a in albums for item in a['items'])
        doc.replace(gallery, '<div class="reviewed-photo-grid" id="gallery-container">' + content + '</div>')
        replaced_ranges.append((gallery.start, gallery.end))
        challenge_section = doc.by_id('challenge')
        for n in doc.nodes:
            if n.has('ind-gallery-3') and challenge_section.start < n.start < challenge_section.end:
                doc.replace(n, '<div class="ind-gallery-3">' + ''.join(thumbnail(i) for i in lookup['pa-p1']['items']) + '</div>')
                replaced_ranges.append((n.start, n.end))
        timeline = doc.by_id('timeline')
        chronological = [photo(i, caption) for i, caption in [
            (35, 'ดูแลอุปกรณ์ห้องคอมพิวเตอร์'), (47, 'บริจาคและส่งมอบเสื้อผ้า'),
            (64, 'ประชุมคณะครู'), (262, 'ร่วมทำความสะอาดอาคาร'),
            (265, 'ประชุมผู้ปกครองนักเรียน'), (292, 'เยี่ยมบ้านนักเรียน'),
            (153, 'ประชุมคณะครู'), (166, 'ประชุมคณะกรรมการสถานศึกษา'),
            (188, 'ใช้สื่อสามมิติ CoSpaces ในชั้นเรียน'), (213, 'กิจกรรมสัปดาห์วิทยาศาสตร์'),
            (232, 'ประชุมครูโดยใช้จอแสดงข้อมูลประกอบ'), (253, 'ติดตามการฝึกใช้เมาส์')]]
        timeline_cards = ''.join(f'<div class="timeline-card"><div class="timeline-date-badge">{i["date"]}</div><div class="timeline-card-title">{escape(i["caption"])}</div>{thumbnail(i)}</div>' for i in chronological)
        doc.replace(timeline, '<section id="timeline" class="section-block"><div class="container"><div class="section-header"><h2 class="section-title">ลำดับภาพการปฏิบัติงานในรอบประเมิน</h2><p class="section-desc">1 ตุลาคม 2568 – 30 กันยายน 2569</p></div><div class="timeline-track">' + timeline_cards + '</div></div></section>')
        replaced_ranges.append((timeline.start, timeline.end))
        for n in doc.nodes:
            if n.tag != 'img' or 'green_culture' not in n.attrs.get('src', ''):
                continue
            parent = n.parent
            while parent and parent.tag != 'section':
                if 'onmouseover' in parent.attrs:
                    doc.replace(parent, '')
                    replaced_ranges.append((parent.start, parent.end))
                    break
                parent = parent.parent
        substitutions = {
            'assets_drop/2569_BigCleaning_สนับสนุนสถานศึกษา/cleaning_03.jpg': lookup['big-cleaning']['items'][1],
            'assets_drop/2569_BigCleaning_สนับสนุนสถานศึกษา/cleaning_01.jpg': lookup['big-cleaning']['items'][0],
            'assets_drop/2569_กิจกรรมส่งเสริมอาชีพ_ทักษะชีวิต/career_01.jpg': lookup['career-skills']['items'][-1],
            'assets_drop/2569_คณะกรรมการสถานศึกษา_สัมพันธ์ชุมชน/board_01.jpg': lookup['school-board']['items'][0],
            'assets_drop/2569_ค่ายวิชาการ_ActiveLearning/camp_02.jpg': lookup['science-day']['items'][0],
            'assets/evidence/waikru_activity.jpg': lookup['1-8']['items'][1],
        }
        for n in doc.nodes:
            if n.tag != 'img' or any(a <= n.start < b for a, b in replaced_ranges):
                continue
            src = n.attrs.get('src', '')
            item = substitutions.get(src) or approved.get(src)
            if not item:
                continue
            wrapper = n
            parent = n.parent
            while parent and parent.tag not in ('section', 'body'):
                if parent.tag == 'figure':
                    wrapper = parent
                    break
                if 'onclick' in parent.attrs and 'openLightbox(' in parent.attrs['onclick']:
                    wrapper = parent.parent if parent.parent and parent.parent.tag == 'figure' else parent
                    break
                parent = parent.parent
            if wrapper == n:
                continue
            doc.replace(wrapper, thumbnail(item))
            replaced_ranges.append((wrapper.start, wrapper.end))
        cards = []
        for a in albums:
            count = str(len(a['items'])).translate(THAI)
            cover = (f'<img class="album-cover-img" src="{escape(a["cover"])}" alt="{escape(a["title"])}" loading="lazy">'
                     if a['cover'] else '<div class="album-document-cover"><i data-lucide="files"></i><span>เอกสารประกอบตัวชี้วัด</span></div>')
            cards.append(f'''<div class="album-card" data-category="{a['category']}" onclick="openAlbumModal('{a['id']}')" role="button" tabindex="0" onkeydown="if(event.key==='Enter')this.click()">
              <div class="album-cover-box">{cover}<div class="album-badge-count">{count} ภาพ</div></div>
              <div class="album-card-body"><span class="album-card-badge">{escape(a['badge'])}</span>
              <div class="album-card-title">{escape(a['title'])}</div><div class="album-card-desc">{escape(a['desc'])}</div>
              <div class="album-card-footer"><span class="album-card-action">เปิดหลักฐาน</span></div></div></div>''')
        doc.replace(grid, '<div class="album-grid" id="album-grid-container">' + '\n'.join(cards) + '</div>')
        # Remove rejected static thumbnails as well as their album entries.
        for n in doc.nodes:
            if n.tag != 'img' or any(a <= n.start < b for a, b in replaced_ranges):
                continue
            src = n.attrs.get('src', '')
            if 'assets/evidence_pa_photos/' not in src:
                continue
            wrapper = n
            ancestor = n.parent
            while ancestor and ancestor.tag not in ('section', 'body'):
                if ancestor.tag == 'figure' or any(ancestor.has(c) for c in ('gallery-item', 'ind-gallery-item', 'timeline-thumb-box', 'photo-frame')):
                    wrapper = ancestor
                    break
                ancestor = ancestor.parent
            if src not in approved:
                doc.replace(wrapper, '')
                static_removed.append(src)
            elif wrapper.tag == 'figure':
                item = approved[src]
                doc.replace(wrapper, f'<figure class="reviewed-photo"><img src="{escape(src)}" alt="{escape(item["caption"])}" loading="lazy"><figcaption>{escape(item["caption"])} · {item["date"]}</figcaption></figure>')
        html = doc.render().replace('Google Photos Evidence', 'หลักฐานประกอบการรายงาน')
        html = html.replace(', รางวัลชมเชยระดับประเทศจากวุฒิสภา (คลิปวิดีโอ Green Culture)', '')
        html = html.replace('PA 2569 Verified', 'เอกสารประกอบตามหัวข้อ')
        html = html.replace('มุมมองอัลบั้มแยกตามข้อ (Google Photos View)', 'อัลบั้มหลักฐานแยกตามข้อ')
        html = html.replace('VERIFIABLE EVIDENCE GALLERY & GOOGLE PHOTOS ALBUMS', 'ภาพกิจกรรมและเอกสารประกอบ')
        for key in SELECTION:
            if not re.fullmatch(r'\d-\d', key):
                continue
            label = key.replace('-', '.').translate(THAI)
            count = str(len(lookup[key]['items'])).translate(THAI)
            html = re.sub(rf'ดู(?:อัลบั้มภาพ|หลักฐาน) ข้อ {re.escape(label)} \([๐-๙0-9]+ (?:รายการ|ภาพ)\)',
                          f'ดูหลักฐาน ข้อ {label} ({count} ภาพ)', html)
        if 'assets/photo-evidence-review.js' not in html:
            html = html.replace('</head>', '<link rel="stylesheet" href="assets/photo-evidence-review.css">\n<script defer src="assets/photo-evidence-review.js"></script>\n</head>')
        html_path.write_text(html, encoding='utf-8', newline='\n')
    (ROOT / 'albums_data.json').write_text(json.dumps(albums, ensure_ascii=False, indent=2), encoding='utf-8')
    shutil.copy2(ROOT / 'albums_data.json', ROOT / 'website/albums_data.json')
    baseline = json.loads(backup.read_text(encoding='utf-8'))
    old_items = [(a['id'], i) for a in baseline for i in a['items']]
    new_placement = {i['src']: a['id'] for a in albums for i in a['items']}
    audit = []
    for album_id, item in old_items:
        src = item['src']
        current = approved.get(src)
        reason = 'คัดออกจากเว็บ: ภาพมุมซ้ำ ภาพทั่วไป หรือบริบทยังไม่พอยืนยันหัวข้อเดิม'
        if '202509' in src:
            reason = 'คัดออก: อยู่นอกช่วง 1 ต.ค. 2568 – 30 ก.ย. 2569'
        elif current:
            reason = 'คงไว้และตรวจคำบรรยาย' if new_placement[src] == album_id else 'ย้ายไปหมวดที่ตรงกับกิจกรรม'
        elif 'green_culture' in src.lower() or 'GreenCulture' in src:
            reason = 'คัดออกจากรอบปัจจุบัน: เกียรติบัตรระบุ 5 สิงหาคม 2567'
        audit.append(dict(src=src, previous_album=album_id, previous_caption=item['caption'],
                          current_album=new_placement.get(src), current_caption=current['caption'] if current else None,
                          decision=reason))
    out = dict(review_date='2026-09-15', source_catalog_count=len(CATALOG),
               source='tmp/รูปที่ใช้ในpa; ตรวจภาพจาก contact-01 ถึง contact-13',
               selected_images=len(selected), albums=len(albums), changes=audit,
               static_removed=sorted(set(static_removed)))
    (ROOT / 'qa-pa/photo-audit-20260915.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:out[k] for k in ['source_catalog_count', 'selected_images', 'albums']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
