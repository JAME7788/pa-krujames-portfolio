from __future__ import annotations

import base64
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSET = ROOT / "assets" / "krujames-portrait-red-web.jpg"
OUT_DIR = ROOT / "embeds" / "page-covers"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_list(items: list[str]) -> str:
    return "\n".join(f"          <span>{esc(item)}</span>" for item in items)


def render_stats(items: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"""          <div class=\"stat\">
            <b>{esc(value)}</b>
            <span>{esc(label)}</span>
          </div>"""
        for value, label in items
    )


PAGES = [
    {
        "slug": "01-home",
        "cover_id": "krujames-cover-home",
        "page_no": "01",
        "kicker": "หน้าแรก | Red Tech Learning Portal",
        "title": "เอเจเจ.ไทย",
        "lead": "ศูนย์รวมบทเรียน เทคโนโลยี ผลงานครู และหลักฐานการพัฒนาผู้เรียนของครูเจมส์ในที่เดียว",
        "focus": "ออกแบบให้ผู้เรียน ผู้ปกครอง ผู้บริหาร และคณะกรรมการเข้าถึงข้อมูลสำคัญได้เร็ว ดูน่าเชื่อถือ และสะท้อนตัวตนครูสายเทคโนโลยี",
        "chips": ["วิทยาการคำนวณ", "AI เพื่อการเรียนรู้", "แฟ้มสะสมงาน", "PA 2569"],
        "stats": [("12 หน้า", "โครงสร้างเว็บไซต์"), ("2569", "พร้อมประกวดเว็บครู.ไทย"), ("3 ด้าน", "หลักฐานตาม PA")],
    },
    {
        "slug": "02-learning",
        "cover_id": "krujames-cover-learning",
        "page_no": "02",
        "kicker": "Learning Hub | Coding and Technology",
        "title": "เว็บการเรียนการสอน",
        "lead": "ห้องเรียนออนไลน์สำหรับบทเรียน วิทยาการคำนวณ Coding AI และการออกแบบเทคโนโลยี",
        "focus": "จัดเนื้อหาให้ผู้เรียนเริ่มจากเป้าหมาย บทเรียน กิจกรรม และหลักฐานการเรียนรู้ เพื่อใช้เรียนซ้ำได้ทั้งในห้องเรียนและที่บ้าน",
        "chips": ["บทเรียนรายวิชา", "ใบงาน", "สื่อโต้ตอบ", "คลังแบบทดสอบ"],
        "stats": [("ป.1-ม.3", "กลุ่มผู้เรียน"), ("Coding", "ทักษะหลัก"), ("Quizizz", "ประเมินผลทันที")],
    },
    {
        "slug": "03-prompt-studio",
        "cover_id": "krujames-cover-prompt-studio",
        "page_no": "03",
        "kicker": "Prompt Studio | AI for Teachers",
        "title": "Prompt Studio",
        "lead": "คลัง Prompt และแนวทางใช้ AI ช่วยออกแบบบทเรียน สื่อ กิจกรรม และการประเมินอย่างรับผิดชอบ",
        "focus": "เน้นให้ครูนำ AI ไปใช้จริงในงานประจำ ลดเวลางานเอกสาร เพิ่มคุณภาพคำถาม กิจกรรม และสื่อการเรียนรู้",
        "chips": ["แผนการสอน", "สร้างสื่อ", "ออกแบบคำถาม", "ตรวจงาน"],
        "stats": [("AI", "เครื่องมือช่วยสอน"), ("Prompt", "ใช้งานได้ทันที"), ("Ethics", "ใช้เทคโนโลยีอย่างรู้เท่าทัน")],
    },
    {
        "slug": "04-eportfolio",
        "cover_id": "krujames-cover-eportfolio",
        "page_no": "04",
        "kicker": "Professional Portfolio | Evidence Center",
        "title": "E-Portfolio ครูเจมส์",
        "lead": "แฟ้มสะสมงานดิจิทัลที่รวบรวมประวัติ ผลงาน รางวัล นวัตกรรม และหลักฐานการพัฒนาวิชาชีพ",
        "focus": "ทำให้เส้นทางการทำงานเห็นเป็นภาพรวม ตรวจหลักฐานต่อได้ง่าย และเชื่อมโยงกับผลลัพธ์ที่เกิดกับผู้เรียน",
        "chips": ["ประวัติ", "ผลงาน", "รางวัล", "หลักฐาน PA"],
        "stats": [("คศ.1", "ตำแหน่งปัจจุบัน"), ("2567-2569", "เส้นทางพัฒนา"), ("PLC", "เรียนรู้ร่วมกัน")],
    },
    {
        "slug": "05-profile",
        "cover_id": "krujames-cover-profile",
        "page_no": "05",
        "kicker": "Teacher Profile | Professional Identity",
        "title": "ประวัติส่วนตัว",
        "lead": "ข้อมูลประวัติ เส้นทางรับราชการ ภาระงาน และบทบาทครูผู้สอนวิทยาศาสตร์และเทคโนโลยี",
        "focus": "สรุปข้อมูลตัวตนและประสบการณ์ให้คณะกรรมการเห็นภาพครูผู้ปฏิบัติงานจริง พร้อมบริบทโรงเรียนและผู้เรียน",
        "chips": ["ครูเจมส์", "โรงเรียนบ้านคลองมดแดง", "วิทยาการคำนวณ", "เทคโนโลยี"],
        "stats": [("17 ม.ค. 2567", "เริ่มรับราชการ"), ("23 ชม./สัปดาห์", "ภาระสอน 2568"), ("คศ.1", "ตามแบบ PA")],
    },
    {
        "slug": "06-pa-learning",
        "cover_id": "krujames-cover-pa-learning",
        "page_no": "06",
        "kicker": "PA ด้านที่ 1 | Learning Management",
        "title": "ด้านที่ 1 การจัดการเรียนรู้",
        "lead": "หลักฐานการออกแบบหน่วยการเรียนรู้ กิจกรรม Active Learning สื่อดิจิทัล และการวัดประเมินผลผู้เรียน",
        "focus": "แสดงกระบวนการสอนตั้งแต่เป้าหมายการเรียนรู้ กิจกรรมในชั้นเรียน สื่อที่ใช้จริง ไปจนถึงผลลัพธ์และชิ้นงานของผู้เรียน",
        "chips": ["Active Learning", "Gamification", "Quizizz", "ชิ้นงานผู้เรียน"],
        "stats": [("ป.1", "Gamification"), ("ม.3", "Quizizz"), ("ก่อน-หลัง", "วัดผลนวัตกรรม")],
    },
    {
        "slug": "07-pa-support",
        "cover_id": "krujames-cover-pa-support",
        "page_no": "07",
        "kicker": "PA ด้านที่ 2 | Student Support",
        "title": "ด้านที่ 2 การส่งเสริมและสนับสนุน",
        "lead": "หลักฐานระบบดูแลช่วยเหลือผู้เรียน การประสานผู้ปกครอง ชุมชน และงานสนับสนุนการเรียนรู้",
        "focus": "เน้นภาพการทำงานจริงกับผู้เรียนรายบุคคล การติดตามช่วยเหลือ และการทำงานร่วมกับครอบครัวและชุมชน",
        "chips": ["ดูแลช่วยเหลือ", "เยี่ยมบ้าน", "ผู้ปกครอง", "ชุมชน"],
        "stats": [("รายบุคคล", "ติดตามผู้เรียน"), ("Home Room", "สร้างวินัยและทักษะชีวิต"), ("เครือข่าย", "ผู้ปกครองและชุมชน")],
    },
    {
        "slug": "08-pa-development",
        "cover_id": "krujames-cover-pa-development",
        "page_no": "08",
        "kicker": "PA ด้านที่ 3 | Professional Development",
        "title": "ด้านที่ 3 การพัฒนาตนเองและวิชาชีพ",
        "lead": "หลักฐานการอบรม พัฒนาทักษะ AI การเข้าร่วม PLC และการนำความรู้กลับมาใช้พัฒนาห้องเรียน",
        "focus": "เชื่อมการพัฒนาตนเองกับผลที่เกิดจริง ทั้งการสร้างสื่อใหม่ การปรับกิจกรรมการสอน และการแลกเปลี่ยนเรียนรู้ในวิชาชีพ",
        "chips": ["อบรม", "AI for Teachers", "PLC", "ต่อยอดสู่ห้องเรียน"],
        "stats": [("104 ชม.", "พัฒนาตนเอง 2568"), ("52 ชม.", "ผู้กำกับลูกเสือ"), ("AI", "ทักษะสำคัญปี 2569")],
    },
    {
        "slug": "09-awards",
        "cover_id": "krujames-cover-awards",
        "page_no": "09",
        "kicker": "Awards and Recognition | Impact Showcase",
        "title": "ผลงานเด่นและรางวัล",
        "lead": "รวมผลงานครู นักเรียน เกียรติบัตร และรางวัลที่สะท้อนคุณภาพการจัดการเรียนรู้ด้านเทคโนโลยี",
        "focus": "จัดแสดงผลงานให้เห็นคุณค่า ไม่ใช่เพียงรายการรางวัล แต่เชื่อมโยงกับทักษะผู้เรียนและบทบาทการเป็นครูผู้ฝึกสอน",
        "chips": ["รางวัลนักเรียน", "ผู้ฝึกสอน", "เกียรติบัตร", "เวทีแข่งขัน"],
        "stats": [("6 รายการ", "ชนะเลิศ/เหรียญทอง"), ("ผลงานจริง", "ใช้ตรวจหลักฐาน"), ("Impact", "ผลลัพธ์กับผู้เรียน")],
    },
    {
        "slug": "10-assessment-docs",
        "cover_id": "krujames-cover-assessment-docs",
        "page_no": "10",
        "kicker": "PA Evidence | Assessment Documents",
        "title": "เอกสารการประเมิน",
        "lead": "ศูนย์รวมเอกสารหลักฐานสำหรับการประเมิน PA พร้อมเส้นทางตรวจหลักฐานที่สั้น ชัด และครบถ้วน",
        "focus": "ทำให้คณะกรรมการเริ่มตรวจจากข้อมูลหลัก ลิงก์หลักฐาน ผลก่อน-หลังนวัตกรรม และเอกสารประกอบได้ภายในไม่กี่นาที",
        "chips": ["แบบข้อตกลง PA", "SAR", "ID Plan", "Drive Evidence"],
        "stats": [("12 รายการ", "ลิงก์หลักฐาน"), ("3 นาที", "เส้นทางตรวจหลักฐาน"), ("ก่อน-หลัง", "ผลนวัตกรรม")],
    },
    {
        "slug": "11-innovation",
        "cover_id": "krujames-cover-innovation",
        "page_no": "11",
        "kicker": "Innovation and Classroom Research",
        "title": "นวัตกรรมและวิจัยในชั้นเรียน",
        "lead": "สรุปนวัตกรรม Gamification และ Quizizz ที่ใช้แก้ปัญหาการเรียนรู้ พร้อมข้อมูลผลก่อนเรียนและหลังเรียน",
        "focus": "นำเสนอปัญหา วิธีพัฒนา เครื่องมือที่ใช้ ข้อมูลผู้เรียน และผลลัพธ์เชิงประจักษ์ให้เห็นความเปลี่ยนแปลงจริง",
        "chips": ["Gamification", "Quizizz", "วิจัยในชั้นเรียน", "Learning Data"],
        "stats": [("Pre/Post", "คะแนนก่อน-หลัง"), ("Learners", "จำนวนผู้เรียน"), ("% ผ่านเกณฑ์", "ผลลัพธ์สำคัญ")],
    },
    {
        "slug": "12-webkru-contest",
        "cover_id": "krujames-cover-webkru-contest",
        "page_no": "12",
        "kicker": "Webkru Contest 2569 | Competition Ready",
        "title": "ประกวดเว็บครู.ไทย",
        "lead": "หน้ารวมความพร้อมประกวดเว็บครู.ไทย พ.ศ. 2569 โทนแดงเทคโนโลยี เนื้อหาชัด และหลักฐานครบ",
        "focus": "ออกแบบให้คณะกรรมการเห็นจุดเด่นของเว็บทันที ทั้งความสวยงาม การใช้งาน เนื้อหาวิชาการ และผลลัพธ์ที่เกิดกับผู้เรียน",
        "chips": ["โทนแดง", "เทคโนโลยี", "UX ชัด", "หลักฐานครบ"],
        "stats": [("Contest", "พร้อมนำเสนอ"), ("PA", "เชื่อมหลักฐาน"), ("KruJames", "ตัวตนครูสายเทค")],
    },
]


