#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を himeji/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_himeji.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「9〜10時に出発」（late、data/routes/himeji.json）と「開城に合わせる」（early、himeji-early.json）。
  どちらも scripts/build_himeji_data.py が作る
- himeji/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- 2026-11-22 に2コースに作り直した。保存キーはコースごと（kyoto-maps-himeji-visited-late など）になったので、
  前の番号で付けた「行った」印・選んだ場所は引き継がれない（番号が変わったため、それでよい）
"""
import os, runpy

CFG = (dict(
    id='himeji', i18n='HIMEJI_I18N', count=7, data_v=5, bump=105,
    head='姫路・明石・須磨 1日ルート（姫路城・好古園・明石の魚の棚・須磨浦山上遊園・舞子）',
    title='姫路・明石・須磨 1日ルート｜姫路城・明石焼・須磨浦 Himeji MAP',
    desc='大阪の梅田〜難波のホテルから1日で回る姫路・明石・須磨。姫路城の9:00の開城に合わせるコースと、9〜10時に出て午後にお城へ行くコースを選べるルートマップ。明石の魚の棚で明石焼、須磨浦のロープウェー、舞子の夕日、夜の姫路城まで。Himeji, Akashi and Suma in one day from a hotel between Umeda and Namba in Osaka: Himeji Castle at its 9:00 opening or in the afternoon, akashiyaki in Akashi, the Sumaura ropeway and sunset at the Akashi Kaikyo Bridge.',
    main='姫路・明石・須磨', alt='Himeji, Akashi & Suma', sub='大阪から1日 Himeji MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
