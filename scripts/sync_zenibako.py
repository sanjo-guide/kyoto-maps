#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を zenibako/ に写し、銭函と朝里用の差分をかけ直す。
（sync_kobe.py と同じ形。sync_higashiyama.py の差分のうち、コースの切り替え以外。コースは1つで、data.plan.defaultMode がないので「全部回る」で開く）

使い方: python3 scripts/sync_zenibako.py   （データを直したときは、先に python3 scripts/build_zenibako_data.py）
- かけ直す差分:
  - データのパス、保存キー（kyoto-maps-zenibako-…）、タイトルと説明文
  - 写真ごとのクレジット表示（data の photos の要素を {"file", "credit": {"author", "license", "page"}} にすると、
    ネットから借りた写真の上に撮影者とライセンスを出す）。このマップの写真はいまは全部 Wikimedia Commons
  - info.verified が false のスポットは「公式サイトで確認しました」ではなく「要確認」の一文を出す
  - 地図を開いたときは data.focus の範囲（銭函〜小樽）だけを映す。「全体を表示」ボタンでは全部
  - hints にも from / to（出す期間）を書ける
  - 番号だけの #6 のリンクも、そのままの番号で開く（叡山電鉄の旧番号の読み替えはしない）
- zenibako/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
- このマップだけ更新したときは、下の DATA_V（データ）と EXTRA（css・js）の数字を上げる
"""
import os, re, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/eizan-line/js/app.js', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

s = s.replace(s.split('(function () {')[0], """/* 銭函と朝里（札幌から日帰り） — map, list, spot detail, intro and language switch.
   Data: ../data/routes/zenibako.json（写真は ../images/zenibako/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_zenibako.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_zenibako.py で写し直す） */
