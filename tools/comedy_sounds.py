import numpy as np
from sound import save, reverb, trim, SR
import sound2
from sound2 import membrane, snare, crash, clap, bandnoise
r = np.random.default_rng(301)
# ba-dum-tss: low tom, high tom, cymbal
save('h_tom1', membrane(140, 0.12, 0.4, 302, 0.35), 0.8)
save('h_tom2', membrane(200, 0.10, 0.4, 303, 0.3), 0.8)
t = np.arange(int(SR * 1.2)) / SR
cym = bandnoise(len(t), 3500, 14000, 304) * np.exp(-t / 0.35)
save('h_tss', reverb(cym, 0.8, 3, 0.2, 305), 0.6)
# a laugh: "하하하하" falling, breathy
def laugh(f0, n, seed, speed=1.0):
    parts = []
    for k in range(n):
        f = f0 * (1 - 0.06 * k)
        y = sound2.syllable('하', f, f * 0.92, 0.07 / speed, seed=seed + k, vib=0.0)
        parts.append(y[: int(len(y) * 0.8)])
        parts.append(np.zeros(int(SR * 0.03 / speed)))
    return np.concatenate(parts)
save('h_haha', trim(reverb(laugh(190, 4, 310), 1.0, 3, 0.25, 311), 2e-3), 0.8)
# crowd laughter: several laughs at different pitches and offsets
L = int(SR * 1.8); crowd = np.zeros(L)
for k, (f0, n, off) in enumerate(((230, 5, 0.0), (150, 4, 0.08), (300, 6, 0.15), (180, 5, 0.22), (260, 4, 0.05))):
    y = laugh(f0, n, 320 + k * 10, 1.1 + 0.1 * k); s = int(off * SR)
    crowd[s:s + len(y)] += y[: L - s] * (0.8 + 0.2 * r.random())
save('h_crowd', trim(reverb(crowd, 1.4, 2.5, 0.3, 330), 2e-3), 0.75)
# applause: many claps scattered over 1.6 s
L = int(SR * 1.8); ap = np.zeros(L); c = clap()
for _ in range(90):
    s = int(r.uniform(0, 1.4) * SR); g = r.uniform(0.2, 0.6) * np.exp(-s / SR / 1.2)
    ap[s:s + len(c)] += c[: L - s] * g
save('h_applause', ap * np.minimum(1, (L / SR - np.arange(L) / SR) / 0.3), 0.6)
print('ok')
