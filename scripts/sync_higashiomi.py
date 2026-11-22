#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を higashiomi/ に写し、湖東用の差分をかけ直す。

使い方: python3 scripts/sync_higashiomi.py   （データを直したときは、先に python3 scripts/build_higashiomi_data.py）
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・hints の期間など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、コースの名前だけこのマップ用に書き換える（2026-11-22）。湖東は「どこへ行くか」で分けている：
    eigenji ＝ 太郎坊宮・永源寺（9〜10時に出発。data/routes/higashiomi.json。何も選んでいなければこれ）
    sanzan  ＝ 湖東三山（8時台に出発。紅葉シャトルバスの日向け。data/routes/higashiomi-sanzan.json）
  ?course=sanzan でも開ける。ボタンの文言は higashiomi/js/i18n.js の courseEigenji・courseSanzan、紹介ページは introFor.eigenji・introFor.sanzan
- 「行った」印・選んだ場所の保存キーは、コースごとに kyoto-maps-higashiomi-…-eigenji / -sanzan
  （2026-11-22 にコースを分けて番号が変わったので、前のキーとは別になる）
- higashiomi/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = (dict(
    id='higashiomi', i18n='HIGASHIOMI_I18N', count=5, data_v=4, bump=103,
    head='湖東の紅葉（太郎坊宮・永源寺・湖東三山・教林坊）',
    title='京都から日帰り 湖東の紅葉｜太郎坊宮・永源寺・湖東三山・教林坊 Higashiomi MAP',
    desc='京都の三条から日帰りで湖東の紅葉へ。太郎坊宮と永源寺を回って教林坊の夜のライトアップで締めるコースと、彦根からの紅葉シャトルバスで西明寺・百済寺・金剛輪寺の湖東三山を回るコースを選べる、時刻つきの1日マップ。A timed day trip from central Kyoto to the autumn leaves east of Lake Biwa: Taroubou-gu, Eigenji and the Kyorinbo illumination, or the three Koto Sanzan temples by shuttle bus from Hikone.',
    main='湖東の紅葉', alt='Autumn in Higashiomi', sub='京都から日帰り Higashiomi MAP'))
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


# コースの名前を early / late から sanzan / eigenji に
patch(f'{R}/higashiomi/js/app.js', [
    ("""   Data: ../data/routes/higashiomi.json と higashiomi-early.json（コースで読み分ける。写真は ../images/higashiomi/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py の説明を参照""",
     """   Data: ../data/routes/higashiomi.json と higashiomi-sanzan.json（コースで読み分ける。写真は ../images/higashiomi/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py と scripts/sync_higashiomi.py の説明を参照"""),
    ("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける""",
     """  // コース: eigenji（太郎坊宮・永源寺）か sanzan（湖東三山）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=sanzan でも開ける"""),
    ("(location.search.match(/[?&]course=(early|late)/) || [])[1]", "(location.search.match(/[?&]course=(sanzan|eigenji)/) || [])[1]"),
    ("  if (course.id !== 'early') course.id = 'late';", "  if (course.id !== 'sanzan') course.id = 'eigenji';"),
    ("  course.file = 'higashiomi' + (course.id === 'early' ? '-early' : '') + '.json';", "  course.file = 'higashiomi' + (course.id === 'sanzan' ? '-sanzan' : '') + '.json';"),
])
patch(f'{R}/higashiomi/index.html', [
    ('    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
     '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
     '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
     '    <p class="sw-label" data-t="swCourse">コース</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="コース">\n'
     '      <button type="button" data-course="eigenji" data-t="courseEigenji">太郎坊宮・永源寺</button>\n'
     '      <button type="button" data-course="sanzan" data-t="courseSanzan">湖東三山</button>\n'),
])
print('patched higashiomi (course: eigenji / sanzan)')
