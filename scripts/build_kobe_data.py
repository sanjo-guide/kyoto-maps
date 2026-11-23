#!/usr/bin/env python3
"""神戸（大阪の梅田〜難波のホテルから1日）のデータ（data/routes/kobe.json）を書き出す。

使い方: python3 scripts/build_kobe_data.py   （そのあと python3 scripts/sync_kobe.py）
- 起点は大阪の梅田〜難波のあたりのホテル（2026-11-22 オーナーの指示）。京都から来る人・帰る人の電車は補足として書く
- コースは1つ（9:30に大阪梅田を出る時間割）。神戸には「開く時間に並ばないと入れない」場所がなく、
  北野の異人館は午前のうちに回る順にしたので、早朝コースは作っていない
- 回る順：神戸三宮 → 北野坂を上る → 北野天満神社 → 北野異人館街 → 三宮でお昼（かつ丼 七兵衛）→ 地下鉄で新神戸・布引の滝
  → 南京町 → メリケンパークで日の入り → ポートタワー → 夜のハーバーランド（モザイク）で晩ごはん → 21時ごろの電車で大阪へ
  （2026-11-20 の最初の版は 滝→北野→お昼13:40→港→17時に帰る、だった。お昼が遅く売り切れの心配があったので、
    北野を先、12時すぎにお昼、午後に滝、の順に入れ替えた。番号が変わったので保存キーも変えてある＝sync_kobe.py）
- 時間割は11月下旬（日の入り16:50ごろ）の土曜のダイヤで組んだ。阪急・阪神・JR・地下鉄の時刻と運賃は
  乗換案内（Yahoo!路線情報、2026-11-28 土曜。行きは 11-26 木曜も）で確認
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/kobe/<スポットのid>-<番号>.jpg を番号の順に全部使う（南京町・ハーバーランドの写真はまだないので、
  6番のスポットの文章と Googleマップのリンクで案内している）
- 店名を出しているのは、Toshi が食べた かつ丼 七兵衛 と、公式サイトで営業時間を確かめた店（老祥記・にしむら珈琲店）だけ
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kobe"
OUT = f"{R}/data/routes/kobe.json"
CHECKED = "2026-11-22"
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


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(hja, hen, ja, en, to=None, url=None):
    d = {"head": T(hja, hen), "text": T(ja, en), "from": None, "to": to}
    if url:
        d["url"] = url
    return d


def info(rows, tip=None, verified=True, source=None):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED, "source": source or []}
    if not verified:
        d["verified"] = False
    return d


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


PLANNER = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
SRC_PLANNER = "乗換案内（Yahoo!路線情報）2026-11-28（土）のダイヤ。行きは 11-26（木）も"
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月28日・土曜のダイヤ）で確認しました。平日は数分ずれます。乗る前にもう一度確かめてください。",
              "Times and fares checked on a route planner (Saturday 28 November 2026 timetable). Weekday trains differ by a few minutes; please check again before you travel.")
MOUNTAIN = "https://www.city.kobe.lg.jp/a17526/kanko/leisure/mountain/index.html"
HERB = "https://www.kobeherb.com/infomation/hours_fare/"
HERB_XMAS = "https://www.kobeherb.com/wordpress/wp-content/uploads/2026/10/88c4a0e9134729b7d5970905bd992b92.pdf"
LUMI_TICKET = "https://kobe-luminarie.jp/ticket/"
CITYHALL = "https://www.city.kobe.lg.jp/a28956/shise/about/building/index.html"

S = [
    # 1 ---------------------------------------------------------------------
    dict(id="sannomiya", name=T("神戸三宮駅（阪急・阪神・JR三ノ宮）", "Kobe-Sannomiya Station (Hankyu, Hanshin, JR)"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("大阪梅田から阪急の特急で27分・330円。難波からは阪神なんば線で乗り換えなし。着いたら山のほうへ、北野坂を上ります。",
                 "27 minutes and ¥330 from Osaka-Umeda by Hankyu limited express; direct from Namba on the Hanshin Namba Line. From the station, head uphill along Kitano-zaka."),
         lat=34.69486, lng=135.19509,
         text=T("神戸三宮（こうべさんのみや）\n\n"
                "梅田のあたりに泊まっているなら、阪急の特急が楽です。大阪梅田9:30発→神戸三宮9:57着、330円。10分おきに出ていて、始発駅なので1本見送れば座りやすいです。"
                "阪神の直通特急（大阪梅田9:40発→10:11着・330円）、JRの新快速（大阪9:45発→三ノ宮10:06着・420円）でもかまいません。3つの駅は隣り合っています。\n\n"
                "難波のあたりからは、阪神なんば線の快速急行が乗り換えなし。大阪難波9:37発→神戸三宮10:18着、420円。このマップの時間より20分ほど後ろにずれますが、同じ順で回れます。\n\n"
                "京都から来る人は、阪急の京都河原町8:46発→十三（じゅうそう）で乗り換え→神戸三宮10:07着・640円。JRなら京都9:00発の新快速で三ノ宮9:51着・1,110円、乗り換えなしです。\n\n"
                "神戸の街は、北が山、南が海。道案内も「山側」「海側」と書いてあります。迷ったら坂を上れば北野、下れば港です。写真は雨の日の阪急神戸三宮駅。\n\n"
                "おすすめ到着時間：9:57",
                "Kobe-Sannomiya\n\n"
                "From a hotel around Umeda, the Hankyu limited express is the easy choice: Osaka-Umeda 9:30 → Kobe-Sannomiya 9:57, ¥330. It runs every 10 minutes and starts at Umeda, so letting one go usually gets you a seat. "
                "The Hanshin limited express (Osaka-Umeda 9:40 → 10:11, ¥330) or the JR Special Rapid (Osaka 9:45 → Sannomiya 10:06, ¥420) work just as well; the three stations stand side by side.\n\n"
                "From around Namba, the Hanshin Namba Line rapid express runs direct: Osaka-Namba 9:37 → Kobe-Sannomiya 10:18, ¥420. You will be about 20 minutes behind the times on this map, but the order stays the same.\n\n"
                "Coming from Kyoto: Hankyu from Kyoto-Kawaramachi at 8:46, change at Juso, Kobe-Sannomiya 10:07, ¥640. Or the JR Special Rapid leaving Kyoto at 9:00, direct to Sannomiya at 9:51, ¥1,110.\n\n"
                "In Kobe, north is the mountains and south is the sea, and street signs say “mountain side” and “sea side”. If in doubt, uphill leads to Kitano and downhill to the port. The photo is Hankyu Kobe-Sannomiya Station on a rainy day.\n\n"
                "Recommended arrival: 9:57"),
         gmaps=[gm("阪急 神戸三宮駅", "Hankyu Kobe-Sannomiya Station", 34.69330, 135.19270, "阪急 神戸三宮駅"), gm("JR三ノ宮駅", "JR Sannomiya Station", 34.69486, 135.19509, "JR三ノ宮駅")],
         links=[PLANNER],
         info=info([row("train", "梅田から：大阪梅田9:30発（阪急の特急・10分おき）→ 神戸三宮9:57着・330円。阪神の直通特急も330円、JRの新快速（大阪→三ノ宮21分）は420円",
                        "From Umeda: Osaka-Umeda 9:30 (Hankyu limited express, every 10 min) → Kobe-Sannomiya 9:57, ¥330. Hanshin limited express also ¥330; JR Special Rapid (Osaka → Sannomiya, 21 min) ¥420"),
                    row("train", "難波から：大阪難波9:37発（阪神なんば線の快速急行）→ 神戸三宮10:18着・420円、乗り換えなし",
                        "From Namba: Osaka-Namba 9:37 (Hanshin Namba Line rapid express) → Kobe-Sannomiya 10:18, ¥420, direct"),
                    row("train", "京都から：京都河原町8:46発（阪急）→ 十三で乗り換え → 神戸三宮10:07着・640円。JRは京都9:00発の新快速 → 三ノ宮9:51着・1,110円",
                        "From Kyoto: Kyoto-Kawaramachi 8:46 (Hankyu) → change at Juso → Kobe-Sannomiya 10:07, ¥640. JR: Special Rapid from Kyoto 9:00 → Sannomiya 9:51, ¥1,110"),
                    row("train", "帰りの最後：大阪へはJR三ノ宮0:10発の各駅停車（大阪0:46着）。難波へは阪神の神戸三宮23:17発（尼崎で乗り換え、大阪難波0:02着）。京都へは阪急23:10発（十三で乗り換え、京都河原町0:34着）かJR新快速23:36発（京都0:30着）",
                        "Last trains back: to Osaka, the JR local leaving Sannomiya at 0:10 (Osaka 0:46). To Namba, Hanshin from Kobe-Sannomiya at 23:17 (change at Amagasaki, Osaka-Namba 0:02). To Kyoto, Hankyu at 23:10 (change at Juso, Kyoto-Kawaramachi 0:34) or the JR Special Rapid at 23:36 (Kyoto 0:30)")],
                   tip=TRAIN_TIP, source=[SRC_PLANNER])),
    # 2 ---------------------------------------------------------------------
    dict(id="tenman", name=T("北野天満神社", "Kitano Tenman Shrine"), kind=T("神社・見晴らし", "Shrine & viewpoint"),
         blurb=T("異人館街のいちばん上。石段を上ると、風見鶏の館の塔と神戸の街、その先の海まで見下ろせます。北野は、まずここから。",
                 "At the very top of the foreign-residence district. Climb the stone steps and you look down on the Weathercock House tower, the city and the sea. Start Kitano here."),
         lat=34.70189, lng=135.18956,
         text=T("北野天満神社（きたのてんまんじんじゃ）\n\n"
                "三宮の駅から北野坂をまっすぐ上って20〜25分。ゆるい上りがずっと続くので、急がずに。坂の途中の「北野坂にしむら珈琲店」は1階の喫茶が10:00から開いていて、ひと息つけます。\n\n"
                "坂を上りきった北野町広場の奥、風見鶏の館の東隣に鳥居があります。石段を上った先が、菅原道真（すがわらのみちざね）をまつる神社。"
                "境内に立つと、すぐ下に風見鶏の館のとがった塔、その向こうに神戸の街と海が見えます。異人館に入る前にここへ上ると、これから歩く町の形が分かります。\n\n"
                "門が開いているのは7:30から17:00までです。\n\n"
                "おすすめ訪問時間：10:25〜10:45",
                "Kitano Tenman Shrine\n\n"
                "From Sannomiya, walk straight up Kitano-zaka for 20–25 minutes. It is a gentle climb all the way, so take it slowly. Halfway up, Kitano-zaka Nishimura Coffee opens its ground-floor café at 10:00 if you want a pause.\n\n"
                "At the top of the slope, behind Kitano-cho Square and just east of the Weathercock House, there is a torii gate. The stone steps lead up to a shrine honouring Sugawara no Michizane. "
                "From the grounds you look down on the pointed tower of the Weathercock House, with the city and the sea beyond. Come up here before the houses and you can see the shape of the streets you are about to walk.\n\n"
                "The gates are open from 7:30 to 17:00.\n\n"
                "Recommended visit time: 10:25–10:45"),
         gmaps=[gm("北野天満神社", "Kitano Tenman Shrine", 34.70189, 135.18956, "北野天満神社 神戸")],
         links=[link("official", "北野天満神社 公式サイト", "Kitano Tenman Shrine (official, Japanese)", "https://www.kobe-kitano.net/"),
                link("official", "北野坂にしむら珈琲店（公式）", "Kitano-zaka Nishimura Coffee (official, Japanese)", "https://kobe-nishimura.jp/shop/kitanozaka.html")],
         info=info([row("hours", "7:30〜17:00（開門・閉門）", "7:30–17:00 (gates open and close)"),
                    row("hours", "三宮の駅から歩いて約20分（公式サイトの案内）。新神戸駅からは約15分", "About 20 minutes on foot from the Sannomiya stations (per the official site); about 15 from Shin-Kobe Station"),
                    row("hours", "北野坂にしむら珈琲店：1階の喫茶 10:00〜22:00。毎月最終月曜休み（例外あり）", "Kitano-zaka Nishimura Coffee: ground-floor café 10:00–22:00; closed last Monday of the month (with exceptions)")],
                   tip=T("神社と、にしむら珈琲店の公式サイトで確認しました。", "Checked on the shrine’s and Nishimura Coffee’s official websites."),
                   source=["北野天満神社 公式サイト https://www.kobe-kitano.net/", "にしむら珈琲店 公式サイト https://kobe-nishimura.jp/shop/kitanozaka.html"])),
    # 3 ---------------------------------------------------------------------
    dict(id="ijinkan", name=T("北野異人館街", "Kitano foreign residences"), kind=T("町並み・洋館", "Historic houses"),
         caution=T("館ごとに入館料。風見鶏の館は毎月第3火曜が休み", "Each house charges admission. Weathercock House closed 3rd Tuesday"),
         blurb=T("明治・大正の外国人の住まいが残る坂の町。館ごとに入館料がかかるので、入るのは2〜3館にしぼります。",
                 "Hillside lanes of Meiji- and Taisho-era foreigners’ homes. Every house charges admission, so pick two or three to go inside."),
         lat=34.70139, lng=135.18951,
         notices=[notice("入る館を先に決めておく", "Decide which houses before you go",
                         "館ごとに入館料がかかり、全部入ると5,000円を超えます。風見鶏の館と萌黄の館は2館で800円。うろこの家は1,100円、英国館は880円、洋館長屋と山手八番館は各550円です。"
                         "風見鶏の館は毎月第3火曜（祝日なら翌日）が休み。外から眺めて歩くだけなら、お金はかかりません。",
                         "Each house charges its own admission, and entering them all costs over ¥5,000. The Weathercock House and Moegi House are ¥800 for the pair; the Scale House is ¥1,100, the English House ¥880, the row houses and Yamate Hachibankan ¥550 each. "
                         "The Weathercock House is closed on the third Tuesday of each month (the next day if that is a holiday). Just walking the lanes and looking from outside costs nothing.")],
         text=T("北野異人館街（きたのいじんかんがい）\n\n"
                "北野天満神社の石段を下りると北野町広場で、風見鶏の館は目の前です。\n\n"
                "神戸港が開かれたあと、外国人が住んだ洋館が今も残る坂の町。"
                "屋根に風見鶏がのる赤レンガの「風見鶏の館」と、隣の淡い緑の「萌黄（もえぎ）の館」は、どちらも国の重要文化財で、2館で800円の共通券があります。迷ったらこの2つに入れば十分で、中を見て1時間ほど。\n\n"
                "広場のまわりには、英国館、洋館長屋、山手八番館、うろこの家など、ほかにも入れる館があります。うろこの家は広場からさらに急な坂を上った上です。\n\n"
                "見終わったら北野坂を下って三宮へ。下りは15〜20分です。\n\n"
                "おすすめ訪問時間：10:45〜12:00",
                "Kitano foreign residences\n\n"
                "Come down the steps from Kitano Tenman Shrine and you are in Kitano-cho Square, with the Weathercock House right in front of you.\n\n"
                "After the port of Kobe opened, foreign residents built homes on these slopes, and many survive. "
                "The red-brick Weathercock House with its weathervane and the pale-green Moegi House next door are both Important Cultural Properties, with a combined ticket for ¥800. If you can’t decide, these two are enough: allow about an hour inside.\n\n"
                "Around the square there are more houses you can enter: the English House, the Western-style row houses, Yamate Hachibankan, the Scale House and others. The Scale House is further up a steep lane above the square.\n\n"
                "Afterwards, walk back down Kitano-zaka to Sannomiya, 15–20 minutes downhill.\n\n"
                "Recommended visit time: 10:45–12:00"),
         gmaps=[gm("風見鶏の館", "Weathercock House", 34.70139, 135.18951, "風見鶏の館"), gm("萌黄の館", "Moegi House", 34.70100, 135.18925, "萌黄の館")],
         links=[link("official", "風見鶏の館 公式サイト", "Weathercock House (official, Japanese)", "https://kobe-kazamidori.com/guide/"),
                link("official", "萌黄の館（神戸市）", "Moegi House (Kobe City, Japanese)", "https://www.city.kobe.lg.jp/a21651/kanko/bunka/bunkashisetsu/foreigner/sub3.html"),
                link("official", "うろこグループの館（料金）", "Uroko group houses (fees, Japanese)", "https://kobe-ijinkan.net/ticket/tankan/")],
         info=info([row("hours", "風見鶏の館・萌黄の館 9:00〜17:00（入館16:45まで）。うろこグループの館（うろこの家・英国館・洋館長屋・山手八番館など）10:00〜17:00",
                        "Weathercock House & Moegi House 9:00–17:00 (last entry 16:45). Uroko group houses (Scale House, English House, row houses, Yamate Hachibankan and others) 10:00–17:00"),
                    row("closed", "風見鶏の館は毎月第3火曜（祝日なら翌日）。萌黄の館は2月の第3水曜とその翌日",
                        "Weathercock House: 3rd Tuesday of each month (next day if a holiday). Moegi House: 3rd Wednesday of February and the day after"),
                    row("fee", "風見鶏の館・萌黄の館 各500円、2館共通券800円（高校生以下は無料）。うろこの家・展望ギャラリー1,100円、英国館880円、洋館長屋550円、山手八番館550円",
                        "Weathercock House and Moegi House ¥500 each, combined ¥800 (free for high school and under). Scale House & gallery ¥1,100, English House ¥880, row houses ¥550, Yamate Hachibankan ¥550")],
                   tip=T("風見鶏の館の公式サイト、神戸市のページ、うろこグループの公式サイトで確認しました。", "Checked on the Weathercock House website, the Kobe City page and the Uroko group website."),
                   source=["風見鶏の館 公式サイト https://kobe-kazamidori.com/guide/", "神戸市 萌黄の館 https://www.city.kobe.lg.jp/a21651/kanko/bunka/bunkashisetsu/foreigner/sub3.html",
                           "うろこグループ 単館チケット https://kobe-ijinkan.net/ticket/tankan/"])),
    # 4 ---------------------------------------------------------------------
    dict(id="katsudon", name=T("かつ丼 七兵衛（三宮）", "Katsudon Hichibei (Sannomiya)"), kind=T("ランチ", "Lunch"),
         caution=T("食券制。とんかつが売り切れたら閉店", "Ticket machine. Closes when the cutlets sell out"),
         blurb=T("阪急神戸三宮駅のすぐ横、高架下の小さな店。厚いとんかつを玉子でとじたかつ丼で、午後の滝の階段にそなえます。",
                 "A small counter under the tracks right by Hankyu Kobe-Sannomiya: thick pork cutlets simmered with egg over rice, fuel for the waterfall steps this afternoon."),
         lat=34.69228, lng=135.19180,
         notices=[notice("入る前に", "Before you go in",
                         "入口の券売機で食券を買う店です。とんかつが売り切れると、その日は早く閉まります。閉店の時刻・定休日・支払い方法は公式のページに書かれていません。現金を用意して、閉まっていたら駅のまわりで別の店を探してください。",
                         "You buy a meal ticket from the machine at the door. When the cutlets sell out, the shop closes early for the day. The official page gives no closing time, closed days or payment methods, so bring cash, and if it is shut, look for somewhere else around the station.")],
         text=T("かつ丼 七兵衛（ひちべい）\n\n"
                "北野坂を下りきって、阪急の神戸三宮駅の西口へ。出てすぐ、JRの高架下にある小さなお店です。看板は「かつ丼 七兵衛」（運営会社のページでは「とんかつ七兵衛 神戸本店」）。\n\n"
                "入口の券売機で食券を買い、カウンターで食べます。店の前に写真つきのメニューが出ています（2枚目の写真）。分厚いかつを玉子でとじたかつ丼は、ボリュームたっぷり。ソースカツ丼やみそカツめしもあります。\n\n"
                "お店は11:30から。とんかつが売り切れると早めに閉まるので、お昼はあまり遅くしないほうが安心です。12時台は席が空くのを少し待つかもしれません。\n\n"
                "食べ終わったら、地下鉄の三宮駅まで歩いて約5分。次は新神戸へ1駅です。\n\n"
                "おすすめ訪問時間：12:20〜13:00",
                "Katsudon Hichibei\n\n"
                "At the bottom of Kitano-zaka, head for the west exit of Hankyu Kobe-Sannomiya Station. The tiny shop is right outside, under the JR tracks. The sign reads “Katsudon Hichibei” (the operator calls it “Tonkatsu Hichibei, Kobe main shop”).\n\n"
                "Buy a ticket from the machine at the door and eat at the counter. There’s a picture menu out front (second photo). The katsudon, thick cutlets simmered with egg, is a hearty bowl; there are sauce-katsudon and miso-katsu versions too.\n\n"
                "It opens at 11:30 and closes early once the cutlets sell out, so don’t leave lunch too late. Around noon you may wait a little for a seat.\n\n"
                "Afterwards it is about 5 minutes’ walk to Sannomiya subway station, one stop from Shin-Kobe.\n\n"
                "Recommended visit time: 12:20–13:00"),
         gmaps=[gm("とんかつ七兵衛", "Tonkatsu Hichibei", 34.69228, 135.19180, "とんかつ七兵衛 三宮")],
         links=[link("official", "とんかつ七兵衛（運営会社のページ）", "Tonkatsu Hichibei (operator page, Japanese)", "http://www.rb-syuhari.com/hichibe.html")],
         info=info([row("hours", "11:30〜（とんかつが売り切れたら閉店）。閉店時刻・定休日・支払い方法は公式のページに書かれていません（要確認）",
                        "From 11:30 (closes when the cutlets sell out). Closing time, closed days and payment methods are not given on the official page (please check)")],
                   tip=T("店名と開店時間、メニューは運営会社のページで確認しました。2024年2月に撮った店頭の案内には「11:10〜22:00、15:00〜17:00も開いてます」とありました。今は変わっているかもしれません。",
                         "Name, opening time and menu checked on the operator’s page. A sign at the door in February 2024 said 11:10–22:00, “open 15:00–17:00 too”; that may have changed."),
                   source=["有限会社アール・アンド・ビー守破離 とんかつ七兵衛 http://www.rb-syuhari.com/hichibe.html", "店頭の案内（Toshi の写真、2024年2月）"])),
    # 5 ---------------------------------------------------------------------
    dict(id="nunobiki", name=T("布引の滝", "Nunobiki Falls"), kind=T("滝・展望台", "Waterfall & viewpoint"),
         caution=T("階段が続く山道。歩きやすい靴で、15時には下りはじめる", "A trail of steps: wear good shoes and start down by 15:00"),
         blurb=T("新幹線の駅のすぐ裏に、落差43mの滝。その先のみはらし展望台から、午前に歩いた北野と、夕方に行く港がまとめて見えます。",
                 "A 43 m waterfall right behind a bullet-train station. From the lookout above it you can see both Kitano, where you walked this morning, and the port you are heading for."),
         lat=34.70983, lng=135.19385,
         notices=[notice("歩く前に", "Before you set off",
                         "駅からすぐですが、階段が続く山道です。歩きやすい靴で。日が短い季節は谷が早く暗くなるので、15時には下りはじめてください。",
                         "It starts right by the station, but it is a mountain trail of steps: wear good shoes. In the short days of late autumn and winter the valley darkens early, so start down by 15:00."),
                  notice("北野道は通行止め（2027年3月末まで）", "Kitano-michi path closed (until end of March 2027)",
                         "新神戸駅の裏からハーブ園の山麓駅の北へ抜ける山道「北野道」は、のり面の工事で通れません（神戸市）。滝からの帰りは、来た道を新神戸駅へ戻ってください。",
                         "The Kitano-michi trail from behind Shin-Kobe Station to north of the Herb Garden lower station is closed for slope works (Kobe City). Come back from the falls the way you went up, to Shin-Kobe Station.",
                         to="2027-03-31", url=MOUNTAIN)],
         text=T("布引の滝（ぬのびきのたき）\n\n"
                "三宮13:09か13:16発の地下鉄で新神戸まで1駅、2分・210円（歩くと上り坂を約20分）。トイレと飲み物は新神戸駅で済ませておくと安心です。\n\n"
                "新神戸駅の1階から歩いてすぐ山道に入り、雌滝（めんたき）、鼓ヶ滝（つづみがだき）、夫婦滝（めおとだき）、そしていちばん大きな雄滝（おんたき・落差43m）と、4つの滝が続きます。"
                "雌滝までは駅から約5分、雄滝までは約15分。階段が続くので、ゆっくり上って片道20〜25分とみておきましょう。\n\n"
                "雄滝からさらに数分登ると、みはらし展望台。ベンチがあり、神戸の街と港、晴れた日には大阪湾の向こうまで見えます。ここで座って休む時間をとってあります。\n\n"
                "入場料はいりません。11月下旬は16:50ごろに日が沈み、谷あいは先に暗くなるので、15時には下りはじめてください。\n\n"
                "新神戸14:50発の地下鉄で三宮へ戻ります。\n\n"
                "おすすめ訪問時間：13:25〜14:40",
                "Nunobiki Falls\n\n"
                "Take the subway from Sannomiya at 13:09 or 13:16: one stop to Shin-Kobe, 2 minutes, ¥210 (or about 20 minutes’ walk uphill). Use the toilets and buy a drink at Shin-Kobe Station before you set off.\n\n"
                "A trail starts right from the ground floor of the station and passes four falls: Mentaki, Tsuzumigadaki, Meotodaki and the biggest, Ontaki (43 m). "
                "Mentaki is about 5 minutes from the station and Ontaki about 15. It is steps most of the way, so allow 20–25 minutes each way at an easy pace.\n\n"
                "A few minutes’ climb beyond Ontaki is the Miharashi lookout, with benches and a view over the city and port, and on clear days across Osaka Bay. The timetable leaves you time to sit here.\n\n"
                "It’s free. In late November the sun sets around 16:50 and the valley darkens first, so start down by 15:00.\n\n"
                "Take the 14:50 subway from Shin-Kobe back to Sannomiya.\n\n"
                "Recommended visit time: 13:25–14:40"),
         gmaps=[gm("布引の滝（雄滝）", "Nunobiki Falls (Ontaki)", 34.70983, 135.19385, "布引の滝 雄滝"), gm("新神戸駅", "Shin-Kobe Station", 34.70722, 135.19692, "新神戸駅"),
                gm("神戸布引ロープウェイ ハーブ園山麓駅", "Nunobiki Ropeway lower station", 34.70560, 135.19530, "神戸布引ロープウェイ ハーブ園山麓駅")],
         links=[link("info", "布引の滝（Feel KOBE 神戸公式観光サイト）", "Nunobiki Falls (Feel KOBE, official)", "https://www.feel-kobe.jp/facilities/0000000093/"),
                link("official", "神戸布引ハーブ園／ロープウェイ（時間・料金）", "Nunobiki Herb Gardens & Ropeway (hours & fares, Japanese)", HERB), PLANNER],
         info=info([row("fee", "無料", "Free"),
                    row("hours", "新神戸駅から雌滝まで約5分、雄滝まで約15分（公式観光サイトの案内）。みはらし展望台まで上って休んで、往復1時間15分ほど",
                        "From Shin-Kobe Station: about 5 min to Mentaki, 15 min to Ontaki (per the official tourism site). Allow about 1 h 15 min there and back with a rest at the Miharashi lookout"),
                    row("train", "三宮13:09・13:16発 →（地下鉄西神・山手線）→ 新神戸 2分・210円。帰りは新神戸14:42・14:50発",
                        "Sannomiya 13:09 or 13:16 → (Seishin-Yamate subway line) → Shin-Kobe, 2 min, ¥210. Back from Shin-Kobe at 14:42 or 14:50"),
                    row("hours", "階段が苦手な人は、駅の近くから出るロープウェイでハーブ園へ：9:30〜、月〜木は下りの最終17:15。金・土・日・祝は夜も動き、上りは20:15まで、下りの最終21:00（12月11日〜28日は毎日）",
                        "Rather skip the steps? The ropeway to the Herb Gardens leaves from near the station: from 9:30; Mon–Thu last car down 17:15. On Fri, Sat, Sun and holidays it runs into the evening: last car up 20:15, last down 21:00 (daily 11–28 December)",
                        until="2026-12-28"),
                    row("hours", "階段が苦手な人は、駅の近くから出るロープウェイでハーブ園へ：9:30〜、下りの最終17:15（冬の時間）",
                        "Rather skip the steps? The ropeway to the Herb Gardens leaves from near the station: from 9:30, last car down 17:15 (winter hours)",
                        until="2027-03-12", frm="2026-12-29"),
                    row("fee", "ロープウェイ（ハーブ園の入園料込み）：12月28日まではクリスマスシーズンの特別料金で、大人 往復3,300円・片道2,700円。17時以降の割引料金はありません",
                        "Ropeway incl. Herb Gardens admission: Christmas-season fare until 28 December, adults ¥3,300 return, ¥2,700 one way. No after-17:00 discount in this period",
                        until="2026-12-28"),
                    row("fee", "ロープウェイ（ハーブ園の入園料込み）往復2,500円", "Ropeway incl. Herb Gardens admission ¥2,500 return", until="2027-03-12", frm="2026-12-29"),
                    row("closed", "ロープウェイとハーブ園は2027年1月23日〜2月19日、点検で休み（予定）", "Ropeway and gardens closed for maintenance 23 January – 19 February 2027 (planned)", until="2027-02-19")],
                   tip=T("滝は神戸観光局（Feel KOBE）、通行止めは神戸市、ロープウェイは布引ハーブ園の公式サイト、地下鉄は乗換案内で確認しました。",
                         "Falls checked on Feel KOBE, the closure on the Kobe City site, the ropeway on the Herb Gardens website and the subway on a route planner."),
                   source=["Feel KOBE 布引の滝 https://www.feel-kobe.jp/facilities/0000000093/", "神戸市 六甲山系登山道通行止（通行注意）状況（2026-11-09 版）" + " " + MOUNTAIN,
                           "神戸布引ハーブ園／ロープウェイ 営業時間・料金 " + HERB,
                           "神戸布引ハーブ園／ロープウェイ 2026年クリスマスシーズン料金表（PDF、2026-11-24 確認） " + HERB_XMAS, SRC_PLANNER])),
    # 6 ---------------------------------------------------------------------
    dict(id="meriken", name=T("メリケンパーク・神戸ポートタワー", "Meriken Park & Kobe Port Tower"), kind=T("港・展望タワー・夜景", "Harbour, tower & night view"),
         caution=T("ポートタワーは日時指定のチケット", "Port Tower needs a timed ticket"),
         blurb=T("南京町でつまんでから港へ。日の入りをメリケンパークで迎え、明かりの入ったポートタワーを対岸のモザイクから眺めて、晩ごはんまで。",
                 "Snack through Chinatown, then on to the harbour: sunset at Meriken Park, the lit-up Port Tower seen from Mosaic across the water, and dinner."),
         lat=34.68263, lng=135.18672,
         notices=[notice("ポートタワーに上るなら", "If you want to go up the Port Tower",
                         "展望フロアは日時指定のチケット制です。当日券は1階の売り場で、その時間の枠に空きがあるときだけ買えます。夕暮れに上りたい日は、先に公式サイトで買っておくと安心。屋上デッキは雨や強い風の日に閉まることがあります。",
                         "The observation floors need a timed ticket. Same-day tickets are sold at the ground-floor counter only if that time slot has space. If you want to be up there at dusk, buy on the official site beforehand. The rooftop deck can close in rain or strong wind.",
                         url="https://www.kobe-port-tower.com/ticket/"),
                  notice("神戸ルミナリエ（2027年1月29日〜2月7日）", "Kobe Luminarie (29 January – 7 February 2027)",
                         "点灯は薄暮から21:30まで。会場はメリケンパーク・東遊園地・旧居留地で、メリケンパークのメイン作品の有料エリアは日時指定のチケット制です。"
                         "前売券は平日500円・土日750円、当日券は平日1,000円・土日1,500円（小学生以下は無料）。当日券は15:00からメリケンパークの会場でも売っています。このスポットの5〜7枚目の写真は、2025年1月のルミナリエです。",
                         "Lit from dusk to 21:30 at Meriken Park, Higashi Yuenchi and the old foreign settlement. The paid area around the main work in Meriken Park needs a timed ticket: "
                         "¥500 weekdays / ¥750 weekends in advance, ¥1,000 / ¥1,500 on the day (free for elementary school age and under). Same-day tickets are also sold at the Meriken Park venue from 15:00. Photos 5–7 here are from the Luminarie in January 2025.",
                         to="2027-02-07", url=LUMI_TICKET)],
         text=T("メリケンパーク・神戸ポートタワー\n\n"
                "【南京町を抜けて港へ】三宮に戻ったら（14:52着）、センター街のアーケードを西へ歩いて約20分。大丸の先に、南京町（なんきんまち）の東の門があります。"
                "屋台の豚まんや小籠包をつまみながら通り抜けましょう。豚まんの「老祥記（ろうしょうき）」は18:30までですが、売り切れると早く閉まります。南京町から海へまっすぐ歩いて10分ちょっとで、メリケンパークです。\n\n"
                "【日の入り】海に面した公園に、赤い鼓のような形のポートタワーと、白い帆を重ねたような神戸海洋博物館が並びます。「BE KOBE」の白い文字の前には、写真を撮る人の列ができていることがあります。"
                "11月下旬の日の入りは16:50ごろです。16:30ごろの枠でポートタワーに上ると、夕暮れから街に明かりがつくまでを上から見られます。上らない日も、タワーの低い階の店とカフェには切符なしで入れます。\n\n"
                "【夜はモザイクへ】暗くなったら、海ぞいを西へ歩いて約15分、ハーバーランドの「モザイク」へ。海側のデッキから、明かりの入ったポートタワーと海洋博物館が水面ごと見えます（1枚目の写真が、こちら側から見た昼の眺めです）。"
                "晩ごはんはモザイクの中で。飲食店は22:00まで開いていて、観覧車（800円）も22:00までです。\n\n"
                "【帰り】モザイクからJR神戸駅まで歩いて約10分。神戸21:13発の新快速で、大阪21:39着・460円。難波へは高速神戸駅から、京都へは同じ新快速で（下の「電車」を見てください）。\n\n"
                "元町や三宮に戻って夜を過ごすなら、神戸市役所1号館の24階に、22:00まで開いている無料の展望ロビーがあります。\n\n"
                "おすすめ訪問時間：15:15〜21:00",
                "Meriken Park & Kobe Port Tower\n\n"
                "[Through Chinatown to the harbour] Back at Sannomiya (14:52), walk west through the Center-gai arcade for about 20 minutes. Just past the Daimaru department store is the east gate of Nankinmachi, Kobe’s Chinatown. "
                "Walk through it with a pork bun or soup dumplings from the stalls. The pork-bun shop Roshoki stays open until 18:30 but closes early when it sells out. From Nankinmachi it is a little over 10 minutes straight down to the sea and Meriken Park.\n\n"
                "[Sunset] On the waterfront stand the red, drum-shaped Port Tower and the white, sail-like Kobe Maritime Museum. There is sometimes a queue for photos in front of the white “BE KOBE” letters. "
                "In late November the sun sets around 16:50. Take a tower slot around 16:30 and you watch dusk fall and the city light up from above. Even without a ticket you can use the shops and café on the tower’s lower floors.\n\n"
                "[After dark: Mosaic] Once it is dark, walk west along the water for about 15 minutes to Mosaic in Harborland. From its seaside decks you see the lit-up Port Tower and Maritime Museum reflected in the water (the first photo is the same view by day). "
                "Have dinner in Mosaic: its restaurants are open until 22:00, as is the Ferris wheel (¥800).\n\n"
                "[Going home] JR Kobe Station is about 10 minutes’ walk from Mosaic. The 21:13 Special Rapid reaches Osaka at 21:39 (¥460). For Namba use Kosoku-Kobe Station; for Kyoto stay on the same Special Rapid (see “Train” below).\n\n"
                "If you would rather spend the evening back around Motomachi or Sannomiya, the 24th floor of Kobe City Hall Building 1 has a free observation lobby open until 22:00.\n\n"
                "Recommended visit time: 15:15–21:00"),
         gmaps=[gm("南京町（長安門）", "Nankinmachi (east gate)", 34.68860, 135.18960, "南京町 長安門"),
                gm("神戸ポートタワー", "Kobe Port Tower", 34.68263, 135.18672, "神戸ポートタワー"),
                gm("モザイク（ハーバーランド）", "Mosaic (Harborland)", 34.67990, 135.18380, "神戸ハーバーランドumie モザイク"),
                gm("JR神戸駅", "JR Kobe Station", 34.67929, 135.17828, "JR神戸駅"),
                gm("神戸市役所1号館（24階 展望ロビー）", "Kobe City Hall Bldg 1 (24F lobby)", 34.68990, 135.19560, "神戸市役所 1号館 展望ロビー")],
         links=[link("official", "神戸ポートタワー 公式サイト", "Kobe Port Tower (official)", "https://www.kobe-port-tower.com/"),
                link("official", "南京町 公式サイト", "Nankinmachi (official, Japanese)", "https://www.nankinmachi.or.jp/"),
                link("official", "老祥記 公式サイト", "Roshoki (official, Japanese)", "https://roushouki.com/shop/"),
                link("official", "神戸ハーバーランドumie（営業時間）", "Kobe Harborland umie (hours, Japanese)", "https://umie.jp/static-pages/opening-hours"),
                link("official", "神戸市役所 展望ロビー（神戸市）", "City Hall observation lobby (Kobe City, Japanese)", CITYHALL),
                link("official", "神戸ルミナリエ 公式サイト", "Kobe Luminarie (official)", "https://www.kobe-luminarie.jp/"), PLANNER],
         info=info([row("hours", "ポートタワー 展望フロア・屋上デッキ 9:00〜23:00（入場22:30まで）、日時指定のチケット制。年中無休（メンテナンスの日をのぞく）",
                        "Port Tower observation floors & rooftop deck 9:00–23:00 (last entry 22:30), timed tickets. Open daily except maintenance days"),
                    row("fee", "ポートタワー 展望フロア＋屋上デッキ 大人1,200円、展望フロアのみ1,000円。低い階の店は切符なしで入れます",
                        "Port Tower: observation floors + rooftop ¥1,200 adults, observation floors only ¥1,000. The lower-floor shops need no ticket"),
                    row("hours", "南京町：元町駅から歩いて約5分。店ごとに時間と休みが違います。老祥記 10:00〜18:30（売り切れ次第終了）、不定休",
                        "Nankinmachi: about 5 min on foot from Motomachi Station; hours and closing days vary by shop. Roshoki 10:00–18:30 (until sold out), irregular closing days"),
                    row("hours", "南京町ランターンフェア：2026年11月28日〜12月25日", "Nankinmachi Lantern Fair: 28 November – 25 December 2026", until="2026-12-25"),
                    row("hours", "モザイク：飲食店 11:00〜22:00、物販 10:00〜20:00（店により違います）。観覧車 10:00〜22:00・800円",
                        "Mosaic: restaurants 11:00–22:00, shops 10:00–20:00 (varies by shop). Ferris wheel 10:00–22:00, ¥800"),
                    row("hours", "神戸市役所1号館 24階展望ロビー：平日9:00〜22:00、土日祝10:00〜22:00、無料。12月29日〜1月3日と設備点検の日（2026年12月20日）は休み",
                        "Kobe City Hall Bldg 1, 24F observation lobby: weekdays 9:00–22:00, weekends & holidays 10:00–22:00, free. Closed 29 Dec – 3 Jan and on inspection days (20 December 2026)"),
                    row("hours", "神戸ルミナリエ：2027年1月29日〜2月7日、点灯は薄暮〜21:30", "Kobe Luminarie: 29 Jan – 7 Feb 2027, lit from dusk to 21:30", until="2027-02-07"),
                    row("fee", "ルミナリエの有料エリア（メリケンパーク、日時指定）：前売 平日500円・土日750円、当日 平日1,000円・土日1,500円。小学生以下は無料",
                        "Luminarie paid area (Meriken Park, timed): advance ¥500 weekdays / ¥750 weekends; on the day ¥1,000 / ¥1,500. Free for elementary school age and under",
                        until="2027-02-07"),
                    row("train", "大阪・梅田へ：JR神戸21:13発（新快速）→ 大阪21:39着・460円。阪急なら高速神戸21:10発（特急）→ 大阪梅田21:42着・470円",
                        "To Osaka/Umeda: JR Kobe 21:13 (Special Rapid) → Osaka 21:39, ¥460. By Hankyu: Kosoku-Kobe 21:10 (limited express) → Osaka-Umeda 21:42, ¥470"),
                    row("train", "難波へ：高速神戸21:05発（阪神の直通特急）→ 尼崎で乗り換え → 大阪難波21:56着・560円。高速神戸駅はJR神戸駅のすぐ先です",
                        "To Namba: Kosoku-Kobe 21:05 (Hanshin limited express) → change at Amagasaki → Osaka-Namba 21:56, ¥560. Kosoku-Kobe Station is just beyond JR Kobe Station"),
                    row("train", "京都へ：JR神戸21:13発（新快速）→ 京都22:09着・1,110円、乗り換えなし。最後は神戸23:32発（京都0:30着）",
                        "To Kyoto: JR Kobe 21:13 (Special Rapid) → Kyoto 22:09, ¥1,110, direct. The last one leaves Kobe at 23:32 (Kyoto 0:30)"),
                    row("train", "元町・三宮から帰るとき：阪急の神戸三宮21:03発（特急）→ 大阪梅田21:30着・330円。阪神の神戸三宮21:03発（快速急行）→ 大阪難波21:49着・420円、乗り換えなし",
                        "Going home from Motomachi/Sannomiya: Hankyu Kobe-Sannomiya 21:03 (limited express) → Osaka-Umeda 21:30, ¥330. Hanshin Kobe-Sannomiya 21:03 (rapid express) → Osaka-Namba 21:49, ¥420, direct")],
                   tip=T("ポートタワー・南京町・老祥記・ハーバーランドumie・ルミナリエは公式サイト、展望ロビーは神戸市、電車は乗換案内（土曜のダイヤ）で確認しました。",
                         "Port Tower, Nankinmachi, Roshoki, Harborland umie and the Luminarie checked on their websites, the lobby on the Kobe City site, trains on a route planner (Saturday timetable)."),
                   source=["神戸ポートタワー 公式サイト https://www.kobe-port-tower.com/", "南京町商店街振興組合 https://www.nankinmachi.or.jp/", "老祥記 https://roushouki.com/shop/",
                           "神戸ハーバーランドumie 営業時間 https://umie.jp/static-pages/opening-hours", "神戸市 庁舎案内（1号館24階展望ロビー、2026-11-10 更新）" + " " + CITYHALL,
                           "神戸ルミナリエ 公式サイト https://www.kobe-luminarie.jp/",
                           "第32回神戸ルミナリエ チケット（有料エリアの料金、2026-11-24 確認） " + LUMI_TICKET, SRC_PLANNER])),
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
N = lambda ids: [NO[k] for k in ids]
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": {k: N(v) for k, v in rule.items()}, "text": T(ja, en)}
SEC = lambda a, b, aj, ae, tj, te: {"first": NO[a], "last": NO[b], "area": T(aj, ae), "title": T(tj, te)}
data = {
    "id": "kobe",
    "_note": "神戸の1日ルート（kobe/ のページ専用。形は eizan-line.json と同じ）。起点は大阪の梅田〜難波のあたりのホテル（京都から来る人の電車は補足）。"
             "大阪梅田9:30発→神戸三宮→北野坂→北野天満神社→北野異人館街→三宮でかつ丼→地下鉄で新神戸・布引の滝→南京町→メリケンパークで日の入り・ポートタワー→夜のハーバーランド（モザイク）→21時ごろの電車で大阪へ。"
             "各スポットの「おすすめ訪問時間」は11月下旬（日の入り16:50ごろ）・土曜のダイヤの時間割。コースは1つ（朝早く行かないと困る場所がないため）。"
             "写真は Toshi の写真ライブラリから選んだもの（布引の滝と北野は2023年6月19日の Nikon D7000、メリケンパークは2024年2月・8月と2025年1月のルミナリエ、七兵衛は2024年2月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "南京町・ハーバーランドは写真がないので、6番のスポットの中で案内している。"
             "info.source は確認した出典、info.checked は確認日。入口で困ること（休み・チケット・売り切れ・通行止め）は caution と head つきの notices。"
             "店名を出しているのは Toshi が食べた七兵衛と、公式サイトで営業時間を確かめた店（老祥記・にしむら珈琲店）だけ。このファイルは scripts/build_kobe_data.py で作る（直接直さない）。",
    "sections": [SEC("sannomiya", "sannomiya", "三宮", "Sannomiya", "大阪から阪急で27分", "27 minutes from Osaka"),
                 SEC("tenman", "ijinkan", "北野", "Kitano", "午前は坂の上の異人館へ", "Morning among the hillside houses"),
                 SEC("katsudon", "katsudon", "三宮", "Sannomiya", "坂を下りてお昼", "Down the slope for lunch"),
                 SEC("nunobiki", "nunobiki", "新神戸", "Shin-Kobe", "駅の裏の滝と展望台", "The falls and lookout behind the station"),
                 SEC("meriken", "meriken", "南京町〜港", "Chinatown to the harbour", "夕暮れから夜の港", "The harbour from dusk into the night")],
    "plan": {"_note": "「選んで回る」の設定。駅はいつも入る。最初は「全部回る」で開く（6か所とも時間割に入っているため）。",
             "picks": N(["tenman", "ijinkan", "katsudon", "nunobiki", "meriken"]),
             "auto": {str(NO["sannomiya"]): {"always": True}},
             "hints": [
                 H("nunobiki", {"any": ["nunobiki"], "none": ["tenman", "ijinkan"]},
                   "北野に行かない日は、三宮に着いたらそのまま地下鉄で新神戸へ。午前のうちに滝を歩けば、七兵衛が開く11:30に合わせて三宮へ下りられます。",
                   "Skipping Kitano? Take the subway straight to Shin-Kobe when you arrive. Walk the falls in the morning and you are back down in Sannomiya as Hichibei opens at 11:30."),
                 H("ijinkan", {"any": ["ijinkan"], "none": ["katsudon"]},
                   "お昼を三宮で食べない日は、北野坂の途中の「北野坂にしむら珈琲店」へ。1階の喫茶は10:00〜22:00、2階のレストランの昼は11:00〜14:30です（毎月最終月曜休み）。",
                   "Not having lunch in Sannomiya? Kitano-zaka Nishimura Coffee is halfway down the slope: ground-floor café 10:00–22:00, upstairs restaurant lunch 11:00–14:30 (closed last Monday of the month)."),
                 H("meriken", {"any": ["meriken"], "none": ["nunobiki"]},
                   "滝に行かない日は、13時すぎに三宮を出られます。旧居留地の石造りのビルの通りをゆっくり歩いて南京町へ。時間が余ったら、先に神戸市役所1号館24階の無料の展望ロビーから港を見ておけます。",
                   "Skipping the falls? You can leave Sannomiya soon after 13:00. Stroll through the stone-fronted streets of the old foreign settlement to Nankinmachi. With time to spare, look over the port first from the free 24th-floor lobby of Kobe City Hall Building 1."),
                 H("sannomiya", {"any": ["tenman", "ijinkan", "katsudon", "nunobiki"], "none": ["meriken"]},
                   "港に行かない日の夜景は、神戸市役所1号館24階の展望ロビーで（三宮の駅から海側へ歩いて10分弱、無料、22:00まで）。",
                   "Not going to the harbour? See the night view from the 24th-floor lobby of Kobe City Hall Building 1: under 10 minutes’ walk towards the sea from the Sannomiya stations, free, open until 22:00."),
             ]},
    "photoBase": "../images/kobe/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
