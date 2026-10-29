"""Modal moktak resynthesis fitted to the reference recording (rec/src.wav).
Analysis (24 averaged hits): main modes 603 Hz and 1556 Hz (ratio 2.58), weaker 926/1405/1744 Hz,
a cluster of faint wood modes 2.1-3.8 kHz, decay time constants ~90-230 ms, envelope peak ~8-10 ms
after the strike, and a room reflection around 115 ms."""
import numpy as np, json, wave
from scipy.signal import butter, lfilter
SR = 44100

MODES = [  # Hz, level dB, tau ms — fitted to the averaged reference hits (rec/modes.json, rec/specenv.json)
    (603, 0.0, 75), (926, -18.0, 90), (1405, -23.0, 60), (1556, -4.0, 55), (1744, -22.0, 50)]
WOOD = [(2164, -40), (2396, -40), (2579, -38), (2799, -38), (3063, -39), (3763, -46)]   # faint, short

def bandnoise(n, lo, hi, r):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, r.standard_normal(n))

def resonator(x, f, q):
    w0 = 2 * np.pi * f / SR; alpha = np.sin(w0) / (2 * q)
    b = [alpha, 0, -alpha]; a = [1 + alpha, -2 * np.cos(w0), 1 - alpha]
    return lfilter(b, a, x)

def strike(n, r, pitch, hardness):
    t = np.arange(n) / SR
    x = np.zeros(n)
    rise = 0.006 / hardness
    onset = np.where(t < rise, 0.5 - 0.5 * np.cos(np.pi * t / rise), 1.0)
    for f, db, tau in MODES:
        f *= pitch * (1 + r.uniform(-0.004, 0.004)); A = 10 ** (db / 20); ph = r.uniform(0, 6.28)
        # narrow ringing part + a heavily damped wide part (gives the broad skirt seen in the recording)
        ring = 0.5 * (np.sin(2 * np.pi * f * t + ph) + np.sin(2 * np.pi * (f + r.uniform(0.6, 1.8)) * t + ph)) * np.exp(-t / (tau / 1000))
        wide = resonator(r.standard_normal(n) * np.exp(-t / 0.006), f, 6) * 0.5
        x += A * (ring + wide / (np.abs(wide).max() + 1e-9) * 0.9)
    for f, db in WOOD:
        f *= pitch; x += 10 ** (db / 20) * np.sin(2 * np.pi * f * t + r.uniform(0, 6)) * np.exp(-t / 0.035)
    x *= onset
    click = bandnoise(n, 1500, 4500, r) * np.exp(-t / 0.002)
    x += 0.05 * hardness * click / (np.abs(click).max() + 1e-9)
    return x

def moktak(pitch=1.0, seed=0, dur=0.45, room=True, hardness=1.0):
    r = np.random.default_rng(seed)
    n = int(SR * dur); t = np.arange(n) / SR
    x = strike(n, r, pitch, hardness)
    # mallet rebound ~27 ms after the strike (visible as a second envelope peak in every reference hit)
    d = int(0.027 * SR); reb = strike(n, r, pitch, hardness * 0.8)
    x[d:] += 0.8 * reb[:-d]
    if room:
        y = x.copy()
        d = int(0.118 * SR); y[d:] += 0.55 * x[:-d]
        d = int(0.205 * SR); y[d:] += 0.25 * x[:-d]
        ir_n = int(0.4 * SR); ir = r.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / (0.08 * SR))
        b, a = butter(2, 2500 / (SR / 2)); ir = lfilter(b, a, ir); ir[: int(0.012 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
        x = y + 0.22 * np.convolve(y, ir)[:n]
    x *= np.minimum(1, (dur - t) / 0.08)
    return x / np.abs(x).max()

def save(name, y, gain=0.9):
    y = y / (np.abs(y).max() + 1e-9) * gain
    with wave.open(f'snd/{name}.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype('<i2').tobytes())

if __name__ == '__main__':
    import shutil, os
    for i in range(3):   # keep the first synth for comparison
        if os.path.exists(f'snd/moktak{i}.wav') and not os.path.exists(f'snd/moktakO{i}.wav'):
            shutil.copy(f'snd/moktak{i}.wav', f'snd/moktakO{i}.wav')
    for i, (p, h) in enumerate(((1.0, 1.0), (1.015, 1.1), (0.985, 0.9))):
        save(f'moktak{i}', moktak(p, 100 + i, hardness=h))
