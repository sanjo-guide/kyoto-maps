#!/usr/bin/env python3
"""京都 高雄の紅葉（神護寺・西明寺・高山寺）のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_takao_data.py  （そのあと python3 scripts/sync_takao.py）
- 作るもの（COURSES）:
  - data/routes/takao.json … 「9〜10時に出発」（京都市役所前9:25ごろの地下鉄で二条へ→二条駅前9:46のJRバス→終点の栂ノ尾10:26着。
    高山寺→門前の茶屋で早めのお昼→西明寺→高雄橋→午後の神護寺→高雄15:36のバス→北野天満宮か街なかへ→夜は三条・先斗町）
  - data/routes/takao-early.json … 「神護寺の開門に合わせる」（京都市役所前7:16（土日祝7:21）の地下鉄→二条駅前7:36のJRバス→高雄8:14着。
    朝の高雄橋→神護寺9:00→参道の茶屋でひと休み→西明寺→槇ノ尾でお昼→高山寺→栂ノ尾14:34のバス→仁和寺・北野天満宮か街なかへ）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方の一言、「選んで回る」の設定
  - SOURCES … 時刻・料金の出典と確認日（データの sources に入る）
- 出発地は京都の中心・三条のあたり（地下鉄東西線の京都市役所前・三条京阪から二条へ。JRバスは三条を通らないので、二条駅前から乗る）
- 写真は images/takao/ にあるものだけ（足していない）。高山寺は Wikimedia Commons（photos の要素が {file, credit}）
  - オーナーの写真は 2024年11月19日（Nikon D7000 と iPhone）。高山寺はオーナーが行っていない場所なので、文章にも行った日などは書かない
- 2026-11-22 オーナーの基準で作り直した（ゲストが実際に回れる1日。開門コースと9〜10時発コース、お昼の場所と時間、帰りのバス、
  帰りに寄れる場所（仁和寺・北野天満宮は金閣寺〜北野のマップにあるので文章で案内）、街なかの夜）
"""
import copy, json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "takao"
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


def info(rows, source, tip=None, verified=True, cash=False):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED, "source": source}
    if not verified:
        d["verified"] = False
    return d


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


def own(pid, nums):
    return [f"{pid}-{i}.jpg" for i in nums]


PHOTOS = {
    "kiyotaki": own("kiyotaki", [1, 2, 3, 4, 5, 7]),
    "jingoji": own("jingoji", [1, 2, 3, 4, 5, 6, 8]),
    "saimyoji": own("saimyoji", [1, 2, 3, 4, 5, 6, 7, 8]),
    "kosanji": [cc("kosanji-1.jpg", "663highland", "CC BY 2.5", "Sekisuiin Kozanji Kyoto Kyoto06s5s4350.jpg"),
                cc("kosanji-2.jpg", "KimonBerlin", "CC BY-SA 2.0", "Kozan-ji (7069446619).jpg"),
                cc("kosanji-3.jpg", "PlusMinus", "CC BY-SA 3.0", "Kouzanji sandou.jpg"),
                cc("kosanji-4.jpg", "KimonBerlin", "CC BY-SA 2.0", "Kozan-ji (7069445443).jpg")],
}

JR_URL = "https://www.nishinihonjrbus.co.jp/route/kyoto/"
JR_PDF = "https://www.nishinihonjrbus.co.jp/route/kyoto/pdf/jikoku/takaokeihoku_20260401.pdf"
JRBUS = link("timetable", "JRバス 高雄・京北線の時刻表（PDF）", "JR Bus Takao–Keihoku line timetable (PDF, Japanese)", JR_PDF)
CITYBUS = link("timetable", "市バス 停留所ごとの時刻表（京都市交通局）", "Kyoto City Bus timetables by stop (Japanese)", "https://www2.city.kyoto.lg.jp/kotsu/busdia/bustime.htm")
HOSHO = link("info", "高雄保勝会（お食事処の一覧）", "Takao tourist association: places to eat (Japanese)", "https://www.kyo-takao.com/shop/")
MOMIJI = "https://ja.kyoto.travel/flower/momiji/"
KINKAKU = link("info", "金閣寺〜北野のマップ（仁和寺・龍安寺・北野天満宮）", "Kinkaku-ji to Kitano map (Ninna-ji, Ryoan-ji, Kitano Tenmangu)", "../kinkakuji/#list")
EIZAN = link("info", "叡山電鉄のマップ（夜の祇園四条・先斗町は24〜26番）", "Eizan Railway map (evening stops 24–26)", "../eizan-line/#list")

SEASON = notice("紅葉の見ごろは例年11月上旬〜下旬", "Autumn leaves: usually early to late November",
                "京都観光Navi（京都市）の紅葉だよりでは、例年の見ごろは神護寺が11月上旬〜下旬、西明寺が11月10日前後、高山寺が11月中旬〜下旬です。年によって前後するので、行く前に紅葉だよりを見てください。写真は2024年11月19日に撮ったものです。",
                "Kyoto City’s autumn-leaf report gives the usual peak as early to late November at Jingoji, around 10 November at Saimyoji, and mid to late November at Kosanji. It shifts from year to year, so check the report before you go. My photos were taken on 19 November 2024.",
                url=MOMIJI)
AUTUMN_BUS = notice("紅葉の週末は、バスが混みます", "On autumn weekends the buses are busy",
                    "JRバスは、紅葉の季節の週末などに、午前は栂ノ尾行き、午後は京都駅前行きの臨時便を出すことがあります（JRバスの案内）。二条駅前は途中のバス停なので、座れないことがあります。座って行きたい人は、始発の京都駅前から乗ってください（京都駅前から高雄まで約55分）。帰りは、栂ノ尾で始まる便（13:14、13:34、14:34、15:14、16:14発など）なら座りやすいです。",
                    "On autumn weekends JR Bus sometimes adds extra buses: towards Toganoo in the morning, towards Kyoto Station in the afternoon (JR Bus notice). Nijo-eki-mae is a stop along the way, so you may have to stand. If you want a seat, board at the first stop, Kyoto Station (about 55 minutes to Takao). Going back, buses that start at Toganoo (13:14, 13:34, 14:34, 15:14, 16:14 and so on) are easier for a seat.",
                    url=JR_URL, frm="2026-11-01", to="2026-12-06")
WINTER = notice("紅葉が終わったあと（12〜2月）", "After the leaves have gone (December–February)",
                "お寺はふだんどおり開いていますが、茶屋は冬に休む店があります。硯石亭は1・2月が休み、とがの茶屋は木曜が休み（10月20日〜11月30日だけ休みなし）、高雄茶屋は不定休です。お昼を食べる店は、出かける前に高雄保勝会の案内で確かめてください。山あいなので、雪や凍った日は石段に気をつけて。",
                "The temples keep their usual hours, but some teahouses close in winter: Suzuri-ishi-tei is closed in January and February, Togano-chaya on Thursdays (open daily only from 20 October to 30 November), and Takao-chaya closes on irregular days. Check the Takao tourist association’s list before you go to be sure of lunch. In snow or frost, take care on the stone steps.",
                url="https://www.kyo-takao.com/shop/", frm="2026-12-01", to="2027-02-28")

