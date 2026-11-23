#!/usr/bin/env python3
"""京都 宇治と伏見のデータを書き出す（2つのコース。2026-11-22 に時間割から作り直した）。

使い方: python3 scripts/build_uji_data.py  →  python3 scripts/sync_uji.py
- data/routes/uji.json        … 「9〜10時に出発」（三条 9:26発の京阪 → 京阪宇治 9:59）
- data/routes/uji-early.json  … 「開門に合わせる」（三条 7:49発の京阪 → 京阪宇治 8:22、平等院の8:45の開門へ）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- BASE がスポットごとの文章（コースに関係ない部分）、COURSES がコースごとの順番・時間・行き方
- 出発は京都の中心・三条のあたり（京阪の三条駅）。JR宇治駅はスポットから外した（文章の中で案内）
- 自分の写真は images/uji/<スポットのid>-<番号>.jpg を番号の順に全部使う
- ネットから借りた写真（Wikimedia Commons）は images/uji/<id>-w<番号>.jpg。撮影者とライセンスは scripts/uji_web_credits.json
- 電車の時刻は 2026-11-28（土）のダイヤ（Yahoo!路線情報で 2026-11-22 に確認）。平日（11-25）は三条 7:50→宇治 8:24、9:29→9:58
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "uji"
IMG = f"{R}/images/uji"
CHECKED = "2026-11-22"      # この日に公式サイト・乗換案内を見直した
CHECKED_21 = "2026-11-21"   # 前の日に確認して、今回は見直していないもの
CHECKED_23 = "2026-11-23"   # 「要確認」の調べ直しで、公式サイトをもう一度見たもの
BOAT_END = "2026-12-06"     # 十石舟の2026年の最終日
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


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def info(rows, source, tip=None, verified=True, cash=False, checked=CHECKED):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked, "source": source}
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
TRAIN_SRC = "Yahoo!路線情報（2026-11-28 土曜のダイヤ。平日は 2026-11-25 で確認）"
TRAIN_TIP = T("電車の時刻と運賃は乗換案内で確認しました（2026年11月28日・土曜のダイヤ）。平日は数分ずれます。乗る前にもう一度確かめてください。",
              "Train times and fares checked on a route planner (Saturday 28 November 2026 timetable). Weekday trains differ by a few minutes; please check again before you travel.")

# ───────── スポットごとの文章（コースに関係ない部分）。body のあとに、コースごとの行き方と時間が付く ─────────
BASE = dict(
    keihanuji=dict(
        name=T("京阪 宇治駅", "Keihan Uji Station"), kind=T("駅（スタート）", "Station (start)"),
        blurb=T("三条から京阪電車で、中書島で乗り換えて約35分。宇治橋の東のたもとの駅です。午後は同じ駅から伏見へ向かいます。",
                "About 35 minutes from Sanjo on the Keihan line, changing at Chushojima. The station sits at the east end of Uji Bridge; you leave for Fushimi from here in the afternoon."),
        lat=34.89387, lng=135.80698,
        body=T("京阪 宇治駅（けいはん うじえき）\n\n三条のあたりからは京阪電車がいちばん簡単です。三条駅で淀屋橋（よどやばし）方面行きに乗り、中書島（ちゅうしょじま）で宇治線に乗り換えて終点まで。運賃は400円です。丸いアーチを重ねたコンクリートの駅舎を出ると、目の前が宇治橋です。\n\n"
               "宇治には駅が2つあります。JRの宇治駅は川の向こうで、歩いて10分ほど離れています。京都駅の近くから来る人はJR奈良線で（京都9:34発のみやこ路快速で宇治9:51着、240円）。帰りにこのマップの順で伏見へ行くなら、乗るのは京阪のこの駅です。\n\n"
               "橋のたもとの「通圓（つうえん）」は、平安時代の終わりの創業と伝わるお茶屋さんです（10:30〜17:30）。午後、電車を待つあいだにお茶を買えます。",
               "Keihan Uji Station\n\nFrom the Sanjo area the Keihan line is the simplest way: board a train bound for Yodoyabashi at Sanjo, change to the Uji Line at Chushojima and ride to the end. The fare is ¥400. Step out of the concrete station of stacked round arches and Uji Bridge is right in front of you.\n\n"
               "Uji has two stations. JR Uji is across the river, about 10 minutes’ walk away. If you are staying near Kyoto Station, take the JR Nara Line instead (the 9:34 Miyakoji Rapid reaches Uji at 9:51, ¥240). To go on to Fushimi in the order of this map, you leave from this Keihan station.\n\n"
               "Tsuen, at the foot of the bridge, is a tea shop said to date from the end of the Heian period (10:30–17:30). You can buy tea there while you wait for your afternoon train."),
        gmaps=[gm("京阪 宇治駅", "Keihan Uji Station", 34.89387, 135.80698, "京阪宇治駅")],
        links=[YAHOO, link("official", "通圓（公式）", "Tsuen tea shop (official, Japanese)", "https://www.tsuentea.com/")],
        info=None),
    ujibashi=dict(
        name=T("宇治橋と紫式部像", "Uji Bridge & the Murasaki Shikibu statue"), kind=T("橋", "Bridge"),
        blurb=T("宇治川にかかる、木の欄干の橋。西のたもとに紫式部の像があり、ここから平等院表参道が始まります。",
                "The bridge over the Uji River with wooden railings. A statue of Murasaki Shikibu sits at its west end, where the approach to Byodoin begins."),
        lat=34.89228, lng=135.80589,
        body=T("宇治橋（うじばし）\n\n646年に初めて架けられたと伝わる、日本でも指折りの古い橋です。今の橋は1996年に架け替えられたもので、欄干はヒノキ。上流側に張り出した「三の間（さんのま）」は、豊臣秀吉がお茶の水を汲ませた場所と伝わります。\n\n"
               "京阪宇治駅を出たら、この橋を渡ります。橋の上から上流を見ると、川の中の島と朝霧橋の朱色、その奥の山。\n\n"
               "渡りきった西のたもとに、紫式部の像があります。源氏物語の最後の十帖が宇治を舞台にしていることにちなんだものです。その横の鳥居のある道が平等院表参道。平等院の表門まで、ここから歩いて5分ほどです。",
               "Uji Bridge\n\nSaid to have first been built in 646, this is one of the oldest bridge sites in Japan. The current bridge dates from 1996 and has cypress railings. The little platform jutting out upstream, the “San-no-ma”, is where Toyotomi Hideyoshi is said to have had water drawn for tea.\n\n"
               "You cross it as soon as you leave Keihan Uji Station. Look upstream for the islands, the vermilion Asagiri Bridge and the hills behind.\n\n"
               "At the far (west) end sits a statue of Murasaki Shikibu: the last ten chapters of The Tale of Genji are set in Uji. The lane with the torii beside her is Byodoin Omotesando, and Byodoin’s main gate is about 5 minutes’ walk along it."),
        gmaps=[gm("宇治橋（紫式部像）", "Uji Bridge (Murasaki Shikibu statue)", 34.89228, 135.80589, "紫式部像 宇治橋")],
        links=[link("info", "宇治市観光協会", "Uji City Tourist Association (Japanese)", "https://www.kyoto-uji-kankou.or.jp/")],
        info=info([row("hours", "いつでも渡れます", "Open at all times"),
                   row("fee", "無料", "Free")], "現地は自由に通れる橋", checked=CHECKED_21)),
    byodoin=dict(
        name=T("平等院 鳳凰堂", "Byodoin Temple (Phoenix Hall)"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
        caution=T("お堂の中に入る券は先着順。入ったらまず受付へ", "Interior tickets are first come, first served: go to that desk first"),
        blurb=T("10円玉の表のお堂。池の向こうに左右に翼を広げた姿を、正面から。中に入る券は先着順なので、入ったらまず受付へ。",
                "The hall on the ¥10 coin, spreading its wings across the pond. Tickets to go inside are first come, first served, so head to that desk first."),
        lat=34.88930, lng=135.80762,
        body=T("平等院（びょうどういん）\n\n1053年に藤原頼通が建てた阿弥陀堂が、今も池の中の島に建っています。10円玉の表の絵がこの鳳凰堂、1万円札の裏の鳳凰は屋根の上の鳳凰です。\n\n"
               "【写真を撮る場所】池（阿字池）をはさんだ正面の岸です。鳳凰堂は東を向いているので、午前は正面に日が当たり、午後は逆光ぎみになります。風のない朝は池にお堂が映ります。1枚目の写真は2025年2月の午後2時半ごろ、正面の岸から撮りました。\n\n"
               "お堂の中では、高さ約2.8mの阿弥陀如来坐像と、壁にかかる雲中供養菩薩像を目の前で見られます（中は撮影禁止）。券の時間まではミュージアム鳳翔館（9:00〜）へ。鳳凰の本物と、雲中供養菩薩像を間近で見られます。\n\n"
               "境内は飲食禁止で、ふたのないテイクアウトのカップは持ち込めません。抹茶ラテを買うなら出てからに。境内の茶房「藤花（とうか）」は10:00〜16:30（ラストオーダー16:00）、月・火・水曜が休み（祝日は営業）です。",
               "Byodoin\n\nThe Amida hall built by Fujiwara no Yorimichi in 1053 still stands on its island in the pond. It is the building on the ¥10 coin, and the phoenix on the back of the ¥10,000 note is the one on its roof.\n\n"
               "Where to take the photo: from the bank straight across the pond. The hall faces east, so the front is sunlit in the morning and backlit in the afternoon. On a still morning it is mirrored in the water. My first photo was taken from that bank at about 2:30 pm in February 2025.\n\n"
               "Inside you stand right in front of the 2.8-metre seated Amida and the small bodhisattvas on clouds along the walls (no photos inside). While you wait for your slot, see the Hoshokan museum (from 9:00): the original roof phoenixes and more of the cloud bodhisattvas up close.\n\n"
               "No eating or drinking in the grounds, and open takeaway cups are not allowed in, so buy your matcha latte afterwards. The Toka tea room inside the grounds is open 10:00–16:30 (last orders 16:00), closed Monday to Wednesday (open on holidays)."),
        gmaps=[gm("平等院", "Byodoin", 34.88930, 135.80762, "平等院")],
        links=[link("official", "平等院 公式サイト（拝観案内）", "Byodoin (official)", "https://www.byodoin.or.jp/guide/", "https://www.byodoin.or.jp/en/"),
               link("info", "鳳凰堂内部拝観について（待ち時間のめやす）", "Phoenix Hall interior visit (official, Japanese)", "https://www.byodoin.or.jp/guide/internal-view/")],
        notices=[notice("お堂の中に入る券は先着順", "Interior tickets: first come, first served",
                        "鳳凰堂の中に入るには、拝観券（700円）とは別に300円（現金のみ）。庭園の中の受付で、9:10から時間指定の券を配ります。20分ごとに35人で、なくなり次第終わりです。写真より先に受付へ行ってください。表門の拝観券はカード・電子マネー・コード決済も使えます。",
                        "Going inside the Phoenix Hall costs ¥300 (cash only) on top of the ¥700 ticket. Timed tickets are handed out from 9:10 at a desk inside the garden: 35 people every 20 minutes, until they run out. Go to the desk before you take photos. The main ticket can also be paid by card, e-money or QR code.",
                        url="https://www.byodoin.or.jp/guide/internal-view/"),
                 notice("紅葉の時期（12月6日まで）", "Autumn season (until 6 Dec)",
                        "11月13日〜12月6日は混み合います。11月28日・29日はミュージアムの映像展示が休み、11月28日・29日と12月5日・6日は御朱印が「鳳凰堂」の1種類だけです。ミュージアムの遺物コーナーは12月6日まで休み。夜間特別拝観は2026年秋はありません。",
                        "Very busy from 13 Nov to 6 Dec. On 28–29 Nov the museum’s video room is closed, and on 28–29 Nov and 5–6 Dec only the “Phoenix Hall” goshuin is given. The museum’s artefacts corner is closed until 6 Dec. There are no evening openings in autumn 2026.",
                        url="https://www.byodoin.or.jp/news/cat23/2022-1/", to="2026-12-06")],
        info=info([row("hours", "庭園 8:45〜17:30（受付17:15まで）。ミュージアム鳳翔館 9:00〜17:00（受付16:45まで）", "Garden 8:45–17:30 (last entry 17:15). Hoshokan museum 9:00–17:00 (last entry 16:45)"),
                   row("hours", "鳳凰堂内部拝観 9:30〜16:10、20分ごと・各回35人。受付は9:10から先着順（なくなり次第終了）", "Phoenix Hall interior 9:30–16:10, every 20 min, 35 people each. Tickets from 9:10, first come, first served"),
                   row("closed", "年中無休（法要や行事で内部拝観が休みの日があります）", "Open every day (interior visits are sometimes suspended for services)"),
                   row("fee", "大人700円、中高生400円、小学生300円（庭園とミュージアム）。鳳凰堂内部は別に300円", "Adults ¥700, junior/senior high ¥400, elementary ¥300 (garden and museum). Phoenix Hall interior ¥300 extra")],
                  "平等院 公式サイト（拝観案内）https://www.byodoin.or.jp/guide/ 、よくある質問 https://www.byodoin.or.jp/faq/public/ と https://www.byodoin.or.jp/faq/internal-view/ （再入場・支払い）、お知らせ https://www.byodoin.or.jp/news/cat23/20261016/ （定員35人・内部拝観券での再入場）、https://www.byodoin.or.jp/news/1/post-83/ （飲食）、https://www.byodoin.or.jp/news/cat23/2022-1/ （紅葉の時期）、https://www.byodoin.or.jp/news/cat23/post-97/ （夜間拝観の休止）。2026-11-23 に確認",
                  tip=T("時間・料金・内部拝観の決まりは平等院の公式サイトで確認しました。ふだんは再入場できませんが、内部拝観の券を持っていれば、表門の受付で見せて出入りできます（内部拝観のあとは不可）。京阪宇治駅から歩いて約10分、JR宇治駅からも約10分です。",
                        "Hours, fees and the interior-visit rules checked on the official Byodoin website. Re-entry is normally not allowed, but with an interior ticket you can go out and back in by showing it at the gate (not after your interior visit). About 10 minutes on foot from either Keihan Uji or JR Uji Station."),
                  checked=CHECKED_23)),
    omotesando=dict(
        name=T("平等院表参道と中村藤吉 平等院店", "Byodoin Omotesando & Nakamura Tokichi"), kind=T("お茶の通り・甘味", "Tea street & sweets"),
        caution=T("中村藤吉は予約できません", "Nakamura Tokichi takes no reservations"),
        blurb=T("お茶屋さんが並ぶ、ほうじ茶を炒る香りの通り。宇治川に面した中村藤吉で、抹茶のひと休みを。",
                "A lane of tea shops that smells of roasting hojicha. Stop for matcha at Nakamura Tokichi, overlooking the Uji River."),
        lat=34.89147, lng=135.80664,
        body=T("平等院表参道（びょうどういんおもてさんどう）\n\n宇治橋のたもとから平等院の表門まで約200m。古いお茶屋さんや抹茶のお菓子の店が並び、店先でほうじ茶を炒る香りがします。店が開くのは10時ごろからです。\n\n"
               "ひと休みは、通りの中ほどから宇治川のほうへ入った「中村藤吉（なかむらとうきち）平等院店」で。丸に十の字ののれんが目印です。カウンターで注文して自分で席へ運ぶ形で、窓の向こうは宇治川。写真の抹茶にソフトクリームをのせた一杯と、名物の生茶ゼリイを食べました（写真は2025年2月）。予約はできません。JR宇治駅の近くには本店もあります。\n\n"
               "通りの入口近くには、庭を眺められるスターバックス（京都宇治平等院表参道店）があります。8:00〜20:00で、この通りでは朝いちばんに開いている店です。",
               "Byodoin Omotesando\n\nAbout 200 metres from the foot of Uji Bridge to Byodoin’s main gate, lined with old tea merchants and matcha sweet shops; you can smell hojicha being roasted at the shopfronts. Shops start opening around 10:00.\n\n"
               "For a break, turn towards the river halfway along to Nakamura Tokichi Byodoin: look for the curtain with a cross in a circle. You order at the counter and carry your tray to a seat; the windows look onto the Uji River. I had the matcha topped with soft-serve in my photo and the “nama-cha jelly” (photos from February 2025). No reservations. The main shop is near JR Uji Station.\n\n"
               "Near the start of the lane there is also a Starbucks with a garden view, open 8:00–20:00: the first place on the street to open in the morning."),
        gmaps=[gm("中村藤吉 平等院店", "Nakamura Tokichi Byodoin", 34.89147, 135.80664, "中村藤吉 平等院店"),
               gm("平等院表参道", "Byodoin Omotesando", 34.89180, 135.80620, "平等院表参道")],
        links=[link("official", "中村藤吉 平等院店（公式）", "Nakamura Tokichi Byodoin (official, Japanese)", "https://tokichi.jp/pages/byodo-in-store-page"),
               link("official", "スターバックス 京都宇治平等院表参道店（公式）", "Starbucks Kyoto Uji Byodoin Omotesando (official, Japanese)", "https://store.starbucks.co.jp/detail-1443/")],
        info=info([row("hours", "中村藤吉 平等院店：銘茶売場・カフェ 10:00〜17:00（カフェのラストオーダー16:30）", "Nakamura Tokichi Byodoin: shop and café 10:00–17:00 (café last orders 16:30)"),
                   row("closed", "定休日なし（1月1日〜3日と臨時休業を除く）", "Open daily (except 1–3 January and occasional closures)"),
                   row("hours", "中村藤吉 平等院店：12月31日は10:00〜16:00（カフェのラストオーダー15:00）", "Nakamura Tokichi Byodoin: 31 Dec 10:00–16:00 (café last orders 15:00)", until="2026-12-31"),
                   row("hours", "スターバックス 京都宇治平等院表参道店：8:00〜20:00（不定休）", "Starbucks Kyoto Uji Byodoin Omotesando: 8:00–20:00 (irregular closures)")],
                  "中村藤吉 公式サイト https://tokichi.jp/pages/byodo-in-store-page とメニュー https://tokichi.jp/blogs/menu/byodoin （2026-11-23）、スターバックス公式の店舗ページ https://store.starbucks.co.jp/detail-1443/ （2026-11-22）",
                  tip=T("中村藤吉とスターバックスの公式サイトで確認しました。中村藤吉 平等院店はセルフ式のカフェで、公式サイトのメニュー（2026年11月）は抹茶のパフェやゼリイ、ソフトクリーム、お茶などの甘いものと飲み物だけです。食事は別の店で。混む日はラストオーダーより早く受付が終わることがあります。ほかの店の時間は店ごとに違います。",
                        "Checked on the official Nakamura Tokichi and Starbucks sites. Nakamura Tokichi Byodoin is a self-service café; its official menu (November 2026) lists only sweets and drinks, such as matcha parfaits, jelly, soft-serve and tea, so eat your meal elsewhere. On busy days it may stop taking guests before last orders. Other shops keep their own hours."),
                  checked=CHECKED_23)),
    tonoshima=dict(
        name=T("宇治川 塔の島と朝霧橋（夏の夜は鵜飼）", "Uji River: Tonoshima island & Asagiri Bridge"), kind=T("川・散歩", "River walk"),
        blurb=T("川の中の島に渡り、朱色の朝霧橋で向こう岸へ。夏の夜は、かがり火の下で鵜飼が見られます。",
                "Cross to the islands in the river, then over the vermilion Asagiri Bridge to the far bank. On summer nights, cormorant fishing by firelight."),
        lat=34.88900, lng=135.80930,
        body=T("宇治川（うじがわ）の塔の島・橘島と朝霧橋（あさぎりばし）\n\n平等院の南門を出るか、表参道から川沿いの「あじろぎの道」を上流へ歩くと、朱色の小さな喜撰橋（きせんばし）があります。渡った先が塔の島。高さ約15mの十三重石塔は鎌倉時代のものです。隣の橘島へ進み、朱色の朝霧橋を渡ると、宇治神社の鳥居の前に出ます。\n\n"
               "宇治川は流れが速く、水の色が濃い川です。島の岸には屋形船が並びます。平等院の前の人の多さから、ここで急に静かになります。ベンチがあるので、座って川を見るのにいい場所です。\n\n"
               "【夏の夜の鵜飼】7月1日〜9月30日（水曜休み）は、喜撰橋のたもとから鵜飼の船が出ます。乗合船は予約なしの当日受付で、17:30ごろから受付、7・8月は19:00、9月は18:30に出船。かがり火のすぐ近くまで船を寄せてくれます。後半の写真は2017年9月に乗合船から撮りました。岸からも見えます。\n\n"
               "鵜飼まで見る日は、順番を逆にして伏見を午前に回り、午後に宇治へ来てください（月桂冠大倉記念館は9:30から）。ただし平等院の内部拝観の券は、午後だとなくなっていることがあります。",
               "Tonoshima and Tachibana islands and Asagiri Bridge\n\nLeave Byodoin by the south gate, or walk upstream along the riverside path from Omotesando, to the little vermilion Kisen Bridge. It leads to Tonoshima island and its 15-metre, thirteen-storey stone pagoda from the Kamakura period. Continue to Tachibana island and cross the vermilion Asagiri Bridge to arrive in front of the torii of Uji Shrine.\n\n"
               "The Uji runs fast and deep green. Roofed pleasure boats are moored along the island. After the crowds in front of Byodoin it suddenly goes quiet here, and there are benches for sitting and watching the river.\n\n"
               "Cormorant fishing on summer nights: from 1 July to 30 September (not Wednesdays) boats leave from beside Kisen Bridge. Shared boats take no reservations; sign up on the day from about 17:30. Departure is 19:00 in July and August and 18:30 in September, and the boat takes you right up to the fire. My night photos were taken from a shared boat in September 2017. You can also watch from the bank.\n\n"
               "If you want to stay for it, reverse the day: Fushimi in the morning (the Gekkeikan museum opens at 9:30) and Uji in the afternoon. Note that Phoenix Hall interior tickets may be gone by then."),
        gmaps=[gm("塔の島（十三重石塔）", "Tonoshima (stone pagoda)", 34.88880, 135.80905, "宇治公園 塔の島 十三重石塔"),
               gm("朝霧橋", "Asagiri Bridge", 34.89021, 135.80941, "朝霧橋 宇治")],
        links=[link("official", "宇治川の鵜飼（宇治市観光協会）", "Uji River cormorant fishing (Uji tourist association, Japanese)", "https://www.kyoto-uji-kankou.or.jp/ukai.html")],
        info=info([row("hours", "島と橋はいつでも歩けます（無料）", "The islands and bridges are always open (free)"),
                   row("hours", "鵜飼：7月1日〜9月30日（水曜休み）。受付17:30ごろ〜、出船は7・8月19:00、9月18:30（約1時間）", "Cormorant fishing: 1 Jul – 30 Sep (not Wed). Sign-up from about 17:30; departs 19:00 in Jul–Aug, 18:30 in Sep (about 1 hour)"),
                   row("fee", "鵜飼の乗合船 大人2,700円、小学生1,200円（予約不可・定員になり次第終了）", "Shared cormorant boat: adults ¥2,700, elementary ¥1,200 (no reservations; closes when full)")],
                  "宇治市観光協会 https://www.kyoto-uji-kankou.or.jp/ukai.html （2026-11-23）",
                  tip=T("鵜飼の期間・時間・料金は宇治市観光協会の公式サイトで確認しました。荒天の日や、天ヶ瀬ダムの放流で川が増水した日は中止になることがあります。",
                        "Cormorant fishing dates, times and fares checked on the Uji tourist association website. It may be cancelled in stormy weather or when the Amagase dam releases water."),
                  checked=CHECKED_23)),
    koshoji=dict(
        name=T("興聖寺と琴坂", "Koshoji Temple & Kotozaka slope"), kind=T("寺（寄り道）", "Temple (detour)"),
        caution=T("拝観の受付は10:00〜16:00", "Reception 10:00–16:00"),
        blurb=T("もみじのトンネルになる参道「琴坂」の先の、静かな禅寺。朝霧橋から上流へ歩いて7分ほどの寄り道です。",
                "A quiet Zen temple at the top of Kotozaka, an approach that becomes a tunnel of maples. A 7-minute detour upstream from Asagiri Bridge."),
        lat=34.88946, lng=135.81340,
        body=T("興聖寺（こうしょうじ）\n\n朝霧橋を渡ったら、川沿いを上流（右）へ歩いて約7分。石の門から本堂の前の竜宮造りの門まで、ゆるい上り坂が200mほど続きます。両側の水路を流れる水の音が琴の音に聞こえることから「琴坂（ことざか）」。両側はもみじで、新緑の5月と紅葉の11月下旬がとくにきれいです。\n\n"
               "道元が開いた曹洞宗の寺を、江戸時代のはじめにこの地に再興した禅寺で、今も修行の場です。琴坂を歩くだけなら無料。本堂や庭を見る場合は受付で志納料を納めます。\n\n"
               "平等院のまわりに比べて人が少ないので、静かな場所が好きな人に。見たら同じ道を戻って、宇治神社へ。",
               "Koshoji\n\nAfter crossing Asagiri Bridge, walk upstream (right) along the river for about 7 minutes. From the stone gate a gentle slope climbs some 200 metres to the white Chinese-style gate before the main hall. The water running in the channels on both sides was said to sound like a koto, hence “Kotozaka”. Maples line both sides: best in the fresh green of May and the red of late November.\n\n"
               "A Soto Zen temple first founded by Dogen and re-established here in the early Edo period; monks still train here. Walking Kotozaka is free; to see the halls and garden, pay the donation at the reception.\n\n"
               "Fewer people come here than to Byodoin, so it suits anyone who likes quiet. Return the same way to Uji Shrine."),
        gmaps=[gm("興聖寺（琴坂）", "Koshoji (Kotozaka)", 34.88946, 135.81340, "興聖寺 宇治 琴坂")],
        links=[link("official", "興聖寺 公式サイト", "Koshoji (official)", "https://www.uji-koushouji.jp/access/", "https://www.uji-koushouji.jp/en/")],
        info=info([row("hours", "拝観の受付 10:00〜16:00（行事で入れない日があります）", "Reception 10:00–16:00 (closed to visitors during some events)"),
                   row("fee", "拝観志納料 500円（琴坂を歩くだけなら無料）", "Donation ¥500 (walking Kotozaka is free)")],
                  "興聖寺 公式サイト https://www.uji-koushouji.jp/access/ （2026-11-23）",
                  tip=T("時間と志納料は興聖寺の公式サイトで確認しました。公式サイトでは、京阪宇治駅から歩いて約20分です。", "Hours and donation checked on the official Koshoji website, which gives about 20 minutes on foot from Keihan Uji Station."),
                  checked=CHECKED_23)),
    ujigami=dict(
        name=T("宇治上神社と宇治神社", "Ujigami Shrine & Uji Shrine"), kind=T("神社（世界遺産）", "Shrines (World Heritage)"),
        caution=T("宇治上神社の閉門の時間は公式で確かめられませんでした（要確認）。夕方前に", "Ujigami Shrine’s closing time could not be confirmed officially (unconfirmed). Go before late afternoon"),
        blurb=T("朝霧橋を渡ると宇治神社、その奥に世界遺産の宇治上神社。日本でいちばん古い神社の建物が、木立の中に残っています。",
                "Across Asagiri Bridge is Uji Shrine, and behind it World Heritage Ujigami Shrine, with the oldest shrine building in Japan among the trees."),
        lat=34.89205, lng=135.81146,
        body=T("宇治神社（うじじんじゃ）と宇治上神社（うじかみじんじゃ）\n\n朝霧橋を渡った正面の鳥居が宇治神社。石段の上の朱色の門の奥に、鎌倉時代の本殿（重要文化財）があります。道に迷った祭神を兎が振り返りながら案内したという言い伝えから、境内のあちこちに「みかえり兎」がいます。\n\n"
               "宇治神社の横の「さわらびの道」を2分ほど上ると、朱色の鳥居の先が宇治上神社です。平等院と同じく世界遺産。手前の拝殿は鎌倉時代、奥の本殿は平安時代の後期に建てられた、今残っている中で日本でいちばん古い神社の建物で、どちらも国宝です。本殿は覆いの建物の中に、3つの小さな社が並んでいます。格子ごしにのぞいてみてください。\n\n"
               "色を塗っていない木の建物で、平等院の華やかさとは反対の静けさがあります。境内は小さく、15分ほどで見られます。境内に湧く「桐原水（きりはらすい）」は宇治七名水のうち今も残るただ1つです。\n\n"
               "ここから京阪宇治駅までは、さわらびの道を歩いて約8分。途中に源氏物語ミュージアムがあります。",
               "Uji Shrine and Ujigami Shrine\n\nThe torii straight ahead as you come off Asagiri Bridge is Uji Shrine. Up the steps, behind the vermilion gate, stands a Kamakura-period main hall (Important Cultural Property). Legend says a rabbit led the lost deity here, looking back to check he was following, so “looking-back rabbits” are all over the grounds.\n\n"
               "Two minutes up the Sawarabi path beside it, through a vermilion torii, is Ujigami Shrine, World Heritage like Byodoin. The worship hall in front is Kamakura period; the main hall behind it, from the late Heian period, is the oldest surviving shrine building in Japan. Both are National Treasures. The main hall is three small shrines side by side inside a sheltering building: peer through the lattice.\n\n"
               "The wood is unpainted, and the mood is the opposite of Byodoin’s splendour. The grounds are small; 15 minutes is enough. The Kirihara spring in the grounds is the only one left of Uji’s seven famous waters.\n\n"
               "From here it is about 8 minutes along the Sawarabi path to Keihan Uji Station, passing the Tale of Genji Museum."),
        gmaps=[gm("宇治上神社", "Ujigami Shrine", 34.89205, 135.81146, "宇治上神社"),
               gm("宇治神社", "Uji Shrine", 34.89085, 135.81042, "宇治神社")],
        links=[link("official", "宇治神社 公式サイト", "Uji Shrine (official, Japanese)", "https://uji-jinja.com/")],
        info=info([row("hours", "宇治上神社：公式で確かめられませんでした（要確認）。宇治神社の境内は自由", "Ujigami Shrine: could not be confirmed officially (unconfirmed). Uji Shrine grounds are open"),
                   row("fee", "どちらも無料", "Both free")],
                  "宇治上神社には公式サイトがなく、宇治市観光協会 https://www.kyoto-uji-kankou.or.jp/tourism.html にも時間の記載なし。旅行ガイドでは閉門の時間が分かれるので、時間はページに出さない。京都府の冊子 https://www.pref.kyoto.jp/kyotoyamashiro/pdf/p4_5.pdf は2014年ごろの古い冊子なので時間の出典にしない（拝観無料はこの冊子による）（2026-11-23）",
                  tip=T("宇治上神社の時間は公式の案内で確かめられませんでした（門が閉まる時間は案内によって違います）。午後遅くに行く日は、早めに着くか電話（0774-21-4634）で確かめてください。写真の鳥居と朱色の門は2017年6月。",
                        "Ujigami Shrine’s hours could not be confirmed from an official source (guides disagree on the closing time), so arrive early or phone ahead (0774-21-4634) if you go late in the afternoon. The torii and vermilion gate photos are from June 2017."),
                  verified=False, checked=CHECKED_23)),
    mimuroto=dict(
        name=T("三室戸寺", "Mimurotoji Temple"), kind=T("花の寺（寄り道）", "Flower temple (detour)"),
        caution=T("拝観は15:10まで。花は4月下旬〜7月上旬", "Open until 15:10. Flowers late April to early July"),
        blurb=T("6月に2万株のあじさいが咲く花の寺。宇治上神社から歩いて25分ほどかかるので、花の時期に時間をとって。",
                "The flower temple, with 20,000 hydrangeas in June. It is a 25-minute walk from Ujigami Shrine, so make time for it in the flower season."),
        lat=34.89978, lng=135.81870,
        body=T("三室戸寺（みむろとじ）\n\n西国三十三所の第十番札所。山すその広い庭に、春はつつじ（4月下旬〜5月中旬）、6月はあじさい、夏は本堂の前の蓮と、花が続きます。いちばんの見ごろはあじさいで、杉木立の下に約2万株。公式サイトの2027年の案内では、あじさい園の公開は5月29日〜7月4日です。\n\n"
               "花のない時期は、正直なところ遠回りになります。行くなら4月下旬〜7月上旬に。\n\n"
               "宇治上神社からは、源氏物語ミュージアムの前を通って歩いて約25分。帰りは京阪の三室戸駅まで歩いて15分で、そこから中書島へ（14分・320円）。宇治駅へ戻る必要はありません。\n\n"
               "拝観時間は15:10までと早く、6月の土日は混みます。気象警報が出ている日は拝観できません。境内は飲食禁止、三脚も使えません。",
               "Mimurotoji\n\nTemple no. 10 of the Saigoku Kannon pilgrimage. Its big garden at the foot of the hills flowers in turn: azaleas (late April to mid May), hydrangeas in June, then lotuses in front of the main hall in summer. The hydrangeas are the highlight: about 20,000 plants under tall cedars. The official site lists the 2027 hydrangea garden as open 29 May – 4 July.\n\n"
               "Outside the flower seasons it is honestly a long detour; come between late April and early July.\n\n"
               "From Ujigami Shrine it is about 25 minutes on foot, past the Tale of Genji Museum. Afterwards walk 15 minutes to Keihan Mimuroto Station and ride to Chushojima (14 min, ¥320); no need to go back to Uji Station.\n\n"
               "Visiting hours end as early as 15:10, and June weekends are crowded. The temple closes to visitors when a weather warning is in force. No eating or drinking, and no tripods."),
        gmaps=[gm("三室戸寺", "Mimurotoji", 34.89978, 135.81870, "三室戸寺"),
               gm("京阪 三室戸駅", "Keihan Mimuroto Station", 34.89886, 135.80634, "三室戸駅")],
        links=[link("official", "三室戸寺 公式サイト（拝観のご案内）", "Mimurotoji (official, Japanese)", "https://www.mimurotoji.com/guide/index.html")],
        info=info([row("hours", "8:30〜15:10（あじさい園の期間は16:00に完全閉門との案内）", "8:30–15:10 (during the hydrangea season the gate fully closes at 16:00)"),
                   row("closed", "8月11日〜17日、12月29日〜31日。気象警報が出ている日も拝観できません", "11–17 August, 29–31 December, and whenever a weather warning is in force"),
                   row("fee", "大人1,000円、小人500円", "Adults ¥1,000, children ¥500"),
                   row("train", "京阪 三室戸駅から歩いて15分。三室戸 → 中書島 14分・320円", "15 min on foot from Keihan Mimuroto Station. Mimuroto → Chushojima 14 min, ¥320")],
                  "三室戸寺 公式サイト https://www.mimurotoji.com/guide/index.html とあじさい園 https://www.mimurotoji.com/event/hydrangea.html （2026-11-23）。三室戸→中書島は乗換案内（2026-11-21）",
                  tip=T("時間・料金・休みは三室戸寺の公式サイトで確認しました。花の見ごろは年によって前後します。", "Hours, fees and closed days checked on the official Mimurotoji website. Flowering times vary from year to year."),
                  checked=CHECKED_23)),
    chushojima=dict(
        name=T("京阪 中書島駅", "Keihan Chushojima Station"), kind=T("駅", "Station"),
        blurb=T("伏見の酒蔵の町の入口。月桂冠大倉記念館へ歩いて5分、寺田屋へ7分です。",
                "The gateway to Fushimi’s sake district: 5 minutes on foot to the Gekkeikan museum, 7 to Teradaya."),
        lat=34.92689, lng=135.76007,
        body=T("京阪 中書島駅（ちゅうしょじまえき）\n\n宇治線の終点で、京阪本線との乗り換え駅です。北口を出て、まっすぐ北へ歩くと酒蔵の町に入ります。\n\n"
               "伏見は、京都と大阪を結ぶ川の港として栄えた町です。地下水がよく、今も20近い蔵元が酒を造っています。歩くエリアは中書島駅から伏見桃山駅まで、南北に800mほど。帰りは北の伏見桃山駅から乗るので、ここへは戻りません。\n\n"
               "伏見だけに来る日は、三条から京阪の特急で中書島まで13分（320円）です。",
               "Keihan Chushojima Station\n\nThe end of the Uji Line and the junction with the Keihan Main Line. Leave by the north exit and walk straight north into the brewery quarter.\n\n"
               "Fushimi grew rich as the river port between Kyoto and Osaka. Its groundwater is good, and nearly twenty breweries still make sake here. The walking area runs about 800 metres north from Chushojima to Fushimi-Momoyama Station; you leave from the latter, so you won’t come back here.\n\n"
               "Coming only to Fushimi? The Keihan limited express from Sanjo takes 13 minutes to Chushojima (¥320)."),
        gmaps=[gm("中書島駅", "Chushojima Station", 34.92689, 135.76007, "中書島駅")],
        links=[YAHOO],
        info=None),
    teradaya=dict(
        name=T("寺田屋", "Teradaya Inn"), kind=T("史跡", "Historic inn"),
        caution=T("時間と料金は公式で確かめられませんでした（要確認）", "Hours and fee could not be confirmed officially (unconfirmed)"),
        blurb=T("坂本龍馬が襲われた船宿。川べりに建つ2階建ての旅籠で、中を見学できます。",
                "The riverside boat inn where Sakamoto Ryoma was attacked. You can go inside the two-storey building."),
        lat=34.93029, lng=135.75956,
        body=T("寺田屋（てらだや）\n\n大阪へ下る三十石船の客が泊まった船宿です。1866年、ここに泊まっていた坂本龍馬が幕府の役人に襲われ、のちに妻となるお龍の知らせで逃げのびた「寺田屋事件」で知られます。\n\n"
               "中には龍馬ゆかりの品や写真が並びます。今の建物は、幕末の戦いで焼けたあとに建て直されたものとされています。そのつもりで見ると、かえって船宿の造りそのものを楽しめます。\n\n"
               "中に入らなくても、外から見る格子の2階建てと提灯、隣の庭の龍馬像だけで雰囲気は十分。すぐ前の川が十石舟の通る宇治川派流です。ここから北へ延びる「竜馬通り商店街」を歩くと、鳥せい本店まで約5分です。",
               "Teradaya\n\nA boat inn for passengers on the river boats to Osaka. It is known for the Teradaya incident of 1866, when Sakamoto Ryoma, staying here, was attacked by shogunate officers and escaped thanks to a warning from Oryo, later his wife.\n\n"
               "Inside are mementoes and photographs. The present building is thought to have been rebuilt after the original burned in the fighting of 1868; knowing that, you can simply enjoy it as a boat inn.\n\n"
               "Even without going in, the latticed two-storey front with its lanterns and the Ryoma statue in the garden next door give you the feel. The canal in front is the one the jikkokubune boats use. From here the Ryoma-dori shopping street leads north; Torisei is about 5 minutes away."),
        gmaps=[gm("寺田屋", "Teradaya", 34.93029, 135.75956, "寺田屋 伏見")],
        links=[],
        info=info([row("hours", "公式で確かめられませんでした（要確認）", "Could not be confirmed officially (unconfirmed)"),
                   row("closed", "月曜に休みがあるとの案内（要確認）", "Guides say it closes on some Mondays (unconfirmed)"),
                   row("fee", "公式で確かめられませんでした（要確認）", "Could not be confirmed officially (unconfirmed)")],
                  "寺田屋には公式サイトがなく、時間と料金の公式の案内は見つからない。旅行ガイドどうしでも料金が分かれるので、時間と料金はページに出さない（2026-11-23）",
                  tip=T("寺田屋には公式サイトがなく、時間と料金を公式の案内で確かめられませんでした。夕方は早めに閉まるとの案内が多いので、伏見に着いたら先に寄り、行く前に電話（075-622-0243）で確かめると安心です。中書島駅から歩いて約7分。",
                        "Teradaya has no official website, so its hours and fee could not be confirmed. Guides say it closes fairly early in the afternoon, so go there first when you reach Fushimi, and phone ahead (075-622-0243) to be sure. About 7 minutes on foot from Chushojima Station."),
                  verified=False, cash=True, checked=CHECKED_23)),
    torisei=dict(
        name=T("鳥せい本店", "Torisei Honten"), kind=T("焼き鳥と蔵出しの酒", "Chicken & brewery sake"),
        caution=T("月曜休み。電子マネーは使えません", "Closed Mondays. No e-money"),
        blurb=T("蔵元「神聖」の酒蔵を使った鳥料理の店。鳥めしや焼き鳥と、蔵出しの生原酒を。",
                "Chicken dishes in a converted storehouse of the Shinsei brewery, with unpasteurised sake straight from the brewery."),
        lat=34.93108, lng=135.76207,
        body=T("鳥せい本店（とりせいほんてん）\n\n1677年創業の蔵元、山本本家（銘柄は「神聖」）の酒蔵を改装した鳥料理の店です。白い壁に「鳥せい」の看板、「蔵元直営」の紺ののれんが目印。中は太い梁の広い土間で、ひとりでも入りやすい店です。\n\n"
               "お昼は鳥めしや焼き鳥の御膳が手ごろ。写真は2025年2月のお昼に食べたものです。お酒が飲める人は、蔵元ならではの蔵出しの生原酒を一杯。\n\n"
               "店の横には、酒造りに使う伏見の名水「白菊水（しらぎくすい）」が湧いていて、地元の人が汲みに来ます。",
               "Torisei Honten\n\nA chicken restaurant in a converted storehouse of Yamamoto Honke, brewers of “Shinsei” sake since 1677. Look for the white wall with the 鳥せい sign and the navy curtain. Inside is a big earthen-floored hall under heavy beams, easy to enter alone.\n\n"
               "At lunch the chicken-rice and yakitori sets are good value; my photo is a lunch from February 2025. If you drink, try a glass of the brewery’s unpasteurised sake.\n\n"
               "Beside the restaurant the Shiragiku spring, one of Fushimi’s brewing waters, flows freely; locals come to fill bottles."),
        gmaps=[gm("鳥せい本店", "Torisei Honten", 34.93108, 135.76207, "鳥せい本店 伏見")],
        links=[link("official", "鳥せい本店（公式）", "Torisei Honten (official, Japanese)", "https://www.torisei.com/honten/")],
        info=info([row("hours", "11:00〜22:00（ラストオーダー21:30）。昼から夜まで通しで営業", "11:00–22:00 (last orders 21:30), open straight through the afternoon"),
                   row("closed", "月曜、12月31日〜1月3日", "Mondays, 31 December – 3 January"),
                   row("fee", "支払いはカード可（VISA・Master・JCB・AMEX・Diners）。電子マネーは使えません", "Payment: cards accepted (Visa, Mastercard, JCB, AMEX, Diners); no e-money")],
                  "鳥せい 公式サイト（本店のページ）https://www.torisei.com/honten/ （2026-11-23）",
                  tip=T("時間・休み・支払いは鳥せいの公式サイトで確認しました。祝日の月曜に開くかどうかは公式サイトに書かれていないので、その日は電話（075-622-5533、営業時間内）で確かめてください。伏見桃山駅から歩いて約7分。",
                        "Hours, closed days and payment checked on the official Torisei website. It does not say whether the shop opens on a Monday that is a public holiday; if so, phone first (075-622-5533, during opening hours). About 7 minutes on foot from Fushimi-Momoyama Station."),
                  checked=CHECKED_23)),
    gekkeikan=dict(
        name=T("月桂冠大倉記念館", "Gekkeikan Okura Sake Museum"), kind=T("酒の博物館・きき酒", "Sake museum & tasting"),
        caution=T("現金は使えません。受付は16:00まで", "No cash. Last entry 16:00"),
        blurb=T("1637年創業の月桂冠の酒蔵を使った博物館。最後に、コイン3枚で好きな酒を3種類きき酒できます。現金は使えません。",
                "A museum in the old storehouses of Gekkeikan, founded 1637. At the end, three coins buy three tastings of your choice. No cash accepted."),
        lat=34.92888, lng=135.76163,
        body=T("月桂冠大倉記念館（げっけいかんおおくらきねんかん）\n\n白壁と焼杉板の酒蔵が並ぶ、伏見らしい一角にあります。入ると、おみやげのおちょことコインを3枚もらえます。昔の酒造りの道具を見たあと、きき酒処へ。約10種類の酒が機械に並んでいて、コインを1枚入れてボタンを押すと1杯分が出てきます。\n\n"
               "【きき酒のこつ】ボタンは軽く1回押すだけ（自動で止まります）。大吟醸のような香りの軽いものから先に、古酒や梅酒のような味の濃いものはあとに。水も置いてあるので、あいだに飲みましょう。おちょこは持ち帰れます。空腹だとすぐ回るので、何か食べてからに。\n\n"
               "【予約】公式サイトで2週間前の9:30から前日16:30まで予約できます（先着順）。予約なしでも当日の枠で入れることがありますが、混む日は待つか、入れないこともあります。土日や桜・紅葉の時期は予約を。\n\n"
               "写真は2025年2月。建物の裏の川沿いが十石舟の乗り場です。",
               "Gekkeikan Okura Sake Museum\n\nIt stands in the most Fushimi-like corner of town, among white-plastered, charred-cedar storehouses. On entry you receive a souvenir sake cup and three coins. After the old brewing tools, go to the tasting room: about ten sakes sit in dispensers; put in a coin, press the button, and one serving comes out.\n\n"
               "Tasting tips: press the button once, lightly (it stops by itself). Start with light, fragrant ones such as daiginjo and leave the strong-flavoured aged sake or plum wine for last. Water is provided; drink some between cups. The cup is yours to keep. Sake hits fast on an empty stomach, so eat something first.\n\n"
               "Booking: you can reserve on the official site from 9:30 two weeks ahead until 16:30 the day before (first come, first served). Walk-ins may get a same-day slot, but on busy days you may wait or be turned away; book for weekends and the cherry and maple seasons.\n\n"
               "Photos from February 2025. The boarding place for the jikkokubune is on the canal behind the building."),
        gmaps=[gm("月桂冠大倉記念館", "Gekkeikan Okura Sake Museum", 34.92888, 135.76163, "月桂冠大倉記念館")],
        links=[link("official", "月桂冠大倉記念館（ご見学案内・予約）", "Gekkeikan Okura Sake Museum (official)", "https://www.gekkeikan.co.jp/enjoy/museum/access/")],
        notices=[notice("現金は使えません", "No cash",
                        "入館料・売店・追加のきき酒コインは、すべてキャッシュレス決済だけです。クレジットカード、電子マネー、スマホのコード決済のどれかを用意してください。",
                        "Admission, the shop and extra tasting coins are all cashless only. Bring a credit card, e-money or a QR payment app.",
                        url="https://www.gekkeikan.co.jp/enjoy/museum/access/"),
                 notice("きき酒ができない人", "Who cannot taste",
                        "20歳未満の人、車・バイク・自転車で来た人、妊娠中・授乳中の人はきき酒ができません。",
                        "No tasting for anyone under 20, anyone who came by car, motorbike or bicycle, or anyone pregnant or nursing.",
                        url="https://www.gekkeikan.co.jp/enjoy/museum/access/")],
        info=info([row("hours", "9:30〜16:30（受付16:00まで）。見学は40〜60分", "9:30–16:30 (last entry 16:00). Allow 40–60 minutes"),
                   row("closed", "8月13日〜16日、12月28日〜1月4日、ほかに臨時休館あり", "13–16 August, 28 December – 4 January, plus occasional closures"),
                   row("fee", "20歳以上600円（きき酒3種類とおみやげ付き）、13〜19歳100円、12歳以下無料", "Ages 20+ ¥600 (three tastings and a souvenir), 13–19 ¥100, 12 and under free")],
                  "月桂冠 公式サイト https://www.gekkeikan.co.jp/enjoy/museum/access/ （2026-11-22）",
                  tip=T("月桂冠の公式サイトで確認しました。臨時休館や時間の変更は公式サイトに出ます（2026年11月も数日ありました）。中書島駅から歩いて5分、伏見桃山駅から10分です。",
                        "Checked on the official Gekkeikan website, which also announces occasional closures and shortened hours (there were a few in November 2026). 5 minutes on foot from Chushojima, 10 from Fushimi-Momoyama."))),
    jikkoku=dict(
        name=T("十石舟と酒蔵の町並み", "Jikkokubune boat & the brewery canal"), kind=T("遊覧船・川沿いの散歩", "Canal boat & riverside walk"),
        caution=T("舟は3月下旬〜12月上旬だけ。冬は運休", "Boats late March to early December only; none in winter"),
        blurb=T("柳と酒蔵の白壁の下を、小さな屋形船で約55分。春から秋だけの運航です。冬は川沿いを歩きます。",
                "About 55 minutes in a small roofed boat under willows and white brewery walls. Spring to autumn only; in winter, walk the bank."),
        lat=34.92850, lng=135.76130,
        body=T("十石舟（じっこくぶね）\n\n月桂冠大倉記念館の裏、川に下りた所が乗り場です。江戸時代に酒や米、旅人を運んだ舟を再現した20人乗りの屋形船で、柳の並ぶ宇治川派流を下り、三栖閘門（みすこうもん）でいったん降りて資料館を見てから戻ります。全部で約55分。舟の上では飲食できません。\n\n"
               "川から見上げる酒蔵の焼杉の壁と柳が、伏見でいちばん絵になる景色です。舟に乗らなくても、乗り場のあたりから弁天橋まで川沿いを歩けば同じ景色が見られます（歩くだけなら20分ほど）。桜の時期（3月末〜4月上旬）と、あじさいの6月がとくにきれいです。\n\n"
               "【乗り方】空席があれば予約なしで乗れます。便は10:00〜11:20と13:00〜16:20の20分おきで、11:40〜12:40は出ません。受付は出航の15分前（3〜5月は20分前）まで。記念館に入る前に乗り場で空席を聞いて、便を決めておくと安心です。支払いは乗り場で現金。桜の時期や土日は、公式サイトからネット予約を（乗る日の2日前の0時まで。3〜4月の予約はカード払いだけで、30日前の22時から）。\n\n"
               "2026年は12月6日まで（11月25日からは最終便が15:40）。冬は川の工事のため運休で、例年3月下旬に再開します。",
               "Jikkokubune\n\nThe landing is down on the canal behind the Gekkeikan museum. The 20-seat roofed boat recreates the craft that carried sake, rice and travellers in the Edo period. It glides down the willow-lined canal to the Misu lock gate, where you get off to see a small museum, then returns: about 55 minutes in all. No eating or drinking on board.\n\n"
               "The charred-cedar brewery walls and willows seen from the water are Fushimi’s most photogenic view. Without the boat, you get the same view walking the bank from the landing to Benten Bridge (about 20 minutes just walking). It is at its best in cherry season (late March to early April) and with the hydrangeas in June.\n\n"
               "How to ride: if there are seats you can board without a reservation. Boats leave every 20 minutes from 10:00 to 11:20 and from 13:00 to 16:20; there are none from 11:40 to 12:40. Check in at least 15 minutes before departure (20 minutes in March–May). It is safest to ask at the landing and fix your boat before you go into the museum. Pay in cash at the landing. In cherry season and at weekends, book online on the official site (until midnight two days before; March–April bookings open 30 days ahead at 22:00 and are card-only).\n\n"
               "In 2026 the boats run until 6 December (last boat 15:40 from 25 November). They stop in winter for river works and usually restart in late March."),
        gmaps=[gm("十石舟のりば", "Jikkokubune landing", 34.92850, 135.76130, "伏見十石舟 乗船場")],
        links=[link("official", "十石舟（伏見観光協会・予約）", "Jikkokubune (Fushimi tourist association, Japanese)", "https://kyoto-fushimi.or.jp/fune"),
               link("info", "伏見十石舟（京都観光Navi）", "Fushimi Jikkokubune (Kyoto City official guide, Japanese)", "https://ja.kyoto.travel/event/single.php?event_id=4100")],
        notices=[notice("冬は運休", "No boats in winter",
                        "12月中旬から3月中旬は運休です。この時間は川沿いを弁天橋まで歩いて、残りは御香宮神社へ。2027年の運航日は伏見観光協会のサイトで確かめてください。",
                        "No boats from mid December to mid March. Use this slot to walk the bank to Benten Bridge, then go on to Gokonomiya Shrine. Check the Fushimi tourist association site for the 2027 season.",
                        url="https://kyoto-fushimi.or.jp/fune", frm="2026-12-07", to="2027-03-19")],
        info=info([row("hours", "2026年：3月20日〜12月6日（8月は1日〜11日だけ）", "2026: 20 Mar – 6 Dec (in August, only 1–11 Aug)", until=BOAT_END),
                   row("hours", "出航 10:00・10:20・10:40・11:00・11:20、13:00〜16:20の20分おき（11月25日〜12月6日は15:40が最終）。約55分", "Departures 10:00, 10:20, 10:40, 11:00, 11:20, then every 20 min from 13:00 to 16:20 (last boat 15:40 from 25 Nov to 6 Dec). About 55 min", until=BOAT_END),
                   row("closed", "月曜（祝日は運航。4・5・10・11月は月曜も運航）、8月12日〜31日、冬（12月中旬〜3月中旬）", "Mondays (runs on holidays, and on Mondays in Apr, May, Oct, Nov), 12–31 August, winter (mid Dec – mid Mar)"),
                   row("fee", "大人（中学生以上）1,900円、小学生900円。乗り場で当日現金（3〜4月のネット予約はカード払い）", "Adults (junior high and up) ¥1,900, elementary ¥900. Cash at the landing on the day (March–April online bookings are paid by card)")],
                  "伏見観光協会 今年の運航 https://kyoto-fushimi.or.jp/fune/unkou/ （運航期間・出航時刻・料金）、予約の前に https://kyoto-fushimi.or.jp/fune/reserve.php （支払い・受付・予約の締め切り）、十石舟 https://kyoto-fushimi.or.jp/fune （2026-11-23）。京都観光Navi https://ja.kyoto.travel/event/single.php?event_id=4100 （2026-11-22）",
                  tip=T("運航日・出航時刻・料金・支払い方法は伏見観光協会のサイトで確認しました。予約なしで乗るときは、乗り場で当日現金で払います。出航時刻は天気や川の様子で変わることがあります。",
                        "Dates, departure times, fares and payment checked on the Fushimi tourist association site. Without a booking you pay in cash at the landing on the day. Sailings can change with the weather and river conditions."),
                  checked=CHECKED_23)),
    gokonomiya=dict(
        name=T("御香宮神社", "Gokonomiya Shrine"), kind=T("神社（寄り道）", "Shrine (detour)"),
        blurb=T("伏見の酒を育てた水の神社。境内に湧く「御香水」は名水百選で、表門は伏見城の門を移したものです。",
                "The shrine of the water behind Fushimi’s sake. Its spring is one of Japan’s 100 famous waters, and its gate came from Fushimi Castle."),
        lat=34.93523, lng=135.76722,
        body=T("御香宮神社（ごこうのみやじんじゃ）\n\n伏見桃山駅から大手筋を東へ、線路を2本越えて歩いて約6分。平安時代に境内から香りのよい水が湧いたことが名前の由来で、今も本殿の横に「御香水（ごこうすい）」が湧いています（水を汲めるのは7:00〜19:00）。伏見の酒がこの地下水で造られていることを、ここで実感できます。\n\n"
               "通りに面した表門は伏見城の大手門を移したもの。拝殿の正面の、極彩色の彫刻も見どころです。\n\n"
               "境内は自由に入れます。社務所の裏には小堀遠州ゆかりと伝わる石庭があります（入れる時間と料金は公式で確かめられませんでした。要確認）。舟に乗らない日や、時間が余ったときの寄り道に。冬は17時ごろには暗くなるので、その前に。",
               "Gokonomiya Shrine\n\nFrom Fushimi-Momoyama Station walk east along Otesuji, over two railway lines, for about 6 minutes. The name comes from a fragrant spring that appeared here in the Heian period, and the “Gokosui” water still flows beside the main hall (water can be drawn 7:00–19:00). Here you can see for yourself the groundwater Fushimi’s sake is made from.\n\n"
               "The front gate on the street was moved from Fushimi Castle. The brightly painted carvings on the front of the worship hall are worth a look too.\n\n"
               "The grounds are free to enter. Behind the shrine office is a stone garden said to be linked to Kobori Enshu (its hours and fee could not be confirmed officially). A good detour on days without the boat or when you have time left. In winter it is dark by about 17:00, so go before then."),
        gmaps=[gm("御香宮神社", "Gokonomiya Shrine", 34.93523, 135.76722, "御香宮神社")],
        links=[link("official", "御香宮神社 公式サイト", "Gokonomiya Shrine (official, Japanese)", "https://gokounomiya.kyoto.jp/")],
        info=info([row("hours", "境内は自由。御香水を汲めるのは7:00〜19:00、社務所は9:00〜16:00。石庭の時間は公式で確かめられませんでした（要確認）", "Grounds open. Spring water 7:00–19:00, shrine office 9:00–16:00. Stone garden hours could not be confirmed officially (unconfirmed)"),
                   row("fee", "境内は無料。石庭の料金は公式で確かめられませんでした（要確認）", "Grounds free. The stone garden’s fee could not be confirmed officially (unconfirmed)")],
                  "御香宮神社 公式サイト https://gokounomiya.kyoto.jp/ と境内案内 https://gokounomiya.kyoto.jp/grounds/grounds.html （2026-11-23。御香水と社務所の時間、駅からの時間は記載あり。石庭は境内図に名前があるだけで、料金と時間は記載なし）",
                  tip=T("御香水と社務所の時間は公式サイトで確認しました。石庭の料金と時間は公式サイトに書かれていませんでした。", "Spring and office hours checked on the official website. The stone garden’s fee and hours are not given there."),
                  verified=False, checked=CHECKED_23)),
    kizakura=dict(
        name=T("キザクラカッパカントリー", "Kizakura Kappa Country"), kind=T("地ビールと日本酒・夜ごはん", "Craft beer, sake & dinner"),
        caution=T("火曜休み。14:30〜17:00は閉まります", "Closed Tuesdays, and 14:30–17:00 every day"),
        blurb=T("カッパの絵で知られる黄桜の直営店。京都で最初の地ビールを、酒蔵の中のレストランで。夜は21:30まで開いています。",
                "The brewery restaurant of Kizakura, known for its kappa cartoons, with Kyoto’s first craft beer on tap in an old storehouse. Open until 21:30."),
        lat=34.93083, lng=135.76050,
        body=T("キザクラカッパカントリー\n\n黄桜（きざくら）の酒蔵を使った店で、レストラン「黄桜酒場」と売店、カッパの資料を集めたギャラリーがあります。黄桜は1995年に京都で最初の地ビールを造った蔵で、できたての京都麦酒を飲めるのがここです。売店には缶ビールや限定の酒が並びます（写真は2025年2月）。\n\n"
               "レストランは昼と夜に分かれていて、14:30〜17:00は閉まります。夜は17:00から21:30まで（ラストオーダー20:50）。きき酒のあと、日本酒はもう十分という人もビールなら、という店です。クレジットカードが使えます。鳥せい本店から歩いて2分。",
               "Kizakura Kappa Country\n\nIn Kizakura’s old storehouses: the Kizakura Sakaba restaurant, a shop, and a gallery of kappa (water sprite) memorabilia. Kizakura brewed Kyoto’s first craft beer in 1995, and this is where you drink it fresh. The shop sells cans and limited sakes (photos from February 2025).\n\n"
               "The restaurant closes between lunch and dinner, 14:30–17:00. In the evening it is open 17:00–21:30 (last orders 20:50): the place for anyone who has had enough sake at the tasting but could manage a beer. Credit cards are accepted. Two minutes’ walk from Torisei."),
        gmaps=[gm("キザクラカッパカントリー", "Kizakura Kappa Country", 34.93083, 135.76050, "キザクラカッパカントリー")],
        links=[link("official", "キザクラカッパカントリー（公式）", "Kizakura Kappa Country (official, Japanese)", "https://kizakura.co.jp/restaurant/country/")],
        info=info([row("hours", "黄桜酒場：11:30〜14:30（土日祝は11:00〜、ラストオーダー14:00）、17:00〜21:30（ラストオーダー20:50）", "Kizakura Sakaba: 11:30–14:30 (from 11:00 on weekends and holidays; last orders 14:00), 17:00–21:30 (last orders 20:50)"),
                   row("hours", "売店（黄桜商店）10:00〜20:00。黄桜記念館・河童資料館 10:00〜16:00（無料）", "Shop (Kizakura Shoten) 10:00–20:00. Kizakura Memorial Hall and kappa gallery 10:00–16:00 (free)"),
                   row("closed", "火曜（祝日のときは水曜）、12月31日・1月1日（レストラン・売店・記念館とも）", "Tuesdays (Wednesday if Tuesday is a holiday), 31 December and 1 January (restaurant, shop and gallery)")],
                  "黄桜 公式サイト https://kizakura.co.jp/restaurant/country/ （レストラン）、https://kizakura.co.jp/restaurant/country/shop/index.html （売店）、https://kizakura.co.jp/restaurant/country/memorial/index.html （記念館）（2026-11-23）",
                  tip=T("レストラン・売店・記念館の時間と休みは黄桜の公式サイトで確認しました。", "Restaurant, shop and gallery hours and closed days checked on the official Kizakura website."),
                  checked=CHECKED_23)),
    momoyama=dict(
        name=T("大手筋商店街と伏見桃山駅", "Otesuji arcade & Fushimi-Momoyama Station"), kind=T("商店街・駅（ゴール）", "Arcade & station (finish)"),
        blurb=T("屋根のある長い商店街を抜けると駅。京阪で三条へ、丹波橋で特急に乗り換えて約15分です。",
                "A long covered arcade leads to the station. About 15 minutes to Sanjo by Keihan, changing to the limited express at Tambabashi."),
        lat=34.93281, lng=135.76437,
        body=T("大手筋（おおてすじ）商店街と伏見桃山駅（ふしみももやまえき）\n\n酒蔵の町から北へ5分ほど歩くと、屋根のある大手筋商店街に出ます。地元の人の買い物の通りです。商店街を東へ抜けた所が京阪の伏見桃山駅。その先の赤い大鳥居をくぐると、すぐ近鉄の桃山御陵前駅です。\n\n"
               "・三条へ：京阪で。出町柳（でまちやなぎ）行きに乗り、次の丹波橋（たんばばし）で特急に乗り換えると約15分（320円）。乗り換えずに準急のまま行くと25分ほどです。\n"
               "・京都駅へ：近鉄の桃山御陵前から12分（300円）。\n\n"
               "【もう1軒】日本酒をもう少し、という人には藤岡酒造の「酒蔵Bar えん」（11:30〜18:00、水曜休み）。場所はGoogleマップで「藤岡酒造」と探してください。\n\n"
               "三条に戻ってから飲み直すなら、三条駅から鴨川を渡ってすぐの木屋町（きやまち）や先斗町（ぽんとちょう）に、遅くまで開いている店が並んでいます。",
               "Otesuji arcade and Fushimi-Momoyama Station\n\nFive minutes’ walk north of the breweries is the covered Otesuji arcade, where locals shop. The east end of the arcade is Keihan Fushimi-Momoyama Station. Just beyond, through the big red torii, is Kintetsu Momoyamagoryo-mae Station.\n\n"
               "· To Sanjo: Keihan. Board a train for Demachiyanagi and change to the limited express at the next stop, Tambabashi: about 15 minutes (¥320). Staying on the sub-express takes about 25 minutes.\n"
               "· To Kyoto Station: Kintetsu from Momoyamagoryo-mae, 12 minutes (¥300).\n\n"
               "One more stop: if you want a little more sake, Fujioka Shuzo’s Sakagura Bar En is open 11:30–18:00 (closed Wednesdays). Search for 藤岡酒造 on Google Maps.\n\n"
               "For another drink back in town, Kiyamachi and Pontocho, just across the Kamo River from Sanjo Station, are lined with places open late."),
        gmaps=[gm("伏見桃山駅（京阪）", "Fushimi-Momoyama Station (Keihan)", 34.93281, 135.76437, "伏見桃山駅"),
               gm("桃山御陵前駅（近鉄）", "Momoyamagoryo-mae Station (Kintetsu)", 34.93345, 135.76553, "桃山御陵前駅")],
        links=[YAHOO, link("official", "藤岡酒造（酒蔵Bar えん）公式サイト", "Fujioka Shuzo / Sakagura Bar En (official, Japanese)", "https://www.sookuu.net/")],
        info=None),
)

ARR = ("おすすめ到着時間", "Recommended arrival")
VIS = ("おすすめ訪問時間", "Recommended visit time")
DEP = ("おすすめ出発時間", "Recommended departure")
BOAT = ("おすすめ乗船時間", "Recommended boat time")

UJI = ["ujibashi", "byodoin", "omotesando", "tonoshima", "koshoji", "ujigami", "mimuroto"]
FUSHIMI = ["teradaya", "torisei", "gekkeikan", "jikkoku", "gokonomiya", "kizakura"]
DEFAULT = ["ujibashi", "byodoin", "omotesando", "tonoshima", "ujigami", "teradaya", "torisei", "gekkeikan", "jikkoku", "kizakura"]

KOSHOJI_GO = lambda a, b: T(f"寄るなら約40分（{a}〜{b}ごろ）。そのぶん、あとの予定が40分ずつ遅くなります。", f"About 40 minutes if you stop by (around {a}–{b}). Everything after it shifts 40 minutes later.")
GOKO_J = "寄るなら約20分。十石舟に乗らない日は、川沿いを歩いたあとにここへ。"
GOKO_E = "About 20 minutes if you stop by. On days without the boat, come here after the riverside walk."
BOAT_LATE_NOTE = notice("11月25日〜12月6日は最終便が15:40", "25 Nov – 6 Dec: last boat 15:40",
                        "この期間は、月桂冠大倉記念館のあとでは舟に間に合いません。舟に乗りたい日は、中書島に着いたらまず乗り場へ行って便を決め、記念館は舟の前か後のどちらかにしてください（記念館の受付は16:00まで）。両方が無理な日は、川沿いを歩くだけに。",
                        "In this period you cannot make the boat after the Gekkeikan museum. If you want the boat, go to the landing first when you reach Chushojima, fix your sailing, and fit the museum in before or after it (museum last entry 16:00). If both won’t fit, just walk the bank.",
                        frm="2026-11-25", to=BOAT_END)
MONDAY = ("torisei", dict(any=["torisei"]), None, None,
          "月曜は鳥せい本店が休みです。月曜はキザクラカッパカントリーへ（お昼はラストオーダー14:00、夜は17:00から）。寺田屋も月曜に不定休があります。",
          "Torisei is closed on Mondays. On a Monday go to Kizakura Kappa Country instead (lunch last orders 14:00, dinner from 17:00). Teradaya also closes on some Mondays.")
TUESDAY = ("kizakura", dict(any=["kizakura"]), None, None,
           "火曜は休みです（祝日のときは水曜）。火曜の夜は鳥せい本店へ（22:00まで、ラストオーダー21:30）。",
           "Closed on Tuesdays (Wednesday if Tuesday is a holiday). On a Tuesday evening go to Torisei instead (open until 22:00, last orders 21:30).")
UJI_ONLY = lambda dep: ("keihanuji", dict(any=UJI, none=FUSHIMI), None, None,
                        "宇治だけの日は、帰りも京阪宇治駅から。中書島で乗り換えて三条まで約35分・400円です。JR宇治駅からは京都駅へ約20分・240円。",
                        "Uji only? Go back from Keihan Uji: about 35 minutes to Sanjo, changing at Chushojima (¥400). From JR Uji it is about 20 minutes to Kyoto Station (¥240).")
FUSHIMI_ONLY = ("chushojima", dict(any=FUSHIMI, none=UJI), None, None,
                "伏見だけの日は、三条から京阪の特急で中書島へ13分（320円）。月桂冠大倉記念館は9:30から、十石舟は10:00からなので、午前に来てもゆっくり回れます。",
                "Fushimi only? Take the Keihan limited express from Sanjo to Chushojima, 13 minutes (¥320). The Gekkeikan museum opens at 9:30 and the boats start at 10:00, so a morning visit works too.")
MIMUROTO_HINT = ("mimuroto", dict(any=["mimuroto"], andAny=FUSHIMI), None, None,
                 "三室戸寺のあとは、京阪の三室戸駅（歩いて15分）から中書島へ。宇治駅へ戻らなくて大丈夫です。伏見に着くのが1時間半ほど遅くなるので、寺田屋（時間は要確認）と月桂冠（受付16:00まで）のどちらかに絞りましょう。",
                 "After Mimurotoji, ride from Keihan Mimuroto Station (15 min on foot) to Chushojima; no need to return to Uji Station. You will reach Fushimi about 90 minutes later, so choose between Teradaya (hours unconfirmed) and Gekkeikan (last entry 16:00).")
BOTH_DETOURS = ("koshoji", dict(any=["koshoji"], andAny=["mimuroto"]), None, None,
                "興聖寺と三室戸寺の両方に寄ると、宇治だけで午後の半ばまでかかります。その日は伏見を別の日に。",
                "With both Koshoji and Mimurotoji, Uji alone takes until mid-afternoon. Leave Fushimi for another day.")
STATION_EXTRA = {   # 駅のスポットの文章に出てくるお店の出典
    "keihanuji": "。通圓の営業時間（10:30〜17:30、L.O.16:00、年中無休）は通圓 公式サイト https://tsuentea.com/ （2026-11-23）",
    "momoyama": "。酒蔵Bar えんの営業時間（11:30〜18:00、水曜休み）は藤岡酒造 公式サイト https://www.sookuu.net/ （2026-11-23）",
}
STATION_INFO = lambda rows, sid=None: info(rows, TRAIN_SRC + STATION_EXTRA.get(sid, ""), tip=TRAIN_TIP)

COURSES = [
    dict(
        id="late", file="uji.json",
        note="「9〜10時に出発」コース。三条9:26発の京阪（中書島で乗り換え）→京阪宇治9:59。宇治橋→平等院（10:15〜11:45。まず内部拝観の券）→表参道でお昼と抹茶（11:45〜13:00）→塔の島・朝霧橋→宇治上神社→京阪宇治14:17発→中書島14:33→寺田屋→月桂冠大倉記念館（受付16:00まで）→十石舟（最終16:20）か川沿いの散歩→鳥せい本店（夜ごはん 17:20〜）→キザクラカッパカントリー（18:40〜）→伏見桃山20:12発→三条20:27。",
        order=[
            ("keihanuji", ARR, "9:59（三条 9:26発）", "9:59 (the 9:26 from Sanjo)",
             T("三条9:26発の特急に乗り、中書島（9:39着）で向かいのホームの宇治行き（9:44発）に乗り換えて、宇治に9:59。平日は三条9:29発で9:58着です。\n\n午後は14:17発の中書島行きで伏見へ（14:33着・320円）。宇治線は10〜15分おきに出ています。",
               "Take the 9:26 limited express from Sanjo, change at Chushojima (9:39) to the Uji train across the platform (9:44) and arrive at 9:59. On weekdays the 9:29 from Sanjo arrives at 9:58.\n\nIn the afternoon take the 14:17 to Chushojima for Fushimi (arrives 14:33, ¥320). Uji Line trains run every 10–15 minutes."),
             [row("train", "三条9:26発（京阪・中書島で乗り換え）→ 京阪宇治9:59着・400円", "Sanjo 9:26 (Keihan, change at Chushojima) → Keihan Uji 9:59, ¥400"),
              row("train", "京阪宇治14:17発 → 中書島14:33着・320円（10〜15分おき）", "Keihan Uji 14:17 → Chushojima 14:33, ¥320 (every 10–15 min)"),
              row("train", "京都駅から：JR奈良線 京都9:34発（みやこ路快速）→ 宇治9:51着・240円", "From Kyoto Station: JR Nara Line 9:34 (Miyakoji Rapid) → Uji 9:51, ¥240")]),
            ("ujibashi", VIS, "10:00〜10:10", "10:00–10:10", None, None),
            ("byodoin", VIS, "10:15〜11:45", "10:15–11:45",
             T("【この時間に着く人へ】表門で拝観券を買ったら、まっすぐ庭園の中の「鳳凰堂内部拝観受付」へ。この時間だと、取れるのは何時間か先の回になることがあり、混む日は券がもうないこともあります。券の時間まで、庭園を一周してミュージアムを見て、それでも時間が余れば、いったん外へ出て表参道でお昼にして戻れます（内部拝観の券を表門の受付で見せれば再入場できます。お堂の中を見たあとは再入場できません）。\n\nお堂の中をどうしても見たい人は、一覧の上のボタンで「開門に合わせる」コースに切り替えてください。券がなくても、池の正面からの眺めとミュージアムで1時間は十分に楽しめます。",
               "Arriving at this hour: once you have your ticket at the main gate, go straight to the “Phoenix Hall interior” desk inside the garden. At this time your slot may be a few hours away, and on busy days the tickets may already be gone. Until your slot, walk round the garden and see the museum; if there is still time, you can go out for lunch on Omotesando and come back (show your interior ticket at the gate to re-enter; there is no re-entry after the interior visit).\n\nIf seeing the interior matters to you, switch to the “At opening time” course with the buttons above the list. Even without a ticket, the view across the pond and the museum easily fill an hour."), None),
            ("omotesando", VIS, "11:45〜13:00", "11:45–13:00",
             T("このコースでは、ここでお昼にします。通りに茶そばやにしんそばの店が何軒かあるので、空いている店に入ってください（店名は、営業時間を公式に確かめられなかったので書いていません）。\n\n食後に中村藤吉へ。昼すぎは列が長くなることがあります。並びたくない日は、入口のスターバックスか、宇治橋のたもとの通圓（10:30〜17:30、ラストオーダー16:00）へ。",
               "On this course, have lunch here. Several places on the street serve green-tea soba or herring soba; take whichever has seats (I name none because I could not confirm their hours on official pages).\n\nGo to Nakamura Tokichi afterwards. The queue can be long from early afternoon; if you don’t want to wait, try the Starbucks at the start of the lane or Tsuen at the foot of Uji Bridge (10:30–17:30, last orders 16:00)."), None),
            ("tonoshima", VIS, "13:05〜13:25", "13:05–13:25", None, None),
            ("koshoji", VIS, None, None, KOSHOJI_GO("13:30", "14:10"), None),
            ("ujigami", VIS, "13:30〜14:05", "13:30–14:05",
             T("見終わったら、さわらびの道を歩いて京阪宇治駅へ（約8分）。14:17発の電車に乗ります。",
               "Afterwards walk the Sawarabi path to Keihan Uji Station (about 8 minutes) for the 14:17 train."), None),
            ("mimuroto", VIS, None, None,
             T("寄るなら歩きを入れて約1時間40分。このコースで寄ると拝観時間の15:10に間に合わせるのがやっとで、伏見の記念館には入れなくなります。花の時期に行くなら「開門に合わせる」コースで。",
               "Allow about 1 h 40 min including the walk. On this course you would barely make it before the 15:10 closing and would miss the museum in Fushimi; in the flower season, use the “At opening time” course."), None),
            ("chushojima", ARR, "14:33", "14:33",
             T("ここからは受付の時間との勝負です。寺田屋（時間は公式で確かめられませんでした。要確認）へ歩いて7分、そのあと月桂冠大倉記念館（受付16:00まで）へ3分。記念館は予約しておくと安心です。",
               "From here you are racing the last-entry times: 7 minutes on foot to Teradaya (hours could not be confirmed officially), then 3 minutes to the Gekkeikan museum (last entry 16:00). Booking the museum ahead is safest."),
             [row("train", "京阪宇治14:17発 → 中書島14:33着・320円", "Keihan Uji 14:17 → Chushojima 14:33, ¥320"),
              row("train", "三条 → 中書島 13分・320円（京阪の特急）", "Sanjo → Chushojima 13 min, ¥320 (Keihan limited express)")]),
            ("teradaya", VIS, "14:42〜15:00", "14:42–15:00",
             T("このコースでは時間が短いので、中を見るのは15分ほどに。外から見るだけにして、記念館に早めに入るのも手です。",
               "Time is short on this course, so allow about 15 minutes inside; or just look from outside and get to the museum earlier."), None),
            ("gekkeikan", VIS, "15:05〜15:55", "15:05–15:55",
             T("受付は16:00まで。宇治でのんびりしすぎた日は、寺田屋を外から見るだけにして、先にここへ。お昼から時間がたっているので、きき酒の前に水を飲んで、ゆっくりと。",
               "Last entry is 16:00. If you lingered in Uji, see Teradaya from outside only and come here first. It has been a while since lunch, so drink some water before the tasting and take it slowly."), None),
            ("jikkoku", BOAT, "16:20〜17:15（最終便。11月24日までと春〜秋）。冬は川沿いを歩いて20分", "16:20–17:15 (the last boat; until 24 Nov, and spring to autumn). In winter, a 20-minute walk along the bank",
             T("記念館を出たら、すぐ裏の乗り場へ。この時間割で乗れるのは16:20の最終便です（11月24日まで。受付は16:05まで、3〜5月は16:00まで）。記念館に入る前に乗り場で空席を聞いて、決めておいてください。",
               "From the museum go straight to the landing behind it. On this timetable the boat you can make is the last one, at 16:20 (until 24 November; check in by 16:05, or 16:00 in March–May). Ask about seats at the landing and fix it before you go into the museum."), None),
            ("gokonomiya", VIS, None, None, T(GOKO_J, GOKO_E), None),
            ("torisei", VIS, "17:25〜18:30（舟に乗らない日は16:40ごろから）", "17:25–18:30 (from about 16:40 on days without the boat)",
             T("このコースでは夜ごはんに。舟を降りたら、川沿いと竜馬通りを歩いて約10分。焼き鳥と鳥めしで、蔵出しの酒をもう一杯。昼から夜まで通しで開いている店です（22:00まで、ラストオーダー21:30）。",
               "On this course, dinner. From the boat it is about 10 minutes’ walk along the canal and Ryoma-dori. Yakitori and chicken rice with one more glass of brewery sake. It stays open from lunch straight through the evening (until 22:00, last orders 21:30)."), None),
            ("kizakura", VIS, "18:40〜20:00", "18:40–20:00",
             T("鳥せい本店から歩いて2分。締めに地ビールを一杯。鳥せいが混んでいる日や月曜は、夜ごはんもここで（17:00から）。20:00に出れば、伏見桃山駅まで歩いて7分ほどです。",
               "Two minutes’ walk from Torisei, for a last craft beer. If Torisei is full, or on a Monday, have dinner here too (from 17:00). Leave at 20:00 and it is about 7 minutes’ walk to Fushimi-Momoyama Station."), None),
            ("momoyama", DEP, "20:12（三条に20:27）", "20:12 (Sanjo at 20:27)",
             T("20:12発に乗り、丹波橋で特急に乗り換えて三条に20:27。もう少し飲んで21:05発にしても、三条に21:21に着きます。",
               "Take the 20:12, change to the limited express at Tambabashi and reach Sanjo at 20:27. Stay for another drink and the 21:05 still gets you to Sanjo at 21:21."),
             [row("train", "伏見桃山20:12発（京阪・丹波橋で特急に乗り換え）→ 三条20:27着・320円", "Fushimi-Momoyama 20:12 (Keihan, change to the limited express at Tambabashi) → Sanjo 20:27, ¥320"),
              row("train", "伏見桃山21:05発（同じく丹波橋で乗り換え）→ 三条21:21着・320円", "Fushimi-Momoyama 21:05 (same change at Tambabashi) → Sanjo 21:21, ¥320"),
              row("train", "桃山御陵前（近鉄）→ 京都 12分・300円", "Momoyamagoryo-mae (Kintetsu) → Kyoto 12 min, ¥300")]),
        ],
        sections=[dict(first="keihanuji", last="omotesando", day=0), dict(first="tonoshima", last="mimuroto", day=1),
                  dict(first="chushojima", last="gokonomiya", day=2), dict(first="torisei", last="momoyama", day=3)],
        extra_notices={"jikkoku": [BOAT_LATE_NOTE]},
        hints=[UJI_ONLY(None), FUSHIMI_ONLY, BOTH_DETOURS, MONDAY, TUESDAY]),
    dict(
        id="early", file="uji-early.json",
        note="「開門に合わせる」コース。三条7:49発の京阪（中書島で乗り換え）→京阪宇治8:22。宇治橋→平等院（8:40に表門、8:45開門、内部拝観の券は9:10から）→表参道の中村藤吉（10:00開店）でひと休み→塔の島・朝霧橋→宇治上神社→京阪宇治12:28発→中書島12:44→寺田屋→鳥せい本店（お昼）→月桂冠大倉記念館→十石舟か川沿いの散歩→キザクラカッパカントリー（17:00〜、夜ごはん）→伏見桃山18:48発→三条19:04。",
        order=[
            ("keihanuji", ARR, "8:22（三条 7:49発）", "8:22 (the 7:49 from Sanjo)",
             T("三条7:49発の淀屋橋行きに乗り、中書島（8:02着）で宇治行き（8:07発）に乗り換えて、宇治に8:22。平等院の表門に、開門の少し前に着けます。次の8:01発だと宇治に8:34で、表門に着くのは開門とほぼ同時です。平日は三条7:50発で8:24着。\n\nお昼前に、12:28発の中書島行きで伏見へ（12:44着・320円）。宇治線は10〜15分おきに出ています。",
               "Take the 7:49 from Sanjo (bound for Yodoyabashi), change at Chushojima (8:02) to the Uji train (8:07) and arrive at 8:22: in time to be at Byodoin’s main gate a little before it opens. The next one, at 8:01, reaches Uji at 8:34, putting you at the gate just as it opens. On weekdays the 7:50 from Sanjo arrives at 8:24.\n\nBefore lunch take the 12:28 to Chushojima for Fushimi (arrives 12:44, ¥320). Uji Line trains run every 10–15 minutes."),
             [row("train", "三条7:49発（京阪・中書島で乗り換え）→ 京阪宇治8:22着・400円", "Sanjo 7:49 (Keihan, change at Chushojima) → Keihan Uji 8:22, ¥400"),
              row("train", "京阪宇治12:28発 → 中書島12:44着・320円（10〜15分おき）", "Keihan Uji 12:28 → Chushojima 12:44, ¥320 (every 10–15 min)"),
              row("train", "京都駅から：JR奈良線 京都8:15発 → 宇治8:33着・240円", "From Kyoto Station: JR Nara Line 8:15 → Uji 8:33, ¥240")]),
            ("ujibashi", VIS, "8:25〜8:35", "8:25–8:35",
             T("朝は橋の上に人が少なく、川の音がよく聞こえます。", "In the morning there are few people on the bridge and you can hear the river."), None),
            ("byodoin", VIS, "8:40〜10:15", "8:40–10:15",
             T("【開門に合わせて行く人へ】8:40ごろ表門に着いて、8:45の開門を待ちます。入ったら、写真より先に庭園の中の「鳳凰堂内部拝観受付」へ。券を配り始めるのは9:10で、最初の回は9:30です。早く並ぶほど早い回を取りやすくなります。\n\n券を受け取ったら、池の正面の岸へ。午前は鳳凰堂の正面に日が当たる時間です。お堂の中を見たあと、ミュージアム鳳翔館を見て、10:15ごろ外へ。",
               "Arriving for the opening: be at the main gate at about 8:40 and wait for it to open at 8:45. Once in, go to the “Phoenix Hall interior” desk inside the garden before taking photos. Tickets are handed out from 9:10 and the first visit is at 9:30; the earlier you queue, the earlier the slot you are likely to get.\n\nWith your ticket in hand, go to the bank straight across the pond: in the morning the front of the hall is in the sun. After the interior, see the Hoshokan museum and leave at about 10:15."), None),
            ("omotesando", VIS, "10:20〜11:05", "10:20–11:05",
             T("早起きした日のひと休みは、ここで。平等院を出るころに、ちょうど中村藤吉が開いています（10:00開店）。昼すぎからは列が長くなることがあるので、この時間に入れるのが早く来た人の得です。\n\n朝ごはんを食べずに出てきた人は、平等院の前に入口のスターバックス（8:00〜）へ寄るなら、三条を1本早い電車で。\n\nお昼は伏見で食べるので、ここでは甘いものだけに。",
               "This is your rest after the early start. Nakamura Tokichi has just opened (10:00) as you leave Byodoin. The queue can grow from early afternoon, so getting in at this hour is the reward for coming early.\n\nIf you left without breakfast and want the Starbucks at the start of the lane (from 8:00) before Byodoin, take one train earlier from Sanjo.\n\nLunch is in Fushimi, so keep it to sweets here."), None),
            ("tonoshima", VIS, "11:10〜11:30", "11:10–11:30", None, None),
            ("koshoji", VIS, None, None, KOSHOJI_GO("11:35", "12:15"), None),
            ("ujigami", VIS, "11:35〜12:10", "11:35–12:10",
             T("見終わったら、さわらびの道を歩いて京阪宇治駅へ（約8分）。12:28発の電車に乗ります。待つあいだに橋のたもとの通圓でお茶を。",
               "Afterwards walk the Sawarabi path to Keihan Uji Station (about 8 minutes) for the 12:28 train. While you wait, look in at Tsuen by the bridge."), None),
            ("mimuroto", VIS, None, None,
             T("寄るなら歩きを入れて約1時間40分（宇治上神社を12:10に出て、三室戸駅に13:50ごろ）。伏見に着くのは14:15ごろになります。",
               "Allow about 1 h 40 min including the walk (leave Ujigami Shrine at 12:10, reach Mimuroto Station at about 13:50). You would reach Fushimi at about 14:15."), None),
            ("chushojima", ARR, "12:44", "12:44",
             T("北口から寺田屋まで歩いて7分。お腹がすいていたら、先に鳥せい本店へ行ってもかまいません（駅から歩いて約10分）。",
               "Seven minutes on foot from the north exit to Teradaya. If you are hungry, go to Torisei first (about 10 minutes from the station)."),
             [row("train", "京阪宇治12:28発 → 中書島12:44着・320円", "Keihan Uji 12:28 → Chushojima 12:44, ¥320"),
              row("train", "三条 → 中書島 13分・320円（京阪の特急）", "Sanjo → Chushojima 13 min, ¥320 (Keihan limited express)")]),
            ("teradaya", VIS, "12:52〜13:15", "12:52–13:15", None, None),
            ("torisei", VIS, "13:20〜14:10", "13:20–14:10",
             T("このコースではお昼に。12時台は並ぶことがあり、13時すぎに着くこの時間割なら少し落ち着いています。このあと月桂冠できき酒をするので、しっかり食べておきましょう。",
               "On this course, lunch. There can be a queue around noon; arriving after 13:00, as this timetable does, it is usually calmer. You will be tasting sake at Gekkeikan next, so eat properly."), None),
            ("gekkeikan", VIS, "14:20〜15:10", "14:20–15:10",
             T("鳥せい本店から南へ歩いて約5分。", "About 5 minutes’ walk south of Torisei."), None),
            ("jikkoku", BOAT, "15:40〜16:35（冬は川沿いを歩いて20分）", "15:40–16:35 (in winter a 20-minute walk along the bank)",
             T("記念館を出たら、すぐ裏の乗り場へ。乗るのは15:40の便です（11月25日〜12月6日はこれが最終便）。受付は出航の15分前（3〜5月は20分前）までなので、記念館を15:10には出てください。",
               "From the museum go straight to the landing behind it. Take the 15:40 boat (the last one from 25 November to 6 December). Check-in closes 15 minutes before departure (20 minutes in March–May), so leave the museum by 15:10."), None),
            ("gokonomiya", VIS, None, None, T(GOKO_J, GOKO_E), None),
            ("kizakura", VIS, "17:00〜18:30", "17:00–18:30",
             T("舟を降りてから17:00までは、川沿いと竜馬通り商店街を歩くか、御香宮神社へ。17:00に店が開いたら、夜ごはんとビールを。\n\n朝が早かった日なので、舟のあとまっすぐ帰るのもありです（伏見桃山駅から三条へ約15分）。まだ飲める人は、ここのあと鳥せい本店でもう1軒（22:00まで、ラストオーダー21:30。月曜休み）。",
               "Between the boat and 17:00, walk the canal and the Ryoma-dori shopping street, or visit Gokonomiya Shrine. When the restaurant opens at 17:00, have dinner and a beer.\n\nAfter such an early start, going straight home after the boat is fine too (about 15 minutes from Fushimi-Momoyama to Sanjo). If you can manage more, Torisei makes a second stop afterwards (until 22:00, last orders 21:30; closed Mondays)."), None),
            ("momoyama", DEP, "18:48（三条に19:04）", "18:48 (Sanjo at 19:04)",
             T("キザクラから歩いて7分ほど。18:48発に乗り、丹波橋で特急に乗り換えて三条に19:04。遅くなっても電車はあります（21:05発で三条に21:21）。",
               "About 7 minutes’ walk from Kizakura. Take the 18:48, change to the limited express at Tambabashi and reach Sanjo at 19:04. There are trains later too (the 21:05 reaches Sanjo at 21:21)."),
             [row("train", "伏見桃山18:48発（京阪・丹波橋で特急に乗り換え）→ 三条19:04着・320円", "Fushimi-Momoyama 18:48 (Keihan, change to the limited express at Tambabashi) → Sanjo 19:04, ¥320"),
              row("train", "伏見桃山21:05発（同じく丹波橋で乗り換え）→ 三条21:21着・320円", "Fushimi-Momoyama 21:05 (same change at Tambabashi) → Sanjo 21:21, ¥320"),
              row("train", "桃山御陵前（近鉄）→ 京都 12分・300円", "Momoyamagoryo-mae (Kintetsu) → Kyoto 12 min, ¥300")]),
        ],
        sections=[dict(first="keihanuji", last="omotesando", day=0), dict(first="tonoshima", last="mimuroto", day=1),
                  dict(first="chushojima", last="torisei", day=2), dict(first="gekkeikan", last="gokonomiya", day=3),
                  dict(first="kizakura", last="momoyama", day=4)],
        extra_notices={},
        hints=[UJI_ONLY(None), FUSHIMI_ONLY, MIMUROTO_HINT, BOTH_DETOURS, MONDAY, TUESDAY]),
]

NOTE_HEAD = "京都 宇治と伏見の1日ルート（uji/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（uji.json＝9〜10時に出発、uji-early.json＝平等院の開門に合わせる）。出発は京都の中心・三条（京阪）。このファイル："
NOTE_TAIL = (" 興聖寺・三室戸寺・御香宮神社は寄り道（defaultPicks に入れていない）。"
             "写真は Toshi の写真ライブラリから（宇治は2017年6月・2017年9月の鵜飼・2025年2月、伏見は2025年2月、中書島駅は2026年5月。横の写真だけ、縦で撮った抹茶・きき酒・おちょこは横に切り抜き。長辺1600px・位置情報なし）。"
             "自分の写真がない場所（宇治橋・宇治上神社の建物・興聖寺・三室戸寺・京阪宇治駅・寺田屋・十石舟・御香宮神社・大鳥居など）は Wikimedia Commons の写真（photos の要素が {file, credit}。一覧は scripts/uji_web_credits.json）。"
             "info.source は確認した出典、info.checked は確認日（各公式サイト、電車は乗換案内）。verified: false は公式で確認できなかったもの（宇治上神社の時間・寺田屋・御香宮の石庭）。"
             "入口で困ること（現金不可・先着順・休み・受付の締め切り）は caution と head つきの notices。plan.defaultPicks は最初から選ばれている場所で、各スポットの「おすすめ◯◯時間」はこの組み合わせの時間割。"
             "このファイルは scripts/build_uji_data.py で作る（直接直さない）。")
WEB_FIRST = {"ujigami", "kizakura"}


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    spots = []
    for sid, (lj, le), tj, te, go, rows in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        if tj:
            text = T(body["ja"] + ("\n\n" + go["ja"] if go else "") + f"\n\n{lj}：{tj}",
                     body["en"] + ("\n\n" + go["en"] if go else "") + f"\n\n{le}: {te}")
        else:   # 寄り道：時間割の外。行き方の文がそのまま「おすすめ訪問時間」になる
            text = T(body["ja"] + f"\n\n{lj}：{go['ja']}", body["en"] + f"\n\n{le}: {go['en']}")
        if rows:
            b["info"] = STATION_INFO(rows, sid)
        assert b["info"], sid
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out["text"] = text
        out["photos"] = photos(sid, sid in WEB_FIRST)
        out["notices"] = c.get("extra_notices", {}).get(sid, []) + out.get("notices", [])
        spots.append(out)
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    uji, fushimi = [NO[i] for i in UJI], [NO[i] for i in FUSHIMI]
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": [{"first": NO[s["first"]], "last": NO[s["last"]], "day": s["day"]} for s in c["sections"]],
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は1日で無理なく回れる組み合わせ（時間割どおり）。京阪宇治駅は宇治の場所を選ぶと入り、中書島駅と伏見桃山駅は伏見の場所を選ぶと入る。寄り道を足したときの回り方は各スポットの文章と hints。",
                 "defaultMode": "pick",
                 "picks": [NO[x[0]] for x in order if x[0] in UJI + FUSHIMI],
                 "defaultPicks": [NO[i] for i in DEFAULT],
                 "auto": {str(NO["keihanuji"]): {"any": uji}, str(NO["chushojima"]): {"any": fushimi}, str(NO["momoyama"]): {"any": fushimi}},
                 "hints": [{"spot": NO[sid], "rule": rule(r), "from": frm, "to": to, "text": T(ja, en)} for sid, r, frm, to, ja, en in c["hints"]]},
        "photoBase": f"../images/{MAP_ID}/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


for c in COURSES:
    build(c)
