#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を osaka/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_osaka.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「9〜10時に出発」（late、data/routes/osaka.json）と「朝早く出発」（early、osaka-early.json）。
  どちらも scripts/build_osaka_data.py が作る
- osaka/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- keyv: 2026-11-22 に2コースに作り直して番号が変わったので、保存キーの末尾に -b を付けた
"""
import os, runpy

CFG = (dict(
    id='osaka', i18n='OSAKA_I18N', count=13, data_v=2, bump=101, keyv='-b',
    head='大阪 1日ルート（大阪城・黒門市場・新世界・夜の道頓堀）',
    title='大阪 1日ルート｜大阪城・新世界・夜の道頓堀 Osaka MAP',
    desc='梅田〜難波のホテルから1日で回る大阪。黒門市場、新世界の串カツ、四天王寺、大阪城、夜の道頓堀まで。天守閣の9:00の開館に合わせるコースと、9〜10時に出るコースを選べるルートマップ。Osaka in one day from a hotel between Umeda and Namba: Kuromon Market, kushikatsu in Shinsekai, Shitennoji, the castle and Dotonbori at night, with an early-start and a 9–10 o’clock course.',
    main='大阪', alt='Osaka', sub='大阪 1日ルート Osaka MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
