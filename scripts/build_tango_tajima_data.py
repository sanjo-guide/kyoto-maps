#!/usr/bin/env python3
"""丹後・但馬ガイド（tango-tajima/）の js/data.js を作る。

使い方: python3 scripts/build_tango_tajima_data.py
- 文章・料金・時間・モデルプランはこのファイルの中。直したらこのスクリプトを実行し直す（data.js を直接直さない）
- 写真は tango-tajima/img/<id>-<番号>.jpg。キャプションの数と写真の数が合わないと止まる
- ネットの写真（Wikimedia Commons）は tango-tajima/img/web-<id>-<番号>.jpg。スポットの "web" に
  (番号, 日本語キャプション, 英語キャプション, 撮影者, ライセンス, ファイルのページURL) を書くと、クレジットつきで自分の写真のあとに並ぶ
  （"caps" のないスポットは、ネットの写真だけになる）
- 簡易地図の輪郭は scripts/tango_tajima_region.json
"""
import json, os, struct, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = f"{R}/tango-tajima"
IMG = f"{SITE}/img"


def T(ja, en):
    return {"ja": ja, "en": en}


def gmap(q):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    raise ValueError(path)


def photos(pid, caps):
    files = sorted([f for f in os.listdir(IMG) if f.startswith(pid + "-") and f[len(pid) + 1:-4].isdigit()],
                   key=lambda f: int(f[len(pid) + 1:-4]))
    assert len(files) == len(caps), (pid, len(files), len(caps))
    out = []
    for f, c in zip(files, caps):
        w, h = jpeg_size(os.path.join(IMG, f))
        out.append({"f": f, "cap": T(*c), "w": w, "h": h})
    return out


def web_photos(pid, items):
    """ネットの写真（クレジットつき）。ファイルは img/web-<id>-<番号>.jpg"""
    out = []
    for n, ja, en, author, lic, page in items:
        f = f"web-{pid}-{n}.jpg"
        w, h = jpeg_size(os.path.join(IMG, f))
        out.append({"f": f, "cap": T(ja, en), "w": w, "h": h, "credit": {"author": author, "license": lic, "page": page}})
    return out


def link(ja, en, url):
    return {"ja": ja, "en": en, "url": url}


ROUTE_AMA = link("天橋立・伊根の日帰りルートマップ", "Amanohashidate & Ine day-trip route map", "../amanohashidate/")
ROUTE_KINO = link("城崎温泉・竹田城跡の日帰りルートマップ", "Kinosaki & Takeda day-trip route map", "../kinosaki/")

intro = T([
    "京都府の北の丹後（天橋立・伊根・舞鶴）と、兵庫県の北の但馬（豊岡・城崎温泉・竹野・竹田城跡）のおすすめをまとめました。",
    "京都から日帰りなら、天橋立と伊根がおすすめです。特急で乗り換えなしで行けて、海の上の松並木と、舟屋の町を1日で回れます。",
    "1泊以上できるなら、豊岡のゲストハウス「Hostel Act」を拠点にするのがおすすめです。豊岡からは城崎温泉まで電車で約12分、天橋立まで京都丹後鉄道で約1時間15〜25分。天橋立・伊根、舞鶴、城崎温泉、竹野の海、竹田城跡まで、毎日ちがう場所へ出かけられます。",
    "下の「モデルプラン」に、日帰り・1泊・2泊・3泊の回り方の例を書きました。出石と玄武洞は、私はまだ行っていませんが、豊岡に泊まるなら外せない場所なので、公式の情報をもとに紹介しています（写真はクレジットつき）。",
    "いちばん大事なのは、予定を詰め込みすぎないこと。気になる場所を、ゆっくり楽しんでください。",
], [
    "Here are my recommendations for Tango in northern Kyoto (Amanohashidate, Ine, Maizuru) and Tajima in northern Hyogo (Toyooka, Kinosaki Onsen, Takeno, Takeda Castle).",
    "For a day trip from Kyoto, go to Amanohashidate and Ine. A direct limited express takes you there, and in one day you can see the pine-covered sandbar across the sea and the town of boathouses.",
    "If you can stay a night or more, base yourself at Hostel Act, a guesthouse in Toyooka. Kinosaki Onsen is about 12 minutes away by train and Amanohashidate about 1 h 15–25 min on the Kyoto Tango Railway, so each day you can head somewhere different: Amanohashidate and Ine, Maizuru, Kinosaki, the sea at Takeno, or Takeda Castle.",
    "The model plans below show ways to do it as a day trip, or with one, two or three nights. I haven’t yet been to Izushi or Genbudo, but if you stay in Toyooka they shouldn’t be missed, so I’ve described them from official information (photos are credited).",
    "The most important thing is not to overpack your schedule. Just take your time and enjoy the places that really interest you.",
])
outro = T([
    "以上が、私の丹後・但馬のおすすめです。",
    "海の京都の丹後と、温泉とコウノトリの但馬。電車で行き来できるので、何日かかけて、ゆっくり回ってみてください。",
    "電車やバスは本数が少ないので、時間を先に確かめて、無理せず、自分らしい旅を楽しんでください。",
], [
    "That’s my list of picks for Tango and Tajima.",
    "Tango, the seaside of Kyoto, and Tajima, land of hot springs and storks, are linked by train, so take a few days and travel slowly.",
    "Trains and buses are infrequent, so check the times first, don’t push yourself too hard, and enjoy the trip your own way.",
])

