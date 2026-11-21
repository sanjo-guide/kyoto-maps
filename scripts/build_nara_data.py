#!/usr/bin/env python3
"""奈良のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_nara_data.py  （そのあと python3 scripts/sync_nara.py）
- 作るもの（COURSES）:
  - data/routes/nara.json … 「9〜10時に出発」（興福寺→ならまちで早めのお昼→春鹿→春日大社→15時半すぎの大仏殿→夕暮れの二月堂→奈良で晩ごはん）
  - data/routes/nara-early.json … 「早朝に出発」（大仏殿の開門に合わせる→二月堂→春日大社→春日荷茶屋で朝ごはん→ならまち→春鹿→興福寺）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方の一言、「選んで回る」の設定
- 出発地は京都（三条のあたり）と大阪（梅田〜難波のあたり）の両方を、近鉄奈良駅のスポットと紹介ページに書いてある。
  近鉄奈良駅に着く時刻がほぼ同じ（早朝 7:17〜7:22、9〜10時発 10:09〜10:18）なので、時間割は1つで足りる
- 写真は scripts/nara_photos.py（表示する順）。Toshi の写真はファイル名だけ、Wikimedia Commons から借りた写真は W(...)
- 2026-11-22 オーナーの基準で作り直した（ゲストが実際に回れる1日。早朝コースと9〜10時発コース。春鹿をスポットに）。
  時刻と運賃は乗換案内（Yahoo!路線情報。2026年11月28日・土曜と11月25日・水曜のダイヤ）、拝観の時間と料金は各公式サイト
"""
import copy, json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "nara"
IMG = f"{R}/images/{MAP_ID}"
D21, D22 = "2026-11-21", "2026-11-22"   # 確認日（21日に確認して22日は見直していないものは D21）


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


def info(rows, source, tip=None, verified=True, cash=False, checked=D22):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked, "source": source}
    if not verified:
        d["verified"] = False
    return d


