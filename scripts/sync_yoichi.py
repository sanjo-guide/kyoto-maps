#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を yoichi/ に写し、余市用の差分をかけ直す。

使い方: python3 scripts/sync_yoichi.py   （データを直したときは、先に python3 scripts/build_yoichi_data.py）
- 共通の差分（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）は
  scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、余市だけの差分をかける（形は scripts/sync_hieizan.py と scripts/sync_otaru.py と同じ）:
  - コースは2つ（scripts/build_yoichi_data.py が作る）。early / late はコース切り替えの仕組みの名前を借りているだけ
      late  （4月中旬〜12月中旬：蒸溜所・ワイナリー・ニシン漁の浜の史跡・温泉）= data/routes/yoichi.json
      early （冬：12月中旬〜4月上旬。浜の史跡が閉まるので、蒸溜所・ワイナリー・浜・温泉）= data/routes/yoichi-winter.json
    ?course=early などでも開ける。ボタンの文言は yoichi/js/i18n.js の courseLate・courseEarly
  - 一覧の上のボタンは「4月中旬〜12月中旬」を先（左）に
  - コースを選んだことがない人には、日付で最初のコースを決める：12月14日〜4月10日は冬のコース
    （福原漁場・運上家・水産博物館の2026年の開館期間 4/11〜12/13 から。2027年の期間が発表されたら WINTER_FROM / WINTER_TO を直す）
- 「行った」印・回り方・選んだ場所の保存キーはコースごと（kyoto-maps-yoichi-visited-late など）
- yoichi/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINTER_FROM, WINTER_TO = 1214, 410   # 月×100＋日
CFG = dict(
    id='yoichi', i18n='YOICHI_I18N', count=9, data_v=1, bump=100,
    head='余市（札幌から日帰り）',
    title='余市｜札幌から日帰り ニッカの蒸溜所・ワイナリー・ニシン漁の浜 Yoichi MAP',
    desc='札幌から日帰りの余市。8:41の電車で余市へ、ニッカウヰスキー余市蒸溜所のツアー（予約制）とお昼、余市ワイナリー、ニシン漁の時代の旧余市福原漁場と旧下ヨイチ運上家、シリパ岬の見える浜、温泉と回転ずしまでの1日。冬（12月中旬〜4月上旬）のコースと、電車・高速バスの時刻、タトゥーや支払いの注意つき。A day trip from Sapporo to Yoichi: a booked tour of the Nikka Yoichi distillery and lunch, Yoichi Winery, the herring-era Fukuhara fishery and Unjoya, the beach facing Cape Shiripa, a hot spring and sushi, with a winter course, train and bus times, and notes on tattoos and payment.',
    main='余市', alt='Yoichi', sub='札幌から日帰り Yoichi MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def fix(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:80], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


fix(f'{R}/yoichi/js/app.js', [
    ("yoichi.json と yoichi-early.json（コースで読み分ける。",
     "yoichi.json と yoichi-winter.json（コースで読み分ける。"),
    ("違いは scripts/sync_higashiyama.py の説明を参照",
     "違いは scripts/sync_yoichi.py と scripts/sync_higashiyama.py の説明を参照"),
    ("  if (course.id !== 'early') course.id = 'late';\n  course.file = 'yoichi' + (course.id === 'early' ? '-early' : '') + '.json';",
     f"""  // コースを選んだことがない人には、日付で最初のコースを決める（12月14日〜4月10日は浜の史跡が閉まるので冬のコース。scripts/sync_yoichi.py）
  if (!course.id) {{
    var today = new Date(), md = (today.getMonth() + 1) * 100 + today.getDate();
    course.id = md >= {WINTER_FROM} || md <= {WINTER_TO} ? 'early' : 'late';
  }}
  if (course.id !== 'early') course.id = 'late';
  course.file = course.id === 'early' ? 'yoichi-winter.json' : 'yoichi.json';"""),
])
fix(f'{R}/yoichi/index.html', [(
    '    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
    '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
    '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
    '    <p class="sw-label" data-t="swCourse">季節</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="季節">\n'
    '      <button type="button" data-course="late" data-t="courseLate">4月中旬〜12月中旬\n浜の史跡も</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">冬\n12月中旬〜4月上旬</button>\n')])
open(f'{R}/yoichi/css/style.css', 'a', encoding='utf-8').write("""/* 余市: コースのボタンは2行 */
.coursesw button { min-height: 52px; font-size: 12.5px; white-space: pre-line; }
""")
print('yoichi: winter default, file names and button order applied')
