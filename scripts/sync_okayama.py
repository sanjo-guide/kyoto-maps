#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を okayama/ に写し、岡山と倉敷用の差分をかけ直す。

使い方: python3 scripts/sync_okayama.py   （データを直したときは、先に python3 scripts/build_okayama_data.py）
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、コースの名前だけこのマップ用に書き換える（2026-11-22）。東山などは early / late（出発時間）だが、岡山は旅の形で分けている：
    stay ＝ 1泊2日（data/routes/okayama.json。何も選んでいなければこれ）
    stop ＝ 移動の途中に立ち寄る（data/routes/okayama-stop.json）
  ?course=stop でも開ける。ボタンの文言は okayama/js/i18n.js の courseStay・courseStop、紹介ページは introFor.stay・introFor.stop
- 「行った」印・選んだ場所の保存キーはコースごとに kyoto-maps-okayama-…-stay-b / -stop-b
  （日帰りをやめて番号を振り直したので、前のキーは引き継がない）
- okayama/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = (dict(
    id='okayama', i18n='OKAYAMA_I18N', count=15, data_v=3, bump=105, keyv='-b',
    head='岡山と倉敷（1泊2日・京都や大阪から広島への途中に立ち寄る）',
    title='岡山と倉敷｜1泊2日・広島への途中に Okayama &amp; Kurashiki MAP',
    desc='岡山城と後楽園、夜と朝の倉敷美観地区、吉備津神社を回る1泊2日と、京都・大阪から広島へ行く途中に立ち寄るコースを選べる、時刻つきのルートマップ。荷物の預け方と途中下車のきっぷの買い方も。Okayama and Kurashiki: a timed overnight route with the canal town by night and morning, or a stopover on the way from Kyoto or Osaka to Hiroshima, with luggage and ticket tips.',
    main='岡山と倉敷', alt='Okayama &amp; Kurashiki', sub='1泊2日・途中下車 Okayama MAP'))
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


# コースの名前を early / late から stop / stay に
patch(f'{R}/okayama/js/app.js', [
    ("""   Data: ../data/routes/okayama.json と okayama-early.json（コースで読み分ける。写真は ../images/okayama/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py の説明を参照""",
     """   Data: ../data/routes/okayama.json と okayama-stop.json（コースで読み分ける。写真は ../images/okayama/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py と scripts/sync_okayama.py の説明を参照"""),
    ("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける""",
     """  // コース: stay（1泊2日）か stop（移動の途中に立ち寄る）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=stop でも開ける"""),
    ("(location.search.match(/[?&]course=(early|late)/) || [])[1]", "(location.search.match(/[?&]course=(stop|stay)/) || [])[1]"),
    ("  if (course.id !== 'early') course.id = 'late';", "  if (course.id !== 'stop') course.id = 'stay';"),
    ("  course.file = 'okayama' + (course.id === 'early' ? '-early' : '') + '.json';", "  course.file = 'okayama' + (course.id === 'stop' ? '-stop' : '') + '.json';"),
    # ?course= つきのアドレスから切り替えても、選んだほうで読み直す
    ("    history.replaceState(null, '', location.pathname + '#list');", "    history.replaceState(null, '', location.pathname + '?course=' + c + '#list');"),
])
patch(f'{R}/okayama/index.html', [
    ('    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
     '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
     '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
     '    <p class="sw-label" data-t="swCourse">旅の形</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="旅の形">\n'
     '      <button type="button" data-course="stay" data-t="courseStay">1泊2日</button>\n'
     '      <button type="button" data-course="stop" data-t="courseStop">移動の途中に立ち寄る</button>\n'),
])
print('patched okayama (course: stay / stop)')
