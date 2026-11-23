#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を kinkakuji/ に写し、金閣寺〜北野天満宮用の差分をかけ直す。
（sync_higashiyama.py と同じ差分＋コースの切り替え。data.plan.defaultMode がないので「全部回る」で開く）

使い方: python3 scripts/sync_kinkakuji.py
- かけ直す差分:
  - データのパス、保存キー（kyoto-maps-kinkakuji-…）、タイトルと説明文
  - 写真ごとのクレジット表示（data の photos の要素を {"file", "credit": {"author", "license", "page"}} にすると、
    ネットから借りた写真の上に撮影者とライセンスを出す）
  - info.verified が false のスポットは「公式サイトで確認しました」ではなく「要確認」の一文を出す
  - 地図を開いたときは data.focus の範囲（歩くエリア）だけを映す。「全体を表示」ボタンでは全部
  - 最初から「選んで回る」で開く（data.plan.defaultMode が 'pick' のとき。一度切り替えたらその選択を覚える）
  - 番号だけの #16 のリンクも、そのままの番号で開く（叡山電鉄の旧番号の読み替えはしない）
  - コースの切り替え（2026-11-22）：一覧の上に「早朝コース／9〜10時に出発」のボタンの段（.coursesw）を足す。
    コースごとにデータファイルが別（kinkakuji.json・kinkakuji-late.json。scripts/build_kinkakuji_data.py が作る）で、押すと読み直す。
    紹介ページと一覧の文言は i18n.js の courseFor[コース] で上書き。「行った」印と選んだ場所はコースごとに別のキーで保存。
    紹介ページの写真は [スポットの id, 写真の番号] で指定（番号はコースで変わるため）
- kinkakuji/js/i18n.js は金閣寺〜北野専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/eizan-line/js/app.js', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

s = s.replace(s.split('(function () {')[0], """/* 京都 金閣寺〜北野天満宮 — map, list, spot detail, intro and language switch.
   Data: ../data/routes/kinkakuji.json（写真は ../images/kinkakuji/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_kinkakuji.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_kinkakuji.py で写し直す） */
""", 1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s = s.replace("window.EIZAN_I18N", "window.KINKAKUJI_I18N").replace("'kyoto-maps-eizan-", "'kyoto-maps-kinkakuji-")
s = re.sub(r"t = spots\.length \|\| \d+;", "t = spots.length || 6;", s)
m = re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)", s); assert m
s = s.replace(m.group(0), "fetch('../data/routes/' + course.file + '?v=5')")
# 2026-11-22 にスポットの順番を変えたので、「行った」印と選んだ場所は新しいキーで保存し直す
assert s.count("'kyoto-maps-kinkakuji-visited-v2'") == 1 and s.count("'kyoto-maps-kinkakuji-picks'") == 1
s = s.replace("'kyoto-maps-kinkakuji-visited-v2'", "'kyoto-maps-kinkakuji-visited-v3'").replace("'kyoto-maps-kinkakuji-picks'", "'kyoto-maps-kinkakuji-picks-v2'")

# コースの切り替え
rep("""  var mode = 'all', picks = {}, routeLine = null;
""", """  var mode = 'all', picks = {}, routeLine = null;
  // 金閣寺〜北野: コースは early（早朝。龍安寺と金閣寺に開門で入る）か late（9〜10時に出発）。コースごとにデータファイルが別。
  // 一覧の上のボタン（.coursesw）で切り替える。?course=late でも開ける
  var KEY_COURSE = 'kyoto-maps-kinkakuji-course';
  var course = { id: ((location.search.match(/[?&]course=([a-z]+)/) || [])[1] || load(KEY_COURSE)) === 'late' ? 'late' : 'early' };
  course.file = course.id === 'late' ? 'kinkakuji-late.json' : 'kinkakuji.json';
  // 「行った」印と選んだ場所はコースごとに別（番号がちがうため）
  if (course.id !== 'early') { KEY_VISITED += '-' + course.id; KEY_PICKS += '-' + course.id; }
  // i18n.js の courseFor[コース] に書いてある項目で、文言を上書きする（intro の中は項目ごとに）
  Object.keys(I18N).forEach(function (l) {
    var o = I18N[l].courseFor && I18N[l].courseFor[course.id];
    if (!o) return;
    Object.keys(o).forEach(function (k) {
      if (k === 'intro') Object.keys(o.intro).forEach(function (j) { I18N[l].intro[j] = o.intro[j]; });
      else I18N[l][k] = o[k];
    });
  });
""")
rep("""      b.addEventListener('click', function () { setMode(b.dataset.mode); });
    });""", """      b.addEventListener('click', function () { setMode(b.dataset.mode); });
    });
    // コースを切り替えたら、そのコースのデータで読み直す（一覧を開いた状態で）
    [].forEach.call(document.querySelectorAll('.coursesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.course === course.id));
      b.addEventListener('click', function () {
        if (b.dataset.course === course.id) return;
        store(KEY_COURSE, b.dataset.course);
        history.replaceState(null, '', location.pathname + '#list');
        location.reload();
      });
    });""")
