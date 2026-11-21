#!/usr/bin/env python3
"""大阪 造幣局の桜の通り抜けと大阪城の桜（4月中旬だけのマップ）のデータ（data/routes/osaka-sakura.json）を書き出す。

使い方: python3 scripts/build_osaka_sakura_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/osaka-sakura/<スポットのid>-<番号>.jpg を番号の順に全部使う（全部 Toshi の写真）
- 造幣局の日程は毎年3月に発表される。発表されたら、下の「2026年は…」の行と notices を新しい年の内容に直す
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/osaka-sakura"
OUT = f"{R}/data/routes/osaka-sakura.json"
CHECKED = "2026-11-21"
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


MINT = "https://www.mint.go.jp/enjoy/toorinuke/sakura_osaka_news_r8.html"
PLANNER = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
NEXT_YEAR = {"from": None, "to": "2027-03-31", "url": "https://www.mint.go.jp/enjoy/toorinuke/",
             "head": T("2027年の日程はまだ出ていません", "Dates for 2027 are not out yet"),
             "text": T("造幣局の桜の通り抜けは、毎年3月に日程と申し込みの方法が発表されます。ここに書いた日時は2026年のものです。行く前に、かならず造幣局の公式サイトを見てください（要確認）。",
                       "The Mint announces each year’s dates and booking method in March. The dates here are those of 2026. Check the Mint’s official site before you go.")}

S = [
    dict(id="temmabashi", name=T("京阪 天満橋駅", "Keihan Temmabashi Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都の祇園四条から京阪の特急で46分。大阪城にも造幣局にも歩いて行ける、この日の出発点です。",
                 "46 minutes by Keihan limited express from Gion-Shijo in Kyoto. Both the castle and the Mint are within walking distance."),
         lat=34.69006, lng=135.51690,
         text=T("京阪 天満橋駅（てんまばしえき）\n\n"
                "京都からは京阪の特急で乗り換えなし。祇園四条14:30発に乗ると、天満橋に15:16に着きます（490円）。特急は昼間およそ10分おきです。JRで来るなら、京都から新快速で大阪へ出て、地下鉄の谷町線で東梅田から天満橋へ。\n\n"
                "駅の北側が大川（おおかわ）。天満橋の上から、両岸に続く桜並木と大阪城の方のビルが見えます（写真は2025年4月9日）。ここから大阪城の大手門まで歩いて約10分、造幣局の南門まで約15分です。\n\n"
                "このマップは4月中旬、造幣局の桜の通り抜けが開いている1週間のためのものです。造幣局は事前の申し込みが必要なので、入る時間を先に決めてから、ほかの場所の時間を合わせてください。\n\nおすすめ到着時間：15:16",
                "Keihan Temmabashi Station\n\n"
                "Direct from Kyoto by Keihan limited express: the 14:30 from Gion-Shijo arrives at 15:16 (¥490). Limited expresses run about every 10 minutes in the daytime. By JR, take the Special Rapid from Kyoto to Osaka, then the Tanimachi subway line from Higashi-Umeda to Temmabashi.\n\n"
                "The Okawa river runs just north of the station. From Temmabashi bridge you see the cherry trees lining both banks and the towers near the castle (photos: 9 April 2025). From here it is about 10 minutes’ walk to the castle’s Otemon gate and about 15 to the Mint’s south gate.\n\n"
                "This map is for one week in mid-April, while the Mint’s cherry-blossom walk is open. The Mint needs advance booking, so fix your entry time there first and fit the other stops around it.\n\nRecommended arrival: 15:16"),
         gmaps=[gm("天満橋駅", "Temmabashi Station", 34.69006, 135.51690, "天満橋駅")],
         links=[PLANNER],
         info=info([row("train", "祇園四条14:30発（京阪特急）→ 天満橋15:16着・490円（乗り換えなし）", "Gion-Shijo 14:30 (Keihan limited express) → Temmabashi 15:16, ¥490 (direct)"),
                    row("train", "帰り：天満橋20:04発（特急）→ 祇園四条20:50着・490円", "Return: Temmabashi 20:04 (limited express) → Gion-Shijo 20:50, ¥490")],
                   tip=T("時刻と運賃は乗換案内（2027年4月の土曜のダイヤ）で確認しました。乗る前にもう一度確かめてください。", "Times and fares from a route planner (Saturday timetable, April 2027). Please check again before you travel."))),
    dict(id="nishinomaru", name=T("大阪城 西の丸庭園の桜", "Cherry blossoms at Osaka Castle’s Nishinomaru Garden"), kind=T("城・庭園（昼の桜と夜桜）", "Castle garden (day and night blossoms)"),
         blurb=T("芝生の向こうに天守閣、手前に桜。大阪城でいちばん桜と天守がきれいに重なる庭です。夜のライトアップがある年も。",
                 "The castle tower beyond a lawn, cherry trees in front: the garden where blossoms and tower line up best. In some years it is lit at night."),
         lat=34.68700, lng=135.52180,
         text=T("大阪城 西の丸庭園（にしのまるていえん）\n\n"
                "天満橋駅から歩いて約20分。大手門をくぐって左へ進んだ所が入口です。お堀の内側の広い芝生の庭で、桜の木の間から天守閣を見上げる場所がいくつもあります。有料なので、外の公園よりずっと静かです。\n\n"
                "大事なのは時期です。ここの桜の多くはソメイヨシノで、見ごろはふつう3月の終わりから4月のはじめ。造幣局の通り抜け（遅咲きの八重桜）は、その1週間ほど後に開きます。"
                "ぼくが昼に行った2025年4月9日は、通り抜けが4月5日からだったので、両方が満開でした（昼の写真）。2026年のように通り抜けが4月9日からの年は、大阪城は散り始めか葉桜のことが多いです。それでも、芝生と天守閣の眺めは変わりません。\n\n"
                "桜の時期には、夜に庭を開けてライトアップする「観桜ナイター」があります。夜の写真は2026年4月8日の20時すぎに撮ったもの（入園350円）。白く光る天守閣に夜桜が重なります。開催の日と時間は年によって違い、通り抜けの週にはもう終わっていることもあるので、行く前に公式サイトで確かめてください。\n\n"
                "ふだんの入園は16:30まで、月曜は休みです。次の造幣局の南門までは、天満橋を渡って歩いて約25分。\n\nおすすめ訪問時間：15:35〜16:45",
                "Nishinomaru Garden, Osaka Castle\n\n"
                "About 20 minutes’ walk from Temmabashi Station; go in by the Otemon gate and the entrance is to the left. A wide lawn inside the moat, with many spots where you look up at the tower between cherry trees. As it charges admission, it is far quieter than the park outside.\n\n"
                "Timing matters. Most trees here are Somei-yoshino, usually at their best from the end of March to early April. The Mint’s walk, with its late double-flowered cherries, opens about a week later. "
                "When I came by day on 9 April 2025, the Mint had opened on 5 April and both were in full bloom (the daytime photos). In a year like 2026, when the Mint opened on 9 April, the castle’s trees are usually falling or in leaf by then. The view of lawn and tower is the same either way.\n\n"
                "In blossom season the garden opens at night with illuminations (“Kan-o Nighter”). The night photos were taken after 20:00 on 8 April 2026 (¥350): night blossoms against the white-lit tower. Dates and hours differ each year and it may be over by the week of the Mint walk, so check the official site first.\n\n"
                "On normal days last entry is 16:30, and the garden is closed on Mondays. The Mint’s south gate is about 25 minutes’ walk from here, across Temmabashi bridge.\n\nRecommended visit time: 15:35–16:45"),
         gmaps=[gm("大阪城 西の丸庭園", "Nishinomaru Garden", 34.68700, 135.52180, "大阪城 西の丸庭園"),
                gm("大手門", "Otemon gate", 34.68605, 135.52125, "大阪城 大手門")],
         links=[link("official", "大阪城パークセンター（大阪城公園）", "Osaka Castle Park (official)", "https://osakacastlepark.jp/"),
                link("official", "大阪城天守閣 公式サイト", "Osaka Castle Museum (official)", "https://www.osakacastle.net/", "https://www.osakacastle.net/english/")],
         info=info([row("hours", "3〜10月 9:00〜17:00（入園は16:30まで）", "March–October 9:00–17:00 (last entry 16:30)"),
                    row("closed", "月曜（祝日のときは次の平日）、年末年始", "Mondays (next weekday if a holiday), New Year period"),
                    row("fee", "300円（桜の時期は350円）", "¥300 (¥350 in blossom season)"),
                    row("hours", "夜桜のライトアップ（観桜ナイター）：2027年の日程は未発表（要確認）。2026年4月8日は20時台に入れました", "Night illumination: 2027 dates not announced (please check). On 8 April 2026 it was open after 20:00")],
                   tip=T("時間・休み・料金は大阪周遊パスの公式サイトの施設案内で確認しました。観桜ナイターの日程は公式サイトで確認できなかったので、2026年に行ったときのことを書いています。",
                         "Hours, closing day and fee from the facility list on the Osaka Amazing Pass site. The night-opening dates could not be confirmed officially; what is written is from my visit in 2026."), verified=False)),
    dict(id="mint", name=T("造幣局 桜の通り抜け", "Japan Mint cherry-blossom walk"), kind=T("桜（4月中旬の1週間だけ）", "Cherry blossoms (one week in mid-April)"),
         notices=[NEXT_YEAR],
         blurb=T("硬貨をつくる造幣局の構内を、年に1週間だけ歩けます。約560mの道に、140品種・331本の八重桜（2026年）。",
                 "For one week a year you can walk through the grounds of the Mint: 331 trees of 140 varieties, mostly double-flowered, along 560 m (2026)."),
         lat=34.69550, lng=135.52150,
         text=T("造幣局（ぞうへいきょく）の桜の通り抜け\n\n"
                "明治16年（1883年）から続く、大阪の春の行事です。大川沿いの造幣局の構内、約560mの道を、南門（天満橋側）から北門（桜宮橋側）へ一方通行で歩きます。後戻りはできません。\n\n"
                "ここの桜は、ほとんどが遅咲きの八重桜。ソメイヨシノとはまったく違って、ぼたんのように重たい花、緑がかった花、1本に白とピンクが混ざる花と、品種ごとに札が立っています。2026年は140品種331本で、「今年の花」は黄緑色の御衣黄（ぎょいこう）でした。写真は2025年4月9日と2026年4月14日。赤レンガの建物の前の関山（かんざん）や、白い花の札「舞姫」を探してみてください。\n\n"
                "近年は事前の申し込みが必要です。2026年は4月9日〜15日の7日間で、インターネットで入場の時間帯を選んで申し込む方式（先着順）。当日は、申し込みのメールに届く2次元コードを入口で見せます。申し込んだ時間帯以外は、原則として入れません。\n\n"
                "ぼくのおすすめは夕方の時間帯。17時を過ぎると昼より人が少し減り、ぼんぼりに灯が入ります。歩くだけなら30分、写真を撮りながらで1時間。中での飲食はできず、日傘・自撮り棒・三脚も使えません。入口で手荷物の検査があります。\n\nおすすめ訪問時間：17:15〜18:15（申し込んだ時間帯に合わせる）",
                "The Japan Mint cherry-blossom walk\n\n"
                "An Osaka spring custom since 1883. You walk about 560 m through the Mint’s riverside grounds, one way only, from the south gate (Temmabashi side) to the north gate (Sakuranomiya bridge side). There is no turning back.\n\n"
                "Nearly all the trees are late-blooming double-flowered cherries, nothing like Somei-yoshino: blooms heavy as peonies, greenish ones, trees mixing white and pink, each variety with its own name board. In 2026 there were 331 trees of 140 varieties, and the “flower of the year” was the yellow-green Gyoiko. Photos: 9 April 2025 and 14 April 2026. Look for the Kanzan in front of the red-brick building and the name board for the white Maihime.\n\n"
                "In recent years you must book ahead. In 2026 it ran for 7 days, 9–15 April, with online booking of an entry time slot (first come, first served). On the day you show the 2D code from your confirmation e-mail at the entrance; outside your slot you are generally not admitted.\n\n"
                "I recommend an evening slot. After 17:00 the crowd thins a little and the paper lanterns are lit. It takes 30 minutes just to walk, an hour with photos. No eating or drinking inside, and no parasols, selfie sticks or tripods. Bags are checked at the entrance.\n\nRecommended visit time: 17:15–18:15 (match your booked slot)"),
         gmaps=[gm("造幣局 南門（入口）", "Mint south gate (entrance)", 34.69335, 135.52060, "造幣局 南門 大阪"),
                gm("造幣局 北門（出口）", "Mint north gate (exit)", 34.69780, 135.52200, "造幣局 北門 大阪")],
         links=[link("official", "造幣局 桜の通り抜け（公式）", "Japan Mint: cherry-blossom walk (official, Japanese)", MINT, "https://www.mint.go.jp/eng/")],
         info=info([row("hours", "2026年は4月9日（木）〜15日（水）。平日10:00〜19:15、土日9:00〜19:15（19:45までに退場）", "2026: 9–15 April. Weekdays 10:00–19:15, weekends 9:00–19:15 (everyone out by 19:45)"),
                    row("fee", "事前申込制（インターネット・先着順）。2026年は3月18日に受付が始まりました。2027年の日程と申し込み方法は未発表（要確認）", "Advance booking online, first come first served. In 2026 booking opened on 18 March. Dates and booking for 2027 not yet announced (please check)"),
                    row("closed", "造幣博物館は通り抜けの期間は臨時休館（2026年は4月8日〜15日）", "The Mint Museum closes during the event (8–15 April in 2026)"),
                    row("train", "天満橋駅（京阪は14番出口、谷町線は2号出口）から歩いて約15分。入口は南門だけ", "About 15 minutes’ walk from Temmabashi Station (Keihan exit 14, Tanimachi Line exit 2). Entry is by the south gate only")],
                   tip=T("造幣局の公式サイト（2026年の開催情報と「沿革・データ」）で確認しました。受付が始まった日は当時の報道によります。",
                         "From the Mint’s official site (2026 event page and its history page). The date booking opened is from news reports at the time."), verified=False)),
    dict(id="kema", name=T("毛馬桜之宮公園（大川沿いの桜並木）", "Kema Sakuranomiya Park (the Okawa riverside)"), kind=T("公園・桜並木", "Riverside park & cherry trees"),
         blurb=T("造幣局の北門を出たら、目の前の桜宮橋を渡って川沿いへ。申し込みもお金もいらない、長い桜並木です。",
                 "Out of the Mint’s north gate, cross Sakuranomiya bridge to the riverside: a long avenue of cherry trees with no booking and no charge."),
         lat=34.69760, lng=135.52330,
         text=T("毛馬桜之宮公園（けまさくらのみやこうえん）\n\n"
                "大川の両岸に、毛馬から天満橋まで約4.2km続く公園で、およそ4,800本の桜が植えられています。造幣局の北門を出ると、銀色のアーチの桜宮橋（さくらのみやばし・通称「銀橋」）のたもと。橋を渡って東岸の遊歩道に下りると、桜の下を川と並んで歩けます。\n\n"
                "ここはソメイヨシノが中心なので、見ごろは造幣局より1週間ほど早め。写真は2025年4月9日の夕方で、この年は両方が重なりました。水上バスや屋形船が行き来し、対岸の桜と大阪城の方のビルが川に映ります。夕方は西日で花が金色に見える時間です。\n\n"
                "桜宮橋から南へ歩けば、天満橋駅まで約18分。通り抜けの期間は、造幣局の裏の川沿いに屋台が並びます（2025年に見たときのこと）。北へ歩けばJR環状線の桜ノ宮駅まで約15分で、大阪駅で新快速に乗り換えて京都へ帰れます（約42分・840円）。\n\nおすすめ訪問時間：18:15〜18:45",
                "Kema Sakuranomiya Park\n\n"
                "A park running about 4.2 km along both banks of the Okawa from Kema down to Temmabashi, planted with some 4,800 cherry trees. The Mint’s north gate brings you out at the foot of Sakuranomiya bridge, a silver arch known locally as Ginbashi. Cross it and step down to the east-bank promenade to walk under the blossoms beside the water.\n\n"
                "The trees here are mostly Somei-yoshino, so they peak about a week before the Mint. The photos are from the evening of 9 April 2025, a year when the two overlapped. Water buses and pleasure boats pass, and the far-bank blossoms and the towers near the castle reflect in the river. Towards evening the low sun turns the flowers gold.\n\n"
                "Walking south from the bridge, Temmabashi Station is about 18 minutes. During the Mint week, food stalls line the riverside behind the Mint (as I saw in 2025). Walking north, JR Sakuranomiya Station on the Loop Line is about 15 minutes; change at Osaka to the Special Rapid for Kyoto (about 42 min, ¥840).\n\nRecommended visit time: 18:15–18:45"),
         gmaps=[gm("桜宮橋（銀橋）", "Sakuranomiya bridge", 34.69760, 135.52260, "桜宮橋 大阪"),
                gm("JR桜ノ宮駅", "JR Sakuranomiya Station", 34.70500, 135.52090, "桜ノ宮駅")],
         links=[link("info", "毛馬桜之宮公園（大阪観光局）", "Kema Sakuranomiya Park (Osaka Info)", "https://osaka-info.jp/spot/kema-sakuranomiya-park/", "https://osaka-info.jp/en/spot/kema-sakuranomiya-park/"), PLANNER],
         info=info([row("fee", "無料。いつでも歩けます", "Free; open at all hours"),
                    row("train", "帰り（京阪）：天満橋20:04発（特急）→ 祇園四条20:50着・490円", "Return (Keihan): Temmabashi 20:04 (limited express) → Gion-Shijo 20:50, ¥490"),
                    row("train", "帰り（JR）：桜ノ宮19:02発 → 大阪で新快速に乗り換え → 京都19:44着・840円", "Return (JR): Sakuranomiya 19:02 → change at Osaka to the Special Rapid → Kyoto 19:44, ¥840")],
                   tip=T("公園の長さと桜の本数は大阪市の広報（2009年）の数字で、今の本数は確認できていません（要確認）。電車は乗換案内です。",
                         "Length and tree count are from an Osaka City bulletin of 2009; the current count is unconfirmed. Trains from a route planner."), verified=False)),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    out.setdefault("notices", [])
    spots.append(out)

data = {
    "id": "osaka-sakura",
    "_note": "大阪 造幣局の桜の通り抜けと大阪城の桜（osaka-sakura/ のページ専用。形は eizan-line.json と同じ）。4月中旬の1週間だけのマップ。京阪 天満橋駅→大阪城 西の丸庭園→造幣局 桜の通り抜け（南門から北門へ一方通行）→毛馬桜之宮公園→天満橋駅か桜ノ宮駅。"
             "写真は全部 Toshi の写真ライブラリから（2025年4月9日の Nikon D7000 と iPhone、2026年4月14日の造幣局、2026年4月8日の夜の西の丸庭園。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（造幣局の公式サイト、大阪周遊パスの公式サイトの施設案内、電車は乗換案内）。2027年の通り抜けの日程は未発表なので、verified: false と notices で要確認と出している。このファイルは scripts/build_osaka_sakura_data.py で作る。",
    "sections": [{"first": 1, "last": 2, "day": 0}, {"first": 3, "last": 3, "day": 1}, {"first": 4, "last": 4, "day": 2}],
    "photoBase": "../images/osaka-sakura/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
