#!/usr/bin/env python3
"""大津 三井寺と琵琶湖疏水の夜桜のデータ（data/routes/miidera.json）を書き出す。

使い方: python3 scripts/build_miidera_data.py  （そのあと python3 scripts/sync_miidera.py）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）。
  紹介ページ・使い方の文章は miidera/js/i18n.js（時刻を直すときは両方）
- 写真は images/miidera/<スポットのid>-<番号>.jpg を番号の順に全部使う（足していない）
- 2026-11-23 オーナーの基準で作り直した（ゲストが実際に回れる1日）:
  - 起点は京都の中心・三条のあたり。三条京阪17:16発 → 三井寺17:46着（土日祝17:42）→ 18:00の夜の受付 → 大門 → 金堂 →
    三重塔 → 観音堂 → 琵琶湖疏水 → 20:39発 → 三条京阪21:08着（土日祝21:07）→ 祇園白川か円山公園の夜桜（22:00まで）か晩ごはん
  - 疏水は最後に回した（春分すぎの日没は18:12〜18:26で、点灯直後はまだ明るい。帰り道にあり、無料で21:30まで）。
    これで番号の順が変わったので、「行った」印の保存キーを変えた（scripts/sync_miidera.py）
  - 昼から来る人の過ごし方（坂本→昼の三井寺→逢坂山かねよ、または疏水船）は1番に文章で。写真のない場所はスポットにしていない
  - コースの切り替えは作っていない（夜の受付と回る順はだれでも同じ。晩ごはんを先に食べる人は約1時間うしろへずらす案内）
  - offSeason: True のお知らせは、春以外に開いたときだけ出る（時期は scripts/sync_miidera.py の SEASON_FROM／SEASON_TO）
- 春の日程・料金は全部「2026年春の実績」、電車は2026年11月のダイヤ。次の春の発表が出たら文章と SOURCES と i18n.js を直す
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/miidera"
OUT = f"{R}/data/routes/miidera.json"
CHECKED = "2026-11-23"
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


def row(kind, ja, en):
    return {"kind": kind, "text": T(ja, en), "until": None, "from": None}


def notice(head_ja, head_en, ja, en, url=None, off_season=False):
    d = {"from": None, "to": None, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}
    if off_season:
        d["offSeason"] = True
    return d


def info(rows, tip, source):
    return {"rows": rows, "cash": False, "tip": tip, "checked": CHECKED, "source": source}


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


def yahoo(fr, to, day, hhmm, kind=1):
    """乗換案内の検索結果の直接のURL（kind: 1=出発, 2=終電）"""
    q = {"from": fr, "to": to, "y": day[:4], "m": day[4:6], "d": day[6:], "hh": hhmm[:2], "m1": hhmm[2], "m2": hhmm[3],
         "type": kind, "ticket": "normal", "expkind": 1, "ws": 3, "s": 0}
    return "https://transit.yahoo.co.jp/search/result?" + urllib.parse.urlencode(q)


# ---------------------------------------------------------------------------
# 出典
# ---------------------------------------------------------------------------
LIGHT = "https://miidera1200.jp/2026lightup-spring/"
INFO = "https://miidera1200.jp/information"
TOUR = "https://miidera1200.jp/recommended_route"
OTSU = "https://otsu.or.jp/tripideas/otsu-sakura/"
OTSU_EVENT = "https://web.archive.org/web/20260419150522/https://otsu.or.jp/event/sakuranobiwakososui2026"
OTSU_LEAFLET = "https://otsu.or.jp/wp/wp-content/uploads/2025/12/biwako-otsu-04_260220.pdf"
BOAT = "https://biwakososui.kyoto.travel/information/"
BOAT_2026 = "https://web.archive.org/web/20260212130255/https://biwakososui.kyoto.travel/information/"
BOAT_ACCESS = "https://biwakososui.kyoto.travel/information/access.html"
BOAT_DOCK = "https://biwakososui.kyoto.travel/pdf/pamphlet.pdf"
BOAT_EVENT = "https://ja.kyoto.travel/event/single.php?event_id=6185"
KANEYO = "https://kaneyo.in/"
TSURUYA = "https://www.tsurukisoba.com/"
HIYOSHI = "https://hiyoshitaisha.jp/"
NIGHT_NAVI = "https://ja.kyoto.travel/times/night/article/single.php?id=472"
SUN_MAR = "https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s2603.html"
SUN_APR = "https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s2604.html"
WEEKDAY, HOLIDAY = "20261202", "20261205"    # 調べた日（水曜・土曜）

L_YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
L_LIGHT = link("official", "三井寺 春のライトアップ2026（公式・終了した回）", "Miidera spring illumination 2026 (official, now over; Japanese)", LIGHT)
L_INFO = link("official", "三井寺 昼の拝観案内（公式）", "Miidera daytime visits (official, Japanese)", INFO)
L_TOUR = link("official", "三井寺 境内の回り方（公式）", "Miidera: walking the precinct (official)", TOUR)
L_OTSU = link("official", "三井寺と疏水の桜（びわ湖大津観光協会）", "Miidera and canal cherries (Otsu tourism, Japanese)", OTSU)
L_KANEYO = link("official", "逢坂山かねよ（時間・休み）", "Osakayama Kaneyo: hours and closing days (Japanese)", KANEYO)
L_TSURUYA = link("official", "手打蕎麦 鶴屋喜八（時間・休み）", "Tsuruya Kihachi soba: hours and closing days (Japanese)", TSURUYA)
L_BOAT = link("official", "びわ湖疏水船（日程・料金・予約）", "Lake Biwa Canal boat: dates, fares, booking", BOAT, "https://biwakososui.kyoto.travel/en/")
L_HIEI = link("info", "比叡山と坂本のマップ（日吉大社・石垣の町）", "Mt. Hiei & Sakamoto map (Hiyoshi Taisha, the stone-walled town)", "../hieizan/#list")
L_EIZAN = link("info", "叡山電鉄のマップ（夜の祇園四条・先斗町は24〜26番）", "Eizan Railway map (evening stops 24–26)", "../eizan-line/#list")
L_NAVI = link("info", "2026年春の京都の夜桜（京都観光Navi・終了した回）", "Kyoto evening cherries, spring 2026 (now over; Japanese)", NIGHT_NAVI)

# ---------------------------------------------------------------------------
# お知らせ
# ---------------------------------------------------------------------------
N_OFF = notice(
    "春のライトアップは、いまはやっていません", "The spring light-up isn’t on now",
    "春の約3週間の夜だけに使うマップです。2026年の回は4月12日で終わりました。来春の日程・料金は未発表なので要確認です。",
    "This map is only for about three weeks of spring evenings. The 2026 run ended on 12 April. Next spring’s dates and fees haven’t been announced, so please check.",
    url=LIGHT, off_season=True)
N_ENTRY = notice(
    "夜の受付は18:00〜21:00（2026年春の実績）", "Evening entry 18:00–21:00 (as in spring 2026)",
    "2026年は3月25日〜4月12日、18:00〜21:30。大人1,500円・小中高生700円で、昼の入山料800円とは別でした。全部見るなら19:30までに大門へ。来春は要確認。支払い方法も公式に書かれていないので、現金も持っていくと安心です。",
    "In 2026 it ran 25 March – 12 April, 18:00–21:30, at ¥1,500 (¥700 for school pupils), separate from the ¥800 daytime ticket. Be at the Daimon by 19:30 to see it all. Please check for next spring. Payment methods aren’t stated, so carry cash too.",
    url=LIGHT)
N_TRAIN = notice(
    "地下鉄は「びわ湖浜大津」行きに", "Take the train for Biwako-Hamaotsu",
    "東西線の「六地蔵」行きは大津へ行きません。京都市役所前から乗ると540円、三条京阪からは520円です。",
    "Tozai-line trains for Rokujizo don’t go to Otsu. It’s ¥540 from Kyoto Shiyakusho-mae, ¥520 from Sanjo Keihan.",
    url=yahoo("三条京阪", "三井寺", WEEKDAY, "1715"))
N_STEPS = notice(
    "暗い石段があります", "Dark stone steps",
    "観音堂は高台です。歩きやすい靴で。夜に使える下り道と出口は毎年の案内で要確認。分からなければ受付で聞いてから上がってください。",
    "The Kannon hall is on high ground, so wear good shoes. Please check which paths and exits are open at night; ask at the entrance before you climb.")
N_CANAL = notice(
    "疏水の点灯も21:30まで（2026年春の実績）", "Canal lights off at 21:30 (as in spring 2026)",
    "無料ですが、三井寺と同じ時刻に消えます。20時半を過ぎて着いた人は、疏水とお寺のどちらかに絞ってください。住宅街なので静かに。来春は要確認。",
    "It’s free, but the lights go off at the same time as the temple’s. If you arrive after 20:30, choose either the canal or the temple. People live here, so keep quiet. Please check for next spring.",
    url=OTSU)
N_LAST = notice(
    "最終は三井寺23:17発", "Last train from Miidera 23:17",
    "びわ湖浜大津で乗り換えて三条京阪23:49着。平日・土日祝とも同じです（2026年11月のダイヤ。来春は要確認）。",
    "Change at Biwako-Hamaotsu for Sanjo Keihan at 23:49, the same every day (November 2026 timetable; please check for next spring).",
    url=yahoo("三井寺", "三条京阪", WEEKDAY, "2359", 2))

CAUTION = T("春の夜だけ（2026年は3/25〜4/12。来春は要確認）", "Spring evenings only (25 Mar – 12 Apr in 2026; check for next spring)")
NIGHT = row("hours", "夜：18:00〜21:30、受付21:00まで（2026年春の実績。来春は要確認）",
            "Evening: 18:00–21:30, last entry 21:00 (spring 2026; please check for next spring)")
NIGHT_FEE = row("fee", "夜：大人1,500円、小中高生700円（2026年春の実績。来春は要確認）",
                "Evening: ¥1,500 adults, ¥700 school pupils (spring 2026; please check for next spring)")
TIP_TEMPLE = T("夜の日程・料金は2026年春の公式ページの数字です。来春のものではありません。",
               "Evening dates and fees are from the official spring 2026 page, not for next spring.")
SRC_TEMPLE = f"三井寺 春のライトアップ2026 {LIGHT}、拝観案内 {INFO}。{CHECKED}に確認"

# ---------------------------------------------------------------------------
# スポット（番号は並び順）
# ---------------------------------------------------------------------------
S = [
    dict(id="daimon", name=T("三井寺 大門（仁王門）", "Miidera Daimon (Nio gate)"), kind=T("門・夜の受付", "Gate & evening entrance"),
         blurb=T("夜はここから。三条京阪17:16発で、18:00の受付に間に合います。昼から来る人の過ごし方も、ここに。",
                 "The evening starts here: the 17:16 from Sanjo Keihan gets you there for 18:00 entry. Plans for coming earlier in the day are here too."),
         caution=CAUTION, lat=35.01345, lng=135.85455,
         text=T("三井寺（みいでら）・園城寺（おんじょうじ）の大門\n\n"
                "天台寺門宗の総本山で、千本を超える桜があります。大門は徳川家康が寄進した門で、仁王像は室町時代のものです。\n\n"
                "三条からの行き方\n"
                "・三条京阪17:16発の「びわ湖浜大津」行き → 終点で乗り換え → 三井寺17:46着（土日祝は17:42着）。520円。\n"
                "・京都市役所前からは同じ電車が17:14発。540円。\n"
                "・京都駅からはJRで17:23発 → 膳所で京阪に乗り換え → 17:46着（土日祝17:52着）。440円。\n"
                "・遅れたら三条京阪17:31発（18:01着）。18:23発（土日祝18:28発）の18:54着でも、ひと通り見られます。\n"
                "駅から疏水に沿って歩いて10〜15分。疏水の桜は帰りに暗くなってから見るので、行きは下見だけにします。\n\n"
                "9時台に出て、1日大津で過ごすなら\n"
                "・9:33 三条京阪発（土日祝9:41発）→ 10:14 坂本比叡山口着（10:22着）。620円。\n"
                "・10:35 日吉大社（500円）、石垣の町を散歩。2026年は4月12〜14日が山王祭でした。\n"
                "・12:15 手打蕎麦 鶴屋喜八でお昼（11:00〜16:00、ラストオーダー15:30。休みは公式の一覧で）。\n"
                "・13:49 坂本発 → 14:02 三井寺着。280円。\n"
                "・14:15 昼の三井寺（800円。夜とは別料金）。境内の CaFe KanOn は16:00まで・火曜休み、ながら茶房 本寿院は16:30まで・木曜休み（2026年春）。16:10には出ます。\n"
                "・16:33 三井寺発（土日祝16:34発）→ 16:46 大谷着。駅から約50mの逢坂山かねよで、17:00から晩ごはん（うなぎ）。\n"
                "・18:24 大谷発 → 18:39 三井寺着（土日祝18:34着）。大門18:55、金堂19:15、三重塔19:45、観音堂20:05、疏水20:45、三井寺21:17発（土日祝21:18発）→ 三条京阪21:49着。\n"
                "昼の拝観料を払わないなら、坂本に長くいて、15時台に大津港の湖岸でひと休みしてから大谷へ。比叡山の上まで行く人は、京都側へ下りずに坂本へ戻ってください。\n\n"
                "昼すぎに出るなら、疏水船\n"
                "蹴上から三井寺へトンネルをくぐって上る、完全予約制の船です。2026年春の三井寺便は、上り4便が蹴上14:25集合 → 三井寺15:45解散、片道6,000〜9,000円（日によって違う）でした。三条京阪14:04発で蹴上14:07着、乗り場まで歩いて5分。下りたあとは16:33発（土日祝16:34発）で、上と同じ晩ごはんへ。大津港へ着く日は時刻が違います。来春の日程・時刻・料金は要確認。\n\n"
                "晩ごはんの注意\n"
                "逢坂山かねよは11:00〜20:00。本店は木曜、レストランは火曜が休みで、ほかに月1回不定休。14〜17時は中休みのことがあり、予約は本店だけ（電話）。ラストオーダーは要確認。夕方に京都を出る人は、軽く食べてから電車に乗るか、三条に戻って21時すぎに。\n\n"
                "おすすめ訪問時間：18:00〜18:15",
                "Miidera (Onjoji): the Daimon gate\n\n"
                "The head temple of the Tendai Jimon school has more than a thousand cherry trees. The Daimon was given by Tokugawa Ieyasu, and its guardian statues date from the Muromachi era.\n\n"
                "Getting here from Sanjo\n"
                "・17:16 from Sanjo Keihan on the train for Biwako-Hamaotsu, change at the end of the line, Miidera 17:46 (17:42 on weekends and holidays). ¥520.\n"
                "・The same train leaves Kyoto Shiyakusho-mae at 17:14. ¥540.\n"
                "・From Kyoto Station: JR at 17:23, change to Keihan at Zeze, arriving 17:46 (17:52 on weekends and holidays). ¥440.\n"
                "・Running late: the 17:31 (arrives 18:01). Even the 18:23 (18:28 on weekends and holidays), arriving 18:54, leaves time for the whole route.\n"
                "It’s 10–15 minutes on foot along the canal. Just take a first look on the way: you’ll see its cherries on the way back, once it’s dark.\n\n"
                "Leaving around 9:30 for a whole day in Otsu\n"
                "・9:33 from Sanjo Keihan (9:41 weekends and holidays) → Sakamoto-Hieizanguchi 10:14 (10:22). ¥620.\n"
                "・10:35 Hiyoshi Taisha (¥500) and the stone-walled lanes. The Sanno festival fell on 12–14 April in 2026.\n"
                "・12:15 soba at Tsuruya Kihachi (11:00–16:00, last order 15:30; closing days on its website).\n"
                "・13:49 from Sakamoto → Miidera 14:02. ¥280.\n"
                "・14:15 Miidera by day (¥800, separate from the evening). In the grounds, CaFe KanOn serves until 16:00 (closed Tue) and Nagara Sabo Honjuin until 16:30 (closed Thu), as in spring 2026. Leave by 16:10.\n"
                "・16:33 from Miidera (16:34 weekends and holidays) → Otani 16:46. Eel for an early dinner from 17:00 at Osakayama Kaneyo, about 50 m from the station.\n"
                "・18:24 from Otani → Miidera 18:39 (18:34 weekends and holidays). Daimon 18:55, main hall 19:15, pagoda 19:45, Kannon hall 20:05, canal 20:45, train 21:17 (21:18 weekends and holidays) → Sanjo Keihan 21:49.\n"
                "To skip the daytime ticket, stay longer in Sakamoto and rest by the lake at Otsu Port around 15:00–16:00 before going to Otani. If you go up Mt. Hiei, come back down on the Sakamoto side, not the Kyoto side.\n\n"
                "Leaving after lunch: the canal boat\n"
                "A reservation-only boat climbs from Keage through the tunnels to Miidera. In spring 2026 the fourth upstream Miidera boat met at Keage at 14:25 and finished at Miidera at 15:45, ¥6,000–9,000 one way depending on the day. The 14:04 from Sanjo Keihan reaches Keage at 14:07, 5 minutes from the dock. Afterwards take the 16:33 (16:34 weekends and holidays) to the same dinner. Times differ on days the boats run to Otsu Port. Please check next spring’s dates, times and fares.\n\n"
                "About dinner\n"
                "Osakayama Kaneyo is open 11:00–20:00. The main house closes Thursdays and the restaurant Tuesdays, plus one irregular day a month. It may shut 14:00–17:00, and only the main house takes bookings (by phone). Last order isn’t stated. If you leave Kyoto in the evening, have a snack before the train or eat back in Sanjo after 21:00.\n\n"
                "Recommended visit time: 18:00–18:15"),
         gmaps=[gm("三井寺 大門", "Miidera Daimon", 35.01345, 135.85455, "三井寺 大門 仁王門"),
                gm("京阪 三井寺駅", "Keihan Miidera Station", 35.01250, 135.85930, "京阪 三井寺駅"),
                gm("逢坂山かねよ（晩ごはん）", "Osakayama Kaneyo (dinner)", 34.99431, 135.85427, "逢坂山かねよ 大津市大谷町23-15")],
         links=[L_LIGHT, L_INFO, L_YAHOO, L_HIEI, L_TSURUYA, L_BOAT, L_KANEYO],
         notices=[N_OFF, N_ENTRY, N_TRAIN],
         info=info([NIGHT, NIGHT_FEE,
                    row("train", "行き：三条京阪17:16発 → 17:46着（土日祝17:42着）・520円。京都市役所前17:14発・540円",
                        "Out: Sanjo Keihan 17:16 → 17:46 (17:42 weekends and holidays), ¥520. Kyoto Shiyakusho-mae 17:14, ¥540"),
                    row("day", "9:00〜16:30（受付16:00まで）、大人800円・中高生500円・小学生300円。夜とは別",
                        "9:00–16:30 (last entry 16:00), ¥800 adults, ¥500 junior and senior high, ¥300 elementary. Separate from the evening"),
                    row("meal", "逢坂山かねよ 11:00〜20:00（中休みのことあり）。本店は木曜、レストランは火曜休み＋月1回不定休",
                        "Osakayama Kaneyo 11:00–20:00 (may close mid-afternoon). Main house closed Thu, restaurant Tue, plus one day a month")],
                   T("夜の日程・料金と疏水船は2026年春の実績、電車は2026年11月のダイヤです。来春は要確認。",
                     "Evening dates and fees and the boat are from spring 2026; trains are the November 2026 timetable. Please check for next spring."),
                   SRC_TEMPLE + f"。電車は乗換案内、疏水船 {BOAT_2026}、かねよ {KANEYO}")),

    dict(id="kondo", name=T("金堂と三井の晩鐘", "Main hall & the Evening Bell of Mii"), kind=T("国宝・桜", "National Treasure & cherries"),
         blurb=T("国宝の金堂と桜並木。日が沈んで空が青から黒に変わるころ、照明の色が出てきます。",
                 "The National Treasure main hall and its cherry avenue. The colours of the lights come up as the sky turns from blue to black."),
         caution=CAUTION, lat=35.01339, lng=135.85286,
         text=T("金堂（こんどう）と三井の晩鐘（みいのばんしょう）\n\n"
                "大門から参道を進むと、桃山時代に建てられた国宝の金堂です。大津の日没は、3月25日で18:12、4月12日で18:26ごろ。18時に入ってもしばらくは明るいので、ここで暗くなるのを待ちます。参道の桜がピンクや紫に変わるのはそれからです。\n\n"
                "金堂の南東の鐘楼が、近江八景のひとつ「三井の晩鐘」。金堂のすぐ西の閼伽井屋（あかいや）には、今も音を立てて水が湧きます。天智・天武・持統の3人の天皇が産湯に使ったと伝わり、「三井寺」の名前のもとになった泉です。その奥の霊鐘堂には「弁慶の引摺り鐘」があります。比叡山へ引きずり上げて撞いたら「イノー（帰りたい）」と響いたので、谷へ投げ捨てたという鐘です。\n\n"
                "夜に堂内や霊鐘堂へ入れるか、鐘を撞けるかは要確認です。\n\n"
                "おすすめ訪問時間：18:20〜18:50",
                "Main hall & the Evening Bell of Mii\n\n"
                "The approach from the Daimon leads to the National Treasure main hall, built in the Momoyama period. The sun sets in Otsu around 18:12 on 25 March and 18:26 on 12 April, so it’s still light for a while after 18:00. Wait for dark here: that’s when the avenue turns pink and violet.\n\n"
                "The belfry south-east of the hall holds the “Evening Bell of Mii”, one of the Eight Views of Omi. Just west of the hall, the little Akaiya covers a spring you can hear bubbling. Three emperors are said to have had their first bath in its water, which gave Miidera its name. Behind it is the bell Benkei is said to have dragged up Mt. Hiei and thrown into a valley when it moaned “ino” (I want to go home).\n\n"
                "Please check whether the halls can be entered, or the bell rung, in the evening.\n\n"
                "Recommended visit time: 18:20–18:50"),
         gmaps=[gm("三井寺 金堂", "Miidera main hall", 35.01339, 135.85286, "三井寺 金堂")],
         links=[L_LIGHT, L_TOUR],
         notices=[N_OFF, N_ENTRY],
         info=info([NIGHT, NIGHT_FEE], TIP_TEMPLE, SRC_TEMPLE + f"。由来 {TOUR}、日没 {SUN_MAR}・{SUN_APR}")),

    dict(id="sanju", name=T("唐院・三重塔", "Toin & three-storey pagoda"), kind=T("塔", "Pagoda"),
         blurb=T("夜空に黒く立つ三重塔と、そのまわりの桜。", "The three-storey pagoda dark against the night sky, among the cherries."),
         caution=CAUTION, lat=35.01257, lng=135.85221,
         text=T("唐院（とういん）・三重塔\n\n"
                "金堂から歩いて3〜5分。唐院は、三井寺の今の基礎を築いた智証大師・円珍をまつる場所です。奥の三重塔は奈良の寺から移された重要文化財で、空が暗くなってから来ると、影がくっきり出ます。\n\n"
                "ここから観音堂へは南東へ歩いて10分ほど。最後は石段です。\n\n"
                "おすすめ訪問時間：18:55〜19:05",
                "Toin & three-storey pagoda\n\n"
                "3–5 minutes from the main hall. The Toin honours Enchin, who laid the foundations of Miidera as it is today. The pagoda behind it was moved from a temple in Nara and is an Important Cultural Property; its silhouette is sharpest once the sky is dark.\n\n"
                "The Kannon hall is about 10 minutes south-east, with steps at the end.\n\n"
                "Recommended visit time: 18:55–19:05"),
         gmaps=[gm("三井寺 三重塔", "Miidera pagoda", 35.01257, 135.85221, "三井寺 三重塔")],
         links=[L_LIGHT, L_TOUR],
         notices=[N_OFF, N_ENTRY],
         info=info([NIGHT], TIP_TEMPLE, SRC_TEMPLE + f"。由来 {TOUR}")),

    dict(id="kannondo", name=T("観音堂と大津の夜景", "Kannon hall & the lights of Otsu"), kind=T("お堂・展望", "Hall & view"),
         blurb=T("境内の南の高台。観音堂の屋根ごしに、大津の町のあかりが見下ろせます。",
                 "High ground at the south of the precinct, looking over the Kannon hall’s roofs to the lights of Otsu."),
         caution=CAUTION, lat=35.01038, lng=135.85493,
         text=T("観音堂（かんのんどう）と大津の夜景\n\n"
                "西国三十三所の第14番札所です。1枚目の写真は、観音堂の広場より一段高いところから撮ったもの。お堂の屋根ごしに町のあかりが見え、琵琶湖は夜には黒く沈みます。\n\n"
                "ここから疏水の大津閘門までは、大門へ戻る道でも歩いて20分みておけば着きます。19:40には下りはじめてください。隣の CaFe KanOn は昼だけです。\n\n"
                "おすすめ訪問時間：19:15〜19:40",
                "Kannon hall & the lights of Otsu\n\n"
                "No. 14 of the Saigoku 33-temple pilgrimage. The first photo is from a level above the forecourt, over the roofs to the city lights; at night the lake is just darkness beyond.\n\n"
                "Allow 20 minutes to the Otsu lock on the canal, even going back by the Daimon. Start down by 19:40. CaFe KanOn next door is daytime only.\n\n"
                "Recommended visit time: 19:15–19:40"),
         gmaps=[gm("三井寺 観音堂", "Miidera Kannon hall", 35.01038, 135.85493, "三井寺 観音堂")],
         links=[L_LIGHT],
         notices=[N_OFF, N_STEPS, N_ENTRY],
         info=info([NIGHT], TIP_TEMPLE, SRC_TEMPLE)),

    dict(id="sosui", name=T("琵琶湖疏水の夜桜", "Cherries on the Lake Biwa Canal at night"), kind=T("桜並木（無料）", "Cherry avenue (free)"),
         blurb=T("帰り道の仕上げに。暗くなった水路の両岸に、照らされた桜が続きます。帰りの電車と京都の夜もここに。",
                 "The finish, on your way back: lit cherries along both banks of the dark waterway. Trains home and the evening in Kyoto are here too."),
         caution=CAUTION, lat=35.01212, lng=135.85744,
         text=T("琵琶湖疏水（びわこそすい）の夜桜\n\n"
                "明治時代に琵琶湖の水を京都へ引いた水路です。大津閘門から第一トンネル（第一隧道）まで、両岸に桜が並びます。第一トンネルは2025年に国宝になりました。お寺より先に見ても点灯したばかりでまだ明るいので、帰りに見ます。写真は2026年4月2日の夜。\n\n"
                "三条へ帰る\n"
                "三井寺駅まで歩いて5分。\n"
                "・基本：20:39発 → 三条京阪21:08着（土日祝21:07着）。\n"
                "・早めに：20:18発（土日祝20:11発）→ 20:47着。\n"
                "・遅くなったら：20:59発（土日祝20:58発）→ 21:29着、21:37発（土日祝21:38発）→ 22:08着。\n"
                "・最終：23:17発 → 23:49着。\n"
                "どれもびわ湖浜大津で乗り換え、520円。京都駅へは20:39発 → 京阪膳所でJRに乗り換え → 21:06着（土日祝21:03着）、440円。京都駅への最終は23:23発 → 大津京で乗り換え → 23:56着。\n\n"
                "京都に戻ってからの夜\n"
                "・もう少し夜桜：三条京阪から祇園白川へ歩いて10分弱で、21:20ごろから。しだれ桜の円山公園までなら、さらに10〜15分です。2026年春は祇園白川が3月27日〜4月5日、円山公園が3月24日〜4月8日、どちらも18:00〜22:00・無料でした。日にちが三井寺より短いので、来春の日程は要確認。\n"
                "・晩ごはん：三条から木屋町・先斗町へ歩いてすぐです。21時すぎに着くので、ラストオーダーを先に見ておいてください。夜桜と両方なら、ごはんを先に済ませてから大津へ。\n\n"
                "おすすめ訪問時間：20:00〜20:30",
                "Cherries on the Lake Biwa Canal at night\n\n"
                "The Meiji-era waterway that carries lake water to Kyoto, lined with cherries from the Otsu lock to the first tunnel, a National Treasure since 2025. Before the temple it’s still too light, so see it on the way back. Photos from the night of 2 April 2026.\n\n"
                "Back to Sanjo\n"
                "Miidera Station is 5 minutes on foot.\n"
                "・The plan: 20:39 → Sanjo Keihan 21:08 (21:07 weekends and holidays).\n"
                "・Earlier: 20:18 (20:11 weekends and holidays) → 20:47.\n"
                "・Later: 20:59 (20:58 weekends and holidays) → 21:29, or 21:37 (21:38) → 22:08.\n"
                "・Last train: 23:17 → 23:49.\n"
                "All change at Biwako-Hamaotsu, ¥520. For Kyoto Station, the 20:39 connects to JR at Keihan-Zeze, arriving 21:06 (21:03 weekends and holidays), ¥440. The last train for Kyoto Station is the 23:23 via Otsukyo, arriving 23:56.\n\n"
                "The evening back in Kyoto\n"
                "・More night cherries: Gion Shirakawa is under 10 minutes’ walk from Sanjo Keihan, so you’re there by about 21:20; Maruyama Park’s weeping cherry is another 10–15 minutes. In spring 2026 Shirakawa was lit 27 March – 5 April and Maruyama 24 March – 8 April, both 18:00–22:00 and free. They end earlier in the season than Miidera, so please check next spring’s dates.\n"
                "・Dinner: Kiyamachi and Pontocho are a short walk from Sanjo. You arrive after 21:00, so check last orders first. To fit in both, eat before you go to Otsu.\n\n"
                "Recommended visit time: 20:00–20:30"),
         gmaps=[gm("琵琶湖疏水 大津閘門", "Lake Biwa Canal, Otsu lock", 35.01212, 135.85744, "琵琶湖疏水 大津閘門"),
                gm("京阪 三井寺駅", "Keihan Miidera Station", 35.01250, 135.85930, "京阪 三井寺駅"),
                gm("祇園白川", "Gion Shirakawa", 35.00560, 135.77390, "祇園白川 巽橋")],
         links=[L_OTSU, L_YAHOO, L_NAVI, L_EIZAN],
         notices=[N_OFF, N_CANAL, N_LAST],
         info=info([row("hours", "18:00〜21:30点灯（2026年3月25日〜4月12日の実績。来春は要確認）", "Lit 18:00–21:30 (25 Mar – 12 Apr 2026; please check for next spring)"),
                    row("fee", "無料", "Free"),
                    row("train", "帰り：三井寺20:39発 → 三条京阪21:08着（土日祝21:07着）・520円。最終23:17発 → 23:49着",
                        "Return: Miidera 20:39 → Sanjo Keihan 21:08 (21:07 weekends and holidays), ¥520. Last 23:17 → 23:49")],
                   T("点灯と京都の夜桜は2026年春の実績、電車は2026年11月のダイヤです。来春は要確認。",
                     "Light-up details are from spring 2026; trains are the November 2026 timetable. Please check for next spring."),
                   f"びわ湖大津観光協会 {OTSU}、{OTSU_EVENT}。京都観光Navi {NIGHT_NAVI}。電車は乗換案内。{CHECKED}に確認")),
]


# ---------------------------------------------------------------------------
# 出典（データの sources に入る）
# ---------------------------------------------------------------------------
def src(what, url):
    return {"what": what, "url": url, "checked": CHECKED}


def trains(what, fr, to, hhmm, weekday, holiday, kind=1):
    """平日と土曜の検索結果を1行ずつ"""
    return [src(f"{what}（平日 2026-12-02）：{weekday}", yahoo(fr, to, WEEKDAY, hhmm, kind)),
            src(f"{what}（土曜 2026-12-05）：{holiday}", yahoo(fr, to, HOLIDAY, hhmm, kind))]


SOURCES = [
    src("三井寺 春のライトアップ2026：3/25〜4/12、18:00〜21:30（受付21:00）、夜1,500円・小中高生700円、昼9:00〜16:30・800円、CaFe KanOn 10:30〜16:00 火休み、ながら茶房 本寿院 10:00〜16:30 木休み。来春は未発表", LIGHT),
    src("三井寺 昼の拝観：9:00〜16:30（受付16:00）、大人800円・中高生500円・小学生300円、年中無休", INFO),
    src("三井寺 境内：駅から仁王門まで歩いて10分、大門の由来、閼伽井屋、引摺り鐘、三重塔", TOUR),
    src("三井寺と疏水の桜：疏水の両岸のライトアップ、第一隧道は2025年に国宝", OTSU),
    src("桜の琵琶湖疏水 2026：3/25〜4/12、18:00〜21:30点灯、観覧無料、住宅街の注意（公式ページの2026-04-19の保存。元のページは削除済み）", OTSU_EVENT),
    src("2026年春の大津の催し：山王祭 4/12〜14", OTSU_LEAFLET),
    src("疏水船 2026年春：3/26〜6/14のうち63日、予約は2/25から。大津港便は8日間", BOAT_EVENT),
    src("疏水船 2026年春の三井寺便：上り4便 蹴上14:25集合→三井寺15:45解散、片道6,000〜9,000円（公式ページの2026-02-12の保存。いまのページは秋の分）", BOAT_2026),
    src("疏水船の乗り場：蹴上駅1番出口から歩いて約5分", BOAT_ACCESS),
    src("疏水船の乗り場：三井寺駅から歩いて約4分", BOAT_DOCK),
    src("逢坂山かねよ：11:00〜20:00、本店は木曜・レストランは火曜休み＋月1回不定休、14〜17時に中休みの場合あり、予約は本店のみ電話、大谷駅から約50m", KANEYO),
    src("手打蕎麦 鶴屋喜八：11:00〜16:00（L.O.15:30）、休みは日付の一覧", TSURUYA),
    src("日吉大社：参拝9:00〜16:00・大人500円（比叡山のマップと同じ出典）", HIYOSHI),
    src("祇園白川 3/27〜4/5、円山公園 3/24〜4/8、どちらも18:00〜22:00・無料（2026年の実績）", NIGHT_NAVI),
    src("大津の日没 2027-03-25 18:12", SUN_MAR),
    src("大津の日没 2027-04-12 18:26", SUN_APR),
    src("歩く時間（OpenStreetMap の徒歩ルートの目安。文章では長めに）：駅→大門11分、大門→金堂3分、金堂→塔2分、塔→観音堂6分、観音堂→大門5分、観音堂→大津閘門6分、閘門→駅4分、三条京阪→祇園白川7分、白川→円山公園9分", "https://routing.openstreetmap.de/"),
    *trains("行き", "三条京阪", "三井寺", "1715", "17:16→17:46、17:31→18:01、520円", "17:16→17:42、17:31→18:01、520円"),
    *trains("遅い行き", "三条京阪", "三井寺", "1810", "18:23→18:54、520円", "18:28→18:54、520円"),
    *trains("京都市役所前から", "京都市役所前", "三井寺", "1700", "17:14→17:46、540円", "17:14→17:42、540円"),
    *trains("京都駅から", "京都", "三井寺", "1715", "17:23→17:46（膳所で乗り換え）、440円", "17:23→17:52、440円"),
    *trains("昼：坂本へ", "三条京阪", "坂本比叡山口", "0925", "9:33→10:14、620円", "9:41→10:22、620円"),
    *trains("昼：坂本から", "坂本比叡山口", "三井寺", "1340", "13:49→14:02、280円", "13:49→14:02、280円"),
    *trains("昼：疏水船へ", "三条京阪", "蹴上", "1358", "14:04→14:07、220円", "14:04→14:07、220円"),
    *trains("晩ごはんへ", "三井寺", "大谷(滋賀県)", "1630", "16:33→16:46、200円", "16:34→16:46、200円"),
    *trains("晩ごはんから", "大谷(滋賀県)", "三井寺", "1820", "18:24→18:39、200円", "18:24→18:34、200円"),
    *trains("帰り・早め", "三井寺", "三条京阪", "2010", "20:18→20:47、520円", "20:11→20:47、520円"),
    *trains("帰り・基本", "三井寺", "三条京阪", "2036", "20:39→21:08、20:59→21:29、520円", "20:39→21:07、20:58→21:29、520円"),
    *trains("帰り・晩ごはんを先に食べた日", "三井寺", "三条京阪", "2108", "21:17→21:49、21:37→22:08、520円", "21:18→21:49、21:38→22:08、520円"),
    *trains("帰りの最終", "三井寺", "三条京阪", "2359", "23:17→23:49、520円", "23:17→23:49、520円", 2),
    *trains("京都駅へ", "三井寺", "京都", "2036", "20:39→21:06、440円", "20:39→21:03、440円"),
    *trains("京都駅への最終", "三井寺", "京都", "2359", "23:23→23:56（大津京で乗り換え）、440円", "23:23→23:56、440円", 2),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    spots.append(out)
data = {
    "id": "miidera",
    "_note": "大津 三井寺と琵琶湖疏水の夜桜のルート（miidera/ のページ専用。形は eizan-line.json と同じ）。三条から京阪で、大門→金堂・三井の晩鐘→唐院・三重塔→観音堂→琵琶湖疏水→三条。春のライトアップの期間だけのルート。"
             "写真は Toshi の写真ライブラリから選んだもの（2025年4月11日と2026年4月2日の夜、Nikon D7000 と iPhone。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし。人の顔が近くに写る写真は使っていない）。"
             "春の日程・料金は2026年春の実績、電車は2026年11月のダイヤ（春の改正は未確認）。info.checked は事実情報を確認した日。出典は sources。このファイルは scripts/build_miidera_data.py で作る。",
    "sections": [
        {"first": 1, "last": 4, "area": T("三井寺", "Miidera"), "title": T("18:00〜19:40 大門から金堂・三重塔・観音堂へ", "18:00–19:40 The Daimon, main hall, pagoda and Kannon hall")},
        {"first": 5, "last": 5, "area": T("帰り道", "Way back"), "title": T("20:00〜20:30 暗くなった疏水の桜、20:39の電車で三条へ", "20:00–20:30 The canal in the dark, then the 20:39 to Sanjo")},
    ],
    "photoBase": "../images/miidera/",
    "sources": SOURCES,
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
