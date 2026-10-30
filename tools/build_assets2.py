import json, base64, io, os, subprocess, shutil
from art2 import *
from art import ICONS, icon_image, COW_TYPES
from aseprite import write_aseprite, read_aseprite

for d in ('ase', 'png'):
    if os.path.isdir(d): shutil.rmtree(d)
    os.makedirs(d)
PALETTE = list(dict.fromkeys(P.values()))
manifest = {}
def emit(name, frames, durations=None, tags=None, sub=''):
    w, h = frames[0].size
    os.makedirs(f'ase/{sub}', exist_ok=True); os.makedirs(f'png/{sub}', exist_ok=True)
    path = f'ase/{sub}{name}.aseprite'
    write_aseprite(path, frames, durations, tags, PALETTE)
    back, _ = read_aseprite(path)
    assert all(a.tobytes() == b.tobytes() for a, b in zip(back, frames)), name
    sheet = Image.new('RGBA', (w * len(frames), h), T)
    for i, f in enumerate(frames): sheet.paste(f, (i * w, 0))
    sheet.save(f'png/{sub}{name}.png')
    buf = io.BytesIO(); sheet.save(buf, 'PNG', optimize=True)
    manifest[name] = dict(w=w, h=h, n=len(frames), uri='data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode())

for v in VENUES: emit('bg_' + v['key'], [v['bg']()], sub='venues/')
emit('monk', [monk_image('up'), monk_image('down')], [160, 120], [('idle', 0, 0), ('strike', 0, 1)], 'monk/')
emit('moktak', [moktak_image(False), moktak_image(True)], [160, 80], [('idle', 0, 0), ('hit', 1, 1)], 'monk/')
emit('novice', [novice_image(False), novice_image(True)], [160, 120], [('play', 0, 1)], 'performers/')
emit('mini_moktak', [mini_moktak()], sub='performers/')
for k, fr in performers().items():
    emit(k, fr, [160, 120], [('play', 0, 1)], 'performers/')
for i, L in enumerate(LISTENERS):
    emit('L_' + L['key'], listener_frames(L), [400, 120, 160, 160],
         [('idle', 0, 0), ('blink', 1, 1), ('ear_in', 2, 2), ('ear_out', 3, 3)], 'listeners/%02d_' % i if False else 'listeners/')
sut = ['sut0', 'sut1', 'sut2', 'sut3', 'sut4', 'grn', 'blue', 'pur', 'red', 'org', 'teal', 'sut5']   # one ink colour per sutra tier (12)
emit('sutra', [glyph_image(g, c) for c in sut for g in range(4)], sub='fx/')
emit('karma', [karma_image(0), karma_image(1)], [150, 150], [('twinkle', 0, 1)], 'fx/')
emit('halo', [halo_image()], sub='fx/'); emit('lotus', [lotus_image()], sub='fx/')
for k in ICONS: emit('icon_' + k, [icon_image(k)], sub='icons/')
for k, im in icons2().items(): emit(k, [im], sub='icons/')

chars = "0123456789+.,×!" + "만억조경해자양구간정재극항하사아승기나유타불가의무량대수" + "탁"
idx = json.load(open('chant_index.json'))
chars += ''.join({k[0] for k in idx['syl']})
glyphs = bdf_glyphs('package/dist/Galmuri7.bdf', ''.join(set(chars)))
assert not (set(chars) - set(glyphs)), set(chars) - set(glyphs)
# other languages: chant characters, number units, onomatopoeia (kept when the pixel font has them)
I18N = json.load(open('i18n.json'))
extra = set(json.dumps(I18N['chant'], ensure_ascii=False)) | set('万億兆京垓秭穣溝澗正載極恒河沙阿僧祇那由他不可思議無量大数萬穰恆數亿沟涧载极议无KMBTQaiSxpOcNoDUVgdeh') | set('ポク!tok')
glyphs.update(bdf_glyphs('package/dist/Galmuri7.bdf', ''.join(c for c in extra if c not in glyphs)))

sounds = {}
os.makedirs('snd_mp3', exist_ok=True)
for f in sorted(os.listdir('snd')):
    name = f[:-4]; mp3 = f'snd_mp3/{name}.mp3'
    br = '96k' if name.startswith(('op_', 'beomjong', 'm_chord', 's_jing', 'c_', 'j_obj', 'h_')) else '64k'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'snd/{f}', '-ac', '1', '-ar', '44100', '-b:a', br, mp3], check=True)
    sounds[name] = 'data:audio/mpeg;base64,' + base64.b64encode(open(mp3, 'rb').read()).decode()

json.dump(dict(sprites=manifest, font=glyphs, sounds=sounds), open('assets2.json', 'w'))
data = dict(
    listeners=[dict(key=L['key'], name=L['name'], tag=L['tag'], v=L['v']) for L in LISTENERS],
    venues=[dict(key=v['key'], name=v['name'], cap=v['cap']) for v in VENUES],
    chant=idx, balance=json.load(open('balance3.json')))
json.dump(data, open('gamedata.json', 'w'), ensure_ascii=False)
print(len(manifest), 'sprites;', len(sounds), 'sounds;', os.path.getsize('assets2.json') // 1024, 'KB')
