#!/usr/bin/env python3
"""京都から日帰り 湖東の紅葉のデータを書き出す（2コース）。

使い方: python3 scripts/build_higashiomi_data.py   → そのあと python3 scripts/sync_higashiomi.py
- data/routes/higashiomi.json        ＝ コース「太郎坊宮・永源寺」（eigenji。最初に開く）
    三条9:44発 → 近江八幡で近江鉄道 → 太郎坊宮 → 八日市からバスで永源寺（遅めのお昼）→ 近江八幡・安土 → タクシーで教林坊のライトアップ → 三条20:32
- data/routes/higashiomi-sanzan.json ＝ コース「湖東三山」（sanzan）
    三条8:22発（土日祝8:10）→ 彦根駅10:00の紅葉シャトルバス → 西明寺（門前でお昼）→ 百済寺 → 金剛輪寺 → 彦根17:30 → 三条19:00
    教林坊は「選んで回る」で足せる（最初は外してある）
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/higashiomi/<スポットのid>-<番号>.jpg を番号の順に全部使う（湖東三山コースの1番だけ omihachimaneki-1.jpg を1枚）
- 2026-11-22 作り直し。時刻・料金・休みは公式サイトと乗換案内で確かめ、開いたページは data の sources に書いた
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/higashiomi"
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


def info(rows, tip=None, cash=False, verified=True):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def photos(pid, extra=None):
    # extra: ネットから借りた写真（{"file", "credit": {"author", "license", "page"}}）。写真の上に撮影者とライセンスが出る
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def cc(file, author, license, title):
    return {"file": file, "credit": {"author": author, "license": license, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


# ---- リンク ----
YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
EIGENJI_BUS = link("timetable", "近江鉄道バス 永源寺へのアクセス（時刻表）", "Ohmi bus to Eigenji (timetable, Japanese)", "https://www.ohmitetudo.co.jp/bus/access/eigenji/")
SHUTTLE = link("timetable", "湖東三山 紅葉シャトルバス（近江鉄道・湖国バス）", "Koto Sanzan autumn shuttle bus (Japanese)", "https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/")
SHUTTLE_BOOK = link("info", "シャトルバスのWeb予約（もみじきっぷ）", "Book the shuttle (Momiji Kippu, Japanese)", "https://kokokubus.rsvsys.jp/reservations/calendar?category=5")
KOTOSANZAN = link("info", "湖東三山観光振興協議会", "Koto Sanzan tourism council (Japanese)", "https://kotousanzan.jp/")
TAXI_LIST = link("info", "東近江市観光協会（タクシー会社の一覧）", "Higashiomi tourism: taxi companies (Japanese)", "https://www.higashiomi.net/guide/access.html")
OMI_MAP = link("info", "近江八幡のマップ（晩ごはんのティファニーなど）", "Omihachiman map (dinner and more)", "../omihachiman/")

# 期間（この日を過ぎると行が消える／注意が出る）
SHUTTLE_END = "2026-11-29"
AFTER_SHUTTLE = "2026-11-30"
EIGENJI_LU_END = "2026-11-28"
HYAKU_LU_END = "2026-11-30"
KYORIN_LU_END = "2026-12-06"
KYORIN_OPEN_END = "2026-12-15"
SPECIAL_END = "2026-12-13"

# ---- 教林坊（両コース共通の行と注意） ----
KYORIN_NOTICES = [
    notice("ライトアップは12月6日まで", "Illumination until 6 Dec",
           "2026年の夜のライトアップは12月6日（日）まで、17:30〜19:30（受付は19:00まで）。予約の案内はなく、拝観料は大人1,000円です。安土駅から歩くと約60分かかるので、行きも帰りもタクシーで。駅前にタクシーが待っているとは限らないので、前もって予約し、帰りの迎えの時間も決めておいてください。",
           "The 2026 evening illumination runs until Sunday 6 December, 17:30–19:30 (last entry 19:00). No booking is mentioned; adults ¥1,000. Azuchi Station is about 60 minutes away on foot, so take a taxi both ways. Taxis don’t always wait at the station: book ahead and arrange your pick-up time.",
           url="https://kyourinbo.jimdofree.com/", to=KYORIN_LU_END),
    notice("秋の公開は12月15日まで", "Autumn opening until 15 Dec",
           "ライトアップは12月6日で終わりました。昼の公開は12月15日まで、9:30〜16:30です。そのあとは次の春まで公開されません（春と秋だけの公開）。",
           "The illumination ended on 6 December. Daytime opening continues until 15 December, 9:30–16:30; after that the temple is closed until spring (it opens only in spring and autumn).",
           url="https://kyourinbo.jimdofree.com/", frm="2026-12-07", to=KYORIN_OPEN_END),
    notice("今は公開していません", "Not open now",
           "教林坊は春と秋の特別公開のときだけ入れます。2026年秋の公開は12月15日で終わりました。次の公開日は公式サイトで確かめてください。",
           "Kyorinbo opens only for special spring and autumn openings. The autumn 2026 opening ended on 15 December; check the official website for the next dates.",
           url="https://kyourinbo.jimdofree.com/", frm="2026-12-16"),
]
KYORIN_ROWS = [
    row("hours", "2026年秋の公開：11月1日〜12月15日の毎日 9:30〜16:30（ライトアップの期間は8:30から）", "Autumn 2026 opening: daily 1 Nov – 15 Dec, 9:30–16:30 (from 8:30 during the illumination)", until=KYORIN_OPEN_END),
    row("hours", "ライトアップ：12月6日まで 17:30〜19:30（受付は19:00まで）", "Illumination: until 6 Dec, 17:30–19:30 (last entry 19:00)", until=KYORIN_LU_END),
    row("fee", "大人1,000円、小中学生300円（11月1日〜12月15日）", "¥1,000 adults, ¥300 children (1 Nov – 15 Dec)"),
    row("taxi", "JR安土駅の北口からタクシーで約10分・2,500円前後（教林坊の公式サイトの目安）", "About 10 min by taxi from the north exit of JR Azuchi Station, around ¥2,500 (the temple’s own estimate)"),
]
KYORIN_LINKS = [link("official", "教林坊 公式サイト", "Kyorinbo (official, Japanese)", "https://kyourinbo.jimdofree.com/"), TAXI_LIST, YAHOO]
KYORIN_EXTRA_JA = ("三脚・一脚は使えません。写真を撮るための長い滞在も断られています（公式サイト）。\n\n"
                   "タクシーは、東近江市観光協会の一覧にある滋賀第一交通 近江八幡営業所（0748-37-4000）など。")
KYORIN_EXTRA_EN = ("Tripods and monopods are not allowed, and long stays just to take photos are discouraged (official website).\n\n"
                   "For taxis, the Higashiomi tourism association lists Shiga Daiichi Kotsu, Omi-Hachiman office (0748-37-4000), among others.")
KYORIN_TIP = T("時刻・料金は教林坊の公式サイト（公開日・ライトアップ・アクセスのページ）と乗換案内で、2026年11月22日に確認しました。",
               "Hours and fees checked on the Kyorinbo website (opening, illumination and access pages); trains on a route planner, 22 Nov 2026.")

# =====================================================================
# コース1：太郎坊宮・永源寺（eigenji）
# =====================================================================
A = [
    dict(id="omihachimaneki", name=T("京都から近江八幡へ（近江鉄道に乗り換え）", "Kyoto to Omi-Hachiman (change to the Ohmi Railway)"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("三条から地下鉄で山科へ出て、JRの新快速で近江八幡へ。同じ駅で近江鉄道に乗り換えて、太郎坊宮前まで1時間15分ほど。",
                 "From Sanjo, subway to Yamashina, then the JR Special Rapid to Omi-Hachiman, where you change to the Ohmi Railway. About 1 hour 15 minutes to Taroubougu-mae."),
         lat=35.12280, lng=136.10280,
         text=T("京都から近江八幡へ\n\n"
                "三条京阪9:44発（土日祝は9:43発）の地下鉄東西線「六地蔵（ろくじぞう）」行きで山科（やましな）へ。10:06発（土日祝は10:05発）の新快速「近江塩津（おうみしおつ）」行きに乗り換えて、近江八幡に10:35（土日祝は10:34）に着きます。京都市役所前からは同じ電車がその2分ほど前に出ます。\n\n"
                "近江八幡で近江鉄道の八日市線（ようかいちせん）に乗り換え（7分）。10:42発の電車で、太郎坊宮前（たろうぼうぐうまえ）に10:57に着きます。地下鉄260円＋JR590円＋近江鉄道390円で、合わせて1,240円。近江鉄道は2026年3月からICOCAなどの交通系ICカードで乗れます。\n\n"
                "地下鉄は「六地蔵」行きに乗ってください。「びわ湖浜大津」行きは京阪山科駅に着くので、乗り換えに少し歩き、運賃も130円高くなります。京都駅から乗るなら、10:00発の同じ新快速で近江八幡まで680円です。\n\n"
                "このあと太郎坊宮から永源寺へのバスに乗るまで、食べる店はほとんどありません。お昼は永源寺で14時ごろになるので、朝ごはんはしっかり、おやつを持っていくと安心です。\n\n"
                "おすすめ出発時間：三条京阪 9:44（土日祝は9:43）",
                "Kyoto to Omi-Hachiman\n\n"
                "Take the Tozai subway line from Sanjo Keihan at 9:44 (9:43 at weekends and holidays), bound for Rokujizo, to Yamashina. Change to the 10:06 (10:05) Special Rapid bound for Omi-Shiotsu and you reach Omi-Hachiman at 10:35 (10:34). The same subway leaves Kyoto Shiyakusho-mae about 2 minutes earlier.\n\n"
                "At Omi-Hachiman, change to the Ohmi Railway Yokaichi Line (7 minutes). The 10:42 train reaches Taroubougu-mae at 10:57. Subway ¥260 + JR ¥590 + Ohmi Railway ¥390 = ¥1,240. Since March 2026 you can ride the Ohmi Railway with ICOCA and other transport IC cards.\n\n"
                "Take a subway bound for Rokujizo. The one for Biwako-Hamaotsu stops at Keihan Yamashina instead, a short walk away, and costs ¥130 more. From Kyoto Station, the same 10:00 Special Rapid takes you to Omi-Hachiman for ¥680.\n\n"
                "There’s almost nowhere to eat until Eigenji, and lunch there will be around 14:00. Have a good breakfast and bring a snack.\n\n"
                "Recommended departure: Sanjo Keihan 9:44 (9:43 at weekends and holidays)"),
         gmaps=[gm("近江八幡駅", "Omi-Hachiman Station", 35.12280, 136.10280, "近江八幡駅")],
         links=[YAHOO, link("info", "近江鉄道線のICOCA", "ICOCA on the Ohmi Railway (Japanese)", "https://www.ohmitetudo.co.jp/railway/icoca-2025/")],
         info=info([row("train", "三条京阪 9:44（土日祝9:43）→ 山科 10:06（10:05）新快速 → 近江八幡 10:35（10:34）→ 近江鉄道 10:42 → 太郎坊宮前 10:57。1,240円",
                        "Sanjo Keihan 9:44 (weekends 9:43) → Yamashina 10:06 (10:05) Special Rapid → Omi-Hachiman 10:35 (10:34) → Ohmi Railway 10:42 → Taroubougu-mae 10:57. ¥1,240"),
                    row("train", "京都駅から：10:00発の新快速で近江八幡 10:35（土日祝10:34）、680円", "From Kyoto Station: 10:00 Special Rapid to Omi-Hachiman 10:35 (10:34), ¥680")],
                   tip=T("2026年11月25日（水）と28日（土）のダイヤを乗換案内で確かめました。", "Checked on a route planner for Wednesday 25 and Saturday 28 November 2026."))),
    dict(id="taroubouekimae", name=T("近江鉄道 太郎坊宮前駅", "Ohmi Railway Taroubougu-mae Station"), kind=T("駅", "Station"),
         blurb=T("駅を出ると、正面にとがった形の太郎坊山（赤神山）。田んぼの中の道を、山のふもとまで歩いて約20分。",
                 "Out of the station, the pointed peak of Mt. Taroubou (Akagami-yama) is right ahead. About 20 minutes on foot through the fields to the foot of the mountain."),
         lat=35.10853, lng=136.18378,
         text=T("近江鉄道 太郎坊宮前駅（たろうぼうぐうまええき）\n\n"
                "小さな無人駅です。駅から太郎坊宮までは歩いて約20分（太郎坊宮の公式サイト）。田んぼの向こうに、岩がむき出しになったとがった山が見えてきます。大きな鳥居をくぐって、参道を山の方へ。\n\n"
                "帰りの電車（八日市方面）は1時間に2本、昼は毎時41分と59分ごろです。12:41か12:59の電車で八日市へ行けば、どちらも13:15の永源寺行きのバスに間に合います。\n\n"
                "おすすめ到着時間：10:57",
                "Ohmi Railway Taroubougu-mae Station\n\n"
                "A small unstaffed station. The shrine is about 20 minutes on foot (shrine website). Across the rice fields rises a sharp, rocky peak. Pass under the big torii and follow the approach towards the mountain.\n\n"
                "Trains on to Yokaichi run twice an hour, around :41 and :59 past the hour at midday. The 12:41 and the 12:59 both connect with the 13:15 bus to Eigenji.\n\n"
                "Recommended arrival: 10:57"),
         gmaps=[gm("太郎坊宮前駅", "Taroubougu-mae Station", 35.10853, 136.18378, "太郎坊宮前駅")],
         links=[YAHOO],
         info=info([row("train", "近江八幡 → 太郎坊宮前 15分・390円。太郎坊宮前 → 八日市 4〜5分・160円（昼は毎時41分・59分ごろ）",
                        "Omi-Hachiman → Taroubougu-mae 15 min, ¥390. Taroubougu-mae → Yokaichi 4–5 min, ¥160 (around :41 and :59 at midday)")],
                   tip=T("乗換案内（2026年11月25日・28日のダイヤ）で確認しました。", "Checked on a route planner (25 and 28 Nov 2026 timetables)."))),
    dict(id="taroubou", name=T("太郎坊宮（阿賀神社）", "Taroubou-gu (Aga Shrine)"), kind=T("神社", "Shrine"),
         blurb=T("742段の石段を登った先に、紅葉と近江の平野を見渡す本殿。大きな岩が割れた「夫婦岩」の間を通ってお参りします。",
                 "Climb 742 stone steps to a main hall above the autumn leaves and the Omi plain. You reach it by squeezing between the split “Meoto-iwa” rocks."),
         lat=35.11819, lng=136.18244,
         text=T("太郎坊宮（たろうぼうぐう）阿賀神社（あがじんじゃ）\n\n"
                "赤神山の中腹にある、勝運の神様の神社です。ふもとから本殿までは742段の石段。赤い鳥居が続く参道や、木の格子に囲まれた長い石段があり、紅葉の時期はもみじのトンネルになります。\n\n"
                "本殿の手前には、大きな岩が二つに割れた「夫婦岩（めおといわ）」。すき間を通ってお参りします。本殿の前からは、八日市の町と近江の平野が遠くまで見渡せます。\n\n"
                "石段は急な所もあるので、歩きやすい靴で。上り下りと駅までの道で1時間半あまり見ておくと、あわてずに済みます。参拝はいつでもでき、拝観料はいりません。お守りの授与などの受付は9:00〜17:00です。\n\n"
                "駅に戻ったら、12:41か12:59の電車で八日市（ようかいち）へ。\n\n"
                "おすすめ訪問時間：11:15〜12:35",
                "Taroubou-gu (Aga Shrine)\n\n"
                "A shrine to the god of victory, halfway up Mt. Akagami. From the foot of the mountain it is 742 stone steps to the main hall, past red torii and a long stairway enclosed in wooden lattice; in autumn it becomes a tunnel of maples.\n\n"
                "Just below the main hall are the Meoto-iwa, a huge boulder split in two; you pass through the gap to pray. From the hall you can see over Yokaichi and far across the Omi plain.\n\n"
                "Some steps are steep, so wear good shoes. Allow a good hour and a half for the climb and the walk to and from the station. The shrine is open at all times and free; the office (amulets and so on) is open 9:00–17:00.\n\n"
                "Back at the station, take the 12:41 or 12:59 train to Yokaichi.\n\n"
                "Recommended visit time: 11:15–12:35"),
         gmaps=[gm("太郎坊宮", "Taroubou-gu", 35.11819, 136.18244, "太郎坊宮 阿賀神社")],
         links=[link("official", "太郎坊宮 公式サイト", "Taroubou-gu (official, Japanese)", "https://tarobo.or.jp/")],
         info=info([row("hours", "参拝はいつでも（24時間）。社務の受付 9:00〜17:00（ご祈祷などは16:00まで）", "Open 24 hours. Shrine office 9:00–17:00 (prayers until 16:00)"),
                    row("fee", "無料（拝観料・駐車料なし）", "Free (no admission or parking fee)")],
                   tip=T("ふもとから本殿まで742段。車なら山上の第一駐車場から約260段です（太郎坊宮の公式サイト、2026年11月22日に確認）。",
                         "742 steps from the foot of the mountain; about 260 from the upper car park (shrine website, checked 22 Nov 2026)."))),
    dict(id="eigenji", name=T("永源寺", "Eigenji Temple"), kind=T("寺", "Temple"),
         blurb=T("愛知川の渓谷にある禅寺。山門と法堂のまわりが一面のもみじ。門前で遅めのお昼にして、夕方のバスまでゆっくり。",
                 "A Zen temple in the Echigawa valley, its great gate and lecture hall wrapped in maples. A late lunch by the gate, then take your time until the late-afternoon bus."),
         lat=35.08058, lng=136.31999,
         text=T("永源寺（えいげんじ）\n\n"
                "鈴鹿の山あいを流れる愛知川（えちがわ）のほとりにある、臨済宗永源寺派の大本山です。旦度橋（たんどばし）を渡り、石段を上ると大きな山門。その先の法堂や方丈のまわりを、たくさんのもみじが囲んでいます。紅葉は11月上旬から下旬で、中旬が色づきのピーク（永源寺の案内）。\n\n"
                "八日市駅の1番のりばから13:15発の近江鉄道バス（永源寺車庫行き）に乗り、「永源寺前」に13:43ごろ着（670円）。着いたらまずお昼を。永源寺のお知らせでは、紅葉の時期は食事処とキッチンカーが開いていて、うどん・そば・ぜんざいなどがあります（営業時間は要確認）。門前の茶店では名物の永源寺こんにゃくも。\n\n"
                "2026年秋は、ボランティアガイドの案内で山門と法堂に上がれる特別拝観が10:00・11:30・14:00にあります（1,500円・参拝志納料込み。11月18日の永源寺のお知らせ。いつまで行うか・申し込み方法は要確認）。11月18日のお知らせでは、山門の上から見るもみじが見ごろでした。14:00の回なら間に合います。\n\n"
                "帰りは永源寺前16:24発（土日祝は16:25発）のバスで八日市へ。教林坊に行かない日は、夕方のライトアップ（2026年は11月28日まで、17時から）を見てから帰ることもできます。\n\n"
                "おすすめ訪問時間：13:45〜16:20",
                "Eigenji Temple\n\n"
                "Head temple of the Eigenji school of Rinzai Zen, on the Echigawa river in the Suzuka hills. Cross the Tando bridge and climb to the great gate; beyond, the lecture hall and abbot’s quarters are wrapped in maples. The leaves turn from early to late November, peaking in mid-November (temple FAQ).\n\n"
                "Take the 13:15 Ohmi bus (for Eigenji Shako) from stop 1 at Yokaichi Station and get off at “Eigenji-mae” at about 13:43 (¥670). Have lunch first. The temple’s news page says a seasonal eatery and a food truck are open in the leaf season, with udon, soba, zenzai and the like (hours not confirmed). Tea houses by the gate sell the local Eigenji konnyaku.\n\n"
                "In autumn 2026, volunteer guides take visitors up into the great gate and lecture hall at 10:00, 11:30 and 14:00 (¥1,500 including admission; temple news of 18 Nov; end date and booking not confirmed). On 18 Nov the temple said the maples seen from the top of the gate were at their best; the 14:00 tour is within reach.\n\n"
                "Leave on the 16:24 bus from Eigenji-mae (16:25 at weekends and holidays). If you’re skipping Kyorinbo, you can stay for the evening illumination instead (until 28 Nov in 2026, from 17:00).\n\n"
                "Recommended visit time: 13:45–16:20"),
         gmaps=[gm("永源寺", "Eigenji", 35.08058, 136.31999, "永源寺 東近江市")],
         links=[link("official", "永源寺 公式サイト（お知らせ）", "Eigenji (official news, Japanese)", "https://eigenji-t.jp/haikan/"), EIGENJI_BUS],
         notices=[notice("11月は時間が変わります", "November hours differ",
                         "ふだんの参拝時間は9:00〜16:00ですが、11月は紅葉の時期のため変わります（永源寺の案内）。2026年11月の時間は公式サイトで見つけられませんでした（要確認）。",
                         "Usual hours are 9:00–16:00, but they change in November for the leaf season (temple FAQ). We couldn’t find the November 2026 hours on the website; please check.",
                         url="https://eigenji-t.jp/contact/", to="2026-11-30")],
         info=info([row("hours", "ふだんは9:00〜16:00。11月は変わる（2026年11月の時間は要確認）", "Usually 9:00–16:00; different in November (November 2026 hours not confirmed)"),
                    row("hours", "2026年秋のライトアップ：11月14日〜28日 17時から（金・土は20時まで。ほかの日の終わりの時間は要確認）",
                        "Autumn 2026 illumination: 14–28 Nov from 17:00 (until 20:00 on Fridays and Saturdays; other days not confirmed)", until=EIGENJI_LU_END),
                    row("hours", "山門・法堂の特別拝観：10:00・11:30・14:00、1,500円（参拝志納料込み。期間は要確認）",
                        "Gate and lecture-hall tour: 10:00, 11:30, 14:00, ¥1,500 incl. admission (end date not confirmed)", until="2026-11-30"),
                    row("fee", "参拝志納料 大人600円、中学生200円、小学生以下無料", "Admission ¥600 adults, ¥200 junior high, free for younger children"),
                    row("bus", "八日市駅1番のりば 13:15 → 永源寺前 13:43ごろ（670円）。帰りは永源寺前 16:24（土日祝16:25）→ 八日市駅 16:59（17:00）",
                        "Yokaichi stop 1 13:15 → Eigenji-mae about 13:43 (¥670). Back: Eigenji-mae 16:24 (weekends 16:25) → Yokaichi 16:59 (17:00)")],
                   tip=T("参拝志納料・紅葉の時期・11月の時間の変更は永源寺の公式サイト（よくある質問）、ライトアップと特別拝観は永源寺のお知らせ（2026年11月13日・18日・20日・21日）、バスは近江鉄道バスの時刻表と乗換案内で、2026年11月22日に確認しました。",
                         "Admission, leaf season and the November change from the temple FAQ; illumination and tours from the temple news (13, 18, 20 and 21 Nov 2026); buses from Ohmi bus’s timetable and a route planner. Checked 22 Nov 2026."),
                   verified=False)),
    dict(id="kyorinbo", name=T("教林坊（夜のライトアップ）", "Kyorinbo (evening illumination)"), kind=T("寺", "Temple"),
         blurb=T("春と秋だけ公開される、竹林と石の庭の小さなお寺。夜は、もみじと竹林がやわらかく照らされます。安土駅からタクシーで。",
                 "A small temple of bamboo and stone gardens, open only in spring and autumn. At night the maples and bamboo are softly lit. Taxi from Azuchi Station."),
         lat=35.13898, lng=136.16383, caution=T("駅からタクシー・12月6日まで", "Taxi from the station · until 6 Dec"),
         text=T("教林坊（きょうりんぼう）\n\n"
                "観音正寺のある繖山（きぬがさやま）のふもと、安土町石寺の山あいにある小さなお寺です。ふだんは公開されておらず、春と秋の特別公開のときだけ入れます。竹林の小道を抜けると、苔と巨石の庭。書院の丸窓や三日月の窓から見る庭も絵のようです。写真は2026年11月17日の夜のライトアップです。\n\n"
                "永源寺前16:24（土日祝16:25）のバスで八日市駅16:59、17:09の近江鉄道で近江八幡17:28、17:41のJR（米原行き）でひと駅、安土（あづち）に17:44着（バス670円・近江鉄道460円・JR190円）。北口からタクシーで約10分、18時ごろに着きます。タクシーは前もって予約し、帰りの迎えも頼んでおきましょう。\n\n"
                "帰りは安土19:28発の電車で山科へ（土日祝は近江八幡で19:37の新快速に乗り換え）、地下鉄に乗り換えて三条京阪に20:32（土日祝は20:30）着（940円）。三条・木屋町・先斗町（ぽんとちょう）のあたりは遅くまで開いている店が多いので、21〜22時まで晩ごはんを楽しめます。次の電車は19:50（土日祝は19:55）発で三条京阪20:53着。\n\n"
                "近江八幡で晩ごはんにするなら、19:28の電車をひと駅の近江八幡（19:32着）で降りて、北口から歩いて3分のティファニーへ（ディナーのラストオーダー20:00、火曜休み。近江八幡のマップの13番）。食後は21:13発の新快速で、山科で地下鉄に乗り換えて三条京阪に21:58着（平日。850円）。\n\n"
                + KYORIN_EXTRA_JA + "\n\nおすすめ訪問時間：18:00〜19:00",
                "Kyorinbo\n\n"
                "A small temple tucked in the hills of Ishidera, Azuchi, at the foot of Mt. Kinugasa. It is usually closed and opens only for special spring and autumn openings. A path through bamboo leads to a garden of moss and huge rocks, framed by the round and crescent-moon windows of the study hall. The photos show the illumination on 17 November 2026.\n\n"
                "Take the 16:24 bus from Eigenji-mae (16:25 at weekends) to Yokaichi (16:59), the 17:09 Ohmi Railway to Omi-Hachiman (17:28), and the 17:41 JR train for Maibara one stop to Azuchi (17:44). Bus ¥670, Ohmi Railway ¥460, JR ¥190. A taxi from the north exit takes about 10 minutes, so you arrive around 18:00. Book the taxi ahead, including the pick-up back.\n\n"
                "Head home on the 19:28 train from Azuchi to Yamashina (at weekends, change at Omi-Hachiman to the 19:37 Special Rapid), then the subway to Sanjo Keihan: 20:32 (20:30 at weekends), ¥940. Around Sanjo, Kiyamachi and Pontocho many places stay open late, so dinner can run to 21:00–22:00. The next train leaves at 19:50 (19:55 at weekends), reaching Sanjo Keihan at 20:53.\n\n"
                "For dinner in Omihachiman instead, get off the 19:28 train one stop later at Omi-Hachiman (19:32) and walk 3 minutes from the north exit to Tiffany (dinner last order 20:00, closed Tuesdays; no. 13 on our Omihachiman map). Afterwards the 21:13 Special Rapid and the subway from Yamashina get you to Sanjo Keihan at 21:58 (weekdays, ¥850).\n\n"
                + KYORIN_EXTRA_EN + "\n\nRecommended visit time: 18:00–19:00"),
         gmaps=[gm("教林坊", "Kyorinbo", 35.13898, 136.16383, "教林坊 近江八幡市安土町石寺1145"), gm("安土駅", "Azuchi Station", 35.14290, 136.13790, "安土駅")],
         links=KYORIN_LINKS + [OMI_MAP],
         notices=KYORIN_NOTICES,
         info=info(KYORIN_ROWS + [
             row("train", "行き：永源寺前 16:24（土日祝16:25）バス → 八日市 17:09 近江鉄道 → 近江八幡 17:41 JR → 安土 17:44（合わせて1,320円）",
                 "There: Eigenji-mae 16:24 (weekends 16:25) bus → Yokaichi 17:09 Ohmi Railway → Omi-Hachiman 17:41 JR → Azuchi 17:44 (¥1,320 in all)"),
             row("train", "帰り：安土 19:28 → 山科で地下鉄 → 三条京阪 20:32（土日祝20:30）、940円。次は19:50（土日祝19:55）→ 20:53。遅い便は22:33 → 23:49",
                 "Back: Azuchi 19:28 → subway at Yamashina → Sanjo Keihan 20:32 (weekends 20:30), ¥940. Next 19:50 (weekends 19:55) → 20:53. A late one: 22:33 → 23:49")],
             tip=KYORIN_TIP)),
]

A_PLAN = lambda NO: {
    "_note": "「選んで回る」の設定。近江八幡駅はいつも入る。太郎坊宮前駅は太郎坊宮を選ぶと入る。defaultPicks は時間割どおりの3か所（全部）。",
    "defaultMode": "pick",
    "picks": [NO["taroubou"], NO["eigenji"], NO["kyorinbo"]],
    "defaultPicks": [NO["taroubou"], NO["eigenji"], NO["kyorinbo"]],
    "auto": {str(NO["omihachimaneki"]): {"always": True}, str(NO["taroubouekimae"]): {"any": [NO["taroubou"]]}},
    "hints": [
        H(NO, "omihachimaneki", {"any": [NO["eigenji"]], "none": [NO["taroubou"]]},
          "太郎坊宮に寄らない日は、近江八幡10:42発の近江鉄道を終点の八日市（ようかいち）まで乗り（460円）、駅の1番のりば11:15発のバスで永源寺前に11:43ごろ着。永源寺でお昼にして、ゆっくり回れます。",
          "Skipping Taroubou-gu? Stay on the 10:42 Ohmi Railway to the end of the line at Yokaichi (¥460) and take the 11:15 bus from stop 1, reaching Eigenji-mae around 11:43. Lunch at Eigenji and take your time."),
        H(NO, "taroubou", {"any": [NO["taroubou"]], "none": [NO["eigenji"]]},
          "永源寺に行かない日は、太郎坊宮のあと近江鉄道で近江八幡へ戻り、八幡堀のあたりを歩いてお昼に（近江八幡のマップを見てください）。教林坊へは、夕方に近江八幡からJRでひと駅の安土へ。",
          "Not going to Eigenji? After the shrine, take the Ohmi Railway back to Omi-Hachiman, walk the canal district and have lunch there (see our Omihachiman map). For Kyorinbo, take JR one stop to Azuchi in the late afternoon."),
        H(NO, "eigenji", {"any": [NO["eigenji"]], "none": [NO["kyorinbo"]]},
          "教林坊に行かない日は、永源寺のライトアップ（17時から）を見てから帰れます。永源寺前18:24発（土日祝は18:16発）のバスに乗ると、近江鉄道・JR・地下鉄を乗り継いで三条京阪に20:32（土日祝20:30）着（1,980円）。",
          "Skipping Kyorinbo? Stay for Eigenji’s illumination (from 17:00). The 18:24 bus from Eigenji-mae (18:16 at weekends) connects by Ohmi Railway, JR and subway to Sanjo Keihan at 20:32 (20:30), ¥1,980.", to=EIGENJI_LU_END),
        H(NO, "eigenji", {"any": [NO["eigenji"]], "none": [NO["kyorinbo"]]},
          "教林坊に行かない日は、永源寺前16:24発（土日祝16:25発）のバスで八日市へ。近江鉄道で近江八幡に17:28、17:36の新快速で山科へ出て地下鉄に乗り換え、三条京阪に18:29（土日祝は18:33）着きます（1,980円）。",
          "Skipping Kyorinbo? Take the 16:24 bus (16:25 at weekends) to Yokaichi and the Ohmi Railway to Omi-Hachiman (17:28). The 17:36 Special Rapid gets you to Yamashina; change to the subway for Sanjo Keihan at 18:29 (18:33 at weekends), ¥1,980.", frm="2026-11-29"),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "none": [NO["eigenji"]]},
          "永源寺に寄らない日は、近江八幡から米原方面の普通電車でひと駅、安土へ。ライトアップは17:30からなので、17:20ごろ安土に着く電車で十分です。",
          "Not going to Eigenji? From Omi-Hachiman take a local train one stop towards Maibara to Azuchi. The illumination starts at 17:30, so a train reaching Azuchi around 17:20 is fine."),
    ]}

# =====================================================================
# コース2：湖東三山（sanzan）
# =====================================================================
SHUTTLE_OVER = notice("シャトルバスは11月29日で終わりました", "The shuttle bus ended on 29 Nov",
                      "2026年の紅葉シャトルバスは11月29日で終わりました。12月は、JR河瀬駅（かわせえき）から予約制の乗合タクシー「愛のりタクシー」で西明寺へ（毎時51分発・約15分・800円）。西明寺から金剛輪寺へも乗合タクシー（毎時56分発・約5分、料金は要確認）、金剛輪寺からJR稲枝駅（いなええき）へは毎時42分発（800円）。予約は乗る1時間前までに近江タクシー彦根営業所 0749-22-1111（「愛のりお願いします」）。12月29日〜1月3日は運休。百済寺へは八日市駅からタクシーで約10分です。",
                      "The 2026 autumn shuttle bus ended on 29 November. In December, take the bookable shared taxi “Ainori Taxi” from JR Kawase Station to Saimyoji (:51 past each hour, about 15 min, ¥800), then on to Kongorinji (:56 past, about 5 min; fare not confirmed), and from Kongorinji to JR Inae Station (:42 past, ¥800). Book at least 1 hour ahead with Ohmi Taxi Hikone, 0749-22-1111. Not running 29 Dec – 3 Jan. For Hyakusaiji, a taxi from Yokaichi Station takes about 10 minutes.",
                      url="https://saimyouji.com/access/", frm=AFTER_SHUTTLE)

SAIMYOJI_EXTRA = [cc("saimyoji-1.jpg", "Maechan0360", "CC BY-SA 4.0", "File:Saimyo-Ji 01.jpg"),
                  cc("saimyoji-2.jpg", "663highland", "CC BY 2.5", "File:Saimyoji Kora Shiga pref11bs4592.jpg"),
                  cc("saimyoji-3.jpg", "663highland", "CC BY 2.5", "File:Saimyoji Kora Shiga pref15n3900.jpg"),
                  cc("saimyoji-4.jpg", "663highland", "CC BY 2.5", "File:Saimyoji Kora Shiga pref14n3900.jpg")]
KONGORINJI_EXTRA = [cc("kongorinji-1.jpg", "先従隗始", "CC0", "File:Shōhōzan Kongōrin-ji 20221117 61.jpg"),
                    cc("kongorinji-2.jpg", "先従隗始", "CC0", "File:Shōhōzan Kongōrin-ji 20221117 46.jpg"),
                    cc("kongorinji-3.jpg", "先従隗始", "CC0", "File:Shōhōzan Kongōrin-ji 20221117 02.jpg"),
                    cc("kongorinji-4.jpg", "先従隗始", "CC0", "File:Shōhōzan Kongōrin-ji 20221117 60.jpg")]
FLYER_TIP_JA = "湖東三山観光振興協議会の2026年のチラシ、近江鉄道のシャトルバスの案内（時刻表）"
FLYER_TIP_EN = "the 2026 Koto Sanzan leaflet and Ohmi Railway’s shuttle bus page (timetable)"

B = [
    dict(id="hikoneeki", _photos=["omihachimaneki-1.jpg"],
         name=T("京都から彦根駅へ（シャトルバスのりば）", "Kyoto to Hikone Station (shuttle bus stop)"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("10:00の紅葉シャトルバスに乗るため、三条を8時台の前半に出ます。もみじきっぷを買って予約しておくと安心。",
                 "To catch the 10:00 autumn shuttle bus, leave Sanjo early in the 8 o’clock hour. Buying a Momiji Kippu and booking a seat is the safe way."),
         lat=35.27200, lng=136.26250, cash=True,
         text=T("京都から彦根駅へ\n\n"
                "湖東三山（ことうさんざん）の西明寺・金剛輪寺・百済寺は、鈴鹿の山すその離れた場所にあります。2026年の紅葉の時期（11月19日〜29日）は、JR彦根駅の西口から紅葉シャトルバスが出て、3つのお寺を結びます。このコースは10:00発のバス（第2便）に乗る組み立てです。\n\n"
                "平日は三条京阪8:22発の地下鉄「六地蔵」行きで山科へ、8:42発の新快速「長浜」行きで彦根に9:31着。土日祝は三条京阪8:10発、山科8:36発の新快速「米原」行きで彦根に9:20着（どちらも1,250円）。京都駅からなら平日8:37発・土日祝8:30発の新快速で、1,170円。写真は途中で通る近江八幡駅です。\n\n"
                "バスは路線バスの車両で、座れないこともあります。彦根駅発の便は、1日乗り放題の「もみじきっぷ」（大人2,500円・当日に現金で）を買う人だけ予約でき、予約した人が先に乗れます。予約はWebなら乗る日の2日前まで、電話（湖国バス彦根営業所 0749-25-2501、9:00〜18:00）なら前日まで。予約がないと、希望の便に乗れないことがあります。\n\n"
                "このコースのバス代を1回ずつ払うと2,300円。もみじきっぷなら2,500円で、3つのお寺の入山料が50円ずつ安くなり、予約もできます。\n\n"
                "バスの時刻に合わせるのが大変なら、京都駅八条口から湖東三山と永源寺をまわる昼食付きの定期観光バス（京阪バス、12月13日まで。12月6日までは大人14,000円）もあります（湖東三山のチラシより）。\n\n"
                "おすすめ出発時間：三条京阪 8:22（土日祝は8:10）",
                "Kyoto to Hikone Station\n\n"
                "The three Koto Sanzan temples, Saimyoji, Kongorinji and Hyakusaiji, lie far apart along the foot of the Suzuka hills. In the 2026 leaf season (19–29 November) an autumn shuttle bus links them from the west exit of JR Hikone Station. This course is built around the 10:00 bus (no. 2).\n\n"
                "On weekdays, take the 8:22 subway from Sanjo Keihan (bound for Rokujizo) to Yamashina and the 8:42 Special Rapid for Nagahama, reaching Hikone at 9:31. At weekends and holidays, leave Sanjo Keihan at 8:10 and take the 8:36 Special Rapid for Maibara from Yamashina, reaching Hikone at 9:20 (¥1,250 either way). From Kyoto Station, the 8:37 Special Rapid (8:30 at weekends), ¥1,170. The photo is Omi-Hachiman Station, which you pass on the way.\n\n"
                "The shuttle is an ordinary city-type bus and you may have to stand. Seats on buses from Hikone can be booked only with the “Momiji Kippu” day pass (¥2,500, cash on the day), and those who book board first. Book online up to 2 days before, or by phone (Kokoku Bus Hikone, 0749-25-2501, 9:00–18:00) up to the day before. Without a booking you may not get on the bus you want.\n\n"
                "Single fares for this course add up to ¥2,300. The ¥2,500 Momiji Kippu takes ¥50 off each temple’s admission and lets you book.\n\n"
                "If juggling the bus times sounds like too much, there is also a guided coach tour with lunch from Kyoto Station Hachijo exit to the three temples and Eigenji (Keihan Bus, until 13 Dec; ¥14,000 for adults until 6 Dec; from the Koto Sanzan leaflet).\n\n"
                "Recommended departure: Sanjo Keihan 8:22 (8:10 at weekends and holidays)"),
         gmaps=[gm("彦根駅 西口", "Hikone Station (west exit)", 35.27200, 136.26250, "彦根駅 西口")],
         links=[SHUTTLE, SHUTTLE_BOOK, KOTOSANZAN, YAHOO],
         notices=[notice("もみじきっぷは現金だけ", "Momiji Kippu: cash only",
                         "もみじきっぷ（大人2,500円）は、当日に彦根駅西口のバスのりばかバスの中で、現金で払います。予約した人も、乗る日に現金で払います。",
                         "The Momiji Kippu (¥2,500 adults) is paid in cash on the day, at the Hikone Station west-exit bus stop or on the bus, even if you booked.",
                         url="https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/", to=SHUTTLE_END),
                  SHUTTLE_OVER],
         info=info([row("train", "平日：三条京阪 8:22 → 山科 8:42 新快速 → 彦根 9:31。土日祝：三条京阪 8:10 → 山科 8:36 → 彦根 9:20。1,250円",
                        "Weekdays: Sanjo Keihan 8:22 → Yamashina 8:42 Special Rapid → Hikone 9:31. Weekends: Sanjo Keihan 8:10 → Yamashina 8:36 → Hikone 9:20. ¥1,250"),
                    row("train", "京都駅から：平日8:37・土日祝8:30の新快速、1,170円", "From Kyoto Station: Special Rapid at 8:37 (weekends 8:30), ¥1,170"),
                    row("bus", "紅葉シャトルバス（2026年11月19日〜29日）：彦根駅西口4番のりば 9:00・10:00・11:00・12:00発。このコースは10:00発 → 西明寺 10:32（700円）",
                        "Autumn shuttle (19–29 Nov 2026): Hikone Station west exit, stop 4, at 9:00, 10:00, 11:00, 12:00. This course: 10:00 → Saimyoji 10:32 (¥700)", until=SHUTTLE_END),
                    row("fee", "もみじきっぷ 大人2,500円・こども1,250円（当日だけ有効、現金。三山の入山料が50円引き）",
                        "Momiji Kippu ¥2,500 adults, ¥1,250 children (valid on the day, cash; ¥50 off each temple)", until=SHUTTLE_END)],
                   cash=True,
                   tip=T("電車は乗換案内（2026年11月25日・28日のダイヤ）、バスと予約は" + FLYER_TIP_JA + "で、2026年11月22日に確認しました。",
                         "Trains checked on a route planner (25 and 28 Nov 2026); the bus and booking on " + FLYER_TIP_EN + ", 22 Nov 2026."))),
    dict(id="saimyoji", _extra=SAIMYOJI_EXTRA,
         name=T("西明寺（湖東三山）", "Saimyoji Temple (Koto Sanzan)"), kind=T("寺", "Temple"),
         blurb=T("湖東三山のいちばん北。鎌倉時代の本堂と三重塔は、どちらも国宝。秋は紅葉と一緒に、秋から咲く「不断桜」も。お昼は門前で近江牛を。",
                 "The northernmost Koto Sanzan temple, with a Kamakura-period main hall and pagoda that are both National Treasures, and a cherry that blooms in autumn. Lunch on Omi beef by the gate."),
         lat=35.18334, lng=136.28475,
         text=T("西明寺（さいみょうじ）\n\n"
                "湖東三山のいちばん北にある天台宗のお寺です。鎌倉時代の本堂と三重塔は、どちらも国宝。杉木立の中に、ひわだぶきの屋根が2つ並びます。本坊の庭「蓬莱庭（ほうらいてい）」から本堂までは石段を上ります。\n\n"
                "秋は境内の約1,000本のもみじが色づき、11月に満開になる「西明寺不断桜（ふだんざくら）」も咲くので、紅葉と桜が一度に見られます（湖東三山のチラシより）。2026年は、宝冠毘沙門天（ほうかんびしゃもんてん）像の初めての公開（12月13日まで）と、本堂の後ろの仏像群の特別拝観（11月30日まで・1,000円）があります。\n\n"
                "シャトルバスで10:32に着いたら、1時間ほどお参りを。境内は持ち込みの飲食ができません。お昼は門前の「近江牛一筋＠千成亭ぎゅ〜じあむ」で（11:00〜15:00、公式サイト）。公式サイトでは月・火が定休、湖東三山のチラシには「11月は休まず営業」とあるので、月・火に行くなら電話（0749-29-9090）で確かめてください。もみじきっぷを見せると、ここで食事をした人はウーロン茶が1杯無料です。\n\n"
                "次のバスは西明寺12:32発。金剛輪寺（12:47）では降りずに、そのまま百済寺まで乗ります（13:10着・500円）。\n\n"
                "おすすめ訪問時間：10:32〜12:30（お昼を含む）",
                "Saimyoji Temple\n\n"
                "A Tendai temple, the northernmost of the Koto Sanzan. Its Kamakura-period main hall and three-storied pagoda are both National Treasures, their cypress-bark roofs side by side among tall cedars. From the garden of the main residence, Horai-tei, stone steps lead up to the main hall.\n\n"
                "In autumn about 1,000 maples colour the grounds, and the temple’s “fudan-zakura” cherry is in full bloom in November, so you see leaves and blossom together (Koto Sanzan leaflet). In 2026 the crowned Bishamonten statue is on show for the first time (until 13 Dec), and the statues behind the main altar can be seen (until 30 Nov, ¥1,000).\n\n"
                "Arriving on the 10:32 shuttle, give the temple about an hour. You can’t eat or drink your own food in the grounds. For lunch, go to “Omi Beef Hitosuji @ Sennaritei Gyuseum” by the gate (11:00–15:00, official site). The site lists Mondays and Tuesdays as closed, while the Koto Sanzan leaflet says it is open every day in November, so phone ahead on a Monday or Tuesday (0749-29-9090). Show your Momiji Kippu with a meal there for a free oolong tea.\n\n"
                "The next bus leaves Saimyoji at 12:32. Stay on past Kongorinji (12:47) all the way to Hyakusaiji (13:10, ¥500).\n\n"
                "Recommended visit time: 10:32–12:30 (with lunch)"),
         gmaps=[gm("西明寺", "Saimyoji", 35.18334, 136.28475, "西明寺 甲良町池寺")],
         links=[link("official", "西明寺 公式サイト（拝観のご案内）", "Saimyoji (official, Japanese)", "https://saimyouji.com/information/"),
                link("official", "近江牛一筋＠千成亭ぎゅ〜じあむ", "Sennaritei Gyuseum (official, Japanese)", "https://gyuseum.jp/"), SHUTTLE],
         notices=[SHUTTLE_OVER],
         info=info([row("hours", "8:30〜17:00（受付は16:30まで）", "8:30–17:00 (last entry 16:30)"),
                    row("hours", "2026年秋：宝冠毘沙門天像の公開 12月13日まで。本堂後陣の仏像群の特別拝観 11月30日まで（1,000円）",
                        "Autumn 2026: crowned Bishamonten until 13 Dec; statues behind the altar until 30 Nov (¥1,000)", until=SPECIAL_END),
                    row("fee", "入山料 大人800円、中学生500円、小学生300円", "¥800 adults, ¥500 junior high, ¥300 elementary"),
                    row("hours", "お昼：千成亭ぎゅ〜じあむ 11:00〜15:00（月・火定休。11月は無休とチラシにあり、要確認）",
                        "Lunch: Sennaritei Gyuseum 11:00–15:00 (closed Mon–Tue; the leaflet says open daily in November, so check)"),
                    row("bus", "西明寺 12:32 → 百済寺 13:10（500円）。彦根駅へ戻るバスは西明寺 13:43・14:43・15:53・16:53発（700円）",
                        "Saimyoji 12:32 → Hyakusaiji 13:10 (¥500). Back to Hikone from Saimyoji at 13:43, 14:43, 15:53, 16:53 (¥700)", until=SHUTTLE_END)],
                   tip=T("西明寺の公式サイト（拝観のご案内。入山料は「令和5年4月より変更」の料金表の金額）、" + FLYER_TIP_JA + "、千成亭ぎゅ〜じあむの公式サイトで、2026年11月22日に確認しました。",
                         "Checked on the Saimyoji website (fees from its table, “changed April 2023”), " + FLYER_TIP_EN + ", and the Gyuseum website, 22 Nov 2026."))),
    dict(id="hyakusaiji", name=T("百済寺（湖東三山）", "Hyakusaiji Temple (Koto Sanzan)"), kind=T("寺", "Temple"),
         blurb=T("苔むした石垣と杉の参道を上る、近江で最も古いお寺のひとつ。本坊の庭「天下遠望の名園」から、遠く琵琶湖の方まで。",
                 "One of the oldest temples in Omi: climb a cedar-lined approach between mossy stone walls. The garden looks out towards Lake Biwa."),
         lat=35.12683, lng=136.29151,
         text=T("百済寺（ひゃくさいじ）\n\n"
                "湖東三山のいちばん南。聖徳太子が百済の人のために建てたと伝わる、近江で最も古いお寺のひとつです。苔むした石垣にはさまれた参道を上り、大きなわらじが下がる仁王門をくぐって本堂へ。本坊・喜見院（きけんいん）の池泉回遊式の庭は「天下遠望の名園」と呼ばれ、上の遠望台から湖東の平野が見渡せます。\n\n"
                "13:10にシャトルバスで着いたら、帰りのバスの15:20まで2時間あまり。参道は長い上りなので、半分ずつ本堂と庭に時間を使うくらいでちょうどいい広さです。写真は2025年8月の新緑のころのもの。秋は参道ともみじが赤く染まります。\n\n"
                "15:20発のバスで金剛輪寺へ（15:43着・300円）。\n\n"
                "おすすめ訪問時間：13:10〜15:20",
                "Hyakusaiji Temple\n\n"
                "The southernmost of the Koto Sanzan, said to have been founded by Prince Shotoku for people from the kingdom of Baekje and one of the oldest temples in Omi. Climb the approach between mossy stone walls, pass the Nio gate hung with giant straw sandals, and go up to the main hall. The pond garden of the main residence, Kikenin, is known as the garden with a view over the land, and the lookout above it takes in the plain east of the lake.\n\n"
                "Arriving at 13:10, you have just over two hours before the 15:20 bus. The approach is a long climb; splitting the time between the main hall and the garden works well. The photos are from August 2025, in summer green; in autumn the approach turns red.\n\n"
                "Take the 15:20 bus to Kongorinji (15:43, ¥300).\n\n"
                "Recommended visit time: 13:10–15:20"),
         gmaps=[gm("百済寺", "Hyakusaiji", 35.12683, 136.29151, "百済寺 東近江市")],
         links=[link("official", "百済寺 公式サイト", "Hyakusaiji (official, Japanese)", "http://hyakusaiji.jp/"), SHUTTLE],
         notices=[SHUTTLE_OVER],
         info=info([row("hours", "8:30〜17:00（受付は16:30まで）", "8:30–17:00 (last entry 16:30)"),
                    row("hours", "2026年秋のライトアップ：11月30日まで 17時から。平日は受付19:00まで（閉門19:30）、土日祝は受付20:30まで（閉門21:00）",
                        "Autumn 2026 illumination: until 30 Nov from 17:00. Last entry 19:00 on weekdays (closes 19:30), 20:30 at weekends and holidays (closes 21:00)", until=HYAKU_LU_END),
                    row("fee", "大人600円、中学生300円、小学生200円", "¥600 adults, ¥300 junior high, ¥200 elementary"),
                    row("bus", "百済寺 15:20 → 金剛輪寺 15:43（300円）。彦根駅へ直接戻るバスは百済寺 13:10・14:10・15:20・16:20発（1,000円）",
                        "Hyakusaiji 15:20 → Kongorinji 15:43 (¥300). Straight back to Hikone from Hyakusaiji at 13:10, 14:10, 15:20, 16:20 (¥1,000)", until=SHUTTLE_END)],
                   tip=T("時間・料金は百済寺の公式サイト（トップページ）、ライトアップは百済寺の「令和8年 秋季ライトアップのご案内」とチラシ、バスは" + FLYER_TIP_JA + "で、2026年11月22日に確認しました。",
                         "Hours and fees from the Hyakusaiji website, the illumination from its 2026 notice and flyer, buses from " + FLYER_TIP_EN + ", 22 Nov 2026."))),
    dict(id="kongorinji", _extra=KONGORINJI_EXTRA,
         name=T("金剛輪寺（湖東三山）", "Kongorinji Temple (Koto Sanzan)"), kind=T("寺", "Temple"),
         blurb=T("千体のお地蔵さまが並ぶ参道を上ると、国宝の本堂のまわりが「血染めのもみじ」と呼ばれる深い赤に。夕方の光の中で。",
                 "An approach lined with a thousand Jizo statues climbs to a National Treasure main hall ringed by deep-red “blood-dyed” maples, here in the late-afternoon light."),
         lat=35.16128, lng=136.28304, caution=T("受付は16:30まで", "Last entry 16:30"),
         text=T("金剛輪寺（こんごうりんじ）\n\n"
                "湖東三山のまん中にある天台宗のお寺です。総門から本堂までは上りの参道で、両わきに千体のお地蔵さまが並びます。上りきると二天門、その奥に鎌倉時代の本堂（国宝）と三重塔。本堂のまわりと庭のもみじは、色の深さから「血染めのもみじ」と呼ばれています（公式サイトより）。写真は2022年11月17日のものです。\n\n"
                "百済寺からのバスで15:43に着き、受付は16:30まで。総門から本堂までは上りの参道なので、着いたらまっすぐ本堂へ向かいましょう。2026年は秘仏の大黒天の公開（12月13日まで）と、三重塔の大日如来の開扉（11月29日まで・天気のよい日だけ）があります。\n\n"
                "帰りは16:43発のバスで彦根駅へ（17:30着。もみじきっぷで乗れます）。彦根17:52発の新快速に乗ると、山科で地下鉄に乗り換えて三条京阪に19:00（土日祝は18:55）着（1,250円）。三条・木屋町・先斗町のあたりで晩ごはんにして、21〜22時までゆっくりできます。\n\n"
                "おすすめ訪問時間：15:43〜16:43",
                "Kongorinji Temple\n\n"
                "A Tendai temple, the middle one of the Koto Sanzan. From the outer gate an uphill approach is lined on both sides with a thousand Jizo statues. At the top is the Niten-mon gate, and beyond it the Kamakura-period main hall (a National Treasure) and a three-storied pagoda. The maples around the hall and in the garden are called “blood-dyed maples” for their deep colour (temple website). The photos are from 17 November 2022.\n\n"
                "The bus from Hyakusaiji arrives at 15:43, and last entry is 16:30. It is uphill from the outer gate, so head straight up to the main hall. In 2026 the hidden Daikokuten statue is on show (until 13 Dec), and the Dainichi Nyorai in the pagoda is opened on fine days until 29 Nov.\n\n"
                "Leave on the 16:43 bus to Hikone Station (17:30; covered by the Momiji Kippu day ticket). The 17:52 Special Rapid from Hikone, changing to the subway at Yamashina, reaches Sanjo Keihan at 19:00 (18:55 at weekends), ¥1,250. Have dinner around Sanjo, Kiyamachi and Pontocho and take your time until 21:00–22:00.\n\n"
                "Recommended visit time: 15:43–16:43"),
         gmaps=[gm("金剛輪寺", "Kongorinji", 35.16128, 136.28304, "金剛輪寺 愛荘町松尾寺")],
         links=[link("official", "金剛輪寺 公式サイト（参拝・境内）", "Kongorinji (official, Japanese)", "https://kongourinji.jp/precinct"), SHUTTLE,
                link("info", "乗合タクシーの時刻（金剛輪寺 交通）", "Shared taxi times (Kongorinji access page, Japanese)", "https://kongourinji.jp/access")],
         notices=[SHUTTLE_OVER],
         info=info([row("hours", "8:30〜16:30（閉山17:00）", "8:30–16:30 (grounds close 17:00)"),
                    row("hours", "2026年秋：秘仏 大黒天の公開 12月13日まで。三重塔 大日如来の開扉 11月29日まで（天気のよい日だけ）",
                        "Autumn 2026: hidden Daikokuten until 13 Dec; Dainichi Nyorai in the pagoda until 29 Nov (fine days only)", until=SPECIAL_END),
                    row("fee", "大人800円、中学生300円、小学生200円", "¥800 adults, ¥300 junior high, ¥200 elementary"),
                    row("bus", "金剛輪寺 16:43 → 彦根駅 17:30（もみじきっぷで乗れます）。ほかに13:33・14:33・15:43発", "Kongorinji 16:43 → Hikone Station 17:30 (covered by the Momiji Kippu). Also 13:33, 14:33, 15:43", until=SHUTTLE_END),
                    row("train", "彦根 17:52 新快速 → 山科で地下鉄 → 三条京阪 19:00（土日祝18:55）、1,250円", "Hikone 17:52 Special Rapid → subway at Yamashina → Sanjo Keihan 19:00 (weekends 18:55), ¥1,250")],
                   tip=T("時間・料金は金剛輪寺の公式サイト（参拝・境内）、特別公開とバスは" + FLYER_TIP_JA + "、電車は乗換案内で、2026年11月22日に確認しました。境内の食事処「華楽坊」は5名以上の予約制です（公式サイト）。",
                         "Hours and fees from the Kongorinji website, special openings and buses from " + FLYER_TIP_EN + ", trains on a route planner, 22 Nov 2026. The temple restaurant, Karakubo, takes bookings for 5 or more only (website)."))),
    dict(id="kyorinbo", name=T("教林坊（夜のライトアップ）", "Kyorinbo (evening illumination)"), kind=T("寺", "Temple"),
         blurb=T("春と秋だけ公開される、竹林と石の庭の小さなお寺。彦根から電車で安土へ、タクシーで夜の庭へ。最初は外してあります。",
                 "A small temple of bamboo and stone gardens, open only in spring and autumn. Train from Hikone to Azuchi, then a taxi. Not selected at first."),
         lat=35.13898, lng=136.16383, caution=T("駅からタクシー・12月6日まで", "Taxi from the station · until 6 Dec"),
         text=T("教林坊（きょうりんぼう）\n\n"
                "観音正寺のある繖山（きぬがさやま）のふもと、安土町石寺の山あいにある小さなお寺です。ふだんは公開されておらず、春と秋の特別公開のときだけ入れます。竹林の小道を抜けると、苔と巨石の庭。書院の丸窓や三日月の窓から見る庭も絵のようです。写真は2026年11月17日の夜のライトアップです。\n\n"
                "湖東三山のあとに寄るなら、彦根駅17:30着のバスから、18:02発の普通電車（網干行き）で安土へ（18:19着・330円）。北口からタクシーで約10分、18:35ごろ着きます。受付は19:00まで。タクシーは前もって予約し、帰りの迎えも頼んでおきましょう。\n\n"
                "帰りは安土19:28発の電車で山科へ（土日祝は近江八幡で19:37の新快速に乗り換え）、地下鉄で三条京阪に20:32（土日祝は20:30）着（940円）。次は19:50（土日祝は19:55）発で20:53着。朝8時台からの長い1日になり、タクシー代も往復で5,000円前後かかるので、最初は外してあります。\n\n"
                + KYORIN_EXTRA_JA + "\n\nおすすめ訪問時間：18:35〜19:10",
                "Kyorinbo\n\n"
                "A small temple tucked in the hills of Ishidera, Azuchi, at the foot of Mt. Kinugasa. It is usually closed and opens only for special spring and autumn openings. A path through bamboo leads to a garden of moss and huge rocks, framed by the round and crescent-moon windows of the study hall. The photos show the illumination on 17 November 2026.\n\n"
                "To add it after the three temples, take the 18:02 local train (for Aboshi) from Hikone, after the bus gets in at 17:30, to Azuchi (18:19, ¥330). A taxi from the north exit takes about 10 minutes, so you arrive around 18:35; last entry is 19:00. Book the taxi ahead, including the pick-up back.\n\n"
                "Head home on the 19:28 train from Azuchi to Yamashina (at weekends, change at Omi-Hachiman to the 19:37 Special Rapid), then the subway to Sanjo Keihan: 20:32 (20:30 at weekends), ¥940. The next is 19:50 (19:55) → 20:53. It makes a long day from the 8 o’clock hour, and taxis cost around ¥5,000 there and back, so it isn’t selected at first.\n\n"
                + KYORIN_EXTRA_EN + "\n\nRecommended visit time: 18:35–19:10"),
         gmaps=[gm("教林坊", "Kyorinbo", 35.13898, 136.16383, "教林坊 近江八幡市安土町石寺1145"), gm("安土駅", "Azuchi Station", 35.14290, 136.13790, "安土駅")],
         links=KYORIN_LINKS,
         notices=KYORIN_NOTICES,
         info=info(KYORIN_ROWS + [
             row("train", "行き：彦根 18:02 → 安土 18:19（330円）", "There: Hikone 18:02 → Azuchi 18:19 (¥330)"),
             row("train", "帰り：安土 19:28 → 山科で地下鉄 → 三条京阪 20:32（土日祝20:30）、940円。次は19:50（土日祝19:55）→ 20:53",
                 "Back: Azuchi 19:28 → subway at Yamashina → Sanjo Keihan 20:32 (weekends 20:30), ¥940. Next 19:50 (19:55) → 20:53")],
             tip=KYORIN_TIP)),
]

B_PLAN = lambda NO: {
    "_note": "「選んで回る」の設定。彦根駅はいつも入る。defaultPicks は時間割どおりの三山（西明寺→百済寺→金剛輪寺）。教林坊は寄り道（最初は外す）。",
    "defaultMode": "pick",
    "picks": [NO["saimyoji"], NO["hyakusaiji"], NO["kongorinji"], NO["kyorinbo"]],
    "defaultPicks": [NO["saimyoji"], NO["hyakusaiji"], NO["kongorinji"]],
    "auto": {str(NO["hikoneeki"]): {"always": True}},
    "hints": [
        H(NO, "hikoneeki", {"any": [NO["hyakusaiji"], NO["kongorinji"]], "none": [NO["saimyoji"]]},
          "西明寺に寄らない日は、11:00発のバスで百済寺へ直行できます（12:10着・1,000円）。三条京阪を平日9:24、土日祝9:21に出れば間に合います（彦根10:41・10:39着）。お昼は彦根で済ませるか、持っていくと安心です。",
          "Skipping Saimyoji? The 11:00 bus goes straight to Hyakusaiji (12:10, ¥1,000); leave Sanjo Keihan at 9:24 (9:21 at weekends), reaching Hikone at 10:41 (10:39). Eat in Hikone first or bring lunch.", to=SHUTTLE_END),
        H(NO, "hyakusaiji", {"any": [NO["hyakusaiji"]], "none": [NO["kongorinji"], NO["kyorinbo"]]},
          "金剛輪寺に寄らない日は、百済寺のライトアップ（17時から、11月30日まで）まで残れます。百済寺本坊前17:54発のちょこっとバスで八日市駅へ（約35分）、近江鉄道・JR・地下鉄で三条京阪に19:54着（合わせて1,510円）。",
          "Skipping Kongorinji? Stay for Hyakusaiji’s illumination (from 17:00, until 30 Nov). The 17:54 Chokotto Bus from Hyakusaiji Honbo-mae runs to Yokaichi (about 35 min); by Ohmi Railway, JR and subway you reach Sanjo Keihan at 19:54 (¥1,510 in all).", to=HYAKU_LU_END),
        H(NO, "kongorinji", {"any": [NO["kongorinji"]], "none": [NO["hyakusaiji"]]},
          "百済寺に寄らない日は、西明寺11:32発のバスで金剛輪寺へ（11:47着・200円）。帰りのバスは金剛輪寺13:33・14:33・15:43・16:43発です（金剛輪寺から彦根駅までの1回分の運賃は要確認）。",
          "Skipping Hyakusaiji? Take the 11:32 bus from Saimyoji to Kongorinji (11:47, ¥200). Buses back leave Kongorinji at 13:33, 14:33, 15:43 and 16:43 (single fare from Kongorinji to Hikone: please check).", to=SHUTTLE_END),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "andAny": [NO["kongorinji"]]},
          "金剛輪寺16:43発のバスで彦根駅17:30着、18:02の普通電車で安土へ。タクシーは安土駅に18:20ごろ迎えに来てもらうよう予約しておきます。",
          "From Kongorinji take the 16:43 bus to Hikone (17:30) and the 18:02 local to Azuchi. Book a taxi to meet you at Azuchi around 18:20.", to=SHUTTLE_END),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "none": [NO["kongorinji"]]},
          "金剛輪寺に寄らない日は、百済寺15:20発のバスで彦根駅16:30着、17:04発の普通電車で安土へ（17:20着・330円）。タクシーで17:35ごろ、ライトアップが始まったところに着きます。",
          "Skipping Kongorinji? The 15:20 bus from Hyakusaiji reaches Hikone at 16:30; the 17:04 local reaches Azuchi at 17:20 (¥330), and a taxi gets you to Kyorinbo around 17:35, just as the illumination starts.", to=SHUTTLE_END),
    ]}


def H(NO, spot, rule, ja, en, frm=None, to=None):
    h = {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
    if frm:
        h["from"] = frm
    if to:
        h["to"] = to
    return h


SOURCES_COMMON = [
    {"what": "教林坊：秋の公開 11月1日〜12月15日 毎日、9:30〜16:30（ライトアップ期間は8:30から）、大人1,000円・小中学生300円。ライトアップ 令和8年11月14日〜12月6日 17:30〜19:30（19時受付終了）。予約の記載なし（団体バスだけ事前連絡）。三脚・一脚・長時間の撮影目的の入場は不可", "url": "https://kyourinbo.jimdofree.com/", "checked": CHECKED},
    {"what": "教林坊 アクセス：JR安土駅よりタクシー約10分（2,500円前後）・徒歩約60分。普通車100台", "url": "https://kyourinbo.jimdofree.com/ホーム/アクセス-駐車場ご案内/", "checked": CHECKED},
    {"what": "タクシー会社：永源寺タクシー 0748-27-1151、近江タクシー湖東営業所 0748-37-0106、滋賀第一交通 近江八幡営業所 0748-37-4000（料金の目安の記載なし）", "url": "https://www.higashiomi.net/guide/access.html", "checked": CHECKED},
    {"what": "安土→三条京阪（JR・山科で地下鉄）：2026年11月25日（水）18:50→19:54、18:58→19:54、19:20→20:22、19:28→20:32（940円）、19:50→20:53、20:20→21:25、20:55→21:58、21:07、21:36→22:36、22:03→23:03、22:33→23:49。11月28日（土）：19:28→近江八幡19:37新快速→20:30、19:55→20:53、20:19→21:15、22:33→23:49", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
]
SOURCES_A = [
    {"what": "三条京阪→太郎坊宮前：11月25日（水）9:44 六地蔵行→山科10:06 新快速 近江塩津行→近江八幡10:35、近江鉄道10:42→太郎坊宮前10:57（260＋590＋390＝1,240円）。11月28日（土）9:43→10:05→10:34→10:42→10:57。びわ湖浜大津行は京阪山科着で1,370円。京都駅10:00の新快速で近江八幡10:35（土10:34）・680円", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "近江鉄道 太郎坊宮前→八日市：平日・土曜とも 11:41（土のみ）・11:59・12:41・12:59・13:41…（160円）。12:41・12:59のどちらも八日市駅13:15のバスに接続", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "近江鉄道バス 永源寺線（2024年4月1日改正の時刻表PDF）：八日市駅→永源寺 平日 …11:15・12:15・13:15・13:40・14:40… 土日祝 …11:15・12:15・13:15・14:15… 永源寺→八日市駅 平日 …15:26・15:56・16:24・16:54・17:22・17:54・18:24・18:54・19:27・19:52・20:27、土日祝 …15:26・15:56・16:25・16:55・17:25・18:16・19:16。八日市駅1番のりば、運賃670円。乗換案内の11月25日・28日の結果と一致", "url": "https://www.ohmitetudo.co.jp/bus/access/eigenji/", "checked": CHECKED},
    {"what": "永源寺前→安土：11月25日（水）16:24→八日市駅16:59、近江鉄道17:09→近江八幡17:28、JR17:41→安土17:44（670＋460＋190＝1,320円）。11月28日（土）16:25→17:00→17:09→17:28→17:41→17:44", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "永源寺前→三条京阪（ライトアップのあと）：平日18:24→20:32、土日祝18:16→20:30（1,980円）", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "太郎坊宮：参拝24時間、社務受付9:00〜17:00（ご祈祷等16:00まで）、拝観料・駐車料不要、約740段（ふもとから本殿まで742段、第一駐車場から約260段）。アクセス：太郎坊宮前駅から徒歩約20分", "url": "https://tarobo.or.jp/", "checked": CHECKED},
    {"what": "永源寺 よくある質問：参拝時間 9:00〜16:00（11月は観楓期のため変更）、参拝志納料 大人600円・中学生200円・小学生以下無料。紅葉は11月上旬〜下旬、中旬がピーク", "url": "https://eigenji-t.jp/contact/", "checked": CHECKED},
    {"what": "永源寺 お知らせ：ライトアップ11月14日〜28日（11/13）。山門・法堂の特別拝観 10:00・11:30・14:00、1,500円（入山志納料込）（11/18）。ライトアップは20時まで（11/20金・11/21土）。食事処「音無瀬」とキッチンカー「ブランブル」開店、うどん・そば・ぜんざい・甘酒・パフェ・クレープ（11/15、時間の記載なし）", "url": "https://eigenji-t.jp/haikan/", "checked": CHECKED},
    {"what": "近江鉄道線でICOCAなどが使える（2026年3月1日から、全線）", "url": "https://www.ohmitetudo.co.jp/railway/icoca-2025/", "checked": CHECKED},
    {"what": "ティファニー（近江八幡）：ディナー17:00〜20:00（L.O.）、火曜休み、駅の北口から歩いて3分（近江八幡マップのデータ、2026-11-20確認）", "url": "../omihachiman/", "checked": "2026-11-20"},
    {"what": "近江八幡→三条京阪：11月25日（水）21:13 新快速→山科21:50→21:58（850円）。永源寺前16:24→近江八幡17:36 新快速→三条京阪18:29（11月30日（月））、土日祝16:25→18:33（12月5日（土））", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
]
SOURCES_B = [
    {"what": "湖東三山 紅葉シャトルバス 2026：11月19日〜29日。彦根駅西口4番のりば。往路 彦根9:00→西明寺9:32（1便は西明寺まで）、10:00→西明寺10:32→金剛輪寺10:47（2便は金剛輪寺まで）、11:00→11:32→11:47→クレフィール湖東11:55→読合堂11:59→百済寺12:10、12:00→12:32→12:47→12:55→12:59→13:10。復路 百済寺13:10・14:10・15:20・16:20→金剛輪寺13:33・14:33・15:43・16:43→西明寺13:43・14:43・15:53・16:53→彦根駅14:20・15:20・16:30・17:30。運賃 彦根-西明寺700・西明寺-金剛輪寺200・金剛輪寺-百済寺300・西明寺-百済寺500・金剛輪寺-彦根800・百済寺-彦根1,000円。もみじきっぷ 大人2,500円（当日、彦根駅西口かバス車内、現金）。予約は彦根駅発だけ・もみじきっぷ購入者だけ、電話（湖国バス彦根営業所0749-25-2501、9:00〜18:00）は前日まで、Webは2日前まで。予約者優先、座れないことあり", "url": "https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/", "checked": CHECKED},
    {"what": "湖東三山の2026年のチラシ（近江鉄道のページのPDF）：西明寺 入山料800円・8:30〜16:30（閉門17:00）、宝冠毘沙門天 初公開 10月1日〜12月13日、本堂後陣仏像群特別拝観 11/14〜30。金剛輪寺 800円・8:30〜16:30（閉門17:00）、秘仏大黒天 10月31日〜12月13日、三重塔大日如来開扉 11/14〜29（好天時のみ）。百済寺 600円。千成亭ぎゅ〜じあむ 10:00〜16:00・月火定休（11月は無休）。京阪バス定期観光（京都駅八条口発、湖東三山・永源寺・昼食、11/14〜12/6 大人14,000円、12/7〜12/13 9,900円）", "url": "https://www.ohmitetudo.co.jp/file/bus-icoico-event-kotosanzanshuttlebus2026-chirashi.pdf.pdf", "checked": CHECKED},
    {"what": "三条京阪→彦根：11月25日（水）8:22 六地蔵行→山科8:42 新快速 長浜行→彦根9:31（1,250円）。11月28日（土）8:10→山科8:36 新快速 米原行→9:20、8:43→9:06→9:49。京都駅 平日8:37→9:31、土8:30→9:20（1,170円）。平日9:24→10:41", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "彦根→三条京阪：11月25日（水）17:52 新快速→山科18:51→三条京阪19:00（1,250円）。11月28日（土）17:52→18:55。彦根→安土 16:34→16:50、17:04→17:20、17:32→17:49、18:02→18:19（330円）、18:33→18:50", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "百済寺本坊前→三条京阪：17:54 ちょこっとバス→八日市駅18:29、近江鉄道18:39→近江八幡19:06 新快速→山科、三条京阪19:54（1,510円、11月25日・28日）。百済寺本町（湖国バス角能線）17:16→能登川17:59、平日は18:16・19:16もあり", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "西明寺 拝観のご案内：8:30〜17:00（最終受付は閉門30分前）、料金表 大人800円・中人500円・小人300円（令和5年4月より変更）、本堂後陣仏像群特別拝観料1,000円、境内での持ち込み飲食禁止", "url": "https://saimyouji.com/information/", "checked": CHECKED},
    {"what": "愛のりタクシー（甲良線）：JR河瀬駅東口 7:51〜15:51 毎時51分→西明寺 約15分・800円。西明寺→河瀬駅 7:12〜16:12 毎時12分。西明寺前→金剛輪寺 9:56〜15:56 毎時56分（約5分）。予約 近江タクシー彦根営業所0749-22-1111、1時間前まで。12/29〜1/3運休", "url": "https://saimyouji.com/access/", "checked": CHECKED},
    {"what": "金剛輪寺：8:30〜16:30（17:00閉山）、大人800円・中学生300円・小学生200円。華楽坊は5名以上の予約から。愛のりタクシー 稲枝駅→金剛輪寺800円、金剛輪寺発10:42〜16:42 毎時42分", "url": "https://kongourinji.jp/access", "checked": CHECKED},
    {"what": "百済寺：8:30〜17:00（受付16:30まで）、大人600円・中学生300円・小学生200円。令和8年秋季ライトアップ 11月14日〜30日、平日17時〜最終受付19時・閉門19時30分、土日祝17時〜最終受付20時30分・閉門21時", "url": "http://hyakusaiji.jp/", "checked": CHECKED},
    {"what": "近江牛一筋＠千成亭ぎゅ〜じあむ：甲良町池寺1-5（西明寺門前）、営業時間11:00〜15:00、定休日 月曜・火曜", "url": "https://gyuseum.jp/", "checked": CHECKED},
]


def build(defs, plan_fn, course, out, sections, note, sources, focus=None):
    spots = []
    for i, s in enumerate(defs, 1):
        s = dict(s)
        own = s.pop("_photos", None)
        extra = s.pop("_extra", None)
        cash = s.pop("cash", False)
        o = {"no": i, "id": s.pop("id")}
        o.update(s)
        o["photos"] = own if own else photos(o["id"], extra)
        o.setdefault("notices", [])
        if cash:
            o["info"]["cash"] = True
        spots.append(o)
    NO = {s["id"]: s["no"] for s in spots}
    data = {"id": "higashiomi", "course": course, "_note": note,
            "sections": sections(NO), "photoBase": "../images/higashiomi/",
            "plan": plan_fn(NO), "sources": SOURCES_COMMON + sources, "spots": spots}
    if focus:
        data["focus"] = focus(NO)
    json.dump(data, open(f"{R}/data/routes/{out}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


build(A, A_PLAN, "eigenji", "higashiomi.json",
      lambda NO: [{"first": 1, "last": NO["taroubou"], "area": T("近江八幡・太郎坊宮", "Omi-Hachiman & Taroubou-gu"), "title": T("742段の石段の上へ", "Up 742 stone steps")},
                  {"first": NO["eigenji"], "last": NO["eigenji"], "area": T("永源寺", "Eigenji"), "title": T("渓谷のもみじと遅めのお昼", "Valley maples and a late lunch")},
                  {"first": NO["kyorinbo"], "last": NO["kyorinbo"], "area": T("安土・教林坊", "Azuchi & Kyorinbo"), "title": T("竹林と庭のライトアップ", "Bamboo and garden by lantern light")}],
      "京都から日帰り 湖東の紅葉、コース「太郎坊宮・永源寺」（9〜10時に出発）。三条京阪9:44→近江八幡→近江鉄道で太郎坊宮前10:57→太郎坊宮→八日市13:15のバスで永源寺（お昼）→16:24のバス→近江鉄道・JRで安土17:44→タクシーで教林坊のライトアップ→安土19:28→三条京阪20:32。"
      "写真は Toshi の写真ライブラリ（太郎坊宮は2024年12月1日、永源寺と教林坊は2026年11月17日、近江八幡駅は omihachiman の流用）。このファイルは scripts/build_higashiomi_data.py で作る。",
      SOURCES_A)
build(B, B_PLAN, "sanzan", "higashiomi-sanzan.json",
      lambda NO: [{"first": 1, "last": NO["saimyoji"], "area": T("彦根・西明寺", "Hikone & Saimyoji"), "title": T("10:00のシャトルバスで国宝の本堂へ", "The 10:00 shuttle to a National Treasure hall")},
                  {"first": NO["hyakusaiji"], "last": NO["kongorinji"], "area": T("百済寺・金剛輪寺", "Hyakusaiji & Kongorinji"), "title": T("苔の参道と血染めのもみじ", "Mossy approach and blood-red maples")},
                  {"first": NO["kyorinbo"], "last": NO["kyorinbo"], "area": T("寄り道：教林坊", "Option: Kyorinbo"), "title": T("帰りに夜のライトアップ", "An evening illumination on the way home")}],
      "京都から日帰り 湖東の紅葉、コース「湖東三山」（8時台に出発。紅葉シャトルバスの運行日 2026年11月19日〜29日向け）。三条京阪8:22（土日祝8:10）→彦根9:31（9:20）→シャトルバス10:00→西明寺10:32（門前の千成亭ぎゅ〜じあむでお昼）→12:32のバスで百済寺13:10→15:20のバスで金剛輪寺15:43→16:43のバスで彦根17:30→17:52の新快速で三条京阪19:00。教林坊は寄り道（最初は外す）。"
      "西明寺と金剛輪寺の写真は Wikimedia Commons（photos の要素が {file, credit}）、百済寺は2025年8月12日の Toshi の写真。1番の写真は近江八幡駅（途中で通る駅）。このファイルは scripts/build_higashiomi_data.py で作る。",
      SOURCES_B)
