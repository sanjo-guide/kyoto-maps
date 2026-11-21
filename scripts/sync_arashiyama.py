#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を arashiyama/ に写し、嵐山用の差分をかけ直す。

使い方: python3 scripts/sync_arashiyama.py
- かけ直す差分:
  - データのパス、保存キー（kyoto-maps-arashiyama-…）、タイトルと説明文
  - 写真ごとのクレジット表示（data の photos の要素を {"file", "credit": {"author", "license", "page"}} にすると、
    ネットから借りた写真の上に撮影者とライセンスを出す。二尊院・モンキーパークで使用）
  - info.verified が false のスポットは「公式サイトで確認しました」ではなく「要確認」の一文を出す
  - 地図を開いたときは data.focus の範囲（歩くエリア）だけを映す。「全体を表示」ボタンでは全部
  - 写真カードに切り替わるズームを 16 に（スポットが近いので、14 だと重なる）
  - 番号だけの #16 のリンクも、そのままの番号で開く（叡山電鉄の旧番号の読み替えはしない）
  - 最初から「選んで回る」で開く（data.plan.defaultMode が 'pick' のとき。一度切り替えたらその選択を覚える）
  - はじめて開いたときは、1日で無理なく回れる組み合わせ（data.plan.defaultPicks）を選んだ状態にする
    （sync_osaka.py と同じ差分。2026-11-22 の見直しで追加）
  - コースを選べる（2026-11-22 追加、オーナーの基準 realistic-day-standard）：一覧の上にボタンを1段足し、
    early（早朝に出発・愛宕念仏寺の開門へ）／tenryuji（早朝に出発・天龍寺の開門へ。水・土）／late（9〜10時に出発）から選ぶ。
    コースごとに別のデータファイル（arashiyama-early.json / arashiyama-tenryuji.json / arashiyama.json。
    3つとも scripts/build_arashiyama_courses.py が作る）を読む。箕面（sync_minoh.py）と同じ仕組みだが、
    嵐山は「全部回る／選んで回る」のボタンもそのまま使うので、コースのボタンは別の段（.coursesw、data-course）にしてある。
    選んだコースは保存キー kyoto-maps-arashiyama-course に残り、?course=early でも開ける。何も選んでいなければ late。
    「行った」印・回り方・選んだ場所は、コースごとに別に保存（late はこれまでのキーのまま）。
    文言は i18n.js の courseFor[コース] で上書きする（intro は項目ごと）。
    紹介ページの写真は [スポットの id, 写真の番号] でも指定できる（コースで番号が変わるため）
- arashiyama/js/i18n.js は嵐山専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/eizan-line/js/app.js', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)

s = s.replace(s.split('(function () {')[0], """/* 京都 嵐山・嵯峨野 — map, list, spot detail, intro and language switch.
   Data: ../data/routes/arashiyama.json・arashiyama-early.json・arashiyama-tenryuji.json（コースで読み分ける。写真は ../images/arashiyama/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_arashiyama.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_arashiyama.py で写し直す） */
""", 1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s = s.replace("window.EIZAN_I18N", "window.ARASHIYAMA_I18N").replace("'kyoto-maps-eizan-", "'kyoto-maps-arashiyama-")
s = re.sub(r"t = spots\.length \|\| \d+;", "t = spots.length || 19;", s)
# 2026-11-22 にお昼の店（仙翁）を足して番号が1つずつずれたので、「行った」印と選んだ場所は新しいキーで保存し直す
rep("'kyoto-maps-arashiyama-visited-v2'", "'kyoto-maps-arashiyama-visited-v3'")
rep("KEY_PICKS = 'kyoto-maps-arashiyama-picks'", "KEY_PICKS = 'kyoto-maps-arashiyama-picks-v2'")
m = re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)", s); assert m
s = s.replace(m.group(0), "fetch('../data/routes/' + course.file + '?v=10')")

