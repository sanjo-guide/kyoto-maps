#!/usr/bin/env python3
"""京都から日帰り 湖東の紅葉（太郎坊宮・永源寺・百済寺・教林坊）のデータ（data/routes/higashiomi.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/higashiomi/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/higashiomi"
OUT = f"{R}/data/routes/higashiomi.json"
CHECKED = "2026-11-20"
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


def info(rows, tip=None, verified=True):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


NONE = {"rows": [], "cash": False, "tip": None, "checked": CHECKED}
JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
OHMI_BUS = link("timetable", "近江鉄道バス 永源寺へのアクセス", "Ohmi Railway bus to Eigenji (Japanese)", "https://www.ohmitetudo.co.jp/bus/access/eigenji/")
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。バスは本数が少ないので、乗る前にもう一度確かめてください。",
              "Times and fares checked on a route planner (Saturday timetable, November 2026). Buses are infrequent, so check again before you travel.")

S = [
    dict(id="omihachimaneki", name=T("JR近江八幡駅（乗り換え）", "JR Omi-Hachiman Station (change)"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都からJRの新快速で約35分。ここで近江鉄道の八日市線に乗り換えます。",
                 "About 35 minutes from Kyoto by JR Special Rapid. Change here to the Ohmi Railway Yokaichi Line."),
         lat=35.12280, lng=136.10280,
         text=T("JR近江八幡駅（おうみはちまんえき）\n\n京都からJR琵琶湖線の新快速で約35分（680円）。同じ駅の中で、近江鉄道の八日市線（ようかいちせん）に乗り換えます。\n\n"
                "京都7:16発に乗ると、近江八幡で乗り換えて、太郎坊宮前に8:27に着きます（京都から1,070円）。近江鉄道は1時間に2本ほどです。\n\n"
                "この先は電車とバスの本数が少ないので、永源寺から百済寺、教林坊の行き帰りはタクシーを使うのがおすすめです。\n\nおすすめ出発時間：京都7:16",
                "JR Omi-Hachiman Station\n\nAbout 35 minutes from Kyoto on the JR Biwako Line Special Rapid (¥680). Change inside the station to the Ohmi Railway Yokaichi Line.\n\n"
                "Leave Kyoto at 7:16 and, changing here, you reach Taroubougu-mae at 8:27 (¥1,070 from Kyoto). The Ohmi Railway runs about twice an hour.\n\n"
                "Trains and buses are sparse beyond here, so taxis are the easy way from Eigenji to Hyakusaiji, and to and from Kyorinbo.\n\nRecommended departure: Kyoto 7:16"),
         gmaps=[gm("近江八幡駅", "Omi-Hachiman Station", 35.12280, 136.10280, "近江八幡駅")],
         links=[JR],
         info=info([row("train", "京都7:16発（JR）→ 近江八幡（近江鉄道に乗り換え）→ 太郎坊宮前8:27着", "Kyoto 7:16 (JR) → Omi-Hachiman (change to Ohmi Railway) → Taroubougu-mae 8:27"),
                    row("fee", "京都→近江八幡 680円、京都→太郎坊宮前 1,070円", "Kyoto → Omi-Hachiman ¥680; Kyoto → Taroubougu-mae ¥1,070")],
                   tip=TRAIN_TIP)),
    dict(id="taroubouekimae", name=T("近江鉄道 太郎坊宮前駅", "Ohmi Railway Taroubougu-mae Station"), kind=T("駅", "Station"),
         blurb=T("駅を出ると、正面にとがった形の太郎坊山（赤神山）。鳥居をくぐって、山のふもとまで歩きます。",
                 "Out of the station, the pointed peak of Mt. Taroubou (Akagami-yama) is right ahead. Walk under the torii to the foot of the mountain."),
         lat=35.10853, lng=136.18378,
         text=T("近江鉄道 太郎坊宮前駅（たろうぼうぐうまええき）\n\n近江八幡から近江鉄道八日市線で15分（390円）。駅から太郎坊宮までは歩いて約20分です。\n\n"
                "田んぼの向こうに、岩がむき出しになったとがった山が見えてきます。これが太郎坊宮のある赤神山（あかがみやま）。大きな鳥居をくぐって、参道を山の方へ進みます。\n\nおすすめ到着時間：8:27",
                "Ohmi Railway Taroubougu-mae Station\n\n15 minutes from Omi-Hachiman on the Ohmi Railway Yokaichi Line (¥390). The shrine is about a 20-minute walk.\n\n"
                "Across the rice fields rises a sharp, rocky peak: Mt. Akagami, home of Taroubou-gu. Pass under the big torii and follow the approach towards the mountain.\n\nRecommended arrival: 8:27"),
         gmaps=[gm("太郎坊宮前駅", "Taroubougu-mae Station", 35.10853, 136.18378, "太郎坊宮前駅")],
         links=[JR],
         info=info([row("train", "近江八幡 → 太郎坊宮前 15分（1時間に2本ほど）", "Omi-Hachiman → Taroubougu-mae 15 min (about 2 trains an hour)"),
                    row("fee", "近江八幡→太郎坊宮前 390円", "Omi-Hachiman → Taroubougu-mae ¥390")],
                   tip=TRAIN_TIP)),
    dict(id="taroubou", name=T("太郎坊宮（阿賀神社）", "Taroubou-gu (Aga Shrine)"), kind=T("神社", "Shrine"),
         blurb=T("742段の石段を登った先に、紅葉と近江の平野を見渡す本殿。大きな岩が割れた「夫婦岩」の間を通ってお参りします。",
                 "Climb 742 stone steps to a main hall above the autumn leaves and the Omi plain. You reach it by squeezing between the split “Meoto-iwa” rocks."),
         lat=35.11819, lng=136.18244,
         text=T("太郎坊宮（たろうぼうぐう）阿賀神社（あがじんじゃ）\n\n赤神山の中腹にある、勝運の神様の神社です。ふもとから本殿までは742段の石段。"
                "途中には赤い鳥居が続く参道や、木の格子に囲まれた長い石段があり、紅葉の時期は真っ赤なもみじのトンネルになります。\n\n"
                "本殿の手前には、大きな岩が二つに割れた「夫婦岩（めおといわ）」。すき間を通ってお参りします。本殿の前からは、八日市の町と近江の平野がずっと遠くまで見渡せます。\n\n"
                "石段は急な所もあるので、歩きやすい靴で。境内を一周すると50分ほどです。参拝は自由で、拝観料はいりません。\n\nおすすめ訪問時間：8:50〜10:35",
                "Taroubou-gu (Aga Shrine)\n\nA shrine to the god of victory, halfway up Mt. Akagami. From the foot of the mountain to the main hall is 742 stone steps. "
                "On the way are an approach lined with red torii and a long stairway enclosed in wooden lattice; in autumn it becomes a tunnel of red maples.\n\n"
                "Just below the main hall are the Meoto-iwa, a huge boulder split in two. You pass through the gap to pray. From the hall you can see over Yokaichi and far across the Omi plain.\n\n"
                "Some steps are steep, so wear good shoes. A loop of the grounds takes about 50 minutes. Entry is free at any time.\n\nRecommended visit time: 8:50–10:35"),
         gmaps=[gm("太郎坊宮", "Taroubou-gu", 35.11819, 136.18244, "太郎坊宮 阿賀神社")],
         links=[link("official", "太郎坊宮 公式サイト", "Taroubou-gu (official, Japanese)", "https://tarobo.or.jp/")],
         info=info([row("hours", "参拝は自由（閉門なし）。社務所の受付 9:00〜17:00", "Open at all times. Shrine office 9:00–17:00"),
                    row("fee", "無料", "Free")],
                   tip=T("ふもとから本殿まで742段。車なら中腹の駐車場から約260段です（公式サイトで確認）。", "742 steps from the foot of the mountain; about 260 from the mid-slope car park (checked on the official website)."))),
    dict(id="eigenji", name=T("永源寺", "Eigenji Temple"), kind=T("寺", "Temple"),
         blurb=T("愛知川の渓谷にある禅寺。山門と方丈のまわりが一面のもみじに染まります。秋は夕方からライトアップも。",
                 "A Zen temple in the Echigawa valley. Maples blaze around the great gate and the abbot’s hall, and in autumn they’re lit up after dark."),
         lat=35.08058, lng=136.31999,
         text=T("永源寺（えいげんじ）\n\n鈴鹿の山あいを流れる愛知川（えちがわ）のほとりにある、臨済宗永源寺派の大本山です。旦度橋（たんどばし）を渡り、石段を上ると大きな山門。"
                "その先の法堂や方丈のまわりを、たくさんのもみじが囲んでいます。紅葉は11月上旬から下旬で、中旬が見ごろです。\n\n"
                "八日市駅から近江鉄道バスで約30分（670円）、「永源寺前」で降ります。太郎坊宮前10:57発の電車で八日市へ戻り、11:15発のバスに乗ると11:43に着きます。"
                "門前には茶店やおみやげの店が並び、名物の永源寺こんにゃくも売っています。お昼はここで。\n\n"
                "2026年の秋のライトアップは11月28日（土）まで。夕暮れの山門が、もみじと一緒に照らし出されます。\n\n"
                "永源寺から百済寺へはバスでつながっていないので、タクシーで向かいましょう。\n\nおすすめ訪問時間：11:45〜14:20",
                "Eigenji Temple\n\nHead temple of the Eigenji school of Rinzai Zen, on the Echigawa river in the Suzuka hills. Cross the Tando bridge and climb to the great gate; "
                "beyond, the lecture hall and abbot’s quarters are wrapped in maples. The leaves turn from early to late November, best in mid-November.\n\n"
                "From Yokaichi Station, take the Ohmi Railway bus (about 30 min, ¥670) to “Eigenji-mae”. Take the 10:57 train from Taroubougu-mae back to Yokaichi and the 11:15 bus, and you arrive at 11:43. "
                "Tea houses and souvenir shops line the approach, selling the local Eigenji konnyaku. Have lunch here.\n\n"
                "In autumn 2026 the temple is lit up until Saturday 28 November: the gate glows with the maples at dusk.\n\n"
                "No bus links Eigenji with Hyakusaiji, so take a taxi.\n\nRecommended visit time: 11:45–14:20"),
         gmaps=[gm("永源寺", "Eigenji", 35.08058, 136.31999, "永源寺 東近江市")],
         links=[link("official", "永源寺 公式サイト", "Eigenji (official, Japanese)", "https://eigenji-t.jp/"), OHMI_BUS],
         info=info([row("hours", "9:00〜16:00（11月は紅葉の時期のため時間が変わります。東近江市観光協会の案内では8:00〜17:00）",
                        "9:00–16:00 (hours change in November for the autumn leaves; the Higashiomi tourism association lists 8:00–17:00)"),
                    row("hours", "2026年秋のライトアップ：11月14日〜28日。月〜木 17:00〜18:30、金〜日 17:00〜20:00（閉門）",
                        "Autumn 2026 illumination: 14–28 Nov. Mon–Thu 17:00–18:30, Fri–Sun 17:00–20:00 (gates close)", until="2026-11-28"),
                    row("fee", "参拝志納料 大人600円、中学生200円（2026年4月から）", "Admission ¥600 adults, ¥200 junior high (from April 2026)"),
                    row("train", "八日市駅 → 永源寺前 近江鉄道バス 約30分・670円（1時間に1〜2本）", "Yokaichi Sta. → Eigenji-mae, Ohmi Railway bus, about 30 min, ¥670 (1–2 an hour)")],
                   tip=T("永源寺→百済寺はタクシーで（永源寺タクシー 0748-27-1151、東近江市観光協会の案内より）。所要時間と料金は確認できていません。",
                         "Take a taxi from Eigenji to Hyakusaiji (Eigenji Taxi 0748-27-1151, listed by the Higashiomi tourism association). Journey time and fare not confirmed."))),
    dict(id="hyakusaiji", name=T("百済寺（湖東三山）", "Hyakusaiji Temple (Koto Sanzan)"), kind=T("寺", "Temple"),
         blurb=T("苔むした石垣と杉の参道を上る、湖東三山のひとつ。本坊の庭からは、遠く琵琶湖の方まで見渡せます。",
                 "One of the three great temples east of the lake: climb a cedar-lined approach between mossy stone walls. The garden looks out towards Lake Biwa."),
         lat=35.12683, lng=136.29151,
         text=T("百済寺（ひゃくさいじ）\n\n湖東三山（ことうさんざん）のひとつで、聖徳太子が百済の人のために建てたと伝わる古いお寺です。"
                "本坊・喜見院（きけんいん）の池泉回遊式の庭園と、その上の遠望台からの眺めが見どころ。苔むした石垣にはさまれた参道（千年菩提路）を上り、大きなわらじが下がる仁王門をくぐって本堂へ向かいます。\n\n"
                "写真は2025年8月の新緑のころのもの。秋はこの参道ともみじが赤く染まり、2026年は11月30日までライトアップもあります。\n\n"
                "八日市駅からは「ちょこっとバス」（1日4便）で約30分。永源寺からはタクシーで。帰りは、寺から歩いて約12分の「百済寺本町」から17:16発のバスに乗ると、能登川駅で乗り換えて安土駅に18:19に着きます（980円）。\n\nおすすめ訪問時間：14:40〜16:55",
                "Hyakusaiji Temple\n\nOne of the Koto Sanzan, the three temples east of the lake, said to have been founded by Prince Shotoku for people from the kingdom of Baekje. "
                "Highlights are the pond garden of the main residence, Kikenin, and the view from the lookout above it. Climb the approach between mossy stone walls, pass the Nio gate hung with giant straw sandals, and go up to the main hall.\n\n"
                "The photos are from August 2025, in fresh summer green. In autumn the approach turns red with maples, and in 2026 there is an evening illumination until 30 November.\n\n"
                "From Yokaichi Station the “Chokotto Bus” (4 a day) takes about 30 minutes; from Eigenji, take a taxi. To leave, walk about 12 minutes to “Hyakusaiji-honmachi” and take the 17:16 bus; changing at Notogawa, you reach Azuchi at 18:19 (¥980).\n\nRecommended visit time: 14:40–16:55"),
         gmaps=[gm("百済寺", "Hyakusaiji", 35.12683, 136.29151, "百済寺 東近江市")],
         links=[link("official", "百済寺 公式サイト", "Hyakusaiji (official, Japanese)", "http://hyakusaiji.jp/"), JR],
         info=info([row("hours", "8:30〜17:00（受付は16:30まで）", "8:30–17:00 (last entry 16:30)"),
                    row("hours", "2026年秋のライトアップ：11月14日〜30日 17:00から。平日は受付19:00まで、土日祝は受付20:30まで",
                        "Autumn 2026 illumination: 14–30 Nov from 17:00. Last entry 19:00 on weekdays, 20:30 at weekends and holidays", until="2026-11-30"),
                    row("fee", "大人600円、中学生300円、小学生200円", "¥600 adults, ¥300 junior high, ¥200 elementary"),
                    row("train", "百済寺本町17:16発（湖国バス）→ 能登川駅（JRに乗り換え）→ 安土18:19着・980円", "Hyakusaiji-honmachi 17:16 (Kokoku bus) → Notogawa (change to JR) → Azuchi 18:19, ¥980")],
                   tip=TRAIN_TIP)),
    dict(id="kyorinbo", name=T("教林坊", "Kyorinbo"), kind=T("寺", "Temple"),
         blurb=T("春と秋だけ公開される、竹林と石の庭の小さなお寺。秋の夜は、もみじと竹林がやわらかく照らされます。",
                 "A small temple of bamboo groves and stone gardens, open only in spring and autumn. On autumn nights the maples and bamboo are softly lit."),
         lat=35.13898, lng=136.16383,
         text=T("教林坊（きょうりんぼう）\n\n観音正寺のある繖山（きぬがさやま）のふもと、安土町石寺の山あいにある小さなお寺です。ふだんは公開されておらず、春と秋の特別公開のときだけ入れます。"
                "竹林の小道を抜けると、苔と巨石の庭。書院の丸窓や三日月の窓から見る庭も絵のようです。\n\n"
                "写真は2026年11月17日の夜のライトアップ。足もとの灯りに、もみじと竹林が浮かび上がります。2026年のライトアップは12月6日まで、17:30〜19:30（受付は19:00まで）です。\n\n"
                "JR安土駅からタクシーで約10分（約2,500円）。百済寺から17:16のバスに乗ると安土に18:19に着くので、タクシーで向かえばライトアップに間に合います。"
                "帰りもタクシーで安土駅へ。安土19:55発の電車で京都に20:41に着きます（770円）。\n\nおすすめ訪問時間：18:30〜19:15",
                "Kyorinbo\n\nA small temple tucked in the hills of Ishidera, Azuchi, at the foot of Mt. Kinugasa. It is usually closed and opens only for special spring and autumn openings. "
                "A path through bamboo leads to a garden of moss and huge rocks, framed beautifully by the round and crescent-moon windows of the study hall.\n\n"
                "The photos show the evening illumination on 17 November 2026, with the maples and bamboo glowing above the lanterns. In 2026 it runs until 6 December, 17:30–19:30 (last entry 19:00).\n\n"
                "About 10 minutes by taxi from JR Azuchi Station (around ¥2,500). Take the 17:16 bus from Hyakusaiji to reach Azuchi at 18:19, then a taxi, and you’re in time for the illumination. "
                "Take a taxi back to Azuchi; the 19:55 train gets you to Kyoto at 20:41 (¥770).\n\nRecommended visit time: 18:30–19:15"),
         gmaps=[gm("教林坊", "Kyorinbo", 35.13898, 136.16383, "教林坊 近江八幡市安土町石寺")],
         links=[link("official", "教林坊 公式サイト", "Kyorinbo (official, Japanese)", "https://kyourinbo.jimdofree.com/"), JR],
         caution=T("公開は春と秋だけ", "Open in spring and autumn only"),
         notices=[{"from": None, "to": None, "url": "https://kyourinbo.jimdofree.com/",
                   "head": T("公開は春と秋だけ", "Spring and autumn only"),
                   "text": T("ふだんは非公開です。秋は10月の土日祝と11月1日〜12月15日、春は4月25日〜6月30日の土日祝に公開されます（2026年の公式サイトの案内）。",
                             "Usually closed. Open in autumn on October weekends and holidays and daily 1 Nov – 15 Dec, and in spring on weekends and holidays 25 Apr – 30 Jun (official website, 2026).")}],
         info=info([row("hours", "秋の公開：9:30〜16:30（ライトアップの期間は8:30から）", "Autumn opening: 9:30–16:30 (from 8:30 during the illumination)"),
                    row("hours", "2026年のライトアップ：12月6日まで 17:30〜19:30（受付19:00まで）", "2026 illumination: until 6 Dec, 17:30–19:30 (last entry 19:00)", until="2026-12-06"),
                    row("fee", "大人1,000円、小中学生300円（11月1日〜12月15日。10月の土日祝は大人800円）", "¥1,000 adults, ¥300 children (1 Nov – 15 Dec; ¥800 adults on October weekends)"),
                    row("train", "帰り：安土19:55発 → 京都20:41着・770円（安土駅へはタクシーで約10分）", "Return: Azuchi 19:55 → Kyoto 20:41, ¥770 (taxi to Azuchi Station about 10 min)")],
                   tip=T("公開日・時間・料金は教林坊の公式サイト、電車とバスは乗換案内で確認しました。", "Dates, hours and fees checked on the Kyorinbo website; trains and buses on a route planner."))),
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
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
data = {
    "id": "higashiomi",
    "_note": "京都から日帰り 湖東の紅葉ルート（higashiomi/ のページ専用。形は eizan-line.json と同じ）。京都からJRで近江八幡、近江鉄道で太郎坊宮前へ。"
             "太郎坊宮→（近江鉄道・バス）永源寺→（タクシー）百済寺→（バス・JR・タクシー）教林坊のライトアップ→安土駅から京都へ。"
             "写真は Toshi の写真ライブラリから選んだもの（太郎坊宮は2024年12月1日、永源寺と教林坊は2026年11月17日、百済寺は2025年8月12日。"
             "近江八幡駅は omihachiman の写真を流用。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（各寺社の公式サイト、東近江市観光協会、電車とバスは乗換案内）。このファイルは scripts/build_higashiomi_data.py で作る。",
    "sections": [{"first": 1, "last": 3, "day": 0}, {"first": 4, "last": 4, "day": 1}, {"first": 5, "last": 5, "day": 2}, {"first": 6, "last": 6, "day": 3}],
    "plan": {"_note": "「選んで回る」の設定。近江八幡駅はいつも入る。太郎坊宮前駅は太郎坊宮を選ぶと入る。defaultMode: pick で最初から「選んで回る」。",
             "defaultMode": "pick",
             "picks": [NO[k] for k in ("taroubou", "eigenji", "hyakusaiji", "kyorinbo")],
             "auto": {str(NO["omihachimaneki"]): {"always": True}, str(NO["taroubouekimae"]): {"any": [NO["taroubou"]]}},
             "hints": [
                 H("taroubou", {"any": [NO["taroubou"]], "none": [NO["eigenji"], NO["hyakusaiji"], NO["kyorinbo"]]},
                   "帰りは太郎坊宮前駅から近江鉄道で近江八幡へ戻り、JRで京都へ。",
                   "To go home, take the Ohmi Railway from Taroubougu-mae back to Omi-Hachiman and JR to Kyoto."),
                 H("eigenji", {"any": [NO["eigenji"]], "none": [NO["taroubou"]]},
                   "近江八幡から近江鉄道で八日市駅へ（20分・460円）。駅の1番のりばから永源寺行きのバスに乗ります。",
                   "Take the Ohmi Railway from Omi-Hachiman to Yokaichi (20 min, ¥460) and the Eigenji bus from stop 1."),
                 H("eigenji", {"any": [NO["eigenji"]], "none": [NO["hyakusaiji"], NO["kyorinbo"]]},
                   "ここで終わる日は、永源寺前からバスで八日市駅へ（約30分・670円）、近江鉄道で近江八幡、JRで京都へ。",
                   "Finishing here? Bus from Eigenji-mae to Yokaichi (about 30 min, ¥670), the Ohmi Railway to Omi-Hachiman, then JR to Kyoto."),
                 H("hyakusaiji", {"any": [NO["hyakusaiji"]], "none": [NO["eigenji"]]},
                   "永源寺に寄らない日は、八日市駅からちょこっとバス（愛東線・北回り）で「百済寺本坊前」へ。八日市駅発 9:10・10:05・14:18・17:25 の1日4便で、約30分・200円です。",
                   "Not going to Eigenji? Take the Chokotto Bus (Aito Line, northbound) from Yokaichi to “Hyakusaiji Honbo-mae”: 4 a day at 9:10, 10:05, 14:18 and 17:25, about 30 min, ¥200."),
                 H("hyakusaiji", {"any": [NO["hyakusaiji"]], "none": [NO["kyorinbo"]]},
                   "教林坊に行かない日は、ライトアップ（17:00〜）を見て、百済寺本坊前17:54発のちょこっとバスで八日市駅へ。近江鉄道・JRで京都に19:42に着きます（1,340円）。",
                   "Skipping Kyorinbo? Stay for the illumination (from 17:00) and take the 17:54 Chokotto Bus from Hyakusaiji Honbo-mae to Yokaichi; by Ohmi Railway and JR you reach Kyoto at 19:42 (¥1,340)."),
                 H("kyorinbo", {"any": [NO["kyorinbo"]], "none": [NO["hyakusaiji"]]},
                   "百済寺に寄らない日は、近江八幡から京都方面とは逆の電車でJR安土駅へ。安土駅からタクシーで約10分です。昼の公開（16:30まで）に行くなら、安土駅北口からあかこんバスもあります（石寺東出まで約12分・200円、平日と土曜に1日5便。日曜・祝日は走っていないようです）。",
                   "Not going to Hyakusaiji? Take JR from Omi-Hachiman one stop to Azuchi, then a taxi (about 10 min). For the daytime opening (until 16:30) there is also the Akakon Bus from Azuchi north exit (to Ishidera-higashide, about 12 min, ¥200, 5 a day on weekdays and Saturdays; it seems not to run on Sundays and holidays)."),
             ]},
    "photoBase": "../images/higashiomi/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