# 帰りのバス（各コースの最後のスポットと、高雄橋のスポットに出す）
BACK_ROWS = [
    row("train", "帰り（JRバス・230円）：高雄 → 二条駅前 約40分、京都駅前 約55分。15:16、15:36、16:16、17:16、18:01、18:06、18:36、18:46、19:16、20:06発（最終）。毎日同じ時刻",
        "Back (JR Bus, ¥230): Takao → Nijo-eki-mae about 40 min, Kyoto Station about 55 min. Departs 15:16, 15:36, 16:16, 17:16, 18:01, 18:06, 18:36, 18:46, 19:16, 20:06 (the last). The same every day"),
    row("train", "栂ノ尾・槇ノ尾から乗るときは、高雄の2分前・1分前に出ます（栂ノ尾は11〜15時台の毎時14分・34分発）",
        "From Toganoo or Makinoo the bus leaves 2 or 1 minutes before Takao (Toganoo at :14 and :34 past each hour from 11:00 to 15:59)"),
    row("train", "市バス8系統（230円）：高雄 → 四条烏丸 約45分。10〜16時台は毎時56分発、17:36、18:16、18:56、19:36、20:16発（四条烏丸まで行く最後）",
        "City bus 8 (¥230): Takao → Shijo-Karasuma about 45 min. At :56 past each hour from 10:00 to 16:59, then 17:36, 18:16, 18:56, 19:36, 20:16 (the last to Shijo-Karasuma)"),
    row("train", "二条駅前で降りたら、地下鉄東西線の二条駅から京都市役所前・三条京阪へ 6〜8分・220円",
        "From Nijo-eki-mae, the Tozai subway line takes 6–8 minutes to Kyoto Shiyakusho-mae or Sanjo-Keihan, ¥220"),
]
# 高山寺で終わるコース（開門コース）は、栂ノ尾から乗る時刻を出す
BACK_ROWS_TOGANOO = [
    row("train", "帰り（JRバス・230円）：栂ノ尾 → 御室仁和寺 約18分、二条駅前 約40分、京都駅前 約57分。13:14、13:34、14:14、14:34、15:14、15:34、16:14、17:14、17:59、18:04、18:34、18:44、19:14、20:04発（最終）。毎日同じ時刻",
        "Back (JR Bus, ¥230): Toganoo → Omuro-Ninnaji about 18 min, Nijo-eki-mae about 40 min, Kyoto Station about 57 min. Departs 13:14, 13:34, 14:14, 14:34, 15:14, 15:34, 16:14, 17:14, 17:59, 18:04, 18:34, 18:44, 19:14, 20:04 (the last). The same every day"),
    row("train", "栂ノ尾で始まる便（13:14、13:34、14:34、15:14、16:14など）は座りやすい。14:14・15:34などは周山から来る便です",
        "Buses that start at Toganoo (13:14, 13:34, 14:34, 15:14, 16:14 and so on) are easier for a seat; the 14:14, 15:34 and others come down from Shuzan"),
    BACK_ROWS[3],
]

BACK_TIP = T("JRバスは西日本JRバスの時刻表（2026年4月1日改正）、市バスは京都市交通局の停留所ごとの時刻表（2026年3月20日改正）、地下鉄は乗換案内（Yahoo!路線情報）で、11月22日に確認しました。紅葉の時期は道が混んで遅れることがあります。",
             "JR Bus times are from the West JR Bus timetable (revised 1 April 2026), city bus times from the Kyoto City Transportation Bureau’s stop timetables (revised 20 March 2026), and the subway from a route planner, all checked on 22 November. In the autumn season traffic can make buses late.")

# 帰りに寄れる場所と、街なかの夜（各コースの最後のスポットの文章に足す）
AFTER = T("帰りに寄れる場所と、夜\n\n"
          "高雄は日が暮れると店が閉まります。夜は街なかで。帰りのJRバスは、仁和寺・龍安寺・北野天満宮の近くを通ります（同じサイトの「金閣寺〜北野」のマップにくわしく書いています）。\n"
          "・仁和寺（にんなじ）：「御室仁和寺」で降りてすぐ。御所庭園は3〜11月が9:00〜17:00（受付16:30まで）、12〜2月は9:00〜16:30。大人800円。\n"
          "・北野天満宮のもみじ苑：「北野白梅町」で降りて歩いて約5分。2026年は12月6日まで、9:00〜16:00（受付15:40まで）。11月13日からはライトアップがあり、20:00まで（受付19:40まで）。大人1,500円。帰りは「北野天満宮前」から市バス10系統で三条京阪前へ（三条京阪まで行く最後は21:34発）。\n"
          "・仁和寺の紅葉雲海ライトアップ：2026年は12月13日までの金・土・日・祝日（11月28日は休み）。18:30〜21:00（受付20:30まで）、大人2,800円。帰りは「御室仁和寺」から市バス10系統で三条京阪前へ約40分（三条京阪まで行く最後は21:22発）。\n\n"
          "街なかで晩ごはん\n"
          "二条駅前で降りて地下鉄東西線に乗れば、京都市役所前・三条京阪まで6〜8分。三条大橋のまわりの木屋町通（きやまちどおり）と先斗町（ぽんとちょう）には、遅くまで開いている店が並びます。閉まる時間とラストオーダーは店ごとに違うので、入る前に表の案内で確かめてください。店を決めておきたい人は、叡山電鉄のマップの24〜26番（祇園四条・ともしび3rd・先斗町）も見てください。",
          "Stops on the way back, and the evening\n\n"
          "Takao’s shops close at dusk, so spend the evening in town. The JR Bus back passes close to Ninna-ji, Ryoan-ji and Kitano Tenmangu (see the Kinkaku-ji to Kitano map on this site for details).\n"
          "• Ninna-ji: right by the “Omuro-Ninnaji” stop. The palace garden is open 9:00–17:00 from March to November (last entry 16:30), and 9:00–16:30 from December to February. ¥800.\n"
          "• Kitano Tenmangu’s maple garden: about 5 minutes’ walk from the “Kitano-Hakubaicho” stop. In 2026 it is open until 6 December, 9:00–16:00 (last entry 15:40); from 13 November it is lit up and stays open until 20:00 (last entry 19:40). ¥1,500. Back to town on city bus 10 from “Kitano-Tenmangu-mae” to Sanjo-Keihan-mae (the last that goes all the way to Sanjo-Keihan leaves at 21:34).\n"
          "• Ninna-ji’s autumn light-up (“Koyo Unkai”): in 2026 on Fridays, weekends and holidays until 13 December (not on 28 November), 18:30–21:00 (last entry 20:30), ¥2,800. Back to town on city bus 10 from “Omuro-Ninnaji” to Sanjo-Keihan-mae, about 40 minutes (the last that goes all the way to Sanjo-Keihan leaves at 21:22).\n\n"
          "Dinner in town\n"
          "Get off at Nijo-eki-mae and the Tozai subway line takes 6–8 minutes to Kyoto Shiyakusho-mae or Sanjo-Keihan. Around Sanjo Ohashi bridge, Kiyamachi-dori and Pontocho are lined with places that stay open late. Closing times and last orders differ, so check the sign at the door. If you’d rather have a place picked out, see stops 24–26 (Gion-Shijo, Tomoshibi 3rd, Pontocho) on the Eizan Railway map.")
