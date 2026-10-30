"""v2 sounds: general Korean syllable chant synth, metal band kit, opera voices, stadium cheer kit.
Everything is synthesised; run once, outputs WAV files into snd/."""
import numpy as np
from scipy.signal import lfilter, butter
import wave, os, json
from sound import save, reverb, trim, moktak, pungyeong, beomjong, SR

OUT = 'snd'
R = np.random.default_rng(11)
t_ = lambda d: np.arange(int(SR * d)) / SR

# ---------------- fast time-varying resonator (block-wise lfilter) ----------------
def res_tv(x, f, bw, blk=32):
    """2-pole resonator, unity gain at DC. Constant frequency: one lfilter call.
    Moving frequency: coefficients updated every sample (block-wise updates caused audible clicks)."""
    f = np.asarray(f, dtype=float)
    Rr = np.exp(-np.pi * bw / SR)
    if np.ptp(f) < 1e-6:
        a1 = 2 * Rr * np.cos(2 * np.pi * f[0] / SR); a2 = -Rr * Rr
        return lfilter([1 - a1 - a2], [1, -a1, -a2], x)
    a1s = (2 * Rr * np.cos(2 * np.pi * f / SR)).tolist(); a2 = -Rr * Rr
    xs = x.tolist(); out = [0.0] * len(xs); y1 = y2 = 0.0
    for i, v in enumerate(xs):
        a1 = a1s[i]
        o = (1 - a1 - a2) * v + a1 * y1 + a2 * y2
        y2 = y1; y1 = o; out[i] = o
    return np.array(out)

def bandnoise(n, lo, hi, seed=0):
    r = np.random.default_rng(seed)
    b, a = butter(2, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], 'band')
    return lfilter(b, a, r.standard_normal(n))

def track(keys, n):
    keys = sorted(keys, key=lambda k: k[0])
    ts = [k[0] * SR for k in keys]
    for i in range(1, len(ts)):
        if ts[i] <= ts[i - 1]: ts[i] = ts[i - 1] + 1
    return np.interp(np.arange(n), ts, [k[1] for k in keys])

def glottal(f0track, seed=0, breath=0.02, tilt=0.97):
    r = np.random.default_rng(seed)
    ph = np.cumsum(f0track / SR)
    saw = 2 * (ph % 1) - 1
    d = np.diff(saw, prepend=0)
    d[np.abs(d) > 1] = 0                      # drop the wrap discontinuity, keep the pulse shape
    src = lfilter([1], [1, -tilt], -np.diff(saw, prepend=0)) * 0.03 + saw * 0.25
    return src + breath * r.standard_normal(len(src))

# ---------------- Korean syllable ----------------
VOW = {'a': (760, 1250, 2500), 'eo': (560, 960, 2450), 'o': (420, 780, 2400), 'u': (330, 860, 2300),
       'eu': (350, 1400, 2450), 'i': (290, 2200, 3000), 'e': (480, 1850, 2600)}
NAS = {'n': (260, 1650, 2600), 'm': (260, 1100, 2400), 'ng': (270, 2000, 2700)}
LIQ = (360, 1350, 2700)
MED = [('', 'a'), ('', 'e'), ('y', 'a'), ('y', 'e'), ('', 'eo'), ('', 'e'), ('y', 'eo'), ('y', 'e'), ('', 'o'),
       ('w', 'a'), ('w', 'e'), ('w', 'e'), ('y', 'o'), ('', 'u'), ('w', 'eo'), ('w', 'e'), ('w', 'i'), ('y', 'u'),
       ('', 'eu'), ('eu', 'i'), ('', 'i')]
INI = ['lax_k', 'tense_k', 'n', 'lax_t', 'tense_t', 'r', 'm', 'lax_p', 'tense_p', 's', 'ss', 'none',
       'lax_c', 'tense_c', 'asp_c', 'asp_k', 'asp_t', 'asp_p', 'h']
BAND = {'k': (1400, 3400), 't': (3000, 6500), 'p': (400, 1600), 'c': (2500, 6500)}
FIN = {0: None}
for i in (1, 2, 3, 9, 24): FIN[i] = 'stop'
for i in (4, 5, 6): FIN[i] = 'n'
for i in (7, 19, 20, 22, 23, 25, 27): FIN[i] = 'stop'
for i in (8, 11, 12, 13, 15): FIN[i] = 'l'
for i in (16, 10): FIN[i] = 'm'
for i in (17, 18, 14, 26): FIN[i] = 'stop'
FIN[21] = 'ng'

