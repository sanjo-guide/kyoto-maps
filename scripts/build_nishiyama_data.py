#!/usr/bin/env python3
"""京都 西山（松尾大社・鈴虫寺・地蔵院・浄住寺）のデータ（data/routes/nishiyama.json）を書き出す。

使い方: python3 scripts/build_nishiyama_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/nishiyama/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/nishiyama"
OUT = f"{R}/data/routes/nishiyama.json"
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
TIP = T("時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。", "Times and fares checked on a route planner (Saturday timetable, November 2026).")
S = [
    dict(id="matsuo", name=T("松尾大社", "Matsunoo Taisha"), kind=T("神社", "Shrine"),
         blurb=T("お酒の神様として知られる、京都でもとくに古い神社。朱の大鳥居をくぐると、奉納された酒樽がずらりと並びます。",
                 "One of Kyoto’s oldest shrines, revered as the god of sake: through the vermilion torii, rows of donated sake barrels."),
         lat=35.00019, lng=135.68530,
         text=T("松尾大社（まつのおたいしゃ）\n\n京都河原町から阪急で桂へ、嵐山線に乗り換えて松尾大社駅へ（約20分・240円）。駅を出ると、すぐ大鳥居が見えます。"
                "平安京より前からある古い神社で、お酒の神様として全国の酒造りの人たちが信仰しています。境内には、奉納された酒樽が壁のように積まれています。\n\n"
                "昭和の作庭家・重森三玲の庭「松風苑」と神像館は共通券（500円）で見られます。\n\nおすすめ訪問時間：9:40〜10:15",
                "Matsunoo Taisha\n\nFrom Kyoto-Kawaramachi take the Hankyu line to Katsura and change to the Arashiyama line for Matsuo-taisha (about 20 min, ¥240). The great torii is right outside the station. "
                "Older than the capital of Heian-kyo, the shrine is revered by sake brewers across Japan as the god of sake; donated barrels are stacked like a wall in the grounds.\n\n"
                "The Shofu-en gardens by the Showa garden designer Shigemori Mirei and the statue hall share a ticket (¥500).\n\nRecommended visit time: 9:40–10:15"),
         gmaps=[gm("松尾大社", "Matsunoo Taisha", 35.00019, 135.68530, "松尾大社")],
         links=[link("official", "松尾大社 公式サイト", "Matsunoo Taisha (official, Japanese)", "https://www.matsunoo.or.jp/"), JR],
         info=info([row("train", "京都河原町9:15発（阪急）→ 桂で乗り換え → 松尾大社9:34着・240円", "Kyoto-Kawaramachi 9:15 (Hankyu) → change at Katsura → Matsuo-taisha 9:34, ¥240"),
                    row("hours", "境内 5:00〜18:00。庭園「松風苑」と神像館 9:00〜16:00（日曜・祝日は16:30まで）", "Grounds 5:00–18:00. Shofu-en gardens & statue hall 9:00–16:00 (16:30 on Sundays and holidays)"),
                    row("fee", "庭園と神像館の共通券 大人500円", "Gardens & statue hall ¥500 adults")],
                   tip=T("時間と料金は松尾大社の公式サイトと京都観光Navi、電車は乗換案内で確認しました。", "Checked on the shrine website, Kyoto Kanko Navi and a route planner."))),
    dict(id="suzumushi", name=T("鈴虫寺（華厳寺）", "Suzumushi-dera (Kegon-ji)"), kind=T("寺", "Temple"),
         blurb=T("一年中、鈴虫の声が聞こえるお寺。お茶とお菓子をいただきながら聞く説法と、高台の庭から見る京都の町。",
                 "A temple where bell crickets sing all year round: a talk over tea and sweets, and a hillside garden looking over Kyoto."),
         lat=34.99368, lng=135.68519,
         text=T("鈴虫寺（すずむしでら）・華厳寺（けごんじ）\n\n松尾大社から南へ歩いて約15分。石段を上ると、一年中鈴虫が鳴く書院で、お茶とお菓子をいただきながら住職の説法（約30分）を聞きます。"
                "門の前の「幸福地蔵」は、わらじをはいて願いをかなえに来てくれるお地蔵さまです。\n\n"
                "高台にある庭からは京都の町が見渡せ、秋はもみじがきれいです。説法はだいたい50分ごとに始まり、混む日は待つこともあります。秋の土日などは、公式サイトの「混雑予想カレンダー」で確かめてから行きましょう。\n\nおすすめ訪問時間：10:35〜11:25",
                "Suzumushi-dera (Kegon-ji)\n\nAbout 15 minutes’ walk south of Matsunoo Taisha. Climb the steps to a hall where bell crickets sing all year, and listen to the priest’s talk (about 30 min) over tea and sweets. "
                "The “Kofuku Jizo” at the gate wears straw sandals so he can walk to you and grant your wish.\n\n"
                "The hillside garden looks out over Kyoto, with red maples in autumn. Talks start roughly every 50 minutes; on busy days you may have to wait. On autumn weekends, check the congestion forecast calendar on the temple’s website first.\n\nRecommended visit time: 10:35–11:25"),
         gmaps=[gm("鈴虫寺", "Suzumushi-dera", 34.99368, 135.68519, "鈴虫寺 華厳寺")],
         links=[link("official", "鈴虫寺 公式サイト", "Suzumushi-dera (official, Japanese)", "https://suzutera.or.jp/"),
                link("info", "鈴虫寺 混雑予想カレンダー", "Suzumushi-dera congestion calendar (Japanese)", "https://suzutera.or.jp/#calendar")],
         info=info([row("hours", "9:00〜17:00（入門は16:30まで）。説法の始まりは9:00・9:50・10:40・11:30・12:20…のめやす", "9:00–17:00 (last entry 16:30). Talks start around 9:00, 9:50, 10:40, 11:30, 12:20…"),
                    row("closed", "年中無休", "Open every day"),
                    row("fee", "大人500円、子ども（4歳〜中学生）300円（お茶とお菓子つき）", "¥500 adults, ¥300 children aged 4 to junior high (tea and sweets included)")],
                   tip=T("鈴虫寺の公式サイトで確認しました。", "Checked on the temple website."))),
    dict(id="kokenochaya", name=T("苔乃茶屋（お昼）", "Koke-no-chaya (lunch)"), kind=T("ランチ", "Lunch"),
         blurb=T("苔寺の門前の古い茶屋。とろろとにしんのおそばで、お昼にします。",
                 "An old teahouse by the Moss Temple gate: soba with grated yam or herring for lunch."),
         lat=34.99221, lng=135.68567,
         text=T("苔乃茶屋（こけのちゃや）\n\n鈴虫寺から苔寺（西芳寺）の方へ下りた所にある、門前の茶屋です。のれんに「門前とろいそば」。写真はにしんそばです。\n\n"
                "となりの西芳寺（苔寺）は、事前の申し込みが必要です（オンラインは2か月前から前日まで、冥加料4,000円から。13歳以上）。行きたい人は早めに申し込みましょう。2027年1月12日〜2月26日は、境内整備のため日々参拝はお休みです。\n\nおすすめ訪問時間：11:30〜12:15",
                "Koke-no-chaya\n\nA teahouse by the gate of Saihoji (the Moss Temple), just downhill from Suzumushi-dera. The curtain advertises tororo soba; the photo shows nishin (herring) soba.\n\n"
                "Saihoji next door needs advance application (online from two months to the day before, from ¥4,000; age 13 and over). Apply early if you want to go. The regular visits are suspended from 12 January to 26 February 2027 for work on the grounds.\n\nRecommended visit time: 11:30–12:15"),
         gmaps=[gm("苔乃茶屋", "Koke-no-chaya", 34.99221, 135.68567, "苔乃茶屋 京都 西芳寺")],
         links=[link("official", "西芳寺（苔寺）の参拝申し込み", "Saihoji visit application (official)", "https://intosaihoji.com/nichinichi/")],
         info=info([row("hours", "営業時間と休みの日は、公式の情報が見つかりませんでした（要確認）", "Opening hours and closed days: no official information found (please check)")], verified=False)),
    dict(id="jizoin", name=T("地蔵院（竹の寺）", "Jizoin (the Bamboo Temple)"), kind=T("寺", "Temple"),
         blurb=T("竹林の参道の先に、苔の庭と、ハートの形の窓。静かな「竹の寺」です。",
                 "Past a bamboo-lined approach: a moss garden and a heart-shaped window. The quiet “Bamboo Temple”."),
         lat=34.99069, lng=135.68636,
         text=T("地蔵院（じぞういん）・竹の寺\n\n苔乃茶屋から歩いて数分。山門をくぐると、竹林の中を参道がまっすぐ続きます。方丈の前には苔の庭が広がり、ハートの形の窓から竹林がのぞけます。"
                "庭は方丈に座って眺める庭で、中には入れません。観光客が少なく、座ってゆっくり見られます。\n\n"
                "ハートの形の窓（猪目窓）がある茶室は、春と秋の寺宝特別拝観の間は見られません（2026年の秋は10月31日〜12月13日）。窓が目当てなら、その期間を外しましょう。紅葉の見ごろは例年11月下旬〜12月上旬です（京都観光Naviの紅葉だより）。\n\n"
                "ふだんは木曜・金曜が休みですが、秋の寺宝特別拝観（2026年は10月31日〜12月13日）の間は毎日開いています。特別拝観の間の拝観料は、だれでも大人1,000円です。\n\nおすすめ訪問時間：12:30〜13:15",
                "Jizoin (the Bamboo Temple)\n\nA few minutes’ walk from Koke-no-chaya. Through the gate, a path runs straight through bamboo. In front of the abbot’s hall lies a moss garden, and a heart-shaped window frames the bamboo. "
                "You view the garden seated in the abbot’s hall; you can’t walk in it. With few tourists, there is room to sit and look.\n\n"
                "The tea room with the heart-shaped window can’t be seen during the spring and autumn treasure displays (31 Oct – 13 Dec in autumn 2026), so avoid those weeks if the window is what you’re coming for. The maples usually peak from late November to early December (Kyoto City’s autumn-leaf report).\n\n"
                "It usually closes on Thursdays and Fridays, but is open every day during the autumn treasure display (31 Oct – 13 Dec 2026), when admission is ¥1,000 for all adults.\n\nRecommended visit time: 12:30–13:15"),
         gmaps=[gm("地蔵院（竹の寺）", "Jizoin", 34.99069, 135.68636, "地蔵院 竹の寺 西京区")],
         links=[link("official", "地蔵院 公式サイト", "Jizoin (official, Japanese)", "https://www.takenotera-jizoin.jp/")],
         info=info([row("hours", "9:00〜16:00（最終受付15:40）", "9:00–16:00 (last entry 15:40)"),
                    row("closed", "木曜・金曜（7・8月は月曜・木曜）。寺宝特別拝観の間（2026年は10月31日〜12月13日）、11月21日〜12月10日、ゴールデンウィークは無休。1月4日〜2月10日の平日なども休み。臨時休みあり", "Thursdays and Fridays (Mondays and Thursdays in July and August). Open daily during the treasure display (31 Oct – 13 Dec 2026), 21 Nov – 10 Dec and Golden Week; also closed weekdays 4 Jan – 10 Feb; occasional closures"),
                    row("fee", "大人1,000円、子ども（6〜17歳）500円。日本に住んでいる人は大人500円・小中高生300円。寺宝特別拝観の期間は、だれでも大人1,000円（6〜17歳500円）", "¥1,000 adults, ¥500 children aged 6–17. Residents of Japan: ¥500 adults, ¥300 school pupils. During the treasure displays: ¥1,000 for all adults (¥500 aged 6–17)")],
                   tip=T("地蔵院の公式サイトで確認しました。", "Checked on the temple website."))),
    dict(id="jojuji", name=T("浄住寺", "Jojuji"), kind=T("寺（特別公開）", "Temple (special opening)"),
         blurb=T("ふだんは非公開の、竹林と苔の古いお寺。秋と春の特別公開のときだけ、中に入れます。",
                 "An old temple of bamboo and moss, usually closed; you can go in only during its autumn and spring openings."),
         lat=34.98916, lng=135.68680,
         text=T("浄住寺（じょうじゅうじ）\n\n地蔵院から歩いて約4分。石の門柱の先の石段を上ると、竹林と苔の庭が広がる黄檗宗のお寺です。亀の甲羅のような節の「亀甲竹（きっこうちく）」も見られます。\n\n"
                "ふだんは非公開で、2026年の秋の特別拝観は11月21日〜12月13日です。紅葉の見ごろは例年11月下旬（京都観光Naviの紅葉だより）。写真は2026年1月のもの。\n\n"
                "帰りは阪急の上桂駅まで歩いて約12分。桂で乗り換えて京都河原町へ（200円）。\n\nおすすめ訪問時間：13:25〜14:10",
                "Jojuji\n\nAbout 4 minutes’ walk from Jizoin. Up the steps past the stone gateposts is an Obaku Zen temple of bamboo groves and moss gardens, with “kikkochiku” (tortoise-shell bamboo), whose joints look like a tortoise shell.\n\n"
                "It is usually closed; the autumn 2026 special opening runs from 21 November to 13 December. The maples usually peak in late November (Kyoto City’s autumn-leaf report). The photos are from January 2026.\n\n"
                "Then walk about 12 minutes to Hankyu Kami-Katsura Station and change at Katsura for Kyoto-Kawaramachi (¥200).\n\nRecommended visit time: 13:25–14:10"),
         gmaps=[gm("浄住寺", "Jojuji", 34.98916, 135.68680, "浄住寺 西京区"), gm("阪急 上桂駅", "Hankyu Kami-Katsura Station", 34.99030, 135.69593, "阪急 上桂駅")],
         links=[link("official", "浄住寺 公式サイト（拝観案内）", "Jojuji (official, Japanese)", "https://jojuji.org/admission.html"), JR],
         caution=T("ふだんは非公開", "Usually closed"),
         notices=[{"from": None, "to": "2026-12-13", "url": "https://jojuji.org/admission.html", "head": T("特別公開のときだけ", "Special openings only"),
                   "text": T("ふだんは非公開です。2026年の秋の特別拝観は11月21日〜12月13日、9:30〜16:30（最終受付16:00）。",
                             "Usually closed. Autumn 2026 special opening: 21 Nov – 13 Dec, 9:30–16:30 (last entry 16:00).")},
                  {"from": "2026-12-14", "to": None, "url": "https://jojuji.org/admission.html", "head": T("特別公開のときだけ", "Special openings only"),
                   "text": T("ふだんは非公開で、特別拝観のときだけ中に入れます。次の公開の日程は公式サイトで確かめてください。",
                             "Usually closed; you can go in only during special openings. Check the official website for the next dates.")}],
         info=info([row("hours", "2026年秋の特別拝観：11月21日〜12月13日 9:30〜16:30（最終受付16:00）", "Autumn 2026 opening: 21 Nov – 13 Dec, 9:30–16:30 (last entry 16:00)", until="2026-12-13"),
                    row("fee", "1,000円、子ども500円（土日祝は抹茶とお菓子1,000円も）", "¥1,000, children ¥500 (matcha and sweets ¥1,000 at weekends and holidays)"),
                    row("train", "上桂（阪急）→ 桂で乗り換え → 京都河原町・200円", "Kami-Katsura (Hankyu) → change at Katsura → Kyoto-Kawaramachi, ¥200")],
                   tip=T("浄住寺の公式サイトと京都観光Navi、電車は乗換案内で確認しました。", "Checked on the temple website, Kyoto Kanko Navi and a route planner."))),
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
    "id": "nishiyama",
    "_note": "京都 西山のルート（nishiyama/ のページ専用。形は eizan-line.json と同じ）。阪急で松尾大社→鈴虫寺→苔乃茶屋でお昼→地蔵院（竹の寺）→浄住寺→上桂駅。"
             "写真は Toshi の写真ライブラリから選んだもの（2025年10月30日と2026年1月13日の Nikon D7000。地蔵院のハートの窓は iPhone の位置情報で地蔵院と確認。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（各寺社の公式サイト・京都観光Navi、電車は乗換案内）。このファイルは scripts/build_nishiyama_data.py で作る。",
    "sections": [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 3, "day": 1}, {"first": 4, "last": 5, "day": 2}],
    "plan": {"_note": "「選んで回る」の設定。全部選べる。", "picks": [s["no"] for s in spots], "auto": {}, "hints": [
        H("suzumushi", {"any": [NO["suzumushi"]], "none": [NO["matsuo"]]},
          "松尾大社に寄らない日は、京都駅から京都バス73系統、三条京阪から63系統で終点の「苔寺・すず虫寺」へ（約1時間・230円）。",
          "Skipping Matsunoo? Kyoto Bus 73 from Kyoto Station or 63 from Sanjo Keihan runs to the last stop “Kokedera-Suzumushidera” (about an hour, ¥230)."),
        H("jizoin", {"any": [NO["jizoin"]], "none": [NO["jojuji"]]},
          "帰りは阪急の上桂駅まで歩いて約12分。または「苔寺・すず虫寺」から京都バスで、三条京阪（63系統）・京都駅（73系統）へ。",
          "Go home from Hankyu Kami-Katsura (about 12 min on foot), or by Kyoto Bus from “Kokedera-Suzumushidera” to Sanjo Keihan (63) or Kyoto Station (73)."),
    ]},
    "photoBase": "../images/nishiyama/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
