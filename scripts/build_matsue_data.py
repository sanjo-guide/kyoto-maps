#!/usr/bin/env python3
"""松江・足立美術館ガイド（matsue/）の js/data.js を作る（tango-tajima/ と同じ形。モデルプランつき）。

使い方: python3 scripts/build_matsue_data.py
- 文章・料金・時間・モデルプランはこのファイルの中。直したらこのスクリプトを実行し直す（data.js を直接直さない）
- 写真は matsue/img/<id>-<番号>.jpg。キャプションの数と写真の数が合わないと止まる
- 行っていない場所（出雲大社・稲佐の浜）は Wikimedia Commons の写真 matsue/img/web-<id>-<番号>.jpg を使う。
  スポットの "web" に W(キャプション日, 英, 撮影者, ライセンス, ファイルページ) を並べる（自分の写真のあとに付く。クレジットはページに自動で出る）
- 写真は Toshi の写真ライブラリから（松江 2024年9月9日、足立美術館 2025年1月25日。長辺1280px・位置情報なし・横向きだけ。
  人が写っている写真は使っていない）
- 簡易地図の輪郭は scripts/matsue_region.json
"""
import json, os, struct, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = f"{R}/matsue"
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


def W(ja, en, author, lic, page):
    """Web（Wikimedia Commons）の写真1枚。"""
    return {"cap": T(ja, en), "credit": {"author": author, "license": lic, "page": page}}


def photos(pid, caps, web=()):
    """自分の写真 <id>-<n>.jpg（caps の順）のあとに、Web の写真 web-<id>-<n>.jpg（web の順、クレジットつき）を並べる。"""
    files = sorted([f for f in os.listdir(IMG) if f.startswith(pid + "-") and f[len(pid) + 1:-4].isdigit()],
                   key=lambda f: int(f[len(pid) + 1:-4]))
    assert len(files) == len(caps), (pid, len(files), len(caps))
    out = []
    for f, c in zip(files, caps):
        w, h = jpeg_size(os.path.join(IMG, f))
        out.append({"f": f, "cap": T(*c), "w": w, "h": h})
    pre = "web-" + pid + "-"
    wfiles = [f for f in os.listdir(IMG) if f.startswith(pre) and f[len(pre):-4].isdigit()]
    assert len(wfiles) == len(web), (pid, "web", len(wfiles), len(web))
    for n, x in enumerate(web, 1):
        f = f"{pre}{n}.jpg"
        assert os.path.exists(os.path.join(IMG, f)), ("web photo missing", f)
        w, h = jpeg_size(os.path.join(IMG, f))
        out.append({"f": f, "cap": x["cap"], "w": w, "h": h, "credit": x["credit"]})
    assert out, (pid, "no photos")
    return out


intro = T([
    "島根県の松江（まつえ）と、安来（やすぎ）の足立美術館、そして出雲大社（いずもおおやしろ）をまとめました。",
    "松江は京都から新幹線で岡山へ行き、特急やくもに乗りかえて約4時間。町の真ん中に、江戸時代の天守が残る国宝の松江城があり、お城のまわりのお堀を小さな船でめぐれます。",
    "松江から電車で約25分の安来には、日本庭園のランキングで20年以上日本一に選ばれ続けている足立美術館があります。",
    "松江から西へ電車で約1時間の出雲には、縁結びの神様で知られる出雲大社があります。足立美術館とは反対の方向なので、両方行くなら松江に2泊がおすすめです。",
    "松江だけなら日帰りもできますが、1泊すると、宍道湖（しんじこ）の夕日や温泉もゆっくり楽しめます。いちばん大事なのは、予定を詰め込みすぎないことです。",
], [
    "Here are my picks for Matsue in Shimane, with the Adachi Museum of Art in Yasugi and the Izumo Taisha shrine.",
    "Matsue is about 4 hours from Kyoto: shinkansen to Okayama, then the Yakumo limited express. In the middle of town stands Matsue Castle, a National Treasure whose keep survives from the Edo period, and you can tour its moats by small boat.",
    "About 25 minutes from Matsue by train, in Yasugi, is the Adachi Museum of Art, whose garden has been ranked Japan’s best for more than 20 years in a row.",
    "About an hour west of Matsue by train is Izumo Taisha, the shrine known for its god of good matches. It is in the opposite direction from the Adachi Museum, so stay two nights in Matsue if you want both.",
    "Matsue alone works as a day trip, but with a night there you can also enjoy the sunset over Lake Shinji and the hot springs. Above all, don’t overpack your schedule.",
])
outro = T([
    "以上が、松江と足立美術館、出雲大社のおすすめです。",
    "黒い天守とお堀の町・松江、絵のような庭の足立美術館、大きなしめ縄の出雲大社。山陰の落ち着いた空気を、ゆっくり味わってください。",
    "電車の本数が少ないところもあるので、時刻を先に確かめて、無理せず、自分らしい旅を楽しんでください。",
], [
    "That’s my list for Matsue, the Adachi Museum and Izumo Taisha.",
    "Matsue with its black castle keep and moats, the Adachi Museum with its picture-like garden, and Izumo Taisha with its giant straw rope: take your time and enjoy the calm of the San’in coast.",
    "Some trains are infrequent, so check the times first, don’t push yourself, and enjoy the trip your own way.",
])

