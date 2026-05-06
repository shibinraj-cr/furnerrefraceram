"""
Generate on-brand placeholder JPG images for the Furner RefraCeram site.
Each image follows the design system palette and aesthetic so the site
looks intentional even before real AI-generated photography is dropped in.
"""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)

OUT = os.path.join(os.path.dirname(__file__), "assets", "img")
os.makedirs(OUT, exist_ok=True)

# Design palette
INK = (13, 13, 14)
INK2 = (26, 26, 28)
PAPER = (244, 239, 231)
CREAM = (235, 228, 214)
EMBER = (210, 78, 14)
EMBER_GLOW = (245, 160, 74)
STEEL = (107, 107, 112)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_noise(img, amount=18):
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            n = random.randint(-amount, amount)
            r, g, b = px[x, y][:3]
            px[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
            )
    return img


def radial_gradient(size, inner, outer, center=None, falloff=1.0):
    w, h = size
    if center is None:
        center = (w // 2, h // 2)
    cx, cy = center
    img = Image.new("RGB", size, outer)
    px = img.load()
    maxd = math.hypot(max(cx, w - cx), max(cy, h - cy))
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / maxd
            d = min(1, d ** falloff)
            px[x, y] = lerp(inner, outer, d)
    return img


def linear_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = lerp(top, bottom, t)
        for x in range(w):
            px[x, y] = c
    return img


def vignette(img, strength=0.55):
    w, h = img.size
    overlay = Image.new("RGB", (w, h), (0, 0, 0))
    px = overlay.load()
    cx, cy = w / 2, h / 2
    maxd = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / maxd
            v = int(min(255, max(0, (d ** 2) * 255 * strength)))
            px[x, y] = (v, v, v)
    return Image.blend(img, Image.new("RGB", (w, h), (0, 0, 0)), 0).point(lambda p: p)\
        if False else _multiply_dark(img, overlay)


def _multiply_dark(base, dark_overlay):
    """Darken base by overlay luminance."""
    w, h = base.size
    bp = base.load()
    op = dark_overlay.load()
    out = Image.new("RGB", (w, h))
    pp = out.load()
    for y in range(h):
        for x in range(w):
            br, bg, bb = bp[x, y]
            o = op[x, y][0] / 255
            pp[x, y] = (int(br * (1 - o)), int(bg * (1 - o)), int(bb * (1 - o)))
    return out


def scatter_grains(img, count, color_fn, size_range=(2, 6), opacity_fn=None):
    """Draw irregular angular 'grains' for product close-up feel."""
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for _ in range(count):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(*size_range)
        col = color_fn()
        op = opacity_fn() if opacity_fn else random.randint(170, 250)
        # angular polygon
        pts = []
        sides = random.randint(4, 6)
        rot = random.uniform(0, math.pi * 2)
        for i in range(sides):
            a = rot + i * (2 * math.pi / sides) + random.uniform(-0.3, 0.3)
            r = s * random.uniform(0.6, 1.3)
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        draw.polygon(pts, fill=(*col, op))
        # tiny highlight
        if random.random() < 0.4:
            hx, hy = x - s * 0.3, y - s * 0.3
            draw.ellipse([hx - 1, hy - 1, hx + 1, hy + 1], fill=(255, 255, 255, 200))
    return img


def save_jpg(img, name, quality=82):
    path = os.path.join(OUT, name)
    img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True)
    print(f"  {name}  {os.path.getsize(path)//1024}KB")


# ---------- HERO & ATMOSPHERIC ----------

def hero_crucible():
    """Molten alumina inside furnace — orange-white core on charcoal."""
    w, h = 1600, 1000
    img = radial_gradient((w, h), EMBER_GLOW, INK, center=(w * 0.55, h * 0.5), falloff=0.7)
    # add inner brighter core
    core = radial_gradient((w, h), (255, 220, 160), (0, 0, 0), center=(w * 0.55, h * 0.5), falloff=1.4)
    img = Image.blend(img, core, 0.45)
    # darken edges (manual vignette)
    px = img.load()
    cx, cy = w * 0.55, h * 0.5
    maxd = math.hypot(max(cx, w - cx), max(cy, h - cy))
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / maxd
            f = max(0, min(1, (d - 0.3) * 1.4))
            r, g, b = px[x, y]
            px[x, y] = (int(r * (1 - f * 0.85)), int(g * (1 - f * 0.85)), int(b * (1 - f * 0.85)))
    # spark specks
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(180):
        x = random.randint(0, w)
        y = random.randint(0, int(h * 0.85))
        s = random.choice([1, 1, 1, 2, 2, 3])
        glow = random.choice([(255, 200, 130), (255, 230, 180), (255, 160, 80)])
        a = random.randint(150, 255)
        draw.ellipse([x - s, y - s, x + s, y + s], fill=(*glow, a))
    img = add_noise(img, 8)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    save_jpg(img, "hero-crucible.jpg", quality=85)


