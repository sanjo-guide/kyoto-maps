#!/usr/bin/env python3
"""京都 今宮神社と鷹峯（光悦寺・源光庵・常照寺）のデータ（data/routes/takagamine.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/takagamine/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/takagamine"
OUT = f"{R}/data/routes/takagamine.json"
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


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def info(rows, tip=None, verified=True):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]




JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
S = [
    dict(id="imamiya", name=T("今宮神社とあぶり餅", "Imamiya Shrine & aburi-mochi"), kind=T("神社・おやつ", "Shrine & snack"),
         blurb=T("朱の楼門の今宮神社。東門の前では、向かい合う2軒の茶店が、千年続くあぶり餅を焼いています。",
                 "Imamiya Shrine with its vermilion gate; outside the east gate, two facing teahouses grill aburi-mochi, a thousand-year-old treat."),
         lat=35.04560, lng=135.74213,
         text=T("今宮神社（いまみやじんじゃ）とあぶり餅\n\n四条河原町から市バス46系統で「今宮神社前」へ（約35分・230円）。地下鉄の北大路駅からなら、北大路バスターミナルから204・205系統で「船岡山」へ、歩いて7分です。\n\n"
                "朱色の楼門をくぐると、広い境内に本殿が建ちます。東門を出た参道では、「一和（一文字屋和輔）」と「かざりや」の2軒が向かい合っています。"
                "竹ぐしに刺した小さなお餅を炭火であぶり、白みそのたれをからめた「あぶり餅」は、一和が平安時代（長保2年）から続く名物です。\n\n"
                "お店の営業時間・休み・値段は、公式の情報が見つかりませんでした（行く前に確かめてください）。写真は2026年5月。\n\nおすすめ訪問時間：10:00〜10:45",
                "Imamiya Shrine and aburi-mochi\n\nFrom Shijo-Kawaramachi take city bus 46 to “Imamiya-jinja-mae” (about 35 min, ¥230). From Kitaoji subway station, take bus 204 or 205 from the bus terminal to “Funaokayama” and walk 7 minutes.\n\n"
                "Through the vermilion gate is a broad precinct and the main hall. On the lane outside the east gate, two teahouses face each other: Ichiwa (Ichimonjiya Wasuke) and Kazariya. "
                "Small bamboo-skewered rice cakes toasted over charcoal and coated in sweet white-miso sauce: Ichiwa has served aburi-mochi since the Heian period (the year 1000).\n\n"
                "No official opening hours, closed days or prices could be found for the shops; check before you go. Photos from May 2026.\n\nRecommended visit time: 10:00–10:45"),
         gmaps=[gm("今宮神社", "Imamiya Shrine", 35.04560, 135.74213, "今宮神社"), gm("あぶり餅 かざりや", "Kazariya", 35.04521, 135.74279, "あぶり餅 かざりや")],
         links=[link("official", "今宮神社 公式サイト", "Imamiya Shrine (official, Japanese)", "http://www.imamiyajinja.org/")],
         info=info([row("hours", "参拝自由。社務所 9:00〜17:00", "Open to visit; shrine office 9:00–17:00"),
                    row("fee", "あぶり餅のお店の時間と値段は要確認", "Aburi-mochi shop hours and prices: please check")],
                   tip=T("今宮神社と京都観光Naviで確認しました。", "Checked on the shrine website and Kyoto Kanko Navi."))),
    dict(id="koetsuji", name=T("光悦寺", "Koetsuji"), kind=T("寺", "Temple"),
         blurb=T("江戸時代の芸術家・本阿弥光悦が開いた芸術村の跡。もみじのトンネルの参道と、竹を組んだ「光悦垣」。",
                 "The site of the artists’ village founded by Hon’ami Koetsu: a tunnel of maples and the woven bamboo “Koetsu fence”."),
         lat=35.05352, lng=135.73019,
         text=T("光悦寺（こうえつじ）\n\n今宮神社から歩いて6分の「佛教大学前」から、市バス北1・6系統で「鷹峯源光庵前」へ（4分・230円）。バス停から歩いて約3分です。\n\n"
                "江戸時代のはじめ、書や陶芸で知られる本阿弥光悦が徳川家康からこの地をもらい、職人たちと芸術村を開いた所です。"
                "石畳の参道はもみじのトンネルになり、境内には竹を斜めに組んだ「光悦垣」や茶室が点在します。鷹ヶ峰・鷲ヶ峰の山並みが目の前です。\n\n"
                "毎年11月10日〜13日は拝観できません。\n\nおすすめ訪問時間：11:15〜11:55",
                "Koetsuji\n\nFrom “Bukkyo-daigaku-mae”, 6 minutes’ walk from Imamiya Shrine, take city bus Kita-1 or 6 to “Takagamine-Genkoan-mae” (4 min, ¥230), then walk about 3 minutes.\n\n"
                "In the early Edo period, Hon’ami Koetsu, famous for calligraphy and pottery, was given this land by Tokugawa Ieyasu and founded an artists’ village with craftsmen. "
                "The stone-paved approach becomes a tunnel of maples; the grounds hold teahouses and the “Koetsu-gaki”, a fence of diagonally woven bamboo, with Takagamine’s hills right in front.\n\n"
                "Closed to visitors every year from 10 to 13 November.\n\nRecommended visit time: 11:15–11:55"),
         gmaps=[gm("光悦寺", "Koetsuji", 35.05352, 135.73019, "光悦寺 鷹峯")],
         links=[link("info", "光悦寺（京都観光Navi）", "Koetsuji (Kyoto Kanko Navi, Japanese)", "https://ja.kyoto.travel/tourism/single01.php?category_id=7&tourism_id=279")],
         info=info([row("hours", "8:00〜17:00（紅葉の時期は8:30から）", "8:00–17:00 (from 8:30 in autumn-leaf season)"),
                    row("closed", "毎年11月10日〜13日", "10–13 November every year"),
                    row("fee", "400円（紅葉の時期は500円）", "¥400 (¥500 in autumn-leaf season)")],
                   tip=T("京都観光Navi（京都市）で確認しました。お寺の公式サイトは見つかりませんでした。", "Checked on Kyoto Kanko Navi (Kyoto City); no temple website was found."))),
    dict(id="genkoan", name=T("源光庵", "Genkoan"), kind=T("寺", "Temple"),
         blurb=T("丸窓のある山門と、本堂から眺める静かな庭。四角い「迷いの窓」と丸い「悟りの窓」で知られるお寺です。",
                 "A gate with a round window and a quiet garden seen from the main hall; famous for its square “Window of Confusion” and round “Window of Enlightenment”."),
         lat=35.05484, lng=135.73182,
         text=T("源光庵（げんこうあん）\n\n光悦寺から歩いて約3分。丸い窓のある山門をくぐると、本堂の縁側から苔と植え込みの庭が眺められます。"
                "本堂の四角い「迷いの窓」と丸い「悟りの窓」は、人の一生と悟りの心を表すといわれ、紅葉の時期は窓の外が赤く染まります。\n\n"
                "お寺の行事があるときは拝観を中止することがあります。11月14日〜12月6日は駐車場が使えません。\n\nおすすめ訪問時間：12:00〜12:40",
                "Genkoan\n\nAbout 3 minutes’ walk from Koetsuji. Through a gate with a round window, look out from the main hall’s veranda over a garden of moss and clipped shrubs. "
                "The hall’s square “Window of Confusion” and round “Window of Enlightenment” are said to stand for human life and an enlightened mind; in autumn the view through them turns red.\n\n"
                "Visits are suspended during temple events. The car park is closed from 14 November to 6 December.\n\nRecommended visit time: 12:00–12:40"),
         gmaps=[gm("源光庵", "Genkoan", 35.05484, 135.73182, "源光庵 鷹峯")],
         links=[link("official", "源光庵 公式サイト", "Genkoan (official, Japanese)", "https://genkouan.or.jp/")],
         info=info([row("hours", "9:00〜17:00（受付は16:30まで）。行事の日は拝観中止のことあり", "9:00–17:00 (last entry 16:30); closed during temple events"),
                    row("fee", "拝観料は公式の案内に書かれていません（要確認）", "Admission isn’t given in the official information (please check)")],
                   tip=T("源光庵の公式サイトで確認しました。", "Checked on the temple website."))),
    dict(id="joshoji", name=T("常照寺", "Joshoji"), kind=T("寺", "Temple"),
         blurb=T("江戸時代の名妓・吉野太夫が寄進した朱の「吉野門」。丸い窓の茶室と、もみじの庭。",
                 "The vermilion “Yoshino gate” donated by the famed Edo-era courtesan Yoshino Tayu, a round-windowed teahouse and a maple garden."),
         lat=35.05525, lng=135.73283,
         text=T("常照寺（じょうしょうじ）\n\n源光庵から歩いて2分。参道の先の朱色の山門は、江戸時代の名妓・吉野太夫が寄進したと伝わる「吉野門」です。"
                "境内には丸い窓の茶室や、池のある庭があり、春は桜、秋はもみじがきれいです。\n\n"
                "帰りは「鷹峯源光庵前」から市バス北1系統で北大路バスターミナルへ（18分・230円、20分おき）。6系統なら四条大宮・京都駅の方へ行けます。\n\nおすすめ訪問時間：12:45〜13:25",
                "Joshoji\n\nTwo minutes’ walk from Genkoan. The vermilion gate at the end of the approach is the “Yoshino-mon”, said to have been donated by Yoshino Tayu, a celebrated courtesan of the Edo period. "
                "The grounds hold a teahouse with a round window and a pond garden: cherries in spring, maples in autumn.\n\n"
                "Head home on city bus Kita-1 from “Takagamine-Genkoan-mae” to Kitaoji bus terminal (18 min, ¥230, every 20 min), or bus 6 towards Shijo-Omiya and Kyoto Station.\n\nRecommended visit time: 12:45–13:25"),
         gmaps=[gm("常照寺", "Joshoji", 35.05525, 135.73283, "常照寺 鷹峯")],
         links=[link("official", "常照寺（お寺のサイト）", "Joshoji (temple site, Japanese)", "http://tsakae.justhpbs.jp/joshoji/toppage.html"), JR],
         info=info([row("hours", "8:30〜17:00", "8:30–17:00"),
                    row("fee", "大人400円、小学生200円", "¥400 adults, ¥200 elementary"),
                    row("train", "鷹峯源光庵前 → 北大路バスターミナル 市バス北1系統 18分・230円（毎時13・33・53分）", "Takagamine-Genkoan-mae → Kitaoji bus terminal, city bus Kita-1, 18 min, ¥230 (:13, :33, :53)")],
                   tip=T("常照寺のサイトと乗換案内で確認しました。", "Checked on the temple site and a route planner."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    out.setdefault("notices", [])
    spots.append(out)
NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}

data = {
    "id": "takagamine",
    "_note": "京都 今宮神社と鷹峯のルート（takagamine/ のページ専用。形は eizan-line.json と同じ）。今宮神社であぶり餅→市バスで鷹峯へ、光悦寺→源光庵→常照寺→市バスで北大路へ。"
             "写真は Toshi の写真ライブラリから選んだもの（鷹峯は2025年11月4日の Nikon D7000、今宮神社は2026年5月15日。人の顔が写る写真は使っていない。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（各寺社の公式サイト・京都観光Navi、バスは乗換案内）。このファイルは scripts/build_takagamine_data.py で作る。",
    "sections": [{"first": 1, "last": 1, "day": 0}, {"first": 2, "last": 4, "day": 1}],
    "plan": {"_note": "「選んで回る」の設定。全部選べる。", "picks": [s["no"] for s in spots], "auto": {}, "hints": [
        H("koetsuji", {"any": [NO["koetsuji"]], "none": [NO["imamiya"]]},
          "今宮神社に寄らない日は、地下鉄の北大路駅から市バス北1系統で「鷹峯源光庵前」へ（約18分・230円）。",
          "Skipping Imamiya? From Kitaoji subway station take city bus Kita-1 to “Takagamine-Genkoan-mae” (about 18 min, ¥230)."),
    ]},
    "photoBase": "../images/takagamine/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
