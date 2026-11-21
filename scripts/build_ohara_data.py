#!/usr/bin/env python3
"""京都 大原（三千院・宝泉院・実光院・音無の滝・寂光院）のデータ（data/routes/ohara.json）を書き出す。

使い方: python3 scripts/build_ohara_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/ohara/ にある。並べる順番は下の PHOTOS（自分の写真はファイル名だけ、
  ネットから借りた写真（Wikimedia Commons）は cc(...) で {"file", "credit": {"author", "license", "page"}} にする。
  ページでは写真の上に撮影者とライセンスが出る）
- オーナーの写真は 2024年11月18日（雨の日の夕方、iPhone と Nikon D7000）と 2016年9月27日（三千院の聚碧園の1枚）。
  宝泉院・実光院・来迎院と音無の滝・里の道・寂光院はオーナーの写真がない場所なので、文章にも行った日などは書かない
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/ohara"
OUT = f"{R}/data/routes/ohara.json"
CHECKED = "2026-11-21"


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def info(rows, tip=None, verified=True, cash=False):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED}
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
    "bus": own("bus", 3),
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

KBUS = link("timetable", "京都バス 時刻表", "Kyoto Bus timetables (Japanese)", "https://www.kyotobus.jp/route/timetable/")
PASS = link("info", "地下鉄・バス1日券（京都バス）", "Subway & Bus 1-day Pass (Kyoto Bus, Japanese)", "https://www.kyotobus.jp/route/fare/discount/pass/post-3.html")
HOSHO = link("info", "京都大原観光保勝会", "Kyoto Ohara tourist association (Japanese)", "https://kyoto-ohara-kankouhosyoukai.net/")
MOMIJI = "https://ja.kyoto.travel/flower/momiji/"
SEASON = {"from": None, "to": None, "url": MOMIJI,
          "head": T("紅葉は例年11月中旬〜下旬。写真は秋の雨の日", "Autumn leaves: usually mid to late November. The photos are from a rainy autumn day"),
          "text": T("大原は京都の町なかより気温が低く、紅葉は例年11月中旬〜下旬です（年によって前後します）。三千院のあじさいは6月中旬〜7月はじめ。冬は雪が積もる日があります。私の写真は2024年11月18日、雨の夕方に撮ったものです。晴れた日や、ほかの季節は見え方が違います。",
                    "Ohara is cooler than central Kyoto; the leaves usually peak from mid to late November (it shifts from year to year). Sanzen-in’s hydrangeas bloom from mid June into early July, and in winter there are days of snow. My photos were taken on a rainy late afternoon, 18 November 2024, so expect a different look in sunshine or in other seasons.")}

S = [
    dict(id="bus", name=T("大原バス停", "Ohara bus stop"), kind=T("バス停", "Bus stop"),
         blurb=T("京都駅前から京都バスで約1時間、国際会館駅前からは22分。三千院へは東へ、寂光院へは西へ歩きます。",
                 "About an hour from Kyoto Station by Kyoto Bus, or 22 minutes from Kokusaikaikan subway station. Sanzen-in is to the east, Jakko-in to the west."),
         lat=35.11975, lng=135.82898,
         text=T("大原（おおはら）バス停\n\n大原へ行く乗り物はバスだけです。行き方は2つあります。\n\n"
                "① 京都駅前（C3のりば）から京都バス17系統「大原」行きで約1時間・630円。乗り換えなし。四条河原町・三条京阪・出町柳駅前も通ります。平日は7:36発→8:38着、次は8:16発→9:27着。\n\n"
                "② 地下鉄烏丸線で国際会館駅へ（京都駅から約20分・290円）、駅前から京都バス19系統などで22分・400円。平日は8:36発→8:58着。道が混む秋の週末は、こちらのほうが時間が読めます。\n\n"
                "どちらも「地下鉄・バス1日券」（1,100円）で乗れます。京都駅からバスで往復すると1,260円なので、1日券のほうが安くなります。1日券は京都バスの車内では買えません。地下鉄の駅の券売機か、京都駅前の市バス・地下鉄案内所で先に買ってください。\n\n"
                "秋はバスが混みます。京都駅前は始発なので、発車の15分ほど前から並べば座れます。1時間乗るので、途中のバス停から立って乗るより、京都駅まで行って並ぶほうが楽です。\n\n"
                "三千院は9:00に開きます（11月は8:45）。団体が増えるのは10時ごろからなので、京都駅前7:36発に乗って、開いてすぐの三千院に入るのがおすすめです。\n\n"
                "帰りの大原発は、京都駅前行き（17系統）が毎時27分・57分ごろで、乗り換えなしで帰れる最後は17:27発です。そのあとは国際会館駅前行きが18:21・19:01・20:01・21:01発（21:01が最終）で、地下鉄に乗り換えます。帰りも大原が始発です。\n\n"
                "ICカードは、乗るときと降りるときの2回タッチします。バス停に京都バスの案内所があります。\n\nおすすめ訪問時間：8:40ごろに到着",
                "Ohara bus stop\n\nBuses are the only way to Ohara. There are two routes.\n\n"
                "1) Kyoto Bus 17 from Kyoto Station (stop C3), bound for Ohara: about an hour, ¥630, no change. It also stops at Shijo-Kawaramachi, Sanjo-Keihan and Demachiyanagi. On weekdays the 7:36 arrives at 8:38; the next is 8:16, arriving 9:27.\n\n"
                "2) Subway Karasuma line to Kokusaikaikan (about 20 min from Kyoto Station, ¥290), then Kyoto Bus 19 and others from outside the station: 22 min, ¥400. On weekdays the 8:36 arrives at 8:58. On autumn weekends, when the roads jam, this way keeps better time.\n\n"
                "Both are covered by the Subway & Bus 1-day Pass (¥1,100). The bus alone is ¥1,260 return from Kyoto Station, so the pass is cheaper. You can’t buy it on Kyoto Bus: get it beforehand from a subway ticket machine or the bus and subway information centre at Kyoto Station.\n\n"
                "The buses fill up in autumn. Kyoto Station is the first stop, so queue about 15 minutes before departure and you’ll get a seat. It’s an hour’s ride, so going to the station to queue beats standing from a stop along the way.\n\n"
                "Sanzen-in opens at 9:00 (8:45 in November). Tour groups build up from around 10:00, so take the 7:36 from Kyoto Station and walk in as the temple opens.\n\n"
                "Going back, bus 17 for Kyoto Station leaves Ohara at about :27 and :57 past each hour; the last one without a change is at 17:27. After that, buses run to Kokusaikaikan station at 18:21, 19:01, 20:01 and 21:01 (the last), where you change to the subway. Ohara is the first stop on the way back too.\n\n"
                "With an IC card, tap when you board and again when you get off. There is a Kyoto Bus information desk at the stop.\n\nRecommended visit time: arrive around 8:40"),
         gmaps=[gm("大原バス停", "Ohara bus stop", 35.11975, 135.82898, "大原バス停 京都バス 左京区")],
         links=[KBUS, PASS],
         notices=[SEASON],
         info=info([row("train", "京都駅前（C3のりば）→ 大原：京都バス17系統 約1時間・630円。平日 7:36→8:38、8:16→9:27、8:46→9:48／土曜 7:36→8:49、8:16→9:18",
                        "Kyoto Station (stop C3) → Ohara: Kyoto Bus 17, about 1 h, ¥630. Weekdays 7:36→8:38, 8:16→9:27, 8:46→9:48; Saturdays 7:36→8:49, 8:16→9:18"),
                    row("train", "国際会館駅前 → 大原：京都バス19系統など 22分・400円。平日 7:46、8:36、9:05、9:36、10:05発／土曜 8:27、8:46、9:40発。地下鉄は京都〜国際会館 約20分・290円",
                        "Kokusaikaikan-ekimae → Ohara: Kyoto Bus 19 and others, 22 min, ¥400. Weekdays 7:46, 8:36, 9:05, 9:36, 10:05; Saturdays 8:27, 8:46, 9:40. Subway Kyoto–Kokusaikaikan: about 20 min, ¥290"),
                    row("train", "帰り：大原 → 京都駅前（17系統）14:57、15:27、15:57、16:27、16:57、17:27発（最後）。大原 → 国際会館駅前は 平日15:07、15:42、16:07、16:42、17:07、17:47、18:21、19:01、20:01、21:01発（最終）",
                        "Back: Ohara → Kyoto Station (bus 17) at 14:57, 15:27, 15:57, 16:27, 16:57 and 17:27 (the last). Ohara → Kokusaikaikan-ekimae on weekdays at 15:07, 15:42, 16:07, 16:42, 17:07, 17:47, 18:21, 19:01, 20:01 and 21:01 (the last)"),
                    row("fee", "地下鉄・バス1日券 1,100円（大原バス停まで使えます。その先の小出石方面は別料金）", "Subway & Bus 1-day Pass ¥1,100 (valid as far as the Ohara stop; beyond it, towards Kodeishi, costs extra)")],
                   tip=T("バスの時刻と運賃は乗換案内（2026年11月24日（火）と28日（土）の時刻）で、1日券の範囲は京都バスの公式サイトの区間図（2026年3月20日現在）で確認しました。秋の週末は臨時の特急バス（国際会館駅前〜大原）が出る日があります。",
                         "Bus times and fares were checked on a route planner for Tuesday 24 and Saturday 28 November 2026; the pass area on Kyoto Bus’s official area map (as of 20 March 2026). On autumn weekends extra express buses sometimes run between Kokusaikaikan and Ohara."))),
    dict(id="sando", name=T("三千院の参道（呂川沿い）", "The lane to Sanzen-in"), kind=T("参道", "Approach"),
         blurb=T("バス停から三千院まで、小さな川に沿って上る約10分の道。しば漬の店や茶屋が並びます。",
                 "A ten-minute lane up beside a small stream from the bus stop to Sanzen-in, lined with pickle shops and teahouses."),
         lat=35.11995, lng=135.83150,
         text=T("三千院の参道（さんどう）\n\nバス停から国道の信号を渡って、呂川（ろせん）という小さな川に沿った道を上ります。三千院まで歩いて約10分。ゆるい上り坂です。\n\n"
                "道の両側に、しば漬の店、茶屋、みやげ物の店が並びます。しば漬は大原で生まれた漬物で、赤しそで漬けたなすやきゅうりです。老舗の「志ば久（しばきゅう）」は参道の途中にあります（9:00〜16:00、水曜休み）。\n\n"
                "朝は店がまだ開いていないことが多いので、行きはまっすぐ三千院へ。買い物とお昼は帰りにどうぞ。漬物は荷物になるので、買うのは最後がいいです。\n\n"
                "坂を上りきると石段があり、その上が三千院の前の道です（写真は2024年11月18日。石段のまわりのもみじが真っ赤でした）。雨の日は石畳がすべるので、歩きやすい靴で。\n\nおすすめ訪問時間：8:40〜8:55",
                "The lane to Sanzen-in\n\nFrom the bus stop, cross the main road at the lights and follow the lane up beside a small stream, the Rosen. It’s a gentle ten-minute climb to Sanzen-in.\n\n"
                "Both sides are lined with pickle shops, teahouses and souvenir stalls. Shibazuke, aubergine and cucumber pickled with red shiso, was born in Ohara. The long-established Shibakyu is partway up the lane (9:00–16:00, closed Wednesdays).\n\n"
                "Most shops aren’t open yet in the early morning, so go straight up to Sanzen-in and leave shopping and lunch for the way back. Pickles are heavy, so buy them last.\n\n"
                "At the top of the slope a flight of stone steps brings you out in front of Sanzen-in (my photos are from 18 November 2024, when the maples round the steps were deep red). The paving is slippery in rain: wear shoes with grip.\n\nRecommended visit time: 8:40–8:55"),
         gmaps=[gm("三千院の参道", "Lane to Sanzen-in", 35.11995, 135.83150, "志ば久 大原 京都")],
         links=[link("official", "志ば久 公式サイト", "Shibakyu (official, Japanese)", "https://www.shibakyu.jp/"), HOSHO],
         info=info([row("hours", "大原バス停から三千院まで歩いて約10分（三千院の案内）", "About 10 min on foot from the Ohara bus stop to Sanzen-in (temple’s access page)"),
                    row("hours", "志ば久（しば漬）9:00〜16:00", "Shibakyu (shibazuke pickles) 9:00–16:00"),
                    row("closed", "志ば久は水曜休み", "Shibakyu is closed on Wednesdays")],
                   tip=T("志ば久の時間と休みは公式サイトで確認しました。ほかの店の営業日と時間は店ごとに違います。", "Shibakyu’s hours and closing day were checked on its website. Other shops keep their own days and hours."))),
    dict(id="sanzenin", name=T("三千院", "Sanzen-in"), kind=T("寺", "Temple"),
         blurb=T("杉木立の下に苔が広がる庭と、国宝の阿弥陀三尊。大原でいちばんの見どころです。",
                 "A moss garden under tall cedars and a National Treasure Amida triad: the main sight of Ohara."),
         lat=35.11966, lng=135.83410,
         text=T("三千院（さんぜんいん）\n\n最澄が比叡山に建てたお堂に始まり、皇族が住職をつとめてきた門跡寺院です。明治のはじめに大原へ移りました。石垣の上の御殿門（ごてんもん）から入ります。\n\n"
                "順路は、客殿 → 宸殿 → 庭へ下りる、の順です。\n\n"
                "・聚碧園（しゅうへきえん）：客殿の縁側から座って眺める池の庭。赤い毛氈に座れます。\n"
                "・有清園（ゆうせいえん）：宸殿を出ると、杉とひのきの木立の下に苔が広がります。秋はもみじの赤と苔の緑が重なります（写真1枚目）。\n"
                "・往生極楽院（おうじょうごくらくいん）：苔の庭の奥の小さなお堂。国宝の阿弥陀三尊像がいます。両脇の菩薩が少し前かがみに座る「大和坐り」を、近くで見てください。\n"
                "・わらべ地蔵：往生極楽院の南、弁天池のそばの苔の中に、小さなお地蔵さまがいます。見落としやすいので、足もとを探してください（写真10枚目）。\n\n"
                "その先に、あじさい苑、金色不動堂、観音堂と続きます。奥まで歩いて1時間ほど。\n\n"
                "苔がいちばんきれいなのは雨の日と雨上がりです。私が行った2024年11月18日は雨で、夕方は人も少なく、苔ももみじも色が濃く見えました。写真9枚目は2016年9月の聚碧園で、夏から秋のはじめは緑一色です。\n\n"
                "あじさいは6月中旬から7月はじめ。冬は雪の日があり、閉まるのが16:30と早くなります。\n\nおすすめ訪問時間：9:00〜10:10",
                "Sanzen-in\n\nThe temple began as a hall built by Saicho on Mt. Hiei and was headed for centuries by members of the imperial family; it moved to Ohara in the early Meiji period. You enter through the Goten-mon gate, set in a high stone wall.\n\n"
                "The route runs: guest hall → Shinden hall → down into the garden.\n\n"
                "• Shuheki-en: a pond garden viewed sitting on the veranda of the guest hall, on the red felt.\n"
                "• Yusei-en: step out of the Shinden and moss spreads under tall cedars and cypresses. In autumn, red maples sit over the green (photo 1).\n"
                "• Ojo Gokuraku-in: a small hall at the back of the moss garden, housing the Amida triad, a National Treasure. Look closely at the two attendant bodhisattvas, kneeling and leaning slightly forward.\n"
                "• Warabe Jizo: small stone Jizo figures half-buried in the moss beside the Benten pond, south of the hall. They are easy to miss, so look down (photo 10).\n\n"
                "Beyond are the hydrangea garden, the Konjiki Fudo hall and the Kannon hall. Allow about an hour to walk to the far end.\n\n"
                "The moss is at its best in rain or just after. I went on a rainy 18 November 2024; late in the afternoon it was quiet, and the moss and maples looked their deepest. Photo 9 is Shuheki-en in September 2016: from summer to early autumn it is all green.\n\n"
                "Hydrangeas bloom from mid June into early July. In winter there are snowy days, and the temple closes earlier, at 16:30.\n\nRecommended visit time: 9:00–10:10"),
         gmaps=[gm("三千院", "Sanzen-in", 35.11966, 135.83410, "三千院 大原 京都")],
         links=[link("official", "三千院 公式サイト", "Sanzen-in (official)", "https://www.sanzenin.or.jp/", "https://www.sanzenin.or.jp/en"),
                link("info", "紅葉だより（京都観光Navi）", "Autumn-leaf report (Kyoto City, Japanese)", MOMIJI)],
         info=info([row("hours", "3〜10月 9:00〜17:00／11月 8:45〜16:45／12〜2月 9:00〜16:30", "Mar–Oct 9:00–17:00 / Nov 8:45–16:45 / Dec–Feb 9:00–16:30"),
                    row("closed", "休みなし", "Open every day"),
                    row("fee", "一般700円、中学生・高校生400円、小学生150円", "¥700; junior high and high school ¥400; elementary ¥150")],
                   tip=T("三千院の公式サイトで確認しました。あじさいの時期も公式サイトの案内です。", "Checked on the temple’s website, including the hydrangea season."), cash=True)),
    dict(id="hosenin", name=T("宝泉院と勝林院", "Hosen-in & Shorin-in"), kind=T("寺（額縁庭園）", "Temple (framed garden)"),
         blurb=T("柱と柱のあいだを額縁にして、竹林と樹齢700年の五葉松を眺める部屋。お抹茶がついています。",
                 "A room where the pillars frame a bamboo grove and a 700-year-old pine like pictures. Matcha is included."),
         lat=35.12135, lng=135.83400,
         text=T("宝泉院（ほうせんいん）と勝林院（しょうりんいん）\n\n三千院の門を出て左（北）へ歩いて約5分。道の突き当たりに勝林院の大きな本堂があり、その左手が宝泉院です。\n\n"
                "宝泉院は、客殿に座って庭を見るお寺です。柱と柱のあいだを額縁に見立てるので「額縁庭園」と呼ばれます。西側は竹林ごしに大原の里、南側は樹齢700年の五葉松（ごようのまつ）。拝観料にお抹茶とお菓子がついていて、座っていられる時間に決まりはありません。\n\n"
                "公式サイトのすすめは、畳に座って見ること。縁側まで出ずに、部屋の奥に座ると、柱と鴨居がちょうど額縁になります（写真1・2枚目）。\n\n"
                "廊下の天井は「血天井」です。関ヶ原の戦いの前に伏見城で自刃した鳥居元忠たちの床板を、供養のために天井に張ったものです。\n\n"
                "勝林院は1013年に開かれた、声明（しょうみょう＝お経に節をつけて唱える仏教音楽）の道場です。1186年に法然がここで念仏の教えを論じた「大原問答」で知られます。今の本堂は1778年の再建（写真5枚目は2024年11月18日の夕方、門の外から）。\n\n"
                "秋は宝泉院で夜の拝観があります（2025年は11月8日〜12月7日）。2026年の日程は公式サイトで確認してください。\n\nおすすめ訪問時間：10:20〜11:10",
                "Hosen-in and Shorin-in\n\nTurn left (north) out of Sanzen-in’s gate and walk about five minutes. The big hall at the end of the lane is Shorin-in; Hosen-in is to its left.\n\n"
                "Hosen-in is a temple where you sit in the guest hall and look at the garden. The pillars work as picture frames, so it is known as the “framed garden”: to the west, the Ohara valley through a bamboo grove; to the south, a 700-year-old five-needle pine. Matcha and a sweet come with the entry fee, and you may sit as long as you like.\n\n"
                "The temple’s advice is to view it sitting on the tatami. Stay back from the veranda, deep in the room, and the pillars and lintel become the frame (photos 1 and 2).\n\n"
                "The corridor has a “blood ceiling”: floorboards from Fushimi Castle, where Torii Mototada and his men took their own lives before the battle of Sekigahara, set into the ceiling as a memorial.\n\n"
                "Shorin-in, founded in 1013, is a training hall for shomyo, Buddhist chant. It is known for the Ohara Debate of 1186, when Honen argued the case for the nenbutsu here. The present hall dates from 1778 (photo 5: from outside the gate, late on 18 November 2024).\n\n"
                "Hosen-in opens in the evening in autumn (8 November–7 December in 2025). For the 2026 dates, check the official website.\n\nRecommended visit time: 10:20–11:10"),
         gmaps=[gm("宝泉院", "Hosen-in", 35.12135, 135.83400, "宝泉院 大原 京都"), gm("勝林院", "Shorin-in", 35.12122, 135.83454, "勝林院 大原 京都")],
         links=[link("official", "宝泉院 公式サイト", "Hosen-in (official, Japanese)", "http://www.hosenin.net/"),
                link("official", "勝林院 公式サイト", "Shorin-in (official, Japanese)", "https://www.shourinin.com/")],
         info=info([row("hours", "宝泉院 9:00〜17:00（受付は16:30まで）", "Hosen-in 9:00–17:00 (last entry 16:30)"),
                    row("fee", "宝泉院 大人1,000円（お抹茶・お菓子つき。2026年4月10日から）、中学生・高校生900円、小学生800円", "Hosen-in ¥1,000 including matcha and a sweet (since 10 April 2026); junior high and high school ¥900; elementary ¥800"),
                    row("closed", "宝泉院は行事で休む日があります（公式サイトのお知らせ）", "Hosen-in sometimes closes for temple events (see the news on its website)"),
                    row("fee", "勝林院の拝観料と時間は公式サイトに書かれていません（要確認）", "Shorin-in’s fee and hours aren’t given on its website (please check)")],
                   tip=T("宝泉院の公式サイトで確認しました。写真1〜4枚目は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。", "Checked on Hosen-in’s website. Photos 1–4 are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
    dict(id="jikkoin", name=T("実光院", "Jikko-in"), kind=T("寺（庭と山野草）", "Temple (garden)"),
         blurb=T("秋から春まで咲く「不断桜」のある小さなお寺。客殿から池の庭を眺め、庭へ下りて歩けます。",
                 "A small temple with a cherry that flowers from autumn to spring. View the pond garden from the hall, then walk down into it."),
         lat=35.12055, lng=135.83408,
         text=T("実光院（じっこういん）\n\n三千院と勝林院のあいだ、道の西側にあります。勝林院の子院です。\n\n"
                "庭は2つ。客殿の南の「契心園（けいしんえん）」は、座って眺める池の庭。西の「旧理覚院庭園」は下りて歩ける庭で、大原の山を借景にしています。約120種の山野草が植えられています。\n\n"
                "庭のまん中の「不断桜（ふだんざくら）」は、10月の中ごろから翌年の4月ごろまで咲きます。秋は桜ともみじ、冬は桜と雪がいっしょに見られます。\n\n"
                "宝泉院と似た「座って庭を見るお寺」ですが、こちらは人が少なく、庭を歩けます。時間がない日は、宝泉院か実光院のどちらか1つで十分です。お抹茶つきの拝観もあります。\n\n"
                "閉まるのが15:30と早いので、寂光院より先に行ってください。\n\nおすすめ訪問時間：11:15〜11:45",
                "Jikko-in\n\nOn the west side of the lane between Sanzen-in and Shorin-in, of which it is a sub-temple.\n\n"
                "There are two gardens. Keishin-en, south of the guest hall, is a pond garden to view sitting down. The former Rikaku-in garden to the west is one you walk through, with the Ohara hills as borrowed scenery and about 120 kinds of wild flowers.\n\n"
                "The “fudan-zakura” cherry in the middle of the garden flowers from mid October to around April: cherry blossom with maples in autumn, with snow in winter.\n\n"
                "Like Hosen-in, this is a temple for sitting and looking at a garden, but it is quieter and you can walk in the garden. If you are short of time, one of the two is enough. Entry with matcha is available.\n\n"
                "It closes early, at 15:30, so come here before Jakko-in.\n\nRecommended visit time: 11:15–11:45"),
         gmaps=[gm("実光院", "Jikko-in", 35.12055, 135.83408, "実光院 大原 京都")],
         links=[link("official", "実光院 公式サイト", "Jikko-in (official)", "https://jikkoin.com/", "https://jikkoin.com/english/")],
         info=info([row("hours", "9:30〜15:30（季節で変わることがあります）。見学は約20分", "9:30–15:30 (may change with the season). Allow about 20 minutes"),
                    row("closed", "休みなし", "Open every day"),
                    row("fee", "中学生以上600円、小学生以下300円。お抹茶・お菓子つきは1,100円", "¥600 (junior high and up), ¥300 children; ¥1,100 with matcha and a sweet")],
                   tip=T("実光院の公式サイトで確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。", "Checked on the temple’s website. Photos are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
    dict(id="otonashi", name=T("来迎院と音無の滝", "Raigo-in & Otonashi falls"), kind=T("寺・滝（山道）", "Temple & waterfall"),
         blurb=T("三千院の奥の山道を歩いて、杉木立の中の来迎院と、声明の伝説が残る滝へ。往復で40〜50分。",
                 "A path into the hills behind Sanzen-in, to Raigo-in among the cedars and a waterfall with a legend of Buddhist chant. 40–50 minutes return."),
         lat=35.12062, lng=135.83974,
         text=T("来迎院（らいごういん）と音無の滝（おとなしのたき）\n\n三千院の前の道を南の端まで戻り、呂川に沿って山のほうへ上ります。来迎院まで約300m、歩いて5〜10分。そこから山道をさらに約400m、10分ほどで音無の滝です。\n\n"
                "来迎院は、平安時代の終わりに良忍（りょうにん）が声明の道場として開いたお寺です。三千院のにぎわいがうそのように静かです。\n\n"
                "音無の滝は、岩の上を水がすべり落ちる滝です。良忍がここで声明の稽古をしていると、声と滝の音がひとつになって、滝の音が聞こえなくなった、と伝わります。\n\n"
                "来迎院までは舗装された坂道、その先は土の山道です。雨のあとはぬかるむので、すべりにくい靴で。滝までの道に店やトイレはありません。夕方は暗くなるのが早いので、明るいうちに戻ってください。\n\n"
                "半日しかない日や、歩くのを減らしたい日は、ここを外してください。\n\nおすすめ訪問時間：11:55〜12:45",
                "Raigo-in and Otonashi falls\n\nGo back to the south end of the lane in front of Sanzen-in and follow the Rosen stream uphill. Raigo-in is about 300 m on, 5–10 minutes; the falls are another 400 m or so along a hill path, about 10 minutes.\n\n"
                "Raigo-in was founded at the end of the Heian period by the monk Ryonin as a training hall for shomyo chant. After the bustle of Sanzen-in it is strikingly quiet.\n\n"
                "At Otonashi-no-taki, the “soundless waterfall”, water slides down a rock face. The story goes that when Ryonin practised chanting here, his voice and the falls became one and the sound of the water could no longer be heard.\n\n"
                "The way is a paved slope as far as Raigo-in, then an earth path. It gets muddy after rain, so wear shoes with grip. There are no shops or toilets on the way. It gets dark early in the hills: be back while it’s light.\n\n"
                "With only half a day, or to cut down on walking, leave this one out.\n\nRecommended visit time: 11:55–12:45"),
         gmaps=[gm("音無の滝", "Otonashi falls", 35.12062, 135.83974, "音無の滝 大原 京都"), gm("来迎院", "Raigo-in", 35.11861, 135.83767, "来迎院 大原 京都")],
         links=[HOSHO],
         info=info([row("hours", "音無の滝は自由に見られます（山道。明るい時間に）", "The falls are free to visit (a hill path; go in daylight)"),
                    row("fee", "来迎院の拝観料は400円、時間は9:00〜17:00と紹介されていますが、公式サイトがなく確認できていません（要確認）", "Raigo-in is listed at ¥400, 9:00–17:00, but it has no official website and this could not be confirmed (please check)")],
                   tip=T("滝の位置と道の距離は OpenStreetMap で測った目安です。来迎院の料金と時間は観光サイトの情報で、公式には確認できていません。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "The position of the falls and the distances are estimates from OpenStreetMap. Raigo-in’s fee and hours come from travel sites and could not be confirmed officially. Photos are from Wikimedia Commons (author and license shown on each photo)."),
                   verified=False)),
    dict(id="sato", name=T("お昼と、大原の里の道", "Lunch & the valley walk"), kind=T("里の道", "Village walk"),
         blurb=T("参道でお昼を食べてから、川を渡り、田んぼと畑のあいだの道を寂光院へ。バス停から歩いて約15分。",
                 "Lunch on the lane, then across the river and through fields to Jakko-in: about 15 minutes’ walk from the bus stop."),
         lat=35.12160, lng=135.82520,
         text=T("お昼と、大原の里（さと）の道\n\nお昼は、三千院の参道へ戻って食べるのが便利です。参道とバス停のまわりに、そば・うどん、定食、ゆば料理、甘味の店があります。秋の12時台は並ぶ店が多いので、11時半までに入るか、13時を過ぎてからに。店の営業日と時間は店ごとに違うので、行きたい店があれば先に調べてください（大原観光保勝会のサイトに店の一覧があります）。\n\n"
                "寂光院は、谷の反対側にあります。バス停から国道を渡らずに西へ下り、高野川（たかのがわ）を渡って、案内板にしたがって歩きます。約15分。三千院の前からだと30分ほどです。\n\n"
                "道の両側は田んぼと畑で、しば漬に使う赤しその畑もあります（赤しそは夏）。三千院のあたりより人が少なく、山に囲まれた大原の里がよく見えます。\n\n"
                "畑や家の敷地には入らないでください。車も通る細い道なので、道の端を歩きましょう。\n\nおすすめ訪問時間：13:00〜14:15",
                "Lunch and the valley walk\n\nFor lunch, the handiest place is back down the lane from Sanzen-in. Along it and around the bus stop are soba and udon shops, set-meal restaurants, yuba (tofu skin) dishes and sweet shops. In autumn many have queues between 12:00 and 13:00, so sit down before 11:30 or after 13:00. Opening days and hours differ from shop to shop: if you have one in mind, check first (the Ohara tourist association’s website lists them).\n\n"
                "Jakko-in is on the other side of the valley. From the bus stop, without crossing the main road, head downhill to the west, cross the Takano river and follow the signs: about 15 minutes. From Sanzen-in’s gate it is about 30.\n\n"
                "The lane runs between rice fields and vegetable plots, some growing the red shiso used for shibazuke (in summer). There are fewer people than around Sanzen-in, and you get the open view of the valley ringed by hills.\n\n"
                "Please keep out of the fields and private yards. Cars use this narrow lane too, so walk at the side.\n\nRecommended visit time: 13:00–14:15"),
         gmaps=[gm("大原バス停から寂光院への道", "Lane from the bus stop to Jakko-in", 35.12160, 135.82520, "寂光院 大原 京都")],
         links=[link("info", "大原観光保勝会「食べる」", "Ohara tourist association: places to eat (Japanese)", "https://kyoto-ohara-kankouhosyoukai.net/eat/")],
         info=info([row("hours", "大原バス停から寂光院まで歩いて約15分（寂光院の案内）", "About 15 min on foot from the Ohara bus stop to Jakko-in (temple’s access page)")],
                   tip=T("歩く時間は寂光院の公式サイトの案内です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。", "The walking time is from Jakko-in’s website. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="jakkoin", name=T("寂光院", "Jakko-in"), kind=T("尼寺（平家物語）", "Nunnery (Tale of the Heike)"),
         blurb=T("平家が滅びたあと、建礼門院が余生を送った尼寺。『平家物語』の最後の場面の舞台です。",
                 "The nunnery where Kenreimon-in lived out her days after the fall of the Heike: the setting of the last chapter of the Tale of the Heike."),
         lat=35.12406, lng=135.82082,
         text=T("寂光院（じゃっこういん）\n\n聖徳太子が594年に建てたと伝わる、天台宗の尼寺です。石段を上った先に、小さな本堂と池の庭があります。\n\n"
                "建礼門院（けんれいもんいん）は平清盛の娘で、安徳天皇の母です。1185年、壇ノ浦で平家が滅び、幼い天皇も海に沈みました。ひとり助けられた女院は、その年の秋にここへ入り、一門と我が子を弔って暮らしました。翌年の春、後白河法皇が訪ねてくる場面が『平家物語』の終わりの「大原御幸（おおはらごこう）」です。\n\n"
                "本堂の前の汀の池（みぎわのいけ）と桜は、その場面に出てくるものです。本堂の北の奥に、女院の庵のあとが残っています。\n\n"
                "本堂は2000年5月の火災で焼け、2005年に元の姿で建て直されました。今の本尊の地蔵菩薩像もそのときに作られたもので、色があざやかです。焼けた旧本尊は収蔵庫にあり、特別公開の日だけ見られます。\n\n"
                "三千院より小さく、人も少ないお寺です。石段のもみじは秋がきれいです。客殿でお抹茶もいただけます。\n\n"
                "帰りは大原バス停まで歩いて約15分。15:10に出れば、15:27発の京都駅前行きに間に合います。\n\nおすすめ訪問時間：14:20〜15:10",
                "Jakko-in\n\nA Tendai nunnery said to have been founded by Prince Shotoku in 594. Up a flight of stone steps are a small main hall and a pond garden.\n\n"
                "Kenreimon-in was the daughter of Taira no Kiyomori and mother of the child emperor Antoku. In 1185 the Heike were destroyed at Dan-no-ura and the emperor was lost to the sea. She alone was pulled from the water, and that autumn she came here to pray for her clan and her son for the rest of her life. The visit paid to her the next spring by the retired emperor Go-Shirakawa is the closing chapter of the Tale of the Heike.\n\n"
                "The pond and the cherry tree in front of the main hall appear in that scene. Behind the hall to the north is the site of her hermitage.\n\n"
                "The main hall burned down in May 2000 and was rebuilt as it had been in 2005. The present Jizo statue was made then too, and its colours are bright. The fire-damaged original is kept in a storehouse and shown only on special opening days.\n\n"
                "It is smaller and quieter than Sanzen-in. The maples over the stone steps are good in autumn, and you can have matcha in the guest hall.\n\n"
                "It’s about 15 minutes’ walk back to the Ohara bus stop. Leave by 15:10 for the 15:27 bus to Kyoto Station.\n\nRecommended visit time: 14:20–15:10"),
         gmaps=[gm("寂光院", "Jakko-in", 35.12406, 135.82082, "寂光院 大原 京都")],
         links=[link("official", "寂光院 公式サイト", "Jakko-in (official)", "https://www.jakkoin.jp/", "https://www.jakkoin.jp/en/"), KBUS],
         info=info([row("hours", "3〜11月 9:00〜17:00／12月と1月4日〜2月 9:00〜16:30／1月1〜3日 10:00〜16:00", "Mar–Nov 9:00–17:00 / Dec and 4 Jan–Feb 9:00–16:30 / 1–3 Jan 10:00–16:00"),
                    row("fee", "大人・高校生600円、中学生350円、小学生100円", "¥600 (adults and high school); junior high ¥350; elementary ¥100"),
                    row("train", "帰り：大原 → 京都駅前（17系統）15:27、15:57、16:27、16:57、17:27発（最後）。そのあとは国際会館駅前行き（18:21、19:01、20:01、21:01発）と地下鉄で",
                        "Back: Ohara → Kyoto Station (bus 17) at 15:27, 15:57, 16:27, 16:57 and 17:27 (the last). After that, take a bus to Kokusaikaikan station (18:21, 19:01, 20:01, 21:01) and the subway")],
                   tip=T("寂光院の公式サイトと、乗換案内（2026年11月24日・28日の時刻）で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the temple’s website and a route planner (times for 24 and 28 November 2026). Photos are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = PHOTOS[out["id"]]
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    out.setdefault("notices", [])
    spots.append(out)
NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}

data = {
    "id": "ohara",
    "_note": "京都 大原のルート（ohara/ のページ専用。形は eizan-line.json と同じ）。京都バスで大原へ、参道→三千院→宝泉院・勝林院→実光院→来迎院・音無の滝→（お昼・里の道）→寂光院→大原バス停。"
             "写真は Toshi の写真ライブラリから選んだもの（2024年11月18日の雨の夕方、iPhone と Nikon D7000。三千院の9枚目だけ2016年9月27日。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "宝泉院・実光院・来迎院と音無の滝・里の道・寂光院と、三千院のわらべ地蔵はオーナーの写真がなく、Wikimedia Commons の写真（photos の要素が {file, credit}。ライセンスは Commons の API で2026年11月21日に確認）。"
             "info.checked は事実情報を確認した日（各寺と京都バスの公式サイト、乗換案内）。来迎院の料金・時間と勝林院の料金は公式に確認できず要確認。このファイルは scripts/build_ohara_data.py で作る。",
    "sections": [{"first": 1, "last": 3, "day": 0}, {"first": 4, "last": 6, "day": 1}, {"first": 7, "last": 8, "day": 2}],
    "focus": {"first": 1, "last": 8},
    "plan": {"_note": "「選んで回る」の設定。大原バス停は必ず入る。ほかは全部選べる。",
             "picks": [NO[k] for k in ("sando", "sanzenin", "hosenin", "jikkoin", "otonashi", "sato", "jakkoin")],
             "auto": {str(NO["bus"]): {"always": True}},
             "hints": [
                 H("sanzenin", {"any": [NO["sanzenin"]], "none": [NO["jakkoin"], NO["otonashi"]]},
                   "半日で回るなら、三千院と宝泉院（または実光院）だけで十分です。朝いちばんに着けば、お昼には大原を出られます。大原発の京都駅前行きは毎時27分・57分ごろです。",
                   "For a half day, Sanzen-in plus Hosen-in (or Jikko-in) is enough. Arrive first thing and you can leave Ohara by lunchtime; buses for Kyoto Station leave at about :27 and :57 past each hour."),
                 H("jikkoin", {"any": [NO["jikkoin"]], "andAny": [NO["hosenin"]]},
                   "宝泉院と実光院は、どちらも座って庭を見るお寺です。お抹茶は宝泉院の拝観料についているので、実光院はお抹茶なし（600円）で入ると重なりません。",
                   "Hosen-in and Jikko-in are both temples for sitting and looking at a garden. Matcha is included at Hosen-in, so take the plain ¥600 entry at Jikko-in."),
                 H("jakkoin", {"any": [NO["jakkoin"]], "none": [NO["sanzenin"], NO["hosenin"], NO["jikkoin"], NO["otonashi"]]},
                   "寂光院だけに行く日は、バス停から国道を渡らずに西へ。歩いて約15分です。",
                   "Going to Jakko-in only? From the bus stop head west without crossing the main road: about 15 minutes on foot."),
                 H("jakkoin", {"any": [NO["jakkoin"]], "andAny": [NO["otonashi"]]},
                   "音無の滝と寂光院の両方に行くと、三千院の前から谷の反対側まで、合わせて1時間ほど歩きます。歩きやすい靴で。",
                   "Doing both the falls and Jakko-in means about an hour of walking in total, from behind Sanzen-in to the far side of the valley. Wear comfortable shoes."),
                 H("otonashi", {"any": [NO["otonashi"]], "none": [NO["sanzenin"]]},
                   "音無の滝への道は、三千院の前の道の南の端から、川に沿って山のほうへ上ります。",
                   "The path to the falls starts at the south end of the lane in front of Sanzen-in and follows the stream uphill."),
             ]},
    "photoBase": "../images/ohara/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
