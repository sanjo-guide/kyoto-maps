#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を gosho/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_gosho.py
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ：「開城に合わせる」（data/routes/gosho-early.json）と「9〜10時に出発」（gosho.json）。どちらも scripts/build_gosho_data.py が作る
- 2026-11-22 にコースを分けて番号が変わった。「行った」印・選んだ場所の保存キーはコースごとの新しい名前
  （kyoto-maps-gosho-visited-late など）になるので、古い番号の印は引き継がれない
- gosho/js/i18n.js はこのマップ専用なので触らない
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

CFG = (dict(
    id='gosho', i18n='GOSHO_I18N', count=10, data_v=2, bump=101,
    head='京都の中心：二条城と京都御所',
    title='京都の中心 二条城と京都御所 Nijo Castle &amp; Imperial Palace MAP',
    desc='三条のあたりから歩きと地下鉄で回る、二条城と京都御所の1日ルートマップ。開城の8:45に二条城へ行くコースと、9〜10時に出て二条城を午後に回すコースを選べます。予約なしで入れる京都御所、梅・桜・紅葉の京都御苑、夕方は錦市場、夜は先斗町・木屋町へ。Central Kyoto in a day: Nijo Castle at its 8:45 opening or in the later afternoon, the Imperial Palace and its park, Nishiki Market, then Pontocho by night.',
    main='二条城と京都御所', alt='Nijo Castle & Imperial Palace', sub='京都の中心 Central Kyoto MAP'))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_higashiyama.py'), init_globals={'CFG': CFG})
