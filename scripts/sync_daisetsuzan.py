#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を daisetsuzan/ に写し、大雪山の日帰り（旭岳・層雲峡）用の差分をかけ直す。

使い方: python3 scripts/sync_daisetsuzan.py   （データを直したときは、先に python3 scripts/build_daisetsuzan_data.py）
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・data.focus など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、コースの名前だけこのマップ用に書き換える（形は scripts/sync_sapporo_onsen.py と同じ）。行き先で分けている：
    asahidake ＝ 旭岳（data/routes/daisetsuzan.json。何も選んでいなければこれ）
    sounkyo   ＝ 層雲峡（data/routes/daisetsuzan-sounkyo.json）
  ?course=sounkyo でも開ける。ボタンの文言は daisetsuzan/js/i18n.js の courseAsahidake・courseSounkyo、紹介ページは introFor.asahidake・introFor.sounkyo
- 「行った」印・選んだ場所の保存キーはコースごとに kyoto-maps-daisetsuzan-…-asahidake / -sounkyo
- daisetsuzan/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='daisetsuzan', i18n='DAISETSUZAN_I18N', count=6, data_v=2, bump=101,
    head='大雪山の日帰り：旭岳と層雲峡（旭川から）',
    title='大雪山の日帰り｜旭岳と層雲峡（旭川から） Daisetsuzan day trips from Asahikawa MAP',
    desc='旭川駅からバスで行く大雪山の1日。旭岳はロープウェイで標高1,600mの姿見の池へ、帰りに旭岳温泉か東川の町。層雲峡は黒岳ロープウェイ、銀河・流星の滝、黒岳の湯、冬は氷瀑まつり。バスの時刻と最終便、冬の服装、ロープウェイの運休、タトゥーの決まりまで。Day trips by bus from Asahikawa into the Daisetsuzan mountains: the Asahidake Ropeway and Sugatami Pond with a hot spring or the town of Higashikawa, or Sounkyo gorge with the Kurodake Ropeway, waterfalls, a public bath and the winter Ice Fall Festival. Bus times and last buses, winter clothing, ropeway closures and tattoo rules.',
    main='大雪山の日帰り', alt='Daisetsuzan day trips', sub='旭岳と層雲峡 Asahidake & Sounkyo MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)


# コースの名前を early / late から sounkyo / asahidake に
patch(f'{R}/daisetsuzan/js/app.js', [
    ("""   Data: ../data/routes/daisetsuzan.json と daisetsuzan-early.json（コースで読み分ける。写真は ../images/daisetsuzan/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py の説明を参照""",
     """   Data: ../data/routes/daisetsuzan.json と daisetsuzan-sounkyo.json（コースで読み分ける。写真は ../images/daisetsuzan/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_higashiyama.py と scripts/sync_daisetsuzan.py の説明を参照"""),
    ("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=early でも開ける""",
     """  // コース: asahidake（旭岳）か sounkyo（層雲峡）。コースごとにデータファイルが別で、スポットの番号も変わる。
  // 一覧の上のボタン（data-course）で切り替える。?course=sounkyo でも開ける"""),
    ("(location.search.match(/[?&]course=(early|late)/) || [])[1]", "(location.search.match(/[?&]course=(asahidake|sounkyo)/) || [])[1]"),
    ("  if (course.id !== 'early') course.id = 'late';", "  if (course.id !== 'sounkyo') course.id = 'asahidake';"),
    ("  course.file = 'daisetsuzan' + (course.id === 'early' ? '-early' : '') + '.json';",
     "  course.file = 'daisetsuzan' + (course.id === 'sounkyo' ? '-sounkyo' : '') + '.json';"),
    # ?course= つきのアドレスから切り替えても、選んだほうで読み直す
    ("    history.replaceState(null, '', location.pathname + '#list');", "    history.replaceState(null, '', location.pathname + '?course=' + c + '#list');"),
])
patch(f'{R}/daisetsuzan/index.html', [
    ('    <p class="sw-label" data-t="swCourse">出発時間</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="出発時間">\n'
     '      <button type="button" data-course="early" data-t="courseEarly">早朝に出発</button>\n'
     '      <button type="button" data-course="late" data-t="courseLate">9〜10時に出発</button>\n',
     '    <p class="sw-label" data-t="swCourse">行き先</p>\n'
     '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="行き先">\n'
     '      <button type="button" data-course="asahidake" data-t="courseAsahidake">旭岳</button>\n'
     '      <button type="button" data-course="sounkyo" data-t="courseSounkyo">層雲峡</button>\n'),
])
print('patched daisetsuzan (course: asahidake / sounkyo)')