plans = [
    {"id": "plan-day", "title": T("日帰り（京都から）", "Day trip from Kyoto"),
     "sub": T("天橋立と伊根を1日で", "Amanohashidate and Ine in a day"),
     "days": [
         {"label": T("1日目", "Day 1"),
          "text": T("京都8:38の特急はしだて1号で天橋立へ。「天橋立・伊根フリーパス」で、観光船・傘松公園のケーブルカー・伊根のバスと遊覧船に乗り放題。帰りは天橋立18:09の特急で京都へ。",
                    "Take the 8:38 Hashidate No. 1 from Kyoto to Amanohashidate. With the Amanohashidate & Ine free pass, ride the sightseeing boat, the Kasamatsu cable car, the bus to Ine and the bay cruise as much as you like. Back on the 18:09 express from Amanohashidate.")}],
     "links": [ROUTE_AMA],
     "note": T("城崎温泉も京都から日帰りできます（特急で約2時間20分）。", "Kinosaki Onsen also works as a day trip from Kyoto (about 2 h 20 min by express).")},
    {"id": "plan-1", "title": T("1泊2日", "1 night, 2 days"),
     "sub": T("天橋立・伊根と城崎温泉", "Amanohashidate, Ine and Kinosaki"),
     "days": [
         {"label": T("1日目", "Day 1"),
          "text": T("日帰りプランと同じように天橋立・伊根を回り、夕方の京都丹後鉄道で豊岡へ（天橋立17:21発→豊岡18:47着。あとの便は18:21発→19:48着、19:29発→20:51着。フリーパスを持っていればそのまま乗れます。なければ1,200円）。Hostel Actに泊まります。1階のもりめ食堂は2026年末まで休業中なので、夕食は豊岡駅のまわりで。",
                    "See Amanohashidate and Ine as in the day trip, then take the evening Kyoto Tango Railway to Toyooka (Amanohashidate 17:21 → Toyooka 18:47; later trains 18:21 → 19:48 and 19:29 → 20:51; covered by the free pass, otherwise ¥1,200). Stay at Hostel Act. Morime Shokudo downstairs is closed until the end of 2026, so have dinner around Toyooka Station.")},
         {"label": T("2日目", "Day 2"),
          "text": T("豊岡から電車で12分の城崎温泉へ。柳並木の温泉街で外湯めぐりをして、城崎温泉から特急で京都へ。",
                    "Ride 12 minutes from Toyooka to Kinosaki Onsen. Hop between the public baths in the willow-lined town, then take a limited express from Kinosaki back to Kyoto.")}],
     "links": [ROUTE_AMA, ROUTE_KINO]},
    {"id": "plan-2", "title": T("2泊3日", "2 nights, 3 days"),
     "sub": T("城崎温泉と竹野の海、竹田城跡も", "Add the sea at Takeno and Takeda Castle"),
     "days": [
         {"label": T("1日目", "Day 1"), "text": T("1泊2日と同じ（天橋立・伊根 → 豊岡のHostel Act）。", "As in the 1-night plan (Amanohashidate and Ine → Hostel Act in Toyooka).")},
         {"label": T("2日目", "Day 2"),
          "text": T("城崎温泉で外湯めぐり。となりの竹野駅（電車で約10分）まで足をのばして、竹野浜の海も。夜は豊岡へ戻ってHostel Actにもう1泊。",
                    "Bathhouse-hopping in Kinosaki, then on to Takeno, one station further (about 10 min), for the beach. Back to Toyooka for another night at Hostel Act.")},
         {"label": T("3日目", "Day 3"),
          "text": T("豊岡から竹田まで電車で約45分〜1時間15分（和田山で乗り換え、680円。本数が少ないので時刻を確認）。天空の城・竹田城跡を歩いて、和田山から特急で京都へ。竹田城跡は1月4日〜2月末は冬の閉山で入れません。",
                    "About 45 min to 1 h 15 min by train from Toyooka to Takeda (change at Wadayama, ¥680; trains are few, so check the times). Walk the “castle in the sky”, then take a limited express from Wadayama back to Kyoto. Takeda Castle is closed for winter from 4 Jan to the end of February.")}],
     "links": [ROUTE_KINO]},
    {"id": "plan-3", "title": T("3泊4日", "3 nights, 4 days"),
     "sub": T("舞鶴と出石も入れて、丹後と但馬をぜんぶ", "All of Tango and Tajima, with Maizuru and Izushi"),
     "days": [
         {"label": T("1日目", "Day 1"),
          "text": T("京都から特急まいづるで東舞鶴へ（約1時間30分）。赤れんがパークと北吸トンネルを歩き、西舞鶴へ移って吉原入江へ。夕方、京都丹後鉄道で豊岡へ（舞鶴から約2時間）。Hostel Act泊。",
                    "Limited express Maizuru from Kyoto to Higashi-Maizuru (about 1 h 30 min). Walk the Red Brick Park and the Kitasui tunnel, then move to Nishi-Maizuru for Yoshiwara Irie. In the evening, ride the Kyoto Tango Railway to Toyooka (about 2 hours from Maizuru). Stay at Hostel Act.")},
         {"label": T("2日目", "Day 2"),
          "text": T("豊岡から京都丹後鉄道で天橋立へ（約1時間15〜25分）。天橋立と伊根を回って、夕方の電車で豊岡へ戻ります。「天橋立・伊根フリーパス 1day」は京都丹後鉄道の有人駅でも買えて、豊岡〜天橋立の電車（片道1,200円）も乗り放題に入っています。",
                    "Kyoto Tango Railway from Toyooka to Amanohashidate (about 1 h 15–25 min). See Amanohashidate and Ine, and ride back to Toyooka in the evening. The Amanohashidate & Ine 1-day free pass is also sold at staffed Kyoto Tango Railway stations and covers the train between Toyooka and Amanohashidate (¥1,200 each way).")},
         {"label": T("3日目", "Day 3"),
          "text": T("午前は豊岡駅からバスで約30分の出石へ。辰鼓楼のまわりを歩いて、お昼に皿そば。午後は豊岡へ戻って城崎温泉で外湯めぐり。土日祝なら、出石から城崎温泉への直通バス（出石12:50発・14:05発など、800円）も使えます。", "In the morning, take the bus from Toyooka Station to Izushi (about 30 min). Walk around the Shinkoro clock tower and have sara-soba for lunch. In the afternoon, go back to Toyooka and on to Kinosaki for the baths. On weekends and holidays you can also use the direct bus from Izushi to Kinosaki Onsen (leaving Izushi at 12:50 or 14:05, among others; ¥800).")},
         {"label": T("4日目", "Day 4"),
          "text": T("竹田城跡を歩いて、京都へ帰ります。竹田城跡のかわりに、竹野浜の海でのんびりする1日にしてもいいと思います。", "Walk Takeda Castle, then head back to Kyoto. Or swap the castle for a slow day by the sea at Takeno.")}],
     "links": [ROUTE_AMA, ROUTE_KINO]},
]

