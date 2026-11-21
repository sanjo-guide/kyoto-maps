#!/usr/bin/env python3
"""白馬ガイド（hakuba/）の js/data.js を作る（tango-tajima/ と同じ形。モデルプランつき）。

使い方: python3 scripts/build_hakuba_data.py
- 文章・料金・時間・モデルプランはこのファイルの中。直したらこのスクリプトを実行し直す（data.js を直接直さない）
- 写真は hakuba/img/<id>-<番号>.jpg。キャプションの数と写真の数が合わないと止まる
- 行っていない場所（大出公園・栂池自然園）は Wikimedia Commons の写真 hakuba/img/web-<id>-<番号>.jpg を使う。
  スポットの "web" に W(キャプション日, 英, 撮影者, ライセンス, ファイルページ) を並べる（自分の写真のあとに付く。クレジットはページに自動で出る）
- 写真は2026年6月9〜11日に Toshi が撮ったもの（iPhone と Nikon D7000。長辺1280px・位置情報なし・横向きだけ）
- 簡易地図の輪郭は scripts/hakuba_region.json
"""
import json, os, struct, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = f"{R}/hakuba"
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
    "北アルプスのふもと、長野県の白馬村（はくばむら）のおすすめをまとめました。",
    "京都からは電車を乗り継いで約4時間半〜5時間。日帰りは難しいので、1泊か2泊して、山の上の景色と高原の空気をゆっくり楽しむのがおすすめです。",
    "私の写真は2026年6月、まだ雪が残る初夏の白馬です。夏のゴンドラやリフトは、毎年だいたい5月〜6月から11月の初めまで動きます（年によってちがいます）。",
    "山の天気は変わりやすいので、晴れた日に山の上へ。いちばん大事なのは、予定を詰め込みすぎないことです。",
], [
    "Here are my picks for Hakuba, a village at the foot of the Northern Alps in Nagano.",
    "From Kyoto it takes about 4½ to 5 hours by train, so a day trip is hard. Stay one or two nights and take your time with the mountain views and the highland air.",
    "My own photos are from June 2026, early summer with snow still on the peaks. The summer gondolas and lifts usually run from May or June until early November (dates change every year).",
    "Mountain weather changes fast, so save a clear day for going up high. Above all, don’t overpack your schedule.",
])
outro = T([
    "以上が、私の白馬のおすすめです。",
    "雪の残る山を正面に見ながら歩く八方尾根と、テラスでのんびりできる岩岳。どちらも、ゴンドラで上がるだけで別世界です。",
    "山の上は夏でも冷えます。上着と雨具を持って、無理せず、自分らしい旅を楽しんでください。",
], [
    "That’s my list of picks for Hakuba.",
    "The Happo-one ridge, walking towards snowy peaks, and Iwatake, where you can relax on a terrace: both are another world, just a gondola ride up.",
    "It gets cold up high even in summer. Bring a jacket and rain gear, don’t push yourself, and enjoy the trip your own way.",
])

ROUTE_NOTE = T("乗り換えの時刻は日によってちがいます。出かける前に乗換案内で確認してください。", "Connections vary by day, so check a route planner before you go.")