def hero_grain_macro():
    w, h = 1600, 1000
    img = linear_gradient((w, h), (18, 14, 12), (8, 6, 6))
    # ember side light
    glow = radial_gradient((w, h), (180, 100, 50), (0, 0, 0), center=(w * 0.2, h * 0.3), falloff=1.2)
    img = Image.blend(img, glow, 0.35)
    img = scatter_grains(
        img, 1200,
        color_fn=lambda: random.choice([(120, 70, 40), (90, 50, 25), (160, 95, 55), (70, 40, 20)]),
        size_range=(4, 14),
    )
    img = add_noise(img, 10)
    save_jpg(img, "hero-grain-macro.jpg", quality=82)


def texture_refractory():
    w, h = 1600, 900
    img = linear_gradient((w, h), (235, 225, 205), (200, 185, 160))
    # brick joints
    draw = ImageDraw.Draw(img)
    for y in range(0, h, 90):
        draw.line([(0, y), (w, y)], fill=(150, 130, 100), width=2)
    for col, off in enumerate(range(0, w, 180)):
        for y in range(0, h, 90):
            x = off + (90 if (y // 90) % 2 else 0)
            draw.line([(x, y), (x, y + 90)], fill=(150, 130, 100), width=2)
    # scattered specks (iron oxide flecks)
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(900):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(1, 3)
        col = random.choice([(120, 60, 30), (90, 45, 20), (160, 90, 50)])
        draw.ellipse([x - s, y - s, x + s, y + s], fill=(*col, random.randint(120, 220)))
    img = add_noise(img, 14)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    save_jpg(img, "texture-refractory.jpg", quality=80)


def texture_chemicals():
    w, h = 1600, 900
    img = linear_gradient((w, h), (245, 242, 235), (220, 215, 205))
    # subtle sparkle
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(2000):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.choice([1, 1, 2])
        a = random.randint(180, 255)
        draw.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, a))
    # cool window-light gradient overlay
    overlay = linear_gradient((w, h), (255, 255, 255), (180, 190, 200))
    img = Image.blend(img, overlay, 0.25)
    img = add_noise(img, 6)
    save_jpg(img, "texture-chemicals.jpg", quality=82)


# ---------- PRODUCT CLOSE-UPS (4:5 portrait) ----------

def product_card(name, base_palette, light_pos=(0.3, 0.3), bg=(20, 18, 18)):
    w, h = 1200, 1500
    img = linear_gradient((w, h), bg, (max(0, bg[0]-10), max(0, bg[1]-10), max(0, bg[2]-10)))
    glow = radial_gradient((w, h), (200, 150, 90), (0, 0, 0),
                           center=(int(w * light_pos[0]), int(h * light_pos[1])), falloff=1.1)
    img = Image.blend(img, glow, 0.25)
    img = scatter_grains(
        img, 1800,
        color_fn=lambda: random.choice(base_palette),
        size_range=(5, 16),
    )
    # softer scatter pass
    img = scatter_grains(
        img, 600,
        color_fn=lambda: random.choice(base_palette),
        size_range=(3, 8),
        opacity_fn=lambda: random.randint(80, 160),
    )
    img = add_noise(img, 8)
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    save_jpg(img, name, quality=82)