ROUTE_NOTE = T("時刻と運賃は2026年11月の乗換案内の例です。出かける前に確認してください。", "Times and fares are examples from a route planner (Nov 2026). Check before you go.")

DAY1 = T("京都7:53発の新幹線で岡山へ、特急やくもに乗りかえて松江11:48着（14,420円）。松江城・興雲閣・塩見縄手・堀川めぐりを回って、日の入りの1時間ほど前に島根県立美術館の湖岸へ（松江駅から歩いて約15分）。宍道湖の夕日を見てから、湖のほとりの松江しんじ湖温泉に泊まります。",
         "Shinkansen from Kyoto at 7:53 to Okayama, then the Yakumo to Matsue, arriving 11:48 (¥14,420). See the castle, Kounkaku, Shiomi Nawate and the moat boats, then head to the lakeside by the Shimane Art Museum about an hour before sunset (about 15 min on foot from Matsue Station). Watch the sun set over Lake Shinji and stay at Matsue Shinjiko Onsen on the lakeshore.")
ADACHI_DAY = T("松江9:37発の電車で安来へ（10:04着・420円）。駅前から足立美術館の無料シャトルバスで約20分。庭をゆっくり見て、安来14:25発の特急やくもで岡山へ、新幹線で京都17:59着（14,090円）。",
               "Train from Matsue at 9:37 to Yasugi (10:04, ¥420), then the museum’s free shuttle bus (about 20 min). Take your time in the garden, then the 14:25 Yakumo from Yasugi to Okayama and the shinkansen to Kyoto, arriving 17:59 (¥14,090).")