def decompose(ch):
    c = ord(ch) - 0xAC00
    return c // 588, (c % 588) // 28, c % 28

def syllable(ch, f0a=110, f0b=None, vdur=0.2, seed=0, fscale=1.0, vib=0.012, bw_scale=1.0):
    ini, med, fin = decompose(ch)
    kind = INI[ini]; glide, vow = MED[med]
    V = VOW[vow]
    start = {'y': VOW['i'], 'w': VOW['u'], 'eu': VOW['eu']}.get(glide, V)
    F, AV, AH, AF, bursts = [], [], [], [], []
    fband = (3800, 8000)
    if kind == 'none':
        onset = 0.0; AV += [(0, 0), (0.03, 1)]
    elif kind in ('n', 'm'):
        F += [(0, NAS[kind]), (0.06, NAS[kind])]; AV += [(0, 0), (0.015, 0.45), (0.06, 0.5), (0.1, 1)]; onset = 0.06
    elif kind == 'r':
        F += [(0, LIQ), (0.03, LIQ)]; AV += [(0, 0), (0.01, 0.45), (0.03, 0.4), (0.06, 1)]; onset = 0.03
    elif kind == 'h':
        AH += [(0, 0), (0.015, 0.7), (0.06, 0.45), (0.08, 0)]; AV += [(0, 0), (0.05, 0), (0.085, 1)]; onset = 0.05
    elif kind in ('s', 'ss'):
        L = 0.09 if kind == 's' else 0.13; A = 0.45 if kind == 's' else 0.6
        AF += [(0, 0), (0.02, A), (L - 0.012, A), (L + 0.005, 0)]; AV += [(0, 0), (L - 0.01, 0), (L + 0.03, 1)]; onset = L - 0.01
    else:
        typ, place = kind.split('_')
        band = BAND[place]
        if typ == 'lax':
            cl = 0.02; bursts.append((cl, band, 0.25)); AV += [(0, 0), (cl, 0), (cl + 0.04, 1)]; onset = cl
            F += [(cl, (250, start[1], start[2]))]
            if place == 'c': AF += [(cl, 0), (cl + 0.005, 0.35), (cl + 0.035, 0)]; fband = (2500, 6500)
        elif typ == 'tense':
            cl = 0.035; bursts.append((cl, band, 0.5)); AV += [(0, 0), (cl, 0), (cl + 0.015, 1)]; onset = cl
            if place == 'c': AF += [(cl, 0), (cl + 0.003, 0.4), (cl + 0.02, 0)]; fband = (2500, 6500)
        else:  # aspirated
            cl = 0.025; bursts.append((cl, band, 0.4))
            AH += [(0, 0), (cl, 0), (cl + 0.005, 0.7), (cl + 0.055, 0.3), (cl + 0.075, 0)]
            AV += [(0, 0), (cl + 0.05, 0), (cl + 0.08, 1)]; onset = cl + 0.05
            if place == 'c': AF += [(cl, 0), (cl + 0.005, 0.5), (cl + 0.06, 0)]; fband = (2500, 6500)
    F += [(onset, start)]
    gl = 0.0
    if glide == 'eu': gl = vdur * 0.45
    elif glide: gl = 0.06
    F += [(onset + gl, V)]
    te = onset + gl + vdur
    F += [(te, V)]
    kf = FIN[fin]
    if kf is None:
        AV += [(te, 1), (te + 0.09, 0)]; end = te + 0.09
    elif kf in NAS:
        F += [(te + 0.03, NAS[kf]), (te + 0.2, NAS[kf])]; AV += [(te, 1), (te + 0.03, 0.55), (te + 0.13, 0.5), (te + 0.2, 0)]; end = te + 0.2
    elif kf == 'l':
        F += [(te + 0.04, LIQ), (te + 0.18, LIQ)]; AV += [(te, 1), (te + 0.04, 0.7), (te + 0.12, 0.6), (te + 0.18, 0)]; end = te + 0.18
    else:
        F += [(te + 0.03, (250, V[1], V[2]))]; AV += [(te, 1), (te + 0.03, 0.3), (te + 0.035, 0)]; end = te + 0.06
    n = int(SR * (end + 0.02))
    t = np.arange(n) / SR
    f0b = f0b or f0a
    f0 = np.linspace(f0a, f0b, n) * (1 + vib * np.sin(2 * np.pi * 5.2 * t))
    av = track(AV, n); ah = track(AH, n) if AH else np.zeros(n); af = track(AF, n) if AF else np.zeros(n)
    r = np.random.default_rng(seed)
    src = glottal(f0, seed) * av + 0.35 * r.standard_normal(n) * ah
    Fs = [track([(k[0], k[1][j] * fscale) for k in F], n) for j in range(3)]
    y = res_tv(src, Fs[0], 80 * bw_scale)
    y = res_tv(y, Fs[1], 100 * bw_scale)
    y = res_tv(y, Fs[2], 150 * bw_scale)
    y = res_tv(y, np.full(n, 3400.0 * fscale), 250)
    hb, ha = butter(1, 100 / (SR / 2), 'high'); y = lfilter(hb, ha, y)
    peak = np.max(np.abs(y)) + 1e-9
    if AF:
        # sibilant: smooth, hissy 's' (two soft resonances around 5 and 7 kHz) instead of raw band noise
        wn = np.random.default_rng(seed + 3).standard_normal(n)
        lo_c, hi_c = (fband[0] + fband[1]) / 2 * 0.75, (fband[0] + fband[1]) / 2 * 1.15
        fn = 0.6 * res_tv(wn, np.full(n, lo_c), 1800) + 0.4 * res_tv(wn, np.full(n, hi_c), 2600)
        sb, sa = butter(2, 8500 / (SR / 2)); fn = lfilter(sb, sa, fn)
        sm = np.convolve(af, np.ones(int(0.006 * SR)) / int(0.006 * SR), 'same')     # smoother envelope
        y += sm * fn / (np.max(np.abs(fn)) + 1e-9) * peak * 0.3
    for (bt, band, amp) in bursts:
        k = int(bt * SR); L = int(0.012 * SR)
        b = bandnoise(L, *band, seed=seed + 7) * np.exp(-np.arange(L) / (0.003 * SR)) * np.minimum(1, np.arange(L) / (0.0008 * SR))   # soft attack: no broadband click
        y[k:k + L] += b[: len(y[k:k + L])] / (np.max(np.abs(b)) + 1e-9) * peak * amp
    lb, la = butter(2, 9000 / (SR / 2)); y = lfilter(lb, la, y)       # tame harsh top end
    y[:int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))         # no click at the very start
    return y

