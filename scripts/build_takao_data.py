#!/usr/bin/env python3
"""京都 高雄の紅葉（神護寺・西明寺）のデータ（data/routes/takao.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/takao/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/takao"
OUT = f"{R}/data/routes/takao.json"
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




JRBUS = link("timetable", "JRバス 高雄・京北線", "JR Bus Takao–Keihoku line (Japanese)", "https://www.nishinihonjrbus.co.jp/route/kyoto/")
S = [
    dict(id="kiyotaki", name=T("高雄橋と清滝川", "Takao bridge & Kiyotaki river"), kind=T("渓谷", "Gorge"),
         blurb=T("バスを降りて谷へ下りると、朱の高雄橋と清滝川。川沿いの茶屋を過ぎて、神護寺への石段へ。",
                 "Down from the bus stop into the valley: the vermilion Takao bridge over the Kiyotaki, teahouses by the river, and the steps up to Jingoji."),
         lat=35.05542, lng=135.67303,
         text=T("高雄橋（たかおばし）と清滝川（きよたきがわ）\n\n京都駅前からJRバス高雄・京北線で「高雄」へ（約55分・230円）。8:30発に乗ると9:24に着きます。四条烏丸からは市バス8系統（約50分・230円、1時間に1本）。\n\n"
                "バス停から坂道を谷へ下りると、清滝川にかかる朱色の高雄橋。紅葉の時期は、谷じゅうがもみじに染まります。橋を渡ると、川沿いの茶屋の先から神護寺への長い石段が始まります。\n\n"
                "神護寺は受付が16:00までなので、先に神護寺へ上りましょう。\n\nおすすめ訪問時間：9:30〜9:50",
                "Takao bridge and the Kiyotaki river\n\nFrom Kyoto Station take the JR Bus Takao–Keihoku line to “Takao” (about 55 min, ¥230); the 8:30 arrives at 9:24. From Shijo-Karasuma, city bus 8 takes about 50 minutes (¥230, hourly).\n\n"
                "Walk down from the stop into the valley to the vermilion Takao bridge over the Kiyotaki. In autumn the whole gorge glows with maples. Across the bridge, past the riverside teahouses, the long stone stairway to Jingoji begins.\n\n"
                "Jingoji’s last entry is 16:00, so go up there first.\n\nRecommended visit time: 9:30–9:50"),
         gmaps=[gm("高雄橋", "Takao bridge", 35.05542, 135.67303, "高雄橋 京都 右京区")],
         links=[JRBUS],
         info=info([row("train", "京都駅前8:30発（JRバス）→ 高雄9:24着・230円（土曜はほぼ30分おき）", "Kyoto Station 8:30 (JR Bus) → Takao 9:24, ¥230 (about every 30 min on Saturdays)"),
                    row("hours", "高雄バス停から神護寺まで、遊歩道と石段で約30分", "About 30 min from the Takao stop to Jingoji by the path and stone stairs")],
                   tip=T("JRバスの公式サイトと乗換案内で確認しました。紅葉の時期の週末は臨時便が出ることがあります。", "Checked on the JR Bus website and a route planner; extra buses may run at autumn weekends."))),
    dict(id="jingoji", name=T("神護寺", "Jingoji"), kind=T("寺", "Temple"),
         blurb=T("長い石段を上った山の上のお寺。楼門をくぐると、広い境内一面がもみじに包まれます。",
                 "A mountaintop temple at the top of a long stone stairway; through the gate, the wide precinct is wrapped in maples."),
         lat=35.05467, lng=135.67131,
         text=T("神護寺（じんごじ）\n\n平安時代のはじめに開かれ、空海（弘法大師）もいたことのある、高雄山の中腹のお寺です。もみじに囲まれた長い石段を上りきると、楼門の先に広い境内が開けます。"
                "石段の上の金堂、毘沙門堂、五大堂のまわりは、紅葉の時期は一面の赤。\n\n"
                "境内の西の端からは、谷に向かって素焼きのお皿を投げる「かわらけ投げ」ができます。\n\nおすすめ訪問時間：9:55〜11:15",
                "Jingoji\n\nFounded in the early Heian period, and once home to Kukai (Kobo Daishi), this temple sits high on Mt. Takao. Climb the long, maple-lined stairs, and beyond the gate the broad precinct opens out. "
                "Around the main hall at the top of the steps, the Bishamon hall and the Godai hall, everything turns red in autumn.\n\n"
                "At the western edge of the grounds you can throw little clay discs into the valley (“kawarake-nage”).\n\nRecommended visit time: 9:55–11:15"),
         gmaps=[gm("神護寺", "Jingoji", 35.05467, 135.67131, "神護寺 高雄")],
         links=[link("official", "神護寺 公式サイト", "Jingoji (official, Japanese)", "http://jingoji.or.jp/")],
         info=info([row("hours", "9:00〜16:00", "9:00–16:00"), row("closed", "年中無休", "Open every day"),
                    row("fee", "中学生以上1,000円、小学生500円（2024年7月から）", "¥1,000 (junior high and up), ¥500 elementary (from July 2024)")],
                   tip=T("神護寺の公式サイトで確認しました。", "Checked on the temple website."))),
    dict(id="saimyoji", name=T("西明寺（槇尾）", "Saimyoji (Makinoo)"), kind=T("寺", "Temple"),
         blurb=T("清滝川にかかる朱の指月橋を渡って、小さな山寺へ。本堂と客殿のまわりのもみじが見事です。",
                 "Cross the vermilion Shigetsu bridge over the Kiyotaki to a small mountain temple, its halls framed by maples."),
         lat=35.05632, lng=135.67505,
         text=T("西明寺（さいみょうじ）\n\n神護寺の山門から、清滝川沿いの遊歩道を歩いて約20分。朱色の指月橋（しげつきょう）を渡ると、表門の先に本堂と客殿があり、庭のもみじがとくにきれいです。\n\n"
                "帰りは、近くの「槇ノ尾」バス停からJRバスで京都駅へ（約55分・230円）。さらに20分ほど歩けば、鳥獣戯画で知られる栂尾（とがのお）の高山寺にも行けます（入山料500円、石水院は別料金）。\n\nおすすめ訪問時間：11:35〜12:20",
                "Saimyoji\n\nAbout 20 minutes along the riverside path from Jingoji’s gate. Cross the vermilion Shigetsu bridge; beyond the front gate are the main hall and guest hall, with especially fine maples in the garden.\n\n"
                "Go home by JR Bus from the nearby “Makinoo” stop to Kyoto Station (about 55 min, ¥230). Or walk about 20 minutes more to Kosanji at Toganoo, famous for the Choju-giga scrolls (¥500 entry in autumn; Sekisuiin extra).\n\nRecommended visit time: 11:35–12:20"),
         gmaps=[gm("西明寺", "Saimyoji", 35.05632, 135.67505, "西明寺 槇尾")],
         links=[link("official", "西明寺 公式サイト", "Saimyoji (official, Japanese)", "https://www.saimyoji.or.jp/"),
                link("official", "高山寺 公式サイト", "Kosanji (official, Japanese)", "https://kosanji.com/"), JRBUS],
         info=info([row("hours", "9:00〜17:00（受付は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                    row("fee", "拝観料は公式サイトに書かれていません（要確認）", "Admission isn’t given on the official website (please check)"),
                    row("train", "槇ノ尾・栂ノ尾 → 京都駅前 JRバス 約55分・230円（日中ほぼ20分おき）", "Makinoo / Toganoo → Kyoto Station, JR Bus about 55 min, ¥230 (about every 20 min by day)")],
                   tip=T("西明寺・高山寺・JRバスの公式サイトで確認しました。", "Checked on the Saimyoji, Kosanji and JR Bus websites."))),
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
    "id": "takao",
    "_note": "京都 高雄の紅葉ルート（takao/ のページ専用。形は eizan-line.json と同じ）。JRバスで高雄へ、高雄橋・清滝川→神護寺→（清滝川沿い）西明寺→槇ノ尾からJRバス。"
             "写真は Toshi の写真ライブラリから選んだもの（2024年11月19日の Nikon D7000 と iPhone。実際は西明寺→神護寺の順に歩いたが、神護寺の受付が16:00までなので神護寺を先にした。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "info.checked は事実情報を確認した日（各寺の公式サイト、JRバス、乗換案内）。このファイルは scripts/build_takao_data.py で作る。",
    "sections": [{"first": 1, "last": 2, "day": 0}, {"first": 3, "last": 3, "day": 1}],
    "plan": {"_note": "「選んで回る」の設定。全部選べる。", "picks": [s["no"] for s in spots], "auto": {}, "hints": []},
    "photoBase": "../images/takao/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
