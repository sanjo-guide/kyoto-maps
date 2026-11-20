#!/usr/bin/env python3
"""京都から日帰り 姫路・明石・須磨のデータ（data/routes/himeji.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/himeji/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/himeji"
OUT = f"{R}/data/routes/himeji.json"
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
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。乗る前にもう一度確かめてください。",
              "Times and fares checked on a route planner (Saturday timetable, November 2026). Please check again before you travel.")

S = [
    dict(id="himejieki", name=T("JR姫路駅", "JR Himeji Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都から新快速で1時間36分、乗り換えなし。駅の北口を出ると、大通りの先に白い天守が見えます。",
                 "1 h 36 min from Kyoto by Special Rapid, no change. Out of the north exit, the white keep stands at the end of the main street."),
         lat=34.82800, lng=134.69006,
         text=T("JR姫路駅（ひめじえき）\n\n京都からJRの新快速で乗り換えなし。京都8:14発に乗ると、姫路に9:50に着きます（2,210円）。急ぐなら新幹線で約50分（自由席4,740円）。\n\n"
                "北口を出ると、まっすぐ延びる大手前通りの先に姫路城が見えます。お城の入口までは歩いて約20分。神姫バスで「大手門前」まで行き、歩いて5分という行き方もあります。\n\nおすすめ到着時間：9:50",
                "JR Himeji Station\n\nDirect from Kyoto on the JR Special Rapid: leave at 8:14 and arrive at 9:50 (¥2,210). In a hurry, the Shinkansen takes about 50 minutes (¥4,740 unreserved).\n\n"
                "From the north exit, the castle stands at the end of the straight Otemae-dori. It’s about 20 minutes on foot to the entrance, or take a Shinki bus to “Otemon-mae” and walk 5 minutes.\n\nRecommended arrival: 9:50"),
         gmaps=[gm("JR姫路駅", "JR Himeji Station", 34.82800, 134.69006, "JR姫路駅")],
         links=[JR],
         info=info([row("train", "京都8:14発（JR新快速）→ 姫路9:50着（乗り換えなし）", "Kyoto 8:14 (JR Special Rapid) → Himeji 9:50 (direct)"),
                    row("fee", "京都→姫路 2,210円（新幹線の自由席なら4,740円）", "Kyoto → Himeji ¥2,210 (¥4,740 by Shinkansen, unreserved)")],
                   tip=TRAIN_TIP)),
    dict(id="himejijo", name=T("姫路城", "Himeji Castle"), kind=T("城（世界遺産）", "Castle (World Heritage)"),
         blurb=T("白鷺城とも呼ばれる、真っ白な天守。木造の大天守の中を、急な階段で最上階まで上ります。",
                 "The brilliant white keep, nicknamed the White Heron. Climb steep wooden stairs inside the great keep to the top floor."),
         lat=34.83933, lng=134.69402,
         text=T("姫路城（ひめじじょう）\n\n江戸時代のはじめに建てられた天守が今も残る、世界遺産のお城です。白い漆喰の壁から「白鷺城（しらさぎじょう）」とも呼ばれます。"
                "菱の門から曲がりくねった坂と門をいくつも抜けて、大天守へ。中は木の柱と床がそのまま残り、急な階段で6階の最上階まで上れます。最上階の窓からは、姫路の町がまっすぐ駅まで見通せます。\n\n"
                "建物の中は靴を脱いで上がります（靴を入れる袋をもらえます）。西の丸の長い廊下「百間廊下」も見ておきたい所です。\n\n"
                "入城料は、2026年3月から姫路市外の大人が2,500円になりました。お城と好古園の共通券（2,600円）もあります。\n\nおすすめ訪問時間：10:10〜12:20",
                "Himeji Castle\n\nA World Heritage castle whose early-Edo keep still stands. Its white plaster walls earned it the name “White Heron Castle”. "
                "From the Hishi gate, wind up through slopes and gates to the great keep. Inside, the original wooden pillars and floors remain, and steep stairs lead to the sixth, top floor, with a view straight down the city to the station.\n\n"
                "Shoes come off inside (you’re given a bag for them). Don’t miss the long corridor of the West Bailey, the Hyakken Roka.\n\n"
                "Since March 2026, admission for adults who don’t live in Himeji is ¥2,500. A combined ticket with Kokoen garden is ¥2,600.\n\nRecommended visit time: 10:10–12:20"),
         gmaps=[gm("姫路城", "Himeji Castle", 34.83933, 134.69402, "姫路城")],
         links=[link("official", "姫路城 公式サイト", "Himeji Castle (official)", "https://www.himejicastle.jp/")],
         info=info([row("hours", "9:00〜17:00（入城は16:00まで）", "9:00–17:00 (last entry 16:00)"),
                    row("closed", "12月29日・30日", "29–30 December"),
                    row("fee", "18歳以上 2,500円（姫路市民は1,000円）、18歳未満は無料。好古園との共通券 2,600円", "Ages 18+ ¥2,500 (¥1,000 for Himeji residents); under 18 free. Combined ticket with Kokoen ¥2,600")],
                   tip=T("時間と料金は姫路城の公式サイトで確認しました。", "Hours and fees checked on the official Himeji Castle website."))),
    dict(id="kokoen", name=T("好古園", "Kokoen Garden"), kind=T("日本庭園", "Japanese garden"),
         blurb=T("お城の西の、9つの庭がつながる日本庭園。池の向こうに、天守が顔をのぞかせます。",
                 "Nine linked gardens just west of the castle, with the keep peeking over the pond."),
         lat=34.83797, lng=134.68961,
         text=T("好古園（こうこえん）\n\n姫路城の西の御屋敷跡に造られた、9つの庭からなる日本庭園です。池泉回遊式の「御屋敷の庭」では、池の向こうに天守が見えます。入口はお城の有料区域とは別です。\n\n"
                "写真は2024年9月の夜に撮ったもの。2026年秋は11月17日〜12月6日に夜間開園があり、20:00まで紅葉のライトアップが楽しめます。\n\n"
                "見終わったら駅へ戻り、新快速で明石へ（姫路12:57発→明石13:20着・660円）。\n\nおすすめ訪問時間：12:25〜12:45",
                "Kokoen Garden\n\nNine gardens laid out on the site of the lords’ residences west of Himeji Castle. In the pond garden of the main residence, the keep rises beyond the water. The entrance is separate from the castle’s paid area.\n\n"
                "The photos were taken on an evening in September 2024. In autumn 2026 the garden opens in the evening from 17 November to 6 December, with the autumn leaves lit up until 20:00.\n\n"
                "Then head back to the station and take the Special Rapid to Akashi (Himeji 12:57 → Akashi 13:20, ¥660).\n\nRecommended visit time: 12:25–12:45"),
         gmaps=[gm("好古園", "Kokoen", 34.83797, 134.68961, "好古園 姫路")],
         links=[link("official", "好古園 公式サイト", "Kokoen (official, Japanese)", "https://himeji-machishin.jp/ryokka/kokoen/")],
         info=info([row("hours", "9:00〜17:00（入園は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                    row("hours", "2026年秋の夜間開園：11月17日〜12月6日、20:00まで（入園19:30まで）", "Autumn 2026 evening opening: 17 Nov – 6 Dec, until 20:00 (last entry 19:30)", until="2026-12-06"),
                    row("closed", "12月29日・30日", "29–30 December"),
                    row("fee", "大人400円、18歳未満は無料（姫路城との共通券 2,600円）", "¥400 adults, under 18 free (combined ticket with the castle ¥2,600)"),
                    row("train", "姫路12:57発（新快速）→ 明石13:20着・660円", "Himeji 12:57 (Special Rapid) → Akashi 13:20, ¥660")],
                   tip=T("時間と料金は好古園の公式サイト、電車は乗換案内で確認しました。", "Hours and fees checked on the Kokoen website; trains on a route planner."))),
    dict(id="akashi", name=T("明石 魚の棚と「たこ磯」の明石焼", "Akashi: Uonotana market & Takoiso akashiyaki"), kind=T("市場・ランチ", "Market & lunch"),
         blurb=T("明石駅のすぐ南の、明石だこと魚の商店街。お昼はたこ磯で、だし汁につけて食べる明石焼（玉子焼）を。",
                 "The fish-and-octopus arcade just south of Akashi Station. Lunch is akashiyaki (tamagoyaki) at Takoiso, dipped in dashi."),
         lat=34.64701, lng=134.99213,
         text=T("魚の棚（うおんたな）商店街と、たこ磯（たこいそ）\n\n明石駅から南へ歩いて3分。明石の海でとれた魚やたこ、干物やかまぼこの店が並ぶアーケードの商店街です。お昼ごろからは、その日の昼にとれた魚「昼網」も並びます。\n\n"
                "お昼は、商店街の中ほど、弁天さまの隣にある「たこ磯」へ。白いのれんに赤い字で「玉子焼」。明石では明石焼のことを玉子焼と呼びます。ふわふわの玉子焼を、温かいだし汁につけて食べます。\n\n"
                "木曜日は競りがないので、休む店が多くなります。\n\n食べたら山陽電車の山陽明石駅から須磨浦公園へ（14:40発→14:55着・390円）。\n\nおすすめ訪問時間：13:25〜14:35",
                "Uonotana market and Takoiso\n\nThree minutes’ walk south of Akashi Station: an arcade of shops selling fish and octopus from the Akashi sea, dried fish and fish cakes. From around midday the day’s midday catch, “hiruami”, is on sale too.\n\n"
                "For lunch, go to Takoiso, halfway along next to the little Benten shrine: white curtain, red letters, 玉子焼. In Akashi, akashiyaki is called tamagoyaki. Dip the fluffy dumplings in warm dashi.\n\n"
                "Many shops close on Thursdays, when there is no fish auction.\n\nAfterwards take the Sanyo Railway from Sanyo-Akashi to Sumaura-koen (14:40 → 14:55, ¥390).\n\nRecommended visit time: 13:25–14:35"),
         gmaps=[gm("魚の棚商店街", "Uonotana", 34.64701, 134.99213, "魚の棚商店街 明石"), gm("たこ磯", "Takoiso", 34.64696, 134.99289, "たこ磯 明石 本町")],
         links=[link("official", "魚の棚商店街 公式サイト", "Uonotana shopping street (official, Japanese)", "https://www.uonotana.or.jp/"),
                link("info", "たこ磯（魚の棚商店街のお店のページ）", "Takoiso (shop page on the Uonotana site, Japanese)", "https://www.uonotana.or.jp/shop-057.html")],
         info=info([row("hours", "たこ磯（本店）10:00〜19:00、定休日なし。魚の棚の営業時間は店ごとに違います", "Takoiso (main shop) 10:00–19:00, open daily. Uonotana shop hours vary"),
                    row("closed", "魚の棚は木曜に休む店が多い", "Many Uonotana shops close on Thursdays"),
                    row("train", "山陽明石14:40発 → 須磨浦公園14:55着・390円（途中で1回乗り換え）", "Sanyo-Akashi 14:40 → Sumaura-koen 14:55, ¥390 (one change)")],
                   tip=T("魚の棚商店街の公式サイトで確認しました。たこ磯の値段は資料によって違うので、書いていません。", "Checked on the Uonotana website. Takoiso’s prices differ between sources, so they are not given here."))),
    dict(id="suma", name=T("須磨浦公園（須磨浦山上遊園）", "Sumaura Park (Sumaura Sanjo Yuen)"), kind=T("ロープウェー・展望台", "Ropeway & lookout"),
         blurb=T("ロープウェーと、乗り心地がびっくりなカーレーターで山の上へ。回る喫茶店から、須磨の海と明石海峡大橋が見えます。",
                 "Up by ropeway and the bumpy “Car-rator” to a hilltop. From the revolving café, look over the Suma sea and the Akashi Kaikyo Bridge."),
         lat=34.63784, lng=135.10022,
         text=T("須磨浦公園（すまうらこうえん）と須磨浦山上遊園\n\n山陽電車の須磨浦公園駅を出てすぐ、ロープウェーで鉢伏山へ上ります。窓の外には須磨の海岸と神戸の街。"
                "山上駅からは、ベルトコンベアの上の小さなカゴに乗って進む「カーレーター」で、さらに上の回転展望閣へ。ガタガタ揺れる乗り心地は、ここでしか味わえません。\n\n"
                "回転展望閣の3階の喫茶コスモスは、床がゆっくり回ります（約55分で1回転）。晴れた日は、明石海峡大橋や関西空港まで見えます。\n\n"
                "最終入場は16:30。火曜日が休みです。帰りは須磨浦公園16:26発の山陽電車で舞子公園へ（16:41着・250円）。\n\nおすすめ訪問時間：15:00〜16:25",
                "Sumaura Park and Sumaura Sanjo Yuen\n\nRight outside Sanyo Railway’s Sumaura-koen Station, a ropeway climbs Mt. Hachibuse, with the Suma beach and Kobe below. "
                "From the top station, the “Car-rator”, little baskets riding on a conveyor belt, carries you up to the revolving observatory. Its rattling ride is like nothing else.\n\n"
                "Café Cosmos on the third floor of the observatory slowly revolves (about 55 minutes a turn). On clear days you can see the Akashi Kaikyo Bridge and even Kansai Airport.\n\n"
                "Last entry is 16:30; closed on Tuesdays. Then take the 16:26 Sanyo train to Maiko-koen (arr. 16:41, ¥250).\n\nRecommended visit time: 15:00–16:25"),
         gmaps=[gm("須磨浦公園駅", "Sumaura-koen Station", 34.63784, 135.10022, "須磨浦公園駅"), gm("須磨浦山上遊園", "Sumaura Sanjo Yuen", 34.64190, 135.09421, "須磨浦山上遊園")],
         links=[link("official", "須磨浦山上遊園 公式サイト", "Sumaura Sanjo Yuen (official, Japanese)", "https://www.sumaura-yuen.jp/")],
         notices=[{"from": None, "to": "2027-02-05", "url": "https://www.sumaura-yuen.jp/event/entry-709.html",
                   "text": T("2026年12月2日〜2027年2月5日は土日祝だけの営業です（正月三が日は営業。12/12・13・19・20、1/16・17は休園）。",
                             "From 2 December 2026 to 5 February 2027 it opens on weekends and holidays only (open over New Year; closed 12, 13, 19, 20 Dec and 16, 17 Jan).")}],
         info=info([row("hours", "10:00〜17:00（最終入場16:30）。ロープウェーは毎時0・15・30・45分発", "10:00–17:00 (last entry 16:30). Ropeway every 15 minutes"),
                    row("closed", "火曜日（祝日は営業）", "Tuesdays (open on holidays)"),
                    row("fee", "ロープウェー 往復920円、カーレーター 往復550円、喫茶コスモスの入場200円。回遊券 Bコース1,500円・Aコース（リフトも）2,100円",
                        "Ropeway ¥920 return, Car-rator ¥550 return, Café Cosmos entry ¥200. Round tickets: B course ¥1,500, A course (with chairlift) ¥2,100"),
                    row("train", "須磨浦公園16:26発（山陽電車）→ 舞子公園16:41着・250円", "Sumaura-koen 16:26 (Sanyo) → Maiko-koen 16:41, ¥250")],
                   tip=T("時間と料金は須磨浦山上遊園の公式サイトで確認しました。", "Hours and fees checked on the official website."))),
    dict(id="maiko", name=T("舞子公園・明石海峡大橋", "Maiko Park & Akashi Kaikyo Bridge"), kind=T("公園・夕日", "Park & sunset"),
         blurb=T("世界最大級のつり橋のたもとで、海に沈む夕日を。駅から歩いてすぐです。",
                 "Watch the sun go down by one of the world’s longest suspension bridges, a few minutes from the station."),
         lat=34.63275, lng=135.03300,
         text=T("舞子公園（まいここうえん）と明石海峡大橋\n\nJR舞子駅・山陽電車の舞子公園駅から南へ歩いて約5分。淡路島へ渡る明石海峡大橋の真下の海辺の公園です。"
                "橋の向こうに淡路島、西の海に夕日が沈んでいく景色は、この旅の締めくくりにぴったり。橋の桁の中に入れる「舞子海上プロムナード」もあります。\n\n"
                "帰りはJR舞子駅から京都へ。17:38発に乗ると、途中で新快速に乗り換えて京都に18:59に着きます（1,640円）。\n\nおすすめ訪問時間：16:45〜17:30",
                "Maiko Park and the Akashi Kaikyo Bridge\n\nAbout 5 minutes south of JR Maiko and Sanyo Maiko-koen stations: a seaside park right under the Akashi Kaikyo Bridge to Awaji Island. "
                "With Awaji beyond the bridge and the sun sinking into the western sea, it’s the perfect end to the day. You can also walk inside the bridge girders on the Maiko Marine Promenade.\n\n"
                "Go home from JR Maiko: the 17:38, changing to the Special Rapid on the way, reaches Kyoto at 18:59 (¥1,640).\n\nRecommended visit time: 16:45–17:30"),
         gmaps=[gm("舞子公園", "Maiko Park", 34.63275, 135.03300, "舞子公園"), gm("JR舞子駅", "JR Maiko Station", 34.63351, 135.03382, "JR舞子駅")],
         links=[link("official", "舞子公園 公式サイト", "Maiko Park (official, Japanese)", "https://hyogo-maikopark.jp/"), JR],
         info=info([row("hours", "舞子海上プロムナード 9:00〜18:00（最終入館は30分前）", "Maiko Marine Promenade 9:00–18:00 (last entry 30 min before)"),
                    row("closed", "プロムナード：10〜3月は第2月曜（祝日なら翌日）、12月29日〜31日", "Promenade: 2nd Monday Oct–Mar (next day if a holiday), 29–31 Dec"),
                    row("fee", "プロムナード 大人 平日250円・土日祝300円（高校生以下は無料）", "Promenade ¥250 weekdays, ¥300 weekends and holidays (free for high school and under)"),
                    row("train", "帰り：舞子17:38発 → 京都18:59着・1,640円（途中で新快速に乗り換え）", "Return: Maiko 17:38 → Kyoto 18:59, ¥1,640 (change to the Special Rapid on the way)")],
                   tip=T("舞子公園の公式サイトと乗換案内で確認しました。", "Checked on the Maiko Park website and a route planner."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
data = {
    "id": "himeji",
    "_note": "京都から日帰り 姫路・明石・須磨のルート（himeji/ のページ専用。形は eizan-line.json と同じ）。京都から新快速で姫路へ、姫路城と好古園→新快速で明石（魚の棚・たこ磯の明石焼）→山陽電車で須磨浦公園（ロープウェー・カーレーター）→舞子公園で明石海峡大橋の夕日→JR舞子駅から京都へ。"
             "写真は Toshi の写真ライブラリから選んだもの（須磨浦公園と明石は2023年6月16日の Nikon D7000、姫路城は2023年6月と2024年8・9月、好古園は2024年9月の夜、舞子は2023年7月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（各施設・商店街の公式サイト、電車は乗換案内）。このファイルは scripts/build_himeji_data.py で作る。",
    "sections": [{"first": 1, "last": 3, "day": 0}, {"first": 4, "last": 4, "day": 1}, {"first": 5, "last": 5, "day": 2}, {"first": 6, "last": 6, "day": 3}],
    "plan": {"_note": "「選んで回る」の設定。姫路駅は姫路城か好古園を選ぶと入る。defaultMode: pick で最初から「選んで回る」。",
             "defaultMode": "pick",
             "picks": [NO[k] for k in ("himejijo", "kokoen", "akashi", "suma", "maiko")],
             "auto": {str(NO["himejieki"]): {"any": [NO["himejijo"], NO["kokoen"]]}},
             "hints": [
                 H("akashi", {"any": [NO["akashi"]], "none": [NO["himejijo"], NO["kokoen"]]},
                   "姫路に寄らない日は、京都から新快速で明石へ直接行けます（乗り換えなし）。", "Skipping Himeji? The Special Rapid from Kyoto stops at Akashi (no change)."),
                 H("suma", {"any": [NO["suma"]], "none": [NO["maiko"]]},
                   "舞子に寄らない日は、須磨浦公園駅から山陽電車・阪急で京都河原町へ（約1時間45分・1,050円）。JR京都駅へは山陽電車と阪急で三宮へ出て新快速に乗り換え（1,510円）。",
                   "Not going to Maiko? From Sumaura-koen take the Sanyo and Hankyu lines to Kyoto-Kawaramachi (about 1 h 45 min, ¥1,050), or go to Sannomiya and change to the JR Special Rapid for Kyoto Station (¥1,510)."),
             ]},
    "photoBase": "../images/himeji/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
