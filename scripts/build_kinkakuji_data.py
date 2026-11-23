#!/usr/bin/env python3
"""京都・金閣寺〜北野天満宮ルートのデータを、2つのコースぶん書き出す。

使い方: python3 scripts/build_kinkakuji_data.py（そのあと python3 scripts/sync_kinkakuji.py）
- 作るもの（COURSES）:
  - data/routes/kinkakuji.json … 早朝コース。龍安寺に開門（8:00）、金閣寺に開門（9:00）で入り、大徳寺・仁和寺・平野神社・北野天満宮へ
  - data/routes/kinkakuji-late.json … 9〜10時に出発するコース。北野天満宮から始めて、金閣寺は夕方に（大徳寺は入れない）
  どちらも直接直さない（文章・料金・時刻はこのファイルの中。直したら実行し直す）
- 出発は京都の中心・三条のあたり（河原町三条・京都市役所前のバス停）を想定
- スポットの文章は「共通の説明（body）＋コースごとの行き方・時間割（way）＋めやすの時間（time）」を組み立てる
- 番号はコースで変わるので、紹介ページ（kinkakuji/js/i18n.js）の写真はスポットの id で指定している
- 時刻・料金の出典と確認日は SOURCES（データの sources に入る）
- 写真は images/kinkakuji/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kinkakuji"
CHECKED = "2026-11-22"
TODAY = "2026-11-24"  # 「要確認」の調べ直しをした日（平野神社・大徳寺・北野天満宮・金閣寺・市バス運賃）
PICKS = {}
for f in os.listdir(IMG):
    m = re.match(r"(.+)-(\d+)\.jpg$", f)
    if m:
        PICKS.setdefault(m.group(1), []).append(int(m.group(2)))

# (コースの id, ファイル名, スポットの順番, [(一覧の区切りに入れるスポット, 紹介ページの「1日の流れ」の何番目か)])
COURSES = [
    ("early", "kinkakuji.json", ["ryoanji", "kinkakuji", "daitokuji", "ninnaji", "hirano", "kitano"],
     [(["ryoanji"], 0), (["kinkakuji"], 1), (["daitokuji"], 2), (["ninnaji"], 3), (["hirano", "kitano"], 4)]),
    ("late", "kinkakuji-late.json", ["kitano", "hirano", "ninnaji", "ryoanji", "kinkakuji"],
     [(["kitano", "hirano"], 0), (["ninnaji"], 1), (["ryoanji"], 2), (["kinkakuji"], 3)]),
]


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def info(rows, tip=None, checked=None):
    return {"rows": rows, "cash": False, "tip": tip, "checked": checked or CHECKED}


def notice(head_ja, head_en, ja, en, url=None, to=None):
    d = {"head": T(head_ja, head_en), "text": T(ja, en)}
    if url:
        d["url"] = url
    if to:
        d["to"] = to
    return d


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]


BUS_URL = "https://www2.city.kyoto.lg.jp/kotsu/busdia/bustime.htm"
RANDEN_URL = "https://www.keifuku.co.jp/randen_timetable.php"
TOYOUKE_URL = "http://www.toyoukeya.co.jp/"
IZUSEN_URL = "https://kyoto-izusen.com/html2/restrant_daijiin.html"
DAISEN_URL = "https://daisen-in.net/"
IZUSEN_PRICE_URL = "https://kyoto-izusen.com/wordpress/info/daijiin/4676/"
HIRANO_HOURS_URL = "https://ja.kyoto.travel/tourism/article/asakanko-yorukanko/post/single.php?id=85"
HIRANO_LIGHTUP_URL = "https://ja.kyoto.travel/event/single.php?event_id=4083"
KINKAKU_FAQ_URL = "https://www.shokoku-ji.jp/kinkakuji/faq/"
KITANO_FAQ_URL = "https://kitanotenmangu.or.jp/faq/"
BUS_FARE_URL = "https://www.city.kyoto.lg.jp/kotsu/page/0000240682.html"
SHUNJU = {"oubaiin": "https://kyotoshunju.com/temple/daitokuji-oubaiin/", "kohrinin": "https://kyotoshunju.com/temple/daitokuji-kohrinin/",
          "jukoin": "https://kyotoshunju.com/temple/daitokuji-jukoin2026/", "sokenin": "https://kyotoshunju.com/temple/daitokuji-sokenin/"}
RANDEN_ROW = row("train", "嵐電（北野白梅町〜御室仁和寺）約5分・250円（どこまで乗っても同じ）。日中は毎時03・13・23・33・43・53分発。運賃は降りるときに現金かICカードで",
                 "Randen tram (Kitano-Hakubaicho – Omuro-Ninnaji): about 5 min, flat ¥250. In the daytime, trams leave at :03, :13, :23, :33, :43 and :53. Pay as you get off, cash or IC card")

S = {
    "ryoanji": dict(
        name=T("龍安寺", "Ryoan-ji Temple"), kind=T("お寺", "Temple"),
        blurb=T("白砂に15の石を置いただけの石庭。縁側に座って、ゆっくり眺めてみてください。",
                "The rock garden: just fifteen stones on white gravel. Sit on the veranda and take your time."),
        lat=35.03346, lng=135.71809,
        body=T("龍安寺（りょうあんじ）\n\n白い砂に15個の石を置いただけの石庭。どこから見ても1つの石がほかの石にかくれて見えない、と言われています。方丈の縁側に座って、静かに眺めてみてください。\n\n"
               "石庭のほかに、大きな鏡容池（きょうようち）のまわりも歩けます。春の桜、秋の紅葉の時期もきれいです。",
               "Ryoan-ji Temple\n\nA rock garden of just fifteen stones on white gravel. It’s said that from any spot one stone is always hidden behind another. Sit on the veranda and look at it quietly.\n\n"
               "You can also walk around the large Kyoyo-chi pond. It’s lovely in the cherry-blossom and autumn-leaf seasons."),
        way={
            "early": T("早朝コースの最初の目的地です。河原町三条を7:11に出る市バス59系統（京都市役所前は7:13）に乗ると、「龍安寺前」に平日7:44、土日祝7:43に着きます。門の前で8:00の開門を待ちましょう。"
                       "1本前（6:48発）は7:20着で早すぎ、1本あとは8:00を過ぎます。運賃は230円、降りるときに払います。\n\n"
                       "12〜2月は開門が8:30です。河原町三条を平日7:43（8:21着）、土日祝7:34（8:06着）に出るバスにして、金閣寺までの時間を30分ずつ後ろにずらしてください。お昼からは同じ時間割に戻れます。\n\n"
                       "8:35ごろ出て、金閣寺へは「きぬかけの路」を歩いて20〜25分。歩きたくない人は、「龍安寺前」を平日8:43、土日祝8:53に出る59系統で「金閣寺道」まで約7分です。",
                       "The first goal of the early course. Take city bus 59 leaving Kawaramachi-Sanjo at 7:11 (Kyoto Shiyakusho-mae at 7:13); it reaches “Ryoanji-mae” at 7:44 on weekdays and 7:43 on weekends and holidays. Wait at the gate for the 8:00 opening. "
                       "The bus before (6:48) arrives at 7:20, too early, and the one after gets in past 8:00. The fare is ¥230, paid as you get off.\n\n"
                       "From December to February the temple opens at 8:30. Take the 7:43 bus on weekdays (arrives 8:21) or the 7:34 on weekends and holidays (arrives 8:06), and move everything up to Kinkaku-ji back by 30 minutes. From lunch on, the timetable is the same.\n\n"
                       "Leave at about 8:35 and walk the Kinukake-no-michi road to Kinkaku-ji, 20–25 minutes. If you’d rather not walk, bus 59 leaves “Ryoanji-mae” at 8:43 on weekdays and 8:53 on weekends and holidays; “Kinkakuji-michi” is about 7 minutes away."),
            "late": T("仁和寺の二王門から、きぬかけの路を歩いて約15分。午後の石庭を、縁側に座ってゆっくりどうぞ。12〜2月は16:30に閉まります。\n\n"
                      "15:00ごろ出て、金閣寺へは同じ道を歩いて20〜25分。バスなら「龍安寺前」15:13発か15:28発の市バス59系統で「金閣寺道」まで約7分（230円）です。",
                      "About 15 minutes on foot from Ninna-ji’s Niomon gate along the Kinukake-no-michi road. Sit on the veranda and take in the garden in the afternoon light. From December to February it closes at 16:30.\n\n"
                      "Leave at about 15:00. Kinkaku-ji is a 20–25 minute walk along the same road, or take city bus 59 from “Ryoanji-mae” at 15:13 or 15:28 to “Kinkakuji-michi”, about 7 minutes (¥230)."),
        },
        time={"early": ("8:00〜8:35（12〜2月は8:30〜9:05）", "8:00–8:35 (8:30–9:05 from December to February)"), "late": ("14:15〜15:00", "14:15–15:00")},
        caution=T("12〜2月は8:30に開き、16:30に閉まります", "December–February: opens 8:30, closes 16:30"),
        notices=[notice("開く時間が季節で変わります", "Opening time changes by season",
                        "3月1日〜11月30日は8:00〜17:00、12月1日〜2月末は8:30〜16:30です（公式サイト）。",
                        "1 March – 30 November: 8:00–17:00. 1 December – end of February: 8:30–16:30 (official website).", "http://www.ryoanji.jp/smph/")],
        gmaps=[gm("龍安寺", "Ryoan-ji", 35.03346, 135.71809, "龍安寺 石庭")],
        links=[link("official", "龍安寺 公式サイト", "Ryoan-ji (official)", "http://www.ryoanji.jp/smph/"),
               link("timetable", "市バス時刻表（京都市交通局）", "Kyoto city bus timetables (Japanese)", BUS_URL)],
        info=info([row("hours", "3月1日〜11月30日 8:00〜17:00、12月1日〜2月末 8:30〜16:30", "1 Mar – 30 Nov 8:00–17:00; 1 Dec – end of Feb 8:30–16:30"),
                   row("fee", "大人600円、高校生500円、小・中学生300円", "Adults ¥600, high school ¥500, elementary and junior high ¥300")],
                  tip=T("市バス59系統「龍安寺前」下車。バスの時刻は京都市交通局の時刻表（2026年3月20日改正）で確認しました。",
                        "Bus 59 to “Ryoanji-mae”. Bus times are from the Kyoto City Transportation Bureau timetable (revised 20 March 2026).")),
    ),
    "kinkakuji": dict(
        name=T("金閣寺（鹿苑寺）", "Kinkaku-ji (Rokuon-ji)"), kind=T("お寺", "Temple"),
        blurb=T("池に映る金色の舎利殿。写真は雪が積もった朝（2026年2月）のものです。",
                "The golden pavilion mirrored in its pond. The photos are from a snowy morning in February 2026."),
        lat=35.03937, lng=135.72924,
        body=T("金閣寺（きんかくじ）\n\n正式には鹿苑寺（ろくおんじ）。室町幕府の将軍・足利義満の山荘がはじまりで、金箔をはった舎利殿「金閣」が鏡湖池（きょうこち）に映る姿は、京都を代表する景色です。\n\n"
               "順路は一方通行で、池のほとりから金閣を眺めたあと、裏山の庭をぐるっと回って出口へ。30〜45分で回れます。晴れた日は、池に映る「逆さ金閣」も見てください。\n\n"
               "写真は雪が積もった2026年2月8日の朝。雪の日は屋根も松も白くなりますが、とても混みます。雪は昼までにとけることが多いので、雪の朝は9:00の開門に合わせて行くのがおすすめです。",
               "Kinkaku-ji (Rokuon-ji)\n\nOfficially Rokuon-ji. It began as the villa of the shogun Ashikaga Yoshimitsu, and its gold-leafed pavilion reflected in the Kyoko-chi pond is one of Kyoto’s defining views.\n\n"
               "The route is one-way: see the pavilion from the pond, then loop through the hillside garden to the exit. It takes 30–45 minutes. On a clear day, look for the pavilion’s reflection in the water.\n\n"
               "The photos are from the snowy morning of 8 February 2026. Snow turns the roofs and pines white, and brings big crowds. It often melts by midday, so on a snowy morning be here for the 9:00 opening."),
        way={
            "early": T("9:00の開門に合わせて入ります。団体が増える前の時間をねらったコースですが、桜や紅葉の時期、雪の朝は、開門から混むこともあります。\n\n"
                       "9:45ごろ出たら、ひと休み。朝ごはんの店は、朝の営業を公式サイトで確かめられたところがなく、店の名前は出していません。出発前に宿の近くで食べておくか、買っておくのが確実です。お茶なら、次の大徳寺の大仙院でお抹茶が飲めます。\n\n"
                       "大徳寺へは「金閣寺道」から市バス205系統（北大路バスターミナル・四条河原町行き）で約6分、「大徳寺前」で降ります（230円）。10時ごろは7〜9分おきに来ます。同じのりばの204・12系統でも行けます。",
                       "Be here for the 9:00 opening. This course aims for the hour before the tour groups build up, though in cherry or maple season, or on a snowy morning, it can be busy from the start.\n\n"
                       "Come out at about 9:45 and take a break. I couldn’t confirm on any official website a breakfast place that is open at this hour, so I don’t name one. The safe way is to eat near your hotel before you leave, or bring something. For tea, you can have matcha at Daisen-in in Daitoku-ji, the next stop.\n\n"
                       "For Daitoku-ji, take city bus 205 (for Kitaoji Bus Terminal and Shijo-Kawaramachi) from “Kinkakuji-michi” to “Daitokuji-mae”, about 6 minutes (¥230). Around 10:00 it comes every 7–9 minutes. Buses 204 and 12 from the same stop go there too."),
            "late": T("このコースでは最後、15:30ごろに入ります。10時から15時ごろは団体やツアーが重なりやすい時間だと言われているので、そこを外しました。それでも空いているとは限りません。閉門は17:00。16:15ごろまでに入れば、あわてずに回れます。\n\n"
                      "龍安寺から歩いてきた人は、そのまま入口へ。バスの人は「金閣寺道」から歩いて5分ほどです。\n\n"
                      "帰りは「金閣寺道」から市バス59系統で河原町三条へ約30分（230円）。平日は16:35発（17:05着）か16:50発（17:20着）、土日祝は16:40発（17:10着）か17:00発（17:30着）です。\n\n"
                      "夜は街なかで。河原町三条から三条通・木屋町・先斗町（ぽんとちょう）は歩いてすぐで、夕食の店を選びやすいあたりです。21〜22時ごろまでゆっくりできます。"
                      "11月13日〜12月6日（2026年）は、北野天満宮のもみじ苑のライトアップ（日没〜20:00、受付19:40まで）に寄ってから帰る手もあります。「金閣寺道」から205・204系統で「北野白梅町」へ、そこから歩いて約5分です。",
                      "On this course it comes last, at about 15:30. From around 10:00 to 15:00 is said to be when tour groups pile up, so the course avoids those hours. It may still be busy. The gate closes at 17:00; go in by about 16:15 and you won’t have to rush.\n\n"
                      "If you walked from Ryoan-ji, go straight to the entrance. From the “Kinkakuji-michi” bus stop it’s about 5 minutes on foot.\n\n"
                      "To go back, take city bus 59 from “Kinkakuji-michi” to Kawaramachi-Sanjo, about 30 minutes (¥230): on weekdays at 16:35 (arrives 17:05) or 16:50 (17:20); on weekends and holidays at 16:40 (17:10) or 17:00 (17:30).\n\n"
                      "Spend the evening downtown. From Kawaramachi-Sanjo, Sanjo-dori, Kiyamachi and Pontocho are a short walk, with plenty of places for dinner, and you can stay out until 21:00–22:00. "
                      "From 13 November to 6 December 2026 you could instead stop at the maple garden light-up at Kitano Tenmangu (sunset to 20:00, last entry 19:40): take bus 205 or 204 from “Kinkakuji-michi” to “Kitano-Hakubaicho”, then walk about 5 minutes."),
        },
        time={"early": ("9:00〜9:45", "9:00–9:45"), "late": ("15:30〜16:20", "15:30–16:20")},
        notices=[notice("お守りとご朱印は現金で", "Amulets and goshuin: cash",
                        "拝観料は現金のほか、キャッシュレス決済（おまいりPay）でも払えます。お守りなどの授与品とご朱印は、キャッシュレスの対象外です（公式サイト）。",
                        "Admission can be paid in cash or by cashless payment (Omairi Pay). Amulets and goshuin stamps are not covered by cashless payment (official website).",
                        "https://www.shokoku-ji.jp/kinkakuji/access/"),
                 notice("撮影は個人で楽しむスナップだけ", "Photos: personal snapshots only",
                        "境内の撮影は、個人で楽しむ範囲の小型カメラでのスナップに限られています。SNSなどで公開するための撮影、団体写真、動画の配信、ドローンは断られています（公式サイトのよくある質問）。",
                        "Inside the grounds, only snapshots with a small camera for personal enjoyment are allowed. Photos taken to publish (including on social media), group photos, live-streaming and drones are not (official FAQ).",
                        KINKAKU_FAQ_URL)],
        gmaps=[gm("金閣寺", "Kinkaku-ji", 35.03937, 135.72924, "金閣寺 鹿苑寺")],
        links=[link("official", "金閣寺 公式サイト（アクセス・参拝料金）", "Kinkaku-ji (official)", "https://www.shokoku-ji.jp/kinkakuji/access/", "https://www.shokoku-ji.jp/en/kinkakuji/"),
               link("timetable", "市バス時刻表（京都市交通局）", "Kyoto city bus timetables (Japanese)", BUS_URL)],
        info=info([row("hours", "9:00〜17:00（年中無休）。受付の締め切り時刻は公式サイトに書かれていません（要確認）",
                       "9:00–17:00, open every day. The official website doesn’t give a last-entry time (please check)"),
                   row("fee", "大人（高校生以上）500円、小・中学生300円", "Adults (high school and up) ¥500; elementary and junior high ¥300")],
                  tip=T("市バス「金閣寺道」（12・59・204・205系統など）から歩きます。", "Walk from the “Kinkakuji-michi” city bus stop (buses 12, 59, 204, 205 and others)."),
                  checked=TODAY),
    ),
    "daitokuji": dict(
        name=T("大徳寺", "Daitoku-ji Temple"), kind=T("お寺", "Temple"),
        blurb=T("土塀と石畳の道に、たくさんの塔頭（たっちゅう）が並ぶ大きな禅寺。ここで休憩とお昼にします。",
                "A vast Zen temple of earthen walls and stone paths lined with sub-temples. Rest and have lunch here."),
        lat=35.04279, lng=135.74655,
        body=T("大徳寺（だいとくじ）\n\n臨済宗大徳寺派の大本山。広い境内に、土塀に囲まれた塔頭（小さなお寺）が並び、松と石畳の道を歩くだけでも気持ちのいい場所です。"
               "朱色の三門（金毛閣）は、千利休ゆかりの門として知られています。最後の写真は、塔頭のひとつ黄梅院（おうばいいん）の門。門の中に青もみじと苔の庭が見えます。\n\n"
               "庭を公開している塔頭もありますが、公開日・時間・拝観料はそれぞれちがいます。入る前に、門の前の案内を見てください。"
               "時期によって、ふだん閉じている塔頭の特別公開もあります。",
               "Daitoku-ji Temple\n\nHead temple of the Daitoku-ji school of Rinzai Zen. Its grounds are lined with walled sub-temples, and simply walking the pine-shaded stone paths is a pleasure. "
               "The vermilion Sanmon gate (Kinmokaku) is famous for its links to the tea master Sen no Rikyu. The last photo is the gate of Obai-in, one of the sub-temples, with green maples and moss inside.\n\n"
               "Some sub-temples open their gardens, but days, hours and fees differ for each. Check the sign at the gate before you go in. "
               "At some times of year, sub-temples that are normally closed hold special openings."),
        way={
            "early": T("金閣寺道からバスで約6分、10:10ごろ着きます。まず石畳の道を歩いて、三門へ。\n\n"
                       "ひと休みするなら大仙院（だいせんいん）。枯山水の庭を見たあと、お抹茶（500円）が飲めます。拝観は大人500円、ふだんは9:00〜16:30。法要などで昼に閉まる日や早く閉まる日があるので、公式サイトのカレンダーでその日の時間を見てください。\n\n"
                       "お昼は11:15ごろ、境内にある「泉仙（いずせん）大慈院店」の精進料理はどうでしょう。11:00〜16:00（ラストオーダー）、休みは12月28〜31日だけ。精進料理は「あやめ」4,500円、「ゆり」5,500円、「ぼたん」6,500円です（税込。2026年9月1日からの値段）。6人以上は予約が必要です。"
                       "もっと手軽に食べたい人向けの店は、昼の営業を公式サイトで確かめられたところがなく、名前は出していません。\n\n"
                       "食べ終わったら、「大徳寺前」12:19発の市バス205系統（金閣寺・西大路四条行き）で「北野白梅町」へ（12:30着、230円）。嵐電の北野白梅町駅から12:43発に乗ると、御室仁和寺駅に12:48に着きます。205系統は7〜8分おき、嵐電は10分おきなので、乗りおくれても次ですぐ行けます。",
                       "About 6 minutes by bus from Kinkakuji-michi, arriving around 10:10. Walk the stone paths to the Sanmon gate first.\n\n"
                       "For a rest, try Daisen-in: after its dry landscape garden you can have a bowl of matcha (¥500). Admission is ¥500 for adults, and it is normally open 9:00–16:30. On some days it closes over midday or early for ceremonies, so check that day’s hours on the calendar on its website.\n\n"
                       "For lunch at about 11:15, there’s Izusen Daiji-in, a Buddhist vegetarian restaurant inside the temple grounds. It’s open 11:00–16:00 (last order) and closed only 28–31 December. The set meals are “Ayame” ¥4,500, “Yuri” ¥5,500 and “Botan” ¥6,500 (tax included; prices from 1 September 2026). Groups of six or more must book. "
                       "I couldn’t confirm on an official website a cheaper place nearby that is open for lunch, so I don’t name one.\n\n"
                       "After lunch take city bus 205 (for Kinkaku-ji and Nishioji-Shijo) from “Daitokuji-mae” at 12:19 to “Kitano-Hakubaicho” (arrives 12:30, ¥230). The 12:43 Randen tram from Kitano-Hakubaicho station gets to Omuro-Ninnaji at 12:48. Bus 205 runs every 7–8 minutes and the tram every 10, so if you miss one the next is close behind."),
        },
        time={"early": ("10:10〜12:15（休憩とお昼を含む）", "10:10–12:15 (with a rest and lunch)")},
        caution=T("塔頭は公開日・時間・料金がそれぞれちがいます", "Each sub-temple has its own days, hours and fees"),
        notices=[notice("大仙院は日によって時間が変わります", "Daisen-in’s hours vary by day",
                        "ふだんは9:00〜16:30ですが、昼に閉まる日や14:30に閉まる日があります。公式サイトのカレンダーに、日ごとの拝観時間が出ています。",
                        "Normally 9:00–16:30, but on some days it closes over midday or at 14:30. The calendar on its website shows the hours for each day.", DAISEN_URL)],
        gmaps=[gm("大徳寺", "Daitoku-ji", 35.04279, 135.74655, "大徳寺 京都市北区")],
        links=[link("info", "臨黄ネット（大徳寺の案内）", "Rinzai-Obaku Zen (Daitoku-ji, Japanese)", "https://www.rinnou.net/cont_03/07daitoku/"),
               link("official", "大仙院 公式サイト（日ごとの拝観時間）", "Daisen-in (official, Japanese)", DAISEN_URL),
               link("official", "泉仙 大慈院店 公式サイト", "Izusen Daiji-in (official, Japanese)", IZUSEN_URL),
               link("info", "黄梅院の特別公開（京都春秋）", "Obai-in special opening (Kyoto Shunju, Japanese)", SHUNJU["oubaiin"]),
               link("timetable", "市バス時刻表（京都市交通局）", "Kyoto city bus timetables (Japanese)", BUS_URL)],
        info=info([row("hours", "大仙院 9:00〜16:30（日によって変わります）。泉仙 大慈院店 11:00〜16:00（ラストオーダー）", "Daisen-in 9:00–16:30 (varies by day). Izusen Daiji-in 11:00–16:00 (last order)"),
                   row("fee", "大仙院 大人500円、小・中学生300円、お抹茶500円。泉仙 大慈院店の精進料理 4,500円・5,500円・6,500円（税込）",
                       "Daisen-in: adults ¥500, elementary and junior high ¥300, matcha ¥500. Izusen Daiji-in set meals: ¥4,500, ¥5,500, ¥6,500 (tax included)"),
                   row("closed", "大仙院は年中無休。泉仙 大慈院店は12月28〜31日", "Daisen-in: open all year. Izusen Daiji-in: closed 28–31 December"),
                   row("hours", "秋の特別公開・総見院（2026年11月30日まで）10:00〜16:00受付終了、大人800円、現金のみ",
                       "Autumn special opening, Soken-in (until 30 Nov 2026): 10:00–16:00 last entry, adults ¥800, cash only", until="2026-11-30"),
                   row("hours", "秋の特別公開・黄梅院（2026年12月6日まで）10:00〜15:45受付終了、大人1,000円、現金のみ",
                       "Autumn special opening, Obai-in (until 6 Dec 2026): 10:00–15:45 last entry, adults ¥1,000, cash only", until="2026-12-06"),
                   row("hours", "秋の特別公開・聚光院（2026年12月6日まで）9:30〜15:30受付終了、大人1,000円、現金のみ。未就学児は入れません。11月27〜29日は休み。境内は撮影禁止",
                       "Autumn special opening, Juko-in (until 6 Dec 2026): 9:30–15:30 last entry, adults ¥1,000, cash only. No preschool children. Closed 27–29 Nov. No photography", until="2026-12-06"),
                   row("hours", "秋の特別公開・興臨院（2026年12月15日まで）10:00〜16:30受付終了（12月1日からは16:00）、大人800円、現金のみ。庭園以外は撮影禁止",
                       "Autumn special opening, Korin-in (until 15 Dec 2026): 10:00–16:30 last entry (16:00 from 1 Dec), adults ¥800, cash only. Photography in the garden only", until="2026-12-15")],
                  tip=T("大仙院と泉仙は公式サイト、秋の特別公開は主催の京都春秋の案内で確認しました（法要で休む日が増えることがあります）。ほかの塔頭の公開日・料金は公式で確かめられませんでした（要確認）。",
                        "Daisen-in and Izusen were checked on their websites, and the autumn special openings on the organiser Kyoto Shunju’s pages (extra closures for ceremonies are possible). Opening days and fees of the other sub-temples could not be confirmed officially (please check)."),
                  checked=TODAY),
    ),
    "ninnaji": dict(
        name=T("仁和寺", "Ninna-ji Temple"), kind=T("お寺", "Temple"),
        blurb=T("五重塔と、背の低い遅咲きの「御室桜（おむろざくら）」。見ごろは4月中ごろです。",
                "A five-storey pagoda and the low, late-blooming Omuro cherries, at their best around mid-April."),
        lat=35.02981, lng=135.71415,
        body=T("仁和寺（にんなじ）\n\n大きな二王門をくぐると、広い境内の奥に五重塔と金堂が建っています。境内を歩くのは、桜の時期以外は無料。御所庭園（800円）は、御殿の建物と庭を見て回る有料のエリアです。全部で1時間は見ておきましょう。\n\n"
               "中門の内側の御室桜は、背が低く、花が目の高さで咲く遅咲きの桜。京都の桜の中では遅めの、4月中ごろが見ごろです（写真は2025年4月17日）。"
               "桜の時期（御室花まつり）は特別入山料がかかります。",
               "Ninna-ji Temple\n\nPass through the huge Niomon gate, and the five-storey pagoda and the main hall stand at the back of the wide grounds. Outside cherry season the grounds are free. The palace garden (¥800) is the paid area, where you walk through the palace buildings and see their gardens. Allow an hour in all.\n\n"
               "Inside the middle gate, the Omuro cherries are short trees whose blossoms open at eye level, and late: they peak around mid-April, later than most in Kyoto (photos: 17 April 2025). "
               "In cherry season (the Omuro Flower Festival) there’s a special entry fee."),
        way={
            "early": T("嵐電の御室仁和寺駅から、まっすぐ歩いて約3分で二王門です。\n\n"
                       "14:15ごろ出て、御室仁和寺駅14:23発の嵐電で北野白梅町へ（14:28着）。運賃は250円で、降りるときに現金かICカードで払います。北野白梅町駅から平野神社までは、北へ歩いて約7分です。",
                       "From Randen’s Omuro-Ninnaji station it’s about 3 minutes straight ahead to the Niomon gate.\n\n"
                       "Leave at about 14:15 and take the 14:23 tram from Omuro-Ninnaji to Kitano-Hakubaicho (arrives 14:28). The fare is ¥250, paid in cash or by IC card as you get off. From Kitano-Hakubaicho station, Hirano Shrine is about 7 minutes’ walk north."),
            "late": T("北野白梅町駅を12:33に出る嵐電に乗ると、御室仁和寺駅に12:38に着きます（250円。降りるときに現金かICカードで）。駅からまっすぐ歩いて約3分で二王門です。\n\n"
                      "お昼がまだの人へ。お弁当は、霊宝館の向かいの広場で食べられます（お酒は持ち込めません。ごみは持ち帰り）。\n\n"
                      "14:00ごろ出て、二王門の前の「きぬかけの路」を東へ歩いて約15分で龍安寺です。",
                      "The 12:33 Randen tram from Kitano-Hakubaicho reaches Omuro-Ninnaji at 12:38 (¥250, paid in cash or by IC card as you get off). From the station it’s about 3 minutes straight ahead to the Niomon gate.\n\n"
                      "Haven’t had lunch? You may eat a packed lunch in the open space opposite the Reihokan treasure hall (no alcohol; take your rubbish with you).\n\n"
                      "Leave at about 14:00 and walk east along the Kinukake-no-michi road in front of the gate; Ryoan-ji is about 15 minutes away."),
        },
        time={"early": ("12:55〜14:15", "12:55–14:15"), "late": ("12:45〜14:00", "12:45–14:00")},
        notices=[notice("御所庭園の受付は閉まる30分前まで", "Palace garden: last entry 30 min before closing",
                        "3〜11月は16:30、12〜2月は16:00で受付が終わります。霊宝館とお堂の中は撮影できません（公式サイト）。",
                        "Last entry is 16:30 from March to November and 16:00 from December to February. No photography inside the treasure hall or the temple halls (official website).",
                        "https://ninnaji.jp/visit/")],
        gmaps=[gm("仁和寺", "Ninna-ji", 35.02981, 135.71415, "仁和寺"),
               gm("嵐電 御室仁和寺駅", "Randen Omuro-Ninnaji Station", 35.02645, 135.71396, "嵐電 御室仁和寺駅")],
        links=[link("official", "仁和寺 公式サイト（拝観・交通案内）", "Ninna-ji (official)", "https://ninnaji.jp/visit/", "https://ninnaji.jp/en/"),
               link("timetable", "嵐電 時刻表（京福電気鉄道）", "Randen tram timetables (Japanese)", RANDEN_URL)],
        info=info([row("hours", "御所庭園 3〜11月 9:00〜17:00（受付16:30まで）、12〜2月 9:00〜16:30（受付16:00まで）", "Palace garden: Mar–Nov 9:00–17:00 (last entry 16:30); Dec–Feb 9:00–16:30 (last entry 16:00)"),
                   row("fee", "御所庭園 大人800円（高校生以下は無料）。霊宝館（期間限定）大人500円。御室花まつりの特別入山料 大人800円",
                       "Palace garden ¥800 (high school and under free). Treasure hall (limited periods) ¥500. Omuro Flower Festival special entry ¥800 per adult"),
                   RANDEN_ROW],
                  tip=T("拝観は仁和寺の公式サイト、嵐電は京福電気鉄道の公式サイトで確認しました。", "Temple details checked on Ninna-ji’s website; the tram on the Keifuku Electric Railroad website.")),
    ),
    "hirano": dict(
        name=T("平野神社", "Hirano Shrine"), kind=T("神社", "Shrine"),
        blurb=T("約60種・400本の桜がある、夜桜の名所。桜の時期は夕暮れからがおすすめです。",
                "About 400 cherry trees of some 60 kinds, known for blossoms at night. In cherry season, come at dusk."),
        lat=35.03238, lng=135.73248,
        body=T("平野神社（ひらのじんじゃ）\n\n平安時代から桜が植えられてきた神社で、今は約60種・400本の桜があります。江戸時代から「平野の夜桜」として知られる花見の名所です。\n\n"
               "3月中ごろの早咲きの桜から4月下旬の八重桜まで、長い期間いろいろな桜が楽しめます。写真は2025年4月5日の夕方〜夜。"
               "2026年の春は3月28日〜4月12日に夜桜のライトアップ（日没〜21:00ごろ、桜苑500円）がありました。来春の日程と料金はまだ発表されていません（要確認）。\n\n"
               "参拝は6:00〜17:00（京都市観光協会の京都観光Navi、2026年6月時点）。桜の時期以外は静かな神社で、20〜30分あれば回れます。",
               "Hirano Shrine\n\nCherry trees have been planted here since the Heian period; today there are about 400 trees of some 60 kinds, and “Hirano’s night cherries” have been famous since the Edo period.\n\n"
               "From early blossoms in mid-March to double-flowered ones in late April, something is in bloom for a long season. The photos were taken at dusk on 5 April 2025. "
               "In spring 2026 the blossoms were lit up from 28 March to 12 April (sunset to about 21:00; cherry garden ¥500). Next spring’s dates and fee have not been announced yet (please check).\n\n"
               "Open for worship 6:00–17:00 (Kyoto City Tourism Association’s Kyoto Navi, as of June 2026). Outside cherry season it’s a quiet shrine that takes 20–30 minutes."),
        way={
            "early": T("嵐電の北野白梅町駅から、北へ歩いて約7分。15:00ごろ出て、北野天満宮へは南東へ歩いてすぐです。",
                       "About 7 minutes’ walk north of Randen’s Kitano-Hakubaicho station. Leave at about 15:00; Kitano Tenmangu is a short walk to the southeast."),
            "late": T("お昼のあと、北野天満宮から北西へ歩いてすぐ。12:25ごろ出て、嵐電の北野白梅町駅まで南へ歩いて約7分。12:33発の嵐電で御室仁和寺へ向かいます（10分おきなので、乗りおくれても次ですぐ行けます）。",
                      "After lunch, a short walk northwest of Kitano Tenmangu. Leave at about 12:25 and walk about 7 minutes south to Randen’s Kitano-Hakubaicho station for the 12:33 tram to Omuro-Ninnaji (they run every 10 minutes, so the next one is never far off)."),
        },
        time={"early": ("14:35〜15:00（春は夕方も）", "14:35–15:00 (or at dusk in spring)"), "late": ("12:00〜12:25", "12:00–12:25")},
        notices=[],
        gmaps=[gm("平野神社", "Hirano Shrine", 35.03238, 135.73248, "平野神社 京都市北区")],
        links=[link("official", "平野神社 公式サイト（平野神社の桜）", "Hirano Shrine (official)", "https://www.hiranojinja.com/home/cherry"),
               link("info", "京都観光Navi（早朝から参拝できる社寺）", "Kyoto Navi: temples and shrines open early (Japanese)", HIRANO_HOURS_URL),
               link("timetable", "嵐電 時刻表（京福電気鉄道）", "Randen tram timetables (Japanese)", RANDEN_URL)],
        info=info([row("hours", "参拝 6:00〜17:00（授与所 9:00〜17:00）", "Open 6:00–17:00 (amulet counter 9:00–17:00)"),
                   row("fee", "2026年春の夜桜ライトアップ（3月28日〜4月12日、日没〜21:00ごろ）は桜苑500円。2027年の日程・料金は未発表（要確認）",
                       "During the spring 2026 light-up (28 Mar – 12 Apr, sunset to about 21:00) the cherry garden was ¥500. Dates and fee for 2027 not yet announced (please check)"),
                   RANDEN_ROW],
                  tip=T("参拝時間と2026年春のライトアップは、京都市観光協会の京都観光Naviで確認しました（平野神社の公式サイトには書かれていません）。嵐電は京福電気鉄道の公式サイトで確認しました。",
                        "Hours and the spring 2026 light-up were checked on Kyoto Navi, the Kyoto City Tourism Association’s site (the shrine’s own website doesn’t list them). The tram was checked on the Keifuku Electric Railroad website."),
                  checked=TODAY),
    ),
    "kitano": dict(
        name=T("北野天満宮", "Kitano Tenmangu Shrine"), kind=T("神社", "Shrine"),
        blurb=T("学問の神さま・菅原道真をまつる「天神さん」。秋はもみじ苑の夜のライトアップも。",
                "“Tenjin-san”, the shrine of Sugawara no Michizane, god of learning. Autumn brings evening light-ups in the maple garden."),
        lat=35.03048, lng=135.73492,
        body=T("北野天満宮（きたのてんまんぐう）\n\n学問の神さまとして知られる菅原道真（すがわらのみちざね）をまつる神社で、京都の人には「天神さん」と呼ばれています。受験の合格をお願いする人も多く、境内には道真が好んだ梅の木がたくさんあります。\n\n"
               "境内の西側の「もみじ苑」は、秋だけ公開される紅葉の名所。紙屋川（かみやがわ）に架かる朱色の橋のまわりが紅葉で埋まり、夜はライトアップされます（写真）。春には梅苑が公開されます（どちらも有料。苑の中で三脚は使えません）。",
               "Kitano Tenmangu Shrine\n\nThe shrine of Sugawara no Michizane, revered as the god of learning, known locally as “Tenjin-san”. Many come to pray for exam success, and the grounds are full of the plum trees Michizane loved.\n\n"
               "On the west side, the Momiji-en maple garden opens only in autumn: red maples crowd round the vermilion bridge over the Kamiya river, and they are lit up in the evening (the photos). In spring the plum garden opens (both charge entry; no tripods inside)."),
        way={
            "early": T("15:10ごろ着きます。本殿にお参りして、境内をひと回り。秋はもみじ苑、春は梅苑へ。本殿の前の三光門は、閉門の30分前に閉まります。\n\n"
                       "16:30ごろ東の門を出ると、花街の上七軒（かみしちけん）です。お茶屋の並ぶ通りを、千本今出川のほうへ10分ほど歩いてみてください。\n\n"
                       "夜の過ごし方は3つ。\n"
                       "・11月13日〜12月6日（2026年）は、もみじ苑のライトアップ（日没〜20:00、受付19:40まで）。\n"
                       "・北野・上七軒で夕食。夜の営業を公式サイトで確かめられた店がなく、名前は出していません。\n"
                       "・街なかへ戻る。「北野天満宮前」から市バス10系統で河原町三条まで約25分（230円）。17時台は10・30・50分発、18時台は平日10・30・50分、土日祝15・45分発。河原町三条から三条通・木屋町・先斗町（ぽんとちょう）は歩いてすぐです。河原町三条まで行く10系統は21:34発が最後です。",
                       "You arrive at about 15:10. Pray at the main hall and walk round the grounds; in autumn add the maple garden, in spring the plum garden. The Sanko-mon gate in front of the main hall shuts 30 minutes before the shrine closes.\n\n"
                       "Leave by the east gate at about 16:30 and you’re in Kamishichiken, a geisha district. Walk its street of teahouses toward Senbon-Imadegawa, about 10 minutes.\n\n"
                       "Three ways to spend the evening:\n"
                       "· From 13 November to 6 December 2026, the maple garden light-up (sunset to 20:00, last entry 19:40).\n"
                       "· Dinner around Kitano and Kamishichiken. I couldn’t confirm any restaurant’s evening hours on an official website, so I don’t name one.\n"
                       "· Back downtown: city bus 10 from “Kitano Tenmangu-mae” to Kawaramachi-Sanjo takes about 25 minutes (¥230). It leaves at :10, :30 and :50 in the 17:00 hour; in the 18:00 hour at :10, :30, :50 on weekdays and :15, :45 on weekends and holidays. From Kawaramachi-Sanjo, Sanjo-dori, Kiyamachi and Pontocho are a short walk. The last bus 10 that goes as far as Kawaramachi-Sanjo leaves at 21:34."),
            "late": T("このコースのスタートです。河原町三条を9:31に出る市バス10系統（京都市役所前は9:33）に乗ると、「北野天満宮前」に9:57に着きます（毎日同じ時刻、230円）。次の便は9:51発、10:17着です。\n\n"
                      "楼門から本殿へお参りして、境内をひと回り。秋はもみじ苑、春は梅苑へ。\n\n"
                      "お昼は早めに。北野天満宮前の「とようけ茶屋」は、豆腐屋さんがやっている昼だけの店で、とようけ丼（豆腐の丼）、生ゆば丼、湯豆腐が食べられます。11:00〜14:30（ラストオーダー14:00）、木曜と金曜が休み（25日と祝日は営業）。11:00の開店に合わせて行きましょう。"
                      "木曜・金曜に行く人向けの店は、昼の営業を公式サイトで確かめられたところがなく、名前は出していません。お弁当を買って、仁和寺の広場（霊宝館の向かい）で食べることもできます。",
                      "This course starts here. Take city bus 10 leaving Kawaramachi-Sanjo at 9:31 (Kyoto Shiyakusho-mae at 9:33); it reaches “Kitano Tenmangu-mae” at 9:57 (same time every day, ¥230). The next one leaves at 9:51 and arrives at 10:17.\n\n"
                      "Walk through the tower gate to the main hall and round the grounds; in autumn add the maple garden, in spring the plum garden.\n\n"
                      "Have an early lunch. Toyouke-jaya, in front of the shrine, is a lunch-only place run by a tofu maker: tofu on rice (Toyouke-don), fresh yuba on rice, or simmered tofu. Open 11:00–14:30 (last order 14:00), closed Thursdays and Fridays (open on the 25th and on holidays). Be there when it opens at 11:00. "
                      "For Thursdays and Fridays I couldn’t confirm another lunch place on an official website, so I don’t name one. You could also buy a packed lunch and eat it at Ninna-ji, in the open space opposite the treasure hall."),
        },
        time={"early": ("15:10〜16:30（秋はライトアップの時間も）", "15:10–16:30 (plus the light-up hours in autumn)"), "late": ("10:00〜10:55、お昼 11:00〜11:50", "10:00–10:55, lunch 11:00–11:50")},
        caution=T("閉門の時間は時期で変わります。毎月25日は縁日", "Closing time varies by season · market day on the 25th"),
        notices=[notice("閉門の時間は時期で変わります", "Closing time varies",
                        "開門は7:00。もみじ苑のライトアップ期間（2026年は12月6日まで）は20:00ごろまで開いています（公式サイトのトップは「7時〜20時」）。ふだんの閉門は17:00です（公式サイトの「よくある質問」。京都観光Naviも同じ）。お正月や催しの日は変わることがあるので、行く前に公式サイトで確かめてください。本殿の前の三光門は、閉門の30分前に閉まります。",
                        "The gates open at 7:00. During the maple garden light-up (until 6 December in 2026) they stay open until about 20:00 (the website’s top page says 7:00–20:00). Normally they close at 17:00 (the website’s FAQ; Kyoto Navi says the same). Times can change at New Year and on event days, so check the website before you go. The Sanko-mon gate in front of the main hall shuts 30 minutes before closing.",
                        KITANO_FAQ_URL),
                 notice("毎月25日は縁日です", "The 25th is market day",
                        "「天神さんの日」。参道に一日じゅう露店が並び、日没からは境内がライトアップされます（公式サイト）。にぎやかな日なので、時間に余裕を見てください。",
                        "On “Tenjin-san’s day” stalls line the approach all day, and the grounds are lit up from sunset (official website). It’s a lively day, so allow extra time.",
                        "https://kitanotenmangu.or.jp/event/")],
        gmaps=[gm("北野天満宮", "Kitano Tenmangu", 35.03048, 135.73492, "北野天満宮")],
        links=[link("official", "北野天満宮 公式サイト", "Kitano Tenmangu (official, Japanese)", "https://kitanotenmangu.or.jp/"),
               link("timetable", "市バス時刻表（京都市交通局）", "Kyoto city bus timetables (Japanese)", BUS_URL)],
        late_links=[link("official", "とようけ茶屋（とようけ屋山本 公式サイト）", "Toyouke-jaya (official, Japanese)", TOYOUKE_URL)],
        info=info([row("hours", "開門 7:00。閉門はライトアップ期間は20:00ごろ、ふだんは17:00（公式サイトのよくある質問）。三光門は閉門の30分前まで",
                       "Gates open 7:00; close about 20:00 during the light-up, otherwise 17:00 (official FAQ). Sanko-mon gate shuts 30 min before closing"),
                   row("hours", "もみじ苑（2026年10月31日〜12月6日）9:00〜16:00（受付15:40まで）。ライトアップ（11月13日〜12月6日）は20:00まで（受付19:40まで）",
                       "Maple garden (31 Oct – 6 Dec 2026) 9:00–16:00 (last entry 15:40); until 20:00 during the light-up, 13 Nov – 6 Dec (last entry 19:40)", until="2026-12-06"),
                   row("fee", "もみじ苑 大人（中学生以上）1,500円、小学生700円", "Maple garden: ¥1,500 (junior high and up), ¥700 (elementary)", until="2026-12-06"),
                   row("fee", "もみじ苑（秋）と梅苑（春）は有料です。公開の時期と料金は公式サイトで発表されます",
                       "The maple garden (autumn) and plum garden (spring) charge entry; dates and fees are announced on the website")],
                  tip=T("市バス10・50・51・55・203系統「北野天満宮前」下車すぐ。嵐電の北野白梅町駅から歩いて約5分。",
                        "Right by the “Kitano Tenmangu-mae” stop (buses 10, 50, 51, 55, 203). About 5 minutes’ walk from Randen’s Kitano-Hakubaicho station."),
                  checked=TODAY),
    ),
}

# とようけ茶屋の時間は、9〜10時出発コースの北野天満宮にだけ出す
LATE_KITANO_ROWS = [
    row("hours", "とようけ茶屋 11:00〜14:30（ラストオーダー14:00）", "Toyouke-jaya: 11:00–14:30 (last order 14:00)"),
    row("closed", "とようけ茶屋 木曜・金曜（25日と祝日は営業）、2026年12月31日〜2027年1月3日", "Toyouke-jaya: Thursdays and Fridays (open on the 25th and on holidays), and 31 Dec 2026 – 3 Jan 2027"),
]

SOURCES = [
    {"what": "龍安寺の拝観時間（3月1日〜11月30日 8:00〜17:00、12月1日〜2月末 8:30〜16:30）と拝観料（公式サイトのトップ）", "url": "http://www.ryoanji.jp/smph/", "checked": CHECKED},
    {"what": "金閣寺の参拝時間（9:00〜17:00・年中無休）、参拝料金、支払い方法（現金とおまいりPay。授与品とご朱印は対象外）、最寄りのバス停（公式サイト）。最終の受付時刻はこのページにも、よくある質問にも記載なし（要確認）", "url": "https://www.shokoku-ji.jp/kinkakuji/access/", "checked": TODAY},
    {"what": "金閣寺のよくある質問：開門時間 9:00〜17:00。境内の写真・動画の撮影は、個人で楽しむ範囲での小型カメラによるスナップ撮影に限る。第三者に公表する目的（SNS等を含む）・営利目的の撮影、団体写真、動画の配信、ドローンは禁止", "url": KINKAKU_FAQ_URL, "checked": TODAY},
    {"what": "仁和寺の拝観料と交通（公式サイト「拝観・交通案内」）、御所庭園 9:00〜17:00・16:30受付終了（公式サイトのトップ）、12〜2月は9:00〜16:30・受付は閉まる30分前まで・桜の時期以外は境内無料（公式サイトの英語ページ）、お弁当は霊宝館向かい広場・堂内は撮影不可・拝観は約1時間（よくある質問）", "url": "https://ninnaji.jp/visit/", "checked": CHECKED},
    {"what": "北野天満宮：トップは「開門時間 7時〜20時」「授与所 9時〜19時30分」（もみじ苑のライトアップ期間中に確認）。もみじ苑 令和8年10月31日〜12月6日 9時〜16時（最終受付15時40分）、ライトアップ 11月13日〜12月6日 日没〜20時（最終受付19時40分）、大人（中学生以上）1500円・小人（小学生）700円、三脚不可（トップ）。毎月25日のご縁日（年中行事）、バスの系統と北野白梅町駅から徒歩5分（アクセス）", "url": "https://kitanotenmangu.or.jp/", "checked": TODAY},
    {"what": "北野天満宮のよくある質問：「開門時間は現在、7:00〜17:00」、御本殿前三光門は閉門の30分前に閉門、正月期間や催し等で開閉門時間が変わる場合あり、休みなし、授与所9:00〜16:30", "url": KITANO_FAQ_URL, "checked": TODAY},
    {"what": "京都観光Navi「早朝から参拝・拝観できる京都の社寺」（京都市観光協会、2026年6月現在の情報）：北野天満宮 参拝7:00〜17:00・本殿前での参拝は16:30まで。平野神社 開門6:00、参拝・拝観6:00〜17:00、授与所9:00〜17:00", "url": HIRANO_HOURS_URL, "checked": TODAY},
    {"what": "平野神社：北野白梅町駅から北へ徒歩7分（公式サイトの交通案内）。開門・閉門の時間と桜苑の料金は、公式サイト（トップ・お知らせ・お問合せ・交通案内・平野神社の桜・English page）には記載なし", "url": "https://www.hiranojinja.com/home/otoiawase", "checked": TODAY},
    {"what": "平野神社の桜ライトアップ（京都観光Navi、終了済みのイベント）：2026年3月28日〜4月12日、日没から21:00頃、「桜苑500円、フリーパス1000円」、問い合わせは平野神社。2027年の日程・料金は未発表", "url": HIRANO_LIGHTUP_URL, "checked": TODAY},
    {"what": "大仙院：通年9:00〜16:30（臨時の変更あり。日ごとの時間はトップのカレンダー）、大人500円・小人300円・お抹茶500円、年中無休（公式サイト）", "url": "https://daisen-in.net/fee_information/", "checked": CHECKED},
    {"what": "泉仙 大慈院店：大徳寺の境内、11:00〜16:00（L.O.）、年中無休（12/28〜31は休み）、6名以上は予約（公式サイトの店舗案内）", "url": IZUSEN_URL, "checked": TODAY},
    {"what": "泉仙 大慈院店の値段：2026年9月1日ご提供分から あやめ4,500円・ゆり5,500円・ぼたん6,500円（すべて税込）（公式サイトのお知らせ「お値上げのおしらせ(9/1より全店)」）", "url": IZUSEN_PRICE_URL, "checked": TODAY},
    {"what": "大徳寺 総見院 秋の特別公開（主催 京都春秋）：2026年10月10日〜11月30日、10:00〜16:00（受付終了）、大人800円・中高生400円・小学生以下無料、現金のみ、休止日あり", "url": SHUNJU["sokenin"], "checked": TODAY},
    {"what": "大徳寺 黄梅院 秋の特別公開（主催 京都春秋）：2026年10月9日〜12月6日、10:00〜15:45（受付終了）、大人1000円・中高生500円・小学生以下無料、現金のみ。静止画の撮影は可（人物・自撮り棒・三脚などは不可）", "url": SHUNJU["oubaiin"], "checked": TODAY},
    {"what": "大徳寺 聚光院 開創460年 特別公開（主催 京都春秋）：2026年9月18日〜12月6日、9:30〜15:30（受付終了）、大人1000円・小中高生500円、現金のみ、未就学児は拝観不可、11月27日〜29日など休止、境内は撮影禁止", "url": SHUNJU["jukoin"], "checked": TODAY},
    {"what": "大徳寺 興臨院 秋の特別公開（主催 京都春秋）：2026年10月3日〜12月15日、10:00〜16:30（受付終了。12月1日以降は16:00）、大人800円・中高生400円・小学生300円、現金のみ、境内は庭園以外撮影禁止。大仙院以外で通年公開の塔頭（龍源院・瑞峯院など）は公式の案内を見つけられず（要確認）", "url": SHUNJU["kohrinin"], "checked": TODAY},
    {"what": "とようけ茶屋：飲食11:00〜14:30（ラストオーダー14:00）、定休日は木曜・金曜（25日と祝日は営業）、年末年始は2026年12月31日〜2027年1月3日休み、北野天満宮前・昼だけの店・湯豆腐／とようけ丼／生ゆば丼／生麩丼（とようけ屋山本の公式サイト）", "url": TOYOUKE_URL, "checked": CHECKED},
    {"what": "市バス59系統（2026年3月20日改正）：河原町三条 7:11発→龍安寺前 平日7:44・土休日7:43。冬は平日7:43発→8:21着、土休日7:34発→8:06着。龍安寺前→金閣寺道は平日8:43・土休日8:53発、15時台は13・28・43・58分発。金閣寺道→河原町三条は平日16:35→17:05・16:50→17:20、土休日16:40→17:10・17:00→17:30（京都市交通局の停留所ごとの時刻表）", "url": BUS_URL, "checked": CHECKED},
    {"what": "市バス205系統（2026年3月20日改正）：金閣寺道→大徳寺前 約6分（10時ごろは7〜9分おき）、大徳寺前12:19発→北野白梅町12:30。市バス10系統：河原町三条9:31発→北野天満宮前9:57、北野天満宮前→河原町三条は約25分（17時台10・30・50分、18時台は平日10・30・50分・土休日15・45分、河原町三条まで行く最終は21:34発）（京都市交通局の停留所ごとの時刻表）", "url": BUS_URL, "checked": CHECKED},
    {"what": "嵐電：均一運賃250円、現金か交通系ICカード、降りるときに払う（京福電気鉄道の公式サイト「ご利用方法」）。北野白梅町・御室仁和寺とも日中は毎時03・13・23・33・43・53分発、所要約5分（駅ごとの時刻表）", "url": RANDEN_URL, "checked": CHECKED},
    {"what": "市バスの普通運賃（均一運賃区間）大人230円・小児120円、交通系ICカード可（京都市交通局「定期券以外の運賃（市バス）」、ページの更新日2026年11月10日）", "url": BUS_FARE_URL, "checked": TODAY},
    {"what": "金閣寺の混む時間帯（10〜15時ごろ）は公式の資料では確認できず、文章では「言われている」と書いた。歩く時間（龍安寺〜金閣寺20〜25分、仁和寺〜龍安寺約15分、上七軒10分ほど）はめやす", "url": "https://www.city.kyoto.lg.jp/kotsu/", "checked": CHECKED},
]

TIME_HEAD = T("おすすめ訪問時間：", "Recommended visit time: ")


def build(cid, order, sections):
    spots = []
    for no, sid in enumerate(order, 1):
        s = S[sid]
        t = {l: s["body"][l] + "\n\n" + s["way"][cid][l] + "\n\n" + TIME_HEAD[l] + s["time"][cid][0 if l == "ja" else 1] for l in ("ja", "en")}
        inf = json.loads(json.dumps(s["info"]))
        links = list(s["links"])
        if cid == "late" and sid == "kitano":
            inf["rows"] = inf["rows"][:1] + LATE_KITANO_ROWS + inf["rows"][1:]
            links = links[:1] + s["late_links"] + links[1:]
        out = {"no": no, "id": sid, "name": s["name"], "kind": s["kind"], "blurb": s["blurb"], "lat": s["lat"], "lng": s["lng"], "text": t,
               "gmaps": s["gmaps"], "links": links, "info": inf, "photos": photos(sid), "notices": s["notices"]}
        if s.get("caution"):
            out["caution"] = s["caution"]
        spots.append(out)
    no_of = {s["id"]: s["no"] for s in spots}
    secs = [{"first": no_of[ids[0]], "last": no_of[ids[-1]], "day": day} for ids, day in sections]
    assert secs[0]["first"] == 1 and secs[-1]["last"] == len(spots)
    assert all(a["last"] + 1 == b["first"] for a, b in zip(secs, secs[1:]))
    return {
        "id": "kinkakuji",
        "course": cid,
        "_note": "京都・金閣寺〜北野天満宮の1日ルート（kinkakuji/ のページ専用。形は eizan-line.json と同じ）。コースは2つ：早朝コース（kinkakuji.json）と9〜10時に出発するコース（kinkakuji-late.json）。"
                 "出発は京都の中心・三条のあたり（河原町三条のバス停）を想定。"
                 "写真は Toshi の写真ライブラリから選んだもの（2024〜2026年の写真を場所ごとに全部見て、1か所10枚以内・Nikon D7000 を含む・横の写真だけ。長辺1600px・位置情報なし）。"
                 "金閣寺の雪の写真は2026年2月8日、仁和寺の御室桜は2025年4月17日、平野神社の夜桜は2025年4月5日、北野天満宮の紅葉のライトアップは2024年12月と2025年11月。"
                 "事実情報の出典と確認日は sources。このファイルは scripts/build_kinkakuji_data.py で作る（直接直さない）。",
        "sections": secs,
        "plan": {"_note": "「選んで回る」の設定。どの場所も自分で選べる。", "picks": list(range(1, len(spots) + 1)), "auto": {}, "hints": []},
        "photoBase": "../images/kinkakuji/",
        "sources": SOURCES,
        "spots": spots,
    }


for cid, fname, order, sections in COURSES:
    d = build(cid, order, sections)
    json.dump(d, open(f"{R}/data/routes/{fname}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", fname, cid, [(s["no"], s["id"], len(s["photos"])) for s in d["spots"]])
