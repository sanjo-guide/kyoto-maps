#!/usr/bin/env python3
"""大阪 造幣局の桜の通り抜け（春のマップ）のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_osaka_sakura_data.py  （そのあと python3 scripts/sync_osaka_sakura.py）
- 作るもの（COURSES）:
  - data/routes/osaka-sakura.json … 「造幣局は午後の枠」（late・最初に開く）。9:30ごろ梅田・なんば→天満橋→大阪城 西の丸庭園→
    （天守閣・玉造口の八重桜）→JO-TERRACE でお昼→造幣局 15:00ごろの枠→毛馬桜之宮公園→天満で晩ごはん
  - data/routes/osaka-sakura-early.json … 「造幣局は朝いちばんの枠」（early）。平日10:00・土日9:00の枠→毛馬桜之宮公園→
    JO-TERRACE でお昼→玉造口→天守閣→西の丸庭園→中之島を歩いて淀屋橋→夜の道頓堀
  どちらも直接直さない（実行のたびに作り直す）
- 起点は大阪の梅田〜難波のあたりのホテル（宿の名前は書かない）。京都から来る人の電車は1番のスポットに短く
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容
  - COURSES … コースごとの並び順、めやすの時間、行き方、最後のスポットに続ける夕方と夜
  - SOURCES … 時刻・料金の出典と確認日（データの sources に入る）
- 造幣局の日程・時間・申し込み方法は全部「2026年の実績」。来春の発表（2026年は3月10日発表、3月18日申込開始）が出たら、
  文章・notices・SOURCES と scripts/sync_osaka_sakura.py の SEASON_FROM / SEASON_TO を直す
- 電車の時刻は2026年12月2日（水）と5日（土）で乗換案内を引いたもの。春までに改正があったら確かめ直す
- 写真は images/osaka-sakura/<スポットのid>-<番号>.jpg を番号の順に全部使う（全部 Toshi の写真。足していない）。
  天守閣・玉造口・JO-TERRACE・天満・中之島は写真がないので、スポットにせず文章で案内する
- 2026-11-23 オーナーの基準（ゲストが実際に回れる1日）で作り直した。造幣局は申し込んだ時間帯でしか入れないので、
  コースは「朝いちばんの枠」と「午後の枠」に分けた
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "osaka-sakura"
IMG = f"{R}/images/{MAP_ID}"
CHECKED = "2026-11-23"

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


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


MINT = "https://www.mint.go.jp/enjoy/toorinuke/sakura_osaka_news_r8.html"
MINT_TOP = "https://www.mint.go.jp/enjoy/toorinuke/"
MINT_DATA = "https://www.mint.go.jp/enjoy/toorinuke/sakura_osaka_data.html"
MINT_NEWS = "https://kumanichi.com/articles/1966401"
NISHI = "https://www.osakacastlepark.jp/articles/detail.html?id=72"
NISHI_FEE = "https://www.osakacastlepark.jp/cms/public/api/v1/informations/489"
PARK_NEWS = "https://www.osakacastlepark.jp/news/"
SAKURA = "https://www.osakacastlepark.jp/articles/detail.html?id=74"
PARK_FAQ = "https://www.osakacastlepark.jp/articles/detail.html?id=3"
TENSHU = "https://osaka-info.jp/spot/osaka-castle-main-keep/"
JOT = "https://www.jo-terrace.jp/shop"
KEMA = "https://osaka-info.jp/spot/kema-sakuranomiya-park/"
YAHOO = "https://transit.yahoo.co.jp/"

L_YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", YAHOO)
L_MINT = link("official", "造幣局 桜の通り抜け（2026年の開催情報）", "Japan Mint: cherry-blossom walk, 2026 (Japanese)", MINT, "https://www.mint.go.jp/eng/")
L_MINT_TOP = link("official", "造幣局 桜の通り抜け（来春の発表はここに）", "Japan Mint: cherry-blossom walk (next spring’s notice)", MINT_TOP)
L_JOT = link("official", "JO-TERRACE OSAKA（お店と時間）", "JO-TERRACE OSAKA: shops and hours (Japanese)", JOT)
L_OSAKA = link("info", "大阪のマップ（夜の道頓堀・法善寺横丁）", "Osaka map (Dotonbori and Hozenji at night)", "../osaka/#list")

# ---------------------------------------------------------------------------
# お知らせ
# ---------------------------------------------------------------------------
OFF_JA = "造幣局の桜の通り抜けが開く、4月中旬の約1週間のためのマップです。いまは開いていません。日程・時間・申し込み方法は2026年の実績、電車は2026年12月の時刻です。来春は要確認（例年3月に造幣局が発表）。"
OFF_EN = "This map is for the week in mid-April when the Japan Mint opens its cherry walk. It is not open now. Dates, hours and booking are as in 2026 and trains as of December 2026, so please check for next spring (the Mint announces each March)."
OFF_SEASON = [
    notice("春のマップです（いまは通り抜けをやっていません）", "A spring map: the Mint walk is not open now", OFF_JA, OFF_EN, url=MINT_TOP, to="2027-03-31"),
    notice("春のマップです（いまは通り抜けをやっていません）", "A spring map: the Mint walk is not open now", OFF_JA, OFF_EN, url=MINT_TOP, frm="2027-04-21"),
]

N_BOOK = notice(
    "申し込んでいないと入れません", "No entry without booking",
    "2026年は、インターネットで入場の時間帯を選ぶ事前申込制（時間帯ごとに定員、先着順）でした。受付は3月18日9:00から。当日は申し込みのメールの2次元コードを入口で見せます（スマホか印刷したもの）。入れるのは申し込んだ時間帯だけです。来春の日程と申し込み方法は要確認。",
    "In 2026 you booked an entry time slot online in advance (each slot has a limit, first come, first served); booking opened at 9:00 on 18 March. On the day you show the 2D code from the confirmation e-mail at the gate, on a phone or printed. You can enter only in your slot. Please check next spring’s dates and booking.",
    url=MINT)
N_RULES = notice(
    "中では食べられません。日傘・自撮り棒も不可", "No food inside; no parasols or selfie sticks",
    "入口で手荷物の検査があります。中は飲食禁止・全面禁煙で、日傘・自撮り棒・三脚・自転車・ペット（補助犬は可）は持ち込めません。南門から北門への一方通行で、戻れません。駐車場はありません。天気が悪いと急に中止になることがあります（2026年の案内）。",
    "Bags are checked at the gate. No eating, drinking or smoking inside, and no parasols, selfie sticks, tripods, bicycles or pets (assistance dogs allowed). It is one way, south gate to north gate, with no turning back. There is no parking. It can be called off at short notice in bad weather (2026 rules).",
    url=MINT)
N_MONDAY = notice(
    "西の丸庭園は月曜休み", "Nishinomaru Garden is closed on Mondays",
    "月曜（祝日なら翌日）は休園です。2026年の通り抜けの週にも月曜（4月13日）がありました。月曜は外から天守閣と玉造口の八重桜を見て、天守閣（毎日開館）に上がってください。観桜期の休みの扱いは要確認。",
    "It closes on Mondays (the next day if Monday is a holiday); the 2026 Mint week included Monday 13 April. On a Monday, see the castle and the late cherries at Tamatsukuri-guchi from the park, and go up the castle tower (open daily). Whether it closes on Mondays in blossom season is unconfirmed.",
    url=NISHI)
N_NIGHTER = notice(
    "観桜期は夜も開き、料金が上がります", "In blossom season it opens at night and costs more",
    "3月下旬〜4月上旬の「観桜ナイター」期は、夜も開いて入園料が350円になります（ふだんは300円）。日程は毎年発表されます。通り抜けの週まで続いているかは、その年の発表で確かめてください（要確認）。",
    "During the “Kan-o Nighter” blossom season, late March to early April, the garden also opens at night and charges ¥350 (normally ¥300). Dates are announced each year; check whether they still run in the week of the Mint walk.",
    url=PARK_NEWS)
N_JOT = notice(
    "月曜はたこ焼きとお好み焼きの店が休み", "The takoyaki and okonomiyaki shops close on Mondays",
    "JO-TERRACE OSAKA のたこ焼道楽わなか（祝日は営業）と名代 千房は月曜休みです。ほかの店（とんかつ・和定食・カフェなど）は開いています。",
    "At JO-TERRACE OSAKA, Takoyaki Doraku Wanaka (open on holidays) and Chibo close on Mondays. The other places (tonkatsu, set meals, cafés and more) are open.",
    url=JOT)

# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    temmabashi=dict(
        name=T("天満橋駅", "Temmabashi Station"), kind=T("駅（スタート）", "Station (start)"),
        blurb=T("梅田から地下鉄で5分、なんばから15分ほど。大阪城にも造幣局にも歩いて行ける、この日の出発点です。",
                "Five minutes by subway from Umeda, about 15 from Namba: the start of the day, within walking distance of both the castle and the Mint."),
        caution=T("造幣局は申し込んだ時間帯だけ入れます", "The Mint admits you only in your booked slot"),
        lat=34.69006, lng=135.51690,
        body=T("天満橋駅（てんまばしえき）\n\n"
               "地下鉄谷町線と京阪の駅です。北側の天満橋（橋）に上がると、大川（おおかわ）の両岸に桜並木が続き、上流の左岸に造幣局があります（写真は2025年4月9日）。\n\n"
               "梅田からは東梅田駅から谷町線で4〜5分・190円。なんばからは千日前線で谷町九丁目へ行き、谷町線に乗り換えて13〜15分・240円です。どちらも数分おきに走っています。\n\n"
               "京都から来る人は、京阪の三条・祇園四条から天満橋まで特急で約50分・490円、乗り換えなしです。",
               "Temmabashi Station\n\n"
               "A Tanimachi subway and Keihan station. Climb to Temmabashi bridge on the north side: cherry trees line both banks of the Okawa river, and the Mint stands upstream on the left bank (photos: 9 April 2025).\n\n"
               "From Umeda take the Tanimachi Line from Higashi-Umeda, 4–5 minutes, ¥190. From Namba take the Sennichimae Line to Tanimachi 9-chome and change to the Tanimachi Line, 13–15 minutes, ¥240. Both run every few minutes.\n\n"
               "From Kyoto, Keihan limited expresses run from Sanjo and Gion-Shijo to Temmabashi in about 50 minutes, ¥490, no change."),
        gmaps=[gm("天満橋駅", "Temmabashi Station", 34.69006, 135.51690, "天満橋駅")],
        links=[L_MINT, L_YAHOO],
        notices=[],
        _rows=[row("train", "梅田（東梅田）→ 天満橋：谷町線 4〜5分・190円", "Higashi-Umeda → Temmabashi: Tanimachi Line, 4–5 min, ¥190"),
               row("train", "なんば → 天満橋：千日前線・谷町線（谷町九丁目で乗り換え）13〜15分・240円", "Namba → Temmabashi: Sennichimae and Tanimachi lines (change at Tanimachi 9-chome), 13–15 min, ¥240")],
        _tip=T("電車は乗換案内で平日と土曜（2026年12月の時刻）を確認しました。春までに変わることがあるので要確認。",
               "Trains checked on a route planner for a weekday and a Saturday (December 2026 timetable); they may change by spring."),
        _source=f"乗換案内（Yahoo!路線情報）{YAHOO}。2026-11-23に確認"),
    nishinomaru=dict(
        name=T("大阪城 西の丸庭園", "Osaka Castle: Nishinomaru Garden"), kind=T("城の庭園（ソメイヨシノ）", "Castle garden (Somei-Yoshino)"),
        blurb=T("芝生の向こうに天守閣、手前に桜。約300本の桜の庭です。八重桜は南東の玉造口へ。",
                "The castle tower beyond a lawn and cherry trees: a garden of about 300 trees. For late double cherries, go on to Tamatsukuri-guchi."),
        caution=T("月曜休み。入園は16:30まで（3〜10月）", "Closed Mondays. Last entry 16:30 (March–October)"),
        lat=34.68740, lng=135.52220,
        body=T("大阪城 西の丸庭園（にしのまるていえん）\n\n"
               "大手門をくぐって左、お堀の内側の芝生の庭です。ソメイヨシノを中心に約300本の桜があり、木の間から天守閣を見上げられます。大阪の桜の開花を決める標本木もこの庭にあります。有料なので、外の公園より落ち着いて歩けます。\n\n"
               "ソメイヨシノの見ごろは、ふつう造幣局の八重桜より早めです。昼の写真は2025年4月9日で、造幣局と同じ日に撮りました。年によっては、通り抜けの週には散りはじめか葉桜です。芝生と天守閣の眺めは変わりません。夜の写真は2026年4月8日の20時すぎ、観桜ナイターのときです。\n\n"
               "通り抜けの週にまだ咲いている桜を見るなら、城の南東の玉造口（たまつくりぐち）へ。遅咲きの八重桜が植えてあり、桜の季節の最後まで咲いています（大阪城公園の案内）。\n\n"
               "天守閣に上がるなら9:00〜18:00（入館は17:30まで）、大人1,200円です。",
               "Nishinomaru Garden, Osaka Castle\n\n"
               "Go in by the Otemon gate and turn left: a lawn inside the moat with about 300 cherry trees, mostly Somei-Yoshino, and views of the tower between them. The tree that decides Osaka’s official blossom date grows here. It charges admission, so it is calmer than the park outside.\n\n"
               "Somei-Yoshino usually peak earlier than the Mint’s double cherries. The daytime photos are from 9 April 2025, the same day as the Mint photos; in some years the garden is shedding petals or in leaf by the Mint week. The lawn and tower look the same either way. The night photos were taken after 20:00 on 8 April 2026, during the evening opening.\n\n"
               "For blossom that is still out that week, walk to Tamatsukuri-guchi on the castle’s south-east side, planted with late double cherries that flower to the end of the season (Osaka Castle Park).\n\n"
               "The castle tower is open 9:00–18:00 (last entry 17:30), ¥1,200 for adults."),
        gmaps=[gm("大阪城 西の丸庭園", "Nishinomaru Garden", 34.68740, 135.52220, "大阪城 西の丸庭園"),
               gm("大手門", "Otemon gate", 34.68605, 135.52125, "大阪城 大手門"),
               gm("大阪城天守閣", "Osaka Castle tower", 34.68731, 135.52590, "大阪城天守閣"),
               gm("玉造口（八重桜）", "Tamatsukuri-guchi (late cherries)", 34.68220, 135.52870, "大阪城 玉造口")],
        links=[link("official", "西の丸庭園（大阪城公園）", "Nishinomaru Garden (Osaka Castle Park, Japanese)", NISHI),
               link("official", "大阪城公園の桜（玉造口の八重桜）", "Cherry blossoms in Osaka Castle Park (Japanese)", SAKURA),
               link("info", "大阪城天守閣（大阪観光局）", "Osaka Castle Main Tower (Osaka Info)", TENSHU, "https://osaka-info.jp/en/spot/osaka-castle-main-keep/")],
        notices=[N_MONDAY, N_NIGHTER],
        _rows=[row("hours", "3〜10月 9:00〜17:00（入園は16:30まで）。観桜期は時間が変わる（要確認）", "March–October 9:00–17:00 (last entry 16:30). Different in blossom season (please check)"),
               row("closed", "月曜（祝日なら翌日）、12/28〜1/4", "Mondays (next day if a holiday), 28 Dec – 4 Jan"),
               row("fee", "大人300円（2026年4月から）。観桜ナイター期（3月下旬〜4月上旬）は350円", "¥300 adults (from April 2026); ¥350 in the evening-opening season (late March – early April)"),
               row("hours", "天守閣：9:00〜18:00（入館は17:30まで）、大人1,200円", "Castle tower: 9:00–18:00 (last entry 17:30), ¥1,200 adults")],
        _tip=T("大阪城公園の公式サイト（西の丸庭園・入園料のお知らせ・桜の案内）と、大阪観光局の天守閣の案内で確認しました。",
               "Checked on the Osaka Castle Park website (garden page, fee notice, cherry page) and the Osaka Info page for the tower."),
        _source=f"大阪城公園 {NISHI}・{NISHI_FEE}・{SAKURA}、大阪観光局 {TENSHU}。2026-11-23に確認"),
    mint=dict(
        name=T("造幣局 桜の通り抜け", "Japan Mint cherry-blossom walk"), kind=T("八重桜（4月中旬の1週間）", "Double cherries (one week in mid-April)"),
        blurb=T("硬貨をつくる造幣局の構内を、年に1週間だけ歩けます。約560mの道に、140品種331本の桜（2026年）。",
                "For one week a year you can walk the grounds of the Mint: 331 trees of 140 varieties along 560 m (2026)."),
        caution=T("事前申込制。申し込んだ時間帯だけ入れます", "Advance booking only; you enter in your slot"),
        lat=34.69550, lng=135.52150,
        body=T("造幣局（ぞうへいきょく）の桜の通り抜け\n\n"
               "1883年（明治16年）から続く、大阪の春の行事です。川沿いの造幣局の構内、約560mの道を、南門から北門へ一方通行で歩きます。\n\n"
               "ここの桜は八重桜が中心で、ソメイヨシノより遅く咲きます。ぼたんのように重たい花、緑がかった花など、木ごとに品種の名札があります。2026年は140品種331本で、「今年の花」は黄緑色の御衣黄（ぎょいこう）でした。写真は2025年4月9日と2026年4月14日。赤レンガの建物の前の関山（かんざん）や、白い花の「舞姫」の名札を探してみてください。\n\n"
               "歩くだけなら30分、写真を撮りながらで1時間ほど。\n\n"
               "2026年は4月9日〜15日の7日間、平日10:00〜19:15、土日9:00〜19:15に入場（19:45に全員退場）。日程は3月10日に発表され、申し込みは3月18日に始まりました。",
               "The Japan Mint cherry-blossom walk\n\n"
               "An Osaka spring custom since 1883. You walk about 560 m through the Mint’s riverside grounds, one way, from the south gate to the north gate.\n\n"
               "The trees are mostly late double-flowered cherries, which bloom after the Somei-Yoshino: blooms heavy as peonies, greenish ones, each tree with a name board. In 2026 there were 331 trees of 140 varieties, and the “flower of the year” was the yellow-green Gyoiko. Photos: 9 April 2025 and 14 April 2026. Look for the Kanzan in front of the red-brick building and the board for the white Maihime.\n\n"
               "Thirty minutes just to walk, about an hour with photos.\n\n"
               "In 2026 it ran for 7 days, 9–15 April, entry 10:00–19:15 on weekdays and 9:00–19:15 at weekends (everyone out by 19:45). The dates were announced on 10 March and booking opened on 18 March."),
        gmaps=[gm("造幣局 南門（入口）", "Mint south gate (entrance)", 34.69335, 135.52060, "造幣局 南門 大阪"),
               gm("造幣局 北門（出口）", "Mint north gate (exit)", 34.69780, 135.52200, "造幣局 北門 大阪")],
        links=[L_MINT, L_MINT_TOP, link("official", "桜の通り抜けのデータ（造幣局）", "Facts about the walk (Japan Mint, Japanese)", MINT_DATA)],
        notices=[N_BOOK, N_RULES],
        _rows=[row("hours", "2026年の実績：4月9日（木）〜15日（水）。平日10:00〜19:15、土日9:00〜19:15（19:45までに退場）。来春は要確認", "As held in 2026: 9–15 April. Weekdays 10:00–19:15, weekends 9:00–19:15 (out by 19:45). Next spring: please check"),
               row("fee", "無料。事前申込制（インターネット・時間帯ごとの先着順）。2026年は3月18日9:00に受付開始", "Free. Advance online booking by time slot, first come first served. Booking opened 18 March 2026 at 9:00"),
               row("train", "南門まで：天満橋駅（京阪は東改札14番出口、谷町線は北改札2号出口）から歩いて約15分。JR大阪城北詰駅3番出口からも約15分", "To the south gate: about 15 min on foot from Temmabashi (Keihan east gate exit 14, Tanimachi Line north gate exit 2) or JR Osakajo-kitazume exit 3"),
               row("closed", "造幣博物館は期間中休館（2026年は4月8日〜15日）", "The Mint Museum closes during the event (8–15 April in 2026)")],
        _tip=T("造幣局の公式サイト（2026年の開催情報・データ）で確認しました。品種と本数、発表日と申込開始は、公式の発表を伝えた報道（2026年3月10日）によります。",
               "Checked on the Mint’s website (2026 event page and facts page). Tree numbers, the announcement date and the booking date are from a news report of the Mint’s announcement (10 March 2026)."),
        _source=f"造幣局 {MINT}・{MINT_DATA}、報道（熊本日日新聞・共同通信 2026-03-10）{MINT_NEWS}。2026-11-23に確認"),
    kema=dict(
        name=T("毛馬桜之宮公園（大川沿いの桜並木）", "Kema Sakuranomiya Park (the Okawa riverside)"), kind=T("川沿いの公園", "Riverside park"),
        blurb=T("造幣局の北門を出たら、桜宮橋を渡って川沿いへ。申し込みもお金もいらない、約4,500本の桜の川岸です。",
                "Out of the Mint’s north gate, cross Sakuranomiya bridge to the riverside: some 4,500 cherry trees, no booking, no charge."),
        caution=T("いつでも無料", "Free, open at all hours"),
        lat=34.69760, lng=135.52330,
        body=T("毛馬桜之宮公園（けまさくらのみやこうえん）\n\n"
               "大川の両岸、毛馬の洗堰（あらいぜき）から天満橋まで続く川沿いの公園で、約4,500本の桜があります（大阪観光局）。いつでも無料で歩けます。\n\n"
               "造幣局の北門を出ると、銀色のアーチの桜宮橋（さくらのみやばし、通称「銀橋」）のたもとです。橋を渡って東岸の遊歩道に下りると、桜の下を川と並んで歩けます。ソメイヨシノが多いので見ごろは造幣局より早め。写真は2025年4月9日の夕方です。",
               "Kema Sakuranomiya Park\n\n"
               "A riverside park on both banks of the Okawa from the Kema weir down to Temmabashi, with about 4,500 cherry trees (Osaka Info). It is free and open at all hours.\n\n"
               "The Mint’s north gate brings you out at the foot of Sakuranomiya bridge, a silver arch known as Ginbashi. Cross it and step down to the east-bank path to walk under the blossom beside the water. Most trees are Somei-Yoshino, so they peak before the Mint. Photos: the evening of 9 April 2025."),
        gmaps=[gm("桜宮橋（銀橋）", "Sakuranomiya bridge", 34.69760, 135.52260, "桜宮橋 大阪"),
               gm("JR桜ノ宮駅", "JR Sakuranomiya Station", 34.70500, 135.52090, "桜ノ宮駅")],
        links=[link("info", "毛馬桜之宮公園（大阪観光局）", "Kema Sakuranomiya Park (Osaka Info)", KEMA, "https://osaka-info.jp/en/spot/kema-sakuranomiya-park/")],
        notices=[],
        _rows=[row("fee", "無料。いつでも歩けます", "Free; open at all hours")],
        _tip=T("大阪観光局の案内で確認しました（桜の本数・常時開園）。歩く時間は地図の徒歩ルートに少し足した目安です。",
               "Checked with Osaka Info (tree count, always open). Walking times are map estimates, rounded up a little."),
        _source=f"大阪観光局 {KEMA}。2026-11-23に確認"),
)

VIS = ("おすすめ訪問時間", "Recommended visit time")

# ---------------------------------------------------------------------------
# 最後のスポットのあとに続ける文章（夕方と夜）
# ---------------------------------------------------------------------------
AFTER_LATE = T(
    "夕方の続き：天満で晩ごはん（17:30ごろ）\n\n"
    "桜宮橋を西へ戻り、天神橋筋商店街（てんじんばしすじ）とJR天満駅のまわりへ。歩いて20〜25分です。南北に長いアーケードで、駅のまわりは飲食店が多く集まっています。21〜22時ごろまで。閉まる時間は店の表で確かめてください。\n\n"
    "帰り：梅田へはJR天満から大阪まで1駅・3分・150円。なんばへは、天満駅から歩いて4分の地下鉄扇町駅から堺筋線で日本橋へ（約10分・240円）。\n"
    "京都へ帰る人：JR天満21:03発（土日祝21:11発）→大阪で新快速に乗り換え→京都21:44着（21:49着）・750円。最終は天満23:45発→京都0:30着（毎日同じ）。京阪なら天満橋23:36発の特急が最終で、三条0:22着・490円。",
    "Evening: dinner in Tenma (about 17:30)\n\n"
    "Walk back west over Sakuranomiya bridge to the Tenjinbashi-suji shopping street and JR Tenma Station, 20–25 minutes. It is a long north–south arcade, and the streets by the station are packed with places to eat and drink. Stay until 21:00 or 22:00; check closing times at the door.\n\n"
    "Back: to Umeda, JR from Tenma to Osaka is one stop, 3 minutes, ¥150. To Namba, walk 4 minutes to Ogimachi subway station and take the Sakaisuji Line to Nippombashi (about 10 minutes, ¥240).\n"
    "To Kyoto: JR Tenma 21:03 (21:11 at weekends and on holidays) → change at Osaka to the Special Rapid → Kyoto 21:44 (21:49), ¥750. The last is Tenma 23:45 → Kyoto 0:30 (every day). By Keihan, the last limited express leaves Temmabashi at 23:36 for Sanjo, arriving 0:22, ¥490.")

AFTER_EARLY = T(
    "夕方の続き：中之島を歩いて、夜は道頓堀（16:15ごろ）\n\n"
    "大手門から天満橋駅へ戻り（15分ほど）、天神橋を渡って中之島公園へ。川に挟まれた細長い島を西へ歩き、赤レンガの中央公会堂の前を通って淀屋橋まで、ゆっくり40分ほどです。淀屋橋から地下鉄御堂筋線でなんばへ（約6分・190円、数分おき）。\n\n"
    "夜は道頓堀と法善寺横丁へ。大阪のマップに、夜の道頓堀と晩ごはんのことを書いています。21〜22時ごろまで。\n"
    "京都へ帰る人：地下鉄なんば21:39発（土日祝21:48発）の御堂筋線→淀屋橋で京阪特急に乗り換え→三条22:41着（22:50着）・680円。JRなら、なんば21:39発（平日）の御堂筋線で梅田へ、大阪22:00発の新快速で京都22:29着・820円。最終は地下鉄なんば23:18発→淀屋橋23:33発の京阪特急→三条0:22着（毎日同じ）。",
    "Later: Nakanoshima on foot, then Dotonbori (about 16:15)\n\n"
    "From the Otemon gate walk back to Temmabashi Station (about 15 minutes), cross Tenjin-bashi bridge to Nakanoshima Park, and walk west along the narrow island between the rivers, past the red-brick Central Public Hall, to Yodoyabashi: a slow 40 minutes. From Yodoyabashi the Midosuji subway runs to Namba (about 6 minutes, ¥190, every few minutes).\n\n"
    "In the evening go to Dotonbori and Hozenji-yokocho; the Osaka map covers Dotonbori at night and dinner. Stay until 21:00 or 22:00.\n"
    "To Kyoto: Midosuji Line from Namba 21:39 (21:48 at weekends and on holidays) → change at Yodoyabashi to the Keihan limited express → Sanjo 22:41 (22:50), ¥680. By JR, the 21:39 Midosuji Line from Namba (weekdays) to Umeda and the 22:00 Special Rapid from Osaka reach Kyoto at 22:29, ¥820. The last is Namba 23:18 → Keihan limited express from Yodoyabashi 23:33 → Sanjo 0:22 (every day).")

# ---------------------------------------------------------------------------
# コース
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="osaka-sakura.json",
        note="「造幣局は午後の枠」コース（最初に開く）。梅田9:35（土日祝9:30）・なんば9:35（9:32）→天満橋→西の丸庭園→天守閣→玉造口→JO-TERRACE でお昼→造幣局15:00ごろの枠→毛馬桜之宮公園→天満で晩ごはん。",
        rows=[row("train", "行き：東梅田9:35発（土日祝9:30発）→ 天満橋9:40着（9:34着）・190円", "Out: Higashi-Umeda 9:35 (weekends and holidays 9:30) → Temmabashi 9:40 (9:34), ¥190"),
              row("train", "行き：なんば9:35発（土日祝9:32発）→ 谷町九丁目で乗り換え → 天満橋9:50着（9:46着）・240円", "Out: Namba 9:35 (weekends and holidays 9:32) → change at Tanimachi 9-chome → Temmabashi 9:50 (9:46), ¥240"),
              row("train", "京都から：三条9:40発（土日祝9:37発）の京阪特急 → 天満橋10:27着（10:25着）・490円", "From Kyoto: Keihan limited express, Sanjo 9:40 (weekends and holidays 9:37) → Temmabashi 10:27 (10:25), ¥490")],
        order=[
            ("temmabashi", "10:00〜10:10", "10:00–10:10",
             T("橋の上から大川を見たら、南へ歩いて大阪城の大手門へ（15分ほど）。京都から来た人は30分ほど遅れて着くので、天守閣を短めにすると、お昼から同じ時間割になります。",
               "Look at the river from the bridge, then walk south to the castle’s Otemon gate (about 15 minutes). Coming from Kyoto you arrive about 30 minutes later; keep the castle tower short and you are back on the same timetable by lunch.")),
            ("nishinomaru", "10:25〜11:25", "10:25–11:25",
             T("11:30ごろから天守閣へ（大手門から歩いて15分、中で1時間ほど）。12:30ごろ南東の玉造口へ歩いて（20分ほど）八重桜を見て、北東の JO-TERRACE OSAKA（JR大阪城公園駅の前）でお昼にします。玉造口から15〜20分。とんかつ、和定食、たこ焼き、お好み焼き、カフェなど11:00から開く店が並び、ゆっくりして14:30ごろまで。",
               "From about 11:30, the castle tower (15 minutes’ walk from the Otemon gate, about an hour inside). Around 12:30 walk to Tamatsukuri-guchi in the south-east (about 20 minutes) for the double cherries, then lunch at JO-TERRACE OSAKA by JR Osakajokoen Station in the north-east, 15–20 minutes on. Tonkatsu, set meals, takoyaki, okonomiyaki and cafés open from 11:00; take your time until about 14:30.")),
            ("mint", "15:00〜16:00", "15:00–16:00",
             T("JO-TERRACE から北へ、大阪城北詰のほうへ出て川崎橋を渡り、南門まで歩いて30分ほど。時間帯の少し前に着くようにします。15時台に申し込めなかった人へ：16〜17時台の枠なら、お昼のあとJO-TERRACE でゆっくりするか天守閣をあとに回し、そのぶん後ろにずらします。朝の枠の人は「朝いちばんの枠」のコースへ。\n\n"
               "歩き終わると北門から桜宮橋のたもとに出ます。",
               "From JO-TERRACE walk north to Osakajo-kitazume and cross Kawasaki-bashi bridge to the south gate, about 30 minutes; aim to arrive a little before your slot. If you couldn’t book a 15:00 slot: with a 16:00 or 17:00 slot, linger at JO-TERRACE or move the castle tower to after lunch and shift the rest later. With a morning slot, switch to the morning course.\n\n"
               "You come out of the north gate at the foot of Sakuranomiya bridge.")),
            ("kema", "16:00〜17:30", "16:00–17:30",
             T("桜宮橋を渡って東岸の遊歩道を上流（北）へ。夕方の光の中、対岸の桜と川を眺めながら歩き、適当なところで桜宮橋へ戻ります。JR桜ノ宮駅も近く、ここで帰ることもできます。",
               "Cross Sakuranomiya bridge and walk upstream (north) on the east-bank path in the late light, with blossom on the far bank, then turn back to the bridge when you like. JR Sakuranomiya Station is close if you want to leave here.")),
        ],
        sections=[dict(first="temmabashi", last="temmabashi", area=T("天満橋", "Temmabashi"), title=T("梅田・なんばから地下鉄で", "By subway from Umeda or Namba")),
                  dict(first="nishinomaru", last="nishinomaru", area=T("大阪城", "Osaka Castle"), title=T("午前は大阪城、お昼は JO-TERRACE", "The castle, then lunch at JO-TERRACE")),
                  dict(first="mint", last="mint", area=T("造幣局", "Japan Mint"), title=T("午後の枠で八重桜の道へ", "The cherry walk in an afternoon slot")),
                  dict(first="kema", last="kema", area=T("大川 → 天満", "Okawa → Tenma"), title=T("川沿いを歩いて、夜は天満で", "The riverside, then dinner in Tenma"))],
        after=AFTER_LATE, links_last=[L_YAHOO],
        gmaps_last=[gm("JR天満駅・天神橋筋商店街", "JR Tenma Station & Tenjinbashi-suji", 34.70470, 135.51240, "JR天満駅")],
        back=[row("train", "梅田へ：JR天満 → 大阪 3分・150円", "To Umeda: JR Tenma → Osaka, 3 min, ¥150"),
              row("train", "京都へ：JR天満21:03発（土日祝21:11発）→ 大阪で新快速 → 京都21:44着（21:49着）・750円", "To Kyoto: JR Tenma 21:03 (weekends and holidays 21:11) → Special Rapid from Osaka → Kyoto 21:44 (21:49), ¥750"),
              row("train", "最終：JR天満23:45発 → 京都0:30着／京阪 天満橋23:36発 → 三条0:22着（毎日同じ）", "Last: JR Tenma 23:45 → Kyoto 0:30 / Keihan Temmabashi 23:36 → Sanjo 0:22 (every day)")],
        notices_extra=dict(nishinomaru=[N_JOT]),
        hints=[("mint", {"none": ["nishinomaru"]},
                "大阪城に寄らないなら、天満橋駅から南門まで歩いて約15分です。お昼は天満橋か天満のあたりで。",
                "Skipping the castle: the south gate is about 15 minutes’ walk from Temmabashi Station. Have lunch around Temmabashi or Tenma."),
               ("kema", {"none": ["mint"]},
                "造幣局の申し込みが取れなかったら：天満橋駅から東岸の遊歩道を北へ、桜宮橋まで歩いて20〜25分。川沿いの桜並木は申し込みなしで歩けます。",
                "No Mint booking? Walk north from Temmabashi Station along the east-bank path to Sakuranomiya bridge, 20–25 minutes. The riverside trees need no booking.")],
    ),
    dict(
        id="early", file="osaka-sakura-early.json",
        note="「造幣局は朝いちばんの枠」コース。平日は東梅田9:17・なんば9:15（土日祝は8:25・8:18）→天満橋→造幣局 平日10:00（土日祝9:00）の枠→毛馬桜之宮公園→JO-TERRACE でお昼→玉造口→天守閣→西の丸庭園→中之島→夜の道頓堀。",
        rows=[row("train", "行き（平日10:00の枠）：東梅田9:17発 → 天満橋9:22着・190円／なんば9:15発 → 天満橋9:28着・240円", "Out (weekday 10:00 slot): Higashi-Umeda 9:17 → Temmabashi 9:22, ¥190 / Namba 9:15 → Temmabashi 9:28, ¥240"),
              row("train", "行き（土日祝9:00の枠）：東梅田8:25発 → 天満橋8:30着／なんば8:18発 → 天満橋8:33着", "Out (weekend 9:00 slot): Higashi-Umeda 8:25 → Temmabashi 8:30 / Namba 8:18 → Temmabashi 8:33"),
              row("train", "京都から：三条8:32発（土日祝7:49発）の京阪特急 → 天満橋9:23着（8:38着）・490円", "From Kyoto: Keihan limited express, Sanjo 8:32 (weekends and holidays 7:49) → Temmabashi 9:23 (8:38), ¥490")],
        order=[
            ("temmabashi", "9:25（土日祝8:30）", "9:25 (weekends 8:30)",
             T("天満橋を渡って川沿いを上流へ、造幣局の南門まで歩いて約15分（造幣局の案内）。入口で手荷物の検査があるので、時間帯の少し前に着くようにします。",
               "Cross Temmabashi bridge and follow the river upstream to the Mint’s south gate, about 15 minutes (the Mint’s guide). Bags are checked at the gate, so arrive a little before your slot.")),
            ("mint", "10:00〜11:00（土日祝9:00〜10:00）", "10:00–11:00 (weekends 9:00–10:00)",
             T("一日の最初の枠です。歩き終わると北門から桜宮橋のたもとに出ます。土日祝は1時間早く終わるので、このあとの時間に余裕ができます。",
               "The first slot of the day. You come out of the north gate at the foot of Sakuranomiya bridge. At weekends you finish an hour earlier, which leaves spare time later.")),
            ("kema", "11:00〜11:45", "11:00–11:45",
             T("桜宮橋を渡って東岸の遊歩道を下流（南）へ。川崎橋のあたりで川を離れ、大阪城北詰のほうから大阪城公園へ入って、JR大阪城公園駅の前の JO-TERRACE OSAKA でお昼にします（桜宮橋から30〜35分）。とんかつ、和定食、たこ焼き、お好み焼き、カフェなど11:00から開く店が並びます。土日祝は時間が余るので、先に天守閣に上がってからお昼でも。",
               "Cross Sakuranomiya bridge and walk downstream (south) on the east-bank path. Leave the river around Kawasaki-bashi bridge, enter Osaka Castle Park from the Osakajo-kitazume side and have lunch at JO-TERRACE OSAKA by JR Osakajokoen Station (30–35 minutes from the bridge). Tonkatsu, set meals, takoyaki, okonomiyaki and cafés open from 11:00. At weekends you have time in hand, so you can go up the castle tower before lunch.")),
            ("nishinomaru", "15:05〜16:05", "15:05–16:05",
             T("お昼のあと13:10ごろ JO-TERRACE を出て、南東の玉造口の八重桜へ（15〜20分）。そこから天守閣へ歩いて（20分ほど）、13:50〜14:50ごろ天守閣。15:05ごろ西の丸庭園に入ります（入園は16:30まで）。",
               "Leave JO-TERRACE about 13:10 for the double cherries at Tamatsukuri-guchi (15–20 minutes), then walk to the castle tower (about 20 minutes) and go up from about 13:50 to 14:50. Enter Nishinomaru Garden about 15:05 (last entry 16:30).")),
        ],
        sections=[dict(first="temmabashi", last="temmabashi", area=T("天満橋", "Temmabashi"), title=T("朝の地下鉄で", "By morning subway")),
                  dict(first="mint", last="mint", area=T("造幣局", "Japan Mint"), title=T("いちばん最初の枠で八重桜の道へ", "The cherry walk in the first slot")),
                  dict(first="kema", last="kema", area=T("大川", "Okawa"), title=T("川沿いを歩いて大阪城へ、お昼は JO-TERRACE", "Along the river to the castle, lunch at JO-TERRACE")),
                  dict(first="nishinomaru", last="nishinomaru", area=T("大阪城 → 中之島 → 道頓堀", "Castle → Nakanoshima → Dotonbori"), title=T("午後は大阪城、夜は道頓堀", "The castle, then Dotonbori at night"))],
        after=AFTER_EARLY, links_last=[L_OSAKA, L_YAHOO],
        gmaps_last=[gm("中之島公園", "Nakanoshima Park", 34.69300, 135.51200, "中之島公園"),
                    gm("大阪市中央公会堂", "Osaka City Central Public Hall", 34.69250, 135.50460, "大阪市中央公会堂")],
        back=[row("train", "淀屋橋 → なんば：御堂筋線 約6分・190円", "Yodoyabashi → Namba: Midosuji Line, about 6 min, ¥190"),
              row("train", "京都へ：なんば21:39発（土日祝21:48発）→ 淀屋橋で京阪特急 → 三条22:41着（22:50着）・680円", "To Kyoto: Namba 21:39 (weekends and holidays 21:48) → Keihan limited express from Yodoyabashi → Sanjo 22:41 (22:50), ¥680"),
              row("train", "最終：なんば23:18発 → 淀屋橋23:33発の京阪特急 → 三条0:22着（毎日同じ）", "Last: Namba 23:18 → Keihan from Yodoyabashi 23:33 → Sanjo 0:22 (every day)")],
        notices_extra=dict(kema=[N_JOT]),
        hints=[("nishinomaru", {"none": ["kema"]},
                "川沿いを歩かないなら、北門を出たら JR大阪城北詰駅のほうへ歩いて大阪城公園へ。JO-TERRACE まで30分ほどです。",
                "Skipping the riverside: from the north gate walk toward JR Osakajo-kitazume and into the castle park, about 30 minutes to JO-TERRACE.")],
    ),
]

# ---------------------------------------------------------------------------
# 出典（時刻・料金・条件）
# ---------------------------------------------------------------------------


def yurl(frm, to, ymd, hm, typ=1):
    q = dict([("from", frm), ("to", to), ("y", ymd[:4]), ("m", ymd[4:6]), ("d", ymd[6:]), ("hh", hm[:2]), ("m1", hm[2]), ("m2", hm[3]), ("type", typ),
              ("ticket", "ic"), ("expkind", 1), ("ws", 3), ("s", 0)])
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(q)


def src(what, url):
    return {"what": what, "url": url, "checked": CHECKED}


WD, SA = "20261202", "20261205"
SOURCES = [
    src("造幣局 桜の通り抜け 2026年（令和8年）：4/9〜4/15の7日間、平日10:00〜19:15・土日9:00〜19:15、19:45完全退場、事前申込の2次元コードで入場、申し込んだ時間帯に入場、飲食禁止・全面禁煙・手荷物検査、日傘・自撮り棒・三脚・自転車・ペット不可、駐車場なし、天満橋（京阪 東改札14番出口・谷町線 北改札2号出口）とJR大阪城北詰3番出口から徒歩約15分、造幣博物館 4/8〜4/15休館", MINT),
    src("造幣局 桜の通り抜けのデータ：全長約560m、明治16年（1883）から、令和8年の今年の花は御衣黄、令和8年の来場者181千人（事前予約制）", MINT_DATA),
    src("2026年3月10日の報道（共同通信）：4/9〜15、140品種331本、専用サイトで事前申込、3月18日9:00受付開始、時間帯ごとに定員・先着順", MINT_NEWS),
    src("西の丸庭園：3〜10月9:00〜17:00（入園は閉園30分前まで）、月曜休み（祝日なら翌日）、12/28〜1/4休み、大人300円、観桜期は時間と料金が異なる、約300本・標本木", NISHI),
    src("西の丸庭園 入園料：2026年4月1日から大人300円。観桜ナイター期（3月下旬〜4月上旬）は350円を継続、開催時期は毎年告知（2025-11-17のお知らせ）", NISHI_FEE),
    src("大阪城公園の桜：約3000本、西の丸庭園はソメイヨシノ中心に約300本、玉造口に遅咲きの八重桜", SAKURA),
    src("大阪城公園 よくある質問：公園は24時間、食事は JO-TERRACE OSAKA（大阪城公園駅前）とミライザ大阪城", PARK_FAQ),
    src("大阪城天守閣：9:00〜18:00（入館は閉館30分前まで）、12/28〜1/1休館、大人1,200円（大阪観光局）", TENSHU),
    src("JO-TERRACE OSAKA：かつ満・さち福や 11:00〜21:00、たこ焼道楽わなか 11:00〜18:00 月曜休み（祝日は営業）、名代 千房 平日11:00〜18:00・土日祝〜20:00 月曜休み、スターバックス 平日7:00〜・土日祝8:00〜22:00 ほか", JOT),
    src("毛馬桜之宮公園：毛馬洗い堰から天満橋までの河川敷、約4,500本、常時開園（大阪観光局）", KEMA),
    src("谷町線 東梅田→天満橋（平日）：9:35発→9:40着、9:17発→9:22着、190円", yurl("東梅田", "天満橋", WD, "0930")),
    src("谷町線 東梅田→天満橋（土）：9:30発→9:34着、8:25発→8:30着、190円", yurl("東梅田", "天満橋", SA, "0930")),
    src("なんば→天満橋（平日）：9:35発→谷町九丁目→9:50着、9:15発→9:28着、240円", yurl("なんば(地下鉄)", "天満橋", WD, "0935")),
    src("なんば→天満橋（土）：9:32発→9:46着、8:18発→8:33着、240円", yurl("なんば(地下鉄)", "天満橋", SA, "0930")),
    src("京阪 三条→天満橋（平日）：特急9:40発→10:27着、8:32発→9:23着、490円", yurl("三条(京都府)", "天満橋", WD, "0930")),
    src("京阪 三条→天満橋（土）：特急9:37発→10:25着、7:49発→8:38着、490円", yurl("三条(京都府)", "天満橋", SA, "0930")),
    src("JR 天満→京都（平日）：21:03発→大阪で新快速→21:44着、750円。天満→大阪 3分・150円", yurl("天満(大阪府)", "京都", WD, "2100")),
    src("JR 天満→京都（土）：21:11発→21:49着、750円", yurl("天満(大阪府)", "京都", SA, "2100")),
    src("JR 天満→京都 最終（平日・土）：23:45発→大阪0:00発の新快速→京都0:30着", yurl("天満(大阪府)", "京都", WD, "2359", 2)),
    src("京阪 天満橋→三条 最終（平日・土）：特急23:36発→0:22着、490円", yurl("天満橋", "三条(京都府)", WD, "2359", 2)),
    src("天満→なんば：扇町まで徒歩4分、堺筋線で日本橋へ（約10分）、240円", yurl("天満(大阪府)", "なんば", WD, "2100")),
    src("淀屋橋→なんば：御堂筋線 18:00発→18:06着、190円", yurl("淀屋橋", "なんば", WD, "1800")),
    src("なんば→三条（平日）：21:39発→淀屋橋21:50発の京阪特急→22:41着、680円", yurl("なんば(地下鉄)", "三条(京都府)", WD, "2135")),
    src("なんば→三条（土）：21:48発→淀屋橋22:00発の京阪特急→22:50着、680円", yurl("なんば(地下鉄)", "三条(京都府)", SA, "2135")),
    src("なんば→京都（平日）：21:39発→梅田→大阪22:00発の新快速→22:29着、820円", yurl("なんば(地下鉄)", "京都", WD, "2135")),
    src("なんば→三条 最終（平日・土）：地下鉄なんば23:18発→淀屋橋23:33発の京阪特急→0:22着", yurl("なんば", "三条(京都府)", WD, "2359", 2)),
    src("歩く時間（OpenStreetMap の徒歩ルートの目安。文章では長めに）：天満橋駅→大手門10分、大手門→天守閣12分、天守閣→玉造口15分、玉造口→JO-TERRACE 14分、JO-TERRACE→造幣局南門24分、桜宮橋（東）→JO-TERRACE 25分、北門→天神橋筋（天満）17〜22分、天満橋駅→中之島公園→中央公会堂→淀屋橋 約30分", "https://routing.openstreetmap.de/"),
]

NOTE_HEAD = ("大阪 造幣局の桜の通り抜けのルート（osaka-sakura/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、"
             "コースごとに別のファイルを読む（osaka-sakura.json＝造幣局は午後の枠、osaka-sakura-early.json＝朝いちばんの枠）。起点は大阪の梅田〜難波のホテル。このファイル：")
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（2025年4月9日、2026年4月8日の夜の西の丸庭園、2026年4月14日の造幣局。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "造幣局の日程・時間・申し込みは2026年の実績で、来春は要確認。info.source は確認した出典、info.checked は確認日、sources は時刻・料金の出典の一覧。このファイルは scripts/build_osaka_sakura_data.py で作る（直接直さない）。")
TRANSIT_TIP = T("電車は乗換案内で平日と土曜（2026年12月の時刻）を確認しました。春までに変わることがあるので要確認。歩く時間は少しゆったりめです。",
                "Trains checked on a route planner for a weekday and a Saturday (December 2026 timetable); they may change by spring. Walking times are rounded up a little.")


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    last = order[-1][0]
    spots = []
    for sid, tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body, rows, tip, source = b.pop("body"), b.pop("_rows"), b.pop("_tip"), b.pop("_source")
        first = NO[sid] == 1
        b["notices"] = OFF_SEASON + b["notices"] + c["notices_extra"].get(sid, [])
        ja = body["ja"] + "\n\n" + go["ja"] + f"\n\n{VIS[0]}：{tj}"
        en = body["en"] + "\n\n" + go["en"] + f"\n\n{VIS[1]}: {te}"
        if first:
            rows = c["rows"] + rows
        if sid == last:
            rows = rows + c["back"]
            ja += "\n\n" + c["after"]["ja"]
            en += "\n\n" + c["after"]["en"]
            b["links"] += [x for x in c["links_last"] if x not in b["links"]]
            b["gmaps"] += c["gmaps_last"]
        if first or sid == last:
            tip = T(tip["ja"] + ("" if first and sid == "temmabashi" else TRANSIT_TIP["ja"]), tip["en"] + ("" if first and sid == "temmabashi" else " " + TRANSIT_TIP["en"]))
        if sid in ("nishinomaru", "kema") and any(x["url"] == JOT for x in b["notices"]):
            b["links"] = b["links"] + [L_JOT]
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out.update(info={"rows": rows, "cash": False, "tip": tip, "checked": CHECKED, "source": source},
                   text=T(ja, en), photos=photos(sid))
        spots.append(out)
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    picks = [NO[x[0]] for x in order if x[0] != "temmabashi"]
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": [dict(s, first=NO[s["first"]], last=NO[s["last"]]) for s in c["sections"]],
        "plan": {"_note": "「選んで回る」の設定。最初は「全部回る」。天満橋駅（スタート）はいつも入る。外したときの回り方は hints。",
                 "picks": picks, "auto": {str(NO["temmabashi"]): {"always": True}}, "defaultPicks": picks,
                 "hints": [{"spot": NO[sid], "rule": rule(r), "from": None, "to": None, "text": T(ja, en)} for sid, r, ja, en in c["hints"]]},
        "photoBase": f"../images/{MAP_ID}/",
        "sources": SOURCES,
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


if __name__ == "__main__":
    for c in COURSES:
        build(c)
