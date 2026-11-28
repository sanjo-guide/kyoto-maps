#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を biei/ に写し、美瑛用の差分をかけ直す。

使い方: python3 scripts/sync_biei.py   （データを直したときは、先に python3 scripts/build_biei_data.py）
- 共通の差分（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）は
  scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、美瑛だけの差分をかける（形は scripts/sync_otaru.py と scripts/sync_yoichi.py を合わせたもの）:
  - コースは3つ（scripts/build_biei_data.py が作る）。ボタンは横に3つ。late / early はコース切り替えの仕組みの名前を借りているだけ
      late   （雪のない季節：自転車で丘・青い池・白金温泉）  = data/routes/biei.json
      early  （冬：クリスマスツリーの木・白金温泉・青い池のライトアップ）= data/routes/biei-winter.json
      furano （花畑：ファーム富田・四季彩の丘）              = data/routes/biei-furano.json
    ?course=early などでも開ける。ボタンの文言は biei/js/i18n.js の courseLate・courseEarly・courseFurano
  - コースを選んだことがない人には、日付で最初のコースを決める：11月1日〜4月20日は冬のコース
    （雪で自転車が使えず、青い池が雪の下になる時期。青い池のライトアップは2026年10月22日〜2027年4月21日。
      次の冬の期間が発表されたら WINTER_FROM / WINTER_TO を直す）
- 「行った」印・回り方・選んだ場所の保存キーはコースごと（kyoto-maps-biei-visited-late など）
- biei/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINTER_FROM, WINTER_TO = 1101, 420   # 月×100＋日
CFG = dict(
    id='biei', i18n='BIEI_I18N', count=10, data_v=1, bump=101,
    head='美瑛・青い池と富良野（旭川から日帰り）',
    title='美瑛・青い池と富良野｜旭川から日帰り 丘・白金温泉・冬のライトアップ Biei MAP',
    desc='旭川から日帰りの美瑛。車なしで、JR富良野線と道北バスで回ります。雪のない季節は電動自転車でパッチワークの路の丘、午後はバスで白金青い池・白ひげの滝・白金温泉。冬はクリスマスツリーの木と、青い池のライトアップ（最終バスは18:05）。花の季節にはファーム富田と四季彩の丘のコースも。バスと電車の時刻、タトゥーや寒さの注意つき。A car-free day trip from Asahikawa to Biei by the JR Furano Line and Dohoku Bus: the Patchwork Road hills by e-bike, the Shirogane Blue Pond, Shirahige Falls and a hot spring; in winter the Christmas Tree and the Blue Pond light-up (last bus 18:05); and a flower-season course to Farm Tomita and Shikisai-no-oka, with bus and train times and notes on tattoos and the cold.',
    main='美瑛・青い池', alt='Biei', sub='旭川から日帰り Biei MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js
APP = f'{R}/biei/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("biei.json と biei-early.json（コースで読み分ける。",
    "biei.json・biei-winter.json・biei-furano.json（コースで読み分ける。")
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_biei.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""", """  // コース: late（雪のない季節）・early（冬）・furano（花畑：ファーム富田と四季彩の丘）。
  // コースごとにデータファイルが別で、スポットの番号も変わる。一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""")
rep("""  var course = { id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) };
  if (course.id !== 'early') course.id = 'late';
  course.file = 'biei' + (course.id === 'early' ? '-early' : '') + '.json';
""", f"""  var COURSE_FILES = {{ late: 'biei.json', early: 'biei-winter.json', furano: 'biei-furano.json' }};
  var course = {{ id: (location.search.match(/[?&]course=(late|early|furano)/) || [])[1] || load(KEY_COURSE) }};
  // コースを選んだことがない人には、日付で最初のコースを決める（11月1日〜4月20日は冬のコース。scripts/sync_biei.py）
  if (!course.id) {{
    var today = new Date(), md = (today.getMonth() + 1) * 100 + today.getDate();
    course.id = md >= {WINTER_FROM} || md <= {WINTER_TO} ? 'early' : 'late';
  }}
  if (!COURSE_FILES.hasOwnProperty(course.id)) course.id = 'late';
  course.file = COURSE_FILES[course.id];
""")
open(APP, 'w', encoding='utf-8').write(s)

# index.html（ボタンを3つに）
PAGE = f'{R}/biei/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">季節とコース</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="季節とコース">\n'
    '      <button type="button" data-course="early" data-t="courseEarly">冬 11〜4月中旬\n青い池のライトアップ</button>\n'
    '      <button type="button" data-course="late" data-t="courseLate">雪のない季節\n丘・青い池・温泉</button>\n'
    '      <button type="button" data-course="furano" data-t="courseFurano">花畑 5〜10月\nファーム富田も</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css（ボタンは横に3つ）
CSS = f'{R}/biei/css/style.css'
open(CSS, 'a', encoding='utf-8').write("""/* 美瑛: コースのボタンは横に3つ */
.coursesw { grid-template-columns: 1fr 1fr 1fr; }
.coursesw button { min-height: 52px; font-size: 12px; white-space: pre-line; }
.coursesw button + button { border-left: 1px solid var(--ink); }
""")
print('patched biei (3 courses, winter default by date)')
