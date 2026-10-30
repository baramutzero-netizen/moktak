"""v2 art: 38 '…소' listeners, 7 venues, performers (novices, metal band, opera, cheer squad,
djembe, samulnori). Every sprite uses the same 1px grid; the scene is 320x200."""
from PIL import Image
import math, random
from art import (P, T, hx, grid, put, COW_BASE, cow_image, COW_TYPES, monk_image, moktak_image,
                 novice_image, mini_moktak, glyph_image, karma_image, halo_image, lotus_image, BAYER, bdf_glyphs)

# extra palette entries
EXTRA = {
 'red':'#d0453a','redS':'#8f2a2a','blue':'#3d6fc4','blueS':'#2a4a8a','navy':'#2b3557','yel':'#f2c53d','yelS':'#c7942a',
 'grn':'#4fa35a','grnS':'#2f6e3c','pur':'#8a4fb8','purS':'#5e3484','org':'#ec8a3a','orgS':'#b85f22',
 'cyan':'#6cc8e0','cyanS':'#3d8fb0','pink':'#f08fb4','pinkS':'#c25f86','tux':'#22202a','tuxL':'#3c3946',
 'shirt':'#f4f1ea','hairB':'#2a2026','hairY':'#e8c25a','hairR':'#b0502e','hairBr':'#6b4426',
 'skin2':'#c98f62','skin2S':'#9c6844','skin3':'#7a4a2e','skin3S':'#5a331f',
 'brass':'#e3b648','brassS':'#a87a24','steel':'#c9ccd6','steelS':'#8b8f9c',
 'night0':'#141024','night1':'#221a3a','night2':'#3a2a5a','stage':'#1a1620','stageL':'#3a3444',
 'velvet':'#8e1f2a','velvetS':'#5e1219','velvetL':'#b8303a','field':'#3f8a3a','fieldS':'#2f6e2e','fieldL':'#58a64a',
 'sav0':'#f6b35c','sav1':'#e88a3c','sav2':'#c25a32','savG':'#d9a84a','savGS':'#b0823a','savGL':'#ecc76a',
 'city0':'#f7c49a','city1':'#e48f8a','city2':'#7a6aa8','bld':'#4a4f6a','bldS':'#363a52','bldL':'#6c7290','win':'#ffd98a',
 'space0':'#05060f','space1':'#0d1030','sea':'#2f6fb8','seaS':'#24508a','land':'#5fa04e','landS':'#3f7a3a','cloud':'#eef4ff',
 'ash':'#9a9aa2','white':'#ffffff','jade':'#6cc0a4','teal':'#3f8f8a','cream':'#fff4d8',
}
for k, v in EXTRA.items(): P[k] = hx(v)