STAY_NOTE = T(
    "ドミトリー（5人の相部屋）は1ベッド4,400円、和室の個室Aは1人5,900円から、個室Bは2人12,100円から（すべて素泊まり・税込。GW・お盆・年末年始は1人1泊550円アップ）。"
    "チェックインは15時から（22時以降は夜間受付で追加料金）。1階の「もりめ食堂」（立ち飲みと日替わり定食）は2026年末まで臨時休業中です。2026年11月20日に公式サイトで確認。",
    "Dorm (5 beds) ¥4,400 per bed; Japanese-style private room A from ¥5,900 for one; room B from ¥12,100 for two (room only, tax included; +¥550 per person per night in Golden Week, Obon and New Year). "
    "Check-in from 15:00 (late arrival after 22:00 costs extra). Morime Shokudo, the standing bar and set-meal place downstairs, is temporarily closed until the end of 2026. Checked on the official website on 20 Nov 2026.")

# ネットの写真（Wikimedia Commons）。scratchpad の manifest から写したもの
WEB = json.load(open(f"{R}/scripts/tango_tajima_web_photos.json", encoding="utf-8"))

city = [
    {"id": "toyooka", "lat": 35.54420, "lon": 134.81450, "ja": "豊岡の町とふれあい公設市場", "en": "Toyooka and the Fureai public market",
     "short": T("豊岡", "Toyooka"), "map": gmap("ふれあい公設市場 豊岡"),
     "time": T("京都から特急で豊岡まで約2時間10〜20分（5,030円）", "About 2 h 10–20 min from Kyoto to Toyooka by limited express (¥5,030)"),
     "body": T([
         "コウノトリと鞄（かばん）の町・豊岡は、城崎温泉のひとつ手前の駅の町です。旅の拠点にちょうどいい大きさで、駅のまわりにお店や食堂が集まっています。",
         "駅から歩いて数分のふれあい公設市場は、昭和のはじめにできた木造アーケードの市場です。のれんと提灯が並ぶ細い通りを歩くと、昔の町にタイムスリップしたような気分になります。",
     ], [
         "Toyooka, town of storks and bags, is the station before Kinosaki Onsen. It’s just the right size for a base, with shops and diners around the station.",
         "A few minutes’ walk from the station, the Fureai public market is a wooden arcade market from the early Showa era. Walking its narrow lane of curtains and lanterns feels like slipping back in time.",
     ]),
     "caps": [("のれんの並ぶ市場の通り", "The market lane with its curtains"), ("夜のふれあい公設市場", "The Fureai market at night"), ("木造アーケードの屋根", "The wooden arcade roof"),
              ("ふれあい公設市場の入り口", "The market entrance"), ("雪の日の豊岡駅", "Toyooka Station in snow"), ("夜の豊岡駅", "Toyooka Station at night")]},
    {"id": "kinosaki", "lat": 35.62550, "lon": 134.80850, "ja": "城崎温泉", "en": "Kinosaki Onsen",
     "short": T("城崎温泉", "Kinosaki Onsen"), "map": gmap("城崎温泉"),
     "time": T("豊岡から電車で約12分（200円）", "About 12 min by train from Toyooka (¥200)"),
     "body": T([
         "柳並木の大谿川（おおたにがわ）に沿って、外湯（共同浴場）が並ぶ温泉町です。外湯は7つありますが、駅前のさとの湯は建て替え工事のため休業中です（駅前の足湯も2025年10月15日で終了）。浴衣と下駄で、外湯をめぐりながら歩くのが城崎の楽しみ方です。",
         "外湯めぐりの1日券「ゆめぱ」（1,500円）は、どの外湯でも買えます。夜は川沿いに灯りがともり、冬は雪景色になります。外湯の時間や休みの日は、ルートマップにまとめています。",
     ], [
         "A hot-spring town whose public bathhouses line the willow-fringed Otani River. There are seven, but Sato-no-yu by the station is closed for rebuilding (its foot bath by the station also closed on 15 Oct 2025). The thing to do is wander between them in a yukata and geta.",
         "The “Yumepa” day pass (¥1,500) is sold at every bathhouse. At night the river is lit up, and in winter it’s a snow scene. Bathhouse hours and closing days are in the route map.",
     ]),
     "links": [ROUTE_KINO],
     "caps": [("大谿川の柳並木", "Willows along the Otani River"), ("石の太鼓橋と柳", "An arched stone bridge and willows"), ("川沿いの木造の旅館", "Wooden inns by the river"),
              ("一の湯", "Ichi-no-yu"), ("御所の湯", "Gosho-no-yu"), ("夏の夜の花火", "Fireworks on a summer night"),
              ("夜の川沿い", "The river at night"), ("雪の夜の温泉街", "The town on a snowy night"), ("城崎温泉駅", "Kinosaki Onsen Station")]},
    {"id": "genbudo", "lat": 35.58798, "lon": 134.80426, "ja": "玄武洞（げんぶどう）", "en": "Genbudo basalt caves",
     "short": T("玄武洞", "Genbudo"), "map": gmap("玄武洞公園"),
     "time": T("豊岡駅から全但バスで「玄武洞公園」まで約15分（370円）、城崎温泉駅からは約12分（330円）。タクシーなら豊岡駅から約15分、城崎温泉駅から約10分",
               "About 15 min by Zentan Bus from Toyooka Station to “Genbudo Koen” (¥370), or about 12 min from Kinosaki Onsen Station (¥330). By taxi, about 15 min from Toyooka or 10 min from Kinosaki Onsen"),
     "body": T([
         "約160万年前の噴火で流れた溶岩が、冷えるときに六角形の柱の形に割れてできた岩の崖です。「玄武岩（げんぶがん）」という岩の名前は、ここから付けられました。国の天然記念物です。",
         "豊岡と城崎温泉のちょうど間、円山川（まるやまがわ）の東岸にあります。公園の中に洞がいくつかあり、柱が縦にも横にも曲がって並ぶようすを、すぐ近くで見られます。",
         "バスは1日に数本で、平日だけ・土日祝だけの便もあります。行きと帰りの時刻を先に決めてから出かけてください。入園は16:30までです。",
     ], [
         "A rock face made when lava from an eruption about 1.6 million years ago cracked into six-sided columns as it cooled. Basalt is called “genbugan” in Japanese after this place. It is a national natural monument.",
         "It sits on the east bank of the Maruyama River, halfway between Toyooka and Kinosaki Onsen. The park has several caves, and you can stand right in front of the columns as they run upright, sideways and in curves.",
         "There are only a few buses a day, and some run on weekdays only or weekends only, so fix your bus there and back before you set off. Last entry is at 16:30.",
     ]),
     "note": T("玄武洞公園は大人500円・学生300円。9:00〜17:00（入園は16:30まで）、12月29日〜1月3日は休み（臨時に休むこともあります）。2026年11月21日に玄武洞公園の公式サイトで確認。バスは全但バスの時刻表（2026年11月1日改正）と運賃表で確認。",
               "Genbudo Park: ¥500 (adults), ¥300 (students). 9:00–17:00 (last entry 16:30), closed 29 Dec – 3 Jan (and occasionally at other times). Checked on the park’s official website on 21 Nov 2026. Bus checked against Zentan Bus’s timetable (revised 1 Nov 2026) and fare table."),
     "links": [link("玄武洞公園（公式）", "Genbudo Park (official)", "https://genbudo-park.jp/")],
     "web": WEB["genbudo"]},
    {"id": "izushi", "lat": 35.46216, "lon": 134.87434, "ja": "出石（いずし）の城下町と皿そば", "en": "Izushi castle town and sara-soba",
     "short": T("出石", "Izushi"), "map": gmap("辰鼓楼 出石"),
     "time": T("豊岡駅から全但バスの出石行きで約30分（630円）。城崎温泉駅からの直通バスは約1時間（800円、平日1往復・土日祝3往復）",
               "About 30 min by Zentan Bus from Toyooka Station to Izushi (¥630). The direct bus from Kinosaki Onsen Station takes about 1 hour (¥800; one round trip on weekdays, three on weekends and holidays)"),
     "body": T([
         "「但馬の小京都」と呼ばれる小さな城下町です。町のまん中に、時計台の辰鼓楼（しんころう）が立っています。出石城跡の石垣や、赤い鳥居の並ぶ石段、土壁の酒蔵まで、ぜんぶ歩いて回れます。",
         "名物は出石皿そば。出石焼の小さな皿に盛ったそばを、5皿で1人前として食べます。薬味は玉子・とろろ・ねぎなど。町にはそば屋が約40軒あります。",
         "食べくらべをしたい人には、3軒で3皿ずつ食べられる「出石皿そば巡り」のセット（2,000円・税別）もあります。バスは豊岡駅から20〜40分おきに出ているので、半日あれば行って帰れます。",
     ], [
         "A small castle town known as the “little Kyoto of Tajima”. In the middle stands the Shinkoro clock tower. The stone walls of Izushi Castle, the steps lined with red torii, and the earthen-walled sake storehouse are all within walking distance.",
         "The local dish is Izushi sara-soba: soba served on small Izushi-ware plates, five plates to a portion, with egg, grated yam, spring onion and other condiments. There are about 40 soba shops in town.",
         "If you want to compare shops, the “Izushi sara-soba meguri” set (¥2,000 before tax) gets you three plates each at three shops. Buses leave Toyooka Station every 20–40 minutes, so half a day is enough for the round trip.",
     ]),
     "note": T("バスの時刻と運賃は全但バスの時刻表（2026年11月1日改正）と運賃表で、そばのことは出石観光協会のサイトで、2026年11月21日に確認。お店ごとの営業時間と休みは、出石観光協会の「そば屋一覧」で確認してください。",
               "Bus times and fares checked against Zentan Bus’s timetable (revised 1 Nov 2026) and fare table, and the soba details on the Izushi tourist association website, on 21 Nov 2026. For each shop’s hours and closing days, see the association’s soba shop list."),
     "links": [link("出石観光協会", "Izushi tourist association", "https://www.izushi.co.jp/"), link("全但バスの時刻表", "Zentan Bus timetables", "https://www.zentanbus.co.jp/local_bus/")],
     "web": WEB["izushi"]},
    {"id": "takeno", "lat": 35.66130, "lon": 134.76416, "ja": "竹野浜（たけのはま）", "en": "Takeno beach",
     "short": T("竹野浜", "Takeno"), "map": gmap("竹野浜"),
     "time": T("城崎温泉から電車で1駅・約10分（200円）。竹野駅から海まで歩いて約20分", "One stop (about 10 min, ¥200) from Kinosaki Onsen. About 20 min on foot from Takeno Station to the beach"),
     "body": T([
         "日本の渚百選にも選ばれた、透明な海と白い砂浜の海岸です。夏は海水浴の人でにぎわいますが、ほかの季節は静かで、波の音を聞きながら散歩できます。",
         "浜の東には猫崎（ねこざき）半島の山が海に突き出していて、港には漁船が並びます。城崎温泉とあわせて回るのがおすすめです。",
     ], [
         "A beach of clear water and white sand, chosen as one of Japan’s 100 best shores. It’s busy with swimmers in summer, but quiet the rest of the year, and you can walk to the sound of the waves.",
         "To the east, the Nekozaki peninsula juts into the sea, and fishing boats line the harbour. Combine it with Kinosaki Onsen.",
     ]),
     "caps": [("竹野浜と猫崎半島", "Takeno beach and the Nekozaki peninsula"), ("波打ちぎわ", "The water’s edge"), ("白い砂浜と海", "White sand and the sea"),
              ("寄せる波と山", "Waves and the headland"), ("浜から見る猫崎", "Nekozaki from the beach"),
              ("海沿いの遊歩道", "The seaside promenade"), ("竹野の港と町", "Takeno harbour and town"), ("港の漁船", "Fishing boats in the harbour"), ("竹野の神社", "A shrine in Takeno")]},
]

