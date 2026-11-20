#!/usr/bin/env python3
"""天橋立・伊根マップのデータを2通りの順番で書き出す。
   data/routes/amanohashidate.json（傘松公園が先）と amanohashidate-ine.json（伊根が先）。

使い方: python3 scripts/build_amanohashidate_data.py
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直すと、2つのデータが両方そろって書き換わる
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
CHECKED = "2026-11-20"
TANKAI_TICKETS = "https://www.tankai.jp/tourist_tickets/"


def gm(label_ja, label_en, lat, lng, q):
    return {"label": {"ja": label_ja, "en": label_en}, "lat": lat, "lng": lng,
            "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url, url_en=None):
    return {"kind": kind, "label": {"ja": ja, "en": en}, "url": {"ja": url, "en": url_en or url}}


def row(kind, ja, en, frm=None, until=None):
    return {"kind": kind, "text": {"ja": ja, "en": en}, "until": until, "from": frm}


def info(rows, cash=False, tip=None):
    return {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED}


def photos(pid, extra=None):
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid]) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def T(ja, en):
    return {"ja": ja, "en": en}


def build(course):
    A = course == "kasamatsu"
    S = {}

    S["kyoto"] = {
        "name": T("京都駅", "Kyoto Station"),
        "kind": T("駅（スタート）", "Station (start)"),
        "blurb": T("特急はしだてで、乗り換えなしで天橋立へ。約2時間の電車の旅から1日が始まります。",
                   "Take the Hashidate limited express straight to Amanohashidate: about 2 hours, no change of trains."),
        "lat": 34.98535, "lng": 135.758766,
        "text": T(
            "京都駅（きょうとえき）\n\n8:38発の特急はしだて1号に乗ると、乗り換えなしで10:39に天橋立に着きます。山陰線（嵯峨野線）のホームから出る、京都丹後鉄道に乗り入れる特急です。\n\n指定席は、帰りの18:09発の特急はしだて8号の分も一緒に買っておくと安心です。片道は大人4,800円（指定席・通常期。時期によって少し変わります）。\n\n写真は京都丹後鉄道の観光列車「丹後の海」。はしだてにこの車両が使われる日もあります。\n\nおすすめ出発時間：8:38",
            "Kyoto Station\n\nTake the 8:38 Hashidate No. 1 limited express and you’ll reach Amanohashidate at 10:39 without changing trains. It leaves from the San’in (Sagano) Line platforms and runs through onto the Kyoto Tango Railway.\n\nBuy reserved seats in advance, including the 18:09 Hashidate No. 8 for the way back. One way costs ¥4,800 per adult (reserved seat, regular season; it varies a little by season).\n\nThe blue train in the photos is the Kyoto Tango Railway’s “Tango no Umi”, which is used for some Hashidate services.\n\nRecommended departure time: 8:38"),
        "gmaps": [gm("JR京都駅", "JR Kyoto Station", 34.98535, 135.758766, "JR京都駅")],
        "links": [link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/")],
        "info": info([
            row("train", "特急はしだて1号 京都8:38発→天橋立10:39着（毎日運転）", "Hashidate No. 1: Kyoto 8:38 → Amanohashidate 10:39 (daily)"),
            row("fee", "片道 大人4,800円（乗車券2,320円＋指定席特急料金2,480円・通常期。時期によって少し変わります）",
                "One way ¥4,800 per adult (fare ¥2,320 + reserved-seat express charge ¥2,480, regular season; varies a little by season)"),
        ], tip=T("時刻はJR西日本の時刻表、運賃は乗換案内で確認しました。", "Times checked on JR West’s timetable; fares on a route planner.")),
    }

    S["station"] = {
        "name": T("天橋立駅（フリーパスを買う）", "Amanohashidate Station (get the day pass)"),
        "kind": T("駅・観光案内所", "Station & tourist info"),
        "blurb": T("駅の観光案内所で「天橋立・伊根フリーパス 1day」を。船もケーブルカーもバスも、これ1枚で乗り放題です。",
                   "Buy the Amanohashidate & Ine 1-Day Free Pass at the station’s tourist office: boats, cable car and buses all in one."),
        "lat": 35.557585, "lng": 135.182426,
        "text": T(
            "天橋立駅（あまのはしだてえき）\n\n着いたら、駅の観光案内所で「海の京都 天橋立・伊根フリーパス 1day」（大人3,550円）を買いましょう。この1枚で、天橋立の観光船、傘松公園のケーブルカー・リフト、伊根へのバス、伊根湾めぐり遊覧船に1日乗り放題です。京都丹後鉄道の電車（特急は自由席）にも乗れます。\n\n観光船で行き帰りするこのルートなら、別々に買うより450円お得。自転車で渡る場合は、紹介ページの「交通費のめやす」も見てください。\n\n駅の横には日帰り温泉「智恵の湯」（11番）もあります。\n\nおすすめ訪問時間：10:39〜10:45",
            "Amanohashidate Station\n\nWhen you arrive, buy the “Kyoto by the Sea Amanohashidate & Ine Free Pass 1day” (¥3,550 per adult) at the station’s tourist office. It covers the Amanohashidate sightseeing boat, the Kasamatsu Park cable car and chairlift, the bus to Ine and the Ine Bay boat for the whole day, plus Kyoto Tango Railway trains (non-reserved seats on limited expresses).\n\nOn this route, crossing Amanohashidate by boat both ways, it saves ¥450 compared with buying each ticket. If you plan to cross by bike, see “Getting around: fares” on the intro page.\n\nNext to the station is Chie-no-Yu, a hot spring (stop 11).\n\nRecommended visit time: 10:39–10:45"),
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
        ], tip=T("京都からの特急はしだての料金は含まれません。天橋立桟橋（観光船乗り場）でも買えます。",
                 "The Hashidate express from Kyoto isn’t covered. The pass is also sold at the Amanohashidate boat pier.")),
    }

    S["chionji"] = {
        "name": T("智恩寺（文殊堂）", "Chion-ji Temple (Monju-do)"),
        "kind": T("お寺", "Temple"),
        "blurb": T("「三人寄れば文殊の知恵」の文殊さま。松の枝に結ばれた白い扇子のおみくじが、花が咲いたようです。",
                   "Home of Monju, the bodhisattva of wisdom. Fan-shaped fortunes tied to the pine branches look like white flowers."),
        "lat": 35.557877, "lng": 135.184531,
        "text": T(
            "智恩寺（ちおんじ）\n\n「三人寄れば文殊の知恵」の文殊菩薩をまつる、日本三文殊のひとつ。天橋立の入り口に立つ2階建ての山門は、丹後でも最大級の木造の門です。観光船の乗り場はこのお寺のすぐ横です。\n\n境内の松には、扇の形をした「すえひろ扇子おみくじ」がたくさん結ばれています。参道の茶屋の名物「智恵の餅」も一緒にどうぞ。\n\nおすすめ訪問時間：10:45〜10:55",
            "Chion-ji Temple\n\nOne of Japan’s three great temples of Monju, the bodhisattva of wisdom (as in the saying “three heads are better than one”). Its two-story wooden gate at the entrance to Amanohashidate is one of the largest in the Tango region. The sightseeing boat pier is right next to the temple.\n\nThe pine trees in the grounds are covered with “suehiro” fan-shaped fortunes. Try “chie no mochi”, the rice-cake sweet sold at the tea houses on the approach.\n\nRecommended visit time: 10:45–10:55"),
        "gmaps": [gm("智恩寺", "Chion-ji", 35.557877, 135.184531, "智恩寺 宮津")],
        "links": [link("official", "天橋山 智恩寺 公式サイト", "Chion-ji official site (Japanese)", "https://www.monjudo-chionji.jp/")],
        "info": info([row("hours", "本堂の授与所（お守り・おみくじ）8:00〜17:00", "Main hall counter (charms, fortunes): 8:00–17:00")]),
    }

    after_cross_ja = ("一の宮桟橋に着いたら、すぐ近くの籠神社（5番）へ。" if A else
                      "一の宮桟橋に着いたら、200mほど先の「天橋立ケーブル下」バス停から伊根行きのバスへ。平日は11:24発に間に合います（伊根湾めぐり・日出11:53着）。土日祝は船が遠回りのコースになって11:22に着くので、12:08発のバスで（12:37着）。")
    after_cross_en = ("From Ichinomiya pier, Kono Shrine (stop 5) is just a short walk away." if A else
                      "From Ichinomiya pier, walk about 200 m to the “Amanohashidate Cable-shita” stop and take the bus to Ine. On weekdays you can catch the 11:24 bus (arrives at Ine-wan Meguri Hide at 11:53). On weekends and holidays the 11:00 boat takes a longer route and arrives at 11:22, so take the 12:08 bus (arr. 12:37).")
    S["crossing"] = {
        "name": T("天橋立を渡る（観光船か自転車で）", "Crossing Amanohashidate (boat or bike)"),
        "kind": T("観光船・レンタサイクル", "Boat or rental bike"),
        "blurb": T("智恩寺の横の桟橋から、カモメと一緒に観光船で12分。自転車なら松並木の中を15〜20分で対岸の府中へ。",
                   "From the pier by Chion-ji, 12 minutes by boat with the seagulls, or 15–20 minutes by bike through the pines, to Fuchu on the far side."),
        "lat": 35.558543, "lng": 135.184739,
        "text": T(
            "天橋立（あまのはしだて）を渡る\n\n宮島・松島と並ぶ日本三景のひとつ、天橋立。宮津湾と阿蘇海（あそかい）を分ける長さ3.6kmの砂の道を、観光船か自転車で対岸の府中（ふちゅう）へ渡ります。\n\n観光船（フリーパスで乗れます）は、智恩寺のすぐ横の天橋立桟橋から毎時0分・30分に出て、約12分で一の宮桟橋へ。出てすぐに、廻旋橋（かいせんきょう）がぐるっと回って船を通してくれます。カモメが船と並んで飛ぶので、エサやりも楽しめます。\n\n自転車なら、天橋立桟橋で借りて、松並木の中を15〜20分。片側は白い砂浜、もう片側は静かな内海です。対岸の一の宮桟橋で返せます（2時間500円。フリーパスには含まれません）。\n\n" + after_cross_ja + "\n\nおすすめ移動時間：11:00（観光船）",
            "Crossing Amanohashidate\n\nAmanohashidate is one of Japan’s Three Scenic Views, along with Miyajima and Matsushima: a 3.6 km sandbar between Miyazu Bay and the Aso Sea. Cross it by boat or by bike to Fuchu on the far side.\n\nThe sightseeing boat (covered by the free pass) leaves Amanohashidate pier, right next to Chion-ji, on the hour and half hour and reaches Ichinomiya pier in about 12 minutes. Just after leaving, the Kaisenkyo bridge swings around to let the boat through, and seagulls fly right alongside: feeding them is part of the fun.\n\nBy bike, rent one at Amanohashidate pier and ride 15–20 minutes through the pines, with white sand on one side and a calm inland sea on the other. You can drop it off at Ichinomiya pier (¥500 for 2 hours; not covered by the free pass).\n\n" + after_cross_en + "\n\nRecommended travel time: 11:00 (boat)"),
        "gmaps": [gm("天橋立桟橋（観光船・レンタサイクル）", "Amanohashidate pier (boat & bikes)", 35.558543, 135.184739, "天橋立観光船 天橋立桟橋")],
        "links": [
            link("timetable", "天橋立観光船（時刻表・料金）", "Sightseeing boat: times & fares (Japanese)", "https://www.tankai.jp/trip/amaboat/"),
            link("official", "レンタサイクル（丹後海陸交通）", "Rental bikes (Tankai, Japanese)", "https://www.tankai.jp/trip/bicycle/"),
        ],
        "info": info([
            row("hours", "観光船 天橋立桟橋発 9:00〜16:00の毎時0分・30分（3〜10月は17:00、4〜9月は17:30も）。土日祝の11:00〜15:00の0分発は、廻旋橋と運河をめぐる22分のコース",
                "Boats from Amanohashidate pier: on the hour and half hour, 9:00–16:00 (also 17:00 Mar–Oct, 17:30 Apr–Sep). On weekends and holidays, the on-the-hour boats 11:00–15:00 take a 22-minute route via the turning bridge and canal"),
            row("fee", "観光船 片道800円（フリーパスで乗れます）。レンタサイクル2時間500円（延長は1時間ごとに300円）",
                "Boat ¥800 one way (covered by the free pass). Rental bike ¥500 for 2 hours (¥300 per extra hour)"),
        ] + ([] if A else [row("bus", "天橋立ケーブル下→伊根湾めぐり・日出：11:24→11:53、12:08→12:37（毎日）。フリーパスで乗れます（なければ200円）",
                               "Amanohashidate Cable-shita → Ine-wan Meguri Hide: 11:24→11:53, 12:08→12:37 (daily). Covered by the free pass (otherwise ¥200)")])),
    }

    S["kono"] = {
        "name": T("元伊勢 籠神社", "Motoise Kono Shrine"),
        "kind": T("神社", "Shrine"),
        "blurb": T("伊勢神宮の神さまが、伊勢へ移る前にまつられていたと伝わる「元伊勢」。丹後でいちばん格式の高い神社です。",
                   "Known as “Moto-Ise”: the gods of Ise Grand Shrine are said to have been worshipped here before moving to Ise."),
        "lat": 35.582586, "lng": 135.196863,
        "text": T(
            "元伊勢 籠神社（このじんじゃ）\n\n天橋立を渡りきった府中にある、丹後国の一宮（いちのみや）。今は伊勢神宮にまつられている天照大御神（あまてらすおおみかみ）と豊受大御神（とようけのおおみかみ）が、昔この地にまつられていたと伝わることから「元伊勢」と呼ばれます。\n\nまっすぐな参道には、伊勢神宮と同じ形の鳥居。その先の神門をくぐって、静かな境内でゆっくりお参りしてください。\n\n" +
            ("一の宮桟橋から歩いてすぐ。お参りしたら、すぐ隣の府中駅から傘松公園へ上ります。\n\nおすすめ訪問時間：11:15〜11:35" if A else
             "傘松公園から下りてきたら、閉門（17:00）の前にお参りを。神社のすぐ先が、帰りの観光船の一の宮桟橋です。\n\nおすすめ訪問時間：16:25〜16:40"),
            "Motoise Kono Shrine\n\nThe most important shrine of old Tango Province, in Fuchu at the far end of Amanohashidate. Amaterasu and Toyouke, the deities now enshrined at Ise Grand Shrine, are said to have been worshipped here first, which is why it’s called “Moto-Ise” (the original Ise).\n\nThe straight approach has a torii in the same style as Ise’s. Go through the gate beyond it and take your time in the quiet grounds.\n\n" +
            ("It’s a short walk from Ichinomiya pier. After your visit, head up to Kasamatsu Park from Fuchu Station next door.\n\nRecommended visit time: 11:15–11:35" if A else
             "Visit after coming down from Kasamatsu Park, before the gates close at 17:00. Ichinomiya pier, for the boat back, is just beyond the shrine.\n\nRecommended visit time: 16:25–16:40")),
        "gmaps": [gm("元伊勢 籠神社", "Motoise Kono Shrine", 35.582586, 135.196863, "元伊勢籠神社")],
        "links": [link("official", "元伊勢 籠神社 公式サイト", "Kono Shrine official site (Japanese)", "https://www.motoise.jp/")],
        "info": info([row("hours", "開門 8:00〜17:00（季節や土日祝などで延びることがあります）", "Gates open 8:00–17:00 (sometimes longer on weekends, holidays and in some seasons)")]),
    }

    S["kasamatsu"] = {
        "name": T("天橋立傘松公園", "Amanohashidate Kasamatsu Park"),
        "kind": T("展望台", "Viewpoint"),
        "blurb": T("ケーブルカーかリフトで山の上へ。天に昇る龍のような「昇龍観」と、股のぞき発祥の地です。",
                   "Up by cable car or chairlift to the “rising dragon” view, the place where looking between your legs started."),
        "lat": 35.586553, "lng": 135.195928,
        "text": T(
            "天橋立傘松公園（かさまつこうえん）\n\n籠神社のすぐ横の府中駅から、ケーブルカー（約4分）かリフト（6〜8分ほど）で上ります（フリーパスで乗れます）。こちらからの天橋立は、龍が天に昇っていくように見えることから「昇龍観（しょうりゅうかん）」。「股のぞき発祥の地」で、股のぞき台もあります。股の間から逆さまにのぞくと、海と空が入れ替わって、橋が空に架かっているように見えます。\n\n" +
            ("山の上の展望レストラン「AmaTerrace（アマテラス）」で、天橋立を見ながらお昼ごはんにするのがおすすめです。\n\n下りたら、府中駅の近くの「天橋立ケーブル下」バス停から13:29発のバスで伊根へ（伊根湾めぐり・日出に13:58着）。\n\nおすすめ訪問時間：11:40〜13:15" if A else
             "伊根からのバス（伊根15:08発）を「天橋立ケーブル下」で降りたら、すぐ近くの府中駅へ。ケーブルカーの最終は季節で変わるので（12〜1月は17:00、11月・2月は17:30）、先に上りましょう。山の上には展望レストラン「AmaTerrace（アマテラス）」もあります。\n\nおすすめ訪問時間：15:45〜16:20"),
            "Amanohashidate Kasamatsu Park\n\nFrom Fuchu Station, right next to Kono Shrine, ride the cable car (about 4 min) or chairlift (6–8 min) up the hill (covered by the free pass). From here Amanohashidate looks like a dragon rising into the sky, the “Shoryukan” view. This is said to be where the upside-down “matanozoki” view began: bend over and look back between your legs, and the sandbar seems to float in the sky.\n\n" +
            ("Have lunch with the view at AmaTerrace, the viewing restaurant at the top.\n\nBack at the bottom, take the 13:29 bus to Ine from the “Amanohashidate Cable-shita” stop near Fuchu Station (arrives at Ine-wan Meguri Hide at 13:58).\n\nRecommended visit time: 11:40–13:15" if A else
             "Get off the bus from Ine (Ine 15:08) at “Amanohashidate Cable-shita” and walk to Fuchu Station. The last cable car depends on the season (17:00 in Dec–Jan, 17:30 in Nov and Feb), so go up first. There’s also a viewing restaurant at the top, AmaTerrace.\n\nRecommended visit time: 15:45–16:20")),
        "gmaps": [gm("府中駅（ケーブルカー乗り場）", "Fuchu Station (cable car)", 35.58323, 135.1953, "天橋立ケーブルカー 府中駅")],
        "links": [
            link("official", "天橋立ケーブルカー・リフト（運行時間・運賃）", "Cable car & lift: times and fares (Japanese)", "https://www.tankai.jp/trip/cable/"),
            link("timetable", "丹海バス 時刻表（伊根・蒲入線）", "Tankai bus timetable (Ine line, Japanese)", "https://www.tankai.jp/routebus/timetable/"),
        ],
        "info": info([
            row("hours", "ケーブルカー 9:00〜（最終は3〜10月18:00、11月・2月17:30、12〜1月17:00）、15分ごと。リフト 9:00〜16:00（12月1日〜1月5日は10:00から、1月6日〜2月末は土日祝だけ）",
                "Cable car from 9:00, every 15 min (last car 18:00 Mar–Oct, 17:30 Nov & Feb, 17:00 Dec–Jan). Chairlift 9:00–16:00 (from 10:00 Dec 1–Jan 5; weekends and holidays only Jan 6–end of Feb)"),
            row("fee", "ケーブルカー・リフト共通 往復 大人800円・小児400円（フリーパスで乗れます）。公園は無料",
                "Cable car / lift round trip ¥800 (children ¥400), covered by the free pass. The park itself is free"),
        ] + ([row("bus", "天橋立ケーブル下→伊根湾めぐり・日出：13:29→13:58、14:24→14:53（毎日）。フリーパスで乗れます（なければ200円）",
                  "Amanohashidate Cable-shita → Ine-wan Meguri Hide: 13:29→13:58, 14:24→14:53 (daily). Covered by the free pass (otherwise ¥200)")] if A else []),
            tip=T("山の上の傘松駅では現金しか使えません。切符は下の府中駅で買うと、カードや電子マネーも使えます。",
                  "Kasamatsu Station at the top takes cash only. Buy tickets at Fuchu Station at the bottom, where cards and e-money work.")),
        "notices": [{"from": None, "to": "2026-12-18", "url": "https://www.tankai.jp/trip/kasamatsu/",
                     "text": T("2026年12月18日は天橋立傘松公園が休業です。", "Kasamatsu Park is closed on Dec 18, 2026.")}],
    }

    S["ineboat"] = {
        "name": T("伊根湾めぐり遊覧船", "Ine Bay Sightseeing Boat"),
        "kind": T("遊覧船", "Boat ride"),
        "blurb": T("海の上から舟屋の並ぶ町を眺める25分の船旅。船のまわりをカモメがいっしょに飛びます。",
                   "A 25-minute cruise past Ine’s boathouses, with seagulls flying right alongside."),
        "lat": 35.6704, "lng": 135.2772,
        "text": T(
            "伊根湾めぐり遊覧船\n\nバスを「伊根湾めぐり・日出（ひで）」で降りると、目の前が遊覧船乗り場です（フリーパスで乗れます）。30分ごとに出る船で、約25分かけて伊根湾をぐるっと一周。1階が船のガレージになった舟屋（ふなや）が、海のすぐ上に並ぶ景色を海側から見られます。\n\n船が出るとカモメが集まってきて、船と並んで飛びます。乗り場と船内でカモメのエサも売っています。\n\n" +
            ("おすすめ訪問時間：14:00〜14:30" if A else "伊根に先に来た日は、お昼ごはんも伊根で。\n\nおすすめ訪問時間：13:00〜13:30"),
            "Ine Bay Sightseeing Boat\n\nGet off the bus at “Ine-wan Meguri Hide” and the pier is right in front of you (covered by the free pass). Boats leave every 30 minutes and loop around Ine Bay in about 25 minutes, giving you the view of the funaya — houses with a boat garage on the ground floor — lined up right on the water.\n\nOnce the boat leaves, seagulls gather and fly alongside. Gull food is sold at the pier and on board.\n\n" +
            ("Recommended visit time: 14:00–14:30" if A else "If you come to Ine first, have lunch in Ine too.\n\nRecommended visit time: 13:00–13:30")),
        "gmaps": [gm("伊根湾めぐり遊覧船 日出乗り場", "Ine Bay boat pier (Hide)", 35.6704, 135.2772, "伊根湾めぐり遊覧船")],
        "links": [link("official", "伊根湾めぐり遊覧船（丹後海陸交通）", "Ine Bay Sightseeing Boat (Tankai, Japanese)", "https://www.tankai.jp/trip/ineboat/")],
        "info": info([
            row("hours", "9:00〜16:00、毎時0分・30分に出航（約25分）", "9:00–16:00, departing on the hour and half hour (about 25 min)"),
            row("closed", "年中無休（天気が悪いと欠航することがあります）", "Open every day (may be cancelled in bad weather)"),
            row("fee", "大人1,200円（中学生以上）・小学生600円（フリーパスで乗れます）", "¥1,200 (junior high and up), ¥600 (elementary); covered by the free pass"),
        ]),
    }

    S["mukai"] = {
        "name": T("向井酒造", "Mukai Sake Brewery"),
        "kind": T("酒蔵", "Sake brewery"),
        "blurb": T("「海に一番近い酒蔵」。古代米で造る赤いお酒「伊根満開」で知られる、舟屋の町の酒蔵です。",
                   "“The sake brewery closest to the sea”, known for Ine Mankai, a red sake made with ancient rice."),
        "lat": 35.674754, "lng": 135.286395,
        "text": T(
            "向井酒造（むかいしゅぞう）\n\n遊覧船乗り場から湾ぞいの道を15分ほど歩いたところ、舟屋の町・平田（ひらた）の入り口にある酒蔵です。お酒はすべて純米酒。いちばん有名なのは、伊根で育てた古代米（紫黒米）を使った赤いお酒「伊根満開（いねまんかい）」で、甘酸っぱくて飲みやすい味です。\n\n直売所でお酒を買えるので、おみやげにどうぞ。お昼休み（12:00〜13:00）と木曜日はお休みです。\n\n" +
            ("おすすめ訪問時間：14:45〜15:05" if A else "おすすめ訪問時間：13:40〜14:00"),
            "Mukai Sake Brewery\n\nAbout 15 minutes on foot along the bay from the boat pier, at the edge of Hirata, the boathouse village. Everything they brew is junmai (pure rice) sake. Their best-known sake is Ine Mankai, a red sake made with an ancient purple rice grown in Ine: sweet and tart, and easy to drink.\n\nYou can buy sake at their shop, a nice souvenir. The shop closes for lunch (12:00–13:00) and on Thursdays.\n\n" +
            ("Recommended visit time: 14:45–15:05" if A else "Recommended visit time: 13:40–14:00")),
        "gmaps": [gm("向井酒造", "Mukai Shuzo", 35.674754, 135.286395, "向井酒造 伊根")],
        "links": [link("official", "向井酒造 直売所のご案内", "Mukai Shuzo shop info (Japanese)", "https://www.kuramoto-mukai.jp/%e7%9b%b4%e5%a3%b2%e6%89%80%e3%81%ae%e3%81%94%e6%a1%88%e5%86%85/")],
        "info": info([
            row("hours", "9:00〜12:00 / 13:00〜17:00", "9:00–12:00 / 13:00–17:00"),
            row("closed", "木曜日・年末年始", "Thursdays and New Year holidays"),
        ]),
        "caution": T("木曜はお休み", "Closed on Thursdays"),
        "_extra": [
            {"file": "mukai-2.jpg", "credit": {"author": "漱石の猫", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:%E5%90%91%E4%BA%95%E9%85%92%E9%80%A0.jpg"}},
            {"file": "mukai-3.jpg", "credit": {"author": "Asturio Cantabrio", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:Ine_Mukai_Brewery_2021-04_ac_(1).jpg"}},
            {"file": "mukai-4.jpg", "credit": {"author": "Asturio Cantabrio", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:Ine_Mukai_Brewery_2021-04_ac_(2).jpg"}},
        ],
    }

    S["funaya"] = {
        "name": T("伊根の舟屋（伊根浦）", "Ine’s Funaya Boathouses"),
        "kind": T("町並み", "Historic district"),
        "blurb": T("海の上に建つ約230軒の舟屋。湖のように静かな湾ぞいを、のんびり歩きます。",
                   "About 230 boathouses built right on the water. Stroll along a bay as calm as a lake."),
        "lat": 35.675733, "lng": 135.287658,
        "text": T(
            "伊根の舟屋（ふなや）\n\n1階が海に開いた船のガレージ、2階が住まいになった舟屋が、伊根湾にそって約230軒並びます。国の重要伝統的建造物群保存地区にも選ばれた、ほかでは見られない漁師町です。\n\n遊覧船乗り場から、向井酒造の前を通って、伊根浦公園と観光案内所のある町の中心まで、湾ぞいの道を20分ほど歩きます。乗り場のそばの日出（ひで）の入り江は、水が透き通っていてきれいです。\n\n舟屋の多くは今も人が暮らす家なので、静かに歩いて、勝手に入らないようにしてください。\n\n" +
            ("帰りは「伊根」バス停から16:00発のバスで「天橋立ケーブル下」へ（16:33着）。そこから一の宮桟橋まで歩いてすぐです。\n\nおすすめ訪問時間：15:05〜15:55" if A else
             "町の食事どころで、海を見ながらお昼ごはんもどうぞ。\n\nそのあとは「伊根」バス停から15:08発のバスで「天橋立ケーブル下」へ（15:41着）。傘松公園に向かいます。\n\nおすすめ訪問時間：14:00〜15:05"),
            "Ine’s Funaya\n\nAbout 230 funaya line Ine Bay: the ground floor is a garage that opens onto the sea for a boat, and people live upstairs. It’s a fishing village like nowhere else, protected as a national Preservation District for Groups of Traditional Buildings.\n\nFrom the boat pier, walk about 20 minutes along the bay road, past Mukai Sake Brewery, to the center of the village with Ine-ura Park and the tourist information center. The cove at Hide, next to the pier, has beautifully clear water.\n\nMost funaya are still people’s homes, so please keep your voice down and don’t go inside without permission.\n\n" +
            ("For the way back, take the 16:00 bus from the “Ine” stop to “Amanohashidate Cable-shita” (arr. 16:33). Ichinomiya pier is a short walk from there.\n\nRecommended visit time: 15:05–15:55" if A else
             "Have lunch with a sea view at one of the village’s restaurants.\n\nThen take the 15:08 bus from the “Ine” stop to “Amanohashidate Cable-shita” (arr. 15:41) for Kasamatsu Park.\n\nRecommended visit time: 14:00–15:05")),
        "gmaps": [gm("伊根浦公園", "Ine-ura Park", 35.675733, 135.287658, "伊根浦公園")],
        "links": [
            link("info", "伊根町観光協会", "Ine Tourist Association", "https://www.ine-kankou.jp/"),
            link("timetable", "丹海バス 時刻表（伊根・蒲入線）", "Tankai bus timetable (Ine line, Japanese)", "https://www.tankai.jp/routebus/timetable/"),
        ],
        "info": info([
            row("bus", "伊根→天橋立ケーブル下：15:08→15:41、16:00→16:33（毎日）。フリーパスで乗れます（なければ200円）",
                "Ine → Amanohashidate Cable-shita: 15:08→15:41, 16:00→16:33 (daily). Covered by the free pass (otherwise ¥200)"),
        ], tip=T("バスはタッチ決済・QRコード決済も使えますが、交通系ICカード（ICOCAなど）は使えません。",
                 "The bus takes contactless credit cards and QR payments, but not transit IC cards like ICOCA.")),
    }

    S["return"] = {
        "name": T("天橋立を渡って戻る（観光船か自転車で）", "Back across Amanohashidate (boat or bike)"),
        "kind": T("観光船・レンタサイクル", "Boat or rental bike"),
        "blurb": T("一の宮桟橋から、16:45の観光船で天橋立駅側へ。自転車なら、夕方の松並木を走って戻ります。",
                   "From Ichinomiya pier, the 16:45 boat back to the station side, or ride a bike back through the evening pines."),
        "lat": 35.580862, "lng": 135.196014,
        "text": T(
            "天橋立を渡って戻る\n\n" +
            ("伊根からのバスを「天橋立ケーブル下」で降りたら、歩いてすぐの一の宮桟橋へ。" if A else "籠神社のお参りを終えたら、すぐ先の一の宮桟橋へ。") +
            "16:45発の観光船に乗ると、16:57に天橋立桟橋に着きます（フリーパスで乗れます。3〜10月は17:15発、4〜9月は17:45発もあります）。天橋立桟橋から天橋立駅までは歩いて5分ほどです。\n\n自転車で戻るなら、一の宮桟橋で借りて、行きとは違う夕方の松並木を走って天橋立桟橋で返します（2時間500円）。砂浜に寄り道するのも気持ちいいです。自転車は窓口が開いているうちに返せるよう、早めに出発しましょう。\n\nおすすめ移動時間：16:45（観光船）",
            "Back across Amanohashidate\n\n" +
            ("Get off the bus from Ine at “Amanohashidate Cable-shita” and walk to Ichinomiya pier. " if A else "After Kono Shrine, walk to Ichinomiya pier just beyond it. ") +
            "The 16:45 boat reaches Amanohashidate pier at 16:57 (covered by the free pass; there are also boats at 17:15 in Mar–Oct and 17:45 in Apr–Sep). The station is about 5 minutes on foot from the pier.\n\nTo ride back, rent a bike at Ichinomiya pier and return it at Amanohashidate pier (¥500 for 2 hours), riding the pine forest in the evening light; stop at the beach on the way. Leave early enough to return the bike while the counter is open.\n\nRecommended travel time: 16:45 (boat)"),
        "gmaps": [gm("一の宮桟橋（観光船・レンタサイクル）", "Ichinomiya pier (boat & bikes)", 35.580862, 135.196014, "天橋立観光船 一の宮桟橋")],
        "links": [
            link("timetable", "天橋立観光船（時刻表・料金）", "Sightseeing boat: times & fares (Japanese)", "https://www.tankai.jp/trip/amaboat/"),
            link("official", "レンタサイクル（丹後海陸交通）", "Rental bikes (Tankai, Japanese)", "https://www.tankai.jp/trip/bicycle/"),
        ],
        "info": info([
            row("hours", "観光船 一の宮桟橋発 9:15〜16:45の毎時15分・45分（3〜10月は17:15、4〜9月は17:45も）。天橋立桟橋まで約12分",
                "Boats from Ichinomiya pier at :15 and :45 past the hour, 9:15–16:45 (also 17:15 Mar–Oct, 17:45 Apr–Sep); about 12 min to Amanohashidate pier"),
            row("fee", "観光船 片道800円（フリーパスで乗れます）。レンタサイクル2時間500円",
                "Boat ¥800 one way (covered by the free pass). Rental bike ¥500 for 2 hours"),
        ]),
    }

    S["chienoyu"] = {
        "name": T("天橋立温泉 智恵の湯", "Chie-no-Yu Hot Spring"),
        "kind": T("日帰り温泉（時間があれば）", "Hot spring (if you have time)"),
        "blurb": T("天橋立駅のすぐ横の日帰り温泉。特急の時間まで、歩き疲れた足を休めて。",
                   "A day-use hot spring right next to the station. Soak your tired legs before the train."),
        "lat": 35.557418, "lng": 135.183084,
        "text": T(
            "天橋立温泉 智恵の湯（ちえのゆ）\n\n天橋立駅の横にある日帰り温泉です。露天風呂やつぼ湯もあり、1日歩いたあとにぴったり。\n\n16:57に観光船で戻ってくると、18:09の特急まで1時間ほどあります。温泉でひと休みしてから帰りましょう。もっとゆっくりしたいときは、19:05の特急はしだて10号（京都着21:20）もあります。\n\n入館は18:30まで。火・水・木曜日はお休みです。\n\nおすすめ訪問時間：17:05〜18:00",
            "Chie-no-Yu Hot Spring\n\nA day-use hot spring next to Amanohashidate Station, with an outdoor bath and tub baths: just right after a day of walking.\n\nBack on the 16:57 boat, you have about an hour before the 18:09 express. Relax here first. For more time, there’s also the 19:05 Hashidate No. 10 (Kyoto 21:20).\n\nLast entry 18:30. Closed Tuesdays, Wednesdays and Thursdays.\n\nRecommended visit time: 17:05–18:00"),
        "gmaps": [gm("天橋立温泉 智恵の湯", "Chie-no-Yu", 35.557418, 135.183084, "天橋立温泉 智恵の湯")],
        "links": [link("official", "天橋立温泉 智恵の湯", "Chie-no-Yu (Japanese)", "https://www.viewland.jp/chienoyu")],
        "info": info([
            row("hours", "12:00〜20:00（入館は18:30まで）", "12:00–20:00 (last entry 18:30)"),
            row("closed", "火曜日・水曜日・木曜日", "Tuesdays, Wednesdays and Thursdays"),
            row("fee", "大人800円（中学生以上）・小学生400円", "¥800 (junior high and up), ¥400 (elementary)"),
        ], tip=T("入れ墨・タトゥーのある方は入れません。キャリーケースの持ち込み・預かりもできません。",
                 "No entry with tattoos. Suitcases can’t be brought in or left here.")),
        "caution": T("火・水・木曜はお休み", "Closed Tue, Wed and Thu"),
    }

    S["station2"] = {
        "name": T("天橋立駅（京都へ帰る）", "Amanohashidate Station (back to Kyoto)"),
        "kind": T("駅（ゴール）", "Station (finish)"),
        "blurb": T("18:09の特急はしだて8号で京都へ。20:21に京都駅に着きます。",
                   "The 18:09 Hashidate No. 8 back to Kyoto, arriving at 20:21."),
        "lat": 35.557585, "lng": 135.182426,
        "text": T(
            "天橋立駅（京都へ帰る）\n\n18:09発の特急はしだて8号に乗ると、20:21に京都駅に着きます。温泉でゆっくりした日は、19:05発のはしだて10号（京都着21:20）で。\n\nおすすめ出発時間：18:09",
            "Amanohashidate Station (back to Kyoto)\n\nThe 18:09 Hashidate No. 8 gets you to Kyoto at 20:21. If you lingered at the hot spring, take the 19:05 Hashidate No. 10 (Kyoto 21:20).\n\nRecommended departure time: 18:09"),
        "gmaps": [gm("天橋立駅", "Amanohashidate Station", 35.557585, 135.182426, "天橋立駅")],
        "links": [link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/")],
        "info": info([
            row("train", "特急はしだて8号 天橋立18:09発→京都20:21着、はしだて10号 19:05発→21:20着（毎日運転）",
                "Hashidate No. 8: Amanohashidate 18:09 → Kyoto 20:21; No. 10: 19:05 → 21:20 (daily)"),
            row("fee", "片道 大人4,800円（指定席・通常期）", "One way ¥4,800 per adult (reserved seat, regular season)"),
        ]),
    }

    order = (["kyoto", "station", "chionji", "crossing", "kono", "kasamatsu", "ineboat", "mukai", "funaya", "return", "chienoyu", "station2"] if A else
             ["kyoto", "station", "chionji", "crossing", "ineboat", "mukai", "funaya", "kasamatsu", "kono", "return", "chienoyu", "station2"])
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
                  "京都駅から特急はしだてで天橋立へ、天橋立駅の観光案内所で「海の京都 天橋立・伊根フリーパス 1day」を買い、観光船か自転車で府中へ渡り、傘松公園・籠神社と伊根（遊覧船・向井酒造・舟屋）を回って、一の宮桟橋から観光船か自転車で戻り、18:09の特急で京都へ（オーナーの希望 2026-11-20）。"
                  "写真は Toshi の写真ライブラリから選んだもの（2023〜2026年の6回分、約4,100枚を全部見て、1か所10枚以内・横の写真だけ・Nikon D7000 を含む。長辺1600px・位置情報なし）。ファイル名はスポットの id。向井酒造の一部の写真は Wikimedia Commons（photos の要素が {file, credit}）。籠神社は神門の外で撮った写真だけを使っている。"
                  "info.checked は事実情報を確認した日（各社・各施設の公式サイト。特急の時刻はJR西日本の時刻表、特急の運賃は乗換案内、バス・観光船の時刻と運賃は丹後海陸交通の時刻表と運賃表）。notices は from〜to の間だけ表示される。focus は地図を開いたときに映す範囲（京都駅は離れているので入れない）。"),
        "sections": sections,
        "focus": {"first": 2, "last": 12},
        "photoBase": "../images/amanohashidate/",
        "spots": spots,
    }


for c, fn in [("kasamatsu", "amanohashidate.json"), ("ine", "amanohashidate-ine.json")]:
    d = build(c)
    json.dump(d, open(f"{OUTDIR}/{fn}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(fn, [s["id"] for s in d["spots"]])
