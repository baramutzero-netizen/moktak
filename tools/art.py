"""소 귀에 경 읽기 — pixel art. Every sprite is authored at 1 game-pixel = 1 image pixel,
so when the game scales the whole 320x180 scene by an integer factor every dot stays the same size."""
from PIL import Image
import random

def hx(s, a=255):
    s = s.lstrip('#'); return (int(s[0:2],16), int(s[2:4],16), int(s[4:6],16), a)

# ---- master palette (shared by every sprite; also embedded in each .aseprite) ----
PAL = {
 'ink':'#2a1e26', 'ink2':'#45333d',
 'skin':'#f1c49c', 'skinS':'#d4946e', 'blush':'#e88a7a',
 'robe':'#9c9cab', 'robeS':'#6c6c7f', 'robeL':'#c3c3cc',
 'kasa':'#a8473a', 'kasaS':'#7a2f2c', 'kasaL':'#cf6a4c',
 'wood':'#c97f3d', 'woodS':'#8c4f22', 'woodL':'#eab46a', 'woodD':'#5e3218',
 'hw':'#c8823c', 'hwS':'#985826', 'hwL':'#e8ad5c',
 'milk':'#f1ede2', 'milkS':'#c9c2b4',
 'blk':'#3b3239', 'blkS':'#272027', 'blkL':'#5f4f59',
 'buf':'#66707b', 'bufS':'#474f5a', 'bufL':'#8a96a0',
 'yak':'#6b4831', 'yakS':'#4a3022', 'yakL':'#93694a',
 'wht':'#fbf6ea', 'whtS':'#ddd2bf', 'gold':'#f3c34f', 'goldS':'#c98a2a', 'goldL':'#fff0a8',
 'muz':'#e9a0a0', 'muzS':'#c27580', 'ear':'#e78a92',
 'horn':'#efe2c0', 'hornS':'#bba57d', 'hoof':'#3d3236',
 'sky0':'#f6d9b4', 'sky1':'#f2c39b', 'sky2':'#a9c4d6', 'sky3':'#7fa6c4',
 'mtn0':'#8fa2b8', 'mtn1':'#6c8299', 'mtn2':'#4f6a75',
 'grs0':'#7fa35a', 'grs1':'#5f8646', 'grs2':'#456b38', 'grsL':'#a6c46e',
 'dirt':'#c9a477', 'dirtS':'#a7835a',
 'roof':'#4b4f5f', 'roofL':'#6c7184', 'roofS':'#33363f',
 'pill':'#b5473b', 'dan':'#3f8f7a', 'danL':'#6cc0a4', 'wall':'#efe4cf',
 'pine':'#3e6b4c', 'pineS':'#2c4f3a', 'bark':'#6a4a3a',
 'stone':'#b7b2a6', 'stoneS':'#8d887f',
 'k0':'#fff7d6', 'k1':'#ffd75e', 'k2':'#f5a63a',
 'lotus':'#f6a6be', 'lotusS':'#d97497', 'lotusL':'#ffe0ea', 'leaf':'#5f9c6a',
 'smoke':'#d9d4e0',
 'sut0':'#3a2a2e', 'sut1':'#2d6a8f', 'sut2':'#7a3f9a', 'sut3':'#b23a3a', 'sut4':'#c98a12', 'sut5':'#f7f0ff',
}
P = {k: hx(v) for k, v in PAL.items()}
T = (0, 0, 0, 0)

def grid(rows, cmap):
    h = len(rows); w = max(len(r) for r in rows)
    im = Image.new('RGBA', (w, h), T)
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and c != ' ':
                im.putpixel((x, y), P[cmap[c]])
    return im

def mirror_rows(half, swap=None):
    out = []
    for r in half:
        rr = r[::-1]
        if swap: rr = ''.join(swap.get(c, c) for c in rr)
        out.append(r + rr)
    return out

def put(rows, x, y, ch):
    r = list(rows[y]); r[x] = ch; rows[y] = ''.join(r)

