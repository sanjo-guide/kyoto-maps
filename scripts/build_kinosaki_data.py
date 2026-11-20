#!/usr/bin/env python3
"""京都から日帰り 城崎温泉（＋竹田城跡）ルートのデータ（data/routes/kinosaki.json）を書き出す。

使い方: python3 scripts/build_kinosaki_data.py
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/kinosaki/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kinosaki"
OUT = f"{R}/data/routes/kinosaki.json"
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


def row(kind, ja, en):
    return {"kind": kind, "text": T(ja, en), "until": None, "from": None}


def info(rows, tip=None, verified=True):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid, extra=None):
    # extra: ネットから借りた写真（{"file", "credit": {"author", "license", "page"}}）。写真の上に撮影者とライセンスが出る
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def cc(file, author, license, title):
    return {"file": file, "credit": {"author": author, "license": license, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


JR = link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/")
SPA = link("official", "城崎温泉観光協会（外湯の案内）", "Visit Kinosaki: the seven onsen", "https://kinosaki-spa.gr.jp/",
           "https://visitkinosaki.com/about-kinosaki/the-7-mystic-onsen/")
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の平日のダイヤ）で確認しました。季節や曜日で変わるので、乗る前に確かめてください。",
              "Times and fares checked on a route planner (weekday timetable, November 2026). They change by season and day, so check before you travel.")
YUMEPA = row("fee", "外湯めぐりの1日券「ゆめぱ」1,500円（どの外湯でも買えます。城崎の宿に泊まる人は宿でもらえることが多い）。1か所だけなら大人800円",
             "“Yumepa” onsen day pass ¥1,500, sold at every bathhouse (guests at Kinosaki inns usually get one at check-in). A single bath is ¥800 for adults")
BATH_TIP = T("外湯はどこもタトゥーOK。男女別です。タオルを持っていきましょう。",
             "Every bathhouse is tattoo-friendly. Baths are separated by gender; bring a towel.")


def bath(hours_ja, hours_en, closed_ja, closed_en, extra=None):
    rows = [row("hours", hours_ja, hours_en), row("closed", closed_ja, closed_en), YUMEPA]
    return info(rows + (extra or []), tip=BATH_TIP)


S = [
    dict(id="kyoto", name=T("京都駅", "Kyoto Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("7:32発の特急きのさき1号で出発。竹田城跡に寄る日は和田山で乗り換えます。",
                 "Leave on the 7:32 Kinosaki No. 1 limited express. If you’re stopping at Takeda Castle, change at Wadayama."),
         lat=34.98535, lng=135.758766,
         text=T("京都駅（きょうとえき）\n\n山陰線（嵯峨野線）のホームから出る特急きのさき1号（7:32発）に乗ります。\n\n"
                "竹田城跡に寄る日は、和田山（わだやま）で降りてJR播但線（ばんたんせん）に乗り換え、竹田に9:36着。"
                "城崎温泉だけの日は、乗り換えなしで城崎温泉に9:52に着きます。\n\n"
                "写真は城崎温泉駅で撮った特急の車両です。\n\nおすすめ出発時間：7:32",
                "Kyoto Station\n\nTake the 7:32 Kinosaki No. 1 limited express from the San’in (Sagano) Line platforms.\n\n"
                "If you’re stopping at Takeda Castle, get off at Wadayama and change to the JR Bantan Line, arriving in Takeda at 9:36. "
                "If you’re going only to Kinosaki, stay on: no change, arriving at Kinosaki Onsen at 9:52.\n\n"
                "The photos of the trains were taken at Kinosaki Onsen Station.\n\nRecommended departure time: 7:32"),
         gmaps=[gm("JR京都駅", "JR Kyoto Station", 34.98535, 135.758766, "JR京都駅")],
         links=[JR],
         info=info([row("train", "特急きのさき1号 京都7:32発 → 城崎温泉9:52着（乗り換えなし）", "Kinosaki No. 1: Kyoto 7:32 → Kinosaki Onsen 9:52 (direct)"),
                    row("train", "竹田へは和田山で播但線に乗り換え、竹田9:36着", "For Takeda, change at Wadayama to the Bantan Line, arriving 9:36"),
                    row("fee", "京都→城崎温泉 5,370円（乗車券2,640円＋特急料金2,730円）、京都→竹田 4,700円（乗車券2,310円＋特急料金2,390円）",
                        "Kyoto → Kinosaki Onsen ¥5,370 (fare ¥2,640 + express charge ¥2,730); Kyoto → Takeda ¥4,700 (fare ¥2,310 + express charge ¥2,390)")],
                   tip=TRAIN_TIP)),
    dict(id="takeda", name=T("竹田城跡", "Takeda Castle Ruins"), kind=T("城跡", "Castle ruins"),
         blurb=T("山のてっぺんに石垣だけが残る「天空の城」。秋の早朝は雲海に浮かびます。",
                 "The “castle in the sky”: only stone walls remain on the mountaintop. On autumn mornings it floats above a sea of clouds."),
         lat=35.30029, lng=134.82937,
         text=T("竹田城跡（たけだじょうあと）\n\n標高約350mの山の上に、石垣がほぼそのまま残る山城の跡です。建物は残っていませんが、"
                "石垣の上からは360度、但馬（たじま）の山と町が見渡せます。秋の早朝には雲海に浮かぶ姿が見られることがあり、「天空の城」と呼ばれています。\n\n"
                "竹田駅からは、天空バスかタクシーで山の中腹の「竹田城跡」バス停・タクシー乗降場まで約20分。そこから入り口まで歩いて約20分です。"
                "駅の裏から歩いて登る駅裏登山道は、クマの出没に備えて閉鎖が続いています（2026年10月の公式サイトの案内）。\n\n"
                "天空バスは、9〜11月のダイヤでは竹田駅10:05発（竹田城跡10:25着）。帰りは竹田城跡12:15発（竹田駅12:30着）か、12:50発（竹田駅13:05着）です。"
                "運賃は片道300円、1日フリー乗車券は500円で、現金だけ（ICカードは使えません）。12月以降の時刻は全但バスのサイトで確かめてください。\n\n"
                "城跡の中は30分〜1時間ほど。石垣の上は柵のない所もあるので、足元に気をつけてください。\n\nおすすめ訪問時間：10:05〜12:30（天空バスで往復）",
                "Takeda Castle Ruins\n\nThe stone walls of a mountaintop castle, about 350 m up, survive almost intact. No buildings are left, "
                "but from the top of the walls you get a 360° view over the mountains and towns of Tajima. On some autumn mornings the ruins seem to float above a sea of clouds, hence “castle in the sky”.\n\n"
                "From Takeda Station, take the Tenku Bus or a taxi to the “Takeda-jo-ato” stop halfway up (about 20 min), then walk about 20 min to the entrance. "
                "The trail from behind the station is still closed as a precaution against bears (official notice, October 2026).\n\n"
                "On the September–November timetable, the Tenku Bus leaves Takeda Station at 10:05 (arriving at the castle stop at 10:25). "
                "Coming back, it leaves the castle stop at 12:15 (Takeda Station 12:30) or 12:50 (13:05). "
                "The fare is ¥300 each way or ¥500 for a 1-day pass, cash only (no IC cards). From December, check the times on the Zentan Bus website.\n\n"
                "Allow 30 minutes to an hour inside. Parts of the walls have no railings, so watch your step.\n\nRecommended visit time: 10:05–12:30 (Tenku Bus both ways)"),
         gmaps=[gm("竹田城跡", "Takeda Castle Ruins", 35.30029, 134.82937, "竹田城跡"),
                gm("竹田城跡バス停・タクシー乗降場", "Takeda-jo-ato bus stop", 35.29916, 134.82498, "竹田城跡 バス停 タクシー乗降場")],
         links=[link("official", "竹田城跡 公式ホームページ", "Takeda Castle Ruins (official, Japanese)", "https://www.city.asago.hyogo.jp/site/takeda/"),
                link("timetable", "全但バス（天空バスの時刻表）", "Zentan Bus (Tenku Bus timetable, Japanese)", "https://www.zentanbus.co.jp/local_bus/tenkubus/")],
         info=info([row("hours", "3月〜5月 8:00〜17:00、6月〜12月はじめ（2026年は12月6日まで）5:00〜17:00、12月はじめ（2026年は12月7日から）〜1月3日 10:00〜15:00（最後に登れるのは30分前、南登山道は1時間前）",
                        "Mar–May 8:00–17:00; Jun–early Dec (until 6 Dec in 2026) 5:00–17:00; early Dec (from 7 Dec in 2026) – 3 Jan 10:00–15:00 (last entry 30 min before, 1 hour before on the south trail)"),
                    row("closed", "1月4日〜2月末は冬の閉山。大雨・台風・積雪などの日は入れないことがあります", "Closed for winter 4 Jan – end of Feb; may close in heavy rain, typhoons or snow"),
                    row("fee", "大人（高校生以上）500円、中学生以下は無料。現金とキャッシュレス決済が使えます", "Adults (high school and up) ¥500; junior high and under free. Cash or cashless"),
                    {"kind": "bus", "text": T("天空バス（9〜11月）：竹田駅10:05発 → 竹田城跡10:25着。帰りは竹田城跡12:15発 → 竹田駅12:30着（次は12:50発 → 13:05着）",
                                              "Tenku Bus (Sep–Nov): Takeda Station 10:05 → castle stop 10:25. Back: castle stop 12:15 → Takeda Station 12:30 (next 12:50 → 13:05)"),
                     "until": "2026-11-30", "from": None},
                    row("fee", "天空バス 片道300円、1日フリー乗車券500円（現金だけ）", "Tenku Bus ¥300 each way, 1-day pass ¥500 (cash only)")],
                   tip=T("天空バスの時刻と運賃は全但バスのサイト（2026年9〜11月のダイヤ）で確認しました。12月以降の時刻は全但バスのサイトで確かめてください。",
                         "Tenku Bus times and fares checked on the Zentan Bus website (September–November 2026 timetable). From December, check the times there.")),
         notices=[{"from": None, "to": None, "url": "https://www.city.asago.hyogo.jp/site/takeda/27510.html",
                   "text": T("駅裏登山道と表米神社登山道は閉鎖中です（クマの出没に備えて）。天空バスかタクシーで、西登山道・南登山道を使ってください。",
                             "The trails from behind the station and from Hyomai Shrine are closed (bear precautions). Use the Tenku Bus or a taxi and the west or south trail.")}]),
    dict(id="takedatown", name=T("竹田駅と寺町通り", "Takeda Station and Teramachi-dori"), kind=T("駅・町並み", "Station & old town"),
         blurb=T("竹田城跡のふもとの城下町。お寺と石の橋が並ぶ水路沿いの道を歩きます。",
                 "The castle town at the foot of Takeda Castle. Walk the canal lined with temples and stone bridges."),
         lat=35.29870, lng=134.83530,
         text=T("竹田駅と寺町通り（たけだえき・てらまちどおり）\n\n竹田城跡のふもとにある、小さな城下町です。駅の裏の山の上が竹田城跡。"
                "駅の西側には、水路に沿ってお寺が並ぶ寺町通りがあり、石の橋や白壁の古い家が残っています。\n\n"
                "城跡から戻ったら、町を歩いてお昼ごはんに。駅の近くには食事処やカフェもあります。\n\n"
                "城崎温泉へは、竹田13:34発の播但線で和田山へ行き、山陰本線に乗り換えて14:35着（860円）。\n\nおすすめ訪問時間：12:30〜13:30",
                "Takeda Station and Teramachi-dori\n\nA small castle town at the foot of Takeda Castle; the ruins sit on the hill right behind the station. "
                "West of the station, Teramachi-dori runs along a canal lined with temples, with stone bridges and old white-walled houses.\n\n"
                "Back from the castle, stroll the town and have lunch. There are places to eat and cafés near the station.\n\n"
                "To Kinosaki: take the 13:34 Bantan Line train to Wadayama and change to the San’in Line, arriving at 14:35 (¥860).\n\nRecommended visit time: 12:30–13:30"),
         gmaps=[gm("JR竹田駅", "JR Takeda Station", 35.29910, 134.83590, "JR竹田駅 兵庫県朝来市"),
                gm("竹田寺町通り", "Teramachi-dori", 35.29814, 134.83473, "竹田寺町通り 朝来市")],
         links=[JR],
         info=info([row("train", "竹田13:34発 → 和田山で乗り換え → 城崎温泉14:35着・860円", "Takeda 13:34 → change at Wadayama → Kinosaki Onsen 14:35, ¥860")],
                   tip=TRAIN_TIP)),
    # さとの湯は建て替え工事で休業中。駅前のさとの湯の足湯も2025年10月15日で使えなくなった（城崎温泉観光協会のお知らせ 2025-09-26）ので、足湯のことは書かない
    dict(id="station", name=T("城崎温泉駅", "Kinosaki Onsen Station"), kind=T("駅", "Station"),
         blurb=T("駅を出たら温泉街。外湯めぐりの1日券「ゆめぱ」は、どの外湯でも買えます。",
                 "Step out of the station into the onsen town. The “Yumepa” day pass is sold at every bathhouse."),
         lat=35.62398, lng=134.81331,
         text=T("城崎温泉駅（きのさきおんせんえき）\n\n駅を出るとすぐ温泉街。大谿川（おおたにがわ）沿いに柳並木が続き、浴衣と下駄で外湯（共同浴場）をめぐるのが城崎の楽しみ方です。\n\n"
                "外湯めぐりの1日券「ゆめぱ」（1,500円）は、どの外湯でも買えます。外湯は全部で7つありますが、駅前のさとの湯は建て替え工事のため休業しています（2024年4月から）。"
                "1日で回るなら3〜4か所がちょうどいいくらいです。\n\n"
                "竹田城跡に寄る日は14:35着。城崎温泉だけの日は9:52に着くので、朝からゆっくり回れます。\n\nおすすめ到着時間：14:35",
                "Kinosaki Onsen Station\n\nThe onsen town starts right outside. Willows line the Otani River, and the thing to do is wander between the public bathhouses in a yukata and wooden geta.\n\n"
                "The “Yumepa” day pass (¥1,500) is sold at every bathhouse. There are seven bathhouses, but Sato-no-yu by the station has been closed for rebuilding since April 2024. "
                "Three or four in a day is about right.\n\n"
                "You’ll arrive at 14:35 if you went to Takeda Castle first, or at 9:52 if you came straight, with the whole day to enjoy.\n\nRecommended arrival: 14:35"),
         gmaps=[gm("城崎温泉駅", "Kinosaki Onsen Station", 35.62398, 134.81331, "城崎温泉駅")],
         links=[SPA, JR],
         info=info([YUMEPA, row("closed", "さとの湯は建て替え工事のため休業中（2024年4月1日から）", "Sato-no-yu has been closed for rebuilding since 1 Apr 2024")],
                   tip=T("外湯の情報は城崎温泉観光協会のサイトで確認しました。", "Bathhouse details checked on the Kinosaki Onsen Tourism Association website."))),
    dict(id="jizo", name=T("地蔵湯", "Jizo-yu"), kind=T("外湯", "Public bath"),
         blurb=T("駅からいちばん近い外湯のひとつ。朝7時から開いています。",
                 "One of the bathhouses closest to the station, open from 7 in the morning."),
         lat=35.62681, lng=134.81265,
         text=T("地蔵湯（じぞうゆ）\n\n駅から歩いて数分の外湯です。泉源からお地蔵さまが出てきたという言い伝えにちなんだ名前で、地元の人もよく使う、気取らない雰囲気のお風呂です。\n\n"
                "朝7時から開いているので、城崎温泉だけの日は、ここから湯めぐりを始めるのもおすすめです。\n\nおすすめ訪問時間：14:45〜15:15",
                "Jizo-yu\n\nA bathhouse a few minutes’ walk from the station. It’s named after a statue of Jizo said to have appeared from the spring, and it has a relaxed, everyday feel; locals use it too.\n\n"
                "It opens at 7:00, so on a Kinosaki-only day it’s a good place to start.\n\nRecommended visit time: 14:45–15:15"),
         gmaps=[gm("地蔵湯", "Jizo-yu", 35.62681, 134.81265, "城崎温泉 地蔵湯")],
         links=[SPA],
         info=bath("7:00〜23:00", "7:00–23:00", "月曜", "Mondays")),
    dict(id="river", name=T("大谿川の柳並木", "Willows along the Otani River"), kind=T("散歩道", "Riverside walk"),
         blurb=T("石の太鼓橋と柳並木、木造の旅館。城崎らしい景色はこの川沿いに。",
                 "Arched stone bridges, willows and wooden inns: Kinosaki’s classic view is along this river."),
         lat=35.62630, lng=134.81130,
         text=T("大谿川の柳並木（おおたにがわのやなぎなみき）\n\n温泉街の真ん中を流れる大谿川に沿って、柳の並木と石の太鼓橋が続きます。川沿いには木造3階建ての旅館も並び、浴衣で歩く人の姿もよく似合います。\n\n"
                "外湯から外湯へは、この川沿いを歩いて数分ずつ。お土産屋さんや食べ歩きのお店も川の近くに集まっています。\n\nおすすめ訪問時間：15:15〜15:30",
                "Willows along the Otani River\n\nWillows and arched stone bridges line the Otani River through the middle of town, with three-storey wooden inns along the banks. It’s made for strolling in a yukata.\n\n"
                "The bathhouses are a few minutes apart along the river, and the souvenir shops and snack stalls are close by too.\n\nRecommended visit time: 15:15–15:30"),
         gmaps=[gm("大谿川", "Otani River", 35.62630, 134.81130, "城崎温泉 大谿川 柳並木")],
         links=[SPA],
         info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    dict(id="yanagi", name=T("柳湯", "Yanagi-yu"), kind=T("外湯", "Public bath"),
         blurb=T("柳の木のそばの、小さな外湯。午後3時から開きます。",
                 "A small bathhouse by the willows, opening at 3 pm."),
         lat=35.62642, lng=134.81022,
         text=T("柳湯（やなぎゆ）\n\n大谿川のほとりにある、こぢんまりとした外湯です。木造の建物が柳並木によく合います。\n\n"
                "開くのは午後3時から。一の湯へは川沿いに歩いてすぐです。\n\nおすすめ訪問時間：15:30〜15:50",
                "Yanagi-yu\n\nA compact bathhouse on the bank of the Otani River; its wooden building suits the willows perfectly.\n\n"
                "It opens at 15:00. Ichi-no-yu is just a short walk along the river.\n\nRecommended visit time: 15:30–15:50"),
         gmaps=[gm("柳湯", "Yanagi-yu", 35.62642, 134.81022, "城崎温泉 柳湯")],
         links=[SPA],
         info=bath("15:00〜23:00", "15:00–23:00", "木曜", "Thursdays")),
    dict(id="ichi", name=T("一の湯", "Ichi-no-yu"), kind=T("外湯", "Public bath"),
         blurb=T("お城のような建物の、城崎を代表する外湯。洞窟風呂が名物です。",
                 "Kinosaki’s signature bathhouse in a castle-like building, famous for its cave bath."),
         lat=35.62618, lng=134.80954,
         text=T("一の湯（いちのゆ）\n\n温泉街の真ん中にある、桃山風の立派な建物の外湯です。岩をくりぬいたような洞窟風呂が名物。\n\n"
                "人気があるので、夕方は混みやすいです。朝7時から開いているので、城崎温泉だけの日は朝のうちに入るのもおすすめです。\n\nおすすめ訪問時間：15:50〜16:30",
                "Ichi-no-yu\n\nIn the middle of town, in a grand Momoyama-style building. Its cave bath, which feels carved out of the rock, is the highlight.\n\n"
                "It’s popular and gets busy in the late afternoon. It opens at 7:00, so on a Kinosaki-only day try it in the morning.\n\nRecommended visit time: 15:50–16:30"),
         gmaps=[gm("一の湯", "Ichi-no-yu", 35.62618, 134.80954, "城崎温泉 一の湯")],
         links=[SPA],
         info=bath("7:00〜23:00", "7:00–23:00", "水曜", "Wednesdays")),
    dict(id="gosho", name=T("御所の湯", "Gosho-no-yu"), kind=T("外湯", "Public bath"),
         blurb=T("池の上に建つような大きな外湯。となりには四所神社があります。",
                 "A large bathhouse that seems to stand over a pond, next to Shisho Shrine."),
         lat=35.62590, lng=134.80740,
         text=T("御所の湯（ごしょのゆ）\n\n格子の立派な建物の前に池がある、大きな外湯です。露天風呂もあります。\n\n"
                "すぐとなりには温泉街の氏神さまの四所神社（ししょじんじゃ）。夏の夜は、鳥居から提灯が連なります。\n\nおすすめ訪問時間：16:40〜17:20",
                "Gosho-no-yu\n\nA large bathhouse with a pond in front of its grand latticed facade. It has an open-air bath too.\n\n"
                "Right next door is Shisho Shrine, the town’s guardian shrine; on summer nights, lanterns hang in rows from its torii.\n\nRecommended visit time: 16:40–17:20"),
         gmaps=[gm("御所の湯", "Gosho-no-yu", 35.62590, 134.80740, "城崎温泉 御所の湯")],
         links=[SPA],
         info=bath("7:00〜23:00", "7:00–23:00", "木曜", "Thursdays")),
    dict(id="mandara", name=T("まんだら湯", "Mandara-yu"), kind=T("外湯", "Public bath"),
         blurb=T("緑の屋根の小さな外湯。午後3時から開きます。",
                 "A small bathhouse with a green roof, opening at 3 pm."),
         lat=35.62446, lng=134.80573,
         text=T("まんだら湯（まんだらゆ）\n\n温泉街の奥のほうにある、小さめの外湯です。緑色の屋根が目印。\n\n"
                "開くのは午後3時から。にぎやかな中心から少し離れているぶん、落ち着いて入れることが多いです。\n\nおすすめ訪問時間：17:25〜17:45",
                "Mandara-yu\n\nA smaller bathhouse towards the far end of town; look for the green roof.\n\n"
                "It opens at 15:00. Being a little away from the busy centre, it’s often quieter.\n\nRecommended visit time: 17:25–17:45"),
         gmaps=[gm("まんだら湯", "Mandara-yu", 35.62446, 134.80573, "城崎温泉 まんだら湯")],
         links=[SPA],
         info=bath("15:00〜23:00", "15:00–23:00", "水曜", "Wednesdays")),
    dict(id="kou", name=T("鴻の湯", "Kou-no-yu"), kind=T("外湯", "Public bath"),
         blurb=T("いちばん奥にある、城崎でいちばん古いといわれる外湯。コウノトリの伝説があります。",
                 "The furthest bathhouse, said to be Kinosaki’s oldest, with a legend about a stork."),
         lat=35.62628, lng=134.80451,
         text=T("鴻の湯（こうのゆ）\n\n温泉街のいちばん奥、山のふもとにある外湯です。コウノトリが傷をいやしているのを見て温泉が見つかった、という言い伝えがあり、城崎でいちばん古い外湯といわれています。\n\n"
                "駅からは歩いて15分ほどなので、帰りの時間に気をつけてください。\n\nおすすめ訪問時間：17:50〜18:10",
                "Kou-no-yu\n\nAt the far end of town, at the foot of the hill. Legend says the spring was found when someone saw a stork healing its wound in it, and it’s said to be Kinosaki’s oldest bathhouse.\n\n"
                "It’s about 15 minutes’ walk from the station, so keep an eye on the time for your train.\n\nRecommended visit time: 17:50–18:10"),
         gmaps=[gm("鴻の湯", "Kou-no-yu", 35.62628, 134.80451, "城崎温泉 鴻の湯")],
         links=[SPA],
         info=bath("7:00〜23:00", "7:00–23:00", "火曜", "Tuesdays")),
    # 温泉寺とロープウェイは Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    dict(id="onsenji", name=T("温泉寺と城崎温泉ロープウェイ", "Onsen-ji Temple & Kinosaki Ropeway"), kind=T("お寺・ロープウェイ", "Temple & ropeway"),
         blurb=T("温泉街のいちばん奥から、ロープウェイで大師山の上へ。城崎の町と円山川を見下ろせます。途中の駅には、城崎温泉を開いた上人のお寺。",
                 "From the far end of town, a ropeway climbs Mt. Daishi for a view over Kinosaki and the Maruyama River. Halfway up is the temple of the monk who founded the hot spring."),
         lat=35.62524, lng=134.80382,
         text=T("温泉寺（おんせんじ）と城崎温泉ロープウェイ\n\n鴻の湯のすぐとなり、薬師公園にロープウェイの乗り場があります。山頂駅まで約7分。展望台からは、温泉街の屋根と円山川、その先の海まで見えます。山頂にはカフェもあります。\n\n"
                "途中の温泉寺駅の前が、温泉寺の本堂です。約1300年前に城崎温泉を開いた道智上人（どうちしょうにん）のお寺で、昔は城崎に着いたらまずここにお参りして、湯の入り方を教わってから外湯に入ったそうです（温泉寺の公式サイトより）。本堂の裏には多宝塔があります。\n\n"
                "ふもとの山門から本堂までは、石段を約500段、歩いて20分ほど。ロープウェイは上りの最終が16:50、下りの最終が17:10なので、夕方の外湯めぐりより先に行きましょう。ふもとの薬師堂は無料で、石段を上らなくてもお参りできます。\n\n"
                "山頂駅から温泉寺駅までの遊歩道は山道です。下駄やヒールでは歩きにくいので、歩く人は靴で。\n\nおすすめ訪問時間：9:10〜16:50の間に（山頂と温泉寺で1時間〜1時間半）",
                "Onsen-ji Temple and the Kinosaki Ropeway\n\nThe ropeway station is in Yakushi Park, right next to Kou-no-yu. It takes about 7 minutes to the top, where the lookout shows the roofs of the town, the Maruyama River and the sea beyond. There is a café at the top too.\n\n"
                "The middle station, Onsenji, is in front of the temple’s main hall. Onsen-ji is the temple of Dochi Shonin, the monk who founded Kinosaki Onsen about 1,300 years ago. In the old days visitors came here first to pray and learn how to bathe before going to the bathhouses (from the temple’s website). A two-storied pagoda stands behind the hall.\n\n"
                "On foot, it’s about 500 stone steps and 20 minutes from the gate at the bottom to the main hall. The last ropeway up is at 16:50 and the last one down at 17:10, so come here before your evening baths. The Yakushi-do hall at the foot is free and needs no climbing.\n\n"
                "The path between the top station and Onsenji station is a mountain trail: fine in shoes, awkward in geta or heels.\n\nRecommended visit time: any time between 9:10 and 16:50 (allow 1–1.5 hours for the summit and temple)"),
         gmaps=[gm("城崎温泉ロープウェイ 山麓駅", "Kinosaki Ropeway (bottom station)", 35.62524, 134.80382, "城崎温泉ロープウェイ"),
                gm("温泉寺 本堂", "Onsen-ji main hall", 35.62424, 134.80051, "温泉寺 城崎 本堂")],
         links=[link("official", "城崎温泉ロープウェイ 公式サイト", "Kinosaki Ropeway (official, Japanese)", "https://www.kinosaki-ropeway.jp/ropeway"),
                link("official", "温泉寺 公式サイト（拝観案内）", "Onsen-ji (official, Japanese)", "http://www.kinosaki-onsenji.jp/visit/seeing.html")],
         info={"rows": [row("hours", "ロープウェイ 9:10〜17:10。毎時10・30・50分発（12:30発は日曜・祝日だけ）。上りの最終16:50、下りの最終17:10。山頂駅まで約7分",
                            "Ropeway 9:10–17:10, leaving at :10, :30 and :50 (the 12:30 runs on Sundays and holidays only). Last car up 16:50, last down 17:10. About 7 min to the top"),
                        row("closed", "ロープウェイは第2・第4木曜（祝日は営業）。雷や強風で止まる日もあります", "Ropeway: 2nd and 4th Thursdays (open on holidays). It also stops for thunder or strong wind"),
                        row("fee", "ロープウェイ往復 山頂駅まで大人1,200円・小人600円、温泉寺駅まで大人750円・小人370円（片道は山頂620円・温泉寺380円）",
                            "Ropeway return: to the top ¥1,200 adults, ¥600 children; to Onsenji station ¥750 / ¥370 (one way ¥620 to the top, ¥380 to Onsenji)"),
                        row("hours", "温泉寺 本堂の拝観 9:00〜17:00（ロープウェイが休みの日は閉まることがあります）。ふもとの薬師堂は夏8:30〜17:00、冬9:00〜16:30",
                            "Onsen-ji main hall 9:00–17:00 (may close when the ropeway is not running). Yakushi-do at the foot: 8:30–17:00 in summer, 9:00–16:30 in winter"),
                        row("fee", "温泉寺 本堂 300円（城崎美術館との共通券400円）。薬師堂は無料", "Onsen-ji main hall ¥300 (¥400 with the Kinosaki Art Museum). Yakushi-do is free")],
               "cash": False, "checked": "2026-11-21",
               "tip": T("2026年11月21日に確認しました。ロープウェイの時刻・料金・休みは城崎温泉ロープウェイの公式サイトから。温泉寺の時間と拝観料は温泉寺の公式サイトからですが、案内が古いので変わっているかもしれません（要確認）。",
                        "Checked on 21 November 2026. Ropeway times, fares and closed days are from the official ropeway website. Onsen-ji’s hours and fee are from the temple’s website, which is old, so they may have changed (please check).")},
         _extra=[cc("onsenji-1.jpg", "663highland", "CC BY-SA 4.0", "File:Kinosaki ropeway01n2610.jpg"),
                 cc("onsenji-2.jpg", "663highland", "CC BY-SA 4.0", "File:241230 Kinosaki Ropeway Toyooka Hyogo pref Japan01s3.jpg"),
                 cc("onsenji-3.jpg", "663highland", "CC BY 2.5", "File:Onsenji02 1920.jpg"),
                 cc("onsenji-4.jpg", "663highland", "CC BY 2.5", "File:Onsenji04 2816.jpg")]),
    dict(id="night", name=T("夜の温泉街", "Kinosaki at night"), kind=T("散歩道", "Evening walk"),
         blurb=T("灯りがともる川沿いを、湯上がりにのんびり。夏は花火、冬は雪景色も。",
                 "A gentle post-bath stroll along the lantern-lit river. Fireworks in summer, snow in winter."),
         lat=35.62600, lng=134.80850,
         text=T("夜の温泉街（よるのおんせんがい）\n\n日が暮れると、柳並木と太鼓橋に灯りがともり、昼とはちがう落ち着いた雰囲気になります。湯上がりに浴衣で川沿いを歩くのは、城崎ならではの時間です。\n\n"
                "夏は温泉街で花火が上がる日があり（写真は2023年7月28日）、冬は雪をかぶった柳と灯籠の景色も見られます。花火の日程は年によって違うので、行く前に確かめてください。\n\n"
                "京都へ帰るなら、城崎温泉18:53発の特急に乗れるように駅へ向かいましょう。\n\nおすすめ訪問時間：18:10〜18:40",
                "Kinosaki at night\n\nAfter dark, the willows and arched bridges are lit up and the town takes on a calmer mood. Strolling the river in a yukata after a bath is pure Kinosaki.\n\n"
                "On some summer nights there are fireworks over the town (photos: 28 July 2023), and in winter you may see the willows and stone lanterns under snow. Firework dates change every year, so check before you go.\n\n"
                "If you’re heading back to Kyoto, make your way to the station in time for the 18:53 express.\n\nRecommended visit time: 18:10–18:40"),
         gmaps=[gm("城崎温泉 大谿川", "Otani River, Kinosaki", 35.62600, 134.80850, "城崎温泉 大谿川")],
         links=[SPA],
         info={"rows": [], "cash": False, "tip": None, "checked": CHECKED}),
    dict(id="station2", name=T("城崎温泉駅（帰り）", "Kinosaki Onsen Station (return)"), kind=T("駅（ゴール）", "Station (finish)"),
         blurb=T("18:53発の特急で京都へ。福知山で特急はしだてに乗り換え、21:20着。",
                 "Take the 18:53 express to Kyoto, changing at Fukuchiyama to the Hashidate, arriving 21:20."),
         lat=35.62398, lng=134.81331,
         text=T("城崎温泉駅（帰り）\n\n18:53発の特急こうのとり28号に乗り、福知山で特急はしだて10号に乗り換えると、京都に21:20に着きます。\n\n"
                "早めに帰るなら、16:31発の特急きのさき20号なら乗り換えなしで京都19:07着です。\n\n帰りの電車の窓からは、円山川（まるやまがわ）の景色が見えます。\n\nおすすめ出発時間：18:53",
                "Kinosaki Onsen Station (return)\n\nTake the 18:53 Konotori No. 28 and change at Fukuchiyama to the Hashidate No. 10, arriving in Kyoto at 21:20.\n\n"
                "For an earlier return, the 16:31 Kinosaki No. 20 goes straight to Kyoto, arriving at 19:07.\n\nOn the way back, watch the Maruyama River from the train window.\n\nRecommended departure time: 18:53"),
         gmaps=[gm("城崎温泉駅", "Kinosaki Onsen Station", 35.62398, 134.81331, "城崎温泉駅")],
         links=[JR],
         info=info([row("train", "城崎温泉18:53発 特急こうのとり28号 → 福知山で特急はしだて10号に乗り換え → 京都21:20着",
                        "Kinosaki Onsen 18:53 Konotori No. 28 → change at Fukuchiyama to Hashidate No. 10 → Kyoto 21:20"),
                    row("train", "早めに帰るなら：16:31発 特急きのさき20号 → 京都19:07着（乗り換えなし）", "Earlier: 16:31 Kinosaki No. 20 → Kyoto 19:07 (direct)"),
                    row("fee", "城崎温泉→京都 5,370円（乗車券2,640円＋特急料金2,730円）", "Kinosaki Onsen → Kyoto ¥5,370 (fare ¥2,640 + express charge ¥2,730)")],
                   tip=TRAIN_TIP)),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"], out.pop("_extra", None))
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
BATHS_AND_WALKS = [NO[k] for k in ("jizo", "river", "yanagi", "ichi", "gosho", "mandara", "kou", "onsenji", "night")]
data = {
    "id": "kinosaki",
    "_note": "京都から日帰り 城崎温泉（＋竹田城跡）のルート（kinosaki/ のページ専用。形は eizan-line.json と同じ）。京都7:32の特急きのさき1号で出発し、"
             "竹田城跡に寄る日は和田山で播但線に乗り換えて竹田へ、城跡と寺町通りを歩いてから城崎温泉へ。城崎では外湯（地蔵湯・柳湯・一の湯・御所の湯・まんだら湯・鴻の湯）と大谿川の柳並木を回り、"
             "18:53の特急で京都へ帰る。外湯と竹田城跡は行きたい所を選ぶので「選んで回る」で開く（plan.defaultMode）。"
             "写真は Toshi の写真ライブラリから選んだもの（城崎・竹田の2023〜2026年の写真、横写真約1,300枚を全部見て、1か所10枚以内・Nikon D7000 を含む。長辺1600px・位置情報なし）。"
             "京都駅の写真は城崎温泉駅で撮った特急の車両。外湯は建物の外の写真だけ。温泉寺とロープウェイ（2026-11-21 追加）は Toshi がまだ行っていない場所で、写真は Wikimedia Commons（photos の要素が {file, credit}）、文章は公式サイトの情報だけ。"
             "info.checked は事実情報を確認した日（外湯は城崎温泉観光協会、竹田城跡は朝来市の公式ホームページ、天空バスは全但バスのサイト（2026年9〜11月のダイヤ）、電車の時刻と運賃は乗換案内）。"
             "focus は地図を開いたときに映す範囲（京都と竹田は離れているので入れない）。このファイルは scripts/build_kinosaki_data.py で作る。",
    "sections": [
        {"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 3, "day": 1}, {"first": 4, "last": 6, "day": 2},
        {"first": 7, "last": 9, "day": 3}, {"first": 10, "last": 11, "day": 4},
        {"first": NO["onsenji"], "last": NO["onsenji"], "area": T("温泉寺・大師山", "Onsen-ji & Mt. Daishi"), "title": T("ロープウェイで温泉街の上へ", "Up the ropeway above the town")},
        {"first": NO["night"], "last": NO["station2"], "day": 5},
    ],
    "focus": {"first": NO["station"], "last": NO["station2"]},
    "plan": {"_note": "「選んで回る」の設定。京都駅・城崎温泉駅（行きと帰り）はいつも入る。竹田駅と寺町通りは竹田城跡を選ぶと入る。",
             "defaultMode": "pick",
             "picks": [NO["takeda"]] + BATHS_AND_WALKS,
             "auto": {str(NO["kyoto"]): {"always": True}, str(NO["takedatown"]): {"any": [NO["takeda"]]},
                      str(NO["station"]): {"always": True}, str(NO["station2"]): {"always": True}},
             "hints": [
                 {"spot": NO["kyoto"], "rule": {"any": [NO["takeda"]]},
                  "text": T("竹田城跡に寄るので、特急きのさき1号を和田山で降りて、播但線に乗り換えて竹田へ（9:36着）。9〜11月は竹田駅10:05発の天空バスで城跡へ。",
                            "You’re stopping at Takeda Castle: get off the Kinosaki No. 1 at Wadayama and change to the Bantan Line for Takeda (arr. 9:36). From September to November, take the 10:05 Tenku Bus up to the castle.")},
                 {"spot": NO["kyoto"], "rule": {"any": BATHS_AND_WALKS, "none": [NO["takeda"]]},
                  "text": T("竹田城跡には寄らないので、特急きのさき1号に乗ったまま城崎温泉へ（9:52着・乗り換えなし）。",
                            "No Takeda Castle today, so stay on the Kinosaki No. 1 all the way to Kinosaki Onsen (arr. 9:52, no change).")},
                 {"spot": NO["station"], "rule": {"any": BATHS_AND_WALKS, "none": [NO["takeda"]]},
                  "text": T("9:52に着くので、時間はたっぷり。柳湯とまんだら湯は15時からなので、午前中はほかの外湯や温泉街の散歩を。早く帰るなら16:31発のきのさき20号も。",
                            "You arrive at 9:52, so there’s plenty of time. Yanagi-yu and Mandara-yu open at 15:00, so start with the other baths and a stroll. For an early return, there’s the 16:31 Kinosaki No. 20.")},
                 {"spot": NO["onsenji"], "rule": {"any": [NO["onsenji"]], "andAny": [NO["takeda"]]},
                  "text": T("竹田城跡に寄る日は、城崎温泉に着くのが14:35。ロープウェイの上りは16:50が最終なので、外湯より先にロープウェイ乗り場へ向かいます（駅から歩いて約15〜20分）。15:10か15:30の便に乗れば、山頂と温泉寺を見て17:10までに下りられます。外湯は、そのあと奥の鴻の湯から駅の方へ戻りながら。",
                            "With Takeda Castle you reach Kinosaki at 14:35. The last ropeway up is at 16:50, so walk straight to the ropeway first (15–20 minutes from the station). Take the 15:10 or 15:30 car and you can see the summit and the temple and be down by 17:10. Do the baths afterwards, starting at Kou-no-yu and working back towards the station.")},
                 {"spot": NO["onsenji"], "rule": {"any": [NO["onsenji"]], "none": [NO["takeda"]]},
                  "text": T("城崎だけの日は、柳湯とまんだら湯が開く15時より前の時間に行くのがちょうどいいです。",
                            "On a Kinosaki-only day, go before 15:00, while Yanagi-yu and Mandara-yu are still closed.")},
             ]},
    "photoBase": "../images/kinosaki/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
