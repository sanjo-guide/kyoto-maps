#!/usr/bin/env python3
"""大雪山の日帰り：旭岳と層雲峡（daisetsuzan）のデータを書き出す。行き先ごとに1ファイル。

使い方: python3 scripts/build_daisetsuzan_data.py   （そのあと python3 scripts/sync_daisetsuzan.py）
- data/routes/daisetsuzan.json         … 旭岳（あさひだけ。asahidake。最初に開く）6か所
- data/routes/daisetsuzan-sounkyo.json … 層雲峡（そううんきょう。sounkyo）7か所
- どちらも旭川駅のまわりのホテルを9〜10時に出て、バスで往復する1日（車を運転しない人が前提）。旭川に戻るのは18:33／18:55。
  一年中使えるコースにして、冬（雪・服装・短い運行時間・整備の運休）と、夏だけのもの（散策路・リフト・滝へのバス）は
  notices（from / to）と rows（until）、文章で出す
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 時刻：バスは旭川電気軌道（いで湯号、2025-10-01改正）と道北バス（層雲峡・上川線、2026-07-01改正）の公式の時刻表。
  JR（上川→旭川）は乗換案内の2026年12月3日（木）・5日（土）。JR北海道は2027年3月にダイヤ改正があるので、そのあと確かめ直す
- 毎年直すもの：ロープウェイの整備運休の期間（旭岳・黒岳）、氷瀑まつりの日程、黒岳のスノーシューツアーの期間、黒岳の料金（2027-06-01に変更）
- タトゥー：お風呂ごとに公式サイトの決まりを書いた。書いていない施設は「要確認」
- 店名は、公式サイトか観光協会（ひがしかわ観光協会・層雲峡観光協会）の店の紹介ページで時間を確かめた店だけ
- 写真はまだ Wikimedia Commons だけ（scripts/daisetsuzan_web_photos.json）。自分の写真はあとで <スポットのid>-<番号>.jpg で入る
- 文章は中立に（だれかが行った・食べたとは書かない）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = "daisetsuzan"
IMG = f"{R}/images/{ID}"
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


def winters(hja, hen, ja, en, url=None, months=("11-01", "04-30")):
    """冬だけ出すお知らせを、2026〜2028年の冬の分つくる（from / to は年つきの日付なので）"""
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


WEB = json.load(open(f"{R}/scripts/daisetsuzan_web_photos.json", encoding="utf-8"))


def W(sid):
    """そのスポットの写真。自分の写真（<sid>-<番号>.jpg）があれば先に並べる"""
    own = sorted(f for f in os.listdir(IMG) if f.startswith(sid + "-") and not f.startswith(sid + "-w")) if os.path.isdir(IMG) else []
    return own + [cc(x) for x in WEB.get(sid, [])]


D1, D2 = "2026/12/03", "2026/12/05"   # 木曜・土曜
U = dict(
    ideyu="https://www.asahikawa-denkikidou.jp/asahidaek_line/",
    ideyu_fare="https://www.asahikawa-denkikidou.jp/manage/wp-content/uploads/2026/07/un66_2026.09.pdf",
    rope="https://asahidake.hokkaido.jp/ja/", rope_en="https://asahidake.hokkaido.jp/en/",
    avc="https://www.asahidake-vc-2291.jp/", avc_en="https://www.asahidake-vc-2291.jp/foreign",
    avc_guide="https://www.asahidake-vc-2291.jp/guide/", avc_rental="https://www.asahidake-vc-2291.jp/rental_goods/",
    avc_course="https://www.asahidake-vc-2291.jp/course/", avc_qa="https://www.asahidake-vc-2291.jp/q%ef%bc%86a/",
    hk_onsen="https://www.welcome-higashikawa.jp/onsen",
    ks="https://kshouse.jp/hokkaido-j/index.html", ks_en="https://kshouse.jp/hokkaido-e/index.html",
    ks_faq="https://kshouse.jp/hokkaido-e/faq.html",
    bear="https://www.bearmonte.jp/hotspring/", yukoman="https://www.yukoman.jp/day_trip",
    shirakaba="https://www.shirakabasou.com/",
    michikusa="https://www.welcome-higashikawa.jp/michikusa/", hk_gourmet="https://www.welcome-higashikawa.jp/gurmet",
    tune="https://www.welcome-higashikawa.jp/members/cafetune/", natures="https://www.welcome-higashikawa.jp/members/natures-brewing/",
    dohoku="https://www.dohokubus.com/files/kamikawa_souun.pdf", dohoku_top="https://www.dohokubus.com/rosen_bus3.html",
    dohoku_touch="https://www.dohokubus.com/touch-payment.html",
    kuro="https://www.rinyu.co.jp/kurodake/", kuro_about="https://www.rinyu.co.jp/kurodake/about/",
    kuro_fac="https://www.rinyu.co.jp/kurodake/facility/", kuro_tour="https://www.rinyu.co.jp/kurodake/tour_rental/",
    sk="https://sounkyo.net/", sk_access="https://sounkyo.net/go/detail.html?content=62",
    sk_taki="https://sounkyo.net/view/detail.html?content=7", sk_obako="https://sounkyo.net/view/detail.html?content=10",
    sk_vc="https://sounkyovc.net/aboutus", sk_vc_en="https://sounkyovc.net/en",
    sk_yu="https://sounkyo.net/stay/detail.html?content=25",
    sk_canyon="https://sounkyo.net/eat/detail.html?content=32", sk_shokudo="https://sounkyo.net/eat/detail.html?content=34",
    sk_tozanken="https://sounkyo.net/eat/detail.html?content=75",
    hyobaku="https://sounkyo.net/hyoubaku/", hyobaku_access="https://sounkyo.net/hyoubaku/access/",
    sun="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0112.html",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("いで湯号（66番）の時刻", U["ideyu"], "2025年10月1日改正、4往復、毎日運行。旭川駅（のりば9）7:15・9:15・12:15・14:15→旭岳9:03・11:03・14:03・16:03。旭岳9:55・11:55・14:55・16:55→旭川駅11:33・13:33・16:33・18:33。ひがしかわ道草館は行き8:12・10:12・13:12・15:12、帰り10:34・12:34・15:34・17:34。旭岳温泉入口は旭岳発の2分後、ホテルベアモンテ前は同じ分"),
    ("いで湯号の運賃・支払い", U["ideyu"], "旭川駅〜旭岳 大人2,300円、旭川空港〜旭岳1,650円、ひがしかわ道草館〜旭岳1,450円（2026年9月1日改定）。使用可能なICカードはAsaca・DoCARD。券売機は旭川電気軌道総合案内所と旭川空港（キャッシュレス券売機もあり）。往復割引なし"),
    ("いで湯号の運賃表（PDF）", U["ideyu_fare"], "運賃改定日 令和8年9月1日。旭川駅〜ひがしかわ道草館1,110円、旭岳温泉入口〜旭岳250円、旭川駅〜旭岳温泉入口2,300円"),
    ("旭岳ロープウェイの運行日・時間", U["rope"], "整備運休 2026年11月16日〜12月10日、2027年5月10日〜21日。12月11日〜2月28日 9:00〜15:40（下り最終）、3月1〜15日 9:00〜16:00、3月16日〜5月9日 9:00〜17:00、6月1〜19日 8:00〜17:00、6月20日〜9月30日 6:30（土日祝など6:00）〜17:30、10月1〜20日 8:00〜17:00、10月21日〜11月15日 9:00〜16:00。6/1〜10/20は15分間隔、10/21〜5/31は20分間隔（00・20・40）、上り最終は下り最終の15分／20分前。片道約10分"),
    ("旭岳ロープウェイの料金・注意", U["rope"], "往復 大人3,000円（11/1〜5/31）・3,500円（6/1〜10/31）、小人1,750円。クレジットカード可。予約乗車制ではない。強風・落雷で運行休止。最終下り便への乗り遅れが山岳事故扱いになった事例。姿見の池散策路は1周約1時間・約1.7km（6月〜10月中旬）、山頂駅でレンタル長靴。運休期間はレストラン・売店も休業"),
    ("旭岳ビジターセンター", U["avc_guide"], "開館9:00〜17:00、休館日は年末年始。無料Wi-Fi、休憩コーナー"),
    ("旭岳ビジターセンターのレンタル", U["avc_rental"], "長靴500円、ストック500円、スノーシュー1,000円（ストックつき、積雪期のみ）。顔写真入りの身分証を提示。スノーシューのレンタルは2026年12月11日から、予約不可"),
    ("旭岳ビジターセンター Q＆A", U["avc_qa"], "旭岳近辺にATMなし。コンビニはラビスタ大雪山1階のヤマザキショップ。食堂は旭岳ロープウェイ山麓駅2階、売店は1階。キャッシュレス決済可（交通系電子マネーも）。コインロッカーは旭岳ロープウェイに"),
    ("旭岳温泉の日帰り入浴（ひがしかわ観光協会）", U["hk_onsen"], "ホテルベアモンテ12:30〜19:00（受付〜18:00）1,140円、大雪山白樺荘13:00〜19:00 800円、湯元湧駒荘12:00〜19:00（受付〜18:00）1,200円、ケイズハウス北海道（不定休）15:00〜19:00 900円"),
    ("ケイズハウス北海道の日帰り温泉", U["ks"], "15:00〜19:00（退館は20:00前）900円。時短営業日、休業日あり。バス停 旭岳温泉入口で下車"),
    ("ケイズハウス北海道のタトゥー", U["ks_faq"], "英語のFAQ：Are people with tattoos allowed in the onsen? → Yes, tattoo friendly"),
    ("ホテルベアモンテの日帰り入浴", U["bear"], "12:30〜19:00（最終受付18:00）、大人1,140円・小人570円、フェイスタオル110円・バスタオル220円。タトゥーの記載なし"),
    ("湧駒荘の日帰り入浴", U["yukoman"], "別館「神々の湯」、受付12:00〜18:00（19:00までの営業）、大人1,200円・小学生600円。バスタオル貸出300円、フェイスタオル販売200円。タトゥーの記載なし"),
    ("道の駅ひがしかわ「道草館」", U["michikusa"], "9:00〜18:00（4〜9月）、9:00〜17:00（10〜3月）、休館日は年末年始（12/31〜1/4）、お手洗いは24時間"),
    ("CAFEtune（ひがしかわ観光協会）", U["tune"], "YAMAtune併設、東川町南町2丁目、10:00〜17:00、木曜・不定休あり"),
    ("NATURES Brewing（ひがしかわ観光協会）", U["natures"], "東川町東町3丁目6-8、15:00〜21:00、月曜・木曜定休、22席"),
    ("道北バス 層雲峡・上川線の時刻・運賃", U["dohoku"], "2026年7月1日改正。旭川駅前（のりば8）6:55→層雲峡8:54、9:55→11:54、10:55→12:54。層雲峡14:40→旭川駅前16:35、17:00→18:55。層雲峡18:55→上川森のテラス バスタッチ19:25（上川止まり）。層雲峡〜旭川2,140円、上川〜層雲峡890円、層雲峡〜滝見台220円。層雲峡12:50→滝見台13:09→大函入口13:15、大函入口13:43→滝見台13:49→層雲峡14:00は7月1日〜10月31日の運行"),
    ("道北バスのタッチ決済", U["dohoku_touch"], "対象路線に「その他（白金線、層雲峡線、空港線等の路線バスの一部）」"),
    ("JR 上川→旭川（木曜）", q("上川", "旭川", D1, "19:25"), "上川20:24発の普通→旭川21:22着、21:04発の特別快速大雪→21:44着、1,380円"),
    ("JR 上川→旭川（土曜）", q("上川", "旭川", D2, "19:25"), "木曜と同じ（20:24→21:22、21:04→21:44）"),
    ("黒岳ロープウェイ・リフトの料金と時間", U["kuro_about"], "ロープウェイ往復 大人3,000円・小学生1,500円、片道7分・20分間隔。11月9日〜30日整備運休、12月1日〜6月20日 8:00〜16:00、6月21日〜9月30日 6:00〜18:00、10月1〜15日 7:00〜17:00、上りの最終は営業終了の40分前。リフト往復1,200円（2027年夏：6月1〜20日 8:30〜15:30、6月21日〜9月30日 6:30〜17:30、10月1〜15日 7:30〜16:30）、セット往復3,900円（夏季のみ）。冬季リフトは滑走具を持つ人だけ"),
    ("黒岳ロープウェイのお知らせ", U["kuro"], "12:20の便は運休（従業員の昼休憩のため）。2027年6月1日から料金変更。本日の運行状況は7:00更新"),
    ("黒岳ロープウェイの駅の施設", U["kuro_fac"], "層雲峡駅：コインロッカー、売店、Black Mountain Coffee 9:00〜15:30（月・火休み）。黒岳駅（5合目）：ともちゃん食堂11:00〜15:30（LO15:00）不定休、売店、屋上の黒岳ネイチャーテラス。お手洗いは5合目の駅が最後"),
    ("くろだけスノーシューハイキング", U["kuro_tour"], "2027年1月5日〜3月10日、前日・当日受付（電話01658-5-3031か現地）。ショートコース 大人7,000円・約2時間・9:30までに山麓窓口に集合。料金にロープウェイ往復・ガイド・スノーシュー・ストック・スノーブーツ・スキーウェア・保険を含む"),
    ("銀河・流星の滝（層雲峡観光協会）", U["sk_taki"], "日本の滝百選。滝を背に20分ほど斜面を登ると双瀑台。通年、無料"),
    ("大函（層雲峡観光協会）", U["sk_obako"], "層雲峡温泉より北見方面へ約6km。小函遊歩道は落石の危険があるため通行禁止。通年、無料"),
    ("層雲峡ビジターセンター", U["sk_vc"], "9時〜17時。6〜10月無休、11〜5月は月曜休み（祝日の場合は翌日）、年末年始12月31日〜1月5日休み"),
    ("黒岳の湯（層雲峡観光協会）", U["sk_yu"], "5月1日〜10月31日 10時〜22時（最終受付21時30分）、11月1日〜4月30日 11時〜21時30分（最終受付21時）、12月31日〜1月3日 11時〜18時。無休（メンテナンス休館あり）。大人800円・子ども400円。タトゥーの記載なし"),
    ("層雲峡の食事（層雲峡観光協会）", U["sk_shokudo"], "大雪山食堂 11:00〜15:00、17:30〜20:30、不定休。ビアグリル・キャニオン 11:30〜15:00、17:30〜20:00（水曜定休）。登山軒 10〜21時（11〜5月は休業）"),
    ("層雲峡温泉氷瀑まつり", U["hyobaku"], "第52回 2027年1月23日（土）〜3月7日（日）。平日17:00〜21:30、土日祝11:00〜21:30（最終入場21:15）。協力金1,000円。暖かい服と滑り止めのついた靴で。会場内休憩所で手袋・滑り止めを販売"),
    ("氷瀑まつりの会場への行き方", U["hyobaku_access"], "層雲峡温泉で下車後、徒歩5分"),
    ("日の入り（札幌、12月）", U["sun"], "12月の日の入りは16時ごろ"),
]]

IDEYU = link("timetable", "いで湯号（66番）時刻・運賃", "Ideyu-go bus (route 66): times and fares", U["ideyu"])
ROPE = link("official", "旭岳ロープウェイ（運行状況・今の気温）", "Asahidake Ropeway (status, live temperature)", U["rope"], U["rope_en"])
AVC = link("info", "旭岳ビジターセンター", "Asahidake Visitor Center", U["avc"], U["avc_en"])
HK = link("info", "ひがしかわ観光協会", "Higashikawa Tourism Association (Japanese)", "https://www.welcome-higashikawa.jp/")
DOHOKU = link("timetable", "道北バス 層雲峡・上川線の時刻表（PDF）", "Dohoku Bus: Sounkyo–Kamikawa timetable (PDF)", U["dohoku"])
DOHOKU2 = link("official", "道北バス（モバイルチケット）", "Dohoku Bus (mobile tickets, Japanese)", U["dohoku_top"])
KURO = link("official", "黒岳ロープウェイ（運行状況）", "Kurodake Ropeway (today’s status, Japanese)", U["kuro"])
SK = link("info", "層雲峡観光協会", "Sounkyo Tourist Association (Japanese)", U["sk"])

# 何か所かに出すお知らせ
N_COLD = winters(
    "冬の山の上の服装", "What to wear up the mountain in winter",
    "11月から4月は、山の上は雪と氷点下の世界で、風が強い日があります。スキーウェアか、それに近い風を通さない上下、帽子、厚い手袋、首と顔をおおうもの、サングラスかゴーグル、雪が入らない冬の靴で。12月の日の入りは16時ごろです。強風でロープウェイが止まることがあるので、朝、公式サイトの運行状況を見てから出てください。",
    "From November to April it is snow, sub-zero temperatures and often strong wind at the top. Wear ski clothing or something close to it (windproof jacket and trousers), a hat, thick gloves, something to cover your neck and face, sunglasses or goggles, and winter boots that keep snow out. In December the sun sets at about 16:00. Strong wind can stop the ropeway, so check the status on the official site before you leave in the morning.")
N_AROPE = [
    notice("ロープウェイは12月10日まで運休", "Ropeway closed until 10 December",
           "旭岳ロープウェイは、整備のため2026年11月16日〜12月10日は運休です。山麓駅の食堂と売店も休み。12月11日から動きます。この期間は、ビジターセンターのまわりの森と温泉だけになります。",
           "The Asahidake Ropeway is closed for maintenance from 16 November to 10 December 2026, along with the restaurant and shop in the base station. It reopens on 11 December. Until then, a visit means the forest around the Visitor Center and the hot springs only.",
           U["rope"], to="2026-12-10"),
    notice("ロープウェイは5月10日〜21日に運休", "Ropeway closed 10–21 May",
           "旭岳ロープウェイは、整備のため2027年5月10日〜21日は運休です。山麓駅の食堂と売店も休み。",
           "The Asahidake Ropeway is closed for maintenance from 10 to 21 May 2027, along with the restaurant and shop in the base station.",
           U["rope"], start="2027-04-20", to="2027-05-21")]
N_KURO = [notice("黒岳ロープウェイは11月30日まで運休", "Kurodake Ropeway closed until 30 November",
                 "黒岳ロープウェイは、整備のため2026年11月9日〜30日は運休です。12月1日から動きます。",
                 "The Kurodake Ropeway is closed for maintenance from 9 to 30 November 2026 and reopens on 1 December.",
                 U["kuro"], to="2026-11-30")]
N_HYOBAKU = [notice("氷瀑まつり：1月23日〜3月7日", "Ice Fall Festival: 23 January–7 March",
                    "第52回 層雲峡温泉氷瀑（ひょうばく）まつりは、2027年1月23日（土）〜3月7日（日）。平日は17:00〜21:30、土日祝は11:00〜21:30。協力金1,000円。平日は、旭川行きの最後のバス（17:00発）のあとに始まります。",
                    "The 52nd Sounkyo Onsen Ice Fall Festival runs from Saturday 23 January to Sunday 7 March 2027: 17:00–21:30 on weekdays, 11:00–21:30 at weekends and on holidays. Entry is a ¥1,000 contribution. On weekdays it opens just as the last bus to Asahikawa (17:00) leaves.",
                    U["hyobaku"], start="2026-11-01", to="2027-03-07")]
N_TATTOO_A = notice(
    "タトゥーがある人へ", "If you have tattoos",
    "旭岳温泉で、公式サイトに「タトゥーがあっても入れます」と書いているのはケイズハウス北海道です（15:00〜19:00、900円、休みの日あり）。ホテルベアモンテと湧駒荘の公式サイトには、タトゥーについての記載がありません。入る前に受付か電話で確かめてください。",
    "At Asahidake Onsen, K’s House Hokkaido says on its website that guests with tattoos are welcome in its hot spring (15:00–19:00, ¥900, closed on some days). The websites of Hotel Bear Monte and Yukomanso say nothing about tattoos: ask at the desk or by phone before you go in.",
    U["ks_faq"])
N_TATTOO_S = notice(
    "タトゥーがある人へ", "If you have tattoos",
    "黒岳の湯のタトゥーの決まりは、層雲峡観光協会の案内には書かれていません。行く前に電話（01658-5-3333）で確かめてください。",
    "The Sounkyo Tourist Association’s page for Kurodake-no-yu says nothing about tattoos. Phone before you go (01658-5-3333, Japanese).",
    U["sk_yu"])

# ---------------------------------------------------------------------------
# 旭岳のコース
# ---------------------------------------------------------------------------
ASAHIDAKE = [
    dict(
        id="astart", name=T("旭川駅から旭岳へ", "Asahikawa to Asahidake"), kind=T("出発・バス", "Start: bus"),
        blurb=T("旭川駅前9:15発のバス「いで湯号」で1時間48分。1日4往復で、帰りの最終は旭岳16:55発。",
                "The 9:15 Ideyu-go bus from Asahikawa Station takes 1 hr 48 min. Four buses a day; the last one back leaves at 16:55."),
        caution=T("帰りの最終バスは旭岳16:55発。Kitaca・Suicaの案内なし", "Last bus back leaves Asahidake at 16:55. Kitaca/Suica not listed"),
        lat=43.76330, lng=142.35870,
        text=T("旭岳（あさひだけ、2,291m）は北海道でいちばん高い山で、大雪山（たいせつざん）の主峰です。旭川駅から、旭川電気軌道のバス66番「いで湯号」が、旭川空港と東川（ひがしかわ）の町を通って、ロープウェイの山麓駅の前（終点「旭岳」）まで行きます。1日4往復、毎日運行、予約は要りません。\n\n"
               "旭川駅前の9番のりばを9:15発、旭岳に11:03着。片道2,300円です。公式サイトに書かれているICカードは、旭川のバスのカード（Asaca・DoCARD）だけ。KitacaやSuicaは書かれていません。現金で払うか（両替は千円札と硬貨のつもりで）、駅前の旭川電気軌道 総合案内所（旭川駅前のツルハビル1階）の券売機で先に乗車券を買います。券売機はカードなども使えます。往復割引はないので、往復なら2枚。JRのレールパスは使えません。\n\n"
               "帰りのバスは、旭岳発11:55・14:55・16:55の3本です。16:55発（旭川駅18:33着）が最終で、乗り遅れると旭川へ戻るバスはありません。\n\n"
               "ロープウェイは強風で止まることがあります。止まった日も、ふもとのビジターセンターと温泉で最終バスまで過ごせますが、朝、ロープウェイの公式サイトで運行状況を見てから出ると無駄がありません。\n\n"
               "山の上をゆっくり歩いて、温泉にも東川の町にも寄りたい日は、7:15発（旭岳9:03着）で。旭川に戻ったあとの晩ごはんは、駅前から歩ける買物公園のあたりで。",
               "Asahidake (2,291 m) is the highest mountain in Hokkaido and the main peak of the Daisetsuzan range. Asahikawa Denkikido’s route 66 bus, the Ideyu-go, runs from Asahikawa Station via Asahikawa Airport and the town of Higashikawa to the ropeway base station (the last stop, “Asahidake”). Four round trips a day, every day, no booking.\n\n"
               "Leave from stop 9 outside Asahikawa Station at 9:15 and arrive at 11:03. The fare is ¥2,300 one way. The only IC cards listed on the bus company’s page are the local Asaca and DoCARD; Kitaca and Suica are not mentioned. Pay cash on board (carry ¥1,000 notes and coins), or buy a ticket beforehand from the machine in the company’s information office on the ground floor of the Tsuruha building in front of the station; the machine also takes cards. There is no return discount, so buy two tickets for a round trip. Japan Rail passes are not valid.\n\n"
               "Buses back leave Asahidake at 11:55, 14:55 and 16:55. The 16:55 (Asahikawa Station 18:33) is the last one: miss it and there is no bus to Asahikawa.\n\n"
               "Strong wind can stop the ropeway. You can still spend the day at the Visitor Center and the hot springs, but it is worth checking the ropeway’s status page before you set out.\n\n"
               "For a slower walk at the top plus both a bath and the town of Higashikawa, take the 7:15 bus (arrives 9:03). Back in Asahikawa, dinner is a short walk from the station around the Kaimono Koen pedestrian street."),
        gmaps=[gm("旭川駅前バスのりば", "Bus stops outside Asahikawa Station", 43.76330, 142.35870, "旭川駅前 バスのりば 9番")],
        links=[IDEYU, link("info", "いで湯号の運賃表（PDF）", "Ideyu-go fare table (PDF, Japanese)", U["ideyu_fare"]), ROPE],
        rows=[row("bus", "いで湯号 旭川駅（9番のりば）9:15 → 旭岳11:03（朝は7:15 → 9:03）", "Ideyu-go: Asahikawa Station (stop 9) 9:15 → Asahidake 11:03 (earlier: 7:15 → 9:03)"),
              row("bus", "帰り 旭岳11:55・14:55・16:55発 → 旭川駅13:33・16:33・18:33着。16:55が最終", "Back: Asahidake 11:55, 14:55, 16:55 → Asahikawa Station 13:33, 16:33, 18:33. The 16:55 is the last bus"),
              row("fee", "片道2,300円（2026年9月1日改定）。現金、Asaca・DoCARD、または総合案内所の券売機。往復割引なし", "¥2,300 one way (from 1 Sep 2026). Cash, Asaca/DoCARD, or a ticket from the machine at the bus office. No return discount")],
        notices=N_AROPE + N_COLD,
        cash=True,
        tip=T("時刻と運賃は、旭川電気軌道の公式ページ（2025年10月1日改正の時刻表、2026年9月1日改定の運賃表）で2026年11月28日に確認しました。",
              "Times and fares checked on Asahikawa Denkikido’s pages (timetable revised 1 October 2025, fares revised 1 September 2026) on 28 November 2026."),
        time=(DEP, "9:15（旭川駅前 9番のりば）", "9:15 from stop 9 outside Asahikawa Station")),

    dict(
        id="avc", name=T("旭岳ビジターセンター", "Asahidake Visitor Center"), kind=T("案内・レンタル", "Information & rental"),
        blurb=T("バスを降りたら最初にここへ。今日の山の様子を聞いて、冬はスノーシューを借ります。入館無料。",
                "Come here first when you get off the bus: today’s conditions, and snowshoe rental in winter. Free."),
        lat=43.65202, lng=142.79959,
        text=T("バスの終点から歩いて2分。国立公園の案内施設で、入館は無料、9:00〜17:00（年末年始は休み）。入って左のパネルに、ロープウェイの運行状況と道の様子が出ています。姿見の池を歩けるか、何が要るかを、窓口で聞いてから上がってください。\n\n"
               "借りられるもの（1日）：長靴500円、ストック500円、スノーシュー1,000円（ストックつき。雪のある季節だけで、この冬は2026年12月11日から。予約はできません）。借りるときに顔写真つきの身分証（パスポートなど）を見せます。支払いはクレジットカードやKitaca・Suicaなども使えます。17:00の閉館までに返します。\n\n"
               "無料のWi-Fi、休憩用のテーブル、お手洗いがあり、最終バスまでの待ち時間もここで過ごせます。旭岳温泉にATMはありません。コンビニは、ラビスタ大雪山（坂を下って約800m）の1階のヤマザキショップだけです。\n\n"
               "ロープウェイが止まった日や、上が吹雪の日は、ビジターセンターのまわりの森を歩けます（冬はスノーシューとクロスカントリースキーのコース、夏は自然探勝路。地図は窓口と公式サイトに）。係の人と歩く「旭岳温泉ネイチャーウォーク」（13:30〜15:00、2,000円、スノーシューつき、開催日は公式サイトのカレンダーに）は、日本語で話せる人だけの受け付けです。",
               "Two minutes’ walk from the last bus stop. This is the national park’s information centre: free, open 9:00–17:00 (closed over New Year). A panel to the left of the entrance shows the ropeway’s status and trail conditions. Ask at the desk whether the Sugatami Pond walk is possible today and what you need before you go up.\n\n"
               "Rental (per day): rubber boots ¥500, poles ¥500, snowshoes ¥1,000 (with poles; snow season only, from 11 December 2026 this winter; no reservations). You must show photo ID such as a passport. Cards and IC cards such as Kitaca and Suica are accepted. Return everything before the 17:00 closing time.\n\n"
               "There is free Wi-Fi, tables to rest at and toilets, so it is also a place to wait for the last bus. There is no ATM at Asahidake Onsen. The only convenience shop is the Yamazaki Shop on the ground floor of La Vista Daisetsuzan, about 800 m down the road.\n\n"
               "If the ropeway is stopped or the top is in a blizzard, you can walk in the forest around the Visitor Center instead (snowshoe and cross-country ski courses in winter, nature trails in summer; maps at the desk and on the website). The guided Asahidake Onsen Nature Walk (13:30–15:00, ¥2,000 with snowshoes, dates on the website calendar) is only for people who can communicate in Japanese."),
        gmaps=[gm("旭岳ビジターセンター", "Asahidake Visitor Center", 43.65202, 142.79959, "旭岳ビジターセンター")],
        links=[AVC, link("info", "レンタルの料金", "Rental prices (Japanese)", U["avc_rental"]),
               link("info", "周辺コースの地図", "Maps of the walking courses (Japanese)", U["avc_course"])],
        rows=[row("hours", "9:00〜17:00", "9:00–17:00"),
              row("closed", "年末年始", "Closed over New Year"),
              row("fee", "入館無料。スノーシュー1,000円（積雪期、2026年は12月11日から）、長靴500円、ストック500円。顔写真つきの身分証が要ります", "Free. Snowshoes ¥1,000 (snow season; from 11 Dec in 2026), boots ¥500, poles ¥500. Photo ID required")],
        notices=[],
        tip=T("旭岳ビジターセンターの公式サイト（館内のご案内・レンタル・Q＆A・お知らせ）で2026年11月28日に確認しました。年末年始の休みの日付は書かれていません。",
              "Checked on the Asahidake Visitor Center’s website (guide, rental, Q&A and news pages) on 28 November 2026. The exact New Year closing dates are not given."),
        time=(VIS, "11:05〜11:30", "11:05–11:30")),

    dict(
        id="arope", name=T("旭岳ロープウェイ", "Asahidake Ropeway"), kind=T("ロープウェイ", "Ropeway"),
        blurb=T("山麓駅から標高1,600mの姿見駅まで約10分。冬は20分おき、下りの最終は15:40。",
                "About 10 minutes from the base to Sugatami Station at 1,600 m. Every 20 minutes in winter; last car down at 15:40."),
        caution=T("冬の下り最終は15:40（12月11日〜2月28日）。強風で運休あり", "Winter last car down 15:40 (11 Dec–28 Feb). Stops in strong wind"),
        lat=43.65310, lng=142.79880,
        text=T("バスの終点の目の前が山麓駅です。標高1,600mの姿見（すがたみ）駅まで約10分。予約はなく、来た順に乗ります。往復は、11月1日〜5月31日が3,000円、6月1日〜10月31日が3,500円（小人はどちらも1,750円）。クレジットカードが使えます。\n\n"
               "冬（12月11日〜2月28日）は9:00〜15:40で、毎時00・20・40分の20分おき。15:40は下りの最終で、上りの最終は15:20です。3月1日〜15日は16:00まで、3月16日〜5月9日は17:00まで。6月1日〜10月20日は15分おきになり、6月20日〜9月30日は6:30（土日祝などは6:00）〜17:30。\n\n"
               "毎年、整備で止まる期間があります。この冬は2026年11月16日〜12月10日、春は2027年5月10日〜21日。その間は食堂と売店も休みです。\n\n"
               "強風や雷で止まります。上にいて風が強くなってきたら、早めに下りてください。下りの最終に乗り遅れて、遭難の扱いになった例があると、公式サイトに書かれています。\n\n"
               "山麓駅の2階に食堂（カレー、ラーメン）、1階に売店とコインロッカー。姿見駅にも売店（コロッケ、コーヒー）とお手洗いがあります。食堂の営業時間は公式サイトに書かれていないので、お昼をここに決めている日は電話（0166-68-9111）で確かめるか、旭川駅で軽い食べ物を買っておくと安心です。",
               "The base station is right in front of the last bus stop. The ride up to Sugatami Station at 1,600 m takes about 10 minutes. No reservations: you board in order of arrival. A return ticket is ¥3,000 from 1 November to 31 May and ¥3,500 from 1 June to 31 October (children ¥1,750 all year). Credit cards are accepted.\n\n"
               "In winter (11 December–28 February) it runs 9:00–15:40, every 20 minutes at :00, :20 and :40. 15:40 is the last car down; the last car up is 15:20. From 1 to 15 March it runs until 16:00, and from 16 March to 9 May until 17:00. From 1 June to 20 October cars run every 15 minutes, and from 20 June to 30 September the hours are 6:30 (6:00 at weekends and on holidays) to 17:30.\n\n"
               "It closes for maintenance every year: this winter from 16 November to 10 December 2026, and in spring from 10 to 21 May 2027. The restaurant and shop close too.\n\n"
               "It stops in strong wind or lightning. If the wind picks up while you are at the top, come down early. The official site notes that people who missed the last car down have been treated as mountain-rescue cases.\n\n"
               "The base station has a restaurant upstairs (curry, ramen), a shop and coin lockers downstairs. Sugatami Station has a shop (croquettes, coffee) and toilets. The restaurant’s hours are not on the website: if you are counting on it for lunch, phone 0166-68-9111, or bring something light from Asahikawa Station."),
        gmaps=[gm("旭岳ロープウェイ 山麓駅", "Asahidake Ropeway base station", 43.65310, 142.79880, "大雪山旭岳ロープウェイ 山麓駅")],
        links=[ROPE, IDEYU],
        rows=[row("hours", "12月11日〜2月28日 9:00〜15:40（下り最終。上り最終15:20）、20分おき", "11 Dec–28 Feb: 9:00–15:40 (last down; last up 15:20), every 20 min", until="2027-02-28"),
              row("hours", "3月1日〜15日 9:00〜16:00、3月16日〜5月9日 9:00〜17:00（20分おき）", "1–15 Mar: 9:00–16:00; 16 Mar–9 May: 9:00–17:00 (every 20 min)", until="2027-05-09"),
              row("hours", "6月1日〜19日 8:00〜17:00、6月20日〜9月30日 6:30（土日祝など6:00）〜17:30、10月1日〜20日 8:00〜17:00（15分おき）、10月21日〜11月15日 9:00〜16:00（2026年の予定表）", "1–19 Jun: 8:00–17:00; 20 Jun–30 Sep: 6:30 (6:00 weekends/holidays)–17:30; 1–20 Oct: 8:00–17:00 (every 15 min); 21 Oct–15 Nov: 9:00–16:00 (2026 calendar)"),
              row("fee", "往復3,000円（11月1日〜5月31日）、3,500円（6月1日〜10月31日）、小人1,750円。カード可", "Return ¥3,000 (1 Nov–31 May), ¥3,500 (1 Jun–31 Oct); children ¥1,750. Cards accepted"),
              row("closed", "整備運休：2026年11月16日〜12月10日、2027年5月10日〜21日", "Closed for maintenance: 16 Nov–10 Dec 2026 and 10–21 May 2027", until="2027-05-21")],
        notices=N_AROPE,
        tip=T("旭岳ロープウェイの公式サイト（運行予定表・運賃・ご注意）で2026年11月28日に確認しました。運行予定表は2027年5月までの分です。",
              "Checked on the Asahidake Ropeway website (operating calendar, fares and notes) on 28 November 2026. The calendar runs to May 2027."),
        time=(VIS, "11:40発の便で上へ（夏は11:45発）。下りは13:20発", "Up on the 11:40 car (11:45 in summer); down on the 13:20")),

    dict(
        id="sugatami", name=T("姿見の池", "Sugatami Pond"), kind=T("山の上の散策", "Walk at the top"),
        blurb=T("姿見駅を出ると、目の前に噴気を上げる旭岳。夏は一周約1時間の散策路、冬は晴れた日にスノーシューで。",
                "Step out of Sugatami Station to steaming Asahidake. A one-hour loop in summer; snowshoes on clear days in winter."),
        caution=T("冬は道が雪の下。見通しのない日は駅から離れないで", "In winter the path is under snow. In poor visibility stay by the station"),
        lat=43.66139, lng=142.83334,
        text=T("姿見駅を出ると、正面が旭岳です。山腹から白い噴気が上がり、晴れて風のない日は、その姿が姿見（すがたみ）の池に映ります。\n\n"
               "雪のない季節（6月〜10月中旬）：駅から、展望台と夫婦池（めおといけ）、姿見の池、噴気孔の近くを回って駅に戻る、一周約1.7km・約1時間の散策路があります。石の多い山道なので、底の厚い靴で。6月はまだ雪が残っていて、姿見駅で長靴を借りられます。雨と風をよける長そでの上着も要ります。高山植物は6月上旬〜8月中旬、紅葉は例年9月中旬〜下旬で、9月中旬の土日祝はロープウェイがとても混みます。\n\n"
               "冬（12月〜5月）：一面の雪で、道は見えません。晴れて見通しのよい日に、スノーシュー（ふもとのビジターセンターで借りる）で駅のまわりから第1展望台のあたりまで歩くのが、初めての人の範囲です。姿見の池まで行くかどうかは、ビジターセンターか駅の係の人に、その日の様子を聞いてから決めてください。雲や吹雪で先が見えない日は、駅舎から離れないこと。入るときに晴れていても急に見えなくなることがよくある、と公式サイトが注意しています。\n\n"
               "冬の服装：スキーウェアかそれに近い上下、帽子、厚い手袋、首と顔をおおうもの、サングラスかゴーグル、雪が入らない冬の靴。標高1,600mで、旭川の街よりずっと寒く、風が強い場所です。今の気温と風速は、ロープウェイの公式サイトのいちばん上に出ています。スマートフォンは寒さで電池が切れやすいので、内ポケットに入れておきます。\n\n"
               "ここから先（旭岳の山頂や裾合平）は登山で、このマップの範囲の外です。",
               "Asahidake is straight ahead as you leave Sugatami Station, with white steam rising from vents on its flank. On a clear, still day the mountain is reflected in Sugatami Pond.\n\n"
               "Snow-free season (June to mid-October): a loop of about 1.7 km and one hour leads from the station past viewpoints and the Meoto ponds to Sugatami Pond and the steam vents, then back. It is a stony mountain path, so wear thick-soled shoes. Snow still lies on it in June, and you can borrow rubber boots at Sugatami Station. Bring a long-sleeved jacket for rain and wind. Alpine flowers bloom from early June to mid-August; autumn colour usually peaks in mid to late September, when the ropeway is very crowded at weekends.\n\n"
               "Winter (December to May): everything is under snow and the path cannot be seen. On a clear day with good visibility, a first-timer’s range is the area from the station to around the first viewpoint, on snowshoes rented at the Visitor Center below. Ask at the Visitor Center or the station about the day’s conditions before deciding whether to go as far as the pond. If cloud or blowing snow hides the way ahead, stay by the station building. The official site warns that visibility often collapses suddenly even when it was clear at the start.\n\n"
               "Winter clothing: ski wear or something close to it, a hat, thick gloves, a neck and face cover, sunglasses or goggles, and winter boots that keep snow out. At 1,600 m it is far colder and windier than in Asahikawa. The ropeway’s website shows the current temperature and wind speed at the top of its home page. Phone batteries die fast in the cold: keep yours in an inside pocket.\n\n"
               "Beyond here (the summit of Asahidake, Susoaidaira) is mountaineering and outside this map."),
        gmaps=[gm("姿見の池", "Sugatami Pond", 43.66139, 142.83334, "姿見の池 旭岳"),
               gm("旭岳ロープウェイ 姿見駅", "Sugatami Station", 43.66190, 142.82499, "旭岳ロープウェイ 姿見駅")],
        links=[ROPE, link("info", "姿見の池 周辺散策路の地図（ビジターセンター）", "Map of the Sugatami Pond trails (Visitor Center, Japanese)", U["avc_course"]), AVC],
        rows=[row("hours", "ロープウェイの時間の中で。冬は下り最終15:40（12月11日〜2月28日）", "Within ropeway hours. In winter the last car down is 15:40 (11 Dec–28 Feb)"),
              row("fee", "散策は無料（ロープウェイ往復3,000〜3,500円）", "The walk is free (ropeway return ¥3,000–3,500)"),
              row("closed", "散策路を歩けるのは6月〜10月中旬。冬は雪の上をスノーシューで（道しるべは雪の下）", "The path is walkable June to mid-October. In winter it is snowshoes over deep snow (the path is buried)")],
        notices=N_COLD,
        tip=T("散策路の距離と時間、装備、冬の注意は旭岳ロープウェイの公式サイト、見ごろとレンタルは旭岳ビジターセンターの公式サイトで2026年11月28日に確認しました。",
              "Trail length, time, gear and winter warnings from the Asahidake Ropeway website; seasons and rental from the Asahidake Visitor Center website. Checked on 28 November 2026."),
        time=(VIS, "11:50〜13:15", "11:50–13:15")),

    dict(
        id="aonsen", name=T("旭岳温泉の日帰り入浴", "Day baths at Asahidake Onsen"), kind=T("温泉", "Hot spring"),
        blurb=T("森の中の宿で日帰り入浴。タトゥーがあっても入れると公式に書いているのは、ケイズハウス北海道（15:00から）。",
                "Day-use baths at lodges in the forest. K’s House Hokkaido (from 15:00) says officially that tattoos are fine."),
        caution=T("最終バスは16:55。お風呂は16:30までに上がる", "Last bus 16:55: be out of the bath by 16:30"),
        lat=43.65071, lng=142.79902,
        text=T("旭岳温泉には温泉街がなく、森の中の道沿いに宿が点々とあります。日帰りで入れる宿は次のとおりです。\n\n"
               "・ケイズハウス北海道：15:00〜19:00、900円。公式サイトの英語のよくある質問に、タトゥーがあっても温泉に入れると書いてあります。内湯と露天風呂。休みの日と短い営業の日があるので、公式サイトのカレンダーで確かめてください。バス停「旭岳温泉入口」の目の前です。\n\n"
               "・ホテルベアモンテ：12:30〜19:00（受付18:00まで）、1,140円。フェイスタオル110円、バスタオル220円。大浴場にサウナつき。ロープウェイの駅から坂を下って歩いて5分で、バス停「ホテルベアモンテ前」があります。タトゥーの記載なし（要確認）。\n\n"
               "・湯元 湧駒荘（ゆこまんそう）の別館「神々の湯」：受付12:00〜18:00（19:00まで）、1,200円。バスタオルの貸し出し300円、フェイスタオル200円。バス停「旭岳温泉入口」のそば。タトゥーの記載なし（要確認）。\n\n"
               "・大雪山白樺荘：13:00〜19:00、800円（ひがしかわ観光協会の案内）。宿の公式サイトには日帰り入浴のことが書かれておらず、宿が休みの期間もあるので、行く前に電話で確認を。\n\n"
               "時間割：ロープウェイを下りてお昼のあと、ベアモンテなら歩いてすぐ。ケイズハウスと湧駒荘は、ロープウェイの駅から道を約1km下ったところで、歩いて15〜20分（冬は雪道）。14:55発のバスなら2分、250円です。\n\n"
               "帰りの最終バスは、ホテルベアモンテ前16:55発、旭岳温泉入口16:57発。お風呂は16:30までに上がって、バス停で待ちましょう。",
               "Asahidake Onsen has no town centre: the lodges are spread along the road through the forest. These take day visitors.\n\n"
               "• K’s House Hokkaido (a backpackers’ lodge): 15:00–19:00, ¥900. Its English FAQ says guests with tattoos are welcome in the hot spring. Indoor and outdoor baths. It closes on some days and shortens hours on others, so check the calendar on its website. Right in front of the Asahidake Onsen Iriguchi bus stop.\n\n"
               "• Hotel Bear Monte: 12:30–19:00 (last entry 18:00), ¥1,140. Face towel ¥110, bath towel ¥220. Saunas in the bath hall. Five minutes’ walk down the hill from the ropeway station, with its own bus stop (Hotel Bear Monte-mae). Nothing on tattoos (please check).\n\n"
               "• Yumoto Yukomanso, annexe bath “Kamigami-no-yu”: entry 12:00–18:00 (open until 19:00), ¥1,200. Bath towel rental ¥300, face towel ¥200. Near the Asahidake Onsen Iriguchi stop. Nothing on tattoos (please check).\n\n"
               "• Daisetsuzan Shirakabaso: 13:00–19:00, ¥800 according to the Higashikawa Tourism Association. The lodge’s own website does not mention day bathing and the lodge closes for some periods, so phone first.\n\n"
               "Timing: after the ropeway and lunch, Bear Monte is a short walk. K’s House and Yukomanso are about 1 km down the road from the ropeway station, 15–20 minutes on foot (on snow in winter), or 2 minutes and ¥250 on the 14:55 bus.\n\n"
               "The last bus back stops at Hotel Bear Monte-mae at 16:55 and Asahidake Onsen Iriguchi at 16:57. Be out of the bath by 16:30 and wait at the stop."),
        gmaps=[gm("ケイズハウス北海道", "K’s House Hokkaido", 43.64774, 142.78756, "ケイズハウス北海道 旭岳温泉"),
               gm("ホテルベアモンテ", "Hotel Bear Monte", 43.65071, 142.79902, "旭岳温泉 ホテルベアモンテ"),
               gm("湯元 湧駒荘", "Yumoto Yukomanso", 43.64784, 142.78992, "湯元 湧駒荘")],
        links=[link("official", "ケイズハウス北海道（休みのカレンダー）", "K’s House Hokkaido (closing-day calendar)", U["ks"], U["ks_en"]),
               link("official", "ホテルベアモンテ 日帰り入浴", "Hotel Bear Monte day bath (Japanese)", U["bear"]),
               link("official", "湯元 湧駒荘 日帰り利用", "Yukomanso day use (Japanese)", U["yukoman"]),
               link("info", "旭岳温泉の日帰り入浴（ひがしかわ観光協会）", "Day baths at Asahidake Onsen (Japanese)", U["hk_onsen"])],
        rows=[row("tattoo", "ケイズハウス北海道は可（公式サイト）。ベアモンテ・湧駒荘・白樺荘は記載なし＝要確認", "OK at K’s House Hokkaido (official site). Bear Monte, Yukomanso, Shirakabaso: not stated, please check"),
              row("hours", "ケイズハウス15:00〜19:00（休みの日あり）／ベアモンテ12:30〜19:00（受付18:00まで）／湧駒荘 受付12:00〜18:00", "K’s House 15:00–19:00 (some closed days) / Bear Monte 12:30–19:00 (entry to 18:00) / Yukomanso entry 12:00–18:00"),
              row("fee", "ケイズハウス900円／ベアモンテ1,140円／湧駒荘1,200円／白樺荘800円", "K’s House ¥900 / Bear Monte ¥1,140 / Yukomanso ¥1,200 / Shirakabaso ¥800"),
              row("bus", "最終 ホテルベアモンテ前16:55発、旭岳温泉入口16:57発 → 旭川駅18:33着", "Last bus: Hotel Bear Monte-mae 16:55, Asahidake Onsen Iriguchi 16:57 → Asahikawa Station 18:33")],
        notices=[N_TATTOO_A],
        tip=T("各宿の公式サイトと、ひがしかわ観光協会の「旭岳温泉日帰り入浴」の表で2026年11月28日に確認しました。支払い方法は書かれていないので、現金を用意してください。",
              "Checked on each lodge’s website and the Higashikawa Tourism Association’s day-bath table on 28 November 2026. Payment methods are not stated, so bring cash."),
        cash=True,
        time=(VIS, "14:20〜16:30（ケイズハウスは15:00から）", "14:20–16:30 (K’s House from 15:00)")),

    dict(
        id="higashikawa", name=T("東川町", "Higashikawa"), kind=T("帰り道の町", "Town on the way back"),
        blurb=T("旭岳14:55発のバスで途中下車。道の駅とカフェ、ブルワリーを歩いて、17:34発で旭川へ。",
                "Get off the 14:55 bus here: a roadside market, a café and a brewery on foot, then the 17:34 on to Asahikawa."),
        caution=T("旭川へのいで湯号は道草館17:34発が最後", "Last Ideyu-go to Asahikawa leaves Michikusa-kan at 17:34"),
        lat=43.69724, lng=142.50879,
        text=T("東川（ひがしかわ）は旭岳のふもとの町で、「写真の町」として知られています。いで湯号が町の真ん中の道の駅「ひがしかわ道草館（みちくさかん）」に止まるので、帰りに途中下車できます。\n\n"
               "旭岳14:55発 → 道草館15:34着（1,450円）。町を歩いて、道草館17:34発 → 旭川駅18:33着（1,110円）。17:34発が、旭川へ戻る最後のいで湯号です。\n\n"
               "・道の駅ひがしかわ「道草館」：9:00〜17:00（4〜9月は18:00まで）。12月31日〜1月4日は休み。町の店のパンや菓子、米、酒が並び、町の地図（グルメマップ）がもらえます。おにぎりやパンは昼すぎには売り切れることがあります。お手洗いは24時間。\n"
               "・CAFEtune：道草館から歩いて5分、YAMAtune 大雪山店に併設のカフェ。10:00〜17:00、木曜と不定休。コーヒーとホットドッグ。\n"
               "・NATURES Brewing：クラフトビールの醸造所とタップルーム（東町3丁目）。15:00〜21:00、月・木曜休み。\n\n"
               "お昼だけ開けている店（うどん、おむすびなど）は、この時間にはもう閉まっています。\n\n"
               "9:15発のバスで来た日は、東川に寄ると温泉に入る時間がありません。温泉も東川も、という日は旭川7:15発で出て、姿見の池→お昼→温泉（12時台から入れるベアモンテか湧駒荘）→14:55発のバスで東川へ。",
               "Higashikawa is the town at the foot of Asahidake, known in Japan as the “town of photography”. The Ideyu-go stops at the roadside market Higashikawa Michikusa-kan in the middle of town, so you can break the ride back here.\n\n"
               "Asahidake 14:55 → Michikusa-kan 15:34 (¥1,450). Walk around town, then Michikusa-kan 17:34 → Asahikawa Station 18:33 (¥1,110). The 17:34 is the last Ideyu-go to Asahikawa.\n\n"
               "• Michi-no-Eki Higashikawa “Michikusa-kan”: 9:00–17:00 (to 18:00 April–September), closed 31 December–4 January. Bread and sweets from shops in town, local rice and sake, and a free food map of the town. Rice balls and bread can sell out soon after noon. Toilets open 24 hours.\n"
               "• CAFEtune: five minutes’ walk from Michikusa-kan, inside the YAMAtune Daisetsuzan shop. 10:00–17:00, closed Thursdays and some other days. Coffee and hot dogs.\n"
               "• NATURES Brewing: a craft brewery with a taproom (Higashimachi 3-chome). 15:00–21:00, closed Mondays and Thursdays.\n\n"
               "Lunch-only places (udon, rice balls) have already closed by this time of day.\n\n"
               "If you came on the 9:15 bus, stopping in Higashikawa leaves no time for a bath. To do both, leave Asahikawa at 7:15: Sugatami Pond, lunch, a bath (Bear Monte and Yukomanso open around noon), then the 14:55 bus to Higashikawa."),
        gmaps=[gm("道の駅ひがしかわ「道草館」", "Higashikawa Michikusa-kan", 43.69724, 142.50879, "道の駅ひがしかわ 道草館"),
               gm("CAFEtune（YAMAtune 大雪山店）", "CAFEtune (YAMAtune)", 43.69517, 142.51168, "YAMAtune 大雪山店 CAFEtune"),
               gm("NATURES Brewing", "NATURES Brewing", 43.69724, 142.50879, "NATURES Brewing 東川町東町3丁目6-8")],
        links=[link("info", "道の駅ひがしかわ「道草館」", "Michikusa-kan (Japanese)", U["michikusa"]),
               link("info", "東川のグルメ情報（ひがしかわ観光協会）", "Places to eat in Higashikawa (Japanese)", U["hk_gourmet"]), IDEYU],
        rows=[row("bus", "旭岳14:55 → 道草館15:34、1,450円。道草館17:34 → 旭川駅18:33、1,110円（最終）", "Asahidake 14:55 → Michikusa-kan 15:34, ¥1,450. Michikusa-kan 17:34 → Asahikawa Station 18:33, ¥1,110 (last bus)"),
              row("hours", "道草館 9:00〜17:00（4〜9月は18:00まで）／CAFEtune 10:00〜17:00／NATURES Brewing 15:00〜21:00", "Michikusa-kan 9:00–17:00 (to 18:00 Apr–Sep) / CAFEtune 10:00–17:00 / NATURES Brewing 15:00–21:00"),
              row("closed", "道草館 12月31日〜1月4日／CAFEtune 木曜・不定休／NATURES Brewing 月・木曜", "Michikusa-kan 31 Dec–4 Jan / CAFEtune Thursdays and irregular days / NATURES Brewing Mondays and Thursdays")],
        notices=[],
        tip=T("ひがしかわ観光協会のページ（道草館・グルメ情報の各店）と、いで湯号の時刻表・運賃表で2026年11月28日に確認しました。",
              "Checked on the Higashikawa Tourism Association’s pages (Michikusa-kan and each shop) and the Ideyu-go timetable and fare table on 28 November 2026."),
        time=(VIS, "15:34〜17:34", "15:34–17:34")),
]

# ---------------------------------------------------------------------------
# 層雲峡のコース
# ---------------------------------------------------------------------------
SOUNKYO = [
    dict(
        id="sstart", name=T("旭川駅から層雲峡へ", "Asahikawa to Sounkyo"), kind=T("出発・バス", "Start: bus"),
        blurb=T("旭川駅前9:55発の道北バスで約2時間。旭川へ戻る最後のバスは層雲峡17:00発。",
                "The 9:55 Dohoku Bus from Asahikawa Station takes about two hours. The last bus back to Asahikawa leaves at 17:00."),
        caution=T("旭川行きの最終バスは層雲峡17:00発。Kitaca・Suicaの案内なし", "Last bus to Asahikawa 17:00. Kitaca/Suica not listed"),
        lat=43.76300, lng=142.35960,
        text=T("層雲峡（そううんきょう）は、石狩川が大雪山のふもとを削った、約24km続く断崖の谷です。その中ほどに温泉街があり、黒岳（くろだけ）の5合目へ上がるロープウェイが出ています。\n\n"
               "旭川駅前の8番のりばから、道北バスの「層雲峡・上川線」9:55発に乗り、終点の層雲峡に11:54着。片道2,140円で、予約は要りません。支払いは現金か、スマートフォンで買うモバイルチケット（道北バスの公式サイトから）。クレジットカードのタッチ決済は「層雲峡線の一部」と案内されているので、あてにしないで現金を用意してください。JRのレールパスは使えません。\n\n"
               "帰りは、層雲峡17:00発（旭川駅前18:55着）が旭川まで行く最後のバスです。その前は14:40発（16:35着）。\n\n"
               "もっと遅くまで残る日（氷瀑まつりの夜など）：層雲峡18:55発のバスは上川（かみかわ）止まりで、JR上川駅の横の「上川森のテラス バスタッチ」に19:25着（890円）。上川20:24発の普通列車（旭川21:22着）か、21:04発の特別快速（旭川21:44着）に乗り継ぎます（1,380円）。上川で1時間ほど待ちます。\n\n"
               "朝早く出るなら6:55発（層雲峡8:54着）。黒岳のスノーシューツアー（9:30集合）に出る日や、夏にリフトで7合目まで上がって歩く日はこちらで。\n\n"
               "レールパスを使う人は、旭川〜上川をJR石北本線で行き、上川から同じバスに乗れます（上川森のテラス バスタッチ9:30・10:50・11:24発など、層雲峡まで約30分、890円）。列車は本数が少ないので、乗換案内で確かめてください。\n\n"
               "旭川に戻ったあとの晩ごはんは、駅前から歩ける買物公園のあたりで。",
               "Sounkyo is a gorge about 24 km long that the Ishikari river has cut along the foot of the Daisetsuzan mountains. A hot-spring town sits in the middle of it, with a ropeway up to the fifth station of Mt Kurodake.\n\n"
               "From stop 8 outside Asahikawa Station, take the 9:55 Dohoku Bus on the Sounkyo–Kamikawa line to the last stop, Sounkyo, arriving at 11:54. The fare is ¥2,140 one way; no booking. Pay cash, or buy a mobile ticket on your phone through Dohoku Bus’s website. Contactless card payment is listed only for “some buses on the Sounkyo line”, so do not count on it: carry cash. Japan Rail passes are not valid.\n\n"
               "The 17:00 from Sounkyo (Asahikawa Station 18:55) is the last bus that goes all the way to Asahikawa. The one before leaves at 14:40 (arrives 16:35).\n\n"
               "Staying later, for example for the Ice Fall Festival at night: the 18:55 bus from Sounkyo goes only as far as Kamikawa, reaching the Kamikawa Mori-no-Terrace bus stop beside JR Kamikawa Station at 19:25 (¥890). From there take the 20:24 local train (Asahikawa 21:22) or the 21:04 rapid (Asahikawa 21:44), ¥1,380. Expect to wait about an hour at Kamikawa.\n\n"
               "For an earlier start take the 6:55 bus (Sounkyo 8:54): you need it for the Kurodake snowshoe tour (meets at 9:30) or for a summer day riding the chairlift to the seventh station and walking.\n\n"
               "Rail-pass holders can ride the JR Sekihoku line from Asahikawa to Kamikawa and join the same bus there (from Kamikawa Mori-no-Terrace at 9:30, 10:50, 11:24 and so on; about 30 minutes to Sounkyo, ¥890). Trains are few, so check a route planner.\n\n"
               "Back in Asahikawa, dinner is a short walk from the station around the Kaimono Koen pedestrian street."),
        gmaps=[gm("旭川駅前バスのりば", "Bus stops outside Asahikawa Station", 43.76300, 142.35960, "旭川駅前 バスのりば 8番 道北バス"),
               gm("層雲峡バスターミナル", "Sounkyo Bus Terminal", 43.72614, 142.94823, "層雲峡バスターミナル")],
        links=[DOHOKU, DOHOKU2, link("info", "層雲峡へのアクセス（層雲峡観光協会）", "Getting to Sounkyo (Japanese)", U["sk_access"])],
        rows=[row("bus", "旭川駅前（8番のりば）9:55 → 層雲峡11:54（朝は6:55 → 8:54）、2,140円", "Asahikawa Station (stop 8) 9:55 → Sounkyo 11:54 (earlier: 6:55 → 8:54), ¥2,140"),
              row("bus", "帰り 層雲峡14:40 → 旭川駅前16:35、17:00 → 18:55（旭川行きの最終）", "Back: Sounkyo 14:40 → Asahikawa Station 16:35; 17:00 → 18:55 (last bus to Asahikawa)"),
              row("train", "遅い帰り：層雲峡18:55 → 上川19:25（バス890円）、上川20:24 → 旭川21:22（JR 1,380円。2026年12月のダイヤ）", "Late return: Sounkyo 18:55 → Kamikawa 19:25 (bus ¥890), Kamikawa 20:24 → Asahikawa 21:22 (JR ¥1,380; December 2026 timetable)", until="2027-03-12")],
        notices=N_KURO + N_HYOBAKU + N_COLD,
        cash=True,
        tip=T("バスは道北バスの公式の時刻表（2026年7月1日改正）、JRは乗換案内（2026年12月3日・5日）で、2026年11月28日に確認しました。JRは2027年3月にダイヤ改正の見込みです。",
              "Buses from Dohoku Bus’s timetable (revised 1 July 2026), trains from a route planner (3 and 5 December 2026); checked on 28 November 2026. JR timetables are expected to change in March 2027."),
        time=(DEP, "9:55（旭川駅前 8番のりば）", "9:55 from stop 8 outside Asahikawa Station")),

    dict(
        id="sgai", name=T("層雲峡温泉街（お昼とビジターセンター）", "Sounkyo Onsen town: lunch & Visitor Center"), kind=T("温泉街・お昼", "Town & lunch"),
        blurb=T("バスを降りると、もう温泉街の中。お昼を食べて、ビジターセンターで山と谷の様子を見ます。",
                "The bus drops you in the middle of town. Have lunch, then see the day’s conditions at the Visitor Center."),
        caution=T("冬は開いている店が少ない。ビジターセンターは11〜5月の月曜休み", "Few places open in winter. Visitor Center closed Mondays, Nov–May"),
        lat=43.72614, lng=142.94823,
        text=T("バスターミナルを出ると、坂道の両側にホテルと店が並ぶ小さな温泉街です。歩いて5分ほどで端まで行けて、ロープウェイの駅は坂のいちばん上にあります。\n\n"
               "お昼は、次のどちらかで。\n"
               "・大雪山食堂：ラーメンの店。11:00〜15:00と17:30〜20:30、不定休。バスターミナルから歩いて2〜3分。\n"
               "・ビアグリル・キャニオン：洋食とイタリア料理。11:30〜15:00と17:30〜20:00、水曜休み。\n"
               "ロープウェイで上がった5合目の駅にも「ともちゃん食堂」（11:00〜15:30、不定休）があります。ラーメンの「登山軒」は11月〜5月は休業です。冬は開いている店が少ないので、旭川駅で軽い食べ物を買っておくと安心です。\n\n"
               "層雲峡ビジターセンター：ロープウェイの駅の手前。大雪山の地形や動物の展示と、その日の山と遊歩道の情報があります。9:00〜17:00、無料。6〜10月は無休、11〜5月は月曜休み（祝日なら翌日）、12月31日〜1月5日は休み。\n\n"
               "荷物：黒岳ロープウェイの層雲峡駅にコインロッカーがあります（大きさと数は要確認）。",
               "Outside the bus terminal is a small hot-spring town: one sloping street lined with hotels and shops. It takes about five minutes to walk from end to end, and the ropeway station is at the top of the slope.\n\n"
               "For lunch, choose one of these.\n"
               "• Daisetsuzan Shokudo: ramen. 11:00–15:00 and 17:30–20:30, irregular closing days. Two or three minutes’ walk from the bus terminal.\n"
               "• Beer Grill Canyon: Western and Italian dishes. 11:30–15:00 and 17:30–20:00, closed Wednesdays.\n"
               "There is also Tomo-chan Shokudo (11:00–15:30, irregular closing days) in the ropeway’s fifth-station building. The ramen shop Tozanken is closed from November to May. Few places open in winter, so it is wise to bring something light from Asahikawa Station.\n\n"
               "Sounkyo Visitor Center: just below the ropeway station. Exhibits on the geology and wildlife of Daisetsuzan, and today’s information on the mountain and trails. 9:00–17:00, free. Open daily June–October; closed Mondays November–May (the next day if Monday is a holiday) and 31 December–5 January.\n\n"
               "Luggage: there are coin lockers in the ropeway’s Sounkyo Station (sizes and number: please check)."),
        gmaps=[gm("層雲峡バスターミナル", "Sounkyo Bus Terminal", 43.72614, 142.94823, "層雲峡バスターミナル"),
               gm("大雪山食堂", "Daisetsuzan Shokudo", 43.72664, 142.94671, "大雪山食堂 層雲峡"),
               gm("ビアグリル・キャニオン", "Beer Grill Canyon", 43.72614, 142.94823, "ビアグリル キャニオン 層雲峡"),
               gm("層雲峡ビジターセンター", "Sounkyo Visitor Center", 43.72477, 142.94634, "層雲峡ビジターセンター")],
        links=[link("info", "層雲峡ビジターセンター", "Sounkyo Visitor Center", U["sk_vc"], U["sk_vc_en"]),
               link("info", "大雪山食堂（層雲峡観光協会）", "Daisetsuzan Shokudo (Japanese)", U["sk_shokudo"]),
               link("info", "ビアグリル・キャニオン（層雲峡観光協会）", "Beer Grill Canyon (Japanese)", U["sk_canyon"]), SK],
        rows=[row("food", "大雪山食堂 11:00〜15:00・17:30〜20:30（不定休）／ビアグリル・キャニオン 11:30〜15:00・17:30〜20:00（水曜休み）", "Daisetsuzan Shokudo 11:00–15:00, 17:30–20:30 (irregular days off) / Beer Grill Canyon 11:30–15:00, 17:30–20:00 (closed Wed)"),
              row("hours", "ビジターセンター 9:00〜17:00、無料", "Visitor Center 9:00–17:00, free"),
              row("closed", "ビジターセンター：11〜5月は月曜（祝日なら翌日）、12月31日〜1月5日。6〜10月は無休", "Visitor Center: Mondays Nov–May (next day if a holiday), 31 Dec–5 Jan. Open daily Jun–Oct")],
        notices=[],
        cash=True,
        tip=T("店の時間は層雲峡観光協会の各店のページ、ビジターセンターは公式サイトで2026年11月28日に確認しました。店の支払い方法は書かれていないので、現金を用意してください。",
              "Restaurant hours from the Sounkyo Tourist Association’s pages, the Visitor Center from its own site; checked on 28 November 2026. Payment methods are not stated, so bring cash."),
        time=(VIS, "11:55〜12:35（お昼）。ビジターセンターはロープウェイのあと", "11:55–12:35 for lunch; the Visitor Center after the ropeway")),

    dict(
        id="kurodake", name=T("黒岳ロープウェイ（5合目）", "Kurodake Ropeway (5th station)"), kind=T("ロープウェイ・展望台", "Ropeway & lookout"),
        blurb=T("温泉街から標高1,300mの5合目まで7分。屋上の展望台から、黒岳と層雲峡の谷。夏はリフトで7合目へ。",
                "Seven minutes from town to the fifth station at 1,300 m; a rooftop lookout over Kurodake and the gorge. In summer a chairlift goes on to the seventh station."),
        caution=T("12:20の便は運休。冬は16:00まで（上り最終15:20）。冬のリフトは滑る人だけ", "No 12:20 car. Winter hours to 16:00 (last up 15:20). Winter chairlift for skiers only"),
        lat=43.72405, lng=142.94697,
        text=T("温泉街（標高670m）の層雲峡駅から、黒岳5合目の黒岳駅（1,300m）まで7分。20分おきに出ますが、12:20の便は運休です（係の人の昼休みのため、と公式サイトにあります）。往復3,000円、小学生1,500円。2027年6月1日から料金が変わります。\n\n"
               "冬の時間（12月1日〜6月20日）は8:00〜16:00で、上りの最終は15:20。6月21日〜9月30日は6:00〜18:00、10月1日〜15日は7:00〜17:00。毎年11月に整備で止まります（2026年は11月9日〜30日）。\n\n"
               "5合目の駅の屋上が「黒岳ネイチャーテラス」という展望台で、黒岳と、柱のような岩が並ぶ層雲峡の谷を見渡せます。駅の中に、大雪山の資料館、売店、ともちゃん食堂（11:00〜15:30）。お手洗いはこの駅が最後です。\n\n"
               "雪のない季節（6月〜10月15日）：駅のまわりに一周約30分の散策路があります。さらにペアリフト（片道15分、往復1,200円。ロープウェイとのセット往復は3,900円）で7合目（1,520m）へ。7合目から片道約15分の「黒岳カムイの森のみち」を歩くと、あまりょうの滝の展望台です。リフトにも乗るなら、ロープウェイと合わせて2時間はみてください。黒岳の山頂（1,984m）は7合目から登山道を約1時間半で、登山の用意が要ります。\n\n"
               "冬（12月〜5月上旬）：5合目から上はスキー場になり、冬のリフトはスキーやスノーボードを持った人しか乗れません。滑らない人は、テラスからの雪山と、駅の中で過ごします。雪の上を歩きたい人には、ガイドつきの「くろだけスノーシューハイキング」（2027年1月5日〜3月10日）。5合目を歩くショートコースは約2時間、大人7,000円で、ロープウェイ往復・スノーシュー・ブーツ・スキーウェアの貸し出し込み。9:30までに山麓の窓口に集合なので、旭川6:55発のバスで来ます。前日か当日に、電話（01658-5-3031）か窓口で申し込みます（英語で参加できるかは要確認）。\n\n"
               "強風や吹雪で止まることがあります。公式サイトのいちばん上に、その日の運行状況が朝7:00に出ます。",
               "From Sounkyo Station in the town (670 m) to Kurodake Station at the fifth station (1,300 m) takes 7 minutes. Cars leave every 20 minutes, except that the 12:20 car does not run (the official site says it is the crew’s lunch break). Return ¥3,000, primary-school children ¥1,500. Fares change on 1 June 2027.\n\n"
               "Winter hours (1 December–20 June) are 8:00–16:00, with the last car up at 15:20. From 21 June to 30 September it runs 6:00–18:00, and from 1 to 15 October 7:00–17:00. It closes for maintenance every November (9–30 November in 2026).\n\n"
               "The roof of the fifth-station building is a lookout, the Kurodake Nature Terrace, facing Kurodake and the gorge with its walls of rock columns. Inside are a small museum on Daisetsuzan, a shop and Tomo-chan Shokudo (11:00–15:30). These are the last toilets on the mountain.\n\n"
               "Snow-free season (June to 15 October): a loop path of about 30 minutes circles the station. A pair chairlift (15 minutes each way, return ¥1,200; ¥3,900 return combined with the ropeway) goes on to the seventh station (1,520 m), where a 15-minute path, the Kamui Forest Trail, leads to a lookout over Amaryo Falls. Allow two hours in all if you ride the lift. The summit of Kurodake (1,984 m) is about 90 minutes’ climb from the seventh station and needs proper hiking gear.\n\n"
               "Winter (December to early May): above the fifth station is a ski area, and the winter chairlift takes only people carrying skis or a snowboard. Non-skiers have the terrace view of the snow-covered mountains and the station building. To walk on the snow, join the guided Kurodake Snowshoe Hiking tour (5 January–10 March 2027): the short course around the fifth station takes about two hours and costs ¥7,000 for adults, including the ropeway, snowshoes, boots and ski wear. It meets at the base-station ticket window by 9:30, so take the 6:55 bus from Asahikawa. Book the day before or on the day by phone (01658-5-3031) or at the window (whether you can join in English: please check).\n\n"
               "Strong wind or blizzards can stop the ropeway. The day’s status appears at the top of the official site at 7:00."),
        gmaps=[gm("黒岳ロープウェイ 層雲峡駅", "Kurodake Ropeway, Sounkyo Station", 43.72405, 142.94697, "黒岳ロープウェイ 層雲峡駅"),
               gm("黒岳駅（5合目）", "Kurodake Station (5th station)", 43.71106, 142.94023, "黒岳ロープウェイ 黒岳駅 5合目")],
        links=[KURO, link("official", "料金・営業時間", "Fares and hours (Japanese)", U["kuro_about"]),
               link("official", "スノーシューハイキング", "Snowshoe hiking tour (Japanese)", U["kuro_tour"])],
        rows=[row("hours", "12月1日〜6月20日 8:00〜16:00（上り最終15:20）。20分おき、12:20の便は運休", "1 Dec–20 Jun: 8:00–16:00 (last up 15:20). Every 20 min; no 12:20 car"),
              row("hours", "6月21日〜9月30日 6:00〜18:00、10月1日〜15日 7:00〜17:00（上り最終は終了の40分前）", "21 Jun–30 Sep: 6:00–18:00; 1–15 Oct: 7:00–17:00 (last up 40 min before closing)"),
              row("fee", "往復3,000円、小学生1,500円（2027年5月31日まで。6月1日から変更）", "Return ¥3,000, primary-school children ¥1,500 (until 31 May 2027; changes on 1 June)", until="2027-05-31"),
              row("fee", "リフト（夏だけ）往復1,200円、ロープウェイとのセット往復3,900円", "Chairlift (summer only) return ¥1,200; ropeway + lift return ¥3,900", until="2027-05-31"),
              row("closed", "整備運休：ロープウェイ11月9日〜30日、リフト10月16日〜11月30日（2026年）", "Closed for maintenance: ropeway 9–30 Nov, chairlift 16 Oct–30 Nov (2026)", until="2026-11-30")],
        notices=N_KURO + N_COLD,
        tip=T("黒岳ロープウェイの公式サイト（料金・営業時間、駅の施設、ツアー、お知らせ）で2026年11月28日に確認しました。2027年6月からの新しい料金は、公式サイトに画像で出ています。",
              "Checked on the Kurodake Ropeway website (fares and hours, facilities, tours, news) on 28 November 2026. The new fares from June 2027 are shown as an image on that site."),
        time=(VIS, "12:40発の便で上へ、13:40ごろ下りる（7〜10月に滝へ行く日は14:20発で上へ）", "Up on the 12:40 car, down around 13:40 (on a July–October day with the falls: up on the 14:20)")),

    dict(
        id="taki", name=T("銀河の滝・流星の滝", "Ginga & Ryusei Falls"), kind=T("滝", "Waterfalls"),
        blurb=T("断崖を落ちる2本の滝。バスは7月〜10月だけ、1日1往復（12:50発、14:00戻り）。",
                "Two waterfalls down the gorge wall. A bus runs only July–October, once a day (out 12:50, back 14:00)."),
        caution=T("バスは7月1日〜10月31日だけ。ほかの季節はタクシー", "Bus 1 July–31 October only. Taxi in other seasons"),
        lat=43.71885, lng=142.97751,
        text=T("温泉街から国道39号を上流へ約3km。断崖を落ちる2本の滝で、細く分かれて落ちるのが銀河（ぎんが）の滝、太い1本で落ちるのが流星（りゅうせい）の滝。日本の滝百選です。バス停のある駐車場から、どちらも目の前に見えます。滝を背にして斜面の道を20分ほど登ると「双瀑台（そうばくだい）」で、2本を同時に見られます。無料、通年。\n\n"
               "7月1日〜10月31日はバスがあります（1日1往復）。層雲峡12:50発 → 滝見台13:09着、帰りは滝見台13:49発 → 層雲峡14:00着。片道220円。滝にいられるのは40分で、帰りのバスはこの1本だけです。双瀑台まで登るなら、着いてすぐに登り始めてください。この日は、お昼を12:40までに済ませ、ロープウェイは滝から戻った14:20発に乗ります。\n\n"
               "それ以外の季節はバスがありません。行くならタクシーで（層雲峡ハイヤー 01658-5-3221。料金は要確認）。冬は滝が凍り、双瀑台への道は雪の中です。",
               "About 3 km up the gorge from the town along Route 39, two waterfalls drop down the cliff: Ginga (“Milky Way”), which falls in fine threads, and Ryusei (“Shooting Star”), a single heavy column. Both are on the list of Japan’s top 100 waterfalls. You can see them from the car park where the bus stops. With your back to the falls, a path climbs the slope for about 20 minutes to Sobakudai, a lookout from which both are visible at once. Free, all year.\n\n"
               "From 1 July to 31 October there is a bus, once a day: Sounkyo 12:50 → Takimidai 13:09, and back Takimidai 13:49 → Sounkyo 14:00. ¥220 each way. That gives you 40 minutes at the falls, and it is the only bus back. If you want to climb to Sobakudai, start as soon as you arrive. On this plan, finish lunch by 12:40 and ride the ropeway at 14:20 after you return.\n\n"
               "In other seasons there is no bus: go by taxi (Sounkyo Hire, 01658-5-3221; fare: please check). In winter the falls freeze and the path to Sobakudai is under snow."),
        gmaps=[gm("銀河・流星の滝（滝見台）", "Ginga & Ryusei Falls car park", 43.71885, 142.97751, "銀河の滝 流星の滝 駐車場"),
               gm("双瀑台", "Sobakudai lookout", 43.71933, 142.97877, "双瀑台 層雲峡")],
        links=[link("info", "銀河・流星の滝（層雲峡観光協会）", "Ginga & Ryusei Falls (Japanese)", U["sk_taki"]), DOHOKU],
        rows=[row("bus", "7月1日〜10月31日だけ：層雲峡12:50 → 滝見台13:09、滝見台13:49 → 層雲峡14:00、220円（2026年の時刻表）", "1 Jul–31 Oct only: Sounkyo 12:50 → Takimidai 13:09; Takimidai 13:49 → Sounkyo 14:00; ¥220 (2026 timetable)"),
              row("fee", "無料", "Free"),
              row("closed", "11月〜6月はバスなし（タクシーで）", "No bus November–June (taxi only)")],
        notices=[],
        tip=T("バスは道北バスの公式の時刻表（2026年7月1日改正）、滝の案内は層雲峡観光協会のページで2026年11月28日に確認しました。2027年のバスの運行期間は未発表です。",
              "Bus from Dohoku Bus’s timetable (revised 1 July 2026), the falls from the Sounkyo Tourist Association’s page; checked on 28 November 2026. The 2027 bus season has not been announced."),
        time=(VIS, "13:09〜13:49（7月〜10月のバスで）", "13:09–13:49 (by the July–October bus)")),

    dict(
        id="obako", name=T("大函（おおばこ）", "Obako"), kind=T("峡谷", "Gorge"),
        blurb=T("柱のように割れた岩の壁が、川の両側に屏風のように並ぶ場所。温泉街から約6km。",
                "Walls of rock columns standing like folding screens on both sides of the river, about 6 km from town."),
        caution=T("バスは7月〜10月だけ。滝と大函の両方には降りられません", "Bus July–October only. You cannot stop at both the falls and Obako"),
        lat=43.69987, lng=143.01596,
        text=T("温泉街から国道39号を北見方面へ約6km、新大函トンネルを過ぎてすぐ左に入口があります。柱状節理（ちゅうじょうせつり）という、柱のように割れた岩の壁が川の両側に並び、層雲峡の谷のでき方がいちばんよく分かる場所です。無料、通年。隣の小函（こばこ）の遊歩道は、落石の危険があるため通行禁止です。\n\n"
               "7月1日〜10月31日のバス（1日1往復）：層雲峡12:50発 → 大函入口13:15着、帰りは大函入口13:43発 → 層雲峡14:00着。運賃は公式の時刻表に書かれていないので、乗るときに確かめてください。銀河・流星の滝と同じバスなので、両方には降りられません。見る時間は大函が28分、滝が40分です。\n\n"
               "ほかの季節はタクシーで（層雲峡ハイヤー 01658-5-3221。料金は要確認）。",
               "About 6 km from the town towards Kitami on Route 39; the entrance is on the left just after the Shin-Obako tunnel. Walls of columnar-jointed rock line both sides of the river, and this is the place that shows most clearly how the gorge was formed. Free, all year. The path through neighbouring Kobako is closed because of falling rocks.\n\n"
               "Bus from 1 July to 31 October (once a day): Sounkyo 12:50 → Obako Iriguchi 13:15, and back Obako Iriguchi 13:43 → Sounkyo 14:00. The fare is not on the official timetable: ask when you board. It is the same bus as for the Ginga and Ryusei falls, so you cannot get off at both. You get 28 minutes at Obako, or 40 at the falls.\n\n"
               "In other seasons go by taxi (Sounkyo Hire, 01658-5-3221; fare: please check)."),
        gmaps=[gm("大函", "Obako", 43.69987, 143.01596, "大函 層雲峡")],
        links=[link("info", "大函（層雲峡観光協会）", "Obako (Japanese)", U["sk_obako"]), DOHOKU],
        rows=[row("bus", "7月1日〜10月31日だけ：層雲峡12:50 → 大函入口13:15、大函入口13:43 → 層雲峡14:00（運賃は要確認）", "1 Jul–31 Oct only: Sounkyo 12:50 → Obako Iriguchi 13:15; Obako Iriguchi 13:43 → Sounkyo 14:00 (fare: please check)"),
              row("fee", "無料", "Free"),
              row("closed", "小函の遊歩道は通行禁止（落石）", "Kobako path closed (rockfall)")],
        notices=[],
        tip=T("層雲峡観光協会のページと道北バスの公式の時刻表（2026年7月1日改正）で2026年11月28日に確認しました。",
              "Checked on the Sounkyo Tourist Association’s page and Dohoku Bus’s timetable (revised 1 July 2026) on 28 November 2026."),
        time=(VIS, "13:15〜13:43（7月〜10月のバスで。滝の代わりに）", "13:15–13:43 (by the July–October bus, instead of the falls)")),

    dict(
        id="kuroyu", name=T("黒岳の湯", "Kurodake-no-yu"), kind=T("日帰り温泉", "Day bath"),
        blurb=T("温泉街の真ん中にある、日帰り入浴だけの施設。3階に露天風呂。800円。",
                "A day-use bath house in the middle of town, with an open-air bath on the top floor. ¥800."),
        caution=T("タトゥーの決まりは要確認（電話 01658-5-3333）", "Tattoo rule not stated: phone 01658-5-3333"),
        lat=43.72605, lng=142.94675,
        text=T("バスターミナルから歩いて2分の、日帰り入浴だけの施設です。2つの大浴場と3階の露天風呂、サウナ、水風呂。大人800円、子ども400円。\n\n"
               "5月〜10月は10:00〜22:00（受付は21:30まで）、11月〜4月は11:00〜21:30（受付は21:00まで）、12月31日〜1月3日は11:00〜18:00（受付は17:30まで）。決まった休みはありませんが、設備の点検で休む日があります。\n\n"
               "タトゥー：層雲峡観光協会の案内には、決まりが書かれていません。行く前に電話（01658-5-3333）で確かめてください。\n\n"
               "タオルは持っていくと確実です（貸し出しと販売は要確認）。17:00のバスで旭川へ帰るなら、16:40には出ましょう。",
               "A day-use bath house two minutes’ walk from the bus terminal: two bath halls, an open-air bath on the third floor, a sauna and a cold bath. Adults ¥800, children ¥400.\n\n"
               "May–October 10:00–22:00 (entry until 21:30); November–April 11:00–21:30 (entry until 21:00); 31 December–3 January 11:00–18:00 (entry until 17:30). No regular closing day, but it shuts for maintenance on some days.\n\n"
               "Tattoos: the Sounkyo Tourist Association’s page gives no rule. Phone before you go (01658-5-3333, Japanese).\n\n"
               "Bring a towel to be safe (rental or sale: please check). For the 17:00 bus to Asahikawa, leave by 16:40."),
        gmaps=[gm("黒岳の湯", "Kurodake-no-yu", 43.72605, 142.94675, "層雲峡 黒岳の湯")],
        links=[link("info", "黒岳の湯（層雲峡観光協会）", "Kurodake-no-yu (Japanese)", U["sk_yu"]), SK],
        rows=[row("tattoo", "記載なし＝要確認（電話 01658-5-3333）", "Not stated: please check (01658-5-3333)"),
              row("hours", "5〜10月 10:00〜22:00（受付21:30まで）／11〜4月 11:00〜21:30（受付21:00まで）／12月31日〜1月3日 11:00〜18:00", "May–Oct 10:00–22:00 (entry to 21:30) / Nov–Apr 11:00–21:30 (entry to 21:00) / 31 Dec–3 Jan 11:00–18:00"),
              row("fee", "大人800円、子ども400円", "Adults ¥800, children ¥400"),
              row("closed", "無休（設備の点検で休む日あり）", "No regular closing day (some maintenance closures)")],
        notices=[N_TATTOO_S],
        cash=True,
        tip=T("層雲峡観光協会の黒岳の湯のページで2026年11月28日に確認しました。施設の公式サイトは見つからず、タトゥー・タオル・支払い方法は確認できていません。",
              "Checked on the Sounkyo Tourist Association’s page for Kurodake-no-yu on 28 November 2026. No website of its own was found; the tattoo rule, towels and payment methods could not be confirmed."),
        time=(VIS, "14:45〜16:40", "14:45–16:40")),

    dict(
        id="hyobaku", name=T("層雲峡温泉氷瀑まつり", "Sounkyo Ice Fall Festival"), kind=T("冬のまつり", "Winter festival"),
        blurb=T("川原に氷の建物とトンネルが並び、夜は色の光で照らされます。2027年は1月23日〜3月7日。",
                "Buildings and tunnels of ice by the river, lit in colour at night. 23 January–7 March in 2027."),
        caution=T("2027年1月23日〜3月7日だけ。平日は17:00から", "23 Jan–7 Mar 2027 only. From 17:00 on weekdays"),
        lat=43.72800, lng=142.95000,
        text=T("氷瀑（ひょうばく）まつりは、石狩川のそばの会場に、水を凍らせて作った氷の建物やトンネルが並ぶ冬のまつりです。夜は色のついた光で照らされます。第52回は2027年1月23日（土）〜3月7日（日）。平日は17:00〜21:30、土日祝は11:00〜21:30（最終入場21:15）。協力金1,000円。バスターミナルから歩いて5分です。\n\n"
               "土日祝：明るいうちから入れます。お風呂のあと16:00ごろに入って、17:00のバスで旭川へ帰れます。\n\n"
               "平日と、暗くなってからゆっくり見たい日：17:00のバスには乗らず、18:55発のバスで上川へ（19:25着、890円）。上川20:24発の普通列車で旭川21:22着（1,380円）。晩ごはんは、まつりの前後に温泉街で（大雪山食堂は17:30〜20:30、ビアグリル・キャニオンは17:30〜20:00で水曜休み）。18:55のバスに乗り遅れると、その日のうちに旭川へ戻る方法はタクシーだけになります。\n\n"
               "会場はとても寒いので、暖かい服と、滑り止めのついた靴で（公式の案内）。会場の休憩所で、手袋と靴の滑り止めを売っています。",
               "The Hyobaku (Ice Fall) Festival fills a site beside the Ishikari river with buildings and tunnels made by freezing water, lit in colour after dark. The 52nd festival runs from Saturday 23 January to Sunday 7 March 2027: 17:00–21:30 on weekdays, 11:00–21:30 at weekends and on holidays (last entry 21:15). Entry is a ¥1,000 contribution. Five minutes’ walk from the bus terminal.\n\n"
               "Weekends and holidays: it is open in daylight. Go in at about 16:00 after your bath and still catch the 17:00 bus to Asahikawa.\n\n"
               "Weekdays, or to see it properly after dark: skip the 17:00 bus and take the 18:55 to Kamikawa (19:25, ¥890), then the 20:24 local train to Asahikawa (21:22, ¥1,380). Eat in the town before or after the festival (Daisetsuzan Shokudo 17:30–20:30; Beer Grill Canyon 17:30–20:00, closed Wednesdays). If you miss the 18:55 bus, a taxi is the only way back to Asahikawa that night.\n\n"
               "It is very cold at the site: the organisers ask for warm clothes and shoes with a good grip. Gloves and slip-on ice grips are sold at the rest hut on site."),
        gmaps=[gm("氷瀑まつりの会場", "Ice Fall Festival site", 43.72800, 142.95000, "層雲峡温泉 氷瀑まつり 会場")],
        links=[link("official", "層雲峡温泉氷瀑まつり", "Sounkyo Ice Fall Festival", U["hyobaku"]), DOHOKU],
        rows=[row("hours", "2027年1月23日〜3月7日。平日17:00〜21:30、土日祝11:00〜21:30（最終入場21:15）", "23 Jan–7 Mar 2027. Weekdays 17:00–21:30; weekends/holidays 11:00–21:30 (last entry 21:15)", until="2027-03-07"),
              row("fee", "協力金1,000円", "¥1,000 contribution", until="2027-03-07"),
              row("bus", "遅い帰り：層雲峡18:55 → 上川19:25（890円）、JR 上川20:24 → 旭川21:22（1,380円）", "Late return: Sounkyo 18:55 → Kamikawa 19:25 (¥890), JR Kamikawa 20:24 → Asahikawa 21:22 (¥1,380)", until="2027-03-07"),
              row("closed", "まつりの期間の外は、会場に何もありません", "Outside the festival dates there is nothing at the site")],
        notices=N_HYOBAKU,
        cash=True,
        tip=T("氷瀑まつりの公式サイト（層雲峡観光協会）で2026年11月28日に確認しました。協力金の支払い方法は書かれていません。",
              "Checked on the festival’s official site (Sounkyo Tourist Association) on 28 November 2026. How to pay the contribution is not stated."),
        time=(VIS, "土日祝 16:00〜16:50／平日 17:00〜18:45", "Weekends/holidays 16:00–16:50 / weekdays 17:00–18:45")),
]

# ---------------------------------------------------------------------------
# 書き出し
# ---------------------------------------------------------------------------
COURSES = [
    dict(file=f"{ID}.json", course="asahidake", spots=ASAHIDAKE,
         note="旭岳。旭川駅9:15のいで湯号→旭岳ビジターセンター→ロープウェイ→姿見の池→お昼→旭岳温泉の日帰り入浴→16:55の最終バスで旭川18:33（東川に寄るなら14:55発で、温泉なし）。",
         sections=[(1, 1, T("旭川から", "From Asahikawa"), T("バスで1時間48分", "1 hr 48 min by bus")),
                   (2, 4, T("旭岳", "Asahidake"), T("ビジターセンター、ロープウェイ、姿見の池", "Visitor Center, ropeway and Sugatami Pond")),
                   (5, 6, T("ふもとと帰り道", "Below the mountain"), T("温泉か、東川の町。旭川に18:33", "A bath, or the town of Higashikawa. Asahikawa by 18:33"))],
         focus=(2, 5), auto={"astart": "always"}, default_off=["higashikawa"],
         hints=[("higashikawa", ["aonsen"], [],
                 "9:15発のバスで来た日は、温泉と東川の両方には時間が足りません。両方なら旭川7:15発で来て、お昼のあと12時台から入れるベアモンテか湧駒荘へ、14:55発のバスで東川へ。",
                 "Coming on the 9:15 bus, there is not enough time for both a bath and Higashikawa. To do both, take the 7:15 bus, bathe after lunch at Bear Monte or Yukomanso (open around noon), then take the 14:55 bus to Higashikawa."),
                ("higashikawa", [], ["aonsen"],
                 "ロープウェイは13:20発までに下りて、お昼を食べ、旭岳14:55発のバスで東川へ（道草館15:34着）。",
                 "Come down on the 13:20 car at the latest, have lunch, and take the 14:55 bus from Asahidake to Higashikawa (Michikusa-kan 15:34).")]),
    dict(file=f"{ID}-sounkyo.json", course="sounkyo", spots=SOUNKYO,
         note="層雲峡。旭川駅前9:55の道北バス→温泉街でお昼→黒岳ロープウェイの5合目→（7〜10月はバスで銀河・流星の滝）→ビジターセンター→黒岳の湯→17:00の最終バスで旭川18:55（氷瀑まつりの夜は18:55発のバスとJR）。",
         sections=[(1, 1, T("旭川から", "From Asahikawa"), T("バスで約2時間", "About 2 hours by bus")),
                   (2, 3, T("温泉街と黒岳", "The town and Kurodake"), T("お昼、ロープウェイで5合目", "Lunch, then the ropeway to the fifth station")),
                   (4, 5, T("峡谷", "The gorge"), T("滝と大函。バスは7月〜10月だけ", "Waterfalls and Obako; bus July–October only")),
                   (6, 7, T("お風呂と冬の夜", "Bath and winter evening"), T("黒岳の湯。1月下旬〜3月上旬は氷瀑まつり", "Kurodake-no-yu; Ice Fall Festival late Jan–early Mar"))],
         focus=(2, 4), auto={"sstart": "always"}, default_off=["obako", "hyobaku"],
         hints=[("obako", ["taki"], [],
                 "滝と大函は同じ1本のバスなので、両方には降りられません。どちらか1つに（タクシーなら両方回れます）。",
                 "The falls and Obako are on the same single bus, so you cannot get off at both. Pick one (a taxi can do both)."),
                ("taki", ["kurodake"], [],
                 "7月〜10月：お昼を12:40までに食べて12:50発のバスで滝へ、14:00に戻って14:20発のロープウェイ。11月〜6月はバスがないので、滝はタクシーで行く人だけ。",
                 "July–October: finish lunch by 12:40, take the 12:50 bus to the falls, return at 14:00 and ride the 14:20 ropeway. November–June there is no bus: the falls are for taxi users only."),
                ("hyobaku", [], [],
                 "まつりは2027年1月23日〜3月7日。平日は17:00からなので、帰りは18:55発のバスで上川へ出て、JRで旭川へ（21:22着）。",
                 "The festival runs 23 January–7 March 2027. On weekdays it opens at 17:00, so return on the 18:55 bus to Kamikawa and the train to Asahikawa (21:22).")]),
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
        "_note": "大雪山の日帰り：旭岳と層雲峡（daisetsuzan/ のページ専用。形は eizan-line.json と同じ）。" + C["note"]
                 + "写真は今は Wikimedia Commons だけ（一覧は scripts/daisetsuzan_web_photos.json）。"
                 + "info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。このファイルは scripts/build_daisetsuzan_data.py で作る（直接直さない）。",
        "sections": [{"first": a, "last": b, "area": area, "title": title} for a, b, area, title in C["sections"]],
        "focus": {"first": C["focus"][0], "last": C["focus"][1]},
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。旭川からのバスは自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": default, "auto": auto, "hints": hints},
        "photoBase": f"../images/{ID}/", "sources": SOURCES,
        "spots": out_spots,
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"], len(s["photos"])) for s in out_spots], "default", default)


for C in COURSES:
    build(C)
