#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を hakodate/ に写し、函館用の差分をかけ直す。

使い方: python3 scripts/sync_hakodate.py   （データを直したときは、先に python3 scripts/build_hakodate_data.py）
- 共通の差分（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）は
  scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、函館だけの差分をかける（形は scripts/sync_otaru.py と同じ）:
  - コースは3つ（scripts/build_hakodate_data.py が作る）。ボタンは横に3つ
      late    （9〜10時に出る：朝市・五稜郭・元町・函館山の夜景。最初に開く）= data/routes/hakodate.json
      early   （6時台に出る：朝の朝市と元町・五稜郭・函館山・湯の川）       = data/routes/hakodate-early.json
      sapporo （札幌から1泊2日）                                          = data/routes/hakodate-sapporo.json
    ?course=early などでも開ける。ボタンの文言は hakodate/js/i18n.js の courseLate・courseEarly・courseSapporo
- 「行った」印・回り方・選んだ場所の保存キーはコースごと（kyoto-maps-hakodate-visited-late など）
- hakodate/js/i18n.js はこのマップ専用なので触らない（作り直すときは scratchpad の gen_i18n.py か、直接直す）。
  テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='hakodate', i18n='HAKODATE_I18N', count=12, data_v=1, bump=101,
    head='函館で1日',
    title='函館で1日｜朝市・五稜郭・元町・函館山の夜景・湯の川温泉 Hakodate MAP',
    desc='函館駅のまわりのホテルから回る函館の1日。朝市の朝ごはん、五稜郭タワーと五稜郭公園、八幡坂と元町の教会、日の入りに合わせた函館山ロープウェイの夜景、夜の金森赤レンガ倉庫、湯の川温泉。朝6時台に出るコースと、札幌から特急北斗で行く1泊2日のコースも。市電の乗り方、冬の坂道、タトゥーと温泉のことつき。One day in Hakodate from a hotel near the station: breakfast at the morning market, Goryokaku Tower and park, Hachiman-zaka and the Motomachi churches, the Mt. Hakodate night view timed to sunset, the red-brick warehouses after dark and Yunokawa Onsen, with an early course, a two-day trip from Sapporo by the Hokuto limited express, tram tips and winter advice.',
    main='函館', alt='Hakodate', sub='函館で1日 Hakodate MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js
APP = f'{R}/hakodate/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("hakodate.json と hakodate-early.json（コースで読み分ける。",
    "hakodate.json・hakodate-early.json・hakodate-sapporo.json（コースで読み分ける。")
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_hakodate.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""", """  // コース: late（9〜10時に出る）・early（6時台に出る）・sapporo（札幌から1泊2日）。
  // コースごとにデータファイルが別で、スポットの番号も変わる。一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""")
rep("""  var course = { id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) };
  if (course.id !== 'early') course.id = 'late';
  course.file = 'hakodate' + (course.id === 'early' ? '-early' : '') + '.json';
""", """  var COURSE_FILES = { late: 'hakodate.json', early: 'hakodate-early.json', sapporo: 'hakodate-sapporo.json' };
  var course = { id: (location.search.match(/[?&]course=(late|early|sapporo)/) || [])[1] || load(KEY_COURSE) };
  if (!COURSE_FILES.hasOwnProperty(course.id)) course.id = 'late';
  course.file = COURSE_FILES[course.id];
""")
open(APP, 'w', encoding='utf-8').write(s)

# index.html（ボタンを3つに）
PAGE = f'{R}/hakodate/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">コース</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="コース">\n'
    '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出る\n朝市・五稜郭・夜景</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">6時台に出る\n朝の元町・湯の川</button>\n'
    '      <button type="button" data-course="sapporo" data-t="courseSapporo">札幌から\n1泊2日</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css（ボタンは横に3つ）
CSS = f'{R}/hakodate/css/style.css'
open(CSS, 'a', encoding='utf-8').write("""/* 函館: コースのボタンは横に3つ */
.coursesw { grid-template-columns: 1fr 1fr 1fr; }
.coursesw button { min-height: 52px; font-size: 12.5px; }
.coursesw button + button { border-left: 1px solid var(--ink); }
""")
print('patched hakodate (3 courses)')