AFTER_NOTICES = [
    notice("北野天満宮のもみじ苑は12月6日まで", "Kitano Tenmangu’s maple garden: until 6 December",
           "帰りのバスを北野白梅町で降りると、歩いて約5分。11月13日からはライトアップで20:00まで（受付19:40まで）。大人1,500円。",
           "Get off the bus at Kitano-Hakubaicho and it’s about 5 minutes’ walk. From 13 November it is lit up until 20:00 (last entry 19:40). ¥1,500.",
           url="https://kitanotenmangu.or.jp/", frm="2026-10-31", to="2026-12-06"),
    notice("仁和寺の紅葉雲海ライトアップ（金・土・日・祝日）", "Ninna-ji autumn light-up (Fri, weekends, holidays)",
           "2026年は12月13日まで（11月28日は休み）。18:30〜21:00（受付20:30まで）、大人2,800円。帰りは御室仁和寺から市バス10系統で三条京阪前へ（最後は21:22発）。",
           "In 2026 until 13 December (not on 28 November). 18:30–21:00 (last entry 20:30), ¥2,800. Back by city bus 10 from Omuro-Ninnaji to Sanjo-Keihan-mae (the last at 21:22).",
           url="https://ninnaji.jp/news/event-34-2/", frm="2026-10-24", to="2026-12-13"),
]
AFTER_LINKS = [KINKAKU, EIZAN, link("official", "仁和寺 紅葉雲海ライトアップ", "Ninna-ji autumn light-up (Japanese)", "https://ninnaji.jp/news/event-34-2/")]

# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    kiyotaki=dict(
        name=T("高雄橋と清滝川", "Takao bridge & Kiyotaki river"), kind=T("渓谷・茶屋", "Gorge & teahouses"),
        blurb=T("高雄バス停から谷へ下りると、朱の高雄橋と清滝川。橋を渡ると、茶屋の並ぶ石段が神護寺へ続きます。",
                "Down from the Takao bus stop into the valley: the vermilion Takao bridge over the Kiyotaki, and teahouses on the stone stairway up to Jingoji."),
        caution=T("高雄は夜に開いている店がほぼありません。京都駅前行きJRバスの最終は高雄20:06発", "Almost nothing is open in Takao after dark. The last JR Bus to Kyoto Station leaves Takao at 20:06"),
        lat=35.05542, lng=135.67303,
        body=T("高雄橋（たかおばし）と清滝川（きよたきがわ）\n\n"
               "JRバスも市バスも、バス停の名前は「高雄」。国道からわき道の坂を谷へ下りると、清滝川にかかる朱色の高雄橋です。バス停から橋まで歩いて10分ほど（地図で見た目安）。紅葉の時期は、谷じゅうがもみじに染まります。橋を渡ると、神護寺への長い石段が始まります。神護寺の案内では、高雄バス停から神護寺まで歩いて約20分です。\n\n"
               "石段の途中に茶屋が2軒あります（どちらも高雄保勝会の案内）。\n"
               "・硯石亭（すずりいしてい）：9:00〜17:00。不定休（11月は休みなし、1・2月は休み）。うどん・そば（750円〜）、秋だけの湯豆腐の膳（1,900円）、もみじ餅（700円）、抹茶とお菓子（850円）。秋は11:00〜14:00に、もみじ餅を売らないことがあります（店の案内）。写真6枚目がこの店です。\n"
               "・高雄茶屋：9:00〜17:00。不定休（10月〜12月上旬は休みなし）。もみじ餅つきのお抹茶600円、柚子入りのもみじうどん800円など。\n"
               "高雄バス停の横の山本食堂（9:00〜18:00ごろ、シーズン中は休みなし）は、帰りのバスを待つあいだにも。\n\n"
               "高雄は日が暮れると店が閉まり、谷の道も暗くなります。神護寺を出たら、明るいうちにバス停へ上がりましょう。",
               "Takao bridge and the Kiyotaki river\n\n"
               "JR Bus and city bus both call the stop “Takao”. From the main road, a side lane drops into the valley to the vermilion Takao bridge over the Kiyotaki, about 10 minutes from the stop (an estimate from the map). In autumn the whole gorge turns red. Across the bridge the long stone stairway up to Jingoji begins; the temple gives about 20 minutes on foot from the Takao stop.\n\n"
               "Two teahouses sit on the stairway (both listed by the Takao tourist association):\n"
               "• Suzuri-ishi-tei: 9:00–17:00, closes on irregular days (open every day in November; closed in January and February). Udon and soba from ¥750, an autumn-only yudofu (simmered tofu) set ¥1,900, momiji-mochi ¥700, matcha with a sweet ¥850. In autumn it may stop selling momiji-mochi between 11:00 and 14:00 (the shop’s notice). It’s in photo 6.\n"
               "• Takao-chaya: 9:00–17:00, closes on irregular days (open every day from October to early December). Matcha with momiji-mochi ¥600, momiji udon with yuzu ¥800 and more.\n"
               "Yamamoto Shokudo, right by the Takao bus stop (9:00 to about 18:00, open every day in the season), is handy while you wait for the bus home.\n\n"
               "After dark the shops close and the valley path is unlit, so head back up to the bus stop while it’s light."),
        gmaps=[gm("高雄橋", "Takao bridge", 35.05542, 135.67303, "高雄橋 京都 右京区"),
               gm("高雄バス停", "Takao bus stop", 35.05620, 135.67383, "高雄 バス停 京都 右京区"),
               gm("硯石亭", "Suzuri-ishi-tei", 35.05481, 135.67215, "硯石亭 高雄")],
        links=[link("official", "硯石亭", "Suzuri-ishi-tei (Japanese)", "http://www.suzuriishitei.com/"), HOSHO, JRBUS,
               link("info", "紅葉だより（京都観光Navi）", "Autumn-leaf report (Kyoto City, Japanese)", MOMIJI)],
        notices=[SEASON, AUTUMN_BUS, WINTER],
        _rows=[row("hours", "高雄バス停 → 高雄橋 歩いて約10分（地図で見た目安）、→ 神護寺 約20分（神護寺の案内）",
                   "Takao stop → Takao bridge about 10 min on foot (map estimate); → Jingoji about 20 min (temple’s access page)"),
               row("hours", "硯石亭 9:00〜17:00（11月は休みなし、1・2月は休み）／高雄茶屋 9:00〜17:00（10月〜12月上旬は休みなし）",
                   "Suzuri-ishi-tei 9:00–17:00 (open daily in November; closed Jan–Feb) / Takao-chaya 9:00–17:00 (open daily October to early December)")] + BACK_ROWS[:1] + BACK_ROWS[2:3],
        _tip=T("茶屋の時間と値段は、硯石亭の公式サイトと高雄保勝会の「お食事処」の案内で確認しました（11月22日）。バスは西日本JRバスと京都市交通局の時刻表です。",
               "Teahouse hours and prices were checked on Suzuri-ishi-tei’s website and the Takao tourist association’s list (22 November). Buses are from the West JR Bus and Kyoto City Transportation Bureau timetables."),
        _source="硯石亭 公式サイト、高雄保勝会（お食事処）、神護寺 公式サイト（交通案内）、西日本JRバス 高雄京北線時刻表（2026年4月1日改正）、京都市交通局 8系統 高雄の時刻表（2026年3月20日改正）。2026-11-22に確認"),
    jingoji=dict(
        name=T("神護寺", "Jingoji"), kind=T("寺", "Temple"),
        blurb=T("長い石段を上った山の中腹のお寺。楼門をくぐると、広い境内がもみじで赤くなります。",
                "A temple high on the mountainside at the top of a long stone stairway; through the gate, the wide precinct turns red with maples."),
        caution=T("9:00〜16:00。高雄バス停から石段を上って約20分。中学生以上1,000円", "9:00–16:00. About 20 minutes up the steps from the Takao stop. ¥1,000 (junior high and up)"),
        lat=35.05467, lng=135.67131,
        body=T("神護寺（じんごじ）\n\n"
               "平安時代のはじめに開かれ、空海（弘法大師）もいたことのある、高雄山の中腹のお寺です。高雄橋から、もみじに囲まれた長い石段をゆっくり上ります。上りきると、楼門の先に広い境内が開けます。金堂、毘沙門堂、五大堂のまわりは、紅葉の時期は一面の赤。\n\n"
               "石段が長いので、歩きやすい靴で。金堂の前の石段を上りきって振り返ると、五大堂と毘沙門堂の屋根ごしにもみじが見下ろせます（写真5枚目）。境内の西の端からは、谷に向かって素焼きのお皿を投げる「かわらけ投げ」ができます。\n\n"
               "拝観は9:00〜16:00。16時には閉まるので、遅くとも15時すぎには入りましょう。境内の拝観料は中学生以上1,000円（2024年7月から）、小学生500円です。",
               "Jingoji\n\n"
               "Founded in the early Heian period, and once home to Kukai (Kobo Daishi), this temple sits high on Mt. Takao. From the Takao bridge you climb a long, maple-lined stairway at an easy pace; at the top, beyond the gate, the broad precinct opens out. Around the main hall, the Bishamon hall and the Godai hall, everything turns red in autumn.\n\n"
               "The stairs are long, so wear comfortable shoes. Climb the steps in front of the main hall and turn round: you look down on the maples over the roofs of the Godai and Bishamon halls (photo 5). At the western edge of the grounds you can throw little clay discs into the valley (“kawarake-nage”).\n\n"
               "Open 9:00–16:00. It closes at 16:00, so go in by just after 15:00 at the latest. Entry is ¥1,000 from junior high up (since July 2024), ¥500 for elementary children."),
        gmaps=[gm("神護寺", "Jingoji", 35.05467, 135.67131, "神護寺 高雄")],
        links=[link("official", "神護寺 公式サイト", "Jingoji (official, Japanese)", "http://jingoji.or.jp/")],
        _rows=[row("hours", "9:00〜16:00", "9:00–16:00"), row("closed", "年中無休", "Open every day"),
               row("fee", "中学生以上1,000円、小学生500円（2024年7月1日から）", "¥1,000 (junior high and up), ¥500 elementary (from 1 July 2024)")],
        _tip=T("神護寺の公式サイトのトップと交通案内で確認しました（11月22日）。", "Checked on the temple website’s top page and access page (22 November)."),
        _source="神護寺 公式サイト（トップの境内拝観時間・拝観料金、交通案内）2026-11-22"),
    saimyoji=dict(
        name=T("西明寺（槇尾）", "Saimyoji (Makinoo)"), kind=T("寺", "Temple"),
        blurb=T("清滝川にかかる朱の指月橋を渡って、小さな山寺へ。表門ごしに見る本堂と、庭のもみじ。",
                "Cross the vermilion Shigetsu bridge over the Kiyotaki to a small mountain temple: the main hall seen through the front gate, and maples in the garden."),
        caution=T("受付は16:30まで。大人700円、中・高生500円", "Last entry 16:30. ¥700; junior high and high school ¥500"),
        lat=35.05632, lng=135.67505,
        body=T("西明寺（さいみょうじ）\n\n"
               "神護寺と高山寺のあいだ、槇尾（まきのお）の山すそのお寺です。朱色の指月橋（しげつきょう）を渡り、もみじに覆われた石段を上ると表門、その先に本堂があります。今の本堂は元禄13年（1700年）に建てられたものです。本堂の中から東の苔庭を見ると、額縁の中の絵のように見えます（お寺の案内）。秋は客殿でお抹茶をいただけます（料金は要確認）。\n\n"
               "写真を撮るなら、川のそばから指月橋を見上げる場所（写真1枚目）と、表門ごしに本堂が見える場所（2枚目）。京都観光Naviの紅葉だよりでは、見ごろは例年11月10日前後です。\n\n"
               "神護寺とは清滝川沿いの道で、高山寺とは国道162号でつながっています。どちらも歩いて15〜20分です。歩いて約5分の「槇ノ尾」バス停からも、JRバスと市バスに乗れます。\n\n"
               "近くでお昼を食べるなら（高雄保勝会の案内）\n"
               "・指月亭（しげつてい）：清滝川のそば。10:00〜17:00、不定休。秋は湯どうふ定食（2,500円）。\n"
               "・よしでん：槇ノ尾バス停の前。9:00〜18:30、不定休。めん類・丼物・定食、秋はおでんも。",
               "Saimyoji\n\n"
               "A temple at the foot of Makinoo hill, between Jingoji and Kosanji. Cross the vermilion Shigetsu bridge and climb the maple-covered steps to the front gate, with the main hall beyond; the present hall was built in 1700. From inside the hall, the moss garden to the east looks like a framed painting (the temple’s guide). In autumn matcha is served in the guest hall (price: please check).\n\n"
               "Two good photo spots: looking up at the Shigetsu bridge from beside the river (photo 1), and the main hall framed by the front gate (photo 2). Kyoto City’s autumn-leaf report gives the usual peak as around 10 November.\n\n"
               "A riverside path links it to Jingoji, and Route 162 to Kosanji; either is 15–20 minutes on foot. JR Bus and city bus also stop at “Makinoo”, about 5 minutes’ walk.\n\n"
               "Lunch nearby (Takao tourist association list)\n"
               "• Shigetsu-tei, by the Kiyotaki river: 10:00–17:00, closes on irregular days. In autumn, a yudofu set (¥2,500).\n"
               "• Yoshiden, in front of the Makinoo bus stop: 9:00–18:30, closes on irregular days. Noodles, rice bowls and set meals; oden in autumn."),
        gmaps=[gm("西明寺", "Saimyoji", 35.05632, 135.67505, "西明寺 槇尾"),
               gm("槇ノ尾バス停", "Makinoo bus stop", 35.05639, 135.67654, "槇ノ尾 バス停 京都")],
        links=[link("official", "西明寺 公式サイト", "Saimyoji (official, Japanese)", "https://www.saimyoji.or.jp/"), HOSHO, JRBUS],
        _rows=[row("hours", "9:00〜17:00（受付は16:30まで）", "9:00–17:00 (last entry 16:30)"),
               row("fee", "大人700円、中・高生500円", "¥700; junior high and high school ¥500"),
               row("hours", "指月亭 10:00〜17:00／よしでん 9:00〜18:30（どちらも不定休）", "Shigetsu-tei 10:00–17:00 / Yoshiden 9:00–18:30 (both close on irregular days)"),
               row("train", "槇ノ尾 → 京都駅前 JRバス（230円）。11〜15時台は毎時15分・35分発", "Makinoo → Kyoto Station, JR Bus (¥230): at :15 and :35 past each hour from 11:00 to 15:59")],
        _tip=T("拝観時間と料金は西明寺の公式サイト（料金はトップの画像の案内）、お店は高雄保勝会の案内、バスは西日本JRバスの時刻表で確認しました（11月22日）。お抹茶の料金は公式サイトに書かれていません。",
               "Hours and fees were checked on the temple’s website (fees are shown as an image on the top page), the places to eat on the Takao tourist association’s list, and the bus on the West JR Bus timetable (22 November). The price of the matcha isn’t given on the website."),
        _source="西明寺 公式サイト（トップ・歩き方・アクセス）、高雄保勝会（お食事処）、西日本JRバス 高雄京北線時刻表（2026年4月1日改正）。2026-11-22に確認"),
    kosanji=dict(
        name=T("高山寺（栂尾）", "Kosanji (Toganoo)"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
        blurb=T("「鳥獣人物戯画」が伝わる、世界遺産の山寺。国宝の石水院の縁側から、川の向こうの山を眺めます。",
                "A World Heritage mountain temple, home of the Choju-jinbutsu-giga scrolls. From the veranda of Sekisuiin, a National Treasure, you look out to the hill across the river."),
        caution=T("8:30〜17:00。石水院1,000円。秋は別に入山料500円（2026年は12月上旬まで）", "8:30–17:00. Sekisuiin ¥1,000; in autumn a separate ¥500 entry fee (until early December in 2026)"),
        lat=35.06012, lng=135.67855,
        body=T("高山寺（こうさんじ）\n\n"
               "JRバスの終点「栂ノ尾（とがのお）」のバス停のそばから、山の斜面に広がるお寺です。1206年に明恵上人（みょうえしょうにん）が再興し、1994年に世界遺産に登録されました。\n\n"
               "いちばんの見どころは、国宝の石水院（せきすいいん）。明恵上人の時代から残る、ただひとつの建物です。南の縁側は、清滝川の向こうの山に向かって開けています。公式サイトのすすめは、縁から一歩下がって畳に座ること。柱と蔀戸（しとみど）が額縁になって、景色が切り取られて見えます。\n\n"
               "うさぎやかえるが遊ぶ国宝の絵巻「鳥獣人物戯画（ちょうじゅうじんぶつぎが）」が伝わるお寺でもあります（石水院には複製が展示されています）。境内には「日本最古之茶園」の碑が立つ茶園があり、栄西禅師が宋から持ち帰った茶の実を、明恵上人がここで育てたと伝わります。\n\n"
               "料金は、石水院が一般1,000円・小学生500円。秋は境内の入口で、別に入山料500円（小学生300円）がかかります。2026年は10月3日から12月上旬まで（公式サイトのお知らせ）。\n\n"
               "門前でお昼を食べるなら（高雄保勝会の案内）\n"
               "・とがの茶屋：高山寺の前。清滝川を眺めながら食べられる店。9:00〜17:00、木曜休み（10月20日〜11月30日は休みなし）。\n"
               "・錦水亭支店：栂ノ尾の国道沿い、清滝川を望む店。9:00〜18:00、木曜休み。山菜入りのおそば、鮎の塩焼き、わらび餅など。",
               "Kosanji\n\n"
               "The temple climbs the hillside from beside “Toganoo”, the last stop on the JR Bus line. The priest Myoe revived it in 1206, and it was registered as a World Heritage site in 1994.\n\n"
               "The highlight is Sekisuiin, a National Treasure and the only building left from Myoe’s time. Its south veranda opens towards the hill across the Kiyotaki river. The temple’s own advice: sit on the tatami a step back from the veranda, and the pillars and lattice shutters frame the view like a picture.\n\n"
               "This is also the temple of the Choju-jinbutsu-giga, the National Treasure scrolls of frolicking rabbits and frogs (copies are shown in Sekisuiin). In the grounds is a tea garden marked with a stone reading “Japan’s oldest tea garden”: the Zen master Eisai brought tea seeds from Song China, and Myoe is said to have grown them here.\n\n"
               "Sekisuiin costs ¥1,000 (elementary ¥500). In autumn there is also a ¥500 entry fee at the gate (elementary ¥300); in 2026 from 3 October to early December (the temple’s notice).\n\n"
               "Lunch at the gate (Takao tourist association list)\n"
               "• Togano-chaya, in front of the temple, with a view of the Kiyotaki: 9:00–17:00, closed Thursdays (open daily from 20 October to 30 November).\n"
               "• Kinsuitei branch, on the main road at Toganoo with a view of the river: 9:00–18:00, closed Thursdays. Soba with mountain vegetables, grilled ayu, warabi-mochi and more."),
        gmaps=[gm("高山寺", "Kosanji", 35.06012, 135.67855, "高山寺 栂尾 京都"), gm("栂ノ尾バス停", "Toganoo bus stop", 35.05991, 135.67898, "栂ノ尾 バス停 京都")],
        links=[link("official", "高山寺 公式サイト", "Kosanji (official, Japanese)", "https://kosanji.com/"),
               link("info", "高山寺のお知らせ（秋期の入山料）", "Kosanji notices (autumn entry fee, Japanese)", "https://kosanji.com/blog/"), HOSHO, JRBUS],
        _rows=[row("hours", "8:30〜17:00", "8:30–17:00"),
               row("fee", "石水院 一般1,000円、小学生500円。秋（2026年は10月3日〜12月上旬）は別に入山料500円（小学生300円）",
                   "Sekisuiin ¥1,000, elementary ¥500. In autumn (3 October to early December in 2026) a separate ¥500 entry fee (elementary ¥300)"),
               row("hours", "とがの茶屋 9:00〜17:00（木曜休み、10月20日〜11月30日は休みなし）／錦水亭支店 9:00〜18:00（木曜休み）",
                   "Togano-chaya 9:00–17:00 (closed Thu; open daily 20 Oct – 30 Nov) / Kinsuitei branch 9:00–18:00 (closed Thu)")],
        _tip=T("高山寺の公式サイト（拝観案内とお知らせ）、高雄保勝会の案内、バスは西日本JRバスの時刻表で確認しました（11月22日）。西明寺との距離は OpenStreetMap で測った目安です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
               "Checked on the temple’s website (visitor guide and notices), the Takao tourist association’s list, and the West JR Bus timetable (22 November). The distance from Saimyoji is an estimate measured on OpenStreetMap. Photos are from Wikimedia Commons (author and license shown on each photo)."),
        _source="高山寺 公式サイト（拝観・境内のご案内、お知らせ「秋期拝観のご案内」2026-09-13）、高雄保勝会（お食事処）、西日本JRバス 高雄京北線時刻表（2026年4月1日改正）。2026-11-22に確認"),
)

