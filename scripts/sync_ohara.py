#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を ohara/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_ohara.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「三千院の開門に合わせる」（data/routes/ohara-early.json）と「9〜10時に出発」（ohara.json）。どちらも scripts/build_ohara_data.py が作る
- 2026-11-22 にコースを分けて「帰りのバスと、街なかの夜」を足し、番号が変わった（9か所）。「行った」印・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-ohara-visited-late など）になるので、古い番号の印は引き継がれない
- ohara/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = (dict(
    id='ohara', i18n='OHARA_I18N', count=9, data_v=3, bump=102,
    head='京都 大原（三千院・宝泉院・寂光院）',
    title='京都 大原｜三千院・宝泉院・寂光院 Ohara MAP',
    desc='三条から京都バスで約45分の山里、大原。三千院の開門に合わせるコースと、先に寂光院へ行って三千院を午後に回す9〜10時発コースを選べる1日ルートマップ。お昼の時間、帰りのバス、街なかに戻ってからの夜も。Ohara, north of Kyoto, by bus from Sanjo: a course timed for Sanzen-in’s opening, or a 9–10 o’clock course that saves Sanzen-in for the afternoon, with lunch timing, buses back and the evening in town.',
    main='大原', alt='Ohara', sub='京都 Ohara MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
