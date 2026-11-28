#!/usr/bin/env python3
"""札幌市内で1日（札幌駅〜大通〜すすきののホテルから）のデータを書き出す。コースは3つ。

使い方: python3 scripts/build_sapporo_data.py   （そのあと python3 scripts/sync_sapporo.py）
- data/routes/sapporo.json … 定番（9:15に出る。最初に開く）10か所
    赤れんが庁舎→時計台→大通公園・テレビ塔→（資料館）→二条市場でお昼→（狸小路）→サッポロビール博物館→藻岩山の夜景→すすきの
- data/routes/sapporo-early.json … 朝いちばん（7:00に出る）11か所
    場外市場で朝ごはん→北海道大学→赤れんが庁舎→時計台→大通公園・テレビ塔→（二条市場）→狸小路でお昼→ビール博物館→藻岩山→すすきの
- data/routes/sapporo-maruyama.json … もう1日あるなら（9:15に出る）7か所
    北海道神宮・円山公園→円山動物園→白い恋人パーク（または モエレ沼公園）→大通公園の夜→すすきの
  どのコースも最初から「選んで回る」で、時間割どおりの場所が選ばれている（defaultPicks）。
  コースを分けたのは、(1) 朝の市場と北大は早く出ないと1日に入らない、(2) 円山と宮の沢は反対の方向にあって
  街なかの定番と同じ日には回れない（札幌に2泊以上する人の2日目）ため。
- 起点は札幌駅〜大通〜すすきののホテル。夜は藻岩山の夜景とすすきので21時すぎまで
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 冬（12〜3月）と雪のない季節の両方で使える。季節で変わるところは notices（from / to）と rows（until / from）で出す
  （藻岩山の冬期営業、円山動物園の冬期開園、ホワイトイルミネーション、ミュンヘン・クリスマス市、雪まつり、白い恋人パークの点灯）
- 写真はすべて Wikimedia Commons（オーナーはまだ北海道の写真を持っていない）。一覧とクレジットは scripts/sapporo_web_photos.json。
  オーナーの写真はあとで images/sapporo/<スポットのid>-<番号>.jpg として足す（ネットの写真は -w<番号>）
- 行っていない場所なので文章は中立に。店名は、公式サイトで時間を確かめたところだけ
- 入れなかったもの：羊ヶ丘展望台・大倉山ジャンプ競技場・北海道博物館と開拓の村（どれも1日に入らない）、
  定山渓・登別の温泉（sapporo-onsen のマップ）、小樽・余市・銭函（otaru・yoichi・zenibako のマップ）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/sapporo"
CHECKED = "2026-11-29"
DEP = ("おすすめ出発時間", "Recommended departure time")
VIS = ("おすすめ訪問時間", "Recommended visit time")


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, qq):
    return {"label": T(ja, en), "lat": lat, "lng": lng,
            "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(qq)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, start=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": start}


def notice(hja, hen, ja, en, url=None, start=None, to=None):
    d = {"head": T(hja, hen), "text": T(ja, en), "from": start, "to": to}
    if url:
        d["url"] = url
    return d


def q(f, t, day, hm):
    """確かめた乗換案内（Yahoo!路線情報）の検索結果のURL。day は '2026/12/03' の形"""
    h, m = hm.split(":")
    y, mon, d = day.split("/")
    p = dict(to=t, y=y, m=mon, d=d, hh=h, m1=m[0], m2=m[1], type=1, ticket="ic",
             expkind=1, shin=1, ex=1, lb=1, al=0, hb=1, sr=0, s=0, userpass=0, ws=3)
    p["from"] = f
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(p)


def cc(x):
    """Wikimedia Commons の写真。"""
    return {"file": x["file"], "credit": {"author": x["author"], "license": x["license"],
            "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(x["title"].replace(" ", "_"))}}


WEB = json.load(open(f"{R}/scripts/sapporo_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]

U = dict(
    akarenga="https://www.hokkaido-redbrick.jp/",
    akarenga_guide="https://www.hokkaido-redbrick.jp/information/",
    akarenga_illum="https://www.hokkaido-redbrick.jp/2026/11/18/788/",
    tokeidai="https://sapporoshi-tokeidai.jp/",
    tokeidai_guide="https://sapporoshi-tokeidai.jp/inspect/guide.php",
    tokeidai_en="https://sapporoshi-tokeidai.jp/english/",
    tv="https://www.tv-tower.co.jp/",
    tv_price="https://www.tv-tower.co.jp/pricetime.html",
    illum="https://www.sapporo.travel/event/winter/white_illumination/",
    illum_pdf="https://www.sapporo.travel/cms/wp-content/uploads/2026/10/2026-%E3%81%95%E3%81%A3%E3%81%BD%E3%82%8D%E3%83%9B%E3%83%AF%E3%82%A4%E3%83%88%E3%82%A4%E3%83%AB%E3%83%9F%E3%83%8D%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%85%AC%E5%BC%8F%E3%82%AC%E3%82%A4%E3%83%89%E3%83%96%E3%83%83%E3%82%AF.pdf",
    snowfes="https://www.snowfes.com/",
    nijo="https://nijomarket.com/",
    nijo_about="https://nijomarket.com/about",
    nijo_en="https://nijomarket.com/en/top_en/",
    tanuki="https://www.tanukikoji.or.jp/",
    beer="https://www.sapporobeer.jp/brewery/s_museum/",
    beer_guide="https://www.sapporobeer.jp/brewery/s_museum/kengaku/",
    beer_access="https://www.sapporobeer.jp/brewery/s_museum/access/",
    beer_en="https://www.sapporobeer.jp/english/",
    beerpark="https://www.sapporo-bier-garten.jp/",
    moiwa="https://mt-moiwa.jp/",
    moiwa_guide="https://mt-moiwa.jp/guide/",
    moiwa_bus="https://mt-moiwa.jp/access/bus/",
    moiwa_tram="https://mt-moiwa.jp/access/shuttlebus-tram/",
    moiwa_winter="https://mt-moiwa.jp/2026/11/21/%e5%86%ac%e6%9c%9f%e9%96%9312%ef%bd%9e3%e6%9c%88%e3%81%ae%e5%96%b6%e6%a5%ad%e6%99%82%e9%96%93%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6/",
    moiwa_cam="https://mt-moiwa.jp/live-camera/",
    hokudai="https://www.hokudai.ac.jp/introduction/campus/campusmap/",
    hokudai_m="https://www.museum.hokudai.ac.jp/",
    zoo="https://www.city.sapporo.jp/zoo/",
    zoo_time="https://www.city.sapporo.jp/zoo/s077/166519.html",
    zoo_fee="https://www.city.sapporo.jp/zoo/s077/76124.html",
    jingu="http://www.hokkaidojingu.or.jp/",   # https は証明書の期限が切れていて開けない（2026-11-29 確認）
    sun12="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html",
    sun1="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0001.html",
    sun2="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0002.html",
    shiroi="https://www.shiroikoibitopark.jp/",
    shiroi_illum="https://www.shiroikoibitopark.jp/illumination/",
    shiroi_access="https://www.shiroikoibitopark.jp/park-guide/access.html",
    shiroi_en="https://www.shiroikoibitopark.jp/en/",
    shiryokan="https://www.s-shiryokan.jp/aboutus/",
    moere="https://moerenumapark.jp/",
    moere_access="https://moerenumapark.jp/access/",
    jogai="https://www.sapporo.travel/spot/facility/sapporo_central_wholesale_market/",
    subway="https://www.city.sapporo.jp/st/josyaken/ryokin/ryoukin.html",
    donichika="https://www.city.sapporo.jp/st/josyaken/doni-chika/donichika.html",
    fare_en="https://www.city.sapporo.jp/st/s107/77494.html",
    ticket="https://www.city.sapporo.jp/st/josyaken/ticket_h.html",
    jrbus="https://www.jrhokkaidobus.com/",
    chuobus="https://www.chuo-bus.co.jp/",
    unkou="https://www3.jrhokkaido.co.jp/webunkou/",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("北海道庁旧本庁舎（赤れんが庁舎） 公式サイト", U["akarenga"],
     "開館時間 8:45〜21:00（最終入館20:30）。11月15日・12月29日〜1月3日は休館。入館料 一般300円、大学生・高校生200円、中学生以下無料、1階の店舗のみの利用は無料。団体（20名以上）一般270円。オプション：八角塔観覧1,200円（小学生以上）。2025年7月25日にリニューアル再開館。赤れんがイルミネーション 2026年11月20日〜2027年2月28日。八角塔観覧は12月の催行時間変更のお知らせあり"),
    ("札幌市時計台 観覧案内", U["tokeidai_guide"],
     "開館時間 8時45分〜17時10分（入館は17時まで）。休館日 1月1日〜1月3日。観覧料 大人350円、大学生150円、小中学生・高校生無料、団体（20人以上）300円。キャッシュレス決済可。冷房設備なし、暖房はあるが真冬は快適な室温にならない。コインロッカーなし（大きな荷物は1階事務室前に置ける）。館内は原則飲食禁止"),
    ("札幌市時計台 トップページのお知らせ", U["tokeidai"],
     "1日1回10:30〜 時計の巻き上げ実演と説明。夜間開館日は8:45〜20:00。毎月16日は札幌市民無料の日。年末臨時開館 12/29・30は8:45〜17:10（入館17時まで）、12/31は8:45〜20:10（入館19時半まで）と23:00〜翌1:00（無料開館）"),
    ("さっぽろテレビ塔 展望台入場料金・営業時間", U["tv_price"],
     "営業時間 9:00〜22:00（展望最終入場21:50）。休業日（設備点検日）2027年1月1日 終日休業。展望台入場料金 一般 大人（高校生以上）1,200円、小学生・中学生600円、幼児（小学生未満）無料。団体（15名以上）900円／500円。札幌市民料金 800円／400円"),
    ("さっぽろテレビ塔 トップページ", U["tv"],
     "本日のライトアップ 16:00〜24:00。2026年12月23日〜25日は営業時間延長のお知らせ。時計台との共通入場券の案内あり（金額はこのページには出ていない）"),
    ("2026 さっぽろホワイトイルミネーション 公式ガイドブック（札幌市の観光サイト）", U["illum_pdf"],
     "開催期間 2026年11月20日〜2027年3月14日。大通会場は12月25日（金）まで、点灯16:30〜22:00（12月23日〜25日は24時まで）。駅前通会場は2月11日まで、赤れんがエリア会場・札幌北3条広場（アカプラ）会場は3月14日まで。入場無料。ミュンヘン・クリスマス市 in Sapporo は大通公園（大通西2丁目）、2026年11月20日〜12月25日、11:00〜21:00"),
    ("第78回さっぽろ雪まつり 公式サイト", U["snowfes"],
     "2027年の開催期間は大通会場・つどーむ会場・すすきの会場いずれも2027年2月4日（木）〜2月11日（木・祝）。詳しい情報は順次更新予定"),
    ("札幌二条市場 店舗情報（公式）", U["nijo_about"],
     "営業時間（店舗により異なります）朝7時頃〜夜17時頃、年中無休。所在地 中央区南3条東1〜2丁目。狸小路商店街（1丁目）から徒歩約1分。「125年以上の歴史を持つ、札幌市民の台所」「朝は8時から夕方6時ころまで」という紹介文もある"),
    ("札幌狸小路商店街 商店街の歴史（公式）", U["tanuki"] + "about/",
     "北海道で最古の商店街の一つ。2026年で153年（明治6年〜）。7ブロック総延長約900m・店舗数約200軒の全蓋アーケード。1丁目から6丁目の現在のアーケードは二代目（1982年完成）で、交差する路上も覆うロングアーケード。2014年に商店街区内は許可車両以外24時間車両通行禁止に"),
    ("サッポロビール博物館 利用案内（自由見学・ガイドツアー）", U["beer_guide"],
     "自由見学：全営業日 11:00〜18:00（最終入館17:30）。所要15〜30分（音声ガイド利用で15〜40分）。見学後のTasting Hall（有料試飲）の利用は最大30分。料金 大人1,000円、中学生〜20歳未満500円、小学生以下無料（道民割 700円／200円）。予約なしで入れる。音声ガイドは日本語・英語・韓国語・中国語（繁体字／簡体字）。順路は3階→2階→1階の一方通行。試飲付きガイドツアー：所要約55分、月曜休止（月曜が祝日の場合は実施し翌火曜が休止）、初回11:30スタート、WEB予約は当日朝9:30まで、ツアーガイドは日本語のみ。料金 大人2,000円（入館料・試飲2杯付き）、中学生〜20歳未満1,000円、小学生無料、未就学児は参加不可"),
    ("サッポロビール博物館 アクセス", U["beer_access"],
     "JR函館本線「苗穂駅」北口から徒歩約8分。札幌市営地下鉄東豊線「東区役所前駅」4番出口から徒歩約10分。北海道中央バス［188］サッポロビール園・アリオ線＜直行便＞札幌駅北口2番のりば→「サッポロビール園」下車すぐ。北海道中央バス［環88］サッポロビール園・ファクトリー線（札幌駅南口〜大通公園〜サッポロビール園）。併設のサッポロビール園でジンギスカン"),
    ("札幌もいわ山ロープウェイ 営業時間・料金", U["moiwa_guide"],
     "夏期（4月〜11月）ロープウェイ 10:30〜22:00（上り最終21:30）、ミニケーブルカー 10:30〜21:50（上り最終21:40）。冬期（12月〜3月）ロープウェイ 11:00〜22:00（上り最終21:30）、ミニケーブルカー 11:10〜21:50（上り最終21:40）。大晦日（12月31日）と元日（1月1日）は休業。休業日 2027年3月29日（月）〜4月28日（水）年次整備点検。運行間隔15分。セット料金（ロープウェイ＋ミニケーブルカー）往復 大人2,100円・小人1,050円、片道 大人1,050円。ロープウェイのみ往復 大人1,400円。上り最終便は21:30、21:25頃までにチケット購入を。レストラン ザ ジュエルズ 冬期ランチ12:00〜14:30（LO13:30）・ディナー17:00〜21:00（LO19:30）、平日のランチタイムは休み。藻岩山観光自動車道は2026年11月21日〜翌4月下旬頃まで冬期通行止め"),
    ("札幌もいわ山ロープウェイ 冬期間（12〜3月）の営業時間について（2026年11月21日）", U["moiwa_winter"],
     "2026年12月から2027年3月まで、ロープウェイの営業時間を11:00〜22:00（上り最終21:30）に変更。2027年3月29日（月）〜4月28日（水）は整備点検のため全館休業。藻岩山観光自動車道は2026年11月20日で今シーズンの営業を終了"),
    ("札幌もいわ山ロープウェイ 地下鉄／バスで", U["moiwa_bus"],
     "地下鉄南北線さっぽろ駅→（2分）大通駅→地下鉄東西線（6分）円山公園駅2番出口→JR北海道バス ロープウェイ線［循環円11］乗車15分→バス停「もいわ山ロープウェイ」（ロープウェイ乗り場直結）。運賃 大人240円・小人120円。［循環円10］［循環円12］は「もいわ山ロープウェイ」に止まらない。直通［啓明線50］JR札幌駅 ジェイ・アール北海道仮設バス停13番のりば→乗車37分（1日3本のみ）、240円"),
    ("札幌もいわ山ロープウェイ 市電／無料シャトルバスで", U["moiwa_tram"],
     "市電「ロープウェイ入口」下車 徒歩1分の無料シャトルバス乗り場から〈ロープウェイ山麓駅〉まで15分間隔で無料シャトルバス。運行時間は平日17:17〜、土日祝10:17〜（冬期10:47〜）。シャトルバス乗り場からは徒歩約10分（約0.5km）でも山麓駅に着く"),
    ("札幌もいわ山ロープウェイ トップページ（日没と夜景の時刻）", U["moiwa"],
     "2026年11月29日の営業時間 10:30〜21:30（上り終了時間）。この日の日没16:02、夜景16:22。山頂展望台ライブカメラあり"),
    ("北海道大学総合博物館 公式サイト", U["hokudai_m"],
     "開館時間 10:00〜17:00。休館日 月曜（祝日は開館し、翌平日は休館）。入館料 無料。約300万点の標本・資料を保管し、一部を公開"),
    ("札幌市円山動物園 開園時間・休園日", U["zoo_time"],
     "夏期（3月1日〜10月31日）9時30分〜16時30分（最終入園16時）。冬期（11月1日〜2月末日）9時30分〜16時（最終入園15時30分）。休園日 毎月第2・第4水曜日（8月のみ第1・第4水曜日。祝日の場合は翌日）、4月は第2水曜日を含むその週の月曜〜金曜、11月は第2水曜日を含むその週の月曜〜金曜、12月29日〜31日"),
    ("札幌市円山動物園 入園料について", U["zoo_fee"],
     "大人800円、高校生400円（半額減免。生徒手帳等の提示が必要）、中学生以下無料、団体（30名以上）720円、年間パスポート（高校生以上）2,000円。2026年3月2日から入園券の電子チケットの取扱いを開始"),
    ("白い恋人パーク イルミネーション期間の営業時間のお知らせ（2026年9月）と公式サイト", U["shiroi_illum"],
     "イルミネーション期間 2026年12月1日（火）〜2027年3月31日（水）。白い恋人パーク営業時間 10:00〜19:00、イルミネーション点灯 16:00〜19:00（無料）。チケットセンター10:00〜16:30受付、チョコレートラウンジ・工場など10:00〜17:30、チュダーハウス10:00〜18:30。有料エリア 大人（16歳以上）1,200円、団体（20名以上）900円、3歳以下無料。定休日は年中無休"),
    ("北海道神宮 公式サイトのお知らせ一覧", "http://www.hokkaidojingu.or.jp/",
     "お知らせに「閉門時間変更のお知らせ（◯月◯日〜）」「各月一日の開門時間変更のお知らせ」「年末年始開閉門時間のお知らせ」「正月期間閉門時間の変更について」が繰り返し出ていて、決まった開閉門の時刻表は掲載されていない。参拝料の記載もない。https は証明書の期限が切れていて開けず、http で確認した"),
    ("札幌市資料館（旧札幌控訴院庁舎） 入館案内・アクセス", U["shiryokan"],
     "開館時間 9:00〜19:00。休館日 月曜日（祝日にあたる場合は翌平日）、年末年始（12月29日〜1月3日）。入館料 無料。おおば比呂司記念室は11月1日〜3月31日が9:00〜18:00（最終入室17:40）"),
    ("モエレ沼公園 各施設の営業時間", U["moere"],
     "モエレ沼公園 7:00〜22:00 無休（園内各施設は定休日あり）。東口ゲート 7:00〜22:00（入園は21:00まで）、西口ゲート・南口ゲート 7:00〜19:00。ガラスのピラミッド 9:00〜17:00、休館日 毎週月曜日。海の噴水は2026年度の運転は終了。ウィンタースポーツ用品レンタル 2027年1月5日〜3月7日 10:00〜16:00 毎週月曜休。2026年11月4日から冬季営業期間"),
    ("モエレ沼公園 アクセス", U["moere_access"],
     "札幌市街地からは地下鉄とバスを乗り継ぐ。例）さっぽろ駅→環状通東駅→バス停「モエレ沼公園東口」。地下鉄東豊線「環状通東駅」から中央バス【東69】「あいの里教育大駅」行き、【東69｜東79】「中沼小学校通」行きで「モエレ沼公園東口」下車。【東61｜ビ61】（平日のみ）で「モエレ沼公園西口」下車。期間限定バス【ビ68】「モエレ沼公園」行き（サッポロビール博物館発）は2026年4月25日〜11月3日の土日祝（7月27日〜8月20日は毎日）"),
    ("札幌市中央卸売市場 場外市場（札幌市の観光サイト。市場の公式サイトは見つからなかった）", U["jogai"],
     "営業時間 6:00〜15:00、大型店舗は6:00〜17:00。無休。鮮魚店・青果店・乾物店など約60店舗。問い合わせは場外市場商店街振興組合 011-621-7044"),
    ("札幌市交通局 乗車料金", U["subway"],
     "地下鉄単独料金 大人 210円・250円・290円・330円・360円・380円（1区〜6区）。市電（路面電車）単独料金 大人230円・小児120円。地下鉄と市電を乗り継ぐ場合 大人360円・400円・440円・480円"),
    ("札幌市交通局 ドニチカキップ", U["donichika"],
     "土曜・日曜・祝日と年末年始（12月29日〜1月3日）に地下鉄全線が乗り放題。大人520円・こども260円。支払いは現金のみ。販売は地下鉄駅券売機・各地下鉄駅事務室・各定期券発売所。路面電車には乗れず、市電・バスへの乗継割引は適用されない"),
    ("札幌市交通局 乗車券発売所及び取扱券種", U["ticket"],
     "地下鉄専用1日乗車券・ドニチカキップは地下鉄駅券売機、地下鉄駅事務室、各定期券発売所で購入できる（券売機での地下鉄専用1日乗車券の発売は平日のみ）。大通定期券発売所では市電（路面電車）専用1日乗車券も発売。地下鉄専用1日乗車券は大人830円・こども420円"),
    ("大通 → 札幌もいわ山ロープウェイ 平日", q("大通", "札幌もいわ山ロープウェイ", "2026/12/03", "15:00"),
     "ルート1 15:00→15:44（44分、230円）市電 西4丁目→中央図書館前→徒歩9分。ルート2 15:07→15:46（39分、230円）市電 西4丁目→ロープウェイ入口・電車事業所前→徒歩7分。乗換案内は無料シャトルバスを考えに入れていない"),
    ("円山公園駅前 → もいわ山ロープウェイ 平日の夕方", q("円山公園駅前", "もいわ山ロープウェイ", "2026/12/03", "15:00"),
     "15:10→15:26（16分、240円）、15:35→15:55、15:50→16:08、16:00→16:18。JR北海道バス 循環円11"),
    ("円山公園駅前 → もいわ山ロープウェイ 土曜の夕方", q("円山公園駅前", "もいわ山ロープウェイ", "2026/12/05", "15:00"),
     "15:00→15:16（16分、240円）、15:40→16:00"),
    ("もいわ山ロープウェイ → すすきの 平日の夜", q("もいわ山ロープウェイ", "すすきの", "2026/12/03", "18:30"),
     "18:30→19:03（33分、230円）、18:35→19:08"),
    ("大通 → サッポロビール園 平日", q("大通", "サッポロビール園", "2026/12/03", "13:40"),
     "13:46→14:08（22分、210円）"),
    ("東区役所前 → 円山公園 平日", q("東区役所前", "円山公園", "2026/12/03", "15:20"),
     "15:20→15:42（22分、250円）、15:27→15:49"),
    ("大通 → 二十四軒 平日の朝", q("大通", "二十四軒", "2026/12/03", "07:10"),
     "7:13→7:22（9分、250円）、7:17→7:26"),
    ("大通 → 円山公園 平日の朝", q("大通", "円山公園", "2026/12/03", "09:30"),
     "9:32→9:37（5分、210円）、9:39→9:44"),
    ("円山公園 → 宮の沢 平日", q("円山公園", "宮の沢", "2026/12/03", "14:00"),
     "14:04→14:15（11分、250円）、14:11→14:22"),
    ("宮の沢 → 大通 平日の夕方", q("宮の沢", "大通", "2026/12/03", "16:40"),
     "16:42→16:58（16分、290円）、16:49→17:04"),
    ("宮の沢 → 白い恋人パーク 徒歩", q("宮の沢", "白い恋人パーク", "2026/12/03", "14:20"),
     "宮の沢駅 出口1 から徒歩7分（0.5km）"),
    ("すすきの → 札幌 夜", q("すすきの", "札幌", "2026/12/03", "21:30"),
     "21:36→21:47（11分、210円）、21:44→21:55"),
    ("札幌の日の出・日の入り（国立天文台 暦計算室。札幌 北緯43.0667° 東経141.35°）2026年12月", U["sun12"],
     "日の入り 12月1日16:01、11日16:00、21日16:03、31日16:09ごろ。日の出 12月1日6:46、21日7:02"),
    ("同 2027年1月", U["sun1"], "日の入り 1月1日16:10、11日16:20、21日16:32"),
    ("同 2027年2月", U["sun2"], "日の入り 2月1日16:46、11日17:00、21日17:13、28日17:22。日の出 2月28日6:13"),
    ("赤れんがイルミネーション2026-2027（公式のお知らせ）", U["akarenga_illum"],
     "期間 2026年11月20日（金）〜2027年2月28日（日）。点灯時間 16:30〜22:00（期間中、日没時間等に合わせて点灯時刻を変更する場合あり）。イルミネーションの観覧は無料"),
    ("北海道庁旧本庁舎 施設案内（公式）", U["akarenga_guide"],
     "八角塔展望バルコニー 1,200円（小学生以上）。これまで非公開だった八角塔のバルコニーから街を一望できる。煉瓦造・地下1階、地上2階建て、八角塔屋付"),
]]

# ───────── お知らせ（notices） ─────────
N_WINTER = notice(
    "冬は、歩道が凍ります", "In winter the pavements turn to ice",
    "12月から3月の札幌は、雪が踏み固められて歩道がつるつるになります。靴の底に溝のある冬用の靴か、滑り止め（駅やコンビニで買えます）を。歩幅を小さく、靴の裏全体を地面につけて歩くと転びにくいです。横断歩道の前と、建物の出入口のあたりがいちばんすべります。\n\n"
    "さっぽろ地下街とチカホ（札幌駅前通地下歩行空間）が札幌駅から大通・すすきのまでつながっているので、寒い日はできるだけ地下を歩くと楽です。",
    "From December to March the snow on Sapporo’s pavements gets packed down into ice. Wear winter boots with a deep tread, or buy a pair of clip-on grips (sold at stations and convenience stores). Take short steps and put the whole sole down at once. The worst patches are at crossings and in front of building entrances.\n\n"
    "An underground walkway runs from Sapporo Station through Odori to Susukino, so on cold days stay below ground as much as you can.",
    None, start="2026-11-20", to="2027-03-31")
N_DARK = notice(
    "冬は16時前後に日が暮れます", "In winter the sun sets around 16:00",
    "札幌の日の入りは、12月が16:00〜16:03、1月11日で16:20、2月11日で17:00、2月28日で17:22（国立天文台）。12月がいちばん早く、そこから少しずつ遅くなります。外を歩く場所は、明るいうちに回る順番にしてあります。\n\n藻岩山の公式サイトのトップには、その日の日没と「夜景」の時刻が出ます（2026年11月29日は日没16:02、夜景16:22）。暗くなってからは、イルミネーションと藻岩山の夜景の時間です。",
    "Sunset in Sapporo falls between 16:00 and 16:03 through December, reaching 16:20 on 11 January, 17:00 on 11 February and 17:22 on 28 February (National Astronomical Observatory of Japan). December is the earliest, and it draws out from there. The outdoor parts of this route come while it is still light.\n\nThe front page of the Mt. Moiwa site gives the day’s sunset and “night view” times — on 29 November 2026, 16:02 and 16:22. After dark it is time for the illuminations and the night view.",
    U["sun12"], start="2026-11-20", to="2027-02-20")
N_IC = notice(
    "地下鉄・市電・バスは Suica などのICカードで乗れます", "Suica and other IC cards work on the subway, tram and buses",
    "札幌市営地下鉄と市電、市内の路線バスは、Kitaca・Suica・PASMO・ICOCA などの全国相互利用のICカードで乗れます。残高が足りないときは改札のそばの機械で足せます。\n\n"
    "1日に地下鉄を3回以上乗るなら1日乗車券が得です。土日祝と12月29日〜1月3日は「ドニチカキップ」大人520円（現金のみ）、平日は「地下鉄専用1日乗車券」大人830円。どちらも地下鉄だけで、市電とバスには使えません。",
    "The Sapporo subway and tram and the city’s buses all take Kitaca, Suica, PASMO, ICOCA and the other nationally interoperable IC cards. Top up at the machines beside the ticket gates.\n\n"
    "If you will use the subway three times or more in a day, a day pass is cheaper: the Donichika Kippu on weekends, holidays and 29 Dec – 3 Jan (¥520, cash only), or the Subway 1-Day Card on weekdays (¥830). Both cover the subway only, not the tram or the buses.",
    U["donichika"])
N_ILLUM = notice(
    "さっぽろホワイトイルミネーション（11月20日〜3月14日）", "Sapporo White Illumination (20 November – 14 March)",
    "大通会場は12月25日まで、点灯は16:30〜22:00（12月23日〜25日は24時まで）。そのあとも駅前通が2月11日まで、赤れんが庁舎のまわりと札幌北3条広場（アカプラ）は3月14日まで続きます。どこも無料です。\n\n"
    "大通西2丁目では、11月20日から12月25日まで「ミュンヘン・クリスマス市 in Sapporo」（11:00〜21:00）。ホットワインとソーセージの小屋が並びます。",
    "The Odori Park section runs until 25 December, lit from 16:30 to 22:00 (until midnight on 23–25 December). After that the Ekimae-dori avenue stays lit until 11 February, and the Red Brick Office grounds and Akapura square until 14 March. All free.\n\n"
    "At Odori Nishi 2-chome, the Munich Christmas Market in Sapporo runs from 20 November to 25 December, 11:00–21:00, with huts selling mulled wine and sausages.",
    U["illum"], to="2027-03-14")
N_SNOWFES = notice(
    "さっぽろ雪まつりは2027年2月4日〜11日", "Sapporo Snow Festival: 4–11 February 2027",
    "大通会場（雪像）・すすきの会場（氷像）・つどーむ会場は、どれも2027年2月4日（木）から2月11日（木・祝）まで。この週は市内のホテルが早くうまり、大通公園とすすきのはとても混みます。",
    "The Odori site (snow sculptures), the Susukino site (ice sculptures) and the Tsudome site all run from Thu 4 to Thu 11 February 2027. Hotels in the city fill up early that week, and Odori Park and Susukino get very crowded.",
    U["snowfes"], start="2026-12-15", to="2027-02-11")
N_AKARENGA_CLOSED = notice(
    "年末年始（12月29日〜1月3日）は休館", "Closed 29 December – 3 January",
    "赤れんが庁舎は12月29日から1月3日まで休みです。1階の店舗も入れません。公式サイトには、ほかに11月15日も休館日として出ています。",
    "The Red Brick Office is closed from 29 December to 3 January, shops included. The official site also lists 15 November as a closing day.",
    U["akarenga"], start="2026-12-15", to="2027-01-03")
N_AKARENGA_ILLUM = notice(
    "赤れんがイルミネーション（11月20日〜2月28日）", "Red Brick illumination (20 November – 28 February)",
    "点灯は16:30から22:00まで（観覧は無料）。庁舎と前庭がライトアップされます。建物は21時まで開いているので、夜に立ち寄るのも気持ちのよい場所です。期間中は「AKARENGA YUKIGUNI FANTASY」として庁舎の中でも催しがあります。",
    "The lights are on from 16:30 to 22:00 and free to see. The building and its front garden are both lit; the building itself stays open until 21:00, so it is a pleasant place to drop by in the evening, and there are events inside during the season.",
    U["akarenga_illum"], to="2027-02-28")
N_TOKEIDAI_NY = notice(
    "1月1日〜3日は休館（大晦日は夜も開きます）", "Closed 1–3 January (open late on New Year’s Eve)",
    "時計台の休館日は1月1日〜3日だけです。12月29日・30日は8:45〜17:10（入館17時まで）、12月31日は8:45〜20:10（入館19時半まで）に加えて、23:00から翌1:00まで無料で開きます。",
    "The Clock Tower closes only on 1–3 January. On 29 and 30 December it is open 8:45–17:10 (last entry 17:00); on 31 December 8:45–20:10 (last entry 19:30), and again free of charge from 23:00 to 1:00.",
    U["tokeidai"], start="2026-12-15", to="2027-01-03")
N_TOKEIDAI_COLD = notice(
    "中は寒いままです（冷房も強い暖房もありません）", "The inside is cold (little heating, and no air conditioning)",
    "重要文化財なので、明治時代の姿のまま使われています。暖房はありますが、真冬に快適な室温にはならないと公式サイトに書かれています。上着は着たまま見てください。コインロッカーはありません（大きな荷物は1階の事務室前に置けます）。",
    "As a designated Important Cultural Property the building is kept close to its 1878 state. There is heating, but the official site says it does not reach a comfortable temperature in midwinter, so keep your coat on. There are no lockers, though large bags can be left by the office on the ground floor.",
    U["tokeidai_guide"])
N_TV_NY = notice(
    "テレビ塔は2027年1月1日が終日休業", "The TV Tower is closed all day on 1 January 2027",
    "設備点検のため、1月1日はテレ地下グルメコートも含めて全館休業です。",
    "The whole building, the basement food court included, closes for maintenance on 1 January.",
    U["tv_price"], start="2026-12-15", to="2027-01-01")
N_BEER_TOUR = notice(
    "ガイドツアーは予約が必要で、月曜は休みです", "The guided tour needs a booking and does not run on Mondays",
    "試飲付きガイドツアー（約55分、大人2,000円・入館料と試飲2杯つき）は、公式のチケットサイトで前の日までに予約します。当日のWEB予約は朝9:30まで。月曜は休止（月曜が祝日のときは実施し、翌火曜が休止）。ガイドの案内は日本語だけです。\n\n"
    "予約なしの「自由見学」（大人1,000円）には、日本語・英語・韓国語・中国語のスマートフォン用の音声ガイドがあります。英語で見たい人はこちらです。",
    "The tasting tour (about 55 minutes, ¥2,000 including admission and two beers) is booked through the official ticket site, up to 9:30 on the morning of the visit. It does not run on Mondays (if Monday is a public holiday it runs and the Tuesday is skipped), and the guiding is in Japanese only.\n\n"
    "The self-guided visit (¥1,000, no booking) comes with a smartphone audio guide in Japanese, English, Korean and Chinese, which is the better choice if you want it in English.",
    U["beer_guide"])
N_MOIWA_WINTER = notice(
    "冬（12月〜3月）は11:00から", "Winter hours (December – March): from 11:00",
    "ロープウェイは11:00〜22:00（上り最終21:30）、山頂行きのミニケーブルカーは11:10〜21:50（上り最終21:40）。夏（4月〜11月）は30分早い10:30からです。12月31日と1月1日は休業。\n\n"
    "上りの最終は21:30ですが、21:25ごろまでにチケットを買い終えてくださいと公式に書かれています。",
    "The ropeway runs 11:00–22:00 (last ride up 21:30) and the cable car to the summit 11:10–21:50 (last ride up 21:40). From April to November both start 30 minutes earlier, at 10:30. Closed on 31 December and 1 January.\n\n"
    "The last ride up is at 21:30, but the operator asks you to finish buying tickets by about 21:25.",
    U["moiwa_winter"], to="2027-03-28")
N_MOIWA_SHUT = notice(
    "2027年3月29日〜4月28日は全館休業", "Closed 29 March – 28 April 2027",
    "年次の整備点検で、ロープウェイもミニケーブルカーも山頂の施設も休みです。この期間に札幌にいる人は、夜景はテレビ塔の展望台（22:00まで）で。",
    "The ropeway, the cable car and the summit buildings all close for annual maintenance. If you are in Sapporo then, see the night view from the TV Tower observatory instead (open until 22:00).",
    U["moiwa_guide"], start="2027-02-28", to="2027-04-28")
N_MOIWA_SHUTTLE = notice(
    "行き方は、円山公園駅からのバスがいちばん楽です", "The easiest way up is the bus from Maruyama-koen Station",
    "地下鉄東西線「円山公園」駅の2番出口の前から、JR北海道バス ロープウェイ線［循環円11］が出ています。15分・240円で、終点の「もいわ山ロープウェイ」はロープウェイ乗り場に直結です。平日は15:10・15:35・15:50・16:00発などがあります。\n\n"
    "市電の「ロープウェイ入口」から行く方法もありますが、そこから山麓駅までの無料シャトルバスは平日は17:17から、土日祝は10:17から（冬期は10:47から）しか走りません。それより前に着くと、坂を10分ほど登ることになります。",
    "From in front of Exit 2 of Maruyama-koen Station on the Tozai subway line, JR Hokkaido Bus “Ropeway Line” (Junkan En 11) runs to the ropeway in 15 minutes for ¥240, stopping right at the base station. Weekday departures include 15:10, 15:35, 15:50 and 16:00.\n\n"
    "You can also take the tram to “Ropeway Iriguchi”, but the free shuttle from there to the base station only runs from 17:17 on weekdays and from 10:17 on weekends and holidays (10:47 in winter). Arrive before that and you have a ten-minute walk uphill.",
    U["moiwa_bus"])
N_MOIWA_WEATHER = notice(
    "霧や雪だと、何も見えない日があります", "On foggy or snowy days you may see nothing",
    "藻岩山は標高531m。雲の中に入ってしまう日があります。公式サイトに山頂展望台のライブカメラがあるので、出る前に見てください。夜景だけが目的なら、晴れた日に合わせるのがいちばんです。",
    "Mt. Moiwa is 531 m high and sometimes sits inside the cloud. The official site has a live camera at the summit observatory: check it before you set out. If the night view is the whole point, go on a clear evening.",
    U["moiwa_cam"])
N_ZOO_CLOSED = notice(
    "第2・第4水曜日は休園（12月29日〜31日も）", "Closed on the 2nd and 4th Wednesday of the month (and 29–31 December)",
    "円山動物園は毎月の第2・第4水曜日が休園（祝日の場合は翌日）。11月と4月は、第2水曜を含むその週の月曜から金曜まで休みます。12月29日〜31日も休園です。",
    "Maruyama Zoo closes on the second and fourth Wednesday of each month (the next day if that is a public holiday). In November and April it closes for the whole week, Monday to Friday, containing the second Wednesday. It also closes 29–31 December.",
    U["zoo_time"])
N_ZOO_WINTER = notice(
    "冬（11月〜2月）は16:00閉園", "Winter closing time (November – February): 16:00",
    "冬期（11月1日〜2月末日）は9:30〜16:00で、最終入園は15:30。3月からは16:30まで（最終入園16:00）になります。雪の日はホッキョクグマやユキヒョウが元気に動く季節です。",
    "From 1 November to the end of February the zoo is open 9:30–16:00, with last entry at 15:30; from March it closes at 16:30 (last entry 16:00). Snowy days are when the polar bears and snow leopards are at their liveliest.",
    U["zoo_time"], start="2026-10-20", to="2027-02-28")
N_SHIROI_ILLUM = notice(
    "イルミネーション期間は19:00まで（点灯は16:00）", "Open until 19:00 during the illumination season (lit from 16:00)",
    "2026年12月1日〜2027年3月31日は、パークの営業が10:00〜19:00になり、16:00から19:00までイルミネーションが点きます。イルミネーションは無料のエリアで見られます。\n\n"
    "有料エリア（工場の見学路・チョコレートラウンジなど）は時間が別で、チケットセンターの受付が16:30まで、工場などは17:30まで。先に有料エリアを見て、暗くなってから外のイルミネーションへ、という順番になります。",
    "From 1 December 2026 to 31 March 2027 the park is open 10:00–19:00 and the lights are on from 16:00 to 19:00. The illumination is in the free part of the park.\n\n"
    "The paid area (the factory walkway, the chocolate lounge and so on) keeps different hours: the ticket desk closes at 16:30 and the factory at 17:30. So see the paid area first, then step outside for the lights once it is dark.",
    U["shiroi_illum"], start="2026-12-01", to="2027-03-31")
N_MOERE_MON = notice(
    "ガラスのピラミッドは月曜休館。冬は噴水が止まります", "The Glass Pyramid is closed on Mondays, and the fountain stops in winter",
    "ガラスのピラミッドは9:00〜17:00、毎週月曜日が休館です。「海の噴水」は2026年度の運転を終えていて、冬は動きません。公園そのものは7:00〜22:00（東口ゲートからの入園は21:00まで）。\n\n"
    "冬は雪原になり、モエレ山をそり遊びやスノーシューで登る人がいます。用品のレンタルは2027年1月5日〜3月7日の10:00〜16:00（月曜休）。",
    "The Glass Pyramid is open 9:00–17:00 and closed on Mondays. The Sea Fountain has finished its 2026 season and does not run in winter. The park itself is open 7:00–22:00 (last entry through the East Gate 21:00).\n\n"
    "In winter the park becomes a snowfield and people climb Moere-yama with sledges or snowshoes. Equipment rental runs 5 January – 7 March 2027, 10:00–16:00, closed Mondays.",
    U["moere"])
N_MON = notice(
    "月曜は休みの施設があります", "Some places close on Mondays",
    "北海道大学総合博物館、札幌市資料館、モエレ沼公園のガラスのピラミッドは月曜が休み（祝日のときは翌平日）。サッポロビール博物館のガイドツアーも月曜は休止です。赤れんが庁舎・時計台・テレビ塔・藻岩山は月曜も開いています。",
    "The Hokkaido University Museum, the Sapporo City Archive Museum and the Glass Pyramid in Moerenuma Park all close on Mondays (the next weekday if Monday is a holiday), and the guided tour at the Sapporo Beer Museum does not run on Mondays either. The Red Brick Office, the Clock Tower, the TV Tower and Mt. Moiwa are open on Mondays.",
    None)
N_JOGAI_CHECK = notice(
    "店ごとに時間が違います", "Opening hours vary from shop to shop",
    "場外市場には公式のホームページがなく、札幌市の観光サイトには6:00〜15:00（大型店は6:00〜17:00）・無休と出ています。店によって時間が違い、昼すぎに閉める店もあります。朝のうちに行くのが確実です。",
    "The Curb Market has no official website; the city’s tourism site gives 6:00–15:00 (larger shops 6:00–17:00) and says it is open every day. Individual shops differ and some close early in the afternoon, so the morning is the safe time to go.",
    U["jogai"])

# ───────── 共通のリンク ─────────
L_SUBWAY = link("info", "札幌市交通局 乗車料金", "Sapporo subway and tram fares (city website)", U["subway"], U["fare_en"])
L_DONICHIKA = link("info", "ドニチカキップ・1日乗車券", "Day passes for the subway", U["donichika"], U["fare_en"])


def spots(c):
    """c は 'teiban'・'early'・'maruyama'。コースごとに回る場所と時間が変わる"""
    E = c == "early"

    S_EKI = dict(
        id="eki", name=T("札幌駅・大通（出発）", "Sapporo Station / Odori (start)"),
        kind=T("駅・地下街", "Station & underground walkway"),
        blurb=T("7:00に出発。地下鉄東西線で二十四軒へ、朝の市場へ。", "Leave at 7:00: the Tozai subway line to Nijuyonken and the morning market.") if E else
              T("9:15に出発。まずは歩いて赤れんが庁舎へ。", "Leave at 9:15 and walk to the Red Brick Office."),
        caution=T("地下鉄の始発は5時台。市電とバスはもう少し遅い", "The first subway is just after 05:00; the tram and buses start later"),
        lat=43.06846, lng=141.35076,
        body=T(
            ("札幌駅・大通・すすきののどのホテルからでも、このコースは始められます。7:00にホテルを出て、大通駅から地下鉄東西線で二十四軒（にじゅうよんけん）へ（7:13発→7:22着、250円）。\n\n"
             "札幌駅・大通・すすきのは地下街（さっぽろ地下街とチカホ）でつながっています。冬の朝は外に出ずに地下から地下鉄に乗れるので、ホテルを出るときから地下を歩くのが楽です。\n\n"
             "地下鉄・市電・市内のバスは Suica・Kitaca・PASMO・ICOCA などで乗れます。このコースは地下鉄に4回以上乗るので、1日乗車券（平日830円／土日祝520円）のほうが安くなります。券売機で買えます。"
             if E else
             "札幌駅・大通・すすきののどのホテルからでも、このコースは始められます。9:15にホテルを出れば、最初の赤れんが庁舎まで歩いて10〜20分です。\n\n"
             "札幌の街は碁盤の目で、「北3条西6丁目」のような住所がそのまま地図になっています。札幌駅から大通までは南へ約1km、大通からすすきのまでは約500m。この区間は地下街（さっぽろ地下街とチカホ）でつながっているので、冬や雨の日は地下を歩けます。\n\n"
             "地下鉄・市電・市内のバスは Suica・Kitaca・PASMO・ICOCA などで乗れます。このコースは地下鉄とバスを3〜4回使います。地下鉄だけなら1日乗車券（平日830円／土日祝520円）が得ですが、市電とバスには使えないので、ICカードのままでもかまいません。"),
            ("This course works from any hotel around Sapporo Station, Odori or Susukino. Leave at 7:00 and take the Tozai subway line from Odori to Nijuyonken (7:13 → 7:22, ¥250).\n\n"
             "Sapporo Station, Odori and Susukino are joined by an underground walkway. On a winter morning you can reach the subway without stepping outside, so start underground as you leave the hotel.\n\n"
             "The subway, tram and city buses all take Suica, Kitaca, PASMO, ICOCA and similar cards. This course uses the subway four times or more, so a day pass (¥830 on weekdays, ¥520 at weekends) costs less. Buy one from a ticket machine."
             if E else
             "This course works from any hotel around Sapporo Station, Odori or Susukino. Leave at 9:15 and the first stop, the Red Brick Office, is a 10–20 minute walk away.\n\n"
             "Sapporo is laid out on a grid, and addresses like “Kita 3 Nishi 6” are a map in themselves. It is about 1 km south from Sapporo Station to Odori and another 500 m to Susukino, all linked by an underground walkway you can use in snow or rain.\n\n"
             "The subway, tram and city buses all take Suica, Kitaca, PASMO, ICOCA and similar cards. This course uses the subway and a bus three or four times. A subway day pass (¥830 on weekdays, ¥520 at weekends) is good value, but it does not cover the tram or buses, so an IC card is fine too.")),
        gmaps=[gm("JR札幌駅", "JR Sapporo Station", 43.06846, 141.35076, "JR札幌駅"),
               gm("大通駅", "Odori Station", 43.05990, 141.35270, "札幌市営地下鉄 大通駅")],
        links=[L_SUBWAY, L_DONICHIKA],
        notices=[N_IC, N_WINTER, N_DARK, N_MON],
        rows=[row("train", "大通 7:13 → 二十四軒 7:22（地下鉄東西線、9分・250円）。次は7:17 → 7:26", "Odori 7:13 → Nijuyonken 7:22 (Tozai line, 9 min, ¥250); next 7:17 → 7:26") if E else
              row("walk", "札幌駅から赤れんが庁舎まで歩いて約10分、大通からは約10分、すすきのからは約20分", "About 10 minutes’ walk to the Red Brick Office from Sapporo Station or Odori, about 20 from Susukino"),
              row("fee", "地下鉄 210〜380円、市電230円、地下鉄と市電の乗り継ぎ360円から", "Subway ¥210–380, tram ¥230, subway-to-tram transfer from ¥360"),
              row("fee", "地下鉄専用1日乗車券 大人830円（平日）。ドニチカキップ 大人520円（土日祝と12月29日〜1月3日、現金のみ）", "Subway 1-Day Card ¥830 (weekdays); Donichika Kippu ¥520 (weekends, holidays and 29 Dec – 3 Jan, cash only)"),
              row("pay", "Kitaca・Suica・PASMO・ICOCA などのICカードが地下鉄・市電・市内のバスで使えます", "Kitaca, Suica, PASMO, ICOCA and other IC cards work on the subway, tram and city buses")],
        tip=T("運賃と1日乗車券は札幌市交通局の公式ページ、地下鉄の時刻は乗換案内（2026年12月3日・5日のダイヤ）で確認しました。",
              "Fares and day passes from the Sapporo transport bureau’s official pages; subway times checked in a route planner for 3 and 5 December 2026."),
        time=(DEP, "7:00（朝の市場に合わせる日）", "7:00 (to catch the morning market)") if E else (DEP, "9:15（ホテルを出る時間）", "9:15 (leave your hotel)"),
        photos=W("eki"))

    S_JOGAI = dict(
        id="jogai", name=T("札幌市中央卸売市場 場外市場（じょうがいしじょう）", "Sapporo Central Wholesale Market Curb Market"),
        kind=T("市場・朝ごはん", "Market & breakfast"),
        blurb=T("朝6時から。海鮮丼で1日を始める場所。", "Open from 06:00: a seafood bowl to start the day."),
        caution=T("昼すぎに閉める店があります", "Some shops close in the early afternoon"),
        lat=43.07033, lng=141.31750,
        body=T(
            "札幌市中央卸売市場のすぐ横にある、鮮魚店・青果店・乾物店など約60店の市場です。朝6時から開いていて、カニ・ウニ・イクラ・ホタテが氷の上に並びます。市場の中と周りには食堂があり、朝から海鮮丼を出す店が多いです。\n\n"
            "二十四軒（にじゅうよんけん）駅の7番出口から歩いて8分ほど。地下鉄の出口を出て、北西へまっすぐです。\n\n"
            "買った魚を送ってもらうこともできます。店によって時間が違い、昼すぎに閉める店もあるので、朝のうちに行くのが確実です。食堂は8時前から開いている店が多く、7:30に着けば席が選べます。",
            "About sixty shops — fishmongers, greengrocers, dried-goods sellers — alongside Sapporo’s central wholesale market. It opens at 06:00, with crab, sea urchin, salmon roe and scallops laid out on ice, and the restaurants in and around it serve seafood rice bowls from early morning.\n\n"
            "It is about an eight-minute walk from Exit 7 of Nijuyonken subway station: out of the exit and straight to the north-west.\n\n"
            "Shops will ship what you buy. Hours vary and some close in the early afternoon, so the morning is the safe time. Most of the restaurants open before 08:00; arrive at 07:30 and you can pick your table."),
        gmaps=[gm("場外市場", "Curb Market", 43.07033, 141.31750, "札幌市中央卸売市場 場外市場"),
               gm("地下鉄 二十四軒駅", "Nijuyonken Station", 43.07048, 141.32851, "札幌市営地下鉄 二十四軒駅")],
        links=[link("info", "場外市場（札幌市の観光サイト）", "Curb Market (Sapporo’s official tourism site)", U["jogai"]), L_SUBWAY],
        notices=[N_JOGAI_CHECK, N_WINTER],
        rows=[row("hours", "6:00〜15:00（大型店は6:00〜17:00）、無休。店によって違います", "6:00–15:00 (larger shops to 17:00), open every day; hours vary by shop"),
              row("walk", "地下鉄東西線「二十四軒」駅から徒歩約8分", "About 8 minutes’ walk from Nijuyonken Station (Tozai line)"),
              row("pay", "現金だけの店があります", "Some shops take cash only"),
              row("fee", "海鮮丼はおおよそ1,500〜4,000円（店によります）", "Seafood bowls run roughly ¥1,500–4,000 depending on the shop")],
        tip=T("場外市場には公式のホームページがなく、時間は札幌市の観光サイトの情報です（要確認）。値段も店によって違います。",
              "The market has no official website, so the hours come from the city’s tourism site and should be checked. Prices vary by shop."),
        time=(VIS, "7:30〜8:40（朝ごはん）", "7:30–8:40 (breakfast)"),
        verified=False, photos=W("jogai"))

    S_HOKUDAI = dict(
        id="hokudai", name=T("北海道大学（ほっかいどうだいがく） 札幌キャンパス", "Hokkaido University, Sapporo campus"),
        kind=T("大学の構内・並木道", "University campus & tree-lined avenues"),
        blurb=T("札幌駅のすぐ北。ポプラ並木と、無料の総合博物館。", "Just north of Sapporo Station: the poplar avenue and a free museum."),
        caution=T("総合博物館は月曜休館（10:00〜17:00）", "The university museum is closed on Mondays (10:00–17:00)"),
        lat=43.07262, lng=141.34718,
        body=T(
            "1876年の札幌農学校から続く大学で、構内は南北に1.7kmあります。札幌駅の北口から正門まで歩いて10分ほど。だれでも歩いて入れます。\n\n"
            "見どころは、幅の広い道の両側に伸びるイチョウ並木（北13条通。10月下旬から11月上旬が黄色）と、奥のポプラ並木、そして無料の総合博物館です。博物館は1929年の理学部の建物で、恐竜のニッポノサウルスの骨格やマンモスの標本、札幌農学校以来の標本が並びます。開館は10:00〜17:00、月曜休館。\n\n"
            "冬は構内が雪原になり、並木道が雪で縁取られます。除雪された道は歩けますが、脇に入ると膝まで沈むので、道から出ないこと。\n\n"
            "7:00に出発したこのコースでは、9:20ごろに正門。構内を北へ歩いてポプラ並木まで行き、10:00に博物館が開いたら入って、10:50ごろに南へ戻ります。クラーク博士の胸像は構内の中ほど（農学部の前）です。",
            "The university grew out of the Sapporo Agricultural College of 1876, and its campus runs 1.7 km from north to south. The main gate is about a ten-minute walk from the north exit of Sapporo Station, and anyone may walk in.\n\n"
            "The things to see are the ginkgo avenue along Kita 13-jo (golden from late October into early November), the poplar avenue further in, and the free university museum. The museum occupies the 1929 science building and holds the skeleton of the dinosaur Nipponosaurus, mammoth material and specimens collected since the Agricultural College days. It is open 10:00–17:00 and closed on Mondays.\n\n"
            "In winter the campus turns into a snowfield with the avenues outlined in white. The cleared paths are easy to walk, but step off them and you sink to the knee, so stay on the path.\n\n"
            "On this early course you reach the main gate at about 9:20. Walk north through the campus to the poplar avenue, go into the museum when it opens at 10:00, and head back south at around 10:50. The bust of Dr Clark stands midway along, in front of the agriculture building."),
        gmaps=[gm("北海道大学 正門", "Hokkaido University Main Gate", 43.07262, 141.34718, "北海道大学 正門"),
               gm("総合博物館", "Hokkaido University Museum", 43.07666, 141.34316, "北海道大学総合博物館"),
               gm("ポプラ並木", "Poplar Avenue", 43.07693, 141.33972, "北海道大学 ポプラ並木")],
        links=[link("official", "北海道大学 キャンパスガイド", "Hokkaido University campus guide", U["hokudai"]),
               link("official", "北海道大学総合博物館", "Hokkaido University Museum", U["hokudai_m"])],
        notices=[N_MON, N_WINTER],
        rows=[row("hours", "構内はいつでも歩けます。総合博物館は10:00〜17:00", "The campus is open to walk through; the museum is open 10:00–17:00"),
              row("closed", "総合博物館は月曜休館（祝日は開館し、翌平日が休館）", "The museum closes on Mondays (open on public holidays, closed the next weekday instead)"),
              row("fee", "構内・総合博物館とも無料", "Both the campus and the museum are free"),
              row("walk", "札幌駅北口から正門まで徒歩約10分。正門からポプラ並木まで徒歩約20分", "About 10 minutes from the station’s north exit to the main gate, and 20 more to the poplar avenue")],
        tip=T("総合博物館の時間と休館日、入館料は公式サイトで確認しました。イチョウ並木の色づく時期は年によって前後します。",
              "The museum’s hours, closing days and free admission are from its official site. When the ginkgo avenue turns gold varies from year to year."),
        time=(VIS, "9:20〜10:50（博物館は10:00開館）", "9:20–10:50 (the museum opens at 10:00)"),
        photos=W("hokudai"))

    S_AKARENGA = dict(
        id="akarenga", name=T("北海道庁旧本庁舎（赤れんが庁舎）", "Former Hokkaido Government Office (the Red Brick Office)"),
        kind=T("重要文化財・展示", "Important Cultural Property & exhibitions"),
        blurb=T("1888年の赤れんが。5年の改修を終えて2025年に再開館。", "An 1888 red brick building, reopened in 2025 after five years of restoration."),
        caution=T("12月29日〜1月3日と11月15日は休館", "Closed 29 Dec – 3 Jan and on 15 November"),
        lat=43.06424, lng=141.34754,
        body=T(
            "1888年（明治21年）に建った、北海道庁の最初の本庁舎。アメリカ風のネオ・バロック様式で、約250万個のれんがを積んでいます。1969年に国の重要文化財になりました。\n\n"
            "2019年から5年あまりの大規模改修に入っていて、2025年7月25日に再開館しました。中は北海道の歴史とこれからをあつかう展示に作り替えられ、八角塔（屋根の上の塔）に登る観覧（1,200円・小学生以上）も始まっています。\n\n"
            "入館料は一般300円。開館は8:45から21:00まで（最終入館20:30）で、朝いちばんでも、夜のついでにでも入れる長さです。1階の店舗だけなら無料で入れます。\n\n"
            "前庭の池に建物が映るところが、写真でよく見る眺めです。冬は雪の中に赤いれんがが立って、11月20日から2月28日まではライトアップされます。",
            "Built in 1888 as Hokkaido’s first prefectural office, in an American neo-baroque style, from some 2.5 million bricks. It was designated an Important Cultural Property in 1969.\n\n"
            "After more than five years of major restoration from 2019 it reopened on 25 July 2025, with new exhibitions on Hokkaido’s past and future and a paid tour up into the octagonal tower on the roof (¥1,200, primary school age and up).\n\n"
            "Admission is ¥300. It is open from 8:45 all the way to 21:00 (last entry 20:30), so it fits first thing in the morning or on the way back in the evening. The shops on the ground floor are free to enter.\n\n"
            "The classic view is the building reflected in the pond in the front garden. In winter the red brick stands in the snow, and from 20 November to 28 February it is floodlit."),
        gmaps=[gm("赤れんが庁舎", "Red Brick Office", 43.06424, 141.34754, "北海道庁旧本庁舎")],
        links=[link("official", "赤れんが庁舎 公式サイト", "Red Brick Office official site", U["akarenga"], U["akarenga"] + "en/"),
               link("info", "施設案内（八角塔観覧など）", "Facilities and the octagonal tower tour", U["akarenga_guide"])],
        notices=[N_AKARENGA_ILLUM, N_AKARENGA_CLOSED, N_WINTER],
        rows=[row("hours", "8:45〜21:00（最終入館20:30）", "8:45–21:00 (last entry 20:30)"),
              row("closed", "11月15日、12月29日〜1月3日", "15 November and 29 December – 3 January"),
              row("fee", "一般300円、大学生・高校生200円、中学生以下無料。1階の店舗だけなら無料", "Adults ¥300, university and high school students ¥200, junior high and younger free; the ground-floor shops are free"),
              row("fee", "八角塔観覧 1,200円（小学生以上）。12月は催行時間が変わります", "Octagonal tower tour ¥1,200 (primary school age and up); times change in December"),
              row("walk", "札幌駅から徒歩約10分、大通から徒歩約10分", "About 10 minutes’ walk from Sapporo Station or from Odori")],
        tip=T("時間・休館日・料金は公式サイトで確認しました。八角塔観覧は12月の催行時間変更のお知らせが出ているので、登りたい人は公式サイトを見てください。",
              "Hours, closing days and prices are from the official site. A notice says the octagonal tower tour runs at different times in December, so check the site if you want to go up."),
        time=(VIS, "11:10〜11:55", "11:10–11:55") if E else (VIS, "9:30〜10:15", "9:30–10:15"),
        photos=W("akarenga"))

    S_TOKEIDAI = dict(
        id="tokeidai", name=T("札幌市時計台（さっぽろしとけいだい）", "Sapporo Clock Tower"),
        kind=T("重要文化財・展示", "Important Cultural Property & exhibition"),
        blurb=T("1878年の演武場。10:30に時計を手で巻く実演。", "An 1878 drill hall; the clock is wound by hand at 10:30."),
        caution=T("1月1日〜3日は休館。中は寒いです", "Closed 1–3 January. The inside is cold"),
        lat=43.06268, lng=141.35367,
        body=T(
            "1878年（明治11年）に札幌農学校の演武場として建てられた建物で、2026年10月16日で創建148年になりました。屋根の時計は重りで動く塔時計で、いまも動いています。\n\n"
            "1日1回、10:30から時計の巻き上げの実演と説明があります。重りを人の手で巻き上げる様子を見られるのはこの時間だけです。\n\n"
            "ビルに囲まれた場所に建っているので、「思っていたより小さい」と言われます。正面からだと背景にビルが入るので、少し斜めから、または夜のライトアップで撮る人が多いです。中は2階が演武場の広間で、椅子に座って見られます。\n\n"
            "観覧料は大人350円、小中学生と高校生は無料。重要文化財なので明治時代のままに使われていて、冷房がなく、暖房も真冬は効ききれません。上着を着たまま見てください。",
            "Built in 1878 as the drill hall of the Sapporo Agricultural College, it turned 148 years old in October 2026. The clock in the roof is a weight-driven tower clock, still running.\n\n"
            "Once a day, at 10:30, a staff member winds the clock and explains how it works. That is the only time you can watch the weights being raised by hand.\n\n"
            "Hemmed in by office buildings, it strikes many visitors as smaller than expected. Straight on, the towers behind get in the frame, so most people shoot it from an angle, or at night when it is lit. Inside, the upstairs hall is the old drill hall, with chairs to sit in.\n\n"
            "Admission is ¥350 for adults and free for school students up to high school. As an Important Cultural Property it is kept as it was in Meiji times: there is no air conditioning, and the heating cannot keep up in midwinter, so keep your coat on."),
        gmaps=[gm("札幌市時計台", "Sapporo Clock Tower", 43.06268, 141.35367, "札幌市時計台")],
        links=[link("official", "札幌市時計台 公式サイト", "Sapporo Clock Tower official site", U["tokeidai"], U["tokeidai_en"]),
               link("info", "観覧案内（料金・注意）", "Visitor information (fees and notes)", U["tokeidai_guide"])],
        notices=[N_TOKEIDAI_COLD, N_TOKEIDAI_NY],
        rows=[row("hours", "8:45〜17:10（入館は17:00まで）。1日1回10:30から時計の巻き上げ実演", "8:45–17:10 (last entry 17:00); the clock is wound at 10:30, once a day"),
              row("closed", "1月1日〜3日", "1–3 January"),
              row("fee", "大人350円、大学生150円、小中学生・高校生は無料", "Adults ¥350, university students ¥150, school students up to high school free"),
              row("pay", "クレジットカード・交通系ICカード・QRコード決済が使えます", "Credit cards, transport IC cards and QR payments accepted"),
              row("walk", "赤れんが庁舎から徒歩約8分、大通公園から徒歩約5分", "About 8 minutes’ walk from the Red Brick Office, 5 from Odori Park")],
        tip=T("時間・休館日・料金は公式サイトの観覧案内で確認しました。毎月16日は札幌市民が無料です。",
              "Hours, closing days and fees are from the official visitor information page. Sapporo residents get in free on the 16th of each month."),
        time=(VIS, "12:05〜12:35", "12:05–12:35") if E else (VIS, "10:25〜11:00（10:30の実演に合わせる）", "10:25–11:00 (in time for the 10:30 winding)"),
        photos=W("tokeidai"))

    if c == "maruyama":
        odori_body = T(
            "1.5kmの細長い公園が、街を東西に貫いています。東の端に立つのがさっぽろテレビ塔（1957年）。展望台は地上90mで、エレベーターで60秒。9:00から22:00まで開いていて、入場は大人1,200円です。\n\n"
            "このコースでは、宮の沢やモエレ沼から戻ってきた17時すぎに歩きます。冬は11月20日から12月25日まで「さっぽろホワイトイルミネーション」の大通会場（16:30〜22:00）で、西2丁目には「ミュンヘン・クリスマス市 in Sapporo」（11:00〜21:00）のヒュッテが並びます。ホットワインのカップは中身とは別に代金がかかり、返すと戻る仕組みの店が多いです。\n\n"
            "大通会場は12月25日で終わりますが、駅前通は2月11日まで、赤れんが庁舎のまわりとアカプラは3月14日まで続きます。2月4日〜11日は雪まつりの雪像が並びます。\n\n"
            "テレビ塔の展望台から見下ろすと、光の列がまっすぐ西へ伸びているのが分かります。寒い日は、展望台からガラス越しに見るのが暖かくて確実です。",
            "A ribbon of park 1.5 km long cuts the city from east to west, with the Sapporo TV Tower (1957) standing at its eastern end. The observatory is 90 m up, 60 seconds by lift, open 9:00–22:00, ¥1,200 for adults.\n\n"
            "On this course you walk it after 17:00, coming back from Miyanosawa or Moerenuma. In winter the Odori site of the Sapporo White Illumination is lit from 16:30 to 22:00 between 20 November and 25 December, and the huts of the Munich Christmas Market fill Nishi 2-chome from 11:00 to 21:00. Mulled wine usually comes with a deposit on the cup, refunded when you bring it back.\n\n"
            "The Odori site ends on 25 December, but Ekimae-dori stays lit until 11 February and the Red Brick grounds and Akapura square until 14 March. From 4 to 11 February the snow sculptures of the Snow Festival stand here.\n\n"
            "From the TV Tower observatory you can see the line of lights running straight west. On a cold evening, watching from behind the glass up there is both warmer and more reliable.")
        odori_time = (VIS, "17:05〜18:10（イルミネーションの時間）", "17:05–18:10 (illumination time)")
    elif E:
        odori_body = T(
            "1.5kmの細長い公園が、街を東西に貫いています。東の端に立つのがさっぽろテレビ塔（1957年）。展望台は地上90mで、エレベーターで60秒。9:00から22:00まで開いています（展望最終入場21:50）。入場は大人1,200円、小中学生600円。\n\n"
            "お昼どきのこの時間は、テレビ塔に上がって札幌の碁盤の目を上から見るのに向いています。西へまっすぐ伸びる公園と、その奥の藻岩山（このあと夜に登る山）が同時に見えます。\n\n"
            "公園の中には噴水とベンチ、トウモロコシのワゴン（夏）があり、冬は雪に埋まります。地下では「チカホ」（札幌駅前通地下歩行空間）が札幌駅まで続いているので、寒い日の移動はここを使ってください。\n\n"
            "時計台との共通入場券があります（金額は公式サイトの案内で確かめてください）。",
            "A ribbon of park 1.5 km long cuts the city from east to west, with the Sapporo TV Tower (1957) at its eastern end. The observatory is 90 m up, 60 seconds by lift, and open 9:00–22:00 (last entry 21:50). Adults ¥1,200, school students ¥600.\n\n"
            "Around midday it is a good moment to go up and look down on Sapporo’s grid: the park running dead straight to the west, and behind it Mt. Moiwa, the hill you will climb this evening.\n\n"
            "The park has fountains, benches and sweetcorn wagons in summer; in winter it is buried in snow. Underneath, the Chi-Ka-Ho walkway runs all the way to Sapporo Station, which is the way to move about on a cold day.\n\n"
            "There is a combined ticket with the Clock Tower; check the price on the tower’s own pages.")
        odori_time = (VIS, "12:45〜13:30", "12:45–13:30")
    else:
        odori_body = T(
            "1.5kmの細長い公園が、街を東西に貫いています。東の端に立つのがさっぽろテレビ塔（1957年）。展望台は地上90mで、エレベーターで60秒。9:00から22:00まで開いています（展望最終入場21:50）。入場は大人1,200円、小中学生600円。\n\n"
            "午前のこの時間は人が少なく、展望台から札幌の碁盤の目を見下ろせます。西へまっすぐ伸びる公園の奥に、このあと夜に登る藻岩山が見えます。\n\n"
            "冬は11月20日から12月25日まで、公園が「さっぽろホワイトイルミネーション」の大通会場になります（点灯16:30〜22:00）。西2丁目には「ミュンヘン・クリスマス市 in Sapporo」（11:00〜21:00）のヒュッテが並び、昼から開いています。2月4日〜11日は雪まつりの雪像が並びます。\n\n"
            "夜にもう一度ここへ戻ってくるなら、すすきのからは歩いて10分ほどです。時計台との共通入場券もあります（金額は公式サイトで確かめてください）。",
            "A ribbon of park 1.5 km long cuts the city from east to west, with the Sapporo TV Tower (1957) at its eastern end. The observatory is 90 m up, 60 seconds by lift, and open 9:00–22:00 (last entry 21:50). Adults ¥1,200, school students ¥600.\n\n"
            "At this hour it is quiet, and from the observatory you look down on Sapporo’s grid: the park running dead straight to the west, and beyond it Mt. Moiwa, the hill you will climb tonight.\n\n"
            "In winter, from 20 November to 25 December, the park becomes the Odori site of the Sapporo White Illumination (lit 16:30–22:00). The huts of the Munich Christmas Market stand at Nishi 2-chome from 11:00 to 21:00, open from midday. From 4 to 11 February the Snow Festival’s sculptures fill the park.\n\n"
            "If you want to come back after dark, it is a ten-minute walk from Susukino. There is also a combined ticket with the Clock Tower; check the price on the official pages.")
        odori_time = (VIS, "11:10〜12:00", "11:10–12:00")

    S_ODORI = dict(
        id="odori", name=T("大通公園（おおどおりこうえん）・さっぽろテレビ塔", "Odori Park & the Sapporo TV Tower"),
        kind=T("公園・展望台", "Park & observatory"),
        blurb=T("夜はイルミネーション。テレビ塔は22時まで。", "Illuminated after dark; the TV Tower is open until 22:00.") if c == "maruyama" else
              T("街を東西に貫く1.5kmの公園と、90mの展望台。", "A 1.5 km park across the city, and a 90 m observatory."),
        caution=T("テレビ塔は2027年1月1日が終日休業", "The TV Tower closes all day on 1 January 2027"),
        lat=43.06100, lng=141.35650,
        body=odori_body,
        gmaps=[gm("さっぽろテレビ塔", "Sapporo TV Tower", 43.06100, 141.35650, "さっぽろテレビ塔"),
               gm("大通公園 西4丁目", "Odori Park, Nishi 4-chome", 43.05949, 141.35192, "大通公園 西4丁目")],
        links=[link("official", "さっぽろテレビ塔 公式サイト", "Sapporo TV Tower official site", U["tv"], U["tv"] + "en/"),
               link("info", "展望台の料金・営業時間", "Observatory fees and hours", U["tv_price"]),
               link("info", "さっぽろホワイトイルミネーション", "Sapporo White Illumination", U["illum"]),
               link("info", "さっぽろ雪まつり", "Sapporo Snow Festival", U["snowfes"])],
        notices=[N_ILLUM, N_SNOWFES, N_TV_NY, N_DARK],
        rows=[row("hours", "テレビ塔 9:00〜22:00（展望最終入場21:50）", "TV Tower 9:00–22:00 (last entry to the observatory 21:50)"),
              row("fee", "展望台 大人（高校生以上）1,200円、小中学生600円、幼児無料", "Observatory: adults (high school and up) ¥1,200, school students ¥600, pre-school free"),
              row("closed", "テレビ塔は2027年1月1日 終日休業（設備点検）", "The TV Tower is closed all day on 1 January 2027 for maintenance"),
              row("season", "ホワイトイルミネーション 大通会場は11月20日〜12月25日、16:30〜22:00。入場無料", "White Illumination, Odori site: 20 Nov – 25 Dec, 16:30–22:00, free", until="2026-12-25"),
              row("season", "ミュンヘン・クリスマス市（大通西2丁目）11月20日〜12月25日 11:00〜21:00", "Munich Christmas Market (Odori Nishi 2-chome): 20 Nov – 25 Dec, 11:00–21:00", until="2026-12-25"),
              row("season", "さっぽろ雪まつり 2027年2月4日〜11日（大通・すすきの・つどーむ）", "Sapporo Snow Festival: 4–11 February 2027 (Odori, Susukino and Tsudome)", until="2027-02-11"),
              row("walk", "公園そのものはいつでも歩けます（無料）", "The park itself is always open and free")],
        tip=T("テレビ塔の時間・料金・休業日は公式サイト、イルミネーションと雪まつりの日程は札幌市の観光サイトの公式ガイドブックと雪まつり公式サイトで確認しました。",
              "The TV Tower’s hours, prices and closing day are from its official site; the illumination and Snow Festival dates come from the city’s official guidebook and the festival’s own site."),
        time=odori_time,
        photos=W("odori"))

    S_SHIRYOKAN = dict(
        id="shiryokan", name=T("札幌市資料館（旧札幌控訴院）", "Sapporo City Archive Museum (the former Court of Appeals)"),
        kind=T("重要文化財・無料の展示", "Important Cultural Property, free exhibition"),
        blurb=T("大通公園の西の端。無料で、刑事法廷が残っています。", "At the west end of Odori Park: free, with the old criminal courtroom kept intact."),
        caution=T("月曜休館（祝日のときは翌平日）", "Closed on Mondays (the next weekday if Monday is a holiday)"),
        lat=43.05813, lng=141.33694,
        body=T(
            "大通公園を西の端（西13丁目）まで歩いた先に建つ、1926年の軟石の建物です。もとは控訴院（いまの高等裁判所）で、国の重要文化財。中に当時の刑事法廷がそのまま残っていて、無料で見られます。法服を貸し出していて、着て座ることもできます。\n\n"
            "開館は9:00〜19:00、入館無料、月曜休館（祝日のときは翌平日）。年末年始は12月29日〜1月3日が休みです。\n\n"
            "テレビ塔から大通公園を歩いて西へ約20分。公園の中をずっと歩いて行けるので、晴れた日の散歩に向いています。冬は雪の中の軟石の建物になります。帰りは地下鉄東西線「西11丁目」駅が近いです。",
            "At the far west end of Odori Park (Nishi 13-chome) stands this 1926 building of local soft stone. It was the Court of Appeals — today’s High Court — and is an Important Cultural Property. The old criminal courtroom survives inside and can be seen free of charge; judges’ robes are lent out, and you may sit in them.\n\n"
            "Open 9:00–19:00, free, closed on Mondays (the next weekday if Monday is a public holiday) and from 29 December to 3 January.\n\n"
            "It is about a 20-minute walk west from the TV Tower, the whole way through the park, which makes a good stroll on a fine day; in winter it is a stone building in the snow. Nishi 11-chome subway station (Tozai line) is the nearest for the way back."),
        gmaps=[gm("札幌市資料館", "Sapporo City Archive Museum", 43.05813, 141.33694, "札幌市資料館")],
        links=[link("official", "札幌市資料館 入館案内", "Sapporo City Archive Museum (visitor information)", U["shiryokan"])],
        notices=[N_MON],
        rows=[row("hours", "9:00〜19:00", "9:00–19:00"),
              row("closed", "月曜日（祝日にあたる場合は翌平日）、12月29日〜1月3日", "Mondays (the next weekday if Monday is a holiday) and 29 December – 3 January"),
              row("fee", "入館無料", "Free"),
              row("walk", "テレビ塔から大通公園を西へ徒歩約20分。地下鉄東西線「西11丁目」駅から徒歩約5分", "About 20 minutes’ walk west from the TV Tower through the park; 5 minutes from Nishi 11-chome Station")],
        tip=T("開館時間・休館日・入館無料は公式サイトの入館案内で確認しました。刑事法廷展示室の個別の見学時間は公式サイトに書かれていません。",
              "Hours, closing days and free admission are from the official visitor information. The site does not give separate hours for the courtroom room itself."),
        time=(VIS, "12:10〜12:50（寄り道）", "12:10–12:50 (side trip)"),
        photos=W("shiryokan"))

    S_NIJO = dict(
        id="nijo", name=T("二条市場（にじょういちば）", "Nijo Market"),
        kind=T("市場・お昼", "Market & lunch"),
        blurb=T("お昼はここか、狸小路。海鮮丼の食堂が並びます。", "Lunch here or in Tanukikoji: a row of seafood-bowl restaurants.") if E else
              T("街なかで海鮮丼。狸小路から徒歩1分。", "Seafood bowls in the centre of town, a minute from Tanukikoji."),
        caution=T("店によって時間が違います（だいたい7時〜17時）", "Hours vary by shop (roughly 07:00–17:00)"),
        lat=43.05694, lng=141.35736,
        body=T(
            "創成川の東側、南3条東1〜2丁目のアーケードに並ぶ市場です。明治のはじめ、石狩浜の漁師が石狩川をさかのぼってこのあたりで魚を売ったのが始まりといわれ、125年以上「札幌市民の台所」と呼ばれてきました。\n\n"
            "カニ・ウニ・イクラ・ホタテが氷の上に並び、その場で食べられる店と、海鮮丼の食堂、土産物店が軒を連ねています。公式の店舗情報では、営業時間は店によって違い、だいたい朝7時ごろから夜17時ごろまで、年中無休です。\n\n"
            "大通公園からは歩いて10分ほど、狸小路商店街の1丁目からは徒歩1分。地下鉄なら「バスセンター前」駅が近いです。\n\n"
            + ("朝ごはんにも使えますが、場外市場より小さく、朝いちばんから開く食堂は少なめです。このコースではお昼に寄る場所にしてあります。"
               if E else
               "お昼は12時台が混みます。少し早めの11:45か、13時すぎが入りやすい時間です。市場の値段は店によって違い、現金だけの店もあります。"),
            "A market under an arcade on the east side of Sosei River, at Minami 3-jo Higashi 1–2 chome. The story goes that fishermen from the Ishikari coast came up the river in early Meiji times and sold their catch here; for more than 125 years it has been called “Sapporo’s kitchen”.\n\n"
            "Crab, sea urchin, salmon roe and scallops lie on the ice, with stalls that will serve them on the spot, restaurants doing seafood rice bowls, and souvenir shops. The market’s own shop listing says hours vary by shop, roughly 07:00 to 17:00, open every day.\n\n"
            "It is about ten minutes’ walk from Odori Park and one minute from 1-chome of the Tanukikoji arcade; the nearest subway station is Bus Center-mae.\n\n"
            + ("It works for breakfast too, but it is smaller than the Curb Market and fewer places open at first light, so on this course it is a midday stop."
               if E else
               "Noon is the busy hour: 11:45 or after 13:00 is easier. Prices differ from shop to shop, and some take cash only.")),
        gmaps=[gm("二条市場", "Nijo Market", 43.05694, 141.35736, "札幌二条市場")],
        links=[link("official", "札幌二条市場 公式サイト", "Nijo Market official site", U["nijo"], U["nijo_en"]),
               link("info", "店舗情報・営業時間", "Shops and hours", U["nijo_about"])],
        notices=[N_WINTER],
        rows=[row("hours", "だいたい7:00〜17:00（店によって違います）、年中無休", "Roughly 7:00–17:00 (varies by shop), open every day"),
              row("fee", "海鮮丼はおおよそ1,500〜4,000円（店によります）", "Seafood bowls run roughly ¥1,500–4,000 depending on the shop"),
              row("pay", "現金だけの店があります", "Some shops take cash only"),
              row("walk", "大通公園から徒歩約10分、狸小路1丁目から徒歩約1分", "About 10 minutes’ walk from Odori Park, 1 minute from Tanukikoji 1-chome")],
        tip=T("営業時間と場所は公式サイトの店舗情報で確認しました。店ごとの時間と値段は公式には出ていません。",
              "The hours and location are from the market’s official shop listing. Individual shops’ hours and prices are not published officially."),
        time=(VIS, "13:40〜14:30（お昼。狸小路とどちらか）", "13:40–14:30 (lunch; this or Tanukikoji)") if E else (VIS, "12:30〜13:30（お昼）", "12:30–13:30 (lunch)"),
        photos=W("nijo"))

    S_TANUKI = dict(
        id="tanukikoji", name=T("狸小路商店街（たぬきこうじしょうてんがい）", "Tanukikoji shopping arcade"),
        kind=T("アーケード商店街", "Covered shopping street"),
        blurb=T("約900mの全蓋アーケード。雨も雪も関係なし。", "900 m of fully roofed arcade: rain and snow do not matter.") if not E else
              T("お昼はここか、二条市場。ラーメン、スープカレー、海鮮。", "Lunch here or at Nijo Market: ramen, soup curry, seafood."),
        caution=T("店ごとに定休日が違います", "Each shop has its own closing day"),
        lat=43.05638, lng=141.35322,
        body=T(
            "明治6年（1873年）から「狸小路」と呼ばれてきた、北海道でいちばん古い商店街のひとつ。2026年で153年になりました。7ブロック・総延長約900mの全蓋（ぜんがい）アーケードに、約200軒が並びます。屋根が交差する道路の上まで続いているので、雪の日も雨の日もぬれずに歩けます。\n\n"
            + ("このコースでは、ここでお昼にします。味噌ラーメン、スープカレー（札幌で生まれた料理）、海鮮、ジンギスカンなど、たいていのものがこの一帯にあります。昼どきは混むので、12時前か13時すぎが入りやすいです。\n\n"
               if E else
               "二条市場でお昼を食べたあと、西へ歩いて散歩がてら見るのにちょうどよい場所です。寒い日や雪の日の「歩ける場所」としても役に立ちます。\n\n")
            + "東の端は二条市場のすぐそば、西の端は地下鉄東西線「西11丁目」駅のあたり。南へ1本入るとすすきので、夜はこの一帯が明るくなります。\n\n"
            "店ごとに定休日と時間が違います。このマップでは個別の店名は挙げていません（公式サイトで時間を確かめられた店だけを載せる方針のため）。",
            "One of Hokkaido’s oldest shopping streets, known as Tanukikoji since 1873 — 153 years old in 2026. Seven blocks, about 900 m in all, are fully roofed over, with some two hundred shops: souvenirs, drugstores, vintage clothing and restaurants side by side. The roof carries on over the cross streets, so you stay dry through snow and rain.\n\n"
            + ("This is where this course stops for lunch. Miso ramen, soup curry (a Sapporo invention), seafood, grilled lamb: most of it is somewhere in these blocks. It fills up at noon, so before 12:00 or after 13:00 is easier.\n\n"
               if E else
               "After lunch at Nijo Market it makes an easy westward stroll, and on a cold or snowy day it is simply somewhere you can walk.\n\n")
            + "The eastern end is right by Nijo Market and the western end near Nishi 11-chome subway station. One street south is Susukino, and the whole area lights up at night.\n\n"
            "Each shop keeps its own hours and closing days. This map does not name individual restaurants here, since it only names places whose hours could be checked on an official site."),
        gmaps=[gm("狸小路3丁目", "Tanukikoji 3-chome", 43.05638, 141.35322, "狸小路商店街 3丁目"),
               gm("狸小路1丁目（二条市場側）", "Tanukikoji 1-chome (Nijo Market end)", 43.05650, 141.35700, "狸小路商店街 1丁目")],
        links=[link("official", "札幌狸小路商店街 公式サイト", "Tanukikoji shopping arcade official site", U["tanuki"]),
               link("info", "商店街の歴史", "The arcade’s history", U["tanuki"] + "about/")],
        notices=[],
        rows=[row("hours", "商店街そのものはいつでも歩けます。店の時間は店ごとに違います", "The arcade itself is always open to walk through; shop hours vary"),
              row("walk", "7ブロック・総延長約900m、約200軒。許可車両以外は24時間 車両通行禁止です", "Seven blocks, about 900 m, some 200 shops. Closed to vehicles around the clock apart from permit holders"),
              row("walk", "二条市場から徒歩約1分、大通公園から徒歩約5分、すすきのから徒歩約3分", "About 1 minute from Nijo Market, 5 from Odori Park, 3 from Susukino"),
              row("pay", "小さな店は現金だけのところがあります", "Smaller shops may take cash only")],
        tip=T("商店街の長さ・店舗数・歴史は公式サイトで確認しました。個別の店の時間は公式に一覧がないので、このマップでは店名を挙げていません。",
              "The arcade’s length, number of shops and history are from its official site. There is no official list of individual shops’ hours, so none are named here."),
        time=(VIS, "13:40〜14:30（お昼。二条市場とどちらか）", "13:40–14:30 (lunch; this or Nijo Market)") if E else (VIS, "13:30〜14:00（寄り道）", "13:30–14:00 (side trip)"),
        photos=W("tanukikoji"))

    S_BEER = dict(
        id="beer", name=T("サッポロビール博物館", "Sapporo Beer Museum"),
        kind=T("博物館・試飲", "Museum & tasting"),
        blurb=T("1890年の製糖工場の赤れんが。日本でいちばん古いビール博物館。", "Red brick from 1890: Japan’s oldest beer museum."),
        caution=T("11:00〜18:00（最終入館17:30）。ガイドツアーは月曜休止", "11:00–18:00 (last entry 17:30); the guided tour does not run on Mondays"),
        lat=43.07187, lng=141.37182,
        body=T(
            "1876年に開拓使が札幌でビールづくりを始めてからの歴史を見せる博物館です。建物は1890年に製糖工場として建った赤れんがで、隣のサッポロビール園 開拓使館とともに北海道遺産になっています。\n\n"
            "見学は2通り。予約なしの「自由見学」は大人1,000円で、3階から1階へ降りながら見る一方通行の順路。所要15〜30分、スマートフォンの音声ガイド（日本語・英語・韓国語・中国語）を聞きながらだと15〜40分。見学のあと1階の Tasting Hall で、工場直送のビールを有料で飲めます（最大30分）。\n\n"
            "もう一つは「試飲付きガイドツアー」（約55分、大人2,000円）。入館料と試飲2杯が含まれ、創業当時の味を復刻した「復刻札幌製麦酒」と現代の黒ラベルを飲み比べます。要予約・日本語のみ・月曜休止です。\n\n"
            "隣のサッポロビール園では、同じ赤れんがの建物でジンギスカン（羊肉の焼き肉）を食べられます。ここで晩ごはんにしてしまう手もありますが、このコースでは藻岩山の夜景に向かいます。",
            "A museum on the brewing that began in Sapporo in 1876 under the Hokkaido Development Commission. The building is red brick, put up in 1890 as a sugar refinery, and together with the neighbouring Sapporo Beer Garten hall it is listed as Hokkaido Heritage.\n\n"
            "There are two ways in. The self-guided visit needs no booking, costs ¥1,000, and follows a one-way route down from the third floor to the first: 15–30 minutes, or 15–40 with the smartphone audio guide (Japanese, English, Korean and Chinese). Afterwards you can buy beer brewed for the site in the ground-floor Tasting Hall, for up to 30 minutes.\n\n"
            "The other is the tasting tour (about 55 minutes, ¥2,000), which includes admission and two beers, comparing a revival of the original 1880s recipe with today’s Black Label. It must be booked, is guided in Japanese only, and does not run on Mondays.\n\n"
            "Next door, the Sapporo Beer Garten serves jingisukan — grilled lamb — in the same red brick. You could make dinner of it, but this course heads on to the night view from Mt. Moiwa."),
        gmaps=[gm("サッポロビール博物館", "Sapporo Beer Museum", 43.07187, 141.37182, "サッポロビール博物館"),
               gm("地下鉄 東区役所前駅", "Higashi-kuyakusho-mae Station", 43.07611, 141.36167, "札幌市営地下鉄 東区役所前駅")],
        links=[link("official", "サッポロビール博物館 公式サイト", "Sapporo Beer Museum official site", U["beer"], U["beer_en"]),
               link("info", "利用案内（自由見学・ガイドツアー）", "Visitor information (self-guided and guided)", U["beer_guide"]),
               link("info", "アクセス", "Getting there", U["beer_access"]),
               link("official", "サッポロビール園（ジンギスカン）", "Sapporo Beer Garten (jingisukan)", U["beerpark"])],
        notices=[N_BEER_TOUR, N_MON],
        rows=[row("hours", "11:00〜18:00（最終入館17:30）、全営業日", "11:00–18:00 (last entry 17:30), every day it is open"),
              row("fee", "自由見学 大人1,000円、中学生〜20歳未満500円、小学生以下無料（道民割 700円／200円）", "Self-guided: adults ¥1,000, ages 13–19 ¥500, primary school and younger free (Hokkaido residents ¥700 / ¥200)"),
              row("fee", "試飲付きガイドツアー 大人2,000円（入館料・試飲2杯つき）、約55分", "Tasting tour: adults ¥2,000 (admission and two beers included), about 55 minutes"),
              row("reserve", "ガイドツアーは要予約（WEBは当日朝9:30まで）。自由見学は予約不要", "The tour must be booked (online up to 9:30 on the day); the self-guided visit needs no booking"),
              row("closed", "ガイドツアーは月曜休止（月曜が祝日のときは翌火曜）", "No tour on Mondays (the following Tuesday instead if Monday is a holiday)"),
              row("train", "大通 13:46 → サッポロビール園 14:08（中央バス、22分・210円）", "Odori 13:46 → Sapporo Beer Garten 14:08 (Chuo Bus, 22 min, ¥210)"),
              row("walk", "地下鉄東豊線「東区役所前」4番出口から徒歩約10分。JR苗穂駅 北口から徒歩約8分", "About 10 minutes from Exit 4 of Higashi-kuyakusho-mae Station (Toho line); 8 minutes from the north exit of JR Naebo Station"),
              row("pay", "キャッシュレス決済が使えます", "Cashless payment accepted")],
        tip=T("時間・料金・ツアーの条件・アクセスは公式サイトで確認しました。バスの時刻は乗換案内（2026年12月3日）です。",
              "Hours, prices, tour conditions and access are from the official site. The bus time is from a route planner for 3 December 2026."),
        time=(VIS, "15:10〜16:15", "15:10–16:15") if E else (VIS, "14:10〜15:15", "14:10–15:15"),
        photos=W("beer"))

    S_MOIWA = dict(
        id="moiwa", name=T("藻岩山（もいわやま）の夜景", "The night view from Mt. Moiwa"),
        kind=T("ロープウェイ・展望台", "Ropeway & observatory"),
        blurb=T("標高531m。街の光が石狩湾まで広がります。", "531 m up, with the city’s lights spreading to the bay."),
        caution=T("冬（12〜3月）は11:00から。12月31日・1月1日は休業", "Winter hours (Dec–Mar) start at 11:00; closed 31 Dec and 1 Jan"),
        lat=43.02333, lng=141.32444,
        body=T(
            "札幌の街のすぐ南にある標高531mの山。ロープウェイで中腹駅まで、そこから「もーりすカー」というミニケーブルカーで山頂駅へ。展望台からは、碁盤の目の光が石狩湾まで広がって見えます。\n\n"
            "公式サイトのトップには、その日の日没と夜景の時刻が出ています（2026年11月29日は日没16:02、夜景16:22）。冬は暗くなるのが早いので、16時台に上がれば夕空と夜景の両方が見られます。山頂は街より風が強く、体感温度がずっと低いので、手袋と帽子を忘れないでください。\n\n"
            "行き方は、地下鉄東西線「円山公園」駅の2番出口の前から JR北海道バス ロープウェイ線［循環円11］で15分・240円。終点の「もいわ山ロープウェイ」はロープウェイ乗り場に直結です。市電の「ロープウェイ入口」から行く方法もありますが、無料シャトルバスが走るのは平日17:17から、土日祝10:17から（冬期10:47から）なので、それより早い時間だと坂を10分登ります。\n\n"
            "料金はロープウェイとミニケーブルカーのセット往復で大人2,100円。ロープウェイだけの往復（中腹駅まで）は1,400円です。山頂にレストラン「ザ ジュエルズ」があり、冬のディナーは17:00〜21:00（LO19:30）。晩ごはんをここにする手もありますが、このコースではすすきのへ下ります。",
            "A 531 m hill immediately south of the city. A ropeway takes you to the mid-station and a little cable car called the Morris Car on to the summit, where the grid of lights spreads out to Ishikari Bay.\n\n"
            "The front page of the official site gives the day’s sunset and “night view” times — on 29 November 2026, 16:02 and 16:22. The dark comes early in winter, so going up in the late afternoon gets you both the evening sky and the night view. The summit is windier than the city and feels far colder, so bring gloves and a hat.\n\n"
            "To get there, take JR Hokkaido Bus “Ropeway Line” (Junkan En 11) from in front of Exit 2 of Maruyama-koen Station on the Tozai subway line: 15 minutes, ¥240, stopping right at the ropeway. You can also take the tram to Ropeway Iriguchi, but the free shuttle from there only runs from 17:17 on weekdays and 10:17 at weekends (10:47 in winter), so earlier than that means a ten-minute walk uphill.\n\n"
            "A return ticket covering both the ropeway and the cable car is ¥2,100 for adults; the ropeway alone, to the mid-station, is ¥1,400. There is a restaurant, The Jewels, at the summit, serving dinner 17:00–21:00 in winter (last orders 19:30). You could eat there, but this course goes back down to Susukino."),
        gmaps=[gm("もいわ山ロープウェイ 山麓駅", "Mt. Moiwa Ropeway base station", 43.03628, 141.33400, "札幌もいわ山ロープウェイ 山麓駅"),
               gm("藻岩山 山頂展望台", "Mt. Moiwa summit observatory", 43.02333, 141.32444, "藻岩山 山頂展望台"),
               gm("地下鉄 円山公園駅", "Maruyama-koen Station", 43.05528, 141.31861, "札幌市営地下鉄 円山公園駅")],
        links=[link("official", "札幌もいわ山ロープウェイ 公式サイト", "Mt. Moiwa Ropeway official site (the site switches language itself)", U["moiwa"]),
               link("info", "営業時間・料金", "Hours and fares", U["moiwa_guide"]),
               link("info", "地下鉄／バスでの行き方", "By subway and bus", U["moiwa_bus"]),
               link("info", "山頂展望台ライブカメラ", "Summit live camera", U["moiwa_cam"])],
        notices=[N_MOIWA_WINTER, N_MOIWA_SHUTTLE, N_MOIWA_WEATHER, N_MOIWA_SHUT],
        rows=[row("hours", "冬（12月〜3月）ロープウェイ 11:00〜22:00（上り最終21:30）、ミニケーブルカー 11:10〜21:50", "Winter (Dec–Mar): ropeway 11:00–22:00 (last up 21:30), cable car 11:10–21:50", until="2027-03-28"),
              row("hours", "夏（4月〜11月）ロープウェイ 10:30〜22:00（上り最終21:30）、ミニケーブルカー 10:30〜21:50", "Summer (Apr–Nov): ropeway 10:30–22:00 (last up 21:30), cable car 10:30–21:50"),
              row("closed", "12月31日・1月1日は休業。2027年3月29日〜4月28日は整備点検で全館休業", "Closed 31 December and 1 January; closed for maintenance 29 March – 28 April 2027"),
              row("fee", "ロープウェイ＋ミニケーブルカー 往復 大人2,100円・小人1,050円。ロープウェイのみ往復 大人1,400円", "Ropeway + cable car return: adults ¥2,100, children ¥1,050. Ropeway only, return: adults ¥1,400"),
              row("bus", "円山公園駅前 16:00 → もいわ山ロープウェイ 16:18（循環円11、240円）。平日は15:10・15:35・15:50・16:55・17:10発も", "Maruyama-koen Station 16:00 → Mt. Moiwa Ropeway 16:18 (Junkan En 11, ¥240); weekdays also 15:10, 15:35, 15:50, 16:55, 17:10"),
              row("bus", "土曜は円山公園駅前 15:00・15:40・15:55・16:10発（所要16分）", "Saturdays: 15:00, 15:40, 15:55 and 16:10 (16 minutes)"),
              row("train", "サッポロビール園から：東区役所前 15:27 → 円山公園 15:49（地下鉄、22分・250円）", "From the Beer Garten: Higashi-kuyakusho-mae 15:27 → Maruyama-koen 15:49 (subway, 22 min, ¥250)"),
              row("train", "帰り：もいわ山ロープウェイ 18:30 → すすきの 19:03（33分・230円）", "Back: Mt. Moiwa Ropeway 18:30 → Susukino 19:03 (33 min, ¥230)"),
              row("pay", "交通系ICカード・クレジットカードが使えます", "Transport IC cards and credit cards accepted")],
        tip=T("営業時間・料金・冬期の変更・休業期間・行き方は公式サイトで確認しました。バスの時刻は乗換案内（2026年12月3日・5日）です。",
              "Hours, fares, the winter change, the maintenance closure and the access are from the official site. Bus times are from a route planner for 3 and 5 December 2026."),
        time=(VIS, "17:20〜18:45", "17:20–18:45") if E else (VIS, "16:35〜18:30（日が暮れたころ）", "16:35–18:30 (just after dark)"),
        photos=W("moiwa"))

    S_SUSUKINO = dict(
        id="susukino", name=T("すすきの（晩ごはん）", "Susukino (dinner)"),
        kind=T("繁華街・晩ごはん", "Nightlife district & dinner"),
        blurb=T("味噌ラーメン、ジンギスカン、海鮮。21時すぎまで。", "Miso ramen, grilled lamb, seafood — well past 21:00."),
        caution=T("現金だけの店があります", "Some places take cash only"),
        lat=43.05533, lng=141.35322,
        body=T(
            "大通の南、南4条から南7条あたりに広がる繁華街です。交差点のニッカウヰスキーの看板が目印で、夜はこの一帯が明るくなります。\n\n"
            "札幌の味噌ラーメンは、この近くの「元祖さっぽろラーメン横丁」（南5条西3丁目）に17軒ほどが並んでいます。路地の幅は人がすれ違うくらいで、どの店も数席から十数席。ジンギスカン（羊肉の焼き肉）、スープカレー、海鮮、北海道の日本酒とワインも、この一帯にそろいます。\n\n"
            "このマップでは個別の店名は挙げていません（公式サイトで時間を確かめられた店だけを載せる方針で、横丁の多くの店に公式サイトがないため）。横丁は入口から見て、空いている店に入るのがふつうです。\n\n"
            "地下鉄南北線「すすきの」駅から札幌駅までは11分・210円、終電は0時すぎまであります。大通までは歩いて10分ほど。冬は地下街を通って帰れます。\n\n"
            "2月4日〜11日の雪まつりのときは、駅前通に氷像が並ぶ「すすきの会場」になり、とても混みます。",
            "The nightlife district spreads south of Odori, roughly between Minami 4-jo and Minami 7-jo. The Nikka whisky sign at the crossing is the landmark, and the whole area lights up after dark.\n\n"
            "Sapporo’s miso ramen has its own lane here: Ganso Sapporo Ramen Yokocho at Minami 5-jo Nishi 3-chome, with some seventeen shops. The alley is barely wide enough for two people to pass, and each shop seats a handful. Jingisukan (grilled lamb), soup curry, seafood and Hokkaido sake and wine are all in these blocks.\n\n"
            "No individual restaurants are named on this map: it only names places whose hours could be checked on an official site, and most of the shops in the alley have none. In the alley, people simply look in and take whichever shop has a seat.\n\n"
            "From Susukino station on the Namboku subway line, Sapporo Station is 11 minutes and ¥210, with the last trains after midnight. Odori is about a ten-minute walk, or underground in winter.\n\n"
            "During the Snow Festival, 4–11 February, the Ekimae-dori avenue here becomes the Susukino site, lined with ice sculptures, and gets very crowded."),
        gmaps=[gm("すすきの交差点", "Susukino crossing", 43.05533, 141.35322, "すすきの交差点"),
               gm("元祖さっぽろラーメン横丁", "Ganso Sapporo Ramen Yokocho", 43.05472, 141.35250, "元祖さっぽろラーメン横丁")],
        links=[L_SUBWAY, link("info", "さっぽろ雪まつり すすきの会場", "Snow Festival, Susukino site", U["snowfes"])],
        notices=[N_SNOWFES, N_IC],
        rows=[row("train", "すすきの 21:36 → 札幌 21:47（地下鉄南北線、11分・210円）", "Susukino 21:36 → Sapporo 21:47 (Namboku line, 11 min, ¥210)"),
              row("walk", "大通まで徒歩約10分（冬は地下街が使えます）", "About 10 minutes’ walk to Odori, or underground in winter"),
              row("pay", "横丁の小さな店は現金だけのことがあります", "The small shops in the alley may take cash only"),
              row("season", "すすきの会場（氷像）2027年2月4日〜11日", "Susukino site (ice sculptures): 4–11 February 2027", until="2027-02-11")],
        tip=T("地下鉄の時刻と運賃は乗換案内（2026年12月3日）、雪まつりの日程は公式サイトで確認しました。店の時間はそれぞれの店で確かめてください。",
              "Subway times and fares are from a route planner for 3 December 2026 and the Snow Festival dates from its official site. Check individual restaurants’ hours yourself."),
        time=((DEP, "19:20〜21:30", "19:20–21:30") if E else
              (DEP, "18:30〜21:00", "18:30–21:00") if c == "maruyama" else (DEP, "19:05〜21:00", "19:05–21:00")),
        photos=W("susukino"))

    S_JINGU = dict(
        id="jingu", name=T("北海道神宮（ほっかいどうじんぐう）・円山公園", "Hokkaido Jingu shrine & Maruyama Park"),
        kind=T("神社・公園", "Shrine & park"),
        blurb=T("円山のふもとの森の中。春は桜の名所。", "In the woods at the foot of Mt. Maruyama; famous for cherry blossom."),
        caution=T("開門・閉門の時刻は月ごとに変わります（公式サイトのお知らせ）", "The gate times change every month: see the shrine’s notices"),
        lat=43.05430, lng=141.30736,
        body=T(
            "1869年に開拓の守り神としてまつられた神社で、円山（まるやま）のふもとの森の中にあります。地下鉄東西線「円山公園」駅から、円山公園の木立を抜けて歩いて15分ほど。\n\n"
            "鳥居をくぐると参道が森の中をまっすぐ伸びていて、冬は雪をかぶった杉が続きます。境内には約1,400本の桜と梅があり、4月末から5月初めに同時に咲きます（札幌の桜はゴールデンウィークごろ）。\n\n"
            "隣の円山公園は、円山原始林に続く森の公園です。円山そのものは標高225mで、登山道を40分ほどで登れます。エゾリスが見られることもあります。\n\n"
            "開門と閉門の時刻は月ごとに変わります。公式サイトのお知らせに「閉門時間変更のお知らせ（◯月◯日〜）」が毎月のように出る仕組みで、決まった時刻表はありません。朝から夕方までが基本ですが、行く前にお知らせを見てください。公式サイトに拝観料の記載はなく、境内に入るのに料金はかかりません。",
            "A shrine founded in 1869 to watch over the settlement of Hokkaido, set in the woods at the foot of Mt. Maruyama. It is about fifteen minutes’ walk from Maruyama-koen subway station (Tozai line), through the trees of Maruyama Park.\n\n"
            "Past the torii gate, the approach runs straight through the forest, lined in winter with snow-laden cedars. The grounds hold some 1,400 cherry and plum trees, which bloom together in late April and early May — Sapporo’s cherry blossom comes around the start of May.\n\n"
            "Maruyama Park next door is a wooded park running into the old-growth forest of Mt. Maruyama. The hill itself is 225 m high and takes about forty minutes to climb; you may meet Hokkaido squirrels on the way.\n\n"
            "The gates open and close at different times through the year: the shrine posts a “closing time change” notice almost every month and publishes no fixed timetable. Broadly it is morning to late afternoon, but check the notices before you go. The site lists no admission fee; there is no charge to enter the grounds."),
        gmaps=[gm("北海道神宮", "Hokkaido Jingu", 43.05430, 141.30736, "北海道神宮"),
               gm("円山公園", "Maruyama Park", 43.05389, 141.31306, "円山公園 札幌"),
               gm("地下鉄 円山公園駅", "Maruyama-koen Station", 43.05528, 141.31861, "札幌市営地下鉄 円山公園駅")],
        links=[link("official", "北海道神宮 公式サイト（お知らせに開閉門時間）", "Hokkaido Jingu official site (gate times are in the notices)", U["jingu"])],
        notices=[N_WINTER],
        rows=[row("fee", "公式サイトに拝観料の記載はありません（境内に入るのに料金はかかりません）", "The official site lists no admission fee; there is no charge to enter the grounds"),
              row("hours", "開門・閉門の時刻は月ごとに変わります。決まった時刻表はなく、公式サイトのお知らせで出ます（要確認）", "The gate times change every month; there is no fixed timetable, only the notices on the shrine’s website (please check)"),
              row("walk", "地下鉄東西線「円山公園」駅から徒歩約15分（円山公園を抜けます）", "About 15 minutes’ walk from Maruyama-koen Station, through Maruyama Park"),
              row("season", "桜と梅は4月末〜5月初め", "Cherry and plum blossom: late April to early May")],
        tip=T("公式サイトのお知らせの一覧を見ると、閉門時間は月ごとに変わっていて、決まった時刻表は出ていません（要確認）。行く日の時刻は公式サイトのお知らせで確かめてください。参拝が無料であることと場所は、札幌市の観光サイトで確かめています。",
              "The notice list on the shrine’s website shows the closing time changing month by month, with no fixed timetable published (so please check). Look up the times for your date in those notices. That it is free to visit, and its location, are confirmed on the city’s tourism site."),
        time=(VIS, "9:55〜10:50", "9:55–10:50"),
        verified=False, photos=W("jingu"))

    S_ZOO = dict(
        id="zoo", name=T("札幌市円山動物園（まるやまどうぶつえん）", "Sapporo Maruyama Zoo"),
        kind=T("動物園", "Zoo"),
        blurb=T("レッサーパンダもオオカミも、雪の日がいちばん元気。", "Red pandas and wolves are at their liveliest in the snow."),
        caution=T("第2・第4水曜は休園。冬（11〜2月）は16:00閉園", "Closed on the 2nd and 4th Wednesday; winter closing is 16:00"),
        lat=43.05333, lng=141.30278,
        body=T(
            "1951年に開いた、北海道神宮の隣の森の中の動物園です。ホッキョクグマ館は水中が見えるトンネルがあり、ゾウ舎は屋内のプールでゾウが泳ぐところを見られます。ユキヒョウ、レッサーパンダ、エゾシカやエゾヒグマなど北海道の動物も揃っています。\n\n"
            "冬が見どころの動物園です。雪が降るとホッキョクグマもユキヒョウも元気に動きます。ただし冬期（11月1日〜2月末）は9:30〜16:00で、最終入園は15:30。3月からは16:30まで（最終入園16:00）。\n\n"
            "休園日に気をつけてください。毎月第2・第4水曜日が休み（祝日のときは翌日）、11月と4月は第2水曜を含むその週の月〜金が休み、12月29日〜31日も休園です。\n\n"
            "入園料は大人800円、中学生以下は無料。園内に食堂があるので、お昼はここで。坂のある園内なので、冬は滑りにくい靴で。北海道神宮からは歩いて10分ほどです。",
            "A zoo in the woods next to Hokkaido Jingu, opened in 1951. The polar bear house has an underwater tunnel, and the elephant house lets you watch the elephants swim in an indoor pool. Snow leopards, red pandas, and Hokkaido animals such as sika deer and brown bears are all here.\n\n"
            "Winter is the season. When snow falls, the polar bears and snow leopards come alive. But from 1 November to the end of February the zoo is open only 9:30–16:00, with last entry at 15:30; from March it closes at 16:30 (last entry 16:00).\n\n"
            "Watch the closing days: the second and fourth Wednesday of each month (the next day if that is a holiday), the whole Monday-to-Friday week containing the second Wednesday in November and April, and 29–31 December.\n\n"
            "Admission is ¥800 for adults and free for junior high school students and younger. There are restaurants inside, so have lunch here. The grounds are hilly, so wear shoes that grip in winter. It is about ten minutes’ walk from Hokkaido Jingu."),
        gmaps=[gm("円山動物園 正門", "Maruyama Zoo Main Gate", 43.05333, 141.30278, "札幌市円山動物園 正門")],
        links=[link("official", "札幌市円山動物園 公式サイト", "Sapporo Maruyama Zoo official site", U["zoo"]),
               link("info", "開園時間・休園日", "Hours and closing days", U["zoo_time"]),
               link("info", "入園料について", "Admission", U["zoo_fee"])],
        notices=[N_ZOO_WINTER, N_ZOO_CLOSED, N_WINTER],
        rows=[row("hours", "冬期（11月1日〜2月末日）9:30〜16:00（最終入園15:30）", "Winter (1 Nov – end of Feb): 9:30–16:00 (last entry 15:30)", until="2027-02-28"),
              row("hours", "夏期（3月1日〜10月31日）9:30〜16:30（最終入園16:00）", "Summer (1 Mar – 31 Oct): 9:30–16:30 (last entry 16:00)"),
              row("closed", "毎月第2・第4水曜日（祝日の場合は翌日）、11月と4月は第2水曜を含む週の月〜金、12月29日〜31日", "2nd and 4th Wednesday each month (next day if a holiday); the Mon–Fri week with the 2nd Wednesday in November and April; 29–31 December"),
              row("fee", "大人800円、高校生400円（学生証が必要）、中学生以下無料。年間パスポート2,000円", "Adults ¥800, high school students ¥400 with ID, junior high and younger free; annual pass ¥2,000"),
              row("pay", "電子チケットがあります（2026年3月から）", "Electronic tickets are available (since March 2026)"),
              row("walk", "北海道神宮から徒歩約10分。地下鉄東西線「円山公園」駅から徒歩約15分", "About 10 minutes’ walk from Hokkaido Jingu, 15 from Maruyama-koen Station")],
        tip=T("開園時間・休園日・入園料は札幌市の公式ページで確認しました。動物の展示は入れ替わることがあるので、見たい動物がいる人は公式サイトで確かめてください。",
              "Hours, closing days and admission are from the city’s official pages. Which animals are on show changes, so check the site if there is one you particularly want to see."),
        time=(VIS, "11:00〜13:40（園内でお昼）", "11:00–13:40 (lunch inside)"),
        photos=W("zoo"))

    S_SHIROI = dict(
        id="shiroi", name=T("白い恋人パーク", "Shiroi Koibito Park"),
        kind=T("お菓子の工場・庭", "Chocolate factory & gardens"),
        blurb=T("地下鉄で15分。冬は16:00からイルミネーション。", "Fifteen minutes by subway; lit from 16:00 in winter."),
        caution=T("有料エリアの受付は16:30まで", "The ticket desk for the paid area closes at 16:30"),
        lat=43.08789, lng=141.26575,
        body=T(
            "北海道の土産でよく知られたクッキー「白い恋人」を作る石屋製菓が、工場のまわりに作った施設です。地下鉄東西線の終点「宮の沢」駅の出口1から歩いて7分。\n\n"
            "外のエリア（中庭のローズガーデン、からくり時計塔）は無料で、有料エリア（大人1,200円）では工場の製造ラインを見学路から見られます。お菓子づくり体験もあります。\n\n"
            "2026年12月1日から2027年3月31日は「スイートイルミネーション」の期間で、パークの営業が10:00〜19:00、点灯は16:00〜19:00。イルミネーションは無料のエリアで見られます。英国風の建物とレンガの街並みが雪と光に包まれるのが、この時期の見どころです。\n\n"
            "有料エリアは時間が別で、チケットセンターの受付が16:30まで、工場などは17:30まで。14:20ごろに着いて、先に有料エリア、暗くなったら外のイルミネーション、という順番になります。年中無休です。",
            "Ishiya, the maker of the Shiroi Koibito cookies that are Hokkaido’s best-known souvenir, built this around its factory. It is a seven-minute walk from Exit 1 of Miyanosawa, the western terminus of the Tozai subway line.\n\n"
            "The outdoor part — the rose garden courtyard and the chiming clock tower — is free; in the paid area (¥1,200 for adults) a walkway looks down on the production lines. There are sweet-making workshops too.\n\n"
            "From 1 December 2026 to 31 March 2027 the Sweet Illumination is on: the park is open 10:00–19:00 and the lights are on from 16:00 to 19:00, in the free part of the park. The point of the season is the English-style buildings and brick streets under snow and lights.\n\n"
            "The paid area keeps different hours: the ticket desk closes at 16:30 and the factory at 17:30. Arriving at about 14:20, do the paid area first and step out for the lights once it is dark. Open every day of the year."),
        gmaps=[gm("白い恋人パーク", "Shiroi Koibito Park", 43.08789, 141.26575, "白い恋人パーク"),
               gm("地下鉄 宮の沢駅", "Miyanosawa Station", 43.08528, 141.27167, "札幌市営地下鉄 宮の沢駅")],
        links=[link("official", "白い恋人パーク 公式サイト", "Shiroi Koibito Park official site", U["shiroi"], U["shiroi_en"]),
               link("info", "スイートイルミネーション", "Sweet Illumination", U["shiroi_illum"]),
               link("info", "アクセス", "Getting there", U["shiroi_access"])],
        notices=[N_SHIROI_ILLUM, N_WINTER],
        rows=[row("hours", "イルミネーション期間（2026年12月1日〜2027年3月31日）10:00〜19:00、点灯16:00〜19:00", "Illumination season (1 Dec 2026 – 31 Mar 2027): 10:00–19:00, lit 16:00–19:00", until="2027-03-31"),
              row("hours", "有料エリア：チケットセンター受付10:00〜16:30、工場など10:00〜17:30、チュダーハウス10:00〜18:30", "Paid area: ticket desk 10:00–16:30, factory 10:00–17:30, Tudor House 10:00–18:30", until="2027-03-31"),
              row("fee", "有料エリア 大人（16歳以上）1,200円、3歳以下無料。イルミネーションと中庭は無料", "Paid area: adults (16+) ¥1,200, under-4s free. The illumination and courtyard are free"),
              row("closed", "年中無休", "Open every day"),
              row("train", "円山公園 14:04 → 宮の沢 14:15（地下鉄東西線、11分・250円）", "Maruyama-koen 14:04 → Miyanosawa 14:15 (Tozai line, 11 min, ¥250)"),
              row("walk", "宮の沢駅 出口1から徒歩約7分", "About 7 minutes’ walk from Exit 1 of Miyanosawa Station"),
              row("train", "帰り：宮の沢 16:42 → 大通 16:58（16分・290円）", "Back: Miyanosawa 16:42 → Odori 16:58 (16 min, ¥290)")],
        tip=T("イルミネーションの期間と時間、有料エリアの時間と料金は公式サイトで確認しました。地下鉄の時刻は乗換案内（2026年12月3日）です。",
              "The illumination dates and times and the paid area’s hours and prices are from the official site. Subway times are from a route planner for 3 December 2026."),
        time=(VIS, "14:22〜16:40（点灯は16:00）", "14:22–16:40 (lights on at 16:00)"),
        photos=W("shiroi"))

    S_MOERE = dict(
        id="moerenuma", name=T("モエレ沼公園", "Moerenuma Park"),
        kind=T("公園・ガラスのピラミッド", "Park & the Glass Pyramid"),
        blurb=T("イサム・ノグチが設計した公園。冬は一面の雪原。", "A park designed by Isamu Noguchi; a field of snow in winter."),
        caution=T("ガラスのピラミッドは月曜休館。冬は噴水が止まります", "The Glass Pyramid closes on Mondays; the fountain stops in winter"),
        lat=43.14380, lng=141.39500,
        body=T(
            "彫刻家イサム・ノグチが「公園全体を一つの彫刻作品に」と設計した、札幌の北東にある大きな公園です。ゴミ処理場だった土地を造り替えたもので、ノグチが1988年に亡くなったあと、計画どおりに2005年に完成しました。\n\n"
            "ガラスのピラミッド「HIDAMARI」（9:00〜17:00、月曜休館）、人工の山「モエレ山」（標高62m）、「海の噴水」、三角形のプレイマウンテンなどが広い敷地に置かれています。\n\n"
            "冬は一面の雪原になり、モエレ山をそりやスノーシューで登る人がいます。用品のレンタルは2027年1月5日〜3月7日の10:00〜16:00（月曜休）。「海の噴水」は2026年度の運転を終えていて、冬は動きません。\n\n"
            "行き方は、地下鉄東豊線「環状通東」駅から中央バス【東69】「あいの里教育大駅」行き、または【東69・東79】「中沼小学校通」行きで「モエレ沼公園東口」下車。街なかから片道50分ほどかかるので、白い恋人パークとどちらか一方にしてください。",
            "A large park in the north-east of Sapporo, designed by the sculptor Isamu Noguchi on the principle that the whole park would be a single sculpture. Built over a former waste site, it was completed in 2005 to his plan, seventeen years after his death in 1988.\n\n"
            "Spread across the grounds are the Glass Pyramid “Hidamari” (9:00–17:00, closed Mondays), the man-made hill Moere-yama (62 m), the Sea Fountain and the triangular Play Mountain.\n\n"
            "In winter it becomes a field of snow, and people climb Moere-yama with sledges or snowshoes; equipment rental runs 5 January – 7 March 2027, 10:00–16:00, closed Mondays. The Sea Fountain has finished its season and does not run in winter.\n\n"
            "To get there, take a Chuo Bus from Kanjo-dori-higashi Station on the Toho subway line — route 69 towards Ainosato Kyoikudai, or routes 69 and 79 towards Nakanuma Shogakko-dori — and get off at Moerenuma Park East Gate. It is about fifty minutes each way from the centre, so choose between this and Shiroi Koibito Park rather than doing both."),
        gmaps=[gm("ガラスのピラミッド", "Glass Pyramid", 43.14380, 141.39500, "モエレ沼公園 ガラスのピラミッド"),
               gm("モエレ山", "Moere-yama", 43.14028, 141.39028, "モエレ山")],
        links=[link("official", "モエレ沼公園 公式サイト", "Moerenuma Park official site", U["moere"]),
               link("info", "アクセス", "Getting there", U["moere_access"])],
        notices=[N_MOERE_MON, N_WINTER],
        rows=[row("hours", "公園 7:00〜22:00（東口ゲートからの入園は21:00まで）。ガラスのピラミッド 9:00〜17:00", "Park 7:00–22:00 (last entry through the East Gate 21:00); Glass Pyramid 9:00–17:00"),
              row("closed", "ガラスのピラミッドは毎週月曜日休館", "The Glass Pyramid is closed on Mondays"),
              row("fee", "公式サイトに入園料・入館料の記載はありません（公園もガラスのピラミッドも料金なしで入れます）", "The official site lists no admission charge for either the park or the Glass Pyramid"),
              row("bus", "地下鉄東豊線「環状通東」駅から中央バス【東69】【東79】で「モエレ沼公園東口」下車", "From Kanjo-dori-higashi Station (Toho line), Chuo Bus routes 69 or 79 to Moerenuma Park East Gate"),
              row("season", "海の噴水は冬は止まります。そり・スノーシューのレンタルは2027年1月5日〜3月7日", "The Sea Fountain stops in winter; sledge and snowshoe rental runs 5 Jan – 7 Mar 2027")],
        tip=T("公園と各施設の時間・休館日・アクセスは公式サイトで確認しました。街なかからの所要時間は目安です（乗換案内でバス停の時刻が出ませんでした）。",
              "The park’s and the buildings’ hours, closing days and access are from the official site. The travel time from the centre is an estimate: the route planner did not return times for the bus stop."),
        time=(VIS, "14:20〜16:20（白い恋人パークの代わりに）", "14:20–16:20 (instead of Shiroi Koibito Park)"),
        verified=False, photos=W("moerenuma"))

    if c == "teiban":
        return [S_EKI, S_AKARENGA, S_TOKEIDAI, S_ODORI, S_SHIRYOKAN, S_NIJO, S_TANUKI, S_BEER, S_MOIWA, S_SUSUKINO]
    if c == "early":
        return [S_EKI, S_JOGAI, S_HOKUDAI, S_AKARENGA, S_TOKEIDAI, S_ODORI, S_NIJO, S_TANUKI, S_BEER, S_MOIWA, S_SUSUKINO]
    return [S_EKI, S_JINGU, S_ZOO, S_SHIROI, S_MOERE, S_ODORI, S_SUSUKINO]


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
    info = {"rows": b["rows"], "cash": False, "tip": b["tip"], "checked": CHECKED}
    if b.get("verified") is False:
        info["verified"] = False
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"], links=b["links"], notices=b["notices"],
               info=info, photos=b["photos"])
    assert out["photos"], b["id"]
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


def build(c):
    S = spots(c)
    N = {s["id"]: i for i, s in enumerate(S, 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}

    if c == "teiban":
        default = ns("akarenga", "tokeidai", "odori", "nijo", "beer", "moiwa")
        hints = [
            h("shiryokan", {"any": ns("shiryokan")},
              "資料館を入れた日は、テレビ塔のあと大通公園を西の端まで歩きます（約20分）。帰りは地下鉄東西線「西11丁目」から1駅で大通へ。二条市場のお昼が13:00ごろになります。",
              "With the Archive Museum, walk the length of Odori Park west after the TV Tower (about 20 minutes) and come back one stop on the subway from Nishi 11-chome. Lunch at Nijo Market then falls at about 13:00."),
            h("tanukikoji", {"any": ns("tanukikoji"), "andAny": ns("shiryokan")},
              "資料館と狸小路の両方を入れると、ビール博物館に着くのが15時すぎになります。博物館は11:00〜18:00（最終入館17:30）なので間に合いますが、試飲の時間は短めに。",
              "With both the Archive Museum and Tanukikoji you reach the Beer Museum after 15:00. It is open until 18:00 (last entry 17:30), so that still works, but keep the tasting short."),
            h("beer", {"none": ns("beer")},
              "ビール博物館に行かない日は、午後に時間ができます。狸小路と大通公園をゆっくり歩いて、15:30ごろに円山公園駅へ。藻岩山に早く上がれば、夕空から夜景まで見られます。",
              "Without the Beer Museum the afternoon opens up: take Tanukikoji and Odori Park slowly and head for Maruyama-koen Station at about 15:30. Going up Mt. Moiwa earlier gets you the evening sky as well as the night view."),
            h("moiwa", {"none": ns("moiwa")},
              "藻岩山に行かない日は、夜景はテレビ塔の展望台（22:00まで、大人1,200円）で。冬は赤れんが庁舎のライトアップ（21:00まで）と大通公園のイルミネーションも夜の見どころです。",
              "Without Mt. Moiwa, see the city from the TV Tower observatory instead (open to 22:00, ¥1,200). In winter the floodlit Red Brick Office (open to 21:00) and the Odori illumination are the other evening sights."),
            h("akarenga", {"none": ns("akarenga", "tokeidai")},
              "赤れんが庁舎も時計台も入れない日は、朝に余裕ができます。大通公園からテレビ塔に上がって、二条市場でゆっくり朝ごはんにする回り方もできます。",
              "With neither the Red Brick Office nor the Clock Tower, the morning is easy: go up the TV Tower from Odori Park and have a slow breakfast at Nijo Market instead."),
        ]
        sections = [
            {"first": 1, "last": 4, "area": T("街の真ん中（午前）", "City centre · morning"),
             "title": T("赤れんが庁舎と時計台、大通公園のテレビ塔", "The Red Brick Office, the Clock Tower and the TV Tower")},
            {"first": 5, "last": 7, "area": T("お昼（大通から東へ）", "Lunch · east of Odori"),
             "title": T("資料館に寄って、二条市場で海鮮、狸小路", "A stop at the Archive Museum, seafood at Nijo Market, then Tanukikoji")},
            {"first": 8, "last": 10, "area": T("午後と夜", "Afternoon & evening"),
             "title": T("ビール博物館、藻岩山の夜景、すすきの", "The Beer Museum, the night view from Mt. Moiwa, and Susukino")},
        ]
        focus = {"first": 1, "last": 7}
        note = ("定番（9:15にホテルを出る）。赤れんが庁舎→時計台→大通公園・テレビ塔→二条市場でお昼→サッポロビール博物館→藻岩山の夜景→すすきの。"
                "札幌市資料館と狸小路は選んだ日だけ。")
    elif c == "early":
        default = ns("jogai", "hokudai", "akarenga", "tokeidai", "odori", "tanukikoji", "beer", "moiwa")
        hints = [
            h("nijo", {"any": ns("nijo"), "andAny": ns("jogai")},
              "朝に場外市場、昼に二条市場だと、海鮮が2回続きます。二条市場は通り抜けるだけにして、お昼は狸小路のラーメンかスープカレーにする手もあります。",
              "The Curb Market in the morning and Nijo Market at midday means seafood twice. You could just walk through Nijo Market and have ramen or soup curry in Tanukikoji instead."),
            h("hokudai", {"none": ns("hokudai")},
              "北大に行かない日は、7:00に出る必要がありません。9:15に出る「定番」のコースのほうが向いています（上のボタンで切り替えられます）。",
              "Without the university there is no need to leave at 07:00: the 9:15 “classic” course suits you better (switch with the buttons above)."),
            h("jogai", {"none": ns("jogai")},
              "場外市場に行かない日は、北大の構内を朝8時から歩けます。雪の朝の構内は人が少なく、ポプラ並木まで静かです。博物館は10:00開館です。",
              "Without the Curb Market you can be walking the university campus from 08:00. On a snowy morning it is almost empty all the way to the poplar avenue; the museum opens at 10:00."),
            h("beer", {"any": ns("beer")},
              "朝が早い日は、ビール博物館が15:00ごろになります。試飲付きガイドツアー（要予約・月曜休止）に入りたい人は、予約の時間を15:00以降にしてください。",
              "On this early day you reach the Beer Museum at about 15:00. If you want the tasting tour (booking required, no Mondays), book a time from 15:00 on."),
            h("moiwa", {"any": ns("moiwa")},
              "藻岩山は冬（12月〜3月）は11:00から、上りの最終は21:30。17:00に上がれば、夜景をゆっくり見てから19:20ごろすすきのに着きます。",
              "Mt. Moiwa opens at 11:00 in winter (December to March), with the last ride up at 21:30. Go up at 17:00 and you can take your time before reaching Susukino at about 19:20."),
        ]
        sections = [
            {"first": 1, "last": 3, "area": T("朝（市場と北大）", "Morning · market & university"),
             "title": T("6時から開く市場で朝ごはん、雪のキャンパス", "Breakfast at a market open from 06:00, then a snowy campus")},
            {"first": 4, "last": 6, "area": T("街の真ん中（昼前）", "City centre · late morning"),
             "title": T("赤れんが庁舎、時計台、テレビ塔の展望台", "The Red Brick Office, the Clock Tower and the TV Tower")},
            {"first": 7, "last": 11, "area": T("午後と夜", "Afternoon & evening"),
             "title": T("狸小路でお昼、ビール博物館、藻岩山、すすきの", "Lunch in Tanukikoji, the Beer Museum, Mt. Moiwa and Susukino")},
        ]
        focus = {"first": 1, "last": 8}
        note = ("朝いちばん（7:00にホテルを出る）。場外市場で朝ごはん→北海道大学→赤れんが庁舎→時計台→大通公園・テレビ塔→狸小路でお昼→"
                "サッポロビール博物館→藻岩山の夜景→すすきの。二条市場は選んだ日だけ。")
    else:
        default = ns("jingu", "zoo", "shiroi", "odori")
        hints = [
            h("moerenuma", {"any": ns("moerenuma"), "andAny": ns("shiroi")},
              "白い恋人パーク（西）とモエレ沼公園（北東）は街の反対側です。両方に行くと移動だけで2時間以上かかるので、どちらか1つにしてください。",
              "Shiroi Koibito Park is in the west and Moerenuma Park in the north-east. Doing both means more than two hours of travelling, so choose one."),
            h("moerenuma", {"any": ns("moerenuma"), "none": ns("shiroi")},
              "モエレ沼公園を選んだ日は、動物園を13:00に出て、円山公園→大通→環状通東と地下鉄を乗り継いで、バスで14:20ごろ。ガラスのピラミッドは17:00まで（月曜休館）。帰りも50分かかるので、大通に戻るのは17:30ごろです。",
              "With Moerenuma Park, leave the zoo at 13:00, ride the subway from Maruyama-koen through Odori to Kanjo-dori-higashi and catch the bus to arrive at about 14:20. The Glass Pyramid closes at 17:00 (shut on Mondays). The way back also takes fifty minutes, so you are at Odori at about 17:30."),
            h("zoo", {"none": ns("zoo")},
              "動物園に行かない日は、円山を歩いて登れます（標高225m、片道約40分）。北海道神宮から登山道に入って、昼に下りてきて、午後は白い恋人パークへ。",
              "Without the zoo you can climb Mt. Maruyama itself (225 m, about 40 minutes each way): take the trail from Hokkaido Jingu, come down around midday and go on to Shiroi Koibito Park in the afternoon."),
            h("shiroi", {"none": ns("shiroi", "moerenuma")},
              "午後の行き先を入れない日は、動物園を出たあと円山のカフェや裏参道を歩いて、夕方に大通公園のイルミネーションへ。無理のない1日になります。",
              "With no afternoon trip, walk the cafés and back streets of Maruyama after the zoo and head for the Odori illumination in the evening. An easy day."),
            h("odori", {"none": ns("odori")},
              "大通公園に戻らない日は、円山から地下鉄でそのまますすきのへ（円山公園→大通→すすきの、約10分）。晩ごはんのあとに大通のイルミネーションを見に歩くこともできます。",
              "If you skip Odori Park, ride straight from Maruyama to Susukino (Maruyama-koen → Odori → Susukino, about 10 minutes). You can always walk up to the Odori lights after dinner."),
        ]
        sections = [
            {"first": 1, "last": 3, "area": T("円山（午前）", "Maruyama · morning"),
             "title": T("森の中の神宮と、雪の動物園", "A shrine in the woods and a zoo in the snow")},
            {"first": 4, "last": 5, "area": T("午後に1つ", "One for the afternoon"),
             "title": T("白い恋人パークか、モエレ沼公園", "Shiroi Koibito Park, or Moerenuma Park")},
            {"first": 6, "last": 7, "area": T("夜", "Evening"),
             "title": T("大通公園のイルミネーションと、すすきの", "The Odori illumination, and Susukino")},
        ]
        focus = {"first": 1, "last": 4}
        note = ("もう1日あるなら（9:15にホテルを出る）。北海道神宮・円山公園→円山動物園→白い恋人パーク→大通公園の夜→すすきの。"
                "モエレ沼公園は白い恋人パークの代わりに選ぶ場所。")

    data = {
        "id": "sapporo", "course": {"teiban": "late", "early": "early", "maruyama": "maruyama"}[c],
        "_note": "札幌市内で1日（sapporo/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "写真はすべて Wikimedia Commons（一覧は scripts/sapporo_web_photos.json）。info.checked と sources.checked は確認した日、"
                   "sources.saw はそのページで見た内容、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。"
                   "このファイルは scripts/build_sapporo_data.py で作る（直接直さない）。",
        "sections": sections,
        "focus": focus,
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。出発の駅と、晩ごはんのすすきのはいつも入る。",
                 "defaultMode": "pick",
                 "picks": [N[s["id"]] for s in S if s["id"] not in ("eki", "susukino")],
                 "defaultPicks": default,
                 "auto": {str(N["eki"]): {"always": True}, str(N["susukino"]): {"always": True}},
                 "hints": hints},
        "photoBase": "../images/sapporo/", "sources": SOURCES,
        "spots": [spot(i, s) for i, s in enumerate(S, 1)],
    }
    name = {"teiban": "sapporo.json", "early": "sapporo-early.json", "maruyama": "sapporo-maruyama.json"}[c]
    with open(f"{R}/data/routes/{name}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", name, [(s["no"], s["id"], len(s["photos"])) for s in data["spots"]])


build("teiban")
build("early")
build("maruyama")