NIJO = gm("二条駅前（JRバス・市バスのバス停）", "Nijo-eki-mae (JR Bus & city bus stop)", 35.01152, 135.74260, "二条駅前 バス停 JRバス 千本通")

VIS, ARR = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
# （スポットの id, 時間の見出し, 時間（日本語）, 時間（英語）, そのコースでの一言）
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="takao.json",
        note="「9〜10時に出発」コース。京都市役所前9:25（土日祝9:24）の地下鉄で二条→二条駅前9:46のJRバス→栂ノ尾10:26着。高山寺→門前の茶屋で早めのお昼→西明寺→高雄橋→神護寺（16:00まで）→高雄15:36のバス→北野天満宮のもみじ苑（12月6日まで）か街なか→夜は三条・先斗町。",
        rows=[row("train", "行き：京都市役所前 9:25（土日祝 9:24）発の地下鉄東西線で二条へ（6分・220円。三条京阪からは8分）→ 二条駅前 9:46発のJRバス（栂ノ尾行き）→ 終点の栂ノ尾 10:26着・230円",
                  "Out: Tozai subway from Kyoto Shiyakusho-mae at 9:25 (9:24 on weekends and holidays) to Nijo (6 min, ¥220; 8 min from Sanjo-Keihan) → JR Bus from Nijo-eki-mae at 9:46 (for Toganoo) → Toganoo, the last stop, 10:26, ¥230"),
              row("train", "京都駅前から乗るなら 9:30発（始発）→ 栂ノ尾 10:26着。1本あとは京都駅前 10:00発・二条駅前 10:16発 → 栂ノ尾 10:56着",
                  "From Kyoto Station: the 9:30 (first stop) → Toganoo 10:26. The next is Kyoto Station 10:00 / Nijo-eki-mae 10:16 → Toganoo 10:56"),
              row("train", "市バス8系統なら：四条烏丸 9:52発 → 高雄 10:40着・230円（毎日同じ時刻。栂ノ尾まで行きます）",
                  "By city bus 8: Shijo-Karasuma 9:52 → Takao 10:40, ¥230 (the same every day; it runs on to Toganoo)")],
        order=[
            ("kosanji", VIS, "10:30〜11:20、お昼 11:20〜12:10", "10:30–11:20, lunch 11:20–12:10",
             T("このコースは、バスの終点の栂ノ尾から歩き始めて、谷を下りながら3つのお寺を回ります。二条駅前9:46発のJRバスで、栂ノ尾に10:26に着きます。「高雄」では降りずに、終点まで乗ってください。\n\n"
               "石水院でゆっくり座ったら、門前の茶屋で早めのお昼に。11時半前なら、昼の混む時間の前に入れます。\n\n"
               "食べ終わったら、国道162号を南へ歩いて西明寺へ（約15分、約800m）。",
               "This course starts at Toganoo, the end of the bus line, and works down the valley through the three temples. The 9:46 JR Bus from Nijo-eki-mae reaches Toganoo at 10:26. Don’t get off at Takao: stay on to the last stop.\n\n"
               "After a long sit at Sekisuiin, have an early lunch at a teahouse by the gate. Before 11:30 you beat the midday rush.\n\n"
               "Then walk south along Route 162 to Saimyoji (about 15 minutes, about 800 m).")),
            ("saimyoji", VIS, "12:30〜13:15", "12:30–13:15",
             T("国道から脇道を下りて、指月橋を渡ります。見終わったら、清滝川沿いの道を下流へ歩いて高雄橋へ（15〜20分）。",
               "Leave the road, go down a side lane and cross the Shigetsu bridge. Afterwards, follow the riverside path downstream to the Takao bridge (15–20 minutes).")),
            ("kiyotaki", VIS, "13:35〜13:50", "13:35–13:50",
             T("川沿いの道を歩いてくると、高雄橋に出ます。橋のまわりで写真を撮ったら、神護寺の石段へ。上る前に、石段の茶屋でひと休みしても。",
               "The riverside path brings you out at the Takao bridge. Take your photos, then head for Jingoji’s stairs; you can rest at a teahouse on the way up.")),
            ("jingoji", VIS, "14:10〜15:15（16:00に閉まります）", "14:10–15:15 (closes at 16:00)",
             T("石段をゆっくり上って14時すぎに着きます。16時に閉まるので、ここを最後にするなら遅れないように。\n\n"
               "出たら石段を下りて、高雄バス停まで約20分。15:36発のJRバスに乗ると、北野白梅町16:03、二条駅前16:15に着きます（次は16:16発）。",
               "Climb the steps at an easy pace to arrive just after 14:00. It closes at 16:00, so don’t run late on the last stop of the day.\n\n"
               "Then it’s about 20 minutes down the steps and back up to the Takao bus stop. The 15:36 JR Bus reaches Kitano-Hakubaicho at 16:03 and Nijo-eki-mae at 16:15 (the next leaves at 16:16).")),
        ],
        sections=[dict(first="kosanji", last="kosanji", day=0), dict(first="saimyoji", last="saimyoji", day=1),
                  dict(first="kiyotaki", last="jingoji", day=2)],
        focus=("kosanji", "jingoji"),
        hints=[("saimyoji", dict(any=["saimyoji"], none=["kiyotaki", "jingoji"]), None, None,
                "神護寺に行かない日は、西明寺のあと「槇ノ尾」バス停からJRバスで帰れます（11〜15時台は毎時15分・35分発。二条駅前まで約40分）。",
                "Skipping Jingoji? After Saimyoji take the JR Bus from the “Makinoo” stop (at :15 and :35 past each hour from 11:00 to 15:59; about 40 minutes to Nijo-eki-mae)."),
               ("jingoji", dict(any=["jingoji"], none=["kosanji", "saimyoji"]), None, None,
                "神護寺だけの日は、二条駅前9:46発のバスを「高雄」で降ります（10:24着）。石段を上って11時前に着き、帰りは石段の茶屋でお昼にして、高雄から12〜13時台のバスで戻れます（12:16、12:36、13:16、13:36発）。",
                "Jingoji only? Get off the 9:46 from Nijo-eki-mae at “Takao” (10:24). You reach the temple before 11:00; have lunch at a teahouse on the steps and take a bus back from Takao in the 12:00 or 13:00 hour (12:16, 12:36, 13:16, 13:36).")]),
    dict(
        id="early", file="takao-early.json",
        note="「神護寺の開門に合わせる」コース。京都市役所前7:16（土日祝7:21）の地下鉄で二条→二条駅前7:36のJRバス→高雄8:14着。朝の高雄橋→神護寺9:00→参道の茶屋でひと休み→西明寺→槇ノ尾でお昼→高山寺→栂ノ尾14:34のバス→仁和寺・北野天満宮か街なか→夜は三条・先斗町。",
        rows=[row("train", "行き：京都市役所前 7:16（土日祝 7:21）発の地下鉄東西線で二条へ（6分・220円。三条京阪からは8分）→ 二条駅前 7:36発のJRバス（栂ノ尾行き）→ 高雄 8:14着・230円",
                  "Out: Tozai subway from Kyoto Shiyakusho-mae at 7:16 (7:21 on weekends and holidays) to Nijo (6 min, ¥220; 8 min from Sanjo-Keihan) → JR Bus from Nijo-eki-mae at 7:36 (for Toganoo) → Takao 8:14, ¥230"),
              row("train", "京都駅前から乗るなら 7:20発（始発）→ 高雄 8:14着", "From Kyoto Station: the 7:20 (first stop) → Takao 8:14"),
              row("train", "市バス8系統なら：四条烏丸 7:53（平日）→ 高雄 8:41着／7:55（土日祝）→ 8:38着・230円。神護寺に着くのは9時すぎです",
                  "By city bus 8: Shijo-Karasuma 7:53 (weekdays) → Takao 8:41 / 7:55 (weekends and holidays) → 8:38, ¥230. You reach Jingoji just after 9:00")],
        order=[
            ("kiyotaki", ARR, "8:14（二条駅前 7:36発）。高雄橋 8:25〜8:40", "8:14 (the 7:36 from Nijo-eki-mae). Takao bridge 8:25–8:40",
             T("神護寺が開く9時に合わせるバスです。高雄に8:14に着いたら、谷へ下りて高雄橋へ。茶屋が開く前の清滝川です。\n\n"
               "朝ごはんは、出る前に食べてください。高雄で朝早く開いている食事の店は確かめられていません。石段の茶屋は9時から開くので、神護寺のあとにひと休みできます。\n\n"
               "8:40ごろから石段を上ると、神護寺の門に9時ごろ着きます。",
               "This bus is timed for Jingoji’s 9:00 opening. Off at Takao at 8:14, walk down to the Takao bridge: the Kiyotaki river before the teahouses open.\n\n"
               "Have breakfast before you leave: no place to eat in Takao could be confirmed as open this early. The teahouses on the steps open at 9:00, so you can rest there after Jingoji.\n\n"
               "Start up the steps at about 8:40 and you reach Jingoji’s gate at about 9:00.")),
            ("jingoji", VIS, "9:00〜10:15、茶屋でひと休み 10:15〜10:45", "9:00–10:15, teahouse break 10:15–10:45",
             T("開門の9時に入ります。人が増える前に、金堂の石段の上から境内を見下ろしてください。\n\n"
               "出たら、石段の途中の高雄茶屋か硯石亭でひと休み。もみじ餅とお抹茶か、温かいうどんで、遅めの朝ごはんのかわりに。\n\n"
               "そのあと、高雄橋から清滝川沿いの道を上流へ歩いて西明寺へ（15〜20分）。",
               "Go in at the 9:00 opening. Before it fills up, look down over the precinct from the top of the main hall’s steps.\n\n"
               "Afterwards, rest at Takao-chaya or Suzuri-ishi-tei on the steps: momiji-mochi and matcha, or a hot bowl of udon, as a late breakfast.\n\n"
               "Then walk upstream along the Kiyotaki from the Takao bridge to Saimyoji (15–20 minutes).")),
            ("saimyoji", VIS, "11:05〜11:45、お昼 11:50〜12:40", "11:05–11:45, lunch 11:50–12:40",
             T("見終わったら、近くの指月亭か、槇ノ尾バス停の前のよしでんでお昼に。12時前に入ると楽です。\n\n"
               "食べ終わったら、国道162号を北へ歩いて高山寺へ（約15分、約800m）。",
               "Afterwards, have lunch nearby at Shigetsu-tei or at Yoshiden by the Makinoo bus stop. Before 12:00 it’s easier to get a table.\n\n"
               "Then walk north along Route 162 to Kosanji (about 15 minutes, about 800 m).")),
            ("kosanji", VIS, "12:55〜14:15", "12:55–14:15",
             T("石水院の縁側に座って、川の向こうの山を眺めてください。\n\n"
               "帰りは「栂ノ尾」バス停から。14:34発は栂ノ尾で始まる便なので、座りやすいです。御室仁和寺14:52、龍安寺前14:55、北野白梅町15:03、二条駅前15:15に着きます。1本前の14:14発は周山から来る便です。",
               "Sit on Sekisuiin’s veranda and look out to the hill across the river.\n\n"
               "Go back from the “Toganoo” stop. The 14:34 starts there, so seats are easier; it reaches Omuro-Ninnaji at 14:52, Ryoanji-mae 14:55, Kitano-Hakubaicho 15:03 and Nijo-eki-mae 15:15. The one before, at 14:14, comes down from Shuzan.")),
        ],
        sections=[dict(first="kiyotaki", last="jingoji", day=0), dict(first="saimyoji", last="saimyoji", day=1),
                  dict(first="kosanji", last="kosanji", day=2)],
        focus=("kiyotaki", "kosanji"),
        hints=[("kosanji", dict(any=["kosanji"], none=["saimyoji"]), None, None,
                "西明寺に寄らない日は、神護寺のあと高雄バス停からJRバスで栂ノ尾へ2分（高雄10:54・11:34発など）。高山寺の門前でお昼にしてから石水院へ。",
                "Skipping Saimyoji? After Jingoji, ride the JR Bus two minutes from Takao to Toganoo (10:54, 11:34 and so on). Have lunch at Kosanji’s gate, then see Sekisuiin."),
               ("saimyoji", dict(any=["saimyoji"], none=["kosanji"]), None, None,
                "高山寺に寄らない日は、お昼のあと「槇ノ尾」バス停からJRバスで（毎時15分・35分発）。御室仁和寺まで約17分、二条駅前まで約40分です。",
                "Skipping Kosanji? After lunch take the JR Bus from the “Makinoo” stop (at :15 and :35 past each hour): about 17 minutes to Omuro-Ninnaji, about 40 to Nijo-eki-mae."),
               ("jingoji", dict(any=["jingoji"], none=["saimyoji", "kosanji"]), None, None,
                "神護寺だけの日は、茶屋でひと休みしたあと、高雄から10〜11時台のバスで戻れます（10:36、11:16、11:36発）。",
                "Jingoji only? After a break at a teahouse, take a bus back from Takao in the 10:00 or 11:00 hour (10:36, 11:16, 11:36).")]),
]

