#!/usr/bin/env python3
"""京都 大原のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_ohara_data.py  （そのあと python3 scripts/sync_ohara.py）
- 作るもの（COURSES）:
  - data/routes/ohara.json … 「9〜10時に出発」（三条京阪前9:07発→大原9:48着。先に寂光院→早めのお昼→参道→宝泉院→実光院→
    団体が帰りはじめる14時すぎの三千院→16:27のバスで三条へ→街なかで晩ごはん）
  - data/routes/ohara-early.json … 「三千院の開門に合わせる」（三条京阪前7:57発→大原8:38着（土日祝は8:49着）。参道→三千院9:00→宝泉院のお抹茶→
    11時半にお昼→里の道→寂光院→14:27のバスで戻る）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方の一言、「選んで回る」の設定
- 出発地は京都の中心・三条のあたり（京都バスの「三条京阪前」。四条河原町・出町柳駅前からも同じバスに乗れる）
- 写真は images/ohara/ にある（足していない）。大原バス停の3枚のうち、夜のバスの1枚（bus-3.jpg）を9番「帰りのバスと、街なかの夜」に移した
  - オーナーの写真は 2024年11月18日（雨の日の夕方、iPhone と Nikon D7000）と 2016年9月27日（三千院の聚碧園の1枚）。
    宝泉院・実光院・来迎院と音無の滝・里の道・寂光院はオーナーの写真がない場所なので、文章にも行った日などは書かない
- 2026-11-22 オーナーの基準で作り直した（ゲストが実際に回れる1日。開門コースと9〜10時発コース、お昼の場所と時間、帰りのバス、街なかの夜）。
  バスの時刻と運賃は京都バスの公式サイトの時刻表（2026年9月28日改正と、11月21日〜12月6日の秋のダイヤ）、
  地下鉄・京阪は乗換案内（Yahoo!路線情報）、拝観の時間と料金は各寺の公式サイト
"""
import copy, json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "ohara"
IMG = f"{R}/images/{MAP_ID}"
D21, D22, D24 = "2026-11-21", "2026-11-22", "2026-11-24"   # 確認日（21日に確認して22日は見直していないものは D21。24日は「要確認」の調べ直し）


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def info(rows, source, tip=None, verified=True, cash=False, checked=D22):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked, "source": source}
    if not verified:
        d["verified"] = False
    return d


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


def own(pid, n):
    return [f"{pid}-{i}.jpg" for i in range(1, n + 1)]


PHOTOS = {
    "bus": ["bus-1.jpg", "bus-2.jpg"],
    "kaeri": ["bus-3.jpg"],
    "sando": own("sando", 6),
    "sanzenin": own("sanzenin", 9) + [cc("sanzenin-10.jpg", "Arvined Winstud", "CC BY-SA 3.0", "三千院のお地蔵様 (258188583).jpeg")],
    "hosenin": [cc("hosenin-1.jpg", "Maechan0360", "CC BY-SA 3.0", "宝泉院 01.JPG"),
                cc("hosenin-2.jpg", "Maechan0360", "CC BY-SA 3.0", "宝泉院 02.JPG"),
                cc("hosenin-3.jpg", "Asturio Cantabrio", "CC BY-SA 4.0", "Hosenin (Kyoto) ac (4).jpg"),
                cc("hosenin-4.jpg", "Asturio Cantabrio", "CC BY-SA 4.0", "Hosenin (Kyoto) ac (2).jpg"),
                "shorinin-1.jpg"],
    "jikkoin": [cc("jikkoin-1.jpg", "Maechan0360", "CC BY-SA 3.0", "実光院 01.JPG"),
                cc("jikkoin-2.jpg", "Maechan0360", "CC BY-SA 3.0", "実光院 03.JPG"),
                cc("jikkoin-3.jpg", "Susumu331", "CC BY-SA 4.0", "実光院001.jpg")],
    "otonashi": [cc("otonashi-1.jpg", "Nankou Oronain", "CC BY-SA 3.0", "京都・大原にて 来迎院 Raigō-in 2011.8.28 - panoramio.jpg"),
                 cc("otonashi-2.jpg", "米田賢一", "CC BY 3.0", "音無の滝 - panoramio.jpg")],
    "sato": [cc("sato-1.jpg", "kajikawa", "CC BY 3.0", "大原 - panoramio - kajikawa.jpg"),
             cc("sato-2.jpg", "KimonBerlin", "CC BY-SA 2.0", "Ohara 2008-11-26 (3261975204).jpg")],
    "jakkoin": [cc("jakkoin-1.jpg", "PlusMinus", "CC BY-SA 3.0", "JyakkouinHondo.jpg"),
                cc("jakkoin-2.jpg", "Suikotei", "CC BY-SA 4.0", "Jakkoin (Ohara).jpg"),
                cc("jakkoin-3.jpg", "Suikotei", "CC BY-SA 4.0", "Jakkoin Hondo 2019.jpg"),
                cc("jakkoin-4.jpg", "くろふね", "CC BY 3.0", "寂光院 - panoramio (4).jpg"),
                cc("jakkoin-5.jpg", "Suikotei", "CC BY-SA 4.0", "Jakkoin Kenreimonin Goanshitsu Ato.jpg")],
}

KBUS = link("timetable", "京都バス 時刻表（バス停の名前で検索）", "Kyoto Bus timetables (search by stop name, Japanese)", "https://www.kyotobus.jp/route/timetable/")
KBUS_OHARA = link("timetable", "京都バス「大原」発の時刻表", "Kyoto Bus: departures from Ohara (Japanese)", "https://www.kyotobus.jp/route/timetable/stop.html?stop_id=6039_1")
KBUS_SANJO = link("timetable", "京都バス「三条京阪前」発の時刻表", "Kyoto Bus: departures from Sanjo-Keihan-mae (Japanese)", "https://www.kyotobus.jp/route/timetable/stop.html?stop_id=114_1")
PASS = link("info", "地下鉄・バス1日券（京都バス）", "Subway & Bus 1-day Pass (Kyoto Bus, Japanese)", "https://www.kyotobus.jp/route/fare/discount/pass/post-3.html")
HOSHO = link("info", "京都大原観光保勝会", "Kyoto Ohara tourist association (Japanese)", "https://kyoto-ohara-kankouhosyoukai.net/")
MOMIJI = "https://ja.kyoto.travel/flower/momiji/"
SEASON = notice("紅葉は例年11月中旬〜下旬。写真は秋の雨の日", "Autumn leaves: usually mid to late November. The photos are from a rainy autumn day",
                "大原は京都の町なかより気温が低く、紅葉は例年11月中旬〜下旬です（年によって前後します）。三千院のあじさいは6月中旬〜7月はじめ。冬は雪が積もる日があります。私の写真は2024年11月18日、雨の夕方に撮ったものです。晴れた日や、ほかの季節は見え方が違います。",
                "Ohara is cooler than central Kyoto; the leaves usually peak from mid to late November (it shifts from year to year). Sanzen-in’s hydrangeas bloom from mid June into early July, and in winter there are days of snow. My photos were taken on a rainy late afternoon, 18 November 2024, so expect a different look in sunshine or in other seasons.",
                url=MOMIJI)
AUTUMN_BUS = notice("紅葉の土日祝は、バスも道も混みます", "On autumn weekends the buses and the road are busy",
                    "三条京阪前は途中のバス停なので、座れないことがあります（大原まで40〜50分）。立つのがつらい人は、地下鉄で国際会館駅へ行き（烏丸御池から14分・290円）、駅前から大原行きに乗ると、バスは約22分・400円で済みます。11月29日までの土日祝は、国際会館駅前〜大原の臨時の特急バスも出ています。帰りは大原が始発なので、並べば座れます。",
                    "Sanjo-Keihan-mae is a stop along the way, so you may have to stand (40–50 minutes to Ohara). If that’s hard, take the subway to Kokusaikaikan (14 minutes from Karasuma Oike, ¥290) and catch an Ohara bus outside the station: only about 22 minutes on the bus, ¥400. On Saturdays, Sundays and holidays until 29 November extra express buses also run between Kokusaikaikan and Ohara. Going back, Ohara is the first stop, so queue and you get a seat.",
                    frm="2026-11-01", to="2026-12-06")

# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    bus=dict(
        name=T("大原バス停", "Ohara bus stop"), kind=T("バス停（スタート）", "Bus stop (start)"),
        blurb=T("三条京阪前から京都バス17系統で40〜50分・570円。乗り換えなしで着きます。三千院へは東へ、寂光院へは西へ歩きます。",
                "40–50 minutes on Kyoto Bus 17 from Sanjo-Keihan-mae, ¥570, no change. Sanzen-in is to the east, Jakko-in to the west."),
        caution=T("1日券はバスの中では買えません。ICカードは乗るときと降りるときにタッチ", "The 1-day pass isn’t sold on the bus. With an IC card, tap on and tap off"),
        lat=35.11975, lng=135.82898,
        body=T("大原（おおはら）バス停\n\n大原へ行く乗り物はバスだけです。京都の中心からは、京都バスの17系統「大原」行きが乗り換えなしで便利です。京都駅前を出て、四条河原町、三条京阪前、出町柳駅前の順に止まります。\n\n"
               "・三条京阪前から：40〜50分・570円。のりばは、三条大橋の東のたもとから川端通を北へ少し歩いた、川側の歩道です（下の「Googleマップで開く」で場所を確かめられます）。市バスののりばとは別の場所なので、「京都バス 17 大原」の表示を探してください。\n"
               "・四条河原町から：三条京阪前の8分前に出ます。590円。\n"
               "・出町柳駅前から：三条京阪前の9分後。490円。\n"
               "・京都駅前（C3のりば）から：約1時間・630円。始発なので、早めに並べば座れます。\n\n"
               "もう1つの行き方は、地下鉄烏丸線で国際会館駅へ行き（烏丸御池から14分・290円）、駅前から京都バス19系統などに乗る方法です。バスは約22分・400円。道が混む秋の週末は、こちらのほうが時間が読めます。\n\n"
               "どれも「地下鉄・バス1日券」（1,100円）で乗れます。三条京阪前から往復すると1,140円なので、1日券のほうが少し安く、夜に地下鉄や市バスにも乗れます。1日券は京都バスの車内では買えません。地下鉄の駅の券売機で先に買ってください。\n\n"
               "バスは後ろのドアから乗って、前から降ります。ICカード（ICOCA・Suicaなど）は、乗るときと降りるときの2回タッチ。現金は降りるときに運賃箱へ。\n\n"
               "大原バス停（京都バスの大原バスターミナル）の中に、京都市の公衆トイレがあります。開いているのはバスが走る時間に合わせて6:30ごろ〜21:30ごろ。多機能トイレもあります。\n\n"
               "大原は町なかより寒く、拝観料は現金の所がほとんどです。上着を1枚多く、千円札と小銭を多めに。",
               "Ohara bus stop\n\nBuses are the only way to Ohara. From central Kyoto the simplest is Kyoto Bus 17, bound for Ohara, with no change. It starts at Kyoto Station and stops at Shijo-Kawaramachi, Sanjo-Keihan-mae and Demachiyanagi-ekimae, in that order.\n\n"
               "• From Sanjo-Keihan-mae: 40–50 minutes, ¥570. The stop is a short walk north along Kawabata-dori from the east end of Sanjo Ohashi bridge, on the river side of the road (check the spot with the Google Maps button below). It is not at the city-bus stops: look for the sign “Kyoto Bus 17 Ohara”.\n"
               "• From Shijo-Kawaramachi: leaves 8 minutes before Sanjo-Keihan-mae. ¥590.\n"
               "• From Demachiyanagi-ekimae: 9 minutes after Sanjo-Keihan-mae. ¥490.\n"
               "• From Kyoto Station (stop C3): about 1 hour, ¥630. It’s the first stop, so queue early and you get a seat.\n\n"
               "The other way is the Karasuma subway line to Kokusaikaikan (14 minutes from Karasuma Oike, ¥290), then Kyoto Bus 19 and others from outside the station: about 22 minutes, ¥400. On autumn weekends, when the road jams, this way keeps better time.\n\n"
               "All of these are covered by the Subway & Bus 1-day Pass (¥1,100). A return from Sanjo-Keihan-mae is ¥1,140, so the pass is slightly cheaper and also covers the subway and city buses in the evening. It isn’t sold on Kyoto Bus: buy it first from a ticket machine at a subway station.\n\n"
               "Board at the rear door and get off at the front. With an IC card (ICOCA, Suica and so on), tap when you board and again when you get off. With cash, pay into the fare box as you leave.\n\n"
               "There are public toilets run by the city inside the Ohara bus terminal, open from about 6:30 to about 21:30 to match the bus service, including an accessible toilet.\n\n"
               "Ohara is colder than the city, and most temples take cash. Bring an extra layer, ¥1,000 notes and coins."),
        gmaps=[gm("大原バス停", "Ohara bus stop", 35.11975, 135.82898, "大原バス停 京都バス 左京区"),
               gm("三条京阪前（京都バスのりば）", "Sanjo-Keihan-mae (Kyoto Bus stop)", 35.009724, 135.772129, "三条京阪前 バス停 京都バス")],
        links=[KBUS_SANJO, KBUS, PASS],
        notices=[AUTUMN_BUS, SEASON],
        _rows=[row("fee", "大原まで：三条京阪前から570円、四条河原町から590円、出町柳駅前から490円、京都駅前から630円、国際会館駅前から400円",
                   "To Ohara: ¥570 from Sanjo-Keihan-mae, ¥590 from Shijo-Kawaramachi, ¥490 from Demachiyanagi-ekimae, ¥630 from Kyoto Station, ¥400 from Kokusaikaikan-ekimae"),
               row("fee", "地下鉄・バス1日券 1,100円（大原バス停まで使えます。その先の小出石方面は別料金）",
                   "Subway & Bus 1-day Pass ¥1,100 (valid as far as the Ohara stop; beyond it, towards Kodeishi, costs extra)"),
               row("hours", "トイレ：大原バス停（大原バスターミナル）の中の京都市の公衆トイレ。6:30ごろ〜21:30ごろ（バスの運行時間に合わせて）",
                   "Toilets: city public toilets inside the Ohara bus terminal, about 6:30–21:30 (matching the bus service)")],
        _tip=T("バスの時刻と運賃は、京都バスの公式サイトの時刻表で確認しました（2026年9月28日改正のダイヤと、11月21日〜12月6日の秋のダイヤ）。秋のあいだは日によって時刻が少し変わり、道が混むと遅れます。乗る前に公式の時刻表を見てください。地下鉄の時間と運賃は乗換案内、1日券の範囲は京都バスの公式サイトの区間図（21日に確認）です。",
               "Bus times and fares were checked on Kyoto Bus’s official timetable (the timetable revised on 28 September 2026 and the autumn timetable for 21 November–6 December). In autumn the times vary a little from day to day, and buses run late when the road is busy: check the official timetable before you go. Subway times and fares are from a route planner; the pass area is from Kyoto Bus’s official area map (checked on the 21st)."),
        _source="京都バス公式サイトの時刻表・運賃（2026-11-22）、乗換案内（Yahoo!路線情報）2026-11-22、1日券は京都バス公式サイト（2026-11-21）、"
                "トイレは京都市「(R1)大原の里公衆トイレ」https://www.city.kyoto.lg.jp/kankyo/page/0000331165.html（2026-11-24）"),
    sando=dict(
        name=T("三千院の参道（呂川沿い）", "The lane to Sanzen-in"), kind=T("参道", "Approach"),
        blurb=T("バス停から三千院まで、小さな川に沿って上る道。ゆっくり歩いて15分。しば漬の店や茶屋が並びます。",
                "A lane up beside a small stream from the bus stop to Sanzen-in, 15 minutes at an easy pace, lined with pickle shops and teahouses."),
        lat=35.11995, lng=135.83150,
        body=T("三千院の参道（さんどう）\n\nバス停から国道の信号を渡って、呂川（ろせん）という小さな川に沿った道を上ります。三千院の案内では歩いて約10分。ゆるい上り坂なので、15分みておくと楽です。\n\n"
               "道の両側に、しば漬の店、茶屋、みやげ物の店が並びます。しば漬は大原で生まれた漬物で、赤しそで漬けたなすやきゅうりです。老舗の「志ば久（しばきゅう）」は参道の途中にあります（9:00〜16:00、水曜休み）。\n\n"
               "店が開くのは9〜10時ごろから、閉まるのは16時ごろが多い土地です（店ごとに違います）。漬物は重いので、買うのは帰り道に。ただし16時を過ぎると買えない店があります。\n\n"
               "坂を上りきると石段があり、その上が三千院の前の道です（写真は2024年11月18日。石段のまわりのもみじが真っ赤でした）。雨の日は石畳がすべるので、歩きやすい靴で。",
               "The lane to Sanzen-in\n\nFrom the bus stop, cross the main road at the lights and follow the lane up beside a small stream, the Rosen. The temple gives it as about 10 minutes; it’s a gentle climb, so allow 15.\n\n"
               "Both sides are lined with pickle shops, teahouses and souvenir stalls. Shibazuke, aubergine and cucumber pickled with red shiso, was born in Ohara. The long-established Shibakyu is partway up the lane (9:00–16:00, closed Wednesdays).\n\n"
               "Here shops tend to open at around 9–10 and close at around 16:00 (each keeps its own hours). Pickles are heavy, so buy them on the way down, but note that after 16:00 some shops are shut.\n\n"
               "At the top of the slope a flight of stone steps brings you out in front of Sanzen-in (my photos are from 18 November 2024, when the maples round the steps were deep red). The paving is slippery in rain: wear shoes with grip."),
        gmaps=[gm("三千院の参道", "Lane to Sanzen-in", 35.11995, 135.83150, "志ば久 大原 京都")],
        links=[link("official", "志ば久 公式サイト", "Shibakyu (official, Japanese)", "https://www.shibakyu.jp/"), HOSHO],
        info=info([row("hours", "大原バス停から三千院まで歩いて約10分（三千院の案内）。このマップでは15分でみています", "About 10 min on foot from the Ohara bus stop to Sanzen-in (temple’s access page). This map allows 15"),
                   row("hours", "志ば久（しば漬）9:00〜16:00", "Shibakyu (shibazuke pickles) 9:00–16:00"),
                   row("closed", "志ば久は水曜休み", "Shibakyu is closed on Wednesdays")],
                  "三千院 公式サイト（アクセス）、志ば久 公式サイト。2026-11-21に確認", checked=D21,
                  tip=T("志ば久の時間と休みは公式サイトで確認しました（11月21日）。ほかの店の営業日と時間は店ごとに違います。", "Shibakyu’s hours and closing day were checked on its website (21 November). Other shops keep their own days and hours."))),
    sanzenin=dict(
        name=T("三千院", "Sanzen-in"), kind=T("寺", "Temple"),
        blurb=T("杉木立の下に苔が広がる庭と、国宝の阿弥陀三尊。大原でいちばん人が集まる場所なので、開門すぐか14時すぎに。",
                "A moss garden under tall cedars and a National Treasure Amida triad. It draws the biggest crowds in Ohara, so come right at opening or after 14:00."),
        caution=T("11月は8:45〜16:45、12〜2月は16:30まで。拝観料は現金を用意", "Nov 8:45–16:45; closes 16:30 Dec–Feb. Bring cash for the fee"),
        lat=35.11966, lng=135.83410,
        body=T("三千院（さんぜんいん）\n\n最澄が比叡山に建てたお堂に始まり、皇族が住職をつとめてきた門跡寺院です。明治のはじめに大原へ移りました。石垣の上の御殿門（ごてんもん）から入ります。\n\n"
               "大原へ来る人のほとんどがここへ来ます。団体が多いのは10時ごろから昼すぎまで。開門すぐか、14時を過ぎてからのほうが、縁側に座る場所を見つけやすいです（日によります）。\n\n"
               "順路は、客殿 → 宸殿 → 庭へ下りる、の順です。\n\n"
               "・聚碧園（しゅうへきえん）：客殿の縁側から座って眺める池の庭。赤い毛氈に座れます。\n"
               "・有清園（ゆうせいえん）：宸殿を出ると、杉とひのきの木立の下に苔が広がります。秋はもみじの赤と苔の緑が重なります（写真1枚目）。\n"
               "・往生極楽院（おうじょうごくらくいん）：苔の庭の奥の小さなお堂。国宝の阿弥陀三尊像がいます。両脇の菩薩が少し前かがみに座る「大和坐り」を、近くで見てください。\n"
               "・わらべ地蔵：往生極楽院の南、弁天池のそばの苔の中に、小さなお地蔵さまがいます。見落としやすいので、足もとを探してください（写真10枚目）。\n\n"
               "その先に、あじさい苑、金色不動堂、観音堂と続きます。奥まで歩いて1時間ほど。靴を脱いで上がるので、脱ぎやすい靴と、冬は厚い靴下を。\n\n"
               "苔がいちばんきれいなのは雨の日と雨上がりです。私が行った2024年11月18日は雨で、夕方は人も少なく、苔ももみじも色が濃く見えました。写真9枚目は2016年9月の聚碧園で、夏から秋のはじめは緑一色です。\n\n"
               "あじさいは6月中旬から7月はじめ。冬は雪の日があります。",
               "Sanzen-in\n\nThe temple began as a hall built by Saicho on Mt. Hiei and was headed for centuries by members of the imperial family; it moved to Ohara in the early Meiji period. You enter through the Goten-mon gate, set in a high stone wall.\n\n"
               "Almost everyone who comes to Ohara comes here. Tour groups are thickest from about 10:00 until early afternoon. Right at opening, or after 14:00, it is easier to find a place to sit on the veranda (it varies by day).\n\n"
               "The route runs: guest hall → Shinden hall → down into the garden.\n\n"
               "• Shuheki-en: a pond garden viewed sitting on the veranda of the guest hall, on the red felt.\n"
               "• Yusei-en: step out of the Shinden and moss spreads under tall cedars and cypresses. In autumn, red maples sit over the green (photo 1).\n"
               "• Ojo Gokuraku-in: a small hall at the back of the moss garden, housing the Amida triad, a National Treasure. Look closely at the two attendant bodhisattvas, kneeling and leaning slightly forward.\n"
               "• Warabe Jizo: small stone Jizo figures half-buried in the moss beside the Benten pond, south of the hall. They are easy to miss, so look down (photo 10).\n\n"
               "Beyond are the hydrangea garden, the Konjiki Fudo hall and the Kannon hall. Allow about an hour to walk to the far end. You take your shoes off to go in, so wear ones that slip off easily, and thick socks in winter.\n\n"
               "The moss is at its best in rain or just after. I went on a rainy 18 November 2024; late in the afternoon it was quiet, and the moss and maples looked their deepest. Photo 9 is Shuheki-en in September 2016: from summer to early autumn it is all green.\n\n"
               "Hydrangeas bloom from mid June into early July. In winter there are snowy days."),
        gmaps=[gm("三千院", "Sanzen-in", 35.11966, 135.83410, "三千院 大原 京都")],
        links=[link("official", "三千院 公式サイト", "Sanzen-in (official)", "https://www.sanzenin.or.jp/", "https://www.sanzenin.or.jp/en"),
               link("info", "紅葉だより（京都観光Navi）", "Autumn-leaf report (Kyoto City, Japanese)", MOMIJI)],
        info=info([row("hours", "3〜10月 9:00〜17:00／11月 8:45〜16:45／12〜2月 9:00〜16:30", "Mar–Oct 9:00–17:00 / Nov 8:45–16:45 / Dec–Feb 9:00–16:30"),
                   row("closed", "休みなし", "Open every day"),
                   row("fee", "一般700円、中学生・高校生400円、小学生150円", "¥700; junior high and high school ¥400; elementary ¥150")],
                  "三千院 公式サイト（拝観時間は2026-11-22、料金は2026-11-21に確認）", cash=True,
                  tip=T("時間は11月22日、料金は21日に三千院の公式サイトで確認しました。あじさいの時期も公式サイトの案内です。混む時間は目安で、日によって違います。",
                        "Hours checked on the temple’s website on 22 November, fees on the 21st; the hydrangea season is from the same site. Busy times are a guide and vary by day."))),
    hosenin=dict(
        name=T("宝泉院と勝林院", "Hosen-in & Shorin-in"), kind=T("寺（額縁庭園）", "Temple (framed garden)"),
        blurb=T("柱と柱のあいだを額縁にして、竹林と樹齢700年の五葉松を眺める部屋。お抹茶とお菓子がついていて、座って休めます。",
                "A room where the pillars frame a bamboo grove and a 700-year-old pine like pictures. Matcha and a sweet are included, so it doubles as a rest."),
        caution=T("行事で休む日があります（公式サイトのお知らせ）。受付は16:30まで", "Sometimes closed for temple events (see the website). Last entry 16:30"),
        lat=35.12135, lng=135.83400,
        body=T("宝泉院（ほうせんいん）と勝林院（しょうりんいん）\n\n三千院の門を出て左（北）へ歩いて約5分。道の突き当たりに勝林院の大きな本堂があり、その左手が宝泉院です。\n\n"
               "宝泉院は、客殿に座って庭を見るお寺です。柱と柱のあいだを額縁に見立てるので「額縁庭園」と呼ばれます。西側は竹林ごしに大原の里、南側は樹齢700年の五葉松（ごようのまつ）。拝観料にお抹茶とお菓子がついていて、座っていられる時間に決まりはありません。歩きつかれた足を休めるのにちょうどいい場所です。\n\n"
               "公式サイトのすすめは、畳に座って見ること。縁側まで出ずに、部屋の奥に座ると、柱と鴨居がちょうど額縁になります（写真1・2枚目）。\n\n"
               "廊下の天井は「血天井」です。関ヶ原の戦いの前に伏見城で自刃した鳥居元忠たちの床板を、供養のために天井に張ったものです。\n\n"
               "勝林院は1013年に開かれた、声明（しょうみょう＝お経に節をつけて唱える仏教音楽）の道場です。1186年に法然がここで念仏の教えを論じた「大原問答」で知られます。今の本堂は1778年の再建（写真5枚目は2024年11月18日の夕方、門の外から）。\n\n"
               "宝泉院の秋の夜の拝観（秋の夜灯り）は、2026年は開かれません（京都市観光協会の公式サイトの案内）。",
               "Hosen-in and Shorin-in\n\nTurn left (north) out of Sanzen-in’s gate and walk about five minutes. The big hall at the end of the lane is Shorin-in; Hosen-in is to its left.\n\n"
               "Hosen-in is a temple where you sit in the guest hall and look at the garden. The pillars work as picture frames, so it is known as the “framed garden”: to the west, the Ohara valley through a bamboo grove; to the south, a 700-year-old five-needle pine. Matcha and a sweet come with the entry fee, and you may sit as long as you like. It’s a good place to rest tired legs.\n\n"
               "The temple’s advice is to view it sitting on the tatami. Stay back from the veranda, deep in the room, and the pillars and lintel become the frame (photos 1 and 2).\n\n"
               "The corridor has a “blood ceiling”: floorboards from Fushimi Castle, where Torii Mototada and his men took their own lives before the battle of Sekigahara, set into the ceiling as a memorial.\n\n"
               "Shorin-in, founded in 1013, is a training hall for shomyo, Buddhist chant. It is known for the Ohara Debate of 1186, when Honen argued the case for the nenbutsu here. The present hall dates from 1778 (photo 5: from outside the gate, late on 18 November 2024).\n\n"
               "Hosen-in’s autumn evening opening (Aki no Yoakari) is not being held in 2026, according to the Kyoto City Tourism Association’s official site."),
        gmaps=[gm("宝泉院", "Hosen-in", 35.12135, 135.83400, "宝泉院 大原 京都"), gm("勝林院", "Shorin-in", 35.12122, 135.83454, "勝林院 大原 京都")],
        links=[link("official", "宝泉院 公式サイト", "Hosen-in (official, Japanese)", "http://www.hosenin.net/"),
               link("official", "勝林院 公式サイト", "Shorin-in (official, Japanese)", "https://www.shourinin.com/"),
               link("info", "勝林院（大原観光保勝会）", "Shorin-in (Ohara tourist association, Japanese)", "https://kyoto-ohara-kankouhosyoukai.net/detail/5522/")],
        notices=[notice("2026年は、秋の夜の拝観（夜灯り）はありません", "No autumn evening opening in 2026",
                        "例年11月上旬〜12月上旬の宝泉院の夜の拝観は、2026年は開催中止と京都市観光協会の公式サイトに出ています（11月24日確認）。昼の拝観（9:00〜17:00）はふだんどおりです。",
                        "Hosen-in’s evening opening, usually early November to early December, is cancelled for 2026 according to the Kyoto City Tourism Association’s official site (checked 24 November). Daytime visits (9:00–17:00) are as usual.",
                        url="https://ja.kyoto.travel/event/single.php?event_id=5013", frm="2026-11-01", to="2026-12-07")],
        info=info([row("hours", "宝泉院 9:00〜17:00（受付は16:30まで）", "Hosen-in 9:00–17:00 (last entry 16:30)"),
                   row("fee", "宝泉院 大人1,000円（お抹茶・お菓子つき。2026年4月10日から）、中学生・高校生900円、小学生800円", "Hosen-in ¥1,000 including matcha and a sweet (since 10 April 2026); junior high and high school ¥900; elementary ¥800"),
                   row("closed", "宝泉院は行事で休む日があります（公式サイトのお知らせ）", "Hosen-in sometimes closes for temple events (see the news on its website)"),
                   row("hours", "勝林院 9:00〜16:00（大原観光保勝会の案内）", "Shorin-in 9:00–16:00 (per the Ohara tourist association)"),
                   row("fee", "勝林院の拝観料は、公式サイトにも保勝会の案内にも書かれていません（要確認）", "Shorin-in’s entry fee isn’t given on its website or by the tourist association (please check)")],
                  "宝泉院 公式サイト（拝観について・お知らせ http://www.hosenin.net/haikan/ 2026-11-24）、"
                  "京都観光Navi「秋の夜灯り 大原宝泉院」https://ja.kyoto.travel/event/single.php?event_id=5013（2026年度は開催中止。2026-11-24）、"
                  "大原観光保勝会「勝林院」https://kyoto-ohara-kankouhosyoukai.net/detail/5522/（時間。2026-11-24）", cash=True, checked=D24,
                  tip=T("宝泉院の時間と料金は宝泉院の公式サイト、2026年の夜の拝観の中止は京都市観光協会の公式サイト、勝林院の時間は大原観光保勝会のサイトで確認しました（11月24日）。勝林院の拝観料はどこにも書かれていません。写真1〜4枚目は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Hosen-in’s hours and fees are from its website, the cancellation of the 2026 evening opening from the Kyoto City Tourism Association’s official site, and Shorin-in’s hours from the Ohara tourist association’s site (all checked 24 November). Shorin-in’s fee isn’t published anywhere we could find. Photos 1–4 are from Wikimedia Commons (author and license shown on each photo)."))),
    jikkoin=dict(
        name=T("実光院", "Jikko-in"), kind=T("寺（庭と山野草）", "Temple (garden)"),
        blurb=T("秋から春まで咲く「不断桜」のある小さなお寺。客殿から池の庭を眺め、庭へ下りて歩けます。受付は15:30まで。",
                "A small temple with a cherry that flowers from autumn to spring. View the pond garden from the hall, then walk down into it. Last entry 15:30."),
        caution=T("受付は9:30〜15:30。ほかのお寺より早く閉まります", "Entry 9:30–15:30: it closes earlier than the others"),
        lat=35.12055, lng=135.83408,
        body=T("実光院（じっこういん）\n\n三千院と勝林院のあいだ、道の西側にあります。勝林院の子院です。\n\n"
               "庭は2つ。客殿の南の「契心園（けいしんえん）」は、座って眺める池の庭。西の「旧理覚院庭園」は下りて歩ける庭で、大原の山を借景にしています。約120種の山野草が植えられています。\n\n"
               "庭のまん中の「不断桜（ふだんざくら）」は、10月の中ごろから翌年の4月ごろまで咲きます。秋は桜ともみじ、冬は桜と雪がいっしょに見られます。\n\n"
               "宝泉院と似た「座って庭を見るお寺」ですが、こちらは人が少なく、庭を歩けます。時間がない日は、宝泉院か実光院のどちらか1つで十分です。お抹茶つきの拝観もあります。",
               "Jikko-in\n\nOn the west side of the lane between Sanzen-in and Shorin-in, of which it is a sub-temple.\n\n"
               "There are two gardens. Keishin-en, south of the guest hall, is a pond garden to view sitting down. The former Rikaku-in garden to the west is one you walk through, with the Ohara hills as borrowed scenery and about 120 kinds of wild flowers.\n\n"
               "The “fudan-zakura” cherry in the middle of the garden flowers from mid October to around April: cherry blossom with maples in autumn, with snow in winter.\n\n"
               "Like Hosen-in, this is a temple for sitting and looking at a garden, but it is quieter and you can walk in the garden. If you are short of time, one of the two is enough. Entry with matcha is available."),
        gmaps=[gm("実光院", "Jikko-in", 35.12055, 135.83408, "実光院 大原 京都")],
        links=[link("official", "実光院 公式サイト", "Jikko-in (official)", "https://jikkoin.com/", "https://jikkoin.com/english/")],
        info=info([row("hours", "受付 9:30〜15:30（季節で変わることがあります）。見学は約20分", "Entry 9:30–15:30 (may change with the season). Allow about 20 minutes"),
                   row("closed", "休みなし", "Open every day"),
                   row("fee", "中学生以上600円、小学生以下300円。お抹茶・お菓子つきは1,100円", "¥600 (junior high and up), ¥300 children; ¥1,100 with matcha and a sweet")],
                  "実光院 公式サイト（受付時間は2026-11-22、料金は2026-11-21に確認）", cash=True,
                  tip=T("実光院の公式サイトで確認しました（受付時間は11月22日、料金は21日）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。", "Checked on the temple’s website (entry hours on 22 November, fees on the 21st). Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    otonashi=dict(
        name=T("来迎院と音無の滝", "Raigo-in & Otonashi falls"), kind=T("寺・滝（山道）", "Temple & waterfall"),
        blurb=T("三千院の奥の山道を歩いて、杉木立の中の来迎院と、声明の伝説が残る滝へ。往復で40〜50分。寄り道です。",
                "A path into the hills behind Sanzen-in, to Raigo-in among the cedars and a waterfall with a legend of Buddhist chant. 40–50 minutes return. A side trip."),
        caution=T("土の山道。店もトイレもありません。明るいうちに戻る", "An earth path with no shops or toilets. Be back in daylight"),
        lat=35.12062, lng=135.83974,
        body=T("来迎院（らいごういん）と音無の滝（おとなしのたき）\n\n三千院の前の道を南の端まで戻り、呂川に沿って山のほうへ上ります。来迎院まで約300m、歩いて5〜10分。そこから山道をさらに約400m、10分ほどで音無の滝です。\n\n"
               "来迎院は、平安時代の終わりに良忍（りょうにん）が声明の道場として開いたお寺です。三千院のにぎわいがうそのように静かです。\n\n"
               "音無の滝は、岩の上を水がすべり落ちる滝です。良忍がここで声明の稽古をしていると、声と滝の音がひとつになって、滝の音が聞こえなくなった、と伝わります。\n\n"
               "来迎院までは舗装された坂道、その先は土の山道です。雨のあとはぬかるむので、すべりにくい靴で。滝までの道に店やトイレはありません。山あいは暗くなるのが早いので（11月下旬の日の入りは16:50ごろ）、明るいうちに戻ってください。\n\n"
               "歩くのを減らしたい日は、ここを外してください。",
               "Raigo-in and Otonashi falls\n\nGo back to the south end of the lane in front of Sanzen-in and follow the Rosen stream uphill. Raigo-in is about 300 m on, 5–10 minutes; the falls are another 400 m or so along a hill path, about 10 minutes.\n\n"
               "Raigo-in was founded at the end of the Heian period by the monk Ryonin as a training hall for shomyo chant. After the bustle of Sanzen-in it is strikingly quiet.\n\n"
               "At Otonashi-no-taki, the “soundless waterfall”, water slides down a rock face. The story goes that when Ryonin practised chanting here, his voice and the falls became one and the sound of the water could no longer be heard.\n\n"
               "The way is a paved slope as far as Raigo-in, then an earth path. It gets muddy after rain, so wear shoes with grip. There are no shops or toilets on the way. It gets dark early in the hills (sunset in late November is at about 16:50): be back while it’s light.\n\n"
               "To cut down on walking, leave this one out."),
        gmaps=[gm("音無の滝", "Otonashi falls", 35.12062, 135.83974, "音無の滝 大原 京都"), gm("来迎院", "Raigo-in", 35.11861, 135.83767, "来迎院 大原 京都")],
        links=[link("info", "来迎院（大原観光保勝会）", "Raigo-in (Ohara tourist association, Japanese)", "https://kyoto-ohara-kankouhosyoukai.net/detail/5561/"), HOSHO],
        info=info([row("hours", "音無の滝は自由に見られます（山道。明るい時間に）", "The falls are free to visit (a hill path; go in daylight)"),
                   row("hours", "来迎院 9:00〜17:00、休みなし", "Raigo-in 9:00–17:00, open every day"),
                   row("fee", "来迎院 大人400円（5月1日〜30日と11月1日〜30日は宝物展のため500円）。子どもの料金は案内に書かれていません", "Raigo-in ¥400 for adults (¥500 from 1 to 30 May and 1 to 30 November, during the treasure exhibition). No child fee is given")],
                  "大原観光保勝会「来迎院」https://kyoto-ohara-kankouhosyoukai.net/detail/5561/（2026-11-24。来迎院は公式サイトがない）、OpenStreetMap（道の距離。2026-11-21）", checked=D24,
                  tip=T("来迎院の時間と料金は、大原観光保勝会のサイトで確認しました（11月24日。来迎院には公式サイトがありません）。滝の位置と道の距離は OpenStreetMap で測った目安です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Raigo-in’s hours and fee were checked on the Ohara tourist association’s site (24 November; the temple has no website of its own). The position of the falls and the distances are estimates from OpenStreetMap. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    sato=dict(
        name=T("お昼と、大原の里の道", "Lunch & the valley walk"), kind=T("お昼・里の道", "Lunch & village walk"),
        blurb=T("大原のお昼は早めに、14時までに。三千院の門前かバス停のまわりで食べて、田んぼと畑のあいだの道を歩きます。",
                "Eat early in Ohara, by 14:00 at the latest: at Sanzen-in’s gate or around the bus stop, then walk the lane between the fields."),
        caution=T("お昼の店は閉まるのが早い土地です。11時半ごろに入るのが楽", "Lunch places here close early. Sitting down at about 11:30 is easiest"),
        lat=35.12160, lng=135.82520,
        body=T("お昼と、大原の里（さと）の道\n\n"
               "お昼は早めに\n大原の食事の店は、昼だけ開けて夕方前に閉まる所がほとんどです。秋の12時台は並ぶ店が多いので、11時半ごろに入ってしまうのがいちばん楽です。遅くとも14時までに。夜に開いている店はあまりないので、晩ごはんは街なかへ戻ってからにしてください。\n\n"
               "時間を確かめられた店\n"
               "・芹生（せりょう）のお食事処「ひな里」：三千院の門前、石段を下りたところの料理旅館です。三千草（みちくさ）弁当3,850円、湯豆腐膳3,300円（公式サイトの値段）。昼は11:30〜15:00（大原観光保勝会の案内）。旅館の公式サイトには「季節により利用できないことがあります」とあるので、あてにする日は先に電話（075-744-2301）で確かめてください。\n"
               "・里の駅 大原の「花むらさき」：大原バス停から国道を南へ約1km、「野村別れ（里の駅大原）」バス停の近くにある農産物の直売所の食堂です。ランチは11:00〜14:00、カフェは11:00〜15:30（ラストオーダー15:00）。看板の親子丼は1,320円、日替わりの大原膳は1,100円。月曜休み（祝日のときは翌日の火曜）。日曜は朝6:00〜9:00に朝市があり、食堂も7:30〜9:00に朝の営業をします（卵かけご飯660円とカフェ。9:00〜11:00は準備で休み）。寂光院から歩くと25分ほどです。\n\n"
               "トイレは、大原バス停の中と、寂光院の近くの駐車場（大原寂光院駐車場）に京都市の公衆トイレがあります。\n\n"
               "ほかに、参道とバス停のまわりに、そば・うどん、定食、甘味の店があります。営業日と時間は店ごとに違い、ここでは確かめきれていません。行きたい店がある人は先に調べてください（大原観光保勝会のサイトに店の一覧があります）。\n\n"
               "里の道\n寂光院は、谷の反対側にあります。バス停から国道を渡らずに西へ下り、高野川（たかのがわ）を渡って、案内板にしたがって歩きます。寂光院の案内では約15分。ゆっくり歩いて20分。三千院の前からだと35分ほどです。\n\n"
               "道の両側は田んぼと畑で、しば漬に使う赤しその畑もあります（赤しそは夏）。三千院のあたりより人が少なく、山に囲まれた大原の里がよく見えます。\n\n"
               "畑や家の敷地には入らないでください。車も通る細い道なので、道の端を歩きましょう。",
               "Lunch and the valley walk\n\n"
               "Eat early\nMost places to eat in Ohara open for lunch only and shut before evening. In autumn many have queues between 12:00 and 13:00, so the easiest plan is to sit down at about 11:30, and by 14:00 at the latest. Little is open at night, so have dinner back in the city.\n\n"
               "Places whose hours could be checked\n"
               "• Hinasato, the dining room of the inn Seryo: at the foot of the stone steps in front of Sanzen-in. Michikusa bento ¥3,850, yudofu set ¥3,300 (prices from the official website). Lunch is served 11:30–15:00 (per the Ohara tourist association). The inn’s website says it “may not be available in some seasons”, so phone ahead (075-744-2301) if you are counting on it.\n"
               "• Hanamurasaki at Sato-no-Eki Ohara: the diner of a farmers’ market about 1 km south of the Ohara bus stop along the main road, near the Nomura-wakare (Sato-no-Eki Ohara) stop. Lunch 11:00–14:00, café 11:00–15:30 (last orders 15:00). The house oyakodon is ¥1,320; the daily Ohara set ¥1,100. Closed Mondays (Tuesday if Monday is a holiday). On Sundays a morning market runs 6:00–9:00, and the diner opens early, 7:30–9:00, for tamago-kake-gohan (rice with raw egg, ¥660) and drinks; it then closes 9:00–11:00 to get ready. About 25 minutes on foot from Jakko-in.\n\n"
               "There are city public toilets inside the Ohara bus terminal and at the Ohara Jakko-in car park near the temple.\n\n"
               "Along the lane and around the bus stop there are also soba and udon shops, set-meal places and sweet shops. Their days and hours differ and could not all be checked here: if you have one in mind, look it up first (the tourist association’s website lists them).\n\n"
               "The valley walk\nJakko-in is on the other side of the valley. From the bus stop, without crossing the main road, head downhill to the west, cross the Takano river and follow the signs. The temple gives it as about 15 minutes; allow 20 at an easy pace. From Sanzen-in’s gate it is about 35.\n\n"
               "The lane runs between rice fields and vegetable plots, some growing the red shiso used for shibazuke (in summer). There are fewer people than around Sanzen-in, and you get the open view of the valley ringed by hills.\n\n"
               "Please keep out of the fields and private yards. Cars use this narrow lane too, so walk at the side."),
        gmaps=[gm("寂光院への道", "Lane to Jakko-in", 35.12160, 135.82520, "寂光院 大原 京都"),
               gm("芹生（ひな里）", "Seryo (Hinasato)", 35.11966, 135.83410, "芹生 大原 京都"),
               gm("里の駅 大原", "Sato-no-Eki Ohara", 35.112169, 135.825645, "里の駅大原")],
        links=[link("official", "芹生 料理のご案内", "Seryo: dining (official, Japanese)", "https://www.seryo.co.jp/cuisine.html"),
               link("official", "里の駅 大原", "Sato-no-Eki Ohara (official, Japanese)", "http://www.satonoeki-ohara.com"),
               link("info", "大原観光保勝会「食べる」", "Ohara tourist association: places to eat (Japanese)", "https://kyoto-ohara-kankouhosyoukai.net/eat/")],
        info=info([row("hours", "芹生「ひな里」昼 11:30〜15:00（大原観光保勝会の案内）。季節により利用できないことがあります（芹生の公式サイト）", "Seryo “Hinasato” lunch 11:30–15:00 (per the Ohara tourist association). It may not be available in some seasons (inn’s website)"),
                   row("fee", "芹生「ひな里」三千草弁当3,850円、湯豆腐膳3,300円。京ゆば膳4,400円は要予約", "Seryo “Hinasato”: Michikusa bento ¥3,850, yudofu set ¥3,300. The yuba set (¥4,400) must be booked"),
                   row("hours", "里の駅 大原「花むらさき」ランチ11:00〜14:00、カフェ11:00〜15:30（ラストオーダー15:00）。日曜は7:30〜9:00に朝の営業（9:00〜11:00は休み）。日曜の朝市 6:00〜9:00", "Sato-no-Eki Ohara “Hanamurasaki”: lunch 11:00–14:00, café 11:00–15:30 (last orders 15:00). Sundays also 7:30–9:00 (closed 9:00–11:00). Sunday morning market 6:00–9:00"),
                   row("fee", "花むらさき：こだわりの親子丼1,320円、日替わり大原膳1,100円、日曜朝の卵かけご飯660円", "Hanamurasaki: oyakodon ¥1,320, daily Ohara set ¥1,100, Sunday-morning tamago-kake-gohan ¥660"),
                   row("closed", "花むらさきは月曜休み（祝日のときは翌日の火曜）", "Hanamurasaki is closed on Mondays (Tuesday if Monday is a holiday)"),
                   row("hours", "トイレ：大原バス停の中（6:30ごろ〜21:30ごろ）と大原寂光院駐車場（いつでも）に京都市の公衆トイレ", "Toilets: city public toilets in the Ohara bus terminal (about 6:30–21:30) and at the Ohara Jakko-in car park (always open)"),
                   row("hours", "大原バス停から寂光院まで歩いて約15分（寂光院の案内）。このマップでは20分でみています", "About 15 min on foot from the Ohara bus stop to Jakko-in (temple’s access page). This map allows 20")],
                  "芹生 公式サイト（料理のご案内）https://www.seryo.co.jp/cuisine.html、大原観光保勝会「芹生」https://kyoto-ohara-kankouhosyoukai.net/detail/4712/（昼食プランの時間）、"
                  "里の駅大原 公式サイト（店舗情報 https://www.satonoeki-ohara.com/access/、花むらさき https://www.satonoeki-ohara.com/hanamurasaki/、"
                  "お知らせ「花むらさきの営業時間がかわります」https://www.satonoeki-ohara.com/blog/3396/、朝市 https://www.satonoeki-ohara.com/market/）、"
                  "京都市「(R1)大原の里公衆トイレ」「(R2)寂光院公衆トイレ」https://www.city.kyoto.lg.jp/kankyo/page/0000331162.html、寂光院 公式サイト。2026-11-24", checked=D24,
                  tip=T("芹生の値段は芹生の公式サイト、昼の時間は大原観光保勝会のサイト、花むらさきの時間・値段・休みは里の駅大原の公式サイト、トイレは京都市のサイトで確認しました（11月24日）。里の駅までの距離は地図で測った目安です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Seryo’s prices are from its website and its lunch hours from the Ohara tourist association’s site; Hanamurasaki’s hours, prices and closing day from Sato-no-Eki Ohara’s website; the toilets from Kyoto City’s site (all checked 24 November). The distance to Sato-no-Eki is an estimate from the map. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    jakkoin=dict(
        name=T("寂光院", "Jakko-in"), kind=T("尼寺（平家物語）", "Nunnery (Tale of the Heike)"),
        blurb=T("平家が滅びたあと、建礼門院が余生を送った尼寺。三千院より小さく、人も少ないお寺です。バス停から歩いて20分。",
                "The nunnery where Kenreimon-in lived out her days after the fall of the Heike. Smaller and quieter than Sanzen-in; 20 minutes’ walk from the bus stop."),
        caution=T("12〜2月は16:30まで。拝観料は現金を用意", "Closes 16:30 Dec–Feb. Bring cash for the fee"),
        lat=35.12406, lng=135.82082,
        body=T("寂光院（じゃっこういん）\n\n聖徳太子が594年に建てたと伝わる、天台宗の尼寺です。石段を上った先に、小さな本堂と池の庭があります。\n\n"
               "建礼門院（けんれいもんいん）は平清盛の娘で、安徳天皇の母です。1185年、壇ノ浦で平家が滅び、幼い天皇も海に沈みました。ひとり助けられた女院は、その年の秋にここへ入り、一門と我が子を弔って暮らしました。翌年の春、後白河法皇が訪ねてくる場面が『平家物語』の終わりの「大原御幸（おおはらごこう）」です。\n\n"
               "本堂の前の汀の池（みぎわのいけ）と桜は、その場面に出てくるものです。本堂の北の奥に、女院の庵のあとが残っています。\n\n"
               "本堂は2000年5月の火災で焼け、2005年に元の姿で建て直されました。今の本尊の地蔵菩薩像もそのときに作られたもので、色があざやかです。焼けた旧本尊は収蔵庫にあり、特別公開の日だけ見られます。\n\n"
               "石段のもみじは秋がきれいです。客殿でお抹茶もいただけます。",
               "Jakko-in\n\nA Tendai nunnery said to have been founded by Prince Shotoku in 594. Up a flight of stone steps are a small main hall and a pond garden.\n\n"
               "Kenreimon-in was the daughter of Taira no Kiyomori and mother of the child emperor Antoku. In 1185 the Heike were destroyed at Dan-no-ura and the emperor was lost to the sea. She alone was pulled from the water, and that autumn she came here to pray for her clan and her son for the rest of her life. The visit paid to her the next spring by the retired emperor Go-Shirakawa is the closing chapter of the Tale of the Heike.\n\n"
               "The pond and the cherry tree in front of the main hall appear in that scene. Behind the hall to the north is the site of her hermitage.\n\n"
               "The main hall burned down in May 2000 and was rebuilt as it had been in 2005. The present Jizo statue was made then too, and its colours are bright. The fire-damaged original is kept in a storehouse and shown only on special opening days.\n\n"
               "The maples over the stone steps are good in autumn, and you can have matcha in the guest hall."),
        gmaps=[gm("寂光院", "Jakko-in", 35.12406, 135.82082, "寂光院 大原 京都")],
        links=[link("official", "寂光院 公式サイト", "Jakko-in (official)", "https://www.jakkoin.jp/", "https://www.jakkoin.jp/en/")],
        info=info([row("hours", "3〜11月 9:00〜17:00／12月と1月4日〜2月 9:00〜16:30／1月1〜3日 10:00〜16:00", "Mar–Nov 9:00–17:00 / Dec and 4 Jan–Feb 9:00–16:30 / 1–3 Jan 10:00–16:00"),
                   row("fee", "大人・高校生600円、中学生350円、小学生100円", "¥600 (adults and high school); junior high ¥350; elementary ¥100")],
                  "寂光院 公式サイト。2026-11-21に確認", cash=True, checked=D21,
                  tip=T("寂光院の公式サイトで確認しました（11月21日）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Checked on the temple’s website (21 November). Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    kaeri=dict(
        name=T("帰りのバスと、街なかの夜", "The bus back & an evening in town"), kind=T("帰り・夜", "Return & evening"),
        blurb=T("三条京阪前まで乗り換えなしの最後は17:47発。大原の最終は21:01発（国際会館駅前行き）。晩ごはんは三条・先斗町で。",
                "The last bus straight to Sanjo-Keihan-mae leaves at 17:47; the very last bus from Ohara is at 21:01 (to Kokusaikaikan station). Have dinner around Sanjo and Pontocho."),
        caution=T("三条へ乗り換えなしの最後は17:47発。最終は21:01発（国際会館駅前行き）", "Last direct bus to Sanjo 17:47. Last bus of all 21:01 (to Kokusaikaikan station)"),
        lat=35.008548, lng=135.772454,
        body=T("帰りのバスと、街なかの夜\n\n"
               "大原は日が暮れると店が閉まり、道も暗くなります。晩ごはんは街なかへ戻ってから。帰りのバスは大原が始発なので、少し早めに並べば座れます。\n\n"
               "帰りのバス（大原バス停から）\n"
               "・17系統 京都駅前行き：1時間に2本。出町柳駅前まで約34分・490円、三条京阪前まで約43分・570円、四条河原町まで約50分・590円。最後は17:27発（三条京阪前18:10着）。\n"
               "・17:47発（特16系統）：三条京阪前止まり、18:40着。三条まで乗り換えなしで帰れる最後のバスです。\n"
               "・18時からは国際会館駅前行き（19系統）だけになります。18:21（日曜・祝日は18:25）、19:01、20:01、21:01発。21:01が最終です。国際会館駅前まで約23分・400円、そこから地下鉄で烏丸御池まで14分・290円（京都市役所前へは烏丸御池で東西線に乗り換え）。\n\n"
               "秋の夕方は国道が混んで、バスが遅れることがあります。夜に予約を入れた日は、1本早いバスで。\n\n"
               "三条京阪前で降りたら\n"
               "降りたところが三条大橋の東のたもとです。橋を西へ渡ると、木屋町通（きやまちどおり）と先斗町（ぽんとちょう）まで歩いて5分ほど。先斗町は三条通から四条通まで続く石畳の細い路地で、料理屋さんや居酒屋さんが並びます。表にお品書きを出している店が多いので、歩きながら決められます。\n\n"
               "遅くまで開いている店もありますが、閉まる時間とラストオーダーは店ごとに違います。入る前に表の案内で確かめてください。晩ごはんのあとは、鴨川の河原を歩いて四条へ出ても、三条へ戻っても10分ほどです。\n\n"
               "お店を決めておきたい人は、同じサイトの叡山電鉄のマップの24〜26番（祇園四条・ともしび3rd・先斗町）も見てください。\n\n"
               "出町柳駅前で降りる\n"
               "三条の手前、出町柳駅前で降りると、鴨川デルタ（川が合わさる三角の河原と飛び石）まで歩いて3分、下鴨神社の糺の森（ただすのもり）まで10分ほどです。早い時間に大原を出た日の寄り道に向いています。出町柳から三条へは、京阪電車で3分・240円。鴨川の河原を歩くと40分ほどです。",
               "The bus back and an evening in town\n\n"
               "After dark the shops in Ohara are shut and the lanes are unlit, so have dinner back in the city. Ohara is the first stop for the buses back: queue a little early and you get a seat.\n\n"
               "Buses back (from the Ohara stop)\n"
               "• Bus 17 for Kyoto Station: two an hour. About 34 minutes to Demachiyanagi-ekimae (¥490), 43 minutes to Sanjo-Keihan-mae (¥570), 50 minutes to Shijo-Kawaramachi (¥590). The last leaves at 17:27 (Sanjo-Keihan-mae 18:10).\n"
               "• The 17:47 (bus Toku-16) ends at Sanjo-Keihan-mae, arriving 18:40. It is the last bus to Sanjo without a change.\n"
               "• From 18:00 the only buses go to Kokusaikaikan station (bus 19): 18:21 (18:25 on Sundays and holidays), 19:01, 20:01 and 21:01. The 21:01 is the last. About 23 minutes, ¥400; then the subway to Karasuma Oike takes 14 minutes, ¥290 (for Kyoto Shiyakusho-mae, change to the Tozai line at Karasuma Oike).\n\n"
               "On autumn afternoons the main road gets busy and buses run late. If you have a dinner booking, take one bus earlier.\n\n"
               "Getting off at Sanjo-Keihan-mae\n"
               "You are at the east end of Sanjo Ohashi bridge. Cross it to the west and Kiyamachi-dori and Pontocho are about 5 minutes away. Pontocho is a narrow stone-paved alley running from Sanjo-dori to Shijo-dori, lined with small restaurants and izakaya. Many post their menus outside, so you can choose as you walk.\n\n"
               "Some places stay open late, but closing times and last orders differ: check the sign at the door before you go in. After dinner it’s about 10 minutes along the Kamo riverbank either down to Shijo or back to Sanjo.\n\n"
               "If you’d rather have a place picked out, see stops 24–26 (Gion-Shijo, Tomoshibi 3rd, Pontocho) on the Eizan Railway map on this site.\n\n"
               "Getting off at Demachiyanagi-ekimae\n"
               "Get off here, before Sanjo, and the Kamo delta (the triangle of riverbank where two rivers meet, with stepping stones) is 3 minutes’ walk and the Tadasu-no-mori forest of Shimogamo Shrine about 10. A good stop on a day you leave Ohara early. From Demachiyanagi to Sanjo it’s 3 minutes by Keihan train, ¥240, or about 40 minutes on foot along the river."),
        gmaps=[gm("三条京阪前（バス停）", "Sanjo-Keihan-mae bus stop", 35.008548, 135.772454, "三条京阪前 バス停"),
               gm("先斗町", "Pontocho", 35.00590, 135.77100, "先斗町 京都"),
               gm("鴨川デルタ（出町柳）", "Kamo delta (Demachiyanagi)", 35.03020, 135.77190, "鴨川デルタ")],
        links=[KBUS_OHARA,
               link("info", "叡山電鉄のマップ（夜の祇園四条・先斗町は24〜26番、出町柳は1〜5番）", "Eizan Railway map (evening stops 24–26; Demachiyanagi 1–5)", "../eizan-line/#list")],
        _rows=[row("train", "大原 → 三条京阪前（17系統・570円）：毎時27分と57分発（土日祝と、12月4日までの平日）。ふだんの平日は毎時27分（17系統）と45分（特17系統）。最後は17:27発 → 18:10着",
                   "Ohara → Sanjo-Keihan-mae (bus 17, ¥570): at :27 and :57 past each hour (weekends, holidays, and weekdays until 4 December). On ordinary weekdays at :27 (bus 17) and :45 (bus Toku-17). The last leaves at 17:27 → 18:10"),
               row("train", "17:47発（特16系統）→ 三条京阪前 18:40着。三条まで乗り換えなしの最後",
                   "17:47 (bus Toku-16) → Sanjo-Keihan-mae 18:40: the last bus to Sanjo without a change"),
               row("train", "大原 → 国際会館駅前（19系統・約23分・400円）：18:21（日祝18:25）、19:01、20:01、21:01発（最終）。地下鉄は国際会館 → 烏丸御池 14分・290円",
                   "Ohara → Kokusaikaikan-ekimae (bus 19, about 23 min, ¥400): 18:21 (18:25 Sundays and holidays), 19:01, 20:01, 21:01 (the last). Subway Kokusaikaikan → Karasuma Oike: 14 min, ¥290"),
               row("train", "出町柳 → 三条（京阪）3分・240円", "Demachiyanagi → Sanjo (Keihan): 3 min, ¥240")],
        _tip=T("バスの時刻と運賃は、京都バスの公式サイトの時刻表で確認しました（2026年9月28日改正のダイヤと、11月21日〜12月6日の秋のダイヤ）。地下鉄と京阪は乗換案内です。歩く時間は地図で見た目安です。先斗町の店の営業時間は、1軒ずつは確かめていません。写真は2024年11月18日の夜、大原バス停で撮ったバスです。",
               "Bus times and fares were checked on Kyoto Bus’s official timetable (the timetable revised on 28 September 2026 and the autumn timetable for 21 November–6 December); the subway and Keihan on a route planner. Walking times are estimates from the map. Opening hours of individual places in Pontocho were not checked. The photo shows a bus at the Ohara stop on the evening of 18 November 2024."),
        _source="京都バス公式サイトの時刻表・運賃（2026-11-22）、乗換案内（Yahoo!路線情報）2026-11-22"),
)

VIS, ARR, DEP = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time"), ("おすすめの時間", "Recommended time")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
# （スポットの id, 時間の見出し, 時間（日本語）, 時間（英語）, そのコースでの行き方の一言）
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="ohara.json",
        note="「9〜10時に出発」コース。三条京阪前9:07発（四条河原町8:59発）→大原9:48着。人の集まる三千院を午後に回し、先に谷の反対側の寂光院へ→里の道を戻って11時半ごろにお昼→参道→宝泉院→実光院→14時すぎの三千院→16:27発のバスで三条京阪前17:10着→三条・先斗町で晩ごはん。来迎院と音無の滝は寄り道。",
        rows=[row("train", "行き：三条京阪前 9:07発（17系統。四条河原町 8:59発、出町柳駅前 9:16発）→ 大原 9:48着・570円。毎日同じ時刻です",
                  "Out: Sanjo-Keihan-mae 9:07 (bus 17; Shijo-Kawaramachi 8:59, Demachiyanagi-ekimae 9:16) → Ohara 9:48, ¥570. The same every day"),
              row("train", "次のバス：土日祝は三条京阪前 9:40発 → 10:22着、10:10発 → 10:52着。平日は 9:37発 → 10:18着（12月7日からは国際会館駅前経由で10:27着）、10:10発 → 10:52着",
                  "Next buses: on weekends and holidays, Sanjo-Keihan-mae 9:40 → 10:22 and 10:10 → 10:52. On weekdays, 9:37 → 10:18 (10:27, via Kokusaikaikan, from 7 December) and 10:10 → 10:52"),
              row("train", "地下鉄で行くなら：烏丸御池 → 国際会館 14分・290円、国際会館駅前 9:36発（平日）／9:40発（土日祝）→ 大原 約22分・400円",
                  "By subway: Karasuma Oike → Kokusaikaikan, 14 min, ¥290; then Kokusaikaikan-ekimae 9:36 (weekdays) / 9:40 (weekends and holidays) → Ohara, about 22 min, ¥400")],
        order=[
            ("bus", ARR, "9:48（三条京阪前 9:07発）", "9:48 (the 9:07 from Sanjo-Keihan-mae)",
             T("三条京阪前9:07発の17系統に乗ります（四条河原町からは8:59発）。このバスは毎日同じ時刻で、大原に9:48に着きます。1本あとは9:40ごろ発・10:20ごろ着。そのときは、この先を30分ずつ遅らせてください。\n\n"
               "この時間に着くと、三千院はちょうど団体が増えてくるころです。このコースでは三千院を午後に回して、先に谷の反対側の寂光院へ歩きます。バスを降りたら、国道を渡らずに西へ。\n\n"
               "帰りは16:27発のバスで、三条京阪前に17:10に着きます。",
               "Take the 9:07 bus 17 from Sanjo-Keihan-mae (8:59 from Shijo-Kawaramachi). It runs at the same time every day and reaches Ohara at 9:48. The next leaves at about 9:40 and arrives at about 10:20; if you take that, shift everything below by 30 minutes.\n\n"
               "Arriving at this hour, Sanzen-in is just filling with tour groups. So this course leaves Sanzen-in for the afternoon and walks first to Jakko-in, on the other side of the valley. From the bus, head west without crossing the main road.\n\n"
               "You go back on the 16:27 bus, reaching Sanjo-Keihan-mae at 17:10.")),
            ("jakkoin", VIS, "10:10〜10:55", "10:10–10:55",
             T("バス停から里の道を歩いて約20分。午前の寂光院は静かです。見終わったら、同じ道をバス停のほうへ戻ります。",
               "About 20 minutes along the valley lane from the bus stop. Jakko-in is quiet in the morning. Afterwards, walk back the same way towards the bus stop.")),
            ("sato", VIS, "里の道 10:55〜11:15、お昼 11:30〜12:30", "Valley walk 10:55–11:15, lunch 11:30–12:30",
             T("寂光院から里の道を戻って、バス停に11:15ごろ。そのまま参道を上って、三千院の門前かその手前で11:30ごろにお昼にします。昼の混雑の前に入れる時間です。里の駅 大原の花むらさきで食べるなら、寂光院から南へ歩いて約25分。食後は国道を北へ15分ほど歩いてバス停に戻ります。",
               "Walk back along the valley lane from Jakko-in to reach the bus stop at about 11:15. Carry on up the lane and have lunch at about 11:30, at Sanzen-in’s gate or just below it: early enough to beat the midday rush. For Hanamurasaki at Sato-no-Eki Ohara, walk about 25 minutes south from Jakko-in; after lunch it’s about 15 minutes north along the main road back to the bus stop.")),
            ("sando", VIS, "上り 11:15〜11:30、店は帰りの15:30〜16:00に", "Up 11:15–11:30; shops on the way down, 15:30–16:00",
             T("お昼の前に上ります。買い物は帰り道に。三千院を15:30に出れば、16:00に閉まる志ば久にも間に合います。",
               "You climb it before lunch. Leave the shopping for the way down: come out of Sanzen-in at 15:30 and you are still in time for Shibakyu, which closes at 16:00.")),
            ("hosenin", VIS, "12:40〜13:30", "12:40–13:30",
             T("お昼のあと、三千院の門の前を通りすぎて北へ約5分。食後のお抹茶をここで。",
               "After lunch, walk past Sanzen-in’s gate and about 5 minutes north. Have your after-lunch matcha here.")),
            ("jikkoin", VIS, "13:35〜14:00", "13:35–14:00",
             T("宝泉院から三千院のほうへ戻る途中、右手にあります。受付は15:30までなので、三千院より先に。",
               "On your right as you walk back from Hosen-in towards Sanzen-in. Last entry is 15:30, so come here before Sanzen-in.")),
            ("otonashi", VIS, "14:05〜14:55（寄る日は三千院を15:00〜16:15に。12〜2月は外す）", "14:05–14:55 (then Sanzen-in 15:00–16:15; skip in Dec–Feb)",
             T("このコースでは寄り道です。寄ると三千院が15時からになり、帰りのバスは16:57発（三条京阪前17:40着）になります。三千院が16:30に閉まる12〜2月は、ここを外してください。",
               "A side trip on this course. It pushes Sanzen-in back to 15:00 and your bus to the 16:57 (Sanjo-Keihan-mae 17:40). From December to February, when Sanzen-in closes at 16:30, leave it out.")),
            ("sanzenin", VIS, "14:10〜15:30", "14:10–15:30",
             T("昼の団体が帰りはじめることが多い時間です。客殿の縁側でゆっくり座って、苔の庭へ。11月は16:45、12〜2月は16:30に閉まります。\n\n"
               "出たら参道を下って、バス停まで約15分。16:27発のバスに乗ります。",
               "By now the midday groups have usually begun to leave. Sit a while on the veranda of the guest hall, then go down into the moss garden. It closes at 16:45 in November and 16:30 from December to February.\n\n"
               "Afterwards walk down the lane, about 15 minutes to the bus stop, for the 16:27 bus.")),
            ("kaeri", DEP, "大原 16:27発 → 三条京阪前 17:10着。晩ごはんは18時ごろから", "Ohara 16:27 → Sanjo-Keihan-mae 17:10. Dinner from about 18:00",
             T("16:27発に乗ると、三条京阪前に17:10に着きます。16:57発なら17:40着、17:27発なら18:10着。宿でひと休みするか、鴨川の河原を少し歩いてから、18時ごろ先斗町・木屋町で晩ごはんに。そのまま21〜22時ごろまで、街なかの夜を楽しめます。",
               "The 16:27 gets you to Sanjo-Keihan-mae at 17:10 (the 16:57 at 17:40, the 17:27 at 18:10). Rest at your hotel or stroll the Kamo riverbank, then have dinner in Pontocho or Kiyamachi from about 18:00. From there the evening in town can run on to 21:00 or 22:00.")),
        ],
        sections=[dict(first="bus", last="jakkoin", day=0), dict(first="sato", last="sando", day=1),
                  dict(first="hosenin", last="sanzenin", day=2), dict(first="kaeri", last="kaeri", day=3)],
        focus=("bus", "sanzenin"),
        default=["jakkoin", "sato", "sando", "hosenin", "jikkoin", "sanzenin"], auto=["bus", "kaeri"],
        extra_notices={"sanzenin": [notice("12〜2月は16:30に閉まります", "Closes at 16:30 from December to February",
                                           "このコースは14:10に入ります。音無の滝へ寄る日は三千院が15時からになるので、冬は滝を外してください。",
                                           "This course goes in at 14:10. With the falls added, Sanzen-in starts at 15:00, so leave the falls out in winter.",
                                           frm="2026-12-01", to="2027-02-28")]},
        hints=[("sanzenin", dict(any=["sanzenin"], none=["jakkoin"]), None, None,
                "寂光院に行かない日は、バス停から参道を上って先に宝泉院・実光院へ。11:30にお昼を食べて、三千院は12:30ごろから。14:27発か14:57発のバスで戻れます（14:57発は土日祝と12月4日までの平日）。",
                "Skipping Jakko-in? Walk up the lane and see Hosen-in and Jikko-in first, have lunch at 11:30 and go into Sanzen-in at about 12:30. You can take the 14:27 or 14:57 bus back (the 14:57 runs on weekends, holidays, and weekdays until 4 December)."),
               ("jikkoin", dict(any=["jikkoin"], andAny=["hosenin"]), None, None,
                "宝泉院と実光院は、どちらも座って庭を見るお寺です。お抹茶は宝泉院の拝観料についているので、実光院はお抹茶なし（600円）で入ると重なりません。",
                "Hosen-in and Jikko-in are both temples for sitting and looking at a garden. Matcha is included at Hosen-in, so take the plain ¥600 entry at Jikko-in."),
               ("jakkoin", dict(any=["jakkoin"], none=["sanzenin", "hosenin", "jikkoin", "otonashi"]), None, None,
                "寂光院だけの日は、里の道を戻って11:30ごろにお昼を食べ、12時台のバス（12:27発など）で戻れます。",
                "On a Jakko-in-only day, walk back along the lane, have lunch at about 11:30 and take a bus back in the 12:00 hour (the 12:27, for one)."),
               ("otonashi", dict(any=["otonashi"], none=["sanzenin"]), None, None,
                "音無の滝への道は、三千院の前の道の南の端から、川に沿って山のほうへ上ります。",
                "The path to the falls starts at the south end of the lane in front of Sanzen-in and follows the stream uphill.")]),
    dict(
        id="early", file="ohara-early.json",
        note="「三千院の開門に合わせる」コース。三条京阪前7:57発（四条河原町7:49発）→大原8:38着（平日）／8:49着（土日祝。国際会館駅前経由）。参道→三千院（11月は8:45、ほかの月は9:00開門）→宝泉院のお抹茶でひと休み→11:30にお昼→里の道→寂光院→大原14:27発→三条京阪前15:10着（出町柳駅前で降りて鴨川デルタ・下鴨神社へ寄り道も）→夜は三条・先斗町。実光院、来迎院と音無の滝は寄り道。",
        rows=[row("train", "行き（平日）：三条京阪前 7:57発（17系統。四条河原町 7:49発、出町柳駅前 8:06発）→ 大原 8:38着・570円",
                  "Out (weekdays): Sanjo-Keihan-mae 7:57 (bus 17; Shijo-Kawaramachi 7:49, Demachiyanagi-ekimae 8:06) → Ohara 8:38, ¥570"),
              row("train", "行き（土日祝）：三条京阪前 7:57発（特17系統・国際会館駅前経由。四条河原町 7:49発）→ 大原 8:49着・570円。1本前は 7:19発（特16系統）→ 8:09着",
                  "Out (weekends and holidays): Sanjo-Keihan-mae 7:57 (bus Toku-17 via Kokusaikaikan; Shijo-Kawaramachi 7:49) → Ohara 8:49, ¥570. The one before is the 7:19 (bus Toku-16) → 8:09"),
              row("train", "地下鉄で行くなら：烏丸御池 → 国際会館 14分・290円、国際会館駅前 7:46発（平日）→ 大原 8:08着／8:27発（土日祝）→ 8:49着・400円",
                  "By subway: Karasuma Oike → Kokusaikaikan, 14 min, ¥290; then Kokusaikaikan-ekimae 7:46 (weekdays) → Ohara 8:08 / 8:27 (weekends and holidays) → 8:49, ¥400")],
        order=[
            ("bus", ARR, "8:38（平日）／8:49（土日祝）。三条京阪前 7:57発", "8:38 (weekdays) / 8:49 (weekends and holidays): the 7:57 from Sanjo-Keihan-mae",
             T("三千院が開く時間に合わせるバスです。三条京阪前7:57発（四条河原町からは7:49発）。平日は8:38、土日祝は国際会館駅前を回るので8:49に着きます。ここから参道を15分上ると、三千院の門に9時ごろ。三千院は11月が8:45、ほかの月は9:00に開きます。\n\n"
               "朝ごはんは食べてから乗ってください。大原で朝早く開いている食事の店は、日曜の里の駅 大原（下）のほかは確かめられていません。三千院のあと、宝泉院のお抹茶とお菓子でひと休みして、11:30に早めのお昼にします。\n\n"
               "日曜だけの寄り道：1本早い7:19発（特16系統）に乗って、大原の2分手前の「野村別れ（里の駅大原）」で降りると（8:05着・550円）、里の駅 大原の朝市（6:00〜9:00）に間に合います。食堂の花むらさきも日曜は7:30〜9:00に開いていて、卵かけご飯（660円）で朝ごはんにできます。そこから三千院までは歩いて30分ほどです。\n\n"
               "帰りは14:27発のバスで、三条京阪前に15:10に着きます。",
               "This bus is timed for Sanzen-in’s opening: the 7:57 from Sanjo-Keihan-mae (7:49 from Shijo-Kawaramachi). It arrives at 8:38 on weekdays and, running via Kokusaikaikan station, at 8:49 on weekends and holidays. Fifteen minutes up the lane puts you at Sanzen-in’s gate at about 9:00. The temple opens at 8:45 in November and 9:00 in other months.\n\n"
               "Have breakfast before you board: apart from Sato-no-Eki Ohara on Sundays (below), no place to eat in Ohara could be confirmed as open this early. After Sanzen-in, rest over the matcha and sweet at Hosen-in, then have an early lunch at 11:30.\n\n"
               "A Sunday-only extra: take the earlier 7:19 (bus Toku-16) and get off at Nomura-wakare (Sato-no-Eki Ohara), two minutes before Ohara (8:05, ¥550), in time for the morning market at Sato-no-Eki Ohara (6:00–9:00). On Sundays its diner, Hanamurasaki, also opens 7:30–9:00, so you can breakfast on tamago-kake-gohan (rice with raw egg, ¥660). From there it’s about 30 minutes on foot to Sanzen-in.\n\n"
               "You go back on the 14:27 bus, reaching Sanjo-Keihan-mae at 15:10.")),
            ("sando", VIS, "8:40〜9:00（上るだけ。店は帰りに）", "8:40–9:00 (just the climb; shops later)",
             T("朝は店がまだ開いていないことが多いので、まっすぐ三千院へ上ります。買い物は三千院・宝泉院のあと、お昼の前後に。",
               "Most shops aren’t open yet, so go straight up to Sanzen-in. Shop after Sanzen-in and Hosen-in, around lunch.")),
            ("sanzenin", VIS, "9:00〜10:15（11月は8:45開門、ほかの月は9:00開門）", "9:00–10:15 (opens 8:45 in November, 9:00 in other months)",
             T("9時ごろ門に着きます。団体が増える前なので、客殿の縁側に座って庭を眺められます。10時を過ぎると人が増えてくるので、先に客殿と苔の庭、往生極楽院を見て、奥のあじさい苑や観音堂はそのあとに。",
               "You reach the gate at about 9:00, before the tour groups, so you can sit on the veranda of the guest hall and look at the garden. People build up after 10:00: see the guest hall, the moss garden and Ojo Gokuraku-in first, and the hydrangea garden and Kannon hall at the back afterwards.")),
            ("hosenin", VIS, "10:25〜11:10", "10:25–11:10",
             T("三千院の門を出て左（北）へ約5分。朝から歩いたあとの休憩にちょうどいい時間です。お抹茶とお菓子をいただきながら、額縁庭園をゆっくり。",
               "Turn left (north) out of Sanzen-in’s gate, about 5 minutes. A well-timed rest after the morning’s walking: take your time over the matcha, the sweet and the framed garden.")),
            ("jikkoin", VIS, "11:15〜11:40（寄る日は、お昼を11:45から）", "11:15–11:40 (then lunch from 11:45)",
             T("このコースでは寄り道です。宝泉院から三千院のほうへ戻る途中、右手にあります。寄るとお昼が15分遅くなるだけです。",
               "A side stop on this course. On your right as you walk back from Hosen-in towards Sanzen-in. It only delays lunch by 15 minutes.")),
            ("otonashi", VIS, "11:15〜12:05（寄る日は、お昼が12:15ごろ、寂光院が13:45〜14:30、バスは14:57発か15:27発）", "11:15–12:05 (then lunch at about 12:15, Jakko-in 13:45–14:30, and the 14:57 or 15:27 bus)",
             T("このコースでは寄り道です。寄るとお昼が12時すぎになり、店が混む時間に重なります。寂光院のあとのバスは14:57発（土日祝と12月4日までの平日）か15:27発に。",
               "A side trip on this course. It pushes lunch past 12:00, into the busy hour. After Jakko-in, take the 14:57 bus (weekends, holidays, and weekdays until 4 December) or the 15:27.")),
            ("sato", VIS, "お昼 11:30〜12:25、里の道 12:25〜13:00", "Lunch 11:30–12:25, valley walk 12:25–13:00",
             T("宝泉院を出たら、三千院の門前か参道でお昼に。11:30なら、開いたばかりで入りやすい時間です。食べたら参道を下り（約15分）、バス停の前で国道を渡らずに西へ、里の道を寂光院へ（約20分）。",
               "After Hosen-in, have lunch at Sanzen-in’s gate or on the lane. At 11:30 places have just opened and it’s easy to get a table. Then walk down the lane (about 15 minutes), and from the bus stop head west, without crossing the main road, along the valley lane to Jakko-in (about 20 minutes).")),
            ("jakkoin", VIS, "13:00〜13:45", "13:00–13:45",
             T("見終わったら、里の道をバス停へ戻って約20分。14:27発のバスに乗ります。",
               "Afterwards it’s about 20 minutes back along the lane to the bus stop for the 14:27 bus.")),
            ("kaeri", DEP, "大原 14:27発 → 出町柳駅前 15:01着・三条京阪前 15:10着。夜は18時ごろから", "Ohara 14:27 → Demachiyanagi-ekimae 15:01, Sanjo-Keihan-mae 15:10. Evening from about 18:00",
             T("14:27発に乗ると、三条京阪前に15:10に着きます。早起きした日なので、宿に戻ってひと休みを。まだ歩ける人は、手前の出町柳駅前（15:01着）で降りて、鴨川デルタと糺の森へ。晩ごはんは18時ごろから、三条・先斗町で。",
               "The 14:27 gets you to Sanjo-Keihan-mae at 15:10. After an early start, go back to your hotel for a rest. If you still have legs, get off earlier at Demachiyanagi-ekimae (15:01) for the Kamo delta and Tadasu-no-mori. Have dinner around Sanjo and Pontocho from about 18:00.")),
        ],
        sections=[dict(first="bus", last="sanzenin", day=0), dict(first="hosenin", last="otonashi", day=1),
                  dict(first="sato", last="jakkoin", day=2), dict(first="kaeri", last="kaeri", day=3)],
        focus=("bus", "jakkoin"),
        default=["sando", "sanzenin", "hosenin", "sato", "jakkoin"], auto=["bus", "kaeri"],
        extra_notices={"sanzenin": [notice("11月は8:45に開きます", "Opens at 8:45 in November",
                                           "平日は三条京阪前7:57発のバスで8:38に着くので、開いてすぐに入れます。土日祝は8:49着で、門に着くのは9時すぎです。",
                                           "On weekdays the 7:57 from Sanjo-Keihan-mae arrives at 8:38, so you can go in just after opening. On weekends and holidays it arrives at 8:49 and you reach the gate soon after 9:00.",
                                           frm="2026-11-01", to="2026-11-30")]},
        hints=[("sanzenin", dict(any=["sanzenin"], none=["jakkoin", "otonashi"]), None, None,
                "半日で回るなら、三千院と宝泉院（または実光院）だけで十分です。11:30にお昼を食べて、12時台のバス（12:27発など）で戻れます。",
                "For a half day, Sanzen-in plus Hosen-in (or Jikko-in) is enough. Have lunch at 11:30 and take a bus back in the 12:00 hour (the 12:27, for one)."),
               ("jikkoin", dict(any=["jikkoin"], andAny=["hosenin"]), None, None,
                "宝泉院と実光院は、どちらも座って庭を見るお寺です。お抹茶は宝泉院の拝観料についているので、実光院はお抹茶なし（600円）で入ると重なりません。",
                "Hosen-in and Jikko-in are both temples for sitting and looking at a garden. Matcha is included at Hosen-in, so take the plain ¥600 entry at Jikko-in."),
               ("jakkoin", dict(any=["jakkoin"], andAny=["otonashi"]), None, None,
                "音無の滝と寂光院の両方に行くと、三千院の奥から谷の反対側まで、合わせて1時間ほど歩きます。歩きやすい靴で。",
                "Doing both the falls and Jakko-in means about an hour of walking in total, from behind Sanzen-in to the far side of the valley. Wear comfortable shoes."),
               ("otonashi", dict(any=["otonashi"], none=["sanzenin"]), None, None,
                "音無の滝への道は、三千院の前の道の南の端から、川に沿って山のほうへ上ります。",
                "The path to the falls starts at the south end of the lane in front of Sanzen-in and follows the stream uphill.")]),
]

NOTE_HEAD = "京都 大原のルート（ohara/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（ohara.json＝9〜10時に出発、ohara-early.json＝三千院の開門に合わせる）。このファイル："
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（2024年11月18日の雨の夕方、iPhone と Nikon D7000。三千院の9枚目だけ2016年9月27日。横の写真だけ・長辺1600px・位置情報なし）。"
             "宝泉院・実光院・来迎院と音無の滝・里の道・寂光院と、三千院のわらべ地蔵はオーナーの写真がなく、Wikimedia Commons の写真（photos の要素が {file, credit}）。"
             "info.source は確認した出典、info.checked は確認日、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。このファイルは scripts/build_ohara_data.py で作る（直接直さない）。")


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    spots = []
    for sid, (lj, le), tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        if "_rows" in b:
            rows = b.pop("_rows")
            rows = (c["rows"] + rows) if sid == "bus" else rows
            b["info"] = info(rows, b.pop("_source"), tip=b.pop("_tip"))
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out["text"] = T(body["ja"] + "\n\n" + go["ja"] + f"\n\n{lj}：{tj}", body["en"] + "\n\n" + go["en"] + f"\n\n{le}: {te}")
        out["photos"] = PHOTOS[sid]
        for p in out["photos"]:
            f = p if isinstance(p, str) else p["file"]
            assert os.path.exists(f"{IMG}/{f}"), f
        out["notices"] = c.get("extra_notices", {}).get(sid, []) + out.get("notices", [])
        spots.append(out)
    auto = c["auto"]
    secs = [{"first": NO[s["first"]], "last": NO[s["last"]], "day": s["day"]} for s in c["sections"]]
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": secs,
        "focus": {"first": NO[c["focus"][0]], "last": NO[c["focus"][1]]},
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は時間割どおりに1日で回れる組み合わせ。それ以外は寄り道で、足したときの回り方は各スポットの文章と hints。大原バス停と帰りのバスは全員共通。",
                 "defaultMode": "pick",
                 "picks": [NO[x[0]] for x in order if x[0] not in auto],
                 "defaultPicks": [NO[i] for i in c["default"]],
                 "auto": {str(NO[i]): {"always": True} for i in auto},
                 "hints": [{"spot": NO[sid], "rule": rule(r), "from": frm, "to": to, "text": T(ja, en)} for sid, r, frm, to, ja, en in c["hints"]]},
        "photoBase": f"../images/{MAP_ID}/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


for c in COURSES:
    build(c)
