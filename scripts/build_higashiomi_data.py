#!/usr/bin/env python3
"""京都から日帰り 湖東の紅葉のデータを書き出す（2コース）。

使い方: python3 scripts/build_higashiomi_data.py   → そのあと python3 scripts/sync_higashiomi.py
- data/routes/higashiomi.json        ＝ コース「太郎坊宮・永源寺」（eigenji。最初に開く）
    京都駅10:00発 → 近江八幡で近江鉄道 → 太郎坊宮 → 八日市からバスで永源寺（遅めのお昼）→ 近江八幡・安土 → タクシーで教林坊のライトアップ → 京都駅20:12
    12月6日まで読まれる。12/7からは次のものに自動で替わる（日付は scripts/sync_higashiomi.py の WINTER_FROM）
- data/routes/higashiomi-eigenji-winter.json ＝ 太郎坊宮・永源寺の 12/7から（教林坊なし。番号1〜4は同じ）
    京都駅10:00発 → 太郎坊宮 → 永源寺（お昼は持っていく・拝観16:00まで）→ 永源寺前16:24発（土日祝16:25）→ 京都駅18:12 → 夜は街なか
- data/routes/higashiomi-sanzan.json ＝ コース「湖東三山」（sanzan）
    京都駅8:37発（土日祝8:30）→ 彦根駅10:00の紅葉シャトルバス → 西明寺（門前でお昼）→ 百済寺 → 金剛輪寺 → 彦根17:30 → 京都駅18:42
    11月29日まで読まれる。11/30からは次の2つに自動で替わる（どの日にどれを読むかは scripts/sync_higashiomi.py の TAXI_FROM・WINTER_FROM）
- data/routes/higashiomi-sanzan-taxi.json   ＝ 湖東三山の 11/30〜12/6（乗合タクシーの時間割）
    京都駅9:34発（土日祝9:37）→ 河瀬10:51のタクシー → 西明寺（お昼）→ 12:56のタクシー → 金剛輪寺 → 14:42のタクシー → 稲枝16:13 → 京都駅17:06
    最初に選ばれるのは西明寺と金剛輪寺。百済寺（別の日に行く）と教林坊の夜は外してある
- data/routes/higashiomi-sanzan-winter.json ＝ 湖東三山の 12/7から。taxi から教林坊を抜いたもの（ライトアップが終わり、昼の公開にも間に合わない）
    教林坊は「選んで回る」で足せる（最初は外してある）
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/higashiomi/<スポットのid>-<番号>.jpg を番号の順に全部使う（湖東三山コースの1番だけ omihachimaneki-1.jpg を1枚）
- 起点は京都駅（2026-11-22 オーナーの指示で三条から変えた。三条のあたりからは地下鉄で京都駅へ、の補足）
- 2026-11-22 作り直し。時刻・料金・休みは公式サイトと乗換案内で確かめ、開いたページは data の sources に書いた
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/higashiomi"
CHECKED = "2026-11-22"
RECHECKED = "2026-11-23"   # 要確認の調べ直し（永源寺の11月・千成亭ぎゅ〜じあむの定休日・愛のりタクシーの運賃）
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


def info(rows, tip=None, cash=False, verified=True, checked=None):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked or CHECKED}
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
EIGENJI_AUTUMN = "https://www.higashiomi.net/media/event/a793"   # 東近江市観光協会：永源寺の秋（11月の参拝受付・ライトアップ・特別拝観・お茶席。チラシの画像つき）
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
         blurb=T("京都駅10:00発の新快速で近江八幡へ35分。同じ駅で近江鉄道に乗り換えて、太郎坊宮前に10:57。三条のあたりからは、地下鉄で京都駅へ（約15分）。",
                 "The 10:00 Special Rapid from Kyoto Station takes 35 minutes to Omi-Hachiman. Change there to the Ohmi Railway for Taroubougu-mae (10:57). From around Sanjo, take the subway to Kyoto Station first (about 15 minutes)."),
         lat=35.12280, lng=136.10280,
         text=T("京都から近江八幡へ\n\n"
                "京都駅10:00発の新快速「近江塩津（おうみしおつ）」行きに乗れば、乗り換えなしで近江八幡に10:35（土日祝は10:34）着。680円です。\n\n"
                "近江八幡で近江鉄道の八日市線（ようかいちせん）に乗り換え（7分）。10:42発の電車で、太郎坊宮前（たろうぼうぐうまえ）に10:57に着きます。390円で、京都駅から合わせて1,070円。近江鉄道は2026年3月からICOCAなどの交通系ICカードで乗れます。\n\n"
                "三条のあたりからは、地下鉄で京都駅へ（烏丸御池（からすまおいけ）で乗り換え、約15分・260円）。平日は三条京阪9:30発、土日祝は9:32発なら間に合います。\n\n"
                "三条からは、地下鉄「六地蔵（ろくじぞう）」行きで山科（やましな）へ出て、同じ新快速に乗ることもできます（三条京阪9:44発、土日祝9:43発。近江八幡まで850円）。「びわ湖浜大津」行きは京阪山科駅に着き、運賃も130円高くなります。\n\n"
                "このあと太郎坊宮から永源寺へのバスに乗るまで、食べる店はほとんどありません。お昼は永源寺で14時ごろになるので、朝ごはんはしっかり、おやつを持っていくと安心です。\n\n"
                "おすすめ出発時間：京都駅 10:00",
                "Kyoto to Omi-Hachiman\n\n"
                "Take the 10:00 Special Rapid for Omi-Shiotsu from Kyoto Station. It runs direct to Omi-Hachiman, arriving at 10:35 (10:34 at weekends and holidays), for ¥680.\n\n"
                "At Omi-Hachiman, change to the Ohmi Railway Yokaichi Line (7 minutes). The 10:42 train reaches Taroubougu-mae at 10:57 for ¥390, so ¥1,070 from Kyoto Station. Since March 2026 you can ride the Ohmi Railway with ICOCA and other transport IC cards.\n\n"
                "From around Sanjo, take the subway to Kyoto Station (change at Karasuma Oike; about 15 minutes, ¥260). The 9:30 from Sanjo Keihan on weekdays, or the 9:32 at weekends and holidays, gets you there in time.\n\n"
                "From Sanjo you can also ride a Rokujizo-bound subway to Yamashina and board the same Special Rapid (Sanjo Keihan 9:44, or 9:43 at weekends and holidays; ¥850 to Omi-Hachiman). Subways for Biwako-Hamaotsu stop at Keihan Yamashina instead and cost ¥130 more.\n\n"
                "There’s almost nowhere to eat until Eigenji, and lunch there will be around 14:00. Have a good breakfast and bring a snack.\n\n"
                "Recommended departure: Kyoto Station 10:00"),
         gmaps=[gm("近江八幡駅", "Omi-Hachiman Station", 35.12280, 136.10280, "近江八幡駅")],
         links=[YAHOO, link("info", "近江鉄道線のICOCA", "ICOCA on the Ohmi Railway (Japanese)", "https://www.ohmitetudo.co.jp/railway/icoca-2025/")],
         info=info([row("train", "京都駅 10:00 新快速 → 近江八幡 10:35（土日祝10:34）→ 近江鉄道 10:42 → 太郎坊宮前 10:57。1,070円（JR680円＋近江鉄道390円）",
                        "Kyoto Station 10:00 Special Rapid → Omi-Hachiman 10:35 (weekends 10:34) → Ohmi Railway 10:42 → Taroubougu-mae 10:57. ¥1,070 (JR ¥680 + Ohmi Railway ¥390)"),
                    row("train", "三条京阪 → 京都駅：地下鉄（烏丸御池で乗り換え）約15分・260円", "Sanjo Keihan → Kyoto Station: subway (change at Karasuma Oike), about 15 min, ¥260")],
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
                "八日市駅の1番のりばから13:15発の近江鉄道バス（永源寺車庫行き）に乗り、「永源寺前」に13:44（土日祝は13:43）着（670円）。着いたらまずお昼を。永源寺のお知らせでは、11月14日から食事処とキッチンカーが開いていて、うどん・そば・ぜんざいなどがあります（営業時間は要確認）。門前の茶店では名物の永源寺こんにゃくも。座って休むなら、含空院の庭を見る標月亭のお茶席も（11月30日まで、9:00〜17:00・一席700円。参拝志納料は別）。\n\n"
                "拝観は、11月は8:00〜17:00。ライトアップの11月14日〜28日は夜まで開いています。12月は9:00〜16:00です。\n\n"
                "帰りは永源寺前16:24発（土日祝は16:25発）のバスで八日市へ。教林坊に行かない日は、夕方のライトアップ（2026年は11月28日まで、17時から。金〜日と祝日は20:00、月〜木は18:30に閉門）を見てから帰ることもできます。\n\n"
                "おすすめ訪問時間：13:45〜16:00",
                "Eigenji Temple\n\n"
                "Head temple of the Eigenji school of Rinzai Zen, on the Echigawa river in the Suzuka hills. Cross the Tando bridge and climb to the great gate; beyond, the lecture hall and abbot’s quarters are wrapped in maples. The leaves turn from early to late November, peaking in mid-November (temple FAQ).\n\n"
                "Take the 13:15 Ohmi bus (for Eigenji Shako) from stop 1 at Yokaichi Station and get off at “Eigenji-mae” at 13:44 (13:43 at weekends and holidays; ¥670). Have lunch first. The temple’s news page says an eatery and a food truck have been open since 14 November, with udon, soba, zenzai and the like (hours not confirmed). Tea houses by the gate sell the local Eigenji konnyaku. For a sit-down rest, the Hyogetsu-tei tea room looks onto the Gankuin garden (until 30 Nov, 9:00–17:00, ¥700 a seat, admission extra).\n\n"
                "The temple is open 8:00–17:00 in November, and into the evening during the illumination (14–28 Nov). In December it is open 9:00–16:00.\n\n"
                "Leave on the 16:24 bus from Eigenji-mae (16:25 at weekends and holidays). If you’re skipping Kyorinbo, you can stay for the evening illumination instead (until 28 Nov in 2026, from 17:00; the gate closes at 20:00 Friday to Sunday and on holidays, 18:30 Monday to Thursday).\n\n"
                "Recommended visit time: 13:45–16:00"),
         gmaps=[gm("永源寺", "Eigenji", 35.08058, 136.31999, "永源寺 東近江市")],
         links=[link("official", "永源寺 公式サイト（お知らせ）", "Eigenji (official news, Japanese)", "https://eigenji-t.jp/haikan/"),
                link("info", "東近江市観光協会（永源寺の秋の拝観・特別拝観）", "Higashiomi tourism: Eigenji in autumn (Japanese)", EIGENJI_AUTUMN), EIGENJI_BUS],
         notices=[notice("12月の拝観は16:00まで", "Closes at 16:00 in December",
                         "12月の拝観は9:00〜16:00です。紅葉の時期の食事処とキッチンカーが12月も開いているかは確かめられませんでした（要確認）。お昼は持っていくと安心です。",
                         "In December Eigenji is open 9:00–16:00. We couldn’t confirm that the leaf-season eatery and food truck open in December (please check), so bringing lunch is safer.",
                         url="https://eigenji-t.jp/contact/", frm="2026-12-01")],
         info=info([row("hours", "11月：8:00〜17:00（閉門）。11月14日〜28日はライトアップで夜まで", "November: 8:00–17:00 (gate closes); open into the evening 14–28 Nov for the illumination", until="2026-11-30"),
                    row("hours", "2026年秋のライトアップ：11月14日〜28日 17:00から。金〜日・祝は20:00、月〜木は18:30に閉門",
                        "Autumn 2026 illumination: 14–28 Nov from 17:00. Gate closes 20:00 Fri–Sun and holidays, 18:30 Mon–Thu", until=EIGENJI_LU_END),
                    row("hours", "12月から：9:00〜16:00", "From December: 9:00–16:00", frm="2026-12-01"),
                    row("hours", "山門・法堂の特別拝観（ボランティアガイドの案内）：11月23日まで 10:00・11:30・14:00、1,500円（参拝志納料込み）。集合は永源寺観光案内所、予約は 0748-27-2020",
                        "Guided tour of the great gate and lecture hall: until 23 Nov, 10:00, 11:30, 14:00, ¥1,500 incl. admission. Meet at the Eigenji tourist information office; booking 0748-27-2020", until="2026-11-23"),
                    row("hours", "含空院庭園と標月亭のお茶席：11月30日まで 9:00〜17:00（入場16:45まで）、一席700円（参拝志納料は別）",
                        "Gankuin garden and Hyogetsu-tei tea room: until 30 Nov, 9:00–17:00 (last entry 16:45), ¥700 a seat (admission extra)", until="2026-11-30"),
                    row("hours", "お昼：食事処とキッチンカー（11月14日から。営業時間は要確認）", "Lunch: eatery and food truck (open since 14 Nov; hours not confirmed)", until="2026-11-30"),
                    row("fee", "参拝志納料 大人600円、中学生200円、小学生以下無料", "Admission ¥600 adults, ¥200 junior high, free for younger children"),
                    row("bus", "八日市駅1番のりば 13:15 → 永源寺前 13:44（土日祝13:43）、670円。帰りは永源寺前 16:24（土日祝16:25）→ 八日市駅 16:59（17:00）",
                        "Yokaichi stop 1 13:15 → Eigenji-mae 13:44 (weekends 13:43), ¥670. Back: Eigenji-mae 16:24 (weekends 16:25) → Yokaichi 16:59 (17:00)")],
                   tip=T("参拝志納料とふだんの時間は永源寺の公式サイト（よくある質問）、11月の時間・ライトアップ・特別拝観・お茶席は東近江市観光協会の案内とチラシ、永源寺のお知らせ（2026年11月15日・21日・23日）で、2026年11月23日に確認しました。食事処の営業時間はどこにも書かれていません。バスは近江鉄道バスの時刻表と乗換案内（11月22日）。",
                         "Admission and usual hours from the temple FAQ; November hours, illumination, tour and tea room from the Higashiomi tourism association’s page and leaflet and the temple news (15, 21, 23 Nov 2026), checked 23 Nov 2026. The eatery’s hours aren’t published. Buses from Ohmi bus’s timetable and a route planner (22 Nov)."),
                   verified=False, checked=RECHECKED)),
    dict(id="kyorinbo", name=T("教林坊（夜のライトアップ）", "Kyorinbo (evening illumination)"), kind=T("寺", "Temple"),
         blurb=T("春と秋だけ公開される、竹林と石の庭の小さなお寺。夜は、もみじと竹林がやわらかく照らされます。安土駅からタクシーで。",
                 "A small temple of bamboo and stone gardens, open only in spring and autumn. At night the maples and bamboo are softly lit. Taxi from Azuchi Station."),
         lat=35.13898, lng=136.16383, caution=T("駅からタクシー・12月6日まで", "Taxi from the station · until 6 Dec"),
         text=T("教林坊（きょうりんぼう）\n\n"
                "観音正寺のある繖山（きぬがさやま）のふもと、安土町石寺の山あいにある小さなお寺です。ふだんは公開されておらず、春と秋の特別公開のときだけ入れます。竹林の小道を抜けると、苔と巨石の庭。書院の丸窓や三日月の窓から見る庭も絵のようです。写真は2026年11月17日の夜のライトアップです。\n\n"
                "永源寺前16:24（土日祝16:25）のバスで八日市駅16:59、17:09の近江鉄道で近江八幡17:28、17:41のJR（米原行き）でひと駅、安土（あづち）に17:44着（バス670円・近江鉄道460円・JR190円）。北口からタクシーで約10分、18時ごろに着きます。タクシーは前もって予約し、帰りの迎えも頼んでおきましょう。\n\n"
                "帰りは安土19:28発の電車に乗り、次の近江八幡で19:37発の新快速に乗り換えて、京都駅に20:12着（770円）。次は安土19:50発で京都駅20:36着（土日祝は19:55発で20:41着）。最終は23:23発で0:12着です。\n\n"
                "晩ごはんは京都に戻ってから、21〜22時まで。三条・木屋町・先斗町（ぽんとちょう）のあたりは遅くまで開いている店が多く、京都駅から地下鉄で約15分です。\n\n"
                "近江八幡で晩ごはんにするなら、19:28の電車をひと駅の近江八幡（19:32着）で降りて、北口から歩いて3分のティファニーへ（ディナーのラストオーダー20:00、火曜休み。近江八幡のマップの13番）。食後は21:13発の新快速で、京都駅に21:48着（680円）。\n\n"
                + KYORIN_EXTRA_JA + "\n\nおすすめ訪問時間：18:00〜19:00",
                "Kyorinbo\n\n"
                "A small temple tucked in the hills of Ishidera, Azuchi, at the foot of Mt. Kinugasa. It is usually closed and opens only for special spring and autumn openings. A path through bamboo leads to a garden of moss and huge rocks, framed by the round and crescent-moon windows of the study hall. The photos show the illumination on 17 November 2026.\n\n"
                "Take the 16:24 bus from Eigenji-mae (16:25 at weekends) to Yokaichi (16:59), the 17:09 Ohmi Railway to Omi-Hachiman (17:28), and the 17:41 JR train for Maibara one stop to Azuchi (17:44). Bus ¥670, Ohmi Railway ¥460, JR ¥190. A taxi from the north exit takes about 10 minutes, so you arrive around 18:00. Book the taxi ahead, including the pick-up back.\n\n"
                "Head home on the 19:28 train from Azuchi and change one stop later at Omi-Hachiman to the 19:37 Special Rapid: Kyoto Station at 20:12, ¥770. The next leaves Azuchi at 19:50, reaching Kyoto Station at 20:36 (19:55 → 20:41 at weekends and holidays). The last is 23:23, arriving 0:12.\n\n"
                "Dinner back in Kyoto can run to 21:00–22:00. Many places around Sanjo, Kiyamachi and Pontocho stay open late; they are about 15 minutes from Kyoto Station by subway.\n\n"
                "For dinner in Omihachiman instead, get off the 19:28 train one stop later at Omi-Hachiman (19:32) and walk 3 minutes from the north exit to Tiffany (dinner last order 20:00, closed Tuesdays; no. 13 on our Omihachiman map). Afterwards the 21:13 Special Rapid gets you to Kyoto Station at 21:48 (¥680).\n\n"
                + KYORIN_EXTRA_EN + "\n\nRecommended visit time: 18:00–19:00"),
         gmaps=[gm("教林坊", "Kyorinbo", 35.13898, 136.16383, "教林坊 近江八幡市安土町石寺1145"), gm("安土駅", "Azuchi Station", 35.14290, 136.13790, "安土駅")],
         links=KYORIN_LINKS + [OMI_MAP],
         notices=KYORIN_NOTICES,
         info=info(KYORIN_ROWS + [
             row("train", "行き：永源寺前 16:24（土日祝16:25）バス → 八日市 17:09 近江鉄道 → 近江八幡 17:41 JR → 安土 17:44（合わせて1,320円）",
                 "There: Eigenji-mae 16:24 (weekends 16:25) bus → Yokaichi 17:09 Ohmi Railway → Omi-Hachiman 17:41 JR → Azuchi 17:44 (¥1,320 in all)"),
             row("train", "帰り：安土 19:28 → 近江八幡 19:37 新快速 → 京都駅 20:12、770円。次は19:50 → 20:36（土日祝19:55 → 20:41）。最終は23:23 → 0:12",
                 "Back: Azuchi 19:28 → Omi-Hachiman 19:37 Special Rapid → Kyoto Station 20:12, ¥770. Next 19:50 → 20:36 (weekends 19:55 → 20:41). Last train 23:23 → 0:12")],
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
          "太郎坊宮に寄らない日は、京都駅10:00発の新快速で近江八幡へ。10:42発の近江鉄道を八日市（ようかいち）まで乗り、駅の1番のりば11:15発のバスで永源寺前に11:44（土日祝11:43）着。京都駅から1,810円です。永源寺でお昼にして、ゆっくり回れます。",
          "Skipping Taroubou-gu? Take the 10:00 Special Rapid from Kyoto Station to Omi-Hachiman, the 10:42 Ohmi Railway to Yokaichi and the 11:15 bus from stop 1, reaching Eigenji-mae at 11:44 (11:43 at weekends), ¥1,810 from Kyoto Station. Lunch at Eigenji and take your time."),
        H(NO, "taroubou", {"any": [NO["taroubou"]], "none": [NO["eigenji"]]},
          "永源寺に行かない日は、太郎坊宮のあと近江鉄道で近江八幡へ戻り、八幡堀のあたりを歩いてお昼に（近江八幡のマップを見てください）。教林坊へは、夕方に近江八幡からJRでひと駅の安土へ。",
          "Not going to Eigenji? After the shrine, take the Ohmi Railway back to Omi-Hachiman, walk the canal district and have lunch there (see our Omihachiman map). For Kyorinbo, take JR one stop to Azuchi in the late afternoon."),
        H(NO, "eigenji", {"any": [NO["eigenji"]], "none": [NO["kyorinbo"]]},
          "教林坊に行かない日は、永源寺のライトアップ（17時から）を見てから帰れます。永源寺前18:24発（土日祝は18:16発）のバスに乗ると、近江鉄道と近江八幡19:37発の新快速を乗り継いで、京都駅に20:12着（1,810円）。",
          "Skipping Kyorinbo? Stay for Eigenji’s illumination (from 17:00). The 18:24 bus from Eigenji-mae (18:16 at weekends) connects with the Ohmi Railway and the 19:37 Special Rapid from Omi-Hachiman, reaching Kyoto Station at 20:12 (¥1,810).", to=EIGENJI_LU_END),
        H(NO, "eigenji", {"any": [NO["eigenji"]], "none": [NO["kyorinbo"]]},
          "教林坊に行かない日は、永源寺前16:24発（土日祝16:25発）のバスで八日市へ。近江鉄道で近江八幡に17:28、17:36の新快速で京都駅に18:12に着きます（1,810円）。",
          "Skipping Kyorinbo? Take the 16:24 bus (16:25 at weekends) to Yokaichi and the Ohmi Railway to Omi-Hachiman (17:28). The 17:36 Special Rapid reaches Kyoto Station at 18:12 (¥1,810).", frm="2026-11-29"),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "none": [NO["eigenji"]]},
          "永源寺に寄らない日は、近江八幡から米原方面の普通電車でひと駅、安土へ。ライトアップは17:30からなので、近江八幡17:24発（安土17:27着・190円）で十分です。",
          "Not going to Eigenji? From Omi-Hachiman take a local train one stop towards Maibara to Azuchi. The illumination starts at 17:30, so the 17:24 from Omi-Hachiman (Azuchi 17:27, ¥190) is fine."),
    ]}

# =====================================================================
# コース2：湖東三山（sanzan）
# =====================================================================
AINORI_URL = "https://www.city.hikone.lg.jp/kurashi/kotsu_doro/3/6022.html"
SHUTTLE_OVER = notice("シャトルバスは終了。乗合タクシーで回れます", "Shuttle over: use the shared taxi",
                      "2026年の紅葉シャトルバスは11月29日で終わりました。西明寺と金剛輪寺へは、予約制の「愛のりタクシー」（現金のみ。12月29日〜1月3日は運休）で。京都駅9:34発（土日祝9:37発）の普通電車で河瀬（かわせ）に10:34（10:32）着（990円）。東口10:51発 → 西明寺11:08（800円）。門前でお昼にして（12月は月・火休み）、西明寺12:56発 → 金剛輪寺13:03（400円）。帰りは金剛輪寺14:42発 → 稲枝（いなえ）駅15:54（800円。各地の停留所を回る路線なので、時刻表では1時間12分）、16:13発の電車で京都駅17:06着（990円）。15:42発なら京都駅18:06、16:42発なら19:06に着きます。予約は1週間前から乗る1時間前までに、3回分まとめて近江タクシー彦根営業所 0749-22-1111へ（「愛のりタクシーお願いします」）。百済寺は路線にないので、八日市駅からタクシーで約10分です。",
                      "The 2026 autumn shuttle ended on 29 November. For Saimyoji and Kongorinji, use the bookable “Ainori Taxi” shared taxi (cash only; not running 29 Dec – 3 Jan). Take the 9:34 local from Kyoto Station (9:37 at weekends and holidays) to Kawase, 10:34 (10:32), ¥990. Taxi from the east exit 10:51 → Saimyoji 11:08 (¥800). Lunch by the gate (closed Mon–Tue in December), then Saimyoji 12:56 → Kongorinji 13:03 (¥400). Back: Kongorinji 14:42 → Inae Station 15:54 (¥800; the route winds between stops, 1 hour 12 minutes by the timetable), then the 16:13 train to Kyoto Station, 17:06 (¥990). The 15:42 taxi gets you to Kyoto Station at 18:06, the 16:42 at 19:06. Book all three rides from a week to 1 hour ahead with Ohmi Taxi Hikone, 0749-22-1111 (ask for “Ainori Taxi”). Hyakusaiji is off this route: about 10 minutes by taxi from Yokaichi Station.",
                      url=AINORI_URL, frm=AFTER_SHUTTLE)

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
         blurb=T("10:00の紅葉シャトルバス（11月29日まで）に乗るため、京都駅を平日8:37・土日祝8:30の新快速で出ます。もみじきっぷを買って予約しておくと安心。",
                 "To catch the 10:00 autumn shuttle (until 29 Nov), take the Special Rapid from Kyoto Station at 8:37 on weekdays, 8:30 at weekends and holidays. Buying a Momiji Kippu and booking a seat is the safe way."),
         lat=35.27200, lng=136.26250, cash=True,
         text=T("京都から彦根駅へ\n\n"
                "湖東三山（ことうさんざん）の西明寺・金剛輪寺・百済寺は、鈴鹿の山すその離れた場所にあります。2026年の紅葉の時期（11月19日〜29日）は、JR彦根駅の西口から紅葉シャトルバスが出て、3つのお寺を結びます。このコースは10:00発のバス（第2便）に乗る組み立てです。\n\n"
                "平日は京都駅8:37発の新快速「長浜」行きで、彦根に9:31着。土日祝は京都駅8:30発の新快速「米原」行きで、彦根に9:20着。どちらも乗り換えなしで1,170円です。写真は途中で通る近江八幡駅です。\n\n"
                "三条のあたりからは、地下鉄で京都駅へ（烏丸御池で乗り換え、約15分・260円）。平日は三条京阪8:05発、土日祝は7:59発なら間に合います。\n\n"
                "三条からは、地下鉄「六地蔵」行きで山科へ出て、同じ新快速に乗ることもできます（三条京阪8:22発、土日祝8:10発。彦根まで1,250円）。\n\n"
                "バスは路線バスの車両で、座れないこともあります。彦根駅発の便は、1日乗り放題の「もみじきっぷ」（大人2,500円・当日に現金で）を買う人だけ予約でき、予約した人が先に乗れます。予約はWebなら乗る日の2日前まで、電話（湖国バス彦根営業所 0749-25-2501、9:00〜18:00）なら前日まで。予約がないと、希望の便に乗れないことがあります。\n\n"
                "このコースのバス代を1回ずつ払うと2,300円。もみじきっぷなら2,500円で、3つのお寺の入山料が50円ずつ安くなり、予約もできます。\n\n"
                "バスの時刻に合わせるのが大変なら、京都駅八条口から湖東三山と永源寺をまわる昼食付きの定期観光バス（京阪バス、12月13日まで。12月6日までは大人14,000円）もあります（湖東三山のチラシより）。\n\n"
                "おすすめ出発時間：京都駅 8:37（土日祝は8:30）",
                "Kyoto to Hikone Station\n\n"
                "The three Koto Sanzan temples, Saimyoji, Kongorinji and Hyakusaiji, lie far apart along the foot of the Suzuka hills. In the 2026 leaf season (19–29 November) an autumn shuttle bus links them from the west exit of JR Hikone Station. This course is built around the 10:00 bus (no. 2).\n\n"
                "On weekdays, take the 8:37 Special Rapid for Nagahama from Kyoto Station, reaching Hikone at 9:31. At weekends and holidays, take the 8:30 Special Rapid for Maibara, reaching Hikone at 9:20. Both run direct, ¥1,170. The photo is Omi-Hachiman Station, which you pass on the way.\n\n"
                "From around Sanjo, take the subway to Kyoto Station (change at Karasuma Oike; about 15 minutes, ¥260). The 8:05 from Sanjo Keihan on weekdays, or the 7:59 at weekends and holidays, gets you there in time.\n\n"
                "From Sanjo you can also ride a Rokujizo-bound subway to Yamashina and board the same Special Rapid (Sanjo Keihan 8:22, or 8:10 at weekends and holidays; ¥1,250 to Hikone).\n\n"
                "The shuttle is an ordinary city-type bus and you may have to stand. Seats on buses from Hikone can be booked only with the “Momiji Kippu” day pass (¥2,500, cash on the day), and those who book board first. Book online up to 2 days before, or by phone (Kokoku Bus Hikone, 0749-25-2501, 9:00–18:00) up to the day before. Without a booking you may not get on the bus you want.\n\n"
                "Single fares for this course add up to ¥2,300. The ¥2,500 Momiji Kippu takes ¥50 off each temple’s admission and lets you book.\n\n"
                "If juggling the bus times sounds like too much, there is also a guided coach tour with lunch from Kyoto Station Hachijo exit to the three temples and Eigenji (Keihan Bus, until 13 Dec; ¥14,000 for adults until 6 Dec; from the Koto Sanzan leaflet).\n\n"
                "Recommended departure: Kyoto Station 8:37 (8:30 at weekends and holidays)"),
         gmaps=[gm("彦根駅 西口", "Hikone Station (west exit)", 35.27200, 136.26250, "彦根駅 西口")],
         links=[SHUTTLE, SHUTTLE_BOOK, KOTOSANZAN, YAHOO],
         notices=[notice("もみじきっぷは現金だけ", "Momiji Kippu: cash only",
                         "もみじきっぷ（大人2,500円）は、当日に彦根駅西口のバスのりばかバスの中で、現金で払います。予約した人も、乗る日に現金で払います。",
                         "The Momiji Kippu (¥2,500 adults) is paid in cash on the day, at the Hikone Station west-exit bus stop or on the bus, even if you booked.",
                         url="https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/", to=SHUTTLE_END),
                  SHUTTLE_OVER],
         info=info([row("train", "平日：京都駅 8:37 新快速 → 彦根 9:31。土日祝：京都駅 8:30 → 彦根 9:20。1,170円",
                        "Weekdays: Kyoto Station 8:37 Special Rapid → Hikone 9:31. Weekends: Kyoto Station 8:30 → Hikone 9:20. ¥1,170", until=SHUTTLE_END),
                    row("train", "11月30日から：京都駅 9:34（土日祝9:37）普通 → 河瀬 10:34（10:32）、990円",
                        "From 30 Nov: Kyoto Station 9:34 local (weekends 9:37) → Kawase 10:34 (10:32), ¥990", frm=AFTER_SHUTTLE),
                    row("taxi", "愛のりタクシー：河瀬駅東口 10:51 → 西明寺 11:08（800円・現金のみ・要予約）",
                        "Ainori Taxi: Kawase east exit 10:51 → Saimyoji 11:08 (¥800, cash only, booking required)", frm=AFTER_SHUTTLE),
                    row("train", "三条京阪 → 京都駅：地下鉄（烏丸御池で乗り換え）約15分・260円", "Sanjo Keihan → Kyoto Station: subway (change at Karasuma Oike), about 15 min, ¥260"),
                    row("bus", "紅葉シャトルバス（2026年11月19日〜29日）：彦根駅西口4番のりば 9:00・10:00・11:00・12:00発。このコースは10:00発 → 西明寺 10:32（700円）",
                        "Autumn shuttle (19–29 Nov 2026): Hikone Station west exit, stop 4, at 9:00, 10:00, 11:00, 12:00. This course: 10:00 → Saimyoji 10:32 (¥700)", until=SHUTTLE_END),
                    row("fee", "もみじきっぷ 大人2,500円・こども1,250円（当日だけ有効、現金。三山の入山料が50円引き）",
                        "Momiji Kippu ¥2,500 adults, ¥1,250 children (valid on the day, cash; ¥50 off each temple)", until=SHUTTLE_END)],
                   cash=True,
                   tip=T("電車は乗換案内（2026年11月25日・28日・30日、12月5日のダイヤ）、バスと予約は" + FLYER_TIP_JA + "、愛のりタクシーは彦根市の時刻表（2026年4月改正）で、2026年11月22日に確認しました。",
                         "Trains checked on a route planner (25, 28 and 30 Nov and 5 Dec 2026); the bus and booking on " + FLYER_TIP_EN + "; the Ainori Taxi on Hikone City’s timetable (revised April 2026), 22 Nov 2026."))),
    dict(id="saimyoji", _extra=SAIMYOJI_EXTRA,
         name=T("西明寺（湖東三山）", "Saimyoji Temple (Koto Sanzan)"), kind=T("寺", "Temple"),
         blurb=T("湖東三山のいちばん北。鎌倉時代の本堂と三重塔は、どちらも国宝。秋は紅葉と一緒に、秋から咲く「不断桜」も。お昼は門前で近江牛を。",
                 "The northernmost Koto Sanzan temple, with a Kamakura-period main hall and pagoda that are both National Treasures, and a cherry that blooms in autumn. Lunch on Omi beef by the gate."),
         lat=35.18334, lng=136.28475,
         text=T("西明寺（さいみょうじ）\n\n"
                "湖東三山のいちばん北にある天台宗のお寺です。鎌倉時代の本堂と三重塔は、どちらも国宝。杉木立の中に、ひわだぶきの屋根が2つ並びます。本坊の庭「蓬莱庭（ほうらいてい）」から本堂までは石段を上ります。\n\n"
                "秋は境内の約1,000本のもみじが色づき、11月に満開になる「西明寺不断桜（ふだんざくら）」も咲くので、紅葉と桜が一度に見られます（湖東三山のチラシより）。2026年は、宝冠毘沙門天（ほうかんびしゃもんてん）像の初めての公開（12月13日まで）と、本堂の後ろの仏像群の特別拝観（11月30日まで・1,000円）があります。\n\n"
                "シャトルバスで10:32に着いたら、1時間ほどお参りを。境内は持ち込みの飲食ができません。お昼は門前の「近江牛一筋＠千成亭ぎゅ〜じあむ」で（11:00〜15:00、ラストオーダー14:30。公式サイト）。定休日の月・火も紅葉シーズンは開いていて（公式サイト）、湖東三山のチラシでも11月は無休です。もみじきっぷを見せると、ここで食事をした人はウーロン茶が1杯無料です。\n\n"
                "次のバスは西明寺12:32発。金剛輪寺（12:47）では降りずに、そのまま百済寺まで乗ります（13:10着・500円）。\n\n"
                "おすすめ訪問時間：10:32〜12:30（お昼を含む）",
                "Saimyoji Temple\n\n"
                "A Tendai temple, the northernmost of the Koto Sanzan. Its Kamakura-period main hall and three-storied pagoda are both National Treasures, their cypress-bark roofs side by side among tall cedars. From the garden of the main residence, Horai-tei, stone steps lead up to the main hall.\n\n"
                "In autumn about 1,000 maples colour the grounds, and the temple’s “fudan-zakura” cherry is in full bloom in November, so you see leaves and blossom together (Koto Sanzan leaflet). In 2026 the crowned Bishamonten statue is on show for the first time (until 13 Dec), and the statues behind the main altar can be seen (until 30 Nov, ¥1,000).\n\n"
                "Arriving on the 10:32 shuttle, give the temple about an hour. You can’t eat or drink your own food in the grounds. For lunch, go to “Omi Beef Hitosuji @ Sennaritei Gyuseum” by the gate (11:00–15:00, last order 14:30; official site). Its usual Monday and Tuesday closing doesn’t apply in the autumn-leaf season (official site), and the Koto Sanzan leaflet says it is open every day in November. Show your Momiji Kippu with a meal there for a free oolong tea.\n\n"
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
                    row("hours", "お昼：千成亭ぎゅ〜じあむ 11:00〜15:00（ラストオーダー14:30）。11月は無休（月・火の定休は紅葉シーズンを除く）",
                        "Lunch: Sennaritei Gyuseum 11:00–15:00 (last order 14:30). Open daily in November (the Mon–Tue closing doesn’t apply in the leaf season)"),
                    row("bus", "西明寺 12:32 → 百済寺 13:10（500円）。彦根駅へ戻るバスは西明寺 13:43・14:43・15:53・16:53発（700円）",
                        "Saimyoji 12:32 → Hyakusaiji 13:10 (¥500). Back to Hikone from Saimyoji at 13:43, 14:43, 15:53, 16:53 (¥700)", until=SHUTTLE_END),
                    row("taxi", "愛のりタクシー：西明寺 12:56 → 金剛輪寺 13:03（400円）。河瀬駅へ戻る便は毎時12分発 → 29分着（800円、16:12発まで）",
                        "Ainori Taxi: Saimyoji 12:56 → Kongorinji 13:03 (¥400). Back to Kawase at :12, arriving :29 (¥800; until 16:12)", frm=AFTER_SHUTTLE)],
                   tip=T("西明寺の公式サイト（拝観のご案内。入山料は「令和5年4月より変更」の料金表の金額）、" + FLYER_TIP_JA + "で2026年11月22日に、千成亭ぎゅ〜じあむの公式サイト（施設のご案内）で11月23日に確認しました。",
                         "Checked on the Saimyoji website (fees from its table, “changed April 2023”) and " + FLYER_TIP_EN + " on 22 Nov 2026, and the Gyuseum website (facility guide) on 23 Nov."),
                   checked=RECHECKED)),
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
                "帰りは16:43発のバスで彦根駅へ（17:30着。もみじきっぷで乗れます）。彦根17:52発の新快速で、京都駅に18:42着（平日・土日祝とも、1,170円）。京都に戻って晩ごはんにして、21〜22時までゆっくりできます。三条・木屋町・先斗町のあたりへは、京都駅から地下鉄で約15分です。\n\n"
                "おすすめ訪問時間：15:43〜16:43",
                "Kongorinji Temple\n\n"
                "A Tendai temple, the middle one of the Koto Sanzan. From the outer gate an uphill approach is lined on both sides with a thousand Jizo statues. At the top is the Niten-mon gate, and beyond it the Kamakura-period main hall (a National Treasure) and a three-storied pagoda. The maples around the hall and in the garden are called “blood-dyed maples” for their deep colour (temple website). The photos are from 17 November 2022.\n\n"
                "The bus from Hyakusaiji arrives at 15:43, and last entry is 16:30. It is uphill from the outer gate, so head straight up to the main hall. In 2026 the hidden Daikokuten statue is on show (until 13 Dec), and the Dainichi Nyorai in the pagoda is opened on fine days until 29 Nov.\n\n"
                "Leave on the 16:43 bus to Hikone Station (17:30; covered by the Momiji Kippu day ticket). The 17:52 Special Rapid from Hikone reaches Kyoto Station at 18:42 every day (¥1,170), so you can take your time over dinner until 21:00–22:00. Sanjo, Kiyamachi and Pontocho are about 15 minutes from Kyoto Station by subway.\n\n"
                "Recommended visit time: 15:43–16:43"),
         gmaps=[gm("金剛輪寺", "Kongorinji", 35.16128, 136.28304, "金剛輪寺 愛荘町松尾寺")],
         links=[link("official", "金剛輪寺 公式サイト（参拝・境内）", "Kongorinji (official, Japanese)", "https://kongourinji.jp/precinct"), SHUTTLE,
                link("info", "乗合タクシーの時刻（金剛輪寺 交通）", "Shared taxi times (Kongorinji access page, Japanese)", "https://kongourinji.jp/access"),
                link("timetable", "愛のりタクシーの時刻表（彦根市）", "Ainori Taxi timetables (Hikone City, Japanese)", AINORI_URL)],
         notices=[SHUTTLE_OVER],
         info=info([row("hours", "8:30〜16:30（閉山17:00）", "8:30–16:30 (grounds close 17:00)"),
                    row("hours", "2026年秋：秘仏 大黒天の公開 12月13日まで。三重塔 大日如来の開扉 11月29日まで（天気のよい日だけ）",
                        "Autumn 2026: hidden Daikokuten until 13 Dec; Dainichi Nyorai in the pagoda until 29 Nov (fine days only)", until=SPECIAL_END),
                    row("fee", "大人800円、中学生300円、小学生200円", "¥800 adults, ¥300 junior high, ¥200 elementary"),
                    row("bus", "金剛輪寺 16:43 → 彦根駅 17:30（もみじきっぷで乗れます）。ほかに13:33・14:33・15:43発", "Kongorinji 16:43 → Hikone Station 17:30 (covered by the Momiji Kippu). Also 13:33, 14:33, 15:43", until=SHUTTLE_END),
                    row("train", "彦根 17:52 新快速 → 京都駅 18:42、1,170円", "Hikone 17:52 Special Rapid → Kyoto Station 18:42, ¥1,170", until=SHUTTLE_END),
                    row("taxi", "愛のりタクシー：金剛輪寺 14:42 → 稲枝駅 15:54（800円）。15:42発 → 16:54、16:42発 → 17:54",
                        "Ainori Taxi: Kongorinji 14:42 → Inae Station 15:54 (¥800). 15:42 → 16:54, 16:42 → 17:54", frm=AFTER_SHUTTLE),
                    row("train", "稲枝 16:13 → 京都駅 17:06、990円。17:13発 → 18:06、18:11発 → 19:06",
                        "Inae 16:13 → Kyoto Station 17:06, ¥990. 17:13 → 18:06, 18:11 → 19:06", frm=AFTER_SHUTTLE)],
                   tip=T("時間・料金は金剛輪寺の公式サイト（参拝・境内）、特別公開とバスは" + FLYER_TIP_JA + "、電車は乗換案内で、2026年11月22日に確認しました。境内の食事処「華楽坊」は5名以上の予約制です（公式サイト）。",
                         "Hours and fees from the Kongorinji website, special openings and buses from " + FLYER_TIP_EN + ", trains on a route planner, 22 Nov 2026. The temple restaurant, Karakubo, takes bookings for 5 or more only (website)."))),
    dict(id="kyorinbo", name=T("教林坊（夜のライトアップ）", "Kyorinbo (evening illumination)"), kind=T("寺", "Temple"),
         blurb=T("春と秋だけ公開される、竹林と石の庭の小さなお寺。彦根から電車で安土へ、タクシーで夜の庭へ。最初は外してあります。",
                 "A small temple of bamboo and stone gardens, open only in spring and autumn. Train from Hikone to Azuchi, then a taxi. Not selected at first."),
         lat=35.13898, lng=136.16383, caution=T("駅からタクシー・12月6日まで", "Taxi from the station · until 6 Dec"),
         text=T("教林坊（きょうりんぼう）\n\n"
                "観音正寺のある繖山（きぬがさやま）のふもと、安土町石寺の山あいにある小さなお寺です。ふだんは公開されておらず、春と秋の特別公開のときだけ入れます。竹林の小道を抜けると、苔と巨石の庭。書院の丸窓や三日月の窓から見る庭も絵のようです。写真は2026年11月17日の夜のライトアップです。\n\n"
                "湖東三山のあとに寄るなら、彦根駅17:30着のバスから、18:02発の普通電車（網干行き）で安土へ（18:19着・330円）。北口からタクシーで約10分、18:35ごろ着きます。受付は19:00まで。タクシーは前もって予約し、帰りの迎えも頼んでおきましょう。\n\n"
                "帰りは安土19:28発の電車に乗り、次の近江八幡で19:37発の新快速に乗り換えて、京都駅に20:12着（770円）。次は安土19:50発で京都駅20:36着（土日祝は19:55発で20:41着）。朝8時台からの長い1日になり、行きと帰りにタクシー代（片道2,500円前後、教林坊の公式サイトの目安）もかかるので、最初は外してあります。\n\n"
                + KYORIN_EXTRA_JA + "\n\nおすすめ訪問時間：18:35〜19:10",
                "Kyorinbo\n\n"
                "A small temple tucked in the hills of Ishidera, Azuchi, at the foot of Mt. Kinugasa. It is usually closed and opens only for special spring and autumn openings. A path through bamboo leads to a garden of moss and huge rocks, framed by the round and crescent-moon windows of the study hall. The photos show the illumination on 17 November 2026.\n\n"
                "To add it after the three temples, take the 18:02 local train (for Aboshi) from Hikone, after the bus gets in at 17:30, to Azuchi (18:19, ¥330). A taxi from the north exit takes about 10 minutes, so you arrive around 18:35; last entry is 19:00. Book the taxi ahead, including the pick-up back.\n\n"
                "Head home on the 19:28 train from Azuchi and change one stop later at Omi-Hachiman to the 19:37 Special Rapid: Kyoto Station at 20:12, ¥770. The next is 19:50 → 20:36 (19:55 → 20:41 at weekends and holidays). It makes a long day from the 8 o’clock hour, and you pay for a taxi each way (around ¥2,500 one way, the temple’s own estimate), so it isn’t selected at first.\n\n"
                + KYORIN_EXTRA_EN + "\n\nRecommended visit time: 18:35–19:10"),
         gmaps=[gm("教林坊", "Kyorinbo", 35.13898, 136.16383, "教林坊 近江八幡市安土町石寺1145"), gm("安土駅", "Azuchi Station", 35.14290, 136.13790, "安土駅")],
         links=KYORIN_LINKS,
         notices=KYORIN_NOTICES,
         info=info(KYORIN_ROWS + [
             row("train", "行き：彦根 18:02 → 安土 18:19（330円）", "There: Hikone 18:02 → Azuchi 18:19 (¥330)", until=SHUTTLE_END),
             row("train", "行き：稲枝 17:13 → 安土 17:20（200円）", "There: Inae 17:13 → Azuchi 17:20 (¥200)", frm=AFTER_SHUTTLE, until=KYORIN_LU_END),
             row("train", "帰り：安土 19:28 → 近江八幡 19:37 新快速 → 京都駅 20:12、770円。次は19:50 → 20:36（土日祝19:55 → 20:41）",
                 "Back: Azuchi 19:28 → Omi-Hachiman 19:37 Special Rapid → Kyoto Station 20:12, ¥770. Next 19:50 → 20:36 (weekends 19:55 → 20:41)")],
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
          "西明寺に寄らない日は、11:00発のバスで百済寺へ直行できます（12:10着・1,000円）。京都駅を平日9:34、土日祝9:37に出る普通電車なら乗り換えなしで間に合います（彦根10:41・10:39着、1,170円）。お昼は彦根で済ませるか、持っていくと安心です。",
          "Skipping Saimyoji? The 11:00 bus goes straight to Hyakusaiji (12:10, ¥1,000); the 9:34 local from Kyoto Station (9:37 at weekends) runs direct to Hikone, arriving 10:41 (10:39), ¥1,170. Eat in Hikone first or bring lunch.", to=SHUTTLE_END),
        H(NO, "hyakusaiji", {"any": [NO["hyakusaiji"]], "none": [NO["kongorinji"], NO["kyorinbo"]]},
          "金剛輪寺に寄らない日は、百済寺のライトアップ（17時から、11月30日まで）まで残れます。百済寺本坊前17:54発のちょこっとバスで八日市駅へ（約35分）、近江鉄道と近江八幡19:06発の新快速で京都駅に19:42着（平日・土日祝とも、合わせて1,340円）。",
          "Skipping Kongorinji? Stay for Hyakusaiji’s illumination (from 17:00, until 30 Nov). The 17:54 Chokotto Bus from Hyakusaiji Honbo-mae runs to Yokaichi (about 35 min); the Ohmi Railway and the 19:06 Special Rapid from Omi-Hachiman get you to Kyoto Station at 19:42 every day (¥1,340 in all).", to=HYAKU_LU_END),
        H(NO, "kongorinji", {"any": [NO["kongorinji"]], "none": [NO["hyakusaiji"]]},
          "百済寺に寄らない日は、西明寺11:32発のバスで金剛輪寺へ（11:47着・200円）。帰りのバスは金剛輪寺13:33・14:33・15:43・16:43発です（彦根駅まで800円）。",
          "Skipping Hyakusaiji? Take the 11:32 bus from Saimyoji to Kongorinji (11:47, ¥200). Buses back leave Kongorinji at 13:33, 14:33, 15:43 and 16:43 (¥800 to Hikone).", to=SHUTTLE_END),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "andAny": [NO["kongorinji"]]},
          "金剛輪寺16:43発のバスで彦根駅17:30着、18:02の普通電車で安土へ。タクシーは安土駅に18:20ごろ迎えに来てもらうよう予約しておきます。",
          "From Kongorinji take the 16:43 bus to Hikone (17:30) and the 18:02 local to Azuchi. Book a taxi to meet you at Azuchi around 18:20.", to=SHUTTLE_END),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "none": [NO["kongorinji"]]},
          "金剛輪寺に寄らない日は、百済寺15:20発のバスで彦根駅16:30着、17:04発の普通電車で安土へ（17:20着・330円）。タクシーで17:35ごろ、ライトアップが始まったところに着きます。",
          "Skipping Kongorinji? The 15:20 bus from Hyakusaiji reaches Hikone at 16:30; the 17:04 local reaches Azuchi at 17:20 (¥330), and a taxi gets you to Kyorinbo around 17:35, just as the illumination starts.", to=SHUTTLE_END),
        H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "andAny": [NO["kongorinji"]]},
          "シャトルバスのない日は、金剛輪寺15:42発の愛のりタクシーで稲枝駅16:54着、17:13発の電車で安土へ（17:20着・200円）。タクシーで17:30すぎに着きます。帰りは安土19:28発で京都駅20:12着（770円）。",
          "Without the shuttle, take the 15:42 Ainori Taxi from Kongorinji to Inae (16:54) and the 17:13 train to Azuchi (17:20, ¥200); a taxi gets you to Kyorinbo just after 17:30. Back on the 19:28 from Azuchi: Kyoto Station 20:12 (¥770).", frm=AFTER_SHUTTLE, to=KYORIN_LU_END),
    ]}


# =====================================================================
# コース2の 11/30 から（乗合タクシーの時間割）。12/7 からは教林坊を抜く
# =====================================================================
def from_b(pid, **new):
    """コース2の同じスポットをもとに、書いた項目だけ差し替える"""
    d = dict(next(x for x in B if x["id"] == pid))
    d.update(new)
    return d


def about(pid, lang):
    """コース2の本文の最初の2段（名前と、お寺そのものの説明）"""
    return "\n\n".join(next(x for x in B if x["id"] == pid)["text"][lang].split("\n\n")[:2]) + "\n\n"


AINORI = link("timetable", "愛のりタクシーの時刻表（彦根市）", "Ainori Taxi timetables (Hikone City, Japanese)", AINORI_URL)
AINORI_HOW = link("info", "愛のりタクシーの予約のしかた（彦根市）", "How to book the Ainori Taxi (Hikone City, Japanese)", "https://www.city.hikone.lg.jp/kakuka/toshi_seisaku/5/2_3/28164.html")
TAXI_TIP_JA = "愛のりタクシーは彦根市の時刻表（2026年4月改正）"
TAXI_TIP_EN = "the Ainori Taxi on Hikone City’s timetable (revised April 2026)"
YEAR_END = notice("12月29日〜1月3日は運休", "No service 29 Dec – 3 Jan",
                  "愛のりタクシーは12月29日〜1月3日は走りません。この期間は、この時間割では回れません。",
                  "The Ainori Taxi doesn’t run from 29 December to 3 January, so this timetable doesn’t work on those days.",
                  url=AINORI_URL, to="2027-01-03")

C = [
    dict(id="kawaseeki", _photos=["omihachimaneki-1.jpg"],
         name=T("京都から河瀬駅へ（乗合タクシーのりば）", "Kyoto to Kawase Station (shared taxi stop)"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都駅9:34発（土日祝9:37発）の普通電車で河瀬へ。東口10:51発の予約制の乗合タクシーで西明寺へ向かいます。",
                 "Take the 9:34 local from Kyoto Station (9:37 at weekends and holidays) to Kawase, then the bookable 10:51 shared taxi from the east exit to Saimyoji."),
         lat=35.22518, lng=136.22500, cash=True, caution=T("要予約・現金のみ", "Booking required · cash only"),
         text=T("京都から河瀬駅へ\n\n"
                "2026年の紅葉シャトルバスは11月29日で終わりました。11月30日からは、予約制の乗合タクシー「愛のりタクシー」で、湖東三山のうち西明寺と金剛輪寺の2つを回ります。\n\n"
                "平日は京都駅9:34発の普通電車「米原」行きで、河瀬（かわせ）に10:34着。土日祝は9:37発で10:32着。乗り換えなしで990円です。東口10:51発の愛のりタクシーで、西明寺に11:08ごろ着きます（800円）。写真は途中で通る近江八幡駅です。\n\n"
                "この日に乗るタクシーは3回。①河瀬駅東口10:51 → 西明寺11:08（800円）、②西明寺12:56 → 金剛輪寺13:03（400円）、③金剛輪寺14:42 → 稲枝（いなえ）駅15:54（800円）。相乗りなので、着く時刻は多少前後します。\n\n"
                "予約は近江タクシー彦根営業所 0749-22-1111へ、乗る1週間前から1時間前までに。「愛のりタクシーお願いします」と伝えて、3回分をまとめて頼みます。予約のない便は走りません。支払いは降りるときに現金で（カード・ICカードは使えません）。2人以上でまとめて予約して同じ停留所から乗ると、運賃は半額になります。Web予約もありますが、利用者登録が必要です。\n\n"
                "三条のあたりからは、地下鉄で京都駅へ（烏丸御池で乗り換え、約15分・260円）。平日は三条京阪9:09発、土日祝は9:07発なら間に合います。\n\n"
                "おすすめ出発時間：京都駅 9:34（土日祝は9:37）",
                "Kyoto to Kawase Station\n\n"
                "The 2026 autumn shuttle ended on 29 November. From 30 November you visit two of the three Koto Sanzan temples, Saimyoji and Kongorinji, by the bookable “Ainori Taxi” shared taxi.\n\n"
                "On weekdays, take the 9:34 local for Maibara from Kyoto Station, reaching Kawase at 10:34. At weekends and holidays, take the 9:37, arriving at 10:32. It runs direct, ¥990. The 10:51 Ainori Taxi from the east exit reaches Saimyoji around 11:08 (¥800). The photo is Omi-Hachiman Station, which you pass on the way.\n\n"
                "You take three taxis: (1) Kawase east exit 10:51 → Saimyoji 11:08 (¥800), (2) Saimyoji 12:56 → Kongorinji 13:03 (¥400), (3) Kongorinji 14:42 → Inae Station 15:54 (¥800). Rides are shared, so arrival times vary a little.\n\n"
                "Book with Ohmi Taxi Hikone, 0749-22-1111, from a week to an hour before each ride. Ask for “Ainori Taxi” and book all three at once; a run with no booking doesn’t operate. Pay in cash as you get off (no cards or IC cards). Two or more people booked together from the same stop pay half fare. Web booking needs user registration.\n\n"
                "From around Sanjo, take the subway to Kyoto Station (change at Karasuma Oike; about 15 minutes, ¥260). The 9:09 from Sanjo Keihan on weekdays, or the 9:07 at weekends and holidays, gets you there in time.\n\n"
                "Recommended departure: Kyoto Station 9:34 (9:37 at weekends and holidays)"),
         gmaps=[gm("河瀬駅 東口", "Kawase Station (east exit)", 35.22518, 136.22500, "河瀬駅 東口")],
         links=[AINORI, AINORI_HOW, KOTOSANZAN, YAHOO],
         notices=[notice("3回とも予約・現金だけ", "Book all three rides · cash only",
                         "乗合タクシーは、予約がないと来ません。3回分を1時間前までに、近江タクシー彦根営業所 0749-22-1111へ。支払いは現金だけです。",
                         "The shared taxi only comes if booked. Book all three rides at least 1 hour ahead with Ohmi Taxi Hikone, 0749-22-1111. Cash only.",
                         url=AINORI_URL),
                  YEAR_END],
         info=info([row("train", "平日：京都駅 9:34 普通 → 河瀬 10:34。土日祝：京都駅 9:37 → 河瀬 10:32。990円",
                        "Weekdays: Kyoto Station 9:34 local → Kawase 10:34. Weekends: Kyoto Station 9:37 → Kawase 10:32. ¥990"),
                    row("taxi", "愛のりタクシー：河瀬駅東口 10:51 → 西明寺 11:08（800円）。予約 0749-22-1111、1週間前〜1時間前",
                        "Ainori Taxi: Kawase east exit 10:51 → Saimyoji 11:08 (¥800). Book on 0749-22-1111, from a week to 1 hour ahead"),
                    row("train", "三条京阪 → 京都駅：地下鉄（烏丸御池で乗り換え）約15分・260円", "Sanjo Keihan → Kyoto Station: subway (change at Karasuma Oike), about 15 min, ¥260")],
                   cash=True,
                   tip=T("電車は乗換案内（2026年11月30日、12月5日・6日・28日のダイヤ）、" + TAXI_TIP_JA + "で、2026年11月22日に確認しました。",
                         "Trains checked on a route planner (30 Nov and 5, 6, 28 Dec 2026), " + TAXI_TIP_EN + ", 22 Nov 2026."))),
    from_b("saimyoji",
           blurb=T("湖東三山のいちばん北。鎌倉時代の本堂と三重塔は、どちらも国宝。門前で近江牛のお昼にして（月・火は休み）、乗合タクシーで金剛輪寺へ。",
                   "The northernmost Koto Sanzan temple, with a Kamakura-period main hall and pagoda that are both National Treasures. Omi beef by the gate (closed Mon–Tue), then the shared taxi to Kongorinji."),
           text=T(about("saimyoji", "ja") +
                  "河瀬駅からの愛のりタクシーで11:08ごろ着。停留所は名勝庭園の前の受付です。1時間ほどお参りしたら、お昼は門前の「近江牛一筋＠千成亭ぎゅ〜じあむ」で（11:00〜15:00、ラストオーダー14:30。公式サイト）。11月は無休です。12月は月・火が定休で、紅葉シーズンは開いていることもあるので（公式サイト）、月・火は電話（0749-29-9090）で確かめてください。\n\n"
                  "境内は持ち込みの飲食ができません。休みの日は、京都駅を出る前に食べるか、持ってきたものを境内の外で。早く終わったら、11:56発のタクシー（金剛輪寺12:03着）にもできます。予約のときに決めてください。\n\n"
                  "12:56発の愛のりタクシーで金剛輪寺へ（13:03着・400円）。\n\n"
                  "おすすめ訪問時間：11:08〜12:56（お昼を含む）",
                  about("saimyoji", "en") +
                  "The Ainori Taxi from Kawase arrives around 11:08; the stop is the reception in front of the garden. Give the temple about an hour, then have lunch at “Omi Beef Hitosuji @ Sennaritei Gyuseum” by the gate (11:00–15:00, last order 14:30; official site). It is open every day in November. In December it usually closes on Mondays and Tuesdays, though it may open in the leaf season (official site), so phone ahead on those days (0749-29-9090).\n\n"
                  "You can’t eat or drink your own food in the grounds. If it’s closed, eat before you leave Kyoto or outside the grounds. If you need less time, there is an 11:56 taxi (Kongorinji 12:03); decide when you book.\n\n"
                  "Take the 12:56 Ainori Taxi to Kongorinji (13:03, ¥400).\n\n"
                  "Recommended visit time: 11:08–12:56 (with lunch)"),
           links=[link("official", "西明寺 公式サイト（拝観のご案内）", "Saimyoji (official, Japanese)", "https://saimyouji.com/information/"),
                  link("official", "近江牛一筋＠千成亭ぎゅ〜じあむ", "Sennaritei Gyuseum (official, Japanese)", "https://gyuseum.jp/"), AINORI],
           notices=[notice("門前のお昼は12月の月・火に注意", "Lunch by the gate: Mondays and Tuesdays in December",
                           "千成亭ぎゅ〜じあむの定休日は月・火です（紅葉シーズンを除く、と公式サイト）。11月は無休ですが、12月の月・火に行くなら電話（0749-29-9090）で確かめてください。境内は持ち込みの飲食ができません。",
                           "Sennaritei Gyuseum usually closes on Mondays and Tuesdays, except in the leaf season (official site). It is open every day in November; for a Monday or Tuesday in December, phone ahead (0749-29-9090). No food or drink of your own in the grounds.",
                           url="https://gyuseum.jp/guidance/")],
           info=info([row("hours", "8:30〜17:00（受付は16:30まで）", "8:30–17:00 (last entry 16:30)"),
                      row("hours", "2026年秋：本堂後陣の仏像群の特別拝観 11月30日まで（1,000円）", "Autumn 2026: statues behind the altar until 30 Nov (¥1,000)", until="2026-11-30"),
                      row("hours", "2026年秋：宝冠毘沙門天像の公開 12月13日まで", "Autumn 2026: crowned Bishamonten on show until 13 Dec", until=SPECIAL_END),
                      row("fee", "入山料 大人800円、中学生500円、小学生300円", "¥800 adults, ¥500 junior high, ¥300 elementary"),
                      row("hours", "お昼：千成亭ぎゅ〜じあむ 11:00〜15:00（ラストオーダー14:30）。11月は無休", "Lunch: Sennaritei Gyuseum 11:00–15:00 (last order 14:30). Open daily in November", until="2026-11-30"),
                      row("hours", "お昼：千成亭ぎゅ〜じあむ 11:00〜15:00（ラストオーダー14:30）。月・火定休（紅葉シーズンを除く。12月の月・火は電話で確認）",
                          "Lunch: Sennaritei Gyuseum 11:00–15:00 (last order 14:30). Closed Mon–Tue except in the leaf season (phone ahead on those days in December)", frm="2026-12-01"),
                      row("taxi", "愛のりタクシー：西明寺 12:56 → 金剛輪寺 13:03（400円）。河瀬駅へ戻る便は毎時12分発 → 29分着（800円、16:12発まで）",
                          "Ainori Taxi: Saimyoji 12:56 → Kongorinji 13:03 (¥400). Back to Kawase at :12, arriving :29 (¥800; until 16:12)")],
                     cash=True,
                     tip=T("西明寺の公式サイトと湖東三山の2026年のチラシは2026年11月22日に、千成亭ぎゅ〜じあむの公式サイト（施設のご案内）と、愛のりタクシーの時刻と運賃（彦根市の時刻表・2026年4月改正の料金表）は11月23日に確認しました。",
                           "Saimyoji website and the 2026 Koto Sanzan leaflet checked 22 Nov 2026; the Gyuseum website (facility guide) and the Ainori Taxi times and fares (Hikone City timetable and fare table, revised April 2026) checked 23 Nov."),
                     checked=RECHECKED)),
    from_b("kongorinji",
           blurb=T("千体のお地蔵さまが並ぶ参道を上ると、国宝の本堂のまわりに「血染めのもみじ」と呼ばれる木々。14:42の乗合タクシーまでゆっくり。",
                   "An approach lined with a thousand Jizo statues climbs to a National Treasure main hall among the “blood-dyed” maples. Take your time until the 14:42 shared taxi."),
           text=T(about("kongorinji", "ja") +
                  "西明寺からの愛のりタクシーで13:03ごろ着。総門から本堂までは上りの参道です。本堂と三重塔、下りてきて本坊明壽院の庭まで、帰りのタクシーまで1時間40分ほどあります。\n\n"
                  "帰りは金剛輪寺14:42発の愛のりタクシーで稲枝（いなえ）駅へ（15:54着・800円）。各地の停留所を回る路線なので、時刻表では1時間12分かかります。16:13発の電車で京都駅に17:06着（990円）。\n\n"
                  "もっとゆっくりするなら、15:42発で稲枝16:54着、17:13発の電車で京都駅18:06着。16:42発なら稲枝17:54着、18:11発で京都駅19:06着です。予約のときに決めてください。京都に戻って晩ごはんに。三条・木屋町・先斗町のあたりへは、京都駅から地下鉄で約15分です。\n\n"
                  "おすすめ訪問時間：13:03〜14:42",
                  about("kongorinji", "en") +
                  "The Ainori Taxi from Saimyoji arrives around 13:03. It is uphill from the outer gate. You have about 1 hour 40 minutes for the main hall, the pagoda and, on the way down, the garden of Myojuin.\n\n"
                  "Leave on the 14:42 Ainori Taxi to Inae Station (15:54, ¥800). The route winds between stops and takes 1 hour 12 minutes by the timetable. The 16:13 train reaches Kyoto Station at 17:06 (¥990).\n\n"
                  "For more time, the 15:42 taxi reaches Inae at 16:54 for the 17:13 train (Kyoto Station 18:06), and the 16:42 reaches Inae at 17:54 for the 18:11 (Kyoto Station 19:06). Decide when you book. Have dinner back in Kyoto; Sanjo, Kiyamachi and Pontocho are about 15 minutes from Kyoto Station by subway.\n\n"
                  "Recommended visit time: 13:03–14:42"),
           gmaps=[gm("金剛輪寺", "Kongorinji", 35.16128, 136.28304, "金剛輪寺 愛荘町松尾寺"), gm("稲枝駅", "Inae Station", 35.20332, 136.19454, "稲枝駅")],
           links=[link("official", "金剛輪寺 公式サイト（参拝・境内）", "Kongorinji (official, Japanese)", "https://kongourinji.jp/precinct"),
                  link("info", "乗合タクシーの時刻（金剛輪寺 交通）", "Shared taxi times (Kongorinji access page, Japanese)", "https://kongourinji.jp/access"), AINORI, YAHOO],
           notices=[],
           info=info([row("hours", "8:30〜16:30（閉山17:00）", "8:30–16:30 (grounds close 17:00)"),
                      row("hours", "2026年秋：秘仏 大黒天の公開 12月13日まで", "Autumn 2026: hidden Daikokuten on show until 13 Dec", until=SPECIAL_END),
                      row("fee", "大人800円、中学生300円、小学生200円", "¥800 adults, ¥300 junior high, ¥200 elementary"),
                      row("taxi", "愛のりタクシー：金剛輪寺 14:42 → 稲枝駅 15:54（800円）。15:42発 → 16:54、16:42発 → 17:54",
                          "Ainori Taxi: Kongorinji 14:42 → Inae Station 15:54 (¥800). 15:42 → 16:54, 16:42 → 17:54"),
                      row("train", "稲枝 16:13 → 京都駅 17:06、990円。17:13発 → 18:06、18:11発 → 19:06", "Inae 16:13 → Kyoto Station 17:06, ¥990. 17:13 → 18:06, 18:11 → 19:06")],
                     cash=True,
                     tip=T("時間・料金は金剛輪寺の公式サイト（参拝・境内）、特別公開は湖東三山の2026年のチラシ、" + TAXI_TIP_JA + "、電車は乗換案内で、2026年11月22日に確認しました。境内の食事処「華楽坊」は5名以上の予約制です（公式サイト）。",
                           "Hours and fees from the Kongorinji website, special openings from the 2026 Koto Sanzan leaflet, " + TAXI_TIP_EN + ", trains on a route planner, 22 Nov 2026. The temple restaurant, Karakubo, takes bookings for 5 or more only (website)."))),
    from_b("hyakusaiji", caution=T("乗合タクシーでは行けない", "Not on the shared-taxi route"),
           blurb=T("苔むした石垣と杉の参道を上る、近江で最も古いお寺のひとつ。乗合タクシーの路線にないので、別の日に。最初は外してあります。",
                   "One of the oldest temples in Omi, up a cedar-lined approach between mossy walls. It is off the shared-taxi route, so save it for another day. Not selected at first."),
           text=T(about("hyakusaiji", "ja") +
                  "愛のりタクシーの路線にないので、西明寺・金剛輪寺の時間割には入っていません。別の日に、午後から出かけて行けます。\n\n"
                  "京都駅13:00発の新快速で近江八幡へ（13:34着）。13:44発の近江鉄道で八日市14:04着、14:18発のちょこっとバス（愛東線・北回り）で百済寺本坊前に14:47着（京都駅から1,340円）。八日市駅からタクシーなら約10分です（百済寺の公式サイト）。\n\n"
                  "拝観は17:00まで（受付16:30まで）。帰りのバスは17:54発で京都駅19:42着（1,340円）。門が閉まってからバスまで1時間近くあり、外は暗くなるので、早めに戻るならタクシーを呼んで八日市駅へ。写真は2025年8月の新緑のころのものです。\n\n"
                  "おすすめ訪問時間：別の日の14:47〜17:00",
                  about("hyakusaiji", "en") +
                  "It is off the Ainori Taxi route, so it isn’t on the Saimyoji and Kongorinji timetable. You can visit on another day, leaving at lunchtime.\n\n"
                  "Take the 13:00 Special Rapid from Kyoto Station to Omi-Hachiman (13:34), the 13:44 Ohmi Railway to Yokaichi (14:04) and the 14:18 Chokotto Bus (Aito Line, northern loop) to Hyakusaiji Honbo-mae (14:47), ¥1,340 from Kyoto Station. By taxi it is about 10 minutes from Yokaichi Station (temple website).\n\n"
                  "The temple closes at 17:00 (last entry 16:30). The bus back leaves at 17:54, reaching Kyoto Station at 19:42 (¥1,340). That means nearly an hour’s wait in the dark after the gate closes, so to leave sooner, call a taxi to Yokaichi Station. The photos are from August 2025, in summer green.\n\n"
                  "Recommended visit time: 14:47–17:00, on another day"),
           links=[link("official", "百済寺 公式サイト", "Hyakusaiji (official, Japanese)", "http://hyakusaiji.jp/"),
                  link("info", "百済寺 交通案内", "Hyakusaiji access (Japanese)", "http://hyakusaiji.jp/info_access/"), TAXI_LIST, YAHOO],
           notices=[notice("西明寺・金剛輪寺とは別の日に", "On a different day from the other two",
                           "百済寺は愛のりタクシーの路線にありません。行き方は下の説明を見てください。",
                           "Hyakusaiji isn’t on the Ainori Taxi route. See below for how to get there.",
                           url="http://hyakusaiji.jp/info_access/")],
           info=info([row("hours", "8:30〜17:00（受付は16:30まで）", "8:30–17:00 (last entry 16:30)"),
                      row("hours", "2026年秋のライトアップ：11月30日まで 17時から（30日は受付19:00まで・閉門19:30）",
                          "Autumn 2026 illumination: until 30 Nov from 17:00 (on the 30th last entry 19:00, closes 19:30)", until=HYAKU_LU_END),
                      row("fee", "大人600円、中学生300円、小学生200円", "¥600 adults, ¥300 junior high, ¥200 elementary"),
                      row("train", "京都駅 13:00 → 近江八幡 13:44 近江鉄道 → 八日市 14:18 ちょこっとバス → 百済寺本坊前 14:47（1,340円）",
                          "Kyoto Station 13:00 → Omi-Hachiman 13:44 Ohmi Railway → Yokaichi 14:18 Chokotto Bus → Hyakusaiji Honbo-mae 14:47 (¥1,340)"),
                      row("bus", "帰り：百済寺本坊前 17:54 → 京都駅 19:42（1,340円）", "Back: Hyakusaiji Honbo-mae 17:54 → Kyoto Station 19:42 (¥1,340)")],
                     tip=T("時間・料金とタクシーの目安は百済寺の公式サイト、電車とバスは乗換案内（2026年11月30日、12月2日・5日・6日・28日）で、2026年11月22日に確認しました。",
                           "Hours, fees and the taxi estimate from the Hyakusaiji website; trains and buses on a route planner (30 Nov and 2, 5, 6, 28 Dec 2026), 22 Nov 2026."))),
    from_b("kyorinbo",
           blurb=T("春と秋だけ公開される、竹林と石の庭の小さなお寺。金剛輪寺を15:42に出て、稲枝から電車で安土へ、タクシーで夜の庭へ。最初は外してあります。",
                   "A small temple of bamboo and stone gardens, open only in spring and autumn. Leave Kongorinji at 15:42, take the train from Inae to Azuchi, then a taxi. Not selected at first."),
           text=T(about("kyorinbo", "ja") +
                  "金剛輪寺のあとに寄るなら、帰りの愛のりタクシーを15:42発で予約します。稲枝駅16:54着、17:13発の電車で安土へ（17:20着・200円）。北口からタクシーで約10分、17:35ごろ着きます。安土駅のタクシーは前もって予約し、帰りの迎えも18:40ごろに頼んでおきましょう。\n\n"
                  "帰りは安土18:58発の電車に乗り、次の近江八幡で19:06発の新快速に乗り換えて、京都駅に19:42着（770円）。ゆっくりするなら安土19:28発で京都駅20:12着です。行きと帰りにタクシー代（片道2,500円前後、教林坊の公式サイトの目安）がかかるので、最初は外してあります。\n\n"
                  + KYORIN_EXTRA_JA + "\n\nおすすめ訪問時間：17:35〜18:40",
                  about("kyorinbo", "en") +
                  "To add it after Kongorinji, book the 15:42 Ainori Taxi instead. It reaches Inae at 16:54; take the 17:13 train to Azuchi (17:20, ¥200). A taxi from the north exit takes about 10 minutes, so you arrive around 17:35. Book the Azuchi taxi ahead, with a pick-up around 18:40.\n\n"
                  "Head home on the 18:58 train from Azuchi and change one stop later at Omi-Hachiman to the 19:06 Special Rapid: Kyoto Station at 19:42, ¥770. For longer, the 19:28 from Azuchi arrives at 20:12. You pay for a taxi each way (around ¥2,500 one way, the temple’s own estimate), so it isn’t selected at first.\n\n"
                  + KYORIN_EXTRA_EN + "\n\nRecommended visit time: 17:35–18:40"),
           notices=KYORIN_NOTICES,
           info=info(KYORIN_ROWS + [
               row("train", "行き：稲枝 17:13 → 安土 17:20（200円）", "There: Inae 17:13 → Azuchi 17:20 (¥200)"),
               row("train", "帰り：安土 18:58 → 近江八幡 19:06 新快速 → 京都駅 19:42、770円。19:28発なら20:12",
                   "Back: Azuchi 18:58 → Omi-Hachiman 19:06 Special Rapid → Kyoto Station 19:42, ¥770. The 19:28 arrives 20:12")],
               tip=KYORIN_TIP)),
]


def C_PLAN(NO):
    night = "kyorinbo" in NO
    extra = [NO["kyorinbo"]] if night else []
    hints = [
        H(NO, "kawaseeki", {"any": [NO["kongorinji"]], "none": [NO["saimyoji"]]},
          "西明寺に寄らない日は、河瀬ではなく稲枝へ。京都駅9:34発（土日祝9:37発）で稲枝10:31（10:29）着、990円。10:51発の愛のりタクシーで金剛輪寺に12:03着（800円）。お昼は持っていきます。",
          "Skipping Saimyoji? Go to Inae instead of Kawase: the 9:34 from Kyoto Station (9:37 at weekends) arrives 10:31 (10:29), ¥990. The 10:51 Ainori Taxi reaches Kongorinji at 12:03 (¥800). Bring lunch."),
        H(NO, "saimyoji", {"any": [NO["saimyoji"]], "none": [NO["kongorinji"]] + extra},
          "金剛輪寺に寄らない日は、西明寺14:12発の愛のりタクシーで河瀬駅14:29着、14:41発の電車で京都駅15:37着（990円）。",
          "Skipping Kongorinji? The 14:12 Ainori Taxi from Saimyoji reaches Kawase at 14:29; the 14:41 train reaches Kyoto Station at 15:37 (¥990)."),
        H(NO, "hyakusaiji", {"any": [NO["hyakusaiji"]]},
          "百済寺は、西明寺・金剛輪寺の時間割には入りません。別の日に、京都駅13:00発で出かけてください。",
          "Hyakusaiji doesn’t fit into the Saimyoji and Kongorinji timetable. Go on another day, on the 13:00 from Kyoto Station."),
    ]
    if night:
        hints += [
            H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "andAny": [NO["kongorinji"]]},
              "金剛輪寺からのタクシーは15:42発（稲枝16:54着）で予約し、17:13発の電車で安土へ。安土駅のタクシーは17:20に迎えに来てもらうよう予約しておきます。",
              "Book the 15:42 taxi from Kongorinji (Inae 16:54), then take the 17:13 train to Azuchi. Book a taxi to meet you at Azuchi at 17:20."),
            H(NO, "kyorinbo", {"any": [NO["kyorinbo"]], "andAny": [NO["saimyoji"]], "none": [NO["kongorinji"]]},
              "金剛輪寺に寄らない日は、西明寺16:12発の愛のりタクシーで河瀬駅16:29着、17:10発の電車で安土17:20着（240円）。",
              "Skipping Kongorinji? The 16:12 Ainori Taxi from Saimyoji reaches Kawase at 16:29; the 17:10 train reaches Azuchi at 17:20 (¥240)."),
        ]
    return {
        "_note": "「選んで回る」の設定。河瀬駅はいつも入る。defaultPicks は乗合タクシーの時間割どおりの2か所（西明寺→金剛輪寺）。百済寺は別の日に、教林坊（12/6まで）は寄り道。",
        "defaultMode": "pick",
        "picks": [NO["saimyoji"], NO["kongorinji"], NO["hyakusaiji"]] + extra,
        "defaultPicks": [NO["saimyoji"], NO["kongorinji"]],
        "auto": {str(NO["kawaseeki"]): {"always": True}},
        "hints": hints,
    }


def C_SECTIONS(NO):
    out = [{"first": 1, "last": NO["saimyoji"], "area": T("河瀬・西明寺", "Kawase & Saimyoji"), "title": T("乗合タクシーで国宝の本堂へ", "A shared taxi to a National Treasure hall")},
           {"first": NO["kongorinji"], "last": NO["kongorinji"], "area": T("金剛輪寺", "Kongorinji"), "title": T("千体地蔵の参道と、午後の本堂", "A thousand Jizo and an afternoon at the hall")},
           {"first": NO["hyakusaiji"], "last": NO["hyakusaiji"], "area": T("別の日に：百済寺", "Another day: Hyakusaiji"), "title": T("苔の参道は午後の半日で", "The mossy approach, as a half day")}]
    if "kyorinbo" in NO:
        out.append({"first": NO["kyorinbo"], "last": NO["kyorinbo"], "area": T("寄り道：教林坊", "Option: Kyorinbo"), "title": T("帰りに夜のライトアップ", "An evening illumination on the way home")})
    return out


# =====================================================================
# コース1の 12/7 から（教林坊なし。永源寺から京都へ帰る）
# =====================================================================
def from_a(pid, **new):
    """コース1の同じスポットをもとに、書いた項目だけ差し替える"""
    d = dict(next(x for x in A if x["id"] == pid))
    d.update(new)
    return d


def paras(pid, lang):
    """コース1の本文を段ごとに分けたもの"""
    return next(x for x in A if x["id"] == pid)["text"][lang].split("\n\n")


W_START_JA, W_START_EN = paras("omihachimaneki", "ja"), paras("omihachimaneki", "en")
W_TIP = T("乗換案内（2026年12月7日・12日・13日のダイヤ）で確認しました。", "Checked on a route planner (7, 12 and 13 Dec 2026 timetables).")
W = [
    from_a("omihachimaneki",
           text=T("\n\n".join(W_START_JA[:-2] + ["紅葉の時期のあと、永源寺のまわりで開いている食事の店は確かめられませんでした（要確認）。永源寺に着くのは14時ごろなので、お昼は京都駅で買って持っていくと安心です。"] + W_START_JA[-1:]),
                  "\n\n".join(W_START_EN[:-2] + ["We couldn’t confirm any place to eat around Eigenji after the leaf season (please check). You get there around 14:00, so buy lunch at Kyoto Station and bring it along."] + W_START_EN[-1:])),
           notices=[notice("お昼は持っていく", "Bring lunch",
                           "永源寺の食事処とキッチンカーは紅葉の時期の案内で、そのあとも開いているかは確かめられませんでした（要確認）。お昼は京都駅で買っておくと安心です。",
                           "Eigenji’s eatery and food truck were announced for the leaf season, and we couldn’t confirm they open after it (please check). Buy lunch at Kyoto Station to be safe.",
                           url="https://eigenji-t.jp/haikan/")],
           info=info([row("train", "京都駅 10:00 新快速 → 近江八幡 10:35（土日祝10:34）→ 近江鉄道 10:42 → 太郎坊宮前 10:57。1,070円（JR680円＋近江鉄道390円）",
                          "Kyoto Station 10:00 Special Rapid → Omi-Hachiman 10:35 (weekends 10:34) → Ohmi Railway 10:42 → Taroubougu-mae 10:57. ¥1,070 (JR ¥680 + Ohmi Railway ¥390)"),
                      row("train", "三条京阪 → 京都駅：地下鉄（烏丸御池で乗り換え）約15分・260円", "Sanjo Keihan → Kyoto Station: subway (change at Karasuma Oike), about 15 min, ¥260")],
                     tip=W_TIP)),
    from_a("taroubouekimae",
           info=info([row("train", "近江八幡 → 太郎坊宮前 15分・390円。太郎坊宮前 → 八日市 4〜5分・160円（昼は毎時41分・59分ごろ）",
                          "Omi-Hachiman → Taroubougu-mae 15 min, ¥390. Taroubougu-mae → Yokaichi 4–5 min, ¥160 (around :41 and :59 at midday)")],
                     tip=W_TIP)),
    from_a("taroubou",
           blurb=T("742段の石段を登った先に、近江の平野を見渡す本殿。大きな岩が割れた「夫婦岩」の間を通ってお参りします。",
                   "Climb 742 stone steps to a main hall above the Omi plain. You reach it by squeezing between the split “Meoto-iwa” rocks.")),
    from_a("eigenji", caution=T("拝観は16:00まで・お昼は持参", "Closes 16:00 · bring lunch"),
           blurb=T("愛知川の渓谷にある禅寺。大きな山門と法堂を、閉まる16:00までゆっくり。写真は11月の紅葉とライトアップのころのものです。",
                   "A Zen temple in the Echigawa valley. Take your time at the great gate and lecture hall until it closes at 16:00. The photos show the November leaves and illumination."),
           text=T("\n\n".join(paras("eigenji", "ja")[:2]) + "\n\n"
                  "八日市駅の1番のりばから13:15発の近江鉄道バス（永源寺車庫行き）に乗り、「永源寺前」に13:44（土日祝は13:43）着（670円）。着いたら、持ってきたお昼を食べてからお参りを。紅葉の時期に開く食事処とキッチンカーが、そのあとも開いているかは確かめられませんでした（要確認）。\n\n"
                  "拝観は9:00〜16:00（永源寺の案内。11月だけ時間が変わる）。夜のライトアップは11月28日で終わりました。写真は11月の紅葉とライトアップのころのものです。\n\n"
                  "帰りは永源寺前16:24発（土日祝は16:25発）のバスで八日市駅へ（16:59着、土日祝17:00着）。17:09発の近江鉄道で近江八幡17:28着、17:36発の新快速で京都駅に18:12着です（合わせて1,810円）。早く見終わって15:56発のバスに乗っても、八日市で待って同じ電車になります。年末年始（12月30日〜1月3日）のバスは土日祝の時刻です（乗換案内）。\n\n"
                  "晩ごはんは京都に戻ってから、21〜22時まで。三条・木屋町・先斗町（ぽんとちょう）のあたりは遅くまで開いている店が多く、京都駅から地下鉄で約15分（260円）。18:30ごろには着けます。\n\n"
                  "おすすめ訪問時間：13:45〜16:00",
                  "\n\n".join(paras("eigenji", "en")[:2]) + "\n\n"
                  "Take the 13:15 Ohmi bus (for Eigenji Shako) from stop 1 at Yokaichi Station and get off at “Eigenji-mae” at 13:44 (13:43 at weekends and holidays; ¥670). Eat the lunch you brought, then visit. We couldn’t confirm that the leaf-season eatery and food truck stay open afterwards (please check).\n\n"
                  "The temple is open 9:00–16:00 (temple FAQ; only November differs). The evening illumination ended on 28 November. The photos show the November leaves and illumination.\n\n"
                  "Leave on the 16:24 bus from Eigenji-mae (16:25 at weekends and holidays) to Yokaichi (16:59, or 17:00). The 17:09 Ohmi Railway reaches Omi-Hachiman at 17:28, and the 17:36 Special Rapid reaches Kyoto Station at 18:12 (¥1,810 in all). If you finish early and take the 15:56 bus, you wait at Yokaichi for the same train. Over New Year (30 Dec – 3 Jan) buses follow the weekend timetable (route planner).\n\n"
                  "Dinner back in Kyoto can run to 21:00–22:00. Many places around Sanjo, Kiyamachi and Pontocho stay open late; they are about 15 minutes from Kyoto Station by subway (¥260), so you can be there by about 18:30.\n\n"
                  "Recommended visit time: 13:45–16:00"),
           links=[link("official", "永源寺 公式サイト（よくある質問：時間・料金）", "Eigenji (official FAQ: hours and fees, Japanese)", "https://eigenji-t.jp/contact/"),
                  link("official", "永源寺 公式サイト（お知らせ）", "Eigenji (official news, Japanese)", "https://eigenji-t.jp/haikan/"), EIGENJI_BUS, YAHOO],
           notices=[notice("拝観は16:00まで", "Closes at 16:00",
                           "永源寺の拝観は9:00〜16:00です（11月だけ時間が変わる）。夜のライトアップはありません。",
                           "Eigenji is open 9:00–16:00 (only November differs). There is no evening illumination.",
                           url="https://eigenji-t.jp/contact/")],
           info=info([row("hours", "9:00〜16:00（11月だけ時間が変わる）", "9:00–16:00 (only November differs)"),
                      row("hours", "お昼：食事処・キッチンカーの紅葉の時期のあとの営業は要確認。持っていくと安心", "Lunch: eatery and food truck not confirmed open after the leaf season; bring your own"),
                      row("fee", "参拝志納料 大人600円、中学生200円、小学生以下無料", "Admission ¥600 adults, ¥200 junior high, free for younger children"),
                      row("bus", "八日市駅1番のりば 13:15 → 永源寺前 13:44（土日祝13:43）、670円。帰りは永源寺前 16:24（土日祝16:25）→ 八日市駅 16:59（17:00）",
                          "Yokaichi stop 1 13:15 → Eigenji-mae 13:44 (weekends 13:43), ¥670. Back: Eigenji-mae 16:24 (weekends 16:25) → Yokaichi 16:59 (17:00)"),
                      row("train", "八日市 17:09 近江鉄道 → 近江八幡 17:36 新快速 → 京都駅 18:12（バスから合わせて1,810円）",
                          "Yokaichi 17:09 Ohmi Railway → Omi-Hachiman 17:36 Special Rapid → Kyoto Station 18:12 (¥1,810 incl. the bus)")],
                     tip=T("時間・参拝志納料は永源寺の公式サイト（よくある質問）、食事処は永源寺のお知らせ（2026年11月15日）、バスと電車は乗換案内（2026年12月7日・12日・13日・30日・31日、2027年1月1日・13日）で、2026年11月22日に確認しました。",
                           "Hours and admission from the temple FAQ, the eatery from the temple news (15 Nov 2026), buses and trains on a route planner (7, 12, 13, 30, 31 Dec 2026 and 1, 13 Jan 2027). Checked 22 Nov 2026."),
                     verified=False)),
]

W_PLAN = lambda NO: {
    "_note": "「選んで回る」の設定。近江八幡駅はいつも入る。太郎坊宮前駅は太郎坊宮を選ぶと入る。defaultPicks は12/7からの時間割どおりの2か所（全部）。",
    "defaultMode": "pick",
    "picks": [NO["taroubou"], NO["eigenji"]],
    "defaultPicks": [NO["taroubou"], NO["eigenji"]],
    "auto": {str(NO["omihachimaneki"]): {"always": True}, str(NO["taroubouekimae"]): {"any": [NO["taroubou"]]}},
    "hints": [
        H(NO, "omihachimaneki", {"any": [NO["eigenji"]], "none": [NO["taroubou"]]},
          "太郎坊宮に寄らない日は、京都駅10:00発の新快速で近江八幡へ。10:42発の近江鉄道を八日市（ようかいち）まで乗り、駅の1番のりば11:15発のバスで永源寺前に11:44（土日祝11:43）着。京都駅から1,810円です。拝観は16:00までなので、ゆっくり回れます。",
          "Skipping Taroubou-gu? Take the 10:00 Special Rapid from Kyoto Station to Omi-Hachiman, the 10:42 Ohmi Railway to Yokaichi and the 11:15 bus from stop 1, reaching Eigenji-mae at 11:44 (11:43 at weekends), ¥1,810 from Kyoto Station. The temple is open until 16:00, so take your time."),
        H(NO, "taroubou", {"any": [NO["taroubou"]], "none": [NO["eigenji"]]},
          "永源寺に行かない日は、太郎坊宮のあと近江鉄道で近江八幡へ戻り、八幡堀のあたりを歩いてお昼に（近江八幡のマップを見てください）。帰りは近江八幡17:36発の新快速で京都駅に18:12着（680円）。",
          "Not going to Eigenji? After the shrine, take the Ohmi Railway back to Omi-Hachiman, walk the canal district and have lunch there (see our Omihachiman map). The 17:36 Special Rapid from Omi-Hachiman reaches Kyoto Station at 18:12 (¥680)."),
    ]}


def H(NO, spot, rule, ja, en, frm=None, to=None):
    h = {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
    if frm:
        h["from"] = frm
    if to:
        h["to"] = to
    return h


def yt(a, b, md, hm, found, typ=1, year=2026):
    """乗換案内の検索結果（条件つきの URL）と、そこで見た数字"""
    q = {"from": a, "to": b, "y": year, "m": md[:2], "d": md[2:], "hh": hm[:2], "m1": hm[2], "m2": hm[3], "type": typ, "ticket": "ic",
         "expkind": 1, "userpass": 1, "ws": 3, "s": 0, "al": 0, "shin": 0, "ex": 0, "hb": 1, "lb": 1, "sr": 1}   # hb・lb・sr＝高速バス・路線バス・船も出す（バスの区間に要る）
    return {"what": f"乗換案内 {a.split('/')[0]}→{b.split('/')[0]} {int(md[:2])}月{int(md[2:])}日：{found}",
            "url": "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(q), "checked": CHECKED}


EIGENJI_STOP = "永源寺前/近江鉄道バス湖国バス"
SOURCES_COMMON = [
    {"what": "教林坊：秋の公開 11月1日〜12月15日 毎日、9:30〜16:30（ライトアップ期間は8:30から）、大人1,000円・小中学生300円。ライトアップ 令和8年11月14日〜12月6日 17:30〜19:30（19時受付終了）。予約の記載なし（団体バスだけ事前連絡）。三脚・一脚・長時間の撮影目的の入場は不可", "url": "https://kyourinbo.jimdofree.com/", "checked": CHECKED},
    {"what": "教林坊 アクセス：JR安土駅よりタクシー約10分（2,500円前後）・徒歩約60分。普通車100台", "url": "https://kyourinbo.jimdofree.com/ホーム/アクセス-駐車場ご案内/", "checked": CHECKED},
    {"what": "タクシー会社：永源寺タクシー 0748-27-1151、近江タクシー湖東営業所 0748-37-0106、滋賀第一交通 近江八幡営業所 0748-37-4000（料金の目安の記載なし）", "url": "https://www.higashiomi.net/guide/access.html", "checked": CHECKED},
    yt("安土", "京都", "1125", "1925", "19:28→近江八幡19:37新快速→20:12（770円）、次19:50→20:36"),
    yt("安土", "京都", "1128", "1925", "19:28→近江八幡19:37新快速→20:12（770円）、次19:55→20:41"),
    yt("安土", "京都", "1205", "1925", "19:28→20:12（770円）、次19:55→20:41"),
    yt("安土", "京都", "1125", "2228", "22:33→23:20、23:04→23:50、最終23:23→0:12"),
    yt("安土", "京都", "1128", "2228", "22:33→23:20、23:04→23:50、最終23:23→0:12"),
    yt("京都", "三条京阪", "1125", "2015", "地下鉄20:15→20:32（烏丸御池で乗り換え・260円）"),
]
SOURCES_A = [
    yt("京都", "太郎坊宮前", "1125", "0955", "10:00新快速 近江塩津行→近江八幡10:35/10:42→10:57（1,070円）"),
    yt("京都", "太郎坊宮前", "1128", "0955", "10:00→近江八幡10:34/10:42→10:57（1,070円）"),
    yt("京都", "太郎坊宮前", "1202", "0955", "10:00→10:57（1,070円）"),
    yt("三条京阪", "京都", "1125", "0929", "9:30→9:47（260円）"),
    yt("三条京阪", "京都", "1128", "0931", "9:32→9:45（260円）"),
    yt("三条京阪", "近江八幡", "1125", "0940", "9:44六地蔵行→山科10:06新快速→10:35（850円）。びわ湖浜大津行は980円"),
    yt("三条京阪", "近江八幡", "1128", "0940", "9:43→山科10:05→10:34（850円）"),
    yt("京都", EIGENJI_STOP, "1125", "0955", "10:00→八日市駅11:15のバス→11:44（1,810円）"),
    yt("京都", EIGENJI_STOP, "1128", "0955", "10:00→八日市駅11:15のバス→11:43（1,810円）"),
    yt("八日市", EIGENJI_STOP, "1125", "1300", "バス13:15→13:44（670円）"),
    yt("八日市", EIGENJI_STOP, "1128", "1300", "バス13:15→13:43（670円）"),
    {"what": "近江鉄道 太郎坊宮前→八日市：平日・土曜とも 11:41（土のみ）・11:59・12:41・12:59・13:41…（160円）。12:41・12:59のどちらも八日市駅13:15のバスに接続", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "近江鉄道バス 永源寺線（2024年4月1日改正の時刻表PDF）：八日市駅→永源寺 平日 …11:15・12:15・13:15・13:40・14:40… 土日祝 …11:15・12:15・13:15・14:15… 永源寺→八日市駅 平日 …15:26・15:56・16:24・16:54・17:22・17:54・18:24・18:54・19:27・19:52・20:27、土日祝 …15:26・15:56・16:25・16:55・17:25・18:16・19:16。八日市駅1番のりば、運賃670円。乗換案内の11月25日・28日の結果と一致", "url": "https://www.ohmitetudo.co.jp/bus/access/eigenji/", "checked": CHECKED},
    yt(EIGENJI_STOP, "安土", "1125", "1620", "16:24→八日市17:09→近江八幡17:41→17:44（1,320円）"),
    yt(EIGENJI_STOP, "安土", "1128", "1620", "16:25→八日市17:09→近江八幡17:41→17:44（1,320円）"),
    yt(EIGENJI_STOP, "京都", "1125", "1820", "18:24→近江八幡19:37新快速→20:12（1,810円）"),
    yt(EIGENJI_STOP, "京都", "1128", "1812", "18:16→近江八幡19:37新快速→20:12（1,810円）"),
    yt(EIGENJI_STOP, "京都", "1130", "1620", "16:24→近江八幡17:36新快速→18:12（1,810円）"),
    yt(EIGENJI_STOP, "京都", "1205", "1620", "16:25→近江八幡17:36新快速→18:12（1,810円）"),
    yt("近江八幡", "安土", "1125", "1705", "17:24→17:27（190円）"),
    yt("近江八幡", "安土", "1128", "1705", "17:24→17:27（190円）"),
    {"what": "太郎坊宮：参拝24時間、社務受付9:00〜17:00（ご祈祷等16:00まで）、拝観料・駐車料不要、約740段（ふもとから本殿まで742段、第一駐車場から約260段）。アクセス：太郎坊宮前駅から徒歩約20分", "url": "https://tarobo.or.jp/", "checked": CHECKED},
    {"what": "永源寺 よくある質問：参拝時間 9:00〜16:00（11月は観楓期のため変更）、参拝志納料 大人600円・中学生200円・小学生以下無料。紅葉は11月上旬〜下旬、中旬がピーク", "url": "https://eigenji-t.jp/contact/", "checked": CHECKED},
    {"what": "永源寺 お知らせ：山門・法堂の特別拝観 10:00・11:30・14:00、1,500円（入山志納料含）、問い合わせは永源寺前観光案内所 0748-27-2020（11/18）。ライトアップは20時まで（11/20金・11/21土）。11/21のお知らせにライトアップのチラシの画像（2026年 11月14日（土）〜11月28日（土）、月〜木曜日17:00〜18:30（閉門）、金〜日曜日17:00〜20:00（閉門）、大人600円・中学生200円）。11/23（月・祝）は祝日のため20時閉門。11/23のお知らせに「ライトアップ期間は29日（土）まで」とあるが、29日は日曜で、チラシ・観光協会の案内は28日（土）まで、11/29・30は8:00〜17:00なので28日にそろえた。食事処「音無瀬」とキッチンカー「ブランブル」が11/14に開店、うどん・そば・ぜんざい・甘酒・パフェ・クレープ（11/15、営業時間の記載なし）。参拝志納料 大人600円・中学生200円・団体500円・小学生以下無料（2026年4月2日のお知らせ）", "url": "https://eigenji-t.jp/haikan/", "checked": RECHECKED},
    {"what": "東近江市観光協会「大本山永源寺 山門と法堂雲龍図 特別拝観2026」：特別拝観 令和8年11月7日（土）〜11月23日（月・祝）、10:00〜・11:30〜・14:00〜、集合は永源寺観光案内所（永源寺高野町52、0748-27-2020、予約は電話）、1,500円（参拝志納料含む・お茶席100円割引付き）。含空院庭園と標月亭お茶席 11月7日〜30日 9:00〜17:00（入場16:45まで）一席700円（参拝志納料は別）。ライトアップ 11月14日（土）〜28日（土）17:00〜20:00（閉門）、月〜木は18:30閉門。チラシ（裏面）の参拝受付：①11/1〜13 8:00〜17:00（閉門）②11/14〜28 8:00〜20:00（閉門。月〜木は18:30閉門）③11/29〜30 8:00〜17:00（閉門）", "url": EIGENJI_AUTUMN, "checked": RECHECKED},
    {"what": "同じページのチラシ画像（裏面。参拝受付の時間・参拝志納料 大人600円）", "url": "https://www.higashiomi.net/dcms_media/image/sanmontokubetu26-2.jpg", "checked": RECHECKED},
    {"what": "近江鉄道線でICOCAなどが使える（2026年3月1日から、全線）", "url": "https://www.ohmitetudo.co.jp/railway/icoca-2025/", "checked": CHECKED},
    {"what": "ティファニー（近江八幡）：ディナー17:00〜20:00（L.O.）、火曜休み、駅の北口から歩いて3分（近江八幡マップのデータ、2026-11-20確認）", "url": "../omihachiman/", "checked": "2026-11-20"},
    yt("近江八幡", "京都", "1125", "2110", "21:13新快速→21:48（680円）"),
    yt("近江八幡", "京都", "1128", "2110", "21:13新快速→21:48（680円）"),
]
SOURCES_B = [
    {"what": "湖東三山 紅葉シャトルバス 2026：11月19日〜29日。彦根駅西口4番のりば。往路 彦根9:00→西明寺9:32（1便は西明寺まで）、10:00→西明寺10:32→金剛輪寺10:47（2便は金剛輪寺まで）、11:00→11:32→11:47→クレフィール湖東11:55→読合堂11:59→百済寺12:10、12:00→12:32→12:47→12:55→12:59→13:10。復路 百済寺13:10・14:10・15:20・16:20→金剛輪寺13:33・14:33・15:43・16:43→西明寺13:43・14:43・15:53・16:53→彦根駅14:20・15:20・16:30・17:30。運賃 彦根-西明寺700・西明寺-金剛輪寺200・金剛輪寺-百済寺300・西明寺-百済寺500・金剛輪寺-彦根800・百済寺-彦根1,000円。もみじきっぷ 大人2,500円（当日、彦根駅西口かバス車内、現金）。予約は彦根駅発だけ・もみじきっぷ購入者だけ、電話（湖国バス彦根営業所0749-25-2501、9:00〜18:00）は前日まで、Webは2日前まで。予約者優先、座れないことあり", "url": "https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/", "checked": CHECKED},
    {"what": "湖東三山の2026年のチラシ（近江鉄道のページのPDF）：西明寺 入山料800円・8:30〜16:30（閉門17:00）、宝冠毘沙門天 初公開 10月1日〜12月13日、本堂後陣仏像群特別拝観 11/14〜30。金剛輪寺 800円・8:30〜16:30（閉門17:00）、秘仏大黒天 10月31日〜12月13日、三重塔大日如来開扉 11/14〜29（好天時のみ）。百済寺 600円。千成亭ぎゅ〜じあむ 10:00〜16:00・月火定休（11月は無休）。京阪バス定期観光（京都駅八条口発、湖東三山・永源寺・昼食、11/14〜12/6 大人14,000円、12/7〜12/13 9,900円）", "url": "https://www.ohmitetudo.co.jp/file/bus-icoico-event-kotosanzanshuttlebus2026-chirashi.pdf.pdf", "checked": CHECKED},
    yt("京都", "彦根", "1125", "0825", "8:37新快速 長浜行→9:31（1,170円）"),
    yt("京都", "彦根", "1128", "0825", "8:30新快速 米原行→9:20（1,170円）"),
    yt("京都", "彦根", "1123", "0825", "祝日も8:30→9:20（1,170円）"),
    yt("京都", "彦根", "1125", "0931", "9:34普通→10:41（1,170円）"),
    yt("京都", "彦根", "1128", "0930", "9:37普通→10:39（1,170円）"),
    yt("三条京阪", "京都", "1125", "0800", "8:05→8:19（260円）"),
    yt("三条京阪", "京都", "1128", "0752", "7:59→8:13（260円）"),
    yt("三条京阪", "彦根", "1125", "0818", "8:22→山科8:42→9:31（1,250円）"),
    yt("三条京阪", "彦根", "1128", "0806", "8:10→山科8:36→9:20（1,250円）"),
    yt("彦根", "京都", "1125", "1740", "17:52新快速→18:42（1,170円）"),
    yt("彦根", "京都", "1128", "1740", "17:52新快速→18:42（1,170円）"),
    yt("彦根", "安土", "1125", "1640", "17:04→17:20、18:02→18:19（330円）"),
    yt("彦根", "安土", "1128", "1640", "17:04→17:20、18:02→18:19（330円）"),
    yt("百済寺本坊前", "京都", "1125", "1750", "17:54ちょこっとバス→近江八幡19:06新快速→19:42（1,340円）"),
    yt("百済寺本坊前", "京都", "1128", "1750", "17:54→19:42（1,340円）"),
    yt("百済寺本坊前", "京都", "1130", "1750", "17:54→19:42（1,340円）"),
    yt("京都", "河瀬", "1130", "1051", "9:34普通→10:34（990円）", 4),
    yt("京都", "河瀬", "1205", "1051", "9:37普通→10:32（990円）", 4),
    yt("稲枝", "京都", "1130", "1555", "16:13→17:06、17:13→18:06（990円）"),
    yt("稲枝", "京都", "1205", "1555", "16:13→17:06、17:13→18:06（990円）"),
    yt("稲枝", "京都", "1130", "1756", "18:11→19:06（990円）"),
    yt("稲枝", "京都", "1205", "1756", "18:11→19:06（990円）"),
    yt("稲枝", "安土", "1130", "1656", "17:13→17:20（200円）"),
    yt("稲枝", "安土", "1205", "1656", "17:13→17:20（200円）"),
    {"what": "湖東三山シャトルバスの運賃表の画像（2026年度のページに掲載）：金剛輪寺-彦根駅800円、西明寺-百済寺500円", "url": "https://www.ohmitetudo.co.jp/bus/icoico/event/image/bus-icoico-kotousanzanshuttlebus2025-untin.png", "checked": CHECKED},
    {"what": "西明寺 拝観のご案内：8:30〜17:00（最終受付は閉門30分前）、料金表 大人800円・中人500円・小人300円（令和5年4月より変更）、本堂後陣仏像群特別拝観料1,000円、境内での持ち込み飲食禁止", "url": "https://saimyouji.com/information/", "checked": CHECKED},
    {"what": "愛のりタクシーこうら 時刻表（彦根市、2026年4月1日改正）：河瀬駅東口 毎時51分→西明寺前 08分（西明寺へは15:51発まで）、800円。西明寺前 毎時12分→河瀬駅東口 29分（16:12発まで）。現金か回数券のみ。予約 0749-22-1111、1週間前〜1時間前（9時までの便は前日21時まで）。12/29〜1/3運休。料金表（区間A〜F）：河瀬駅東口（B）→西明寺前（F）800円。2人以上でまとめて予約し同じ停留所から乗ると半額（ふく割）", "url": "https://www.city.hikone.lg.jp/material/files/group/128/2026_koura_0319fix.pdf", "checked": RECHECKED},
    {"what": "愛のりタクシーあいしょう 金剛輪寺線 時刻表（彦根市、2026年4月のページ）：西明寺前12:56→金剛輪寺13:03（料金表：西明寺前・金剛輪寺ともC区間、C〜C 400円）。金剛輪寺14:42→稲枝駅15:54、15:42→16:54、16:42→17:54（稲枝駅はA区間、A〜C 800円）。同乗者で多少前後。毎日運行、12/29〜1/3運休。支払いは現金と共通回数券のみ（カード・ICカード不可）", "url": "https://www.city.hikone.lg.jp/material/files/group/128/2026_aisyo_0319fix.pdf", "checked": RECHECKED},
    {"what": "西明寺のアクセス：愛のりタクシー 河瀬駅東口から800円、西明寺→金剛輪寺の発時刻（毎時56分）", "url": "https://saimyouji.com/access/", "checked": CHECKED},
    {"what": "百済寺の交通案内：八日市駅からタクシー約10分、ちょこっとバス約30分", "url": "http://hyakusaiji.jp/info_access/", "checked": CHECKED},
    {"what": "金剛輪寺：8:30〜16:30（17:00閉山）、大人800円・中学生300円・小学生200円。華楽坊は5名以上の予約から。愛のりタクシー 稲枝駅→金剛輪寺800円、金剛輪寺発10:42〜16:42 毎時42分", "url": "https://kongourinji.jp/access", "checked": CHECKED},
    {"what": "百済寺：8:30〜17:00（受付16:30まで）、大人600円・中学生300円・小学生200円。令和8年秋季ライトアップ 11月14日〜30日、平日17時〜最終受付19時・閉門19時30分、土日祝17時〜最終受付20時30分・閉門21時", "url": "http://hyakusaiji.jp/", "checked": CHECKED},
    {"what": "近江牛一筋＠千成亭ぎゅ〜じあむ：甲良町池寺1-5（西明寺門前）、営業時間11:00〜15:00、定休日 月曜・火曜", "url": "https://gyuseum.jp/", "checked": CHECKED},
    {"what": "千成亭ぎゅ〜じあむ 施設のご案内：グルメコート・レストラン 11:00〜15:00（LO 14:30）、物産館 11:00〜15:00、定休日 毎週月・火曜日（紅葉シーズンを除く）。お知らせに2026年11月の営業の記載はなし（2024年11月7日に「11月は休まず営業」の記事）", "url": "https://gyuseum.jp/guidance/", "checked": RECHECKED},
]
SOURCES_C = [
    yt("京都", "河瀬", "1130", "1051", "9:34普通→10:34（990円）", 4),
    yt("京都", "河瀬", "1205", "1051", "9:37普通→10:32（990円）", 4),
    yt("京都", "河瀬", "1206", "1051", "9:37普通→10:32（990円）", 4),
    yt("京都", "河瀬", "1228", "1051", "9:34普通→10:34（990円）", 4),
    yt("三条京阪", "京都", "1130", "0903", "9:09→9:25（260円）"),
    yt("三条京阪", "京都", "1205", "0903", "9:07→9:21（260円）"),
    yt("稲枝", "京都", "1130", "1555", "16:13→17:06、17:13→18:06（990円）"),
    yt("稲枝", "京都", "1205", "1555", "16:13→17:06、17:13→18:06（990円）"),
    yt("稲枝", "京都", "1228", "1555", "16:13→17:06、17:13→18:06（990円）"),
    yt("稲枝", "京都", "1130", "1756", "18:11→19:06（990円）"),
    yt("稲枝", "京都", "1205", "1756", "18:11→19:06（990円）"),
    yt("京都", "稲枝", "1130", "1051", "9:34→10:31（990円）", 4),
    yt("京都", "稲枝", "1205", "1051", "9:37→10:29（990円）", 4),
    yt("河瀬", "京都", "1130", "1430", "14:41→15:37（990円）"),
    yt("河瀬", "京都", "1205", "1430", "14:41→15:37（990円）"),
    yt("河瀬", "安土", "1130", "1630", "17:10→17:20（240円）"),
    yt("河瀬", "安土", "1205", "1630", "17:10→17:20（240円）"),
    yt("稲枝", "安土", "1130", "1656", "17:13→17:20（200円）"),
    yt("稲枝", "安土", "1205", "1656", "17:13→17:20（200円）"),
    yt("安土", "京都", "1130", "1845", "18:58→近江八幡19:06新快速→19:42（770円）"),
    yt("安土", "京都", "1205", "1845", "18:58→近江八幡19:06新快速→19:42（770円）"),
    yt("京都", "百済寺本坊前", "1130", "1255", "13:00→近江八幡13:34/13:44→八日市14:04、バス14:18→14:47（1,340円）"),
    yt("京都", "百済寺本坊前", "1205", "1255", "13:00→14:47（1,340円）"),
    yt("京都", "百済寺本坊前", "1228", "1255", "13:00→14:47（1,340円）"),
    yt("百済寺本坊前", "京都", "1205", "1700", "17:54→19:42（1,340円）"),
    yt("百済寺本坊前", "京都", "1228", "1700", "17:54→19:42（1,340円）"),
] + [x for x in SOURCES_B if "transit.yahoo.co.jp" not in x["url"] and "シャトルバス" not in x["what"]]
SOURCES_W = [
    yt("京都", "太郎坊宮前", "1207", "0955", "10:00→近江八幡10:35/10:42→10:57（1,070円）"),
    yt("京都", "太郎坊宮前", "1212", "0955", "10:00→近江八幡10:34/10:42→10:57（1,070円）"),
    yt("京都", "太郎坊宮前", "1213", "0955", "10:00→10:57（1,070円）"),
    yt("三条京阪", "京都", "1207", "0929", "9:30→9:47（260円）"),
    yt("三条京阪", "京都", "1212", "0931", "9:32→9:45（260円）"),
    yt("三条京阪", "近江八幡", "1207", "0940", "9:44→山科10:06→10:35（850円）。びわ湖浜大津行は980円"),
    yt("三条京阪", "近江八幡", "1212", "0940", "9:43→山科10:05→10:34（850円）"),
    yt("太郎坊宮前", "八日市", "1207", "1238", "12:41→12:45、12:59→13:04（160円）"),
    yt("太郎坊宮前", "八日市", "1212", "1238", "12:41→12:45、12:59→13:04（160円）"),
    yt("八日市", EIGENJI_STOP, "1207", "1300", "バス13:15→13:44（670円）"),
    yt("八日市", EIGENJI_STOP, "1212", "1300", "バス13:15→13:43（670円）"),
    yt("八日市", EIGENJI_STOP, "1213", "1300", "バス13:15→13:43（670円）"),
    yt("八日市", EIGENJI_STOP, "1230", "1300", "バス13:15→13:43（670円）。年末は土日祝の時刻"),
    yt("京都", EIGENJI_STOP, "1207", "0955", "10:00→八日市駅11:15のバス→11:44（1,810円）"),
    yt("京都", EIGENJI_STOP, "1212", "0955", "10:00→八日市駅11:15のバス→11:43（1,810円）"),
    yt(EIGENJI_STOP, "京都", "1207", "1550", "16:24→16:59、八日市17:09→近江八幡17:28/17:36→18:12（1,810円）。15:56発でも18:12"),
    yt(EIGENJI_STOP, "京都", "1212", "1550", "16:25→17:00、八日市17:09→近江八幡17:28/17:36→18:12（1,810円）。15:56発でも18:12"),
    yt(EIGENJI_STOP, "京都", "1213", "1550", "16:25→18:12（1,810円）"),
    yt(EIGENJI_STOP, "京都", "1230", "1550", "16:25→18:12（1,810円）。年末は土日祝の時刻"),
    yt(EIGENJI_STOP, "京都", "1231", "1550", "16:25→18:12（1,810円）"),
    yt(EIGENJI_STOP, "京都", "0101", "1550", "16:25→18:12（1,810円）", year=2027),
    yt(EIGENJI_STOP, "京都", "0113", "1550", "16:24→18:12（1,810円）", year=2027),
    yt("近江八幡", "京都", "1207", "1730", "17:36新快速→18:12（680円）"),
    yt("近江八幡", "京都", "1212", "1730", "17:36新快速→18:12（680円）"),
    yt("京都", "三条京阪", "1207", "1812", "地下鉄18:13→18:28（260円）"),
    yt("京都", "三条京阪", "1212", "1812", "地下鉄18:15→18:28（260円）"),
] + [x for x in SOURCES_A if "transit.yahoo.co.jp" not in x["url"] and "ティファニー" not in x["what"]]


def build(defs, plan_fn, course, out, sections, note, sources, focus=None, common=None):
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
            "plan": plan_fn(NO), "sources": (SOURCES_COMMON if common is None else common) + sources, "spots": spots}
    if focus:
        data["focus"] = focus(NO)
    json.dump(data, open(f"{R}/data/routes/{out}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


build(A, A_PLAN, "eigenji", "higashiomi.json",
      lambda NO: [{"first": 1, "last": NO["taroubou"], "area": T("近江八幡・太郎坊宮", "Omi-Hachiman & Taroubou-gu"), "title": T("742段の石段の上へ", "Up 742 stone steps")},
                  {"first": NO["eigenji"], "last": NO["eigenji"], "area": T("永源寺", "Eigenji"), "title": T("渓谷のもみじと遅めのお昼", "Valley maples and a late lunch")},
                  {"first": NO["kyorinbo"], "last": NO["kyorinbo"], "area": T("安土・教林坊", "Azuchi & Kyorinbo"), "title": T("竹林と庭のライトアップ", "Bamboo and garden by lantern light")}],
      "京都から日帰り 湖東の紅葉、コース「太郎坊宮・永源寺」（京都駅10:00発）。京都駅10:00→近江八幡→近江鉄道で太郎坊宮前10:57→太郎坊宮→八日市13:15のバスで永源寺（お昼）→16:24のバス→近江鉄道・JRで安土17:44→タクシーで教林坊のライトアップ→安土19:28→京都駅20:12。"
      "写真は Toshi の写真ライブラリ（太郎坊宮は2024年12月1日、永源寺と教林坊は2026年11月17日、近江八幡駅は omihachiman の流用）。このファイルは scripts/build_higashiomi_data.py で作る。",
      SOURCES_A)
build(B, B_PLAN, "sanzan", "higashiomi-sanzan.json",
      lambda NO: [{"first": 1, "last": NO["saimyoji"], "area": T("彦根・西明寺", "Hikone & Saimyoji"), "title": T("10:00のシャトルバスで国宝の本堂へ", "The 10:00 shuttle to a National Treasure hall")},
                  {"first": NO["hyakusaiji"], "last": NO["kongorinji"], "area": T("百済寺・金剛輪寺", "Hyakusaiji & Kongorinji"), "title": T("苔の参道と血染めのもみじ", "Mossy approach and blood-red maples")},
                  {"first": NO["kyorinbo"], "last": NO["kyorinbo"], "area": T("寄り道：教林坊", "Option: Kyorinbo"), "title": T("帰りに夜のライトアップ", "An evening illumination on the way home")}],
      "京都から日帰り 湖東の紅葉、コース「湖東三山」（8時台に出発。紅葉シャトルバスの運行日 2026年11月19日〜29日向け）。京都駅8:37（土日祝8:30）→彦根9:31（9:20）→シャトルバス10:00→西明寺10:32（門前の千成亭ぎゅ〜じあむでお昼）→12:32のバスで百済寺13:10→15:20のバスで金剛輪寺15:43→16:43のバスで彦根17:30→17:52の新快速で京都駅18:42。11/30からは注意書きが京都駅9:34（9:37）→河瀬→愛のりタクシー→稲枝→京都駅の案内になる。教林坊は寄り道（最初は外す）。"
      "西明寺と金剛輪寺の写真は Wikimedia Commons（photos の要素が {file, credit}）、百済寺は2025年8月12日の Toshi の写真。1番の写真は近江八幡駅（途中で通る駅）。このファイルは scripts/build_higashiomi_data.py で作る。",
      SOURCES_B)
C_NOTE = ("京都から日帰り 湖東の紅葉、コース「湖東三山」の11月30日から（紅葉シャトルバスが終わったあと。scripts/sync_higashiomi.py の日付で読み分ける）。"
          "京都駅9:34（土日祝9:37）→河瀬10:34（10:32）→愛のりタクシー10:51→西明寺11:08（お昼）→12:56→金剛輪寺13:03→14:42→稲枝15:54→16:13の電車で京都駅17:06。"
          "番号の順はシャトルバスの日と違う（保存キーに -off が付く）。百済寺は別の日に。")
build(C, C_PLAN, "sanzan", "higashiomi-sanzan-taxi.json", C_SECTIONS,
      C_NOTE + "12月6日までの分で、教林坊の夜が寄り道に入る。このファイルは scripts/build_higashiomi_data.py で作る。", SOURCES_C)
build([x for x in C if x["id"] != "kyorinbo"], C_PLAN, "sanzan", "higashiomi-sanzan-winter.json", C_SECTIONS,
      C_NOTE + "12月7日からの分で、教林坊はない（ライトアップが終わり、昼の公開16:30までにも着けない）。このファイルは scripts/build_higashiomi_data.py で作る。", SOURCES_C)
build(W, W_PLAN, "eigenji", "higashiomi-eigenji-winter.json",
      lambda NO: [{"first": 1, "last": NO["taroubou"], "area": T("近江八幡・太郎坊宮", "Omi-Hachiman & Taroubou-gu"), "title": T("742段の石段の上へ", "Up 742 stone steps")},
                  {"first": NO["eigenji"], "last": NO["eigenji"], "area": T("永源寺", "Eigenji"), "title": T("渓谷の禅寺で16:00まで", "A valley Zen temple until 16:00")}],
      "京都から日帰り 湖東の紅葉、コース「太郎坊宮・永源寺」の12月7日から（教林坊のライトアップが終わったあと。scripts/sync_higashiomi.py の WINTER_FROM で読み分ける）。"
      "京都駅10:00→太郎坊宮前10:57→太郎坊宮→八日市13:15のバスで永源寺（お昼は持参）→16:24（土日祝16:25）のバス→近江八幡17:36の新快速→京都駅18:12→夜は街なか。"
      "番号1〜4は12月6日までと同じ。このファイルは scripts/build_higashiomi_data.py で作る。",
      SOURCES_W, common=[])