# ================= COW (front view, 24x24) =================
COW_HALF = [
 "............",
 "..o.........",
 ".oho........",
 ".ohHo.......",
 "..ohHo......",
 "...ohHoooooo",
 "....oHbbbbll",
 "ooo.obbbbbbl",
 "oiiiobbbbbbb",
 "oiiiobbewbbb",
 ".ooosbbeebbb",
 "..ooosbbbbbb",
 ".oSSosbbbbbb",
 ".oSSoobmmmmm",
 "oSSSosmmmmmm",
 "oSSSosmmmmnm",
 "oSSSSomMmmmm",
 "oSSSSSoMMMMM",
 "oSSSSSSooooo",
 "oSSSSSSSSSSS",
 "oSSSoSSSSSSS",
 ".oSSoSSSSoSS",
 ".oSSoSSSSoSS",
 ".okkooooooko",
]
COW_BASE = mirror_rows(COW_HALF, swap={'w': 'e'})
# make the right eye glint mirror correctly (glint on the inner-top of both eyes)

COW_TYPES = [
 # key, name, body, shade, light, extra
 dict(key='hanwoo', name='누렁소', b='hw', s='hwS', l='hwL', horn='horn', hornS='hornS'),
 dict(key='holstein', name='얼룩젖소', b='milk', s='milkS', l='milk', horn='horn', hornS='hornS', patch=True),
 dict(key='heuku', name='흑우', b='blk', s='blkS', l='blkL', horn='horn', hornS='hornS'),
 dict(key='buffalo', name='물소', b='buf', s='bufS', l='bufL', horn='stone', hornS='stoneS', bighorn=True),
 dict(key='yak', name='야크', b='yak', s='yakS', l='yakL', horn='horn', hornS='hornS', shaggy=True),
 dict(key='white', name='흰 소', b='wht', s='whtS', l='wht', horn='gold', hornS='goldS', holy=True),
]

def cow_rows(t, frame):
    rows = list(COW_BASE)
    if t.get('bighorn'):
        horns = [
         "........................",
         "........................",
         "o......................o",
         "ho....................oh",
         "Hho..................ohH",
         ".oHhoooooooooooooooohHo.",
        ]
        rows[0:6] = horns
        rows[6] = "....." + rows[6][5:19] + "....."
    if t.get('patch'):
        # holstein spots, painted with 'x' over body pixels
        spots = [(6,7),(7,7),(6,8),(15,6),(16,6),(16,7),(17,7),(2,15),(3,15),(2,16),(3,16),(4,17),
                 (18,19),(19,19),(20,19),(19,20),(20,20),(9,19),(10,19),(10,20),(14,22),(15,21)]
        for (x, y) in spots:
            if rows[y][x] in 'bSsl': put(rows, x, y, 'x')
    if t.get('shaggy'):
        for x in range(1, 23):
            y = 18 if x % 3 else 19
            if rows[y][x] in 'S': put(rows, x, y, 'f')
        for x in (9, 10, 11, 12, 13, 14):
            put(rows, x, 6, 'f')
        put(rows, 10, 7, 'f'); put(rows, 13, 7, 'f'); put(rows, 11, 7, 'f')
    # frames: 0 idle, 1 blink, 2 left ear up (scripture enters), 3 right ear up (scripture exits)
    if frame == 1:
        for x in (7, 8, 15, 16):
            put(rows, x, 9, 'b'); put(rows, x, 10, 'o')
    if frame in (2, 3):
        xs = range(0, 4) if frame == 2 else range(20, 24)
        for y in range(6, 11):
            for x in xs:
                put(rows, x, y, rows[y + 1][x] if y < 10 else '.')
        # wide happy eyes while the sutra passes through
        for x in (7, 8, 15, 16):
            put(rows, x, 9, 'o'); put(rows, x, 10, 'b')
    return rows

def cow_image(t, frame):
    cmap = {'o': 'ink', 'b': t['b'], 's': t['s'], 'S': t['s'], 'l': t['l'], 'h': t['horn'], 'H': t['hornS'],
            'i': 'ear', 'e': 'ink', 'w': 'k0', 'm': 'muz', 'M': 'muzS', 'n': 'ink', 'k': 'hoof',
            'x': 'blk', 'f': 'yakL'}
    if t.get('holy'):
        cmap['k'] = 'goldS'
    im = grid(cow_rows(t, frame), cmap)
    # glints: top-left pixel of each eye
    if frame in (0, 2, 3):
        for x in (8, 16):
            if frame == 0: im.putpixel((x, 9), P['k0'])
    return im

