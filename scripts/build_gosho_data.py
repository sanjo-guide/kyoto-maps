#!/usr/bin/env python3
"""京都の中心：二条城と京都御所のデータ（data/routes/gosho.json）を書き出す。

使い方: python3 scripts/build_gosho_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 自分の写真は images/gosho/<スポットのid>-<番号>.jpg を番号の順に全部使う
- ネットから借りた写真（Wikimedia Commons）は images/gosho/<id>-w<番号>.jpg。スポットの _first（自分の写真の前に並べる）か
  _extra（後ろに並べる）に {"file", "credit": {"author", "license", "page"}} で書く。ページでは写真の上に撮影者とライセンスが出る
- 神泉苑・晴明神社・仙洞御所・マンガミュージアムはオーナーが写真を撮っていない場所なので、文章にも行った日などは書かない
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/gosho"
OUT = f"{R}/data/routes/gosho.json"
CHECKED = "2026-11-21"
PICKS = {}
for f in os.listdir(IMG):
    m = re.match(r"(.+)-(\d+)\.jpg$", f)
    if m:
        PICKS.setdefault(m.group(1), []).append(int(m.group(2)))


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def info(rows, tip=None, verified=True):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def photos(pid, first=None, extra=None):
    """クレジットつきの写真（first）→ 自分の写真（番号の順）→ クレジットつきの写真（extra）の順に並べる。"""
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, []))]
    out = (first or []) + own + (extra or [])
    for p in out:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    return out


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


NIJO = "https://nijo-jocastle.city.kyoto.lg.jp/"
KUNAI = "https://kyoto-gosho.kunaicho.go.jp/"
GYOEN = "https://fng.or.jp/kyoto/"
SUBWAY = link("timetable", "乗換案内（Yahoo!）", "Train times (Yahoo! Transit, Japanese)", "https://transit.yahoo.co.jp/")
WEBPHOTO_JA = "写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。"
WEBPHOTO_EN = "Photos are from Wikimedia Commons (author and license shown on each photo)."

GOSHO_CLOSED = {"from": None, "to": None, "url": KUNAI + "visit",
                "head": T("京都御所は月曜休み。冬は15:20までに入場", "The Palace is closed on Mondays; in winter, enter by 15:20"),
                "text": T("京都御所の公開は、月曜（祝日のときは翌日）と12月28日〜1月4日が休みです。行事で休む日もあるので、行く前に宮内庁の参観カレンダーを見てください。入場は10〜2月が15:20まで、3月と9月が15:50まで、4〜8月が16:20までです。",
                          "The Palace is closed on Mondays (the next day if Monday is a holiday) and from 28 December to 4 January, and sometimes for court events, so check the Imperial Household Agency’s calendar first. Last entry is 15:20 from October to February, 15:50 in March and September, and 16:20 from April to August.")}

S = [
    dict(id="nijojo", name=T("二条城", "Nijo Castle"), kind=T("城（世界遺産）", "Castle (World Heritage)"),
         blurb=T("徳川家康が建て、慶喜が大政奉還を告げた城。国宝の二の丸御殿は、金のふすま絵と、歩くと鳴るうぐいす張りの廊下。",
                 "Built by Tokugawa Ieyasu; here the last shogun announced the return of power to the emperor. The National Treasure Ninomaru Palace has gold-leaf screens and “nightingale” floors that chirp as you walk."),
         lat=35.01353, lng=135.74972,
         text=T("二条城（にじょうじょう）\n\n京都駅から地下鉄烏丸線で烏丸御池へ、東西線に乗り換えて「二条城前」まで14分・260円（8:17発→8:31着）。1番出口から東大手門まで歩いて約6分です。\n\n"
                "1603年に徳川家康が建てた城で、1867年に15代将軍の慶喜が大政奉還を告げた場所でもあります。東大手門から入り、金の飾りの唐門（からもん）をくぐると、国宝の二の丸御殿。部屋が奥へ奥へと続き、狩野派の虎や松のふすま絵が並びます。廊下は歩くとキュッキュッと鳴る「うぐいす張り」。御殿の中は撮影できません。\n\n"
                "開城の8:45に入るのがおすすめです。団体が増える前に、二の丸御殿を静かに見られます。御殿のあとは二の丸庭園、内堀を渡って本丸へ。天守閣跡の石垣に上ると、本丸御殿の屋根と京都の町が見渡せます。\n\n"
                "入城券と二の丸御殿のセットで1,300円。本丸御殿（2024年に修理が終わって公開）は別に1,000円で、日時を決めたWEBチケットの予約が要ります（来城日の30日前から）。\n\n"
                "夜の写真は2016年8月と2017年4月の夜のライトアップのときのもの。夜の公開は年によって内容も期間も変わるので、公式サイトで確認してください。\n\nおすすめ訪問時間：8:45〜10:30",
                "Nijo Castle\n\nFrom Kyoto Station take the Karasuma subway line to Karasuma-Oike and change to the Tozai line for “Nijojo-mae”: 14 minutes, ¥260 (8:17 → 8:31). From exit 1 it’s about 6 minutes on foot to the East Gate.\n\n"
                "Tokugawa Ieyasu built the castle in 1603, and in 1867 the 15th shogun, Yoshinobu, announced here that he was returning power to the emperor. Enter by the East Gate, pass under the gold-fitted Karamon gate, and you reach the Ninomaru Palace, a National Treasure. Room leads on to room, lined with Kano-school tigers and pines on gold leaf. The corridor floors chirp underfoot (“nightingale floors”). No photography inside the palace.\n\n"
                "Go in at opening time, 8:45: you see the palace quietly before the tour groups arrive. After the palace, walk the Ninomaru garden, then cross the inner moat to the Honmaru. Climb the stone base of the old keep for a view over the Honmaru Palace roofs and the city.\n\n"
                "Castle entry with the Ninomaru Palace is ¥1,300. The Honmaru Palace (reopened in 2024 after repairs) costs another ¥1,000 and needs a timed web ticket booked in advance (on sale from 30 days before).\n\n"
                "The night photos are from evening illuminations in August 2016 and April 2017. Evening openings change from year to year, so check the official website.\n\nRecommended visit time: 8:45–10:30"),
         gmaps=[gm("二条城 東大手門（入口）", "Nijo Castle East Gate (entrance)", 35.01425, 135.75205, "二条城 東大手門")],
         links=[link("official", "二条城 公式サイト", "Nijo Castle (official)", NIJO, NIJO + "?lang=en"),
                link("info", "本丸御殿の予約（公式）", "Honmaru Palace tickets (official)", NIJO + "admission/"), SUBWAY],
         notices=[{"from": None, "to": "2026-12-06", "url": NIJO,
                   "head": T("12月6日（日）は入城受付の時間が変わります", "Entry hours change on Sunday 6 December"),
                   "text": T("二条城の公式サイトに、2026年12月6日（日）は入城受付の時間を変えるというお知らせが出ています。この日に行く人は、公式サイトで時間を確かめてください。",
                             "The castle website announces different entry hours on Sunday 6 December 2026. If you go that day, check the times on the website.")}],
         info=info([row("hours", "8:45〜16:00（閉城17:00）。二の丸御殿の受付は16:10まで", "8:45–16:00 (gates close 17:00); Ninomaru Palace entry until 16:10"),
                    row("closed", "休城は12月29〜31日。二の丸御殿は1月・7月・8月・12月の火曜（祝日なら翌日）と12月26〜28日、1月1〜3日は入れません",
                        "Castle closed 29–31 December. The Ninomaru Palace is also closed on Tuesdays in January, July, August and December (next day if a holiday), 26–28 December and 1–3 January"),
                    row("fee", "入城＋二の丸御殿 一般1,300円（入城だけなら800円）、中高生400円、小学生300円。本丸御殿は別に1,000円（要予約）",
                        "Castle + Ninomaru Palace ¥1,300 (castle only ¥800); ages 12–18 ¥400, 6–12 ¥300. Honmaru Palace ¥1,000 extra (booking required)"),
                    row("train", "京都8:17発（地下鉄烏丸線）→ 烏丸御池で東西線に乗り換え → 二条城前8:31着・260円", "Kyoto 8:17 (Karasuma subway line) → change at Karasuma-Oike to the Tozai line → Nijojo-mae 8:31, ¥260")],
                   tip=T("二条城の公式サイトと乗換案内（2026年11月26日の時刻）で確認しました。地下鉄一日券か地下鉄・バス一日券を当日の券売所で見せると、入城料800円が700円になります（公式サイト）。唐門・二の丸御殿・二の丸庭園・本丸の昼の写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the castle website and Yahoo! Transit (times for 26 November 2026). Show a subway or subway & bus one-day pass at the ticket office and the ¥800 entry fee becomes ¥700 (castle website). The daytime photos of the Karamon gate, Ninomaru Palace, garden and Honmaru are from Wikimedia Commons (author and license shown on each photo).")),
         _first="nijojo"),
    dict(id="shinsenen", name=T("神泉苑", "Shinsen-en"), kind=T("寺・池", "Temple & pond"),
         blurb=T("二条城のすぐ南。平安京ができたときの天皇の庭の名残で、池に朱色の法成橋がかかります。",
                 "Just south of the castle: what remains of the emperor’s garden from the founding of Kyoto, with the vermilion Hojo bridge over its pond."),
         lat=35.01155, lng=135.74807,
         text=T("神泉苑（しんせんえん）\n\n二条城の東大手門から南へ歩いて約9分、地下鉄の二条城前駅からは約4分。794年、平安京と一緒に桓武天皇が造った庭（禁苑）の名残です。もとはずっと広く、二条城を造るときに大きく削られて、今の広さになりました。\n\n"
                "池にかかる朱色の法成橋（ほうじょうばし）と、池の中の善女龍王社（ぜんにょりゅうおうしゃ）が見どころ。824年に空海がここで雨乞いをして、龍王を呼んだと伝わります。疫病をしずめるためにここで行われた御霊会（ごりょうえ）は、祇園祭の始まりとされています。\n\n"
                "境内は無料で、10〜15分で回れます。二条城のあとに寄って、そのまま二条城前駅から地下鉄に乗るとむだがありません。\n\nおすすめ訪問時間：10:35〜10:50",
                "Shinsen-en\n\nAbout 9 minutes’ walk south of the castle’s East Gate, or 4 minutes from Nijojo-mae subway station. This is what is left of the imperial garden Emperor Kanmu laid out in 794 along with the new capital. It was once far larger; much of it was taken when Nijo Castle was built.\n\n"
                "Look for the vermilion Hojo bridge over the pond and the small shrine to the dragon queen Zennyo Ryuo on the island. In 824 the monk Kukai is said to have prayed for rain here and summoned the dragon. A ritual held here to calm an epidemic is counted as the origin of the Gion Festival.\n\n"
                "Entry is free and 10–15 minutes is enough. Stop by after the castle, then take the subway from Nijojo-mae.\n\nRecommended visit time: 10:35–10:50"),
         gmaps=[gm("神泉苑", "Shinsen-en", 35.01155, 135.74807, "神泉苑 京都")],
         links=[link("official", "神泉苑 公式サイト", "Shinsen-en (official, Japanese)", "http://www.shinsenen.org/")],
         info=info([row("hours", "境内の参拝 6:30〜20:00", "Grounds open 6:30–20:00"), row("fee", "無料", "Free"),
                    row("train", "地下鉄東西線 二条城前駅から歩いて約2分（神泉苑の案内）", "About 2 min on foot from Nijojo-mae station, Tozai subway line (temple’s access page)")],
                   tip=T("神泉苑の公式サイトで確認しました。二条城からの歩く時間は OpenStreetMap で測った目安です。" + WEBPHOTO_JA,
                         "Checked on the temple website. The walking time from the castle is an estimate measured on OpenStreetMap. " + WEBPHOTO_EN)),
         _first="shinsenen"),
    dict(id="seimei", name=T("晴明神社", "Seimei Shrine"), kind=T("神社", "Shrine"),
         blurb=T("陰陽師・安倍晴明をまつる神社。鳥居にも提灯にも、五芒星（晴明桔梗）の印。",
                 "The shrine of Abe no Seimei, the Heian-period yin-yang master; his five-pointed star is on the torii and the lanterns."),
         lat=35.02776, lng=135.75114,
         text=T("晴明神社（せいめいじんじゃ）\n\n平安時代の陰陽師、安倍晴明（あべのせいめい）の屋敷があった場所に建つ神社です。二条城前のバス停から堀川通を北へ、市バス9・12系統で「一条戻橋・晴明神社前」へ（230円）。\n\n"
                "一の鳥居の額は、神社の名前ではなく金色の五芒星（ごぼうせい）。「晴明桔梗」と呼ばれる神社の紋です。境内には、晴明が念力で湧かせたと伝わる「晴明井」、なでて厄を落とす「厄除桃」、昔の一条戻橋の欄干と式神の石像があります。小さな境内なので20分ほどで回れます。\n\n"
                "ここから京都御苑へは、東へまっすぐ歩いて約15分（約1.1km）で中立売御門。そのまま進むと京都御所の入口の清所門です。この場合、4番の梅林・桃林は御所のあとに回ってください。\n\nおすすめ訪問時間：11:10〜11:30",
                "Seimei Shrine\n\nThe shrine stands where the house of Abe no Seimei, the Heian-period yin-yang master, once stood. From the Nijojo-mae bus stop take city bus 9 or 12 north along Horikawa-dori to “Ichijo-modoribashi / Seimei-jinja-mae” (¥230).\n\n"
                "The plaque on the first torii carries not the shrine’s name but a golden five-pointed star, the shrine’s crest. Inside are the Seimei well, said to have sprung up by Seimei’s power; a bronze peach you stroke to rub off bad luck; and the railing posts of the old Ichijo Modoribashi bridge with a stone figure of his spirit servant. It’s a small precinct: 20 minutes is enough.\n\n"
                "From here it’s about 15 minutes (1.1 km) straight east on foot to the Nakadachiuri gate of the Imperial Palace Park; keep going and you reach the Seishomon gate, the entrance to the Palace. If you come this way, see the plum and peach groves (No. 4) after the Palace.\n\nRecommended visit time: 11:10–11:30"),
         gmaps=[gm("晴明神社", "Seimei Shrine", 35.02776, 135.75114, "晴明神社 京都")],
         links=[link("official", "晴明神社 公式サイト", "Seimei Shrine (official, Japanese)", "https://www.seimeijinja.jp/"),
                link("timetable", "市バスの時刻表（京都市交通局）", "City bus timetables (Kyoto City, Japanese)", "https://www.city.kyoto.lg.jp/kotsu/")],
         info=info([row("hours", "9:00〜17:00（授与所は16:30まで）", "9:00–17:00 (amulet counter until 16:30)"), row("closed", "無休", "Open every day"), row("fee", "無料", "Free"),
                    row("bus", "市バス9・12系統「一条戻橋・晴明神社前」すぐ・230円。バスの時刻は要確認", "City bus 9 or 12 to “Ichijo-modoribashi / Seimei-jinja-mae”, right outside, ¥230. Bus times: please check")],
                   tip=T("晴明神社の公式サイトで確認しました（バスの系統も公式サイトの案内）。バスの時刻は確認していません。御苑までの距離は OpenStreetMap で測った目安です。" + WEBPHOTO_JA,
                         "Checked on the shrine website (bus numbers are from its access page). Bus times were not checked. The distance to the park is an estimate measured on OpenStreetMap. " + WEBPHOTO_EN)),
         _first="seimei"),
    dict(id="gyoen", name=T("京都御苑：梅林・桃林と蛤御門", "Imperial Palace Park: plum & peach groves, Hamaguri gate"), kind=T("公園", "Park"),
         blurb=T("御所を囲む、24時間入れる無料の公園。西側を南から北へ、しだれ桜・桃林・梅林・蛤御門と歩きます。",
                 "The free park around the Palace, open round the clock. Walk up its west side: weeping cherry, peach grove, plum grove, Hamaguri gate."),
         lat=35.0218, lng=135.7604,
         text=T("京都御苑（きょうとぎょえん）\n\n二条城前から地下鉄で烏丸御池へ、烏丸線に乗り換えて1駅の「丸太町」まで7分・220円（10:58発→11:05着）。1番出口から北へ歩いて約5分で、御苑の南西の角です。\n\n"
                "京都御苑は、京都御所を囲む東西約700m・南北約1.3kmの公園。江戸時代まで約200の公家屋敷が並んでいた場所で、今は玉砂利の広い道と松林です。毎日24時間、無料で入れます。\n\n"
                "西側を南から北へ歩きましょう。出水（でみず）の小川のそばに、御苑でも早く咲くしだれ桜（写真1枚目は2015年3月25日）。その北が約70本の桃林（見ごろは3月中旬〜4月上旬）、続いて約130本の梅林（2月中旬〜3月中旬）。梅の写真は2016年2月22日と2019年3月2日、花の色が混ざった4月の写真は2023年4月10日です。\n\n"
                "梅林のすぐ北が蛤御門（はまぐりごもん）。1864年の「禁門の変」で長州藩と会津・薩摩藩が戦った場所で、門の柱や梁に、そのときのものと伝わる弾の跡が残っています。門を見たら、北東へ約6分で京都御所の入口・清所門です。\n\n"
                "玉砂利は思ったより足が疲れます。自転車が通ってできた細いわだち（砂利のない筋）の上を歩くと楽です。\n\nおすすめ訪問時間：11:10〜11:40",
                "Kyoto Imperial Palace Park (Kyoto Gyoen)\n\nFrom Nijojo-mae take the subway to Karasuma-Oike and change to the Karasuma line for one stop to “Marutamachi”: 7 minutes, ¥220 (10:58 → 11:05). From exit 1 it’s about 5 minutes’ walk north to the south-west corner of the park.\n\n"
                "Kyoto Gyoen is the park around the Imperial Palace, about 700 m east to west and 1.3 km north to south. Until the end of the Edo period some 200 court nobles’ houses stood here; now it is wide gravel avenues and pines. It’s open 24 hours a day and free.\n\n"
                "Walk up the west side from the south. By the Demizu stream is a weeping cherry that flowers early (photo 1: 25 March 2015). North of it is the peach grove, about 70 trees (best mid-March to early April), then the plum grove, about 130 trees (mid-February to mid-March). The plum photos are from 22 February 2016 and 2 March 2019; the April photos with mixed colours are from 10 April 2023.\n\n"
                "Just north of the plums is the Hamaguri gate. In 1864 Choshu troops fought the Aizu and Satsuma domains here (the Kinmon incident), and the gate’s posts and beams still carry what are said to be bullet marks from that day. From the gate it’s about 6 minutes north-east to Seishomon, the entrance to the Palace.\n\n"
                "The gravel is more tiring than it looks. Walk along the narrow tracks worn clear by bicycles.\n\nRecommended visit time: 11:10–11:40"),
         gmaps=[gm("出水の小川（しだれ桜）", "Demizu stream (weeping cherry)", 35.02011, 135.7607, "京都御苑 出水の小川"),
                gm("蛤御門", "Hamaguri gate", 35.02315, 135.7596, "蛤御門 京都御苑")],
         links=[link("official", "京都御苑（国民公園協会）", "Kyoto Gyoen (National Parks Foundation, Japanese)", GYOEN),
                link("info", "京都御苑（環境省）", "Kyoto Gyoen (Ministry of the Environment)", "https://www.env.go.jp/garden/kyotogyoen/"), SUBWAY],
         info=info([row("hours", "24時間入れます", "Open 24 hours"), row("fee", "無料", "Free"),
                    row("train", "二条城前10:58発（東西線）→ 烏丸御池で烏丸線に乗り換え → 丸太町11:05着・220円", "Nijojo-mae 10:58 (Tozai line) → change at Karasuma-Oike to the Karasuma line → Marutamachi 11:05, ¥220"),
                    row("hours", "梅は2月中旬〜3月中旬、桃は3月中旬〜4月上旬（国民公園協会の案内）", "Plums mid-Feb to mid-March, peaches mid-March to early April (park foundation’s guide)")],
                   tip=T("環境省と国民公園協会の京都御苑のサイト、乗換案内（2026年11月26日の時刻）で確認しました。歩く時間は OpenStreetMap で測った目安です。蛤御門の写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the park’s websites (Ministry of the Environment and the National Parks Foundation) and Yahoo! Transit (times for 26 November 2026). Walking times are estimates measured on OpenStreetMap. The photo of the Hamaguri gate is from Wikimedia Commons (author and license shown on the photo).")),
         _extra="gyoen"),
    dict(id="gosho", name=T("京都御所", "Kyoto Imperial Palace"), kind=T("御所", "Palace"),
         blurb=T("明治まで約500年、天皇の住まいだった場所。予約なし・無料で入れて、紫宸殿や御池庭を外から見て回ります。",
                 "The emperors’ home for some 500 years until 1869. Free, no booking: you walk round the Shishinden hall and the pond garden from outside."),
         lat=35.02583, lng=135.76102,
         text=T("京都御所（きょうとごしょ）\n\n1331年から明治のはじめまで、天皇が住んでいた場所です。今の建物は1855年に、平安時代の様式で建て直されたもの。予約はいらず、無料で入れます。入口は西側の清所門（せいしょもん）で、入るときに手荷物検査があります。\n\n"
                "順路は約50分。車寄せのある御車寄（おくるまよせ）、朱色の回廊と承明門（じょうめいもん）、その奥に即位の礼が行われた紫宸殿（ししんでん）。写真2枚目のように、承明門の柱のあいだから紫宸殿を正面に見られます。続いて清涼殿、池に欅橋がかかる御池庭（おいけにわ）、御常御殿と御内庭へ。建物の中には入れず、外から見ます。\n\n"
                "ガイドツアー（無料・予約なし）は日本語が9:30・10:30・13:30・14:30、英語が10:00・14:00。開始時間までに、入ってすぐの参観者休所へ。無料の音声ガイドアプリもあります。\n\n"
                "冬（10〜2月）は入場が15:20までなので、午前のうちに入りましょう。月曜は休みです。中は砂利道で、飲食はできません。\n\n"
                "お昼は、清所門から歩いて3分の中立売（なかだちうり）休憩所で。レストランと無料の休憩スペースがあります。\n\n"
                "写真は2024年1月6日と11月6日。\n\nおすすめ訪問時間：11:45〜12:40（そのあとお昼）",
                "Kyoto Imperial Palace (Kyoto Gosho)\n\nThe emperors lived here from 1331 until the start of the Meiji era. The present buildings were rebuilt in 1855 in the style of the Heian period. No booking, no charge. The entrance is the Seishomon gate on the west side; bags are checked as you go in.\n\n"
                "The route takes about 50 minutes: the Okurumayose carriage porch, the vermilion corridors and Jomeimon gate, and beyond them the Shishinden, the hall of enthronements. As in photo 2, you can look straight at the Shishinden between the pillars of the Jomeimon. Then come the Seiryoden, the Oikeniwa pond garden with its Keyaki bridge, and the Otsunegoten with its inner garden. You see the buildings from outside; you can’t go in.\n\n"
                "Free guided tours (no booking): English at 10:00 and 14:00; Japanese at 9:30, 10:30, 13:30 and 14:30. Be at the visitors’ rest house just inside the gate by the start time. There is also a free audio-guide app.\n\n"
                "In winter (October to February) last entry is 15:20, so go in the morning. Closed on Mondays. The paths are gravel, and you can’t eat or drink inside.\n\n"
                "For lunch, the Nakadachiuri rest house is 3 minutes’ walk from the Seishomon gate, with a restaurant and a free seating area.\n\n"
                "Photos: 6 January and 6 November 2024.\n\nRecommended visit time: 11:45–12:40 (then lunch)"),
         gmaps=[gm("清所門（京都御所の入口）", "Seishomon gate (Palace entrance)", 35.02583, 135.76102, "京都御所 清所門"),
                gm("中立売休憩所（お昼）", "Nakadachiuri rest house (lunch)", 35.0256, 135.7599, "京都御苑 中立売休憩所")],
         links=[link("official", "京都御所（宮内庁）", "Kyoto Imperial Palace (Imperial Household Agency)", KUNAI, KUNAI + "en"),
                link("info", "参観要領・カレンダー", "Visiting guide & calendar", KUNAI + "visit", KUNAI + "en/visit"),
                link("info", "中立売休憩所", "Nakadachiuri rest house (Japanese)", GYOEN + "place/rest/")],
         notices=[GOSHO_CLOSED],
         info=info([row("hours", "入場 9:00〜15:20（10〜2月）／〜15:50（3月・9月）／〜16:20（4〜8月）。退出はその40分後まで", "Entry 9:00–15:20 (Oct–Feb) / until 15:50 (Mar & Sep) / until 16:20 (Apr–Aug); leave within 40 min after that"),
                    row("closed", "月曜（祝日のときは翌日）、12月28日〜1月4日、行事のある日", "Mondays (next day if a holiday), 28 Dec–4 Jan, and days of court events"),
                    row("fee", "無料・予約不要", "Free, no booking"),
                    row("train", "地下鉄烏丸線 今出川駅3番出口から歩いて約5分（丸太町駅からは御苑の中を歩いて約20分）", "About 5 min on foot from exit 3 of Imadegawa station, Karasuma subway line (about 20 min through the park from Marutamachi)"),
                    row("hours", "中立売休憩所のレストランは10〜2月 9:00〜16:30（ラストオーダー15:30）。ほかの月は要確認", "Nakadachiuri restaurant: 9:00–16:30 (last order 15:30) from October to February; other months: please check")],
                   tip=T("宮内庁の京都御所のサイト（参観要領・よくあるご質問）と、国民公園協会の京都御苑のサイトで確認しました。",
                         "Checked on the Imperial Household Agency’s Kyoto Imperial Palace website (visiting guide and FAQ) and the park foundation’s website."))),
    dict(id="kitagyoen", name=T("京都御苑の北側：紅葉・近衞邸跡のしだれ桜", "North side of the park: maples & the Konoe weeping cherries"), kind=T("公園", "Park"),
         blurb=T("御所の北は人が少なくて静か。秋は乾御門のあたりのもみじとイチョウ、春は近衞邸跡のしだれ桜、冬は雪の松林。",
                 "North of the Palace it’s quiet. Maples and ginkgo near the Inui gate in autumn, weeping cherries at the old Konoe residence in spring, snow on the pines in winter."),
         lat=35.02832, lng=135.76191,
         text=T("京都御苑の北側\n\n清所門から御所の塀に沿って北へ歩いて約5分。御苑の北西、乾御門（いぬいごもん）の近くは、秋になるともみじが赤く、大きなイチョウが黄色くなります（写真1〜5枚目は2017年11月23日）。芝生に落ち葉が積もり、お寺の紅葉とちがって人が少なく、無料です。\n\n"
                "その東が近衞邸跡（このえていあと）。五摂家の近衞家の屋敷があった場所で、池のまわりに約60本のしだれ桜（糸桜）があります。御苑でいちばん早く、3月中旬に咲き始め、種類によって時期がずれるので1か月ほど楽しめます。\n\n"
                "御所の北の門が朔平門（さくへいもん、写真10枚目）。ここから御所の東側へ回ると、長い築地塀（ついじべい）と松林が続きます。雪の写真は2017年1月15日と2019年1月27日。京都の町なかで雪が積もるのは年に数回なので、積もった朝はまずここへ。\n\n"
                "ここから地下鉄の今出川駅までは歩いて約5分。足をのばすなら、今出川から地下鉄で3駅の北山に京都府立植物園があります。下鴨神社は叡山電鉄のマップに載せています。\n\nおすすめ訪問時間：13:20〜13:50",
                "North side of the park\n\nAbout 5 minutes’ walk north from the Seishomon gate along the Palace wall. In the north-west of the park, near the Inui gate, the maples turn red and a big ginkgo turns yellow in autumn (photos 1–5: 23 November 2017). Leaves pile up on the grass; unlike the temples, there are few people and no charge.\n\n"
                "East of it is the site of the Konoe residence, home of one of the five regent families, with about 60 weeping cherries around a pond. They are the first in the park to flower, from mid-March, and as the varieties differ the blossom lasts about a month.\n\n"
                "The Palace’s north gate is the Sakuheimon (photo 10). Walk round from here to the east side and the long earthen wall and pine woods go on and on. The snow photos are from 15 January 2017 and 27 January 2019. Snow settles in central Kyoto only a few times a year; on such a morning, come here first.\n\n"
                "Imadegawa subway station is about 5 minutes’ walk from here. To go further: Kyoto Botanical Gardens are at Kitayama, three subway stops north of Imadegawa; Shimogamo Shrine is on the Eizan Railway map.\n\nRecommended visit time: 13:20–13:50"),
         gmaps=[gm("近衞邸跡", "Konoe residence site", 35.02832, 135.76191, "京都御苑 近衛邸跡"),
                gm("乾御門", "Inui gate", 35.02748, 135.75963, "乾御門 京都御苑")],
         links=[link("official", "京都御苑の自然（国民公園協会）", "Nature in Kyoto Gyoen (Japanese)", GYOEN + "place/creature/"),
                link("info", "叡山電鉄のマップ（下鴨神社）", "Eizan Railway map (Shimogamo Shrine)", "../eizan-line/")],
         info=info([row("hours", "24時間入れます", "Open 24 hours"), row("fee", "無料", "Free"),
                    row("hours", "近衞邸跡のしだれ桜は3月中旬から約1か月（国民公園協会の案内）。紅葉の時期は年によって変わります", "Konoe weeping cherries: about a month from mid-March (park foundation’s guide). Autumn colour varies by year"),
                    row("train", "地下鉄烏丸線 今出川駅まで歩いて約5分", "About 5 min on foot to Imadegawa station, Karasuma subway line")],
                   tip=T("国民公園協会の京都御苑のサイトで確認しました。歩く時間は OpenStreetMap で測った目安です。紅葉の見ごろの時期は公式の案内がないので、写真の日付（11月23日）を目安にしてください。",
                         "Checked on the park foundation’s website. Walking times are estimates measured on OpenStreetMap. There is no official guide to the autumn-colour dates; use the date of the photos (23 November) as a rough guide."))),
    dict(id="nashinoki", name=T("梨木神社", "Nashinoki Shrine"), kind=T("神社・名水", "Shrine & spring water"),
         blurb=T("御苑の東の門を出てすぐの、木立の中の小さな神社。京都三名水でただ一つ残る「染井」の水が湧いています。",
                 "A small shrine in the trees just outside the park’s east gate, with Somei, the only one of Kyoto’s three famous wells still flowing."),
         lat=35.02454, lng=135.76733,
         text=T("梨木神社（なしのきじんじゃ）\n\n御所の東側を南へ歩き、清和院御門（せいわいんごもん）を出てすぐ左。明治18年に、明治維新に尽くした三條實萬（さねつむ）・實美（さねとみ）の親子をまつって建てられた神社です。萩の名所で、9月下旬に萩まつりがあります。\n\n"
                "手水舎の水は「染井（そめい）」。京都三名水のうち、今も湧いているただ一つの井戸です。蛇口から自由に汲めて、口にふくむとやわらかい水です（蛇口が開いているのは6:00〜18:30ごろ）。空のペットボトルを持って行くと、持ち帰れます。\n\n"
                "境内の古い茶室は、今はコーヒースタンド「Coffee Base NASHINOKI」。染井の水でいれたコーヒーが飲めます（写真6・7枚目。営業の日と時間は要確認）。\n\n"
                "写真は2026年5月18日、青もみじの時期です。\n\nおすすめ訪問時間：14:00〜14:15",
                "Nashinoki Shrine\n\nWalk south down the east side of the Palace and leave the park by the Seiwain gate; the shrine is immediately on the left. It was founded in 1885 for Sanjo Sanetsumu and his son Sanetomi, court nobles who worked for the Meiji Restoration. It is known for bush clover, with a festival in late September.\n\n"
                "The water at the purification basin is Somei, the only one of Kyoto’s three famous wells that still flows. Anyone may fill a bottle from the taps; the water tastes soft (taps are open from about 6:00 to 18:30). Bring an empty bottle and take some with you.\n\n"
                "The old tea room in the grounds is now a coffee stand, Coffee Base NASHINOKI, brewing with Somei water (photos 6 and 7; opening days and hours: please check).\n\n"
                "Photos: 18 May 2026, with the maples in fresh green.\n\nRecommended visit time: 14:00–14:15"),
         gmaps=[gm("梨木神社", "Nashinoki Shrine", 35.02454, 135.76733, "梨木神社 京都")],
         links=[link("official", "梨木神社 公式サイト", "Nashinoki Shrine (official, Japanese)", "https://www.nashinoki.jp/")],
         info=info([row("hours", "開門7:30、閉門16:30。授与所は9:00〜16:30（12:15〜13:15は休み）", "Gates 7:30–16:30; amulet counter 9:00–16:30 (closed 12:15–13:15)"),
                    row("fee", "無料", "Free"),
                    row("hours", "染井の水の蛇口は6:00〜18:30ごろ", "Somei water taps: about 6:00–18:30"),
                    row("hours", "Coffee Base NASHINOKI の営業時間は公式の情報で確認できていません（要確認）", "Coffee Base NASHINOKI’s hours could not be confirmed from an official source (please check)")],
                   tip=T("梨木神社の公式サイトで確認しました。", "Checked on the shrine website."))),
    dict(id="sento", name=T("京都仙洞御所", "Sento Imperial Palace"), kind=T("庭園（要予約）", "Garden (booking needed)"),
         blurb=T("退位した天皇の御所の庭。二つの池と、丸い石を敷きつめた洲浜を、職員の案内で約1時間歩きます。18歳以上・無料。",
                 "The garden of the retired emperors’ palace: two ponds and a shore of rounded stones, seen on a one-hour guided walk. Ages 18 and over, free."),
         lat=35.02168, lng=135.76563,
         text=T("京都仙洞御所（きょうとせんとうごしょ）\n\n17世紀のはじめ、退位した後水尾上皇のために造られた御所です。建物は1854年の火事で焼けて、庭が残りました。北池と南池のまわりを歩く庭で、南池の岸は、平たく丸い石を一面に敷きつめた洲浜（すはま）になっています。\n\n"
                "自由には入れず、職員の案内で約1時間（約1km）。開始は9:30・11:00・13:30・14:30・15:30で、7・8月は原則9:30・11:00・15:30だけです。参観できるのは18歳以上、無料。全員の本人確認の書類（外国の人はパスポート）が要ります。\n\n"
                "申し込みは2通り。①宮内庁のサイトで、行く月の3か月前の1日から、3日前までに予約。②当日、仙洞御所の前で8:40から先着順に配る整理券（1日50人）。紅葉や桜の時期の当日券は朝のうちになくなるので、行きたい人は予約を。当日券をねらうなら、朝いちばんにここへ来て整理券をもらってから二条城へ行く順番に変えてください。\n\n"
                "説明は日本語です。英語・中国語・フランス語・韓国語・スペイン語の音声ガイドを無料で借りられます。細い石橋や飛び石があるので、歩きやすい靴で。\n\nおすすめ訪問時間：14:30〜15:30（14:30の回。20分前までに）",
                "Sento Imperial Palace (Kyoto Sento Gosho)\n\nBuilt in the early 17th century for the retired emperor Go-Mizunoo. The buildings burned down in 1854; the garden remains. You walk round a north pond and a south pond, and the shore of the south pond is paved all over with flat, rounded stones.\n\n"
                "You can’t walk in freely: visits are guided by staff and take about an hour (about 1 km). Tours start at 9:30, 11:00, 13:30, 14:30 and 15:30; in July and August normally only 9:30, 11:00 and 15:30. Visitors must be 18 or over; it’s free. Everyone needs ID (a passport for visitors from abroad).\n\n"
                "Two ways to get in. (1) Book on the Imperial Household Agency website, from the 1st of the month three months ahead until three days before. (2) Same-day tickets, handed out in front of the Sento Palace from 8:40, first come first served (50 a day). In the cherry and maple seasons these go early in the morning, so book if you really want to go. If you’re trying for a same-day ticket, come here first thing, get your ticket, and then go to Nijo Castle.\n\n"
                "The tour is in Japanese; free audio guides are lent in English, Chinese, French, Korean and Spanish. There are narrow stone bridges and stepping stones, so wear good shoes.\n\nRecommended visit time: 14:30–15:30 (the 14:30 tour; be there 20 minutes before)"),
         gmaps=[gm("京都仙洞御所", "Sento Imperial Palace", 35.02168, 135.76563, "京都仙洞御所")],
         links=[link("official", "京都仙洞御所（宮内庁）", "Sento Imperial Palace (Imperial Household Agency)", KUNAI + "sento-gosho", KUNAI + "en/sento-gosho"),
                link("info", "参観の申し込み（宮内庁）", "Apply for a visit (Imperial Household Agency)", "https://sankan.kunaicho.go.jp/")],
         info=info([row("hours", "案内の開始 9:30・11:00・13:30・14:30・15:30（7・8月は原則9:30・11:00・15:30）。約60分", "Tours at 9:30, 11:00, 13:30, 14:30, 15:30 (Jul–Aug normally 9:30, 11:00, 15:30); about 60 min"),
                    row("closed", "月曜（祝日のときは翌日）、12月28日〜1月4日、行事のある日", "Mondays (next day if a holiday), 28 Dec–4 Jan, and days of court events"),
                    row("fee", "無料。18歳以上、要申し込み（1件4人まで）。当日券は8:40から先着順・1日50人", "Free. Ages 18+, application needed (up to 4 people each). Same-day tickets from 8:40, first come first served, 50 a day"),
                    row("train", "地下鉄烏丸線 丸太町駅1番出口から歩いて約15分（宮内庁の案内）", "About 15 min on foot from exit 1 of Marutamachi station, Karasuma subway line (official access)")],
                   tip=T("宮内庁の「京都仙洞御所 参観申込要領」で確認しました。" + WEBPHOTO_JA, "Checked in the Imperial Household Agency’s application guide for the Sento Imperial Palace. " + WEBPHOTO_EN)),
         _first="sento"),
    dict(id="manga", name=T("京都国際マンガミュージアム", "Kyoto International Manga Museum"), kind=T("ミュージアム", "Museum"),
         blurb=T("昔の小学校の校舎が、マンガの博物館に。壁いっぱいの本棚のマンガを、館内や芝生で好きなだけ読めます。",
                 "An old primary school turned manga museum: take any book from the walls of shelves and read it inside or out on the lawn."),
         lat=35.0117, lng=135.75918,
         text=T("京都国際マンガミュージアム\n\n地下鉄の丸太町から1駅の烏丸御池で降りて、2番出口から歩いて2分（御苑の南の端からなら、烏丸通を南へ歩いて約10分）。昭和のはじめに建った小学校の校舎を使った、マンガの博物館です。\n\n"
                "廊下の壁が上から下まで本棚になっていて、並んでいるマンガはどれでも手に取って読めます。天気のいい日は、校庭だった芝生に寝ころんで読む人も。外国語に訳されたマンガの棚もあるので、日本語が読めなくても楽しめます。\n\n"
                "雨の日や、夏と冬に歩き疲れたときの休み場所としても便利です。水曜は休み。最終入館は16:30なので、仙洞御所の14:30の回に入った日は、ここを飛ばして錦市場へ行くほうがゆっくりできます。\n\nおすすめ訪問時間：15:45〜16:30（仙洞御所に入らない日は14:45〜15:45）",
                "Kyoto International Manga Museum\n\nOne subway stop from Marutamachi: get off at Karasuma-Oike and walk 2 minutes from exit 2 (or walk about 10 minutes south down Karasuma-dori from the southern edge of the park). The museum occupies a primary-school building from the early Showa era.\n\n"
                "The corridor walls are bookshelves from top to bottom, and you may take down and read any manga on them. On a fine day people lie reading on the lawn that was once the playground. There are shelves of manga translated into other languages too, so you don’t need to read Japanese.\n\n"
                "It’s a good place to rest on a rainy day, or when the heat or cold has worn you out. Closed on Wednesdays. Last entry is 16:30, so if you took the 14:30 Sento Palace tour, it’s more relaxed to skip this and go straight to Nishiki Market.\n\nRecommended visit time: 15:45–16:30 (14:45–15:45 if you skip the Sento Palace)"),
         gmaps=[gm("京都国際マンガミュージアム", "Kyoto International Manga Museum", 35.0117, 135.75918, "京都国際マンガミュージアム")],
         links=[link("official", "京都国際マンガミュージアム 公式サイト", "Kyoto International Manga Museum (official)", "https://kyotomm.jp/", "https://kyotomm.jp/en/")],
         info=info([row("hours", "10:00〜17:00（最終入館16:30）", "10:00–17:00 (last entry 16:30)"), row("closed", "水曜。ほかに臨時の休みもあるので公式サイトで確認を", "Wednesdays; occasional other closures, see the website"),
                    row("fee", "大人1,200円、中高生400円、小学生200円", "Adults ¥1,200, ages 12–18 ¥400, 6–12 ¥200"),
                    row("train", "地下鉄 烏丸御池駅2番出口から歩いて2分。丸太町→烏丸御池は1駅・220円", "2 min on foot from exit 2 of Karasuma-Oike subway station; Marutamachi → Karasuma-Oike is one stop, ¥220")],
                   tip=T("京都国際マンガミュージアムの公式サイトと乗換案内で確認しました。" + WEBPHOTO_JA, "Checked on the museum website and Yahoo! Transit. " + WEBPHOTO_EN)),
         _first="manga"),
    dict(id="nishiki", name=T("錦市場", "Nishiki Market"), kind=T("市場", "Market"),
         blurb=T("「京の台所」と呼ばれる、長さ390mのアーケードの市場。魚、漬物、だし巻き、串ものの店が両側に並びます。",
                 "“Kyoto’s kitchen”: a 390-metre covered market lined on both sides with fish, pickles, rolled omelette and food on skewers."),
         lat=35.00502, lng=135.76557,
         text=T("錦市場（にしきいちば）\n\n地下鉄の四条駅から歩いて約5分（丸太町から四条まで3分・220円）、マンガミュージアムからは歩いて約13分。高倉通から寺町通まで東西390mのアーケードです。\n\n"
                "魚屋、漬物屋、だし巻き卵、湯葉、串にさした焼き魚や天ぷら。少しずつ買って食べるのが楽しい場所ですが、食べながら歩くのは商店街がやめてほしいと呼びかけています。買ったものは、その店の前か店の中で食べてください。イートインの席がある店も多いです。\n\n"
                "夕方は早く閉まる店が多いので、17時までに着くと安心です（営業時間は店ごとにちがいます）。昼どきはとても混みます。\n\n"
                "東の端は錦天満宮。そこから新京極を抜けて東へ7分歩くと先斗町と鴨川で、夕暮れの散歩と晩ごはんにちょうどいい場所です。\n\n"
                "写真1枚目は2025年11月。\n\nおすすめ訪問時間：15:30〜17:00（仙洞御所とマンガミュージアムの両方に入った日は16:45ごろから）",
                "Nishiki Market\n\nAbout 5 minutes on foot from Shijo subway station (Marutamachi to Shijo: 3 minutes, ¥220), or about 13 minutes’ walk from the Manga Museum. The arcade runs 390 m east to west from Takakura-dori to Teramachi-dori.\n\n"
                "Fishmongers, pickle shops, rolled omelette, yuba, grilled fish and tempura on skewers. Buying a little here and there is the fun of it, but the market association asks people not to eat while walking. Eat what you buy in front of the shop or inside it; many shops have a few seats.\n\n"
                "Many shops close early in the evening, so try to arrive by 17:00 (hours differ from shop to shop). It gets very crowded around lunchtime.\n\n"
                "At the east end is Nishiki Tenmangu shrine. Go on through Shinkyogoku and 7 minutes further east you reach Pontocho and the Kamo river, good for a walk at dusk and dinner.\n\n"
                "Photo 1 is from November 2025.\n\nRecommended visit time: 15:30–17:00 (from about 16:45 if you did both the Sento Palace and the Manga Museum)"),
         gmaps=[gm("錦市場（西の入口・高倉通）", "Nishiki Market (west end, Takakura-dori)", 35.00505, 135.7617, "錦市場 高倉通"),
                gm("錦天満宮（東の端）", "Nishiki Tenmangu (east end)", 35.00506, 135.76742, "錦天満宮"),
                gm("先斗町", "Pontocho", 35.0052, 135.7708, "先斗町 京都")],
         links=[link("official", "錦市場商店街 公式サイト", "Nishiki Market (official, Japanese)", "https://www.kyoto-nishiki.or.jp/"),
                link("info", "お願いとご案内（食べ歩きについて）", "Requests to visitors (about eating while walking, Japanese)", "https://www.kyoto-nishiki.or.jp/manner/")],
         info=info([row("hours", "営業時間と休みは店ごとにちがいます（要確認）", "Hours and closing days differ from shop to shop (please check)"),
                    row("fee", "食べながら歩かない。買った店の前か店の中で食べる（商店街のお願い）", "Don’t eat while walking: eat in front of or inside the shop where you bought it (market’s request)"),
                    row("train", "丸太町13:34発（地下鉄烏丸線）→ 四条13:37着・220円。四条駅から歩いて約5分", "Marutamachi 13:34 (Karasuma subway line) → Shijo 13:37, ¥220; about 5 min on foot from Shijo station")],
                   tip=T("錦市場商店街の公式サイト（長さ390m、食べ歩きについてのお願い）と乗換案内（2026年11月26日の時刻。昼は数分おきに出ています）で確認しました。歩く時間は OpenStreetMap で測った目安です。アーケードの写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the market association’s website (390 m long; request about eating while walking) and Yahoo! Transit (times for 26 November 2026; trains run every few minutes in the daytime). Walking times are estimates measured on OpenStreetMap. The arcade photos are from Wikimedia Commons (author and license shown on each photo).")),
         _extra="nishiki"),
]

# ネットから借りた写真（Wikimedia Commons）。ライセンスは Commons の API で 2026-11-21 に確認
WEB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gosho_web_photos.json"), encoding="utf-8"))

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    first, extra = s.pop("_first", None), s.pop("_extra", None)
    out.update(s)
    w = [cc(x["file"], x["author"], x["license"], x["title"]) for x in WEB.get(out["id"], [])]
    out["photos"] = photos(out["id"], w if first else None, w if extra else None)
    assert out["photos"], out["id"]
    out.setdefault("notices", [])
    spots.append(out)
NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}

data = {
    "id": "gosho",
    "_note": "京都の中心：二条城と京都御所のルート（gosho/ のページ専用。形は eizan-line.json と同じ）。地下鉄で二条城へ→（神泉苑・晴明神社）→地下鉄で丸太町→京都御苑の西側（しだれ桜・桃林・梅林・蛤御門）→京都御所→御苑の北側（紅葉・近衞邸跡・朔平門）→（梨木神社・仙洞御所）→（マンガミュージアム）→錦市場。"
             "写真は Toshi の写真ライブラリから選んだもの（御苑：2015年3月・2016年2月・2017年1月の雪・2017年11月の紅葉・2019年1月と3月・2020年4月・2023年4月、京都御所：2024年1月6日と11月6日、梨木神社：2026年5月18日、二条城の夜：2016年8月と2017年4月、錦市場：2025年11月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし。人が主役の写真、大学の建物、私的な写真は使っていない）。"
             "二条城の昼・神泉苑・晴明神社・蛤御門・仙洞御所・マンガミュージアム・錦市場のアーケードの写真は Wikimedia Commons（photos の要素が {file, credit}。一覧は scripts/gosho_web_photos.json。ライセンスは Commons の API で2026年11月21日に確認）。"
             "info.checked は事実情報を確認した日（二条城・宮内庁・国民公園協会・環境省・各寺社・マンガミュージアム・錦市場の公式サイト、電車は乗換案内）。このファイルは scripts/build_gosho_data.py で作る。",
    "sections": [
        {"first": NO["nijojo"], "last": NO["seimei"], "area": T("二条城のまわり", "Around Nijo Castle"), "title": T("朝いちばんに将軍の城へ", "The shogun’s castle, first thing")},
        {"first": NO["gyoen"], "last": NO["sento"], "area": T("京都御苑", "Imperial Palace Park"), "title": T("御所と、それを囲む広い公園", "The Palace and the park around it")},
        {"first": NO["manga"], "last": NO["nishiki"], "area": T("烏丸御池〜四条", "Karasuma-Oike to Shijo"), "title": T("午後は町なかへ", "Into town for the afternoon")},
    ],
    "plan": {"_note": "「選んで回る」の設定。全部選べる（駅などの自動で入る場所はない）。全部は1日に入りきらないので defaultMode: pick。",
             "defaultMode": "pick",
             "picks": [s["no"] for s in spots], "auto": {}, "hints": [
        H("seimei", {"any": [NO["seimei"]]},
          "晴明神社に寄る日は、二条城前のバス停から市バス9・12系統で北へ（230円）。お参りのあとは東へ歩いて約15分で御苑の中立売御門。先に京都御所へ入り、梅林・桃林はそのあとに。",
          "Visiting Seimei Shrine? Take city bus 9 or 12 north from the Nijojo-mae stop (¥230). Afterwards walk about 15 minutes east to the park’s Nakadachiuri gate; see the Palace first and the plum and peach groves after it."),
        H("gyoen", {"any": [NO["gyoen"], NO["gosho"]], "none": [NO["nijojo"], NO["shinsenen"], NO["seimei"]]},
          "二条城に寄らない日は、京都駅から地下鉄烏丸線で丸太町へ（約7分・260円）。御所だけなら、次の今出川駅が近いです（3番出口から歩いて約5分）。",
          "Skipping Nijo Castle? Take the Karasuma subway line from Kyoto Station to Marutamachi (about 7 min, ¥260). For the Palace alone, the next stop, Imadegawa, is closer (about 5 min on foot from exit 3)."),
        H("sento", {"any": [NO["sento"]]},
          "仙洞御所は申し込みが要ります（18歳以上・本人確認の書類）。予約がない日は、朝8:40からの当日券（先着50人）を先にもらってから二条城へ。",
          "The Sento Palace needs an application (ages 18+, bring ID). Without a booking, get a same-day ticket first (from 8:40, first 50 people), then go to Nijo Castle."),
        H("manga", {"any": [NO["manga"]], "andAny": [NO["sento"]]},
          "仙洞御所の14:30の回とマンガミュージアム（最終入館16:30）の両方に入ると、錦市場は17時前になります。閉まり始める店もあるので、どちらか一つにするとゆっくりできます。",
          "With both the 14:30 Sento Palace tour and the Manga Museum (last entry 16:30) you reach Nishiki Market just before 17:00, when some shops start closing. Choosing one of the two makes for an easier afternoon."),
        H("nishiki", {"any": [NO["nishiki"]], "none": [NO["manga"]]},
          "マンガミュージアムに寄らない日は、丸太町駅から地下鉄で四条へ（3分・220円）。駅から錦市場まで歩いて約5分です。",
          "Skipping the Manga Museum? Take the subway from Marutamachi to Shijo (3 min, ¥220); the market is about 5 minutes’ walk from the station."),
    ]},
    "photoBase": "../images/gosho/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