TEMPLATE = """<!doctype html>
<html lang=\"th\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;600;700;800&display=swap');

    :root {{
      --red-950: #170104;
      --red-900: #3f0508;
      --red-800: #6f0710;
      --red-700: #a30b18;
      --red-600: #d21424;
      --gold: #ffcf66;
      --cream: #fff7e4;
      --ink: #201213;
      --line: rgba(255, 255, 255, .22);
    }}

    * {{
      box-sizing: border-box;
    }}

    html,
    body {{
      margin: 0;
      min-height: 100%;
      background: transparent;
      font-family: \"Noto Sans Thai\", Tahoma, Arial, sans-serif;
      color: var(--cream);
    }}

    body {{
      padding: 0;
    }}

    .kj-cover {{
      width: min(1120px, 100%);
      min-height: 352px;
      margin: 0 auto;
      position: relative;
      overflow: hidden;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, .18);
      background:
        radial-gradient(circle at 85% 20%, rgba(255, 207, 102, .26), transparent 30%),
        radial-gradient(circle at 14% 88%, rgba(255, 42, 64, .38), transparent 28%),
        linear-gradient(135deg, #2a0206 0%, #870813 47%, #120104 100%);
      box-shadow: 0 18px 40px rgba(60, 0, 10, .28);
      isolation: isolate;
    }}

    .kj-cover::before {{
      content: \"\";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(90deg, rgba(255, 255, 255, .075) 1px, transparent 1px),
        linear-gradient(0deg, rgba(255, 255, 255, .055) 1px, transparent 1px);
      background-size: 38px 38px;
      mask-image: linear-gradient(90deg, rgba(0,0,0,.84), rgba(0,0,0,.2));
      z-index: -2;
    }}

    .kj-cover::after {{
      content: \"\";
      position: absolute;
      width: 560px;
      height: 560px;
      right: -190px;
      top: -210px;
      border: 1px solid rgba(255, 207, 102, .25);
      border-radius: 50%;
      background:
        repeating-conic-gradient(from 10deg, rgba(255, 255, 255, .12) 0deg 8deg, transparent 8deg 18deg),
        radial-gradient(circle, rgba(255, 255, 255, .05), transparent 54%);
      z-index: -1;
    }}

    .inner {{
      min-height: 352px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 310px;
      gap: 26px;
      align-items: stretch;
      padding: 34px;
    }}

    .copy {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-width: 0;
    }}

    .kicker {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
      color: #ffd989;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }}

    .kicker::before {{
      content: \"\";
      width: 32px;
      height: 3px;
      border-radius: 999px;
      background: var(--gold);
      box-shadow: 0 0 18px rgba(255, 207, 102, .8);
      flex: 0 0 auto;
    }}

    h1 {{
      margin: 0;
      color: #fff;
      font-size: 42px;
      line-height: 1.16;
      font-weight: 800;
      letter-spacing: 0;
      text-wrap: balance;
    }}

    .lead {{
      max-width: 760px;
      margin: 12px 0 0;
      color: rgba(255, 247, 228, .9);
      font-size: 17px;
      line-height: 1.75;
      font-weight: 500;
    }}

    .focus {{
      max-width: 780px;
      margin: 14px 0 0;
      padding-left: 14px;
      border-left: 3px solid rgba(255, 207, 102, .8);
      color: rgba(255, 255, 255, .78);
      font-size: 14px;
      line-height: 1.68;
    }}

    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 20px;
    }}

    .chips span {{
      display: inline-flex;
      align-items: center;
      min-height: 32px;
      padding: 6px 12px;
      border: 1px solid rgba(255, 255, 255, .22);
      border-radius: 999px;
      background: rgba(255, 255, 255, .09);
      color: rgba(255, 255, 255, .92);
      font-size: 13px;
      font-weight: 700;
      white-space: nowrap;
      backdrop-filter: blur(10px);
    }}

    .panel {{
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 284px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, .22);
      background:
        linear-gradient(180deg, rgba(255, 255, 255, .14), rgba(255, 255, 255, .06)),
        rgba(28, 2, 5, .72);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, .22);
      overflow: hidden;
    }}

    .panel::before {{
      content: \"\";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(135deg, transparent 0 38%, rgba(255, 207, 102, .18) 38% 39%, transparent 39% 100%),
        radial-gradient(circle at 24% 20%, rgba(255, 255, 255, .14), transparent 24%);
      pointer-events: none;
    }}

    .portrait-row {{
      position: relative;
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 18px 18px 10px;
    }}

    .portrait {{
      width: 78px;
      height: 78px;
      flex: 0 0 auto;
      border-radius: 50%;
      border: 3px solid rgba(255, 207, 102, .9);
      background: #2455d8 url(\"{portrait_uri}\") center 24% / cover no-repeat;
      box-shadow: 0 12px 26px rgba(0, 0, 0, .3);
    }}

    .id strong {{
      display: block;
      color: #fff;
      font-size: 17px;
      line-height: 1.35;
      font-weight: 800;
    }}

    .id span {{
      display: block;
      margin-top: 4px;
      color: rgba(255, 247, 228, .74);
      font-size: 12px;
      line-height: 1.5;
      font-weight: 700;
    }}

    .page-tag {{
      margin: 4px 18px 12px;
      padding: 10px 12px;
      border-radius: 8px;
      background: rgba(255, 207, 102, .14);
      border: 1px solid rgba(255, 207, 102, .28);
      color: #fff5d2;
      font-size: 13px;
      line-height: 1.55;
      font-weight: 700;
    }}

    .stats {{
      position: relative;
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
      padding: 0 18px 18px;
    }}

    .stat {{
      display: grid;
      grid-template-columns: 92px 1fr;
      align-items: center;
      gap: 10px;
      padding: 9px 10px;
      min-height: 44px;
      border-radius: 8px;
      background: rgba(255, 255, 255, .08);
      border: 1px solid rgba(255, 255, 255, .12);
    }}

    .stat b {{
      color: var(--gold);
      font-size: 15px;
      line-height: 1.28;
      font-weight: 800;
    }}

    .stat span {{
      color: rgba(255, 255, 255, .78);
      font-size: 12px;
      line-height: 1.35;
      font-weight: 700;
    }}

    .page-no {{
      position: absolute;
      right: 18px;
      top: 14px;
      color: rgba(255, 255, 255, .12);
      font-size: 68px;
      line-height: 1;
      font-weight: 800;
    }}

    @media (max-width: 760px) {{
      .kj-cover {{
        min-height: auto;
      }}

      .inner {{
        min-height: auto;
        grid-template-columns: 1fr;
        padding: 24px;
      }}

      h1 {{
        font-size: 31px;
      }}

      .lead {{
        font-size: 15px;
      }}

      .panel {{
        min-height: auto;
      }}

      .stat {{
        grid-template-columns: 84px 1fr;
      }}
    }}
  </style>
</head>
<body>
  <section class=\"kj-cover\" data-cover-id=\"{cover_id}\">
    <div class=\"inner\">
      <div class=\"copy\">
        <div class=\"kicker\">{kicker}</div>
        <h1>{title}</h1>
        <p class=\"lead\">{lead}</p>
        <p class=\"focus\">{focus}</p>
        <div class=\"chips\" aria-label=\"จุดเด่นของหน้า\">
{chips}
        </div>
      </div>

      <aside class=\"panel\" aria-label=\"ข้อมูลสรุปของหน้า\">
        <div class=\"page-no\">{page_no}</div>
        <div>
          <div class=\"portrait-row\">
            <div class=\"portrait\" aria-hidden=\"true\"></div>
            <div class=\"id\">
              <strong>ครูเจมส์</strong>
              <span>เทคโนโลยี · วิทยาการคำนวณ</span>
            </div>
          </div>
          <div class=\"page-tag\">{page_tag}</div>
        </div>
        <div class=\"stats\">
{stats}
        </div>
      </aside>
    </div>
  </section>
</body>
</html>
"""


