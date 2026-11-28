#!/usr/bin/env python3
"""札幌から日帰り 温泉めぐり（sapporo-onsen）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_sapporo_onsen_data.py   （そのあと python3 scripts/sync_sapporo_onsen.py）
- data/routes/sapporo-onsen.json             … 定山渓（じょうざんけい）温泉（jozankei。最初に開く）7か所
- data/routes/sapporo-onsen-noboribetsu.json … 登別（のぼりべつ）温泉（noboribetsu）8か所
- どちらも札幌駅・大通・すすきののホテルを9〜10時に出る1日。夜は札幌に戻る（21〜23時着）。一年中使えるコースにして、
  冬（雪・凍った道・早い日没・冬だけの休み）は notices（from / to）と rows（until）で出す
- 3つ目の温泉地（洞爺湖・支笏湖）は作らない（2026-11-26）：札幌から片道2時間半以上か、バスが少なく、日帰りで無理がないコースにならないため
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 時刻：JR は乗換案内の2026年12月3日（木）・5日（土）。JR北海道は2027年3月にダイヤ改正があるので、そのあと確かめ直す。
  バスはじょうてつバス（2026-04-01改正、かっぱライナー号は2026-10-01改正）と道南バス（2026-10-01改正）の公式の時刻表
- タトゥー：お風呂ごとに公式サイトの決まりを書いた。書いていない施設は「要確認」。足湯はどこも無料で、入る条件の記載はない
- 店名は、定山渓観光協会・登別国際観光コンベンション協会の店の紹介ページで時間を確かめた店だけ
- 写真はまだ Wikimedia Commons だけ（scripts/sapporo_onsen_web_photos.json）。オーナーの写真はあとで <スポットのid>-<番号>.jpg で入る
- 文章は中立に（だれかが行った・食べたとは書かない）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = "sapporo-onsen"
IMG = f"{R}/images/{ID}"
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


def winters(hja, hen, ja, en, url=None, months=("11-15", "04-15")):
    """冬だけ出すお知らせを、2026〜2029年の冬の分つくる（from / to は年つきの日付なので）"""
    return [notice(hja, hen, ja, en, url, f"{y}-{months[0]}", f"{y + 1}-{months[1]}") for y in (2026, 2027, 2028)]


def q(f, t, day, hm, kind="d"):
    """確かめた乗換案内（Yahoo!路線情報）の検索結果のURL。day は '2026/12/03' の形"""
    h, m = hm.split(":")
    y, mon, d = day.split("/")
    p = dict(to=t, y=y, m=mon, d=d, hh=h, m1=m[0], m2=m[1], type={"d": 1, "l": 2, "a": 4}[kind], ticket="normal",
             expkind=1, shin=1, ex=1, hb=1, lb=1, al=1, sr=1, s=0, userpass=1, ws=3)
    p["from"] = f
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(p)


def cc(x):
    """Wikimedia Commons の写真。"""
    return {"file": x["file"], "credit": {"author": x["author"], "license": x["license"],
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(x["title"].replace(" ", "_"))}}


WEB = json.load(open(f"{R}/scripts/sapporo_onsen_web_photos.json", encoding="utf-8"))


def W(sid):
    """そのスポットの写真。オーナーの写真（<sid>-<番号>.jpg）があれば先に並べる"""
    own = sorted(f for f in os.listdir(IMG) if f.startswith(sid + "-") and not f.startswith(sid + "-w")) if os.path.isdir(IMG) else []
    return own + [cc(x) for x in WEB.get(sid, [])]


D1, D2 = "2026/12/03", "2026/12/05"   # 木曜・土曜
U = dict(
    kappa="https://www.jotetsu.co.jp/bus/kappa_liner/index.html",
    kappa_winter="http://www.jotetsu.co.jp/bus/news/ash96e0000003ig7.html",
    kappa_book="https://jotetsu.quicktrip.jp/buy",
    jt_sapporo="https://www.jotetsu.co.jp/bus/times/260401/sapporoeki-26.pdf",
    jt_yunomachi="https://www.jotetsu.co.jp/bus/times/260401/jyouzankeiyunomati.pdf",
    jt_hoheikyo="https://www.jotetsu.co.jp/bus/times/260401/houheikyouonsen.pdf",
    jt_dec="http://www.jotetsu.co.jp/bus/news/ash96e0000003lq0.html",
    jt_ic="https://www.jotetsu.co.jp/bus/guide/qlqoi2000000005z.html",
    joz_oneday="https://jozankei.jp/oneday/",
    futami_ashiyu="https://jozankei.jp/oneday/hutami-footbat/",
    futami_notice="https://jozankei.jp/news/futami-park-notice/",
    futami_park="https://jozankei.jp/en/spot/1269/",
    iwato="https://jozankei.jp/en/spot/179/",
    gensen="https://jozankei.jp/oneday/jozan-gensen-park/",
    ontama="https://jozankei.jp/oneday/ontama/",
    bussankan="https://jozankei.jp/store/bussankan/",
    ichi="https://jozankei.jp/store/ichi/", koyotei="https://jozankei.jp/store/koyotei/",
    karaku="https://jozankei.jp/store/karaku/", france="https://jozankei.jp/store/france/",
    matsuo="https://jozankei.jp/store/matsuo-jingisukan/", konno="https://jozankei.jp/store/konno/",
    kappa_izakaya="https://jozankei.jp/store/kita-no-kappa/",
    hoheikyo="https://hoheikyo.co.jp/", hoheikyo_onsen="https://hoheikyo.co.jp/onsen/",
    hoheikyo_food="https://jozankei.jp/store/hoheikyo-onsen/",
    hoheikyo_dam="https://jozankei.jp/en/spot/hoheikyo-dam/",
    yukitouro="https://jozankei.jp/event/yukitouro2027/",
    milione="https://www.milione.jp/spa/daytrip/", shikanoyu="https://shikanoyu.co.jp/shikanoyu/spa/day",
    shoten="https://jyozankei-shoten.com/onsen/", kyuujitsu="https://www.kyuujitsu.com/faq/",
    view="https://en.jozankeiview.com/faq/",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    donan_local="https://www.donanbus.co.jp/cms/wp-content/uploads/2026/09/2_R8.10.1_noboribetsu.pdf",
    donan_onsengo="https://www.donanbus.co.jp/cms/wp-content/uploads/2026/10/R8.12_onsen_airport.pdf",
    nb_luggage="https://noboribetsu-spa.jp/usefulinfo/tenimotsu/",
    nb_oneday="https://noboribetsu-spa.jp/oneday/",
    jigoku="https://noboribetsu-spa.jp/spot/spot0034/", tessen="https://noboribetsu-spa.jp/spot/spot0059/",
    oyunuma="https://noboribetsu-spa.jp/spot/spot0055/", ashiyu="https://noboribetsu-spa.jp/spot/spot0068/",
    oyu_course="https://noboribetsu-spa.jp/modelcourse/120min/%e5%9c%b0%e7%8d%84%e6%ba%80%e5%96%ab%e3%82%b3%e3%83%bc%e3%82%b9/",
    ashiyu_winter="https://www.visit-hokkaido.jp/spot/detail_11428.html",
    sengen="https://noboribetsu-spa.jp/spot/spot0079/", enma="https://noboribetsu-spa.jp/spot/spot0103/",
    daio="https://noboribetsu-spa.jp/spot/spot0189/", tenho="https://noboribetsu-spa.jp/spot/spot0206/",
    ichiba="https://noboribetsu-spa.jp/spot/spot0169/", adex="https://noboribetsu-spa.jp/spot/spot0228/",
    isekura="https://noboribetsu-spa.jp/spot/spot0190/",
    bear="https://bearpark.jp/information/", bear_top="https://bearpark.jp/",
    sagiri="https://sagiriyu-noboribetsu.com/", sagiri_rule="https://sagiriyu-noboribetsu.com/goriyou/",
    sagiri_nb="https://noboribetsu-spa.jp/oneday/oneday020/",
    taki="https://takimotokan.co.jp/ja/day_spa/", taki_faq="https://takimotokan.co.jp/ja/faq/",
    mansei="https://www.noboribetsu-manseikaku.jp/spa/daytrip/",
    sun="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("地下鉄＋12番バス 平日", q("札幌", "定山渓湯の町", D1, "09:20"), "さっぽろ9:52→真駒内10:10、真駒内駅10:20発12H→定山渓湯の町11:01、290円＋750円"),
    ("地下鉄＋12番バス 土曜", q("札幌", "定山渓湯の町", D2, "09:20"), "さっぽろ9:51→真駒内10:09、10:20発12H→定山渓湯の町11:03"),
    ("かっぱライナー号（冬ダイヤ）", U["kappa_winter"], "2026/10/1〜2027/3/31、11往復。札幌駅9:35→定山渓湯の町10:31。帰りは湯の町17:15→札幌駅18:19（豊平峡温泉17:00発）が最終"),
    ("かっぱライナー号（予約・運賃）", U["kappa"], "全便予約制、1か月前〜前日17:00、空席があれば予約なしでも乗車可。札幌駅〜豊平峡温泉・定山渓車庫前1,700円（ネット割1,460円）。車内は現金（千円札・硬貨）"),
    ("札幌駅のじょうてつバス時刻表", U["jt_sapporo"], "札幌駅から定山渓への快速は朝と9:00の1本だけ。「予約制かっぱライナー号または地下鉄南北線真駒内駅より12J・12Hを」"),
    ("12月のダイヤ改正", U["jt_dec"], "2026年12月はダイヤ改正の予定なし"),
    ("交通系ICカード（じょうてつバス）", U["jt_ic"], "Kitaca・Suicaなど10種類が札幌市内全路線で使える（札幌国際スキー場線を除く）"),
    ("定山渓湯の町の時刻表", U["jt_yunomachi"], "豊平峡温泉行き 平日14:34・15:32・16:32、土日祝14:33・15:29。札幌駅行き快速8 平日20:53・土日祝20:45（12/31〜1/3運休）。真駒内駅行き12 最終21:50"),
    ("豊平峡温泉の時刻表", U["jt_hoheikyo"], "真駒内駅行き12 平日・土日祝とも17:30・18:30・20:00が夕方以降（土日祝の18:30は1/1運休、20:00は12/31〜1/3運休）"),
    ("湯の町→豊平峡温泉", q("定山渓湯の町", "豊平峡温泉", D1, "14:20"), "14:34→14:50、200円（土曜は14:33発）"),
    ("豊平峡温泉→すすきの 18:30 平日", q("豊平峡温泉", "すすきの", D1, "18:25"), "18:30→真駒内→すすきの19:51、850円＋290円"),
    ("豊平峡温泉→すすきの 18:30 土曜", q("豊平峡温泉", "すすきの", D2, "18:25"), "すすきの19:51"),
    ("豊平峡温泉→すすきの 最終 平日", q("豊平峡温泉", "すすきの", D1, "19:50"), "20:00→真駒内20:51→すすきの21:12"),
    ("豊平峡温泉→すすきの 最終 土曜", q("豊平峡温泉", "すすきの", D2, "19:50"), "20:00→すすきの21:20"),
    ("豊平峡温泉→湯の町", q("豊平峡温泉", "定山渓湯の町", D1, "18:25"), "18:30→18:41、200円"),
    ("湯の町→札幌駅 快速8 平日", q("定山渓湯の町", "札幌", D1, "20:40"), "20:53→札幌駅（JR駅に22:13）、1,000円。次は21:50の12番（乗り換え1回）"),
    ("湯の町→札幌駅 快速8 土曜", q("定山渓湯の町", "札幌", D2, "20:30"), "20:45→札幌駅22:00（JR駅に22:04）、1,000円"),
    ("湯の町→すすきの 最終 土曜", q("定山渓湯の町", "すすきの", D2, "21:40"), "21:50→すすきの22:58、1,040円"),
    ("二見の足湯", U["futami_ashiyu"], "9:00〜21:00、無料、年中無休、無人、定員15名、タオル自販機300円、湯の町バス停から徒歩3分"),
    ("二見公園の工事", U["futami_notice"], "2026/9/24〜2027年3月末、二見公園は立入禁止。二見吊橋へは行ける。迂回路は10/1から、冬は閉鎖"),
    ("二見公園（冬）", U["futami_park"], "冬季は積雪のため二見吊橋まで行けません"),
    ("岩戸観音堂", U["iwato"], "7:00〜20:00、365日、参拝無料、洞窟は大人300円・子ども100円、約120mに観音像33体、1936年建立"),
    ("定山源泉公園", U["gensen"], "通年 7:00〜21:00、無料、月見橋のたもと"),
    ("おんたまの湯", U["ontama"], "約20分で温泉卵。卵は対岸の定山渓物産館で3個＋ネット180円。カラスに注意"),
    ("定山渓物産館", U["bussankan"], "8:00〜21:00、不定休、湯の町バス停すぐ、温泉卵セット180円"),
    ("食堂いち", U["ichi"], "11:00〜15:00、火曜休み（祝日・お盆・GW・正月は除く）、定食7種類、定山渓大橋バス停から徒歩5分"),
    ("生そば紅葉亭", U["koyotei"], "11:00〜17:00（そばがなくなり次第終了）、水・木曜休み"),
    ("ラーメン可楽", U["karaku"], "昼11:00〜15:00、夜18:00〜23:00（火曜は夜なし）、水曜・第2第4火曜休み"),
    ("喫茶＆軽食フランセ", U["france"], "10:30〜17:00（L.O.16:30）、カツカレー"),
    ("松尾ジンギスカン", U["matsuo"], "17:00〜22:00（L.O.21:30）、昼は土日だけ11:30〜15:00、不定休"),
    ("食堂こんの", U["konno"], "11:30〜14:00、18:00〜0:00、不定休"),
    ("居酒屋北のかっぱ", U["kappa_izakaya"], "18:00〜24:00、水・日曜休み"),
    ("豊平峡温泉", U["hoheikyo"], "入浴10:00〜22:30（最終受付21:45）、インド料理11:00〜21:00（L.O.）、和食11:00〜14:00・17:00〜20:00（L.O.）、年中無休、現金・カード・QR決済"),
    ("豊平峡温泉（温泉）", U["hoheikyo_onsen"], "大人1,300円・子ども600円、タオル220円・バスタオル500円（販売）、ボディソープ・リンスインシャンプーあり、家族風呂なし、露天は日替わりで男女入れ替え。タトゥーの記載なし"),
    ("豊平峡温泉の料理", U["hoheikyo_food"], "チキンカリー1,200円、ラムカリー1,400円など"),
    ("豊平峡ダム", U["hoheikyo_dam"], "期間5/2〜11/3、8:45〜16:00、大人1,000円（電気バス）"),
    ("新・雪灯路2027", U["yukitouro"], "2027/1/20〜2/28、18:00〜21:30（最終入場21:15）、無料。定山渓神社は宿泊者限定。中止は当日14:00ごろ告知"),
    ("ホテルミリオーネ 日帰り入浴", U["milione"], "入れ墨・タトゥー・疑似シール・ペインティングは入場・入浴お断り"),
    ("鹿の湯 日帰り入浴", U["shikanoyu"], "刺青・タトゥーの入浴お断り"),
    ("旅籠屋 定山渓商店", U["shoten"], "日帰り13:30〜18:00・1,200円、刺青・タトゥーはご遠慮"),
    ("休日ビルヂング", U["kyuujitsu"], "刺繍やタトゥーは入館お断り（シール・ペイントも含む）"),
    ("定山渓ビューホテル", U["view"], "tattoos, temporary tattoos or body paint: cannot use baths or pools"),
    ("日帰り入浴の一覧（定山渓）", U["joz_oneday"], "13施設と無料の足湯5か所"),
    ("札幌→登別 平日", q("札幌", "登別", D1, "09:22"), "特急北斗8号 9:45→10:59、乗車券2,530円＋指定席2,360円"),
    ("札幌→登別 土曜", q("札幌", "登別", D2, "09:22"), "特急北斗8号 9:45→10:59"),
    ("札幌→登別温泉 すずらん", q("札幌", "登別温泉", D1, "09:00"), "特急すずらん4号 9:21→登別10:39、バス10:44→登別温泉11:05、450円"),
    ("登別温泉地区バス時刻表", U["donan_local"], "登別駅前→登別温泉 10:44・11:00・11:13（11:32着）・11:45。登別温泉→登別駅前 17:13・18:00（18:15着）・19:10（19:22着）・20:35（20:47着）。前ドアは一律450円先払い、中ドアは整理券・後払い"),
    ("高速おんせん号", U["donan_onsengo"], "札幌駅前13:40→登別温泉15:20、登別温泉9:30→札幌駅前11:15の1往復。予約制、12〜3月は3,800円"),
    ("登別→札幌 夕方 平日", q("登別", "札幌", D1, "17:30"), "北斗15号 17:34→18:47"),
    ("登別→札幌 18:40 平日", q("登別", "札幌", D1, "18:15"), "すずらん11号 18:40→19:58"),
    ("登別→札幌 18:40 土曜", q("登別", "札幌", D2, "18:15"), "すずらん11号 18:40→19:58"),
    ("登別→札幌 夜 平日", q("登別", "札幌", D1, "19:30"), "北斗19号 20:26→21:41"),
    ("登別→札幌 夜 土曜", q("登別", "札幌", D2, "19:30"), "北斗19号 20:26→21:41"),
    ("登別→札幌 最後 平日", q("登別", "札幌", D1, "20:47"), "北斗21号 21:21→22:41"),
    ("登別→札幌 最後 土曜", q("登別", "札幌", D2, "20:47"), "北斗21号 21:21→22:41"),
    ("北海道レールパス・エリアパス", U["railpass"], "特急は全席指定。エリアパス（札幌・小樽・登別・新千歳空港、4日間）は10,000円（購入は事前）・11,000円（駅）。他社のバスは対象外"),
    ("登別の手荷物預かり", U["nb_luggage"], "9:00〜16:30（窓口17:00まで）、1個500〜700円、日本語・英語・中国語・韓国語"),
    ("地獄谷", U["jigoku"], "無料、直径約450m、1日約1万トン、パークサービスセンターから展望台まで車いす用スロープ（最大8%）"),
    ("鉄泉池", U["tessen"], "地獄谷のほぼ中央の小さな間欠泉、無料"),
    ("大湯沼", U["oyu_course"], "周囲約1kmのひょうたん型の沼、沼底から約130℃の硫黄泉"),
    ("大湯沼川天然足湯", U["ashiyu"], "無料、大湯沼川探勝歩道、大正地獄のすぐ近く"),
    ("大湯沼川天然足湯（冬）", U["ashiyu_winter"], "冬季は遊歩道の通行止めあり"),
    ("泉源公園の間欠泉", U["sengen"], "約3時間の間隔、無料"),
    ("閻魔堂", U["enma"], "からくり山車 10:00・11:00・13:00・15:00・17:00・20:00・21:00、無料、天候により閉めることあり"),
    ("味の大王 登別温泉店", U["daio"], "11:30〜15:00、火曜休み、地獄ラーメン"),
    ("ラーメン天鳳", U["tenho"], "11:30〜14:00／18:00〜23:00、不定休"),
    ("温泉市場", U["ichiba"], "10:30〜21:00（お食事コーナー11:00〜21:00）、不定休"),
    ("adex BAKERY&CAFE", U["adex"], "8:00〜22:00、定休日なし"),
    ("炭火焼＆ラーメンいせくら", U["isekura"], "18:00〜1:00、不定休"),
    ("のぼりべつクマ牧場", U["bear"], "大人3,200円（ロープウェイ往復込み）、10/21〜4/20は9:30〜16:30（最終入園15:50）、4/21〜10/20は9:00〜17:00（16:20）、見学60〜90分、ロッカー300円・200円、カード・交通系IC・QR可、雪の日も入園可"),
    ("クマ牧場の休み", U["bear_top"], "2027/4/5〜4/23はロープウェイ点検で休園"),
    ("夢元さぎり湯", U["sagiri"], "9:00〜21:00（最終受付20:30）、大人500円・子ども180円、1日710円。フェイスタオルなしは入浴不可（2025/12/16）"),
    ("夢元さぎり湯 ご利用案内", U["sagiri_rule"], "タオル・シャンプーは持参が前提。さぎり湯タオル400円、貸しバスタオル200円、シャンプー・ボディソープ各80円。タトゥーの記載なし"),
    ("夢元さぎり湯（観光協会）", U["sagiri_nb"], "大人550円・子ども180円、露天風呂・貸切風呂なし"),
    ("第一滝本館 日帰り入浴", U["taki"], "9:00〜18:00（最終退館21:00）、大人2,500円・子ども1,500円、バスタオル・フェイスタオル込み、温水プール込み、2027/4/5〜15休み"),
    ("第一滝本館 よくある質問", U["taki_faq"], "予約不要、基本無休、各種カード・PayPayなど可。タトゥーの記載なし"),
    ("登別万世閣 日帰り入浴", U["mansei"], "入れ墨・タトゥー・疑似シール・ペインティングは入場・入浴お断り"),
    ("日帰り入浴の一覧（登別）", U["nb_oneday"], "第一滝本館・グランドホテル・石水亭・万世閣・ゆもと登別・はなや・さぎり湯ほか"),
    ("日の入り（札幌）", U["sun"], "12月1日16:01、12月15日16:00、12月21日16:03、12月31日16:09"),
]]

JT = link("timetable", "じょうてつバス 時刻表", "Jotetsu Bus timetables (Japanese)", "https://www.jotetsu.co.jp/bus/times/260401/busstop.html")
KAPPA = link("official", "かっぱライナー号（予約・時刻）", "Kappa Liner: booking and times (Japanese)", U["kappa"])
JOZ = link("info", "定山渓観光協会", "Jozankei Tourist Association", "https://jozankei.jp/", "https://jozankei.jp/en/")
NB = link("info", "登別国際観光コンベンション協会", "Noboribetsu tourism association", "https://noboribetsu-spa.jp/", "https://noboribetsu-spa.jp/en/")
DONAN = link("timetable", "道南バス 登別温泉地区の時刻表（PDF）", "Donan Bus: Noboribetsu Onsen timetable (PDF)", U["donan_local"])
JR = link("timetable", "JR北海道（列車の時刻・運賃）", "JR Hokkaido", "https://www.jrhokkaido.co.jp/", "https://www.jrhokkaido.co.jp/global/index.html")
PASS = link("info", "北海道レールパス・札幌−登別エリアパス", "Hokkaido Rail Pass and Sapporo–Noboribetsu Area Pass", U["railpass"])

# 何か所かに出すお知らせ
N_ICE = winters(
    "冬の道は凍ります", "Icy streets in winter",
    "11月の中ごろから4月の中ごろまでは、雪や凍った道を歩く日があります。滑りにくい靴をはいてください。札幌の12月の日の入りは16時ちょうどごろで、16時半には暗くなります。雪でバスや列車が遅れることもあるので、帰りは1本早めのつもりで。",
    "From mid-November to mid-April expect snow and icy pavements: wear shoes with a good grip. In December the sun sets in Sapporo at about 16:00 and it is dark by 16:30. Snow can delay buses and trains, so plan to head back one service early.",
    U["sun"])
N_TATTOO_J = notice(
    "タトゥーがある人へ", "If you have tattoos",
    "定山渓では、ホテルミリオーネ・鹿の湯・旅籠屋 定山渓商店・休日ビルヂング・定山渓ビューホテルが、公式サイトでタトゥーの入浴を断っています（タトゥーシールやペイントも断ると書いている施設もあります。カバーシールで隠せば入れるという案内はありません）。豊平峡温泉は公式サイトに記載がないので、行く前に電話で確かめてください（011-598-2410）。足湯は無料で、入る条件の記載はありません。",
    "In Jozankei, Hotel Milione, Shikanoyu, Hatagoya Jozankei Shoten, Kyujitsu Building and Jozankei View Hotel all refuse bathers with tattoos on their websites (some also refuse tattoo stickers and body paint; none says covering tattoos makes it OK). Hoheikyo Onsen’s website says nothing about tattoos, so phone before you go (011-598-2410). The foot baths are free and list no conditions.",
    U["milione"])

# ---------------------------------------------------------------------------
# 定山渓のコース
# ---------------------------------------------------------------------------
JOZANKEI = [
    dict(
        id="jstart", name=T("札幌から定山渓へ", "Sapporo to Jozankei"), kind=T("出発・地下鉄とバス", "Start: subway & bus"),
        blurb=T("予約なしなら地下鉄で真駒内へ出て、12番のバスで定山渓へ。予約していれば、札幌駅から直行のかっぱライナー号。",
                "No booking: subway to Makomanai, then the No. 12 bus. Booked: the direct Kappa Liner from Sapporo Station."),
        caution=T("かっぱライナー号は予約制（前日17:00まで）", "Kappa Liner: book by 17:00 the day before"),
        lat=43.06866, lng=141.35079,
        text=T("定山渓（じょうざんけい）温泉は、札幌の中心から南西へ約30km、豊平川（とよひらがわ）の谷にある温泉街です。札幌市の中なので、地下鉄とバスで1時間ほど。\n\n"
               "予約なしで行く：地下鉄南北線のさっぽろ駅9:52発（大通9:53、すすきの9:55）で終点の真駒内（まこまない）へ、10:10着。駅前から、じょうてつバス12番「豊平峡温泉」行き10:20発に乗り、定山渓湯の町（ゆのまち）で降ります。11:01着（土日祝は11:03着）。運賃は地下鉄290円とバス750円で、どちらもKitaca・Suicaなどの交通系ICカードが使えます。\n\n"
               "予約して行く：じょうてつの「かっぱライナー号」は、札幌駅（仮設27番のりば）9:35発、大通西1・すすきのを通って、定山渓湯の町に10:31着。全便予約制で、予約は乗る日の1か月前から前日17:00まで、スマートフォンの予約サイト（カードやPayPayで先払い）か電話0120-737-109（9:00〜17:00）で。空席があれば予約なしでも乗れますが、満席なら乗れません。札幌駅から終点の豊平峡温泉までは片道1,700円（ネット予約1,460円）。車内で払うときは現金（千円札と硬貨）です。\n\n"
               "札幌駅から定山渓へ行く一般のバス（快速7・8番）は、朝の早い時間と9:00の1本だけです。札幌駅の時刻表にも「かっぱライナー号か、地下鉄で真駒内へ出て12番に」と書いてあります。JRのレールパスは、地下鉄にもバスにも使えません。",
               "Jozankei is a hot-spring town in the Toyohira river valley, about 30 km south-west of central Sapporo. It is inside the city, about an hour away by subway and bus.\n\n"
               "Without a booking: take the Namboku subway line from Sapporo Station at 9:52 (Odori 9:53, Susukino 9:55) to the end of the line, Makomanai (10:10). Outside the station, board Jotetsu Bus No. 12 for Hoheikyo Onsen at 10:20 and get off at Jozankei Yunomachi, 11:01 (11:03 at weekends and on holidays). The fares, ¥290 and ¥750, can both be paid with an IC card such as Kitaca or Suica.\n\n"
               "With a booking: the Kappa Liner leaves Sapporo Station (temporary stop 27) at 9:35, calls at Odori Nishi 1 and Susukino, and reaches Jozankei Yunomachi at 10:31. Every trip needs a reservation, from one month ahead until 17:00 the day before, on the booking website by smartphone (pay by card or PayPay when you book) or by phone on 0120-737-109 (9:00–17:00). If seats are left you can board without one; if it is full you cannot. Sapporo Station to the last stop, Hoheikyo Onsen, is ¥1,700 one way (¥1,460 booked online). Paying on board is cash only (¥1,000 notes and coins).\n\n"
               "Ordinary buses from Sapporo Station to Jozankei (rapid routes 7 and 8) run only early in the morning and once at 9:00; the station timetable itself tells you to take the Kappa Liner or go via Makomanai. Japan Rail passes are not valid on the subway or these buses."),
        gmaps=[gm("地下鉄南北線 さっぽろ駅", "Sapporo Station (Namboku subway line)", 43.06866, 141.35079, "地下鉄 さっぽろ駅 南北線"),
               gm("真駒内駅", "Makomanai Station", 42.99117, 141.35843, "真駒内駅 バスターミナル")],
        links=[KAPPA, link("official", "かっぱライナー号 予約サイト", "Kappa Liner booking site", U["kappa_book"]), JT],
        rows=[row("train", "地下鉄 さっぽろ9:52 → 真駒内10:10（土曜は9:51 → 10:09）、290円", "Subway Sapporo 9:52 → Makomanai 10:10 (Sat 9:51 → 10:09), ¥290"),
              row("bus", "12番 真駒内駅10:20 → 定山渓湯の町11:01（土日祝11:03）、750円。交通系IC可", "No. 12 Makomanai 10:20 → Jozankei Yunomachi 11:01 (11:03 weekends/holidays), ¥750. IC cards OK"),
              row("bus", "かっぱライナー号 札幌駅9:35 → 定山渓湯の町10:31（予約制。2026年10月1日〜2027年3月31日の冬ダイヤ）", "Kappa Liner Sapporo Station 9:35 → Jozankei Yunomachi 10:31 (reservation; winter timetable 1 Oct 2026–31 Mar 2027)", until="2027-03-31")],
        notices=N_ICE,
        tip=T("時刻と運賃は乗換案内（2026年12月3日・5日）と、じょうてつバスの公式の時刻表（2026年4月1日改正、かっぱライナー号は10月1日改正）。12月のダイヤ改正はないとの案内です。",
              "Times and fares from a route planner (3 and 5 December 2026) and Jotetsu Bus’s timetables (revised 1 April 2026; Kappa Liner 1 October 2026). Jotetsu says there is no timetable change in December."),
        time=(DEP, "9:52（地下鉄 さっぽろ駅）。かっぱライナー号なら9:35（札幌駅）", "9:52 subway from Sapporo Station, or the 9:35 Kappa Liner")),

    dict(
        id="futami", name=T("二見の足湯と二見吊橋", "Futami foot bath & bridge"), kind=T("足湯・吊り橋", "Foot bath & bridge"),
        blurb=T("湯の町のバス停から歩いて3分、川を見ながら入る無料の足湯。雪のない季節は、その先の二見吊橋まで。",
                "A free foot bath over the river, 3 minutes from the bus stop. When there is no snow, walk on to the suspension bridge."),
        caution=T("冬は雪で吊橋まで行けません。二見公園は工事で立入禁止", "No access to the bridge in snow; Futami Park closed for works"),
        lat=42.96469, lng=141.16006,
        text=T("「四季のせせらぎ 二見の足湯」は、豊平川を見下ろす半屋外の足湯です。9:00〜21:00、無料、年中無休。15人まで入れます。係の人はいない無人の足湯で、入る条件は書かれていないので、タトゥーがあっても気にせず使えます。足をふくタオルは持っていくか、横の自動販売機で買います（1枚300円）。雨や雪の日も屋根の下で入れます。\n\n"
               "足湯から上流へ歩くと、岩の間の川に架かる二見吊橋（ふたみつりばし）。紅葉の名所です。2026年9月24日から2027年3月末までは、二見公園が川の工事で立入禁止ですが、吊橋へは迂回路で行けます。ただし迂回路は冬は閉鎖で、冬は雪で吊橋まで行けません。冬は足湯から川と雪の谷を眺めるだけにして、次の岩戸観音堂へ。",
               "The Futami foot bath is a half-open shelter looking down on the Toyohira river. 9:00–21:00, free, open every day, room for 15. There is no attendant and no conditions are listed for using it, so tattoos are not an issue. Bring a small towel for your feet, or buy one from the vending machine next to it (¥300). There is a roof, so rain or snow is fine.\n\n"
               "Upstream from the foot bath is the Futami suspension bridge over a rocky stretch of river, a well-known autumn-leaf spot. From 24 September 2026 to the end of March 2027 Futami Park is closed for river works, but a detour leads to the bridge. The detour closes in winter, and in winter snow blocks the way to the bridge anyway. In winter, enjoy the river and snowy valley from the foot bath and go on to Iwato Kannon-do."),
        gmaps=[gm("二見の足湯", "Futami foot bath", 42.96500, 141.16050, "四季のせせらぎ 二見の足湯 定山渓"),
               gm("二見吊橋", "Futami suspension bridge", 42.96383, 141.15815, "二見吊橋 定山渓")],
        links=[link("info", "二見の足湯（定山渓観光協会）", "Futami foot bath (Japanese)", U["futami_ashiyu"]),
               link("info", "二見公園の工事のお知らせ", "Futami Park works notice (Japanese)", U["futami_notice"]), JOZ],
        rows=[row("hours", "足湯 9:00〜21:00、年中無休", "Foot bath 9:00–21:00, every day"),
              row("fee", "無料。タオルは自動販売機で1枚300円", "Free. Towels ¥300 from a vending machine"),
              row("closed", "二見公園：2026年9月24日〜2027年3月末は工事で立入禁止（吊橋へは迂回路。冬は閉鎖）", "Futami Park: closed for works 24 Sep 2026–end of Mar 2027 (detour to the bridge, closed in winter)", until="2027-03-31"),
              row("closed", "冬は積雪で二見吊橋まで行けません", "In winter snow blocks the way to the bridge")],
        notices=[notice("二見公園は工事中", "Futami Park is closed for works",
                        "2026年9月24日〜2027年3月末は、二見公園が立入禁止です。二見吊橋へは迂回路で行けますが、迂回路は冬は閉鎖、冬は雪で吊橋まで行けません。足湯は使えます。",
                        "Futami Park is closed from 24 September 2026 to the end of March 2027. A detour leads to the suspension bridge, but it closes in winter, and in winter snow blocks the way to the bridge anyway. The foot bath stays open.",
                        U["futami_notice"], to="2027-03-31")],
        tip=T("定山渓観光協会のページ（足湯・二見公園・工事のお知らせ）で2026年11月26日に確認しました。",
              "Checked on the Jozankei Tourist Association’s pages (foot bath, Futami Park, works notice) on 26 November 2026."),
        time=(VIS, "11:05〜11:45", "11:05–11:45")),

    dict(
        id="iwato", name=T("岩戸観音堂", "Iwato Kannon-do"), kind=T("洞窟のお堂", "Cave shrine"),
        blurb=T("お堂の奥の約120mの洞窟に、観音像が33体。外が雪でも雨でも見られます。",
                "A 120 m cave behind the hall, lined with 33 Kannon statues. Fine in snow or rain."),
        lat=42.96645, lng=141.16081,
        text=T("1936年に建てられたお堂です。本堂の奥から全長約120mの洞窟が続き、観音像が33体並んでいます。参拝は無料で、洞窟に入るのは大人300円・子ども100円。7:00〜20:00、1年中開いています。\n\n"
               "国道230号の章月グランドホテル前の交差点から入ります。二見の足湯から歩いて10分ほど。ここから次のお昼の店までは、温泉街を10分ほど歩きます。",
               "The hall was built in 1936. A cave about 120 m long runs back from it, lined with 33 statues of Kannon. Visiting the hall is free; the cave costs ¥300 for adults and ¥100 for children. Open 7:00–20:00 every day of the year.\n\n"
               "The entrance is at the junction on Route 230 in front of the Shogetsu Grand Hotel, about 10 minutes’ walk from the Futami foot bath. Lunch is another 10 minutes’ walk through the town."),
        gmaps=[gm("岩戸観音堂", "Iwato Kannon-do", 42.96645, 141.16081, "岩戸観音堂 定山渓")],
        links=[link("info", "岩戸観音堂（定山渓観光協会）", "Iwato Kannon-do (Jozankei Tourist Association)", U["iwato"]), JOZ],
        rows=[row("hours", "7:00〜20:00、年中無休", "7:00–20:00, every day"),
              row("fee", "参拝は無料。洞窟は大人300円・子ども100円（支払い方法は要確認）", "Hall free; cave ¥300 adults, ¥100 children (payment methods not confirmed)")],
        tip=T("定山渓観光協会のページで2026年11月26日に確認しました。歩く時間は地図で測った距離に、ゆとりを足した目安です。",
              "Checked on the Jozankei Tourist Association’s page on 26 November 2026. Walking times are map estimates with some slack."),
        time=(VIS, "11:50〜12:15", "11:50–12:15")),

    dict(
        id="lunch", name=T("温泉街でお昼", "Lunch in the town"), kind=T("お昼", "Lunch"),
        blurb=T("定食、手打ちのそば、昔ながらのラーメン、喫茶店のカツカレー。お店ごとに休みの曜日が違います。",
                "Set meals, handmade soba, old-style ramen or a café’s katsu curry. Each place closes on a different day."),
        caution=T("休みの曜日：いち＝火、紅葉亭＝水・木、可楽＝水", "Closed: Ichi Tue, 紅葉亭 Wed–Thu, 可楽 Wed"),
        lat=42.96880, lng=141.16560,
        text=T("お昼の例です。どの店も、支払い方法と英語のメニューの有無は要確認。\n\n"
               "・食堂いち：焼き鮭や炭焼き鶏など7種類の定食。11:00〜15:00、火曜休み（祝日・お盆・GW・正月は営業）。定山渓大橋のバス停から歩いて5分、風マチビルヂングの2階。\n"
               "・生そば紅葉亭：石臼で挽いた粉の手打ちそば。11:00〜17:00（そばがなくなりしだい終わり）、水・木曜休み。\n"
               "・ラーメン可楽：昔ながらのラーメンとチャーハン。昼11:00〜15:00・夜18:00〜23:00（火曜は夜なし）。水曜と第2・第4火曜休み。\n"
               "・喫茶＆軽食フランセ：サイフォンで淹れるコーヒーと、揚げたてのカツカレー。10:30〜17:00（ラストオーダー16:30）。\n\n"
               "食べたら、温泉街を通って定山源泉公園へ（10〜15分）。",
               "Some lunch options. For all of them, payment methods and English menus are not confirmed.\n\n"
               "• Shokudo Ichi: seven set meals, such as grilled salmon or charcoal-grilled chicken. 11:00–15:00, closed Tuesdays (open on holidays and in the Obon, Golden Week and New Year periods). 5 minutes’ walk from the Jozankei Ohashi bus stop, 2nd floor of the Kazemachi Building.\n"
               "• 紅葉亭 (soba): handmade soba from stone-ground flour. 11:00–17:00 (until the soba runs out), closed Wednesdays and Thursdays.\n"
               "• Ramen 可楽: old-style ramen and fried rice. 11:00–15:00 and 18:00–23:00 (no evening service on Tuesdays). Closed Wednesdays and the 2nd and 4th Tuesdays.\n"
               "• Café France: siphon coffee and freshly fried katsu curry. 10:30–17:00 (last order 16:30).\n\n"
               "Afterwards, walk through the town to Jozan Gensen Park (10–15 minutes)."),
        gmaps=[gm("食堂いち", "Shokudo Ichi", 42.96880, 141.16560, "食堂いち 定山渓"),
               gm("生そば紅葉亭", "紅葉亭 (soba)", 42.96600, 141.16400, "生そば紅葉亭 定山渓"),
               gm("ラーメン可楽", "Ramen 可楽", 42.96800, 141.16300, "ラーメン可楽 定山渓"),
               gm("喫茶＆軽食フランセ", "Café France", 42.96500, 141.16000, "喫茶フランセ 定山渓")],
        links=[link("info", "食堂いち", "Shokudo Ichi (Japanese)", U["ichi"]), link("info", "生そば紅葉亭", "紅葉亭 (soba, Japanese)", U["koyotei"]),
               link("info", "ラーメン可楽", "Ramen 可楽 (Japanese)", U["karaku"]), link("info", "喫茶＆軽食フランセ", "Café France (Japanese)", U["france"])],
        rows=[row("food", "いち 11:00〜15:00（火休）／紅葉亭 11:00〜17:00（水・木休）／可楽 11:00〜15:00（水・第2第4火休）／フランセ 10:30〜17:00",
                  "Ichi 11:00–15:00 (closed Tue) / 紅葉亭 11:00–17:00 (closed Wed–Thu) / 可楽 11:00–15:00 (closed Wed, 2nd & 4th Tue) / France 10:30–17:00")],
        tip=T("お店の時間と休みは、定山渓観光協会の店の紹介ページで2026年11月26日に確認しました。臨時の休みは店に確かめてください。",
              "Hours and closing days from the Jozankei Tourist Association’s shop pages, checked on 26 November 2026. Ask the shop about irregular closures."),
        time=(VIS, "12:25〜13:20", "12:25–13:20")),

    dict(
        id="gensen", name=T("定山源泉公園", "Jozan Gensen Park"), kind=T("足湯・温泉卵", "Foot bath & onsen eggs"),
        blurb=T("源泉の足湯と、温泉卵をつくる湯つぼ。卵は向かいの物産館で3個180円、約20分でできあがり。",
                "A hot-spring foot bath and a spring pot for cooking eggs. Buy 3 eggs for ¥180 opposite; ready in about 20 minutes."),
        lat=42.96500, lng=141.16324,
        text=T("月見橋のたもとにある無料の足湯公園です。7:00〜21:00、1年中開いています。足湯は入る条件が書かれていないので、だれでも入れます。冬は雪の中の足湯になります。足をふくタオルを持っていきましょう。\n\n"
               "温泉卵：川の向かいの定山渓物産館（8:00〜21:00、不定休。湯の町のバス停のすぐ前）で「温泉卵セット」（卵3個とネット、180円）を買い、公園の「おんたまの湯」に入れて約20分。物産館で、その日のちょうどいいゆで時間を聞けます。季節によってはカラスが卵をねらうので、目を離さないで。\n\n"
               "時間があれば、近くの無料の足湯「足のふれあい太郎の湯」や、かっぱ像に湯を注ぐ「かっぱ家族の願かけ手湯」、歩いて4分ほどの定山渓神社へ。",
               "A free foot-bath park at the end of Tsukimi bridge, open 7:00–21:00 all year. No conditions are listed for the foot bath, so anyone can use it. In winter it is a foot bath in the snow. Bring a small towel.\n\n"
               "Onsen eggs: across the river at the Jozankei Bussankan shop (8:00–21:00, irregular closures, right by the Yunomachi bus stop), buy the onsen-egg set (3 eggs and a net, ¥180), then lower it into the park’s egg pot for about 20 minutes. The shop can tell you the right time for the day. Depending on the season, crows go for the eggs, so keep an eye on them.\n\n"
               "With time to spare, try the free Taro-no-yu foot bath nearby, the kappa hand bath where you pour hot water over the kappa statues, or Jozankei Shrine, about 4 minutes away on foot."),
        gmaps=[gm("定山源泉公園", "Jozan Gensen Park", 42.96500, 141.16324, "定山源泉公園"),
               gm("定山渓物産館", "Jozankei Bussankan", 42.96537, 141.16217, "定山渓物産館")],
        links=[link("info", "定山源泉公園", "Jozan Gensen Park (Japanese)", U["gensen"]), link("info", "おんたまの湯（温泉卵）", "Onsen egg pot (Japanese)", U["ontama"]),
               link("info", "定山渓物産館", "Jozankei Bussankan (Japanese)", U["bussankan"])],
        rows=[row("hours", "足湯・おんたまの湯 7:00〜21:00、通年／物産館 8:00〜21:00（不定休）", "Foot bath and egg pot 7:00–21:00 all year / Bussankan 8:00–21:00 (irregular closures)"),
              row("fee", "足湯は無料。温泉卵セット（卵3個＋ネット）180円", "Foot bath free. Egg set (3 eggs + net) ¥180")],
        tip=T("定山渓観光協会のページ（定山源泉公園・おんたまの湯・定山渓物産館）で2026年11月26日に確認しました。",
              "Checked on the Jozankei Tourist Association’s pages (park, egg pot, Bussankan) on 26 November 2026."),
        time=(VIS, "13:35〜14:30（14:34のバスへ）", "13:35–14:30 (for the 14:34 bus)")),

    dict(
        id="hoheikyo", name=T("豊平峡温泉", "Hoheikyo Onsen"), kind=T("日帰り入浴・インドカレー", "Day bath & Indian curry"),
        blurb=T("大きな露天風呂と、インド料理の食堂がある日帰り専用の温泉。お風呂は21:45まで受付。",
                "A day-use hot spring with big outdoor baths and an Indian restaurant. Last entry 21:45."),
        caution=T("タトゥー：公式サイトに記載なし（要確認・電話011-598-2410）", "Tattoos: not mentioned on the website (phone 011-598-2410)"),
        lat=42.94964, lng=141.15615,
        text=T("タトゥー：公式サイトにタトゥーの決まりは書かれていません。入れるかどうかは、行く前に電話で確かめてください（011-598-2410）。定山渓のほかの日帰り入浴は、公式サイトでタトゥーを断っているところが多いので、だめなときは足湯（二見の足湯・定山源泉公園）を中心にしてください。\n\n"
               "温泉街から2.6kmほど奥にある、泊まれない日帰り専用の温泉です。定山渓湯の町14:34発（土日祝は14:33発）の12番「豊平峡温泉」行きで16分、200円。歩くと30分あまりかかり、冬の車道ぞいはすすめません。温泉街でもう少し過ごすなら、次は15:32発（土日祝15:29発）。\n\n"
               "お風呂：男女別の内風呂と露天風呂（露天は日によって男女が入れ替わります）。ボディソープとリンスインシャンプーはあります。タオルは売っています（ロゴ入りタオル220円、バスタオル500円）。家族風呂・貸切風呂はありません。10:00〜22:30（最終受付21:45）、大人1,300円・子ども600円、年中無休（臨時休業の日あり）。支払いは現金・クレジットカード・QRコード決済。\n\n"
               "食事：インド料理は11:00〜21:00（ラストオーダー）。カレーはチキン1,200円、ラム1,400円など。和食（そば・ジンギスカンなど）は11:00〜14:00と17:00〜20:00（ラストオーダー）。\n\n"
               "帰り：豊平峡温泉18:30発の12番で真駒内駅へ、地下鉄に乗り換えてすすきの19:51着。最後は20:00発で、すすきの21:12着（土日祝21:20着）。運賃はバス850円と地下鉄290円。土日祝の18:30発は1月1日、20:00発は12月31日〜1月3日は運休です。札幌駅へ直行のかっぱライナー号（予約制）は17:00発が最後で、札幌駅18:19着。\n\n"
               "雪のない季節は、ここから電気バスで豊平峡ダムへ行けます（定山渓観光協会の案内では5月2日〜11月3日、8:45〜16:00、大人1,000円。2027年の期間は要確認）。",
               "Tattoos: the website says nothing about tattoos, so phone before you go to ask whether you can bathe (011-598-2410). Most other day baths in Jozankei refuse tattoos on their websites; if this one does too, make the foot baths (Futami and Jozan Gensen Park) the core of your day.\n\n"
               "This day-use-only hot spring (no rooms) is about 2.6 km up the valley from the town. Take the No. 12 bus for Hoheikyo Onsen from Jozankei Yunomachi at 14:34 (14:33 at weekends and on holidays): 16 minutes, ¥200. Walking takes over 30 minutes along the road, not advised in winter. For more time in town, the next bus is at 15:32 (15:29 at weekends).\n\n"
               "Baths: separate indoor and outdoor baths for men and women (the outdoor baths swap sides by date). Body soap and shampoo are provided. Towels are sold (small towel ¥220, bath towel ¥500). No family or private baths. 10:00–22:30 (last entry 21:45), adults ¥1,300, children ¥600, open every day except occasional closures. Cash, credit cards and QR payments.\n\n"
               "Food: the Indian restaurant serves 11:00–21:00 (last order), with curries such as chicken ¥1,200 or lamb ¥1,400. The Japanese menu (soba, lamb barbecue and more) is served 11:00–14:00 and 17:00–20:00 (last orders).\n\n"
               "Back to town: the No. 12 at 18:30 to Makomanai, then the subway, reaches Susukino at 19:51. The last bus is at 20:00, arriving Susukino 21:12 (21:20 at weekends and on holidays). Fares: bus ¥850, subway ¥290. At weekends and on holidays the 18:30 does not run on 1 January and the 20:00 not on 31 December–3 January. The last direct Kappa Liner (reservation) to Sapporo Station leaves at 17:00 (arrives 18:19).\n\n"
               "When there is no snow, an electric bus runs from here to Hoheikyo Dam (per the tourist association: 2 May–3 November, 8:45–16:00, adults ¥1,000; check the 2027 dates)."),
        gmaps=[gm("豊平峡温泉", "Hoheikyo Onsen", 42.94964, 141.15615, "豊平峡温泉")],
        links=[link("official", "豊平峡温泉 公式サイト", "Hoheikyo Onsen (official, Japanese)", U["hoheikyo"]),
               link("official", "豊平峡温泉 温泉の案内", "Hoheikyo Onsen: baths (Japanese)", U["hoheikyo_onsen"]),
               link("timetable", "豊平峡温泉のバス時刻表（PDF）", "Hoheikyo Onsen bus stop timetable (PDF)", U["jt_hoheikyo"])],
        rows=[row("tattoo", "公式サイトに記載なし（要確認・電話011-598-2410）", "Not mentioned on the website (phone 011-598-2410)"),
              row("hours", "お風呂 10:00〜22:30（最終受付21:45）、年中無休", "Baths 10:00–22:30 (last entry 21:45), open every day"),
              row("fee", "大人1,300円・子ども600円。タオル220円・バスタオル500円（販売）", "Adults ¥1,300, children ¥600. Towel ¥220, bath towel ¥500 (for sale)"),
              row("food", "インド料理 11:00〜21:00（L.O.）／和食 11:00〜14:00・17:00〜20:00（L.O.）", "Indian 11:00–21:00 (last order) / Japanese 11:00–14:00, 17:00–20:00 (last orders)"),
              row("bus", "行き：湯の町14:34（土日祝14:33）→ 14:50、200円。帰り：18:30・20:00発（真駒内へ）", "There: Yunomachi 14:34 (14:33 weekends) → 14:50, ¥200. Back: 18:30 or 20:00 (to Makomanai)")],
        notices=[N_TATTOO_J],
        tip=T("豊平峡温泉の公式サイト、定山渓観光協会のページ、じょうてつバスの時刻表、乗換案内（2026年12月3日・5日）で2026年11月26日に確認しました。",
              "Checked on 26 November 2026 on Hoheikyo Onsen’s website, the Jozankei Tourist Association’s pages, Jotetsu Bus timetables and a route planner (3 and 5 December 2026)."),
        time=(VIS, "14:50〜20:00（お風呂と晩ごはん）", "14:50–20:00 (bath and dinner)")),

    dict(
        id="yoru", name=T("夜の温泉街で晩ごはん", "Dinner in town"), kind=T("晩ごはん・帰り", "Dinner & ride back"),
        blurb=T("温泉街で食べて、20:53（土日祝20:45）の札幌駅行きで帰る。1月20日〜2月28日は雪灯路も。",
                "Eat in town and ride the 20:53 (20:45 weekends) back to Sapporo Station. Snow lanterns 20 January–28 February."),
        lat=42.96543, lng=141.16199,
        text=T("豊平峡温泉に行かない日か、豊平峡温泉18:30発のバスで温泉街へ戻った日（湯の町18:41着、200円）に。晩ごはんの例です（支払い方法は要確認）。\n\n"
               "・松尾ジンギスカン：17:00〜22:00（ラストオーダー21:30）、不定休。\n"
               "・ラーメン可楽：夜は18:00〜23:00（火曜は夜なし、水曜と第2・第4火曜休み）。\n"
               "・食堂こんの：しょうゆ・しお・みそのラーメン。18:00〜0:00、不定休。\n"
               "・居酒屋北のかっぱ：18:00〜24:00、水・日曜休み。\n\n"
               "雪灯路（ゆきとうろ）：2027年1月20日〜2月28日の18:00〜21:30（最終入場21:15）は、温泉街に雪の灯りが並びます。無料。定山渓神社の会場は、泊まる人だけの招待制です。天気で中止や短縮のときは、当日の14:00ごろに定山渓観光協会のサイトとSNSで案内があります。\n\n"
               "帰り：定山渓湯の町20:53発（土日祝は20:45発）の快速8番が札幌駅まで乗り換えなしで、札幌駅のJRの駅まで22:13ごろ（土日祝22:04ごろ）、1,000円。交通系ICカードが使えます。これを逃したら、最後は21:50発の12番で真駒内へ、地下鉄に乗り換えてすすきの22:58着（1,040円）。土日祝の20:45と21:50は、12月31日〜1月3日は運休です。",
               "For a day without Hoheikyo, or after taking the 18:30 bus back from Hoheikyo Onsen (Yunomachi 18:41, ¥200). Some dinner options (payment methods not confirmed):\n\n"
               "• Matsuo Jingisukan (lamb barbecue): 17:00–22:00 (last order 21:30), irregular closures.\n"
               "• Ramen 可楽: evenings 18:00–23:00 (none on Tuesdays; closed Wednesdays and the 2nd and 4th Tuesdays).\n"
               "• Shokudo Konno: soy, salt or miso ramen. 18:00–0:00, irregular closures.\n"
               "• Izakaya Kita no Kappa: 18:00–24:00, closed Wednesdays and Sundays.\n\n"
               "Yukitouro snow lanterns: 20 January–28 February 2027, 18:00–21:30 (last entry 21:15), lanterns line the town. Free. The Jozankei Shrine venue is by invitation for hotel guests only. If weather cancels or shortens it, the tourist association posts a notice on its website and social media at about 14:00 that day.\n\n"
               "Back: the rapid No. 8 from Jozankei Yunomachi at 20:53 (20:45 at weekends and on holidays) goes straight to Sapporo Station; you are at the JR station by about 22:13 (22:04 at weekends). ¥1,000, IC cards OK. Missed it? The last option is the No. 12 at 21:50 to Makomanai, then the subway to Susukino (22:58, ¥1,040). At weekends and on holidays the 20:45 and 21:50 do not run on 31 December–3 January."),
        gmaps=[gm("定山渓湯の町（バス停）", "Jozankei Yunomachi bus stop", 42.96543, 141.16199, "定山渓湯の町 バス停"),
               gm("松尾ジンギスカン 定山渓店", "Matsuo Jingisukan Jozankei", 42.96600, 141.16450, "松尾ジンギスカン 定山渓")],
        links=[link("info", "松尾ジンギスカン", "Matsuo Jingisukan (Japanese)", U["matsuo"]), link("info", "食堂こんの", "Shokudo Konno (Japanese)", U["konno"]),
               link("info", "居酒屋北のかっぱ", "Kita no Kappa (Japanese)", U["kappa_izakaya"]),
               link("info", "新・雪灯路2027", "Yukitouro 2027 snow lanterns (Japanese)", U["yukitouro"]),
               link("timetable", "定山渓湯の町のバス時刻表（PDF）", "Jozankei Yunomachi bus timetable (PDF)", U["jt_yunomachi"])],
        rows=[row("food", "松尾ジンギスカン 17:00〜22:00（L.O.21:30）／可楽 18:00〜23:00／こんの 18:00〜0:00／北のかっぱ 18:00〜24:00（水・日休）",
                  "Matsuo 17:00–22:00 (LO 21:30) / 可楽 18:00–23:00 / Konno 18:00–0:00 / Kita no Kappa 18:00–24:00 (closed Wed, Sun)"),
              row("bus", "湯の町20:53（土日祝20:45）→ 札幌駅、1,000円。最後は21:50発の12番（すすきの22:58着）", "Yunomachi 20:53 (20:45 weekends) → Sapporo Station, ¥1,000. Last: No. 12 at 21:50 (Susukino 22:58)")],
        notices=[notice("雪灯路（1月20日〜2月28日）", "Yukitouro snow lanterns (20 Jan–28 Feb)",
                        "18:00〜21:30（最終入場21:15）、無料。定山渓神社の会場は泊まる人だけ。中止・短縮は当日14:00ごろに定山渓観光協会のサイトで。",
                        "18:00–21:30 (last entry 21:15), free. The shrine venue is for hotel guests only. Cancellations are posted on the tourist association’s website at about 14:00 that day.",
                        U["yukitouro"], start="2026-12-01", to="2027-02-28")] + N_ICE,
        tip=T("お店の時間は定山渓観光協会の店の紹介ページ、雪灯路は定山渓観光協会、バスはじょうてつバスの時刻表と乗換案内（2026年12月3日・5日）で、2026年11月26日に確認しました。",
              "Shop hours from the Jozankei Tourist Association’s pages, Yukitouro from the association, buses from Jotetsu’s timetables and a route planner (3 and 5 December 2026), all checked on 26 November 2026."),
        time=(VIS, "18:00〜20:50（晩ごはん）", "18:00–20:50 (dinner)")),
]

# ---------------------------------------------------------------------------
# 登別のコース
# ---------------------------------------------------------------------------
N_TATTOO_N = notice(
    "タトゥーがある人へ", "If you have tattoos",
    "登別万世閣は、公式サイトでタトゥー（タトゥーシールやペイントも）の入浴を断っています。夢元さぎり湯と第一滝本館は、公式サイトにタトゥーの決まりが書かれていません（要確認）。行く前に電話で確かめてください（さぎり湯 0143-84-2050）。大湯沼川の天然足湯は無料で、入る条件の記載はありません。",
    "Noboribetsu Manseikaku refuses bathers with tattoos (tattoo stickers and body paint included) on its website. Sagiriyu and Dai-ichi Takimotokan say nothing about tattoos on their websites, so phone before you go (Sagiriyu 0143-84-2050). The natural foot bath on the Oyunuma river is free and lists no conditions.",
    U["mansei"])

NOBORIBETSU = [
    dict(
        id="nstart", name=T("札幌駅から特急で登別へ", "Sapporo to Noboribetsu"), kind=T("出発・特急とバス", "Start: express & bus"),
        blurb=T("札幌9:45発の特急北斗で登別10:59着。駅前から道南バスで登別温泉へ。", "The 9:45 Hokuto from Sapporo reaches Noboribetsu at 10:59; a Donan bus takes you up to the onsen town."),
        caution=T("特急は全席指定。バスは現金450円", "All limited-express seats reserved; bus ¥450 cash"),
        lat=43.06866, lng=141.35079,
        text=T("登別（のぼりべつ）温泉は、札幌から南へ約110km、太平洋に近い山の中の温泉街です。\n\n"
               "行き：JR札幌駅9:45発の特急北斗8号（函館行き）で、登別10:59着（平日・土日とも）。運賃は乗車券2,530円と指定席2,360円で4,890円（2026年12月3日・5日の額）。北海道の特急はすべての席が指定席なので、乗る前に指定席をとります。\n\n"
               "登別駅前から、道南バスの登別温泉行き11:13発に乗り、終点の登別温泉ターミナルで降ります。11:32着、450円。このバスは中ドアから乗って整理券を取り、降りるときに払います。現金の小銭を用意してください（交通系ICカードが使えるかは要確認）。ひとつ早い特急すずらん4号（札幌9:21発、登別10:39着）なら、10:44発のバスで登別温泉11:05着です。\n\n"
               "レールパス：北海道レールパスと「札幌−登別エリアパス」（どちらも日本以外のパスポートを持つ人向け）で、特急の指定席に乗れます。エリアパスは4日間で10,000円（事前に買う場合）、駅で買うと11,000円。道南バスはパスの対象外です。\n\n"
               "札幌から登別温泉へ直行する高速おんせん号（予約制）は、札幌駅前13:40発の1日1本だけなので、日帰りには向きません。\n\n"
               "荷物：登別温泉の手荷物預かり（登別国際観光コンベンション協会、1個500〜700円、英語も可）は16:30（窓口17:00）までなので、夜まで残る日は、大きな荷物は札幌のホテルに置いてきてください。",
               "Noboribetsu Onsen is a hot-spring town in the hills near the Pacific, about 110 km south of Sapporo.\n\n"
               "Getting there: the limited express Hokuto 8 (for Hakodate) leaves JR Sapporo Station at 9:45 and reaches Noboribetsu at 10:59, weekdays and weekends. The fare is ¥2,530 plus ¥2,360 for the reserved seat, ¥4,890 in total (prices for 3 and 5 December 2026). Every seat on Hokkaido’s limited expresses is reserved, so get a seat reservation before you board.\n\n"
               "From the station, take the Donan bus for Noboribetsu Onsen at 11:13 to the last stop, Noboribetsu Onsen Terminal: arrives 11:32, ¥450. On this bus you board by the middle door, take a numbered ticket and pay when you get off. Have coins ready (IC cards not confirmed). One train earlier, the Suzuran 4 (Sapporo 9:21, Noboribetsu 10:39), connects with the 10:44 bus (Noboribetsu Onsen 11:05).\n\n"
               "Rail passes: the Hokkaido Rail Pass and the Sapporo–Noboribetsu Area Pass (both for holders of non-Japanese passports) cover reserved seats on limited expresses. The Area Pass costs ¥10,000 for 4 days if bought in advance, ¥11,000 at the station. Donan buses are not covered.\n\n"
               "The direct Onsen-go highway bus (reservation) leaves Sapporo only once a day, at 13:40, so it does not suit a day trip.\n\n"
               "Luggage: the left-luggage desk in Noboribetsu Onsen (tourism association, ¥500–700 per item, English spoken) closes at 16:30 (counter 17:00). If you stay into the evening, leave big bags at your Sapporo hotel."),
        gmaps=[gm("JR札幌駅", "JR Sapporo Station", 43.06866, 141.35079, "JR札幌駅"),
               gm("JR登別駅", "JR Noboribetsu Station", 42.45201, 141.18080, "JR登別駅")],
        links=[JR, PASS, DONAN, link("info", "登別温泉の手荷物預かり", "Left luggage in Noboribetsu Onsen (Japanese)", U["nb_luggage"])],
        rows=[row("train", "札幌9:45（北斗8号）→ 登別10:59。すずらん4号なら9:21 → 10:39（平日・土日とも）", "Sapporo 9:45 (Hokuto 8) → Noboribetsu 10:59; or Suzuran 4, 9:21 → 10:39 (every day)"),
              row("fee", "札幌〜登別 4,890円（乗車券2,530円＋指定席2,360円。12月3日・5日の額）", "Sapporo–Noboribetsu ¥4,890 (fare ¥2,530 + reserved seat ¥2,360, on 3 and 5 Dec)"),
              row("bus", "登別駅前11:13 → 登別温泉11:32（10:44 → 11:05も）、450円・現金", "Noboribetsu Station 11:13 → Noboribetsu Onsen 11:32 (also 10:44 → 11:05), ¥450 cash")],
        notices=N_ICE,
        cash=True,
        tip=T("列車は乗換案内（2026年12月3日・5日のダイヤ。JR北海道は2027年3月にダイヤ改正の予定）、バスは道南バスの公式の時刻表（2026年10月1日改正）、パスはJR北海道の英語のページで確認しました。",
              "Trains from a route planner (timetable for 3 and 5 December 2026; JR Hokkaido is expected to revise it in March 2027), buses from Donan Bus’s timetable (revised 1 October 2026), passes from JR Hokkaido’s English pages."),
        time=(DEP, "9:45発（札幌駅に9:30ごろ）", "the 9:45 (be at Sapporo Station by about 9:30)")),

    dict(
        id="nlunch", name=T("極楽通りと閻魔堂", "Gokuraku-dori & Enma-do"), kind=T("お昼・からくり", "Lunch & Enma show"),
        blurb=T("温泉街のまん中の坂道でお昼。食べたら、閻魔堂の閻魔大王のからくりを13:00の回で。",
                "Lunch on the main street, then the mechanical King of Hell at Enma-do at 13:00."),
        lat=42.49300, lng=141.14350,
        text=T("バスを降りたら、温泉街のまん中の坂道「極楽通り」を地獄谷のほうへ上ります。お昼の例です（支払い方法・英語のメニューは要確認）。\n\n"
               "・味の大王 登別温泉店：辛さに挑戦する「地獄ラーメン」。11:30〜15:00、火曜休み。\n"
               "・ラーメン天鳳：長く煮たみそのスープのラーメン。シカ肉・クマ肉の煮込みも。11:30〜14:00、不定休。\n"
               "・温泉市場：登別の近海の魚介を刺身や炭焼きで。食事は11:00〜21:00、不定休。\n"
               "・adex BAKERY&CAFE：毎日焼くパンのカフェ。8:00〜22:00、無休。\n\n"
               "閻魔堂（えんまどう）：極楽通りの上のほうにあるお堂で、中の「閻魔大王からくり山車」が10:00・11:00・13:00・15:00・17:00・20:00・21:00に動きます。無料。天気によってお堂を閉めることがあります。食べ終わったら13:00の回へ。",
               "From the bus, walk up Gokuraku-dori, the sloping main street, towards Jigokudani. Some lunch options (payment methods and English menus not confirmed):\n\n"
               "• Aji no Daio: “hell ramen” with a heat level you choose. 11:30–15:00, closed Tuesdays.\n"
               "• Ramen 天鳳: ramen in a long-simmered miso broth, plus venison and bear stew. 11:30–14:00, irregular closures.\n"
               "• Onsen Ichiba: local seafood as sashimi or charcoal-grilled. Meals 11:00–21:00, irregular closures.\n"
               "• adex Bakery & Café: bread baked daily. 8:00–22:00, open every day.\n\n"
               "Enma-do: a small hall near the top of Gokuraku-dori. The mechanical float of Enma, King of Hell, inside performs at 10:00, 11:00, 13:00, 15:00, 17:00, 20:00 and 21:00. Free. The hall may close in bad weather. After lunch, catch the 13:00 show."),
        gmaps=[gm("味の大王 登別温泉店", "Aji no Daio Noboribetsu Onsen", 42.49300, 141.14320, "味の大王 登別温泉店"),
               gm("ラーメン天鳳", "Ramen 天鳳", 42.49300, 141.14350, "ラーメン天鳳 登別温泉"),
               gm("温泉市場", "Onsen Ichiba", 42.49320, 141.14350, "温泉市場 登別温泉"),
               gm("adex BAKERY&CAFE", "adex Bakery & Café", 42.49250, 141.14300, "adex BAKERY&CAFE 登別"),
               gm("閻魔堂", "Enma-do", 42.49414, 141.14389, "閻魔堂 登別温泉")],
        links=[link("info", "閻魔堂", "Enma-do (Japanese)", U["enma"]), link("info", "味の大王 登別温泉店", "Aji no Daio (Japanese)", U["daio"]), link("info", "ラーメン天鳳", "Ramen 天鳳 (Japanese)", U["tenho"]),
               link("info", "温泉市場", "Onsen Ichiba (Japanese)", U["ichiba"]), link("info", "adex BAKERY&CAFE", "adex Bakery & Café (Japanese)", U["adex"])],
        rows=[row("food", "味の大王 11:30〜15:00（火休）／天鳳 11:30〜14:00／温泉市場 11:00〜21:00／adex 8:00〜22:00",
                  "Aji no Daio 11:30–15:00 (closed Tue) / 天鳳 11:30–14:00 / Onsen Ichiba 11:00–21:00 / adex 8:00–22:00"),
              row("hours", "閻魔堂のからくり：10:00・11:00・13:00・15:00・17:00・20:00・21:00（無料）", "Enma-do shows: 10:00, 11:00, 13:00, 15:00, 17:00, 20:00, 21:00 (free)")],
        tip=T("お店の時間と閻魔堂は、登別国際観光コンベンション協会の紹介ページで2026年11月26日に確認しました。臨時の休みは店に確かめてください。",
              "Shop hours and Enma-do from the Noboribetsu tourism association’s pages, checked on 26 November 2026. Ask shops about irregular closures."),
        time=(VIS, "11:35〜13:05（閻魔堂は13:00の回）", "11:35–13:05 (Enma-do at 13:00)")),

    dict(
        id="sengen", name=T("泉源公園の間欠泉", "Sengen Park geyser"), kind=T("間欠泉", "Geyser"),
        blurb=T("地獄谷から流れてくる湯の川ぞいの小さな公園。約3時間おきに、音を立てて湯が噴き上がります。",
                "A small park on the hot stream from Jigokudani, where a geyser roars up about every three hours."),
        lat=42.49489, lng=141.14367,
        text=T("極楽通りのいちばん上、地獄谷へ向かう坂の入口にあります。地獄谷から流れる温泉の川を使った間欠泉で、約3時間おきに大きな音と湯気を上げて噴き出します。無料。噴く時間に当たらなくても、湯けむりは見られます。ここから地獄谷までは坂を上って約10分。",
               "At the top of Gokuraku-dori, where the road climbs to Jigokudani. The geyser is fed by the hot stream from the valley and erupts with a roar and a cloud of steam about every three hours. Free. Even if you miss an eruption, the steam is there. Jigokudani is about 10 minutes uphill from here."),
        gmaps=[gm("泉源公園", "Sengen Park", 42.49489, 141.14367, "泉源公園 登別温泉")],
        links=[link("info", "泉源公園の間欠泉", "Sengen Park geyser (Japanese)", U["sengen"]), NB],
        rows=[row("fee", "無料", "Free")],
        tip=T("登別国際観光コンベンション協会のページで2026年11月26日に確認しました。", "Checked on the Noboribetsu tourism association’s page on 26 November 2026."),
        time=(VIS, "13:05〜13:15", "13:05–13:15")),

    dict(
        id="jigoku", name=T("地獄谷", "Jigokudani (Hell Valley)"), kind=T("火口の谷", "Volcanic valley"),
        blurb=T("直径約450mの火口のあと。谷のあちこちから湯気が上がり、木道で中ほどの鉄泉池まで歩けます。無料。",
                "An old crater about 450 m across, steaming all over. A boardwalk leads into the middle to Tessen-ike. Free."),
        lat=42.49816, lng=141.14964,
        text=T("直径約450mの爆裂火口のあとで、谷のあちこちから湯気と温泉が噴き出し、1日に約1万トンの湯が湧いています。入場は無料。\n\n"
               "入口のパークサービスセンターから展望台までは、車いす用のスロープ（勾配は最大8%）。展望台から木道を下ると、谷のほぼ中央の鉄泉池（てっせんいけ）という小さな間欠泉まで行けます。\n\n"
               "冬：木道と坂は凍ります。滑りにくい靴で、手すりを持って歩いてください。",
               "An explosion crater about 450 m across: from all over the valley, steam and hot water burst out, some 10,000 tonnes of it a day. Entry is free.\n\n"
               "A wheelchair slope (up to 8% gradient) runs from the Park Service Center at the entrance to the viewpoint. From there a boardwalk drops into the valley to Tessen-ike, a small geyser near its centre.\n\n"
               "Winter: the boardwalk and slopes ice over. Wear shoes with grip and hold the handrails."),
        gmaps=[gm("地獄谷 展望台", "Jigokudani viewpoint", 42.49700, 141.14800, "登別地獄谷 展望台"),
               gm("鉄泉池", "Tessen-ike", 42.49816, 141.14964, "鉄泉池 登別")],
        links=[link("info", "地獄谷（登別国際観光コンベンション協会）", "Jigokudani (Japanese)", U["jigoku"]), NB],
        rows=[row("fee", "無料", "Free")],
        notices=N_ICE,
        tip=T("登別国際観光コンベンション協会のページ（地獄谷・鉄泉池）で2026年11月26日に確認しました。", "Checked on the Noboribetsu tourism association’s pages on 26 November 2026."),
        time=(VIS, "13:25〜14:00", "13:25–14:00")),

    dict(
        id="oyunuma", name=T("大湯沼と天然足湯", "Oyunuma & natural foot bath"), kind=T("沼・天然の足湯", "Pond & foot bath"),
        blurb=T("地獄谷の奥の遊歩道で大湯沼へ。下りの途中、温泉の川に足を入れる無料の天然足湯。",
                "A trail beyond Jigokudani to the steaming Oyunuma pond, then down to a free foot bath in a hot river."),
        caution=T("冬は遊歩道が通行止めになることがあります（期間は要確認）", "Trails may close in winter (dates not confirmed)"),
        lat=42.50099, lng=141.14737,
        text=T("地獄谷から遊歩道を上って大湯沼展望台へ（約1.3km、上り坂）。大湯沼は、日和山（ひよりやま）の水蒸気爆発でできた火口のあとの、周囲約1kmのひょうたん形の沼。沼の底から約130℃の硫黄泉が噴き出しています。\n\n"
               "展望台から大湯沼川探勝歩道を下ると、大正地獄のすぐ近くに「大湯沼川天然足湯」。大湯沼からあふれた湯が流れる川に、そのまま足を入れます。無料で、入る条件は書かれていないので、タトゥーがあっても入れます。足をふくタオルを持っていきましょう。足湯から温泉街までは、歩いて約1.5km・25分ほど。全部で約3.3km、ゆっくり歩いて1時間半を見てください。\n\n"
               "冬：遊歩道は冬に通行止めになることがあります（北海道観光機構の案内。期間は出ていません）。通れない日は、かわりにロープウェイでクマ牧場へ（「選んで回る」で入れ替え）。道の状況は登別国際観光コンベンション協会へ（0143-84-3311）。",
               "From Jigokudani a trail climbs to the Oyunuma viewpoint (about 1.3 km, uphill). Oyunuma, a crater left by a steam explosion of Mt Hiyori, is a gourd-shaped pond about 1 km round, with sulphurous water at around 130°C gushing up from the bottom.\n\n"
               "From the viewpoint, the Oyunuma river trail goes down past Taisho Jigoku to the natural foot bath, where the overflow from the pond runs as a hot river and you put your feet straight in. It is free and lists no conditions, so tattoos are not an issue. Bring a towel. From the foot bath it is about 1.5 km, 25 minutes, back to town. Allow about 1½ hours for the whole 3.3 km at an easy pace.\n\n"
               "Winter: the trails can close in winter (per the Hokkaido Tourism Organization; no dates given). If they are closed, take the ropeway to the Bear Park instead (swap it in with “Choose stops”). For trail conditions, call the tourism association (0143-84-3311)."),
        gmaps=[gm("大湯沼展望台", "Oyunuma viewpoint", 42.50099, 141.14737, "大湯沼展望台 登別"),
               gm("大湯沼川天然足湯", "Oyunuma river natural foot bath", 42.50210, 141.14333, "大湯沼川天然足湯")],
        links=[link("info", "大湯沼川天然足湯", "Natural foot bath (Japanese)", U["ashiyu"]),
               link("info", "大湯沼（モデルコース）", "Oyunuma (Japanese)", U["oyu_course"]),
               link("info", "冬の遊歩道（北海道観光機構）", "Winter trail note (Japanese)", U["ashiyu_winter"])],
        rows=[row("fee", "無料", "Free"),
              row("closed", "冬は遊歩道の通行止めあり（期間は要確認）", "Trails may close in winter (dates not confirmed)")],
        notices=winters("冬は遊歩道が通行止めのことがあります", "Winter trail closures",
                        "大湯沼・天然足湯への遊歩道は、冬に通行止めになることがあります。行く前に登別国際観光コンベンション協会（0143-84-3311）か、地獄谷の入口のパークサービスセンターで確かめてください。通れない日は、クマ牧場へ。",
                        "The trails to Oyunuma and the foot bath can close in winter. Check with the tourism association (0143-84-3311) or the Park Service Center at the Jigokudani entrance first. If they are closed, go to the Bear Park instead.",
                        U["ashiyu_winter"]),
        tip=T("登別国際観光コンベンション協会のページ（大湯沼・天然足湯・モデルコース）と北海道観光機構のページで確認しました。距離は地図で測ったもので、時間はゆとりを足した目安です。",
              "From the Noboribetsu tourism association’s pages and the Hokkaido Tourism Organization’s page. Distances measured on a map; times include some slack."),
        time=(VIS, "14:00〜15:30", "14:00–15:30")),

    dict(
        id="bear", name=T("のぼりべつクマ牧場", "Noboribetsu Bear Park"), kind=T("ロープウェイ・クマ", "Ropeway & bears"),
        blurb=T("ロープウェイで約7分、山の上でヒグマを近くで見ます。雪の日も開いています。冬は最終入園15:50。",
                "A 7-minute ropeway ride up to see brown bears close by. Open in snow. Winter last entry 15:50."),
        caution=T("冬（10月21日〜4月20日）は最終入園15:50", "Winter (21 Oct–20 Apr) last entry 15:50"),
        lat=42.49309, lng=141.14434,
        text=T("温泉街の中ほどにあるロープウェイの山麓駅（バスターミナルから歩いて5分ほど）から、山頂駅まで片道約7分。入園料にロープウェイの往復が入っていて、大人3,200円・子ども1,600円（4歳〜小学生）。見学は60〜90分。\n\n"
               "10月21日〜4月20日は9:30〜16:30（最終入園15:50）、4月21日〜10月20日は9:00〜17:00（最終入園16:20）。雪の日も入れます。支払いは現金・クレジットカード・交通系ICカード・QRコード決済など。山麓駅の正面入口の右にコインロッカー（300円・200円）があります。\n\n"
               "大湯沼の遊歩道のかわりに入れる場所です。両方は時間が足りません。2027年4月5日〜23日はロープウェイの点検で休みです。",
               "The ropeway from the base station in the middle of town (about 5 minutes’ walk from the bus terminal) takes about 7 minutes to the top. Admission includes the return ride: adults ¥3,200, children ¥1,600 (age 4 to primary school). Allow 60–90 minutes.\n\n"
               "Open 9:30–16:30 from 21 October to 20 April (last entry 15:50), 9:00–17:00 from 21 April to 20 October (last entry 16:20). Open in snow. Cash, credit cards, IC cards and QR payments. Coin lockers (¥300 and ¥200) are to the right of the base station’s main entrance.\n\n"
               "This replaces the Oyunuma trail; there is not time for both. Closed 5–23 April 2027 for ropeway inspection."),
        gmaps=[gm("のぼりべつクマ牧場 ロープウェイ山麓駅", "Bear Park ropeway base station", 42.49309, 141.14434, "のぼりべつクマ牧場 ロープウェイ 山麓駅")],
        links=[link("official", "のぼりべつクマ牧場 ご利用案内", "Noboribetsu Bear Park: visitor info", U["bear"], "https://bearpark.jp/en/")],
        rows=[row("hours", "10月21日〜4月20日 9:30〜16:30（最終入園15:50）／4月21日〜10月20日 9:00〜17:00（16:20）", "21 Oct–20 Apr 9:30–16:30 (last entry 15:50) / 21 Apr–20 Oct 9:00–17:00 (16:20)"),
              row("fee", "大人3,200円・子ども1,600円（ロープウェイ往復込み）。カード・交通系IC可", "Adults ¥3,200, children ¥1,600 (return ropeway included). Cards and IC OK"),
              row("closed", "2027年4月5日〜23日（ロープウェイ点検）", "5–23 April 2027 (ropeway inspection)", until="2027-04-23")],
        tip=T("のぼりべつクマ牧場の公式サイト（ご利用案内・お知らせ）で2026年11月26日に確認しました。", "Checked on the Bear Park’s website on 26 November 2026."),
        time=(VIS, "14:00〜15:40（大湯沼のかわり）", "14:00–15:40 (instead of Oyunuma)")),

    dict(
        id="bath", name=T("夢元さぎり湯・第一滝本館", "Sagiriyu or Takimotokan"), kind=T("日帰り入浴", "Day bath"),
        blurb=T("地元の人も通う温泉銭湯か、地獄谷の下の大きな旅館の大浴場。どちらもタトゥーの決まりは公式に記載なし。",
                "A local hot-spring bathhouse, or the big baths of a large inn below Jigokudani. Neither states a tattoo rule."),
        caution=T("タトゥー：どちらも公式に記載なし（要確認）。登別万世閣は不可", "Tattoos: not stated at either (please check); Manseikaku refuses"),
        lat=42.49223, lng=141.14301,
        text=T("タトゥー：夢元さぎり湯・第一滝本館とも、公式サイトにタトゥーの決まりは書かれていません。行く前に電話で確かめてください（さぎり湯 0143-84-2050）。登別万世閣は、公式サイトでタトゥー（タトゥーシールやペイントも）の入浴を断っています。入れないときは、大湯沼川の天然足湯（無料）へ。\n\n"
               "・夢元さぎり湯：温泉街のまん中の温泉銭湯で、硫黄泉と鉄泉の2種類。9:00〜21:00（最終受付20:30）、大人500円・子ども180円（公式サイト。観光協会のページは550円なので、変わっているかもしれません）。休憩室も使える1日券は710円。銭湯なので、タオル・シャンプー・ボディソープは持っていくのが前提です。中でも買えます（さぎり湯タオル400円、貸しバスタオル200円、シャンプー・ボディソープ各80円）。フェイスタオルがないと入れません。露天風呂・貸切風呂はありません。\n\n"
               "・第一滝本館：地獄谷のすぐ下の大きな旅館の大浴場。日帰りは9:00〜18:00に入って、21:00までに出ます。大人2,500円・子ども1,500円で、バスタオルとフェイスタオルが入っています。温水プールも使えます（水着は有料で貸し出し）。予約はいりません。カード・PayPayなどが使えます。2027年4月5日〜15日は日帰り入浴が休み。",
               "Tattoos: neither Sagiriyu nor Dai-ichi Takimotokan says anything about tattoos on its website, so phone before you go (Sagiriyu 0143-84-2050). Noboribetsu Manseikaku refuses tattoos (tattoo stickers and body paint included) on its website. If you cannot bathe, use the free natural foot bath on the Oyunuma river.\n\n"
               "• Sagiriyu: a hot-spring bathhouse in the middle of town with two kinds of water, sulphur and iron. 9:00–21:00 (last entry 20:30), adults ¥500, children ¥180 (per its website; the tourism association lists ¥550, so the price may have changed). A day ticket with the rest room is ¥710. As a public bathhouse it expects you to bring a towel, shampoo and soap; you can also buy them there (Sagiriyu towel ¥400, bath towel rental ¥200, shampoo or body soap ¥80 each). You will not be let in without a small towel. No outdoor or private baths.\n\n"
               "• Dai-ichi Takimotokan: the big baths of a large inn just below Jigokudani. Day visitors enter 9:00–18:00 and leave by 21:00. Adults ¥2,500, children ¥1,500, bath and face towels included. The heated pool is included too (swimsuit rental extra). No booking needed. Cards, PayPay and more accepted. No day bathing 5–15 April 2027."),
        gmaps=[gm("夢元さぎり湯", "Sagiriyu", 42.49223, 141.14301, "夢元さぎり湯"),
               gm("第一滝本館", "Dai-ichi Takimotokan", 42.49518, 141.14484, "第一滝本館")],
        links=[link("official", "夢元さぎり湯 公式サイト", "Sagiriyu (official, Japanese)", U["sagiri"]),
               link("official", "第一滝本館 日帰り入浴", "Dai-ichi Takimotokan day bathing", U["taki"], "https://takimotokan.co.jp/en/"),
               link("info", "登別の日帰り入浴の一覧", "Day baths in Noboribetsu (Japanese)", U["nb_oneday"])],
        rows=[row("tattoo", "さぎり湯・第一滝本館：公式に記載なし（要確認）／登別万世閣：不可", "Sagiriyu, Takimotokan: not stated (please check) / Manseikaku: refused"),
              row("hours", "さぎり湯 9:00〜21:00（最終受付20:30）／第一滝本館 9:00〜18:00に入館、21:00までに退館", "Sagiriyu 9:00–21:00 (last entry 20:30) / Takimotokan enter 9:00–18:00, leave by 21:00"),
              row("fee", "さぎり湯 大人500円（タオル400円）／第一滝本館 大人2,500円（タオル込み）", "Sagiriyu ¥500 (towel ¥400) / Takimotokan ¥2,500 (towels included)"),
              row("closed", "第一滝本館の日帰り入浴：2027年4月5日〜15日", "Takimotokan day bathing: 5–15 April 2027", until="2027-04-15")],
        notices=[N_TATTOO_N],
        tip=T("夢元さぎり湯・第一滝本館・登別万世閣の公式サイトと、登別国際観光コンベンション協会の日帰り入浴のページで2026年11月26日に確認しました。",
              "Checked on 26 November 2026 on the websites of Sagiriyu, Takimotokan and Manseikaku and the tourism association’s day-bathing page."),
        time=(VIS, "15:40〜17:30", "15:40–17:30")),

    dict(
        id="nyoru", name=T("晩ごはんと帰りのバス", "Dinner & ride back"), kind=T("晩ごはん・帰り", "Dinner & ride back"),
        blurb=T("温泉街で食べて、19:10のバスと20:26の特急で札幌21:41着。最後は20:35のバスと21:21の特急。",
                "Eat in town, then the 19:10 bus and 20:26 train reach Sapporo at 21:41. Last: the 20:35 bus and 21:21 train."),
        caution=T("登別温泉発の最終バスは20:35", "Last bus from the onsen: 20:35"),
        lat=42.49141, lng=141.14321,
        text=T("晩ごはんの例です（支払い方法は要確認）。\n\n"
               "・ラーメン天鳳：夜は18:00〜23:00、不定休。\n"
               "・温泉市場：食事は21:00まで、不定休。\n"
               "・炭火焼＆ラーメンいせくら：ホルモン焼きやジンギスカン。18:00〜1:00、不定休。\n"
               "・adex BAKERY&CAFE：22:00まで、無休。\n\n"
               "帰り：登別温泉ターミナル19:10発のバスで登別駅前19:22着。特急北斗19号 登別20:26発 → 札幌21:41着（平日・土日とも）。駅で1時間ほど待つので、温泉街でゆっくりして最終のバス20:35発（登別駅前20:47着）→ 特急北斗21号 21:21発 → 札幌22:41着でも。札幌で晩ごはんにするなら、18:00発のバス（18:15着）→ 特急すずらん11号 18:40発 → 札幌19:58着。\n\n"
               "帰りの特急も指定席を先にとっておくと安心です。冬は雪で遅れることがあります。",
               "Some dinner options (payment methods not confirmed):\n\n"
               "• Ramen 天鳳: evenings 18:00–23:00, irregular closures.\n"
               "• Onsen Ichiba: meals until 21:00, irregular closures.\n"
               "• Isekura: charcoal-grilled offal and lamb. 18:00–1:00, irregular closures.\n"
               "• adex Bakery & Café: until 22:00, open every day.\n\n"
               "Back: the 19:10 bus from Noboribetsu Onsen Terminal reaches Noboribetsu Station at 19:22. The limited express Hokuto 19 leaves at 20:26 and arrives in Sapporo at 21:41 (every day). That leaves an hour at the station, so you could stay in town for the last bus at 20:35 (station 20:47) and the Hokuto 21 at 21:21 (Sapporo 22:41). For dinner in Sapporo instead: the 18:00 bus (18:15), then the Suzuran 11 at 18:40 (Sapporo 19:58).\n\n"
               "Reserve your seat for the return train early. Snow can cause delays in winter."),
        gmaps=[gm("登別温泉ターミナル（バス）", "Noboribetsu Onsen bus terminal", 42.49141, 141.14321, "登別温泉 バスターミナル 道南バス"),
               gm("ラーメン天鳳", "Ramen 天鳳", 42.49300, 141.14350, "ラーメン天鳳 登別温泉")],
        links=[DONAN, JR, link("info", "炭火焼＆ラーメンいせくら", "Isekura (Japanese)", U["isekura"]), link("info", "ラーメン天鳳", "Ramen 天鳳 (Japanese)", U["tenho"])],
        rows=[row("bus", "登別温泉19:10 → 登別駅前19:22／最終20:35 → 20:47、450円・現金", "Onsen 19:10 → station 19:22 / last 20:35 → 20:47, ¥450 cash"),
              row("train", "登別20:26（北斗19号）→ 札幌21:41／最終の特急21:21（北斗21号）→ 22:41", "Noboribetsu 20:26 (Hokuto 19) → Sapporo 21:41 / last limited express 21:21 (Hokuto 21) → 22:41"),
              row("food", "天鳳 18:00〜23:00／温泉市場 〜21:00／いせくら 18:00〜1:00／adex 〜22:00", "天鳳 18:00–23:00 / Onsen Ichiba to 21:00 / Isekura 18:00–1:00 / adex to 22:00")],
        cash=True,
        tip=T("バスは道南バスの時刻表（2026年10月1日改正）、列車は乗換案内（2026年12月3日・5日）、お店は登別国際観光コンベンション協会のページで確認しました。",
              "Buses from Donan Bus’s timetable (revised 1 October 2026), trains from a route planner (3 and 5 December 2026), shops from the tourism association’s pages."),
        time=(VIS, "17:45〜20:35（晩ごはん・帰り）", "17:45–20:35 (dinner and the ride back)")),
]

# ---------------------------------------------------------------------------
# 書き出し
# ---------------------------------------------------------------------------
COURSES = [
    dict(file=f"{ID}.json", course="jozankei", spots=JOZANKEI,
         note="定山渓。地下鉄と12番のバス（予約制のかっぱライナー号も）→二見の足湯→岩戸観音堂→お昼→定山源泉公園→豊平峡温泉（お風呂と晩ごはん）か夜の温泉街→札幌。",
         sections=[(1, 1, T("札幌から", "From Sapporo"), T("地下鉄とバスで約1時間", "About an hour by subway and bus")),
                   (2, 5, T("定山渓の温泉街", "Jozankei town"), T("足湯、洞窟のお堂、お昼、温泉卵", "Foot baths, a cave shrine, lunch and onsen eggs")),
                   (6, 7, T("夕方〜夜", "Evening"), T("豊平峡温泉か、温泉街で晩ごはん", "Hoheikyo Onsen, or dinner in town"))],
         focus=(2, 7), auto={"jstart": "always"}, default_off=["yoru"],
         hints=[("yoru", ["hoheikyo"], [],
                 "豊平峡温泉のあと温泉街で食べるなら、豊平峡温泉18:30発のバスで湯の町へ戻ります（18:41着、200円）。帰りは20:53発（土日祝20:45発）の札幌駅行き。",
                 "To eat in town after Hoheikyo, take the 18:30 bus back to Yunomachi (18:41, ¥200), then the 20:53 (20:45 weekends) to Sapporo Station."),
                ("yoru", [], ["hoheikyo"],
                 "豊平峡温泉に行かない日は、源泉公園のあとに定山渓神社や、足のふれあい太郎の湯へ。晩ごはんは17:00から開く松尾ジンギスカンなど。",
                 "Skipping Hoheikyo? After the park, visit Jozankei Shrine or the Taro-no-yu foot bath. Matsuo Jingisukan opens at 17:00 for dinner.")]),
    dict(file=f"{ID}-noboribetsu.json", course="noboribetsu", spots=NOBORIBETSU,
         note="登別。特急北斗→道南バス→極楽通りでお昼と閻魔堂→泉源公園→地獄谷→大湯沼と天然足湯（冬はクマ牧場）→日帰り入浴→晩ごはん→札幌。",
         sections=[(1, 1, T("札幌から", "From Sapporo"), T("特急で1時間14分、バスで19分", "74 minutes by train, 19 by bus")),
                   (2, 3, T("極楽通り", "Gokuraku-dori"), T("お昼と閻魔堂、間欠泉", "Lunch, Enma-do and the geyser")),
                   (4, 6, T("地獄谷と山", "Jigokudani and the hills"), T("地獄谷から大湯沼へ。冬はクマ牧場", "Jigokudani to Oyunuma; Bear Park in winter")),
                   (7, 8, T("お風呂と晩ごはん", "Bath and dinner"), T("札幌に21:41（最後は22:41）", "Sapporo by 21:41 (last 22:41)"))],
         focus=(2, 8), auto={"nstart": "always", "nyoru": "always"}, default_off=["bear"],
         hints=[("bear", ["oyunuma"], [],
                 "大湯沼の遊歩道とクマ牧場の両方は、お風呂の時間がなくなります（冬はクマ牧場の最終入園が15:50）。どちらか1つに。",
                 "The Oyunuma trail and the Bear Park together leave no time for a bath (winter last entry at the Bear Park is 15:50). Pick one."),
                ("bear", [], ["oyunuma"],
                 "クマ牧場は地獄谷のあと14:00ごろに。ロープウェイの山麓駅は、バスターミナルから歩いて5分ほどです。",
                 "Go to the Bear Park after Jigokudani, at about 14:00. The ropeway base station is about 5 minutes’ walk from the bus terminal.")]),
]


def build(C):
    spots_src = C["spots"]
    N = {s["id"]: i for i, s in enumerate(spots_src, 1)}
    out_spots = []
    for no, s in enumerate(spots_src, 1):
        label, tja, ten = s["time"]
        text = {"ja": s["text"]["ja"] + f"\n\n{label[0]}：{tja}", "en": s["text"]["en"] + f"\n\n{label[1]}: {ten}"}
        text = {l: s["name"][l] + "\n\n" + text[l] for l in ("ja", "en")}
        o = {"no": no, "id": s["id"], "name": s["name"], "kind": s["kind"], "blurb": s["blurb"]}
        if s.get("caution"):
            o["caution"] = s["caution"]
        o.update(lat=s["lat"], lng=s["lng"], text=text, gmaps=s["gmaps"], links=s["links"], notices=s.get("notices", []),
                 info={"rows": s["rows"], "cash": s.get("cash", False), "tip": s["tip"], "checked": CHECKED},
                 photos=W(s["id"]))
        assert o["photos"], s["id"]
        for p in o["photos"]:
            f = p if isinstance(p, str) else p["file"]
            assert os.path.exists(f"{IMG}/{f}"), f
        out_spots.append(o)
    picks = [N[s["id"]] for s in spots_src if s["id"] not in C["auto"]]
    default = [n for n in picks if spots_src[n - 1]["id"] not in C["default_off"]]
    auto = {str(N[k]): {"always": True} for k in C["auto"]}
    hints = [{"spot": N[sid], "rule": dict({"any": [N[sid]]}, **({"andAny": [N[x] for x in with_]} if with_ else {}),
                                           **({"none": [N[x] for x in without]} if without else {})),
              "text": T(ja, en)} for sid, with_, without, ja, en in C["hints"]]
    data = {
        "id": ID, "course": C["course"],
        "_note": "札幌から日帰り 温泉めぐり（sapporo-onsen/ のページ専用。形は eizan-line.json と同じ）。" + C["note"]
                 + "写真は今は Wikimedia Commons だけ（一覧は scripts/sapporo_onsen_web_photos.json）。"
                 + "info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。このファイルは scripts/build_sapporo_onsen_data.py で作る（直接直さない）。",
        "sections": [{"first": a, "last": b, "area": area, "title": title} for a, b, area, title in C["sections"]],
        "focus": {"first": C["focus"][0], "last": C["focus"][1]},
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。札幌からの行き（と登別の帰り）は自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": default, "auto": auto, "hints": hints},
        "photoBase": f"../images/{ID}/", "sources": SOURCES,
        "spots": out_spots,
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"], len(s["photos"])) for s in out_spots], "default", default)


for C in COURSES:
    build(C)