# 一覧を開いたとき（#list）は、いちばん上（切り替えボタン）から見せる
rep("""  function route() {
    showRoute();
    updateTabs();
  }""", """  function listTop() {
    if (location.hash !== '#list') return;
    viewList.scrollTop = 0;
    setTimeout(function () { if (location.hash === '#list') viewList.scrollTop = 0; }, 80);
  }
  window.addEventListener('load', listTop);
  function route() {
    showRoute();
    updateTabs();
    listTop();
  }""")
rep("""  function introPhoto(p) { return photoUrl(byNo[p[0]].photos[p[1]]); }""",
"""  // [スポットの番号 or id, 写真の番号]（コースで番号が変わるので id で指定する）
  function introPhoto(p) {
    var s = typeof p[0] === 'string' ? spots.filter(function (x) { return x.id === p[0]; })[0] : byNo[p[0]];
    return photoUrl(s.photos[p[1]]);
  }""")

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
h = re.sub(r'<title>.*?</title>', '<title>京都 金閣寺・龍安寺・仁和寺・北野天満宮 Kinkaku-ji MAP</title>', h)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="大徳寺から金閣寺、龍安寺の石庭、御室桜の仁和寺、夜桜の平野神社、天神さんの北野天満宮へ。京都の北西を歩く1日ルートマップ。A one-day route through north-west Kyoto: Daitoku-ji, Kinkaku-ji, the Ryoan-ji rock garden, Ninna-ji, Hirano Shrine and Kitano Tenmangu.">', h)
h = re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)', r'\1金閣寺〜北野\2', h)
h = re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)', r'\1Kinkaku-ji to Kitano\2', h)
h = re.sub(r'(<p class="t-sub">)[^<]*(<span)', r'\1京都 Kinkaku-ji MAP\2', h)
a = '<span class="ph-area" id="ph-area"></span>'
assert h.count(a) == 1
h = h.replace(a, a + '\n        <span class="ph-credit" id="ph-credit" hidden></span>')
# コースの切り替えボタンの段を、「全部回る／選んで回る」の上に足す
_m = re.search(r'    <div class="modesw" role="group" data-t-aria="modeAria"[^>]*>', h); assert _m
h = h.replace(_m.group(0),
  '    <p class="sw-label" data-t="swCourse">コース</p>\n'
  '    <div class="coursesw" role="group" data-t-aria="courseAria" aria-label="コース">\n'
  '      <button type="button" data-course="early" data-t="courseEarly">早朝コース</button>\n'
  '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n'
  '    </div>\n'
  '    <p class="sw-label" data-t="swMode">回り方</p>\n' + _m.group(0))
# CSS / JS の ?v= は、テンプレートの数字に 100 を足す（このマップだけ更新したときに上げやすいように別の番号）
# このマップだけ更新したときは EXTRA の数字を上げる（2026-11-20：i18n.js とデータを直したので i18n・app を +1。2026-11-22：コースの切り替えで全部 +1。2026-11-24：要確認の調べ直しでデータを直したので app を +1）
EXTRA = {'css/style.css': 1, 'js/i18n.js': 2, 'js/app.js': 3}
h = re.sub(r'(css/style\.css|js/i18n\.js|js/app\.js)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + 100 + EXTRA[m.group(1)]}', h)

css = open(f'{R}/eizan-line/css/style.css', encoding='utf-8').read() + """
/* 金閣寺〜北野: credit for photos taken from the web (Wikimedia Commons): author and license on the photo itself */
.l-cr, .ph-credit { position: absolute; z-index: 1; max-width: calc(100% - 120px); font-size: 10.5px; line-height: 1.35; color: #fff; background: rgba(18,22,20,.62); padding: 3px 7px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.l-cr a, .ph-credit a { color: #fff; text-decoration: underline; text-underline-offset: 2px; }
.l-cr { left: 10px; bottom: 10px; }
.ph-credit { right: 10px; top: 10px; }
.l-cr[hidden], .ph-credit[hidden] { display: none; }
/* 金閣寺〜北野: コースの切り替えボタンの段（早朝コース／9〜10時に出発）と、段ごとの見出し */
.sw-label { margin: 8px 0 0; font-size: 12.5px; font-weight: 700; line-height: 1.5; color: var(--ink); }
.sw-label + .coursesw, .sw-label + .modesw { margin-top: 4px; }
.coursesw { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--ink); background: var(--card); margin: 4px 0 10px; }
.coursesw button { min-height: 44px; border: 0; background: transparent; font-size: 14px; font-weight: 700; color: var(--ink); white-space: pre-line; line-height: 1.35; padding: 6px 4px; }
.coursesw button[aria-pressed="true"] { background: var(--ink); color: var(--paper); }
.coursesw button + button { border-left: 1px solid var(--ink); }
"""

# ここまで来たら全部書き込む
os.makedirs(f'{R}/kinkakuji/js', exist_ok=True); os.makedirs(f'{R}/kinkakuji/css', exist_ok=True)
open(f'{R}/kinkakuji/css/style.css', 'w', encoding='utf-8').write(css)
open(f'{R}/kinkakuji/js/app.js', 'w', encoding='utf-8').write(app_js)
open(f'{R}/kinkakuji/index.html', 'w', encoding='utf-8').write(h)
print('synced')