def W(file, author, lic, title):
    return {"file": file, "credit": {"author": author, "license": lic,
                                     "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


PHOTOS = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nara_photos.py"), encoding="utf-8").read())

YAHOO = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")

# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    eki=dict(
        name=T("近鉄奈良駅", "Kintetsu-Nara Station"), kind=T("駅（スタート）", "Station (start)"),
        blurb=T("京都からも大阪からも、近鉄で。奈良公園へは、JRより近鉄の駅のほうがずっと近いです。",
                "By Kintetsu, from Kyoto or from Osaka. For Nara Park, the Kintetsu station is much closer than JR."),
        lat=34.68414, lng=135.82854,
        body=T("近鉄奈良駅（きんてつならえき）\n\n"
               "京都の中心（三条・烏丸御池のあたり）から\n"
               "・地下鉄 烏丸御池駅から：竹田（たけだ）駅で同じホームの近鉄の急行に乗り換え。烏丸御池から近鉄奈良まで乗り換えなしの急行もあります（土曜の9:21発など）。約1時間、1,020円。\n"
               "・京都駅まで地下鉄で出て、近鉄に乗る：980円（地下鉄220円＋近鉄760円）。京都駅が始発なので座りやすく、特急（＋520円・全席指定・35〜40分）にも乗れます。\n"
               "・京阪の三条駅から：特急で丹波橋（たんばばし）へ約10分、となりの近鉄丹波橋駅で急行に乗り換え。1,000円（京阪320円＋近鉄680円）。\n"
               "・JR（ジャパン・レール・パスの人向け）：京都駅からみやこ路快速で約47分・720円。ただしJR奈良駅は近鉄奈良駅より西に約1km離れています。\n\n"
               "大阪（梅田〜難波のあたり）から\n"
               "・大阪難波（おおさかなんば）駅から近鉄奈良線の快速急行で35〜40分、680円。乗り換えなし。\n"
               "・梅田からは、地下鉄御堂筋線でなんばへ出て（約9分・240円）、近鉄に乗り換え。合わせて920円。\n\n"
               "近鉄の急行・快速急行は、行き先が「近鉄奈良」でないときは大和西大寺（やまとさいだいじ）で乗り換えます。\n\n"
               "近鉄奈良駅は地下の駅です。地上に上がると、行基（ぎょうき）さんの像が立つ噴水の広場。そこから東へ、ゆるい坂（登大路）を上ると5分で興福寺、その先が奈良公園です。\n\n"
               "ICカード（ICOCA・Suicaなど）は地下鉄・近鉄・京阪・JRのどれでも使えます。お寺の拝観料は現金だけの所が多いので、千円札と小銭を多めに。",
               "Kintetsu-Nara Station\n\n"
               "From central Kyoto (around Sanjo and Karasuma Oike)\n"
               "• From Karasuma Oike subway station: change at Takeda to a Kintetsu express on the same platform. Some expresses run straight through from Karasuma Oike to Kintetsu-Nara (the 9:21 on Saturdays, for one). About 1 hour, ¥1,020.\n"
               "• Subway to Kyoto Station, then Kintetsu: ¥980 (subway ¥220 + Kintetsu ¥760). Trains start at Kyoto so seats are easier, and you can take the limited express (+¥520, all seats reserved, 35–40 minutes).\n"
               "• From Keihan Sanjo Station: limited express to Tambabashi (about 10 minutes), then a Kintetsu express from Kintetsu-Tambabashi next door. ¥1,000 (Keihan ¥320 + Kintetsu ¥680).\n"
               "• JR (for Japan Rail Pass holders): Miyakoji Rapid from Kyoto Station, about 47 minutes, ¥720. But JR Nara Station is about 1 km west of Kintetsu-Nara.\n\n"
               "From Osaka (around Umeda and Namba)\n"
               "• From Osaka-Namba Station: Kintetsu Nara Line rapid express, 35–40 minutes, ¥680, no change.\n"
               "• From Umeda: Midosuji subway line to Namba (about 9 minutes, ¥240), then Kintetsu. ¥920 in all.\n\n"
               "If your Kintetsu express or rapid express is not bound for Kintetsu-Nara, change at Yamato-Saidaiji.\n\n"
               "Kintetsu-Nara is underground. Up at street level you are by the fountain with the statue of the monk Gyoki. Walk east up the gentle slope (Noborioji): 5 minutes to Kofukuji, with Nara Park just beyond.\n\n"
               "IC cards (ICOCA, Suica and so on) work on the subway, Kintetsu, Keihan and JR. Many temples take cash only, so bring ¥1,000 notes and coins."),
        gmaps=[gm("近鉄奈良駅", "Kintetsu-Nara Station", 34.68414, 135.82854, "近鉄奈良駅"),
               gm("地下鉄 烏丸御池駅", "Karasuma Oike subway station", 35.01092, 135.75952, "烏丸御池駅"),
               gm("近鉄 大阪難波駅", "Kintetsu Osaka-Namba Station", 34.66696, 135.49851, "大阪難波駅")],
        links=[link("official", "近鉄特急チケットレスサービス", "Kintetsu limited express ticketless service (Japanese)", "https://www.kintetsu.co.jp/gyoumu/ticket/"),
               link("official", "奈良世界遺産フリーきっぷ（近鉄）", "Nara World Heritage Free Ticket (Kintetsu, Japanese)", "https://www.kintetsu.co.jp/senden/Railway/Ticket/sekaiisan/nara_nishi.html"), YAHOO],
        _rows=[row("fee", "京都から：烏丸御池→近鉄奈良 1,020円（竹田経由）／京都駅経由 980円／京阪三条から 1,000円。近鉄特急は＋520円",
                   "From Kyoto: Karasuma Oike → Kintetsu-Nara ¥1,020 (via Takeda) / ¥980 via Kyoto Station / ¥1,000 from Keihan Sanjo. Kintetsu limited express +¥520"),
               row("fee", "大阪から：大阪難波→近鉄奈良 680円（梅田からは地下鉄240円を足して920円）",
                   "From Osaka: Osaka-Namba → Kintetsu-Nara ¥680 (¥920 from Umeda, with ¥240 for the subway)"),
               row("fee", "法隆寺や平城宮跡までバス・近鉄で回る日は「奈良世界遺産フリーきっぷ 奈良・斑鳩1日コース」（京都から1,800円。21日に確認）もあります。歩いて回るだけなら普通のきっぷで十分です",
                   "If you add Horyuji or the Heijo Palace site by bus and Kintetsu, there is the Nara World Heritage Free Ticket (Nara–Ikaruga 1-day, ¥1,800 from Kyoto; checked on the 21st). For the walking route alone, ordinary tickets are enough")],
        _tip=T("時刻と運賃は乗換案内で確認しました（2026年11月28日・土曜のダイヤ。平日は数分ちがいます）。時刻は曜日とダイヤ改正で変わるので、乗る前にもう一度確かめてください。JRの時刻と運賃は11月21日に確認。写真は近鉄奈良駅のホームで撮った京都行きの特急（2021年）と、JR奈良駅の京都行き（2022年）です。",
               "Times and fares checked on a route planner (timetable for Saturday 28 November 2026; weekdays differ by a few minutes). They change by day and with timetable revisions, so check again before you travel. JR times and fare checked on 21 November. The photos show Kyoto-bound limited expresses at Kintetsu-Nara (2021) and a Kyoto-bound train at JR Nara (2022)."),
        _source="乗換案内（Yahoo!路線情報）2026-11-22。きっぷは近鉄の公式サイト（2026-11-21）"),
    kofukuji=dict(
        name=T("興福寺", "Kofukuji Temple"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
        blurb=T("駅から5分。阿修羅像のいる国宝館は9:00から。五重塔は修理中で、覆いの中です。拝観料は現金だけ。",
                "Five minutes from the station. The National Treasure Hall with the Ashura statue opens at 9:00. The five-storied pagoda is under repair, hidden inside its cover. Cash only."),
        caution=T("五重塔は修理中（覆いで見えません）・拝観料は現金のみ", "Pagoda under repair (covered, not visible) · cash only"),
        lat=34.68325, lng=135.83117,
        body=T("興福寺（こうふくじ）\n\n藤原氏の氏寺として1300年続くお寺です。境内は塀がなく、朝から自由に歩けます。\n\n"
               "先に知っておいてほしいこと：奈良の絵はがきでおなじみの五重塔は、約120年ぶりの大修理の最中で、塔全体が工事用の建物（素屋根）にすっぽり覆われています。外から塔の姿は見えません。工事は2030年代前半まで続く予定です。夜の猿沢池（さるさわいけ）に塔が映る3枚目の写真は、工事が始まる前の2022年12月に撮ったものです。\n\n"
               "それでも寄る価値があるのは国宝館です。3つの顔と6本の腕をもつ阿修羅（あしゅら）像をはじめ、教科書で見た仏像がガラスなしで目の前に並びます。見るのに30〜40分。\n\n"
               "2018年に再建された朱色の中金堂（ちゅうこんどう）、八角形の南円堂（なんえんどう）は外から見るだけなら無料。南円堂の横の石段を下りると猿沢池で、池の南がならまちです。\n\n"
               "拝観料は現金だけ。お堂と国宝館の中にトイレはありません。",
               "Kofukuji Temple\n\nThe family temple of the Fujiwara clan, 1,300 years old. The grounds have no walls and you can walk in freely from early morning.\n\n"
               "One thing to know first: the five-storied pagoda from every Nara postcard is in the middle of its first major repair in about 120 years, and the whole tower is wrapped in a construction shelter. You cannot see it from outside. The work is planned to run into the early 2030s. The third photo, the pagoda reflected in Sarusawa Pond at night, was taken in December 2022, before the work began.\n\n"
               "What still makes the stop worthwhile is the National Treasure Hall. The three-faced, six-armed Ashura and other statues you may know from textbooks stand right in front of you, with no glass. Allow 30–40 minutes.\n\n"
               "The vermilion Central Golden Hall, rebuilt in 2018, and the octagonal Nan’endo are free to see from outside. The stone steps beside the Nan’endo lead down to Sarusawa Pond; Naramachi lies south of the pond.\n\n"
               "Admission is cash only. There are no toilets inside the halls or the museum."),
        gmaps=[gm("興福寺 国宝館", "Kofukuji National Treasure Hall", 34.68353, 135.83253, "興福寺 国宝館"),
               gm("猿沢池", "Sarusawa Pond", 34.68144, 135.83095, "猿沢池")],
        links=[link("official", "興福寺 拝観案内", "Kofukuji visitor information (Japanese)", "https://www.kohfukuji.com/info/info-guide/"),
               link("info", "五重塔の保存修理（奈良県）", "Pagoda repair work (Nara Prefecture, Japanese)", "https://www.pref.nara.jp/62140.htm")],
        info=info([row("hours", "国宝館・中金堂・東金堂 9:00〜17:00（受付は16:45まで）、休みなし。境内は自由", "National Treasure Hall, Central Golden Hall, Eastern Golden Hall 9:00–17:00 (last entry 16:45), open daily. Grounds always open"),
                   row("fee", "国宝館 900円、中金堂 500円、東金堂 500円（現金のみ）", "National Treasure Hall ¥900, Central Golden Hall ¥500, Eastern Golden Hall ¥500 (cash only)"),
                   row("fee", "11月30日まで：東金堂の後堂の特別公開中（東金堂＋後堂 1,000円、4か所共通券 2,000円・販売は16:00まで）", "Until 30 November: special opening of the rear hall of the Eastern Golden Hall (hall + rear hall ¥1,000; 4-site combined ticket ¥2,000, sold until 16:00)", until="2026-11-30")],
                  "興福寺 公式サイト（拝観案内）、奈良県（五重塔の保存修理）。2026-11-21に確認", cash=True, checked=D21,
                  tip=T("時間と料金は興福寺の公式サイト、五重塔の工事は奈良県のページで確認しました（11月21日）。12月以降の共通券の料金は確認できていません（要確認）。",
                        "Hours and fees checked on Kofukuji’s website, the pagoda work on Nara Prefecture’s page (21 November). The combined-ticket price from December could not be confirmed (please check)."))),
    shika=dict(
        name=T("奈良公園の鹿", "The deer of Nara Park"), kind=T("公園・鹿", "Park & deer"),
        blurb=T("鹿せんべいは買ったらすぐあげる。なくなったら両手を開いて見せる。人の少ない芝生であげると落ち着いて楽しめます。",
                "Buy the crackers and hand them over at once; show both open hands when they’re gone. It’s calmer on the quieter lawns."),
        caution=T("鹿は野生。せんべいは買ったらすぐあげる（じらすとかまれます）", "The deer are wild. Hand crackers over at once (tease and you get nipped)"),
        lat=34.68412, lng=135.83450,
        body=T("奈良公園（ならこうえん）の鹿\n\n県庁の向かいの芝生（登大路園地）から東大寺の南大門、春日大社の参道まで、道ばたにも芝生にも鹿がいます。1,000頭を超える鹿は国の天然記念物で、飼われているのではなく野生です。\n\n"
               "鹿せんべいは、道ばたの売り場で買えます（2019年から10枚200円。今の値段は売り場で確かめてください。小銭を用意）。あげ方のコツは奈良県の案内のとおりです。\n\n"
               "・買ったらすぐにあげる。じらすと、服やお尻をかまれます\n"
               "・なくなったら、両手を開いて「もうないよ」と見せる。これで離れていきます\n"
               "・鹿せんべい以外の食べ物はあげない（おなかを壊します）\n"
               "・かばんから出ている地図や紙袋は食べられます。しまっておく\n"
               "・小さい子は必ず大人と一緒に\n"
               "・5月中旬〜7月は子鹿の季節。母鹿が気が立っています。子鹿にはさわらない\n"
               "・秋（9〜11月ごろ）は角のある雄鹿に近づかない\n\n"
               "南大門の前は鹿も人もいちばん多く、せんべいを持った瞬間に囲まれます。落ち着いてあげたいなら、県庁の向かいの登大路園地か、春日大社へ向かう参道わきの芝生（飛火野・とびひの）が静かです。公園にごみ箱はないので、包み紙は持ち帰ります（せんべいを束ねている紙は鹿が食べられます）。\n\n"
               "奈良国立博物館は、仏像館が改修で2028年春ごろまで休館中。今は青銅器館で仏像の名品を少しだけ見られます。",
               "The deer of Nara Park\n\nFrom the lawn opposite the prefectural office (Noborioji Park) to Todaiji’s Great South Gate and the approach to Kasuga Taisha, deer are on the paths and on the grass. There are over a thousand; they are a protected natural monument and wild, not kept.\n\n"
               "Deer crackers (shika-senbei) are sold at stands along the way (¥200 for ten since 2019; check the price at the stand, and have coins ready). Nara Prefecture’s own advice on feeding:\n\n"
               "• Hand them over as soon as you buy them. Tease, and you get nipped on the clothes or the backside\n"
               "• When you run out, show both open hands. The deer understand and walk away\n"
               "• Never give any other food; it makes them ill\n"
               "• Maps and paper bags sticking out of your bag get eaten. Put them away\n"
               "• Small children only together with an adult\n"
               "• Mid-May to July is fawn season and mothers are on edge. Don’t touch fawns\n"
               "• In autumn (about September to November) keep away from stags with antlers\n\n"
               "In front of the Great South Gate both deer and people are thickest, and you are surrounded the moment you hold a cracker. For a calmer time, feed them at Noborioji Park opposite the prefectural office, or on the Tobihino lawn beside the approach to Kasuga Taisha. There are no rubbish bins in the park, so take wrappers with you (the paper band around the crackers is safe for deer).\n\n"
               "The Nara National Museum’s Buddhist Sculpture Hall is closed for renovation until about spring 2028; for now a small selection of its statues is shown in the Bronze Hall."),
        gmaps=[gm("奈良公園 登大路園地", "Noborioji Park", 34.68412, 135.83450, "奈良公園 登大路園地"),
               gm("飛火野", "Tobihino lawn", 34.68074, 135.84083, "飛火野 奈良公園")],
        links=[link("official", "奈良公園の鹿（奈良公園クイックガイド）", "The deer of Nara Park (Nara Park Quick Guide, Japanese)", "https://www.pref.nara.lg.jp/site/park/1003.html"),
               link("official", "奈良の鹿愛護会", "Nara Deer Preservation Foundation (Japanese)", "https://naradeer.com/"),
               link("official", "奈良国立博物館", "Nara National Museum", "https://www.narahaku.go.jp/", "https://www.narahaku.go.jp/english/")],
        info=info([row("hours", "公園は出入り自由", "The park is always open"),
                   row("fee", "鹿せんべい：10枚200円（2019年の改定時の値段。今の値段は要確認）", "Deer crackers: ¥200 for ten (the price set in 2019; please check the current price)")],
                  "奈良県「奈良公園クイックガイド」、奈良の鹿愛護会。2026-11-21に確認。鹿せんべいの今の値段・売り場の開く時間は未確認", cash=True, verified=False, checked=D21,
                  tip=T("鹿との接し方は奈良県の「奈良公園クイックガイド」と奈良の鹿愛護会のページで確認しました（11月21日）。鹿せんべいの今の値段、支払い方法、売り場が朝何時から開くかは、公式のページでは確認できませんでした。写真は2022年12月。",
                        "The advice on deer is from Nara Prefecture’s Nara Park Quick Guide and the Nara Deer Preservation Foundation (21 November). The current cracker price, payment methods and what time the stands open in the morning could not be confirmed on an official page. Photos: December 2022."))),
    isuien=dict(
        name=T("依水園・吉城園", "Isuien & Yoshikien gardens"), kind=T("日本庭園・寄り道", "Japanese gardens, side stop"),
        blurb=T("東大寺のすぐ手前にある、隣り合う2つの庭。依水園は火曜休みで入園は16:00まで。吉城園は無料です。",
                "Two neighbouring gardens just before Todaiji. Isuien is closed on Tuesdays, last entry 16:00. Yoshikien is free."),
        caution=T("依水園は火曜休み・入園は16:00まで", "Isuien: closed Tuesdays, last entry 16:00"),
        lat=34.68547, lng=135.83792,
        body=T("依水園（いすいえん）と吉城園（よしきえん）\n\n県庁の東の交差点から北へ入った細い道に、入口が並んでいます。南大門まで歩いて5分なのに、表の道とは人の数がちがいます。\n\n"
               "依水園は、池の向こうに東大寺の南大門の屋根と若草山を取り込んだ「借景」の庭。奈良でひとつ庭を見るならここです。入園料に寧楽（ねいらく）美術館も含まれます。火曜が休みで、9月下旬と年末〜1月中旬には庭の手入れで休む期間があります。\n\n"
               "隣の吉城園は苔の庭と茶室の庭。こちらは無料なので、時間がなければ吉城園だけ10分のぞくのもありです。\n\n"
               "どちらも紅葉は11月中旬〜12月初め。",
               "Isuien and Yoshikien\n\nTheir gates stand side by side on a narrow lane running north from the crossing east of the prefectural office. They are 5 minutes from the Great South Gate, yet far fewer people come this way.\n\n"
               "Isuien is a “borrowed scenery” garden: beyond its pond you see the roof of Todaiji’s Great South Gate and Mt. Wakakusa as part of the view. If you see one garden in Nara, make it this one. Admission includes the Neiraku Museum. Closed on Tuesdays, and for garden maintenance in late September and from late December to mid-January.\n\n"
               "Next door, Yoshikien has a moss garden and a tea-house garden. It’s free, so if time is short, just look into Yoshikien for 10 minutes.\n\n"
               "Autumn colours in both: mid-November to early December."),
        gmaps=[gm("依水園", "Isuien", 34.68547, 135.83792, "依水園 奈良"), gm("吉城園", "Yoshikien", 34.68510, 135.83721, "吉城園 奈良")],
        links=[link("official", "依水園・寧楽美術館", "Isuien Garden & Neiraku Museum", "https://isuien.or.jp/"),
               link("official", "吉城園（奈良県）", "Yoshikien (Nara Prefecture, Japanese)", "https://www.pref.nara.jp/39910.htm")],
        info=info([row("hours", "依水園 9:30〜16:30（入園は16:00まで）", "Isuien 9:30–16:30 (last entry 16:00)"),
                   row("closed", "依水園：火曜（祝日なら開園して次の平日が休み）、9月下旬と12月末〜1月中旬の庭園整備期間", "Isuien: Tuesdays (open if a holiday, closed the next weekday); maintenance periods in late September and from late December to mid-January"),
                   row("fee", "依水園 1,200円（寧楽美術館を含む）", "Isuien ¥1,200 (includes the Neiraku Museum)"),
                   row("hours", "吉城園 9:00〜17:00（入園は16:30まで）、無料。2月24日〜28日は休み", "Yoshikien 9:00–17:00 (last entry 16:30), free. Closed 24–28 February")],
                  "依水園 公式サイト、奈良県（吉城園）。2026-11-21に確認", checked=D21,
                  tip=T("依水園は公式サイト、吉城園は奈良県のページで確認しました（11月21日）。", "Isuien checked on its website; Yoshikien on Nara Prefecture’s page (21 November)."))),
    todaiji=dict(
        name=T("東大寺 南大門・大仏殿", "Todaiji: Great South Gate & Great Buddha Hall"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
        blurb=T("大仏殿は11〜3月が8:00、4〜10月が7:30に開きます。団体が多いのは昼。開門すぐか、閉まる1時間前に。拝観料は現金だけ。",
                "The Great Buddha Hall opens at 8:00 from November to March, 7:30 from April to October. Tour groups come in the middle of the day; go at opening, or in the last hour. Cash only."),
        caution=T("拝観料は現金のみ・11〜3月は17:00、4〜10月は17:30に閉まります", "Cash only · closes 17:00 (Nov–Mar), 17:30 (Apr–Oct)"),
        lat=34.68899, lng=135.83987,
        body=T("東大寺（とうだいじ）南大門・大仏殿\n\nまず南大門（なんだいもん）。門の左右に、見上げる大きさの木の仁王像が向かい合って立っています。みんな鹿を見ていて素通りするので、門の中で立ち止まって見上げてください。\n\n"
               "その先の大仏殿（だいぶつでん）は、世界最大級の木造建築です。入口は正面ではなく、左（西）側の回廊の端にあります。中に入ると、正面に大仏さま（盧舎那仏・るしゃなぶつ）。右回りに裏へ回ると、昔の東大寺の模型と、大仏さまの鼻の穴と同じ大きさの穴があいた柱があります（くぐれるのは子どもか細い人）。\n\n"
               "大仏殿の中は写真を撮れます（三脚は不可）。拝観料は現金だけです。",
               "Todaiji: Great South Gate and Great Buddha Hall\n\nFirst the Great South Gate (Nandaimon). Inside it, left and right, two towering wooden guardian kings face each other. Most people walk through watching the deer, so stop inside the gate and look up.\n\n"
               "Beyond it, the Great Buddha Hall (Daibutsuden) is one of the largest wooden buildings in the world. The entrance is not in the middle but at the left (west) end of the cloister. Inside, the Great Buddha (Vairocana) sits straight ahead. Walk round clockwise to the back for models of the original temple and the pillar with a hole the size of the Buddha’s nostril (only children and slim adults fit through).\n\n"
               "Photos are allowed inside the hall (no tripods). Admission is cash only."),
        gmaps=[gm("東大寺 南大門", "Great South Gate", 34.68580, 135.83987, "東大寺 南大門"), gm("東大寺 大仏殿", "Great Buddha Hall", 34.68899, 135.83987, "東大寺 大仏殿")],
        links=[link("official", "東大寺 拝観時間・拝観料", "Todaiji hours and admission", "https://www.todaiji.or.jp/information/haikan/", "https://www.todaiji.or.jp/en/")],
        info=info([row("hours", "大仏殿：4〜10月 7:30〜17:30、11〜3月 8:00〜17:00", "Great Buddha Hall: April–October 7:30–17:30, November–March 8:00–17:00"),
                   row("fee", "大仏殿 800円（小学生400円）。東大寺ミュージアム（9:30〜）とのセット券 1,200円。現金のみ", "Great Buddha Hall ¥800 (primary school children ¥400). Combined ticket with the Todaiji Museum (from 9:30) ¥1,200. Cash only"),
                   row("closed", "休みなし", "Open daily")],
                  "東大寺 公式サイト（拝観時間・拝観料）。2026-11-22に確認", cash=True,
                  tip=T("時間と料金は東大寺の公式サイトで確認しました。混み具合は日によります。写真の1・2枚目は2022年12月。",
                        "Hours and fees checked on Todaiji’s website. How busy it is varies from day to day. The first two photos: December 2022."))),
    nigatsudo=dict(
        name=T("二月堂", "Nigatsudo Hall"), kind=T("お堂・展望（無料）", "Hall & viewpoint (free)"),
        blurb=T("大仏殿の裏の坂を上って10分。舞台から奈良の町と大仏殿の屋根を見下ろせます。24時間お参りできて、西向きなので夕方がきれいです。",
                "Ten minutes up the slope behind the Great Buddha Hall. From its balcony you look down on Nara and the roof of the Great Buddha Hall. Open 24 hours; it faces west, so evening is the time."),
        lat=34.68927, lng=135.84427,
        body=T("二月堂（にがつどう）\n\n大仏殿で帰ってしまう人が多いのですが、奈良でいちばんの景色はこの先です。大仏殿を出たら右（東）へ。鐘楼の丘を越えるか、大仏殿の裏から土塀の続く石畳の坂（裏参道）を上ると、約10分で崖に張り出したお堂が見えてきます。\n\n"
               "石段を上った舞台からは、大仏殿の大屋根、奈良の町、その向こうに生駒山（いこまやま）。西向きなので、夕方は空と町が赤く染まります。24時間お参りできます。日が暮れると吊り灯籠に火が入り、昼とは別の場所になります。\n\n"
               "お堂のまわりでは三脚を使えません。堂内の撮影もできません。お百度（おひゃくど）を回っている人にカメラを向けないでください。夜は静かに。\n\n"
               "舞台の北側に休憩所があります（開いている時間は確認できていません）。隣の三月堂（法華堂）は中の仏像を見るなら800円。3月1日〜14日の夜は「お水取り」の松明（たいまつ）で大変混みます。",
               "Nigatsudo Hall\n\nMany people turn back at the Great Buddha Hall, but the best view in Nara is further on. Leaving the hall, go right (east). Either cross the bell-tower hill or take the stone-paved lane with earthen walls behind the hall; in about 10 minutes the hall appears, built out over the hillside.\n\n"
               "Climb the stone steps to the balcony: the great roof of the Buddha hall, the town of Nara, and Mt. Ikoma beyond. It faces west, so towards evening the sky and the town turn red. You can visit 24 hours a day. After dark the hanging lanterns are lit and it becomes a different place.\n\n"
               "No tripods around the hall, and no photos inside it. Don’t point a camera at worshippers walking their rounds of prayer. Keep quiet at night.\n\n"
               "There is a rest house on the north side of the balcony (opening hours not confirmed). Next door, the Sangatsudo (Hokkedo) costs ¥800 to see the statues inside. On the evenings of 1–14 March the Omizutori fire ceremony draws big crowds."),
        gmaps=[gm("二月堂", "Nigatsudo", 34.68927, 135.84427, "東大寺 二月堂")],
        links=[link("official", "東大寺 二月堂", "Todaiji: Nigatsudo (Japanese)", "https://www.todaiji.or.jp/information/nigatsudo/")],
        info=info([row("hours", "二月堂は24時間お参りできます（夜は静かに。三脚は使えません）", "Nigatsudo can be visited 24 hours a day (quietly at night; no tripods)"),
                   row("fee", "三月堂（法華堂）は8:30〜16:00・800円（現金のみ）", "Sangatsudo (Hokkedo): 8:30–16:00, ¥800 (cash only)")],
                  "東大寺 公式サイト（二月堂、拝観時間・拝観料）。2026-11-22に確認。休憩所の時間は未確認",
                  tip=T("東大寺の公式サイトで確認しました。休憩所の開いている時間は確認できていません（要確認）。日の入りは11月下旬〜12月が17時前、6月は19時すぎです。",
                        "Checked on Todaiji’s website. The opening hours of the rest house could not be confirmed (please check). Sunset is before 17:00 from late November through December, after 19:00 in June."))),
    wakakusa=dict(
        name=T("若草山", "Mt. Wakakusa"), kind=T("芝生の山・展望・寄り道", "Grassy hill & view, side stop"),
        blurb=T("二月堂と春日大社のあいだ。芝生の斜面を20分上ると、奈良の町が全部見えます。9:00〜17:00、冬は入れません。",
                "Between Nigatsudo and Kasuga Taisha. Twenty minutes up the grass slope and all of Nara is below you. 9:00–17:00; closed in winter."),
        caution=T("冬は入山できません（12月第2日曜の翌日〜3月第3土曜の前日）", "Closed in winter (from the day after the 2nd Sunday of December to the day before the 3rd Saturday of March)"),
        lat=34.68930, lng=135.84920,
        body=T("若草山（わかくさやま）\n\n全体が芝生の、標高342mの山です。二月堂と春日大社のあいだ、みやげ物屋の並ぶ道ぞいにゲートがあります。入山料を払って芝生の斜面を上ります。\n\n"
               "最初の高まり（一重目）まで約20分。ここで奈良の町と大仏殿の屋根が見渡せるので、時間がなければここで引き返して十分です。山頂（三重目）までは片道40分ほど。上にも鹿がいます。\n\n"
               "日かげがなく、夏は暑いです。飲み物を持って。ゲートは北と南の2つがあり、約300m離れています。北ゲートは二月堂（手向山八幡宮・たむけやまはちまんぐう）側、南ゲートは春日大社側です。\n\n"
               "入れるのは3月の第3土曜から12月の第2日曜まで（2026年は12月13日まで）。毎年1月の第4土曜には、山全体を焼く「若草山焼き」があります。",
               "Mt. Wakakusa\n\nA 342 m hill covered entirely in grass. Its gates are on the lane of souvenir shops between Nigatsudo and Kasuga Taisha. Pay the small fee and climb the grass slope.\n\n"
               "It takes about 20 minutes to the first shoulder. From there you already look over the town and the roof of the Great Buddha Hall, so turning back here is fine if time is short. The summit is about 40 minutes each way. There are deer up here too.\n\n"
               "There is no shade and it’s hot in summer; carry a drink. There are two gates about 300 m apart: the North Gate on the Nigatsudo (Tamukeyama Hachimangu) side, the South Gate on the Kasuga Taisha side.\n\n"
               "The hill is open from the third Saturday of March to the second Sunday of December (until 13 December in 2026). On the fourth Saturday of January the whole hillside is burned in the Wakakusa Yamayaki."),
        gmaps=[gm("若草山 北ゲート", "Mt. Wakakusa North Gate", 34.68930, 135.84920, "若草山 北ゲート")],
        links=[link("official", "若草山（奈良公園クイックガイド）", "Mt. Wakakusa (Nara Park Quick Guide, Japanese)", "https://www.pref.nara.lg.jp/site/park/2585.html")],
        notices=[notice("冬は入山できません", "Closed for winter",
                        "若草山は3月の第3土曜（2027年は3月20日）まで入れません。ふもとから見上げるだけになります。",
                        "Mt. Wakakusa is closed until the third Saturday of March (20 March 2027). You can only look up at it from the foot.",
                        frm="2026-12-14", to="2027-03-19")],
        info=info([row("hours", "3月第3土曜〜12月第2日曜の9:00〜17:00（2026年は12月13日まで）", "Third Saturday of March to second Sunday of December, 9:00–17:00 (until 13 December in 2026)"),
                   row("fee", "150円（3歳〜小学生80円）", "¥150 (¥80 for ages 3 to primary school)")],
                  "奈良県「奈良公園クイックガイド」。2026-11-21に確認", cash=True, checked=D21,
                  tip=T("奈良県の「奈良公園クイックガイド」で確認しました（11月21日）。上る時間は目安です。", "Checked on Nara Prefecture’s Nara Park Quick Guide (21 November). Climbing times are rough guides."))),
    kasuga=dict(
        name=T("春日大社", "Kasuga Taisha Shrine"), kind=T("神社（世界遺産）", "Shrine (World Heritage)"),
        blurb=T("森の中の朱色の社殿と、約3,000基の灯籠。奥の特別参拝（700円）は9:00〜16:00。毎月1・11・21日の午前など、入れない時間があります。",
                "Vermilion halls in the forest and some 3,000 lanterns. The paid inner area (¥700) is open 9:00–16:00, but not on the mornings of the 1st, 11th and 21st and some other times."),
        caution=T("特別参拝は毎月1・11・21日の午前は不可。12月20日〜1月7日は終日不可", "Inner area closed on the mornings of the 1st, 11th and 21st, and all day 20 Dec – 7 Jan"),
        lat=34.68149, lng=135.84800,
        body=T("春日大社（かすがたいしゃ）\n\n森の中に朱色の回廊が続く神社です。お参りだけなら無料で、幣殿（へいでん）の前まで入れます。その奥の「御本殿特別参拝」（700円）に入ると、朱色の回廊にずらりと下がる釣灯籠と、暗い部屋で灯籠に火を入れた様子を再現した「藤浪之屋（ふじなみのや）」が見られます。灯籠を見に来たなら、ここは入る価値があります。\n\n"
               "特別参拝に入れない日と時間があります（公式サイトより）：毎月1日・11日・21日の午前、祝日や祭りの日の午前（11月23日、12月17日など）、12月16日の午後、12月20日〜1月7日と成人の日は終日。行く日が決まったら公式サイトで確かめてください。\n\n"
               "二之鳥居から西へ下る参道は、苔のついた石灯籠のあいだに鹿が立っていて、写真を撮るならこの道です。参道の途中、萬葉植物園の正門の横にある「春日荷茶屋（かすがにないぢゃや）」は春日大社の茶屋で、季節の野菜が入る万葉粥（まんようがゆ）が名物。10:30から開きます。",
               "Kasuga Taisha Shrine\n\nA shrine of vermilion cloisters in the forest. Praying is free and takes you as far as the offering hall. Beyond it, the paid inner area (¥700) has the cloisters hung with rows of bronze lanterns and the Fujinami-no-ya, a dark room where lit lanterns recreate the lantern festival. If the lanterns are what you came for, it’s worth paying.\n\n"
               "There are days and times when the inner area is closed (from the official website): the mornings of the 1st, 11th and 21st of every month, the mornings of some holidays and festival days (such as 23 November and 17 December), the afternoon of 16 December, and all day from 20 December to 7 January and on Coming-of-Age Day. Once you know your date, check the website.\n\n"
               "The approach running west from the second torii is the path for photos: deer stand between the mossy stone lanterns. Partway down, beside the main gate of the Man’yo Botanical Garden, Kasuga Ninaijaya is the shrine’s own teahouse, known for Man’yo-gayu, rice porridge with seasonal vegetables. It opens at 10:30."),
        gmaps=[gm("春日大社", "Kasuga Taisha", 34.68149, 135.84800, "春日大社 本殿"), gm("春日荷茶屋", "Kasuga Ninaijaya teahouse", 34.68231, 135.84338, "春日荷茶屋")],
        links=[link("official", "春日大社 参拝案内", "Kasuga Taisha visitor information", "https://www.kasugataisha.or.jp/about/basic/", "https://www.kasugataisha.or.jp/en/"),
               link("official", "春日荷茶屋", "Kasuga Ninaijaya teahouse (Japanese)", "https://www.kasugataisha.or.jp/ninaijyaya/")],
        notices=[notice("12月20日〜1月7日は特別参拝に入れません", "Inner area closed 20 December – 7 January",
                        "12月20日〜1月7日は御本殿特別参拝が終日休みです。お参り（無料）はできます。",
                        "From 20 December to 7 January the paid inner area is closed all day. You can still pray at the shrine (free).",
                        url="https://www.kasugataisha.or.jp/about/basic/", frm="2026-12-13", to="2027-01-07")],
        info=info([row("hours", "お参り：3〜10月 6:30〜17:30、11〜2月 7:00〜17:00", "Shrine: March–October 6:30–17:30, November–February 7:00–17:00"),
                   row("hours", "御本殿特別参拝 9:00〜16:00（毎月1・11・21日の午前など、入れない日・時間があります）", "Inner area (special visit) 9:00–16:00 (closed on the mornings of the 1st, 11th and 21st and at some other times)"),
                   row("fee", "お参りは無料。御本殿特別参拝 700円、国宝殿（10:00〜17:00）700円", "Praying is free. Inner area ¥700; Kasuga Taisha Museum (10:00–17:00) ¥700"),
                   row("hours", "春日荷茶屋 10:30〜16:30（ラストオーダー16:00）。休みは不定で、月ごとに公式サイトに出ます（2026年11月は10日・17日）。万葉粥 1,200円（11月21日に確認）",
                       "Kasuga Ninaijaya 10:30–16:30 (last orders 16:00). Irregular closing days, listed monthly on the website (10 and 17 November 2026). Man’yo-gayu ¥1,200 (checked 21 November)")],
                  "春日大社 公式サイト（参拝案内、春日荷茶屋）。2026-11-22に確認。万葉粥の値段は2026-11-21。荷茶屋の支払い方法は未確認",
                  tip=T("春日大社の公式サイトで確認しました。荷茶屋の支払い方法は確認できていません（要確認）。4枚目の鳥居の写真は2022年12月。", "Checked on Kasuga Taisha’s website. Payment methods at the teahouse could not be confirmed (please check). The fourth photo (the torii): December 2022."))),
    naramachi=dict(
        name=T("ならまち", "Naramachi"), kind=T("古い町並み・食事", "Old town & food"),
        blurb=T("格子の町家が残る、元興寺のまわりの古い町。お昼も、夜の一杯もここで。火曜・水曜は休む店が多めです。",
                "The old quarter around Gangoji, with its latticed townhouses. Lunch and an evening drink are both here. Many places close on Tuesdays and Wednesdays."),
        lat=34.67763, lng=135.83121,
        body=T("ならまち\n\n猿沢池の南に広がる、江戸〜明治の町家が残る一帯です。もとは全部、元興寺（がんごうじ）というお寺の境内でした。道は細く、車も少なく、公園側とは空気が違います。\n\n"
               "見る所：\n・元興寺：世界遺産。屋根の一部に、1400年前の飛鳥時代の瓦が今も使われています。\n・ならまち格子の家：昔の町家を再現した建物で、中まで無料で入れます。奥に細長い造りがよくわかります（月曜休み）。\n・鹿の舟（しかのふね）：格子の家のすぐ南。観光案内所の「繭（まゆ）」は9:00〜17:00・無休で、地図をもらって休めます。\n\n"
               "軒先に下がっている赤い布のぬいぐるみは「身代わり申（さる）」。庚申（こうしん）さんの魔よけです。\n\n"
               "食べる・飲む（どれも公式サイトで時間を確かめた店です）：\n"
               "・鹿の舟「竈（かまど）」：食堂。11:00〜16:00、水曜休み。\n"
               "・粟（あわ）ならまち店：大和野菜の料理。完全予約制です。昼は11:30〜14:30（入店は13:00まで）、夜は17:30〜21:00（入店は19:00まで）、火曜休み。昼3,800円から、夜4,800円から。カードも使えます。\n"
               "・なら泉勇斎（ならいずみゆうさい）：奈良の地酒の店。カウンターで有料の試飲ができます。11:00〜20:00、木曜休み。夕方、駅へ戻る前の一杯に。\n"
               "・中谷堂（なかたにどう）：三条通の角。つきたてのよもぎ餅。10:00〜19:00。\n\n"
               "予約なしで入るなら、町家のカフェや食事の店は元興寺の北と西の通りに集まっています。ランチが14時ごろで終わる店に注意。駅前のアーケード（東向商店街・もちいどのセンター街）は、昼から夜まで開いている店が多いです。\n\n"
               "近鉄奈良駅へは、もちいどのセンター街のアーケードを北へ抜けて歩いて約15分。",
               "Naramachi\n\nThe quarter south of Sarusawa Pond, where townhouses from the Edo and Meiji periods survive. All of it was once the precinct of one temple, Gangoji. The lanes are narrow, there are few cars, and the mood is quite different from the park side.\n\n"
               "What to see:\n• Gangoji: a World Heritage temple. Part of its roof still carries tiles from the Asuka period, 1,400 years old.\n• Naramachi Koshi-no-Ie: a reconstructed townhouse you can walk right through, free. You see how long and narrow these houses are (closed Mondays).\n• Shika-no-Fune: just south of Koshi-no-Ie. Its tourist information centre “Mayu” is open 9:00–17:00 every day; pick up a map and sit down.\n\n"
               "The red cloth charms hanging under the eaves are “migawari-zaru”, monkey charms of the Koshin faith that take bad luck in your place.\n\n"
               "Eating and drinking (hours of all of these were checked on their own websites):\n"
               "• Shika-no-Fune “Kamado”: a canteen. 11:00–16:00, closed Wednesdays.\n"
               "• Awa Naramachi: dishes built on traditional Yamato vegetables. Reservation only. Lunch 11:30–14:30 (last seating 13:00), dinner 17:30–21:00 (last seating 19:00), closed Tuesdays. Lunch from ¥3,800, dinner from ¥4,800. Cards accepted.\n"
               "• Nara Izumi Yusai: a shop for Nara’s local sake, with paid tastings at the counter. 11:00–20:00, closed Thursdays. Good for a glass before you walk back to the station.\n"
               "• Nakatanidou: on the corner of Sanjo-dori. Freshly pounded mugwort rice cakes. 10:00–19:00.\n\n"
               "Without a booking, cafés and restaurants in old townhouses are clustered on the streets north and west of Gangoji. Watch out for places whose lunch ends around 14:00. The covered arcades by the station (Higashimuki and Mochiidono) have many places open from lunch into the evening.\n\n"
               "To Kintetsu-Nara Station, walk north through the Mochiidono arcade: about 15 minutes."),
        gmaps=[gm("元興寺", "Gangoji", 34.67763, 135.83121, "元興寺 奈良"), gm("ならまち格子の家", "Naramachi Koshi-no-Ie", 34.67502, 135.83067, "ならまち格子の家"),
               gm("鹿の舟", "Shika-no-Fune", 34.67408, 135.83068, "鹿の舟 奈良"), gm("なら泉勇斎", "Nara Izumi Yusai", 34.67974, 135.82934, "なら泉勇斎"),
               gm("中谷堂", "Nakatanidou", 34.68193, 135.82886, "中谷堂 奈良")],
        links=[link("official", "元興寺", "Gangoji (Japanese)", "https://gangoji-tera.or.jp/about/"),
               link("official", "ならまち格子の家（奈良市）", "Naramachi Koshi-no-Ie (Nara City, Japanese)", "https://www.city.nara.lg.jp/site/shisetsu/6242.html"),
               link("official", "鹿の舟", "Shika-no-Fune (Japanese)", "https://www.kuruminoki.co.jp/shikanofune/access/"),
               link("official", "粟 ならまち店（予約）", "Awa Naramachi (reservations, Japanese)", "https://www.kiyosumi.jp/naramachiten"),
               link("official", "なら泉勇斎", "Nara Izumi Yusai (Japanese)", "https://naraizumi.jp/"),
               link("official", "中谷堂", "Nakatanidou (Japanese)", "https://nakatanidou.jp/shop")],
        info=info([row("hours", "元興寺 9:00〜17:00（入門は16:30まで）、700円", "Gangoji 9:00–17:00 (last entry 16:30), ¥700"),
                   row("hours", "ならまち格子の家 9:00〜17:00、無料。月曜休み（祝日なら翌日）、祝日の翌日、12月26日〜1月5日も休み", "Naramachi Koshi-no-Ie 9:00–17:00, free. Closed Mondays (next day if a holiday), the day after a holiday, and 26 December – 5 January"),
                   row("hours", "鹿の舟：繭（観光案内所）9:00〜17:00・無休／竈（食堂）11:00〜16:00・水曜休み／囀（喫茶）11:30〜17:00・火水休み", "Shika-no-Fune: Mayu (tourist information) 9:00–17:00 daily / Kamado (canteen) 11:00–16:00, closed Wed / Saezuri (tea room) 11:30–17:00, closed Tue & Wed"),
                   row("hours", "粟 ならまち店：完全予約制。昼 11:30〜14:30（入店13:00まで）、夜 17:30〜21:00（入店19:00まで）、火曜休み", "Awa Naramachi: reservation only. Lunch 11:30–14:30 (last seating 13:00), dinner 17:30–21:00 (last seating 19:00), closed Tuesdays"),
                   row("hours", "なら泉勇斎 11:00〜20:00、木曜休み。試飲は有料（料金は要確認）", "Nara Izumi Yusai 11:00–20:00, closed Thursdays. Paid tastings (prices: please check)"),
                   row("hours", "中谷堂 10:00〜19:00（売り切れで早じまいあり）。よもぎ餅3個600円（11月21日に確認）", "Nakatanidou 10:00–19:00 (may close early when sold out). Mugwort rice cakes ¥600 for three (checked 21 November)")],
                  "鹿の舟・粟 ならまち店・なら泉勇斎の公式サイト（2026-11-22）、元興寺・奈良市（格子の家）・中谷堂の公式サイト（2026-11-21）",
                  tip=T("それぞれの公式サイト（格子の家は奈良市）で確認しました。鹿の舟・粟・なら泉勇斎は11月22日、元興寺・格子の家・中谷堂は11月21日。鹿の舟は月ごとの休みのお知らせが公式サイトに出ます。中谷堂の休みは決まっていません（お店のSNSで告知）。",
                        "Checked on each official website (Koshi-no-Ie on Nara City’s page): Shika-no-Fune, Awa and Nara Izumi Yusai on 22 November; Gangoji, Koshi-no-Ie and Nakatanidou on 21 November. Shika-no-Fune posts its monthly closing days on its website. Nakatanidou has no fixed closing day (announced on its social media)."))),
    harushika=dict(
        name=T("春鹿（今西清兵衛商店）", "Harushika sake brewery (Imanishi Seibei Shoten)"), kind=T("酒蔵・きき酒", "Sake brewery & tasting"),
        blurb=T("ならまちの東の端にある、日本酒「春鹿」の蔵元。700円で5種類のきき酒。受付は10:00〜16:30、火曜休み。",
                "The brewery of Harushika sake, at the eastern edge of Naramachi. A tasting of five kinds for ¥700. Reception 10:00–16:30, closed Tuesdays."),
        caution=T("火曜休み・きき酒の受付は16:30まで・20歳から。運転する人は不可", "Closed Tuesdays · tasting reception until 16:30 · age 20 and over, not for drivers"),
        lat=34.67720, lng=135.83440,
        body=T("春鹿（はるしか）今西清兵衛商店（いまにしせいべえしょうてん）\n\n日本酒「春鹿」の蔵元です。元興寺から東へ歩いて約5分。杉玉（すぎたま）の下がる、格子の古い建物が入口です。\n\n"
               "きき酒は1人700円で、5種類を1杯ずつ。受付は10:00から16:30まで。お酒とグラスは季節で変わります（公式サイトより）。公式サイトで予約を受けているのは4〜8人の組だけです（10:00と11:00の回）。1〜3人は店で直接受付を。\n\n"
               "お酒は20歳から。車や自転車を運転する人は、きき酒はできません。\n\n"
               "支払い方法は公式サイトに書かれていません（要確認）。現金を用意しておくと安心です。\n\n"
               "蔵の中の見学は、毎年2月ごろの期間限定です。\n\n"
               "写真は2022年12月。そのときの店内の案内では、きき酒のあとにグラスを持ち帰れました（今も同じかは要確認）。",
               "Harushika (Imanishi Seibei Shoten)\n\nThe brewery of Harushika sake, about 5 minutes’ walk east of Gangoji. Look for the old latticed building with a cedar ball hanging over the door.\n\n"
               "The tasting is ¥700 per person for one cup each of five kinds. Reception runs from 10:00 to 16:30. The sakes and the glass change with the season (from the official website). The website takes bookings only for groups of 4–8 (at 10:00 and 11:00). If you are 1–3 people, ask at the shop.\n\n"
               "You must be 20 or over. If you are driving or cycling, you can’t do the tasting.\n\n"
               "The website does not say how you can pay (unconfirmed). Have cash ready to be safe.\n\n"
               "Tours of the brewery itself run only for a limited period around February each year.\n\n"
               "The photos are from December 2022. The notice in the shop then said you could take your tasting glass home (please check whether that still applies)."),
        gmaps=[gm("今西清兵衛商店（春鹿）", "Imanishi Seibei Shoten (Harushika)", 34.67720, 135.83440, "今西清兵衛商店 春鹿")],
        links=[link("official", "春鹿 蔵元見学・きき酒", "Harushika brewery tasting (Japanese)", "https://www.harushika.com/visit-brewery/")],
        info=info([row("hours", "店 9:00〜17:00。きき酒の受付 10:00〜16:30", "Shop 9:00–17:00. Tasting reception 10:00–16:30"),
                   row("closed", "火曜（祝日なら翌日）、お盆、年末年始など", "Tuesdays (next day if a holiday), mid-August, New Year and some other days"),
                   row("fee", "きき酒 700円（5種類）。支払い方法は要確認", "Tasting ¥700 (five kinds). Payment methods: please check"),
                   row("bus", "歩きたくないとき：近鉄奈良駅・JR奈良駅から天理行きのバスで約10分「福智院町」下車、歩いて3分（運賃は要確認）", "If you’d rather not walk: bus bound for Tenri from Kintetsu-Nara or JR Nara, about 10 min to Fukuchiin-cho, then 3 min on foot (fare: please check)")],
                  "春鹿（今西清兵衛商店）公式サイト「蔵元見学・きき酒」。2026-11-22に確認。支払い方法とグラスの持ち帰りは記載なし（要確認）",
                  tip=T("春鹿の公式サイトで確認しました。年末年始の休みの日付は公式サイトに出ていません（要確認）。支払い方法も書かれていません。",
                        "Checked on Harushika’s website. The exact New Year closing dates are not given there (please check), and neither are payment methods."))),
    heijo=dict(
        name=T("平城宮跡", "Heijo Palace Site"), kind=T("都の跡（世界遺産）・寄り道", "Palace site (World Heritage), side trip"),
        blurb=T("1300年前の都の中心。広い野原に朱雀門と大極殿が復元されています。帰りの電車で途中下車して寄れます。無料。建物は入場16:00まで、月曜休み。",
                "The heart of the capital 1,300 years ago. On a wide open field, the Suzaku Gate and the Great Audience Hall have been rebuilt. Stop off on the train home. Free. Buildings: last entry 16:00, closed Mondays."),
        caution=T("大極殿・朱雀門は入場16:00まで・月曜休み", "Daigokuden and Suzaku Gate: last entry 16:00, closed Mondays"),
        lat=34.69393, lng=135.79424,
        body=T("平城宮跡（へいじょうきゅうせき）\n\n奈良時代の都・平城京の宮殿があった場所です。建物はほとんど残っていませんが、1km四方の野原に、正門の朱雀門（すざくもん）と、天皇の儀式の場だった第一次大極殿（だいごくでん）が実物大で復元されています。敷地の中を近鉄電車が横切って走ります。\n\n"
               "行き方：京都へも大阪へも、帰り道の途中です。近鉄奈良から2駅目の大和西大寺駅で降り、南口から歩いて約20分で大極殿。見たあと朱雀門まで南へ歩いて約15分、そこから大和西大寺駅へ戻るか、バスで近鉄奈良駅・JR奈良駅へ。京都行きの特急・急行も、大阪難波方面の快速急行も、大和西大寺に止まります。\n\n"
               "大極殿と朱雀門は16:30で閉まります（入場は16:00まで）。建物の中に入らず、夕方の野原を歩くだけなら何時でも大丈夫です。",
               "Heijo Palace Site\n\nThis is where the palace of Heijo-kyo, the Nara-period capital, stood. Almost nothing original remains above ground, but on a field a kilometre square the main Suzaku Gate and the Former Great Audience Hall (Daigokuden), where the emperor held state ceremonies, have been rebuilt at full size. Kintetsu trains run right across the site.\n\n"
               "Getting there: it’s on your way home, to Kyoto or to Osaka. Get off at Yamato-Saidaiji, two stops from Kintetsu-Nara, and walk about 20 minutes from the south exit to the Daigokuden. Then walk about 15 minutes south to the Suzaku Gate, and either return to Yamato-Saidaiji or take a bus to Kintetsu-Nara or JR Nara. Kyoto-bound limited expresses and expresses and Osaka-Namba-bound rapid expresses all stop at Yamato-Saidaiji.\n\n"
               "The Daigokuden and the Suzaku Gate close at 16:30 (last entry 16:00). Just walking the open field in the evening light, without going inside, works at any hour."),
        gmaps=[gm("第一次大極殿", "Former Great Audience Hall", 34.69393, 135.79424, "平城宮跡 第一次大極殿"), gm("朱雀門", "Suzaku Gate", 34.68693, 135.79428, "平城宮跡 朱雀門"),
               gm("大和西大寺駅", "Yamato-Saidaiji Station", 34.69380, 135.78268, "大和西大寺駅")],
        links=[link("official", "平城宮跡歴史公園 施設情報", "Heijo Palace Site Historical Park: facilities (Japanese)", "https://www.heijo-park.jp/information/facility/"),
               link("official", "平城宮跡歴史公園 アクセス", "Heijo Palace Site Historical Park: access (Japanese)", "https://www.heijo-park.jp/information/access/")],
        info=info([row("hours", "第一次大極殿・朱雀門 9:00〜16:30（入場は16:00まで）。平城宮いざない館 9:00〜17:00（入館は16:30まで）", "Daigokuden and Suzaku Gate 9:00–16:30 (last entry 16:00). Heijo Palace Izanai-kan 9:00–17:00 (last entry 16:30)"),
                   row("closed", "大極殿・朱雀門：月曜（祝日なら次の平日）、12月29日〜1月3日。いざない館：2・4・7・11月の第2月曜、12月29日〜1月1日", "Daigokuden and Suzaku Gate: Mondays (next weekday if a holiday), 29 Dec – 3 Jan. Izanai-kan: 2nd Monday of Feb, Apr, Jul and Nov; 29 Dec – 1 Jan"),
                   row("fee", "無料", "Free"),
                   row("train", "近鉄奈良 → 大和西大寺 約5分。南口から大極殿・朱雀門ひろばへ歩いて約20分", "Kintetsu-Nara → Yamato-Saidaiji about 5 min. About 20 min on foot from the south exit to the Daigokuden or Suzaku Gate Square"),
                   row("bus", "朱雀門ひろば前 → 近鉄奈良駅 約16分、JR奈良駅西口 約10分（奈良交通バス。運賃は要確認）", "Suzakumon Hiroba-mae → Kintetsu-Nara Station about 16 min, JR Nara Station west exit about 10 min (Nara Kotsu bus; fare: please check)")],
                  "平城宮跡歴史公園 公式サイト（2026-11-21）、乗換案内", checked=D21,
                  tip=T("平城宮跡歴史公園の公式サイトと乗換案内で確認しました（11月21日）。", "Checked on the Heijo Palace Site Historical Park website and a route planner (21 November)."))),
    horyuji=dict(
        name=T("法隆寺", "Horyuji Temple"), kind=T("寺（世界遺産）・別に半日", "Temple (World Heritage), needs half a day"),
        blurb=T("世界でいちばん古い木造建築。奈良公園から電車と徒歩で約50分かかるので、同じ日に入れるなら何かを外します。拝観料は現金だけ。",
                "The oldest wooden buildings in the world. It’s about 50 minutes from Nara Park by train and on foot, so fitting it into the same day means dropping something. Cash only."),
        caution=T("奈良公園と同じ日に全部は回れません・現金のみ", "Doesn’t fit with the whole Nara Park route in one day · cash only"),
        lat=34.61470, lng=135.73420,
        body=T("法隆寺（ほうりゅうじ）\n\n聖徳太子が建てたお寺で、金堂と五重塔は7世紀のもの。世界でいちばん古い木造建築です。興福寺の五重塔が見られない今、五重塔を見たい人にはここをすすめます。\n\n"
               "奈良公園のルートを全部歩いた日に法隆寺まで行くのは無理があります。JR奈良駅から大和路快速で11分、法隆寺駅から歩いて約20分（バスなら約8分）。近鉄奈良駅からJR奈良駅までも歩いて15分あり、片道で約50分みてください。中を見るのに1時間半はかかります。\n\n"
               "11月4日〜2月21日は16:30で閉まり、受付はその30分前までです。帰りは、法隆寺駅からJRで奈良へ戻るか、そのまま大阪方面（天王寺・大阪）へも出られます。\n\n"
               "拝観券は西院伽藍（金堂・五重塔）、大宝蔵院（百済観音・玉虫厨子）、東院伽藍（夢殿）の共通で、現金のみです。",
               "Horyuji Temple\n\nFounded by Prince Shotoku; its Golden Hall and five-storied pagoda date from the 7th century and are the oldest wooden buildings in the world. With Kofukuji’s pagoda hidden for now, this is where I’d send anyone who wants to see a five-storied pagoda.\n\n"
               "Going on to Horyuji after walking the whole Nara Park route is too much. It’s 11 minutes from JR Nara by Yamatoji Rapid, then about 20 minutes on foot from Horyuji Station (about 8 minutes by bus). Kintetsu-Nara to JR Nara is another 15 minutes’ walk, so allow about 50 minutes each way, and at least an hour and a half inside.\n\n"
               "From 4 November to 21 February it closes at 16:30, and tickets stop 30 minutes before. Afterwards, return by JR to Nara, or carry straight on by JR towards Osaka (Tennoji, Osaka).\n\n"
               "One ticket covers the Western Precinct (Golden Hall and pagoda), the Gallery of Temple Treasures (Kudara Kannon, Tamamushi Shrine) and the Eastern Precinct (Hall of Dreams). Cash only."),
        gmaps=[gm("法隆寺", "Horyuji", 34.61470, 135.73420, "法隆寺"), gm("JR法隆寺駅", "JR Horyuji Station", 34.60180, 135.73967, "JR法隆寺駅"),
               gm("JR奈良駅", "JR Nara Station", 34.68088, 135.81993, "JR奈良駅")],
        links=[link("official", "法隆寺 拝観案内", "Horyuji visitor information (Japanese)", "https://www.horyuji.or.jp/annai/"), YAHOO],
        info=info([row("hours", "2月22日〜11月3日 8:00〜17:00、11月4日〜2月21日 8:00〜16:30（受付は30分前まで）", "22 Feb – 3 Nov 8:00–17:00; 4 Nov – 21 Feb 8:00–16:30 (tickets until 30 minutes before closing)"),
                   row("fee", "2,000円（中学生1,700円、小学生1,000円）。西院伽藍・大宝蔵院・東院伽藍の共通。現金のみ", "¥2,000 (junior high ¥1,700, primary ¥1,000) for the Western Precinct, Gallery of Temple Treasures and Eastern Precinct. Cash only"),
                   row("train", "JR奈良 → 法隆寺 大和路快速で11分・240円（日中は約15分おき）", "JR Nara → Horyuji 11 min by Yamatoji Rapid, ¥240 (about every 15 minutes in the daytime)"),
                   row("bus", "法隆寺駅 南口 → 法隆寺参道 約8分（奈良交通バス72番。運賃は要確認）。歩くと約20分", "Horyuji Station south exit → Horyuji Sando about 8 min (Nara Kotsu bus 72; fare: please check). About 20 min on foot")],
                  "法隆寺 公式サイト（2025年3月改定の料金）、乗換案内、斑鳩町（バス）。2026-11-21に確認", cash=True, checked=D21,
                  tip=T("時間と料金は法隆寺の公式サイト（2025年3月改定）、電車は乗換案内、バスの時間は斑鳩町のページで確認しました（11月21日）。",
                        "Hours and fees checked on Horyuji’s website (revised March 2025); trains on a route planner; bus time on Ikaruga Town’s page (21 November)."))),
)

VIS, ARR = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time")
SIDE = [dict(first="heijo", last="horyuji", area=T("寄り道", "Side trips"), title=T("時間をつくって足をのばす", "If you make the time"))]

FIRST_11_21 = notice("毎月1・11・21日は、午前に特別参拝ができません", "No inner-area visits on the mornings of the 1st, 11th and 21st",
                     "このコースは午前に春日大社に着きます。その日は、お参り（無料）だけにするか、国宝殿（10:00〜）を見てください。11月23日・12月17日の午前も入れません。",
                     "This course reaches Kasuga Taisha in the morning. On those days, just pray (free) or see the shrine museum (from 10:00). The mornings of 23 November and 17 December are closed too.",
                     url="https://www.kasugataisha.or.jp/about/basic/")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
#   order の1件 = (スポットの id, 時間の見出し, 時間（日本語）, 時間（英語）, このコースでの行き方・過ごし方)
# ---------------------------------------------------------------------------
COURSES = [
    dict(
        id="late", file="nara.json",
        note="「9〜10時に出発」コース。烏丸御池9:21発の直通急行（近鉄奈良10:18着）か、大阪難波9:34発の快速急行（10:09着）。興福寺 国宝館→ならまちで早めのお昼→春鹿のきき酒→飛火野の鹿→春日大社→大仏殿（15:40〜16:35。団体が減る時間）→夕暮れの二月堂→駅のまわり・ならまちで晩ごはん→19:46か20:54の急行で京都へ（大阪は19:52・20:03の快速急行）。依水園と若草山は寄り道。",
        eki_rows=[row("train", "行き（京都・土曜）：烏丸御池 9:21発（急行 近鉄奈良行き・乗り換えなし）→ 近鉄奈良 10:18着・1,020円。京阪なら 三条 9:14発（特急）→ 丹波橋で乗り換え → 近鉄丹波橋 9:39発（同じ急行）→ 10:18着・1,000円",
                      "Out (Kyoto, Saturdays): Karasuma Oike 9:21 (express for Kintetsu-Nara, no change) → Kintetsu-Nara 10:18, ¥1,020. By Keihan: Sanjo 9:14 (limited express) → change at Tambabashi → Kintetsu-Tambabashi 9:39 (the same express) → 10:18, ¥1,000"),
                  row("train", "特急で行くなら（土曜）：烏丸御池 9:33発 → 京都 9:50発（近鉄特急）→ 近鉄奈良 10:28着・1,500円",
                      "By limited express (Saturdays): Karasuma Oike 9:33 → Kyoto 9:50 (Kintetsu limited express) → Kintetsu-Nara 10:28, ¥1,500"),
                  row("train", "行き（大阪・土曜）：大阪難波 9:34発（快速急行）→ 近鉄奈良 10:09着・680円。梅田からは御堂筋線 9:17発でなんばへ",
                      "Out (Osaka, Saturdays): Osaka-Namba 9:34 (rapid express) → Kintetsu-Nara 10:09, ¥680. From Umeda, the 9:17 Midosuji Line train to Namba connects"),
                  row("train", "帰り（京都・土曜）：近鉄奈良 19:46発（急行 京都行き）→ 竹田で地下鉄に乗り換え → 烏丸御池 20:43着・1,020円／20:54発（急行）→ 京都 21:39着 → 地下鉄で烏丸御池 21:56着・980円",
                      "Back (Kyoto, Saturdays): Kintetsu-Nara 19:46 (express for Kyoto) → change to the subway at Takeda → Karasuma Oike 20:43, ¥1,020 / 20:54 (express) → Kyoto 21:39 → subway → Karasuma Oike 21:56, ¥980"),
                  row("train", "帰り（大阪・土曜）：近鉄奈良 19:52発（快速急行）→ 大阪難波 20:28着／20:03発 → 20:41着・680円",
                      "Back (Osaka, Saturdays): Kintetsu-Nara 19:52 (rapid express) → Osaka-Namba 20:28 / 20:03 → 20:41, ¥680")],
        order=[
            ("eki", ARR, "10:18（烏丸御池 9:21発／大阪難波からは 9:34発→10:09着）", "10:18 (the 9:21 from Karasuma Oike; from Osaka-Namba, 9:34 → 10:09)",
             T("京都からは、烏丸御池9:21発の急行が近鉄奈良まで乗り換えなしです（土曜のダイヤ）。京阪の三条駅からなら9:14発の特急で丹波橋へ行くと、同じ急行に乗れます。大阪からは難波9:34発の快速急行で10:09着。\n\n"
               "このコースは、団体の多い昼の東大寺を避けて、先にならまちへ行きます。大仏殿は15時半すぎ、二月堂は夕暮れに。\n\n"
               "帰りは、奈良で晩ごはんを食べてから。近鉄奈良19:46発か20:54発の急行で、京都の中心に20:43か21:56に戻れます。大阪へは19:52発・20:03発の快速急行で約40分。早く帰る日は、17時台・18時台にも急行と快速急行があります（時刻は乗換案内で）。",
               "From Kyoto, the 9:21 express from Karasuma Oike runs straight through to Kintetsu-Nara (Saturday timetable). From Keihan Sanjo, the 9:14 limited express to Tambabashi connects with the same express. From Osaka, the 9:34 rapid express from Namba arrives at 10:09.\n\n"
               "This course avoids Todaiji at midday, when the tour groups are there, and goes to Naramachi first. The Great Buddha Hall comes after 15:30, Nigatsudo at dusk.\n\n"
               "Go home after dinner in Nara. The 19:46 or 20:54 express from Kintetsu-Nara gets you back to central Kyoto at 20:43 or 21:56. For Osaka, the 19:52 and 20:03 rapid expresses take about 40 minutes. If you leave earlier, there are expresses and rapid expresses in the 17:00 and 18:00 hours too (check a route planner).")),
            ("kofukuji", VIS, "10:30〜11:15", "10:30–11:15",
             T("駅から登大路の坂を上って5分。国宝館を見たら、南円堂の横の石段を下りて猿沢池へ。池の南がならまちです（歩いて約10分）。",
               "Five minutes up the Noborioji slope from the station. After the National Treasure Hall, take the stone steps beside the Nan’endo down to Sarusawa Pond. Naramachi is south of the pond, about 10 minutes on foot.")),
            ("isuien", VIS, "11:25〜12:05（寄る日は、ならまちのお昼を12:30ごろに。春鹿を短くして調整）", "11:25–12:05 (if you stop here, have lunch in Naramachi at about 12:30 and shorten the Harushika stop)",
             T("興福寺から東へ歩いて約10分。このコースでは寄り道です。夕方には閉まっている（入園16:00まで）ので、寄るなら午前のうちに。庭からならまちへは歩いて約20分。",
               "About 10 minutes’ walk east of Kofukuji. A side stop on this course. It is shut by late afternoon (last entry 16:00), so come in the morning if at all. From the gardens it’s about 20 minutes on foot to Naramachi.")),
            ("naramachi", VIS, "11:30〜13:05", "11:30–13:05",
             T("着いたらまずお昼に。11時半なら、開いたばかりの店が多く、入りやすい時間です。食べてから元興寺と格子の家へ。\n\n"
               "夜もここへ戻ってきます。二月堂から歩いて約35分、18時ごろ。なら泉勇斎は20:00まで、粟は予約して19:00までに入店。予約なしなら、もちいどのセンター街と東向商店街のアーケードで。",
               "Have lunch as soon as you arrive: at 11:30 many places have just opened and it’s easier to get a table. Then see Gangoji and Koshi-no-Ie.\n\n"
               "You come back here in the evening, about 35 minutes’ walk from Nigatsudo, at around 18:00. Nara Izumi Yusai is open until 20:00; Awa needs a booking and seats until 19:00. Without a booking, try the Mochiidono and Higashimuki arcades.")),
            ("harushika", VIS, "13:10〜13:50", "13:10–13:50",
             T("元興寺から東へ歩いて約5分。きき酒は30分ほど。このあと春日大社と東大寺まで1時間半ほど歩くので、水も飲んでおいてください。",
               "About 5 minutes’ walk east of Gangoji. The tasting takes about 30 minutes. You then walk about an hour and a half to Kasuga Taisha and Todaiji, so drink some water too.")),
            ("shika", VIS, "14:10〜14:25（飛火野）", "14:10–14:25 (Tobihino lawn)",
             T("春鹿から北東へ歩いて約15分で、春日大社の参道わきの芝生、飛火野（とびひの）に出ます。南大門の前より人が少なく、落ち着いて鹿せんべいをあげられます。",
               "About 15 minutes’ walk north-east of Harushika you come out on Tobihino, the lawn beside the approach to Kasuga Taisha. There are fewer people than in front of the Great South Gate, so it’s a calmer place for deer crackers.")),
            ("kasuga", VIS, "14:35〜15:15", "14:35–15:15",
             T("飛火野から石灯籠の並ぶ参道を上って約10分。特別参拝は16:00までなので、この時間なら入れます。\n\n"
               "東大寺へは、参道を戻って春日野園地の芝生を北へ、南大門まで歩いて約25分。大仏殿が閉まる時間（11〜3月は17:00）があるので、15:15には出てください。",
               "About 10 minutes up the lantern-lined approach from Tobihino. The inner area is open until 16:00, so you are in time.\n\n"
               "For Todaiji, go back down the approach and north across the Kasugano lawns: about 25 minutes to the Great South Gate. The Great Buddha Hall has a closing time (17:00 from November to March), so leave by 15:15.")),
            ("wakakusa", VIS, "15:25〜16:10（4〜10月だけ。ならまちか春鹿を短くして、ここまでを30分早めた日に）", "15:25–16:10 (April–October only, on a day when you have run 30 minutes ahead by shortening Naramachi or Harushika)",
             T("このコースでは寄り道です。春日大社から南ゲートまで歩いて約10分。11〜3月は大仏殿が17:00に閉まるので、上ると間に合いません。大仏殿が17:30まで開いている4〜10月に、一重目まで。",
               "A side stop on this course. The South Gate is about 10 minutes’ walk from Kasuga Taisha. From November to March the Great Buddha Hall closes at 17:00, so there isn’t time to climb. Do it from April to October, when the hall stays open until 17:30, and go as far as the first shoulder.")),
            ("todaiji", VIS, "15:40〜16:35", "15:40–16:35",
             T("昼の団体が減ってくることが多い時間です。南大門の仁王像を見上げてから大仏殿へ。11〜3月は17:00に閉まるので、16:00までには入ってください（4〜10月は17:30まで）。",
               "By this time the midday tour groups have usually thinned out. Look up at the guardians in the Great South Gate, then go on to the Great Buddha Hall. From November to March it closes at 17:00, so be inside by 16:00 (April to October: 17:30).")),
            ("nigatsudo", VIS, "16:45〜17:20", "16:45–17:20",
             T("大仏殿を出て右（東）へ、坂を上って約10分。11月下旬〜1月は、ちょうど日が沈んで灯籠に火が入る時間です。日の長い季節は、明るいうちの景色になります（6月の日の入りは19時すぎ）。\n\n"
               "帰りは裏参道の石畳を下り、大仏殿の裏から県庁の前を通って近鉄奈良駅へ、歩いて約30分。足元が暗くなるので、冬は小さなライトがあると安心です。ならまちへは約35分。",
               "Leaving the Great Buddha Hall, turn right (east) and climb for about 10 minutes. From late November to January this is just when the sun goes down and the lanterns are lit. In the long-day months you get the daytime view instead (sunset in June is after 19:00).\n\n"
               "Walk back down the stone-paved back lane, round behind the Great Buddha Hall and past the prefectural office to Kintetsu-Nara Station: about 30 minutes. It gets dark underfoot, so in winter a small light helps. Naramachi is about 35 minutes.")),
            ("heijo", VIS, "このコースでは建物に入れません（別の日か、早朝コースで）", "The buildings are shut by the time this course ends (another day, or on the early course)",
             T("このコースで歩き終わるのは17時すぎ。大極殿と朱雀門はもう閉まっています。", "This course finishes after 17:00, when the Daigokuden and the Suzaku Gate are already closed.")),
            ("horyuji", VIS, "このコースには入りません（別の日か、早朝コースで）", "Doesn’t fit this course (another day, or on the early course)",
             T("9〜10時に出る日は、法隆寺を入れると奈良公園が半分になります。行くなら、興福寺のあとJR奈良駅へ歩き（約20分）、12時ごろの電車で。午後は法隆寺だけになります。",
               "Leaving at 9–10, adding Horyuji cuts Nara Park in half. If you do go, walk from Kofukuji to JR Nara (about 20 minutes) for a train at around 12:00; the afternoon is then Horyuji only.")),
        ],
        sections=[dict(first="eki", last="isuien", day=0), dict(first="naramachi", last="harushika", day=1),
                  dict(first="shika", last="wakakusa", day=2), dict(first="todaiji", last="nigatsudo", day=3)] + SIDE,
        focus=("eki", "nigatsudo"),
        pos={"shika": (34.68074, 135.84083)},   # このコースでは、鹿のスポットの印を飛火野に置く
        default=["kofukuji", "naramachi", "harushika", "kasuga", "todaiji", "nigatsudo"], auto=["eki", "shika"],
        extra_notices={"todaiji": [notice("11〜3月は17:00に閉まります", "Closes at 17:00 from November to March",
                                          "このコースは15:40に南大門に着きます。春日大社を15:15までに出てください。",
                                          "This course reaches the Great South Gate at 15:40. Leave Kasuga Taisha by 15:15.",
                                          frm="2026-11-01", to="2027-03-31")]},
        hints=[("harushika", dict(any=["harushika"], none=["kasuga"]), None, None,
                "春日大社に寄らない日は、春鹿のあと飛火野から春日野園地の芝生を北へ歩いて、南大門まで約30分です。",
                "Skipping Kasuga Taisha? After Harushika, walk north from Tobihino across the Kasugano lawns: about 30 minutes to the Great South Gate."),
               ("todaiji", dict(any=["todaiji"], none=["naramachi", "harushika", "kasuga"]), None, None,
                "東大寺だけの日も、行くのは開門すぐか15時半すぎに。昼の10〜15時ごろは団体が多い時間です。",
                "Even on a Todaiji-only day, go right at opening or after 15:30. From about 10:00 to 15:00 the tour groups are there."),
               ("horyuji", dict(any=["horyuji"], andAny=["kasuga", "naramachi", "harushika", "todaiji", "nigatsudo", "wakakusa", "heijo"]), None, None,
                "法隆寺と奈良公園の全部は、9〜10時に出る日には入りません。法隆寺へ行くなら、午前は興福寺だけにして12時ごろJR奈良駅へ。",
                "Horyuji plus all of Nara Park doesn’t fit a 9–10 o’clock start. For Horyuji, keep the morning to Kofukuji and head for JR Nara at around 12:00.")]),
    dict(
        id="early", file="nara-early.json",
        note="「早朝に出発」コース（11〜3月は大仏殿が8:00開門）。烏丸御池6:24発→竹田6:38発の急行→大和西大寺7:16発→近鉄奈良7:22着（土曜。平日は7:28着）、大阪難波6:37発の快速急行→7:17着。奈良公園の鹿→南大門→大仏殿8:00→二月堂→春日大社→春日荷茶屋（10:30〜）で朝ごはん→ならまち→春鹿→興福寺 国宝館→15:45の急行で京都へ。4〜10月は7:30開門なので、1本早い電車（7:02着）で全部を20分早める。依水園と若草山は寄り道、平城宮跡と法隆寺はこのコースなら入る。",
        eki_rows=[row("train", "行き（京都・土曜）：烏丸御池 6:24発（地下鉄）→ 竹田 6:38発（近鉄急行）→ 大和西大寺 7:16発 → 近鉄奈良 7:22着・1,020円。平日は竹田 6:42発 → 近鉄奈良 7:28着",
                      "Out (Kyoto, Saturdays): Karasuma Oike 6:24 (subway) → Takeda 6:38 (Kintetsu express) → Yamato-Saidaiji 7:16 → Kintetsu-Nara 7:22, ¥1,020. On weekdays: Takeda 6:42 → Kintetsu-Nara 7:28"),
                  row("train", "京阪なら（土曜）：三条 6:13発（特急）→ 丹波橋で乗り換え → 近鉄丹波橋 6:41発（急行）→ 大和西大寺 7:16発 → 近鉄奈良 7:22着・1,000円",
                      "By Keihan (Saturdays): Sanjo 6:13 (limited express) → change at Tambabashi → Kintetsu-Tambabashi 6:41 (express) → Yamato-Saidaiji 7:16 → Kintetsu-Nara 7:22, ¥1,000"),
                  row("train", "行き（大阪）：大阪難波 6:37発（快速急行・土曜）→ 近鉄奈良 7:17着・680円。平日は 6:38発 → 7:16着",
                      "Out (Osaka): Osaka-Namba 6:37 (rapid express, Saturdays) → Kintetsu-Nara 7:17, ¥680. On weekdays: 6:38 → 7:16"),
                  row("train", "4〜10月（大仏殿は7:30開門）は1本早く：烏丸御池 5:54発 → 京都 6:15発（近鉄急行）→ 近鉄奈良 7:02着／三条 5:59発（京阪）→ 7:02着／大阪難波 6:17発（準急）→ 7:02着（2026年11月の土曜のダイヤ。春に確かめ直してください）",
                      "April–October (hall opens 7:30), one train earlier: Karasuma Oike 5:54 → Kyoto 6:15 (Kintetsu express) → Kintetsu-Nara 7:02 / Sanjo 5:59 (Keihan) → 7:02 / Osaka-Namba 6:17 (semi-express) → 7:02 (Saturday timetable of November 2026; check again in spring)"),
                  row("train", "帰り（土曜）：近鉄奈良 15:45発（急行 京都行き）→ 竹田で地下鉄に乗り換え → 烏丸御池 16:44着・1,020円。大阪へは 15:26発（急行）→ 大阪難波 16:05着／15:36発（快速急行）→ 16:16着・680円",
                      "Back (Saturdays): Kintetsu-Nara 15:45 (express for Kyoto) → change to the subway at Takeda → Karasuma Oike 16:44, ¥1,020. For Osaka: 15:26 (express) → Osaka-Namba 16:05 / 15:36 (rapid express) → 16:16, ¥680")],
        order=[
            ("eki", ARR, "7:22（烏丸御池 6:24発／大阪難波からは 6:37発→7:17着）", "7:22 (the 6:24 from Karasuma Oike; from Osaka-Namba, 6:37 → 7:17)",
             T("大仏殿の開門（11〜3月は8:00）に合わせる電車です。京都からは、烏丸御池6:24発の地下鉄で竹田へ、6:38発の近鉄の急行に乗り換え、大和西大寺でもう一度乗り換えて7:22着（土曜。平日は7:28着）。大阪からは難波6:37発の快速急行で7:17着（平日は6:38発）。\n\n"
               "4〜10月は大仏殿が7:30に開くので、1本早い電車で7:02に着いてください（時刻は下の表に）。この先の時間もすべて20〜30分早まります。\n\n"
               "朝ごはんは春日大社のあと、10:30ごろになります。出る前に何か少し食べておくか、電車の中で食べてください。奈良公園で食べ物を出すと鹿が寄ってきます。\n\n"
               "朝5時台から動いた日なので、帰りは15:45発の急行（烏丸御池16:44着）をめやすに。大阪へは15:26発か15:36発で約40分。",
               "These trains are timed for the opening of the Great Buddha Hall (8:00 from November to March). From Kyoto, take the 6:24 subway from Karasuma Oike to Takeda, change to the 6:38 Kintetsu express, change once more at Yamato-Saidaiji and arrive at 7:22 (Saturdays; 7:28 on weekdays). From Osaka, the 6:37 rapid express from Namba arrives at 7:17 (6:38 on weekdays).\n\n"
               "From April to October the hall opens at 7:30, so take one train earlier and arrive at 7:02 (times in the table below). Everything after that moves 20–30 minutes earlier too.\n\n"
               "Breakfast comes after Kasuga Taisha, at about 10:30. Eat a little before you leave or on the train. If you take food out in Nara Park, the deer come for it.\n\n"
               "You have been up since before six, so aim for the 15:45 express home (Karasuma Oike 16:44). For Osaka, the 15:26 or 15:36 takes about 40 minutes.")),
            ("shika", VIS, "7:30〜7:45", "7:30–7:45",
             T("駅から登大路の坂を上って、興福寺の境内を抜けると、もう鹿がいます。この時間は観光客がほとんどいません。鹿せんべいの売り場が朝何時から開くかは確認できていないので、せんべいは帰り道の楽しみに。県庁の前から南大門まで歩いて約15分。",
               "Walk up the Noborioji slope from the station and through the grounds of Kofukuji, and the deer are already there. At this hour there are hardly any visitors. It isn’t confirmed what time the cracker stands open, so save the crackers for later in the day. From the prefectural office it’s about 15 minutes’ walk to the Great South Gate.")),
            ("todaiji", VIS, "7:50〜8:50（11〜3月は8:00開門、4〜10月は7:30開門）", "7:50–8:50 (opens 8:00 Nov–Mar, 7:30 Apr–Oct)",
             T("7:50ごろ南大門に着きます。まだ人が少ないので、仁王像をゆっくり見上げてから、大仏殿の入口（左の回廊の端）へ。8:00に開きます。団体が増える前に、大仏さまの前でゆっくりできます。",
               "You reach the Great South Gate at about 7:50. With few people around, take your time looking up at the guardians, then go to the entrance of the Great Buddha Hall (the left end of the cloister). It opens at 8:00, and you can take your time in front of the Great Buddha before the tour groups build up.")),
            ("nigatsudo", VIS, "9:00〜9:30", "9:00–9:30",
             T("大仏殿を出て右（東）へ、坂を上って約10分。舞台の北の休憩所でひと休みできます（開いている時間は要確認）。\n\n"
               "ここから春日大社へは、手向山八幡宮（たむけやまはちまんぐう）の前を通り、若草山のふもとのみやげ物屋の並ぶ道を南へ、歩いて約20分です。",
               "Leaving the Great Buddha Hall, turn right (east) and climb for about 10 minutes. You can rest at the rest house north of the balcony (opening hours: please check).\n\n"
               "From here to Kasuga Taisha, pass Tamukeyama Hachimangu and walk south along the lane of souvenir shops at the foot of Mt. Wakakusa: about 20 minutes.")),
            ("wakakusa", VIS, "9:35〜10:20（上る日は、この先を45分ずつ遅らせます）", "9:35–10:20 (if you climb, shift everything after by 45 minutes)",
             T("このコースでは寄り道です。二月堂から北ゲートまで歩いて約5分。ゲートは9:00に開きます。下りは南ゲートから出ると春日大社に近いです。",
               "A side stop on this course. The North Gate is about 5 minutes’ walk from Nigatsudo and opens at 9:00. Leave by the South Gate: it’s closer to Kasuga Taisha.")),
            ("kasuga", VIS, "9:50〜10:30、そのあと春日荷茶屋で朝ごはん（10:30〜11:15）", "9:50–10:30, then breakfast at Kasuga Ninaijaya (10:30–11:15)",
             T("特別参拝は9:00から。お参りのあと、二之鳥居から参道を西へ約8分下ると、右手に春日荷茶屋があります。10:30に開くので、ここで朝ごはん（万葉粥）とひと休み。荷茶屋が休みの日（不定休。公式サイトに出ます）は、ならまちまで歩いてお昼を早めに。\n\n"
               "ならまちへは、参道を下って飛火野（とびひの）の芝生の横を通り、南西へ歩いて約25分。飛火野は鹿せんべいをあげるのにいい場所です。",
               "The inner area opens at 9:00. After the shrine, walk about 8 minutes west down the approach from the second torii and Kasuga Ninaijaya is on your right. It opens at 10:30: have breakfast (Man’yo-gayu porridge) and a rest here. If the teahouse is closed (irregular days, listed on the website), walk on to Naramachi and have an early lunch.\n\n"
               "For Naramachi, go down the approach past the Tobihino lawn and head south-west: about 25 minutes. Tobihino is a good place for deer crackers.")),
            ("naramachi", VIS, "11:40〜13:10", "11:40–13:10",
             T("元興寺、格子の家を見て、お昼に。10:30にお粥を食べているので、軽いお昼か甘いもので十分かもしれません。鹿の舟の観光案内所「繭」は休憩にも使えます。",
               "See Gangoji and Koshi-no-Ie, then have lunch. After porridge at 10:30, a light lunch or something sweet may be enough. The tourist information centre “Mayu” at Shika-no-Fune is a good place to sit down.")),
            ("harushika", VIS, "13:15〜13:55", "13:15–13:55",
             T("元興寺から東へ歩いて約5分。きき酒は30分ほど。早起きした日のお酒は回りやすいので、水も一緒に。",
               "About 5 minutes’ walk east of Gangoji. The tasting takes about 30 minutes. Sake hits harder after an early start, so drink water with it.")),
            ("kofukuji", VIS, "14:15〜15:00", "14:15–15:00",
             T("春鹿から北西へ、猿沢池の横の石段を上って歩いて約15分。朝に通り抜けた境内へ戻ってきて、国宝館を見ます。ここから近鉄奈良駅まで歩いて約7分。15:45発の急行で、烏丸御池に16:44に着きます。\n\n"
               "まだ元気な人は、依水園（入園16:00まで）か、帰りの電車を大和西大寺で降りて平城宮跡へ。",
               "About 15 minutes’ walk north-west of Harushika, up the stone steps beside Sarusawa Pond. You are back in the grounds you crossed this morning, now for the National Treasure Hall. From here it’s about 7 minutes’ walk to Kintetsu-Nara Station; the 15:45 express gets you to Karasuma Oike at 16:44.\n\n"
               "Still have energy? Go on to Isuien (last entry 16:00), or get off your train home at Yamato-Saidaiji for the Heijo Palace site.")),
            ("isuien", VIS, "15:10〜15:50（入園は16:00まで。火曜休み）", "15:10–15:50 (last entry 16:00; closed Tuesdays)",
             T("このコースでは寄り道です。興福寺から東へ歩いて約10分。見終わったら、駅まで歩いて約12分。",
               "A side stop on this course. About 10 minutes’ walk east of Kofukuji. Afterwards it’s about 12 minutes on foot to the station.")),
            ("heijo", VIS, "15:40〜16:30（興福寺を14:55ごろに出て、15時すぎの電車で大和西大寺へ）", "15:40–16:30 (leave Kofukuji at about 14:55 and take a train soon after 15:00 to Yamato-Saidaiji)",
             T("早朝コースなら、帰り道に寄れます。大極殿の入場は16:00までなので、興福寺の国宝館を少し早めに出てください。月曜は建物が休みです。",
               "On the early course you can stop here on the way home. Last entry to the Daigokuden is 16:00, so leave Kofukuji’s National Treasure Hall a little early. The buildings are closed on Mondays.")),
            ("horyuji", VIS, "12:45〜14:30（ならまち・春鹿・興福寺をやめて行く場合）", "12:45–14:30 (in place of Naramachi, Harushika and Kofukuji)",
             T("早朝コースなら同じ日に入ります。春日荷茶屋で朝ごはんを食べたら（11:15）、三条通をまっすぐ西へJR奈良駅まで歩いて約35分。12時ごろの大和路快速に乗れば、12:45ごろ法隆寺に着きます。ならまち・春鹿・興福寺は外すことになります。",
               "On the early course it fits the same day. After breakfast at Kasuga Ninaijaya (11:15), walk straight west along Sanjo-dori to JR Nara, about 35 minutes. A Yamatoji Rapid at around 12:00 gets you to Horyuji by about 12:45. You give up Naramachi, Harushika and Kofukuji.")),
        ],
        sections=[dict(first="eki", last="nigatsudo", day=0), dict(first="wakakusa", last="kasuga", day=1),
                  dict(first="naramachi", last="harushika", day=2), dict(first="kofukuji", last="isuien", day=3)] + SIDE,
        focus=("eki", "isuien"),
        default=["todaiji", "nigatsudo", "kasuga", "naramachi", "harushika", "kofukuji"], auto=["eki", "shika"],
        extra_notices={"kasuga": [FIRST_11_21],
                       "todaiji": [notice("4〜10月は7:30に開きます", "Opens at 7:30 from April to October",
                                          "開門に合わせるなら、近鉄奈良駅に7:02に着く電車で。時刻は近鉄奈良駅のスポットに書いてあります。",
                                          "To be there at opening, take the train that reaches Kintetsu-Nara at 7:02. Times are in the Kintetsu-Nara Station entry.",
                                          frm="2027-03-25", to="2027-10-31")]},
        hints=[("naramachi", dict(any=["naramachi"], none=["kasuga"]), None, None,
                "春日大社に寄らない日は、二月堂から大仏殿の横を通って興福寺・猿沢池へ戻り、南へ。歩いて約40分です。朝ごはんは、鹿の舟の「竈」（11:00〜、水曜休み）などで早めのお昼に。",
                "Skipping Kasuga Taisha? Walk back from Nigatsudo past the Great Buddha Hall, Kofukuji and Sarusawa Pond, then south: about 40 minutes. Make breakfast an early lunch, for example at Kamado in Shika-no-Fune (from 11:00, closed Wednesdays)."),
               ("horyuji", dict(any=["horyuji"], andAny=["naramachi", "harushika", "kofukuji", "heijo", "isuien"]), None, None,
                "法隆寺へ行く日は、春日荷茶屋のあと（11:15）JR奈良駅へ向かいます。ならまち・春鹿・興福寺・平城宮跡は入りません。",
                "On a Horyuji day, head for JR Nara after Kasuga Ninaijaya (11:15). Naramachi, Harushika, Kofukuji and the Heijo Palace site don’t fit."),
               ("heijo", dict(any=["heijo"], andAny=["isuien"]), None, None,
                "依水園と平城宮跡の両方は入りません。どちらか1つに。",
                "Isuien and the Heijo Palace site don’t both fit. Choose one.")]),
]

NOTE_HEAD = "京都・大阪から日帰り 奈良のルート（nara/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（nara.json＝9〜10時に出発、nara-early.json＝早朝に出発）。このファイル："
NOTE_TAIL = (" Toshi の写真は2022年12月28日（東大寺・鹿・春日大社・春鹿・猿沢池）と2021〜2022年の駅の写真。手持ちが少ないので、ほかは Wikimedia Commons の写真（写真の上に撮影者とライセンスを表示）。"
             "info.source は確認した出典、info.checked は確認日、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。このファイルは scripts/build_nara_data.py で作る（直接直さない）。")


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    spots = []
    for sid, (lj, le), tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        if sid == "eki":
            b["info"] = info(c["eki_rows"] + b.pop("_rows"), b.pop("_source"), tip=b.pop("_tip"))
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out["text"] = T(body["ja"] + "\n\n" + go["ja"] + f"\n\n{lj}：{tj}", body["en"] + "\n\n" + go["en"] + f"\n\n{le}: {te}")
        if sid in c.get("pos", {}):
            out["lat"], out["lng"] = c["pos"][sid]
        out["photos"] = PHOTOS[sid]
        for p in out["photos"]:
            f = p if isinstance(p, str) else p["file"]
            assert os.path.exists(f"{IMG}/{f}"), f
        out["notices"] = c.get("extra_notices", {}).get(sid, []) + out.get("notices", [])
        spots.append(out)
    auto = c["auto"]
    secs = []
    for s in c["sections"]:
        d = {"first": NO[s["first"]], "last": NO[s["last"]]}
        if "day" in s:
            d["day"] = s["day"]
        else:
            d["area"], d["title"] = s["area"], s["title"]
        secs.append(d)
    rule = lambda r: {k: [NO[i] for i in v] for k, v in r.items()}
    data = {
        "id": MAP_ID,
        "course": c["id"],
        "_note": NOTE_HEAD + c["note"] + NOTE_TAIL,
        "sections": secs,
        "focus": {"first": NO[c["focus"][0]], "last": NO[c["focus"][1]]},
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は時間割どおりに1日で回れる6か所。それ以外（依水園・若草山・平城宮跡・法隆寺）は寄り道で、足したときの回り方は各スポットの文章と hints。近鉄奈良駅と鹿は全員共通。",
                 "defaultMode": "pick",
                 "picks": [NO[x[0]] for x in order if x[0] not in auto],
                 "defaultPicks": [NO[i] for i in c["default"]],
                 "auto": {str(NO[i]): {"always": True} for i in auto},
                 "hints": [{"spot": NO[sid], "rule": rule(r), "from": frm, "to": to, "text": T(ja, en)} for sid, r, frm, to, ja, en in c["hints"]]},
        "photoBase": f"../images/{MAP_ID}/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


for c in COURSES:
    build(c)