SOURCES = [
    {"what": "JRバス 高雄京北線の時刻（2026年4月1日改正）：下り 京都駅前7:20・二条駅前7:36→高雄8:14、京都駅前9:30・二条駅前9:46→栂ノ尾10:26、京都駅前10:00・二条駅前10:16→栂ノ尾10:56。上り 高雄15:16・15:36・16:16・17:16・18:01・18:06・18:36・18:46・19:16・20:06（最終、京都駅前21:01着）、栂ノ尾11〜15時台14分・34分、槇ノ尾15分・35分、高雄15:36→北野白梅町16:03・二条駅前16:15、栂ノ尾14:34→御室仁和寺14:52・龍安寺前14:55・北野白梅町15:03・二条駅前15:15（14:14は周山発の便）。栂ノ尾の上り 13:14・13:34・14:14・14:34・15:14・15:34・16:14・17:14・17:59・18:04・18:34・18:44・19:14・20:04（最終）、うち周山発の便は11:34・12:34・14:14・15:34・17:14・17:59・18:44・20:04。平日だけの便は49系統（栂ノ尾6:39発）だけ", "url": JR_PDF, "checked": CHECKED},
    {"what": "JRバス 京都駅前〜栂ノ尾は230円均一（高雄京北線 普通運賃表）。紅葉の季節の週末などは午前は栂ノ尾行き、午後は京都駅前行きの臨時便を出すことがある（路線案内）", "url": JR_URL, "checked": CHECKED},
    {"what": "市バス8系統（2026年3月20日改正）：四条烏丸→高雄・栂ノ尾行き 平日7:53・土休日7:55、毎日9:52（四条烏丸の時刻表）。高雄着は平日8:41・土休日8:38、毎日10:40（高雄の栂ノ尾行きの時刻表）。高雄→四条烏丸 10〜16時台56分、17:36、18:16、18:56、19:36、20:16（20:56と22:02は京都外大前まで）", "url": "https://www2.city.kyoto.lg.jp/kotsu/busdia/diapdf/17430001.pdf", "checked": CHECKED},
    {"what": "市バス10系統（2026年3月20日改正）：北野天満宮前→三条京阪 最終21:34（21:59は四条京阪前まで）、御室仁和寺→三条京阪 最終21:22（21:47は四条京阪前まで）", "url": "https://www2.city.kyoto.lg.jp/kotsu/busdia/diapdf/15710001.pdf", "checked": CHECKED},
    {"what": "地下鉄東西線 京都市役所前→二条 6分・220円（平日7:16→7:22、9:25→9:31／土休日7:21→7:27、9:24→9:30）、三条京阪→二条 8分・220円（乗換案内 Yahoo!路線情報）", "url": "https://transit.yahoo.co.jp/", "checked": CHECKED},
    {"what": "神護寺：境内拝観 9:00〜16:00 年中無休、拝観料 中学生以上1,000円・小学生500円（2024年7月1日から）。高雄バス停から徒歩約20分、市バス8系統は四条烏丸から約45分（交通案内）", "url": "http://jingoji.or.jp/", "checked": CHECKED},
    {"what": "西明寺：拝観 9:00〜17:00（受付9:00〜16:30）、大人700円・中高生500円（トップの画像）。槇ノ尾バス停から徒歩5分、紅葉時期は臨時バス増発予定（アクセス）。秋は客殿でお抹茶（歩き方。料金の記載なし）", "url": "https://www.saimyoji.or.jp/", "checked": CHECKED},
    {"what": "高山寺：8:30〜17:00、石水院 一般1,000円・小学生500円、秋期入山料500円。2026年は10月3日〜12月上旬に入山料500円（小学生300円）（お知らせ「秋期拝観のご案内」2026-09-13）", "url": "https://kosanji.com/blog/", "checked": CHECKED},
    {"what": "お食事処（高雄保勝会）：とがの茶屋 9:00〜17:00 木曜定休（10/20〜11/30無休）、よしでん 9:00〜18:30 不定休、指月亭 10:00〜17:00 不定休・湯どうふ定食2,500円、硯石亭 9:00〜17:00、山本食堂 9:00〜18:00頃 シーズン中無休、錦水亭支店 9:00〜18:00 木曜定休、高雄茶屋 9:00〜17:00 不定休（10月〜12月上旬無休）・もみじ餅付お抹茶600円・柚子入もみじうどん800円", "url": "https://www.kyo-takao.com/shop/", "checked": CHECKED},
    {"what": "硯石亭：9〜17時、不定休（11月は無休、1・2月は休み）。おしながき（うどん・そば750円〜、秋期の湯豆腐の膳1,900円、もみじ餅700円、抹茶（菓子付）850円）、秋期11:00〜14:00はもみじ餅を販売停止することがある", "url": "http://www.suzuriishitei.com/", "checked": CHECKED},
    {"what": "仁和寺：御所庭園 3〜11月9:00〜17:00（16:30受付終了）、12〜2月9:00〜16:30（トップ）、大人800円（拝観・交通案内）。紅葉雲海ライトアップ 2026年10月24日〜12月13日の金土日祝、休止11月8日・28日、18:30〜21:00（受付20:30まで）、大人2,800円。市バス10系統で京阪三条駅から約40分（拝観・交通案内）", "url": "https://ninnaji.jp/news/event-34-2/", "checked": CHECKED},
    {"what": "北野天満宮：もみじ苑 2026年10月31日〜12月6日、9時〜16時（受付15時40分まで）、ライトアップ期間中は20時まで（受付19時40分まで）、大人1,500円（トップ）", "url": "https://kitanotenmangu.or.jp/", "checked": CHECKED},
    {"what": "紅葉の見ごろ（例年）：神護寺 11月上旬〜下旬、西明寺 11月10日前後、高山寺 11月中旬〜下旬（京都観光Navi 紅葉だより）", "url": MOMIJI, "checked": "2026-11-21"},
]

