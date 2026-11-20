#!/usr/bin/env python3
"""京都 高雄の紅葉（神護寺・西明寺・高山寺）のデータ（data/routes/takao.json）を書き出す。

使い方: python3 scripts/build_takao_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/takao/<スポットのid>-<番号>.jpg を番号の順に全部使う
- ネットから借りた写真（Wikimedia Commons）は、スポットの _extra に {"file", "credit": {"author", "license", "page"}} で書く。
  ページでは写真の上に撮影者とライセンスが出る（高山寺。オーナーは行っていないので、文章にも行った日などは書かない）
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/takao"
OUT = f"{R}/data/routes/takao.json"
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


def photos(pid, extra=None):
    """自分の写真（番号の順）のあとに、クレジットつきの写真（extra）を並べる。extra にあるファイルは二重に入れない。"""
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


JRBUS = link("timetable", "JRバス 高雄・京北線", "JR Bus Takao–Keihoku line (Japanese)", "https://www.nishinihonjrbus.co.jp/route/kyoto/")
MOMIJI = "https://ja.kyoto.travel/flower/momiji/"
SEASON = {"from": None, "to": None, "url": MOMIJI,
          "head": T("紅葉の見ごろは例年11月上旬〜下旬", "Autumn leaves: usually early to late November"),
          "text": T("京都観光Navi（京都市）の紅葉だよりでは、例年の見ごろは神護寺が11月上旬〜下旬、西明寺が11月10日前後、高山寺が11月中旬〜下旬です。年によって前後するので、行く前に紅葉だよりを見てください。",
                    "Kyoto City’s autumn-leaf report gives the usual peak as early to late November at Jingoji, around 10 November at Saimyoji, and mid to late November at Kosanji. It shifts from year to year, so check the report before you go.")}
S = [
    dict(id="kiyotaki", name=T("高雄橋と清滝川", "Takao bridge & Kiyotaki river"), kind=T("渓谷", "Gorge"),
         blurb=T("バスを降りて谷へ下りると、朱の高雄橋と清滝川。川沿いの茶屋を過ぎて、神護寺への石段へ。",
                 "Down from the bus stop into the valley: the vermilion Takao bridge over the Kiyotaki, teahouses by the river, and the steps up to Jingoji."),
         lat=35.05542, lng=135.67303,
         text=T("高雄橋（たかおばし）と清滝川（きよたきがわ）\n\n京都駅前からJRバス高雄・京北線で「高雄」へ（約55分・230円）。8:30発に乗ると9:24に着きます。四条烏丸からは市バス8系統（約50分・230円、1時間に1本）。\n\n"
                "バス停から坂道を谷へ下りると、清滝川にかかる朱色の高雄橋。紅葉の時期は、谷じゅうがもみじに染まります。橋を渡ると、川沿いの茶屋の先から神護寺への長い石段が始まります。\n\n"
                "神護寺は受付が16:00までなので、先に神護寺へ上りましょう。お昼は、高雄橋のそばや神護寺の参道の茶屋で（写真の硯石亭のような茶屋があります。営業の日と時間は要確認）。\n\n"
                "紅葉の時期の週末はバスが混むので、朝の早い便がおすすめです。JRバスは、混む日に臨時便を出すことがあります。\n\nおすすめ訪問時間：9:35〜9:50",
                "Takao bridge and the Kiyotaki river\n\nFrom Kyoto Station take the JR Bus Takao–Keihoku line to “Takao” (about 55 min, ¥230); the 8:30 arrives at 9:24. From Shijo-Karasuma, city bus 8 takes about 50 minutes (¥230, hourly).\n\n"
                "Walk down from the stop into the valley to the vermilion Takao bridge over the Kiyotaki. In autumn the whole gorge turns red with maples. Across the bridge, past the riverside teahouses, the long stone stairway to Jingoji begins.\n\n"
                "Jingoji’s last entry is 16:00, so go up there first. For lunch, try the teahouses by the bridge or on the way up to Jingoji (like Suzuri-ishi-tei in the photo; opening days and hours: please check).\n\n"
                "Buses get crowded at autumn weekends, so take an early one. JR Bus sometimes adds extra buses on busy days.\n\nRecommended visit time: 9:35–9:50"),
         gmaps=[gm("高雄橋", "Takao bridge", 35.05542, 135.67303, "高雄橋 京都 右京区")],
         links=[JRBUS, link("info", "紅葉だより（京都観光Navi）", "Autumn-leaf report (Kyoto City, Japanese)", MOMIJI)],
         notices=[SEASON],
         info=info([row("train", "京都駅前8:30発（JRバス）→ 高雄9:24着・230円（朝は8:00・8:30・9:00・9:30・10:00発）", "Kyoto Station 8:30 (JR Bus) → Takao 9:24, ¥230 (morning buses at 8:00, 8:30, 9:00, 9:30, 10:00)"),
                    row("fee", "京都駅前〜栂ノ尾は230円均一。地下鉄・バス一日券（1,100円）も使えます", "Flat ¥230 between Kyoto Station and Toganoo; the Subway & Bus 1-day Pass (¥1,100) is valid"),
                    row("hours", "高雄バス停から神護寺まで歩いて約20分（石段の上りを含む。神護寺の案内）", "About 20 min on foot from the Takao stop to Jingoji, including the stone stairs (temple’s access page)")],
                   tip=T("JRバスの公式サイトの時刻表（2026年4月1日改正）と運賃表で確認しました。", "Checked on the JR Bus timetable (revised 1 April 2026) and fare table."))),
    dict(id="jingoji", name=T("神護寺", "Jingoji"), kind=T("寺", "Temple"),
         blurb=T("長い石段を上った山の上のお寺。楼門をくぐると、広い境内がもみじで赤くなります。",
                 "A mountaintop temple at the top of a long stone stairway; through the gate, the wide precinct turns red with maples."),
         lat=35.05467, lng=135.67131,
         text=T("神護寺（じんごじ）\n\n平安時代のはじめに開かれ、空海（弘法大師）もいたことのある、高雄山の中腹のお寺です。高雄橋から、もみじに囲まれた長い石段をゆっくり上って約20分（神護寺の案内では、高雄バス停から歩いて約20分）。上りきると、楼門の先に広い境内が開けます。"
                "石段の上の金堂、毘沙門堂、五大堂のまわりは、紅葉の時期は一面の赤。\n\n"
                "石段が長いので、歩きやすい靴で行きましょう。金堂の前の石段を上りきって振り返ると、五大堂と毘沙門堂の屋根ごしにもみじが見下ろせます（写真5枚目）。\n\n"
                "境内の西の端からは、谷に向かって素焼きのお皿を投げる「かわらけ投げ」ができます。\n\nおすすめ訪問時間：10:10〜11:15",
                "Jingoji\n\nFounded in the early Heian period, and once home to Kukai (Kobo Daishi), this temple sits high on Mt. Takao. From the Takao bridge it’s about 20 minutes at an easy pace up the long, maple-lined stairs (the temple gives about 20 minutes from the Takao bus stop). At the top, beyond the gate, the broad precinct opens out. "
                "Around the main hall at the top of the steps, the Bishamon hall and the Godai hall, everything turns red in autumn.\n\n"
                "The stairs are long, so wear comfortable shoes. Climb the steps in front of the main hall and turn round: you look down on the maples over the roofs of the Godai and Bishamon halls (photo 5).\n\n"
                "At the western edge of the grounds you can throw little clay discs into the valley (“kawarake-nage”).\n\nRecommended visit time: 10:10–11:15"),
         gmaps=[gm("神護寺", "Jingoji", 35.05467, 135.67131, "神護寺 高雄")],
         links=[link("official", "神護寺 公式サイト", "Jingoji (official, Japanese)", "http://jingoji.or.jp/")],
         info=info([row("hours", "9:00〜16:00", "9:00–16:00"), row("closed", "年中無休", "Open every day"),
                    row("fee", "中学生以上1,000円、小学生500円（2024年7月から）", "¥1,000 (junior high and up), ¥500 elementary (from July 2024)")],
                   tip=T("神護寺の公式サイトで確認しました。", "Checked on the temple website."))),
    dict(id="saimyoji", name=T("西明寺（槇尾）", "Saimyoji (Makinoo)"), kind=T("寺", "Temple"),
         blurb=T("清滝川にかかる朱の指月橋を渡って、小さな山寺へ。表門ごしに見る本堂と、庭のもみじ。",
                 "Cross the vermilion Shigetsu bridge over the Kiyotaki to a small mountain temple: the main hall seen through the front gate, and maples in the garden."),
         lat=35.05632, lng=135.67505,
         text=T("西明寺（さいみょうじ）\n\n神護寺の山門から石段を下り、清滝川沿いの道を歩いて約20分。朱色の指月橋（しげつきょう）を渡ると、表門の先に本堂と客殿があります。\n\n"
                "写真を撮るなら、川のそばから指月橋を見上げる場所（写真1枚目）と、表門ごしに本堂が見える場所（2枚目）。京都観光Naviの紅葉だよりでは、西明寺の見ごろは例年11月10日前後です。\n\n"
                "茶屋でお昼にした日は、ここからの時間を40分ほど後ろにずらしてください。\n\n"
                "ここで帰るなら、歩いて約5分の「槇ノ尾」バス停からJRバスで京都駅へ（約55分・230円）。高山寺へは、国道162号を北へ歩いて約15分です。\n\nおすすめ訪問時間：11:35〜12:20",
                "Saimyoji\n\nDown the steps from Jingoji’s gate and about 20 minutes along the riverside path. Cross the vermilion Shigetsu bridge; beyond the front gate are the main hall and guest hall.\n\n"
                "Two good photo spots: looking up at the Shigetsu bridge from beside the river (photo 1), and the main hall framed by the front gate (photo 2). Kyoto City’s autumn-leaf report gives Saimyoji’s usual peak as around 10 November.\n\n"
                "If you stopped at a teahouse for lunch, push the times from here back by about 40 minutes.\n\n"
                "To go home from here, the “Makinoo” stop is about 5 minutes’ walk: JR Bus to Kyoto Station (about 55 min, ¥230). For Kosanji, walk north along Route 162 for about 15 minutes.\n\nRecommended visit time: 11:35–12:20"),
         gmaps=[gm("西明寺", "Saimyoji", 35.05632, 135.67505, "西明寺 槇尾")],
         links=[link("official", "西明寺 公式サイト", "Saimyoji (official, Japanese)", "https://www.saimyoji.or.jp/"), JRBUS],
         info=info([row("hours", "9:00〜17:00（受付は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                    row("fee", "拝観料は公式サイトに文字で書かれていません（要確認）", "Admission isn’t given as text on the official website (please check)"),
                    row("train", "槇ノ尾 → 京都駅前 JRバス 約55分・230円。11〜15時台は毎時15分・35分発", "Makinoo → Kyoto Station, JR Bus about 55 min, ¥230; at :15 and :35 past each hour from 11:00 to 15:59")],
                   tip=T("西明寺の公式サイトと、JRバスの時刻表（2026年4月1日改正）で確認しました。", "Checked on the temple website and the JR Bus timetable (revised 1 April 2026)."))),
    dict(id="kosanji", name=T("高山寺（栂尾）", "Kosanji (Toganoo)"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
         blurb=T("「鳥獣人物戯画」が伝わる、世界遺産の山寺。国宝の石水院の縁側から、川の向こうの山を眺めます。",
                 "A World Heritage mountain temple, home of the Choju-jinbutsu-giga scrolls. From the veranda of Sekisuiin, a National Treasure, you look out to the hill across the river."),
         lat=35.06012, lng=135.67855,
         text=T("高山寺（こうさんじ）\n\n西明寺から国道162号を北へ歩いて約15分（約800m）。栂尾（とがのお）の山の斜面にあるお寺で、1206年に明恵上人（みょうえしょうにん）が再興しました。1994年に世界遺産に登録されています。\n\n"
                "いちばんの見どころは、国宝の石水院（せきすいいん）。明恵上人の時代から残る、ただひとつの建物です。南の縁側は、清滝川の向こうの山に向かって開けています。公式サイトのすすめは、縁から一歩下がって畳に座ること。柱と蔀戸（しとみど）が額縁になって、景色が切り取られて見えます。\n\n"
                "うさぎやかえるが遊ぶ国宝の絵巻「鳥獣人物戯画（ちょうじゅうじんぶつぎが）」が伝わるお寺でもあります。境内には「日本最古之茶園」の碑が立つ茶園があり、栄西禅師が宋から持ち帰った茶の実を、明恵上人がここで育てたと伝わります。\n\n"
                "石水院は1,000円。秋は、ほかに入山料500円がかかります（入山料の期間は公式サイトに書かれていません。要確認）。\n\n"
                "帰りは「栂ノ尾」バス停からJRバスで京都駅へ（13:34発→京都駅前14:31着・230円）。栂ノ尾が始発の便が多く、槇ノ尾や高雄より先に乗れます。\n\nおすすめ訪問時間：12:35〜13:25",
                "Kosanji\n\nAbout 15 minutes’ walk (about 800 m) north along Route 162 from Saimyoji. The temple stands on the hillside at Toganoo; the priest Myoe revived it in 1206. It was registered as a World Heritage site in 1994.\n\n"
                "The highlight is Sekisuiin, a National Treasure and the only building left from Myoe’s time. Its south veranda opens towards the hill across the Kiyotaki river. The temple’s own advice: sit on the tatami a step back from the veranda, and the pillars and lattice shutters frame the view like a picture.\n\n"
                "This is also the temple of the Choju-jinbutsu-giga, the National Treasure scrolls of frolicking rabbits and frogs. In the grounds is a tea garden marked with a stone reading “Japan’s oldest tea garden”: the Zen master Eisai brought tea seeds from Song China, and Myoe is said to have grown them here.\n\n"
                "Sekisuiin costs ¥1,000. In autumn there is also a ¥500 entry fee for the grounds (the website doesn’t give the dates; please check).\n\n"
                "Go home by JR Bus from the “Toganoo” stop to Kyoto Station (13:34 → Kyoto Station 14:31, ¥230). Many buses start at Toganoo, so you board before the Makinoo and Takao stops.\n\nRecommended visit time: 12:35–13:25"),
         gmaps=[gm("高山寺", "Kosanji", 35.06012, 135.67855, "高山寺 栂尾 京都"), gm("栂ノ尾バス停", "Toganoo bus stop", 35.05991, 135.67898, "栂ノ尾 バス停 京都")],
         links=[link("official", "高山寺 公式サイト", "Kosanji (official, Japanese)", "https://kosanji.com/"), JRBUS],
         info=info([row("hours", "8:30〜17:00", "8:30–17:00"),
                    row("fee", "石水院 一般1,000円、小学生500円。秋は別に入山料500円（期間は要確認）", "Sekisuiin ¥1,000, elementary ¥500. In autumn, a separate ¥500 entry fee for the grounds (dates: please check)"),
                    row("train", "栂ノ尾 → 京都駅前 JRバス 約57分・230円。11〜15時台は毎時14分・34分発（13:34発→14:31着）。16時からは16:14・17:14・17:59発…と少なくなります",
                        "Toganoo → Kyoto Station, JR Bus about 57 min, ¥230; at :14 and :34 past each hour from 11:00 to 15:59 (13:34 → 14:31). Fewer from 16:00: 16:14, 17:14, 17:59…")],
                   tip=T("高山寺の公式サイトと、JRバスの時刻表（2026年4月1日改正）で確認しました。西明寺からの距離は OpenStreetMap で測った目安です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the temple website and the JR Bus timetable (revised 1 April 2026). The distance from Saimyoji is an estimate measured on OpenStreetMap. Photos are from Wikimedia Commons (author and license shown on each photo).")),
         _extra=[
             cc("kosanji-1.jpg", "663highland", "CC BY 2.5", "Sekisuiin Kozanji Kyoto Kyoto06s5s4350.jpg"),
             cc("kosanji-2.jpg", "KimonBerlin", "CC BY-SA 2.0", "Kozan-ji (7069446619).jpg"),
             cc("kosanji-3.jpg", "PlusMinus", "CC BY-SA 3.0", "Kouzanji sandou.jpg"),
             cc("kosanji-4.jpg", "KimonBerlin", "CC BY-SA 2.0", "Kozan-ji (7069445443).jpg"),
         ]),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    extra = s.pop("_extra", None)
    out.update(s)
    out["photos"] = photos(out["id"], extra)
    out.setdefault("notices", [])
    spots.append(out)
NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}

data = {
    "id": "takao",
    "_note": "京都 高雄の紅葉ルート（takao/ のページ専用。形は eizan-line.json と同じ）。JRバスで高雄へ、高雄橋・清滝川→神護寺→（清滝川沿い）西明寺→（国道162号）高山寺→栂ノ尾からJRバス。"
             "写真は Toshi の写真ライブラリから選んだもの（2024年11月19日の Nikon D7000 と iPhone。実際は西明寺→神護寺の順に歩いたが、神護寺の受付が16:00までなので神護寺を先にした。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "高山寺はオーナーが行っていない場所で、写真は Wikimedia Commons（photos の要素が {file, credit}。ライセンスは Commons の API で2026年11月21日に確認）。"
             "info.checked は事実情報を確認した日（各寺の公式サイト、JRバスの時刻表と運賃表、京都観光Naviの紅葉だより）。このファイルは scripts/build_takao_data.py で作る。",
    "sections": [{"first": 1, "last": 2, "day": 0}, {"first": 3, "last": 3, "day": 1}, {"first": 4, "last": 4, "day": 2}],
    "plan": {"_note": "「選んで回る」の設定。全部選べる。", "picks": [s["no"] for s in spots], "auto": {}, "hints": [
        H("jingoji", {"any": [NO["jingoji"], NO["kiyotaki"]], "none": [NO["saimyoji"], NO["kosanji"]]},
          "神護寺だけで帰る日は、「高雄」バス停からJRバスで京都駅へ（約55分・230円、11〜15時台は毎時16分・36分発）。",
          "Going home after Jingoji? Take the JR Bus from the “Takao” stop to Kyoto Station (about 55 min, ¥230; at :16 and :36 past each hour from 11:00 to 15:59)."),
        H("saimyoji", {"any": [NO["saimyoji"]], "none": [NO["kosanji"]]},
          "高山寺に寄らない日は、「槇ノ尾」バス停からJRバスで京都駅へ（約55分・230円、11〜15時台は毎時15分・35分発）。",
          "Skipping Kosanji? Take the JR Bus from the “Makinoo” stop to Kyoto Station (about 55 min, ¥230; at :15 and :35 past each hour from 11:00 to 15:59)."),
        H("kosanji", {"any": [NO["kosanji"]], "none": [NO["saimyoji"]]},
          "西明寺に寄らない日は、高雄橋から国道162号へ上がり、北へ歩いて約20分（約1km）。JRバスなら「高雄」から「栂ノ尾」まで2分です。",
          "Skipping Saimyoji? From the Takao bridge go up to Route 162 and walk north for about 20 minutes (about 1 km), or ride the JR Bus two minutes from “Takao” to “Toganoo”."),
        H("kosanji", {"any": [NO["kosanji"]], "none": [NO["kiyotaki"], NO["jingoji"], NO["saimyoji"]]},
          "高山寺だけに行く日は、京都駅前からJRバスで終点の「栂ノ尾」へ（約55分・230円）。「周山」行きに乗っても栂ノ尾で降りられます。",
          "Going to Kosanji only? Take the JR Bus from Kyoto Station to “Toganoo” (about 55 min, ¥230); buses bound for Shuzan stop there too."),
    ]},
    "photoBase": "../images/takao/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
