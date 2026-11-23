#!/usr/bin/env python3
"""京都 今宮神社と鷹峯（光悦寺・源光庵・常照寺）のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_takagamine_data.py  （そのあと python3 scripts/sync_takagamine.py）
- 作るもの（COURSES）:
  - data/routes/takagamine.json … 「9〜10時に出発」（四条河原町9:36（日祝9:39）の市バス46系統→今宮神社前10:11着。
    今宮神社とあぶり餅→佛教大学前11:04の市バス6系統で鷹峯へ→源光庵→常照寺→光悦寺→しょうざんでお昼と庭園→歩いて金閣寺→
    金閣寺道から市バス59系統で河原町三条→夜は三条・先斗町。12月6日まではしょうざんの夜の紅葉ライトアップも）
  - data/routes/takagamine-early.json … 「鷹峯の開門に合わせる」（京都市役所前7:55（土休日8:01）の地下鉄で二条→
    二条駅前8:10（土休日8:13）の市バス6系統→鷹峯源光庵前8:32着。常照寺8:30→源光庵9:00の開門→光悦寺→市バス6系統で
    佛教大学前へ→今宮神社であぶり餅（遅めの朝ごはんのかわり）→大徳寺（黄梅院・大仙院）→泉仙でお昼→金閣寺か北野→夜は街なか）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方の一言、「選んで回る」の設定
  - SOURCES … 時刻・料金の出典と確認日（データの sources に入る）
- 出発地は京都の中心・三条のあたり（京都市役所前・三条・京都河原町）。宿の名前は書かない
- 写真は images/takagamine/ にあるものだけ（足していない）。鷹峯は2025年11月4日、今宮神社は2026年5月15日
- 大徳寺・しょうざん・金閣寺・船岡温泉は写真がないので、スポットにせず、最後のスポットの文章で案内する
- 2026-11-23 要確認の調べ直し：一和の時間・源光庵の拝観料は京都府観光連盟、船岡温泉は京都府浴場組合（1010.kyoto）で確認
- 2026-11-22 オーナーの基準で作り直した（ゲストが実際に回れる1日。開門コースと9〜10時発コース、お昼の場所と時間、帰りのバス、夜）
"""
import copy, json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "takagamine"
IMG = f"{R}/images/{MAP_ID}"
CHECKED = "2026-11-22"


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def info(rows, source, tip=None, verified=True, cash=False, checked=CHECKED):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked, "source": source}
    if not verified:
        d["verified"] = False
    return d


def own(pid, nums):
    return [f"{pid}-{i}.jpg" for i in nums]


PHOTOS = {
    "imamiya": own("imamiya", [1, 2, 3, 4]),
    "koetsuji": own("koetsuji", [1, 2, 3, 5, 6, 7]),
    "genkoan": own("genkoan", [1, 2, 3, 4, 5, 7, 8]),
    "joshoji": own("joshoji", [1, 2, 3, 4, 5, 6, 7]),
}

BUS_URL = "https://www2.city.kyoto.lg.jp/kotsu/busdia/bustime.htm"
CITYBUS = link("timetable", "市バス 停留所ごとの時刻表（京都市交通局）", "Kyoto City Bus timetables by stop (Japanese)", BUS_URL)
YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
NAVI_KOETSU = "https://ja.kyoto.travel/tourism/single01.php?category_id=7&tourism_id=279"
MOMIJI = "https://ja.kyoto.travel/flower/momiji/"
KANKO_ICHIWA = "https://www.kyoto-kankou.or.jp/info_search/680"
KANKO_KAZARI = "https://www.kyoto-kankou.or.jp/info_search/681"
KANKO_ABURI = "https://www.kyoto-kankou.or.jp/info_search/8455"
KANKO_GENKOAN = "https://www.kyoto-kankou.or.jp/info_search/9493"
SENTO_FUNAOKA = "https://1010.kyoto/spot/funaokaonsen/"
SENTO_HOWTO = "https://1010.kyoto/how_to_use/"
PREF_SENTO_FEE = "https://www.pref.kyoto.jp/seikatsu/news/press/2025/3/nyuyokuryoukintouseigaku.html"
SHOZAN = "https://www.shozan.co.jp/"
SHOZAN_GARDEN = "https://www.shozan.co.jp/sansaku/index.html"
SHOZAN_LIGHT = "https://www.shozan.co.jp/topic/lightup.html"
SHOZAN_WAKADORI = "https://www.shozan.co.jp/restaurant/wakadori.html"
SHOZAN_LOURAN = "https://www.shozan.co.jp/restaurant/louran.html"
OUBAI = "https://kyotoshunju.com/temple/daitokuji-oubaiin/"
DAISEN = "https://daisen-in.net/fee_information/"
IZUSEN = "https://kyoto-izusen.com/html2/restrant_daijiin.html"
KINKAKU = "https://www.shokoku-ji.jp/kinkakuji/access/"
KINKAKU_MAP = link("info", "金閣寺〜北野のマップ（金閣寺・龍安寺・北野天満宮）", "Kinkaku-ji to Kitano map (Kinkaku-ji, Ryoan-ji, Kitano Tenmangu)", "../kinkakuji/#list")
EIZAN = link("info", "叡山電鉄のマップ（夜の祇園四条・先斗町は24〜26番）", "Eizan Railway map (evening stops 24–26)", "../eizan-line/#list")

SEASON = notice("紅葉の見ごろは例年11月中旬〜下旬", "Autumn leaves: usually mid to late November",
                "京都観光Navi（京都市）の紅葉だよりでは、例年の見ごろは源光庵・しょうざんリゾート京都・大徳寺黄梅院が11月中旬〜下旬です。年によって前後するので、行く前に紅葉だよりを見てください。鷹峯の写真は2025年11月4日、今宮神社は2026年5月に撮ったものです。",
                "Kyoto City’s autumn-leaf report gives the usual peak at Genkoan, Shozan Resort Kyoto and Daitoku-ji’s Obai-in as mid to late November. It shifts from year to year, so check the report before you go. My Takagamine photos are from 4 November 2025; Imamiya’s from May 2026.",
                url=MOMIJI, frm="2026-10-01", to="2026-12-06")
WINTER = notice("紅葉が終わったあと（12月〜2月）", "After the leaves have gone (December–February)",
                "お寺はふだんどおり開いています。光悦寺は紅葉の時期が終わると8:00から・400円（京都観光Navi）。12月7日からは、しょうざんの夜のライトアップと大徳寺黄梅院の特別公開はありません。大徳寺では一年中開いている大仙院へ。あぶり餅の2軒は12月16日〜31日がお休みです。12月29日〜1月3日の市バスは休日の時刻で走ります。",
                "The temples keep their usual hours; Koetsuji opens at 8:00 and costs ¥400 outside the autumn season (Kyoto Kanko Navi). From 7 December there is no evening light-up at Shozan and no special opening at Daitoku-ji’s Obai-in; go to Daisen-in, open all year. Both aburi-mochi shops close from 16 to 31 December. From 29 December to 3 January city buses run to the Sunday/holiday timetable.",
                url=BUS_URL, frm="2026-12-07", to="2027-02-28")
ABURI_YEAREND = notice("あぶり餅は12月16日〜31日お休み", "Aburi-mochi: closed 16–31 December",
                       "一和・かざりやの2軒とも、年末（12月16日〜31日）はお休みです（京都府観光連盟の案内）。今宮神社のお参りはできます。",
                       "Both Ichiwa and Kazariya close at the end of the year, 16–31 December (Kyoto Prefecture tourism guide). You can still visit the shrine.",
                       url=KANKO_KAZARI, frm="2026-12-10", to="2026-12-31")
