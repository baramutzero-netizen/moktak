"""Synthesised sounds: 목탁 (wood block), 나무아미타불 chant syllables (source-filter voice),
풍경 wind-bell for purchases, 범종 temple bell for the ending."""
import numpy as np
from scipy.signal import lfilter, butter
import wave, os

SR = 44100
rng = np.random.default_rng(3)
OUT = 'snd'
os.makedirs(OUT, exist_ok=True)

def save(name, x, gain=0.9):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    pcm = (x * 32767).astype('<i2')
    with wave.open(f'{OUT}/{name}.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def t_(dur): return np.arange(int(SR * dur)) / SR

def reverb(x, dur=1.2, decay=3.5, mix=0.25, seed=0):
    r = np.random.default_rng(seed)
    n = int(SR * dur)
    ir = r.standard_normal(n) * np.exp(-decay * np.arange(n) / SR * 3)
    b, a = butter(2, 3500 / (SR / 2))
    ir = lfilter(b, a, ir); ir[: int(SR * 0.012)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = np.convolve(x, ir)[: len(x) + n]
    wet = np.pad(wet, (0, len(x) + n - len(wet)))
    dry = np.concatenate([x, np.zeros(n)])
    return dry + mix * wet

def trim(x, thresh=1e-3):
    idx = np.where(np.abs(x) > thresh * np.max(np.abs(x)))[0]
    return x[: idx[-1] + 1] if len(idx) else x

# ---------------- 목탁: hollow wooden fish ----------------
def moktak(pitch=1.0, seed=0):
    r = np.random.default_rng(seed)
    t = t_(0.5)
    modes = [(395, 1.0, 0.10), (612, 0.8, 0.060), (1490, 0.35, 0.030), (2730, 0.18, 0.016), (4100, 0.08, 0.010)]
    x = np.zeros_like(t)
    for f, a, d in modes:
        f *= pitch * (1 + r.uniform(-0.01, 0.01))
        x += a * np.sin(2 * np.pi * f * t + r.uniform(0, 6)) * np.exp(-t / d)
    # strike transient: short filtered noise click
    n = r.standard_normal(len(t)) * np.exp(-t / 0.004)
    b, a = butter(2, [900 / (SR / 2), 6000 / (SR / 2)], 'band')
    x += 0.6 * lfilter(b, a, n)
    # attack ramp of 1 ms to avoid DC click
    x[: 44] *= np.linspace(0, 1, 44)
    return trim(reverb(x, 0.8, 4.0, 0.18, seed))

# ---------------- chant voice ----------------
def resonator(x, f, bw):
    """2-pole resonator with time-varying f (array) and bw (scalar), sample by sample in blocks."""
    y = np.zeros_like(x)
    blk = 64
    y1 = y2 = 0.0
    for s in range(0, len(x), blk):
        fc = f[s]
        R = np.exp(-np.pi * bw / SR)
        a1 = 2 * R * np.cos(2 * np.pi * fc / SR); a2 = -R * R
        g = 1 - a1 - a2  # Klatt-style unity gain at DC, so resonators can be cascaded
        seg = x[s:s + blk]
        out = np.empty_like(seg)
        for i, v in enumerate(seg):
            o = g * v + a1 * y1 + a2 * y2
            y2, y1 = y1, o
            out[i] = o
        y[s:s + blk] = out
    return y

VOWEL = {  # F1, F2, F3 (adult male, Korean vowels)
    'a': (720, 1200, 2500), 'u': (330, 820, 2350), 'i': (290, 2150, 2950),
    'n': (260, 1600, 2600), 'm': (260, 1100, 2400), 'l': (360, 1350, 2700), 'o': (450, 850, 2500),
}

def segs_to_track(segs, total):
    """segs: list of (time, (F1,F2,F3)) keyframes -> per-sample formant tracks."""
    n = int(SR * total)
    ts = np.array([s[0] for s in segs]) * SR
    out = []
    for k in range(3):
        vals = np.array([s[1][k] for s in segs])
        out.append(np.interp(np.arange(n), ts, vals))
    return out

def voice_source(n, f0, seed):
    r = np.random.default_rng(seed)
    t = np.arange(n) / SR
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.2 * t) + 0.004 * r.standard_normal(n).cumsum() / np.sqrt(n)
    f = f0 * vib
    ph = np.cumsum(f / SR)
    saw = 2 * (ph % 1) - 1
    # soften: glottal-ish spectrum tilt
    b, a = butter(1, 1800 / (SR / 2))
    src = lfilter(b, a, saw)
    src += 0.02 * r.standard_normal(n)  # breath
    return src

def syllable(cons, vowel, coda=None, dur=0.42, f0=108, f0_end=None, seed=0):
    n = int(SR * dur)
    f0_end = f0_end or f0
    # formant keyframes
    V = VOWEL[vowel]
    segs = []
    amp = np.ones(n)
    t = np.arange(n) / SR
    if cons in ('n', 'm'):
        segs += [(0, VOWEL[cons]), (0.07, VOWEL[cons]), (0.13, V)]
        amp *= np.where(t < 0.08, 0.45, 1.0)
    elif cons in ('t', 'b'):
        segs += [(0, V)]
    else:
        segs += [(0, V)]
    if coda == 'l':
        segs += [(dur - 0.16, V), (dur - 0.07, VOWEL['l']), (dur, VOWEL['l'])]
    else:
        segs += [(dur, V)]
    F = segs_to_track(segs, dur)
    f0s = np.linspace(f0, f0_end, n)
    # source with varying pitch
    r = np.random.default_rng(seed)
    ph = np.cumsum(f0s * (1 + 0.012 * np.sin(2 * np.pi * 5.0 * t)) / SR)
    saw = 2 * (ph % 1) - 1
    src = saw + 0.02 * r.standard_normal(n)
    src = np.diff(src, prepend=0) * 0.15 + lfilter([1], [1, -0.97], np.diff(src, prepend=0)) * 0.02  # glottal tilt
    y = resonator(src, F[0], 80)
    y = resonator(y, F[1], 100)
    y = resonator(y, F[2], 150)
    y = resonator(y, np.full(n, 3400.0), 250)
    hb, ha = butter(1, 120 / (SR / 2), 'high')
    y = lfilter(hb, ha, y)
    # envelopes
    env = np.ones(n)
    att = int(0.03 * SR); rel = int(0.12 * SR)
    if cons == 't':
        # aspirated ㅌ: silence-ish closure, burst + breathy onset
        clo = int(0.035 * SR)
        env[:clo] = 0
        burst = r.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / (0.012 * SR))
        bb, ba = butter(2, [2500 / (SR / 2), 7000 / (SR / 2)], 'band')
        burst = lfilter(bb, ba, burst) * 0.35
        att_s = clo + int(0.04 * SR)
        env[clo:att_s] = np.linspace(0, 1, att_s - clo) ** 2
    elif cons == 'b':
        clo = int(0.02 * SR)
        env[:clo] = 0
        env[clo:clo + att] = np.linspace(0, 1, att)
        burst = None
    else:
        env[:att] = np.linspace(0, 1, att)
        burst = None
    env[-rel:] *= np.linspace(1, 0, rel)
    y = y * env * amp
    if cons == 't':
        y[clo:clo + len(burst)] += burst * np.max(np.abs(y))
    return y

