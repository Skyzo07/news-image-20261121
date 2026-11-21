# render.py — draws entry.png for news-image-20261121 from scratch.
# Pure Python stdlib (zlib/struct). No network, deterministic output.
# A 5x7 bitmap font defined here in code; all pictograms drawn with
# rectangles, lines, circles and polygons. Run: python3 render.py
# Writes entry.png (1024x1024) next to this file.
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font
# Each glyph: 7 rows of 5 bits, "1" = filled pixel.
FONT = {
"A": ["01110","10001","10001","11111","10001","10001","10001"],
"B": ["11110","10001","10001","11110","10001","10001","11110"],
"C": ["01110","10001","10000","10000","10000","10001","01110"],
"D": ["11110","10001","10001","10001","10001","10001","11110"],
"E": ["11111","10000","10000","11110","10000","10000","11111"],
"F": ["11111","10000","10000","11110","10000","10000","10000"],
"G": ["01110","10001","10000","10111","10001","10001","01111"],
"H": ["10001","10001","10001","11111","10001","10001","10001"],
"I": ["01110","00100","00100","00100","00100","00100","01110"],
"J": ["00111","00010","00010","00010","00010","10010","01100"],
"K": ["10001","10010","10100","11000","10100","10010","10001"],
"L": ["10000","10000","10000","10000","10000","10000","11111"],
"M": ["10001","11011","10101","10101","10001","10001","10001"],
"N": ["10001","11001","10101","10011","10001","10001","10001"],
"O": ["01110","10001","10001","10001","10001","10001","01110"],
"P": ["11110","10001","10001","11110","10000","10000","10000"],
"Q": ["01110","10001","10001","10001","10101","10010","01101"],
"R": ["11110","10001","10001","11110","10100","10010","10001"],
"S": ["01111","10000","10000","01110","00001","00001","11110"],
"T": ["11111","00100","00100","00100","00100","00100","00100"],
"U": ["10001","10001","10001","10001","10001","10001","01110"],
"V": ["10001","10001","10001","10001","10001","01010","00100"],
"W": ["10001","10001","10001","10101","10101","11011","10001"],
"X": ["10001","10001","01010","00100","01010","10001","10001"],
"Y": ["10001","10001","01010","00100","00100","00100","00100"],
"Z": ["11111","00001","00010","00100","01000","10000","11111"],
"0": ["01110","10001","10011","10101","11001","10001","01110"],
"1": ["00100","01100","00100","00100","00100","00100","01110"],
"2": ["01110","10001","00001","00010","00100","01000","11111"],
"3": ["11111","00010","00100","00010","00001","10001","01110"],
"4": ["00010","00110","01010","10010","11111","00010","00010"],
"5": ["11111","10000","11110","00001","00001","10001","01110"],
"6": ["00110","01000","10000","11110","10001","10001","01110"],
"7": ["11111","00001","00010","00100","01000","01000","01000"],
"8": ["01110","10001","10001","01110","10001","10001","01110"],
"9": ["01110","10001","10001","01111","00001","00010","01100"],
"a": ["00000","00000","01110","00001","01111","10001","01111"],
"b": ["10000","10000","11110","10001","10001","10001","11110"],
"c": ["00000","00000","01110","10001","10000","10001","01110"],
"d": ["00001","00001","01111","10001","10001","10001","01111"],
"e": ["00000","00000","01110","10001","11111","10000","01110"],
"f": ["00110","01001","01000","11110","01000","01000","01000"],
"g": ["00000","01111","10001","10001","01111","00001","01110"],
"h": ["10000","10000","11110","10001","10001","10001","10001"],
"i": ["00100","00000","01100","00100","00100","00100","01110"],
"j": ["00010","00000","00110","00010","00010","10010","01100"],
"k": ["10000","10000","10010","10100","11000","10100","10010"],
"l": ["01100","00100","00100","00100","00100","00100","01110"],
"m": ["00000","00000","11010","10101","10101","10101","10101"],
"n": ["00000","00000","11110","10001","10001","10001","10001"],
"o": ["00000","00000","01110","10001","10001","10001","01110"],
"p": ["00000","11110","10001","10001","11110","10000","10000"],
"q": ["00000","00000","01111","10001","10001","01111","00001"],
"r": ["00000","00000","10110","11001","10000","10000","10000"],
"s": ["00000","00000","01111","10000","01110","00001","11110"],
"t": ["01000","01000","11100","01000","01000","01000","00110"],
"u": ["00000","00000","10001","10001","10001","10011","01101"],
"v": ["00000","00000","10001","10001","10001","01010","00100"],
"w": ["00000","00000","10001","10101","10101","10101","01010"],
"x": ["00000","00000","10001","01010","00100","01010","10001"],
"y": ["00000","00000","10001","10001","01111","00001","01110"],
"z": ["00000","00000","11111","00010","00100","01000","11111"],
" ": ["00000","00000","00000","00000","00000","00000","00000"],
".": ["00000","00000","00000","00000","00000","01100","01100"],
",": ["00000","00000","00000","00000","01100","00100","01000"],
":": ["00000","01100","01100","00000","01100","01100","00000"],
";": ["00000","01100","01100","00000","01100","00100","01000"],
"'": ["00100","00100","01000","00000","00000","00000","00000"],
"-": ["00000","00000","00000","01110","00000","00000","00000"],
"!": ["00100","00100","00100","00100","00100","00000","00100"],
"?": ["01110","10001","00001","00010","00100","00000","00100"],
"%": ["11001","11010","00010","00100","01000","01011","10011"],
"(": ["00010","00100","01000","01000","01000","00100","00010"],
")": ["01000","00100","00010","00010","00010","00100","01000"],
"/": ["00001","00010","00010","00100","01000","01000","10000"],
"$": ["00100","01111","10100","01110","00101","11110","00100"],
"&": ["01100","10010","10100","01000","10101","10010","01101"],
"+": ["00000","00100","00100","11111","00100","00100","00000"],
"=": ["00000","00000","11111","00000","11111","00000","00000"],
'"': ["01010","01010","00000","00000","00000","00000","00000"],
"*": ["00000","10101","01110","11111","01110","10101","00000"],
">": ["10000","01000","00100","00010","00100","01000","10000"],
"<": ["00001","00010","00100","01000","00100","00010","00001"],
"#": ["01010","01010","11111","01010","11111","01010","01010"],
"~": ["00000","00000","01001","10110","00000","00000","00000"],
"@": ["01110","10001","10111","10101","10110","10000","01110"],
}