# ================= MONK (side view facing right, 32x28) =================
MONK = {
 'up': [
 "................................",
 "................................",
 "...........ooooo...........oo...",
 "..........okkkkko.........owWo..",
 ".........okkkkkkko.......owWWo..",
 ".........oKkkkkkkko.......owo...",
 ".........oKkkkkekkko.....owo....",
 ".........oKKkkkkkkko....owo.....",
 "..........oKkkkkcko....owo......",
 "...........oKKkkko....owo.......",
 "..........ooooooooo..owo........",
 ".........orrgggggggoowo.........",
 "........orRrrgggggokko..........",
 ".......ogRrrrggggGokKo..........",
 ".......ogGRrrrgggGgoo...........",
 ".......oggGRrrrggGgo............",
 "......ogggGgRrrrgGgo............",
 "......oggGgggRrrrGgo............",
 "......oggGggggRrrRo.............",
 ".....ogggGgggggRrRGo............",
 ".....oggGGgggggggRGgo...........",
 "....ooggGgggggggggGggoo.........",
 "...oggggggggggggggggggGo........",
 "..ogLLggggggggggggggggGGo.......",
 "..ogggggggggggggggggggGGo.......",
 "...oGGGGGGGGGGGGGGGGGGGo........",
 "....ooooooooooooooooooo.........",
 "................................",
 ],
}
# down frame: same body, mallet swung to strike the moktak (lower right)
MONK['down'] = [r for r in MONK['up']]
for y in range(2, 11):
    MONK['down'][y] = MONK['down'][y][:20] + "............"
MONK['down'][11] = ".........orrgggggggoo..........."
MONK['down'][12] = "........orRrrgggggokkoooo......."
MONK['down'][13] = ".......ogRrrrggggGokKowwwWo....."
MONK['down'][14] = ".......ogGRrrrgggGgoo.owWWo....."
MONK['down'][15] = ".......oggGRrrrggGgo...ooo......"
# chant mouth open on the down frame
MONK['down'][8] = "..........oKkkkkcko............."
def monk_image(f):
    rows = MONK[f]
    if f == 'down':
        rows = list(rows); put(rows, 17, 7, 'o')
    cmap = {'o':'ink','k':'skin','K':'skinS','c':'blush','e':'ink','g':'robe','G':'robeS','L':'robeL',
            'r':'kasa','R':'kasaS','w':'wood','W':'woodS'}
    return grid(rows, cmap)

# ================= MOKTAK (16x12) =================
MOKTAK = [
 "................",
 ".....oooooo.....",
 "...ooLLwwwwoo...",
 "..oLLwwwwwwwWo..",
 ".oLwwwwwwwwwwWo.",
 ".oLwwwwwwwwwwWo.",
 "oLwwwooooooowwWo",
 "owwwoDDDDDDDowWo",
 "owwwwoooooooowWo",
 ".oWwwwwwwwwwWWo.",
 "..ooWWWWWWWWoo..",
 "....oooooooo....",
]
def moktak_image(hit=False):
    rows = list(MOKTAK)
    im = grid(rows, {'o':'ink','w':'wood','W':'woodS','L':'woodL','D':'woodD'})
    if hit:  # squash 1px + bright flash on top
        out = Image.new('RGBA', im.size, T)
        out.paste(im.crop((0, 0, 16, 5)), (0, 1))
        out.paste(im.crop((0, 5, 16, 12)), (0, 5))
        for x in range(5, 11): out.putpixel((x, 2), P['k0'])
        return out
    return im

# ================= NOVICE MONK 동자승 (16x16, facing right) =================
NOVICE_UP = [
 "................",
 ".....oooo.......",
 "....okkkko......",
 "...okkkkkko.....",
 "...oKkkekko..o..",
 "...oKkkkkcko.wo.",
 "....oKkkkko.ow..",
 "....oooooooow...",
 "...ogrrgggokko..",
 "..oggRrrggok.o..",
 "..ogggRrrgo.....",
 ".ogggggRrgo.....",
 ".ogggggggggo....",
 ".oLggggggggo....",
 "..oGGGGGGGo.....",
 "...ooooooo......",
]
NOVICE_DOWN = list(NOVICE_UP)
NOVICE_DOWN[4] = "...oKkkekko....."
NOVICE_DOWN[5] = "...oKkkkkcko...."
NOVICE_DOWN[6] = "....oKkkkko....."
NOVICE_DOWN[7] = "....ooooooo....."
NOVICE_DOWN[8] = "...ogrrgggokko.."
NOVICE_DOWN[9] = "..oggRrrggokKwo."
NOVICE_DOWN[10]= "..ogggRrrgo..ow."
def novice_image(down):
    rows = NOVICE_DOWN if down else NOVICE_UP
    return grid(rows, {'o':'ink','k':'skin','K':'skinS','c':'blush','e':'ink','g':'robe','G':'robeS',
                       'L':'robeL','r':'kasa','R':'kasaS','w':'wood'})