LIGHTUP = notice("しょうざん庭園の秋の紅葉ライトアップ（12月6日まで）", "Shozan garden autumn light-up (until 6 December)",
                 "2026年10月31日〜12月6日、17:30〜20:00（最終受付19:30）、入園料800円（しょうざんの公式サイト）。鷹峯から歩いて15分ほど。晩ごはんは中にある中国料理の楼蘭（17:00〜21:00、ラストオーダー20:30、年中無休）か、鳥料理と和食のわかどり（17:00〜22:00、ラストオーダー21:30、休業日はサイトのカレンダー）。帰りは土天井町から市バス北1系統で北大路バスターミナルへ約17分、地下鉄で三条のあたりへ（北1系統の最終は22:37発）。",
                 "31 October – 6 December 2026, 17:30–20:00 (last entry 19:30), ¥800 (Shozan website). About 15 minutes’ walk from Takagamine. For dinner inside: Louran, Chinese (17:00–21:00, last orders 20:30, open every day), or Wakadori, chicken and Japanese (17:00–22:00, last orders 21:30; closing days on its calendar). Back by city bus Kita-1 from Dotenjocho to Kitaoji bus terminal (about 17 minutes), then the subway to the Sanjo area (last Kita-1 at 22:37).",
                 url=SHOZAN_LIGHT, frm="2026-10-31", to="2026-12-06")
OUBAI_N = notice("大徳寺黄梅院の秋の特別公開（12月6日まで）", "Daitoku-ji Obai-in: autumn opening (until 6 December)",
                 "2026年10月9日〜12月6日、10:00〜15:45（受付終了）、大人1,000円・現金のみ（京都春秋）。静止画は撮れますが、人物を入れた撮影・自撮り棒・三脚は禁止です。法務で休みが増えることがあります。",
                 "9 October – 6 December 2026, 10:00–15:45 (last entry), ¥1,000, cash only (Kyoto Shunju). Still photos are allowed, but not of people, and no selfie sticks or tripods. Extra closing days are possible for temple services.",
                 url=OUBAI, frm="2026-10-09", to="2026-12-06")

# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    imamiya=dict(
        name=T("今宮神社とあぶり餅", "Imamiya Shrine & aburi-mochi"), kind=T("神社・おやつ", "Shrine & snack"),
        blurb=T("朱の楼門の今宮神社。東門の前では、向かい合う2軒の茶店が、平安時代から続くあぶり餅を焼いています。",
                "Imamiya Shrine with its vermilion gate; outside the east gate, two facing teahouses grill aburi-mochi, made here since the Heian period."),
        caution=T("あぶり餅の2軒は水曜休み（1日・15日・祝日なら翌日）、12月16日〜31日も休み", "Both aburi-mochi shops close on Wednesdays (Thursday if the 1st, 15th or a holiday) and 16–31 December"),
        lat=35.04560, lng=135.74213,
        body=T("今宮神社（いまみやじんじゃ）とあぶり餅\n\n"
               "朱色の楼門をくぐると、広い境内に本殿が建ちます。東門を出た参道では、「一和（いちわ。一文字屋和輔）」と「かざりや」の2軒が向かい合っています。"
               "竹ぐしに刺した小さなお餅を炭火であぶり、白みそのたれをからめた「あぶり餅」。一和は平安時代（長保2年＝1000年）から続く店です。"
               "1人前600円（京都府観光連盟の案内）。どちらに入っても同じ値段です。\n\n"
               "2軒とも10:00〜17:00。水曜休み（1日・15日・祝日が水曜日のときは翌日）、12月16日〜31日もお休みです（京都府観光連盟の案内）。\n\n"
               "バス停は「今宮神社前」（市バス46系統）と、歩いて5〜7分の「佛教大学前」（6・北1・46系統。鷹峯行きはここから）。大徳寺は南へ歩いて10分ほどです。",
               "Imamiya Shrine and aburi-mochi\n\n"
               "Through the vermilion gate is a broad precinct and the main hall. On the lane outside the east gate, two teahouses face each other: Ichiwa (Ichimonjiya Wasuke) and Kazariya. "
               "Small bamboo-skewered rice cakes are toasted over charcoal and coated in sweet white-miso sauce; Ichiwa has been making them since the year 1000. "
               "¥600 a portion at either shop (Kyoto Prefecture tourism guide).\n\n"
               "Both are open 10:00–17:00 and close on Wednesdays (on Thursday instead when the 1st, the 15th or a holiday falls on a Wednesday) and from 16 to 31 December (Kyoto Prefecture tourism guide).\n\n"
               "Bus stops: “Imamiya-jinja-mae” (city bus 46), and “Bukkyo-daigaku-mae”, 5–7 minutes’ walk (buses 6, Kita-1 and 46; buses up to Takagamine leave from here). Daitoku-ji is about 10 minutes’ walk south."),
        gmaps=[gm("今宮神社", "Imamiya Shrine", 35.04560, 135.74213, "今宮神社 京都市北区"),
               gm("あぶり餅 かざりや", "Kazariya", 35.04521, 135.74279, "あぶり餅 かざりや"),
               gm("佛教大学前バス停", "Bukkyo-daigaku-mae bus stop", 35.04590, 135.73904, "佛教大学前 バス停 今宮通")],
        links=[link("official", "今宮神社 公式サイト（交通案内）", "Imamiya Shrine: access (official, Japanese)", "http://www.imamiyajinja.org/access/"),
               link("info", "あぶり餅 2軒の時間と休み（京都府観光連盟）", "Both aburi-mochi shops: hours and closing days (Kyoto Prefecture tourism, Japanese)", KANKO_ABURI),
               link("info", "あぶり餅 一和（京都府観光連盟）", "Ichiwa aburi-mochi (Kyoto Prefecture tourism, Japanese)", KANKO_ICHIWA),
               link("info", "あぶり餅 かざりや（京都府観光連盟）", "Kazariya aburi-mochi (Kyoto Prefecture tourism, Japanese)", KANKO_KAZARI), CITYBUS],
        notices=[ABURI_YEAREND],
        _rows=[row("hours", "社務所（電話の受付）9:00〜17:00", "Shrine office (phone) 9:00–17:00"),
               row("fee", "あぶり餅 1人前600円（一和・かざりやとも10:00〜17:00）", "Aburi-mochi ¥600 a portion (Ichiwa and Kazariya both 10:00–17:00)"),
               row("closed", "あぶり餅の2軒：水曜（1日・15日・祝日なら翌日）、12月16日〜31日", "Both aburi-mochi shops: Wednesdays (Thursday if the 1st, 15th or a holiday), and 16–31 December")],
        _tip=T("今宮神社の公式サイト（交通案内）と、京都府観光連盟の案内（あぶり餅の2軒）で確認しました（11月23日）。",
               "Checked on the shrine’s access page and the Kyoto Prefecture tourism guide for the two shops (23 November)."),
        _source="今宮神社 公式サイト（交通案内）、京都府観光連盟（あぶり餅、あぶり餅 一和・かざりや）。2026-11-23に確認",
        _checked="2026-11-23"),
    koetsuji=dict(
        name=T("光悦寺", "Koetsuji"), kind=T("寺", "Temple"),
        blurb=T("江戸時代の芸術家・本阿弥光悦が開いた芸術村の跡。もみじのトンネルの参道と、竹を組んだ「光悦垣」。",
                "The site of the artists’ village founded by Hon’ami Koetsu: a tunnel of maples and the woven bamboo “Koetsu fence”."),
        caution=T("紅葉の時期は8:30から・500円。毎年11月10日〜13日は拝観できません", "In autumn from 8:30, ¥500. Closed every year 10–13 November"),
        lat=35.05352, lng=135.73019,
        body=T("光悦寺（こうえつじ）\n\n"
               "江戸時代のはじめ、書や陶芸で知られる本阿弥光悦（ほんあみこうえつ）が徳川家康からこの地をもらい、職人たちと芸術村を開いた所です。"
               "石畳の参道はもみじのトンネルになり、境内には竹を斜めに組んだ「光悦垣」や茶室が点在します。鷹ヶ峰・鷲ヶ峰の山並みが目の前です。\n\n"
               "「鷹峯源光庵前」バス停から歩いて約4分、源光庵からも約4分（地図で見た目安）。\n\n"
               "拝観は8:00〜17:00（紅葉の時期は8:30から）、400円（紅葉の時期は500円）。毎年11月10日〜13日は拝観できません（京都観光Navi）。お寺の公式サイトは見つかりませんでした。",
               "Koetsuji\n\n"
               "In the early Edo period, Hon’ami Koetsu, famous for calligraphy and pottery, was given this land by Tokugawa Ieyasu and founded an artists’ village with craftsmen. "
               "The stone-paved approach becomes a tunnel of maples; the grounds hold teahouses and the “Koetsu-gaki”, a fence of diagonally woven bamboo, with Takagamine’s hills right in front.\n\n"
               "About 4 minutes’ walk from the “Takagamine-Genkoan-mae” bus stop, and about 4 from Genkoan (map estimate).\n\n"
               "Open 8:00–17:00 (from 8:30 in the autumn-leaf season), ¥400 (¥500 in autumn). Closed every year from 10 to 13 November (Kyoto Kanko Navi). No temple website was found."),
        gmaps=[gm("光悦寺", "Koetsuji", 35.05352, 135.73019, "光悦寺 鷹峯")],
        links=[link("info", "光悦寺（京都観光Navi）", "Koetsuji (Kyoto Kanko Navi, Japanese)", NAVI_KOETSU)],
        _rows=[row("hours", "8:00〜17:00（紅葉の時期は8:30から）", "8:00–17:00 (from 8:30 in autumn-leaf season)"),
               row("closed", "毎年11月10日〜13日", "10–13 November every year"),
               row("fee", "400円（紅葉の時期は500円）", "¥400 (¥500 in autumn-leaf season)")],
        _tip=T("京都観光Navi（京都市）で確認しました（11月22日）。お寺の公式サイトは見つかりませんでした。", "Checked on Kyoto Kanko Navi (Kyoto City) on 22 November; no temple website was found."),
        _source="京都観光Navi 光悦寺（営業時間・拝観料・休み）。2026-11-22に確認"),
    genkoan=dict(
        name=T("源光庵", "Genkoan"), kind=T("寺", "Temple"),
        blurb=T("丸窓のある山門と、本堂から眺める静かな庭。四角い「迷いの窓」と丸い「悟りの窓」で知られるお寺です。",
                "A gate with a round window and a quiet garden seen from the main hall; famous for its square “Window of Confusion” and round “Window of Enlightenment”."),
        caution=T("9:00〜17:00（受付16:30まで）。大人400円（紅葉の時期は500円）。靴を入れる袋を持って", "9:00–17:00 (last entry 16:30). ¥400 (¥500 in autumn-leaf season). Bring a bag for your shoes"),
        lat=35.05484, lng=135.73182,
        body=T("源光庵（げんこうあん）\n\n"
               "「鷹峯源光庵前」バス停のすぐそば。丸い窓のある山門をくぐると、本堂の縁側から苔と植え込みの庭が眺められます。"
               "本堂の四角い「迷いの窓」と丸い「悟りの窓」は、人の一生と悟りの心を表すといわれ、紅葉の時期は窓の外が赤く染まります。窓の前は、人が少ない朝のうちが落ち着いて座れます。\n\n"
               "本堂の天井は、伏見城の遺構の「血天井」です。\n\n"
               "本堂に上がるので、脱いだ靴を入れる袋を持っていきましょう（お寺のお願い）。お寺の行事があるときは、拝観を止めることがあります。"
               "拝観料は大人（中学生以上）400円、紅葉の時期は500円、小学生200円（京都府観光連盟の案内。お寺のサイトには書かれていません）。2026年は11月14日〜12月6日、駐車場が使えません。",
               "Genkoan\n\n"
               "Right by the “Takagamine-Genkoan-mae” bus stop. Through a gate with a round window, look out from the main hall’s veranda over a garden of moss and clipped shrubs. "
               "The hall’s square “Window of Confusion” and round “Window of Enlightenment” are said to stand for human life and an enlightened mind; in autumn the view through them turns red. Early in the day, with fewer people, you can sit in front of the windows in peace.\n\n"
               "The hall’s ceiling is the “blood ceiling”, a remnant of Fushimi Castle.\n\n"
               "You take your shoes off for the hall, so bring a bag for them (the temple asks visitors to). Visits are suspended during temple events. "
               "Admission is ¥400 for adults (junior high and up), ¥500 in the autumn-leaf season, ¥200 for elementary pupils (Kyoto Prefecture tourism guide; the temple website doesn’t list it). In 2026 the car park is closed from 14 November to 6 December."),
        gmaps=[gm("源光庵", "Genkoan", 35.05484, 135.73182, "源光庵 鷹峯"),
               gm("鷹峯源光庵前バス停", "Takagamine-Genkoan-mae bus stop", 35.05432, 135.73237, "鷹峯源光庵前 バス停")],
        links=[link("official", "源光庵 公式サイト", "Genkoan (official, Japanese)", "https://genkouan.or.jp/"),
               link("info", "源光庵のお知らせ", "Genkoan notices (Japanese)", "https://genkouan.or.jp/notice/"),
               link("info", "源光庵（京都府観光連盟。拝観料）", "Genkoan (Kyoto Prefecture tourism: admission, Japanese)", KANKO_GENKOAN)],
        _rows=[row("hours", "9:00〜17:00（受付は16:30まで）。行事の日は拝観中止のことあり", "9:00–17:00 (last entry 16:30); closed during temple events"),
               row("fee", "大人（中学生以上）400円（紅葉の時期は500円）、小学生200円", "¥400 adults (junior high and up; ¥500 in autumn-leaf season), ¥200 elementary")],
        _tip=T("時間とお知らせは源光庵の公式サイト（11月22日）、拝観料は京都府観光連盟の案内（11月23日）で確認しました。お寺のサイトには拝観料が書かれていません。",
               "Hours and notices checked on the temple website (22 November), admission on the Kyoto Prefecture tourism guide (23 November); the temple website doesn’t list the fee."),
        _source="源光庵 公式サイト（拝観時間、お知らせ 2026-11-09「駐車場ご利用休止のご案内（11月14日～12月6日）」、靴袋のお願い、アクセス）2026-11-22に確認。拝観料は京都府観光連盟（源光庵）2026-11-23に確認",
        _checked="2026-11-23"),
    joshoji=dict(
        name=T("常照寺", "Joshoji"), kind=T("寺", "Temple"),
        blurb=T("江戸時代の名妓・吉野太夫が寄進した朱の「吉野門」。丸い窓の茶室と、もみじの庭。",
                "The vermilion “Yoshino gate” donated by the famed Edo-era courtesan Yoshino Tayu, a round-windowed teahouse and a maple garden."),
        caution=T("8:30〜17:00。大人400円", "8:30–17:00. ¥400"),
        lat=35.05525, lng=135.73283,
        body=T("常照寺（じょうしょうじ）\n\n"
               "源光庵から歩いて2分。参道の先の朱色の山門は、江戸時代の名妓・吉野太夫（よしのたゆう）が寄進したと伝わる「吉野門」です。"
               "境内には丸い窓の茶室や、池のある庭があり、春は桜、秋はもみじがきれいです。\n\n"
               "庭園と堂内の拝観は8:30〜17:00、大人400円・小学生200円（お寺のサイト）。",
               "Joshoji\n\n"
               "Two minutes’ walk from Genkoan. The vermilion gate at the end of the approach is the “Yoshino-mon”, said to have been donated by Yoshino Tayu, a celebrated courtesan of the Edo period. "
               "The grounds hold a teahouse with a round window and a pond garden: cherries in spring, maples in autumn.\n\n"
               "The garden and halls are open 8:30–17:00; ¥400 adults, ¥200 elementary (temple website)."),
        gmaps=[gm("常照寺", "Joshoji", 35.05525, 135.73283, "常照寺 鷹峯")],
        links=[link("official", "常照寺（お寺のサイト）", "Joshoji (temple site, Japanese)", "http://tsakae.justhpbs.jp/joshoji/toppage.html")],
        _rows=[row("hours", "8:30〜17:00", "8:30–17:00"),
               row("fee", "大人400円、小学生200円", "¥400 adults, ¥200 elementary")],
        _tip=T("常照寺のサイト（トップ・アクセス・行事）で確認しました（11月22日）。", "Checked on the temple website (top, access and events pages) on 22 November."),
        _source="常照寺 公式サイト（トップの拝観時間・拝観志納金、アクセス、行事）。2026-11-22に確認"),
)

VIS, ARR = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time")