food = [
    {"id": "hostelact", "lat": 35.54360, "lon": 134.81892, "ja": "Hostel Act（豊岡）", "en": "Hostel Act (Toyooka)",
     "short": T("Hostel Act", "Hostel Act"), "map": gmap("Hostel Act 豊岡"),
     "time": T("豊岡駅から歩いて約6分。ふれあい公設市場の中ほど", "About 6 min on foot from Toyooka Station, halfway along the Fureai public market"),
     "body": T([
         "1泊以上するなら、拠点にとてもおすすめなのがこのゲストハウスです。昭和のはじめにできた木造アーケードの市場「ふれあい公設市場」の中にあって、のれんの並ぶ通りに小さな看板が出ています。",
         "2階が客室で、5人の相部屋（ドミトリー）と、畳の個室が2部屋。1階には共用のリビングとキッチン、シャワーがあります。オーナーご夫婦がとても気さくで、町のことやおすすめのお店をいろいろ教えてくれます。",
         "豊岡は城崎温泉まで電車で約12分、天橋立まで京都丹後鉄道で約1時間15〜25分。毎朝ここから、ちがう場所へ出かけられます。",
     ], [
         "If you’re staying a night or more, this guesthouse is the base I most recommend. It’s inside the Fureai public market, a wooden arcade market from the early Showa era, with a small sign among the curtained shopfronts.",
         "Upstairs are a 5-bed dorm and two tatami private rooms; downstairs, a shared living room, kitchen and showers. The owners, a husband and wife, are really friendly and full of tips about the town and places to eat.",
         "From Toyooka, Kinosaki Onsen is about 12 minutes by train and Amanohashidate about 1 h 15–25 min on the Kyoto Tango Railway, so every morning you can set off somewhere new.",
     ]),
     "note": STAY_NOTE,
     "links": [link("Hostel Act 公式サイト", "Hostel Act (official site)", "https://hostelact.com/"),
               link("予約のページ", "Booking page", "https://hostelact.com/booking/")],
     "caps": [("Hostel Actの看板", "The Hostel Act sign"), ("市場の通りに面した入り口", "The entrance on the market lane"), ("畳の個室", "A tatami private room"),
              ("洗面所", "The washroom"), ("洗面所とトイレの入り口", "Washroom and toilet doors"),
              ("1階のもりめ食堂の夜の定食（2023年）", "An evening set meal at Morime Shokudo downstairs (2023)")]},
]

