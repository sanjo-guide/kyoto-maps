#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を minoh/ に写し、箕面用の差分をかけ直す。

使い方: python3 scripts/sync_minoh.py
- かけ直す差分: データのパス、保存キー（kyoto-maps-minoh-…）、「お得なきっぷ」欄を省略できるようにする変更、タイトルと説明文
- コースを選べる：出発時間（早めに出発 / ゆっくり出発）と、箕面温泉に入るかどうかの2つを別々に選ぶ（4通り）。
  天橋立・伊根（sync_amanohashidate.py）と同じ仕組みで、一覧の上の切り替えボタン（テンプレートの「全部回る／選んで回る」）を
  出発時間に使い、その下に温泉のボタンの段を足す。コースごとに別のデータファイル（minoh.json / minoh-noonsen.json /
  minoh-late.json / minoh-late-noonsen.json。4つとも scripts/build_minoh_courses.py が作る）を読む。
  選んだ内容は保存キー kyoto-maps-minoh-course（early / late）と kyoto-maps-minoh-onsen（yes / no）に残り、
  ?course=late&onsen=no でも開ける。「行った」印はコースごとに別に保存
  紹介ページは i18n.js の intro に、introFor[コースの id]（コースで変わる項目）を上書きして使う。
  紹介ページの写真（favPhoto・day の photo）は [スポットの id, 写真の番号] で指定する（コースで番号が変わるため）
"""
import os, re, shutil
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=f'{R}/minoh/js/app.js'; s=open(f'{R}/eizan-line/js/app.js',encoding='utf-8').read()
s=s.replace(s.split('(function () {')[0],"""/* 大阪 箕面 — map, list, spot detail, intro and language switch.
   Data: ../data/routes/minoh.json と minoh-late.json（出発時間で読み分ける。写真は ../images/minoh/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_minoh.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_minoh.py で写し直す） */
""",1)
assert "window.EIZAN_I18N" in s and "'kyoto-maps-eizan-" in s
s=s.replace("window.EIZAN_I18N","window.MINOH_I18N").replace("'kyoto-maps-eizan-","'kyoto-maps-minoh-")
s=re.sub(r"t = spots\.length \|\| \d+;","t = spots.length || 12;",s)
m=re.search(r"fetch\('\.\./data/routes/eizan-line\.json\?v=\d+'\)",s); assert m
s=s.replace(m.group(0),"fetch('../data/routes/' + course.file + '?v=8')")
def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
# コース（出発時間と温泉）の切り替え
rep("""  var mode = 'all', picks = {}, routeLine = null;
""", """  var mode = 'all', picks = {}, routeLine = null;
  // 箕面: 出発時間（early / late）と、箕面温泉に入るか（yes / no）を別々に選べる。組み合わせごとにデータファイルが別。
  // 一覧の上の切り替えボタン（all / pick）を出発時間に使い、その下に温泉のボタン（data-onsen）の段がある
  var KEY_COURSE = 'kyoto-maps-minoh-course', KEY_ONSEN = 'kyoto-maps-minoh-onsen';
  function chosen(name, key, opts) {
    var q = (location.search.match(new RegExp('[?&]' + name + '=([a-z]+)')) || [])[1] || load(key);
    return opts.indexOf(q) >= 0 ? q : opts[0];
  }
  var course = { start: chosen('course', KEY_COURSE, ['early', 'late']), onsen: chosen('onsen', KEY_ONSEN, ['yes', 'no']) };
  course.id = course.start + (course.onsen === 'no' ? '-noonsen' : '');
  course.file = 'minoh' + (course.start === 'late' ? '-late' : '') + (course.onsen === 'no' ? '-noonsen' : '') + '.json';
  // 「行った」印はコースごとに別（早めに出発・温泉に入る は、これまでのキーのまま）
  if (course.id !== 'early') KEY_VISITED += '-' + course.id;
  // 紹介ページ: i18n.js の introFor[コース] に書いてある項目で intro を上書きする
  Object.keys(I18N).forEach(function (l) {
    var o = I18N[l].introFor && I18N[l].introFor[course.id];
    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
  });