MINI_MOKTAK = [
 "..oooo..",
 ".owwwwo.",
 "owoooowo",
 "owwwwwWo",
 ".oWWWWo.",
 "..oooo..",
]
def mini_moktak():
    return grid(MINI_MOKTAK, {'o':'ink','w':'wood','W':'woodS'})

# ================= SUTRA GLYPHS (7x7) — tiny stylised 경 characters =================
GLYPHS = [
 ["ooooooo","..o.o..",".ooooo.","..o.o..","ooooooo","...o...","..ooo.."],
 ["o.ooooo","o...o..","ooo.o..","o..ooo.","o...o..","o.o.o.o","oo..ooo"],
 ["ooo.ooo","o.o.o.o","ooo.ooo","...o...","ooooooo","..o.o..",".o...o."],
 ["...o...","ooooooo","o.....o",".ooooo.","..o.o..",".o.o.o.","o..o..o"],
]
def glyph_image(gi, color):
    im = Image.new('RGBA', (9, 9), T)
    rows = GLYPHS[gi]
    # 1px soft outline (light) so the ink shows on any background
    halo = P['k0'] if color not in ('sut5',) else P['ink']
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == 'o':
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    xx, yy = x+1+dx, y+1+dy
                    if im.getpixel((xx, yy))[3] == 0: im.putpixel((xx, yy), (*halo[:3], 255))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == 'o': im.putpixel((x+1, y+1), P[color])
    return im

# ================= KARMA ORB (7x7, 2 frames) =================
KARMA = [
 ["...a...","..aba..",".abcba.","abcccba",".abcba.","..aba..","...a..."],
 ["...c...","...b...","..bab..","cbacabc","..bab..","...b...","...c..."],
]
def karma_image(f):
    return grid(KARMA[f], {'a':'k2','b':'k1','c':'k0'})

# ================= HALO & LOTUS (ending) =================
HALO = [
 "....oooooooo....",
 "..oo........oo..",
 ".o............o.",
 "..oo........oo..",
 "....oooooooo....",
]
def halo_image():
    return grid(HALO, {'o':'gold'})
LOTUS = [
 ".......pp.......",
 "......pLLp......",
 "..pp..pLLp..pp..",
 ".pLLp.pLLp.pLLp.",
 ".pLLppSLLSppLLp.",
 "..pSLpSLLSpLSp..",
 "gg.ppSSppSSpp.gg",
 ".gggggggggggggg.",
]
def lotus_image():
    return grid(LOTUS, {'p':'lotus','L':'lotusL','S':'lotusS','g':'leaf'})