plans = [
    {"id": "plan-1", "title": T("1泊2日", "1 night, 2 days"),
     "sub": T("岩岳と八方池を1日ずつ", "Iwatake one day, Happo Pond the next"),
     "days": [
         {"label": T("1日目", "Day 1"),
          "text": T("京都から新幹線で名古屋へ行き、特急しなので塩尻・松本へ。乗り換えて白馬へ（京都7:12発→白馬11:40着の例で約4時間半、12,750円）。午後は岩岳へ（白馬駅からタクシーで。特急バスは本数が少ないので時刻を確認）。ゴンドラで山頂のHAKUBA MOUNTAIN HARBORへ。白馬に泊まります。",
                    "Shinkansen from Kyoto to Nagoya, the Shinano limited express towards Shiojiri / Matsumoto, then on to Hakuba (e.g. Kyoto 7:12 → Hakuba 11:40, about 4½ hours, ¥12,750). In the afternoon head to Iwatake (by taxi from the station; the express buses are few, so check the times) and ride the gondola up to HAKUBA MOUNTAIN HARBOR. Stay in Hakuba.")},
         {"label": T("2日目", "Day 2"),
          "text": T("朝のうちに八方のゴンドラとリフトで八方池山荘へ。八方池まで歩いて往復約2時間半。お昼すぎに下りて、白馬駅から京都へ（白馬17:10発→松本で乗り換え→京都22:09着の例で12,670円）。",
                    "Early in the morning, ride the Happo gondola and lifts to Happo-ike Sanso and hike to Happo Pond and back (about 2½ hours). Come down after lunch and head home from Hakuba Station (e.g. Hakuba 17:10 → change at Matsumoto → Kyoto 22:09, ¥12,670).")}],
     "note": ROUTE_NOTE},
    {"id": "plan-2", "title": T("2泊3日", "2 nights, 3 days"),
     "sub": T("私が回った順番に、朝の大出公園を足しました", "The way I did it, plus a morning walk to Oide Park"),
     "days": [
         {"label": T("1日目", "Day 1"),
          "text": T("京都を出て、夕方に白馬へ。駅のまわりのお店で、次の日の飲みものや軽食を買っておくと安心です。",
                    "Leave Kyoto and reach Hakuba in the evening. Pick up drinks and snacks for the next day from the shops near the station.")},
         {"label": T("2日目", "Day 2"),
          "text": T("晴れていたら、朝のうちに駅の東の大出公園へ（歩いて約15分）。そのあとスノーピーク ランドステーション白馬と、田んぼの道を散歩。午後は岩岳へ行き、ゴンドラで山頂のテラスへ。",
                    "If it’s clear, start with Oide Park east of the station (about 15 min on foot). Then Snow Peak Land Station Hakuba and a walk through the rice fields. In the afternoon, go to Iwatake and take the gondola up to the summit terrace.")},
         {"label": T("3日目", "Day 3"),
          "text": T("晴れていたら朝から八方尾根へ。八方池まで歩いて、山の上でお昼。午後に白馬駅へ戻って、電車で京都へ。岩の道より花と湿原を歩きたい人は、八方尾根のかわりに栂池自然園もいい選択です（白馬駅前9:22発のバスで栂池高原へ。帰りのバスは本数が少ないので先に確認）。",
                    "If it’s clear, go up Happo-one in the morning, hike to Happo Pond and have lunch on the mountain. Back to Hakuba Station in the afternoon and take the train home. If you prefer flowers and marshland to a rocky trail, Tsugaike Nature Park is a good alternative to Happo-one (take the 9:22 bus from Hakuba Station to Tsugaike Kogen; buses back are few, so check them first).")}],
     "note": ROUTE_NOTE},
]