def new(w, h): return Image.new('RGBA', (w, h), T)
def px(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height: im.putpixel((x, y), P[c] if isinstance(c, str) else c)
def rect(im, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1): px(im, x, y, c)
def over(im, rows, cmap, ox=0, oy=0):
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch not in '. ': px(im, ox + x, oy + y, cmap[ch])
def outline(im, col='ink'):
    """1px outline around every opaque pixel (only into transparent pixels)."""
    a = im.copy(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if a.getpixel((x, y))[3] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and a.getpixel((xx, yy))[3] > 0 and a.getpixel((xx, yy)) != P[col]:
                        im.putpixel((x, y), P[col]); break
    return im

# ---------- tiny 3x5 letters for element symbols ----------
F35 = {
 'H':["x.x","x.x","xxx","x.x","x.x"], 'O':["xxx","x.x","x.x","x.x","xxx"], 'C':["xxx","x..","x..","x..","xxx"],
 'N':["x.x","xxx","xxx","xxx","x.x"], 'l':["x","x","x","x","x"], 'S':["xxx","x..","xxx","..x","xxx"],
 'o':["...","xxx","x.x","x.x","xxx"], '8':["xxx","x.x","xxx","x.x","xxx"], 'i':["x",".","x","x","x"],
}
def text35(im, s, x, y, c):
    for ch in s:
        g = F35[ch]
        for yy, r in enumerate(g):
            for xx, v in enumerate(r):
                if v == 'x': px(im, x + xx, y + yy, c)
        x += len(g[0]) + 1

# ================= generic "소" face: ears + eyes + muzzle + horns =================
EYES = [(7, 9), (15, 9)]
def add_face(im, ear='hw', horns='horn', muzzle='muz', muzzleS='muzS', ears=True):
    if horns:
        hc, hs = ({'horn': ('horn', 'hornS'), 'gold': ('gold', 'goldS'), 'stone': ('stone', 'stoneS')})[horns]
        L = ["..o.", ".oho", ".ohHo", "..ohHo", "...ohH"]
        for y, r in enumerate(L):
            for x, ch in enumerate(r):
                if ch == '.': continue
                c = {'o': 'ink', 'h': hc, 'H': hs}[ch]
                for xx in (x, 23 - x):
                    if im.getpixel((xx, y + 1))[3] == 0 or ch != 'o': px(im, xx, y + 1, c)
    if ears:
        E = ["ooo.", "oiii", "oiii", ".ooo"]
        for y, r in enumerate(E):
            for x, ch in enumerate(r):
                if ch == '.': continue
                c = {'o': 'ink', 'i': 'ear'}[ch]
                px(im, x, 7 + y, c); px(im, 23 - x, 7 + y, c)
        px(im, 0, 8, ear); px(im, 23, 8, ear)
    for (x, y) in EYES:
        rect(im, x, y, x + 2, y + 2, 'ink'); px(im, x + 1, y, 'k0')
    if muzzle:
        M = [".mmmmmmmm.", "mmmmmmmmmm", "mmnmmmmnmm", "MmmmmmmmmM", ".MMMMMMMM."]
        for y, r in enumerate(M):
            for x, ch in enumerate(r):
                if ch == '.': continue
                px(im, 7 + x, 13 + y, {'m': muzzle, 'M': muzzleS, 'n': 'ink'}[ch])
        for x in range(7, 17):
            if im.getpixel((x, 18))[3] == 0: px(im, x, 18, 'ink')
        px(im, 6, 14, 'ink'); px(im, 17, 14, 'ink'); px(im, 6, 15, 'ink'); px(im, 17, 15, 'ink')
    return im

def frames_from(base, bodycol):
    """4 frames: idle, blink, left ear up, right ear up."""
    f0 = base.copy()
    f1 = base.copy()
    for (x, y) in EYES:
        rect(f1, x, y, x + 2, y + 1, bodycol); rect(f1, x, y + 1, x + 2, y + 2, 'ink')
    def ear_up(xs):
        f = base.copy()
        for x in xs:
            for y in range(5, 12):
                c = base.getpixel((x, y + 1)) if y < 11 else base.getpixel((x, y))
                f.putpixel((x, y), c)
        return f
    return [f0, f1, ear_up(range(0, 4)), ear_up(range(20, 24))]

# ================= cow-family listeners =================
def cow_variant(b, s, l, horn='horn', hornS='hornS', mods=()):
    rows = list(COW_BASE)
    if 'goat' in mods:
        # short swept-back horns, beard, grey muzzle
        rows[0:6] = ["........................", "........................", "......o..........o......",
                     ".....oho........oho.....", "......ohoooooooooho.....", ".....oobbbbbbbbbbbboo....".ljust(24, '.')[:24]]
    if 'rhino' in mods:
        rows[0:6] = ["........................"] * 4 + ["......oooooooooooo......", ".....obbbbbbbbbbbbbo....."]
    cmap = {'o': 'ink', 'b': b, 's': s, 'S': s, 'l': l, 'h': horn, 'H': hornS, 'i': 'ear', 'e': 'ink', 'w': 'k0',
            'm': 'muz', 'M': 'muzS', 'n': 'ink', 'k': 'hoof', 'x': 'blk', 'f': 'yakL'}
    im = grid(rows, cmap)
    if 'goat' in mods or 'rhino' in mods:
        for y in range(13, 18):
            for x in range(7, 17):
                c = im.getpixel((x, y))
                if c == P['muz']: im.putpixel((x, y), P['ash'] if 'goat' in mods else P[l])
                elif c == P['muzS']: im.putpixel((x, y), P['stoneS'] if 'goat' in mods else P[s])
    if 'goat' in mods:
        for (x, y) in [(10, 18), (11, 18), (12, 18), (13, 18), (11, 19), (12, 19), (11, 20), (12, 20)]: px(im, x, y, 'milkS' if b != 'blk' else 'blkL')
    if 'rhino' in mods:   # big nose horn + small one
        H = ["....o....", "...oho...", "...oho...", "..ohhho..", "..ohhHo..", ".ohhhHHo."]
        over(im, H, {'o': 'ink', 'h': 'horn', 'H': 'hornS'}, 7, 8)
        rect(im, 4, 12, 6, 13, s); rect(im, 18, 12, 20, 13, s)   # skin folds
        for (x, y) in EYES: rect(im, x, y, x + 2, y + 2, 'ink'); px(im, x + 1, y, 'k0')
    if 'brindle' in mods:
        for x in range(2, 22):
            for y in range(6, 23):
                c = im.getpixel((x, y))
                if c in (P[b], P[s]) and (x + y // 2) % 4 == 0: im.putpixel((x, y), P['yakS'])
    if 'ring' in mods:
        for (x, y) in [(11, 17), (12, 17), (10, 18), (13, 18), (11, 19), (12, 19)]: px(im, x, y, 'gold')
    if 'shaggy' in mods:
        for x in range(1, 23):
            y = 18 if x % 3 else 19
            if im.getpixel((x, y)) == P[s]: px(im, x, y, l)
        for x in range(8, 16): px(im, x, 6, l); px(im, x, 7, l if x % 2 else b)
    if 'patch' in mods:
        for (x, y) in [(6,7),(7,7),(6,8),(15,6),(16,6),(16,7),(17,7),(2,15),(3,15),(2,16),(3,16),(4,17),
                       (18,19),(19,19),(20,19),(19,20),(20,20),(9,19),(10,19),(10,20),(14,22),(15,21)]:
            if im.getpixel((x, y)) in (P[b], P[s], P[l]): px(im, x, y, 'blk')
    if 'bighorn' in mods:
        rows2 = ["o......................o", "ho....................oh", "Hho..................ohH", ".oHhoooo..........ooohHo."[:24]]
        for y, r in enumerate(rows2):
            for x, ch in enumerate(r):
                if ch != '.': px(im, x, 2 + y, {'o': 'ink', 'h': horn, 'H': hornS}[ch])
    return im

# ================= building / object listeners =================
def building(wall, wallS, roof, roofS, deco):
    im = new(24, 24)
    rect(im, 4, 7, 20, 23, wall); rect(im, 18, 7, 20, 23, wallS)
    for y in range(3, 7):            # pitched roof
        inset = 6 - y
        rect(im, 3 + inset, y, 21 - inset, y + 1, roof if y < 6 else roofS)
    rect(im, 3, 6, 21, 7, roofS)
    rect(im, 4, 22, 20, 23, wallS)
    deco_draw(im, deco)
    outline(im)
    add_face(im, ear=wall, horns='horn')
    return im

def deco_draw(im, d):
    cx = 12
    if d == 'moon': over(im, [".oo", "o..", "o..", ".oo"], {'o': 'yel'}, 10, 8)
    elif d == 'siren': rect(im, 10, 1, 12, 3, 'red'); rect(im, 12, 1, 14, 3, 'blue')
    elif d == 'cross': rect(im, 11, 0, 13, 4, 'grn'); rect(im, 10, 1, 14, 3, 'grn')
    elif d == 'drop': over(im, ["..o..", ".ooo.", "ooooo", ".ooo."], {'o': 'org'}, 10, 0)
    elif d == 'fire': over(im, ["..o..", ".oyo.", "oyyyo", ".ooo."], {'o': 'red', 'y': 'yel'}, 10, 0)
    elif d == 'antenna': rect(im, 12, 0, 13, 3, 'steelS'); px(im, 11, 0, 'red')
    elif d == 'zzz': over(im, ["zzz", "..z", ".z.", "zzz"], {'z': 'cyan'}, 11, 0)
    elif d == 'bubble': over(im, [".o..o", "o.o..", ".o..o"], {'o': 'cyan'}, 10, 0)
    elif d == 'pole': [px(im, 12, y, ('red', 'shirt', 'blue')[y % 3]) for y in range(0, 4)]
    elif d == 'flask': over(im, [".o.", ".o.", "ooo", "ogo"], {'o': 'shirt', 'g': 'grn'}, 11, 0)
    elif d == 'ticket': over(im, ["yyyyy", "y.y.y", "yyyyy"], {'y': 'yel'}, 10, 0)
    elif d == 'info': over(im, ["bbb", "bwb", "bbb", "bwb"], {'b': 'blue', 'w': 'shirt'}, 11, 0)
    elif d == 'cup': over(im, ["s.s.", "oooo", "ooo.", ".oo."], {'s': 'smoke', 'o': 'shirt'}, 10, 0)

def tower():
    im = new(24, 24)
    for y in range(3, 23):
        half = 6 + int(2 * ((y - 13) / 10) ** 2 * 3) // 3
        rect(im, 12 - half, y, 12 + half, y + 1, 'stone' if y % 5 else 'stoneS')
    over(im, [".ss.s", "s..s.", ".s.s."], {'s': 'cloud'}, 9, 0)
    outline(im); add_face(im, ear='stone', horns='horn')
    return im

def sphere(col, colS, sym, symcol='ink', orbit=True):
    im = new(24, 24)
    cx, cy, r = 12, 13, 9
    for y in range(24):
        for x in range(24):
            d = (x - cx + .5) ** 2 + (y - cy + .5) ** 2
            if d <= r * r: px(im, x, y, colS if (x - cx) + (y - cy) > 7 else col)
    outline(im)
    if orbit:
        for a in range(0, 360, 4):
            x = int(cx + 11.5 * math.cos(math.radians(a))); y = int(cy + 3.5 * math.sin(math.radians(a)) + 4 * math.cos(math.radians(a)) * 0.5)
            if 0 <= x < 24 and im.getpixel((x, y))[3] == 0: px(im, x, y, 'cyan')
        px(im, 21, 11, 'yel'); px(im, 2, 15, 'yel')
    add_face(im, ear=col, horns='horn')
    w = sum(len(F35[c][0]) + 1 for c in sym) - 1
    text35(im, sym, cx - w // 2, 18, symcol)
    return im

def bamboo(dark, mid, light):
    im = new(24, 24)
    rect(im, 6, 2, 18, 23, mid); rect(im, 15, 2, 18, 23, dark); rect(im, 6, 2, 8, 23, light)
    for y in (6, 12, 19): rect(im, 6, y, 18, y + 1, dark)
    for y in (4, 21): px(im, 12, y, 'ink'); px(im, 11, y, 'ink')
    outline(im); add_face(im, ear=mid, horns='horn')
    return im

def doc(paper, icon):
    im = new(24, 24)
    rect(im, 5, 4, 19, 23, paper); rect(im, 17, 4, 19, 23, 'milkS' if paper != 'ash' else 'stoneS')
    for x in range(15, 19): px(im, x, 4, 'k0' if paper == 'cream' else paper)
    rect(im, 15, 4, 16, 6, 'milkS')
    outline(im)
    add_face(im, ear=paper, horns='horn')
    for y in (19, 21): rect(im, 7, y, 17, y + 1, 'ink2')
    if icon == 'seal': rect(im, 15, 18, 19, 22, 'red'); px(im, 16, 19, 'k0'); px(im, 17, 20, 'k0')
    if icon == 'up': over(im, ['..g..', '.ggg.', 'g.g.g', '..g..'], {'g': 'grnS'}, 10, 0)
    if icon == 'up2': over(im, ['..b....b..', '.bbb..bbb.', 'b.b.bb.b.b', '..b....b..'], {'b': 'blueS'}, 7, 0)
    if icon == 'check': over(im, ['.....g', '....gg', 'g..gg.', 'gggg..', '.gg...'], {'g': 'grnS'}, 9, 0)
    if icon == 'x': over(im, ['r...r', '.r.r.', '..r..', '.r.r.', 'r...r'], {'r': 'red'}, 10, 0)
    if icon == 'pen': over(im, ['....o', '...oy', '..oy.', '.oy..', 'kk...'], {'o': 'ink', 'y': 'yel', 'k': 'ink'}, 17, 16)
    if icon == 'swap': over(im, ['.rrr.', 'r...r', 'r..rrr', '....r.'], {'r': 'redS'}, 9, 0)
    return im

def briefcase(c, cs):
    im = new(24, 24)
    rect(im, 9, 4, 15, 6, cs); rect(im, 10, 5, 14, 6, T if False else cs)
    rect(im, 3, 6, 21, 23, c); rect(im, 3, 12, 21, 13, cs); rect(im, 11, 11, 13, 14, 'gold')
    outline(im); add_face(im, ear=c, horns='horn')
    return im

def face(col, colS, eyes, mouth, extra):
    im = new(24, 24)
    for y in range(24):
        for x in range(24):
            if (x - 12) ** 2 + (y - 13) ** 2 <= 81: px(im, x, y, col if x + y < 30 else colS)
    outline(im); add_face(im, ear=col, horns='horn')
    for (x, y) in EYES:
        rect(im, x, y, x + 2, y + 2, col)
        if eyes == 'normal': rect(im, x, y, x + 2, y + 2, 'ink'); px(im, x + 1, y, 'k0')
        elif eyes == 'happy': px(im, x, y + 1, 'ink'); px(im, x + 1, y, 'ink')
        elif eyes == 'half': rect(im, x, y + 1, x + 2, y + 2, 'ink')
        elif eyes == 'wink': (rect(im, x, y, x + 2, y + 2, 'ink') if x > 10 else rect(im, x, y + 1, x + 2, y + 2, 'ink'))
    if mouth == 'open': rect(im, 9, 16, 15, 18, 'redS')
    if mouth == 'smirk': px(im, 12, 17, 'ink'); px(im, 13, 17, 'ink'); px(im, 14, 16, 'ink')
    if mouth == 'tongue': rect(im, 10, 16, 14, 17, 'ink'); rect(im, 11, 17, 13, 19, 'pink')
    if mouth == 'smile': px(im, 9, 16, 'ink'); rect(im, 10, 17, 14, 18, 'ink'); px(im, 14, 16, 'ink')
    if extra == 'tears': px(im, 5, 11, 'cyan'); px(im, 5, 12, 'cyan'); px(im, 18, 11, 'cyan'); px(im, 18, 12, 'cyan'); px(im, 4, 13, 'cyan'); px(im, 19, 13, 'cyan')
    if extra == 'blush': px(im, 6, 12, 'pink'); px(im, 17, 12, 'pink')
    if extra == 'ice': over(im, ['c.c', '.c.', 'c.c'], {'c': 'k0'}, 11, 0)
    if extra == 'bubble': over(im, ['oooo', 'owwo', 'oooo', '.o..'], {'o': 'ink', 'w': 'shirt'}, 19, 0)
    if extra == 'hands':
        over(im, ['.ss', 'sss', 'ss.'], {'s': 'skin'}, 0, 17); over(im, ['ss.', 'sss', '.ss'], {'s': 'skin'}, 21, 17)
    return im

def blob(kind):
    im = new(24, 24)
    if kind == 'plead':
        for y in range(24):
            for x in range(24):
                if (x - 12) ** 2 + (y - 13) ** 2 <= 81: px(im, x, y, 'pink' if x + y < 30 else 'pinkS')
    if kind == 'note':
        for y in range(24):
            for x in range(24):
                if ((x - 11) / 9) ** 2 + ((y - 14) / 8) ** 2 <= 1: px(im, x, y, 'shirt' if x + y < 30 else 'milkS')
        rect(im, 19, 1, 21, 13, 'ink'); rect(im, 21, 1, 23, 3, 'ink'); rect(im, 21, 3, 23, 5, 'ink')
    if kind == 'enzyme':
        for y in range(24):
            for x in range(24):
                d = (x - 12) ** 2 + (y - 13) ** 2
                ang = math.degrees(math.atan2(y - 13, x - 12))
                if d <= 81 and not (-25 < ang < 25 and x > 14): px(im, x, y, 'pur' if (x + y) % 9 else 'purS')
        im2 = im
    elif kind == 'leaf':
        for y in range(3, 23):
            w = int(9 * math.sin(math.pi * (y - 3) / 20))
            rect(im, 12 - w, y, 12 + w, y + 1, 'grn')
        for y in range(4, 23): px(im, 12, y, 'grnS')
    elif kind == 'laugh':
        for y in range(24):
            for x in range(24):
                if (x - 12) ** 2 + (y - 13) ** 2 <= 81: px(im, x, y, 'org')
        px(im, 5, 11, 'cyan'); px(im, 5, 12, 'cyan'); px(im, 18, 11, 'cyan'); px(im, 18, 12, 'cyan')
    elif kind == 'smile':
        for y in range(24):
            for x in range(24):
                if (x - 12) ** 2 + (y - 13) ** 2 <= 81: px(im, x, y, 'yel' if x + y < 30 else 'yelS')
    elif kind == 'tile':
        rect(im, 4, 5, 20, 23, 'cream'); rect(im, 4, 5, 20, 6, 'org'); rect(im, 19, 5, 20, 23, 'milkS')
        text35(im, 'So', 9, 17, 'ink')
    outline(im)
    body = {'enzyme': 'pur', 'leaf': 'grn', 'laugh': 'org', 'smile': 'yel', 'tile': 'cream', 'note': 'shirt', 'plead': 'pink'}[kind]
    add_face(im, ear=body, horns='gold' if kind == 'smile' else 'horn')
    if kind == 'laugh':   # eyes squeezed shut (^ ^) and open laughing mouth
        for (x, y) in EYES: rect(im, x, y, x + 2, y + 2, body); px(im, x, y + 1, 'ink'); px(im, x + 1, y, 'ink')
        rect(im, 9, 16, 15, 18, 'redS')
    if kind == 'plead':   # teary, pleading eyes
        for (x, y) in EYES: px(im, x, y + 2, 'cyan'); px(im, x, y + 3, 'cyan')
        over(im, ['o..o', 'oo.oo'], {'o': 'pinkS'}, 3, 19)
    if kind == 'smile':   # 염화미소: a lotus held up beside the face
        over(im, [".p.", "pLp", ".g."], {'p': 'lotus', 'L': 'lotusL', 'g': 'leaf'}, 19, 15)
    if kind == 'tile': text35(im, '8', 5, 7, 'ink')
    return im

# ================= listener catalogue (38) =================
def C(b, s, l, **kw): return ('cow', (b, s, l), kw)
LISTENERS = [
 # venue 0 절간
 dict(key='hanwoo', name='누렁소', v=0, tag='처음부터 함께한 한우. 귀가 순하다.', art=C('hw', 'hwS', 'hwL')),
 dict(key='holstein', name='얼룩소', v=0, tag='얼룩마다 경이 한 줄씩 스며든다.', art=C('milk', 'milkS', 'milk', mods=('patch',))),
 dict(key='heuku', name='검정소', v=0, tag='제주에서 왔다. 경이 까맣게 빨려 든다.', art=C('blk', 'blkS', 'blkL')),
 dict(key='chik', name='칡소', v=0, tag='얼룩빼기 황소, 칡소. 무늬가 경처럼 굽이친다.', art=C('hw', 'hwS', 'hwL', mods=('brindle',))),
 dict(key='hwang', name='황소', v=0, tag='코뚜레까지 하고 왔다. 고집도 수행이다.', art=C('orgS', 'redS', 'org', mods=('ring',))),
 dict(key='haeuso', name='해우소', v=0, tag='근심을 푸는 곳. 절에서는 뒷간을 해우소라 부른다.', art=('bld', ('wood', 'woodS', 'woodS', 'woodD', 'moon'), {})),
 # venue 1 콘서트장
 dict(key='yak', name='털소', v=1, tag='히말라야에서 온 야크. 귀털 사이로 경이 샌다.', art=C('yak', 'yakS', 'yakL', mods=('shaggy',))),
 dict(key='bison', name='들소', v=1, tag='초원의 들소. 헤드뱅잉이 제일 세다.', art=C('yakS', 'ink2', 'yak', mods=('shaggy',))),
 dict(key='goat', name='염소', v=1, tag='소인 척하는 염소. 수염으로 듣는다.', art=C('milk', 'milkS', 'milk', mods=('goat',))),
 # venue 2 오페라홀
 dict(key='bgoat', name='흑염소', v=2, tag='턱시도를 입은 줄 알았는데 원래 검다.', art=C('blk', 'blkS', 'blkL', mods=('goat',))),
 # venue 3 오케스트라홀
 dict(key='danso', name='단소', v=3, tag='대나무 단소. 구멍마다 경이 빠져나간다.', art=('bamboo', ('grnS', 'grn', 'savGL'), {})),
 dict(key='tungso', name='퉁소', v=3, tag='단소의 큰형. 낮은 소리로 경을 받는다.', art=('bamboo', ('woodS', 'wood', 'woodL'), {})),
 dict(key='eumso', name='음소', v=3, tag='소리의 가장 작은 단위. 소 귀에서 소리로 돌아간다.', art=('blob', ('note',), {})),
 # venue 4 법원
 dict(key='goso', name='고소', v=4, tag='누가 소 귀에 경을 읽었는지 따지겠다.', art=('doc', ('cream', 'seal'), {})),
 dict(key='hangso', name='항소', v=4, tag='1심에 불복. 귀를 다시 열었다.', art=('doc', ('cream', 'up'), {})),
 dict(key='sangso', name='상소', v=4, tag='더 높은 곳에서 다시 듣는다.', art=('doc', ('cyan', 'up2'), {})),
 dict(key='seungso', name='승소', v=4, tag='이겼다! 경이 잘 들어갔다고 인정받았다.', art=('doc', ('yel', 'check'), {})),
 dict(key='paeso', name='패소', v=4, tag='졌다. 그래도 경은 계속 듣는다.', art=('doc', ('ash', 'x'), {})),
 dict(key='giso', name='기소', v=4, tag='검사가 경 읽기를 정식으로 기소했다.', art=('case', ('woodS', 'wood'), {})),
 dict(key='gongso', name='공소', v=4, tag='공소장 낭독도 결국 경 읽기다.', art=('doc', ('cyan', 'seal'), {})),
 dict(key='jeso', name='제소', v=4, tag='소장을 냅니다. 소가 소장을 냈다.', art=('doc', ('cream', 'pen'), {})),
 dict(key='banso', name='반소', v=4, tag='맞고소. 소가 소에게.', art=('doc', ('pink', 'swap'), {})),
 dict(key='hoso', name='호소', v=4, tag='판사님, 저는 그냥 들었을 뿐입니다.', art=('blob', ('plead',), {})),
 # venue 5 웃음 극장
 dict(key='poksoh', name='폭소', v=5, tag='경을 듣다 웃음이 터졌다.', art=('blob', ('laugh',), {})),
 dict(key='silso', name='실소', v=5, tag='어이가 없어서 피식.', art=('face', ('yel', 'yelS', 'half', 'smirk', None), {})),
 dict(key='naengso', name='냉소', v=5, tag='차갑게 한쪽 입꼬리만 올린다.', art=('face', ('cyan', 'cyanS', 'half', 'smirk', 'ice'), {})),
 dict(key='joso', name='조소', v=5, tag='메롱. 놀리는 웃음.', art=('face', ('pur', 'purS', 'wink', 'tongue', None), {})),
 dict(key='damso', name='담소', v=5, tag='경 얘기로 수다가 끊이지 않는다.', art=('face', ('grn', 'grnS', 'happy', 'open', 'bubble'), {})),
 dict(key='hongso', name='홍소', v=5, tag='얼굴이 빨개지도록 껄껄.', art=('face', ('red', 'redS', 'happy', 'open', 'blush'), {})),
 dict(key='ilso', name='일소', v=5, tag='한 번 웃고 다 잊는다.', art=('face', ('shirt', 'milkS', 'normal', 'smile', None), {})),
 dict(key='bakjang', name='박장대소', v=5, tag='손뼉을 치며 크게 웃는다.', art=('face', ('org', 'orgS', 'happy', 'open', 'hands'), {})),
 dict(key='paan', name='파안대소', v=5, tag='얼굴이 깨질 듯 크게 웃는다.', art=('face', ('yel', 'yelS', 'happy', 'open', 'tears'), {})),
 # venue 6 야구장
 dict(key='maepyo', name='매표소', v=6, tag='외야석 두 장이요. 경은 무료.', art=('bld', ('yel', 'yelS', 'redS', 'ink2', 'ticket'), {})),
 dict(key='annae', name='안내소', v=6, tag='경은 왼쪽 귀로 들어가 오른쪽 귀로 나갑니다.', art=('bld', ('cyan', 'cyanS', 'blueS', 'navy', 'info'), {})),
 dict(key='hyuge', name='휴게소', v=6, tag='경(經)부고속도로 휴게소에서 잠시 쉬어 간다.', art=('bld', ('cream', 'milkS', 'red', 'redS', 'cup'), {})),
 # venue 4 아프리카 초원
 dict(key='rhino', name='코뿔소', v=7, tag='귀보다 뿔이 먼저 듣는다.', art=C('buf', 'bufS', 'bufL', mods=('rhino',))),
 dict(key='wrhino', name='흰코뿔소', v=7, tag='이름만 희다. 입이 넓어 경을 많이 머금는다.', art=C('stone', 'stoneS', 'steel', mods=('rhino',))),
 dict(key='brhino', name='검은코뿔소', v=7, tag='사바나의 수행자. 혼자 걷는다.', art=C('blkL', 'blk', 'ash', mods=('rhino',))),
 dict(key='buffalo', name='물소', v=7, tag='귀에 물 들어간 것처럼 경이 잘 빠진다.', art=C('buf', 'bufS', 'bufL', horn='stone', hornS='stoneS', mods=('bighorn',))),
 # venue 5 서울
 dict(key='pachul', name='파출소', v=8, tag='경(警)과 경(經)을 헷갈린 순경이 왔다.', art=('bld', ('shirt', 'milkS', 'navy', 'tux', 'siren'), {})),
 dict(key='bogeon', name='보건소', v=8, tag='귀 건강 검진은 무료입니다.', art=('bld', ('shirt', 'milkS', 'grn', 'grnS', 'cross'), {})),
 dict(key='juyu', name='주유소', v=8, tag='경으로 가득 채워 주세요.', art=('bld', ('org', 'orgS', 'red', 'redS', 'drop'), {})),
 dict(key='sobang', name='소방소', v=8, tag='원래는 소방서. 오늘만 소방소로 출동했다.', art=('bld', ('red', 'redS', 'tux', 'ink2', 'fire'), {})),
 dict(key='samu', name='사무소', v=8, tag='경 접수는 3번 창구에서.', art=('bld', ('bldL', 'bld', 'bldS', 'tux', 'antenna'), {})),
 dict(key='suk', name='숙소', v=8, tag='자면서도 귀는 열어 둔다.', art=('bld', ('pink', 'pinkS', 'woodS', 'woodD', 'zzz'), {})),
 dict(key='setak', name='세탁소', v=8, tag='귀를 깨끗이 빨아 드립니다.', art=('bld', ('cyan', 'cyanS', 'teal', 'seaS', 'bubble'), {})),
 dict(key='ibal', name='이발소', v=8, tag='귀 옆머리를 단정히. 경이 더 잘 들린다.', art=('bld', ('shirt', 'milkS', 'blue', 'blueS', 'pole'), {})),
 dict(key='yeongu', name='연구소', v=8, tag='소 귀에 경 읽기의 효과를 연구하고 있다.', art=('bld', ('shirt', 'steelS', 'teal', 'seaS', 'flask'), {})),
 dict(key='baljeon', name='발전소', v=8, tag='흘러나온 경으로 전기를 만든다.', art=('tower', (), {})),
 # venue 6 지구
 dict(key='suso', name='수소', v=9, tag='우주에서 가장 가벼운 소.', art=('sph', ('shirt', 'milkS', 'H'), {})),
 dict(key='sanso', name='산소', v=9, tag='숨 쉴 때마다 경을 듣는다.', art=('sph', ('red', 'redS', 'O', 'shirt'), {})),
 dict(key='tanso', name='탄소', v=9, tag='모든 생명의 뼈대.', art=('sph', ('blkL', 'blk', 'C', 'shirt'), {})),
 dict(key='jilso', name='질소', v=9, tag='공기의 7할. 과자 봉지에도 산다.', art=('sph', ('blue', 'blueS', 'N', 'shirt'), {})),
 dict(key='yeomso', name='염소(Cl)', v=9, tag='아까 그 염소 아님. 수영장 냄새가 난다.', art=('sph', ('grn', 'grnS', 'Cl', 'shirt'), {})),
 dict(key='hyoso', name='효소', v=9, tag='들은 경을 잘게 소화시켜 준다.', art=('blob', ('enzyme',), {})),
 dict(key='yeoprok', name='엽록소', v=9, tag='햇빛으로 경을 광합성한다.', art=('blob', ('leaf',), {})),
 dict(key='wonso', name='원소', v=9, tag='주기율표에 없는 원소. 기호 So.', art=('blob', ('tile',), {})),
 dict(key='miso', name='미소', v=9, tag='염화미소. 꽃을 들어 보이자 빙그레 웃었다.', art=('blob', ('smile',), {})),
 dict(key='white', name='흰 소', v=9, tag='모든 소가 하나로 돌아간 자리. 열반을 기다린다.', art=('holy', (), {})),
]

def listener_frames(L):
    kind, args, kw = L['art']
    if kind == 'cow':
        b, s, l = args
        base = cow_variant(b, s, l, kw.get('horn', 'horn'), kw.get('hornS', 'hornS'), kw.get('mods', ()))
        return frames_from(base, b)
    if kind == 'holy':
        t = [t for t in COW_TYPES if t['key'] == 'white'][0]
        return [cow_image(t, 0), cow_image(t, 1), *frames_from(cow_image(t, 0), 'wht')[2:]]
    if kind == 'bld': base = building(*args); return frames_from(base, args[0])
    if kind == 'tower': base = tower(); return frames_from(base, 'stone')
    if kind == 'bamboo': base = bamboo(*args); return frames_from(base, args[1])
    if kind == 'doc': base = doc(*args); return frames_from(base, args[0])
    if kind == 'face': base = face(*args); return frames_from(base, args[0])
    if kind == 'case': base = briefcase(*args); return frames_from(base, args[0])
    if kind == 'sph': base = sphere(*args); return frames_from(base, args[0])
    if kind == 'blob':
        base = blob(args[0]); body = {'enzyme': 'pur', 'leaf': 'grn', 'laugh': 'org', 'smile': 'yel', 'tile': 'cream', 'note': 'shirt', 'plead': 'pink'}[args[0]]
        return frames_from(base, body)

# ================= performers =================
PERSON = [
 "................",
 "................",
 "......oooo......",
 ".....oHHHHo.....",
 "....oHHHHHHo....",
 "....oHSSSSHo....",
 "....oSESSESo....",
 "....oSSSSSSo....",
 ".....oSMMSo.....",
 "......oSSo......",
 "....ooCCCCoo....",
 "...oCCCCCCCCo...",
 "..oSoCCCCCCoSo..",
 "..oSoCCCCCCoSo..",
 "..oSocCCCCcoSo..",
 "..oSocCCCCcoSo..",
 "..ooocCCCCcooo..",
 "....oPPPPPPo....",
 "....oPPPPPPo....",
 "....oPPooPPo....",
 "....oPPo.oPPo...",
 "....oPPo.oPPo...",
 "....oKKo.oKKo...",
 "....oooo.oooo...",
]
GOWN_LEGS = [
 "....oCCCCCCo....",
 "...oCCCCCCCCo...",
 "...oCCCCCCCCo...",
 "..oCCCCCCCCCCo..",
 "..oCCCCCCCCCCo..",
 "..occccccccccco.",
 "..oooooooooooo..",
]
def person(hair, skin, skinS, top, topS, pants, shoes='ink2', style='short', gown=False, mouth_open=False):
    rows = [r for r in PERSON]
    if gown: rows = rows[:17] + GOWN_LEGS
    if style == 'long':   # hair falls past the shoulders
        for y in (6, 7, 8, 9, 10, 11):
            r = list(rows[y]); r[3] = 'H'; r[12] = 'H'
            if y < 9: r[4] = 'H'; r[11] = 'H'
            rows[y] = ''.join(r)
    if style == 'bald':
        rows[3] = ".....oSSSSo....."; rows[4] = "....oSSSSSSo...."
    if style == 'bun':
        rows[1] = "......oHHo......"; rows[0] = ".......oo......."
    if style == 'pony':
        rows[3] = ".....oHHHHoHH..."; rows[4] = "....oHHHHHHoHH.."; rows[5] = "....oHSSSSHo.H.."
    if mouth_open:
        rows[8] = ".....oSmmSo....."
    cmap = {'o': 'ink', 'H': hair, 'S': skin, 'E': 'ink', 'M': skinS, 'm': 'redS', 'C': top, 'c': topS, 'P': pants, 'K': shoes}
    return grid(rows, cmap)

def with_prop(im, rows, cmap, ox, oy):
    im = im.copy(); over(im, rows, cmap, ox, oy); return im

def performers():
    out = {}
    # ---- metal band ----
    guitar = (["........ooo", ".......ow o", "......oo...", ".....oo....", "..oooo.....", ".oBBBo.....", "oBBBBBo....", "oBBwBBo....", ".oBBBo.....", "..ooo......"],
              {'o': 'ink', 'B': 'redS', 'w': 'shirt', ' ': 'steel'})
    vee = (["........oo.", ".......oso.", "......oo...", "..o..oo....", ".owoowo.....", "..owwwo....", "...owwo....", "....oo....."],
           {'o': 'ink', 'w': 'shirt', 's': 'steel'})
    bassg = (["..........o", ".........oo", "........oo.", ".......oo..", "......oo...", "..ooooo....", ".oKKKKo....", "oKKwKKo....", ".oKKKo.....", "..ooo......"],
             {'o': 'ink', 'K': 'blueS', 'w': 'shirt'})
    for name, hair, prop, style in (('m_rhythm', 'hairB', guitar, 'long'), ('m_lead', 'hairY', vee, 'long'), ('m_bass', 'hairR', bassg, 'short')):
        a = person(hair, 'skin', 'skinS', 'tux', 'tuxL', 'tux', style=style)
        f0 = with_prop(a, prop[0], prop[1], 3, 11)
        b = person(hair, 'skin', 'skinS', 'tux', 'tuxL', 'tux', style=style, mouth_open=True)
        b2 = Image.new('RGBA', b.size, T); b2.paste(b.crop((0, 0, 16, 10)), (0, 1)); b2.paste(b.crop((0, 10, 16, 24)), (0, 10))
        f1 = with_prop(b2, prop[0], prop[1], 3, 12)
        out[name] = [f0, f1]
    mic = (["...oo", "..oso", "...o.", "...o.", "...o.", "...o.", "...o.", "...o.", "...o.", "...o.", "..ooo"], {'o': 'ink', 's': 'steel'})
    v0 = person('hairB', 'skin', 'skinS', 'redS', 'redS', 'tux', style='long')
    v1 = person('hairB', 'skin', 'skinS', 'redS', 'redS', 'tux', style='long', mouth_open=True)
    v1b = Image.new('RGBA', v1.size, T); v1b.paste(v1.crop((0, 0, 16, 10)), (0, 2)); v1b.paste(v1.crop((0, 10, 16, 24)), (0, 10))
    out['m_vocal'] = [with_prop(v0, mic[0], mic[1], 11, 9), with_prop(v1b, mic[0], mic[1], 11, 9)]
    # drummer 24x24: kit in front of a seated drummer
    def drummer(up):
        im = new(24, 24)
        p = person('hairB', 'skin', 'skinS', 'tux', 'tuxL', 'tux', style='long', mouth_open=up)
        im.alpha_composite(p.crop((0, 0, 16, 16)), (4, 0 if not up else 1))
        kit = ["..oo...............oo...", ".osso.............osso..", "..oo...ooooooooo...oo...", "...o..oKKKKKKKKKo..o....",
               "...o.oKKKwwwwwKKKo.o....", "..ooooKKwwrrrwwKKoooo...", ".oKKKoKKwrrrrrwKKoKKKo..", ".oKKKoKKwwrrrwwKKoKKKo..",
               ".oooooKKKwwwwwKKKooooo..", "......oKKKKKKKKKo.......", ".......ooooooooo........"]
        over(im, kit, {'o': 'ink', 's': 'brass', 'K': 'redS', 'w': 'shirt', 'r': 'red'}, 0, 13)
        sticks = [(6, 9), (7, 10), (8, 11), (17, 9), (16, 10), (15, 11)] if up else [(5, 13), (6, 13), (7, 14), (18, 13), (17, 13), (16, 14)]
        for (x, y) in sticks: px(im, x, y, 'woodL')
        return im
    out['m_drum'] = [drummer(False), drummer(True)]
    # ---- opera ----
    def singer(hair, top, topS, pants, style, gown, skin='skin', skinS='skinS', beard=False, bow=False):
        fr = []
        for open_ in (False, True):
            im = person(hair, skin, skinS, top, topS, pants, style=style, gown=gown, mouth_open=open_)
            if bow: px(im, 7, 10, 'red'); px(im, 8, 10, 'red'); rect(im, 7, 11, 9, 14, 'shirt')
            if beard: rect(im, 6, 8, 10, 9, hair); px(im, 5, 7, hair); px(im, 10, 7, hair)
            if open_:   # arms flung open
                for y in (11, 12): px(im, 1, y, skin); px(im, 14, y, skin); px(im, 0, y - 1, 'ink'); px(im, 15, y - 1, 'ink')
            fr.append(im)
        return fr
    out['o_sop'] = singer('hairY', 'red', 'redS', 'red', 'bun', True)
    out['o_mez'] = singer('hairBr', 'blue', 'blueS', 'blue', 'long', True, skin='skin2', skinS='skin2S')
    out['o_ten'] = singer('hairB', 'tux', 'tuxL', 'tux', 'short', False, bow=True)
    out['o_bar'] = singer('hairBr', 'tux', 'tuxL', 'tux', 'short', False, beard=True, bow=True, skin='skin2', skinS='skin2S')
    def choir(open_):
        im = new(24, 24)
        for i, (x, y, sk) in enumerate(((0, 2, 'skin'), (8, 0, 'skin2'), (16, 2, 'skin3'))):
            p = person(('hairB', 'hairBr', 'hairB')[i], sk, sk + 'S', 'velvet', 'velvetS', 'velvet', gown=True, mouth_open=open_ and i != 1 or (not open_ and i == 1))
            im.alpha_composite(p.crop((0, 0, 16, 24)).resize((16, 24)), (x - 4 + (i == 1) * 0, y))
        return im
    out['o_choir'] = [choir(False), choir(True)]
    # ---- orchestra ----
    def orch(prop, up, hair='hairB', skin='skin', skinS='skinS', gown=False, top='tux', topS='tuxL', style='short'):
        im = person(hair, skin, skinS, top, topS, top, style=style, gown=gown, mouth_open=False)
        if not gown: px(im, 7, 10, 'shirt'); px(im, 8, 10, 'shirt')
        if prop == 'baton':
            if up: px(im, 13, 7, 'shirt'); px(im, 14, 6, 'shirt'); px(im, 15, 5, 'shirt'); px(im, 13, 11, skin); px(im, 13, 9, skin); px(im, 13, 10, skin)
            else: px(im, 14, 11, 'shirt'); px(im, 15, 10, 'shirt')
            px(im, 0, 9 if up else 12, skin); px(im, 1, 10 if up else 12, skin)
        if prop == 'violin':
            over(im, ["..ooo..", ".oWWWo.", "oWwWWo.", ".oooWo.", "....o.."], {'o': 'ink', 'W': 'woodS', 'w': 'wood'}, 9, 7)
            bx = 2 if up else 4
            for k in range(8): px(im, bx + k, 6 + k // 2 if up else 9 - k // 3, 'steel')
        if prop == 'cello':
            over(im, ["...o...", "...o...", "..ooo..", ".oWWWo.", "oWwWwWo", "oWWWWWo", ".oWwWo.", "oWWWWWo", "oWWWWWo", ".ooooo.", "...o..."], {'o': 'ink', 'W': 'woodS', 'w': 'wood'}, 5, 11)
            for k in range(7): px(im, 2 + k, 17 + (k % 2 if up else 0), 'steel')
        if prop == 'flute':
            for x in range(1, 15): px(im, x, 9, 'steel' if x % 3 else 'steelS')
            if up: px(im, 15, 8, 'steel')
        if prop == 'horn':
            over(im, ["..ooo..", ".obbbo.", "obo.obo", "ob...bo", "obo.obo", ".obbbbo", "..ooo.o"], {'o': 'brassS', 'b': 'brass'}, 4, 11 if up else 12)
        return im
    out['r_cond'] = [orch('baton', False, hair='steel'), orch('baton', True, hair='steel')]
    out['r_vln'] = [orch('violin', False, hair='hairBr', gown=True, top='tux', topS='tuxL', style='bun'), orch('violin', True, hair='hairBr', gown=True, top='tux', topS='tuxL', style='bun')]
    out['r_vc'] = [orch('cello', False, skin='skin2', skinS='skin2S'), orch('cello', True, skin='skin2', skinS='skin2S')]
    out['r_fl'] = [orch('flute', False, hair='hairY', gown=True, style='long'), orch('flute', True, hair='hairY', gown=True, style='long')]
    out['r_hn'] = [orch('horn', False, hair='hairR'), orch('horn', True, hair='hairR')]
    def timpani(up):
        im = new(24, 24)
        p = person('hairB', 'skin3', 'skin3S', 'tux', 'tuxL', 'tux', style='short')
        im.alpha_composite(p.crop((0, 0, 16, 16)), (4, 0))
        drum = ["oooooooo", "osssssso", "obbbbbbo", ".obbbbo.", "..obbo..", "...oo..."]
        over(im, drum, {'o': 'ink', 's': 'cream', 'b': 'brass'}, 0, 13); over(im, drum, {'o': 'ink', 's': 'cream', 'b': 'brass'}, 15, 14)
        for (x, y) in ([(3, 9), (4, 10), (20, 9), (19, 10)] if up else [(5, 12), (6, 12), (18, 12), (17, 12)]): px(im, x, y, 'woodL')
        return im
    out['r_timp'] = [timpani(False), timpani(True)]
    # ---- courtroom ----
    def court(role, up):
        if role == 'judge':
            im = person('steel', 'skin', 'skinS', 'tux', 'tuxL', 'tux', style='short', gown=True)
            rect(im, 6, 10, 10, 12, 'shirt')
            g = ['.ooo', 'owwo', '.ooo', '..o.', '..o.'] if not up else ['...o', 'ooow', 'owwo', 'ooo.']
            over(im, g, {'o': 'ink', 'w': 'wood'}, 12, 7 if up else 11)
            return im
        if role == 'pros':
            im = person('hairB', 'skin', 'skinS', 'tux', 'tuxL', 'tux', style='short', mouth_open=up)
            rect(im, 7, 10, 9, 15, 'red')
            if up:
                for (x, y) in ((13, 9), (14, 8), (15, 7)): px(im, x, y, 'skin')
                px(im, 14, 9, 'ink'); px(im, 15, 8, 'ink')
            return im
        if role == 'lawyer':
            im = person('hairBr', 'skin2', 'skin2S', 'navy', 'blueS', 'navy', style='short')
            rect(im, 7, 10, 9, 15, 'shirt')
            over(im, ['.oooo.', 'owwwwo', 'owwwwo', '.oooo.'] if up else ['oooo', 'wwwo', 'wwwo', 'oooo'], {'o': 'ink', 'w': 'cream'}, 10, 9 if up else 12)
            return im
        if role == 'steno':
            im = person('hairR', 'skin', 'skinS', 'blue', 'blueS', 'navy', style='bun', gown=True)
            over(im, ['oooooooooo', 'osksksksko', 'oooooooooo'], {'o': 'ink', 's': 'steel', 'k': 'tuxL'}, 3, 15 + (1 if up else 0))
            return im
    for k, role in (('j_judge', 'judge'), ('j_pros', 'pros'), ('j_lawyer', 'lawyer'), ('j_steno', 'steno')):
        out[k] = [court(role, False), court(role, True)]
    # ---- comedy club ----
    def comic(up):
        im = person('hairB', 'skin', 'skinS', 'pur', 'purS', 'tux', style='short', mouth_open=up)
        rect(im, 7, 10, 9, 15, 'yel')
        over(im, ['.oo', 'oso', '.o.'], {'o': 'ink', 's': 'steel'}, 12 if up else 11, 6 if up else 9)
        if up: px(im, 1, 9, 'skin'); px(im, 0, 8, 'skin')
        return im
    def rimshot(up):
        im = new(24, 24)
        p = person('hairBr', 'skin2', 'skin2S', 'blue', 'blueS', 'navy', style='short', mouth_open=up)
        im.alpha_composite(p.crop((0, 0, 16, 16)), (4, 0))
        kit = ['.oo..........oo.', 'osso........osso', '.oo..ooooo...oo.', '..o.obbbbbo..o..', '..oobbwwwbboo...', '...obbwwwbbo....', '....obbbbbo.....', '.....ooooo......']
        over(im, kit, {'o': 'ink', 's': 'brass', 'b': 'blueS', 'w': 'shirt'}, 4, 15)
        for (x, y) in ([(5, 10), (6, 11), (18, 9), (17, 10)] if up else [(6, 14), (7, 14), (17, 14), (16, 14)]): px(im, x, y, 'woodL')
        return im
    def crowd(up):
        im = new(24, 24)
        for i, (x, sk, hair, top) in enumerate(((0, 'skin', 'hairY', 'red'), (8, 'skin3', 'hairB', 'grn'), (16, 'skin2', 'hairBr', 'blue'))):
            p = person(hair, sk, sk + 'S', top, top + 'S', 'navy', style='short', mouth_open=up or i == 1)
            im.alpha_composite(p.crop((0, 0, 16, 18)), (x - 4, 6 - (1 if up and i != 1 else 0)))
        return im
    def clapper(up):
        im = person('hairR', 'skin', 'skinS', 'org', 'orgS', 'navy', style='pony', mouth_open=True)
        for y in (11, 12):
            for x in (2, 3, 12, 13): px(im, x, y, T if True else 'skin')
        if up: rect(im, 6, 10, 10, 12, 'skin')
        else: px(im, 3, 11, 'skin'); px(im, 12, 11, 'skin'); px(im, 2, 11, 'ink'); px(im, 13, 11, 'ink')
        return im
    out['h_comic'] = [comic(False), comic(True)]
    out['h_drum'] = [rimshot(False), rimshot(True)]
    out['h_crowd'] = [crowd(False), crowd(True)]
    out['h_clap'] = [clapper(False), clapper(True)]
    # ---- stadium cheer squad ----
    def jersey(skin, skinS, hair, style, prop=None, up=False, skirt=False, col='blue', colS='blueS'):
        im = person(hair, skin, skinS, col, colS, 'shirt' if skirt else 'navy', style=style, gown=False, mouth_open=up)
        if skirt:
            for y in range(17, 20): rect(im, 4, y, 12, y + 1, col if y < 19 else colS)
            for y in range(20, 24): r = list(PERSON[y]); im2 = None
            rect(im, 5, 20, 7, 22, skin); rect(im, 9, 20, 11, 22, skin)
        if prop == 'pompom':
            for (x, y) in ((1, 8 if up else 14), (14, 8 if up else 14)):
                for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                    px(im, x + dx, y + dy, 'yel' if (dx + dy) % 2 else 'red')
        if prop == 'mega':
            over(im, (["oo...", "oyyo.", "oyyyo", "oyyo.", "oo..."] if up else ["....oo", "...oyo", "..oyyo", "...oyo", "....oo"]),
                 {'o': 'ink', 'y': 'yel'}, 11 if up else 0, 5 if up else 10)
        if prop == 'trumpet':
            over(im, ["....oo", "ooooyo", "yyyyyo", "ooooyo", "....oo"], {'o': 'brassS', 'y': 'brass'}, 10, 7 if up else 8)
        if prop == 'drum':
            over(im, [".ooooo.", "orrrrro", "owwwwwo", "orrrrro", "owwwwwo", "orrrrro", ".ooooo."], {'o': 'ink', 'r': 'red', 'w': 'shirt'}, 9, 12)
            px(im, 14 if up else 12, 9 if up else 11, 'woodL'); px(im, 13, 10, 'woodL')
        return im
    out['c_leader'] = [jersey('skin', 'skinS', 'hairB', 'short', 'mega', False), jersey('skin', 'skinS', 'hairB', 'short', 'mega', True)]
    for i, (sk, hair, col, colS) in enumerate((('skin', 'hairB', 'red', 'redS'), ('skin2', 'hairBr', 'blue', 'blueS'), ('skin', 'hairY', 'red', 'redS'))):
        out[f'c_cheer{i}'] = [jersey(sk, sk + 'S', hair, 'pony', 'pompom', False, True, col, colS), jersey(sk, sk + 'S', hair, 'pony', 'pompom', True, True, col, colS)]
    out['c_drum'] = [jersey('skin2', 'skin2S', 'hairB', 'short', 'drum', False), jersey('skin2', 'skin2S', 'hairB', 'short', 'drum', True)]
    out['c_trumpet'] = [jersey('skin', 'skinS', 'hairBr', 'short', 'trumpet', False), jersey('skin', 'skinS', 'hairBr', 'short', 'trumpet', True)]
    # ---- djembe (savanna) ----
    def djembe(skin, skinS, top, topS, up):
        im = person('hairB', skin, skinS, top, topS, 'woodD', style='short', mouth_open=up)
        for y in range(11, 17):
            for x in range(5, 11):
                if im.getpixel((x, y)) == P[top] and (x + y) % 3 == 0: px(im, x, y, 'yel')
        dj = ["oooooo", "owwwwo", ".oWWo.", "..oWo.", "..oWo.", ".oWWWo", ".ooooo"]
        over(im, dj, {'o': 'ink', 'w': 'cream', 'W': 'woodS'}, 5, 14)
        if up: px(im, 4, 11, skin); px(im, 11, 11, skin)
        else: px(im, 6, 14, skin); px(im, 9, 14, skin)
        return im
    for i, (sk, top, topS) in enumerate((('skin3', 'org', 'orgS'), ('skin2', 'grn', 'grnS'), ('skin3', 'yel', 'yelS'))):
        out[f'd_djembe{i}'] = [djembe(sk, sk + 'S', top, topS, False), djembe(sk, sk + 'S', top, topS, True)]
    # ---- samulnori (Seoul street festival) ----
    def samul(sash, prop, up):
        im = person('hairB', 'skin', 'skinS', 'shirt', 'milkS', 'shirt', shoes='ink2', style='short', mouth_open=up)
        rect(im, 4, 14, 12, 15, sash)          # sash
        over(im, ["...o...", "..oro..", ".owwwo.", "owwwwwo"], {'o': 'ink', 'w': 'shirt', 'r': 'pink'}, 4, 0)   # 고깔
        if prop == 'kkwaeng': over(im, [".ooo.", "obbbo", "obbbo", ".ooo."], {'o': 'brassS', 'b': 'brass'}, 0 if not up else 1, 10)
        if prop == 'janggu': over(im, ["oo.....oo", "oro...oro", "oooooooo.", "oro...oro", "oo.....oo"], {'o': 'ink', 'r': 'red'}, 3, 13)
        if prop == 'buk': over(im, [".ooooo.", "owwwwwo", "orrrrro", "owwwwwo", ".ooooo."], {'o': 'ink', 'w': 'cream', 'r': 'redS'}, 4, 12)
        if prop == 'jing': over(im, ["..ooooo..", ".obbbbbo.", "obbbBbbbo", ".obbbbbo.", "..ooooo.."], {'o': 'brassS', 'b': 'brass', 'B': 'yelS'}, 7, 11)
        stick = (12, 9) if up else (13, 12)
        px(im, stick[0], stick[1], 'woodL'); px(im, stick[0] + 1, stick[1] - 1, 'woodL')
        return im
    for k, sash, prop in (('s_kkwaeng', 'red', 'kkwaeng'), ('s_janggu', 'blue', 'janggu'), ('s_buk', 'yel', 'buk'), ('s_jing', 'grn', 'jing')):
        out[k] = [samul(sash, prop, False), samul(sash, prop, True)]
    return out

# ================= venues (320x200) =================
W, H = 320, 200
def canvas(c='sky0'): return Image.new('RGBA', (W, H), P[c])
def dgrad(im, y0, y1, cols, x0=0, x1=W):
    pxs = im.load()
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0) * (len(cols) - 1)
        i = min(int(t), len(cols) - 2); f = t - i
        for x in range(x0, x1): pxs[x, y] = P[cols[i + 1]] if f * 16 > BAYER[y % 4][x % 4] else P[cols[i]]
def fill(im, x0, y0, x1, y1, c):
    pxs = im.load()
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)): pxs[x, y] = P[c]
def ridge(im, base, amp, freq, seed, col, bottom=None):
    rr = random.Random(seed); ph = [rr.uniform(0, 6.28) for _ in range(3)]
    pxs = im.load()
    for x in range(W):
        h = int(base - amp * (0.55 * math.sin(x * freq + ph[0]) + 0.3 * math.sin(x * freq * 2.3 + ph[1]) + 0.15 * math.sin(x * freq * 5.1 + ph[2])))
        for y in range(max(0, h), bottom or H): pxs[x, y] = P[col]
def disc(im, cx, cy, r, c):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r and 0 <= x < W and 0 <= y < H: im.putpixel((x, y), P[c])

def ground(im, y0, cols=('grs0', 'grs1', 'grs2'), tuft='grsL', seed=1):
    pxs = im.load(); rnd = random.Random(seed)
    for y in range(y0, H):
        t = (y - y0) / (H - y0)
        i = 0 if t < 0.35 else (1 if t < 0.75 else 2)
        for x in range(W):
            c = cols[i]
            if 0.3 <= t < 0.4 and BAYER[y % 4][x % 4] < 8: c = cols[1]
            if 0.7 <= t < 0.8 and BAYER[y % 4][x % 4] < 8: c = cols[2]
            pxs[x, y] = P[c]
    for x in range(W): pxs[x, y0] = P[tuft]
    for _ in range(160):
        x = rnd.randrange(2, W - 2); y = rnd.randrange(y0 + 3, H - 2)
        pxs[x, y] = P[tuft]; pxs[x - 1, y + 1] = P[tuft]; pxs[x + 1, y + 1] = P[tuft]

def venue_temple():
    from art import background
    old = background()                         # the original 320x180 temple scene
    im = canvas(); im.paste(old, (0, 0))
    pxs = im.load(); rnd = random.Random(2)
    for y in range(176, H):
        for x in range(W):
            c = pxs[x, y]
            if y >= 178 or c in (P['dirt'], P['dirtS']):
                pxs[x, y] = P['grs2'] if (y > 181 or BAYER[y % 4][x % 4] < 10) else P['grs1']
    for _ in range(30):
        x = rnd.randrange(2, W - 2); y = rnd.randrange(182, H - 2)
        pxs[x, y] = P['grs1']; pxs[x - 1, y + 1] = P['grs1']; pxs[x + 1, y + 1] = P['grs1']
    return im

def stars(im, n, y1, seed=3, cols=('k0', 'steel')):
    rnd = random.Random(seed)
    for _ in range(n): px(im, rnd.randrange(W), rnd.randrange(y1), rnd.choice(cols))

def venue_concert():
    im = canvas('night0'); dgrad(im, 0, 120, ['night0', 'night1', 'night2'])
    stars(im, 40, 60)
    # LED wall with a giant 소 glyph
    fill(im, 140, 18, 300, 70, 'stage');
    g = bdf_glyphs('package/dist/Galmuri7.bdf', '소')['소']
    for yy, r in enumerate(g['rows']):
        for xx, v in enumerate(r):
            if v == '1': fill(im, 196 + xx * 6, 22 + yy * 6, 196 + xx * 6 + 5, 22 + yy * 6 + 5, 'pinkS')
    # truss with lamps
    fill(im, 0, 8, W, 11, 'steelS')
    for x in range(0, W, 6): px(im, x, 9, 'steel'); px(im, x + 3, 10, 'steel')
    lamp_cols = ['red', 'cyan', 'yel', 'pink', 'grn']
    for i, x in enumerate(range(14, W, 30)):
        fill(im, x, 11, x + 4, 15, 'ink'); fill(im, x + 1, 13, x + 3, 15, lamp_cols[i % 5])
        for y in range(15, 170):     # dithered light cone
            spread = (y - 15) // 5
            for xx in range(x + 2 - spread, x + 2 + spread + 1):
                if 0 <= xx < W and BAYER[y % 4][xx % 4] == 0 and (y + xx) % 3 == 0: px(im, xx, y, lamp_cols[i % 5])
    # stage (left) and crowd floor
    fill(im, 0, 86, 118, 96, 'stageL'); fill(im, 0, 96, 118, 100, 'ink')
    for x0 in (0, 104):   # amp stacks
        fill(im, x0, 50, x0 + 14, 86, 'ink'); fill(im, x0 + 2, 54, x0 + 12, 68, 'stage'); fill(im, x0 + 2, 70, x0 + 12, 84, 'stage')
        disc(im, x0 + 7, 61, 4, 'tuxL'); disc(im, x0 + 7, 77, 4, 'tuxL')
    fill(im, 0, 100, W, H, 'stage')
    for y in range(100, H):
        for x in range(W):
            if BAYER[y % 4][x % 4] < 2: px(im, x, y, 'night1')
    return im

def venue_opera():
    im = canvas('velvetS'); dgrad(im, 0, 110, ['velvetS', 'velvet'])
    # balconies with tiny audience
    for by in (22, 46):
        fill(im, 120, by, W, by + 4, 'gold'); fill(im, 120, by + 4, W, by + 6, 'goldS')
        rnd = random.Random(by)
        for x in range(122, W - 2, 3): px(im, x, by - 2, rnd.choice(['skin', 'skin2', 'hairB', 'skin3'])); px(im, x, by - 1, rnd.choice(['tux', 'red', 'blue']))
    fill(im, 0, 0, W, 6, 'velvetL');
    for x in range(0, W, 8): fill(im, x, 6, x + 4, 9, 'gold')
    # curtains framing the stage (left side)
    for x in range(0, 10):
        for y in range(0, 120): px(im, x, y, 'velvetL' if (x // 2) % 2 else 'velvet')
    for x in range(110, 120):
        for y in range(0, 120): px(im, x, y, 'velvetL' if (x // 2) % 2 else 'velvet')
    # stage floor + footlights
    fill(im, 0, 110, 120, 124, 'wood');
    for x in range(0, 120, 4): fill(im, x, 110, x + 1, 124, 'woodS')
    fill(im, 0, 124, 120, 127, 'woodD')
    for x in range(6, 118, 12): fill(im, x, 122, x + 3, 124, 'k1')
    fill(im, 0, 127, 120, H, 'velvetS')
    # seats in rows for the herd (aligned to listener rows)
    fill(im, 120, 60, W, H, 'velvetS')
    for ry in (52, 71, 90, 109, 128, 147, 166):
        for x in range(118, W, 13):
            fill(im, x, ry + 18, x + 11, ry + 24, 'velvetL'); fill(im, x, ry + 24, x + 11, ry + 26, 'velvet')
    return im

def venue_orchestra():
    im = canvas('woodD'); dgrad(im, 0, 120, ['woodD', 'woodS'])
    # organ pipes
    for i, x in enumerate(range(130, 312, 6)):
        h = 30 + int(22 * math.sin((x - 130) / 182 * math.pi))
        fill(im, x, 50 - h + 20, x + 4, 70, 'steel' if i % 2 else 'steelS'); px(im, x + 1, 70 - 8, 'ink'); px(im, x + 2, 70 - 8, 'ink')
    fill(im, 124, 70, 318, 74, 'woodL')
    # wood panels
    for x in range(0, W, 20): fill(im, x, 0, x + 1, 120, 'woodD')
    # risers for the players (left)
    for k, y in enumerate((60, 86, 112)):
        fill(im, 0, y, 120, y + 3, 'woodL'); fill(im, 0, y + 3, 120, y + 5, 'woodS')
    # warm stage lights
    for x in range(10, 120, 22): fill(im, x, 0, x + 3, 3, 'k1')
    # audience floor with seats
    fill(im, 120, 74, W, H, 'woodS')
    for ry in (52, 71, 90, 109, 128, 147, 166):
        for x in range(118, W, 13):
            if ry + 18 > 74: fill(im, x, ry + 18, x + 11, ry + 24, 'blueS'); fill(im, x, ry + 24, x + 11, ry + 26, 'navy')
    fill(im, 0, 120, 120, H, 'woodS')
    for y in range(120, H, 6): fill(im, 0, y, 120, y + 1, 'woodD')
    return im

def venue_court():
    im = canvas('woodD'); dgrad(im, 0, 120, ['woodD', 'woodS'])
    for x in range(0, W, 16): fill(im, x, 0, x + 1, 130, 'woodD')
    for y in (24, 60, 96): fill(im, 0, y, W, y + 1, 'woodD')
    # scales emblem on the back wall
    cx = 220
    fill(im, cx - 1, 10, cx + 1, 40, 'gold'); fill(im, cx - 18, 14, cx + 19, 16, 'gold'); fill(im, cx - 8, 40, cx + 9, 42, 'gold')
    for dx in (-16, 16):
        for k in range(8): px(im, cx + dx - 4 + k, 24 + (k in (0, 7)) * 0, 'goldS')
        fill(im, cx + dx - 5, 24, cx + dx + 6, 26, 'gold')
        px(im, cx + dx, 16, 'gold'); fill(im, cx + dx, 17, cx + dx + 1, 24, 'goldS')
    # judge's bench (left, high) and witness rail
    fill(im, 0, 86, 118, 112, 'wood'); fill(im, 0, 86, 118, 89, 'woodL'); fill(im, 0, 110, 118, 112, 'woodS')
    for x in range(8, 118, 18): fill(im, x, 92, x + 12, 106, 'woodS')
    # floor and pews for the herd
    fill(im, 0, 112, W, H, 'woodS')
    for y in range(112, H, 7): fill(im, 0, y, W, y + 1, 'woodD')
    for ry in (46, 62, 78, 94, 110, 126, 142, 158):
        fill(im, 118, ry + 18, W, ry + 21, 'wood'); fill(im, 118, ry + 21, W, ry + 23, 'woodD')
    fill(im, 116, 168, W, 172, 'woodL')
    return im

def venue_comedy():
    im = canvas('velvetS')
    # brick wall
    for y in range(0, 130):
        for x in range(W):
            mortar = y % 6 == 5 or (x + (y // 6 % 2) * 6) % 12 == 11
            px(im, x, y, 'ink2' if mortar else ('redS' if (x // 12 + y // 6) % 3 else 'velvetS'))
    # neon sign "웃음" (Galmuri7 glyphs, 4x)
    g = bdf_glyphs('package/dist/Galmuri7.bdf', '웃음')
    x0 = 170
    for ch in '웃음':
        gg = g[ch]
        for yy, r in enumerate(gg['rows']):
            for xx, v in enumerate(r):
                if v == '1': fill(im, x0 + xx * 4, 10 + yy * 4, x0 + xx * 4 + 3, 10 + yy * 4 + 3, 'pink')
        x0 += gg['dw'] * 4 + 4
    # stage (left), spotlight circle, mic stand
    fill(im, 0, 112, 118, 122, 'wood'); fill(im, 0, 112, 118, 114, 'woodL'); fill(im, 0, 122, 118, 126, 'woodD')
    for y in range(0, 112):
        half = 10 + y // 4
        for x in range(56 - half, 56 + half):
            if 0 <= x < 118 and BAYER[y % 4][x % 4] < 2: px(im, x, y, 'k1')
    # audience floor with little round tables
    fill(im, 0, 126, W, H, 'tux'); fill(im, 118, 60, W, H, 'tux')
    for y in range(60, H):
        for x in range(118, W):
            if BAYER[y % 4][x % 4] == 0: px(im, x, y, 'tuxL')
    for (tx, ty) in ((140, 86), (200, 100), (260, 84), (170, 132), (240, 140), (300, 120)):
        disc(im, tx, ty, 5, 'wood'); px(im, tx, ty - 3, 'k1')
    return im

def venue_stadium():
    im = canvas('night0'); dgrad(im, 0, 60, ['night0', 'night1'])
    stars(im, 30, 40)
    # stands with crowd
    rnd = random.Random(9)
    for y in range(30, 70):
        for x in range(W):
            px(im, x, y, rnd.choice(['blueS', 'navy', 'red', 'shirt', 'blue', 'navy']) if (x + y) % 2 == 0 else 'tux')
    fill(im, 0, 70, W, 74, 'steelS')
    # floodlight towers
    for x0 in (20, 290):
        fill(im, x0, 4, x0 + 3, 40, 'steelS'); fill(im, x0 - 6, 0, x0 + 9, 6, 'steel')
        for x in range(x0 - 5, x0 + 9, 2): px(im, x, 2, 'k0'); px(im, x + 1, 4, 'k0')
    # scoreboard
    fill(im, 120, 4, 228, 28, 'ink'); fill(im, 122, 6, 226, 26, 'tux')
    g = bdf_glyphs('package/dist/Galmuri7.bdf', '소경0:')
    def t(s, x, y, c):
        for ch in s:
            if ch == ' ': x += 6; continue
            gg = g[ch]
            for yy, r in enumerate(gg['rows']):
                for xx, v in enumerate(r):
                    if v == '1': fill(im, x + gg['ox'] + xx * 2, y + (7 - gg['oy'] - gg['h'] + yy) * 2, x + gg['ox'] + xx * 2 + 2, y + (7 - gg['oy'] - gg['h'] + yy) * 2 + 2, c)
            x += gg['dw'] * 2
    t('소 0:0 경', 132, 8, 'yel')
    # field
    fill(im, 0, 74, W, H, 'field')
    for y in range(74, H):
        for x in range(W):
            if (x // 16 + y // 16) % 2 == 0: px(im, x, y, 'fieldL' if BAYER[y % 4][x % 4] < 3 else 'field')
    # infield dirt diamond + bases
    for y in range(110, H):
        for x in range(W):
            if abs(x - 215) + abs(y - 170) * 1.6 < 95 and abs(x - 215) + abs(y - 170) * 1.6 > 70: px(im, x, y, 'dirt')
    for (x, y) in ((215, 116), (160, 152), (270, 152)): fill(im, x - 2, y - 2, x + 2, y + 2, 'shirt')
    # cheer stage (응원단상) bottom
    fill(im, 116, 196, W, H, 'blueS')
    fill(im, 0, 140, 116, 145, 'blue')
    return im

def venue_savanna():
    im = canvas('sav0'); dgrad(im, 0, 96, ['sav0', 'sav1', 'sav2'][::-1][::-1])
    disc(im, 160, 70, 34, 'k1'); disc(im, 160, 70, 30, 'k0')
    # Kilimanjaro-ish mountain with snow cap
    for x in range(W):
        h = int(64 + abs(x - 250) * 0.45)
        for y in range(h, 100): px(im, x, y, 'sav2' if y > h + 3 else ('shirt' if h < 72 else 'sav2'))
    ground(im, 92, ('savGL', 'savG', 'savGS'), 'sav0', seed=5)
    # acacia trees (flat crowns)
    for (x0, y0, w) in ((40, 60, 34), (284, 50, 30)):
        fill(im, x0 + w // 2 - 1, y0 + 4, x0 + w // 2 + 2, y0 + 40, 'bark')
        for k in range(4):
            fill(im, x0 + k * 2, y0 + k, x0 + w - k * 2, y0 + k + 1, 'grnS')
        for k in range(5): px(im, x0 + w // 2 - 3 + k, y0 + 6 + k, 'bark')
    return im

def venue_seoul():
    im = canvas('city0'); dgrad(im, 0, 100, ['city2', 'city1', 'city0'])
    rnd = random.Random(21)
    # far apartments
    x = 0
    while x < W:
        w = rnd.randrange(10, 22); h = rnd.randrange(20, 46)
        fill(im, x, 96 - h, x + w, 96, 'bldS')
        for wy in range(96 - h + 3, 94, 4):
            for wx in range(x + 2, x + w - 2, 3):
                if rnd.random() < 0.45: px(im, wx, wy, 'win')
        x += w + 1
    # Namsan tower on a hill
    for xx in range(150, 230):
        h = int(78 - 14 * math.sin((xx - 150) / 80 * math.pi))
        for y in range(h, 96): px(im, xx, y, 'grnS')
    fill(im, 189, 26, 192, 66, 'steel'); fill(im, 185, 40, 196, 46, 'steel'); fill(im, 186, 46, 195, 48, 'steelS')
    fill(im, 190, 14, 191, 26, 'steelS'); px(im, 190, 13, 'red')
    # tall tower on the right
    for y in range(10, 96):
        hw = 2 + (y - 10) // 12
        fill(im, 270 - hw, y, 270 + hw, y + 1, 'bldL' if y % 6 else 'bld')
    # river + bridge
    fill(im, 0, 96, W, 104, 'sea')
    for x in range(0, W, 2): px(im, x, 98 + (x // 2) % 2, 'cyan')
    fill(im, 0, 92, W, 94, 'steelS')
    for x in range(10, W, 40):
        for k in range(10): px(im, x + k, 92 - int(4 * math.sin(k / 9 * math.pi)), 'steel'); px(im, x + 20 + k, 92 - int(4 * math.sin(k / 9 * math.pi)), 'steel')
    # plaza ground (paving)
    fill(im, 0, 104, W, H, 'stone')
    for y in range(104, H):
        for x in range(W):
            if y % 8 == 0 or (x + (y // 8) * 4) % 16 == 0: px(im, x, y, 'stoneS')
    return im

def venue_earth():
    im = canvas('space0'); dgrad(im, 0, H, ['space0', 'space1'])
    stars(im, 150, H, seed=8, cols=('k0', 'steel', 'cyan', 'k1'))
    disc(im, 40, 30, 12, 'stone'); disc(im, 44, 27, 3, 'stoneS'); disc(im, 36, 34, 2, 'stoneS')
    # the Earth: a huge disc whose top arc forms the ground
    cx, cy, r = 160, 560, 470
    rnd = random.Random(4)
    pxs = im.load()
    for y in range(80, H):
        for x in range(W):
            d = (x - cx) ** 2 + (y - cy) ** 2
            if d <= r * r:
                n = math.sin(x * 0.05) + math.sin(y * 0.09 + x * 0.02) + math.sin(x * 0.013 - y * 0.05)
                c = 'land' if n > 0.6 else ('landS' if n > 0.4 else 'sea')
                if n < -1.4: c = 'cloud'
                if d > (r - 3) ** 2: c = 'cyan'
                pxs[x, y] = P[c]
            elif d <= (r + 2) ** 2 and BAYER[y % 4][x % 4] < 8:
                pxs[x, y] = P['cyanS']
    return im

VENUES = [
 dict(key='temple', name='절간', cap=6, bg=venue_temple),
 dict(key='concert', name='콘서트장', cap=9, bg=venue_concert),
 dict(key='opera', name='오페라홀', cap=10, bg=venue_opera),
 dict(key='orchestra', name='오케스트라홀', cap=13, bg=venue_orchestra),
 dict(key='court', name='법원', cap=23, bg=venue_court),
 dict(key='comedy', name='웃음 극장', cap=32, bg=venue_comedy),
 dict(key='stadium', name='야구장', cap=35, bg=venue_stadium),
 dict(key='savanna', name='아프리카 초원', cap=39, bg=venue_savanna),
 dict(key='seoul', name='서울', cap=49, bg=venue_seoul),
 dict(key='earth', name='지구', cap=59, bg=venue_earth),
]

# ================= new icons (12x12) =================
def icons2():
    out = {}
    out['icon_venue'] = grid(["............", ".....oo.....", "....oRRo....", "...oRRRRo...", "..oRRRRRRo..", ".oooooooooo.", "..oWWWWWWo..", "..oWdWWdWo..", "..oWdWWdWo..", "..oWWWWWWo..", ".oooooooooo.", "............"],
                             {'o': 'ink', 'R': 'roof', 'W': 'wall', 'd': 'pill'})
    out['icon_band'] = grid(["........oo..", ".......oso..", "......oo....", ".....oo.....", "..oooo......", ".oRRRo......", "oRRRRRo.....", "oRRwRRo.....", ".oRRRo......", "..ooo.......", "............", "............"],
                            {'o': 'ink', 'R': 'redS', 'w': 'shirt', 's': 'steel'})
    out['icon_cheat'] = grid(["............", "....oooo....", "...oyyyyo...", "..oyyooyyo..", "..oyo..oyo..", "..oyyooyyo..", "...oyyyyo...", "....oyyo....", "....oyyo....", "....oyyo....", "....oooo....", "............"],
                             {'o': 'ink', 'y': 'yel'})
    return out