def main() -> None:
    if not ASSET.exists():
        raise FileNotFoundError(f"Missing portrait asset: {ASSET}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    portrait_uri = "data:image/jpeg;base64," + base64.b64encode(ASSET.read_bytes()).decode("ascii")

    cards: list[str] = []
    for page in PAGES:
        filename = f"{page['slug']}.html"
        output = OUT_DIR / filename
        document = TEMPLATE.format(
            title=esc(page["title"]),
            cover_id=esc(page["cover_id"]),
            page_no=esc(page["page_no"]),
            kicker=esc(page["kicker"]),
            lead=esc(page["lead"]),
            focus=esc(page["focus"]),
            chips=render_list(page["chips"]),
            stats=render_stats(page["stats"]),
            portrait_uri=portrait_uri,
            page_tag=esc(page["focus"]),
        )
        output.write_text(document, encoding="utf-8")
        cards.append(
            f"""<article>
  <h2>{esc(page['page_no'])}. {esc(page['title'])}</h2>
  <iframe src=\"{filename}\" title=\"{esc(page['title'])}\"></iframe>
</article>"""
        )

    preview = f"""<!doctype html>
<html lang=\"th\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Preview Page Covers</title>
  <style>
    body {{
      margin: 0;
      padding: 28px;
      background: #f6f0ea;
      font-family: Tahoma, Arial, sans-serif;
      color: #241112;
    }}
    h1 {{
      margin: 0 0 18px;
      font-size: 28px;
    }}
    article {{
      margin: 0 0 28px;
    }}
    h2 {{
      margin: 0 0 8px;
      font-size: 16px;
    }}
    iframe {{
      width: 100%;
      height: 380px;
      border: 0;
      display: block;
      background: transparent;
    }}
  </style>
</head>
<body>
  <h1>ชุดปกหน้าเว็บครูเจมส์</h1>
  {''.join(cards)}
</body>
</html>
"""
    (OUT_DIR / "index.html").write_text(preview, encoding="utf-8")
    print(f"Generated {len(PAGES)} covers in {OUT_DIR}")


if __name__ == "__main__":
    main()
