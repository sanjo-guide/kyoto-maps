#!/usr/bin/env python3
"""友ヶ島・加太（大阪の梅田〜難波のホテルから日帰り）のデータを書き出す。行きの船ごとに1ファイル。

使い方: python3 scripts/build_tomogashima_data.py   （そのあと python3 scripts/sync_tomogashima.py）
- data/routes/tomogashima.json        … 「11:00の船」（late。なんば8:14発→加太→淡嶋神社→11:00の船→島で5時間→16:30の船→夜はなんば）
- data/routes/tomogashima-early.json  … 「9:00の船」（early。なんば6:38発→9:00の船→島で4時間→13:30の船→加太でお昼・淡嶋神社・温泉→夜はなんば）
- 起点は大阪の梅田〜難波のあたりのホテル（2026-11-22 オーナーの指示。京都の三条のあたりから来る人の電車は補足として書く）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの行き方（pre）→ 共通の説明（body）→ コースごとの次へ（post）→ おすすめ訪問時間」の順に組み立てる
- 確認した出典（2026-11-22）:
  - 船：友ヶ島汽船の公式サイト（時刻表・運航日・整理券・運賃は画像。運航連絡はトップページ）。支払い方法と整理券を配りはじめる時刻は書かれていない（要確認。2026-11-24 に和歌山市のページも含めて再確認）
  - 運航連絡が出る時刻は公式に書かれていない。2026-11-24 に公式サイトの記事の日時（wp-json）を見て、8月中旬〜11月はどの日も前の晩か当日6:30までに出ていたことを確認して書いた
  - 「朝8時以降なら電話で」は出どころが見つからなかったので 2026-11-24 に消した（和歌山市のページは「当日、友ヶ島汽船に問い合わせ」だけ）
  - 2026-11-24 の調べ直し：いなさ・ひいなの湯・加太海月・休暇村・最終電車（RECHECKED のスポットの source に直接のURL）
  - 島の中：和歌山市の公式サイト「友ヶ島」（トイレ4か所、飲み物は野奈浦広場のまわりだけ、水道なし、ごみ持ち帰り、名所探訪コース3.3km、深蛇池・虎島は見学不可）
  - 電車：乗換案内（Yahoo!路線情報）2026-11-26（木）と 11-28（土）のダイヤ
  - 淡嶋神社：kada.jp/awashima（参拝9〜17時）。活魚料理いなさ：inasa.net。ひいなの湯：hiina.com。休暇村紀州加太：qkamura.or.jp/kada。加太海月：kada-kaigetsu.com
  - 日の入り：国立天文台 暦計算室（和歌山）
- 店名を出しているのは、公式サイトで営業時間を確かめた店だけ（いなさ、ひいなの湯、休暇村紀州加太、加太海月、島のらぴゅカフェ）。行ったとは書いていない
- 写真は images/tomogashima/<スポットのid>-<番号>.jpg を番号の順に全部使う（2026-11-22 の作り直しでは足していない）
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/tomogashima"
CHECKED = "2026-11-22"
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


def notice(hja, hen, ja, en, url=None):
    d = {"head": T(hja, hen), "text": T(ja, en)}
    if url:
        d["url"] = url
    return d


def info(rows, tip=None, verified=True, cash=False, source=None, checked=None):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked or CHECKED, "source": source or []}
    if not verified:
        d["verified"] = False
    return d


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


KISEN_URL = "https://tomogashimakisen.com/main/"
CITY_URL = "https://www.city.wakayama.wakayama.jp/kankou/kankouspot/1027585/index.html"
KISEN = link("official", "友ヶ島汽船 公式サイト（今日の運航連絡・時刻・運賃）", "Tomogashima Kisen ferry: today’s operating notice, times, fares (official, Japanese)", KISEN_URL)
CITY = link("info", "和歌山市「友ヶ島」（島の地図・通れない道・注意）", "Wakayama City: Tomogashima (island map, closed trails, cautions; Japanese)", CITY_URL)
PLANNER = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
MEDETAI = link("timetable", "めでたいでんしゃ（南海電鉄・運行ダイヤ）", "Medetai Densha: which train runs when (Nankai, Japanese)", "https://www.nankai.co.jp/kada/medetai.html")
OSAKA_MAP = link("info", "夜のなんば：大阪マップ（法善寺横丁・道頓堀）", "Evening in Namba: the Osaka map (Hozenji Yokocho, Dotonbori)", "../osaka/")
RECHECKED = "2026-11-24"   # 「要確認」の調べ直しをした日（港・淡嶋神社・加太駅のスポット）
SRC_KISEN = ("友ヶ島汽船 公式サイト（運航時刻・運航日・当日乗船整理券・旅客運賃・運航連絡。2026-11-24 再確認："
             "https://tomogashimakisen.com/main/ ・ https://tomogashimakisen.com/main/%e9%81%8b%e8%88%aa%e6%99%82%e5%88%bb-copy ・ "
             "https://tomogashimakisen.com/main/%e6%97%85%e5%ae%a2%e9%81%8b%e8%b3%83 ・ 運航連絡の記事の日時 https://tomogashimakisen.com/main/category/operation-contact）")
SRC_CITY_ACCESS = ("和歌山市 公式サイト「友ヶ島へのアクセス」（当日の朝に運航を判断・電話 073-459-1333・整理券は第2便から・定員100名。2026-11-24 確認："
                   "https://www.city.wakayama.wakayama.jp/kankou/kankouspot/1027585/1027593.html）")
SRC_CITY = "和歌山市 公式サイト「友ヶ島」（散策コース・施設・注意・通行止め）"
SRC_PLANNER = "乗換案内（Yahoo!路線情報）2026-11-26（木）・11-28（土）のダイヤ"
SRC_LAST = ("最終の電車：乗換案内（Yahoo!路線情報 https://transit.yahoo.co.jp/ 、2026-11-24 に 11-26（木）・11-28（土）の「終電」で検索）。"
            "加太→なんば 木22:45発→0:39着・土22:51発→0:39着／加太→梅田(地下鉄) 木22:13発→0:19着・土21:53発→23:46着／加太→三条(京阪) 木21:25発・土21:27発→0:22着")
TRAIN_TIP = T("電車の時刻と運賃は乗換案内（2026年11月26日・木曜と28日・土曜のダイヤ）で確認しました。乗る前にもう一度確かめてください。",
              "Train times and fares checked on a route planner (timetables for Thu 26 and Sat 28 Nov 2026). Please check again before you travel.")
ISLAND_TIP = T("歩く時間は、和歌山市の「名所探訪コース」（3.3km、歩くだけで1時間20分）をもとに、少しゆったりめにしてあります。",
               "Walking times follow Wakayama City’s “Meisho Tambo” course (3.3 km, 1 h 20 min of walking alone), with a little slack added.")

# ---------------------------------------------------------------------------
# スポット（コースで変わらない部分）
# ---------------------------------------------------------------------------
S = dict(
    kadaeki=dict(
        name=T("南海 加太駅", "Nankai Kada Station"), kind=T("駅（スタート）", "Station (start)"),
        title=T("南海 加太駅（かだえき）", "Nankai Kada Station"),
        lat=34.27507, lng=135.08070,
        caution=T("出かける前に、今日の船が出るかを確認", "Before you set off, check that today’s boats are running"),
        body=T("運賃はなんばから加太まで1,010円。特急サザンは、なんば寄りの4両が自由席で、乗車券だけで乗れます（指定席は700円）。梅田のあたりのホテルからは、御堂筋線でなんばへ8分・240円。地下鉄から南海への乗り換えには、10分ほどみてください。\n\n"
               "和歌山市から先の加太線には、鯛をモチーフにした「めでたいでんしゃ」が走っています。吊り革も鯛の形。追加料金も予約もいりません。どの色がいつ走るかは、南海電鉄のサイトに出ています。\n\n"
               "島には売店がカフェ1軒しかありません。お昼に食べるものと飲み物は、なんばで電車に乗る前に買っておくのが確実です。",
               "Namba to Kada is ¥1,010. On the Southern limited express the four cars at the Namba end are unreserved and need only an ordinary ticket (reserved seats are ¥700). From a hotel around Umeda, the Midosuji Line takes 8 minutes to Namba (¥240); allow about 10 minutes to change from the subway to the Nankai platforms.\n\n"
               "Beyond Wakayamashi, the Kada Line runs the “Medetai Densha”, trains themed on the lucky sea bream, down to the fish-shaped hand straps. No surcharge, no booking. Nankai’s website shows which colour runs when.\n\n"
               "The island has just one small cafe. The sure way is to buy your lunch and drinks in Namba before you board the train."),
        gmaps=[gm("南海 加太駅", "Nankai Kada Station", 34.27507, 135.08070, "南海 加太駅")],
        links=[KISEN, PLANNER, MEDETAI],
        notices=[notice("出かける前に：今日、船は出ますか", "Before you leave: are the boats running today?",
                        "友ヶ島汽船は風と波でよく欠航します。2026年11月14日〜23日の10日間で、船が出たのは14日・17日・23日の3日だけでした（18日は水曜の運休、ほかの6日は強風・荒天で全便欠航）。出るかどうかは当日の朝に決まり（和歌山市の案内）、友ヶ島汽船の公式サイトの「運航連絡」に出ます。何時に出すとは書かれていませんが、2026年8月中旬〜11月の運航連絡は、どの日も前の晩か当日の朝6:30までに載っていました。電話でも聞けます（073-459-1333、日本語。受付時間は書かれていません）。",
                        "The Tomogashima boats are often cancelled for wind and waves. In the ten days from 14 to 23 November 2026 they ran on just three (the 14th, 17th and 23rd; the 18th was the regular Wednesday off, and the other six days were cancelled for strong wind or rough weather). The decision is made that morning (Wakayama City) and posted under “運航連絡” on the ferry’s website. No time is given, but from mid-August to November 2026 every notice was up by 6:30 that morning, sometimes the night before. You can also phone (073-459-1333, Japanese; phone hours not stated).",
                        KISEN_URL)],
        tip=TRAIN_TIP, checked=RECHECKED, source=[SRC_PLANNER, "南海電鉄 公式サイト（特急サザン・めでたいでんしゃ）", SRC_KISEN, SRC_CITY_ACCESS]),
    port=dict(
        name=T("加太港（友ヶ島汽船乗り場）", "Kada Port (Tomogashima ferry)"), kind=T("船乗り場", "Ferry pier"),
        title=T("加太港（かだこう）の友ヶ島汽船乗り場", "Kada Port: the Tomogashima Kisen ferry"),
        lat=34.27549, lng=135.07041,
        caution=T("水曜運休（1〜2月は土日祝だけ）。強風で欠航。現金を用意", "No boats Wed (Jan–Feb: weekends and holidays only). Cancelled in strong wind. Bring cash"),
        body=T("船は1日4往復だけです。加太港発 9:00・11:00・13:00・16:00、友ヶ島発 9:30・11:30・13:30・16:30。片道20分ほど。4月29日〜5月5日と7月20日〜8月31日は臨時便（加太発10:00）が増えますが、15:00の便は迎えの船なので日帰りの人は乗れません。\n\n"
               "往復で大人2,800円、こども1,250円。予約はできません。2便目（11:00）からは当日の乗船整理券が配られ、1便の定員は100人です。配りはじめる時刻と支払い方法は公式サイトに書かれていないので（要確認）、現金を用意して、船の時刻の45分前には港に着くようにしています。\n\n"
               "9〜10時にホテルを出る人は、13:00の船になります（なんば9:45発の特急サザン11号で加太11:21着、土曜は11:22着）。港で整理券をもらってから加太でお昼を食べ、島にいられるのは13:20〜16:30の約3時間。主な場所は回れますが、帰りは最終便しかありません。風で最終便が早まる日（2026年11月17日は友ヶ島発15:30が最終でした）は回りきれないので、できれば11:00までの船に乗ってください。\n\n"
               "欠航だった日は、加太で淡嶋神社とお昼と温泉にするか、和歌山市駅まで戻って和歌山城へ。",
               "There are only four round trips a day: from Kada at 9:00, 11:00, 13:00 and 16:00; from the island at 9:30, 11:30, 13:30 and 16:30. The crossing takes about 20 minutes. From 29 April to 5 May and 20 July to 31 August there is an extra 10:00 from Kada; the 15:00 extra is a pick-up run and day visitors cannot use it.\n\n"
               "A return ticket is ¥2,800 for adults, ¥1,250 for children. There are no advance bookings. From the second boat (11:00) on, same-day numbered tickets are handed out, and each boat takes 100 people. The website says neither when the tickets start being handed out nor how you can pay (unconfirmed), so bring cash, and this plan gets you to the port 45 minutes before the boat.\n\n"
               "If you leave your hotel at 9–10, your boat is the 13:00 (Southern 11 from Namba at 9:45, Kada 11:21, 11:22 on Saturdays). Get your numbered ticket, have lunch in Kada, and you have about three hours on the island, 13:20 to 16:30. That covers the main sights, but your only way back is the last boat. On days when wind brings the last boat forward (on 17 Nov 2026 it left the island at 15:30) you won’t get round, so take the 11:00 or earlier if you can.\n\n"
               "If the boats are cancelled: stay in Kada for Awashima Shrine, lunch and a hot spring, or go back to Wakayamashi Station for Wakayama Castle."),
        gmaps=[gm("友ヶ島汽船 乗り場", "Tomogashima Kisen pier", 34.27549, 135.07041, "友ヶ島汽船 加太")],
        links=[KISEN, CITY],
        notices=[notice("船が出ない日", "Days with no boats",
                        "3月〜12月は水曜が運休（祝日は運航）。1月〜2月は土・日・祝日だけ。12月29日〜1月3日は運休。そのほかの日も、風や波で欠航します。風が強くなる日は帰りの最終便が早まることがあり、「午前2便のみ運航（友ヶ島発最終便12時30分）」という日もあります（2026年10月13日・11月5日）。",
                        "March to December: no boats on Wednesdays (they run if it is a public holiday). January and February: Saturdays, Sundays and holidays only. None from 29 December to 3 January. On any other day they can be cancelled for wind or waves. On windy days the last boat back may leave early, and some days only the two morning boats run, with the last boat leaving the island at 12:30 (13 Oct and 5 Nov 2026).",
                        KISEN_URL)],
        rows=[row("hours", "加太港発 9:00・11:00・13:00・16:00／友ヶ島発 9:30・11:30・13:30・16:30（3月〜12月と、1〜2月の土日祝）。臨時便：4月29日〜5月5日・7月20日〜8月31日",
                  "From Kada 9:00, 11:00, 13:00, 16:00 / from the island 9:30, 11:30, 13:30, 16:30 (Mar–Dec, and weekends and holidays in Jan–Feb). Extra boats 29 Apr – 5 May and 20 Jul – 31 Aug"),
              row("closed", "3月〜12月の水曜（祝日は運航）。1月〜2月の平日。12月29日〜1月3日。悪天候の日は欠航",
                  "Wednesdays in Mar–Dec (except public holidays). Weekdays in Jan–Feb. 29 Dec – 3 Jan. Cancelled in bad weather"),
              row("fee", "往復 大人2,800円・こども1,250円（2026年7月1日から）。支払い方法は要確認", "Return: adults ¥2,800, children ¥1,250 (from 1 Jul 2026). Payment methods unconfirmed")],
        cash=True,
        tip=T("運航日・時刻・運賃・整理券は友ヶ島汽船の公式サイトで確認しました。電話番号は和歌山市の公式サイトから。支払い方法と整理券を配りはじめる時刻は、どちらのサイトにも書かれていません。",
              "Days, times, fares and numbered tickets checked on the Tomogashima Kisen website; the phone number is from the Wakayama City website. Neither site says how you can pay or when numbered tickets start being handed out."),
        checked=RECHECKED, source=[SRC_KISEN, SRC_CITY_ACCESS]),
    nonaura=dict(
        name=T("友ヶ島 野奈浦桟橋", "Nonaura Pier, Tomogashima"), kind=T("船着き場", "Pier"),
        title=T("友ヶ島 野奈浦桟橋（のなうらさんばし）", "Nonaura Pier, Tomogashima"),
        lat=34.28380, lng=135.00860,
        caution=T("島に水道なし。飲み物を買えるのは桟橋のまわりだけ", "No drinking water on the island. Drinks are sold only around the pier"),
        blurb=T("無人島の友ヶ島に到着。歩きだす前に、帰りの船の時刻・トイレ・飲み物の3つを済ませます。",
                "Landing on uninhabited Tomogashima. Before you walk: the boat back, the toilet, and something to drink."),
        body=T("友ヶ島は紀淡海峡に浮かぶ無人島の集まりで、船が着くのはいちばん大きな沖ノ島です。明治時代に大阪湾を守る要塞が造られ、レンガの砲台跡が森の中に残っています。\n\n"
               "桟橋のそばに友ヶ島案内センターとトイレ、「らぴゅカフェ」があります。カフェは9:30〜16:00、船が出る日だけ（天気で時間が変わります）。飲み物・ソフトクリーム・軽食があり、島で飲み物を買えるのはこのあたりだけです。島に水道はなく、井戸の水は沸かしても飲めません。1人1リットルは持って歩きましょう。\n\n"
               "トイレは島に4か所：ここ（野奈浦広場）、第3砲台跡の下、池尻広場、南垂水広場。ごみは全部持ち帰ります。道は舗装のない山道で、雨のあとは荒れています。歩きやすい靴で。砲台跡の中は暗いので、スマホのライトを使います。\n\n"
               "深蛇池（しんじゃいけ）と虎島へは、いまは行けません（和歌山市、2026年8月の案内）。",
               "Tomogashima is a group of uninhabited islands in the Kitan Strait; boats land on the largest, Okinoshima. In the Meiji era it was fortified to guard Osaka Bay, and brick gun batteries still stand in the woods.\n\n"
               "By the pier are the information centre, toilets and the Rapyu Cafe. The cafe opens 9:30–16:00, only on days the boats run (hours change with the weather), with drinks, soft-serve and light meals. This is the only place on the island where drinks are sold. There is no tap water, and the well water is not drinkable even boiled: carry a litre each.\n\n"
               "There are four toilets on the island: here (Nonaura Square), below the No. 3 Battery, Ikejiri Square and Minami-tarumi Square. Take all your rubbish back with you. The trails are unpaved and rough after rain: wear proper shoes. The batteries are dark inside, so use your phone torch.\n\n"
               "Shinja-ike pond and Torajima are closed for now (Wakayama City notice, August 2026)."),
        gmaps=[gm("野奈浦桟橋", "Nonaura Pier", 34.28380, 135.00860, "友ヶ島 野奈浦桟橋")],
        links=[KISEN, CITY, link("official", "らぴゅカフェ（友ヶ島汽船）", "Rapyu Cafe (Tomogashima Kisen, Japanese)", "https://tomogashimakisen.com/cafe/")],
        tip=ISLAND_TIP, source=[SRC_CITY, "らぴゅカフェ（tomogashimakisen.com/cafe/）", SRC_KISEN]),
    dai3=dict(
        name=T("第3砲台跡", "No. 3 Battery ruins"), kind=T("砲台跡", "Fort ruins"),
        title=T("第3砲台跡（だいさんほうだいあと）", "No. 3 Battery ruins"),
        lat=34.28005, lng=135.00666,
        blurb=T("レンガのアーチが並ぶ、友ヶ島でいちばん有名な場所。桟橋から上り坂を25分ほど。",
                "Tomogashima’s best-known sight: rows of brick arches, about 25 minutes uphill from the pier."),
        body=T("野奈浦桟橋から0.9km。山道の上りで、ゆっくり歩いて25分ほどです。\n\n"
               "レンガ造りの弾薬庫のアーチが並び、苔とつたに覆われています。地下の通路は真っ暗な所があるので、スマホのライトをつけて、足元を見ながら。建物の上や崩れかけた所には登らないでください。\n\n"
               "砲台跡の下にトイレがあります。次の展望台にはないので、ここで済ませておきましょう。",
               "0.9 km from Nonaura pier, up a hill trail: about 25 minutes at an easy pace.\n\n"
               "Rows of brick magazine arches stand covered in moss and ivy. Parts of the underground passages are pitch dark, so switch on your phone torch and watch your step. Don’t climb on the structures or crumbling sections.\n\n"
               "There is a toilet just below the battery, and none at the lookout that comes next."),
        gmaps=[gm("友ヶ島 第3砲台跡", "No. 3 Battery, Tomogashima", 34.28005, 135.00666, "友ヶ島 第3砲台跡")],
        links=[CITY], tip=ISLAND_TIP, source=[SRC_CITY]),
    takanosu=dict(
        name=T("タカノス山展望台", "Takanosu-yama Observatory"), kind=T("展望台", "Viewpoint"),
        title=T("タカノス山展望台（たかのすやまてんぼうだい）", "Takanosu-yama Observatory"),
        lat=34.28133, lng=135.00597,
        blurb=T("島のいちばん高い所。屋根のある休憩所があり、淡路島と紀淡海峡が見渡せます。",
                "The island’s highest point, with a roofed shelter and views over Awaji Island and the Kitan Strait."),
        body=T("第3砲台跡から階段を上って5分ほど。白い屋根の休憩所があり、海の向こうに淡路島が大きく見えます。道しるべには「大展望台」と書かれています。\n\n"
               "トイレはありません（第3砲台跡の下まで、階段を下りて5分ほど）。",
               "About 5 minutes up the steps from the No. 3 Battery. There is a shelter with white roofs, and Awaji Island looms across the sea. Signposts call it the “Dai-tenbodai”.\n\n"
               "No toilet here (the nearest is below the No. 3 Battery, about 5 minutes down the steps)."),
        gmaps=[gm("タカノス山展望台", "Takanosu-yama Observatory", 34.28133, 135.00597, "タカノス山展望台 友ヶ島")],
        links=[CITY], tip=ISLAND_TIP, source=[SRC_CITY]),
    kosuke=dict(
        name=T("孝助松海岸", "Kosukematsu beach"), kind=T("海岸", "Beach"),
        title=T("孝助松海岸（こうすけまつかいがん）", "Kosukematsu beach"),
        lat=34.28330, lng=135.00240,
        blurb=T("とがった岩が海に突き出す、島の北西の海岸。となりの池尻広場にトイレがあります。",
                "A beach on the north-west shore where a pointed rock juts into the sea. Toilets at Ikejiri Square next door."),
        body=T("展望台から山道を下って約1km、20〜25分。「孝助松」と書いた木の道しるべが目印です。海にとがった岩が突き出し、晴れた日は水の色がよく見えます。泳ぐのは禁止です。\n\n"
               "すぐとなりの池尻広場にトイレがあります。ここから灯台までは歩いて10分ほど。",
               "About 1 km down the trail from the lookout, 20 to 25 minutes. A wooden signpost reading “孝助松” marks the spot. A pointed rock juts into the sea, and on a clear day you can see the colour of the water. No swimming.\n\n"
               "Ikejiri Square, right beside it, has toilets. From here the lighthouse is about 10 minutes’ walk."),
        gmaps=[gm("孝助松海岸", "Kosukematsu beach", 34.28330, 135.00240, "友ヶ島 孝助松海岸")],
        links=[CITY], tip=ISLAND_TIP, source=[SRC_CITY]),
    toudai=dict(
        name=T("友ヶ島灯台", "Tomogashima Lighthouse"), kind=T("灯台", "Lighthouse"),
        title=T("友ヶ島灯台（ともがしまとうだい）", "Tomogashima Lighthouse"),
        lat=34.28091, lng=135.00046,
        blurb=T("明治時代に建てられた白い灯台。まわりは芝生で、腰を下ろして休めます。",
                "A white lighthouse from the Meiji era, with grass around it to sit and rest on."),
        body=T("島の西の端に立つ白い灯台です。明治時代に建てられた古い灯台のひとつで、まわりは芝生の広場。岩場の海を見下ろせます。すぐとなりが子午線広場です。\n\n"
               "第2砲台跡までは歩いて10分ほどです。",
               "A white lighthouse at the western tip of the island, one of Japan’s early Meiji-era lighthouses. Grass surrounds it, looking down on the rocky shore. Shigosen (Meridian) Square is right beside it.\n\n"
               "The No. 2 Battery is about 10 minutes’ walk."),
        gmaps=[gm("友ヶ島灯台", "Tomogashima Lighthouse", 34.28091, 135.00046, "友ヶ島灯台")],
        links=[CITY], tip=ISLAND_TIP, source=[SRC_CITY]),
    dai2=dict(
        name=T("第2砲台跡", "No. 2 Battery ruins"), kind=T("砲台跡", "Fort ruins"),
        title=T("第2砲台跡（だいにほうだいあと）", "No. 2 Battery ruins"),
        lat=34.28213, lng=135.00055,
        body=T("海に面した砲台跡です。大きなレンガとコンクリートの塊が崩れ落ちたまま残っていて、第3砲台跡とは違う迫力があります。崩れていて危ないので、柵の中には入らないでください。\n\n"
               "ここから野奈浦桟橋までは0.9km、ゆっくり歩いて25分ほどです。",
               "A battery facing the sea. Huge blocks of brick and concrete lie where they fell, a different kind of drama from the No. 3 Battery. It is unstable, so stay outside the fences.\n\n"
               "From here it is 0.9 km to Nonaura pier, about 25 minutes at an easy pace."),
        gmaps=[gm("友ヶ島 第2砲台跡", "No. 2 Battery, Tomogashima", 34.28213, 135.00055, "友ヶ島 第2砲台跡")],
        links=[CITY, KISEN], tip=ISLAND_TIP, source=[SRC_CITY, SRC_KISEN]),
    awashima=dict(
        name=T("淡嶋神社", "Awashima Shrine"), kind=T("神社", "Shrine"),
        title=T("淡嶋神社（あわしまじんじゃ）", "Awashima Shrine"),
        lat=34.27360, lng=135.06671,
        caution=T("参拝は9:00〜17:00", "Open 9:00–17:00"),
        body=T("人形供養で知られる神社です。社殿のまわりに、全国から納められた人形がびっしり並んでいます。毎年3月3日には、ひな人形を小舟にのせて海へ流す「雛流し」があります。参拝は9:00〜17:00。\n\n"
               "参道には、つぼ焼きやよもぎ餅を売るみやげ物屋が3軒あります（雨の日は休むことがあります）。",
               "A shrine known for its memorial services for dolls: dolls sent from all over Japan stand packed around the hall. Every 3 March, in the “Hina-nagashi”, Girls’ Day dolls are set adrift on the sea in little boats. Open 9:00–17:00.\n\n"
               "Three souvenir stalls on the approach sell grilled turban shells and yomogi rice cakes (they may close on rainy days)."),
        gmaps=[gm("淡嶋神社", "Awashima Shrine", 34.27360, 135.06671, "淡嶋神社 和歌山市加太")],
        rows=[row("hours", "参拝 9:00〜17:00", "Open 9:00–17:00")],
        tip=T("参拝時間は淡嶋神社の公式ページ、お店と温泉の時間はそれぞれの公式サイトで確認しました。", "Shrine hours checked on the shrine’s official page; restaurant and bath hours on their own websites."),
        checked=RECHECKED,
        source=["淡嶋神社 公式ページ（kada.jp/awashima）",
                "活魚料理 いなさ（2026-11-24 確認 https://www.inasa.net/index.html ：11:00〜15:00・LO14:30、夜は要予約、火・水曜休み、祝日の連休は要問合せ。支払い方法の記載なし）",
                "加太淡嶋温泉 大阪屋 ひいなの湯（2026-11-24 確認 https://www.hiina.com/spa/ ・ https://www.hiina.com/faq/ ：11:00〜19:00、土日祝・休前日・混雑時は15:00まで、1,200円。最終受付とタトゥーの記載なし）",
                "休暇村紀州加太（2026-11-24 確認 https://www.qkamura.or.jp/kada/oneday/ ：12:00〜15:50・15:00札止め・1,500円・刺青タトゥー不可）",
                "シーサイドホテル加太海月（2026-11-24 確認 https://kada-kaigetsu.com/day_use/ ：11:00〜15:00・最終受付14:30・1,200円・精算は現金かカード。タトゥーの記載なし）",
                "いなさの位置：国土地理院の住所検索（加太196番地）と OpenStreetMap。友ヶ島汽船の乗り場から直線で約170m"]),
    kadaeki2=dict(
        name=T("南海 加太駅（帰り）", "Nankai Kada Station (return)"), kind=T("駅（ゴール）", "Station (finish)"),
        title=T("南海 加太駅（帰り）", "Nankai Kada Station (return)"),
        lat=34.27507, lng=135.08070,
        body=T("加太の「活魚料理 いなさ」は、夜は予約制です（公式サイト）。予約なしで入れる晩ごはんの店は公式サイトで確かめられなかったので、晩ごはんはなんばに戻ってからにしています。なんば駅から法善寺横丁と道頓堀までは歩いて5分ほど。店は大阪マップにまとめてあります。\n\n"
               "遅くなっても、木曜なら加太22:13発でなんば23:53着、御堂筋線の最終（なんば0:10発）で梅田0:19着。土曜は、梅田まで地下鉄で帰れる最後が加太21:53発（梅田23:46着）です。なんばまでの最終は加太22:45発（土曜22:51発）で、なんば0:39着。京都へ帰る人は、加太21:25発（土曜21:27発）が最後で、淀屋橋23:33発の京阪特急で三条0:22着です。",
               "Inasa in Kada takes dinner guests by reservation only (official site). No place you can simply walk into for dinner could be confirmed on an official website, so dinner in this plan is back in Namba. Hozenji Yokocho and Dotonbori are about 5 minutes’ walk from Namba Station; the Osaka map lists where to eat.\n\n"
               "If you run late: on Thursdays the 22:13 from Kada reaches Namba at 23:53, in time for the last Midosuji Line train (Namba 0:10, Umeda 0:19). On Saturdays the last train from Kada that connects with the subway to Umeda is the 21:53 (Umeda 23:46). The last train to Namba leaves Kada at 22:45 (22:51 on Saturdays) and arrives at 0:39. For Kyoto, the last is the 21:25 from Kada (21:27 on Saturdays), connecting with the 23:33 Keihan limited express from Yodoyabashi to Sanjo (0:22)."),
        gmaps=[gm("南海 加太駅", "Nankai Kada Station", 34.27507, 135.08070, "南海 加太駅")],
        links=[PLANNER, OSAKA_MAP], tip=TRAIN_TIP, checked=RECHECKED,
        source=[SRC_PLANNER, SRC_LAST, "活魚料理 いなさ（2026-11-24 確認 https://www.inasa.net/index.html ：夜の営業は要予約）"]),
)

# 加太のお昼・温泉（淡嶋神社のスポットの中で紹介する。どれも公式サイトで確認、タトゥーは書いてあるものだけ）
LUNCH = T("お昼：加太の鯛を出す「活魚料理 いなさ」は11:00〜15:00（オーダーストップ14:30）、火・水曜休み（祝日が続く日は店に問い合わせ）。支払い方法は公式サイトに書かれていません（要確認）。",
          "Lunch: Inasa, which serves Kada sea bream, opens 11:00–15:00 (last orders 14:30), closed Tuesdays and Wednesdays (ask the restaurant about holiday weekends). Its website does not say how you can pay (unconfirmed).")
BATHS = T("温泉：神社のすぐそばの旅館・大阪屋の「ひいなの湯」は日帰り入浴11:00〜19:00（土日祝・休前日と混む日は15:00まで）、1,200円・フェイスタオルつき。最終受付の時刻とタトゥーの決まりは公式サイトに書かれていないので、入る前に受付で聞いてください（要確認）。"
          "休暇村紀州加太の「天空の湯」は12:00〜15:50（受付15:00まで）・1,500円ですが、タトゥーのある人は入れません（公式サイト）。シーサイドホテル加太海月は11:00〜15:00（受付14:30まで）・1,200円・バスタオルつき、支払いは現金かカード。タトゥーは公式サイトに書かれていません（要確認）。",
          "Baths: Hiina-no-yu at the Osakaya inn, right by the shrine, takes day visitors 11:00–19:00 (until 15:00 on weekends, holidays, the day before a holiday and busy days), ¥1,200 with a small towel. Its website gives neither a last entry time nor a tattoo policy, so ask at the desk first (unconfirmed). "
          "Tenku-no-yu at Kyukamura Kishu-Kada is 12:00–15:50 (entry until 15:00), ¥1,500, but does not admit guests with tattoos (official site). Seaside Hotel Kada Kaigetsu is 11:00–15:00 (entry until 14:30), ¥1,200 with a bath towel, cash or card; its website says nothing about tattoos (unconfirmed).")
AW_LINKS = [link("official", "淡嶋神社", "Awashima Shrine (Japanese)", "https://www.kada.jp/awashima/"),
            link("official", "活魚料理 いなさ（11:00〜15:00、火・水曜休み）", "Inasa restaurant (11:00–15:00, closed Tue & Wed; Japanese)", "http://www.inasa.net/index.html"),
            link("official", "ひいなの湯（日帰り入浴）", "Hiina-no-yu day bathing (Japanese)", "https://www.hiina.com/spa/"),
            link("official", "休暇村紀州加太（日帰り入浴・タトゥー不可）", "Kyukamura Kishu-Kada day bathing (no tattoos; Japanese)", "https://www.qkamura.or.jp/kada/oneday/")]
S["awashima"]["links"] = AW_LINKS

KYOTO_OUT_LATE = row("train", "京都から：三条6:48発（京阪）→ 淀屋橋7:50着 →（御堂筋線）→ なんば8:03着 → 8:14発の特急サザン5号に。三条→加太 1,690円。土曜は三条6:58発の特急で同じサザン5号（なんば8:15発）",
                     "From Kyoto: Sanjo 6:48 (Keihan) → Yodoyabashi 7:50 → (Midosuji Line) → Namba 8:03 → Southern 5 at 8:14. Sanjo → Kada ¥1,690. Saturdays: the 6:58 limited express from Sanjo makes the same Southern 5 (Namba 8:15)")
KYOTO_OUT_EARLY = row("train", "京都から：三条5:04発（京阪・始発）→ 北浜6:14着 →（堺筋線）→ 天下茶屋6:34着 → 6:42発の南海の急行 → 和歌山市7:47着・7:55発 → 加太8:19着。1,700円・乗り換え3回",
                      "From Kyoto: Sanjo 5:04 (the first Keihan train) → Kitahama 6:14 → (Sakaisuji Line) → Tengachaya 6:34 → Nankai express 6:42 → Wakayamashi 7:47 / 7:55 → Kada 8:19. ¥1,700, three changes")
KYOTO_BACK = row("train", "京都へ帰る人：加太17:27発 → なんば18:59着 →（御堂筋線）→ 淀屋橋 →（京阪）→ 三条20:20ごろ。最後は、加太21:25発（土曜21:27発）→ 淀屋橋23:33発の京阪特急 → 三条0:22着",
                 "Back to Kyoto: Kada 17:27 → Namba 18:59 → (Midosuji Line) → Yodoyabashi → (Keihan) → Sanjo about 20:20. The last connection: Kada 21:25 (21:27 on Saturdays) → Keihan limited express from Yodoyabashi 23:33 → Sanjo 0:22")
LAST_ROW = row("train", "遅い電車：木曜は加太22:13発 → なんば23:53着 →（御堂筋線の最終 0:10発）→ 梅田0:19着。土曜に梅田まで地下鉄で帰れる最後は加太21:53発 → 梅田23:46着。なんばまでの最終は加太22:45発（土曜22:51発）→ なんば0:39着（御堂筋線の梅田行きは終わっています）",
               "Late trains: on Thursdays, Kada 22:13 → Namba 23:53 → (last Midosuji Line train, 0:10) → Umeda 0:19. On Saturdays the last that connects with the subway to Umeda is Kada 21:53 → Umeda 23:46. The last train to Namba: Kada 22:45 (22:51 on Saturdays) → Namba 0:39 (the last Midosuji Line train to Umeda has gone)")

# ---------------------------------------------------------------------------
# コース
# ---------------------------------------------------------------------------
LATE = dict(
    id="late", file="tomogashima.json",
    order=["kadaeki", "port", "awashima", "nonaura", "dai3", "takanosu", "kosuke", "toudai", "dai2", "kadaeki2"],
    sections=[("kadaeki", "awashima", "加太", "Kada", "なんばから電車で加太へ。整理券をもらって淡嶋神社", "By train from Namba; get your boat ticket, then the shrine"),
              ("nonaura", "takanosu", "友ヶ島", "Tomogashima", "11:00の船で島へ。第3砲台跡と展望台でお昼", "The 11:00 boat; the No. 3 Battery and lunch at the lookout"),
              ("kosuke", "dai2", "友ヶ島の西", "West side of the island", "海岸・灯台・第2砲台跡。15:15に桟橋へ向かう", "Beach, lighthouse, No. 2 Battery; head for the pier at 15:15"),
              ("kadaeki2", "kadaeki2", "加太 → なんば", "Kada → Namba", "16:30の船で戻って、夜はなんばで", "Back on the 16:30 boat; evening in Namba")],
    spots=dict(
        kadaeki=dict(
            blurb=T("なんば8:14発の特急サザン5号で、加太に9:58着（土曜は8:15発・9:48着）。お昼と飲み物は、乗る前になんばで。",
                    "Southern 5 leaves Namba at 8:14 and gets you to Kada at 9:58 (Saturdays 8:15, arriving 9:48). Buy lunch and drinks in Namba first."),
            pre=T("なんば8:14発の特急サザン5号で和歌山市へ（9:17着）、9:35発の加太線に乗り換えて、加太に9:58に着きます。土曜は、なんば8:15発・和歌山市9:14着、9:24発・加太9:48着。梅田のあたりのホテルは7:40ごろ、難波のあたりなら8:00ごろに出れば間に合います。",
                  "Take Southern 5 from Namba at 8:14 to Wakayamashi (9:17), change to the 9:35 Kada Line train and arrive at 9:58. On Saturdays: Namba 8:15, Wakayamashi 9:14 / 9:24, Kada 9:48. Leave a hotel around Umeda at about 7:40, or one around Namba at about 8:00."),
            post=T("駅から加太港の友ヶ島汽船乗り場までは、歩いて15〜20分。まっすぐ港へ行き、先に船の整理券をもらいます。",
                   "The ferry pier at Kada Port is 15 to 20 minutes’ walk. Go straight there and get your numbered boat ticket first."),
            time=T("9:58着（土曜は9:48着）", "arrive 9:58 (9:48 on Saturdays)"),
            rows=[row("train", "なんば8:14発（特急サザン5号）→ 和歌山市9:17着・9:35発（加太線）→ 加太9:58着。土曜：なんば8:15発 → 和歌山市9:14着・9:24発 → 加太9:48着",
                      "Namba 8:14 (Southern 5) → Wakayamashi 9:17 / 9:35 (Kada Line) → Kada 9:58. Saturdays: Namba 8:15 → Wakayamashi 9:14 / 9:24 → Kada 9:48"),
                  row("fee", "なんば→加太 1,010円（サザンの自由席は追加料金なし）。梅田→なんば 240円", "Namba → Kada ¥1,010 (no surcharge in the Southern’s unreserved cars). Umeda → Namba ¥240"),
                  KYOTO_OUT_LATE]),
        port=dict(
            blurb=T("10:15に港に着いて11:00の船の整理券をもらい、船まで淡嶋神社へ。帰りは16:30の最終便です。",
                    "Reach the port at 10:15 for a numbered ticket for the 11:00 boat, then visit the shrine. You come back on the last boat, the 16:30."),
            pre=T("10:15ごろ港に着いたら、まず11:00の船の乗船整理券をもらい、乗船券を買います。船が出るまでの30分ほどで、歩いて5分の淡嶋神社へ。10:50には乗り場に戻ってください。列が長い日は、神社は鳥居だけ見て戻ります。",
                  "Arriving at about 10:15, first get your numbered ticket for the 11:00 boat and buy your fare. In the half hour before it leaves, walk 5 minutes to Awashima Shrine, and be back at the pier by 10:50. If the queue is long, just look at the torii and come back."),
            time=T("10:15着・11:00の船に乗る", "arrive 10:15, board the 11:00 boat"), rows=[]),
        awashima=dict(
            blurb=T("人形供養で知られる神社。整理券をもらってから、船が出るまでの20分でお参りします。",
                    "A shrine known for its doll memorials: a 20-minute visit between getting your ticket and boarding."),
            pre=T("港から歩いて5分。帰りの船が加太に着くのは16:50で、神社は17:00に閉まります。このコースでは、行きの船に乗る前にお参りしておきます。",
                  "Five minutes’ walk from the port. The boat back reaches Kada at 16:50 and the shrine closes at 17:00, so on this course you visit before the outbound boat."),
            post=T("船で戻ったあとの加太：11月下旬の日の入りは16:50ごろで、船を降りるころに日が沈みます（1月中旬は17:10ごろ、3月下旬は18:15ごろ）。\n\n" + BATHS["ja"] + "\n\n平日（休前日をのぞく）なら、16:30の船で戻ってから「ひいなの湯」に入れます。",
                   "Kada after the boat back: in late November the sun sets at about 16:50, just as you step off the boat (about 17:10 in mid-January, 18:15 in late March).\n\n" + BATHS["en"] + "\n\nOn weekdays (other than the day before a holiday) you can still use Hiina-no-yu after the 16:30 boat."),
            time=T("10:22〜10:42", "10:22–10:42"), rows=[]),
        nonaura=dict(
            pre=T("11:00の船で、11:20に着きます。", "The 11:00 boat lands at 11:20."),
            post=T("帰りは16:30発の最終便です。着いたらすぐ、乗り場かカフェで「今日の最終便は何時ですか」と確かめてください。風の強い日は15:30に早まることがあり、その日は下の時間を1時間ずつ前に詰めます。「午前2便のみ運航」の日は12:30が最終で、島にいられるのは1時間ほどです（第3砲台跡まで往復すると間に合わないことがあります）。最終便を逃すと、その日のうちに島を出る船はありません。\n\n"
                   "時間割：11:35に出発 → 第3砲台跡 → 展望台でお昼 → 孝助松海岸 → 灯台 → 第2砲台跡を15:15に出る → 15:40に桟橋。カフェは16:00までなので、冷たいものはそれまでに。16:10には乗り場に並びます。",
                   "You go back on the last boat, the 16:30. As soon as you land, ask at the pier or the cafe what time today’s last boat leaves. On windy days it can be brought forward to 15:30; if so, move everything below an hour earlier. On days when only the two morning boats run, the last leaves at 12:30 and you have about an hour on the island (not always enough for the round trip to the No. 3 Battery). Miss the last boat and there is no other boat off the island that day.\n\n"
                   "Timetable: set off at 11:35 → No. 3 Battery → lunch at the lookout → Kosukematsu beach → lighthouse → leave the No. 2 Battery at 15:15 → pier at 15:40. The cafe closes at 16:00, so have your cold drink before then, and queue at the pier by 16:10."),
            time=T("11:20着〜11:35出発（帰りは16:30の船）", "arrive 11:20, set off 11:35 (16:30 boat back)"),
            rows=[row("hours", "らぴゅカフェ 9:30〜16:00（船が出る日だけ。天気で変わる）", "Rapyu Cafe 9:30–16:00 (only on days the boats run; changes with the weather)")]),
        dai3=dict(time=T("12:00〜12:40", "12:00–12:40")),
        takanosu=dict(
            post=T("持ってきたお昼は、ここの休憩所で。", "Eat the lunch you brought in the shelter here."),
            time=T("12:45〜13:25（お昼）", "12:45–13:25 (lunch)")),
        kosuke=dict(time=T("13:45〜14:05", "13:45–14:05")),
        toudai=dict(time=T("14:15〜14:40", "14:15–14:40")),
        dai2=dict(
            blurb=T("海に面して崩れたままの砲台跡。ここを15:15に出れば、16:30の船に余裕で間に合います。",
                    "A battery left as it collapsed, facing the sea. Leave here at 15:15 and you make the 16:30 boat with time to spare."),
            post=T("15:15にはここを出て、桟橋へ。写真を撮っていて遅れても、15:45には歩きはじめてください。",
                   "Leave here at 15:15 for the pier. Even if photos hold you up, be walking by 15:45."),
            time=T("14:45〜15:15", "14:45–15:15")),
        kadaeki2=dict(
            blurb=T("16:50に港に戻り、17:27発でなんばに18:59着。晩ごはんは法善寺横丁か道頓堀で。",
                    "Back at the port at 16:50; the 17:27 train reaches Namba at 18:59. Dinner at Hozenji Yokocho or Dotonbori."),
            pre=T("16:30の船は加太港に16:50に着きます。港から駅まで歩いて15〜20分。17:27発に乗ると、和歌山市で特急サザン50号に乗り換えて、なんばに18:59に着きます。平日に「ひいなの湯」に入るなら、18:24発（土曜は18:20発）でなんば20:00ごろ。",
                  "The 16:30 boat reaches Kada Port at 16:50, and the station is 15 to 20 minutes’ walk. The 17:27 connects at Wakayamashi with Southern 50 and reaches Namba at 18:59. If you take a bath at Hiina-no-yu on a weekday, the 18:24 (18:20 on Saturdays) gets you to Namba at about 20:00."),
            time=T("17:27発（なんば18:59着）", "depart 17:27 (Namba 18:59)"),
            rows=[row("train", "加太17:27発 → 和歌山市17:52着・18:00発（特急サザン50号）→ なんば18:59着・1,010円。次は17:46発 → 19:25着、18:03発 → 19:48着（土曜は19:55着）、18:24発（土曜18:20発）→ 20:00ごろ",
                      "Kada 17:27 → Wakayamashi 17:52 / 18:00 (Southern 50) → Namba 18:59, ¥1,010. Then 17:46 → 19:25, 18:03 → 19:48 (19:55 on Saturdays), 18:24 (18:20 on Saturdays) → about 20:00"),
                  LAST_ROW, KYOTO_BACK]),
    ),
)

EARLY = dict(
    id="early", file="tomogashima-early.json",
    order=["kadaeki", "port", "nonaura", "dai3", "takanosu", "kosuke", "toudai", "dai2", "awashima", "kadaeki2"],
    sections=[("kadaeki", "port", "加太", "Kada", "なんば6:38発。8:40に港へ", "Namba 6:38; at the port by 8:40"),
              ("nonaura", "takanosu", "友ヶ島", "Tomogashima", "9:00の船で島へ。人の少ない第3砲台跡", "The 9:00 boat; the No. 3 Battery before the crowds"),
              ("kosuke", "dai2", "友ヶ島の西", "West side of the island", "海岸・灯台・第2砲台跡。12:45に桟橋へ向かう", "Beach, lighthouse, No. 2 Battery; head for the pier at 12:45"),
              ("awashima", "kadaeki2", "加太 → なんば", "Kada → Namba", "13:30の船で戻って、加太でお昼と神社と温泉", "Back on the 13:30 boat: lunch, shrine and a bath in Kada")],
    spots=dict(
        kadaeki=dict(
            blurb=T("なんば6:38発の急行で、加太に8:19着（土曜は6:24発・7:59着）。朝ごはんと飲み物は、乗る前になんばで。",
                    "The 6:38 express from Namba gets you to Kada at 8:19 (Saturdays 6:24, arriving 7:59). Buy breakfast and drinks in Namba first."),
            pre=T("なんば6:38発の急行で和歌山市へ（7:47着）、7:55発の加太線に乗り換えて、加太に8:19に着きます。土曜は、なんば6:24発の区間急行で紀ノ川7:35着、7:38発に乗り換えて加太7:59着（次の6:40発の空港急行だと、泉佐野と紀ノ川で乗り換えて8:21着）。梅田のあたりのホテルは6:00ごろ、難波のあたりなら6:20ごろに出ます。\n\n"
                  "公式サイトの運航連絡は、2026年8月中旬〜11月はどの日も前の晩か当日の朝6:30までに出ていました。ホテルを出る前に見て、電車の中と加太駅でもう一度確かめてください。",
                  "Take the 6:38 express from Namba to Wakayamashi (7:47), change to the 7:55 Kada Line train and arrive at 8:19. On Saturdays: the 6:24 semi-express from Namba to Kinokawa (7:35), change to the 7:38 and arrive at 7:59 (the next train, the 6:40 airport express, means changing at Izumisano and Kinokawa and arrives 8:21). Leave a hotel around Umeda at about 6:00, or one around Namba at about 6:20.\n\n"
                  "From mid-August to November 2026 the ferry’s operating notice was always up by 6:30 that morning, sometimes the night before. Check it before you leave the hotel, and again on the train and at Kada Station."),
            post=T("駅から加太港の友ヶ島汽船乗り場までは、歩いて15〜20分です。", "The ferry pier at Kada Port is 15 to 20 minutes’ walk."),
            time=T("8:19着（土曜は7:59着）", "arrive 8:19 (7:59 on Saturdays)"),
            rows=[row("train", "なんば6:38発（急行）→ 和歌山市7:47着・7:55発（加太線）→ 加太8:19着。土曜：なんば6:24発（区間急行）→ 紀ノ川7:35着・7:38発 → 加太7:59着",
                      "Namba 6:38 (express) → Wakayamashi 7:47 / 7:55 (Kada Line) → Kada 8:19. Saturdays: Namba 6:24 (semi-express) → Kinokawa 7:35 / 7:38 → Kada 7:59"),
                  row("fee", "なんば→加太 1,010円。梅田→なんば 240円（御堂筋線の始発は梅田5:15発）", "Namba → Kada ¥1,010. Umeda → Namba ¥240 (first Midosuji Line train from Umeda 5:15)"),
                  KYOTO_OUT_EARLY]),
        port=dict(
            blurb=T("8:40に港に着いて、9:00の最初の船へ。帰りは13:30の船にして、午後は加太で過ごします。",
                    "At the port by 8:40 for the first boat at 9:00. Come back on the 13:30 and spend the afternoon in Kada."),
            pre=T("8:40ごろ港に着いて、9:00の最初の船に乗ります。公式の案内では、整理券が配られるのは2便目からの分です。最初の船は、乗り場で乗船券を買って乗ります。帰りは13:30の船。そのあとにも16:30の便があるので、風で予定が変わった日も戻りやすいのがこの船のいいところです。",
                  "Reach the port at about 8:40 and take the first boat at 9:00. According to the ferry company, numbered tickets are for the second boat on; for the first you simply buy your fare at the pier. You come back on the 13:30. With the 16:30 still to come after it, this is the boat that leaves you a way back if the wind changes the day."),
            time=T("8:40着・9:00の船に乗る", "arrive 8:40, board the 9:00 boat"), rows=[]),
        nonaura=dict(
            pre=T("9:00の船で、9:20に着きます。カフェが開くのは9:30です。", "The 9:00 boat lands at 9:20. The cafe opens at 9:30."),
            post=T("帰りは13:30発の船です。着いたら、乗り場で今日の帰りの便の時刻を確かめてから歩きはじめます。\n\n"
                   "時間割：9:35に出発 → 第3砲台跡 → 展望台でひと休み → 孝助松海岸 → 灯台 → 第2砲台跡を12:45に出る → 13:10に桟橋。13:20には乗り場に並びます。お昼は加太に戻ってからなので、おにぎりかパンを1つ持って歩くと楽です。",
                   "You go back on the 13:30 boat. On landing, check today’s return times at the pier before you set off.\n\n"
                   "Timetable: set off at 9:35 → No. 3 Battery → a rest at the lookout → Kosukematsu beach → lighthouse → leave the No. 2 Battery at 12:45 → pier at 13:10. Queue at the pier by 13:20. Lunch is back in Kada, so carry a rice ball or a bun to keep you going."),
            time=T("9:20着〜9:35出発（帰りは13:30の船）", "arrive 9:20, set off 9:35 (13:30 boat back)"),
            rows=[row("hours", "らぴゅカフェ 9:30〜16:00（船が出る日だけ。天気で変わる）", "Rapyu Cafe 9:30–16:00 (only on days the boats run; changes with the weather)")]),
        dai3=dict(
            blurb=T("レンガのアーチが並ぶ、友ヶ島でいちばん有名な場所。最初の船なら、人の少ないうちに着きます。",
                    "Tomogashima’s best-known sight: rows of brick arches. Off the first boat, you get here before most people."),
            time=T("10:00〜10:40", "10:00–10:40")),
        takanosu=dict(time=T("10:45〜11:10", "10:45–11:10")),
        kosuke=dict(time=T("11:30〜11:45", "11:30–11:45")),
        toudai=dict(time=T("11:55〜12:15", "11:55–12:15")),
        dai2=dict(
            blurb=T("海に面して崩れたままの砲台跡。ここを12:45に出れば、13:30の船に間に合います。",
                    "A battery left as it collapsed, facing the sea. Leave here at 12:45 and you make the 13:30 boat."),
            post=T("12:45にはここを出て、桟橋へ。遅くとも13:00には歩きはじめてください。乗り遅れても16:30の便がありますが、加太の午後はなくなります。",
                   "Leave here at 12:45 for the pier, 13:00 at the very latest. If you miss the boat there is still the 16:30, but you lose your afternoon in Kada."),
            time=T("12:20〜12:45", "12:20–12:45")),
        awashima=dict(
            blurb=T("13:50に港に戻ったら、加太でお昼、淡嶋神社、温泉。神社は17:00まで。",
                    "Back at the port at 13:50: lunch in Kada, Awashima Shrine and a bath. The shrine closes at 17:00."),
            pre=T("13:30の船は加太港に13:50に着きます。先にお昼、そのあと神社（港から歩いて5分）、時間があれば温泉の順です。\n\n" + LUNCH["ja"] + "港に着いてからオーダーストップまで40分しかないので、船を降りたらまっすぐ向かいます。店は港の乗り場から淡嶋神社の方へ200mほど（Googleマップで「活魚料理 いなさ」）。火曜と、間に合わなかった日は、神社の参道の店でつぼ焼きを。",
                  "The 13:30 boat reaches Kada Port at 13:50. Lunch first, then the shrine (5 minutes’ walk from the port), then a bath if there is time.\n\n" + LUNCH["en"] + " You have only 40 minutes between landing and last orders, so head straight there off the boat: it is about 200 m from the pier towards Awashima Shrine (search “活魚料理 いなさ” in Google Maps). On Tuesdays, or if you are too late, have grilled turban shells at the stalls on the shrine approach."),
            post=T(BATHS["ja"] + "\n\n土日祝は3つとも受付が15:00ごろまでなので、温泉に入りたい日は、船を降りたら先に温泉へ。",
                   BATHS["en"] + "\n\nOn weekends and holidays all three stop taking bathers at about 15:00, so if you want a bath, go there first off the boat."),
            time=T("お昼13:55〜14:40、神社14:45〜15:10", "lunch 13:55–14:40, shrine 14:45–15:10"), rows=[]),
        kadaeki2=dict(
            blurb=T("神社から駅まで歩いて約20分。16:25発でなんばに17:59着。温泉に入った日は16:56発で18:29着。",
                    "About 20 minutes’ walk from the shrine. The 16:25 reaches Namba at 17:59; after a bath, the 16:56 arrives at 18:29."),
            pre=T("淡嶋神社から駅までは歩いて約20分。神社を15:10に出て町をぶらぶら歩いても、16:25発に間に合います。和歌山市で特急サザン46号に乗り換えて、なんばに17:59着。平日に「ひいなの湯」に入った日は16:56発（土曜は16:58発）で18:29着。夕日まで加太にいるなら17:27発で18:59着です（11月下旬の日の入りは16:50ごろ）。",
                  "The station is about 20 minutes’ walk from Awashima Shrine. Leave the shrine at 15:10, wander through the town, and you still make the 16:25, which connects at Wakayamashi with Southern 46 and reaches Namba at 17:59. After a weekday bath at Hiina-no-yu, take the 16:56 (16:58 on Saturdays), arriving 18:29. To stay for the sunset, the 17:27 arrives at 18:59 (sunset is about 16:50 in late November)."),
            time=T("16:25発（なんば17:59着）", "depart 16:25 (Namba 17:59)"),
            rows=[row("train", "加太16:25発 → 和歌山市16:49着・17:00発（特急サザン46号）→ なんば17:59着・1,010円。前は15:59発（土曜15:58発）→ 17:29着。あとは16:56発（土曜16:58発）→ 18:29着、17:27発 → 18:59着",
                      "Kada 16:25 → Wakayamashi 16:49 / 17:00 (Southern 46) → Namba 17:59, ¥1,010. Before it: 15:59 (15:58 on Saturdays) → 17:29. After it: 16:56 (16:58 on Saturdays) → 18:29, 17:27 → 18:59"),
                  LAST_ROW, KYOTO_BACK]),
    ),
)

NOTE_HEAD = ("友ヶ島・加太の日帰りルート（tomogashima/ のページ専用。形は eizan-line.json と同じ）。起点は大阪の梅田〜難波のあたりのホテル。一覧の上のボタンで行きの船を選び、コースごとに別のファイルを読む"
             "（tomogashima.json＝11:00の船で渡って16:30の船で戻る、tomogashima-early.json＝9:00の船で渡って13:30の船で戻り、午後は加太）。このファイル：")
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから（加太は2022年7月8日、友ヶ島と淡嶋神社は2023年6月20日。Nikon D7000 の写真は島にGPSの写真が2枚しかないので、道しるべの看板と撮影時刻の順で場所を決めた。"
             "1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。port-1.jpg は、窓に貼ってあった選挙のポスターが写らないように上の部分だけを切り出した。"
             "info.source は確認した出典、info.checked は確認日。入口で困ること（欠航・運休日・現金・水道なし・参拝時間）は caution と head つきの notices。"
             "友ヶ島汽船の支払い方法、整理券を配りはじめる時刻、ひいなの湯の最終受付、ひいなの湯と加太海月のタトゥーの決まり、いなさの支払い方法は公式サイトに書かれておらず、文章の中で「要確認」としている（2026-11-24 再確認）。"
             "店名を出しているのは公式サイトで営業時間を確かめた店だけ（いなさ・ひいなの湯・休暇村紀州加太・加太海月・らぴゅカフェ）。"
             "各スポットの「おすすめ訪問時間」は11月下旬・木曜のダイヤの時間割。このファイルは scripts/build_tomogashima_data.py で作る（直接直さない）。")


def build(c):
    cs = c["spots"]
    spots = []
    for i, sid in enumerate(c["order"], 1):
        b, o = S[sid], cs.get(sid, {})
        parts = [b["title"], o.get("pre"), b["body"], o.get("post")]
        tm = o["time"]
        text = {}
        lead = {"ja": "おすすめ到着時間：" if sid in ("kadaeki", "port", "nonaura") else "おすすめ出発時間：" if sid == "kadaeki2" else "おすすめ訪問時間：",
                "en": "Recommended arrival: " if sid in ("kadaeki", "port", "nonaura") else "Recommended departure time: " if sid == "kadaeki2" else "Recommended visit time: "}
        for lang in ("ja", "en"):
            text[lang] = "\n\n".join(p[lang] for p in parts if p) + "\n\n" + lead[lang] + tm[lang]
        out = {"no": i, "id": sid, "name": b["name"], "kind": b["kind"], "blurb": o.get("blurb") or b["blurb"], "lat": b["lat"], "lng": b["lng"]}
        if b.get("caution"):
            out["caution"] = b["caution"]
        out["text"] = text
        out["gmaps"] = b["gmaps"]
        out["links"] = b["links"]
        out["info"] = info(o.get("rows", []) + b.get("rows", []), tip=b["tip"], cash=b.get("cash", False), source=b.get("source"), checked=b.get("checked"))
        out["photos"] = photos(sid)
        out["notices"] = b.get("notices", [])
        spots.append(out)
    NO = {s["id"]: s["no"] for s in spots}
    data = {
        "id": "tomogashima", "course": c["id"],
        "_note": NOTE_HEAD + c["file"] + "。" + NOTE_TAIL,
        "sections": [{"first": NO[a], "last": NO[b], "area": T(aj, ae), "title": T(tj, te)} for a, b, aj, ae, tj, te in c["sections"]],
        "focus": {"first": NO["nonaura"], "last": NO["dai2"]},
        "plan": {"_note": "「選んで回る」の設定。駅・港・桟橋はいつも入る。島の中と淡嶋神社は選べる。",
                 "picks": sorted(NO[k] for k in ("dai3", "takanosu", "kosuke", "toudai", "dai2", "awashima")),
                 "auto": {str(NO[k]): {"always": True} for k in ("kadaeki", "port", "nonaura", "kadaeki2")},
                 "hints": []},
        "photoBase": "../images/tomogashima/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


assert set(LATE["order"]) == set(EARLY["order"]) == set(S)
for c in (LATE, EARLY):
    build(c)