# ================= ICONS (12x12) =================
ICONS = {
 'moktak': (["............","....oooo....","..ooLwwwoo..",".oLwwwwwwWo.",".owwoooowWo.","owwoDDDDowWo","owwwooooowWo",".oWwwwwwWWo.","..ooWWWWoo..","....oooo....","............","............"],
            {'o':'ink','w':'wood','W':'woodS','L':'woodL','D':'woodD'}),
 'sutra': (["............","..oooooooo..",".oyyyyyyyyo.",".oyiyiyiyyo.",".oyiyiyiyyo.",".oyiyiyiyyo.",".oyiyiyiyyo.",".oyyyyyyyyo.","oRoooooooooR","oRRRRRRRRRRo",".oooooooooo.","............"],
           {'o':'ink','y':'wall','i':'ink2','R':'kasa'}),
 'cow': (["o..........o","ho........oh",".ho.oooo.oh.","oooobbbboooo","oiiobebboiio",".oobbbbbboo.","...bmmmmb...","...ommnmmo..","....oMMMo...",".....ooo....","............","............"],
         {'o':'ink','h':'horn','b':'hw','i':'ear','e':'ink','m':'muz','M':'muzS','n':'ink'}),
 'novice': (["....oooo....","...okkkko...","..okkekkko..","..oKkkkcko..","...oKkkko...","...oooooo...","..ogrrggo...",".oggRrrggo..",".ogggRrggo..","oLgggggggGo.",".oGGGGGGGo..","..ooooooo..."],
            {'o':'ink','k':'skin','K':'skinS','c':'blush','e':'ink','g':'robe','G':'robeS','L':'robeL','r':'kasa','R':'kasaS'}),
 'earpick': (["..........o.","........oowo","......oowwo.",".....owwo...","....owwo....","...owwo.....","..owwo......",".owwo.......",".owo........","ow.o........","owwo........",".oo........."],
             {'o':'ink','w':'woodL'}),
 'incense': (["....s.......",".....s.s....","....s.s.....",".....s......",".....r......",".....w......",".....w......","..oooooooo..",".ogGGgGGgGo.",".ogggggggGo.","..oGGGGGGo..","...oooooo..."],
             {'o':'ink','s':'smoke','r':'k2','w':'woodS','g':'gold','G':'goldS'}),
 'lotus': (["............",".....pp.....","....pLLp....",".pp.pLLp.pp.","pLLppLLppLLp",".pSLpSSpLSp.","..pSSppSSp..","g..pppppp..g",".gggggggggg.","............","............","............"],
           {'p':'lotus','L':'lotusL','S':'lotusS','g':'leaf'}),
}
def icon_image(name):
    rows, cmap = ICONS[name]
    return grid(rows, cmap)