# ---------------- chant script ----------------
CHANT_LINES = [
    ('염불', '나무아미타불'),
    ('천수경', '수리수리 마하수리 수수리 사바하'),
    ('반야심경', '아제아제 바라아제 바라승아제 모지 사바하'),
    ('금강경', '여시아문 일시불'),
    ('아미타경', '극락세계 무량광불'),
    ('지장경', '지장보살 마하살'),
    ('법화경', '나무묘법연화경'),
    ('능엄경', '다냐타 옴 아나례 비사제'),
    ('화엄경', '대방광불화엄경'),
]

def chant_set():
    out = {}
    for _, line in CHANT_LINES:
        words = line.split()
        for w in words:
            for i, ch in enumerate(w):
                last = i == len(w) - 1
                key = ch + ('_' if last else '')
                if key in out: continue
                f0a, f0b, vd = (112, 110, 0.17) if not last else (110, 98, 0.30)
                y = syllable(ch, f0a, f0b, vd, seed=len(out))
                out[key] = trim(reverb(y, 1.3, 2.6, 0.32, seed=len(out)), 2e-3)
    return out

# ---------------- opera voices: sustained "아~" with vibrato + singer's formant ----------------
def opera(f0, fscale, dur=2.6, seed=0, vib=0.03):
    n = int(SR * dur); t = np.arange(n) / SR
    vibr = 1 + vib * np.sin(2 * np.pi * 5.6 * t) * np.clip(t / 0.5, 0, 1)
    f = f0 * vibr * (1 + 0.004 * np.sin(2 * np.pi * 0.7 * t))
    src = glottal(f, seed, breath=0.01, tilt=0.9)
    F1 = max(700 * fscale, f0 * 1.15)        # sopranos tune F1 up to the fundamental
    y = res_tv(src, np.full(n, F1), 110)
    y = res_tv(y, np.full(n, 1150 * fscale), 130)
    y = res_tv(y, np.full(n, 2600 * fscale), 180)
    y = res_tv(y, np.full(n, 3000.0), 300) * 1.0 + 0.6 * res_tv(src, np.full(n, 2900.0), 350)
    env = np.minimum(1, t / 0.18) * np.minimum(1, (dur - t) / 0.5)
    hb, ha = butter(1, 90 / (SR / 2), 'high')
    return trim(reverb(lfilter(hb, ha, y * env), 2.2, 1.6, 0.35, seed + 50))

