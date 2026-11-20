#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を minoh/ に写し、箕面用の差分をかけ直す。

使い方: python3 scripts/sync_minoh.py
- かけ直す差分: データのパス、保存キー（kyoto-maps-minoh-…）、「お得なきっぷ」欄を省略できるようにする変更、タイトルと説明文
- minoh/js/i18n.js は箕面専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, shutil
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=f'{R}/minoh/js/app.js'; s=open(f'{R}/eizan-line/js/app.js',encoding='utf-8').read()
s=s.replace(s.split('(function () {')[0],"""/* 大阪 箕面 — map, list, spot detail, intro and language switch.
   Data: ../data/routes/minoh.json（写真は ../images/minoh/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。データのパス、保存キー、「お得なきっぷ」欄を省略できるようにした点だけが違う
   （テンプレートを更新したら python3 scripts/sync_minoh.py で写し直す） */
""",1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s=s.replace("window.EIZAN_I18N","window.MINOH_I18N").replace("'kyoto-maps-eizan-","'kyoto-maps-minoh-")
s=re.sub(r"t = spots\.length \|\| \d+;","t = spots.length || 11;",s)
m=re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)",s); assert m
s=s.replace(m.group(0),"fetch('../data/routes/minoh.json?v=3')")
s2=re.sub(r"""(        )'<section class="in-sec"><h2 class="in-h2">' \+ esc\(x\.dealsHead\) \+ (.*?)'</div><p class="in-deals-note">' \+ esc\(x\.dealsNote\) \+ '</p></section>' \+""",
  lambda m: m.group(1)+"""(x.deals && x.deals.length ? '<section class="in-sec"><h2 class="in-h2">' + esc(x.dealsHead) + """+m.group(2).replace("""'<a href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">' + esc(x.dealsMore) + '</a></div>';""","""(d.url ? '<a href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">' + esc(x.dealsMore) + '</a>' : '') + '</div>';""")+"""'</div>' + (x.dealsNote ? '<p class="in-deals-note">' + esc(x.dealsNote) + '</p>' : '') + '</section>' : '') +""", s, flags=re.S)
assert s2!=s, 'deals block not found'; s=s2
app_js=s
# index.html: タイトル・説明・タイトルカード
h=open(f'{R}/eizan-line/index.html',encoding='utf-8').read()
h=re.sub(r'<title>.*?</title>','<title>大阪 箕面｜勝尾寺と箕面大滝</title>',h)
h=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="勝尾寺のダルマ、森の山道、箕面大滝、川沿いのテラス、たこ焼きと地ビールをめぐる大阪・箕面の1日ルートマップ。A one-day route map of Minoh, Osaka: Katsuoji Temple, a forest walk, Minoh Falls, takoyaki and craft beer.">',h)
h=re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)',r'\1大阪 箕面\2',h)
h=re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)',r'\1Minoh, Osaka\2',h)
h=re.sub(r'(<p class="t-sub">)[^<]*(<span)',r'\1箕面 Minoh MAP\2',h)
# ここまで来たら全部書き込む
shutil.copy(f'{R}/eizan-line/css/style.css', f'{R}/minoh/css/style.css')
open(f'{R}/minoh/js/app.js','w',encoding='utf-8').write(app_js)
open(f'{R}/minoh/index.html','w',encoding='utf-8').write(h)
print('synced')