""", 1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s = s.replace("window.EIZAN_I18N", "window.ZENIBAKO_I18N").replace("'kyoto-maps-eizan-", "'kyoto-maps-zenibako-")
DATA_V = 2
s = re.sub(r"t = spots\.length \|\| \d+;", "t = spots.length || 8;", s)
m = re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)", s); assert m
s = s.replace(m.group(0), f"fetch('../data/routes/zenibako.json?v={DATA_V}')")

# 最初から「選んで回る」
rep("mode = load(KEY_MODE) === 'pick' && data.plan ? 'pick' : 'all';",
    "mode = (load(KEY_MODE) || (data.plan && data.plan.defaultMode)) === 'pick' && data.plan ? 'pick' : 'all';")

# hints にも出す期間（from / to）
rep("""    return data.plan.hints.filter(function (h) { return h.spot === no && ruleOk(h.rule); });""",
"""    return data.plan.hints.filter(function (h) { return h.spot === no && ruleOk(h.rule) && inRange(h.from, h.to); });""")

# 番号だけのリンク
rep("""    // #spot-16 が今の形式。以前配った #18 形式のリンクは旧番号（スタート前の2か所を含む）なので 2 を引いて開く
    var m = location.hash.match(/^#spot-(\\d+)$/), old = location.hash.match(/^#(\\d+)$/);
    var no = m ? Number(m[1]) : old ? Number(old[1]) - 2 : 0;""",
"""    // #spot-16 の形。番号だけの #16 でも同じスポットを開く
    var m = location.hash.match(/^#spot-(\\d+)$/) || location.hash.match(/^#(\\d+)$/);
    var no = m ? Number(m[1]) : 0;""")

# 写真ごとのクレジット
rep("  function photoUrl(f) { return data.photoBase + f; }",
"""  // a photo is a file name, or {file, credit: {author, license, page}} for a photo taken from the web
  function photoFile(p) { return typeof p === 'string' ? p : p.file; }
  function photoUrl(p) { return data.photoBase + photoFile(p); }
  function creditHtml(p) {
    var c = p && p.credit;
    if (!c) return '';
    return '<a href="' + esc(c.page) + '" target="_blank" rel="noopener noreferrer">' + esc(T().photoBy) + esc(c.author) + ' / ' + esc(c.license) + '</a>';
  }
  function showCredit(el, p) {
    if (!el) return;
    var h = creditHtml(p);
    el.innerHTML = h;
    el.hidden = !h;
  }""")
rep("""        }).join('') + '</div>' + badge(s.no) +""",
"""        }).join('') + '</div>' + badge(s.no) +
        '<span class="l-cr"' + (creditHtml(s.photos[0]) ? '' : ' hidden') + '>' + creditHtml(s.photos[0]) + '</span>' +""")
rep("""        var box = sl.parentNode, c = box.querySelector('.l-count');
        if (c) c.textContent = (i + 1) + ' / ' + n;""",
"""        var box = sl.parentNode, c = box.querySelector('.l-count');
        if (c) c.textContent = (i + 1) + ' / ' + n;
        var sp = byNo[Number(sl.dataset.open)];
        if (sp) showCredit(box.querySelector('.l-cr'), sp.photos[i]);""")
rep("""    $('slide-next').disabled = i >= n - 1;
  }""", """    $('slide-next').disabled = i >= n - 1;
    if (activeNo && byNo[activeNo]) showCredit($('ph-credit'), byNo[activeNo].photos[i]);
  }""")
rep("""    $('detail-scroll').scrollTop = 0;
    setActive(no);""", """    $('detail-scroll').scrollTop = 0;
    setActive(no);
    showCredit($('ph-credit'), s.photos[0]);""")
rep("""    [].forEach.call($('slides').querySelectorAll('img'), function (img, i) {
      img.alt = s.name[lang] + ' (' + (i + 1) + '/' + s.photos.length + ')';
    });
  }""", """    [].forEach.call($('slides').querySelectorAll('img'), function (img, i) {
      img.alt = s.name[lang] + ' (' + (i + 1) + '/' + s.photos.length + ')';
    });
    if (activeNo === s.no) updateCounter();   // photo credit in the current language
  }""")

# 要確認
rep("""    if (rows.length) html += '<p class="checked">' + esc(fill(t.checked, { d: t.checkedDate })) + '</p>';""",
"""    if (rows.length) html += '<p class="checked">' + esc(fill(inf.verified === false ? t.unchecked : t.checked, { d: t.checkedDate })) + '</p>';""")

# 最初に映す範囲
rep("""  function fitAll() {
    var r = routeSpots();""", """  // 地図を開いたときは歩くエリア（data.focus）だけを映す。「全体を表示」ボタン（e がある）では全部
  function fitAll(e) {
    var r = routeSpots(), f = !e && data.focus;
    if (f) r = r.filter(function (x) { return x.no >= f.first && x.no <= f.last; });""")
app_js = s

# index.html
h = open(f'{R}/eizan-line/index.html', encoding='utf-8').read()
h = re.sub(r'<title>.*?</title>', '<title>銭函と朝里｜札幌から日帰り Zenibako MAP</title>', h)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="札幌から快速で21分の銭函へ。1931年の駅舎、丘の上の豊足神社、海の前でお昼。午後は海べりの線路を朝里へ、バスで朝里川温泉。夜は小樽の運河沿いでビールと晩ごはん。冬も回れる、時刻つきの1日ルートマップ。A timed day trip from Sapporo: Zenibako’s 1931 station, a hilltop shrine and lunch by the sea, the seaside line to Asari, Asarigawa Onsen, and beer by the Otaru canal, planned for winter too.">', h)
h = re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)', r'\1銭函と朝里\2', h)
h = re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)', r'\1Zenibako &amp; Asari\2', h)
h = re.sub(r'(<p class="t-sub">)[^<]*(<span)', r'\1札幌から日帰り Zenibako MAP\2', h)
a = '<span class="ph-area" id="ph-area"></span>'
assert h.count(a) == 1
h = h.replace(a, a + '\n        <span class="ph-credit" id="ph-credit" hidden></span>')
# CSS / JS の ?v= は、テンプレートの数字に 100 を足す。このマップだけ i18n.js・app.js を変えたときは EXTRA を上げる
EXTRA = {'css/style.css': 0, 'js/i18n.js': 0, 'js/app.js': 0}
h = re.sub(r'(css/style\.css|js/i18n\.js|js/app\.js)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + 100 + EXTRA[m.group(1)]}', h)

css = open(f'{R}/eizan-line/css/style.css', encoding='utf-8').read() + """
/* 銭函と朝里: credit for photos taken from the web (Wikimedia Commons): author and license on the photo itself */
.l-cr, .ph-credit { position: absolute; z-index: 1; max-width: calc(100% - 120px); font-size: 10.5px; line-height: 1.35; color: #fff; background: rgba(18,22,20,.62); padding: 3px 7px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.l-cr a, .ph-credit a { color: #fff; text-decoration: underline; text-underline-offset: 2px; }
.l-cr { left: 10px; bottom: 10px; }
.ph-credit { right: 10px; top: 10px; }
.l-cr[hidden], .ph-credit[hidden] { display: none; }
"""

# ここまで来たら全部書き込む
os.makedirs(f'{R}/zenibako/js', exist_ok=True); os.makedirs(f'{R}/zenibako/css', exist_ok=True)
open(f'{R}/zenibako/css/style.css', 'w', encoding='utf-8').write(css)
open(f'{R}/zenibako/js/app.js', 'w', encoding='utf-8').write(app_js)
open(f'{R}/zenibako/index.html', 'w', encoding='utf-8').write(h)
print('synced zenibako')
