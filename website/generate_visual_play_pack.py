from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "assets" / "visual-play"
FONT_REGULAR = Path("C:/Windows/Fonts/tahoma.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/tahomabd.ttf")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


def rounded_shadow(size: tuple[int, int], radius: int = 36, shadow: int = 24) -> Image.Image:
    w, h = size
    base = Image.new("RGBA", (w + shadow * 2, h + shadow * 2), (0, 0, 0, 0))
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    blur = Image.new("RGBA", base.size, (0, 0, 0, 0))
    blur.paste((70, 0, 8, 95), (shadow, shadow), mask)
    blur = blur.filter(ImageFilter.GaussianBlur(18))
    base.alpha_composite(blur)
    return base


def bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), "#230106")
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w) * 0.68 + (y / h) * 0.32
            glow = max(0, 1 - math.hypot((x - w * 0.78) / (w * 0.52), (y - h * 0.18) / (h * 0.78)))
            r = int(34 + 150 * t + 45 * glow)
            g = int(2 + 16 * t + 9 * glow)
            b = int(8 + 20 * t)
            px[x, y] = (min(r, 188), min(g, 40), min(b, 48), 255)
    draw = ImageDraw.Draw(img)
    for x in range(0, w, 54):
        draw.line((x, 0, x, h), fill=(255, 255, 255, 24), width=1)
    for y in range(0, h, 54):
        draw.line((0, y, w, y), fill=(255, 255, 255, 18), width=1)
    for x in range(-100, w, 180):
        draw.line((x, h, x + 390, 0), fill=(255, 207, 102, 28), width=2)
    return img


def pill(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: tuple[int, int, int], outline=(255, 220, 145, 170)) -> None:
    draw.rounded_rectangle(xy, radius=(xy[3] - xy[1]) // 2, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle((x1 + 12, y1 + 10, x2 - 12, y1 + 35), radius=18, fill=(255, 255, 255, 58))


def draw_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, kind: str, scale: int = 1) -> None:
    gold = (255, 207, 102, 255)
    white = (255, 255, 255, 235)
    red = (210, 20, 36, 255)
    if kind == "cursor":
        pts = [(cx - 22, cy - 42), (cx + 40, cy + 2), (cx + 8, cy + 9), (cx + 24, cy + 44), (cx + 2, cy + 52), (cx - 14, cy + 18), (cx - 37, cy + 39)]
        draw.polygon(pts, fill=white, outline=gold)
        draw.line((cx - 54, cy - 30, cx - 76, cy - 54), fill=gold, width=5)
        draw.line((cx - 62, cy - 2, cx - 95, cy - 3), fill=gold, width=5)
    elif kind == "robot":
        draw.rounded_rectangle((cx - 44, cy - 36, cx + 44, cy + 38), radius=18, fill=(255, 255, 255, 235), outline=gold, width=4)
        draw.rectangle((cx - 6, cy - 66, cx + 6, cy - 38), fill=gold)
        draw.ellipse((cx - 12, cy - 84, cx + 12, cy - 60), fill=gold)
        draw.ellipse((cx - 25, cy - 7, cx - 9, cy + 9), fill=red)
        draw.ellipse((cx + 9, cy - 7, cx + 25, cy + 9), fill=red)
        draw.arc((cx - 20, cy + 4, cx + 20, cy + 28), 0, 180, fill=(100, 0, 12, 255), width=4)
    elif kind == "quiz":
        draw.rounded_rectangle((cx - 42, cy - 46, cx + 42, cy + 50), radius=12, fill=white, outline=gold, width=4)
        for i, label in enumerate(["A", "B", "C"]):
            y = cy - 23 + i * 28
            draw.ellipse((cx - 28, y - 9, cx - 10, y + 9), outline=red, width=3)
            draw.text((cx + 2, y - 13), label, font=font(20, True), fill=(80, 0, 9, 255))
    elif kind == "medal":
        draw.polygon([(cx - 34, cy - 62), (cx - 8, cy - 18), (cx - 28, cy - 10), (cx - 54, cy - 54)], fill=red)
        draw.polygon([(cx + 34, cy - 62), (cx + 8, cy - 18), (cx + 28, cy - 10), (cx + 54, cy - 54)], fill=(150, 7, 18, 255))
        draw.ellipse((cx - 46, cy - 36, cx + 46, cy + 56), fill=gold, outline=white, width=4)
        draw.text((cx - 15, cy - 14), "1", font=font(52, True), fill=(105, 3, 12, 255))
    elif kind == "drive":
        draw.rounded_rectangle((cx - 56, cy - 42, cx + 56, cy + 46), radius=12, fill=white, outline=gold, width=4)
        draw.rectangle((cx - 36, cy - 22, cx + 36, cy - 13), fill=red)
        draw.rectangle((cx - 36, cy - 2, cx + 36, cy + 7), fill=(95, 8, 15, 255))
        draw.rectangle((cx - 36, cy + 18, cx + 18, cy + 27), fill=gold)


