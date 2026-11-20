#!/usr/bin/env python3
"""京都・金閣寺〜北野天満宮ルートのデータ（data/routes/kinkakuji.json）を書き出す。

使い方: python3 scripts/build_kinkakuji_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/kinkakuji/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kinkakuji"
OUT = f"{R}/data/routes/kinkakuji.json"
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


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def info(rows, tip=None, verified=True):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


NONE = {"rows": [], "cash": False, "tip": None, "checked": CHECKED}

S = [
    dict(id="daitokuji", name=T("大徳寺", "Daitoku-ji Temple"), kind=T("お寺", "Temple"),
         blurb=T("土塀と石畳の道に、たくさんの塔頭（たっちゅう）が並ぶ大きな禅寺。朝の静かなうちに。",
                 "A vast Zen temple of earthen walls and stone paths lined with sub-temples. Best in the quiet morning."),
         lat=35.04279, lng=135.74655,
         text=T("大徳寺（だいとくじ）\n\n臨済宗大徳寺派の大本山。広い境内に、土塀に囲まれた塔頭（小さなお寺）が並び、松と石畳の道を歩くだけでも気持ちのいい場所です。"
                "朱色の三門（金毛閣）は、千利休ゆかりの門として知られています。\n\n"
                "塔頭の中には庭を公開しているところもありますが、公開日や拝観料はそれぞれちがうので、行く前に確かめてください。\n\n"
                "京都駅からは市バスで「大徳寺前」下車すぐ。金閣寺へは市バスか、歩いて約25分です。\n\nおすすめ訪問時間：9:00〜9:50",
                "Daitoku-ji Temple\n\nHead temple of the Daitoku-ji school of Rinzai Zen. Its grounds are lined with walled sub-temples, and simply walking the pine-shaded stone paths is a pleasure. "
                "The vermilion Sanmon gate (Kinmokaku) is famous for its links to the tea master Sen no Rikyu.\n\n"
                "Some sub-temples open their gardens to visitors, but days and fees vary, so check before you go.\n\n"
                "From Kyoto Station, take a city bus to “Daitokuji-mae”. To Kinkaku-ji, take a bus or walk about 25 minutes.\n\nRecommended visit time: 9:00–9:50"),
         gmaps=[gm("大徳寺", "Daitoku-ji", 35.04279, 135.74655, "大徳寺 京都市北区")],
         links=[link("info", "臨黄ネット（大徳寺の案内）", "Rinzai-Obaku Zen (Daitoku-ji, Japanese)", "https://www.rinnou.net/cont_03/07daitoku/")],
         info=NONE),
    dict(id="kinkakuji", name=T("金閣寺（鹿苑寺）", "Kinkaku-ji (Rokuon-ji)"), kind=T("お寺", "Temple"),
         blurb=T("池に映る金色の舎利殿。雪の日の金閣は、一度は見てみたい景色です。",
                 "The golden pavilion mirrored in its pond. Kinkaku-ji under snow is a sight worth seeing once in your life."),
         lat=35.03937, lng=135.72924,
         text=T("金閣寺（きんかくじ）\n\n正式には鹿苑寺（ろくおんじ）。室町幕府の将軍・足利義満の山荘がはじまりで、金箔をはった舎利殿「金閣」が鏡湖池（きょうこち）に映る姿は、京都を代表する景色です。\n\n"
                "順路は一方通行で、池のほとりから金閣を眺めたあと、裏山の庭をぐるっと回って出口へ。見学は30分〜1時間ほどです。\n\n"
                "雪が積もった朝の金閣はとくに美しく、そのぶんとても混みます（写真は2026年2月8日）。晴れた日は、池に映る「逆さ金閣」もきれいです。\n\nおすすめ訪問時間：10:10〜11:00",
                "Kinkaku-ji (Rokuon-ji)\n\nOfficially Rokuon-ji. It began as the villa of the shogun Ashikaga Yoshimitsu, and its gold-leafed pavilion reflected in the Kyoko-chi pond is one of Kyoto’s defining views.\n\n"
                "The route is one-way: admire the pavilion from the pond, then loop through the hillside garden to the exit. Allow 30 minutes to an hour.\n\n"
                "On a snowy morning it is especially beautiful, and very crowded (photos: 8 Feb 2026). On clear days, look for the pavilion’s reflection in the pond.\n\nRecommended visit time: 10:10–11:00"),
         gmaps=[gm("金閣寺", "Kinkaku-ji", 35.03937, 135.72924, "金閣寺 鹿苑寺")],
         links=[link("official", "金閣寺 公式サイト（アクセス・参拝料金）", "Kinkaku-ji (official)", "https://www.shokoku-ji.jp/kinkakuji/access/", "https://www.shokoku-ji.jp/en/kinkakuji/")],
         info=info([row("hours", "9:00〜17:00（年中無休）", "9:00–17:00, open every day"),
                    row("fee", "大人（高校生以上）500円、小・中学生300円", "Adults (high school and up) ¥500; elementary and junior high ¥300")],
                   tip=T("市バス「金閣寺道」から歩いてすぐ。", "A short walk from the “Kinkakuji-michi” city bus stop."))),
    dict(id="ryoanji", name=T("龍安寺", "Ryoan-ji Temple"), kind=T("お寺", "Temple"),
         blurb=T("白砂に15の石を置いただけの石庭。縁側に座って、ゆっくり眺めてみてください。",
                 "The rock garden: just fifteen stones on white gravel. Sit on the veranda and take your time."),
         lat=35.03346, lng=135.71809,
         text=T("龍安寺（りょうあんじ）\n\n金閣寺から「きぬかけの路」を歩いて約20分。白い砂に15個の石が置かれた石庭は、どこから見ても1つの石がほかの石にかくれて見えないと言われています。方丈の縁側に座って、静かに眺めてみてください。\n\n"
                "石庭のほかに、大きな鏡容池（きょうようち）のまわりの庭も歩けます。春の桜、秋の紅葉の時期もきれいです。\n\nおすすめ訪問時間：11:20〜12:10",
                "Ryoan-ji Temple\n\nAbout 20 minutes’ walk from Kinkaku-ji along the Kinukake-no-michi road. Its rock garden sets fifteen stones on white gravel, and it’s said that from any spot one stone is always hidden behind another. Sit on the veranda and look at it quietly.\n\n"
                "You can also stroll around the large Kyoyo-chi pond. It’s lovely in the cherry-blossom and autumn-leaf seasons.\n\nRecommended visit time: 11:20–12:10"),
         gmaps=[gm("龍安寺", "Ryoan-ji", 35.03346, 135.71809, "龍安寺 石庭")],
         links=[link("official", "龍安寺 公式サイト", "Ryoan-ji (official)", "http://www.ryoanji.jp/smph/")],
         info=info([row("hours", "3月1日〜11月30日 8:00〜17:00、12月1日〜2月末 8:30〜16:30", "1 Mar – 30 Nov 8:00–17:00; 1 Dec – end of Feb 8:30–16:30"),
                    row("fee", "大人600円、高校生500円、小・中学生300円", "Adults ¥600, high school ¥500, elementary and junior high ¥300")])),
    dict(id="ninnaji", name=T("仁和寺", "Ninna-ji Temple"), kind=T("お寺", "Temple"),
         blurb=T("五重塔と、背の低い遅咲きの「御室桜（おむろざくら）」。京都の桜の最後をかざるお寺です。",
                 "A five-storey pagoda and the low, late-blooming Omuro cherries, the last great cherry show in Kyoto."),
         lat=35.02981, lng=135.71415,
         text=T("仁和寺（にんなじ）\n\n龍安寺から歩いて約15分。大きな二王門をくぐると、広い境内の奥に五重塔が建っています。\n\n"
                "中門の内側の御室桜は、背が低く、花が目の高さで咲く遅咲きの桜。京都の桜の中では遅めの、4月中ごろが見ごろです（写真は2025年4月17日）。"
                "桜の時期（御室花まつり）は特別入山料がかかります。\n\n"
                "次の平野神社へは、目の前の嵐電「御室仁和寺」駅から北野白梅町まで5分（250円）、そこから北へ歩いて約7分です。\n\nおすすめ訪問時間：12:30〜13:40",
                "Ninna-ji Temple\n\nAbout 15 minutes’ walk from Ryoan-ji. Pass through the huge Niomon gate, and the five-storey pagoda stands at the back of the wide grounds.\n\n"
                "Inside the middle gate, the Omuro cherries are short trees whose blossoms bloom at eye level, and late: they peak around mid-April, later than most in Kyoto (photos: 17 Apr 2025). "
                "In cherry season (the Omuro Flower Festival) there’s a special entry fee.\n\n"
                "For Hirano Shrine, take the Randen tram from Omuro-Ninnaji station, right in front, to Kitano-Hakubaicho (5 min, ¥250), then walk about 7 min north.\n\nRecommended visit time: 12:30–13:40"),
         gmaps=[gm("仁和寺", "Ninna-ji", 35.02981, 135.71415, "仁和寺"),
                gm("嵐電 御室仁和寺駅", "Randen Omuro-Ninnaji Station", 35.02645, 135.71396, "嵐電 御室仁和寺駅")],
         links=[link("official", "仁和寺 公式サイト（拝観・交通案内）", "Ninna-ji (official, Japanese)", "https://ninnaji.jp/visit/")],
         info=info([row("fee", "御所庭園 大人800円、霊宝館（期間限定）大人500円、御室花まつりの特別入山料 大人800円（高校生以下は無料）",
                        "Palace garden ¥800, treasure hall (limited periods) ¥500, Omuro Flower Festival special entry ¥800 per adult (high school and under free)"),
                    row("train", "嵐電 御室仁和寺→北野白梅町 約5分・250円", "Randen tram Omuro-Ninnaji → Kitano-Hakubaicho, about 5 min, ¥250")],
                   tip=T("拝観料は仁和寺の公式サイト、嵐電の運賃は乗換案内で確認しました。", "Fees checked on Ninna-ji’s website; tram fare on a route planner."))),
    dict(id="hirano", name=T("平野神社", "Hirano Shrine"), kind=T("神社", "Shrine"),
         blurb=T("約60種・400本の桜が咲く、京都の夜桜の名所。春はぜひ夕暮れに。",
                 "About 400 cherry trees of some 60 kinds: a classic spot for cherry blossoms at night. Come at dusk in spring."),
         lat=35.03238, lng=135.73248,
         text=T("平野神社（ひらのじんじゃ）\n\n嵐電の北野白梅町駅から北へ歩いて約7分。平安時代から桜が植えられてきた神社で、今は約60種・400本の桜があります。江戸時代から「平野の夜桜」として知られる花見の名所です。\n\n"
                "3月中ごろの早咲きの桜から4月下旬の八重桜まで、長い期間いろいろな桜が楽しめます。写真は2025年4月5日の夕方〜夜。桜の時期は境内の桜苑が有料になることがあります（料金・時間は要確認）。\n\n"
                "北野天満宮は、ここから南東へ歩いてすぐです。\n\nおすすめ訪問時間：14:00〜14:30（春は夕方も）",
                "Hirano Shrine\n\nAbout 7 minutes’ walk north of Randen’s Kitano-Hakubaicho station. Cherry trees have been planted here since the Heian period; today there are about 400 trees of some 60 kinds, and “Hirano’s night cherries” have been famous since the Edo period.\n\n"
                "From early blossoms in mid-March to double-flowered ones in late April, there’s something in bloom for a long season. The photos were taken at dusk on 5 Apr 2025. In cherry season the shrine’s cherry garden may charge for entry (check fees and hours).\n\n"
                "Kitano Tenmangu is just a short walk to the southeast.\n\nRecommended visit time: 14:00–14:30 (or at dusk in spring)"),
         gmaps=[gm("平野神社", "Hirano Shrine", 35.03238, 135.73248, "平野神社 京都市北区")],
         links=[link("official", "平野神社 公式サイト（平野神社の桜）", "Hirano Shrine (official)", "https://www.hiranojinja.com/home/cherry")],
         info=NONE),
    dict(id="kitano", name=T("北野天満宮", "Kitano Tenmangu Shrine"), kind=T("神社", "Shrine"),
         blurb=T("学問の神さま・菅原道真をまつる「天神さん」。秋はもみじ苑の夜のライトアップも。",
                 "“Tenjin-san”, the shrine of Sugawara no Michizane, god of learning. Autumn brings evening light-ups in the maple garden."),
         lat=35.03048, lng=135.73492,
         text=T("北野天満宮（きたのてんまんぐう）\n\n学問の神さまとして知られる菅原道真（すがわらのみちざね）をまつる神社で、京都の人には「天神さん」と呼ばれています。受験の合格をお願いする人も多く、境内には道真が好んだ梅の木がたくさんあります。\n\n"
                "境内の西側の「もみじ苑」は、秋だけ公開される紅葉の名所。紙屋川（かみやがわ）に架かる朱色の橋と紅葉の景色がみごとで、夜のライトアップもあります。春には梅苑が公開されます（どちらも有料）。\n\n"
                "帰りは「北野天満宮前」から市バスで京都駅や四条方面へ（230円）。\n\nおすすめ訪問時間：14:40〜15:40（秋はライトアップの時間も）",
                "Kitano Tenmangu Shrine\n\nThe shrine of Sugawara no Michizane, revered as the god of learning, known locally as “Tenjin-san”. Many come to pray for exam success, and the grounds are full of the plum trees Michizane loved.\n\n"
                "On the west side, the Momiji-en maple garden opens only in autumn: the vermilion bridge over the Kamiya river framed by red leaves is superb, and there are evening light-ups. In spring the plum garden opens (both charge entry).\n\n"
                "To go back, take a city bus from “Kitano Tenmangu-mae” toward Kyoto Station or Shijo (¥230).\n\nRecommended visit time: 14:40–15:40 (plus the light-up hours in autumn)"),
         gmaps=[gm("北野天満宮", "Kitano Tenmangu", 35.03048, 135.73492, "北野天満宮")],
         links=[link("official", "北野天満宮 公式サイト", "Kitano Tenmangu (official, Japanese)", "https://kitanotenmangu.or.jp/")],
         info=info([row("hours", "開門 7:00〜20:00", "Gates open 7:00–20:00"),
                    row("hours", "もみじ苑（2026年10月31日〜12月6日）9:00〜16:00。ライトアップ期間（11月13日〜12月6日）は20:00まで（受付は20分前まで）",
                        "Maple garden (31 Oct – 6 Dec 2026) 9:00–16:00; until 20:00 during the light-up (13 Nov – 6 Dec). Last entry 20 min before", until="2026-12-06"),
                    row("fee", "もみじ苑 大人（中学生以上）1,500円、小学生700円", "Maple garden: ¥1,500 (junior high and up), ¥700 (elementary)", until="2026-12-06"),
                    row("fee", "もみじ苑（秋）と梅苑（春）は有料です。公開の時期と料金は公式サイトで発表されます",
                        "The maple garden (autumn) and plum garden (spring) charge entry; dates and fees are announced on the website")])),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    out.setdefault("notices", [])
    spots.append(out)

data = {
    "id": "kinkakuji",
    "_note": "京都・金閣寺〜北野天満宮の1日ルート（kinkakuji/ のページ専用。形は eizan-line.json と同じ）。大徳寺から金閣寺、きぬかけの路を歩いて龍安寺・仁和寺へ、嵐電で北野白梅町に出て平野神社・北野天満宮へ。"
             "写真は Toshi の写真ライブラリから選んだもの（2024〜2026年の写真を場所ごとに全部見て、1か所10枚以内・Nikon D7000 を含む・横の写真だけ。長辺1600px・位置情報なし）。"
             "金閣寺の雪の写真は2026年2月8日、仁和寺の御室桜は2025年4月17日、平野神社の夜桜は2025年4月5日、北野天満宮の紅葉のライトアップは2024年12月と2025年11月。"
             "info.checked は事実情報を確認した日（各寺社の公式サイト。嵐電の運賃は乗換案内）。大徳寺の塔頭と平野神社の桜苑の料金は公式サイトで確認できなかったので書いていない（文章で要確認と書いた）。"
             "このファイルは scripts/build_kinkakuji_data.py で作る。",
    "sections": [
        {"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 2, "day": 1}, {"first": 3, "last": 4, "day": 2}, {"first": 5, "last": 6, "day": 3},
    ],
    "plan": {"_note": "「選んで回る」の設定。どの場所も自分で選べる。", "picks": list(range(1, len(spots) + 1)), "auto": {}, "hints": []},
    "photoBase": "../images/kinkakuji/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