# ================= BACKGROUND (320x180) =================
BAYER = [[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def background():
    W, H = 320, 180
    im = Image.new('RGBA', (W, H), P['sky0'])
    px = im.load()
    rnd = random.Random(7)
    sky = ['sky3', 'sky2', 'sky1', 'sky0']
    # dithered sky gradient top->horizon
    for y in range(0, 110):
        t = y / 110 * (len(sky) - 1)
        i = min(int(t), len(sky) - 2); f = t - i
        for x in range(W):
            px[x, y] = P[sky[i + 1]] if f * 16 > BAYER[y % 4][x % 4] else P[sky[i]]
    # sun disc behind mountains
    cx, cy, r = 232, 70, 16
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                px[x, y] = P['k0']
    # three mountain layers (pixel-stepped ridgelines)
    def ridge(base, amp, freq, seed, col, shade=None):
        rr = random.Random(seed)
        ph = [rr.uniform(0, 6.28) for _ in range(3)]
        import math
        prev = None
        for x in range(W):
            h = base - amp * (0.55 * math.sin(x * freq + ph[0]) + 0.3 * math.sin(x * freq * 2.3 + ph[1]) + 0.15 * math.sin(x * freq * 5.1 + ph[2]))
            h = int(h)
            for y in range(max(0, h), 120):
                px[x, y] = P[col]
            if shade and prev is not None and h > prev:  # light on left slopes
                pass
            prev = h
    ridge(72, 18, 0.025, 1, 'mtn0')
    ridge(88, 14, 0.035, 2, 'mtn1')
    ridge(100, 8, 0.05, 3, 'mtn2')
    # ground
    for y in range(104, H):
        for x in range(W):
            t = (y - 104) / (H - 104)
            c = 'grs0' if t < 0.35 else ('grs1' if t < 0.75 else 'grs2')
            if t >= 0.3 and t < 0.4 and BAYER[y % 4][x % 4] < 8: c = 'grs1'
            if t >= 0.7 and t < 0.8 and BAYER[y % 4][x % 4] < 8: c = 'grs2'
            px[x, y] = P[c]
    # horizon highlight line
    for x in range(W):
        px[x, 104] = P['grsL']
    # grass tufts
    for _ in range(140):
        x = rnd.randrange(2, W - 2); y = rnd.randrange(108, H - 2)
        c = P['grsL'] if y < 140 else P['grs0']
        px[x, y] = c; px[x - 1, y + 1] = c; px[x + 1, y + 1] = c
    # dirt clearing where the monk sits and the cows stand
    for y in range(118, 176):
        for x in range(W):
            # elliptical worn patch
            dx = (x - 200) / 125; dy = (y - 148) / 30
            if dx * dx + dy * dy <= 1:
                edge = dx * dx + dy * dy > 0.86
                if edge and BAYER[y % 4][x % 4] < 8: continue
                px[x, y] = P['dirt']
    for _ in range(60):
        x = rnd.randrange(90, 315); y = rnd.randrange(124, 172)
        dx = (x - 200) / 125; dy = (y - 148) / 30
        if dx * dx + dy * dy < 0.8: px[x, y] = P['dirtS']
    # ---- temple hall on the left ----
    # stone base
    for y in range(96, 106):
        for x in range(0, 92):
            px[x, y] = P['stoneS'] if y in (96, 105) or x % 12 == 0 else P['stone']
    # wall and pillars
    for y in range(64, 96):
        for x in range(4, 88):
            px[x, y] = P['wall']
    for x0 in (4, 30, 56, 82):
        for y in range(62, 96):
            for x in range(x0, x0 + 5):
                px[x, y] = P['pill'] if x != x0 + 4 else P['kasaS']
    # lattice doors
    for x0 in (11, 37, 63):
        for y in range(70, 96):
            for x in range(x0, x0 + 15):
                edge = x in (x0, x0 + 14) or y == 70
                lat = (x - x0) % 3 == 0 or (y - 70) % 3 == 0
                px[x, y] = P['woodS'] if edge else (P['wood'] if lat else P['wall'])
    # dancheong band under eaves
    for y in range(56, 64):
        for x in range(0, 92):
            c = 'dan' if (x // 4 + y // 4) % 2 == 0 else 'danL'
            if y in (56, 63): c = 'pill'
            px[x, y] = P[c]
    # curved giwa roof with upturned eaves
    import math
    for x in range(-6, 100):
        t = (x - 46) / 54
        lift = int(6 * t ** 4)
        bot = 57 - lift
        top = 34 + int(5 * abs(t)) - lift
        for y in range(max(0, top), bot):
            if 0 <= x < W:
                c = 'roof'
                if y == top: c = 'roofL'
                elif y >= bot - 2: c = 'roofS'
                elif x % 3 == 0: c = 'roofS'
                px[x, y] = P[c]
    for x in range(10, 84):  # ridge beam
        px[x, 33] = P['roofS']; px[x, 32] = P['roofL']
    # hanging plaque (현판)
    for y in range(58, 63):
        for x in range(38, 54):
            px[x, y] = P['ink'] if y in (58, 62) or x in (38, 53) else P['gold']
    # ---- pine tree on the right edge ----
    for y in range(40, 112):
        for x in range(304, 310):
            px[x, y] = P['bark'] if (x + y) % 5 else P['ink2']
    for cy2, cw in ((46, 18), (62, 22), (78, 20)):
        for y in range(cy2 - 7, cy2 + 5):
            for x in range(306 - cw, 320):
                d = ((x - 306) / cw) ** 2 + ((y - cy2) / 6) ** 2
                if d <= 1:
                    px[x, y] = P['pineS'] if y > cy2 + 1 or (x + y) % 7 == 0 else P['pine']
    # ---- stone lantern (석등) ----
    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1):
            for x in range(x0, x1): px[x, y] = P[c]
    rect(100, 92, 112, 95, 'stoneS'); rect(102, 95, 110, 103, 'stone'); rect(104, 97, 108, 101, 'k1')
    rect(100, 103, 112, 105, 'stoneS'); rect(104, 105, 108, 116, 'stone'); rect(101, 116, 111, 119, 'stoneS')
    rect(105, 89, 107, 92, 'stoneS')
    return im

# ================= PIXEL FONT (from Galmuri7 BDF) =================
def bdf_glyphs(path, chars):
    out = {}
    want = {ord(c) for c in chars}
    cur = None; bits = []; reading = False
    with open(path, encoding='latin-1') as f:
        for line in f:
            if line.startswith('ENCODING'):
                cur = int(line.split()[1])
            elif line.startswith('BBX'):
                bbx = list(map(int, line.split()[1:]))
            elif line.startswith('DWIDTH'):
                dw = int(line.split()[1])
            elif line.startswith('BITMAP'):
                reading = True; bits = []
            elif line.startswith('ENDCHAR'):
                reading = False
                if cur in want:
                    w, h, ox, oy = bbx
                    rows = []
                    for b in bits:
                        v = int(b, 16); nb = len(b) * 4
                        rows.append(''.join('1' if v >> (nb - 1 - i) & 1 else '0' for i in range(w)))
                    out[chr(cur)] = dict(w=w, h=h, ox=ox, oy=oy, dw=dw, rows=rows)
            elif reading:
                bits.append(line.strip())
    return out