trips = [
    {"kind": "group", "id": "g-hashidate", "ja": "天橋立・伊根", "en": "Amanohashidate and Ine",
     "time": T("京都から特急はしだてで天橋立まで約2時間（乗り換えなし）。豊岡からは京都丹後鉄道で約1時間15〜25分（1,200円）",
               "About 2 hours from Kyoto to Amanohashidate on the Hashidate express (direct). From Toyooka, about 1 h 15–25 min on the Kyoto Tango Railway (¥1,200)"),
     "body": T(["京都から日帰りでいちばんのおすすめ。回り方は、ルートマップにくわしくまとめています。"],
               ["My top pick for a day trip from Kyoto. The route map has all the details."])},
    {"id": "hashidate", "ja": "天橋立", "en": "Amanohashidate",
     "pins": [{"lat": 35.56950, "lon": 135.19100, "ja": "天橋立", "en": "Amanohashidate", "anchor": "start"}], "map": gmap("天橋立"),
     "body": T([
         "日本三景のひとつ。海の上に約3.6kmの松並木の砂州がのびています。観光船でカモメと一緒に渡り、傘松公園の上から見下ろす景色は、龍が天に昇るような形に見えます。",
     ], [
         "One of Japan’s three great views: a pine-covered sandbar about 3.6 km long across the sea. Cross by boat with the seagulls, then look down from Kasamatsu Park, where it looks like a dragon rising to the sky.",
     ]),
     "links": [ROUTE_AMA],
     "caps": [("傘松公園から見る天橋立", "Amanohashidate from Kasamatsu Park"), ("山の上から見る砂州", "The sandbar from the hilltop"), ("観光船とカモメ", "A seagull by the boat"),
              ("船から見る海", "The sea from the boat"), ("天橋立の観光船", "The sightseeing boat"), ("智恩寺の山門", "Chion-ji’s gate"),
              ("元伊勢籠神社の鳥居", "The torii of Kono Shrine"), ("ケーブルカーから見る天橋立", "Amanohashidate from the cable car")]},
    {"id": "ine", "ja": "伊根の舟屋", "en": "The boathouses of Ine",
     "pins": [{"lat": 35.67573, "lon": 135.28766, "ja": "伊根", "en": "Ine", "anchor": "start"}], "map": gmap("伊根の舟屋"),
     "body": T([
         "海に面して、1階が船のガレージになった舟屋が湾をぐるりと囲む漁村です。遊覧船から見ると、家々が海に浮かんでいるように見えます。",
         "天橋立から丹海バスで約1時間。天橋立・伊根フリーパスで乗れます。",
     ], [
         "A fishing village where boathouses, with a garage for boats on the ground floor, ring the bay. From the cruise boat the houses seem to float on the water.",
         "About an hour by Tankai bus from Amanohashidate, covered by the free pass.",
     ]),
     "links": [ROUTE_AMA],
     "caps": [("伊根湾と舟屋", "Ine Bay and the boathouses"), ("海に面した舟屋", "Boathouses on the water"), ("舟屋の並ぶ町", "A row of boathouses"),
              ("遊覧船から見る舟屋", "Boathouses from the cruise"), ("湾に並ぶ舟屋", "Boathouses around the bay"), ("カモメと遊覧船", "Seagulls and the cruise boat"), ("向井酒造", "Mukai Sake Brewery")]},

    {"kind": "group", "id": "g-maizuru", "ja": "舞鶴", "en": "Maizuru",
     "time": T("京都から特急まいづるで東舞鶴まで約1時間30分（4,370円）。西舞鶴と東舞鶴はJRで約7分（210円）。豊岡からは京都丹後鉄道で約2時間",
               "About 1 h 30 min from Kyoto to Higashi-Maizuru on the Maizuru express (¥4,370). Nishi- and Higashi-Maizuru are about 7 min apart by JR (¥210). About 2 hours from Toyooka on the Kyoto Tango Railway"),
     "body": T(["海軍の町として発展した港町です。東舞鶴には赤れんがの倉庫、西舞鶴には舟屋のような家が並ぶ入り江があります。"],
               ["A port town that grew up around the navy. Higashi-Maizuru has its red-brick warehouses; Nishi-Maizuru a cove lined with boathouse-like homes."])},
    {"id": "yoshiwara", "ja": "吉原入江（よしわらいりえ）", "en": "Yoshiwara Irie",
     "pins": [{"lat": 35.45450, "lon": 135.33000, "ja": "吉原入江", "en": "Yoshiwara Irie", "anchor": "end"}], "map": gmap("吉原入江 舞鶴"),
     "body": T([
         "西舞鶴の町の中にある入り江で、水ぎわに家と船がぎっしり並びます。伊根の舟屋に似ていることから「舞鶴の伊根」とも呼ばれています。",
         "朝の静かな水面に家と船が映る景色や、夕日が山に沈むころがとくにきれいです。西舞鶴駅から歩いて約20分。",
     ], [
         "A cove in the middle of Nishi-Maizuru, where houses and boats crowd the water’s edge. It looks so like Ine’s boathouses that it’s called “the Ine of Maizuru”.",
         "It’s loveliest in the still morning, when houses and boats are mirrored in the water, or as the sun sets behind the hills. About 20 minutes on foot from Nishi-Maizuru Station.",
     ]),
     "caps": [("朝の吉原入江", "Yoshiwara Irie in the morning"), ("入り江に並ぶ家", "Houses along the cove"),
              ("入り江の船", "Boats in the cove"), ("静かな水面", "Still water"), ("夕方の入り江", "The cove in the evening"),
              ("山に沈む夕日", "Sunset behind the hills"), ("夕焼けの空", "The evening sky"), ("入り江と漁船", "The cove and fishing boats")]},
    {"id": "akarenga", "ja": "舞鶴赤れんがパークと北吸トンネル", "en": "Maizuru Red Brick Park and the Kitasui tunnel",
     "pins": [{"lat": 35.47556, "lon": 135.38285, "ja": "赤れんがパーク", "en": "Red Brick Park", "anchor": "start"}], "map": gmap("舞鶴赤れんがパーク"),
     "body": T([
         "明治から大正にかけて、旧海軍が建てた赤れんがの倉庫が並ぶ公園です。中は博物館やお店、イベントの会場になっています。目の前の港には、自衛隊の船が見えることもあります。",
         "東舞鶴駅からは、旧海軍の鉄道のトンネルだった北吸（きたすい）トンネルを通って歩いていけます（駅から約20分）。",
     ], [
         "A park of red-brick warehouses built by the old Imperial Navy from the Meiji to Taisho eras. Inside are a museum, shops and event spaces. In the harbour opposite you may see Self-Defense Force ships.",
         "From Higashi-Maizuru Station you can walk there through the Kitasui tunnel, once a naval railway tunnel (about 20 minutes).",
     ]),
     "note": T("9:00〜17:00（夜のイベントがある日は22:00まで）。2026年11月20日に公式サイトで確認。", "9:00–17:00 (until 22:00 on evenings with events). Checked on the official website on 20 Nov 2026."),
     "caps": [("赤れんが倉庫の並ぶ広場", "The square of red-brick warehouses"), ("倉庫の前の庭", "The lawn in front of the warehouses"),
              ("つたのからまる倉庫", "Ivy on the warehouses"), ("赤れんが倉庫", "A red-brick warehouse"), ("倉庫とテーブル", "Warehouses and tables"),
              ("北吸トンネルの中", "Inside the Kitasui tunnel"), ("北吸トンネルの入り口", "The Kitasui tunnel entrance"), ("港に泊まる船", "Ships in the harbour"), ("倉庫の中", "Inside a warehouse")]},

    {"kind": "group", "id": "g-takeda", "ja": "竹田城跡", "en": "Takeda Castle Ruins",
     "time": T("豊岡から電車で竹田まで、和田山で乗り換えて約45分〜1時間15分（680円）。本数が少ないので時刻を確認してください", "About 45 min to 1 h 15 min by train from Toyooka to Takeda, changing at Wadayama (¥680). Trains are few, so check the times"),
     "body": T(["但馬の山の上に石垣だけが残る「天空の城」です。"], ["The “castle in the sky”: only its stone walls remain on a mountaintop in Tajima."])},
    {"id": "takeda", "ja": "竹田城跡", "en": "Takeda Castle Ruins",
     "pins": [{"lat": 35.30029, "lon": 134.82937, "ja": "竹田城跡", "en": "Takeda Castle", "anchor": "start"}], "map": gmap("竹田城跡"),
     "body": T([
         "標高約350mの山の上に、石垣がほぼそのまま残っています。石垣の上からは、まわりの山と町が360度見渡せます。秋の早朝には雲海に浮かぶ姿が見られることもあります。",
         "竹田駅からは天空バスかタクシーで山の中腹へ行き、そこから歩いて約20分です。",
     ], [
         "On a mountaintop about 350 m up, the stone walls survive almost intact, with 360° views over the surrounding hills and town. On some autumn mornings the ruins float above a sea of clouds.",
         "From Takeda Station, take the Tenku Bus or a taxi halfway up, then walk about 20 minutes.",
     ]),
     "note": T("大人（高校生以上）500円。1月4日〜2月末は冬の閉山。駅の裏から登る道はクマ対策で閉鎖中（2026年10月の公式サイトの案内）。くわしくはルートマップで。",
               "¥500 (high school and up). Closed for winter 4 Jan – end of Feb. The trail from behind the station is closed as a bear precaution (official notice, Oct 2026). Details in the route map."),
     "links": [ROUTE_KINO],
     "caps": [("山の上の石垣と町", "Stone walls above the town"), ("石垣と谷", "The walls and the valley"), ("見上げる石垣", "Looking up at the walls"),
              ("松と石垣", "A pine and the walls"), ("石垣の上から見る山", "The mountains from the walls"), ("本丸の広場", "The main enclosure")]},
]

