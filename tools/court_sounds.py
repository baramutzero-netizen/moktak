import numpy as np
from scipy.signal import butter, lfilter
from moktak_model import moktak, save, SR
from sound2 import bandnoise
# gavel: harder, higher, shorter wood knock than the moktak, on a block
g = moktak(pitch=1.7, seed=201, dur=0.35, hardness=1.8)
save('j_gavel', g, 0.9)
# typing: a short dry click with a tiny body
def click(seed):
    t = np.arange(int(SR * 0.05)) / SR
    x = bandnoise(len(t), 2500, 9000, seed) * np.exp(-t / 0.004) + 0.4 * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.01)
    return x
save('j_type', click(202), 0.5)
# paper: page-turn swish
t = np.arange(int(SR * 0.35)) / SR
p = bandnoise(len(t), 1500, 8000, 203) * np.sin(np.pi * t / 0.35) ** 2 * (1 + 0.5 * np.sin(2 * np.pi * 23 * t))
save('j_paper', p, 0.45)
print('ok')
