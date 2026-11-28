#!/usr/bin/env python3
"""函館で1日（函館駅のまわりのホテルから）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_hakodate_data.py   （そのあと python3 scripts/sync_hakodate.py）
- data/routes/hakodate.json          … late   ＝9〜10時に出る。朝市→五稜郭タワー・五稜郭公園→お昼→元町の坂と教会→函館山の夜景→夜の赤レンガ倉庫→晩ごはん（最初に開く）
- data/routes/hakodate-early.json    … early  ＝6時台に出る。朝市の朝ごはん→人のいない八幡坂と元町→赤レンガ倉庫→五稜郭→函館山の夜景→湯の川温泉→晩ごはん
- data/routes/hakodate-sapporo.json  … sapporo＝札幌から1泊2日。1日目は昼に着いて朝市・元町・函館山、2日目は五稜郭と湯の川温泉、夕方の特急で札幌へ
- 起点は函館駅のまわりのホテル（北海道のマップの決まり、2026-11-26）。だれかが行った・食べたことは書かない（写真は全部 Wikimedia Commons）
- 時間割は冬（12〜3月、12月の日の入りは16:07ごろ）を基本に組んだ。夏（日の入り19時ごろ）の函館山の順番は、函館山のスポットの文章に書いてある
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの時間割（pre）→ 共通の説明（body）→ おすすめの時間」の順に組み立てる
- JR と市電の時刻は乗換案内の2026年12月3日（木）・5日（土）のダイヤ。JR北海道のダイヤ改正（春）のあとは確かめ直す
- 市電は昼間およそ8分おきなので、時間割の市電の時刻は「例」。日の入りは函館の緯度・経度から計算した値（国立天文台の一覧に函館がないため）
- 写真は images/hakodate/<スポットのid>-w<番号>.jpg（Wikimedia Commons。一覧は scripts/hakodate_web_photos.json）。
  あとでオーナーの写真を <スポットのid>-<番号>.jpg で入れるときは、PHOTOS の先頭にファイル名を足す
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/hakodate"
CHECKED = "2026-11-28"
DEP = ("おすすめ出発時間", "Recommended departure time")
VIS = ("おすすめ訪問時間", "Recommended visit time")


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, start=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": start}


def notice(hja, hen, ja, en, url=None, start=None, to=None):
    d = {"head": T(hja, hen), "text": T(ja, en), "from": start, "to": to}
    if url:
        d["url"] = url
    return d


def q(f, t, day, hm, kind="d"):
    """確かめた乗換案内（Yahoo!路線情報）の検索結果のURL（飛行機なし）。day は '2026-12-03' の形"""
    h, m = hm.split(":")
    y, mon, d = day.split("-")
    p = {"from": f, "to": t, "y": y, "m": mon, "d": d, "hh": h, "m1": m[0], "m2": m[1], "type": {"d": 1, "l": 2, "a": 4}[kind],
         "ticket": "ic", "expkind": 1, "shin": 1, "ex": 1, "lb": 1, "al": 0, "hb": 1, "sr": 0, "s": 0, "userpass": 0, "ws": 3}
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(p)


def cc(x):
    """Wikimedia Commons の写真。"""
    return {"file": x["file"], "credit": {"author": x["author"], "license": x["license"],
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(x["title"].replace(" ", "_"))}}


WEB = json.load(open(f"{R}/scripts/hakodate_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]
# オーナーの写真が入ったら、ここで W(...) の前にファイル名を足す（例: "ropeway": ["ropeway-1.jpg"] + W("ropeway")）
PHOTOS = {k: W(k) for k in ("sapporo", "eki", "asaichi", "tower", "goryokaku", "hiru", "hachiman", "kokaido", "haris",
                            "ropeway", "kanemori", "yunokawa", "yuhan", "kaeri")}

D1, D2 = "2026-12-03", "2026-12-05"     # 乗換案内で確かめた日：木曜と土曜
U = dict(
    rw="https://334.co.jp/", rw_price="https://334.co.jp/ropeway/price/", rw_access="https://334.co.jp/access/",
    rw_en="https://334.co.jp/en/", rw_newyear="https://334.co.jp/news/2026/1123-22350/",
    rw_kisei="https://334.co.jp/news/2026/0401-22643/", rw_maint="https://334.co.jp/news/2026/1031-21931/",
    road="https://www.hakobura.jp/news/1062",
    tower="https://www.goryokaku-tower.co.jp/price/", tower_en="https://www.goryokaku-tower.co.jp/en/",
    bugyo="https://hakodate-bugyosho.jp/information/", bugyo_guide="https://hakodate-bugyosho.jp/guide/",
    asaichi="https://www.hakodate-asaichi.com/", asaichi_map="https://www.hakodate-asaichi.com/map/",
    kanemori="https://hakodate-kanemori.com/",
    kokaido="https://hakodate-kokaido.jp/",
    haris="https://www.orthodox-hakodate.jp/services",
    xmas="http://www.hakodatexmas.com/",
    lights="https://www.hakobura.jp/features/434",
    tram="https://www.city.hakodate.hokkaido.jp/bunya/hakodateshiden/",
    tram_fare="https://www.city.hakodate.hokkaido.jp/docs/2014012100946/",
    tram_pass="https://www.city.hakodate.hokkaido.jp/tram/value-ticket/",
    tram_shop="https://www.city.hakodate.hokkaido.jp/docs/2014012100991/",
    tram_ic="https://www.city.hakodate.hokkaido.jp/docs/2020111700024/",
    tram_time="https://www.city.hakodate.hokkaido.jp/docs/2014012100939/",
    tram_newyear="https://www.city.hakodate.hokkaido.jp/docs/2020102800313/",
    yu_day="https://hakodate-yunokawa.jp/dayspa/", yu_spots="https://hakodate-yunokawa.jp/spots/", yu_en="https://hakodate-yunokawa.jp/lan/en.html",
    eco="https://www.hako-eco.com/", eco_about="https://hako-eco.com/about", eco_qa="https://hako-eco.com/qa",
    trap="https://www.hakobura.jp/spots/504", tachi="https://www.hakobura.jp/spots/587",
    lp_goryo="https://luckypierrot.jp/shop/goryokaku/", lp_bay="https://luckypierrot.jp/shop/bayarea/", lp_eki="https://luckypierrot.jp/shop/hakodatest/",
    ajisai="https://www.ajisai.tv/shop/",
    yatai="https://www.hakodate-yatai.com/", yatai_faq="https://www.hakodate-yatai.com/faq",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    jr_info="https://www3.jrhokkaido.co.jp/webunkou/",
    vacan="https://vacan.com/map/41.7606471,140.7089998,15?areaName=hakodate-city",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("札幌→函館 朝 平日", q("札幌", "函館", D1, "08:00"), "特急北斗6号 8:43→12:33、9,770円（乗車券6,600円＋指定席3,170円）"),
    ("札幌→函館 朝 土曜", q("札幌", "函館", D2, "08:00"), "平日と同じ（北斗6号 8:43→12:33）"),
    ("札幌→函館 早朝・その次 平日", q("札幌", "函館", D1, "06:00"), "北斗2号 6:00→9:29。9:30で検索すると北斗8号 9:45→13:35"),
    ("函館→札幌 午後 平日", q("函館", "札幌", D1, "15:00"), "北斗15号 15:01→18:47、9,770円"),
    ("函館→札幌 夕方 平日", q("函館", "札幌", D1, "17:00"), "北斗19号 17:55→21:41、北斗21号 18:43→22:41"),
    ("函館→札幌 夕方 土曜", q("函館", "札幌", D2, "17:00"), "平日と同じ（17:55→21:41、18:43→22:41）"),
    ("函館→札幌 最終 平日", q("函館", "札幌", D1, "23:00", "l"), "最終は北斗21号 18:43→22:41"),
    ("JR北海道の特急は全車指定席・レールパス", U["railpass"], "All seats are reserved on all JR Hokkaido’s limited express trains. There are no non-reserved seats／パスで普通車指定席に乗れる"),
    ("市電 函館駅前→五稜郭公園前 平日", q("函館駅前", "五稜郭公園前", D1, "10:25"), "10:32→10:51、10:40→10:59、270円"),
    ("市電 函館駅前→五稜郭公園前 土曜", q("函館駅前", "五稜郭公園前", D2, "10:25"), "10:32→10:51"),
    ("市電 函館駅前→五稜郭公園前 朝", q("函館駅前", "五稜郭公園前", D1, "08:40"), "平日8:41→8:58・8:47→9:04、土曜8:42→8:59・8:48→9:07"),
    ("市電 五稜郭公園前→十字街 13時台", q("五稜郭公園前", "十字街", D1, "13:45"), "13:50→14:13、13:58→14:21、14:06→14:29、290円（土曜も同じ）"),
    ("市電 五稜郭公園前→十字街 14時台", q("五稜郭公園前", "十字街", D1, "14:40"), "14:46→15:09、14:54→15:17、15:02→15:25（土曜も同じ）"),
    ("市電 十字街→五稜郭公園前", q("十字街", "五稜郭公園前", D1, "11:20"), "11:22→11:47、11:30→11:55、11:38→12:03、290円（土曜も同じ）"),
    ("市電 函館駅前→十字街", q("函館駅前", "十字街", D1, "13:40"), "13:43→13:49、13:51→13:57、250円（土曜も同じ）"),
    ("市電 五稜郭公園前→湯の川温泉", q("五稜郭公園前", "湯の川温泉", D1, "12:05"), "12:11→12:23、12:19→12:31、270円（土曜も同じ）"),
    ("市電 十字街→湯の川温泉 夕方", q("十字街", "湯の川温泉", D1, "17:30"), "平日17:32→18:07・17:39→18:14、土曜17:30→18:07・17:38→18:14、300円"),
    ("市電 十字街→湯の川温泉 18時台", q("十字街", "湯の川温泉", D1, "18:30"), "平日18:35→19:10・18:42→19:17、土曜18:34→19:11・18:42→19:19"),
    ("市電 湯の川温泉→函館駅前 午後", q("湯の川温泉", "函館駅前", D1, "15:00"), "15:04→15:35、15:12→15:43、15:20→15:51、290円（土曜も同じ）"),
    ("市電 湯の川温泉→函館駅前 19時台", q("湯の川温泉", "函館駅前", D1, "19:30"), "19:37→20:07、19:52→20:22、20:06→20:36（土曜も同じ）"),
    ("市電 湯の川温泉→函館駅前 20時台", q("湯の川温泉", "函館駅前", D1, "20:20"), "20:21→20:51、20:41→21:11、21:01→21:31（土曜も同じ）"),
    ("市電 湯の川温泉→函館駅前 最終", q("湯の川温泉", "函館駅前", D1, "23:59", "l"), "最終21:46→22:16、その前21:26・21:01（土曜も同じ）"),
    ("市電 十字街→函館駅前 夜・最終", q("十字街", "函館駅前", D1, "23:59", "l"), "最終22:40→22:46、その前22:20・21:55（土曜も同じ）。19時台は平日19:03・19:09、土曜19:06・19:17"),
    ("市電 運賃", U["tram_fare"], "令和7年12月1日改定。2kmまで250円・4kmまで270円・7kmまで290円・7km超え300円。函館駅前から：十字街250円、五稜郭公園前270円、湯の川温泉290円。五稜郭公園前から：十字街290円、湯の川温泉270円。十字街から湯の川温泉300円。料金は降りるときに払う"),
    ("市電 1日乗車券", U["tram_pass"], "市電1日乗車券 大人800円（紙・スマートフォン）、24時間乗車券1,130円（スマートフォンのみ）、市電・函館バス1日乗車券1,600円（スマートフォンのみ）"),
    ("市電 1日乗車券の販売場所", U["tram_shop"], "市電1日乗車券は車内でも販売（停車中に乗務員へ）。函館市観光案内所（JR函館駅内）、駅前のホテルなど"),
    ("市電 ICカード", U["tram_ic"], "乗るときと降りるときにタッチ。Kitaca・Suica・PASMO・manaca・PiTaPa・TOICA・ICOCA・はやかけん・SUGOCA も使える"),
    ("函館山ロープウェイ 営業時間・運賃", U["rw_price"], "4/20〜9/30 始発10:00・上り最終21:30・下り最終22:00、10/1〜4/19 始発10:00・上り最終20:30・下り最終21:00。15分おき（混雑時5〜10分おき）、約3分。往復 大人1,800円・片道1,200円。クレジットカード・電子マネー・コード決済可"),
    ("函館山ロープウェイ 混雑", U["rw"], "日没・夜景になる時間から1〜2時間は山頂展望台が大変混み合うことが予想されます"),
    ("函館山ロープウェイ 年末年始", U["rw_newyear"], "2026年12月31日〜2027年1月3日：始発10:00、上り最終17:30、下り最終19:00。山頂展望台10:00〜19:00"),
    ("函館山ロープウェイ 秋の点検", U["rw_maint"], "2026年10月20日〜11月8日は法定整備点検のため運休"),
    ("函館山登山道 冬季通行止め", U["road"], "2026年11月9日11:00〜2027年4月12日11:00。期間中は車・タクシー・バスで山頂へ行けない。山頂へはロープウェイで"),
    ("函館山ロープウェイ アクセス", U["rw_access"], "函館山登山バス 片道 大人700円（函館バス）。元町・ベイエリア周遊号 250円"),
    ("五稜郭タワー", U["tower"], "9:00〜18:00（展望チケット販売終了17:50）、年中無休。大人1,200円・中高生900円・小学生600円。コインロッカー小300円・大500円（営業時間内）"),
    ("箱館奉行所", U["bugyo"], "一般500円。4〜10月9:00〜18:00（17:45受付終了）、11〜3月9:00〜17:00（16:45受付終了）。休館は12月31日〜1月3日と臨時休館"),
    ("箱館奉行所 見学の注意", U["bugyo_guide"], "履き物を脱いで入館、大きな荷物の持ち込み禁止、館内は飲食禁止"),
    ("函館朝市", U["asaichi"], "年中無休（店ごとに異なる）。1〜4月6:00〜14:00過ぎ、5〜12月5:00〜14:00過ぎ"),
    ("金森赤レンガ倉庫", U["kanemori"], "物販店9:30〜19:00、函館ビヤホール 平日11:30〜21:30・土日祝11:00〜21:30（21:00L.O.）、年中無休"),
    ("旧函館区公会堂", U["kokaido"], "4〜10月9:00〜18:00（土〜月は19:00まで）、11〜3月9:00〜17:00。入館は終了の30分前まで。一般300円。年末年始休館 令和8年12月31日〜令和9年1月3日、臨時休館 令和9年1月26日"),
    ("函館ハリストス正教会", U["haris"], "拝観 月〜金10:00〜17:00（11・12・3月は16:00まで）、土10:00〜16:00、日13:00〜16:00。冬期（12月25日〜2月末）はお祈り以外の拝観休止。拝観献金 大人200円・中学生100円。聖堂内部の撮影は不可"),
    ("はこだてクリスマスファンタジー", U["xmas"], "2026年12月1日（火）〜12月25日（金）。ツリー点灯16:30〜17:45・18:00〜22:00（12/1は18:00から）。花火は毎日18時。スープバー16:30〜20:00"),
    ("Hakodate Winter Lights", U["lights"], "八幡坂・開港通り・駅前のイルミネーション 2026年12月1日〜2027年2月28日、日没〜22:00（予定）。五稜星の夢 同じ期間、日没〜19:00（予定）。冬花火：1月8日〜30日の金・土18:00湯の川温泉、2月5日〜27日の金・土18:00金森赤レンガ倉庫周辺"),
    ("湯の川温泉 日帰り入浴", U["yu_day"], "ホテル雨宮館 800円・6:00〜22:00、KKRはこだて 1,000円・11:00〜21:00、ホテルテトラ湯の川温泉 550円・13:00〜22:00、湯元啄木亭 1,200円・13:00〜21:00（タオル300円）、笑函館屋 平日1,200円・土日祝1,500円・15:00〜21:00。タトゥーの記載なし"),
    ("湯の川温泉 足湯", U["yu_spots"], "湯の川温泉足湯 湯巡り舞台（毎日9:00〜21:00）、湯川町1-16-5"),
    ("函館市熱帯植物園", U["eco_about"], "4〜10月9:30〜18:00、11〜3月9:30〜16:30。休園12月29日〜1月1日。一般300円。12月から5月のゴールデンウィークまで、サル山で温泉に入るサル"),
    ("熱帯植物園 サルの温泉の時期", U["eco_qa"], "12月1日から翌年の5月GW前後まで（赤ちゃんが生まれた時点でそのシーズンは終了）"),
    ("トラピスチヌ修道院", U["trap"], "（3・4・10・11月）8:30〜16:30、（5〜9月）8:30〜17:00、（12〜2月）9:00〜16:00。年末年始12月29日〜1月2日休み。無料。「トラピスチヌ入口」バス停から徒歩10分"),
    ("立待岬", U["tachi"], "冬期は車両通行止め、徒歩のみ通行可能。市電「谷地頭」電停から徒歩20分"),
    ("ラッキーピエロ", U["lp_goryo"], "五稜郭公園前店 9:30〜22:00（ラストオーダー21:30）。ベイエリア本店10:00〜21:00（同20:30）、函館駅前店8:00〜22:00（同21:30）"),
    ("函館麺厨房あじさい", U["ajisai"], "本店（五稜郭町29-22）11:00〜20:25（LO）、第四水曜休み。紅店（豊川町12-7 函館ベイ美食倶楽部）11:00〜21:30（LO）"),
    ("函館ひかりの屋台 大門横丁", U["yatai_faq"], "26店。営業時間・定休日は店ごとに違う。基本は現金払い。予約は各店へ"),
]]

JR = link("timetable", "JR北海道 運行情報", "JR Hokkaido service status", U["jr_info"])
TRAM = link("timetable", "函館市電（時刻表・乗車券）", "Hakodate City Tram (timetables, passes)", U["tram"])
RW = link("official", "函館山ロープウェイ（運行状況・料金）", "Mt. Hakodate Ropeway (status, fares)", U["rw"], U["rw_en"])

# ---------------------------------------------------------------------------
# 何か所かに出すお知らせ
# ---------------------------------------------------------------------------
N_WINTER_WALK = notice(
    "冬は坂と歩道が凍ります", "Slopes and pavements freeze in winter",
    "12〜3月は雪と氷の道です。元町の坂は急で、下りがいちばん滑ります。底に溝の深い、滑りにくい靴で、歩く時間を多めに見てください。雪の日は市電も遅れます。",
    "From December to March the streets are snow and ice. The Motomachi slopes are steep and going down is the slippery part. Wear shoes with deep tread and allow extra walking time. Trams also run late in snow.",
    start="2026-11-20", to="2027-03-31")
N_YEAREND = notice(
    "年末年始は時間が変わります", "Shorter hours over New Year",
    "函館山ロープウェイは12月31日〜1月3日、上りの最終17:30・下りの最終19:00。箱館奉行所と旧函館区公会堂は12月31日〜1月3日、熱帯植物園は12月29日〜1月1日が休み。市電も年末年始のダイヤになります。朝市は店ごとに違います。",
    "The ropeway’s last ride up is 17:30 and last ride down 19:00 from 31 December to 3 January. The Magistrate’s Office and the Old Public Hall close 31 December–3 January; the tropical garden closes 29 December–1 January. Trams run a holiday timetable. Market stalls each keep their own days.",
    U["rw_newyear"], to="2027-01-03")
N_XMAS = notice(
    "12月1日〜25日 はこだてクリスマスファンタジー", "Hakodate Christmas Fantasy, 1–25 December",
    "赤レンガ倉庫の前の海に大きなツリーが浮かびます。点灯は16:30〜17:45と18:00〜22:00（12月1日は18:00から）。毎日18:00に点灯式と花火（風の強い日は中止）。温かいスープの屋台は16:30〜20:00。",
    "A large tree floats on the water in front of the warehouses. Lights are on 16:30–17:45 and 18:00–22:00 (from 18:00 on 1 December), with a relighting and fireworks every day at 18:00 (cancelled in strong wind). Soup stalls open 16:30–20:00.",
    U["xmas"], start="2026-11-20", to="2026-12-25")
N_LIGHTS = notice(
    "12月1日〜2月28日 坂のイルミネーション", "Lights on the slopes, 1 December–28 February",
    "八幡坂と開港通りの並木に明かりがつきます（日の入り〜22:00の予定）。2月5日〜27日の金曜・土曜は、18:00から赤レンガ倉庫のあたりで冬花火（約10分の予定）。",
    "The trees on Hachiman-zaka and Kaiko-dori are lit from sunset to 22:00 (planned). On Fridays and Saturdays from 5 to 27 February there are winter fireworks near the warehouses at 18:00 (about 10 minutes, planned).",
    U["lights"], start="2026-11-20", to="2027-02-28")
N_HARIS_WINTER = notice(
    "12月25日〜2月末は聖堂の中に入れません", "No visits inside from 25 December to the end of February",
    "冬のあいだは、お祈りのとき以外の拝観をお休みしています。外からは見られます。",
    "In winter the church is closed to visitors except during services. You can still see it from outside.",
    U["haris"], start="2026-12-15", to="2027-02-28")
N_ROPE_AUTUMN = notice(
    "秋にロープウェイが止まる時期があります", "The ropeway closes for inspection in autumn",
    "2026年は10月20日〜11月8日が点検で運休でした。2027年の日程は公式サイトで確かめてください。運休のあいだは登山バスやタクシーで山頂へ（道路が雪で通行止めの日は行けません）。",
    "In 2026 it was closed for inspection from 20 October to 8 November. Check the official site for 2027. While it is closed, the summit is reached by bus or taxi (not on days the road is shut by snow).",
    U["rw"], start="2027-09-15", to="2027-11-15")
N_MONKEY = notice(
    "12月〜5月の連休ごろ サルの温泉", "Monkeys in the hot spring, December to early May",
    "熱帯植物園のサル山に温泉が入るのは、12月1日から5月の連休ごろまで。4月に赤ちゃんが生まれると、その年は早めに終わります。",
    "The monkey enclosure at the tropical garden has hot-spring water from 1 December until around the early-May holidays. It ends earlier if a baby is born in April.",
    U["eco_qa"], start="2026-11-20", to="2027-05-06")
N_YU_FIRE = notice(
    "1月の金曜・土曜は湯の川で冬花火", "Winter fireworks at Yunokawa on January Fridays and Saturdays",
    "2027年1月8日〜30日の金曜・土曜、18:00から海岸で約10分（予定）。",
    "Fridays and Saturdays from 8 to 30 January 2027, at 18:00 from the shore, for about 10 minutes (planned).",
    U["lights"], start="2026-12-26", to="2027-01-30")

# ---------------------------------------------------------------------------
# スポットの共通部分
# ---------------------------------------------------------------------------
ROPE_SEASON_JA = ("・12月：日の入り16:05〜16:15 → 15:30ごろの便で上へ\n・1月：16:15〜16:50 → 15:45〜16:15ごろ\n・2月：16:50〜17:25 → 16:15〜16:45ごろ\n"
                  "・3〜4月：17:25〜18:35 → 17:00〜18:00ごろ\n・5〜8月：18:20〜19:15 → 18:00〜18:30ごろ（晩ごはんを先に）\n・9〜11月：18:15〜16:10 → 月のはじめと終わりで1時間違います")
ROPE_SEASON_EN = ("· December: sunset 16:05–16:15 → ride up around 15:30\n· January: 16:15–16:50 → around 15:45–16:15\n· February: 16:50–17:25 → around 16:15–16:45\n"
                  "· March–April: 17:25–18:35 → around 17:00–18:00\n· May–August: 18:20–19:15 → around 18:00–18:30 (eat dinner first)\n· September–November: 18:15 down to 16:10; it moves an hour within a month")

S = dict(
    sapporo=dict(
        name=T("札幌駅（JR）", "Sapporo Station (JR)"), kind=T("駅", "Station"),
        blurb=T("特急北斗で函館まで3時間50分。全部の席が指定席なので、先にきっぷを取ります。",
                "The Hokuto limited express takes 3 hours 50 minutes to Hakodate. Every seat is reserved, so get your ticket first."),
        lat=43.06866, lng=141.35079,
        body=T("特急北斗（ほくと）は自由席がありません。乗る前に、駅のみどりの窓口か指定席券売機で指定席を取ってください。片道9,770円（乗車券6,600円＋指定席3,170円）。\n\n"
               "外国のパスポートで使えるJR北海道レールパス（全線）なら、指定席も追加料金なしで取れます。パスでも席の指定は必要です。\n\n"
               "苫小牧（とまこまい）を過ぎると左に太平洋、長万部（おしゃまんべ）からは左に内浦湾。函館の手前の大沼公園（おおぬまこうえん）のあたりでは、晴れていれば駒ヶ岳が見えます。\n\n"
               "雪の日は遅れや運休が出ることがあります。出る前にJR北海道の運行情報を見てください。",
               "The Hokuto limited express has no unreserved seats. Reserve a seat at the ticket office or a reserved-seat machine before boarding. One way is ¥9,770 (fare ¥6,600 + reserved seat ¥3,170).\n\n"
               "With the JR Hokkaido Rail Pass (all lines, for foreign passport holders) reserved seats cost nothing extra, but you still need to get a seat ticket.\n\n"
               "After Tomakomai the Pacific is on the left; from Oshamambe it is Uchiura Bay. Near Onuma-Koen, just before Hakodate, Mt. Komagatake shows on a clear day.\n\n"
               "Snow can delay or cancel trains. Check JR Hokkaido’s service status before you leave."),
        gmaps=[gm("JR札幌駅", "JR Sapporo Station", 43.06866, 141.35079, "JR札幌駅")],
        links=[JR, link("info", "JR北海道のレールパス（英語）", "JR Hokkaido rail passes", U["railpass"])],
        rows=[row("fee", "札幌→函館 9,770円（乗車券6,600円＋指定席3,170円）", "Sapporo → Hakodate ¥9,770 (fare ¥6,600 + reserved seat ¥3,170)")],
        tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました。春のダイヤ改正のあとは確かめ直してください。指定席とパスのことはJR北海道の英語のページで確認しました。",
              "Times and fares from a route planner for Thursday 3 and Saturday 5 December 2026; check again after the spring timetable change. Seat and pass rules from JR Hokkaido’s English site.")),

    eki=dict(
        name=T("函館（はこだて）駅と市電", "Hakodate Station and the tram"), kind=T("駅・市電", "Station, tram"),
        blurb=T("朝市は駅のすぐ横。五稜郭・元町・湯の川へは、駅前から市電で行きます。",
                "The morning market is next to the station. Trams from the front of the station go to Goryokaku, Motomachi and Yunokawa."),
        lat=41.773798, lng=140.726378,
        body=T("・市電（路面電車）：乗り場「函館駅前」は、駅を出て広場の先の大通りにあります。昼間はおよそ8分おき。2系統と5系統のどちらに乗っても、五稜郭公園前・十字街・湯の川温泉に行けます。\n\n"
               "・運賃：乗った距離で250〜300円（函館駅前から十字街250円、五稜郭公園前270円、湯の川温泉290円）。降りるときに払います。Suica・Kitaca・ICOCAなどの交通系ICカードが使え、乗るときと降りるときにタッチします。\n\n"
               "・1日乗車券：800円。3回乗ればほぼ元が取れます。市電の車内（止まっているときに運転士さんへ）、駅の中の観光案内所、駅前のホテルなどで買えます。スマートフォン版と24時間券（1,130円）もあります。\n\n"
               "・最終：湯の川温泉発は21:46（函館駅前22:16着）、十字街発は22:40（函館駅前22:46着）。夜は20分おきくらいになります。\n\n"
               "・荷物：泊まる日はホテルに預けるのが楽です。五稜郭タワーにもコインロッカーがあります（小300円・大500円、営業時間内）。",
               "· Tram: the Hakodate-ekimae stop is on the main road beyond the station plaza. Trams come about every 8 minutes in the daytime. Both routes, 2 and 5, go to Goryokaku-Koen-mae, Jujigai and Yunokawa-Onsen.\n\n"
               "· Fares: ¥250–300 by distance (from Hakodate-ekimae: Jujigai ¥250, Goryokaku-Koen-mae ¥270, Yunokawa-Onsen ¥290). You pay when you get off. Suica, Kitaca, ICOCA and other IC cards work: tap when you board and when you leave.\n\n"
               "· Day pass: ¥800, which roughly pays for itself after three rides. Buy it on the tram (ask the driver while it is stopped), at the tourist information centre inside the station, or at hotels near the station. There are also a smartphone version and a 24-hour pass (¥1,130).\n\n"
               "· Last trams: 21:46 from Yunokawa-Onsen (Hakodate-ekimae 22:16) and 22:40 from Jujigai (22:46). In the evening they run about every 20 minutes.\n\n"
               "· Luggage: leaving it at your hotel is easiest. Goryokaku Tower also has coin lockers (¥300 small, ¥500 large, during opening hours)."),
        gmaps=[gm("JR函館駅", "JR Hakodate Station", 41.773798, 140.726378, "JR函館駅"),
               gm("市電 函館駅前", "Hakodate-ekimae tram stop", 41.772355, 140.727866, "函館駅前 電停")],
        links=[TRAM, link("info", "市電のお得な乗車券", "Tram passes", U["tram_pass"]), JR],
        rows=[row("fee", "市電 1回250〜300円、1日乗車券800円", "Tram ¥250–300 a ride, day pass ¥800"),
              row("train", "市電は昼間およそ8分おき。最終は湯の川温泉21:46発、十字街22:40発", "Trams about every 8 minutes in the daytime. Last: 21:46 from Yunokawa-Onsen, 22:40 from Jujigai")],
        tip=T("市電の運賃・乗車券・ICカードは函館市（市電）の公式ページ、時刻は乗換案内の2026年12月3日（木）・5日（土）のダイヤで確認しました。年末年始は特別なダイヤです。",
              "Tram fares, passes and IC cards from the City of Hakodate’s tram pages; times from a route planner for 3 and 5 December 2026. A holiday timetable runs over New Year.")),

    asaichi=dict(
        name=T("函館朝市（はこだてあさいち）", "Hakodate Morning Market"), kind=T("市場・朝ごはん", "Market, breakfast"),
        blurb=T("駅のすぐ横の市場。海鮮丼の食堂が集まる「どんぶり横丁市場」と、イカ・カニ・干物の店が並びます。",
                "A market beside the station: seafood-bowl restaurants in the Donburi Yokocho hall, and stalls of squid, crab and dried fish."),
        lat=41.772239, lng=140.724817,
        caution=T("14時すぎには閉まります。昼をすぎると片付けを始める店があります", "It closes soon after 14:00; some stalls start packing up after noon"),
        body=T("市場が開くのは、1〜4月は6:00、5〜12月は5:00。閉まるのは14:00すぎです。店ごとに休みと時間が違います。\n\n"
               "食堂は駅に近い「どんぶり横丁市場」に集まっています。店の前に写真つきのメニューと値段が出ているので、何軒か見てから決められます。イクラ・ウニ・ホタテなど、のせるものを選べる店が多く、焼き魚の定食もあります。\n\n"
               "声をかけてくる店もありますが、断って大丈夫です。カニやメロンは値段を聞いてから。現金のほうが確実です。\n\n"
               "8〜10時は団体の人で混みます。7時前か、10時半すぎが歩きやすい時間です。",
               "The market opens at 6:00 from January to April and 5:00 from May to December, and closes soon after 14:00. Each stall keeps its own days and hours.\n\n"
               "The restaurants are gathered in the Donburi Yokocho hall on the station side. Menus with photos and prices are posted outside, so look at a few before choosing. Many let you pick the toppings (salmon roe, sea urchin, scallops), and there are grilled-fish set meals too.\n\n"
               "Some stallholders call out to you; it is fine to say no. Ask the price before buying crab or melon. Cash is the safe choice.\n\n"
               "Tour groups fill the market from 8 to 10. Before 7:00 or after 10:30 is easier."),
        gmaps=[gm("函館朝市", "Hakodate Morning Market", 41.772239, 140.724817, "函館朝市"),
               gm("どんぶり横丁市場", "Donburi Yokocho", 41.77285, 140.72575, "函館朝市 どんぶり横丁市場")],
        links=[link("official", "函館朝市（公式）", "Hakodate Morning Market (official)", U["asaichi"])],
        rows=[row("hours", "1〜4月 6:00〜14:00すぎ、5〜12月 5:00〜14:00すぎ（店ごとに違う）", "Jan–Apr 6:00–about 14:00, May–Dec 5:00–about 14:00 (varies by stall)")],
        tip=T("時間は函館朝市の公式サイトで確認しました。食堂ごとの時間と支払い方法は確認していません（要確認）。混む時間は一般的な目安です。",
              "Hours from the market’s official site. Individual restaurants’ hours and payment methods were not checked (please check). Busy times are a general guide.")),

    tower=dict(
        name=T("五稜郭（ごりょうかく）タワー", "Goryokaku Tower"), kind=T("展望台", "Observation tower"),
        blurb=T("星の形は、上から見ないと分かりません。先にタワーに上ってから、公園を歩きます。",
                "You only see the star from above. Go up the tower first, then walk the park."),
        lat=41.794591, lng=140.753958,
        body=T("市電「五稜郭公園前」から歩いて15分ほど。電停から大きな通りを北へまっすぐです。\n\n"
               "展望台から、堀に囲まれた星の形の城の跡がそのまま見えます。冬は雪で白い星、5月のはじめは桜で堀のふちがピンクになります。函館山と海も反対側に見えます。\n\n"
               "9:00〜18:00、休みなし。チケットは17:50まで。1階にコインロッカーがあります（小300円・大500円）。\n\n"
               "12月1日〜2月28日は、日の入りから19:00（予定）まで堀に明かりがつく「五稜星の夢（ほしのゆめ）」。函館山が雲で見えない日は、夕方にここへ来る手もあります。",
               "About 15 minutes on foot from the Goryokaku-Koen-mae tram stop: straight north along the main road.\n\n"
               "From the deck you see the whole star-shaped fort and its moat. In winter it is a white star in the snow; in early May cherry blossom turns the edge of the moat pink. Mt. Hakodate and the sea are on the other side.\n\n"
               "Open 9:00–18:00 every day; tickets until 17:50. There are coin lockers on the ground floor (¥300 small, ¥500 large).\n\n"
               "From 1 December to 28 February the moat is outlined in lights from sunset until 19:00 (planned). On a day when Mt. Hakodate is in cloud, coming here at dusk is a good alternative."),
        gmaps=[gm("五稜郭タワー", "Goryokaku Tower", 41.794591, 140.753958, "五稜郭タワー"),
               gm("市電 五稜郭公園前", "Goryokaku-Koen-mae tram stop", 41.789161, 140.752887, "五稜郭公園前 電停")],
        links=[link("official", "五稜郭タワー（料金・営業時間）", "Goryokaku Tower (official)", U["tower"], U["tower_en"]), TRAM],
        rows=[row("hours", "9:00〜18:00（チケットは17:50まで）、休みなし", "9:00–18:00 (tickets until 17:50), open every day"),
              row("fee", "大人1,200円、中高生900円、小学生600円", "Adults ¥1,200, ages 12–18 ¥900, ages 6–12 ¥600")],
        tip=T("時間・料金は五稜郭タワーの公式サイト、明かりの期間は函館市の公式観光サイトで確認しました。",
              "Hours and prices from the tower’s official site; the light-up dates from the city’s official tourism site.")),

    goryokaku=dict(
        name=T("五稜郭公園と箱館奉行所（はこだてぶぎょうしょ）", "Goryokaku Park and the Magistrate’s Office"), kind=T("城の跡・公園", "Fort, park"),
        blurb=T("堀を渡って星の中へ。まん中に、江戸時代の役所を木で建て直した箱館奉行所があります。",
                "Cross the moat into the star. In the middle stands the Magistrate’s Office, rebuilt in timber as it was in the Edo period."),
        lat=41.796933, lng=140.756725,
        caution=T("奉行所は靴を脱いで入ります。11〜3月は受付16:45まで", "Shoes off inside the Magistrate’s Office. Last entry 16:45 from November to March"),
        body=T("タワーの前の橋から堀を渡ります。公園は無料で、いつでも歩けます。土手の上に上がると、堀と石垣の角ばった形がよく分かります。\n\n"
               "箱館奉行所は、靴を脱いで入る木の建物です。冬は床が冷たいので、厚い靴下で。大きな荷物は持ち込めません。中は30〜40分で見られます。\n\n"
               "冬は堀が凍り、土手の道は踏み固めた雪になります。滑るので、土手の上は無理をしないでください。",
               "Cross the moat by the bridge in front of the tower. The park is free and always open. From the top of the earthworks you can see the angles of the moat and stone walls.\n\n"
               "The Magistrate’s Office is a timber building you enter without shoes. The floors are cold in winter, so wear thick socks. Large bags are not allowed in. Allow 30–40 minutes inside.\n\n"
               "In winter the moat freezes and the paths on the earthworks are packed snow. They are slippery; skip the top if it looks icy."),
        gmaps=[gm("箱館奉行所", "Hakodate Magistrate’s Office", 41.796933, 140.756725, "箱館奉行所")],
        links=[link("official", "箱館奉行所（時間・料金・休館日）", "Hakodate Magistrate’s Office (official)", U["bugyo"])],
        rows=[row("hours", "奉行所 4〜10月 9:00〜18:00（受付17:45まで）、11〜3月 9:00〜17:00（受付16:45まで）", "Magistrate’s Office: Apr–Oct 9:00–18:00 (entry until 17:45), Nov–Mar 9:00–17:00 (entry until 16:45)"),
              row("fee", "奉行所 一般500円。公園は無料", "Magistrate’s Office ¥500. The park is free"),
              row("closed", "奉行所は12月31日〜1月3日休み（ほかに臨時休館あり）", "Magistrate’s Office closed 31 Dec–3 Jan (and occasional extra days)")],
        tip=T("箱館奉行所の公式サイトで確認しました。支払い方法は確認していません（要確認）。",
              "From the Magistrate’s Office official site. Payment methods were not checked (please check).")),

    hiru=dict(
        name=T("五稜郭でお昼", "Lunch at Goryokaku"), kind=T("お昼", "Lunch"),
        blurb=T("タワーのすぐ近くに、函館の塩ラーメンと、函館だけのハンバーガーの店があります。",
                "Right by the tower: Hakodate’s salt-broth ramen, and a burger chain found only around Hakodate."),
        lat=41.794342, lng=140.753182,
        caution=T("あじさい本店は第4水曜休み", "Ajisai’s main shop closes on the fourth Wednesday"),
        body=T("・函館麺厨房あじさい 本店：澄んだスープの塩ラーメン。11:00〜20:25（ラストオーダー）、第4水曜休み（祝日なら次の平日）。タワーの向かいです。\n\n"
               "・ラッキーピエロ 五稜郭公園前店：函館のあたりにしかないハンバーガーの店。甘辛い鶏のから揚げをはさんだバーガーが看板です。9:30〜22:00（ラストオーダー21:30）。注文してから作るので、混む時間は20分ほど待ちます。\n\n"
               "どちらも12時台は並びます。少し早めか、13時すぎが入りやすい時間です。写真はラッキーピエロの別の店舗です。",
               "· Hakodate Menchubo Ajisai, main shop: shio (salt) ramen in a clear broth. 11:00–20:25 (last order), closed on the fourth Wednesday (the next weekday if that is a holiday). Opposite the tower.\n\n"
               "· Lucky Pierrot, Goryokaku-Koen-mae branch: a burger chain that exists only around Hakodate. The signature burger has sweet-and-salty fried chicken. 9:30–22:00 (last order 21:30). Food is made to order, so expect about 20 minutes at busy times.\n\n"
               "Both have queues around noon. Slightly early, or after 13:00, is easier. The photo shows a different Lucky Pierrot branch."),
        gmaps=[gm("あじさい 本店", "Ajisai main shop", 41.79455, 140.75345, "函館麺厨房あじさい 本店"),
               gm("ラッキーピエロ 五稜郭公園前店", "Lucky Pierrot Goryokaku-Koen-mae", 41.794342, 140.753182, "ラッキーピエロ 五稜郭公園前店")],
        links=[link("official", "函館麺厨房あじさい（店舗）", "Ajisai (shops)", U["ajisai"]),
               link("official", "ラッキーピエロ 五稜郭公園前店", "Lucky Pierrot Goryokaku-Koen-mae", U["lp_goryo"])],
        rows=[row("hours", "あじさい本店 11:00〜20:25（ラストオーダー）", "Ajisai main shop 11:00–20:25 (last order)"),
              row("hours", "ラッキーピエロ 五稜郭公園前店 9:30〜22:00（ラストオーダー21:30）", "Lucky Pierrot 9:30–22:00 (last order 21:30)"),
              row("closed", "あじさい本店 第4水曜（祝日なら次の平日）", "Ajisai main shop: fourth Wednesday (next weekday if a holiday)")],
        tip=T("時間と休みは、それぞれの店の公式サイトで確認しました。値段・支払い方法・英語のメニューがあるかは確認していません（要確認）。混む時間は一般的な目安です。",
              "Hours and closing days from each shop’s official site. Prices, payment methods and English menus were not checked (please check). Busy times are a general guide.")),

    hachiman=dict(
        name=T("八幡坂（はちまんざか）と元町の坂", "Hachiman-zaka and the Motomachi slopes"), kind=T("坂道・町歩き", "Slopes, old town"),
        blurb=T("石だたみの坂が、まっすぐ港へ下りていきます。坂の上から海と船を見下ろせます。",
                "A stone-paved slope running straight down to the harbour. From the top you look down on the sea and the ships."),
        lat=41.764723, lng=140.712741,
        body=T("市電「十字街」か「末広町」から、坂を歩いて上って10分ほど。坂のいちばん上が、写真でよく見る場所です。\n\n"
               "車が通る道です。道のまん中に立って写真を撮る人がいますが、車が来ます。歩道から撮ってください。\n\n"
               "となりの大三坂（だいさんざか）は、石だたみと並木の静かな坂で、上ると教会の前に出ます。八幡坂を上り、坂の上の道を歩いて、大三坂や基坂（もといざか）を下りると、同じ道を戻らずに回れます。\n\n"
               "冬は石だたみが凍ります。坂の端の、砂をまいてあるところを歩いてください。12月1日〜2月28日は並木に明かりがつきます（日の入り〜22:00の予定）。",
               "About 10 minutes uphill from the Jujigai or Suehirocho tram stops. The very top of the slope is the view you have seen in photos.\n\n"
               "It is a road with traffic. People stand in the middle for photos, but cars do come: shoot from the pavement.\n\n"
               "Daisan-zaka, the next slope, is quieter, with stone paving and trees, and leads up to the churches. Go up Hachiman-zaka, walk along the top and come down Daisan-zaka or Motoi-zaka, and you never retrace your steps.\n\n"
               "The paving freezes in winter. Walk at the edge where grit has been spread. From 1 December to 28 February the trees are lit (sunset to 22:00, planned)."),
        gmaps=[gm("八幡坂", "Hachiman-zaka", 41.764723, 140.712741, "八幡坂 函館"),
               gm("市電 十字街", "Jujigai tram stop", 41.764344, 140.719281, "十字街 電停 函館")],
        links=[link("info", "冬のイルミネーション（函館市公式観光サイト）", "Winter lights (city tourism site)", U["lights"]), TRAM],
        rows=[row("fee", "無料", "Free")],
        tip=T("イルミネーションの期間は函館市の公式観光サイトで確認しました。歩く時間は地図からの目安です。",
              "Light-up dates from the city’s official tourism site. Walking times are estimates from the map.")),

    kokaido=dict(
        name=T("旧函館区公会堂（きゅうはこだてくこうかいどう）", "Old Public Hall of Hakodate Ward"), kind=T("洋館", "Western-style hall"),
        blurb=T("坂の上に建つ、水色と黄色の木造の洋館。2階のバルコニーから港が見えます。",
                "A blue-grey and yellow wooden hall at the top of the hill, built in 1910. The upstairs balcony looks over the harbour."),
        lat=41.765037, lng=140.708920,
        caution=T("11〜3月は17:00まで（入館は16:30まで）", "November–March: until 17:00 (last entry 16:30)"),
        body=T("1910年にできた、町の集会所です。大広間と、当時の家具を置いた部屋を見られます。2階のバルコニーに出ると、元町の屋根の向こうに港が見えます。\n\n"
               "八幡坂の上から、坂の上の道を西へ歩いて5分ほど。下の元町公園からも、建物の正面がよく見えます。中に入らない日も、公園から見上げてください。\n\n"
               "中は30分ほどで見られます。",
               "Built in 1910 as the town’s assembly hall. You can see the ballroom and rooms with furniture of the time. From the upstairs balcony the harbour shows beyond the roofs of Motomachi.\n\n"
               "About 5 minutes west along the top road from Hachiman-zaka. The front of the building is also well seen from Motomachi Park below, even on a day you do not go in.\n\n"
               "Allow about 30 minutes inside."),
        gmaps=[gm("旧函館区公会堂", "Old Public Hall of Hakodate Ward", 41.765037, 140.708920, "旧函館区公会堂")],
        links=[link("official", "旧函館区公会堂（公式）", "Old Public Hall (official)", U["kokaido"])],
        rows=[row("hours", "4〜10月 9:00〜18:00（土〜月は19:00まで）、11〜3月 9:00〜17:00。入館は終わる30分前まで", "Apr–Oct 9:00–18:00 (Sat–Mon until 19:00), Nov–Mar 9:00–17:00. Last entry 30 minutes before closing"),
              row("fee", "一般300円", "Adults ¥300"),
              row("closed", "12月31日〜1月3日、2027年1月26日（点検）", "31 Dec–3 Jan; 26 Jan 2027 (maintenance)")],
        tip=T("旧函館区公会堂の公式サイトで確認しました。支払い方法は確認していません（要確認）。",
              "From the hall’s official site. Payment methods were not checked (please check).")),

    haris=dict(
        name=T("函館ハリストス正教会と元町の教会", "Hakodate Orthodox Church and the Motomachi churches"), kind=T("教会", "Churches"),
        blurb=T("白い壁に緑の屋根の、ロシア正教の教会。まわりにカトリックと聖公会の教会が並びます。",
                "A white Russian Orthodox church with green roofs. A Catholic and an Anglican church stand close by."),
        lat=41.762844, lng=140.712212,
        caution=T("聖堂の中は撮影できません。日曜は13:00から。12月25日〜2月末は中に入れません", "No photos inside. Sundays from 13:00. No visits inside from 25 December to the end of February"),
        body=T("1860年に、日本で最初の正教会の聖堂が建てられた場所です。今も毎週お祈りが行われている教会なので、中では静かに。聖堂の中の撮影はできません。拝観のときに献金（大人200円）をお願いされます。\n\n"
               "外から見るだけでも来る価値があります。大三坂を上ると、カトリック元町教会のとがった塔、その先にハリストス正教会、すぐ近くに聖ヨハネ教会があります。チャチャ登りという細い坂を少し上ると、3つの教会の屋根と港がいっしょに見えます。\n\n"
               "ロープウェイの山麓駅まで、ここから歩いて5分です。",
               "This is where Japan’s first Orthodox church was built, in 1860. Services are still held here every week, so be quiet inside. Photography inside is not allowed. Visitors are asked for a donation (¥200 for adults).\n\n"
               "It is worth coming just for the outside. Climbing Daisan-zaka you pass the pointed tower of the Motomachi Catholic Church, then the Orthodox church, with St. John’s Church close by. A little way up the narrow lane called Chacha-nobori you see the roofs of all three with the harbour beyond.\n\n"
               "The ropeway’s lower station is 5 minutes on foot from here."),
        gmaps=[gm("函館ハリストス正教会", "Hakodate Orthodox Church", 41.762844, 140.712212, "函館ハリストス正教会"),
               gm("カトリック元町教会", "Motomachi Catholic Church", 41.763257, 140.713160, "カトリック元町教会 函館")],
        links=[link("official", "函館ハリストス正教会（拝観の案内）", "Hakodate Orthodox Church (visiting)", U["haris"])],
        rows=[row("hours", "拝観 月〜金 10:00〜17:00（11・12・3月は16:00まで）、土 10:00〜16:00、日 13:00〜16:00", "Visits: Mon–Fri 10:00–17:00 (until 16:00 in Nov, Dec, Mar), Sat 10:00–16:00, Sun 13:00–16:00"),
              row("fee", "拝観献金 大人200円、中学生100円", "Donation: adults ¥200, ages 12–15 ¥100"),
              row("closed", "12月25日〜2月末は拝観休止。行事やお葬式のときも入れません", "No visits 25 Dec–end of Feb, nor during church events and funerals")],
        tip=T("函館ハリストス正教会の公式サイトで確認しました。ほかの2つの教会の中の見学は確認していません（要確認）。",
              "From the church’s official site. Whether the other two churches can be visited inside was not checked (please check).")),

    ropeway=dict(
        name=T("函館山（はこだてやま）ロープウェイと夜景", "Mt. Hakodate Ropeway and the night view"), kind=T("夜景・ロープウェイ", "Night view, ropeway"),
        blurb=T("両側を海にはさまれた町の明かり。日の入りの30分前に上がって、暗くなるまで待ちます。",
                "The lights of a town pinched between two seas. Go up 30 minutes before sunset and wait for dark."),
        lat=41.760920, lng=140.714177,
        caution=T("日の入りの30〜40分前の便で上へ。強い風の日は止まります", "Ride up 30–40 minutes before sunset. It stops in strong wind"),
        body=T("山麓駅は、市電「十字街」から坂を上って10分。ロープウェイは15分おき（混むと5〜10分おき）で、山頂まで3分です。往復1,800円。カード・電子マネーが使えます。\n\n"
               "いちばんきれいなのは、日の入りの20〜30分あと。空に青みが残って、町の明かりがそろう時間です。ただ、その時間に上ろうとすると、山麓駅で長く並びます。日の入りの30〜40分前に上がって、展望台の手すりの前で待つのが確実です。待つあいだは風が冷たいので、冬は手袋と帽子を。中にも窓ぎわの席があります。\n\n"
               "いつ上がるかの目安（日の入りは函館の位置から計算した時刻）：\n" + ROPE_SEASON_JA + "\n\n"
               "下りも、暗くなって30分ほどたつと行列になります。十分に見たら、早めに下りの列へ。\n\n"
               "山に雲がかかると、何も見えません。上がる前に、公式サイトの「運行状況と函館山」のライブカメラを見てください。強い風の日は止まります。\n\n"
               "冬（11月9日〜4月12日）は山頂への道路が通行止めで、バスとタクシーは使えません。ロープウェイだけです。",
               "The lower station is 10 minutes uphill from the Jujigai tram stop. Cars leave every 15 minutes (every 5–10 when busy) and take 3 minutes. Return ¥1,800; cards and e-money accepted.\n\n"
               "The best moment is 20–30 minutes after sunset, with some blue left in the sky and the town fully lit. But if you try to ride up then, you queue for a long time at the bottom. Going up 30–40 minutes before sunset and waiting at the railing is the sure way. The wind is cold while you wait: bring gloves and a hat in winter. There are window seats indoors too.\n\n"
               "When to ride up (sunset times calculated for Hakodate):\n" + ROPE_SEASON_EN + "\n\n"
               "The queue to come down builds about 30 minutes after dark. Once you have seen enough, join it early.\n\n"
               "If cloud sits on the mountain you see nothing. Check the live camera on the official site before going up. The ropeway stops in strong wind.\n\n"
               "In winter (9 November–12 April) the summit road is closed, so there are no buses or taxis to the top: the ropeway is the only way."),
        gmaps=[gm("函館山ロープウェイ 山麓駅", "Ropeway lower station", 41.760920, 140.714177, "函館山ロープウェイ 山麓駅")],
        links=[RW, link("info", "山頂の混み具合（函館市）", "How busy the summit is (city live map)", U["vacan"])],
        rows=[row("hours", "10/1〜4/19 10:00〜（上りの最終20:30、下りの最終21:00）。4/20〜9/30 上りの最終21:30、下りの最終22:00", "1 Oct–19 Apr: from 10:00, last up 20:30, last down 21:00. 20 Apr–30 Sep: last up 21:30, last down 22:00"),
              row("fee", "往復 大人1,800円、子ども900円（片道1,200円）", "Return: adults ¥1,800, children ¥900 (one way ¥1,200)")],
        tip=T("時間・料金・運休は函館山ロープウェイの公式サイト、道路の通行止めは函館市の公式観光サイトで確認しました。日の入りは函館の緯度・経度から計算した時刻で、数分のずれがあります。並ぶ時間は日によって違います。",
              "Hours, fares and closures from the ropeway’s official site; the road closure from the city’s tourism site. Sunset times are calculated from Hakodate’s position and may be a few minutes off. Queues vary by day.")),

    kanemori=dict(
        name=T("金森（かねもり）赤レンガ倉庫とベイエリア", "Kanemori Red Brick Warehouses and the bay"), kind=T("倉庫・買い物", "Warehouses, shops"),
        blurb=T("港に並ぶ赤いレンガの倉庫。中は店とビヤホールで、夜は壁に明かりが当たります。",
                "Red-brick warehouses along the harbour, now shops and a beer hall, floodlit after dark."),
        lat=41.766306, lng=140.716843,
        body=T("市電「十字街」から歩いて5分。倉庫のあいだの運河と、海ぞいの道を歩けます。店は9:30〜19:00。ガラス、オルゴール、お菓子などの店が入っています。\n\n"
               "写真は、七財橋（しちざいばし）のあたりから運河ごしに倉庫を見るのと、海側から函館山を背景に見るのがきれいです。暗くなると倉庫に明かりが当たり、雪の日は特に静かです。\n\n"
               "倉庫の中の函館ビヤホールは、平日11:30から、土日祝11:00から21:30まで（ラストオーダー21:00）。寒い日の休憩にも使えます。\n\n"
               "函館駅までは、海ぞいを歩いて15〜20分。市電なら十字街から6分です。",
               "Five minutes on foot from the Jujigai tram stop. You can walk the canal between the warehouses and the path along the water. Shops open 9:30–19:00: glass, music boxes, sweets.\n\n"
               "For photos, look across the canal from around Shichizai Bridge, or from the water side with Mt. Hakodate behind. After dark the walls are floodlit; on a snowy night it is very quiet.\n\n"
               "Hakodate Beer Hall, inside one of the warehouses, opens from 11:30 on weekdays and 11:00 at weekends until 21:30 (last order 21:00). It is also a place to warm up.\n\n"
               "Hakodate Station is 15–20 minutes on foot along the water, or 6 minutes by tram from Jujigai."),
        gmaps=[gm("金森赤レンガ倉庫", "Kanemori Red Brick Warehouses", 41.766306, 140.716843, "金森赤レンガ倉庫")],
        links=[link("official", "金森赤レンガ倉庫（公式）", "Kanemori Red Brick Warehouses (official)", U["kanemori"]),
               link("info", "はこだてクリスマスファンタジー", "Hakodate Christmas Fantasy", U["xmas"])],
        rows=[row("hours", "店 9:30〜19:00、休みなし。函館ビヤホール 平日11:30〜・土日祝11:00〜21:30（ラストオーダー21:00）", "Shops 9:30–19:00, every day. Beer hall from 11:30 (weekends 11:00) to 21:30 (last order 21:00)"),
              row("fee", "入るのは無料", "Free to enter")],
        tip=T("時間は金森赤レンガ倉庫の公式サイト、クリスマスの日程は公式サイトで確認しました。",
              "Hours from the warehouses’ official site; Christmas dates from the event’s official site.")),

    yunokawa=dict(
        name=T("湯の川（ゆのかわ）温泉", "Yunokawa Onsen"), kind=T("温泉・足湯", "Hot spring, foot bath"),
        blurb=T("市電の終点の近くにある温泉街。電停の前に無料の足湯、ホテルに日帰りのお風呂があります。",
                "A hot-spring district near the end of the tram line: a free foot bath by the stop, and day-visit baths at the hotels."),
        lat=41.779614, lng=140.785680,
        caution=T("日帰り入浴のタトゥーの決まりは、公式サイトに書かれていません（要確認）。足湯はだれでも入れます", "Tattoo rules for the day baths are not on the official sites (please check). The foot bath is open to everyone"),
        body=T("・足湯「湯巡り舞台（ゆめぐりぶたい）」：市電「湯の川温泉」を降りてすぐ。無料で、毎日9:00〜21:00。足だけなので、タトゥーがあっても関係ありません。足をふくタオルを持っていってください。\n\n"
               "・日帰りのお風呂（湯の川温泉旅館協同組合の一覧から）：ホテル雨宮館（あめみやかん）800円・6:00〜22:00、KKRはこだて 1,000円・11:00〜21:00、ホテルテトラ湯の川温泉 550円・13:00〜22:00、湯元 啄木亭（たくぼくてい）1,200円・13:00〜21:00（タオル貸し出し300円）。休む日や時間が変わる日があります。\n\n"
               "・タトゥー：どの施設の公式サイトにも、タトゥーの決まりは書かれていませんでした。タトゥーのある人は、行く前に電話で聞くか、入口で確かめてください。\n\n"
               "・お風呂の入り方：服は脱衣所で全部脱ぎます。体を洗ってから湯ぶねへ。タオルは湯に入れません。水着は使いません。\n\n"
               "・函館市熱帯植物園：電停から海のほうへ歩いて15分。12月から5月の連休ごろまで、サル山のサルが温泉に入ります。一般300円、11〜3月は9:30〜16:30。昼間に湯の川へ来る日に。\n\n"
               "・トラピスチヌ修道院：湯の川からさらにバスで山のほうへ。前庭と資料室を見られます（無料、12〜2月は9:00〜16:00）。「トラピスチヌ入口」バス停から歩いて10分。バスの時刻は確かめていません（要確認）。",
               "· Foot bath “Yumeguri Butai”: right by the Yunokawa-Onsen tram stop. Free, every day 9:00–21:00. Only your feet go in, so tattoos do not matter. Bring a small towel to dry your feet.\n\n"
               "· Day baths (from the Yunokawa ryokan association’s list): Hotel Amemiyakan ¥800, 6:00–22:00; KKR Hakodate ¥1,000, 11:00–21:00; Hotel Tetora Yunokawa Onsen ¥550, 13:00–22:00; Yumoto Takubokutei ¥1,200, 13:00–21:00 (towel rental ¥300). Days and hours can change.\n\n"
               "· Tattoos: none of these places states a tattoo rule on its official site. If you have tattoos, phone ahead or ask at the entrance before paying.\n\n"
               "· How to bathe: undress completely in the changing room, wash before getting into the bath, and keep your towel out of the water. No swimwear.\n\n"
               "· Hakodate Tropical Botanical Garden: 15 minutes on foot towards the sea. From December until around early May the monkeys sit in their own hot spring. Adults ¥300; November–March 9:30–16:30. For a day when you come to Yunokawa in daylight.\n\n"
               "· Trappistine Convent: further inland by bus. The front garden and a small exhibition room are open (free; December–February 9:00–16:00), 10 minutes on foot from the Trappistine-iriguchi bus stop. Bus times were not checked (please check)."),
        gmaps=[gm("足湯 湯巡り舞台", "Yumeguri Butai foot bath", 41.779614, 140.785680, "湯の川温泉足湯 湯巡り舞台"),
               gm("函館市熱帯植物園", "Tropical Botanical Garden", 41.774149, 140.789321, "函館市熱帯植物園"),
               gm("ホテル雨宮館", "Hotel Amemiyakan", 41.780819, 140.783906, "湯の川温泉 ホテル雨宮館")],
        links=[link("official", "湯の川温泉 日帰り温泉の一覧", "Yunokawa day baths (association list)", U["yu_day"], U["yu_en"]),
               link("official", "函館市熱帯植物園", "Hakodate Tropical Botanical Garden", U["eco"]),
               link("info", "トラピスチヌ修道院（函館市公式観光サイト）", "Trappistine Convent (city tourism site)", U["trap"])],
        rows=[row("hours", "足湯 9:00〜21:00（無料）", "Foot bath 9:00–21:00 (free)"),
              row("fee", "日帰り入浴 550〜1,200円（施設による）", "Day baths ¥550–1,200 depending on the place"),
              row("train", "市電 湯の川温泉→函館駅前 約30分・290円。最終21:46発", "Tram Yunokawa-Onsen → Hakodate-ekimae about 30 min, ¥290. Last tram 21:46")],
        tip=T("日帰り入浴の料金と時間は湯の川温泉旅館協同組合の公式サイト、熱帯植物園は公式サイト、トラピスチヌ修道院は函館市の公式観光サイトで確認しました。タトゥーの決まりと、タオルを借りられるか（啄木亭以外）は確認できていません（要確認）。",
              "Bath prices and hours from the Yunokawa ryokan association’s site; the garden from its own site; the convent from the city’s tourism site. Tattoo rules and towel rental (other than Takubokutei) could not be confirmed (please check).")),

    yuhan=dict(
        name=T("晩ごはん：ベイエリアと大門横丁（だいもんよこちょう）", "Dinner: the bay area and Daimon Yokocho"), kind=T("晩ごはん", "Dinner"),
        blurb=T("赤レンガ倉庫のまわりか、函館駅から歩いて5分の屋台の横丁で。",
                "Around the warehouses, or in the lane of small food stalls 5 minutes’ walk from the station."),
        lat=41.772393, lng=140.730001,
        caution=T("大門横丁は基本は現金です", "Daimon Yokocho is mostly cash only"),
        body=T("【ベイエリア（赤レンガ倉庫のまわり）】\n"
               "・函館ビヤホール（金森赤レンガ倉庫の中）：21:30まで（ラストオーダー21:00）。\n"
               "・函館麺厨房あじさい 紅（くれない）店：塩ラーメン。11:00〜21:30（ラストオーダー）。\n"
               "・ラッキーピエロ ベイエリア本店：10:00〜21:00（ラストオーダー20:30）。\n\n"
               "【函館駅の近く】\n"
               "・函館ひかりの屋台 大門横丁：小さな店が26軒並ぶ屋台の横丁。カウンターだけの店が多く、1〜2人で入りやすい場所です。海鮮、ラーメン、焼き鳥、ジンギスカンなど。時間と休みは店ごとに違い、支払いは基本は現金です。公式サイトに店ごとの案内があります。\n"
               "・ラッキーピエロ 函館駅前店：8:00〜22:00（ラストオーダー21:30）。遅くなった日に。\n\n"
               "イカは函館の名物ですが、とれない日・時期があります。店で聞いてください。\n\n"
               "ベイエリアから駅へは、市電「十字街」から6分（最終22:40発）。歩くと15〜20分です。",
               "[Bay area, around the warehouses]\n"
               "· Hakodate Beer Hall (inside the Kanemori warehouses): until 21:30 (last order 21:00).\n"
               "· Hakodate Menchubo Ajisai, Kurenai branch: shio ramen. 11:00–21:30 (last order).\n"
               "· Lucky Pierrot Bay Area main shop: 10:00–21:00 (last order 20:30).\n\n"
               "[Near Hakodate Station]\n"
               "· Hakodate Hikari no Yatai Daimon Yokocho: a lane of 26 tiny food stalls. Most are counter-only, so easy for one or two people. Seafood, ramen, grilled chicken, grilled lamb and more. Hours and days off differ by stall and payment is mostly cash. The official site lists each stall.\n"
               "· Lucky Pierrot Hakodate-ekimae: 8:00–22:00 (last order 21:30). Useful on a late night.\n\n"
               "Squid is Hakodate’s speciality, but there are days and seasons with no catch. Ask at the restaurant.\n\n"
               "From the bay to the station: 6 minutes by tram from Jujigai (last tram 22:40), or 15–20 minutes on foot."),
        gmaps=[gm("大門横丁", "Daimon Yokocho", 41.772393, 140.730001, "函館ひかりの屋台 大門横丁"),
               gm("金森赤レンガ倉庫（函館ビヤホール）", "Kanemori warehouses (Beer Hall)", 41.766306, 140.716843, "函館ビヤホール"),
               gm("ラッキーピエロ ベイエリア本店", "Lucky Pierrot Bay Area", 41.765794, 140.714894, "ラッキーピエロ ベイエリア本店")],
        links=[link("official", "函館ひかりの屋台 大門横丁", "Daimon Yokocho (official)", U["yatai"]),
               link("official", "函館麺厨房あじさい（店舗）", "Ajisai (shops)", U["ajisai"]),
               link("official", "ラッキーピエロ ベイエリア本店", "Lucky Pierrot Bay Area", U["lp_bay"])],
        rows=[row("hours", "函館ビヤホール 21:30まで（ラストオーダー21:00）。あじさい紅店 21:30ラストオーダー。大門横丁は店ごと", "Beer Hall until 21:30 (last order 21:00). Ajisai Kurenai last order 21:30. Daimon Yokocho varies by stall")],
        tip=T("時間は、それぞれの公式サイトで確認しました。値段・英語のメニュー・カードが使えるかは確認していません（要確認）。",
              "Hours from each official site. Prices, English menus and card payment were not checked (please check).")),

    kaeri=dict(
        name=T("函館駅から札幌へ", "Back to Sapporo from Hakodate Station"), kind=T("駅・帰り", "Station, return"),
        blurb=T("特急北斗19号は17:55発、札幌21:41着。最終は18:43発です。",
                "Hokuto 19 leaves at 17:55 and reaches Sapporo at 21:41. The last train is at 18:43."),
        lat=41.773798, lng=140.726378,
        body=T("帰りも全部の席が指定席です。行きのきっぷを買うときに、帰りの席もいっしょに取っておくと安心です。\n\n"
               "・北斗15号 15:01発 → 札幌18:47着\n・北斗19号 17:55発 → 札幌21:41着\n・北斗21号 18:43発 → 札幌22:41着（最終）\n\n"
               "最終のあとは、その日のうちに札幌へ帰る列車がありません。雪で遅れる日もあるので、最終より1本前にしておくと安心です。\n\n"
               "駅の中にお弁当とお土産の店があります。朝市は14時すぎに閉まるので、市場で買うものは朝のうちに。",
               "Every seat is reserved on the way back too. It is safest to book the return seat when you buy the outbound ticket.\n\n"
               "· Hokuto 15: 15:01 → Sapporo 18:47\n· Hokuto 19: 17:55 → Sapporo 21:41\n· Hokuto 21: 18:43 → Sapporo 22:41 (last train)\n\n"
               "After the last train there is nothing to Sapporo that day. Snow can cause delays, so taking the one before the last is the safer choice.\n\n"
               "There are shops for boxed meals and souvenirs inside the station. The morning market closes soon after 14:00, so buy anything from there in the morning."),
        gmaps=[gm("JR函館駅", "JR Hakodate Station", 41.773798, 140.726378, "JR函館駅")],
        links=[JR],
        rows=[row("train", "函館17:55→札幌21:41（北斗19号）。最終は18:43→22:41。早いのは15:01→18:47", "Hakodate 17:55 → Sapporo 21:41 (Hokuto 19). Last: 18:43 → 22:41. Earlier: 15:01 → 18:47"),
              row("fee", "函館→札幌 9,770円（乗車券6,600円＋指定席3,170円）", "Hakodate → Sapporo ¥9,770 (fare ¥6,600 + reserved seat ¥3,170)")],
        tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました。春のダイヤ改正のあとは確かめ直してください。",
              "Times and fares from a route planner for 3 and 5 December 2026; check again after the spring timetable change.")),
)

# ---------------------------------------------------------------------------
# コースごとの時間割
#   pre: 名前のすぐ下に出る段落、time: いちばん下の行、notices・rows・caution・blurb・name は共通部分に足す／入れ替える
# ---------------------------------------------------------------------------
LATE = dict(
    file="hakodate.json", course="late",
    order=["eki", "asaichi", "tower", "goryokaku", "hiru", "hachiman", "kokaido", "haris", "ropeway", "kanemori", "yunokawa", "yuhan"],
    spots=dict(
        eki=dict(
            pre=T("9:30にホテルを出て、まず駅の横の朝市で朝ごはん。市電で五稜郭へ行ってタワーと公園、お昼を食べてから市電で元町へ。坂と教会を歩いて、日の入りの30分前にロープウェイで函館山へ上がります。下りてから、明かりのついた赤レンガ倉庫と晩ごはん。\n\n"
                  "冬（12〜1月）の日の入りに合わせた時間割です。日の長い季節は、元町をゆっくり歩いて晩ごはんを先にします（函館山のスポットに目安）。市電に3回乗るので、最初に1日乗車券（800円）を買うと楽です。",
                  "Leave your hotel at 9:30 and start with breakfast at the market beside the station. Take the tram to Goryokaku for the tower and the park, eat lunch, then ride to Motomachi. Walk the slopes and churches and take the ropeway up Mt. Hakodate 30 minutes before sunset. After coming down: the floodlit warehouses and dinner.\n\n"
                  "This timetable follows December–January sunsets. In the long days of summer, take Motomachi slowly and eat dinner first (see the Mt. Hakodate stop). You ride the tram three times, so a day pass (¥800) at the start makes things simple."),
            notices=[N_WINTER_WALK, N_YEAREND],
            time=(DEP, "9:30", "9:30")),
        asaichi=dict(
            pre=T("9:35から朝ごはん。団体の人が多い時間なので、どんぶり横丁市場で空いている店を選んでください。10:20に市場を出て、市電の乗り場へ。",
                  "Breakfast from 9:35. Tour groups are around at this hour, so pick a restaurant with space in Donburi Yokocho. Leave at 10:20 for the tram stop."),
            time=(VIS, "9:35〜10:20", "9:35–10:20")),
        tower=dict(
            pre=T("市電は函館駅前10:32発→五稜郭公園前10:51着（その次は10:40発）。電停から歩いて15分でタワーです。",
                  "Tram: Hakodate-ekimae 10:32 → Goryokaku-Koen-mae 10:51 (the next is 10:40). The tower is 15 minutes’ walk from the stop."),
            rows=[row("train", "市電 函館駅前10:32→五稜郭公園前10:51、270円", "Tram Hakodate-ekimae 10:32 → Goryokaku-Koen-mae 10:51, ¥270")],
            time=(VIS, "11:10〜11:55", "11:10–11:55")),
        goryokaku=dict(time=(VIS, "12:00〜12:55", "12:00–12:55")),
        hiru=dict(
            pre=T("13時すぎは、12時台より入りやすい時間です。13:40には店を出て、歩いて15分の電停へ。",
                  "Just after 13:00 is easier than noon. Leave by 13:40 for the tram stop, 15 minutes’ walk away."),
            time=(VIS, "13:00〜13:40", "13:00–13:40")),
        hachiman=dict(
            pre=T("市電は五稜郭公園前13:58発→十字街14:21着（その次は14:06発→14:29着）。十字街から坂を上って10分で、八幡坂の上です。",
                  "Tram: Goryokaku-Koen-mae 13:58 → Jujigai 14:21 (the next is 14:06 → 14:29). From Jujigai it is 10 minutes uphill to the top of Hachiman-zaka."),
            notices=[N_LIGHTS],
            rows=[row("train", "市電 五稜郭公園前13:58→十字街14:21、290円", "Tram Goryokaku-Koen-mae 13:58 → Jujigai 14:21, ¥290")],
            time=(VIS, "14:35〜14:50", "14:35–14:50")),
        kokaido=dict(
            pre=T("12〜1月は日の入りが早いので、最初は選ばれていません。中に入るなら30分。そのぶん、お昼を短くするか、五稜郭を10分早く出てください。2月からは日が長くなり、入りやすくなります。",
                  "Not selected at first, because the sun sets so early in December and January. Going inside takes 30 minutes: shorten lunch or leave Goryokaku a little earlier. From February the longer days make it easy to fit in."),
            time=(VIS, "14:55〜15:25（入る場合）", "14:55–15:25 (if you go in)")),
        haris=dict(
            pre=T("八幡坂の上から、坂の上の道を東へ5分。教会を外から見て、中に入る日は献金を払って静かに。15:20に出て山麓駅へ。",
                  "Five minutes east along the top road from Hachiman-zaka. See the churches from outside; if you go in, make the donation and be quiet. Leave at 15:20 for the ropeway."),
            notices=[N_HARIS_WINTER],
            time=(VIS, "14:55〜15:20", "14:55–15:20")),
        ropeway=dict(
            pre=T("15:30の便で上がります（12月の日の入りは16:07ごろ）。明かりがそろうのは16:30〜16:50ごろ。17:00ごろに下りの列に並びます。",
                  "Take the 15:30 car up (sunset in December is about 16:07). The town is fully lit around 16:30–16:50. Join the queue down at about 17:00."),
            notices=[N_YEAREND, N_ROPE_AUTUMN],
            time=(VIS, "15:30〜17:10", "15:30–17:10")),
        kanemori=dict(
            pre=T("山麓駅から坂を下って15分。暗くなって明かりのついた倉庫を歩きます。店は19:00まで。12月は18:00にツリーの点灯式と花火があります。",
                  "Fifteen minutes downhill from the ropeway. Walk the floodlit warehouses after dark; shops stay open until 19:00. In December the tree is relit with fireworks at 18:00."),
            notices=[N_XMAS, N_LIGHTS],
            time=(VIS, "17:30〜18:20", "17:30–18:20")),
        yunokawa=dict(
            pre=T("最初は選ばれていません。入れるなら、赤レンガ倉庫のあと十字街18:35発の市電で湯の川温泉19:10着（土曜は18:34発→19:11着）。足湯かお風呂に入って、20:21発（函館駅前20:51着）か20:41発で戻り、駅の近くで遅い晩ごはんにします。最終は21:46発です。",
                  "Not selected at first. To add it, take the 18:35 tram from Jujigai after the warehouses (Yunokawa-Onsen 19:10; on Saturdays 18:34 → 19:11). Use the foot bath or a day bath, then return on the 20:21 (Hakodate-ekimae 20:51) or the 20:41 and eat a late dinner near the station. The last tram is 21:46."),
            notices=[N_YU_FIRE],
            rows=[row("train", "市電 十字街18:35→湯の川温泉19:10、300円。帰り 湯の川温泉20:21→函館駅前20:51", "Tram Jujigai 18:35 → Yunokawa-Onsen 19:10, ¥300. Back: Yunokawa-Onsen 20:21 → Hakodate-ekimae 20:51")],
            time=(VIS, "19:10〜20:20（入れる場合）", "19:10–20:20 (if you add it)")),
        yuhan=dict(
            pre=T("赤レンガ倉庫のまわりで食べるなら18:20から。駅の近くで食べるなら、十字街から市電で6分（19時台は平日19:03・19:09、土曜19:06・19:17など）。",
                  "Eat around the warehouses from 18:20, or take the tram 6 minutes from Jujigai to eat near the station (around 19:00: 19:03 and 19:09 on weekdays, 19:06 and 19:17 on Saturdays)."),
            time=(VIS, "18:20〜20:30ごろ", "18:20–about 20:30")),
    ))

EARLY = dict(
    file="hakodate-early.json", course="early",
    order=["eki", "asaichi", "hachiman", "kokaido", "haris", "kanemori", "hiru", "tower", "goryokaku", "ropeway", "yunokawa", "yuhan"],
    spots=dict(
        eki=dict(
            pre=T("6:30にホテルを出て、団体の人が来る前の朝市で朝ごはん。そのまま海ぞいを歩いて、人も車もいない八幡坂と元町へ。開いたばかりの公会堂と教会を見て、赤レンガ倉庫でひと休み。昼は五稜郭、夕方は函館山、最後に湯の川温泉であたたまります。\n\n"
                  "冬（12〜1月）の日の入りに合わせた時間割です。12〜1月は日の出が7時ごろなので、朝市はまだ暗いうちです。市電に4回乗るので、1日乗車券（800円）を買ってください。",
                  "Leave your hotel at 6:30 for breakfast at the market before the tour groups arrive. Walk along the water to Hachiman-zaka and Motomachi while they are empty of people and cars. See the Public Hall and the churches as they open and take a break at the warehouses. Goryokaku at midday, Mt. Hakodate at dusk, and a soak at Yunokawa Onsen to finish.\n\n"
                  "This timetable follows December–January sunsets. Sunrise is about 7:00 in those months, so the market is still dark when you arrive. You ride the tram four times: buy the day pass (¥800)."),
            notices=[N_WINTER_WALK, N_YEAREND],
            time=(DEP, "6:30", "6:30")),
        asaichi=dict(
            pre=T("6:35から朝ごはん。1〜4月は市場が6:00から、5〜12月は5:00からです。この時間は並ばずに入れる店が多く、店の人ともゆっくり話せます。",
                  "Breakfast from 6:35. The market opens at 6:00 from January to April and 5:00 from May to December. At this hour most restaurants have no queue and stallholders have time to talk."),
            time=(VIS, "6:35〜7:30", "6:35–7:30")),
        hachiman=dict(
            pre=T("朝市から海ぞいの道を歩いて20分で赤レンガ倉庫（店はまだ閉まっています。外を見ながら通ります）。そこから坂を上って10分。8時すぎの八幡坂は、人も車もほとんどいません。大三坂と、坂の上の道も歩いてください。\n\n"
                  "歩きたくない日は、市電で函館駅前から十字街まで6分です。",
                  "From the market, 20 minutes along the waterfront brings you to the warehouses (still closed; just walk past). From there it is 10 minutes uphill. Soon after 8:00 Hachiman-zaka has almost no people or cars. Walk Daisan-zaka and the road along the top as well.\n\n"
                  "If you would rather not walk, the tram from Hakodate-ekimae to Jujigai takes 6 minutes."),
            time=(VIS, "8:00〜8:50", "8:00–8:50")),
        kokaido=dict(
            pre=T("9:00に開きます。開いてすぐは、大広間とバルコニーにほとんど人がいません。",
                  "It opens at 9:00. Right after opening the ballroom and balcony are nearly empty."),
            time=(VIS, "9:00〜9:35", "9:00–9:35")),
        haris=dict(
            pre=T("聖堂が開くのは10:00（日曜は13:00）。先にチャチャ登りと教会のまわりを歩いて、10時に中へ。",
                  "The church opens at 10:00 (13:00 on Sundays). Walk Chacha-nobori and around the churches first, then go in at 10:00."),
            notices=[N_HARIS_WINTER],
            time=(VIS, "9:40〜10:20", "9:40–10:20")),
        kanemori=dict(
            pre=T("大三坂を下って10分。店は9:30から開いています。朝から歩いたので、ここで座って休みます。11:15に出て、十字街の電停へ5分。",
                  "Ten minutes down Daisan-zaka. Shops open at 9:30. After a morning on foot, sit down here for a while. Leave at 11:15 for the Jujigai stop, 5 minutes away."),
            notices=[N_XMAS],
            time=(VIS, "10:30〜11:15", "10:30–11:15")),
        hiru=dict(
            pre=T("市電は十字街11:22発→五稜郭公園前11:47着（その次は11:30発→11:55着）。歩いて15分で、タワーのそばの店です。",
                  "Tram: Jujigai 11:22 → Goryokaku-Koen-mae 11:47 (the next is 11:30 → 11:55). The shops by the tower are 15 minutes’ walk."),
            rows=[row("train", "市電 十字街11:22→五稜郭公園前11:47、290円", "Tram Jujigai 11:22 → Goryokaku-Koen-mae 11:47, ¥290")],
            time=(VIS, "12:05〜12:45", "12:05–12:45")),
        tower=dict(time=(VIS, "12:50〜13:30", "12:50–13:30")),
        goryokaku=dict(
            pre=T("14:25には公園を出て、歩いて15分の電停へ。函館山に間に合うように、ここは時間を守ってください。",
                  "Leave the park by 14:25 for the tram stop, 15 minutes’ walk. Keep to time here so you reach Mt. Hakodate before sunset."),
            time=(VIS, "13:35〜14:25", "13:35–14:25")),
        ropeway=dict(
            pre=T("市電は五稜郭公園前14:46発→十字街15:09着。坂を上って10分で山麓駅、15:30の便で上がります（12月の日の入りは16:07ごろ）。明かりがそろうのは16:30〜16:50ごろ。17:00ごろに下りの列に並びます。",
                  "Tram: Goryokaku-Koen-mae 14:46 → Jujigai 15:09. Ten minutes uphill to the lower station for the 15:30 car (sunset in December is about 16:07). The town is fully lit around 16:30–16:50. Join the queue down at about 17:00."),
            notices=[N_YEAREND, N_ROPE_AUTUMN],
            rows=[row("train", "市電 五稜郭公園前14:46→十字街15:09、290円", "Tram Goryokaku-Koen-mae 14:46 → Jujigai 15:09, ¥290")],
            time=(VIS, "15:30〜17:10", "15:30–17:10")),
        yunokawa=dict(
            pre=T("山を下りて十字街まで10分。市電は十字街17:39発→湯の川温泉18:14着（平日。土曜は17:38発）。足湯かお風呂であたたまって、19:37発（函館駅前20:07着）か19:52発で戻ります。\n\n"
                  "つかれた日は外して、山を下りたら赤レンガ倉庫の明かりを見て晩ごはんにしてください。",
                  "Ten minutes down to Jujigai. Tram: Jujigai 17:39 → Yunokawa-Onsen 18:14 (weekdays; 17:38 on Saturdays). Warm up in the foot bath or a day bath and return on the 19:37 (Hakodate-ekimae 20:07) or the 19:52.\n\n"
                  "If you are tired, leave this out: after the mountain, see the warehouses lit up and go to dinner."),
            notices=[N_YU_FIRE],
            rows=[row("train", "市電 十字街17:39→湯の川温泉18:14、300円。帰り 湯の川温泉19:37→函館駅前20:07", "Tram Jujigai 17:39 → Yunokawa-Onsen 18:14, ¥300. Back: Yunokawa-Onsen 19:37 → Hakodate-ekimae 20:07")],
            time=(VIS, "18:15〜19:35", "18:15–19:35")),
        yuhan=dict(
            pre=T("湯の川から戻って、駅の近くで。大門横丁は函館駅前の電停から歩いて3分ほどです。",
                  "Back from Yunokawa, eat near the station. Daimon Yokocho is about 3 minutes’ walk from the Hakodate-ekimae tram stop."),
            time=(VIS, "20:15〜21:30ごろ", "20:15–about 21:30")),
    ))

SAPPORO = dict(
    file="hakodate-sapporo.json", course="sapporo",
    order=["sapporo", "eki", "asaichi", "kanemori", "hachiman", "kokaido", "haris", "ropeway", "yuhan", "tower", "goryokaku", "hiru", "yunokawa", "kaeri"],
    spots=dict(
        sapporo=dict(
            pre=T("1日目は札幌8:43発の特急北斗6号で、函館12:33着（平日・土曜とも）。朝市でお昼を食べて、赤レンガ倉庫、元町、夕暮れの函館山へ。2日目は五稜郭と湯の川温泉を回って、函館17:55発の北斗19号で札幌21:41着です。\n\n"
                  "片道3時間50分かかるので、日帰りはすすめません。函館駅のまわりに泊まると、朝市も市電も歩いてすぐです。",
                  "Day 1: the 8:43 Hokuto 6 from Sapporo reaches Hakodate at 12:33 (weekdays and Saturdays). Lunch at the morning market, then the warehouses, Motomachi and Mt. Hakodate at dusk. Day 2: Goryokaku and Yunokawa Onsen, then the 17:55 Hokuto 19 back, reaching Sapporo at 21:41.\n\n"
                  "It is 3 hours 50 minutes each way, so a day trip is not worth it. Stay near Hakodate Station and the market and trams are a short walk away."),
            notices=[N_WINTER_WALK, N_YEAREND],
            rows=[row("train", "札幌8:43→函館12:33（特急北斗6号）。次は9:45→13:35", "Sapporo 8:43 → Hakodate 12:33 (Hokuto 6). Next: 9:45 → 13:35")],
            time=(DEP, "1日目 8:43（札幌駅に8:25ごろ）", "Day 1, 8:43 (be at Sapporo Station by about 8:25)")),
        eki=dict(
            pre=T("12:33に着いたら、先にホテルに荷物を預けます。朝市は14時すぎに閉まるので、すぐお昼へ。",
                  "Arriving at 12:33, drop your bags at the hotel first. The market closes soon after 14:00, so go straight to lunch."),
            time=(VIS, "1日目 12:33〜12:45", "Day 1, 12:33–12:45")),
        asaichi=dict(
            pre=T("お昼の海鮮丼。この時間は朝より空いていますが、売り切れのものや、片付けを始める店があります。食堂は14時ごろまでに入ってください。",
                  "A seafood bowl for lunch. It is quieter than the morning, but some items sell out and some stalls start closing. Be seated by about 14:00."),
            time=(VIS, "1日目 12:45〜13:30", "Day 1, 12:45–13:30")),
        kanemori=dict(
            pre=T("市電は函館駅前13:43発→十字街13:49着（その次は13:51発）。歩いても海ぞいに15〜20分です。倉庫はさっと見て、夜にもう一度通ります。",
                  "Tram: Hakodate-ekimae 13:43 → Jujigai 13:49 (the next is 13:51), or 15–20 minutes on foot along the water. Take a quick look now; you pass again after dark."),
            notices=[N_XMAS],
            rows=[row("train", "市電 函館駅前13:43→十字街13:49、250円", "Tram Hakodate-ekimae 13:43 → Jujigai 13:49, ¥250")],
            time=(VIS, "1日目 13:55〜14:25", "Day 1, 13:55–14:25")),
        hachiman=dict(
            pre=T("赤レンガ倉庫から坂を上って10分。", "Ten minutes uphill from the warehouses."),
            notices=[N_LIGHTS],
            time=(VIS, "1日目 14:35〜14:50", "Day 1, 14:35–14:50")),
        kokaido=dict(
            pre=T("12〜1月は日の入りが早いので、最初は選ばれていません。2月からの日の長い季節や、北斗2号（札幌6:00発→函館9:29着）で早く着いた日に。",
                  "Not selected at first, because of the early sunsets in December and January. Add it from February on, or if you arrive early on Hokuto 2 (Sapporo 6:00 → Hakodate 9:29)."),
            time=(VIS, "1日目 14:55〜15:25（入る場合）", "Day 1, 14:55–15:25 (if you go in)")),
        haris=dict(
            pre=T("八幡坂の上から東へ5分。15:20に出て山麓駅へ。", "Five minutes east from the top of Hachiman-zaka. Leave at 15:20 for the ropeway."),
            notices=[N_HARIS_WINTER],
            time=(VIS, "1日目 14:55〜15:20", "Day 1, 14:55–15:20")),
        ropeway=dict(
            pre=T("15:30の便で上がります（12月の日の入りは16:07ごろ）。明かりがそろうのは16:30〜16:50ごろ。17:00ごろに下りの列へ。雲で見えない日は、2日目の夕方（列車を18:43発にする）か、五稜郭タワーの夕暮れに切り替えてください。",
                  "Take the 15:30 car up (sunset in December is about 16:07). The town is fully lit around 16:30–16:50; join the queue down at about 17:00. If cloud hides the view, try again on day 2 (and take the 18:43 train), or switch to dusk at Goryokaku Tower."),
            notices=[N_YEAREND, N_ROPE_AUTUMN],
            time=(VIS, "1日目 15:30〜17:10", "Day 1, 15:30–17:10")),
        yuhan=dict(
            pre=T("山を下りたら、明かりのついた赤レンガ倉庫を通って晩ごはんへ（12月は18:00にツリーの花火）。ベイエリアで食べても、市電で駅に戻って大門横丁でも。",
                  "Coming down, walk through the floodlit warehouses to dinner (in December, fireworks at the tree at 18:00). Eat in the bay area, or take the tram back and go to Daimon Yokocho."),
            notices=[N_XMAS],
            time=(VIS, "1日目 17:30〜20:30ごろ", "Day 1, 17:30–about 20:30")),
        tower=dict(
            pre=T("2日目。荷物はホテルに預けたままにします。朝ごはんをもう一度朝市で食べるなら7:30ごろに。市電は函館駅前8:41発→五稜郭公園前8:58着（土曜は8:42発→8:59着）。開いたばかりのタワーは、エレベーターにすぐ乗れます。",
                  "Day 2. Leave your bags at the hotel. If you want breakfast at the market again, go at about 7:30. Tram: Hakodate-ekimae 8:41 → Goryokaku-Koen-mae 8:58 (Saturdays 8:42 → 8:59). Just after opening there is no wait for the lift."),
            rows=[row("train", "市電 函館駅前8:41→五稜郭公園前8:58、270円", "Tram Hakodate-ekimae 8:41 → Goryokaku-Koen-mae 8:58, ¥270")],
            time=(VIS, "2日目 9:15〜10:00", "Day 2, 9:15–10:00")),
        goryokaku=dict(time=(VIS, "2日目 10:05〜11:00", "Day 2, 10:05–11:00")),
        hiru=dict(
            pre=T("あじさい本店が開く11:00に合わせて早めのお昼。11:50に出て、歩いて15分の電停へ。",
                  "An early lunch as Ajisai opens at 11:00. Leave at 11:50 for the tram stop, 15 minutes’ walk."),
            time=(VIS, "2日目 11:05〜11:50", "Day 2, 11:05–11:50")),
        yunokawa=dict(
            pre=T("市電は五稜郭公園前12:11発→湯の川温泉12:23着（その次は12:19発）。足湯のあと、冬は熱帯植物園のサルの温泉へ（歩いて15分）。13時から開くお風呂に入って、15:04発の市電で函館駅前15:35着。\n\n"
                  "15:01発の北斗15号で早く帰る日は、湯の川を外してください。",
                  "Tram: Goryokaku-Koen-mae 12:11 → Yunokawa-Onsen 12:23 (the next is 12:19). After the foot bath, in winter walk 15 minutes to see the monkeys in their hot spring. Take a bath at one of the places that open at 13:00, then the 15:04 tram reaches Hakodate-ekimae at 15:35.\n\n"
                  "If you are going back early on the 15:01 Hokuto 15, leave Yunokawa out."),
            notices=[N_MONKEY, N_YU_FIRE],
            rows=[row("train", "市電 五稜郭公園前12:11→湯の川温泉12:23、270円。帰り 湯の川温泉15:04→函館駅前15:35", "Tram Goryokaku-Koen-mae 12:11 → Yunokawa-Onsen 12:23, ¥270. Back: Yunokawa-Onsen 15:04 → Hakodate-ekimae 15:35")],
            time=(VIS, "2日目 12:25〜15:00", "Day 2, 12:25–15:00")),
        kaeri=dict(
            pre=T("15:35に駅へ戻ったら、ホテルで荷物を受け取り、お土産とお弁当を買います。時間があまったら、湯の川をもう30分のばしてもかまいません（15:20発→15:51着）。17:55発の北斗19号で札幌21:41着。",
                  "Back at the station at 15:35: collect your bags, buy souvenirs and a boxed meal. If you would rather, stay 30 minutes longer at Yunokawa (15:20 tram → 15:51). The 17:55 Hokuto 19 reaches Sapporo at 21:41."),
            time=(DEP, "2日目 17:55（駅に17:30ごろ）", "Day 2, 17:55 (be at the station by about 17:30)")),
    ))


def spot(C, no, sid):
    b, o = S[sid], C["spots"][sid]
    name = o.get("name", b["name"])
    kind = o.get("kind", b["kind"])
    (label, tja, ten), pre = o["time"], o.get("pre")
    text = {}
    for i, l in enumerate(("ja", "en")):
        parts = [name[l]] + ([pre[l]] if pre else []) + [b["body"][l]]
        parts.append(f"{label[0]}：{tja}" if l == "ja" else f"{label[1]}: {ten}")
        text[l] = "\n\n".join(parts)
    out = {"no": no, "id": sid, "name": name, "kind": kind, "blurb": o.get("blurb", b["blurb"])}
    caution = o.get("caution", b.get("caution"))
    if caution:
        out["caution"] = caution
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"], links=o.get("links", b.get("links", [TRAM])),
               notices=o.get("notices", []),
               info={"rows": o.get("rows", []) + b["rows"], "cash": sid == "yuhan", "tip": b["tip"], "checked": CHECKED},
               photos=PHOTOS[sid])
    assert out["photos"], sid
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


for C in (LATE, EARLY, SAPPORO):
    N = {k: i for i, k in enumerate(C["order"], 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
    fixed = [k for k in ("sapporo", "eki", "kaeri") if k in N]
    picks = [N[k] for k in C["order"] if k not in fixed]
    auto = {str(N[k]): {"always": True} for k in fixed}
    if C is LATE:
        default = [n for n in picks if n not in ns("kokaido", "yunokawa")]
        sections = [{"first": 1, "last": N["asaichi"], "area": T("函館駅", "Hakodate Station"), "title": T("9:30に出て、朝市で朝ごはん", "Out at 9:30, breakfast at the market")},
                    {"first": N["tower"], "last": N["hiru"], "area": T("五稜郭", "Goryokaku"), "title": T("市電で五稜郭へ。タワー、公園、お昼", "Tram to Goryokaku: tower, park, lunch")},
                    {"first": N["hachiman"], "last": N["ropeway"], "area": T("元町・函館山", "Motomachi · Mt. Hakodate"), "title": T("坂と教会を歩いて、日の入り前に函館山へ", "Slopes and churches, then up the mountain before sunset")},
                    {"first": N["kanemori"], "last": N["yuhan"], "area": T("ベイエリア・夜", "Bay area · evening"), "title": T("明かりのついた赤レンガ倉庫と晩ごはん", "The floodlit warehouses and dinner")}]
        hints = [
            h("ropeway", {"none": ns("ropeway")},
              "函館山に上がらない日（雲・強い風）は、元町をゆっくり歩いて、16:30ごろ八幡坂の明かりか、赤レンガ倉庫の夕暮れを。五稜郭を午後にして、タワーから夕暮れの堀の明かり（12〜2月）を見る回り方もあります。",
              "No Mt. Hakodate today (cloud or wind)? Take Motomachi slowly and see the lights on Hachiman-zaka or dusk at the warehouses around 16:30. Or move Goryokaku to the afternoon and watch the moat light up from the tower (December–February)."),
            h("kokaido", {"any": ns("kokaido")},
              "公会堂に入ると30分かかります。12〜1月は、五稜郭のお昼を13:25までにして、1本前の市電（13:50発→十字街14:13着）に乗ってください。",
              "The Public Hall adds 30 minutes. In December and January, finish lunch by 13:25 and take the earlier tram (13:50 → Jujigai 14:13)."),
            h("yunokawa", {"any": ns("yunokawa")},
              "湯の川を入れると、晩ごはんは20:50すぎに駅の近くで。大門横丁か、22:00まで開いているラッキーピエロ函館駅前店へ。",
              "With Yunokawa, dinner is after 20:50 near the station: Daimon Yokocho, or Lucky Pierrot Hakodate-ekimae, open until 22:00."),
        ]
        note = "「9〜10時に出る」。9:30朝市→市電10:32→五稜郭タワー→公園・奉行所→お昼→市電13:58→八幡坂→（公会堂は寄り道）→教会→函館山15:30の便→夜の赤レンガ倉庫→晩ごはん（湯の川は寄り道）。"
    elif C is EARLY:
        default = picks
        sections = [{"first": 1, "last": N["asaichi"], "area": T("函館駅", "Hakodate Station"), "title": T("6:30に出て、空いている朝市へ", "Out at 6:30 to a quiet market")},
                    {"first": N["hachiman"], "last": N["kanemori"], "area": T("元町・ベイエリア", "Motomachi · bay area"), "title": T("人のいない八幡坂、開いたばかりの公会堂と教会", "An empty Hachiman-zaka, the hall and churches as they open")},
                    {"first": N["hiru"], "last": N["goryokaku"], "area": T("五稜郭", "Goryokaku"), "title": T("市電で五稜郭へ。お昼、タワー、公園", "Tram to Goryokaku: lunch, tower, park")},
                    {"first": N["ropeway"], "last": N["yuhan"], "area": T("函館山・湯の川", "Mt. Hakodate · Yunokawa"), "title": T("夕暮れの函館山、湯の川温泉、晩ごはん", "Mt. Hakodate at dusk, Yunokawa Onsen, dinner")}]
        hints = [
            h("yuhan", {"none": ns("yunokawa")},
              "湯の川に行かない日は、山を下りて赤レンガ倉庫の明かり（12月は18:00にツリーの花火）を見て、18:30ごろから晩ごはんに。",
              "Without Yunokawa: after the mountain, see the warehouses lit up (fireworks at the tree at 18:00 in December) and have dinner from about 18:30."),
            h("ropeway", {"none": ns("ropeway")},
              "函館山に上がらない日（雲・強い風）は、五稜郭を16:30ごろまでのばして、タワーから堀の明かり（12〜2月）を。そのあと五稜郭公園前から湯の川温泉へ市電で12分です。",
              "No Mt. Hakodate today (cloud or wind)? Stay at Goryokaku until about 16:30 and watch the moat light up from the tower (December–February). Yunokawa-Onsen is then 12 minutes by tram from Goryokaku-Koen-mae."),
            h("haris", {"none": ns("kokaido")},
              "公会堂に入らない日は、八幡坂と大三坂を歩いたあと、9:30に開く赤レンガ倉庫で先に休んで、10:00に教会へ戻る回り方もあります。",
              "Skipping the Public Hall? After the slopes, rest at the warehouses when they open at 9:30 and come back up to the church for 10:00."),
        ]
        note = "「6時台に出る」。6:30朝市→歩いて八幡坂8:00→公会堂9:00→教会10:00→赤レンガ倉庫→市電11:22→お昼→五稜郭タワー→公園→市電14:46→函館山15:30の便→市電17:39→湯の川温泉→市電19:37→晩ごはん。"
    else:
        default = [n for n in picks if n != N["kokaido"]]
        sections = [{"first": 1, "last": N["asaichi"], "area": T("1日目 札幌→函館", "Day 1 · Sapporo → Hakodate"), "title": T("8:43の特急北斗で函館へ、朝市でお昼", "The 8:43 Hokuto to Hakodate, lunch at the market")},
                    {"first": N["kanemori"], "last": N["yuhan"], "area": T("1日目 元町・函館山", "Day 1 · Motomachi · Mt. Hakodate"), "title": T("赤レンガ倉庫、坂と教会、夕暮れの函館山", "Warehouses, slopes and churches, Mt. Hakodate at dusk")},
                    {"first": N["tower"], "last": N["hiru"], "area": T("2日目 五稜郭", "Day 2 · Goryokaku"), "title": T("開いたばかりのタワーと公園、早めのお昼", "The tower as it opens, the park, an early lunch")},
                    {"first": N["yunokawa"], "last": N["kaeri"], "area": T("2日目 湯の川→札幌", "Day 2 · Yunokawa → Sapporo"), "title": T("湯の川温泉、17:55の特急で札幌へ", "Yunokawa Onsen, then the 17:55 back to Sapporo")}]
        hints = [
            h("kaeri", {"none": ns("yunokawa")},
              "湯の川に行かない日は、五稜郭のお昼のあと市電で函館駅前へ（約20分）。15:01発の北斗15号で札幌18:47着です。",
              "Without Yunokawa, take the tram back to the station after lunch at Goryokaku (about 20 minutes). The 15:01 Hokuto 15 reaches Sapporo at 18:47."),
            h("ropeway", {"none": ns("ropeway")},
              "1日目に函館山が見えなかったら、2日目の湯の川を短くして、15:30の便で上がり、18:43発の最終で帰る回り方があります（札幌22:41着）。",
              "If Mt. Hakodate was in cloud on day 1, shorten Yunokawa on day 2, ride up at 15:30 and take the last train at 18:43 (Sapporo 22:41)."),
        ]
        note = "「札幌から1泊2日」。1日目 札幌8:43→函館12:33→朝市でお昼→赤レンガ倉庫→八幡坂→教会→函館山15:30の便→晩ごはん。2日目 五稜郭タワー9:15→公園→お昼→湯の川温泉→函館17:55→札幌21:41。"
    data = {
        "id": "hakodate", "course": C["course"],
        "_note": "函館で1日（hakodate/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "写真はすべて Wikimedia Commons（一覧は scripts/hakodate_web_photos.json）。info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。"
                 + "このファイルは scripts/build_hakodate_data.py で作る（直接直さない）。",
        "sections": sections, "focus": {"first": 2 if C is SAPPORO else 1, "last": len(C["order"])},
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。駅（と札幌駅・帰り）は自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": default, "auto": auto, "hints": hints},
        "photoBase": "../images/hakodate/", "sources": SOURCES,
        "spots": [spot(C, i, k) for i, k in enumerate(C["order"], 1)],
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"]) for s in data["spots"]], "default", default)
