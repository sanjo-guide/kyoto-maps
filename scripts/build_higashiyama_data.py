#!/usr/bin/env python3
"""京都・東山（清水寺から北、銀閣寺まで）のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_higashiyama_data.py
- 作るもの（COURSES）:
  - data/routes/higashiyama.json … 「9〜10時に出発」
  - data/routes/higashiyama-early.json … 「早朝に出発」（5時すぎに出て、6:00の開門に清水寺へ）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方の一言、「選んで回る」の設定
- スポットの番号はコースで変わるので、紹介ページ（higashiyama/js/i18n.js）の写真は id で指定している
- 写真は images/higashiyama/<スポットのid>-<番号>.jpg を番号の順に全部使う
- 2026-11-22 の見直し（オーナーの基準）: 出発は京都の中心・三条のあたり。伏見稲荷・東福寺・泉涌寺・三十三間堂は
  別のマップ（fushimi-inari/、scripts/build_fushimi_inari_data.py）に分けた。時刻と運賃は乗換案内で確認
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "higashiyama"
IMG = f"{R}/images/{MAP_ID}"
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


def link(kind, ja, en, url):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url, "en": url}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


AUTUMN_END = "2026-12-06"   # 永観堂・金戒光明寺の、2026年秋の特別期間の最終日。過ぎると秋だけの行と注意書きは自動で消える
KODAIJI_NIGHT_END = "2026-12-13"
KIYOMIZU_NIGHT_END = "2026-11-30"


def info(rows, source, tip=None, verified=True, checked=CHECKED):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": checked, "source": source}
    if not verified:
        d["verified"] = False
    return d


def photos(pid, extra=None):
    # extra: ネットから借りた写真（{"file", "credit": {"author", "license", "page"}}）。写真の上に撮影者とライセンスが出る
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def cc(file, author, license, title):
    return {"file": file, "credit": {"author": author, "license": license, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    # 銀閣寺は Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    kiyomizu=dict(
        name=T("清水寺", "Kiyomizu-dera"), kind=T("お寺", "Temple"),
        blurb=T("崖にせり出した「清水の舞台」から京都の町を一望。朝6:00に開きます。",
                "Kyoto spread out below the famous wooden stage. It opens at 6:00 in the morning."),
        lat=34.99485, lng=135.78505,
        body=T("清水寺（きよみずでら）\n\n音羽山（おとわやま）の中腹に建つお寺。朱色の仁王門と三重塔を過ぎると、崖の上にせり出した本堂の「清水の舞台」に出ます。少し先の奥の院のあたりから振り返ると、木々の上に浮かぶ舞台の全体が見えます。\n\n舞台の下には、3本の筋になって水が落ちる音羽の滝があります。\n\n春・夏・秋の夜間特別拝観の期間は21:30まで開いていて（受付は21:00まで）、ライトアップされた舞台と京都の夜景が見られます。",
               "Kiyomizu-dera\n\nA temple on the slope of Mt. Otowa. Past the vermilion Nio Gate and three-storied pagoda you come out onto the “Kiyomizu stage” of the main hall, built out over the cliff. Look back from near the Okunoin hall a little further on for the whole stage floating above the trees.\n\nBelow the stage is the Otowa waterfall, falling in three streams.\n\nDuring the special evening openings in spring, summer and autumn the temple stays open until 21:30 (last entry 21:00), with the stage lit up and the city lights below."),
        gmaps=[gm("清水寺", "Kiyomizu-dera", 34.99485, 135.78505, "清水寺")],
        links=[link("official", "清水寺 公式サイト（拝観時間・アクセス）", "Kiyomizu-dera (official)", "https://www.kiyomizudera.or.jp/access.php"),
               link("info", "清水寺 よくある質問", "Kiyomizu-dera FAQ (Japanese)", "https://www.kiyomizudera.or.jp/faq.php")],
        info=info([row("hours", "6:00開門、18:00閉門（7・8月は18:30）", "Opens 6:00, closes 18:00 (18:30 in July and August)"),
                   row("hours", "秋の夜間特別拝観（2026年11月21日〜30日）：21:30まで開門、受付は21:00まで", "Autumn evening opening (21–30 Nov 2026): open until 21:30, last entry 21:00", until=KIYOMIZU_NIGHT_END),
                   row("fee", "拝観料は、公式サイトでは金額を確かめられませんでした（要確認）", "The admission fee could not be confirmed on the official website (unconfirmed)")],
                  "清水寺 公式サイト（拝観時間・アクセス、よくある質問）。2026年の夜間特別拝観は春3/27〜4/5、夏8/14〜16、秋11/21〜30。拝観料は公式サイトの3ページ（トップ、アクセス、よくある質問）に金額がなく未確認",
                  verified=False),
        caution=T("入口は清水坂と茶わん坂の2つだけ", "Only two ways in: Kiyomizu-zaka and Chawan-zaka"),
        notices=[notice("入口は2つだけ。地図アプリの近道に注意", "Only two ways in: beware map-app shortcuts",
                        "境内に入れるのは、清水坂を上って仁王門の前に出る道と、茶わん坂を上る道だけです。Googleマップなどが、入れない道を案内することがあります（公式サイト）。",
                        "You can only enter by walking up Kiyomizu-zaka to the Nio Gate, or up Chawan-zaka. Google Maps and other apps sometimes send you along a route with no way in (official site).",
                        url="https://www.kiyomizudera.or.jp/access.php"),
                 notice("三脚・一脚は使えません", "No tripods or monopods",
                        "境内での飲食（フタの閉まる飲み物を除く）、喫煙、ペットを連れての拝観もできません（公式サイトのよくある質問）。",
                        "Eating in the grounds (drinks with a lid are fine), smoking and pets are not allowed either (from the official FAQ).",
                        url="https://www.kiyomizudera.or.jp/faq.php")]),
    sanneizaka=dict(
        name=T("産寧坂（三年坂）と二年坂", "Sannenzaka and Ninenzaka"), kind=T("町並み", "Historic street"),
        blurb=T("清水寺の門前から北へ下る石畳の坂。昼はとても混みます。早朝コースでは、店が開く前に歩きます。",
                "Stone-paved lanes running north downhill from Kiyomizu-dera. Very crowded by day; the early course walks them before the shops open."),
        lat=34.99680, lng=135.78120,
        body=T("産寧坂（さんねいざか）と二年坂（にねんざか）\n\n清水寺の門前から北へ下る、石畳の坂道です。古い町家に、お土産やお菓子の店、カフェが並びます。\n\n昼間はとても混みます。\n\n二年坂の途中にある町家のスターバックス（京都二寧坂ヤサカ茶屋店）は8:00から20:00まで（不定休）。店の前に並ぶことはできず、混むときは入店を制限することがあります（公式サイト）。",
               "Sannenzaka and Ninenzaka\n\nStone-paved lanes running north downhill from the gate of Kiyomizu-dera, lined with old townhouses that hold souvenir and sweet shops and cafés.\n\nThey are very crowded in the daytime.\n\nThe Starbucks in a townhouse on Ninenzaka (Kyoto Ninenzaka Yasaka Chaya) is open 8:00–20:00 (irregular closing days). Queuing outside is not allowed and entry may be limited when busy (official site)."),
        gmaps=[gm("産寧坂", "Sannenzaka", 34.99680, 135.78120, "産寧坂"),
               gm("スターバックス 京都二寧坂ヤサカ茶屋店", "Starbucks Kyoto Ninenzaka Yasaka Chaya", 34.99830, 135.78080, "スターバックス コーヒー 京都二寧坂ヤサカ茶屋店")],
        links=[link("official", "スターバックス 京都二寧坂ヤサカ茶屋店", "Starbucks Kyoto Ninenzaka Yasaka Chaya (Japanese)", "https://store.starbucks.co.jp/detail-1476/")],
        info=info([row("hours", "スターバックス 京都二寧坂ヤサカ茶屋店 8:00〜20:00、不定休", "Starbucks Kyoto Ninenzaka Yasaka Chaya: 8:00–20:00, irregular closing days")],
                  "スターバックス 公式サイトの店舗ページ。ほかの店の開く時間は確かめていない")),
    yasakatower=dict(
        name=T("八坂の塔（法観寺）", "Yasaka Pagoda (Hokan-ji)"), kind=T("町並み・お寺", "Historic street & temple"),
        blurb=T("石畳の坂の先に立つ五重塔。清水寺が開く前の早朝に、ここで写真を撮る人が多い場所です。",
                "A five-storied pagoda at the end of a stone-paved lane. Many people come here for photos early, before Kiyomizu-dera opens."),
        lat=34.99843, lng=135.77952,
        body=T("八坂の塔（やさかのとう）\n\n法観寺（ほうかんじ）の五重塔で、高さは約46m。八坂通の坂道から見上げる塔は、東山でいちばんよく写真に撮られる景色です。\n\n坂の下から塔を見上げる向きと、塔を過ぎてから振り返る向き、どちらも撮れます。まわりは人が住んでいる町なので、早朝は静かに。",
               "Yasaka Pagoda\n\nThe five-storied pagoda of Hokan-ji, about 46 m tall. The view up the slope of Yasaka-dori to the pagoda is the most photographed in Higashiyama.\n\nYou can shoot looking up from the bottom of the slope, or looking back after you pass the pagoda. People live all around here, so keep your voice down early in the morning."),
        gmaps=[gm("八坂の塔", "Yasaka Pagoda", 34.99843, 135.77952, "八坂の塔 法観寺")],
        links=[], info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    kodaiji=dict(
        name=T("高台寺と圓徳院", "Kodai-ji and Entoku-in"), kind=T("お寺", "Temple"),
        blurb=T("豊臣秀吉の妻・ねねのお寺。開門は9:00。秋の夜は22:00まで開いていて、池に映る紅葉が見られます。",
                "The temple of Nene, wife of Toyotomi Hideyoshi. Opens at 9:00; on autumn evenings it stays open until 22:00, with maples reflected in the pond."),
        lat=35.00077, lng=135.78166,
        body=T("高台寺（こうだいじ）と圓徳院（えんとくいん）\n\n豊臣秀吉の妻・北政所（きたのまんどころ）ねねが、秀吉をとむらうために建てたお寺です。池のまわりの庭を歩き、山の斜面を上って、帰りは竹林の小道を下ります。\n\nねねの道をはさんだ向かいの圓徳院は、ねねが晩年を過ごした場所。座敷に座って北庭を眺められます。2か寺の共通券があります。\n\n夜間特別拝観の期間は17:00に明かりがつき、22:00まで（受付21:30まで）。昼と夜の入れ替えはないので、夕方に入ってそのまま暗くなるのを待てます。",
               "Kodai-ji and Entoku-in\n\nBuilt by Nene (Kita-no-Mandokoro), wife of Toyotomi Hideyoshi, to pray for him. You walk the garden around the pond, climb the hillside, and come back down a bamboo path.\n\nAcross Nene-no-michi, Entoku-in is where Nene spent her last years; you can sit in the tatami rooms and look out at the north garden. There’s a combined ticket for both.\n\nDuring the special evening openings the lights come on at 17:00 and it stays open until 22:00 (last entry 21:30). Day and night are not separate sessions, so you can go in late in the afternoon and wait for dark."),
        gmaps=[gm("高台寺", "Kodai-ji", 35.00077, 135.78166, "高台寺"), gm("圓徳院", "Entoku-in", 35.00066, 135.77942, "圓徳院 京都")],
        links=[link("official", "高台寺 公式サイト（拝観案内）", "Kodai-ji (official, Japanese)", "https://www.kodaiji.com/haikan.html"),
               link("official", "圓徳院（拝観休止のお知らせ）", "Entoku-in (official, Japanese)", "https://www.kodaiji.com/entoku-in/")],
        info=info([row("hours", "9:00〜17:30（受付17:00まで）", "9:00–17:30 (last entry 17:00)"),
                   row("hours", "秋の夜間特別拝観（2026年10月23日〜12月13日）：17:00点灯、22:00閉門（受付21:30まで）。入れ替えなし", "Autumn evening opening (23 Oct – 13 Dec 2026): lights on at 17:00, closes 22:00 (last entry 21:30). No separate evening session", until=KODAIJI_NIGHT_END),
                   row("fee", "高台寺 大人800円・中高生400円。高台寺・圓徳院の共通券1,200円", "Kodai-ji ¥800 adults, ¥400 junior/senior high. Combined ticket with Entoku-in ¥1,200"),
                   row("hours", "圓徳院だけの拝観時間と料金は、公式サイトで確かめられませんでした（要確認）", "Entoku-in’s own hours and single-ticket price could not be confirmed on the official site (unconfirmed)")],
                  "高台寺 公式サイト（拝観案内、歳時）、圓徳院のページ（拝観休止の予定）"),
        notices=[notice("圓徳院は12月11日・12日が休み", "Entoku-in closed 11–12 December",
                        "2026年12月11日（金）・12日（土）は、行事のため圓徳院は一日休みです（公式サイト）。高台寺は拝観できます。",
                        "Entoku-in is closed all day on 11 and 12 December 2026 for an event (official site). Kodai-ji itself is open.",
                        url="https://www.kodaiji.com/entoku-in/", to="2026-12-12")]),
    yasaka=dict(
        name=T("八坂神社と円山公園", "Yasaka Shrine and Maruyama Park"), kind=T("神社・公園", "Shrine & park"),
        blurb=T("祇園の「八坂さん」。四条通の突き当たりの朱色の門が目印です。奥は円山公園。",
                "Gion’s “Yasaka-san”, marked by the vermilion gate at the end of Shijo-dori. Maruyama Park is behind it."),
        lat=35.00366, lng=135.77856,
        body=T("八坂神社（やさかじんじゃ）と円山公園（まるやまこうえん）\n\n祇園の東の端にある神社で、京都の人は「八坂さん」と呼びます。四条通の突き当たりに立つ朱色の西楼門が目印。7月の祇園祭は、この神社のお祭りです。\n\n境内を東へ抜けると円山公園。まん中に大きな「祇園しだれ桜」があり、春は夜にライトアップされます。公園の北には知恩院（ちおんいん）の大きな三門（国宝）があります。\n\n境内は自由にお参りできます。",
               "Yasaka Shrine and Maruyama Park\n\nThe shrine at the eastern end of Gion, “Yasaka-san” to people in Kyoto. Its vermilion west gate stands at the end of Shijo-dori. The Gion Festival in July is this shrine’s festival.\n\nWalk east through the grounds into Maruyama Park, with its huge weeping cherry in the middle, lit up at night in spring. North of the park is the massive Sanmon gate of Chion-in, a National Treasure.\n\nThe shrine grounds are free to enter."),
        gmaps=[gm("八坂神社", "Yasaka Shrine", 35.00366, 135.77856, "八坂神社"), gm("円山公園", "Maruyama Park", 35.00380, 135.78000, "円山公園 京都")],
        links=[link("official", "八坂神社 公式サイト", "Yasaka Shrine (official)", "https://www.yasaka-jinja.or.jp/")],
        info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    nanzenji=dict(
        name=T("南禅寺", "Nanzen-ji Temple"), kind=T("お寺", "Temple"),
        blurb=T("上に登れる大きな三門と、レンガ造りの水路閣。境内は無料で歩けます。",
                "A huge gate you can climb, and the brick Suirokaku aqueduct. The grounds are free to walk."),
        lat=35.01136, lng=135.79348,
        body=T("南禅寺（なんぜんじ）\n\n歌舞伎で石川五右衛門が「絶景かな」と言う大きな三門は、急な階段で上に登れて、京都の町と東山を見渡せます。\n\n境内の奥には、明治時代に琵琶湖の水を京都へ引くために造られたレンガの水路閣（すいろかく）。アーチの上を、今も水が流れています。方丈庭園は小堀遠州の作と伝わる石の庭です。\n\n境内と水路閣は無料。三門と方丈庭園は、それぞれ拝観料がかかります。",
               "Nanzen-ji Temple\n\nYou can climb the huge Sanmon gate, famous from a kabuki play, by a steep staircase for a view over the city and the Higashiyama hills.\n\nAt the back of the grounds stands the brick Suirokaku aqueduct, built in the Meiji era to bring water from Lake Biwa to Kyoto. Water still runs along the top of its arches. The Hojo garden is a rock garden attributed to Kobori Enshu.\n\nThe grounds and aqueduct are free. The gate and the Hojo garden each have their own fee."),
        gmaps=[gm("南禅寺", "Nanzen-ji", 35.01136, 135.79348, "南禅寺"), gm("水路閣", "Suirokaku", 35.01080, 135.79470, "南禅寺 水路閣")],
        links=[link("official", "南禅寺 公式サイト（拝観案内）", "Nanzen-ji (official, Japanese)", "https://nanzenji.or.jp/about_rinzaishu/visit")],
        info=info([row("hours", "3〜11月 8:40〜17:00、12〜2月 8:40〜16:30。受付は20分前まで", "Mar–Nov 8:40–17:00; Dec–Feb 8:40–16:30. Last entry 20 min before"),
                   row("closed", "12月28〜31日は拝観できません", "No admission 28–31 December"),
                   row("fee", "三門 一般600円、方丈庭園 一般600円、南禅院 一般500円（境内は無料）", "Sanmon gate ¥600, Hojo garden ¥600, Nanzen-in ¥500 per adult (grounds free)"),
                   row("train", "地下鉄東西線 蹴上駅から歩いて約10分（三条京阪→蹴上 約4分・220円）", "About 10 min on foot from Keage Station on the Tozai subway line (Sanjo Keihan → Keage: about 4 min, ¥220)")],
                  "南禅寺 公式サイト（拝観案内）。地下鉄の時間と運賃は乗換案内。蹴上駅からの徒歩は地図で測った目安")),
    eikando=dict(
        name=T("永観堂（禅林寺）", "Eikan-do (Zenrin-ji)"), kind=T("お寺", "Temple"),
        blurb=T("「もみじの永観堂」。受付は16:00まで。秋の夜のライトアップは、昼とは別の券で17:30から。",
                "“Eikan-do of the maples”. Last entry 16:00. The autumn light-up is a separate ticket, from 17:30."),
        lat=35.01445, lng=135.79452,
        body=T("永観堂（えいかんどう）\n\n古くから「もみじの永観堂」と呼ばれる紅葉の名所です。お堂が渡り廊下でつながっていて、靴を脱いで上がり、山の斜面に沿って奥の阿弥陀堂まで歩きます。庭の放生池（ほうじょういけ）には、もみじと山の上の多宝塔が映ります。\n\n秋の寺宝展の期間は拝観料が上がり、夜はライトアップがあります。昼と夜は入れ替え制で、券も別です。券は当日に窓口で買うものだけです。",
               "Eikan-do (Zenrin-ji)\n\nLong known as “Eikan-do of the maples”. The halls are joined by covered corridors: you take off your shoes and walk along the hillside to the Amida hall at the far end. The maples and the hilltop pagoda are reflected in the pond in the garden.\n\nDuring the autumn treasure exhibition the fee goes up and there is an evening light-up. Day and night are separate sessions with separate tickets, sold only at the gate on the day."),
        gmaps=[gm("永観堂", "Eikan-do", 35.01445, 135.79452, "永観堂 禅林寺")],
        links=[link("official", "永観堂 拝観のご案内", "Eikan-do visitor info (Japanese)", "https://www.eikando.or.jp/haikan.html")],
        info=info([row("hours", "秋の寺宝展（2026年11月11日〜12月6日）受付9:00〜16:00（17:00閉門）。ライトアップ（11月20日〜12月6日）受付17:30〜20:30（21:00閉門）。昼と夜は入れ替え制",
                       "Autumn exhibition (11 Nov – 6 Dec 2026): entry 9:00–16:00 (gates close 17:00). Light-up (20 Nov – 6 Dec): entry 17:30–20:30 (close 21:00). Day and night are separate sessions", until=AUTUMN_END),
                   row("fee", "秋の寺宝展 一般1,500円・中高生800円、ライトアップ 中高生以上1,000円", "Autumn exhibition ¥1,500 (junior/senior high ¥800); light-up ¥1,000 (junior high and up)", until=AUTUMN_END),
                   row("hours", "秋の寺宝展以外 受付9:00〜16:00（17:00閉門）、年中無休", "Outside the autumn exhibition: entry 9:00–16:00 (gates close 17:00), open every day"),
                   row("fee", "秋の寺宝展以外 一般1,000円、中高生600円、小学生200円", "Outside the autumn exhibition: ¥1,000 adults, ¥600 junior/senior high, ¥200 elementary")],
                  "永観堂 公式サイト（拝観のご案内）"),
        caution=T("三脚・一脚は使えません。境内は飲食禁止", "No tripods or monopods; no eating in the grounds"),
        notices=[notice("受付は16:00まで。三脚・一脚は使えません", "Last entry 16:00. No tripods or monopods",
                        "境内での飲食、ペットを連れての拝観、お堂の中の文化財の撮影もできません。秋の寺宝展とライトアップの券は前売りがなく、当日に窓口で買います（公式サイト）。",
                        "No eating in the grounds, no pets, and no photos of the artworks inside the halls. Tickets for the autumn exhibition and light-up are not sold in advance: buy them at the gate on the day (official site).",
                        url="https://www.eikando.or.jp/haikan.html")]),
    ginkakuji=dict(
        name=T("哲学の道と銀閣寺", "Philosopher’s Path and Ginkaku-ji"), kind=T("散歩道・お寺", "Walk & temple"),
        blurb=T("疏水沿いの散歩道を北へ歩いて銀閣寺へ。白い砂の庭と、こけら葺きの観音殿（銀閣）。17:00に閉まります（12〜2月は16:30）。",
                "Walk north along the canal path to Ginkaku-ji: a white sand garden and the shingle-roofed Silver Pavilion. Closes at 17:00 (16:30 Dec–Feb)."),
        lat=35.02690, lng=135.79837,
        body=T("哲学の道（てつがくのみち）と銀閣寺（ぎんかくじ）\n\n哲学の道は、永観堂の少し北の若王子橋（にゃくおうじばし）から銀閣寺橋まで、琵琶湖疏水に沿って続く約1.5kmの散歩道です。春は桜、秋は紅葉の並木になります。\n\n銀閣寺の正式な名前は慈照寺（じしょうじ）。室町幕府の8代将軍・足利義政の山荘がもとになったお寺です。入ってすぐ、白砂を段に盛った銀沙灘（ぎんしゃだん）と円すい形の向月台（こうげつだい）、その奥に観音殿（銀閣・国宝）。順路は山の上の展望所まで続き、境内と京都の町を見下ろせます。中を回るのに約30分です（公式サイトより）。\n\n拝観料は現金のほか、キャッシュレスでも払えます。",
               "Philosopher’s Path and Ginkaku-ji\n\nThe Philosopher’s Path follows the Lake Biwa Canal for about 1.5 km, from Nyakuoji bridge just north of Eikan-do to Ginkakuji bridge. It is lined with cherry trees in spring and coloured leaves in autumn.\n\nGinkaku-ji, officially Jisho-ji, began as the mountain villa of Ashikaga Yoshimasa, the eighth Muromachi shogun. Just inside are the Ginshadan, a terrace of raked white sand, and the cone-shaped Kogetsudai; behind them stands the Kannon hall, the Silver Pavilion (a National Treasure). The route climbs to a lookout over the grounds and the city. Allow about 30 minutes (from the official website).\n\nYou can pay the admission in cash or cashless."),
        gmaps=[gm("銀閣寺", "Ginkaku-ji", 35.02690, 135.79837, "銀閣寺 慈照寺"), gm("哲学の道（若王子橋）", "Philosopher’s Path (south end)", 35.01539, 135.79580, "哲学の道 若王子橋")],
        links=[link("official", "銀閣寺 公式サイト（アクセス・拝観）", "Ginkaku-ji (official, Japanese)", "https://www.shokoku-ji.jp/ginkakuji/access/")],
        info=info([row("hours", "3月1日〜11月30日 8:30〜17:00、12月1日〜2月末 9:00〜16:30。年中無休", "1 Mar – 30 Nov 8:30–17:00; 1 Dec – end of Feb 9:00–16:30. Open every day"),
                   row("fee", "大人（高校生以上）1,000円、小・中学生500円", "¥1,000 adults (high school and up), ¥500 elementary/junior high"),
                   row("hours", "秋の特別拝観（東求堂など、2026年11月1日〜12月5日）：10:00・11:00・12:00・13:30・14:30・15:30から約30分、各回約20名。当日、本堂前の申込表に名前を書きます。2,000円（拝観料は別）",
                       "Autumn special viewing (Togudo and more, 1 Nov – 5 Dec 2026): about 30 min from 10:00, 11:00, 12:00, 13:30, 14:30 and 15:30, about 20 people each. Sign up on the day at the main hall. ¥2,000 on top of admission; guided in Japanese", until="2026-12-05"),
                   row("train", "帰りは市バス「銀閣寺道」から（5・7・32・203・204系統など、230円）。参道を下って歩いて約10分", "Way back: city buses from “Ginkakuji-michi” (routes 5, 7, 32, 203, 204 and others, ¥230), about 10 min on foot down the approach")],
                  "銀閣寺（相国寺）公式サイト（アクセス・拝観）。秋の特別拝観とバスの系統は2026-11-21の確認、市バスの運賃は2026-11-20に京都市交通局で確認。哲学の道の長さと歩く時間は地図で測った目安",
                  tip=T("どの系統のバスがどこを通るかは確かめていません。バス停の案内で、行き先（四条河原町・三条京阪・京都駅）を見てから乗ってください。", "We haven’t checked which bus route goes where. Read the sign at the stop for your destination (Shijo-Kawaramachi, Sanjo-Keihan or Kyoto Station) before you board.")),
        _extra=[cc("ginkakuji-1.jpg", "Jmhullot", "CC BY 3.0", "File:Ginkakuji Fall1.jpg"),
                cc("ginkakuji-2.jpg", "Jmhullot", "CC BY 3.0", "File:Ginkakuji Sand Garden.jpg"),
                cc("ginkakuji-3.jpg", "Stephan Ridgway", "CC BY 2.0", "File:Philosophers Walk, Kyoto (49073313687).jpg"),
                cc("ginkakuji-4.jpg", "Yiannis Theologos Michellis", "CC0", "File:Japan Spring Down the Philosopher's Path (14164491752).jpg")]),
    kurodani=dict(
        name=T("金戒光明寺（くろ谷さん）", "Konkai Komyo-ji (Kurodani)"), kind=T("お寺", "Temple"),
        blurb=T("京都の人が「くろ谷さん」と呼ぶ大きなお寺。石段の上の山門が目印です。秋の夜は庭のライトアップがあります。",
                "A large temple people in Kyoto call “Kurodani-san”, with a great gate at the top of stone steps. In autumn the garden is lit up at night."),
        lat=35.01975, lng=135.78838,
        body=T("金戒光明寺（こんかいこうみょうじ）\n\n浄土宗の大きなお寺で、幕末には京都守護職・会津藩の本陣が置かれました。石段の上に立つ山門は見上げるほどの大きさです。境内は高台にあって、京都の町が見えます。\n\n境内は自由に歩けます。秋は夜の特別拝観があり、庭の池のまわりのもみじと竹林に明かりが入ります（夜は山門には上れません）。",
               "Konkai Komyo-ji\n\nA large Pure Land temple that served as headquarters of the Aizu clan, Kyoto’s guardians, at the end of the Edo period. The gate at the top of the stone steps towers over you. The grounds sit on a rise with a view over the city.\n\nThe grounds are free to walk. In autumn there is a special evening opening, with the maples around the garden pond and the bamboo grove lit up (the gate itself can’t be climbed at night)."),
        gmaps=[gm("金戒光明寺", "Konkai Komyo-ji", 35.01975, 135.78838, "金戒光明寺")],
        links=[link("official", "金戒光明寺 公式サイト", "Konkai Komyo-ji (official, Japanese)", "https://www.kurodani.jp/"),
               link("info", "金戒光明寺 特別夜間拝観", "Konkai Komyo-ji evening opening", "https://www.kurodani.jp/lightup/")],
        info=info([row("hours", "夜間特別拝観（2026年11月13日〜12月6日）17:30〜20:30（最終入場20:00）。予約はいりません", "Evening opening (13 Nov – 6 Dec 2026): 17:30–20:30 (last entry 20:00). No booking needed", until=AUTUMN_END),
                   row("fee", "夜間特別拝観 御影堂・大方丈・紫雲の庭 大人1,000円、栄摂院 大人800円、セット券 大人1,600円", "Evening opening: Main hall, Hojo & garden ¥1,000; Eisho-in ¥800; set ticket ¥1,600 (adults)", until=AUTUMN_END),
                   row("hours", "ふだんは境内を自由に歩けます。お堂の受付は9:00〜16:00（公式サイトの下に書かれた受付時間。拝観の時間としては要確認）", "The grounds are normally free to walk. Hall reception 9:00–16:00 (the reception hours printed at the foot of the official site; unconfirmed as visiting hours)")],
                  "金戒光明寺 公式サイト（特別夜間拝観）。ふだんの時間はトップページ下の「受付時間 9時〜16時（閉堂）」だけで、拝観時間としての記載は見つからない")),
)

VIS, ARR = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time")

# 秋の夜、永観堂・金戒光明寺へ行く人への注意（期間が終わると消える）
EIKANDO_NIGHT = notice("秋の夜のライトアップは17:30から", "The autumn light-up starts at 17:30",
                       "ライトアップ（2026年は11月20日〜12月6日）は昼とは別の券で、受付は17:30〜20:30。昼に入った人は、いったん出てから並び直します。",
                       "The light-up (20 Nov – 6 Dec in 2026) is a separate ticket, with entry from 17:30 to 20:30. If you visited in the daytime you leave and queue again.",
                       url="https://www.eikando.or.jp/haikan.html", to=AUTUMN_END)
DARK_AT_SIX = notice("11月〜2月の朝6時はまだ暗い", "At 6:00 it is still dark from November to February",
                     "この時期の日の出は6時すぎ〜7時すぎです。暗い道や石段では足もとに気をつけて。写真が目当ての日は、明るくなる時間も考えて出発を決めてください。",
                     "Sunrise in these months is between just after 6:00 and just after 7:00. Watch your step on dark lanes and stone steps. If you’re here for photos, plan your start around the light.",
                     frm="2026-11-01", to="2027-02-28")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
#   order の1件 = (スポットの id, 時間の見出し, 時間（日本語）, 時間（英語）, このコースでの行き方・過ごし方)
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="higashiyama.json",
        note="「9〜10時に出発」コース。三条を9:15ごろ出て、京阪で清水五条へ。清水寺→産寧坂・二年坂→八坂の塔→（お昼）→高台寺→八坂神社→南禅寺→哲学の道と銀閣寺まで歩き、市バスで戻る（18時ごろ）。永観堂と金戒光明寺は時間割の外で、足したときの回り方は hints。",
        order=[
            ("kiyomizu", VIS, "9:50〜10:50", "9:50–10:50",
             T("三条駅から京阪電車で清水五条駅へ（約3分・180円）。五条坂から茶わん坂を上って、歩いて約25分です。三条から歩くと約45分。\n\n日中の清水寺は混みます。人の少ない舞台を見たい日は、一覧の上のボタンで「早朝に出発」に切り替えてください。",
               "Take the Keihan line from Sanjo to Kiyomizu-Gojo (about 3 min, ¥180), then walk up Gojo-zaka and Chawan-zaka, about 25 minutes. Walking all the way from Sanjo takes about 45.\n\nKiyomizu-dera is crowded in the daytime. If you want the stage with fewer people, switch to “Early start” with the buttons above the list.")),
            ("sanneizaka", VIS, "10:50〜11:35", "10:50–11:35",
             T("清水寺の門前から、産寧坂、二年坂の順に下ります。昼間はとても混むので、急がず店をのぞきながら。",
               "From the temple gate, walk down Sannenzaka and then Ninenzaka. It’s very crowded in the daytime, so take it slowly and look into the shops.")),
            ("yasakatower", VIS, "11:40", "11:40",
             T("二年坂を下りきる手前で左へ。八坂通に出ると、坂の先に塔が見えます。\n\nお昼は塔のまわりか、高台寺へ向かうねねの道のあたりで（11:50〜12:40）。人の多い場所なので、12時より前に入るのがおすすめです。",
               "Turn left before the bottom of Ninenzaka onto Yasaka-dori, and the pagoda is ahead up the slope.\n\nHave lunch around the pagoda or along Nene-no-michi on the way to Kodai-ji (11:50–12:40). It’s a busy area, so try to sit down before noon.")),
            ("kodaiji", VIS, "12:45〜13:40", "12:45–13:40",
             T("八坂の塔から歩いて約7分。ねねの道から石段（台所坂）を上がります。圓徳院まで見るなら、あと20分ほど。",
               "About 7 minutes on foot from Yasaka Pagoda: climb the stone steps (Daidokoro-zaka) from Nene-no-michi. Allow another 20 minutes if you add Entoku-in.")),
            ("yasaka", VIS, "13:50〜14:20", "13:50–14:20",
             T("ねねの道を北へ歩いて約10分。南の門から入って本殿へ。本殿の東が円山公園です。",
               "About 10 minutes north along Nene-no-michi. Enter by the south gate for the main hall; Maruyama Park is just east of it.")),
            ("nanzenji", VIS, "14:50〜15:25", "14:50–15:25",
             T("円山公園から知恩院の三門の前を通り、北へ歩いて約30分。歩くのがつらくなってきたら、地下鉄の東山駅から蹴上駅まで1駅乗れます。\n\n銀閣寺が17:00に閉まるので、ここは35分ほど。三門に上るか、方丈庭園に入るか、どちらか1つにして、水路閣を見てください。",
               "About 30 minutes’ walk north from Maruyama Park, passing the Sanmon gate of Chion-in. If your legs are going, ride the subway one stop from Higashiyama to Keage.\n\nGinkaku-ji closes at 17:00, so allow about 35 minutes here: climb the gate or see the Hojo garden, not both, and walk to the aqueduct.")),
            ("eikando", VIS, "足す日は14:35〜15:20（高台寺を外して。受付16:00まで）", "if added, 14:35–15:20 (dropping Kodai-ji; last entry 16:00)",
             T("南禅寺から北へ歩いて約7分。このコースの時間割には入っていません。昼に入る日は、高台寺を外して1時間早く進めないと、銀閣寺に間に合いません。",
               "About 7 minutes’ walk north of Nanzen-ji. It isn’t in this course’s timetable: to go in during the day, drop Kodai-ji and run an hour earlier, or you won’t make Ginkaku-ji.")),
            ("ginkakuji", VIS, "16:05〜16:40（17:00に閉まります。12〜2月は16:30）", "16:05–16:40 (closes at 17:00; 16:30 from December to February)",
             T("南禅寺から永観堂の前を通り、哲学の道を歩いて約40分。\n\n見終わったら、参道を下りた「銀閣寺道」のバス停から市バスで四条河原町・三条のほうへ（230円）。戻るのは18時ごろを見ておいてください。",
               "About 40 minutes on foot from Nanzen-ji, past Eikan-do and along the Philosopher’s Path.\n\nAfterwards walk down the approach to the “Ginkakuji-michi” stop for a city bus back toward Shijo-Kawaramachi or Sanjo (¥230). Allow until about 18:00 to get back.")),
            ("kurodani", VIS, "足す日は17:05ごろ（境内）。秋の夜は18:45〜19:20", "if added, about 17:05 (grounds); 18:45–19:20 on autumn evenings",
             T("銀閣寺から南西へ歩いて約25分。このコースの時間割には入っていません。",
               "About 25 minutes’ walk southwest of Ginkaku-ji. It isn’t in this course’s timetable.")),
        ],
        sections=[dict(first="kiyomizu", last="yasakatower", day=0), dict(first="kodaiji", last="yasaka", day=2), dict(first="nanzenji", last="nanzenji", day=3),
                  dict(first="eikando", last="eikando", area=T("足すなら", "Optional"), title=T("もみじの永観堂", "Eikan-do of the maples")),
                  dict(first="ginkakuji", last="ginkakuji", day=3),
                  dict(first="kurodani", last="kurodani", area=T("足すなら", "Optional"), title=T("くろ谷さん", "Kurodani"))],
        default=["kiyomizu", "sanneizaka", "yasakatower", "kodaiji", "yasaka", "nanzenji", "ginkakuji"],
        extra_notices={"ginkakuji": [notice("12月〜2月は16:30に閉まります", "Closes at 16:30 from December to February",
                                             "この時期は、南禅寺を15:10に出てください（哲学の道を歩いて約40分）。または高台寺を外すと、全体が1時間早くなります。",
                                             "In these months leave Nanzen-ji at 15:10 (it’s about 40 minutes along the Philosopher’s Path). Or drop Kodai-ji, which moves everything an hour earlier.",
                                             frm="2026-12-01", to="2027-02-28")],
                       "eikando": [EIKANDO_NIGHT]},
        hints=[
            ("eikando", dict(any=["eikando"], andAny=["ginkakuji"]), None, AUTUMN_END,
             "ライトアップへ行く日は、銀閣寺を先に。16:40に銀閣寺を出て哲学の道を戻ると、17:10ごろ永観堂に着きます。受付は17:30から。秋の夜はとても混みます。",
             "On a light-up evening, see Ginkaku-ji first: leave it at 16:40, walk back down the Philosopher’s Path and you reach Eikan-do at about 17:10. Entry starts at 17:30, and autumn evenings are very busy."),
            ("eikando", dict(any=["eikando"], andAny=["kodaiji"]), "2026-12-07", None,
             "永観堂の受付は16:00まで。高台寺を外すと、南禅寺に13:50、永観堂に14:35、銀閣寺に16:00ごろ着けます。",
             "Eikan-do’s last entry is 16:00. Drop Kodai-ji and you reach Nanzen-ji at 13:50, Eikan-do at 14:35 and Ginkaku-ji at about 16:00."),
            ("kurodani", dict(any=["kurodani"], andAny=["eikando"]), None, AUTUMN_END,
             "永観堂のライトアップを18:30ごろ出て、歩いて約15分。夜間特別拝観の最終入場は20:00です。帰りは「岡崎道」のバス停から市バス、または地下鉄の東山駅まで歩いて約20分。",
             "Leave the Eikan-do light-up at about 18:30; it’s about 15 minutes on foot. Last entry to the evening opening is 20:00. To go back, take a city bus from “Okazaki-michi” or walk about 20 minutes to Higashiyama subway station."),
        ]),
    dict(
        id="early", file="higashiyama-early.json",
        note="「早朝に出発」コース。三条を5:10ごろ歩いて出て、八坂の塔と坂道を通り、6:00の開門に清水寺へ。8:00から二年坂のスターバックスで朝ごはん、9:00の開門に高台寺、八坂神社、南禅寺、（お昼）、永観堂、哲学の道と銀閣寺まで。金戒光明寺は時間割の外。5時台に三条から東山へ行く電車は京阪の5:04・5:24発（清水五条まで約3分）だけなので、歩きを基本にした。",
        order=[
            ("yasakatower", VIS, "5:35〜5:45", "5:35–5:45",
             T("三条から歩いて約30分。5:05ごろ出て、鴨川の東の道を南へ、祇園を抜けて八坂通へ入ります。この時間に動いている電車は京阪だけで（三条5:04発・5:24発、清水五条まで約3分・180円）、清水五条駅からは坂を上って約20分。歩くのがつらい日はタクシーで。\n\n清水寺が開くまでの間に、塔と坂道の写真を撮っていきます。",
               "About 30 minutes on foot from Sanjo. Leave at about 5:05, head south along the east side of the Kamo River, through Gion and onto Yasaka-dori. The only trains running this early are on the Keihan line (5:04 and 5:24 from Sanjo; about 3 min to Kiyomizu-Gojo, ¥180), and from that station it’s a 20-minute climb. Take a taxi if you’d rather not walk.\n\nPhotograph the pagoda and the lanes on your way, while you wait for Kiyomizu-dera to open.")),
            ("sanneizaka", VIS, "5:45（上り）、7:15〜8:50（下りと朝ごはん）", "5:45 (going up), 7:15–8:50 (coming down, and breakfast)",
             T("行きは、八坂の塔から二年坂、産寧坂と上って、清水寺の仁王門へ（約15分）。\n\n清水寺を出たら、同じ坂をゆっくり下ります。8:00になったら、二年坂のスターバックスで朝ごはんにして、9:00に高台寺が開くまで休みます。",
               "On the way up, walk from Yasaka Pagoda up Ninenzaka and Sannenzaka to Kiyomizu-dera’s Nio Gate (about 15 minutes).\n\nAfter the temple, come slowly back down the same lanes. At 8:00 the Starbucks on Ninenzaka opens: have breakfast and rest there until Kodai-ji opens at 9:00.")),
            ("kiyomizu", VIS, "6:00〜7:15", "6:00–7:15",
             T("6:00の開門に合わせて仁王門の前へ。舞台、奥の院、音羽の滝と、順路のとおりに回って1時間ほどです。",
               "Be at the Nio Gate for the 6:00 opening. Follow the route past the stage, the Okunoin hall and the Otowa waterfall: about an hour.")),
            ("kodaiji", VIS, "9:00〜10:00", "9:00–10:00",
             T("二年坂のスターバックスから、ねねの道を歩いて約5分。9:00の開門に合わせて入ります。圓徳院も合わせて1時間ほど。",
               "About 5 minutes along Nene-no-michi from the Starbucks on Ninenzaka. Go in when it opens at 9:00; an hour covers Entoku-in as well.")),
            ("yasaka", VIS, "10:10〜10:40", "10:10–10:40",
             T("ねねの道を北へ歩いて約10分。南の門から入って本殿へ。本殿の東が円山公園です。",
               "About 10 minutes north along Nene-no-michi. Enter by the south gate for the main hall; Maruyama Park is just east of it.")),
            ("nanzenji", VIS, "11:10〜12:05", "11:10–12:05",
             T("円山公園から知恩院の三門の前を通り、北へ歩いて約30分。朝から歩いているので、地下鉄の東山駅から蹴上駅まで1駅乗ってもかまいません。\n\n三門に上って、水路閣まで歩きます。お昼は南禅寺の参道か、永観堂へ向かう道のあたりで（12:05〜13:00）。",
               "About 30 minutes’ walk north from Maruyama Park, passing the Sanmon gate of Chion-in. You’ve been walking since dawn, so feel free to ride the subway one stop from Higashiyama to Keage.\n\nClimb the gate and walk to the aqueduct. Have lunch on the approach to Nanzen-ji or on the way to Eikan-do (12:05–13:00).")),
            ("eikando", VIS, "13:05〜14:00", "13:05–14:00",
             T("南禅寺から北へ歩いて約7分。",
               "About 7 minutes’ walk north of Nanzen-ji.")),
            ("ginkakuji", VIS, "14:40〜15:25", "14:40–15:25",
             T("永観堂から哲学の道を歩いて約35分。途中にベンチがあるので、休みながら。\n\n見終わったら、参道を下りた「銀閣寺道」のバス停から市バスで四条河原町・三条のほうへ（230円）。夜まで時間があるので、いったん宿で休めます。",
               "About 35 minutes along the Philosopher’s Path from Eikan-do, with benches along the way.\n\nAfterwards walk down the approach to the “Ginkakuji-michi” stop for a city bus back toward Shijo-Kawaramachi or Sanjo (¥230). There’s time to rest at your lodging before the evening.")),
            ("kurodani", VIS, "足す日は15:50〜16:20", "if added, 15:50–16:20",
             T("銀閣寺から南西へ歩いて約25分。このコースの時間割には入っていません。帰りは「岡崎道」のバス停から市バス、または地下鉄の東山駅まで歩いて約20分。",
               "About 25 minutes’ walk southwest of Ginkaku-ji. It isn’t in this course’s timetable. To go back, take a city bus from “Okazaki-michi” or walk about 20 minutes to Higashiyama subway station.")),
        ],
        sections=[dict(first="yasakatower", last="kiyomizu", day=0), dict(first="kodaiji", last="yasaka", day=2), dict(first="nanzenji", last="eikando", day=3),
                  dict(first="ginkakuji", last="ginkakuji", day=4),
                  dict(first="kurodani", last="kurodani", area=T("足すなら", "Optional"), title=T("くろ谷さん", "Kurodani"))],
        default=["yasakatower", "sanneizaka", "kiyomizu", "kodaiji", "yasaka", "nanzenji", "eikando", "ginkakuji"],
        extra_notices={"yasakatower": [DARK_AT_SIX], "eikando": [EIKANDO_NIGHT]},
        hints=[]),
]

NOTE_HEAD = "京都・東山の1日ルート（higashiyama/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（higashiyama.json＝9〜10時に出発、higashiyama-early.json＝早朝に出発）。このファイル："
NOTE_TAIL = " 「哲学の道と銀閣寺」は Toshi がまだ行っていない場所（写真は Wikimedia Commons で photos の要素が {file, credit}、文章は公式サイトの情報だけ）。 写真は Toshi の写真ライブラリから選んだもの（長辺1600px・位置情報なし）。info.source は確認した出典、info.checked は確認日、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。入口で困ること（休み・撮影禁止・入口の場所）は caution と head つきの notices。plan.defaultPicks は最初から選ばれている場所で、各スポットの「おすすめ◯◯時間」はこの組み合わせの時間割。このファイルは scripts/build_higashiyama_data.py で作る（直接直さない）。"


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    spots = []
    for sid, (lj, le), tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        text = T(body["ja"] + ("\n\n" + go["ja"] if go else "") + f"\n\n{lj}：{tj}",
                 body["en"] + ("\n\n" + go["en"] if go else "") + f"\n\n{le}: {te}")
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out["text"] = text
        out["photos"] = photos(sid, out.pop("_extra", None))
        out["notices"] = c.get("extra_notices", {}).get(sid, []) + out.get("notices", [])
        spots.append(out)
    auto = c.get("auto", [])
    secs = []
    for s in c["sections"]:
        d = {"first": NO[s["first"]], "last": NO[s["last"]]}
        if "day" in s:
            d["day"] = s["day"]
        else:
            d["area"], d["title"] = s["area"], s["title"]
        secs.append(d)
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": secs,
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は1日で無理なく回れる組み合わせ（時間割どおり）。それ以外は時間割の外で、足したときの回り方は各スポットの文章と hints（from〜to の間だけ出る）。",
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