# ---------------------------------------------------------------------------
# 最後のスポットのあとに続ける文章（コースごと）
# ---------------------------------------------------------------------------
AFTER_LATE = T(
    "お昼は、しょうざんで（13:30ごろ）\n\n"
    "光悦寺から鷹峯の街道を南へ下ると、しょうざんリゾート京都の西門です（歩いて15分ほど。地図で見た目安）。広い日本庭園の中に料理店があります（しょうざんの公式サイト）。\n"
    "・わかどり（鳥料理と和食）：ランチ11:30〜14:30（ラストオーダー14:00）。休業日はサイトのカレンダーで。\n"
    "・楼蘭（中国料理）：ランチは平日12:00〜、土日祝11:30〜、14:30まで（ラストオーダーは平日14:00・土日祝14:30）。年中無休。\n"
    "ラストオーダーが14時なので、13時半までに入ってください。\n\n"
    "食べたら、北庭の日本庭園へ（9:00〜17:00、無休。一般500円、店で食事をした人は300円）。紙屋川の流れと、茶室や屋敷が点在する庭です。\n\n"
    "金閣寺へ歩いて下りる（15:00ごろ）\n"
    "しょうざんから金閣寺までは、歩いて25分ほど（地図で見た目安）。金閣寺は9:00〜17:00、大人500円（相国寺の公式サイト）。15時半ごろに入れば、閉まるまで1時間あります。金閣寺から先、北野天満宮や龍安寺へ回るなら、同じサイトの「金閣寺〜北野」のマップを見てください。\n\n"
    "帰りと、夜\n"
    "金閣寺道から市バス59系統で河原町三条へ約30分・230円（平日16:35発→17:05着。日中は15〜20分おき。59系統の最終は20:39発）。三条大橋のまわりの木屋町通（きやまちどおり）と先斗町（ぽんとちょう）には、遅くまで開いている店が並びます。閉まる時間とラストオーダーは店ごとに違うので、入る前に表の案内で確かめてください。店を決めておきたい人は、叡山電鉄のマップの24〜26番も見てください。\n\n"
    "12月6日までは、金閣寺のかわりに、しょうざんの夜の紅葉ライトアップ（17:30〜20:00）もあります。このスポットの「お知らせ」を見てください。\n\n"
    "船岡温泉（ふなおかおんせん）は、今宮神社の南、船岡山のふもとの古い銭湯です。Toshiも入りに行く銭湯で、タトゥーがあっても入れるはずです（念のため入口で確かめてください）。京都府浴場組合のサイトでは、15:00〜23:30（日曜は8:00から）、火曜休み、大人550円（京都の銭湯は同じ料金）。組合の英語のページは時間と休みが違う書き方なので、行く前に電話（075-441-3735）で確かめると安心です。行くなら、千本鞍馬口のバス停から歩いて6分ほど（地図で見た目安）。",
    "Lunch at Shozan (around 13:30)\n\n"
    "From Koetsuji, walk south down the old Takagamine road to the west gate of Shozan Resort Kyoto (about 15 minutes; map estimate). Its restaurants sit inside a large Japanese garden (Shozan website):\n"
    "• Wakadori (chicken and Japanese): lunch 11:30–14:30 (last orders 14:00). Closing days are on its online calendar.\n"
    "• Louran (Chinese): lunch from 12:00 on weekdays, from 11:30 at weekends and on holidays, until 14:30 (last orders 14:00 on weekdays, 14:30 at weekends). Open every day.\n"
    "With last orders at 14:00, get there by 13:30.\n\n"
    "After lunch, walk round the north garden (9:00–17:00, open every day; ¥500, or ¥300 if you ate at one of the restaurants): the Kamiya river runs through it past teahouses and old houses.\n\n"
    "Walk down to Kinkaku-ji (around 15:00)\n"
    "From Shozan to Kinkaku-ji is about 25 minutes on foot (map estimate). Kinkaku-ji is open 9:00–17:00, ¥500 (Shokoku-ji website). In by about 15:30 gives you an hour before it closes. To go on to Kitano Tenmangu or Ryoan-ji, see the Kinkaku-ji to Kitano map on this site.\n\n"
    "Back to town, and the evening\n"
    "City bus 59 from Kinkakuji-michi to Kawaramachi-Sanjo takes about 30 minutes, ¥230 (weekdays 16:35 → 17:05; every 15–20 minutes in the daytime; the last 59 leaves at 20:39). Around Sanjo Ohashi bridge, Kiyamachi-dori and Pontocho are lined with places that stay open late. Closing times and last orders differ, so check the sign at the door. If you’d rather have a place picked out, see stops 24–26 on the Eizan Railway map.\n\n"
    "Until 6 December there is also Shozan’s evening autumn light-up (17:30–20:00) instead of Kinkaku-ji: see the notes at the top of this spot.\n\n"
    "Funaoka Onsen, south of Imamiya at the foot of Funaokayama hill, is an old public bath. Toshi bathes here himself, and tattoos should be fine (ask at the entrance to be sure). The Kyoto bathhouse association’s site gives 15:00–23:30 (from 8:00 on Sundays), closed on Tuesdays, ¥550 for adults (the standard Kyoto sento price). Its English page lists different hours (15:00–1:00, open every day), so it’s worth phoning ahead (075-441-3735). It’s about 6 minutes’ walk from the Senbon-Kuramaguchi bus stop (map estimate).")

AFTER_EARLY = T(
    "大徳寺へ歩いて（11:45ごろ）\n\n"
    "今宮神社から南へ歩いて10分ほどで、大徳寺（だいとくじ）の境内です。土塀に囲まれた塔頭（たっちゅう。小さなお寺）が並びます。\n"
    "・黄梅院（おうばいいん）：秋の特別公開は2026年10月9日〜12月6日、10:00〜15:45（受付終了）、大人1,000円・現金のみ（京都春秋）。千利休が作ったと伝わる庭があります。\n"
    "・大仙院（だいせんいん）：一年中、9:00〜16:30。大人500円、お抹茶500円。年中無休（大仙院の公式サイト。臨時で時間を変えることがあり、日ごとの時間はサイトのカレンダーで）。\n\n"
    "お昼（12:45ごろ）\n"
    "大徳寺の中、大慈院の泉仙（いずせん）で精進料理を。11:00〜16:00（ラストオーダー）、年中無休（12月28日〜31日は休み）、6人以上は予約。あやめ4,500円から（泉仙の公式サイト）。\n\n"
    "午後（14時ごろから）\n"
    "大徳寺前から市バス12系統（金閣寺・立命館大学行き）で金閣寺道まで6分・230円（日中は12〜15分おき）。金閣寺は9:00〜17:00、大人500円（相国寺の公式サイト）。その先の北野天満宮や龍安寺は、同じサイトの「金閣寺〜北野」のマップに書いています。\n"
    "12月6日までは、金閣寺から歩いて25分ほど（地図で見た目安）上ると、しょうざんの庭園（昼は17:00まで）と、夜の紅葉ライトアップ（17:30〜20:00）。このスポットの「お知らせ」を見てください。\n\n"
    "帰りと、夜\n"
    "金閣寺道から市バス59系統で河原町三条へ約30分・230円（日中は15〜20分おき。最終は20:39発）。三条大橋のまわりの木屋町通と先斗町には、遅くまで開いている店が並びます。閉まる時間とラストオーダーは店ごとに違うので、入る前に表の案内で確かめてください。叡山電鉄のマップの24〜26番も見てください。\n\n"
    "船岡温泉は、大徳寺の南西、船岡山のふもとの古い銭湯です。Toshiも入りに行く銭湯で、タトゥーがあっても入れるはずです（念のため入口で確かめてください）。京都府浴場組合のサイトでは、15:00〜23:30（日曜は8:00から）、火曜休み、大人550円（京都の銭湯は同じ料金）。組合の英語のページは時間と休みが違う書き方なので、行く前に電話（075-441-3735）で確かめると安心です。",
    "Walk to Daitoku-ji (around 11:45)\n\n"
    "About 10 minutes’ walk south of Imamiya Shrine lies Daitoku-ji, a precinct of sub-temples behind earthen walls.\n"
    "• Obai-in: autumn special opening 9 October – 6 December 2026, 10:00–15:45 (last entry), ¥1,000, cash only (Kyoto Shunju). Its garden is said to be the work of Sen no Rikyu.\n"
    "• Daisen-in: open all year, 9:00–16:30, ¥500, matcha ¥500, open every day (Daisen-in website; hours can change at short notice, so see its calendar).\n\n"
    "Lunch (around 12:45)\n"
    "Buddhist vegetarian cooking at Izusen in Daiji-in, inside Daitoku-ji: 11:00–16:00 (last orders), open every day except 28–31 December, groups of six or more should book. Sets from ¥4,500 (Izusen website).\n\n"
    "The afternoon (from about 14:00)\n"
    "City bus 12 (for Kinkaku-ji/Ritsumeikan University) from Daitokuji-mae to Kinkakuji-michi takes 6 minutes, ¥230 (every 12–15 minutes in the daytime). Kinkaku-ji is open 9:00–17:00, ¥500 (Shokoku-ji website). For Kitano Tenmangu and Ryoan-ji beyond, see the Kinkaku-ji to Kitano map on this site.\n"
    "Until 6 December, a walk of about 25 minutes uphill from Kinkaku-ji (map estimate) brings you to Shozan’s garden (daytime until 17:00) and its evening autumn light-up (17:30–20:00): see the notes at the top of this spot.\n\n"
    "Back to town, and the evening\n"
    "City bus 59 from Kinkakuji-michi to Kawaramachi-Sanjo takes about 30 minutes, ¥230 (every 15–20 minutes in the daytime; the last at 20:39). Around Sanjo Ohashi bridge, Kiyamachi-dori and Pontocho are lined with places that stay open late. Closing times and last orders differ, so check the sign at the door. See also stops 24–26 on the Eizan Railway map.\n\n"
    "Funaoka Onsen, south-west of Daitoku-ji at the foot of Funaokayama hill, is an old public bath. Toshi bathes here himself, and tattoos should be fine (ask at the entrance to be sure). The Kyoto bathhouse association’s site gives 15:00–23:30 (from 8:00 on Sundays), closed on Tuesdays, ¥550 for adults (the standard Kyoto sento price). Its English page lists different hours (15:00–1:00, open every day), so it’s worth phoning ahead (075-441-3735).")

