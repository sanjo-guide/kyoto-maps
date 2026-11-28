#!/usr/bin/env python3
"""旭山動物園と旭川の町（旭川駅のまわりのホテルから1日）のデータを書き出す。コースは季節で2つ。

使い方: python3 scripts/build_asahikawa_data.py   （そのあと python3 scripts/sync_asahikawa.py）
- data/routes/asahikawa-winter.json … 冬（動物園の冬期開園 11/11〜4/7、10:30〜15:30）
    旭川駅9:40のバス→旭山動物園（11:00のペンギンの散歩）→14:10のバスで戻る→髙砂酒造→買物公園でラーメン→5・7小路ふらりーと
- data/routes/asahikawa.json … 雪のない季節（夏期開園 4/29〜11/3、9:30〜17:15。10/16からは16:30まで）
    旭川駅9:10のバス→旭山動物園→13:40のバスで戻る→男山→買物公園→常磐公園と旭橋の夕方→5・7小路ふらりーと
  スポットは9か所で、番号は2つのコースで同じ。どちらも最初から「選んで回る」で、時間割どおりの場所が選ばれている（defaultPicks）。
  コースを分けたのは、動物園の開園時間が冬と夏で大きく違い（冬は5時間だけ）、冬は16時ごろに日が暮れるため。
  早朝のコースは作っていない（開園が冬10:30・夏9:30で、9時台に出れば開園に合う）
- 起点は旭川駅のまわりのホテル。札幌から日帰りの人向けの特急の時刻は1番と9番に補足
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 動物園のバスは旭川電気軌道の公式の時刻表（冬：2026年11月11日〜2027年4月7日。夏：2026年4月29日〜11月3日の時刻表＝2027年の分は未発表）。
  男山へのバス（道北バス）と JR は乗換案内の2026年12月3日（木）・5日（土）。JR北海道は2027年3月にダイヤ改正があるはず
- 動物園の入園料は2027年4月29日から1,400円（rows の until / from で自動で切り替わる）
- 写真はすべて Wikimedia Commons（オーナーはまだ北海道の写真を持っていない）。一覧とクレジットは scripts/asahikawa_web_photos.json。
  オーナーの写真はあとで images/asahikawa/<スポットのid>-<番号>.jpg として足す（ネットの写真は -w<番号>）
- 行っていない場所なので文章は中立に。店名は、公式サイトで時間を確かめた店だけ（梅光軒 旭川本店・らーめん山頭火 旭川本店・焼鳥専門ぎんねこ）
- 入れなかったもの：雪の美術館（公式サイトが開けず、営業を確かめられなかった）、大雪地ビール館（公式サイトに営業時間が見つからなかった）、
  あさひかわラーメン村（駅から遠い）。美瑛・青い池・富良野は biei、旭岳・層雲峡は daisetsuzan のマップ
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/asahikawa"
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


WEB = json.load(open(f"{R}/scripts/asahikawa_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]

ZOO = "https://www.city.asahikawa.hokkaido.jp/asahiyamazoo/"
BUSSTOP = "１条８丁目・１条７丁目/道北バス"
U = dict(
    zoo=ZOO, zoo_cal=ZOO + "event/event.html", zoo_fee=ZOO + "generalinformation/d052849.html",
    zoo_access=ZOO + "generalinformation/d053767.html", zoo_rules=ZOO + "generalinformation/d053773.html",
    zoo_food=ZOO + "generalinformation/p008636.html",
    zoo_winter=ZOO + "news-blog/osirase/d082799.html", zoo_newfee=ZOO + "news-blog/osirase/d084291.html",
    zoo_bear=ZOO + "news-blog/osirase/d085126.html",
    zoo_en="https://honyaku.j-server.com/LUCAKC/ns/tl_ex.cgi?SURL=https://honyaku.j-server.com/LUCAKC/ns/warning_mess.cgi%3furl=https://www.city.asahikawa.hokkaido.jp/asahiyamazoo/index.html%26target=_top&SLANG=ja&TLANG=en&XMODE=0",
    bus="https://www.asahikawa-denkikidou.jp/schedule/zoo-airport-timetable/",
    bus_summer="http://web.archive.org/web/20260715212918/https://www.asahikawa-denkikidou.jp/schedule/zoo-airport-timetable/",
    noriba="https://www.city.asahikawa.hokkaido.jp/kurashi/452/453/456/d064214.html",
    dohoku="https://www.dohokubus.com/", dohoku_touch="https://www.dohokubus.com/touch-payment.html",
    otoko="https://www.otokoyama.com/museum/", otoko_en="https://www.otokoyama.com/en/", sakepark="https://sake-park.otokoyama.com/",
    takasago="https://takasagoshuzo.com/meiji-sakagura/", takasago_access="https://takasagoshuzo.com/contact/",
    miura="https://www.hyouten.com/info", miura_access="https://www.hyouten.com/access",
    forest="https://www.atca.jp/kankouspoy/%e5%a4%96%e5%9b%bd%e6%a8%b9%e7%a8%ae%e8%a6%8b%e6%9c%ac%e6%9e%97/",
    kaimono="https://www.kaimonokouen.com/about",
    baiko="https://baikohken.com/shop", santouka="https://www.santouka.co.jp/shop-jp",
    tokiwa="https://www.atca.jp/kankouspoy/%e5%b8%b8%e7%a3%90%e5%85%ac%e5%9c%92/",
    asahibashi="https://www.atca.jp/kankouspoy/%e6%97%ad%e6%a9%8b/",
    museum="https://artmuseum.pref.hokkaido.lg.jp/abj/guide/about/",
    winfes="https://asahikawa-winterfes.jp/",
    furari="https://www.atca.jp/kankouspoy/%ef%bc%95%ef%bc%8e%ef%bc%97%e5%b0%8f%e8%b7%af%e3%81%b5%e3%82%89%e3%82%8a%e3%83%bc%e3%81%a8/",
    ginneko="https://www.ginneko.co.jp/",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    unkou="https://www3.jrhokkaido.co.jp/webunkou/",
    jma="https://www.data.jma.go.jp/stats/etrn/view/nml_sfc_ym.php?prec_no=12&block_no=47407&year=&month=&day=&view=",
    sun="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容
SOURCES = [dict(what=a, url=b, saw=c, checked=CHECKED) for a, b, c in [
    ("旭山動物園 開園日カレンダー", U["zoo_cal"], "2026年：11/11〜12/29 10:30〜15:30（最終入園15:00）、11/4〜11/10休園。2027年：1/2〜4/7 10:30〜15:30（15:00）、4/29〜10/15 9:30〜17:15（16:00）、10/16〜11/3 9:30〜16:30（16:00）、11/11〜12/29 10:30〜15:30（15:00）。特別開園 2027年2/5〜2/7 10:30〜20:30（20:00）、8/10〜8/16 9:30〜21:00（20:00）"),
    ("旭山動物園 令和8年度冬期開園について（2026年11月6日更新）", U["zoo_winter"], "冬期開園 2026年11月11日〜2027年4月7日、10:30〜15:30（最終入園15:00）。12月30日〜1月1日休園。ペンギンの散歩は12月下旬頃から3月中旬頃までの積雪期、11:00と14:30（3月は11:00のみの予定）、開始はSNSで知らせる、天候や積雪で休止・コース変更あり。園内は坂が多く、滑り止めのついた靴を"),
    ("旭山動物園 開園期間・入園料・チケット（2026年10月1日更新）", U["zoo_fee"], "大人1,000円、中学生以下無料。Webチケット・コンビニチケットあり（Webチケットは旭山三浦庭園連絡ゲートからは入れない）。券売窓口・券売機はキャッシュレス対応（ブランドは画像）"),
    ("旭山動物園 入園料の改定について（2026年7月1日）", U["zoo_newfee"], "2027年4月29日の夏期開園から 大人1,400円（現在1,000円）。中学生以下は無料のまま"),
    ("旭山動物園 アクセス（2026年8月14日更新）", U["zoo_access"], "旭川駅〜動物園 路線バス 約30分間隔・約40分・大人670円。旭川電気軌道 41・47番、のりばは旭川駅前の6番。タクシー約30分・約4,800円。札幌〜旭川 JR約1時間30分"),
    ("旭山動物園 利用案内・おやくそく（2026年11月16日更新）", U["zoo_rules"], "再入園はできません。フラッシュ撮影禁止。ペンギンの散歩やもぐもぐタイムなど混雑エリアで三脚禁止。園内サービスにコインロッカー・フリーWiFi・多言語情報発信サービス。その日のガイドの時間は各門とビジターインフォメーションの看板に掲示"),
    ("旭山動物園 売店・飲食店", U["zoo_food"], "飲食店：Museum Cafe ASAHIYAMA（正門付近）、FOOD BASE CAFE TOTORI（ととりの村向かい）、旭山動物園中央食堂（あざらし館2階）、FarmZoo（西門付近）、カムイチカプ（東門2階）ほか。営業時間の記載はない"),
    ("旭山動物園 ホッキョクグマ「ピリカ」の展示中止（2026年11月24日）", U["zoo_bear"], "ピリカは寝室のみで過ごす。ホッキョクグマのもぐもぐタイムはしばらく中止"),
    ("旭川電気軌道 旭川駅〜旭山動物園線 冬の時刻表（2026年11月11日〜2027年4月7日）", U["bus"], "旭川駅のりば6発→動物園着：41番8:40→9:27、47番9:10→9:49、42番9:35→10:10、41番9:40→10:22、47番9:55→10:34、47番10:10→10:49、41番10:40→11:22 … 41番14:40→15:10。動物園発→旭川駅着：47番13:10→13:54、41番13:40→14:27、47番14:10→14:54、41番14:40→15:27、42番15:00→15:45、47番15:10→15:54、41番15:25→16:12、41番15:40→16:32、47番15:55→16:44、47番16:10→16:59（最終）。運賃 片道 大人670円（2026年9月1日改定）。ICカードはAsaca・DoCARDのみ。バス総合案内所に乗車券の券売機（入園券も買える、クレジット対応の券売機あり）"),
    ("旭川電気軌道 同じページの夏の時刻表（2026年4月29日〜11月3日。Internet Archive の2026年7月15日の保存）", U["bus_summer"], "旭川駅のりば6発→動物園着：41番7:40→8:27、47番8:10→8:54、41番8:40→9:27、47番9:10→9:49、41番9:40→10:22 …。動物園発→旭川駅着：47番13:10→13:50、41番13:40→14:23、47番14:10→14:50 … 47番17:10→17:55、41番17:40→18:28（最終）"),
    ("札幌→旭川 朝 平日", q("札幌", "旭川", "2026/12/03", "07:30"), "特急宗谷 7:30→8:58、特急ライラック5号 8:00→9:25。5,440円（乗車券3,080円＋指定席2,360円）"),
    ("札幌→旭川 朝 土曜", q("札幌", "旭川", "2026/12/05", "07:30"), "特急宗谷 7:30→8:58、特急ライラック5号 8:00→9:25"),
    ("札幌→旭川 9時台 平日・土曜", q("札幌", "旭川", "2026/12/03", "08:30"), "特急カムイ7号 9:00→10:25（12/5も同じ）。高速あさひかわ号 札幌駅前9:00→旭川駅前11:10、2,500円"),
    ("旭川→札幌 夜 平日・土曜", q("旭川", "札幌", "2026/12/03", "19:50"), "特急カムイ42号 20:00→21:25、特急ライラック44号 21:00→22:25（12/5も同じ）"),
    ("旭川→札幌 最終 平日・土曜", q("旭川", "札幌", "2026/12/03", "23:59", "l"), "特急ライラック46号 22:00→23:25（最終。12/5も同じ）。その前は特急宗谷 21:30→22:56"),
    ("JR北海道 北海道レールパス（英語）", U["railpass"], "All seats are reserved on all JR Hokkaido’s limited express trains. There are no non-reserved seats. 乗る前に指定席券を受け取る。Sapporo-Furano Area Pass 11,000円・4日間（旭川を含む）"),
    ("1条8丁目→永山2条6丁目（道北バス）平日", q(BUSSTOP, "永山２条６丁目", "2026/12/03", "14:35"), "14:35→15:03（260円）、14:40→15:09（260円）、15:00→15:25（310円）。15:30→15:55、15:40→16:10 もある"),
    ("1条8丁目→永山2条6丁目（道北バス）土曜・日曜", q(BUSSTOP, "永山２条６丁目", "2026/12/05", "14:35"), "14:40→15:10（260円）、14:45→15:15（350円）、15:30→15:54（12/6の日曜も14:40→15:10、14:45→15:15）"),
    ("永山2条6丁目→1条8丁目（道北バス）平日", q("永山２条６丁目", BUSSTOP, "2026/12/03", "16:10"), "永山2条4丁目16:29→16:54（310円。停留所まで歩く時間を入れて16:24発）、次は17:13→17:40、17:29→17:54"),
    ("永山2条6丁目→1条8丁目（道北バス）土曜", q("永山２条６丁目", BUSSTOP, "2026/12/05", "16:10"), "永山2条4丁目16:29→16:53（310円）、永山2条2丁目16:38→17:00（260円）、17:13→17:40（12/6の日曜も16:29→16:53）"),
    ("道北バス タッチ決済", U["dohoku_touch"], "クレジットカードのタッチ決済は対象路線だけ（都市間バスと、白金線・層雲峡線・空港線などの路線バスの一部）"),
    ("道北バス バスカード", "https://www.dohokubus.com/buscard.html", "ICカードは Doカード と Asaca（全国の交通系ICカードの記載はない）"),
    ("男山 酒造り資料舘", U["otoko"], "9時〜17時、休舘日 年末年始（12/31、1/1〜3）、入舘料無料。道北バス「永山2条6丁目」下車 徒歩2分。旭山動物園から車で15分。3階のビデオは5か国語（日本語・英語・中国語・韓国語・タイ語）。仕込水「延命長寿の水」"),
    ("OTOKOYAMA SAKE PARK", U["sakepark"], "2024年9月13日オープン。新館1階の売店で日本酒の有料試飲（試飲は16:30まで）、カフェスタンド。資料舘（旧館2・3階）は無料のまま"),
    ("髙砂酒造 直売店・工場見学", U["takasago"], "明治酒蔵（直売店）：営業時間9:00〜17:00、定休日 年末年始。1909年に建てられた酒蔵、2000年から資料館・直売店。試飲コーナー、酒造り解説動画（約15分）。工場見学は無料・事前予約制（各回先着10名、WEBか電話、見学日の前日正午まで）"),
    ("髙砂酒造 お問合せ・アクセス", U["takasago_access"], "JR旭川駅から徒歩15分、タクシーで5分。旭川市宮下通17丁目右1号"),
    ("三浦綾子記念文学館 ご利用案内", U["miura"], "9:00〜17:00（最終入館16:30）。7/1〜8/31は毎日開館、9/1〜翌6/30は月曜休館（祝日でも休館）、12/28〜1/5は年末年始休館。大人700円・学生300円・小中高生無料。現金・クレジットカード・交通系電子マネーほか。分館・氷点ラウンジ10:00〜16:00"),
    ("三浦綾子記念文学館 アクセス", U["miura_access"], "JR旭川駅東口より氷点橋を渡り、突当たりが文学館のある見本林。徒歩約20分。タクシーで約3分"),
    ("外国樹種見本林（旭川観光コンベンション協会）", U["forest"], "1898年（明治31年）に植栽。ストローブマツ・ヨーロッパカラマツなど約30種。三浦綾子『氷点』の舞台"),
    ("旭川平和通買物公園（商店街振興組合）", U["kaimono"], "1972年6月1日に開設された全国初の恒久的な歩行者専用道路。旭川駅前から8条通まで約1km。2月の冬まつりのときに氷彫刻世界大会の会場"),
    ("梅光軒 店舗一覧", U["baiko"], "旭川本店：旭川市2条8丁目 買物公園ピアザビルB1F、11:00〜15:30（L.O.15:00）、17:00〜21:00（L.O.20:30）、不定休"),
    ("らーめん山頭火 国内店舗", U["santouka"], "旭川本店：11:00〜22:00（ラストオーダー21:30）、スープがなくなり次第終了、定休日 木曜（祝日は営業）、旭川市1条通8丁目348番地6"),
    ("常磐公園（旭川観光コンベンション協会）", U["tokiwa"], "1910年（明治43年）開設の旭川で最初の公園。16ヘクタール、白鳥・千鳥の2つの池、手漕ぎボート。日本の都市公園100選"),
    ("旭橋（旭川観光コンベンション協会）", U["asahibashi"], "1932年（昭和7年）11月完成。橋長225.4m、幅18.3m のアーチ橋。昭和31年までは市内電車が橋の上を走った。北海道遺産（平成16年）。夕日の残照、冬の川霧"),
    ("北海道立旭川美術館 開館時間・休館日・観覧料", U["museum"], "9:30〜17:00（展示室への入場は16:30まで）。月曜休館（祝日は開館して翌火曜休館）、年末年始12/29〜1/3、展示替期間。観覧料は展覧会ごと"),
    ("旭川冬まつり 公式サイト", U["winfes"], "第68回旭川冬まつり2027：2027年2月6日（土）〜11日（木・祝）の6日間。会場は常磐公園と石狩川旭橋河畔会場ほか"),
    ("5・7小路ふらりーと（旭川観光コンベンション協会）", U["furari"], "5条通7丁目の小路、正式名称は中央市場。戦前は魚菜市場、のちに「焼き鳥横丁」。約3mの通路をはさんで焼き鳥・ラーメン・居酒屋など18店舗ほど。冬は店の前にアイスキャンドル"),
    ("焼鳥専門ぎんねこ", U["ginneko"], "昭和25年創業。旭川市5条通7丁目右6（5・7小路ふらりーと）。営業時間13:00〜22:00、月曜定休。席の予約は受けていない。新子焼きは生後4〜5週の若鶏。英語などのページあり。休業日のお知らせが毎月出る"),
    ("気象庁 旭川の平年値（1991〜2020年）", U["jma"], "1月：日最高−3.3℃、日最低−11.7℃。2月：−1.7℃、−11.8℃。12月：−0.8℃、−8.0℃。7月：26.2℃、16.4℃"),
    ("国立天文台 札幌の日の出入り 2026年12月", U["sun"], "札幌の12月の日の入りは16時ごろ。旭川（北緯43.77度・東経142.36度）は計算で12月上旬〜下旬15:54ごろ、6月下旬19:15、8月末18:10、9月末17:15、10月末16:24"),
]]

ZOO_L = link("official", "旭山動物園", "Asahiyama Zoo (machine-translated English)", U["zoo"], U["zoo_en"])
ZOO_CAL = link("official", "旭山動物園 開園日カレンダー・その日のスケジュール", "Asahiyama Zoo calendar and daily schedule (Japanese)", U["zoo_cal"])
BUS_L = link("timetable", "旭川駅〜旭山動物園のバス時刻表（旭川電気軌道）", "Bus timetable, Asahikawa Station – Asahiyama Zoo (Asahikawa Denki Kido)", U["bus"])
JR = link("timetable", "JR北海道 運行情報", "JR Hokkaido service status", U["unkou"], "https://www3.jrhokkaido.co.jp/webunkou/en/")
JRPASS = link("info", "北海道レールパス（JR北海道）", "Hokkaido Rail Pass (JR Hokkaido)", U["railpass"])

N_COLD = notice(
    "冬（12〜3月）：−10℃を下回る朝があります", "Winter (Dec–Mar): mornings can drop below −10°C",
    "旭川の1月は、平年で最高−3.3℃・最低−11.7℃。外に長くいる動物園では、ダウンの上着、帽子、手袋、厚い靴下、首を覆うものを。カイロはコンビニで買えます。歩道は雪が踏み固められて凍るので、底がすべりにくい靴で。スマートフォンは寒いと電池が早く減ります。",
    "January in Asahikawa averages a high of −3.3°C and a low of −11.7°C. For the hours outside at the zoo, wear a down jacket, hat, gloves, thick socks and something over your neck; convenience stores sell stick-on hand warmers (kairo). Pavements turn to packed ice, so wear shoes with grippy soles. Phone batteries drain fast in the cold.",
    U["jma"])
N_SNOW_JR = notice(
    "冬：雪の日はJRとバスが遅れることがあります", "Winter: snow can delay trains and buses",
    "大雪の日は特急が遅れたり運休したりします。札幌から日帰りの人は、出る前と帰る前にJR北海道の運行情報を見てください。",
    "Heavy snow can delay or cancel limited express trains. Day-trippers from Sapporo should check JR Hokkaido’s service status before leaving and before heading back.",
    U["unkou"])
N_BUS_PAY = notice(
    "バスでは Suica などのICカードが使えません", "Suica and other IC cards do not work on the buses",
    "旭川のバスで使えるICカードは、地元の Asaca と DoCARD だけです。動物園までは片道670円。現金（千円札と小銭）を用意するか、駅前のバス総合案内所の券売機で先にきっぷを買ってください（往復なら2枚）。券売機では動物園の入園券も買えます。",
    "The only IC cards accepted on Asahikawa buses are the local Asaca and DoCARD. The zoo is ¥670 each way: carry cash (¥1,000 notes and coins), or buy tickets first from the machine at the bus information centre by the station (two tickets for a return). The machine also sells zoo admission tickets.",
    U["bus"])
N_ZOO_YEAREND = notice(
    "12月30日〜1月1日は休園", "Closed 30 December – 1 January",
    "旭山動物園は2026年12月30日（水）から2027年1月1日（金）まで休みです。1月2日から開きます。",
    "Asahiyama Zoo is closed from Wed 30 December 2026 to Fri 1 January 2027 and reopens on 2 January.",
    U["zoo_winter"], start="2026-12-10", to="2027-01-01")
N_ZOO_SPRING = notice(
    "4月8日〜28日は休園", "Closed 8–28 April",
    "冬期開園は2027年4月7日まで。4月8日から28日は休園で、4月29日から夏期開園（9:30〜17:15）です。",
    "The winter season ends on 7 April 2027. The zoo is closed from 8 to 28 April and reopens for summer on 29 April (9:30–17:15).",
    U["zoo_cal"], start="2027-03-25", to="2027-04-28")
N_ZOO_AUTUMN = notice(
    "11月4日〜10日は休園", "Closed 4–10 November",
    "夏期開園は2027年11月3日まで。11月4日から10日は休園で、11月11日から冬期開園（10:30〜15:30）です。",
    "The summer season ends on 3 November 2027. The zoo is closed from 4 to 10 November and reopens for winter on 11 November (10:30–15:30).",
    U["zoo_cal"], start="2027-10-20", to="2027-11-10")
N_PENGUIN = notice(
    "ペンギンの散歩は、雪が積もってから（12月下旬ごろ〜3月中旬ごろ）", "The penguin walk starts once the snow has settled (about late December to mid-March)",
    "11:00と14:30の2回（3月は11:00だけの予定）。始まる日は、動物園の公式SNSと公式サイトで発表されます。天気や雪の状態で中止になったり、コースが変わったりします。11:00の回に合わせるなら、旭川駅9:40のバスで。",
    "Twice a day at 11:00 and 14:30 (11:00 only in March, as planned). The start date is announced on the zoo’s social media and website; the walk can be cancelled or rerouted depending on weather and snow. For the 11:00 walk, take the 9:40 bus from Asahikawa Station.",
    U["zoo_winter"], to="2027-03-20")
N_BEAR = notice(
    "ホッキョクグマのもぐもぐタイムは、しばらく中止", "Polar bear feeding talks are suspended for now",
    "2026年11月24日から、メスの「ピリカ」は寝室で過ごしていて見られません。ホッキョクグマのもぐもぐタイム（えさの時間のガイド）も、しばらくありません。",
    "Since 24 November 2026 the female polar bear Pirika has been kept in her den and cannot be seen, and the polar bear feeding talks are suspended.",
    U["zoo_bear"], to="2027-04-07")
N_YUKIAKARI = notice(
    "2月5日〜7日は夜8時半まで（雪あかりの動物園）", "Open until 20:30 on 5–7 February (Snow-lantern nights)",
    "2027年2月5日（金）〜7日（日）は、10:30〜20:30（最終入園20:00）の特別開園です。旭川冬まつり（2月6日〜11日）と重なります。帰りのバスの時刻は、旭川電気軌道のページで確かめてください。",
    "On Fri 5 – Sun 7 February 2027 the zoo stays open 10:30–20:30 (last entry 20:00). It overlaps with the Asahikawa Winter Festival (6–11 February). Check the bus company’s page for return buses on those evenings.",
    U["zoo_cal"], start="2027-01-10", to="2027-02-07")
N_NEWFEE = notice(
    "2027年4月29日から入園料は1,400円", "Admission rises to ¥1,400 from 29 April 2027",
    "大人1,000円の入園料は、2027年4月29日の夏期開園から1,400円になります。中学生以下は無料のままです。",
    "Adult admission (now ¥1,000) becomes ¥1,400 from the summer opening on 29 April 2027. Junior high school students and younger stay free.",
    U["zoo_newfee"], to="2027-04-28")
N_SUMMER_BUS = notice(
    "夏のバスの時刻は2026年のものです", "Summer bus times are from 2026",
    "2027年の夏期開園（4月29日〜）のバスの時刻表は、まだ発表されていません。このコースの動物園のバスの時刻は、2026年の夏の時刻表です。行く前に、旭川電気軌道のページで確かめてください。",
    "The bus timetable for the 2027 summer season (from 29 April) has not been published yet. The zoo bus times in this course are from the 2026 summer timetable: check the bus company’s page before you go.",
    U["bus"])
N_FES = notice(
    "2月6日〜11日は旭川冬まつり", "Asahikawa Winter Festival: 6–11 February",
    "第68回旭川冬まつりは2027年2月6日（土）〜11日（木・祝）。会場は常磐公園と、旭橋のそばの石狩川の河畔です。買物公園には氷の彫刻が並びます。このときは、暗くなってからも公園まで歩く人が多くいます。",
    "The 68th Asahikawa Winter Festival runs from Sat 6 to Thu 11 February 2027, in Tokiwa Park and on the Ishikari riverbank beside Asahibashi Bridge, with ice sculptures along the Kaimono Koen mall. During the festival plenty of people walk up to the park after dark.",
    U["winfes"], start="2027-01-10", to="2027-02-11")
N_MIURA_CLOSED = notice(
    "月曜は休館（7・8月は毎日開館）", "Closed on Mondays (open daily in July and August)",
    "9月1日〜6月30日は、祝日でも月曜は休みです。12月28日〜1月5日も年末年始の休館。最終入館は16:30。",
    "From 1 September to 30 June the museum is closed every Monday, holidays included, and from 28 December to 5 January. Last entry is 16:30.",
    U["miura"])
N_GINNEKO = notice(
    "ぎんねこは月曜休み、席の予約はできません", "Ginneko: closed Mondays, no table bookings",
    "13:00〜22:00。ほかに臨時の休みが毎月あり、公式サイトのお知らせに出ます。小さな店なので、混む時間は待つことがあります。",
    "Open 13:00–22:00. Extra closing days are posted each month on the official website. It is a small place, so expect a wait at busy times.",
    U["ginneko"])


def spots(c):
    """c は 'winter' か 'summer'。番号は同じで、時間と文章の一部が変わる"""
    w = c == "winter"
    return [
        dict(
            id="eki", name=T("旭川駅（出発）", "Asahikawa Station (start)"), kind=T("駅・バスのりば", "Station & bus stop"),
            blurb=T("駅前の6番のりばから、9:40のバスで動物園へ。運賃は現金で。", "Bus stop 6 in front of the station: the 9:40 to the zoo. Pay in cash.") if w else
                  T("駅前の6番のりばから、9:10のバスで動物園へ。運賃は現金で。", "Bus stop 6 in front of the station: the 9:10 to the zoo. Pay in cash."),
            caution=T("バスはSuicaなどのICカードが使えません（現金670円）", "No Suica or other IC cards on the bus (¥670 in cash)"),
            lat=43.76275, lng=142.35793,
            body=T(
                ("動物園行きのバス（旭川電気軌道の41番・47番）は、旭川駅の北口を出た駅前の6番のりばから出ます。冬の動物園は10:30に開くので、9:40発（10:22着）がちょうどよい時刻です。次の9:55発（10:34着）でも大丈夫。約40分、片道670円です。\n\n"
                 "駅のまわりのホテルなら、9:25ごろに出れば間に合います。のりばは外なので、冬は早く着きすぎないように。駅の中で待って、5分前に出るくらいで。\n\n"
                 "札幌から日帰りの人：札幌8:00発の特急ライラック5号が旭川9:25着で、9:40のバスに乗れます（乗り換え15分）。札幌9:00発のカムイ7号（10:25着）だと10:40のバスで動物園に11:22。11:00のペンギンの散歩には間に合わないので、午後2時半の回を見ることになります。特急は全部の席が指定席で、片道5,440円。北海道レールパスの人も、乗る前に指定席券を受け取ってください。"
                 if w else
                 "動物園行きのバス（旭川電気軌道の41番・47番）は、旭川駅の北口を出た駅前の6番のりばから出ます。雪のない季節の動物園は9:30に開きます。9:10発（9:49着）なら、駅のまわりのホテルを8:55ごろに出れば間に合います。開園と同時に入りたい日は8:40発（9:27着）で。約40分、片道670円です。\n\n"
                 "夏休みや連休の昼前はバスも園内も混みます。朝のうちに着くほど、人気の館をゆっくり見られます。\n\n"
                 "札幌から日帰りの人：札幌8:00発の特急ライラック5号が旭川9:25着で、9:40のバス（10:22着）に乗れます。特急は全部の席が指定席で、片道5,440円。北海道レールパスの人も、乗る前に指定席券を受け取ってください。"),
                ("Buses to the zoo (Asahikawa Denki Kido routes 41 and 47) leave from stop 6, right outside the station’s north exit. In winter the zoo opens at 10:30, so the 9:40 (arriving 10:22) is the one to take; the 9:55 (arriving 10:34) works too. The ride takes about 40 minutes and costs ¥670 each way.\n\n"
                 "From a hotel near the station, leaving at about 9:25 is enough. The stop is outdoors, so in winter do not arrive too early: wait inside the station and step out five minutes before.\n\n"
                 "Day trip from Sapporo: the Lilac 5 limited express leaves Sapporo at 8:00 and reaches Asahikawa at 9:25, in time for the 9:40 bus (15 minutes to change). The Kamui 7 at 9:00 (arriving 10:25) puts you on the 10:40 bus, at the zoo at 11:22: too late for the 11:00 penguin walk, so you would watch the 14:30 one. All seats on the limited expresses are reserved: ¥5,440 each way. Hokkaido Rail Pass holders also need to pick up a seat reservation before boarding."
                 if w else
                 "Buses to the zoo (Asahikawa Denki Kido routes 41 and 47) leave from stop 6, right outside the station’s north exit. Outside winter the zoo opens at 9:30. For the 9:10 bus (arriving 9:49), leave a hotel near the station at about 8:55; to walk in at opening time, take the 8:40 (arriving 9:27). The ride takes about 40 minutes and costs ¥670 each way.\n\n"
                 "In the summer holidays and on long weekends both the buses and the zoo fill up before noon. The earlier you arrive, the easier the popular houses are.\n\n"
                 "Day trip from Sapporo: the Lilac 5 limited express leaves Sapporo at 8:00 and reaches Asahikawa at 9:25, in time for the 9:40 bus (arriving 10:22). All seats on the limited expresses are reserved: ¥5,440 each way. Hokkaido Rail Pass holders also need to pick up a seat reservation before boarding.")),
            gmaps=[gm("旭川駅前 バスのりば（6番）", "Bus stops in front of Asahikawa Station (stop 6)", 43.76365, 142.35850, "旭川駅前 バスタッチ"),
                   gm("JR旭川駅", "JR Asahikawa Station", 43.76275, 142.35793, "JR旭川駅")],
            links=[BUS_L, link("info", "旭川駅周辺のバスのりば案内（旭川市）", "Bus stops around Asahikawa Station (city website, Japanese)", U["noriba"]), JR, JRPASS],
            notices=([N_COLD, N_BUS_PAY, N_SNOW_JR] if w else [N_BUS_PAY, N_SUMMER_BUS]),
            rows=([row("bus", "旭川駅6番のりば 9:40 → 旭山動物園 10:22（41番）。次は9:55 → 10:34（47番）、10:10 → 10:49。平日・土日祝とも（2027年4月7日まで）", "Asahikawa Station stop 6 9:40 → Asahiyama Zoo 10:22 (route 41). Next: 9:55 → 10:34 (route 47), 10:10 → 10:49. Same every day (until 7 April 2027)")]
                  if w else
                  [row("bus", "旭川駅6番のりば 9:10 → 旭山動物園 9:49（47番）。前は8:40 → 9:27（41番）、次は9:40 → 10:22。2026年夏の時刻", "Asahikawa Station stop 6 9:10 → Asahiyama Zoo 9:49 (route 47). Before: 8:40 → 9:27 (route 41); next: 9:40 → 10:22. 2026 summer times")]) + [
                  row("fee", "バス 片道670円（2026年9月1日から）。現金か、バス総合案内所の券売機のきっぷ", "Bus ¥670 each way (since 1 Sept 2026): cash, or a ticket from the machine at the bus information centre"),
                  row("train", "札幌8:00 → 旭川9:25（特急ライラック5号）。札幌9:00 → 旭川10:25（特急カムイ7号）。平日・土曜とも", "Sapporo 8:00 → Asahikawa 9:25 (Lilac 5). Sapporo 9:00 → Asahikawa 10:25 (Kamui 7). Weekdays and Saturdays"),
                  row("fee", "札幌〜旭川 片道5,440円（乗車券3,080円＋指定席2,360円）。全席指定", "Sapporo – Asahikawa ¥5,440 each way (fare ¥3,080 + reserved seat ¥2,360). All seats reserved")],
            tip=T("バスは旭川電気軌道の公式の時刻表、JRは乗換案内の2026年12月3日（木）・5日（土）で確認しました。JR北海道は2027年3月にダイヤ改正の予定なので、春からは時刻が変わることがあります。",
                  "Buses from the operator’s official timetable; trains checked in a route planner for Thu 3 and Sat 5 December 2026. JR Hokkaido usually revises its timetable in March, so times may change from spring 2027."),
            time=(DEP, "9:40発（ホテルは9:25ごろ出る）", "9:40 (leave your hotel at about 9:25)") if w else (DEP, "9:10発（ホテルは8:55ごろ出る）", "9:10 (leave your hotel at about 8:55)"),
            photos=W("eki")),
        dict(
            id="zoo", name=T("旭山動物園（あさひやまどうぶつえん）", "Asahiyama Zoo"), kind=T("動物園", "Zoo"),
            blurb=T("冬は10:30〜15:30。雪の上を歩くペンギンは11:00と14:30。", "Winter hours 10:30–15:30. Penguins walk on the snow at 11:00 and 14:30.") if w else
                  T("9:30開園。水の中のペンギン、アザラシ、ホッキョクグマを間近に。", "Opens 9:30. Penguins, seals and polar bears seen from under the water."),
            caution=T("再入園はできません。12月30日〜1月1日は休園", "No re-entry. Closed 30 Dec – 1 Jan") if w else T("再入園はできません。4月8日〜28日と11月4日〜10日は休園", "No re-entry. Closed 8–28 Apr and 4–10 Nov"),
            lat=43.76859, lng=142.47592,
            body=T(
                "日本でいちばん北にある動物園。動物が泳ぐ、飛び込む、歩くところを、すぐ近くから見られるように造った展示で知られています。ぺんぎん館は水の中のトンネルから、あざらし館は筒の形の水槽を上り下りするアザラシを、ほっきょくぐま館は水に飛び込むクマをガラス越しに見ます。\n\n"
                + ("冬の見ものはペンギンの散歩。雪が積もってから（例年12月下旬ごろ〜3月中旬ごろ）、11:00と14:30にキングペンギンが園内の雪道を歩きます。10:22に着いたら、まず看板でその日の予定を確かめて、散歩のコースへ。人が並ぶので、10分前には場所を決めておくと前で見られます。三脚は使えません。\n\n"
                   "園は山の斜面にあり、坂が多くて、雪の日はすべります。正門から入って、ペンギン・アザラシ・ホッキョクグマを先に見て、体が冷えたら屋内の館か休憩所へ。お昼は園内の食堂で（あざらし館2階の中央食堂、正門のそばの Museum Cafe など）。再入園はできないので、外に食べに出ることはできません。\n\n"
                   "帰りは14:10のバス（旭川駅14:54着）。開いているのが5時間だけなので、3時間半あれば主な館は回れます。14:30の散歩も見る日は、15:10のバス（15:54着）で。最後のバスは16:10発です。"
                   if w else
                   "9:49に着いたら、正門から入って、人気のぺんぎん館・あざらし館・ほっきょくぐま館を先に。昼前から混んでくる館なので、朝のうちがゆっくり見られます。えさの時間に飼育員が話す「もぐもぐタイム」の時刻は、門のそばの看板と公式サイトの「本日のスケジュール」に出ます。\n\n"
                   "園は山の斜面にあって坂が多いので、歩きやすい靴で。お昼は園内の食堂で（あざらし館2階の中央食堂、正門のそばの Museum Cafe、東門2階のカムイチカプなど）。再入園はできません。\n\n"
                   "帰りは13:40のバス（旭川駅14:23着）。もっと見ていたい日は、男山をやめて16時台まで残る手もあります（10月16日からは16:30閉園）。雪の上のペンギンの散歩は冬だけです。"),
                "Japan’s northernmost zoo, known for enclosures built so that you see the animals swim, dive and walk from very close. You watch penguins from a tunnel under their pool, seals rising and sinking through a vertical glass tube, and polar bears plunging into the water on the other side of the glass.\n\n"
                + ("The winter highlight is the penguin walk. Once the snow has settled (usually late December to mid-March), king penguins walk a snowy path through the zoo at 11:00 and 14:30. Arriving at 10:22, check the day’s schedule on the board first, then head for the walk route. People line the path, so pick your spot ten minutes ahead to be at the front. Tripods are not allowed.\n\n"
                   "The zoo sits on a hillside with many slopes, slippery on snowy days. Enter by the Main Gate, see the penguins, seals and polar bears first, and warm up in an indoor house or rest room when you get cold. Have lunch at one of the zoo’s restaurants (the Central Restaurant upstairs in the Seal House, Museum Cafe by the Main Gate and others): there is no re-entry, so you cannot pop out to eat.\n\n"
                   "Take the 14:10 bus back (Asahikawa Station 14:54). The zoo is only open five hours, and three and a half are enough for the main houses. To see the 14:30 walk as well, take the 15:10 bus (arriving 15:54). The last bus leaves at 16:10."
                   if w else
                   "Arriving at 9:49, enter by the Main Gate and go to the popular Penguin, Seal and Polar Bear houses first: they get crowded from late morning. Times for the keepers’ feeding talks (“mogu-mogu time”) are on the board by the gates and on the “today’s schedule” page of the website.\n\n"
                   "The zoo sits on a hillside with many slopes, so wear comfortable shoes. Have lunch at one of the zoo’s restaurants (the Central Restaurant upstairs in the Seal House, Museum Cafe by the Main Gate, Kamuy Cikap upstairs at the East Gate and others). There is no re-entry.\n\n"
                   "Take the 13:40 bus back (Asahikawa Station 14:23). If you would rather stay, skip Otokoyama and remain until after 16:00 (the zoo closes at 16:30 from 16 October). The penguin walk on snow is winter only.")),
            gmaps=[gm("旭山動物園 正門", "Asahiyama Zoo Main Gate", 43.76859, 142.47592, "旭山動物園 正門")],
            links=[ZOO_L, ZOO_CAL, link("official", "入園料・チケット（Webチケット）", "Admission and web tickets (Japanese)", U["zoo_fee"]), BUS_L],
            notices=([N_ZOO_YEAREND, N_PENGUIN, N_COLD, N_YUKIAKARI, N_BEAR, N_ZOO_SPRING, N_NEWFEE] if w else [N_NEWFEE, N_ZOO_AUTUMN, N_SUMMER_BUS]),
            rows=([row("hours", "冬期開園 10:30〜15:30（最終入園15:00）。2026年11月11日〜2027年4月7日", "Winter season 10:30–15:30 (last entry 15:00), 11 Nov 2026 – 7 Apr 2027"),
                   row("closed", "12月30日〜1月1日。4月8日〜28日", "30 Dec – 1 Jan; 8–28 Apr")]
                  if w else
                  [row("hours", "夏期開園 9:30〜17:15（最終入園16:00）。2027年4月29日〜10月15日。10月16日〜11月3日は16:30まで", "Summer season 9:30–17:15 (last entry 16:00), 29 Apr – 15 Oct 2027; until 16:30 from 16 Oct to 3 Nov"),
                   row("closed", "4月8日〜28日、11月4日〜10日", "8–28 Apr and 4–10 Nov")]) + [
                  row("fee", "大人1,000円、中学生以下は無料", "Adults ¥1,000; junior high school students and younger free", until="2027-04-28"),
                  row("fee", "大人1,400円、中学生以下は無料（2027年4月29日から）", "Adults ¥1,400; junior high school students and younger free (from 29 Apr 2027)", start="2027-04-29"),
                  row("pay", "券売窓口と券売機はキャッシュレス対応。Webチケットなら券売所に並ばずに入れます", "Ticket windows and machines take cashless payment. A web ticket lets you skip the ticket queue")] + (
                  [row("bus", "帰り：動物園14:10 → 旭川駅14:54（47番）。14:40 → 15:27、15:10 → 15:54、最終16:10 → 16:59", "Back: Zoo 14:10 → Asahikawa Station 14:54 (route 47). Then 14:40 → 15:27, 15:10 → 15:54; last bus 16:10 → 16:59")]
                  if w else
                  [row("bus", "帰り：動物園13:40 → 旭川駅14:23（41番）。14:10 → 14:50、最終17:40 → 18:28。2026年夏の時刻", "Back: Zoo 13:40 → Asahikawa Station 14:23 (route 41). Then 14:10 → 14:50; last bus 17:40 → 18:28. 2026 summer times")]),
            tip=T("開園日・時間・料金・ペンギンの散歩は旭山動物園の公式サイト、バスは旭川電気軌道の時刻表で確認しました。園内の食堂の営業時間は公式サイトに書かれていません。荷物は園内のコインロッカーへ。",
                  "Opening days, hours, fees and the penguin walk are from the zoo’s official website; buses from the operator’s timetable. The website gives no hours for the zoo restaurants. There are coin lockers inside the zoo."),
            time=(VIS, "10:22〜14:10", "10:22–14:10") if w else (VIS, "9:49〜13:40", "9:49–13:40"),
            photos=W("zoo")),
        dict(
            id="otoko", name=T("男山 酒造り資料舘（おとこやま）", "Otokoyama Sake Brewery Museum"), kind=T("酒蔵・資料館", "Sake brewery & museum"),
            blurb=T("無料の資料館と、売店での試飲（有料・16:30まで）。バスで約30分。", "A free museum and paid tastings at the shop (until 16:30). About 30 minutes by bus."),
            caution=T("試飲は16:30まで。12月31日〜1月3日は休み", "Tastings until 16:30. Closed 31 Dec – 3 Jan"),
            lat=43.79604, lng=142.40937,
            body=T(
                "「男山」は江戸時代から名前の知られた酒で、旭川の蔵がその名を受け継いでいます。資料舘（無料）の2階には、男山が描かれた歌麿や国芳の浮世絵、3階には昔の酒造りの桶や道具。3階のビデオは英語・中国語・韓国語・タイ語でも見られます。仕込みの時期は、酒造りの様子も一部見られます。\n\n"
                "となりの新しい売店には有料の試飲があり、蔵でしか買えない酒も並びます。試飲は16:30まで。仕込みに使う大雪山の伏流水「延命長寿の水」は、だれでも飲めます。\n\n"
                + ("冬にここを選ぶ日：動物園を1本早い13:40のバスで出て、旭川駅14:27。1条通の「1条8丁目」のバス停（駅から歩いて5分）から14:40発の道北バスで「永山2条6丁目」15:09、歩いて2分。1時間ほど見て、16:29発のバスで1条8丁目16:54着。帰りはもう暗くなっています。髙砂酒造（4番）と両方に行く時間はないので、どちらか1つに。"
                   if w else
                   "動物園から13:40のバスで旭川駅に戻り（14:23）、1条通の「1条8丁目」のバス停へ歩いて5分。14:40発の道北バスで「永山2条6丁目」15:09、そこから歩いて2分です。1時間ほど見て、16:29発のバスで1条8丁目16:54着。")
                + "\n\nバスは行き先に「永山」と出る系統がいくつもあり、乗る系統で運賃が少し違います（260〜350円）。運転手さんに「永山2条6丁目」と見せて確かめると安心です。",
                "Otokoyama is a sake name famous since the Edo period, carried on today by this Asahikawa brewery. The free museum shows ukiyo-e prints by Utamaro and Kuniyoshi that feature Otokoyama (2nd floor) and old wooden vats and brewing tools (3rd floor), with a video available in English, Chinese, Korean and Thai. In the brewing season you can also see part of the brewery at work.\n\n"
                "The new shop next door has paid tastings and bottles sold only at the brewery; tastings end at 16:30. The brewing water, an underground flow from the Daisetsuzan mountains, runs from a tap for anyone to drink.\n\n"
                + ("If you choose this in winter: leave the zoo one bus earlier, on the 13:40 (Asahikawa Station 14:27). From the “1-jo 8-chome” stop on Ichijo-dori, five minutes’ walk from the station, the 14:40 Dohoku Bus reaches “Nagayama 2-jo 6-chome” at 15:09, two minutes’ walk from the brewery. Allow about an hour and come back on the 16:29, arriving 1-jo 8-chome at 16:54. It will be dark on the way back. There is not time for both this and Takasago (no. 4): pick one."
                   if w else
                   "Take the 13:40 bus from the zoo back to Asahikawa Station (14:23) and walk five minutes to the “1-jo 8-chome” stop on Ichijo-dori. The 14:40 Dohoku Bus reaches “Nagayama 2-jo 6-chome” at 15:09, two minutes’ walk from the brewery. Allow about an hour, then take the 16:29 bus back, arriving 1-jo 8-chome at 16:54.")
                + "\n\nSeveral bus routes with “Nagayama” (永山) on the front go this way, and the fare differs a little by route (¥260–350). Show the driver “永山2条6丁目” to be sure."),
            gmaps=[gm("男山 酒造り資料舘", "Otokoyama Sake Brewery Museum", 43.79604, 142.40937, "男山酒造り資料館"),
                   gm("道北バス 1条8丁目のりば", "Dohoku Bus stop, 1-jo 8-chome", 43.76470, 142.35960, "1条8丁目 バス停 旭川 道北バス")],
            links=[link("official", "男山 酒造り資料舘", "Otokoyama (English)", U["otoko"], U["otoko_en"]),
                   link("official", "OTOKOYAMA SAKE PARK（売店・試飲）", "Otokoyama Sake Park: shop and tastings (Japanese)", U["sakepark"]),
                   link("timetable", "道北バス", "Dohoku Bus (Japanese)", U["dohoku"])],
            notices=[notice("バスは現金で", "Pay the bus in cash",
                            "道北バスの市内の路線は、SuicaなどのICカードが使えません。クレジットカードのタッチ決済も一部の路線だけです。小銭と千円札を用意してください。",
                            "Dohoku Bus city routes do not take Suica or other national IC cards, and contactless credit cards work on only a few routes. Carry coins and ¥1,000 notes.",
                            U["dohoku_touch"])],
            rows=[row("hours", "9:00〜17:00（試飲は16:30まで）", "9:00–17:00 (tastings until 16:30)"),
                  row("closed", "12月31日〜1月3日", "31 Dec – 3 Jan"),
                  row("fee", "資料舘は無料。試飲は有料", "Museum free; tastings are paid"),
                  row("bus", "行き：1条8丁目14:40 → 永山2条6丁目15:09（土日は15:10）。次は15:30 → 15:55。12月の時刻",
                      "Out: 1-jo 8-chome 14:40 → Nagayama 2-jo 6-chome 15:09 (15:10 at weekends). Next 15:30 → 15:55. December times"),
                  row("bus", "帰り：永山2条4丁目16:29 → 1条8丁目16:54（土日は16:53）。次は17:13 → 17:40。260〜350円", "Back: Nagayama 2-jo 4-chome 16:29 → 1-jo 8-chome 16:54 (16:53 at weekends). Next 17:13 → 17:40. ¥260–350")],
            tip=T("時間・休みは男山の公式サイト。バスは乗換案内の2026年12月3日（木）・5日（土）・6日（日）の時刻で、季節で変わることがあります。帰りのバス停は、乗換案内では来た道を少し戻った「永山2条4丁目」でした（歩いて5分ほど）。試飲の値段は公式サイトに書かれていません。",
                  "Hours and closing days from Otokoyama’s website. Bus times are from a route planner for Thu 3, Sat 5 and Sun 6 December 2026 and may differ in other seasons. For the return, the planner used the “Nagayama 2-jo 4-chome” stop, about five minutes’ walk back the way the bus came. Tasting prices are not on the website."),
            time=(VIS, "15:10〜16:20（選んだ日）", "15:10–16:20 (if chosen)") if w else (VIS, "15:10〜16:20", "15:10–16:20"),
            photos=W("otoko")),
        dict(
            id="takasago", name=T("髙砂酒造 明治酒蔵（たかさごしゅぞう）", "Takasago Sake Brewery: Meiji Sakagura"), kind=T("酒蔵・直売店", "Sake brewery shop"),
            blurb=T("1909年の酒蔵が直売店と資料館に。駅から歩いて15分。", "A 1909 brewery building, now the shop and a small museum. 15 minutes on foot from the station."),
            caution=T("17:00まで。年末年始は休み", "Open until 17:00. Closed over New Year"),
            lat=43.76030, lng=142.37245,
            body=T(
                "「国士無双（こくしむそう）」の蔵。1909年（明治42年）に建てられた酒蔵が、いまは直売店と資料館になっています。試飲のコーナーがあり、酒造りを説明する動画（約15分）も流れています。ここでしか買えない酒もあります。\n\n"
                + ("動物園から14:10のバスで旭川駅に戻ったら（14:54）、宮下通を東へ歩いて15分。雪道が心配な日や荷物のある日はタクシーで5分です。暗くなる前に着けます（12月の日の入りは16時ごろ）。帰りは同じ道を戻って、買物公園へ。"
                   if w else
                   "駅から宮下通を東へ歩いて15分。男山（3番）のかわりに選ぶなら、動物園から戻って15:00ごろに着きます。男山と両方に行くには時間が足りません。")
                + "\n\n蔵の中の見学は無料ですが、予約制です（各回10人まで。公式サイトか電話で、前日の正午まで）。予約なしでも、直売店と資料館には入れます。",
                "The home of Kokushi Muso sake. The brewery building of 1909 is now the shop and a small museum, with a tasting counter and a 15-minute video on how sake is made. Some bottles are sold only here.\n\n"
                + ("Back at Asahikawa Station on the 14:10 bus from the zoo (14:54), walk 15 minutes east along Miyashita-dori; on snowy days or with bags, a taxi takes five minutes. You arrive before dark (sunset is around 16:00 in December). Walk back the same way to the Kaimono Koen mall."
                   if w else
                   "It is 15 minutes’ walk east from the station along Miyashita-dori. If you choose it instead of Otokoyama (no. 3), you will get here at about 15:00 after the zoo. There is not time for both breweries.")
                + "\n\nTours inside the working brewery are free but must be booked (up to 10 people per slot; on the website or by phone, by noon the day before). The shop and museum need no booking."),
            gmaps=[gm("髙砂酒造 明治酒蔵", "Takasago Shuzo Meiji Sakagura", 43.76030, 142.37245, "高砂酒造 明治酒蔵")],
            links=[link("official", "髙砂酒造 直売店・工場見学", "Takasago Shuzo shop and tours (Japanese)", U["takasago"]),
                   link("info", "髙砂酒造 アクセス", "Takasago Shuzo access (Japanese)", U["takasago_access"])],
            notices=[],
            rows=[row("hours", "直売店 9:00〜17:00", "Shop 9:00–17:00"),
                  row("closed", "年末年始", "New Year period"),
                  row("walk", "旭川駅から歩いて15分。タクシーで5分", "15 min on foot from Asahikawa Station; 5 min by taxi"),
                  row("reserve", "蔵の見学は予約制・無料（前日の正午まで）。直売店は予約なしで", "Brewery tours: free, by booking (by noon the day before). No booking for the shop")],
            tip=T("時間と見学の予約は髙砂酒造の公式サイトで確認しました。年末年始の休みの日付と、試飲が有料かどうかは公式サイトに書かれていません（要確認）。",
                  "Hours and tour bookings from Takasago Shuzo’s website. The exact New Year closing dates and whether tastings are charged are not stated there (please check)."),
            time=(VIS, "15:15〜16:00", "15:15–16:00") if w else (VIS, "15:00〜15:45（選んだ日）", "15:00–15:45 (if chosen)"),
            photos=W("takasago")),
        dict(
            id="miura", name=T("三浦綾子記念文学館と外国樹種見本林（みうらあやこ・みほんりん）", "Miura Ayako Literature Museum & the Arboretum"),
            kind=T("文学館・森", "Museum & forest"),
            blurb=T("駅の南、川を渡った先のまっすぐな森。小説『氷点』の舞台。", "A straight-trunked forest across the river south of the station, the setting of the novel Hyoten."),
            caution=T("月曜休館（7・8月は毎日開館）。入館は16:30まで", "Closed Mondays (open daily in Jul–Aug). Last entry 16:30"),
            lat=43.75361, lng=142.34797,
            body=T(
                "旭川で生まれ育った作家・三浦綾子（1922〜1999）の文学館。代表作『氷点（ひょうてん）』の舞台になった見本林の入口に建っています。\n\n"
                "見本林は、外国の木が北海道で育つかを確かめるために1898年（明治31年）に植えられた森で、ストローブマツやヨーロッパカラマツなど約30種がまっすぐ空へ伸びています。森の中の道は、文学館に入らなくても歩けます。冬は雪の森になります。\n\n"
                "旭川駅の東口から、氷点橋で忠別川を渡って突き当たりまで、歩いて約20分。タクシーなら約3分です。"
                + ("動物園のあとに行くなら、14:54に駅に戻ってそのまま歩き、明るいうちに森を見てから文学館へ（16:30までに入館）。酒蔵のかわりに選ぶ場所です。"
                   if w else
                   "動物園のあとに行くなら、14:23に駅に戻ってそのまま歩き、15:00ごろに着きます。男山のかわりに選ぶ場所です。森は夏でも涼しく、秋は木の葉が色づきます。"),
                "A museum for Miura Ayako (1922–1999), the novelist born and raised in Asahikawa. It stands at the entrance to the forest where her best-known novel, Hyoten (Freezing Point), is set.\n\n"
                "The forest was planted in 1898 to test whether foreign trees would grow in Hokkaido: about 30 species, including white pine and European larch, rising dead straight. You can walk the forest paths without entering the museum. In winter it is a forest in snow.\n\n"
                "From the east exit of Asahikawa Station, cross the Chubetsu River by Hyoten Bridge and keep on to the end of the road: about 20 minutes on foot, or about three by taxi. "
                + ("After the zoo, walk straight here from the station (back at 14:54), see the forest while it is light, then go into the museum (last entry 16:30). Choose it instead of the sake brewery."
                   if w else
                   "After the zoo, walk straight here from the station (back at 14:23) to arrive at about 15:00. Choose it instead of Otokoyama. The forest stays cool in summer and turns colour in autumn.")),
            gmaps=[gm("三浦綾子記念文学館", "Miura Ayako Literature Museum", 43.75361, 142.34797, "三浦綾子記念文学館"),
                   gm("氷点橋", "Hyoten Bridge", 43.76049, 142.35841, "氷点橋 旭川")],
            links=[link("official", "三浦綾子記念文学館 ご利用案内", "Miura Ayako Literature Museum: visitor information (Japanese)", U["miura"]),
                   link("info", "外国樹種見本林（旭川観光コンベンション協会）", "The arboretum (Asahikawa tourism association, Japanese)", U["forest"])],
            notices=[N_MIURA_CLOSED],
            rows=[row("hours", "9:00〜17:00（最終入館16:30）", "9:00–17:00 (last entry 16:30)"),
                  row("closed", "9月1日〜6月30日の月曜（祝日でも）、12月28日〜1月5日", "Mondays from 1 Sept to 30 June (even on holidays); 28 Dec – 5 Jan"),
                  row("fee", "大人700円、学生300円、小中高生は無料。カード・交通系ICも使えます", "Adults ¥700, students ¥300, school pupils free. Cards and transport IC cards accepted"),
                  row("walk", "旭川駅東口から歩いて約20分。タクシー約3分", "About 20 min on foot from the station’s east exit; about 3 min by taxi")],
            tip=T("時間・休み・料金・道順は三浦綾子記念文学館の公式サイト、見本林の説明は旭川観光コンベンション協会のページで確認しました。館内の英語の案内がどのくらいあるかは確かめられていません。",
                  "Hours, closing days, fees and directions from the museum’s website; the forest from the Asahikawa tourism association. How much English there is inside the museum could not be confirmed."),
            time=(VIS, "15:15〜16:45（選んだ日）", "15:15–16:45 (if chosen)") if w else (VIS, "15:00〜16:30（選んだ日）", "15:00–16:30 (if chosen)"),
            photos=W("miura")),
        dict(
            id="kaimono", name=T("平和通買物公園と旭川ラーメン（へいわどおりかいものこうえん）", "Heiwa-dori Kaimono Koen mall & Asahikawa ramen"),
            kind=T("歩行者の通り・ラーメン", "Pedestrian street & ramen"),
            blurb=T("駅前から約1km続く、車の入らない通り。しょうゆのラーメンを1杯。", "A car-free street running about 1 km from the station. Stop for a bowl of soy-sauce ramen."),
            lat=43.76680, lng=142.35940,
            body=T(
                "旭川駅の正面から8条通まで約1km、まっすぐ北へ続く歩行者だけの通りです。1972年にできた、日本で最初の恒久的な歩行者専用道路。店や喫茶店が両側に並んでいます。\n\n"
                "旭川ラーメンは、しょうゆ味が基本。スープの表面をラードの膜がおおっていて、寒い日でも冷めにくいのが特徴です。この通りと、すぐ横の通りに本店が2つあります。\n"
                "・梅光軒（ばいこうけん）旭川本店：2条8丁目、買物公園に面したピアザビルの地下1階。11:00〜15:30と17:00〜21:00、不定休。\n"
                "・らーめん山頭火（さんとうか）旭川本店：1条通8丁目。11:00〜22:00（ラストオーダー21:30）、木曜休み。午後も通しで開いています。\n\n"
                + ("髙砂酒造から歩いて戻ると16:20ごろ。もう暗くなっています。店をのぞきながら北へ歩いて、17:00に夜の営業が始まる梅光軒か、通しで開いている山頭火へ。動物園でお昼を軽くした日は、駅に戻ってすぐ（15:00ごろ）山頭火で遅いお昼にする手もあります。"
                   if w else
                   "男山からのバスを1条8丁目で降りると16:54。山頭火はバス停のすぐ近く、梅光軒は1本北の2条です（夜の営業は17:00から）。早めの晩ごはんにラーメンを食べて、通りを北へ歩いて常磐公園へ向かいます。日の長い季節は、先に公園へ行って、ラーメンを夜のしめにしてもかまいません。"),
                "A pedestrian-only street running dead straight for about 1 km, from the front of Asahikawa Station north to Hachijo-dori. Opened in 1972, it was Japan’s first permanent pedestrian street. Shops and cafés line both sides.\n\n"
                "Asahikawa ramen is soy-sauce based, with a film of lard on top that keeps the soup hot on cold days. Two well-known shops have their main branches on or just off this street:\n"
                "• Baikohken, main shop: 2-jo 8-chome, basement of the Piazza Building facing the mall. 11:00–15:30 and 17:00–21:00, irregular closing days.\n"
                "• Ramen Santouka, main shop: 1-jo-dori 8-chome. 11:00–22:00 (last order 21:30), closed Thursdays. Open straight through the afternoon.\n\n"
                + ("Walking back from Takasago you reach the mall at about 16:20, already dark. Browse your way north, then eat at Baikohken when it reopens at 17:00, or at Santouka, which is open all afternoon. If lunch at the zoo was light, you could also have a late ramen lunch at Santouka as soon as you are back at the station (about 15:00)."
                   if w else
                   "The bus from Otokoyama drops you at 1-jo 8-chome at 16:54. Santouka is right by the stop; Baikohken is one block north at 2-jo (evening opening from 17:00). Have ramen as an early dinner, then walk north up the mall to Tokiwa Park. In the long days of summer you can go to the park first and leave the ramen for the end of the night.")),
            gmaps=[gm("平和通買物公園", "Heiwa-dori Kaimono Koen", 43.76680, 142.35940, "平和通買物公園 旭川"),
                   gm("梅光軒 旭川本店", "Baikohken main shop", 43.76560, 142.35905, "梅光軒 旭川本店"),
                   gm("らーめん山頭火 旭川本店", "Ramen Santouka main shop", 43.76455, 142.35985, "らーめん山頭火 旭川本店")],
            links=[link("info", "旭川平和通買物公園", "Kaimono Koen mall (Japanese)", U["kaimono"]),
                   link("official", "梅光軒 店舗一覧", "Baikohken shops (Japanese)", U["baiko"], "https://baikohken.com/en"),
                   link("official", "らーめん山頭火 店舗案内", "Ramen Santouka shops (Japanese)", U["santouka"])],
            notices=([N_FES] if w else []),
            rows=[row("hours", "梅光軒 旭川本店：11:00〜15:30（L.O.15:00）、17:00〜21:00（L.O.20:30）、不定休", "Baikohken main shop: 11:00–15:30 (last order 15:00), 17:00–21:00 (last order 20:30), irregular closing days"),
                  row("hours", "らーめん山頭火 旭川本店：11:00〜22:00（L.O.21:30）、木曜休み（祝日は営業）。スープがなくなると早く閉まります", "Ramen Santouka main shop: 11:00–22:00 (last order 21:30), closed Thursdays (open if a holiday). Closes early if the soup runs out")],
            tip=T("通りの歴史は旭川平和通商店街振興組合のページ、店の時間はそれぞれの公式サイトで確認しました。支払い方法と英語のメニューがあるかは、公式サイトに書かれていません（要確認）。現金を持っていくと安心です。",
                  "The street’s history is from the shopping street association’s page; shop hours from each official website. Payment methods and English menus are not stated on the websites (please check): carrying cash is safest."),
            time=(VIS, "16:20〜17:50", "16:20–17:50") if w else (VIS, "16:54〜17:45", "16:54–17:45"),
            photos=W("kaimono")),
        dict(
            id="tokiwa", name=T("常磐公園と旭橋（ときわこうえん・あさひばし）", "Tokiwa Park & Asahibashi Bridge"), kind=T("公園・橋", "Park & bridge"),
            blurb=T("買物公園の先の池のある公園と、石狩川にかかる1932年のアーチ橋。", "A park with ponds beyond the mall, and a 1932 arch bridge over the Ishikari River."),
            lat=43.77530, lng=142.35786,
            body=T(
                "常磐公園は1910年（明治43年）にできた、旭川で最初の公園です。買物公園の北の端から歩いて5分ほど。池が2つあり、まわりをニレやポプラの大きな木が囲んでいます。雪のない季節は手こぎのボートが出ます。公園の中に北海道立旭川美術館があります（9:30〜17:00、月曜休み）。\n\n"
                "公園の北の土手を上がると石狩川。右手に見えるアーチが旭橋です。1932年（昭和7年）に完成した長さ225mの鉄の橋で、1956年までは路面電車が橋の上を走っていました。旭川のしるしになっている橋で、北海道遺産に選ばれています。\n\n"
                + ("冬は池が凍って雪におおわれ、土手は風が冷たいので、時間割には入れていません。行くなら明るい時間に、動物園を早めに出て。2月の旭川冬まつりのときは、ここと旭橋のそばの河畔が会場になります。"
                   if w else
                   "ラーメンのあと、買物公園を北へ歩いて18:00ごろ着きます。池のまわりを歩いて、土手から夕方の光の旭橋を見るのがこのコースの順番です。日の入りは6〜7月が19時ごろ、8月の終わりは18時すぎ、9月の終わりは17時15分ごろ、10月の終わりは16時半前。9月からはラーメンをあとにして、男山から戻ったらまっすぐここへ来てください。"),
                "Tokiwa Park, opened in 1910, was Asahikawa’s first park. It is about five minutes’ walk from the north end of the Kaimono Koen mall, with two ponds ringed by big elms and poplars, and rowing boats outside the snow season. The Hokkaido Asahikawa Museum of Art stands inside the park (9:30–17:00, closed Mondays).\n\n"
                "Climb the embankment on the park’s north side and you are at the Ishikari River. The arches to your right are Asahibashi, a 225-metre steel bridge completed in 1932; trams crossed it until 1956. It is the symbol of the city and a designated Hokkaido Heritage site.\n\n"
                + ("In winter the ponds freeze under snow and the wind on the embankment is bitter, so this stop is not in the winter timetable. If you go, go in daylight by leaving the zoo early. During the Winter Festival in February, this park and the riverbank by the bridge are the main venue."
                   if w else
                   "After ramen, walk north up the mall to arrive at about 18:00. Stroll round the ponds, then see the bridge in evening light from the embankment. Sunset is around 19:00 in June and July, just after 18:00 at the end of August, about 17:15 at the end of September and just before 16:30 at the end of October: from September, come straight here after Otokoyama and eat afterwards.")),
            gmaps=[gm("常磐公園", "Tokiwa Park", 43.77530, 142.35786, "常磐公園 旭川"),
                   gm("旭橋", "Asahibashi Bridge", 43.77846, 142.36017, "旭橋 旭川"),
                   gm("北海道立旭川美術館", "Hokkaido Asahikawa Museum of Art", 43.77413, 142.35542, "北海道立旭川美術館")],
            links=[link("info", "常磐公園（旭川観光コンベンション協会）", "Tokiwa Park (Asahikawa tourism association, Japanese)", U["tokiwa"]),
                   link("info", "旭橋（旭川観光コンベンション協会）", "Asahibashi Bridge (Asahikawa tourism association, Japanese)", U["asahibashi"]),
                   link("official", "北海道立旭川美術館 開館時間・観覧料", "Hokkaido Asahikawa Museum of Art (English page)", U["museum"], "https://artmuseum.pref.hokkaido.lg.jp/abj/english"),
                   link("official", "旭川冬まつり", "Asahikawa Winter Festival (Japanese)", U["winfes"])],
            notices=[N_FES],
            rows=[row("hours", "公園はいつでも入れます", "The park is always open"),
                  row("hours", "北海道立旭川美術館：9:30〜17:00（入場は16:30まで）、月曜休み（祝日は開いて翌火曜休み）、12月29日〜1月3日休み。観覧料は展覧会ごと", "Museum of Art: 9:30–17:00 (last entry 16:30), closed Mondays (open on holiday Mondays, closed the next day) and 29 Dec – 3 Jan. Fees vary by exhibition"),
                  row("walk", "旭川駅から買物公園を通って歩いて約20分。5・7小路ふらりーとまで約10分", "About 20 min on foot from the station via the mall; about 10 min on to Furarito alley")],
            tip=T("公園と橋の説明は旭川観光コンベンション協会、美術館は公式サイト、冬まつりは公式サイトで確認しました。ボートの期間と料金は確かめられていません（要確認）。",
                  "The park and bridge are described from the Asahikawa tourism association’s pages; the museum and the Winter Festival from their official websites. The boat season and price could not be confirmed (please check)."),
            time=(VIS, "明るい時間に（選んだ日）", "In daylight (if chosen)") if w else (VIS, "18:00〜19:00", "18:00–19:00"),
            photos=W("tokiwa")),
        dict(
            id="furari", name=T("5・7小路ふらりーと（ごーななこうじ）", "Furarito alley (5-jo 7-chome)"), kind=T("飲み屋の小路・晩ごはん", "Food alley & dinner"),
            blurb=T("焼き鳥の煙が流れる細い小路。旭川の名物「新子焼き」をここで。", "A narrow alley of yakitori smoke. Try Asahikawa’s shinko-yaki grilled young chicken here."),
            caution=T("ぎんねこは月曜休み・予約不可", "Ginneko: closed Mondays, no bookings"),
            lat=43.76987, lng=142.36085,
            body=T(
                "5条通7丁目にある、幅3mほどの小路です。戦前は魚と野菜の市場で、そのあと焼き鳥の店が増えて「焼き鳥横丁」と呼ばれてきました。いまも焼き鳥、ラーメン、居酒屋など18軒ほどが並んでいます。冬は、店の前に氷のキャンドルが灯ります。\n\n"
                "旭川の名物「新子焼き（しんこやき）」は、若鶏の半身を炭火で焼いたもの。たれか塩を選びます。小路の中の焼鳥専門ぎんねこは1950年（昭和25年）創業で、13:00から22:00まで通しで開いています（月曜休み）。席の予約はできないので、混んでいたら小路のほかの店をのぞいて、あとで戻るのがよいでしょう。公式サイトに英語のページがあります。\n\n"
                + ("買物公園から歩いて5分。18:00ごろに入って、20時半ごろまで。ホテルが駅のまわりなら、歩いて10〜15分で帰れます。凍った道を歩くので、飲みすぎないように。"
                   if w else
                   "常磐公園から歩いて約10分。19:10ごろに入って、21時ごろまで。ホテルが駅のまわりなら、歩いて10〜15分で帰れます。"),
                "An alley about three metres wide at 5-jo-dori 7-chome. Before the war it was a fish and vegetable market; yakitori shops moved in afterwards and it became known as “Yakitori Alley”. Around 18 places still line it: yakitori, ramen, izakaya. In winter, ice candles are lit outside the shops.\n\n"
                "Asahikawa’s local dish is shinko-yaki: half a young chicken grilled over charcoal, with sauce or salt. Ginneko, a yakitori shop in the alley since 1950, is open straight through from 13:00 to 22:00 (closed Mondays). It does not take table bookings, so if it is full, look into the other places and come back. Its website has an English page.\n\n"
                + ("Five minutes’ walk from the mall. Go in at about 18:00 and stay until 20:30 or so. Hotels around the station are 10–15 minutes’ walk away. You will be walking back on ice, so go easy on the drink."
                   if w else
                   "About ten minutes’ walk from Tokiwa Park. Go in at about 19:10 and stay until 21:00 or so. Hotels around the station are 10–15 minutes’ walk away.")),
            gmaps=[gm("5・7小路ふらりーと", "Furarito alley", 43.76987, 142.36085, "5・7小路ふらりーと"),
                   gm("焼鳥専門ぎんねこ", "Yakitori Ginneko", 43.76990, 142.36075, "焼鳥専門ぎんねこ 旭川")],
            links=[link("info", "5・7小路ふらりーと（旭川観光コンベンション協会）", "Furarito alley (Asahikawa tourism association, Japanese)", U["furari"]),
                   link("official", "焼鳥専門ぎんねこ", "Yakitori Ginneko (has an English page)", U["ginneko"])],
            notices=[N_GINNEKO],
            rows=[row("hours", "焼鳥専門ぎんねこ：13:00〜22:00、月曜休み（ほかに臨時の休みあり）。席の予約は不可", "Yakitori Ginneko: 13:00–22:00, closed Mondays (plus occasional extra days). No table bookings"),
                  row("hours", "ほかの店の時間と休みは店ごとに違います", "Hours and closing days of the other shops vary"),
                  row("walk", "旭川駅から買物公園を通って歩いて約12分", "About 12 min on foot from Asahikawa Station via the mall")],
            tip=T("小路の説明は旭川観光コンベンション協会、ぎんねこの時間は公式サイトで確認しました。値段と支払い方法は公式サイトに書かれていません（要確認）。小さな店が多いので、現金を持っていってください。",
                  "The alley is described from the Asahikawa tourism association’s page; Ginneko’s hours from its website. Prices and payment methods are not stated there (please check). Most places are small: bring cash."),
            time=(VIS, "18:00〜20:30", "18:00–20:30") if w else (VIS, "19:10〜21:00", "19:10–21:00"),
            photos=W("furari")),
        dict(
            id="kaeri", name=T("旭川駅（帰り）", "Asahikawa Station (return)"), kind=T("駅", "Station"),
            blurb=T("札幌へ帰る人は21:00発で22:25着。最終は22:00発。", "For Sapporo: the 21:00 arrives 22:25. The last train leaves at 22:00."),
            lat=43.76275, lng=142.35793,
            body=T(
                "旭川に泊まる人は、ふらりーとから歩いてホテルへ。札幌へ帰る人は、ふらりーとから駅まで歩いて12分ほどです。\n\n"
                "札幌行きの特急は、20:00発（カムイ42号、21:25着）、21:00発（ライラック44号、22:25着）、最終が22:00発（ライラック46号、23:25着）。全部の席が指定席なので、朝のうちに帰りの指定席券も取っておくと安心です。"
                + ("\n\n冬は雪で遅れたり運休したりすることがあります。日帰りの日は最終の1本前までに乗るつもりで、晩ごはんの前に運行情報を見てください。" if w else ""),
                "Staying in Asahikawa? Walk back to your hotel from Furarito. Heading to Sapporo? The station is about 12 minutes’ walk from the alley.\n\n"
                "Limited expresses to Sapporo leave at 20:00 (Kamui 42, arriving 21:25), 21:00 (Lilac 44, arriving 22:25) and, last of the day, 22:00 (Lilac 46, arriving 23:25). All seats are reserved, so it is safest to get your return seat in the morning."
                + ("\n\nIn winter, snow can delay or cancel trains. On a day trip, plan to be on the train before the last one, and check the service status before dinner." if w else "")),
            gmaps=[gm("JR旭川駅", "JR Asahikawa Station", 43.76275, 142.35793, "JR旭川駅")],
            links=[JR, JRPASS],
            notices=([N_SNOW_JR] if w else []),
            rows=[row("train", "旭川20:00 → 札幌21:25（特急カムイ42号）、21:00 → 22:25（特急ライラック44号）。平日・土曜とも", "Asahikawa 20:00 → Sapporo 21:25 (Kamui 42); 21:00 → 22:25 (Lilac 44). Weekdays and Saturdays"),
                  row("train", "最終：旭川22:00 → 札幌23:25（特急ライラック46号）", "Last train: Asahikawa 22:00 → Sapporo 23:25 (Lilac 46)"),
                  row("fee", "片道5,440円（乗車券3,080円＋指定席2,360円）。全席指定", "¥5,440 each way (fare ¥3,080 + reserved seat ¥2,360). All seats reserved"),
                  row("pay", "北海道レールパスで乗れます（指定席券を先に受け取る）", "Covered by the Hokkaido Rail Pass (collect a seat reservation first)")],
            tip=T("時刻と運賃は乗換案内で2026年12月3日（木）・5日（土）を確認しました。JR北海道は2027年3月にダイヤ改正の予定なので、春からは時刻が変わることがあります。",
                  "Times and fares checked in a route planner for Thu 3 and Sat 5 December 2026. JR Hokkaido usually revises its timetable in March, so times may change from spring 2027."),
            time=(DEP, "札幌へは21:00発（最終は22:00発）", "For Sapporo: the 21:00 (last train 22:00)"),
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


def build(c):
    w = c == "winter"
    S = spots(c)
    N = {s["id"]: i for i, s in enumerate(S, 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
    if w:
        default = ns("zoo", "takasago", "kaimono", "furari")
        hints = [
            h("otoko", {"any": ns("otoko"), "none": ns("takasago", "miura")},
              "男山を選んだ日は、動物園を1本早い13:40のバスで出て駅に14:27。1条8丁目14:40発のバスで永山2条6丁目15:09。帰りは16:29発で1条8丁目16:54、そのまま買物公園へ。",
              "With Otokoyama: leave the zoo one bus earlier, on the 13:40 (station 14:27), then take the 14:40 bus from 1-jo 8-chome (Nagayama 2-jo 6-chome 15:09). Come back on the 16:29, reaching 1-jo 8-chome at 16:54, right by the mall."),
            h("otoko", {"any": ns("otoko"), "andAny": ns("takasago", "miura")},
              "動物園のあとの午後は2時間ほどです。男山・髙砂酒造・文学館は、どれか1つにしてください。",
              "There are only about two hours after the zoo: choose just one of Otokoyama, Takasago and the literature museum."),
            h("miura", {"any": ns("miura"), "none": ns("otoko")},
              "文学館を選んだ日は、14:54に駅に着いたら東口から歩いて約20分。明るいうちに見本林を歩いて、16:30までに入館。帰りは暗いので、タクシー（約3分）が楽です。",
              "With the literature museum: from the station (14:54) walk about 20 minutes from the east exit, see the forest while it is light and enter by 16:30. It will be dark afterwards: a taxi back (about 3 minutes) is easier."),
            h("takasago", {"any": ns("takasago"), "andAny": ns("miura")},
              "髙砂酒造と文学館の両方は、冬の午後には入りません。どちらか1つに。",
              "Takasago and the literature museum do not both fit into a winter afternoon: choose one."),
            h("tokiwa", {"any": ns("tokiwa")},
              "冬に常磐公園と旭橋へ行くなら、動物園を13:10のバス（旭川駅13:54着）で出て、買物公園を北へ歩いて14:20ごろ。16時には暗くなります。酒蔵はやめるか、15:30ごろに髙砂酒造へ。",
              "For Tokiwa Park and the bridge in winter, leave the zoo on the 13:10 bus (Asahikawa Station 13:54) and walk north up the mall to arrive at about 14:20. It is dark by 16:00. Skip the brewery, or reach Takasago at about 15:30."),
            h("kaimono", {"none": ns("zoo")},
              "動物園に行かない日は、午前に男山（1条8丁目からバスで約30分）、お昼に買物公園でラーメン、午後に文学館と見本林か髙砂酒造、という回り方ができます。",
              "Without the zoo: Otokoyama in the morning (about 30 minutes by bus from 1-jo 8-chome), ramen on the mall for lunch, then the literature museum and forest or Takasago in the afternoon."),
        ]
        sections = [
            {"first": 1, "last": 2, "area": T("旭山動物園", "Asahiyama Zoo"), "title": T("9:40のバスで動物園へ。11:00にペンギンの散歩", "The 9:40 bus to the zoo; penguins walk at 11:00")},
            {"first": 3, "last": 5, "area": T("午後に1つ", "One for the afternoon"), "title": T("駅に戻って、酒蔵か、雪の森の文学館", "Back in town: a sake brewery, or the museum in a snowy forest")},
            {"first": 6, "last": 9, "area": T("旭川の町・夜", "Town · evening"), "title": T("暗くなったら買物公園、ラーメン、焼き鳥の小路", "After dark: the mall, ramen and the yakitori alley")},
        ]
        note = ("冬（動物園の冬期開園 11/11〜4/7）。旭川駅9:40のバス→旭山動物園10:22〜14:10→髙砂酒造→買物公園・ラーメン→5・7小路ふらりーと。"
                "男山・文学館・常磐公園は選んだ日だけ。")
    else:
        default = ns("zoo", "otoko", "kaimono", "tokiwa", "furari")
        hints = [
            h("otoko", {"any": ns("otoko"), "andAny": ns("takasago", "miura")},
              "動物園のあとの午後は、男山・髙砂酒造・文学館のうち1つ（多くて近くの2つ：髙砂酒造と文学館はどちらも駅から歩けます）にしてください。男山はバスで往復1時間かかります。",
              "After the zoo, choose one of Otokoyama, Takasago and the literature museum (or at most the two near the station: Takasago and the museum are both walkable). Otokoyama takes an hour on the bus there and back."),
            h("takasago", {"any": ns("takasago"), "none": ns("otoko")},
              "髙砂酒造を選んだ日は、14:23に駅に着いたら宮下通を東へ歩いて15分。16:00ごろ買物公園に戻れば、あとは時間割どおりです。",
              "With Takasago: from the station (14:23) walk 15 minutes east along Miyashita-dori. Be back on the mall by about 16:00 and the rest of the timetable holds."),
            h("miura", {"any": ns("miura"), "none": ns("otoko")},
              "文学館を選んだ日は、14:23に駅に着いたら東口から歩いて約20分。16:30ごろ出て、買物公園へ戻ります。月曜は休み（7・8月は開館）。",
              "With the literature museum: from the station (14:23) walk about 20 minutes from the east exit. Leave at about 16:30 and head back to the mall. Closed Mondays (open daily in July and August)."),
            h("zoo", {"any": ns("zoo"), "none": ns("otoko", "takasago", "miura")},
              "午後に酒蔵も文学館も入れない日は、動物園に16時ごろまでいられます。帰りのバスは15:40発（16:28着）や16:10発（16:55着）。",
              "With no brewery or museum in the afternoon you can stay at the zoo until about 16:00. Return buses include the 15:40 (arriving 16:28) and the 16:10 (arriving 16:55)."),
            h("kaimono", {"none": ns("zoo")},
              "動物園に行かない日は、午前に文学館と見本林、お昼に買物公園でラーメン、午後に男山、夕方に常磐公園と旭橋、という回り方ができます。",
              "Without the zoo: the literature museum and forest in the morning, ramen on the mall for lunch, Otokoyama in the afternoon, then Tokiwa Park and the bridge towards evening."),
        ]
        sections = [
            {"first": 1, "last": 2, "area": T("旭山動物園", "Asahiyama Zoo"), "title": T("朝のバスで動物園へ。混む前に人気の館を", "The morning bus to the zoo, before the crowds")},
            {"first": 3, "last": 5, "area": T("午後に1つ", "One for the afternoon"), "title": T("酒蔵か、森の中の文学館", "A sake brewery, or the museum in the forest")},
            {"first": 6, "last": 9, "area": T("旭川の町・夕方と夜", "Town · evening"), "title": T("買物公園でラーメン、夕方の旭橋、焼き鳥の小路", "Ramen on the mall, the bridge at dusk, the yakitori alley")},
        ]
        note = ("雪のない季節（動物園の夏期開園 4/29〜11/3）。旭川駅9:10のバス→旭山動物園9:49〜13:40→男山→買物公園・ラーメン→常磐公園と旭橋→5・7小路ふらりーと。"
                "髙砂酒造・文学館は選んだ日だけ。")
    data = {
        "id": "asahikawa", "course": "early" if w else "late",
        "_note": "旭山動物園と旭川の町（asahikawa/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "写真はすべて Wikimedia Commons（一覧は scripts/asahikawa_web_photos.json）。info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。"
                   "このファイルは scripts/build_asahikawa_data.py で作る（直接直さない）。",
        "sections": sections,
        "focus": {"first": 6, "last": 9},
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。旭川駅（出発・帰り）はいつも入る。",
                 "defaultMode": "pick", "picks": ns("zoo", "otoko", "takasago", "miura", "kaimono", "tokiwa", "furari"),
                 "defaultPicks": default,
                 "auto": {str(N["eki"]): {"always": True}, str(N["kaeri"]): {"always": True}},
                 "hints": hints},
        "photoBase": "../images/asahikawa/", "sources": SOURCES,
        "spots": [spot(i, s) for i, s in enumerate(S, 1)],
    }
    name = "asahikawa-winter.json" if w else "asahikawa.json"
    with open(f"{R}/data/routes/{name}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", name, [(s["no"], s["id"], len(s["photos"])) for s in data["spots"]])


build("winter")
build("summer")
