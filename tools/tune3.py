"""Design the purchase path, price every node for a steady ~4 s cadence (~10 min run),
and lay the node tree out: each venue anchors the upgrades that are worth buying there."""
import json, math

LIST_PER_V = [6, 3, 1, 3, 10, 9, 3, 4, 10, 10]        # listeners joining at each venue (v0 includes the free 누렁소)
GROUPS = [  # key, members, venue, power per credited hit, credited hits per bar
    ('novice', 10, 0, 1, 2), ('metal', 4, 1, 25, 4), ('opera', 5, 2, 700, 3), ('orch', 6, 3, 2e4, 4),
    ('court', 4, 4, 1.5e5, 4), ('comedy', 4, 5, 4e5, 4), ('cheer', 6, 6, 1.2e6, 4), ('djembe', 3, 7, 3e7, 4), ('samul', 4, 8, 8e8, 4)]
PERF = [(g, v, pw, hb) for (g, n, v, pw, hb) in GROUPS for _ in range(n)]
NV = len(LIST_PER_V)
COUNTS = dict(moktak=20, sutra=11, incense=18, ear=16)
BAR, CLICK, END, END_WAIT = 2.4, 3, 1e68, 12
PACE = 0.46   # overall speed: 0.5 = about a 5-minute run

def path():
    lv = [n for n in LIST_PER_V]; lv[0] -= 1                   # purchasable listeners per venue
    pv = [sum(1 for p in PERF if p[1] == v) for v in range(NV)]
    w = [lv[v] + pv[v] + 4 for v in range(NV)]
    tot = sum(w); b = [sum(w[:v]) / tot for v in range(NV + 1)]
    items = []
    li = 1
    for v in range(NV):
        if v > 0: items.append((b[v] - 1e-6, 'venue', v))
        for k in range(lv[v]): items.append((b[v] + (b[v + 1] - b[v]) * (k + 0.5) / lv[v], 'listener', li)); li += 1
    pj = 0
    for v in range(NV):
        for k in range(pv[v]): items.append((b[v] + (b[v + 1] - b[v]) * (k + 0.3) / pv[v], 'perf', pj)); pj += 1
    for t, n in COUNTS.items():
        off = {'moktak': 0.1, 'sutra': 0.55, 'incense': 0.3, 'ear': 0.75}[t]
        for k in range(n): items.append(((k + off) / n * 0.985, t, k))
    items.sort()
    # tier of a generic item = venue segment its position falls in
    out = []
    for pos, t, i in items:
        tier = max(v for v in range(NV) if b[v] <= pos + 1e-9) if t in COUNTS else None
        out.append(dict(type=t, i=i, tier=tier))
    # gating repair: a listener/perf/generic never comes before its venue
    venue = 0; fixed = []; pend = list(out)
    while pend:
        it = pend.pop(0)
        need = 0
        if it['type'] == 'listener': need = next(v for v in range(NV) if it['i'] < sum(LIST_PER_V[:v + 1]))
        elif it['type'] == 'perf': need = PERF[it['i']][1]
        elif it['type'] in COUNTS: need = it['tier']
        if need > venue:
            vi = next(k for k, x in enumerate(pend) if x['type'] == 'venue'); v = pend.pop(vi)
            fixed.append(v); venue = v['i']; pend.insert(0, it); continue
        fixed.append(it)
        if it['type'] == 'venue': venue = it['i']
    return fixed

def simulate(order, LSTEP):
    st = dict(sutra=0, moktak=0, venue=0, inc=1.0, ears=0, eartier=0, lsum=1.0, taps=CLICK)
    def rate():
        per = 40 ** st['sutra'] * 2 ** st['moktak'] * st['inc'] * 8 ** st['venue'] * st['lsum']
        ch = min(0.95, 0.04 * st['ears']); pw = 6 + 6 * st['eartier']
        return per * (1 + ch * (pw - 1)) * st['taps']
    M = len(order); t = 0
    v1 = next(j for j, it in enumerate(order) if it['type'] == 'venue' and it['i'] == 1)
    for j, it in enumerate(order):
        interval = 1.8 + 9.0 * (1 - j / M) ** 3   # slow start (time to tap the moktak), faster and faster later
        if j < v1: interval *= 0.7                 # reach the concert hall ~30% sooner
        interval *= PACE
        it['cost'] = float('%.2g' % max(1, rate() * interval))
        t += interval
        ty = it['type']
        if ty == 'sutra': st['sutra'] += 1
        elif ty == 'moktak': st['moktak'] += 1
        elif ty == 'venue': st['venue'] += 1
        elif ty == 'incense': st['inc'] *= 2 + it['tier']
        elif ty == 'ear': st['ears'] += 1; st['eartier'] = max(st['eartier'], it['tier'])
        elif ty == 'listener': st['lsum'] += LSTEP ** it['i']
        elif ty == 'perf': p = PERF[it['i']]; st['taps'] += p[2] * p[4 - 1] / BAR
    return rate(), t