no = 1
for s in city + food:
    s["no"] = no; no += 1
no = 1
for s in trips:
    if s.get("kind") != "group":
        s["no"] = no; no += 1
for s in city + food + trips:
    if "caps" in s or "web" in s:
        s["photos"] = (photos(s["id"], s.pop("caps")) if "caps" in s else []) + web_photos(s["id"], s.pop("web", []))

G = {"intro": intro, "outro": outro, "plans": plans, "city": city, "food": food, "trips": trips, "refs": [],
     "region": json.load(open(f"{R}/scripts/tango_tajima_region.json", encoding="utf-8")),
     "sources": {"checked": "2026-11-20", "list": [
         "https://hostelact.com/room-facility/",
         "https://hostelact.com/access/",
         "https://hostelact.com/morime-shokudo/",
         "https://hostelact.com/booking/",
         "https://akarenga-park.com/",
         "https://www.city.asago.hyogo.jp/site/takeda/",
         "https://www.tankai.jp/tourist_tickets/",
         "https://kinosaki-spa.gr.jp/news/27947",
         "https://transit.yahoo.co.jp/",
         "https://genbudo-park.jp/",
         "https://www.izushi.co.jp/access/",
         "https://www.izushi.co.jp/sobahistory/",
         "https://www.izushi.co.jp/sobameguri/",
         "https://www.zentanbus.co.jp/local_bus/"]}}
js = "/* Generated by scripts/build_tango_tajima_data.py: spots, text (EN/JA), plans, photos and map data for the Tango & Tajima guide. */\nwindow.GUIDE = " + json.dumps(G, ensure_ascii=False, indent=1) + ";\n"
os.makedirs(f"{SITE}/js", exist_ok=True)
open(f"{SITE}/js/data.js", "w", encoding="utf-8").write(js)
print("ok", len(city), len(food), len([t for t in trips if t.get("kind") != "group"]))