plans = [
    {"id": "plan-day", "title": T("日帰り（京都から）", "Day trip from Kyoto"),
     "sub": T("松江城と塩見縄手、堀川めぐり", "Matsue Castle, Shiomi Nawate and the moat boats"),
     "days": [
         {"label": T("1日目", "Day 1"),
          "text": T("京都7:53発の新幹線で岡山へ、特急やくもに乗りかえて松江11:48着（14,420円）。松江城の天守に上り、興雲閣と塩見縄手を歩いて、堀川めぐりの船へ。松江17:10発のやくもで京都21:01着。",
                    "Shinkansen from Kyoto at 7:53 to Okayama, then the Yakumo to Matsue, arriving 11:48 (¥14,420). Climb the castle keep, walk past Kounkaku and along Shiomi Nawate, then take a moat boat. Back on the 17:10 Yakumo, reaching Kyoto at 21:01.")}],
     "note": ROUTE_NOTE},
    {"id": "plan-1", "title": T("1泊2日（松江と足立美術館）", "1 night: Matsue and the Adachi Museum"),
     "sub": T("松江に泊まって、2日目は足立美術館へ", "A night in Matsue, then the Adachi Museum"),
     "days": [
         {"label": T("1日目", "Day 1"), "text": DAY1},
         {"label": T("2日目", "Day 2"), "text": ADACHI_DAY}],
     "note": ROUTE_NOTE},
    {"id": "plan-izumo", "title": T("1泊2日（松江と出雲大社）", "1 night: Matsue and Izumo Taisha"),
     "sub": T("松江に泊まって、2日目は出雲大社から京都へ帰る", "A night in Matsue, then Izumo Taisha and home from Izumo"),
     "days": [
         {"label": T("1日目", "Day 1"), "text": DAY1},
         {"label": T("2日目", "Day 2"),
          "text": T("松江しんじ湖温泉駅8:08発の一畑電車に乗り、川跡（かわと）で乗りかえて出雲大社前9:13着（900円。平日の例で、土曜は8:34発→9:37着）。午前のうちに出雲大社をお参りして、神楽殿の大しめ縄を見てから、歩いて15分の稲佐の浜へ。駅前の神門通りでお昼にして、出雲大社前14:20発の電車で電鉄出雲市へ。JR出雲市15:35発の特急やくもで岡山へ、新幹線で京都19:58着（出雲大社前から14,050円）。松江には戻りません。",
                    "Take the 8:08 Ichibata train from Matsue Shinjiko Onsen Station, change at Kawato and reach Izumo Taisha-mae at 9:13 (¥900; a weekday example, on Saturdays 8:34 → 9:37). Visit the shrine in the morning, see the giant straw rope at the Kagura-den, then walk 15 minutes to Inasa Beach. Have lunch on Shinmon-dori by the station, then take the 14:20 train to Dentetsu Izumoshi. The 15:35 Yakumo from JR Izumoshi and the shinkansen from Okayama get you to Kyoto at 19:58 (¥14,050 from Izumo Taisha-mae). You don’t go back to Matsue.")}],
     "note": ROUTE_NOTE},
    {"id": "plan-2", "title": T("2泊3日", "2 nights, 3 days"),
     "sub": T("松江に2泊して、出雲大社と足立美術館を1日ずつ", "Two nights in Matsue: a day each for Izumo Taisha and the Adachi Museum"),
     "days": [
         {"label": T("1日目", "Day 1"), "text": DAY1},
         {"label": T("2日目", "Day 2"),
          "text": T("松江しんじ湖温泉駅8:08発の一畑電車で出雲大社前9:13着（川跡で乗りかえ、900円。土曜は8:34発→9:37着）。出雲大社と稲佐の浜をゆっくり回って、出雲大社前15:20発の電車で松江しんじ湖温泉16:26着。1日目に夕日を見られなかったら、この日の夕方に。往復するだけなら、1日フリー乗車券（1,800円）は往復の運賃と同じ値段です。",
                    "Take the 8:08 Ichibata train from Matsue Shinjiko Onsen Station to Izumo Taisha-mae, arriving 9:13 (change at Kawato, ¥900; on Saturdays 8:34 → 9:37). Take your time at the shrine and Inasa Beach, then the 15:20 train back, reaching Matsue Shinjiko Onsen at 16:26. If you missed the sunset on day 1, catch it this evening. For a simple return trip, the one-day pass (¥1,800) costs the same as two single tickets.")},
         {"label": T("3日目", "Day 3"), "text": ADACHI_DAY}],
     "note": ROUTE_NOTE},
]