city = [
    {"id": "station", "lat": 36.69600, "lon": 137.86380, "ja": "白馬駅", "en": "Hakuba Station",
     "short": T("白馬駅", "Hakuba Sta."), "map": gmap("白馬駅"),
     "time": T("京都から約4時間半〜5時間。名古屋・松本経由（約12,750円）か、敦賀・長野経由で長野からバス（約18,380円）", "About 4½ to 5 hours from Kyoto: via Nagoya and Matsumoto (about ¥12,750), or via Tsuruga and Nagano, then the bus from Nagano (about ¥18,380)"),
     "body": T([
         "JR大糸線（おおいとせん）の駅で、白馬の町の入り口です。山小屋のような駅舎で、ホームからは北アルプスの山が見えます。",
         "八方（はっぽう）のバスターミナルまでは、駅前からバスで約8分（180円）。長野駅から来る特急バスも、白馬駅前と八方に止まります。",
     ], [
         "A station on the JR Oito Line and the gateway to Hakuba. The station building looks like a mountain lodge, and you can see the Northern Alps from the platform.",
         "The Happo bus terminal is about 8 minutes by bus from the station (¥180). The express bus from Nagano stops at both Hakuba Station and Happo.",
     ]),
     "note": T("長野駅東口〜白馬駅前・白馬八方の特急バスは2,900円（夏）、予約なしで乗れます（2026年4月1日〜12月11日のダイヤ）。2026年11月20日にアルピコ交通の公式サイトで確認。電車の時間と運賃は乗換案内で確認（2026年11月の平日・土曜）。",
               "Express bus from Nagano Station (east exit) to Hakuba Station / Hakuba Happo: ¥2,900 in summer, no booking needed (timetable from 1 Apr to 11 Dec 2026). Checked on Alpico’s website on 20 Nov 2026. Train times and fares checked on a route planner (weekday and Saturday, Nov 2026)."),
     "caps": [("山小屋のような白馬駅", "Hakuba Station, built like a mountain lodge"),
              ("駅の「ようこそ白馬へ」の幕", "The “Welcome to Hakuba” banner at the station"),
              ("白馬駅のホーム", "The platform at Hakuba Station"),
              ("白馬駅の駅名標", "The Hakuba station sign")]},
    {"id": "snowpeak", "lat": 36.69760, "lon": 137.85675, "ja": "スノーピーク ランドステーション白馬", "en": "Snow Peak Land Station Hakuba",
     "short": T("スノーピーク", "Snow Peak"), "map": gmap("スノーピーク ランドステーション白馬"),
     "time": T("白馬駅から歩いて10分ほど（約700m）", "About 10 min on foot from Hakuba Station (about 700 m)"),
     "body": T([
         "アウトドア用品のスノーピークのお店に、レストランとスターバックス、白馬村観光局のインフォメーションが入った施設です。木を組んだ大きな建物が目印です。",
         "大きな窓の向こうに白馬の山が見えて、コーヒーを飲みながらのんびりできます。まわりの芝生や田んぼの道も、散歩にぴったりです。",
     ], [
         "A Snow Peak outdoor-gear store with a restaurant, a Starbucks and the Hakuba Village tourist information centre, in a striking building of interlocking timber.",
         "The mountains fill the huge windows, so it’s a lovely place to linger over a coffee. The lawns and the paths through the rice fields around it are perfect for a stroll.",
     ]),
     "note": T("年中無休。お店11:00〜19:00、スターバックス7:00〜19:00、雪峰食堂11:30〜15:00・17:00〜20:00（火曜休み）、観光局インフォメーション9:00〜17:00。2026年11月20日に公式サイトで確認。",
               "Open every day. Store 11:00–19:00, Starbucks 7:00–19:00, Seppo Shokudo restaurant 11:30–15:00 and 17:00–20:00 (closed Tuesdays), tourist information 9:00–17:00. Checked on the official website on 20 Nov 2026."),
     "caps": [("木を組んだ建物", "The interlocking timber structure"),
              ("スノーピークの建物", "The Snow Peak building"),
              ("木組みと黒い外壁", "Timber lattice and dark walls"),
              ("窓から見る白馬の山", "The mountains from the window")]},
    {"id": "fields", "lat": 36.69830, "lon": 137.85700, "ja": "田んぼと北アルプスの景色", "en": "Rice fields and the Northern Alps",
     "short": T("田んぼの道", "Rice fields"), "map": gmap("スノーピーク ランドステーション白馬"),
     "time": T("スノーピーク ランドステーション白馬のすぐ北", "Just north of Snow Peak Land Station Hakuba"),
     "body": T([
         "白馬駅のまわりには田んぼが広がっていて、その向こうに雪の残る北アルプスが並びます。",
         "6月は田植えのあとで、水をはった田んぼに山や雲が映ります。駅に戻る前に、少し遠回りして歩いてみてください。",
     ], [
         "Rice fields spread out around Hakuba Station, with the snow-streaked Northern Alps lined up beyond them.",
         "In June, just after planting, the flooded paddies mirror the mountains and clouds. Take a slight detour on foot before heading back to the station.",
     ]),
     "caps": [("田んぼの向こうの北アルプス", "The Northern Alps beyond the paddies"),
              ("水をはった田んぼ", "Flooded rice fields"),
              ("田んぼに映る空", "The sky mirrored in a paddy"),
              ("田んぼと雲のかかる山並み", "Paddies and clouds over the ridges")]},

    {"id": "oide", "lat": 36.69696, "lon": 137.87301, "ja": "大出公園（おおいでこうえん）", "en": "Oide Park",
     "short": T("大出公園", "Oide Park"), "map": gmap("大出公園 白馬村"),
     "time": T("白馬駅から東へ歩いて約15分（約1.2km）", "About 15 min on foot east of Hakuba Station (about 1.2 km)"),
     "body": T([
         "姫川（ひめかわ）にかかる吊橋と、茅葺き屋根の家、その向こうに白馬三山。白馬のポスターでよく見る景色は、この公園です。",
         "山は西にあるので、日が当たる朝から午前がいちばんきれいです。午後は逆光になります。公園の展望台に上がると、川と茅葺きの家と山が1枚に入ります。",
         "桜は4月下旬〜5月上旬、紅葉は10月中旬〜下旬。桜のころはとても混むので、長くとどまらず、ゆずり合って見てください。",
     ], [
         "A suspension bridge over the Himekawa river, thatched houses, and the three Hakuba peaks behind them: the view you see on Hakuba posters is from this park.",
         "The mountains are to the west, so they are lit from early to late morning; in the afternoon you face into the sun. Climb to the park’s viewpoint, where the river, the houses and the peaks fit in one frame.",
         "Cherry blossom is late April to early May, autumn colour mid to late October. It gets very crowded at blossom time, so don’t linger and give others a turn.",
     ]),
     "note": T("公園は自由に歩けます。展望台や園内で、三脚を立てて長く撮影するのは控えてください。桜の時期は駐車場や通れる道の規制があります（2026年は4月11日〜5月6日のうち数日）。2026年11月21日に白馬村観光局の公式サイトで確認。駅からの距離は乗換案内。",
               "The park is open to walk at any time. Please don’t set up a tripod for long at the viewpoint or in the park. At blossom time there are parking and access restrictions (several days between 11 April and 6 May in 2026). Checked on the Hakuba Village tourism website on 21 Nov 2026; walking distance from a route planner."),
     "web": [W("桜と茅葺きの家と白馬三山", "Cherry blossom, thatched houses and the Hakuba peaks", "くろふね", "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:大出公園の桜03.jpg"),
             W("新緑の吊橋と白馬三山", "The bridge and the peaks in fresh green", "くろふね", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:大出の吊橋と白馬三山20240511-IMG_1387.jpg"),
             W("姫川にかかる大出の吊橋", "The Oide suspension bridge over the Himekawa", "くろふね", "CC BY 3.0", "https://commons.wikimedia.org/wiki/File:大出の吊橋_-_panoramio_(1).jpg"),
             W("雪の大出公園", "Oide Park in the snow", "くろふね", "CC BY 3.0", "https://commons.wikimedia.org/wiki/File:大出の吊橋_-_panoramio.jpg")]},
]

food = []

trips = [
    {"kind": "group", "id": "g-happo", "ja": "八方尾根（はっぽうおね）", "en": "Happo-one",
     "time": T("白馬八方バスターミナルから歩いて八方駅へ。ゴンドラとリフト2本で八方池山荘まで約40分（往復 大人3,500円）",
               "Walk from the Hakuba Happo bus terminal to the gondola station. A gondola and two chairlifts take about 40 min to Happo-ike Sanso (¥3,500 return)"),
     "body": T([
         "白馬のスキー場として知られる八方尾根は、夏は北アルプスの展望台です。ゴンドラ「アダム」とリフトを乗り継いで、標高1,830mの八方池山荘まで上がれます。",
     ], [
         "Famous for skiing, Happo-one becomes a viewpoint over the Northern Alps in summer. The Adam gondola and two chairlifts take you up to Happo-ike Sanso at 1,830 m.",
     ])},
    {"id": "happo", "ja": "八方池（はっぽういけ）", "en": "Happo Pond",
     "pins": [{"lat": 36.69425, "lon": 137.78454, "ja": "八方池", "en": "Happo Pond", "anchor": "end"},
              {"lat": 36.69713, "lon": 137.79887, "ja": "八方池山荘", "en": "Happo-ike Sanso", "anchor": "start", "minor": True}],
     "map": gmap("八方池"),
     "body": T([
         "八方池山荘から尾根の道を歩いて、標高2,060mの八方池へ。晴れた日は、池の向こうに白馬三山（しろうまさんざん）などの雪山が並び、池の水に山が映ります。",
         "道は2つあり、木道が続くゆるやかな道で上り約90分、岩の多い近道なら約60分。帰りは約60分です。途中には石を積んだケルンがいくつも立っています。写真は2026年6月11日。池のまわりにはまだ雪が残っていました。",
     ], [
         "From Happo-ike Sanso, follow the ridge path up to Happo Pond at 2,060 m. On a clear day the snowy peaks, including the Hakuba Sanzan, line up beyond the pond and are reflected in the water.",
         "There are two paths: the gentler one with boardwalks takes about 90 minutes up, the rocky shortcut about 60. Allow about 60 minutes back down. Stone cairns stand along the way. Photos from 11 June 2026, with snow still around the pond.",
     ]),
     "note": T("2026年の夏の運行は5月30・31日と6月6日〜11月3日。ゴンドラはふだん8:00〜16:50（混む日は6:30か7:00から）、八方池山荘からの下りの最終は16:30。歩き始めは13時までに。登山靴か歩きなれた靴、雨具と上着を。登山道から外れず、ペットは連れて入れません。2026年11月20日に公式サイトで確認。",
               "2026 summer operation: 30–31 May and 6 June – 3 November. The gondola usually runs 8:00–16:50 (from 6:30 or 7:00 on busy days); the last ride down from Happo-ike Sanso is at 16:30. Start walking by 13:00. Wear hiking boots or well-worn shoes and bring rain gear and a jacket. Stay on the trail; no pets. Checked on the official website on 20 Nov 2026."),
     "caps": [("八方池と北アルプスの山", "Happo Pond and the Northern Alps"), ("雪の残る八方池", "Happo Pond with snow still around it"),
              ("尾根から見る雪山", "Snowy peaks from the ridge"), ("道の途中のケルン", "A cairn along the trail"), ("池と山並み", "The pond and the ridgeline"),
              ("間近に見える雪山", "Snowy peaks up close"), ("池に映る雲と山", "Clouds and peaks reflected in the pond"), ("尾根の斜面と雪渓", "Ridge slopes and snowfields"),
              ("尾根の道からの眺め", "The view from the ridge path"), ("グラートクワッドの山の上の駅", "The top station of the Grat Quad lift")]},

    {"kind": "group", "id": "g-iwatake", "ja": "白馬岩岳（いわたけ）", "en": "Hakuba Iwatake",
     "time": T("白馬八方バスターミナルから長野行きの特急バスで「白馬岩岳マウンテンリゾート」まで約12分（1日6本ほど。時刻を確認）。ゴンドラで山頂まで約7分",
               "About 12 min from the Hakuba Happo bus terminal on the Nagano express bus to “Hakuba Iwatake Mountain Resort” (about six a day; check the times), then about 7 min by gondola to the top"),
     "body": T([
         "白馬の町の北にある、標高1,289mの岩岳の山頂です。ゴンドラで上がると、白馬三山を正面に見るテラスやカフェ、ブランコ、森の遊び場があります。",
     ], [
         "The 1,289 m summit of Mt. Iwatake, north of Hakuba town. Up the gondola you’ll find a terrace facing the Hakuba Sanzan, cafés, swings and play areas in the woods.",
     ])},
    {"id": "iwatake", "ja": "HAKUBA MOUNTAIN HARBOR", "en": "HAKUBA MOUNTAIN HARBOR",
     "pins": [{"lat": 36.72965, "lon": 137.83820, "ja": "HAKUBA MOUNTAIN HARBOR", "en": "Mountain Harbor", "anchor": "end"},
              {"lat": 36.71383, "lon": 137.87277, "ja": "岩岳のゴンドラ乗り場", "en": "Iwatake gondola", "anchor": "start", "minor": True}],
     "map": gmap("HAKUBA MOUNTAIN HARBOR"),
     "body": T([
         "岩岳の山頂の、白馬三山を正面に見る大きなテラスです。中にはニューヨークのベーカリー「THE CITY BAKERY」があり、パンとコーヒーを持ってテラスで景色を楽しめます。",
         "まわりには芝生の広場やブランコ、森の遊び場もあります。写真は2026年6月10日の午後。雲が流れて、山が見えたり隠れたりしていました。",
     ], [
         "A big terrace on the summit of Iwatake, looking straight at the Hakuba Sanzan. Inside is THE CITY BAKERY from New York: take bread and coffee out to the terrace and enjoy the view.",
         "Around it are lawns, swings and play areas in the woods. Photos from the afternoon of 10 June 2026, with clouds drifting across the peaks.",
     ]),
     "note": T("2026年のグリーンシーズンは4月23日〜11月15日、8:30〜17:00（下りのゴンドラの最終は16:50。時期によってちがいます）。入場料は大人2,900円（ゴンドラの往復つき）。2026年11月20日に公式サイトで確認。",
               "2026 green season: 23 April – 15 November, 8:30–17:00 (last gondola down at 16:50; varies by season). Entry ¥2,900 for adults, including the gondola both ways. Checked on the official website on 20 Nov 2026."),
     "caps": [("テラスの先の白馬三山", "The Hakuba Sanzan beyond the terrace"), ("雲の流れる北アルプス", "Clouds drifting over the Northern Alps"),
              ("山頂から見る雪山", "Snowy peaks from the summit"), ("山に向かって突き出したテラス", "The terrace jutting towards the mountains"), ("テラスと谷の眺め", "The terrace and the valley"),
              ("芝生の広場と白馬の町", "The lawn and Hakuba town below"), ("森の中のテント", "Tents in the woods"), ("山頂の広場からの眺め", "The view from the summit lawn"),
              ("ゴンドラから見る景色", "The view from the gondola")]},

    {"kind": "group", "id": "g-tsugaike", "ja": "栂池高原（つがいけこうげん）", "en": "Tsugaike Kogen",
     "time": T("白馬駅前からアルピコ交通のバス（長野〜白馬線の栂池高原・白馬乗鞍行き）で栂池高原まで約30分（570円）。本数が少ないので、行きも帰りも時刻を確認",
               "About 30 min from Hakuba Station on the Alpico bus (Nagano–Hakuba line, bound for Tsugaike Kogen or Hakuba Norikura) to Tsugaike Kogen (¥570). Buses are few, so check the times both ways"),
     "body": T([
         "白馬村のとなり、小谷村（おたりむら）の高原です。ここからゴンドラ「イヴ」（約20分）とロープウェイ（約5分）を乗り継ぐと、標高約1,900mの栂池自然園に着きます。",
     ], [
         "A highland in Otari, the village next to Hakuba. From here the Eve gondola (about 20 min) and a ropeway (about 5 min) take you up to Tsugaike Nature Park at about 1,900 m.",
     ])},
    {"id": "tsugaike", "ja": "栂池自然園（つがいけしぜんえん）", "en": "Tsugaike Nature Park",
     "pins": [{"lat": 36.77400, "lon": 137.81823, "ja": "栂池自然園", "en": "Tsugaike Nature Park", "anchor": "end", "dy": 14}],
     "map": gmap("栂池自然園"),
     "body": T([
         "標高約1,900mに広がる湿原で、木道を歩いて回ります。八方尾根のような岩の登りがないので、山歩きに慣れていない人でも歩きやすい場所です。",
         "手前の「みずばしょう湿原」と「わたすげ湿原」を回るだけなら1時間〜1時間半。いちばん奥の展望湿原まで行くと、白馬大雪渓と白馬三山が正面に見えますが、一周は約5.5km、3時間半〜4時間かかります。帰りのロープウェイの最終に間に合うよう、奥まで行く日は朝の早いゴンドラで上がってください。",
         "混む日はロープウェイの待ち時間だけで片道1時間ほどかかることがあります。山の上は夏でも冷えるので、上着と雨具を。",
     ], [
         "A highland marsh at about 1,900 m that you walk on boardwalks. There is no rocky climb like on Happo-one, so it is easy going even if you are not used to hiking.",
         "The two nearest marshes (Mizubasho and Watasuge) take 1 to 1½ hours. The far Tenbo marsh faces the Hakuba snow gully and the three Hakuba peaks, but the full loop is about 5.5 km and takes 3½ to 4 hours. If you plan to go all the way, take an early gondola so you make the last ropeway down.",
         "On busy days the ropeway queue alone can take about an hour each way. It is cold up there even in summer, so bring a jacket and rain gear.",
     ]),
     "note": T("2026年の営業は6月6日〜10月25日で終了（2027年の日程は要確認）。ゴンドラとロープウェイの往復＋自然園の入園料は大人4,000円・小児2,200円（入園料だけなら大人320円）。ふだんの日はゴンドラ8:00〜上り最終16:10、ロープウェイ8:30〜下り最終16:40（夏休みや連休は早く始まります）。園内はペット・ドローン・たばこ禁止、木道から外れないこと。2026年11月21日に栂池高原と栂池自然園の公式サイトで確認。バスは乗換案内（2026年11月）。",
               "The 2026 season ran 6 June – 25 October and has ended (2027 dates: please check). Gondola and ropeway return plus park entry: ¥4,000 for adults, ¥2,200 for children (park entry alone ¥320). On ordinary days the gondola runs 8:00 – last ride up 16:10 and the ropeway 8:30 – last ride down 16:40 (earlier starts in summer holidays and on long weekends). No pets, drones or smoking in the park, and stay on the boardwalks. Checked on the Tsugaike Kogen and Tsugaike Nature Park websites on 21 Nov 2026; bus from a route planner (Nov 2026)."),
     "web": [W("秋の湿原と白馬の山", "The marsh in autumn and the Hakuba range", "くろふね", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:栂池自然園20221001-IMG_3700.jpg"),
             W("湿原の木道", "A boardwalk across the marsh", "くろふね", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:栂池自然園20221001-IMG_3606.jpg"),
             W("草紅葉の湿原", "The marsh in autumn colour", "くろふね", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:栂池自然園20221001-IMG_3604.jpg"),
             W("ゴンドラと北アルプス", "The gondola and the Northern Alps", "くろふね", "CC BY 4.0", "https://commons.wikimedia.org/wiki/File:栂池自然園20221001-IMG_3559.jpg")]},
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
     "region": json.load(open(f"{R}/scripts/hakuba_region.json", encoding="utf-8")),
     "sources": {"checked": "2026-11-21", "list": [
         "https://www.happo-one.jp/trekking/alpenline",
         "https://www.happo-one.jp/happo-ike/",
         "https://iwatake-mountain-resort.com/green/",
         "https://iwatake-mountain-resort.com/hmh/",
         "https://www.snowpeak.co.jp/landstation/hakuba/",
         "https://www.alpico.co.jp/traffic/express/nagano_hakuba/",
         "https://www.vill.hakuba.nagano.jp/spots/ooide-park/",
         "https://www.tsugaike.gr.jp/ropeway",
         "https://sizenen.otarimura.com/about/",
         "https://transit.yahoo.co.jp/"]}}
js = "/* Generated by scripts/build_hakuba_data.py: spots, text (EN/JA), plans, photos and map data for the Hakuba guide. */\nwindow.GUIDE = " + json.dumps(G, ensure_ascii=False, indent=1) + ";\n"
os.makedirs(f"{SITE}/js", exist_ok=True)
open(f"{SITE}/js/data.js", "w", encoding="utf-8").write(js)
print("ok", len(city), len(food), len([t for t in trips if t.get("kind") != "group"]))
