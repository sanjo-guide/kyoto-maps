"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を higashiyama/ に写し、東山用の差分をかけ直す。
（同じ差分を伏見稲荷マップにも使う。scripts/sync_fushimi_inari.py が、設定を渡してこのファイルを実行する）

使い方: python3 scripts/sync_higashiyama.py
- かけ直す差分:
  - データのパス、保存キー（kyoto-maps-<id>-…）、タイトルと説明文
  - コースを選べる：一覧の上にボタンの段を足し、「早朝に出発」（early）と「9〜10時に出発」（late）でデータを読み分ける
    （<id>-early.json と <id>.json。どちらも scripts/build_<id>_data.py が作る）。選んだコースは保存キー
    kyoto-maps-<id>-course に残り、?course=early でも開ける。「行った」印・選んだ場所はコースごとに別に保存
    紹介ページは i18n.js の intro に、introFor[コース]（コースで変わる項目）を上書きして使う。
    紹介ページの写真（favPhoto・day の photo）は [スポットの id, 写真の番号] で指定する（コースで番号が変わるため）
  - 最初から「選んで回る」で開く（data.plan.defaultMode）。はじめて開いたときは data.plan.defaultPicks を選んだ状態にする
  - hints にも from / to（出す期間）を書ける
  - 写真ごとのクレジット表示（data の photos の要素を {"file", "credit": {"author", "license", "page"}} にすると、
    ネットから借りた写真の上に撮影者とライセンスを出す）
  - info.verified が false のスポットは「公式サイトで確認しました」ではなく「要確認」の一文を出す
  - 地図を開いたときは data.focus の範囲だけを映す（focus があるとき）。「全体を表示」ボタンでは全部
  - 番号だけの #16 のリンクも、そのままの番号で開く（叡山電鉄の旧番号の読み替えはしない）
- <id>/js/i18n.js はマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- テンプレートの作りが変わって置き換え先が見つからないと、途中で止まる（そのときはこのスクリプトを直す）
- このマップだけ更新したときは、下の CFG の data_v（データ）と bump（css・js）の数字を上げる
"""
import os, re, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HIGASHIYAMA = dict(
    id='higashiyama', i18n='HIGASHIYAMA_I18N', count=12, data_v=7, bump=104, keyv='-b',   # keyv: 2026-11-22 に3か所足して番号が変わった
    head='京都 東山（清水寺〜南禅寺〜銀閣寺）',
    title='京都 東山｜清水寺・南禅寺・銀閣寺 Higashiyama MAP',
    desc='朝6時の清水寺から、高台寺、八坂神社、青蓮院、南禅寺、永観堂、真如堂、銀閣寺へ。早朝に出るコースと9〜10時に出るコースを選べる、京都・東山の1日ルートマップ。A one-day route through Higashiyama, Kyoto, from Kiyomizu-dera at its 6:00 opening to Nanzen-ji and Ginkaku-ji, with an early-start and a 9–10 o’clock course.',
    main='京都 東山', alt='Higashiyama, Kyoto', sub='東山 Higashiyama MAP')


# ほかのマップ（scripts/sync_fushimi_inari.py）から呼ぶときは、CFG にそのマップの設定を入れて、このファイルをそのまま実行する
C = globals().get('CFG') or HIGASHIYAMA
ID = C['id']
s = open(f'{R}/eizan-line/js/app.js', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


s = s.replace(s.split('(function () {')[0], f"""/* {C['head']} — map, list, spot detail, intro and language switch.
   Data: ../data/routes/{ID}.json と {ID}-early.json（コースで読み分ける。写真は ../images/{ID}/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_{ID.replace('-', '_')}.py で写し直す） */
""", 1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s = s.replace("window.EIZAN_I18N", "window." + C['i18n']).replace("'kyoto-maps-eizan-", f"'kyoto-maps-{ID}-")
s = re.sub(r"t = spots\.length \|\| \d+;", f"t = spots.length || {C['count']};", s)
m = re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)", s); assert m
s = s.replace(m.group(0), f"fetch('../data/routes/' + course.file + '?v={C['data_v']}')")

# 最初から「選んで回る」
rep("mode = load(KEY_MODE) === 'pick' && data.plan ? 'pick' : 'all';",
    "mode = (load(KEY_MODE) || (data.plan && data.plan.defaultMode)) === 'pick' && data.plan ? 'pick' : 'all';")

# はじめて開いたときは、基本の組み合わせ（data.plan.defaultPicks）を選んだ状態にする（一度でも選び直したらその選択を覚える）
rep("""    try { (JSON.parse(load(KEY_PICKS) || '[]') || []).forEach(function (n) { if (isPick(n)) picks[n] = true; }); } catch (e) {}""",
"""    try { (JSON.parse(load(KEY_PICKS) || '[]') || []).forEach(function (n) { if (isPick(n)) picks[n] = true; }); } catch (e) {}
    if (load(KEY_PICKS) === null && data.plan && data.plan.defaultPicks) data.plan.defaultPicks.forEach(function (n) { if (isPick(n)) picks[n] = true; });""")

# コース（早朝に出発 / 9〜10時に出発）の切り替え
# スポットの番号を振り直したら keyv を変える（古い「行った」印・選んだ場所が、別のスポットに付かないように）
KV = C.get('keyv', '')
KEYS_JS = (f"  // 番号を振り直したので、保存キーの末尾に {KV} を付けてある\n  KEY_VISITED += '-' + course.id + '{KV}'; KEY_MODE += '-' + course.id; KEY_PICKS += '-' + course.id + '{KV}';" if KV
           else "  KEY_VISITED += '-' + course.id; KEY_MODE += '-' + course.id; KEY_PICKS += '-' + course.id;")
rep("""  var mode = 'all', picks = {}, routeLine = null;
""", f"""  var mode = 'all', picks = {{}}, routeLine = null;
  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
  var KEY_COURSE = 'kyoto-maps-{ID}-course';
  var course = {{ id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) }};
  if (course.id !== 'early') course.id = 'late';
  course.file = '{ID}' + (course.id === 'early' ? '-early' : '') + '.json';
  // 「行った」印・回り方・選んだ場所はコースごとに別に保存する（番号がコースで変わるため）
{KEYS_JS}
  // 紹介ページ: i18n.js の introFor[コース] に書いてある項目で intro を上書きする
  Object.keys(I18N).forEach(function (l) {{
    var o = I18N[l].introFor && I18N[l].introFor[course.id];
    if (o) Object.keys(o).forEach(function (k) {{ I18N[l].intro[k] = o[k]; }});
  }});
