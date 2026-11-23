#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を tomogashima/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_tomogashima.py
- 差分は東山マップと同じ（コースの切り替え・写真のクレジット・要確認の一文・最初に映す範囲 data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは行きの船で2つ：「11:00の船」（late、data/routes/tomogashima.json。最初に開く）と
  「9:00の船」（early、tomogashima-early.json）。どちらも scripts/build_tomogashima_data.py が作る
- data.plan.defaultMode がないので「全部回る」で開く
- tomogashima/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
- keyv: 2026-11-22 に2コースに作り直して番号が変わった（11:00の船では淡嶋神社が3番）ので、保存キーの末尾に -b を付けた
"""
import os, runpy

CFG = (dict(
    id='tomogashima', i18n='TOMOGASHIMA_I18N', count=10, data_v=6, bump=103, keyv='-b',
    head='友ヶ島・加太（大阪から日帰り）',
    title='友ヶ島・加太｜大阪から日帰り Tomogashima MAP',
    desc='大阪・なんばから南海電車で加太へ、船で無人島の友ヶ島へ。レンガの砲台跡と灯台を歩き、淡嶋神社と加太の温泉まで。9:00の船と11:00の船、行きの船ごとの時間割を選べる日帰りルートマップ。A day trip from Osaka (Namba) to Kada and the uninhabited island of Tomogashima: brick gun batteries, a lighthouse, Awashima Shrine, with a timetable for the 9:00 boat and one for the 11:00.',
    main='友ヶ島・加太', alt='Tomogashima & Kada', sub='大阪から日帰り Tomogashima MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
