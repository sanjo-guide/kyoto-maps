#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を fushimi-inari/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_fushimi_inari.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・写真のクレジット・要確認の一文など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- fushimi-inari/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = (dict(
    id='fushimi-inari', i18n='FUSHIMI_INARI_I18N', count=7, data_v=2, bump=101,
    head='京都 伏見稲荷から七条へ（伏見稲荷・東福寺・泉涌寺・三十三間堂・梅湯）',
    title='京都 伏見稲荷から七条へ｜千本鳥居・東福寺・銭湯とビール Fushimi Inari MAP',
    desc='朝6時の伏見稲荷から、東福寺、泉涌寺、三十三間堂へ。夕方は高瀬川ぞいの銭湯とクラフトビール。早朝に出るコースと9〜10時に出るコースを選べる1日ルートマップ。A one-day route in Kyoto from Fushimi Inari at 6 am to Tofuku-ji, Sennyu-ji and Sanjusangen-do, ending with a public bath and craft beer by the Takase River.',
    main='伏見稲荷から七条へ', alt='Fushimi Inari to Shichijo', sub='伏見稲荷 Fushimi Inari MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
