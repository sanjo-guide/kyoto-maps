#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を nara/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_nara.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「早朝に出発」（data/routes/nara-early.json）と「9〜10時に出発」（nara.json）。どちらも scripts/build_nara_data.py が作る
- 2026-11-22 にコースを分けて春鹿を足し、番号が変わった。「行った」印・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-nara-visited-late など）になるので、古い番号の印は引き継がれない
- nara/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = (dict(
    id='nara', i18n='NARA_I18N', count=12, data_v=4, bump=104,
    head='京都・大阪から日帰り 奈良',
    title='京都・大阪から日帰り 奈良｜東大寺・春日大社・ならまち Nara MAP',
    desc='京都・大阪から近鉄で奈良へ。大仏殿の開門に合わせる早朝コースと、昼の混雑を避けて夕方に大仏殿・夕暮れの二月堂へ行く9〜10時発コースを選べる1日ルートマップ。興福寺、春日大社、ならまち、酒蔵「春鹿」のきき酒も。A day in Nara on foot from Kyoto or Osaka: an early course timed for the opening of the Great Buddha Hall, or a 9–10 o’clock course that saves Todaiji for late afternoon and Nigatsudo for dusk.',
    main='奈良', alt='Nara', sub='京都・大阪から日帰り Nara MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