# ---------------------------------------------------------------- canvas
class Img:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i+3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            row = bytes(c) * (x1 - x0)
            self.px[base:base + (x1 - x0) * 3] = row

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=False):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.set(xx, yy, c)
                else:
                    if r * r - 2 * r <= d <= r * r:
                        self.set(xx, yy, c)

    def poly(self, pts, c):
        # scanline fill of a simple polygon
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                    self.set(x, y, c)

    def text(self, x, y, s, c, txt):
        cx = x
        for ch in txt:
            g = FONT.get(ch, FONT["?"])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == "1":
                        self.rect(cx + col * s, y + r * s, s, s, c)
            cx += 6 * s
        return cx

    def text_w(self, s, txt):
        return len(txt) * 6 * s - s

    def text_c(self, cx, y, s, c, txt):
        self.text(cx - self.text_w(s, txt) // 2, y, s, c, txt)

    def wrap(self, s, txt, maxw):
        words = txt.split(" ")
        lines, cur = [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if self.text_w(s, trial) <= maxw:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def save_png(img, path):
    raw = b"".join(b"\x00" + bytes(img.px[y * img.w * 3:(y + 1) * img.w * 3])
                   for y in range(img.h))

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", img.w, img.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (26, 26, 46)
NAVY = (20, 33, 61)
NAVY2 = (30, 48, 90)
RED = (178, 34, 34)
DRED = (139, 0, 0)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
LIGHT = (226, 232, 240)
GREY = (90, 90, 100)
GREEN = (34, 139, 60)
TEAL = (14, 116, 116)
ORANGE = (214, 110, 20)
SKY = (70, 130, 180)

# ---------------------------------------------------------------- pictograms
def draw_missile_scene(im, x, y, w, h):
    """Night sky over a border: two missile streaks, burst, ground line."""
    im.rect(x, y, w, h, NAVY)
    # stars
    for sx, sy in [(18, 22), (70, 12), (130, 30), (190, 14), (250, 26),
                   (40, 60), (110, 52), (210, 58), (285, 44), (160, 16)]:
        im.rect(x + sx, y + sy, 3, 3, WHITE)
    # moon
    im.circle(x + 250, y + 78, 16, (240, 230, 190), fill=True)
    im.circle(x + 244, y + 72, 14, NAVY, fill=True)
    # ground + border line
    gy = y + h - 46
    im.rect(x, gy, w, 46, (18, 28, 54))
    im.line(x, gy, x + w, gy, GOLD, 3)
    im.text(x + 14, gy + 14, 2, GOLD, "POLAND")
    im.text(x + w - 118, gy + 14, 2, WHITE, "UKRAINE")
    # NATO compass star (4-point)
    cx, cy = x + w - 66, y + 66
    im.poly([(cx, cy - 26), (cx + 7, cy - 7), (cx + 26, cy), (cx + 7, cy + 7),
             (cx, cy + 26), (cx - 7, cy + 7), (cx - 26, cy), (cx - 7, cy - 7)],
            (150, 180, 220))
    im.circle(cx, cy, 6, WHITE, fill=True)
    # missile 1: streak + body + flame
    im.line(x + 30, y + 150, x + 150, y + 96, (255, 200, 90), 3)
    im.line(x + 150, y + 96, x + 196, y + 76, WHITE, 4)
    im.poly([(x + 196, y + 76), (x + 214, y + 70), (x + 214, y + 82)], (255, 120, 40))
    im.poly([(x + 30, y + 150), (x + 18, y + 158), (x + 26, y + 162)], (255, 160, 40))
    # missile 2
    im.line(x + 60, y + 210, x + 170, y + 160, (255, 200, 90), 3)
    im.line(x + 170, y + 160, x + 210, y + 142, WHITE, 4)
    im.poly([(x + 210, y + 142), (x + 226, y + 136), (x + 226, y + 148)], (255, 120, 40))
    # impact burst
    bx, by = x + 120, gy - 6
    im.poly([(bx, by - 34), (bx + 10, by - 10), (bx + 34, by - 14), (bx + 14, by),
             (bx + 30, by + 16), (bx + 4, by + 10), (bx, by + 30), (bx - 8, by + 10),
             (bx - 30, by + 14), (bx - 12, by), (bx - 32, by - 16), (bx - 8, by - 12)],
            (255, 170, 50))
    im.circle(bx, by, 10, (255, 220, 120), fill=True)


def draw_scales(im, x, y, w, h):
    """Scales of justice."""
    cx, cy = x + w // 2, y + 12
    im.rect(cx - 3, cy, 6, h - 26, GOLD)
    im.rect(cx - 62, cy, 124, 6, GOLD)
    im.circle(cx, cy - 6, 6, GOLD, fill=True)
    for sgn in (-1, 1):
        px = cx + sgn * 56
        im.line(px, cy + 6, px - 18, cy + 30, GOLD, 2)
        im.line(px, cy + 6, px + 18, cy + 30, GOLD, 2)
        im.poly([(px - 22, cy + 30), (px + 22, cy + 30), (px, cy + 48)], (120, 90, 20))
        im.rect(px - 22, cy + 28, 44, 5, GOLD)
    im.rect(cx - 34, y + h - 10, 68, 6, GOLD)


def draw_chart(im, x, y, w, h):
    """Red falling market chart with bars."""
    bx, by, bw, bh = x + 12, y + 6, w - 24, h - 12
    vals = [0.86, 0.78, 0.82, 0.66, 0.58, 0.44, 0.30]
    bw2 = bw // len(vals)
    for i, v in enumerate(vals):
        bh2 = int(bh * v)
        im.rect(bx + i * bw2 + 4, by + bh - bh2, bw2 - 8, bh2, (200, 60, 60))
    fx = [0.03, 0.20, 0.37, 0.54, 0.71, 0.92]
    fy = [0.12, 0.38, 0.30, 0.62, 0.78, 0.98]
    pts = [(bx + int(f * bw), by + int(g * bh)) for f, g in zip(fx, fy)]
    for a, b in zip(pts, pts[1:]):
        im.line(a[0], a[1], b[0], b[1], DRED, 4)
    im.poly([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 16, pts[-1][1] - 2),
             (pts[-1][0] - 2, pts[-1][1] - 16)], DRED)


def draw_cop(im, x, y, w, h):
    """Globe + clock: climate talks in overtime, no deal yet."""
    cx, cy = x + 58, y + h // 2
    im.circle(cx, cy, 30, SKY, fill=True)
    im.circle(cx, cy, 30, NAVY, fill=False)
    im.line(cx - 30, cy, cx + 30, cy, NAVY, 2)
    im.line(cx, cy - 30, cx, cy + 30, NAVY, 2)
    im.circle(cx, cy, 18, NAVY, fill=False)
    kx, ky = x + w - 58, cy
    im.circle(kx, ky, 28, WHITE, fill=True)
    im.circle(kx, ky, 28, INK, fill=False)
    im.line(kx, ky, kx, ky - 18, INK, 3)
    im.line(kx, ky, kx + 14, ky + 6, INK, 3)
    im.circle(kx, ky, 3, RED, fill=True)


def draw_quake(im, x, y, w, h):
    """Seismograph trace over mountains."""
    my = y + h - 8
    im.poly([(x + 8, my), (x + 60, y + 22), (x + 112, my), (x + 160, y + 36),
             (x + 210, my), (x + 258, y + 16), (x + 306, my)], (120, 140, 160))
    pts = []
    px = x + 10
    base = y + 48
    seq = [0, -3, 2, -2, 2, -22, 18, -10, 6, -3, 2, 0, -4, 3, -2, 0]
    for d in seq:
        pts.append((px, base + d))
        px += 18
    for a, b in zip(pts, pts[1:]):
        im.line(a[0], a[1], b[0], b[1], RED, 3)
    im.text(x + w - 108, y + h - 24, 3, DRED, "M 6.8")


def draw_pill(im, x, y, w, h):
    """Capsule + small rising bars (hopeful trial)."""
    cx, cy = x + 30, y + h // 2
    # capsule, horizontal: red left half, white right half, dark outline
    im.rect(cx + 14, cy - 15, 90, 30, RED)
    im.rect(cx + 104, cy - 15, 90, 30, WHITE)
    im.circle(cx + 14, cy, 15, RED, fill=True)
    im.circle(cx + 194, cy, 15, WHITE, fill=True)
    im.circle(cx + 14, cy, 15, INK, fill=False)
    im.circle(cx + 194, cy, 15, INK, fill=False)
    im.line(cx + 14, cy - 15, cx + 194, cy - 15, INK, 2)
    im.line(cx + 14, cy + 15, cx + 194, cy + 15, INK, 2)
    im.line(cx + 104, cy - 15, cx + 104, cy + 15, INK, 2)
    # small green bars bottom right
    for i, v in enumerate([10, 18, 30]):
        im.rect(x + w - 66 + i * 18, y + h - 12 - v, 12, v, GREEN)


# ---------------------------------------------------------------- panels
def tag(im, x, y, label, bg):
    w = im.text_w(2, label) + 16
    im.rect(x, y, w, 24, bg)
    im.text(x + 8, y + 5, 2, WHITE, label)
    return w


def story_panel(im, x, y, w, h, tag_label, tag_bg, pict, headline, label,
                accent):
    im.rect(x, y, w, h, WHITE)
    im.rect(x, y, w, 4, accent)
    # outline border
    im.rect(x, y, w, 2, INK)
    im.rect(x, y + h - 2, w, 2, INK)
    im.rect(x, y, 2, h, INK)
    im.rect(x + w - 2, y, 2, h, INK)
    tag(im, x + 10, y + 12, tag_label, tag_bg)
    py = y + 42
    ph = 76
    pict(im, x + 8, py, w - 16, ph)
    ty = py + ph + 6
    for ln in im.wrap(3, headline, w - 20):
        im.text(x + 10, ty, 3, INK, ln)
        ty += 24
    ty += 4
    for ln in im.wrap(2, label, w - 20):
        im.text(x + 10, ty, 2, GREY, ln)
        ty += 17


def main():
    im = Img(W, H, PAPER)
    # outer border
    im.rect(0, 0, W, 8, INK)
    im.rect(0, H - 8, W, 8, INK)
    im.rect(0, 0, 8, H, INK)
    im.rect(W - 8, 0, 8, H, INK)

    # ---------------- masthead
    im.text_c(W // 2, 26, 7, NAVY, "THE WORLD IN ONE DAY")
    im.rect(40, 92, 944, 3, NAVY)
    im.text_c(W // 2, 104, 4, RED, "SATURDAY 21 NOVEMBER 2026")
    im.text_c(W // 2, 136, 2, GREY, "SIX STORIES THAT DEFINED THE DAY")

    # ---------------- lead panel: Poland / NATO
    lx, ly, lw, lh = 24, 158, 976, 312
    im.rect(lx, ly, lw, lh, NAVY)
    im.rect(lx, ly, lw, 4, RED)
    tag(im, lx + 16, ly + 16, "LEAD  -  CONFLICT, EUROPE", RED)
    im.text(lx + 16, ly + 52, 5, WHITE, "MISSILES LAND")
    im.text(lx + 16, ly + 90, 5, WHITE, "IN POLAND")
    im.text(lx + 16, ly + 134, 3, (255, 220, 120), "TWO RUSSIAN MISSILES")
    im.text(lx + 16, ly + 160, 3, (255, 220, 120), "AND A DRONE COME DOWN")
    im.text(lx + 16, ly + 186, 3, (255, 220, 120), "DURING ALLIED DRILLS")
    for i, ln in enumerate([
            "NATO calls it a grave violation of Polish",
            "airspace. PM Tusk: a deliberate provocation.",
            "No injuries reported in Poland."]):
        im.text(lx + 16, ly + 218 + i * 24, 2, LIGHT, ln)
    draw_missile_scene(im, lx + 560, ly + 48, 400, 252)

    # ---------------- grid of five
    gy = 486
    # row 1: three panels
    pw, ph, gap = 318, 216, 11
    x0 = 24
    story_panel(im, x0, gy, pw, ph, "JUSTICE", NAVY2, draw_scales,
                "MYANMAR GUILTY OF GENOCIDE",
                "First-ever genocide verdict, 9-6. Final.", NAVY2)
    story_panel(im, x0 + pw + gap, gy, pw, ph, "MARKETS", DRED, draw_chart,
                "WALL ST PLUNGES INTO CORRECTION",
                "S&P -3.7%, Nasdaq -5.3%, Nvidia -14%.", DRED)
    story_panel(im, x0 + 2 * (pw + gap), gy, pw, ph, "CLIMATE", TEAL, draw_cop,
                "CLIMATE TALKS IN OVERTIME",
                "Draft omits fossil fuels. No deal yet.", TEAL)
    # row 2: two wider panels
    gy2 = gy + ph + 12
    pw2 = 482
    story_panel(im, x0, gy2, pw2, ph, "DISASTER  -  PERU", ORANGE, draw_quake,
                "MAGNITUDE 6.8 QUAKE HITS PERU",
                "Junin tremor felt 320 km away in Lima. No casualties.", ORANGE)
    story_panel(im, x0 + pw2 + 12, gy2, pw2, ph, "HEALTH  -  HOPE", GREEN, draw_pill,
                "CANCER PILL: TUMOURS VANISH",
                "Early trial: tumours gone in 1 in 12. Not a cure.", GREEN)

    # ---------------- bottom strip
    by = 938
    im.rect(24, by, 976, 78, NAVY)
    im.text_c(W // 2, by + 10, 4, WHITE, "SATURDAY 21 NOVEMBER 2026")
    im.text_c(W // 2, by + 46, 2, LIGHT,
              "SOURCES: AP  -  REUTERS  -  HUMAN RIGHTS WATCH  -  BBC  -  NATURE")

    n = save_png(im, "entry.png")
    print("wrote entry.png", n, "bytes")


if __name__ == "__main__":
    main()
