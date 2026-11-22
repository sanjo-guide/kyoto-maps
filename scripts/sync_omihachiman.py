#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を omihachiman/ に写し、近江八幡用の差分をかけ直す。

使い方: python3 scripts/sync_omihachiman.py   （データを直したときは、先に python3 scripts/build_omihachiman_courses.py）
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、コースの名前だけこのマップ用に書き換える（2026-11-22）。東山などは early / late（出発時間）だが、
  近江八幡は「どこまで行くか」で分けている：
    day    ＝ 近江八幡で1日（data/routes/omihachiman.json。何も選んでいなければこれ）
    hikone ＝ 彦根城にも行く（data/routes/omihachiman-hikone.json。scripts/build_omihachiman_courses.py が作る）
  ?course=hikone でも開ける。ボタンの文言は omihachiman/js/i18n.js の courseDay・courseHikone、紹介ページは introFor.day・introFor.hikone
- 最初の地図は data.focus の番号の範囲（近江八幡の町）に合わせる。京都と彦根は離れているため（「全体を表示」では全部）
- 「行った」印・選んだ場所の保存キーは、コースごとに kyoto-maps-omihachiman-…-day / -hikone
  （2026-11-22 に彦根の3か所を別のコースに分けたので、前のキーとは別になる）
- omihachiman/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = (dict(
    id='omihachiman', i18n='OMI_I18N', count=14, data_v=7, bump=104, keyv='-b',
    head='近江八幡（京都駅から日帰り・彦根城にも）',
    title='近江八幡｜京都から日帰り（彦根城にも）',
    desc='京都駅から新快速で乗り換えなし35分。八幡堀、八幡山ロープウェーと琵琶湖の眺め、近江牛のお昼（すき焼きか焼肉丼）、蔵のクラフトビール、夕方のラ コリーナ。夜は京都に戻るか近江八幡で晩ごはん。彦根城にも行くコースに切り替えられる、時刻つきの1日マップ。A timed day trip from Kyoto Station to Omihachiman: canal, ropeway and Lake Biwa views, an Omi-beef lunch, craft beer and La Collina, with a second course that adds Hikone Castle.',
    main='近江八幡', alt='Omihachiman', sub='京都発 From Kyoto MAP'))
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


# コースの名前を early / late から hikone / day に
patch(f'{R}/omihachiman/js/app.js', [
    ("""   Data: ../data/routes/omihachiman.json と omihachiman-early.json（コースで読み分ける。写真は ../images/omihachiman/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py の説明を参照""",
     """   Data: ../data/routes/omihachiman.json と omihachiman-hikone.json（コースで読み分ける。写真は ../images/omihachiman/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py と scripts/sync_omihachiman.py の説明を参照"""),
    ("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける""",
     """  // コース: day（近江八幡で1日）か hikone（彦根城にも行く）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=hikone でも開ける"""),
    ("(location.search.match(/[?&]course=(early|late)/) || [])[1]", "(location.search.match(/[?&]course=(hikone|day)/) || [])[1]"),
    ("  if (course.id !== 'early') course.id = 'late';", "  if (course.id !== 'hikone') course.id = 'day';"),
    ("  course.file = 'omihachiman' + (course.id === 'early' ? '-early' : '') + '.json';", "  course.file = 'omihachiman' + (course.id === 'hikone' ? '-hikone' : '') + '.json';"),
])
patch(f'{R}/omihachiman/index.html', [
    ('    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
     '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
     '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
     '    <p class="sw-label" data-t="swCourse">コース</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="コース">\n'
     '      <button type="button" data-course="day" data-t="courseDay">近江八幡で1日</button>\n'
     '      <button type="button" data-course="hikone" data-t="courseHikone">彦根城にも行く</button>\n'),
])
print('patched omihachiman (course: day / hikone)')
