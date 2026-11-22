#!/usr/bin/env python3
"""京都から日帰り 城崎温泉（＋竹田城跡）ルートのデータを2コース分書き出す。
  data/routes/kinosaki.json        … 城崎温泉だけ（コースの id は late。最初に開く）
  data/routes/kinosaki-early.json  … 竹田城跡に寄ってから城崎温泉へ（コースの id は early）
（early / late は sync_higashiyama.py のコース切り替えの名前を借りているだけで、どちらも京都7:32発）

使い方: python3 scripts/build_kinosaki_data.py → python3 scripts/sync_kinosaki.py
- 2026-11-22「ゲストが実際に回れる1日」として見直し：三条のあたりからの行き方、乗り遅れたときの次の便、お昼と晩ごはん、
  外湯の休みの曜日、ロープウェイの冬の最終（11/1〜1/31は上り16:30・下り16:50）を入れた
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/kinosaki/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kinosaki"
OUT = f"{R}/data/routes/kinosaki.json"
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


def rowr(kind, ja, en, frm=None, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


JR = link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/")
SPA = link("official", "城崎温泉観光協会（外湯の時間と休み）", "Visit Kinosaki: the bathhouses", "https://kinosaki-spa.gr.jp/about/spa/7onsen/",
           "https://visitkinosaki.com/about-kinosaki/the-7-mystic-onsen/")
TATTOO = link("info", "Visit Kinosaki（タトゥーの案内。英語）", "Visit Kinosaki: tattoos at the bathhouses", "https://visitkinosaki.com/about-kinosaki/the-7-mystic-onsen/")
GUBI = link("official", "GUBIGABU（グビガブ）公式サイト", "GUBIGABU (official, Japanese)", "https://www.gubigabu.com/restaurant/")
TRAIN_TIP = T("時刻と運賃は乗換案内で確認しました（2026年11月25日・28日の検索）。特急の指定席は日によって200円変わります。乗る前に確かめてください。",
              "Times and fares checked on a route planner (searches for 25 and 28 November 2026). Reserved-seat charges vary by ¥200 depending on the day. Check before you travel.")
YUMEPA = row("fee", "1か所 大人800円。1日券「ゆめぱ」は1,500円で入り放題（外湯の窓口で買う）。2か所入るなら1日券",
             "¥800 per bath for adults. The “Yumepa” day pass is ¥1,500 for unlimited baths (buy it at any bathhouse counter): worth it from two baths")
BATH_TIP = T("タトゥーがあっても入れます（城崎の公式観光サイト Visit Kinosaki の案内。隠す必要もなし）。男女別。タオルは持っていきましょう。支払い方法は公式サイトに書かれていないので、現金があると確実です。",
             "Tattoos are fine (stated on Visit Kinosaki, the town’s official tourism site; no need to cover them). Baths are separated by gender. Bring a towel. The official pages don’t say how you can pay, so carry cash to be safe.")
CLOSED_DAYS = T("休みの曜日：月＝地蔵湯、火＝鴻の湯、水＝一の湯・まんだら湯、木＝御所の湯・柳湯",
                "Closed days: Mon Jizo-yu · Tue Kou-no-yu · Wed Ichi-no-yu, Mandara-yu · Thu Gosho-no-yu, Yanagi-yu")
FARE_KINO = row("fee", "京都↔城崎温泉 片道5,370〜5,570円（乗車券2,640円＋指定席2,730〜2,930円。日によって変わります）",
                "Kyoto ↔ Kinosaki Onsen ¥5,370–5,570 one way (fare ¥2,640 + reserved seat ¥2,730–2,930, depending on the day)")
SUBWAY = row("train", "三条のあたりから（平日）：地下鉄 烏丸御池6:57発→京都7:02着・220円（7:07発→7:12着でも間に合う）。三条京阪6:52発→烏丸御池で乗り換え→京都7:12着・260円",
             "From the Sanjo area (weekdays): subway from Karasuma Oike 6:57 → Kyoto 7:02, ¥220 (the 7:07 → 7:12 also works). From Sanjo Keihan 6:52 → change at Karasuma Oike → Kyoto 7:12, ¥260")
SUBWAY_JA = ("三条のあたりからは地下鉄で。烏丸御池（からすまおいけ）6:57発に乗ると京都7:02着（220円）。次の7:07発（7:12着）でも間に合います。"
             "三条京阪からは6:52発の東西線で烏丸御池へ行き、烏丸線に乗り換えて7:12着（260円）。どれも平日の時刻です。きっぷをまだ買っていない人、朝ごはんを買う人は、烏丸御池6:47発で。")
SUBWAY_EN = ("From the Sanjo area, take the subway. The 6:57 from Karasuma Oike gets to Kyoto at 7:02 (¥220); the 7:07 (arr. 7:12) still works. "
             "From Sanjo Keihan, take the 6:52 Tozai Line to Karasuma Oike and change to the Karasuma Line, arriving 7:12 (¥260). These are weekday times. If you still need tickets or breakfast, take the 6:47 from Karasuma Oike.")


def bath(hours_ja, hours_en, closed_ja, closed_en):
    return info([row("hours", hours_ja + "（受付は閉まる30分前まで）", hours_en + " (last entry 30 min before closing)"),
                 row("closed", closed_ja, closed_en), YUMEPA], tip=BATH_TIP)


def time_ja(t): return f"\n\nおすすめ訪問時間：{t}"
def time_en(t): return f"\n\nRecommended visit time: {t}"


def build(E):
    """E=True: 竹田城跡に寄るコース（early）。E=False: 城崎温泉だけ（late）"""
    def tm(late, early):
        t = early if E else late
        return t if isinstance(t, tuple) else (t, t)

    def text(ja, en, late, early):
        a, b = tm(late, early)
        return T(ja + time_ja(a), en + time_en(b))

    S = {}
    # ---------- 京都駅
    if E:
        S["kyoto"] = dict(
            name=T("京都駅", "Kyoto Station"), kind=T("駅（スタート）", "Station (start)"),
            blurb=T("三条のあたりを6:45ごろに出て、7:32の特急きのさき1号へ。和田山で乗り換えて竹田に9:36着。",
                    "Leave the Sanjo area around 6:45 for the 7:32 Kinosaki No. 1 express. Change at Wadayama; Takeda at 9:36."),
            caution=T("7:32に乗り遅れると竹田城跡は回れません", "Miss the 7:32 and the castle no longer fits"),
            lat=34.98535, lng=135.758766,
            text=T("京都駅（きょうとえき）\n\n7:32発の特急きのさき1号に乗ります。乗り場は山陰線（嵯峨野線）の30番のりば。"
                   "和田山（わだやま）に9:16に着いたら降りて、9:29発のJR播但線（ばんたんせん）寺前行きに乗り換え、竹田に9:36着です。\n\n"
                   + SUBWAY_JA + "\n\n"
                   "指定席は、帰りの城崎温泉18:53発の分も一緒に買っておきます。京都→竹田は4,700〜4,900円（日によって変わります）。竹田→城崎温泉は普通列車で860円。\n\n"
                   "7:32に乗り遅れたら、竹田駅10:05発の天空バスに間に合いません。一覧の上のボタンで「城崎温泉だけ」に切り替えて、8:38発の特急（福知山で乗り換え、城崎温泉10:58着）で行くのが現実的です。\n\n"
                   "お昼を食べる竹田は店が少ないので、心配な人は京都駅でお昼の分も買っておくと安心です。\n\n"
                   "写真は城崎温泉駅で撮った特急の車両です。\n\nおすすめ出発時間：6:45（三条のあたり）→ 7:32（京都駅）",
                   "Kyoto Station\n\nTake the 7:32 Kinosaki No. 1 limited express from platform 30 (San’in / Sagano Line). "
                   "Get off at Wadayama (9:16) and change to the 9:29 JR Bantan Line train for Teramae, arriving in Takeda at 9:36.\n\n"
                   + SUBWAY_EN + "\n\n"
                   "Buy your reserved seats ahead, including the 18:53 back from Kinosaki Onsen. Kyoto → Takeda is ¥4,700–4,900 (it depends on the day); Takeda → Kinosaki Onsen is ¥860 by local train.\n\n"
                   "If you miss the 7:32, you can’t make the 10:05 Tenku Bus at Takeda. Switch to “Kinosaki only” with the buttons above the list and take the 8:38 express (change at Fukuchiyama, Kinosaki Onsen 10:58).\n\n"
                   "There are few places to eat in Takeda, so if you want to be sure of lunch, buy it at Kyoto Station.\n\n"
                   "The photos of the trains were taken at Kinosaki Onsen Station.\n\nRecommended departure time: 6:45 (Sanjo area) → 7:32 (Kyoto Station)"),
            gmaps=[gm("JR京都駅", "JR Kyoto Station", 34.98535, 135.758766, "JR京都駅")], links=[JR],
            info=info([row("train", "特急きのさき1号 京都7:32発（30番のりば）→ 和田山9:16着。播但線 和田山9:29発 → 竹田9:36着",
                           "Kinosaki No. 1: Kyoto 7:32 (platform 30) → Wadayama 9:16. Bantan Line: Wadayama 9:29 → Takeda 9:36"),
                       SUBWAY,
                       row("fee", "京都→竹田 4,700〜4,900円（乗車券2,310円＋指定席2,390〜2,590円）。竹田→城崎温泉 860円",
                           "Kyoto → Takeda ¥4,700–4,900 (fare ¥2,310 + reserved seat ¥2,390–2,590). Takeda → Kinosaki Onsen ¥860"),
                       row("train", "乗り遅れたら：京都8:38発 特急はしだて1号 → 福知山9:55発 特急こうのとり1号 → 城崎温泉10:58着（竹田城跡はなし）",
                           "If you miss it: Kyoto 8:38 Hashidate No. 1 → Fukuchiyama 9:55 Konotori No. 1 → Kinosaki Onsen 10:58 (no castle)")],
                      tip=TRAIN_TIP))
    else:
        S["kyoto"] = dict(
            name=T("京都駅", "Kyoto Station"), kind=T("駅（スタート）", "Station (start)"),
            blurb=T("三条のあたりを6:45ごろに出て、7:32の特急きのさき1号へ。乗り換えなしで9:52に城崎温泉。",
                    "Leave the Sanjo area around 6:45 for the 7:32 Kinosaki No. 1 express: direct to Kinosaki Onsen, arriving 9:52."),
            caution=T("指定席は帰りの分も先に", "Reserve seats ahead, the return too"),
            lat=34.98535, lng=135.758766,
            text=T("京都駅（きょうとえき）\n\n7:32発の特急きのさき1号は、乗り換えなしで9:52に城崎温泉に着きます。乗り場は山陰線（嵯峨野線）の30番のりば。\n\n"
                   + SUBWAY_JA + "\n\n"
                   "指定席は帰りの分も一緒に買っておきます。片道5,370〜5,570円（日によって変わります）。\n\n"
                   "乗り遅れても大丈夫。8:38発の特急はしだて1号に乗り、福知山で9:55発の特急こうのとり1号に乗り換えると10:58着です（福知山の乗り換えは1分）。1時間遅れるだけで、あとは同じ順に回れます。\n\n"
                   "写真は城崎温泉駅で撮った特急の車両です。\n\nおすすめ出発時間：6:45（三条のあたり）→ 7:32（京都駅）",
                   "Kyoto Station\n\nThe 7:32 Kinosaki No. 1 limited express runs direct to Kinosaki Onsen, arriving at 9:52. It leaves from platform 30 (San’in / Sagano Line).\n\n"
                   + SUBWAY_EN + "\n\n"
                   "Buy reserved seats for both ways. One way is ¥5,370–5,570 (it depends on the day).\n\n"
                   "If you miss it, no harm done: take the 8:38 Hashidate No. 1 and change at Fukuchiyama to the 9:55 Konotori No. 1, arriving at 10:58 (the change at Fukuchiyama is one minute). You are an hour behind but can do everything in the same order.\n\n"
                   "The photos of the trains were taken at Kinosaki Onsen Station.\n\nRecommended departure time: 6:45 (Sanjo area) → 7:32 (Kyoto Station)"),
            gmaps=[gm("JR京都駅", "JR Kyoto Station", 34.98535, 135.758766, "JR京都駅")], links=[JR],
            info=info([row("train", "特急きのさき1号 京都7:32発（30番のりば）→ 城崎温泉9:52着（乗り換えなし）",
                           "Kinosaki No. 1: Kyoto 7:32 (platform 30) → Kinosaki Onsen 9:52 (direct)"),
                       SUBWAY, FARE_KINO,
                       row("train", "乗り遅れたら：京都8:38発 特急はしだて1号 → 福知山9:55発 特急こうのとり1号 → 城崎温泉10:58着",
                           "If you miss it: Kyoto 8:38 Hashidate No. 1 → Fukuchiyama 9:55 Konotori No. 1 → Kinosaki Onsen 10:58")],
                      tip=TRAIN_TIP))

    # ---------- 竹田（early だけ）
    S["takeda"] = dict(
        name=T("竹田城跡", "Takeda Castle Ruins"), kind=T("城跡", "Castle ruins"),
        blurb=T("山の上に石垣だけが残る「天空の城」。竹田駅10:05発の天空バスで上がり、12:15発で下ります。",
                "The “castle in the sky”: only stone walls remain on the mountaintop. Up on the 10:05 Tenku Bus from Takeda Station, down on the 12:15."),
        caution=T("天空バスは現金のみ。歩く登山道は閉鎖中", "Tenku Bus is cash only; the walking trails are closed"),
        lat=35.30029, lng=134.82937,
        text=T("竹田城跡（たけだじょうあと）\n\n標高約350mの山の上に、石垣がほぼそのまま残る山城の跡です。建物はありませんが、石垣の上から但馬（たじま）の山と町が360度見渡せます。秋の早朝には雲海に浮かぶことがあり、「天空の城」と呼ばれています（雲海は夜明けごろのもので、この時間には見られません）。\n\n"
               "9:36に竹田駅に着くと、バスまで約30分あります。駅のすぐ西の寺町通りを先に歩いておくと、お昼をゆっくり取れます。\n\n"
               "10:05発の天空バスで「竹田城跡」バス停へ（10:25着）。往復するので、車内で運転士から1日フリー乗車券（500円）を買います。現金のみで、ICカードは使えません。バス停から料金所までは坂道を歩いて約20分。城跡の中は40〜50分みておきます。石垣の上は柵のない所があるので足元に注意。\n\n"
               "11:50ごろには下り始めて、12:15発のバスで竹田駅に12:30着。乗り遅れても12:50発（13:05着）があり、13:34の電車には間に合いますが、お昼の時間がなくなります。\n\n"
               "駅の裏から歩いて登る道（駅裏登山道・表米神社登山道）は、クマの出没に備えて閉鎖が続いています（2026年10月16日の公式の案内）。\n\nおすすめ訪問時間：10:05〜12:30（天空バスで往復）",
               "Takeda Castle Ruins\n\nThe stone walls of a mountaintop castle, about 350 m up, survive almost intact. No buildings are left, but from the walls you get a 360° view over the mountains and towns of Tajima. On some autumn dawns the ruins float above a sea of clouds, hence “castle in the sky” (that happens around sunrise, not at this hour).\n\n"
               "You reach Takeda Station at 9:36, about 30 minutes before the bus. Walk Teramachi-dori, just west of the station, now and you’ll have a relaxed lunch later.\n\n"
               "Take the 10:05 Tenku Bus to the “Takeda-jo-ato” stop (10:25). You’re going both ways, so buy the ¥500 1-day pass from the driver. Cash only; no IC cards. From the stop it’s a 20-minute uphill walk to the ticket gate. Allow 40–50 minutes inside. Parts of the walls have no railings, so watch your step.\n\n"
               "Start down by about 11:50 for the 12:15 bus, back at Takeda Station at 12:30. If you miss it, the 12:50 (arr. 13:05) still connects with the 13:34 train, but leaves no time for lunch.\n\n"
               "The walking trails from behind the station (Ekiura and Hyomai Shrine trails) are still closed as a precaution against bears (official notice, 16 October 2026).\n\nRecommended visit time: 10:05–12:30 (Tenku Bus both ways)"),
        gmaps=[gm("竹田城跡", "Takeda Castle Ruins", 35.30029, 134.82937, "竹田城跡"),
               gm("竹田城跡バス停・タクシー乗降場", "Takeda-jo-ato bus stop", 35.29916, 134.82498, "竹田城跡 バス停 タクシー乗降場")],
        links=[link("official", "竹田城跡 公式ホームページ", "Takeda Castle Ruins (official, Japanese)", "https://www.city.asago.hyogo.jp/site/takeda/"),
               link("timetable", "全但バス（天空バスの時刻表）", "Zentan Bus (Tenku Bus timetable, Japanese)", "https://www.zentanbus.co.jp/local_bus/tenkubus/")],
        info=dict(info([
            rowr("bus", "天空バス（9〜11月）：竹田駅10:05発 → 竹田城跡10:25着。帰りは竹田城跡12:15発 → 竹田駅12:30着（次は12:50発 → 13:05着）",
                 "Tenku Bus (Sep–Nov): Takeda Station 10:05 → castle stop 10:25. Back: castle stop 12:15 → Takeda Station 12:30 (next 12:50 → 13:05)", until="2026-11-30"),
            rowr("bus", "天空バス：12月からの時刻は、2026年11月22日の時点で発表されていません（要確認）。全但バス 八鹿営業所 079-662-6151",
                 "Tenku Bus: times from December had not been published as of 22 November 2026 (please check). Zentan Bus Yoka office: 079-662-6151", frm="2026-12-01"),
            row("fee", "天空バス 片道300円。往復するなら1日フリー乗車券500円（最初に乗ったバスの中で買う）。現金のみ",
                "Tenku Bus ¥300 each way; for a return trip buy the ¥500 1-day pass on your first bus. Cash only"),
            row("hours", "城跡：6月〜12月はじめ 5:00〜17:00、12月はじめ〜1月3日 10:00〜15:00、3月〜5月 8:00〜17:00（最後に登れるのは30分前）",
                "Ruins: Jun–early Dec 5:00–17:00; early Dec–3 Jan 10:00–15:00; Mar–May 8:00–17:00 (last entry 30 min before)"),
            row("closed", "1月4日〜2月末は冬の閉山。大雨・台風・雪の日は入れないことがあります", "Closed for winter 4 Jan – end of Feb; may close in heavy rain, typhoons or snow"),
            row("fee", "観覧料 大人（高校生以上）500円、中学生以下は無料。現金・クレジットカード・QR決済（交通系ICは不可）",
                "Entry: adults (high school and up) ¥500; junior high and under free. Cash, credit cards or QR payment (no transit IC cards)")],
            tip=T("天空バスは全但バスのサイト（2026年9〜11月のダイヤ）、城跡の時間・料金・登山道は朝来市の公式ホームページで確認しました。",
                  "Tenku Bus checked on the Zentan Bus website (September–November 2026 timetable); hours, fees and trails on Asago City’s official site.")), cash=True),
        notices=[{"from": None, "to": "2026-11-30", "url": "https://www.city.asago.hyogo.jp/site/takeda/27510.html",
                  "text": T("駅裏登山道と表米神社登山道は閉鎖中（クマの出没に備えて）。天空バスかタクシーで上がってください。",
                            "The trails from behind the station and from Hyomai Shrine are closed (bear precautions). Go up by Tenku Bus or taxi.")},
                 {"from": "2026-12-01", "to": "2027-01-03", "url": "https://www.zentanbus.co.jp/local_bus/tenkubus/",
                  "text": T("12月からの天空バスの時刻は未発表でした（2026年11月22日に確認）。このページのバスの時刻は11月までのものです。行く前に全但バスで確かめてください。城跡は12月はじめから10:00〜15:00になります。",
                            "Tenku Bus times from December had not been published when checked on 22 November 2026. The bus times on this page are for November. Check with Zentan Bus before you go. From early December the ruins open 10:00–15:00.")},
                 {"from": "2027-01-04", "to": "2027-02-28", "url": "https://www.city.asago.hyogo.jp/site/takeda/3090.html",
                  "text": T("竹田城跡は冬の閉山中です（1月4日〜2月末）。一覧の上のボタンで「城崎温泉だけ」に切り替えてください。",
                            "Takeda Castle is closed for winter (4 January – end of February). Switch to “Kinosaki only” with the buttons above the list.")}])
    S["takedatown"] = dict(
        name=T("竹田駅と寺町通り", "Takeda Station and Teramachi-dori"), kind=T("駅・町並み", "Station & old town"),
        blurb=T("城跡のふもとの城下町でお昼。13:34の電車で城崎温泉へ向かいます。",
                "Lunch in the castle town below the ruins, then the 13:34 train to Kinosaki Onsen."),
        caution=T("13:34発を逃すと次は15:23発（城崎17:40着）", "Miss the 13:34 and the next is 15:23 (Kinosaki 17:40)"),
        lat=35.29870, lng=134.83530,
        text=T("竹田駅と寺町通り（たけだえき・てらまちどおり）\n\n12:30にバスで駅に戻ったら、まずお昼。竹田駅のまわりは店が少なく、昼だけの店や予約制の店もあります。営業時間を公式サイトで確かめられた店がなかったので、店名は書いていません（要確認）。京都駅でお昼を買ってきた人は、寺町通りのあたりで。\n\n"
               "寺町通りは駅のすぐ西。水路に沿ってお寺が並び、石の橋と白壁の家が続きます。\n\n"
               "城崎温泉へは13:34発の播但線で。和田山に13:40着、13:51発の山陰本線に乗り換えて城崎温泉14:35着（860円）。この電車は必ず乗ってください。次は15:23発で、城崎温泉に着くのは17:40。外湯は1つ入るのがやっとになります。\n\nおすすめ訪問時間：12:30〜13:30",
               "Takeda Station and Teramachi-dori\n\nBack at the station by bus at 12:30, have lunch first. There are only a few places to eat around Takeda Station; some open only at lunchtime or by reservation. I couldn’t confirm any shop’s hours on an official page, so I name none (please check). If you brought lunch from Kyoto Station, eat it around Teramachi-dori.\n\n"
               "Teramachi-dori is just west of the station: temples in a row along a canal, with stone bridges and white-walled houses.\n\n"
               "For Kinosaki, take the 13:34 Bantan Line train: Wadayama 13:40, change to the 13:51 San’in Line train, Kinosaki Onsen 14:35 (¥860). Don’t miss this one. The next leaves at 15:23 and reaches Kinosaki at 17:40, with time for barely one bath.\n\nRecommended visit time: 12:30–13:30"),
        gmaps=[gm("JR竹田駅", "JR Takeda Station", 35.29910, 134.83590, "JR竹田駅 兵庫県朝来市"),
               gm("竹田寺町通り", "Teramachi-dori", 35.29814, 134.83473, "竹田寺町通り 朝来市")],
        links=[JR],
        info=info([row("train", "竹田13:34発 → 和田山13:40着・13:51発 → 城崎温泉14:35着・860円", "Takeda 13:34 → Wadayama 13:40 / 13:51 → Kinosaki Onsen 14:35, ¥860"),
                   row("train", "次の電車：竹田15:23発 → 和田山・豊岡で乗り換え → 城崎温泉17:40着", "Next train: Takeda 15:23 → change at Wadayama and Toyooka → Kinosaki Onsen 17:40")],
                  tip=TRAIN_TIP))

    # ---------- 城崎温泉駅
    st_common_ja = ("外湯（共同浴場）は6つ。1か所800円、1日券「ゆめぱ」は1,500円で入り放題なので、2か所入るなら1日券です。最初に入る外湯の窓口で買えます。\n\n"
                    "タトゥーがあっても、どの外湯にも入れます。隠す必要もありません（城崎の公式観光サイト Visit Kinosaki の案内）。\n\n"
                    "外湯は曜日ごとに休みます。月曜＝地蔵湯、火曜＝鴻の湯、水曜＝一の湯・まんだら湯、木曜＝御所の湯・柳湯。柳湯とまんだら湯は15:00から。休みの外湯は「選んで回る」で外して、近くの別の外湯に替えてください。\n\n"
                    "駅のとなりのさとの湯は、建て替えのため2024年4月から休んでいます。再開の日は発表されていません。")
    st_common_en = ("There are six public bathhouses. One bath is ¥800; the “Yumepa” day pass is ¥1,500 for unlimited baths, so take the pass if you’ll use two or more. Buy it at the counter of your first bathhouse.\n\n"
                    "Tattoos are fine at every bathhouse, with no need to cover them (stated on Visit Kinosaki, the town’s official tourism site).\n\n"
                    "Each bathhouse closes one day a week: Monday Jizo-yu, Tuesday Kou-no-yu, Wednesday Ichi-no-yu and Mandara-yu, Thursday Gosho-no-yu and Yanagi-yu. Yanagi-yu and Mandara-yu open at 15:00. Drop the closed ones in “Choose stops” and use a nearby bath instead.\n\n"
                    "Sato-no-yu, next to the station, has been closed for rebuilding since April 2024; no reopening date has been announced.")
    if E:
        st_ja = ("城崎温泉駅（きのさきおんせんえき）\n\n14:35着。帰りの18:53発まで約4時間あります。外湯は3つがちょうどいい量です：地蔵湯 → 一の湯 → 御所の湯の順に奥へ歩き、17:15ごろから早めの晩ごはん、18:35に駅へ。\n\n" + st_common_ja + "\n\nおすすめ到着時間：14:35")
        st_en = ("Kinosaki Onsen Station\n\nYou arrive at 14:35, with about four hours until the 18:53 back. Three baths is the right amount: Jizo-yu → Ichi-no-yu → Gosho-no-yu, walking into town, then an early dinner from about 17:15 and back at the station by 18:35.\n\n" + st_common_en + "\n\nRecommended arrival: 14:35")
        st_blurb = T("14:35着。外湯は3つがちょうどいい量。1日券「ゆめぱ」は最初の外湯で。", "Arrive 14:35. Three baths is about right. Buy the “Yumepa” day pass at your first bathhouse.")
    else:
        st_ja = ("城崎温泉駅（きのさきおんせんえき）\n\n9:52着。駅を出るとすぐ温泉街です。午前は朝から開いている地蔵湯と一の湯、お昼をはさんで御所の湯、午後はいちばん奥のロープウェイと鴻の湯へ。外湯4つとロープウェイで16時すぎまで。そのあとは15:00に開く柳湯・まんだら湯か、早めの晩ごはんを。\n\n" + st_common_ja + "\n\nおすすめ到着時間：9:52")
        st_en = ("Kinosaki Onsen Station\n\nYou arrive at 9:52, and the onsen town starts right outside. In the morning, Jizo-yu and Ichi-no-yu (both open early); after lunch, Gosho-no-yu; in the afternoon, the ropeway and Kou-no-yu at the far end. Four baths and the ropeway take you to just after 16:00. Then Yanagi-yu or Mandara-yu (open from 15:00), or an early dinner.\n\n" + st_common_en + "\n\nRecommended arrival: 9:52")
        st_blurb = T("9:52着。外湯4つとロープウェイで1日。1日券「ゆめぱ」は最初の外湯で。", "Arrive 9:52. Four baths and the ropeway fill the day. Buy the “Yumepa” day pass at your first bathhouse.")
    S["station"] = dict(
        name=T("城崎温泉駅", "Kinosaki Onsen Station"), kind=T("駅", "Station"), blurb=st_blurb,
        caution=T("外湯は曜日ごとに休み。どこもタトゥーOK", "Each bath closes one day a week; tattoos OK at all"),
        lat=35.62398, lng=134.81331, text=T(st_ja, st_en),
        gmaps=[gm("城崎温泉駅", "Kinosaki Onsen Station", 35.62398, 134.81331, "城崎温泉駅")],
        links=[SPA, TATTOO, JR],
        info=info([YUMEPA, row("closed", CLOSED_DAYS["ja"], CLOSED_DAYS["en"]),
                   row("hours", "地蔵湯・一の湯・御所の湯・鴻の湯 7:00〜23:00、柳湯・まんだら湯 15:00〜23:00",
                       "Jizo-yu, Ichi-no-yu, Gosho-no-yu, Kou-no-yu 7:00–23:00; Yanagi-yu, Mandara-yu 15:00–23:00"),
                   row("closed", "さとの湯は建て替えのため休み（2024年4月から。再開日は未発表）", "Sato-no-yu is closed for rebuilding (since April 2024; no reopening date announced)")],
                  tip=T("外湯の時間・休み・料金は城崎温泉観光協会のサイト、タトゥーの扱いは公式観光サイト Visit Kinosaki で確認しました。祝日や年末年始は休みが変わることがあります。",
                        "Hours, closed days and prices checked on the Kinosaki Onsen Tourism Association website; the tattoo policy on Visit Kinosaki. Closed days can shift around holidays and New Year.")))

    # ---------- 外湯
    S["jizo"] = dict(
        name=T("地蔵湯", "Jizo-yu"), kind=T("外湯", "Public bath"),
        blurb=T("駅からいちばん近い外湯。最初の1つに。", "The bathhouse closest to the station: a good first one."),
        caution=T("月曜休み", "Closed Mondays"),
        lat=35.62681, lng=134.81265,
        text=text("地蔵湯（じぞうゆ）\n\n駅から歩いて数分。泉源からお地蔵さまが出てきたという言い伝えが名前の由来で、地元の人もよく使う、気取らない外湯です。\n\n"
                  "最初の1つにして、ここで1日券「ゆめぱ」を買います。月曜は休みなので、その日は一の湯から始めてください。",
                  "Jizo-yu\n\nA few minutes’ walk from the station. It’s named after a statue of Jizo said to have appeared from the spring, and has an everyday feel; locals use it too.\n\n"
                  "Make it your first bath and buy the “Yumepa” day pass here. It’s closed on Mondays; start at Ichi-no-yu instead.",
                  "10:00〜10:40", "14:45〜15:20"),
        gmaps=[gm("地蔵湯", "Jizo-yu", 35.62681, 134.81265, "城崎温泉 地蔵湯")], links=[SPA],
        info=bath("7:00〜23:00", "7:00–23:00", "月曜", "Mondays"))
    S["river"] = dict(
        name=T("大谿川の柳並木", "Willows along the Otani River"), kind=T("散歩道", "Riverside walk"),
        blurb=T("石の太鼓橋と柳、木造の旅館。外湯から外湯へはこの川沿いを歩きます。",
                "Arched stone bridges, willows and wooden inns. You walk this river from bath to bath."),
        lat=35.62630, lng=134.81130,
        text=text("大谿川の柳並木（おおたにがわのやなぎなみき）\n\n温泉街の真ん中を流れる大谿川に沿って、柳の並木と石の太鼓橋が続きます。川沿いには木造3階建ての旅館が並びます。\n\n"
                  "外湯から外湯へは、この川沿いを歩いて数分ずつ。お土産の店もこのあたりに集まっています。",
                  "Willows along the Otani River\n\nWillows and arched stone bridges line the Otani River through the middle of town, with three-storey wooden inns along the banks.\n\n"
                  "The bathhouses are a few minutes apart along the river. The souvenir shops are around here too.",
                  "10:45〜11:10", "15:20〜15:35"),
        gmaps=[gm("大谿川", "Otani River", 35.62630, 134.81130, "城崎温泉 大谿川 柳並木")], links=[SPA],
        info={"rows": [], "cash": False, "tip": None, "checked": CHECKED})
    S["yanagi"] = dict(
        name=T("柳湯", "Yanagi-yu"), kind=T("外湯", "Public bath"),
        blurb=T("柳並木のそばの小さな外湯。開くのは15:00から。", "A small bathhouse by the willows. It opens at 15:00."),
        caution=T("15:00から・木曜休み", "Opens 15:00 · closed Thursdays"),
        lat=35.62642, lng=134.81022,
        text=text("柳湯（やなぎゆ）\n\n大谿川のほとりの、こぢんまりした木造の外湯です。一の湯へは川沿いに歩いてすぐ。\n\n"
                  + ("15:00に開くので、着いてすぐでも入れます。水曜（一の湯が休み）や月曜（地蔵湯が休み）の代わりにどうぞ。" if E else
                     "15:00に開きます。奥の鴻の湯から駅へ戻る途中で、最後の1つに。"),
                  "Yanagi-yu\n\nA compact wooden bathhouse on the bank of the Otani River, a short walk along the river from Ichi-no-yu.\n\n"
                  + ("It opens at 15:00, so it’s available as soon as you arrive. Use it on Wednesdays (Ichi-no-yu closed) or Mondays (Jizo-yu closed)." if E else
                     "It opens at 15:00. Make it your last bath on the way back to the station from Kou-no-yu."),
                  "17:00〜17:30", ("15:40〜16:10（一の湯の代わりに）", "15:40–16:10 (instead of Ichi-no-yu)")),
        gmaps=[gm("柳湯", "Yanagi-yu", 35.62642, 134.81022, "城崎温泉 柳湯")], links=[SPA],
        info=bath("15:00〜23:00", "15:00–23:00", "木曜", "Thursdays"))
    lunch_ja = ("出たらお昼に（12:00〜13:00）。川沿いと駅通りに食事の店が並びます。大谿川のほとりの GUBIGABU（グビガブ）は城崎の地ビールのレストランで、11:30〜22:00（ラストオーダー21:30）、木曜と第3水曜が休み。"
                "ほかの店は昼だけ・夕方までの所もあるので、店先で時間を確かめてください。")
    lunch_en = ("Have lunch when you come out (12:00–13:00). Places to eat line the river and the street from the station. GUBIGABU, on the Otani River, is the restaurant of Kinosaki’s craft brewery: 11:30–22:00 (last orders 21:30), closed Thursdays and the 3rd Wednesday. "
                "Other places may open only for lunch or close in the late afternoon, so check the hours at the door.")
    S["ichi"] = dict(
        name=T("一の湯", "Ichi-no-yu"), kind=T("外湯", "Public bath"),
        blurb=T("お城のような建物の、城崎を代表する外湯。洞窟風呂が名物です。",
                "Kinosaki’s signature bathhouse in a castle-like building, known for its cave bath."),
        caution=T("水曜休み", "Closed Wednesdays"),
        lat=35.62618, lng=134.80954,
        text=text("一の湯（いちのゆ）\n\n温泉街の真ん中にある、桃山風の建物の外湯です。岩をくりぬいたような洞窟風呂が名物。\n\n"
                  + ("夕方は混むことがあります。水曜は休みなので、すぐ近くの柳湯（15:00から）に替えてください。" if E else
                     "夕方は混むことがあるので、午前のうちに。水曜は休みなので、その日は御所の湯を先に。\n\n" + lunch_ja),
                  "Ichi-no-yu\n\nIn the middle of town, in a Momoyama-style building. Its cave bath, which feels carved out of the rock, is the highlight.\n\n"
                  + ("It can be busy in the late afternoon. It’s closed on Wednesdays; use Yanagi-yu nearby (from 15:00) instead." if E else
                     "It can be busy in the late afternoon, so go in the morning. It’s closed on Wednesdays; go to Gosho-no-yu first that day.\n\n" + lunch_en),
                  ("11:15〜11:55（そのあとお昼）", "11:15–11:55 (then lunch)"), "15:40〜16:20"),
        gmaps=[gm("一の湯", "Ichi-no-yu", 35.62618, 134.80954, "城崎温泉 一の湯")], links=[SPA] + ([] if E else [GUBI]),
        info=bath("7:00〜23:00", "7:00–23:00", "水曜", "Wednesdays"))
    S["gosho"] = dict(
        name=T("御所の湯", "Gosho-no-yu"), kind=T("外湯", "Public bath"),
        blurb=T("露天風呂のある大きな外湯。となりは四所神社。", "A large bathhouse with an open-air bath, next to Shisho Shrine."),
        caution=T("木曜休み", "Closed Thursdays"),
        lat=35.62590, lng=134.80740,
        text=text("御所の湯（ごしょのゆ）\n\n格子の建物の前に池がある、大きな外湯です。露天風呂があります。となりは温泉街の氏神さまの四所神社（ししょじんじゃ）。\n\n"
                  + ("ここが3つ目。出たら川沿いを駅のほうへ戻りながら晩ごはんへ。駅までは歩いて10〜15分です。木曜は休みなので、奥のまんだら湯（15:00から）に替えてください。" if E else
                     "お昼のあとに。出たら、いちばん奥のロープウェイ乗り場まで歩いて7〜8分。14:10の便に乗ります。木曜は休みです。"),
                  "Gosho-no-yu\n\nA large bathhouse with a pond in front of its latticed facade, and an open-air bath. Next door is Shisho Shrine, the town’s guardian shrine.\n\n"
                  + ("This is your third bath. Afterwards head back along the river towards the station for dinner; the station is 10–15 minutes on foot. It’s closed on Thursdays; use Mandara-yu further in (from 15:00) instead." if E else
                     "Come after lunch. From here it’s 7–8 minutes on foot to the ropeway at the far end of town, for the 14:10 car. Closed on Thursdays."),
                  "13:10〜13:50", "16:30〜17:10"),
        gmaps=[gm("御所の湯", "Gosho-no-yu", 35.62590, 134.80740, "城崎温泉 御所の湯")], links=[SPA],
        info=bath("7:00〜23:00", "7:00–23:00", "木曜", "Thursdays"))
    S["mandara"] = dict(
        name=T("まんだら湯", "Mandara-yu"), kind=T("外湯", "Public bath"),
        blurb=T("緑の屋根の小さな外湯。開くのは15:00から。", "A small bathhouse with a green roof. It opens at 15:00."),
        caution=T("15:00から・水曜休み", "Opens 15:00 · closed Wednesdays"),
        lat=35.62446, lng=134.80573,
        text=text("まんだら湯（まんだらゆ）\n\n温泉街の奥のほうにある、小さめの外湯です。緑色の屋根が目印。\n\n"
                  + ("木曜（御所の湯が休み）の代わりに。駅まで歩いて15分ほどかかるので、17:10には出ましょう。" if E else
                     "15:00に開きます。鴻の湯から駅へ戻る途中で、もう1つ入りたい人に。"),
                  "Mandara-yu\n\nA smaller bathhouse towards the far end of town; look for the green roof.\n\n"
                  + ("Use it on Thursdays, when Gosho-no-yu is closed. It’s about 15 minutes’ walk to the station, so leave by 17:10." if E else
                     "It opens at 15:00. For one more bath on the way back to the station from Kou-no-yu."),
                  "16:20〜16:50", ("16:35〜17:05（御所の湯の代わりに）", "16:35–17:05 (instead of Gosho-no-yu)")),
        gmaps=[gm("まんだら湯", "Mandara-yu", 35.62446, 134.80573, "城崎温泉 まんだら湯")], links=[SPA],
        info=bath("15:00〜23:00", "15:00–23:00", "水曜", "Wednesdays"))
    S["kou"] = dict(
        name=T("鴻の湯", "Kou-no-yu"), kind=T("外湯", "Public bath"),
        blurb=T("いちばん奥の外湯。ロープウェイ乗り場のとなりです。", "The furthest bathhouse, next to the ropeway station."),
        caution=T("火曜休み・駅まで歩いて15〜20分", "Closed Tuesdays · 15–20 min walk to the station"),
        lat=35.62628, lng=134.80451,
        text=text("鴻の湯（こうのゆ）\n\n温泉街のいちばん奥、山のふもとにある外湯です。コウノトリが傷をいやしているのを見て温泉が見つかった、という言い伝えがあります。\n\n"
                  + ("駅から歩いて15〜20分。ロープウェイに乗った人が、下りてすぐ入るのにちょうどいい場所です。18:53の特急に乗るなら、18:10にはここを出てください。" if E else
                     "ロープウェイを下りたらすぐとなり。16:31の特急で帰る人は、ここには入らず15:50には駅へ向かってください（歩いて15〜20分）。"),
                  "Kou-no-yu\n\nAt the far end of town, at the foot of the hill. Legend says the spring was found when someone saw a stork healing its wound here.\n\n"
                  + ("It’s 15–20 minutes on foot from the station: best right after the ropeway. For the 18:53 express, leave here by 18:10." if E else
                     "It’s right next to the ropeway. If you’re taking the 16:31 express, skip this bath and start for the station by 15:50 (15–20 minutes on foot)."),
                  "15:35〜16:15", ("ロープウェイのあとに（17:00〜17:40）", "after the ropeway (17:00–17:40)")),
        gmaps=[gm("鴻の湯", "Kou-no-yu", 35.62628, 134.80451, "城崎温泉 鴻の湯")], links=[SPA],
        info=bath("7:00〜23:00", "7:00–23:00", "火曜", "Tuesdays"))

    # 温泉寺とロープウェイは Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    S["onsenji"] = dict(
        name=T("温泉寺と城崎温泉ロープウェイ", "Onsen-ji Temple & Kinosaki Ropeway"), kind=T("お寺・ロープウェイ", "Temple & ropeway"),
        blurb=T("いちばん奥からロープウェイで大師山の上へ。温泉街と円山川を見下ろします。途中の駅に、城崎温泉を開いた上人のお寺。",
                "From the far end of town, a ropeway climbs Mt. Daishi for a view over Kinosaki and the Maruyama River. Halfway up is the temple of the monk who founded the hot spring."),
        caution=T("11〜1月は上りの最終16:30。第2・第4木曜休み", "Nov–Jan: last car up 16:30. Closed 2nd & 4th Thursdays"),
        lat=35.62524, lng=134.80382,
        text=text("温泉寺（おんせんじ）と城崎温泉ロープウェイ\n\n鴻の湯のとなりの薬師公園に乗り場があります。毎時10分・30分・50分発で、山頂駅まで約7分。展望台から温泉街の屋根と円山川、その先の海まで見えます。山頂にカフェがあります。\n\n"
                  "11月1日〜1月31日は、上りの最終が16:30、下りの最終が16:50です（ふだんは16:50と17:10）。第2・第4木曜は休み。\n\n"
                  "途中の温泉寺駅の前が温泉寺の本堂。約1300年前に城崎温泉を開いた道智上人（どうちしょうにん）のお寺で、昔は城崎に着いたらまずここにお参りしてから外湯に入ったそうです（温泉寺の公式サイトより）。下りの便を温泉寺駅で降りて、お参りしてから次の便で下ります。\n\n"
                  + ("この時間割では入っていません。行くなら、14:35に着いたら外湯より先にここへ（駅から歩いて約20分）。15:10の便で上がり、16:30ごろまでに下りて、となりの鴻の湯と、帰り道の御所の湯に入ると、外湯は2つです。\n\n" if E else
                     "御所の湯を出て14:10の便で山頂へ。山頂で30分、温泉寺で20〜30分、15:30ごろに下りて、となりの鴻の湯へ。\n\n")
                  + "山頂駅から温泉寺駅までを歩く道は山道です。下駄では歩けません。",
                  "Onsen-ji Temple and the Kinosaki Ropeway\n\nThe station is in Yakushi Park, next to Kou-no-yu. Cars leave at :10, :30 and :50 and take about 7 minutes to the top, where the lookout shows the roofs of the town, the Maruyama River and the sea beyond. There is a café at the top.\n\n"
                  "From 1 November to 31 January the last car up is at 16:30 and the last one down at 16:50 (normally 16:50 and 17:10). Closed on the 2nd and 4th Thursdays.\n\n"
                  "The middle station, Onsenji, is in front of the temple’s main hall. Onsen-ji is the temple of Dochi Shonin, the monk who founded Kinosaki Onsen about 1,300 years ago; visitors used to pray here first before going to the baths (from the temple’s website). On the way down, get off at Onsenji station, visit, and take the next car.\n\n"
                  + ("It’s not in this timetable. If you want it, come here before any bath when you arrive at 14:35 (about 20 minutes on foot from the station). Go up on the 15:10, be down by about 16:30, then bathe at Kou-no-yu next door and Gosho-no-yu on the way back: two baths.\n\n" if E else
                     "From Gosho-no-yu, take the 14:10 car to the top. Allow 30 minutes at the summit and 20–30 at the temple, coming down around 15:30, then Kou-no-yu next door.\n\n")
                  + "The path between the top station and Onsenji station is a mountain trail: not for geta.",
                  "14:10〜15:30", ("着いたら先に（15:10〜16:30）", "first thing on arrival (15:10–16:30)")),
        gmaps=[gm("城崎温泉ロープウェイ 山麓駅", "Kinosaki Ropeway (bottom station)", 35.62524, 134.80382, "城崎温泉ロープウェイ"),
               gm("温泉寺 本堂", "Onsen-ji main hall", 35.62424, 134.80051, "温泉寺 城崎 本堂")],
        links=[link("official", "城崎温泉ロープウェイ 公式サイト", "Kinosaki Ropeway (official, Japanese)", "https://www.kinosaki-ropeway.jp/ropeway"),
               link("official", "温泉寺 公式サイト（拝観案内）", "Onsen-ji (official, Japanese)", "http://www.kinosaki-onsenji.jp/visit/seeing.html")],
        info={"rows": [rowr("hours", "ロープウェイ（11月1日〜1月31日）始発9:10、毎時10・30・50分発（12:30発は日曜・祝日だけ）。上りの最終16:30、下りの最終16:50",
                            "Ropeway (1 Nov – 31 Jan): first car 9:10, then at :10, :30 and :50 (the 12:30 runs on Sundays and holidays only). Last car up 16:30, last down 16:50", until="2027-01-31"),
                       rowr("hours", "ロープウェイ 9:10〜17:10。毎時10・30・50分発（12:30発は日曜・祝日だけ）。上りの最終16:50、下りの最終17:10",
                            "Ropeway 9:10–17:10, leaving at :10, :30 and :50 (the 12:30 runs on Sundays and holidays only). Last car up 16:50, last down 17:10", frm="2027-02-01"),
                       row("closed", "ロープウェイは第2・第4木曜（祝日は営業）。雷や強風で止まる日もあります", "Ropeway: 2nd and 4th Thursdays (open on holidays). It also stops for thunder or strong wind"),
                       row("fee", "ロープウェイ往復 山頂駅まで大人1,200円・小人600円、温泉寺駅まで大人750円・小人370円",
                           "Ropeway return: to the top ¥1,200 adults, ¥600 children; to Onsenji station ¥750 / ¥370"),
                       row("hours", "温泉寺 本堂の拝観 9:00〜17:00（ロープウェイが休みの日は閉まることがあります）",
                           "Onsen-ji main hall 9:00–17:00 (may close when the ropeway is not running)"),
                       row("fee", "温泉寺 本堂 300円", "Onsen-ji main hall ¥300")],
              "cash": False, "checked": CHECKED,
              "tip": T("ロープウェイの時刻・料金・休みは公式サイトと、城崎温泉観光協会の「冬期営業時間のお知らせ」（2026年10月20日）から。温泉寺の時間は温泉寺の公式サイトからですが、案内が古いので変わっているかもしれません（要確認）。",
                       "Ropeway times, fares and closed days are from its official site and the tourism association’s winter-hours notice (20 October 2026). Onsen-ji’s hours are from the temple’s website, which is old, so they may have changed (please check).")},
        _extra=[cc("onsenji-1.jpg", "663highland", "CC BY-SA 4.0", "File:Kinosaki ropeway01n2610.jpg"),
                cc("onsenji-2.jpg", "663highland", "CC BY-SA 4.0", "File:241230 Kinosaki Ropeway Toyooka Hyogo pref Japan01s3.jpg"),
                cc("onsenji-3.jpg", "663highland", "CC BY 2.5", "File:Onsenji02 1920.jpg"),
                cc("onsenji-4.jpg", "663highland", "CC BY 2.5", "File:Onsenji04 2816.jpg")])

    # ---------- 夜
    S["night"] = dict(
        name=T("夜の温泉街と晩ごはん", "Kinosaki in the evening, and dinner"), kind=T("散歩道・晩ごはん", "Evening walk & dinner"),
        blurb=T("灯りがともる川沿いを歩いて、早めの晩ごはん。18:35には駅へ。", "Walk the lantern-lit river and have an early dinner. Be at the station by 18:35."),
        caution=T("18:53の特急なら18:35に駅へ", "For the 18:53 express, be at the station by 18:35"),
        lat=35.62600, lng=134.80850,
        text=T("夜の温泉街と晩ごはん\n\n日が暮れると、柳並木と太鼓橋に灯りがともります。冬は17時ごろにはもう暗く、帰る前に夜の景色が見られます。\n\n"
               "18:53の特急で帰る人は、城崎で晩ごはんを済ませるのがおすすめです。京都に着くのは21:20で、京都駅の店はラストオーダーの直前になります。"
               "大谿川のほとりの GUBIGABU（グビガブ）は城崎の地ビールのレストランで、11:30〜22:00（ラストオーダー21:30）、通しで開いています。木曜と第3水曜は休み。"
               "ほかの店は夕方に閉まる所もあるので、店先で時間を確かめてください。時間がなければ、乗る前に食べるものを買って車内で。\n\n"
               "夏は温泉街で花火が上がる日があり（写真は2023年7月28日）、冬は雪をかぶった柳と灯籠が見られる日もあります。花火の日程は年によって違います。\n\nおすすめ訪問時間：17:15〜18:35",
               "Kinosaki in the evening, and dinner\n\nAfter dark the willows and arched bridges are lit. In winter it’s dark by about 17:00, so you see the night view before you leave.\n\n"
               "If you’re taking the 18:53 express, eat in Kinosaki: you reach Kyoto at 21:20, just before last orders at the station restaurants. "
               "GUBIGABU, on the Otani River, is the restaurant of Kinosaki’s craft brewery, open straight through 11:30–22:00 (last orders 21:30); closed Thursdays and the 3rd Wednesday. "
               "Other places may close in the late afternoon, so check the hours at the door. If you’re short of time, buy something to eat on the train.\n\n"
               "On some summer nights there are fireworks over the town (photos: 28 July 2023), and in winter you may see the willows and stone lanterns under snow. Firework dates change every year.\n\nRecommended visit time: 17:15–18:35"),
        gmaps=[gm("城崎温泉 大谿川", "Otani River, Kinosaki", 35.62600, 134.80850, "城崎温泉 大谿川")], links=[GUBI, SPA],
        info=info([row("hours", "GUBIGABU（グビガブ） 11:30〜22:00（ラストオーダー21:30）", "GUBIGABU 11:30–22:00 (last orders 21:30)"),
                   row("closed", "GUBIGABU 木曜・第3水曜", "GUBIGABU: Thursdays and the 3rd Wednesday")],
                  tip=T("GUBIGABU の時間と休みは公式サイトで確認しました。", "GUBIGABU’s hours and closed days checked on its official site.")))
    S["station2"] = dict(
        name=T("城崎温泉駅（帰り）", "Kinosaki Onsen Station (return)"), kind=T("駅（ゴール）", "Station (finish)"),
        blurb=T("18:53の特急で京都へ（福知山で乗り換え、21:20着）。早めなら16:31発で19:07着。",
                "The 18:53 express to Kyoto (change at Fukuchiyama, arr. 21:20). Earlier: the 16:31, arr. 19:07."),
        caution=T("18:53が最後の特急。次は普通で京都23:38着", "18:53 is the last express; after that, local trains reach Kyoto at 23:38"),
        lat=35.62398, lng=134.81331,
        text=T("城崎温泉駅（帰り）\n\n18:53発の特急こうのとり28号に乗り、福知山（19:59着）で20:05発の特急はしだて10号に乗り換えると、京都に21:20に着きます。"
               "これが京都へ帰れる最後の特急です。乗り遅れると、19:42発の普通列車を3回乗り継いで京都23:38着になります。\n\n"
               "京都駅に21:20に着いてから入れる店は少なく、京都拉麺小路（駅ビル10階）はラストオーダーが21:30です。晩ごはんは城崎で済ませるか、乗る前に買っておきます。\n\n"
               + ("" if E else
                  "早めに帰るなら、16:31発の特急きのさき20号が乗り換えなしで京都19:07着。晩ごはんは京都駅（京都拉麺小路、地下街ポルタのポルタダイニング。どちらも22:00まで）か、地下鉄で烏丸御池へ戻って三条・木屋町のあたりで。21〜22時まで開いている店がたくさんあります。\n\n")
               + "京都駅から三条のあたりへは、地下鉄烏丸線で烏丸御池まで約6分（220円）。\n\nおすすめ出発時間：18:53",
               "Kinosaki Onsen Station (return)\n\nTake the 18:53 Konotori No. 28, change at Fukuchiyama (arr. 19:59) to the 20:05 Hashidate No. 10, and you reach Kyoto at 21:20. "
               "This is the last express that gets you back to Kyoto. Miss it and it’s the 19:42 local with three changes, arriving at 23:38.\n\n"
               "Little is still serving when you reach Kyoto Station at 21:20; Kyoto Ramen Koji (10th floor of the station building) takes last orders at 21:30. Eat in Kinosaki, or buy something before you board.\n\n"
               + ("" if E else
                  "For an earlier return, the 16:31 Kinosaki No. 20 runs direct to Kyoto, arriving at 19:07. Have dinner at Kyoto Station (Kyoto Ramen Koji, or Porta Dining in the underground mall; both until 22:00), or take the subway back to Karasuma Oike and eat around Sanjo and Kiyamachi, where plenty of places stay open until 21:00–22:00.\n\n")
               + "From Kyoto Station to the Sanjo area, the Karasuma subway line takes about 6 minutes to Karasuma Oike (¥220).\n\nRecommended departure time: 18:53"),
        gmaps=[gm("城崎温泉駅", "Kinosaki Onsen Station", 35.62398, 134.81331, "城崎温泉駅")], links=[JR],
        info=info([row("train", "城崎温泉18:53発 特急こうのとり28号 → 福知山19:59着・20:05発 特急はしだて10号 → 京都21:20着（最後の特急）",
                       "Kinosaki Onsen 18:53 Konotori No. 28 → Fukuchiyama 19:59 / 20:05 Hashidate No. 10 → Kyoto 21:20 (last express)"),
                   row("train", "早めに帰るなら：16:31発 特急きのさき20号 → 京都19:07着（乗り換えなし）", "Earlier: 16:31 Kinosaki No. 20 → Kyoto 19:07 (direct)"),
                   row("train", "18:53に乗り遅れたら：19:42発の普通 → 豊岡・福知山・園部で乗り換え → 京都23:38着",
                       "If you miss the 18:53: 19:42 local → change at Toyooka, Fukuchiyama and Sonobe → Kyoto 23:38"),
                   FARE_KINO,
                   row("hours", "京都駅の晩ごはん：京都拉麺小路 11:00〜22:00（ラストオーダー21:30）。京都ポルタのポルタダイニング 11:00〜22:00（店によって違います）",
                       "Dinner at Kyoto Station: Kyoto Ramen Koji 11:00–22:00 (last orders 21:30); Porta Dining 11:00–22:00 (varies by shop)")],
                  tip=TRAIN_TIP))

    # ---------- 並べる
    if E:
        order = ["kyoto", "takeda", "takedatown", "station", "jizo", "river", "yanagi", "ichi", "gosho", "mandara", "kou", "onsenji", "night", "station2"]
        default = ["takeda", "jizo", "river", "ichi", "gosho", "night"]
    else:
        order = ["kyoto", "station", "jizo", "river", "ichi", "gosho", "onsenji", "kou", "mandara", "yanagi", "night", "station2"]
        default = ["jizo", "river", "ichi", "gosho", "onsenji", "kou", "night"]
    spots = []
    for i, sid in enumerate(order, 1):
        s = dict(S[sid])
        out = {"no": i, "id": sid}
        out.update(s)
        out["photos"] = photos(sid, out.pop("_extra", None))
        out.setdefault("notices", [])
        spots.append(out)
    NO = {s["id"]: s["no"] for s in spots}
    walks = [NO[k] for k in ("jizo", "river", "yanagi", "ichi", "gosho", "mandara", "kou", "onsenji", "night")]
    if E:
        sections = [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 3, "day": 1}, {"first": 4, "last": 6, "day": 2},
                    {"first": 7, "last": 9, "day": 3},
                    {"first": 10, "last": 12, "area": T("温泉街の奥", "The far end of town"), "title": T("時間があれば：奥の外湯とロープウェイ", "If you have time: the far baths and the ropeway")},
                    {"first": 13, "last": 14, "day": 4}]
        picks = [NO["takeda"]] + sorted(walks)
        auto = {str(NO["kyoto"]): {"always": True}, str(NO["takedatown"]): {"any": [NO["takeda"]]},
                str(NO["station"]): {"always": True}, str(NO["station2"]): {"always": True}}
        hints = [
            {"spot": NO["station"], "rule": {"any": [NO["onsenji"]]}, "from": None, "to": "2027-01-31",
             "text": T("ロープウェイを選んだので、外湯より先に乗り場へ（駅から歩いて約20分）。11〜1月は上りの最終が16:30です。15:10の便で上がり、下りたらとなりの鴻の湯、帰り道の御所の湯の順に。",
                       "You chose the ropeway: walk there before any bath (about 20 minutes from the station). From November to January the last car up is at 16:30. Go up on the 15:10, then bathe at Kou-no-yu next door and Gosho-no-yu on the way back.")},
            {"spot": NO["station"], "rule": {"any": [NO["onsenji"]]}, "from": "2027-02-01", "to": None,
             "text": T("ロープウェイを選んだので、外湯より先に乗り場へ（駅から歩いて約20分）。上りの最終は16:50です。15:10か15:30の便で上がり、下りたらとなりの鴻の湯、帰り道の御所の湯の順に。",
                       "You chose the ropeway: walk there before any bath (about 20 minutes from the station). The last car up is at 16:50. Go up on the 15:10 or 15:30, then bathe at Kou-no-yu next door and Gosho-no-yu on the way back.")},
            {"spot": NO["kyoto"], "rule": {"none": [NO["takeda"]]}, "from": None, "to": None,
             "text": T("竹田城跡を外すなら、一覧の上のボタンで「城崎温泉だけ」のコースに切り替えてください。乗り換えなしで9:52に城崎温泉に着きます。",
                       "If you’re skipping the castle, switch to the “Kinosaki only” course with the buttons above the list: direct, arriving at 9:52.")},
        ]
        note = "竹田城跡に寄るコース（early）。京都7:32→和田山→竹田9:36、天空バス10:05で城跡へ、12:30に駅へ戻ってお昼、13:34発で城崎温泉14:35着。外湯3つ（地蔵湯・一の湯・御所の湯）と早めの晩ごはん、18:53発で京都21:20着。"
    else:
        sections = [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 5, "day": 1}, {"first": 6, "last": 8, "day": 2},
                    {"first": 9, "last": 10, "day": 3}, {"first": 11, "last": 12, "day": 4}]
        picks = sorted(walks)
        auto = {str(NO["kyoto"]): {"always": True}, str(NO["station"]): {"always": True}, str(NO["station2"]): {"always": True}}
        hints = [
            {"spot": NO["station"], "rule": {"none": [NO["onsenji"]]}, "from": None, "to": None,
             "text": T("ロープウェイに乗らないなら、午後の時間が1時間あきます。鴻の湯を14時ごろにして、15:00に開くまんだら湯と柳湯をゆっくり回るか、16:31の特急で早めに帰って京都で晩ごはんを。",
                       "Without the ropeway you gain an hour in the afternoon. Go to Kou-no-yu around 14:00 and take your time at Mandara-yu and Yanagi-yu (open from 15:00), or go home on the 16:31 and have dinner in Kyoto.")},
        ]
        note = "城崎温泉だけのコース（late。最初に開く）。京都7:32→城崎温泉9:52。地蔵湯→大谿川→一の湯→お昼→御所の湯→ロープウェイ14:10→鴻の湯、そのあと15時に開くまんだら湯・柳湯か早めの晩ごはん、18:53発で京都21:20着（16:31発で19:07着も）。"
    data = {
        "id": "kinosaki",
        "course": "early" if E else "late",
        "_note": "京都から日帰り 城崎温泉（＋竹田城跡）のルート（kinosaki/ のページ専用。形は eizan-line.json と同じ）。" + note +
                 "2026-11-22 に「ゲストが実際に回れる1日」として見直し、竹田城跡あり／なしを2つのコース（一覧の上のボタン）に分けた。三条のあたりから京都駅までの行き方、乗り遅れたときの次の便、お昼と晩ごはん、外湯の休みの曜日を足した。"
                 "写真は Toshi の写真ライブラリから選んだもの（城崎・竹田の2023〜2026年の写真。長辺1600px・位置情報なし）。京都駅の写真は城崎温泉駅で撮った特急の車両。外湯は建物の外の写真だけ。"
                 "温泉寺とロープウェイは Toshi がまだ行っていない場所で、写真は Wikimedia Commons（photos の要素が {file, credit}）、文章は公式サイトの情報だけ。"
                 "GUBIGABU は公式サイトで時間を確かめて店名を出した店（Toshi が行ったとは書いていない）。竹田のお昼の店は公式で時間を確かめられず、店名を出していない。"
                 "info.checked は事実情報を確認した日（外湯は城崎温泉観光協会、タトゥーは Visit Kinosaki、竹田城跡は朝来市の公式ホームページ、天空バスは全但バスのサイト（2026年9〜11月のダイヤ。12月以降は未発表）、"
                 "ロープウェイは公式サイトと観光協会のお知らせ、電車と地下鉄の時刻と運賃は乗換案内、京都駅の店は天橋立マップのために同じ日に確認したもの）。"
                 "focus は地図を開いたときに映す範囲（京都と竹田は離れているので入れない）。このファイルは scripts/build_kinosaki_data.py で作る。",
        "sections": sections,
        "focus": {"first": NO["station"], "last": NO["station2"]},
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は時間割どおりの組み合わせ。駅はいつも入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": sorted(NO[k] for k in default), "auto": auto, "hints": hints},
        "photoBase": "../images/kinosaki/",
        "spots": spots,
    }
    out = f"{R}/data/routes/kinosaki{'-early' if E else ''}.json"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


build(False)
build(True)