LINKS_LATE = [link("official", "しょうざん 日本庭園", "Shozan Japanese garden (Japanese)", SHOZAN_GARDEN),
              link("official", "しょうざん わかどり", "Shozan: Wakadori (Japanese)", SHOZAN_WAKADORI),
              link("official", "しょうざん 楼蘭", "Shozan: Louran (Japanese)", SHOZAN_LOURAN),
              link("official", "金閣寺（参拝時間・料金）", "Kinkaku-ji: hours and fees (Japanese)", KINKAKU), KINKAKU_MAP, EIZAN, CITYBUS]
LINKS_EARLY = [link("official", "大徳寺 黄梅院（京都春秋）", "Daitoku-ji Obai-in (Kyoto Shunju, Japanese)", OUBAI),
               link("official", "大徳寺 大仙院", "Daitoku-ji Daisen-in (Japanese)", DAISEN),
               link("official", "泉仙 大慈院店", "Izusen, Daiji-in (Japanese)", IZUSEN),
               link("official", "金閣寺（参拝時間・料金）", "Kinkaku-ji: hours and fees (Japanese)", KINKAKU), KINKAKU_MAP, EIZAN, CITYBUS]
GMAPS_LATE = [gm("しょうざんリゾート京都", "Shozan Resort Kyoto", 35.05092, 135.73227, "しょうざんリゾート京都"),
              gm("金閣寺", "Kinkaku-ji", 35.03937, 135.72924, "金閣寺"),
              gm("金閣寺道バス停", "Kinkakuji-michi bus stop", 35.03690, 135.73300, "金閣寺道 バス停")]
GMAPS_EARLY = [gm("大徳寺 黄梅院", "Daitoku-ji Obai-in", 35.04330, 135.74600, "大徳寺 黄梅院"),
               gm("大徳寺 大仙院", "Daitoku-ji Daisen-in", 35.04420, 135.74610, "大徳寺 大仙院"),
               gm("泉仙 大慈院店", "Izusen, Daiji-in", 35.04250, 135.74560, "泉仙 大慈院店"),
               gm("大徳寺前バス停", "Daitokuji-mae bus stop", 35.04078, 135.74788, "大徳寺前 バス停 北大路通")]

BACK_LATE = [
    row("hours", "しょうざん：庭園 9:00〜17:00・無休・500円（食事をした人は300円）／わかどり ランチ11:30〜14:30（LO14:00）／楼蘭 ランチ 平日12:00〜・土日祝11:30〜14:30（LO 平日14:00・土日祝14:30）、年中無休",
        "Shozan: garden 9:00–17:00, open daily, ¥500 (¥300 after a meal) / Wakadori lunch 11:30–14:30 (LO 14:00) / Louran lunch from 12:00 weekdays, 11:30 weekends–14:30 (LO 14:00 weekdays, 14:30 weekends), open daily"),
    row("hours", "金閣寺 9:00〜17:00・年中無休、大人500円", "Kinkaku-ji 9:00–17:00, open daily, ¥500"),
    row("train", "帰り：金閣寺道 → 河原町三条 市バス59系統 約30分・230円（平日16:35発→17:05着。最終20:39発）",
        "Back: Kinkakuji-michi → Kawaramachi-Sanjo, city bus 59, about 30 min, ¥230 (weekdays 16:35 → 17:05; last 20:39)"),
    row("train", "しょうざんから：土天井町 → 北大路バスターミナル 市バス北1系統 約17分（最終22:37発）、地下鉄で京都市役所前へ（平日21:30発なら22:14着）",
        "From Shozan: Dotenjocho → Kitaoji bus terminal, city bus Kita-1, about 17 min (last 22:37), then the subway to Kyoto Shiyakusho-mae (the 21:30 bus gets you there at 22:14 on weekdays)"),
]
BACK_EARLY = [
    row("hours", "大徳寺：大仙院 9:00〜16:30・500円・年中無休／黄梅院 10:00〜15:45（受付終了）・1,000円・現金のみ（12月6日まで）",
        "Daitoku-ji: Daisen-in 9:00–16:30, ¥500, open daily / Obai-in 10:00–15:45 (last entry), ¥1,000, cash only (until 6 Dec)", until="2026-12-06"),
    row("hours", "大徳寺：大仙院 9:00〜16:30・500円・年中無休", "Daitoku-ji: Daisen-in 9:00–16:30, ¥500, open daily", frm="2026-12-07"),
    row("hours", "泉仙 大慈院店 11:00〜16:00（LO）・年中無休（12月28日〜31日休み）、あやめ4,500円から", "Izusen, Daiji-in 11:00–16:00 (last orders), open daily (closed 28–31 Dec), sets from ¥4,500"),
    row("train", "大徳寺前 → 金閣寺道 市バス12系統 6分・230円。金閣寺 9:00〜17:00・500円",
        "Daitokuji-mae → Kinkakuji-michi, city bus 12, 6 min, ¥230. Kinkaku-ji 9:00–17:00, ¥500"),
    row("train", "帰り：金閣寺道 → 河原町三条 市バス59系統 約30分・230円（最終20:39発）",
        "Back: Kinkakuji-michi → Kawaramachi-Sanjo, city bus 59, about 30 min, ¥230 (last 20:39)"),
]
BACK_TIP = T("市バスは京都市交通局の停留所ごとの時刻表（2026年3月20日改正）、地下鉄と乗り継ぎは乗換案内（Yahoo!路線情報）で、11月22日に確認しました。紅葉の時期は道が混んで、バスが遅れることがあります。",
             "City bus times are from the Kyoto City Transportation Bureau’s stop timetables (revised 20 March 2026), the subway and connections from a route planner, all checked on 22 November. In the autumn season traffic can make buses late.")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