# コース（出発のしかた）の切り替え
rep("""  var mode = 'all', picks = {}, routeLine = null;
""", """  var mode = 'all', picks = {}, routeLine = null;
  // 嵐山: 出発のしかた（コース）を3つから選べる。コースごとにデータファイルが別。
  // 一覧の上のボタン（.coursesw、data-course）で切り替える。「全部回る／選んで回る」のボタンはその下にそのまま残る
  var KEY_COURSE = 'kyoto-maps-arashiyama-course';
  var COURSE_FILES = { late: 'arashiyama.json', early: 'arashiyama-early.json', tenryuji: 'arashiyama-tenryuji.json' };
  var course = { id: (location.search.match(/[?&]course=([a-z]+)/) || [])[1] || load(KEY_COURSE) };
  if (!COURSE_FILES[course.id]) course.id = 'late';
  course.file = COURSE_FILES[course.id];
  // 「行った」印・回り方・選んだ場所はコースごとに別（9〜10時に出発 は、これまでのキーのまま）
  if (course.id !== 'late') { KEY_VISITED += '-' + course.id; KEY_MODE += '-' + course.id; KEY_PICKS += '-' + course.id; }
  // i18n.js の courseFor[コース] に書いてある文言で上書きする（intro は項目ごと）
  Object.keys(I18N).forEach(function (l) {
    var o = I18N[l].courseFor && I18N[l].courseFor[course.id];
    if (!o) return;
    Object.keys(o).forEach(function (k) {
      if (k === 'intro') Object.keys(o.intro).forEach(function (j) { I18N[l].intro[j] = o.intro[j]; });
      else I18N[l][k] = o[k];
    });
  });
""")
rep("""    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
    // 「選んで回る」の設定（data.plan）がないマップでは、切り替えボタンごと出さない
    document.querySelector('.modesw').hidden = !(data && data.plan);""", """    // 嵐山: ボタンは2段。上がコース（data-course）、下が「全部回る／選んで回る」（data-mode）
    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.course ? b.dataset.course === course.id : b.dataset.mode === mode));
    });
    document.querySelector('.modesw:not(.coursesw)').hidden = !(data && data.plan);""")
rep("""  function setMode(m) {
    if (m === mode) return;""", """  // 嵐山: コースを切り替えたら、そのコースのデータで読み直す（一覧を開いた状態で）
  function setCourse(c) {
    if (c === course.id) return;
    store(KEY_COURSE, c);
    history.replaceState(null, '', location.pathname + '#list');
    location.reload();
  }
  function setMode(m) {
    if (m === mode) return;""")
rep("""      b.addEventListener('click', function () { setMode(b.dataset.mode); });""",
"""      b.addEventListener('click', function () { if (b.dataset.course) setCourse(b.dataset.course); else setMode(b.dataset.mode); });""")
# 一覧を開いたとき（#list）は、いちばん上（切り替えボタン）から見せる（sync_minoh.py と同じ）
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
"""  // [スポットの番号 or id, 写真の番号]（コースで番号が変わるので、id でも指定できる）
  function introPhoto(p) {
    var s = typeof p[0] === 'string' ? spots.filter(function (x) { return x.id === p[0]; })[0] : byNo[p[0]];
    return photoUrl(s.photos[p[1]]);
  }""")

# 写真カードに切り替わるズーム
s, k = re.subn(r"var PHOTO_ZOOM = 14;[^\n]*", "var PHOTO_ZOOM = 16;          // show photo cards at this zoom and closer（嵐山はスポットが近いので16から）", s); assert k == 1

# 最初から「選んで回る」
rep("mode = load(KEY_MODE) === 'pick' && data.plan ? 'pick' : 'all';",
    "mode = (load(KEY_MODE) || (data.plan && data.plan.defaultMode)) === 'pick' && data.plan ? 'pick' : 'all';")