def product_powder(name, base_color, vessel_tone=(220, 218, 210), bg=(225, 220, 210)):
    """Crystalline powder in glass vessel — for chemicals."""
    w, h = 1200, 1500
    img = linear_gradient((w, h), bg, (bg[0]-30, bg[1]-30, bg[2]-30))
    # glass vessel suggestion
    draw = ImageDraw.Draw(img, "RGBA")
    cx = w // 2
    cy = int(h * 0.6)
    rw, rh = 380, 280
    draw.ellipse([cx - rw, cy - rh//4, cx + rw, cy + rh//2], fill=(*vessel_tone, 180))
    # powder mound
    for r in range(rw, 0, -8):
        a = int(180 * (r / rw))
        c = lerp(base_color, (255, 255, 255), 0.25 + 0.3 * (1 - r / rw))
        draw.ellipse([cx - r, cy - r//2, cx + r, cy + r//3], fill=(*c, a))
    # crystal sparkles
    for _ in range(1500):
        x = random.randint(cx - rw, cx + rw)
        y = random.randint(cy - rh//4, cy + rh//3)
        if abs(x - cx) / rw + abs(y - cy) / (rh/2) < 1.1:
            s = random.choice([1, 1, 2, 3])
            a = random.randint(180, 255)
            draw.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, a))
    img = add_noise(img, 7)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    save_jpg(img, name, quality=82)


# ---------- SECTION / CONTEXTUAL (16:10) ----------

def category_abrasives():
    w, h = 1400, 1000
    img = linear_gradient((w, h), (30, 25, 22), (12, 10, 9))
    # grinding wheel circle
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = w // 2, h // 2
    R = int(h * 0.42)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(60, 45, 35, 255))
    draw.ellipse([cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14], fill=(80, 60, 45, 255))
    # center bore
    r = 60
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(15, 12, 10, 255))
    # surface grains
    for _ in range(2500):
        a = random.uniform(0, math.pi * 2)
        rr = random.uniform(r + 10, R - 8)
        x = cx + math.cos(a) * rr
        y = cy + math.sin(a) * rr
        s = random.randint(2, 5)
        col = random.choice([(140, 85, 50), (100, 60, 35), (170, 110, 65)])
        draw.ellipse([x - s, y - s, x + s, y + s], fill=(*col, random.randint(180, 250)))
    # warm side light
    glow = radial_gradient((w, h), (180, 100, 50), (0, 0, 0), center=(w * 0.15, h * 0.5), falloff=1.2)
    img = Image.blend(img, glow, 0.25)
    img = add_noise(img, 8)
    save_jpg(img, "category-abrasives.jpg", quality=82)


def category_refractory():
    w, h = 1400, 1000
    img = radial_gradient((w, h), (255, 140, 60), (8, 6, 6), center=(w * 0.5, h * 0.6), falloff=0.9)
    inner = radial_gradient((w, h), (255, 220, 150), (0, 0, 0), center=(w * 0.5, h * 0.6), falloff=1.5)
    img = Image.blend(img, inner, 0.4)
    # arch suggestion — darken upper arch lines
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(0, int(h * 0.4), 60):
        draw.line([(0, y), (w, y)], fill=(0, 0, 0, 80), width=4)
    # vertical brick joints
    for x in range(0, w, 110):
        draw.line([(x, 0), (x, int(h * 0.45))], fill=(0, 0, 0, 60), width=3)
    img = add_noise(img, 8)
    save_jpg(img, "category-refractory.jpg", quality=82)


def category_chemicals():
    w, h = 1400, 1000
    img = linear_gradient((w, h), (60, 65, 72), (25, 28, 32))
    draw = ImageDraw.Draw(img, "RGBA")
    # vertical reactor cylinders
    for cx in [int(w * 0.25), int(w * 0.55), int(w * 0.82)]:
        cw = 140
        # body
        draw.rectangle([cx - cw // 2, int(h * 0.2), cx + cw // 2, int(h * 0.85)],
                       fill=(180, 185, 195, 255))
        # top dome
        draw.ellipse([cx - cw // 2, int(h * 0.15), cx + cw // 2, int(h * 0.28)],
                     fill=(200, 205, 215, 255))
        # specular highlight
        draw.rectangle([cx - cw // 2 + 12, int(h * 0.2), cx - cw // 2 + 24, int(h * 0.85)],
                       fill=(240, 245, 250, 255))
        # shadow
        draw.rectangle([cx + cw // 2 - 18, int(h * 0.2), cx + cw // 2 - 6, int(h * 0.85)],
                       fill=(80, 85, 95, 255))
    # top light wash
    overlay = linear_gradient((w, h), (255, 255, 255), (0, 0, 0))
    img = Image.blend(img, overlay, 0.12)
    img = add_noise(img, 6)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    save_jpg(img, "category-chemicals.jpg", quality=82)


def lab_qc():
    w, h = 1400, 1000
    img = linear_gradient((w, h), (210, 215, 220), (160, 165, 172))
    draw = ImageDraw.Draw(img, "RGBA")
    # bench surface
    draw.rectangle([0, int(h * 0.65), w, h], fill=(80, 85, 92, 255))
    # vials in rack — small rectangles
    rack_y = int(h * 0.55)
    for i in range(8):
        x = int(w * 0.1) + i * 80
        draw.rectangle([x, rack_y, x + 30, rack_y + 90], fill=(220, 230, 240, 230))
        draw.rectangle([x + 4, rack_y + 30, x + 26, rack_y + 86],
                       fill=random.choice([(180, 200, 220, 255), (200, 215, 200, 255), (210, 200, 195, 255)]))
    # instrument box
    draw.rectangle([int(w * 0.55), int(h * 0.3), int(w * 0.9), int(h * 0.65)],
                   fill=(45, 50, 58, 255))
    draw.rectangle([int(w * 0.58), int(h * 0.34), int(w * 0.87), int(h * 0.5)],
                   fill=(20, 25, 30, 255))
    # subtle ember accent
    draw.rectangle([int(w * 0.58), int(h * 0.61), int(w * 0.6), int(h * 0.63)],
                   fill=(*EMBER, 255))
    img = add_noise(img, 8)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    save_jpg(img, "lab-qc.jpg", quality=82)


def facility():
    w, h = 1600, 900
    img = linear_gradient((w, h), (50, 45, 40), (15, 12, 10))
    glow = radial_gradient((w, h), (240, 180, 110), (0, 0, 0), center=(w * 0.7, h * 0.25), falloff=1.0)
    img = Image.blend(img, glow, 0.45)
    draw = ImageDraw.Draw(img, "RGBA")
    # high windows
    for i in range(6):
        x = int(w * 0.1) + i * int(w * 0.13)
        draw.rectangle([x, int(h * 0.08), x + int(w * 0.08), int(h * 0.32)],
                       fill=(255, 220, 160, 200))
    # floor / horizon
    draw.rectangle([0, int(h * 0.7), w, h], fill=(20, 18, 16, 255))
    # equipment silhouettes
    for i in range(4):
        x = int(w * 0.15) + i * int(w * 0.2)
        draw.rectangle([x, int(h * 0.5), x + int(w * 0.08), int(h * 0.7)],
                       fill=(35, 30, 26, 255))
        draw.rectangle([x - 10, int(h * 0.45), x + int(w * 0.08) + 10, int(h * 0.5)],
                       fill=(50, 42, 36, 255))
    img = add_noise(img, 8)
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    save_jpg(img, "facility.jpg", quality=82)


def industries_bg():
    w, h = 1600, 900
    img = linear_gradient((w, h), (40, 32, 28), (15, 12, 10))
    # layered patina strokes
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(60):
        y = random.randint(0, h)
        col = random.choice([(80, 50, 30, 30), (60, 40, 25, 30), (120, 70, 40, 30), (40, 28, 22, 60)])
        draw.rectangle([0, y, w, y + random.randint(2, 12)], fill=col)
    img = add_noise(img, 10)
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    save_jpg(img, "industries-bg.jpg", quality=78)


def og_image():
    w, h = 1200, 630
    img = radial_gradient((w, h), EMBER_GLOW, INK, center=(int(w * 0.65), h // 2), falloff=0.8)
    inner = radial_gradient((w, h), (255, 220, 160), (0, 0, 0), center=(int(w * 0.65), h // 2), falloff=1.4)
    img = Image.blend(img, inner, 0.4)
    draw = ImageDraw.Draw(img, "RGBA")
    for _ in range(120):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.choice([1, 1, 2])
        draw.ellipse([x - s, y - s, x + s, y + s],
                     fill=(255, random.randint(180, 230), random.randint(120, 180), random.randint(180, 255)))
    img = add_noise(img, 6)
    save_jpg(img, "og-image.jpg", quality=85)


# ---------- BUILD ----------

def main():
    print("Generating placeholder imagery...")

    hero_crucible()
    hero_grain_macro()
    texture_refractory()
    texture_chemicals()

    # Product close-ups
    product_card("prod-brown-alumina.jpg",
                 [(120, 70, 40), (95, 55, 28), (150, 90, 50), (75, 45, 22), (170, 100, 60)])
    product_card("prod-white-alumina.jpg",
                 [(235, 235, 235), (210, 210, 215), (250, 250, 245), (190, 192, 198)])
    product_card("prod-pink-alumina.jpg",
                 [(220, 160, 165), (190, 130, 140), (230, 175, 180), (170, 110, 120)])
    product_card("prod-ruby-alumina.jpg",
                 [(160, 35, 40), (120, 25, 30), (180, 50, 55), (90, 18, 22), (200, 65, 70)])
    product_card("prod-black-sic.jpg",
                 [(40, 40, 45), (25, 25, 30), (60, 55, 65), (15, 15, 18), (80, 70, 90)])
    product_card("prod-green-sic.jpg",
                 [(50, 110, 75), (30, 80, 55), (70, 140, 95), (90, 160, 110), (20, 60, 40)])
    product_card("prod-zirconia.jpg",
                 [(180, 175, 165), (210, 205, 195), (140, 135, 128), (230, 225, 215)])
    product_card("prod-garnet.jpg",
                 [(110, 35, 30), (85, 25, 22), (140, 50, 40), (70, 20, 18), (160, 65, 50)])
    product_card("prod-glass-bead.jpg",
                 [(220, 230, 240), (180, 195, 210), (240, 245, 250), (160, 175, 195)],
                 light_pos=(0.5, 0.4), bg=(30, 32, 36))
    product_card("prod-tabular-alumina.jpg",
                 [(220, 215, 200), (240, 235, 220), (190, 185, 170), (200, 195, 180)])

    product_powder("prod-oxalic-acid.jpg", (250, 248, 245), bg=(230, 226, 218))
    product_powder("prod-pto-pbo.jpg", (245, 244, 240), bg=(210, 215, 220))

    category_abrasives()
    category_refractory()
    category_chemicals()
    lab_qc()
    facility()
    industries_bg()
    og_image()

    print("Done.")


if __name__ == "__main__":
    main()
