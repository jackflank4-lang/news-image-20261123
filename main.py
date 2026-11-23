#!/usr/bin/env python3
"""Sum up Monday 23 November 2026's world news in one image.

Draws a newspaper-style poster (1024x1024 PNG) with Python stdlib only:
a 5x5 bitmap font written from scratch and a hand-rolled PNG encoder.
Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
"""
import os
import struct
import zlib

W, H = 1024, 1024

# --- 5x5 bitmap font: each glyph is 5 rows of 5 bits (MSB = left pixel) ---
FONT = {
    'A': (0b01110, 0b10001, 0b11111, 0b10001, 0b10001),
    'B': (0b11110, 0b10001, 0b11110, 0b10001, 0b11110),
    'C': (0b01110, 0b10001, 0b10000, 0b10001, 0b01110),
    'D': (0b11110, 0b10001, 0b10001, 0b10001, 0b11110),
    'E': (0b11111, 0b10000, 0b11110, 0b10000, 0b11111),
    'F': (0b11111, 0b10000, 0b11110, 0b10000, 0b10000),
    'G': (0b01110, 0b10001, 0b10000, 0b10111, 0b01111),
    'H': (0b10001, 0b10001, 0b11111, 0b10001, 0b10001),
    'I': (0b01110, 0b00100, 0b00100, 0b00100, 0b01110),
    'J': (0b00111, 0b00010, 0b00010, 0b10010, 0b01100),
    'K': (0b10001, 0b10010, 0b11100, 0b10010, 0b10001),
    'L': (0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    'M': (0b10001, 0b11011, 0b10101, 0b10001, 0b10001),
    'N': (0b10001, 0b11001, 0b10101, 0b10011, 0b10001),
    'O': (0b01110, 0b10001, 0b10001, 0b10001, 0b01110),
    'P': (0b11110, 0b10001, 0b11110, 0b10000, 0b10000),
    'Q': (0b01110, 0b10001, 0b10001, 0b10101, 0b01111),
    'R': (0b11110, 0b10001, 0b11110, 0b10010, 0b10001),
    'S': (0b01111, 0b10000, 0b01110, 0b00001, 0b11110),
    'T': (0b11111, 0b00100, 0b00100, 0b00100, 0b00100),
    'U': (0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    'V': (0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    'W': (0b10001, 0b10001, 0b10101, 0b11011, 0b10001),
    'X': (0b10001, 0b01010, 0b00100, 0b01010, 0b10001),
    'Y': (0b10001, 0b01010, 0b00100, 0b00100, 0b00100),
    'Z': (0b11111, 0b00010, 0b00100, 0b01000, 0b11111),
    '0': (0b01110, 0b10001, 0b10011, 0b10101, 0b01110),
    '1': (0b00100, 0b01100, 0b00100, 0b00100, 0b01110),
    '2': (0b01110, 0b10001, 0b00010, 0b00100, 0b11111),
    '3': (0b11110, 0b00001, 0b01110, 0b00001, 0b11110),
    '4': (0b00010, 0b00110, 0b01010, 0b11111, 0b00010),
    '5': (0b11111, 0b10000, 0b11110, 0b00001, 0b11110),
    '6': (0b01110, 0b10000, 0b11110, 0b10001, 0b01110),
    '7': (0b11111, 0b00010, 0b00100, 0b01000, 0b01000),
    '8': (0b01110, 0b10001, 0b01110, 0b10001, 0b01110),
    '9': (0b01110, 0b10001, 0b01111, 0b00001, 0b01110),
    ' ': (0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0b00100),
    ',': (0, 0, 0, 0b00100, 0b01000),
    ':': (0, 0b00100, 0, 0b00100, 0),
    ';': (0, 0b00100, 0, 0b00100, 0b01000),
    '!': (0b00100, 0b00100, 0b00100, 0, 0b00100),
    '?': (0b01110, 0b10001, 0b00010, 0, 0b00100),
    "'": (0b00100, 0b00100, 0, 0, 0),
    '-': (0, 0, 0b01110, 0, 0),
    '/': (0b00001, 0b00010, 0b00100, 0b01000, 0b10000),
    '(': (0b00010, 0b00100, 0b00100, 0b00100, 0b00010),
    ')': (0b01000, 0b00100, 0b00100, 0b00100, 0b01000),
    '%': (0b10001, 0b00010, 0b00100, 0b01000, 0b10001),
    '+': (0, 0b00100, 0b01110, 0b00100, 0),
    '&': (0b01100, 0b10010, 0b10100, 0b01001, 0b01101),
    '$': (0b00100, 0b01111, 0b10100, 0b01110, 0b00100),
    '"': (0b01010, 0b01010, 0, 0, 0),
    '=': (0, 0b01110, 0, 0b01110, 0),
    '*': (0, 0b10101, 0b01110, 0b10101, 0),
}

# --- canvas: flat bytearray, RGB ---
def new_canvas(w, h, rgb):
    buf = bytearray(w * h * 3)
    r, g, b = rgb
    buf[0::3] = bytes([r]) * (w * h)
    buf[1::3] = bytes([g]) * (w * h)
    buf[2::3] = bytes([b]) * (w * h)
    return buf


def fill_rect(buf, w, x, y, rw, rh, rgb):
    r, g, b = rgb
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(w, x + rw), min(H, y + rh)
    for yy in range(y0, y1):
        base = (yy * w + x0) * 3
        n = x1 - x0
        buf[base:base + n * 3:3] = bytes([r]) * n
        buf[base + 1:base + 1 + n * 3:3] = bytes([g]) * n
        buf[base + 2:base + 2 + n * 3:3] = bytes([b]) * n


def fill_circle(buf, w, cx, cy, rad, rgb):
    for dy in range(-rad, rad + 1):
        dx = int((rad * rad - dy * dy) ** 0.5)
        fill_rect(buf, w, cx - dx, cy + dy, dx * 2 + 1, 1, rgb)


def draw_line(buf, w, x0, y0, x1, y1, rgb, thick=1):
    """Simple Bresenham line with square thickness."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        fill_rect(buf, w, x - thick // 2, y - thick // 2, thick, thick, rgb)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def _png_chunk(ctype, data):
    chunk = struct.pack('>I', len(data)) + ctype + data
    chunk += struct.pack('>I', zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return chunk


def write_png(path, buf, w, h):
    raw = bytearray()
    stride = w * 3
    for yy in range(h):
        raw.append(0)
        raw += buf[yy * stride:(yy + 1) * stride]
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    data = b'\x89PNG\r\n\x1a\n'
    data += _png_chunk(b'IHDR', ihdr)
    data += _png_chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    data += _png_chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(data)
    return len(data)

# --- text: draw one glyph, one string, wrapped paragraphs ---
def char_w(scale):
    return 5 * scale + scale  # 5 px glyph + 1 px gap, scaled


def text_w(text, scale):
    return len(text) * char_w(scale) - scale


def draw_glyph(buf, w, x, y, ch, scale, rgb):
    glyph = FONT.get(ch.upper(), FONT[' '])
    for row in range(5):
        bits = glyph[row]
        for col in range(5):
            if bits & (1 << (4 - col)):
                fill_rect(buf, w, x + col * scale, y + row * scale,
                          scale, scale, rgb)


def draw_text(buf, w, x, y, text, scale, rgb):
    cx = x
    for ch in text:
        draw_glyph(buf, w, cx, y, ch, scale, rgb)
        cx += char_w(scale)
    return cx


def draw_text_centered(buf, w, x, y, width, text, scale, rgb):
    tw = text_w(text, scale)
    draw_text(buf, w, x + max(0, (width - tw) // 2), y, text, scale, rgb)


def wrap_text(text, scale, max_w):
    """Greedy word wrap; returns list of lines (upper-cased by caller)."""
    words = text.split(' ')
    lines, cur = [], ''
    cw = char_w(scale)
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if len(trial) * cw - scale <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # a single over-long word: hard-split it
            while len(word) * cw - scale > max_w:
                take = max_w // cw
                lines.append(word[:take])
                word = word[take:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(buf, w, x, y, text, scale, rgb, max_w, line_h, max_lines=None):
    lines = wrap_text(text, scale, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw_text(buf, w, x, y + i * line_h, line, scale, rgb)
    return len(lines)

# --- pictogram icons (56x56 box at x, y), drawn from rectangles/circles ---
def icon_ship(buf, w, x, y, c):
    # mast + flag, clearly separated from the hull
    fill_rect(buf, w, x + 26, y + 4, 3, 22, c)
    fill_rect(buf, w, x + 29, y + 4, 13, 6, c)
    # superstructure
    fill_rect(buf, w, x + 18, y + 24, 20, 7, c)
    # hull: long deck, tapered bow to the right
    fill_rect(buf, w, x + 4, y + 31, 42, 7, c)
    fill_rect(buf, w, x + 8, y + 38, 34, 5, c)
    draw_line(buf, w, x + 46, y + 31, x + 52, y + 38, c, 2)
    # waves
    draw_line(buf, w, x + 4, y + 50, x + 16, y + 50, c, 2)
    draw_line(buf, w, x + 22, y + 50, x + 34, y + 50, c, 2)
    draw_line(buf, w, x + 40, y + 50, x + 52, y + 50, c, 2)


def icon_chart(buf, w, x, y, c):
    # axes
    fill_rect(buf, w, x + 8, y + 8, 3, 40, c)
    fill_rect(buf, w, x + 8, y + 45, 40, 3, c)
    # rising line with arrowhead
    draw_line(buf, w, x + 12, y + 40, x + 24, y + 30, c, 3)
    draw_line(buf, w, x + 24, y + 30, x + 36, y + 34, c, 3)
    draw_line(buf, w, x + 36, y + 34, x + 48, y + 14, c, 3)
    draw_line(buf, w, x + 48, y + 14, x + 40, y + 14, c, 3)
    draw_line(buf, w, x + 48, y + 14, x + 48, y + 22, c, 3)


def icon_globe(buf, w, x, y, c):
    cx, cy, r = x + 28, y + 28, 20
    # disc
    fill_circle(buf, w, cx, cy, r, c)
    # land hint: light cross bands cut out (bg colour circles/rects)
    bg = (255, 255, 255)
    fill_rect(buf, w, cx - 14, cy - 4, 28, 3, bg)
    fill_rect(buf, w, cx - 3, cy - 14, 3, 28, bg)
    fill_circle(buf, w, cx - 12, cy - 10, 5, bg)
    fill_circle(buf, w, cx + 12, cy + 10, 5, bg)


def icon_cuffs(buf, w, x, y, c):
    # two rings joined by a bar
    for cx in (x + 15, x + 41):
        fill_circle(buf, w, cx, y + 30, 12, c)
        fill_circle(buf, w, cx, y + 30, 6, (255, 255, 255))
    fill_rect(buf, w, x + 15, y + 24, 26, 5, c)
    fill_rect(buf, w, x + 13, y + 12, 4, 10, c)
    fill_rect(buf, w, x + 39, y + 12, 4, 10, c)


def icon_flags(buf, w, x, y, c):
    # two upright poles, pennants flying outward
    fill_rect(buf, w, x + 14, y + 8, 3, 42, c)
    fill_rect(buf, w, x + 39, y + 8, 3, 42, c)
    fill_rect(buf, w, x + 3, y + 8, 11, 8, c)
    fill_rect(buf, w, x + 42, y + 8, 11, 8, c)
    # ground line
    fill_rect(buf, w, x + 10, y + 50, 36, 4, c)


def icon_flame(buf, w, x, y, c):
    # flame: stacked shrinking rects forming a teardrop
    fill_rect(buf, w, x + 24, y + 6, 8, 10, c)
    fill_rect(buf, w, x + 20, y + 14, 16, 10, c)
    fill_rect(buf, w, x + 16, y + 22, 24, 10, c)
    fill_rect(buf, w, x + 14, y + 30, 28, 10, c)
    fill_rect(buf, w, x + 18, y + 38, 20, 8, c)
    # base
    fill_rect(buf, w, x + 10, y + 48, 36, 4, c)

# --- palette ---
NAVY = (11, 37, 69)
GOLD = (212, 175, 55)
PAPER = (244, 241, 234)
CARD = (255, 255, 255)
INK = (20, 24, 30)
GRAY = (90, 96, 104)
BORDER = (200, 204, 210)

# tag, accent, headline, deck, dateline, icon
STORIES = [
    ("WAR", (192, 57, 43), "SEA DRONES SINK RUSSIAN WARSHIP",
     "Zelenskyy: seven drones hit corvette Merkury at Benghazi port",
     "BENGHAZI, LIBYA", icon_ship),
    ("MARKETS", (30, 132, 73), "HUANG BACK AT NVIDIA, SHARES SOAR 33%",
     "S&P jumps 4.8% as AI sell-off eases; Nikkei falls 5%",
     "NEW YORK", icon_chart),
    ("CLIMATE", (17, 122, 101), "COP31 ENDS WITH NO DEAL",
     "Longest climate talks ever close in Antalya without a pact",
     "ANTALYA, TURKIYE", icon_globe),
    ("JUSTICE", (40, 73, 125), "FBI MOST-WANTED 'CHAPO ISIDRO' CAPTURED",
     "Mexican forces seize cartel boss in Sinaloa with US help",
     "SINALOA, MEXICO", icon_cuffs),
    ("DIPLOMACY", (108, 74, 158), "ZELENSKYY WANTS FOUR-WAY TALKS 'TOMORROW'",
     "Ukraine, Europe, US and Russia urged to meet before Christmas",
     "BERLIN", icon_flags),
    ("MIDEAST", (202, 111, 30), "IRAN VOWS TO FIGHT US BLOCKADE",
     "Tehran says it downed a US drone; blasts reported in Hormuz",
     "STRAIT OF HORMUZ", icon_flame),
]


def draw_card(buf, x, y, w, h, story):
    tag, accent, headline, deck, dateline, icon = story
    fill_rect(buf, W, x, y, w, h, CARD)
    # border
    fill_rect(buf, W, x, y, w, 1, BORDER)
    fill_rect(buf, W, x, y + h - 1, w, 1, BORDER)
    fill_rect(buf, W, x, y, 1, h, BORDER)
    fill_rect(buf, W, x + w - 1, y, 1, h, BORDER)
    # accent strip
    fill_rect(buf, W, x, y, w, 8, accent)
    # tag
    draw_text(buf, W, x + 20, y + 22, tag, 2, accent)
    # headline (up to 3 lines)
    n = draw_para(buf, W, x + 20, y + 52, headline, 3, INK, w - 40, 26,
                  max_lines=3)
    # deck
    draw_para(buf, W, x + 20, y + 52 + n * 26 + 10, deck, 2, GRAY,
              w - 40, 18, max_lines=2)
    # dateline
    draw_text(buf, W, x + 20, y + h - 38, dateline, 2, accent)
    # icon bottom-right
    icon(buf, W, x + w - 76, y + h - 76, accent)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    buf = new_canvas(W, H, PAPER)
    # header
    fill_rect(buf, W, 0, 0, W, 150, NAVY)
    fill_rect(buf, W, 0, 150, W, 4, GOLD)
    draw_text_centered(buf, W, 0, 28, W, "23 NOVEMBER 2026", 5,
                       (255, 255, 255))
    draw_text_centered(buf, W, 0, 94, W, "MONDAY - THE WORLD IN ONE DAY",
                       3, GOLD)
    # grid 2x3
    cw, ch, gap, margin = 480, 252, 16, 24
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(buf, margin + col * (cw + gap),
                  170 + row * (ch + gap), cw, ch, story)
    # footer
    draw_text_centered(buf, W, 0, 978, W,
                       "COMPILED FROM WIRE REPORTS - 23 NOVEMBER 2026",
                       2, GRAY)
    path = os.path.join(out_dir, "entry.png")
    size = write_png(path, buf, W, H)
    print("Wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