NOTE_HEAD = "京都 高雄の紅葉ルート（takao/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（takao.json＝9〜10時に出発、takao-early.json＝神護寺の開門に合わせる）。このファイル："
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（2024年11月19日の Nikon D7000 と iPhone。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "高山寺はオーナーが行っていない場所で、写真は Wikimedia Commons（photos の要素が {file, credit}）。"
             "info.source は確認した出典、info.checked は確認日、sources は時刻・料金の出典の一覧。このファイルは scripts/build_takao_data.py で作る（直接直さない）。")


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
            back = BACK_ROWS_TOGANOO if sid == "kosanji" else BACK_ROWS
            rows = rows + [r for r in back if r not in rows]
        tip, source = b.pop("_tip"), b.pop("_source")
        if sid == last:
            tip = T(tip["ja"] + BACK_TIP["ja"], tip["en"] + " " + BACK_TIP["en"])
        b["info"] = info(rows, source, tip=tip)
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        if NO[sid] == 1:
            out["gmaps"] = out["gmaps"] + [NIJO]
            # 1番のスポットには、紅葉の時期・バスの混雑・冬の茶屋のお知らせを必ず出す（期間つき）
            out["notices"] = [n for n in (SEASON, AUTUMN_BUS, WINTER) if n not in out.get("notices", [])] + out.get("notices", [])
        ja = body["ja"] + "\n\n" + go["ja"] + f"\n\n{lj}：{tj}"
        en = body["en"] + "\n\n" + go["en"] + f"\n\n{le}: {te}"
        if sid == last:
            ja += "\n\n" + AFTER["ja"]
            en += "\n\n" + AFTER["en"]
            out["links"] = out.get("links", []) + AFTER_LINKS
            out["notices"] = out.get("notices", []) + AFTER_NOTICES
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
