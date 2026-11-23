#!/usr/bin/env python3
"""天橋立・伊根マップのデータを2通りの順番で書き出す。
   data/routes/amanohashidate.json（傘松公園が先）と amanohashidate-ine.json（伊根が先）。

使い方: python3 scripts/build_amanohashidate_data.py
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直すと、2つのデータが両方そろって書き換わる
- 2026-11-22: ゲストが実際に回れる1日として見直し（時刻・料金を公式で再確認、出典は各スポットの info.source）
- 写真は images/amanohashidate/<スポットのid>-<番号>.jpg を番号の順に全部使う（向井酒造の Wikimedia Commons の写真は下の _extra）
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = f"{R}/data/routes"
IMG = f"{R}/images/amanohashidate"
_files = os.listdir(IMG)
PICKS = {}
for f in _files:
    m = re.match(r"(.+)-(\d+)\.jpg$", f)
    if m:
        PICKS.setdefault(m.group(1), []).append(int(m.group(2)))
CHECKED = "2026-11-22"
D20 = "2026-11-20"   # 20日に確認して22日は見直していないもの
TANKAI_TICKETS = "https://www.tankai.jp/tourist_tickets/"
TANKAI_BUS = "https://www.tankai.jp/routebus/timetable/"
TANKAI_BOAT = "https://www.tankai.jp/trip/amaboat/"
YAHOO = "https://transit.yahoo.co.jp/"


def gm(label_ja, label_en, lat, lng, q):
    return {"label": {"ja": label_ja, "en": label_en}, "lat": lat, "lng": lng,
            "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url, url_en=None):
    return {"kind": kind, "label": {"ja": ja, "en": en}, "url": {"ja": url, "en": url_en or url}}


def row(kind, ja, en, frm=None, until=None):
    return {"kind": kind, "text": {"ja": ja, "en": en}, "until": until, "from": frm}


def info(rows, source, cash=False, tip=None, checked=CHECKED):
    """source は出典と確認日（画面には出ない記録）"""
    return {"rows": rows, "cash": cash, "tip": tip, "checked": checked, "source": source}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    """スポットを開いていちばん上に出る注意書き"""
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def photos(pid, extra=None):
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid]) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def T(ja, en):
    return {"ja": ja, "en": en}


BUS_BACK = row("bus", "伊根→天橋立ケーブル下→天橋立駅：15:08→15:41→16:08／16:00→16:33→17:00／16:47→17:20→17:47／17:56→18:27→18:54（毎日）。フリーパスで乗れます（なければケーブル下まで200円、天橋立駅まで400円）",
               "Ine → Amanohashidate Cable-shita → Amanohashidate Sta.: 15:08→15:41→16:08 / 16:00→16:33→17:00 / 16:47→17:20→17:47 / 17:56→18:27→18:54 (daily). Covered by the free pass (otherwise ¥200 to Cable-shita, ¥400 to the station)")
BUS_SRC = "丹後海陸交通 公式の時刻表（伊根・蒲入線）と路線バスの案内（エリア制上限200円・支払方法）。2026-11-22に確認"


def build(course):
    A = course == "kasamatsu"
    S = {}

    S["kyoto"] = {
        "name": T("京都駅", "Kyoto Station"),
        "kind": T("駅（スタート）", "Station (start)"),
        "blurb": T("三条のあたりを8時ごろに出て、8:38の特急はしだて1号へ。乗り換えなしで約2時間です。",
                   "Leave the Sanjo area around 8:00 for the 8:38 Hashidate No. 1: about 2 hours to Amanohashidate, no change."),
        "lat": 34.98535, "lng": 135.758766,
        "caution": T("指定席は先に。帰りの18:09の分も一緒に", "Reserve seats ahead, including the 18:09 back"),
        "notices": [notice("乗り場は31番のりば", "The train leaves from platform 31",
                           "山陰線（嵯峨野線）のホームは駅のいちばん西側です。地下鉄の改札から歩いて10分ほど見ておいてください。",
                           "The San’in (Sagano) Line platforms are at the far west end of the station. Allow about 10 minutes on foot from the subway gates.")],
        "text": T(
            "京都駅（きょうとえき）\n\n8:38発の特急はしだて1号は、乗り換えなしで10:39に天橋立に着きます。乗り場は山陰線（嵯峨野線）の31番のりばです。\n\n三条のあたりからは地下鉄で。烏丸御池（からすまおいけ）8:04発に乗ると京都8:09着（220円）。三条京阪からは7:58発の東西線で烏丸御池へ行き、烏丸線に乗り換えて8:14着（260円）。どちらも平日の時刻です。きっぷをまだ買っていない人、朝ごはんや飲み物を買う人は、もう15分早く出てください。\n\n指定席は、帰りの18:09発はしだて8号の分も一緒に買っておきます。片道は指定席で4,800〜5,200円（日によって変わります）。\n\n安く行くなら、京都駅前9:00発の高速バスもあります（天橋立駅11:05着、3,400〜3,900円、予約できます）。そのときは「傘松公園が先」の順番で、11:30の観光船から始めれば、あとは同じ時間で回れます。\n\n写真は京都丹後鉄道の観光列車「丹後の海」。はしだてにこの車両が使われる日もあります。\n\nおすすめ出発時間：8:00（三条のあたり）→ 8:38（京都駅）",
            "Kyoto Station\n\nThe 8:38 Hashidate No. 1 limited express reaches Amanohashidate at 10:39 with no change. It leaves from platform 31 on the San’in (Sagano) Line.\n\nFrom the Sanjo area, take the subway. The 8:04 from Karasuma Oike gets to Kyoto at 8:09 (¥220). From Sanjo Keihan, take the 7:58 Tozai Line to Karasuma Oike and change to the Karasuma Line, arriving 8:14 (¥260). These are weekday times. If you still need tickets, breakfast or drinks, leave 15 minutes earlier.\n\nBuy reserved seats for both ways, including the 18:09 Hashidate No. 8 back. One way with a reserved seat is ¥4,800–5,200 (it depends on the day).\n\nA cheaper way is the 9:00 highway bus from Kyoto Station (Amanohashidate Station 11:05, ¥3,400–3,900, seats can be booked). In that case choose “Kasamatsu first” and start with the 11:30 boat; the rest of the day runs at the same times.\n\nThe blue train in the photos is the Kyoto Tango Railway’s “Tango no Umi”, which is used for some Hashidate services.\n\nRecommended departure time: 8:00 (Sanjo area) → 8:38 (Kyoto Station)"),
        "gmaps": [gm("JR京都駅", "JR Kyoto Station", 34.98535, 135.758766, "JR京都駅"),
                  gm("地下鉄 烏丸御池駅", "Karasuma Oike subway station", 35.01092, 135.75952, "烏丸御池駅")],
        "links": [link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/"),
                  link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", YAHOO),
                  link("official", "高速バス 京都線（丹後海陸交通）", "Highway bus, Kyoto line (Tankai, Japanese)", "https://www.tankai.jp/highwaybus/kyotoline/")],
        "info": info([
            row("train", "特急はしだて1号 京都8:38発（31番のりば）→天橋立10:39着",
                "Hashidate No. 1: Kyoto 8:38 (platform 31) → Amanohashidate 10:39"),
            row("train", "三条のあたりから（平日）：地下鉄 烏丸御池8:04発→京都8:09着・220円（8:08発・8:13発もあります）。三条京阪7:58発→烏丸御池で乗り換え→京都8:14着・260円",
                "From the Sanjo area (weekdays): subway Karasuma Oike 8:04 → Kyoto 8:09, ¥220 (also 8:08 and 8:13). Sanjo Keihan 7:58 → change at Karasuma Oike → Kyoto 8:14, ¥260"),
            row("fee", "特急 片道：乗車券2,320円＋指定席特急料金2,480〜2,880円＝4,800〜5,200円（日によって変わります）",
                "Express, one way: fare ¥2,320 + reserved-seat charge ¥2,480–2,880 = ¥4,800–5,200 (depends on the day)"),
            row("bus", "高速バス：京都駅前9:00発→天橋立駅11:05着。帰りは天橋立駅18:00発→京都駅前20:10着。片道3,400〜3,900円（日によって変わります）",
                "Highway bus: Kyoto Station 9:00 → Amanohashidate Station 11:05; back 18:00 → Kyoto Station 20:10. ¥3,400–3,900 one way (depends on the day)"),
        ], "特急の時刻・のりば・料金と地下鉄は乗換案内（Yahoo!路線情報。特急は2026年11月25日・28日・12月2日、地下鉄は12月2日の検索結果）。高速バスは丹後海陸交通 公式（2026年10月1日改正の時刻と運賃）。2026-11-22に確認",
            tip=T("特急の料金は、乗換案内で調べた3日で4,800円・5,000円・5,200円と違いました。買うときに確かめてください。",
                  "The express cost ¥4,800, ¥5,000 and ¥5,200 on the three days we looked up. Check when you buy.")),
    }

    S["station"] = {
        "name": T("天橋立駅（フリーパスを買う）", "Amanohashidate Station (get the day pass)"),
        "kind": T("駅・観光案内所", "Station & tourist info"),
        "blurb": T("最初に「天橋立・伊根フリーパス 1day」を買います。船もケーブルカーもバスも、これ1枚。",
                   "First buy the Amanohashidate & Ine 1-Day Free Pass: boats, cable car and buses all in one."),
        "lat": 35.557585, "lng": 135.182426,
        "caution": T("バスはICOCAなどが使えません", "Buses don’t take ICOCA or other transit IC cards"),
        "text": T(
            "天橋立駅（あまのはしだてえき）\n\n着いたら最初に「海の京都 天橋立・伊根フリーパス 1day」（大人3,550円）を買います。天橋立駅の切符売り場（京都丹後鉄道の窓口）か、歩いて5分の天橋立桟橋の観光船乗り場で売っています。\n\nこの1枚で、天橋立の観光船、傘松公園のケーブルカー・リフト、伊根へのバス、伊根湾めぐり遊覧船に乗れます。別々に買うと3,700〜4,000円なので150〜450円安く、乗り継ぎのたびに切符を買わなくてすみます。伊根へのバスは交通系ICカード（ICOCAなど）が使えないので、その点でも楽です。\n\n" +
            ("" if A else "土日祝に「伊根が先」で回る日は、ここのバス停から10:58発のバスでまっすぐ伊根へ行く方法もあります（4番に書いています）。\n\n") +
            "自転車で渡る人は、紹介ページの「交通費のめやす」も見てください。\n\nおすすめ訪問時間：10:39〜10:45",
            "Amanohashidate Station\n\nFirst buy the “Kyoto by the Sea Amanohashidate & Ine Free Pass 1day” (¥3,550 per adult), at the Kyoto Tango Railway ticket window in the station or at the boat office on Amanohashidate pier, 5 minutes’ walk away.\n\nIt covers the Amanohashidate sightseeing boat, the Kasamatsu Park cable car and chairlift, the bus to Ine and the Ine Bay boat. Bought separately these cost ¥3,700–4,000, so you save ¥150–450 and don’t have to buy a ticket at every connection. The bus to Ine doesn’t take transit IC cards such as ICOCA, which is another reason to have it.\n\n" +
            ("" if A else "On weekends and holidays, if you do Ine first, you can also take the 10:58 bus from the stop here straight to Ine (see stop 4).\n\n") +
            "If you plan to cross by bike, see “Getting around: fares” on the intro page.\n\nRecommended visit time: 10:39–10:45"),
        "gmaps": [gm("天橋立駅", "Amanohashidate Station", 35.557585, 135.182426, "天橋立駅")],
        "links": [
            link("official", "お得なチケット（丹後海陸交通）", "Value tickets (Tankai, Japanese)", TANKAI_TICKETS),
            link("info", "天橋立観光協会", "Amanohashidate Tourist Association", "https://www.amanohashidate.jp/"),
        ],
        "info": info([
            row("pass", "海の京都 天橋立・伊根フリーパス 1day：大人3,550円・小児1,780円（買った日1日有効）",
                "Amanohashidate & Ine Free Pass 1day: ¥3,550 adults, ¥1,780 children (valid on the day)"),
            row("pass", "乗れるもの：天橋立観光船（宮津桟橋〜天橋立桟橋〜一の宮桟橋）、ケーブルカー・リフト（往復）、丹海バス（宮津駅〜天橋立駅前〜天橋立ケーブル下〜伊根湾めぐり・日出〜伊根）、伊根湾めぐり遊覧船、京都丹後鉄道（特急は普通車自由席）",
                "Covers: Amanohashidate sightseeing boat (Miyazu–Amanohashidate–Ichinomiya piers), cable car & chairlift (round trip), Tankai bus (Miyazu Sta.–Amanohashidate Sta.–Cable-shita–Ine-wan Meguri Hide–Ine), Ine Bay boat, Kyoto Tango Railway (non-reserved seats on expresses)"),
            row("pass", "売っている場所：京都丹後鉄道の駅の窓口（駅員のいる駅）、天橋立桟橋の観光船乗り場、宮津桟橋",
                "Sold at: Kyoto Tango Railway station ticket windows (staffed stations), the boat office on Amanohashidate pier, and Miyazu pier"),
        ], "丹後海陸交通 公式「お得なチケット」（https://www.tankai.jp/tourist_tickets/）。2026-11-22・2026-11-24に確認。切符販売場所は「宮津案内所・宮津桟橋／旅客船営業所 天橋立桟橋／京都丹後鉄道（対象路線内の有人駅）」。駅の観光案内所は一覧になく、天橋立観光協会の「お得なチケット」（https://www.amanohashidate.jp/blog/ticket/）にもこのフリーパスは載っていない（2026-11-24確認）ので、案内所での販売は書かない",
            tip=T("京都からの特急はしだての料金は含まれません。",
                  "The Hashidate express from Kyoto isn’t covered.")),
    }

    S["chionji"] = {
        "name": T("智恩寺（文殊堂）", "Chion-ji Temple (Monju-do)"),
        "kind": T("お寺", "Temple"),
        "blurb": T("「三人寄れば文殊の知恵」の文殊さま。松の枝に結ばれた白い扇子のおみくじが、花が咲いたようです。",
                   "Home of Monju, the bodhisattva of wisdom. Fan-shaped fortunes tied to the pine branches look like white flowers."),
        "lat": 35.557877, "lng": 135.184531,
        "text": T(
            "智恩寺（ちおんじ）\n\n「三人寄れば文殊の知恵」の文殊菩薩をまつる、日本三文殊のひとつ。駅から歩いて5分、観光船の乗り場はお寺のすぐ横です。\n\n境内の松には、扇の形の「すえひろ扇子おみくじ」がたくさん結ばれています。参道の茶屋の名物は「智恵の餅」。\n\n11:00の船まで10分ほどなので、ここは短めに。帰りの船を降りたあとにも寄れます（お守り・おみくじは17:00まで）。\n\nおすすめ訪問時間：10:45〜10:55",
            "Chion-ji Temple\n\nOne of Japan’s three great temples of Monju, the bodhisattva of wisdom (as in the saying “three heads are better than one”). It is 5 minutes on foot from the station, and the boat pier is right beside it.\n\nThe pine trees in the grounds are covered with “suehiro” fan-shaped fortunes. The tea houses on the approach sell “chie no mochi” rice cakes.\n\nYou have about 10 minutes before the 11:00 boat, so keep it short. You can come back after the return boat (charms and fortunes until 17:00).\n\nRecommended visit time: 10:45–10:55"),
        "gmaps": [gm("智恩寺", "Chion-ji", 35.557877, 135.184531, "智恩寺 宮津")],
        "links": [link("official", "天橋山 智恩寺 公式サイト", "Chion-ji official site (Japanese)", "https://www.monjudo-chionji.jp/")],
        "info": info([row("hours", "本堂の授与所（お守り・おみくじ）8:00〜17:00", "Main hall counter (charms, fortunes): 8:00–17:00")],
                     "智恩寺 公式サイト。2026-11-20に確認（22日は見直していない）", checked=D20),
    }

    after_cross_ja = ("一の宮桟橋から籠神社（5番）へは歩いて3分ほどです。\n\n土日祝の11:00の船は、廻旋橋と運河をめぐる22分のコースで、11:22に着きます。このあとの予定が10分ずつ遅れますが、13:29のバスには十分間に合います。\n\n特急が遅れて11:00の船に乗れなかったら、11:30の船で。" if A else
                      "平日：一の宮桟橋（11:12着）から200mほど先の「天橋立ケーブル下」バス停へ歩き、11:24発のバスで伊根へ（伊根湾めぐり・日出に11:53着）。乗り遅れたら次は12:08発（12:37着）です。\n\n土日祝：11:00の船は廻旋橋と運河をめぐる22分のコースで、11:22着。11:24のバスには間に合いません。次のどちらかにしてください。\n・船に乗らず、天橋立駅のバス停を10:58に出る同じバスで伊根へ（11:53着）。天橋立は帰りに船で渡り、智恩寺は船を降りてからお参りします。\n・11:00の船に乗り、待ち時間に籠神社（8番）をお参りして、神社前のバス停「天橋立元伊勢籠神社」から12:10発のバスに乗る（12:37着）。お昼は13:45ごろになります。")
    after_cross_en = ("From Ichinomiya pier, Kono Shrine (stop 5) is about 3 minutes on foot.\n\nOn weekends and holidays the 11:00 boat takes the 22-minute route via the turning bridge and canal, arriving at 11:22. Everything after runs 10 minutes later, still in good time for the 13:29 bus.\n\nIf the express is late and you miss the 11:00 boat, take the 11:30." if A else
                      "Weekdays: from Ichinomiya pier (arr. 11:12), walk about 200 m to the “Amanohashidate Cable-shita” stop and take the 11:24 bus to Ine (Ine-wan Meguri Hide 11:53). If you miss it, the next is 12:08 (arr. 12:37).\n\nWeekends and holidays: the 11:00 boat takes the 22-minute route via the turning bridge and canal and arrives at 11:22, too late for the 11:24 bus. Do one of these instead.\n- Skip the boat and take the same bus from the Amanohashidate Station stop at 10:58 (Ine 11:53). Cross Amanohashidate by boat on the way back, and visit Chion-ji after you get off.\n- Take the 11:00 boat, visit Kono Shrine (stop 8) while you wait, then take the 12:10 bus from the “Amanohashidate Motoise Kono-jinja” stop in front of the shrine (arr. 12:37). Lunch will be around 13:45.")
    S["crossing"] = {
        "name": T("天橋立を渡る（観光船か自転車で）", "Crossing Amanohashidate (boat or bike)"),
        "kind": T("観光船・レンタサイクル", "Boat or rental bike"),
        "blurb": T("智恩寺の横から観光船で12分。自転車なら松並木の中を15〜20分で、対岸の府中へ。",
                   "From the pier by Chion-ji: 12 minutes by boat, or 15–20 minutes by bike through the pines, to Fuchu on the far side."),
        "lat": 35.558543, "lng": 135.184739,
        "caution": (T("風や波の強い日は船が止まります", "Boats stop in strong wind or waves") if A else
                    T("土日祝は11:00の船だと11:24のバスに乗れません", "Weekends: the 11:00 boat misses the 11:24 bus")),
        "notices": [notice("船が止まっていたら", "If the boats aren’t running",
                           "風や波の強い日は運航中止になります。そのときは天橋立駅のバス停から丹海バスで「天橋立ケーブル下」へ（10:58発→11:24着、次は11:42発→12:08着。フリーパスで乗れます）。雨の日は自転車を借りられないことがあります。",
                           "Boats are cancelled in strong wind or waves. In that case take the Tankai bus from the Amanohashidate Station stop to “Amanohashidate Cable-shita” (10:58 → 11:24, then 11:42 → 12:08; covered by the free pass). Bikes may not be rented out on rainy days.",
                           url=TANKAI_BOAT)],
        "text": T(
            "天橋立（あまのはしだて）を渡る\n\n日本三景のひとつ、宮津湾と阿蘇海（あそかい）を分ける長さ3.6kmの砂の道です。観光船か自転車で、対岸の府中（ふちゅう）へ渡ります。\n\n観光船（フリーパスで乗れます）は智恩寺の横の天橋立桟橋から出て、約12分で一の宮桟橋へ。出てすぐ、廻旋橋（かいせんきょう）が回って船を通します。カモメが船と並んで飛ぶので、エサやりもできます。\n\n自転車は天橋立桟橋で借りて、松並木の中を15〜20分。対岸の一の宮桟橋で返せます（2時間500円。フリーパスには含まれず、予約はできません）。\n\n" + after_cross_ja + "\n\nおすすめ移動時間：11:00（観光船）",
            "Crossing Amanohashidate\n\nOne of Japan’s Three Scenic Views: a 3.6 km sandbar between Miyazu Bay and the Aso Sea. Cross it by boat or by bike to Fuchu on the far side.\n\nThe sightseeing boat (covered by the free pass) leaves Amanohashidate pier, beside Chion-ji, and reaches Ichinomiya pier in about 12 minutes. Just after leaving, the Kaisenkyo bridge swings open for the boat. Seagulls fly alongside, and you can feed them.\n\nBikes are rented at Amanohashidate pier: 15–20 minutes through the pines, and you can drop the bike at Ichinomiya pier (¥500 for 2 hours; not covered by the free pass, no reservations).\n\n" + after_cross_en + "\n\nRecommended travel time: 11:00 (boat)"),
        "gmaps": [gm("天橋立桟橋（観光船・レンタサイクル）", "Amanohashidate pier (boat & bikes)", 35.558543, 135.184739, "天橋立観光船 天橋立桟橋")],
        "links": [
            link("timetable", "天橋立観光船（時刻表・料金）", "Sightseeing boat: times & fares (Japanese)", TANKAI_BOAT),
            link("official", "レンタサイクル（丹後海陸交通）", "Rental bikes (Tankai, Japanese)", "https://www.tankai.jp/trip/bicycle/"),
        ] + ([] if A else [link("timetable", "丹海バス 時刻表（伊根・蒲入線）", "Tankai bus timetable (Ine line, Japanese)", TANKAI_BUS)]),
        "info": info([
            row("hours", "観光船 天橋立桟橋発 9:00、10:00〜16:00は毎時0分・30分（3〜10月は17:00、4〜9月は17:30も）。約12分。土日祝の11:00〜15:00の0分発は、廻旋橋と運河をめぐる22分のコース",
                "Boats from Amanohashidate pier: 9:00, then on the hour and half hour 10:00–16:00 (also 17:00 Mar–Oct, 17:30 Apr–Sep); about 12 min. On weekends and holidays, the on-the-hour boats 11:00–15:00 take a 22-minute route via the turning bridge and canal"),
            row("fee", "観光船 片道800円・往復1,300円（フリーパスで乗れます）。レンタサイクル2時間500円（延長は1時間ごとに300円）",
                "Boat ¥800 one way, ¥1,300 round trip (covered by the free pass). Rental bike ¥500 for 2 hours (¥300 per extra hour)"),
        ] + ([] if A else [row("bus", "天橋立駅→天橋立ケーブル下→伊根湾めぐり・日出：10:58→11:24→11:53／11:42→12:08→12:37（毎日）。フリーパスで乗れます（なければケーブル下から200円、天橋立駅から400円）",
                               "Amanohashidate Sta. → Cable-shita → Ine-wan Meguri Hide: 10:58→11:24→11:53 / 11:42→12:08→12:37 (daily). Covered by the free pass (otherwise ¥200 from Cable-shita, ¥400 from the station)")]),
            "丹後海陸交通 公式（天橋立観光船の時刻表・運賃・運航中止の基準、レンタサイクル、伊根・蒲入線の時刻表）。2026-11-22に確認。レンタサイクル（https://www.tankai.jp/trip/bicycle/）は2026-11-24にも確認：天橋立桟橋・一の宮桟橋で貸出、2時間500円・1時間ごとに300円、予約不可、雨天は断ることあり、カード・電子マネー可（商品により不可）。窓口の時間は公式サイト・よくある質問・お得なチケットのどれにも記載なし（要確認）"),
    }

    S["kono"] = {
        "name": T("元伊勢 籠神社", "Motoise Kono Shrine"),
        "kind": T("神社", "Shrine"),
        "blurb": T("伊勢神宮の神さまが、伊勢へ移る前にまつられていたと伝わる「元伊勢」。",
                   "Known as “Moto-Ise”: the gods of Ise Grand Shrine are said to have been worshipped here before moving to Ise."),
        "lat": 35.582586, "lng": 135.196863,
        "caution": T("門は17:00まで。お守りは16:30まで", "Gates close 17:00; charm counter 16:30"),
        "text": T(
            "元伊勢 籠神社（このじんじゃ）\n\n天橋立を渡りきった府中にある、丹後国の一宮（いちのみや）。今は伊勢神宮にまつられている天照大御神（あまてらすおおみかみ）と豊受大御神（とようけのおおみかみ）が、昔この地にまつられていたと伝わり、「元伊勢」と呼ばれます。参道の鳥居は伊勢神宮と同じ形です。\n\n" +
            ("一の宮桟橋から歩いて3分ほど。お参りしたら、すぐ隣の府中駅から11:45のケーブルカーで傘松公園へ（土日祝は12:00）。\n\nおすすめ訪問時間：11:15〜11:40（土日祝は11:25〜11:50）" if A else
             "伊根からのバスは、「天橋立ケーブル下」のひとつ手前の「天橋立元伊勢籠神社」で降ります（伊根15:08発→15:39着）。先にお参りして、すぐ隣の府中駅から16:00のケーブルカーで傘松公園へ。土日祝に行きの待ち時間でお参りした人は、そのまま「天橋立ケーブル下」まで乗って15:45のケーブルカーへ。\n\nおすすめ訪問時間：15:40〜15:55"),
            "Motoise Kono Shrine\n\nThe most important shrine of old Tango Province, in Fuchu at the far end of Amanohashidate. Amaterasu and Toyouke, the deities now enshrined at Ise Grand Shrine, are said to have been worshipped here first, which is why it’s called “Moto-Ise” (the original Ise). The torii on the approach is in the same style as Ise’s.\n\n" +
            ("About 3 minutes on foot from Ichinomiya pier. After your visit, take the 11:45 cable car up to Kasamatsu Park from Fuchu Station next door (12:00 on weekends and holidays).\n\nRecommended visit time: 11:15–11:40 (weekends and holidays 11:25–11:50)" if A else
             "Get off the bus from Ine at “Amanohashidate Motoise Kono-jinja”, one stop before “Cable-shita” (Ine 15:08 → 15:39). Visit the shrine first, then take the 16:00 cable car to Kasamatsu Park from Fuchu Station next door. If you already visited while waiting on a weekend morning, stay on to “Cable-shita” for the 15:45 cable car.\n\nRecommended visit time: 15:40–15:55")),
        "gmaps": [gm("元伊勢 籠神社", "Motoise Kono Shrine", 35.582586, 135.196863, "元伊勢籠神社")],
        "links": [link("official", "元伊勢 籠神社 公式サイト", "Kono Shrine official site (Japanese)", "https://www.motoise.jp/")],
        "info": info([row("hours", "開門 8:00〜17:00（変わることがあります）。授与所 8:30〜16:30（御朱印は9:00から）",
                          "Gates open 8:00–17:00 (may change). Charm counter 8:30–16:30 (goshuin from 9:00)")],
                     "元伊勢 籠神社 公式サイト。2026-11-22に確認"),
    }

    S["kasamatsu"] = {
        "name": T("天橋立傘松公園", "Amanohashidate Kasamatsu Park"),
        "kind": T("展望台", "Viewpoint"),
        "blurb": T("ケーブルカーかリフトで山の上へ。天に昇る龍のような「昇龍観」と、股のぞき発祥の地です。",
                   "Up by cable car or chairlift for the “rising dragon” view. Bend over and look at it upside down between your legs: the custom started here."),
        "lat": 35.586553, "lng": 135.195928,
        "caution": (T("山の上の駅は現金のみ。切符は下の府中駅で", "Cash only at the top station: buy tickets at the bottom") if A else
                    T("リフトは16:00まで。16:45の船に乗るなら16:30のケーブルカーで下ります", "Chairlift ends 16:00. For the 16:45 boat, take the 16:30 cable car down")),
        "text": T(
            "天橋立傘松公園（かさまつこうえん）\n\n籠神社のすぐ横の府中駅から、ケーブルカー（約4分、15分ごと）かリフト（約8分）で上ります。フリーパスで乗れます。ここからの天橋立は、龍が天に昇るように見える「昇龍観（しょうりゅうかん）」。股のぞき台で逆さまにのぞくと、橋が空に架かって見えます。\n\n" +
            ("上りはケーブルカー、下りはリフトにすると、天橋立を正面に見ながら下りられます（切符は共通）。\n\nお昼はここで。展望施設「AmaTerrace（アマテラス）」に、レストラン「アマダイニング」（そば・うどん1,200円、海鮮丼2,500円など）とカフェ「アマカフェ」があります。12時を過ぎると席が埋まりやすいので、上に着いたら先に食べるのがおすすめです。\n\n13:10ごろまでに下りて、「天橋立ケーブル下」バス停から13:29発のバスで伊根へ（伊根湾めぐり・日出に13:58着）。乗り遅れると次は14:24発（14:53着）で、伊根は15:00の遊覧船と舟屋の町を少し歩くだけになります。\n\nおすすめ訪問時間：11:45〜13:15" if A else
             "16:00のケーブルカーで上ります。リフトは16:00で終わるので、上りも下りもケーブルカーです。上には30分ほど。16:30のケーブルカーで下りると、歩いて5分ほどの一の宮桟橋から16:45の船に乗れます。\n\n船に乗り遅れても、「天橋立ケーブル下」17:20発のバスで天橋立駅に17:47に着き、18:09の特急に間に合います（フリーパスで乗れます）。3〜10月は17:15の船もあります。\n\n展望施設「AmaTerrace（アマテラス）」には、カフェ「アマカフェ」もあります。\n\nおすすめ訪問時間：16:00〜16:30"),
            "Amanohashidate Kasamatsu Park\n\nFrom Fuchu Station, right next to Kono Shrine, ride the cable car (about 4 min, every 15 min) or the chairlift (about 8 min) up the hill; both are covered by the free pass. From here Amanohashidate looks like a dragon rising into the sky, the “Shoryukan” view. Look at it upside down between your legs from the “matanozoki” stand and the sandbar seems to hang in the sky.\n\n" +
            ("Go up by cable car and come down by chairlift, and you face Amanohashidate all the way down (same ticket).\n\nHave lunch here. AmaTerrace, the viewing building, has a restaurant, AmaDining (soba or udon ¥1,200, seafood rice bowl ¥2,500, for example), and a café, AmaCafe. Seats tend to fill after noon, so eat as soon as you get to the top.\n\nBe down by about 13:10 and take the 13:29 bus to Ine from the “Amanohashidate Cable-shita” stop (Ine-wan Meguri Hide 13:58). If you miss it, the next is 14:24 (arr. 14:53), which leaves time only for the 15:00 boat and a short walk in the village.\n\nRecommended visit time: 11:45–13:15" if A else
             "Take the 16:00 cable car up. The chairlift stops at 16:00, so it’s the cable car both ways. You get about 30 minutes at the top. The 16:30 cable car down gets you to Ichinomiya pier, about 5 minutes on foot, for the 16:45 boat.\n\nIf you miss the boat, the 17:20 bus from “Amanohashidate Cable-shita” reaches Amanohashidate Station at 17:47, in time for the 18:09 express (covered by the free pass). From March to October there is also a 17:15 boat.\n\nAmaTerrace, the viewing building at the top, also has a café, AmaCafe.\n\nRecommended visit time: 16:00–16:30")),
        "gmaps": [gm("府中駅（ケーブルカー乗り場）", "Fuchu Station (cable car)", 35.58323, 135.1953, "天橋立ケーブルカー 府中駅")],
        "links": [
            link("official", "天橋立ケーブルカー・リフト（運行時間・運賃・乗り方）", "Cable car & lift: times and fares (Japanese)", "https://www.tankai.jp/trip/cable/"),
            link("official", "AmaTerrace（アマテラス）", "AmaTerrace (Japanese)", "https://www.tankai.jp/trip/amaterrace/"),
            link("timetable", "丹海バス 時刻表（伊根・蒲入線）", "Tankai bus timetable (Ine line, Japanese)", TANKAI_BUS),
        ],
        "info": info([
            row("hours", "ケーブルカー 9:00〜、15分ごと（最終は3〜10月18:00、11月・2月17:30、12〜1月17:00）。リフト 9:00〜16:00（12月1日〜1月5日は10:00から、1月6日〜2月末は土日祝だけ。天気や整備で止まることがあります）",
                "Cable car from 9:00, every 15 min (last car 18:00 Mar–Oct, 17:30 Nov & Feb, 17:00 Dec–Jan). Chairlift 9:00–16:00 (from 10:00 Dec 1–Jan 5; weekends and holidays only Jan 6–end of Feb; may stop for weather or maintenance)"),
            row("fee", "ケーブルカー・リフト共通 往復 大人800円・小児400円（フリーパスで乗れます）。公園は無料",
                "Cable car / lift round trip ¥800 (children ¥400), covered by the free pass. The park itself is free"),
        ] + ([row("bus", "天橋立ケーブル下→伊根湾めぐり・日出：13:29→13:58、14:24→14:53（毎日）。フリーパスで乗れます（なければ200円）",
                  "Amanohashidate Cable-shita → Ine-wan Meguri Hide: 13:29→13:58, 14:24→14:53 (daily). Covered by the free pass (otherwise ¥200)")] if A else
             [row("bus", "天橋立ケーブル下→天橋立駅：17:20→17:47、18:27→18:54（毎日）。フリーパスで乗れます",
                  "Amanohashidate Cable-shita → Amanohashidate Sta.: 17:20→17:47, 18:27→18:54 (daily). Covered by the free pass")]),
            "丹後海陸交通 公式（ケーブルカー・リフト、傘松公園、AmaTerrace、伊根・蒲入線の時刻表、12月18日休業のお知らせ）。2026-11-22に確認。AmaTerrace（https://www.tankai.jp/trip/amaterrace/、2026-11-24に確認）：レストラン「アマダイニング」・カフェ「アマカフェ」・1Fにショップ（1Fは傘松公園のページ）。営業時間 9:00〜18:00（季節により変動）。メニュー例 傘松そば・うどん1,200円、おまかせ海鮮丼2,500円。キャッシュレス（クレジットカード・電子マネー・QRコード決済）可。食事の時間・ラストオーダーは記載なし＝要確認。前の版の「2階が食事」は公式で確かめられないので外した。ケーブルカー最終下り 3〜10月18:00・12〜1月17:00・2月と11月17:30、リフト16:00まで（よくある質問 https://www.tankai.jp/trip/faq）",
            tip=T("山の上の傘松駅では現金しか使えません。切符は下の府中駅で買うと、カードや電子マネーも使えます。AmaTerrace の店ではカード・電子マネー・QRコード決済が使えます。食事のラストオーダーは公式サイトに載っていません（要確認）。",
                  "Kasamatsu Station at the top takes cash only. Buy tickets at Fuchu Station at the bottom, where cards and e-money work. AmaTerrace takes cards, e-money and QR payments. Its last-order time isn’t given on the official site, so check on the day.")),
        "notices": [notice("12月18日は休み", "Closed on December 18",
                           "2026年12月18日（金）は工事のため、ケーブルカー・リフト・アマテラスがすべて休みです。",
                           "On Friday, Dec 18, 2026 the cable car, chairlift and AmaTerrace are all closed for construction work.",
                           url="https://www.tankai.jp/news/42473/", to="2026-12-18")],
    }

    S["ineboat"] = {
        "name": T("伊根湾めぐり遊覧船", "Ine Bay Sightseeing Boat"),
        "kind": T("遊覧船", "Boat ride"),
        "blurb": T("海の上から舟屋の並ぶ町を眺める25分の船旅。船のまわりをカモメがいっしょに飛びます。",
                   "A 25-minute cruise past Ine’s boathouses, with seagulls flying right alongside."),
        "lat": 35.6704, "lng": 135.2772,
        "caution": T("最終は16:00。風や波の強い日は欠航", "Last boat 16:00; cancelled in strong wind or waves"),
        "text": T(
            "伊根湾めぐり遊覧船\n\nバスを「伊根湾めぐり・日出（ひで）」で降りると、目の前が乗り場です（フリーパスで乗れます）。毎時0分と30分に出て、約25分で伊根湾を一周。1階が船のガレージになった舟屋（ふなや）が海のすぐ上に並ぶ景色を、海側から見られます。カモメのエサは乗り場と船内で売っています。\n\n" +
            ("バスは13:58着。時間どおりなら14:00の船に乗れますが、2分しかないので、14:30の船のつもりでいてください。待つあいだは、乗り場の横の日出の入り江へ。水が透き通っています。\n\n降りたら、湾ぞいの道を15分ほど歩いて向井酒造（8番）へ。\n\nおすすめ訪問時間：14:30〜14:55（間に合えば14:00〜14:25）" if A else
             "11:53に着いたら12:00の船へ（間に合わなければ12:30）。12:37に着いた日は13:00の船に。\n\n降りたら、湾ぞいの道を15分ほど歩いて平田（ひらた）へ。お昼ごはんの場所は7番に書いています。乗り場にも軽食の売店があります。\n\nおすすめ訪問時間：12:00〜12:25（12:37に着いた日は13:00〜13:25）"),
            "Ine Bay Sightseeing Boat\n\nGet off the bus at “Ine-wan Meguri Hide” and the pier is right in front of you (covered by the free pass). Boats leave on the hour and half hour and loop around Ine Bay in about 25 minutes, with the funaya — houses with a boat garage on the ground floor — lined up right on the water. Gull food is sold at the pier and on board.\n\n" +
            ("The bus arrives at 13:58. If it’s on time you can make the 14:00 boat, but that’s only 2 minutes, so plan on the 14:30. While you wait, look at the cove at Hide next to the pier: the water is very clear.\n\nAfterwards, walk about 15 minutes along the bay to Mukai Sake Brewery (stop 8).\n\nRecommended visit time: 14:30–14:55 (14:00–14:25 if you make it)" if A else
             "Arriving at 11:53, take the 12:00 boat (or the 12:30 if you miss it). Arriving at 12:37, take the 13:00.\n\nAfterwards, walk about 15 minutes along the bay to Hirata. Where to have lunch is under stop 7. There is also a snack counter at the pier.\n\nRecommended visit time: 12:00–12:25 (13:00–13:25 if you arrive at 12:37)")),
        "gmaps": [gm("伊根湾めぐり遊覧船 日出乗り場", "Ine Bay boat pier (Hide)", 35.6704, 135.2772, "伊根湾めぐり遊覧船")],
        "links": [link("official", "伊根湾めぐり遊覧船（丹後海陸交通）", "Ine Bay Sightseeing Boat (Tankai, Japanese)", "https://www.tankai.jp/trip/ineboat/")],
        "info": info([
            row("hours", "9:00〜16:00、毎時0分・30分に出航（約25分）", "9:00–16:00, departing on the hour and half hour (about 25 min)"),
            row("closed", "年中無休（風や波の強い日は運航を見合わせます）", "Open every day (suspended in strong wind or waves)"),
            row("fee", "大人1,200円（中学生以上）・小学生600円（フリーパスで乗れます）。乗り場ではクレジットカード・電子マネーも使えます",
                "¥1,200 (junior high and up), ¥600 (elementary); covered by the free pass. Cards and e-money are accepted at the pier"),
        ], "丹後海陸交通 公式（伊根湾めぐり遊覧船）。2026-11-22に確認"),
    }

    S["mukai"] = {
        "name": T("向井酒造", "Mukai Sake Brewery"),
        "kind": T("酒蔵", "Sake brewery"),
        "blurb": T("「海に一番近い酒蔵」。古代米で造る赤いお酒「伊根満開」で知られる、舟屋の町の酒蔵です。",
                   "“The sake brewery closest to the sea”, known for Ine Mankai, a red sake made with ancient rice."),
        "lat": 35.674754, "lng": 135.286395,
        "text": T(
            "向井酒造（むかいしゅぞう）\n\n遊覧船乗り場から湾ぞいの道を15分ほど歩いた、舟屋の町・平田（ひらた）の酒蔵です。お酒はすべて純米酒。いちばん知られているのは、古代米（紫黒米）で造る赤いお酒「伊根満開（いねまんかい）」で、甘酸っぱい味です。直売所で買えます。\n\n木曜と、12:00〜13:00の昼休みは閉まっています。" +
            ("\n\nおすすめ訪問時間：15:10〜15:25" if A else "お昼ごはんのあと、13時を過ぎてから寄ります。\n\nおすすめ訪問時間：13:35〜13:50"),
            "Mukai Sake Brewery\n\nAbout 15 minutes on foot along the bay from the boat pier, in Hirata, the boathouse village. Everything they brew is junmai (pure rice) sake. The best known is Ine Mankai, a red sake made with an ancient purple rice: sweet and tart. You can buy it at the brewery shop.\n\nClosed on Thursdays and for lunch from 12:00 to 13:00." +
            ("\n\nRecommended visit time: 15:10–15:25" if A else " Come after lunch, once it’s past 13:00.\n\nRecommended visit time: 13:35–13:50")),
        "gmaps": [gm("向井酒造", "Mukai Shuzo", 35.674754, 135.286395, "向井酒造 伊根")],
        "links": [link("official", "向井酒造 直売所のご案内", "Mukai Shuzo shop info (Japanese)", "https://www.kuramoto-mukai.jp/%e7%9b%b4%e5%a3%b2%e6%89%80%e3%81%ae%e3%81%94%e6%a1%88%e5%86%85/")],
        "info": info([
            row("hours", "9:00〜12:00 / 13:00〜17:00", "9:00–12:00 / 13:00–17:00"),
            row("closed", "木曜日・年末年始", "Thursdays and New Year holidays"),
        ], "向井酒造 公式サイト（直売所のご案内）。2026-11-22に確認"),
        "caution": T("木曜休み・12:00〜13:00は昼休み", "Closed Thursdays and 12:00–13:00"),
        "_extra": [
            {"file": "mukai-2.jpg", "credit": {"author": "漱石の猫", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:%E5%90%91%E4%BA%95%E9%85%92%E9%80%A0.jpg"}},
            {"file": "mukai-3.jpg", "credit": {"author": "Asturio Cantabrio", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:Ine_Mukai_Brewery_2021-04_ac_(1).jpg"}},
            {"file": "mukai-4.jpg", "credit": {"author": "Asturio Cantabrio", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:Ine_Mukai_Brewery_2021-04_ac_(2).jpg"}},
        ],
    }

    biyori_ja = "食事と休憩は、同じ平田にある観光交流施設「舟屋日和（ふなやびより）」が使いやすいです（「伊根」バス停から歩いて8分。舟屋日和の案内）。INE CAFE（平日10:30〜17:00、土日祝は17:30まで）と、鮨割烹 海宮（わだつみ。昼は11:00〜14:30、ラストオーダー14:00）があり、どちらも水曜休み。ランチは数に限りがあり、休む日もあります。水曜に行く人は、伊根町観光協会のサイトの「食べる」で開いている店を確かめてください。"
    biyori_en = "For food and a rest, Funaya Biyori, a visitor facility also in Hirata, is the easiest (8 minutes on foot from the “Ine” bus stop, according to the facility): INE CAFE (weekdays 10:30–17:00, until 17:30 on weekends and holidays) and the sushi restaurant Wadatsumi (lunch 11:00–14:30, last order 14:00). Both close on Wednesdays; lunch is limited in number and not served every day. If you go on a Wednesday, check the “Eat” page of the Ine Tourist Association for what’s open."
    S["funaya"] = {
        "name": T("伊根の舟屋（伊根浦）", "Ine’s Funaya Boathouses"),
        "kind": T("町並み", "Historic district"),
        "blurb": T("海の上に建つ約230軒の舟屋。湖のように静かな湾ぞいを、のんびり歩きます。",
                   "About 230 boathouses built right on the water. Stroll along a bay as calm as a lake."),
        "lat": 35.675733, "lng": 135.287658,
        "caution": (T("帰りのバスは16:00。次は16:47", "Bus back at 16:00; the next is 16:47") if A else
                    T("バスは15:08。次は16:00・水曜は舟屋日和が休み", "Bus at 15:08, next 16:00 · Funaya Biyori closed Wed")),
        "notices": [notice("舟屋は人の家です", "The funaya are people’s homes",
                           "舟屋も母屋も敷地も個人のものです。中や敷地に入らず、洗濯物や人が写らないように撮ってください。",
                           "The boathouses, the houses and the land around them are private. Don’t go in, and keep laundry and people out of your photos.",
                           url="https://www.ine-kankou.jp/")],
        "text": T(
            "伊根の舟屋（ふなや）\n\n1階が海に開いた船のガレージ、2階が住まいの舟屋が、伊根湾にそって約230軒並びます。国の重要伝統的建造物群保存地区です。向井酒造のすぐ先が伊根浦公園と観光案内所で、「伊根」バス停もここです。\n\n" +
            ("向井酒造を出たら、伊根浦公園のあたりから舟屋を眺めます。14:00の船に乗れた日は30分ほど余裕があるので、舟屋日和でひと休みを。" + biyori_ja + "\n\n帰りは「伊根」16:00発のバスで「天橋立ケーブル下」へ（16:33着）。乗り遅れたら次は16:47発で、船には間に合いません。そのまま天橋立駅まで乗れば17:47に着き、18:09の特急に乗れます。その次の17:56発だと天橋立駅18:54着で、19:05の特急になります。\n\nおすすめ訪問時間：15:25〜15:55" if A else
             "お昼ごはん：遊覧船を降りて、湾ぞいの道を向井酒造の前を通って舟屋日和まで歩くと20分ほど（地図で見た目安）。12:45〜12:50ごろに着きます。" + biyori_ja + "\n\n食べたら向井酒造（6番）に寄り、伊根浦公園のあたりまで歩いて舟屋を眺めます。\n\n「伊根」15:08発のバスで「天橋立元伊勢籠神社」へ（15:39着）。乗り遅れたら次は16:00発（天橋立ケーブル下16:33着）。その場合は籠神社をやめて16:45のケーブルカーで傘松公園に上り、17:20のバスで天橋立駅へ戻ります（17:47着）。\n\nおすすめ訪問時間：12:45〜15:05（お昼ごはんを含む）"),
            "Ine’s Funaya\n\nAbout 230 funaya line Ine Bay: the ground floor is a garage that opens onto the sea for a boat, and people live upstairs. The village is a national Preservation District for Groups of Traditional Buildings. Just past Mukai Sake Brewery are Ine-ura Park and the tourist information center, where the “Ine” bus stop is.\n\n" +
            ("After the brewery, look out over the funaya from around Ine-ura Park. If you made the 14:00 boat you have about 30 minutes to spare for a break at Funaya Biyori. " + biyori_en + "\n\nGo back on the 16:00 bus from “Ine” to “Amanohashidate Cable-shita” (arr. 16:33). If you miss it, the next is 16:47, too late for the boat: stay on to Amanohashidate Station (17:47) for the 18:09 express. The one after, 17:56, reaches the station at 18:54, which means the 19:05 express.\n\nRecommended visit time: 15:25–15:55" if A else
             "Lunch: from the boat, walk along the bay past Mukai Sake Brewery to Funaya Biyori, about 20 minutes (a map estimate); you arrive around 12:45–12:50. " + biyori_en + "\n\nAfter eating, stop at Mukai Sake Brewery (stop 6) and walk on to Ine-ura Park for the view of the funaya.\n\nTake the 15:08 bus from “Ine” to “Amanohashidate Motoise Kono-jinja” (arr. 15:39). If you miss it, the next is 16:00 (Cable-shita 16:33): skip the shrine, take the 16:45 cable car up to Kasamatsu Park, and go back to Amanohashidate Station on the 17:20 bus (arr. 17:47).\n\nRecommended visit time: 12:45–15:05 (including lunch)")),
        "gmaps": [gm("伊根浦公園", "Ine-ura Park", 35.675733, 135.287658, "伊根浦公園"),
                  gm("舟屋日和", "Funaya Biyori", 35.67384, 135.29075, "舟屋日和 伊根町平田")],
        "links": [
            link("info", "伊根町観光協会", "Ine Tourist Association", "https://www.ine-kankou.jp/"),
            link("official", "舟屋日和（INE CAFE・鮨割烹 海宮）", "Funaya Biyori: INE CAFE & Wadatsumi (Japanese)", "https://funayabiyori.com/food/"),
            link("timetable", "丹海バス 時刻表（伊根・蒲入線）", "Tankai bus timetable (Ine line, Japanese)", TANKAI_BUS),
        ],
        "info": info([BUS_BACK,
                      row("hours", "舟屋日和：INE CAFE 平日10:30〜17:00（ラストオーダー16:30）、土日祝は17:30まで。鮨割烹 海宮 11:00〜14:30（ラストオーダー14:00）・17:00〜20:30",
                          "Funaya Biyori: INE CAFE weekdays 10:30–17:00 (last order 16:30), until 17:30 on weekends and holidays. Wadatsumi 11:00–14:30 (last order 14:00) and 17:00–20:30"),
                      row("closed", "舟屋日和：水曜日（海宮はほかにも休みあり。ランチは不定休・数量限定）",
                          "Funaya Biyori: Wednesdays (Wadatsumi has other closed days; lunch is limited and not served every day)")],
                     BUS_SRC + "。舟屋日和は公式サイト（https://funayabiyori.com/food/、2026-11-22・24に確認）：伊根町字平田593番地1、バス停「伊根」より徒歩8分（トップのアクセス）。地図の位置は公式サイトの Google map のリンク先（35.67384, 135.29075）。遊覧船乗り場から舟屋日和までの20分は地図で見た目安。舟屋のマナーは伊根町観光協会。2026-11-22に確認",
                     tip=T("バスはタッチ決済・QRコード決済も使えますが、交通系ICカード（ICOCAなど）は使えません。",
                           "The bus takes contactless credit cards and QR payments, but not transit IC cards like ICOCA.")),
    }

    S["return"] = {
        "name": T("天橋立を渡って戻る（観光船か自転車で）", "Back across Amanohashidate (boat or bike)"),
        "kind": T("観光船・レンタサイクル", "Boat or rental bike"),
        "blurb": T("一の宮桟橋から、16:45の観光船で天橋立駅側へ。11〜2月はこれが最後の船です。",
                   "The 16:45 boat from Ichinomiya pier back to the station side: the last boat of the day from November to February."),
        "lat": 35.580862, "lng": 135.196014,
        "caution": T("11〜2月は16:45が最後の船", "Nov–Feb: 16:45 is the last boat"),
        "text": T(
            "天橋立を渡って戻る\n\n" +
            ("伊根からのバスを「天橋立ケーブル下」で降りて（16:33着）、歩いて5分ほどの一の宮桟橋へ。バスが遅れて16:45の船に間に合いそうにないときは、降りずに天橋立駅まで乗ってください（17:00着）。" if A else "16:30のケーブルカーで下りたら、歩いて5分ほどの一の宮桟橋へ。間に合わなければ「天橋立ケーブル下」17:20発のバスで天橋立駅へ（17:47着）。") +
            "\n\n16:45発の観光船は16:57に天橋立桟橋に着きます（フリーパスで乗れます）。3〜10月は17:15発、4〜9月は17:45発もあります。桟橋から駅までは歩いて5分ほどです。\n\n自転車で戻るなら、一の宮桟橋で借りて天橋立桟橋で返します（2時間500円）。窓口の閉まる時間は公式サイトに載っていないので、借りるときに聞いてください。冬は17時ごろに暗くなります。\n\nおすすめ移動時間：16:45（観光船）",
            "Back across Amanohashidate\n\n" +
            ("Get off the bus from Ine at “Amanohashidate Cable-shita” (arr. 16:33) and walk about 5 minutes to Ichinomiya pier. If the bus is late and you’d miss the 16:45 boat, stay on to Amanohashidate Station (arr. 17:00)." if A else "After the 16:30 cable car down, walk about 5 minutes to Ichinomiya pier. If you can’t make it, take the 17:20 bus from “Amanohashidate Cable-shita” to Amanohashidate Station (arr. 17:47).") +
            "\n\nThe 16:45 boat reaches Amanohashidate pier at 16:57 (covered by the free pass). There are also boats at 17:15 in Mar–Oct and 17:45 in Apr–Sep. The station is about 5 minutes on foot from the pier.\n\nTo ride back, rent a bike at Ichinomiya pier and return it at Amanohashidate pier (¥500 for 2 hours). The counter’s closing time isn’t on the official site, so ask when you rent. In winter it gets dark around 17:00.\n\nRecommended travel time: 16:45 (boat)"),
        "gmaps": [gm("一の宮桟橋（観光船・レンタサイクル）", "Ichinomiya pier (boat & bikes)", 35.580862, 135.196014, "天橋立観光船 一の宮桟橋")],
        "links": [
            link("timetable", "天橋立観光船（時刻表・料金）", "Sightseeing boat: times & fares (Japanese)", TANKAI_BOAT),
            link("official", "レンタサイクル（丹後海陸交通）", "Rental bikes (Tankai, Japanese)", "https://www.tankai.jp/trip/bicycle/"),
        ],
        "info": info([
            row("hours", "観光船 一の宮桟橋発 9:15、10:15〜16:45は毎時15分・45分（3〜10月は17:15、4〜9月は17:45も）。天橋立桟橋まで約12分",
                "Boats from Ichinomiya pier: 9:15, then at :15 and :45 from 10:15 to 16:45 (also 17:15 Mar–Oct, 17:45 Apr–Sep); about 12 min to Amanohashidate pier"),
            row("bus", "船に乗れなかったら：天橋立ケーブル下→天橋立駅 16:33→17:00、17:20→17:47、18:27→18:54（毎日）。フリーパスで乗れます",
                "If you miss the boat: Amanohashidate Cable-shita → Amanohashidate Sta. 16:33→17:00, 17:20→17:47, 18:27→18:54 (daily). Covered by the free pass"),
            row("fee", "観光船 片道800円（フリーパスで乗れます）。レンタサイクル2時間500円",
                "Boat ¥800 one way (covered by the free pass). Rental bike ¥500 for 2 hours"),
        ], "丹後海陸交通 公式（天橋立観光船・レンタサイクル・伊根・蒲入線の時刻表）。2026-11-22に確認。レンタサイクルの窓口の時間は公式サイト（https://www.tankai.jp/trip/bicycle/、よくある質問、お得なチケット）に記載なし（2026-11-24に再確認、要確認）"),
    }

    S["chienoyu"] = {
        "name": T("天橋立温泉 智恵の湯", "Chie-no-Yu Hot Spring"),
        "kind": T("日帰り温泉（時間があれば）", "Hot spring (if you have time)"),
        "blurb": T("天橋立駅のすぐ横の日帰り温泉。18:09の特急まで、歩き疲れた足を休めて。",
                   "A day-use hot spring right next to the station. Soak your tired legs before the 18:09 express."),
        "lat": 35.557418, "lng": 135.183084,
        "notices": [notice("入れない人・日", "Who can’t enter, and closed days",
                           "入れ墨・タトゥーのある人、お酒を飲んだあとの人は入れません。火・水・木曜は休みです。",
                           "No entry with tattoos or after drinking alcohol. Closed Tuesdays, Wednesdays and Thursdays.",
                           url="https://www.viewland.jp/chienoyu")],
        "text": T(
            "天橋立温泉 智恵の湯（ちえのゆ）\n\n天橋立駅の横の日帰り温泉です。16:57に船で戻ると、18:09の特急まで1時間ほど。17:05ごろ入って、17:55には出ましょう。\n\n入れない日や入らない人は、智恩寺の山門や廻旋橋のあたりを歩いて待てます。\n\nおすすめ訪問時間：17:05〜17:55",
            "Chie-no-Yu Hot Spring\n\nA day-use hot spring next to Amanohashidate Station. Back on the 16:57 boat, you have about an hour before the 18:09 express: go in around 17:05 and be out by 17:55.\n\nOn closed days, or if you’re not bathing, walk around the Chion-ji gate and the turning bridge instead.\n\nRecommended visit time: 17:05–17:55"),
        "gmaps": [gm("天橋立温泉 智恵の湯", "Chie-no-Yu", 35.557418, 135.183084, "天橋立温泉 智恵の湯")],
        "links": [link("official", "天橋立温泉 智恵の湯", "Chie-no-Yu (Japanese)", "https://www.viewland.jp/chienoyu")],
        "info": info([
            row("hours", "12:00〜20:00（入館は18:30まで）", "12:00–20:00 (last entry 18:30)"),
            row("closed", "火曜日・水曜日・木曜日", "Tuesdays, Wednesdays and Thursdays"),
            row("fee", "大人800円（中学生以上）・小学生400円", "¥800 (junior high and up), ¥400 (elementary)"),
        ], "天橋立温泉 智恵の湯 公式ページ（viewland.jp/chienoyu）。2026-11-22に確認。キャリーケースの件は2026-11-20の確認。支払い方法・タオルは記載なし",
            tip=T("キャリーケースの持ち込み・預かりはできません。", "Suitcases can’t be brought in or left here.")),
        "caution": T("火・水・木曜休み・タトゥー不可", "Closed Tue–Thu · no tattoos"),
    }

    S["station2"] = {
        "name": T("天橋立駅（京都へ帰る）", "Amanohashidate Station (back to Kyoto)"),
        "kind": T("駅（ゴール）", "Station (finish)"),
        "blurb": T("18:09の特急はしだて8号で京都へ（20:21着）。晩ごはんは京都駅で。",
                   "The 18:09 Hashidate No. 8 back to Kyoto (arr. 20:21). Dinner at Kyoto Station."),
        "lat": 35.557585, "lng": 135.182426,
        "caution": T("18:09の次は19:05。これが最後の特急", "After 18:09 the next is 19:05, the last express"),
        "text": T(
            "天橋立駅（京都へ帰る）\n\n18:09発の特急はしだて8号で、20:21に京都駅に着きます。乗り遅れたら19:05発のはしだて10号（21:20着）。これが最後の特急で、そのあとは20:13発の普通列車を3回乗り継いで23:38着になります。\n\n車内は約2時間あります。飲み物と軽く食べるものは、乗る前に買っておくと楽です。\n\n晩ごはんは京都駅で。20:21に着いてから入れるのは、\n・京都拉麺小路（きょうとらーめんこうじ）：京都駅ビル10階。22:00まで（ラストオーダー21:30）\n・京都ポルタ：駅前の地下街の「ポルタダイニング」と、11階の「ポルタスカイダイニング」。22:00まで（店によって違います）\n19:05の特急で帰ると21:20着なので、ラストオーダーにはぎりぎりです。\n\n三条のあたりへは、地下鉄烏丸線で烏丸御池まで約6分（220円）です。\n\nおすすめ出発時間：18:09",
            "Amanohashidate Station (back to Kyoto)\n\nThe 18:09 Hashidate No. 8 gets you to Kyoto at 20:21. If you miss it, there is the 19:05 Hashidate No. 10 (Kyoto 21:20). That is the last express; after it, the 20:13 local with three changes arrives at 23:38.\n\nThe ride is about 2 hours, so buy drinks and a snack before boarding.\n\nHave dinner at Kyoto Station. Open after a 20:21 arrival:\n- Kyoto Ramen Koji: 10th floor of the Kyoto Station Building, until 22:00 (last order 21:30)\n- Kyoto Porta: “Porta Dining” in the underground mall in front of the station and “Porta Sky Dining” on the 11th floor, until 22:00 (some shops differ)\nOn the 19:05 express you arrive at 21:20, which is cutting it fine for last orders.\n\nFor the Sanjo area, the Karasuma subway line takes about 6 minutes to Karasuma Oike (¥220).\n\nRecommended departure time: 18:09"),
        "gmaps": [gm("天橋立駅", "Amanohashidate Station", 35.557585, 135.182426, "天橋立駅"),
                  gm("京都拉麺小路（京都駅ビル10階）", "Kyoto Ramen Koji (Kyoto Station Building 10F)", 34.98535, 135.758766, "京都拉麺小路 京都駅ビル")],
        "links": [link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/"),
                  link("official", "京都拉麺小路（京都駅ビル）", "Kyoto Ramen Koji (Japanese)", "https://www.kyoto-station-building.co.jp/ramen_koji/"),
                  link("official", "京都ポルタ", "Kyoto Porta (Japanese)", "https://www.porta.co.jp/")],
        "info": info([
            row("train", "特急はしだて8号 天橋立18:09発→京都20:21着。はしだて10号 19:05発→21:20着（最後の特急）。普通列車は20:13発→京都23:38着（乗り換え3回）",
                "Hashidate No. 8: Amanohashidate 18:09 → Kyoto 20:21. No. 10: 19:05 → 21:20 (last express). Local trains: 20:13 → Kyoto 23:38 (3 changes)"),
            row("fee", "片道 指定席で4,800〜5,200円（日によって変わります）", "One way ¥4,800–5,200 with a reserved seat (depends on the day)"),
            row("hours", "京都駅の晩ごはん：京都拉麺小路 11:00〜22:00（ラストオーダー21:30）。京都ポルタのポルタダイニング・ポルタスカイダイニング 11:00〜22:00（店によって違います）",
                "Dinner at Kyoto Station: Kyoto Ramen Koji 11:00–22:00 (last order 21:30). Kyoto Porta’s Porta Dining and Porta Sky Dining 11:00–22:00 (some shops differ)"),
        ], "特急・普通列車は乗換案内（Yahoo!路線情報。2026年11月28日・12月2日の検索結果）。京都拉麺小路は京都駅ビル 公式、京都ポルタは公式サイトの営業時間。2026-11-22に確認"),
    }

    order = (["kyoto", "station", "chionji", "crossing", "kono", "kasamatsu", "ineboat", "mukai", "funaya", "return", "chienoyu", "station2"] if A else
             ["kyoto", "station", "chionji", "crossing", "ineboat", "mukai", "funaya", "kono", "kasamatsu", "return", "chienoyu", "station2"])
    spots = []
    for i, sid in enumerate(order, 1):
        s = dict(S[sid])
        extra = s.pop("_extra", None)
        out = {"no": i, "id": sid}
        out.update(s)
        out["photos"] = photos(sid, extra)
        out.setdefault("notices", [])
        spots.append(out)
    sections = ([{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 3, "day": 1}, {"first": 4, "last": 4, "day": 2},
                 {"first": 5, "last": 6, "day": 3}, {"first": 7, "last": 9, "day": 4}, {"first": 10, "last": 10, "day": 5},
                 {"first": 11, "last": 12, "day": 6}] if A else
                [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 3, "day": 1}, {"first": 4, "last": 4, "day": 2},
                 {"first": 5, "last": 7, "day": 4}, {"first": 8, "last": 9, "day": 3}, {"first": 10, "last": 10, "day": 5},
                 {"first": 11, "last": 12, "day": 6}])
    return {
        "id": "amanohashidate" if A else "amanohashidate-ine",
        "_note": ("天橋立・伊根マップのデータ（amanohashidate/ のページ専用。形は eizan-line.json と同じ）。回る順番が2通りあり、このファイルは「" +
                  ("傘松公園が先" if A else "伊根が先") +
                  "」の順番（もう一方は " + ("amanohashidate-ine.json" if A else "amanohashidate.json") + "。どちらも scripts/build_amanohashidate_data.py で作る）。"
                  "京都駅から特急はしだてで天橋立へ、天橋立駅の観光案内所で「海の京都 天橋立・伊根フリーパス 1day」を買い、観光船か自転車で府中へ渡り、傘松公園・籠神社と伊根（遊覧船・向井酒造・舟屋）を回って、一の宮桟橋から観光船か自転車で戻り、18:09の特急で京都へ（オーナーの希望 2026-11-20）。2026-11-22 に「ゲストが実際に回れる1日」として見直し：三条のあたりから京都駅までの行き方、乗り遅れたときの次の便、お昼の場所、京都駅での晩ごはんを足した。「伊根が先」は籠神社→傘松公園の順（バスを神社前で降りる）。"
                  "写真は Toshi の写真ライブラリから選んだもの（2023〜2026年の6回分、約4,100枚を全部見て、1か所10枚以内・横の写真だけ・Nikon D7000 を含む。長辺1600px・位置情報なし）。ファイル名はスポットの id。向井酒造の一部の写真は Wikimedia Commons（photos の要素が {file, credit}）。籠神社は神門の外で撮った写真だけを使っている。"
                  "info.checked は事実情報を確認した日（各社・各施設の公式サイト。特急の時刻はJR西日本の時刻表、特急の運賃は乗換案内、バス・観光船の時刻と運賃は丹後海陸交通の時刻表と運賃表）。info.source は出典と確認日の記録（画面には出ない）。notices は from〜to の間だけ表示される。focus は地図を開いたときに映す範囲（京都駅は離れているので入れない）。"),
        "sections": sections,
        "focus": {"first": 2, "last": 12},
        "photoBase": "../images/amanohashidate/",
        "spots": spots,
    }


for c, fn in [("kasamatsu", "amanohashidate.json"), ("ine", "amanohashidate-ine.json")]:
    d = build(c)
    json.dump(d, open(f"{OUTDIR}/{fn}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(fn, [s["id"] for s in d["spots"]])
