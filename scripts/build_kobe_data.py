#!/usr/bin/env python3
"""京都から日帰り 神戸（布引の滝・北野異人館・メリケンパーク）のデータ（data/routes/kobe.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/kobe/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kobe"
OUT = f"{R}/data/routes/kobe.json"
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
JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
FEEL = "https://www.feel-kobe.jp/"
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。乗る前にもう一度確かめてください。",
              "Times and fares checked on a route planner (Saturday timetable, November 2026). Please check again before you travel.")

S = [
    dict(id="sannomiya", name=T("三宮（JR三ノ宮駅・阪急神戸三宮駅）", "Sannomiya Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都からJRの新快速で51分。神戸の真ん中の三宮から歩きはじめます。",
                 "51 minutes from Kyoto by JR Special Rapid. Start walking from Sannomiya, the heart of Kobe."),
         lat=34.69486, lng=135.19509,
         text=T("三宮（さんのみや）\n\n京都からJR琵琶湖線・神戸線の新快速で乗り換えなし。京都9:00発に乗ると、三ノ宮に9:51に着きます（1,110円）。"
                "阪急なら、京都河原町から十三で乗り換えて神戸三宮まで約1時間15分（640円）。時間はかかりますが安く行けます。\n\n"
                "三宮から新神戸駅へは、地下鉄西神・山手線で1駅（2分・210円）。歩いても行けます。写真は雨の日の阪急神戸三宮駅です。\n\nおすすめ到着時間：9:51",
                "Sannomiya\n\nNo change needed from Kyoto: the JR Special Rapid leaving Kyoto at 9:00 reaches Sannomiya at 9:51 (¥1,110). "
                "By Hankyu, from Kyoto-Kawaramachi with a change at Juso, it takes about 1 h 15 min to Kobe-Sannomiya (¥640): slower but cheaper.\n\n"
                "From Sannomiya to Shin-Kobe Station is one stop on the Seishin-Yamate subway line (2 min, ¥210), or you can walk. The photo is Hankyu Kobe-Sannomiya Station on a rainy day.\n\nRecommended arrival: 9:51"),
         gmaps=[gm("JR三ノ宮駅", "JR Sannomiya Station", 34.69486, 135.19509, "JR三ノ宮駅")],
         links=[JR],
         info=info([row("train", "京都9:00発（JR新快速）→ 三ノ宮9:51着（乗り換えなし）", "Kyoto 9:00 (JR Special Rapid) → Sannomiya 9:51 (direct)"),
                    row("fee", "京都→三ノ宮 1,110円（阪急なら京都河原町→神戸三宮 640円）／三宮→新神戸（地下鉄）210円",
                        "Kyoto → Sannomiya ¥1,110 (Hankyu Kyoto-Kawaramachi → Kobe-Sannomiya ¥640) / Sannomiya → Shin-Kobe (subway) ¥210")],
                   tip=TRAIN_TIP)),
    dict(id="nunobiki", name=T("布引の滝", "Nunobiki Falls"), kind=T("滝・展望台", "Waterfall & viewpoint"),
         blurb=T("新幹線の駅のすぐ裏に、日本の名瀑。雄滝の先のみはらし展望台からは、神戸の街と港が見渡せます。",
                 "A famous waterfall right behind a bullet-train station. From the lookout above it, the city and port of Kobe spread out below."),
         lat=34.70983, lng=135.19385,
         text=T("布引の滝（ぬのびきのたき）\n\n新神戸駅の1階から歩いてすぐ山道に入り、雌滝（めんたき）、鼓ヶ滝（つづみがだき）、夫婦滝（めおとだき）、そしていちばん大きな雄滝（おんたき・落差43m）と、4つの滝が続きます。"
                "雌滝までは駅から約5分、雄滝までは約15分。階段が続くので、歩きやすい靴で。\n\n"
                "雄滝からさらに数分登ると、みはらし展望台。ベンチがあり、神戸の街と港、晴れた日には大阪湾の向こうまで見えます。\n\n"
                "入場料はいりません。新神戸駅の裏から布引ハーブ園の山麓駅の北へ抜ける「北野道」は、2027年3月末まで工事で通れないので、帰りは来た道を新神戸駅へ戻りましょう。\n\nおすすめ訪問時間：10:05〜11:15",
                "Nunobiki Falls\n\nA trail starts right from the ground floor of Shin-Kobe Station and passes four falls: Mentaki, Tsuzumigadaki, Meotodaki and the biggest, Ontaki (43 m). "
                "Mentaki is about 5 minutes from the station and Ontaki about 15. There are lots of steps, so wear good shoes.\n\n"
                "A few minutes’ climb beyond Ontaki is the Miharashi lookout, with benches and a view over the city and port, and on clear days across Osaka Bay.\n\n"
                "It’s free. The “Kitano-michi” path from behind Shin-Kobe Station towards the Nunobiki Herb Garden lower station is closed for works until the end of March 2027, so come back down the same way to Shin-Kobe Station.\n\nRecommended visit time: 10:05–11:15"),
         gmaps=[gm("布引の滝（雄滝）", "Nunobiki Falls (Ontaki)", 34.70983, 135.19385, "布引の滝 雄滝"), gm("新神戸駅", "Shin-Kobe Station", 34.70722, 135.19692, "新神戸駅")],
         links=[link("info", "布引の滝（Feel KOBE 神戸公式観光サイト）", "Nunobiki Falls (Feel KOBE, official)", "https://www.feel-kobe.jp/facilities/0000000093/")],
         notices=[{"from": None, "to": "2027-03-31", "url": "https://www.city.kobe.lg.jp/a17526/kanko/leisure/mountain/index.html",
                   "text": T("北野道（新神戸駅の裏〜ハーブ園山麓駅の北側）は、のり面の工事で2027年3月末まで通行止めです（神戸市）。",
                             "The Kitano-michi path (behind Shin-Kobe Station to north of the Herb Garden lower station) is closed for slope works until the end of March 2027 (Kobe City).")}],
         info=info([row("fee", "無料", "Free"),
                    row("hours", "新神戸駅から雌滝まで約5分、雄滝まで約15分（往復で約40分）", "From Shin-Kobe Station: about 5 min to Mentaki, 15 min to Ontaki (about 40 min there and back)")],
                   tip=T("神戸市と神戸観光局（Feel KOBE）のサイトで確認しました。", "Checked on the Kobe City and Feel KOBE websites."))),
    dict(id="tenman", name=T("北野天満神社", "Kitano Tenman Shrine"), kind=T("神社", "Shrine"),
         blurb=T("異人館街のいちばん上にある学問の神様。境内から、風見鶏の館の塔と神戸の街並みが見下ろせます。",
                 "A shrine to the god of learning at the top of the foreign-residence district, looking down on the Weathercock House tower and the city."),
         lat=34.70189, lng=135.18956,
         text=T("北野天満神社（きたのてんまんじんじゃ）\n\n新神戸駅から歩いて約15分。異人館街のいちばん上、石段を上った所にある、菅原道真をまつる神社です。"
                "境内からは、すぐ下に風見鶏の館のとがった塔、その向こうに神戸の街と海が見えます。ここから坂を下りながら異人館を回るのがおすすめです。\n\n"
                "門が開いているのは朝7時半ごろから夕方5時ごろまでです。\n\nおすすめ訪問時間：11:30〜11:50",
                "Kitano Tenman Shrine\n\nAbout 15 minutes on foot from Shin-Kobe Station. At the very top of the foreign-residence district, up a flight of stone steps, this shrine honours Sugawara no Michizane. "
                "From the grounds you look down on the pointed tower of the Weathercock House, with the city and sea beyond. Visit here first, then wander down the slopes past the residences.\n\n"
                "The gates are open from about 7:30 to about 17:00.\n\nRecommended visit time: 11:30–11:50"),
         gmaps=[gm("北野天満神社", "Kitano Tenman Shrine", 34.70189, 135.18956, "北野天満神社 神戸")],
         links=[link("official", "北野天満神社 公式サイト", "Kitano Tenman Shrine (official, Japanese)", "https://www.kobe-kitano.net/")],
         info=info([row("hours", "7:30ごろ〜17:00ごろ", "About 7:30 to about 17:00")],
                   tip=T("公式サイトで確認しました。", "Checked on the official website."))),
    dict(id="ijinkan", name=T("北野異人館街", "Kitano foreign residences"), kind=T("町並み・洋館", "Historic houses"),
         blurb=T("明治・大正の外国人の住まいが残る坂の町。赤レンガの風見鶏の館、緑の萌黄の館をはじめ、洋館をのぞきながら歩きます。",
                 "Hillside lanes of Meiji- and Taisho-era foreigners’ homes: the red-brick Weathercock House, the green Moegi House and more."),
         lat=34.70139, lng=135.18951,
         text=T("北野異人館街（きたのいじんかんがい）\n\n神戸港が開かれたあと、外国人が住んだ洋館が今も残る坂の町です。"
                "屋根に風見鶏がのる赤レンガの「風見鶏の館」と、隣の淡い緑の「萌黄（もえぎ）の館」は、どちらも国の重要文化財。北野町広場のまわりには、英国館や洋館長屋、山手八番館、うろこの家など、中に入れる館がたくさんあります。\n\n"
                "全部入るとかなりの料金になるので、気になる館を2〜3館選ぶのがおすすめ。風見鶏の館と萌黄の館は共通券（800円）があります。館はどこも17:00ごろに閉まります。\n\n"
                "見終わったら北野坂を下って三宮へ。歩いて15分ほどです。\n\nおすすめ訪問時間：11:50〜13:20",
                "Kitano foreign residences\n\nAfter the port of Kobe opened, foreign residents built homes on these slopes, and many survive. "
                "The red-brick Weathercock House with its weathervane and the pale-green Moegi House next door are both Important Cultural Properties. Around Kitano-cho Square there are many more you can enter: the English House, the Western-style row houses, Yamate Hachibankan, the Scale House and others.\n\n"
                "Entering them all adds up, so pick two or three. The Weathercock and Moegi houses share a combined ticket (¥800). Most houses close around 17:00.\n\n"
                "Afterwards, walk down Kitano-zaka to Sannomiya, about 15 minutes.\n\nRecommended visit time: 11:50–13:20"),
         gmaps=[gm("風見鶏の館", "Weathercock House", 34.70139, 135.18951, "風見鶏の館"), gm("萌黄の館", "Moegi House", 34.70100, 135.18925, "萌黄の館")],
         links=[link("official", "風見鶏の館 公式サイト", "Weathercock House (official, Japanese)", "https://kobe-kazamidori.com/guide/"),
                link("official", "うろこグループの館（料金）", "Uroko group houses (fees, Japanese)", "https://kobe-ijinkan.net/ticket/tankan/")],
         info=info([row("hours", "風見鶏の館・萌黄の館 9:00〜17:00（入館16:45まで）。うろこグループの館 10:00〜17:00",
                        "Weathercock House & Moegi House 9:00–17:00 (last entry 16:45). Uroko group houses 10:00–17:00"),
                    row("closed", "風見鶏の館は毎月第3火曜（祝日なら翌日）。萌黄の館は2月の第3水曜とその翌日",
                        "Weathercock House: 3rd Tuesday of each month (next day if a holiday). Moegi House: 3rd Wednesday of February and the day after"),
                    row("fee", "風見鶏の館・萌黄の館 各500円、2館共通券800円（高校生以下は無料）。英国館880円、洋館長屋550円、山手八番館550円、うろこの家・展望ギャラリー1,100円",
                        "Weathercock House and Moegi House ¥500 each, combined ¥800 (free for high school and under). English House ¥880, row houses ¥550, Yamate Hachibankan ¥550, Scale House & gallery ¥1,100")],
                   tip=T("神戸市・神戸観光局と各館の公式サイトで確認しました。", "Checked on the Kobe City, Feel KOBE and house websites."))),
    dict(id="katsudon", name=T("かつ丼 七兵衛（三宮）", "Katsudon Hichibei (Sannomiya)"), kind=T("ランチ", "Lunch"),
         blurb=T("阪急三宮駅のすぐ横、高架下の小さなかつ丼の店。厚いとんかつを玉子でとじた、ボリュームのあるかつ丼です。",
                 "A small katsudon counter under the tracks right by Hankyu Sannomiya: thick pork cutlets simmered with egg over rice."),
         lat=34.69228, lng=135.19180,
         text=T("かつ丼 七兵衛（ひちべい）\n\n阪急の神戸三宮駅の西口を出てすぐ、JRの高架下にある小さなお店です。看板は「かつ丼 七兵衛」（運営会社のページでは「とんかつ七兵衛 神戸本店」）。"
                "入口の券売機で食券を買い、カウンターで食べます。分厚いかつを玉子でとじたかつ丼は、ボリュームたっぷりです。\n\n"
                "お店は11:30から。とんかつが売り切れると早めに閉まります。\n\nおすすめ訪問時間：13:40〜14:20",
                "Katsudon Hichibei\n\nA tiny shop under the JR tracks, right outside the west exit of Hankyu Kobe-Sannomiya Station. The sign reads “Katsudon Hichibei” (the operator calls it “Tonkatsu Hichibei, Kobe main shop”). "
                "Buy a ticket from the machine at the door and eat at the counter. The katsudon, thick cutlets simmered with egg, is a hearty bowl.\n\n"
                "It opens at 11:30 and closes early once the cutlets sell out.\n\nRecommended visit time: 13:40–14:20"),
         gmaps=[gm("とんかつ七兵衛", "Tonkatsu Hichibei", 34.69228, 135.19180, "とんかつ七兵衛 三宮")],
         links=[link("official", "とんかつ七兵衛（運営会社のページ）", "Tonkatsu Hichibei (operator page, Japanese)", "http://www.rb-syuhari.com/hichibe.html")],
         info=info([row("hours", "11:30〜（とんかつが売り切れたら閉店）。閉店時刻と定休日は公式のページに書かれていません（要確認）",
                        "From 11:30 (closes when the cutlets sell out). Closing time and closed days are not given on the official page (please check)")],
                   tip=T("店名と開店時間は運営会社のページで確認しました。", "Name and opening time checked on the operator’s page."))),
    dict(id="meriken", name=T("メリケンパーク・神戸ポートタワー", "Meriken Park & Kobe Port Tower"), kind=T("公園・展望タワー", "Park & tower"),
         blurb=T("赤い鼓の形のポートタワーと、白い帆の海洋博物館。夕方から夜は、港のあかりがきれいです。",
                 "The red, drum-shaped Port Tower and the white sails of the Maritime Museum. Lovely as the harbour lights come on."),
         lat=34.68263, lng=135.18672,
         text=T("メリケンパーク・神戸ポートタワー\n\nJR元町駅の西口から歩いて約15分（三宮からも旧居留地を抜けて歩けます）。海に面した公園に、赤い鼓のような形のポートタワーと、白い帆を重ねたような神戸海洋博物館が並びます。"
                "ポートタワーは2024年にリニューアルし、展望フロアと屋上デッキから、港と六甲の山並みが見渡せます（日時指定のチケット制）。\n\n"
                "冬には「神戸ルミナリエ」の会場にもなります。写真は2025年1月のもの。次は2027年1月29日〜2月7日の予定で、メリケンパークの一部は有料エリアです。\n\n"
                "帰りはJR元町駅から（元町17:01発→三ノ宮で新快速に乗り換え→京都17:59着・1,110円）。\n\nおすすめ訪問時間：14:45〜16:40",
                "Meriken Park & Kobe Port Tower\n\nAbout 15 minutes on foot from the west exit of JR Motomachi Station (you can also walk from Sannomiya through the old foreign settlement). On the waterfront stand the red, drum-shaped Port Tower and the white, sail-like Kobe Maritime Museum. "
                "The tower reopened after renovation in 2024; from its observation floor and rooftop deck you see the port and the Rokko mountains (timed tickets).\n\n"
                "In winter the park is a venue for the Kobe Luminarie; the photos are from January 2025. The next one is planned for 29 January – 7 February 2027, with a paid area in part of Meriken Park.\n\n"
                "Go home from JR Motomachi (17:01, change to the Special Rapid at Sannomiya, Kyoto 17:59, ¥1,110).\n\nRecommended visit time: 14:45–16:40"),
         gmaps=[gm("神戸ポートタワー", "Kobe Port Tower", 34.68263, 135.18672, "神戸ポートタワー"), gm("JR元町駅", "JR Motomachi Station", 34.68957, 135.18715, "JR元町駅 神戸")],
         links=[link("official", "神戸ポートタワー 公式サイト", "Kobe Port Tower (official)", "https://www.kobe-port-tower.com/"),
                link("official", "神戸ルミナリエ 公式サイト", "Kobe Luminarie (official)", "https://www.kobe-luminarie.jp/"), JR],
         info=info([row("hours", "ポートタワー 9:00〜23:00（入場22:30まで）、日時指定のチケット制。年中無休（メンテナンス休業日をのぞく）",
                        "Port Tower 9:00–23:00 (last entry 22:30), timed tickets. Open daily except maintenance days"),
                    row("fee", "ポートタワー 展望フロア＋屋上デッキ 大人1,200円、展望フロアのみ1,000円", "Port Tower: observation floor + rooftop ¥1,200 adults, observation floor only ¥1,000"),
                    row("hours", "神戸ルミナリエ：2027年1月29日〜2月7日、点灯は夕方〜21:30", "Kobe Luminarie: 29 Jan – 7 Feb 2027, lit from dusk to 21:30", until="2027-02-07"),
                    row("train", "帰り：元町17:01発 → 三ノ宮（新快速に乗り換え）→ 京都17:59着・1,110円", "Return: Motomachi 17:01 → Sannomiya (change to Special Rapid) → Kyoto 17:59, ¥1,110")],
                   tip=T("ポートタワーとルミナリエは公式サイト、電車は乗換案内で確認しました。", "Port Tower and Luminarie checked on their websites; trains on a route planner."))),
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
    "id": "kobe",
    "_note": "京都から日帰り 神戸のルート（kobe/ のページ専用。形は eizan-line.json と同じ）。京都からJRで三ノ宮へ、地下鉄で新神戸、布引の滝→北野天満神社→北野異人館街→三宮でかつ丼→メリケンパーク・ポートタワー→元町駅から京都へ。"
             "写真は Toshi の写真ライブラリから選んだもの（布引の滝と北野は2023年6月19日の Nikon D7000、メリケンパークは2024年2月・8月と2025年1月のルミナリエ、七兵衛は2024年2月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（各施設・神戸市・神戸観光局の公式サイト、電車は乗換案内）。このファイルは scripts/build_kobe_data.py で作る。",
    "sections": [{"first": 1, "last": 2, "day": 0}, {"first": 3, "last": 4, "day": 1}, {"first": 5, "last": 5, "day": 2}, {"first": 6, "last": 6, "day": 3}],
    "plan": {"_note": "「選んで回る」の設定。三宮はいつも入る。",
             "picks": [NO[k] for k in ("nunobiki", "tenman", "ijinkan", "katsudon", "meriken")],
             "auto": {str(NO["sannomiya"]): {"always": True}},
             "hints": [
                 H("tenman", {"any": [NO["tenman"]], "none": [NO["nunobiki"]]},
                   "布引の滝に行かない日は、三宮から北野坂を上って歩いて約20分です。", "Skipping the falls? Walk up Kitano-zaka from Sannomiya, about 20 minutes."),
                 H("ijinkan", {"any": [NO["ijinkan"]], "none": [NO["nunobiki"], NO["tenman"]]},
                   "三宮から北野坂を上って、歩いて15分ほどです。", "Walk up Kitano-zaka from Sannomiya, about 15 minutes."),
             ]},
    "photoBase": "../images/kobe/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
