#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を kobe/ に写し、神戸用の差分をかけ直す。
（sync_higashiyama.py と同じ差分のうち、コースの切り替え以外。コースは1つで、data.plan.defaultMode がないので「全部回る」で開く）
2026-11-22: 大阪の梅田〜難波のホテル起点の時間割に作り直し、回る順（番号）が変わったので、「行った」印と選んだ場所の保存キーの末尾に -b を付けた

使い方: python3 scripts/sync_kobe.py
- かけ直す差分:
  - データのパス、保存キー（kyoto-maps-kobe-…）、タイトルと説明文
  - 写真ごとのクレジット表示（data の photos の要素を {"file", "credit": {"author", "license", "page"}} にすると、
    ネットから借りた写真の上に撮影者とライセンスを出す）
  - info.verified が false のスポットは「公式サイトで確認しました」ではなく「要確認」の一文を出す
  - 地図を開いたときは data.focus の範囲（歩くエリア）だけを映す。「全体を表示」ボタンでは全部
  - 最初から「選んで回る」で開く（data.plan.defaultMode が 'pick' のとき。一度切り替えたらその選択を覚える）
  - 番号だけの #16 のリンクも、そのままの番号で開く（叡山電鉄の旧番号の読み替えはしない）
- kobe/js/i18n.js は神戸専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/eizan-line/js/app.js', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

s = s.replace(s.split('(function () {')[0], """/* 神戸 1日ルート（北野異人館・布引の滝・南京町・夜の港） — map, list, spot detail, intro and language switch.
   Data: ../data/routes/kobe.json（写真は ../images/kobe/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_kobe.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_kobe.py で写し直す） */
""", 1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s = s.replace("window.EIZAN_I18N", "window.KOBE_I18N").replace("'kyoto-maps-eizan-", "'kyoto-maps-kobe-")
# 番号を振り直したので、保存キーの末尾に -b（古い「行った」印・選んだ場所が、別のスポットに付かないように）
for k in ("'kyoto-maps-kobe-visited-v2'", "'kyoto-maps-kobe-picks'"):
    assert s.count(k) == 1, k
    s = s.replace(k, k[:-1] + "-b'")
s = re.sub(r"t = spots\.length \|\| \d+;", "t = spots.length || 6;", s)
m = re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)", s); assert m
s = s.replace(m.group(0), "fetch('../data/routes/kobe.json?v=5')")

# 最初から「選んで回る」
rep("mode = load(KEY_MODE) === 'pick' && data.plan ? 'pick' : 'all';",
    "mode = (load(KEY_MODE) || (data.plan && data.plan.defaultMode)) === 'pick' && data.plan ? 'pick' : 'all';")

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
h = re.sub(r'<title>.*?</title>', '<title>神戸 1日ルート｜北野異人館・布引の滝・夜の港 Kobe MAP</title>', h)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="大阪の梅田〜難波のホテルから1日で回る神戸。午前は北野の異人館、三宮でかつ丼、午後は新神戸駅の裏の布引の滝、南京町を抜けてメリケンパークの夕暮れ、夜のハーバーランドまで。時刻つきのルートマップ。Kobe in one day from a hotel in Osaka: the Kitano foreign residences, a katsudon lunch, Nunobiki Falls, Chinatown, sunset at Meriken Park and the harbour at night, with a timetable.">', h)
h = re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)', r'\1神戸\2', h)
h = re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)', r'\1Kobe\2', h)
h = re.sub(r'(<p class="t-sub">)[^<]*(<span)', r'\1神戸 1日ルート Kobe MAP\2', h)
a = '<span class="ph-area" id="ph-area"></span>'
assert h.count(a) == 1
h = h.replace(a, a + '\n        <span class="ph-credit" id="ph-credit" hidden></span>')
# CSS / JS の ?v= は、テンプレートの数字に 100 を足す（このマップだけ更新したときに上げやすいように別の番号）
# EXTRA: このマップだけ i18n.js・app.js（データの ?v）を変えたときに足す数（2026-11-20 点検の修正で +1、2026-11-22 の作り直しで +1、2026-11-24 の要確認の見直しで app.js +1）
EXTRA = {'css/style.css': 0, 'js/i18n.js': 2, 'js/app.js': 3}
h = re.sub(r'(css/style\.css|js/i18n\.js|js/app\.js)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + 100 + EXTRA[m.group(1)]}', h)

css = open(f'{R}/eizan-line/css/style.css', encoding='utf-8').read() + """
/* 神戸: credit for photos taken from the web (Wikimedia Commons): author and license on the photo itself */
.l-cr, .ph-credit { position: absolute; z-index: 1; max-width: calc(100% - 120px); font-size: 10.5px; line-height: 1.35; color: #fff; background: rgba(18,22,20,.62); padding: 3px 7px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.l-cr a, .ph-credit a { color: #fff; text-decoration: underline; text-underline-offset: 2px; }
.l-cr { left: 10px; bottom: 10px; }
.ph-credit { right: 10px; top: 10px; }
.l-cr[hidden], .ph-credit[hidden] { display: none; }
"""

# ここまで来たら全部書き込む
os.makedirs(f'{R}/kobe/js', exist_ok=True); os.makedirs(f'{R}/kobe/css', exist_ok=True)
open(f'{R}/kobe/css/style.css', 'w', encoding='utf-8').write(css)
open(f'{R}/kobe/js/app.js', 'w', encoding='utf-8').write(app_js)
open(f'{R}/kobe/index.html', 'w', encoding='utf-8').write(h)
print('synced')