def chant_syllables():
    # 나 무 아 미 타 불 — monotone reciting pitch, slight fall on 불
    spec = [('na', 'n', 'a', None, 0.36, 110, 110), ('mu', 'm', 'u', None, 0.36, 110, 108),
            ('a', '', 'a', None, 0.34, 108, 110), ('mi', 'm', 'i', None, 0.36, 110, 110),
            ('ta', 't', 'a', None, 0.36, 112, 110), ('bul', 'b', 'u', 'l', 0.62, 110, 96)]
    outs = {}
    for i, (nm, c, v, coda, d, f0, f1) in enumerate(spec):
        y = syllable(c, v, coda, d, f0, f1, seed=i)
        y = reverb(y, 1.4, 2.6, 0.35, seed=10 + i)
        outs[nm] = trim(y, 2e-3)
    return outs

# ---------------- 풍경 (wind bell) ----------------
def pungyeong(seed=0):
    r = np.random.default_rng(seed)
    t = t_(1.6)
    base = 1320 * r.uniform(0.97, 1.03)
    x = np.zeros_like(t)
    for ratio, a, d in [(1, 1, 0.9), (2.76, 0.5, 0.45), (5.4, 0.25, 0.25), (8.93, 0.12, 0.12)]:
        x += a * np.sin(2 * np.pi * base * ratio * t) * np.exp(-t / d)
    x *= 1 + 0.15 * np.sin(2 * np.pi * 4 * t)
    x[:30] *= np.linspace(0, 1, 30)
    return trim(reverb(x, 1.0, 3, 0.2, seed))

# ---------------- 범종 (temple bell) ----------------
def beomjong():
    t = t_(7.0)
    base = 72.0
    x = np.zeros_like(t)
    for ratio, a, d in [(0.5, 0.7, 4.5), (1, 1, 3.8), (1.19, 0.6, 3.0), (1.5, 0.45, 2.4), (2.0, 0.4, 2.0),
                        (2.52, 0.3, 1.4), (3.0, 0.2, 1.0), (4.1, 0.12, 0.6)]:
        # slight detune pairs -> characteristic 맥놀이 (beating) of Korean bells
        x += a * (np.sin(2 * np.pi * base * ratio * t) + np.sin(2 * np.pi * (base * ratio + 0.9) * t)) * np.exp(-t / d)
    hit = rng.standard_normal(len(t)) * np.exp(-t / 0.02)
    b, a = butter(2, 600 / (SR / 2))
    x += 0.8 * lfilter(b, a, hit)
    x[:200] *= np.linspace(0, 1, 200)
    return trim(reverb(x, 2.5, 1.2, 0.3, 99))

if __name__ == '__main__':
    for i, p in enumerate((1.0, 1.04, 0.96)):
        save(f'moktak{i}', moktak(p, i))
    for nm, y in chant_syllables().items():
        save(f'chant_{nm}', y, 0.8)
    for i in range(3):
        save(f'bell{i}', pungyeong(i), 0.6)
    save('beomjong', beomjong(), 0.9)
    # a stitched preview of one full 나무아미타불 phrase with taps
    parts = []
    syl = chant_syllables(); m = moktak(1.0, 0)
    for nm in ('na', 'mu', 'a', 'mi', 'ta', 'bul'):
        seg = np.zeros(int(SR * 0.42))
        s = syl[nm][: len(seg)] * 0.8
        seg[: len(s)] += s
        mm = m[: len(seg)]
        seg[: len(mm)] += mm * 0.9
        parts.append(seg)
    save('preview_phrase', np.concatenate(parts + [np.zeros(SR // 2)]))
    print(sorted(os.listdir(OUT)))
