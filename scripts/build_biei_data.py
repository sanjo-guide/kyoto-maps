#!/usr/bin/env python3
"""美瑛・青い池と富良野（旭川から日帰り）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_biei_data.py   （そのあと python3 scripts/sync_biei.py）
- data/routes/biei.json         … late  ＝雪のない季節（4月下旬〜10月）。自転車で丘→お昼→バスで青い池→白ひげの滝→白金温泉→美瑛で晩ごはん（10か所）
- data/routes/biei-winter.json  … early ＝冬（11月〜4月中旬）。クリスマスツリーの木→お昼→バスで白ひげの滝→白金温泉→青い池のライトアップ（8か所）
- data/routes/biei-furano.json  … furano＝花畑（5〜10月）。中富良野のファーム富田→美馬牛の四季彩の丘→美瑛の町（6か所）
  （late / early はコース切り替えの仕組みの名前を借りているだけ。どれも旭川9:38発。最初にどれで開くかは日付で決める＝scripts/sync_biei.py）
- 起点は旭川駅のまわりのホテル（北海道のマップの決まり、2026-11-26）。車を運転しない人が前提。
  だれかが行った・食べたことは書かない（写真は全部 Wikimedia Commons）
- 冬の富良野（ニングルテラスなど）のコースは作っていない：ふらのバス「ラベンダー号」の旭川行きの最終が新富良野プリンスホテル15:55発で、
  灯りのつく時間まで居ると路線バスで帰れない。ファーム富田の畑も冬は雪の下
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの時間割（pre）→ 共通の説明（body）→ おすすめの時間」の順に組み立てる
- JR の時刻は乗換案内の2026年12月3日（木）・5日（土）のダイヤ。JR北海道のダイヤ改正（2027年春）のあとは確かめ直す
  （雪のない季節のコースと花畑のコースは、2027年に使う前に必ず。夏は臨時列車「富良野・美瑛ノロッコ号」と臨時のラベンダー畑駅もある）
- 道北バス 39番・42番（美瑛・白金線）は公式の時刻表（2026年10月1日改正、平日・土日祝とも同じ）。年末年始は特別ダイヤ（12月に公表）
- 青い池・ビルケの森のライトアップは2026年10月22日〜2027年4月21日。次の冬の期間・時間が出たら LIGHT と notices を直す
- 冬の定期観光バス（美遊バス ライトアップコース、クリスマスツリーライナー）は2026-27年の冬の内容。次の冬は観光協会のページで確かめて直す
- 写真は images/biei/<スポットのid>-w<番号>.jpg（Wikimedia Commons。一覧は scripts/biei_web_photos.json）。
  あとでオーナーの写真を <スポットのid>-<番号>.jpg で入れるときは、PHOTOS の先頭にファイル名を足す
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/biei"
CHECKED = "2026-11-28"
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


WEB = json.load(open(f"{R}/scripts/biei_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]
SIDS = ("asahikawa", "eki", "xmas", "hokusei", "kenmary", "seven", "machi", "pond", "falls", "onsen", "kaeri", "tomita", "bibaushi", "shikisai")
# オーナーの写真が入ったら、ここで W(...) の前にファイル名を足す（例: "pond": ["pond-1.jpg"] + W("pond")）
PHOTOS = {k: W(k) for k in SIDS}

D1, D2 = "2026-12-03", "2026-12-05"     # 乗換案内で確かめた日：木曜と土曜
BK = "https://www.biei-hokkaido.jp/ja"
U = dict(
    bus_wd="https://www.dohokubus.com/files/houmen/kaguraoka_biei_heijitu.pdf",
    bus_hd="https://www.dohokubus.com/files/houmen/kaguraoka_biei_kyuujitu.pdf",
    bus_out="https://www.dohokubus.com/passing/11.pdf", bus_back="https://www.dohokubus.com/passing/12.pdf",
    bus_top="https://www.dohokubus.com/rosen_bus.html", bus_pay="https://www.dohokubus.com/touch-payment.html",
    bus_pass="https://dohokubus.tourbooking-japan.com/A/ja-JP/product-detail/1358",
    bus_stop="https://www.biei-hokkaido.jp/wp3/wp-content/uploads/2024/09/busstop-revised-on-October-1-2024.pdf",
    light=f"{BK}/27188", light_town="https://town.biei.hokkaido.jp/culture/event/illuminate.html",
    tour=f"{BK}/202627ws", tour_news=f"{BK}/27888",
    pond=f"{BK}/shirogane-blue-pond", pond_shop=f"{BK}/facility/aoiike", birke=f"{BK}/facility/shirogane-biruke",
    falls=f"{BK}/facility/shirahige-waterfalls", onsen=f"{BK}/hot-spring",
    park="https://www.biei-hotelparkhills.com/daytrip/", rin="https://www.shirogane-kankou.com/spa/", yuyu="https://www.shiroganeonsen.com/spa/",
    hoyou="https://town.biei.hokkaido.jp/facility/hoyou.html",
    kura=f"{BK}/facility/okanokura", tower=f"{BK}/facility/shiki-no-tou-tower", meal=f"{BK}/meal",
    namaste="https://namaste-hokkaido.com/biei/", gio=f"{BK}/facility/gio",
    cruise=f"{BK}/cruise", faq=f"{BK}/faq", about=f"{BK}/about-us", manner=f"{BK}/bieikankou-manner110",
    hokusei=f"{BK}/facility/hokusei-no-oka", kenmary=f"{BK}/facility/ken-merry-tree", seven=f"{BK}/facility/seven-stars-tree",
    en="https://www.biei-hokkaido.jp/en/",
    shikisai="http://www.shikisainooka.jp/about/guide/", shikisai_w="http://www.shikisainooka.jp/winter/",
    shikisai_bk=f"{BK}/facility/shikisai-no-oka-flower-park", shikisai_en="http://www.shikisainooka.jp/en/",
    tomita="https://www.farm-tomita.co.jp/", tomita_cafe="https://www.farm-tomita.co.jp/cafe/", tomita_acc="https://www.farm-tomita.co.jp/access/",
    tomita_sta="https://www.farm-tomita.co.jp/access/station.asp", tomita_en="https://www.farm-tomita.co.jp/en/",
    lavender="https://www.furanobus.jp/lavender/index.html",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    kitaca="https://www.jrhokkaido.co.jp/kitaca/02area.html",
    jr_info="https://www3.jrhokkaido.co.jp/webunkou/",
    sun_dec="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html", sun_jan="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0001.html",
    sun_feb="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0002.html",
)
SUN = row("hours", "日の入り（札幌の値。旭川もほぼ同じころ）：12月1日16:01、1月31日16:45、2月28日17:22", "Sunset (Sapporo figures; Asahikawa is much the same): 1 Dec 16:01, 31 Jan 16:45, 28 Feb 17:22", until="2027-03-31")

# 出典。what＝何を確かめたか、saw＝そのページで見た内容、checked＝確かめた日
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("旭川→美瑛 朝 平日", q("旭川", "美瑛", D1, "07:30"), "7:39→8:18、8:44→9:17、9:38→10:12、680円"),
    ("旭川→美瑛 9時台 平日", q("旭川", "美瑛", D1, "09:00"), "JR 9:38→10:12（680円）。道北バス白金線 旭川駅前9番のりば9:40→美瑛駅前10:34（580円）。ふらのバス ラベンダー号 9:55→美瑛駅10:52（1,000円）"),
    ("旭川→美瑛 土曜", q("旭川", "美瑛", D2, "09:00"), "平日と同じ（9:38→10:12、次は10:39→11:13、11:33→12:07）"),
    ("美瑛→旭川 夕方 平日", q("美瑛", "旭川", D1, "16:30"), "17:39→18:19、18:05→18:37、680円"),
    ("美瑛→旭川 夜 平日", q("美瑛", "旭川", D1, "18:30"), "18:40→19:13、19:54→20:27、21:19→21:47"),
    ("美瑛→旭川 最終 平日", q("美瑛", "旭川", D1, "23:59", "l"), "最終は21:19→21:47"),
    ("美瑛→旭川 夜・最終 土曜", q("美瑛", "旭川", D2, "18:30"), "平日と同じ（18:40、19:54、21:19）"),
    ("札幌→旭川 平日", q("札幌", "旭川", D1, "07:30"), "8:00 特急ライラック5号→旭川9:25、5,440円。7:30 特急宗谷→8:58"),
    ("バス 美瑛駅前→白金青い池入口の運賃", q("美瑛駅前/道北バス", "白金青い池入口", D1, "13:30"), "13:45→14:07、14:45→15:07、15:34→15:56、800円"),
    ("バス 美瑛駅前→白金温泉の運賃", q("美瑛駅前/道北バス", "白金温泉", D1, "13:30"), "13:45→14:11、900円"),
    ("バス 白金青い池入口→白金温泉の運賃", q("白金青い池入口", "白金温泉", D1, "15:00"), "15:07→15:11、220円。歩くと38分"),
    ("道北バス 神楽岡・美瑛方面の時刻表（平日）", U["bus_wd"], "2026年10月1日改正。39番 旭川駅前(9)9:40→美瑛駅前10:34→白金青い池10:56→青少年の家・白金温泉11:06。42番 美瑛駅前13:45→14:07→14:17、14:45→15:07→15:17、17:15→17:37→17:47。帰り 16:30→16:35→美瑛駅前17:00、18:00→18:05→18:30が最終。年末年始は特別ダイヤ（12月に公表）"),
    ("道北バス 同じ時刻表（土日祝）", U["bus_hd"], "39番・42番の時刻は平日と同じ"),
    ("道北バス 美瑛・白金線の通過時刻（行き）", U["bus_out"], "全日。美瑛駅前から白金青い池入口まで22分、白金温泉まで26分、終点の青少年の家まで32分"),
    ("道北バス 美瑛・白金線の通過時刻（帰り）", U["bus_back"], "全日。青少年の家16:30→白金温泉16:32→白金青い池入口16:35→道の駅白金16:37→美瑛駅前17:00。18:00→18:02→18:05→18:07→18:30。39番の9:02着・11:27着・13:27着・16:07着は旭川駅前まで行く"),
    ("道北バスの支払い", U["bus_pay"], "タッチ決済の対象路線に「白金線、層雲峡線、空港線等の路線バスの一部」。交通系ICカードの記載はなし"),
    ("美瑛・白金エリア1日フリーパス", U["bus_pass"], "道北バスの公式販売サイト。美瑛駅前〜青い池・白金温泉が当日乗り放題。値段は販売ページで（文字では確かめられなかった）"),
    ("青い池・白ひげの滝・ビルケの森のライトアップ", U["light"], "青い池とビルケの森：2026年10月22日〜2027年4月21日。10・11月17:00、12月16:30、1月17:00、2月17:30、3月18:00、4月18:30から21:00まで。白ひげの滝：通年、日没〜21:00"),
    ("ライトアップ（美瑛町）", U["light_town"], "同じ期間と時間。悪天候のときは中止することがある"),
    ("白金青い池（観光協会）", U["pond"], "冬は雪で青い水面は見えない。12月31日〜1月3日は点灯を翌2時まで延長。晴れた日の13〜15時がいちばん混む。雪どけや大雨のあとは青く見えないことがある。駐車場は有料"),
    ("青い池売店", U["pond_shop"], "4〜11月 9:00〜17:00、12〜3月 11:00〜16:00。休み：12月31日、1月1日、3月1日〜20日の平日"),
    ("道の駅びえい「白金ビルケ」", U["birke"], "6〜8月 9:00〜18:00、3〜5月・9〜11月 9:00〜17:00、12〜2月 10:00〜17:00。12月31日〜1月3日休み"),
    ("冬の定期観光バス（2026-27年）", U["tour"], "美遊バス ライトアップコース：2026年11月20日〜2027年2月13日の金・土曜（1月1・2日運休）、四季の情報館16:35発・18:30着（2月は19:00着）、大人4,000円から。クリスマスツリーライナー：12月1日〜2月28日（12月31日〜1月5日運休）、10:45・13:20・14:50発の約1時間、大人2,000円から。予約は2日前まで、支払いはクレジットカード・Google Pay・PayPay。空きがあれば前日から四季の情報館で当日券"),
    ("ライトアップコースの案内", U["tour_news"], "JRの時刻に合わせて運行。今年は白金温泉に寄らない"),
    ("白ひげの滝", U["falls"], "白金温泉のバス停から歩いて約3分。トイレは白金観光センターの公共トイレ（24時間）"),
    ("白金温泉の日帰り入浴", U["onsen"], "森の雫 RIN 11:00〜21:00・1,200円、碧の美 ゆゆ 11:00〜20:00（受付19:30まで）・1,200円、ホテルパークヒルズ 11:00〜21:00・1,530円、森の旅亭びえい 11:00〜14:00・月曜休み、杖忘れの湯 11:00〜17:00・800円・火水休み。国民保養センターは休館中"),
    ("ホテルパークヒルズ 日帰り", U["park"], "日帰り入浴11:00〜21:00、大人1,530円。お食事・入浴セット1,970円（昼食11:30〜LO13:40）。フェイスタオル220円、バスタオル貸出330円。タトゥーの記載なし"),
    ("国民保養センター", U["hoyou"], "休館を続ける（令和8年度中に今後を決める）"),
    ("道の駅びえい「丘のくら」", U["kura"], "6〜8月 9:00〜18:00、3〜5月・9〜11月 9:00〜17:00、12〜2月 10:00〜17:00。香麦食堂11:00〜14:30(LO)。休み：12月31日・1月1日・1月7日、12月30日は10:00〜12:00"),
    ("ナマステ 美瑛店", U["namaste"], "通し営業 11:00–21:30、L.O. 21:00、定休日なし"),
    ("和牛焼肉・火鍋 GIO（観光協会）", U["gio"], "12:00〜15:30、16:30〜20:00、月曜休み。美瑛駅から歩いて約2分"),
    ("美瑛のめぐり方（観光協会）", U["cruise"], "駅前の貸自転車：松浦商店・寺島商会・スギモト・びえいのガイド・BIEI HILLS。電動自転車は1kmあたり4〜5分。タクシーは美瑛ハイヤー 0166-92-1181（貸切時間制）。町内にレンタカー店はない"),
    ("よくある質問（観光協会）", U["faq"], "12〜3月は最低気温が−15℃を下回る。手荷物は四季の情報館（コインロッカー、大きな荷物1個1,000円）とホテルラヴニール"),
    ("北西の丘展望公園", U["hokusei"], "美瑛駅から2.5km。展望台は雪の時期は閉鎖。案内所は5〜9月。無料"),
    ("ケンとメリーの木", U["kenmary"], "畑に入らない、路肩に長く止まらない。近くにトイレ・駐車場が少ない"),
    ("セブンスターの木", U["seven"], "一帯が「パッチワークの路」。鉄道・バスなし"),
    ("四季彩の丘 ご利用案内", U["shikisai"], "1月8:40〜16:30、2〜4月9:10〜17:00、5・10月8:40〜17:00、6〜9月8:40〜17:30（7〜9月の最終入園17:15）、11〜12月9:10〜16:30。入場料は7〜9月だけ、高校生以上800円（窓口は現金のみ）。レストランLO15時・水曜休み。12月31日・1月1日休み"),
    ("四季彩の丘（観光協会）", U["shikisai_bk"], "美馬牛駅から歩いて30分、美瑛駅から車で12分"),
    ("ファーム富田 営業時間", U["tomita_cafe"], "5月〜6月中旬8:30〜17:00、6月下旬〜8月中旬8:30〜17:30、8月下旬〜9月9:00〜17:00、10〜11月9:30〜16:30、12月〜4月上旬10:00〜16:00。カフェ ルネは11月〜4月中旬クローズ"),
    ("ファーム富田 アクセス", U["tomita_acc"], "中富良野駅から歩いて約25分。ラベンダー畑駅（ノロッコ号の季節だけ）から約7分"),
    ("旭川→中富良野 平日・土曜", q("旭川", "中富良野", D1, "09:00"), "9:38→10:46、1,380円。次は11:33→12:34"),
    ("中富良野→美馬牛 平日・土曜", q("中富良野", "美馬牛", D1, "12:30"), "13:27→13:45、470円。次は15:55→16:14"),
    ("中富良野→美瑛 平日・土曜", q("中富良野", "美瑛", D1, "13:00"), "13:27→13:53、680円"),
    ("旭川→美馬牛 平日", q("旭川", "美馬牛", D1, "09:00"), "9:38→10:22、800円"),
    ("美馬牛→美瑛 平日・土曜", q("美馬牛", "美瑛", D1, "15:30"), "16:18→16:25、320円。次は17:31→17:38、18:32→18:39"),
    ("ふらのバス ラベンダー号", U["lavender"], "2026年4月1日改正。旭川駅9:55→美瑛駅10:52→中富良野11:21→富良野駅前11:38→新富良野プリンスホテル11:55。旭川行きの最終は新富良野プリンスホテル15:55発（旭川駅前17:55）"),
    ("日の入り（国立天文台・札幌）12月", U["sun_dec"], "札幌の日の入り：12月1日16:01（旭川の値は載っていない）"),
    ("日の入り（国立天文台・札幌）1月", U["sun_jan"], "1月31日16:45"),
    ("日の入り（国立天文台・札幌）2月", U["sun_feb"], "2月28日17:22"),
    ("歩く距離（OpenStreetMap の道のデータ）", "https://routing.openstreetmap.de/", "青い池の駐車場の入口→池 約420m、美瑛駅→丘のくら 約260m、美瑛駅→四季の塔 約620m、美瑛駅→北西の丘 3.3km→ケンとメリーの木 1.0km→セブンスターの木 3.9km→美瑛駅 7.4km"),
]]

JR = link("timetable", "JR北海道 運行情報", "JR Hokkaido service status", U["jr_info"])
BUS = link("timetable", "道北バス 時刻表（美瑛・白金）", "Dohoku Bus timetable (Japanese PDF)", U["bus_wd"])
KK = link("official", "美瑛町観光協会", "Biei Tourism Association", f"{BK}/", U["en"])

# ---------------------------------------------------------------------------
# 何か所かに出すお知らせ
# ---------------------------------------------------------------------------
N_COLD = notice(
    "冬の美瑛・白金の寒さ", "How cold it gets",
    "12〜3月は最低気温が−15℃を下回ります（美瑛町観光協会）。青い池では日が沈んでから1時間以上、外にいます。厚い上着、帽子、手袋、首を覆うもの、底に溝の深い冬靴で。スマートフォンは寒さで電池が早く減るので、内側のポケットに。",
    "From December to March the lows drop below −15°C (Biei Tourism Association). At the Blue Pond you will be outdoors for over an hour after dark. Bring a heavy coat, hat, gloves, something for your neck and winter boots with deep tread. Phone batteries drain fast in the cold; keep yours in an inside pocket.",
    U["faq"], start="2026-11-01", to="2027-03-31")
N_LASTBUS = notice(
    "白金からの最終バスは18時", "The last bus from Shirogane leaves at 18:00",
    "美瑛駅行きの最終は、白金温泉18:02発・白金青い池入口18:05発です（美瑛駅前18:30着）。乗り遅れるとタクシーしかありません。雪の日はバスが遅れることがあります。",
    "The last bus to Biei Station leaves Shirogane Onsen at 18:02 and the Blue Pond stop at 18:05 (Biei Station 18:30). Miss it and a taxi is the only way back. Buses can run late in snow.",
    U["bus_back"])
N_NEWYEAR = notice(
    "年末年始はバスが特別ダイヤ", "Special bus timetable over New Year",
    "道北バスは年末年始に特別ダイヤで走ります（内容は12月に公表）。丘のくら・白金ビルケは12月31日〜1月3日ごろ休み、クリスマスツリーライナーは12月31日〜1月5日運休。行く前に道北バスのサイトを見てください。",
    "Dohoku Bus runs a special timetable over New Year (details announced in December). The roadside stations close around 31 December–3 January and the Christmas Tree Liner does not run 31 December–5 January. Check the bus company’s site before you go.",
    U["bus_top"], start="2026-12-10", to="2027-01-06")
N_LINER_OFF_NOV = notice(
    "クリスマスツリーライナーは12月1日から", "The Christmas Tree Liner starts on 1 December",
    "11月は走っていません。クリスマスツリーの木へは美瑛ハイヤーのタクシー（0166-92-1181、料金は要確認）で行くか、外して町で過ごします。",
    "It does not run in November. Take a taxi (Biei Hire, 0166-92-1181; ask the fare) or leave the tree out and spend the time in town.",
    U["tour"], to="2026-11-30")
N_LINER_OFF_SPRING = notice(
    "クリスマスツリーライナーは2月28日まで", "The Christmas Tree Liner ends on 28 February",
    "3月からは走りません。クリスマスツリーの木へは美瑛ハイヤーのタクシー（0166-92-1181、料金は要確認）で行くか、外して町で過ごします。",
    "It stops running in March. Take a taxi (Biei Hire, 0166-92-1181; ask the fare) or leave the tree out and spend the time in town.",
    U["tour"], start="2027-03-01", to="2027-04-20")
N_MARCH_LIGHT = notice(
    "3月・4月はライトアップが18時から", "In March and April the lights come on at 18:00 or later",
    "3月は18:00、4月は18:30に点灯します。最終バス（青い池入口18:05発）では見られません。この時期は温泉をゆっくりにして、白金温泉18:02発の最終バスで帰るのがおすすめです。雪どけのころは池が濁って青く見えないことがあります。",
    "The Blue Pond is lit from 18:00 in March and 18:30 in April, too late for the last bus (18:05 from the pond). At this time of year, take a longer bath and the 18:02 bus from Shirogane Onsen instead. During the thaw the pond can look cloudy rather than blue.",
    U["light"], start="2027-03-01", to="2027-04-20")
N_TO_WINTER = notice(
    "11月からは「冬」のコースへ", "From November, use the winter course",
    "雪が積もると自転車は借りられず、青い池の水面も雪の下になります。11月からは、一覧の上のボタンで「冬」を選んでください（夜のライトアップに合わせた時間割です）。",
    "Once the snow comes there are no rental bikes and the pond disappears under snow. From November, pick “Winter” above the list; that course is timed for the evening light-up.",
    U["light"], start="2026-10-15", to="2026-11-30")
N_JR_2027 = notice(
    "時刻は2026年12月のダイヤです", "Times are from the December 2026 timetable",
    "JR北海道は春にダイヤを改正します。2027年3月よりあとに使うときは、乗換案内で列車の時刻を確かめてください。道北バスの時刻は2026年10月1日改正のものです。",
    "JR Hokkaido revises its timetable every spring. If you use this after March 2027, check the train times in a route planner. Bus times are from the 1 October 2026 timetable.",
    "https://transit.yahoo.co.jp/")
N_GREEN_ONLY = notice(
    "このコースは雪のない季節用です", "This course is for the snow-free months",
    "貸自転車は雪のある時期には使えません（各店の営業期間は要確認）。北西の丘の展望台も雪の時期は閉鎖です。11月〜4月中旬は「冬」のコースを選んでください。",
    "Rental bikes are not available while there is snow (ask each shop for its season), and the Hokusei-no-oka lookout is closed in snow. From November to mid-April, choose the winter course.",
    U["cruise"], start="2026-11-01", to="2027-04-20")
N_FURANO_SEASON = notice(
    "花畑は5月〜10月はじめ", "The flower fields run from May to early October",
    "このコースは花の季節用です。ファーム富田のカフェ ルネは11月〜4月中旬は閉まり、畑は雪の下になります。四季彩の丘は冬は雪遊びの「スノーランド」になります。冬は一覧の上のボタンで「冬」を選んでください。",
    "This course is for the flower season. Farm Tomita’s Café René closes from November to mid-April and the fields lie under snow; Shikisai-no-oka turns into a snow-play park. In winter, pick “Winter” above the list.",
    U["tomita_cafe"], start="2026-10-15", to="2027-04-30")
N_NOROKKO = notice(
    "夏は臨時列車とラベンダー畑駅", "Extra summer trains and Lavender-Batake Station",
    "ラベンダーの季節には、観光列車「富良野・美瑛ノロッコ号」と、ファーム富田まで歩いて約7分の臨時駅「ラベンダー畑」があります。2027年の運転日はまだ発表されていません（JR北海道のサイトで要確認）。",
    "In lavender season the Furano-Biei Norokko sightseeing train runs and stops at the temporary Lavender-Batake Station, about 7 minutes’ walk from Farm Tomita. Dates for 2027 have not been announced; check JR Hokkaido’s site.",
    U["tomita_sta"], start="2027-04-21", to="2027-09-30")
N_MANNER = notice(
    "畑には入らない", "Stay out of the fields",
    "丘の木はどれも農家の畑の中に立っています。雪の日も、道から外に出ないで見ます。路肩に長く止まらないこと、ドローンは原則禁止です。",
    "Every famous tree stands in a working farm field. Even under snow, stay on the road. Don’t linger on the roadside, and drones are banned as a rule.",
    U["manner"])

# ---------------------------------------------------------------------------
# スポットの共通部分
# ---------------------------------------------------------------------------
TIP_JR = T("JRは乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました（2026年11月28日）。春のダイヤ改正のあとは確かめ直してください。",
           "Train times checked in a route planner for 3 December (Thu) and 5 December (Sat) 2026, on 28 November 2026. Re-check after the spring timetable revision.")
TIP_BUS = T("道北バスの公式時刻表（2026年10月1日改正、平日・土日祝とも同じ時刻）と、美瑛町観光協会のページで確認しました（2026年11月28日）。運賃は乗換案内の表示です。",
            "Checked against Dohoku Bus’s official timetable (revised 1 October 2026; same times every day) and the Biei Tourism Association’s pages on 28 November 2026. Fares are as shown in a route planner.")
ROW_BUS_UP = row("bus", "美瑛駅前→白金青い池入口→白金温泉：11:05→11:27→11:31、13:45→14:07→14:11、14:45→15:07→15:11、15:34→15:56→16:00、17:15→17:37→17:41（毎日同じ）",
                 "Biei Station → Blue Pond → Shirogane Onsen: 11:05→11:27→11:31, 13:45→14:07→14:11, 14:45→15:07→15:11, 15:34→15:56→16:00, 17:15→17:37→17:41 (same every day)")
ROW_BUS_DOWN = row("bus", "白金温泉→白金青い池入口→美瑛駅前：13:16→13:19→13:44、14:42→14:45→15:10、15:46→15:49→16:14、16:32→16:35→17:00、最終18:02→18:05→18:30",
                   "Shirogane Onsen → Blue Pond → Biei Station: 13:16→13:19→13:44, 14:42→14:45→15:10, 15:46→15:49→16:14, 16:32→16:35→17:00, last 18:02→18:05→18:30")
ROW_BUS_FEE = row("fee", "バス 美瑛駅前→白金青い池入口800円、美瑛駅前→白金温泉900円、青い池入口→白金温泉220円（現金は整理券を取って降りるときに。タッチ決済のクレジットカードが使える便もあります）",
                  "Bus: Biei Station → Blue Pond ¥800, Biei Station → Shirogane Onsen ¥900, Blue Pond → Shirogane Onsen ¥220 (cash: take a numbered ticket and pay as you get off; some buses take contactless credit cards)")

S = dict(
    asahikawa=dict(
        name=T("旭川駅（JR）", "Asahikawa Station (JR)"), kind=T("駅", "Station"),
        blurb=T("美瑛まではJR富良野線で34分。1時間に1本ほどなので、乗る列車を決めてから出ます。",
                "Biei is 34 minutes away on the JR Furano Line. Trains run about once an hour, so pick yours before you leave the hotel."),
        lat=43.76275, lng=142.35793,
        body=T("旭川（あさひかわ）9:38発の富良野線に乗ると、美瑛（びえい）10:12着。平日も土曜も同じ時刻で、運賃は680円です。乗り遅れると次は10:39発（11:13着）、その次は11:33発です。\n\n"
               "きっぷ：富良野線で交通系ICカード（Kitaca・Suica）が使えるかは、JR北海道のサイトの文字では確かめられませんでした。券売機で行き先までのきっぷを買えば確実です。JR北海道レールパス（全線）で乗れます。札幌から来る人向けに「札幌・富良野エリアパス」もあります（使える範囲と値段はJR北海道の英語ページで確認を）。\n\n"
               "札幌から日帰りで来るなら、札幌8:00発の特急ライラック5号で旭川9:25着、13分の乗り換えで9:38発に間に合います（乗換案内で5,440円）。雪の日は特急が遅れることがあるので、1本早い7:30発（8:58着）だと安心です。\n\n"
               "バスで行く方法：旭川駅前の9番のりばから、道北（どうほく）バス39番「白金線」が美瑛駅前を通って白金青い池入口・白金温泉まで行きます（9:40発→美瑛駅前10:34→青い池入口10:56→白金温泉11:00）。乗り換えなしで青い池まで行きたい日はこちらを。",
               "Take the 9:38 Furano Line train from Asahikawa and you reach Biei at 10:12. Times are the same on weekdays and Saturdays, and the fare is ¥680. Miss it and the next trains leave at 10:39 (Biei 11:13) and 11:33.\n\n"
               "Tickets: JR Hokkaido’s site does not say in plain text whether IC cards (Kitaca, Suica) work on the Furano Line, so buy a paper ticket to your destination from the machine. The JR Hokkaido Rail Pass covers the line. There is also a Sapporo-Furano Area Pass for visitors coming from Sapporo; check its coverage and price on JR Hokkaido’s English page.\n\n"
               "Coming from Sapporo for the day? The 8:00 Lilac 5 limited express reaches Asahikawa at 9:25, leaving 13 minutes to change to the 9:38 (¥5,440 in the route planner). Expresses can run late in snow, so the 7:30 (Asahikawa 8:58) is the safer choice.\n\n"
               "By bus: Dohoku Bus route 39 (Shirogane Line) leaves from stop 9 in front of Asahikawa Station and runs via Biei Station to the Blue Pond and Shirogane Onsen (9:40 → Biei Station 10:34 → Blue Pond 10:56 → Shirogane Onsen 11:00). Use it on days when you want to reach the pond without changing."),
        gmaps=[gm("JR旭川駅", "JR Asahikawa Station", 43.76275, 142.35793, "JR旭川駅")],
        links=[JR, BUS, link("official", "JR北海道のレールパス", "JR Hokkaido rail passes", U["railpass"])],
        rows=[row("train", "旭川9:38→美瑛10:12（平日・土曜とも）。前後は8:44→9:17、10:39→11:13、11:33→12:07", "Asahikawa 9:38 → Biei 10:12, weekdays and Saturdays. Also 8:44→9:17, 10:39→11:13, 11:33→12:07"),
              row("train", "札幌8:00（特急ライラック5号）→旭川9:25", "Sapporo 8:00 (Lilac 5 limited express) → Asahikawa 9:25"),
              row("bus", "道北バス39番 旭川駅前（9番のりば）9:40→美瑛駅前10:34→白金青い池入口10:56→白金温泉11:00。11:00発もあります（青い池入口12:16）", "Dohoku Bus 39: Asahikawa Station (stop 9) 9:40 → Biei Station 10:34 → Blue Pond 10:56 → Shirogane Onsen 11:00. Also at 11:00 (Blue Pond 12:16)"),
              row("fee", "JR 旭川→美瑛680円。道北バス 旭川駅前→美瑛駅前580円", "JR Asahikawa → Biei ¥680. Dohoku Bus Asahikawa Station → Biei Station ¥580")],
        tip=T("JRは乗換案内で2026年12月3日（木）・5日（土）のダイヤを、道北バスは公式時刻表（2026年10月1日改正）を確認しました（2026年11月28日）。",
              "Train times are from a route planner for 3 and 5 December 2026; bus times from Dohoku Bus’s official timetable (revised 1 October 2026). Checked 28 November 2026.")),
    eki=dict(
        name=T("美瑛駅と四季の情報館", "Biei Station and Shiki-no-Johokan"), kind=T("駅・観光案内所", "Station · Tourist information"),
        blurb=T("石造りの駅舎を出て1分の観光案内所。コインロッカーと、観光バスの受付があります。",
                "A stone station building, and a minute away the tourist office with coin lockers and the sightseeing-bus counter."),
        lat=43.591465, lng=142.462849,
        body=T("美瑛駅は美瑛軟石（びえいなんせき）の石造り。駅前のロータリーの中にある「四季の情報館」が観光案内所で、コインロッカーがあり、大きな荷物は1個1,000円で預かってもらえます。定期観光バスの受付もここの1階です。\n\n"
               "白金（しろがね）行きの道北バスの乗り場は「美瑛駅前」。駅のすぐ近くですが、初めてだと分かりにくいので、観光協会の乗り場案内（下のリンク）を見ておくか、案内所で聞いてください。運賃は降りるときに払います。行きと帰りで3回以上乗るなら、道北バスの「美瑛・白金エリア1日フリーパス」（公式の販売サイトでスマートフォンから買う。値段は販売ページで確認を）も選べます。\n\n"
               "タクシーは美瑛ハイヤー（本町1丁目、0166-92-1181）。丘を回るときは時間貸しになります（料金は要確認）。町にレンタカーの店はありません。",
               "Biei Station is built of local Biei soft stone. Shiki-no-Johokan, inside the station forecourt, is the tourist office: it has coin lockers and will keep a large bag for ¥1,000. The counter for the sightseeing buses is on its ground floor.\n\n"
               "Buses to Shirogane leave from the “Biei-ekimae” stop. It is close to the station but not obvious the first time, so look at the tourism association’s stop guide (link below) or ask at the office. You pay when you get off. If you will ride three times or more, Dohoku Bus sells a one-day Biei-Shirogane pass on its official booking site (buy it on your phone; check the price there).\n\n"
               "Taxis: Biei Hire in Honcho 1-chome (0166-92-1181). Touring the hills is charged by the hour (ask the fare). There is no car rental office in town."),
        gmaps=[gm("四季の情報館", "Shiki-no-Johokan", 43.591465, 142.462849, "四季の情報館 美瑛"), gm("JR美瑛駅", "JR Biei Station", 43.59096, 142.461225, "JR美瑛駅")],
        links=[KK, link("info", "道北バスの乗り場案内（PDF）", "Bus stop guide (PDF)", U["bus_stop"]),
               link("official", "美瑛・白金エリア1日フリーパス", "Biei-Shirogane one-day bus pass", U["bus_pass"]),
               link("info", "美瑛のめぐり方（貸自転車・タクシー）", "Getting around Biei (Japanese)", U["cruise"])],
        rows=[row("hours", "観光協会の営業は平日8:30〜17:15と案内されています。土日祝の案内所の時間は要確認", "The tourism association lists weekday hours of 8:30–17:15; weekend hours for the information desk are not confirmed (please check)"),
              row("fee", "手荷物預かり 大きな荷物1個1,000円（コインロッカーもあり）", "Luggage: ¥1,000 per large bag (coin lockers too)")],
        tip=T("美瑛町観光協会のサイト（よくある質問・美瑛のめぐり方・協会について）で確認しました（2026年11月28日）。",
              "Checked on the Biei Tourism Association’s site (FAQ, getting around, about us) on 28 November 2026.")),
    xmas=dict(
        name=T("クリスマスツリーの木", "The Christmas Tree"), kind=T("丘の木", "Tree on the hills"),
        blurb=T("雪の丘に1本だけ立つトウヒ。冬は予約制の小さなバスが駅から往復します。",
                "A single spruce on a snow-covered hill. In winter a small bookable bus runs there and back from the station."),
        lat=43.55437, lng=142.44425, caution=T("ライナーは予約制（2日前まで）", "The Liner must be booked 2 days ahead"),
        body=T("広い丘の畑に1本だけ立つトウヒの木で、形がクリスマスツリーに見えることからこの名前で呼ばれています。近くに路線バスも駅もありません。\n\n"
               "冬は美瑛町観光協会の「クリスマスツリーライナー」が四季の情報館から往復します（2026年12月1日〜2027年2月28日。12月31日〜1月5日は運休）。10:45・13:20・14:50発の1日3便、約1時間で、木のそばに20分ほど止まります。大人2,000円から（日によって変わります）。予約は観光協会のサイトで2日前まで、支払いはクレジットカード・Google Pay・PayPay。席が残っていれば、前日から四季の情報館で当日券が買えます。出発の10分前までに、情報館1階のカウンターでQRコードを見せて受付を。\n\n"
               "木は農家の畑の中にあります。雪で境目が見えなくても、道から畑へは入りません。バスを降りる場所から歩いて3分ほど、まわりにトイレはありません。",
               "A lone spruce in a wide hillside field, named for its shape. No train or regular bus goes near it.\n\n"
               "In winter the Biei Tourism Association runs the Christmas Tree Liner from Shiki-no-Johokan (1 December 2026–28 February 2027; not 31 December–5 January). Three runs a day at 10:45, 13:20 and 14:50, each about an hour with roughly 20 minutes at the tree. From ¥2,000 per adult (the price varies by day). Book on the association’s site up to two days ahead and pay by credit card, Google Pay or PayPay; if seats remain, same-day tickets are sold at Shiki-no-Johokan from the day before. Check in with your QR code at the ground-floor counter at least 10 minutes before departure.\n\n"
               "The tree stands in a farmer’s field. Even when snow hides the edge, do not step off the road. It is about 3 minutes’ walk from where the bus stops, and there are no toilets nearby."),
        gmaps=[gm("クリスマスツリーの木", "The Christmas Tree", 43.55437, 142.44425, "クリスマスツリーの木 美瑛")],
        links=[link("official", "冬の定期観光バス（予約）", "Winter sightseeing buses (booking)", U["tour"]), link("info", "観光客の皆様へのおねがい", "Visitor manners (Japanese)", U["manner"])],
        rows=[row("bus", "クリスマスツリーライナー 四季の情報館10:45発→11:45着（ほかに13:20発、14:50発）。2027年2月28日まで、12月31日〜1月5日は運休", "Christmas Tree Liner: Shiki-no-Johokan 10:45 → back 11:45 (also 13:20 and 14:50). Until 28 February 2027; no service 31 December–5 January", until="2027-02-28"),
              row("fee", "大人2,000円から、子供（4〜11歳）1,000円から。予約は2日前まで", "Adults from ¥2,000, children (4–11) from ¥1,000. Book up to 2 days ahead", until="2027-02-28")],
        tip=T("美瑛町観光協会の「2026-27年 冬 定期観光バスのご案内」で確認しました（2026年11月28日）。次の冬の運行は未発表です。",
              "Checked on the Biei Tourism Association’s 2026–27 winter sightseeing bus page on 28 November 2026. Next winter’s service has not been announced.")),
    hokusei=dict(
        name=T("北西の丘展望公園", "Hokusei-no-oka Observation Park"), kind=T("展望台", "Lookout"),
        blurb=T("ピラミッド形の展望台から、丘の畑と大雪山・十勝岳の山並み。トイレと夏の案内所があります。",
                "A pyramid-shaped lookout over the patchwork fields to the Daisetsu and Tokachi ranges. Toilets, and an information desk in summer."),
        lat=43.604939, lng=142.457984,
        body=T("駅から3kmほど、坂を上った丘の上の公園です。三角の展望台に上がると、畑の向こうに大雪山（たいせつざん）と十勝岳（とかちだけ）の山並みが見えます。夏は公園のラベンダーも咲きます。\n\n"
               "丘めぐりは坂ばかりなので、自転車は電動のものを。貸自転車の店は駅前に数軒あります（観光協会の「美瑛のめぐり方」に一覧。料金と営業する期間は店ごとに違うので要確認）。観光協会の目安では、電動自転車で1kmあたり4〜5分です。\n\n"
               "トイレはここで済ませておきます。この先のケンとメリーの木・セブンスターの木のまわりには、トイレがほとんどありません。入場は無料。5〜9月は公園の中の観光案内所が開いています。",
               "A park on a hilltop about 3 km uphill from the station. From the triangular lookout you see across the fields to the Daisetsu and Tokachi mountains. The park’s own lavender flowers in summer.\n\n"
               "The hills are all slopes, so rent an electric bike. Several shops near the station rent them (listed on the tourism association’s “getting around” page; prices and seasons differ by shop, so ask). The association’s rule of thumb is 4–5 minutes per kilometre on an e-bike.\n\n"
               "Use the toilets here: there are almost none around the Ken & Mary Tree and the Seven Stars Tree. Entry is free, and an information desk in the park is open from May to September."),
        gmaps=[gm("北西の丘展望公園", "Hokusei-no-oka Observation Park", 43.604939, 142.457984, "北西の丘展望公園")],
        links=[link("official", "北西の丘展望公園（観光協会）", "Hokusei-no-oka (Japanese)", U["hokusei"]), link("info", "美瑛のめぐり方（貸自転車の一覧）", "Getting around Biei: bike rental list (Japanese)", U["cruise"])],
        rows=[row("fee", "無料。展望台は雪の時期は閉鎖、案内所は5〜9月", "Free. The lookout closes when there is snow; information desk May–September"),
              row("hours", "美瑛駅から約3.3km（電動自転車で15分ほど）", "About 3.3 km from Biei Station (some 15 minutes by e-bike)")],
        tip=T("美瑛町観光協会のページで確認しました（2026年11月28日）。距離は OpenStreetMap の道のデータから。",
              "Checked on the Biei Tourism Association’s pages on 28 November 2026. Distances are from OpenStreetMap road data.")),
    kenmary=dict(
        name=T("ケンとメリーの木", "Ken & Mary Tree"), kind=T("丘の木", "Tree on the hills"),
        blurb=T("1972年の車のCMで知られた大きな木。北西の丘から自転車で5分ほどです。",
                "A tall tree made famous by a 1972 car commercial, about 5 minutes by bike from Hokusei-no-oka."),
        lat=43.609151, lng=142.464277,
        body=T("1972年に日産スカイラインのCMに出た、丘の上の木です。名前はCMの登場人物「ケンとメリー」から。\n\n"
               "木は畑の中に立っています。写真は道から撮り、畑には入りません。観光バスや車が集まる場所なので、自転車は道の端に寄せて止め、道の真ん中で立ち止まらないようにします。農作業の大きな車が通るときは先に通してください。",
               "The tree on the hill appeared in a 1972 Nissan Skyline commercial; its name comes from the characters, Ken and Mary.\n\n"
               "It stands in a field, so take your photos from the road and stay out of the crops. Tour buses and cars gather here: park your bike well to the side and don’t stop in the middle of the road. Let farm vehicles through first."),
        gmaps=[gm("ケンとメリーの木", "Ken & Mary Tree", 43.609151, 142.464277, "ケンとメリーの木")],
        links=[link("official", "ケンとメリーの木（観光協会）", "Ken & Mary Tree (Japanese)", U["kenmary"]), link("info", "観光客の皆様へのおねがい", "Visitor manners (Japanese)", U["manner"])],
        rows=[row("fee", "無料", "Free"), row("hours", "北西の丘から約1km", "About 1 km from Hokusei-no-oka")],
        tip=T("美瑛町観光協会のページで確認しました（2026年11月28日）。", "Checked on the Biei Tourism Association’s page on 28 November 2026.")),
    seven=dict(
        name=T("セブンスターの木", "Seven Stars Tree"), kind=T("丘の木", "Tree on the hills"),
        blurb=T("パッチワークの路の奥、高台に立つ1本の木。畑の色が区画ごとに違って見える場所です。",
                "A lone tree on high ground along Patchwork Road, where each field shows a different colour."),
        lat=43.629089, lng=142.431177,
        body=T("1976年にたばこ「セブンスター」のCMに使われた木です。少し高い場所にあり、区画ごとに違う作物が植えられた畑が、布のパッチワークのように見えます。初夏の花から、麦の穂が色づく真夏までがいちばんきれいな時期です（観光協会）。\n\n"
               "ケンとメリーの木から約4km、電動自転車で20分ほど。ここから駅までは約7.5km、30〜35分です。風をさえぎるものがないので、帽子と飲み物を。時間が足りない日は、ここを外して北西の丘とケンとメリーの木だけにすると、1時間ほどで駅に戻れます。",
               "This tree was used in advertising for Seven Stars cigarettes in 1976. From its slightly higher ground, fields planted with different crops look like a patchwork quilt. The tourism association says the best time runs from the early-summer flowers to midsummer, when the wheat turns gold.\n\n"
               "It is about 4 km from the Ken & Mary Tree, some 20 minutes by e-bike, and about 7.5 km (30–35 minutes) back to the station. There is no shade or shelter, so bring a hat and a drink. Short of time? Leave this one out; Hokusei-no-oka and the Ken & Mary Tree alone make a loop of about an hour."),
        gmaps=[gm("セブンスターの木", "Seven Stars Tree", 43.629089, 142.431177, "セブンスターの木")],
        links=[link("official", "セブンスターの木（観光協会）", "Seven Stars Tree (Japanese)", U["seven"]), link("info", "観光客の皆様へのおねがい", "Visitor manners (Japanese)", U["manner"])],
        rows=[row("fee", "無料", "Free"), row("hours", "ケンとメリーの木から約3.9km、美瑛駅まで約7.4km", "About 3.9 km from the Ken & Mary Tree; about 7.4 km back to Biei Station")],
        tip=T("美瑛町観光協会のページで確認しました（2026年11月28日）。距離は OpenStreetMap の道のデータから。",
              "Checked on the Biei Tourism Association’s page on 28 November 2026. Distances are from OpenStreetMap road data.")),
    machi=dict(
        name=T("道の駅びえい「丘のくら」でお昼", "Lunch at Okanokura roadside station"), kind=T("お昼・みやげ", "Lunch · Shop"),
        blurb=T("駅から歩いて3分、大正時代の石の倉庫を使った道の駅。食堂は14:30ラストオーダーです。",
                "Three minutes from the station, a roadside station in a stone warehouse from the 1910s. The canteen takes last orders at 14:30."),
        lat=43.59228, lng=142.46397,
        body=T("1917年に建った美瑛軟石の豆の倉庫を、道の駅にした建物です。中の「香麦（こうばく）食堂」が11:00から14:30ラストオーダー。売店には美瑛だけのみやげが並びます。\n\n"
               "ほかに駅の近くで昼に開いている店は、インド・ネパールカレーの「ナマステ 美瑛店」（歩いて5分、11:00〜21:30の通し営業）、「和牛焼肉・火鍋 GIO」（歩いて2分、12:00〜15:30、月曜休み）。観光協会の「飲食」のページに一覧があります。\n\n"
               "時間が余ったら、役場の横の「四季の塔」へ（駅から歩いて8分）。高さ32.4mの塔で、いちばん上から美瑛の町と丘を見渡せます。開いている時間は公式のページに書かれていないので、役場（0166-92-1111）か案内所で確かめてください。",
               "A 1917 bean warehouse of Biei soft stone, now a roadside station. Its canteen, Kobaku Shokudo, is open from 11:00 with last orders at 14:30. The shop stocks Biei-only souvenirs.\n\n"
               "Other places near the station open at lunchtime: Namaste Biei for Indian and Nepalese curry (5 minutes’ walk, open straight through 11:00–21:30) and GIO for wagyu barbecue and hotpot (2 minutes, 12:00–15:30, closed Mondays). The tourism association’s “eat” page lists more.\n\n"
               "With time to spare, walk 8 minutes to Shiki-no-To, the 32.4-metre tower beside the town hall, for a view over the town and the hills from the top. Its opening hours are not on the official page, so ask the town hall (0166-92-1111) or the tourist office."),
        gmaps=[gm("道の駅びえい「丘のくら」", "Okanokura roadside station", 43.59228, 142.46397, "道の駅びえい 丘のくら"), gm("四季の塔", "Shiki-no-To tower", 43.58821, 142.46694, "四季の塔 美瑛町役場")],
        links=[link("official", "丘のくら（観光協会）", "Okanokura (Japanese)", U["kura"]), link("official", "ナマステ 美瑛店", "Namaste Biei", U["namaste"]), link("info", "美瑛の飲食店（観光協会）", "Places to eat in Biei (Japanese)", U["meal"])],
        rows=[row("hours", "丘のくら 6〜8月9:00〜18:00、3〜5月・9〜11月9:00〜17:00、12〜2月10:00〜17:00。香麦食堂11:00〜14:30（ラストオーダー）", "Okanokura: Jun–Aug 9:00–18:00, Mar–May and Sep–Nov 9:00–17:00, Dec–Feb 10:00–17:00. Kobaku Shokudo 11:00–14:30 (last orders)"),
              row("closed", "12月31日・1月1日・1月7日。12月30日は10:00〜12:00", "31 December, 1 January, 7 January. 30 December 10:00–12:00 only"),
              row("hours", "四季の塔の開いている時間は要確認", "Shiki-no-To tower hours: not confirmed (please check)")],
        tip=T("美瑛町観光協会の施設のページとナマステの公式サイトで確認しました（2026年11月28日）。四季の塔の時間は公式で確かめられませんでした。",
              "Checked on the Biei Tourism Association’s facility pages and Namaste’s official site on 28 November 2026. The tower’s hours could not be confirmed.")),
    pond=dict(
        name=T("白金 青い池", "Shirogane Blue Pond"), kind=T("池", "Pond"),
        blurb=T("立ち枯れのカラマツが並ぶ青い池。冬は雪の下になり、夜のライトアップで見ます。",
                "A blue pond studded with dead larch trunks. In winter it lies under snow and is seen by its evening light-up."),
        lat=43.49349, lng=142.614097,
        body=T("十勝岳の防災工事でできた堰（せき）に水がたまった池です。白ひげの滝の下を流れる美瑛川に、アルミニウムなどを含む沢の水が混ざり、光が散らばって青く見えるとされています。雪どけの春や大雨のあとは、濁って青く見えないことがあります。\n\n"
               "バス停「白金青い池入口」から池までは、駐車場の横を通って歩いて6分ほど。池のふちの道を歩いて見ます（池や、決められた場所の外には入れません）。駐車場のそばの売店は4〜11月が9:00〜17:00、12〜3月が11:00〜16:00です。\n\n"
               "雪のない季節は、晴れた日の13〜15時がいちばん混みます（観光協会）。\n\n"
               "冬（11月ごろ〜4月）は池が凍って雪に覆われ、青い水面は見えません。そのかわり、2026年10月22日〜2027年4月21日は毎晩ライトアップがあり、約15分でひと回りする光の演出で、雪の池と枯れ木が浮かび上がります。点灯は10・11月が17:00、12月が16:30、1月が17:00、2月が17:30、3月が18:00、4月が18:30から、21:00まで。荒れた天気の日は中止になることがあります。\n\n"
               "夜は売店が閉まっていて、暖まれる建物がありません。美瑛駅へ戻るバスは16:35の次が最終の18:05です。金・土曜（2026年11月20日〜2027年2月13日、1月1・2日は運休）は、観光協会の「美遊バス ライトアップコース」が美瑛駅前の四季の情報館を16:35に出て、ビルケの森と青い池のライトアップを回り、18:30（2月は19:00）に戻ります。大人4,000円から、予約は2日前まで。外で待つ時間が短いので、金・土曜に行く人にはこちらが楽です。",
               "The pond formed where water collected behind a barrier built to protect against mudflows from Mt. Tokachi. Water from streams carrying aluminium mixes into the Biei River below Shirahige Falls, scattering light so the water looks blue. In the spring thaw or after heavy rain it can turn cloudy.\n\n"
               "From the “Shirogane Aoi-ike Iriguchi” bus stop it is about 6 minutes on foot, past the car park. You view the pond from the path along its edge; stay on the marked route. The shop by the car park opens 9:00–17:00 from April to November and 11:00–16:00 from December to March.\n\n"
               "In the snow-free months, the busiest time is 13:00–15:00 on sunny days (tourism association).\n\n"
               "In winter (roughly November to April) the pond freezes and is covered in snow, so you cannot see blue water. Instead it is lit every evening from 22 October 2026 to 21 April 2027, with a roughly 15-minute light sequence picking out the snow and the dead trees. Lights come on at 17:00 in October and November, 16:30 in December, 17:00 in January, 17:30 in February, 18:00 in March and 18:30 in April, until 21:00. The light-up can be cancelled in bad weather.\n\n"
               "In the evening the shop is shut and there is nowhere to warm up. After the 16:35 bus, the only bus back to Biei Station is the last one at 18:05. On Fridays and Saturdays (20 November 2026–13 February 2027, not 1–2 January) the tourism association’s Biyu Bus light-up tour leaves Shiki-no-Johokan by Biei Station at 16:35, visits the lit-up birch forest and the pond, and returns at 18:30 (19:00 in February). From ¥4,000 per adult; book up to two days ahead. It means far less waiting outdoors, so take it if you are here on those days."),
        gmaps=[gm("白金 青い池", "Shirogane Blue Pond", 43.49349, 142.614097, "白金青い池")],
        links=[link("official", "白金青い池（観光協会）", "Blue Pond (Japanese)", U["pond"]), link("official", "ライトアップの期間と時間", "Light-up dates and times (Japanese)", U["light"]),
               link("official", "美遊バス ライトアップコース（予約）", "Biyu Bus light-up tour (booking)", U["tour"]), BUS],
        rows=[row("hours", "ライトアップ 2027年4月21日まで毎晩：10・11月17:00〜、12月16:30〜、1月17:00〜、2月17:30〜、3月18:00〜、4月18:30〜、21:00まで", "Light-up nightly until 21 April 2027: from 17:00 in Oct–Nov, 16:30 in Dec, 17:00 in Jan, 17:30 in Feb, 18:00 in Mar, 18:30 in Apr, until 21:00", until="2027-04-21"),
              row("hours", "売店 4〜11月9:00〜17:00、12〜3月11:00〜16:00（12月31日・1月1日、3月1〜20日の平日は休み）", "Shop: Apr–Nov 9:00–17:00, Dec–Mar 11:00–16:00 (closed 31 Dec, 1 Jan and weekdays 1–20 Mar)"),
              ROW_BUS_UP, ROW_BUS_DOWN, ROW_BUS_FEE,
              row("fee", "池の見学は無料とは公式に書かれていませんが、料金の案内があるのは駐車場だけです（歩いて入る人の料金は要確認）", "The official page lists a charge only for the car park; whether visitors on foot pay anything is not stated (please check)")],
        tip=TIP_BUS),
    falls=dict(
        name=T("白ひげの滝とブルーリバー橋", "Shirahige Falls and the Blue River bridge"), kind=T("滝", "Waterfall"),
        blurb=T("岩の間からしみ出た地下水が、青い美瑛川へ落ちる滝。橋の上から見下ろします。冬はまわりの木に霧氷がつきます。",
                "Groundwater seeps out of the rock and drops into the blue Biei River. You look down on it from a bridge; in winter the trees around it are white with frost."),
        lat=43.474582, lng=142.639187,
        body=T("落差は約30m。岩のすき間から出た地下水が、白いひげのように何本も落ちています。下を流れる美瑛川が青い池と同じ色をしていて、橋（通称ブルーリバー橋）の上から、滝と青い川をいっしょに見られます。\n\n"
               "バス停「白金温泉」から歩いて3分ほど。冬は滝のしぶきと湯気で、まわりの木に霧氷がつきます。橋の上は風が通って冷えるので、長くいるなら手袋を。一年を通して、日が沈んでから21:00までライトアップされます。\n\n"
               "トイレは、白金観光センターの中の公共トイレ（24時間）が使えます。見るのは無料です。",
               "About 30 metres high. Groundwater emerges from cracks in the rock and falls in many strands like a white beard. The Biei River below is the same colour as the Blue Pond, and from the bridge (known as the Blue River bridge) you see falls and river together.\n\n"
               "It is about 3 minutes’ walk from the “Shirogane Onsen” bus stop. In winter the spray and steam coat the nearby trees in frost. The bridge is exposed to the wind, so wear gloves if you linger. The falls are lit from sunset to 21:00 all year.\n\n"
               "There are public toilets, open 24 hours, in the Shirogane Tourist Centre. Viewing is free."),
        gmaps=[gm("白ひげの滝", "Shirahige Falls", 43.474582, 142.639187, "白ひげの滝 美瑛")],
        links=[link("official", "白ひげの滝（観光協会）", "Shirahige Falls (Japanese)", U["falls"]), link("official", "ライトアップの期間と時間", "Light-up times (Japanese)", U["light"]), BUS],
        rows=[row("hours", "ライトアップ 通年、日没〜21:00", "Lit all year from sunset to 21:00"), row("fee", "無料", "Free"), ROW_BUS_UP, ROW_BUS_DOWN],
        tip=TIP_BUS),
    onsen=dict(
        name=T("白金温泉の日帰り入浴", "A day bath at Shirogane Onsen"), kind=T("温泉", "Hot spring"),
        blurb=T("十勝岳のふもとの温泉街。滝から歩いてすぐのホテル3軒が、夜まで日帰り入浴を受けています。",
                "A hot-spring village at the foot of Mt. Tokachi. Three hotels a short walk from the falls take day bathers into the evening."),
        lat=43.47435, lng=142.63745, caution=T("タトゥーの決まりは公式に記載なし（要確認）", "Tattoo rules not stated officially (please check)"),
        body=T("1950年に掘り当てられた温泉で、白金（しろがね）の名前は「地底から湧いたプラチナのように尊い湯」という言葉から。バス停と白ひげの滝のまわりに宿が集まっています。\n\n"
               "日帰り入浴ができて、午後から夜まで開いているのは次の3軒です（どれも露天風呂とサウナ、シャンプー・ボディソープあり）。\n"
               "・森の雫 RIN（旧 大雪山白金観光ホテル）：11:00〜21:00、大人1,200円。フェイスタオル220円（販売）、バスタオル100円（貸出）\n"
               "・碧の美 ゆゆ（旧 湯元白金温泉ホテル）：11:00〜20:00（受付は19:30まで）、大人1,200円。タオルのセット330円（貸出）\n"
               "・ホテルパークヒルズ：11:00〜21:00、大人1,530円。フェイスタオル220円（販売）、バスタオル330円（貸出）。お昼と入浴のセット1,970円（昼食は11:30〜13:40ラストオーダー）\n\n"
               "タトゥー：3軒とも、公式サイトにも観光協会のページにも決まりが書かれていません（要確認）。タトゥーのある人は、行く前に電話かフロントで確かめてください（RIN 0166-94-3111、ゆゆ 0166-94-3333、パークヒルズ 0166-94-3041）。貸切風呂の案内も公式では確かめられませんでした。\n\n"
               "入り方：服は脱衣所で全部脱ぎ、湯船に入る前に洗い場で体を洗います。タオルは湯に入れません。貸切などで日帰り入浴を休む日があるので、その日の朝に宿のサイトのお知らせを見ておくと確実です。町の日帰り温泉「国民保養センター」は休館が続いています。",
               "The spring was struck in 1950; the name Shirogane (“platinum”) comes from the remark that the water was as precious as platinum from the earth. The inns cluster around the bus stop and Shirahige Falls.\n\n"
               "Three hotels take day bathers from late morning into the evening (all have outdoor baths, saunas, shampoo and body soap):\n"
               "· Mori-no-Shizuku RIN (formerly Taisetsuzan Shirogane Kanko Hotel): 11:00–21:00, adults ¥1,200. Face towel ¥220 (to buy), bath towel ¥100 (to rent)\n"
               "· Ao-no-Bi Yuyu (formerly Yumoto Shirogane Onsen Hotel): 11:00–20:00 (last entry 19:30), adults ¥1,200. Towel set ¥330 (rental)\n"
               "· Hotel Park Hills: 11:00–21:00, adults ¥1,530. Face towel ¥220 (to buy), bath towel ¥330 (to rent). Lunch-and-bath set ¥1,970 (lunch 11:30, last orders 13:40)\n\n"
               "Tattoos: none of the three states a rule, either on its own site or on the tourism association’s page (please check). If you have tattoos, phone ahead or ask at the front desk (RIN 0166-94-3111, Yuyu 0166-94-3333, Park Hills 0166-94-3041). No private-bath option could be confirmed officially.\n\n"
               "How to bathe: undress completely in the changing room and wash at the showers before getting into the bath; keep your towel out of the water. Day bathing is sometimes suspended for private events, so check the hotel’s news page that morning. The town’s public bathhouse, Kokumin Hoyo Center, remains closed."),
        gmaps=[gm("ホテルパークヒルズ", "Hotel Park Hills", 43.475115, 142.637168, "美瑛白金温泉 ホテルパークヒルズ"),
               gm("森の雫 RIN", "Mori-no-Shizuku RIN", 43.4738, 142.6385, "森の雫 RIN 白金温泉"), gm("碧の美 ゆゆ", "Ao-no-Bi Yuyu", 43.4738, 142.6385, "碧の美 ゆゆ 白金温泉")],
        links=[link("official", "白金温泉の日帰り入浴（観光協会）", "Day bathing at Shirogane Onsen (Japanese)", U["onsen"]), link("official", "ホテルパークヒルズ 日帰り", "Hotel Park Hills day use (Japanese)", U["park"]),
               link("official", "森の雫 RIN", "Mori-no-Shizuku RIN (Japanese)", U["rin"]), link("official", "碧の美 ゆゆ", "Ao-no-Bi Yuyu (Japanese)", U["yuyu"])],
        rows=[row("hours", "森の雫 RIN 11:00〜21:00／碧の美 ゆゆ 11:00〜20:00（受付19:30まで）／ホテルパークヒルズ 11:00〜21:00", "RIN 11:00–21:00 / Yuyu 11:00–20:00 (last entry 19:30) / Park Hills 11:00–21:00"),
              row("fee", "RIN・ゆゆ 大人1,200円、パークヒルズ 大人1,530円。支払い方法は要確認（現金を用意）", "RIN and Yuyu ¥1,200, Park Hills ¥1,530 per adult. Payment methods not confirmed; bring cash"),
              ROW_BUS_DOWN],
        tip=T("美瑛町観光協会の「温泉」のページとホテルパークヒルズの公式サイトで確認しました（2026年11月28日）。タトゥーの決まりはどの公式ページにも見つかりませんでした。",
              "Checked on the Biei Tourism Association’s hot-spring page and Hotel Park Hills’ official site on 28 November 2026. No official page states a tattoo policy.")),
    kaeri=dict(
        name=T("美瑛駅：晩ごはんと帰りの電車", "Biei Station: dinner and the train back"), kind=T("晩ごはん・駅", "Dinner · Station"),
        blurb=T("旭川行きは18:40、19:54、最終21:19。駅の近くで食べてから帰れます。",
                "Trains to Asahikawa leave at 18:40, 19:54 and, last, 21:19, leaving time to eat near the station first."),
        lat=43.59096, lng=142.461225,
        body=T("美瑛から旭川への電車は、夕方からは17:39、18:05、18:40、19:54、最終が21:19発です（平日・土曜とも。旭川まで30〜40分、680円）。\n\n"
               "駅の近くで夜に開いている店：インド・ネパールカレーの「ナマステ 美瑛店」（歩いて5分、11:00〜21:30、ラストオーダー21:00、定休日なし）、「和牛焼肉・火鍋 GIO」（歩いて2分、16:30〜20:00、月曜休み）。夜の時間を公式に確かめられた店は多くないので、遅くなる日は旭川に戻ってから食べるほうが店を選べます。\n\n"
               "札幌へ帰る人は、旭川からの特急の時刻を先に乗換案内で確かめておいてください。",
               "Evening trains from Biei to Asahikawa leave at 17:39, 18:05, 18:40, 19:54 and, last, 21:19 (weekdays and Saturdays; 30–40 minutes, ¥680).\n\n"
               "Open in the evening near the station: Namaste Biei for Indian and Nepalese curry (5 minutes’ walk, 11:00–21:30, last orders 21:00, no closing day) and GIO for wagyu barbecue and hotpot (2 minutes, 16:30–20:00, closed Mondays). Few other places could be confirmed as open in the evening, so on a late day you will have more choice back in Asahikawa.\n\n"
               "Heading back to Sapporo? Check the limited-express times from Asahikawa in a route planner beforehand."),
        gmaps=[gm("JR美瑛駅", "JR Biei Station", 43.59096, 142.461225, "JR美瑛駅")],
        links=[JR, link("official", "ナマステ 美瑛店", "Namaste Biei", U["namaste"]), link("info", "和牛焼肉・火鍋 GIO（観光協会）", "GIO (Japanese)", U["gio"])],
        rows=[row("train", "美瑛→旭川 17:39→18:19、18:05→18:37、18:40→19:13、19:54→20:27、最終21:19→21:47（平日・土曜とも）", "Biei → Asahikawa 17:39→18:19, 18:05→18:37, 18:40→19:13, 19:54→20:27, last 21:19→21:47 (weekdays and Saturdays)"),
              row("fee", "JR 美瑛→旭川680円", "JR Biei → Asahikawa ¥680")],
        tip=T("JRは乗換案内で2026年12月3日（木）・5日（土）のダイヤを、店の時間はナマステの公式サイトと美瑛町観光協会のページで確認しました（2026年11月28日）。",
              "Train times are from a route planner for 3 and 5 December 2026; shop hours from Namaste’s official site and the Biei Tourism Association, checked 28 November 2026.")),
    tomita=dict(
        name=T("ファーム富田（中富良野）", "Farm Tomita (Nakafurano)"), kind=T("花畑", "Flower farm"),
        blurb=T("富良野のラベンダーを広めた農園。斜面いっぱいの花畑と、ラベンダーの製品の店やカフェがあります。",
                "The farm that made Furano’s lavender famous: hillside flower fields, lavender shops and cafés."),
        lat=43.417298, lng=142.425476,
        body=T("中富良野（なかふらの）駅から歩いて約25分。斜面に花畑が広がり、花の時期が違う畑がいくつもあります。ラベンダーの見ごろは年によって違うので、行く前に公式サイトの花の情報を見てください。\n\n"
               "園内にはカフェや軽食の店があり、ガラス張りの「カフェ ルネ」ではカレーなどの軽食が食べられます（5月〜6月上旬9:30〜16:30、6月中旬〜8月9:00〜16:30、9月9:30〜16:30、10月10:00〜16:30。11月〜4月中旬は休み）。園の営業時間は5月〜6月中旬が8:30〜17:00、6月下旬〜8月中旬が8:30〜17:30、8月下旬〜9月が9:00〜17:00、10〜11月が9:30〜16:30。営業時間の外は入れません。\n\n"
               "ラベンダーの季節には、園から歩いて約7分の臨時の駅「ラベンダー畑」に観光列車のノロッコ号が止まります。その時期は道も駅も混みます。入園料は公式サイトで確かめられませんでした（要確認）。",
               "About 25 minutes on foot from Nakafurano Station. The flower fields spread over a slope, with several fields that bloom at different times. Peak lavender varies by year, so check the flower updates on the official site before you go.\n\n"
               "There are cafés and snack stands on site; the glass-walled Café René serves curry and other light meals (9:30–16:30 from May to early June, 9:00–16:30 from mid-June to August, 9:30–16:30 in September, 10:00–16:30 in October; closed November to mid-April). The farm opens 8:30–17:00 from May to mid-June, 8:30–17:30 from late June to mid-August, 9:00–17:00 from late August to September and 9:30–16:30 in October and November. You cannot enter outside opening hours.\n\n"
               "In lavender season the Norokko sightseeing train stops at the temporary Lavender-Batake Station, about 7 minutes’ walk away; roads and stations get crowded then. The admission charge, if any, could not be confirmed on the official site (please check)."),
        gmaps=[gm("ファーム富田", "Farm Tomita", 43.417298, 142.425476, "ファーム富田"), gm("JR中富良野駅", "JR Nakafurano Station", 43.40585, 142.421038, "JR中富良野駅")],
        links=[link("official", "ファーム富田", "Farm Tomita", U["tomita"], U["tomita_en"]), link("official", "カフェと営業時間", "Cafés and hours (Japanese)", U["tomita_cafe"]), link("info", "ラベンダー畑駅", "Lavender-Batake Station (Japanese)", U["tomita_sta"]), JR],
        rows=[row("train", "旭川9:38→中富良野10:46（美瑛10:12を通ります）", "Asahikawa 9:38 → Nakafurano 10:46 (via Biei at 10:12)"),
              row("train", "中富良野13:27→美馬牛13:45。次は15:55発", "Nakafurano 13:27 → Bibaushi 13:45. The next is at 15:55"),
              row("hours", "5月〜6月中旬8:30〜17:00、6月下旬〜8月中旬8:30〜17:30、8月下旬〜9月9:00〜17:00、10〜11月9:30〜16:30", "May–mid-Jun 8:30–17:00, late Jun–mid-Aug 8:30–17:30, late Aug–Sep 9:00–17:00, Oct–Nov 9:30–16:30"),
              row("fee", "JR 旭川→中富良野1,380円、中富良野→美馬牛470円。入園料は要確認", "JR Asahikawa → Nakafurano ¥1,380, Nakafurano → Bibaushi ¥470. Admission: please check")],
        tip=T("ファーム富田の公式サイト（カフェ・アクセスのページ）と乗換案内（2026年12月3日・5日のダイヤ）で確認しました（2026年11月28日）。",
              "Checked on Farm Tomita’s official site (café and access pages) and in a route planner for 3 and 5 December 2026, on 28 November 2026.")),
    bibaushi=dict(
        name=T("美馬牛駅", "Bibaushi Station"), kind=T("駅", "Station"),
        blurb=T("赤い屋根の小さな駅。四季彩の丘へはここから歩いて30分です。",
                "A small station with a red roof. Shikisai-no-oka is a 30-minute walk from here."),
        lat=43.537649, lng=142.447376,
        body=T("美馬牛（びばうし）は美瑛のひとつ富良野寄りの駅です。四季彩の丘までは歩いて30分ほど（観光協会の案内）。飲み物は先に用意しておくと安心です。\n\n"
               "駅の近くに貸自転車の店「ガイドの山小屋」があります（観光協会の一覧。料金と営業日は要確認）。電車は1時間に1本ほどなので、帰りに乗る電車を決めてから歩き始めてください。",
               "Bibaushi is the next station after Biei towards Furano. Shikisai-no-oka is about 30 minutes on foot (tourism association’s figure). Bring a drink with you.\n\n"
               "A bike rental shop, Guide no Yamagoya, is near the station (on the tourism association’s list; check prices and opening days). Trains come about once an hour, so decide which one you are taking back before you set off."),
        gmaps=[gm("JR美馬牛駅", "JR Bibaushi Station", 43.537649, 142.447376, "JR美馬牛駅")],
        links=[JR, link("info", "美瑛のめぐり方（貸自転車の一覧）", "Getting around Biei (Japanese)", U["cruise"])],
        rows=[row("train", "美馬牛→美瑛 16:18→16:25、17:31→17:38、18:32→18:39", "Bibaushi → Biei 16:18→16:25, 17:31→17:38, 18:32→18:39"),
              row("fee", "JR 美馬牛→美瑛320円", "JR Bibaushi → Biei ¥320")],
        tip=TIP_JR),
    shikisai=dict(
        name=T("四季彩の丘", "Shikisai-no-oka"), kind=T("花畑", "Flower garden"),
        blurb=T("丘の斜面に花の帯が何本も並ぶ展望花畑。奥に十勝岳の山並みが見えます。",
                "Stripes of flowers running across a hillside, with the Tokachi range behind."),
        lat=43.528087, lng=142.466049,
        body=T("丘の斜面に、色の違う花が帯のように植えられた花畑です。グリーンシーズンは4月下旬〜10月下旬。広いので、園内の乗りもの（有料）もあります。アルパカ牧場（有料）は閉園の30分前まで。\n\n"
               "入場料がかかるのは7〜9月だけで、高校生以上800円、小・中学生500円（券売機。窓口は現金のみ）。それ以外の月の入場は、公式の案内に料金がありません。営業時間は5月・10月が8:40〜17:00、6〜9月が8:40〜17:30（7〜9月の最終入園は17:15）。レストランは15:00ラストオーダーで水曜休み、売店にはじゃがいものコロッケがあります。\n\n"
               "冬は花畑が雪に埋もれて「スノーランド」になり、スノーモービルやスノーラフトに乗れます（有料。雪が十分に積もってから始まります）。",
               "A hillside planted with bands of flowers in different colours. The green season runs from late April to late October. The grounds are large, and there are paid rides to get around. The alpaca farm (extra charge) closes 30 minutes before the garden.\n\n"
               "Admission is charged only from July to September: ¥800 for high-school age and above, ¥500 for younger schoolchildren (ticket machine; the counter takes cash only). The official guide lists no charge for other months. Hours are 8:40–17:00 in May and October and 8:40–17:30 from June to September (last entry 17:15 in July–September). The restaurant takes last orders at 15:00 and is closed on Wednesdays; the shop sells potato croquettes.\n\n"
               "In winter the fields disappear under snow and the garden becomes “Snow Land”, with snowmobiles and snow rafting (paid; starting once enough snow has fallen)."),
        gmaps=[gm("四季彩の丘", "Shikisai-no-oka", 43.528087, 142.466049, "四季彩の丘")],
        links=[link("official", "四季彩の丘 ご利用案内", "Shikisai-no-oka", U["shikisai"], U["shikisai_en"]), JR],
        rows=[row("hours", "5月・10月8:40〜17:00、6〜9月8:40〜17:30（7〜9月の最終入園17:15）。レストランは15:00ラストオーダー", "May and Oct 8:40–17:00, Jun–Sep 8:40–17:30 (last entry 17:15 in Jul–Sep). Restaurant last orders 15:00"),
              row("fee", "7〜9月だけ入場料：高校生以上800円、小・中学生500円（窓口は現金のみ）", "Admission July–September only: ¥800 (high-school age and up), ¥500 (younger schoolchildren); cash only at the counter"),
              row("closed", "12月31日・1月1日。レストランは水曜休み", "31 December and 1 January. Restaurant closed Wednesdays"),
              row("train", "帰りは美馬牛16:18発（美瑛16:25着）。逃すと次は17:31発", "Back from Bibaushi at 16:18 (Biei 16:25); the next is 17:31")],
        tip=T("四季彩の丘の公式サイト（ご利用案内・ウィンターシーズン）と美瑛町観光協会のページで確認しました（2026年11月28日）。",
              "Checked on Shikisai-no-oka’s official site (visitor guide, winter season) and the Biei Tourism Association’s page on 28 November 2026.")),
)

# ---------------------------------------------------------------------------
# コース
# ---------------------------------------------------------------------------
LATE = dict(
    file="biei.json", course="late",
    order=["asahikawa", "eki", "hokusei", "kenmary", "seven", "machi", "pond", "falls", "onsen", "kaeri"],
    spots=dict(
        asahikawa=dict(
            pre=T("雪のない季節（4月下旬〜10月）の1日です。旭川9:38発で美瑛10:12着。駅前で電動自転車を借りて丘を回り、お昼のあと13:45のバスで青い池へ。白ひげの滝を見て白金温泉に入り、美瑛の町で晩ごはんを食べて、18:40の電車で旭川19:13着。",
                  "A day for the snow-free months (late April to October). The 9:38 from Asahikawa reaches Biei at 10:12. Rent an e-bike by the station and ride the hills, then after lunch take the 13:45 bus to the Blue Pond. See Shirahige Falls, soak at Shirogane Onsen, have dinner in Biei and take the 18:40 train (Asahikawa 19:13)."),
            notices=[N_TO_WINTER, N_GREEN_ONLY, N_LASTBUS, N_JR_2027],
            time=(DEP, "9:38（旭川駅に9:25ごろ）", "9:38 (be at Asahikawa Station by about 9:25)")),
        eki=dict(
            pre=T("10:12着。大きな荷物は四季の情報館に預け、駅前の店で電動自転車を借ります（借りる手続きに15分ほどみて、10:30に出発）。13:35までに返して、13:45のバスに乗ります。自転車に乗らない人は、美瑛ハイヤーのタクシーを時間貸しで頼む方法があります。",
                  "Arrive 10:12. Leave big bags at Shiki-no-Johokan and rent an e-bike at one of the shops by the station (allow 15 minutes for the paperwork and set off at 10:30). Return it by 13:35 for the 13:45 bus. Not cycling? You can hire a Biei Hire taxi by the hour instead."),
            time=(MOV, "10:12着、10:30に自転車で出発", "arrive 10:12, set off by bike at 10:30")),
        hokusei=dict(pre=T("駅から坂を上って15分ほど。最初にここで全体をながめ、トイレも済ませます。", "About 15 minutes uphill from the station. Start here for the overview, and use the toilets."),
                     time=(VIS, "10:45〜11:05", "10:45–11:05")),
        kenmary=dict(pre=T("北西の丘から5分ほど。", "About 5 minutes from Hokusei-no-oka."), time=(VIS, "11:10〜11:25", "11:10–11:25")),
        seven=dict(pre=T("ケンとメリーの木から20分ほど。12:00に出れば、12:35ごろ駅に戻れます。", "About 20 minutes from the Ken & Mary Tree. Leave by 12:00 and you are back at the station around 12:35."),
                   time=(VIS, "11:45〜12:00", "11:45–12:00")),
        machi=dict(pre=T("12:35ごろ駅に戻り、自転車を返してお昼。13:45のバスに乗るので、13:35には店を出ます。", "Back at the station around 12:35; return the bike and have lunch. Leave by 13:35 for the 13:45 bus."),
                   time=(VIS, "12:40〜13:35", "12:40–13:35")),
        pond=dict(pre=T("美瑛駅前13:45発のバスで、白金青い池入口14:07着（800円）。15:07発のバスで白金温泉へ進むので、15:00にはバス停へ戻り始めます。晴れた日のこの時間は混みます。人の少ない池を見たい日は、順番を変えて、旭川駅前9:40発の39番のバスで先に青い池へ（10:56着）。",
                       "Take the 13:45 bus from Biei Station to the Blue Pond stop (14:07, ¥800). You continue to Shirogane Onsen on the 15:07, so start back to the stop by 15:00. On sunny days this is the busy time; for a quieter pond, switch the order and take the 9:40 route 39 bus from Asahikawa Station straight to the pond (10:56)."),
                  time=(VIS, "14:15〜15:00", "14:15–15:00")),
        falls=dict(pre=T("青い池入口15:07発のバスで白金温泉15:11着（220円）。バス停から歩いて3分。", "The 15:07 bus from the pond reaches Shirogane Onsen at 15:11 (¥220). Three minutes’ walk from the stop."),
                   time=(VIS, "15:15〜15:35", "15:15–15:35")),
        onsen=dict(pre=T("滝のすぐそばの宿で入浴。16:32のバスに乗るなら、16:20には出ます。ゆっくり入りたい人は18:02発の最終バスで（美瑛駅前18:30着、18:40の電車に乗り継ぎ）。",
                        "Bathe at one of the hotels beside the falls. For the 16:32 bus, be out by 16:20. Want a longer soak? Take the last bus at 18:02 (Biei Station 18:30, connecting with the 18:40 train)."),
                   time=(VIS, "15:40〜16:20", "15:40–16:20")),
        kaeri=dict(pre=T("白金温泉16:32発のバスで美瑛駅前17:00着（900円）。預けた荷物を受け取り（受け取れる時間は、朝に預けるときに確かめておきます）、17:15ごろから晩ごはん。18:40発で旭川19:13着。まっすぐ帰るなら17:39発（旭川18:19着）。",
                        "The 16:32 bus from Shirogane Onsen reaches Biei Station at 17:00 (¥900). Pick up your bags (ask in the morning until when you can collect them) and have dinner from about 17:15, then take the 18:40 (Asahikawa 19:13). To go straight back, take the 17:39 (Asahikawa 18:19)."),
                   time=(DEP, "18:40（旭川19:13着）", "18:40 (Asahikawa 19:13)")),
    ),
)

EARLY = dict(
    file="biei-winter.json", course="early",
    order=["asahikawa", "eki", "xmas", "machi", "falls", "onsen", "pond", "kaeri"],
    spots=dict(
        asahikawa=dict(
            pre=T("冬（11月〜4月中旬）の1日です。旭川9:38発で美瑛10:12着。予約しておいたクリスマスツリーライナーで雪の丘の木を見て、町でお昼。13:45のバスで白金へ行き、白ひげの滝と温泉。日が沈んだら16:32のバスで青い池のライトアップへ。最終の18:05のバスで美瑛に戻り、18:40の電車で旭川19:13着。\n\n"
                     "金・土曜は、青い池を観光協会の「美遊バス ライトアップコース」（美瑛16:35発、予約制）で見るほうが楽です。その日は順番を変えて、旭川駅前9:40発の39番のバスで先に白金温泉へ（11:00着）。滝と温泉とお昼のあと、白金温泉13:16発のバスで美瑛へ戻り（13:44着）、14:50発のクリスマスツリーライナー、16:35発のライトアップコースと続けると、外で待つ時間がほとんどありません。",
                  "A winter day (November to mid-April). The 9:38 from Asahikawa reaches Biei at 10:12. Ride the pre-booked Christmas Tree Liner to the tree on the snowy hill, then lunch in town. Take the 13:45 bus to Shirogane for Shirahige Falls and a hot spring. After dark, the 16:32 bus takes you to the lit-up Blue Pond; the last bus at 18:05 brings you back to Biei for the 18:40 train (Asahikawa 19:13).\n\n"
                  "On Fridays and Saturdays it is easier to see the pond on the tourism association’s Biyu Bus light-up tour (16:35 from Biei, booking needed). On those days, change the order: take the 9:40 route 39 bus from Asahikawa Station straight to Shirogane Onsen (11:00), see the falls, bathe and have lunch, ride the 13:16 bus back to Biei (13:44), then join the 14:50 Christmas Tree Liner and the 16:35 light-up tour. You will hardly wait outdoors at all."),
            caution=T("青い池では夜に1時間以上、外にいます", "Over an hour outdoors after dark at the pond"),
            notices=[N_COLD, N_LASTBUS, N_NEWYEAR, N_LINER_OFF_NOV, N_LINER_OFF_SPRING, N_MARCH_LIGHT],
            time=(DEP, "9:38（旭川駅に9:25ごろ）", "9:38 (be at Asahikawa Station by about 9:25)")),
        eki=dict(
            pre=T("10:12着。四季の情報館の1階で、10:35までにクリスマスツリーライナーの受付を済ませます（予約のQRコードを見せます）。大きな荷物はここに預けられます。歩道は踏み固められた雪で滑ります。",
                  "Arrive 10:12. Check in for the Christmas Tree Liner at the ground-floor counter of Shiki-no-Johokan by 10:35 (show your booking QR code). You can leave large bags here. The pavements are packed snow and slippery."),
            time=(MOV, "10:12着、10:35までに受付", "arrive 10:12, check in by 10:35")),
        xmas=dict(pre=T("四季の情報館10:45発、11:45に戻ります。", "Leaves Shiki-no-Johokan at 10:45 and is back at 11:45."),
                  notices=[N_LINER_OFF_NOV, N_LINER_OFF_SPRING, N_NEWYEAR, N_MANNER],
                  time=(VIS, "10:45〜11:45（ライナーの往復）", "10:45–11:45 (the Liner’s round trip)")),
        machi=dict(pre=T("11:50ごろからお昼。13:45のバスまで時間があるので、食べたあとは四季の塔か、道の駅の売店へ。13:35にはバス停へ向かいます。", "Lunch from about 11:50. There is time before the 13:45 bus for the tower or the roadside-station shop; head for the bus stop by 13:35."),
                   notices=[N_NEWYEAR],
                   time=(VIS, "11:50〜13:35", "11:50–13:35")),
        falls=dict(pre=T("美瑛駅前13:45発のバスで白金温泉14:11着（900円）。バス停から歩いて3分。まだ明るいうちに、青い川と滝を見ます。温泉のあと、暗くなってからもう一度のぞくとライトアップが見られます。",
                        "The 13:45 bus from Biei Station reaches Shirogane Onsen at 14:11 (¥900); the falls are 3 minutes from the stop. See the blue river and the falls while it is still light. Look in again after your bath, once it is dark, for the light-up."),
                   rows=[SUN], notices=[N_NEWYEAR],
                   time=(VIS, "14:15〜14:40", "14:15–14:40")),
        onsen=dict(pre=T("14:45ごろから入浴。16:32のバスに乗るので、16:15には出て、厚着をし直します。髪はよく乾かしてください（外は氷点下です）。",
                        "Bathe from about 14:45. For the 16:32 bus, be out by 16:15 and get properly wrapped up again. Dry your hair well: it is below freezing outside."),
                   time=(VIS, "14:45〜16:15", "14:45–16:15")),
        pond=dict(pre=T("白金温泉16:32発のバスで、白金青い池入口16:35着（220円）。12月は16:30、1月は17:00、2月は17:30に点灯します。帰りは18:05発の最終バスだけなので、17:55にはバス停に戻ります。それまで外にいることになるので、寒さがきびしい日は無理をせず、青い池を外して温泉に長く入り、白金温泉18:02発の同じ最終バスで帰ってください。途中で帰りたくなったときのために、美瑛ハイヤー（0166-92-1181）の番号を控えておくと安心です（迎えに来てもらえるか、料金は要確認）。",
                       "The 16:32 bus from Shirogane Onsen reaches the Blue Pond stop at 16:35 (¥220). Lights come on at 16:30 in December, 17:00 in January and 17:30 in February. The only bus back is the last one at 18:05, so return to the stop by 17:55. You will be outdoors until then: on a bitterly cold day, don’t push it. Skip the pond, stay longer in the bath and catch the same last bus from Shirogane Onsen at 18:02. Keep Biei Hire’s number (0166-92-1181) in case you want to leave early; ask whether they can collect you and what it costs."),
                  rows=[SUN], notices=[N_COLD, N_LASTBUS, N_MARCH_LIGHT, N_NEWYEAR],
                  caution=T("夜は暖まれる建物なし。最終バス18:05", "No shelter at night; last bus 18:05"),
                  time=(VIS, "16:40〜17:55（最終バス18:05発）", "16:40–17:55 (last bus 18:05)")),
        kaeri=dict(pre=T("最終バスは美瑛駅前18:30着。朝に四季の情報館へ荷物を預けるときは、18:30すぎに受け取れるかを必ず聞いてください（観光協会の営業は平日17:15までと案内されています。受け取れないなら持ったまま回ります）。18:40発で旭川19:13着。バスが遅れて間に合わなかったら、駅の近くで晩ごはんを食べて19:54発（旭川20:27着）に。",
                        "The last bus reaches Biei Station at 18:30. If you leave bags at Shiki-no-Johokan in the morning, ask whether you can collect them after 18:30 (the tourism association lists weekday hours until 17:15); if not, carry them with you. Take the 18:40 (Asahikawa 19:13). If the bus runs late and you miss it, have dinner near the station and take the 19:54 (Asahikawa 20:27)."),
                   notices=[N_NEWYEAR],
                   time=(DEP, "18:40（旭川19:13着）", "18:40 (Asahikawa 19:13)")),
    ),
)

FURANO = dict(
    file="biei-furano.json", course="furano",
    order=["asahikawa", "tomita", "bibaushi", "shikisai", "machi", "kaeri"],
    spots=dict(
        asahikawa=dict(
            pre=T("花の季節（5月〜10月はじめ）の1日です。旭川9:38発の富良野線で、美瑛を通って中富良野10:46着。ファーム富田を歩いてお昼を食べ、13:27の電車で美馬牛（びばうし）へ戻って四季彩の丘。16:18の電車で美瑛に出て、町で晩ごはんを食べて18:40発で旭川19:13着。駅から花畑まで、片道25〜30分の歩きが2回あります。",
                  "A day for the flower season (May to early October). The 9:38 Furano Line train from Asahikawa passes Biei and reaches Nakafurano at 10:46. Walk around Farm Tomita and have lunch, take the 13:27 back to Bibaushi for Shikisai-no-oka, then the 16:18 to Biei for dinner and the 18:40 (Asahikawa 19:13). Expect two walks of 25–30 minutes each way between station and garden."),
            caution=T("片道25〜30分の歩きが2回", "Two 25–30 minute walks each way"),
            notices=[N_FURANO_SEASON, N_NOROKKO, N_JR_2027],
            time=(DEP, "9:38（旭川駅に9:25ごろ）", "9:38 (be at Asahikawa Station by about 9:25)")),
        tomita=dict(pre=T("中富良野10:46着、歩いて25分で11:15ごろ着きます。花畑を回って、園内のカフェでお昼。13:27の電車に乗るので、12:55には駅へ歩き始めます（次の電車は15:55までありません）。",
                         "Arrive at Nakafurano at 10:46 and walk 25 minutes, getting there about 11:15. See the fields and have lunch at one of the cafés. For the 13:27 train, start walking back by 12:55; the next train is not until 15:55."),
                    notices=[N_FURANO_SEASON, N_NOROKKO],
                    time=(VIS, "11:15〜12:55", "11:15–12:55")),
        bibaushi=dict(pre=T("中富良野13:27発で13:45着（470円）。ここから四季彩の丘へ歩きます。", "The 13:27 from Nakafurano arrives at 13:45 (¥470). Walk on to Shikisai-no-oka from here."),
                      time=(MOV, "13:45着", "arrive 13:45")),
        shikisai=dict(pre=T("14:15ごろ着。16:18の電車に乗るので、15:40には駅へ歩き始めます。", "Arrive about 14:15. For the 16:18 train, start walking back to the station by 15:40."),
                      time=(VIS, "14:15〜15:40", "14:15–15:40")),
        machi=dict(name=T("美瑛の町：丘のくらと四季の塔", "Biei town: Okanokura and the tower"), kind=T("町歩き・みやげ", "Town · Shop"),
                   pre=T("美馬牛16:18発で美瑛16:25着（320円）。道の駅「丘のくら」は6〜8月は18:00まで、5月・9〜10月は17:00までなので、先にみやげを見てから、四季の塔か晩ごはんへ。",
                         "The 16:18 from Bibaushi reaches Biei at 16:25 (¥320). Okanokura closes at 18:00 from June to August and 17:00 in May, September and October, so shop there first, then go on to the tower or dinner."),
                   time=(VIS, "16:30〜17:15", "16:30–17:15")),
        kaeri=dict(pre=T("17:15ごろから晩ごはん。18:40発で旭川19:13着。まっすぐ帰るなら17:39発（旭川18:19着）。", "Dinner from about 17:15, then the 18:40 (Asahikawa 19:13). To go straight back, take the 17:39 (Asahikawa 18:19)."),
                   time=(DEP, "18:40（旭川19:13着）", "18:40 (Asahikawa 19:13)")),
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
    photos = PHOTOS[sid]
    order = C.get("photos", {}).get(sid)
    if order:   # コースで最初の写真を変える（冬は雪・夜の写真を先に）
        by = {p["file"][:-4]: p for p in photos}
        photos = [by[k] for k in order] + [p for p in photos if p["file"][:-4] not in order]
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"], links=o.get("links", b.get("links", [JR])),
               notices=o.get("notices", []),
               info={"rows": o.get("rows", []) + b["rows"], "cash": False, "tip": b["tip"], "checked": CHECKED},
               photos=photos)
    assert out["photos"], sid
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


# 冬のコースで先に出す写真（雪・夜）。ファイル名は scripts/biei_web_photos.json を見て決める
EARLY["photos"] = WEB.get("_winter_first", {})

for C in (LATE, EARLY, FURANO):
    N = {k: i for i, k in enumerate(C["order"], 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
    fixed = {"late": ("asahikawa", "eki", "kaeri"), "early": ("asahikawa", "eki", "kaeri"), "furano": ("asahikawa", "bibaushi", "kaeri")}[C["course"]]
    picks = [N[k] for k in C["order"] if k not in fixed]
    auto = {str(N[k]): {"always": True} for k in fixed}
    if C is LATE:
        sections = [{"first": 1, "last": N["eki"], "area": T("旭川→美瑛", "Asahikawa → Biei"), "title": T("9:38の電車で美瑛へ", "The 9:38 train to Biei")},
                    {"first": N["hokusei"], "last": N["seven"], "area": T("美瑛・パッチワークの路", "Biei · Patchwork Road"), "title": T("電動自転車で丘を回る", "The hills by e-bike")},
                    {"first": N["machi"], "last": N["machi"], "area": T("美瑛・駅前", "Biei · station"), "title": T("石の倉庫の道の駅でお昼", "Lunch at the stone-warehouse roadside station")},
                    {"first": N["pond"], "last": N["onsen"], "area": T("白金", "Shirogane"), "title": T("13:45のバスで青い池、滝、温泉", "The 13:45 bus to the pond, the falls and a hot spring")},
                    {"first": N["kaeri"], "last": N["kaeri"], "area": T("美瑛・夜", "Biei · evening"), "title": T("晩ごはんと18:40の電車", "Dinner and the 18:40 train")}]
        hints = [
            h("kenmary", {"none": ns("seven")}, "セブンスターの木を外すと、北西の丘とケンとメリーの木で1時間ほど。11:40ごろ駅に戻れるので、お昼をゆっくり食べられます。",
              "Without the Seven Stars Tree, Hokusei-no-oka and the Ken & Mary Tree take about an hour. You are back at the station around 11:40, with time for a slow lunch."),
            h("pond", {"none": ns("hokusei", "kenmary", "seven")}, "丘を回らない日は、旭川駅前9:40発の39番のバスでまっすぐ青い池へ（10:56着）。混む前に見て、12:16発のバスで白金温泉へ進めます（12:20着）。",
              "Skipping the hills? Take the 9:40 route 39 bus from Asahikawa Station straight to the pond (10:56), see it before the crowds and go on to Shirogane Onsen on the 12:16 (12:20)."),
            h("kaeri", {"none": ns("onsen")}, "温泉に入らない日は、滝を見たあと白金温泉15:46発のバスで美瑛駅前16:14着。",
              "Not bathing? After the falls, take the 15:46 bus from Shirogane Onsen (Biei Station 16:14)."),
            h("falls", {"none": ns("pond")}, "青い池に寄らない日は、美瑛駅前13:45発のバスでそのまま白金温泉へ（14:11着）。温泉にゆっくり入れます。",
              "Leaving out the pond? Stay on the 13:45 bus to Shirogane Onsen (14:11) and take your time in the bath."),
        ]
        note = "「雪のない季節（4月下旬〜10月）」。旭川9:38→美瑛10:12。電動自転車で北西の丘→ケンとメリーの木→セブンスターの木→丘のくらでお昼→13:45のバスで青い池→15:07のバスで白金温泉（白ひげの滝・日帰り入浴）→16:32のバスで美瑛→晩ごはん→美瑛18:40発（旭川19:13着）。"
    elif C is EARLY:
        sections = [{"first": 1, "last": N["eki"], "area": T("旭川→美瑛", "Asahikawa → Biei"), "title": T("9:38の電車で美瑛へ", "The 9:38 train to Biei")},
                    {"first": N["xmas"], "last": N["machi"], "area": T("美瑛・丘と駅前", "Biei · hills and station"), "title": T("雪の丘の1本の木と、町でお昼", "A lone tree on a snowy hill, then lunch in town")},
                    {"first": N["falls"], "last": N["onsen"], "area": T("白金温泉", "Shirogane Onsen"), "title": T("13:45のバスで白金へ、滝と温泉", "The 13:45 bus to Shirogane: falls and a hot spring")},
                    {"first": N["pond"], "last": N["kaeri"], "area": T("青い池・夜", "Blue Pond · evening"), "title": T("ライトアップと、18:05の最終バス", "The light-up and the last bus at 18:05")}]
        hints = [
            h("machi", {"none": ns("xmas")}, "クリスマスツリーの木に行かない日（ライナーが走らない日・予約が取れなかった日）は、旭川10:39発の電車（美瑛11:13着）でも間に合います。お昼を食べて13:45のバスへ。",
              "Not going to the Christmas Tree (no Liner that day, or no seats)? The 10:39 train from Asahikawa (Biei 11:13) is early enough. Have lunch and take the 13:45 bus."),
            h("kaeri", {"none": ns("pond")}, "青い池に寄らない日は、温泉にゆっくり入り、暗くなってから白ひげの滝のライトアップを見て、白金温泉18:02発の最終バスで美瑛駅前18:30着。",
              "Leaving out the pond? Take a long bath, see Shirahige Falls lit up after dark and catch the last bus from Shirogane Onsen at 18:02 (Biei Station 18:30)."),
            h("pond", {"none": ns("onsen")}, "温泉に入らない日は、滝のあと、日帰り入浴のある宿のロビーや食事処が使えるかを聞いてみてください（外で16:32のバスを待つのは寒すぎます）。または美瑛駅前14:45発のバスで来れば、白金温泉15:11着で待つ時間が短くなります。",
              "Not bathing? After the falls, ask whether one of the hotels will let you use its lobby or café; it is too cold to wait outdoors for the 16:32 bus. Or come on the 14:45 bus from Biei Station (Shirogane Onsen 15:11) to shorten the wait."),
        ]
        note = "「冬（11月〜4月中旬）」。旭川9:38→美瑛10:12。クリスマスツリーライナー10:45〜11:45（12月1日〜2月28日・予約制）→丘のくらでお昼→13:45のバスで白金温泉（白ひげの滝・日帰り入浴）→16:32のバスで青い池のライトアップ→最終18:05のバスで美瑛18:30→美瑛18:40発（旭川19:13着）。"
    else:
        auto[str(N["bibaushi"])] = {"any": ns("shikisai")}
        sections = [{"first": 1, "last": N["tomita"], "area": T("旭川→中富良野", "Asahikawa → Nakafurano"), "title": T("9:38の電車でファーム富田へ、園内でお昼", "The 9:38 train to Farm Tomita, lunch on site")},
                    {"first": N["bibaushi"], "last": N["shikisai"], "area": T("美瑛・美馬牛", "Biei · Bibaushi"), "title": T("13:27の電車で戻って、四季彩の丘", "Back on the 13:27 for Shikisai-no-oka")},
                    {"first": N["machi"], "last": N["kaeri"], "area": T("美瑛・駅前", "Biei · station"), "title": T("町を歩いて晩ごはん、18:40の電車", "The town, dinner and the 18:40 train")}]
        hints = [
            h("machi", {"none": ns("shikisai")}, "四季彩の丘に寄らない日は、中富良野13:27発の電車でそのまま美瑛へ（13:53着）。美瑛駅前14:45発のバスで青い池（15:07着）にも行けます。帰りは青い池入口16:35発か、最終18:05発のバスで。",
              "Leaving out Shikisai-no-oka? Stay on the 13:27 from Nakafurano to Biei (13:53). You could then take the 14:45 bus to the Blue Pond (15:07) and come back on the 16:35 or the last bus at 18:05."),
            h("shikisai", {"none": ns("tomita")}, "ファーム富田に寄らない日は、旭川9:38発で美馬牛10:22着（800円）。午前に四季彩の丘を見て、美馬牛から美瑛へ戻れば、午後は「雪のない季節」のコースの青い池と白金温泉に回れます。",
              "Leaving out Farm Tomita? The 9:38 from Asahikawa reaches Bibaushi at 10:22 (¥800). See Shikisai-no-oka in the morning, return to Biei and you can spend the afternoon at the Blue Pond and Shirogane Onsen as in the snow-free course."),
        ]
        note = "「花畑（5月〜10月はじめ）」。旭川9:38→中富良野10:46。歩いてファーム富田（お昼）→中富良野13:27→美馬牛13:45→歩いて四季彩の丘→美馬牛16:18→美瑛16:25→丘のくら・四季の塔・晩ごはん→美瑛18:40発（旭川19:13着）。"
    data = {
        "id": "biei", "course": C["course"],
        "_note": "美瑛・青い池と富良野（旭川から日帰り。biei/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "写真はすべて Wikimedia Commons（一覧は scripts/biei_web_photos.json）。info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。"
                 + "このファイルは scripts/build_biei_data.py で作る（直接直さない）。",
        "sections": sections, "focus": {"first": 2, "last": N["kaeri"]},
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。旭川駅・美瑛駅（花畑のコースは美馬牛駅）・帰りは自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": picks, "auto": auto, "hints": hints},
        "photoBase": "../images/biei/", "sources": SOURCES,
        "spots": [spot(C, i, k) for i, k in enumerate(C["order"], 1)],
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"]) for s in data["spots"]])