# ---------------- metal band ----------------
def kick():
    t = t_(0.35); f = 45 + 110 * np.exp(-t / 0.03)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.14)
    x[:400] += bandnoise(400, 2000, 6000, 1) * 0.3 * np.exp(-np.arange(400) / 80)
    return np.tanh(2 * x)
def snare():
    t = t_(0.3)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    nz = bandnoise(len(t), 1200, 9000, 2) * np.exp(-t / 0.09)
    return reverb(tone * 0.8 + nz / np.max(np.abs(nz)) * 0.9, 0.6, 4, 0.15, 3)
def hat():
    t = t_(0.08); return bandnoise(len(t), 7000, 15000, 4) * np.exp(-t / 0.018)
def crash():
    t = t_(1.6); return bandnoise(len(t), 4000, 16000, 5) * np.exp(-t / 0.45)
def dist_saw(freqs, dur, mute=False, drive=14, seed=0, lp=4200):
    t = t_(dur); x = np.zeros_like(t)
    for f in freqs:
        for det in (-0.004, 0.004):
            x += 2 * ((f * (1 + det) * t + R.random()) % 1) - 1
    env = np.exp(-t / (0.07 if mute else 0.9)) * np.minimum(1, t / 0.003)
    y = np.tanh(drive * x / len(freqs) * env)
    b, a = butter(2, (1800 if mute else lp) / (SR / 2)); y = lfilter(b, a, y)
    hb, ha = butter(1, 90 / (SR / 2), 'high'); y = lfilter(hb, ha, y)
    fade = np.minimum(1, (dur - t) / 0.03)
    return y * fade
def bass():
    t = t_(0.32); f = 55.0
    x = 2 * ((f * t) % 1) - 1
    b, a = butter(2, 700 / (SR / 2)); x = lfilter(b, a, np.tanh(3 * x)) * np.exp(-t / 0.25)
    return x * np.minimum(1, (0.32 - t) / 0.02)
def lead():
    t = t_(0.5); f = 440 * (1 + 0.012 * np.sin(2 * np.pi * 6 * t) * np.clip((t - 0.1) / 0.2, 0, 1))
    x = 2 * ((np.cumsum(f) / SR) % 1) - 1
    y = np.tanh(10 * x) * np.exp(-t / 0.6) * np.minimum(1, t / 0.005)
    b, a = butter(2, 5000 / (SR / 2)); y = lfilter(b, a, y)
    return reverb(y * np.minimum(1, (0.5 - t) / 0.05), 1.0, 3, 0.25, 6)

# ---------------- stadium cheer kit ----------------
def whistle():
    t = t_(0.45); f = 2900 * (1 + 0.04 * np.sign(np.sin(2 * np.pi * 28 * t)))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.15 * bandnoise(len(t), 2500, 4000, 7)
    return x * np.minimum(1, t / 0.01) * np.minimum(1, (0.45 - t) / 0.05)
def clap():
    n = int(SR * 0.25); x = np.zeros(n)
    for k, d in enumerate((0, 0.009, 0.019, 0.03)):
        s = int(d * SR); L = n - s
        x[s:] += bandnoise(L, 900, 3500, 10 + k) * np.exp(-np.arange(L) / ((0.006 if k < 3 else 0.06) * SR))
    return reverb(x, 0.5, 4, 0.2, 9)
def pompom():
    t = t_(0.14); return bandnoise(len(t), 4500, 12000, 12) * np.sin(np.pi * t / 0.14) ** 2
