from pathlib import Path
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
ALBUMS_PATH = ROOT / "albums_data.json"

# Two complementary, non-repeated items per indicator. Document/certificate
# evidence is used where an activity photograph would not prove the criterion.
CURATED = {
    "1-1": [
        ("assets/evidence_pa_photos/IMG_20260910_133433.jpg", "นำหน่วยการเรียนรู้วิทยาการคำนวณตามหลักสูตรสถานศึกษาไปใช้จริง", "๑๐ ก.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260224_111740.jpg", "จัดการเรียนรู้ตามสาระเทคโนโลยีในห้องปฏิบัติการคอมพิวเตอร์", "๒๔ ก.พ. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260202_084245.jpg", "นำสาระเทคโนโลยีไปจัดประสบการณ์เรียนรู้ให้ผู้เรียนช่วงชั้นต้น", "๒ ก.พ. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260202_110800.jpg", "ผู้เรียนเรียนรู้อุปกรณ์และการใช้งานคอมพิวเตอร์ตามหน่วยการเรียนรู้", "๒ ก.พ. ๒๕๖๙"),
    ],
    "1-2": [
        ("assets/evidence_pa_photos/MVIMG_20260514_151034.jpg", "ครูสาธิตและจัดกิจกรรม Active Learning ตามแผนที่ออกแบบ", "๑๔ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260122_095316.jpg", "จัดลำดับกิจกรรมจากการอธิบายสู่การฝึกปฏิบัติรายบุคคล", "๒๒ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20251205_100158.jpg", "จัดกิจกรรมกลุ่มย่อยและหมุนเวียนให้ผู้เรียนลงมือปฏิบัติ", "๕ ธ.ค. ๒๕๖๘"),
        ("assets/evidence_pa_photos/IMG_20260223_105753.jpg", "ออกแบบกิจกรรมให้ผู้เรียนโต้ตอบกับสื่อและรับผลย้อนกลับทันที", "๒๓ ก.พ. ๒๕๖๙"),
    ],
    "1-3": [
        ("assets/evidence_pa_photos/IMG_20260716_114228.jpg", "กิจกรรม Coding แบบลงมือปฏิบัติและเรียนรู้ร่วมกัน", "๑๖ ก.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260128_140013.jpg", "ครูให้คำแนะนำรายกลุ่มระหว่างสร้างชิ้นงานดิจิทัล", "๒๘ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260130_121507.jpg", "ผู้เรียนทดลองใช้เครื่องมือดิจิทัลร่วมกับการชี้แนะของครู", "๓๐ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260910_133441.jpg", "ผู้เรียนลงมือทำภารกิจ Coding รายบุคคลและเรียนรู้ร่วมกัน", "๑๐ ก.ย. ๒๕๖๙"),
    ],
    "1-4": [
        ("assets/evidence_pa_photos/IMG_20260803_084731.jpg", "ใช้สื่อเกมดิจิทัลและ Gamification ประกอบการเรียนรู้", "๓ ส.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260819_143408.jpg", "ใช้หูฟังและบทเรียนดิจิทัลให้ผู้เรียนเรียนรู้ตามจังหวะของตนเอง", "๑๙ ส.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260223_105749.jpg", "ผู้เรียนโต้ตอบกับสื่อออนไลน์ผ่านหน้าจอสัมผัส", "๒๓ ก.พ. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260311_143717.jpg", "ใช้สื่อ Coding แบบบล็อกคำสั่งเพื่อสร้างชิ้นงาน", "๑๑ มี.ค. ๒๕๖๙"),
    ],
    "1-5": [
        ("assets/evidence_pa_photos/IMG_20260611_132439.jpg", "ผู้เรียนทำแบบประเมินและภารกิจดิจิทัลรายบุคคล", "๑๑ มิ.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260910_133427.jpg", "ประเมินทักษะการใช้เมาส์และการปฏิบัติงานจริง", "๑๐ ก.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260611_132449.jpg", "เก็บหลักฐานผลการตอบแบบประเมินผ่านระบบออนไลน์", "๑๑ มิ.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/MVIMG_20260518_132242.jpg", "ผู้เรียนทำแบบประเมินดิจิทัลเพื่อใช้เปรียบเทียบพัฒนาการ", "๑๘ พ.ค. ๒๕๖๙"),
    ],
    "1-6": [
        ("assets/evidence_pa_photos/IMG_20260128_140738.jpg", "สังเกตปัญหาและช่วยเหลือผู้เรียนระหว่างปฏิบัติ", "๒๘ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260122_095645.jpg", "วิเคราะห์ข้อผิดพลาดและให้คำแนะนำเฉพาะจุดเป็นรายบุคคล", "๒๒ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260128_140019.jpg", "ให้ความช่วยเหลือเฉพาะกลุ่มตามปัญหาที่พบระหว่างเรียน", "๒๘ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260122_101147.jpg", "ติดตามวิธีคิดและปรับคำแนะนำให้เหมาะกับผู้เรียน", "๒๒ ม.ค. ๒๕๖๙"),
    ],
    "1-7": [
        ("assets/evidence_pa_photos/IMG_20260910_111013.jpg", "ห้องปฏิบัติการที่เอื้อต่อการเรียนรู้แบบหนึ่งคนหนึ่งเครื่อง", "๑๐ ก.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260224_111728.jpg", "จัดสภาพแวดล้อมและอุปกรณ์พร้อมสำหรับการฝึกปฏิบัติ", "๒๔ ก.พ. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260224_111732.jpg", "ผู้เรียนมีพื้นที่และอุปกรณ์พร้อมสำหรับทำกิจกรรมอย่างทั่วถึง", "๒๔ ก.พ. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20251106_103307.jpg", "จัดห้องเรียนเทคโนโลยีให้มีระเบียบและเอื้อต่อการมีส่วนร่วม", "๖ พ.ย. ๒๕๖๘"),
    ],
    "1-8": [
        ("assets/evidence_pa_photos/IMG_20260911_075634.jpg", "กิจกรรมส่งเสริมสมาธิ คุณธรรม และคุณลักษณะอันพึงประสงค์", "๑๑ ก.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260723_082840.jpg", "กิจกรรมกลุ่มสร้างความรับผิดชอบและการอยู่ร่วมกัน", "๒๓ ก.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20251204_095244.jpg", "กิจกรรมปลูกต้นไม้ส่งเสริมความรับผิดชอบและจิตสาธารณะ", "๔ ธ.ค. ๒๕๖๘"),
        ("assets/evidence_pa_photos/IMG_20260721_093801.jpg", "กิจกรรมวันสำคัญทางศาสนาเพื่อปลูกฝังคุณธรรม", "๒๑ ก.ค. ๒๕๖๙"),
    ],
    "2-1": [
        ("assets/evidence_pa_photos/MVIMG_20260518_132255.jpg", "ใช้ระบบดิจิทัลบันทึกข้อมูลและติดตามความก้าวหน้ารายบุคคล", "๑๘ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260611_132506.jpg", "ตรวจสอบผลจากกิจกรรมออนไลน์เพื่อวางแผนพัฒนาผู้เรียน", "๑๑ มิ.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260611_132457.jpg", "บันทึกผลการทำภารกิจของผู้เรียนผ่านระบบสารสนเทศ", "๑๑ มิ.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/MVIMG_20260518_132305.jpg", "จัดเก็บข้อมูลคำตอบรายบุคคลเพื่อใช้ติดตามและช่วยเหลือ", "๑๘ พ.ค. ๒๕๖๙"),
    ],
    "2-2": [
        ("assets/evidence_pa_photos/MVIMG_20260519_164336.jpg", "เยี่ยมบ้านเพื่อศึกษาสภาพจริงและวางแนวทางช่วยเหลือผู้เรียน", "๑๙ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/MVIMG_20260520_163341.jpg", "ครูและผู้ปกครองร่วมแลกเปลี่ยนข้อมูลระหว่างการเยี่ยมบ้าน", "๒๐ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/MVIMG_20260520_164914.jpg", "บันทึกสภาพแวดล้อมและข้อมูลจำเป็นของผู้เรียนระหว่างเยี่ยมบ้าน", "๒๐ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/MVIMG_20260521_164311.jpg", "ติดตามผู้เรียนถึงบ้านอย่างต่อเนื่องตามระบบดูแลช่วยเหลือ", "๒๑ พ.ค. ๒๕๖๙"),
    ],
    "2-3": [
        ("assets/evidence_pa_photos/IMG_20260224_091508.jpg", "ดูแลระบบคอมพิวเตอร์และโครงสร้างพื้นฐานเพื่อสนับสนุนการเรียนรู้", "๒๔ ก.พ. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260617_164612.jpg", "ตรวจสอบและบำรุงรักษาเครื่องคอมพิวเตอร์ให้พร้อมใช้งาน", "๑๗ มิ.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20251118_105930.jpg", "จัดระเบียบและตรวจความพร้อมของอุปกรณ์ห้องคอมพิวเตอร์", "๑๘ พ.ย. ๒๕๖๘"),
        ("assets/evidence_pa_photos/IMG_20260313_085710.jpg", "ปรับปรุงระบบอุปกรณ์และเครือข่ายของสถานศึกษา", "๑๓ มี.ค. ๒๕๖๙"),
    ],
    "2-4": [
        ("assets/evidence_pa_photos/MVIMG_20260506_085132.jpg", "ประชุมผู้ปกครองเพื่อสื่อสารข้อมูลผู้เรียนและสร้างความร่วมมือ", "๖ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260907_141703.jpg", "สื่อสารแนวทางดูแลผู้เรียนร่วมกับผู้ปกครองรายชั้นเรียน", "๗ ก.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/MVIMG_20260506_085133.jpg", "ชี้แจงแนวทางดำเนินงานและรับฟังความคิดเห็นจากผู้ปกครอง", "๖ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260618_173246.jpg", "ร่วมประชุมกับคณะกรรมการสถานศึกษาและภาคีเครือข่าย", "๑๘ มิ.ย. ๒๕๖๙"),
    ],
    "3-1": [
        ("assets_drop/06_ภาพเกียรติบัตรและรางวัล/LINE_ALBUM_อนันตชัย_260712_1.jpg", "เกียรติบัตรการพัฒนาความรู้ด้าน AI Learning Hub และ OBEC Content Center", "๗ มิ.ย. ๒๕๖๙"),
        ("assets_drop/06_ภาพเกียรติบัตรและรางวัล/messageImage_1783918653571.jpg", "เกียรติบัตรพัฒนาความรู้และฝึกสอนการสร้างสื่อด้วย AI", "๒๖ มิ.ย. ๒๕๖๙"),
        ("assets_drop/06_ภาพเกียรติบัตรและรางวัล/Picture1.png", "ผ่านการอบรมการจัดการเรียนรู้ปัญญาประดิษฐ์ ระดับมัธยมศึกษาปีที่ 1-3", "๗ พ.ค. ๒๕๖๙"),
        ("assets_drop/06_ภาพเกียรติบัตรและรางวัล/Picture2.png", "ผ่านการอบรมการจัดการเรียนรู้ปัญญาประดิษฐ์ ระดับประถมศึกษาปีที่ 4-6", "๗ พ.ค. ๒๕๖๙"),
    ],
    "3-2": [
        ("assets/evidence_pa_photos/MVIMG_20260506_155728.jpg", "ประชุมแลกเปลี่ยนเรียนรู้ทางวิชาชีพและร่วมวางแผนพัฒนาผู้เรียน", "๖ พ.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260105_173546.jpg", "คณะครูร่วมประชุมสะท้อนผลและกำหนดแนวทางการทำงาน", "๕ ม.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260610_162021.jpg", "แลกเปลี่ยนข้อมูลการจัดการเรียนรู้และการดำเนินงานในที่ประชุมครู", "๑๐ มิ.ย. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260901_152108.jpg", "ประชุมสะท้อนผลการดำเนินงานและวางแผนพัฒนาร่วมกัน", "๑ ก.ย. ๒๕๖๙"),
    ],
    "3-3": [
        ("assets/evidence_pa_photos/IMG_20260724_085632.jpg", "นำความรู้ด้านสื่อสามมิติและเกมดิจิทัลมาประยุกต์ใช้", "๒๔ ก.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260803_085102.jpg", "ผู้เรียนใช้สื่อ Gamification ที่ครูนำมาพัฒนากิจกรรม", "๓ ส.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260311_143723.jpg", "ประยุกต์ความรู้ด้าน Coding เป็นกิจกรรมสร้างชิ้นงานของผู้เรียน", "๑๑ มี.ค. ๒๕๖๙"),
        ("assets/evidence_pa_photos/IMG_20260910_133655.jpg", "ผู้เรียนใช้สื่อดิจิทัลที่ครูพัฒนาผ่านการฝึกปฏิบัติจริง", "๑๐ ก.ย. ๒๕๖๙"),
    ],
}