""")
rep("""    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
    // 「選んで回る」の設定（data.plan）がないマップでは、切り替えボタンごと出さない
    document.querySelector('.modesw').hidden = !(data && data.plan);""",
"""    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.course ? b.dataset.course === course.id : b.dataset.mode === mode));
    });
    // 「選んで回る」の設定（data.plan）がないマップでは、回り方のボタンを出さない（コースのボタンはいつも出す）
    document.querySelector('.modesw:not(.coursesw)').hidden = !(data && data.plan);""")
rep("""  function setMode(m) {
    if (m === mode) return;
    mode = m;
    savePlan();
    updateRoute();
  }""", """  function setMode(m) {
    if (m === mode) return;
    mode = m;
    savePlan();
    updateRoute();
  }
  // コースを切り替えたら、そのコースのデータで読み直す（一覧を開いた状態で）
  function setCourse(c) {
    if (c === course.id) return;
    store(KEY_COURSE, c);
    history.replaceState(null, '', location.pathname + '#list');
    location.reload();
  }""")
rep("""      b.addEventListener('click', function () { setMode(b.dataset.mode); });""",
"""      b.addEventListener('click', function () { if (b.dataset.course) setCourse(b.dataset.course); else setMode(b.dataset.mode); });""")
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
h = re.sub(r'<title>.*?</title>', f'<title>{C["title"]}</title>', h)
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{C["desc"]}">', h)
h = re.sub(r'(<p class="t-main" id="t-main">).*?(</p>)', r'\g<1>' + C['main'] + r'\2', h)
h = re.sub(r'(<p class="t-alt" id="t-alt">).*?(</p>)', r'\g<1>' + C['alt'] + r'\2', h)
h = re.sub(r'(<p class="t-sub">)[^<]*(<span)', r'\g<1>' + C['sub'] + r'\2', h)
a = '<span class="ph-area" id="ph-area"></span>'
assert h.count(a) == 1
h = h.replace(a, a + '\n        <span class="ph-credit" id="ph-credit" hidden></span>')
# コースのボタンの段を、回り方（全部回る／選んで回る）のボタンの上に足す
_m = re.search(r'    <div class="modesw" role="group" data-t-aria="modeAria"[^>]*>', h); assert _m
h = h.replace(_m.group(0), '    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
    '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
    '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n'
    '    </div>\n'
    '    <p class="sw-label" data-t="swMode">回り方</p>\n' + _m.group(0))
# CSS / JS の ?v= は、テンプレートの数字に C['bump'] を足す（このマップだけ更新したときは bump を1つ上げる）
h = re.sub(r'(css/style\.css|js/i18n\.js|js/app\.js)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + C["bump"]}', h)

css = open(f'{R}/eizan-line/css/style.css', encoding='utf-8').read() + """
/* credit for photos taken from the web (Wikimedia Commons): author and license on the photo itself */
.l-cr, .ph-credit { position: absolute; z-index: 1; max-width: calc(100% - 120px); font-size: 10.5px; line-height: 1.35; color: #fff; background: rgba(18,22,20,.62); padding: 3px 7px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.l-cr a, .ph-credit a { color: #fff; text-decoration: underline; text-underline-offset: 2px; }
.l-cr { left: 10px; bottom: 10px; }
.ph-credit { right: 10px; top: 10px; }
.l-cr[hidden], .ph-credit[hidden] { display: none; }
/* コースのボタンの段と、段ごとの見出し。2行に分かれるボタンの文字 */
.sw-label { margin: 8px 0 0; font-size: 12.5px; font-weight: 700; line-height: 1.5; color: var(--ink); }
.sw-label + .modesw { margin-top: 4px; }
.modesw button { white-space: pre-line; line-height: 1.35; padding: 6px 4px; }
"""

# ここまで来たら全部書き込む
os.makedirs(f'{R}/{ID}/js', exist_ok=True); os.makedirs(f'{R}/{ID}/css', exist_ok=True)
open(f'{R}/{ID}/css/style.css', 'w', encoding='utf-8').write(css)
open(f'{R}/{ID}/js/app.js', 'w', encoding='utf-8').write(app_js)
open(f'{R}/{ID}/index.html', 'w', encoding='utf-8').write(h)
print('synced', ID)
