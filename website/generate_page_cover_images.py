from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from generate_page_covers import PAGES


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "assets" / "page-covers"
PORTRAIT_PATH = ROOT / "assets" / "krujames-portrait-red-web.jpg"

FONT_REGULAR = Path("C:/Windows/Fonts/tahoma.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/tahomabd.ttf")

W, H = 1600, 600


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if text_width(draw, candidate, fnt) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def gradient_bg() -> Image.Image:
    img = Image.new("RGB", (W, H), "#1c0105")
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = (x / W) * 0.72 + (y / H) * 0.28
            glow = max(0, 1 - math.hypot((x - 1280) / 760, (y - 120) / 460))
            r = int(28 + 150 * t + 64 * glow)
            g = int(2 + 10 * t + 16 * glow)
            b = int(7 + 14 * t + 10 * glow)
            px[x, y] = (min(r, 170), min(g, 38), min(b, 44))
    return img


def draw_tech(draw: ImageDraw.ImageDraw) -> None:
    grid = (255, 255, 255, 22)
    for x in range(0, W, 64):
        draw.line((x, 0, x, H), fill=grid, width=1)
    for y in range(0, H, 64):
        draw.line((0, y, W, y), fill=grid, width=1)

    for offset in range(-260, 1460, 220):
        draw.line((offset, H, offset + 460, 0), fill=(255, 207, 102, 34), width=2)

    for r, alpha in [(360, 56), (470, 38), (590, 24)]:
        draw.ellipse((W - r - 60, 40 - r // 2, W + r // 2, 40 + r), outline=(255, 207, 102, alpha), width=3)

    for i in range(18):
        x = 1180 + (i * 71) % 360
        y = 100 + (i * 43) % 360
        draw.ellipse((x, y, x + 8, y + 8), fill=(255, 207, 102, 120))
        if i % 3 == 0:
            draw.line((x + 4, y + 4, x - 80, y + 36), fill=(255, 255, 255, 36), width=2)


def paste_portrait(base: Image.Image) -> None:
    portrait = Image.open(PORTRAIT_PATH).convert("RGB")
    portrait = ImageOps.fit(portrait, (178, 178), centering=(0.5, 0.18))
    mask = Image.new("L", (178, 178), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((0, 0, 178, 178), fill=255)

    ring = Image.new("RGBA", (198, 198), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(ring)
    rdraw.ellipse((4, 4, 194, 194), fill=(255, 207, 102, 255))
    rdraw.ellipse((14, 14, 184, 184), fill=(90, 5, 15, 255))

    base.alpha_composite(ring, (1246, 115))
    base.paste(portrait.convert("RGBA"), (1256, 125), mask)


def draw_chip(draw: ImageDraw.ImageDraw, x: int, y: int, label: str) -> int:
    fnt = font(24, bold=True)
    pad_x = 22
    box = draw.textbbox((0, 0), label, font=fnt)
    width = box[2] - box[0] + pad_x * 2
    draw.rounded_rectangle((x, y, x + width, y + 46), radius=23, fill=(255, 255, 255, 24), outline=(255, 255, 255, 70), width=1)
    draw.text((x + pad_x, y + 8), label, font=fnt, fill=(255, 249, 232, 238))
    return x + width + 12


def draw_stat(draw: ImageDraw.ImageDraw, x: int, y: int, value: str, label: str) -> None:
    draw.rounded_rectangle((x, y, x + 310, y + 76), radius=8, fill=(255, 255, 255, 22), outline=(255, 255, 255, 54), width=1)
    draw.text((x + 18, y + 12), value, font=font(27, bold=True), fill=(255, 207, 102, 255))
    draw.text((x + 18, y + 45), label, font=font(18, bold=True), fill=(255, 255, 255, 190))


def render(page: dict[str, object]) -> Image.Image:
    base = gradient_bg().convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_tech(draw)

    draw.rounded_rectangle((64, 54, W - 64, H - 54), radius=18, outline=(255, 255, 255, 58), width=2)
    draw.rounded_rectangle((76, 66, W - 76, H - 66), radius=12, outline=(255, 207, 102, 38), width=1)
    draw.rectangle((64, H - 92, W - 64, H - 54), fill=(45, 2, 8, 92))

    kicker_font = font(25, bold=True)
    title_font = font(74, bold=True)
    lead_font = font(31)
    focus_font = font(23)

    draw.rounded_rectangle((116, 105, 208, 112), radius=4, fill=(255, 207, 102, 255))
    draw.text((230, 88), str(page["kicker"]), font=kicker_font, fill=(255, 222, 146, 255))

    title_lines = wrap_text(draw, str(page["title"]), title_font, 960)
    if len(title_lines) > 1:
        title_font = font(58, bold=True)
        title_lines = wrap_text(draw, str(page["title"]), title_font, 930)
    title_y = 138 if len(title_lines) > 1 else 148
    for line in title_lines[:2]:
        draw.text((112, title_y), line, font=title_font, fill=(255, 255, 255, 255))
        title_y += 68

    y = 252 + max(0, len(title_lines[:2]) - 1) * 36
    for line in wrap_text(draw, str(page["lead"]), lead_font, 940)[:2]:
        draw.text((116, y), line, font=lead_font, fill=(255, 247, 228, 232))
        y += 44

    y += 16
    draw.rounded_rectangle((116, y + 2, 122, y + 104), radius=3, fill=(255, 207, 102, 220))
    for line in wrap_text(draw, str(page["focus"]), focus_font, 890)[:3]:
        draw.text((142, y), line, font=focus_font, fill=(255, 255, 255, 200))
        y += 34

    chip_x = 116
    chip_y = 490
    for label in list(page["chips"])[:4]:
        chip_x = draw_chip(draw, chip_x, chip_y, str(label))

    draw.rounded_rectangle((1200, 86, 1488, 514), radius=16, fill=(18, 1, 5, 150), outline=(255, 255, 255, 68), width=2)
    paste_portrait(overlay)

    draw.text((1260, 315), "ครูเจมส์", font=font(40, bold=True), fill=(255, 255, 255, 255))
    draw.text((1240, 366), "เทคโนโลยี · วิทยาการคำนวณ", font=font(22, bold=True), fill=(255, 236, 187, 218))
    draw.text((1396, 92), str(page["page_no"]), font=font(84, bold=True), fill=(255, 255, 255, 34))

    stats = list(page["stats"])
    draw_stat(draw, 1216, 420, str(stats[0][0]), str(stats[0][1]))
    draw_stat(draw, 1216, 504, str(stats[1][0]), str(stats[1][1]))

    base.alpha_composite(overlay)
    return base.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    thumbs: list[Image.Image] = []
    for page in PAGES:
        image = render(page)
        out = OUT_DIR / f"{page['slug']}.png"
        image.save(out, optimize=True)
        thumbs.append(image.resize((400, 150)))

    sheet = Image.new("RGB", (1200, 900), "#f4eee9")
    for idx, thumb in enumerate(thumbs):
        x = (idx % 3) * 400
        y = (idx // 3) * 225
        sheet.paste(thumb, (x, y))
    sheet.save(OUT_DIR / "preview-sheet.png", optimize=True)
    print(f"Generated {len(PAGES)} cover images in {OUT_DIR}")


if __name__ == "__main__":
    main()
