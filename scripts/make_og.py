"""Generate OG / Twitter card image (1200x630) from scratch — no external assets.

Linear-style: dark canvas with two violet glow orbs, big serif headline,
brand mark, and a tag-line.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path("public/og.png")
W, H = 1200, 630

img = Image.new("RGB", (W, H), (8, 9, 10))
draw = ImageDraw.Draw(img)


def glow_orb(cx, cy, radius, color_rgba):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill=color_rgba,
    )
    layer = layer.filter(ImageFilter.GaussianBlur(radius=80))
    img.alpha_composite(layer.convert("RGBA")) if False else None
    # alpha_composite needs both RGBA
    base = img.convert("RGBA")
    base.alpha_composite(layer)
    return base.convert("RGB")


# convert canvas to RGBA for orb compositing
canvas = img.convert("RGBA")
o1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(o1).ellipse((100, 100, 600, 600), fill=(113, 112, 255, 80))
o1 = o1.filter(ImageFilter.GaussianBlur(radius=120))
canvas.alpha_composite(o1)

o2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(o2).ellipse((700, 280, 1250, 750), fill=(94, 106, 210, 70))
o2 = o2.filter(ImageFilter.GaussianBlur(radius=120))
canvas.alpha_composite(o2)

img = canvas.convert("RGB")
draw = ImageDraw.Draw(img)


def load_font(name_candidates, size):
    for name in name_candidates:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


# fonts (windows): Calibri / Arial / Times New Roman
serif_xl = load_font(
    ["C:/Windows/Fonts/times.ttf", "Times New Roman.ttf"], 88
)
sans_lg = load_font(["C:/Windows/Fonts/arialbd.ttf", "Arial.ttf"], 26)
sans = load_font(["C:/Windows/Fonts/arial.ttf", "Arial.ttf"], 22)
sans_sm = load_font(["C:/Windows/Fonts/arial.ttf", "Arial.ttf"], 20)


# brand mark (top-left)
def round_rect(xy, r, fill, outline=None, width=0):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


round_rect((72, 72, 72 + 40, 72 + 40), 10, fill=(113, 112, 255))
draw.text((82, 76), "O", fill=(255, 255, 255), font=sans_lg)
draw.text((132, 80), "Omnia.AI", fill=(247, 248, 248), font=sans_lg)


# eyebrow pill (top-right)
pill_text = "PRE-LAUNCH · WAITLIST OPEN"
bbox = draw.textbbox((0, 0), pill_text, font=sans_sm)
pw = bbox[2] - bbox[0]
ph = bbox[3] - bbox[1]
px = W - 72 - pw - 32
py = 78
draw.rounded_rectangle(
    (px, py, px + pw + 32, py + ph + 16),
    radius=20,
    fill=(113, 112, 255, 30),
    outline=(113, 112, 255, 100),
    width=2,
)
draw.text((px + 16, py + 8), pill_text, fill=(139, 138, 255), font=sans_sm)


# Big headline (centered, two lines)
line1 = "Ваш сайт за час,"
line2 = "не за месяц."
draw.text((72, 240), line1, fill=(247, 248, 248), font=serif_xl)
# accent line
draw.text((72, 340), line2, fill=(180, 184, 200), font=serif_xl)


# Sub
sub = "Frontend, backend, домен и SSL — собирает AI. От 990 ₽/мес."
draw.text((72, 460), sub, fill=(168, 170, 177), font=sans)


# Footer strip with key facts
foot_y = 540
divider_y = foot_y - 14
draw.line((72, divider_y, W - 72, divider_y), fill=(255, 255, 255, 30), width=1)

facts = [
    "Без VPN и крипты",
    "Российские серверы",
    "152-ФЗ из коробки",
    "Откат версий в 1 клик",
]
x = 72
for text in facts:
    # green dot bullet
    draw.ellipse((x, foot_y + 11, x + 9, foot_y + 20), fill=(39, 166, 68))
    x_after = x + 9 + 10
    draw.text((x_after, foot_y), text, fill=(220, 222, 230), font=sans_sm)
    bbox = draw.textbbox((0, 0), text, font=sans_sm)
    x = x_after + (bbox[2] - bbox[0]) + 36


OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"OK: {OUT} ({OUT.stat().st_size} bytes, {W}x{H})")