def bigdrum():
    t = t_(0.6); f = 62 + 40 * np.exp(-t / 0.04)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.25)
    x += 0.4 * bandnoise(len(t), 150, 1200, 13) * np.exp(-t / 0.03)
    return reverb(x, 1.0, 2.5, 0.25, 14)
def trumpet():
    t = t_(0.42); f = 466.16 * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t))   # B♭4 base
    x = 2 * ((np.cumsum(f) / SR) % 1) - 1
    env = np.minimum(1, t / 0.03) * np.minimum(1, (0.42 - t) / 0.06)
    y = np.zeros_like(x); zi = np.zeros(2)
    for s in range(0, len(x), 64):        # brassy: cutoff follows the envelope
        fc = 600 + 4200 * env[s]
        b, a = butter(2, fc / (SR / 2))
        if s == 0: zi = np.zeros(max(len(a), len(b)) - 1)
        y[s:s + 64], zi = lfilter(b, a, x[s:s + 64] * env[s:s + 64], zi=zi)
    return reverb(y, 1.2, 2.5, 0.25, 15)

# ---------------- djembe ----------------
def membrane(f, decay, noise, seed, dur=0.5):
    t = t_(dur); fr = f * (1 + 0.3 * np.exp(-t / 0.01))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / decay)
    x += noise * bandnoise(len(t), 800, 7000, seed) / 3 * np.exp(-t / 0.015)
    x[:60] *= np.linspace(0, 1, 60)
    return reverb(x, 0.6, 3, 0.15, seed)

# ---------------- samulnori ----------------
def metal_hit(base, partials, decay, seed, dur, noise=0.3):
    t = t_(dur); x = np.zeros_like(t); r = np.random.default_rng(seed)
    for ratio, a in partials:
        x += a * np.sin(2 * np.pi * base * ratio * t + r.uniform(0, 6)) * np.exp(-t / (decay / ratio ** 0.5))
    x += noise * bandnoise(len(t), 2000, 10000, seed) / 3 * np.exp(-t / 0.01)
    x[:40] *= np.linspace(0, 1, 40)
    return x
def jing():
    t = t_(4.5); base = 118.0
    x = np.zeros_like(t)
    for ratio, a, d in [(1, 1, 2.6), (1.008, 0.8, 2.6), (2.01, 0.35, 1.4), (2.76, 0.25, 1.0), (3.9, 0.12, 0.6)]:
        x += a * np.sin(2 * np.pi * base * ratio * t) * np.exp(-t / d)
    env = 1 - np.exp(-t / 0.03)   # soft padded mallet swell
    return reverb(x * env, 1.5, 1.5, 0.25, 77)

# ---------------- orchestra ----------------
def strings(f0, dur, voices=5, seed=0, lp=3500, att=0.12):
    t = t_(dur); r = np.random.default_rng(seed); x = np.zeros_like(t)
    for v in range(voices):
        det = 1 + r.uniform(-0.006, 0.006); vib = 1 + 0.006 * np.sin(2 * np.pi * (5 + r.uniform(-.4, .4)) * t + r.uniform(0, 6))
        ph = np.cumsum(f0 * det * vib / SR) + r.random()
        x += 2 * (ph % 1) - 1
    b, a = butter(2, lp / (SR / 2)); x = lfilter(b, a, x / voices)
    x = res_tv(x, np.full(len(t), 900.0), 300) * 0.6 + x * 0.6
    env = np.minimum(1, t / att) * np.minimum(1, (dur - t) / 0.3)
    return reverb(x * env, 2.0, 1.6, 0.35, seed + 60)
def flute(f0, dur=0.5, seed=0):
    t = t_(dur); vib = 1 + 0.008 * np.sin(2 * np.pi * 5.5 * t)
    ph = np.cumsum(f0 * vib / SR)
    x = np.sin(2 * np.pi * ph) + 0.12 * np.sin(4 * np.pi * ph) + 0.08 * bandnoise(len(t), f0 * 0.8, f0 * 3, seed)
    env = np.minimum(1, t / 0.04) * np.minimum(1, (dur - t) / 0.12)
    return reverb(x * env, 1.6, 2.0, 0.3, seed + 70)