""")
rep("""    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
    // 「選んで回る」の設定（data.plan）がないマップでは、切り替えボタンごと出さない
    document.querySelector('.modesw').hidden = !(data && data.plan);""", """    // 箕面: 切り替えボタンは「出発時間」（all = 早めに出発、pick = ゆっくり出発）と「温泉に入る／入らない」
    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      var on = b.dataset.onsen ? b.dataset.onsen === course.onsen : b.dataset.mode === (course.start === 'late' ? 'pick' : 'all');
      b.setAttribute('aria-pressed', String(on));
    });
    [].forEach.call(document.querySelectorAll('.modesw'), function (el) { el.hidden = false; });""")
rep("""  function setMode(m) {
    if (m === mode) return;
    mode = m;
    savePlan();
    updateRoute();
  }""", """  // 箕面: 出発時間か温泉を切り替えたら、その組み合わせのデータで読み直す（一覧を開いた状態で）
  function setMode(m, o) {
    var start = m ? (m === 'pick' ? 'late' : 'early') : course.start, onsen = o || course.onsen;
    if (start === course.start && onsen === course.onsen) return;
    store(KEY_COURSE, start);
    store(KEY_ONSEN, onsen);
    history.replaceState(null, '', location.pathname + '#list');
    location.reload();
  }""")
rep("""      b.addEventListener('click', function () { setMode(b.dataset.mode); });""",
"""      b.addEventListener('click', function () { setMode(b.dataset.mode, b.dataset.onsen); });""")
# 一覧を開いたとき（#list）は、いちばん上（切り替えボタン）から見せる。
# ブラウザは #list を見ると id="list" の一覧そのものまで自動で送るので、上のボタンが隠れてしまう
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
"""  // [スポットの番号 or id, 写真の番号]（箕面はコースで番号が変わるので id で指定する）
  function introPhoto(p) {
    var s = typeof p[0] === 'string' ? spots.filter(function (x) { return x.id === p[0]; })[0] : byNo[p[0]];
    return photoUrl(s.photos[p[1]]);
  }""")
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
# 要確認（info.verified が false のスポットは「公式サイトで確認しました」ではなく「要確認」の一文を出す）
_a = """    if (rows.length) html += '<p class="checked">' + esc(fill(t.checked, { d: t.checkedDate })) + '</p>';"""
assert app_js.count(_a) == 1
app_js = app_js.replace(_a, """    if (rows.length) html += '<p class="checked">' + esc(fill(inf.verified === false ? t.unchecked : t.checked, { d: t.checkedDate })) + '</p>';""")
# 切り替えボタンを2段にする（出発時間／箕面温泉）。それぞれの上に見出しを付ける
_m = re.search(r'    <div class="modesw" role="group" data-t-aria="modeAria"[^>]*>.*?</div>\n', h, flags=re.S); assert _m
h = h.replace(_m.group(0), '    <p class="sw-label" data-t="swStart">出発時間</p>\n' + _m.group(0) +
  '    <p class="sw-label" data-t="swOnsen">箕面温泉</p>\n'
  '    <div class="modesw" role="group" data-t-aria="onsenAria" aria-label="箕面温泉に入るかどうか">\n'
  '      <button type="button" data-onsen="yes" data-t="onsenYes">温泉に入る</button>\n'
  '      <button type="button" data-onsen="no" data-t="onsenNo">温泉に入らない</button>\n'
  '    </div>\n')
css = open(f'{R}/eizan-line/css/style.css', encoding='utf-8').read() + """
/* 箕面: 切り替えボタンが2段（出発時間／箕面温泉）。段ごとの見出しと、2行に分かれるボタンの文字 */
.sw-label { margin: 8px 0 0; font-size: 12.5px; font-weight: 700; line-height: 1.5; color: var(--ink); }
.sw-label + .modesw { margin-top: 4px; }
.modesw button { white-space: pre-line; line-height: 1.35; padding: 6px 4px; }
"""
h = re.sub(r'(css/style\.css)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + 1}', h)
# このマップだけ i18n.js / app.js を直したときの番号（テンプレートの番号に足す）
h = re.sub(r'(js/i18n\.js|js/app\.js)\?v=(\d+)', lambda m: f'{m.group(1)}?v={int(m.group(2)) + 3}', h)
# ここまで来たら全部書き込む
open(f'{R}/minoh/css/style.css', 'w', encoding='utf-8').write(css)
open(f'{R}/minoh/js/app.js','w',encoding='utf-8').write(app_js)
open(f'{R}/minoh/index.html','w',encoding='utf-8').write(h)
print('synced')
