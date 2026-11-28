#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を asahikawa/ に写し、旭川用の差分をかけ直す。

使い方: python3 scripts/sync_asahikawa.py   （データを直したときは、先に python3 scripts/build_asahikawa_data.py）
- 共通の差分（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）は
  scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、旭川だけの差分をかける（形は scripts/sync_yoichi.py と同じ）:
  - コースは2つ（scripts/build_asahikawa_data.py が作る）。early / late はコース切り替えの仕組みの名前を借りているだけ
      early （冬：旭山動物園の冬期開園 11/11〜4/7、10:30〜15:30）= data/routes/asahikawa-winter.json
      late  （雪のない季節：夏期開園 4/29〜11/3、9:30〜17:15）= data/routes/asahikawa.json
    ?course=early などでも開ける。ボタンの文言は asahikawa/js/i18n.js の courseLate・courseEarly
  - 一覧の上のボタンは「冬」を先（左）に
  - コースを選んだことがない人には、日付で最初のコースを決める：11月4日〜4月28日は冬のコース
    （動物園の夏期開園が4/29〜11/3 のため。休園の 11/4〜11/10 と 4/8〜4/28 は冬のコースで開き、休園のお知らせが出る。
      動物園の開園日が変わったら WINTER_FROM / WINTER_TO を直す）
- 「行った」印・回り方・選んだ場所の保存キーはコースごと（kyoto-maps-asahikawa-visited-late など）
- asahikawa/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINTER_FROM, WINTER_TO = 1104, 428   # 月×100＋日
CFG = dict(
    id='asahikawa', i18n='ASAHIKAWA_I18N', count=9, data_v=2, bump=101,
    head='旭山動物園と旭川の町',
    title='旭山動物園と旭川の町｜旭川駅から1日 Asahiyama Zoo & Asahikawa MAP',
    desc='旭川駅のまわりのホテルから1日。朝のバスで旭山動物園へ（冬は11:00のペンギンの散歩）、午後は酒蔵（男山・髙砂酒造）か三浦綾子記念文学館と見本林、夕方は買物公園で旭川ラーメン、常磐公園と旭橋、夜は5・7小路ふらりーとで新子焼き。冬と雪のない季節の2つの時間割、バスと特急の時刻、支払いと寒さの注意つき。A day in Asahikawa from a hotel near the station: the morning bus to Asahiyama Zoo (penguin walk at 11:00 in winter), a sake brewery or the Miura Ayako museum and its forest, Asahikawa ramen on the pedestrian mall, Tokiwa Park and Asahibashi Bridge, and grilled chicken in Furarito alley, with winter and snow-free timetables, bus and train times, and notes on payment and the cold.',
    main='旭山動物園と旭川の町', alt='Asahiyama Zoo & Asahikawa', sub='旭川駅から1日 Asahikawa MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def fix(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:80], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


fix(f'{R}/asahikawa/js/app.js', [
    ("asahikawa.json と asahikawa-early.json（コースで読み分ける。",
     "asahikawa.json と asahikawa-winter.json（コースで読み分ける。"),
    ("違いは scripts/sync_higashiyama.py の説明を参照",
     "違いは scripts/sync_asahikawa.py と scripts/sync_higashiyama.py の説明を参照"),
    ("  if (course.id !== 'early') course.id = 'late';\n  course.file = 'asahikawa' + (course.id === 'early' ? '-early' : '') + '.json';",
     f"""  // コースを選んだことがない人には、日付で最初のコースを決める（11月4日〜4月28日は冬のコース。scripts/sync_asahikawa.py）
  if (!course.id) {{
    var today = new Date(), md = (today.getMonth() + 1) * 100 + today.getDate();
    course.id = md >= {WINTER_FROM} || md <= {WINTER_TO} ? 'early' : 'late';
  }}
  if (course.id !== 'early') course.id = 'late';
  course.file = course.id === 'early' ? 'asahikawa-winter.json' : 'asahikawa.json';"""),
])
fix(f'{R}/asahikawa/index.html', [(
    '    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
    '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
    '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
    '    <p class="sw-label" data-t="swCourse">季節</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="季節">\n'
    '      <button type="button" data-course="early" data-t="courseEarly">冬\n11月11日〜4月7日</button>\n'
    '      <button type="button" data-course="late" data-t="courseLate">雪のない季節\n4月29日〜11月3日</button>\n')])
open(f'{R}/asahikawa/css/style.css', 'a', encoding='utf-8').write("""/* 旭川: コースのボタンは2行 */
.coursesw button { min-height: 52px; font-size: 12.5px; white-space: pre-line; }
""")
print('asahikawa: winter default, file names and button labels applied')
