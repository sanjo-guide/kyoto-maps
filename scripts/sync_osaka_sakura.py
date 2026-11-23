#!/usr/bin/env python3
"""ルート型のテンプレート（eizan-line/）の index.html・css・app.js を osaka-sakura/ に写し、差分をかけ直す。

使い方: python3 scripts/sync_osaka_sakura.py  （データは先に python3 scripts/build_osaka_sakura_data.py で作る）
- 共通の差分（コースの切り替え・写真のクレジット・要確認の一文など）は scripts/sync_higashiyama.py にあり、
  ここではこのマップの名前と番号だけを渡して、そのファイルを実行する
- コースは2つ（scripts/build_osaka_sakura_data.py が作る）:
    late  （造幣局は午後の枠・最初に開く）= data/routes/osaka-sakura.json
    early （造幣局は朝いちばんの枠）       = data/routes/osaka-sakura-early.json
  ボタンは late を上に並べ替える
- 春以外（SEASON_FROM〜SEASON_TO の外。月-日で見る）に開くと「春のマップ・いまはやっていない」の一文
  （i18n.js の offKicker・offHow・offHowText・offLead・offNote）を使い方・紹介ページ・一覧に出す。
  来春の日程が発表されたら、SEASON_FROM / SEASON_TO と build の notices の日付を直す
- 2026-11-23 にコースを分けた。「行った」印・回り方・選んだ場所の保存キーはコースごとの名前
  （kyoto-maps-osaka-sakura-visited-late など）になるので、前の印は引き継がれない
- osaka-sakura/js/i18n.js はこのマップ専用なので触らない。テンプレートに新しい文言キーが増えたら、i18n.js に手で足す
- このマップだけ更新したときは、data_v（データ）と bump（css・js）の数字を上げる
  （2026-11-22 までは css +100・i18n +101・app +100 だったので、bump は 102 から）
- 置き換え先が見つからないと途中で止まる（そのときはこのスクリプトを直す）
"""
import os, re, runpy

SEASON_FROM, SEASON_TO = '04-01', '04-20'
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = dict(
    id='osaka-sakura', i18n='OSAKA_SAKURA_I18N', count=4, data_v=2, bump=102,
    head='大阪 造幣局の桜の通り抜け（大阪城 西の丸庭園・毛馬桜之宮公園）',
    title='大阪 造幣局の桜の通り抜け｜春のマップ Osaka Sakura MAP',
    desc='春のマップ。4月中旬の約1週間だけ開く造幣局の桜の通り抜け（事前申込制）を、申し込んだ時間帯に合わせて。大阪城 西の丸庭園と玉造口の八重桜、大川沿いの毛馬桜之宮公園、夜は天満か道頓堀まで。梅田〜難波のホテルから。A spring map for the week in mid-April when the Japan Mint opens its cherry walk (booking required), built around your entry slot, with Osaka Castle, the Okawa riverside and an evening in Tenma or Dotonbori, starting from a hotel between Umeda and Namba.',
    main='造幣局の桜の通り抜け', alt='Osaka Mint cherry walk', sub='大阪 Osaka Sakura MAP')
runpy.run_path(os.path.join(R, 'scripts', 'sync_higashiyama.py'), init_globals={'CFG': CFG})

s = ''


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# app.js
APP = f'{R}/osaka-sakura/js/app.js'
s = open(APP, encoding='utf-8').read()
rep("違いは scripts/sync_higashiyama.py の説明を参照",
    "違いは scripts/sync_osaka_sakura.py と scripts/sync_higashiyama.py の説明を参照")
rep("""  // コース: early（早朝に出発）か late（9〜10時に出発）。コースごとにデータファイルが別で、スポットの番号も変わる。
""", """  // コース: late（造幣局は午後の枠）か early（朝いちばんの枠）。コースごとにデータファイルが別で、スポットの番号も変わる。
""")
rep("""  course.file = 'osaka-sakura' + (course.id === 'early' ? '-early' : '') + '.json';
""", f"""  course.file = 'osaka-sakura' + (course.id === 'early' ? '-early' : '') + '.json';
  var md = todayJST().slice(5);     // 月-日。通り抜けの時期以外は「春のマップ」の一文を出す
  var offSeason = md < '{SEASON_FROM}' || md > '{SEASON_TO}';
""")
rep("""    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
  });
""", """    if (o) Object.keys(o).forEach(function (k) { I18N[l].intro[k] = o[k]; });
    // 通り抜けの時期以外は「春のマップ・いまはやっていない」の一文を先に出す
    if (offSeason) {
      I18N[l].intro.kicker = I18N[l].offKicker;
      // 使い方の1つ目は、開いて最初に見える場所
      I18N[l].intro.how[0].title = I18N[l].offHow;
      I18N[l].intro.how[0].text = I18N[l].offHowText + I18N[l].intro.how[0].text;
      I18N[l].intro.lead = I18N[l].offLead + I18N[l].intro.lead;
      I18N[l].listNote = I18N[l].offNote + I18N[l].listNote;
    }
  });
  if (offSeason) document.body.classList.add('off-season');
""")
open(APP, 'w', encoding='utf-8').write(s)

# index.html（午後の枠のボタンを上に）
PAGE = f'{R}/osaka-sakura/index.html'
s = open(PAGE, encoding='utf-8').read()
m = re.search(r'    <p class="sw-label" data-t="swCourse">.*?    </div>\n', s, re.S)
assert m
rep(m.group(0),
    '    <p class="sw-label" data-t="swCourse">造幣局に入る時間帯</p>\n'
    '    <div class="modesw coursesw" role="group" data-t-aria="courseAria" aria-label="造幣局に入る時間帯">\n'
    '      <button type="button" data-course="late" data-t="courseLate">午後の枠（15時ごろ）\n9:30ごろ梅田・なんば発</button>\n'
    '      <button type="button" data-course="early" data-t="courseEarly">朝いちばんの枠（平日10時・土日9時）\n9:15ごろ（土日8:20ごろ）発</button>\n'
    '    </div>\n')
open(PAGE, 'w', encoding='utf-8').write(s)

# css
CSS = f'{R}/osaka-sakura/css/style.css'
open(CSS, 'a', encoding='utf-8').write("""/* 造幣局の桜: 季節外は一覧の一文を目立たせる */
.off-season .list-note { padding: 8px 10px; background: var(--warn-soft); color: #4A3209; }
""")
print('patched osaka-sakura (2 courses, season)')
