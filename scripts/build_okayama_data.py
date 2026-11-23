#!/usr/bin/env python3
"""岡山と倉敷のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_okayama_data.py   （そのあと python3 scripts/sync_okayama.py）
- data/routes/okayama.json       … 「1泊2日」（stay。最初に開く。1日目 岡山→夜の倉敷／2日目 朝の倉敷→吉備津神社→京都・大阪か広島へ）15か所
- data/routes/okayama-stop.json  … 「移動の途中に立ち寄る」（stop。京都・大阪→広島。最初は岡山城と後楽園。倉敷はかわりに選ぶ）14か所
- 2026-11-22 オーナーの指示：日帰りの時間割は作らない。「1泊した方が良い場所。もしくは京都・大阪〜広島の移動中に立ち寄る場所」
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの時間割（pre）→ 共通の説明（body）→ おすすめの時間」の順に組み立てる
- 時刻は2026年11月25日（水）・28日（土）・29日（日）のダイヤ（乗換案内）。JR のダイヤ改正のあとは確かめ直す
- 写真は images/okayama/。自分の写真はファイル名だけ、借りた写真（Wikimedia Commons）は scripts/okayama_web_photos.json から
- オーナーの写真は岡山城・月見橋（2021年3月。改修の前）、岡山駅（2021・2023・2025年）、路面電車（2023年8月）だけ。
  後楽園・吉備津神社・倉敷は行っていない場所として中立に書く（行った・食べたことを書かない）
- 店名は、公式サイトで時間を確かめた店だけ（四季彩・三宅商店・ウイステリア・バー レジーナ・吾妻寿司）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/okayama"
CHECKED = "2026-11-22"
DEP = ("おすすめ出発時間", "Recommended departure time")
VIS = ("おすすめ訪問時間", "Recommended visit time")
MOV = ("おすすめ移動時間", "Recommended travel time")


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def notice(hja, hen, ja, en, url=None, start=None, to=None):
    d = {"head": T(hja, hen), "text": T(ja, en), "from": start, "to": to}
    if url:
        d["url"] = url
    return d


def q(f, t, day, hm, kind="d", seat=1):
    """確かめた乗換案内（Yahoo!路線情報）の検索結果のURL。day は '25'（2026年11月）か '2026/12/30'"""
    h, m = hm.split(":")
    y, mon, d = day.split("/") if "/" in day else ("2026", "11", day)
    p = dict(to=t, y=y, m=mon, d=d, hh=h, m1=m[0], m2=m[1], type={"d": 1, "l": 2, "a": 4}[kind], ticket="normal",
             expkind=seat, shin=1, ex=1, lb=1, al=0, hb=1, sr=0, s=0, userpass=0, ws=3)
    p["from"] = f
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(p)


def cc(x):
    """Wikimedia Commons の写真。"""
    return {"file": x["file"], "credit": {"author": x["author"], "license": x["license"],
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(x["title"].replace(" ", "_"))}}


WEB = json.load(open(f"{R}/scripts/okayama_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]
PHOTOS = {
    "kyoto": ["eki-1.jpg"], "okayamaeki": ["eki-3.jpg"] + W("okayamaeki"), "tram": ["tram-1.jpg"] + W("tram"),
    "castle": W("castle") + ["castle-1.jpg"], "tsukimi": ["tsukimi-1.jpg", "tsukimi-2.jpg", "tsukimi-3.jpg"],
    "korakuen": W("korakuen"), "kibitsu": W("kibitsu"), "lunch": W("lunch"), "bikan": W("bikan"), "ohara": W("ohara"),
    "boat": W("boat"), "ivy": W("ivy"), "honmachi": W("honmachi"), "achi": W("achi"), "kaeri": ["eki-4.jpg"],
}

U = dict(
    castle="https://okayama-castle.jp/guide/", castle_faq="https://okayama-castle.jp/faq",
    castle_light="https://okayama-castle.jp/2929/", castle_event="https://okayama-castle.jp/5898/",
    castle_reentry="https://okayama-castle.jp/news",
    garden="https://okayama-korakuen.jp/goriyo/441.html", garden_access="https://okayama-korakuen.jp/goriyo/130.html",
    garden_event="https://okayama-korakuen.jp/ibento/1303.html",
    shikisai="https://korakuen-shikisai.jp/",
    tram="https://okayama-kido.co.jp/tram/route-map/", tram_top="https://okayama-kido.co.jp/tram/",
    ohara="https://www.ohara.or.jp/visitor_info/",
    ohara_cal="https://www.ohara.or.jp/cms/wp-content/themes/ohara/images/top/calendar_pdf/2026calendar.pdf",
    boat="https://kankou-kurashiki.jp/special/kawafune/",
    boat_faq="https://kankou-kurashiki.jp/wp-content/uploads/2026/07/0a31b13f80349a6fcc7616b8c89f4fef.pdf",
    lights="https://www.kurashiki-tabi.jp/see/201/", nightmap="https://www.kurashiki-tabi.jp/feature/yorumeguri-map/",
    hotel_rest="https://www.kurashiki-kokusai-hotel.co.jp/restaurants",
    wisteria="https://www.kurashiki-kokusai-hotel.co.jp/restaurants/wisteria",
    ohara_list="https://www.ohara.or.jp/calendar/",
    kurabo="https://www.kurabo.co.jp/kurabo_kinenkan/",
    kura_map="https://eki.jr-odekake.net/premises?id=0650612",
    faq_stop="https://support-faq.westjr.co.jp/westjr/faq/show/1461?site_domain=default",
    faq_parallel="https://support-faq.westjr.co.jp/westjr/faq/show/1403?site_domain=default",
    miyake="https://miyakeshouten.com/time/", azuma="http://azumazushi.ecgo.jp/page0111.html",
    sunste="https://sun-ste.com/okayama-ichibangai/information/",
    nekonote="https://www.okayama-kanko.jp/spot/detail_10022.html",
    locker="https://www.akilocker.biz/mobile/map.html?locationId=JR_OKAYAMA&mapId=M51001&lang=1",
    sta_oka="https://eki.jr-odekake.net/top?id=0650608", sta_kura="https://eki.jr-odekake.net/top?id=0650612",
    info_eki="https://kankou-kurashiki.jp/info/" + urllib.parse.quote("倉敷駅前観光案内所") + "/",
    info_kan="https://kankou-kurashiki.jp/info/" + urllib.parse.quote("倉敷館観光案内所") + "/",
    info_rest="https://kankou-kurashiki.jp/info/" + urllib.parse.quote("倉敷市観光休憩所") + "/",
    stopover="https://railway.jr-central.co.jp/ticket-rule/rule05.html",
    valid="https://railway.jr-central.co.jp/ticket-rule/rule04.html",
    ex="https://smart-ex.jp/product/plan/service/",
    ex_fare="https://smart-ex.jp/product/plan/service/pdf/service_fares_reserved.pdf",
    baggage="https://smart-ex.jp/reservation/reserve_smart/oversized-baggage/",
    baggage_west="https://www.westjr.co.jp/travel-information/en/train-usage-guide/luggage/",
    reserved="https://jr-central.co.jp/news/release/_pdf/000045592.pdf",
    kibitsu="https://www.kibitujinja.com/", achi="https://achi.or.jp/", ivy="https://www.ivysquare.co.jp/history/",
    sun="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s3411.html",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容。RECHECKED は 2026-11-23 の「要確認」の見直しで開き直したもの
TODAY = "2026-11-23"
RECHECKED = {"ウイステリア・バー", "ウイステリア", "三宅商店", "吾妻寿司", "さんすて岡山", "四季彩", "大原美術館",
             "大原美術館 開館情報一覧", "倉紡記念館", "倉敷駅の構内図", "途中下車（JR西日本）", "新幹線経由の乗車券と在来線（JR西日本）",
             "岡山駅のロッカー", "岡山駅の設備", "倉敷駅の設備"}
SOURCES = [dict(what=a, url=b, saw=c, checked=TODAY if a in RECHECKED else CHECKED) for a, b, c in [
    ("京都→岡山 平日", q("京都", "岡山", "25", "09:20"), "のぞみ9号 9:25→10:25、自由席7,140円（乗車券3,740円＋3,400円）"),
    ("京都→岡山 土曜", q("京都", "岡山", "28", "09:20"), "のぞみ9号 9:25→10:25、自由席7,140円"),
    ("京都→岡山 日曜", q("京都", "岡山", "29", "09:20"), "のぞみ9号 9:25→10:25"),
    ("京都→岡山 指定席 平日", q("京都", "岡山", "25", "09:20", seat=2), "8,100円（特急料金4,360円）"),
    ("京都→岡山 指定席 土曜", q("京都", "岡山", "28", "09:20", seat=2), "8,300円（特急料金4,560円）"),
    ("京都→岡山 年末", q("京都", "岡山", "2026/12/30", "09:20"), "のぞみは指定席だけ、8,500円"),
    ("新大阪→岡山 平日", q("新大阪", "岡山", "25", "09:30"), "のぞみ9号 9:41→10:25、自由席5,610円"),
    ("新大阪→岡山 土曜", q("新大阪", "岡山", "28", "09:30"), "のぞみ9号 9:41→10:25"),
    ("新大阪→岡山 指定席", q("新大阪", "岡山", "25", "09:30", seat=2), "6,460円（特急料金3,380円）"),
    ("三条京阪→京都 平日", q("三条京阪", "京都", "25", "08:50"), "8:55→9:10、260円"),
    ("三条京阪→京都 土曜", q("三条京阪", "京都", "28", "08:50"), "8:52→9:09、260円"),
    ("梅田→新大阪", q("梅田(Osaka Metro)", "新大阪", "25", "09:15"), "6分、240円"),
    ("難波→新大阪", q("難波(Osaka Metro)", "新大阪", "25", "09:05"), "9:08→9:27、290円"),
    ("路面電車 行き 平日", q("岡山駅前", "城下(岡山県)", "25", "10:40"), "10:44→10:52、160円"),
    ("路面電車 行き 土曜", q("岡山駅前", "城下(岡山県)", "28", "10:40"), "10:44→10:52"),
    ("路面電車 行き 日曜", q("岡山駅前", "城下(岡山県)", "29", "10:40"), "10:44→10:52"),
    ("路面電車 帰り 平日", q("城下(岡山県)", "岡山駅前", "25", "14:20"), "14:25→14:32、160円"),
    ("路面電車 帰り 土曜", q("城下(岡山県)", "岡山駅前", "28", "14:20"), "14:25→14:32"),
    ("路面電車 帰り 日曜", q("城下(岡山県)", "岡山駅前", "29", "14:20"), "14:25→14:32"),
    ("岡山→倉敷 1日目 平日", q("岡山", "倉敷", "25", "14:38"), "15:04→15:20、330円"),
    ("岡山→倉敷 1日目 土曜", q("岡山", "倉敷", "28", "14:55"), "15:04→15:20、330円"),
    ("岡山→倉敷 1日目 日曜", q("岡山", "倉敷", "29", "14:38"), "15:04→15:20"),
    ("岡山→倉敷 午前 平日", q("岡山", "倉敷", "25", "10:33"), "10:40→10:58、330円"),
    ("岡山→倉敷 午前 土曜", q("岡山", "倉敷", "28", "10:33"), "10:40→10:58"),
    ("岡山→倉敷 午前 日曜", q("岡山", "倉敷", "29", "10:33"), "10:40→10:58"),
    ("倉敷→岡山 夜", q("倉敷", "岡山", "25", "20:20"), "20:49→21:05（土曜も同じ）"),
    ("倉敷→岡山 2日目 平日", q("倉敷", "岡山", "25", "13:00"), "13:11→13:28、330円"),
    ("倉敷→岡山 2日目 土曜", q("倉敷", "岡山", "28", "13:00"), "13:11→13:28"),
    ("倉敷→岡山 2日目 日曜", q("倉敷", "岡山", "29", "13:00"), "13:11→13:28"),
    ("倉敷→岡山 入れ替えの朝", q("倉敷", "岡山", "25", "09:20"), "9:23→9:40（土曜も同じ）"),
    ("岡山→吉備津 平日", q("岡山", "吉備津", "25", "13:40"), "13:52→14:07、14:22→14:37、210円"),
    ("岡山→吉備津 土曜", q("岡山", "吉備津", "28", "13:40"), "13:52→14:07"),
    ("岡山→吉備津 日曜", q("岡山", "吉備津", "29", "13:40"), "13:52→14:07"),
    ("吉備津→岡山 平日", q("吉備津", "岡山", "25", "15:05"), "15:47→16:05、210円"),
    ("吉備津→岡山 土曜", q("吉備津", "岡山", "28", "15:05"), "15:47→16:05"),
    ("吉備津→岡山 日曜", q("吉備津", "岡山", "29", "15:05"), "15:47→16:05"),
    ("岡山→京都 2日目 平日", q("岡山", "京都", "25", "16:10"), "のぞみ38号 16:20→17:20"),
    ("岡山→京都 2日目 土曜", q("岡山", "京都", "28", "16:10"), "のぞみ38号 16:20→17:20"),
    ("岡山→京都 2日目 日曜", q("岡山", "京都", "29", "16:10"), "のぞみ38号 16:20→17:20"),
    ("岡山→新大阪 2日目", q("岡山", "新大阪", "25", "16:10"), "のぞみ38号 16:20→17:04（土日も同じ）、5,610円"),
    ("岡山→広島 2日目 平日", q("岡山", "広島", "25", "16:10"), "のぞみ35号 16:26→17:02"),
    ("岡山→広島 2日目 土曜", q("岡山", "広島", "28", "16:10"), "のぞみ35号 16:26→17:02"),
    ("岡山→広島 2日目 日曜", q("岡山", "広島", "29", "16:20"), "のぞみ35号 16:26→17:02"),
    ("岡山→京都 最終 平日", q("岡山", "京都", "25", "23:00", "l"), "乗り換えなしは21:44→22:45、最終は22:48発みずほ＋新快速で0:30着"),
    ("岡山→京都 最終 土曜", q("岡山", "京都", "28", "23:00", "l"), "21:44→22:45、22:48→0:30"),
    ("倉敷→京都 最終", q("倉敷", "京都", "25", "23:00", "l"), "21:13発で22:45着、最終22:18発で0:30着（土日も同じ）"),
    ("岡山→新大阪 最終", q("岡山", "新大阪", "25", "23:00", "l"), "22:48→23:37（土曜も同じ）"),
    ("京都→三条京阪 最終", q("京都", "三条京阪", "25", "23:40", "l"), "地下鉄の最終は23:25発→23:58着"),
    ("岡山→広島 立ち寄り 平日", q("岡山", "広島", "25", "15:00"), "のぞみ69号 15:06→15:42、自由席5,610円（乗車券3,080円＋2,530円）"),
    ("岡山→広島 立ち寄り 土曜", q("岡山", "広島", "28", "15:00"), "のぞみ69号 15:06→15:42"),
    ("岡山→広島 立ち寄り 日曜", q("岡山", "広島", "29", "15:00"), "のぞみ69号 15:06→15:42"),
    ("岡山→広島 指定席 平日", q("岡山", "広島", "25", "14:40", seat=2), "のぞみ6,460円（特急料金3,380円）"),
    ("岡山→広島 指定席 土曜", q("岡山", "広島", "28", "14:40", seat=2), "のぞみ6,660円"),
    ("倉敷→広島 平日", q("倉敷", "広島", "25", "15:00"), "15:13発（岡山乗換）5,940円、15:06発（福山乗換）5,170円、どちらも16:27着"),
    ("倉敷→広島 土曜", q("倉敷", "広島", "28", "15:00"), "15:13発・15:06発とも16:27着"),
    ("倉敷→広島 日曜", q("倉敷", "広島", "29", "15:00"), "15:13発・15:06発とも16:27着"),
    ("倉敷→広島 夕方", q("倉敷", "広島", "25", "18:00"), "18:18発（岡山）→19:23、18:46発（新倉敷）→19:46。新倉敷経由は60分"),
    ("倉敷→広島 最終", q("倉敷", "広島", "25", "23:00", "l"), "22:42発→23:54着（岡山乗換）"),
    ("岡山→広島 最終", q("岡山", "広島", "25", "23:00", "l"), "23:14→23:54"),
    ("京都→広島 通し", q("京都", "広島", "25", "09:20"), "380.6km、乗車券6,600円、通しの自由席10,770円"),
    ("新大阪→広島 通し", q("新大阪", "広島", "25", "09:35"), "341.6km、乗車券5,720円、通しの自由席9,890円"),
    ("京都→倉敷 立ち寄り", q("京都", "倉敷", "25", "09:20"), "9:25→10:58（岡山乗換）、自由席7,470円"),
    ("倉敷→京都", q("倉敷", "京都", "25", "17:40"), "京都〜倉敷は自由席7,470円"),
    ("広島→岡山 逆向き 平日", q("広島", "岡山", "25", "09:20"), "のぞみ124号 9:29→10:04"),
    ("広島→岡山 逆向き 土曜", q("広島", "岡山", "28", "09:20"), "のぞみ124号 9:29→10:04"),
    ("岡山→京都 逆向き 平日", q("岡山", "京都", "25", "15:00"), "のぞみ34号 15:20→16:20"),
    ("岡山→京都 逆向き 土曜", q("岡山", "京都", "28", "15:00"), "のぞみ34号 15:20→16:20"),
    ("岡山→新大阪 逆向き", q("岡山", "新大阪", "25", "15:15"), "のぞみ34号 15:20→16:04（土曜も同じ）"),
    ("岡山→京都 逆向き 日曜", q("岡山", "京都", "29", "15:00"), "15:20→16:20"),
    ("岡山→新大阪 逆向き 日曜", q("岡山", "新大阪", "29", "15:15"), "15:20→16:04"),
    ("岡山→京都 遅い時間 日曜", q("岡山", "京都", "29", "21:40"), "21:44→22:45が乗り換えなしの最後"),
    ("岡山→京都 最終 日曜", q("岡山", "京都", "29", "23:00", "l"), "22:48→0:30"),
    ("岡山→新大阪 最終 日曜", q("岡山", "新大阪", "29", "23:00", "l"), "22:48→23:37"),
    ("岡山→広島 最終 土曜", q("岡山", "広島", "28", "23:00", "l"), "23:14→23:54"),
    ("岡山→広島 最終 日曜", q("岡山", "広島", "29", "23:00", "l"), "23:14→23:54"),
    ("倉敷→広島 最終 土曜", q("倉敷", "広島", "28", "23:00", "l"), "22:42→23:54"),
    ("倉敷→広島 最終 日曜", q("倉敷", "広島", "29", "23:00", "l"), "22:42→23:54"),
    ("倉敷→岡山 夜 日曜", q("倉敷", "岡山", "29", "20:20"), "20:49→21:05"),
    ("倉敷→岡山 入れ替えの朝 月曜祝日", q("倉敷", "岡山", "23", "09:20"), "9:23→9:40"),
    ("三条京阪→京都 日曜", q("三条京阪", "京都", "29", "08:50"), "8:52→9:09"),
    ("倉敷→京都 夕方 日曜", q("倉敷", "京都", "29", "17:40"), "17:44→19:19"),
    ("途中下車", U["stopover"], "乗車券は後戻りしなければ何回でも途中下車可。100キロまでと特急券は不可"),
    ("乗車券の有効期間", U["valid"], "200キロまで2日、400キロまで3日"),
    ("スマートEX", U["ex"], "途中下車はできません。下車した先の区間は無効"),
    ("スマートEXのおねだん", U["ex_fare"], "のぞみ通常期：京都〜岡山7,900円、新大阪〜岡山6,260円、岡山〜広島6,260円、京都〜広島11,740円"),
    ("特大荷物", U["baggage"], "3辺160cm超250cm以内は予約が必要、予約なしは1,000円"),
    ("特大荷物と自由席", U["baggage_west"], "Oversized baggage is not allowed in non-reserved seats"),
    ("のぞみ全席指定の期間", U["reserved"], "11/21〜23、12/25〜1/5、1/9〜11、3/20〜22"),
    ("ねこのてステーション", U["nekonote"], "新幹線改札口すぐ。預かり8:00〜20:00・600円/800円、宿への配達は13:30まで受付・1,500円"),
    ("岡山駅のロッカー", U["locker"], "H：2F新幹線改札外、0:00〜24:00、ICカード専用、大8・中45・小56。A：さんすて南館2F 6:00〜24:00。料金の記載なし"),
    ("岡山駅の設備", U["sta_oka"], "コインロッカーあり"),
    ("倉敷駅の設備", U["sta_kura"], "コインロッカーあり。料金の記載なし"),
    ("倉敷駅前観光案内所", U["info_eki"], "西ビル2階、ロッカー9:00〜17:00・当日のみ"),
    ("倉敷館観光案内所", U["info_kan"], "9:00〜18:00、ロッカー9:00〜17:00・当日のみ"),
    ("倉敷市観光休憩所", U["info_rest"], "ロッカー9:00〜17:00。過ぎると翌日まで出せない"),
    ("岡山城", U["castle"], "9:00〜17:30（入場17:00まで）、12/29〜31休み、500円、共通券800円"),
    ("岡山城 所要時間", U["castle_faq"], "平均50〜60分、ロッカーは天守に100円返却式"),
    ("岡山城 再入場", U["castle_reentry"], "天守の再入場はできません"),
    ("岡山城 ライトアップ", U["castle_light"], "毎日、日没〜24時"),
    ("岡山城 秋の烏城灯源郷", U["castle_event"], "11/20〜29 17:00〜20:30（天守は20:00まで）"),
    ("後楽園", U["garden"], "10/1〜3/19 8:00〜17:00（入園16:45）、3/20〜9/30 7:30〜18:00（17:45）、500円、無休"),
    ("後楽園 アクセス", U["garden_access"], "城下から徒歩10分、岡山駅から徒歩25分"),
    ("幻想庭園", U["garden_event"], "秋は11/20〜29 17:00〜20:30（入園20:00まで）"),
    ("四季彩", U["shikisai"], "後楽園外苑、お食事11:00〜14:30、カフェ14:30〜16:00、夜は完全予約制（6名から）、年中無休"),
    ("路面電車", U["tram"], "160円、1日券400円、交通系IC可"),
    ("路面電車 MOMO", U["tram_top"], "検査のため運休中"),
    ("大原美術館", U["ohara"], "3〜11月9:00〜17:00（入館16:30）、12〜2月〜15:00（14:30）、月曜休み（祝日は開館）、2,000円、撮影不可"),
    ("大原美術館 カレンダー", U["ohara_cal"], "12/21〜25・28、1/12〜15も休館。元日は本館のみ"),
    ("川舟", U["boat"], "9:30〜17:00・30分おき、第2月曜休み、1〜2月は土日祝、1,000円、30日前からWEB予約"),
    ("川舟 よくある質問", U["boat_faq"], "当日券は午前中に売り切れることも。12:00・12:30便は当日券のみ。夏は15:30便以降運休の可能性"),
    ("夜間景観照明", U["lights"], "10〜3月は日没〜21:00、4〜9月は日没〜22:00"),
    ("夜めぐりマップ", U["nightmap"], "夜の230店舗を掲載"),
    ("ウイステリア・バー", U["hotel_rest"], "ウイステリア ディナー17:00〜21:00（L.O.20:00）。バー レジーナ18:00〜24:00（L.O.23:00）、日月休み"),
    ("ウイステリア", U["wisteria"], "ディナータイム17:00〜21:00（L.O.20:00）、ディナーコース6,160円〜、料金に10%のサービス料"),
    ("三宅商店", U["miyake"], "平日11:30、土11:00、日8:30〜17:00（L.O.16:30）、年中無休"),
    ("吾妻寿司", U["azuma"], "さんすて岡山2F、11:00〜22:00（L.O.21:00）、年中無休、ネタ・シャリがなくなり次第終了の場合あり"),
    ("さんすて岡山", U["sunste"], "レストラン11:00〜22:00。旅弁当 駅弁にぎわい（南館2F）7:00〜20:30。ロッカーは一番街B1F、さんすて南館1F・2F（料金の記載なし）"),
    ("大原美術館 開館情報一覧", U["ohara_list"], "12/21〜25・28休館、12/29〜31は9:00〜15:00開館、1/1は本館のみ、1/12〜15休館"),
    ("倉紡記念館", U["kurabo"], "10:00〜16:00（入館15:45まで）、年中無休、一般300円・学生250円、小学生未満無料"),
    ("倉敷駅の構内図", U["kura_map"], "2024年4月1日時点の図。コインロッカーは2階の改札外（北口寄り）と1階の南口の西側（レンタカーのそば）。料金の記載なし"),
    ("途中下車（JR西日本）", U["faq_stop"], "普通乗車券は後戻りしない限り何回でも途中下車可。100キロまでの乗車券と特急券は不可"),
    ("新幹線経由の乗車券と在来線（JR西日本）", U["faq_parallel"], "東京〜熱海・新下関〜博多以外は、新幹線経由の普通乗車券で並行する在来線（山陽本線）に乗れる"),
    ("吉備津神社", U["kibitsu"], "5:00〜18:00、御守は16時ごろまで、鳴釜神事9:00〜14:00・金曜休み、駅から徒歩約10分"),
    ("阿智神社", U["achi"], "参拝は終日可、授与所9:00〜17:00"),
    ("日の入り（岡山）", U["sun"], "11月22日16:56、28日16:54"),
]]

JR = link("timetable", "JRおでかけネット（時刻・運賃）", "JR West timetables and fares", "https://www.jr-odekake.net/", "https://www.westjr.co.jp/global/en/")
STOPOVER = link("info", "途中下車の決まり（JR東海）", "Stopover rules (JR Central, Japanese)", U["stopover"])
EX = link("official", "スマートEX（途中下車は不可）", "smartEX (no stopovers; Japanese)", U["ex"])
NEKO = link("info", "ねこのてステーション（手荷物）", "Nekonote Station (luggage)", U["nekonote"], "https://www.okayama-japan.jp/en/spot/10887")
LOCKER = link("info", "岡山駅のロッカーの空き状況", "Locker availability at Okayama Station", U["locker"])
KTABI = link("info", "倉敷観光WEB", "Kurashiki tourism website", "https://www.kurashiki-tabi.jp/", "https://www.kurashiki-tabi.jp/for/en/")

# 何か所かに出すお知らせ
N_RESERVED = notice(
    "のぞみに自由席がない日", "Days with no unreserved seats on the Nozomi",
    "2026年11月21〜23日、12月25日〜2027年1月5日、1月9〜11日、3月20〜22日は、のぞみが全席指定です。指定席を先に買ってください。ひかり・さくら・こだまには自由席があります。",
    "On 21–23 November 2026, 25 December–5 January, 9–11 January and 20–22 March 2027 every Nozomi seat is reserved, so buy a seat first. Hikari, Sakura and Kodama trains keep their unreserved cars.",
    U["reserved"], to="2027-03-22")
N_BIG = notice(
    "大きな荷物は予約が要ります", "Oversized bags need a reservation",
    "3辺の合計が160cmを超える荷物（250cmまで）は、「特大荷物スペースつき座席」の予約が要ります。予約なしだと1,000円の手数料です。自由席には持ち込めません。",
    "A bag over 160 cm in total dimensions (up to 250 cm) needs a seat with an oversized baggage area. Without one the charge is ¥1,000, and such bags are not allowed in unreserved cars.",
    U["baggage"])
N_BAGS_STAY = notice(
    "荷物：13:30までに預ければ宿に届きます", "Bags: hand them in by 13:30 and they go to your hotel",
    "新幹線の改札を出てすぐの「ねこのてステーション」で、岡山市内・倉敷市内の指定の宿へ17:00ごろまでに届けてくれます（1,500円、受付8:00〜13:30）。自分の宿が対象か、先に確かめてください。対象外なら、改札の外のロッカーか一時預かり（8:00〜20:00）へ。",
    "Nekonote Station, just outside the Shinkansen gates, delivers to listed hotels in Okayama and Kurashiki by about 17:00 (¥1,500, hand in 8:00–13:30). Check beforehand that yours is listed. Otherwise use the lockers outside the gates or the bag storage there (8:00–20:00).",
    U["nekonote"])
N_BAGS_STOP = notice(
    "荷物：新幹線の改札を出てすぐ預ける", "Bags: leave them just outside the Shinkansen gates",
    "「ねこのてステーション」の一時預かりは8:00〜20:00。3辺120cm・15kgまで600円、160cm・25kgまで800円で、それより大きい荷物は預かってもらえません。改札の外のロッカーは24時間・交通系ICカード専用で、大は8つだけ（料金は要確認）。",
    "Bag storage at Nekonote Station runs 8:00–20:00: ¥600 up to 120 cm and 15 kg, ¥800 up to 160 cm and 25 kg, nothing larger. The lockers outside the gates are open 24 hours and take IC cards only, with just eight large ones (prices not confirmed).",
    U["nekonote"])
N_TICKET = notice(
    "きっぷ：スマートEXの通しでは途中で降りられません", "Tickets: you cannot stop over on a through smartEX ticket",
    "スマートEXは途中下車ができず、岡山で改札を出ると広島までの分は無効になります。EXで買うなら京都→岡山、岡山→広島の2つに分けてください。紙のきっぷなら、乗車券は広島までの1枚で途中下車できます。特急券は途中下車できないので、岡山で区切って2枚買います。",
    "smartEX does not allow stopovers: leave the gates at Okayama and the rest to Hiroshima is void. With EX, book Kyoto–Okayama and Okayama–Hiroshima separately. With paper tickets one fare ticket to Hiroshima allows a stopover, but express tickets do not, so buy two, split at Okayama.",
    U["ex"])
N_NIGHT_STAY = notice(
    "11月29日までは、岡山の夜も明かりがつきます", "Until 29 November Okayama lights up at night",
    "後楽園の「秋の幻想庭園」と岡山城の「秋の烏城灯源郷」は20:30まで（入場は20:00まで）。見たい人は1日目の宿を岡山駅のまわりにして、倉敷を昼、後楽園とお城を夕方からにしてください。",
    "Korakuen and the castle open until 20:30 for their autumn illuminations (last entry 20:00). To see them, stay near Okayama Station on the first night, do Kurashiki by day and the garden and castle from late afternoon.",
    U["garden_event"], to="2026-11-29")
N_NIGHT_STOP = notice(
    "11月29日までは、夕方から寄っても入れます", "Until 29 November an evening stop works too",
    "後楽園と岡山城は20:30まで開いています（入場は20:00まで）。夕方に岡山に着いて夜の庭とお城を見てから、広島へ進めます。岡山から広島への最終は23:14発（23:54着）です。",
    "The garden and castle are open until 20:30 (last entry 20:00), so you can arrive late, see both lit up and carry on. The last train to Hiroshima leaves Okayama at 23:14 (arrives 23:54).",
    U["garden_event"], to="2026-11-29")
N_SWAP = notice(
    "2日目が月曜日なら、2日を入れ替えてください", "If day 2 is a Monday, swap the days",
    "大原美術館は月曜休みです（祝日は開館）。日曜に着く人は、岡山10:40発の電車で倉敷へ（10:58着）。日曜のうちに美術館と町を見て泊まり、月曜は倉敷9:23発で岡山へ戻って（9:40着）、お城と後楽園、午後に吉備津神社の順にします。",
    "The Ohara Museum closes on Mondays (open on holidays). Arriving on a Sunday, take the 10:40 from Okayama to Kurashiki (10:58), see the museum and town that day and stay. On Monday take the 9:23 back to Okayama (9:40) for the castle and garden, then Kibitsu Shrine in the afternoon.",
    U["ohara"])
N_OHARA_DATES = notice(
    "この冬、月曜のほかに休む日", "Extra closures this winter",
    "2026年12月21〜25日・28日、2027年1月12〜15日も休館です。年末の12月29〜31日と1月2・3日は開館（9:00〜15:00、入館14:30まで）、元日は本館だけの開館です。",
    "The museum is also closed on 21–25 and 28 December 2026 and 12–15 January 2027. It opens 9:00–15:00 (last entry 14:30) on 29–31 December and 2–3 January; on New Year’s Day only the Main Gallery opens.",
    U["ohara_list"], to="2027-01-15")

# ---------------------------------------------------------------------------
# スポットの共通部分
# ---------------------------------------------------------------------------
S = dict(
    kyoto=dict(
        name=T("京都駅（新幹線）", "Kyoto Station (Shinkansen)"), kind=T("駅", "Station"),
        blurb=T("京都9:25発ののぞみで、岡山に10:25着。大阪からは新大阪9:41発の同じ列車です。",
                "The 9:25 Nozomi reaches Okayama at 10:25. From Osaka, board the same train at Shin-Osaka at 9:41."),
        lat=34.98535, lng=135.75877,
        body=T("三条のあたりからは、地下鉄で京都駅まで15〜17分・260円。三条京阪8:55発（土日は8:52発）で京都駅に9:10ごろ着きます。\n\n"
               "大阪から行く人は、新大阪9:41発の同じのぞみに乗ります（岡山まで44分・自由席5,610円）。新大阪までは御堂筋線で、梅田から6分・240円、なんばから約20分・290円です。",
               "From around Sanjo the subway to Kyoto Station takes 15–17 minutes (¥260): the 8:55 from Sanjo Keihan (8:52 at weekends) arrives at about 9:10.\n\n"
               "From Osaka, take the same Nozomi from Shin-Osaka at 9:41 (44 minutes to Okayama, ¥5,610 unreserved). The Midosuji subway reaches Shin-Osaka in 6 minutes from Umeda (¥240) and about 20 from Namba (¥290)."),
        gmaps=[gm("京都駅 新幹線のりば", "Kyoto Station (Shinkansen gates)", 34.98535, 135.75877, "京都駅 新幹線中央口")],
        rows=[row("train", "京都9:25 → 岡山10:25、新大阪9:41 → 岡山10:25（平日・土・日とも）", "Kyoto 9:25 → Okayama 10:25; Shin-Osaka 9:41 → Okayama 10:25 (weekdays and weekends)"),
              row("fee", "京都→岡山：自由席7,140円。のぞみの指定席は日によって変わります（11月25日は8,100円、28日は8,300円、12月30日は8,500円）",
                  "Kyoto–Okayama: ¥7,140 unreserved. Reserved Nozomi seats vary by date (¥8,100 on 25 Nov, ¥8,300 on 28 Nov, ¥8,500 on 30 Dec)"),
              row("fee", "新大阪→岡山：自由席5,610円。指定席は6,460円（11月25日）", "Shin-Osaka–Okayama: ¥5,610 unreserved; ¥6,460 reserved (25 Nov)")],
        tip=T("時刻と運賃は乗換案内で2026年11月25日（水）・28日（土）・29日（日）を確認しました。きっぷと荷物の決まりはJR東海・JR西日本・スマートEXの公式の説明です。写真は岡山駅で撮った新幹線（2025年9月）。",
              "Times and fares from a route planner for Wed 25, Sat 28 and Sun 29 November 2026. Ticket and luggage rules from JR Central, JR West and smartEX. The photo is a Shinkansen at Okayama (September 2025).")),

    okayamaeki=dict(
        name=T("岡山駅", "Okayama Station"), kind=T("駅・荷物", "Station & bags"),
        blurb=T("新幹線の改札を出たら、まず荷物。そのあと後楽園口（東口）から路面電車へ。",
                "Out of the Shinkansen gates, deal with bags first, then take the Korakuen (east) exit for the tram."),
        lat=34.66640, lng=133.91850,
        body=T("荷物を預けたら「後楽園口（東口）」へ下ります。駅前の広場に、犬・猿・きじを連れた桃太郎の像と噴水があり、その先の大通りのまん中が路面電車ののりばです（写真は2023年8月の夕方）。\n\n"
               "ロッカーは、新幹線の改札の外（24時間）、さんすて岡山南館2F（6:00〜24:00）、地下の一番街にもあります。空きはリンク先の地図で見られます。",
               "With bags stowed, go down to the Korakuen exit on the east side. In the square are a statue of Momotaro with his dog, monkey and pheasant, and a fountain; the tram stop is beyond them in the middle of the avenue (my photo is from an August evening in 2023).\n\n"
               "There are lockers outside the Shinkansen gates (24 hours), on 2F of Sun Station Terrace South (6:00–24:00) and in the underground mall. The linked map shows which are free."),
        gmaps=[gm("岡山駅 後楽園口（東口）", "Okayama Station, Korakuen exit", 34.66640, 133.91850, "岡山駅 東口 桃太郎像"),
               gm("ねこのてステーション", "Nekonote Station", 34.66630, 133.91790, "ねこのてステーション 岡山駅")],
        links=[NEKO, LOCKER, link("info", "岡山観光WEB", "Okayama Prefecture tourism website", "https://www.okayama-kanko.jp/", "https://www.okayama-japan.jp/en/")],
        rows=[row("hours", "ねこのてステーション：一時預かり8:00〜20:00、宿への配達の受付8:00〜13:30", "Nekonote Station: storage 8:00–20:00; hotel delivery accepted 8:00–13:30"),
              row("fee", "一時預かり600円（120cm・15kgまで）、800円（160cm・25kgまで）。宿への配達1,500円", "Storage ¥600 (up to 120 cm, 15 kg) or ¥800 (160 cm, 25 kg). Hotel delivery ¥1,500"),
              row("fee", "コインロッカーの料金は、JRの駅ページ・空き状況の地図・さんすて岡山のどこにも載っていません（要確認）", "Locker prices are not given on JR’s station page, the availability map or the station mall’s site (please check)")],
        tip=T("手荷物は岡山県の観光サイト、ロッカーの場所と時間はJRの駅ページからリンクされている空き状況の地図と、さんすて岡山の営業案内で確認しました。",
              "Luggage services from the prefecture’s tourism site; locker locations and hours from the availability map linked from JR’s station page and the station mall’s information page.")),

    tram=dict(
        name=T("路面電車（岡山駅前 → 城下）", "Tram: Okayama-ekimae → Shiroshita"), kind=T("路面電車", "Tram"),
        blurb=T("「東山」行きで3つ目の城下へ。8分・160円。交通系ICカードが使えます。",
                "A Higashiyama-bound tram to Shiroshita, the third stop: 8 minutes, ¥160. IC cards accepted."),
        lat=34.66575, lng=133.92895,
        body=T("行き先は2つあります。「東山（ひがしやま）」行きに乗ってください。「清輝橋（せいきばし）」行きは途中で曲がってしまいます。\n\n"
               "3つ目の「城下（しろした）」で降ります。始発の駅前はどのドアからも乗れて、お金は降りるときに前で。おつりは出ないので、現金なら両替機で160円にしてから入れます。交通系ICカードは使えますが、車内でチャージはできません。\n\n"
               "城下から岡山城までも、後楽園の正門までも、歩いて約10分。1日乗車券は400円ですが、往復の2回なら買わなくて大丈夫です。\n\n"
               "写真の青い電車は低床車の「MOMO」です（2023年8月）。2026年11月22日の時点では検査で運休しています。",
               "There are two destinations: take a tram for Higashiyama. Trams for Seikibashi turn off partway.\n\n"
               "Get off at Shiroshita, the third stop. At the terminus you can board by any door; pay at the front as you get off. No change is given, so break notes or coins in the machine to pay exactly ¥160. IC cards work but cannot be topped up on board.\n\n"
               "From Shiroshita it is about 10 minutes on foot to either the castle or Korakuen’s main gate. The ¥400 day pass isn’t worth it for a return trip.\n\n"
               "The blue tram in the photo is the low-floor MOMO (August 2023). As of 22 November 2026 it is out of service for inspection."),
        gmaps=[gm("城下電停", "Shiroshita tram stop", 34.66575, 133.92895, "城下駅 岡山電気軌道"), gm("岡山駅前電停", "Okayama-ekimae tram stop", 34.66585, 133.91960, "岡山駅前駅 岡山電気軌道")],
        links=[link("official", "岡山電気軌道（路面電車）", "Okayama Electric Tramway (Japanese)", U["tram"])],
        rows=[row("train", "岡山駅前10:44 → 城下10:52。帰りは城下14:25 → 岡山駅前14:32（平日・土・日とも）", "Okayama-ekimae 10:44 → Shiroshita 10:52; back 14:25 → 14:32 (weekdays and weekends)"),
              row("fee", "大人160円、子ども80円。1日乗車券400円", "¥160, children ¥80. Day pass ¥400")],
        tip=T("運賃・乗り方・MOMOの運休は岡山電気軌道の公式サイト、時刻は乗換案内で確認しました。", "Fares, boarding and MOMO’s suspension from the tramway’s website; times from a route planner.")),

    castle=dict(
        name=T("岡山城", "Okayama Castle"), kind=T("城", "Castle"),
        blurb=T("黒い板張りの天守から「烏城（うじょう）」と呼ばれる城。中は2022年に新しくなった展示室です。",
                "The “Crow Castle”, named for its black-boarded keep. Inside are exhibition rooms renewed in 2022."),
        caution=T("天守は再入場できません。12月29〜31日は休み", "No re-entry to the keep. Closed 29–31 December"),
        lat=34.66515, lng=133.93605,
        body=T("宇喜多秀家（うきたひでいえ）が築いた城です。天守は1945年の空襲で焼け、今の建物は1966年に建て直したコンクリート造り。2022年に「令和の大改修」が終わりました（私の写真は改修前の2021年3月）。\n\n"
               "天守の中は博物館で、古い木の階段や柱はありません。見学は50〜60分の人が多いそうです。時間がなければ外から眺めるだけにしても。エレベーターは4階までで、5・6階は階段です。\n\n"
               "見るところは、いびつな五角形の天守台、本丸の北西の角に残る江戸時代の月見櫓（つきみやぐら）、旭川と後楽園を見下ろす最上階。\n\n"
               "入場券は後楽園との共通券（800円）を。別々だと500円ずつです。天守の中に100円が戻るロッカーがあります。夜は毎日、日没から24時まで天守に明かりがつきます。",
               "Built by Ukita Hideie. The keep burned in the 1945 air raid; today’s is a concrete rebuild of 1966, renovated in 2022 (my photo is from March 2021, before that work).\n\n"
               "The inside is a museum, with no old timber stairs or pillars. Most visitors take 50–60 minutes. If time is short, look from outside. The lift goes to the 4th floor; the 5th and 6th are by stairs.\n\n"
               "Look for the irregular pentagonal base, the original Edo-period moon-viewing turret at the north-west corner, and the top-floor view over the river and Korakuen.\n\n"
               "Buy the combined ticket with Korakuen (¥800) instead of ¥500 each. There are coin-return lockers (¥100) in the keep. It is lit every night from sunset to midnight."),
        gmaps=[gm("岡山城 天守", "Okayama Castle keep", 34.66515, 133.93605, "岡山城 天守閣")],
        links=[link("official", "岡山城 公式サイト", "Okayama Castle (official)", U["castle"], "https://okayama-castle.jp/home-en/")],
        rows=[row("hours", "9:00〜17:30（入場は17:00まで）", "9:00–17:30 (last entry 17:00)"),
              row("hours", "11月20〜29日は20:30まで（入場は20:00まで）", "20–29 November until 20:30 (last entry 20:00)", until="2026-11-29"),
              row("closed", "12月29〜31日。荒天や点検で休む日もあります", "29–31 December; also for bad weather or inspections"),
              row("fee", "大人（15歳以上）500円、中学生以下無料。後楽園との共通券800円。カード・交通系IC・QR決済可", "¥500 (15+), junior high and under free. Combined with Korakuen ¥800. Cards, IC and QR payments accepted")],
        tip=T("岡山城の公式サイトで確認しました。再入場不可は2026年のお知らせにある案内です。改修後の写真は Wikimedia Commons から。",
              "Checked on the castle’s website; the no re-entry rule is from its 2026 news. Post-renovation photos are from Wikimedia Commons.")),

    tsukimi=dict(
        name=T("月見橋", "Tsukimi bridge"), kind=T("橋", "Bridge"),
        blurb=T("お城と後楽園をつなぐ歩行者の橋。ふり返ると、川の上に天守が立って見えます。",
                "The footbridge between castle and garden. Look back for the keep standing above the river."),
        lat=34.66640, lng=133.93486,
        body=T("天守の北側の「廊下門（ろうかもん）」を出て坂を下ると、旭川に架かる鉄の橋があります。渡った先が後楽園の南門です。\n\n"
               "橋のまん中でふり返ると、石垣の上の天守と川が一度に入ります（写真1枚目、2021年3月）。渡ってから右へ少し歩いた川べりからも撮れます（写真3枚目）。",
               "Leave by the Roka-mon gate north of the keep and walk down to the iron bridge over the Asahi river. Korakuen’s south gate is on the far side.\n\n"
               "Look back from the middle for keep, stone walls and river in one view (photo 1, March 2021). The riverbank a little to the right after crossing works too (photo 3)."),
        gmaps=[gm("月見橋", "Tsukimi bridge", 34.66640, 133.93486, "月見橋 岡山市北区")],
        rows=[row("hours", "自由に渡れます。天守から後楽園の南門まで歩いて5〜10分", "Free to cross. 5–10 minutes on foot from the keep to the garden’s south gate")],
        tip=T("歩く時間は地図で測った目安に、ゆとりを足したものです。", "The walking time is an estimate from the map, with some slack.")),

    korakuen=dict(
        name=T("岡山後楽園", "Okayama Korakuen"), kind=T("庭園（日本三名園）", "Garden"),
        blurb=T("広い芝生と池のむこうに天守。約300年前に岡山藩主がつくった庭です。お昼は正門の外で。",
                "Wide lawns and ponds with the keep beyond: a lord’s garden of about 300 years ago. Lunch is outside the main gate."),
        caution=T("10月〜3月19日は17:00まで（入園16:45まで）", "1 Oct–19 Mar: closes 17:00 (last entry 16:45)"),
        lat=34.66780, lng=133.93560,
        body=T("岡山藩主の池田綱政（いけだつなまさ）がつくらせた庭で、兼六園、偕楽園と並ぶ日本三名園の一つです。ひと回り1時間ほど。\n\n"
               "南門から入って、こう歩くと戻らずにすみます。\n\n"
               "・唯心山（ゆいしんざん）：小さな築山。芝生と池が一度に見えます。\n"
               "・流店（りゅうてん）：水路が建物の中を通る休憩所。\n"
               "・沢の池（さわのいけ）：園の中心の池。北側からふり返ると天守が入ります。\n"
               "・延養亭（えんようてい）：藩主が庭を眺めた建物。前からの眺めが、この庭の正面です。\n"
               "・鶴舎（かくしゃ）：タンチョウがいます。\n\n"
               "正門を出たところの「四季彩（しきさい）」で食事ができます（11:00〜14:30、年中無休。夜は予約制）。軽くすませるなら、岡山駅2階の駅弁売り場（7:00〜20:30）で買っても。\n\n"
               "帰りは正門から鶴見橋を渡って城下電停へ、歩いて約10分。日かげが少ないので夏は帽子と水を。",
               "Laid out for Ikeda Tsunamasa, lord of Okayama, and one of Japan’s three great gardens with Kenroku-en and Kairaku-en. Allow about an hour.\n\n"
               "From the south gate this order avoids doubling back.\n\n"
               "• Yuishinzan: a small hill with lawns and ponds in one view.\n"
               "• Ryuten: a rest pavilion with a stream running through it.\n"
               "• Sawa-no-ike: the central pond. Look back from its north side for the keep.\n"
               "• Enyo-tei: the lord’s viewing house. The view from in front is the garden’s “front”.\n"
               "• The aviary, with red-crowned cranes.\n\n"
               "Shikisai, just outside the main gate, serves lunch 11:00–14:30 every day (evenings by reservation). For something lighter, the boxed-meal shop on 2F at Okayama Station is open 7:00–20:30.\n\n"
               "From the main gate, cross Tsurumi bridge to the Shiroshita tram stop: about 10 minutes. There is little shade, so bring a hat and water in summer."),
        gmaps=[gm("後楽園 南門", "Korakuen south gate", 34.66690, 133.93470, "岡山後楽園 南門"), gm("後楽園 正門", "Korakuen main gate", 34.66930, 133.93420, "岡山後楽園 正門"), gm("四季彩", "Shikisai", 34.66935, 133.93400, "後楽園 四季彩")],
        links=[link("official", "岡山後楽園 公式サイト", "Okayama Korakuen (official)", U["garden"], "https://okayama-korakuen.jp/foregin_taravelers.html"),
               link("official", "四季彩 公式サイト", "Shikisai (official, Japanese)", U["shikisai"])],
        rows=[row("hours", "10月1日〜3月19日 8:00〜17:00（入園16:45まで）／3月20日〜9月30日 7:30〜18:00（入園17:45まで）", "1 Oct–19 Mar 8:00–17:00 (last entry 16:45) / 20 Mar–30 Sep 7:30–18:00 (last entry 17:45)"),
              row("hours", "11月20〜29日は20:30まで（入園20:00まで）", "20–29 November until 20:30 (last entry 20:00)", until="2026-11-29"),
              row("closed", "休みなし", "Open every day"),
              row("fee", "大人500円、65歳以上200円、高校生以下無料（2027年3月31日まで）。岡山城との共通券800円（シニア用はなし）", "¥500; 65+ ¥200; high school and under free (until 31 March 2027). Combined with the castle ¥800 (no senior version)"),
              row("hours", "四季彩：お食事11:00〜14:30、年中無休", "Shikisai: lunch 11:00–14:30, every day")],
        tip=T("後楽園・四季彩・さんすて岡山の公式サイトで確認しました。共通券を売らない日もあります。写真は Wikimedia Commons から。",
              "Checked on the websites of the garden, Shikisai and Sun Station Terrace. The combined ticket is withheld on some days. Photos are from Wikimedia Commons.")),

    kibitsu=dict(
        name=T("吉備津神社", "Kibitsu Shrine"), kind=T("神社（国宝の本殿と長い廻廊）", "Shrine"),
        blurb=T("桃太郎の話のもとになったとされる神社。国宝の本殿と、山すそを下る長い廻廊。岡山からJRで15分。",
                "The shrine linked to the Momotaro legend: a National Treasure hall and a long corridor down the hillside. 15 minutes by JR from Okayama."),
        caution=T("電車は本数が少ない。時刻を先に", "Trains are infrequent: fix your times first"),
        lat=34.67068, lng=133.85061,
        body=T("吉備津駅から、松並木の参道を歩いて約10分。吉備津彦命（きびつひこのみこと）が温羅（うら）という鬼を退治した話が伝わり、桃太郎のもとになったといわれます。\n\n"
               "・本殿と拝殿（国宝）：屋根が2つ並んだ「吉備津造り」。横に回ると形がよく分かります。\n"
               "・廻廊（かいろう）：山すそに沿ってまっすぐ下る、屋根つきの長い廊下。上からと下からの両方で見てください。\n\n"
               "お守りと御朱印は16時ごろまで。途中の御竈殿（おかまでん）の鳴釜神事は14:00までなので、この時間割では受けられません（金曜は休み）。",
               "About 10 minutes on foot from Kibitsu Station along an avenue of pines. Legend says Kibitsuhiko-no-mikoto defeated an ogre called Ura here, the story said to lie behind Momotaro.\n\n"
               "• Main and worship halls (National Treasure): twin roofs in the Kibitsu-zukuri style, best seen from the side.\n"
               "• The corridor: a long roofed passage straight down the foot of the hill. See it from both top and bottom.\n\n"
               "Amulets and seals until about 16:00. The Narukama cauldron ritual ends at 14:00 (none on Fridays), too early for this timetable."),
        gmaps=[gm("吉備津神社", "Kibitsu Shrine", 34.67068, 133.85061, "吉備津神社 岡山市"), gm("吉備津駅", "Kibitsu Station", 34.67441, 133.84605, "吉備津駅")],
        links=[link("official", "吉備津神社 公式サイト", "Kibitsu Shrine (official)", U["kibitsu"], "https://www.kibitujinja.com/en/"), JR],
        rows=[row("hours", "参拝5:00〜18:00。御守・御朱印9:00〜16:00ごろ。鳴釜神事9:00〜14:00", "Open 5:00–18:00. Amulets and seals 9:00 to about 16:00. Narukama 9:00–14:00"),
              row("closed", "鳴釜神事は金曜休み", "No Narukama on Fridays"),
              row("train", "岡山13:52 → 吉備津14:07、吉備津15:47 → 岡山16:05（平日・土・日とも）。片道210円", "Okayama 13:52 → Kibitsu 14:07; Kibitsu 15:47 → Okayama 16:05 (weekdays and weekends). ¥210 each way")],
        tip=T("吉備津神社の公式サイトと乗換案内で確認しました。写真は Wikimedia Commons から。", "Checked on the shrine’s website and a route planner. Photos are from Wikimedia Commons.")),

    lunch=dict(
        name=T("倉敷駅", "Kurashiki Station"), kind=T("駅", "Station"),
        blurb=T("岡山から16〜18分・330円。南口から美観地区まで歩いて10〜15分です。", "16–18 minutes from Okayama, ¥330. The old quarter is 10–15 minutes on foot from the south exit."),
        lat=34.60085, lng=133.76610,
        body=T("南口へ出ます。美観地区への道は、まっすぐ南への倉敷中央通りか、左手から続くアーケードの商店街。雨の日は商店街が楽です。\n\n"
               "荷物は駅のコインロッカーか、南口の西ビル2階の倉敷駅前観光案内所、美観地区の倉敷館・観光休憩所のロッカーへ。駅のロッカーは、JRの構内図では2階の改札の外（北口寄り）と、1階の南口の西側（駅レンタカーのそば）にあります（料金と使える時間は要確認）。案内所と休憩所のロッカーは9:00〜17:00の当日かぎりです。17:00を過ぎる日は駅のほうに預けてください。",
               "Use the south exit. Either follow Chuo-dori straight south, or the covered arcades from the left of the square, which are easier in rain.\n\n"
               "Bags go in the station lockers, or in lockers at the tourist office on 2F of the West Building by the south exit, at Kurashiki-kan or at the rest house in the old quarter. JR’s station map shows station lockers on 2F outside the ticket gates (towards the north exit) and on 1F at the west end of the south side, by the rent-a-car office (prices and hours not confirmed). The other three are same-day, 9:00–17:00 only. If you’ll be later than 17:00, use the station."),
        gmaps=[gm("倉敷駅 南口", "Kurashiki Station, south exit", 34.60085, 133.76610, "倉敷駅 南口"), gm("倉敷駅前観光案内所", "Kurashiki station-front tourist office", 34.60090, 133.76570, "倉敷駅前観光案内所")],
        links=[link("info", "倉敷駅前観光案内所", "Station-front tourist office (Japanese)", U["info_eki"]), link("info", "倉敷駅の構内図（JR西日本）", "Kurashiki Station map (JR West, Japanese)", U["kura_map"]), KTABI, JR],
        rows=[row("hours", "倉敷駅前観光案内所9:00〜18:00（12月29日〜1月1日休み）。ロッカーは9:00〜17:00", "Station-front office 9:00–18:00 (closed 29 Dec–1 Jan); its lockers 9:00–17:00"),
              row("fee", "倉敷駅のコインロッカー：2階の改札の外（北口寄り）と1階の南口の西側。料金と使える時間は公式で確かめられませんでした（要確認）", "Kurashiki Station lockers: 2F outside the gates (north side) and 1F west end of the south side. Prices and hours could not be confirmed (please check)")],
        tip=T("倉敷観光コンベンションビューロー、JRの駅ページと構内図（2024年4月1日時点）、乗換案内で確認しました。写真は Wikimedia Commons から。",
              "Checked with the Kurashiki visitors bureau, JR’s station page and station map (as of 1 April 2024) and a route planner. The photo is from Wikimedia Commons.")),

    ohara=dict(
        name=T("大原美術館", "Ohara Museum of Art"), kind=T("美術館", "Art museum"),
        blurb=T("エル・グレコ「受胎告知」、モネ「睡蓮」。1930年にできた西洋美術の美術館。月曜休みです。",
                "El Greco’s Annunciation and Monet’s Water Lilies, in a museum of Western art opened in 1930. Closed Mondays."),
        caution=T("月曜休み（祝日は開館）。12〜2月は15:00まで。館内は撮影禁止", "Closed Mondays (open on holidays). Until 15:00 Dec–Feb. No photos inside"),
        lat=34.59603, lng=133.77044,
        body=T("倉敷の実業家・大原孫三郎が、画家の児島虎次郎（こじまとらじろう）に集めてもらった絵をもとに開いた美術館です。柱の並ぶ本館が今橋の前に立っています。\n\n"
               "1枚の入館券で、本館、工芸・東洋館、児島虎次郎記念館に入れます。見ていない館は別の日にも使えます。分館は長く休館中です。1時間なら本館だけに、もう30分あれば米蔵を使った工芸・東洋館へ。\n\n"
               "荷物は入館券売場の隣で無料で預かってくれます。",
               "Opened by the Kurashiki industrialist Ohara Magosaburo around pictures the painter Kojima Torajiro collected for him. The columned main building faces Imabashi.\n\n"
               "One ticket covers the Main Gallery, the Craft and Asian Art Gallery and the Kojima Torajiro Memorial Hall; unused halls can be visited another day. The Annex is closed long-term. With an hour, see the Main Gallery; with 30 minutes more, add the galleries in the old rice storehouses.\n\n"
               "Bags are looked after free next to the ticket office."),
        gmaps=[gm("大原美術館 本館", "Ohara Museum of Art, Main Gallery", 34.59603, 133.77044, "大原美術館")],
        links=[link("official", "大原美術館 公式サイト", "Ohara Museum of Art (official)", U["ohara"], "https://www.ohara.or.jp/en/"), link("info", "開館情報一覧", "Opening days (Japanese)", U["ohara_list"]), link("info", "開館カレンダー（PDF）", "Opening calendar (PDF, Japanese)", U["ohara_cal"])],
        rows=[row("hours", "3〜11月 9:00〜17:00（入館16:30まで）／12〜2月 9:00〜15:00（入館14:30まで）。児島虎次郎記念館は10:00〜16:00（冬は15:00まで）", "Mar–Nov 9:00–17:00 (last entry 16:30) / Dec–Feb 9:00–15:00 (last entry 14:30). Kojima hall 10:00–16:00 (15:00 in winter)"),
              row("closed", "月曜（祝日・振替休日は開館。8月は無休）。臨時休館あり", "Mondays (open on holidays; none in August). Occasional extra closures"),
              row("fee", "一般2,000円、18歳未満の小〜高校生500円。現金・カード・電子マネー・QR決済可", "¥2,000; school pupils under 18 ¥500. Cash, cards, e-money and QR accepted")],
        tip=T("大原美術館の公式サイト（入館案内・開館情報一覧）と2026年度の開館カレンダーで確認しました。写真は Wikimedia Commons から。", "Checked on the museum’s website (visitor information and opening days) and 2026 calendar. Photos are from Wikimedia Commons.")),

    bikan=dict(
        name=T("倉敷川と白壁の町並み", "Kurashiki canal and the white-walled quarter"), kind=T("町並み", "Old quarter"),
        blurb=T("柳の川ぞいに蔵と屋敷。夜は21時（4〜9月は22時）まで明かりがつきます。",
                "Storehouses along a willow-lined canal, lit until 21:00 (22:00 April–September)."),
        lat=34.59610, lng=133.77105,
        body=T("江戸時代、このあたりの米や綿を舟で運び出した川です。両岸の蔵と屋敷は商人たちのもの。\n\n"
               "・今橋（いまばし）：美術館の前の石橋。ここから川下を見るのが定番の眺めです。\n"
               "・中橋（なかばし）と倉敷館：川が曲がる角の石橋と、洋風の木造の観光案内所。\n"
               "・高砂橋（たかさごばし）：舟が折り返すあたり。\n\n"
               "夜間景観照明は日没から、10〜3月は21:00、4〜9月は22:00まで。11〜12月の日の入りは17時前後です。",
               "This canal carried the district’s rice and cotton away by boat in the Edo period; the buildings along it were the merchants’.\n\n"
               "• Imabashi: the stone bridge before the museum, for the classic view downstream.\n"
               "• Nakabashi and Kurashiki-kan: the bridge at the bend and the wooden Western-style tourist office.\n"
               "• Takasago-bashi: where the boats turn.\n\n"
               "The night lighting runs from sunset to 21:00 October–March and 22:00 April–September. In November and December the sun sets at about 17:00."),
        gmaps=[gm("中橋・倉敷館", "Nakabashi & Kurashiki-kan", 34.59582, 133.77176, "倉敷館観光案内所"), gm("今橋", "Imabashi", 34.59640, 133.77065, "今橋 倉敷美観地区")],
        links=[link("info", "夜間景観照明", "Night lighting (Japanese)", U["lights"]), KTABI],
        rows=[row("hours", "町並みは自由に歩けます。夜間景観照明：日没〜21:00（4〜9月は22:00）", "Free to walk. Night lighting: sunset–21:00 (22:00 April–September)"),
              row("hours", "倉敷館観光案内所9:00〜18:00（12月31日・1月1日休み）", "Kurashiki-kan 9:00–18:00 (closed 31 Dec and 1 Jan)")],
        tip=T("倉敷観光WEB、倉敷観光コンベンションビューロー、国立天文台の日の入りの表で確認しました。写真は Wikimedia Commons から。",
              "Checked on the Kurashiki tourism website, with the visitors bureau and on the national observatory’s sunset table. Photos are from Wikimedia Commons.")),

    boat=dict(
        name=T("くらしき川舟流し", "Kurashiki river boat"), kind=T("川舟（約20分）", "Canal boat (about 20 min)"),
        blurb=T("小さな舟で倉敷川を約20分。1艘6人なので、WEB予約か朝9時の当日券を。",
                "Twenty minutes on the canal. Six to a boat, so book online or buy at 9:00 on the day."),
        caution=T("売り切れ・雨で中止あり。第2月曜休み、1〜2月は土日祝だけ", "Sells out; cancelled in rain. No boats 2nd Monday; weekends and holidays only Jan–Feb"),
        lat=34.59570, lng=133.77150,
        body=T("すげ笠をかぶって、石垣と白壁を下から見上げます。船頭さんの案内は日本語だけです。\n\n"
               "券は2通りです。\n"
               "・WEB予約：乗る日の30日前の0:00から。前日15:00までは取り消せます。12:00と12:30の便にはありません。\n"
               "・当日券：9:00から倉敷館観光案内所で、便ごとに先着順。土日祝は午前中に売り切れることもあります。WEBが満席でも別の枠です。\n\n"
               "乗り場は倉敷館の対岸。乗り遅れは払い戻しがありません。雨傘も日傘もさせません。",
               "In a sedge hat, you look up at the stone banks and white walls. The boatman’s commentary is Japanese only.\n\n"
               "Two ways to get a ticket.\n"
               "• Online: from 0:00, 30 days ahead; free cancellation until 15:00 the day before. None for the 12:00 and 12:30 boats.\n"
               "• On the day: from 9:00 at Kurashiki-kan, per departure, first come first served. On weekends and holidays they can be gone by late morning. These seats are separate from online ones.\n\n"
               "The landing is opposite Kurashiki-kan. No refund if you miss the boat, and no umbrellas or parasols on board."),
        gmaps=[gm("川舟乗り場", "Boat landing", 34.59570, 133.77150, "くらしき川舟流し 乗船場"), gm("倉敷館観光案内所（当日券）", "Kurashiki-kan (same-day tickets)", 34.59582, 133.77176, "倉敷館観光案内所")],
        links=[link("official", "くらしき川舟流し 公式ページ（WEB予約）", "River boat: official page and booking (Japanese)", U["boat"]),
               link("info", "運航状況（Instagram）", "Today’s operation (Instagram, Japanese)", "https://www.instagram.com/kurashiki_riverboat/")],
        rows=[row("hours", "9:30〜17:00発、30分おき。夏は15:30以降の便が運休することも", "Departures 9:30–17:00, every 30 min. Boats from 15:30 may be cancelled in summer"),
              row("hours", "夜の川舟：11月28日までの土曜18:00〜19:00（3便）", "Evening boats: Saturdays until 28 November, 18:00–19:00 (three boats)", until="2026-11-28"),
              row("closed", "3〜12月の第2月曜（祝日は運航）、1〜2月の平日、12月29日〜1月3日。雨・強風・低水位は中止", "2nd Monday Mar–Dec (runs on holidays), weekdays Jan–Feb, 29 Dec–3 Jan. Cancelled in rain, wind or low water"),
              row("fee", "大人1,000円、5歳〜小学生500円、5歳未満無料", "¥1,000; age 5 to elementary school ¥500; under 5 free")],
        tip=T("倉敷観光コンベンションビューローの公式ページと「よくある質問」で確認しました。写真は Wikimedia Commons から。", "Checked on the visitors bureau’s official page and FAQ. Photos are from Wikimedia Commons.")),

    ivy=dict(
        name=T("倉敷アイビースクエア", "Kurashiki Ivy Square"), kind=T("赤れんがの工場あと", "Former brick mill"),
        blurb=T("明治の紡績工場を使ったホテルと広場。つたのからむ中庭は、泊まらなくても歩けます。",
                "A Meiji cotton mill turned hotel. The ivy-walled courtyard is open to non-guests."),
        lat=34.59470, lng=133.77350,
        body=T("1889年にできた倉敷紡績所の最初の工場です。外壁と骨組みを残して、建築家・浦辺鎮太郎（うらべしずたろう）がホテルに作りかえました。\n\n"
               "見るのは中庭。つたは夏に緑、秋に赤、冬は葉が落ちます。西の門から入って東の門へ抜けると、本町通りへの近道です。\n\n"
               "敷地の中の「倉紡記念館」は、倉敷紡績の歩みを見せる資料館です。10:00〜16:00（入館15:45まで）、年中無休、一般300円。",
               "The first mill of the Kurashiki Spinning Works, built in 1889. The architect Urabe Shizutaro turned it into a hotel, keeping walls and frame.\n\n"
               "The courtyard is the thing to see: ivy green in summer, red in autumn, bare in winter. In by the west gate and out by the east is a short cut to Honmachi.\n\n"
               "The Kurabo Memorial Hall in the grounds tells the spinning company’s story: 10:00–16:00 (last entry 15:45), every day, ¥300."),
        gmaps=[gm("倉敷アイビースクエア", "Kurashiki Ivy Square", 34.59470, 133.77350, "倉敷アイビースクエア")],
        links=[link("official", "倉敷アイビースクエア 公式サイト", "Kurashiki Ivy Square (official)", U["ivy"]),
               link("official", "倉紡記念館（倉敷紡績）", "Kurabo Memorial Hall (Japanese)", U["kurabo"])],
        rows=[row("hours", "中庭は自由に歩けます。倉紡記念館：10:00〜16:00（入館15:45まで）、年中無休", "The courtyard is free to walk through. Kurabo Memorial Hall: 10:00–16:00 (last entry 15:45), every day"),
              row("fee", "倉紡記念館：一般300円、学生250円、小学生未満無料", "Kurabo Memorial Hall: ¥300, students ¥250, under school age free")],
        tip=T("建物の歴史は公式サイト、倉紡記念館は倉敷紡績の公式ページで確認しました。写真は Wikimedia Commons から。", "The history is from the official website; the memorial hall from Kurabo’s own page. Photos are from Wikimedia Commons.")),

    achi=dict(
        name=T("阿智神社", "Achi Shrine"), kind=T("神社（町を見下ろす丘）", "Shrine on the hill"),
        blurb=T("鶴形山の上。石段を3〜4分上ると、美観地区の瓦屋根を見下ろせます。",
                "On Tsurugata hill: 3–4 minutes of steps to a view over the tiled roofs."),
        caution=T("日が暮れると石段は暗い。明るいうちに", "The steps are dark after sunset: go in daylight"),
        lat=34.59720, lng=133.77344,
        body=T("本町通りから石段を上ります。上りきってふり返るか、境内の南の端の絵馬殿から、瓦屋根の重なりが見えます。\n\n"
               "参拝はいつでもできますが、授与所は17:00まで。秋と冬は日が暮れる前に上ってください。",
               "Climb the steps from Honmachi. Turn round at the top, or go to the votive-tablet hall at the south edge, for the layers of tiled roofs.\n\n"
               "Open at all hours, but the amulet office closes at 17:00. In autumn and winter climb before dusk."),
        gmaps=[gm("阿智神社", "Achi Shrine", 34.59720, 133.77344, "阿智神社 倉敷市本町")],
        links=[link("official", "阿智神社 公式サイト", "Achi Shrine (official, Japanese)", U["achi"])],
        rows=[row("hours", "参拝は終日。授与所9:00〜17:00", "Open all day. Amulet office 9:00–17:00"), row("fee", "無料", "Free")],
        tip=T("阿智神社の公式サイトで確認しました。写真は Wikimedia Commons から。", "Checked on the shrine’s website. Photos are from Wikimedia Commons.")),

    honmachi=dict(
        name=T("本町・東町", "Honmachi & Higashimachi"), kind=T("町家の通り", "Townhouse streets"),
        blurb=T("川ぞいの一本北、格子の町家の通り。東へ行くほど、ふつうの暮らしの町になります。",
                "One street north of the canal, lined with latticed townhouses, more residential the further east you go."),
        lat=34.59640, lng=133.77400,
        body=T("鶴形山のふもとの昔の街道です。格子窓、しっくいと焼き板の壁の町家に、帆布、マスキングテープ、器などの店が入っています。\n\n"
               "東へ歩くと東町（ひがしまち）。店が減って、静かな家並みになります。端まで行って戻って15分ほど。住んでいる人の家なので、戸口や中は撮らないように。\n\n"
               "「三宅商店」は本町通りの町家のカフェで、野菜のカレーと季節のパフェがあります。平日11:30、土曜11:00、日曜8:30から17:00まで（L.O.16:30）、年中無休です。",
               "An old highway at the foot of Tsurugata hill. Townhouses with lattice windows, plaster and charred-board walls hold shops for canvas, masking tape and tableware.\n\n"
               "East is Higashimachi, where shops thin out into a quiet street of homes: about 15 minutes to the end and back. People live here, so don’t photograph doorways or interiors.\n\n"
               "Miyake Shoten is a townhouse cafe on Honmachi with vegetable curry and seasonal parfaits. It opens at 11:30 on weekdays, 11:00 on Saturdays and 8:30 on Sundays, until 17:00 (last order 16:30), every day."),
        gmaps=[gm("本町通り", "Honmachi street", 34.59640, 133.77400, "倉敷市本町 本町通り"), gm("東町", "Higashimachi", 34.59672, 133.77706, "倉敷市東町"), gm("三宅商店", "Miyake Shoten", 34.59640, 133.77290, "三宅商店 倉敷市本町")],
        links=[link("official", "三宅商店 営業時間", "Miyake Shoten hours (Japanese)", U["miyake"]), KTABI],
        rows=[row("hours", "通りは自由に歩けます。ほかの店の時間と休みは店ごとに違います", "Free to walk. Other shops’ hours and closing days vary"),
              row("hours", "三宅商店：平日11:30、土11:00、日8:30〜17:00（L.O.16:30）、年中無休", "Miyake Shoten: from 11:30 weekdays, 11:00 Sat, 8:30 Sun, to 17:00 (last order 16:30), every day")],
        tip=T("三宅商店は公式サイトで確認しました。通りの説明は倉敷観光WEBによります。写真は Wikimedia Commons から。", "Miyake Shoten was checked on its website. The street description draws on the Kurashiki tourism website. Photos are from Wikimedia Commons.")),

    kaeri=dict(
        name=T("岡山駅（次の町へ）", "Okayama Station (onward)"), kind=T("駅", "Station"),
        blurb=T("新幹線で、京都・大阪へも広島へも。", "Shinkansen for Kyoto, Osaka or Hiroshima."),
        lat=34.66668, lng=133.91740,
        body=T("在来線からは乗り換え口まで5分、荷物を取るなら10分はみてください。きびだんごなどのおみやげと駅弁は、改札のある2階で買えます。\n\n"
               "岡山駅で晩ごはんにするなら、さんすて岡山2Fの「吾妻寿司」が22:00まで（L.O.21:00）、年中無休。ばら寿司やままかりの店です。\n\n"
               "写真は岡山駅の新幹線ホーム（2021年3月）。",
               "Allow 5 minutes from the local platforms to the transfer gate, 10 if collecting bags. Souvenirs such as kibi-dango and boxed meals are sold on 2F, the same floor as the gates.\n\n"
               "For dinner at the station, Azumazushi on 2F of Sun Station Terrace is open until 22:00 (last order 21:00), every day, serving bara-zushi and mamakari.\n\n"
               "The photo is the Shinkansen platform at Okayama (March 2021)."),
        gmaps=[gm("岡山駅 新幹線のりば", "Okayama Station (Shinkansen)", 34.66668, 133.91740, "岡山駅 新幹線"), gm("吾妻寿司 さんすて岡山店", "Azumazushi, Sun Station Terrace", 34.66546, 133.91779, "吾妻寿司 さんすて岡山店")],
        links=[JR, link("official", "吾妻寿司 公式サイト", "Azumazushi (official, Japanese)", U["azuma"])],
        rows=[row("hours", "吾妻寿司：11:00〜22:00（L.O.21:00）、年中無休。売り切れで早く閉まることも", "Azumazushi: 11:00–22:00 (last order 21:00), every day; may close early when sold out")],
        tip=T("時刻は乗換案内（2026年11月25日・28日・29日）、吾妻寿司は公式サイトで確認しました。", "Times from a route planner (25, 28 and 29 November 2026); Azumazushi from its website.")),
)

# ---------------------------------------------------------------------------
# コースごとの時間割
#   pre: 名前のすぐ下に出る段落、time: いちばん下の行、notices・rows・caution・blurb・name は共通部分に足す／入れ替える
# ---------------------------------------------------------------------------
STAY = dict(
    file="okayama.json", course="stay",
    order=["kyoto", "okayamaeki", "tram", "castle", "tsukimi", "korakuen", "lunch", "ivy", "achi", "bikan",
           "honmachi", "ohara", "boat", "kibitsu", "kaeri"],
    day2="honmachi",
    spots=dict(
        kyoto=dict(
            pre=T("1日目は岡山のお城と庭、夕方から倉敷で泊まり。2日目は朝の倉敷を歩いて、吉備津神社へ寄ってから帰るか、広島へ進みます。\n\n宿は、倉敷美観地区のまわりが夜も朝もいちばん楽です。倉敷駅のまわりなら美観地区まで歩いて10〜15分。岡山駅のまわりに泊まっても回れます。夜は倉敷20:49発の電車で岡山に21:05着です。",
                  "Day 1 is Okayama’s castle and garden, then the evening and night in Kurashiki. On day 2, walk early Kurashiki, stop at Kibitsu Shrine, and go home or on to Hiroshima.\n\nThe Kurashiki old quarter is the easiest place to stay for both night and morning. Around Kurashiki Station you are 10–15 minutes’ walk away. Around Okayama Station works too: the 20:49 from Kurashiki gets back at 21:05."),
            caution=T("2日目が月曜なら、2日を入れ替え（大原美術館が休み）", "If day 2 is a Monday, swap the days (Ohara Museum closed)"),
            notices=[N_SWAP, N_BAGS_STAY, N_RESERVED, N_BIG, N_NIGHT_STAY,
                     notice("2日目に広島へ進む人のきっぷ", "Tickets if you go on to Hiroshima",
                            "京都・新大阪→広島の乗車券は3日間有効で、岡山で途中下車できます。特急券は岡山で区切って2枚。乗車券は後戻りする向きには使えないので、岡山から倉敷・吉備津へ往復する分は別に買います（片道で岡山〜倉敷330円、岡山〜吉備津210円）。スマートEXは途中下車できないので、区間ごとに予約します。",
                            "A fare ticket from Kyoto or Shin-Osaka to Hiroshima is valid three days and allows a stopover at Okayama. Buy two express tickets, split there. A fare ticket can’t be used to travel back the way you came, so buy separate tickets for the return trips from Okayama to Kurashiki and Kibitsu (one way: ¥330 to Kurashiki, ¥210 to Kibitsu). smartEX allows no stopovers, so book each section.",
                            U["faq_stop"])],
            links=[JR, link("info", "途中下車の決まり（JR西日本）", "Stopover rules (JR West, Japanese)", U["faq_stop"]), STOPOVER, EX],
            time=(DEP, "1日目 9:25発（京都駅に9:10ごろ）", "day 1, the 9:25 train (be at Kyoto Station by about 9:10)")),
        okayamaeki=dict(
            caution=T("宿への荷物の配達は13:30まで受付", "Hotel bag delivery: hand in by 13:30"),
            notices=[N_BAGS_STAY],
            time=(VIS, "1日目 10:25〜10:40", "day 1, 10:25–10:40")),
        tram=dict(
            pre=T("10:44発に乗ると、城下に10:52。次の10:50発でも10:58に着きます。", "The 10:44 reaches Shiroshita at 10:52; the 10:50 also works (10:58)."),
            time=(MOV, "1日目 10:44〜10:52", "day 1, 10:44–10:52")),
        castle=dict(time=(VIS, "1日目 11:05〜12:00", "day 1, 11:05–12:00")),
        tsukimi=dict(time=(VIS, "1日目 12:00〜12:15", "day 1, 12:00–12:15")),
        korakuen=dict(
            pre=T("12:15から庭を1時間、13:20から正門の外でお昼。14:10に出れば、城下14:25発の電車で岡山駅前に14:32着。岡山15:04発の電車で倉敷へ向かいます。",
                  "An hour in the garden from 12:15, lunch outside the main gate from 13:20. Leave at 14:10 for the 14:25 tram (station 14:32) and the 15:04 train to Kurashiki."),
            time=(VIS, "1日目 12:15〜14:10（お昼を含む）", "day 1, 12:15–14:10 (including lunch)")),
        lunch=dict(
            pre=T("岡山15:04発の山陽本線で、倉敷に15:20。宿に寄るか荷物を置いて、明るいうちにアイビースクエアと阿智神社へ。",
                  "The 15:04 Sanyo line train from Okayama arrives at 15:20. Drop in at your hotel, then Ivy Square and Achi Shrine while it is light."),
            rows=[row("train", "岡山15:04 → 倉敷15:20（平日・土・日とも）。330円", "Okayama 15:04 → Kurashiki 15:20 (weekdays and weekends). ¥330")],
            time=(MOV, "1日目 15:04〜15:20", "day 1, 15:04–15:20")),
        ivy=dict(
            pre=T("この時間には倉紡記念館は閉まっています（入館15:45まで）。入りたい人は2日目の朝、美術館のあとに。",
                  "By this time the Kurabo Memorial Hall has closed (last entry 15:45). To go in, fit it in after the museum on day 2."),
            time=(VIS, "1日目 16:00〜16:20", "day 1, 16:00–16:20")),
        achi=dict(
            pre=T("日の入りの前に上ります。11月下旬の日の入りは16:55ごろ。", "Climb before sunset, which is at about 16:55 in late November."),
            time=(VIS, "1日目 16:30〜16:50", "day 1, 16:30–16:50")),
        bikan=dict(
            name=T("夕暮れ〜夜の倉敷川", "The canal from dusk into night"), kind=T("町並み・夜", "Old quarter by night"),
            blurb=T("明かりがつく倉敷川を歩いて晩ごはん。照明は21時（4〜9月は22時）まで。",
                    "Walk the canal as the lamps come on, then dinner. Lit until 21:00 (22:00 April–September)."),
            caution=T("夜の店はラストオーダーが早めなので、先に決めて", "Last orders come early: pick dinner in advance"),
            pre=T("17:00ごろから明かりのつく川ぞいを歩いて、18:15ごろ晩ごはん。食べ終わったら、照明の消える21:00までもう一度川ぞいへ。\n\n"
                  "晩ごはんの例は、倉敷国際ホテルのレストラン「ウイステリア」。17:00〜21:00（L.O.20:00）で、ディナーのコースは6,160円から（サービス料別）。もっと気軽な店は、倉敷市の観光サイトが紹介している「夜めぐりマップ」（230店、ラストオーダーと定休日つき）を観光案内所でもらって選んでください。\n\n"
                  "そのあと飲むなら、同じホテルの「バー レジーナ」が18:00〜24:00（日・月休み）。",
                  "Walk the canal from about 17:00 as it lights up and eat at about 18:15. Afterwards walk it again until the lights go off at 21:00.\n\n"
                  "One dinner option is Wisteria at the Kurashiki Kokusai Hotel: 17:00–21:00 (last order 20:00), courses from ¥6,160 plus service. For something more casual, pick up the city’s night dining map at a tourist office (230 places, with last orders and closing days; Japanese and traditional Chinese).\n\n"
                  "For a drink afterwards, Bar Regina in the same hotel is open 18:00–24:00 (closed Sundays and Mondays)."),
            gmaps_add=[gm("倉敷国際ホテル（ウイステリア・バー）", "Kurashiki Kokusai Hotel (Wisteria & bar)", 34.59650, 133.76985, "倉敷国際ホテル")],
            links_add=[link("official", "倉敷国際ホテル レストラン＆バー", "Kurashiki Kokusai Hotel restaurants (Japanese)", U["hotel_rest"]),
                       link("info", "夜めぐりマップ", "Night dining map (Japanese)", U["nightmap"])],
            rows=[row("hours", "ウイステリア：夜17:00〜21:00（L.O.20:00）／バー レジーナ：18:00〜24:00（日・月休み）", "Wisteria: 17:00–21:00 (last order 20:00) / Bar Regina: 18:00–24:00 (closed Sun and Mon)")],
            time=(VIS, "1日目 17:00〜21:00（晩ごはんを含む）", "day 1, 17:00–21:00 (including dinner)")),
        honmachi=dict(
            name=T("朝の本町・東町と倉敷川", "Honmachi, Higashimachi and the canal in the morning"),
            blurb=T("泊まった人の時間。店が開く前の町家の通りと、川ぞいを歩きます。", "The reward for staying: townhouse streets and canal before the shops open."),
            pre=T("7:30ごろ宿を出ます。店が開く前なので、通りも川ぞいも昼より静かです。朝ごはんは宿で。日曜なら三宅商店が8:30から開いています（美術館に入るのは少し遅くなります）。",
                  "Leave at about 7:30. Before the shops open, both street and canal are quieter than by day. Have breakfast at your hotel; on Sundays Miyake Shoten opens at 8:30, which puts you into the museum a little later."),
            time=(VIS, "2日目 7:30〜8:45", "day 2, 7:30–8:45")),
        ohara=dict(
            pre=T("9:00の開館に入ります。冬は15:00で閉まりますが、朝なら関係ありません。10:40ごろ出て、11:30から本町の三宅商店でお昼（平日は11:30開店、土曜は11:00、日曜は8:30）。食べたら荷物を取って、倉敷13:11発の電車へ。",
                  "Go in at the 9:00 opening; the early winter closing doesn’t matter in the morning. Out at about 10:40, lunch from 11:30 at Miyake Shoten on Honmachi (opens 11:30 weekdays, 11:00 Saturdays, 8:30 Sundays), collect bags and catch the 13:11 train."),
            notices=[N_SWAP, N_OHARA_DATES],
            time=(VIS, "2日目 9:00〜10:40", "day 2, 9:00–10:40")),
        boat=dict(
            pre=T("乗るなら、美術館のあとの11:00の便を。WEB予約がなければ、美術館に入る前、9:00に倉敷館で当日券を買います。",
                  "If you ride, take the 11:00 after the museum. Without an online booking, buy at Kurashiki-kan at 9:00 before going into the museum."),
            time=(VIS, "2日目 11:00〜11:20（時間割では寄り道）", "day 2, 11:00–11:20 (optional)")),
        kibitsu=dict(
            pre=T("倉敷13:11発で岡山13:28着。荷物をロッカーに入れて、岡山13:52発の桃太郎線（吉備線）で吉備津に14:07着。帰りは吉備津15:47発で岡山16:05着です。",
                  "The 13:11 from Kurashiki reaches Okayama at 13:28. Put bags in a locker and take the 13:52 Momotaro line (Kibi line) to Kibitsu (14:07). Return on the 15:47 (Okayama 16:05)."),
            time=(VIS, "2日目 14:20〜15:30", "day 2, 14:20–15:30")),
        kaeri=dict(
            blurb=T("16:20発で京都17:20・新大阪17:04。広島へは16:26発で17:02着。", "The 16:20 reaches Kyoto 17:20 and Shin-Osaka 17:04. For Hiroshima, the 16:26 arrives 17:02."),
            pre=T("・京都へ：のぞみ16:20発 → 17:20着（自由席7,140円）。\n・新大阪へ：同じ列車で17:04着（5,610円）。\n・広島へ：のぞみ16:26発 → 17:02着（5,610円）。\n\n"
                  "京都に着いてからも街なかで晩ごはんが食べられる時間です。もっと岡山に残るなら、京都へ乗り換えなしの最後は21:44発（22:45着）。22:48発のみずほに乗ると新大阪で新快速に乗り換えて0:30着ですが、地下鉄（三条へ行ける最終は京都駅23:25発）には間に合いません。新大阪へは22:48発（23:37着）、広島へは23:14発（23:54着）が最終です。",
                  "• Kyoto: the 16:20 Nozomi arrives 17:20 (¥7,140 unreserved).\n• Shin-Osaka: the same train, 17:04 (¥5,610).\n• Hiroshima: the 16:26 Nozomi arrives 17:02 (¥5,610).\n\n"
                  "That leaves time for dinner in town in Kyoto. Staying later, the last direct train to Kyoto is the 21:44 (22:45). The 22:48 Mizuho, changing to a Special Rapid at Shin-Osaka, arrives at 0:30, too late for the subway (last for Sanjo leaves Kyoto Station at 23:25). Last trains: Shin-Osaka 22:48 (23:37), Hiroshima 23:14 (23:54)."),
            rows=[row("train", "岡山16:20 → 京都17:20／新大阪17:04、岡山16:26 → 広島17:02（平日・土・日とも）", "Okayama 16:20 → Kyoto 17:20 / Shin-Osaka 17:04; 16:26 → Hiroshima 17:02 (weekdays and weekends)"),
                  row("train", "最終：京都へ乗り換えなし21:44（22:45着）、新大阪へ22:48、広島へ23:14", "Last trains: direct to Kyoto 21:44 (22:45), Shin-Osaka 22:48, Hiroshima 23:14")],
            time=(DEP, "2日目 16:20発（広島へは16:26発）", "day 2, 16:20 (16:26 for Hiroshima)")),
    ))

STOP = dict(
    file="okayama-stop.json", course="stop",
    order=["kyoto", "okayamaeki", "tram", "castle", "tsukimi", "korakuen",
           "lunch", "ohara", "honmachi", "bikan", "boat", "ivy", "achi", "kaeri"],
    spots=dict(
        kyoto=dict(
            pre=T("広島へ行く途中に、岡山で降ります。9:25ののぞみに乗ると、お城と後楽園とお昼で広島に15:42着。\n\n"
                  "使える時間（岡山駅に着いてから出るまで）で選んでください。\n"
                  "・3時間：後楽園と月見橋だけ。\n"
                  "・4時間40分：お城、後楽園、お昼。最初はこれを選んであります。\n"
                  "・5時間半：岡山はやめて、倉敷の美術館と町並み（広島に16:27着）。\n"
                  "・岡山と倉敷の両方：9時間はかかります。立ち寄りではなく「1泊2日」のコースにしてください。\n\n"
                  "きっぷの合計（自由席、岡山だけに寄る場合）：\n"
                  "・京都から：乗車券を通しにして特急券2枚で12,530円。全部区間ごとに買うと12,750円。寄らなければ10,770円。\n"
                  "・新大阪から：通しの乗車券で10,780円。区間ごとだと11,220円。寄らなければ9,890円。\n"
                  "・スマートEX（のぞみ指定席・通常期）を2つに分けると、京都から14,160円、新大阪から12,520円。\n\n"
                  "逆向き（広島 → 京都・大阪）は、広島9:29発ののぞみで岡山10:04着。同じ順に回って、岡山15:20発で新大阪16:04・京都16:20着です。",
                  "Get off at Okayama on the way to Hiroshima. Take the 9:25 Nozomi and, with castle, garden and lunch, you reach Hiroshima at 15:42.\n\n"
                  "Choose by the time you have between arriving at and leaving Okayama Station.\n"
                  "• 3 hours: Korakuen and Tsukimi bridge only.\n"
                  "• 4 hours 40: castle, garden and lunch. This is selected to start with.\n"
                  "• 5½ hours: skip Okayama for Kurashiki’s museum and old quarter (Hiroshima 16:27).\n"
                  "• Both towns: at least 9 hours. That is not a stopover, so use the overnight course.\n\n"
                  "Ticket totals (unreserved, stopping at Okayama only):\n"
                  "• From Kyoto: ¥12,530 with a through fare ticket and two express tickets; ¥12,750 bought section by section; ¥10,770 without stopping.\n"
                  "• From Shin-Osaka: ¥10,780 with a through fare ticket; ¥11,220 by section; ¥9,890 without stopping.\n"
                  "• Two smartEX bookings (reserved Nozomi, regular season): ¥14,160 from Kyoto, ¥12,520 from Shin-Osaka.\n\n"
                  "The other way (Hiroshima to Kyoto or Osaka): the 9:29 Nozomi from Hiroshima reaches Okayama at 10:04. Do the same round and take the 15:20 (Shin-Osaka 16:04, Kyoto 16:20)."),
            caution=T("スマートEXの通しでは途中下車不可。岡山で区切って買う。荷物は改札の外で預ける", "No stopovers on a through smartEX ticket: split at Okayama. Leave bags outside the gates"),
            notices=[N_TICKET, N_BAGS_STOP, N_BIG, N_RESERVED, N_NIGHT_STOP],
            links=[JR, STOPOVER, EX],
            rows=[row("fee", "通しの乗車券：京都→広島6,600円、新大阪→広島5,720円（3日間有効・岡山で途中下車できます）", "Through fare ticket: Kyoto–Hiroshima ¥6,600, Shin-Osaka–Hiroshima ¥5,720 (valid three days; stopover allowed)"),
                  row("fee", "特急券（自由席）：京都→岡山3,400円、新大阪→岡山2,530円、岡山→広島2,530円", "Express tickets (unreserved): Kyoto–Okayama ¥3,400, Shin-Osaka–Okayama ¥2,530, Okayama–Hiroshima ¥2,530")],
            time=(DEP, "9:25発（京都駅に9:10ごろ）", "the 9:25 train (be at Kyoto Station by about 9:10)")),
        okayamaeki=dict(
            caution=T("預かりは20:00まで・160cmまで。大きいロッカーは8つだけ", "Bag storage until 20:00, up to 160 cm. Only eight large lockers"),
            notices=[N_BAGS_STOP, N_TICKET],
            time=(VIS, "10:25〜10:40", "10:25–10:40")),
        tram=dict(
            pre=T("10:44発で城下に10:52着。帰りは城下14:25発で、岡山駅前に14:32着です。", "The 10:44 reaches Shiroshita at 10:52. Back, the 14:25 reaches the station at 14:32."),
            time=(MOV, "10:44〜10:52", "10:44–10:52")),
        castle=dict(time=(VIS, "11:05〜12:00", "11:05–12:00")),
        tsukimi=dict(time=(VIS, "12:00〜12:15", "12:00–12:15")),
        korakuen=dict(
            pre=T("庭を1時間、13:20からお昼。14:10に出て城下14:25発の電車で駅へ戻り、荷物を取って15:06ののぞみに乗ります。",
                  "An hour in the garden, lunch from 13:20. Leave at 14:10 for the 14:25 tram, collect bags and board the 15:06 Nozomi."),
            time=(VIS, "12:15〜14:10（お昼を含む）", "12:15–14:10 (including lunch)")),
        lunch=dict(
            pre=T("お城と後楽園のかわりに倉敷へ寄る場合です。岡山10:40発の伯備線で倉敷10:58着。帰りに岡山で乗り換えるなら、荷物は岡山駅に預けても取りに寄れます。福山で乗り換えるなら、荷物は倉敷まで持ってきてください。",
                  "This is for Kurashiki instead of the castle and garden. The 10:40 Hakubi line train from Okayama arrives at 10:58. If you will change at Okayama later you can leave bags there; if at Fukuyama, bring them to Kurashiki."),
            rows=[row("train", "岡山10:40 → 倉敷10:58（平日・土・日とも）。330円", "Okayama 10:40 → Kurashiki 10:58 (weekdays and weekends). ¥330")],
            time=(MOV, "10:40〜10:58", "10:40–10:58")),
        ohara=dict(
            pre=T("倉敷に寄る場合の最初の場所です。見たらお昼は本町の三宅商店などで。月曜なら美術館は飛ばして、川舟かアイビースクエアに。",
                  "The first stop if you choose Kurashiki. Have lunch afterwards on Honmachi, at Miyake Shoten for example. On a Monday skip the museum for the boat or Ivy Square."),
            notices=[N_OHARA_DATES],
            time=(VIS, "11:15〜12:30", "11:15–12:30")),
        bikan=dict(
            pre=T("お昼（12:35〜13:25）のあとに川ぞいを歩きます。", "Walk the canal after lunch (12:35–13:25)."),
            time=(VIS, "13:25〜13:50", "13:25–13:50")),
        boat=dict(
            pre=T("立ち寄りで乗るなら、阿智神社のかわりに14:00の便をWEB予約で。着いてからの当日券はあてにしないほうが安全です。",
                  "On a stopover, book the 14:00 boat online instead of Achi Shrine. Don’t count on same-day tickets after you arrive."),
            time=(VIS, "14:00〜14:20", "14:00–14:20")),
        ivy=dict(time=(VIS, "14:00〜14:20（阿智神社のかわりに）", "14:00–14:20 (instead of Achi Shrine)")),
        achi=dict(time=(VIS, "14:00〜14:20", "14:00–14:20")),
        honmachi=dict(
            pre=T("お昼を食べる通りです。三宅商店は平日11:30開店。食べ終わったら川ぞいへ。14:25ごろ美観地区を出て、駅へ向かいます。",
                  "The street for lunch; Miyake Shoten opens at 11:30 on weekdays. Then the canal. Leave the old quarter at about 14:25 for the station."),
            time=(VIS, "12:35〜13:25（お昼）", "12:35–13:25 (lunch)")),
        kaeri=dict(
            name=T("広島へ（岡山駅）", "On to Hiroshima (Okayama Station)"),
            blurb=T("岡山15:06発で広島15:42着。倉敷からは15:13発か15:06発で16:27着。", "Okayama 15:06 → Hiroshima 15:42. From Kurashiki, the 15:13 or 15:06 arrives 16:27."),
            pre=T("・岡山城と後楽園に寄った日：のぞみ15:06発 → 広島15:42着（自由席5,610円）。\n\n"
                  "・倉敷に寄った日：広島に着くのはどちらも16:27です。\n"
                  "　倉敷15:13発、岡山でのぞみに乗り換え：5,940円。岡山駅に荷物がある人はこちら。\n"
                  "　倉敷15:06発、福山で同じのぞみに乗り換え：5,170円。荷物を持っている人はこちらが安い。\n"
                  "　京都→倉敷を7,470円で買うと、京都からの合計は12,640円（福山乗り換え）か13,410円（岡山乗り換え）。\n\n"
                  "新倉敷でこだまに乗る方法もあります。速いかどうかは時間によって変わり、倉敷18:46発なら新倉敷・福山で乗り換えて19:46着の60分、18:18発の岡山回りは19:23着の65分でした。\n\n"
                  "最終は岡山23:14発（広島23:54着）、倉敷22:42発（岡山乗り換え、広島23:54着）です。",
                  "• After the castle and garden: the 15:06 Nozomi arrives in Hiroshima at 15:42 (¥5,610 unreserved).\n\n"
                  "• After Kurashiki, both options arrive at 16:27.\n"
                  "The 15:13 from Kurashiki, changing to a Nozomi at Okayama: ¥5,940, for anyone with bags at Okayama.\n"
                  "The 15:06, changing to the same Nozomi at Fukuyama: ¥5,170, cheaper if you have your bags with you.\n"
                  "With a ¥7,470 Kyoto–Kurashiki ticket, the total from Kyoto is ¥12,640 via Fukuyama or ¥13,410 via Okayama.\n\n"
                  "A Kodama from Shin-Kurashiki is another way. Which is faster depends on the hour: the 18:46 from Kurashiki via Shin-Kurashiki and Fukuyama took 60 minutes (19:46), the 18:18 via Okayama 65 (19:23).\n\n"
                  "Last trains: Okayama 23:14 (Hiroshima 23:54); Kurashiki 22:42 via Okayama (23:54)."),
            links=[JR, STOPOVER, link("official", "吾妻寿司 公式サイト", "Azumazushi (official, Japanese)", U["azuma"])],
            rows=[row("train", "岡山15:06 → 広島15:42（平日・土・日とも）。指定席は6,460円（11月25日）、6,660円（28日）", "Okayama 15:06 → Hiroshima 15:42 (weekdays and weekends). Reserved ¥6,460 (25 Nov), ¥6,660 (28 Nov)"),
                  row("train", "倉敷15:13（岡山乗換）・15:06（福山乗換）→ 広島16:27（平日・土・日とも）", "Kurashiki 15:13 via Okayama or 15:06 via Fukuyama → Hiroshima 16:27 (weekdays and weekends)")],
            time=(DEP, "15:06発（広島に15:42着）", "the 15:06 (Hiroshima 15:42)")),
    ))


def spot(C, no, sid):
    b, o = S[sid], C["spots"][sid]
    name = o.get("name", b["name"])
    kind = o.get("kind", b["kind"])
    if C["course"] == "stay":
        d = 2 if C["order"].index(sid) >= C["order"].index(C["day2"]) else 1
        kind = T(f"{d}日目・{kind['ja']}", f"Day {d} · {kind['en']}")
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
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"] + o.get("gmaps_add", []),
               links=o.get("links", b.get("links", [JR])) + o.get("links_add", []), notices=o.get("notices", []),
               info={"rows": o.get("rows", []) + b["rows"], "cash": False, "tip": b["tip"],
                     "checked": TODAY if sid in ("ivy", "ohara") else CHECKED},  # 2026-11-23 に表の中身を全部確かめ直した場所
               photos=PHOTOS[sid])
    assert out["photos"], sid
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


for C in (STAY, STOP):
    N = {k: i for i, k in enumerate(C["order"], 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
    OKA = ns("castle", "tsukimi", "korakuen")
    KURA = ns("ivy", "achi", "bikan", "honmachi", "ohara", "boat")
    auto = {str(N["kyoto"]): {"always": True}, str(N["okayamaeki"]): {"always": True}, str(N["tram"]): {"any": OKA},
            str(N["lunch"]): {"any": KURA}, str(N["kaeri"]): {"always": True}}
    if C is STAY:
        picks = sorted(OKA + KURA + ns("kibitsu"))
        default = [n for n in picks if n != N["boat"]]
        split = N[C["day2"]]
        sections = [{"first": 1, "last": N["korakuen"], "area": T("1日目・岡山", "Day 1 · Okayama"), "title": T("1日目 午前〜午後：お城と後楽園", "Day 1: the castle and Korakuen")},
                    {"first": N["lunch"], "last": split - 1, "area": T("1日目・倉敷", "Day 1 · Kurashiki"), "title": T("1日目 夕方〜夜：倉敷に泊まる", "Day 1, evening: a night in Kurashiki")},
                    {"first": split, "last": N["boat"], "area": T("2日目・倉敷", "Day 2 · Kurashiki"), "title": T("2日目 朝：静かな町と美術館", "Day 2, morning: quiet streets and the museum")},
                    {"first": N["kibitsu"], "last": N["kaeri"], "area": T("2日目・岡山", "Day 2 · Okayama"), "title": T("2日目 午後：吉備津神社、京都・大阪か広島へ", "Day 2, afternoon: Kibitsu, then home or Hiroshima")}]
        focus = {"first": 2, "last": N["kaeri"]}
        hints = [
            h("boat", {"any": ns("boat")},
              "川舟に乗る日は、11:20に舟を降りてからお昼へ。WEB予約は乗る日の30日前からです。",
              "With the boat you land at 11:20, then have lunch. Online booking opens 30 days ahead."),
            h("castle", {"any": ns("castle"), "andAny": ns("korakuen")},
              "岡山城と後楽園の両方に入るなら、共通券（800円）を。",
              "Going into both castle and garden? Buy the ¥800 combined ticket."),
            h("kaeri", {"any": KURA, "none": ns("kibitsu")},
              "吉備津神社に寄らない日は、倉敷で午後もゆっくりできます。倉敷17:44発で岡山乗り換え、京都に19:19着です。",
              "Skipping Kibitsu? Spend the afternoon in Kurashiki: the 17:44, changing at Okayama, reaches Kyoto at 19:19."),
        ]
        note = "「1泊2日」。1日目：岡山城・後楽園→夕暮れと夜の倉敷に泊まる。2日目：朝の倉敷・大原美術館→吉備津神社→京都・新大阪か広島。"
    else:
        picks = sorted(OKA + KURA)
        default = OKA
        sections = [{"first": 1, "last": N["korakuen"], "area": T("岡山", "Okayama"), "title": T("最初に選んであるのは、お城と後楽園（約4時間40分）", "Selected to start: castle and garden (about 4 h 40)")},
                    {"first": N["lunch"], "last": N["achi"], "area": T("倉敷", "Kurashiki"), "title": T("かわりに倉敷へ寄るなら（約5時間半）", "Or Kurashiki instead (about 5½ hours)")},
                    {"first": N["kaeri"], "last": N["kaeri"], "area": T("広島へ", "To Hiroshima"), "title": T("広島には15:42（倉敷に寄ると16:27）", "Hiroshima at 15:42 (16:27 via Kurashiki)")}]
        focus = {"first": 2, "last": N["korakuen"]}
        hints = [
            h(sid, {"any": OKA, "andAny": KURA},
              "岡山と倉敷の両方は、立ち寄りの時間には入りません（9時間はかかります）。どちらかを外すか、「1泊2日」のコースに切り替えてください。",
              "Both towns don’t fit in a stopover (at least 9 hours). Drop one, or switch to the overnight course.")
            for sid in ("kyoto", "okayamaeki", "castle", "korakuen", "ohara", "bikan")
        ] + [
            h("korakuen", {"any": ns("korakuen"), "none": ns("castle")},
              "後楽園だけなら約3時間です。城下電停から鶴見橋を渡って正門へ（約10分）。月見橋でお城を眺めて戻ります。",
              "Korakuen alone takes about 3 hours. Cross Tsurumi bridge from Shiroshita to the main gate (about 10 min), see the castle from Tsukimi bridge and return."),
            h("castle", {"any": ns("castle"), "andAny": ns("korakuen")},
              "岡山城と後楽園の両方に入るなら、共通券（800円）を。",
              "Going into both castle and garden? Buy the ¥800 combined ticket."),
            h("boat", {"any": ns("boat"), "andAny": ns("achi", "ivy")},
              "川舟・阿智神社・アイビースクエアは同じ時間帯です。15:06か15:13の電車に乗るなら、1つにしてください。",
              "The boat, Achi Shrine and Ivy Square share one slot. Pick one to catch the 15:06 or 15:13."),
            h("achi", {"any": ns("achi"), "andAny": ns("ivy")},
              "阿智神社とアイビースクエアは同じ時間帯です。どちらか1つに。",
              "Achi Shrine and Ivy Square share one slot. Pick one."),
        ]
        note = "「移動の途中に立ち寄る」。京都・新大阪→岡山→広島。最初は岡山城・月見橋・後楽園だけ。倉敷はかわりに選ぶ。"
    data = {
        "id": "okayama", "course": C["course"],
        "_note": "岡山と倉敷（okayama/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "日帰りの時間割は作らない（2026-11-22 オーナー）。後楽園・吉備津神社・倉敷と改修後の岡山城は Wikimedia Commons の写真（一覧は scripts/okayama_web_photos.json）。"
                 + "info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。このファイルは scripts/build_okayama_data.py で作る（直接直さない）。",
        "sections": sections, "focus": focus,
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。駅と路面電車は自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": default, "auto": auto, "hints": hints},
        "photoBase": "../images/okayama/", "sources": SOURCES,
        "spots": [spot(C, i, k) for i, k in enumerate(C["order"], 1)],
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"]) for s in data["spots"]], "default", default)
