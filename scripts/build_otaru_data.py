#!/usr/bin/env python3
"""小樽（札幌から日帰り）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_otaru_data.py   （そのあと python3 scripts/sync_otaru.py）
- data/routes/otaru.json         … late  ＝9〜10時に札幌を出る。市場→旧手宮線→北運河→運河→銀行街→堺町→夕暮れの運河→天狗山の夜景→晩ごはん（最初に開く）
- data/routes/otaru-early.json   … early ＝7時台に出る。市場の朝ごはん→朝の運河→北一ホールのランプ→開店すぐの堺町→祝津（貴賓館・水族館）→夜の運河
- data/routes/otaru-yoichi.json  … yoichi＝余市のニッカの蒸溜所（予約）→午後の小樽→晩ごはん（天狗山は寄り道）
- 起点は札幌駅〜大通〜すすきののホテル（北海道のマップの決まり、2026-11-26）。だれかが行った・食べたことは書かない（写真は全部 Wikimedia Commons）
- 時間割は冬（12〜3月）を基本に組んだ。夏（日の入り19時ごろ）の天狗山の順番は、スポットの文章と notices に書いてある
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの時間割（pre）→ 共通の説明（body）→ おすすめの時間」の順に組み立てる
- JR の時刻は乗換案内の2026年12月3日（木）・5日（土）のダイヤ。JR北海道のダイヤ改正（春）のあとは確かめ直す
- バスは北海道中央バスの公式時刻表：12月10日までは「2026年4月1日改正」、12月11日からは「2026年12月11日改正（冬ダイヤ）」。
  時間割に使ったバスは、両方のダイヤ・平日と土日祝の全部にある便だけ（天狗山 16:40・18:07・18:40・20:07、祝津 12:00・16:32）
- 写真は images/otaru/<スポットのid>-w<番号>.jpg（Wikimedia Commons。一覧は scripts/otaru_web_photos.json）。
  あとでオーナーの写真を <スポットのid>-<番号>.jpg で入れるときは、PHOTOS の先頭にファイル名を足す
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/otaru"
CHECKED = "2026-11-26"
DEP = ("おすすめ出発時間", "Recommended departure time")
VIS = ("おすすめ訪問時間", "Recommended visit time")
MOV = ("おすすめ移動時間", "Recommended travel time")


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
    """確かめた乗換案内（Yahoo!路線情報）の検索結果のURL。day は '2026-12-03' の形"""
    h, m = hm.split(":")
    y, mon, d = day.split("-")
    p = {"from": f, "to": t, "y": y, "m": mon, "d": d, "hh": h, "m1": m[0], "m2": m[1], "type": {"d": 1, "l": 2, "a": 4}[kind],
         "ticket": "ic", "expkind": 1, "shin": 1, "ex": 1, "lb": 1, "al": 1, "hb": 1, "sr": 0, "s": 0, "userpass": 0, "ws": 3}
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(p)


def cc(x):
    """Wikimedia Commons の写真。"""
    return {"file": x["file"], "credit": {"author": x["author"], "license": x["license"],
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(x["title"].replace(" ", "_"))}}


WEB = json.load(open(f"{R}/scripts/otaru_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]
# オーナーの写真が入ったら、ここで W(...) の前にファイル名を足す（例: "unga": ["unga-1.jpg"] + W("unga")）
PHOTOS = {k: W(k) for k in ("sapporo", "otarueki", "sankaku", "temiya", "kitaunga", "unga", "ginko", "kitaichi", "meruhen",
                            "asakusa", "tengu", "yuhan", "kaeri", "shukutsu", "aq", "yoichi", "nikka")}

D1, D2 = "2026-12-03", "2026-12-05"     # 乗換案内で確かめた日：木曜と土曜
U = dict(
    tengu="https://tenguyama.ckk.chuo-bus.co.jp/hours-and-fees/",
    tengu_en="https://tenguyama.ckk.chuo-bus.co.jp/en/",
    tengu_access="https://tenguyama.ckk.chuo-bus.co.jp/access/",
    tengu_news="https://tenguyama.ckk.chuo-bus.co.jp/news/",
    bus_otaru="https://www.chuo-bus.co.jp/city_route/course/otaru/",
    bus_summer="https://www.chuo-bus.co.jp/city_route/pdf/otaru_E.pdf",
    bus_winter="https://www.chuo-bus.co.jp/city_route/timetable/index.20261211.php",
    bus_dia="https://www.chuo-bus.co.jp/feature/dia-winter2026/",
    bus_ic="https://www.chuo-bus.co.jp/support/sapica/area/",
    aq="https://otaru-aq.jp/guide/openningtime/", aq_fee="https://otaru-aq.jp/guide/tickets/", aq_bus="https://otaru-aq.jp/guide/bus/",
    kihin="https://www.otaru-kihinkan.jp/", kihin_fee="https://www.otaru-kihinkan.jp/aoyama_about/", kihin_en="https://www.otaru-kihinkan.jp/en/",
    nishin="https://www.city.otaru.lg.jp/docs/2020100900596/",
    boj="https://www3.boj.or.jp/otaru-m/", boj_en="https://www3.boj.or.jp/otaru-m/english/",
    art="https://www.nitorihd.co.jp/otaru-art-base/",
    kitaichi="https://kitaichiglass.co.jp/kitaichihall/",
    orgel="https://www.otaru-orgel.co.jp/shop",
    cruise="https://otaru.cc/", cruise_price="https://otaru.cc/price/", cruise_time="https://otaru.cc/timetable/",
    cruise_dec="https://otaru.cc/wp-content/uploads/2026/09/2026_1201_1230.pdf",
    soko="https://otarubeer.com/jp/Ppage_id=357.html",
    naruto="http://otaru-naruto.jp/naruto/shop.html", naruto_menu="http://otaru-naruto.jp/naruto/menu.html",
    sankaku="http://otaru-sankaku.com/eating.html",
    museum="https://www.city.otaru.lg.jp/docs/2023031200049/otarumuseum.html",
    museum_note="https://www.city.otaru.lg.jp/docs/2025032900126/otarumuseum.html",
    nikka="https://www.nikka.com/distilleries/yoichi/visit/", nikka_faq="https://www.nikka.com/distilleries/yoichi/faq/",
    nikka_access="https://www.nikka.com/distilleries/yoichi/access/", nikka_en="https://www.nikka.com/en/distilleries/yoichi/",
    nikka_book="https://reserva.be/nikkayoichi/", nikka_news="https://reserva.be/nikkayoichi/news",
    locker="https://www.jrhokkaido.co.jp/network/locker/locker.pdf",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    kitaca="https://www.jrhokkaido.co.jp/kitaca/02area.html",
    jr_info="https://www3.jrhokkaido.co.jp/webunkou/",
    sun_dec="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html", sun_jan="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0001.html",
    sun_feb="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0002.html", sun_mar="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0003.html",
    sun_jun="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0006.html",
    yuki="https://yukiakarinomichi.org/",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("札幌→小樽 平日", q("札幌", "小樽", D1, "09:15"), "快速エアポート31号 9:33→10:07、普通 9:16→10:01・9:25→10:15、800円（ICカード）"),
    ("札幌→小樽 土曜", q("札幌", "小樽", D2, "09:15"), "平日と同じ（9:33→10:07、9:16→10:01、9:25→10:15）"),
    ("札幌→小樽 朝 平日", q("札幌", "小樽", D1, "06:50"), "6:52→7:38、7:05→7:51、7:14→8:01"),
    ("札幌→小樽 朝 土曜", q("札幌", "小樽", D2, "06:50"), "平日と同じ"),
    ("すすきの→札幌（地下鉄）", q("すすきの", "札幌", D1, "09:10"), "南北線 すすきの→さっぽろ 5分、210円"),
    ("小樽→札幌 夕方 平日", q("小樽", "札幌", D1, "18:50"), "快速エアポート170号 19:00→19:34、174号 19:27→20:01、19:56→20:41"),
    ("小樽→札幌 夕方 土曜", q("小樽", "札幌", D2, "18:50"), "平日と同じ"),
    ("小樽→札幌 夜 平日", q("小樽", "札幌", D1, "19:50"), "20:22→21:11"),
    ("小樽→札幌 夜 土曜", q("小樽", "札幌", D2, "19:50"), "20:22→21:11"),
    ("小樽→札幌 21時台 平日", q("小樽", "札幌", D1, "21:00"), "21:16→22:03、21:37→22:24、21:59→22:44"),
    ("小樽→札幌 21時台 土曜", q("小樽", "札幌", D2, "21:00"), "平日と同じ"),
    ("小樽→札幌 最終 平日", q("小樽", "札幌", D1, "23:30", "l"), "22:31→23:17、最終23:08→23:53"),
    ("小樽→札幌 最終 土曜", q("小樽", "札幌", D2, "23:30", "l"), "22:31→23:17、最終23:08→23:53"),
    ("札幌→余市 平日", q("札幌", "余市", D1, "08:00"), "8:41→小樽（9:36発に乗り換え）→余市10:00、1,380円。次は10:06→余市11:23"),
    ("札幌→余市 土曜", q("札幌", "余市", D2, "08:00"), "平日と同じ"),
    ("余市→小樽 平日", q("余市", "小樽", D1, "13:00"), "12:37→13:01、13:43→14:09、470円。高速バス13:06→14:00（560円）"),
    ("余市→小樽 土曜", q("余市", "小樽", D2, "13:00"), "平日と同じ"),
    ("余市→小樽 午後 平日", q("余市", "小樽", D1, "14:10"), "15:02→15:26。高速バス14:36→15:30・15:06→16:00"),
    ("余市→小樽 午後 土曜", q("余市", "小樽", D2, "14:10"), "平日と同じ"),
    ("小樽→新千歳空港 昼 平日", q("小樽", "新千歳空港", D1, "11:00"), "快速エアポート 11:17→12:39・12:17→13:39、特別快速 11:53→13:08・12:53→14:08、2,040円"),
    ("小樽→新千歳空港 昼 土曜", q("小樽", "新千歳空港", D2, "11:00"), "平日と同じ"),
    ("小樽→新千歳空港 午後 平日", q("小樽", "新千歳空港", D1, "13:00"), "13:17→14:39、特別快速13:53→15:08、14:17→15:39"),
    ("小樽→新千歳空港 午後 土曜", q("小樽", "新千歳空港", D2, "13:00"), "平日と同じ"),
    ("小樽→新千歳空港 夕方", q("小樽", "新千歳空港", D1, "15:00"), "15:33→16:52、16:00→17:15（土曜も同じ）"),
    ("天狗山ロープウエイ 営業時間・料金", U["tengu"], "冬期2026/11/28〜2027/3/28 上り9:00〜19:48・下り〜20:00、夏期2026/4/25〜11/3 上り〜20:48・下り〜21:00。毎時00・12・24・36・48分発。往復 冬2,000円・夏1,800円。カード・電子マネー可。水族館とのセット券3,000円（現金のみ、7日間有効）"),
    ("天狗山 秋季運休", U["tengu_news"], "2026年11月4日〜27日は秋季整備運休、11月28日から冬期営業"),
    ("天狗山 アクセス", U["tengu_access"], "小樽駅前ターミナル乗り場④、天狗山ロープウエイ線（9）約17分、240円。おたる市内線バス1日乗車券800円"),
    ("中央バス 天狗山線（2026年4月1日改正）", U["bus_summer"], "小樽駅前発 平日16:10・16:40・18:40・19:10・19:40、土日祝16:10・16:40・18:40・19:10・19:40。天狗山発 平日18:07・18:37・20:07・20:42・21:17、土日祝18:07・18:47・20:07・20:47・21:17"),
    ("中央バス 冬ダイヤ（2026年12月11日改正）小樽駅前", U["bus_winter"], "天狗山行き 平日16:00・16:40・18:40・19:10・19:40、土日祝16:10・16:40・18:40。祝津線（水族館）毎時00分・おたる水族館線40分。直行10（12/12〜2/23）"),
    ("中央バス 冬ダイヤ 天狗山", U["bus_winter"], "小樽駅前行き 平日・土日祝とも18:07・18:27・18:47・20:07、平日20:42、土日祝20:47、21:17（12/31〜1/3は夜の便が運休）"),
    ("中央バス 冬ダイヤ おたる水族館", U["bus_winter"], "小樽駅前行き 平日・土日祝とも16:32、直行16:10（12/12〜2/23）"),
    ("中央バス 冬ダイヤ改正のお知らせ", U["bus_dia"], "12月11日改正。直行9（天狗山）・直行10（水族館）を増便、祝津線は減便"),
    ("おたる水族館 バス時刻表", U["aq_bus"], "小樽駅前発 祝津線（赤岩経由）毎時00分・おたる水族館線（高島経由）40分。帰り祝津線32分。所要 赤岩経由約25分・高島経由約20分、240円"),
    ("中央バスのICカード", U["bus_ic"], "小樽市内全線・郊外線・余市郊外線でSAPICAと全国相互利用のICカード"),
    ("小樽駅のコインロッカー", U["locker"], "小樽：小400円65個、中500円20個、大700円21個・800円14個"),
    ("JR北海道のレールパス", U["railpass"], "Hokkaido Rail Pass：JR北海道の全線（新幹線を除く）。Sapporo-Noboribetsu Area Pass：新千歳空港・札幌・小樽・登別。どちらもJR北海道バス・札幌の地下鉄と市電は不可"),
    ("三角市場 お食事案内", U["sankaku"], "海鮮食堂かわしま6:00〜16:00、味処たけだ7:00〜16:00、滝波食堂8:00〜17:00、さんかく亭8:00〜17:00（店舗案内のページ）"),
    ("日本銀行旧小樽支店金融資料館", U["boj"], "入館無料、4〜11月9:30〜17:00・12〜3月10:00〜17:00（最終入館16:30）、水曜休館（祝休日は開館）、12/29〜1/5休館、スマートフォンの音声ガイド"),
    ("小樽芸術村", U["art"], "11〜4月10:00〜17:00（最終入館16:30）毎週水曜休館、5〜10月9:30〜17:00 第4水曜休館"),
    ("北一ホール", U["kitaichi"], "9:00〜17:30、注文9:30〜17:00、ランプ点灯作業の見学9:00〜9:30、食事は木・土・日曜11:00〜14:50"),
    ("小樽オルゴール堂 本館", U["orgel"], "9:00〜18:00（2・3階は17:45まで）、定休日なし"),
    ("小樽運河クルーズ 料金", U["cruise_price"], "デイ1,800円、ナイト2,000円（大人）、約40分"),
    ("小樽運河クルーズ 12月の時刻", U["cruise_dec"], "中央橋発着。デイ10:00〜15:30、ナイト16:00〜18:00の30分ごと。12/31・1/1は定休日。冬は船にシートヒーターと幌"),
    ("小樽倉庫No.1", U["soko"], "11:00〜22:00（料理LO21:00・飲み物LO21:30）、不定休。木・土曜は2時間2,600円のビール飲み放題（予約不要）。醸造設備のセルフ見学無料。TEL 0134-21-2323"),
    ("若鶏時代なると 本店", U["naruto"], "11:00〜21:00（LO20:30）、定休日1月1日、小樽駅から徒歩7〜8分。お品書き：若鶏半身揚げ1,190円"),
    ("小樽貴賓館（旧青山別邸）", U["kihin"], "旧青山別邸 4〜10月9:00〜17:00・11〜3月9:00〜16:00（最終受付30分前）、12/29〜31は15:00まで、1/1〜1/7休業。レストランのお食事11:00〜14:30、12/26〜1/7休業。バスは「貴賓館入口」下車徒歩5分"),
    ("旧青山別邸 入館料", U["kihin_fee"], "大人1,300円、カード・電子決済不可、見学20〜30分、館内ガイド休止中"),
    ("小樽市鰊御殿", U["nishin"], "令和8年度 4/4〜11/23、9:00〜17:00（10/16から16:00）、一般300円"),
    ("おたる水族館 営業期間・時間", U["aq"], "通常営業2026/3/14〜11/23、冬期営業2026/12/12〜2027/2/23 10:00〜16:00（最終入館15:30）。休館11/24〜12/11。冬期は海獣公園・遊園地閉鎖"),
    ("おたる水族館 料金（冬期）", U["aq_fee"], "大人（高校生以上）1,300円"),
    ("小樽市総合博物館", U["museum"], "9:30〜17:00（最終入館16:30）、本館は火曜（祝日は翌平日）と12/29〜1/3休館、本館一般400円（冬期300円）"),
    ("小樽市総合博物館 お知らせ", U["museum_note"], "本館は2026/11/5〜2027/4/28が冬期料金。手宮口は冬期閉鎖"),
    ("ニッカ 余市蒸溜所 楽しみ方", U["nikka"], "ガイドツアー無料・予約制。予約なしはミュージアム・ショップ・レストラン（最終入場15:30）。RITA'S KITCHEN 10:00〜15:50（LO15:20）。休業 12/23〜1/7・6/11。全施設16:15まで"),
    ("ニッカ 余市蒸溜所 よくある質問", U["nikka_faq"], "1〜9名、20歳未満だけの参加不可、ツアーは日本語のみ、予約は4週間先まで、食品の持ち込み不可、ロッカー100円（返却式・ツアー予約者のみ）"),
    ("ニッカ 余市蒸溜所 アクセス", U["nikka_access"], "余市駅から徒歩約5分。小樽駅から余市駅まで約30分、列車の本数は多くない"),
    ("ニッカ 予約サイト 12月以降のお知らせ", U["nikka_news"], "2026年12月・2027年1月は設備改修のため無料ガイドツアーなし、キーモルトセミナーのみ（9:30・10:00・10:30・11:30・12:00・12:30・13:30・14:00）。20歳以上・運転しない人。新規予約はWEBのみ、4週間前0:00から。12/5はレストラン休業"),
    ("ニッカ 予約サイト 11月のお知らせ", U["nikka_news"], "ガイドツアー所要60分（9:30〜14:30の9回）、キーモルトセミナー所要90分・3,000円・現地で現金のみ"),
    ("ニッカ 予約サイト 年末年始", U["nikka_news"], "12/23〜1/7休業。1/8・1/9午前はガイドツアーなし"),
    ("日の入り（札幌）12月", U["sun_dec"], "12/1 16:01、12/10 16:00、12/20 16:02、12/31 16:09"),
    ("日の入り（札幌）1月", U["sun_jan"], "1/1 16:10、1/20 16:31、1/31 16:45"),
    ("日の入り（札幌）2月", U["sun_feb"], "2/1 16:46、2/28 17:22"),
    ("日の入り（札幌）3月", U["sun_mar"], "3/1 17:23、3/31 17:59"),
    ("日の入り（札幌）6月", U["sun_jun"], "6/1 19:07、6/28 19:18"),
    ("小樽雪あかりの路", U["yuki"], "2026-11-26 に公式サイトへ接続できず、2027年の日程は確認できなかった（ページには「例年2月」とだけ書く）"),
]]

JR = link("timetable", "JR北海道 運行情報", "JR Hokkaido service status", U["jr_info"])
TENGU = link("official", "小樽天狗山ロープウエイ（営業時間・料金）", "Mt. Tengu Ropeway (official)", U["tengu"], U["tengu_en"])
BUS9 = link("timetable", "中央バスの時刻表（小樽駅前など）", "Chuo Bus timetables (Japanese)", U["bus_winter"])
CRUISE = link("official", "小樽運河クルーズ（時刻・チケット）", "Otaru Canal Cruise (official)", U["cruise"], "https://otaru.cc/en/")

# ---------------------------------------------------------------------------
# 何か所かに出すお知らせ
# ---------------------------------------------------------------------------
N_TENGU_CLOSED = notice(
    "天狗山ロープウエイは11月27日まで運休", "Mt. Tengu Ropeway is closed until 27 November",
    "秋の整備で11月4日〜27日は運休です（山頂のカフェと観光道路も）。11月28日から冬の営業（9:00〜20:00）。運休の日は、夕方からナイトクルーズか夜の運河にしてください。",
    "It is closed for maintenance from 4 to 27 November, with the summit café and road. Winter service (9:00–20:00) starts on 28 November. Until then, take the night canal cruise or walk the canal after dark instead.",
    U["tengu_news"], to="2026-11-27")
N_TENGU_SPRING = notice(
    "春は天狗山ロープウエイが止まる時期があります", "The ropeway closes for a while in spring",
    "冬の営業は3月28日まで。夏の営業がいつ始まるかは公式サイトで確かめてください（2026年は4月25日から）。止まっている日は、夕方からナイトクルーズか夜の運河にしてください。",
    "Winter service ends on 28 March. Check the official site for the start of summer service (it was 25 April in 2026). While it is closed, take the night canal cruise or walk the canal after dark instead.",
    U["tengu"], start="2027-03-20", to="2027-05-06")
N_BUS_WINTER = notice(
    "12月11日から小樽のバスは冬ダイヤ", "Otaru buses switch to the winter timetable on 11 December",
    "このマップの時間割で使うバス（天狗山16:40・18:07、祝津12:00・16:32など）は、冬ダイヤでも同じ時刻です。ほかの便は時刻が変わるものがあります。",
    "The buses used in this timetable (16:40 and 18:07 for Mt. Tengu, 12:00 and 16:32 for Shukutsu) keep the same times. Some other runs change.",
    U["bus_dia"], to="2026-12-10")
N_YEAREND = notice(
    "年末年始は休む場所があります", "Some places close over New Year",
    "日本銀行旧小樽支店金融資料館は12月29日〜1月5日、小樽貴賓館は1月1日〜7日（12月29〜31日は15:00まで）、ニッカの蒸溜所は12月23日〜1月7日、運河クルーズは12月31日・1月1日が休みです。12月31日〜1月3日は天狗山の夜のバスが運休になる便があり、ロープウエイも早く終わります（12/31・1/2・1/3は17:00、1/1は16:00まで）。",
    "The Bank of Japan museum closes 29 December–5 January, Kihinkan 1–7 January (until 15:00 on 29–31 December), the Nikka distillery 23 December–7 January, and the canal cruise on 31 December and 1 January. From 31 December to 3 January some evening buses to Mt. Tengu don’t run and the ropeway closes early (17:00 on 31 Dec, 2 and 3 Jan; 16:00 on 1 Jan).",
    U["tengu"], start="2026-12-15", to="2027-01-07")
N_WINTER_WALK = notice(
    "冬の小樽を歩くとき", "Walking in Otaru in winter",
    "歩道は踏み固められた雪や氷になります。底に溝の深い、滑りにくい靴で。坂の多い町なので、駅から運河へ下る中央通りも気をつけて。12月は16時ごろに日が沈み、雪の日は電車が遅れることがあります。",
    "Pavements turn to packed snow and ice. Wear boots with deep-tread soles. The town is hilly, so take care on the slope from the station down to the canal. In December the sun sets around 16:00, and trains can run late on snowy days.",
    start="2026-11-26", to="2027-03-31")
N_AQ_CLOSED = notice(
    "おたる水族館は12月11日まで休館", "Otaru Aquarium is closed until 11 December",
    "11月24日〜12月11日は休館で、12月12日から冬期営業（10:00〜16:00）です。それまでは、祝津では小樽貴賓館だけ開いています。",
    "It is closed from 24 November to 11 December and reopens for winter (10:00–16:00) on 12 December. Until then only Kihinkan is open in Shukutsu.",
    U["aq"], to="2026-12-11")
N_AQ_SPRING = notice(
    "おたる水族館は2月24日から休館", "Otaru Aquarium closes from 24 February",
    "冬期営業は2月23日まで。春の通常営業がいつ始まるかは公式サイトで（2026年は3月14日から）。",
    "Winter opening ends on 23 February. Check the official site for the spring reopening (14 March in 2026).",
    U["aq"], start="2027-02-15", to="2027-03-31")
N_NIKKA_WINTER = notice(
    "12月・1月は無料のガイドツアーがありません", "No free tours in December and January",
    "試飲の建物の改修のため、2026年12月〜2027年1月は有料の「余市蒸溜所限定キーモルトセミナー」だけです（9:30・10:00・10:30・11:30・12:00・12:30・13:30・14:00）。20歳以上で、その日に車を運転しない人だけ参加できます。料金は予約ページで確かめてください（11月の案内では90分・3,000円・現地で現金払い）。予約なしでも、ミュージアム・ショップ・レストランには入れます。",
    "Because the tasting hall is being renovated, only the paid Key Malt Seminar runs from December 2026 to January 2027 (9:30, 10:00, 10:30, 11:30, 12:00, 12:30, 13:30, 14:00). You must be 20 or over and not driving that day. Check the fee on the booking page (in November it was 90 minutes, ¥3,000, cash only on the day). Without a booking you can still visit the museum, shop and restaurant.",
    U["nikka_news"], to="2027-01-31")
N_NIKKA_CLOSED = notice(
    "12月23日〜1月7日は蒸溜所が休み", "The distillery is closed 23 December–7 January",
    "ショップ・レストラン・ミュージアムも休みです。1月8日と9日の午前はツアーがありません。休みの日は「9〜10時に出る」コースへ。",
    "The shop, restaurant and museum close too, and there are no tours on 8 January or the morning of 9 January. On those days, use the 9–10 o’clock course instead.",
    U["nikka_news"], start="2026-12-10", to="2027-01-09")

# ---------------------------------------------------------------------------
# スポットの共通部分
# ---------------------------------------------------------------------------
S = dict(
    sapporo=dict(
        name=T("札幌駅（JR）", "Sapporo Station (JR)"), kind=T("駅", "Station"),
        blurb=T("快速エアポートで小樽まで34分、800円。Kitaca・Suicaなどの交通系ICカードが使えます。",
                "The Rapid Airport train reaches Otaru in 34 minutes for ¥800. Kitaca, Suica and other IC cards work."),
        lat=43.06866, lng=141.35079,
        body=T("大通・すすきののホテルからは、地下鉄南北線で「さっぽろ」駅へ（すすきのから5分・210円）。大通からは、地下の歩行空間（チ・カ・ホ）を歩いても行けます。\n\n"
               "小樽へは「快速エアポート」（新千歳空港から来て小樽まで行く電車）がいちばん速く、34分。小樽行きの普通でも45〜50分で、運賃は同じ800円です。銭函（ぜにばこ）を過ぎると線路が海ぎわを走ります。海は進行方向の右側です。\n\n"
               "外国のパスポートで使えるJR北海道レールパス（全線）と札幌・登別エリアパス（新千歳空港・札幌・小樽を含む）で乗れます。小樽の路線バスとロープウエイは別に払います。\n\n"
               "雪の日は遅れや運休が出ることがあります。出る前にJR北海道の運行情報を見てください。",
               "From hotels around Odori or Susukino, take the Namboku subway line to Sapporo (5 minutes from Susukino, ¥210). From Odori you can also walk through the underground passage (Chi-Ka-Ho).\n\n"
               "The fastest train is the Rapid Airport, which runs through from New Chitose Airport to Otaru: 34 minutes. Local trains to Otaru take 45–50 minutes for the same ¥800. After Zenibako the line runs right along the sea, on the right-hand side.\n\n"
               "The JR Hokkaido Rail Pass and the Sapporo-Noboribetsu Area Pass (which includes New Chitose Airport, Sapporo and Otaru) cover this train. Otaru’s buses and the ropeway are paid separately.\n\n"
               "Snow can delay or cancel trains. Check JR Hokkaido’s service status before you leave."),
        gmaps=[gm("JR札幌駅", "JR Sapporo Station", 43.06866, 141.35079, "JR札幌駅")],
        links=[JR, link("info", "JR北海道のレールパス（英語）", "JR Hokkaido rail passes", U["railpass"])],
        rows=[row("fee", "札幌→小樽 800円（ICカード）", "Sapporo → Otaru ¥800 (IC card)")],
        tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました。春のダイヤ改正のあとは確かめ直してください。パスはJR北海道の英語のページで確認しました。",
              "Times and fares from a route planner for Thursday 3 and Saturday 5 December 2026; check again after the spring timetable change. Pass details from JR Hokkaido’s English site.")),

    otarueki=dict(
        name=T("小樽（おたる）駅", "Otaru Station"), kind=T("駅・荷物・バス", "Station, lockers, buses"),
        blurb=T("駅舎の中にランプが下がる駅。駅前の中央通りをまっすぐ下ると、10分ほどで運河です。",
                "An old station with oil lamps inside. Walk straight down Chuo-dori from the front and you reach the canal in about 10 minutes."),
        lat=43.19770, lng=140.99440,
        body=T("・荷物：駅のコインロッカーは小400円（65個）、中500円（20個）、大700円（21個）・800円（14個）。札幌に戻らずに空港へ行く日はここに。\n\n"
               "・バス：駅前の「中央バス小樽駅前ターミナル」から。天狗山は4番のりば。運賃は1回240円で、交通系ICカードが使えます（乗るときと降りるときにタッチ）。1日に3回以上乗るなら、ターミナルの窓口で「おたる市内線バス1日乗車券」（800円）を。\n\n"
               "・新千歳空港へ：快速エアポートは小樽発の新千歳空港行きで、乗り換えなし（2,040円）。昼は毎時17分発（1時間22分）と、53分発の特別快速（1時間15分）。17:30の飛行機なら14:17発（空港15:39着）か13:53発（15:08着）。午前だけ小樽を歩く日は、12:17発（13:39着）か12:53発（14:08着）です。",
               "• Bags: lockers in the station cost ¥400 small (65), ¥500 medium (20), ¥700 large (21) or ¥800 (14). Use them if you go straight on to the airport.\n\n"
               "• Buses leave from the Chuo Bus terminal in front of the station; Mt. Tengu is stop 4. Each ride is ¥240 and IC cards work (touch on when you board and again when you get off). If you will ride three times or more, buy the ¥800 Otaru city bus day pass at the terminal counter.\n\n"
               "• To New Chitose Airport: the Rapid Airport starts here and runs straight to the airport (¥2,040). In the daytime it leaves at 17 past each hour (1 h 22), plus a Special Rapid at 53 past (1 h 15). For a 17:30 flight, take the 14:17 (airport 15:39) or the 13:53 (15:08). For a morning in Otaru, the 12:17 (13:39) or 12:53 (14:08)."),
        gmaps=[gm("JR小樽駅", "JR Otaru Station", 43.19770, 140.99440, "JR小樽駅"),
               gm("中央バス小樽駅前ターミナル", "Chuo Bus Otaru Station terminal", 43.19725, 140.99419, "中央バス 小樽駅前ターミナル")],
        links=[link("info", "JR北海道 コインロッカー設置駅一覧（PDF）", "JR Hokkaido lockers by station (PDF, Japanese)", U["locker"]),
               link("timetable", "中央バス 小樽の路線と時刻表", "Chuo Bus routes in Otaru (Japanese)", U["bus_otaru"])],
        rows=[row("train", "小樽→新千歳空港：快速エアポート 11:17・12:17・13:17・14:17・15:33・16:00発、特別快速 11:53・12:53・13:53発（平日・土曜とも）",
                  "Otaru → New Chitose Airport: Rapid Airport at 11:17, 12:17, 13:17, 14:17, 15:33, 16:00; Special Rapid at 11:53, 12:53, 13:53 (weekdays and Saturdays)"),
              row("fee", "市内のバス1回240円、1日乗車券800円。空港まで2,040円", "City bus ¥240 a ride, day pass ¥800. Airport ¥2,040")],
        tip=T("ロッカーはJR北海道の一覧、バスは中央バスと天狗山ロープウエイの公式サイト、空港までの時刻は乗換案内（2026年12月3日・5日）で確認しました。",
              "Lockers from JR Hokkaido’s list, buses from Chuo Bus and the ropeway’s site, airport trains from a route planner (3 and 5 December 2026).")),

    sankaku=dict(
        name=T("小樽三角市場（さんかくいちば）", "Sankaku Market"), kind=T("市場・食堂", "Market & seafood diners"),
        blurb=T("駅のすぐ横の小さな市場。中の食堂で海鮮丼。12時前後を外すと入りやすい。",
                "A small market right beside the station, with diners serving seafood bowls. Easier outside the noon rush."),
        lat=43.19854, lng=140.99387,
        body=T("土地と屋根が三角の形をしていることから付いた名前で、坂になった細い通路に鮮魚店と食堂が並びます。\n\n"
               "食堂は朝から開いています。市場の公式サイトの店舗案内では、海鮮食堂かわしま 6:00〜16:00、味処たけだ 7:00〜16:00、滝波食堂 8:00〜17:00、さんかく亭 8:00〜17:00。休みの日と支払い方法は、サイトに書かれていません（要確認）。\n\n"
               "店の前のメニューの写真と値段を見てから選べます。カニやウニは「時価」の店もあるので、注文の前に値段を確かめて。",
               "The name comes from the triangular plot and roof. Fish shops and small diners line a narrow, sloping aisle.\n\n"
               "The diners open early. The market’s website lists Kaisen Shokudo Kawashima 6:00–16:00, Ajidokoro Takeda 7:00–16:00, Takinami Shokudo 8:00–17:00 and Sankaku-tei 8:00–17:00. Closing days and payment methods are not listed (please check).\n\n"
               "Most shops show photos and prices outside. Crab or sea urchin may be “market price”, so ask the price before you order."),
        gmaps=[gm("小樽三角市場", "Sankaku Market", 43.19854, 140.99387, "小樽三角市場")],
        links=[link("official", "小樽三角市場（お食事案内）", "Sankaku Market (Japanese)", U["sankaku"])],
        rows=[row("hours", "店ごとに違います（かわしま6:00〜16:00、たけだ7:00〜16:00、滝波食堂8:00〜17:00、さんかく亭8:00〜17:00）",
                  "Varies by shop (Kawashima 6:00–16:00, Takeda 7:00–16:00, Takinami 8:00–17:00, Sankaku-tei 8:00–17:00)"),
              row("closed", "店ごとに違います（要確認）", "Varies by shop (please check)")],
        tip=T("時間は市場の公式サイトの店舗案内です。サイトの更新が少ないので、変わっていることがあります。",
              "Hours from the market’s own website, which is rarely updated, so they may have changed.")),

    temiya=dict(
        name=T("旧国鉄手宮線（てみやせん）跡", "The old Temiya railway line"), kind=T("線路の跡・散策路", "Old railway, now a walkway"),
        blurb=T("使われなくなった線路が、街なかにそのまま残る散策路。レールの上を歩けます。",
                "Disused tracks left in place through the middle of town. You can walk right along the rails."),
        lat=43.19885, lng=140.99830,
        body=T("駅から中央通りを運河へ下る途中で、線路が道を横切っています。そこから北（手宮の方）へ、レールの横の小道を歩けます。夏は草の間のレール、冬は雪に埋もれた枕木と、季節で見え方が違います。\n\n"
               "線路を北へたどった先の小樽市総合博物館（本館）は、鉄道の展示が中心の博物館です（9:30〜17:00、火曜休み、冬は300円）。冬は手宮口が閉まり、外の展示も一部見られません。\n\n"
               "冬はレールの上が凍ります。線路の上ではなく横の道を歩いてください。",
               "Walking down Chuo-dori from the station towards the canal, you cross the old line. From there a path follows the rails north towards Temiya: rails in the grass in summer, sleepers under snow in winter.\n\n"
               "At the north end, the Otaru Museum (main building) is mostly about the railway (9:30–17:00, closed Tuesdays, ¥300 in winter). In winter the Temiya entrance and some outdoor exhibits are closed.\n\n"
               "In winter the rails are icy. Walk on the path beside them, not on the tracks."),
        gmaps=[gm("旧手宮線跡（中央通り）", "Old Temiya line at Chuo-dori", 43.19885, 140.99830, "旧国鉄手宮線 散策路 小樽"),
               gm("小樽市総合博物館 本館", "Otaru Museum (main building)", 43.21136, 141.00144, "小樽市総合博物館 本館")],
        links=[link("official", "小樽市総合博物館（開館時間・入館料）", "Otaru Museum (Japanese)", U["museum"])],
        rows=[row("hours", "散策路は自由に歩けます。博物館本館 9:30〜17:00（最終入館16:30）", "The path is open any time. Museum 9:30–17:00 (last entry 16:30)"),
              row("closed", "博物館本館：火曜（祝日なら翌平日）、12月29日〜1月3日", "Museum: Tuesdays (next weekday after a holiday), 29 Dec–3 Jan"),
              row("fee", "博物館本館 400円（2026年11月5日〜2027年4月28日は冬期料金300円）", "Museum ¥400 (winter rate ¥300, 5 Nov 2026–28 Apr 2027)")],
        tip=T("博物館の時間と料金は小樽市の公式ページで確認しました。", "Museum hours and fees from the City of Otaru’s website.")),

    kitaunga=dict(
        name=T("北運河（きたうんが）", "The North Canal"), kind=T("運河の北の端", "The quiet end of the canal"),
        blurb=T("浅草橋のにぎわいから歩いて15分ほど。古い倉庫と小さな船が並ぶ、静かな運河の北の端。",
                "About 15 minutes’ walk from the crowds at Asakusa Bridge: old warehouses and small boats at the quiet north end."),
        lat=43.20503, lng=140.99970,
        body=T("浅草橋の側は道路を通すために半分が埋め立てられましたが、北運河は昔の幅のまま残っています。北浜橋（きたはまばし）のあたりから運河を見ると、石の倉庫と船だまりが続きます。\n\n"
               "近くの「旧日本郵船株式会社小樽支店」は、2025年4月にリニューアルオープンした石造りの建物で、市の博物館の一つです（中に入るなら時間と料金は市のページで。要確認）。写真の2枚目は、その裏に残る手宮線の線路です。\n\n"
               "ここから運河ぞいの散策路を南へ歩くと、中央橋・浅草橋に出ます。",
               "The southern half of the canal was partly filled in for a road, but the North Canal keeps its old width. From around Kitahama Bridge you see stone warehouses and a small boat basin.\n\n"
               "Nearby, the stone Former NYK Line Otaru Branch reopened in April 2025 as one of the city’s museums (check the city’s site for hours and fees). The second photo shows the Temiya line tracks behind it.\n\n"
               "From here the canal path runs south to Chuo Bridge and Asakusa Bridge."),
        gmaps=[gm("北浜橋（北運河）", "Kitahama Bridge (North Canal)", 43.20503, 140.99970, "北浜橋 小樽"),
               gm("旧日本郵船株式会社小樽支店", "Former NYK Line Otaru Branch", 43.20730, 140.99830, "旧日本郵船株式会社小樽支店")],
        links=[link("info", "小樽市総合博物館からのお知らせ", "Otaru Museum notices (Japanese)", U["museum_note"])],
        rows=[row("hours", "運河ぞいは自由に歩けます", "The canal path is open any time")],
        tip=T("旧日本郵船のリニューアルは小樽市の博物館のページで確認しました。", "The NYK building’s reopening is from the city museum’s page.")),

    unga=dict(
        name=T("小樽運河（中央橋〜浅草橋）", "Otaru Canal (Chuo Bridge to Asakusa Bridge)"), kind=T("運河・クルーズ", "Canal & boat ride"),
        blurb=T("石造りの倉庫が並ぶ運河ぞいの散策路。中央橋から40分の運河クルーズ。",
                "The canal path lined with stone warehouses. Canal cruises leave from Chuo Bridge (40 minutes)."),
        lat=43.20002, lng=141.00154,
        body=T("中央橋から浅草橋までの約300mが、倉庫の並ぶいちばん小樽らしい区間です。散策路は道路より一段低い、水面に近いところにあり、倉庫が水に映ります。\n\n"
               "中央橋のたもとから「小樽運河クルーズ」が出ます。運河から港へ出て戻る約40分。デイクルーズ1,800円、日没後のナイトクルーズ2,000円。12月はデイが10:00〜15:30、ナイトが16:00〜18:00の30分ごと（12月31日・1月1日は休み）。冬は船にシートヒーターと幌（ほろ）が付きます。チケットは公式サイト（英語あり）で出航の1時間前まで買えます。天気や波で止まることがあります。\n\n"
               "暗くなると、ガス灯と倉庫の明かりが水面に映ります。",
               "The 300 m from Chuo Bridge to Asakusa Bridge is the classic stretch of warehouses. The path sits a step below street level, so the buildings reflect in the water.\n\n"
               "The Otaru Canal Cruise leaves from the foot of Chuo Bridge: about 40 minutes out to the harbour and back. Day cruise ¥1,800, night cruise after sunset ¥2,000. In December day cruises run 10:00–15:30 and night cruises 16:00–18:00, every 30 minutes (none on 31 Dec and 1 Jan). In winter the boats have heated seats and a canopy. Buy tickets online (English available) up to an hour before. Weather and waves can cancel sailings.\n\n"
               "After dark the gas lamps and warehouse lights reflect in the water."),
        gmaps=[gm("中央橋（運河クルーズ乗り場）", "Chuo Bridge (cruise pier)", 43.20002, 141.00154, "小樽運河クルーズ 中央橋")],
        links=[CRUISE],
        rows=[row("hours", "散策路は自由。運河クルーズ12月：デイ10:00〜15:30、ナイト16:00〜18:00（30分ごと）",
                  "Path open any time. Cruise in December: day 10:00–15:30, night 16:00–18:00 (every 30 min)"),
              row("fee", "運河クルーズ デイ1,800円、ナイト2,000円（大人・約40分）", "Cruise: day ¥1,800, night ¥2,000 (adult, about 40 min)")],
        tip=T("クルーズの料金と12月の時刻表は小樽運河クルーズの公式サイトで確認しました。ほかの月の時刻は公式サイトの時刻表で。",
              "Cruise fares and the December timetable from the operator’s website. See its timetable for other months.")),

    ginko=dict(
        name=T("日本銀行旧小樽支店金融資料館と色内（いろない）の銀行街", "Former Bank of Japan Otaru Branch and the old bank street"),
        kind=T("建物・無料の資料館", "Historic buildings, free museum"),
        caution=T("水曜休館（祝日は開館）", "Closed Wednesdays (open on holidays)"),
        blurb=T("1912年に建った日本銀行の支店が、無料の資料館に。まわりにも昔の銀行の建物が残ります。",
                "The Bank of Japan’s 1912 Otaru branch is now a free museum, with more old bank buildings around it."),
        lat=43.19665, lng=141.00045,
        body=T("東京駅の設計で知られる辰野金吾（たつのきんご）らが設計した建物です。中では日本銀行の仕事や、小樽が栄えたころの歴史を紹介しています。スマートフォンで聞ける音声ガイドもあります。見学は30〜40分ほど。\n\n"
               "前の色内大通りには、旧三井銀行・旧安田銀行・旧北海道拓殖銀行など、昔の銀行の建物が並びます（写真の5枚目は旧三井銀行小樽支店）。旧北海道拓殖銀行の建物は、ステンドグラスや西洋美術の「小樽芸術村」の一部です（11〜4月は10:00〜17:00・水曜休み、料金は公式サイトで）。",
               "Designed by Tatsuno Kingo, the architect of Tokyo Station, and colleagues. Inside are displays on the Bank of Japan’s work and Otaru’s boom years, with an audio guide you can play on your phone. Allow 30–40 minutes.\n\n"
               "Along Ironai-odori stand more old banks: the former Mitsui, Yasuda and Hokkaido Takushoku branches (photo 5 is the former Mitsui Bank). The Takushoku building is part of the Otaru Art Base museums of stained glass and Western art (Nov–Apr 10:00–17:00, closed Wednesdays; fees on the official site)."),
        gmaps=[gm("日本銀行旧小樽支店金融資料館", "Bank of Japan Otaru Museum", 43.19665, 141.00045, "日本銀行旧小樽支店金融資料館"),
               gm("小樽芸術村", "Otaru Art Base", 43.19740, 141.00151, "小樽芸術村")],
        links=[link("official", "日本銀行旧小樽支店金融資料館", "Bank of Japan Otaru Museum (official)", U["boj"], U["boj_en"]),
               link("official", "小樽芸術村", "Otaru Art Base (Japanese)", U["art"])],
        rows=[row("hours", "4〜11月 9:30〜17:00、12〜3月 10:00〜17:00（最終入館16:30）", "Apr–Nov 9:30–17:00, Dec–Mar 10:00–17:00 (last entry 16:30)"),
              row("closed", "水曜（祝日は開館）、12月29日〜1月5日", "Wednesdays (open on holidays), 29 Dec–5 Jan"),
              row("fee", "無料", "Free")],
        tip=T("日本銀行旧小樽支店金融資料館と小樽芸術村の公式サイトで確認しました。", "Checked on the websites of the museum and Otaru Art Base.")),

    kitaichi=dict(
        name=T("堺町通り（さかいまちどおり）と北一硝子（きたいちがらす）", "Sakaimachi Street and Kitaichi Glass"),
        kind=T("通り・ガラスの店・ランプの喫茶", "Shopping street, glass, lamp-lit café"),
        blurb=T("ガラス・オルゴール・菓子の店が続く通り。北一ホールは石油ランプの明かりだけの喫茶。",
                "A street of glass, music box and sweet shops. Kitaichi Hall is a café lit only by oil lamps."),
        lat=43.19231, lng=141.00732,
        body=T("浅草橋から南へ続く通りに、古い商家や倉庫を使った店が並びます。\n\n"
               "北一硝子三号館の奥の「北一ホール」は、木の梁の倉庫の中を石油ランプだけで照らした喫茶です（9:00〜17:30、注文は9:30〜17:00）。毎朝9:00〜9:30は、ランプに火を入れる作業を見られます。食事のメニューは木・土・日曜だけ（11:00〜14:50）。\n\n"
               "昼から夕方は通りが混みやすくなります。店を見るなら、開店してすぐの時間が落ち着いています。冬は歩道が凍る日があるので、店の出入りの段差にも気をつけて。",
               "South from Asakusa Bridge, the street is lined with shops in old merchant houses and warehouses.\n\n"
               "At the back of Kitaichi Glass Building No. 3, Kitaichi Hall is a café in a timbered warehouse lit only by oil lamps (9:00–17:30, orders 9:30–17:00). Every morning from 9:00 to 9:30 you can watch the lamps being lit. Food is served only on Thursdays, Saturdays and Sundays (11:00–14:50).\n\n"
               "The street gets busy from midday into the afternoon; just after opening is calmer. In winter pavements can be icy, so watch the steps at shop doors."),
        gmaps=[gm("北一硝子三号館（北一ホール）", "Kitaichi Glass No. 3 (Kitaichi Hall)", 43.19231, 141.00732, "北一硝子三号館 北一ホール")],
        links=[link("official", "北一ホール（北一硝子）", "Kitaichi Hall (Japanese)", U["kitaichi"])],
        rows=[row("hours", "北一ホール 9:00〜17:30（注文9:30〜17:00）、ランプの点灯作業 9:00〜9:30", "Kitaichi Hall 9:00–17:30 (orders 9:30–17:00); lamp lighting 9:00–9:30")],
        tip=T("北一ホールの時間は北一硝子の公式サイトで確認しました。臨時に時間が変わる日は、同じページに出ます。",
              "Kitaichi Hall’s hours from Kitaichi Glass’s website, which also posts any one-off changes.")),

    meruhen=dict(
        name=T("メルヘン交差点と小樽オルゴール堂 本館", "Märchen Crossing and the Otaru Music Box Museum"),
        kind=T("交差点・オルゴールの店", "Crossroads & music box shop"),
        blurb=T("堺町通りの南の端。蒸気時計の前の石造りの建物が、3階までオルゴールが並ぶ本館です。",
                "The south end of Sakaimachi. The stone building behind the steam clock is the main hall, full of music boxes on three floors."),
        lat=43.19052, lng=141.00772,
        body=T("交差点の角に立つ蒸気時計と、オルゴール堂の本館が目印です。本館は9:00〜18:00（2・3階は17:45まで）、休みはありません。小さなオルゴールから、アンティークの大きなものまで並びます。\n\n"
               "すぐ近くには、アンティークのオルゴールの展示と演奏をしている2号館もあります。",
               "Look for the steam clock on the corner and the main hall of the Music Box Museum. It opens 9:00–18:00 every day (2nd and 3rd floors until 17:45), with everything from tiny music boxes to large antiques.\n\n"
               "Building No. 2 nearby shows and plays antique music boxes."),
        gmaps=[gm("小樽オルゴール堂 本館", "Otaru Music Box Museum (main hall)", 43.19052, 141.00772, "小樽オルゴール堂 本館")],
        links=[link("official", "小樽オルゴール堂（店舗一覧）", "Otaru Music Box Museum (official)", U["orgel"])],
        rows=[row("hours", "本館 9:00〜18:00（2・3階は17:45まで）。2号館 9:00〜18:00", "Main hall 9:00–18:00 (2F–3F until 17:45). Building No. 2 9:00–18:00"),
              row("closed", "なし", "Open every day")],
        tip=T("オルゴール堂の公式サイトの店舗一覧で確認しました。", "Checked on the Music Box Museum’s shop list.")),

    asakusa=dict(
        name=T("浅草橋（あさくさばし）から見る運河", "The canal from Asakusa Bridge"), kind=T("運河の眺め", "Canal view"),
        blurb=T("倉庫とガス灯が水面に映る、小樽運河のいちばん有名な眺め。空がまだ青いうちに明かりがつく時間が見ごろ。",
                "Otaru’s best-known view: warehouses and gas lamps reflected in the water. Best when the lamps are on and the sky is still blue."),
        lat=43.19784, lng=141.00328,
        body=T("浅草橋の上と、橋のたもとから運河ぞいの散策路に下りたところから、倉庫の並びを見通せます。人が多いのは橋の上なので、散策路に下りて少し北へ歩くと撮りやすくなります。\n\n"
               "日の入り（札幌）：12月は16:00〜16:09、1月16:10〜16:45、2月16:46〜17:22、3月17:23〜17:59、6月は19:07〜19:18。日が沈んでから20〜30分が、空の青と明かりがいっしょに見える時間です。\n\n"
               "朝の7〜8時台は人が少ない時間です。冬は散策路が凍り、橋の上は海からの風が冷たいので、手袋と帽子を。例年2月には「小樽雪あかりの路」が開かれます（2027年の日程は公式サイトで）。",
               "From the bridge, or from the canal path just below it, you look straight down the line of warehouses. The bridge itself is where the crowds stand; walk a little north along the path for an easier shot.\n\n"
               "Sunset (Sapporo): 16:00–16:09 in December, 16:10–16:45 in January, 16:46–17:22 in February, 17:23–17:59 in March, 19:07–19:18 in June. The 20–30 minutes after sunset give you blue sky and lamps together.\n\n"
               "Early morning, around 7–8 o’clock, is quiet. In winter the path is icy and the wind off the sea is cold on the bridge, so bring gloves and a hat. The Otaru Snow Light Path festival is usually held in February (check its website for 2027 dates)."),
        gmaps=[gm("浅草橋（小樽運河）", "Asakusa Bridge (Otaru Canal)", 43.19784, 141.00328, "浅草橋 小樽運河")],
        links=[link("info", "小樽雪あかりの路（公式サイト）", "Otaru Snow Light Path (official)", U["yuki"])],
        rows=[row("hours", "自由に見られます", "Open any time")],
        tip=T("日の入りは国立天文台の札幌の暦です（小樽もほぼ同じ時刻）。", "Sunset times from the National Astronomical Observatory for Sapporo; Otaru is almost the same.")),

    tengu=dict(
        name=T("小樽天狗山（てんぐやま）ロープウエイ", "Mt. Tengu Ropeway"), kind=T("夜景・展望台", "Night view"),
        caution=T("冬の営業は11月28日〜3月28日、9:00〜20:00（上りの最終19:48）", "Winter season 28 Nov–28 Mar, 9:00–20:00 (last ride up 19:48)"),
        blurb=T("小樽駅前からバスで約17分、ロープウエイで山頂へ。港と街の明かりを見下ろします。",
                "About 17 minutes by bus from Otaru Station, then the ropeway to the top for the lights of the town and harbour."),
        lat=43.17794, lng=140.97516,
        body=T("バスは小樽駅前ターミナルの4番のりばから「天狗山ロープウエイ線」（9番）、終点の「天狗山ロープウエイ」まで。240円で、交通系ICカードが使えます。\n\n"
               "ロープウエイは毎時00・12・24・36・48分に出ます（混むと6分おき）。往復は冬2,000円・夏1,800円で、クレジットカードと電子マネーが使えます。冬の山頂はスキー場で、街よりずっと寒く風が強いので、持っているいちばん暖かい服で。公式サイトのトップに、その日の「夜景になる時刻」が出ます。\n\n"
               "季節で時間割を入れ替えます。\n"
               "・冬（11月28日〜3月28日）：このマップの時間割どおり、16:40のバスで上がって、18:07のバスで下ります。晩ごはんはそのあと。\n"
               "・夏（2026年は4月25日〜11月3日）：日の入りが19時ごろなので、晩ごはんを先に。19:10か19:40のバスで上がります（上りの最終20:48、下りの最終21:00）。帰りのバスは平日20:42・土日祝20:47、どの日も21:17。小樽21:16発で札幌22:03着、21:37発で22:24着です。\n\n"
               "春と秋に整備の運休があります（2026年秋は11月4日〜27日）。天気が悪くて止まる日もあります。ロープウエイとおたる水族館のセット券（3,000円・現金のみ・7日間有効）もあります。",
               "Take the Tenguyama Ropeway line (No. 9) from stop 4 at the Otaru Station bus terminal to the last stop. ¥240; IC cards work.\n\n"
               "The ropeway leaves at :00, :12, :24, :36 and :48 past each hour (every 6 minutes when busy). A return ticket is ¥2,000 in winter and ¥1,800 in summer; cards and e-money are accepted. In winter the summit is a ski area and much colder and windier than town, so wear your warmest clothes. The official site’s front page shows the time the night view begins that day.\n\n"
               "Swap the order by season.\n"
               "• Winter (28 Nov–28 Mar): as in this timetable, up on the 16:40 bus and down on the 18:07, then dinner.\n"
               "• Summer (25 Apr–3 Nov in 2026): sunset is around 19:00, so eat first and take the 19:10 or 19:40 bus up (last ride up 20:48, last down 21:00). Buses back: 20:42 on weekdays, 20:47 at weekends and holidays, and 21:17 every day. The 21:16 train from Otaru reaches Sapporo at 22:03, the 21:37 at 22:24.\n\n"
               "It closes for maintenance in spring and autumn (4–27 November in 2026) and can stop in bad weather. A ¥3,000 combined ticket with Otaru Aquarium (cash only, valid 7 days) is also sold."),
        gmaps=[gm("天狗山ロープウエイ 山麓駅", "Mt. Tengu Ropeway base station", 43.17794, 140.97516, "小樽天狗山ロープウエイ")],
        links=[TENGU, BUS9],
        rows=[row("bus", "小樽駅前→天狗山：16:40、18:40、19:10、19:40（平日・土日祝とも、12月11日からの冬ダイヤでも同じ）",
                  "Otaru Station → Mt. Tengu: 16:40, 18:40, 19:10, 19:40 (every day, also on the winter timetable from 11 Dec)"),
              row("bus", "天狗山→小樽駅前：18:07、20:07、21:17（どの日も）。冬ダイヤは18:27・18:47も", "Mt. Tengu → Otaru Station: 18:07, 20:07, 21:17 every day; also 18:27 and 18:47 on the winter timetable"),
              row("hours", "冬 9:00〜20:00（上りの最終19:48）、夏 上りの最終20:48・下りの最終21:00", "Winter 9:00–20:00 (last up 19:48); summer last up 20:48, last down 21:00"),
              row("fee", "往復 冬2,000円・夏1,800円。バスは片道240円", "Return: ¥2,000 winter, ¥1,800 summer. Bus ¥240 each way")],
        tip=T("ロープウエイの時間・料金・運休は公式サイト、バスは中央バスの時刻表（2026年4月1日改正と12月11日改正の両方）で確認しました。",
              "Ropeway times, fares and closures from its website; buses from Chuo Bus timetables (both the April and the 11 December 2026 versions).")),

    yuhan=dict(
        name=T("晩ごはん：小樽倉庫No.1 か 若鶏時代なると本店", "Dinner: Otaru Soko No.1 or Naruto"), kind=T("晩ごはん", "Dinner"),
        blurb=T("運河ぞいの倉庫で小樽のビール、か、駅の近くで名物の若鶏の半身揚げ。",
                "Local beer in a canal-side warehouse, or the famous half fried chicken near the station."),
        lat=43.20030, lng=141.00215,
        body=T("・小樽倉庫No.1（そうこナンバーワン）：小樽ビールの醸造所がある、中央橋のそばの倉庫のビアパブ。11:00〜22:00（料理のラストオーダー21:00、飲み物21:30）、不定休。木・土曜は2時間2,600円のビール飲み放題（予約不要）。店内の仕込み釜や発酵タンクは自由に見学できます。席の予約は電話（0134-21-2323）。\n\n"
               "・若鶏時代なると本店：小樽駅から歩いて7〜8分。若鶏の半身揚げ（1,190円）が名物の店で、270席。11:00〜21:00（ラストオーダー20:30）、休みは1月1日だけ。天狗山からのバスを駅前で降りて、そのまま行けます。\n\n"
               "写真は夜の運河です。",
               "• Otaru Soko No.1: a beer pub with its own brewery in a warehouse by Chuo Bridge. 11:00–22:00 (last food order 21:00, drinks 21:30), closed on irregular days. On Thursdays and Saturdays there is a two-hour all-you-can-drink beer deal for ¥2,600, no booking needed. You can look at the brewing kettle and tanks for free. Table bookings by phone (0134-21-2323).\n\n"
               "• Wakadori Jidai Naruto (main shop): 7–8 minutes’ walk from Otaru Station, known for its half fried young chicken (¥1,190); 270 seats. 11:00–21:00 (last order 20:30), closed only on 1 January. Handy straight off the bus from Mt. Tengu.\n\n"
               "The photos show the canal at night."),
        gmaps=[gm("小樽倉庫No.1", "Otaru Soko No.1", 43.20030, 141.00215, "小樽倉庫No.1"),
               gm("若鶏時代なると 本店", "Wakadori Jidai Naruto (main shop)", 43.20028, 140.99511, "若鶏時代なると 本店")],
        links=[link("official", "小樽ビール 小樽倉庫No.1", "Otaru Beer, Otaru Soko No.1 (Japanese)", U["soko"]),
               link("official", "若鶏時代なると 本店（店舗案内）", "Naruto main shop (Japanese)", U["naruto"])],
        rows=[row("hours", "小樽倉庫No.1 11:00〜22:00（料理LO21:00）、不定休。なると本店 11:00〜21:00（LO20:30）、1月1日休み",
                  "Otaru Soko No.1 11:00–22:00 (last food order 21:00), irregular closing days. Naruto 11:00–21:00 (last order 20:30), closed 1 Jan")],
        tip=T("時間は小樽ビールと若鶏時代なるとの公式サイトで確認しました。支払い方法は公式に書かれていません（要確認）。",
              "Hours from each restaurant’s website. Payment methods are not listed (please check).")),

    kaeri=dict(
        name=T("小樽駅から札幌へ（空港へも）", "Back to Sapporo (or on to the airport)"), kind=T("帰り", "Going back"),
        blurb=T("快速エアポートで札幌まで34分。最終は23:08発。",
                "34 minutes to Sapporo on the Rapid Airport. The last train leaves at 23:08."),
        lat=43.19800, lng=140.99395,
        body=T("札幌行き（平日・土曜とも）：19:00の快速エアポート（札幌19:34着）、19:27の快速エアポート（20:01着）、19:56（20:41着）、20:22（21:11着）、21:16（22:03着）、21:37（22:24着）、21:59（22:44着）、22:31（23:17着）、最終23:08（23:53着）。\n\n"
               "札幌駅から大通・すすきのへは地下鉄南北線で。\n\n"
               "快速エアポートは新千歳空港まで乗り換えなしで行きます（小樽から2,040円）。空港へ行く日の時刻は、小樽駅のスポットにまとめてあります。",
               "To Sapporo (weekdays and Saturdays): Rapid Airport at 19:00 (Sapporo 19:34) and 19:27 (20:01), then 19:56 (20:41), 20:22 (21:11), 21:16 (22:03), 21:37 (22:24), 21:59 (22:44), 22:31 (23:17) and the last at 23:08 (23:53).\n\n"
               "From Sapporo, the Namboku subway line runs to Odori and Susukino.\n\n"
               "The Rapid Airport carries on to New Chitose Airport without a change (¥2,040 from Otaru). Airport times are listed under Otaru Station."),
        gmaps=[gm("JR小樽駅", "JR Otaru Station", 43.19770, 140.99440, "JR小樽駅")],
        links=[JR],
        rows=[row("train", "小樽→札幌 最終23:08（札幌23:53着）", "Last train Otaru → Sapporo 23:08 (arrives 23:53)"),
              row("fee", "小樽→札幌 800円（ICカード）", "Otaru → Sapporo ¥800 (IC card)")],
        tip=T("時刻は乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました。", "Times from a route planner for 3 and 5 December 2026.")),

    shukutsu=dict(
        name=T("祝津（しゅくつ）の高台：小樽貴賓館（旧青山別邸）", "Shukutsu hill: Otaru Kihinkan (former Aoyama villa)"),
        kind=T("屋敷・お昼・眺め", "Villa, lunch, sea view"),
        caution=T("入館は現金のみ。11〜3月は16:00まで（入館は15:30まで）", "Cash only. Nov–Mar until 16:00 (last entry 15:30)"),
        blurb=T("「にしん御殿」とも呼ばれる青山家の別邸。国の登録有形文化財で、敷地の食事処でお昼も。",
                "The Aoyama family’s villa, known as a herring mansion and a registered cultural property, with lunch on site."),
        lat=43.23179, lng=141.00768,
        body=T("にしん漁の村だった祝津の高台にある屋敷で、お金を惜しまずに建てた豪邸として知られます。見学は20〜30分（館内ガイドは休止中）。入館料1,300円で、カードと電子決済は使えません。\n\n"
               "同じ敷地のレストランは、11〜3月は10:00〜16:00、お食事は11:00〜14:30です（12月26日〜1月7日は休み）。\n\n"
               "行き方：貴賓館の案内では、小樽駅前から水族館行きのバスで約20分、「貴賓館入口」で降りて歩いて5分。このマップでは、終点のおたる水族館まで乗って坂を上ります（歩いて15〜20分の目安）。\n\n"
               "近くの小樽市鰊御殿（にしんごてん）は、にしん漁の道具や番屋の暮らしの品を展示する建物で、2026年度は4月4日〜11月23日の開館（9:00〜17:00、10月16日からは16:00まで、300円）。冬は閉まっています。高台からは祝津の港と日和山（ひよりやま）の灯台が見えます（写真）。冬の坂道は凍るので、滑りにくい靴で。",
               "A lavish villa on the hill above Shukutsu, once a herring-fishing village. Allow 20–30 minutes (guided tours are suspended). Admission ¥1,300, cash only (no cards or e-money).\n\n"
               "The restaurant on the grounds opens 10:00–16:00 from November to March, with meals 11:00–14:30 (closed 26 Dec–7 Jan).\n\n"
               "Getting there: Kihinkan says to take an aquarium-bound bus from Otaru Station (about 20 minutes) and walk 5 minutes from the Kihinkan-iriguchi stop. This map rides to the last stop, Otaru Aquarium, and walks up the hill (allow 15–20 minutes).\n\n"
               "Nearby, the Otaru Herring Mansion, with herring-fishing tools and everyday things from the fishing lodges, opens 4 April–23 November in 2026 (9:00–17:00, 16:00 from 16 October, ¥300) and is closed in winter. From the hill you see Shukutsu harbour and the Hiyoriyama lighthouse (photos). The slopes are icy in winter, so wear boots with grip."),
        gmaps=[gm("小樽貴賓館（旧青山別邸）", "Otaru Kihinkan", 43.23179, 141.00768, "小樽貴賓館 旧青山別邸"),
               gm("小樽市鰊御殿", "Otaru Herring Mansion", 43.23750, 141.00950, "小樽市鰊御殿")],
        links=[link("official", "小樽貴賓館", "Otaru Kihinkan (official)", U["kihin"], U["kihin_en"]),
               link("official", "小樽市鰊御殿（小樽市）", "Otaru Herring Mansion (Japanese)", U["nishin"])],
        rows=[row("hours", "旧青山別邸 4〜10月9:00〜17:00、11〜3月9:00〜16:00（入館は30分前まで）。12月29〜31日は15:00まで", "Villa Apr–Oct 9:00–17:00, Nov–Mar 9:00–16:00 (last entry 30 min before); until 15:00 on 29–31 Dec"),
              row("closed", "1月1日〜7日", "1–7 Jan"),
              row("fee", "1,300円（現金のみ）", "¥1,300 (cash only)")],
        tip=T("小樽貴賓館と小樽市の公式サイトで確認しました。坂道の歩く時間は地図からの目安です。",
              "Checked on Kihinkan’s and the city’s websites. The walking time up the hill is an estimate from the map.")),

    aq=dict(
        name=T("おたる水族館", "Otaru Aquarium"), kind=T("水族館", "Aquarium"),
        caution=T("冬期営業は12月12日〜2月23日（10:00〜16:00、入館は15:30まで）", "Winter opening 12 Dec–23 Feb (10:00–16:00, last entry 15:30)"),
        blurb=T("祝津の海ぞいの水族館。冬はペンギンが雪の上を歩く「ペンギンの雪中さんぽ」があります。",
                "An aquarium on the Shukutsu shore. In winter, penguins go for a walk on the snow."),
        lat=43.23701, lng=141.01140,
        body=T("冬期営業（2026年12月12日〜2027年2月23日）は10:00〜16:00（入館は15:30まで）、大人1,300円。この間は、外の「海獣公園」と遊園地は閉まっています。ペンギンの雪中さんぽなどの時間は、公式サイトの「いきもののじかん」で。\n\n"
               "休館：2026年11月24日〜12月11日と、2月24日から春の通常営業まで（2027年の再開日は公式サイトで。2026年は3月14日から）。通常営業は9:00〜17:00（10月16日からは16:00まで）。\n\n"
               "帰りのバスは、どの日も16:32の祝津線（小樽駅前まで約25分）。冬期営業の間は16:10の直行バスもあります。天狗山ロープウエイとのセット券（3,000円・現金のみ）は水族館の窓口でも買えます。",
               "Winter opening (12 Dec 2026–23 Feb 2027) is 10:00–16:00 (last entry 15:30), ¥1,300 for adults. The outdoor sea-mammal park and the amusement rides are closed then. Check the “animal times” page for the penguin walk schedule.\n\n"
               "Closed 24 Nov–11 Dec 2026, and from 24 Feb until the spring season (check the 2027 date; it was 14 March in 2026). In the regular season it opens 9:00–17:00 (16:00 from 16 October).\n\n"
               "The 16:32 Shukutsu line bus runs every day (about 25 minutes to Otaru Station), plus a direct bus at 16:10 during winter opening. The ¥3,000 combined ticket with the Mt. Tengu Ropeway (cash only) is sold here too."),
        gmaps=[gm("おたる水族館", "Otaru Aquarium", 43.23701, 141.01140, "おたる水族館")],
        links=[link("official", "おたる水族館（営業期間・時間）", "Otaru Aquarium (official)", U["aq"], "https://otaru-aq.jp/en/"),
               link("timetable", "おたる水族館 バス時刻表", "Aquarium bus times (Japanese)", U["aq_bus"])],
        rows=[row("hours", "冬期 10:00〜16:00（入館15:30まで）。通常期 9:00〜17:00", "Winter 10:00–16:00 (last entry 15:30). Regular season 9:00–17:00"),
              row("closed", "2026年11月24日〜12月11日、2月24日〜春の通常営業まで", "24 Nov–11 Dec 2026; from 24 Feb until spring opening"),
              row("fee", "冬期 大人1,300円", "Winter ¥1,300 (adult)"),
              row("bus", "水族館→小樽駅前：16:32（どの日も）、直行16:10（12月12日〜2月23日）", "Aquarium → Otaru Station: 16:32 every day; direct bus 16:10 (12 Dec–23 Feb)")],
        tip=T("営業期間・料金・バスは、おたる水族館と中央バスの公式サイトで確認しました。通常期の料金は公式サイトで。",
              "Season, fees and buses from the aquarium’s and Chuo Bus’s websites. See the official site for regular-season fees.")),

    yoichi=dict(
        name=T("余市（よいち）駅", "Yoichi Station"), kind=T("駅", "Station"),
        blurb=T("小樽から各駅停車で24分。蒸溜所は駅前から歩いて5分。電車の本数が少ないので、帰りの時刻を先に。",
                "24 minutes from Otaru by local train, and 5 minutes’ walk to the distillery. Trains are few, so note the return times first."),
        lat=43.18690, lng=140.79479,
        body=T("札幌8:41発の小樽行きに乗り、小樽で9:36発の倶知安（くっちゃん）行きに乗り換えて、余市10:00着。札幌から1,380円です。\n\n"
               "余市から小樽への電車は、昼は12:37・13:43・15:02発と1時間〜1時間20分おき。乗り遅れたら、駅の近くの「余市駅前十字街」から小樽駅前行きの高速バス（約54分・560円）もあります。\n\n"
               "交通系ICカード：小樽〜余市の電車で使えるかは、JR北海道のサイトで確かめられませんでした。きっぷを買えば確実です。JR北海道レールパス（全線）なら乗れます。札幌・登別エリアパスに余市が入るかは要確認です。",
               "Take the 8:41 from Sapporo to Otaru and change there to the 9:36 for Kutchan, arriving at 10:00. ¥1,380 from Sapporo.\n\n"
               "Trains back to Otaru are 60–80 minutes apart in the daytime: 12:37, 13:43, 15:02. If you miss one, highway buses run from the Yoichi-ekimae-jujigai stop near the station to Otaru Station (about 54 minutes, ¥560).\n\n"
               "IC cards: JR Hokkaido’s site does not make clear whether they work between Otaru and Yoichi, so buying a paper ticket is the safe choice. The JR Hokkaido Rail Pass covers it; check whether the Sapporo-Noboribetsu Area Pass does."),
        gmaps=[gm("JR余市駅", "JR Yoichi Station", 43.18690, 140.79479, "JR余市駅")],
        links=[JR],
        rows=[row("train", "札幌8:41→小樽（9:36発に乗り換え）→余市10:00（平日・土曜とも）", "Sapporo 8:41 → Otaru (change to the 9:36) → Yoichi 10:00 (weekdays and Saturdays)"),
              row("train", "余市→小樽：12:37（13:01着）、13:43（14:09着）、15:02（15:26着）", "Yoichi → Otaru: 12:37 (13:01), 13:43 (14:09), 15:02 (15:26)"),
              row("fee", "札幌→余市1,380円、余市→小樽470円。高速バス余市→小樽560円", "Sapporo → Yoichi ¥1,380, Yoichi → Otaru ¥470. Highway bus to Otaru ¥560")],
        tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました。", "Times and fares from a route planner for 3 and 5 December 2026.")),

    nikka=dict(
        name=T("ニッカウヰスキー 北海道 余市蒸溜所", "Nikka Whisky Yoichi Distillery"), kind=T("蒸溜所（ツアーは予約制）", "Distillery (tours by booking)"),
        caution=T("ツアーは予約制・日本語のみ。12月23日〜1月7日は休み", "Tours by booking only, in Japanese. Closed 23 Dec–7 Jan"),
        blurb=T("竹鶴政孝（たけつるまさたか）がスコットランドに似た土地を求めて選んだ蒸溜所。石造りの棟と赤い屋根が並びます。",
                "Taketsuru Masataka chose Yoichi for its Scotland-like climate. Stone buildings with red roofs line the grounds."),
        lat=43.18617, lng=140.78950,
        body=T("・ガイドツアー（無料・試飲つき）は予約制。予約は公式の予約ページ（英語あり）で、4週間先まで。ツアーの案内は日本語だけです。2026年11月の案内では所要60分で、外の製造の建物を歩くので暖かい服で。\n\n"
               "・2026年12月〜2027年1月は、無料のツアーはなく有料のセミナーだけです（お知らせを参照）。2月からのツアーの時刻は予約ページで。\n\n"
               "・予約なしでも、ニッカミュージアム（有料のテイスティングバーあり）、ショップ、レストラン「RITA'S KITCHEN」（10:00〜15:50、ラストオーダー15:20）に入れます。入口はショップ側で、最終入場は15:30、すべて16:15に閉まります。2026年12月5日はレストランだけ休み。\n\n"
               "・食べ物の持ち込みはできません。100円が戻るロッカーは、ツアーを予約した人だけ使えます。",
               "• The guided tour (free, with tasting) needs a booking on the official booking site (English available), up to four weeks ahead. Tours are in Japanese only. In November 2026 they took 60 minutes, partly outdoors, so dress warmly.\n\n"
               "• From December 2026 to January 2027 there are no free tours, only a paid seminar (see the notice). Check the booking site for tour times from February.\n\n"
               "• Without a booking you can visit the Nikka Museum (with a paid tasting bar), the shop and RITA’S KITCHEN restaurant (10:00–15:50, last order 15:20). Use the shop entrance; last entry 15:30, everything closes at 16:15. The restaurant alone is closed on 5 December 2026.\n\n"
               "• No outside food. The coin-return lockers (¥100) are for tour guests only."),
        gmaps=[gm("ニッカウヰスキー 余市蒸溜所", "Nikka Yoichi Distillery", 43.18617, 140.78950, "ニッカウヰスキー 北海道 余市蒸溜所")],
        links=[link("official", "ニッカ 余市蒸溜所（楽しみ方）", "Nikka Yoichi Distillery (official)", U["nikka"], U["nikka_en"]),
               link("official", "見学予約（日本語・英語）", "Tour booking (Japanese / English)", U["nikka_book"]),
               link("info", "予約サイトのお知らせ", "Booking site notices", U["nikka_news"])],
        rows=[row("hours", "予約なしの施設は最終入場15:30、全施設16:15まで。レストラン10:00〜15:50（LO15:20）", "Walk-in areas: last entry 15:30, all close 16:15. Restaurant 10:00–15:50 (last order 15:20)"),
              row("closed", "12月23日〜1月7日、6月11日", "23 Dec–7 Jan, 11 June"),
              row("fee", "ガイドツアー無料（予約制）。12〜1月はセミナーのみ（料金は予約ページで）", "Guided tour free (booking needed). Dec–Jan: paid seminar only (fee on the booking site)")],
        tip=T("ニッカウヰスキーの公式サイトと、公式の見学予約サイトのお知らせ（2026年10〜11月）で確認しました。",
              "Checked on Nikka’s website and the notices on its official booking site (October–November 2026).")),
)

# ---------------------------------------------------------------------------
# コースごとの時間割
#   pre: 名前のすぐ下に出る段落、time: いちばん下の行、notices・rows・caution・blurb・name は共通部分に足す／入れ替える
# ---------------------------------------------------------------------------
LATE = dict(
    file="otaru.json", course="late",
    order=["sapporo", "otarueki", "sankaku", "temiya", "kitaunga", "unga", "ginko", "kitaichi", "meruhen", "asakusa", "tengu", "yuhan", "kaeri"],
    spots=dict(
        sapporo=dict(
            pre=T("札幌9:33発の快速エアポートで小樽10:07着（平日・土曜とも）。早めのお昼を市場で食べて、運河を北の端から南へ歩き、銀行街と堺町通りへ。暗くなるころに浅草橋に戻って、天狗山の夜景と晩ごはん。札幌には20〜22時ごろ戻ります。\n\n冬（12〜3月）の日の入りに合わせた時間割です。夏は天狗山を晩ごはんのあとにします（天狗山のスポットに時刻）。",
                  "The 9:33 Rapid Airport reaches Otaru at 10:07 (weekdays and Saturdays). An early lunch at the market, the canal from its quiet north end southwards, the bank street and Sakaimachi; back to Asakusa Bridge at dusk, then the night view from Mt. Tengu and dinner. You are back in Sapporo between 20:00 and 22:00.\n\nThis timetable follows winter sunsets (December–March). In summer, go up Mt. Tengu after dinner (times under Mt. Tengu)."),
            notices=[N_WINTER_WALK, N_YEAREND],
            rows=[row("train", "札幌9:33→小樽10:07（快速エアポート）。普通なら9:16発（10:01着）か9:25発（10:15着）", "Sapporo 9:33 → Otaru 10:07 (Rapid Airport). Local trains: 9:16 (10:01) or 9:25 (10:15)")],
            time=(DEP, "9:33（札幌駅に9:20ごろ）", "9:33 (be at Sapporo Station by about 9:20)")),
        otarueki=dict(time=(VIS, "10:07〜10:15", "10:07–10:15")),
        sankaku=dict(
            pre=T("10:15から早めのお昼。12時前後より並ばずに入りやすい時間です。", "An early lunch from 10:15, before the noon queues."),
            time=(VIS, "10:15〜11:00", "10:15–11:00")),
        temiya=dict(
            pre=T("中央通りを下って線路の跡へ。北へ15分ほど線路ぞいを歩いて、色内のあたりで海側の北運河へ下ります。",
                  "Walk down Chuo-dori to the old line, follow it north for about 15 minutes, then head down towards the sea to the North Canal."),
            time=(VIS, "11:05〜11:35", "11:05–11:35")),
        kitaunga=dict(time=(VIS, "11:40〜12:05", "11:40–12:05")),
        unga=dict(
            pre=T("散策路を南へ、中央橋から浅草橋まで。クルーズに乗るなら、ここで1便（40分）足すと銀行街は短めに。",
                  "South along the path from Chuo Bridge to Asakusa Bridge. If you add a 40-minute cruise here, shorten the bank street."),
            time=(VIS, "12:05〜12:30", "12:05–12:30")),
        ginko=dict(
            pre=T("水曜は資料館が休みです。その日は外から建物を見て、堺町通りへ早めに。", "On Wednesdays the museum is closed: see the buildings from outside and move on to Sakaimachi."),
            time=(VIS, "12:35〜13:30", "12:35–13:30")),
        kitaichi=dict(
            pre=T("北一ホールでひと休みしてから、通りを南へ。", "Take a break at Kitaichi Hall, then work your way south along the street."),
            time=(VIS, "13:40〜15:00（北一ホールで休む時間を含む）", "13:40–15:00 (including a break at Kitaichi Hall)")),
        meruhen=dict(
            pre=T("15:40に出て、堺町通りを浅草橋へ戻ります（歩いて15〜20分）。", "Leave at 15:40 and walk back along Sakaimachi to Asakusa Bridge (15–20 minutes)."),
            time=(VIS, "15:00〜15:40", "15:00–15:40")),
        asakusa=dict(
            pre=T("12〜1月は16:00〜16:45が日の入り。明かりがついたら、16:20に浅草橋を出て小樽駅前のバスターミナルへ（上り坂を歩いて12〜15分）。2〜3月は日の入りが遅いので、天狗山は18:40のバスにして、先に晩ごはんでも。",
                  "Sunset is 16:00–16:45 in December and January. Once the lamps are on, leave at 16:20 for the bus terminal at Otaru Station (12–15 minutes uphill). In February and March sunset is later, so you can eat first and take the 18:40 bus up Mt. Tengu."),
            time=(VIS, "16:00〜16:20（12〜1月）", "16:00–16:20 (December–January)")),
        tengu=dict(
            pre=T("小樽駅前16:40のバスで山麓へ（どの日も）。17:00か17:12のロープウエイで上がって、夜景を見たら山麓に下り、18:07のバスで駅前へ（18:25ごろ着）。",
                  "The 16:40 bus from Otaru Station (every day) to the base. Ride up at 17:00 or 17:12, enjoy the view, come down for the 18:07 bus to the station (about 18:25)."),
            notices=[N_TENGU_CLOSED, N_TENGU_SPRING, N_BUS_WINTER],
            time=(VIS, "16:40〜18:25（冬。夏は晩ごはんのあと19:10か19:40のバス）", "16:40–18:25 (winter; in summer, after dinner on the 19:10 or 19:40 bus)")),
        yuhan=dict(
            pre=T("なると本店なら駅前から歩いて7〜8分、小樽倉庫No.1なら12分ほど。", "Naruto is 7–8 minutes’ walk from the bus stop; Otaru Soko No.1 about 12."),
            time=(VIS, "18:35〜19:50", "18:35–19:50")),
        kaeri=dict(
            pre=T("小樽20:22発で札幌21:11着。ゆっくりするなら21:16発（22:03着）。", "The 20:22 reaches Sapporo at 21:11; for a slower evening, the 21:16 (22:03)."),
            time=(DEP, "20:22（札幌21:11着）", "20:22 (Sapporo 21:11)")),
    ),
)

EARLY = dict(
    file="otaru-early.json", course="early",
    order=["sapporo", "otarueki", "sankaku", "asakusa", "kitaichi", "meruhen", "ginko", "temiya", "shukutsu", "aq", "unga", "yuhan", "kaeri"],
    spots=dict(
        sapporo=dict(
            pre=T("札幌7:14発の普通で小樽8:01着（平日・土曜とも。7:05発なら7:51着）。市場で朝ごはん、人の少ない朝の運河、北一ホールのランプの火入れ、開店すぐの堺町通り。昼からは祝津の高台の屋敷と水族館へバスで行き、夜の運河を見て晩ごはん。札幌には20時ごろ戻ります。",
                  "The 7:14 local train reaches Otaru at 8:01 (weekdays and Saturdays; or the 7:05, arriving 7:51). Breakfast at the market, the canal before the crowds, the lamp lighting at Kitaichi Hall and Sakaimachi as it opens. After noon, a bus to the villa on Shukutsu hill and the aquarium, then the canal at night and dinner. Back in Sapporo around 20:00."),
            notices=[N_WINTER_WALK, N_AQ_CLOSED, N_AQ_SPRING, N_YEAREND],
            rows=[row("train", "札幌7:14→小樽8:01（普通）。7:05発なら7:51着", "Sapporo 7:14 → Otaru 8:01 (local). Or 7:05 → 7:51")],
            time=(DEP, "7:14（すすきのから地下鉄なら6:55ごろ）", "7:14 (from Susukino, take the subway around 6:55)")),
        otarueki=dict(time=(VIS, "8:01〜8:05", "8:01–8:05")),
        sankaku=dict(
            pre=T("8:05から朝ごはん。この時間に開いているのは、かわしま（6:00〜）・たけだ（7:00〜）・滝波食堂とさんかく亭（8:00〜）。",
                  "Breakfast from 8:05. Open at this hour: Kawashima (from 6:00), Takeda (from 7:00), Takinami and Sankaku-tei (from 8:00)."),
            time=(VIS, "8:05〜8:35", "8:05–8:35")),
        asakusa=dict(
            pre=T("中央通りを下って浅草橋へ（12分ほど）。朝の運河は人が少なく、雪の日は散策路に足あとが少ないことも。",
                  "Walk down Chuo-dori to Asakusa Bridge (about 12 minutes). The canal is quiet in the morning, and on snowy days the path may be almost untouched."),
            time=(VIS, "8:50〜9:05", "8:50–9:05")),
        kitaichi=dict(
            pre=T("9:05に北一ホールへ。ランプに火を入れる作業は9:30まで、注文は9:30から。", "Into Kitaichi Hall at 9:05: the lamps are lit until 9:30, and orders start at 9:30."),
            time=(VIS, "9:05〜9:50", "9:05–9:50")),
        meruhen=dict(
            pre=T("店が開いたばかりの通りを、メルヘン交差点まで。オルゴール堂は9:00から。", "Down the newly opened street to Märchen Crossing. The Music Box Museum opens at 9:00."),
            time=(VIS, "9:50〜10:40（堺町通りの店を含む）", "9:50–10:40 (including the shops on Sakaimachi)")),
        ginko=dict(
            pre=T("12〜3月は10:00、4〜11月は9:30に開きます。水曜は休みなので、外から建物だけ。", "Opens at 10:00 in December–March, 9:30 in April–November. Closed Wednesdays: see it from outside."),
            time=(VIS, "10:55〜11:35", "10:55–11:35")),
        temiya=dict(
            pre=T("線路の跡を少し歩いてから小樽駅前へ（6分ほど）。12:00の祝津線のバスに乗ります。", "A short walk on the old line, then to Otaru Station (about 6 minutes) for the 12:00 Shukutsu line bus."),
            time=(VIS, "11:40〜11:52", "11:40–11:52")),
        shukutsu=dict(
            pre=T("小樽駅前12:00の祝津線（赤岩経由、どの日も）で終点のおたる水族館へ（12:25ごろ）。坂を上って貴賓館でお昼と見学。",
                  "The 12:00 Shukutsu line bus via Akaiwa (every day) to the last stop, Otaru Aquarium (about 12:25). Walk up the hill to Kihinkan for lunch and a look round."),
            time=(VIS, "12:45〜14:00（お昼を含む）", "12:45–14:00 (including lunch)")),
        aq=dict(
            pre=T("坂を下って水族館へ。冬期は15:30までに入館。帰りは16:10の直行バス（12月12日〜2月23日）か、16:32の祝津線。",
                  "Walk down to the aquarium; in winter you must be in by 15:30. Back on the 16:10 direct bus (12 Dec–23 Feb) or the 16:32 Shukutsu line."),
            time=(VIS, "14:15〜16:00", "14:15–16:00")),
        unga=dict(
            pre=T("小樽駅前から運河へ下ります（12分ほど）。冬はもう暗く、倉庫とガス灯の明かりが水面に映ります。ナイトクルーズは12月は18:00の便まで。",
                  "Walk down from the station to the canal (about 12 minutes). In winter it is already dark, with the warehouse lights and gas lamps in the water. In December the last night cruise is at 18:00."),
            time=(VIS, "17:00〜17:30", "17:00–17:30")),
        yuhan=dict(
            pre=T("中央橋のそばの小樽倉庫No.1がすぐです。なると本店なら駅へ戻る途中。", "Otaru Soko No.1 is right by Chuo Bridge; Naruto is on the way back to the station."),
            time=(VIS, "17:35〜19:00", "17:35–19:00")),
        kaeri=dict(
            pre=T("小樽19:27の快速エアポートで札幌20:01着。", "The 19:27 Rapid Airport reaches Sapporo at 20:01."),
            time=(DEP, "19:27（札幌20:01着）", "19:27 (Sapporo 20:01)")),
    ),
)

YOICHI = dict(
    file="otaru-yoichi.json", course="yoichi",
    order=["sapporo", "yoichi", "nikka", "otarueki", "ginko", "kitaichi", "meruhen", "asakusa", "yuhan", "tengu", "kaeri"],
    spots=dict(
        sapporo=dict(
            pre=T("札幌8:41発で余市10:00着。予約した回のツアー（12〜1月はセミナー）と蒸溜所のレストランでお昼。13:43の電車で小樽に戻って、銀行街と堺町通り、暗くなるころの運河と晩ごはん。天狗山の夜景を足すと札幌着は22時ごろです。\n\n蒸溜所の見学は予約制です（予約ページは英語あり、4週間前から）。",
                  "The 8:41 from Sapporo reaches Yoichi at 10:00. Your booked tour (a seminar in December–January) and lunch at the distillery restaurant, then the 13:43 train back to Otaru for the bank street, Sakaimachi, the canal at dusk and dinner. Add the Mt. Tengu night view and you are back in Sapporo around 22:00.\n\nDistillery tours need a booking (English booking site, opens four weeks ahead)."),
            caution=T("蒸溜所は12月23日〜1月7日休み", "Distillery closed 23 Dec–7 Jan"),
            notices=[N_NIKKA_CLOSED, N_NIKKA_WINTER, N_WINTER_WALK],
            time=(DEP, "8:41（札幌駅に8:30ごろ）", "8:41 (be at Sapporo Station by about 8:30)")),
        yoichi=dict(time=(MOV, "10:00着", "arrive 10:00")),
        nikka=dict(
            pre=T("10:05に入って、まず予約なしで入れるミュージアムへ。10:30（12〜1月のセミナー）か11:00ごろのツアーを予約しておくと、12:00すぎにレストランでお昼にできます。13:35に駅へ。",
                  "In at 10:05 and start in the walk-in museum. Book the 10:30 seminar (December–January) or a tour around 11:00, and you can have lunch at the restaurant just after 12:00. Leave for the station at 13:35."),
            notices=[N_NIKKA_WINTER],
            time=(VIS, "10:05〜13:35（お昼を含む）", "10:05–13:35 (including lunch)")),
        otarueki=dict(
            pre=T("余市13:43発で小樽14:09着。中央通りを下って銀行街へ（歩いて12分ほど）。", "The 13:43 from Yoichi arrives at 14:09. Walk down Chuo-dori to the bank street (about 12 minutes)."),
            time=(MOV, "14:09着", "arrive 14:09")),
        ginko=dict(
            pre=T("水曜は資料館が休みなので、外から建物だけ。", "Closed on Wednesdays: see the buildings from outside."),
            time=(VIS, "14:25〜15:00", "14:25–15:00")),
        kitaichi=dict(time=(VIS, "15:10〜15:55（北一ホールで休む時間を含む）", "15:10–15:55 (including a break at Kitaichi Hall)")),
        meruhen=dict(
            pre=T("16:15に出て、堺町通りを浅草橋へ戻ります。", "Leave at 16:15 and walk back along Sakaimachi to Asakusa Bridge."),
            time=(VIS, "15:55〜16:15", "15:55–16:15")),
        asakusa=dict(
            pre=T("12月はもう暗くなるころ、1〜2月はちょうど日の入りのころです。", "Dark already in December; right around sunset in January and February."),
            time=(VIS, "16:30〜16:50", "16:30–16:50")),
        yuhan=dict(
            pre=T("浅草橋から小樽倉庫No.1まで歩いて5分ほど。天狗山へ行く人は18:25に店を出て駅前へ。",
                  "Otaru Soko No.1 is about 5 minutes from Asakusa Bridge. Heading up Mt. Tengu? Leave at 18:25 for the bus terminal."),
            time=(VIS, "17:00〜18:25", "17:00–18:25")),
        tengu=dict(
            pre=T("寄り道：小樽駅前18:40のバスで山麓へ（どの日も）、ロープウエイで夜景を見て、20:07のバスで駅前へ（20:25ごろ）。小樽21:16発で札幌22:03着です。",
                  "Optional: the 18:40 bus from Otaru Station (every day), the ropeway up for the night view, and the 20:07 bus back (about 20:25). The 21:16 train reaches Sapporo at 22:03."),
            notices=[N_TENGU_CLOSED, N_TENGU_SPRING],
            time=(VIS, "18:40〜20:25", "18:40–20:25")),
        kaeri=dict(
            pre=T("天狗山に行かない日は、小樽19:00か19:27の快速エアポートで札幌19:34・20:01着。天狗山に行った日は21:16発（22:03着）。",
                  "Without Mt. Tengu, the 19:00 or 19:27 Rapid Airport reaches Sapporo at 19:34 or 20:01. After Mt. Tengu, the 21:16 (22:03)."),
            time=(DEP, "19:00か19:27（天狗山に行った日は21:16）", "19:00 or 19:27 (21:16 after Mt. Tengu)")),
    ),
)


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
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"], links=o.get("links", b.get("links", [JR])),
               notices=o.get("notices", []),
               info={"rows": o.get("rows", []) + b["rows"], "cash": sid == "shukutsu", "tip": b["tip"], "checked": CHECKED},
               photos=PHOTOS[sid])
    assert out["photos"], sid
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


for C in (LATE, EARLY, YOICHI):
    N = {k: i for i, k in enumerate(C["order"], 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
    picks = [N[k] for k in C["order"] if k not in ("sapporo", "otarueki", "kaeri", "yoichi")]
    auto = {str(N["sapporo"]): {"always": True}, str(N["otarueki"]): {"always": True}, str(N["kaeri"]): {"always": True}}
    hints = []
    if C is LATE:
        default = picks
        sections = [{"first": 1, "last": N["otarueki"], "area": T("札幌→小樽", "Sapporo → Otaru"), "title": T("9:33の快速エアポートで小樽へ", "The 9:33 Rapid Airport to Otaru")},
                    {"first": N["sankaku"], "last": N["unga"], "area": T("小樽・運河", "Otaru · canal"), "title": T("市場でお昼、線路の跡から運河を北から南へ", "Lunch at the market, then the canal from north to south")},
                    {"first": N["ginko"], "last": N["meruhen"], "area": T("小樽・色内と堺町", "Otaru · Ironai & Sakaimachi"), "title": T("銀行街と堺町通り", "The bank street and Sakaimachi")},
                    {"first": N["asakusa"], "last": N["kaeri"], "area": T("小樽・夜", "Otaru · evening"), "title": T("夕暮れの運河、天狗山の夜景、晩ごはん", "Dusk at the canal, the night view, dinner")}]
        hints = [
            h("kaeri", {"none": ns("tengu")},
              "天狗山に行かない日は、夕暮れの運河のあとにナイトクルーズ（12月は18:00の便まで）か、そのまま晩ごはんへ。小樽19:27発で札幌20:01着です。",
              "Skipping Mt. Tengu? After dusk at the canal, take a night cruise (last one 18:00 in December) or go straight to dinner. The 19:27 reaches Sapporo at 20:01."),
            h("temiya", {"none": ns("kitaunga")},
              "北運河を外すと、旧手宮線から中央通りへ戻って中央橋へ。15分ほど早くなります。",
              "Without the North Canal, go back along the old line to Chuo-dori and Chuo Bridge: about 15 minutes saved."),
        ]
        note = "「9〜10時に出る」。札幌9:33→小樽10:07。三角市場で早めのお昼→旧手宮線→北運河→運河→銀行街→堺町→浅草橋の夕暮れ（冬）→天狗山→晩ごはん→小樽20:22発。"
        focus = {"first": 2, "last": N["kaeri"]}
    elif C is EARLY:
        default = picks
        sections = [{"first": 1, "last": N["sankaku"], "area": T("札幌→小樽", "Sapporo → Otaru"), "title": T("7:14の電車で、市場の朝ごはん", "The 7:14 train and breakfast at the market")},
                    {"first": N["asakusa"], "last": N["temiya"], "area": T("小樽・朝", "Otaru · morning"), "title": T("人の少ない運河と、開店すぐの堺町", "The quiet canal and Sakaimachi as it opens")},
                    {"first": N["shukutsu"], "last": N["aq"], "area": T("祝津", "Shukutsu"), "title": T("祝津の高台の屋敷と水族館", "The villa on Shukutsu hill and the aquarium")},
                    {"first": N["unga"], "last": N["kaeri"], "area": T("小樽・夜", "Otaru · evening"), "title": T("夜の運河と晩ごはん", "The canal at night and dinner")}]
        hints = [
            h("shukutsu", {"none": ns("aq"), "andAny": ns("shukutsu")},
              "水族館に寄らない日は、貴賓館のあと祝津の港や高台を歩いて、水族館前から16:32のバス（どの日も）で小樽へ。",
              "Skipping the aquarium? After Kihinkan, walk around the harbour and the hill, then take the 16:32 bus (every day) from the aquarium stop."),
        ]
        note = "「7時台に出る」。札幌7:14→小樽8:01。三角市場で朝ごはん→浅草橋の朝→北一ホール（ランプ9:00〜9:30）→堺町→銀行街→手宮線→12:00のバスで祝津（貴賓館・水族館）→16:32のバス→夜の運河→晩ごはん→小樽19:27発。"
        focus = {"first": 2, "last": N["kaeri"]}
    else:
        auto[str(N["yoichi"])] = {"any": ns("nikka")}
        default = [n for n in picks if n != N["tengu"]]
        sections = [{"first": 1, "last": N["nikka"], "area": T("余市", "Yoichi"), "title": T("8:41の電車で余市の蒸溜所へ（予約制）", "The 8:41 train to the Yoichi distillery (booking needed)")},
                    {"first": N["otarueki"], "last": N["meruhen"], "area": T("小樽・午後", "Otaru · afternoon"), "title": T("13:43の電車で小樽へ、銀行街と堺町", "The 13:43 to Otaru, the bank street and Sakaimachi")},
                    {"first": N["asakusa"], "last": N["kaeri"], "area": T("小樽・夜", "Otaru · evening"), "title": T("夕暮れの運河と晩ごはん（天狗山は寄り道）", "Dusk at the canal and dinner (Mt. Tengu optional)")}]
        hints = [
            h("tengu", {"any": ns("tengu")},
              "天狗山を入れると、札幌に着くのは22:03（小樽21:16発）です。",
              "With Mt. Tengu you reach Sapporo at 22:03 (the 21:16 from Otaru)."),
            h("nikka", {"none": ns("nikka")},
              "蒸溜所に行かない日は、「9〜10時に出る」コースに切り替えてください。",
              "Not going to the distillery? Switch to the 9–10 o’clock course."),
        ]
        note = "「余市蒸溜所＋午後の小樽」。札幌8:41→余市10:00。ニッカ（予約。12〜1月はセミナーのみ）→余市13:43→小樽14:09→銀行街→堺町→浅草橋→晩ごはん→（天狗山は寄り道）→小樽19:27発。"
        focus = {"first": 2, "last": N["kaeri"]}
    data = {
        "id": "otaru", "course": C["course"],
        "_note": "小樽（札幌から日帰り。otaru/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "写真はすべて Wikimedia Commons（一覧は scripts/otaru_web_photos.json）。info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。"
                 + "このファイルは scripts/build_otaru_data.py で作る（直接直さない）。",
        "sections": sections, "focus": focus,
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。札幌駅・小樽駅・帰りは自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": default, "auto": auto, "hints": hints},
        "photoBase": "../images/otaru/", "sources": SOURCES,
        "spots": [spot(C, i, k) for i, k in enumerate(C["order"], 1)],
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"]) for s in data["spots"]], "default", default)