# （スポットの id, 時間の見出し, 時間（日本語）, 時間（英語）, そのコースでの一言）
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="takagamine.json",
        note="「9〜10時に出発」コース。四条河原町9:36（日祝9:39）の市バス46系統→今宮神社前10:11（日祝10:14）着。今宮神社とあぶり餅→佛教大学前11:04の市バス6系統で鷹峯源光庵前11:08着→源光庵→常照寺→光悦寺→しょうざんでお昼と庭園→歩いて金閣寺→金閣寺道から市バス59系統で河原町三条→夜は三条・先斗町（12月6日まではしょうざんの夜のライトアップも）。",
        rows=[row("train", "行き：四条河原町 9:36発（日祝 9:39発）の市バス46系統（佛教大学・今宮神社・上賀茂神社行き）→「今宮神社前」10:11着（日祝 10:14着）・230円。日中は12分おき",
                  "Out: city bus 46 (for Bukkyo-daigaku, Imamiya-jinja, Kamigamo-jinja) from Shijo-Kawaramachi at 9:36 (9:39 on Sundays and holidays) → “Imamiya-jinja-mae” 10:11 (10:14), ¥230. Every 12 min in the daytime"),
              row("train", "地下鉄なら：京都市役所前 9:32（土休日 9:31）発の東西線で二条へ（220円）→ 二条駅前 9:46発の市バス6系統 →「佛教大学前」10:04着（230円）、歩いて5〜7分",
                  "By subway: Tozai line from Kyoto Shiyakusho-mae at 9:32 (9:31 on weekends and holidays) to Nijo (¥220) → city bus 6 from Nijo-eki-mae at 9:46 → “Bukkyo-daigaku-mae” 10:04 (¥230), then 5–7 min on foot"),
              row("train", "今宮神社 → 鷹峯：佛教大学前 11:04発の市バス6系統 →「鷹峯源光庵前」11:08着（北1系統なら11:09発→11:13着）・230円。毎日同じ時刻",
                  "Imamiya → Takagamine: city bus 6 from Bukkyo-daigaku-mae at 11:04 → “Takagamine-Genkoan-mae” 11:08 (or Kita-1 at 11:09 → 11:13), ¥230. The same every day")],
        order=[
            ("imamiya", ARR, "10:11（四条河原町 9:36発）。今宮神社とあぶり餅 10:15〜10:55", "10:11 (the 9:36 from Shijo-Kawaramachi). Shrine and aburi-mochi 10:15–10:55",
             T("このコースは、四条河原町から市バス46系統1本で今宮神社前へ（約35分）。三条からは、四条河原町のバス停まで歩いて10分ほどです。\n\n"
               "あぶり餅は10時から。お参りのあとに、2軒のどちらかで1人前を。午前のおやつにちょうどいい量で、お昼までもちます。\n\n"
               "食べたら、今宮通を西へ歩いて「佛教大学前」のバス停へ（5〜7分）。11:04発の市バス6系統で鷹峯へ上ります。",
               "On this course one city bus, no. 46, takes you from Shijo-Kawaramachi to Imamiya-jinja-mae (about 35 minutes). From Sanjo it’s about 10 minutes’ walk to the Shijo-Kawaramachi stop.\n\n"
               "The aburi-mochi shops open at 10:00. After visiting the shrine, share a portion at either one: a good mid-morning snack that will see you through to lunch.\n\n"
               "Then walk west along Imamiya-dori to the “Bukkyo-daigaku-mae” stop (5–7 minutes) for the 11:04 city bus 6 up to Takagamine.")),
            ("genkoan", VIS, "11:10〜11:50", "11:10–11:50",
             T("「鷹峯源光庵前」で降りたら、目の前です。窓の前に、人の少ない朝のうちに座りたい人は、上のボタンで「鷹峯の開門に合わせる」コースに切り替えてください。\n\n出たら、東へ歩いて2分の常照寺へ。",
               "Get off at “Takagamine-Genkoan-mae” and it’s right there. To sit at the windows early, before most people arrive, switch to the “Takagamine at opening” course with the buttons above.\n\nThen walk 2 minutes east to Joshoji.")),
            ("joshoji", VIS, "11:55〜12:25", "11:55–12:25",
             T("朱の吉野門をくぐって、庭と茶室へ。見終わったら、源光庵の前を通って西へ、光悦寺まで歩いて5分ほど。",
               "Through the red Yoshino gate to the garden and teahouse. Then walk west past Genkoan to Koetsuji, about 5 minutes.")),
            ("koetsuji", VIS, "12:30〜13:10", "12:30–13:10",
             T("もみじのトンネルの参道を抜けて、光悦垣の前から鷹ヶ峰の山並みを眺めてください。\n\n"
               "出たら、鷹峯の街道を南へ下って、しょうざんでお昼に（歩いて15分ほど）。",
               "Walk through the tunnel of maples and look out over Takagamine’s hills from beside the Koetsu fence.\n\n"
               "Then head south down the old road to Shozan for lunch (about 15 minutes’ walk).")),
        ],
        sections=[dict(first="imamiya", last="imamiya", day=0), dict(first="genkoan", last="koetsuji", day=1)],
        focus=("imamiya", "koetsuji"),
        notices_last=[LIGHTUP],
        after=AFTER_LATE, links_last=LINKS_LATE, gmaps_last=GMAPS_LATE, back=BACK_LATE,
        hints=[("genkoan", dict(any=["genkoan"], none=["imamiya"]), None, None,
                "今宮神社に寄らない日は、二条駅前 9:46発の市バス6系統で「鷹峯源光庵前」へ直接（10:08着・230円。京都市役所前から地下鉄東西線で二条へ）。",
                "Skipping Imamiya? Take city bus 6 from Nijo-eki-mae at 9:46 straight to “Takagamine-Genkoan-mae” (10:08, ¥230; the Tozai subway takes you from Kyoto Shiyakusho-mae to Nijo)."),
               ("imamiya", dict(any=["imamiya"], none=["genkoan", "joshoji", "koetsuji"]), None, None,
                "今宮神社だけの日は、南へ歩いて10分ほどの大徳寺へ。帰りは大徳寺前から市バス12系統で三条京阪へ、今宮神社前からなら46系統で四条河原町へ（日中は12分おき）。",
                "Only Imamiya? Walk about 10 minutes south to Daitoku-ji. Back to town by city bus 12 from Daitokuji-mae to Sanjo-Keihan, or bus 46 from Imamiya-jinja-mae to Shijo-Kawaramachi (every 12 minutes in the daytime).")]),
    dict(
        id="early", file="takagamine-early.json",
        note="「鷹峯の開門に合わせる」コース。京都市役所前7:55（土休日8:01）の地下鉄で二条→二条駅前8:10（土休日8:13）の市バス6系統→鷹峯源光庵前8:32（8:33）着。常照寺8:30→源光庵9:00の開門→光悦寺→鷹峯源光庵前10:38の市バス6系統で佛教大学前→今宮神社であぶり餅→大徳寺（黄梅院・大仙院）→泉仙でお昼→市バス12系統で金閣寺か北野へ→夜は街なか（12月6日まではしょうざんの夜のライトアップも）。",
        rows=[row("train", "行き：京都市役所前 7:55発（土休日 8:01発）の地下鉄東西線で二条へ（6分・220円）→ 二条駅前 8:10発（土休日 8:13発）の市バス6系統（佛教大学・玄琢行き）→「鷹峯源光庵前」8:32着（土休日 8:33着）・230円",
                  "Out: Tozai subway from Kyoto Shiyakusho-mae at 7:55 (8:01 on weekends and holidays) to Nijo (6 min, ¥220) → city bus 6 (for Bukkyo-daigaku, Gentaku) from Nijo-eki-mae at 8:10 (8:13) → “Takagamine-Genkoan-mae” 8:32 (8:33), ¥230"),
              row("train", "地下鉄烏丸線で北大路へ出るなら：北大路バスターミナル 8:09発（土休日 8:15発）の北1系統 → 鷹峯源光庵前 8:27着（8:31着）。地下鉄260円＋バス230円",
                  "Via the Karasuma line to Kitaoji: Kita-1 from Kitaoji bus terminal at 8:09 (8:15 on weekends and holidays) → Takagamine-Genkoan-mae 8:27 (8:31). Subway ¥260 + bus ¥230"),
              row("train", "鷹峯 → 今宮神社：鷹峯源光庵前 10:38発の市バス6系統 →「佛教大学前」10:46着・230円、歩いて5〜7分。毎日同じ時刻",
                  "Takagamine → Imamiya: city bus 6 from Takagamine-Genkoan-mae at 10:38 → “Bukkyo-daigaku-mae” 10:46, ¥230, then 5–7 min on foot. The same every day")],
        order=[
            ("joshoji", ARR, "8:32（二条駅前 8:10発）。常照寺 8:35〜8:55", "8:32 (the 8:10 from Nijo-eki-mae). Joshoji 8:35–8:55",
             T("源光庵が開く9時の前に、8:30から開いている常照寺へ。バス停から歩いて2分です（お寺の案内）。\n\n"
               "朝ごはんは、出る前に食べておくか、軽く持っていってください。鷹峯で朝早く開いている食事の店は確かめられていません。10時すぎに、今宮神社のあぶり餅でひと休みします。\n\n"
               "8:55ごろ出て、源光庵の門の前へ。",
               "Before Genkoan opens at 9:00, start at Joshoji, which opens at 8:30, 2 minutes from the bus stop (temple’s access page).\n\n"
               "Eat breakfast before you leave, or bring something light: no place to eat in Takagamine could be confirmed as open this early. After 10:00 you’ll rest over aburi-mochi at Imamiya Shrine.\n\n"
               "Leave at about 8:55 for Genkoan’s gate.")),
            ("genkoan", VIS, "9:00〜9:40", "9:00–9:40",
             T("開門の9時に入ります。人が増える前に、迷いの窓と悟りの窓の前に座ってください。\n\n出たら、西へ歩いて4分ほどの光悦寺へ。",
               "Go in at the 9:00 opening and sit in front of the two windows before it fills up.\n\nThen walk about 4 minutes west to Koetsuji.")),
            ("koetsuji", VIS, "9:45〜10:25", "9:45–10:25",
             T("朝のもみじのトンネルを、ゆっくり歩いてください。\n\n"
               "出たら「鷹峯源光庵前」のバス停へ戻って、10:38発の市バス6系統で「佛教大学前」へ（10:46着）。歩いて下りるなら、今宮神社まで25〜30分です（地図で見た目安）。\n\n"
               "近くのしょうざんの庭園（9:00〜17:00）に寄ってから下りることもできます。光悦寺から歩いて15分ほどです。",
               "Walk slowly through the maple tunnel in the morning light.\n\n"
               "Then go back to the “Takagamine-Genkoan-mae” stop for the 10:38 city bus 6 to “Bukkyo-daigaku-mae” (10:46). On foot it’s 25–30 minutes downhill to Imamiya Shrine (map estimate).\n\n"
               "You could also stop at Shozan’s garden nearby (9:00–17:00) on the way down: about 15 minutes’ walk from Koetsuji.")),
            ("imamiya", VIS, "10:55〜11:35", "10:55–11:35",
             T("佛教大学前から今宮通を東へ5〜7分。お参りして、東門の前の茶店であぶり餅を。遅めの朝ごはんのかわりに、座ってひと休みしてください。",
               "From Bukkyo-daigaku-mae it’s 5–7 minutes east along Imamiya-dori. Visit the shrine, then sit down for aburi-mochi at a teahouse by the east gate: a late breakfast and a rest.")),
        ],
        sections=[dict(first="joshoji", last="koetsuji", day=0), dict(first="imamiya", last="imamiya", day=2)],
        focus=("joshoji", "imamiya"),
        notices_last=[OUBAI_N, LIGHTUP],
        after=AFTER_EARLY, links_last=LINKS_EARLY, gmaps_last=GMAPS_EARLY, back=BACK_EARLY,
        hints=[("imamiya", dict(any=["imamiya"], none=["joshoji", "genkoan", "koetsuji"]), None, None,
                "今宮神社だけの日は、四条河原町から市バス46系統で「今宮神社前」へ（約35分・230円）。あぶり餅は10時から。",
                "Only Imamiya? City bus 46 from Shijo-Kawaramachi to “Imamiya-jinja-mae” (about 35 minutes, ¥230). The aburi-mochi shops open at 10:00."),
               ("koetsuji", dict(any=["koetsuji"], none=["imamiya"]), None, None,
                "今宮神社に寄らない日は、光悦寺から歩いて15分ほどのしょうざんへ。庭園は9:00から、お昼はわかどり（11:30〜）か楼蘭（平日12:00〜、土日祝11:30〜）。",
                "Skipping Imamiya? Walk about 15 minutes from Koetsuji to Shozan: the garden opens at 9:00; lunch at Wakadori (from 11:30) or Louran (from 12:00 on weekdays, 11:30 at weekends).")]),
]

