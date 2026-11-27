#!/usr/bin/env python3
"""余市（札幌から日帰り）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_yoichi_data.py   （そのあと python3 scripts/sync_yoichi.py）
- data/routes/yoichi.json         … late ＝4月中旬〜12月中旬。蒸溜所（予約）→ワイナリー→福原漁場→運上家→モイレの浜→温泉→晩ごはん（9か所）
- data/routes/yoichi-winter.json  … early＝冬（12月中旬〜4月上旬）。漁場・運上家・博物館が閉まるので、蒸溜所→ワイナリー→浜→温泉→晩ごはん（7か所）
  （late / early はコース切り替えの仕組みの名前を借りているだけ。どちらも札幌8:41発。どちらで開くかは日付で決める＝scripts/sync_yoichi.py）
- 起点は札幌駅〜大通〜すすきののホテル（北海道のマップの決まり、2026-11-26）。だれかが行った・食べたことは書かない（写真は全部 Wikimedia Commons）
- 文章・料金・時刻・出典（SOURCES）はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの時間割（pre）→ 共通の説明（body）→ おすすめの時間」の順に組み立てる
- JR の時刻は乗換案内の2026年12月3日（木）・5日（土）のダイヤ。JR北海道のダイヤ改正（春）のあとは確かめ直す
- 高速バスは北海道中央バスの公式時刻表（夏ダイヤ＝2026年7月1日更新、冬ダイヤ＝2026年12月11日改正）
- ニッカの予約サイト（reserva.be）と公式サイトは、2026-11-27 には自動の確認画面・アクセス拒否で開けなかった。
  蒸溜所の内容は小樽のマップの担当が2026-11-26に確かめたもの（scripts/build_otaru_data.py の SOURCES）を使っている
- 文化財施設（福原漁場・運上家・水産博物館・フゴッペ洞窟）の2027年の開館日が出たら、notices と sync_yoichi.py の WINTER_TO を直す
- 写真は images/yoichi/<スポットのid>-w<番号>.jpg（Wikimedia Commons。一覧は scripts/yoichi_web_photos.json）。
  札幌駅・余市駅・ニッカの写真は小樽のマップ（images/otaru/）と同じもの。
  あとでオーナーの写真を <スポットのid>-<番号>.jpg で入れるときは、PHOTOS の先頭にファイル名を足す
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/yoichi"
CHECKED = "2026-11-27"
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


def kk(name):
    """余市観光協会の飲食店のページ"""
    return "https://yoichi-kankoukyoukai.com/spot_food/" + urllib.parse.quote(name) + "/"


WEB = json.load(open(f"{R}/scripts/yoichi_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x) for x in WEB.get(sid, [])]
# オーナーの写真が入ったら、ここで W(...) の前にファイル名を足す（例: "fuku": ["fuku-1.jpg"] + W("fuku")）
PHOTOS = {k: W(k) for k in ("sapporo", "eki", "nikka", "winery", "fuku", "unjo", "moire", "onsen", "kaeri")}

D1, D2 = "2026-12-03", "2026-12-05"     # 乗換案内で確かめた日：木曜と土曜
TB = "https://www.town.yoichi.hokkaido.jp"
U = dict(
    nikka="https://www.nikka.com/distilleries/yoichi/visit/", nikka_faq="https://www.nikka.com/distilleries/yoichi/faq/",
    nikka_en="https://www.nikka.com/en/distilleries/yoichi/", nikka_book="https://reserva.be/nikkayoichi/",
    nikka_news="https://reserva.be/nikkayoichi/news",
    nikka_dec="https://reserva.be/nikkayoichi/news?search_osh_no=60883&mode=list_detail",
    win_rest="https://nipponseishu.co.jp/yoichiwine/restaurant/", win_cafe="https://nipponseishu.co.jp/yoichiwine/cafe/",
    win_top="https://nipponseishu.co.jp/yoichiwine/", win_news="https://nipponseishu.co.jp/yoichiwine/news/",
    win_1011="https://nipponseishu.co.jp/yoichiwine/news/%e4%bd%99%e5%b8%82%e3%83%af%e3%82%a4%e3%83%8a%e3%83%aa%e3%83%bc%e5%96%b6%e6%a5%ad%e6%99%82%e9%96%93%e3%81%ae%e3%81%8a%e7%9f%a5%e3%82%89%e3%81%9b%e3%80%9010%e6%9c%88%e3%80%8111%e6%9c%88%e3%80%91-4/",
    occi="https://www.occigabi.net/access", occi_taste="https://www.occigabi.net/wine-tasting",
    unjo=f"{TB}/machi/syoukai/yoichiunzyouya.html", fuku=f"{TB}/machi/syoukai/fukuharagyoba.html",
    fugoppe=f"{TB}/machi/syoukai/fugoppe.html", museum=f"{TB}/kurashi/kurashinojouhou/kyouiku-bunka/bunkazai-kaikan.html",
    shiripa=f"{TB}/machi/syoukai/bunnkazai-siripa.html", rousoku=f"{TB}/machi/syoukai/bunnkazai-rousokuiwa.html",
    onsen="https://yoichigawa.com/", onsen_bath="https://yoichigawa.com/free/ohuro", onsen_about="https://yoichigawa.com/about",
    dome="https://www.spacedome.jp/",
    kk_notice="https://yoichi-kankoukyoukai.com/2026/11/07/%f0%9f%93%a2%e3%80%90%e5%96%b6%e6%a5%ad%e6%99%82%e9%96%93%e3%83%bb%e5%ae%9a%e4%bc%91%e6%97%a5%e5%a4%89%e6%9b%b4%e3%81%ae%e3%81%8a%e7%9f%a5%e3%82%89%e3%81%9b%e3%80%91/",
    kk_food="https://yoichi-kankoukyoukai.com/food/", kk_en="https://yoichi-kankoukyoukai.com/english-page/",
    kakizaki=kk("柿崎商店-海鮮工房"), banya=kk("回転寿司　余市番屋"), midoriya=kk("みどりや"),
    hw_summer="https://www.chuo-bus.co.jp/highway/?t=39&ope=list&o=1",
    hw_winter="https://www.chuo-bus.co.jp/highway/pocket.20261211/pdf/iwanai.pdf",
    hw_index="https://www.chuo-bus.co.jp/highway/pocket.20261211/",
    bus_yoichi="https://www.chuo-bus.co.jp/city_route/course/yoichi/",
    locker="https://www.jrhokkaido.co.jp/network/locker/locker.pdf",
    railpass="https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html",
    jr_info="https://www3.jrhokkaido.co.jp/webunkou/",
    sun_dec="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s0012.html", sun_jan="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0001.html",
    sun_feb="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0002.html", sun_mar="https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s0003.html",
    otaru_map="../otaru/",
)

# 出典。what＝何を確かめたか、saw＝そのページで見た内容、checked＝確かめた日
SOURCES = [dict(what=a, url=b, saw=c, checked=d) for a, b, c, d in [
    ("札幌→余市 平日", q("札幌", "余市", D1, "08:30"), "8:41→小樽（9:36発の倶知安行きに乗り換え）→余市10:00、1,380円。次は10:06→余市11:23", CHECKED),
    ("札幌→余市 土曜", q("札幌", "余市", D2, "08:30"), "平日と同じ（8:41→余市10:00、10:06→11:23）", CHECKED),
    ("すすきの→札幌（地下鉄）", q("すすきの", "札幌", D1, "08:20"), "南北線 すすきの8:22→さっぽろ8:27、210円", CHECKED),
    ("余市→札幌 夕方 平日", q("余市", "札幌", D1, "17:30"), "17:42→札幌19:07、18:35→19:58", CHECKED),
    ("余市→札幌 夕方 土曜", q("余市", "札幌", D2, "17:30"), "平日と同じ", CHECKED),
    ("余市→札幌 夜 平日", q("余市", "札幌", D1, "19:00"), "19:26→（小樽19:56発）→札幌20:41、20:19→21:44、1,380円", CHECKED),
    ("余市→札幌 夜 土曜", q("余市", "札幌", D2, "19:00"), "平日と同じ", CHECKED),
    ("余市→札幌 最終 平日", q("余市", "札幌", D1, "23:59", "l"), "21:28→22:44、最終22:26→23:53", CHECKED),
    ("余市→札幌 最終 土曜", q("余市", "札幌", D2, "23:59", "l"), "平日と同じ", CHECKED),
    ("余市→小樽 夕方 平日", q("余市", "小樽", D1, "17:30"), "17:42→小樽18:08、18:35→19:02、470円（土曜も同じ）", CHECKED),
    ("高速バス 札幌→余市（夏ダイヤ）", U["hw_summer"], "2026年7月1日更新（夏ダイヤ）。札幌駅前9:05（岩内行き）→小樽駅前10:14→余市駅前十字街10:44。札幌駅前→余市駅前十字街 片道1,290円・往復2,420円。運賃は降車時、ICカード可", CHECKED),
    ("高速バス 冬ダイヤ（2026年12月11日改正）", U["hw_winter"], "札幌駅前9:05→小樽駅前10:19→余市駅前十字街10:50。札幌⇔余市駅前 片道1,290円・往復2,420円。12/29・30は土日祝ダイヤ、12/31〜1/3は運休便が多数", CHECKED),
    ("中央バス 余市方面の路線", U["bus_yoichi"], "積丹線（20）は小樽駅前→余市駅前→美国。余市線（18）は小樽駅前→蘭島→余市梅川車庫前", CHECKED),
    ("余市駅のコインロッカー", U["locker"], "余市：小400円16個、大700円6個", CHECKED),
    ("JR北海道のレールパス", U["railpass"], "Hokkaido Rail Pass：JR北海道の全線（新幹線を除く）", CHECKED),
    ("ニッカ 余市蒸溜所 楽しみ方", U["nikka"], "ガイドツアー無料・予約制。予約なしはミュージアム・ショップ・レストラン（ショップ側入口、最終入場15:30）。RITA'S KITCHEN 10:00〜15:50（LO15:20）。休業 12/23〜1/7・6/11。全施設16:15まで", "2026-11-26（小樽のマップの確認）"),
    ("ニッカ 余市蒸溜所 よくある質問", U["nikka_faq"], "ツアーは日本語のみ、予約は4週間先まで、食品の持ち込み不可、ロッカー100円（返却式・ツアー予約者のみ）", "2026-11-26（小樽のマップの確認）"),
    ("ニッカ 予約サイト 12月以降のご予約について（2026-11-19）", U["nikka_dec"], "12月・1月は設備改修のため無料ツアーなし、キーモルトセミナーのみ（9:30・10:00・10:30・11:30・12:00・12:30・13:30・14:00）。20歳以上・終日運転しない人。新規予約はWEBのみ、4週間前0:00から。12/5はレストランのみ休業", "2026-11-26（小樽のマップの確認）"),
    ("ニッカ 予約サイト 11月のご予約について", U["nikka_news"], "ガイドツアー所要60分、キーモルトセミナー所要90分・3,000円・現地で現金のみ", "2026-11-26（小樽のマップの確認）"),
    ("余市ワイナリー レストラン", U["win_rest"], "11:30〜 ラストオーダー14:30。休業日 1〜4月 火・水曜、5〜12月 火曜。JR余市駅より車で5分。石窯焼きピッツァ、道産牛100％のハンバーグ", CHECKED),
    ("余市ワイナリー カフェ", U["win_cafe"], "10:00〜16:00。休業日はレストランと同じ。余市ワインセット（3杯）、余市ワインソースがけソフト（通年）", CHECKED),
    ("余市ワイナリー 10月・11月の営業時間（2026-09-10）", U["win_1011"], "レストラン11:30〜（LO14:30）、カフェ10:00〜16:00、ワインショップ・工場見学・ギャラリー10:00〜16:30。12月以降のお知らせは2026-11-27の時点で出ていない", CHECKED),
    ("OcciGabi Winery アクセス・営業", U["occi"], "余市駅からタクシー約10分（1,400円前後）。ショップ11:00〜17:00。11月〜2月末は月〜木曜定休、12/17〜1/17冬季休業、2/16〜18臨時休業、3月は水・木曜定休、4〜10月は木曜定休。同じページに「12月〜2月は火曜定休、12/29〜1/3休み」とも書かれている", CHECKED),
    ("OcciGabi 試飲", U["occi_taste"], "カウンターで好きなワイン3種類550円", CHECKED),
    ("旧下ヨイチ運上家", U["unjo"], "令和8年度の開館 4/11〜12/13。月曜・祝日の翌日休館。9:00〜16:30（最終入場）。大人300円。見学約30分。1853年建築、現存する唯一の運上家", CHECKED),
    ("旧余市福原漁場", U["fuku"], "令和8年度の開館 4/11〜12/13。月曜・祝日の翌日休館。9:00〜16:30（最終入場）。大人300円。見学約40分。番屋・米味噌倉・文書庫・網倉・干場", CHECKED),
    ("よいち水産博物館と共通券", U["museum"], "入舟町21。9:00〜16:30（最終入館）、月曜・祝日の翌日休館、冬期閉館12月中旬〜4月上旬、大人300円、見学約40分。共通券（博物館・運上家・福原漁場・フゴッペ洞窟）大人960円、発売日から2日間有効", CHECKED),
    ("フゴッペ洞窟", U["fugoppe"], "令和8年度の開館 4/11〜12/13、月曜・祝日の翌日休館、9:00〜16:30（最終入場）、大人300円、施設内撮影禁止、中央バス「フゴッペ洞窟前」下車1分", CHECKED),
    ("シリパ岬", U["shiripa"], "余市湾の西側の断崖の岬。アイヌ語で sir＝山、pa＝頭。約630万年前に海底に噴出した溶岩ドーム、柱状節理", CHECKED),
    ("ローソク岩", U["rousoku"], "沖合約500m、高さ43m。余市駅から車で約15分、ローソク岩展望駐車場（無料）", CHECKED),
    ("余市川温泉 宇宙の湯", U["onsen"], "10:30〜20:00（水曜のみ13:00〜21:00）、定休日なし。入舟町322。余市駅から徒歩約15分。毛利衛さんの両親が営んでいた銭湯「喜久乃湯」の地", CHECKED),
    ("宇宙の湯 お風呂", U["onsen_bath"], "大人500円。天然温泉内湯・檜露天風呂・サウナ。無料：リンスインシャンプー・ボディソープ・ドライヤー。フェイスタオル250円、バスタオルは持参。タトゥーの記載なし", CHECKED),
    ("宇宙の湯 店舗情報", U["onsen_about"], "キャッシュレス決済：JCB・VISA・MasterCard・Diners・銀聯・QRコード決済", CHECKED),
    ("余市観光協会 営業時間・定休日変更のお知らせ（2026-11-07）", U["kk_notice"], "2026/11/3〜2027/4中旬：エルラプラザ9:30〜17:30・月曜休み、スペース・アップルよいち売店9:30〜17:30・月曜休み、宇宙記念館内ミュージアムショップは2026/11/30〜2027/4中旬冬期休館", CHECKED),
    ("余市宇宙記念館", U["dome"], "3Dシアターの上映予定 4月18日〜11月29日。プラネタリウムは2026年11月25日から機材不調で休止", CHECKED),
    ("回転寿司 余市番屋（余市観光協会）", U["banya"], "大川町4-71-1。11:00〜21:00（LO20:30）、定休日なし", CHECKED),
    ("みどりや（余市観光協会）", U["midoriya"], "黒川町3-54。11:00〜15:00・17:00〜21:00（LO20:00）、木曜休み。寿司・そば・ザンギ", CHECKED),
    ("柿崎商店 海鮮工房（余市観光協会）", U["kakizaki"], "黒川町7-25、余市駅前のオレンジ色の建物の2階。10:00〜18:00（LO17:30）、木曜休み", CHECKED),
    ("日の入り（札幌）12月", U["sun_dec"], "12/1 16:01、12/3 16:00", CHECKED),
    ("日の入り（札幌）1月", U["sun_jan"], "1/1 16:10、1/31 16:45", "2026-11-26（小樽のマップの確認）"),
    ("日の入り（札幌）2月", U["sun_feb"], "2/1 16:46、2/28 17:22", "2026-11-26（小樽のマップの確認）"),
    ("日の入り（札幌）3月", U["sun_mar"], "3/1 17:23、3/31 17:59", "2026-11-26（小樽のマップの確認）"),
    ("中央バス 余市案内所（積丹線などの時刻表の表紙）", "https://www.chuo-bus.co.jp/city_route/pdf/otaru_G.pdf", "余市案内所：JR余市駅隣接エルラプラザ内、9:30〜12:00・13:00〜17:30、月曜定休（祝日なら翌日）", CHECKED),
]]

JR = link("timetable", "JR北海道 運行情報", "JR Hokkaido service status", U["jr_info"])

# ---------------------------------------------------------------------------
# 何か所かに出すお知らせ
# ---------------------------------------------------------------------------
N_NIKKA_WINTER = notice(
    "12月・1月は無料のガイドツアーがありません", "No free tours in December and January",
    "試飲の建物の改修のため、2026年12月〜2027年1月は有料の「余市蒸溜所限定キーモルトセミナー」だけです（9:30・10:00・10:30・11:30・12:00・12:30・13:30・14:00）。20歳以上で、その日に車を運転しない人だけ参加できます。料金は予約ページで確かめてください（11月の案内では90分・3,000円・現地で現金払い）。予約なしでも、ミュージアム・ショップ・レストランには入れます。",
    "Because the tasting hall is being renovated, only the paid Key Malt Seminar runs from December 2026 to January 2027 (9:30, 10:00, 10:30, 11:30, 12:00, 12:30, 13:30, 14:00). You must be 20 or over and not driving that day. Check the fee on the booking page (in November it was 90 minutes, ¥3,000, cash only on the day). Without a booking you can still visit the museum, shop and restaurant.",
    U["nikka_dec"], to="2027-01-31")
N_NIKKA_CLOSED = notice(
    "12月23日〜1月7日は蒸溜所が休み", "The distillery is closed 23 December–7 January",
    "ショップ・レストラン・ミュージアムも休みです。この期間は余市より、小樽のマップの1日がおすすめです。",
    "The shop, restaurant and museum close too. During this time, the Otaru map makes a better day out.",
    U["nikka_news"], start="2026-12-10", to="2027-01-07")
N_TO_WINTER = notice(
    "12月14日からは「冬」のコースへ", "From 14 December, use the winter course",
    "福原漁場・運上家・よいち水産博物館は2026年12月13日まで（月曜休み）。12月14日からは、一覧の上のボタンで「冬」を選んでください。",
    "The fishery, the Unjoya and the fisheries museum are open until 13 December 2026 (closed Mondays). From 14 December, pick “Winter” with the buttons above the list.",
    U["museum"], to="2026-12-13")
N_SPRING_LATE = notice(
    "漁場と運上家は4月中旬から", "The fishery and Unjoya reopen in mid-April",
    "2026年は4月11日に開きました。2027年の開館日は余市町のサイトで確かめてください。開くまでは「冬」のコースを。",
    "They reopened on 11 April in 2026. Check the town’s website for the 2027 date, and use the winter course until then.",
    U["museum"], start="2027-03-20", to="2027-04-20")
N_SPRING_WINTER = notice(
    "4月中旬からは「4月〜12月中旬」のコースも", "From mid-April, the full course is back",
    "福原漁場・運上家・水産博物館が開いたら（2026年は4月11日）、一覧の上のボタンで「4月〜12月中旬」を選ぶと、海辺の史跡も回れます。",
    "Once the fishery, Unjoya and museum reopen (11 April in 2026), pick “Mid-Apr – mid-Dec” above the list to add the historic sites by the sea.",
    U["museum"], start="2027-04-01", to="2027-04-30")
N_WINTER_WALK = notice(
    "冬の余市を歩くとき", "Walking in Yoichi in winter",
    "歩道は踏み固められた雪や氷になります。底に溝の深い、滑りにくい靴で。12月は16時ごろに日が沈みます。雪の日は電車が遅れることがあるので、帰りは乗る電車を早めに決めておきます。",
    "Pavements turn to packed snow and ice. Wear boots with deep-tread soles. In December the sun sets around 16:00. Trains can run late on snowy days, so settle on your train home early.",
    start="2026-11-27", to="2027-03-31")
N_YEAREND = notice(
    "年末年始は休む場所があります", "Some places close over New Year",
    "ニッカの蒸溜所は12月23日〜1月7日、OcciGabiは12月17日〜1月17日が休み。余市ワイナリーの年末年始は2026年11月27日の時点で未発表（要確認）。高速バスは12月29・30日が土日祝ダイヤ、12月31日〜1月3日は運休が多いので、中央バスで確かめてください。宇宙の湯は公式サイトでは「定休日なし」です。",
    "The Nikka distillery closes 23 December–7 January and OcciGabi 17 December–17 January. Yoichi Winery had not announced its New Year days as of 27 November 2026 (please check). Highway buses run a holiday timetable on 29–30 December and many runs are cancelled 31 December–3 January. Uchu no Yu lists no closing days.",
    U["hw_winter"], start="2026-12-10", to="2027-01-07")
N_WINERY_DEC = notice(
    "12月からの営業時間は未発表", "December hours not yet announced",
    "余市ワイナリーの12月以降の営業時間と年末年始の休みは、2026年11月27日の時点で公式サイトに出ていません（要確認）。行く前に公式サイトのお知らせを見てください。",
    "As of 27 November 2026, Yoichi Winery had not posted its hours from December or its New Year closing days. Check the news page on its website before you go.",
    U["win_news"], to="2027-01-15")

# ---------------------------------------------------------------------------
# スポットの共通部分
# ---------------------------------------------------------------------------
S = dict(
    sapporo=dict(
        name=T("札幌駅（JR）", "Sapporo Station (JR)"), kind=T("駅", "Station"),
        blurb=T("余市まではJRで小樽乗り換え、1時間20分ほど。乗り換えなしの高速バスもあります。",
                "About 1 hr 20 min to Yoichi by JR, changing at Otaru. A direct highway bus also runs."),
        lat=43.06866, lng=141.35079,
        body=T("札幌8:41発の普通・小樽行きに乗り、小樽で9:36発の倶知安（くっちゃん）行きに乗り換えて、余市10:00着。平日も土曜も同じ時刻で、運賃は1,380円です。すすきのからは地下鉄南北線でさっぽろ駅まで5分（210円）。\n\n"
               "小樽〜余市の電車は1時間に1本ほど。8:41に乗れないと、次は札幌10:06発（余市11:23着）です。\n\n"
               "乗り換えなしで行くなら、札幌駅前9:05発の中央バスの高速バス（岩内行き）で「余市駅前十字街」まで。12月10日までは10:44着、12月11日からの冬ダイヤでは10:50着です。片道1,290円、予約はいらず、運賃は降りるときに払います（交通系ICカード可）。バスで行く日は、蒸溜所の11時台の回を予約してください。\n\n"
               "きっぷ：小樽〜余市で交通系ICカードが使えるかは、JR北海道のサイトで確かめられませんでした。札幌の券売機で余市までのきっぷを買えば確実です。JR北海道レールパス（全線）で乗れます。札幌・登別エリアパスに余市が入るかは要確認です。",
               "Take the 8:41 local train to Otaru and change there to the 9:36 for Kutchan, arriving in Yoichi at 10:00. Times are the same on weekdays and Saturdays, and the fare is ¥1,380. From Susukino, the Namboku subway line takes 5 minutes to Sapporo (¥210).\n\n"
               "Trains between Otaru and Yoichi run about once an hour. Miss the 8:41 and the next is the 10:06 from Sapporo (Yoichi 11:23).\n\n"
               "For a ride with no change, take Chuo Bus’s 9:05 highway bus for Iwanai from the Sapporo Station bus stop to Yoichi-ekimae-jujigai: 10:44 until 10 December, 10:50 on the winter timetable from 11 December. ¥1,290 one way, no booking, pay when you get off (IC cards work). If you go by bus, book a distillery slot after 11:00.\n\n"
               "Tickets: JR Hokkaido’s site does not make clear whether IC cards work between Otaru and Yoichi, so buy a paper ticket to Yoichi from the machine in Sapporo. The JR Hokkaido Rail Pass covers the trip; check whether the Sapporo-Noboribetsu Area Pass does."),
        gmaps=[gm("JR札幌駅", "JR Sapporo Station", 43.06866, 141.35079, "JR札幌駅")],
        links=[JR, link("timetable", "中央バス 高速よいち・いわない号（夏ダイヤ）", "Chuo Bus highway bus to Yoichi (Japanese)", U["hw_summer"]),
               link("timetable", "中央バス 冬ダイヤ（12月11日から）", "Chuo Bus winter timetable from 11 Dec (Japanese)", U["hw_index"]),
               link("official", "JR北海道レールパス", "JR Hokkaido Rail Pass", U["railpass"])],
        rows=[row("train", "札幌8:41→小樽（9:36発に乗り換え）→余市10:00（平日・土曜とも）。次は札幌10:06→余市11:23", "Sapporo 8:41 → Otaru (change to the 9:36) → Yoichi 10:00, weekdays and Saturdays. Next: Sapporo 10:06 → Yoichi 11:23"),
              row("bus", "高速バス 札幌駅前9:05→余市駅前十字街10:44", "Highway bus: Sapporo Station 9:05 → Yoichi-ekimae-jujigai 10:44", until="2026-12-10"),
              row("bus", "高速バス 札幌駅前9:05→余市駅前十字街10:50（冬ダイヤ）", "Highway bus: Sapporo Station 9:05 → Yoichi-ekimae-jujigai 10:50 (winter timetable)", start="2026-12-11"),
              row("fee", "JR 札幌→余市1,380円。高速バス 札幌駅前→余市駅前十字街1,290円（往復2,420円）", "JR Sapporo → Yoichi ¥1,380. Highway bus ¥1,290 (return ¥2,420)")],
        tip=T("JRは乗換案内で2026年12月3日（木）・5日（土）のダイヤを、高速バスは北海道中央バスの公式時刻表（夏ダイヤと2026年12月11日改正の冬ダイヤ）を確認しました。JR北海道は春にダイヤ改正があります。",
              "JR times from a route planner for 3 and 5 December 2026; bus times from Chuo Bus’s summer timetable and its winter timetable from 11 December 2026. JR Hokkaido revises its timetable in spring.")),

    eki=dict(
        name=T("余市（よいち）駅", "Yoichi Station"), kind=T("駅", "Station"),
        blurb=T("駅前の道をまっすぐ行くと蒸溜所の正門。駅の隣に観光物産センター、駅にコインロッカーがあります。",
                "Walk straight out of the station to the distillery gate. A local produce centre stands next door, and there are coin lockers."),
        lat=43.18690, lng=140.79479,
        body=T("・ニッカの蒸溜所までは歩いて5分ほどです。\n"
               "・コインロッカーは小（400円）が16個、大（700円）が6個（JR北海道の一覧）。\n"
               "・駅の隣の観光物産センター「エルラプラザ」は9:30〜17:30。2026年11月3日〜2027年4月中旬は月曜休み（祝日なら翌日）。中の中央バスの案内所（9:30〜12:00・13:00〜17:30、月曜休み）で、バスの時刻を聞けます。\n"
               "・駅から歩いて10分の道の駅「スペース・アップルよいち」には、余市宇宙記念館があります。宇宙記念館は2026年11月30日から2027年4月中旬まで冬の休館です。\n"
               "・小樽寄りの栄町には、壁に刻画の残るフゴッペ洞窟があります（2026年は4月11日〜12月13日、月曜休み、300円、中は撮影禁止）。行くなら中央バスで「フゴッペ洞窟前」下車。\n"
               "・余市を出る電車は1時間に1本ほど。帰りの時刻（最後のスポット）を先に見ておくと安心です。",
               "• The Nikka distillery is about 5 minutes on foot.\n"
               "• Coin lockers: 16 small (¥400) and 6 large (¥700), according to JR Hokkaido.\n"
               "• Elra Plaza, the local produce centre next to the station, is open 9:30–17:30, closed Mondays (or the next day after a holiday) from 3 November 2026 to mid-April 2027. The Chuo Bus desk inside (9:30–12:00, 13:00–17:30, closed Mondays) can help with bus times.\n"
               "• Ten minutes’ walk away, the Space Apple Yoichi roadside station has the Yoichi Space Museum. The museum closes for winter from 30 November 2026 to mid-April 2027.\n"
               "• Towards Otaru, Fugoppe Cave has carvings on its rock walls (open 11 April–13 December in 2026, closed Mondays, ¥300, no photos inside). Take a Chuo Bus to the Fugoppe-dokutsu-mae stop.\n"
               "• Trains leave Yoichi about once an hour, so check the times home (last stop) first."),
        gmaps=[gm("JR余市駅", "JR Yoichi Station", 43.18690, 140.79479, "JR余市駅"),
               gm("道の駅 スペース・アップルよいち", "Space Apple Yoichi roadside station", 43.18915, 140.78876, "道の駅 スペース・アップルよいち")],
        links=[JR, link("info", "余市観光協会（英語のページあり）", "Yoichi Tourism Association (English page)", "https://yoichi-kankoukyoukai.com/", U["kk_en"]),
               link("official", "余市宇宙記念館", "Yoichi Space Museum (Japanese)", U["dome"]),
               link("official", "フゴッペ洞窟（余市町）", "Fugoppe Cave (Japanese)", U["fugoppe"])],
        rows=[row("hours", "エルラプラザ 9:30〜17:30（11月3日〜4月中旬は月曜休み）", "Elra Plaza 9:30–17:30 (closed Mondays, 3 Nov–mid-Apr)")],
        tip=T("コインロッカーはJR北海道の一覧、エルラプラザ・道の駅・宇宙記念館は余市観光協会のお知らせ（2026年11月7日）、フゴッペ洞窟は余市町のページで確認しました。",
              "Lockers from JR Hokkaido’s list; Elra Plaza, the roadside station and the Space Museum from the Yoichi Tourism Association (7 Nov 2026); Fugoppe Cave from the town’s website.")),

    nikka=dict(
        name=T("ニッカウヰスキー 北海道 余市蒸溜所", "Nikka Whisky Yoichi Distillery"), kind=T("蒸溜所（見学は予約制）", "Distillery (tours by booking)"),
        caution=T("見学は予約制・日本語のみ。12月23日〜1月7日は休み", "Tours by booking only, in Japanese. Closed 23 Dec–7 Jan"),
        blurb=T("竹鶴政孝（たけつるまさたか）がスコットランドに似た土地を求めて選んだ蒸溜所。石造りの棟と赤い屋根が並びます。",
                "Taketsuru Masataka chose Yoichi for its Scotland-like climate. Stone buildings with red roofs line the grounds."),
        lat=43.18617, lng=140.78950,
        body=T("・ガイドツアー（無料・試飲つき）は予約制。予約は公式の予約ページ（英語あり）で、4週間先まで。案内は日本語だけです。11月の案内では所要60分で、外の製造の建物を歩くので暖かい服で。\n\n"
               "・2026年12月〜2027年1月は、無料のツアーはなく有料のセミナーだけです（お知らせを参照）。2月からの回は予約ページで確かめてください。\n\n"
               "・予約なしでも、ニッカミュージアム（有料のテイスティングバーあり）、ショップ、レストラン「RITA'S KITCHEN」に入れます。入口はショップ側で、最終入場は15:30、すべて16:15に閉まります。\n\n"
               "・お昼はRITA'S KITCHEN（10:00〜15:50、ラストオーダー15:20）。2026年12月5日はレストランだけ休みです。駅前で海鮮を食べるなら、国道5号沿いのオレンジ色の建物の2階「柿崎商店 海鮮工房」（10:00〜18:00、ラストオーダー17:30、木曜休み。余市観光協会の案内）。海鮮丼と定食の店で、行列ができることもあります。\n\n"
               "・食べ物の持ち込みはできません。100円が戻るロッカーは、ツアーを予約した人だけ使えます。",
               "• The guided tour (free, with tasting) needs a booking on the official booking site (English available), up to four weeks ahead. Tours are in Japanese only. In November they took 60 minutes, partly outdoors, so dress warmly.\n\n"
               "• From December 2026 to January 2027 there are no free tours, only a paid seminar (see the notice). Check the booking site for what runs from February.\n\n"
               "• Without a booking you can visit the Nikka Museum (with a paid tasting bar), the shop and RITA’S KITCHEN restaurant. Use the shop entrance; last entry 15:30, everything closes at 16:15.\n\n"
               "• Lunch at RITA’S KITCHEN (10:00–15:50, last order 15:20); the restaurant alone is closed on 5 December 2026. For seafood by the station, Kakizaki Shoten Kaisen Kobo is upstairs in the orange building on Route 5 (10:00–18:00, last order 17:30, closed Thursdays, per the Yoichi Tourism Association): rice bowls and set meals, sometimes with a queue.\n\n"
               "• No outside food. The coin-return lockers (¥100) are for tour guests only."),
        gmaps=[gm("ニッカウヰスキー 余市蒸溜所", "Nikka Yoichi Distillery", 43.18617, 140.78950, "ニッカウヰスキー 北海道 余市蒸溜所"),
               gm("柿崎商店 海鮮工房", "Kakizaki Shoten Kaisen Kobo", 43.18658, 140.79303, "柿崎商店 海鮮工房 余市")],
        links=[link("official", "ニッカ 余市蒸溜所（楽しみ方）", "Nikka Yoichi Distillery (official)", U["nikka"], U["nikka_en"]),
               link("official", "見学予約（日本語・英語）", "Tour booking (Japanese / English)", U["nikka_book"]),
               link("info", "予約サイトのお知らせ", "Booking site notices", U["nikka_news"]),
               link("info", "柿崎商店 海鮮工房（余市観光協会）", "Kakizaki Shoten Kaisen Kobo (Yoichi Tourism Association)", U["kakizaki"])],
        rows=[row("hours", "予約なしの施設は最終入場15:30、全施設16:15まで。レストラン10:00〜15:50（LO15:20）", "Walk-in areas: last entry 15:30, all close 16:15. Restaurant 10:00–15:50 (last order 15:20)"),
              row("closed", "12月23日〜1月7日、6月11日", "23 Dec–7 Jan, 11 June"),
              row("fee", "ガイドツアー無料（予約制）。12〜1月はセミナーのみ（料金は予約ページで）", "Guided tour free (booking needed). Dec–Jan: paid seminar only (fee on the booking site)")],
        tip=T("ニッカウヰスキーの公式サイトと公式の見学予約サイトのお知らせ（2026年11月26日に確認）、柿崎商店は余市観光協会の案内で確認しました。",
              "From Nikka’s website and the notices on its official booking site (checked 26 Nov 2026), and the Yoichi Tourism Association for Kakizaki Shoten.")),

    winery=dict(
        name=T("余市ワイナリー", "Yoichi Winery"), kind=T("ワイナリー（試飲・ショップ・レストラン）", "Winery (tasting, shop, restaurant)"),
        caution=T("火曜休み（1〜4月は火・水曜休み）", "Closed Tuesdays (Tuesdays and Wednesdays, Jan–Apr)"),
        blurb=T("札幌の酒蔵・日本清酒（千歳鶴）が営むワイナリー。カフェで余市ワインの3杯セットが飲めます。",
                "Run by Nippon Seishu, the Sapporo brewer behind Chitosetsuru sake. The café pours a three-glass flight of Yoichi wine."),
        lat=43.16936, lng=140.79255,
        body=T("・駅前のタクシーで5分ほど（歩くと40分ほど）。帰りの車は、行きのタクシーで迎えの時間を頼んでおくと安心です。\n\n"
               "・カフェ（10:00〜16:00）では、定番の赤か白を3杯飲み比べる「余市ワインセット」や、余市ワインのソースをかけたソフトクリーム（運転する人や子どもも食べられる、通年）。ワインショップは10:00〜16:30で、ワイナリーでしか買えないワインもあります。工場見学も10:00〜16:30（2026年10・11月の案内）。\n\n"
               "・レストランは11:30から（ラストオーダー14:30）。石窯で焼くピッツァと、道産牛100％のハンバーグ。\n\n"
               "・写真は余市町の登（のぼり）地区のぶどう畑で、ワイナリーの建物ではありません。\n\n"
               "・もう一軒行くなら、山田町のOcciGabi Winery（オチガビ。駅からタクシーで約10分、1,400円前後）。ショップは11:00〜17:00、カウンターで3種類の試飲550円。11月〜2月は月〜木曜が休み、12月17日〜1月17日は冬の休みです（公式サイト。同じページに別の定休日の書き方もあるので、行く前に電話で確かめてください）。",
               "• About 5 minutes by taxi from the station (40 minutes on foot). Ask your driver to come back for you at a set time.\n\n"
               "• The café (10:00–16:00) serves the Yoichi Wine Set, a flight of three reds or three whites, and a soft-serve topped with Yoichi wine sauce that drivers and children can eat too (all year). The wine shop is open 10:00–16:30 and has bottles sold only here. The factory visit area is also open 10:00–16:30 (October–November 2026 notice).\n\n"
               "• The restaurant opens at 11:30 (last order 14:30): stone-oven pizza and 100% Hokkaido beef hamburg steak.\n\n"
               "• The photo shows vineyards in Yoichi’s Nobori district, not the winery building.\n\n"
               "• For a second winery, OcciGabi Winery in Yamada-cho is about 10 minutes by taxi from the station (around ¥1,400). Shop 11:00–17:00; a three-wine tasting at the counter is ¥550. It is closed Monday–Thursday from November to February and from 17 December to 17 January (its website also lists a different set of closing days, so phone before you go)."),
        gmaps=[gm("余市ワイナリー", "Yoichi Winery", 43.16936, 140.79255, "余市ワイナリー"),
               gm("OcciGabi Winery", "OcciGabi Winery", 43.17606, 140.77736, "OcciGabi Winery 余市")],
        links=[link("official", "余市ワイナリー カフェ", "Yoichi Winery café (Japanese)", U["win_cafe"]),
               link("official", "余市ワイナリー レストラン", "Yoichi Winery restaurant (Japanese)", U["win_rest"]),
               link("info", "余市ワイナリーのお知らせ（営業時間）", "Yoichi Winery news (hours)", U["win_news"]),
               link("official", "OcciGabi Winery（アクセス・営業日）", "OcciGabi Winery (Japanese)", U["occi"])],
        rows=[row("hours", "カフェ10:00〜16:00、ワインショップ・工場見学10:00〜16:30、レストラン11:30〜（LO14:30）", "Café 10:00–16:00; wine shop and factory 10:00–16:30; restaurant from 11:30 (last order 14:30)"),
              row("closed", "5〜12月は火曜、1〜4月は火・水曜。年末年始は要確認", "Tuesdays (May–Dec); Tuesdays and Wednesdays (Jan–Apr). New Year: please check")],
        tip=T("日本清酒の公式サイト（レストラン・カフェのページと2026年9月10日のお知らせ）、OcciGabiの公式サイトで確認しました。",
              "From Nippon Seishu’s website (restaurant and café pages, notice of 10 Sep 2026) and OcciGabi’s website.")),

    fuku=dict(
        name=T("旧余市福原漁場（きゅうよいちふくはらぎょば）", "Former Yoichi Fukuhara Fishery"), kind=T("ニシン漁の漁場の建物", "Herring fishery buildings"),
        caution=T("月曜・祝日の翌日休み。12月14日〜4月上旬は冬の閉館", "Closed Mondays and the day after holidays; closed for winter mid-Dec–early Apr"),
        blurb=T("幕末から浜中町でニシン漁をしていた福原家の番屋・蔵・干場が、当時の姿で残っています。",
                "The bunkhouse, storehouses and drying racks of the Fukuhara family, who settled here to fish herring in the late Edo period."),
        lat=43.20002, lng=140.77888,
        body=T("出稼ぎの漁夫が寝泊まりした番屋（主屋）は、板の間の「ダイドコロ」の一部が2階建てで、漁の最盛期には床板を外して土足のまま食事ができるようになっていたそうです。ネズミよけに外壁と内壁の間に石を詰めた米味噌倉、書類と衣服をしまった文書庫、網倉、カズノコや白子を干した干場も残ります。見学は約40分。\n\n"
               "ここから海沿いに東へ歩いて25分ほどで、運上家とモイレの浜です。",
               "The main bunkhouse slept the seasonal fishermen; part of its wooden-floored hall has a second level, and at the height of the season the floorboards came up to make a table where men ate with their boots on. You can also see a rice-and-miso store with stones packed between its walls against rats, a document store, a net store and the racks where herring roe and milt were dried. Allow about 40 minutes.\n\n"
               "From here it is about 25 minutes’ walk east along the coast to the Unjoya and Moire beach."),
        gmaps=[gm("旧余市福原漁場", "Former Yoichi Fukuhara Fishery", 43.20002, 140.77888, "旧余市福原漁場")],
        links=[link("official", "旧余市福原漁場（余市町）", "Former Yoichi Fukuhara Fishery (Japanese)", U["fuku"]),
               link("info", "共通券と水産博物館（余市町）", "Combined ticket and museum (Japanese)", U["museum"])],
        rows=[row("hours", "9:00〜16:30（最終入場）。2026年は4月11日〜12月13日", "9:00–16:30 (last entry). Open 11 Apr–13 Dec in 2026"),
              row("closed", "月曜（祝日なら開館）・祝日の翌日、12月中旬〜4月上旬", "Mondays (open on holidays), the day after a holiday, mid-Dec–early Apr"),
              row("fee", "大人300円。共通券（福原漁場・運上家・水産博物館・フゴッペ洞窟）960円、2日間有効", "¥300. Combined ticket for four sites ¥960, valid two days")],
        tip=T("開館日・時間・料金は余市町の公式サイトで確認しました。", "Dates, hours and fees from the Town of Yoichi’s website.")),

    unjo=dict(
        name=T("旧下ヨイチ運上家（きゅうしもよいちうんじょうや）", "Former Shimo-Yoichi Unjoya"), kind=T("江戸時代の交易の拠点", "Edo-period trading post"),
        caution=T("月曜・祝日の翌日休み。12月14日〜4月上旬は冬の閉館", "Closed Mondays and the day after holidays; closed for winter mid-Dec–early Apr"),
        blurb=T("江戸時代、アイヌ民族との交易を請け負った商人の拠点。1853年の建物で、今も残る運上家はここだけです。",
                "Built in 1853 as the base of the merchant who ran trade with the Ainu for the Matsumae domain. The only unjoya still standing."),
        lat=43.19784, lng=140.78815,
        body=T("間口40m・奥行16mの長い建物に、石を載せた屋根と格子窓。中の柱や梁の多くは当時のままで、座敷には支配人や松前藩士などの人形が置かれています。見学は約30分。\n\n"
               "裏の小山（モイレ山）の上には、よいち水産博物館があります（9:00〜16:30最終入館、300円、見学約40分）。ニシン漁の道具、アイヌ民族の展示、北前船の模型など。時間に余裕がある日や、福原漁場を外した日に。\n\n"
               "運上家から海の方へ歩いて5分で、モイレの浜です。",
               "A 40-metre-long building with a stone-weighted roof and lattice windows; many of the posts and beams inside are original, and the rooms hold figures of the manager and domain officials. Allow about 30 minutes.\n\n"
               "On the small hill behind (Moire-yama) is the Yoichi Fisheries Museum (last entry 16:30, ¥300, about 40 minutes): herring-fishing gear, Ainu exhibits and a model of a Kitamae trading ship. Go if you have spare time or skipped the Fukuhara fishery.\n\n"
               "Moire beach is 5 minutes’ walk towards the sea."),
        gmaps=[gm("旧下ヨイチ運上家", "Former Shimo-Yoichi Unjoya", 43.19784, 140.78815, "旧下ヨイチ運上家"),
               gm("よいち水産博物館", "Yoichi Fisheries Museum", 43.19666, 140.78681, "よいち水産博物館")],
        links=[link("official", "旧下ヨイチ運上家（余市町）", "Former Shimo-Yoichi Unjoya (Japanese)", U["unjo"]),
               link("official", "よいち水産博物館・共通券（余市町）", "Yoichi Fisheries Museum and combined ticket (Japanese)", U["museum"])],
        rows=[row("hours", "9:00〜16:30（最終入場）。2026年は4月11日〜12月13日", "9:00–16:30 (last entry). Open 11 Apr–13 Dec in 2026"),
              row("closed", "月曜（祝日なら開館）・祝日の翌日、12月中旬〜4月上旬", "Mondays (open on holidays), the day after a holiday, mid-Dec–early Apr"),
              row("fee", "運上家・水産博物館 各大人300円。共通券960円（4施設、2日間有効）", "Unjoya and museum ¥300 each. Combined ticket ¥960 (four sites, two days)")],
        tip=T("開館日・時間・料金は余市町の公式サイトで確認しました。", "Dates, hours and fees from the Town of Yoichi’s website.")),

    moire=dict(
        name=T("モイレの浜から見るシリパ岬", "Cape Shiripa from Moire beach"), kind=T("海辺の眺め", "Coastal view"),
        blurb=T("余市湾の西に突き出た断崖の岬。名前はアイヌ語の「山の頭」から。浜から湾の向こうに見えます。",
                "The cliff-edged cape on the west of Yoichi Bay; the name comes from the Ainu for “head of the mountain”. You see it across the bay from the beach."),
        lat=43.19868, lng=140.78549,
        body=T("シリパ岬は、約630万年前に海底に噴き出した溶岩がドームになったものと考えられていて、岩肌には柱のような割れ目（柱状節理）が見られます（余市町のページ）。\n\n"
               "浜中・モイレ海水浴場は運上家から歩いて5分。夏以外は海水浴場の設備は使えませんが、浜の入り口から岬が見えます。冬は雪の積もった浜に無理に下りず、入り口から眺めるだけで十分です。風の強い日は短めに。\n\n11月と12月は16時ごろに日が沈み、16時を過ぎると岬は見えにくくなります。この時期は漁場から歩いてきたら先に浜を見て、そのあと運上家へ（最終入場16:30）。\n\n"
               "西へ車で15分の豊浜町には、沖に立つ高さ43mのローソク岩があります（展望駐車場あり、無料）。路線バスでは行きにくいので、タクシーで往復できる人向けです。",
               "Cape Shiripa is thought to be a lava dome formed by an undersea eruption about 6.3 million years ago, and its rock shows column-like joints (Town of Yoichi).\n\n"
               "Hamanaka-Moire beach is 5 minutes’ walk from the Unjoya. Outside summer the beach facilities are closed, but you can see the cape from the beach entrance. In winter, don’t walk out onto the snow; the view from the entrance is enough. Keep it short on windy days.\n\nIn November and December the sun sets around 16:00, and after that the cape is hard to see. At that time of year, walking from the fishery, look at the beach first and then visit the Unjoya (last entry 16:30).\n\n"
               "Fifteen minutes west by car, at Toyohama, Candle Rock stands 43 m tall offshore (free viewing car park). Buses don’t make it easy, so go only if you can take a taxi there and back."),
        gmaps=[gm("浜中・モイレ海水浴場", "Hamanaka-Moire beach", 43.19868, 140.78549, "浜中モイレ海水浴場 余市"),
               gm("ローソク岩 展望駐車場", "Candle Rock viewpoint", 43.23357, 140.70381, "ローソク岩展望駐車場 余市")],
        links=[link("official", "シリパ岬（余市町）", "Cape Shiripa (Japanese)", U["shiripa"]),
               link("official", "ローソク岩（余市町）", "Candle Rock (Japanese)", U["rousoku"])],
        rows=[row("hours", "浜は自由に見られます", "Open any time")],
        tip=T("岬と岩の説明は余市町の公式サイトで確認しました。", "Cape and rock details from the Town of Yoichi’s website.")),

    onsen=dict(
        name=T("余市川温泉 宇宙の湯（うちゅうのゆ）", "Yoichigawa Onsen Uchu no Yu"), kind=T("日帰り温泉", "Day-use hot spring"),
        caution=T("タトゥーの決まりは公式サイトに書かれていません（受付で確認）", "Tattoo policy not stated on its website: ask at reception"),
        blurb=T("宇宙飛行士・毛利衛（もうりまもる）さんの両親が営んでいた銭湯の場所にある天然温泉。檜の露天風呂とサウナ。",
                "A natural hot spring on the site of the bathhouse once run by astronaut Mohri Mamoru’s parents. Cedar outdoor bath and sauna."),
        lat=43.19262, lng=140.78573,
        body=T("・10:30〜20:00（水曜だけ13:00〜21:00）、休みなし。大人500円。\n"
               "・リンスインシャンプー・ボディソープ・ドライヤーは無料。フェイスタオルは250円で売っています。バスタオルは持っていきます。\n"
               "・クレジットカード（JCB・VISA・Mastercard・Diners・銀聯）とQRコード決済が使えます（公式サイトの店舗情報）。\n"
               "・タトゥー：公式サイトに決まりが書かれていません（要確認）。入る前に受付で聞くか、電話（0135-22-4126）で確かめてください。\n"
               "・初めての人へ：洗い場で体を洗ってから湯船へ。タオルは湯船に入れません。\n"
               "・駅から歩いて約15分。写真は温泉の名前になっている余市川です。",
               "• 10:30–20:00 (Wednesdays 13:00–21:00), open every day. ¥500.\n"
               "• Rinse-in shampoo, body soap and hair dryers are free. Face towels are sold for ¥250; bring a bath towel.\n"
               "• Credit cards (JCB, VISA, Mastercard, Diners, UnionPay) and QR-code payments are accepted (official site).\n"
               "• Tattoos: the website says nothing either way (please check). Ask at reception before you go in, or phone 0135-22-4126.\n"
               "• First time? Wash at the showers before getting in, and keep your towel out of the water.\n"
               "• About 15 minutes’ walk from the station. The photo shows the Yoichi River, which gives the spring its name."),
        gmaps=[gm("余市川温泉 宇宙の湯", "Yoichigawa Onsen Uchu no Yu", 43.19262, 140.78573, "余市川温泉 宇宙の湯")],
        links=[link("official", "余市川温泉（営業時間・料金）", "Yoichigawa Onsen (Japanese)", U["onsen"]),
               link("official", "お風呂と料金", "Baths and fees (Japanese)", U["onsen_bath"])],
        rows=[row("hours", "10:30〜20:00（水曜は13:00〜21:00）", "10:30–20:00 (Wed 13:00–21:00)"),
              row("closed", "なし（公式サイト）", "None (official site)"),
              row("fee", "大人500円、フェイスタオル250円", "¥500; face towel ¥250")],
        tip=T("時間・料金・設備・支払い方法は余市川温泉の公式サイトで確認しました。タトゥーの決まりは書かれていませんでした。",
              "Hours, fees, facilities and payment from the official website, which does not mention tattoos.")),

    kaeri=dict(
        name=T("晩ごはん（回転寿司 余市番屋）と帰りの電車", "Dinner (Yoichi Banya sushi) and the train back"), kind=T("回転ずし・駅", "Conveyor-belt sushi, then the station"),
        blurb=T("毎朝、余市や小樽の沿岸で揚がった魚を仕入れる回転ずし。駅まで歩いて10分ほどです。",
                "A conveyor-belt sushi shop buying fish landed along the Yoichi and Otaru coast each morning. About 10 minutes’ walk to the station."),
        lat=43.19220, lng=140.79482,
        body=T("・回転寿司 余市番屋：11:00〜21:00（ラストオーダー20:30）、休みなし（余市観光協会の案内）。支払い方法は要確認。\n"
               "・駅の近くの寿し処 みどりや（11:00〜15:00・17:00〜21:00、ラストオーダー20:00、木曜休み）は、握りのほか、そばや北海道の唐揚げ「ザンギ」も。\n"
               "・帰りの電車（余市→札幌、平日も土曜も同じ）：18:35発（札幌19:58着）、19:26発（小樽で乗り換え、札幌20:41着）、20:19発（21:44着）、21:28発（22:44着）、最終は22:26発（23:53着）。運賃1,380円。\n"
               "・小樽で晩ごはんにするなら、余市17:42発で小樽18:08着（470円）。小樽からの帰りの時刻は小樽のマップに。\n"
               "・夜の余市駅は電車の間が1時間ほどあくので、乗る電車を決めてから店を出ます。",
               "• Yoichi Banya: 11:00–21:00 (last order 20:30), open every day (Yoichi Tourism Association). Payment methods: please check.\n"
               "• Near the station, Midoriya (11:00–15:00 and 17:00–21:00, last order 20:00, closed Thursdays) serves nigiri plus soba and zangi, Hokkaido-style fried chicken.\n"
               "• Trains to Sapporo (same on weekdays and Saturdays): 18:35 (Sapporo 19:58), 19:26 (change at Otaru, Sapporo 20:41), 20:19 (21:44), 21:28 (22:44), and the last at 22:26 (23:53). ¥1,380.\n"
               "• For dinner in Otaru instead, the 17:42 from Yoichi arrives at 18:08 (¥470); see the Otaru map for trains back from there.\n"
               "• Evening trains are about an hour apart, so pick your train before you leave the restaurant."),
        gmaps=[gm("回転寿司 余市番屋", "Yoichi Banya (sushi)", 43.19220, 140.79482, "回転寿司 余市番屋"),
               gm("寿し処 みどりや", "Midoriya (sushi)", 43.18918, 140.79253, "寿し処 みどりや 余市"),
               gm("JR余市駅", "JR Yoichi Station", 43.18690, 140.79479, "JR余市駅")],
        links=[JR, link("info", "回転寿司 余市番屋（余市観光協会）", "Yoichi Banya (Yoichi Tourism Association)", U["banya"]),
               link("info", "みどりや（余市観光協会）", "Midoriya (Yoichi Tourism Association)", U["midoriya"]),
               link("info", "小樽のマップ", "Otaru map", U["otaru_map"])],
        rows=[row("train", "余市→札幌：18:35（19:58着）、19:26（20:41着）、20:19（21:44着）、21:28（22:44着）、最終22:26（23:53着）", "Yoichi → Sapporo: 18:35 (19:58), 19:26 (20:41), 20:19 (21:44), 21:28 (22:44), last 22:26 (23:53)"),
              row("train", "余市17:42→小樽18:08（小樽で晩ごはんにする日）", "Yoichi 17:42 → Otaru 18:08 (for dinner in Otaru)"),
              row("hours", "余市番屋 11:00〜21:00（LO20:30）、みどりや 11:00〜15:00・17:00〜21:00（LO20:00、木曜休み）", "Yoichi Banya 11:00–21:00 (LO 20:30); Midoriya 11:00–15:00, 17:00–21:00 (LO 20:00, closed Thu)")],
        tip=T("お店の時間は余市観光協会の案内、電車は乗換案内で2026年12月3日（木）・5日（土）のダイヤを確認しました。",
              "Restaurant hours from the Yoichi Tourism Association; trains from a route planner for 3 and 5 December 2026.")),
)

# ---------------------------------------------------------------------------
# コースごとの時間割
# ---------------------------------------------------------------------------
LATE = dict(
    file="yoichi.json", course="late",
    order=["sapporo", "eki", "nikka", "winery", "fuku", "unjo", "moire", "onsen", "kaeri"],
    spots=dict(
        sapporo=dict(
            pre=T("札幌8:41発で余市10:00着。予約したニッカのツアーと蒸溜所でお昼、タクシーでワイナリーへ。午後はニシン漁の漁場と運上家、シリパ岬の見える浜を歩き、温泉と回転ずしで締めて、19:26の電車で札幌20:41着。\n\n蒸溜所の見学は予約制です（予約ページは英語あり、4週間前から）。",
                  "The 8:41 from Sapporo reaches Yoichi at 10:00. A booked Nikka tour and lunch at the distillery, then a taxi to the winery. In the afternoon, the herring fishery, the Unjoya and the beach facing Cape Shiripa, then a hot spring and sushi before the 19:26 train (Sapporo 20:41).\n\nDistillery tours need a booking (English booking site, opens four weeks ahead)."),
            caution=T("漁場・運上家は月曜休み、2026年は12月13日まで", "Fishery and Unjoya closed Mondays; open until 13 Dec in 2026"),
            notices=[N_TO_WINTER, N_SPRING_LATE, N_NIKKA_CLOSED, N_NIKKA_WINTER, N_WINTER_WALK],
            time=(DEP, "8:41（札幌駅に8:30ごろ）", "8:41 (be at Sapporo Station by about 8:30)")),
        eki=dict(time=(MOV, "10:00着", "arrive 10:00")),
        nikka=dict(
            pre=T("10:05に入って、予約なしで入れるミュージアムから。10:30の回のツアー（約60分）を予約しておくと、ショップを見て12:00ごろからレストランでお昼にできます。13:00に出て、駅前のタクシーへ。",
                  "In at 10:05; start with the walk-in museum. Book the 10:30 tour (about an hour), browse the shop and have lunch at the restaurant from about 12:00. Leave at 13:00 for the taxis at the station."),
            notices=[N_NIKKA_WINTER, N_NIKKA_CLOSED],
            time=(VIS, "10:05〜13:00（ツアーとお昼を含む）", "10:05–13:00 (including the tour and lunch)")),
        winery=dict(
            pre=T("13:00に駅前からタクシーで。帰りは、福原漁場まで迎えのタクシーを頼んでおきます（14:15ごろ）。",
                  "Taxi from the station at 13:00. Arrange a taxi to pick you up around 14:15 and take you on to the Fukuhara fishery."),
            notices=[N_WINERY_DEC],
            time=(VIS, "13:10〜14:15", "13:10–14:15")),
        fuku=dict(
            pre=T("ワイナリーからタクシーで15分ほど。月曜（祝日の翌日も）は休みです。", "About 15 minutes by taxi from the winery. Closed Mondays and the day after a holiday."),
            time=(VIS, "14:30〜15:10", "14:30–15:10")),
        unjo=dict(
            pre=T("福原漁場から海沿いに歩いて25分ほど。最終入場は16:30です。", "About 25 minutes’ walk along the coast from the fishery. Last entry 16:30."),
            time=(VIS, "15:35〜16:05", "15:35–16:05")),
        moire=dict(
            pre=T("運上家から歩いて5分。", "Five minutes’ walk from the Unjoya."),
            time=(VIS, "16:10〜16:30", "16:10–16:30")),
        onsen=dict(
            pre=T("浜から歩いて20分ほど。", "About 20 minutes’ walk from the beach."),
            time=(VIS, "16:50〜17:55", "16:50–17:55")),
        kaeri=dict(
            pre=T("宇宙の湯から歩いて15分。18:10ごろから晩ごはん、19:05に店を出て駅へ歩き（10分ほど）、19:26発で札幌20:41着。もう少しゆっくりなら20:19発（21:44着）。",
                  "Fifteen minutes’ walk from Uchu no Yu. Dinner from about 18:10; leave at 19:05 and walk to the station (about 10 minutes) for the 19:26 (Sapporo 20:41). For a slower evening, the 20:19 (21:44)."),
            notices=[N_YEAREND],
            time=(DEP, "19:26（札幌20:41着）", "19:26 (Sapporo 20:41)")),
    ),
)

EARLY = dict(
    file="yoichi-winter.json", course="early",
    order=["sapporo", "eki", "nikka", "winery", "moire", "onsen", "kaeri"],
    spots=dict(
        sapporo=dict(
            pre=T("冬は浜の漁場や博物館が閉まるので、ウイスキー・ワイン・温泉・すしの1日です。札幌8:41発で余市10:00着。12〜1月はニッカの有料セミナー（予約制）、蒸溜所でお昼、タクシーでワイナリーへ。明るいうちに雪のシリパ岬を見て、温泉で温まってから回転ずし。18:35の電車で札幌19:58着です。",
                  "In winter the fishery and museums close, so this is a day of whisky, wine, a hot spring and sushi. The 8:41 from Sapporo reaches Yoichi at 10:00. In December–January, a paid Nikka seminar (booking needed), lunch at the distillery, then a taxi to the winery. See Cape Shiripa in the snow while it is light, warm up in the hot spring, then sushi and the 18:35 train (Sapporo 19:58)."),
            caution=T("蒸溜所は12月23日〜1月7日休み", "Distillery closed 23 Dec–7 Jan"),
            notices=[N_NIKKA_CLOSED, N_NIKKA_WINTER, N_SPRING_WINTER, N_WINTER_WALK],
            time=(DEP, "8:41（札幌駅に8:30ごろ）", "8:41 (be at Sapporo Station by about 8:30)")),
        eki=dict(
            photos=["eki-w2", "eki-w1", "eki-w3"],
            time=(MOV, "10:00着", "arrive 10:00")),
        nikka=dict(
            pre=T("12月・1月は10:30の回のキーモルトセミナー（約90分）を予約。始まる前にミュージアムを見て、終わったら12:00ごろからレストランでお昼。13:00に出て、駅前のタクシーへ。2月からの回は予約ページで確かめてください。",
                  "In December and January, book the 10:30 Key Malt Seminar (about 90 minutes). See the museum first, then lunch at the restaurant from about 12:00. Leave at 13:00 for the taxis at the station. Check the booking site for what runs from February."),
            notices=[N_NIKKA_WINTER, N_NIKKA_CLOSED],
            time=(VIS, "10:05〜13:00（セミナーとお昼を含む）", "10:05–13:00 (including the seminar and lunch)")),
        winery=dict(
            pre=T("13:00に駅前からタクシーで。1〜4月は火・水曜が休みです。帰りは、運上家の前まで迎えのタクシーを頼んでおきます（14:15ごろ）。休みの日は、お昼のあと駅前からタクシーで浜へ。",
                  "Taxi from the station at 13:00; closed Tuesdays and Wednesdays from January to April. Arrange a pickup around 14:15 to take you to the Unjoya, by the beach. On closing days, take a taxi from the station to the beach after lunch."),
            notices=[N_WINERY_DEC, N_YEAREND],
            time=(VIS, "13:10〜14:15", "13:10–14:15")),
        moire=dict(
            pre=T("ワイナリーからタクシーで運上家の前まで（運上家は冬は閉まっています）。そこから浜へ歩いて5分。12月は16時ごろに日が沈みます。",
                  "Taxi from the winery to the Unjoya (closed in winter), then 5 minutes’ walk to the beach. In December the sun sets around 16:00."),
            rows=[row("hours", "日の入り（札幌）：12月1日16:01、1月31日16:45、2月28日17:22、3月31日17:59", "Sunset (Sapporo): 1 Dec 16:01, 31 Jan 16:45, 28 Feb 17:22, 31 Mar 17:59")],
            time=(VIS, "14:30〜14:50", "14:30–14:50")),
        onsen=dict(
            pre=T("浜から歩いて20分ほど（雪の日は25分みておきます）。", "About 20 minutes’ walk from the beach (allow 25 in snow)."),
            time=(VIS, "15:15〜16:45", "15:15–16:45")),
        kaeri=dict(
            pre=T("宇宙の湯から歩いて15分。17:00ごろから晩ごはん、18:20に店を出て、18:35発で札幌19:58着。ゆっくりなら19:26発（20:41着）。",
                  "Fifteen minutes’ walk from Uchu no Yu. Dinner from about 17:00; leave at 18:20 for the 18:35 (Sapporo 19:58), or take the 19:26 (20:41) for a slower evening."),
            notices=[N_YEAREND],
            time=(DEP, "18:35（札幌19:58着）", "18:35 (Sapporo 19:58)")),
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
    if o.get("photos"):   # コースで最初の写真を変える（冬は雪の写真を先に）
        by = {p["file"][:-4]: p for p in photos}
        photos = [by[k] for k in o["photos"]] + [p for p in photos if p["file"][:-4] not in o["photos"]]
    out.update(lat=b["lat"], lng=b["lng"], text=text, gmaps=b["gmaps"], links=o.get("links", b.get("links", [JR])),
               notices=o.get("notices", []),
               info={"rows": o.get("rows", []) + b["rows"], "cash": False, "tip": b["tip"], "checked": CHECKED},
               photos=photos)
    assert out["photos"], sid
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


for C in (LATE, EARLY):
    N = {k: i for i, k in enumerate(C["order"], 1)}
    ns = lambda *ks: [N[k] for k in ks]
    h = lambda sid, rule, ja, en: {"spot": N[sid], "rule": rule, "text": T(ja, en)}
    picks = [N[k] for k in C["order"] if k not in ("sapporo", "eki", "kaeri")]
    auto = {str(N["sapporo"]): {"always": True}, str(N["eki"]): {"always": True}, str(N["kaeri"]): {"always": True}}
    default = picks
    if C is LATE:
        sections = [{"first": 1, "last": N["nikka"], "area": T("余市・駅前", "Yoichi · station"), "title": T("8:41の電車で余市へ、蒸溜所のツアーとお昼（予約制）", "The 8:41 train, a distillery tour and lunch (booking needed)")},
                    {"first": N["winery"], "last": N["winery"], "area": T("余市・黒川町", "Yoichi · Kurokawa"), "title": T("タクシーでワイナリーへ", "A taxi to the winery")},
                    {"first": N["fuku"], "last": N["moire"], "area": T("余市・浜中町と入舟町", "Yoichi · the shore"), "title": T("ニシン漁の時代の浜と、シリパ岬", "The herring-era shore and Cape Shiripa")},
                    {"first": N["onsen"], "last": N["kaeri"], "area": T("余市・夜", "Yoichi · evening"), "title": T("温泉と回転ずし、19:26の電車で札幌へ", "Hot spring, sushi and the 19:26 to Sapporo")}]
        hints = [
            h("fuku", {"none": ns("winery"), "andAny": ns("fuku")},
              "ワイナリーに行かない日は、お昼のあと駅前からタクシーで福原漁場へ（10分ほど）。浜と温泉の前に、よいち水産博物館（運上家の裏の小山の上、最終入館16:30）にも寄れます。",
              "Skipping the winery? Take a taxi from the station to the Fukuhara fishery after lunch (about 10 minutes). You’ll also have time for the Yoichi Fisheries Museum on the hill behind the Unjoya (last entry 16:30)."),
            h("unjo", {"none": ns("fuku")},
              "福原漁場を外す日は、ワイナリーから運上家の前までタクシーで（14:30ごろ着）。運上家の裏の小山の上のよいち水産博物館（最終入館16:30、約40分）も回れます。",
              "Without the Fukuhara fishery, take the taxi from the winery straight to the Unjoya (about 14:30). That leaves time for the Yoichi Fisheries Museum on the hill behind it (last entry 16:30, about 40 minutes)."),
            h("moire", {"none": ns("fuku", "unjo")},
              "月曜（祝日の翌日も）は福原漁場と運上家が休み。その日はワイナリーから運上家の前までタクシーで行き、浜を見てから、早めに温泉へ。",
              "On Mondays (and the day after a holiday) the fishery and the Unjoya are closed. Take the taxi from the winery to the Unjoya anyway, see the beach, and go on to the hot spring early."),
            h("kaeri", {"none": ns("onsen")},
              "温泉に行かない日は、浜から余市番屋まで歩いて20分ほど。または余市17:42発で小樽へ出て（18:08着）、小樽で晩ごはんに。",
              "Skipping the hot spring? It is about 20 minutes’ walk from the beach to Yoichi Banya, or take the 17:42 to Otaru (18:08) and have dinner there."),
        ]
        note = "「4月中旬〜12月中旬」。札幌8:41→余市10:00。ニッカ（予約。12〜1月はセミナーのみ）→タクシーで余市ワイナリー→タクシーで福原漁場→運上家→モイレの浜→宇宙の湯→余市番屋→余市19:26発（札幌20:41着）。"
    else:
        sections = [{"first": 1, "last": N["nikka"], "area": T("余市・駅前", "Yoichi · station"), "title": T("8:41の電車で余市へ、蒸溜所のセミナーとお昼（予約制）", "The 8:41 train, a distillery seminar and lunch (booking needed)")},
                    {"first": N["winery"], "last": N["winery"], "area": T("余市・黒川町", "Yoichi · Kurokawa"), "title": T("タクシーでワイナリーへ", "A taxi to the winery")},
                    {"first": N["moire"], "last": N["kaeri"], "area": T("余市・浜と夜", "Yoichi · shore and evening"), "title": T("雪のシリパ岬、温泉と回転ずし", "Cape Shiripa in snow, a hot spring and sushi")}]
        hints = [
            h("moire", {"none": ns("winery")},
              "ワイナリーに行かない日（火曜、1〜4月は水曜も休み）は、お昼のあと駅前からタクシーで運上家の前まで行き、浜へ。明るいうちに岬が見られて、温泉にも早めに入れます。",
              "Not going to the winery (closed Tuesdays, and Wednesdays from January to April)? After lunch, take a taxi from the station to the Unjoya and walk to the beach. You’ll see the cape in daylight and reach the hot spring earlier."),
            h("kaeri", {"none": ns("onsen")},
              "温泉に行かない日は、浜から余市番屋まで歩いて20分ほど。または余市17:42発で小樽へ出て（18:08着）、小樽で晩ごはんに。",
              "Skipping the hot spring? It is about 20 minutes’ walk from the beach to Yoichi Banya, or take the 17:42 to Otaru (18:08) and have dinner there."),
        ]
        note = "「冬（12月中旬〜4月上旬）」。札幌8:41→余市10:00。ニッカ（12〜1月はセミナー・予約）→タクシーで余市ワイナリー→タクシーでモイレの浜→宇宙の湯→余市番屋→余市18:35発（札幌19:58着）。"
    data = {
        "id": "yoichi", "course": C["course"],
        "_note": "余市（札幌から日帰り。yoichi/ のページ専用。形は eizan-line.json と同じ）。" + note
                 + "写真はすべて Wikimedia Commons（一覧は scripts/yoichi_web_photos.json）。info.checked と sources.checked は確認した日、sources.saw はそのページで見た内容。"
                 + "このファイルは scripts/build_yoichi_data.py で作る（直接直さない）。",
        "sections": sections, "focus": {"first": 2, "last": N["kaeri"]},
        "plan": {"_note": "defaultPicks は時間割どおりの組み合わせ。札幌駅・余市駅・晩ごはんと帰りは自動で入る。",
                 "defaultMode": "pick", "picks": picks, "defaultPicks": default, "auto": auto, "hints": hints},
        "photoBase": "../images/yoichi/", "sources": SOURCES,
        "spots": [spot(C, i, k) for i, k in enumerate(C["order"], 1)],
    }
    with open(f"{R}/data/routes/{C['file']}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", C["file"], [(s["no"], s["id"]) for s in data["spots"]], "default", default)
