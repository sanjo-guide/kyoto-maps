#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を omihachiman/ に写し、近江八幡用の差分をかけ直す。

使い方: python3 scripts/sync_omihachiman.py
- かけ直す差分:
  - データのパス、保存キー（kyoto-maps-omihachiman-…）、「お得なきっぷ」欄を省略できるようにする変更（sync_minoh.py と同じ）
  - 最初から「選んで回る」で開く（data.plan.defaultMode が 'pick' のとき。ゲストが自分で選ぶ前提のマップなので）
  - 最初の地図は data.home の番号の範囲（近江八幡の町）に合わせる。京都駅・彦根は離れているため。「全体を表示」はテンプレートのまま
  - タイトルと説明文
- omihachiman/js/i18n.js は近江八幡専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/eizan-line/js/app.js', encoding='utf-8').read()


def rep(old, new):
    global s
    assert old in s, 'not found: ' + old[:70]
    s = s.replace(old, new, 1)


s = s.replace(s.split('(function () {')[0], """/* 近江八幡（京都発・彦根まで延長も） — map, list, spot detail, intro and language switch.
   Data: ../data/routes/omihachiman.json（写真は ../images/omihachiman/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違うのは データのパス・保存キー・「お得なきっぷ」欄の省略・
   最初から「選んで回る」で開くこと・最初の地図を近江八幡の町に合わせること（data.home）
   （テンプレートを更新したら python3 scripts/sync_omihachiman.py で写し直す） */
""", 1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s = s.replace("window.EIZAN_I18N", "window.OMI_I18N").replace("'kyoto-maps-eizan-", "'kyoto-maps-omihachiman-")
s = re.sub(r"t = spots\.length \|\| \d+;", "t = spots.length || 17;", s)
m = re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)", s)
assert m
s = s.replace(m.group(0), "fetch('../data/routes/omihachiman.json?v=1')")
# 「お得なきっぷ」欄を省略できるように（sync_minoh.py と同じ置き換え）
s2 = re.sub(r"""(        )'<section class="in-sec"><h2 class="in-h2">' \+ esc\(x\.dealsHead\) \+ (.*?)'</div><p class="in-deals-note">' \+ esc\(x\.dealsNote\) \+ '</p></section>' \+""",
            lambda m: m.group(1) + """(x.deals && x.deals.length ? '<section class="in-sec"><h2 class="in-h2">' + esc(x.dealsHead) + """ + m.group(2).replace(
                """'<a href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">' + esc(x.dealsMore) + '</a></div>';""",
                """(d.url ? '<a href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">' + esc(x.dealsMore) + '</a>' : '') + '</div>';""") +
            """'</div>' + (x.dealsNote ? '<p class="in-deals-note">' + esc(x.dealsNote) + '</p>' : '') + '</section>' : '') +""", s, flags=re.S)
assert s2 != s, 'deals block not found'
s = s2
# 最初から「選んで回る」（一度切り替えたら、その選択を覚える）
rep("mode = load(KEY_MODE) === 'pick' && data.plan ? 'pick' : 'all';",
    "mode = (load(KEY_MODE) || (data.plan && data.plan.defaultMode)) === 'pick' && data.plan ? 'pick' : 'all';")
# 最初の地図は data.home の範囲（京都駅・彦根は遠いので入れない）
rep("""  function init(d) {""", """  // 近江八幡: 最初の地図は町の中（data.home の番号の範囲）に合わせる
  function fitHome() {
    var h = data.home;
    if (!h) { fitAll(); return; }
    var b = L.latLngBounds(spots.filter(function (s) { return s.no >= h[0] && s.no <= h[1]; }).map(function (s) { return [s.lat, s.lng]; }));
    map.fitBounds(b, WIDE.matches ? { padding: [40, 40] } : { paddingTopLeft: [20, 150], paddingBottomRight: [20, 80] });
  }

  function init(d) {""")
rep("""    fitAll();
    addBaseMap();""", """    fitHome();
    addBaseMap();""")
app_js = s

# index.html: タイトル・説明・タイトルカード
h = open(f'{R}/eizan-line/index.html', encoding='utf-8').read()
h = re.sub(r'<title>.*?</title>', '<title>近江八幡｜京都から日帰り（彦根まで延長も）</title>', h)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="京都駅から電車で約35分。八幡堀、八幡山ロープウェーと琵琶湖の絶景、近江牛のランチ、クラフトビール、ラ コリーナ。行きたい場所を選んで回る、近江八幡の1日マップ（彦根城・玄宮園まで延長も）。A day trip from Kyoto to Omihachiman: pick the places you like — canal, ropeway and Lake Biwa views, Omi beef, craft beer, La Collina — with an optional extension to Hikone Castle.">', h)
h = re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)', r'\1近江八幡\2', h)
h = re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)', r'\1Omihachiman\2', h)
h = re.sub(r'(<p class="t-sub">)[^<]*(<span)', r'\1京都発 From Kyoto MAP\2', h)
# ここまで来たら全部書き込む
os.makedirs(f'{R}/omihachiman/css', exist_ok=True)
os.makedirs(f'{R}/omihachiman/js', exist_ok=True)
shutil.copy(f'{R}/eizan-line/css/style.css', f'{R}/omihachiman/css/style.css')
open(f'{R}/omihachiman/js/app.js', 'w', encoding='utf-8').write(app_js)
open(f'{R}/omihachiman/index.html', 'w', encoding='utf-8').write(h)
print('synced')