SOURCES = [
    {"what": "市バス6系統（2026年3月20日改正）：二条駅前→佛教大学・玄琢行き 平日8:10・土休日8:13、毎日9:46。佛教大学前（玄琢行き）毎日10:04・11:04。鷹峯源光庵前（四条大宮・京都駅行き）毎日10:08・10:38。土天井町（四条大宮・京都駅行き）最終 平日20:37・土休日20:27", "url": BUS_URL, "checked": CHECKED},
    {"what": "市バス北1系統（2026年3月20日改正）：北大路バスターミナル→佛教大学・玄琢行き 平日8:09・土休日8:15、日中は15・35・55分。佛教大学前（玄琢行き）毎日11:09。土天井町（北大路バスターミナル行き）平日20:01・20:31・21:01・21:30・22:00・22:37、土休日20:01・20:41・21:20・22:00・22:37", "url": BUS_URL, "checked": CHECKED},
    {"what": "市バス46系統（2026年3月20日改正）：四条河原町→佛教大学・今宮神社・上賀茂神社行き 平日・土曜9:36、休日9:39、日中は12分おき。今宮神社前（上賀茂神社行き）平日・土曜10:11、休日10:14", "url": BUS_URL, "checked": CHECKED},
    {"what": "市バス12系統（2026年3月20日改正）：大徳寺前→金閣寺道 6分（土曜13:05→13:11、平日13:32→13:38）、日中は12〜15分おき", "url": BUS_URL, "checked": CHECKED},
    {"what": "市バス59系統（2026年3月20日改正）：金閣寺道→四条河原町・三条京阪行き 日中15〜20分おき、最終20:39（平日・土休日）", "url": BUS_URL, "checked": CHECKED},
    {"what": "乗換案内（Yahoo!路線情報、11月22日に検索）：平日 京都市役所前7:55→二条8:01、二条駅前8:10→鷹峯源光庵前8:32（450円）。土曜・日曜 京都市役所前8:01→二条8:07、二条駅前8:13→鷹峯源光庵前8:33。平日 北大路バスターミナル8:09（北1）→鷹峯源光庵前8:27。平日 四条河原町9:36（46系統）→今宮神社前10:11（230円）。平日 京都市役所前9:32、土曜9:31→二条駅前9:46→佛教大学前10:04。鷹峯源光庵前10:38（6系統）→佛教大学前10:46（平日・土曜）。金閣寺道16:35（59系統）→河原町三条17:05（平日）。土天井町21:30（北1）→北大路新町21:44・北大路バスターミナル21:47、北大路21:59の烏丸線→烏丸御池22:06、22:13の東西線→京都市役所前22:14（平日）", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "今宮神社：所在地・TEL受付9:00〜17:00、市バス46番「今宮神社前」下車すぐ、船岡山から北へ徒歩7分、大徳寺バス停から北西へ徒歩13分（交通案内）", "url": "http://www.imamiyajinja.org/access/", "checked": CHECKED},
    {"what": "あぶり餅 一和：定休日 水曜（1日・15日・祝日が水曜の場合は翌日）、年末12/16〜12/31、1人前600円。営業時間の記載なし（京都府観光連盟）", "url": KANKO_ICHIWA, "checked": CHECKED},
    {"what": "あぶり餅（2軒の案内）：一和 営業時間10時～17時、かざりや 営業時間10時～17時、どちらも定休日 水曜日（1日、15日、祝日が水曜日の場合は翌日）・年末、1人前600円（京都府観光連盟）", "url": KANKO_ABURI, "checked": "2026-11-23"},
    {"what": "あぶり餅 かざりや：10時〜17時、定休日 水曜（1日・15日・祝日が水曜の場合は翌日）、年末12/16〜12/31、1人前600円（京都府観光連盟）", "url": KANKO_KAZARI, "checked": CHECKED},
    {"what": "光悦寺：8:00〜17:00（紅葉時8:30〜17:00）、通常400円（紅葉時500円）、定休日11/10〜11/13、市バス「源光庵前」徒歩約3分、ホームページの記載なし（京都観光Navi）", "url": NAVI_KOETSU, "checked": CHECKED},
    {"what": "源光庵：9:00〜17:00（16:30受付終了）、行事の日は拝観中止あり、靴袋持参のお願い、駐車場休止11/14〜12/6（お知らせ2026-11-09）。拝観料の記載なし（公式サイト）", "url": "https://genkouan.or.jp/", "checked": CHECKED},
    {"what": "源光庵の拝観料：大人400円（中学生以上）、紅葉時期は500円、子供200円（小学生）。9時～17時（16時30分受付終了）、定休日 無（土日祝など法要のある場合は一時拝観停止有り）（京都府観光連盟）。京都観光Navi（京都市）の源光庵のページには料金の記載なし", "url": KANKO_GENKOAN, "checked": "2026-11-23"},
    {"what": "常照寺：庭園と堂内の拝観 8:30〜17:00、拝観志納金 大人400円・小学生200円（トップ）。市バス6系統・北1系統「鷹峯源光庵前」徒歩2分（アクセス）", "url": "http://tsakae.justhpbs.jp/joshoji/toppage.html", "checked": CHECKED},
    {"what": "しょうざんリゾート京都：北庭 日本庭園 9:00〜17:00（閉門）無休、一般500円（お食事割引300円）（日本庭園のページの画像）。秋の紅葉ライトアップ 2026年10月31日〜12月6日 17:30〜20:00（最終受付19:30）、入園料800円（ライトアップのページの画像）。市バス北1・6系統「土天井町」徒歩約5分（交通アクセス）", "url": SHOZAN_GARDEN, "checked": CHECKED},
    {"what": "しょうざん わかどり：ランチ11:30〜14:30（LO14:00）、17:00〜22:00（LO21:30）、休業日はカレンダー。楼蘭：年中無休、ランチ 平日12:00〜14:30（LO14:00）・土日祝11:30〜14:30（LO14:30）、17:00〜21:00（LO20:30）", "url": SHOZAN_LOURAN, "checked": CHECKED},
    {"what": "大徳寺 黄梅院 秋の特別公開：2026年10月9日〜12月6日、10:00〜15:45受付終了、大人1,000円・中高生500円・現金のみ、休止日10/10・11・28、静止画撮影可（人物・自撮り棒・三脚は不可）（京都春秋。京都観光Naviのイベント情報も同じ）", "url": OUBAI, "checked": CHECKED},
    {"what": "大仙院：通年9時〜16時30分（臨時変更あり、カレンダーで確認）、大人500円・小人300円・お抹茶500円、年中無休（公式サイト）", "url": DAISEN, "checked": CHECKED},
    {"what": "泉仙 大慈院店：11:00〜16:00（L.O）、年中無休（12/28〜31は休み）、6名以上は予約、あやめ4,500円・ゆり5,500円・ぼたん6,500円（公式サイト）", "url": IZUSEN, "checked": CHECKED},
    {"what": "金閣寺：参拝時間 9:00〜17:00 年中無休、大人（高校生以上）500円・小中学生300円、現金・おまいりPay（相国寺の公式サイト）", "url": KINKAKU, "checked": CHECKED},
    {"what": "紅葉の見ごろ（例年）：源光庵・しょうざんリゾート京都・大徳寺黄梅院 11月中旬〜下旬。大徳寺高桐院は当面拝観休止（京都観光Navi 紅葉だより、11月20日更新）", "url": MOMIJI, "checked": CHECKED},
    {"what": "地下鉄・バス1日券 大人1,100円（地下鉄・市バスなどが1日乗り放題）（京都観光Navi 交通のお得なチケット）", "url": "https://ja.kyoto.travel/feature/traffic/ticket.php", "checked": CHECKED},
    {"what": "船岡温泉：営業時間 15:00~23:30（日は8:00~23:30)、定休日 火曜日、北区紫野南舟岡町82-1、TEL 075-441-3735（京都府浴場組合「京都銭湯」の日本語のページ）。同じサイトの英語のページは「3 p.m. - 1 a.m.」「Opens every day」で食い違う。自前のサイト（funaokaonsen.net）はドメイン切れ", "url": SENTO_FUNAOKA, "checked": "2026-11-23"},
    {"what": "京都の銭湯の入浴料金：1回 中学生以上550円・小学生200円・乳幼児100円（京都府浴場組合「銭湯の利用方法」）。京都府の統制額は2025年4月1日から大人550円（京都府の報道発表 2025-03-21）。2026年10月22日に府の審議会で改定の必要性を検討（2026-10-19の報道発表）、結果は未発表", "url": SENTO_HOWTO, "checked": "2026-11-23"},
    {"what": "京都府公衆浴場入浴料金統制額の改定（2025年4月1日から 大人550円・中人200円・小人100円）", "url": PREF_SENTO_FEE, "checked": "2026-11-23"},
    {"what": "歩く時間（OpenStreetMap の道で測った目安）：鷹峯源光庵前〜光悦寺 約4分、光悦寺〜源光庵 約4分、源光庵〜常照寺 約2分、今宮神社〜佛教大学前 5〜7分、今宮神社〜大仙院 約9分、常照寺〜今宮神社 約25分、しょうざん〜金閣寺 約22分（文章では少しゆったりめに書いた）", "url": "https://www.openstreetmap.org/", "checked": CHECKED},
]