city = [
    {"id": "matsuejo", "lat": 35.47522, "lon": 133.05080, "ja": "松江城（国宝の天守）", "en": "Matsue Castle (National Treasure keep)",
     "short": T("松江城", "Matsue Castle"), "map": gmap("松江城"),
     "time": T("JR松江駅から歩いて約30分（約2km）。お城の近くまで行くバスもあります", "About 30 min on foot from JR Matsue Station (about 2 km); buses also run near the castle"),
     "body": T([
         "江戸時代に建てられた天守が今も残る、全国で12しかないお城のひとつで、天守は国宝です。黒い板張りの外観から「千鳥城（ちどりじょう）」とも呼ばれます。",
         "天守の中は木の柱と急な階段が続き、いちばん上の階からは、松江の町と宍道湖がぐるりと見渡せます。天守では靴をぬいで上がります。",
     ], [
         "One of only twelve castles in Japan whose original Edo-period keep survives, and the keep is a National Treasure. Its black-boarded walls give it the nickname “Plover Castle”.",
         "Inside are wooden pillars and steep stairs, and from the top floor you can see all around Matsue and Lake Shinji. Shoes come off inside the keep.",
     ]),
     "note": T("天守は大人1,200円・小中学生無料（2026年7月から）。4〜9月 8:30〜18:00、10〜3月 8:30〜17:00（受付は30分前まで）、年中無休。2027年6月からの大修理では、工事の覆いをつける時と外す時の各4か月は天守に上れません（2027年5月までは通常どおり）。2026年1月の地震で、城山の北ノ門〜水の手門は通行止め。2026年11月20日に公式サイトと松江市のサイトで確認。",
               "Keep: ¥1,200 for adults, free for elementary and junior-high pupils (from July 2026). April–September 8:30–18:00, October–March 8:30–17:00 (last entry 30 min before), open every day. During the major repairs from June 2027, the keep closes for four months while the scaffolding cover goes up and four months while it comes down (normal access until May 2027). Since the January 2026 earthquake, the path from Kitanomon to Mizunotemon gate is closed. Checked on the official and Matsue City websites on 20 Nov 2026."),
     "caps": [("黒い板張りの天守", "The black-boarded keep"),
              ("石垣の上に建つ天守", "The keep on its stone walls"),
              ("本丸から見る天守", "The keep from the main enclosure"),
              ("天守から見る松江の町と宍道湖", "Matsue and Lake Shinji from the keep"),
              ("屋根の向こうの町並み", "The town beyond the roof"),
              ("天守の中の木の柱", "Wooden pillars inside the keep"),
              ("木々の向こうの天守", "The keep through the trees")]},
    {"id": "kounkaku", "lat": 35.47358, "lon": 133.05048, "ja": "興雲閣（こううんかく）", "en": "Kounkaku",
     "short": T("興雲閣", "Kounkaku"), "map": gmap("興雲閣 松江"),
     "time": T("松江城の天守から歩いて約3分", "About 3 min on foot from the castle keep"),
     "body": T([
         "1903年（明治36年）に建てられた、白い木造の洋館です。お城の敷地の中にあり、島根県の文化財になっています。",
         "赤いじゅうたんの階段や、大きな窓から光が入る広間など、明治の建物の雰囲気をそのまま楽しめます。入館は無料です。",
     ], [
         "A white wooden Western-style building from 1903, inside the castle grounds and designated a Shimane Prefecture cultural property.",
         "The red-carpeted staircase and the bright halls with tall windows keep the Meiji-era feel. Entry is free.",
     ]),
     "note": T("入館無料、年中無休。4〜9月 8:30〜18:00（最後の入館17:45）、10〜3月 8:30〜17:00（同16:45）。2階の大広間は貸し切りで見られない日があります。2026年11月20日に公式サイトで確認。",
               "Free, open every day. April–September 8:30–18:00 (last entry 17:45), October–March 8:30–17:00 (last entry 16:45). The upstairs hall is sometimes closed for private use. Checked on the official website on 20 Nov 2026."),
     "caps": [("白い洋館の興雲閣", "Kounkaku, a white Western-style building"),
              ("赤いじゅうたんの階段", "The red-carpeted staircase"),
              ("2階の大広間", "The upstairs hall"),
              ("窓の多い部屋", "A room with many windows"),
              ("1階の部屋", "A ground-floor room")]},
    {"id": "shiomi", "lat": 35.47820, "lon": 133.05000, "ja": "塩見縄手（しおみなわて）と堀川", "en": "Shiomi Nawate and the castle moat",
     "short": T("塩見縄手", "Shiomi Nawate"), "map": gmap("塩見縄手"),
     "time": T("松江城の北の門から歩いてすぐ", "Just outside the castle’s north side"),
     "body": T([
         "お城の北のお堀に沿って、武士の屋敷が並んでいた通りです。黒い板塀と松の木が続き、「日本の道100選」にも選ばれています。武家屋敷や、小泉八雲（ラフカディオ・ハーン）の旧居と記念館もこの通りにあります。",
         "お堀は「堀川めぐり」の船で1周約50分。橋の下をくぐるときは、船の屋根が低く下がります。冬は、こたつのある船になります。",
     ], [
         "A street of samurai houses along the castle’s north moat, lined with black board fences and pine trees and chosen as one of Japan’s 100 best roads. The samurai residence and Lafcadio Hearn’s former home and memorial museum are on this street too.",
         "The Horikawa boat tour circles the moats in about 50 minutes; the boat’s roof lowers to pass under the bridges. In winter the boats have kotatsu heated tables.",
     ]),
     "note": T("堀川めぐりは一日乗船券 大人2,000円（その日は何度でも乗れます）、3〜9月 9:00〜17:00、10〜2月 9:00〜16:00、船の中では靴をぬぎます。武家屋敷は大人400円、小泉八雲記念館は大人600円。2026年11月20日に各公式サイトで確認。",
               "Horikawa boat tour: one-day ticket ¥2,000 for adults (ride as often as you like that day), March–September 9:00–17:00, October–February 9:00–16:00; shoes off on board. Samurai residence ¥400, Lafcadio Hearn Memorial Museum ¥600 (adults). Checked on the official websites on 20 Nov 2026."),
     "caps": [("塩見縄手の通り", "Shiomi Nawate"),
              ("お堀を行く堀川めぐりの船", "A Horikawa tour boat on the moat"),
              ("武家屋敷の長屋門", "A samurai-house gatehouse"),
              ("緑に囲まれたお堀", "The tree-lined moat"),
              ("黒い板塀の屋敷", "A house with a black board fence"),
              ("お堀と松", "The moat and pines"),
              ("木々の間のお堀", "The moat among the trees")]},
    {"id": "shinjiko", "lat": 35.45950, "lon": 133.05160, "ja": "宍道湖（しんじこ）の夕日", "en": "Sunset over Lake Shinji",
     "short": T("宍道湖の夕日", "Lake Shinji sunset"), "map": gmap("島根県立美術館"),
     "extra_map": [{"ja": "夕日スポット（とるぱ）", "en": "Sunset spot (Torupa)", "map": gmap("宍道湖夕日スポット とるぱ")}],
     "links": [{"ja": "今日の日の入りの時刻", "en": "Today’s sunset time (JP)", "url": "https://www.kankou-matsue.jp/omoshiro/sunset/266"}],
     "time": T("JR松江駅から歩いて約15分。松江市営バスの南循環線内回りなら6分で「県立美術館前」", "About 15 min on foot from JR Matsue Station, or 6 min on the city bus (South Loop, inner circle) to “Kenritsu Bijutsukan-mae”"),
     "body": T([
         "松江の1日は、宍道湖の夕日で終わるのが定番です。私は島根県立美術館の横の、湖岸の芝生へ行きました。日の入りの1時間ほど前に着くと、まだ人が少なく、湖に光の道ができていくのをゆっくり見られます。写真は2024年9月、17時20分ごろです。",
         "芝生には、12羽のうさぎの像「宍道湖うさぎ」が湖に向かって並んでいます。美術館は1階のロビーまで無料で入れるので、風の強い日や寒い日はガラス越しに眺められます。",
         "湖岸を南へ600mほど歩くと「宍道湖夕日スポット（とるぱ）」があります。小さな嫁ヶ島（よめがしま）が夕日の手前に入る場所で、腰かけられるテラスがあります。",
     ], [
         "A day in Matsue traditionally ends with the sunset over Lake Shinji. I went to the lakeside lawn beside the Shimane Art Museum. Arrive about an hour before sunset: there are still few people, and you can watch the path of light grow across the water. My photos are from September 2024, at about 17:20.",
         "Twelve bronze rabbits, the “Shinjiko Usagi”, line up on the lawn facing the lake. The museum’s ground-floor lobby is free to enter, so on a windy or cold day you can watch through the glass.",
         "About 600 m south along the shore is the Lake Shinji Sunset Spot (Torupa), where tiny Yomegashima island sits in front of the setting sun and there are terraces to sit on.",
     ]),
     "note": T("島根県立美術館は10:00〜18:30、3〜9月は日の入りの30分後まで。火曜と12月28日〜1月1日は休み（展覧会によって変わります）。1階ロビーは無料、コレクション展は400円。日の入りは6月が19時半ごろ、12月は17時前と、季節で大きく変わります。松江観光協会のサイトに毎日の時刻があります。2026年11月21日に美術館と松江観光協会の公式サイトで確認。",
               "Shimane Art Museum: 10:00–18:30, and until 30 minutes after sunset from March to September. Closed Tuesdays and 28 Dec – 1 Jan (may change with exhibitions). The ground-floor lobby is free; the collection galleries cost ¥400. Sunset ranges from about 19:30 in June to before 17:00 in December; the Matsue Tourism Association lists the time for every day. Checked on the museum and tourism association websites on 21 Nov 2026."),
     "caps": [("湖岸の芝生と宍道湖に傾く日", "The lakeside lawn and the sun sinking towards Lake Shinji"), ("美術館のテラスと湖", "The museum terrace and the lake"),
              ("宍道湖と松江の町", "Lake Shinji and the town of Matsue"), ("島根県立美術館の入り口", "The entrance to the Shimane Art Museum")]},
]

