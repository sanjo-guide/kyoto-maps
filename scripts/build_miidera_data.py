#!/usr/bin/env python3
"""大津 三井寺と琵琶湖疏水の夜桜のデータ（data/routes/miidera.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/miidera/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/miidera"
OUT = f"{R}/data/routes/miidera.json"
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




JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
LIGHT = link("official", "三井寺 春のライトアップ2026（公式）", "Miidera spring illumination 2026 (official, Japanese)", "https://miidera1200.jp/2026lightup-spring/")
NIGHT = row("hours", "2026年の春のライトアップ：3月25日〜4月12日 18:00〜21:30（受付21:00まで）。2027年は未発表", "Spring 2026 illumination: 25 Mar – 12 Apr, 18:00–21:30 (last entry 21:00). 2027 dates not yet announced")
SEASON = {"from": None, "to": None, "url": "https://miidera1200.jp/2026lightup-spring/", "head": T("夜桜は3月下旬〜4月中旬だけ", "Night cherries: late March to mid April only"),
          "text": T("三井寺と琵琶湖疏水の桜のライトアップは、春の約3週間だけです（2026年は3月25日〜4月12日）。毎年の日程は三井寺と大津市の発表を確かめてください。",
                    "The Miidera and canal cherry illuminations run for only about three weeks in spring (25 Mar – 12 Apr in 2026). Check each year’s dates with Miidera and Otsu City.")}
S = [
    dict(id="sosui", name=T("琵琶湖疏水の夜桜", "Cherries on the Lake Biwa Canal at night"), kind=T("桜並木（無料）", "Cherry avenue (free)"),
         blurb=T("京阪三井寺駅のすぐそば。明治の琵琶湖疏水の両岸に桜が続き、春の夜は水面に映る光の帯になります。",
                 "Right by Keihan Miidera Station: cherries line both banks of the Meiji-era Lake Biwa Canal, a ribbon of light on the water on spring nights."),
         lat=35.01212, lng=135.85744,
         text=T("琵琶湖疏水（びわこそすい）の夜桜\n\n三条京阪から地下鉄・京阪京津線で、びわ湖浜大津で石山坂本線に乗り換えて三井寺駅へ（約30分・520円）。京都駅からならJR湖西線で大津京、京阪に乗り換えて約26分（440円）。\n\n"
                "駅を出てすぐ、明治時代に琵琶湖の水を京都へ引いた琵琶湖疏水の取り入れ口です。大津閘門から第一トンネルまでの両岸に約100本の桜が並び、春の夜はライトアップされた桜が水面に映ります（観覧は無料）。"
                "第一トンネル（第一隧道）は2025年に国宝、大津閘門は重要文化財になりました。写真は2026年4月2日の夜。\n\nおすすめ訪問時間：18:05〜18:25",
                "Cherries on the Lake Biwa Canal at night\n\nFrom Sanjo Keihan take the subway / Keihan Keishin line, change at Biwako-Hamaotsu to the Ishiyama-Sakamoto line for Miidera Station (about 30 min, ¥520). From Kyoto Station, take the JR Kosei line to Otsukyo and change to Keihan (about 26 min, ¥440).\n\n"
                "Right outside the station is the intake of the Lake Biwa Canal, built in the Meiji era to carry lake water to Kyoto. About 100 cherry trees line both banks from the Otsu lock to the first tunnel, and on spring nights the lit blossoms are reflected in the water (free to view). "
                "The first tunnel became a National Treasure in 2025, and the Otsu lock an Important Cultural Property. Photos from the night of 2 April 2026.\n\nRecommended visit time: 18:05–18:25"),
         gmaps=[gm("琵琶湖疏水 大津閘門", "Lake Biwa Canal, Otsu lock", 35.01212, 135.85744, "琵琶湖疏水 大津閘門"), gm("京阪 三井寺駅", "Keihan Miidera Station", 35.01250, 135.85930, "京阪 三井寺駅")],
         links=[link("official", "桜の琵琶湖疏水（びわ湖大津観光協会）", "Lake Biwa Canal cherries (Otsu tourism, Japanese)", "https://otsu.or.jp/tripideas/otsu-sakura/"), JR],
         notices=[SEASON],
         info=info([row("hours", "2026年のライトアップ：3月25日〜4月12日 18:00〜21:30。観覧無料", "2026 illumination: 25 Mar – 12 Apr, 18:00–21:30. Free"),
                    row("train", "三条京阪17:31発 → びわ湖浜大津で乗り換え → 三井寺18:01着・520円（京都駅からは大津京で乗り換え、440円）", "Sanjo Keihan 17:31 → change at Biwako-Hamaotsu → Miidera 18:01, ¥520 (from Kyoto Station via Otsukyo, ¥440)")],
                   tip=T("大津市・びわ湖大津観光協会の案内と乗換案内（2026年11月の土曜のダイヤ）で確認しました。春はダイヤが変わっていることがあります。", "Checked with Otsu City, the Otsu tourism association and a route planner (Saturday timetable, Nov 2026); spring timetables may differ."))),
    dict(id="daimon", name=T("三井寺 大門（仁王門）", "Miidera Daimon (Nio gate)"), kind=T("門・受付", "Gate & entrance"),
         blurb=T("夜の拝観はここから。照らされた大門のまわりに、しだれ桜とソメイヨシノが咲きます。",
                 "The evening visit starts here: the lit great gate framed by weeping and Somei-Yoshino cherries."),
         lat=35.01345, lng=135.85455,
         text=T("三井寺（みいでら）・園城寺（おんじょうじ）の大門\n\n疏水から歩いて約10分。三井寺は天台寺門宗の総本山で、境内には千本を超える桜があります。春のライトアップの期間は、大門で夜の拝観の受付をします（昼の拝観とは別の料金）。\n\n"
                "昼の拝観は9:00〜16:30（受付16:00まで）、入山料は大人800円（2026年3月から）。\n\nおすすめ訪問時間：18:30〜18:35",
                "Miidera (Onjoji): the Daimon gate\n\nAbout 10 minutes’ walk from the canal. Miidera, head temple of the Tendai Jimon school, has more than a thousand cherry trees. During the spring illumination, the evening entrance is at the Daimon gate (separate fee from the daytime).\n\n"
                "By day it opens 9:00–16:30 (last entry 16:00), ¥800 for adults (from March 2026).\n\nRecommended visit time: 18:30–18:35"),
         gmaps=[gm("三井寺 大門", "Miidera Daimon", 35.01345, 135.85455, "三井寺 大門 仁王門")],
         links=[LIGHT, link("official", "三井寺 拝観案内", "Miidera visiting info (official, Japanese)", "https://miidera1200.jp/information")],
         notices=[SEASON],
         info=info([NIGHT, row("fee", "夜：大人1,500円、小中高生700円（2026年）。昼：入山料 大人800円・中高生500円・小学生300円", "Night: ¥1,500 adults, ¥700 school pupils (2026). Day: ¥800 adults, ¥500 junior/senior high, ¥300 elementary"),
                    row("hours", "昼の拝観 9:00〜16:30（受付16:00まで）、年中無休", "Daytime 9:00–16:30 (last entry 16:00), open daily")],
                   tip=T("三井寺の公式サイトで確認しました。", "Checked on the Miidera website."))),
    dict(id="kondo", name=T("金堂と三井の晩鐘", "Main hall & the Evening Bell of Mii"), kind=T("国宝・桜", "National Treasure & cherries"),
         blurb=T("国宝の金堂のまわりは、照らされた桜の海。近江八景「三井の晩鐘」の鐘楼や、弁慶の引摺り鐘も。",
                 "A sea of lit cherries around the National Treasure main hall, with the belfry of the “Evening Bell of Mii” and Benkei’s dragged bell."),
         lat=35.01339, lng=135.85286,
         text=T("金堂（こんどう）と三井の晩鐘（みいのばんしょう）\n\n大門から参道を進むと、桃山時代に建てられた国宝の金堂。まわりの桜がピンクや紫の光に照らされ、昼とはまったく違う景色です。"
                "金堂の南東の鐘楼は、近江八景のひとつ「三井の晩鐘」。金堂の西の霊鐘堂には、弁慶が比叡山へ引きずり上げたという伝説の「弁慶の引摺り鐘」が置かれています。\n\nおすすめ訪問時間：18:35〜19:05",
                "Main hall & the Evening Bell of Mii\n\nFollow the approach from the Daimon to the National Treasure main hall, built in the Momoyama period. The cherries around it are lit in pink and violet, nothing like the daytime view. "
                "The belfry south-east of the hall holds the “Evening Bell of Mii”, one of the Eight Views of Omi, and west of the hall stands the bell Benkei is said to have dragged up Mt. Hiei.\n\nRecommended visit time: 18:35–19:05"),
         gmaps=[gm("三井寺 金堂", "Miidera main hall", 35.01339, 135.85286, "三井寺 金堂")],
         links=[LIGHT],
         info=info([NIGHT], tip=T("三井寺の公式サイトで確認しました。", "Checked on the Miidera website."))),
    dict(id="sanju", name=T("唐院・三重塔", "Toin & three-storey pagoda"), kind=T("塔", "Pagoda"),
         blurb=T("夜空に黒く立つ三重塔と、そのまわりの桜。", "The three-storey pagoda dark against the night sky, among the cherries."),
         lat=35.01257, lng=135.85221,
         text=T("唐院（とういん）・三重塔\n\n金堂の南西、三井寺を開いた円珍（智証大師）をまつる唐院に、重要文化財の三重塔が建っています。夜は塔のまわりの桜が照らされ、塔の影が夜空に浮かびます。\n\nおすすめ訪問時間：19:05〜19:20",
                "Toin & three-storey pagoda\n\nSouth-west of the main hall, in the Toin precinct dedicated to Enchin, who revived Miidera, stands the three-storey pagoda (Important Cultural Property). At night the cherries around it are lit and the pagoda’s silhouette rises against the sky.\n\nRecommended visit time: 19:05–19:20"),
         gmaps=[gm("三井寺 三重塔", "Miidera pagoda", 35.01257, 135.85221, "三井寺 三重塔")],
         links=[LIGHT],
         info=info([NIGHT], tip=T("三井寺の公式サイトで確認しました。", "Checked on the Miidera website."))),
    dict(id="kannondo", name=T("観音堂と大津の夜景", "Kannon hall & the lights of Otsu"), kind=T("お堂・展望", "Hall & view"),
         blurb=T("境内の南の高台。観音堂のまわりから、大津の町と琵琶湖の夜景が見下ろせます。",
                 "On the high ground at the south of the precinct: from around the Kannon hall, look down on the lights of Otsu and Lake Biwa."),
         lat=35.01038, lng=135.85493,
         text=T("観音堂（かんのんどう）と大津の夜景\n\n三重塔から南東へ歩いて石段を上ると、西国三十三所の第14番札所の観音堂。高台にあり、大津の町と琵琶湖が見下ろせます。写真はライトアップの夜に撮ったもの。\n\n"
                "帰りは三井寺駅まで歩いて15分ほど。三井寺20:11発で三条京阪20:47着（520円）、または京阪膳所でJRに乗り換えて京都20:41着（440円）。もっとゆっくり見るなら、夜の受付は21:00まで、拝観は21:30までです。\n\nおすすめ訪問時間：19:20〜19:50",
                "Kannon hall & the lights of Otsu\n\nWalk south-east from the pagoda and climb the steps to the Kannon hall, No. 14 of the Saigoku 33-temple pilgrimage. From this high ground you look down over Otsu and Lake Biwa. The photos were taken on illumination nights.\n\n"
                "Miidera Station is about 15 minutes’ walk. The 20:11 train reaches Sanjo Keihan at 20:47 (¥520), or change to JR at Keihan-Zeze for Kyoto at 20:41 (¥440). To stay longer: last entry is 21:00 and the grounds close at 21:30.\n\nRecommended visit time: 19:20–19:50"),
         gmaps=[gm("三井寺 観音堂", "Miidera Kannon hall", 35.01038, 135.85493, "三井寺 観音堂")],
         links=[LIGHT, JR],
         info=info([NIGHT, row("train", "帰り：三井寺20:11発 → 三条京阪20:47着・520円／京阪膳所でJRに乗り換え → 京都20:41着・440円", "Return: Miidera 20:11 → Sanjo Keihan 20:47, ¥520 / change to JR at Keihan-Zeze → Kyoto 20:41, ¥440")],
                   tip=T("三井寺の公式サイトと乗換案内で確認しました。", "Checked on the Miidera website and a route planner."))),
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
    "id": "miidera",
    "_note": "大津 三井寺と琵琶湖疏水の夜桜のルート（miidera/ のページ専用。形は eizan-line.json と同じ）。京阪三井寺駅→琵琶湖疏水→大門→金堂・三井の晩鐘→唐院・三重塔→観音堂。春のライトアップの期間だけのルート。"
             "写真は Toshi の写真ライブラリから選んだもの（2025年4月11日と2026年4月2日の夜、Nikon D7000 と iPhone。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし。人の顔が近くに写る写真は使っていない）。"
             "info.checked は事実情報を確認した日（三井寺・大津市・びわ湖大津観光協会の公式サイト、電車は乗換案内）。このファイルは scripts/build_miidera_data.py で作る。",
    "sections": [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 5, "day": 1}],
    "photoBase": "../images/miidera/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
