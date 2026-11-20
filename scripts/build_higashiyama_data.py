#!/usr/bin/env python3
"""京都・東山ルートのデータ（data/routes/higashiyama.json）を書き出す。

使い方: python3 scripts/build_higashiyama_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
- 写真は images/higashiyama/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/higashiyama"
OUT = f"{R}/data/routes/higashiyama.json"
CHECKED = "2026-11-20"
PICKS = {}
for f in os.listdir(IMG):
    m = re.match(r"(.+)-(\d+)\.jpg$", f)
    if m:
        PICKS.setdefault(m.group(1), []).append(int(m.group(2)))


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url, "en": url}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


AUTUMN_END = "2026-12-06"  # 2026年秋のライトアップ・特別期間の最終日。この日を過ぎると秋だけの行と注意書きは自動で消える
NIGHT_AUTUMN_ONLY = {"from": None, "to": None, "url": None,
                     "head": T("夜の拝観は秋だけ", "Evening visits: autumn only"),
                     "text": T("このルートでは17時すぎに着きますが、夜に開くのは秋のライトアップの期間だけです。ほかの時期は16:00で受付が終わるので、行きたい日は南禅寺より前に回ってください。",
                               "On this route you arrive after 17:00, but the temple only opens in the evening during the autumn light-up. At other times reception closes at 16:00, so if you want to go in, visit it before Nanzen-ji.")}


def info(rows, tip=None, verified=True):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid, extra=None):
    # extra: ネットから借りた写真（{"file", "credit": {"author", "license", "page"}}）。写真の上に撮影者とライセンスが出る
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def cc(file, author, license, title):
    return {"file": file, "credit": {"author": author, "license": license, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


S = [
    dict(id="station", name=T("JR稲荷駅", "JR Inari Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都駅からJR奈良線で2駅、約6分。改札を出た目の前が伏見稲荷大社の大鳥居です。",
                 "Two stops (about 6 min) from Kyoto Station on the JR Nara Line. Fushimi Inari’s great torii is right outside the gate."),
         lat=34.96717, lng=135.76926,
         text=T("JR稲荷駅（いなりえき）\n\n京都駅のJR奈良線のホームから、各駅停車で2駅、約6分。朱色に塗られた小さな駅で、駅を出るとすぐ伏見稲荷大社の大鳥居が見えます。\n\n千本鳥居は朝のうちが空いていて歩きやすいので、早めの出発がおすすめです。\n\nおすすめ出発時間：8:30",
                "JR Inari Station\n\nFrom the JR Nara Line platforms at Kyoto Station, it’s two stops on a local train, about 6 minutes. The little station is painted vermilion, and Fushimi Inari’s great torii is right in front of you as you come out.\n\nThe Thousand Torii are quietest in the morning, so set off early.\n\nRecommended departure time: 8:30"),
         gmaps=[gm("JR稲荷駅", "JR Inari Station", 34.96717, 135.76926, "JR稲荷駅")],
         links=[link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/")],
         info=info([row("train", "京都→稲荷 JR奈良線で約6分・150円（ICカードも使えます）", "Kyoto → Inari: about 6 min on the JR Nara Line, ¥150 (IC cards accepted)")],
                   tip=T("運賃は乗換案内で確認しました。", "Fare checked on a route planner."))),
    dict(id="inari", name=T("伏見稲荷大社", "Fushimi Inari Taisha"), kind=T("神社", "Shrine"),
         blurb=T("どこまでも続く朱色の「千本鳥居」。全国の稲荷神社の総本宮です。",
                 "The endless vermilion tunnels of the Thousand Torii, at the head shrine of all Inari shrines in Japan."),
         lat=34.96714, lng=135.77267,
         text=T("伏見稲荷大社（ふしみいなりたいしゃ）\n\n商売繁盛の神さま「お稲荷さん」の総本宮。楼門と本殿にお参りしたら、奥へ進んで千本鳥居をくぐりましょう。奉納された鳥居がすき間なく並び、朱色のトンネルが続きます。\n\nあちこちに神さまのお使いのキツネの像があり、口に鍵や玉をくわえています。稲荷山の山頂まで登ると往復2時間ほどかかるので、時間が限られる日は、四ツ辻（よつつじ）あたりで引き返すのがおすすめです。\n\n境内は自由に参拝できます。\n\nおすすめ訪問時間：8:40〜10:00",
                "Fushimi Inari Taisha\n\nThe head shrine of Inari, the god of business and good harvests. After praying at the gate and main hall, head to the back and walk through the Thousand Torii, where donated gates stand so close together that they form vermilion tunnels.\n\nFox statues, the god’s messengers, stand everywhere with keys or jewels in their mouths. Climbing to the top of Mt. Inari and back takes about two hours, so on a busy day turn back around Yotsutsuji.\n\nThe shrine grounds are open to visit freely.\n\nRecommended visit time: 8:40–10:00"),
         gmaps=[gm("伏見稲荷大社", "Fushimi Inari Taisha", 34.96714, 135.77267, "伏見稲荷大社")],
         links=[link("official", "伏見稲荷大社 公式サイト", "Fushimi Inari Taisha (official)", "https://inari.jp/")],
         info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    dict(id="tofukuji", name=T("東福寺", "Tofuku-ji Temple"), kind=T("お寺", "Temple"),
         blurb=T("谷を埋めつくすもみじを、木の橋「通天橋」から見下ろす。京都でも指折りの紅葉の名所です。",
                 "Look down from the wooden Tsutenkyo bridge onto a valley full of maples, one of Kyoto’s great autumn sights."),
         lat=34.97677, lng=135.77371,
         text=T("東福寺（とうふくじ）\n\n伏見稲荷から歩いて約20分（JRなら東福寺駅まで1駅）。大きな禅寺で、渓谷にかかる通天橋（つうてんきょう）から見る紅葉は、まるで赤い雲海のようです。新緑の季節もきれいです。\n\n秋の見ごろ（11月中ごろ〜12月はじめ）はとても混むので、朝早めに行くのがおすすめです。\n\nおすすめ訪問時間：10:20〜11:10",
                "Tofuku-ji Temple\n\nAbout 20 minutes on foot from Fushimi Inari (or one stop on the JR to Tofukuji Station). From the Tsutenkyo bridge over the ravine at this large Zen temple, the autumn leaves look like a sea of red clouds. The fresh green of spring is lovely too.\n\nIt gets very crowded at the autumn peak (mid-November to early December), so go early.\n\nRecommended visit time: 10:20–11:10"),
         gmaps=[gm("東福寺", "Tofuku-ji", 34.97677, 135.77371, "東福寺 通天橋")],
         links=[link("official", "東福寺 公式サイト（拝観案内）", "Tofuku-ji (official, Japanese)", "https://tofukuji.jp/guide/")],
         info=info([row("hours", "4月1日〜12月6日 受付9:00〜16:00（16:30閉門。11月14日〜12月6日の通天橋は8:30から）、12月7日〜3月31日 受付9:00〜15:30（16:00閉門）",
                        "1 Apr – 6 Dec: entry 9:00–16:00 (gates close 16:30; Tsutenkyo from 8:30 on 14 Nov – 6 Dec). 7 Dec – 31 Mar: entry 9:00–15:30 (close 16:00)"),
                    row("fee", "秋（2026年11月14日〜12月6日）は通天橋 大人1,000円・本坊庭園 大人600円（共通券なし）", "Autumn (14 Nov – 6 Dec 2026): Tsutenkyo ¥1,000, Hojo garden ¥600 per adult (no combined ticket)", until=AUTUMN_END),
                    row("fee", "秋以外は通天橋・開山堂 大人600円、本坊庭園 大人600円、共通券 大人1,000円", "Outside autumn: Tsutenkyo & Kaisando ¥600, Hojo garden ¥600, combined ticket ¥1,000 per adult")])),
    dict(id="sennyuji", name=T("泉涌寺と雲龍院", "Sennyu-ji and Unryu-in"), kind=T("お寺", "Temple"),
         blurb=T("皇室とゆかりの深い「御寺（みてら）」。別院の雲龍院では、丸い窓から庭を眺めます。",
                 "The “Mitera”, a temple with deep ties to the imperial family. At its sub-temple Unryu-in, look at the garden through a round window."),
         lat=34.97810, lng=135.78010,
         text=T("泉涌寺（せんにゅうじ）と雲龍院（うんりゅういん）\n\n東福寺から歩いて約15分。歴代の天皇のお墓がある、皇室の菩提寺です。木々に囲まれた静かな境内で、混み合う東山の中では、ゆっくりできる場所です。\n\n奥にある別院の雲龍院では、「悟りの窓」と呼ばれる丸い窓や、障子の四角い窓から庭を眺められます。雲龍院は泉涌寺とは別に拝観料が必要で、水曜はお休みです（11月は水曜も開いています）。\n\n参道の途中から少し入ったところには、朱色の橋の先に、泉涌寺の山内寺院の今熊野観音寺（いまくまのかんのんじ）もあります。\n\nここから清水寺までは、歩いて約30分。疲れたら、泉涌寺道のバス停から市バスで五条坂へ。\n\nおすすめ訪問時間：11:30〜12:30",
                "Sennyu-ji and Unryu-in\n\nAbout 15 minutes on foot from Tofuku-ji. This is the family temple of the imperial household, where generations of emperors are buried. Its quiet, wooded grounds are a place to slow down in busy Higashiyama.\n\nAt Unryu-in, a sub-temple further in, you can look at the garden through the round “Window of Enlightenment” and square paper windows. Unryu-in has its own admission and is closed on Wednesdays (except in November).\n\nJust off the approach, across a vermilion bridge, is Imakumano Kannon-ji, another of Sennyu-ji’s temples.\n\nFrom here it’s about 30 minutes on foot to Kiyomizu-dera. If you’re tired, take a city bus from the Sennyuji-michi stop to Gojozaka.\n\nRecommended visit time: 11:30–12:30"),
         gmaps=[gm("泉涌寺", "Sennyu-ji", 34.97810, 135.78010, "泉涌寺"), gm("雲龍院", "Unryu-in", 34.97727, 135.78040, "泉涌寺 雲龍院")],
         links=[link("official", "御寺 泉涌寺（拝観のご案内）", "Sennyu-ji (official, Japanese)", "https://www.mitera.org/guide/"),
                link("official", "泉涌寺別院 雲龍院", "Unryu-in (official, Japanese)", "https://www.unryuin.jp/")],
         info=info([row("hours", "泉涌寺 9:00〜16:30（17:00閉門）、12〜2月は16:00まで（16:30閉門）", "Sennyu-ji: 9:00–16:30 (gates close 17:00); until 16:00 in Dec–Feb (close 16:30)"),
                    row("fee", "泉涌寺 伽藍拝観 大人500円・小中学生300円", "Sennyu-ji: ¥500 adults, ¥300 elementary/junior high"),
                    row("hours", "雲龍院 9:00〜17:00（受付16:30まで）。水曜休み（11月を除く）。ほかに行事で休む日あり", "Unryu-in: 9:00–17:00 (last entry 16:30). Closed Wednesdays (except November) and on some event days"),
                    row("fee", "雲龍院 400円（泉涌寺とは別）", "Unryu-in: ¥400 (separate from Sennyu-ji)")])),
    # 三十三間堂と銀閣寺は Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    # 三十三間堂は寺が画像の利用に許可を求めているので、公道（七条通）から撮った外観の写真だけ（CC0）
    dict(id="sanjusangendo", name=T("三十三間堂", "Sanjusangen-do"), kind=T("お寺", "Temple"),
         blurb=T("長さ約120mのお堂に、1,001体の千手観音がずらりと並びます。泉涌寺と清水寺の間の寄り道に。",
                 "A hall about 120 m long, holding 1,001 statues of the thousand-armed Kannon. A detour between Sennyu-ji and Kiyomizu-dera."),
         lat=34.98817, lng=135.77178,
         text=T("三十三間堂（さんじゅうさんげんどう）\n\n正式な名前は蓮華王院（れんげおういん）。南北に約120mある本堂（国宝）の中に、千手観音の立像が1,001体、段になって並んでいます。柱と柱の間が33あるので「三十三間堂」。観音像の前には風神・雷神と二十八部衆の像も立ち、すべて国宝です（公式サイトより）。\n\n"
                "堂内は撮影できません。靴を脱いで上がるので、脱ぎやすい靴が楽です。11月16日〜3月31日は受付が15:30までと早く閉まります。\n\n"
                "泉涌寺から歩いて約25分。ここから清水寺までは上り坂を歩いて約30分で、すぐ前の「博物館三十三間堂前」から東山通を北へ行く市バスに乗れば「五条坂」まで行けます。\n\n"
                "このマップの時間には入っていない寄り道です。寄る日は、清水寺に着くのが1時間ほど遅くなるので、ほかの場所を1〜2か所減らしてください。\n\nおすすめ訪問時間：12:55〜13:35",
                "Sanjusangen-do\n\nOfficially Rengeo-in. Inside the main hall, a National Treasure about 120 m long from north to south, 1,001 standing statues of the thousand-armed Kannon are lined up in tiers. The name means “hall of 33 bays”, the spaces between its pillars. Statues of the Wind and Thunder Gods and 28 guardian deities stand in front, all National Treasures (from the official website).\n\n"
                "No photos inside. You take your shoes off, so wear ones that slip on and off. From 16 November to 31 March, last entry is as early as 15:30.\n\n"
                "About 25 minutes on foot from Sennyu-ji. Kiyomizu-dera is about 30 minutes’ walk uphill from here, or take a northbound city bus on Higashiyama-dori from the “Hakubutsukan-Sanjusangendo-mae” stop right outside to “Gojozaka”.\n\n"
                "This is a detour not counted in this map’s times. If you stop here you’ll reach Kiyomizu-dera about an hour later, so drop one or two other places.\n\nRecommended visit time: 12:55–13:35"),
         gmaps=[gm("三十三間堂", "Sanjusangen-do", 34.98817, 135.77178, "三十三間堂")],
         links=[link("official", "三十三間堂 公式サイト（拝観）", "Sanjusangen-do (official, Japanese)", "https://www.sanjusangendo.jp/visit/")],
         info={"rows": [row("hours", "4月1日〜11月15日 8:30〜17:00、11月16日〜3月31日 9:00〜16:00（受付は30分前まで）。年中無休", "1 Apr – 15 Nov 8:30–17:00; 16 Nov – 31 Mar 9:00–16:00 (last entry 30 min before). Open every day"),
                        row("fee", "一般600円、中高生400円、小学生300円", "¥600 adults, ¥400 junior/senior high, ¥300 elementary"),
                        row("train", "市バス「博物館三十三間堂前」すぐ（京都駅から約10分）。京阪 七条駅から歩いて約7分", "City bus stop “Hakubutsukan-Sanjusangendo-mae” (about 10 min from Kyoto Station). 7 min on foot from Keihan Shichijo Station")],
               "cash": False, "checked": "2026-11-21",
               "tip": T("2026年11月21日に三十三間堂の公式サイトで確認しました。歩く時間は地図で測った目安です。", "Checked on the official Sanjusangen-do website on 21 November 2026. Walking times are estimates measured on a map.")},
         _extra=[cc("sanjusangendo-1.jpg", "TKdows 2026", "CC0", "File:JP 日本 Japan 京都 Kyoto 七條通 Shichijo Dori Street tourism 三十三間堂 Sanjūsangen-dō Temples June 2026 N13P 07.jpg"),
                 cc("sanjusangendo-2.jpg", "TKdows 2026", "CC0", "File:JP 日本 Japan 京都 Kyoto 七條通 Shichijo Dori Street tourism 三十三間堂 Sanjūsangen-dō Temples June 2026 N13P 40.jpg")]),
    dict(id="kiyomizu", name=T("清水寺", "Kiyomizu-dera"), kind=T("お寺", "Temple"),
         blurb=T("「清水の舞台」から京都の町を一望。春・夏・秋の夜間特別拝観では、ライトアップも。",
                 "Look out over Kyoto from the famous wooden stage. Evening openings in spring, summer and autumn are lit up too."),
         lat=34.99485, lng=135.78505,
         text=T("清水寺（きよみずでら）\n\n音羽山（おとわやま）の中腹に建つお寺。崖の上にせり出した本堂の「清水の舞台」からは、京都の町が見渡せます。少し離れた奥の院のあたりから振り返ると、木々の上に浮かぶ舞台の全景が見えます。\n\n朱色の仁王門と三重塔もきれいです。春・夏・秋の夜間特別拝観の時期は、21:30まで（受付は21:00まで）開いていて、ライトアップされた舞台と京都の夜景を楽しめます。\n\nおすすめ訪問時間：13:00〜14:00",
                "Kiyomizu-dera\n\nA temple on the slopes of Mt. Otowa. From the “Kiyomizu stage” of the main hall, jutting out over the cliff, you can see across the city. Look back from near the Okunoin hall for the whole stage floating above the trees.\n\nThe vermilion Nio Gate and three-storied pagoda are beautiful too. During the special evening openings in spring, summer and autumn, the temple stays open until 21:30 (last entry 21:00), with the lit-up stage and the city lights below.\n\nRecommended visit time: 13:00–14:00"),
         gmaps=[gm("清水寺", "Kiyomizu-dera", 34.99485, 135.78505, "清水寺")],
         links=[link("official", "清水寺 公式サイト（拝観時間・アクセス）", "Kiyomizu-dera (official)", "https://www.kiyomizudera.or.jp/access.php")],
         info=info([row("hours", "6:00〜18:00（7・8月は18:30まで）。夜間特別拝観の期間は21:30まで（受付21:00）", "6:00–18:00 (18:30 in July–August). Until 21:30 during special evening openings (last entry 21:00)")],
                   tip=T("拝観料は公式サイトで確認してください。", "Check the admission fee on the official website."))),
    dict(id="sanneizaka", name=T("産寧坂（三年坂）と二年坂", "Sannenzaka and Ninenzaka"), kind=T("町並み", "Historic street"),
         blurb=T("石畳と古い町家が続く坂道。清水寺から下りながら、お店をのぞいて歩きます。",
                 "Stone-paved slopes lined with old townhouses. Walk down from Kiyomizu-dera, peeking into the shops."),
         lat=34.99680, lng=135.78120,
         text=T("産寧坂（さんねいざか）と二年坂（にねんざか）\n\n清水寺の門前から北へ下る、石畳の坂道です。昔ながらの町家にお土産屋さんやカフェが並び、京都らしい町並みが続きます。\n\n町家を生かしたスターバックスや、抹茶のお菓子のお店など、のぞいてみたいお店がたくさん。昼間はとても混むので、朝早くや夕方の、人の少ない時間もおすすめです。\n\nおすすめ訪問時間：14:00〜14:40",
                "Sannenzaka and Ninenzaka\n\nStone-paved lanes running downhill north of Kiyomizu-dera. Old townhouses with souvenir shops and cafés line the way: the classic Kyoto streetscape.\n\nThere’s a Starbucks in a traditional townhouse, matcha sweet shops and much more to browse. It’s very crowded in the middle of the day; early morning or evening, when it’s quieter, is lovely too.\n\nRecommended visit time: 14:00–14:40"),
         gmaps=[gm("産寧坂", "Sannenzaka", 34.99680, 135.78120, "産寧坂")],
         links=[], info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    dict(id="yasakatower", name=T("八坂の塔（法観寺）", "Yasaka Pagoda (Hokan-ji)"), kind=T("町並み・お寺", "Historic street & temple"),
         blurb=T("石畳の坂の先にそびえる五重塔。東山でいちばん絵になる景色です。",
                 "A five-storied pagoda rising at the end of a stone-paved lane: the most photogenic view in Higashiyama."),
         lat=34.99843, lng=135.77952,
         text=T("八坂の塔（やさかのとう）\n\n法観寺（ほうかんじ）の五重塔で、高さは約46m。八坂通の坂道から見上げる塔の姿は、京都を代表する景色のひとつです。\n\n夕暮れどき、空を背にした塔のシルエットもすてきです。\n\nおすすめ訪問時間：14:40",
                "Yasaka Pagoda\n\nThe roughly 46-meter five-storied pagoda of Hokan-ji. The view of it from the slope of Yasaka-dori is one of Kyoto’s iconic sights.\n\nAt dusk, its silhouette against the sky is lovely too.\n\nRecommended visit time: 14:40"),
         gmaps=[gm("八坂の塔", "Yasaka Pagoda", 34.99843, 135.77952, "八坂の塔 法観寺")],
         links=[], info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    dict(id="kodaiji", name=T("高台寺と圓徳院", "Kodai-ji and Entoku-in"), kind=T("お寺", "Temple"),
         blurb=T("豊臣秀吉の妻・ねねゆかりのお寺。秋の夜のライトアップは、池に映る紅葉が見事です。",
                 "The temple of Nene, wife of Toyotomi Hideyoshi. In autumn evenings the lit-up maples reflect in the pond."),
         lat=35.00077, lng=135.78166,
         text=T("高台寺（こうだいじ）と圓徳院（えんとくいん）\n\n豊臣秀吉の妻・北政所（きたのまんどころ）ねねが、秀吉の菩提を弔うために建てたお寺です。池泉回遊式の庭や竹林の小道を歩けます。\n\n春・夏・秋には夜間特別拝観があり、庭のライトアップと方丈前庭のプロジェクションマッピングを楽しめます。ねねの道をはさんだ向かいの圓徳院は、ねねが晩年を過ごした場所で、座敷から眺める北庭がおすすめ。2か寺の共通券があります。\n\nおすすめ訪問時間：15:00〜15:50",
                "Kodai-ji and Entoku-in\n\nKodai-ji was built by Nene (Kita-no-Mandokoro), wife of Toyotomi Hideyoshi, to pray for him. You can walk its pond garden and bamboo path.\n\nIn spring, summer and autumn there are special evening openings, with the garden lit up and projection mapping on the rock garden. Across Nene-no-michi, Entoku-in is where Nene spent her last years; its north garden, seen from the tatami rooms, is my favorite. There’s a combined ticket for both.\n\nRecommended visit time: 15:00–15:50"),
         gmaps=[gm("高台寺", "Kodai-ji", 35.00077, 135.78166, "高台寺"), gm("圓徳院", "Entoku-in", 35.00066, 135.77942, "圓徳院 京都")],
         links=[link("official", "高台寺 公式サイト（拝観案内）", "Kodai-ji (official, Japanese)", "https://www.kodaiji.com/haikan.html")],
         info=info([row("hours", "9:00〜17:30（受付17:00まで）。夜間特別拝観の期間は22:00まで（受付21:30）", "9:00–17:30 (last entry 17:00). Until 22:00 during evening openings (last entry 21:30)"),
                    row("fee", "高台寺 大人800円・中高生400円。高台寺・圓徳院の共通券1,200円", "Kodai-ji ¥800 adults, ¥400 junior/senior high. Combined ticket with Entoku-in ¥1,200")])),
    dict(id="yasaka", name=T("八坂神社と円山公園", "Yasaka Shrine and Maruyama Park"), kind=T("神社・公園", "Shrine & park"),
         blurb=T("祇園の「八坂さん」。奥の円山公園には、春に夜桜が見事な「祇園しだれ桜」があります。",
                 "Gion’s beloved shrine. In Maruyama Park behind it, the great weeping cherry is stunning at night in spring."),
         lat=35.00366, lng=135.77856,
         text=T("八坂神社（やさかじんじゃ）と円山公園（まるやまこうえん）\n\n祇園の東の端にある、京都の人に「八坂さん」と親しまれる神社です。四条通の突き当たりに立つ朱色の西楼門が目印。祇園祭はこの神社のお祭りです。\n\n境内を抜けた先の円山公園には、大きな「祇園しだれ桜」があり、春の夜のライトアップは本当にきれいです。円山公園の北には知恩院（ちおんいん）があり、南禅寺へ歩く途中で国宝の大きな三門の前を通ります。\n\n境内は自由に参拝できます。\n\nおすすめ訪問時間：16:00〜16:30",
                "Yasaka Shrine and Maruyama Park\n\nAt the eastern end of Gion, this shrine is affectionately called “Yasaka-san” by locals. Its vermilion west gate at the end of Shijo-dori is the landmark, and the Gion Matsuri is this shrine’s festival.\n\nThrough the grounds, Maruyama Park has a huge weeping cherry tree; lit up on spring nights, it’s truly beautiful. Just north of the park is Chion-in: on the walk to Nanzen-ji you pass its huge Sanmon gate, a National Treasure.\n\nThe shrine grounds are open to visit freely.\n\nRecommended visit time: 16:00–16:30"),
         gmaps=[gm("八坂神社", "Yasaka Shrine", 35.00366, 135.77856, "八坂神社"), gm("円山公園", "Maruyama Park", 35.00380, 135.78000, "円山公園 京都")],
         links=[link("official", "八坂神社 公式サイト", "Yasaka Shrine (official)", "https://www.yasaka-jinja.or.jp/")],
         info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    dict(id="nanzenji", name=T("南禅寺", "Nanzen-ji Temple"), kind=T("お寺", "Temple"),
         blurb=T("巨大な三門と、レンガ造りの水路閣。紅葉の季節はとくに見事です。",
                 "A huge wooden gate and the brick Suirokaku aqueduct, especially beautiful in autumn."),
         lat=35.01136, lng=135.79348,
         text=T("南禅寺（なんぜんじ）\n\n八坂神社から歩いて約25分（地下鉄なら蹴上駅から歩いて約10分）。歌舞伎で石川五右衛門が「絶景かな」と言う大きな三門は、上に登って東山の景色を眺められます（三門と方丈庭園は17:00まで。上りたい日は、ほかの場所を減らして16:40までに着くように）。\n\n境内の奥には、明治時代に琵琶湖の水を京都へ引くために造られたレンガの水路閣があり、今も水が流れています。小堀遠州作と伝わる方丈庭園もおすすめです。境内は自由に歩けます。\n\nおすすめ訪問時間：17:00〜17:25（境内と水路閣。三門と方丈庭園は17:00で閉まります）",
                "Nanzen-ji Temple\n\nAbout 25 minutes on foot from Yasaka Shrine (or about 10 minutes from Keage subway station). You can climb the huge Sanmon gate, made famous in kabuki, for a view over Higashiyama. (The gate and Hojo garden close at 17:00; to go up, drop a stop or two and arrive by 16:40.)\n\nDeeper in the grounds stands the brick Suirokaku aqueduct, built in the Meiji era to bring water from Lake Biwa to Kyoto, and water still flows over it. The Hojo garden, said to be by Kobori Enshu, is lovely too. The grounds are free to walk around.\n\nRecommended visit time: 17:00–17:25 (the grounds and aqueduct; the gate and Hojo garden close at 17:00)"),
         gmaps=[gm("南禅寺", "Nanzen-ji", 35.01136, 135.79348, "南禅寺"), gm("水路閣", "Suirokaku", 35.01080, 135.79470, "南禅寺 水路閣")],
         links=[link("official", "南禅寺 公式サイト（拝観案内）", "Nanzen-ji (official, Japanese)", "https://nanzenji.or.jp/about_rinzaishu/visit")],
         info=info([row("hours", "8:40〜17:00（12〜2月は16:30まで）。受付は20分前まで。12月28〜31日は拝観休止", "8:40–17:00 (until 16:30 Dec–Feb); last entry 20 min before. No visits 28–31 Dec"),
                    row("fee", "三門 大人600円、方丈庭園 大人600円（境内は無料）", "Sanmon gate ¥600, Hojo garden ¥600 per adult (grounds free)")])),
    dict(id="ginkakuji", name=T("哲学の道と銀閣寺", "Philosopher’s Path and Ginkaku-ji"), kind=T("散歩道・お寺", "Walk & temple"),
         blurb=T("疏水沿いの散歩道を北へ歩いて、銀閣寺へ。白い砂の庭と、こけら葺きの観音殿（銀閣）を見ます。17:00に閉まるので、夜の永観堂より先に。",
                 "Walk north along the canal path to Ginkaku-ji, with its white sand garden and shingle-roofed Silver Pavilion. It closes at 17:00, so come before the evening at Eikan-do."),
         lat=35.02690, lng=135.79837,
         text=T("哲学の道（てつがくのみち）と銀閣寺（ぎんかくじ）\n\n哲学の道は、永観堂の少し北の若王子橋（にゃくおうじばし）から銀閣寺橋まで、琵琶湖疏水に沿って続く約1.5kmの散歩道です。春は桜、秋は紅葉の並木になります。南禅寺から銀閣寺までは、この道を通って歩いて約40分。\n\n"
                "銀閣寺の正式な名前は慈照寺（じしょうじ）。室町幕府の8代将軍・足利義政の山荘がもとになったお寺です。入ってすぐ、白砂を段に盛った銀沙灘（ぎんしゃだん）と円すい形の向月台（こうげつだい）、その奥に観音殿（銀閣・国宝）。順路は山の上の展望所まで続き、境内と京都の町を見下ろせます。中を回るのに約30分です（公式サイトより）。\n\n"
                "閉まるのは17:00（12月〜2月は16:30）。このマップの時間どおりに八坂神社まで回ると間に合わないので、銀閣寺へ行く日は手前の場所をいくつか外して、南禅寺を15:25ごろに出てください。\n\n"
                "秋の夜に永観堂や金戒光明寺のライトアップへ行く日も、銀閣寺が先です。見終わったら哲学の道を戻って（約25分）、17:30からの永観堂へ。ここで終わる日は、「銀閣寺道」のバス停から市バスで四条河原町や京都駅へ帰れます。\n\nおすすめ訪問時間：16:05〜16:40（17:00に閉まります。12月〜2月は16:30）",
                "Philosopher’s Path and Ginkaku-ji\n\nThe Philosopher’s Path follows the Lake Biwa Canal for about 1.5 km, from Nyakuoji bridge just north of Eikan-do to Ginkakuji bridge. It is lined with cherry trees in spring and coloured leaves in autumn. From Nanzen-ji to Ginkaku-ji along the path is about 40 minutes on foot.\n\n"
                "Ginkaku-ji, officially Jisho-ji, began as the mountain villa of Ashikaga Yoshimasa, the eighth Muromachi shogun. Just inside are the Ginshadan, a terrace of raked white sand, and the cone-shaped Kogetsudai; behind them stands the Kannon hall, the Silver Pavilion (a National Treasure). The route climbs to a lookout over the grounds and the city. Allow about 30 minutes (from the official website).\n\n"
                "It closes at 17:00 (16:30 from December to February). If you follow this map’s times as far as Yasaka Shrine you won’t make it, so on a Ginkaku-ji day drop a few earlier places and leave Nanzen-ji at about 15:25.\n\n"
                "Ginkaku-ji also comes first on autumn evenings when you’re going to the light-ups at Eikan-do or Konkai Komyo-ji. Afterwards walk back down the path (about 25 minutes) for Eikan-do from 17:30. If you finish here, city buses from the “Ginkakuji-michi” stop go to Shijo-Kawaramachi and Kyoto Station.\n\nRecommended visit time: 16:05–16:40 (closes at 17:00; 16:30 from December to February)"),
         gmaps=[gm("銀閣寺", "Ginkaku-ji", 35.02690, 135.79837, "銀閣寺 慈照寺"), gm("哲学の道（若王子橋）", "Philosopher’s Path (south end)", 35.01539, 135.79580, "哲学の道 若王子橋")],
         links=[link("official", "銀閣寺 公式サイト（アクセス・拝観）", "Ginkaku-ji (official, Japanese)", "https://www.shokoku-ji.jp/ginkakuji/access/")],
         info={"rows": [row("hours", "3月1日〜11月30日 8:30〜17:00、12月1日〜2月末 9:00〜16:30。年中無休", "1 Mar – 30 Nov 8:30–17:00; 1 Dec – end of Feb 9:00–16:30. Open every day"),
                        row("fee", "大人（高校生以上）1,000円、小・中学生500円（2026年4月から）", "¥1,000 adults (high school and up), ¥500 elementary/junior high (from April 2026)"),
                        row("hours", "秋の特別拝観（東求堂など、2026年11月1日〜12月5日）：10:00・11:00・12:00・13:30・14:30・15:30から約30分、各回約20名。当日、本堂前の申込表に名前を書きます。2,000円（拝観料は別）",
                            "Autumn special viewing (Togudo and more, 1 Nov – 5 Dec 2026): about 30 min from 10:00, 11:00, 12:00, 13:30, 14:30 and 15:30, about 20 people each. Sign up on the day at the main hall. ¥2,000 on top of admission; guided in Japanese", until="2026-12-05"),
                        row("train", "市バス「銀閣寺道」（5・7・32・203・204系統など）", "City bus stop “Ginkakuji-michi” (routes 5, 7, 32, 203, 204 and others)")],
               "cash": False, "checked": "2026-11-21",
               "tip": T("2026年11月21日に銀閣寺（相国寺）の公式サイトで確認しました。哲学の道の長さと歩く時間は地図で測った目安です。", "Checked on the official Ginkaku-ji (Shokoku-ji) website on 21 November 2026. The length of the path and walking times are estimates measured on a map.")},
         _extra=[cc("ginkakuji-1.jpg", "Jmhullot", "CC BY 3.0", "File:Ginkakuji Fall1.jpg"),
                 cc("ginkakuji-2.jpg", "Jmhullot", "CC BY 3.0", "File:Ginkakuji Sand Garden.jpg"),
                 cc("ginkakuji-3.jpg", "Stephan Ridgway", "CC BY 2.0", "File:Philosophers Walk, Kyoto (49073313687).jpg"),
                 cc("ginkakuji-4.jpg", "Yiannis Theologos Michellis", "CC0", "File:Japan Spring Down the Philosopher's Path (14164491752).jpg")]),
    dict(id="eikando", name=T("永観堂（禅林寺）", "Eikan-do (Zenrin-ji)"), kind=T("お寺", "Temple"),
         blurb=T("「もみじの永観堂」。秋の夜は、池のまわりの紅葉がライトアップで燃えるようです。",
                 "“Eikan-do of the maples”. On autumn nights, the lit-up leaves around the pond seem to blaze."),
         lat=35.01445, lng=135.79452,
         text=T("永観堂（えいかんどう）\n\n南禅寺から歩いて約5分。古くから「もみじの永観堂」と呼ばれる紅葉の名所です。秋の寺宝展の期間は夜のライトアップがあり、放生池（ほうじょういけ）の水面に、紅葉と山の上の多宝塔が映ります。\n\n昼の寺宝展と夜のライトアップは入れ替え制で、券も別です。秋の夜はとても混むので、時間に余裕をもって行きましょう。\n\nおすすめ訪問時間：17:30〜18:30（秋のライトアップ）",
                "Eikan-do (Zenrin-ji)\n\nAbout 5 minutes on foot from Nanzen-ji. Long known as “Eikan-do of the maples”. During the autumn treasure exhibition there are evening light-ups, with the maples and the hilltop pagoda reflected in the pond.\n\nThe daytime exhibition and the evening light-up are separate, with separate tickets. Autumn evenings are very busy, so allow plenty of time.\n\nRecommended visit time: 17:30–18:30 (autumn light-up)"),
         gmaps=[gm("永観堂", "Eikan-do", 35.01445, 135.79452, "永観堂 禅林寺")],
         links=[link("official", "永観堂 拝観のご案内", "Eikan-do visitor info (Japanese)", "https://www.eikando.or.jp/haikan.html")],
         info=info([row("hours", "秋の寺宝展（2026年11月11日〜12月6日）受付9:00〜16:00（17:00閉門）。ライトアップ（11月20日〜12月6日）受付17:30〜20:30（21:00閉門）。昼と夜は入れ替え制",
                        "Autumn exhibition (11 Nov – 6 Dec 2026): entry 9:00–16:00 (gates close 17:00). Light-up (20 Nov – 6 Dec): entry 17:30–20:30 (close 21:00). Day and night are separate sessions", until=AUTUMN_END),
                    row("fee", "秋の寺宝展 一般1,500円、ライトアップ 中高生以上1,000円", "Autumn exhibition ¥1,500; light-up ¥1,000 (junior high and up)", until=AUTUMN_END),
                    row("hours", "秋の寺宝展以外 受付9:00〜16:00（17:00閉門）、年中無休", "Outside the autumn exhibition: entry 9:00–16:00 (gates close 17:00), open every day"),
                    row("fee", "秋の寺宝展以外 一般1,000円", "Outside the autumn exhibition: ¥1,000 (adults)")]),
         notices=[NIGHT_AUTUMN_ONLY]),
    dict(id="kurodani", name=T("金戒光明寺（くろ谷さん）", "Konkai Komyo-ji (Kurodani)"), kind=T("お寺", "Temple"),
         blurb=T("京都の人に「くろ谷さん」と呼ばれる大きなお寺。石段の上の山門から、京都の町を見渡せます。",
                 "A large temple known locally as “Kurodani-san”. From the gate at the top of the steps, you look out over Kyoto."),
         lat=35.01975, lng=135.78838,
         text=T("金戒光明寺（こんかいこうみょうじ）\n\n永観堂から歩いて約15分。浄土宗の大きなお寺で、幕末には京都守護職・会津藩の本陣が置かれました。石段の上にそびえる山門は迫力があります。\n\n境内は自由に歩けます。秋などには庭園の特別公開やライトアップがあり、竹林や池のまわりの紅葉が照らされます（2026年秋の夜間特別拝観は11月13日〜12月6日。予約はいりません）。\n\n帰りは岡崎道のバス停から市バス、または地下鉄の東山駅まで歩いて約20分です。\n\nおすすめ訪問時間：18:45〜19:20",
                "Konkai Komyo-ji\n\nAbout 15 minutes on foot from Eikan-do. A large Pure Land temple, it served as the headquarters of the Aizu clan, Kyoto’s guardians, at the end of the Edo period. The great gate at the top of the stone steps is impressive.\n\nThe grounds are free to walk around. In autumn and other seasons there are special garden openings and light-ups, with the bamboo grove and maples around the pond lit up (the 2026 autumn evening opening runs 13 Nov – 6 Dec, no booking needed).\n\nTo go back, take a city bus from Okazaki-michi, or walk about 20 minutes to Higashiyama subway station.\n\nRecommended visit time: 18:45–19:20"),
         gmaps=[gm("金戒光明寺", "Konkai Komyo-ji", 35.01975, 135.78838, "金戒光明寺")],
         links=[link("official", "金戒光明寺 公式サイト", "Konkai Komyo-ji (official, Japanese)", "https://www.kurodani.jp/"),
                link("info", "金戒光明寺 特別夜間拝観", "Konkai Komyo-ji evening opening", "https://www.kurodani.jp/lightup/")],
         info=info([row("hours", "夜間特別拝観（2026年11月13日〜12月6日）17:30〜20:30（最終入場20:00）", "Evening opening (13 Nov – 6 Dec 2026): 17:30–20:30 (last entry 20:00)", until=AUTUMN_END),
                    row("fee", "夜間特別拝観 御影堂・大方丈・紫雲の庭 大人1,000円、栄摂院 大人800円、セット券 大人1,600円", "Evening opening: Main hall, Hojo & garden ¥1,000; Eisho-in ¥800; set ticket ¥1,600 (adults)", until=AUTUMN_END),
                    row("hours", "ふだんの受付 9:00〜16:00（境内は自由に歩けます）", "Usual reception hours 9:00–16:00 (grounds free to walk)")]),
         notices=[NIGHT_AUTUMN_ONLY]),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"], out.pop("_extra", None))
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
N = len(spots)
data = {
    "id": "higashiyama",
    "_note": "京都・東山の1日ルート（higashiyama/ のページ専用。形は eizan-line.json と同じ）。2026-11-21 に三十三間堂と「哲学の道と銀閣寺」を追加（Toshi はまだ行っていない場所。写真は Wikimedia Commons で photos の要素が {file, credit}、文章は公式サイトの情報だけ。もとの12か所の時間には入っていない寄り道）。JR稲荷駅から伏見稲荷・東福寺・泉涌寺・清水寺・産寧坂・八坂の塔・高台寺・八坂神社・南禅寺・永観堂・金戒光明寺へ、南から北へ歩く。見どころが多いので「選んで回る」で開く（plan.defaultMode）。写真は Toshi の写真ライブラリから選んだもの（東山の約3,300枚の横写真をスポットごとに全部見て、1か所10枚以内・Nikon D7000 を含む。長辺1600px・位置情報なし）。夜の写真の多くは春・秋のライトアップの時期のもの。info.checked は事実情報を確認した日（各寺社の公式サイト。JRの運賃は乗換案内）。info.verified=false は公式サイトで確認できなかった情報（要確認）。このファイルは scripts/build_higashiyama_data.py で作る。",
    "sections": [
        {"first": 1, "last": 2, "day": 0}, {"first": NO["tofukuji"], "last": NO["sanjusangendo"], "day": 1}, {"first": NO["kiyomizu"], "last": NO["yasakatower"], "day": 2},
        {"first": NO["kodaiji"], "last": NO["yasaka"], "day": 3}, {"first": NO["nanzenji"], "last": NO["kurodani"], "day": 4},
    ],
    "plan": {"_note": "「選んで回る」の設定。駅（1）はいつも入る。2〜14 は行きたい場所を選ぶ。三十三間堂と銀閣寺はもとの時間に入っていない寄り道（hints に回り方）。", "defaultMode": "pick",
             "picks": list(range(2, N + 1)), "auto": {"1": {"always": True}},
             "hints": [
                 H("sanjusangendo", {"any": [NO["sanjusangendo"]], "none": [NO["tofukuji"], NO["sennyuji"]]},
                   "東福寺・泉涌寺に寄らない日は、伏見稲荷から京阪電車で七条駅へ（伏見稲荷駅から約5分・180円）。駅から歩いて約7分です。",
                   "Skipping Tofuku-ji and Sennyu-ji? Take the Keihan line from Fushimi-Inari to Shichijo (about 5 min, ¥180), then walk about 7 minutes."),
                 H("nanzenji", {"any": [NO["ginkakuji"]], "andAny": [NO["nanzenji"]]},
                   "銀閣寺は17:00まで（12月〜2月は16:30）。南禅寺を15:25ごろに出られるように、手前の場所をいくつか外してください。南禅寺から銀閣寺までは、哲学の道を歩いて約40分です。",
                   "Ginkaku-ji closes at 17:00 (16:30 from December to February). Drop a few earlier places so that you can leave Nanzen-ji at about 15:25; it’s about 40 minutes’ walk to Ginkaku-ji along the Philosopher’s Path."),
                 H("ginkakuji", {"any": [NO["ginkakuji"]], "andAny": [NO["eikando"], NO["kurodani"]]},
                   "秋のライトアップ（永観堂・金戒光明寺は17:30から）へ行く日は、銀閣寺を先に。16:40ごろに出て哲学の道を戻れば、永観堂に17:10ごろ着きます。秋以外の時期は、永観堂は16:00で受付が終わるので、哲学の道を歩く前に寄ってください。",
                   "On an autumn light-up evening (Eikan-do and Konkai Komyo-ji open from 17:30), see Ginkaku-ji first: leave at about 16:40 and walk back down the path to reach Eikan-do at about 17:10. Outside autumn, Eikan-do stops admitting at 16:00, so visit it before you walk the path."),
                 H("ginkakuji", {"any": [NO["ginkakuji"]], "none": [NO["eikando"], NO["kurodani"]]},
                   "銀閣寺がゴールの日は、参道を下りた「銀閣寺道」のバス停から、市バスで四条河原町・京都駅へ（230円）。",
                   "Finishing at Ginkaku-ji? Walk down the approach to the “Ginkakuji-michi” stop and take a city bus to Shijo-Kawaramachi or Kyoto Station (¥230)."),
             ]},
    "photoBase": "../images/higashiyama/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