def save(img: Image.Image, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(OUT_DIR / name, optimize=True)


def cta_button() -> Image.Image:
    canvas = Image.new("RGBA", (1200, 360), (0, 0, 0, 0))
    shadow = rounded_shadow((1040, 190), 95, 38)
    canvas.alpha_composite(shadow, (80 - 38, 86 - 38))
    draw = ImageDraw.Draw(canvas)
    pill(draw, (80, 86, 1120, 276), (210, 20, 36, 255))
    draw.ellipse((118, 112, 248, 242), fill=(255, 255, 255, 238), outline=(255, 207, 102, 255), width=5)
    draw_icon(draw, 184, 177, "cursor")
    draw.text((300, 122), "คลิกเข้าสู่เว็บไซต์", font=font(74, True), fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(130, 0, 16, 255))
    draw.text((305, 214), "KruJames Red Tech Learning Portal", font=font(25, True), fill=(255, 231, 178, 255))
    return canvas


def learning_path() -> Image.Image:
    img = bg(1600, 620)
    draw = ImageDraw.Draw(img)
    draw.text((92, 66), "เส้นทางเรียนรู้ 3 ขั้น", font=font(58, True), fill=(255, 255, 255, 255))
    draw.text((96, 136), "Pre-Test → Learning → Post-Test พร้อมหลักฐานตรวจสอบได้", font=font(30, True), fill=(255, 230, 165, 255))
    cards = [
        ("01", "แบบทดสอบก่อนเรียน", "วัดพื้นฐานและตั้งเป้าหมาย", "quiz"),
        ("02", "เข้าห้องเรียนออนไลน์", "เรียนผ่านสื่อ กิจกรรม และภารกิจ", "robot"),
        ("03", "แบบทดสอบหลังเรียน", "สรุปผลก่อน-หลังและผ่านเกณฑ์", "medal"),
    ]
    for i, (num, title, desc, icon) in enumerate(cards):
        x = 95 + i * 500
        draw.rounded_rectangle((x, 220, x + 420, 525), radius=26, fill=(255, 255, 255, 235), outline=(255, 207, 102, 255), width=5)
        draw.rounded_rectangle((x + 28, 244, x + 128, 294), radius=25, fill=(210, 20, 36, 255))
        draw.text((x + 55, 249), num, font=font(28, True), fill=(255, 255, 255, 255))
        draw_icon(draw, x + 214, 324, icon)
        draw.text((x + 38, 414), title, font=font(34, True), fill=(92, 5, 14, 255))
        draw.text((x + 38, 462), desc, font=font(24, True), fill=(82, 65, 52, 255))
        if i < 2:
            draw.line((x + 428, 370, x + 486, 370), fill=(255, 207, 102, 255), width=8)
            draw.polygon([(x + 486, 370), (x + 462, 350), (x + 462, 390)], fill=(255, 207, 102, 255))
    return img


def ai_lab() -> Image.Image:
    img = bg(1600, 540)
    draw = ImageDraw.Draw(img)
    draw.text((92, 74), "AI • AR • Robot Learning Lab", font=font(62, True), fill=(255, 255, 255, 255))
    draw.text((96, 150), "เทคโนโลยีช่วยสอน สร้างสื่อ ประเมินผล และออกแบบประสบการณ์เรียนรู้", font=font(30, True), fill=(255, 232, 172, 255))
    chips = [("AI", "สร้าง Prompt และสื่อ"), ("AR", "เชื่อมโลกจริงกับดิจิทัล"), ("Robot", "คิดเชิงระบบและ Coding")]
    for i, (label, desc) in enumerate(chips):
        x = 110 + i * 480
        draw.rounded_rectangle((x, 250, x + 420, 430), radius=24, fill=(255, 255, 255, 32), outline=(255, 255, 255, 90), width=2)
        draw.text((x + 34, 280), label, font=font(54, True), fill=(255, 207, 102, 255))
        draw.text((x + 34, 350), desc, font=font(27, True), fill=(90, 4, 13, 255))
    draw_icon(draw, 1420, 142, "robot")
    return img


def evidence_map() -> Image.Image:
    img = bg(1600, 600)
    draw = ImageDraw.Draw(img)
    draw.text((92, 60), "เส้นทางตรวจหลักฐาน 3 นาที", font=font(58, True), fill=(255, 255, 255, 255))
    draw.text((96, 132), "เริ่มจากข้อมูลหลัก → เอกสาร PA → ผลก่อน-หลัง → หลักฐาน Drive", font=font(30, True), fill=(255, 231, 170, 255))
    steps = ["ข้อมูลหลัก", "PA 3 ด้าน", "นวัตกรรม", "ก่อน-หลัง", "Drive 12 รายการ"]
    points = [(170, 355), (470, 355), (770, 355), (1070, 355), (1370, 355)]
    draw.line((170, 355, 1370, 355), fill=(255, 207, 102, 170), width=8)
    for i, ((x, y), label) in enumerate(zip(points, steps), start=1):
        draw.ellipse((x - 58, y - 58, x + 58, y + 58), fill=(255, 255, 255, 238), outline=(255, 207, 102, 255), width=5)
        draw.text((x - 17, y - 34), str(i), font=font(54, True), fill=(171, 10, 23, 255))
        w = draw.textbbox((0, 0), label, font=font(28, True))[2]
        draw.text((x - w // 2, y + 82), label, font=font(28, True), fill=(255, 255, 255, 245))
    return img


def quiz_badge() -> Image.Image:
    img = bg(1200, 520)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((92, 70, 1108, 450), radius=42, fill=(255, 255, 255, 24), outline=(255, 207, 102, 180), width=3)
    draw_icon(draw, 230, 250, "quiz")
    draw.rounded_rectangle((336, 95, 1060, 400), radius=24, fill=(255, 255, 255, 232), outline=(255, 207, 102, 255), width=4)
    draw.text((374, 126), "Gamification + Quizizz", font=font(58, True), fill=(105, 4, 14, 255))
    draw.text((378, 205), "เรียนแบบภารกิจ เล่นอย่างมีเป้าหมาย", font=font(29, True), fill=(120, 25, 25, 255))
    draw.text((378, 248), "วัดผลได้ทันที พร้อมข้อมูลก่อน-หลัง", font=font(29, True), fill=(120, 25, 25, 255))
    pill(draw, (374, 300, 650, 370), (210, 20, 36, 255))
    draw.text((420, 315), "Pre/Post", font=font(28, True), fill=(255, 255, 255, 255))
    pill(draw, (680, 300, 980, 370), (120, 7, 18, 255))
    draw.text((720, 315), "% ผ่านเกณฑ์", font=font(28, True), fill=(255, 255, 255, 255))
    return img


def drive_grid() -> Image.Image:
    img = bg(1400, 620)
    draw = ImageDraw.Draw(img)
    draw.text((92, 58), "Drive Evidence Wall", font=font(58, True), fill=(255, 255, 255, 255))
    draw.text((96, 132), "12 หลักฐานสำคัญสำหรับคณะกรรมการ เปิดดูเร็ว ตรวจต่อได้ครบ", font=font(31, True), fill=(255, 230, 165, 255))
    labels = ["PA", "SAR", "ID Plan", "สื่อสอน", "นวัตกรรม", "ภาพกิจกรรม", "PLC", "อบรม", "รางวัล", "ชิ้นงาน", "ผู้ปกครอง", "วิจัย"]
    for i, label in enumerate(labels):
        col = i % 4
        row = i // 4
        x = 120 + col * 305
        y = 220 + row * 112
        draw.rounded_rectangle((x, y, x + 250, y + 78), radius=14, fill=(255, 255, 255, 235), outline=(255, 207, 102, 255), width=3)
        draw_icon(draw, x + 48, y + 39, "drive")
        draw.text((x + 96, y + 24), label, font=font(27, True), fill=(88, 5, 13, 255))
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assets = [
        ("01-red-click-button.png", cta_button()),
        ("02-learning-path.png", learning_path()),
        ("03-ai-ar-robot-lab.png", ai_lab()),
        ("04-evidence-map.png", evidence_map()),
        ("05-gamification-quizizz.png", quiz_badge()),
        ("06-drive-evidence-wall.png", drive_grid()),
    ]
    for name, img in assets:
        save(img, name)

    sheet = Image.new("RGB", (1200, 1080), "#f5eee8")
    positions = [(0, 0), (0, 270), (0, 570), (600, 0), (600, 315), (600, 590)]
    for (name, img), (x, y) in zip(assets, positions):
        thumb = img.resize((560, int(img.height * 560 / img.width)))
        if thumb.mode == "RGBA":
            sheet.paste(thumb.convert("RGB"), (x + 20, y + 20), thumb.getchannel("A"))
        else:
            sheet.paste(thumb.convert("RGB"), (x + 20, y + 20))
    sheet.save(OUT_DIR / "preview-sheet.png", optimize=True)
    print(f"Generated {len(assets)} visual play assets in {OUT_DIR}")


if __name__ == "__main__":
    main()
