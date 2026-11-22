#!/usr/bin/env python3
"""京都の中心：二条城と京都御所のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_gosho_data.py  （そのあと python3 scripts/sync_gosho.py）
- 作るもの（COURSES）:
  - data/routes/gosho.json … 「9〜10時に出発」（寺町通を歩いて北へ→梨木神社→御苑の北側→京都御所→檜垣でお昼→梅林・蛤御門
    →地下鉄で二条城（14時すぎ）→神泉苑→錦市場→先斗町・木屋町で夜）
  - data/routes/gosho-early.json … 「開城に合わせる」（8時すぎに出て二条城8:45→神泉苑→地下鉄で御苑→京都御所→檜垣でお昼
    →御苑の北側→梨木神社→寺町通を歩いて南へ（一保堂）→錦市場→先斗町・木屋町で夜）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方、「選んで回る」の設定
- 出発は京都の中心・三条のあたり（最寄りは地下鉄の京都市役所前駅）を想定。宿の名前は書かない
- 自分の写真は images/gosho/<スポットのid>-<番号>.jpg を番号の順に全部使う
- ネットから借りた写真（Wikimedia Commons）は images/gosho/<id>-w<番号>.jpg（一覧は scripts/gosho_web_photos.json）。
  スポットの web="first"（自分の写真の前）か "extra"（後ろ）で並べる位置を決める。ページでは写真の上に撮影者とライセンスが出る
- 神泉苑・晴明神社・仙洞御所・マンガミュージアムはオーナーが写真を撮っていない場所なので、文章にも行った日などは書かない
- 2026-11-22 オーナーの基準（ゲストが実際に回れる1日）で作り直した。地下鉄の時刻と運賃は乗換案内（Yahoo!路線情報、
  2026年11月28日・土曜のダイヤ）、開く時間・料金・休みは各公式サイト
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "gosho"
IMG = f"{R}/images/{MAP_ID}"
D21, D22 = "2026-11-21", "2026-11-22"   # 確認日（21日に確認して22日は見直していないものは D21）
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


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


def info(rows, source, tip=None, verified=True, checked=D22):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": checked, "source": source}
    if not verified:
        d["verified"] = False
    return d


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


# ネットから借りた写真（Wikimedia Commons）。ライセンスは Commons の API で 2026-11-21 に確認
WEB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gosho_web_photos.json"), encoding="utf-8"))


def photos(pid, where):
    """クレジットつきの写真（web="first"）→ 自分の写真（番号の順）→ クレジットつきの写真（web="extra"）の順に並べる。"""
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, []))]
    w = [cc(x["file"], x["author"], x["license"], x["title"]) for x in WEB.get(pid, [])]
    out = (w if where == "first" else []) + own + (w if where == "extra" else [])
    for p in out:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    assert out, pid
    return out


NIJO = "https://nijo-jocastle.city.kyoto.lg.jp/"
KUNAI = "https://kyoto-gosho.kunaicho.go.jp/"
GYOEN = "https://fng.or.jp/kyoto/"
IPPODO = "https://www.ippodo-tea.co.jp/pages/store-kyoto"
SUBWAY = link("timetable", "乗換案内（Yahoo!）", "Train times (Yahoo! Transit, Japanese)", "https://transit.yahoo.co.jp/")
WEBPHOTO_JA = "写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。"
WEBPHOTO_EN = "Photos are from Wikimedia Commons (author and license shown on each photo)."

# ---------------------------------------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容。body は見どころの説明（行き方とめやすの時間はコースごとに COURSES に書く）
# ---------------------------------------------------------------------------------------------------------
BASE = dict(
    nijojo=dict(
        name=T("二条城", "Nijo Castle"), kind=T("城（世界遺産）", "Castle (World Heritage)"), web="first",
        blurb=T("徳川家康が建て、慶喜が大政奉還を告げた城。国宝の二の丸御殿は、金のふすま絵と、歩くと鳴るうぐいす張りの廊下。開城は8:45、入城は16:00まで。",
                "Built by Tokugawa Ieyasu; here the last shogun announced the return of power to the emperor. The National Treasure Ninomaru Palace has gold-leaf screens and “nightingale” floors. Opens 8:45; last entry 16:00."),
        lat=35.01353, lng=135.74972,
        body=T("1603年に徳川家康が建てた城で、1867年に15代将軍の慶喜が大政奉還を告げた場所でもあります。東大手門から入り、金の飾りの唐門（からもん）をくぐると、国宝の二の丸御殿。部屋が奥へ奥へと続き、狩野派の虎や松のふすま絵が並びます。廊下は歩くとキュッキュッと鳴る「うぐいす張り」。御殿の中は靴を脱いで上がり、撮影はできません。冬は床が冷たいので厚手の靴下を。\n\n"
               "回る順番は、二の丸御殿（40〜50分）→二の丸庭園→内堀を渡って本丸→天守閣跡の石垣の上→北側の清流園を通って出口へ。全部で1時間半〜2時間です。天守閣跡に上ると、本丸御殿の屋根と京都の町が見渡せます。\n\n"
               "入城券と二の丸御殿のセットで1,300円。本丸御殿（2024年に修理が終わって公開）は別に1,000円で、日時を決めたWEBチケットの事前予約が要ります（来城日の30日前から）。\n\n"
               "夜の写真は2016年8月と2017年4月の夜のライトアップのときのもの。夜の公開は年によって内容も期間も変わるので、公式サイトで確認してください。",
               "Tokugawa Ieyasu built the castle in 1603, and in 1867 the 15th shogun, Yoshinobu, announced here that he was returning power to the emperor. Enter by the East Gate, pass under the gold-fitted Karamon gate, and you reach the Ninomaru Palace, a National Treasure. Room leads on to room, lined with Kano-school tigers and pines on gold leaf. The corridor floors chirp underfoot (“nightingale floors”). You take your shoes off to go in, and photography is not allowed inside. The floors are cold in winter: wear thick socks.\n\n"
               "A good order: the Ninomaru Palace (40–50 minutes) → the Ninomaru garden → across the inner moat to the Honmaru → up the stone base of the old keep → out through the Seiryu-en garden on the north side. Allow an hour and a half to two hours. From the keep base you look over the Honmaru Palace roofs and the city.\n\n"
               "Castle entry with the Ninomaru Palace is ¥1,300. The Honmaru Palace (reopened in 2024 after repairs) costs another ¥1,000 and needs a timed web ticket booked in advance (on sale from 30 days before).\n\n"
               "The night photos are from evening illuminations in August 2016 and April 2017. Evening openings change from year to year, so check the official website."),
        gmaps=[gm("二条城 東大手門（入口）", "Nijo Castle East Gate (entrance)", 35.01425, 135.75205, "二条城 東大手門")],
        links=[link("official", "二条城 公式サイト", "Nijo Castle (official)", NIJO, NIJO + "?lang=en"),
               link("info", "開城時間・休城日（公式）", "Hours & closed days (official, Japanese)", NIJO + "guide/annai/"),
               link("info", "料金・本丸御殿の予約（公式）", "Fees & Honmaru Palace tickets (official)", NIJO + "admission/"), SUBWAY],
        notices=[notice("12月6日（日）は入城の受付が12:00まで", "On Sunday 6 December, last entry is 12:00",
                        "2026年12月6日（日）は行事（寛永行幸400年の行列）のため、入城の受付が12:00まで、二の丸御殿の受付が12:10までになります（閉城は17:00のまま）。この日に行くなら「開城に合わせる」コースで。",
                        "On Sunday 6 December 2026, because of an event (a procession marking 400 years since the Kan’ei imperial visit), last entry to the castle is 12:00 and to the Ninomaru Palace 12:10 (the castle still closes at 17:00). If you go that day, use the “Castle at opening” course.",
                        url=NIJO + "news/12-6uketsuke/", to="2026-12-06"),
                 notice("12月と1月の火曜は、二の丸御殿に入れません", "No Ninomaru Palace on Tuesdays in December and January",
                        "1月・7月・8月・12月の火曜（祝日のときは翌日）と12月26〜28日、1月1〜3日は、二の丸御殿の観覧が休みです。城には入れますが、いちばんの見どころが見られないので、別の曜日に。12月29〜31日は城ごと休みです。",
                        "The Ninomaru Palace is closed on Tuesdays in January, July, August and December (the next day if Tuesday is a holiday), on 26–28 December and on 1–3 January. The castle grounds are open, but you would miss the main sight: choose another day. The whole castle is closed on 29–31 December.",
                        url=NIJO + "guide/annai/", frm="2026-11-25", to="2027-01-31"),
                 notice("二の丸御殿の中は撮影禁止。本丸御殿は事前予約制", "No photos inside the Ninomaru Palace; the Honmaru Palace is by advance booking",
                        "二の丸御殿は靴を脱いで上がります。本丸御殿（別に1,000円）はWEBチケットで日時を予約した人だけ入れます。予約がなくても、本丸の庭と天守閣跡には入城券で入れます。",
                        "You take your shoes off in the Ninomaru Palace. The Honmaru Palace (¥1,000 extra) is only for visitors with a timed web ticket. Without one you can still walk the Honmaru garden and climb the keep base on the ordinary ticket.",
                        url=NIJO + "admission/")],
        rows=[row("hours", "開城 8:45、入城は16:00まで（閉城17:00）。二の丸御殿の受付は8:45〜16:10、本丸御殿（要予約）は9:30〜16:00",
                  "Opens 8:45; last entry 16:00 (closes 17:00). Ninomaru Palace entry 8:45–16:10; Honmaru Palace (booking required) 9:30–16:00"),
              row("closed", "休城は12月29〜31日。二の丸御殿は1月・7月・8月・12月の火曜（祝日なら翌日）と12月26〜28日、1月1〜3日は入れません。本丸御殿は毎月第3月曜とその翌日（祝日なら開く）も休み",
                  "Castle closed 29–31 December. The Ninomaru Palace is also closed on Tuesdays in January, July, August and December (next day if a holiday), 26–28 December and 1–3 January. The Honmaru Palace is also closed on the third Monday of each month and the day after (open if a holiday)"),
              row("fee", "入城＋二の丸御殿 一般1,300円（入城だけなら800円、中高生400円、小学生300円）。本丸御殿は別に一般1,000円・中高生300円・小学生200円（要予約）",
                  "Castle + Ninomaru Palace ¥1,300 (castle only ¥800; ages 12–18 ¥400, 6–12 ¥300). Honmaru Palace extra: ¥1,000, ages 12–18 ¥300, 6–12 ¥200 (booking required)"),
              row("train", "地下鉄東西線 二条城前駅の1番出口から東大手門まで歩いて約5分。京都市役所前から4分・220円、三条京阪から6分・220円（数分おき）",
                  "About 5 min on foot from exit 1 of Nijojo-mae station (Tozai subway line) to the East Gate. From Kyoto Shiyakusho-mae 4 min, ¥220; from Sanjo Keihan 6 min, ¥220 (every few minutes)")],
        source="二条城の公式サイト（開城時間・休城日等、料金、12月6日のお知らせ）、乗換案内（2026年11月28日のダイヤ）",
        tip=T("二条城の公式サイトと乗換案内（2026年11月28日・土曜の時刻）で確認しました。地下鉄一日券か地下鉄・バス一日券を当日の券売所で見せると、入城料800円が700円になります（公式サイト。WEBチケットでは割引になりません）。京都駅からは地下鉄烏丸線で烏丸御池へ、東西線に乗り換えて約15分・260円です。唐門・二の丸御殿・二の丸庭園・本丸の昼の写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
              "Checked on the castle website and Yahoo! Transit (times for Saturday 28 November 2026). Show a subway or subway & bus one-day pass at the ticket office and the ¥800 entry fee becomes ¥700 (castle website; not available with web tickets). From Kyoto Station: Karasuma subway line to Karasuma-Oike, change to the Tozai line, about 15 minutes, ¥260. The daytime photos of the Karamon gate, Ninomaru Palace, garden and Honmaru are from Wikimedia Commons (author and license shown on each photo).")),
    shinsenen=dict(
        name=T("神泉苑", "Shinsen-en"), kind=T("寺・池", "Temple & pond"), web="first",
        blurb=T("二条城のすぐ南。平安京ができたときの天皇の庭の名残で、池に朱色の法成橋がかかります。無料、20:00まで。",
                "Just south of the castle: what remains of the emperor’s garden from the founding of Kyoto, with the vermilion Hojo bridge over its pond. Free, open until 20:00."),
        lat=35.01155, lng=135.74807,
        body=T("794年、平安京と一緒に桓武天皇が造った庭（禁苑）の名残です。もとはずっと広く、二条城を造るときに大きく削られて、今の広さになりました。\n\n"
               "池にかかる朱色の法成橋（ほうじょうばし）と、池の中の善女龍王社（ぜんにょりゅうおうしゃ）が見どころ。824年に空海がここで雨乞いをして、龍王を呼んだと伝わります。疫病をしずめるためにここで行われた御霊会（ごりょうえ）は、祇園祭の始まりとされています。\n\n"
               "境内は無料で、10〜15分で回れます。二条城の大きさを見たあとだと、ここが城より800年古い庭だということがよく分かります。",
               "This is what is left of the imperial garden Emperor Kanmu laid out in 794 along with the new capital. It was once far larger; much of it was taken when Nijo Castle was built.\n\n"
               "Look for the vermilion Hojo bridge over the pond and the small shrine to the dragon queen Zennyo Ryuo on the island. In 824 the monk Kukai is said to have prayed for rain here and summoned the dragon. A ritual held here to calm an epidemic is counted as the origin of the Gion Festival.\n\n"
               "Entry is free and 10–15 minutes is enough. After the scale of the castle, it is striking that this garden is 800 years older."),
        gmaps=[gm("神泉苑", "Shinsen-en", 35.01155, 135.74807, "神泉苑 京都")],
        links=[link("official", "神泉苑 公式サイト", "Shinsen-en (official, Japanese)", "http://www.shinsenen.org/")],
        rows=[row("hours", "境内の参拝 6:30〜20:00", "Grounds open 6:30–20:00"), row("fee", "無料", "Free"),
              row("train", "地下鉄東西線 二条城前駅から歩いて約2分（神泉苑の案内）", "About 2 min on foot from Nijojo-mae station, Tozai subway line (temple’s access page)")],
        source="神泉苑の公式サイト", checked=D21,
        tip=T("神泉苑の公式サイトで確認しました。二条城からの歩く時間は OpenStreetMap で測った目安です。" + WEBPHOTO_JA,
              "Checked on the temple website. The walking time from the castle is an estimate measured on OpenStreetMap. " + WEBPHOTO_EN)),
    seimei=dict(
        name=T("晴明神社", "Seimei Shrine"), kind=T("神社", "Shrine"), web="first",
        blurb=T("陰陽師・安倍晴明をまつる神社。鳥居にも提灯にも、五芒星（晴明桔梗）の印。寄り道で、20分ほど。",
                "The shrine of Abe no Seimei, the Heian-period yin-yang master; his five-pointed star is on the torii and the lanterns. A side stop of about 20 minutes."),
        lat=35.02776, lng=135.75114,
        body=T("平安時代の陰陽師、安倍晴明（あべのせいめい）の屋敷があった場所に建つ神社です。\n\n"
               "一の鳥居の額は、神社の名前ではなく金色の五芒星（ごぼうせい）。「晴明桔梗」と呼ばれる神社の紋です。境内には、晴明が念力で湧かせたと伝わる「晴明井」、なでて厄を落とす「厄除桃」、昔の一条戻橋の欄干と式神の石像があります。小さな境内なので20分ほどで回れます。",
               "The shrine stands where the house of Abe no Seimei, the Heian-period yin-yang master, once stood.\n\n"
               "The plaque on the first torii carries not the shrine’s name but a golden five-pointed star, the shrine’s crest. Inside are the Seimei well, said to have sprung up by Seimei’s power; a bronze peach you stroke to rub off bad luck; and the railing posts of the old Ichijo Modoribashi bridge with a stone figure of his spirit servant. It’s a small precinct: 20 minutes is enough."),
        gmaps=[gm("晴明神社", "Seimei Shrine", 35.02776, 135.75114, "晴明神社 京都")],
        links=[link("official", "晴明神社 公式サイト", "Seimei Shrine (official, Japanese)", "https://www.seimeijinja.jp/"),
               link("timetable", "市バスの時刻表（京都市交通局）", "City bus timetables (Kyoto City, Japanese)", "https://www.city.kyoto.lg.jp/kotsu/")],
        rows=[row("hours", "9:00〜17:00（授与所は16:30まで）", "9:00–17:00 (amulet counter until 16:30)"), row("closed", "無休", "Open every day"), row("fee", "無料", "Free"),
              row("bus", "市バス9・12系統「一条戻橋・晴明神社前」すぐ・230円。バスの時刻は要確認", "City bus 9 or 12 to “Ichijo-modoribashi / Seimei-jinja-mae”, right outside, ¥230. Bus times: please check")],
        source="晴明神社の公式サイト（時間・バスの系統）。バスの時刻は未確認", checked=D21,
        tip=T("晴明神社の公式サイトで確認しました（バスの系統も公式サイトの案内）。バスの時刻は確認していません。歩く時間と距離は OpenStreetMap で測った目安です。" + WEBPHOTO_JA,
              "Checked on the shrine website (bus numbers are from its access page). Bus times were not checked. Walking times and distances are estimates measured on OpenStreetMap. " + WEBPHOTO_EN)),
    gyoen=dict(
        name=T("京都御苑：梅林・桃林と蛤御門", "Imperial Palace Park: plum & peach groves, Hamaguri gate"), kind=T("公園", "Park"), web="extra",
        blurb=T("御所を囲む、24時間入れる無料の公園。西側に、しだれ桜・桃林・梅林と、弾の跡が残る蛤御門。",
                "The free park around the Palace, open round the clock. On its west side: a weeping cherry, peach and plum groves, and the Hamaguri gate with its bullet marks."),
        lat=35.0218, lng=135.7604,
        body=T("京都御苑は、京都御所を囲む東西約700m・南北約1.3kmの公園。江戸時代まで約200の公家屋敷が並んでいた場所で、今は玉砂利の広い道と松林です。毎日24時間、無料で入れます。\n\n"
               "西側の南から順に、出水（でみず）の小川のそばに御苑でも早く咲くしだれ桜（写真1枚目は2015年3月25日）。その北が約70本の桃林（見ごろは3月中旬〜4月上旬）、続いて約130本の梅林（2月中旬〜3月中旬）。梅の写真は2016年2月22日と2019年3月2日、花の色が混ざった4月の写真は2023年4月10日です。花のない季節は、松と大きなクスノキの下の静かな道です。\n\n"
               "梅林のすぐ北が蛤御門（はまぐりごもん）。1864年の「禁門の変」で長州藩と会津・薩摩藩が戦った場所で、門の柱や梁に、そのときのものと伝わる弾の跡が残っています。\n\n"
               "玉砂利は思ったより足が疲れます。自転車が通ってできた細いわだち（砂利のない筋）の上を歩くと楽です。",
               "Kyoto Gyoen is the park around the Imperial Palace, about 700 m east to west and 1.3 km north to south. Until the end of the Edo period some 200 court nobles’ houses stood here; now it is wide gravel avenues and pines. It’s open 24 hours a day and free.\n\n"
               "On the west side, from the south: by the Demizu stream is a weeping cherry that flowers early (photo 1: 25 March 2015). North of it is the peach grove, about 70 trees (best mid-March to early April), then the plum grove, about 130 trees (mid-February to mid-March). The plum photos are from 22 February 2016 and 2 March 2019; the April photos with mixed colours are from 10 April 2023. Out of season it is a quiet path under pines and big camphor trees.\n\n"
               "Just north of the plums is the Hamaguri gate. In 1864 Choshu troops fought the Aizu and Satsuma domains here (the Kinmon incident), and the gate’s posts and beams still carry what are said to be bullet marks from that day.\n\n"
               "The gravel is more tiring than it looks. Walk along the narrow tracks worn clear by bicycles."),
        gmaps=[gm("出水の小川（しだれ桜）", "Demizu stream (weeping cherry)", 35.02011, 135.7607, "京都御苑 出水の小川"),
               gm("蛤御門", "Hamaguri gate", 35.02315, 135.7596, "蛤御門 京都御苑"),
               gm("地下鉄 丸太町駅", "Marutamachi subway station", 35.01741, 135.75955, "丸太町駅 京都市営地下鉄")],
        links=[link("official", "京都御苑（国民公園協会）", "Kyoto Gyoen (National Parks Foundation, Japanese)", GYOEN),
               link("info", "京都御苑（環境省）", "Kyoto Gyoen (Ministry of the Environment)", "https://www.env.go.jp/garden/kyotogyoen/"), SUBWAY],
        rows=[row("hours", "24時間入れます", "Open 24 hours"), row("fee", "無料", "Free"),
              row("train", "地下鉄烏丸線 丸太町駅の1番出口から、御苑の南西の角まで歩いて約5分。二条城前〜丸太町は烏丸御池で乗り換えて10〜12分・220円",
                  "About 5 min on foot from exit 1 of Marutamachi station (Karasuma subway line) to the park’s south-west corner. Nijojo-mae to Marutamachi: change at Karasuma-Oike, 10–12 min, ¥220"),
              row("hours", "梅は2月中旬〜3月中旬、桃は3月中旬〜4月上旬（国民公園協会の案内）", "Plums mid-Feb to mid-March, peaches mid-March to early April (park foundation’s guide)")],
        source="環境省と国民公園協会の京都御苑のサイト、乗換案内（2026年11月28日のダイヤ）",
        tip=T("環境省と国民公園協会の京都御苑のサイト、乗換案内（2026年11月28日・土曜の時刻）で確認しました。歩く時間は OpenStreetMap で測った目安です。蛤御門の写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
              "Checked on the park’s websites (Ministry of the Environment and the National Parks Foundation) and Yahoo! Transit (times for Saturday 28 November 2026). Walking times are estimates measured on OpenStreetMap. The photo of the Hamaguri gate is from Wikimedia Commons (author and license shown on the photo).")),
    gosho=dict(
        name=T("京都御所", "Kyoto Imperial Palace"), kind=T("御所", "Palace"), web=None,
        blurb=T("明治まで約500年、天皇の住まいだった場所。予約なし・無料。月曜休みで、冬は15:20までに入場。お昼はすぐ横の休憩所で。",
                "The emperors’ home for some 500 years until 1869. Free, no booking. Closed Mondays; in winter enter by 15:20. Lunch at the rest house next door."),
        lat=35.02583, lng=135.76102,
        body=T("1331年から明治のはじめまで、天皇が住んでいた場所です。今の建物は1855年に、平安時代の様式で建て直されたもの。予約はいらず、無料で入れます。入口は西側の清所門（せいしょもん）で、入るときに手荷物検査があります。小さな荷物は、入ってすぐの参観者休所のロッカーに預けられます。\n\n"
               "順路は約50分。御車寄（おくるまよせ）、朱色の回廊と承明門（じょうめいもん）、その奥に即位の礼が行われた紫宸殿（ししんでん）。写真2枚目のように、承明門の柱のあいだから紫宸殿を正面に見られます。続いて清涼殿、池に欅橋がかかる御池庭（おいけにわ）、御常御殿と御内庭へ。建物の中には入れず、外から見ます。\n\n"
               "職員の案内（無料・予約なし、約50分）は英語と中国語が10:00・14:00、日本語が9:30・10:30・13:30・14:30。開始時間までに参観者休所へ。時間が合わなければ、無料の音声ガイドアプリ（6言語）を先にスマホに入れておくと便利です。\n\n"
               "お昼は、清所門から歩いて3分の中立売（なかだちうり）休憩所で。レストラン「檜垣（ひがき）」は8:00〜18:30（ラストオーダー18:00）で、年末年始のほかは休みなし。無料で座れる休憩スペースと売店（9:00〜16:30）もあります。御苑の中に食事ができる場所は少ないので、ここで食べるのがいちばん楽です。\n\n"
               "写真は2024年1月6日と11月6日。",
               "The emperors lived here from 1331 until the start of the Meiji era. The present buildings were rebuilt in 1855 in the style of the Heian period. No booking, no charge. The entrance is the Seishomon gate on the west side; bags are checked as you go in. Small bags can go in the lockers in the visitors’ rest house just inside.\n\n"
               "The route takes about 50 minutes: the Okurumayose carriage porch, the vermilion corridors and Jomeimon gate, and beyond them the Shishinden, the hall of enthronements. As in photo 2, you can look straight at the Shishinden between the pillars of the Jomeimon. Then come the Seiryoden, the Oikeniwa pond garden with its Keyaki bridge, and the Otsunegoten with its inner garden. You see the buildings from outside; you can’t go in.\n\n"
               "Free staff-guided tours (no booking, about 50 minutes): English and Chinese at 10:00 and 14:00; Japanese at 9:30, 10:30, 13:30 and 14:30. Be at the visitors’ rest house by the start time. If the times don’t suit, install the free audio-guide app (six languages) on your phone beforehand.\n\n"
               "For lunch, the Nakadachiuri rest house is 3 minutes’ walk from the Seishomon gate. Its restaurant, Higaki, is open 8:00–18:30 (last order 18:00) every day except the New Year holidays, and there is a free seating area and a shop (9:00–16:30). There are few places to eat inside the park, so this is the easy choice.\n\n"
               "Photos: 6 January and 6 November 2024."),
        gmaps=[gm("清所門（京都御所の入口）", "Seishomon gate (Palace entrance)", 35.02583, 135.76102, "京都御所 清所門"),
               gm("中立売休憩所（お昼）", "Nakadachiuri rest house (lunch)", 35.0256, 135.7599, "京都御苑 中立売休憩所")],
        links=[link("official", "京都御所（宮内庁）", "Kyoto Imperial Palace (Imperial Household Agency)", KUNAI, KUNAI + "en"),
               link("info", "参観要領・カレンダー", "Visiting guide & calendar", KUNAI + "visit", KUNAI + "en/visit"),
               link("info", "中立売休憩所（国民公園協会）", "Nakadachiuri rest house (Japanese)", GYOEN + "place/rest/")],
        notices=[notice("月曜休み。冬は15:20までに入場。飲食とスーツケースは不可", "Closed Mondays; in winter enter by 15:20. No food, no suitcases",
                        "京都御所の公開は、月曜（祝日のときは翌日）と12月28日〜1月4日が休みです。行事で休む日もあるので、行く前に宮内庁の参観カレンダーを見てください。入場は10〜2月が15:20まで、3月と9月が15:50まで、4〜8月が16:20まで。中で食事はできず、スーツケースなどの大きな荷物とペットは持ち込めません。",
                        "The Palace is closed on Mondays (the next day if Monday is a holiday) and from 28 December to 4 January, and sometimes for court events, so check the Imperial Household Agency’s calendar first. Last entry is 15:20 from October to February, 15:50 in March and September, and 16:20 from April to August. You can’t eat inside, and suitcases, other large bags and pets are not allowed.",
                        url=KUNAI + "visit")],
        rows=[row("hours", "入場 9:00〜15:20（10〜2月、最終退出16:00）／〜15:50（3月・9月、最終退出16:30）／〜16:20（4〜8月、最終退出17:00）",
                  "Entry 9:00–15:20 (Oct–Feb, out by 16:00) / until 15:50 (Mar & Sep, out by 16:30) / until 16:20 (Apr–Aug, out by 17:00)"),
              row("closed", "月曜（祝日のときは翌日）、12月28日〜1月4日、行事のある日（カレンダーで確認）", "Mondays (next day if a holiday), 28 Dec–4 Jan, and days of court events (see the calendar)"),
              row("fee", "無料・予約不要", "Free, no booking"),
              row("train", "地下鉄烏丸線 今出川駅3番出口から歩いて約5分（丸太町駅からは御苑の中を歩いて約20分）", "About 5 min on foot from exit 3 of Imadegawa station, Karasuma subway line (about 20 min through the park from Marutamachi)"),
              row("hours", "中立売休憩所：レストラン「檜垣」8:00〜18:30（ラストオーダー18:00）、売店9:00〜16:30。年末年始のほかは無休",
                  "Nakadachiuri rest house: Higaki restaurant 8:00–18:30 (last order 18:00), shop 9:00–16:30; open daily except the New Year holidays")],
        source="宮内庁の京都御所のサイト（参観要領・よくあるご質問）、国民公園協会の京都御苑のサイト（食事・お土産）",
        tip=T("宮内庁の京都御所のサイト（参観要領・よくあるご質問）と、国民公園協会の京都御苑のサイトで確認しました。檜垣のメニューと値段は確認していません。",
              "Checked on the Imperial Household Agency’s Kyoto Imperial Palace website (visiting guide and FAQ) and the park foundation’s website. Higaki’s menu and prices were not checked.")),
    kitagyoen=dict(
        name=T("京都御苑の北側：紅葉・近衞邸跡のしだれ桜", "North side of the park: maples & the Konoe weeping cherries"), kind=T("公園", "Park"), web=None,
        blurb=T("御所の北は人が少なくて静か。秋は乾御門のあたりのもみじとイチョウ、春は近衞邸跡のしだれ桜、冬は雪の松林。和菓子屋のカフェがある休憩所も。",
                "North of the Palace it’s quiet. Maples and ginkgo near the Inui gate in autumn, weeping cherries at the old Konoe residence in spring, snow on the pines in winter; and a rest house with a sweet-maker’s café."),
        lat=35.02832, lng=135.76191,
        body=T("御苑の北西、乾御門（いぬいごもん）の近くは、秋になるともみじが赤く、大きなイチョウが黄色くなります（写真1〜5枚目は2017年11月23日）。芝生に落ち葉が積もり、お寺の紅葉とちがって人が少なく、無料です。\n\n"
               "その東が近衞邸跡（このえていあと）。五摂家の近衞家の屋敷があった場所で、池のまわりに約60本のしだれ桜（糸桜）があります。御苑でいちばん早く、3月中旬に咲き始め、種類によって時期がずれるので1か月ほど楽しめます。\n\n"
               "近衞邸跡のそばの休憩所には、和菓子の笹屋伊織（ささやいおり）のカフェ「SASAYAIORI+ 京都御苑」が入っています。10:00から、10〜2月は16:30（ラストオーダー16:00）、3〜9月は17:00（同16:30）まで。月曜（祝日のときは次の平日）と年末年始は休みです。席だけ使える無料の休憩所でもあるので、歩き疲れたらここで座れます。\n\n"
               "御所の北の門が朔平門（さくへいもん、写真10枚目）。ここから御所の東側へ回ると、長い築地塀（ついじべい）と松林が続きます。雪の写真は2017年1月15日と2019年1月27日。京都の町なかで雪が積もるのは年に数回なので、積もった朝はまずここへ。",
               "In the north-west of the park, near the Inui gate, the maples turn red and a big ginkgo turns yellow in autumn (photos 1–5: 23 November 2017). Leaves pile up on the grass; unlike the temples, there are few people and no charge.\n\n"
               "East of it is the site of the Konoe residence, home of one of the five regent families, with about 60 weeping cherries around a pond. They are the first in the park to flower, from mid-March, and as the varieties differ the blossom lasts about a month.\n\n"
               "The rest house beside the Konoe site has a café run by the Kyoto sweet-maker Sasaya Iori, SASAYAIORI+ Kyoto Gyoen. It opens at 10:00 and closes at 16:30 from October to February (last order 16:00) and 17:00 from March to September (last order 16:30); closed Mondays (the next weekday if a holiday) and over the New Year. It is also a free rest house, so you can simply sit down.\n\n"
               "The Palace’s north gate is the Sakuheimon (photo 10). Walk round from here to the east side and the long earthen wall and pine woods go on and on. The snow photos are from 15 January 2017 and 27 January 2019. Snow settles in central Kyoto only a few times a year; on such a morning, come here first."),
        gmaps=[gm("近衞邸跡", "Konoe residence site", 35.02832, 135.76191, "京都御苑 近衛邸跡"),
               gm("乾御門", "Inui gate", 35.02748, 135.75963, "乾御門 京都御苑"),
               gm("近衞邸跡休憩所（SASAYAIORI+）", "Konoe rest house (SASAYAIORI+ café)", 35.0285, 135.7611, "SASAYAIORI+ 京都御苑")],
        links=[link("official", "京都御苑の自然（国民公園協会）", "Nature in Kyoto Gyoen (Japanese)", GYOEN + "place/creature/"),
               link("info", "近衞邸跡休憩所（国民公園協会）", "Konoe rest house (Japanese)", GYOEN + "place/rest/"),
               link("info", "叡山電鉄のマップ（下鴨神社）", "Eizan Railway map (Shimogamo Shrine)", "../eizan-line/")],
        rows=[row("hours", "24時間入れます", "Open 24 hours"), row("fee", "無料", "Free"),
              row("hours", "近衞邸跡休憩所（SASAYAIORI+）：10:00〜16:30（10〜2月、ラストオーダー16:00）／〜17:00（3〜9月、同16:30）。月曜（祝日なら次の平日）と年末年始は休み",
                  "Konoe rest house (SASAYAIORI+): 10:00–16:30 (Oct–Feb, last order 16:00) / until 17:00 (Mar–Sep, last order 16:30). Closed Mondays (next weekday if a holiday) and New Year"),
              row("hours", "近衞邸跡のしだれ桜は3月中旬から約1か月（国民公園協会の案内）。紅葉の時期は年によって変わります", "Konoe weeping cherries: about a month from mid-March (park foundation’s guide). Autumn colour varies by year"),
              row("train", "地下鉄烏丸線 今出川駅まで歩いて約5分", "About 5 min on foot to Imadegawa station, Karasuma subway line")],
        source="国民公園協会の京都御苑のサイト（自然、食事・お土産）",
        tip=T("国民公園協会の京都御苑のサイトで確認しました。歩く時間は OpenStreetMap で測った目安です。紅葉の見ごろの時期は公式の案内がないので、写真の日付（11月23日）を目安にしてください。",
              "Checked on the park foundation’s website. Walking times are estimates measured on OpenStreetMap. There is no official guide to the autumn-colour dates; use the date of the photos (23 November) as a rough guide.")),
    nashinoki=dict(
        name=T("梨木神社", "Nashinoki Shrine"), kind=T("神社・名水", "Shrine & spring water"), web=None,
        blurb=T("御苑の東の門を出てすぐの、木立の中の小さな神社。京都三名水でただ一つ残る「染井」の水が湧いています。門は16:30まで。",
                "A small shrine in the trees just outside the park’s east gate, with Somei, the only one of Kyoto’s three famous wells still flowing. Gates close at 16:30."),
        lat=35.02454, lng=135.76733,
        body=T("御苑の東側の清和院御門（せいわいんごもん）を出てすぐ北。明治18年に、明治維新に尽くした三條實萬（さねつむ）・實美（さねとみ）の親子をまつって建てられた神社です。萩の名所で、9月下旬に萩まつりがあります。\n\n"
               "手水舎の水は「染井（そめい）」。京都三名水のうち、今も湧いているただ一つの井戸です。蛇口から自由に汲めて、口にふくむとやわらかい水です（蛇口が開いているのは6:00〜18:30ごろ）。空のペットボトルを持って行くと、持ち帰れます。\n\n"
               "境内の古い茶室は、今はコーヒースタンド「Coffee Base NASHINOKI」。染井の水でいれたコーヒーが飲めます（写真6・7枚目。営業の日と時間は要確認）。\n\n"
               "写真は2026年5月18日、青もみじの時期です。",
               "Just north of the Seiwain gate on the east side of the park. The shrine was founded in 1885 for Sanjo Sanetsumu and his son Sanetomi, court nobles who worked for the Meiji Restoration. It is known for bush clover, with a festival in late September.\n\n"
               "The water at the purification basin is Somei, the only one of Kyoto’s three famous wells that still flows. Anyone may fill a bottle from the taps; the water tastes soft (taps are open from about 6:00 to 18:30). Bring an empty bottle and take some with you.\n\n"
               "The old tea room in the grounds is now a coffee stand, Coffee Base NASHINOKI, brewing with Somei water (photos 6 and 7; opening days and hours: please check).\n\n"
               "Photos: 18 May 2026, with the maples in fresh green."),
        gmaps=[gm("梨木神社", "Nashinoki Shrine", 35.02454, 135.76733, "梨木神社 京都"),
               gm("一保堂茶舗 京都本店（寺町二条）", "Ippodo Tea, Kyoto main store (Teramachi Nijo)", 35.01437, 135.76745, "一保堂茶舗 京都本店")],
        links=[link("official", "梨木神社 公式サイト", "Nashinoki Shrine (official, Japanese)", "https://www.nashinoki.jp/"),
               link("info", "一保堂茶舗 京都本店（公式）", "Ippodo Tea, Kyoto main store (official)", IPPODO)],
        rows=[row("hours", "開門7:30、閉門16:30。授与所は9:00〜16:30（12:15〜13:15は休み）", "Gates 7:30–16:30; amulet counter 9:00–16:30 (closed 12:15–13:15)"),
              row("fee", "無料", "Free"),
              row("hours", "染井の水の蛇口は6:00〜18:30ごろ", "Somei water taps: about 6:00–18:30"),
              row("hours", "Coffee Base NASHINOKI の営業時間は公式の情報で確認できていません（要確認）", "Coffee Base NASHINOKI’s hours could not be confirmed from an official source (please check)"),
              row("hours", "寺町通の一保堂茶舗 京都本店：店も喫茶室「嘉木」も10:00〜17:00（喫茶室のラストオーダー16:30）。第2水曜休み",
                  "Ippodo Tea main store on Teramachi-dori: shop and Kaboku tearoom 10:00–17:00 (tearoom last order 16:30); closed on the second Wednesday of the month")],
        source="梨木神社の公式サイト（2026-11-21）、一保堂茶舗の公式サイト（京都本店、2026-11-22）",
        tip=T("梨木神社の公式サイト（11月21日）と一保堂茶舗の公式サイト（11月22日）で確認しました。寺町通を歩く時間は OpenStreetMap で測った目安です。",
              "Checked on the shrine website (21 November) and the Ippodo website (22 November). Walking times along Teramachi-dori are estimates measured on OpenStreetMap.")),
    sento=dict(
        name=T("京都仙洞御所", "Sento Imperial Palace"), kind=T("庭園（要申し込み）", "Garden (application needed)"), web="first",
        blurb=T("退位した天皇の御所の庭。二つの池と、丸い石を敷きつめた洲浜を、職員の案内で約1時間歩きます。申し込みが必要、18歳以上・無料。",
                "The garden of the retired emperors’ palace: two ponds and a shore of rounded stones, seen on a one-hour guided walk. Application needed; ages 18 and over, free."),
        lat=35.02168, lng=135.76563,
        body=T("17世紀のはじめ、退位した後水尾上皇のために造られた御所です。建物は1854年の火事で焼けて、庭が残りました。北池と南池のまわりを歩く庭で、南池の岸は、平たく丸い石を一面に敷きつめた洲浜（すはま）になっています。\n\n"
               "自由には入れず、職員の案内で約1時間（約1km）。開始は9:30・11:00・13:30・14:30・15:30で、7・8月は原則9:30・11:00・15:30だけです。参観できるのは18歳以上（子ども連れは入れません）、無料。全員の本人確認の書類（外国の人はパスポート）が要ります。\n\n"
               "申し込みは2通り。①宮内庁のサイトで、行く月の3か月前の1日から、3日前までに予約（1件4人まで）。②当日、仙洞御所の前で8:40から先着順に配る整理券（1日50人、各回10人。予約の空きが出た分は足されます）。確実に入りたい人は予約を。\n\n"
               "説明は日本語です。英語・中国語・フランス語・韓国語・スペイン語の音声ガイドを無料で借りられます（数に限りあり）。手すりのない細い石橋や飛び石があるので、歩きやすい靴で。入口は御苑の中、清和院御門から西へ入ったところです。",
               "Built in the early 17th century for the retired emperor Go-Mizunoo. The buildings burned down in 1854; the garden remains. You walk round a north pond and a south pond, and the shore of the south pond is paved all over with flat, rounded stones.\n\n"
               "You can’t walk in freely: visits are guided by staff and take about an hour (about 1 km). Tours start at 9:30, 11:00, 13:30, 14:30 and 15:30; in July and August normally only 9:30, 11:00 and 15:30. Visitors must be 18 or over (no children, even accompanied); it’s free. Everyone needs ID (a passport for visitors from abroad).\n\n"
               "Two ways to get in. (1) Book on the Imperial Household Agency website, from the 1st of the month three months ahead until three days before (up to 4 people per booking). (2) Same-day tickets, handed out in front of the Sento Palace from 8:40, first come first served (50 a day, 10 per tour, plus any unfilled booked places). Book if you want to be sure.\n\n"
               "The tour is in Japanese; free audio guides are lent in English, Chinese, French, Korean and Spanish (limited numbers). There are narrow stone bridges without rails and stepping stones, so wear good shoes. The entrance is inside the park, just west of the Seiwain gate."),
        gmaps=[gm("京都仙洞御所", "Sento Imperial Palace", 35.02168, 135.76563, "京都仙洞御所")],
        links=[link("official", "京都仙洞御所（宮内庁）", "Sento Imperial Palace (Imperial Household Agency)", KUNAI + "sento-gosho", KUNAI + "en/sento-gosho"),
               link("info", "参観の申し込み（宮内庁）", "Apply for a visit (Imperial Household Agency)", "https://sankan.kunaicho.go.jp/")],
        notices=[notice("申し込みが必要。18歳以上、全員の本人確認の書類を", "Application needed; ages 18+, ID for everyone",
                        "予約（3か月前の1日〜3日前）か、当日8:40から配る整理券（1日50人・各回10人、先着順）が要ります。月曜（祝日のときは翌日）と12月28日〜1月4日、行事のある日は休み。パスポートなどを忘れると入れません。",
                        "You need a booking (from the 1st of the month three months ahead until three days before) or a same-day ticket handed out from 8:40 (50 a day, 10 per tour, first come first served). Closed Mondays (next day if a holiday), 28 December–4 January and on days of court events. Without your passport or other ID you can’t go in.",
                        url=KUNAI + "sento-gosho/visit")],
        rows=[row("hours", "案内の開始 9:30・11:00・13:30・14:30・15:30（7・8月は原則9:30・11:00・15:30）。約60分", "Tours at 9:30, 11:00, 13:30, 14:30, 15:30 (Jul–Aug normally 9:30, 11:00, 15:30); about 60 min"),
              row("closed", "月曜（祝日のときは翌日）、12月28日〜1月4日、行事のある日", "Mondays (next day if a holiday), 28 Dec–4 Jan, and days of court events"),
              row("fee", "無料。18歳以上、要申し込み（1件4人まで）。当日の整理券は8:40から先着順・1日50人（各回10人）", "Free. Ages 18+, application needed (up to 4 people each). Same-day tickets from 8:40, first come first served, 50 a day (10 per tour)"),
              row("train", "地下鉄烏丸線 丸太町駅1番出口から歩いて約15分（宮内庁の案内）", "About 15 min on foot from exit 1 of Marutamachi station, Karasuma subway line (official access)")],
        source="宮内庁「京都仙洞御所 参観申込要領」（PDF）",
        tip=T("宮内庁の「京都仙洞御所 参観申込要領」で確認しました。受付に行く時刻は、予約の通知や整理券の案内に従ってください。" + WEBPHOTO_JA,
              "Checked in the Imperial Household Agency’s application guide for the Sento Imperial Palace. Follow your booking notice or ticket for when to report. " + WEBPHOTO_EN)),
    manga=dict(
        name=T("京都国際マンガミュージアム", "Kyoto International Manga Museum"), kind=T("ミュージアム", "Museum"), web="first",
        blurb=T("昔の小学校の校舎が、マンガの博物館に。壁いっぱいの本棚のマンガを好きなだけ読めます。雨の日の行き先に。水曜休み。",
                "An old primary school turned manga museum: take any book from the walls of shelves and read. Good for a rainy day. Closed Wednesdays."),
        lat=35.0117, lng=135.75918,
        body=T("地下鉄の烏丸御池駅の2番出口から歩いて2分。昭和のはじめに建った小学校の校舎を使った、マンガの博物館です。\n\n"
               "廊下の壁が上から下まで本棚になっていて、並んでいるマンガはどれでも手に取って読めます。天気のいい日は、校庭だった芝生に寝ころんで読む人も。外国語に訳されたマンガの棚もあるので、日本語が読めなくても楽しめます。\n\n"
               "雨の日や、夏と冬に歩き疲れたときの休み場所としても便利です。御苑と二条城のあいだの乗り換え駅なので、どちらのコースでも途中で寄れます。",
               "Two minutes’ walk from exit 2 of Karasuma-Oike subway station. The museum occupies a primary-school building from the early Showa era.\n\n"
               "The corridor walls are bookshelves from top to bottom, and you may take down and read any manga on them. On a fine day people lie reading on the lawn that was once the playground. There are shelves of manga translated into other languages too, so you don’t need to read Japanese.\n\n"
               "It’s a good place to rest on a rainy day, or when the heat or cold has worn you out. It stands at the interchange station between the park and Nijo Castle, so you can stop here on either course."),
        gmaps=[gm("京都国際マンガミュージアム", "Kyoto International Manga Museum", 35.0117, 135.75918, "京都国際マンガミュージアム")],
        links=[link("official", "京都国際マンガミュージアム 公式サイト", "Kyoto International Manga Museum (official)", "https://kyotomm.jp/", "https://kyotomm.jp/en/")],
        notices=[notice("水曜休み。最終入館は16:30", "Closed Wednesdays; last entry 16:30",
                        "水曜のほかに臨時の休みもあります。行く前に公式サイトのカレンダーを見てください。",
                        "There are occasional other closures besides Wednesdays: check the calendar on the website before you go.",
                        url="https://kyotomm.jp/")],
        rows=[row("hours", "10:00〜17:00（最終入館16:30）", "10:00–17:00 (last entry 16:30)"), row("closed", "水曜。ほかに臨時の休みもあるので公式サイトで確認を", "Wednesdays; occasional other closures, see the website"),
              row("fee", "大人1,200円、中高生400円、小学生200円", "Adults ¥1,200, ages 12–18 ¥400, 6–12 ¥200"),
              row("train", "地下鉄 烏丸御池駅2番出口から歩いて2分。丸太町からも二条城前からも1駅・220円", "2 min on foot from exit 2 of Karasuma-Oike subway station; one stop from either Marutamachi or Nijojo-mae, ¥220")],
        source="京都国際マンガミュージアムの公式サイト、乗換案内", checked=D21,
        tip=T("京都国際マンガミュージアムの公式サイトと乗換案内で確認しました。" + WEBPHOTO_JA, "Checked on the museum website and Yahoo! Transit. " + WEBPHOTO_EN)),
    nishiki=dict(
        name=T("錦市場から、夜の先斗町・木屋町へ", "Nishiki Market, then Pontocho and Kiyamachi by night"), kind=T("市場・夜の街なか", "Market & evening in town"), web="extra",
        blurb=T("「京の台所」と呼ばれる390mのアーケード。夕方は早く閉まる店が多いので17時までに。そのあとは先斗町・木屋町で晩ごはん、三条へ歩いて帰ります。",
                "“Kyoto’s kitchen”, a 390-metre covered market. Many shops close early, so come by 17:00. Then dinner in Pontocho or Kiyamachi and a walk back to Sanjo."),
        lat=35.00502, lng=135.76557,
        body=T("錦市場は、高倉通から寺町通まで東西390mのアーケードです。魚屋、漬物屋、だし巻き卵、湯葉、串にさした焼き魚や天ぷら。少しずつ買って食べるのが楽しい場所ですが、食べながら歩くのは商店街がやめてほしいと呼びかけています。買ったものは、その店の前か店の中で食べてください。イートインの席がある店も多いです。\n\n"
               "営業時間は店ごとにちがい、夕方は早く閉まる店が多いです。17時までに着くと安心です。昼どきはとても混みます。\n\n"
               "東の端は錦天満宮（にしきてんまんぐう）。繁華街の真ん中の小さな神社で、20:00まで開いています。\n\n"
               "ここから夜の街なかへ。新京極を抜けて東へ7分歩くと、鴨川と先斗町（ぽんとちょう）です。先斗町は四条通から三条通まで南北に続く、人がすれちがうのがやっとの細い路地。両側に料理屋や居酒屋、バーが並び、北へ歩けばそのまま三条に出ます。1本西の木屋町通（きやまちどおり）は高瀬川ぞいの飲み屋街で、気軽な店はこちらに多いです。晩ごはんを食べて、もう1軒寄って、21〜22時ごろまで過ごせます。閉まる時間とラストオーダーは店ごとにちがうので、入る前に表の案内で確かめてください。席料（お通し）がつく店もあります。\n\n"
               "写真1枚目は2025年11月。",
               "Nishiki Market is a covered arcade running 390 m east to west from Takakura-dori to Teramachi-dori: fishmongers, pickle shops, rolled omelette, yuba, grilled fish and tempura on skewers. Buying a little here and there is the fun of it, but the market association asks people not to eat while walking. Eat what you buy in front of the shop or inside it; many shops have a few seats.\n\n"
               "Hours differ from shop to shop and many close early in the evening. Arrive by 17:00 to be safe. It gets very crowded around lunchtime.\n\n"
               "At the east end is Nishiki Tenmangu, a small shrine in the middle of the shopping streets, open until 20:00.\n\n"
               "From here, the evening. Go through Shinkyogoku and 7 minutes east you reach the Kamo river and Pontocho, a lane barely wide enough for two people to pass, running north from Shijo-dori to Sanjo-dori. It is lined with restaurants, izakaya and bars, and if you walk north you come out at Sanjo. One street west, Kiyamachi-dori follows the Takase canal and has more casual places. Have dinner, stop somewhere for one more drink, and you can easily stay out until 21:00 or 22:00. Closing times and last orders differ, so check the sign outside before you go in. Some places add a small seating charge (otoshi).\n\n"
               "Photo 1 is from November 2025."),
        gmaps=[gm("錦市場（西の入口・高倉通）", "Nishiki Market (west end, Takakura-dori)", 35.00505, 135.7617, "錦市場 高倉通"),
               gm("錦天満宮（東の端）", "Nishiki Tenmangu (east end)", 35.00506, 135.76742, "錦天満宮"),
               gm("先斗町", "Pontocho", 35.0052, 135.7708, "先斗町 京都"),
               gm("木屋町通（三条）", "Kiyamachi-dori (at Sanjo)", 35.00885, 135.77035, "三条木屋町")],
        links=[link("official", "錦市場商店街 公式サイト", "Nishiki Market (official, Japanese)", "https://www.kyoto-nishiki.or.jp/"),
               link("info", "お願いとご案内（食べ歩きについて）", "Requests to visitors (about eating while walking, Japanese)", "https://www.kyoto-nishiki.or.jp/manner/"),
               link("info", "錦天満宮 公式サイト", "Nishiki Tenmangu (official, Japanese)", "https://nishikitenmangu.or.jp/")],
        notices=[notice("夕方は早く閉まる店が多い。食べながら歩かない", "Many shops close early; don’t eat while walking",
                        "営業時間と休みは店ごとにちがいます。17時までに着くのがおすすめ。買ったものは、その店の前か中で食べてください。",
                        "Hours and closing days differ from shop to shop. Try to arrive by 17:00. Eat what you buy in front of or inside the shop.",
                        url="https://www.kyoto-nishiki.or.jp/manner/")],
        rows=[row("hours", "錦市場の営業時間と休みは店ごとにちがいます（要確認）", "Nishiki Market: hours and closing days differ from shop to shop (please check)"),
              row("hours", "錦天満宮 8:00〜20:00", "Nishiki Tenmangu 8:00–20:00"),
              row("fee", "食べながら歩かない。買った店の前か店の中で食べる（商店街のお願い）", "Don’t eat while walking: eat in front of or inside the shop where you bought it (market’s request)"),
              row("train", "地下鉄烏丸線 四条駅・阪急 烏丸駅から歩いて約5分。三条からは寺町通か新京極を南へ歩いて約10分", "About 5 min on foot from Shijo (Karasuma subway line) or Hankyu Karasuma station; about 10 min on foot south from Sanjo along Teramachi-dori or Shinkyogoku")],
        source="錦市場商店街の公式サイト（長さ390m、食べ歩きについてのお願い）、錦天満宮の公式サイト（開門8時・閉門20時）", verified=False,
        tip=T("錦市場商店街と錦天満宮の公式サイトで確認しました。店ごとの営業時間、「17時まで」というめやす、先斗町・木屋町の店の時間は公式の情報では確認できていません。歩く時間は OpenStreetMap で測った目安です。アーケードの写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
              "Checked on the websites of the market association and Nishiki Tenmangu. Individual shop hours, the “by 17:00” rule of thumb and the hours of places in Pontocho and Kiyamachi could not be confirmed from official sources. Walking times are estimates measured on OpenStreetMap. The arcade photos are from Wikimedia Commons (author and license shown on each photo).")),
)

HEAD = {'nijojo': ('二条城（にじょうじょう）', 'Nijo Castle'), 'shinsenen': ('神泉苑（しんせんえん）', 'Shinsen-en'), 'seimei': ('晴明神社（せいめいじんじゃ）', 'Seimei Shrine'), 'gyoen': ('京都御苑（きょうとぎょえん）', 'Kyoto Imperial Palace Park (Kyoto Gyoen)'), 'gosho': ('京都御所（きょうとごしょ）', 'Kyoto Imperial Palace (Kyoto Gosho)'), 'kitagyoen': ('京都御苑の北側', 'North side of the park'), 'nashinoki': ('梨木神社（なしのきじんじゃ）', 'Nashinoki Shrine'), 'sento': ('京都仙洞御所（きょうとせんとうごしょ）', 'Sento Imperial Palace (Kyoto Sento Gosho)'), 'manga': ('京都国際マンガミュージアム', 'Kyoto International Manga Museum'), 'nishiki': ('錦市場（にしきいちば）と夜の街なか', 'Nishiki Market and the evening in town')}
VIS, ARR = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time")
SEC_SIDE = T("寄り道", "Side stops")

# ---------------------------------------------------------------------------------------------------------
# コースごとの並び順・めやすの時間・行き方
# order の要素: (id, ラベル, 時間ja, 時間en, そのコースでの行き方)
# ---------------------------------------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="gosho.json",
        note="「9〜10時に出発」コース。三条のあたりを9:45に出て寺町通を北へ歩く→梨木神社10:15→御苑の北側→京都御所11:25→檜垣でお昼12:25→梅林・蛤御門→丸太町14:00発（地下鉄）→二条城前14:12着→二条城14:20〜16:20（入城16:00まで）→神泉苑→二条城前16:53発→京都市役所前16:57着→錦天満宮・錦市場→先斗町・木屋町で晩ごはん（21〜22時ごろまで）。二条城を、昼の団体が多い時間のあとに回す。仙洞御所（11:00の回）・晴明神社・マンガミュージアムは寄り道。",
        order=[
            ("nashinoki", VIS, "10:15〜10:35（三条のあたりを9:45に出発）", "10:15–10:35 (leave the Sanjo area at 9:45)",
             T("このコースのスタートです。三条のあたりから、寺町通（てらまちどおり）を北へまっすぐ歩いて約30分（約1.8km）。地下鉄の京都市役所前駅の上から北は、古道具屋や紙の店、お茶屋が並ぶ静かな通りです。途中の一保堂茶舗（いっぽどうちゃほ、寺町二条）は10:00に開くので、帰りのおみやげの下見に。丸太町通を渡ると右手に御苑の石垣が見え、そのまま北へ5分ほどで清和院御門、門の向かいが梨木神社です。\n\n"
               "歩きたくない日は、京都市役所前から地下鉄で丸太町へ（烏丸御池で乗り換え、10〜12分・220円）。その場合は御苑の南西から入り、5番の梅林・蛤御門を先に見て、京都御所、北側、梨木神社の順に回ってください。\n\n"
               "お参りして染井の水を飲んだら、清和院御門から御苑に入り、御所の東の塀に沿って北へ歩きます。朔平門まで約10分です。",
               "The start of this course. From the Sanjo area walk straight north up Teramachi-dori for about 30 minutes (about 1.8 km). North of Kyoto Shiyakusho-mae subway station it is a quiet street of antique dealers, paper shops and tea merchants. Ippodo Tea (at Teramachi Nijo) opens at 10:00: have a look now for presents to buy later. Cross Marutamachi-dori and the stone wall of the park appears on your right; 5 minutes further north is the Seiwain gate, and the shrine is opposite it.\n\n"
               "Not in the mood to walk? Take the subway from Kyoto Shiyakusho-mae to Marutamachi (change at Karasuma-Oike; 10–12 minutes, ¥220). In that case enter the park at its south-west corner and see No. 5 (plum grove and Hamaguri gate) first, then the Palace, the north side and Nashinoki Shrine.\n\n"
               "After the shrine and a drink of Somei water, enter the park by the Seiwain gate and walk north along the east wall of the Palace: about 10 minutes to the Sakuheimon gate.")),
            ("sento", VIS, "11:00〜12:00（11:00の回。入る日は、この先を45分ずつ遅らせます）", "11:00–12:00 (the 11:00 tour; if you go, shift everything after by 45 minutes)",
             T("このコースでは寄り道です。梨木神社のすぐ西、清和院御門を入って左（南）へ歩いて3分。予約するなら11:00の回が合います。終わったら北側（3番）は短く切り上げて京都御所へ（12:15ごろ入場）、お昼は13:10ごろ、二条城には15時ごろに着きます。\n\n"
               "予約がない日は、当日の整理券を。8:40に配り始めるので、8:15ごろ三条を出て寺町通を歩き、先に整理券をもらってから梨木神社と御苑の北側を回って11:00に戻ります。",
               "A side stop on this course. Just west of Nashinoki Shrine: go in at the Seiwain gate and walk 3 minutes left (south). If you book, the 11:00 tour fits. Afterwards keep the north side (No. 3) short and go on to the Palace (in at about 12:15), have lunch at about 13:10, and you reach Nijo Castle at about 15:00.\n\n"
               "No booking? Try for a same-day ticket. They are handed out from 8:40, so leave Sanjo at about 8:15, walk up Teramachi-dori, get your ticket first, then see Nashinoki Shrine and the north side of the park and come back for 11:00.")),
            ("kitagyoen", VIS, "10:45〜11:20", "10:45–11:20",
             T("梨木神社から御所の東の塀に沿って北へ歩いて約10分で、北の門の朔平門。そこから西へ、近衞邸跡、乾御門のあたりのもみじとイチョウを見て回ります。歩き疲れたら近衞邸跡のそばの休憩所へ（月曜休み）。\n\n"
               "見終わったら、御所の西の塀に沿って南へ歩いて約5分で、京都御所の入口・清所門です。",
               "From Nashinoki Shrine walk about 10 minutes north along the east wall of the Palace to its north gate, the Sakuheimon. From there go west: the Konoe site, then the maples and ginkgo near the Inui gate. If your feet need a rest, the rest house by the Konoe site is right there (closed Mondays).\n\n"
               "Then walk about 5 minutes south along the west wall of the Palace to Seishomon, the entrance to the Palace.")),
            ("gosho", VIS, "11:25〜12:20、そのあと檜垣でお昼（12:25〜13:15）", "11:25–12:20, then lunch at Higaki (12:25–13:15)",
             T("11:25ごろ清所門から入ります。順路は約50分。出たら、西へ歩いて3分の中立売休憩所の「檜垣」でお昼にします。12時台は混むことがあるので、先にお昼にして（11:25〜）御所を12:20から見る順でもかまいません。冬（10〜2月）は15:20までに入ってください。",
               "Go in by the Seishomon gate at about 11:25. The route takes about 50 minutes. When you come out, have lunch at Higaki in the Nakadachiuri rest house, 3 minutes’ walk west. It can be busy between 12:00 and 13:00, so you could equally eat first (from 11:25) and see the Palace from 12:20. In winter (October to February) be inside by 15:20.")),
            ("gyoen", VIS, "13:20〜13:50", "13:20–13:50",
             T("お昼のあと、中立売休憩所から南へ歩いてすぐが蛤御門。門の弾の跡を見たら、梅林、桃林、出水の小川と、御苑の西側を南へ下ります。南西の角から丸太町通に出て、西へ歩いて約5分で地下鉄の丸太町駅（1番出口）です。\n\n"
               "丸太町14:00発の地下鉄に乗り、次の烏丸御池で東西線（太秦天神川行き）に乗り換えて、二条城前に14:12に着きます（220円。1本前は13:53発→14:04着。土曜の時刻で、ほかの時間も数分おき）。",
               "After lunch the Hamaguri gate is just south of the Nakadachiuri rest house. Look for the bullet marks, then walk down the west side of the park: plum grove, peach grove, Demizu stream. Leave by the south-west corner onto Marutamachi-dori; Marutamachi subway station (exit 1) is about 5 minutes’ walk west.\n\n"
               "Take the 14:00 subway from Marutamachi, change at the next stop, Karasuma-Oike, to the Tozai line (for Uzumasa-Tenjingawa) and you reach Nijojo-mae at 14:12 (¥220; the train before is 13:53 → 14:04. Saturday times; trains run every few minutes).")),
            ("seimei", VIS, "13:40〜14:00（寄る日は、梅林・桃林を短くします）", "13:40–14:00 (if you go, shorten the plum and peach groves)",
             T("このコースでは寄り道です。蛤御門を見たら、1つ北の中立売御門から御苑を出て、中立売通を西へまっすぐ歩いて約15分（約1.1km）。\n\n"
               "お参りのあと二条城へは、堀川通を南へ歩いて約25分（約1.5km）。「一条戻橋・晴明神社前」から市バス9・12系統に乗れば「二条城前」まで行けます（230円。時刻は要確認）。",
               "A side stop on this course. After the Hamaguri gate, leave the park by the next gate north, the Nakadachiuri gate, and walk straight west along Nakadachiuri-dori for about 15 minutes (about 1.1 km).\n\n"
               "From the shrine to Nijo Castle, walk about 25 minutes (about 1.5 km) south down Horikawa-dori, or take city bus 9 or 12 from “Ichijo-modoribashi / Seimei-jinja-mae” to “Nijojo-mae” (¥230; times: please check).")),
            ("manga", VIS, "13:50〜14:40（寄る日は、二条城に15時ごろ）", "13:50–14:40 (if you go, you reach Nijo Castle at about 15:00)",
             T("このコースでは寄り道です。丸太町から地下鉄で1駅の烏丸御池で降りて、2番出口から歩いて2分。ここに50分いると、二条城に着くのは15時ごろになります。二の丸御殿の受付は16:10までなので、15:00までにはここを出てください。雨の日は、御苑を短くしてここで長めに休むのもいい使い方です。",
               "A side stop on this course. Get off the subway at Karasuma-Oike, one stop from Marutamachi, and walk 2 minutes from exit 2. Spend 50 minutes here and you reach Nijo Castle at about 15:00. Entry to the Ninomaru Palace ends at 16:10, so leave here by 15:00 at the latest. On a rainy day, cutting the park short and resting longer here works well.")),
            ("nijojo", VIS, "14:20〜16:20（入城は16:00まで）", "14:20–16:20 (last entry 16:00)",
             T("二条城前駅の1番出口から東大手門まで歩いて約5分。昼前後は団体が多い場所なので、このコースでは午後おそくに回します。着いたら、まず二の丸御殿へ（受付は16:10まで）。御殿を出てから庭と本丸、天守閣跡へ。17:00に閉まるので、16:20ごろに出口へ向かえば十分です。\n\n"
               "本丸御殿を予約するなら、15:00ごろの枠が合います。",
               "From exit 1 of Nijojo-mae station it’s about 5 minutes on foot to the East Gate. Tour groups tend to come around midday, so this course saves the castle for later in the afternoon. Go to the Ninomaru Palace first (entry until 16:10), then the garden, the Honmaru and the keep base. The castle closes at 17:00; heading for the exit at about 16:20 is plenty.\n\n"
               "If you book the Honmaru Palace, a slot at about 15:00 fits.")),
            ("shinsenen", VIS, "16:25〜16:40", "16:25–16:40",
             T("二条城の東大手門を出て、堀に沿って南へ、押小路通を西へ歩いて約7分。20:00まで開いているので、急がなくて大丈夫です。\n\n"
               "帰りは二条城前駅から地下鉄東西線で京都市役所前へ4分・220円（16:53発→16:57着、16:56発→17:00着。数分おき）。三条京阪までは6分です。",
               "Leave the castle by the East Gate, follow the moat south and walk west along Oshikoji-dori: about 7 minutes. It is open until 20:00, so there is no hurry.\n\n"
               "To go back, take the Tozai subway line from Nijojo-mae to Kyoto Shiyakusho-mae: 4 minutes, ¥220 (16:53 → 16:57, 16:56 → 17:00; every few minutes). Sanjo Keihan is 6 minutes.")),
            ("nishiki", VIS, "17:15〜（錦市場は18時ごろまで、そのあと晩ごはん。21〜22時ごろまで）", "from 17:15 (the market until about 18:00, then dinner; out until 21:00–22:00)",
             T("京都市役所前駅から寺町通のアーケードを南へ歩いて約12分で、錦天満宮と錦市場の東の端です。このコースでは着くのが17時を過ぎるので、閉まり始めている店もあります。開いている店で少し食べて、あとは晩ごはんに回してください。錦市場をゆっくり見たい人は「開城に合わせる」コースで。\n\n"
               "18時ごろ、新京極を抜けて先斗町・木屋町へ。晩ごはんのあと北へ歩けば、そのまま三条です。",
               "From Kyoto Shiyakusho-mae station walk about 12 minutes south down the Teramachi arcade to Nishiki Tenmangu and the east end of Nishiki Market. On this course you arrive after 17:00, when some shops are already closing. Eat a little where it is still open and leave the rest for dinner. If the market matters to you, use the “Castle at opening” course.\n\n"
               "At about 18:00 go through Shinkyogoku to Pontocho and Kiyamachi. After dinner, walk north and you are back at Sanjo.")),
        ],
        sections=[dict(first="nashinoki", last="kitagyoen", area=T("寺町通〜京都御苑の東と北", "Teramachi-dori to the east and north of the park"), title=T("歩いて御苑へ。静かな側から入る", "Walk to the park and enter by its quiet side")),
                  dict(first="gosho", last="manga", area=T("京都御所と御苑の西側", "The Palace and the west side of the park"), title=T("御所を見て、休憩所でお昼", "The Palace, then lunch at the rest house")),
                  dict(first="nijojo", last="shinsenen", area=T("二条城", "Nijo Castle"), title=T("団体が減る午後の城へ", "The castle in the later afternoon")),
                  dict(first="nishiki", last="nishiki", area=T("錦市場〜先斗町・木屋町", "Nishiki Market to Pontocho & Kiyamachi"), title=T("街なかへ戻って夜まで", "Back in town for the evening"))],
        default=["nashinoki", "kitagyoen", "gosho", "gyoen", "nijojo", "shinsenen", "nishiki"],
        extra_notices={"nijojo": [notice("このコースは14:20ごろ着。入城は16:00まで", "This course arrives at about 14:20; last entry is 16:00",
                                         "二の丸御殿の受付は16:10までです。寄り道を足した日も、15:30までには東大手門に着いてください。",
                                         "Entry to the Ninomaru Palace ends at 16:10. Even if you add side stops, be at the East Gate by 15:30.")]},
        hints=[("sento", dict(any=["sento"]), None, None,
                "仙洞御所は申し込みが要ります（18歳以上・本人確認の書類）。このコースは11:00の回が合います。当日の整理券は8:40から配るので、ねらう日は8:15ごろ出発に。",
                "The Sento Palace needs an application (ages 18+, bring ID). The 11:00 tour fits this course. Same-day tickets are handed out from 8:40, so leave at about 8:15 if you want one."),
               ("manga", dict(any=["manga"], andAny=["seimei", "sento"]), None, None,
                "寄り道を2つ以上足すと、二条城の入城（16:00まで）に間に合わなくなります。寄り道は1つにしてください。",
                "With two or more side stops you won’t make last entry at Nijo Castle (16:00). Keep it to one."),
               ("gyoen", dict(any=["gyoen", "gosho"], none=["nashinoki", "kitagyoen"]), None, None,
                "梨木神社と北側に寄らない日は、京都市役所前から地下鉄で丸太町へ（烏丸御池で乗り換え、10〜12分・220円）。御所だけなら、1つ先の今出川駅が近いです（3番出口から歩いて約5分）。",
                "Skipping Nashinoki Shrine and the north side? Take the subway from Kyoto Shiyakusho-mae to Marutamachi (change at Karasuma-Oike; 10–12 min, ¥220). For the Palace alone, the next stop, Imadegawa, is closer (about 5 min on foot from exit 3)."),
               ("nijojo", dict(any=["nijojo"], none=["nashinoki", "kitagyoen", "gosho", "gyoen", "sento"]), None, None,
                "二条城だけの日は、開城の8:45か、14時すぎに。京都市役所前から地下鉄東西線で4分・220円です。",
                "A Nijo Castle-only day? Go at the 8:45 opening or after 14:00. It is 4 minutes (¥220) on the Tozai subway line from Kyoto Shiyakusho-mae.")]),
    dict(
        id="early", file="gosho-early.json",
        note="「開城に合わせる」コース。三条のあたりを8:10ごろ出発、京都市役所前8:24発（地下鉄東西線）→二条城前8:28着、二条城8:45〜10:30→神泉苑→二条城前10:58発→（烏丸御池で乗り換え）→丸太町11:10着→御苑の西側（梅林・蛤御門）→京都御所11:55→檜垣でお昼12:55→御苑の北側→梨木神社14:35→寺町通を南へ歩く（一保堂茶舗）→錦市場16:10→錦天満宮→先斗町・木屋町で晩ごはん（21〜22時ごろまで）。晴明神社・仙洞御所（15:30の回）・マンガミュージアムは寄り道。",
        order=[
            ("nijojo", VIS, "8:45〜10:30（三条のあたりを8:10ごろ出発）", "8:45–10:30 (leave the Sanjo area at about 8:10)",
             T("このコースのスタートです。地下鉄東西線の京都市役所前駅から太秦天神川（うずまさてんじんがわ）行きに乗って2駅、4分・220円。8:24発に乗ると二条城前に8:28に着きます（1本前は8:17発、次は8:28発。土曜の時刻で、平日も数分おき）。三条京阪駅からなら8:22発で同じ電車です。1番出口から東大手門まで歩いて約5分。8:35ごろ着いて、券売所に並びましょう。\n\n"
               "開城の8:45に入ると、団体が増える前に二の丸御殿を静かに見られます。入ったらまっすぐ二の丸御殿へ。庭と本丸はそのあとに。\n\n"
               "本丸御殿を予約するなら、9:30〜10:00の枠が合います。",
               "The start of this course. From Kyoto Shiyakusho-mae station take the Tozai subway line (for Uzumasa-Tenjingawa) two stops: 4 minutes, ¥220. The 8:24 reaches Nijojo-mae at 8:28 (the train before leaves at 8:17, the next at 8:28. Saturday times; every few minutes on weekdays too). From Sanjo Keihan station the same train leaves at 8:22. From exit 1 it’s about 5 minutes on foot to the East Gate. Arrive at about 8:35 and join the ticket queue.\n\n"
               "Go in at the 8:45 opening and you see the Ninomaru Palace quietly, before the tour groups build up. Head straight for the palace; leave the gardens and the Honmaru for afterwards.\n\n"
               "If you book the Honmaru Palace, a slot between 9:30 and 10:00 fits.")),
            ("shinsenen", VIS, "10:40〜10:55", "10:40–10:55",
             T("二条城の東大手門を出て、堀に沿って南へ、押小路通を西へ歩いて約7分。見終わったら二条城前駅まで歩いて約4分です。\n\n"
               "二条城前10:58発の地下鉄（東西線）に乗り、次の烏丸御池で烏丸線（国際会館行き）に乗り換えて1駅、丸太町に11:10に着きます（220円。次は11:06発→11:16着）。",
               "Leave the castle by the East Gate, follow the moat south and walk west along Oshikoji-dori: about 7 minutes. Afterwards it’s about 4 minutes on foot to Nijojo-mae station.\n\n"
               "Take the 10:58 subway (Tozai line) from Nijojo-mae, change at the next stop, Karasuma-Oike, to the Karasuma line (for Kokusaikaikan) and go one stop to Marutamachi, arriving 11:10 (¥220; the next is 11:06 → 11:16).")),
            ("seimei", VIS, "11:10〜11:30（寄る日は、梅林・桃林を御所のあとに）", "11:10–11:30 (if you go, see the plum and peach groves after the Palace)",
             T("このコースでは寄り道です。二条城前のバス停から堀川通を北へ、市バス9・12系統で「一条戻橋・晴明神社前」へ（230円。時刻は要確認）。歩くと約25分です。\n\n"
               "ここから京都御苑へは、中立売通を東へまっすぐ歩いて約15分（約1.1km）で中立売御門。そのまま進むと京都御所の入口の清所門です。4番の梅林・桃林と蛤御門は、御所とお昼のあとに回ってください。",
               "A side stop on this course. From the Nijojo-mae bus stop take city bus 9 or 12 north along Horikawa-dori to “Ichijo-modoribashi / Seimei-jinja-mae” (¥230; times: please check). On foot it takes about 25 minutes.\n\n"
               "From here walk straight east along Nakadachiuri-dori for about 15 minutes (1.1 km) to the Nakadachiuri gate of the Imperial Palace Park; keep going and you reach the Seishomon gate, the entrance to the Palace. See the plum and peach groves and the Hamaguri gate (No. 4) after the Palace and lunch.")),
            ("gyoen", VIS, "11:20〜11:50", "11:20–11:50",
             T("丸太町駅の1番出口から北へ歩いて約5分で、御苑の南西の角です。出水の小川、桃林、梅林と、西側を北へ歩いて蛤御門へ。門を見たら、北東へ約6分で京都御所の入口・清所門です。",
               "From exit 1 of Marutamachi station it’s about 5 minutes’ walk north to the south-west corner of the park. Walk up the west side: Demizu stream, peach grove, plum grove, then the Hamaguri gate. From the gate it’s about 6 minutes north-east to Seishomon, the entrance to the Palace.")),
            ("gosho", VIS, "11:55〜12:50、そのあと檜垣でお昼（12:55〜13:45）", "11:55–12:50, then lunch at Higaki (12:55–13:45)",
             T("11:55ごろ清所門から入ります。順路は約50分。出たら、西へ歩いて3分の中立売休憩所の「檜垣」でお昼にします。朝8時から動いているので、ここでしっかり休んでください。おなかがすいていたら、先にお昼にしてから（11:55〜）御所に入る順でもかまいません。冬でも15:20までに入れば大丈夫です。",
               "Go in by the Seishomon gate at about 11:55. The route takes about 50 minutes. When you come out, have lunch at Higaki in the Nakadachiuri rest house, 3 minutes’ walk west. You have been on the move since 8:00, so take a proper break. If you are hungry, eat first (from 11:55) and see the Palace afterwards: even in winter you only need to be inside by 15:20.")),
            ("kitagyoen", VIS, "13:50〜14:25", "13:50–14:25",
             T("中立売休憩所から御所の西の塀に沿って北へ歩いて約7分で乾御門のあたり。もみじとイチョウ、その東の近衞邸跡を見て、北の門の朔平門へ。甘いものが欲しくなったら近衞邸跡のそばの休憩所へ（月曜休み）。\n\n"
               "朔平門から御所の東の塀に沿って南へ歩いて約10分で、清和院御門と梨木神社です。",
               "From the Nakadachiuri rest house walk about 7 minutes north along the west wall of the Palace to the Inui gate area. See the maples and ginkgo, then the Konoe site to the east, and go on to the north gate, the Sakuheimon. Want something sweet? The rest house by the Konoe site is right there (closed Mondays).\n\n"
               "From the Sakuheimon walk about 10 minutes south along the east wall of the Palace to the Seiwain gate and Nashinoki Shrine.")),
            ("nashinoki", VIS, "14:35〜14:55", "14:35–14:55",
             T("清和院御門を出て、向かいが梨木神社です。門は16:30に閉まります。\n\n"
               "ここからは地下鉄に乗らず、寺町通（てらまちどおり）を南へ歩いて街なかへ戻ります。古道具屋や紙の店が並ぶ静かな通りで、三条まで約25分（約1.7km）。途中、歩いて約15分の寺町二条にある一保堂茶舗（いっぽどうちゃほ）は、日本茶の店。喫茶室「嘉木（かぼく）」でお茶を飲んでひと休みできます（10:00〜17:00、ラストオーダー16:30、第2水曜休み）。軽くて割れないお茶は、おみやげにも向いています。",
               "Leave the park by the Seiwain gate; the shrine is opposite. Its gates close at 16:30.\n\n"
               "From here, skip the subway and walk back into town down Teramachi-dori, a quiet street of antique dealers and paper shops: about 25 minutes (1.7 km) to Sanjo. On the way, about 15 minutes’ walk at Teramachi Nijo, is Ippodo Tea, a Japanese tea shop. You can sit down for tea in its Kaboku tearoom (10:00–17:00, last order 16:30; closed on the second Wednesday of the month). Tea is light and unbreakable, so it also makes a good present.")),
            ("sento", VIS, "15:30〜16:30（15:30の回。入る日は、錦市場をやめて晩ごはんへ）", "15:30–16:30 (the 15:30 tour; if you go, skip Nishiki Market and go on to dinner)",
             T("このコースでは寄り道です。梨木神社のすぐ西、清和院御門を入って左（南）へ歩いて3分。このコースで予約するなら15:30の回が合います（7・8月もある回です）。14:30の回にするなら、御苑の北側（6番）を短くして梨木神社を先に。\n\n"
               "当日の整理券は8:40から配るので、二条城の開城には間に合いません。整理券をねらう日は「9〜10時に出発」コースの順で回ってください。",
               "A side stop on this course. Just west of Nashinoki Shrine: go in at the Seiwain gate and walk 3 minutes left (south). If you book for this course, the 15:30 tour fits (it also runs in July and August). For the 14:30 tour, shorten the north side of the park (No. 6) and see Nashinoki Shrine first.\n\n"
               "Same-day tickets are handed out from 8:40, which clashes with the castle opening. If you want one, follow the order of the “Leave at 9–10” course instead.")),
            ("manga", VIS, "14:50〜15:50（御苑の北側と梨木神社のかわりに）", "14:50–15:50 (instead of the north side of the park and Nashinoki Shrine)",
             T("このコースでは寄り道です。お昼のあと蛤御門から丸太町駅へ歩き（約15分）、地下鉄で1駅の烏丸御池へ。2番出口から歩いて2分です。雨の日や寒い日は、御苑の北側と梨木神社のかわりにここへ。出たら、烏丸通を南へ歩いて約13分で錦市場の西の入口です。",
               "A side stop on this course. After lunch walk from the Hamaguri gate to Marutamachi station (about 15 minutes) and take the subway one stop to Karasuma-Oike; the museum is 2 minutes from exit 2. On a wet or cold day, come here instead of the north side of the park and Nashinoki Shrine. Afterwards the west entrance of Nishiki Market is about 13 minutes’ walk south down Karasuma-dori.")),
            ("nishiki", VIS, "16:10〜17:00、そのあと晩ごはん（21〜22時ごろまで）", "16:10–17:00, then dinner (out until 21:00–22:00)",
             T("一保堂から寺町通をそのまま南へ。御池通を渡るとアーケードになり、三条通を過ぎて約20分で、錦天満宮と錦市場の東の端に着きます。市場を西へ歩いて、気になる店で少しずつ。17時ごろ、東の端の錦天満宮へ戻ります。\n\n"
               "そのあと新京極を抜けて鴨川へ。日が暮れるころの四条大橋や河原を少し歩いて、先斗町・木屋町で晩ごはんにします。朝が早かった日なので、18時ごろから食べ始めると楽です。食後に北へ歩けば、そのまま三条です。",
               "From Ippodo keep going south down Teramachi-dori. It becomes a covered arcade once you cross Oike-dori; pass Sanjo-dori and in about 20 minutes you reach Nishiki Tenmangu and the east end of Nishiki Market. Walk west through the market, trying a little here and there. Come back to Nishiki Tenmangu at the east end at about 17:00.\n\n"
               "Then go through Shinkyogoku to the Kamo river. Walk a little by Shijo bridge and the riverbank as it gets dark, and have dinner in Pontocho or Kiyamachi. After an early start, sitting down to eat at about 18:00 is comfortable. Afterwards walk north and you are back at Sanjo.")),
        ],
        sections=[dict(first="nijojo", last="seimei", area=T("二条城のまわり", "Around Nijo Castle"), title=T("開城と同時に将軍の城へ", "The shogun’s castle at opening time")),
                  dict(first="gyoen", last="sento", area=T("京都御苑", "Imperial Palace Park"), title=T("御所と、それを囲む広い公園", "The Palace and the park around it")),
                  dict(first="manga", last="nishiki", area=T("寺町通〜錦市場〜先斗町・木屋町", "Teramachi-dori, Nishiki Market, Pontocho & Kiyamachi"), title=T("歩いて街なかへ戻って夜まで", "Walk back into town for the evening"))],
        default=["nijojo", "shinsenen", "gyoen", "gosho", "kitagyoen", "nashinoki", "nishiki"],
        extra_notices={},
        hints=[("sento", dict(any=["sento"]), None, None,
                "仙洞御所は申し込みが要ります（18歳以上・本人確認の書類）。このコースは15:30の回が合います。終わるのが16:30なので、錦市場はやめて、寺町通を歩いて晩ごはんへ。",
                "The Sento Palace needs an application (ages 18+, bring ID). The 15:30 tour fits this course. It ends at 16:30, so skip Nishiki Market and walk down Teramachi-dori to dinner."),
               ("manga", dict(any=["manga"], andAny=["sento", "kitagyoen", "nashinoki"]), None, None,
                "マンガミュージアム（最終入館16:30）は、御苑の北側・梨木神社・仙洞御所とは方向が逆です。どちらかにすると、錦市場に17時前に着けます。",
                "The Manga Museum (last entry 16:30) is in the opposite direction from the north side of the park, Nashinoki Shrine and the Sento Palace. Choose one or the other to reach Nishiki Market before 17:00."),
               ("gyoen", dict(any=["gyoen", "gosho"], none=["nijojo", "shinsenen", "seimei"]), None, None,
                "二条城に寄らない日は、「9〜10時に出発」コースの順（寺町通を歩いて御苑の東から）が歩きやすいです。地下鉄なら京都市役所前から丸太町へ10〜12分・220円。",
                "Skipping Nijo Castle? The order of the “Leave at 9–10” course (on foot up Teramachi-dori, entering the park from the east) is easier. By subway, Kyoto Shiyakusho-mae to Marutamachi takes 10–12 minutes, ¥220."),
               ("nishiki", dict(any=["nishiki"], none=["nashinoki", "kitagyoen", "sento", "manga"]), None, None,
                "御苑の東と北に寄らない日は、お昼のあと丸太町駅から地下鉄で四条へ（3分・220円）。駅から錦市場まで歩いて約5分で、14時台に着けます。",
                "Skipping the east and north of the park? After lunch take the subway from Marutamachi to Shijo (3 min, ¥220); the market is about 5 minutes’ walk from the station and you arrive before 15:00.")]),
]

NOTE_HEAD = "京都の中心：二条城と京都御所のルート（gosho/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（gosho.json＝9〜10時に出発、gosho-early.json＝開城に合わせる）。出発は京都の中心・三条のあたり（地下鉄 京都市役所前駅）を想定。このファイル："
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（御苑：2015年3月・2016年2月・2017年1月の雪・2017年11月の紅葉・2019年1月と3月・2020年4月・2023年4月、京都御所：2024年1月6日と11月6日、梨木神社：2026年5月18日、二条城の夜：2016年8月と2017年4月、錦市場：2025年11月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "二条城の昼・神泉苑・晴明神社・蛤御門・仙洞御所・マンガミュージアム・錦市場のアーケードの写真は Wikimedia Commons（photos の要素が {file, credit}。一覧は scripts/gosho_web_photos.json）。"
             "info.source は確認した出典、info.checked は確認日、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。このファイルは scripts/build_gosho_data.py で作る（直接直さない）。")


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    assert set(NO) == set(BASE), set(BASE) ^ set(NO)
    spots = []
    for sid, (lj, le), tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        b["info"] = info(b.pop("rows"), b.pop("source"), tip=b.pop("tip"), verified=b.pop("verified", True), checked=b.pop("checked", D22))
        where = b.pop("web")
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        hj, he = HEAD[sid]
        out["text"] = T(hj + "\n\n" + go["ja"] + "\n\n" + body["ja"] + f"\n\n{lj}：{tj}", he + "\n\n" + go["en"] + "\n\n" + body["en"] + f"\n\n{le}: {te}")
        out["photos"] = photos(sid, where)
        out["notices"] = c.get("extra_notices", {}).get(sid, []) + out.get("notices", [])
        spots.append(out)
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": [{"first": NO[s["first"]], "last": NO[s["last"]], "area": s["area"], "title": s["title"]} for s in c["sections"]],
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は時間割どおりに1日で回れる7か所。それ以外（晴明神社・仙洞御所・マンガミュージアム）は寄り道で、足したときの回り方は各スポットの文章と hints。全員共通の場所（駅など）はない。",
                 "defaultMode": "pick",
                 "picks": [NO[x[0]] for x in order],
                 "defaultPicks": [NO[i] for i in c["default"]],
                 "auto": {},
                 "hints": [{"spot": NO[sid], "rule": rule(r), "from": frm, "to": to, "text": T(ja, en)} for sid, r, frm, to, ja, en in c["hints"]]},
        "photoBase": f"../images/{MAP_ID}/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


for c in COURSES:
    build(c)
