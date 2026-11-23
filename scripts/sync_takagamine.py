#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を takagamine/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_takagamine.py
- 差分は東山マップと同じ（コースの切り替え・写真のクレジット・要確認の一文・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「鷹峯の開門に合わせる」（data/routes/takagamine-early.json）と「9〜10時に出発」（takagamine.json）。
  どちらも scripts/build_takagamine_data.py が作る
- 2026-11-22 にコースを分け、コースで番号の順が変わるようになった。「行った」印・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-takagamine-visited-late など）になるので、前の印は引き継がれない
- data.plan.defaultMode がないので「全部回る」で開く
- takagamine/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
  （2026-11-22 までは css +100・i18n/app +101 だったので、bump は 102 から）
"""
import os, runpy

CFG = dict(
    id='takagamine', i18n='TAKAGAMINE_I18N', count=4, data_v=5, bump=103,
    head='京都 今宮神社と鷹峯（光悦寺・源光庵・常照寺）',
    title='京都 今宮神社と鷹峯｜あぶり餅・光悦寺・源光庵・常照寺 Takagamine MAP',
    desc='三条から市バスで京都の北へ。今宮神社のあぶり餅、鷹峯の光悦寺・源光庵・常照寺の紅葉。源光庵の開門に合わせるコースと9〜10時発のコースを選べるルートマップ。お昼の場所、大徳寺・しょうざん・金閣寺へのつなぎ方、帰りのバスと夜も。Imamiya Shrine’s aburi-mochi and the autumn temples of Takagamine, north Kyoto: a course timed for Genkoan’s 9:00 opening or a 9–10 o’clock course, with lunch, Daitoku-ji, Shozan and Kinkaku-ji, buses back and the evening in town.',
    main='今宮神社と鷹峯', alt='Imamiya & Takagamine', sub='京都 Takagamine MAP')
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
