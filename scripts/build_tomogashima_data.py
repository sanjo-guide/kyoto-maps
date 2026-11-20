#!/usr/bin/env python3
"""京都から日帰り 友ヶ島・加太ルートのデータ（data/routes/tomogashima.json）を書き出す。

使い方: python3 scripts/build_tomogashima_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/tomogashima/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/tomogashima"
OUT = f"{R}/data/routes/tomogashima.json"
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
KISEN = link("official", "友ヶ島汽船 公式サイト（運航連絡・時刻・運賃）", "Tomogashima Kisen ferry (official, Japanese)", "https://tomogashimakisen.com/main/")
JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の平日のダイヤ）で確認しました。乗る前にもう一度確かめてください。",
              "Times and fares checked on a route planner (weekday timetable, November 2026). Please check again before you travel.")

S = [
    dict(id="kadaeki", name=T("南海 加太駅", "Nankai Kada Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("和歌山市駅から加太線で終点の加太へ。鯛の形の吊り革がかわいい「めでたいでんしゃ」に会えるかも。",
                 "Ride the Kada Line from Wakayamashi to the end of the line. You may catch the “Medetai Densha”, with sea-bream-shaped straps."),
         lat=34.27507, lng=135.08070,
         text=T("南海 加太駅（かだえき）\n\n京都からは、JRの新快速で大阪へ、地下鉄御堂筋線でなんばへ出て、南海線で和歌山市駅、そこから加太線で終点の加太へ。"
                "京都7:35発に乗ると、加太に10:19に着きます（約2時間45分・1,830円）。\n\n"
                "加太線には、鯛をモチーフにした「めでたいでんしゃ」が走っています。赤やピンクの車両で、車内の吊り革も鯛の形。どの車両が来るかは日によって違います。\n\n"
                "駅から加太港の友ヶ島汽船乗り場までは、歩いて15分ほどです。\n\nおすすめ到着時間：10:19",
                "Nankai Kada Station\n\nFrom Kyoto, take a JR Special Rapid to Osaka, the Midosuji subway to Namba, the Nankai Line to Wakayamashi, then the Kada Line to the end. "
                "Leave Kyoto at 7:35 and you reach Kada at 10:19 (about 2 h 45 min, ¥1,830).\n\n"
                "The Kada Line runs the “Medetai Densha”, trains themed on the lucky sea bream, in red or pink with fish-shaped hand straps. Which one you get varies by day.\n\n"
                "The Tomogashima ferry pier at Kada Port is about 15 minutes’ walk from the station.\n\nRecommended arrival: 10:19"),
         gmaps=[gm("南海 加太駅", "Nankai Kada Station", 34.27507, 135.08070, "南海 加太駅")],
         links=[JR],
         info=info([row("train", "京都7:35発（JR新快速）→ 大阪 → 地下鉄御堂筋線 → なんば → 南海線 → 和歌山市 → 加太線 → 加太10:19着",
                        "Kyoto 7:35 (JR Special Rapid) → Osaka → Midosuji subway → Namba → Nankai Line → Wakayamashi → Kada Line → Kada 10:19"),
                    row("fee", "京都→加太 1,830円（南海の特急サザンは自由席なら追加料金なし）", "Kyoto → Kada ¥1,830 (no extra charge in the unreserved cars of Nankai’s Southern express)")],
                   tip=TRAIN_TIP)),
    dict(id="port", name=T("加太港（友ヶ島汽船乗り場）", "Kada Port (Tomogashima ferry)"), kind=T("船乗り場", "Ferry pier"),
         blurb=T("友ヶ島へ渡る船は、ここから1日に数便だけ。2便目からは当日の整理券を配ります。",
                 "Only a few boats a day leave here for Tomogashima. From the second boat on, same-day numbered tickets are handed out."),
         lat=34.27549, lng=135.07041,
         text=T("加太港（かだこう）の友ヶ島汽船乗り場\n\n漁港の町・加太の港から、友ヶ島汽船の船で沖ノ島（友ヶ島）の野奈浦（のなうら）桟橋へ渡ります。\n\n"
                "3月〜12月は加太港発 9:00・11:00・13:00・16:00（春の連休と夏休みは臨時便あり）。帰りの友ヶ島発は 9:30・11:30・13:30・16:30 です。"
                "2便目からは当日の乗船整理券が配られ、1便の定員は100人。前日までの予約はできないので、混む日は早めに港へ行きましょう。\n\n"
                "風が強い日や海が荒れた日は欠航になります。行く日の朝に、公式サイトの運航連絡を確かめてください。\n\nおすすめ乗船時間：11:00",
                "Kada Port: Tomogashima Kisen ferry\n\nFrom the fishing port of Kada, the Tomogashima Kisen boat takes you to Nonaura pier on Okinoshima (Tomogashima).\n\n"
                "March to December, boats leave Kada at 9:00, 11:00, 13:00 and 16:00 (extra sailings in Golden Week and the summer holidays). Return boats leave the island at 9:30, 11:30, 13:30 and 16:30. "
                "From the second boat on, same-day numbered tickets are handed out; each boat takes 100 people and there are no advance bookings, so arrive early on busy days.\n\n"
                "Boats are cancelled in strong wind or rough seas. Check the operating notice on the website on the morning you go.\n\nRecommended boat: 11:00"),
         gmaps=[gm("友ヶ島汽船 乗り場", "Tomogashima Kisen pier", 34.27549, 135.07041, "友ヶ島汽船 加太")],
         links=[KISEN],
         info=info([row("hours", "3月〜12月：加太港発 9:00・11:00・13:00・16:00／友ヶ島発 9:30・11:30・13:30・16:30（4月29日〜5月5日と7月20日〜8月31日は臨時便あり）",
                        "Mar–Dec: Kada 9:00, 11:00, 13:00, 16:00 / island 9:30, 11:30, 13:30, 16:30 (extra boats 29 Apr – 5 May and 20 Jul – 31 Aug)"),
                    row("closed", "3月〜12月は水曜運休（祝日は運航）。1月〜2月は土・日・祝日だけ運航（12月29日〜1月3日は運休）。悪天候の日は欠航",
                        "Mar–Dec: no boats on Wednesdays (except holidays). Jan–Feb: Sat, Sun and holidays only (none 29 Dec – 3 Jan). Cancelled in bad weather"),
                    row("fee", "往復 大人2,800円（2026年7月1日から）", "Round trip ¥2,800 per adult (from 1 Jul 2026)")],
                   tip=T("運航日・時刻・運賃は友ヶ島汽船の公式サイトで確認しました。", "Days, times and fares checked on the Tomogashima Kisen website."))),
    dict(id="nonaura", name=T("友ヶ島 野奈浦桟橋", "Nonaura Pier, Tomogashima"), kind=T("船着き場", "Pier"),
         blurb=T("無人島の友ヶ島に到着。山道を歩いて、森の中に残るレンガの砲台跡をめぐります。",
                 "Landing on uninhabited Tomogashima. Walk the hill trails to brick gun batteries hidden in the woods."),
         lat=34.28380, lng=135.00860,
         text=T("友ヶ島 野奈浦桟橋（のなうらさんばし）\n\n加太港から船で20分ほど。友ヶ島は紀淡海峡に浮かぶ無人島の集まりで、船が着くのはいちばん大きな沖ノ島です。"
                "明治時代に大阪湾を守る要塞が造られ、レンガ造りの砲台跡が森の中に残っています。\n\n"
                "島の中は舗装されていない山道が多いので、歩きやすい靴で。桟橋の近くに友ヶ島案内センターがありますが、飲み物は多めに持っていくと安心です。"
                "砲台跡を回って戻ってくるまで、2時間半〜3時間ほどみておきましょう。\n\n帰りは16:30発の船で加太港へ（13:30発でも主な場所は回れますが、急ぎ足になります）。\n\nおすすめ到着時間：11:20",
                "Nonaura Pier, Tomogashima\n\nAbout 20 minutes by boat from Kada. Tomogashima is a group of uninhabited islands in the Kitan Strait; boats land on the largest, Okinoshima. "
                "In the Meiji era it was fortified to guard Osaka Bay, and brick gun batteries still stand in the woods.\n\n"
                "Most trails are unpaved hill paths, so wear good shoes. There is an information centre near the pier, but bring plenty to drink. "
                "Allow two and a half to three hours to walk round the batteries and back.\n\nTake the 16:30 boat back to Kada (the 13:30 also works for the main sights, but it’s a rush).\n\nRecommended arrival: 11:20"),
         gmaps=[gm("野奈浦桟橋", "Nonaura Pier", 34.28380, 135.00860, "友ヶ島 野奈浦桟橋")],
         links=[KISEN],
         info=NONE),
    dict(id="dai3", name=T("第3砲台跡", "No. 3 Battery ruins"), kind=T("砲台跡", "Fort ruins"),
         blurb=T("レンガのアーチが並ぶ、友ヶ島でいちばん有名な場所。暗いトンネルの先に、緑に包まれた砲台跡が現れます。",
                 "Tomogashima’s most famous sight: rows of brick arches, and beyond a dark tunnel, battery ruins wrapped in green."),
         lat=34.28005, lng=135.00666,
         text=T("第3砲台跡（だいさんほうだいあと）\n\n野奈浦桟橋から山道を登って約0.5km。レンガ造りの弾薬庫のアーチが並び、苔とつたに覆われた景色は、まるでアニメ映画の世界のようだと人気です。\n\n"
                "長いレンガのトンネルの中は真っ暗な所もあるので、スマホのライトがあると安心です。建物の上や崩れかけた所には登らないでください。\n\nおすすめ訪問時間：11:40〜12:20",
                "No. 3 Battery ruins\n\nAbout 0.5 km up the hill from Nonaura pier. Rows of brick magazine arches covered in moss and ivy make it look like a scene from an animated film, which is why it’s so popular.\n\n"
                "Parts of the long brick tunnel are pitch dark, so a phone torch helps. Don’t climb on the structures or crumbling sections.\n\nRecommended visit time: 11:40–12:20"),
         gmaps=[gm("友ヶ島 第3砲台跡", "No. 3 Battery, Tomogashima", 34.28005, 135.00666, "友ヶ島 第3砲台跡")],
         links=[KISEN],
         info=NONE),
    dict(id="takanosu", name=T("タカノス山展望台", "Takanosu-yama Observatory"), kind=T("展望台", "Viewpoint"),
         blurb=T("島のいちばん高い所にある展望台。淡路島と紀淡海峡が見渡せます。",
                 "The lookout at the island’s highest point, with views over Awaji Island and the Kitan Strait."),
         lat=34.28133, lng=135.00597,
         text=T("タカノス山展望台（たかのすやまてんぼうだい）\n\n第3砲台跡のすぐ近く、島の山の上にある展望台です。白い屋根の休憩所があり、海の向こうに淡路島が大きく見えます。\n\n"
                "道しるべでは「大展望台」と書かれています。ひと休みしてから、島の西側の海岸へ下りていきましょう。\n\nおすすめ訪問時間：12:30〜12:50",
                "Takanosu-yama Observatory\n\nA lookout on the hilltop right by the No. 3 Battery. There’s a shelter with white roofs, and Awaji Island looms across the sea.\n\n"
                "Signposts call it the “Dai-tenbodai” (big observatory). Rest here, then head down to the west coast of the island.\n\nRecommended visit time: 12:30–12:50"),
         gmaps=[gm("タカノス山展望台", "Takanosu-yama Observatory", 34.28133, 135.00597, "タカノス山展望台 友ヶ島")],
         links=[KISEN],
         info=NONE),
    dict(id="kosuke", name=T("孝助松海岸", "Kosukematsu beach"), kind=T("海岸", "Beach"),
         blurb=T("とがった岩が海に突き出す、島の北側の海岸。波の音だけが聞こえる静かな場所です。",
                 "A quiet beach on the north shore where a pointed rock juts into the sea and all you hear are the waves."),
         lat=34.28330, lng=135.00240,
         text=T("孝助松海岸（こうすけまつかいがん）\n\n展望台から下って、池尻広場の先にある海岸です。海にとがった岩が突き出し、晴れた日は海の色がとてもきれいです。\n\n"
                "ここから友ヶ島灯台と第2砲台跡までは、道しるべに沿って歩いて10分ほどです。\n\nおすすめ訪問時間：13:10〜13:25",
                "Kosukematsu beach\n\nDown from the lookout, just past Ikejiri Square. A pointed rock juts into the sea, and on sunny days the water is beautiful.\n\n"
                "From here it’s about 10 minutes along the signposted trail to the lighthouse and the No. 2 Battery.\n\nRecommended visit time: 13:10–13:25"),
         gmaps=[gm("孝助松海岸", "Kosukematsu beach", 34.28330, 135.00240, "友ヶ島 孝助松海岸")],
         links=[KISEN],
         info=NONE),
    dict(id="toudai", name=T("友ヶ島灯台", "Tomogashima Lighthouse"), kind=T("灯台", "Lighthouse"),
         blurb=T("明治時代に建てられた白い灯台。足元には岩場の海が広がります。",
                 "A white lighthouse from the Meiji era, above a rocky shore."),
         lat=34.28091, lng=135.00046,
         text=T("友ヶ島灯台（ともがしまとうだい）\n\n島の西の端に立つ白い灯台で、明治時代に建てられた古い灯台のひとつです。灯台のまわりは芝生の広場になっていて、岩場の海を見下ろせます。\n\n"
                "すぐ近くに第2砲台跡があります。\n\nおすすめ訪問時間：13:35〜13:55",
                "Tomogashima Lighthouse\n\nA white lighthouse at the western tip of the island, one of Japan’s early Meiji-era lighthouses. A grassy area surrounds it, looking down on the rocky shore.\n\n"
                "The No. 2 Battery is close by.\n\nRecommended visit time: 13:35–13:55"),
         gmaps=[gm("友ヶ島灯台", "Tomogashima Lighthouse", 34.28091, 135.00046, "友ヶ島灯台")],
         links=[KISEN],
         info=NONE),
    dict(id="dai2", name=T("第2砲台跡", "No. 2 Battery ruins"), kind=T("砲台跡", "Fort ruins"),
         blurb=T("海に面して崩れたままのレンガの砲台跡。崩れた壁の向こうに淡路島が見えます。",
                 "A brick battery on the sea, left as it collapsed. Awaji Island shows through the broken walls."),
         lat=34.28213, lng=135.00055,
         text=T("第2砲台跡（だいにほうだいあと）\n\n灯台のすぐ近く、海に面した砲台跡です。大きなコンクリートの塊が崩れ落ちたまま残っていて、第3砲台跡とはまた違う迫力があります。\n\n"
                "崩れていて危ないので、柵の中には入らないでください。ここから野奈浦桟橋までは、歩いて20〜30分ほどです。\n\nおすすめ訪問時間：14:00〜14:30",
                "No. 2 Battery ruins\n\nRight by the lighthouse, facing the sea. Huge blocks of concrete lie where they fell, with a different kind of drama from the No. 3 Battery.\n\n"
                "It’s unstable, so stay outside the fences. Nonaura pier is 20 to 30 minutes’ walk from here.\n\nRecommended visit time: 14:00–14:30"),
         gmaps=[gm("友ヶ島 第2砲台跡", "No. 2 Battery, Tomogashima", 34.28213, 135.00055, "友ヶ島 第2砲台跡")],
         links=[KISEN],
         info=NONE),
    dict(id="awashima", name=T("淡嶋神社", "Awashima Shrine"), kind=T("神社", "Shrine"),
         blurb=T("人形供養で知られる神社。加太港から歩いてすぐです。",
                 "A shrine known for its memorial services for dolls, a short walk from Kada Port."),
         lat=34.27360, lng=135.06671,
         text=T("淡嶋神社（あわしまじんじゃ）\n\n加太港のすぐ近く、海に向かって朱色の鳥居が立つ神社です。人形供養で知られ、境内には全国から納められたたくさんの人形が並んでいます。"
                "毎年3月3日には、ひな人形を小舟にのせて海へ流す「雛流し」が行われます。\n\n"
                "友ヶ島から16:30の船で戻ったら、ここにお参りしてから駅へ向かいましょう。\n\nおすすめ訪問時間：16:55〜17:10",
                "Awashima Shrine\n\nRight by Kada Port, with a vermilion torii facing the sea. It’s known for memorial services for dolls, and countless dolls sent from all over Japan line the grounds. "
                "Every 3 March, in the “Hina-nagashi”, Girls’ Day dolls are set adrift on the sea in little boats.\n\n"
                "Back from the island on the 16:30 boat, pay a visit here on your way to the station.\n\nRecommended visit time: 16:55–17:10"),
         gmaps=[gm("淡嶋神社", "Awashima Shrine", 34.27360, 135.06671, "淡嶋神社 和歌山市加太")],
         links=[],
         info=NONE),
    dict(id="kadaeki2", name=T("南海 加太駅（帰り）", "Nankai Kada Station (return)"), kind=T("駅（ゴール）", "Station (finish)"),
         blurb=T("17:27発の電車で京都へ。19:59着です。",
                 "Take the 17:27 train back, arriving in Kyoto at 19:59."),
         lat=34.27507, lng=135.08070,
         text=T("南海 加太駅（帰り）\n\n17:27発の加太線で和歌山市へ、南海線でなんば、地下鉄御堂筋線で梅田（大阪）、JRの新快速で京都へ。京都には19:59に着きます（1,830円）。\n\n"
                "淡嶋神社から駅までは歩いて20分ほどです。\n\nおすすめ出発時間：17:27",
                "Nankai Kada Station (return)\n\nTake the 17:27 Kada Line to Wakayamashi, the Nankai Line to Namba, the Midosuji subway to Umeda (Osaka) and a JR Special Rapid to Kyoto, arriving at 19:59 (¥1,830).\n\n"
                "The station is about 20 minutes’ walk from Awashima Shrine.\n\nRecommended departure time: 17:27"),
         gmaps=[gm("南海 加太駅", "Nankai Kada Station", 34.27507, 135.08070, "南海 加太駅")],
         links=[JR],
         info=info([row("train", "加太17:27発 → 和歌山市 → なんば → 梅田（大阪）→ 京都19:59着", "Kada 17:27 → Wakayamashi → Namba → Umeda (Osaka) → Kyoto 19:59"),
                    row("fee", "加太→京都 1,830円", "Kada → Kyoto ¥1,830")],
                   tip=TRAIN_TIP)),
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
ISLAND = [NO[k] for k in ("dai3", "takanosu", "kosuke", "toudai", "dai2")]
data = {
    "id": "tomogashima",
    "_note": "京都から日帰り 友ヶ島・加太のルート（tomogashima/ のページ専用。形は eizan-line.json と同じ）。京都からJR・地下鉄・南海で加太へ、加太港から友ヶ島汽船で沖ノ島の野奈浦桟橋へ渡り、"
             "第3砲台跡・タカノス山展望台・孝助松海岸・友ヶ島灯台・第2砲台跡を歩いて回り、16:30の船で戻って淡嶋神社にお参りしてから京都へ。"
             "写真は Toshi の写真ライブラリから選んだもの（加太は2022年7月8日、友ヶ島と淡嶋神社は2023年6月20日。Nikon D7000 の写真は島にGPSの写真が2枚しかないので、道しるべの看板と撮影時刻の順で場所を決めた。"
             "1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。info.checked は事実情報を確認した日（船は友ヶ島汽船の公式サイト、電車は乗換案内）。"
             "このファイルは scripts/build_tomogashima_data.py で作る。",
    "sections": [
        {"first": 1, "last": 2, "day": 0}, {"first": 3, "last": 5, "day": 1}, {"first": 6, "last": 8, "day": 2}, {"first": 9, "last": 10, "day": 3},
    ],
    "focus": {"first": NO["nonaura"], "last": NO["dai2"]},
    "plan": {"_note": "「選んで回る」の設定。駅・港・桟橋はいつも入る。島の中と淡嶋神社は選べる。",
             "picks": ISLAND + [NO["awashima"]],
             "auto": {str(NO[k]): {"always": True} for k in ("kadaeki", "port", "nonaura", "kadaeki2")},
             "hints": []},
    "photoBase": "../images/tomogashima/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
