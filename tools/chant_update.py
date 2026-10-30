"""Update the recitation script and synthesise only the syllables that are new."""
import json, os
import sound2
from sound import save, reverb, trim

LINES = [
    ('염불', '나무아미타불'),
    ('천수경', '수리수리 마하수리 수수리 사바하'),
    ('반야심경', '색즉시공 공즉시색'),
    ('금강경', '응무소주 이생기심'),
    ('아미타경', '극락세계 무량광불'),
    ('지장경', '지장보살 마하살'),
    ('관음경', '나무 관세음보살'),
    ('법구경', '제악막작 중선봉행'),
    ('법화경', '나무묘법연화경'),
    ('능엄경', '다냐타 옴 아나례 비사제'),
    ('화엄경', '일체유심조'),
    ('열반경', '제행무상 시생멸법'),
]
idx = json.load(open('chant_index.json'))
syl = {} if os.environ.get('REGEN') else idx['syl']
n_new = 0
for _, line in LINES:
    for w in line.split():
        for i, ch in enumerate(w):
            last = i == len(w) - 1
            key = ch + ('_' if last else '')
            if key in syl: continue
            f0a, f0b, vd = (112, 110, 0.17) if not last else (110, 98, 0.30)
            y = sound2.syllable(ch, f0a, f0b, vd, seed=len(syl))
            y = trim(reverb(y, 1.3, 2.6, 0.32, seed=len(syl)), 2e-3)
            name = 'c_%04x%s' % (ord(ch), 'e' if last else '')
            save(name, y, 0.8); syl[key] = name; n_new += 1
# keep only syllables that the script still uses
used = {ch + ('_' if i == len(w) - 1 else '') for _, line in LINES for w in line.split() for i, ch in enumerate(w)}
for k in list(syl):
    if k not in used:
        p = f"snd/{syl[k]}.wav"
        if os.path.exists(p): os.remove(p)
        del syl[k]
json.dump(dict(lines=LINES, syl=syl), open('chant_index.json', 'w'), ensure_ascii=False)
# courtroom voice: "이의 있음!" — a sharper, higher, faster delivery
import numpy as np
parts = [sound2.syllable(c, f, f2, d, seed=90 + k, vib=0.004) for k, (c, f, f2, d) in enumerate([('이', 150, 160, 0.10), ('의', 165, 170, 0.12), ('있', 175, 170, 0.08), ('음', 170, 120, 0.22)])]
gap = np.zeros(int(sound2.SR * 0.015))
v = np.concatenate([np.concatenate([p, gap]) for p in parts])
save('j_objection', trim(reverb(v, 1.2, 2.2, 0.28, seed=91), 2e-3), 0.85)
print('new syllables', n_new, 'total', len(syl))
