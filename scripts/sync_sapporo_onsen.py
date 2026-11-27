#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を sapporo-onsen/ に写し、札幌から日帰り 温泉めぐり用の差分をかけ直す。

使い方: python3 scripts/sync_sapporo_onsen.py   （データを直したときは、先に python3 scripts/build_sapporo_onsen_data.py）
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、コースの名前だけこのマップ用に書き換える。東山などは early / late（出発時間）だが、ここは温泉地で分けている：
    jozankei    ＝ 定山渓温泉（data/routes/sapporo-onsen.json。何も選んでいなければこれ）
    noboribetsu ＝ 登別温泉（data/routes/sapporo-onsen-noboribetsu.json）
  ?course=noboribetsu でも開ける。ボタンの文言は sapporo-onsen/js/i18n.js の courseJozankei・courseNoboribetsu、紹介ページは introFor.jozankei・introFor.noboribetsu
- 「行った」印・選んだ場所の保存キーはコースごとに kyoto-maps-sapporo-onsen-…-jozankei / -noboribetsu
- sapporo-onsen/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='sapporo-onsen', i18n='SAPPORO_ONSEN_I18N', count=7, data_v=1, bump=100,
    head='札幌から日帰り 温泉めぐり（定山渓・登別）',
    title='札幌から日帰り 温泉めぐり｜定山渓・登別 Hot-spring day trips from Sapporo MAP',
    desc='札幌駅・大通・すすきのから9〜10時に出て、定山渓温泉か登別温泉で1日。足湯、温泉卵、地獄谷と天然の足湯、日帰り入浴、お昼と晩ごはん、帰りの最終のバス・特急まで時刻つき。タトゥーの決まりはお風呂ごとに公式で確かめました。Hot-spring day trips from Sapporo to Jozankei or Noboribetsu: foot baths, onsen eggs, Hell Valley and a natural foot bath in a hot river, day baths with each one’s official tattoo rule, lunch, dinner and the last buses and trains back.',
    main='札幌から日帰り 温泉めぐり', alt='Hot-spring day trips from Sapporo', sub='定山渓・登別 Onsen MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


# コースの名前を early / late から noboribetsu / jozankei に
patch(f'{R}/sapporo-onsen/js/app.js', [
    ("""   Data: ../data/routes/sapporo-onsen.json と sapporo-onsen-early.json（コースで読み分ける。写真は ../images/sapporo-onsen/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py の説明を参照""",
     """   Data: ../data/routes/sapporo-onsen.json と sapporo-onsen-noboribetsu.json（コースで読み分ける。写真は ../images/sapporo-onsen/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py と scripts/sync_sapporo_onsen.py の説明を参照"""),
    ("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける""",
     """  // コース: jozankei（定山渓温泉）か noboribetsu（登別温泉）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=noboribetsu でも開ける"""),
    ("(location.search.match(/[?&]course=(early|late)/) || [])[1]", "(location.search.match(/[?&]course=(jozankei|noboribetsu)/) || [])[1]"),
    ("  if (course.id !== 'early') course.id = 'late';", "  if (course.id !== 'noboribetsu') course.id = 'jozankei';"),
    ("  course.file = 'sapporo-onsen' + (course.id === 'early' ? '-early' : '') + '.json';",
     "  course.file = 'sapporo-onsen' + (course.id === 'noboribetsu' ? '-noboribetsu' : '') + '.json';"),
    # ?course= つきのアドレスから切り替えても、選んだほうで読み直す
    ("    history.replaceState(null, '', location.pathname + '#list');", "    history.replaceState(null, '', location.pathname + '?course=' + c + '#list');"),
])
patch(f'{R}/sapporo-onsen/index.html', [
    ('    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
     '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
     '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
     '    <p class="sw-label" data-t="swCourse">温泉地</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="温泉地">\n'
     '      <button type="button" data-course="jozankei" data-t="courseJozankei">定山渓温泉</button>\n'
     '      <button type="button" data-course="noboribetsu" data-t="courseNoboribetsu">登別温泉</button>\n'),
])
print('patched sapporo-onsen (course: jozankei / noboribetsu)')
