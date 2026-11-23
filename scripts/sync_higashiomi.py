#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を higashiomi/ に写し、湖東用の差分をかけ直す。

使い方: python3 scripts/sync_higashiomi.py   （データを直したときは、先に python3 scripts/build_higashiomi_data.py）
- 差分は東山マップと同じ（コースの切り替え・最初から「選んで回る」・defaultPicks・写真のクレジット・要確認の一文・hints の期間など）。
  中身は scripts/sync_higashiyama.py にあり、ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- そのあと、コースの名前だけこのマップ用に書き換える（2026-11-22）。湖東は「どこへ行くか」で分けている：
    eigenji ＝ 太郎坊宮・永源寺（9〜10時に出発。data/routes/higashiomi.json。何も選んでいなければこれ）
    sanzan  ＝ 湖東三山（8時台に出発。紅葉シャトルバスの日向け。data/routes/higashiomi-sanzan.json）
  ?course=sanzan でも開ける。ボタンの文言は higashiomi/js/i18n.js の courseEigenji・courseSanzan、紹介ページは introFor.eigenji・introFor.sanzan
- 湖東三山は日付で替わる（日本時間。ここの TAXI_FROM・WINTER_FROM）:
    11/29まで            data/routes/higashiomi-sanzan.json        紅葉シャトルバス
    TAXI_FROM（11/30）から   higashiomi-sanzan-taxi.json   乗合タクシーで西明寺と金剛輪寺。紹介ページは introFor.sanzanTaxi を上書き
    WINTER_FROM（12/7）から  higashiomi-sanzan-winter.json 教林坊なし。紹介ページは introFor.sanzanWinter をさらに上書き
  11/30からは番号の順が変わるので、「行った」印・回り方・選んだ場所の保存キーに -off を付ける（シャトルバスの日の選択を持ちこさない）。
  コースのボタンの文字は、どちらのコースを開いていても courseSanzanTaxi に替わる。
  次の秋のシャトルバスが決まったら、ここの日付と build・i18n.js を直す
- 太郎坊宮・永源寺も日付で替わる:
    12/6まで             data/routes/higashiomi.json           教林坊のライトアップまで
    WINTER_FROM（12/7）から  higashiomi-eigenji-winter.json 教林坊なしで京都駅18:12着。紹介ページは introFor.eigenjiWinter を上書き
  番号1〜4は同じなので「行った」印はそのまま。回り方・選んだ場所の保存キーにだけ -off を付ける
- 「行った」印・選んだ場所の保存キーは、コースごとに kyoto-maps-higashiomi-…-eigenji / -sanzan
  （2026-11-22 にコースを分けて番号が変わったので、前のキーとは別になる）
- higashiomi/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
"""
import os, runpy

TAXI_FROM = '2026-11-30'     # シャトルバスが終わった次の日
WINTER_FROM = '2026-12-07'   # 教林坊のライトアップが終わった次の日（両方のコース）
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = (dict(
    id='higashiomi', i18n='HIGASHIOMI_I18N', count=5, data_v=8, bump=107,
    head='湖東の紅葉（太郎坊宮・永源寺・湖東三山・教林坊）',
    title='京都から日帰り 湖東の紅葉｜太郎坊宮・永源寺・湖東三山・教林坊 Higashiomi MAP',
    desc='京都駅から日帰りで湖東の紅葉へ。太郎坊宮と永源寺を回って教林坊の夜のライトアップ（2026年12月6日まで）で締めるコースと、彦根からの紅葉シャトルバス（2026年11月29日まで。その後は乗合タクシーで西明寺と金剛輪寺）で湖東三山を回るコースを選べる、時刻つきの1日マップ。A timed day trip from Kyoto Station to the autumn leaves east of Lake Biwa: Taroubou-gu, Eigenji and the Kyorinbo illumination (until 6 Dec 2026), or the Koto Sanzan temples by shuttle bus from Hikone (until 29 Nov 2026; shared taxi to two of them afterwards).',
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
    # 11/30からの湖東三山（日付で替わる）
    ("  // 紹介ページ: i18n.js の introFor[コース] に書いてある項目で intro を上書きする\n",
     f"""  // シャトルバス・教林坊のライトアップが終わったあと（scripts/sync_higashiomi.py の TAXI_FROM・WINTER_FROM）は、データと紹介ページを替える
  var season = todayJST() >= '{WINTER_FROM}' ? 'winter' : todayJST() >= '{TAXI_FROM}' ? 'taxi' : '';
  var sanzanOff = !!season && course.id === 'sanzan', eigenjiOff = season === 'winter' && course.id === 'eigenji';
  if (sanzanOff) {{
    course.file = 'higashiomi-sanzan-' + season + '.json';
    KEY_VISITED += '-off'; KEY_MODE += '-off'; KEY_PICKS += '-off';
  }} else if (eigenjiOff) {{
    course.file = 'higashiomi-eigenji-winter.json';
    KEY_MODE += '-off'; KEY_PICKS += '-off';
  }}
  // 紹介ページ: i18n.js の introFor[コース] に書いてある項目で intro を上書きする
"""),
    ("    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });\n",
     """    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
    if (season && I18N[l].courseSanzanTaxi) I18N[l].courseSanzan = I18N[l].courseSanzanTaxi;
    (sanzanOff ? (season === 'winter' ? ['sanzanTaxi', 'sanzanWinter'] : ['sanzanTaxi']) : eigenjiOff ? ['eigenjiWinter'] : []).forEach(function (name) {
      var w = I18N[l].introFor && I18N[l].introFor[name];
      if (w) Object.keys(w).forEach(function (k) { I18N[l].intro[k] = w[k]; });
    });
"""),
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
