#!/usr/bin/env python3
"""Generate Signa's original orange Liquid Glass icon assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "Feather/Resources/Assets.xcassets/AppIcon.appiconset"
LAYER_DIR = ROOT / "Feather/Resources/AppIcon.icon/Assets"
SIZE = 2048


def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


SEGMENTS = [
    [(1330, 470), (950, 250), (520, 540), (715, 850)],
    [(715, 850), (850, 1060), (1370, 980), (1360, 1280)],
    [(1360, 1280), (1350, 1570), (850, 1660), (690, 1530)],
]
POINTS = [cubic(*segment, i / 120) for segment in SEGMENTS for i in range(121)]


def smooth_stroke(draw, points, color, width, dx=0, dy=0):
    radius = width / 2
    for x, y in points:
        x += dx
        y += dy
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def background(top, bottom):
    gradient = Image.linear_gradient("L").resize((SIZE, SIZE))
    return Image.merge("RGB", [
        Image.eval(gradient, lambda t, a=a, b=b: int(a + (b - a) * t / 255))
        for a, b in zip(top, bottom)
    ]).convert("RGBA")


def make_icon(dark=False, tinted=False):
    top, bottom = ((61, 27, 22), (172, 55, 24)) if dark else ((255, 183, 91), (244, 83, 16))
    if tinted:
        top, bottom = (248, 248, 248), (205, 205, 205)
    image = background(top, bottom)

    glow = Image.new("RGBA", (SIZE, SIZE))
    draw = ImageDraw.Draw(glow)
    draw.ellipse((-500, -650, 1450, 1250), fill=(255, 245, 215, 90 if not tinted else 45))
    draw.ellipse((900, 1150, 2500, 2600), fill=(255, 120, 45, 70 if not tinted else 20))
    image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(150)))

    glass = Image.new("RGBA", (SIZE, SIZE))
    draw = ImageDraw.Draw(glass)
    draw.ellipse((220, 250, 1820, 1850), fill=(255, 255, 255, 22), outline=(255, 255, 255, 95), width=8)
    draw.ellipse((410, 410, 1640, 1640), fill=(255, 255, 255, 16), outline=(255, 255, 255, 55), width=4)
    draw.arc((260, 290, 1780, 1810), 200, 318, fill=(255, 255, 255, 170), width=14)
    image = Image.alpha_composite(image, glass)

    shadow = Image.new("RGBA", (SIZE, SIZE))
    smooth_stroke(ImageDraw.Draw(shadow), POINTS, (89, 28, 7, 45), 250, 18, 32)
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(16)))

    ribbon = Image.new("RGBA", (SIZE, SIZE))
    draw = ImageDraw.Draw(ribbon)
    smooth_stroke(draw, POINTS, (255, 255, 255, 235), 248)
    smooth_stroke(draw, POINTS, (255, 255, 255, 100), 62, -22, -24)
    image = Image.alpha_composite(image, ribbon)

    highlight = Image.new("RGBA", (SIZE, SIZE))
    ImageDraw.Draw(highlight).rounded_rectangle((120, 110, 1928, 750), radius=300, fill=(255, 255, 255, 28))
    image = Image.alpha_composite(image, highlight.filter(ImageFilter.GaussianBlur(80)))
    return image.resize((1024, 1024), Image.Resampling.LANCZOS).convert("RGB")


ASSET_DIR.mkdir(parents=True, exist_ok=True)
LAYER_DIR.mkdir(parents=True, exist_ok=True)
make_icon().save(ASSET_DIR / "signa.png")
make_icon(dark=True).save(ASSET_DIR / "signa_dark.png")
make_icon(tinted=True).save(ASSET_DIR / "signa_tint.png")

layer = Image.new("RGBA", (SIZE, SIZE))
smooth_stroke(ImageDraw.Draw(layer), POINTS, (255, 255, 255, 245), 248)
layer.resize((1024, 1024), Image.Resampling.LANCZOS).save(LAYER_DIR / "feather.png")

shine = Image.new("RGBA", (SIZE, SIZE))
ImageDraw.Draw(shine).ellipse((200, 100, 1848, 920), fill=(255, 255, 255, 90))
shine.filter(ImageFilter.GaussianBlur(120)).resize((1024, 1024), Image.Resampling.LANCZOS).save(LAYER_DIR / "feather 5.png")
print("Generated Signa icon assets")
