#!/usr/bin/env python3
"""京都 淀・八幡の桜（淀水路の河津桜・石清水八幡宮・背割堤）のデータ（data/routes/yawata.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/yawata/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/yawata"
OUT = f"{R}/data/routes/yawata.json"
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
S = [
    dict(id="yodo", name=T("淀水路の河津桜", "Kawazu cherries along the Yodo canal"), kind=T("桜（3月）", "Cherries (March)"),
         blurb=T("京阪淀駅の近く、水路に沿って約1.3km、ピンクの河津桜が続きます。ソメイヨシノより1か月ほど早い、春いちばんの桜。",
                 "Near Keihan Yodo Station, pink Kawazu cherries line a canal for about 1.3 km: the year’s first blossoms, a month before the Somei-Yoshino."),
         lat=34.90250, lng=135.71700,
         text=T("淀水路（よどすいろ）の河津桜\n\n祇園四条から京阪で淀へ（丹波橋で乗り換え、約20分・360円）。駅の中央改札口から歩いて約10分で、水路沿いの桜並木に出ます。"
                "河津桜が約300本、約1.3km続き、例年3月上旬〜中旬が見ごろ（2月上旬から咲きはじめます）。ゆっくり歩いて30分ほどです。\n\n"
                "トイレは天神橋の近くに1か所だけで、淀駅の改札の外にはありません。写真は2026年3月23日。\n\nおすすめ訪問時間：9:35〜10:30",
                "Kawazu cherries along the Yodo canal\n\nFrom Gion-Shijo take the Keihan line to Yodo (change at Tambabashi, about 20 min, ¥360). About 10 minutes from the central exit, you reach the canal. "
                "Some 300 Kawazu cherries line it for about 1.3 km, usually best in early to mid March (they start in early February). A slow stroll takes about 30 minutes.\n\n"
                "The only toilet is near Tenjin-bashi; there is none outside the ticket gates at Yodo. Photos from 23 March 2026.\n\nRecommended visit time: 9:35–10:30"),
         gmaps=[gm("淀水路 河津桜", "Yodo canal Kawazu cherries", 34.90250, 135.71700, "淀水路 河津桜"), gm("京阪 淀駅", "Keihan Yodo Station", 34.90636, 135.72097, "京阪 淀駅")],
         links=[link("official", "淀の河津桜（京都市観光協会）", "Yodo Kawazu cherries (Kyoto City tourism, Japanese)", "https://totteoki.kyoto.travel/28467/"), JR],
         notices=[{"from": None, "to": None, "url": "https://totteoki.kyoto.travel/28467/", "head": T("見ごろは3月上旬〜中旬", "Best in early to mid March"),
                   "text": T("河津桜は背割堤のソメイヨシノ（4月上旬）より1か月ほど早く咲きます。両方を同じ日に見られるのは、河津桜が遅い年だけです。",
                             "The Kawazu cherries bloom about a month before the Somei-Yoshino at Sewaritei (early April); you can only see both on one day in a late year.")}],
         info=info([row("fee", "無料", "Free"),
                    row("train", "祇園四条 → 丹波橋で乗り換え → 淀 約20分・360円", "Gion-Shijo → change at Tambabashi → Yodo, about 20 min, ¥360")],
                   tip=T("京都市観光協会のサイトと乗換案内で確認しました。", "Checked on the Kyoto City tourism website and a route planner."))),
    dict(id="iwashimizu", name=T("石清水八幡宮", "Iwashimizu Hachimangu"), kind=T("神社（国宝）", "Shrine (National Treasure)"),
         blurb=T("男山の上に建つ、朱と金の国宝の本殿。ケーブルカーで上がると、京都と大阪の間の平野が見渡せます。",
                 "A vermilion-and-gold National Treasure shrine on Mt. Otokoyama. Ride the cable car up for views across the plain between Kyoto and Osaka."),
         lat=34.87973, lng=135.70005,
         text=T("石清水八幡宮（いわしみずはちまんぐう）\n\n淀から京阪で1駅、石清水八幡宮駅へ（3分・240円）。駅の隣から参道ケーブルで男山の上へ（約3分・片道300円）、山上駅から歩いて約5分です。\n\n"
                "朱塗りの南総門をくぐると、極彩色の彫刻で飾られた国宝の本殿。山上の展望台からは、京都の南の平野と三つの川が合流するあたりが見渡せます。"
                "竹林の道は、エジソンが電球に男山の竹を使ったことにちなむ場所としても知られています。\n\nおすすめ訪問時間：10:50〜12:10",
                "Iwashimizu Hachimangu\n\nOne stop from Yodo to Iwashimizu-hachimangu Station (3 min, ¥240). The Sando cable car next to the station climbs Mt. Otokoyama (about 3 min, ¥300 one way), and the shrine is 5 minutes from the top station.\n\n"
                "Through the vermilion south gate stands the National Treasure main hall with its brightly painted carvings. From the lookout you see the plain south of Kyoto where three rivers meet. "
                "The bamboo groves are also known for Edison, who used Otokoyama bamboo for his light-bulb filaments.\n\nRecommended visit time: 10:50–12:10"),
         gmaps=[gm("石清水八幡宮", "Iwashimizu Hachimangu", 34.87973, 135.70005, "石清水八幡宮"), gm("ケーブル八幡宮口駅", "Cable Hachimangu-guchi", 34.88449, 135.69947, "ケーブル八幡宮口")],
         links=[link("official", "石清水八幡宮 公式サイト", "Iwashimizu Hachimangu (official)", "https://iwashimizu.or.jp/"),
                link("timetable", "石清水八幡宮参道ケーブル（京阪）", "Sando cable car (Keihan, Japanese)", "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html")],
         info=info([row("hours", "南総門 6:00〜18:00。お守りの授与所 9:00〜16:00", "South gate 6:00–18:00. Amulet office 9:00–16:00"),
                    row("train", "参道ケーブル 8:10〜18:15、15分おき・約3分", "Cable car 8:10–18:15, every 15 min, about 3 min"),
                    row("fee", "ケーブル 片道300円・往復600円（境内の見学は自由）", "Cable car ¥300 one way, ¥600 return (grounds free to visit)")],
                   tip=T("石清水八幡宮と京阪の公式サイト、京都府観光連盟で確認しました。", "Checked on the shrine and Keihan websites and the Kyoto Prefecture tourism federation."))),
    dict(id="sewaritei", name=T("背割堤の桜並木", "Sewaritei cherry avenue"), kind=T("桜（4月）", "Cherries (April)"),
         blurb=T("木津川と宇治川にはさまれた堤防に、約1.4km、約220本のソメイヨシノ。桜のトンネルの下でお花見を。",
                 "On the levee between the Kizu and Uji rivers, about 220 Somei-Yoshino stretch for 1.4 km: picnic under a tunnel of blossoms."),
         lat=34.89000, lng=135.69300,
         text=T("背割堤（せわりてい）の桜並木\n\nケーブルで下りて、石清水八幡宮駅から歩いて約10分。御幸橋を渡ると、宇治川と木津川にはさまれた細長い堤防に、約1.4km、約220本の桜がトンネルのように続きます。\n\n"
                "見ごろは4月上旬（2026年のさくらまつりは3月28日〜4月5日）。堤防の下の芝生でお花見ができます。まつりの期間は運営協力金（1人100円以上）を集めています。写真は2026年4月8日。\n\nおすすめ訪問時間：12:40〜14:00",
                "Sewaritei cherry avenue\n\nDown by cable car and about 10 minutes’ walk from Iwashimizu-hachimangu Station. Cross the Miyuki bridge: on the long, narrow levee between the Uji and Kizu rivers, about 220 cherries form a tunnel for some 1.4 km.\n\n"
                "Blossoms peak in early April (the 2026 festival ran 28 March – 5 April). You can picnic on the grass below the levee; during the festival a contribution of ¥100 or more is collected. Photos from 8 April 2026.\n\nRecommended visit time: 12:40–14:00"),
         gmaps=[gm("背割堤", "Sewaritei", 34.89000, 135.69300, "背割堤 桜")],
         links=[link("official", "淀川河川公園 背割堤地区", "Yodogawa River Park, Sewaritei (Japanese)", "https://www.yodogawa-park.jp/sansen/")],
         notices=[{"from": None, "to": None, "url": "https://www.yodogawa-park.jp/sansen/", "head": T("見ごろは4月上旬", "Best in early April"),
                   "text": T("背割堤の桜（ソメイヨシノ）は例年4月上旬。淀水路の河津桜（3月上旬〜中旬）とは時期が違います。",
                             "The Sewaritei cherries usually peak in early April, a month after the Kawazu cherries along the Yodo canal.")}],
         info=info([row("hours", "石清水八幡宮駅から歩いて約10分。約1.4km・約220本", "About 10 min on foot from Iwashimizu-hachimangu Station; 1.4 km, about 220 trees"),
                    row("fee", "無料（さくらまつりの期間は運営協力金 1人100円以上）", "Free (¥100+ contribution during the festival)")],
                   tip=T("淀川河川公園の公式サイトで確認しました。", "Checked on the Yodogawa River Park website."))),
    dict(id="deaikan", name=T("さくらであい館（展望塔）", "Sakura Deaikan (observation tower)"), kind=T("展望塔", "Lookout tower"),
         blurb=T("高さ約25mの展望塔から、3つの川の合流点と、まっすぐ延びる桜並木を見下ろせます。",
                 "From the 25 m tower, look down on the meeting of three rivers and the straight line of cherries."),
         lat=34.89042, lng=135.70148,
         text=T("さくらであい館\n\n背割堤の入口にある休憩所で、地上約25mの展望塔に上れます。上から見ると、宇治川・木津川・桂川が合流して淀川になるところと、まっすぐ延びる桜並木がよくわかります。\n\n"
                "展望塔はふだんは無料ですが、桜の時期など混む時期は有料になることがあります（料金は要確認）。帰りは石清水八幡宮駅から京阪で祇園四条へ（約25分・360円）。\n\nおすすめ訪問時間：14:00〜14:30",
                "Sakura Deaikan\n\nA rest house at the entrance to Sewaritei with an observation tower about 25 m high. From the top you can see the Uji, Kizu and Katsura rivers meeting to become the Yodo, and the cherry avenue running straight away.\n\n"
                "The tower is normally free but may charge at busy times such as cherry season (fee to be confirmed). Head home from Iwashimizu-hachimangu Station to Gion-Shijo (about 25 min, ¥360).\n\nRecommended visit time: 14:00–14:30"),
         gmaps=[gm("さくらであい館", "Sakura Deaikan", 34.89042, 135.70148, "さくらであい館")],
         links=[link("official", "さくらであい館", "Sakura Deaikan (Japanese)", "https://www.yodogawa-park.jp/service_center/sewariteisc/"), JR],
         info=info([row("hours", "9:00〜17:00。展望塔 9:00〜16:30（最終受付16:20）", "9:00–17:00. Tower 9:00–16:30 (last entry 16:20)"),
                    row("closed", "12月29日〜1月3日", "29 Dec – 3 Jan"),
                    row("train", "帰り：石清水八幡宮 → 祇園四条 約25分・360円", "Return: Iwashimizu-hachimangu → Gion-Shijo, about 25 min, ¥360")],
                   tip=T("淀川河川公園の公式サイトと乗換案内で確認しました。展望塔の混む時期の料金は確認できていません。", "Checked on the park website and a route planner; the tower’s peak-season fee is unconfirmed."))),
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
    "id": "yawata",
    "_note": "京都 淀・八幡の桜のルート（yawata/ のページ専用。形は eizan-line.json と同じ）。京阪で淀へ、淀水路の河津桜→石清水八幡宮（参道ケーブル）→背割堤の桜→さくらであい館→京阪で京都へ。河津桜は3月上〜中旬、背割堤は4月上旬で時期が違うので、最初から「選んで回る」。"
             "写真は Toshi の写真ライブラリから選んだもの（淀水路と石清水八幡宮は2026年3月23日、背割堤は2026年4月8日、Nikon D7000 を含む。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（京都市観光協会・石清水八幡宮・京阪・淀川河川公園の公式サイト、電車は乗換案内）。このファイルは scripts/build_yawata_data.py で作る。",
    "sections": [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 2, "day": 1}, {"first": 3, "last": 4, "day": 2}],
    "plan": {"_note": "「選んで回る」の設定。defaultMode: pick。", "defaultMode": "pick", "picks": [s["no"] for s in spots], "auto": {}, "hints": [
        H("iwashimizu", {"any": [NO["iwashimizu"]], "none": [NO["yodo"]]},
          "淀に寄らない日は、祇園四条から京阪で石清水八幡宮駅へ（約25分・360円）。",
          "Skipping Yodo? Take the Keihan line from Gion-Shijo straight to Iwashimizu-hachimangu (about 25 min, ¥360)."),
        H("sewaritei", {"any": [NO["sewaritei"]], "andAny": [NO["yodo"]]},
          "淀水路の河津桜（3月上旬〜中旬）と背割堤の桜（4月上旬）は咲く時期が違います。同じ日に見られるのは、河津桜が遅い年だけです。",
          "The Yodo Kawazu cherries (early to mid March) and the Sewaritei cherries (early April) bloom at different times; you’ll only see both on one day in a late year."),
    ]},
    "photoBase": "../images/yawata/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
