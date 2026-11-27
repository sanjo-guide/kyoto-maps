#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を otaru/ に写し、小樽用の差分をかけ直す。

使い方: python3 scripts/sync_otaru.py   （データを直したときは、先に python3 scripts/build_otaru_data.py）
- 共通の差分（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）は
  scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、小樽だけの差分をかける（形は scripts/sync_kohoku.py と同じ）:
  - コースは3つ（scripts/build_otaru_data.py が作る）。ボタンは横に3つ
      late   （9〜10時に出る：運河・堺町・天狗山の夜景。最初に開く）= data/routes/otaru.json
      early  （7時台に出る：朝の運河と市場・祝津）             = data/routes/otaru-early.json
      yoichi （余市の蒸溜所＋午後の小樽）                      = data/routes/otaru-yoichi.json
    ?course=early などでも開ける。ボタンの文言は otaru/js/i18n.js の courseLate・courseEarly・courseYoichi
- 「行った」印・回り方・選んだ場所の保存キーはコースごと（kyoto-maps-otaru-visited-late など）
- otaru/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='otaru', i18n='OTARU_I18N', count=13, data_v=1, bump=100,
    head='小樽（札幌から日帰り）',
    title='小樽｜札幌から日帰り 運河・堺町・天狗山の夜景・余市 Otaru MAP',
    desc='札幌から日帰りの小樽。三角市場、旧手宮線の跡と北運河、運河と銀行街、堺町通り、夕暮れの浅草橋、天狗山ロープウエイの夜景と晩ごはん。朝7時台に出て祝津へ行くコースと、余市のニッカの蒸溜所に寄るコースも。冬の歩き方、バスの時刻、新千歳空港への電車つき。A day trip from Sapporo to Otaru: the market, the old Temiya railway and the North Canal, the canal and old bank street, Sakaimachi, dusk at Asakusa Bridge and the Mt. Tengu night view, with an early course to Shukutsu and one via the Nikka Yoichi distillery, winter tips, bus times and trains to New Chitose Airport.',
    main='小樽', alt='Otaru', sub='札幌から日帰り Otaru MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js
APP = f'{R}/otaru/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("otaru.json と otaru-early.json（コースで読み分ける。",
    "otaru.json・otaru-early.json・otaru-yoichi.json（コースで読み分ける。")
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_otaru.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""", """  // コース: late（9〜10時に出る）・early（7時台に出る）・yoichi（余市の蒸溜所＋午後の小樽）。
  // コースごとにデータファイルが別で、スポットの番号も変わる。一覧の上のボタン（data-course）で切り替える。?course=early でも開ける
""")
rep("""  var course = { id: (location.search.match(/[?&]course=(early|late)/) || [])[1] || load(KEY_COURSE) };
  if (course.id !== 'early') course.id = 'late';
  course.file = 'otaru' + (course.id === 'early' ? '-early' : '') + '.json';
""", """  var COURSE_FILES = { late: 'otaru.json', early: 'otaru-early.json', yoichi: 'otaru-yoichi.json' };
  var course = { id: (location.search.match(/[?&]course=(late|early|yoichi)/) || [])[1] || load(KEY_COURSE) };
  if (!COURSE_FILES.hasOwnProperty(course.id)) course.id = 'late';
  course.file = COURSE_FILES[course.id];
""")
open(APP, 'w', encoding='utf-8').write(s)

# index.html（ボタンを3つに）
PAGE = f'{R}/otaru/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">コース</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="コース">\n'
    '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出る\n運河・堺町・夜景</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">7時台に出る\n朝の運河・祝津</button>\n'
    '      <button type="button" data-course="yoichi" data-t="courseYoichi">余市の蒸溜所\n＋午後の小樽</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css（ボタンは横に3つ）
CSS = f'{R}/otaru/css/style.css'
open(CSS, 'a', encoding='utf-8').write("""/* 小樽: コースのボタンは横に3つ */
.coursesw { grid-template-columns: 1fr 1fr 1fr; }
.coursesw button { min-height: 52px; font-size: 12.5px; }
.coursesw button + button { border-left: 1px solid var(--ink); }
""")
print('patched otaru (3 courses)')
