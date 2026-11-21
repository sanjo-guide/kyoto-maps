#!/usr/bin/env python3
"""京都 宇治と伏見のデータ（data/routes/uji.json）を書き出す。

使い方: python3 scripts/build_uji_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 自分の写真は images/uji/<スポットのid>-<番号>.jpg を番号の順に全部使う
- ネットから借りた写真（Wikimedia Commons）は images/uji/<id>-w<番号>.jpg。撮影者とライセンスは scripts/uji_web_credits.json
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/uji"
OUT = f"{R}/data/routes/uji.json"
CHECKED = "2026-11-21"
WEB = json.load(open(f"{R}/scripts/uji_web_credits.json", encoding="utf-8"))
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


def info(rows, tip=None, verified=True, cash=False):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid, web_first=False):
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, []))]
    web = WEB.get(pid, [])
    for w in web:
        assert os.path.exists(f"{IMG}/{w['file']}"), w["file"]
    out = web + own if web_first else own + web
    assert out, pid
    return out


YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
TRAIN_TIP = T("電車の時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。乗る前にもう一度確かめてください。",
              "Train times and fares checked on a route planner (Saturday timetable, November 2026). Please check again before you travel.")

S = [
    dict(id="ujieki", name=T("JR宇治駅", "JR Uji Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都駅からJR奈良線で20分ほど。平等院が開く8:45に間に合うように、朝早めに出ます。",
                 "About 20 minutes from Kyoto Station on the JR Nara Line. Leave early enough to be at Byodoin when it opens at 8:45."),
         lat=34.89020, lng=135.80144,
         text=T("JR宇治駅（うじえき）\n\n京都駅の8〜10番のりばからJR奈良線で。京都8:15発に乗ると、宇治に8:33に着きます（240円）。9時台からは「みやこ路快速」もあり、快速なら17分ほどです。\n\n"
                "祇園四条や三条のあたりに泊まっているなら、京阪電車のほうが便利です。祇園四条8:03発→中書島で宇治線に乗り換え→京阪宇治8:34着（360円）。京阪の宇治駅は宇治橋のすぐ東で、平等院まで歩いて10分。\n\n"
                "JR宇治駅の南口を出たら、宇治橋通り商店街を歩いて宇治橋のたもとへ（約8分）。駅前には茶壺の形をした郵便ポストがあります。\n\n"
                "朝いちばんに平等院へ行くのには理由があります。鳳凰堂の中に入る券は先着順で、混む日は午前のうちに遠い時間の回しか残らなくなるからです。\n\nおすすめ到着時間：8:33",
                "JR Uji Station\n\nTake the JR Nara Line from platforms 8–10 at Kyoto Station. The 8:15 arrives in Uji at 8:33 (¥240). From around 9:00 there are also “Miyakoji Rapid” trains, about 17 minutes.\n\n"
                "Staying near Gion-Shijo or Sanjo? The Keihan line is easier: Gion-Shijo 8:03 → change to the Uji Line at Chushojima → Keihan Uji 8:34 (¥360). Keihan Uji Station is right at the east end of Uji Bridge, 10 minutes’ walk from Byodoin.\n\n"
                "From the south exit of JR Uji, walk along the Ujibashi-dori shopping street to the bridge (about 8 minutes). Look for the postbox shaped like a tea jar in front of the station.\n\n"
                "There is a reason to do Byodoin first thing: tickets to go inside the Phoenix Hall are first come, first served, and on busy days only late slots are left by mid-morning.\n\nRecommended arrival: 8:33"),
         gmaps=[gm("JR宇治駅", "JR Uji Station", 34.89020, 135.80144, "JR宇治駅")],
         links=[YAHOO],
         info=info([row("train", "京都8:15発（JR奈良線）→ 宇治8:33着・240円", "Kyoto 8:15 (JR Nara Line) → Uji 8:33, ¥240"),
                    row("train", "祇園四条8:03発（京阪・中書島で乗り換え）→ 京阪宇治8:34着・360円", "Gion-Shijo 8:03 (Keihan, change at Chushojima) → Keihan Uji 8:34, ¥360")],
                   tip=TRAIN_TIP)),
    dict(id="ujibashi", name=T("宇治橋と紫式部像", "Uji Bridge & the Murasaki Shikibu statue"), kind=T("橋", "Bridge"),
         blurb=T("宇治川にかかる、木の欄干の橋。西のたもとに紫式部の像があり、ここから平等院表参道が始まります。",
                 "The bridge over the Uji River with wooden railings. A statue of Murasaki Shikibu sits at its west end, where the approach to Byodoin begins."),
         lat=34.89228, lng=135.80589,
         text=T("宇治橋（うじばし）\n\n646年に初めて架けられたと伝わる、日本でも指折りの古い橋です。今の橋は1996年に架け替えられたもので、欄干はヒノキ。上流側に張り出した「三の間（さんのま）」は、豊臣秀吉がお茶の水を汲ませた場所と伝わります。\n\n"
                "西のたもと（JR宇治駅側）には、源氏物語の最後の十帖が宇治を舞台にしていることにちなんだ紫式部の像。その横の鳥居のある道が平等院表参道です。\n\n"
                "橋の上から上流を見ると、川の中の島と朝霧橋の朱色、その奥の山が見えます。朝は人が少なく、川の音がよく聞こえます。橋を渡るのは帰り（京阪宇治駅へ行くとき）でかまいません。\n\nおすすめ訪問時間：8:40〜8:50",
                "Uji Bridge\n\nSaid to have first been built in 646, this is one of the oldest bridge sites in Japan. The current bridge dates from 1996 and has cypress railings. The little platform jutting out upstream, the “San-no-ma”, is where Toyotomi Hideyoshi is said to have had water drawn for tea.\n\n"
                "At the west end (the JR side) sits a statue of Murasaki Shikibu: the last ten chapters of The Tale of Genji are set in Uji. The lane with the torii beside her is Byodoin Omotesando.\n\n"
                "Look upstream from the bridge for the islands, the vermilion Asagiri Bridge and the hills behind. In the morning it is quiet and you can hear the river. You will cross the bridge later, on the way to Keihan Uji Station.\n\nRecommended visit time: 8:40–8:50"),
         gmaps=[gm("宇治橋（紫式部像）", "Uji Bridge (Murasaki Shikibu statue)", 34.89228, 135.80589, "紫式部像 宇治橋")],
         links=[link("info", "宇治市観光協会", "Uji City Tourist Association (Japanese)", "https://www.kyoto-uji-kankou.or.jp/")],
         info=info([row("hours", "いつでも渡れます", "Open at all times"),
                    row("fee", "無料", "Free")])),
    dict(id="byodoin", name=T("平等院 鳳凰堂", "Byodoin Temple (Phoenix Hall)"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
         blurb=T("10円玉の表のお堂。池の向こうに左右に翼を広げた姿を、正面から。中に入る券は先着順なので、着いたらまず受付へ。",
                 "The hall on the ¥10 coin, spreading its wings across the pond. Tickets to go inside are first come, first served, so head to that desk first."),
         lat=34.88930, lng=135.80762,
         text=T("平等院（びょうどういん）\n\n1053年に藤原頼通が建てた阿弥陀堂が、今も池の中の島に建っています。10円玉の表の絵がこの鳳凰堂、1万円札の裏の鳳凰は屋根の上の鳳凰です。\n\n"
                "【着いたらまず】表門で拝観券（700円）を買ったら、写真より先に庭園の中の「鳳凰堂内部拝観受付」へ。内部拝観は別に300円で、9:10から時間指定の券を配ります。20分ごとに1回35人、先着順。2026年10月から定員が50人から35人に減ったので、混む日は昼前に遠い時間の券しか残りません。開門の8:45に入れば、9:30か9:50の回が取れることが多いです。\n\n"
                "【写真を撮る場所】池（阿字池）をはさんだ正面の岸です。鳳凰堂は東を向いているので、午前は正面に日が当たり、午後は逆光ぎみになります。風のない朝は池にお堂が映ります。1枚目の写真は2025年2月の午後2時半ごろ、正面の岸から撮りました。\n\n"
                "お堂の中では、高さ約2.8mの阿弥陀如来坐像と、壁にかかる雲中供養菩薩像を目の前で見られます（中は撮影禁止）。券の時間まではミュージアム鳳翔館へ。鳳凰の本物と、雲中供養菩薩像を間近で見られます。\n\n"
                "境内は飲食禁止で、ふたのないテイクアウトのカップは持ち込めません。抹茶ラテを買うなら出てからに。内部拝観の券を持っていれば、いったん外へ出て戻ることもできます。\n\nおすすめ訪問時間：8:50〜10:25",
                "Byodoin\n\nThe Amida hall built by Fujiwara no Yorimichi in 1053 still stands on its island in the pond. It is the building on the ¥10 coin, and the phoenix on the back of the ¥10,000 note is the one on its roof.\n\n"
                "First thing: after buying your ticket (¥700) at the main gate, go to the “Phoenix Hall interior” desk inside the garden before taking photos. The interior visit costs ¥300 extra; timed tickets are handed out from 9:10, 35 people every 20 minutes, first come, first served. The group size was cut from 50 to 35 in October 2026, so on busy days only late slots are left by late morning. If you enter at 8:45 you can usually get the 9:30 or 9:50 visit.\n\n"
                "Where to take the photo: from the bank straight across the pond. The hall faces east, so the front is sunlit in the morning and backlit in the afternoon. On a still morning it is mirrored in the water. My first photo was taken from that bank at about 2:30 pm in February 2025.\n\n"
                "Inside you stand right in front of the 2.8-metre seated Amida and the small bodhisattvas on clouds along the walls (no photos inside). While you wait for your slot, see the Hoshokan museum: the original roof phoenixes and more of the cloud bodhisattvas up close.\n\n"
                "No eating or drinking in the grounds, and open takeaway cups are not allowed in, so buy your matcha latte afterwards. With an interior ticket you may leave the grounds and come back.\n\nRecommended visit time: 8:50–10:25"),
         gmaps=[gm("平等院", "Byodoin", 34.88930, 135.80762, "平等院")],
         links=[link("official", "平等院 公式サイト（拝観案内）", "Byodoin (official)", "https://www.byodoin.or.jp/guide/", "https://www.byodoin.or.jp/en/"),
                link("info", "鳳凰堂内部拝観について（待ち時間のめやす）", "Phoenix Hall interior visit (official, Japanese)", "https://www.byodoin.or.jp/guide/internal-view/")],
         notices=[{"from": None, "to": "2026-12-06", "url": "https://www.byodoin.or.jp/news/cat23/2022-1/",
                   "head": T("紅葉の時期（12月6日まで）", "Autumn season (until 6 Dec)"),
                   "text": T("11月13日〜12月6日は混み合います。土日祝はミュージアムの映像展示が休みで、御朱印は1種類だけ。夜間特別拝観は2026年秋から休止しています。",
                             "Very busy from 13 Nov to 6 Dec. On weekends and holidays the museum’s video room is closed and only one kind of goshuin is given. Evening openings have been suspended since autumn 2026.")}],
         info=info([row("hours", "庭園 8:45〜17:30（受付17:15まで）。ミュージアム鳳翔館 9:00〜17:00（受付16:45まで）", "Garden 8:45–17:30 (last entry 17:15). Hoshokan museum 9:00–17:00 (last entry 16:45)"),
                    row("hours", "鳳凰堂内部拝観 9:30〜16:10、20分ごと・各回35人。受付は9:10から先着順（なくなり次第終了）", "Phoenix Hall interior 9:30–16:10, every 20 min, 35 people each. Tickets from 9:10, first come, first served"),
                    row("closed", "年中無休（法要や行事で内部拝観が休みの日があります）", "Open every day (interior visits are sometimes suspended for services)"),
                    row("fee", "大人700円、中高生400円、小学生300円（庭園とミュージアム）。鳳凰堂内部は別に300円", "Adults ¥700, junior/senior high ¥400, elementary ¥300 (garden and museum). Phoenix Hall interior ¥300 extra")],
                   tip=T("時間・料金・内部拝観の決まりは平等院の公式サイトで確認しました。JR宇治駅から歩いて約10分、京阪宇治駅からも約10分です。",
                         "Hours, fees and the interior-visit rules checked on the official Byodoin website. About 10 minutes on foot from either JR Uji or Keihan Uji Station."))),
    dict(id="omotesando", name=T("平等院表参道と中村藤吉 平等院店", "Byodoin Omotesando & Nakamura Tokichi"), kind=T("お茶の通り・甘味", "Tea street & sweets"),
         blurb=T("お茶屋さんが並ぶ、ほうじ茶を炒る香りの通り。宇治川に面した中村藤吉で、抹茶のひと休みを。",
                 "A lane of tea shops that smells of roasting hojicha. Stop for matcha at Nakamura Tokichi, overlooking the Uji River."),
         lat=34.89147, lng=135.80664,
         text=T("平等院表参道（びょうどういんおもてさんどう）\n\n宇治橋のたもとから平等院の表門まで約200m。古いお茶屋さんや抹茶のお菓子の店が並び、店先でほうじ茶を炒る香りがします。ほとんどの店は10時ごろに開くので、平等院を見たあとに歩くとちょうどいい時間です。\n\n"
                "ひと休みは、通りの中ほどから宇治川のほうへ入った「中村藤吉（なかむらとうきち）平等院店」で。丸に十の字ののれんが目印です。カウンターで注文して自分で席へ運ぶ形で、窓の向こうは宇治川。写真の抹茶にソフトクリームをのせた一杯と、名物の生茶ゼリイが人気です（写真は2025年2月）。\n\n"
                "予約はできません。昼すぎから列が長くなるので、開店の10時から11時ごろまでに入るのがおすすめ。JR宇治駅の近くには本店もあります。\n\n"
                "通りの入口近くには、庭を眺められるスターバックス（京都宇治平等院表参道店）もあります。\n\n"
                "このあと伏見でお昼にするなら、ここでは甘いものだけに。宇治でお昼にするなら、この通りの茶そばを。\n\nおすすめ訪問時間：10:30〜11:15",
                "Byodoin Omotesando\n\nAbout 200 metres from the foot of Uji Bridge to Byodoin’s main gate, lined with old tea merchants and matcha sweet shops; you can smell hojicha being roasted at the shopfronts. Most shops open around 10:00, so walking it after Byodoin works well.\n\n"
                "For a break, turn towards the river halfway along to Nakamura Tokichi Byodoin: look for the curtain with a cross in a circle. You order at the counter and carry your tray to a seat; the windows look onto the Uji River. The matcha topped with soft-serve in my photo and the “nama-cha jelly” are the favourites (photos from February 2025).\n\n"
                "No reservations. The queue grows from early afternoon, so come between opening at 10:00 and about 11:00. The main shop is near JR Uji Station.\n\n"
                "Near the start of the lane there is also a Starbucks with a garden view.\n\n"
                "If you plan lunch in Fushimi, keep it to sweets here. For lunch in Uji, try green-tea soba on this street.\n\nRecommended visit time: 10:30–11:15"),
         gmaps=[gm("中村藤吉 平等院店", "Nakamura Tokichi Byodoin", 34.89147, 135.80664, "中村藤吉 平等院店"),
                gm("平等院表参道", "Byodoin Omotesando", 34.89180, 135.80620, "平等院表参道")],
         links=[link("official", "中村藤吉 平等院店（公式）", "Nakamura Tokichi Byodoin (official, Japanese)", "https://tokichi.jp/pages/byodo-in-store-page")],
         info=info([row("hours", "中村藤吉 平等院店：銘茶売場・カフェ 10:00〜17:00（カフェのラストオーダー16:30）", "Nakamura Tokichi Byodoin: shop and café 10:00–17:00 (café last orders 16:30)"),
                    row("closed", "定休日なし（年末年始と臨時休業を除く）", "Open daily (except New Year and occasional closures)")],
                   tip=T("中村藤吉の公式サイトで確認しました。予約はできず、混む日はラストオーダーより早く受付が終わることがあります。ほかの店の時間は店ごとに違います。",
                         "Checked on the Nakamura Tokichi website. No reservations; on busy days the café may stop taking guests before last orders. Other shops keep their own hours."))),
    dict(id="tonoshima", name=T("宇治川 塔の島と朝霧橋（夏の夜は鵜飼）", "Uji River: Tonoshima island & Asagiri Bridge"), kind=T("川・散歩", "River walk"),
         blurb=T("川の中の島に渡り、朱色の朝霧橋で向こう岸へ。夏の夜は、かがり火の下で鵜飼が見られます。",
                 "Cross to the islands in the river, then over the vermilion Asagiri Bridge to the far bank. On summer nights, cormorant fishing by firelight."),
         lat=34.88900, lng=135.80930,
         text=T("宇治川（うじがわ）の塔の島・橘島と朝霧橋（あさぎりばし）\n\n平等院の南門を出るか、表参道から川沿いの「あじろぎの道」を上流へ歩くと、朱色の小さな喜撰橋（きせんばし）があります。渡った先が塔の島。高さ約15mの十三重石塔は鎌倉時代のものです。隣の橘島へ進み、朱色の朝霧橋を渡ると、宇治神社の鳥居の前に出ます。\n\n"
                "宇治川は流れが速く、水の色が濃い川です。島の岸には屋形船が並びます。\n\n"
                "【夏の夜の鵜飼】7月1日〜9月30日（水曜休み）は、喜撰橋のたもとから鵜飼の船が出ます。乗合船は予約なしの当日受付で、17:30ごろから受付、7・8月は19:00、9月は18:30に出船。かがり火のすぐ近くまで船を寄せてくれます。後半の写真は2017年9月に乗合船から撮りました。岸からも見えます。\n\n"
                "鵜飼まで見る日は、順番を逆にして伏見を午前に回り、午後に宇治へ来るのがおすすめです（月桂冠大倉記念館は9:30から）。ただし平等院の内部拝観の券は、午後だと売り切れていることがあります。\n\nおすすめ訪問時間：11:20〜11:40",
                "Tonoshima and Tachibana islands and Asagiri Bridge\n\nLeave Byodoin by the south gate, or walk upstream along the riverside path from Omotesando, to the little vermilion Kisen Bridge. It leads to Tonoshima island and its 15-metre, thirteen-storey stone pagoda from the Kamakura period. Continue to Tachibana island and cross the vermilion Asagiri Bridge to arrive in front of the torii of Uji Shrine.\n\n"
                "The Uji runs fast and deep green. Roofed pleasure boats are moored along the island.\n\n"
                "Cormorant fishing on summer nights: from 1 July to 30 September (not Wednesdays) boats leave from beside Kisen Bridge. Shared boats take no reservations; sign up on the day from about 17:30. Departure is 19:00 in July and August and 18:30 in September, and the boat takes you right up to the fire. My night photos were taken from a shared boat in September 2017. You can also watch from the bank.\n\n"
                "If you want to stay for it, reverse the day: Fushimi in the morning (the Gekkeikan museum opens at 9:30) and Uji in the afternoon. Note that Phoenix Hall interior tickets may be gone by then.\n\nRecommended visit time: 11:20–11:40"),
         gmaps=[gm("塔の島（十三重石塔）", "Tonoshima (stone pagoda)", 34.88880, 135.80905, "宇治公園 塔の島 十三重石塔"),
                gm("朝霧橋", "Asagiri Bridge", 34.89021, 135.80941, "朝霧橋 宇治")],
         links=[link("official", "宇治川の鵜飼（宇治市観光協会）", "Uji River cormorant fishing (Uji tourist association, Japanese)", "https://www.kyoto-uji-kankou.or.jp/ukai.html")],
         info=info([row("hours", "島と橋はいつでも歩けます（無料）", "The islands and bridges are always open (free)"),
                    row("hours", "鵜飼：7月1日〜9月30日（水曜休み）。受付17:30ごろ〜、出船は7・8月19:00、9月18:30（約1時間）", "Cormorant fishing: 1 Jul – 30 Sep (not Wed). Sign-up from about 17:30; departs 19:00 in Jul–Aug, 18:30 in Sep (about 1 hour)"),
                    row("fee", "鵜飼の乗合船 大人2,700円、小学生1,200円（予約不可・定員になり次第終了）", "Shared cormorant boat: adults ¥2,700, elementary ¥1,200 (no reservations; closes when full)")],
                   tip=T("鵜飼の期間・時間・料金は宇治市観光協会の公式サイトで確認しました。雨や天ヶ瀬ダムの放流で川が増水した日は中止になります。",
                         "Cormorant fishing dates, times and fares checked on the Uji tourist association website. It is cancelled in bad weather or when the Amagase dam releases water."))),
    dict(id="koshoji", name=T("興聖寺と琴坂", "Koshoji Temple & Kotozaka slope"), kind=T("寺（寄り道）", "Temple (detour)"),
         blurb=T("もみじのトンネルになる参道「琴坂」の先の、静かな禅寺。朝霧橋から上流へ歩いて7分ほどの寄り道です。",
                 "A quiet Zen temple at the top of Kotozaka, an approach that becomes a tunnel of maples. A 7-minute detour upstream from Asagiri Bridge."),
         lat=34.88946, lng=135.81340,
         text=T("興聖寺（こうしょうじ）\n\n朝霧橋を渡ったら、川沿いを上流（右）へ歩いて約7分。石の門から本堂の前の竜宮造りの門まで、ゆるい上り坂が200mほど続きます。両側の水路を流れる水の音が琴の音に聞こえることから「琴坂（ことざか）」。両側はもみじで、新緑の5月と紅葉の11月下旬がとくにきれいです。\n\n"
                "道元が開いた曹洞宗の寺を、江戸時代のはじめにこの地に再興した禅寺で、今も修行の場です。琴坂を歩くだけなら無料。本堂や庭を見る場合は受付で志納料を納めます。\n\n"
                "平等院のまわりに比べて人がぐっと少ないので、静かな場所が好きな人に。見たら同じ道を戻って、宇治神社へ。\n\nおすすめ訪問時間：寄るなら約40分（11:45〜12:25ごろ）",
                "Koshoji\n\nAfter crossing Asagiri Bridge, walk upstream (right) along the river for about 7 minutes. From the stone gate a gentle slope climbs some 200 metres to the white Chinese-style gate before the main hall. The water running in the channels on both sides was said to sound like a koto, hence “Kotozaka”. Maples line both sides: best in the fresh green of May and the red of late November.\n\n"
                "A Soto Zen temple first founded by Dogen and re-established here in the early Edo period; monks still train here. Walking Kotozaka is free; to see the halls and garden, pay the donation at the reception.\n\n"
                "Far fewer people come here than to Byodoin, so it suits anyone who likes quiet. Return the same way to Uji Shrine.\n\nRecommended visit time: allow about 40 minutes (around 11:45–12:25)"),
         gmaps=[gm("興聖寺（琴坂）", "Koshoji (Kotozaka)", 34.88946, 135.81340, "興聖寺 宇治 琴坂")],
         links=[link("official", "興聖寺 公式サイト", "Koshoji (official)", "https://www.uji-koushouji.jp/access/", "https://www.uji-koushouji.jp/en/")],
         info=info([row("hours", "拝観の受付 10:00〜16:00（行事で入れない日があります）", "Reception 10:00–16:00 (closed to visitors during some events)"),
                    row("fee", "拝観志納料 500円（琴坂を歩くだけなら無料）", "Donation ¥500 (walking Kotozaka is free)")],
                   tip=T("時間と志納料は興聖寺の公式サイトで確認しました。京阪宇治駅からは歩いて約15分です。", "Hours and donation checked on the official Koshoji website. About 15 minutes on foot from Keihan Uji Station."))),
    dict(id="ujigami", name=T("宇治上神社と宇治神社", "Ujigami Shrine & Uji Shrine"), kind=T("神社（世界遺産）", "Shrines (World Heritage)"),
         blurb=T("朝霧橋を渡ると宇治神社、その奥に世界遺産の宇治上神社。日本でいちばん古い神社の建物が、木立の中に残っています。",
                 "Across Asagiri Bridge is Uji Shrine, and behind it World Heritage Ujigami Shrine, with the oldest shrine building in Japan among the trees."),
         lat=34.89205, lng=135.81146,
         text=T("宇治神社（うじじんじゃ）と宇治上神社（うじかみじんじゃ）\n\n朝霧橋を渡った正面の鳥居が宇治神社。石段の上の朱色の門の奥に、鎌倉時代の本殿（重要文化財）があります。道に迷った祭神を兎が振り返りながら案内したという言い伝えから、境内のあちこちに「みかえり兎」がいます。\n\n"
                "宇治神社の横の「さわらびの道」を2分ほど上ると、朱色の鳥居の先が宇治上神社です。平等院と同じく世界遺産。手前の拝殿は鎌倉時代、奥の本殿は平安時代の後期に建てられた、今残っている中で日本でいちばん古い神社の建物で、どちらも国宝です。本殿は覆いの建物の中に、3つの小さな社が並んでいます。格子ごしにのぞいてみてください。\n\n"
                "色を塗っていない木の建物で、平等院の華やかさとは反対の静けさがあります。境内は小さく、15分ほどで見られます。境内に湧く「桐原水（きりはらすい）」は宇治七名水のうち今も残るただ1つです。\n\n"
                "ここから京阪宇治駅までは、さわらびの道を歩いて約8分。途中に源氏物語ミュージアムがあります。\n\nおすすめ訪問時間：11:45〜12:20",
                "Uji Shrine and Ujigami Shrine\n\nThe torii straight ahead as you come off Asagiri Bridge is Uji Shrine. Up the steps, behind the vermilion gate, stands a Kamakura-period main hall (Important Cultural Property). Legend says a rabbit led the lost deity here, looking back to check he was following, so “looking-back rabbits” are all over the grounds.\n\n"
                "Two minutes up the Sawarabi path beside it, through a vermilion torii, is Ujigami Shrine, World Heritage like Byodoin. The worship hall in front is Kamakura period; the main hall behind it, from the late Heian period, is the oldest surviving shrine building in Japan. Both are National Treasures. The main hall is three small shrines side by side inside a sheltering building: peer through the lattice.\n\n"
                "The wood is unpainted, and the mood is the opposite of Byodoin’s splendour. The grounds are small; 15 minutes is enough. The Kirihara spring in the grounds is the only one left of Uji’s seven famous waters.\n\n"
                "From here it is about 8 minutes along the Sawarabi path to Keihan Uji Station, passing the Tale of Genji Museum.\n\nRecommended visit time: 11:45–12:20"),
         gmaps=[gm("宇治上神社", "Ujigami Shrine", 34.89205, 135.81146, "宇治上神社"),
                gm("宇治神社", "Uji Shrine", 34.89085, 135.81042, "宇治神社")],
         links=[link("official", "宇治神社 公式サイト", "Uji Shrine (official, Japanese)", "https://uji-jinja.com/")],
         info=info([row("hours", "宇治上神社 9:00〜16:00ごろ（要確認）。宇治神社の境内は自由", "Ujigami Shrine about 9:00–16:00 (please check). Uji Shrine grounds are open"),
                    row("fee", "どちらも無料", "Both free")],
                   tip=T("宇治上神社の時間は公式の案内で確かめられませんでした（16:00ごろに門が閉まるという案内が多いです）。午後遅くに行く日は気をつけてください。写真の鳥居と朱色の門は2017年6月。",
                         "Ujigami Shrine’s hours could not be confirmed from an official source (most guides say the gate closes around 16:00), so don’t leave it too late. The torii and vermilion gate photos are from June 2017."),
                   verified=False)),
    dict(id="mimuroto", name=T("三室戸寺", "Mimurotoji Temple"), kind=T("花の寺（寄り道）", "Flower temple (detour)"),
         caution=T("あじさいは6月。歩いて片道25分", "Hydrangeas in June; a 25-minute walk each way"),
         blurb=T("6月に2万株のあじさいが咲く花の寺。宇治上神社から歩いて25分ほどかかるので、花の時期に時間をとって。",
                 "The flower temple, with 20,000 hydrangeas in June. It is a 25-minute walk from Ujigami Shrine, so make time for it in the flower season."),
         lat=34.89978, lng=135.81870,
         text=T("三室戸寺（みむろとじ）\n\n西国三十三所の第十番札所。山すその広い庭に、春はつつじ（4月下旬〜5月中旬）、6月はあじさい、夏は本堂の前の蓮と、花が続きます。いちばんの見ごろはあじさいで、杉木立の下に約2万株。公式サイトの2027年の案内では、あじさい園の公開は5月29日〜7月4日です。\n\n"
                "花のない時期は、正直なところ遠回りになります。行くなら4月下旬〜7月上旬がおすすめです。\n\n"
                "宇治上神社からは、源氏物語ミュージアムの前を通って歩いて約25分。帰りは京阪の三室戸駅まで歩いて15分で、そこから中書島へ（14分・320円）。宇治駅へ戻る必要はありません。\n\n"
                "受付は15:10までと早く、6月の土日はとても混みます。境内は飲食禁止、三脚も使えません。\n\nおすすめ訪問時間：寄るなら歩きを入れて約1時間40分",
                "Mimurotoji\n\nTemple no. 10 of the Saigoku Kannon pilgrimage. Its big garden at the foot of the hills flowers in turn: azaleas (late April to mid May), hydrangeas in June, then lotuses in front of the main hall in summer. The hydrangeas are the highlight: about 20,000 plants under tall cedars. The official site lists the 2027 hydrangea garden as open 29 May – 4 July.\n\n"
                "Outside the flower seasons it is honestly a long detour; come between late April and early July.\n\n"
                "From Ujigami Shrine it is about 25 minutes on foot, past the Tale of Genji Museum. Afterwards walk 15 minutes to Keihan Mimuroto Station and ride to Chushojima (14 min, ¥320); no need to go back to Uji Station.\n\n"
                "Last entry is as early as 15:10, and June weekends are very crowded. No eating or drinking, and no tripods.\n\nRecommended visit time: allow about 1 h 40 min including the walk"),
         gmaps=[gm("三室戸寺", "Mimurotoji", 34.89978, 135.81870, "三室戸寺"),
                gm("京阪 三室戸駅", "Keihan Mimuroto Station", 34.89886, 135.80634, "三室戸駅")],
         links=[link("official", "三室戸寺 公式サイト（拝観のご案内）", "Mimurotoji (official, Japanese)", "https://www.mimurotoji.com/guide/index.html")],
         info=info([row("hours", "8:30〜15:10（受付終了）", "8:30–15:10 (last entry)"),
                    row("closed", "8月11日〜17日、12月29日〜31日", "11–17 August, 29–31 December"),
                    row("fee", "大人1,000円、小人500円", "Adults ¥1,000, children ¥500"),
                    row("train", "京阪 三室戸駅から歩いて15分。三室戸 → 中書島 14分・320円", "15 min on foot from Keihan Mimuroto Station. Mimuroto → Chushojima 14 min, ¥320")],
                   tip=T("時間・料金・休みは三室戸寺の公式サイトで確認しました。花の見ごろは年によって前後します。", "Hours, fees and closed days checked on the official Mimurotoji website. Flowering times vary from year to year."))),
    dict(id="keihanuji", name=T("京阪 宇治駅", "Keihan Uji Station"), kind=T("駅", "Station"),
         blurb=T("宇治橋の東のたもとの駅。ここから京阪宇治線で、伏見の中書島まで16分です。",
                 "The station at the east end of Uji Bridge. From here the Keihan Uji Line takes 16 minutes to Chushojima in Fushimi."),
         lat=34.89387, lng=135.80698,
         text=T("京阪 宇治駅（けいはん うじえき）\n\n宇治上神社からさわらびの道を歩いて約8分、宇治橋の東のたもとにある駅です。丸いアーチを重ねたコンクリートの駅舎が目印。JRの宇治駅とは川をはさんで歩いて10分ほど離れているので、間違えないように。\n\n"
                "駅の手前、橋のたもとの「通圓（つうえん）」は、平安時代の終わりの創業と伝わるお茶屋さんです。電車を待つあいだにお茶を買えます。\n\n"
                "宇治線は10〜15分おき。12:40発に乗ると中書島に12:56に着きます（320円）。伏見へは中書島で降ります。\n\nおすすめ出発時間：12:40",
                "Keihan Uji Station\n\nAbout 8 minutes on foot from Ujigami Shrine along the Sawarabi path, at the east end of Uji Bridge: a concrete building of stacked round arches. It is a 10-minute walk across the river from JR Uji Station, so don’t mix them up.\n\n"
                "Just before the station, at the foot of the bridge, Tsuen is a tea shop said to date from the end of the Heian period; a good place to buy tea while you wait.\n\n"
                "Uji Line trains run every 10–15 minutes. The 12:40 reaches Chushojima at 12:56 (¥320). Get off there for Fushimi.\n\nRecommended departure: 12:40"),
         gmaps=[gm("京阪 宇治駅", "Keihan Uji Station", 34.89387, 135.80698, "京阪宇治駅")],
         links=[YAHOO],
         info=info([row("train", "京阪宇治12:40発 → 中書島12:56着・320円（10〜15分おき）", "Keihan Uji 12:40 → Chushojima 12:56, ¥320 (every 10–15 min)")],
                   tip=TRAIN_TIP)),
    dict(id="chushojima", name=T("京阪 中書島駅", "Keihan Chushojima Station"), kind=T("駅", "Station"),
         blurb=T("伏見の酒蔵の町の入口。月桂冠大倉記念館へ歩いて5分、寺田屋へ7分です。",
                 "The gateway to Fushimi’s sake district: 5 minutes on foot to the Gekkeikan museum, 7 to Teradaya."),
         lat=34.92689, lng=135.76007,
         text=T("京阪 中書島駅（ちゅうしょじまえき）\n\n宇治線の終点で、京阪本線との乗り換え駅です。北口を出て、まっすぐ北へ歩くと酒蔵の町に入ります。\n\n"
                "伏見は、京都と大阪を結ぶ川の港として栄えた町です。地下水がよく、今も20近い蔵元が酒を造っています。歩くエリアは中書島駅から伏見桃山駅まで、南北に800mほど。帰りは北の伏見桃山駅から乗るので、ここへは戻りません。\n\n"
                "京都の街なかから伏見だけに来るなら、京阪の祇園四条から特急で中書島まで約12分（320円）。京都駅からは近鉄で桃山御陵前まで10分（300円）です。\n\nおすすめ到着時間：12:56",
                "Keihan Chushojima Station\n\nThe end of the Uji Line and the junction with the Keihan Main Line. Leave by the north exit and walk straight north into the brewery quarter.\n\n"
                "Fushimi grew rich as the river port between Kyoto and Osaka. Its groundwater is good, and nearly twenty breweries still make sake here. The walking area runs about 800 metres north from Chushojima to Fushimi-Momoyama Station; you leave from the latter, so you won’t come back here.\n\n"
                "Coming only to Fushimi from central Kyoto? The Keihan limited express from Gion-Shijo takes about 12 minutes to Chushojima (¥320). From Kyoto Station, the Kintetsu line takes 10 minutes to Momoyamagoryo-mae (¥300).\n\nRecommended arrival: 12:56"),
         gmaps=[gm("中書島駅", "Chushojima Station", 34.92689, 135.76007, "中書島駅")],
         links=[YAHOO],
         info=info([row("train", "祇園四条 → 中書島 約12分・320円（京阪の特急）", "Gion-Shijo → Chushojima about 12 min, ¥320 (Keihan limited express)"),
                    row("train", "京都 → 桃山御陵前 10分・300円（近鉄）", "Kyoto → Momoyamagoryo-mae 10 min, ¥300 (Kintetsu)")],
                   tip=TRAIN_TIP)),
    dict(id="teradaya", name=T("寺田屋", "Teradaya Inn"), kind=T("史跡", "Historic inn"),
         blurb=T("坂本龍馬が襲われた船宿。川べりに建つ2階建ての旅籠で、中を見学できます。",
                 "The riverside boat inn where Sakamoto Ryoma was attacked. You can go inside the two-storey building."),
         lat=34.93029, lng=135.75956,
         text=T("寺田屋（てらだや）\n\n大阪へ下る三十石船の客が泊まった船宿です。1866年、ここに泊まっていた坂本龍馬が幕府の役人に襲われ、のちに妻となるお龍の知らせで逃げのびた「寺田屋事件」で知られます。\n\n"
                "中には龍馬ゆかりの品や写真が並びます。今の建物は、幕末の戦いで焼けたあとに建て直されたものとされています。そのつもりで見ると、かえって船宿の造りそのものを楽しめます。\n\n"
                "中に入らなくても、外から見る格子の2階建てと提灯、隣の庭の龍馬像だけで雰囲気は十分。受付は15:40までと早いので、伏見では最初に寄ります。すぐ前の川が十石舟の通る宇治川派流です。\n\n"
                "ここから北へ延びる「竜馬通り商店街」を歩くと、お昼の鳥せい本店まで約5分です。\n\nおすすめ訪問時間：13:05〜13:30",
                "Teradaya\n\nA boat inn for passengers on the river boats to Osaka. It is known for the Teradaya incident of 1866, when Sakamoto Ryoma, staying here, was attacked by shogunate officers and escaped thanks to a warning from Oryo, later his wife.\n\n"
                "Inside are mementoes and photographs. The present building is thought to have been rebuilt after the original burned in the fighting of 1868; knowing that, you can simply enjoy it as a boat inn.\n\n"
                "Even without going in, the latticed two-storey front with its lanterns and the Ryoma statue in the garden next door give you the feel. Last entry is as early as 15:40, so make it your first stop in Fushimi. The canal in front is the one the jikkokubune boats use.\n\n"
                "From here the Ryoma-dori shopping street leads north; lunch at Torisei is about 5 minutes away.\n\nRecommended visit time: 13:05–13:30"),
         gmaps=[gm("寺田屋", "Teradaya", 34.93029, 135.75956, "寺田屋 伏見")],
         links=[],
         info=info([row("hours", "10:00〜16:00（受付15:40まで）", "10:00–16:00 (last entry 15:40)"),
                    row("closed", "月曜に不定休あり、1月1日〜3日", "Some Mondays, 1–3 January"),
                    row("fee", "大人400円", "Adults ¥400")],
                   tip=T("寺田屋には公式サイトがなく、時間と料金は旅行ガイドの情報です。行く前に電話（075-622-0243）で確かめると安心です。中書島駅から歩いて約7分。",
                         "Teradaya has no official website; hours and fee are from travel guides. Phone ahead (075-622-0243) to be sure. About 7 minutes on foot from Chushojima Station."),
                   verified=False, cash=True)),
    dict(id="torisei", name=T("鳥せい本店", "Torisei Honten"), kind=T("ランチ・焼き鳥と蔵出しの酒", "Lunch: chicken & brewery sake"),
         blurb=T("蔵元「神聖」の酒蔵を使った鳥料理の店。お昼の御膳と、蔵出しの生原酒を。",
                 "Chicken dishes in a converted storehouse of the Shinsei brewery. Have a lunch set and a glass of unpasteurised brewery sake."),
         lat=34.93108, lng=135.76207,
         text=T("鳥せい本店（とりせいほんてん）\n\n1677年創業の蔵元、山本本家（銘柄は「神聖」）の酒蔵を改装した鳥料理の店です。白い壁に「鳥せい」の看板、「蔵元直営」の紺ののれんが目印。中は太い梁の広い土間で、ひとりでも入りやすい店です。\n\n"
                "お昼は鳥めしや焼き鳥の御膳が手ごろ。写真は2025年2月のお昼に食べたものです。お酒が飲める人は、蔵元ならではの蔵出しの生原酒を一杯。\n\n"
                "12時台は並びます。宇治を回ってから13時半ごろに着くと、列が短くなっています。このあと月桂冠できき酒をするので、先にしっかり食べておくのがおすすめです。\n\n"
                "店の横には、酒造りに使う伏見の名水「白菊水（しらぎくすい）」が湧いていて、地元の人が汲みに来ます。\n\nおすすめ訪問時間：13:35〜14:25",
                "Torisei Honten\n\nA chicken restaurant in a converted storehouse of Yamamoto Honke, brewers of “Shinsei” sake since 1677. Look for the white wall with the 鳥せい sign and the navy curtain. Inside is a big earthen-floored hall under heavy beams, easy to enter alone.\n\n"
                "At lunch the chicken-rice and yakitori sets are good value; my photo is a lunch from February 2025. If you drink, try a glass of the brewery’s unpasteurised sake.\n\n"
                "There is a queue around noon. Arriving about 13:30 after Uji, it is shorter. You will be tasting sake at Gekkeikan next, so eat properly first.\n\n"
                "Beside the restaurant the Shiragiku spring, one of Fushimi’s brewing waters, flows freely; locals come to fill bottles.\n\nRecommended visit time: 13:35–14:25"),
         gmaps=[gm("鳥せい本店", "Torisei Honten", 34.93108, 135.76207, "鳥せい本店 伏見")],
         links=[],
         info=info([row("hours", "11:00ごろ〜夜まで通し営業（要確認）", "From about 11:00 through to the evening (please check)"),
                    row("closed", "月曜休み（祝日は営業）との案内が多い（要確認）", "Most guides say closed Mondays, open on holidays (please check)")],
                   tip=T("公式サイトにつながらず、営業時間と休みは確認できていません。月曜に行く日は電話（075-622-5533）で確かめてください。伏見桃山駅から歩いて約7分。",
                         "The official website could not be reached, so hours and closed days are unconfirmed. If you go on a Monday, phone first (075-622-5533). About 7 minutes on foot from Fushimi-Momoyama Station."),
                   verified=False)),
    dict(id="gekkeikan", name=T("月桂冠大倉記念館", "Gekkeikan Okura Sake Museum"), kind=T("酒の博物館・きき酒", "Sake museum & tasting"),
         blurb=T("1637年創業の月桂冠の酒蔵を使った博物館。最後に、コイン3枚で好きな酒を3種類きき酒できます。現金は使えません。",
                 "A museum in the old storehouses of Gekkeikan, founded 1637. At the end, three coins buy three tastings of your choice. No cash accepted."),
         lat=34.92888, lng=135.76163,
         text=T("月桂冠大倉記念館（げっけいかんおおくらきねんかん）\n\n白壁と焼杉板の酒蔵が並ぶ、伏見らしい一角にあります。入ると、おみやげのおちょことコインを3枚もらえます。昔の酒造りの道具を見たあと、きき酒処へ。約10種類の酒が機械に並んでいて、コインを1枚入れてボタンを押すと1杯分が出てきます。\n\n"
                "【きき酒のこつ】ボタンは軽く1回押すだけ（自動で止まります）。大吟醸のような香りの軽いものから先に、古酒や梅酒のような味の濃いものはあとに。水も置いてあるので、あいだに飲みましょう。おちょこは持ち帰れます。空腹だとすぐ回るので、お昼のあとがおすすめです。自転車や車で来た人、20歳未満の人は飲めません。\n\n"
                "【大事なこと】支払いはキャッシュレスだけで、現金は使えません。クレジットカードか電子マネー、スマホのコード決済を用意してください。\n\n"
                "【予約】公式サイトで2週間前から前日16:30まで予約でき、予約した人が先に入れます。予約なしでも入れますが、混む日は待つか、入れないこともあります。土日や桜・紅葉の時期は予約を。受付は16:00までなので、遅くなりすぎないように。\n\n"
                "写真は2025年2月。建物の裏の川沿いが十石舟の乗り場です。\n\nおすすめ訪問時間：14:35〜15:25",
                "Gekkeikan Okura Sake Museum\n\nIt stands in the most Fushimi-like corner of town, among white-plastered, charred-cedar storehouses. On entry you receive a souvenir sake cup and three coins. After the old brewing tools, go to the tasting room: about ten sakes sit in dispensers; put in a coin, press the button, and one serving comes out.\n\n"
                "Tasting tips: press the button once, lightly (it stops by itself). Start with light, fragrant ones such as daiginjo and leave the strong-flavoured aged sake or plum wine for last. Water is provided; drink some between cups. The cup is yours to keep. Sake hits fast on an empty stomach, so come after lunch. No tasting if you came by bicycle or car, or are under 20.\n\n"
                "Important: payment is cashless only. Bring a credit card, e-money or a QR payment app.\n\n"
                "Booking: you can reserve on the official site from two weeks ahead until 16:30 the day before, and booked visitors enter first. Walk-ins are accepted, but on busy days you may wait or be turned away; book for weekends and the cherry and maple seasons. Last entry is 16:00, so don’t leave it late.\n\n"
                "Photos from February 2025. The boarding place for the jikkokubune is on the canal behind the building.\n\nRecommended visit time: 14:35–15:25"),
         gmaps=[gm("月桂冠大倉記念館", "Gekkeikan Okura Sake Museum", 34.92888, 135.76163, "月桂冠大倉記念館")],
         links=[link("official", "月桂冠大倉記念館（ご見学案内・予約）", "Gekkeikan Okura Sake Museum (official)", "https://www.gekkeikan.co.jp/enjoy/museum/access/")],
         notices=[{"from": None, "to": None, "url": "https://www.gekkeikan.co.jp/enjoy/museum/access/",
                   "head": T("現金は使えません", "No cash"),
                   "text": T("入館料・売店・追加のきき酒コインは、すべてキャッシュレス決済だけです。", "Admission, the shop and extra tasting coins are all cashless only.")}],
         info=info([row("hours", "9:30〜16:30（受付16:00まで）。見学は40〜60分", "9:30–16:30 (last entry 16:00). Allow 40–60 minutes"),
                    row("closed", "8月13日〜16日、12月28日〜1月4日、ほかに臨時休館あり", "13–16 August, 28 December – 4 January, plus occasional closures"),
                    row("fee", "20歳以上600円（きき酒3種類とおみやげ付き）、13〜19歳100円、12歳以下無料", "Ages 20+ ¥600 (three tastings and a souvenir), 13–19 ¥100, 12 and under free")],
                   tip=T("月桂冠の公式サイトで確認しました。中書島駅から歩いて5分、伏見桃山駅から10分です。", "Checked on the official Gekkeikan website. 5 minutes on foot from Chushojima, 10 from Fushimi-Momoyama."))),
    dict(id="jikkoku", name=T("十石舟と酒蔵の町並み", "Jikkokubune boat & the brewery canal"), kind=T("遊覧船", "Canal boat"),
         caution=T("運航は3月下旬〜12月上旬", "Runs late March to early December"),
         blurb=T("柳と酒蔵の白壁の下を、小さな屋形船で50分。春から秋だけの運航です。冬は川沿いを歩くだけでも。",
                 "Fifty minutes in a small roofed boat under willows and white brewery walls. Spring to autumn only; in winter, just walk the bank."),
         lat=34.92850, lng=135.76130,
         text=T("十石舟（じっこくぶね）\n\n月桂冠大倉記念館の裏、川に下りた所が乗り場です。江戸時代に酒や米、旅人を運んだ舟を再現した20人乗りの屋形船で、柳の並ぶ宇治川派流を下り、三栖閘門（みすこうもん）でいったん降りて資料館を見てから戻ります。全部で約50分。\n\n"
                "川から見上げる酒蔵の焼杉の壁と柳が、伏見でいちばん絵になる景色です。舟に乗らなくても、乗り場のあたりから弁天橋まで川沿いを歩けば同じ景色が見られます。桜の時期（3月末〜4月上旬）と、あじさいの6月がとくにきれいです。\n\n"
                "【乗り方】空席があれば予約なしで乗れます。桜の時期や土日は、公式サイトからネット予約を。出航の15分前（3〜5月は20分前）までに受付をすませます。\n\n"
                "2026年は12月6日まで（11月25日からは最終便が15:40）。冬は川の工事のため運休で、例年3月下旬に再開します。\n\nおすすめ乗船時間：15:40〜16:30",
                "Jikkokubune\n\nThe landing is down on the canal behind the Gekkeikan museum. The 20-seat roofed boat recreates the craft that carried sake, rice and travellers in the Edo period. It glides down the willow-lined canal to the Misu lock gate, where you get off to see a small museum, then returns: about 50 minutes in all.\n\n"
                "The charred-cedar brewery walls and willows seen from the water are Fushimi’s most photogenic view. Without the boat, you get the same view walking the bank from the landing to Benten Bridge. It is at its best in cherry season (late March to early April) and with the hydrangeas in June.\n\n"
                "How to ride: if there are seats you can board without a reservation. In cherry season and at weekends, book online on the official site. Check in 15 minutes before departure (20 minutes in March–May).\n\n"
                "In 2026 the boats run until 6 December (last boat 15:40 from 25 November). They stop in winter for river works and usually restart in late March.\n\nRecommended boat time: 15:40–16:30"),
         gmaps=[gm("十石舟のりば", "Jikkokubune landing", 34.92850, 135.76130, "伏見十石舟 乗船場")],
         links=[link("official", "十石舟（伏見観光協会・予約）", "Jikkokubune (Fushimi tourist association, Japanese)", "https://kyoto-fushimi.or.jp/fune"),
                link("info", "伏見十石舟（京都観光Navi）", "Fushimi Jikkokubune (Kyoto City official guide, Japanese)", "https://ja.kyoto.travel/event/single.php?event_id=4100")],
         notices=[{"from": "2026-12-07", "to": "2027-03-19", "url": "https://kyoto-fushimi.or.jp/fune",
                   "head": T("冬は運休", "No boats in winter"),
                   "text": T("12月中旬から3月中旬は運休です。2027年の運航日は伏見観光協会のサイトで確かめてください。", "No boats from mid December to mid March. Check the Fushimi tourist association site for the 2027 season.")}],
         info=info([row("hours", "2026年：3月20日〜12月6日、10:00〜16:20（11月25日〜12月6日は最終15:40）", "2026: 20 Mar – 6 Dec, 10:00–16:20 (last boat 15:40 from 25 Nov to 6 Dec)", until="2026-12-06"),
                    row("closed", "月曜（祝日は運航。4・5・10・11月は月曜も運航）、8月12日〜31日、冬", "Mondays (runs on holidays, and on Mondays in Apr, May, Oct, Nov), 12–31 August, winter"),
                    row("fee", "大人（中学生以上）1,900円、小学生900円", "Adults (junior high and up) ¥1,900, elementary ¥900")],
                   tip=T("運航日・時間・料金は京都市の観光サイト（京都観光Navi）と伏見観光協会のサイトで確認しました。天気や川の様子で変わることがあります。",
                         "Dates, times and fares checked on Kyoto City’s official travel guide and the Fushimi tourist association site. They can change with the weather and river conditions."))),
    dict(id="kizakura", name=T("キザクラカッパカントリー", "Kizakura Kappa Country"), kind=T("地ビールと日本酒（寄り道）", "Craft beer & sake (detour)"),
         blurb=T("カッパの絵で知られる黄桜の直営店。京都で最初の地ビールを、酒蔵の中のレストランで飲めます。",
                 "The brewery restaurant of Kizakura, known for its kappa cartoons, with Kyoto’s first craft beer on tap in an old storehouse."),
         lat=34.93083, lng=135.76050,
         text=T("キザクラカッパカントリー\n\n黄桜（きざくら）の酒蔵を使った店で、レストラン「黄桜酒場」と売店、カッパの資料を集めたギャラリーがあります。黄桜は1995年に京都で最初の地ビールを造った蔵で、できたての京都麦酒を飲めるのがここです。売店には缶ビールや限定の酒が並びます（写真は2025年2月）。\n\n"
                "レストランは昼と夜に分かれていて、14:30〜17:00は閉まります。日本酒よりビールという人は、お昼をここにするか（ラストオーダー14:00）、十石舟のあとの17:00から寄るのがおすすめです。鳥せい本店から歩いて2分。\n\nおすすめ訪問時間：寄るなら17:00〜",
                "Kizakura Kappa Country\n\nIn Kizakura’s old storehouses: the Kizakura Sakaba restaurant, a shop, and a gallery of kappa (water sprite) memorabilia. Kizakura brewed Kyoto’s first craft beer in 1995, and this is where you drink it fresh. The shop sells cans and limited sakes (photos from February 2025).\n\n"
                "The restaurant closes between lunch and dinner, 14:30–17:00. If you prefer beer to sake, have lunch here instead (last orders 14:00) or drop in from 17:00 after the boat. Two minutes’ walk from Torisei.\n\nRecommended visit time: from 17:00 if you stop by"),
         gmaps=[gm("キザクラカッパカントリー", "Kizakura Kappa Country", 34.93083, 135.76050, "キザクラカッパカントリー")],
         links=[link("official", "キザクラカッパカントリー（公式）", "Kizakura Kappa Country (official, Japanese)", "https://kizakura.co.jp/restaurant/country/")],
         info=info([row("hours", "黄桜酒場：11:30〜14:30（土日祝は11:00〜、ラストオーダー14:00）、17:00〜21:30（ラストオーダー20:50）", "Kizakura Sakaba: 11:30–14:30 (from 11:00 on weekends and holidays; last orders 14:00), 17:00–21:30 (last orders 20:50)"),
                    row("closed", "火曜（祝日のときは水曜）、12月31日・1月1日", "Tuesdays (Wednesday if Tuesday is a holiday), 31 December and 1 January")],
                   tip=T("レストランの時間と休みは黄桜の公式サイトで確認しました。売店とギャラリーの時間は確認できていません。", "Restaurant hours and closed days checked on the official Kizakura website. Shop and gallery hours are unconfirmed."))),
    dict(id="gokonomiya", name=T("御香宮神社", "Gokonomiya Shrine"), kind=T("神社（寄り道）", "Shrine (detour)"),
         blurb=T("伏見の酒を育てた水の神社。境内に湧く「御香水」は名水百選で、表門は伏見城の門を移したものです。",
                 "The shrine of the water behind Fushimi’s sake. Its spring is one of Japan’s 100 famous waters, and its gate came from Fushimi Castle."),
         lat=34.93523, lng=135.76722,
         text=T("御香宮神社（ごこうのみやじんじゃ）\n\n伏見桃山駅から大手筋を東へ、線路を2本越えて歩いて約5分。平安時代に境内から香りのよい水が湧いたことが名前の由来で、今も本殿の横に「御香水（ごこうすい）」が湧いています。伏見の酒がこの地下水で造られていることを、ここで実感できます。\n\n"
                "通りに面した表門は伏見城の大手門を移したもの。拝殿の正面の、極彩色の彫刻も見どころです。\n\n"
                "境内は自由に入れます。小堀遠州ゆかりの石庭は有料です（料金と時間は要確認）。舟に乗らない日や、時間が余ったときの寄り道に。暗くなる前に行きましょう。\n\nおすすめ訪問時間：寄るなら約20分",
                "Gokonomiya Shrine\n\nFrom Fushimi-Momoyama Station walk east along Otesuji, over two railway lines, for about 5 minutes. The name comes from a fragrant spring that appeared here in the Heian period, and the “Gokosui” water still flows beside the main hall. Here you can see for yourself the groundwater Fushimi’s sake is made from.\n\n"
                "The front gate on the street was moved from Fushimi Castle. The brightly painted carvings on the front of the worship hall are worth a look too.\n\n"
                "The grounds are free to enter. The stone garden associated with Kobori Enshu has a fee (fee and hours: please check). A good detour on days without the boat or when you have time left; go before dark.\n\nRecommended visit time: about 20 minutes if you stop by"),
         gmaps=[gm("御香宮神社", "Gokonomiya Shrine", 34.93523, 135.76722, "御香宮神社")],
         links=[link("official", "御香宮神社 公式サイト", "Gokonomiya Shrine (official, Japanese)", "https://gokounomiya.kyoto.jp/")],
         info=info([row("hours", "境内は自由。石庭の時間は要確認", "Grounds open; stone garden hours: please check"),
                    row("fee", "境内は無料。石庭は有料（要確認）", "Grounds free; fee for the stone garden (please check)")],
                   tip=T("石庭の料金と時間は公式サイトで確かめられませんでした。", "The stone garden’s fee and hours could not be confirmed on the official website."),
                   verified=False)),
    dict(id="momoyama", name=T("大手筋商店街と伏見桃山駅", "Otesuji arcade & Fushimi-Momoyama Station"), kind=T("商店街・駅（ゴール）", "Arcade & station (finish)"),
         blurb=T("屋根のある長い商店街を抜けると駅。京阪で祇園四条へ14分、近鉄なら京都駅へ12分です。",
                 "A long covered arcade leads to the station: 14 minutes to Gion-Shijo by Keihan, or 12 to Kyoto Station by Kintetsu."),
         lat=34.93281, lng=135.76437,
         text=T("大手筋（おおてすじ）商店街と伏見桃山駅（ふしみももやまえき）\n\n酒蔵の町から北へ5分ほど歩くと、屋根のある大手筋商店街に出ます。地元の人の買い物の通りで、酒屋には伏見の蔵の酒がそろっています。おみやげの酒はここで買うと、最後まで持ち歩かずにすみます。\n\n"
                "商店街を東へ抜けた所が京阪の伏見桃山駅。その先の赤い大鳥居をくぐると、すぐ近鉄の桃山御陵前駅です。\n\n"
                "・祇園四条や三条へ：京阪で。17:35発に乗り、次の丹波橋で特急に乗り換えると祇園四条に17:49（320円）。\n"
                "・京都駅へ：近鉄の桃山御陵前から12分（300円）。\n\n"
                "京阪の各駅停車で5つ先の伏見稲荷駅で降りれば、伏見稲荷大社です（東山のマップで紹介しています）。鳥居の道は夜も歩けます。\n\nおすすめ出発時間：17:35ごろ",
                "Otesuji arcade and Fushimi-Momoyama Station\n\nFive minutes’ walk north of the breweries is the covered Otesuji arcade, where locals shop; its liquor stores stock sake from all the Fushimi breweries. Buy your bottle here and you won’t have to carry it all afternoon.\n\n"
                "The east end of the arcade is Keihan Fushimi-Momoyama Station. Just beyond, through the big red torii, is Kintetsu Momoyamagoryo-mae Station.\n\n"
                "· To Gion-Shijo or Sanjo: Keihan. Take the 17:35, change to the limited express at the next stop, Tambabashi, and reach Gion-Shijo at 17:49 (¥320).\n"
                "· To Kyoto Station: Kintetsu from Momoyamagoryo-mae, 12 minutes (¥300).\n\n"
                "Five stops up the line by Keihan local train is Fushimi-Inari Station, for Fushimi Inari Shrine (see my Higashiyama map). The torii paths are open after dark.\n\nRecommended departure: about 17:35"),
         gmaps=[gm("伏見桃山駅（京阪）", "Fushimi-Momoyama Station (Keihan)", 34.93281, 135.76437, "伏見桃山駅"),
                gm("桃山御陵前駅（近鉄）", "Momoyamagoryo-mae Station (Kintetsu)", 34.93345, 135.76553, "桃山御陵前駅")],
         links=[YAHOO],
         info=info([row("train", "伏見桃山17:35発（京阪・丹波橋で特急に乗り換え）→ 祇園四条17:49着・320円", "Fushimi-Momoyama 17:35 (Keihan, change to the limited express at Tambabashi) → Gion-Shijo 17:49, ¥320"),
                    row("train", "桃山御陵前17:38発（近鉄）→ 京都17:50着・300円", "Momoyamagoryo-mae 17:38 (Kintetsu) → Kyoto 17:50, ¥300")],
                   tip=TRAIN_TIP)),
]

WEB_FIRST = {"ujigami", "kizakura"}
spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"], out["id"] in WEB_FIRST)
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
UJI = [NO[k] for k in ("ujibashi", "byodoin", "omotesando", "tonoshima", "koshoji", "ujigami", "mimuroto")]
FUSHIMI = [NO[k] for k in ("teradaya", "torisei", "gekkeikan", "jikkoku", "kizakura", "gokonomiya")]
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
data = {
    "id": "uji",
    "_note": "京都 宇治と伏見の1日ルート（uji/ のページ専用。形は eizan-line.json と同じ）。朝にJRで宇治へ、平等院→表参道（中村藤吉）→宇治川の塔の島・朝霧橋→宇治神社・宇治上神社→京阪で中書島→寺田屋→鳥せい本店（昼）→月桂冠大倉記念館→十石舟→伏見桃山駅。"
             "興聖寺・三室戸寺・キザクラカッパカントリー・御香宮神社は寄り道。"
             "写真は Toshi の写真ライブラリから（宇治は2017年6月・2017年9月の鵜飼・2025年2月、伏見は2025年2月、中書島駅は2026年5月。横の写真だけ、縦で撮った抹茶・きき酒・おちょこは横に切り抜き。長辺1600px・位置情報なし）。"
             "自分の写真がない場所（JR宇治駅・宇治橋・宇治上神社の建物・興聖寺・三室戸寺・京阪宇治駅・寺田屋・十石舟・御香宮神社・大鳥居など）は Wikimedia Commons の写真（photos の要素が {file, credit}。一覧は scripts/uji_web_credits.json）。"
             "info.checked は事実情報を確認した日（各公式サイト、電車は乗換案内）。verified: false は公式で確認できなかったもの（宇治上神社の時間・寺田屋・鳥せい本店・御香宮の石庭）。このファイルは scripts/build_uji_data.py で作る。",
    "sections": [{"first": NO["ujieki"], "last": NO["omotesando"], "day": 0}, {"first": NO["tonoshima"], "last": NO["keihanuji"], "day": 1},
                 {"first": NO["chushojima"], "last": NO["torisei"], "day": 2}, {"first": NO["gekkeikan"], "last": NO["momoyama"], "day": 3}],
    "plan": {"_note": "「選んで回る」の設定。JR宇治駅は宇治の場所を選ぶと入る。京阪宇治駅は宇治と伏見の両方を選ぶと入る。中書島駅と伏見桃山駅は伏見の場所を選ぶと入る。最初は「全部回る」。",
             "picks": UJI + FUSHIMI,
             "auto": {str(NO["ujieki"]): {"any": UJI}, str(NO["keihanuji"]): {"any": UJI, "andAny": FUSHIMI},
                      str(NO["chushojima"]): {"any": FUSHIMI}, str(NO["momoyama"]): {"any": FUSHIMI}},
             "hints": [
                 H("ujieki", {"any": UJI, "none": FUSHIMI},
                   "宇治だけの日は、帰りもJR宇治駅から京都へ（約20分・240円）。祇園四条へは京阪宇治駅から中書島乗り換えで約32分・360円です。",
                   "Uji only? Go back from JR Uji to Kyoto (about 20 min, ¥240), or from Keihan Uji to Gion-Shijo via Chushojima (about 32 min, ¥360)."),
                 H("chushojima", {"any": FUSHIMI, "none": UJI},
                   "伏見だけの日は、京阪の祇園四条から特急で中書島へ約12分（320円）。月桂冠大倉記念館は9:30から、十石舟は10:00からなので、午前に来てもゆっくり回れます。",
                   "Fushimi only? Take the Keihan limited express from Gion-Shijo to Chushojima, about 12 minutes (¥320). The Gekkeikan museum opens at 9:30 and the boats start at 10:00, so a morning visit works too."),
                 H("mimuroto", {"any": [NO["mimuroto"]], "andAny": FUSHIMI},
                   "三室戸寺のあとは、京阪の三室戸駅（歩いて15分）から中書島へ。宇治駅へ戻らなくて大丈夫です。伏見に着くのが1時間半ほど遅くなるので、寺田屋（受付15:40まで）と月桂冠（受付16:00まで）のどちらかに絞りましょう。",
                   "After Mimurotoji, ride from Keihan Mimuroto Station (15 min on foot) to Chushojima; no need to return to Uji Station. You will reach Fushimi about 90 minutes later, so choose between Teradaya (last entry 15:40) and Gekkeikan (last entry 16:00)."),
                 H("koshoji", {"any": [NO["koshoji"]], "andAny": [NO["mimuroto"]]},
                   "興聖寺と三室戸寺の両方に寄ると、宇治だけで15時ごろになります。その日は伏見を別の日に。",
                   "With both Koshoji and Mimurotoji, Uji alone takes until about 15:00. Leave Fushimi for another day."),
             ]},
    "photoBase": "../images/uji/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
