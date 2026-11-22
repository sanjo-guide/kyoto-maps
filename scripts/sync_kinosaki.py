#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を kinosaki/ に写し、城崎温泉用の差分をかけ直す。

使い方: python3 scripts/sync_kinosaki.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・写真のクレジット・要確認の一文・最初に映す範囲など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ（2026-11-22）：late＝城崎温泉だけ（kinosaki.json。最初に開く）、early＝竹田城跡に寄る（kinosaki-early.json）。
  early / late はコース切り替えの仕組みの名前を借りているだけで、どちらも京都7:32発。
  どちらも scripts/build_kinosaki_data.py が作る。ボタンの文言は kinosaki/js/i18n.js の courseEarly・courseLate
- 「行った」印・選んだ場所の保存キーは、コースごとに kyoto-maps-kinosaki-…-early / -late（前のキーとは別になる）
- kinosaki/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = (dict(
    id='kinosaki', i18n='KINOSAKI_I18N', count=12, data_v=5, bump=103,
    head='京都から日帰り 城崎温泉（＋竹田城跡）',
    title='京都から日帰り 城崎温泉・竹田城跡 Kinosaki Onsen MAP',
    desc='京都7:32の特急で城崎温泉へ。外湯4つとロープウェイを回る「城崎温泉だけ」と、天空の城・竹田城跡に寄ってから外湯を3つ回るコースを選べる1日ルートマップ。外湯の休みの曜日、乗り遅れたときの次の電車、晩ごはんまで。A day trip from Kyoto to Kinosaki Onsen on the 7:32 express: a Kinosaki-only course with four baths and the ropeway, or a course via Takeda Castle, the “castle in the sky”, with closed days, fallback trains and dinner.',
    main='城崎温泉', alt='Kinosaki Onsen', sub='京都から日帰り Kinosaki MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
