#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を hieizan/ に写し、比叡山延暦寺と坂本用の差分をかけ直す。

使い方: python3 scripts/sync_hieizan.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・写真のクレジット・要確認の一文・最初に映す範囲など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ（2026-11-22）：late＝山を越える（hieizan.json。坂本から上って八瀬へ下りる。山内のバスが走る3月20日〜12月6日）、
  early＝冬：坂本から往復（hieizan-early.json）。early / late はコース切り替えの仕組みの名前を借りているだけで、どちらも三条京阪9:01発。
  どちらも scripts/build_hieizan_data.py が作る。ボタンの文言は hieizan/js/i18n.js の courseEarly・courseLate
- このマップだけの差分（sync_higashiyama.py を実行したあとにかける）:
  - 一覧の上のボタンは「山を越える」を先（左）に
  - コースを選んだことがない人には、日付で最初のコースを決める：12月7日〜3月19日は冬のコース
    （2026年の山内シャトルバスの運行期間 3/20〜12/6 から。2027年の期間が発表されたら WINTER_FROM / WINTER_TO を直す）
- 「行った」印・選んだ場所の保存キーは、コースごとに kyoto-maps-hieizan-…-early / -late（前のキーとは別になる）
- hieizan/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINTER_FROM, WINTER_TO = 1207, 319   # 月×100＋日

CFG = dict(
    id='hieizan', i18n='HIEIZAN_I18N', count=11, data_v=3, bump=102,
    head='京都から日帰り 比叡山延暦寺と坂本',
    title='京都から日帰り 比叡山延暦寺と坂本 Mt. Hiei MAP',
    desc='三条京阪9:01の電車で坂本へ。日吉大社から日本一長いケーブルカーで延暦寺の東塔へ上がり、峰道でお昼、横川・西塔を山の上のバスで回って、ロープウェイで京都側の八瀬へ下りる1日ルートマップ。冬は坂本から往復するコースも。乗り遅れたときの次の便、最後のバス、夜の過ごし方まで。A day trip from Kyoto over Mt. Hiei: Sakamoto and Hiyoshi Taisha, the Sakamoto Cable up to Enryaku-ji, lunch at Minemichi, Yokawa and Saito by the mountain bus, and down to Yase by ropeway, with a winter course up and back from Sakamoto, fallback times and the last buses.',
    main='比叡山延暦寺と坂本', alt='Mt. Hiei & Sakamoto', sub='京都から日帰り Mt. Hiei MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def fix(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:80], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


fix(f'{R}/hieizan/js/app.js', [(
    "  if (course.id !== 'early') course.id = 'late';",
    f"""  // コースを選んだことがない人には、日付で最初のコースを決める（12月7日〜3月19日は山内のバスが走らないので冬のコース。scripts/sync_hieizan.py）
  if (!course.id) {{
    var today = new Date(), md = (today.getMonth() + 1) * 100 + today.getDate();
    course.id = md >= {WINTER_FROM} || md <= {WINTER_TO} ? 'early' : 'late';
  }}
  if (course.id !== 'early') course.id = 'late';""")])
fix(f'{R}/hieizan/index.html', [(
    '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
    '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
    '      <button type="button" data-course="late" data-t="courseLate">山を越える</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">冬：坂本から往復</button>\n')])
print('hieizan: winter default and button order applied')
