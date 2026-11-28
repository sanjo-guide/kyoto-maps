#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を uji/ に写し、宇治・伏見用の差分をかけ直す。

使い方: python3 scripts/sync_uji.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・写真のクレジット・要確認の一文など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ（2026-11-22）：early＝平等院の開門に合わせる（uji-early.json）、late＝9〜10時に出発（uji.json）。
  どちらも scripts/build_uji_data.py が作る。ボタンの文言は uji/js/i18n.js の courseEarly・courseLate
- 「行った」印・選んだ場所の保存キーは、コースごとに kyoto-maps-uji-…-early / -late（2026-11-22 に番号を振り直したので、前のキーとは別になる）
- uji/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = (dict(
    id='uji', i18n='UJI_I18N', count=16, data_v=3, bump=103,
    head='京都 宇治と伏見',
    title='京都 宇治と伏見｜平等院・抹茶・酒蔵の町 Uji &amp; Fushimi MAP',
    desc='三条から京阪電車で宇治へ。平等院と抹茶、宇治川と宇治上神社を歩いて、午後は伏見の酒蔵の町で月桂冠大倉記念館のきき酒、十石舟、夜は蔵元の店と地ビール。平等院の開門に合わせるコースと9〜10時に出るコースを選べる1日ルートマップ。Uji and Fushimi in one day from central Kyoto: Byodoin, matcha and Ujigami Shrine, then sake tasting, a canal boat and dinner in the brewery town, with an opening-time course and a 9–10 o’clock course.',
    main='宇治と伏見', alt='Uji &amp; Fushimi', sub='京都 Uji &amp; Fushimi MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
