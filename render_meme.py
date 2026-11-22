# Draws the GTA 6 meme for make.fun bounty gta6-meme-x-01.
# Original art, drawn with PIL: Vice City sunset, an alligator in sunglasses
# holding a GTA VI game case, and make.fun's white ghost celebrating beside
# it with its magenta star coin. Run: python3 render_meme.py
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "meme.png"
FONT_DIR = "fonts"

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")

# --- sky: purple -> magenta -> orange gradient -----------------------------
top = (38, 8, 74)
mid = (176, 38, 120)
low = (255, 122, 48)
for y in range(700):
    if y < 350:
        t = y / 350
        c = tuple(int(top[i] + (mid[i] - top[i]) * t) for i in range(3))
    else:
        t = (y - 350) / 350
        c = tuple(int(mid[i] + (low[i] - mid[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# --- synthwave sun with slats ----------------------------------------------
sun_cx, sun_cy, sun_r = 512, 430, 190
d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
          fill=(255, 214, 90))
# cut horizontal slats out of the lower half, clipped to the sun's chord
for (y0, h) in [(470, 6), (495, 9), (525, 12), (560, 16), (600, 20)]:
    yc = y0 + h / 2
    dy = yc - sun_cy
    hw = math.sqrt(max(0, sun_r * sun_r - dy * dy))
    d.rectangle([sun_cx - hw, y0, sun_cx + hw, y0 + h],
                fill=(255, 122, 48))

# --- stars in the upper sky -------------------------------------------------
import random
rng = random.Random(6)
for _ in range(70):
    x = rng.randint(0, W)
    y = rng.randint(0, 260)
    r = rng.choice([1, 1, 2])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 200))

# --- skyline silhouettes ----------------------------------------------------
def building(x, w, h, windows=True):
    d.rectangle([x, 640 - h, x + w, 640], fill=(28, 8, 52))
    if windows:
        for wy in range(640 - h + 14, 630, 26):
            for wx in range(x + 10, x + w - 10, 24):
                if rng.random() < 0.45:
                    d.rectangle([wx, wy, wx + 8, wy + 12],
                                fill=(255, 190, 80))

for (x, w, h) in [(0, 90, 150), (95, 70, 210), (170, 110, 130), (285, 60, 180),
                  (700, 80, 190), (785, 110, 140), (900, 70, 220), (975, 49, 160)]:
    building(x, w, h)
# a couple of antennae
d.line([(130, 430), (130, 400)], fill=(28, 8, 52), width=5)
d.line([(935, 420), (935, 392)], fill=(28, 8, 52), width=5)

# --- palm silhouettes -------------------------------------------------------
def palm(x, y, s, flip=False):
    # trunk
    pts = []
    for t in range(0, 21):
        px = x + (t / 20) * 14 * s * (-1 if flip else 1)
        py = y - (t / 20) * 150 * s
        pts.append((px, py))
    d.line(pts, fill=(20, 5, 40), width=int(12 * s))
    tx, ty = pts[-1]
    # fronds: drooping 3-point curves out from the crown
    for ang in [-165, -140, -115, -90, -65, -40, -15]:
        a = math.radians(ang if not flip else 180 - ang)
        mx = tx + math.cos(a) * 55 * s
        my = ty + math.sin(a) * 18 * s
        ex = tx + math.cos(a) * 100 * s
        ey = ty + math.sin(a) * 30 * s + 42 * s
        d.line([(tx, ty), (mx, my), (ex, ey)], fill=(20, 5, 40),
               width=int(9 * s), joint="curve")

# (no palms: the skyline + sun already sell Vice City, and palm
# silhouettes read as clutter at 480 px)

# --- ground: dark beach -----------------------------------------------------
d.rectangle([0, 640, W, H], fill=(24, 10, 46))
for i in range(14):
    y = 680 + i * 24
    d.line([(0, y), (W, y)], fill=(255, 120, 90, 26), width=2)

# --- helpers ----------------------------------------------------------------
def star4(cx, cy, r, fill):
    # four-pointed sparkle
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.22
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

def star5(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

def text_center(y, s, font, fill="white", stroke=7):
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y), s, font=font, fill=fill,
           stroke_width=stroke, stroke_fill=(10, 5, 20))

# --- the alligator ----------------------------------------------------------
# tail (left), body, snout (right) — lounging, facing right toward the ghost
GREEN = (74, 158, 63)
DARK = (46, 110, 42)
BELLY = (150, 214, 120)

# tail: long tapering curve to the left, slightly raised at the tip
d.polygon([(260, 775), (180, 745), (90, 755), (45, 790), (90, 820),
           (180, 825), (260, 825)],
          fill=GREEN)
d.polygon([(260, 775), (180, 745), (90, 755), (45, 790), (90, 820),
           (180, 825), (260, 825)],
          outline=DARK, width=4)
