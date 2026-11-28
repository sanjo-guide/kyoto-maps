#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を yawata/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_yawata.py
- 共通の差分（コースの切り替え・写真のクレジット・要確認の一文など）は scripts/sync_higashiyama.py にあり、
  ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、淀・八幡だけの差分をかける:
  - コースは3つ（scripts/build_yawata_data.py が作る）。ボタンは縦に3つ
      kawazu（3月：淀の河津桜）= data/routes/yawata.json
      sakura（4月：背割堤の桜）= data/routes/yawata-sakura.json
      early （4月：背割堤の開園へ）= data/routes/yawata-early.json
    何も選んでいなければ、SAKURA_FROM〜SAKURA_TO（月-日）に開くと sakura、それ以外は kawazu。?course=sakura でも開ける
  - 春以外（SEASON_FROM〜SEASON_TO の外）に開くと「春のマップ」の一文（i18n.js の offKicker・offHow・offHowText・offLead・offNote）を
    使い方・紹介ページ・一覧に出す。日付は毎年同じ（月-日で見る）
- 2026-11-22 にコースを分けて番号の順が変わった。「行った」印・回り方・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-yawata-visited-v2-kawazu など）になるので、前の印は引き継がれない
- yawata/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
  （2026-11-22 までは css +100・i18n/app +101 だったので、bump は 102 から）
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

SEASON_FROM, SEASON_TO = '03-01', '04-15'
SAKURA_FROM, SAKURA_TO = '03-25', '04-30'
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='yawata', i18n='YAWATA_I18N', count=3, data_v=3, bump=103,
    head='京都 淀・八幡の桜（淀水路の河津桜・石清水八幡宮・背割堤）',
    title='京都 淀・八幡の桜｜3月の河津桜・4月の背割堤 Yawata MAP',
    desc='春のマップ。3月は淀水路の河津桜、3月末〜4月上旬は背割堤の桜のトンネル。三条から京阪で、石清水八幡宮とケーブル、門前のお昼、伏見の酒蔵、夜桜まで。時期と出発時間で選べる3コース。A spring map south of Kyoto by Keihan: Kawazu cherries at Yodo in March or the Sewaritei cherry avenue in late March and early April, with Iwashimizu Hachimangu, lunch, Fushimi and an evening in town.',
    main='淀・八幡の桜', alt='Yodo & Yawata cherries', sub='京都 Yawata MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js
APP = f'{R}/yawata/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("yawata.json と yawata-early.json（コースで読み分ける。",
    "yawata.json・yawata-sakura.json・yawata-early.json（コースで読み分ける。")
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_yawata.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""", """  // コース: kawazu（3月）・sakura（4月）・early（4月、開園へ）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=sakura でも開ける
""")
rep("""  var course = { id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) };
  if (course.id !== 'early') course.id = 'late';
  course.file = 'yawata' + (course.id === 'early' ? '-early' : '') + '.json';
""", f"""  var COURSE_FILES = {{ kawazu: 'yawata.json', sakura: 'yawata-sakura.json', early: 'yawata-early.json' }};
  var md = todayJST().slice(5);     // 月-日
  var course = {{ id: (location.search.match(/[?&]course=(kawazu|sakura|early)/) || [])[1] || load(KEY_COURSE) }};
  // 何も選んでいなければ、咲く時期に合わせる
  if (!COURSE_FILES.hasOwnProperty(course.id)) course.id = md >= '{SAKURA_FROM}' && md <= '{SAKURA_TO}' ? 'sakura' : 'kawazu';
  course.file = COURSE_FILES[course.id];
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
open(APP, 'w', encoding='utf-8').write(s)

# index.html（ボタンを3つに）
PAGE = f'{R}/yawata/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">行く時期・出発時間</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="行く時期・出発時間">\n'
    '      <button type="button" data-course="kawazu" data-t="courseKawazu">3月：淀の河津桜（9:30ごろ発）</button>\n'
    '      <button type="button" data-course="sakura" data-t="courseSakura">3月末〜4月上旬：背割堤の桜（9:30ごろ発）</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">3月末〜4月上旬：背割堤の開園9:00へ（8:10ごろ発）</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css
CSS = f'{R}/yawata/css/style.css'
open(CSS, 'a', encoding='utf-8').write("""/* 淀・八幡: コースのボタンは3つを縦に。春以外は一覧の一文を目立たせる */
.coursesw { grid-template-columns: 1fr; }
.coursesw button { padding: 8px 12px; text-align: left; font-size: 13.5px; }
.coursesw button + button { border-top: 1px solid var(--ink); }
.off-season .list-note { padding: 8px 10px; background: var(--warn-soft); color: #4A3209; }
""")
print('patched yawata (3 courses, season)')
