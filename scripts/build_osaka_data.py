#!/usr/bin/env python3
"""大阪（梅田〜難波のホテルから1日）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_osaka_data.py   （そのあと python3 scripts/sync_osaka.py）
- data/routes/osaka.json        … 「9〜10時に出発」（黒門市場→新世界→四天王寺→大阪城は15時ごろ→法善寺横丁→夜の道頓堀→淀屋橋の無料テラス）
- data/routes/osaka-early.json  … 「朝早く出発」（大阪城天守閣の9:00の開館に合わせる→黒門市場→新世界→四天王寺→うめきた公園→スカイビルの夕日→法善寺横丁→夜の道頓堀）
- 起点は梅田〜難波のあたりのホテル（2026-11-22 オーナーの指示。京都から来る人・帰る人の電車と終電は補足として書く）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの行き方（pre）→ 共通の説明（body）→ コースごとの次へ（post）→ おすすめ訪問時間」の順に組み立てる
- 時間割は11月下旬（日の入り16:50ごろ）の土曜のダイヤで組んだ。地下鉄・京阪・阪急・JRの時刻と運賃は乗換案内（Yahoo!路線情報、2026-11-28 土曜と 11-26 木曜）で確認
- 自分の写真は images/osaka/<スポットのid>-<番号>.jpg を番号の順に全部使う
- ネットの写真（Wikimedia Commons）は images/osaka/<id>-w<番号>.jpg。撮影者・ライセンス・ページは scripts/osaka_web_photos.json
  （WEB_FIRST に入っているスポットは、ネットの写真を先に並べる）
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/osaka"
CHECKED = "2026-11-22"
PICKS = {}
for f in os.listdir(IMG):
    m = re.match(r"(.+)-(\d+)\.jpg$", f)
    if m:
        PICKS.setdefault(m.group(1), []).append(int(m.group(2)))

# ネットの写真（Wikimedia Commons）。(ファイル, 撮影者, ライセンス, ファイルのページ)
WEB = json.load(open(f"{R}/scripts/osaka_web_photos.json", encoding="utf-8"))
WEB_FIRST = {"hozenji", "shinsekai", "shitennoji", "harukas", "sumiyoshi", "kaiyukan", "tenmangu", "skybldg"}


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def notice(hja, hen, ja, en):
    return {"head": T(hja, hen), "text": T(ja, en)}


def info(rows, tip=None, verified=True, cash=False, source=None, checked=None):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked or CHECKED, "source": source or []}
    if not verified:
        d["verified"] = False
    return d


def photos(pid):
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, []))]
    web = [{"file": w["file"], "credit": {"author": w["author"], "license": w["license"], "page": w["page"]}} for w in WEB.get(pid, [])]
    for w in web:
        assert os.path.exists(f"{IMG}/{w['file']}"), w["file"]
    out = web + own if pid in WEB_FIRST else own + web
    assert out, pid
    return out


PLANNER = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
ECO = "https://subway.osakametro.co.jp/guide/page/enjoy-eco.php"
SRC_PLANNER = "乗換案内（Yahoo!路線情報）2026-11-28（土）・11-26（木）のダイヤ"

# ---------------------------------------------------------------------------
# スポット（コースで変わらない部分）。コースで変わる行き方・時間・電車の行は下の COURSES に書く
# ---------------------------------------------------------------------------
S = dict(
    castle=dict(
        name=T("大阪城（天守閣・大阪城公園）", "Osaka Castle (main tower & park)"), kind=T("城・公園", "Castle & park"),
        lat=34.68735, lng=135.52590,
        caution=T("天守閣は5階から上と帰りが階段。入館は17:30まで", "Stairs above the 5th floor and all the way down. Last entry 17:30"),
        notices=[notice("天守閣の中は階段が多い", "Lots of stairs inside the tower",
                        "エレベーターは上りだけで5階まで。5階から8階の展望台までと、帰りの8階から1階までは階段です（車いす・歩くのが難しい人は全部の階で使えます）。入館は17:30までですが、混む日はそれより前に切符の列を締め切ることがあります。",
                        "The lift only goes up, and only to the 5th floor. From there to the 8th-floor deck, and the whole way back down, it is stairs (wheelchair users and people who have trouble walking can use the lift on every floor). Last entry is 17:30, but on busy days the ticket queue may be closed earlier.")],
        body=T("正面の大手門（おおてもん）から入ると、畳何十枚ぶんもある巨石の石垣が続きます。天守閣は中が博物館で、8階が展望台。公園は無料で、お堀のまわりを歩くだけでも来る価値があります。\n\n"
               "切符は窓口で買えますが、公式サイトから入れる予約サイトでWEBチケットを先に買っておくと、窓口の列に並ばずにすみます。カードや交通系ICも使えます。同じ日なら、天守閣の切符で豊臣石垣館にも入れます。\n\n"
               "天守閣の中だけで約1時間。お堀の外まで歩くと2時間近くかかります。写真は2016年2月と2025年4月、夜の天守閣は2026年4月。",
               "Enter by the main Otemon gate and you pass walls built of single stones the size of a room. The tower is a museum inside, with an observation deck on the 8th floor. The park is free, and the walk around the moats alone is worth the trip.\n\n"
               "Tickets are sold at the window, but if you buy a web ticket beforehand (through the booking site linked from the official site) you skip the window queue. Cards and transport IC cards are accepted. On the same day the tower ticket also admits you to the Toyotomi Stone Wall Museum.\n\n"
               "Allow about 1 hour inside the tower, nearly 2 hours if you walk the moats. Photos: February 2016 and April 2025; the night view is from April 2026."),
        gmaps=[gm("大阪城天守閣", "Osaka Castle main tower", 34.68735, 135.52590, "大阪城天守閣"),
               gm("大手門", "Otemon gate", 34.68605, 135.52125, "大阪城 大手門"),
               gm("谷町四丁目駅", "Tanimachi 4-chome Station", 34.68270, 135.51760, "谷町四丁目駅")],
        links=[link("official", "大阪城天守閣 公式サイト（観覧案内）", "Osaka Castle Museum (official)", "https://www.osakacastle.net/guide/", "https://www.osakacastle.net/english/"), PLANNER],
        rows=[row("hours", "天守閣 9:00〜18:00（入館は17:30まで）。公園は自由に歩けます", "Tower 9:00–18:00 (last entry 17:30). The park is always open"),
              row("closed", "12月28日〜1月1日", "28 December – 1 January"),
              row("fee", "天守閣 大人1,200円（高校生・大学生600円、中学生以下は無料。どちらも証明が必要）。エンジョイエコカードを見せると1,080円",
                  "Tower ¥1,200 (high-school and university students ¥600, junior-high and under free; ID needed for both). ¥1,080 with an Enjoy Eco Card")],
        tip=T("時間・料金・エレベーター・支払い方法は大阪城天守閣の公式サイト（観覧案内）、電車は乗換案内で確認しました。エンジョイエコカードの割引と豊臣石垣館は2026年11月21日の確認です。",
              "Hours, fees, lift and payment from the official Osaka Castle site; trains from a route planner. The Enjoy Eco Card discount and the Stone Wall Museum were checked on 21 Nov 2026."),
        source=["https://www.osakacastle.net/guide/", SRC_PLANNER]),
    tenmangu=dict(
        name=T("大阪天満宮・天神橋筋商店街", "Osaka Temmangu & Tenjinbashi-suji arcade"), kind=T("神社・商店街（寄り道）", "Shrine & arcade (detour)"),
        blurb=T("「天神さん」と、南北2.6kmの日本一長い商店街。観光地というより、大阪のふだんの顔です。",
                "“Tenjin-san” and Japan’s longest shopping arcade, 2.6 km from end to end. Less a sight than everyday Osaka."),
        lat=34.69605, lng=135.51265,
        body=T("学問の神様・菅原道真をまつる神社で、7月24日・25日の天神祭はここのお祭りです。門の前を通る天神橋筋商店街は、1丁目から6丁目まで続くアーケード。コロッケやたこ焼き、立ち飲みの店が並び、値段もミナミより気楽です。\n\n"
               "全部歩くと40分ほどかかるので、天満宮にお参りして、南森町の駅までの2丁目あたりを歩けば十分です。\n\n"
               "自分の写真は2024年7月の天神祭の夜の商店街。ふだんはここまで混みません。",
               "The shrine of Sugawara no Michizane, god of learning; the Tenjin Festival on 24–25 July belongs to it. The arcade that runs past its gate stretches from 1-chome to 6-chome: croquettes, takoyaki, standing bars, at easier prices than Minami.\n\n"
               "Walking it all takes about 40 minutes, so visit the shrine and stroll the 2-chome stretch up to Minami-morimachi Station.\n\n"
               "My own photo shows the arcade on a Tenjin Festival night in July 2024. It is not normally this crowded."),
        gmaps=[gm("大阪天満宮", "Osaka Temmangu", 34.69605, 135.51265, "大阪天満宮"),
               gm("南森町駅", "Minami-morimachi Station", 34.69790, 135.51140, "南森町駅")],
        links=[link("official", "大阪天満宮 公式サイト", "Osaka Temmangu (official, Japanese)", "https://osakatemmangu.or.jp/")],
        rows=[row("fee", "お参りは無料", "Free to visit"),
              row("hours", "門の開く時間は公式サイトで確認できませんでした（要確認）", "Gate hours could not be confirmed on the official site (please check)")],
        tip=T("行き方は大阪天満宮の公式サイト（南森町駅4番出口・JR大阪天満宮駅7番出口）、電車は乗換案内で確認しました（2026年11月21日）。", "Access from the shrine’s official site (Minami-morimachi exit 4, JR Osaka-Temmangu exit 7); trains from a route planner (21 Nov 2026)."),
        verified=False, checked="2026-11-21", source=["https://osakatemmangu.or.jp/", SRC_PLANNER]),
    kuromon=dict(
        name=T("黒門市場", "Kuromon Market"), kind=T("市場・食べ歩き", "Market & street food"),
        lat=34.66540, lng=135.50650, cash=True,
        caution=T("現金だけの店が多い。夕方は閉まる", "Many stalls are cash only. Closes late afternoon"),
        notices=[notice("千円札と小銭を", "Bring ¥1,000 notes and coins",
                        "カードやQR決済が使える店もありますが、現金だけの店がまだ多いです。開く時間と休みは店ごとに違い、夕方には閉まる店が多いので、午前から昼すぎに。",
                        "Some shops take cards or QR payment, but many are still cash only. Hours and closing days differ shop by shop and many shut in the late afternoon, so come between mid-morning and early afternoon.")],
        body=T("日本橋（にっぽんばし）駅の10番出口を出てすぐ。約580mのアーケードに、魚屋、ふぐの店、肉屋、果物屋が約150軒並びます。店先で焼いたホタテやうなぎの串、まぐろの刺身、いちごやカットフルーツをその場で食べられます。\n\n"
               "頼み方はかんたんで、指をさして「これを1つ」。値段は札に書いてあります。観光客向けの高い店も増えたので、端から端まで一度歩いて値札を見比べてから買うのがコツ。食べるのは、買った店の前かイートインの席で。歩きながらは食べにくい道幅です。\n\n"
               "このあとの新世界で串カツを食べるので、ここは2〜3品つまむくらいがちょうどいいです。\n\n"
               "写真は2023年12月29日。年末でいちばん混む日でした。",
               "Right outside exit 10 of Nippombashi Station. About 150 shops line a 580 m arcade: fishmongers, fugu specialists, butchers and fruit shops. Scallops and eel skewers grilled at the shopfront, tuna sashimi, strawberries and cut fruit are all sold to eat on the spot.\n\n"
               "Ordering is simple: point and say “kore o hitotsu” (one of these). Prices are on the tags. Some stalls now charge tourist prices, so walk the arcade end to end once and compare before you buy. Eat in front of the shop where you bought, or at its seats: the lane is too narrow to eat as you walk.\n\n"
               "Kushikatsu in Shinsekai comes next, so two or three bites here is about right.\n\n"
               "Photos: 29 December 2023, the busiest day of the year."),
        gmaps=[gm("黒門市場", "Kuromon Market", 34.66540, 135.50650, "黒門市場")],
        links=[link("official", "黒門市場 公式サイト", "Kuromon Market (official)", "https://kuromon.com/jp/", "https://kuromon.com/en/")],
        rows=[row("hours", "店ごとに違います（公式サイトの例：8:00〜20:00の店、10:00〜17:00の店）。行きたい店は公式サイトの店舗ページで確認を", "Varies by shop (examples on the official site: 8:00–20:00, 10:00–17:00). Check the shop pages there if you have one in mind"),
              row("closed", "店ごとに違います（日曜・祝日休み、不定休、年中無休など）", "Varies by shop (Sundays and holidays, irregular, or open every day)")],
        tip=T("店の数・長さ・店ごとの時間の例は黒門市場の公式サイトで確認しました。市場全体の営業時間や休みは決まっていません。", "Shop count, length and sample hours from the official site. The market as a whole has no fixed hours or closing day."),
        source=["https://kuromon.com/jp/", SRC_PLANNER]),
    shinsekai=dict(
        name=T("新世界・通天閣", "Shinsekai & Tsutenkaku tower"), kind=T("下町・串カツ・展望台", "Old downtown, kushikatsu & tower"),
        lat=34.65250, lng=135.50630,
        caution=T("串かつだるま 総本店は現金のみ・予約不可", "Kushikatsu Daruma’s original shop: cash only, no reservations"),
        notices=[notice("串カツの店と通天閣で先に知っておくこと", "Before you queue for kushikatsu or the tower",
                        "串かつだるまの新世界総本店はカウンター12席だけで、現金のみ・予約不可。1人1杯の飲み物を頼む決まりです。通天閣に上るには、切符を買うときに入場時間の予約が必要で、当日は待つことがあります（公式サイトでオンラインの事前予約もできます）。",
                        "Kushikatsu Daruma’s original Shinsekai shop has only 12 counter seats, takes cash only and no reservations, and asks each person to order one drink. To go up Tsutenkaku you must book an entry time when you buy the ticket, and on the day there may be a wait (advance online tickets are on the official site).")],
        body=T("串カツ屋の派手な看板のあいだから通天閣が見える通りが、写真でよく見る場所です。南側の細いアーケード「ジャンジャン横丁」まで歩いて10分もかかりません。\n\n"
               "お昼は串カツで。1本ずつ頼めるので、カウンターに座ったらまず飲み物と5〜6本。ソースは共用の入れ物に「二度づけ禁止」が決まりでしたが、今はボトルでかける店も増えました。足りないときは、付いてくるキャベツですくってかけます。\n\n"
               "店を決めていないなら、「串かつだるま」が新世界に4軒あります（総本店・通天閣店・ジャンジャン店・動物園前店）。どこも年中無休で、平日は11:00、土日祝は10:30から22:30まで。総本店が並んでいたら、席の多いほかの店へ回るのが早いです。\n\n"
               "通天閣の展望台は高さ約90m。梅田スカイビルやハルカスに上る日は、下から見上げるだけで十分です。日が暮れると塔と看板に明かりがつくので、夜にもう一度来る人もいます。\n\n"
               "看板の写真は2023年12月29日のぼくの写真、通天閣の写真はネットから借りたものです。",
               "The street where Tsutenkaku tower rises between loud kushikatsu signs is the view you know from photos. The narrow Janjan Yokocho arcade to the south is less than 10 minutes’ walk away.\n\n"
               "Have kushikatsu for lunch. It is ordered by the skewer: sit at the counter and start with a drink and five or six. The old rule was one shared tub of sauce and “no double dipping”; many shops now give you a bottle instead. If you need more sauce, scoop it with the cabbage that comes alongside.\n\n"
               "If you have no shop in mind, Kushikatsu Daruma has four in Shinsekai (the original shop, Tsutenkaku, Janjan and Dobutsuen-mae). All are open every day, from 11:00 on weekdays and 10:30 at weekends and on holidays, until 22:30. If the original shop has a queue, one of the larger branches is quicker.\n\n"
               "The tower’s deck is about 90 m up. On a day when you go up the Umeda Sky Building or Harukas, looking up at it from the street is enough. After dark the tower and the signs light up, and some people come back for that.\n\n"
               "The signboard photo is mine (29 December 2023); the tower photos are borrowed from the web."),
        gmaps=[gm("通天閣", "Tsutenkaku", 34.65250, 135.50630, "通天閣"),
               gm("串かつだるま 新世界総本店", "Kushikatsu Daruma (original shop)", 34.65170, 135.50610, "串かつだるま 新世界総本店"),
               gm("恵美須町駅", "Ebisucho Station", 34.65480, 135.50570, "恵美須町駅")],
        links=[link("official", "通天閣 公式サイト（営業案内）", "Tsutenkaku (official)", "https://www.tsutenkaku.co.jp/annai/"),
               link("official", "串かつだるま 公式サイト（店舗）", "Kushikatsu Daruma (official, shops, Japanese)", "https://www.kushikatu-daruma.com/location/")],
        rows=[row("hours", "通天閣 9:00〜21:45（最終入場21:15）。12月25日と2月1日は9:30から。年末年始は時間が変わります", "Tsutenkaku 9:00–21:45 (last entry 21:15); from 9:30 on 25 Dec and 1 Feb; different hours around New Year"),
              row("fee", "通天閣 一般展望台 大人1,500円（12月30日〜1月3日は1,800円）。屋外の展望台やすべり台は別料金", "Tsutenkaku general observatory ¥1,500 (¥1,800 from 30 Dec to 3 Jan). The open-air deck and the slide cost extra"),
              row("hours", "串かつだるま（新世界の各店）平日11:00〜22:30、土日祝10:30〜22:30（注文は閉店の30分前まで）。年中無休", "Kushikatsu Daruma (Shinsekai shops) weekdays 11:00–22:30, weekends and holidays 10:30–22:30 (last orders 30 min before closing). Open every day")],
        tip=T("通天閣の時間・料金・入場時間の予約は通天閣の公式サイト（営業案内）、串かつだるまの時間・支払い・席数は公式サイトの店舗ページで確認しました。串カツの値段は書いていません。",
              "Tsutenkaku hours, fee and entry-time booking from its official site; Kushikatsu Daruma hours, payment and seats from its official shop pages. Skewer prices are not given."),
        source=["https://www.tsutenkaku.co.jp/annai/", "https://www.kushikatu-daruma.com/location/shinsekai", SRC_PLANNER]),
    shitennoji=dict(
        name=T("四天王寺", "Shitennoji temple"), kind=T("お寺", "Temple"),
        blurb=T("聖徳太子が593年に建てたと伝わるお寺。新世界のにぎわいから歩いて14分で、急に静かになります。境内は無料。",
                "Said to have been founded by Prince Shotoku in 593. Fourteen minutes’ walk from the noise of Shinsekai, and suddenly quiet. The grounds are free."),
        lat=34.65370, lng=135.51640,
        caution=T("お堂と中心伽藍は16:00まで（4〜9月は16:30）", "Halls and central precinct close 16:00 (16:30 Apr–Sep)"),
        body=T("境内は24時間入れて、歩くだけなら無料です。南から中門・五重塔・金堂・講堂が一直線に並ぶ「四天王寺式」の伽藍は、有料の中心伽藍の中に入ると見られます。建物は戦後の再建ですが、並び方は創建のころのままです。\n\n"
               "串カツのあとの腹ごなしにちょうどいい距離で、食べ歩きの1日の中で座って休める場所でもあります。亀がたくさんいる池と石舞台のあたりにベンチがあります。\n\n"
               "毎月21日（お大師さん）と22日（お太子さん）は縁日で、境内に骨董や古着、食べ物の露店が出ます。この2日は中心伽藍も無料。日が合えば、ここを長めにとる価値があります。",
               "The grounds are open round the clock and free to walk. The “Shitennoji layout”, with middle gate, five-storey pagoda, main hall and lecture hall in one line from the south, is seen inside the paid central precinct. The buildings are post-war, but the plan is that of the founding.\n\n"
               "It is the right distance to walk off the kushikatsu, and a place to sit down in a day of eating on your feet: there are benches by the turtle pond and the stone stage.\n\n"
               "On the 21st and 22nd of every month a temple market fills the grounds with antiques, old clothes and food stalls, and the central precinct is free on those two days. If your date matches, give this stop more time."),
        gmaps=[gm("四天王寺", "Shitennoji", 34.65370, 135.51640, "四天王寺 大阪"),
               gm("四天王寺前夕陽ケ丘駅", "Shitennoji-mae Yuhigaoka Station", 34.65740, 135.51480, "四天王寺前夕陽ケ丘駅")],
        links=[link("official", "四天王寺 公式サイト（拝観案内）", "Shitennoji (official, admission, Japanese)", "https://www.shitennoji.or.jp/admission.html")],
        rows=[row("hours", "お堂・中心伽藍・庭園 8:30〜16:30（10〜3月は16:00まで）。毎月21日は8:00〜17:00（10〜3月は16:30まで。10月21日は17:00まで）。境内は24時間", "Halls, central precinct and garden 8:30–16:30 (to 16:00 October–March). On the 21st, 8:00–17:00 (to 16:30 October–March; 17:00 on 21 Oct). The grounds never close"),
              row("fee", "境内は無料。中心伽藍 500円、庭園 300円、宝物館 500円（毎月21日・22日は中心伽藍が無料）", "Grounds free. Central precinct ¥500, garden ¥300, treasure house ¥500 (central precinct free on the 21st and 22nd)"),
              row("closed", "庭園の休園日は公式サイトの拝観案内に書かれていません（要確認）", "Garden closing days are not given on the official admission page (please check)")],
        tip=T("時間と料金は四天王寺の公式サイト（拝観ご案内）で確認しました。歩く時間は地図からの目安です。", "Hours and fees from the official Shitennoji site. Walking times are estimates from the map."),
        source=["https://www.shitennoji.or.jp/admission.html", SRC_PLANNER]),
    harukas=dict(
        name=T("あべのハルカス（展望台 ハルカス300）", "Abeno Harukas (Harukas 300 observatory)"), kind=T("展望台（寄り道）", "Observation deck (detour)"),
        blurb=T("高さ300mのビルの58〜60階。ガラス張りの回廊を一周して、大阪平野を端から端まで見下ろします。",
                "Floors 58–60 of a 300 m tower. Walk the glass-walled gallery for a view right across the Osaka plain."),
        lat=34.64590, lng=135.51390,
        caution=T("切符売り場は16階。再入場はできません", "Ticket counter on the 16th floor. No re-entry"),
        body=T("天王寺駅の真上に建つ、高さ300mのビルです。四天王寺からは歩いて約15分、通天閣からは天王寺公園の芝生広場「てんしば」を抜けて約18分。\n\n"
               "展望台へは、まず「ハルカスシャトルエレベーター」で16階の切符売り場へ。そこから専用エレベーターで60階まで上ります。60階は四方がガラスの回廊で、足元まで窓。晴れた日は、北に梅田のビル、西に大阪湾と明石海峡大橋、東に生駒山まで見えます。\n\n"
               "高さはこちらが大阪でいちばん。ただし中はガラス越しで、夜は窓に光が映りこみます。夕日と夜景を外の風で感じたいなら梅田スカイビル、高さと昼の遠くの眺めならハルカス、と覚えてください。両方上る必要はありません。\n\n"
               "最後の写真は2023年2月の朝、ビルの中ほどの階のカフェの窓からぼくが撮ったもの。ほかはネットから借りた写真です。",
               "A 300 m tower standing directly over Tennoji Station. About 15 minutes on foot from Shitennoji, or 18 from Tsutenkaku across Tenshiba, the lawn of Tennoji Park.\n\n"
               "For the observatory, first take the Harukas Shuttle lift to the ticket counter on the 16th floor, then a dedicated lift to the 60th. The 60th floor is a gallery glazed on all four sides, with windows down to your feet. On clear days you see the Umeda towers to the north, Osaka Bay and the Akashi Kaikyo Bridge to the west, and Mt. Ikoma to the east.\n\n"
               "This is the highest view in Osaka. But you are behind glass, and at night the windows pick up reflections. Remember it like this: the Umeda Sky Building for sunset and night in the open air, Harukas for height and long daytime views. You do not need both.\n\n"
               "The last photo is mine, taken one morning in February 2023 from a café window partway up the building. The others are borrowed from the web."),
        gmaps=[gm("あべのハルカス", "Abeno Harukas", 34.64590, 135.51390, "あべのハルカス")],
        links=[link("official", "ハルカス300 公式サイト", "Harukas 300 (official)", "https://www.abenoharukas-300.jp/observatory/", "https://www.abenoharukas-300.jp/en/observatory/")],
        rows=[row("hours", "9:00〜22:00（最終入場21:30）", "9:00–22:00 (last entry 21:30)"),
              row("fee", "当日券 大人2,200円（16階の窓口かWEB）。前の日までにWEBで買うと1,980円。エンジョイエコカードを見せると当日料金から10%引き", "Same-day ticket ¥2,200 (16th-floor counter or online); ¥1,980 if bought online by the day before. 10% off the same-day price with an Enjoy Eco Card")],
        tip=T("時間と料金はハルカス300の公式サイトで確認しました。エンジョイエコカードの割引は2026年11月21日の確認です。", "Hours and fees from the official Harukas 300 site. The Enjoy Eco Card discount was checked on 21 Nov 2026."),
        source=["https://www.abenoharukas-300.jp/observatory/", "https://www.abenoharukas-300.jp/observatory/ticket/"]),
    sumiyoshi=dict(
        name=T("住吉大社", "Sumiyoshi Taisha shrine"), kind=T("神社（寄り道）", "Shrine (detour)"),
        blurb=T("朱色の太鼓橋を渡ってお参りする、全国の住吉神社の総本社。天王寺から路面電車で17分。",
                "Head shrine of all the Sumiyoshi shrines, reached over a steep vermilion bridge. 17 minutes by tram from Tennoji."),
        lat=34.61260, lng=135.49300,
        caution=T("外の門は16:00、本殿のまわりは17:00まで", "Outer gates close 16:00, inner precinct 17:00"),
        body=T("大阪の人が「すみよっさん」と呼ぶ、初詣でいちばんにぎわう神社です。池にかかる反橋（そりはし・太鼓橋）は、渡るだけでおはらいになるといわれる急な橋。その奥に、国宝の本殿が4つ、縦に3つと横に1つという珍しい並びで建っています。屋根がまっすぐな「住吉造」は、神社の建物でいちばん古い形のひとつです。\n\n"
               "行きは、あべのハルカスの前の天王寺駅前から阪堺電車（はんかいでんしゃ）で。道路の上をゴトゴト走る路面電車で、住吉鳥居前まで17分・240円。降りたら目の前が鳥居です。帰りは南海の住吉大社駅（歩いて3分）からなんばへ10分・240円。\n\n"
               "往復を入れて1時間半みてください。時間割には入っていないので、入れる日は四天王寺か、そのあとの1か所を外します。\n\n"
               "阪堺電車の写真は2023年8月に天王寺駅前でぼくが撮ったもの。神社の写真はネットから借りました。",
               "“Sumiyossan” to people in Osaka, and the city’s busiest shrine at New Year. The steep arched Sorihashi bridge over the pond is said to purify you just by crossing. Beyond stand four main halls, all National Treasures, in an unusual formation of three in a row and one beside. Their straight-roofed Sumiyoshi-zukuri style is among the oldest forms of shrine building.\n\n"
               "Go by Hankai tram from Tennoji-ekimae, in front of Abeno Harukas: a streetcar rattling down the road, 17 minutes and ¥240 to Sumiyoshi-toriimae, which is right at the torii. Come back from Nankai’s Sumiyoshi-taisha Station (3 minutes’ walk) to Namba, 10 minutes, ¥240.\n\n"
               "Allow an hour and a half including the ride. It is outside the timetable, so on a day you add it, drop Shitennoji or one stop after it.\n\n"
               "The tram photos are mine, taken at Tennoji-ekimae in August 2023. The shrine photos are borrowed from the web."),
        time=T("寄るなら往復を入れて約1時間半（16時までに着く）", "about 1 h 30 min including the ride (arrive before 16:00)"),
        gmaps=[gm("住吉大社", "Sumiyoshi Taisha", 34.61260, 135.49300, "住吉大社"),
               gm("阪堺電車 天王寺駅前", "Hankai tram, Tennoji-ekimae", 34.64600, 135.51290, "阪堺電車 天王寺駅前停留場")],
        links=[link("official", "住吉大社 公式サイト", "Sumiyoshi Taisha (official)", "https://www.sumiyoshitaisha.net/"),
               link("timetable", "阪堺電車 公式サイト", "Hankai Tramway (official, Japanese)", "http://www.hankai.co.jp/")],
        rows=[row("hours", "開門 6:00（10〜3月は6:30）。外の門は16:00、本殿のまわり（御垣内）は17:00に閉まります", "Opens 6:00 (6:30 October–March). Outer gates close at 16:00, the inner precinct at 17:00"),
              row("fee", "お参りは無料", "Free"),
              row("train", "天王寺駅前 →（阪堺電車 上町線）→ 住吉鳥居前 17分・240円", "Tennoji-ekimae → (Hankai Uemachi Line) → Sumiyoshi-toriimae, 17 min, ¥240"),
              row("train", "帰り：住吉大社 →（南海）→ なんば 10分・240円", "Back: Sumiyoshi-taisha → (Nankai) → Namba, 10 min, ¥240")],
        tip=T("門の時間と駅からの道は住吉大社の公式サイト、電車は乗換案内で確認しました（2026年11月21日）。阪堺電車はエンジョイエコカードでは乗れません（1日乗り放題の「てくてくきっぷ」は700円）。",
              "Gate hours and access from the shrine’s official site; trains from a route planner (21 Nov 2026). The Hankai tram is not covered by the Enjoy Eco Card (its own 1-day ticket is ¥700)."),
        checked="2026-11-21", source=["https://www.sumiyoshitaisha.net/", SRC_PLANNER]),
    kaiyukan=dict(
        name=T("海遊館", "Osaka Aquarium Kaiyukan"), kind=T("水族館（半日コース）", "Aquarium (half a day)"),
        blurb=T("ジンベエザメが泳ぐ大きな水槽を、8階から螺旋に下りながら見ます。町の西の端なので、行くなら半日つぶれます。",
                "Spiral down from the 8th floor around a huge tank with whale sharks. It is at the far west of the city: going costs half a day."),
        caution=T("ルートから遠く、往復と見学で約4時間。入る時間が決まります", "Far off the route: about 4 hours with travel. Entry is by time slot"),
        lat=34.65450, lng=135.42900,
        body=T("正直に書くと、このルートに足すには遠い場所です。梅田から地下鉄で約26分、中の見学に2時間半ほど。往復を入れると4時間はかかるので、入れる日は大阪城か、新世界〜四天王寺のどちらかをやめてください。雨の日や、子ども連れの日の主役に向いています。\n\n"
               "見どころは、深さ9mの「太平洋」水槽。8階から始まって、同じ水槽のまわりを螺旋に下りていくので、ジンベエザメやエイを水面近くからも底からも見られます。\n\n"
               "料金は日によって変わる仕組みで、入る時間も決まります。行く日が決まったら、公式サイトで日時を指定するeチケットを買っておくと、窓口で待たずに入れます。当日に窓口で買うと、希望の時間に入れないことがあります。\n\n"
               "行き方は中央線の大阪港駅（1番出口）から歩いて約5分。写真はネットから借りたものです。",
               "To be honest, this is too far to simply add to the route. It is about 26 minutes by subway from Umeda and a visit takes around two and a half hours: four hours with travel. On a day you include it, drop either the castle or the Shinsekai–Shitennoji stretch. It suits a rainy day, or a day built around children.\n\n"
               "The centrepiece is the 9 m deep Pacific Ocean tank. You start on the 8th floor and spiral down around the same tank, so you see the whale sharks and rays from near the surface and from the bottom.\n\n"
               "Admission varies by date and entry is by time slot. Once your day is fixed, buy a dated, timed e-ticket on the official site and you walk straight in; at the window on the day you may not get the time you want.\n\n"
               "Access: about 5 minutes’ walk from exit 1 of Osakako Station on the Chuo Line. The photos are borrowed from the web."),
        time=T("行くなら見学に約2時間半（往復を入れて約4時間）", "about 2 h 30 min inside (about 4 hours with travel)"),
        gmaps=[gm("海遊館", "Kaiyukan", 34.65450, 135.42900, "海遊館")],
        links=[link("official", "海遊館 公式サイト（入館料）", "Kaiyukan (official, tickets)", "https://www.kaiyukan.com/info/ticket/kaiyukan/", "https://www.kaiyukan.com/language/eng/")],
        rows=[row("fee", "日によって変わります（価格変動制）。公式サイトのカレンダーで確認を（要確認）", "Varies by date (dynamic pricing). Check the calendar on the official site"),
              row("hours", "日によって変わります。公式サイトで確認を（要確認）", "Varies by date. Check the official site"),
              row("train", "梅田 →（御堂筋線・本町で中央線に乗り換え）→ 大阪港 約26分・290円。駅から歩いて約5分", "Umeda → (Midosuji Line, change at Hommachi to the Chuo Line) → Osakako, about 26 min, ¥290; then 5 minutes’ walk")],
        tip=T("料金の仕組みと駅からの時間は海遊館の公式サイト（2026年11月21日）、電車は乗換案内で確認しました。その日の料金と時間は公式サイトでしか分かりません。",
              "Pricing system and access from the official Kaiyukan site (21 Nov 2026); trains from a route planner. The day’s price and hours are only on the official site."),
        verified=False, source=["https://www.kaiyukan.com/info/ticket/kaiyukan/", SRC_PLANNER]),
    umekita=dict(
        name=T("うめきた公園（グラングリーン大阪）", "Umekita Park (Grand Green Osaka)"), kind=T("公園・休憩", "Park & rest stop"),
        lat=34.70300, lng=135.49310,
        body=T("貨物駅の跡地に2024年9月にできた、駅前とは思えない広さの公園です。梅田駅・大阪駅から梅田スカイビルへは、ここを通り抜けるのがいちばん気持ちのいい道。大阪駅の「うめきた地下口」か、グランフロント大阪の北側から入れます。\n\n"
               "大きな屋根のイベント広場の下は、雨の日でも座れる休憩場所。芝生に出ると、ビルにかこまれた空の真ん中に、2本の塔を上でつないだスカイビルが見えます。朝から歩いた足を休めるのに、芝生に座るのがちょうどいい所です。\n\n"
               "入るのは無料。写真は2025年6月の昼と、2026年9月の夜。",
               "Opened in September 2024 on a former freight yard, and far bigger than you expect in front of a main station. It is the pleasantest way to walk from Umeda or Osaka Station to the Umeda Sky Building. Enter from the station’s Umekita underground gate or from the north side of Grand Front Osaka.\n\n"
               "Under the great roof of the event plaza you can sit down even in the rain. Out on the lawn, the Sky Building, two towers joined at the top, stands in the middle of the sky between the high-rises. After a day on your feet, the grass is the place to sit.\n\n"
               "Free to enter. Photos: daytime in June 2025, night in September 2026."),
        gmaps=[gm("うめきた公園", "Umekita Park", 34.70300, 135.49310, "うめきた公園 グラングリーン大阪")],
        links=[link("official", "グラングリーン大阪 公式サイト", "Grand Green Osaka (official)", "https://umekita.com/")],
        rows=[row("fee", "無料", "Free")],
        tip=T("電車は乗換案内で確認しました。公園の細かい決まりは公式サイトにあります。", "Trains from a route planner. Park rules are on the official site."),
        source=["https://umekita.com/", SRC_PLANNER]),
    skybldg=dict(
        name=T("梅田スカイビル 空中庭園展望台", "Umeda Sky Building: Kuchu Teien Observatory"), kind=T("展望台・夕日と夜景", "Observation deck: sunset & night view"),
        lat=34.70530, lng=135.49060,
        caution=T("屋上は吹きさらし。冬は上着を", "The rooftop is open to the wind: bring a layer in winter"),
        notices=[notice("屋上は屋根も窓もありません", "The rooftop has no roof and no glass",
                        "風が強く、冬はかなり冷えます。上着を1枚。当日券は39階で買います（現金かカード）。日付を選ぶWEBチケットもあります。施設の点検で早く閉まる日があります（次は2027年4月18日、18:00まで）。",
                        "It is windy and cold in winter, so bring an extra layer. Same-day tickets are sold on the 39th floor (cash or card); dated web tickets are also available. It closes early on inspection days (next: 18 April 2027, to 18:00).")],
        body=T("2本のビルを上でつないだ、高さ173mの展望台です。35階までエレベーターで上り、そこから宙に浮いたガラスのエスカレーターで39階へ。さらに階段を上ると、屋上の「スカイ・ウォーク」に出ます。ここは窓のない外の回廊で、風を受けながら360度を一周できます。\n\n"
               "夕日を見るならここ、というのがこの地図のおすすめです。屋上が外なのでガラスの映りこみがなく、西側が淀川と大阪湾の方向に開けていて、夕日がビルにかくれません。\n\n"
               "日の入りの30〜40分前に着くようにしてください。日の入りの目安は、11〜1月が16時50分〜17時10分ごろ、春と秋が18時前後、6〜7月が19時10分ごろです。\n\n"
               "展望台の写真はネットから借りたものです。",
               "Two towers joined at the top, with a deck 173 m up. Ride the lift to the 35th floor, then a glass escalator that hangs in mid-air to the 39th. One more flight of stairs brings you out onto the rooftop Sky Walk: an open-air ring with no windows, where you walk the full 360 degrees in the wind.\n\n"
               "For sunset, this map says come here. The roof is outdoors, so there are no reflections in glass, and the west side is open towards the Yodo river and Osaka Bay, so no building hides the sun.\n\n"
               "Arrive 30–40 minutes before sunset. Sunset is roughly 16:50–17:10 from November to January, around 18:00 in spring and autumn, about 19:10 in June and July.\n\n"
               "The observatory photos are borrowed from the web."),
        gmaps=[gm("梅田スカイビル", "Umeda Sky Building", 34.70530, 135.49060, "梅田スカイビル 空中庭園展望台"),
               gm("地下鉄 梅田駅", "Umeda subway station", 34.70330, 135.49790, "梅田駅 御堂筋線")],
        links=[link("official", "空中庭園展望台 公式サイト（営業時間・チケット）", "Kuchu Teien Observatory (official)", "https://www.skybldg.co.jp/observatory/information/", "https://www.skybldg.co.jp/en/"), PLANNER],
        rows=[row("hours", "9:30〜22:30（最終入場22:00）。予告なく変わることがあります", "9:30–22:30 (last entry 22:00); may change without notice"),
              row("fee", "大人2,000円（4歳〜小学生500円）。エンジョイエコカードを見せると10%引き", "¥2,000 (age 4 to primary school ¥500). 10% off with an Enjoy Eco Card")],
        tip=T("時間・料金・切符の買い方は空中庭園展望台の公式サイトで確認しました。エンジョイエコカードの割引は2026年11月21日の確認です。日の入りの時刻はおよその目安です。",
              "Hours, fee and ticketing from the official observatory site. The Enjoy Eco Card discount was checked on 21 Nov 2026. Sunset times are approximate."),
        source=["https://www.skybldg.co.jp/observatory/information/", SRC_PLANNER]),
    nakanoshima=dict(
        name=T("中之島・中央公会堂と淀屋橋の無料展望テラス", "Nakanoshima: Central Public Hall & the free Yodoyabashi terrace"), kind=T("近代建築・無料の夜景", "Architecture & a free night view"),
        lat=34.69330, lng=135.50390,
        caution=T("テラスの開く時間は要確認", "Terrace hours unconfirmed"),
        body=T("淀屋橋（よどやばし）駅の真上のビル「淀屋橋ステーションワン」の30階に、「淀屋橋スカイテラス」があります。2025年9月から誰でも無料で入れるようになった展望スペースで、中之島と梅田のビル群を見下ろせます。ぼくは夜に上りました（写真は2025年12月と2026年4月）。有料の展望台に行かない日は、ここで夜景を見て締めくくれます。\n\n"
               "駅から東へ歩いて約5分の中之島（なかのしま）には、1918年にできた赤レンガの大阪市中央公会堂。国の重要文化財で、夜は明かりがつきます。昼に来るなら、となりの東洋陶磁美術館やバラ園も。\n\n"
               "京都へ帰る人には、ここがいちばん楽な出口です。淀屋橋は京阪の始発駅なので、特急に並べば座って帰れます。",
               "On the 30th floor of Yodoyabashi Station One, the tower right above Yodoyabashi Station, is the Yodoyabashi Sky Terrace. Opened to everyone free of charge in September 2025, it looks down on Nakanoshima and the Umeda skyline. I went up at night (photos: December 2025 and April 2026). On a day without a paid observatory, this is where to end with a night view.\n\n"
               "About 5 minutes’ walk east of the station, on Nakanoshima island, stands the red-brick Osaka City Central Public Hall of 1918, an Important Cultural Property, lit up at night. By day there are also the Museum of Oriental Ceramics next door and a rose garden.\n\n"
               "For anyone going back to Kyoto this is the easiest exit: Yodoyabashi is where Keihan trains start, so queue for a limited express and you get a seat."),
        gmaps=[gm("淀屋橋ステーションワン", "Yodoyabashi Station One", 34.69230, 135.50140, "淀屋橋ステーションワン"),
               gm("大阪市中央公会堂", "Osaka City Central Public Hall", 34.69330, 135.50390, "大阪市中央公会堂")],
        links=[link("official", "大阪市中央公会堂 公式サイト", "Osaka City Central Public Hall (official)", "https://osaka-chuokokaido.com/"),
               link("info", "淀屋橋スカイテラスの一般公開（京阪ホールディングスほかの発表）", "Opening of the Yodoyabashi Sky Terrace (press release, Japanese)", "https://newscast.jp/news/4690043")],
        rows=[row("fee", "淀屋橋スカイテラスは入場無料。公会堂の外観は自由に見られます", "The Yodoyabashi Sky Terrace is free. The hall’s exterior is free to see"),
              row("hours", "スカイテラスの開く時間は公式の資料で確認できませんでした（旅行サイトでは10:00〜23:00と紹介されています。要確認）", "Terrace hours could not be confirmed in an official source (travel sites give 10:00–23:00; please check)"),
              row("train", "京都へ：淀屋橋（京阪特急・始発）→ 三条 51分・490円。21:00発→21:51着、21:15発→22:06着。最終の特急は23:33発（三条0:22着）", "To Kyoto: Yodoyabashi (Keihan limited express, starts here) → Sanjo, 51 min, ¥490. 21:00 → 21:51, 21:15 → 22:06. The last limited express leaves at 23:33 (Sanjo 0:22)")],
        tip=T("スカイテラスが無料で一般公開されていることは、京阪ホールディングスと中央日本土地建物の発表（2025年）で確認しました。開く時間は公式の資料が見つからず、要確認です。電車は乗換案内です。",
              "That the terrace is open to the public free of charge is from the 2025 press release by Keihan Holdings and Chuo-Nittochi. No official source for its hours was found. Trains from a route planner."),
        verified=False, source=["https://newscast.jp/news/4690043", SRC_PLANNER]),
    hozenji=dict(
        name=T("法善寺横丁・水掛不動", "Hozenji Yokocho & the moss-covered Fudo"), kind=T("路地・お寺", "Alley & temple"),
        blurb=T("道頓堀のにぎわいから1本入った、石畳の細い路地。提灯がともる夕方からがいちばんです。苔におおわれたお不動さんに水をかけてお参りします。",
                "A narrow stone-paved alley one street back from the noise of Dotonbori, at its best from dusk when the lanterns come on. Pour water over the moss-covered Fudo and pray."),
        lat=34.66790, lng=135.50240,
        body=T("千日前のアーケードの西側に、幅3mほどの石畳の路地が2本あります。割烹や串カツ、バーの小さな店が並び、提灯がともるといちばん雰囲気が出ます。\n\n"
               "路地の奥の法善寺には、全身が苔でおおわれた水掛不動さん。柄杓で水をかけてお願いごとをします。お参りは無料で、いつでもできます。となりの「夫婦善哉（めおとぜんざい）」は、1人前が2つのお椀で出てくるぜんざいの店です（時間は公式サイトで確認できませんでした）。\n\n"
               "夜に備えて座って休むなら、すぐ近くの丸福珈琲店 千日前本店へ。昔ながらの喫茶店で、8:00から23:00まで開いています。",
               "West of the Sennichimae arcade lie two stone-paved lanes barely 3 m wide, lined with small kappo restaurants, kushikatsu counters and bars. They look their best when the lanterns are lit.\n\n"
               "At the end stands Hozenji and its Mizukake Fudo statue, covered head to foot in moss. Ladle water over it and make a wish. It is free and open at any hour. Next door, Meoto Zenzai serves one portion of sweet red-bean soup in two bowls (its hours could not be confirmed on its official site).\n\n"
               "To sit down before the evening, Marufuku Coffee’s Sennichimae main shop is close by: an old-style coffee house, open 8:00 to 23:00."),
        gmaps=[gm("法善寺 水掛不動", "Hozenji (Mizukake Fudo)", 34.66790, 135.50240, "法善寺 水掛不動尊"),
               gm("丸福珈琲店 千日前本店", "Marufuku Coffee (Sennichimae main shop)", 34.66690, 135.50330, "丸福珈琲店 千日前本店")],
        links=[link("info", "法善寺横丁（大阪観光局）", "Hozenji Yokocho (Osaka Info)", "https://osaka-info.jp/spot/hozenji-yokocho/", "https://osaka-info.jp/en/spot/hozenji-yokocho/"),
               link("official", "丸福珈琲店 千日前本店（公式）", "Marufuku Coffee, Sennichimae (official, Japanese)", "https://marufukucoffeeten.com/store/marufukucoffee-sennichimae")],
        rows=[row("fee", "お参りは無料", "Free"),
              row("hours", "路地とお不動さんはいつでも。お店は夕方からの所が多い", "The lanes and the Fudo are open at any hour; many restaurants open from the evening"),
              row("hours", "丸福珈琲店 千日前本店 8:00〜23:00（予告なく変わることがあります。モーニングは平日だけ）", "Marufuku Coffee Sennichimae 8:00–23:00 (may change without notice; breakfast sets on weekdays only)")],
        tip=T("丸福珈琲店の時間は公式サイトの店舗ページで確認しました。路地は公道なので自由に歩けます。お寺と夫婦善哉の時間は公式の案内で確認できていません。",
              "Marufuku’s hours are from its official shop page. The lanes are public streets. Hours for the temple office and Meoto Zenzai could not be confirmed officially."),
        source=["https://marufukucoffeeten.com/store/marufukucoffee-sennichimae", "https://osaka-info.jp/spot/hozenji-yokocho/"]),
    dotonbori=dict(
        name=T("道頓堀・戎橋（グリコの看板）", "Dotonbori & Ebisubashi (the Glico sign)"), kind=T("夜の繁華街・たこ焼き・晩ごはん", "Night district, takoyaki & dinner"),
        lat=34.66905, lng=135.50125, cash=True,
        caution=T("今井 本店は水曜休み。クルーズは運航を要確認", "Imai closed Wednesdays. Check that the cruise is running"),
        notices=[notice("店の休みとクルーズ", "Closing days and the cruise",
                        "うどんの道頓堀 今井 本店は水曜（祝日は営業）と第4火曜（12月を除く）が休みで、注文は21:00まで。会津屋 ナンバ店は奇数月の第3木曜が休み。とんぼりリバークルーズは運航会社のサイトが点検中で、時間と料金を公式に確認できませんでした。乗る前に乗り場（ドン・キホーテ道頓堀店1階）で確かめてください。",
                        "The udon restaurant Dotonbori Imai is closed on Wednesdays (open if a holiday) and the 4th Tuesday (except December), with last orders at 21:00. Aizuya’s Namba shop closes on the 3rd Thursday of odd-numbered months. The Tombori River Cruise operator’s website is under maintenance, so times and fares could not be confirmed officially: check at the ticket desk (ground floor of Don Quijote Dotonbori) before you count on it.")],
        body=T("戎橋の西側の欄干が、グリコの看板の定位置です。橋の上は一日じゅう人でいっぱいなので、橋のたもとの階段で川沿いの遊歩道「とんぼりリバーウォーク」に下りるのがおすすめ。水面の高さから、看板と行き交う船を落ち着いて撮れます。看板は日が暮れてからが本番です。\n\n"
               "まず、たこ焼き。道頓堀の通りに何軒も並んでいて、どこも店先で買って立って食べます。行列の長さより、焼き上がりの回転が速い店を選ぶと待ちません。券売機か現金の店が多いです。"
               "ぼくが食べたのは、なんばの地下街「NAMBAなんなん」にある会津屋（あいづや）の元祖たこ焼き。ソースをかけずに、だしの味で食べる小ぶりのたこ焼きです（写真は2023年6月）。戎橋から歩いて7分ほど、御堂筋線のなんば駅のすぐ近くで、22:00まで開いています。\n\n"
               "座って晩ごはんにするなら、選び方は2つ。うどんとだしなら、道頓堀の通りにある「道頓堀 今井 本店」（11:30〜21:30）。昼に串カツを食べそこねた人や、もう一度食べたい人は「串かつだるま」の道頓堀店か法善寺店（どちらも22:30まで）。道頓堀店は140席あり、カードも使えます。\n\n"
               "川を20分ほどで回る「とんぼりリバークルーズ」は、夜の看板を水の上から見られます。乗り場の受付で時間を指定した当日券を買うか、WEBで予約します。\n\n"
               "写真の昼の道頓堀は2023年12月、夜は2024年8月。",
               "The west railing of Ebisubashi bridge is the classic spot for the Glico sign. The bridge is packed all day, so take the steps at its foot down to the Tombori River Walk: from water level you can photograph the signs and the passing boats in peace. The signs come into their own after dark.\n\n"
               "Takoyaki first. Stands line the main street; you buy at the front and eat standing. Choose a stall that turns batches over quickly rather than the longest queue. Most take a ticket machine or cash. "
               "The one I ate was the original takoyaki at Aizuya, in the NAMBA Nannan underground mall: small, dashi-flavoured, eaten with no sauce (photo: June 2023). It is about 7 minutes’ walk from Ebisubashi, right by Namba Station on the Midosuji Line, and open until 22:00.\n\n"
               "For a sit-down dinner there are two ways to go. For udon and dashi, Dotonbori Imai’s main shop on the main street (11:30–21:30). If you missed kushikatsu at lunch, or want it again, Kushikatsu Daruma’s Dotonbori or Hozenji shop (both until 22:30); the Dotonbori shop has 140 seats and takes cards.\n\n"
               "The Tombori River Cruise, about 20 minutes on the canal, shows you the signs from the water at night. Buy a timed same-day ticket at the desk by the pier, or book online.\n\n"
               "Daytime photos: December 2023; night: August 2024."),
        gmaps=[gm("戎橋", "Ebisubashi bridge", 34.66905, 135.50125, "戎橋 道頓堀"),
               gm("会津屋 ナンバ店", "Aizuya (NAMBA Nannan)", 34.66540, 135.50130, "会津屋 ナンバ店 NAMBAなんなん"),
               gm("道頓堀 今井 本店", "Dotonbori Imai (main shop)", 34.66860, 135.50250, "道頓堀 今井 本店"),
               gm("串かつだるま 道頓堀店", "Kushikatsu Daruma (Dotonbori)", 34.66870, 135.50290, "串かつだるま 道頓堀店")],
        links=[link("official", "道頓堀 今井 本店（公式）", "Dotonbori Imai main shop (official, Japanese)", "https://www.d-imai.com/shops/honten/"),
               link("official", "会津屋 公式サイト（店舗）", "Aizuya (official, shops, Japanese)", "https://www.aiduya.com/shop/"),
               link("official", "串かつだるま 道頓堀店（公式）", "Kushikatsu Daruma Dotonbori (official, Japanese)", "https://www.kushikatu-daruma.com/location/doutonbori"),
               link("info", "とんぼりリバークルーズ（大阪観光局）", "Tombori River Cruise (Osaka Info)", "https://osaka-info.jp/spot/tombori-river-cruise/", "https://osaka-info.jp/en/spot/tombori-river-cruise/")],
        rows=[row("hours", "会津屋 ナンバ店 11:00〜22:00（奇数月の第3木曜休み）", "Aizuya Namba shop 11:00–22:00 (closed 3rd Thursday of odd-numbered months)"),
              row("hours", "道頓堀 今井 本店 11:30〜21:30（注文は21:00まで。鍋料理は19:30まで）。水曜（祝日は営業）・第4火曜（12月を除く）休み。現金・電子マネー・カード", "Dotonbori Imai main shop 11:30–21:30 (last orders 21:00; hot-pot dishes 19:30). Closed Wednesdays (open on holidays) and the 4th Tuesday (except December). Cash, e-money and cards"),
              row("hours", "串かつだるま 道頓堀店 平日11:00〜22:30、土日祝10:30〜22:30（法善寺店は平日11:30から）。年中無休。1人1杯の飲み物を注文", "Kushikatsu Daruma Dotonbori: weekdays 11:00–22:30, weekends and holidays 10:30–22:30 (Hozenji shop from 11:30 on weekdays). Open every day. One drink per person"),
              row("hours", "とんぼりリバークルーズ：大阪観光局の案内では11:00〜21:00、毎時0分・30分発、約20分、大人2,000円（要確認）", "Tombori River Cruise: per the Osaka tourism bureau, 11:00–21:00, on the hour and half-hour, about 20 min, adults ¥2,000 (please check)")],
        tip=T("今井・会津屋・串かつだるまの時間と休みは、それぞれの公式サイトの店舗ページで確認しました。クルーズは運航会社（一本松海運）のサイトが点検中だったため、大阪観光局のサイトの内容です。たこ焼きの値段は変わりやすいので書いていません。",
              "Hours and closing days for Imai, Aizuya and Kushikatsu Daruma are from their official shop pages. The cruise operator’s site was under maintenance, so cruise details are from the Osaka tourism bureau’s site. Takoyaki prices change often, so none are given."),
        source=["https://www.d-imai.com/shops/honten/", "https://www.aiduya.com/shop/", "https://www.kushikatu-daruma.com/location/doutonbori", "https://osaka-info.jp/spot/tombori-river-cruise/", SRC_PLANNER]),
)

# ---------------------------------------------------------------------------
# コース。order＝番号の順、default＝最初から選ばれている場所（時間割どおり）、
# spots[id]＝そのコースでの blurb・行き方（pre）・次へ（post）・おすすめ訪問時間（time）・電車の行（rows）
# ---------------------------------------------------------------------------
HOME_KYOTO_ROW = row("train", "京都へ帰る人：なんば →（御堂筋線）→ 淀屋橋 6分・190円 → 京阪特急で三条へ51分・490円（最終の特急は淀屋橋23:33発）。阪急は大阪梅田23:45発の急行が京都河原町行きの最後、JRは大阪0:00発の新快速が最後。なんばを23時までに出れば間に合います",
                     "Going back to Kyoto: Namba → (Midosuji Line) → Yodoyabashi, 6 min, ¥190 → Keihan limited express to Sanjo, 51 min, ¥490 (last limited express leaves Yodoyabashi 23:33). The last Hankyu train to Kyoto-Kawaramachi is the 23:45 express from Osaka-Umeda; the last JR is the 0:00 Special Rapid from Osaka. Leave Namba by 23:00 and you will make them")

LATE = dict(
    id="late", file="osaka.json",
    order=["kuromon", "shinsekai", "shitennoji", "harukas", "sumiyoshi", "kaiyukan", "castle", "tenmangu", "hozenji", "dotonbori", "nakanoshima", "umekita", "skybldg"],
    default=["kuromon", "shinsekai", "shitennoji", "castle", "hozenji", "dotonbori", "nakanoshima"],
    sections=[("kuromon", "kuromon", "日本橋", "Nippombashi", "朝は市場から", "Start at the market"),
              ("shinsekai", "sumiyoshi", "新世界・天王寺", "Shinsekai & Tennoji", "昼は通天閣の下で串カツ", "Kushikatsu under Tsutenkaku for lunch"),
              ("kaiyukan", "kaiyukan", "ベイエリア", "Bay area", "行くなら半日", "Half a day if you go"),
              ("castle", "tenmangu", "大阪城", "Osaka Castle", "昼の混雑を外して、15時ごろの天守閣へ", "The castle tower around 15:00, after the midday crush"),
              ("hozenji", "dotonbori", "ミナミ", "Minami", "日が暮れてからの道頓堀", "Dotonbori after dark"),
              ("nakanoshima", "skybldg", "淀屋橋・梅田", "Yodoyabashi & Umeda", "帰り道の夜景", "A night view on the way back")],
    spots=dict(
        kuromon=dict(
            blurb=T("ホテルを9時45分ごろに出て、まず市場へ。昼前のまだ歩きやすい時間に、焼きたての貝や串、果物を2〜3品つまみます。",
                    "Leave the hotel about 9:45 and start at the market. Before the lunchtime crowd, pick two or three things: grilled shellfish, skewers, fruit."),
            pre=T("梅田のホテルからは、御堂筋線でなんばへ（梅田9:48発→9:57着・240円）。なんば駅から東へ歩いて約10分です。千日前線に乗り換えて日本橋まで1駅乗ってもかまいません。難波・心斎橋のホテルからは歩いて行けます。",
                  "From a hotel in Umeda, take the Midosuji Line to Namba (9:48 → 9:57, ¥240) and walk east for about 10 minutes, or change to the Sennichimae Line for one stop to Nippombashi. From hotels around Namba or Shinsaibashi, just walk."),
            post=T("次の新世界へは、堺筋（さかいすじ）をまっすぐ南へ歩いて約20分。途中は電気とアニメの店が並ぶ「でんでんタウン」で、通天閣が正面に見えてきます。歩きたくなければ、日本橋から堺筋線で1駅の恵美須町（えびすちょう）へ（2分・190円）。3番出口を出ると通天閣のすぐ北側です。",
                   "For Shinsekai next, walk straight south down Sakaisuji avenue for about 20 minutes. The way runs through Den Den Town, the street of electronics and anime shops, with Tsutenkaku coming into view ahead. To skip the walk, ride the Sakaisuji Line one stop from Nippombashi to Ebisucho (2 min, ¥190); exit 3 comes out just north of the tower."),
            time=T("10:10〜11:10", "10:10–11:10"),
            rows=[row("train", "梅田9:48発 →（御堂筋線）→ なんば9:57着・240円。日本橋駅（堺筋線・千日前線）10番出口からすぐ", "Umeda 9:48 → (Midosuji Line) → Namba 9:57, ¥240. The market is right outside exit 10 of Nippombashi Station (Sakaisuji and Sennichimae lines)"),
                  row("train", "次へ：歩いて約20分。または日本橋 →（堺筋線）→ 恵美須町 2分・190円", "Next: about 20 minutes on foot, or Nippombashi → (Sakaisuji Line) → Ebisucho, 2 min, ¥190")]),
        shinsekai=dict(
            blurb=T("巨大なふぐやビリケンさんの看板が頭の上に並ぶ通りの先に、通天閣。店が開く11時台に着いて、お昼は串カツです。",
                    "A street hung with giant blowfish and Billiken signs, with Tsutenkaku tower at the end. Arrive in the 11 o’clock hour as the shops open, and have kushikatsu for lunch."),
            pre=T("黒門市場から歩いて約20分、または恵美須町駅の3番出口からすぐ。11時半に着けば、串カツの店はまだ昼の列が伸びる前です。",
                  "About 20 minutes’ walk from Kuromon Market, or right by exit 3 of Ebisucho Station. Arrive at 11:30 and the kushikatsu shops are not yet into their lunchtime queues."),
            post=T("次の四天王寺へは、通天閣から東へ歩いて約14分。天王寺動物園の北側の道をまっすぐ進みます。",
                   "For Shitennoji next, walk east from Tsutenkaku for about 14 minutes, straight along the road on the north side of Tennoji Zoo."),
            time=T("11:30〜12:55", "11:30–12:55"),
            rows=[row("train", "恵美須町駅（堺筋線）3番出口からすぐ。動物園前駅（御堂筋線）1番出口からはジャンジャン横丁を抜けて約8分", "Right by exit 3 of Ebisucho Station (Sakaisuji Line). From exit 1 of Dobutsuen-mae (Midosuji Line), about 8 minutes through Janjan Yokocho")]),
        shitennoji=dict(
            pre=T("通天閣から東へ歩いて約14分。",
                  "About 14 minutes’ walk east of Tsutenkaku."),
            post=T("次の大阪城へは、北へ歩いて約5分の四天王寺前夕陽ケ丘（してんのうじまえゆうひがおか）駅から谷町線で。谷町四丁目まで3駅・5分です。",
                   "For the castle next, walk about 5 minutes north to Shitennoji-mae Yuhigaoka Station and take the Tanimachi Line three stops (5 minutes) to Tanimachi 4-chome."),
            time=T("13:10〜13:55", "13:10–13:55"),
            rows=[row("train", "次へ：四天王寺前夕陽ケ丘14:02発 →（谷町線）→ 谷町四丁目14:07着・190円", "Next: Shitennoji-mae Yuhigaoka 14:02 → (Tanimachi Line) → Tanimachi 4-chome 14:07, ¥190")]),
        harukas=dict(time=T("寄るなら約50分（四天王寺のあと。大阪城が遅くなるので、どちらかにします）", "about 50 minutes if you stop (after Shitennoji; it pushes the castle too late, so choose one or the other)")),
        castle=dict(
            blurb=T("昼前後は切符の列が伸びやすい天守閣へ、15時ごろに。帰りは西日の当たる石垣とお堀を見ながら歩きます。",
                    "The tower, whose ticket queue tends to build around midday, at about 15:00 instead. Walk out past stone walls and moats in the low afternoon sun."),
            pre=T("谷町四丁目駅の1-B出口から大手門まで歩いて約8分、そこから天守閣まで約10分。このコースでは、昼の混む時間を外して14時半ごろに天守閣に着きます。それでも列が長い日は、並びながらスマホでWEBチケットを買うほうが早いことがあります。入館は17:30までなので、遅くとも16時半には入口へ。",
                  "From exit 1-B of Tanimachi 4-chome Station it is about 8 minutes to the Otemon gate and 10 more to the tower. This course reaches the tower around 14:30, after the midday peak. If the queue is still long, buying a web ticket on your phone while you stand in it can be quicker. Last entry is 17:30: be at the door by 16:30 at the latest."),
            post=T("11月から1月は、天守閣を出るころに日が傾きます（日の入りは16時50分〜17時10分ごろ）。西の丸庭園の側のお堀ごしに見る天守閣が、いちばんきれいな時間です。\n\n"
                   "次のミナミへは、谷町四丁目から谷町線で谷町九丁目へ行き、千日前線に乗り換えてなんばへ（合わせて約10分）。",
                   "From November to January the sun is getting low as you come out (sunset is around 16:50–17:10). The tower seen across the moat from the Nishinomaru side is at its best then.\n\n"
                   "For Minami next, take the Tanimachi Line from Tanimachi 4-chome to Tanimachi 9-chome and change to the Sennichimae Line for Namba (about 10 minutes in all)."),
            time=T("14:25〜16:30", "14:25–16:30"),
            rows=[row("train", "次へ：谷町四丁目16:43発 →（谷町線・谷町九丁目で千日前線に乗り換え）→ なんば16:53着・240円", "Next: Tanimachi 4-chome 16:43 → (Tanimachi Line, change at Tanimachi 9-chome to the Sennichimae Line) → Namba 16:53, ¥240")]),
        tenmangu=dict(
            pre=T("このコースの時間割には入っていません。大阪城のあとに寄ると着くのは17時ごろで、門が開いているか公式サイトで確認できていません。行くなら、朝いちばんに黒門市場の前に寄るほうが確かです（梅田から東梅田→南森町は谷町線で1駅）。",
                  "Not in this course’s timetable. After the castle you would arrive around 17:00, and the gate hours could not be confirmed on the official site. If you want to go, it is safer first thing in the morning before Kuromon Market (one stop on the Tanimachi Line from Higashi-Umeda to Minami-morimachi)."),
            post=T("南森町駅からは堺筋線で、黒門市場のある日本橋まで乗り換えなしです。", "From Minami-morimachi the Sakaisuji Line runs direct to Nippombashi for Kuromon Market."),
            time=T("寄るなら約40分", "about 40 minutes if you stop"),
            rows=[row("train", "南森町 →（堺筋線）→ 日本橋 7分・240円（乗り換えなし）", "Minami-morimachi → (Sakaisuji Line) → Nippombashi, 7 min, ¥240 (direct)")]),
        hozenji=dict(
            pre=T("なんば駅から歩いて約5分。大阪城から戻ってくる17時ごろは、ちょうど提灯に明かりが入る時間です。",
                  "About 5 minutes’ walk from Namba Station. Coming back from the castle around 17:00, you arrive just as the lanterns are lit."),
            post=T("道頓堀の戎橋までは、北へ歩いて3分です。", "Ebisubashi bridge on Dotonbori is 3 minutes’ walk north."),
            time=T("17:00〜17:15", "17:00–17:15"),
            rows=[]),
        dotonbori=dict(
            blurb=T("日が暮れて看板に明かりが入ってからが本番。たこ焼きをつまんで、うどんか串カツで晩ごはん。21時ごろまでここで過ごします。",
                    "It comes into its own once the signs light up after dark. Takoyaki first, then udon or kushikatsu for dinner: stay until about 21:00."),
            pre=T("法善寺横丁から北へ歩いて3分。11月から1月なら、着くころにはもう看板に明かりが入っています。夏は19時を過ぎないと暗くならないので、先に晩ごはんを済ませてから橋へ。",
                  "Three minutes north of Hozenji Yokocho. From November to January the signs are already lit when you arrive. In summer it is not dark until after 19:00, so have dinner first and go to the bridge afterwards."),
            post=T("20時半ごろにここを出れば、帰りに淀屋橋の無料テラスで夜景を見て、21時半にはホテルに戻れます。難波のホテルなら、そのまま22時ごろまで歩いてもかまいません。",
                   "Leave about 20:30 and you can see the night view from the free terrace at Yodoyabashi on the way and be back at your hotel by 21:30. If you are staying around Namba, you can simply carry on until about 22:00."),
            time=T("17:15〜20:30", "17:15–20:30"),
            rows=[row("train", "次へ：なんば →（御堂筋線）→ 淀屋橋 6分・190円、梅田まで8分・240円", "Next: Namba → (Midosuji Line) → Yodoyabashi, 6 min, ¥190; Umeda, 8 min, ¥240"), HOME_KYOTO_ROW]),
        nakanoshima=dict(
            blurb=T("帰り道の淀屋橋で、ビルの30階の無料テラスから夜景を。京都へ帰る人は、ここから京阪の特急に座って帰れます。",
                    "On the way back, a night view from a free 30th-floor terrace at Yodoyabashi. Anyone returning to Kyoto can get a seat on the Keihan limited express from here."),
            pre=T("なんばから御堂筋線で3駅・6分。梅田のホテルへ帰る途中で降りるだけです。難波に泊まっている人は、道頓堀でそのまま過ごしてもかまいません。",
                  "Three stops (6 minutes) from Namba on the Midosuji Line: just get off on your way back to an Umeda hotel. If you are staying around Namba, you can stay in Dotonbori instead."),
            post=T("梅田へは御堂筋線で1駅（3分）、歩いても約18分です。", "Umeda is one stop (3 minutes) on the Midosuji Line, or about 18 minutes on foot."),
            time=T("20:45〜21:15", "20:45–21:15"),
            rows=[row("train", "なんば20:39発 →（御堂筋線）→ 淀屋橋20:44着・190円", "Namba 20:39 → (Midosuji Line) → Yodoyabashi 20:44, ¥190")]),
        umekita=dict(
            blurb=T("大阪駅の北口を出てすぐの、新しい芝生の公園。このコースでは時間割の外ですが、梅田に泊まっているなら朝か夜の散歩に。",
                    "A new lawn park straight out of Osaka Station’s north side. Outside this course’s timetable, but if you are staying in Umeda it makes a morning or evening walk."),
            pre=T("このコースの時間割には入っていません。梅田に泊まっているなら、出発前の朝か、帰ってきた夜に歩けます。", "Not in this course’s timetable. If you are staying in Umeda, walk it before you set out or when you get back at night."),
            post=T("梅田スカイビルまでは、公園の西側から歩いて約7分です。", "The Umeda Sky Building is about 7 minutes’ walk from the west side of the park."),
            time=T("寄るなら約20分", "about 20 minutes if you stop"),
            rows=[]),
        skybldg=dict(
            blurb=T("屋上は屋根も窓もない吹きさらし。このコースでは夕日には間に合いませんが、22:00まで入れるので、道頓堀のあとの夜景に使えます。",
                    "The rooftop has no roof and no glass. This course does not reach it for sunset, but entry is until 22:00, so it works for a night view after Dotonbori."),
            pre=T("このコースの時間割には入っていません。夕日の時間は大阪城にいるからです。夜景なら、道頓堀を20時半に出て、なんばから梅田へ御堂筋線で8分、駅から歩いて約12分。21時すぎに着いて、22:00の最終入場に間に合います。淀屋橋の無料テラスと両方行く必要はありません。夕日をここで見たい人は、一覧の上のボタンで「朝早く出発」のコースに切り替えてください。",
                  "Not in this course’s timetable: at sunset you are at the castle. For the night view, leave Dotonbori at 20:30, take the Midosuji Line from Namba to Umeda (8 minutes) and walk about 12 minutes from the station: you arrive a little after 21:00, in time for last entry at 22:00. You do not need both this and the free terrace at Yodoyabashi. To watch the sunset here, switch to the “Early start” course with the buttons above the list."),
            post=T("帰りは、地下鉄の梅田駅まで歩いて約12分です。", "Afterwards, Umeda subway station is about 12 minutes’ walk."),
            time=T("寄るなら約1時間（最終入場22:00）", "about 1 hour if you stop (last entry 22:00)"),
            rows=[row("train", "なんば →（御堂筋線）→ 梅田 8分・240円。駅から歩いて約12分", "Namba → (Midosuji Line) → Umeda, 8 min, ¥240; then about 12 minutes’ walk")]),
    ),
    hints=[
        ("castle", {"any": ["harukas", "sumiyoshi"], "andAny": ["castle"]},
         "ハルカスや住吉大社を足すと、大阪城に着くのが16時を過ぎます。天守閣の入館は17:30まで（混む日は早く締め切ることがあります）。四天王寺を短くするか、天守閣は外から見るだけにしてください。",
         "With Harukas or Sumiyoshi Taisha added you reach the castle after 16:00. Last entry to the tower is 17:30 (earlier on busy days): shorten Shitennoji, or settle for seeing the tower from outside."),
        ("nakanoshima", {"any": ["nakanoshima"], "andAny": ["skybldg"]},
         "夜景は1か所で十分です。無料で駅の真上なのが淀屋橋、屋上で風に当たれるのがスカイビル（2,000円）。",
         "One night view is enough: Yodoyabashi is free and right above the station; the Sky Building (¥2,000) puts you on an open rooftop."),
        ("kaiyukan", {"any": ["kaiyukan"], "andAny": ["castle", "shinsekai", "shitennoji"]},
         "海遊館を入れると約4時間かかります。大阪城か、新世界〜四天王寺のどちらかを外してください。",
         "Kaiyukan takes about 4 hours. Drop either the castle or the Shinsekai–Shitennoji stretch."),
        ("dotonbori", {"any": ["dotonbori"], "none": ["castle"]},
         "大阪城に行かない日は、四天王寺のあと天王寺公園の芝生「てんしば」を抜けて動物園前駅へ。御堂筋線でなんばまで4分・190円です。早く着いたら、丸福珈琲店で暗くなるのを待てます。",
         "On a day without the castle, walk from Shitennoji across Tenshiba, the lawn of Tennoji Park, to Dobutsuen-mae Station: Namba is 4 minutes (¥190) on the Midosuji Line. If you arrive early, wait for dark at Marufuku Coffee."),
    ],
)

EARLY = dict(
    id="early", file="osaka-early.json",
    order=["castle", "tenmangu", "kuromon", "shinsekai", "shitennoji", "harukas", "sumiyoshi", "kaiyukan", "umekita", "skybldg", "nakanoshima", "hozenji", "dotonbori"],
    default=["castle", "kuromon", "shinsekai", "shitennoji", "umekita", "skybldg", "hozenji", "dotonbori"],
    sections=[("castle", "tenmangu", "大阪城", "Osaka Castle", "9:00の開館に合わせて天守閣へ", "The castle tower at its 9:00 opening"),
              ("kuromon", "kuromon", "日本橋", "Nippombashi", "市場でつまむ", "A bite at the market"),
              ("shinsekai", "sumiyoshi", "新世界・天王寺", "Shinsekai & Tennoji", "昼は通天閣の下で串カツ", "Kushikatsu under Tsutenkaku for lunch"),
              ("kaiyukan", "kaiyukan", "ベイエリア", "Bay area", "行くなら半日", "Half a day if you go"),
              ("umekita", "nakanoshima", "梅田・淀屋橋", "Umeda & Yodoyabashi", "芝生でひと休みして、屋上で夕日", "A rest on the lawn, then sunset from the roof"),
              ("hozenji", "dotonbori", "ミナミ", "Minami", "日が暮れてからの道頓堀", "Dotonbori after dark")],
    spots=dict(
        castle=dict(
            blurb=T("ホテルを8時10分ごろに出て、9:00の開館に合わせて天守閣へ。切符の列が伸びる前に8階まで上ります。",
                    "Leave the hotel about 8:10 and be at the tower for its 9:00 opening, up to the 8th floor before the ticket queue builds."),
            pre=T("梅田のホテルからは、東梅田駅から谷町線で谷町四丁目へ（8:25発→8:32着・240円）。難波のホテルからは、千日前線で谷町九丁目へ行き、谷町線に乗り換えます（なんば8:18発→8:31着・240円）。1-B出口から大手門まで歩いて約8分、そこから天守閣まで約10分。8時55分には入口の前に立てます。\n\n"
                  "朝ごはんをホテルで食べない人へ：難波側なら、丸福珈琲店 千日前本店が8:00から開いています（モーニングは平日だけ）。",
                  "From a hotel in Umeda, take the Tanimachi Line from Higashi-Umeda to Tanimachi 4-chome (8:25 → 8:32, ¥240). From Namba, ride the Sennichimae Line to Tanimachi 9-chome and change to the Tanimachi Line (Namba 8:18 → 8:31, ¥240). From exit 1-B it is about 8 minutes to the Otemon gate and 10 more to the tower: you are at the door by 8:55.\n\n"
                  "If you do not eat breakfast at your hotel: on the Namba side, Marufuku Coffee’s Sennichimae main shop opens at 8:00 (breakfast sets on weekdays only)."),
            post=T("天守閣を出たら、帰りはお堀ぞいに遠回りして谷町四丁目駅へ戻ります。次の黒門市場へは、谷町線で谷町九丁目へ行き、千日前線に乗り換えて日本橋へ（合わせて約11分）。",
                   "After the tower, take the long way back along the moat to Tanimachi 4-chome Station. For Kuromon Market next, ride the Tanimachi Line to Tanimachi 9-chome and change to the Sennichimae Line for Nippombashi (about 11 minutes in all)."),
            time=T("9:00〜10:40", "9:00–10:40"),
            rows=[row("train", "梅田から：東梅田8:25発 →（谷町線）→ 谷町四丁目8:32着・240円", "From Umeda: Higashi-Umeda 8:25 → (Tanimachi Line) → Tanimachi 4-chome 8:32, ¥240"),
                  row("train", "難波から：なんば8:18発 →（千日前線・谷町九丁目で谷町線に乗り換え）→ 谷町四丁目8:31着・240円", "From Namba: Namba 8:18 → (Sennichimae Line, change at Tanimachi 9-chome to the Tanimachi Line) → Tanimachi 4-chome 8:31, ¥240"),
                  row("train", "京都から来る人：京阪の三条7:49発（特急）→ 天満橋8:38着・490円。大手門まで歩いて約10分", "Coming from Kyoto: Keihan Sanjo 7:49 (limited express) → Temmabashi 8:38, ¥490; about 10 minutes’ walk to the Otemon gate"),
                  row("train", "次へ：谷町四丁目10:55発 →（谷町線・谷町九丁目で千日前線に乗り換え）→ 日本橋11:06着・190円", "Next: Tanimachi 4-chome 10:55 → (Tanimachi Line, change at Tanimachi 9-chome to the Sennichimae Line) → Nippombashi 11:06, ¥190")]),
        tenmangu=dict(
            pre=T("時間割には入っていない寄り道です。大阪城のあと、天満橋駅まで歩いて谷町線で1駅（南森町）。歩いても天満橋駅から約15分です。寄ると、このあとの時間が40分ずつ後ろにずれます。",
                  "A detour outside the timetable. After the castle, walk to Temmabashi Station and ride the Tanimachi Line one stop to Minami-morimachi, or walk about 15 minutes from Temmabashi. Stopping here pushes everything after it back by 40 minutes."),
            post=T("南森町駅からは堺筋線で、次の黒門市場（日本橋駅）まで乗り換えなしで行けます。", "From Minami-morimachi the Sakaisuji Line runs direct to Nippombashi for Kuromon Market."),
            time=T("寄るなら約40分（11:00〜11:40ごろ）", "about 40 minutes if you stop (around 11:00–11:40)"),
            rows=[row("train", "天満橋 →（谷町線）→ 南森町 3分・190円", "Temmabashi → (Tanimachi Line) → Minami-morimachi, 3 min, ¥190"),
                  row("train", "次へ：南森町 →（堺筋線）→ 日本橋 7分・240円（乗り換えなし）", "Next: Minami-morimachi → (Sakaisuji Line) → Nippombashi, 7 min, ¥240 (direct)")]),
        kuromon=dict(
            blurb=T("大阪城のあと、昼前の市場へ。焼きたての貝や串、果物を2〜3品つまみます。お昼の串カツは次の新世界で。",
                    "After the castle, the market before noon. Pick two or three things: grilled shellfish, skewers, fruit. Lunch proper is kushikatsu at the next stop."),
            pre=T("大阪城から地下鉄で約11分。日本橋駅の10番出口を出ると、もうアーケードの入口です。",
                  "About 11 minutes by subway from the castle. Exit 10 of Nippombashi Station opens straight onto the arcade."),
            post=T("次の新世界へは、堺筋（さかいすじ）をまっすぐ南へ歩いて約20分。途中は電気とアニメの店が並ぶ「でんでんタウン」で、通天閣が正面に見えてきます。朝から歩いているので、日本橋から堺筋線で1駅の恵美須町（えびすちょう）へ乗ってもかまいません（2分・190円）。3番出口を出ると通天閣のすぐ北側です。",
                   "For Shinsekai next, walk straight south down Sakaisuji avenue for about 20 minutes. The way runs through Den Den Town, the street of electronics and anime shops, with Tsutenkaku coming into view ahead. You have been walking since morning, so feel free to ride the Sakaisuji Line one stop from Nippombashi to Ebisucho instead (2 min, ¥190); exit 3 comes out just north of the tower."),
            time=T("11:10〜12:00", "11:10–12:00"),
            rows=[row("train", "日本橋駅（堺筋線・千日前線）10番出口からすぐ", "Right outside exit 10 of Nippombashi Station (Sakaisuji and Sennichimae lines)"),
                  row("train", "次へ：歩いて約20分。または日本橋 →（堺筋線）→ 恵美須町 2分・190円", "Next: about 20 minutes on foot, or Nippombashi → (Sakaisuji Line) → Ebisucho, 2 min, ¥190")]),
        shinsekai=dict(
            blurb=T("巨大なふぐやビリケンさんの看板が頭の上に並ぶ通りの先に、通天閣。お昼は串カツです。",
                    "A street hung with giant blowfish and Billiken signs, with Tsutenkaku tower at the end. Kushikatsu for lunch."),
            pre=T("黒門市場から歩いて約20分、または恵美須町駅の3番出口からすぐ。着くのは12時すぎで、串カツの店は昼の列ができる時間です。並んでいたら、先に通りとジャンジャン横丁を歩いて、13時ごろに入るほうが待ちません。",
                  "About 20 minutes’ walk from Kuromon Market, or right by exit 3 of Ebisucho Station. You arrive a little after noon, when the kushikatsu shops have their lunchtime queues. If so, walk the street and Janjan Yokocho first and sit down around 13:00."),
            post=T("次の四天王寺へは、通天閣から東へ歩いて約14分。天王寺動物園の北側の道をまっすぐ進みます。",
                   "For Shitennoji next, walk east from Tsutenkaku for about 14 minutes, straight along the road on the north side of Tennoji Zoo."),
            time=T("12:20〜13:45", "12:20–13:45"),
            rows=[row("train", "恵美須町駅（堺筋線）3番出口からすぐ。動物園前駅（御堂筋線）1番出口からはジャンジャン横丁を抜けて約8分", "Right by exit 3 of Ebisucho Station (Sakaisuji Line). From exit 1 of Dobutsuen-mae (Midosuji Line), about 8 minutes through Janjan Yokocho")]),
        shitennoji=dict(
            pre=T("通天閣から東へ歩いて約14分。", "About 14 minutes’ walk east of Tsutenkaku."),
            post=T("次の梅田へは、北へ歩いて約5分の四天王寺前夕陽ケ丘（してんのうじまえゆうひがおか）駅から谷町線で。東梅田まで乗り換えなしで12分です。",
                   "For Umeda next, walk about 5 minutes north to Shitennoji-mae Yuhigaoka Station and take the Tanimachi Line: 12 minutes direct to Higashi-Umeda."),
            time=T("14:00〜14:45", "14:00–14:45"),
            rows=[row("train", "次へ：四天王寺前夕陽ケ丘15:02発 →（谷町線）→ 東梅田15:14着・240円", "Next: Shitennoji-mae Yuhigaoka 15:02 → (Tanimachi Line) → Higashi-Umeda 15:14, ¥240")]),
        harukas=dict(time=T("寄るなら約50分（四天王寺のあと。日の入りの遅い季節向き）", "about 50 minutes if you stop (after Shitennoji; best in seasons with a late sunset)")),
        umekita=dict(
            blurb=T("大阪駅の北口を出てすぐの、新しい芝生の公園。朝から歩いた足を、スカイビルに上る前にここで休めます。",
                    "A new lawn park straight out of Osaka Station’s north side. Rest the legs you have been on since morning before going up the Sky Building."),
            pre=T("東梅田駅から、大阪駅の中を北へ抜けて歩いて約12分。", "About 12 minutes’ walk from Higashi-Umeda Station, north through Osaka Station."),
            post=T("梅田スカイビルまでは、公園の西側から歩いて約7分です。", "The Umeda Sky Building is about 7 minutes’ walk from the west side of the park."),
            time=T("15:30〜16:05", "15:30–16:05"),
            rows=[row("train", "東梅田駅・梅田駅・JR大阪駅から歩いて約10〜12分", "About 10–12 minutes’ walk from Higashi-Umeda, Umeda or JR Osaka Station")]),
        skybldg=dict(
            blurb=T("屋上は屋根も窓もない吹きさらし。西の淀川に沈む夕日を見て、暗くなったら夜の道頓堀へ向かいます。",
                    "The rooftop has no roof and no glass. Watch the sun set over the Yodo river, then head for Dotonbori once it is dark."),
            pre=T("うめきた公園から歩いて約7分。時間割は11月下旬の日の入り（16時50分ごろ）に合わせてあります。春と秋はここが18時前後、夏は19時ごろになるので、四天王寺のあとにハルカスを足すか、いったんホテルで休んでから来てください。その季節は、スカイビルのあとの道頓堀が20時すぎからになります。",
                  "About 7 minutes’ walk from Umekita Park. The timetable is set for sunset in late November (about 16:50). In spring and autumn this stop moves to around 18:00, in summer to about 19:00: add Harukas after Shitennoji, or rest at your hotel first. In those seasons Dotonbori afterwards starts from about 20:00."),
            post=T("朝8時から歩いているので、梅田に泊まっている人はここで終わりにしてもかまいません。続ける人は、地下鉄の梅田駅まで歩いて約12分、御堂筋線でなんばへ9分。",
                   "You have been out since 8:00, so if you are staying in Umeda it is fine to stop here. To carry on, walk about 12 minutes to Umeda subway station and ride the Midosuji Line 9 minutes to Namba."),
            time=T("16:15〜17:30（日の入りの30〜40分前から）", "16:15–17:30 (from 30–40 minutes before sunset)"),
            rows=[row("train", "次へ：梅田17:47発 →（御堂筋線）→ なんば17:56着・240円", "Next: Umeda 17:47 → (Midosuji Line) → Namba 17:56, ¥240"),
                  row("train", "京都へ帰る人：阪急の大阪梅田駅まで歩いて約9分、特急で京都河原町へ43分・410円。JR大阪駅まで約7分、新快速で京都へ約30分・580円", "Going back to Kyoto: Hankyu Osaka-Umeda Station is about 9 minutes’ walk, then 43 min by limited express to Kyoto-Kawaramachi (¥410). JR Osaka Station is about 7 minutes, then about 30 min by Special Rapid to Kyoto (¥580)")]),
        nakanoshima=dict(
            blurb=T("スカイビルに上らない日の代わりに。淀屋橋のビルの30階に、無料で入れる展望テラスがあります。",
                    "The alternative on a day without the Sky Building: a free terrace on the 30th floor of a tower at Yodoyabashi."),
            pre=T("このコースの時間割には入っていません。スカイビルの代わりにするなら、梅田から御堂筋線で1駅（3分）。うめきた公園のあとに来て、暗くなるのを待ちます。",
                  "Not in this course’s timetable. As an alternative to the Sky Building it is one stop (3 minutes) from Umeda on the Midosuji Line: come after Umekita Park and wait for dark."),
            post=T("なんばへは御堂筋線で3駅・6分です。", "Namba is three stops (6 minutes) on the Midosuji Line."),
            time=T("寄るなら約40分（夕方〜夜）", "about 40 minutes if you stop (evening)"),
            rows=[row("train", "梅田 →（御堂筋線）→ 淀屋橋 3分・190円。次へ：淀屋橋 → なんば 6分・190円", "Umeda → (Midosuji Line) → Yodoyabashi, 3 min, ¥190. Next: Yodoyabashi → Namba, 6 min, ¥190")]),
        hozenji=dict(
            pre=T("なんば駅から歩いて約5分。梅田から戻ってくる18時すぎには、提灯に明かりが入っています。",
                  "About 5 minutes’ walk from Namba Station. By the time you are back from Umeda, a little after 18:00, the lanterns are lit."),
            post=T("道頓堀の戎橋までは、北へ歩いて3分です。", "Ebisubashi bridge on Dotonbori is 3 minutes’ walk north."),
            time=T("18:05〜18:20", "18:05–18:20"),
            rows=[]),
        dotonbori=dict(
            blurb=T("最後は、看板に明かりが入った夜の道頓堀。たこ焼きをつまんで、うどんか串カツで晩ごはん。21時ごろまでここで過ごします。",
                    "Last, Dotonbori at night with the signs lit. Takoyaki first, then udon or kushikatsu for dinner: stay until about 21:00."),
            pre=T("法善寺横丁から北へ歩いて3分。黒門市場のあと（歩いて約10分）に昼の道頓堀も見ておきたい人は、新世界へ向かう前に寄ってもかまいません。夜とはまったく違う顔です。",
                  "Three minutes north of Hozenji Yokocho. If you also want to see Dotonbori by day, it is about 10 minutes’ walk from Kuromon Market: look in before heading to Shinsekai. It is a different place at night."),
            post=T("難波のホテルなら歩いて帰れます。梅田のホテルへは、なんばから御堂筋線で8分。",
                   "Namba hotels are a walk away. For Umeda hotels, the Midosuji Line from Namba takes 8 minutes."),
            time=T("18:20〜21:00", "18:20–21:00"),
            rows=[row("train", "帰り：なんば →（御堂筋線）→ 梅田 8分・240円", "Back: Namba → (Midosuji Line) → Umeda, 8 min, ¥240"), HOME_KYOTO_ROW]),
    ),
    hints=[
        ("kuromon", {"any": ["tenmangu"]},
         "大阪天満宮からは、南森町駅から堺筋線で日本橋へ乗り換えなし（7分・240円）。", "From Osaka Temmangu, the Sakaisuji Line runs direct from Minami-morimachi to Nippombashi (7 min, ¥240)."),
        ("harukas", {"any": ["harukas"], "andAny": ["skybldg"]},
         "展望台は1つで十分です。夕日と夜景ならスカイビル、高さと昼の眺めならハルカス。両方上ると4,200円かかります。",
         "One observatory is enough: the Sky Building for sunset and night, Harukas for height and daytime views. Both together cost ¥4,200."),
        ("skybldg", {"any": ["harukas", "sumiyoshi"], "andAny": ["skybldg"]},
         "天王寺からは御堂筋線で梅田へ15分・290円。寄り道を足した日は、日の入りの時刻から逆算して天王寺を出てください。",
         "From Tennoji the Midosuji Line reaches Umeda in 15 min (¥290). With detours added, count back from sunset to decide when to leave Tennoji."),
        ("nakanoshima", {"any": ["nakanoshima"], "andAny": ["skybldg"]},
         "夜景は1か所で十分です。無料で駅の真上なのが淀屋橋、屋上で風に当たれるのがスカイビル（2,000円）。",
         "One night view is enough: Yodoyabashi is free and right above the station; the Sky Building (¥2,000) puts you on an open rooftop."),
        ("kaiyukan", {"any": ["kaiyukan"], "andAny": ["castle", "shinsekai", "shitennoji"]},
         "海遊館を入れると約4時間かかります。大阪城か、新世界〜四天王寺のどちらかを外してください。",
         "Kaiyukan takes about 4 hours. Drop either the castle or the Shinsekai–Shitennoji stretch."),
        ("dotonbori", {"any": ["dotonbori"], "none": ["umekita", "skybldg", "nakanoshima"]},
         "梅田に行かない日は、四天王寺のあと天王寺公園の芝生「てんしば」を抜けて動物園前駅へ。御堂筋線でなんばまで4分・190円です。早く着いたら、丸福珈琲店で暗くなるのを待てます。",
         "On a day without Umeda, walk from Shitennoji across Tenshiba, the lawn of Tennoji Park, to Dobutsuen-mae Station: Namba is 4 minutes (¥190) on the Midosuji Line. If you arrive early, wait for dark at Marufuku Coffee."),
    ],
)

NOTE_HEAD = ("大阪の1日ルート（osaka/ のページ専用。形は eizan-line.json と同じ）。起点は梅田〜難波のあたりのホテル。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む"
             "（osaka.json＝9〜10時に出発、osaka-early.json＝朝早く出発して大阪城天守閣の9:00の開館に合わせる）。このファイル：")
NOTE_TAIL = (" 自分の写真は Toshi の写真ライブラリから（大阪城 2016年2月・2025年4月・2026年4月、黒門市場と道頓堀 2023年12月29日・2024年8月、会津屋のたこ焼き 2023年6月、中之島 2024年7月・2025年5月、淀屋橋スカイテラス 2025年12月・2026年4月、うめきた公園 2025年6月・2026年9月、阪堺電車 2023年8月、天神橋筋 2024年7月の天神祭）。"
             "法善寺横丁・通天閣・四天王寺・ハルカス300・住吉大社・海遊館・大阪天満宮・空中庭園展望台は Wikimedia Commons の写真（クレジット表示）。"
             "info.source は確認した出典、info.checked は確認日、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。入口で困ること（現金のみ・休み・階段・予約）は caution と head つきの notices。"
             "店名を出しているのは、公式サイトで営業時間を確かめた店（串かつだるま・道頓堀 今井・丸福珈琲店）と、Toshi が食べた会津屋だけ。"
             "plan.defaultPicks は最初から選ばれている場所で、各スポットの「おすすめ訪問時間」はこの組み合わせの時間割（11月下旬・土曜のダイヤ）。このファイルは scripts/build_osaka_data.py で作る（直接直さない）。")


# 文章の1行目（読みがなつきの名前）
TITLE = dict(
    castle=T("大阪城（おおさかじょう）", "Osaka Castle"),
    tenmangu=T("大阪天満宮（おおさかてんまんぐう）と天神橋筋商店街（てんじんばしすじ）", "Osaka Temmangu and the Tenjinbashi-suji arcade"),
    kuromon=T("黒門市場（くろもんいちば）", "Kuromon Market"),
    shinsekai=T("新世界（しんせかい）と通天閣（つうてんかく）", "Shinsekai and Tsutenkaku"),
    shitennoji=T("四天王寺（してんのうじ）", "Shitennoji"),
    harukas=T("あべのハルカスと展望台「ハルカス300」", "Abeno Harukas and the Harukas 300 observatory"),
    sumiyoshi=T("住吉大社（すみよしたいしゃ）", "Sumiyoshi Taisha"),
    kaiyukan=T("海遊館（かいゆうかん）", "Osaka Aquarium Kaiyukan"),
    umekita=T("うめきた公園（グラングリーン大阪）", "Umekita Park (Grand Green Osaka)"),
    skybldg=T("梅田スカイビルの空中庭園展望台（くうちゅうていえんてんぼうだい）", "Kuchu Teien Observatory, Umeda Sky Building"),
    nakanoshima=T("淀屋橋スカイテラスと、中之島の大阪市中央公会堂", "The Yodoyabashi Sky Terrace and Osaka City Central Public Hall on Nakanoshima"),
    hozenji=T("法善寺横丁（ほうぜんじよこちょう）と水掛不動（みずかけふどう）", "Hozenji Yokocho and Mizukake Fudo"),
    dotonbori=T("道頓堀（どうとんぼり）と戎橋（えびすばし）", "Dotonbori and Ebisubashi"),
)


def build(c):
    cs = c["spots"]
    spots = []
    for i, sid in enumerate(c["order"], 1):
        b, o = S[sid], cs.get(sid, {})
        parts = [TITLE.get(sid) or b["name"], o.get("pre"), b["body"], o.get("post")]
        tm = o.get("time") or b.get("time")
        text = {}
        for lang, lead in (("ja", "おすすめ訪問時間："), ("en", "Recommended visit time: ")):
            text[lang] = "\n\n".join(p[lang] for p in parts if p) + "\n\n" + lead + tm[lang]
        out = {"no": i, "id": sid, "name": b["name"], "kind": b["kind"], "blurb": o.get("blurb") or b["blurb"], "lat": b["lat"], "lng": b["lng"]}
        if b.get("caution"):
            out["caution"] = b["caution"]
        out["text"] = text
        out["gmaps"] = b["gmaps"]
        out["links"] = b["links"]
        out["info"] = info(b["rows"] + o.get("rows", []), tip=b["tip"], verified=b.get("verified", True), cash=b.get("cash", False), source=b.get("source"), checked=b.get("checked"))
        out["photos"] = photos(sid)
        out["notices"] = b.get("notices", [])
        spots.append(out)
    NO = {s["id"]: s["no"] for s in spots}
    N = lambda ids: [NO[k] for k in ids]
    data = {
        "id": "osaka", "course": c["id"],
        "_note": NOTE_HEAD + c["file"] + "。" + NOTE_TAIL,
        "sections": [{"first": NO[a], "last": NO[b], "area": T(aj, ae), "title": T(tj, te)} for a, b, aj, ae, tj, te in c["sections"]],
        "plan": {"_note": "「選んで回る」の設定。全部が自分で選ぶ場所。defaultMode: pick で最初から「選んで回る」、defaultPicks は1日で無理なく回れる組み合わせ（時間割どおり）。それ以外は時間割の外の寄り道。",
                 "defaultMode": "pick",
                 "picks": [s["no"] for s in spots],
                 "defaultPicks": N(c["default"]),
                 "auto": {},
                 "hints": [{"spot": NO[sp], "rule": {k: N(v) for k, v in rule.items()}, "text": T(ja, en)} for sp, rule, ja, en in c["hints"]]},
        "photoBase": "../images/osaka/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


assert set(LATE["order"]) == set(EARLY["order"]) == set(S)
for c in (LATE, EARLY):
    build(c)
