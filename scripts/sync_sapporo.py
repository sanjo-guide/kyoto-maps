#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を sapporo/ に写し、札幌用の差分をかけ直す。

使い方: python3 scripts/sync_sapporo.py   （データを直したときは、先に python3 scripts/build_sapporo_data.py）
- 共通の差分（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）は
  scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、札幌だけの差分をかける（形は scripts/sync_kohoku.py と同じ。コースが3つあるため）:
      late     （定番：9:15発。赤れんが→時計台→大通→二条市場→ビール博物館→藻岩山→すすきの）= data/routes/sapporo.json
      early    （朝いちばん：7:00発。場外市場→北大→街なか→狸小路→ビール博物館→藻岩山）  = data/routes/sapporo-early.json
      maruyama （もう1日あるなら：9:15発。北海道神宮→円山動物園→白い恋人パーク→大通の夜）= data/routes/sapporo-maruyama.json
    最初に開くのは late。?course=early / ?course=maruyama でも開ける。ボタンの文言は sapporo/js/i18n.js の
    courseLate・courseEarly・courseMaruyama
- 「行った」印・回り方・選んだ場所の保存キーはコースごと（kyoto-maps-sapporo-visited-late など）
- 日付でコースを自動で切り替える仕組みは入れていない（3つとも一年中使えるコースで、季節の違いは
  notices の from / to と rows の until / from で出している）
- sapporo/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='sapporo', i18n='SAPPORO_I18N', count=10, data_v=1, bump=100,
    head='札幌市内で1日（赤れんが庁舎・大通公園・ビール博物館・藻岩山の夜景）',
    title='札幌市内で1日｜赤れんが庁舎・大通公園・藻岩山の夜景 Sapporo City MAP',
    desc='札幌駅〜大通〜すすきののホテルから1日。赤れんが庁舎と時計台、大通公園のテレビ塔、二条市場の海鮮、サッポロビール博物館、藻岩山の夜景、すすきのの味噌ラーメンへ。朝7時に出る市場と北海道大学のコース、円山動物園と白い恋人パークのコースも。冬の服装、ICカードと1日乗車券、イルミネーションと雪まつりの日程つき。A day in central Sapporo from a hotel by the station, Odori or Susukino: the Red Brick Office and Clock Tower, the TV Tower, seafood at Nijo Market, the Sapporo Beer Museum, the night view from Mt. Moiwa and miso ramen in Susukino, with an early course for the morning market and the university, a second-day course for Maruyama Zoo and Shiroi Koibito Park, and notes on winter clothing, IC cards and day passes, the illuminations and the Snow Festival.',
    main='札幌市内で1日', alt='A day in Sapporo', sub='札幌 Sapporo City MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js（コースを3つに）
APP = f'{R}/sapporo/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("sapporo.json と sapporo-early.json（コースで読み分ける。",
    "sapporo.json・sapporo-early.json・sapporo-maruyama.json（コースで読み分ける。")
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_sapporo.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""", """  // コース: late（定番・9:15発）・early（朝いちばん・7:00発）・maruyama（もう1日あるなら）。
  // コースごとにデータファイルが別で、スポットの番号も変わる。一覧の上のボタン（data-course）で切り替える。
  // ?course=early / ?course=maruyama でも開ける
""")
rep("""  var course = { id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) };
  if (course.id !== 'early') course.id = 'late';
  course.file = 'sapporo' + (course.id === 'early' ? '-early' : '') + '.json';
""", """  var COURSE_FILES = { late: 'sapporo.json', early: 'sapporo-early.json', maruyama: 'sapporo-maruyama.json' };
  var course = { id: (location.search.match(/[?&]course=(late|early|maruyama)/) || [])[1] || load(KEY_COURSE) };
  if (!COURSE_FILES.hasOwnProperty(course.id)) course.id = 'late';
  course.file = COURSE_FILES[course.id];
""")
open(APP, 'w', encoding='utf-8').write(s)

# index.html（ボタンを3つに）
PAGE = f'{R}/sapporo/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m, 'コース切り替えの段が見つからない'
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">コース</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="コース">\n'
    '      <button type="button" data-course="late" data-t="courseLate">定番（9〜10時発）</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">朝いちばん（7:00発）</button>\n'
    '      <button type="button" data-course="maruyama" data-t="courseMaruyama">円山と白い恋人パーク</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css（コースのボタンは縦に3つ。画面が広いと横に3つ）
open(f'{R}/sapporo/css/style.css', 'a', encoding='utf-8').write("""/* 札幌: コースのボタンは3つ。狭い画面では縦に並べる */
.coursesw { grid-template-columns: 1fr; }
.coursesw button { min-height: 42px; font-size: 13px; line-height: 1.35; white-space: pre-line; }
.coursesw button + button { border-top: 1px solid var(--ink); }
@media (min-width: 560px) {
  .coursesw { grid-template-columns: 1fr 1fr 1fr; }
  .coursesw button + button { border-top: 0; border-left: 1px solid var(--ink); }
}
""")
print('patched sapporo (3 courses: late / early / maruyama)')