food = []

trips = [
    {"kind": "group", "id": "g-yasugi", "ja": "安来（やすぎ）", "en": "Yasugi",
     "time": T("JR松江駅から山陰本線の普通電車で安来まで約25分（420円）。京都からなら岡山で特急やくもに乗りかえて安来まで約3時間40分（14,090円）",
               "About 25 min by local train on the San’in Line from JR Matsue to Yasugi (¥420). From Kyoto, change to the Yakumo at Okayama: about 3 h 40 min to Yasugi (¥14,090)"),
     "body": T([
         "松江と米子のあいだの町です。駅前から、足立美術館の無料シャトルバスが出ています。",
     ], [
         "A town between Matsue and Yonago. The Adachi Museum’s free shuttle bus leaves from the station.",
     ])},
    {"id": "adachi", "ja": "足立美術館", "en": "Adachi Museum of Art",
     "pins": [{"lat": 35.38084, "lon": 133.19547, "ja": "足立美術館", "en": "Adachi Museum", "anchor": "end"},
              {"lat": 35.42806, "lon": 133.25925, "ja": "安来駅", "en": "Yasugi Sta.", "anchor": "start", "minor": True}],
     "map": gmap("足立美術館"),
     "body": T([
         "横山大観などの日本画と、5万坪の日本庭園で知られる美術館です。アメリカの日本庭園の専門誌のランキングで、2003年から23年続けて日本一に選ばれています。",
         "白い砂と松、まるく刈った木々の向こうに、本物の山が庭の一部のように重なります。窓の枠を額に見立てた「生の額絵」など、建物の中から眺めるのが基本です。写真は2025年1月25日。冬でも緑が美しい庭でした。",
     ], [
         "A museum known for Japanese-style paintings such as those of Yokoyama Taikan, and for its 165,000 m² garden, ranked Japan’s best by an American journal of Japanese gardens for 23 years running since 2003.",
         "White sand, pines and rounded shrubs lead the eye to real mountains that seem part of the garden. You mostly view it from inside, with windows framing it like living paintings. Photos from 25 January 2025: green and beautiful even in winter.",
     ]),
     "note": T("入館料は大人2,500円。4〜9月 9:00〜17:30、10〜3月 9:00〜17:00、年中無休（新館だけ展示替えの休みあり）。安来駅から無料シャトルバス（1日17本、約20分、予約なし・先着25人）。近くのさぎの湯温泉で日帰り入浴もできます。2026年11月20日に公式サイトで確認。",
               "Admission ¥2,500 for adults. April–September 9:00–17:30, October–March 9:00–17:00, open every day (the new wing closes for exhibition changes). Free shuttle bus from Yasugi Station (17 a day, about 20 min, no booking, first 25 people). You can also bathe at nearby Saginoyu Onsen. Checked on the official website on 20 Nov 2026."),
     "caps": [("白い砂と松の庭と山", "White sand, pines and the mountains"),
              ("石と刈り込みの木の庭", "Rocks and clipped shrubs"),
              ("山に続く庭", "The garden leading to the hills"),
              ("池のある庭", "The pond garden"),
              ("池と石の庭", "The pond and rocks"),
              ("松の幹の向こうの庭", "The garden beyond a pine trunk"),
              ("苔の中庭", "The moss courtyard"),
              ("廊下の先に見える庭", "The garden at the end of a corridor"),
              ("白砂の庭と空", "The white-sand garden and the sky"),
              ("美術館の入り口", "The museum entrance")]},

    {"kind": "group", "id": "g-izumo", "ja": "出雲（いずも）", "en": "Izumo",
     "time": T("松江しんじ湖温泉駅から一畑電車で出雲大社前駅まで約1時間（900円）。ほとんどの電車は川跡（かわと）で乗りかえ。JRなら松江から出雲市まで特急で約30分・普通で約45分（590円、特急は自由席760円を追加）、出雲市駅から一畑バスで約25分",
               "About 1 hour on the Ichibata Electric Railway from Matsue Shinjiko Onsen Station to Izumo Taisha-mae (¥900); most trains need a change at Kawato. By JR, Matsue to Izumoshi takes about 30 min by limited express or 45 min by local train (¥590, plus ¥760 for an unreserved express seat), then about 25 min by Ichibata bus"),
     "body": T([
         "松江から宍道湖の北岸を西へ。一畑電車は湖のすぐ横を走るので、行きは進行方向の左側の席がおすすめです。松江しんじ湖温泉駅は、JR松江駅から市営バスで15〜20分ほど（250円）。泊まる場所が松江駅の近くなら、JRとバスで行くほうが乗りかえが楽です。",
     ], [
         "Head west from Matsue along the north shore of Lake Shinji. The Ichibata train runs right beside the water, so sit on the left on the way out. Matsue Shinjiko Onsen Station is 15–20 minutes by city bus from JR Matsue Station (¥250); if you are staying near JR Matsue, going by JR and bus means easier connections.",
     ])},
    {"id": "izumo", "ja": "出雲大社（いずもおおやしろ）", "en": "Izumo Taisha",
     "pins": [{"lat": 35.40121, "lon": 132.68551, "ja": "出雲大社", "en": "Izumo Taisha", "anchor": "start"},
              {"lat": 35.39353, "lon": 132.68710, "ja": "出雲大社前駅", "en": "Izumo Taisha-mae Sta.", "anchor": "start", "dy": 16, "ldir": "bottom", "minor": True},
              {"lat": 35.46737, "lon": 133.04604, "ja": "松江しんじ湖温泉駅", "en": "Matsue Shinjiko Onsen Sta.", "anchor": "end", "dy": -8, "ldir": "left", "minor": True}],
     "map": gmap("出雲大社"),
     "time": T("一畑電車の出雲大社前駅から、神門通りを歩いて約10分", "About 10 min on foot up Shinmon-dori from Izumo Taisha-mae Station"),
     "body": T([
         "縁結びの神様、大国主大神（おおくにぬしのおおかみ）をまつる神社です。「勢溜（せいだまり）の大鳥居」から松の参道を下っていくと拝殿があり、その奥に高さ24mの国宝の御本殿が建っています。お参りは「二礼四拍手一礼」。手を4回打つのが出雲大社の作法です。",
         "写真でよく見る大きなしめ縄は、拝殿ではなく、西へ歩いて3分ほどの神楽殿（かぐらでん）にあります。長さ約13m、重さ5.2トン。拝殿だけ見て帰ってしまう人が多いので、忘れずに寄ってください。",
         "御本殿の裏側は16時30分に閉まります。人の少ない午前のうちに着いて、裏までぐるりと回るのがおすすめです。松の参道は、根を守るために真ん中を歩けません。両わきの道を歩きます。",
     ], [
         "The shrine of Okuninushi, the god of good matches. From the big Seidamari torii, the pine-lined approach leads down to the worship hall, and behind it stands the main hall, a National Treasure 24 m high. Pray the Izumo way: bow twice, clap four times, bow once.",
         "The giant straw rope you see in photos is not at the worship hall but at the Kagura-den, about 3 minutes’ walk to the west. It is about 13 m long and weighs 5.2 tonnes. Many people see only the worship hall and leave, so don’t miss it.",
         "The area behind the main hall closes at 16:30. Arrive in the morning, when it is quieter, and walk all the way round the back. On the pine approach the centre path is closed to protect the roots, so walk along either side.",
     ]),
     "note": T("参拝は6:00〜19:00、無料。宝物殿（神祜殿）は8:30〜16:30（入館は16:00まで）、大人300円。全国の神様が集まる旧暦10月の神在祭（かみありさい）のころは、とても混みます（2026年は11月下旬）。出雲市駅からのバスは「正門前」で降りると大鳥居の前です（運賃は要確認）。2026年11月21日に出雲大社と出雲観光協会の公式サイトで確認。電車の時刻と運賃は乗換案内（2026年11月）。",
               "Open 6:00–19:00, free. Treasure hall (Shinko-den) 8:30–16:30 (last entry 16:00), ¥300 for adults. It gets very crowded around the Kamiari Festival in the 10th lunar month, when the gods of Japan are said to gather here (late November in 2026). The bus from Izumoshi Station stops at “Seimon-mae”, right by the big torii (fare: please check). Checked on the Izumo Taisha and Izumo Tourism Association websites on 21 Nov 2026; train times and fares from a route planner (Nov 2026)."),
     "web": [W("神楽殿の大しめ縄", "The giant straw rope at the Kagura-den", "Kanesue", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:Kaguraden_of_Izumo_Taisha_Shrine_-_Jun_9,_2025.jpg"),
             W("拝殿", "The worship hall", "Suicasmo", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Izumo_Taisha_20170126-1.jpg"),
             W("銅の鳥居と拝殿", "The bronze torii and the worship hall", "Raita Futo from Tokyo, Japan", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Izumo_Taisha_Grand_Shrine_(51822283655).jpg"),
             W("奥に見える御本殿の屋根", "The roof of the main hall beyond", "Raita Futo from Tokyo, Japan", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Izumo_Taisha_Grand_Shrine_(51821905204).jpg")]},
    {"id": "inasa", "ja": "稲佐の浜（いなさのはま）", "en": "Inasa Beach",
     "pins": [{"lat": 35.40030, "lon": 132.67190, "ja": "稲佐の浜", "en": "Inasa Beach", "anchor": "end"}],
     "map": gmap("稲佐の浜"),
     "time": T("出雲大社から西へ歩いて約15分（約1.2km）", "About 15 min on foot west of Izumo Taisha (about 1.2 km)"),
     "body": T([
         "出雲大社の西にある、神話の舞台の浜です。旧暦の10月10日、全国の神様をここでお迎えすると伝えられています。",
         "砂浜にぽつんと立つ岩が弁天島（べんてんじま）で、上に小さな鳥居とお社があります。今は砂浜が広がって、島の裏側まで歩いて回れます。",
         "西向きの浜なので、晴れた日は夕方がきれいです。ただ、帰りの電車は1時間に1本ほど。出雲大社前駅までは歩いて25分ほどかかるので、電車の時刻を先に決めてから浜へ向かってください。",
     ], [
         "A beach from Japan’s myths, west of Izumo Taisha. On the 10th day of the 10th lunar month, the gods of Japan are said to be welcomed ashore here.",
         "The lone rock on the sand is Bentenjima, with a small torii and shrine on top. The sand has built up over the years, so you can now walk right round behind it.",
         "The beach faces west, so on a clear day it is best towards evening. But trains back run only about once an hour and Izumo Taisha-mae Station is about 25 minutes’ walk away, so pick your train first.",
     ]),
     "note": T("浜は自由に歩けます。海水浴場としては2022年から開かれていません。出雲市駅からのバス（日御碕線「稲佐の浜入口」）は1日4本だけなので、出雲大社から歩くのが確実です。2026年11月21日に出雲観光協会の公式サイトで確認。",
               "The beach is open to walk at any time; it has not opened as a swimming beach since 2022. Buses from Izumoshi Station (Hinomisaki line, “Inasa-no-hama Iriguchi”) run only four times a day, so walking from the shrine is the sure way. Checked on the Izumo Tourism Association website on 21 Nov 2026."),
     "web": [W("弁天島", "Bentenjima", "Kuruman from Tokyo, Japan", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Bentenjima_(15253233125).jpg"),
             W("砂浜と弁天島", "The beach and Bentenjima", "Qurren", "CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:Bentenjima_on_Inasa_Beach.jpg"),
             W("夕方の稲佐の浜", "Inasa Beach towards evening", "mstk east", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Inasa_coast_and_a_distant_view_of_Mt._Sanbe_Dec_20,_2015.jpg"),
             W("夕日に染まる弁天島", "Bentenjima in the evening light", "Raita Futo from Tokyo, Japan", "CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Bentenjima_(51820613402).jpg")]},
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
        s["photos"] = photos(s["id"], s.pop("caps", []), s.pop("web", []))

G = {"intro": intro, "outro": outro, "plans": plans, "city": city, "food": food, "trips": trips, "refs": [],
     "region": json.load(open(f"{R}/scripts/matsue_region.json", encoding="utf-8")),
     "sources": {"checked": "2026-11-21", "list": [
         "https://www.matsue-castle.jp/userguide/index",
         "https://www.city.matsue.lg.jp/kanko_bunka_sports/rekishi_bunkazai/21766.html",
         "https://www.matsue-castle.jp/kounkaku/",
         "https://www.matsue-horikawameguri.jp/price/",
         "https://www.matsue-bukeyashiki.jp/",
         "https://www.hearn-museum-matsue.jp/userguide.html",
         "https://www.adachi-museum.or.jp/hours-admission",
         "https://www.adachi-museum.or.jp/shuttle-bus/",
         "https://izumooyashiro.or.jp/archives/news/12552",
         "https://izumooyashiro.or.jp/precinct/keidai-index/kaguraden",
         "https://www.izumo-kankou.gr.jp/676",
         "https://www.izumo-kankou.gr.jp/213",
         "https://railway.ichibata.co.jp/tichet/free/",
         "https://www.shimane-art-museum.jp/visit/",
         "https://www.shimane-art-museum.jp/visit/access.html",
         "https://www.kankou-matsue.jp/omoshiro/sunset/264",
         "https://www.kankou-matsue.jp/omoshiro/sunset/266",
         "https://transit.yahoo.co.jp/"]}}
js = "/* Generated by scripts/build_matsue_data.py: spots, text (EN/JA), plans, photos and map data for the Matsue, Adachi Museum & Izumo Taisha guide. */\nwindow.GUIDE = " + json.dumps(G, ensure_ascii=False, indent=1) + ";\n"
os.makedirs(f"{SITE}/js", exist_ok=True)
open(f"{SITE}/js/data.js", "w", encoding="utf-8").write(js)
print("ok", len(city), len(food), len([t for t in trips if t.get("kind") != "group"]))
