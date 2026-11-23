#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を kohoku/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_kohoku.py
- 共通の差分（コースの切り替え・写真のクレジット・要確認の一文など）は scripts/sync_higashiyama.py にあり、
  ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、湖北だけの差分をかける:
  - コースは4つ（scripts/build_kohoku_data.py が作る）。ボタンは2列×2段
      late   （9:45ごろ発：桜並木を往復→夕方の長浜。最初に開く）= data/routes/kohoku.json
      through（9:45ごろ発：永原まで歩き通す）              = data/routes/kohoku-through.json
      early  （7:00発：朝の桜→午後の長浜）                = data/routes/kohoku-early.json
      island （7:00発：朝の桜→竹生島）                    = data/routes/kohoku-island.json
    ?course=early などでも開ける
  - 春以外（SEASON_FROM〜SEASON_TO の外）に開くと「春のマップ」の一文（i18n.js の offKicker・offHow・offHowText・offLead・offNote）を
    使い方・紹介ページ・一覧に出し、どのスポットも開いて最初に offHead・offText のお知らせを出す。日付は毎年同じ（月-日で見る）
- 2026-11-22 にコースを分けて番号の順が変わった。「行った」印・回り方・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-kohoku-visited-late-b など）になるので、前の印は引き継がれない
- kohoku/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
  （2026-11-22 までは css +100・i18n/app +101 だったので、bump は 102 から）
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

SEASON_FROM, SEASON_TO = '03-25', '04-20'
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='kohoku', i18n='KOHOKU_I18N', count=7, data_v=4, bump=102, keyv='-b',
    head='京都から日帰り 海津大崎の桜と長浜（竹生島・大浦はコースを分けた）',
    title='京都から日帰り 海津大崎の桜と長浜｜春の4コース Kaizu-Osaki MAP',
    desc='春のマップ。京都駅からJR湖西線でマキノへ。琵琶湖岸に約4km続く海津大崎の桜並木を歩いて、夕方は長浜の豊公園と古い町並みへ。朝7時発の長浜・竹生島のコース、永原まで歩き通すコースも。時刻表、お昼、トイレ、最終の電車つき。A spring day trip from Kyoto Station: the cherry avenue of Kaizu-Osaki on Lake Biwa and an evening in Nagahama, with 7:00 courses for the town or Chikubushima, a long walk to Nagahara, train times, lunch and last trains.',
    main='海津大崎の桜と長浜', alt='Kaizu-Osaki &amp; Nagahama', sub='京都から日帰り Kaizu-Osaki MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js
APP = f'{R}/kohoku/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("kohoku.json と kohoku-early.json（コースで読み分ける。",
    "kohoku.json・kohoku-through.json・kohoku-early.json・kohoku-island.json（コースで読み分ける。")
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_kohoku.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""", """  // コース: late（桜並木を往復）・through（永原まで歩く）・early（朝の桜→長浜）・island（朝の桜→竹生島）。
  // コースごとにデータファイルが別で、スポットの番号も変わる。一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""")
rep("""  var course = { id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) };
  if (course.id !== 'early') course.id = 'late';
  course.file = 'kohoku' + (course.id === 'early' ? '-early' : '') + '.json';
""", f"""  var COURSE_FILES = {{ late: 'kohoku.json', through: 'kohoku-through.json', early: 'kohoku-early.json', island: 'kohoku-island.json' }};
  var course = {{ id: (location.search.match(/[?&]course=(late|through|early|island)/) || [])[1] || load(KEY_COURSE) }};
  if (!COURSE_FILES.hasOwnProperty(course.id)) course.id = 'late';
  course.file = COURSE_FILES[course.id];
  var md = todayJST().slice(5);     // 月-日
  var offSeason = md < '{SEASON_FROM}' || md > '{SEASON_TO}';
""")
rep("""    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
  });
""", """    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
    // 春以外は「春のマップ」の一文を先に出す
    if (offSeason) {
      I18N[l].intro.kicker = I18N[l].offKicker;
      // 使い方の1つ目は、開いて最初に見える場所
      I18N[l].intro.how[0].title = I18N[l].offHow;
      I18N[l].intro.how[0].text = I18N[l].offHowText + I18N[l].intro.how[0].text;
      I18N[l].intro.lead = I18N[l].offLead + I18N[l].intro.lead;
      I18N[l].listNote = I18N[l].offNote + I18N[l].listNote;
    }
  });
  if (offSeason) document.body.classList.add('off-season');
""")
# 春以外は、どのスポットを開いても最初に「春のマップです」
rep("""    var notices = (s.notices || []).filter(function (n) { return inRange(n.from, n.to); });
""", """    var notices = (s.notices || []).filter(function (n) { return inRange(n.from, n.to); });
    if (offSeason) notices.unshift({ head: { ja: I18N.ja.offHead, en: I18N.en.offHead }, text: { ja: I18N.ja.offText, en: I18N.en.offText } });
""")
open(APP, 'w', encoding='utf-8').write(s)

# index.html（ボタンを4つに）
PAGE = f'{R}/kohoku/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">出発時間・歩く距離</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間・歩く距離">\n'
    '      <button type="button" data-course="late" data-t="courseLate">9:45ごろ発\n桜並木→夕方の長浜</button>\n'
    '      <button type="button" data-course="through" data-t="courseThrough">9:45ごろ発\n永原まで歩き通す</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">7:00発\n朝の桜→昼の長浜</button>\n'
    '      <button type="button" data-course="island" data-t="courseIsland">7:00発\n朝の桜→竹生島</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css
CSS = f'{R}/kohoku/css/style.css'
open(CSS, 'a', encoding='utf-8').write("""/* 湖北: コースのボタンは2列×2段。春以外は一覧の一文を目立たせる */
.coursesw button { min-height: 52px; font-size: 13px; }
.coursesw button:nth-child(even) { border-left: 1px solid var(--ink); }
.coursesw button:nth-child(n+3) { border-top: 1px solid var(--ink); }
.off-season .list-note { padding: 8px 10px; background: var(--warn-soft); color: #4A3209; }
""")
print('patched kohoku (4 courses, season)')
