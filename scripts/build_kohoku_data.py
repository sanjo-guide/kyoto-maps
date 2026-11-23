#!/usr/bin/env python3
"""京都から日帰り 海津大崎の桜と長浜のデータを、4つのコース分まとめて書き出す。

使い方: python3 scripts/build_kohoku_data.py  （そのあと python3 scripts/sync_kohoku.py）
- 作るもの（COURSES。どれも京都駅から JR 湖西線で出発。直接直さない。実行のたびに作り直す）:
  - data/routes/kohoku.json         … late（最初に開く）。9:45ごろ発：桜並木を往復 → 夕方の長浜（黒壁・豊公園）
  - data/routes/kohoku-through.json … through。9:45ごろ発：大浦を通って永原駅まで歩き通す → 夜は長浜
  - data/routes/kohoku-early.json   … early。7:00発：朝の桜 → 午後は長浜の町と4つの施設 → 京都駅で晩ごはん
  - data/routes/kohoku-island.json  … island。7:00発：朝の桜 → 今津港13:10の船で竹生島 → 夕方の長浜
- 文章・料金・時間はこのファイルに書いてある
  - BASE … スポットごとの、コースで変わらない内容
  - COURSES … コースごとの並び順、めやすの時間、その時間割での動き方、一覧に出る注意、「選んで回る」の設定
  - SOURCES … 時刻・料金の出典と、そこで見た数字・確認日（データの sources に入る）
- 2027年春の時刻・日程・料金は、ほとんど未発表。書いてあるのは「2026年11月のダイヤ」か「2026年春の実績」。
  発表されたら直す：JR（3月の改正）、海津大崎のバス連絡表・交通規制・臨時トイレ、琵琶湖汽船（4月からの時刻・料金、桜クルーズ）、
  豊公園のぼんぼり、長濱浪漫ビールの休業日
- 距離は OpenStreetMap の徒歩ルートで測り、時間は少しゆったりにしてある
- 写真は images/kohoku/<スポットのid>-<番号>.jpg を番号の順に全部使う（足していない）。竹生島だけ Wikimedia Commons（クレジットつき）。
  オーナーは竹生島に行っていないので、行った・食べたとは書かない
- お店は、公式サイトで時間を確かめた店だけ名前を出す（長濱浪漫ビール・京都拉麺小路）
- 2026-11-22 オーナーの基準で作り直した（海津大崎・長浜・竹生島・大浦を1日に詰め込まない）
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kohoku"
CHECKED = "2026-11-22"
PICKS = {}
for f in os.listdir(IMG):
    m = re.match(r"(.+)-(\d+)\.jpg$", f)
    if m:
        PICKS.setdefault(m.group(1), []).append(int(m.group(2)))


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, q):
    return {"label": T(ja, en), "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


def photos(pid, extra=()):
    """自分の写真（番号の順）のあとに、クレジットつきの写真（extra）を並べる。extra にあるファイルは二重に入れない。"""
    taken = {x["file"] for x in extra}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + list(extra)


def yahoo(frm, to, day, hhmm, kind=1):
    """乗換案内の検索結果のURL（kind=1 出発、2 終電）。day は 2026年11月の日（25=水、28=土、29=日）"""
    hh, mm = hhmm.split(":")
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(
        {"from": frm, "to": to, "y": "2026", "m": "11", "d": str(day), "hh": hh, "m1": mm[0], "m2": mm[1],
         "type": str(kind), "ticket": "ic", "expkind": "1", "ws": "3", "s": "0",
         "al": "0", "shin": "0", "ex": "0", "hb": "0", "lb": "0", "sr": "0"})


# ---------------------------------------------------------------------------
# 出典のURL
# ---------------------------------------------------------------------------
TK = "https://takashima-kanko.jp"
SAKURA = TK + "/sakura/"
REG = SAKURA + "regulation.html"
FAQ = SAKURA + "faq.html"
MAP26 = SAKURA + "2026map.pdf"
BUS_WD = SAKURA + "2026bus.pdf"
BUS_WE = SAKURA + "2026bus_h.pdf"
BUS_REG = SAKURA + "2026bus_kisei.pdf"
CYCLE = TK + "/guide/rentalcycle.html"
OSAKIJI = TK + "/spot/2018/06/post_71.html"
ISHIZUMI = TK + "/spot/2018/06/post_170.html"
BOAT = "https://www.biwakokisen.co.jp/cruise/chikubu/price_time/"
BOAT_FAQ = "https://www.biwakokisen.co.jp/cruise/chikubu/faq/"
BOAT_FLOW = "https://www.biwakokisen.co.jp/cruise/chikubu/flow/"
IMAZU = "https://www.biwakokisen.co.jp/access/imazu/"
CRUISE = "https://www.biwakokisen.co.jp/season_event/5972/"
HOGONJI = "https://www.chikubushima.jp/"
WIND = "https://www.westjr.co.jp/company/action/service/safety_transport/storm/"
TRAFFIC = "https://trafficinfo.westjr.co.jp/kinki.html"
CASTLE = "https://nagahama-rekihaku.jp/info/open"
PARK = "https://kitabiwako.jp/spot/spot_2292"
PARK_2026 = "https://www.city.nagahama.lg.jp/0000016592.html"
STATIONS = "https://www.city.nagahama.lg.jp/0000001880.html"
KEIUN = "https://kitabiwako.jp/keiunkan/guidance.html"
KEIUN_OFF = "https://kitabiwako.jp/spot/spot_1703"
BONBAI = "https://bonbai.jp/"
TETSU = "https://kitabiwako.jp/tetsudou/guidance.html"
GLASS = "https://www.kurokabe.co.jp/shopping/glasshouse/"
ROMAN = "https://www.romanbeer.com/restaurant/"
ROMAN_CLOSED = "https://www.romanbeer.com/news/20260327_id2704/"
RAMEN = "https://www.kyoto-station-building.co.jp/ramen_koji/"

L_YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
L_TRAFFIC = link("info", "JR西日本の運行情報（近畿）", "JR West service status, Kinki area (Japanese)", TRAFFIC)
L_SAKURA = link("official", "海津大崎の桜（開花状況・地図・バス）", "Kaizu-Osaki cherries: bloom, maps and buses (Japanese)", SAKURA)
L_REG = link("info", "交通規制の案内（2026年春の実績）", "Traffic restrictions, as held in spring 2026 (Japanese)", REG)
L_BUS_WD = link("timetable", "バス連絡表・平日（2026年春）", "Bus connections, weekdays, spring 2026 (Japanese)", BUS_WD)
L_BUS_WE = link("timetable", "バス連絡表・土休日（2026年春）", "Bus connections, weekends, spring 2026 (Japanese)", BUS_WE)
L_MAP26 = link("info", "お花見マップ（2026年春。トイレの場所）", "Blossom map with toilets, spring 2026 (Japanese)", MAP26)
L_ROMAN = link("official", "長濱浪漫ビール（時間・営業日・予約）", "Nagahama Roman Beer: hours, open days and booking (Japanese)", ROMAN)
L_RAMEN = link("official", "京都拉麺小路（京都駅ビル10階）", "Kyoto Ramen Koji, Kyoto Station Building 10F (Japanese)", RAMEN)

# ---------------------------------------------------------------------------
# お知らせ（春以外の「春のマップです」は scripts/sync_kohoku.py が全部のスポットに出す）
# ---------------------------------------------------------------------------
N_PACK = notice(
    "お昼は京都で買い、トイレはマキノ駅で", "Buy lunch in Kyoto; use the toilet at Makino Station",
    "駅から先は店が少なく、2026年春は駅前の臨時売店もありませんでした。食べ物と飲み物は電車に乗る前に。常設の公共トイレは駅前で、桜並木の入口と大崎寺の近くは花見の時期だけの仮設です（2026年春の地図）。",
    "There are few shops beyond the station, and the seasonal stall didn’t run in spring 2026. Buy food and drink before boarding. The permanent public toilet is at the station; those at the avenue entrance and near Osakiji are temporary, in season only (2026 map).",
    url=MAP26)
N_WIND = notice(
    "湖西線は強風で止まることがあります", "Strong winds can stop the Kosei Line",
    "家を出る前に運行情報を。マキノを通る区間が止まっている日は海津大崎をやめて、京都10:00発の琵琶湖線の新快速で長浜へ（11:10着・1,340円）。豊公園も桜の名所です。",
    "Check service status before setting out. If the section through Makino is stopped, skip Kaizu-Osaki and take the 10:00 Biwako Line Special Rapid from Kyoto to Nagahama (11:10, ¥1,340): Hoko Park is a cherry spot too.",
    url=TRAFFIC)
N_REG = notice(
    "見ごろの土日は交通規制（2026年春の実績）", "Traffic restrictions on peak weekends (as held in 2026)",
    "2026年は4月4日・5日の9:30〜17:00に、車は東向きの一方通行の予定でした。海津の集落の中は自転車を押して歩きます。国境線のバスは海津1区に止まらず、海津大崎口に止まりました。来春の日程は要確認。",
    "In 2026 cars were to go eastbound only on 4–5 April, 9:30–17:00. Bicycles must be pushed through Kaizu village, and Kokkyo line buses stopped at Kaizu-Osaki-guchi instead of Kaizu 1-ku. Please check next spring’s dates.",
    url=REG)
N_LAST_TRAIN = notice(
    "長浜→京都の最終は22:15", "Last train from Nagahama to Kyoto: 22:15",
    "22:15発は米原で乗り換えて京都23:50着。乗り換えなしの最後は21:17発→22:28着です。三条京阪へ電車で帰るなら21:17発が最後（山科で地下鉄に乗り換えて22:50着）。2026年11月のダイヤです。",
    "The 22:15 changes at Maibara and reaches Kyoto at 23:50. The last direct train is the 21:17 (22:28). For Sanjo-Keihan by train, the 21:17 is the last (subway from Yamashina, arriving 22:50). November 2026 timetable.")

TRAIN_TIP = T("電車は乗換案内で、2026年11月25日（水）・28日（土）・29日（日）と、主な便は23日（祝）も確かめた時刻です。3月にダイヤ改正があることが多いので、来春は要確認。",
              "Trains checked on a route planner for Wed 25, Sat 28 and Sun 29 November 2026, and the main trains also for Mon 23 (a holiday). Timetables often change in March, so please check for next spring.")

# ---------------------------------------------------------------------------
# コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = {
    "makino": dict(
        name=T("マキノ駅・マキノサニービーチ", "Makino Station & Makino Sunny Beach"), kind=T("駅・浜辺", "Station & beach"),
        head=T("マキノ駅とマキノサニービーチ（知内浜・ちないはま）", "Makino Station and Makino Sunny Beach (Chinai beach)"),
        blurb=T("京都駅から湖西線で。トイレを済ませ、食べ物を持って歩きはじめます。",
                "The Kosei Line from Kyoto Station. Use the toilet, and set off with your food."),
        lat=35.45351, lng=136.06021,
        body=T("京都駅には、湖西線経由と琵琶湖線経由の新快速があります。乗るのは湖西線。乗った車両がマキノまで行くかどうかも、ホームの表示と放送で確かめてください。\n\n"
               "三条のあたりからは、三条京阪から地下鉄東西線で山科へ出て、同じ電車に乗れます（マキノまで1,430円）。\n\n"
               "サニービーチは駅から歩いて約15分の、松と白砂の浜。湖の向こうに、これから歩く海津大崎の岬が見えます。",
               "Kyoto Station has Special Rapids on both the Kosei and Biwako lines: you want the Kosei Line. Check the signs and announcements that your carriage goes as far as Makino.\n\n"
               "From around Sanjo, take the Tozai subway from Sanjo-Keihan to Yamashina and board the same train there (¥1,430 to Makino).\n\n"
               "Sunny Beach, a pine-lined white-sand shore, is about 15 minutes on foot from the station. Across the water is the headland of Kaizu-Osaki."),
        gmaps=[gm("JRマキノ駅", "JR Makino Station", "JRマキノ駅"), gm("マキノサニービーチ", "Makino Sunny Beach", "マキノサニービーチ")],
        links=[L_YAHOO, L_TRAFFIC, L_SAKURA, L_MAP26, link("official", "びわ湖高島レンタサイクル", "Takashima rental bicycles (Japanese)", CYCLE)],
        notices=[N_PACK, N_WIND],
        rows=[row("fee", "京都→マキノ 1,170円（三条京阪から山科乗り換えで1,430円）", "Kyoto → Makino ¥1,170 (¥1,430 from Sanjo-Keihan via Yamashina)"),
              row("bike", "駅の観光案内所 9:00〜17:00、普通自転車1日1,000円。台数に限りがあり、2027年5月9日までは予約不可。身分証が必要。高島市の中だけで、大浦・永原（長浜市）へは乗っていけません",
                  "Station tourist office 9:00–17:00, ordinary bicycle ¥1,000 a day. Limited numbers, no bookings until 9 May 2027, ID needed. Takashima city only, so not to Oura or Nagahara (Nagahama city)"),
              row("train", "マキノ→京都の最終：22:10発→23:19着。18時台からは本数が減ります", "Last train Makino → Kyoto: 22:10 → 23:19. Fewer trains from 18:00")],
        tip=TRAIN_TIP),

    "kaizu": dict(
        name=T("海津の石積み", "Kaizu stone embankment"), kind=T("町並み", "Old lakeside village"),
        head=T("海津（かいづ）の石積み", "Kaizu stone embankment"),
        blurb=T("湖の波から家を守るために積まれた、江戸時代の石垣が続く湖岸の集落。桜並木の手前です。",
                "A lakeside village behind an Edo-period wall built against the waves, just before the cherry avenue."),
        lat=35.46400, lng=136.07890,
        body=T("北国へ向かう道と湖の舟運で栄えた港町に、波よけの石垣が約1.2km残っています。海津・西浜・知内の水辺景観として、国の重要文化的景観に選ばれています。\n\n"
               "石積みは湖の側から見るものです。通りの家の間から浜へ下りると、写真のように見えます。人が暮らしている集落なので、家の敷地には入らないでください。",
               "About 1.2 km of wave-breaking stone wall remains in this old port on the road north. With Nishihama and Chinai, it is a nationally designated Important Cultural Landscape.\n\n"
               "The wall is seen from the lake side: go down to the shore between the houses. People live here, so please keep off private property."),
        gmaps=[gm("海津の石積み", "Kaizu stone embankment", "海津の石積み 高島市")],
        links=[link("official", "海津の石積み（びわ湖高島観光協会）", "Kaizu stone embankment (Takashima tourism, Japanese)", ISHIZUMI)],
        notices=[],
        rows=[row("walk", "マキノ駅からまっすぐ約2km・30分。サニービーチからは約2.3km・35分", "About 2 km / 30 min straight from Makino Station; 2.3 km / 35 min from Sunny Beach")],
        tip=T("びわ湖高島観光協会のページで確認しました。時間は、少しゆっくり歩いた場合です。", "Checked on the Takashima tourism association’s pages. Times assume an easy pace.")),

    "sakura": dict(
        name=T("海津大崎の桜並木", "Kaizu-Osaki cherry avenue"), kind=T("桜並木", "Cherry avenue"),
        head=T("海津大崎（かいづおおさき）の桜並木", "Kaizu-Osaki cherry avenue"),
        blurb=T("湖岸に約4km、ソメイヨシノが約800本。大崎寺までの2kmは、湖ぎわの遊歩道も歩けます。",
                "About 800 cherry trees along 4 km of shore. For the 2 km to Osakiji there is also a lakeside footpath."),
        lat=35.45414, lng=136.08334,
        body=T("並木の入口から大崎寺までは約2km。ふつうに歩いて30分、写真を撮りながらだと50分〜1時間です。車道のほかに、湖ぎわに歩行者だけの道（近江湖の辺の道）があります。湖へ枝をのばす桜と、沖の竹生島が見えます。\n\n"
               "例年4月はじめに咲きはじめ、5〜6日で満開になります。京都市内より1週間ほど遅めです。満開は2024年が4月8日、2025年が4月12日。年で動くので、観光協会の開花状況を見てから日を決めてください。ライトアップは、観光協会や市では行っていません。",
               "From the entrance to Osakiji is about 2 km: 30 minutes walking, 50–60 with photo stops. Besides the road there is a pedestrian-only path at the water’s edge, with branches over the lake and Chikubu Island offshore.\n\n"
               "The trees usually open in early April and peak 5–6 days later, about a week after Kyoto city. Full bloom was 8 April in 2024 and 12 April in 2025. It moves each year, so check the tourism association’s bloom report before choosing a day. Neither the association nor the city runs a light-up."),
        gmaps=[gm("海津大崎の桜並木", "Kaizu-Osaki cherry avenue", "海津大崎 桜並木")],
        links=[L_SAKURA, L_REG, L_MAP26],
        notices=[N_REG],
        rows=[row("walk", "並木の入口→大崎寺 約2km・30分（写真を撮りながら50分〜1時間）", "Avenue entrance → Osakiji: about 2 km, 30 min (50–60 with photos)"),
              row("toilet", "花見の時期だけ、入口と大崎寺の近くに仮設（2026年春の地図。来春は要確認）。混むのでマキノ駅で先に", "Temporary, in season only, at the entrance and near Osakiji (2026 map; check for next spring). They get busy, so use Makino Station first")],
        tip=T("びわ湖高島観光協会の開花情報・2026年春のお花見マップ・よくある質問で確認しました。", "Checked on the Takashima tourism association’s bloom report, 2026 map and FAQ.")),

    "osakiji": dict(
        name=T("大崎寺・海津大崎港", "Osakiji Temple & Kaizu-Osaki pier"), kind=T("寺・船着き場", "Temple & pier"),
        head=T("大崎寺（おおさきじ）と海津大崎港", "Osakiji Temple and Kaizu-Osaki pier"),
        blurb=T("第一トンネルの手前、石段の上のお寺。ここで引き返すか、先へ歩くかを決めます。",
                "Up the steps before the first tunnel. This is where you turn back or walk on."),
        lat=35.45021, lng=136.08711,
        body=T("「大崎観音」と呼ばれる、奈良時代に開かれたと伝わるお寺です。県道の第一トンネルの手前の石段を上ると、本堂の前から湖が見渡せます。本堂の右手の阿弥陀堂は、安土城の材を使ったという「血天井」で知られています。\n\n"
               "歩くのをへらしたいときは、海津大崎口のバス停（大崎寺から約2.4km・35分）から、コミュニティバスでマキノ駅へ8分・220円。★印の便でないと遠回りです。\n\n"
               "2026年春は、今津港と長浜港から桜クルーズの船も出ました（4月15日で終了、予約優先、4,500円）。写真の船と看板は、春に撮ったものです。今は運航していません。来春は要確認。",
               "Known as “Osaki Kannon” and said to date from the Nara period. Climb the steps before the first road tunnel for a wide view of the lake from the main hall. The Amida hall to its right is known for a “bloody ceiling” said to be made of timber from Azuchi Castle.\n\n"
               "To walk less, take the community bus from Kaizu-Osaki-guchi (2.4 km, 35 minutes from the temple) to Makino Station: 8 minutes, ¥220. Use a run marked ★; the others go the long way.\n\n"
               "In spring 2026 cherry cruises also ran from Imazu and Nagahama (until 15 April, booking preferred, ¥4,500); the boat and signboard in the photos are from past springs. They aren’t running now; check for next spring."),
        gmaps=[gm("大崎寺", "Osakiji", "大崎寺 高島市マキノ町海津"), gm("海津大崎口のバス停", "Kaizu-Osaki-guchi bus stop", "海津大崎口 バス停")],
        links=[link("official", "大崎寺（びわ湖高島観光協会）", "Osakiji (Takashima tourism, Japanese)", OSAKIJI), L_BUS_WD, L_BUS_WE,
               link("info", "桜クルーズ（2026年春の実績・終了）", "Cherry cruise, spring 2026, ended (Japanese)", CRUISE)],
        notices=[],
        rows=[row("walk", "大崎寺→マキノ駅 約3.8km・1時間", "Osakiji → Makino Station: about 3.8 km, 1 hour"),
              row("bus", "海津大崎口→マキノ駅（2026年春の★の便。平日・土休日とも）10:31・11:31・12:31・14:31・15:31・17:31発、8分・220円。13時台に★はありません",
                  "Kaizu-Osaki-guchi → Makino Station, ★ runs in spring 2026, weekdays and weekends: 10:31, 11:31, 12:31, 14:31, 15:31, 17:31; 8 min, ¥220. No ★ bus in the 13:00 hour"),
              row("fee", "大崎寺の拝観料・時間は要確認", "Osakiji admission and hours: please check")],
        tip=T("バスはびわ湖高島観光協会の2026年春の連絡表（平日用・土休日用）で確認。来春は要確認です。", "Buses checked on the association’s spring 2026 weekday and weekend timetables; please check for next spring.")),

    "oura": dict(
        name=T("大浦の湖岸から永原駅へ", "Oura lakeshore to Nagahara Station"), kind=T("湖岸の桜・駅", "Lakeside cherries & station"),
        head=T("大浦（おおうら）の湖岸から永原（ながはら）駅へ", "Oura lakeshore to Nagahara Station"),
        blurb=T("大崎の先、トンネルを抜けて入り江の集落へ。永原駅まで歩き通します。",
                "Through the tunnels beyond Osaki to a village on a cove, and on to Nagahara Station."),
        lat=35.48641, lng=136.11764,
        body=T("大崎寺から大浦までは約6km。4つのトンネルを含む県道は道幅が狭いので、車に気をつけて端を歩いてください。途中にバスはなく、店やトイレも確かめられていません（要確認）。\n\n"
               "大浦から永原駅までは約1.6km・30分。駅は午後4時半で係員がいなくなりますが、ICOCAで乗れます。",
               "Oura is about 6 km from Osakiji. The road, with four tunnels, is narrow, so keep to the side and watch for cars. There is no bus along it, and we couldn’t confirm any shops or toilets (please check).\n\n"
               "From Oura to Nagahara Station is about 1.6 km, 30 minutes. The station is unstaffed after 16:30, but takes ICOCA."),
        gmaps=[gm("大浦", "Oura", "長浜市西浅井町大浦"), gm("JR永原駅", "JR Nagahara Station", "JR永原駅")],
        links=[L_YAHOO, link("info", "永原駅の案内（長浜市）", "Nagahara Station (Nagahama city, Japanese)", STATIONS)],
        notices=[notice("途中でやめられない約6km", "6 km with no way out",
                        "大崎寺を出るのが13:45を過ぎたら、マキノ駅へ引き返してください（約1時間）。雨や強風の日も歩き通さないほうが安心です。",
                        "If it’s past 13:45 when you leave Osakiji, go back to Makino Station instead (about 1 hour). Don’t attempt it in rain or strong wind.")],
        rows=[row("train", "永原→長浜：15:56発→近江塩津で乗り換え→16:27着・510円。次は16:56発→17:27着", "Nagahara → Nagahama: 15:56 → change at Omi-Shiotsu → 16:27, ¥510. Next 16:56 → 17:27"),
              row("train", "永原→京都：16:42発→17:57着・1,340円。最終は22:04発→23:19着", "Nagahara → Kyoto: 16:42 → 17:57, ¥1,340. Last 22:04 → 23:19"),
              row("hours", "永原駅の係員 7:30〜16:30（10:40〜12:00は不在）", "Nagahara Station staffed 7:30–16:30 (not 10:40–12:00)")],
        tip=TRAIN_TIP),

    "chikubushima": dict(
        name=T("竹生島（宝厳寺・都久夫須麻神社）", "Chikubushima (Hogonji & Tsukubusuma Shrine)"), kind=T("島・寺と神社", "Island temple & shrine"),
        head=T("竹生島（ちくぶしま）", "Chikubushima"),
        blurb=T("今津港から船で渡る、宝厳寺と都久夫須麻神社の島。入島料は現金です。",
                "The island of Hogonji and Tsukubusuma Shrine, by boat from Imazu. The island fee is cash only."),
        lat=35.42110, lng=136.14338,
        body=T("琵琶湖の北に浮かぶ小さな島です。港の先で入島料を払い、165段の石段を上ると、西国三十三所の第三十番札所・宝厳寺（ほうごんじ）。国宝の唐門、重要文化財の観音堂と舟廊下（ふなろうか）を通って、都久夫須麻神社（つくぶすまじんじゃ）へ抜けます。\n\n"
               "今津港の乗り場に売店はありません。島には休憩所と土産物屋が2軒ありますが、食事はあてにせず、船に持って乗れます。港にはトイレがあります。",
               "A small island in the north of Lake Biwa. Pay the fee beyond the pier and climb 165 steps to Hogonji, temple 30 of the Saigoku pilgrimage. The Karamon gate (National Treasure), Kannon hall and Funa-roka corridor (Important Cultural Properties) lead through to Tsukubusuma Shrine.\n\n"
               "Imazu pier has no shop. The island has two rest-and-souvenir shops, but don’t count on a meal; you may take food on the boat. The port has toilets."),
        gmaps=[gm("今津港（琵琶湖汽船）", "Imazu port", "今津港 琵琶湖汽船"), gm("竹生島", "Chikubushima", "竹生島 宝厳寺"), gm("長浜港（琵琶湖汽船）", "Nagahama port", "長浜港 琵琶湖汽船")],
        links=[link("timetable", "琵琶湖汽船 竹生島（時刻・料金・予約）", "Biwako Kisen Chikubushima: times, fares and booking (Japanese)", BOAT),
               link("info", "乗船のよくある質問（支払い・予約）", "Boat FAQ: payment and booking (Japanese)", BOAT_FAQ),
               link("official", "竹生島 宝厳寺 公式サイト", "Hogonji, Chikubushima (official, Japanese)", HOGONJI)],
        notices=[notice("予約を。入島料600円は現金だけ", "Book ahead; the ¥600 island fee is cash only",
                        "桜の時期の満席に備えて、前日15:00までにネットで予約を。船代はカードやICも使えますが、島の入島料は現金です。",
                        "Book online by 15:00 the day before in case it fills up in blossom season. The boat takes cards and IC, but the island fee is cash.", url=BOAT_FAQ),
                 notice("強風の日は欠航・着けないことも", "Cancellations in strong wind",
                        "朝に琵琶湖汽船の運航状況を確かめ、欠航なら近江今津13:43発の電車で長浜へ（14:27着・770円）。",
                        "Check the operator that morning. If cancelled, take the 13:43 train from Omi-Imazu to Nagahama (14:27, ¥770).", url=BOAT),
                 notice("2027年4月の船は未発表", "April 2027 boats not yet announced",
                        "ここに書いた時刻と料金は、2026年4月〜2027年3月の時刻表です。来春は要確認。",
                        "The times and fares here are from the April 2026 – March 2027 timetable. Please check for next spring.", url=BOAT, to="2027-03-31")],
        rows=[row("boat", "びわ湖横断（2026年4月は毎日）：今津港9:30・10:45・12:00・13:10発→長浜港11:30・12:55・14:20・15:45着。4月24日までは13:10が最後の便",
                  "Lake crossing, daily in April 2026: Imazu 9:30, 10:45, 12:00, 13:10 → Nagahama 11:30, 12:55, 14:20, 15:45. Until 24 April the 13:10 was the last"),
              row("fee", "船 大人3,600円・小学生1,800円。入島料 中学生以上600円・小人300円", "Boat ¥3,600, primary school ¥1,800. Island fee ¥600 (junior high and up), children ¥300"),
              row("hours", "宝厳寺 9:30〜16:30（船の時刻に合わせて）", "Hogonji 9:30–16:30 (in line with the boats)")],
        cash=True,
        tip=T("船と入島料は琵琶湖汽船、お寺は宝厳寺の公式サイトで確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
              "Boat and fee checked with Biwako Kisen, the temple on Hogonji’s website. Photos are from Wikimedia Commons (author and license shown on each).")),

    "kurokabe": dict(
        name=T("黒壁スクエア", "Kurokabe Square"), kind=T("古い町並み・ガラス", "Old streets & glass"),
        head=T("黒壁（くろかべ）スクエア", "Kurokabe Square"),
        blurb=T("明治の銀行を生かしたガラス館と、北国街道の古い町家。ガラス館は17:00までです。",
                "A glass house in a Meiji bank, among old townhouses on the Hokkoku-kaido. It closes at 17:00."),
        lat=35.38068, lng=136.26708,
        body=T("明治33年に建てられた銀行が、今の黒壁一號館（黒壁ガラス館）です。北国街道（ほっこくかいどう）沿いに、町家を使ったガラスの店やギャラリーが並びます。\n\n"
               "表通りだけでなく、町の中を流れる米川や、大通寺の表参道の路地へも。長浜駅の東口から歩いて5〜6分です。",
               "The 1900 bank is now Kurokabe No. 1, the Glass House. Glass shops and galleries fill the townhouses along the Hokkoku-kaido.\n\n"
               "Step off the main street to the little Yone river and the lanes on the approach to Daitsuji. It’s 5–6 minutes from the east exit of Nagahama Station."),
        gmaps=[gm("黒壁ガラス館", "Kurokabe Glass House", "黒壁ガラス館")],
        links=[link("official", "黒壁ガラス館（時間・休み）", "Kurokabe Glass House: hours (Japanese)", GLASS)],
        notices=[],
        rows=[row("hours", "黒壁ガラス館 10:00〜17:00（2026年3月31日は16:00まで）。ほかの店は要確認", "Glass House 10:00–17:00 (until 16:00 on 31 Mar 2026). Other shops: please check"),
              row("closed", "黒壁ガラス館は定休日なし", "Glass House: no regular closing day")],
        tip=T("黒壁の公式サイトで確認しました。", "Checked on the Kurokabe website.")),

    "tetsudo": dict(
        name=T("長浜鉄道スクエア", "Nagahama Railway Square"), kind=T("鉄道の博物館", "Railway museum"),
        head=T("長浜鉄道スクエア", "Nagahama Railway Square"),
        blurb=T("現存する日本最古の駅舎と、蒸気機関車・電気機関車の展示。", "Japan’s oldest surviving station building, with steam and electric locomotives."),
        lat=35.37670, lng=136.26600,
        body=T("明治15年にできた旧長浜駅舎は、現存する日本で最も古い駅舎です。となりの記念館には、D51形蒸気機関車とED70形電気機関車が並びます。長浜駅の西口から歩いて3分です。",
               "The old Nagahama Station of 1882 is Japan’s oldest surviving station building. The hall next door has a D51 steam locomotive and an ED70 electric. It’s 3 minutes from the west exit."),
        gmaps=[gm("長浜鉄道スクエア", "Nagahama Railway Square", "長浜鉄道スクエア")],
        links=[link("official", "長浜鉄道スクエア（時間・料金）", "Nagahama Railway Square: hours and fees (Japanese)", TETSU)],
        notices=[],
        rows=[row("hours", "9:30〜17:00（入館16:30まで）", "9:30–17:00 (last entry 16:30)"),
              row("fee", "大人500円、小中学生200円", "¥500 adults, ¥200 children"),
              row("closed", "12月29日〜1月3日", "29 Dec – 3 Jan")],
        tip=T("長浜鉄道スクエアの公式ページで確認しました。", "Checked on the museum’s official page.")),

    "keiunkan": dict(
        name=T("慶雲館", "Keiunkan"), kind=T("庭園・迎賓館", "Garden & guesthouse"),
        head=T("慶雲館（けいうんかん）", "Keiunkan"),
        blurb=T("明治天皇を迎えた迎賓館と、小川治兵衛の庭。写真は冬の盆梅展のときのものです。",
                "A guesthouse for Emperor Meiji with a garden by Ogawa Jihei. The photos show the winter bonsai show."),
        lat=35.37581, lng=136.26634,
        body=T("明治20年に、明治天皇の休憩所として建てられました。国の名勝の庭は、7代目小川治兵衛（植治）の作です。鉄道スクエアのすぐ近くです。\n\n"
               "写真の梅の盆栽は、2025年1月の長浜盆梅展のもの。桜の時期には並んでいません。春は庭と建物の公開です。",
               "Built in 1887 as a resting place for Emperor Meiji. The garden, a national Place of Scenic Beauty, is by Ogawa Jihei VII (Ueji). It’s beside the Railway Square.\n\n"
               "The plum bonsai in the photos are from the January 2025 Bonbai-ten and aren’t there in cherry season, when the garden and buildings are open."),
        gmaps=[gm("慶雲館", "Keiunkan", "慶雲館 長浜")],
        links=[link("official", "慶雲館（時間・料金）", "Keiunkan: hours and fees (Japanese)", KEIUN),
               link("info", "休館の期間（長浜観光協会）", "Closing periods (Nagahama tourism, Japanese)", KEIUN_OFF),
               link("official", "長浜盆梅展 公式サイト", "Nagahama Bonbai-ten (official, Japanese)", BONBAI)],
        notices=[notice("12月1日〜1月9日は休館", "Closed 1 Dec – 9 Jan",
                        "盆梅展の準備のため、2026年12月1日〜2027年1月9日は入れません。", "Closed 1 Dec 2026 – 9 Jan 2027 to prepare the bonsai show.",
                        url=KEIUN_OFF, to="2027-01-09"),
                 notice("3月11日から下旬までは休館", "Closed 11 to late March",
                        "盆梅展の片づけのため休館。開く日は要確認。", "Closed after the bonsai show; please check the reopening date.",
                        url=KEIUN_OFF, frm="2027-03-01", to="2027-03-31")],
        rows=[row("hours", "9:30〜17:00（入館16:30まで）", "9:30–17:00 (last entry 16:30)"),
              row("fee", "大人300円、小中学生150円", "¥300 adults, ¥150 children"),
              row("hours", "長浜盆梅展2027：1月10日〜3月10日、9:00〜17:00（入館16:30まで）・大人1,000円", "Bonbai-ten 2027: 10 Jan – 10 Mar, 9:00–17:00 (last entry 16:30), ¥1,000 adults", until="2027-03-10"),
              row("closed", "12月上旬〜1月上旬、3月11日〜下旬", "Early Dec – early Jan, and 11 to late March")],
        tip=T("慶雲館・長浜観光協会・長浜盆梅展の公式ページで確認しました。", "Checked on the Keiunkan, Nagahama tourism and Bonbai-ten pages.")),

    "nagahamajo": dict(
        name=T("豊公園・長浜城", "Hoko Park & Nagahama Castle"), kind=T("桜の公園・城", "Cherry park & castle"),
        head=T("豊公園（ほうこうえん）と長浜城（ながはまじょう）", "Hoko Park and Nagahama Castle"),
        blurb=T("湖のほとりに約600本の桜。公園はいつでも入れて、天守は16:30までの受付です。",
                "Some 600 cherry trees by the lake. The park is always open; the castle’s last entry is 16:30."),
        lat=35.37766, lng=136.26128,
        body=T("秀吉が初めて持った城の跡で、今の天守は昭和58年に再建された長浜城歴史博物館です。最上階からは琵琶湖と竹生島、足もとに公園の桜が見えます。\n\n"
               "豊公園は日本さくら名所100選。2026年は4月3日に満開で、海津大崎と同じ日に見られるかどうかは年によります。咲いている間は臨時の明かり（ぼんぼり）がつきます（2026年は4月13日で終了。点灯の時間と来春の予定は要確認）。夕方は湖岸へ出てみてください。写真は2025年1月のもので、桜は写っていません。",
               "The site of Hideyoshi’s first castle. The keep, rebuilt in 1983, is the Nagahama Castle History Museum, with Lake Biwa and Chikubu Island from the top and the park’s blossom below.\n\n"
               "Hoko Park is one of Japan’s 100 best cherry spots. Full bloom was 3 April in 2026; whether it coincides with Kaizu-Osaki varies by year. Temporary lanterns are lit during the bloom (until 13 April in 2026; hours and next spring’s plans: please check). Go out to the shore in the evening. The photos are from January 2025, before the blossom."),
        gmaps=[gm("豊公園", "Hoko Park", "豊公園 長浜"), gm("長浜城歴史博物館", "Nagahama Castle History Museum", "長浜城歴史博物館")],
        links=[link("official", "長浜城歴史博物館（時間・休み・料金）", "Nagahama Castle History Museum: hours and fees (Japanese)", CASTLE),
               link("info", "豊公園（長浜観光協会）", "Hoko Park (Nagahama tourism, Japanese)", PARK),
               link("info", "豊公園の桜（2026年春の実績）", "Hoko Park blossom, spring 2026 (Japanese)", PARK_2026)],
        notices=[],
        rows=[row("hours", "公園は24時間。長浜城 9:00〜17:00（受付16:30まで）", "Park open 24 hours. Castle 9:00–17:00 (last entry 16:30)"),
              row("fee", "公園は無料。長浜城 大人500円、小中学生200円（企画展で変わることがあります）", "Park free. Castle ¥500 adults, ¥200 children (may change during special exhibitions)"),
              row("closed", "長浜城は月曜（祝日なら次の平日）、12月27日〜1月2日、展示替えの日。展示品は撮影禁止", "Castle closed Mondays (next weekday if a holiday), 27 Dec – 2 Jan and changeover days. No photographing exhibits")],
        tip=T("長浜城歴史博物館・長浜市・長浜観光協会のページで確認しました。", "Checked on the museum, Nagahama city and tourism association pages.")),

    "nagahamaeki": dict(
        name=T("JR長浜駅（帰り）", "JR Nagahama Station (heading home)"), kind=T("駅・夜", "Station & evening"),
        head=T("JR長浜駅（ながはまえき）から京都へ", "JR Nagahama Station, back to Kyoto"),
        blurb=T("京都まで新快速で約1時間15分。夜は本数が減ります。", "About 1 h 15 min to Kyoto by Special Rapid. Fewer trains at night."),
        lat=35.37845, lng=136.26532,
        body=T("帰りは琵琶湖線です。京都駅のほか、山科で地下鉄東西線に乗り換えれば三条京阪へ出られます（1,430円）。",
               "Home is by the Biwako Line: to Kyoto Station, or change at Yamashina to the Tozai subway for Sanjo-Keihan (¥1,430)."),
        gmaps=[gm("JR長浜駅", "JR Nagahama Station", "JR長浜駅")],
        links=[L_YAHOO, L_TRAFFIC],
        notices=[N_LAST_TRAIN],
        rows=[row("train", "長浜→京都：17:57→19:12、18:28→19:42、18:57→20:12、19:28→20:42（土日祝20:47）、19:57→21:12（土日祝21:07）、20:36→21:48（米原で乗り換え）、21:17→22:28、最終22:15→23:50",
                  "Nagahama → Kyoto: 17:57→19:12, 18:28→19:42, 18:57→20:12, 19:28→20:42 (weekends and holidays 20:47), 19:57→21:12 (21:07), 20:36→21:48 (change at Maibara), 21:17→22:28, last 22:15→23:50"),
              row("fee", "長浜→京都 1,340円", "Nagahama → Kyoto ¥1,340")],
        tip=TRAIN_TIP),
}
EXTRA = {"chikubushima": [
    cc("chikubushima-1.jpg", "HAL-Guandu", "CC BY-SA 4.0", "Chikubushima-2016-07-21.jpg"),
    cc("chikubushima-2.jpg", "Saigen Jiro", "CC0", "Tsukubusuma-jinja honden-1.jpg"),
    cc("chikubushima-3.jpg", "Brakeet", "CC0", "Chikubu Island DSCN1995.jpg"),
    cc("chikubushima-4.jpg", "Brakeet", "CC0", "Chikubu Island DSCN2013.jpg"),
]}

# ---------------------------------------------------------------------------
# 何度も使う、コースごとの部品
# ---------------------------------------------------------------------------
ROW_OUT_LATE = row("train", "行き：京都9:45発（平日9:48発）→ マキノ10:50着、湖西線の新快速。次は10:45発→11:50着、その次は11:45発→12:50着",
                   "Out: Kyoto 9:45 (weekdays 9:48) → Makino 10:50, Kosei Line Special Rapid. Next 10:45 → 11:50, then 11:45 → 12:50")
ROW_OUT_EARLY = row("train", "行き：京都7:00発→近江今津7:59着・8:04発→マキノ8:12着。次は8:15発（平日8:19発）→9:30着",
                    "Out: Kyoto 7:00 → Omi-Imazu 7:59, change for the 8:04 → Makino 8:12. Next 8:15 (weekdays 8:19) → 9:30")
ROW_SANJO_LATE = row("train", "三条京阪から：9:28発（平日9:37発）→山科で乗り換え→マキノ10:50着",
                     "From Sanjo-Keihan: 9:28 (weekdays 9:37) → change at Yamashina → Makino 10:50")
ROW_SANJO_EARLY = row("train", "三条京阪から：6:39発→山科7:05発→近江今津で乗り換え→マキノ8:12着",
                      "From Sanjo-Keihan: 6:39 → Yamashina 7:05 → change at Omi-Imazu → Makino 8:12")
ROW_DINNER = row("food", "長濱浪漫ビール：平日11:30〜15:00（LO14:30）・17:00〜21:00（LO20:15）、土日祝11:30〜21:00（LO20:15）。火曜休み（営業日カレンダーで確認）",
                 "Nagahama Roman Beer: weekdays 11:30–15:00 (LO 14:30) and 17:00–21:00 (LO 20:15); weekends and holidays 11:30–21:00 (LO 20:15). Closed Tuesdays (check its calendar)")
ROW_RAMEN = row("food", "京都拉麺小路（京都駅ビル10階）：11:00〜22:00（LO21:30）", "Kyoto Ramen Koji (Station Building 10F): 11:00–22:00 (LO 21:30)")
GM_ROMAN = gm("長濱浪漫ビール", "Nagahama Roman Beer", "長濱浪漫ビール 長浜市朝日町14-1")
GM_RAMEN = gm("京都拉麺小路", "Kyoto Ramen Koji", "京都拉麺小路 京都駅ビル")
N_ROMAN = notice("長濱浪漫ビールは火曜休み、予約は前日まで", "Roman Beer: closed Tuesdays; book by the day before",
                 "当日の予約は受けていません。火曜や満席なら、長浜18:28か18:57の電車で帰って京都駅で晩ごはんを（京都拉麺小路はLO21:30）。",
                 "No same-day bookings. On a Tuesday, or if it’s full, take the 18:28 or 18:57 and eat at Kyoto Station (Ramen Koji last order 21:30).", url=ROMAN)
N_CASTLE_LATE = notice("この時間割では天守に入れません", "No time for the castle keep on this course",
                       "長浜城の受付は16:30まで。天守に上りたい日は、7:00発のコースに切り替えてください（月曜は休館）。公園は夜も歩けます。",
                       "Castle entry ends at 16:30. To go up, switch to a 7:00 course (closed Mondays). The park stays open at night.", url=CASTLE)
N_MONDAY = notice("長浜城は月曜休み", "The castle is closed on Mondays",
                  "祝日なら開いて、次の平日が休みです。休みの日は公園の桜と湖岸をゆっくり。",
                  "It opens on holiday Mondays and closes the next weekday. On closed days, take your time in the park and by the lake.", url=CASTLE)

C_CASTLE_LATE = T("天守の受付は16:30まで。このコースでは公園だけ", "Castle entry ends 16:30; park only on this course")
C_MONDAY = T("天守は月曜休み、受付16:30まで", "Castle closed Mondays; last entry 16:30")
C_ROMAN = T("晩ごはんの店は火曜休み。終電22:15（米原乗り換え）", "Dinner stop closed Tuesdays; last train 22:15 via Maibara")

EVENING_LATE = T(
    "豊公園から東口側へ歩いて10〜15分。晩ごはんは駅から4分の長濱浪漫ビール（米蔵を改装したビアホール）で18:30〜20:15ごろ。20:36発に乗ると、米原で乗り換えて京都21:48着です。乗り遅れたら21:17発→22:28着。\n\n"
    "京都駅で食べたいなら、18:28発→19:42着か、18:57発→20:12着に。京都拉麺小路はラストオーダー21:30です。",
    "It’s 10–15 minutes from the park to the east side of the station. Have dinner about 18:30–20:15 at Nagahama Roman Beer, a beer hall in an old rice storehouse 4 minutes from the station. The 20:36 changes at Maibara and reaches Kyoto at 21:48; if you miss it, the 21:17 arrives at 22:28.\n\n"
    "To eat at Kyoto Station instead, take the 18:28 (19:42) or 18:57 (20:12). Ramen Koji takes last orders at 21:30.")

KUROKABE_LATE = T(
    "長浜駅に16:27に着いたら、まっすぐ黒壁ガラス館へ（16:35ごろ）。17:00に閉まるので、見たい物を先に。そのあと駅の西側の豊公園へ歩いて約20分です。",
    "Arriving at Nagahama at 16:27, go straight to the Glass House (about 16:35). It closes at 17:00, so see what you want first. Then it’s about 20 minutes’ walk to Hoko Park, west of the station.")
PARK_LATE = T(
    "17:20ごろ着いて、桜の下から湖岸へ。1時間ほどいて、暗くなるころに晩ごはんへ向かいます。",
    "Arrive about 17:20, walk under the blossom to the shore, stay an hour or so and head for dinner as it gets dark.")

EARLY_MAKINO = T(
    "京都駅7:00発の近江今津行きに乗ります。近江今津7:59着、8:04発に乗り換えてマキノ8:12着。朝ごはんと飲み物は京都駅で乗る前に（早い時間なので、前の日に買っておくと確実です）。\n\n"
    "8:20に歩きはじめ、浜には寄らずに海津へ（30分）。乗り遅れたら8:15発（平日8:19発）でマキノ9:30着。次のコース（9:45ごろ発）に近い動きになります。",
    "Take the 7:00 from Kyoto bound for Omi-Imazu (7:59), change to the 8:04 and reach Makino at 8:12. Get breakfast and drinks before boarding (safer bought the night before at that hour).\n\n"
    "Set off at 8:20 straight for Kaizu, skipping the beach (30 minutes). If you miss the train, the 8:15 (weekdays 8:19) reaches Makino at 9:30; your day will then be closer to the 9:45 courses.")
EARLY_KAIZU = T(
    "8:50に着いて、浜で朝ごはん。9:05に出れば、並木の入口はすぐです。",
    "Arrive at 8:50 and have breakfast by the lake. Leave at 9:05; the avenue starts just beyond.")
EARLY_SAKURA = T(
    "9:10から50分かけて大崎寺へ。2026年の交通規制は9:30からでした。人と車が増える前に写真を。",
    "Walk to Osakiji from 9:10, taking 50 minutes. The 2026 restrictions began at 9:30, so take photos before people and cars build up.")

# ---------------------------------------------------------------------------
# コース。spots の順がそのまま番号になる。when はめやすの時間、go はその時間割での動き方
# ---------------------------------------------------------------------------
SEC_EAST = lambda ja, en: (T("マキノ・海津大崎", "Makino & Kaizu-Osaki"), T(ja, en))
SEC_WEST = lambda ja, en: (T("長浜", "Nagahama"), T(ja, en))

COURSES = {
    "late": dict(
        file="kohoku.json",
        secs=[(4, SEC_EAST("お昼を持って、桜並木を往復", "Pack lunch; there and back along the avenue")),
              (7, SEC_WEST("夕方の町と豊公園、晩ごはん", "The town and park at dusk, then dinner"))],
        spots=[
            dict(id="makino", when=("10:50〜11:45", "10:50–11:45"),
                 go=T("京都駅9:45発（平日は9:48発）の湖西線の新快速で、マキノ10:50着。お昼と飲み物は乗る前に京都駅で買います。駅でトイレを済ませて11:05に出発、サニービーチで11:20〜11:45に早めのお昼。海津へは湖岸を35分です。\n\n"
                      "乗り遅れたら10:45発→11:50着。浜をやめて海津でお昼にすれば、そのあとは同じ時間割に戻れます。",
                      "Take the 9:45 Kosei Line Special Rapid from Kyoto (weekdays 9:48), arriving Makino 10:50. Buy lunch and drinks at Kyoto Station first. Use the toilet, leave at 11:05 and eat early on Sunny Beach, 11:20–11:45. Kaizu is 35 minutes along the shore.\n\n"
                      "If you miss it, the 10:45 arrives at 11:50: skip the beach, eat in Kaizu and you’re back on schedule."),
                 caution=T("お昼は京都で買って行く", "Buy lunch in Kyoto"),
                 rows=[ROW_OUT_LATE, ROW_SANJO_LATE]),
            dict(id="kaizu", when=("12:20〜12:40", "12:20–12:40"),
                 go=T("浜から35分で12:20着。石積みを湖の側から見て、12:40に並木の入口へ。",
                      "35 minutes from the beach, arriving 12:20. See the wall from the lake side and go on to the avenue at 12:40.")),
            dict(id="sakura", when=("12:45〜13:45", "12:45–13:45"),
                 go=T("行きは写真を撮りながら1時間。帰りも同じ道なので、行きに車道、帰りに湖ぎわの遊歩道と分けても。",
                      "Allow an hour out with photos. You return the same way, so try the road one way and the lakeside path the other."),
                 caution=T("見ごろの土日は交通規制", "Restrictions on peak weekends")),
            dict(id="osakiji", when=("13:50〜14:20", "13:50–14:20"),
                 go=T("14:20に引き返して、マキノ駅へ約1時間（15:25ごろ着）。15:51発の電車で、近江塩津で乗り換えて長浜16:27着（680円）。疲れたら海津大崎口15:31発のバス（2026年春の時刻）でも、15:51発に間に合います。\n\n"
                      "乗り遅れたら16:51発→長浜17:27着。黒壁をやめて豊公園へ。その次は17:50発→18:27着です。",
                      "Turn back at 14:20: about an hour to Makino Station (15:25). The 15:51, changing at Omi-Shiotsu, reaches Nagahama at 16:27 (¥680). If tired, the 15:31 bus from Kaizu-Osaki-guchi (spring 2026 time) also makes the 15:51.\n\n"
                      "If you miss it, the 16:51 reaches Nagahama at 17:27: skip Kurokabe for the park. The one after is 17:50 → 18:27."),
                 caution=T("14:20に引き返す。マキノ駅まで1時間", "Turn back at 14:20; 1 hour to the station"),
                 rows=[row("train", "マキノ15:51発→近江塩津で乗り換え→長浜16:27着・680円。次は16:51→17:27、17:50→18:27", "Makino 15:51 → change at Omi-Shiotsu → Nagahama 16:27, ¥680. Then 16:51→17:27, 17:50→18:27")]),
            dict(id="kurokabe", when=("16:35〜17:00", "16:35–17:00"), go=KUROKABE_LATE,
                 caution=T("ガラス館は17:00まで", "Glass House closes 17:00")),
            dict(id="nagahamajo", when=("17:20〜18:15", "17:20–18:15"), go=PARK_LATE, caution=C_CASTLE_LATE, notices=[N_CASTLE_LATE]),
            dict(id="nagahamaeki", when=("18:30〜20:36", "18:30–20:36"), go=EVENING_LATE, caution=C_ROMAN,
                 notices=[N_ROMAN], rows=[ROW_DINNER, ROW_RAMEN], links=[L_ROMAN, L_RAMEN], gmaps=[GM_ROMAN, GM_RAMEN]),
        ],
        hints=[("osakiji", {"any": ["kaizu", "sakura", "osakiji"], "none": ["kurokabe", "nagahamajo"]},
                T("長浜へ行かない日は、マキノ15:47発の新快速で京都16:57着（1,170円）。次は16:47発→17:57着。",
                  "Skipping Nagahama: the 15:47 Special Rapid from Makino reaches Kyoto at 16:57 (¥1,170); next 16:47 → 17:57."))]),

    "through": dict(
        file="kohoku-through.json",
        secs=[(5, SEC_EAST("永原駅まで約11.5km、歩き通す", "About 11.5 km on foot to Nagahara")),
              (8, SEC_WEST("夕方の町と豊公園、晩ごはん", "The town and park at dusk, then dinner"))],
        spots=[
            dict(id="makino", when=("10:50〜11:05", "10:50–11:05"),
                 go=T("京都駅9:45発（平日は9:48発）の湖西線の新快速で、マキノ10:50着。お昼と、午後の分の飲み物も乗る前に京都駅で。駅でトイレを済ませ、浜には寄らずに11:05に出発します。\n\n"
                      "乗り遅れて10:45発（11:50着）になったら、このコースはやめて「桜並木を往復」に切り替えてください。",
                      "Take the 9:45 Kosei Line Special Rapid from Kyoto (weekdays 9:48), arriving Makino 10:50. Buy lunch and drinks for the afternoon first. Use the toilet and leave at 11:05, skipping the beach.\n\n"
                      "If you’re on the 10:45 (arriving 11:50) instead, switch to the there-and-back course."),
                 caution=T("お昼と飲み物は京都で。約11.5km歩きます", "Pack food and drink; about 11.5 km on foot"),
                 rows=[ROW_OUT_LATE, ROW_SANJO_LATE]),
            dict(id="kaizu", when=("11:35〜12:00", "11:35–12:00"),
                 go=T("駅から30分で11:35着。石積みの下の浜でお昼にして、12:00に出ます。",
                      "30 minutes from the station, arriving 11:35. Eat on the shore below the wall and leave at 12:00.")),
            dict(id="sakura", when=("12:05〜13:00", "12:05–13:00"),
                 go=T("写真を撮りながら55分で大崎寺へ。引き返さないので、撮るなら行きに。",
                      "55 minutes to Osakiji with photos. You won’t come back this way, so take them now."),
                 caution=T("見ごろの土日は交通規制", "Restrictions on peak weekends")),
            dict(id="osakiji", when=("13:00〜13:20", "13:00–13:20"),
                 go=T("トイレ（花見の時期の仮設）はここで。13:20に出て、大浦まで約6km・1時間35分。13:45を過ぎていたら、マキノ駅へ引き返してください。15:51発の電車なら、長浜に同じ16:27に着きます。",
                      "Use the temporary toilet here (in season). Leave at 13:20 for Oura: about 6 km, 1 h 35 min. If it’s past 13:45, return to Makino Station; its 15:51 train reaches Nagahama at the same 16:27."),
                 caution=T("先へ進むなら13:45までに", "Walk on only before 13:45"),
                 rows=[row("train", "引き返す場合：マキノ15:51発→長浜16:27着・680円", "If turning back: Makino 15:51 → Nagahama 16:27, ¥680")]),
            dict(id="oura", when=("14:55〜15:56", "14:55–15:56"),
                 go=T("14:55に着いて湖岸で15分休み、15:10に出ると永原駅15:40着。15:56発で、近江塩津で乗り換えて長浜16:27着です。\n\n乗り遅れたら16:56発→17:27着。黒壁をやめて豊公園へ。",
                      "Arrive 14:55, rest 15 minutes by the lake and leave at 15:10 to reach Nagahara at 15:40. The 15:56, changing at Omi-Shiotsu, reaches Nagahama at 16:27.\n\nIf you miss it, the 16:56 arrives at 17:27: skip Kurokabe for the park."),
                 caution=T("途中にバスなし。永原15:56発", "No bus on the way; train at 15:56")),
            dict(id="kurokabe", when=("16:35〜17:00", "16:35–17:00"), go=KUROKABE_LATE,
                 caution=T("ガラス館は17:00まで", "Glass House closes 17:00")),
            dict(id="nagahamajo", when=("17:20〜18:15", "17:20–18:15"), go=PARK_LATE, caution=C_CASTLE_LATE, notices=[N_CASTLE_LATE]),
            dict(id="nagahamaeki", when=("18:30〜20:36", "18:30–20:36"), go=EVENING_LATE, caution=C_ROMAN,
                 notices=[N_ROMAN], rows=[ROW_DINNER, ROW_RAMEN], links=[L_ROMAN, L_RAMEN], gmaps=[GM_ROMAN, GM_RAMEN]),
        ],
        hints=[("oura", {"any": ["oura"], "none": ["kurokabe", "nagahamajo"]},
                T("長浜へ行かない日は、永原16:42発の新快速で京都17:57着（1,340円）。",
                  "Skipping Nagahama: the 16:42 Special Rapid from Nagahara reaches Kyoto at 17:57 (¥1,340).")),
               ("osakiji", {"any": ["kaizu", "sakura", "osakiji"], "none": ["oura"]},
                T("大浦まで歩かない日は「桜並木を往復」のコースに切り替えると、時間割が合います。",
                  "Not walking to Oura? Switch to the there-and-back course for times that fit."))]),

    "early": dict(
        file="kohoku-early.json",
        secs=[(4, SEC_EAST("混む前の桜並木を朝に歩く", "The avenue before it fills up")),
              (9, SEC_WEST("お昼から城下町をひと回り", "The castle town from lunchtime"))],
        spots=[
            dict(id="makino", when=("8:12〜8:20", "8:12–8:20"), go=EARLY_MAKINO,
                 caution=T("7:00発。朝ごはんは買って行く", "7:00 start; bring breakfast"),
                 rows=[ROW_OUT_EARLY, ROW_SANJO_EARLY]),
            dict(id="kaizu", when=("8:50〜9:05", "8:50–9:05"), go=EARLY_KAIZU),
            dict(id="sakura", when=("9:10〜10:00", "9:10–10:00"), go=EARLY_SAKURA,
                 caution=T("2026年の規制は9:30から", "2026 restrictions began at 9:30")),
            dict(id="osakiji", when=("10:00〜10:25", "10:00–10:25"),
                 go=T("10:25に引き返して、マキノ駅へ約1時間（11:25ごろ着）。11:51発の電車で、近江塩津で乗り換えて長浜12:27着（680円）。\n\n乗り遅れたら12:51発→13:27着。お昼のあと、鉄道スクエアか慶雲館を1つ外します。",
                      "Turn back at 10:25: about an hour to Makino Station (11:25). The 11:51, changing at Omi-Shiotsu, reaches Nagahama at 12:27 (¥680).\n\nIf you miss it, the 12:51 arrives at 13:27: after lunch, drop either the Railway Square or Keiunkan."),
                 caution=T("10:25に引き返す", "Turn back at 10:25"),
                 rows=[row("train", "マキノ11:51発→近江塩津で乗り換え→長浜12:27着・680円。次は12:51→13:27", "Makino 11:51 → change at Omi-Shiotsu → Nagahama 12:27, ¥680. Next 12:51→13:27")]),
            dict(id="kurokabe", when=("12:35〜14:25", "12:35–14:25"),
                 go=T("お昼は駅から4分の長濱浪漫ビールで12:35〜13:30（平日のラストオーダー14:30、火曜休み）。そのあと北国街道とガラス館を14:25ごろまで。火曜は黒壁のまわりで開いている店を探してください。",
                      "Lunch 12:35–13:30 at Nagahama Roman Beer, 4 minutes from the station (last order 14:30 on weekdays, closed Tuesdays). Then the old street and Glass House until about 14:25. On Tuesdays, look for an open place around Kurokabe."),
                 caution=T("お昼の店は火曜休み", "Lunch stop closed Tuesdays"),
                 rows=[ROW_DINNER], links=[L_ROMAN], gmaps=[GM_ROMAN]),
            dict(id="tetsudo", when=("14:40〜15:15", "14:40–15:15"),
                 go=T("黒壁から駅の西側へ約15分。35分ほど見て、すぐ近くの慶雲館へ。",
                      "About 15 minutes from Kurokabe to the west side of the station. Spend 35 minutes, then Keiunkan is close by.")),
            dict(id="keiunkan", when=("15:20〜15:55", "15:20–15:55"),
                 go=T("庭と建物を35分。15:55に出ると、長浜城へ歩いて10分です。",
                      "35 minutes in the garden and buildings. Leave at 15:55; the castle is 10 minutes’ walk."),
                 caution=T("3月11日〜下旬は休館", "Closed 11 to late March")),
            dict(id="nagahamajo", when=("16:05〜18:10", "16:05–18:10"),
                 go=T("16:05に入って最上階へ（受付16:30まで、17:00閉館）。そのあと公園の桜と湖岸を18:10ごろまで。",
                      "Go in at 16:05 and up to the top (last entry 16:30, closes 17:00). Then blossom and shore until about 18:10."),
                 caution=C_MONDAY, notices=[N_MONDAY]),
            dict(id="nagahamaeki", when=("18:20〜18:28", "18:20–18:28"),
                 go=T("18:28発で京都19:42着。晩ごはんは京都駅ビル10階の京都拉麺小路（22:00まで、ラストオーダー21:30）か、地下鉄で三条へ出て街なかで。21〜22時ごろまで遊べます。\n\n乗り遅れたら18:57発→20:12着、その次は19:28発→20:42着（土日祝20:47着）。",
                      "The 18:28 reaches Kyoto at 19:42. Have dinner at Ramen Koji on the 10th floor of the station building (until 22:00, last order 21:30), or take the subway to Sanjo and stay out in town until 21:00–22:00.\n\nIf you miss it: 18:57 → 20:12, then 19:28 → 20:42 (20:47 on weekends and holidays)."),
                 caution=T("18:28発で京都へ。晩ごはんは京都で", "18:28 to Kyoto; dinner there"),
                 rows=[ROW_RAMEN], links=[L_RAMEN], gmaps=[GM_RAMEN]),
        ],
        hints=[("osakiji", {"any": ["kaizu", "sakura", "osakiji"], "none": ["kurokabe", "tetsudo", "keiunkan", "nagahamajo"]},
                T("長浜へ行かない日は、マキノ11:47発の新快速で京都12:58着（1,170円）。午後は京都で。",
                  "Skipping Nagahama: the 11:47 Special Rapid from Makino reaches Kyoto at 12:58 (¥1,170), leaving the afternoon for Kyoto.")),
               ("nagahamaeki", {"any": ["kurokabe", "tetsudo", "keiunkan", "nagahamajo"], "none": ["kaizu", "sakura", "osakiji"]},
                T("長浜だけの日は、京都10:00発の琵琶湖線の新快速で11:10着（1,340円）。",
                  "Nagahama only: the 10:00 Biwako Line Special Rapid from Kyoto arrives at 11:10 (¥1,340)."))]),

    "island": dict(
        file="kohoku-island.json",
        secs=[(4, SEC_EAST("混む前の桜並木を朝に歩く", "The avenue before it fills up")),
              (5, (T("今津港 → 竹生島", "Imazu → Chikubushima"), T("13:10の船で湖を渡る", "The 13:10 boat across the lake"))),
              (8, SEC_WEST("天守と桜、夜の長浜", "Castle, blossom and evening"))],
        spots=[
            dict(id="makino", when=("8:12〜8:20", "8:12–8:20"), go=EARLY_MAKINO,
                 caution=T("7:00発。船は前日までに予約", "7:00 start; book the boat a day ahead"),
                 rows=[ROW_OUT_EARLY, ROW_SANJO_EARLY]),
            dict(id="kaizu", when=("8:50〜9:05", "8:50–9:05"), go=EARLY_KAIZU),
            dict(id="sakura", when=("9:10〜10:00", "9:10–10:00"), go=EARLY_SAKURA,
                 caution=T("2026年の規制は9:30から", "2026 restrictions began at 9:30")),
            dict(id="osakiji", when=("10:00〜10:20", "10:00–10:20"),
                 go=T("10:20に引き返して、マキノ駅へ約1時間（11:20ごろ着）。11:47発の新快速で近江今津11:58着（200円）。お昼は駅のまわりで12:40まで（店の時間は要確認。心配なら朝に2食分買っておく）。港へは歩いて5分です。\n\n"
                      "次の12:47発→12:58着では乗船手続きの時間が足りないので、11:47発に乗り遅れそうなら竹生島はやめて、12:51発で長浜へ（13:27着）。",
                      "Turn back at 10:20: about an hour to Makino Station (11:20). The 11:47 Special Rapid reaches Omi-Imazu at 11:58 (¥200). Lunch near the station until 12:40 (check shop hours, or buy two meals in the morning). The port is 5 minutes’ walk.\n\n"
                      "The next train (12:47 → 12:58) leaves too little time to check in, so if you’ll miss the 11:47, drop the island and take the 12:51 to Nagahama (13:27)."),
                 caution=T("マキノ11:47発を逃すと船に乗れない", "Miss the 11:47 and you miss the boat"),
                 rows=[row("train", "マキノ11:47発→近江今津11:58着・200円。船をやめる場合はマキノ12:51発→長浜13:27着・680円", "Makino 11:47 → Omi-Imazu 11:58, ¥200. Without the boat: Makino 12:51 → Nagahama 13:27, ¥680")]),
            dict(id="chikubushima", when=("12:50〜15:45", "12:50–15:45"),
                 go=T("12:50までに今津港で手続きし、13:10発。島に13:35着、95分いて15:10発、長浜港15:45着。15:10の船に必ず乗ってください（2026年4月の時刻では、横断航路の最後の便です）。",
                      "Check in at Imazu port by 12:50 for the 13:10. Reach the island at 13:35, stay 95 minutes and leave at 15:10 for Nagahama port at 15:45. Don’t miss the 15:10: on April 2026 times it’s the crossing’s last boat."),
                 caution=T("予約を。入島料は現金。強風で欠航", "Book; cash island fee; wind may cancel")),
            dict(id="nagahamajo", when=("16:00〜17:15", "16:00–17:15"),
                 go=T("長浜港から歩いて15分で16:00着。先に天守へ（受付16:30まで）、そのあと公園の桜と湖岸を17:15ごろまで。月曜や船が遅れた日は公園だけにします。",
                      "15 minutes’ walk from the port, arriving 16:00. Do the keep first (last entry 16:30), then blossom and shore until about 17:15. On Mondays, or if the boat is late, just the park."),
                 caution=C_MONDAY, notices=[N_MONDAY]),
            dict(id="kurokabe", when=("17:30〜17:55", "17:30–17:55"),
                 go=T("ガラス館は閉まったあとなので、外観と北国街道の町並みだけ。ガラス館に入りたければ、長浜港から先にこちらへ（16:10ごろ着）。天守は外れます。",
                      "The Glass House has closed, so it’s the façade and old street only. To go inside, come here first from the port (about 16:10) and skip the keep."),
                 caution=T("ガラス館は閉館後。町並みだけ", "Glass House closed by then; streets only")),
            dict(id="nagahamaeki", when=("18:00〜19:57", "18:00–19:57"),
                 go=T("晩ごはんは駅から4分の長濱浪漫ビールで18:00〜19:40。19:57発で京都21:12着（土日祝21:07着）。乗り遅れたら20:36発→21:48着、21:17発→22:28着。",
                      "Dinner 18:00–19:40 at Nagahama Roman Beer, 4 minutes from the station. The 19:57 reaches Kyoto at 21:12 (21:07 on weekends and holidays). If you miss it: 20:36 → 21:48, 21:17 → 22:28."),
                 caution=C_ROMAN,
                 notices=[N_ROMAN], rows=[ROW_DINNER, ROW_RAMEN], links=[L_ROMAN, L_RAMEN], gmaps=[GM_ROMAN, GM_RAMEN]),
        ],
        hints=[("osakiji", {"any": ["kaizu", "sakura", "osakiji"], "none": ["chikubushima"]},
                T("竹生島をやめる日は「朝の桜と午後の長浜」のコースに切り替えると、時間割が合います。",
                  "Skipping the island? Switch to the morning-blossom and Nagahama course for times that fit.")),
               ("chikubushima", {"any": ["chikubushima"], "none": ["kaizu", "sakura", "osakiji"]},
                T("海津大崎に寄らない日は、京都10:45発の新快速で近江今津11:34着（990円）。13:10の船に間に合います。",
                  "Skipping Kaizu-Osaki: the 10:45 Special Rapid from Kyoto reaches Omi-Imazu at 11:34 (¥990), in time for the 13:10 boat."))]),
}

# ---------------------------------------------------------------------------
# 出典（確かめたページと、そこで見た数字）
# ---------------------------------------------------------------------------
SRC = [
    ("JR 京都→マキノ（平日 11-25）：9:48→10:50・1,170円", yahoo("京都", "マキノ", 25, "09:30")),
    ("JR 京都→マキノ（土 11-28。日 11-29も同じ）：9:45→10:50・1,170円", yahoo("京都", "マキノ", 28, "09:30")),
    ("JR 京都→マキノ（10:40以降。平日・土日とも）：10:45→11:50、11:45→12:50", yahoo("京都", "マキノ", 28, "10:40")),
    ("JR 京都→マキノ（平日）：7:00→近江今津7:59着・8:04発→8:12、次8:19→9:30", yahoo("京都", "マキノ", 25, "06:55")),
    ("JR 京都→マキノ（土。日も同じ）：7:00→8:12、次8:15→9:30", yahoo("京都", "マキノ", 28, "06:55")),
    ("三条京阪→マキノ（平日）：9:37→山科9:46着・9:54発→10:50、1,430円", yahoo("三条京阪", "マキノ", 25, "09:15")),
    ("三条京阪→マキノ（土。日も同じ）：9:28→山科9:38着・9:51発→10:50、1,430円", yahoo("三条京阪", "マキノ", 28, "09:15")),
    ("三条京阪→マキノ（早朝。平日・土日とも）：6:39→山科6:48着・7:05発→8:12、1,430円", yahoo("三条京阪", "マキノ", 25, "06:30")),
    ("JR マキノ→長浜（平日・土日とも）：11:51→近江塩津12:01着・12:06発→12:27、次12:51→13:27、680円", yahoo("マキノ", "長浜", 25, "11:40")),
    ("JR マキノ→長浜（平日・土日とも）：15:51→近江塩津16:01着・16:06発→16:27、次16:51→17:27、17:50→18:27", yahoo("マキノ", "長浜", 25, "15:20")),
    ("JR 永原→長浜（平日・土日とも）：15:56→近江塩津16:01着・16:06発→16:27、次16:56→17:27、510円", yahoo("永原", "長浜", 25, "15:30")),
    ("JR マキノ→近江今津（平日・土日とも）：11:47→11:58、次12:47→12:58、200円", yahoo("マキノ", "近江今津", 25, "11:40")),
    ("JR 近江今津→長浜（平日・土日とも）：13:43→14:27、770円", yahoo("近江今津", "長浜", 25, "13:15")),
    ("JR 京都→近江今津（平日・土日とも）：10:45→11:34、990円", yahoo("京都", "近江今津", 25, "10:40")),
    ("JR 京都→長浜（平日・土日とも）：10:00→11:10、1,340円", yahoo("京都", "長浜", 25, "09:40")),
    ("JR マキノ→京都（平日・土日とも）：15:47→16:57、16:47→17:57、1,170円", yahoo("マキノ", "京都", 25, "15:30")),
    ("JR 永原→京都（平日・土日とも）：16:42→17:57、1,340円", yahoo("永原", "京都", 25, "15:00")),
    ("JR 長浜→京都：17:57→19:12、18:28→19:42、18:57→20:12（平日・土日とも）、1,340円", yahoo("長浜", "京都", 25, "17:50")),
    ("JR 長浜→京都（平日）：19:28→20:42、19:57→21:12、20:36→米原20:45着・20:54発→21:48", yahoo("長浜", "京都", 25, "19:20")),
    ("JR 長浜→京都（土。日も同じ）：19:28→20:47、19:57→21:07、20:36→21:48", yahoo("長浜", "京都", 28, "19:20")),
    ("最終 長浜→京都（平日・土日とも）：22:15→米原22:25着・22:42発→23:50。乗り換えなしは21:17→22:28", yahoo("長浜", "京都", 25, "12:00", 2)),
    ("最終 長浜→三条京阪（平日・土日とも）：21:17→山科22:22着・22:41発→22:50、1,430円", yahoo("長浜", "三条京阪", 25, "12:00", 2)),
    ("最終 マキノ→京都（平日・土日とも）：22:10→23:19", yahoo("マキノ", "京都", 25, "12:00", 2)),
    ("最終 永原→京都（平日・土日とも）：22:04→23:19", yahoo("永原", "京都", 25, "12:00", 2)),
    ("湖西線：風速が基準に達すると運転見合わせ", WIND),
    ("海津大崎：約4km・約800本、満開 2024-04-08・2025-04-12、京都市内より1週間ほど遅い", SAKURA),
    ("交通規制（2026年の予定）：4月4日・5日 9:30〜17:00、東行きの一方通行。集落内は自転車を押す", REG),
    ("トイレは駅前に公共トイレ。ライトアップは協会・行政では予定なし。トンネル4つ", FAQ),
    ("2026年春の地図：駅→並木口 約2km30分、並木口→大崎寺 約2km30分、仮設トイレ、湖岸遊歩道約2km、臨時売店・シャトルバスなし", MAP26),
    ("バス平日（2026年春）：海津大崎口★10:31・11:31・12:31・14:31・15:31・16:31・17:31→駅まで8分、220円", BUS_WD),
    ("バス土休日（2026年春）：海津大崎口★10:31・11:31・12:31・14:31・15:31・17:31→駅まで8分、220円", BUS_WE),
    ("規制日のバス（2026年4月4日・5日）：国境線は海津1区に止まらず海津大崎口に停車", BUS_REG),
    ("レンタサイクル：9:00〜17:00・1,000円、2026-11-14〜2027-05-09 予約不可、高島市内だけ、身分証", CYCLE),
    ("大崎寺：第一トンネルの手前の石段の上、阿弥陀堂の血天井", OSAKIJI),
    ("海津の石積み：約1.2km、重要文化的景観", ISHIZUMI),
    ("桜クルーズ（2026年春の実績）：4月15日で終了、4,500円、予約優先", CRUISE),
    ("竹生島びわ湖横断：13:10→島13:35着・15:10発→長浜港15:45、3,600円。5便目は4月25日から", BOAT),
    ("入島料600円・小人300円は現金。ネット予約は前日15:00まで。島に休憩所と土産物屋2軒", BOAT_FAQ),
    ("竹生島：石段165段", BOAT_FLOW),
    ("今津港：駅から徒歩5分、売店なし、トイレあり", IMAZU),
    ("宝厳寺：9:30〜16:30（船の時刻に基づく）", HOGONJI),
    ("永原駅：係員7:30〜16:30、10:40〜12:00不在、ICOCA可、コインロッカー", STATIONS),
    ("長浜城：9:00〜17:00、受付16:30、月曜休み、500円・200円、展示品は撮影禁止", CASTLE),
    ("豊公園：約600本、24時間、無料", PARK),
    ("豊公園の桜（2026年春の実績）：4月3日満開、4月13日でぼんぼり終了", PARK_2026),
    ("慶雲館：9:30〜17:00、入館16:30、300円・150円", KEIUN),
    ("慶雲館の休館：2026-12-01〜2027-01-09、3月11日〜下旬", KEIUN_OFF),
    ("長浜盆梅展：9:00〜17:00、入館16:30、大人1,000円", BONBAI),
    ("長浜鉄道スクエア：9:30〜17:00、入館16:30、500円・200円、12/29〜1/3休み", TETSU),
    ("黒壁ガラス館：10:00〜17:00（3月31日は16:00まで）、定休日なし", GLASS),
    ("長濱浪漫ビール：平日11:30〜15:00（LO14:30）・17:00〜21:00（LO20:15）、土日祝11:30〜21:00、予約は前日まで", ROMAN),
    ("長濱浪漫ビール：火曜定休（2026年3月27日のお知らせ）", ROMAN_CLOSED),
    ("京都拉麺小路：11:00〜22:00（LO21:30）", RAMEN),
]
SRC += [
    ("祝日（11-23）の主な便：京都9:45→マキノ10:50", yahoo("京都", "マキノ", 23, "09:30")),
    ("祝日（11-23）の主な便：長浜19:28→京都20:47、19:57→21:07、20:36→21:48", yahoo("長浜", "京都", 23, "19:20")),
]
SOURCES = [{"what": w, "url": u, "checked": CHECKED} for w, u in SRC]

AUTO_IDS = ("makino", "nagahamaeki")     # 選んで回るとき、自動で入る駅
EAST = ("kaizu", "sakura", "osakiji", "oura")
WEST = ("chikubushima", "kurokabe", "tetsudo", "keiunkan", "nagahamajo")


def build(cid, c):
    spots = []
    for no, item in enumerate(c["spots"], 1):
        pid = item["id"]
        b = copy.deepcopy(BASE[pid])
        text = {}
        for i, lang in enumerate(("ja", "en")):
            time_head = "おすすめ訪問時間：" if lang == "ja" else "Recommended visit time: "
            text[lang] = "\n\n".join([b["head"][lang], item["go"][lang], b["body"][lang], time_head + item["when"][i]])
        s = {"no": no, "id": pid, "name": b["name"], "kind": b["kind"], "blurb": b["blurb"],
             "lat": b["lat"], "lng": b["lng"], "text": text,
             "gmaps": b["gmaps"] + item.get("gmaps", []),
             "links": b["links"] + item.get("links", [])}
        s["info"] = {"rows": item.get("rows", []) + b["rows"], "cash": b.get("cash", False), "tip": b["tip"], "checked": CHECKED}
        if item.get("caution"):
            s["caution"] = item["caution"]
        s["photos"] = photos(pid, EXTRA.get(pid, ()))
        s["notices"] = item.get("notices", []) + b["notices"]
        spots.append(s)
    no_of = {s["id"]: s["no"] for s in spots}
    nums = lambda ids: [no_of[i] for i in ids if i in no_of]
    picks = [s["no"] for s in spots if s["id"] not in AUTO_IDS]
    hints = [{"spot": no_of[spot], "rule": {k: nums(v) for k, v in rule.items()}, "text": text, "from": None, "to": None}
             for spot, rule, text in c["hints"]]
    sections, first = [], 1
    for last, (area, title) in c["secs"]:
        sections.append({"first": first, "last": last, "area": area, "title": title})
        first = last + 1
    assert first == len(spots) + 1, cid
    return {
        "id": "kohoku", "course": cid,
        "_note": "京都から日帰り 海津大崎の桜と長浜（kohoku/ のページ専用。形は eizan-line.json と同じ）。このファイルは scripts/build_kohoku_data.py が作るので、直接直さない。"
                 "起点は京都駅（JR 湖西線）。春の日程は2026年春の実績、電車は2026年11月のダイヤ。"
                 "写真は Toshi の写真ライブラリから（海津大崎は2025年4月12日と2026年4月3日、長浜は2025年1月13〜14日）。竹生島はオーナーが行っていない場所で、写真は Wikimedia Commons。",
        "sections": sections,
        "plan": {"_note": "「選んで回る」の設定。時期と体力でコースを分けたので、最初は「全部回る」。駅は選んだ場所に合わせて自動で入る。",
                 "picks": picks, "defaultPicks": picks,
                 "auto": {str(no_of["makino"]): {"any": nums(EAST)}, str(no_of["nagahamaeki"]): {"any": nums(WEST)}},
                 "hints": hints},
        "photoBase": "../images/kohoku/",
        "sources": SOURCES,
        "spots": spots,
    }


for cid, c in COURSES.items():
    data = build(cid, c)
    out = f"{R}/data/routes/{c['file']}"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", c["file"], [(s["no"], s["id"], len(s["photos"])) for s in data["spots"]])