def layout(order):
    """Columns hang off each venue anchor: listeners up, performers down, generic segments on the lighter side."""
    cols = [dict(up=[], down=[]) for _ in range(NV)]
    seg = {}
    for it in order:
        ty = it['type']
        if ty == 'venue': continue
        v = (next(v for v in range(NV) if it['i'] < sum(LIST_PER_V[:v + 1])) if ty == 'listener'
             else PERF[it['i']][1] if ty == 'perf' else it['tier'])
        seg.setdefault((v, ty), []).append(it)
    nodes = [dict(id='root', type='root', x=0, y=0, parent=None, cost=0)]
    X = 0
    vx = []
    for v in range(NV):
        anchor = 'root' if v == 0 else f'v{v}'
        if v > 0:
            vit = next(it for it in order if it['type'] == 'venue' and it['i'] == v)
            nodes.append(dict(id=anchor, type='venue', i=v, x=X, y=0, parent='root' if v == 1 else f'v{v - 1}', cost=vit['cost']))
        vx.append(X)
        c = cols[v]
        if (v, 'listener') in seg: c['up'].append(seg[(v, 'listener')])
        if (v, 'perf') in seg: c['down'].append(seg[(v, 'perf')])
        for ty in ('moktak', 'incense', 'ear', 'sutra'):
            if (v, ty) in seg:
                side = 'up' if sum(len(x) for x in c['up']) <= sum(len(x) for x in c['down']) else 'down'
                c[side].append(seg[(v, ty)])
        for side, sgn in (('up', -1), ('down', 1)):
            for j, column in enumerate(c[side]):
                parent = anchor
                for k, it in enumerate(column):
                    pre = {'listener': 'L', 'perf': 'P', 'moktak': 'mk', 'incense': 'in', 'ear': 'ear', 'sutra': 'su'}[it['type']]
                    nid = f"{pre}{it['i']}"
                    nodes.append(dict(id=nid, type=it['type'], i=it['i'], tier=it.get('tier'), x=X + j, y=sgn * (k + 1), parent=parent, cost=it['cost']))
                    parent = nid
        X += max(1, len(c['up']), len(c['down'])) + 1
    nodes.append(dict(id='nirvana', type='nirvana', x=X + 1, y=0, parent=f'v{NV - 1}', cost=END))
    seen = {}
    for n in nodes:
        k = (n['x'], n['y']); assert k not in seen, (k, seen.get(k), n['id']); seen[k] = n['id']
    return nodes

if __name__ == '__main__':
    order = path()
    lo, hi = 1.02, 12
    for _ in range(50):
        mid = (lo + hi) / 2
        final, t = simulate(order, mid)
        if final * END_WAIT < END: lo = mid
        else: hi = mid
    final, t = simulate(order, hi)
    nodes = layout(order)
    print(f'items {len(order)}, LSTEP {hi:.4f}, path {t / 60:.1f} min + ending {END / final:.0f}s')
    json.dump(dict(lstep=round(hi, 5), nodes=nodes, groups=[dict(key=g, n=n, venue=v, pw=pw, hb=hb) for g, n, v, pw, hb in GROUPS]),
              open('balance3.json', 'w'))
    xs = [n['x'] for n in nodes]; ys = [n['y'] for n in nodes]
    print('tree bounds', min(xs), max(xs), min(ys), max(ys))
    from collections import Counter
    0 and print(Counter((n['type'], n.get('tier')) for n in nodes if n['type'] in ('incense', 'ear', 'moktak', 'sutra')))
