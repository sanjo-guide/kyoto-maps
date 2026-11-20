#!/usr/bin/env python3
"""京都 醍醐寺の紅葉ライトアップ（秋期夜間拝観）のデータ（data/routes/daigo.json）を書き出す。

使い方: python3 scripts/build_daigo_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/daigo/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/daigo"
OUT = f"{R}/data/routes/daigo.json"
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
OFFICIAL = link("official", "醍醐寺 秋期夜間拝観（公式）", "Daigoji autumn evening opening (official, Japanese)", "https://www.daigoji.or.jp/event/detail7.html")
NIGHT = row("hours", "2026年秋期夜間拝観：11月20日〜12月6日 18:00〜20:50（受付20:10まで）。昼とは入れ替え制", "Autumn 2026 evening opening: 20 Nov – 6 Dec, 18:00–20:50 (last entry 20:10); separate from the daytime", until="2026-12-06")
# 夜間拝観が終わった次の日から出すお知らせ（全スポット共通）
ENDED = {"from": "2026-12-07", "to": None, "url": "https://www.daigoji.or.jp/event/detail7.html",
         "head": T("2026年の夜間拝観は終わりました", "The 2026 evening opening has ended"),
         "text": T("2026年の秋期夜間拝観は12月6日で終わりました。次の秋の日程は醍醐寺の公式サイトで確かめてください。昼の拝観は9:00から（12月第1日曜の翌日〜2月末は16:30まで、受付は30分前まで）。",
                   "The autumn 2026 evening opening ended on 6 December. Check the Daigoji website for next autumn’s dates. Daytime visits start at 9:00 (until 16:30 from the day after the first Sunday of December to the end of February; last entry 30 min before closing).")}
S = [
    dict(id="niomon", name=T("総門・仁王門", "Somon & Niomon gates"), kind=T("門", "Gates"),
         blurb=T("夜の拝観は、三宝院の受付から。ライトアップされた参道の先に、大きな仁王門が浮かびます。",
                 "The evening visit starts at the Sanboin reception; the great Nio gate glows at the end of the lit avenue."),
         lat=34.95150, lng=135.82002,
         text=T("総門（そうもん）・仁王門（におうもん）\n\n地下鉄東西線の醍醐駅から歩いて約10分（京都駅からJRと地下鉄で約25分・440円）。総門を入り、三宝院の受付で夜間拝観の券を買って、桜の馬場の参道を仁王門へ進みます。\n\n"
                "2026年の秋期夜間拝観は11月20日〜12月6日の18:00〜20:50（受付は20:10まで）。昼の拝観とは入れ替えなので、昼から続けては入れません。券は醍醐寺の公式サイトから先に買うこともできます。紅葉の見ごろは例年11月中旬〜下旬です（京都観光Naviの紅葉だより）。写真は2024年11月24日の夜間拝観です。\n\nおすすめ訪問時間：18:00〜18:20",
                "Somon & Niomon gates\n\nAbout 10 minutes on foot from Daigo Station on the Tozai subway line (about 25 min from Kyoto Station by JR and subway, ¥440). Enter the Somon gate, buy an evening ticket at the Sanboin reception, and follow the approach to the Nio gate.\n\n"
                "The autumn 2026 evening opening runs from 20 November to 6 December, 18:00–20:50 (last entry 20:10). It’s separate from the daytime visit, so you can’t stay on from the day. Tickets can also be bought in advance through the temple website. The leaves usually peak in mid to late November (Kyoto City’s autumn-leaf report). Photos from the evening opening on 24 November 2024.\n\nRecommended visit time: 18:00–18:20"),
         gmaps=[gm("醍醐寺 仁王門", "Daigoji Niomon", 34.95150, 135.82002, "醍醐寺 仁王門"), gm("地下鉄 醍醐駅", "Daigo Station", 34.95049, 135.81066, "地下鉄 醍醐駅")],
         links=[OFFICIAL, JR],
         info=info([NIGHT, row("fee", "夜間拝観 1,500円（中学生以上）", "Evening opening ¥1,500 (junior high and up)", until="2026-12-06"),
                    row("train", "京都駅 → 山科（地下鉄東西線に乗り換え）→ 醍醐 約25分・440円", "Kyoto → Yamashina (change to Tozai line) → Daigo, about 25 min, ¥440")],
                   tip=T("醍醐寺の公式サイトと乗換案内で確認しました。", "Checked on the temple website and a route planner."))),
    dict(id="goju", name=T("五重塔と金堂", "Five-storey pagoda & main hall"), kind=T("国宝", "National Treasures"),
         blurb=T("京都でいちばん古い木造建築の五重塔が、暗い空に白く浮かびます。まわりのもみじも照らされて。",
                 "Kyoto’s oldest wooden building, the five-storey pagoda, glows against the night sky among lit maples."),
         lat=34.95093, lng=135.82281,
         text=T("五重塔（ごじゅうのとう）と金堂（こんどう）\n\n仁王門をくぐると、国宝の金堂と五重塔。五重塔は平安時代（951年）に建てられ、京都府で最も古い木造建築です。夜は塔ともみじが照らされ、昼とはまったく違う姿に。\n\n"
                "日によっては金堂で声明（しょうみょう）の公演もあります（2026年は11月21・22・23日、12月5・6日。声明は18:30〜18:50と20:00〜20:20、不動堂前の護摩は19:15〜19:30。公式サイトには「午後7時より」とも書かれているので、当日の案内で確かめてください）。夜間拝観に入った人は、だれでも金堂に入って聞けます。\n\nおすすめ訪問時間：18:20〜18:50",
                "Five-storey pagoda & main hall\n\nThrough the Nio gate stand the National Treasure main hall and five-storey pagoda. Built in 951 in the Heian period, the pagoda is the oldest wooden building in Kyoto Prefecture. Lit at night with the maples around it, it looks nothing like it does by day.\n\n"
                "On some evenings there are shomyo (Buddhist chant) performances in the main hall (2026: 21, 22, 23 Nov and 5, 6 Dec; chanting 18:30–18:50 and 20:00–20:20, and a fire ritual in front of the Fudo hall 19:15–19:30; the website also says “from 7 pm”, so check the notice on the day). Anyone with an evening ticket can go into the hall and listen.\n\nRecommended visit time: 18:20–18:50"),
         gmaps=[gm("醍醐寺 五重塔", "Daigoji pagoda", 34.95093, 135.82281, "醍醐寺 五重塔")],
         links=[OFFICIAL],
         info=info([NIGHT], tip=T("醍醐寺の公式サイトで確認しました。", "Checked on the temple website."))),
    dict(id="benten", name=T("弁天堂と弁天池", "Bentendo & its pond"), kind=T("池・お堂", "Pond & hall"),
         blurb=T("夜間拝観のいちばんの見どころ。朱の弁天堂と橋、照らされたもみじが、池の水面に鏡のように映ります。",
                 "The evening’s highlight: the vermilion Benten hall and bridge and the lit maples, mirrored in the pond."),
         lat=34.95088, lng=135.82432,
         text=T("弁天堂（べんてんどう）と弁天池\n\n伽藍のいちばん奥、池のほとりに建つ朱色の弁天堂。ライトアップされたもみじと朱の橋が、風のない夜は池に鏡のように映ります。池の正面、橋とお堂が両方入る場所がいちばん混みます（写真2・3枚目）。夜は冷えるので上着を。\n\n"
                "昼に来るなら、三宝院の庭園・霊宝館・伽藍の3か所共通券（1,500円）があります。山の上の上醍醐は、がけ崩れの危険のため当面入山できません。\n\nおすすめ訪問時間：18:50〜19:40",
                "Bentendo and its pond\n\nAt the far end of the precinct, the vermilion Benten hall stands by a pond. On a still night, the lit maples and the red bridge are mirrored in the water. The busiest spot is straight across the pond, where the bridge and hall both fit in the frame (photos 2 and 3). Evenings are cold, so bring a jacket.\n\n"
                "By day, a combined ticket for the Sanboin garden, the Reihokan museum and the main precinct costs ¥1,500. Kami-Daigo on the mountain is closed for now because of landslide risk.\n\nRecommended visit time: 18:50–19:40"),
         gmaps=[gm("醍醐寺 弁天堂", "Daigoji Bentendo", 34.95088, 135.82432, "醍醐寺 弁天堂")],
         links=[OFFICIAL, link("official", "醍醐寺 拝観案内", "Daigoji visiting info (official, Japanese)", "https://www.daigoji.or.jp/guide/time.html")],
         info=info([NIGHT, row("hours", "昼の拝観 9:00〜17:00（12月第1日曜の翌日から2月末は16:30まで、受付は30分前まで）", "Daytime 9:00–17:00 (16:30 from the day after the first Sunday of December to the end of February; last entry 30 min before)"),
                    row("fee", "昼：3か所共通券 大人1,500円、2か所 1,000円、1か所 600円（春期の3月20日〜4月第3日曜は3か所1,800円、1か所800円）", "Daytime: 3-site ticket ¥1,500, 2 sites ¥1,000, 1 site ¥600 (in spring, 20 Mar to the 3rd Sunday of April: 3 sites ¥1,800, 1 site ¥800)")],
                   tip=T("醍醐寺の公式サイトで確認しました。", "Checked on the temple website."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    out.setdefault("notices", [])
    out["notices"].append(ENDED)
    spots.append(out)
NO = {s["id"]: s["no"] for s in spots}

data = {
    "id": "daigo",
    "_note": "京都 醍醐寺の紅葉ライトアップ（秋期夜間拝観）のルート（daigo/ のページ専用。形は eizan-line.json と同じ）。総門・仁王門→五重塔・金堂→弁天堂。"
             "写真は Toshi の写真ライブラリから選んだもの（2024年11月24日の夜間拝観、Nikon D7000 と iPhone。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（醍醐寺の公式サイト、電車は乗換案内）。このファイルは scripts/build_daigo_data.py で作る。",
    "sections": [{"first": 1, "last": 3, "day": 0}],
    "photoBase": "../images/daigo/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