# はじめて開いたときは、基本の組み合わせ（data.plan.defaultPicks）を選んだ状態にする（一度でも選び直したらその選択を覚える）
rep("""    try { (JSON.parse(load(KEY_PICKS) || '[]') || []).forEach(function (n) { if (isPick(n)) picks[n] = true; }); } catch (e) {}""",
"""    try { (JSON.parse(load(KEY_PICKS) || '[]') || []).forEach(function (n) { if (isPick(n)) picks[n] = true; }); } catch (e) {}
    if (load(KEY_PICKS) === null && data.plan && data.plan.defaultPicks) data.plan.defaultPicks.forEach(function (n) { if (isPick(n)) picks[n] = true; });""")

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
h = re.sub(r'<title>.*?</title>', '<title>京都 嵐山・嵯峨野｜Arashiyama MAP</title>', h)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="バスで愛宕念仏寺へ行き、鳥居本の町並み、化野念仏寺、苔のお寺、竹林の小径、天龍寺、渡月橋へと坂道を下る、京都・嵐山と嵯峨野の1日ルートマップ。A one-day route map of Arashiyama and Sagano, Kyoto: take the bus up to Otagi Nenbutsu-ji, then walk downhill past moss temples and the bamboo grove to Togetsukyo Bridge.">', h)
h = re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)', r'\1京都 嵐山・嵯峨野\2', h)
h = re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)', r'\1Arashiyama &amp; Sagano, Kyoto\2', h)
h = re.sub(r'(<p class="t-sub">)[^<]*(<span)', r'\1嵐山 Arashiyama MAP\2', h)
a = '<span class="ph-area" id="ph-area"></span>'
assert h.count(a) == 1
h = h.replace(a, a + '\n        <span class="ph-credit" id="ph-credit" hidden></span>')
# コースのボタンの段を「全部回る／選んで回る」の上に足す
_m = re.search(r'    <div class="modesw" role="group" data-t-aria="modeAria"[^>]*>', h); assert _m
h = h.replace(_m.group(0),
  '    <p class="sw-label" data-t="swCourse">出発のしかた（愛宕念仏寺は水・土がお休み）</p>\n'
  '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発のしかた">\n'
  '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発：愛宕念仏寺の開門へ（日・月・火・木・金）</button>\n'
  '      <button type="button" data-course="tenryuji" data-t="courseTenryuji">早朝に出発：天龍寺の開門へ（水・土）</button>\n'
  '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n'
  '    </div>\n' + _m.group(0))
# CSS / JS の ?v= は、テンプレートの数字に BUMP を足す（嵐山だけ更新したときは BUMP を1つ上げる。2026-11-22 に 100→101→102→103）
BUMP = 103
h = re.sub(r'(css/style\.css|js/i18n\.js|js/app\.js)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + BUMP}', h)

css = open(f'{R}/eizan-line/css/style.css', encoding='utf-8').read() + """
/* 嵐山: credit for photos taken from the web (Wikimedia Commons): author and license on the photo itself */
.l-cr, .ph-credit { position: absolute; z-index: 1; max-width: calc(100% - 120px); font-size: 10.5px; line-height: 1.35; color: #fff; background: rgba(18,22,20,.62); padding: 3px 7px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.l-cr a, .ph-credit a { color: #fff; text-decoration: underline; text-underline-offset: 2px; }
.l-cr { left: 10px; bottom: 10px; }
.ph-credit { right: 10px; top: 10px; }
.l-cr[hidden], .ph-credit[hidden] { display: none; }
/* 嵐山: コース（出発のしかた）のボタン。3つを縦に並べる。その上に見出し */
.sw-label { margin: 8px 0 0; font-size: 12.5px; font-weight: 700; line-height: 1.5; color: var(--ink); }
.sw-label + .modesw { margin-top: 4px; }
.coursesw { grid-template-columns: 1fr; }
.coursesw button { padding: 8px 12px; text-align: left; line-height: 1.4; font-size: 13.5px; }
.coursesw button + button { border-top: 1px solid var(--ink); }
"""

# ここまで来たら全部書き込む
os.makedirs(f'{R}/arashiyama/js', exist_ok=True); os.makedirs(f'{R}/arashiyama/css', exist_ok=True)
open(f'{R}/arashiyama/css/style.css', 'w', encoding='utf-8').write(css)
open(f'{R}/arashiyama/js/app.js', 'w', encoding='utf-8').write(app_js)
open(f'{R}/arashiyama/index.html', 'w', encoding='utf-8').write(h)
print('synced')