# body: long and low
d.ellipse([190, 700, 640, 875], fill=GREEN, outline=DARK, width=5)
# belly
d.ellipse([240, 800, 590, 868], fill=BELLY)
# back ridges
for x in [270, 330, 390, 450, 510]:
    d.polygon([(x, 712), (x + 22, 712), (x + 11, 682)], fill=DARK)
# legs, tucked under the body
for (x0, y0) in [(250, 850), (350, 858), (470, 858), (560, 850)]:
    d.rounded_rectangle([x0, y0, x0 + 55, y0 + 48], radius=18,
                        fill=GREEN, outline=DARK, width=4)
    for cx in [x0 + 14, x0 + 28, x0 + 42]:
        d.polygon([(cx - 6, y0 + 48), (cx + 6, y0 + 48), (cx, y0 + 60)],
                  fill=(230, 230, 220))
# front leg raised to the case (drawn before the head, so the head covers
# its base and only the raised part shows above the snout)
d.rounded_rectangle([640, 660, 700, 770], radius=16, fill=GREEN,
                    outline=DARK, width=4)
# head / snout
d.rounded_rectangle([560, 720, 810, 815], radius=40, fill=GREEN,
                    outline=DARK, width=5)
# jaw line + smile
d.line([(580, 787), (790, 787)], fill=DARK, width=4)
d.arc([710, 755, 810, 835], start=10, end=110, fill=DARK, width=4)
# teeth
for x in [610, 650, 690, 730]:
    d.polygon([(x, 787), (x + 14, 787), (x + 7, 805)], fill="white")
# nostrils
d.ellipse([772, 733, 786, 745], fill=DARK)
d.ellipse([748, 733, 762, 745], fill=DARK)
# eye bumps + sunglasses
d.ellipse([600, 690, 645, 730], fill=GREEN, outline=DARK, width=4)
d.ellipse([660, 690, 705, 730], fill=GREEN, outline=DARK, width=4)
d.rounded_rectangle([592, 695, 652, 727], radius=12, fill=(12, 12, 16))
d.rounded_rectangle([656, 695, 716, 727], radius=12, fill=(12, 12, 16))
d.line([(652, 711), (656, 711)], fill=(12, 12, 16), width=8)
# shine on the shades
d.line([(606, 723), (626, 699)], fill=(255, 255, 255), width=4)
d.line([(670, 723), (690, 699)], fill=(255, 255, 255), width=4)

# GTA VI game case, held up by the gator's raised front leg
d.rounded_rectangle([640, 560, 745, 690], radius=10, fill="white",
                    outline=(15, 15, 15), width=4)
d.rectangle([640, 560, 745, 588], fill=(255, 90, 40))
f_case = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 40)
d.text((692, 612), "GTA", font=f_case, fill=(15, 15, 15), anchor="mm")
d.text((692, 660), "VI", font=f_case, fill=(255, 90, 40), anchor="mm")

# --- make.fun ghost ---------------------------------------------------------
# floating to the right of the gator, cheering with its magenta star coin
gx, gy = 870, 560  # ghost centre
# body: rounded top, wavy bottom, thick black outline
d.rounded_rectangle([gx - 85, gy - 130, gx + 85, gy + 90], radius=80,
                    fill="white", outline=(10, 10, 10), width=7)
# wavy bottom edge (three scallops)
for i, cx in enumerate([gx - 57, gx, gx + 57]):
    d.ellipse([cx - 30, gy + 55, cx + 30, gy + 115], fill="white",
              outline=(10, 10, 10), width=6)
d.rectangle([gx - 85, gy + 55, gx + 85, gy + 92], fill="white")
d.line([(gx - 85, gy + 55), (gx - 85, gy + 92)], fill=(10, 10, 10), width=7)
d.line([(gx + 85, gy + 55), (gx + 85, gy + 92)], fill=(10, 10, 10), width=7)
# sparkle eyes
star4(gx - 34, gy - 45, 26, (10, 10, 10))
star4(gx + 34, gy - 45, 26, (10, 10, 10))
# happy open smile
d.arc([gx - 26, gy - 5, gx + 26, gy + 45], start=15, end=165,
      fill=(10, 10, 10), width=6)
# raised waving hand (round little hand)
d.ellipse([gx - 118, gy - 95, gx - 82, gy - 59], fill="white",
          outline=(10, 10, 10), width=6)
# arm to the coin
d.line([(gx + 80, gy + 10), (gx + 112, gy - 50)], fill=(10, 10, 10), width=7)
# magenta coin with white star, held up
d.ellipse([gx + 88, gy - 108, gx + 148, gy - 48], fill=(230, 0, 160),
          outline=(10, 10, 10), width=6)
star5(gx + 118, gy - 78, 24, "white")

# --- captions ---------------------------------------------------------------
f_top = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 66)
f_bot = ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", 52)
text_center(36, "13 YEARS OF WAITING", f_top)
text_center(948, "WORTH IT. MY BOSS DISAGREES.", f_bot)

img.save(OUT)
print("saved", OUT, img.size)
