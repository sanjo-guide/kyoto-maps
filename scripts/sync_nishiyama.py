#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を nishiyama/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_nishiyama.py
- 差分は東山マップと同じ（コースの切り替え・写真のクレジット・要確認の一文など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「鈴虫寺の最初の説法へ」（data/routes/nishiyama-early.json）と「9〜10時に出発」（nishiyama.json）。
  どちらも scripts/build_nishiyama_data.py が作る
- 西山だけの差分（浄住寺の公開が終わったあと。OFF_FROM から）:
  - はじめて開くと「選んで回る」で、浄住寺を外した4か所（data.plan.offPicks）が選ばれている
  - 紹介ページは i18n.js の introFor の lateOff / earlyOff で上書きする
  - 回り方と選んだ場所の保存キーに -off を付ける（秋に選んだものを持ちこさない）
  次の特別公開の日程が出たら OFF_FROM と、build の日付・文章、i18n.js を直す
- 2026-11-22 にコースを分け、番号の順が変わった。「行った」印・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-nishiyama-visited-late など）になるので、前の印は引き継がれない
- nishiyama/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
  （2026-11-22 までは css +100・i18n/app +101 だったので、bump は 102 から）
"""
import os, runpy

OFF_FROM = '2026-12-14'
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='nishiyama', i18n='NISHIYAMA_I18N', count=5, data_v=4, bump=103,
    head='京都 西山（松尾大社・鈴虫寺・地蔵院・浄住寺）',
    title='京都 西山｜鈴虫寺・地蔵院（竹の寺）・松尾大社 Nishiyama MAP',
    desc='三条から阪急で京都の西山へ。鈴虫寺の説法の回に合わせて、地蔵院（竹の寺）、浄住寺の特別公開、苔寺の門前のお昼、松尾大社を歩く1日ルートマップ。最初の説法に入るコースと9〜10時発のコース。午後の嵐山・桂離宮、夜と帰りの電車も。A one-day route in Nishiyama, west Kyoto, timed around Suzumushi-dera’s talks: Jizoin, Jojuji, lunch by the Moss Temple and Matsunoo Taisha, with a first-talk or 9–10 o’clock start, then Arashiyama and the evening in town.',
    main='京都 西山', alt='Nishiyama, Kyoto', sub='西山 Nishiyama MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

APP = f'{R}/nishiyama/js/app.js'
s = open(APP, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


rep("""  // 紹介ページ: i18n.js の introFor[コース] に書いてある項目で intro を上書きする
""", f"""  // 浄住寺の公開が終わったあと（scripts/sync_nishiyama.py の OFF_FROM）は、回り方・紹介ページを冬の形にする
  var offSeason = todayJST() >= '{OFF_FROM}';
  if (offSeason) {{ KEY_MODE += '-off'; KEY_PICKS += '-off'; }}
  // 紹介ページ: i18n.js の introFor[コース] に書いてある項目で intro を上書きする
""")
rep("""    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
""", """    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
    var w = offSeason && I18N[l].introFor && I18N[l].introFor[course.id + 'Off'];
    if (w) Object.keys(w).forEach(function (k) { I18N[l].intro[k] = w[k]; });
""")
rep("""  function loadPlan() {
""", """  function loadPlan() {
    if (offSeason && data.plan && data.plan.offPicks) { data.plan.defaultMode = 'pick'; data.plan.defaultPicks = data.plan.offPicks; }
""")
open(APP, 'w', encoding='utf-8').write(s)
