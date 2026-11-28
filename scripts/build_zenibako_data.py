#!/usr/bin/env python3
"""銭函と朝里（札幌から日帰り）のデータを書き出す。コースは1つ。

使い方: python3 scripts/build_zenibako_data.py   （そのあと python3 scripts/sync_zenibako.py）
- data/routes/zenibako.json … 札幌10:00発→銭函（駅・豊足神社・浜でお昼）→朝里（海べりの駅）→バスで朝里川温泉→小樽で晩ごはん→札幌 8か所
- 起点は札幌駅〜大通〜すすきののホテル（北海道のマップの決まり、2026-11-26）。9〜10時に出る1コース。
  昼間に激しく混む場所がないので、早朝のコースは作っていない。冬（12〜3月）もこのまま回れる（外を歩くのは14時半まで）。
  冬・夏の違いは notices と rows に書いてある（どちらも毎年のことなので日付は付けていない。海水浴場の期間だけ2026年の実績）
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 時刻は2026年12月3日（木）・5日（土）のダイヤ（乗換案内）と、北海道中央バスの公式時刻表（2026年4月1日改定）。
  JR北海道は2027年3月にダイヤ改正があるはずなので、そのあとは確かめ直す
- 写真はすべて Wikimedia Commons（オーナーはまだ北海道の写真を持っていない）。一覧とクレジットは scripts/zenibako_web_photos.json。
  オーナーの写真はあとで images/zenibako/<スポットのid>-<番号>.jpg として足す（ネットの写真は -w<番号>）
- 行っていない場所なので文章は中立に。店名は、公式サイトでその時間に開いていると確かめた店だけ
  （しろくまコーヒー・手打ちそば 春別・徳光珈琲 銭函店・小樽倉庫No.1）
- 星置の滝（札幌市手稲区）は札幌市の公式ページで「崩落の恐れがあるため当面の間通行止め」なので入れていない。
  北海道ワインは公式に「バスの便がなく、歩いての来場は安全上すすめない」とあるので入れていない（タクシーなら行ける）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/zenibako"
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


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def notice(hja, hen, ja, en, url=None, start=None, to=None):
    d = {"head": T(hja, hen), "text": T(ja, en), "from": start, "to": to}
    if url:
        d["url"] = url
    return d


def q(f, t, day, hm, kind="d"):
    """確かめた乗換案内（Yahoo!路線情報）の検索結果のURL。day は '2026/12/03' の形"""
    h, m = hm.split(":")
    y, mon, d = day.split("/")
    p = dict(to=t, y=y, m=mon, d=d, hh=h, m1=m[0], m2=m[1], type={"d": 1, "l": 2, "a": 4}[kind], ticket="ic",
             expkind=1, shin=1, ex=1, lb=1, al=0, hb=1, sr=0, s=0, userpass=0, ws=3)
    p["from"] = f
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(p)


def cc(x):
    """Wikimedia Commons の写真。"""
    return {"file": x["file"], "credit": {"author": x["author"], "license": x["license"],
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(x["title"].replace(" ", "_"))}}


WEB = json.load(open(f"{R}/scripts/zenibako_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]

NV = "https://transfer.navitime.biz/chuo-bus/pc/diagram/"
U = dict(
    brewery="https://otarubeer.com/jp/Ppage_id=353.html", soko="https://otarubeer.com/jp/Ppage_id=357.html",
    shirokuma="https://shirokumacoffee.com/", shirokuma_en="https://shirokumacoffee.com/en/", shirokuma_menu="https://shirokumacoffee.com/cafemenu/",
    shunbetsu="https://teuchisoba-syunbetsu.jimdofree.com/", tokumitsu="https://tokumitsu-coffee.com/shop",
    shrine="https://hokkaidojinjacho.jp/%e8%b1%8a%e8%b6%b3%e7%a5%9e%e7%a4%be/",
    jishin="https://otaru.gr.jp/citizen/otarujishin-202107", column="https://otaru.gr.jp/column/sengoku_ryoutarou",
    festival="https://otaru.gr.jp/citizen/2026-shrine-festival",
    beach="https://www.city.otaru.lg.jp/docs/2020100901012/",
    hotel="https://asarigawaonsenhotel.com/", hotel_en="https://asarigawaonsenhotel.com/en/",
    bus_asari=NV + "BusDiagram?orvCode=00300020&course=0005601306&stopNo=16",
    bus_back=NV + "BusDiagram?orvCode=00300083&course=0005604150&stopNo=3",
    bus_otaru=NV + "BusDiagram?orvCode=00300075&course=0005601306&stopNo=1",
    run_go_wd=NV + "BusRouteTimetable?operation=803d0029&datetime=2026-11-25T14%3A05%3A00&node=00300075&course=0005601306&stop-no=1",
    run_go_sat=NV + "BusRouteTimetable?operation=803d0018&datetime=2026-11-28T14%3A05%3A00&node=00300075&course=0005601306&stop-no=1",
    run_back_wd=NV + "BusRouteTimetable?operation=803e002e&datetime=2026-11-25T17%3A56%3A00&node=00300083&course=0005604150&stop-no=3",
    run_back_sat=NV + "BusRouteTimetable?operation=803e001c&datetime=2026-11-28T17%3A56%3A00&node=00300083&course=0005604150&stop-no=3",
    run_late_wd=NV + "BusRouteTimetable?operation=803e0031&datetime=2026-11-25T20%3A51%3A00&node=00300083&course=0005604150&stop-no=3",
    run_late_sat=NV + "BusRouteTimetable?operation=803e001f&datetime=2026-11-28T20%3A51%3A00&node=00300083&course=0005604150&stop-no=3",
    run_1951=NV + "BusRouteTimetable?operation=803e0030&datetime=2026-11-25T19%3A51%3A00&node=00300083&course=0005604150&stop-no=3",
    busfaq="https://www.chuo-bus.co.jp/support/faq/",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    jr_regular="https://www.jrhokkaido.co.jp/global/english/ticket/regular/index.html",
    unkou="https://www3.jrhokkaido.co.jp/webunkou/",
    sun="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html", sun6="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0006.html",
    hoshioki="https://www.city.sapporo.jp/teine/midokoro/midokoro1.html", wine="https://www.hokkaidowine.com/tours/",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("札幌→銭函 平日", q("札幌", "銭函", "2026/12/03", "09:00"), "9:16→9:42、9:25→9:56、快速エアポート35号 10:00→10:21、IC・きっぷとも470円"),
    ("札幌→銭函 土曜", q("札幌", "銭函", "2026/12/05", "09:00"), "9:16→9:42、9:25→9:56、10:00→10:21（快速エアポート35号）"),
    ("札幌→銭函 10時台 平日", q("札幌", "銭函", "2026/12/03", "09:30"), "10:00→10:21、10:06→10:33"),
    ("大通→さっぽろ 平日", q("大通", "札幌", "2026/12/03", "09:40"), "地下鉄南北線 乗車2分、210円（9:43発で札幌9:52、歩く時間を含む）"),
    ("すすきの→さっぽろ 平日", q("すすきの", "札幌", "2026/12/03", "09:40"), "乗車4分、210円（9:41発で札幌9:52）"),
    ("すすきの→さっぽろ 土曜", q("すすきの", "札幌", "2026/12/05", "09:40"), "9:42発で札幌9:53、210円"),
    ("銭函→朝里 平日", q("銭函", "朝里", "2026/12/03", "12:40"), "12:55→13:03、快速エアポート71号 13:22→13:30、13:54→14:02、310円"),
    ("銭函→朝里 土曜", q("銭函", "朝里", "2026/12/05", "12:40"), "12:55→13:03、13:22→13:30、13:54→14:02"),
    ("銭函→朝里 午後", q("銭函", "朝里川温泉", "2026/12/03", "14:00"), "快速エアポート83号 銭函14:22→朝里14:30（その先のバスは乗換案内に出ない）"),
    ("朝里→小樽 平日・土曜", q("朝里", "小樽", "2026/12/03", "14:05"), "快速エアポート83号 14:30→14:41、15:03→15:14、310円（12/5も同じ）"),
    ("中央バス13番 朝里町（朝里川温泉行き）", U["bus_asari"], "2026年4月1日改定。平日 12:27 13:27 14:27 15:28 16:28、土曜・日祝 12:27 13:27 14:27 15:27 16:27"),
    ("中央バス13番 14:05の便 平日", U["run_go_wd"], "小樽駅前14:05→小樽築港駅14:20→朝里町14:27→温泉南14:39→朝里川温泉14:41"),
    ("中央バス13番 14:05の便 土曜", U["run_go_sat"], "朝里町14:27→温泉南14:39"),
    ("中央バス13番 温泉南（小樽駅前行き）", U["bus_back"], "2026年4月1日改定。平日・土曜・日祝 15:56 17:01 17:56 18:51 19:51 20:51（最終）"),
    ("中央バス13番 温泉南17:56の便 平日", U["run_back_wd"], "朝里町18:07→小樽築港駅18:14→小樽駅前18:32"),
    ("中央バス13番 温泉南17:56の便 土曜", U["run_back_sat"], "朝里町18:06→小樽築港駅18:13→小樽駅前18:29"),
    ("中央バス13番 温泉南19:51の便 平日", U["run_1951"], "小樽築港駅20:08→小樽駅前20:23"),
    ("中央バス13番 温泉南20:51の便（最終）", U["run_late_wd"], "平日 小樽築港駅21:08→小樽駅前21:23"),
    ("中央バス13番 温泉南20:51の便 土曜", U["run_late_sat"], "小樽築港駅21:07→小樽駅前21:21"),
    ("中央バス 小樽駅前（朝里川温泉行き）", U["bus_otaru"], "13番 平日 13:05 14:05 15:05、土曜 13:05 14:05 15:05"),
    ("中央バス よくある質問", U["busfaq"], "全国相互利用の交通系ICカード（10種類）が使える。現金はおつりが出ない。車内の両替機は千円札・硬貨のみ（5千円・1万円・2千円札は不可）"),
    ("小樽築港→札幌 夕方 平日・土曜", q("小樽築港", "札幌", "2026/12/03", "18:14"), "18:15→18:56、快速エアポート166号 18:36→19:07（12/5も同じ）"),
    ("小樽築港→札幌 夜 平日・土曜", q("小樽築港", "札幌", "2026/12/03", "20:12"), "20:28→21:11、20:44→21:23、800円（12/5も同じ）"),
    ("小樽築港→札幌 最終のバスのあと", q("小樽築港", "札幌", "2026/12/03", "21:12"), "21:22→22:03、21:43→22:24（12/5も同じ）"),
    ("小樽→札幌 夜 平日", q("小樽", "札幌", "2026/12/03", "20:40"), "20:57→21:44、21:16→22:03、800円"),
    ("小樽→札幌 夜 土曜", q("小樽", "札幌", "2026/12/05", "20:40"), "20:57→21:44、21:16→22:03、21:37→22:24"),
    ("小樽→札幌 最終 平日・土曜", q("小樽", "札幌", "2026/12/03", "23:59", "l"), "最終23:08→23:53（12/5も同じ）"),
    ("JR北海道 北海道レールパス", U["railpass"], "JR北海道の全線（新幹線を除く）の特急・快速・普通の普通車に乗れる"),
    ("JR北海道 札幌〜小樽のきっぷ", U["jr_regular"], "札幌〜小樽 自由席800円・指定席1,800円。自由席はICカードだけで乗れる"),
    ("小樽ビール 銭函醸造所 見学", U["brewery"], "要予約（1週間前まで、電話 平日9:00〜17:00）。2〜20名、1人2,200円の1コース、開始11:00・15:00。銭函駅から徒歩20分。所要時間の記載は今のコースにはない"),
    ("小樽ビール 小樽倉庫No.1", U["soko"], "11:00〜22:00（料理L.O.21:00・飲み物L.O.21:30）、不定休。木・土は2時間飲み放題2,600円・予約不要。セルフ見学は無料・試飲なし。銭函醸造所は業務用の樽と瓶ビールの醸造所"),
    ("しろくまコーヒー", U["shirokuma"], "今月の営業時間9:00〜16:30（L.O.16:30）。パリドッグ・ホットサンドなど。銭函駅の目の前。英語のページあり"),
    ("しろくまコーヒー メニュー", U["shirokuma_menu"], "パリドッグ、サバサンド、ホットサンド各種（値段の記載なし）"),
    ("手打ちそば 春別", U["shunbetsu"], "11:00〜19:00（売切次第終了）、定休日 金曜日、小樽市銭函3丁目186-27、銭函駅から車で6分。幌加内産そば粉、つぶこん"),
    ("徳光珈琲 銭函店", U["tokumitsu"], "10:00〜17:00（L.O.16:30）、定休日 日・月・第2・4火曜日、小樽市銭函2丁目2-8"),
    ("豊足神社（北海道神社庁）", U["shrine"], "小樽市銭函2丁目9番10号。例祭日6月25日。安永9年（1780）、松前の商人阿部屋伝次郎が銭函村以北の鎮守として豊受大神を勧請"),
    ("豊足神社（小樽観光協会 月刊小樽自身2021年7月号）", U["jishin"], "銭函駅裏側の高台、白っぽい鳥居。日露戦争でロシア軍が爆破した機雷の残骸が浜で見つかり展示。2月の「雪あかりの路」の会場"),
    ("小樽市内 神社の例大祭 令和8年度", U["festival"], "豊足神社 6月27日（土）〜28日（日）"),
    ("小樽観光協会のコラム（銭函〜朝里）", U["column"], "銭函駅は昭和6年の駅舎、銭箱が置かれたホーム、ゼニキューブ（ZとNに見えるイス）。銭函から張碓・朝里の海岸。札幌方面から小樽へ進むと銭函から海が見える。海の向こうに浜益から増毛の山々"),
    ("小樽市 海水浴場 令和8年度", U["beach"], "銭函海水浴場7/4〜8/24（JR銭函駅から徒歩10分）、おたるドリームビーチ6/26〜8/31。朝里は今年度の5か所に入っていない"),
    ("朝里川温泉ホテル", U["hotel"], "日帰り入浴11:00〜20:00（最終受付19:30）、大人850円、土日祝・年末年始1,000円。フェイスタオル販売200円・バスタオルレンタル200円。家族風呂（貸切・要予約）60分3,000円、日帰りは11:00〜20:00（最終受付19:00）、3名から追加料金。サウナは日帰り20:00まで。中央バス13番で小樽築港駅から15分、温泉南から徒歩2分、大人410円。タトゥーの記載なし"),
    ("朝里川温泉ホテル（英語）", U["hotel_en"], "Day trip bathing 11:00-20:00 (last entry 19:30)、Family Bath need reservation、タトゥーの記載なし"),
    ("日の入り（札幌）12月", U["sun"], "12/1 16:01、12/15 16:00、12/21 16:03、12/31 16:09"),
    ("日の入り（札幌）6月", U["sun6"], "6/15 19:16、6/21 19:18、6/30 19:18"),
    ("星置の滝（札幌市手稲区）", U["hoshioki"], "崩落の恐れがあるため、当面の間通行止め（ページの更新日2023年1月18日）→ 入れていない"),
    ("北海道ワイン おたるワインギャラリー", U["wine"], "9:00〜17:00 年中無休（年末年始を除く）。バスの直行便・経由便はなく、徒歩での来場は安全上すすめない。南小樽駅からタクシー約3,750円 → 入れていない"),
    ("JR北海道 運行情報", U["unkou"], "運行情報のページ"),
    ("銭函駅（Wikipedia）", "https://ja.wikipedia.org/wiki/%E9%8A%AD%E5%87%BD%E9%A7%85", "1880年（明治13年）11月28日 手宮〜札幌の開業とともに正式開業、北海道で最初の駅の1つ。1931年12月 現行駅舎。ニシン漁による地名"),
]]

JR = link("timetable", "JR北海道 運行情報", "JR Hokkaido service status", U["unkou"], "https://www3.jrhokkaido.co.jp/webunkou/en/")
JRPASS = link("info", "北海道レールパス（JR北海道）", "Hokkaido Rail Pass (JR Hokkaido)", U["railpass"])
BUSFAQ = link("info", "北海道中央バス よくある質問（運賃の払い方）", "Chuo Bus FAQ: paying the fare (Japanese)", U["busfaq"])

# 何か所かに出すお知らせ
N_SNOW_JR = notice(
    "冬（12〜3月）：雪の日はJRが遅れることがあります", "Winter (Dec–Mar): snow can delay trains",
    "大雪や強い風の日は、JRが遅れたり止まったりすることがあります。出る前と、帰る前に、JR北海道の運行情報を見てください。",
    "Heavy snow or strong wind can delay or stop JR trains. Check JR Hokkaido’s service status before you set out and before you head back.",
    U["unkou"])
N_SNOW_WALK = notice(
    "冬（12〜3月）：凍った道と早い日の入り", "Winter (Dec–Mar): icy paths, early sunset",
    "歩道は雪が踏み固められて凍ります。底がすべりにくい靴で。12月の日の入りは16:00ごろ（札幌）なので、外を歩くところは午前と、お昼すぎの朝里までにしてあります。",
    "Pavements turn to packed ice. Wear shoes with grippy soles. In December the sun sets at about 16:00 (Sapporo), so the outdoor parts of this day are in the morning and early afternoon.",
    U["sun"])
N_SEA_WINTER = notice(
    "冬の浜は、波打ち際に近づかない", "On the winter beach, keep back from the waves",
    "風の強い日は波が高く、雪が横から吹きつけます。浜は短めにして、しろくまコーヒーの窓から海を見るのでも十分です。",
    "On windy days the waves run high and snow blows sideways. Keep the beach walk short; the view from the windows of Shirokuma Coffee is just as good.")
N_BREWERY = notice(
    "醸造所の見学は、1週間前までに電話で予約", "Brewery tours: book by phone a week ahead",
    "小樽ビール銭函醸造所の見学（試飲つき・1人2,200円、11:00か15:00の開始、2〜20人）は、1週間前までの電話予約（平日9:00〜17:00、日本語）だけです。予約なしでは入れません。",
    "The Otaru Beer Zenibako brewery tour (with tasting, ¥2,200 per person, starting at 11:00 or 15:00, groups of 2–20) is by phone booking only, at least a week ahead (weekdays 9:00–17:00, in Japanese). There are no walk-ins.",
    U["brewery"])
N_BUS_PAY = notice(
    "バスの運賃：ICカードか、くずした現金で", "Bus fare: IC card or small change",
    "中央バスは、Kitaca・Suicaなどの交通系ICカード（10種類）が使えます。現金のときはおつりが出ません。車内の両替機で千円札と硬貨はくずせますが、5千円札・1万円札は使えません。運賃は降りるときに払います。北海道レールパスでは乗れません（JRではないため）。",
    "Chuo Bus takes IC cards such as Kitaca and Suica. If you pay cash, no change is given: the on-board machine changes ¥1,000 notes and coins, but not ¥5,000 or ¥10,000 notes. Pay as you get off. The Hokkaido Rail Pass is not valid (this is not a JR bus).",
    U["busfaq"])
N_TATTOO = notice(
    "タトゥー：公式に決まりが書かれていません", "Tattoos: no policy is published",
    "朝里川温泉ホテルの公式サイトには、タトゥーの決まりが書かれていません（要確認）。貸切の家族風呂（60分3,000円・要予約）があるので、タトゥーのある人は、予約のときに使えるかを聞いてから行くのが確実です。",
    "Asarigawa Onsen Hotel does not publish a tattoo policy on its website, so please check. It has a private family bath (¥3,000 for 60 minutes, booking required): if you have tattoos, the safest plan is to book it and ask when you do.",
    U["hotel"])
N_SUMMER = notice(
    "夏（7〜8月）は海水浴場が開きます", "In summer (Jul–Aug) the beaches open",
    "2026年は、駅から東へ歩いて10分の銭函海水浴場が7月4日〜8月24日、その先のおたるドリームビーチが6月26日〜8月31日でした。泳ぐのは、監視員のいる遊泳区域の中だけで。来年の期間は小樽市の発表で確かめてください。",
    "In 2026 Zenibako beach, ten minutes’ walk east of the station, was open for swimming 4 July–24 August, and Otaru Dream Beach further on 26 June–31 August. Swim only inside the marked, lifeguarded area. Check Otaru City’s page for next year’s dates.",
    U["beach"])

# ---------------------------------------------------------------------------
# スポット（回る順）
# ---------------------------------------------------------------------------
SPOTS = [
    dict(
        id="sapporo", name=T("札幌駅（出発）", "Sapporo Station (start)"), kind=T("駅", "Station"),
        blurb=T("10:00の快速エアポート（小樽行き）で、銭函に10:21。", "The 10:00 Rapid Airport for Otaru reaches Zenibako at 10:21."),
        lat=43.06862, lng=141.35073,
        body=T("小樽行きの快速エアポートに乗って21分。ひとつ前の9:25発の普通（9:56着）でも、次の10:06発の普通（10:33着）でもかまいません。快速エアポートは指定席の車両だけ別料金で、ほかは自由席です。\n\n"
               "大通・すすきののホテルからは、地下鉄南北線でさっぽろ駅まで2〜4分（210円）。地下鉄を降りてからJRの改札まで少し歩くので、9:35ごろにホテルを出れば間に合います。\n\n"
               "大きな荷物はホテルに預けて出てください。JRは交通系ICカード（Kitaca・Suicaなど）でそのまま乗れ、北海道レールパスでも乗れます。",
               "Take the Rapid Airport bound for Otaru: 21 minutes to Zenibako. The local trains just before and after work too (9:25, arriving 9:56; 10:06, arriving 10:33). On the Rapid Airport only the reserved car costs extra; the rest of the train is unreserved.\n\n"
               "From hotels around Odori or Susukino, the Namboku subway line reaches Sapporo Station in 2–4 minutes (¥210). Allow a few minutes to walk from the subway to the JR gates: leaving your hotel at about 9:35 is enough.\n\n"
               "Leave big bags at your hotel. You can ride JR with an IC card (Kitaca, Suica and others) or the Hokkaido Rail Pass."),
        gmaps=[gm("JR札幌駅", "JR Sapporo Station", 43.06862, 141.35073, "JR札幌駅")],
        links=[JR, JRPASS],
        notices=[N_SNOW_JR],
        rows=[row("train", "札幌10:00 → 銭函10:21（快速エアポート35号・小樽行き。平日・土曜とも）。470円", "Sapporo 10:00 → Zenibako 10:21 (Rapid Airport 35 for Otaru; weekdays and Saturdays). ¥470"),
              row("train", "前後の電車：9:25発（9:56着）、10:06発（10:33着）。どちらも普通", "Trains either side: 9:25 (arr. 9:56) and 10:06 (arr. 10:33), both local"),
              row("train", "地下鉄南北線：大通・すすきの → さっぽろ 2〜4分・210円", "Namboku subway: Odori or Susukino → Sapporo, 2–4 min, ¥210"),
              row("pay", "JRは交通系ICカード（自由席）と北海道レールパスで乗れます", "JR: IC cards (unreserved seats) and the Hokkaido Rail Pass are accepted")],
        tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）を確認しました。JR北海道は2027年3月にダイヤ改正の予定なので、春からは時刻が変わることがあります。",
              "Times and fares checked in a route planner for Thu 3 and Sat 5 December 2026. JR Hokkaido usually revises its timetable in March, so times may change from spring 2027."),
        time=(DEP, "10:00発（ホテルは9:35ごろ出る）", "10:00 (leave your hotel at about 9:35)"),
        photos=W("sapporo")),

    dict(
        id="zenibako", name=T("JR銭函駅", "Zenibako Station"), kind=T("駅・町", "Station & town"),
        blurb=T("1880年からある駅。1931年（昭和6年）の駅舎と、ホームの「銭函」。", "A station since 1880, with a 1931 station house and a money box on the platform."),
        lat=43.14348, lng=141.15972,
        body=T("銭函（ぜにばこ）の名前は、ニシンがよくとれたころ、どの家にも銭の箱が積まれていたから、と言われています。駅は1880年、北海道で最初の鉄道（小樽の手宮〜札幌）が通ったときからの駅で、いまの駅舎は1931年（昭和6年）に建てられたものです。\n\n"
               "ホームには名前にちなんだ「銭函」が飾ってあります。駅の中の椅子「ゼニキューブ」は、見る向きでZとNの字に見える形です。\n\n"
               "駅のそばには、徳光珈琲の銭函店もあります（10:00〜17:00、日・月・第2・4火曜休み）。\n\n"
               "ビールが好きな人へ：駅から歩いて20分ほどの小樽ビール銭函醸造所は、予約制で見学できます（上のお知らせ）。11:00の回に入る日は、駅から醸造所へ行き、お昼は近くの手打ちそば 春別（4番の中で紹介）へ。駅に戻って浜と神社を見て、14:22の電車で朝里へ。温泉へのバスは15:28（土日祝は15:27）になります。見学の所要時間は公式サイトに書かれていないので、予約のときに確かめてください。",
               "Zenibako means “money box”: the story goes that in the herring-fishing days every household had boxes of cash piled up. The station opened in 1880 with Hokkaido’s first railway (Temiya in Otaru to Sapporo), and the present station house was built in 1931.\n\n"
               "A wooden money box hangs on the platform, and the “Zeni Cube” seats inside the station look like a Z or an N depending on where you stand.\n\n"
               "Tokumitsu Coffee also has a Zenibako shop near the station (10:00–17:00, closed Sun, Mon and the 2nd and 4th Tue).\n\n"
               "For beer lovers: the Otaru Beer Zenibako brewery, about 20 minutes’ walk away, runs tours by reservation (see the notice above). On the 11:00 tour, walk from the station to the brewery and have lunch at Shunbetsu soba nearby (in no. 4). Then come back for the beach and the shrine and take the 14:22 to Asari; the bus to the hot spring is then the 15:28 (15:27 on weekends and holidays). The tour length is not given on the website, so ask when you book."),
        gmaps=[gm("JR銭函駅", "JR Zenibako Station", 43.14348, 141.15972, "JR銭函駅"),
               gm("小樽ビール 銭函醸造所（見学は予約制）", "Otaru Beer Zenibako brewery (tours by booking)", 43.14087, 141.17383, "小樽ビール 銭函醸造所"),
               gm("徳光珈琲 銭函店", "Tokumitsu Coffee Zenibako", 43.14343, 141.16063, "徳光珈琲 銭函店")],
        links=[link("info", "銭函と朝里の海（小樽観光協会のコラム）", "Zenibako and Asari coast (Otaru Tourism Association, Japanese)", U["column"]),
               link("official", "小樽ビール 銭函醸造所 見学", "Otaru Beer Zenibako brewery tours (Japanese)", U["brewery"]),
               link("official", "徳光珈琲 店舗案内", "Tokumitsu Coffee shops (Japanese)", U["tokumitsu"])],
        notices=[N_BREWERY],
        rows=[row("hours", "徳光珈琲 銭函店：10:00〜17:00（L.O.16:30）、日・月・第2・4火曜休み", "Tokumitsu Coffee Zenibako: 10:00–17:00 (last order 16:30), closed Sun, Mon, 2nd and 4th Tue"),
              row("reserve", "醸造所の見学：1週間前までに電話予約（平日9:00〜17:00）。11:00か15:00の開始、2〜20人、1人2,200円", "Brewery tour: phone at least a week ahead (weekdays 9:00–17:00). Starts 11:00 or 15:00, 2–20 people, ¥2,200 each")],
        tip=T("駅舎と「銭函」は小樽観光協会のコラム、開業の年はWikipedia（銭函駅）から。店の時間と醸造所の見学は、それぞれの公式サイトで2026年11月26日に確認しました。",
              "Station house and money box from an Otaru Tourism Association column; opening year from Wikipedia (Zenibako Station). Shop hours and the brewery tour checked on each official website on 26 November 2026."),
        time=(VIS, "10:21〜10:35", "10:21–10:35"),
        photos=W("zenibako")),

    dict(
        id="toyotari", name=T("豊足神社（とよたりじんじゃ）", "Toyotari Shrine"), kind=T("神社・高台", "Hilltop shrine"),
        blurb=T("駅の裏の高台。白っぽい鳥居と、浜で見つかった日露戦争の機雷。", "On the hill behind the station: a pale torii and a Russo-Japanese War mine found on the beach."),
        caution=T("冬は坂と石段が凍ります", "Slope and steps are icy in winter"),
        lat=43.14271, lng=141.16074,
        body=T("駅の裏から坂を上って5分。1780年、石狩川と近くの海の鮭漁を任された松前の商人が、銭函から北の漁場の守り神として祀ったのが始まりです。\n\n"
               "白っぽい鳥居が目印です。境内の忠魂碑のわきには、日露戦争のときにロシア軍が爆破した機雷の残骸が置かれています。この浜で見つかったものです。\n\n"
               "例大祭は6月下旬（2026年は6月27・28日）。",
               "A five-minute climb from behind the station. In 1780 a merchant from Matsumae, put in charge of salmon fishing on the Ishikari River and nearby coast, enshrined a guardian deity here for the fishing grounds north of Zenibako.\n\n"
               "Look for the pale torii gate. Beside the war memorial in the grounds lie the remains of a mine that Russian forces blew up during the Russo-Japanese War; it was found on this beach.\n\n"
               "The annual festival is in late June (27–28 June in 2026)."),
        gmaps=[gm("豊足神社", "Toyotari Shrine", 43.14271, 141.16074, "豊足神社 小樽市銭函")],
        links=[link("info", "豊足神社（北海道神社庁）", "Toyotari Shrine (Hokkaido Association of Shinto Shrines, Japanese)", U["shrine"]),
               link("info", "小樽の神社（小樽観光協会）", "Otaru’s shrines (Otaru Tourism Association, Japanese)", U["jishin"])],
        notices=[N_SNOW_WALK],
        rows=[row("walk", "銭函駅から歩いて5分（上り坂と石段）", "5 minutes on foot from the station (uphill, with steps)")],
        tip=T("由緒は北海道神社庁、機雷のことは小樽観光協会の記事（2021年7月）、例大祭の日は小樽観光協会の令和8年度の一覧から。",
              "History from the Hokkaido Association of Shinto Shrines; the mine from an Otaru Tourism Association article (July 2021); festival dates from its 2026 list."),
        time=(VIS, "10:40〜11:05", "10:40–11:05"),
        photos=W("toyotari")),

    dict(
        id="hama", name=T("銭函の浜と、海の前でお昼", "Zenibako beach, and lunch by the sea"), kind=T("海・お昼", "Beach & lunch"),
        blurb=T("駅の目の前が石狩湾。浜を歩いて、海の見えるカフェでお昼。", "Ishikari Bay is right outside the station: walk the beach, then lunch with a sea view."),
        lat=43.14402, lng=141.16009,
        body=T("駅から海の側へ出ると、すぐ浜です。晴れた日は、湾の向こうに浜益（はまます）から増毛（ましけ）の山並みが見え、冬は雪をかぶっています。\n\n"
               "お昼は、浜の目の前のしろくまコーヒーで。バゲットにチーズとソーセージをはさんだパリドッグや、ホットサンドがあります。窓から海が見えて、冬は雪と海がいっしょに見えます。営業時間は月によって変わります（2026年11月は9:00〜16:30）。英語のページもあります。\n\n"
               "しっかり食べたい人は、駅から東へ歩いて22分の手打ちそば 春別へ。幌加内（ほろかない）産のそば粉の手打ちそばと、つぶ貝を昆布で巻いて揚げた「つぶこん」が名物です（11:00〜19:00、売り切れまで。金曜休み）。13:22の電車に乗るなら、12:50ごろに店を出ます。",
               "Step out of the station on the sea side and you are on the beach. On a clear day the mountains from Hamamasu to Mashike line the far side of the bay, snow-capped in winter.\n\n"
               "For lunch, Shirokuma Coffee sits right on the beach: a “Paris dog” (baguette with cheese and sausage) or a toasted sandwich, with the sea out of the window — and in winter, snow and sea together. Opening hours change by the month (9:00–16:30 in November 2026). The website has an English page.\n\n"
               "For a proper meal, walk 22 minutes east to Shunbetsu for handmade soba from Horokanai buckwheat, and its signature “tsubukon”, sea snail wrapped in kelp and fried (11:00–19:00 or until sold out, closed Fridays). Leave by about 12:50 to make the 13:22 train."),
        gmaps=[gm("しろくまコーヒー", "Shirokuma Coffee", 43.14402, 141.16009, "しろくまコーヒー 銭函"),
               gm("手打ちそば 春別", "Shunbetsu (soba)", 43.14386, 141.17655, "手打ちそば 春別 銭函"),
               gm("銭函の浜（駅の海側）", "Zenibako beach (sea side of the station)", 43.14440, 141.16080, "銭函海岸")],
        links=[link("official", "しろくまコーヒー", "Shirokuma Coffee (English)", U["shirokuma"], U["shirokuma_en"]),
               link("official", "手打ちそば 春別", "Shunbetsu soba (Japanese)", U["shunbetsu"]),
               link("info", "小樽市の海水浴場", "Otaru City beaches (Japanese)", U["beach"])],
        notices=[N_SEA_WINTER, N_SUMMER],
        rows=[row("hours", "しろくまコーヒー：2026年11月は9:00〜16:30（L.O.16:30）。月によって変わり、休みの日は公式サイトで", "Shirokuma Coffee: 9:00–16:30 in November 2026 (last order 16:30). Hours change by the month; see the website for closed days"),
              row("hours", "手打ちそば 春別：11:00〜19:00（売り切れ次第終了）、金曜休み", "Shunbetsu: 11:00–19:00 (closes when sold out), closed Fridays"),
              row("season", "海水浴場：2026年は銭函が7月4日〜8月24日、おたるドリームビーチが6月26日〜8月31日", "Swimming beaches in 2026: Zenibako 4 Jul–24 Aug, Otaru Dream Beach 26 Jun–31 Aug")],
        tip=T("店の時間は各店の公式サイト、海水浴場は小樽市の令和8年度の案内、山の見え方は小樽観光協会のコラムから（2026年11月26日に確認）。",
              "Shop hours from each shop’s website, beach dates from Otaru City’s 2026 page, the mountain view from an Otaru Tourism Association column (checked 26 November 2026)."),
        time=(VIS, "11:10〜13:15（お昼を含む）", "11:10–13:15 (including lunch)"),
        photos=W("hama")),

    dict(
        id="asari", name=T("朝里駅と、海べりの線路", "Asari Station and the line by the sea"), kind=T("駅・海", "Station & shore"),
        blurb=T("銭函から8分。線路のすぐ横が海の、小さな駅。", "Eight minutes from Zenibako: a small station with the sea right beside the tracks."),
        lat=43.17691, lng=141.06369,
        body=T("銭函13:22発の快速エアポートで8分。銭函を出ると、張碓（はりうす）のあたりから線路のすぐ横が海になります。札幌の側から乗るときは、進行方向の右側の窓に（帰りの小樽から札幌へは左側）。\n\n"
               "朝里（あさり）の駅のまわりは石の浜で、海のすぐそばを電車が走り抜けます。浜からホームの電車と海をいっしょに眺めて、14:05ごろにバス停「朝里町」へ（歩いて15分）。14:27発の中央バス13番「朝里川温泉」行きに乗ります。\n\n"
               "バスはJRではないので、北海道レールパスでは乗れません。ICカードか、くずした現金で（上のお知らせ）。",
               "The 13:22 Rapid Airport from Zenibako takes eight minutes. Past Zenibako, from around Hariusu, the sea runs right beside the line: coming from the Sapporo side, sit on the right (on the way back from Otaru to Sapporo, the left).\n\n"
               "Asari Station sits on a stony shore, and the trains run along the water’s edge. Watch them pass from the beach, then at about 14:05 walk to the Asarimachi bus stop (15 minutes) for the 14:27 Chuo Bus no. 13 to Asarigawa Onsen.\n\n"
               "The bus is not JR, so the Hokkaido Rail Pass does not cover it. Use an IC card or small change (see the notice)."),
        gmaps=[gm("JR朝里駅", "JR Asari Station", 43.17691, 141.06369, "JR朝里駅"),
               gm("バス停 朝里町（朝里川温泉行き）", "Asarimachi bus stop (for Asarigawa Onsen)", 43.17571, 141.05816, "朝里町 バス停 小樽")],
        links=[link("timetable", "中央バス13番 朝里町の時刻表", "Bus no. 13 timetable at Asarimachi (Japanese)", U["bus_asari"]), BUSFAQ],
        notices=[N_BUS_PAY,
                 notice("冬（12〜3月）：バスは雪で遅れることがあります", "Winter (Dec–Mar): buses can run late in snow",
                        "バス停で待つ時間に備えて、帽子と手袋を。乗り遅れたら次は15:28（土日祝は15:27）です。",
                        "Bring a hat and gloves for the wait at the stop. If you miss it, the next bus is 15:28 (15:27 on weekends and holidays).",
                        U["bus_asari"])],
        rows=[row("train", "銭函13:22 → 朝里13:30（快速エアポート71号。平日・土曜とも）。310円。前の電車は12:55発（13:03着）", "Zenibako 13:22 → Asari 13:30 (Rapid Airport 71; weekdays and Saturdays). ¥310. The train before: 12:55 (arr. 13:03)"),
              row("bus", "朝里町14:27 → 温泉南14:39（中央バス13番・朝里川温泉行き。平日・土曜とも）。次は15:28（土日祝15:27）", "Asarimachi 14:27 → Onsen-minami 14:39 (Chuo Bus no. 13 for Asarigawa Onsen; weekdays and Saturdays). Next: 15:28 (15:27 weekends and holidays)"),
              row("fee", "バスの運賃は要確認（小樽築港駅から温泉南までは410円と、朝里川温泉ホテルの案内）", "Bus fare not confirmed (¥410 from Otaru-Chikko Station to Onsen-minami, according to Asarigawa Onsen Hotel)")],
        tip=T("電車は乗換案内（2026年12月3日・5日）、バスは北海道中央バスの公式時刻表（2026年4月1日改定）で確認しました。海の見える側は、線路と海岸の位置（地図）から。",
              "Trains from a route planner (3 and 5 December 2026); buses from Chuo Bus’s official timetable (revised 1 April 2026). The sea side of the train is worked out from the line and the coast on the map."),
        time=(VIS, "13:30〜14:27（バスまで）", "13:30–14:27 (until the bus)"),
        photos=W("asari")),

    dict(
        id="onsen", name=T("朝里川温泉（朝里川温泉ホテルの日帰り入浴）", "Asarigawa Onsen (day bathing at Asarigawa Onsen Hotel)"), kind=T("温泉", "Hot spring"),
        blurb=T("谷あいの温泉街で、露天風呂とサウナ。17:56のバスまで。", "A hot-spring village up the valley: outdoor bath and sauna until the 17:56 bus."),
        caution=T("タトゥーの決まりは公式に書かれていません（要確認）", "No published tattoo policy (please check)"),
        lat=43.14193, lng=141.04058,
        body=T("朝里川（あさりがわ）の谷をバスで12分上ると、温泉街です。「温泉南」で降りて歩いて2分の朝里川温泉ホテルは、日帰りで大浴場と露天風呂、セルフロウリュのできるフィンランド式サウナに入れます。休憩所もあります。\n\n"
               "はじめての人へ：湯船に入る前に体を洗い、タオルはお湯に入れません。水着は着ずに入ります。浴場の中では写真を撮りません。\n\n"
               "帰りは温泉南17:56発のバスで小樽駅前へ（18:32着、土曜は18:29着）。夜まで入るなら、19:51か20:51（最終）のバスで小樽築港駅へ出て、JRで札幌へ（小樽築港20:28発→札幌21:11、21:22発→22:03）。その場合、晩ごはんは札幌で。",
               "The bus climbs the Asari River valley for 12 minutes to the hot-spring village. Asarigawa Onsen Hotel, two minutes on foot from the Onsen-minami stop, lets day visitors use its large bath, outdoor bath and a Finnish sauna where you pour water on the stones yourself. There is a rest area too.\n\n"
               "First time in a Japanese bath? Wash before you get in, keep your towel out of the water, bathe without a swimsuit, and take no photos inside.\n\n"
               "Head back on the 17:56 bus from Onsen-minami to Otaru Station (arr. 18:32; 18:29 on Saturdays). To stay into the evening, take the 19:51 or the last 20:51 bus to Otaru-Chikko Station and the train to Sapporo (20:28 → 21:11, or 21:22 → 22:03), and have dinner in Sapporo."),
        gmaps=[gm("朝里川温泉ホテル", "Asarigawa Onsen Hotel", 43.14193, 141.04058, "朝里川温泉ホテル")],
        links=[link("official", "朝里川温泉ホテル（日帰り入浴）", "Asarigawa Onsen Hotel (English)", U["hotel"], U["hotel_en"]),
               link("timetable", "中央バス13番 温泉南の時刻表（小樽駅前行き）", "Bus no. 13 timetable at Onsen-minami (Japanese)", U["bus_back"])],
        notices=[N_TATTOO],
        rows=[row("hours", "日帰り入浴：11:00〜20:00（受付は19:30まで）", "Day bathing: 11:00–20:00 (last entry 19:30)"),
              row("fee", "大人850円、土日祝・年末年始は1,000円。フェイスタオル200円、バスタオル（貸し出し）200円", "Adults ¥850; ¥1,000 on weekends, holidays and over New Year. Face towel ¥200, bath towel rental ¥200"),
              row("tattoo", "公式サイトに記載なし（要確認）。貸切の家族風呂：60分3,000円・要予約（日帰りは11:00〜20:00、受付19:00まで。3人目から追加料金）", "Not stated on the website (please check). Private family bath: ¥3,000 for 60 min, booking required (day visitors 11:00–20:00, last entry 19:00; extra charge from the 3rd person)"),
              row("bus", "帰り：温泉南17:56 → 小樽築港駅18:14 → 小樽駅前18:32（土曜は18:13・18:29）。そのあとは18:51・19:51・20:51（最終）", "Back: Onsen-minami 17:56 → Otaru-Chikko Sta. 18:14 → Otaru Sta. 18:32 (Sat 18:13, 18:29). Later buses 18:51, 19:51, 20:51 (last)")],
        tip=T("時間と料金は朝里川温泉ホテルの公式サイト、バスは北海道中央バスの公式時刻表（2026年4月1日改定）で、2026年11月26日に確認しました。",
              "Hours and prices from the hotel’s website and buses from Chuo Bus’s official timetable (revised 1 April 2026), checked on 26 November 2026."),
        time=(VIS, "14:45〜17:50", "14:45–17:50"),
        photos=W("onsen")),

    dict(
        id="soko", name=T("小樽倉庫No.1（晩ごはん）", "Otaru Soko No.1 (dinner)"), kind=T("ビール・晩ごはん", "Beer & dinner"),
        blurb=T("運河沿いの石の倉庫の中に醸造所。小樽ビールと晩ごはん。", "A brewery inside a stone warehouse by the canal: Otaru Beer and dinner."),
        caution=T("不定休", "Closes on irregular days"),
        lat=43.19903, lng=141.00269,
        body=T("小樽駅前でバスを降りて、海のほうへ歩いて15分。運河沿いの倉庫の中に醸造所があるビアパブです。小樽ビールの醸造所は2つあり、朝に通った銭函のほうは樽と瓶のビールを造る醸造所、ここは店のまん中の仕込み釜がいまも使われています。2階の回廊の窓から発酵タンクがのぞけ、見学は無料・予約なし（試飲なし）。\n\n"
               "木曜と土曜は「プロスト」の日で、2時間のビール飲み放題が2,600円（予約なし）。席の予約は電話で（0134-21-2323）。\n\n"
               "料理のラストオーダーは21:00。20:35ごろ店を出れば、小樽20:57発の電車に乗れます。ゆっくりするなら21:16発で。",
               "Get off the bus at Otaru Station and walk 15 minutes towards the sea. This beer pub has its brewery inside a canal-side warehouse. Otaru Beer has two breweries: the Zenibako one you passed this morning makes kegs and bottles, while here the brew kettle in the middle of the pub is still in use. You can look into the fermentation tanks from the upstairs gallery; the self-guided visit is free, with no booking (no tasting).\n\n"
               "Thursdays and Saturdays are “Prost” days: two hours of all-you-can-drink beer for ¥2,600, no booking needed. To book a table, phone 0134-21-2323 (Japanese).\n\n"
               "Food last orders are at 21:00. Leave at about 20:35 for the 20:57 train from Otaru, or stay on for the 21:16."),
        gmaps=[gm("小樽倉庫No.1", "Otaru Soko No.1", 43.19903, 141.00269, "小樽倉庫No.1 小樽ビール")],
        links=[link("official", "小樽ビール 小樽倉庫No.1", "Otaru Beer: Otaru Soko No.1 (Japanese)", U["soko"])],
        notices=[],
        rows=[row("hours", "11:00〜22:00（料理L.O.21:00、飲み物L.O.21:30）。不定休", "11:00–22:00 (food last order 21:00, drinks 21:30). Closes on irregular days"),
              row("fee", "木・土の飲み放題：2時間2,600円（予約不要）。見学は無料", "Thu and Sat all-you-can-drink: ¥2,600 for 2 hours (no booking). Brewery visit free"),
              row("walk", "小樽駅から歩いて15分", "15 minutes on foot from Otaru Station")],
        tip=T("時間と料金は小樽ビールの公式サイトで2026年11月26日に確認しました。季節やイベントで時間が変わることがあります。",
              "Hours and prices from Otaru Beer’s website, checked on 26 November 2026. They can change with the season or events."),
        time=(VIS, "18:50〜20:35", "18:50–20:35"),
        photos=W("soko")),

    dict(
        id="kaeri", name=T("小樽駅から札幌へ", "Otaru Station, back to Sapporo"), kind=T("駅", "Station"),
        blurb=T("20:57発で札幌21:44。最終は23:08発。", "The 20:57 reaches Sapporo at 21:44; the last train is 23:08."),
        lat=43.19745, lng=140.99410,
        body=T("小樽20:57発で札幌21:44着（800円）。次は21:16発（22:03着）。札幌への最終は23:08発（23:53着）です。\n\n"
               "札幌駅から大通・すすきのへは地下鉄南北線で。",
               "The 20:57 from Otaru reaches Sapporo at 21:44 (¥800); the next is the 21:16 (22:03). The last train to Sapporo leaves at 23:08 (arr. 23:53).\n\n"
               "From Sapporo Station, the Namboku subway runs to Odori and Susukino."),
        gmaps=[gm("JR小樽駅", "JR Otaru Station", 43.19745, 140.99410, "JR小樽駅")],
        links=[JR],
        notices=[N_SNOW_JR],
        rows=[row("train", "小樽20:57 → 札幌21:44、21:16 → 22:03（平日・土曜とも）。800円", "Otaru 20:57 → Sapporo 21:44, 21:16 → 22:03 (weekdays and Saturdays). ¥800"),
              row("train", "最終：小樽23:08 → 札幌23:53", "Last train: Otaru 23:08 → Sapporo 23:53")],
        tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）を確認しました。", "Times and fares checked in a route planner for Thu 3 and Sat 5 December 2026."),
        time=(DEP, "20:57発", "the 20:57"),
        photos=W("kaeri")),
]


def spot(no, b):
    label, tja, ten = b["time"]
    text = {}
    for l in ("ja", "en"):
        parts = [b["name"][l], b["body"][l]]
        parts.append(f"{label[0]}：{tja}" if l == "ja" else f"{label[1]}: {ten}")
        text[l] = "\n\n".join(parts)
    out = {"no": no, "id": b["id"], "name": b["name"], "kind": b["kind"], "blurb": b["blurb"]}
    if b.get("caution"):
        out["caution"] = b["caution"]
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"], links=b["links"], notices=b["notices"],
               info={"rows": b["rows"], "cash": False, "tip": b["tip"], "checked": CHECKED},
               photos=b["photos"])
    assert out["photos"], b["id"]
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


N = {s["id"]: i for i, s in enumerate(SPOTS, 1)}
ns = lambda *ks: [N[k] for k in ks]
h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
hints = [
    h("asari", {"any": ns("asari"), "none": ns("onsen")},
      "温泉に入らない日は、朝里14:30発の快速エアポートで小樽へ（14:41着）。小樽の町を歩いてから、晩ごはんの小樽倉庫No.1へ。",
      "Skipping the hot spring? Take the 14:30 Rapid Airport from Asari to Otaru (arr. 14:41), explore the town, then go on to Otaru Soko No.1 for dinner."),
    h("onsen", {"any": ns("onsen"), "none": ns("soko")},
      "晩ごはんを札幌で食べる日は、17:56のバスを小樽築港駅で降りて（18:14着、土曜は18:13）、18:36の快速エアポートで札幌19:07着。",
      "Eating in Sapporo tonight? Get off the 17:56 bus at Otaru-Chikko Station (18:14; 18:13 on Saturdays) and take the 18:36 Rapid Airport to Sapporo (19:07)."),
]
data = {
    "id": "zenibako",
    "_note": "銭函と朝里（zenibako/ のページ専用。形は eizan-line.json と同じ）。札幌10:00発→銭函→朝里→朝里川温泉→小樽で晩ごはん→札幌。コースは1つ、最初は「全部回る」。"
             "写真はすべて Wikimedia Commons（一覧は scripts/zenibako_web_photos.json）。info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。"
             "このファイルは scripts/build_zenibako_data.py で作る（直接直さない）。",
    "sections": [
        {"first": 1, "last": 1, "area": T("札幌", "Sapporo"), "title": T("札幌から快速で21分", "21 minutes from Sapporo by rapid train")},
        {"first": 2, "last": 4, "area": T("銭函", "Zenibako"), "title": T("午前：駅と丘の神社、海の前でお昼", "Morning: the station, the hilltop shrine, lunch by the sea")},
        {"first": 5, "last": 6, "area": T("朝里", "Asari"), "title": T("午後：海べりの駅から、谷の温泉へ", "Afternoon: from the seaside station up to the hot spring")},
        {"first": 7, "last": 8, "area": T("小樽", "Otaru"), "title": T("夜：運河沿いでビールと晩ごはん、札幌へ", "Evening: beer and dinner by the canal, then Sapporo")},
    ],
    "focus": {"first": 2, "last": 8},
    "plan": {"_note": "札幌駅・銭函駅・小樽駅はいつも入る。最初は「全部回る」（時間割どおり）。",
             "picks": ns("toyotari", "hama", "asari", "onsen", "soko"),
             "auto": {str(N["sapporo"]): {"always": True}, str(N["zenibako"]): {"always": True}, str(N["kaeri"]): {"always": True}},
             "hints": hints},
    "photoBase": "../images/zenibako/", "sources": SOURCES,
    "spots": [spot(i, s) for i, s in enumerate(SPOTS, 1)],
}
with open(f"{R}/data/routes/zenibako.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("wrote zenibako.json", [(s["no"], s["id"], len(s["photos"])) for s in data["spots"]])
