import json, tune3
B = json.load(open('balance3.json')); N = {n['id']: n for n in B['nodes']}; L = B['lstep']
def sim(click):
    own = {'root'}; k = 0; t = 0; dt = 0.1; log = []
    st = dict(sutra=0, moktak=0, venue=0, inc=1.0, ears=0, eartier=0, lsum=1.0, taps=click)
    def rate():
        ch = min(.95, .04 * st['ears']); pw = 6 + 6 * st['eartier']
        return 40**st['sutra'] * 2**st['moktak'] * st['inc'] * 8**st['venue'] * st['lsum'] * (1 + ch * (pw - 1)) * st['taps']
    while True:
        ready = [n for n in B['nodes'] if n['id'] not in own and n['parent'] in own and n['type'] != 'nirvana']
        if not ready and k >= 1e68: break
        if ready:
            n = min(ready, key=lambda n: n['cost'])
            if k >= n['cost']:
                k -= n['cost']; own.add(n['id']); log.append(t); ty = n['type']
                if ty == 'sutra': st['sutra'] += 1
                elif ty == 'moktak': st['moktak'] += 1
                elif ty == 'venue': st['venue'] += 1
                elif ty == 'incense': st['inc'] *= 2 + n['tier']
                elif ty == 'ear': st['ears'] += 1; st['eartier'] = max(st['eartier'], n['tier'])
                elif ty == 'listener': st['lsum'] += L ** n['i']
                elif ty == 'perf': p = tune3.PERF[n['i']]; st['taps'] += p[2] * p[3] / 2.4
                continue
        k += rate() * dt; t += dt
        if t > 7200: break
    gaps = [b - a for a, b in zip(log, log[1:])]
    return t, len(log), max(gaps), sorted(gaps)[len(gaps) // 2]
for c in (6, 3, 1):
    print(c, ['%.1f' % x for x in sim(c)])
