import json, base64, subprocess, os
src = open('game.src.html', encoding='utf-8').read()
assets = open('assets2.json').read()
data = open('gamedata.json', encoding='utf-8').read()
chars = set(src) | set(data) | set(''.join(chr(c) for c in range(0x20, 0x7f))) | set('만억조경해자양구간정재극항하사아승기나유타불가의무량대수·−◎∞')
text = ''.join(sorted(c for c in chars if ord(c) >= 0x20))
open('/tmp/claude-0/chars2.txt', 'w', encoding='utf-8').write(text)
faces = []
for fam in ('Galmuri14', 'Galmuri11'):
    out = f'/tmp/claude-0/{fam}.sub2.woff2'
    subprocess.run(['pyftsubset', f'package/dist/{fam}.ttf', '--text-file=/tmp/claude-0/chars2.txt', '--flavor=woff2', f'--output-file={out}'], check=True)
    faces.append(f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{base64.b64encode(open(out, "rb").read()).decode()}) format("woff2");font-display:block;}}')
page = src.replace('/*__FONTFACE__*/', '\n'.join(faces)).replace('/*__ASSETS__*/null', assets).replace('/*__DATA__*/null', data)
os.makedirs('dist', exist_ok=True)
open('dist/index2.artifact.html', 'w', encoding='utf-8').write(page)
head = '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
standalone = head + page.replace('\n<div class="app">', '\n</head>\n<body>\n<div class="app">', 1) + '\n</body>\n</html>\n'
open('dist/sogwi.html', 'w', encoding='utf-8').write(standalone)
print(os.path.getsize('dist/sogwi.html') // 1024, 'KB')
