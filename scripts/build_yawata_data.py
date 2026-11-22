#!/usr/bin/env python3
"""京都 淀・八幡の桜（淀水路の河津桜・石清水八幡宮・背割堤）のデータを、3つのコース分まとめて書き出す。

使い方: python3 scripts/build_yawata_data.py  （そのあと python3 scripts/sync_yawata.py）
- 作るもの（COURSES）:
  - data/routes/yawata.json … 「3月：淀の河津桜」（kawazu）。9:30ごろ三条→淀水路→淀城跡→八幡でお昼→石清水八幡宮→
    走井餅→展望塔→伏見で晩ごはん→三条・先斗町
  - data/routes/yawata-sakura.json … 「4月：背割堤の桜」（sakura）。9:30ごろ三条→石清水八幡宮→お昼→展望塔→背割堤→走井餅→
    祇園白川・円山公園の夜桜
  - data/routes/yawata-early.json … 「4月：背割堤の開園へ」（early）。8:10ごろ三条→展望塔9:00→背割堤→走井餅でひと休み→
    石清水八幡宮→遅めのお昼→伏見（月桂冠）→夜桜
  どれも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容
  - COURSES … コースごとの並び順、めやすの時間、行き方、最後のスポットに続ける夕方と夜、「選んで回る」の設定
  - SOURCES … 時刻・料金の出典と確認日（データの sources に入る）
- 春の日程・料金で書いてあるものは全部「2026年春の実績」。次の春の発表が出たら、文章と SOURCES を直す
  （背割堤さくらまつり・展望塔の料金・石清水八幡宮の特別公開・淀本町商店街の桜まつり・夜桜のライトアップ）
- 時刻は2026年8月22日改正の京阪のダイヤ。春までに改正があったら乗換案内で確かめ直す
- 出発地は京都の中心・三条のあたり（京阪 三条駅）。宿の名前は書かない
- 写真は images/yawata/<スポットのid>-<番号>.jpg を番号の順に全部使う（足していない）。
  淀城跡・走井餅・朝日屋・伏見・祇園は写真がないので、スポットにせず文章で案内する
- 2026-11-22 オーナーの基準で作り直した（ゲストが実際に回れる1日。咲く時期で分け、混む背割堤は開園のコースも）
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "yawata"
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


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


YAHOO = "https://transit.yahoo.co.jp/"
YODO = "https://totteoki.kyoto.travel/28467/"
YODO_FES = "https://totteoki.kyoto.travel/events/11848/"
CABLE = "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
IWA = "https://iwashimizu.or.jp/"
IWA_NAVI = "https://www.kankou-yawata.org/?shuhen_jinja=%e7%9f%b3%e6%b8%85%e6%b0%b4%e5%85%ab%e5%b9%a1%e5%ae%ae"
IWA_QA = "https://iwashimizu.or.jp/qa/"
IWA_WALK = "https://www.kankou-yawata.org/course_omoteurasando.html"
SPRING_GUIDE = "https://totteoki.kyoto.travel/wp-content/uploads/2026/03/kyotoyawatasansaku-chirashi_compressed.pdf"
PARK = "https://www.yodogawa-park.jp/annai/sewaritei/"
PARK_HOURS = "https://www.yodogawa-park.jp/cms/wp-content/uploads/2025/04/1a70aa284aa3d9b47315d6a7958e48e8.pdf"
PARK_RULES = "https://www.yodogawa-park.jp/riyouannai/riyou/"
FES = "https://www.yodogawa-park.jp/sakurafes/"
FES_2026 = "https://www.yodogawa-park.jp/cms/wp-content/uploads/2026/03/bb7e63930cdcd26969e16163becee2c9.pdf"
DEAIKAN = "https://www.yodogawa-park.jp/sansen/"
DEAIKAN_SHOP = "https://www.yodogawa-park.jp/sansen/style/sakura-shop-open2020/"
SEWARI_NAVI = "https://www.kankou-yawata.org/?shuhen_jinja=%e8%83%8c%e5%89%b2%e5%a0%a4"
ASAHIYA = "https://sabasusi-asahiya.com/shop/"
HASHIRII = "http://www.yawata-hashiriimochi.com/access/"
YAWATA_FOOD = "https://www.kankou-yawata.org/syokujionly/"
GEKKEIKAN = "https://www.gekkeikan.co.jp/enjoy/museum/access/"
KIZAKURA = "https://kizakura.co.jp/restaurant/country/"
MARUYAMA = "https://ja.kyoto.travel/event/single.php?event_id=4081"
NIGHT = "https://ja.kyoto.travel/times/night/article/single.php?id=472"

L_YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", YAHOO)
L_UJI = link("info", "宇治と伏見のマップ（酒蔵の町）", "Uji & Fushimi map (the sake town)", "../uji/#list")
L_EIZAN = link("info", "叡山電鉄のマップ（夜の祇園四条・先斗町は24〜26番）", "Eizan Railway map (evening stops 24–26)", "../eizan-line/#list")
L_ASAHIYA = link("official", "朝日屋（時間・休み）", "Asahiya: hours and closing days (Japanese)", ASAHIYA)
L_HASHIRII = link("official", "やわた走井餅老舗（時間・休み）", "Hashiriimochi: hours and closing days (Japanese)", HASHIRII)
L_KIZAKURA = link("official", "キザクラカッパカントリー（時間・休み）", "Kizakura Kappa Country: hours (Japanese)", KIZAKURA)
L_GEKKEIKAN = link("official", "月桂冠大倉記念館（時間・予約）", "Gekkeikan Okura Sake Museum: hours and booking", GEKKEIKAN)
L_NIGHT = link("info", "2026年春の夜桜ライトアップ（京都観光Navi）", "Evening cherry light-ups in spring 2026 (Japanese)", NIGHT)

# ---------------------------------------------------------------------------
# お知らせ
# ---------------------------------------------------------------------------
OFF_JA = "3月〜4月上旬に使う春のマップです。いまは見ごろの時期ではありません。日程・料金は2026年春の実績、電車は2026年11月の時刻です。来春は要確認。"
OFF_EN = "This map is for March to early April and the blossoms aren’t at their best now. Dates and fees are from spring 2026 and train times from November 2026, so please check for next spring."
OFF_SEASON = [
    notice("春のマップです", "A spring map", OFF_JA, OFF_EN, to="2027-02-28"),
    notice("春のマップです", "A spring map", OFF_JA, OFF_EN, frm="2027-04-16"),
]

N_YODO = notice(
    "トイレは淀駅の改札を出る前に", "Use the toilet before leaving Yodo Station",
    "淀駅の改札の外にトイレはなく、水路沿いにも天神橋の近くに1か所だけです。ごみ箱もないので持ち帰ってください。火を使うのは禁止です。",
    "There are no toilets outside the station’s ticket gates and only one along the canal, near Tenjin-bashi. There are no bins, so take your litter with you. No fires.",
    url=YODO)
N_IWA = notice(
    "ケーブルの最終は18:15、階段もあります", "Last cable car 18:15, and some steps",
    "毎時15分・45分発（朝は8:10から）。00分・30分は乗る人がいるときだけです。山上駅から本殿までにも階段が少しあります。表参道を歩いて下りると石段と坂で30〜35分です。",
    "Departures at :15 and :45 (from 8:10); :00 and :30 only run when there are passengers. There are a few steps up to the main hall. Walking down the main approach takes 30–35 minutes of steps and slopes.",
    url=CABLE)
N_IWA_SPRING = notice(
    "春の特別公開（2026年の実績）", "Spring special opening (as held in 2026)",
    "2026年は3月20日〜4月12日、受付9:00〜16:00、大人1,000円・中高生500円で国宝の本社が公開されました。来春にあるかどうかと日程は要確認です。境内のお参りは無料です。",
    "In 2026 the National Treasure main buildings opened from 20 March to 12 April, entry 9:00–16:00, ¥1,000 adults and ¥500 for junior and senior high. Please check whether and when it runs next spring. The grounds are free.",
    url=SPRING_GUIDE)
N_PARK = notice(
    "開園は9:00〜17:00、車は止められません", "Open 9:00–17:00, and no parking",
    "背割堤地区の開園は9:00〜17:00です（公園の開園時間表）。さくらまつりの前後は駐車場も閉まるので電車で。堤防の上の道は、自転車を押して歩くのも禁止です。ごみは持ち帰りです。",
    "The Sewaritei section of the park opens 9:00–17:00 (park timetable). Parking shuts around the festival, so come by train. Bicycles can’t be taken along the top path, even pushed. Take your litter home.",
    url=PARK)
N_FES = notice(
    "さくらまつり（2026年の実績）", "Cherry festival (as held in 2026)",
    "2026年は3月28日〜4月5日、9:00〜17:00。入場のときに運営協力金（1人100円以上、6歳未満は不要）があり、屋台のさくらマルシェに40店舗が出ました。来春の日程と金額は要確認。支払い方法も書かれていないので、小銭があると安心です。",
    "In 2026 it ran 28 March – 5 April, 9:00–17:00, with a contribution of ¥100 or more on entry (not for under-6s) and a market of 40 stalls. Please check next spring’s dates and amount. Payment methods aren’t stated, so carry some coins.",
    url=FES_2026)
N_TOWER = notice(
    "展望塔の最終受付は16:20", "Last entry to the tower 16:20",
    "展望塔は9:00〜16:30。ふだんは無料ですが、混む時期は有料になります。2026年のさくらまつりの間は大人300円・子ども100円でした（来春は要確認）。雪などの天気で止まることもあります。",
    "The tower is open 9:00–16:30. It is usually free but charges at busy times: ¥300 adults and ¥100 children during the 2026 festival (please check for next spring). It can close in bad weather, such as snow.",
    url=DEAIKAN)
N_MARCH_TOWER = notice(
    "3月の背割堤は、まだ咲いていません", "Sewaritei won’t be in bloom in March",
    "写真に写っている桜は、3月末〜4月上旬に咲くソメイヨシノです。3月の河津桜の時期は、3つの川と京都の町を眺める場所として寄ります。",
    "The blossom in the photos is Somei-Yoshino, which opens in late March to early April. In the Kawazu season you come here for the view of three rivers and the city.")
N_SHOPS = notice(
    "月曜・火曜はお昼の店に注意", "Lunch on Mondays and Tuesdays",
    "駅前の朝日屋は月・火が休み（祝日は営業）、走井餅老舗は月曜が休み（祝日なら翌日）です。月曜はお弁当を買ってから電車に乗ってください。",
    "Asahiya by the station closes Mondays and Tuesdays (open on holidays) and Hashiriimochi on Mondays (the next day if a holiday). On Mondays buy a packed lunch before you take the train.",
    url=ASAHIYA)

# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    yodo=dict(
        name=T("淀水路の河津桜", "Kawazu cherries along the Yodo canal"), kind=T("桜（3月）", "Cherries (March)"),
        blurb=T("住宅地を流れる細い水路に、約1.3km、約300本。ソメイヨシノより1か月ほど早く咲く、濃いピンクの桜です。",
                "About 300 trees for 1.3 km along a narrow canal through a quiet neighbourhood: deep pink, a month ahead of the Somei-Yoshino."),
        caution=T("見ごろは3月上旬〜中旬。改札の外にトイレなし", "Best early to mid March. No toilets outside the station"),
        lat=34.90250, lng=135.71700,
        body=T("淀水路（よどすいろ）の河津桜\n\n"
               "淀駅の中央改札を出て1階の「出口4」へ。高架沿いを西へ歩いて約10分で、並木の西の端（淀緑地西詰）です。北改札や競馬場側の改札から出ると遠回りになります。\n\n"
               "東の端までゆっくり歩いて30分。道は橋で右岸と左岸に移ります。橋の上から見下ろすと、水路の両側の花が一度に入ります。住宅のすぐ横なので静かに。\n\n"
               "2月はじめに咲きはじめ、例年の見ごろは3月上旬〜中旬です。満開は2026年が3月7日ごろ、2025年は遅くて3月21日ごろでした（京都市観光協会）。満開のあと1週間〜10日ほど楽しめます。2026年は3月27日には葉桜でした。写真は2026年3月23日、散りはじめたころです。",
               "Kawazu cherries along the Yodo canal\n\n"
               "Leave Yodo Station by the central gate and take Exit 4 on the ground floor. Follow the viaduct west for about 10 minutes to the west end of the avenue. The north and racecourse-side gates take you the long way round.\n\n"
               "It’s a slow 30 minutes to the east end, with the path switching banks at the bridges. From a bridge you get the blossom on both sides at once. Homes are right beside it, so keep your voice down.\n\n"
               "Flowers start in early February and are usually best in early to mid March. Full bloom was around 7 March in 2026 and a late 21 March in 2025 (Kyoto City Tourism Association), and lasts a week to ten days. By 27 March 2026 the trees had gone to leaf. My photos are from 23 March 2026, as the petals began to fall."),
        gmaps=[gm("淀水路 河津桜", "Yodo canal Kawazu cherries", 34.90250, 135.71700, "淀水路 河津桜"),
               gm("京阪 淀駅", "Keihan Yodo Station", 34.90591, 135.71997, "京阪 淀駅")],
        links=[link("official", "淀の河津桜（京都市観光協会）", "Yodo Kawazu cherries (Kyoto City tourism, Japanese)", YODO)],
        notices=[N_YODO],
        _rows=[row("hours", "いつでも見られる。例年の見ごろは3月上旬〜中旬", "Open at any time. Usually best in early to mid March"),
               row("fee", "無料", "Free")],
        _tip=T("京都市観光協会の案内で確認しました。満開日は年によって2週間ほどずれるので、出かける前に開花情報を見てください。",
               "Checked with the Kyoto City Tourism Association. Full bloom can shift by two weeks, so check the bloom report before you go."),
        _source=f"京都市観光協会「淀水路の河津桜2026」 {YODO}。2026-11-22に確認"),
    iwashimizu=dict(
        name=T("石清水八幡宮", "Iwashimizu Hachimangu"), kind=T("神社（国宝）", "Shrine (National Treasure)"),
        blurb=T("男山の上に建つ、朱と金の国宝の社殿。行きはケーブル、帰りは竹と木立の表参道を歩きます。",
                "A vermilion-and-gold National Treasure on Mt. Otokoyama: up by cable car, down on foot through bamboo and woods."),
        caution=T("ケーブルは18:15まで。歩いて下りると石段", "Cable car until 18:15. Stone steps on the walk down"),
        lat=34.87973, lng=135.70005,
        body=T("石清水八幡宮（いわしみずはちまんぐう）\n\n"
               "859年に始まった「やわたのはちまんさん」。今の社殿は徳川家光の造替で、本社10棟が国宝です。本殿の欄間（らんま）には極彩色の彫刻が並びます。織田信長が寄進したと伝わる黄金の雨樋は、ふだんは非公開です。\n\n"
               "駅の隣からケーブルで3分（片道300円）、山上駅から歩いて5分ほど。本殿から展望台までも約5分で、3つの川の向こうに京都の町が見えます。\n\n"
               "帰りは歩いて下りるのがおすすめです。エジソン記念碑（電球のフィラメントに男山の竹が使われた縁）、一ッ石、二ノ鳥居を通り、一ノ鳥居まで30〜35分。麓の高良神社は、徒然草の「仁和寺にある法師」が、ここが八幡宮だと思って帰ってしまった場所です。\n\n"
               "山上のトイレは、ケーブルから上がる東参道の左手と、南総門の手前左の建物の裏の2か所です。",
               "Iwashimizu Hachimangu\n\n"
               "Founded in 859. The present buildings were rebuilt under the shogun Tokugawa Iemitsu and ten are National Treasures, with brightly painted carvings on the main hall. The golden gutter said to be Oda Nobunaga’s gift isn’t normally on view.\n\n"
               "The cable car next to the station takes 3 minutes (¥300 one way), then it’s about 5 minutes’ walk. The lookout, 5 minutes from the main hall, faces Kyoto across three rivers.\n\n"
               "Walk down if you can: past the Edison monument (Otokoyama bamboo made his light-bulb filaments), the Hitotsu-ishi stone and the second torii, 30–35 minutes to the first torii. Kora Shrine at the foot is where the monk in the 14th-century “Essays in Idleness” turned back, thinking he had seen the whole shrine.\n\n"
               "There are two toilets on the hill: left of the east approach from the cable car, and behind the building to the left before the south gate."),
        gmaps=[gm("石清水八幡宮", "Iwashimizu Hachimangu", 34.87973, 135.70005, "石清水八幡宮"),
               gm("ケーブル八幡宮口駅", "Cable Hachimangu-guchi", 34.88449, 135.69947, "ケーブル八幡宮口")],
        links=[link("official", "石清水八幡宮 公式サイト", "Iwashimizu Hachimangu (official)", IWA),
               link("timetable", "参道ケーブルの時刻表（京阪）", "Sando cable car timetable (Keihan, Japanese)", CABLE),
               L_ASAHIYA, L_HASHIRII],
        notices=[N_IWA, N_IWA_SPRING, N_SHOPS],
        _rows=[row("hours", "6:00〜18:00（正月は変わる）", "6:00–18:00 (different at New Year)"),
               row("fee", "境内は無料。春の特別公開は別（2026年は大人1,000円。来春は要確認）", "Grounds free. Spring special opening extra (¥1,000 in 2026; please check for next spring)"),
               row("cable", "8:10〜18:15、毎時15分・45分発（00分・30分は不定期）。毎日同じ。片道300円・往復600円", "8:10–18:15 at :15 and :45 (:00 and :30 irregular), same every day. ¥300 one way, ¥600 return"),
               row("hours", "朝日屋（駅前・鯖寿司）11:00〜17:00、月・火休み（祝日は営業）", "Asahiya (by the station, mackerel sushi) 11:00–17:00, closed Mon and Tue (open on holidays)"),
               row("hours", "走井餅老舗（一ノ鳥居前）9:00〜17:30、喫茶は17:00ラストオーダー、月曜休み（祝日なら翌日）", "Hashiriimochi (by the first torii) 9:00–17:30, tearoom last order 17:00, closed Mon (next day if a holiday)")],
        _tip=T("神社・京阪・お店の公式サイトと八幡市観光協会で確認しました。お店の支払い方法は書かれていません（要確認）。",
               "Checked on the shrine, Keihan and shop websites and with the Yawata tourism association. The shops don’t state payment methods (please check)."),
        _source=f"石清水八幡宮 公式サイト {IWA}、八幡市観光協会 {IWA_NAVI}、京阪 {CABLE}、朝日屋 {ASAHIYA}、走井餅老舗 {HASHIRII}。2026-11-22に確認"),
    sewaritei=dict(
        name=T("背割堤の桜並木", "Sewaritei cherry avenue"), kind=T("桜（3月末〜4月上旬）", "Cherries (late Mar – early Apr)"),
        blurb=T("木津川と宇治川を分ける細い堤防に、約1.4km、約220本のソメイヨシノのトンネルです。",
                "A tunnel of about 220 Somei-Yoshino, 1.4 km long, on the narrow levee that divides the Kizu and Uji rivers."),
        caution=T("開園9:00〜17:00。昼は人が多い", "Open 9:00–17:00. Crowded around midday"),
        lat=34.89000, lng=135.69300,
        body=T("背割堤（せわりてい）の桜並木\n\n"
               "行きは堤防の上の道で桜のトンネルをくぐり、帰りは下の芝生から。川と並木が広く入ります。先端まで行って戻ると約2.8km、写真を撮りながらで1時間〜1時間半です。途中で引き返してもかまいません。まつりの間は、現地の通行の案内に従ってください。\n\n"
               "見ごろは3月末〜4月上旬ごろで、年によって前後します。八幡市観光協会によると約20万人が訪れる名所です。写真は2026年4月8日、さくらまつりが終わった3日後です。まつりの日程を過ぎても咲いていることがあります。",
               "Sewaritei cherry avenue\n\n"
               "Go out along the top path through the tunnel and come back on the grass below, where the river and the whole row fit in one view. To the tip and back is about 2.8 km, one to one and a half hours with photos; turn back earlier if you like. During the festival follow the signs for which way to walk.\n\n"
               "It is best around late March to early April, varying by year. The Yawata tourism association says it draws about 200,000 people. My photos are from 8 April 2026, three days after that year’s festival ended: blossom can outlast the festival dates."),
        gmaps=[gm("背割堤", "Sewaritei", 34.89000, 135.69300, "背割堤 桜")],
        links=[link("official", "淀川河川公園 背割堤地区", "Yodogawa River Park, Sewaritei (Japanese)", PARK),
               link("official", "京都やわた背割堤さくらまつり", "Sewaritei cherry festival", FES, FES + "en/")],
        notices=[N_PARK, N_FES],
        _rows=[row("hours", "9:00〜17:00（公園の開園時間表、2025年4月時点）。時間外に歩けるかは要確認", "9:00–17:00 (park timetable as of April 2025). Please check whether you can walk it outside those hours"),
               row("fee", "無料。さくらまつりの間は運営協力金（2026年は1人100円以上。来春は要確認）", "Free. A contribution during the festival (¥100 or more in 2026; please check for next spring)")],
        _tip=T("淀川河川公園の公式サイト・開園時間表・2026年の報道資料と、八幡市観光協会で確認しました。",
               "Checked on the park website, its timetable and 2026 press release, and with the Yawata tourism association."),
        _source=f"淀川河川公園 {PARK}・{PARK_HOURS}・{FES_2026}、八幡市観光協会 {SEWARI_NAVI}。2026-11-22に確認"),
    deaikan=dict(
        name=T("さくらであい館（展望塔）", "Sakura Deaikan (observation tower)"), kind=T("展望塔", "Lookout tower"),
        blurb=T("高さ約25mの展望塔から、3つの川と、まっすぐ延びる背割堤を見下ろします。",
                "From the 25 m tower, look down on three rivers and the straight line of Sewaritei."),
        caution=T("展望塔の最終受付は16:20", "Last entry to the tower 16:20"),
        lat=34.89042, lng=135.70148,
        body=T("さくらであい館\n\n"
               "背割堤の入口、石清水八幡宮駅から御幸橋（ごこうばし）を渡って歩いて10〜15分。展望塔はエレベーターで上がれ、宇治川・木津川・桂川が淀川になるあたりと、まっすぐ延びる並木を見下ろせます。\n\n"
               "館内にトイレ、自販機、コインロッカー（開館中だけ）、売店があります。パンとお寿司の販売は土日などだけで、9:30〜16:00です。",
               "Sakura Deaikan\n\n"
               "At the entrance to Sewaritei, 10–15 minutes’ walk from Iwashimizu-hachimangu Station across the Goko bridge. A lift takes you up the tower to see where the Uji, Katsura and Kizu rivers become the Yodo, and the avenue from above.\n\n"
               "Inside are toilets, vending machines, coin lockers (opening hours only) and a shop. Bread and sushi are sold only on weekends and some holidays, 9:30–16:00."),
        gmaps=[gm("さくらであい館", "Sakura Deaikan", 34.89042, 135.70148, "さくらであい館"),
               gm("京阪 石清水八幡宮駅", "Keihan Iwashimizu-hachimangu Station", 34.88444, 135.70028, "京阪 石清水八幡宮駅")],
        links=[link("official", "さくらであい館", "Sakura Deaikan (Japanese)", DEAIKAN, DEAIKAN + "en/")],
        notices=[N_TOWER],
        _rows=[row("hours", "9:00〜17:00。展望塔 9:00〜16:30（最終受付16:20）", "9:00–17:00. Tower 9:00–16:30 (last entry 16:20)"),
               row("closed", "12月29日〜1月3日", "29 Dec – 3 Jan"),
               row("fee", "展望塔はふだん無料。2026年のさくらまつりの間は大人300円・子ども100円（来春は要確認）", "Tower usually free. ¥300 adults, ¥100 children during the 2026 festival (please check for next spring)")],
        _tip=T("淀川河川公園の公式サイトと、八幡市観光協会の2026年春の観光ガイド（展望塔の料金）で確認しました。",
               "Checked on the park website and the Yawata tourism association’s spring 2026 guide (tower fee)."),
        _source=f"淀川河川公園 {DEAIKAN}、売店 {DEAIKAN_SHOP}、料金は八幡市観光協会の2026年春号 {SPRING_GUIDE}。2026-11-22に確認"),
)

VIS = ("おすすめ訪問時間", "Recommended visit time")
TRANSIT_TIP = T("京阪は乗換案内で平日・土曜・日曜・祝日を確認しました（2026年11月の時刻）。春までに変わることがあるので要確認。歩く時間は少しゆったりめです。",
                "Keihan times were checked on a route planner for a weekday, Saturday, Sunday and holiday (November 2026 timetable) and may change by spring. Walking times are rounded up a little.")

# ---------------------------------------------------------------------------
# 最後のスポットのあとに続ける文章（夕方と夜）
# ---------------------------------------------------------------------------
LAST_TRAIN = T("三条へ帰れる最後の電車は、石清水八幡宮23:58発、中書島0:09発（どちらも0:22着。毎日同じ）。",
               "The last trains to Sanjo leave Iwashimizu-hachimangu at 23:58 and Chushojima at 0:09 (both arrive 0:22, every day).")
NIGHT_SAKURA = T(
    "夜：祇園四条から夜桜へ\n"
    "駅から歩いて5分ほどの祇園白川、そこから15分ほどの円山公園のしだれ桜へ。2026年春のライトアップは、祇園白川が3月27日〜4月5日、円山公園が3月24日〜4月8日、どちらも18:00〜22:00で無料でした。来春は要確認です。\n"
    "19:30ごろ四条通を戻って橋を渡ると、先斗町（ぽんとちょう）と木屋町です。晩ごはんのあと三条へ歩いて、21〜22時ごろまで。閉まる時間は店の表で確かめてください。\n"
    + LAST_TRAIN["ja"],
    "Evening: blossom by lamplight from Gion-Shijo\n"
    "Gion Shirakawa is about 5 minutes from the station, and Maruyama Park’s weeping cherry 15 minutes beyond. In spring 2026 Shirakawa was lit 27 March – 5 April and Maruyama Park 24 March – 8 April, both 18:00–22:00 and free. Please check for next spring.\n"
    "Around 19:30 walk back down Shijo-dori and over the bridge to Pontocho and Kiyamachi. Dinner, then stroll up to Sanjo until 21:00 or 22:00; check closing times at the door.\n"
    + LAST_TRAIN["en"])

AFTER_KAWAZU = T(
    "夕方の続き：伏見の酒蔵の町へ（16:20ごろ出発）\n\n"
    "駅まで歩いて10〜15分。石清水八幡宮16:49発（土日祝16:48発）の京阪で、中書島16:58着・320円。宇治川派流の川沿いと酒蔵の通りを、暗くなるまで歩きます（月桂冠大倉記念館は受付16:00までなので、外から）。\n\n"
    "夜：伏見で晩ごはん、それから三条へ\n"
    "18:00ごろ、キザクラカッパカントリーの黄桜酒場へ。17:00〜21:30（ラストオーダー20:50）、火曜休み（祝日なら水曜）です。中書島まで10分ほど歩いて、19:52発の特急で三条20:06着（土日祝20:05着）・320円。もう1軒は鴨川を渡った先斗町（ぽんとちょう）・木屋町で、21〜22時ごろまで。\n"
    "火曜と、疲れた日は伏見に寄らずに、石清水八幡宮17:14発（土日祝17:12発）→祇園四条17:39着（17:37着）・360円。丹波橋で特急に乗り換えです。晩ごはんは先斗町・木屋町で。\n"
    + LAST_TRAIN["ja"],
    "Later: Fushimi’s sake town (leave about 16:20)\n\n"
    "It is 10–15 minutes’ walk to the station. Take the 16:49 (16:48 at weekends and on holidays) to Chushojima, arriving 16:58, ¥320, and walk the canal and brewery streets until dark. Gekkeikan’s museum takes its last visitors at 16:00, so see it from outside.\n\n"
    "Evening: dinner in Fushimi, then back to Sanjo\n"
    "Around 18:00 go to Kizakura Sakaba at Kizakura Kappa Country: 17:00–21:30 (last orders 20:50), closed Tuesdays (Wednesday if a holiday). Walk about 10 minutes to Chushojima for the 19:52 express, at Sanjo 20:06 (20:05 at weekends and on holidays), ¥320. Have another drink across the Kamo river in Pontocho or Kiyamachi until 21:00 or 22:00.\n"
    "On Tuesdays, or if you’re tired, skip Fushimi: Iwashimizu-hachimangu 17:14 (17:12) → Gion-Shijo 17:39 (17:37), ¥360, changing to an express at Tambabashi. Dinner is in Pontocho or Kiyamachi.\n"
    + LAST_TRAIN["en"])

AFTER_SAKURA = T(
    "夕方の続き：門前の走井餅、それから京都へ（16:15ごろ）\n\n"
    "駅のほうへ歩いて15分ほど。一ノ鳥居前の走井餅老舗でお茶を（喫茶のラストオーダー17:00、月曜休み）。石清水八幡宮17:14発（土日祝17:12発）→祇園四条17:39着（17:37着）・360円。丹波橋で特急に乗り換えです。\n\n"
    + NIGHT_SAKURA["ja"],
    "Later: rice cakes at the foot of the hill, then Kyoto (about 16:15)\n\n"
    "Walk about 15 minutes toward the station for tea at Hashiriimochi by the first torii (last orders 17:00, closed Mondays). Take the 17:14 (17:12 at weekends and on holidays) from Iwashimizu-hachimangu → Gion-Shijo 17:39 (17:37), ¥360, changing to an express at Tambabashi.\n\n"
    + NIGHT_SAKURA["en"])

AFTER_EARLY = T(
    "午後の続き：遅めのお昼、伏見の酒蔵へ（13:50ごろ）\n\n"
    "表参道を下りたら、駅前の朝日屋で鯖寿司のお昼（11:00〜17:00）。月・火は休みなので、お弁当か会場の屋台で早めに。石清水八幡宮15:13発の京阪で、中書島15:22着・320円（毎日同じ）。\n"
    "歩いて10分ほどの月桂冠大倉記念館へ。9:30〜16:30、受付は16:00まで、20歳以上600円でおみやげときき酒つき。現金は使えません。予約は2週間前の9:30から前日16:30までで、予約なしだと混む日は入れないことがあります。\n"
    "そのあと川沿いを歩いて、中書島17:27発（土日祝17:26発）の特急で祇園四条17:39着（17:37着）・320円。\n\n"
    + NIGHT_SAKURA["ja"],
    "Afternoon: a late lunch, then Fushimi’s breweries (about 13:50)\n\n"
    "At the foot of the main approach, lunch on mackerel sushi at Asahiya by the station (11:00–17:00). It closes Mondays and Tuesdays, so eat a packed lunch or something from the festival stalls earlier on those days. Take the 15:13 to Chushojima, arriving 15:22, ¥320 (every day).\n"
    "The Gekkeikan Okura Sake Museum is about 10 minutes’ walk: 9:30–16:30, last entry 16:00, ¥600 for 20 and over with a gift and tasting. No cash. Book from 9:30 two weeks ahead until 16:30 the day before; without a booking you may not get in on busy days.\n"
    "Then walk the canal and take the express from Chushojima at 17:27 (17:26 at weekends and on holidays) → Gion-Shijo 17:39 (17:37), ¥320.\n\n"
    + NIGHT_SAKURA["en"])

LAST_ROW = row("train", "最終：石清水八幡宮23:58発、中書島0:09発 → 三条0:22着（毎日同じ）", "Last: Iwashimizu-hachimangu 23:58, Chushojima 0:09 → Sanjo 0:22 (every day)")
BACK_DIRECT = row("train", "帰り：石清水八幡宮17:14発（土日祝17:12発）→ 祇園四条17:39着（17:37着）・360円。三条までは400円", "Back: Iwashimizu-hachimangu 17:14 (weekends and holidays 17:12) → Gion-Shijo 17:39 (17:37), ¥360. To Sanjo ¥400")
KIZAKURA_ROW = row("hours", "黄桜酒場（伏見）17:00〜21:30（ラストオーダー20:50）、火曜休み（祝日なら水曜）", "Kizakura Sakaba (Fushimi) 17:00–21:30 (last orders 20:50), closed Tuesdays (Wednesday if a holiday)")
GEKKEIKAN_ROW = row("hours", "月桂冠大倉記念館（伏見）9:30〜16:30、受付16:00まで。20歳以上600円、現金不可。臨時休館あり", "Gekkeikan museum (Fushimi) 9:30–16:30, last entry 16:00. ¥600 for 20 and over, no cash. Occasional closures")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
# （スポットの id, 時間（日本語）, 時間（英語）, そのコースでの一言）
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="kawazu", file="yawata.json",
        note="「3月：淀の河津桜」コース。三条9:29（土日祝9:26）→淀→淀水路→淀城跡→淀11:38（11:37）→八幡でお昼→石清水八幡宮→走井餅→展望塔→中書島→伏見で晩ごはん→三条。",
        rows=[row("train", "行き：三条9:29発（土日祝9:26発）→ 丹波橋で乗り換え → 淀9:53着（土日祝9:48着）・360円", "Out: Sanjo 9:29 (weekends and holidays 9:26) → change at Tambabashi → Yodo 9:53 (9:48), ¥360"),
              row("train", "早く見たい人：三条7:05発（土日祝7:12発）→ 淀7:26着（土日祝7:34着）・360円", "To see it early: Sanjo 7:05 (weekends and holidays 7:12) → Yodo 7:26 (7:34), ¥360"),
              row("train", "次へ：淀11:38発（土日祝11:37発）→ 石清水八幡宮11:42着（土日祝11:40着）・240円", "Next: Yodo 11:38 (weekends and holidays 11:37) → Iwashimizu-hachimangu 11:42 (11:40), ¥240")],
        order=[
            ("yodo", "10:05〜10:55", "10:05–10:55",
             T("三条から京阪で20分あまり。特急か快速急行に乗って、丹波橋で各駅停車か準急に乗り換えます。淀水路はいつでも歩けるので、人の少ない写真を撮りたい人は7時台に着く電車で先に。その日は朝ごはんを持っていって、このあとの時間は同じです。\n\n"
               "東の端まで歩いたら、大淀中学校の横を通って駅のほうへ戻ります。駅のそばの淀城跡公園と與杼神社（よどじんじゃ）に寄って、淀11:38発（土日祝11:37発）で石清水八幡宮へ1駅。\n\n"
               "2026年は3月14日と21日の10:00〜17:00に、駅前の淀本町商店街と淀城跡公園で桜まつりがあり、屋台も出ました。来春は要確認です。",
               "A little over 20 minutes from Sanjo: take an express and change at Tambabashi to a local or sub-express. The canal is open at any time, so for photos with fewer people come first on a train that arrives in the 7 o’clock hour. Bring breakfast that day; the rest of the timetable stays the same.\n\n"
               "From the east end walk back toward the station past Oyodo junior high school. Stop at the Yodo castle ruins and Yodo Shrine beside the station, then take the 11:38 (11:37 at weekends and on holidays) one stop to Iwashimizu-hachimangu.\n\n"
               "In 2026 the shopping street by the station and the castle park held a cherry festival with food stalls on 14 and 21 March, 10:00–17:00. Please check for next spring.")),
            ("iwashimizu", "12:55〜14:00", "12:55–14:00",
             T("11:42（土日祝11:40）に駅に着いたら、まずお昼。駅前の朝日屋は100年以上続く鯖寿司の店です。火曜は走井餅老舗の喫茶か持参のお昼、月曜はお弁当で。12:45発のケーブルで上がります。\n\n"
               "14:05ごろから表参道を歩いて下り、14:45ごろ一ノ鳥居前の走井餅老舗へ。つきたての餅でこしあんを包んだ走井餅とお茶でひと休みして、15:10ごろ展望塔へ歩き出します（15分ほど）。月曜は休みなので、そのまま展望塔へ。",
               "Arriving at 11:42 (11:40 at weekends and on holidays), eat first: Asahiya by the station has served mackerel sushi for over 100 years. On Tuesdays use the Hashiriimochi tearoom or your own lunch, and on Mondays bring one. Take the 12:45 cable car up.\n\n"
               "Walk down the main approach from about 14:05, reaching Hashiriimochi by the first torii about 14:45 for tea and its soft rice cakes filled with bean paste. Set off for the tower about 15:10 (15 minutes). It closes on Mondays, so go straight to the tower then.")),
            ("deaikan", "15:30〜16:20", "15:30–16:20",
             T("先に展望塔へ上がり、時間があれば背割堤の入口あたりの川沿いを少し歩きます。16:20には駅へ向かってください。",
               "Go up the tower first and, if there’s time, stroll by the river at the head of Sewaritei. Set off for the station by 16:20.")),
        ],
        sections=[dict(first="yodo", last="yodo", area=T("淀", "Yodo"), title=T("水路沿いの河津桜と、お城の跡", "Kawazu cherries and a castle ruin")),
                  dict(first="iwashimizu", last="iwashimizu", area=T("八幡・男山", "Yawata, Mt. Otokoyama"), title=T("駅前でお昼、山の上の国宝へ", "Lunch, then a National Treasure on the hill")),
                  dict(first="deaikan", last="deaikan", area=T("三川合流 → 伏見", "Three rivers → Fushimi"), title=T("川を見下ろして、夜は酒蔵の町へ", "A river view, then the sake town"))],
        after=AFTER_KAWAZU, links_last=[L_KIZAKURA, L_UJI, L_EIZAN, L_YAHOO],
        gmaps_first=[gm("與杼神社・淀城跡公園", "Yodo Shrine & castle ruins", 34.90530, 135.71838, "與杼神社 淀")],
        gmaps_last=[gm("キザクラカッパカントリー", "Kizakura Kappa Country", 34.93083, 135.76050, "キザクラカッパカントリー")],
        links_first=[link("info", "淀本町商店街の桜まつり（2026年の実績）", "Yodo cherry festival (as held in 2026, Japanese)", YODO_FES), L_YAHOO],
        back=[row("train", "伏見へ：石清水八幡宮16:49発（土日祝16:48発）→ 中書島16:58着・320円", "To Fushimi: Iwashimizu-hachimangu 16:49 (weekends and holidays 16:48) → Chushojima 16:58, ¥320"),
              row("train", "帰り：中書島19:52発 → 三条20:06着（土日祝20:05着）・320円", "Back: Chushojima 19:52 → Sanjo 20:06 (weekends and holidays 20:05), ¥320"),
              BACK_DIRECT, LAST_ROW, KIZAKURA_ROW],
        notices_extra=dict(deaikan=[N_MARCH_TOWER]),
        hints=[
            ("iwashimizu", dict(any=["iwashimizu"], none=["yodo"]),
             "淀に寄らない日は、三条9:29発（土日祝9:26発）で石清水八幡宮9:56着（9:51着）・400円。10:15のケーブルで先にお参りして、お昼はそのあとに。",
             "Skipping Yodo: the 9:29 from Sanjo (9:26 at weekends and on holidays) reaches Iwashimizu-hachimangu at 9:56 (9:51), ¥400. Take the 10:15 cable car and have lunch afterwards."),
            ("yodo", dict(any=["yodo"], none=["iwashimizu", "deaikan"]),
             "淀だけなら午前中で終わります。帰りも丹波橋で特急に乗り換えて、三条まで20分あまり・360円。",
             "Yodo alone takes just the morning. Back to Sanjo is again a little over 20 minutes with a change at Tambabashi, ¥360."),
            ("deaikan", dict(any=["deaikan"], none=["iwashimizu"]),
             "石清水八幡宮に寄らない日は、お昼のあとすぐ展望塔へ（駅から10〜15分）。夕方の伏見に早く行けて、月桂冠大倉記念館（受付16:00まで）にも間に合います。",
             "Skipping the shrine: go to the tower straight after lunch (10–15 minutes from the station). You reach Fushimi earlier, in time for Gekkeikan’s museum (last entry 16:00)."),
        ]),
    dict(
        id="sakura", file="yawata-sakura.json",
        note="「4月：背割堤の桜」コース。三条9:29（土日祝9:26）→石清水八幡宮→お昼→展望塔→背割堤→走井餅→17:14（17:12）→祇園四条→祇園白川・円山公園の夜桜。",
        rows=[row("train", "行き：三条9:29発（土日祝9:26発）→ 丹波橋で乗り換え → 石清水八幡宮9:56着（土日祝9:51着）・400円", "Out: Sanjo 9:29 (weekends and holidays 9:26) → change at Tambabashi → Iwashimizu-hachimangu 9:56 (9:51), ¥400")],
        order=[
            ("iwashimizu", "10:25〜11:50", "10:25–11:50",
             T("人の多い堤防はあとにして、午前は山の上へ。10:15発のケーブルに乗ります。列で乗れなければ、00分・30分の便か次の45分発で。\n\n"
               "11:50ごろから表参道を歩いて下り、12:30ごろ駅前の朝日屋で鯖寿司のお昼。桜の時期は待つかもしれないので、列が長ければ会場の屋台へ。月・火は休みなので、お弁当を持って背割堤の芝生で。まつりの期間なら会場の屋台もあります（2026年の実績）。13:20ごろ御幸橋のほうへ歩きます。",
               "Leave the crowded levee for later and start on the hill, on the 10:15 cable car. If the queue is too long, take a :00 or :30 extra or the :45.\n\n"
               "Walk down the main approach from about 11:50 and have mackerel sushi at Asahiya by the station about 12:30. There may be a wait in blossom season, so use the festival stalls if the line is long. It closes Mondays and Tuesdays: bring a picnic for the grass at Sewaritei then, or use the festival stalls (as in 2026). Set off toward the bridge about 13:20.")),
            ("deaikan", "13:40〜14:25", "13:40–14:25",
             T("桜の時期は展望塔に列ができても受付に間に合うよう、堤防より先に上がります。",
               "Go up before walking the levee, so that a blossom-season queue can’t make you miss the last entry.")),
            ("sewaritei", "14:30〜16:15", "14:30–16:15",
             T("帰りに走井餅老舗へ寄るなら、16:15には堤防を出ます。",
               "Leave the levee by 16:15 if you want tea at Hashiriimochi on the way back.")),
        ],
        sections=[dict(first="iwashimizu", last="iwashimizu", area=T("八幡・男山", "Yawata, Mt. Otokoyama"), title=T("午前は山の上の国宝へ、駅前でお昼", "The hilltop shrine, then lunch")),
                  dict(first="deaikan", last="sewaritei", area=T("背割堤 → 祇園", "Sewaritei → Gion"), title=T("午後は桜のトンネル、夜は夜桜", "A tunnel of blossom, then cherries by night"))],
        after=AFTER_SAKURA, links_last=[L_HASHIRII, L_NIGHT, L_EIZAN, L_YAHOO],
        gmaps_first=[],
        gmaps_last=[gm("祇園白川", "Gion Shirakawa", 35.00560, 135.77390, "祇園白川 巽橋"), gm("円山公園", "Maruyama Park", 35.00380, 135.78000, "円山公園 京都")],
        links_first=[L_YAHOO],
        back=[BACK_DIRECT, LAST_ROW],
        notices_extra=dict(),
        hints=[
            ("sewaritei", dict(any=["sewaritei"], none=["iwashimizu"]),
             "石清水八幡宮に寄らない日は、駅からまっすぐ背割堤へ（10:15ごろ着）。展望塔と並木で12:30ごろまで。午後は京阪で伏見へ寄ってから帰れます。",
             "Skipping the shrine: walk straight to Sewaritei (about 10:15). The tower and avenue take until about 12:30, leaving the afternoon for Fushimi on the way back."),
            ("sewaritei", dict(any=["sewaritei"], none=["deaikan"]),
             "展望塔に上らない日は、並木に14:00ごろ着いて、芝生でゆっくりできます。",
             "Skipping the tower: you reach the avenue about 14:00 and have longer on the grass."),
        ]),
    dict(
        id="early", file="yawata-early.json",
        note="「4月：背割堤の開園へ」コース。三条8:11（土日祝8:12）→展望塔9:00→背割堤→走井餅でひと休み→石清水八幡宮→遅めのお昼→15:13→中書島→月桂冠→祇園四条の夜桜。",
        rows=[row("train", "行き：三条8:11発（土日祝8:12発）→ 石清水八幡宮8:39着（土日祝8:38着）・400円。乗り換えは平日が中書島、土日祝が丹波橋", "Out: Sanjo 8:11 (weekends and holidays 8:12) → Iwashimizu-hachimangu 8:39 (8:38), ¥400. Change at Chushojima on weekdays, Tambabashi at weekends and on holidays")],
        order=[
            ("deaikan", "8:55〜9:30（9:00開館）", "8:55–9:30 (opens 9:00)",
             T("三条を8:10ごろに出て、9:00の開館に合わせます。駅の改札を出て左へ。踏切を渡って橋のほうへ10〜15分です。展望塔に列ができる前に上がってから、堤防へ。朝は軽く食べて出てください。",
               "Leave Sanjo about 8:10 to be here for the 9:00 opening. Turn left out of the station gates, cross the level crossing and head for the bridge: 10–15 minutes. Go up the tower before a queue builds, then onto the levee. Eat something light before you set out.")),
            ("sewaritei", "9:35〜10:50", "9:35–10:50",
             T("昼に人が増える前に歩きます。10:50ごろ出て15分ほど歩き、一ノ鳥居前の走井餅老舗（9:00から）で朝のひと休み。餅とお茶があり、八幡市観光協会の案内ではぜんざいとうどんも出ます。月曜は休みなので、朝ごはんを持ってきて芝生で。",
               "Walk it before the midday crowds. Leave about 10:50 and walk 15 minutes to Hashiriimochi by the first torii (open from 9:00) for a morning break: rice cakes and tea, and the tourism association also lists sweet bean soup and udon. It closes on Mondays, so bring breakfast to eat on the grass.")),
            ("iwashimizu", "11:55〜13:15", "11:55–13:15",
             T("11:45発のケーブルで上がります。お参りと展望台のあと、13:15ごろから表参道を歩いて13:50ごろ下に着きます。",
               "Take the 11:45 cable car up. After the shrine and lookout, walk down from about 13:15 to reach the bottom about 13:50.")),
        ],
        sections=[dict(first="deaikan", last="sewaritei", area=T("背割堤", "Sewaritei"), title=T("開園に合わせて、桜のトンネルへ", "The tunnel of blossom at opening time")),
                  dict(first="iwashimizu", last="iwashimizu", area=T("男山 → 伏見・祇園", "Mt. Otokoyama → Fushimi, Gion"), title=T("山の上の国宝、午後は酒蔵、夜は夜桜", "The shrine, breweries, cherries by night"))],
        after=AFTER_EARLY, links_last=[L_GEKKEIKAN, L_UJI, L_NIGHT, L_EIZAN, L_YAHOO],
        gmaps_first=[],
        gmaps_last=[gm("月桂冠大倉記念館", "Gekkeikan Okura Sake Museum", 34.92888, 135.76163, "月桂冠大倉記念館"), gm("祇園白川", "Gion Shirakawa", 35.00560, 135.77390, "祇園白川 巽橋")],
        links_first=[L_YAHOO],
        back=[row("train", "伏見へ：石清水八幡宮15:13発 → 中書島15:22着・320円（毎日同じ）", "To Fushimi: Iwashimizu-hachimangu 15:13 → Chushojima 15:22, ¥320 (every day)"),
              row("train", "帰り：中書島17:27発（土日祝17:26発）→ 祇園四条17:39着（17:37着）・320円", "Back: Chushojima 17:27 (weekends and holidays 17:26) → Gion-Shijo 17:39 (17:37), ¥320"),
              LAST_ROW, GEKKEIKAN_ROW],
        notices_extra=dict(),
        hints=[
            ("sewaritei", dict(any=["sewaritei"], none=["iwashimizu"]),
             "石清水八幡宮に寄らない日は、ひと休みのあと京阪で中書島へ（320円）。伏見でお昼と酒蔵をゆっくり回れます。",
             "Skipping the shrine: after your break take the train to Chushojima (¥320) for lunch and an unhurried look at Fushimi’s breweries."),
            ("iwashimizu", dict(any=["iwashimizu"], none=["sewaritei", "deaikan"]),
             "背割堤に行かない日は、早く出なくて大丈夫。ケーブルは8:10から動いています。",
             "Skipping Sewaritei: there’s no need to start early. The cable car runs from 8:10."),
        ]),
]


def yurl(frm, to, ymd, hm, typ=1):
    q = dict([("from", frm), ("to", to), ("y", ymd[:4]), ("m", ymd[4:6]), ("d", ymd[6:]), ("hh", hm[:2]), ("m1", hm[2]), ("m2", hm[3]), ("type", typ),
              ("ticket", "ic"), ("expkind", 1), ("ws", 3), ("s", 0)])
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(q)


def src(what, url):
    return {"what": what, "url": url, "checked": CHECKED}


WD, SA = "20261125", "20261128"
SOURCES = [
    src("京阪 三条→淀（平日 11-25。2027-03-10で検索しても同じ）：9:29発→丹波橋9:40着・9:44発→淀9:53着、360円", yurl("三条", "淀", WD, "0925")),
    src("京阪 三条→淀（土 11-28。日 11-29・祝 2027-03-22も同じ）：9:26発→丹波橋9:37着・9:39発→淀9:48着、360円", yurl("三条", "淀", SA, "0925")),
    src("京阪 三条→淀 早朝（平日）：7:05発→丹波橋7:16着・7:17発→淀7:26着、360円", yurl("三条", "淀", WD, "0700")),
    src("京阪 三条→淀 早朝（土・日）：7:12発→丹波橋7:23着・7:24発→淀7:34着、360円", yurl("三条", "淀", SA, "0700")),
    src("京阪 三条→石清水八幡宮（平日）：9:29発→丹波橋9:40着・9:44発→9:56着、400円", yurl("三条", "石清水八幡宮", WD, "0928")),
    src("京阪 三条→石清水八幡宮（土・祝 11-23）：9:26発→丹波橋9:37着・9:39発→9:51着、400円", yurl("三条", "石清水八幡宮", SA, "0918")),
    src("京阪 三条→石清水八幡宮 開園へ（平日 11-25・2027-03-31）：8:11発→中書島8:24着・8:30発→8:39着、400円", yurl("三条", "石清水八幡宮", WD, "0810")),
    src("京阪 三条→石清水八幡宮 開園へ（土 11-28・2027-04-03、祝 11-23）：8:12発→丹波橋8:23着・8:25発→8:38着、400円", yurl("三条", "石清水八幡宮", SA, "0810")),
    src("京阪 淀→石清水八幡宮（平日）：11:38発→11:42着、240円", yurl("淀", "石清水八幡宮", WD, "1130")),
    src("京阪 淀→石清水八幡宮（土・日）：11:37発→11:40着、240円", yurl("淀", "石清水八幡宮", SA, "1130")),
    src("京阪 石清水八幡宮→中書島（平日・土・日）：15:13発→15:22着、320円、乗り換えなし", yurl("石清水八幡宮", "中書島", WD, "1450")),
    src("京阪 石清水八幡宮→中書島（平日）：16:49発→16:58着、320円", yurl("石清水八幡宮", "中書島", WD, "1638")),
    src("京阪 石清水八幡宮→中書島（土・日）：16:48発→16:58着、320円", yurl("石清水八幡宮", "中書島", SA, "1638")),
    src("京阪 石清水八幡宮→祇園四条（平日）：17:14発→丹波橋17:27着・17:30発→17:39着、360円", yurl("石清水八幡宮", "祇園四条", WD, "1710")),
    src("京阪 石清水八幡宮→祇園四条（土・日・祝 11-23）：17:12発→丹波橋17:26着・17:28発→17:37着、360円", yurl("石清水八幡宮", "祇園四条", SA, "1710")),
    src("京阪 中書島→祇園四条（平日）：17:27発→17:39着、320円", yurl("中書島", "祇園四条", WD, "1715")),
    src("京阪 中書島→祇園四条（土・日）：17:26発→17:37着、320円", yurl("中書島", "祇園四条", SA, "1715")),
    src("京阪 中書島→三条：19:52発→平日20:06着・土日20:05着、320円", yurl("中書島", "三条", WD, "1945")),
    src("京阪 石清水八幡宮→三条 終電（平日・土・日）：23:58発→丹波橋0:10着・0:12発→0:22着、400円", yurl("石清水八幡宮", "三条", WD, "2359", 2)),
    src("京阪 中書島→三条 終電（平日・土・日）：0:09発→0:22着、320円", yurl("中書島", "三条", WD, "2359", 2)),
    src("京阪のダイヤ変更：2026年8月22日初発から（上の時刻はこのダイヤ）", "https://www.keihan.co.jp/traffic/news/2026/"),
    src("参道ケーブル：毎日同じ。8時台10・※30・45、9〜17時台※00・15・※30・45、18時台※00・15（※は乗客がいるとき）。3分、片道300円・往復600円", CABLE),
    src("淀水路：例年3月上〜中旬、約300本・約1.3km・30分、中央改札から約10分、改札外にトイレなし、いつでも無料。満開 2026年3/7ごろ・2025年3/21ごろ、2026年3/27葉桜", YODO),
    src("淀本町商店街 桜まつり（2026年の実績）：3/14・21の10:00〜17:00、商店街と淀城跡公園。来春は要確認", YODO_FES),
    src("石清水八幡宮：6:00〜18:00（正月は変動）、定休日なし、山上駅から徒歩約5分", IWA_NAVI),
    src("石清水八幡宮：山上のトイレ2か所、ケーブルでも階段が数段", IWA_QA),
    src("表参道・展望台：本殿→展望台 約5分、一ノ鳥居→本殿の区間の合計 約28分（下りは30〜35分と書いた）", IWA_WALK),
    src("八幡市観光協会 2026年春号：石清水八幡宮の特別公開 3/20〜4/12・9:00〜16:00・大人1,000円・中高生500円、展望塔はまつり期間中 大人300円・子ども100円、最終受付16:20。どちらも来春は要確認", SPRING_GUIDE),
    src("背割堤さくらまつり（2026年の実績）：3/28〜4/5・9:00〜17:00、協力金1人100円以上（6歳未満除く）、マルシェ40店舗、3/26〜4/8は会場と周辺の駐車場閉鎖、駅から約10分。来春は未発表", FES_2026),
    src("背割堤の見ごろの目安：2026年のまつりは「桜が見頃の9日間程度」を3/21〜4/12の間で決める（2025-12-22の報道資料）。実際は3/28〜4/5", "https://www.yodogawa-park.jp/cms/wp-content/uploads/2025/12/2c942c910b3a6e6f2fe0541c8c92e2ec.pdf"),
    src("淀川河川公園 開園時間（2025年4月時点）：背割堤は通年9時〜17時、12/29〜1/3休園", PARK_HOURS),
    src("背割堤：堤防の上の園路は自転車の押し歩きも禁止、ごみ持ち帰り", PARK_RULES),
    src("背割堤：約1.4km・約220本、まつり期間は駐車場利用不可、駅から徒歩約10分（徒歩ルートの写真案内は15分）", PARK),
    src("背割堤：約20万人が訪れる花見名所（八幡市観光協会トップ）", "https://www.kankou-yawata.org/"),
    src("混雑度（お花見期間中）：背割堤は平日 混雑・休日 大変混雑（ウェザーニュース。公式の数字ではない）", "https://weathernews.jp/sakura/spot/61030/"),
    src("混雑度（お花見期間中）：淀水路は平日 混雑・休日 大変混雑（ウェザーニュース。公式の数字ではない）", "https://weathernews.jp/sakura/spot/61050/"),
    src("御幸橋の読み（ごこうばし）：橋のたもとの表示（淀川河川事務所の河川モニター報告）", "https://www-1.kkr.mlit.go.jp/yodogawa/activity/keep/monitor/bd083b00000038ka-att/a1572588736978.pdf"),
    src("さくらであい館：9:00〜17:00、展望塔9:00〜16:30（受付16:20）、12/29〜1/3休館、ふだん無料・繁忙期は有料の場合あり", DEAIKAN),
    src("さくらであい館の売店：パン・寿司は土日と連休最終の祝日 9:30〜16:00", DEAIKAN_SHOP),
    src("朝日屋 本店：11:00〜17:00（金土日の夜は予約制）、月・火休み（祝日は営業）、駅前", ASAHIYA),
    src("やわた走井餅老舗：9:00〜17:30（喫茶LO17:00）、月曜休み（祝日なら翌日）、駅から2分", HASHIRII),
    src("走井餅老舗の喫茶：ぜんざい・うどんもある（八幡市観光協会）", YAWATA_FOOD),
    src("月桂冠大倉記念館：9:30〜16:30（受付16:00）、20歳以上600円、現金不可、予約は2週間前9:30〜前日16:30、8/13〜16・12/28〜1/4ほか臨時休館", GEKKEIKAN),
    src("黄桜酒場：夜17:00〜21:30（LO20:50）、火曜休み（祝日なら水曜）", KIZAKURA),
    src("円山公園 桜ライトアップ（2026年の実績）：3/24〜4/8、無料。来春は要確認", MARUYAMA),
    src("祇園白川宵桜ライトアップ 3/27〜4/5・18:00〜22:00・無料、円山公園 18:00〜22:00（2026年の実績）。来春は要確認", NIGHT),
    src("歩く時間（OpenStreetMap の徒歩ルートの目安。文章では長めに）：石清水八幡宮駅→さくらであい館11分、淀駅→淀水路9分、中書島→月桂冠10分・黄桜11分、祇園四条→円山公園10分", "https://routing.openstreetmap.de/"),
]

NOTE_HEAD = ("京都 淀・八幡の桜のルート（yawata/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで3つのコースを切り替え、"
             "コースごとに別のファイルを読む（yawata.json＝3月の河津桜、yawata-sakura.json＝4月の背割堤、yawata-early.json＝4月の背割堤の開園へ）。このファイル：")
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（淀水路と石清水八幡宮は2026年3月23日、背割堤は2026年4月8日。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "春の日程・料金は2026年春の実績で、来春は要確認。info.source は確認した出典、info.checked は確認日、sources は時刻・料金の出典の一覧。このファイルは scripts/build_yawata_data.py で作る（直接直さない）。")


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    last = order[-1][0]
    spots = []
    for sid, tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body, rows, tip, source = b.pop("body"), b.pop("_rows"), b.pop("_tip"), b.pop("_source")
        first = NO[sid] == 1
        b["notices"] = OFF_SEASON + c["notices_extra"].get(sid, []) + b["notices"]
        ja = body["ja"] + "\n\n" + go["ja"] + f"\n\n{VIS[0]}：{tj}"
        en = body["en"] + "\n\n" + go["en"] + f"\n\n{VIS[1]}: {te}"
        if first:
            rows = c["rows"] + rows
            b["links"] += c["links_first"]
            b["gmaps"] += c["gmaps_first"]
        if sid == last:
            rows = rows + c["back"]
            ja += "\n\n" + c["after"]["ja"]
            en += "\n\n" + c["after"]["en"]
            b["links"] += [x for x in c["links_last"] if x not in b["links"]]
            b["gmaps"] += c["gmaps_last"]
        if first or sid == last:
            tip = T(tip["ja"] + TRANSIT_TIP["ja"], tip["en"] + " " + TRANSIT_TIP["en"])
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out.update(info={"rows": rows, "cash": False, "tip": tip, "checked": CHECKED, "source": source},
                   text=T(ja, en), photos=photos(sid))
        spots.append(out)
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": [dict(s, first=NO[s["first"]], last=NO[s["last"]]) for s in c["sections"]],
        "plan": {"_note": "「選んで回る」の設定。時期はコースで分けたので、最初は「全部回る」。外したときの回り方は hints。",
                 "picks": [NO[x[0]] for x in order], "auto": {}, "defaultPicks": [NO[x[0]] for x in order],
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