def horn(f0, dur=1.3, seed=0):
    t = t_(dur); ph = np.cumsum(f0 * (1 + 0.004 * np.sin(2 * np.pi * 5 * t)) / SR)
    x = 2 * (ph % 1) - 1
    env = np.minimum(1, t / 0.08) * np.minimum(1, (dur - t) / 0.3)
    b, a = butter(2, 900 / (SR / 2)); x = lfilter(b, a, x) * env
    return reverb(x, 1.8, 1.8, 0.35, seed + 80)
def timp(f0, seed=0):
    t = t_(1.4); fr = f0 * (1 + 0.04 * np.exp(-t / 0.05))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.55) + 0.4 * np.sin(2 * np.pi * np.cumsum(fr * 1.5) / SR) * np.exp(-t / 0.3)
    x += 0.3 * bandnoise(len(t), 100, 2000, seed) * np.exp(-t / 0.02) / 3
    x[:60] *= np.linspace(0, 1, 60)
    return reverb(x, 1.6, 1.8, 0.3, seed + 90)

if __name__ == '__main__':
    import shutil
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for i, p in enumerate((1.0, 1.04, 0.96)): save(f'moktak{i}', moktak(p, i))
    for i in range(3): save(f'bell{i}', pungyeong(i), 0.6)
    save('beomjong', beomjong(), 0.9)
    cs = chant_set()
    index = {}
    for k, y in cs.items():
        name = 'c_%04x%s' % (ord(k[0]), 'e' if k.endswith('_') else '')
        save(name, y, 0.8); index[k] = name
    json.dump(dict(lines=CHANT_LINES, syl=index), open('chant_index.json', 'w'), ensure_ascii=False)
    save('op_sop', opera(587.33, 1.18, seed=1), 0.7)   # D5
    save('op_mez', opera(415.30, 1.12, seed=2), 0.7)   # G#4
    save('op_ten', opera(293.66, 1.0, seed=3), 0.7)    # D4
    save('op_bar', opera(103.83, 0.92, seed=4), 0.7)   # G#2
    save('m_kick', kick(), 0.9); save('m_snare', snare(), 0.8); save('m_hat', hat(), 0.5); save('m_crash', crash(), 0.6)
    save('m_bass', bass(), 0.8)
    save('m_chug', dist_saw([110, 164.81, 220], 0.2, mute=True), 0.75)
    save('m_chord', dist_saw([110, 164.81, 220], 1.4), 0.7)
    save('m_lead', lead(), 0.6)
    save('c_whistle', whistle(), 0.5); save('c_clap', clap(), 0.8); save('c_pompom', pompom(), 0.5)
    save('c_drum', bigdrum(), 0.9); save('c_trumpet', trumpet(), 0.7)
    save('d_bass', membrane(80, 0.18, 0.2, 31), 0.9); save('d_tone', membrane(240, 0.08, 0.5, 32, 0.3), 0.8)
    save('d_slap', membrane(420, 0.03, 1.4, 33, 0.25), 0.8)
    kk = [(1, 1), (1.47, 0.7), (2.09, 0.6), (2.56, 0.4), (3.31, 0.3)]
    save('s_kkw_open', reverb(metal_hit(1180, kk, 0.35, 41, 0.6), 0.6, 3, 0.15, 41), 0.6)
    save('s_kkw_mute', metal_hit(1180, kk, 0.035, 42, 0.12, 0.5), 0.55)
    save('s_kung', membrane(95, 0.22, 0.2, 43, 0.5), 0.85)
    save('s_deok', membrane(520, 0.02, 1.2, 44, 0.2), 0.7)
    deong = membrane(95, 0.22, 0.2, 45, 0.5); dk = membrane(520, 0.02, 1.2, 46, 0.5)
    save('s_deong', deong + dk[:len(deong)] if len(dk) >= len(deong) else deong, 0.9)
    save('s_buk', membrane(70, 0.3, 0.5, 47, 0.7), 0.9)
    save('s_jing', jing(), 0.8)
    save('r_vln', strings(440.0, 1.3, seed=1), 0.6); save('r_vc', strings(110.0, 2.4, voices=3, seed=2, lp=1800, att=0.2), 0.7)
    save('r_fl', flute(880.0, 0.45, seed=3), 0.5); save('r_hn', horn(220.0, seed=4), 0.6); save('r_timp', timp(110.0, seed=5), 0.85)
    print(len(cs), 'chant syllables;', len(os.listdir(OUT)), 'files')