def make_item(relative_path: str, caption: str, date: str) -> dict:
    path = ROOT / relative_path
    if not path.exists():
        filename = Path(relative_path).name
        selected = ROOT / "tmp/รูปที่ใช้ในpa" / filename
        if not selected.exists():
            raise FileNotFoundError(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(selected, path)
    return {"src": relative_path, "caption": caption, "date": date}


albums = json.loads(ALBUMS_PATH.read_text(encoding="utf-8"))
awards = next(record for record in albums if record.get("id") == "album-awards")
unrelated_award_photos = {
    "assets/evidence_pa_photos/IMG_20260811_093313.jpg",
    "assets/evidence_pa_photos/IMG_20260811_093748.jpg",
    "assets/evidence_pa_photos/IMG_20260327_134251.jpg",
}
awards["items"] = [item for item in awards["items"] if item["src"] not in unrelated_award_photos]
awards["desc"] = "คัดเฉพาะโล่ ประกาศ เกียรติบัตร และภาพรับรางวัลที่ตรวจสอบความสอดคล้องแล้ว"
used = []
for key, photos in CURATED.items():
    album_id = f"album-{key}"
    album = next((record for record in albums if record.get("id") == album_id), None)
    if album is None:
        raise KeyError(album_id)
    album["items"] = [make_item(*photo) for photo in photos]
    album["cover"] = album["items"][0]["src"]
    album["shared"] = True
    thai_digits = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
    indicator_thai = key.replace("-", ".").translate(thai_digits)
    side_thai = key.split("-", 1)[0].translate(thai_digits)
    album["badge"] = f"ด้านที่ {side_thai} · ตัวชี้วัด {indicator_thai}"
    album["desc"] = f"หลักฐานคัดเลือกเฉพาะรอบ 1 ต.ค. 2568 - 30 ก.ย. 2569 จำนวน 4 รายการ ตรงตามตัวชี้วัด {key.replace('-', '.')}"
    used.extend(item["src"] for item in album["items"])

if len(used) != len(set(used)):
    raise RuntimeError("พบไฟล์ซ้ำข้ามอัลบั้มตัวชี้วัด")

album_json = json.dumps(albums, ensure_ascii=False, separators=(",", ":"))
ALBUMS_PATH.write_text(json.dumps(albums, ensure_ascii=False, indent=2), encoding="utf-8")


def sync_static_album_card(html: str, album: dict) -> str:
    grid_start = html.find('id="album-grid-container"')
    if grid_start == -1:
        return html
    grid_end = html.find('</div>\n      </div>', grid_start)
    if grid_end == -1:
        grid_end = len(html)

    token = f"onclick=\"openAlbumModal('{album['id']}')\""
    token_at = html.find(token, grid_start)
    if token_at == -1 or token_at > grid_end:
        return html

    start = html.rfind('<div class="album-card"', grid_start, token_at)
    if start == -1:
        return html

    next_card = html.find('<div class="album-card"', token_at + len(token))
    if next_card != -1 and next_card < grid_end:
        end = next_card
    else:
        card_close = html.find('</div>\n        </div>', token_at)
        if card_close != -1 and card_close < grid_end:
            end = card_close + len('</div>\n        </div>')
        else:
            end = grid_end

    block = html[start:end]
    block = re.sub(
        r'(<img class="album-cover-img" src=")[^"]+',
        lambda match: match.group(1) + album["cover"],
        block,
        count=1,
    )
    count = str(len(album["items"])).translate(str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙"))
    block = re.sub(
        r'(<div class="album-badge-count">\s*<i[^>]*></i>\s*)[๐-๙0-9]+ รายการ',
        lambda match: match.group(1) + count + " รายการ",
        block,
        count=1,
        flags=re.S,
    )
    block = re.sub(
        r'(<span class="album-card-badge">).*?(</span>)',
        lambda match: match.group(1) + album["badge"] + match.group(2),
        block,
        count=1,
        flags=re.S,
    )
    block = re.sub(
        r'(<div class="album-card-title">).*?(</div>)',
        lambda match: match.group(1) + album["title"] + match.group(2),
        block,
        count=1,
        flags=re.S,
    )
    block = re.sub(
        r'(<div class="album-card-desc">).*?(</div>)',
        lambda match: match.group(1) + album["desc"] + match.group(2),
        block,
        count=1,
        flags=re.S,
    )
    return html[:start] + block + html[end:]

for html_path in (ROOT / "index.html", ROOT / "website/index.html"):
    html = html_path.read_text(encoding="utf-8")
    marker = "const ALBUMS_DATA = "
    start = html.index(marker) + len(marker)
    _, length = json.JSONDecoder().raw_decode(html[start:])
    html = html[:start] + album_json + html[start + length:]
    thai_digits = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
    for key, photos in CURATED.items():
        indicator = key.replace("-", ".").translate(thai_digits)
        count = str(len(photos)).translate(thai_digits)
        pattern = rf"(ดูอัลบั้มภาพ ข้อ {re.escape(indicator)} \()([๐-๙0-9]+)( รายการ\))"
        html = re.sub(pattern, rf"\g<1>{count}\g<3>", html)
    for album in [awards] + [record for record in albums if record.get("id") in {f"album-{key}" for key in CURATED}]:
        html = sync_static_album_card(html, album)
    html_path.write_text(html, encoding="utf-8", newline="\n")

shutil.copy2(ALBUMS_PATH, ROOT / "website/albums_data.json")
print("Updated 15 indicator albums with 60 unique, purpose-matched items.")