NOTE_HEAD = "京都 今宮神社と鷹峯のルート（takagamine/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（takagamine.json＝9〜10時に出発、takagamine-early.json＝鷹峯の開門に合わせる）。このファイル："
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（鷹峯は2025年11月4日の Nikon D7000、今宮神社は2026年5月15日。人の顔が写る写真は使っていない。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "大徳寺・しょうざん・金閣寺・船岡温泉は写真がないので、最後のスポットの文章で案内している。"
             "info.source は確認した出典、info.checked は確認日、sources は時刻・料金の出典の一覧。このファイルは scripts/build_takagamine_data.py で作る（直接直さない）。")


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    last = order[-1][0]
    spots = []
    for sid, (lj, le), tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        rows = b.pop("_rows")
        if NO[sid] == 1:
            rows = c["rows"] + rows
        if sid == last:
            rows = rows + c["back"]
        tip, source = b.pop("_tip"), b.pop("_source")
        checked = b.pop("_checked", CHECKED)
        if sid == last or NO[sid] == 1:
            tip = T(tip["ja"] + BACK_TIP["ja"], tip["en"] + " " + BACK_TIP["en"])
        b["info"] = info(rows, source, tip=tip, checked=checked)
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        if NO[sid] == 1:
            # 1番のスポットには、紅葉の時期・冬のお知らせを必ず出す（期間つき）
            out["notices"] = [n for n in (SEASON, WINTER) if n not in out.get("notices", [])] + out.get("notices", [])
        ja = body["ja"] + "\n\n" + go["ja"] + f"\n\n{lj}：{tj}"
        en = body["en"] + "\n\n" + go["en"] + f"\n\n{le}: {te}"
        if sid == last:
            ja += "\n\n" + c["after"]["ja"]
            en += "\n\n" + c["after"]["en"]
            out["links"] = out.get("links", []) + [l for l in c["links_last"] if l not in out.get("links", [])]
            out["gmaps"] = out["gmaps"] + c["gmaps_last"]
            out["notices"] = out.get("notices", []) + c["notices_last"]
        out["text"] = T(ja, en)
        out["photos"] = PHOTOS[sid]
        for p in out["photos"]:
            f = p if isinstance(p, str) else p["file"]
            assert os.path.exists(f"{IMG}/{f}"), f
        out.setdefault("notices", [])
        spots.append(out)
    secs = [{"first": NO[s["first"]], "last": NO[s["last"]], "day": s["day"]} for s in c["sections"]]
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": secs,
        "focus": {"first": NO[c["focus"][0]], "last": NO[c["focus"][1]]},
        "plan": {"_note": "「選んで回る」の設定。全部選べる。外したときの回り方は hints。",
                 "picks": [NO[x[0]] for x in order], "auto": {},
                 "hints": [{"spot": NO[sid], "rule": rule(r), "from": frm, "to": to, "text": T(ja, en)} for sid, r, frm, to, ja, en in c["hints"]]},
        "photoBase": f"../images/{MAP_ID}/",
        "sources": SOURCES,
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


for c in COURSES:
    build(c)
