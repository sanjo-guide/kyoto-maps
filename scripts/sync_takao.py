#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を takao/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_takao.py
- 差分は東山マップと同じ（コースの切り替え・写真のクレジット・要確認の一文・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「神護寺の開門に合わせる」（data/routes/takao-early.json）と「9〜10時に出発」（takao.json）。どちらも scripts/build_takao_data.py が作る
- 2026-11-22 にコースを分け、コースで番号の順が変わるようになった。「行った」印・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-takao-visited-late など）になるので、前の印は引き継がれない
- data.plan.defaultMode がないので「全部回る」で開く
- takao/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = dict(
    id='takao', i18n='TAKAO_I18N', count=4, data_v=4, bump=103,
    head='京都 高雄の紅葉（神護寺・西明寺・高山寺）',
    title='京都 高雄の紅葉｜神護寺・西明寺・高山寺 Takao MAP',
    desc='三条から地下鉄とJRバスで高雄へ。神護寺の開門に合わせるコースと、栂ノ尾の高山寺から谷を下る9〜10時発コースを選べる、京都の北西の紅葉ルートマップ。お昼の茶屋、帰りのバス、仁和寺・北野天満宮への寄り道と街なかの夜も。Autumn leaves at Takao, north-west Kyoto: a course timed for Jingoji’s opening, or a 9–10 o’clock course from Kosanji down the valley, with lunch, buses back, stops on the way home and the evening in town.',
    main='高雄の紅葉', alt='Autumn in Takao', sub='京都 Takao MAP')
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
