#!/usr/bin/env python3
"""京都から日帰り 奈良のデータ（data/routes/nara.json）を書き出す。

使い方: python3 scripts/build_nara_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は下の PHOTOS に、スポットごとに表示する順で書く。Toshi の写真はファイル名だけ、
  Wikimedia Commons から借りた写真は W(ファイル名, 撮影者, ライセンス, ファイルのページ名) で書く（写真の上にクレジットが出る）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/nara"
OUT = f"{R}/data/routes/nara.json"
CHECKED = "2026-11-21"


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def info(rows, tip=None, verified=True, cash=False):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def W(file, author, lic, title):
    return {"file": file, "credit": {"author": author, "license": lic,
                                     "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


# 写真（表示する順）。文字だけのものは Toshi の写真
PHOTOS = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nara_photos.py"), encoding="utf-8").read())

JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")

S = [
    dict(id="eki", name=T("近鉄奈良駅", "Kintetsu-Nara Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都から近鉄で。特急なら約35分、急行なら約50分。奈良公園へは、JRより近鉄の駅のほうがずっと近いです。",
                 "From Kyoto by Kintetsu: about 35 minutes by limited express, about 50 by express. For Nara Park, the Kintetsu station is much closer than JR."),
         lat=34.68414, lng=135.82854,
         text=T("近鉄奈良駅（きんてつならえき）\n\n京都駅の近鉄のりばから出発します。行き方は3つ。\n\n"
                "・近鉄特急：約35分、1,280円（運賃760円＋特急券520円）。全席指定で必ず座れます。土曜は京都8:30発→近鉄奈良9:08着（乗り換えなし）。特急券は駅の券売機か、近鉄の「チケットレスサービス」で。\n"
                "・近鉄の急行：約50分、760円。橿原神宮前行きに乗り、大和西大寺（やまとさいだいじ）で向かいのホームの奈良行きに乗り換えることがほとんどです。土曜は京都8:42発→9:30着。\n"
                "・JRのみやこ路快速：約47分、720円。京都9:04発→奈良9:51着（日中は30分おき）。ただしJR奈良駅は近鉄奈良駅より西に約1km離れていて、興福寺まで歩いて約20分かかります。ジャパン・レール・パスを使う人向けです。\n\n"
                "近鉄奈良駅は地下の駅です。東改札を出て2番出口の階段を上がると、行基（ぎょうき）さんの噴水の前。そこから東へ、ゆるい坂（登大路）を上ると5分で興福寺、その先が奈良公園です。\n\n"
                "ICカード（ICOCA・Suicaなど）は近鉄・JRとも使えます。お寺の拝観料は現金だけの所が多いので、千円札と小銭を多めに。\n\n"
                "帰りは、近鉄奈良16:13発の急行（京都16:59着・乗り換えなし）か、16:25発の特急（17:01着）がちょうどいい時間です。\n\nおすすめ到着時間：9:08",
                "Kintetsu-Nara Station\n\nYou leave from the Kintetsu platforms at Kyoto Station. There are three ways.\n\n"
                "• Kintetsu limited express: about 35 minutes, ¥1,280 (¥760 fare + ¥520 express ticket). All seats reserved, so you always sit. On Saturdays: Kyoto 8:30 → Kintetsu-Nara 9:08, direct. Buy the express ticket at a station machine or on Kintetsu’s ticketless service.\n"
                "• Kintetsu express: about 50 minutes, ¥760. Most trains go towards Kashiharajingu-mae; change at Yamato-Saidaiji to the Nara train across the platform. On Saturdays: Kyoto 8:42 → 9:30.\n"
                "• JR Miyakoji Rapid: about 47 minutes, ¥720. Kyoto 9:04 → Nara 9:51 (every 30 minutes in the daytime). But JR Nara Station is about 1 km west of Kintetsu-Nara, a 20-minute walk to Kofukuji. Best if you hold a Japan Rail Pass.\n\n"
                "Kintetsu-Nara is underground. Leave by the east gates and take the stairs at Exit 2; you come up by the fountain with the statue of the monk Gyoki. Walk east up the gentle slope (Noborioji): 5 minutes to Kofukuji, with Nara Park just beyond.\n\n"
                "IC cards (ICOCA, Suica and so on) work on both Kintetsu and JR. Many temples take cash only, so bring ¥1,000 notes and coins.\n\n"
                "Going back, the 16:13 express (Kyoto 16:59, direct) or the 16:25 limited express (Kyoto 17:01) are well timed.\n\nRecommended arrival: 9:08"),
         gmaps=[gm("近鉄奈良駅", "Kintetsu-Nara Station", 34.68414, 135.82854, "近鉄奈良駅"),
                gm("京都駅の近鉄のりば", "Kintetsu platforms, Kyoto Station", 34.98463, 135.75731, "近鉄京都駅")],
         links=[link("official", "近鉄特急チケットレスサービス", "Kintetsu limited express ticketless service (Japanese)", "https://www.kintetsu.co.jp/gyoumu/ticket/"),
                link("official", "奈良世界遺産フリーきっぷ（近鉄）", "Nara World Heritage Free Ticket (Kintetsu, Japanese)", "https://www.kintetsu.co.jp/senden/Railway/Ticket/sekaiisan/nara_nishi.html"), JR],
         info=info([row("train", "近鉄特急：京都8:30発 → 近鉄奈良9:08着・1,280円（土曜。平日は8:55発→9:29着など）", "Kintetsu limited express: Kyoto 8:30 → Kintetsu-Nara 9:08, ¥1,280 (Saturdays; on weekdays e.g. 8:55 → 9:29)"),
                    row("train", "近鉄の急行：京都8:42発 → 9:30着・760円（大和西大寺で乗り換え）", "Kintetsu express: Kyoto 8:42 → 9:30, ¥760 (change at Yamato-Saidaiji)"),
                    row("train", "JRみやこ路快速：京都9:04発 → JR奈良9:51着・720円", "JR Miyakoji Rapid: Kyoto 9:04 → JR Nara 9:51, ¥720"),
                    row("train", "帰り：近鉄奈良16:13発（急行）→ 京都16:59着／16:25発（特急）→ 17:01着／17:55発（特急）→ 18:30着", "Return: Kintetsu-Nara 16:13 (express) → Kyoto 16:59 / 16:25 (limited express) → 17:01 / 17:55 (limited express) → 18:30"),
                    row("fee", "法隆寺や平城宮跡までバス・近鉄で回る日は「奈良世界遺産フリーきっぷ 奈良・斑鳩1日コース」（京都から1,800円）が得。歩いて回るだけなら普通のきっぷで十分です",
                        "If you add Horyuji or the Heijo Palace site by bus and Kintetsu, the Nara World Heritage Free Ticket (Nara–Ikaruga 1-day, ¥1,800 from Kyoto) pays off. For the walking route alone, ordinary tickets are cheaper")],
                   tip=T("時刻と運賃は乗換案内（2026年11月28日・土曜のダイヤ）、きっぷは近鉄の公式サイトで確認しました。時刻は曜日で変わるので、乗る前にもう一度確かめてください。写真は近鉄奈良駅のホームで撮った京都行きの特急（2021年）と、JR奈良駅の京都行き（2022年）です。",
                         "Times and fares checked on a route planner (Saturday 28 November 2026 timetable); tickets on Kintetsu’s website. Times differ by day, so check again before you travel. The photos show Kyoto-bound limited expresses at Kintetsu-Nara (2021) and a Kyoto-bound train at JR Nara (2022)."))),
    dict(id="kofukuji", name=T("興福寺", "Kofukuji Temple"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
         blurb=T("駅から5分。阿修羅像のいる国宝館は、朝いちばんが空いています。五重塔は修理中で、覆いの中です。",
                 "Five minutes from the station. The National Treasure Hall with the Ashura statue is quietest first thing. The five-storied pagoda is under repair, hidden inside its cover."),
         caution=T("五重塔は修理中（覆いで見えません）", "Pagoda under repair (covered, not visible)"),
         lat=34.68325, lng=135.83117,
         text=T("興福寺（こうふくじ）\n\n藤原氏の氏寺として1300年続くお寺です。境内は塀がなく、朝から自由に歩けます。\n\n"
                "先に知っておいてほしいこと：奈良の絵はがきでおなじみの五重塔は、約120年ぶりの大修理の最中で、塔全体が工事用の建物（素屋根）にすっぽり覆われています。外から塔の姿は見えません。工事は2030年代前半まで続く予定です。夜の猿沢池（さるさわいけ）に塔が映る3枚目の写真は、工事が始まる前の2022年12月に撮ったものです。\n\n"
                "それでも寄る価値があるのは国宝館です。3つの顔と6本の腕をもつ阿修羅（あしゅら）像をはじめ、教科書で見た仏像がガラスなしで目の前に並びます。9時に開くので、着いたらまずここへ。10時を過ぎると修学旅行の団体が増えます。\n\n"
                "2018年に再建された朱色の中金堂（ちゅうこんどう）、八角形の南円堂（なんえんどう）は外から見るだけなら無料。南円堂の横の石段を下りると猿沢池です。\n\n"
                "拝観料は現金だけ。お堂と国宝館の中にトイレはありません。\n\nおすすめ訪問時間：9:15〜9:55",
                "Kofukuji Temple\n\nThe family temple of the Fujiwara clan, 1,300 years old. The grounds have no walls and you can walk in freely from early morning.\n\n"
                "One thing to know first: the five-storied pagoda from every Nara postcard is in the middle of its first major repair in about 120 years, and the whole tower is wrapped in a construction shelter. You cannot see it from outside. The work is planned to run into the early 2030s. The third photo, the pagoda reflected in Sarusawa Pond at night, was taken in December 2022, before the work began.\n\n"
                "What still makes the stop worthwhile is the National Treasure Hall. The three-faced, six-armed Ashura and other statues you may know from textbooks stand right in front of you, with no glass. It opens at 9:00, so go there first; school groups build up after 10:00.\n\n"
                "The vermilion Central Golden Hall, rebuilt in 2018, and the octagonal Nan’endo are free to see from outside. The stone steps beside the Nan’endo lead down to Sarusawa Pond.\n\n"
                "Admission is cash only. There are no toilets inside the halls or the museum.\n\nRecommended visit time: 9:15–9:55"),
         gmaps=[gm("興福寺 国宝館", "Kofukuji National Treasure Hall", 34.68353, 135.83253, "興福寺 国宝館"),
                gm("猿沢池", "Sarusawa Pond", 34.68144, 135.83095, "猿沢池")],
         links=[link("official", "興福寺 拝観案内", "Kofukuji visitor information (Japanese)", "https://www.kohfukuji.com/info/info-guide/"),
                link("info", "五重塔の保存修理（奈良県）", "Pagoda repair work (Nara Prefecture, Japanese)", "https://www.pref.nara.jp/62140.htm")],
         info=info([row("hours", "国宝館・中金堂・東金堂 9:00〜17:00（受付は16:45まで）、休みなし。境内は自由", "National Treasure Hall, Central Golden Hall, Eastern Golden Hall 9:00–17:00 (last entry 16:45), open daily. Grounds always open"),
                    row("fee", "国宝館 900円、中金堂 500円、東金堂 500円（現金のみ）", "National Treasure Hall ¥900, Central Golden Hall ¥500, Eastern Golden Hall ¥500 (cash only)"),
                    row("fee", "11月30日まで：東金堂の後堂の特別公開中（東金堂＋後堂 1,000円、4か所共通券 2,000円・販売は16:00まで）", "Until 30 November: special opening of the rear hall of the Eastern Golden Hall (hall + rear hall ¥1,000; 4-site combined ticket ¥2,000, sold until 16:00)", until="2026-11-30")],
                   cash=True,
                   tip=T("時間と料金は興福寺の公式サイト、五重塔の工事は奈良県のページで確認しました。12月以降の共通券の料金は確認できていません（要確認）。",
                         "Hours and fees checked on Kofukuji’s website; the pagoda work on Nara Prefecture’s page. The combined-ticket price from December could not be confirmed (please check)."))),
    dict(id="shika", name=T("奈良公園の鹿", "The deer of Nara Park"), kind=T("公園・鹿", "Park & deer"),
         blurb=T("興福寺を出たら、もう鹿がいます。鹿せんべいは買ったらすぐあげる。これだけ守れば楽しい時間です。",
                 "Step out of Kofukuji and the deer are already there. Buy the crackers, hand them over at once: keep to that and it’s great fun."),
         lat=34.68412, lng=135.83450,
         text=T("奈良公園（ならこうえん）の鹿\n\n県庁の向かいの芝生（登大路園地）から東大寺の南大門まで、道ばたにも芝生にも鹿がいます。約1,300頭、国の天然記念物で、飼われているのではなく野生です。\n\n"
                "鹿せんべいは、道ばたの売り場で買えます（2019年から10枚200円。今の値段は売り場で確かめてください。小銭を用意）。あげ方のコツは奈良県の案内のとおりです。\n\n"
                "・買ったらすぐにあげる。じらすと、服やお尻をかまれます\n"
                "・なくなったら、両手を開いて「もうないよ」と見せる。これで離れていきます\n"
                "・鹿せんべい以外の食べ物はあげない（おなかを壊します）\n"
                "・かばんから出ている地図や紙袋は食べられます。しまっておく\n"
                "・小さい子は必ず大人と一緒に\n"
                "・5月中旬〜7月は子鹿の季節。母鹿が気が立っています。子鹿にはさわらない\n"
                "・秋（9〜11月ごろ）は角のある雄鹿に近づかない\n\n"
                "南大門の前は鹿も人もいちばん多く、せんべいを持った瞬間に囲まれます。落ち着いてあげたいなら、手前の登大路園地か、春日大社へ向かう参道わきの芝生（飛火野・とびひの）が静かです。公園にごみ箱はないので、包み紙は持ち帰ります（せんべいを束ねている紙は鹿が食べられます）。\n\n"
                "向かいの奈良国立博物館は、仏像館が改修で2028年春ごろまで休館中。今は青銅器館で仏像の名品を少しだけ見られます。\n\nおすすめ訪問時間：10:00〜10:15",
                "The deer of Nara Park\n\nFrom the lawn opposite the prefectural office (Noborioji Park) all the way to Todaiji’s Great South Gate, deer are on the paths and on the grass. There are about 1,300 of them; they are a protected natural monument and wild, not kept.\n\n"
                "Deer crackers (shika-senbei) are sold at stands along the way (¥200 for ten since 2019; check the price at the stand, and have coins ready). Nara Prefecture’s own advice on feeding:\n\n"
                "• Hand them over as soon as you buy them. Tease, and you get nipped on the clothes or the backside\n"
                "• When you run out, show both open hands. The deer understand and walk away\n"
                "• Never give any other food; it makes them ill\n"
                "• Maps and paper bags sticking out of your bag get eaten. Put them away\n"
                "• Small children only together with an adult\n"
                "• Mid-May to July is fawn season and mothers are on edge. Don’t touch fawns\n"
                "• In autumn (about September to November) keep away from stags with antlers\n\n"
                "In front of the Great South Gate both deer and people are thickest, and you are surrounded the moment you hold a cracker. For a calmer time, feed them here at Noborioji Park, or on the Tobihino lawn beside the path to Kasuga Taisha. There are no rubbish bins in the park, so take wrappers with you (the paper band around the crackers is safe for deer).\n\n"
                "Across the road, the Nara National Museum’s Buddhist Sculpture Hall is closed for renovation until about spring 2028; for now a small selection of its statues is shown in the Bronze Hall.\n\nRecommended visit time: 10:00–10:15"),
         gmaps=[gm("奈良公園 登大路園地", "Noborioji Park", 34.68412, 135.83450, "奈良公園 登大路園地"),
                gm("飛火野", "Tobihino lawn", 34.68074, 135.84093, "飛火野 奈良公園")],
         links=[link("official", "奈良公園の鹿（奈良公園クイックガイド）", "The deer of Nara Park (Nara Park Quick Guide, Japanese)", "https://www.pref.nara.lg.jp/site/park/1003.html"),
                link("official", "奈良の鹿愛護会", "Nara Deer Preservation Foundation (Japanese)", "https://naradeer.com/"),
                link("official", "奈良国立博物館", "Nara National Museum", "https://www.narahaku.go.jp/", "https://www.narahaku.go.jp/english/")],
         info=info([row("hours", "公園は出入り自由", "The park is always open"),
                    row("fee", "鹿せんべい：10枚200円（2019年の改定時の値段。今の値段は要確認）", "Deer crackers: ¥200 for ten (the price set in 2019; please check the current price)")],
                   cash=True, verified=False,
                   tip=T("鹿との接し方は奈良県の「奈良公園クイックガイド」と奈良の鹿愛護会のページで確認しました。鹿せんべいの今の値段と支払い方法は、公式のページでは確認できませんでした。写真は2022年12月。",
                         "The advice on deer is from Nara Prefecture’s Nara Park Quick Guide and the Nara Deer Preservation Foundation. The current cracker price and payment methods could not be confirmed on an official page. Photos: December 2022."))),
    dict(id="isuien", name=T("依水園・吉城園", "Isuien & Yoshikien gardens"), kind=T("日本庭園", "Japanese gardens"),
         blurb=T("東大寺のすぐ手前にある、隣り合う2つの庭。人の波から5分で静かになります。吉城園は無料です。",
                 "Two neighbouring gardens just before Todaiji. Five minutes off the crowded path and it’s quiet. Yoshikien is free."),
         lat=34.68547, lng=135.83792,
         text=T("依水園（いすいえん）と吉城園（よしきえん）\n\n県庁の東の交差点から北へ入った細い道に、入口が並んでいます。南大門まで歩いて5分なのに、団体はほとんど来ません。\n\n"
                "依水園は、池の向こうに東大寺の南大門の屋根と若草山を取り込んだ「借景」の庭。奈良でひとつ庭を見るならここです。入園料に寧楽（ねいらく）美術館も含まれます。火曜が休みで、9月下旬と年末〜1月中旬には庭の手入れで休む期間があります。\n\n"
                "隣の吉城園は苔の庭と茶室の庭。こちらは無料なので、時間がなければ吉城園だけ10分のぞくのもありです。\n\n"
                "どちらも紅葉は11月中旬〜12月初め。\n\nおすすめ訪問時間：10:20〜11:00（ここに寄る日は、この先を40分ずつ遅らせます）",
                "Isuien and Yoshikien\n\nTheir gates stand side by side on a narrow lane running north from the crossing east of the prefectural office. They are 5 minutes from the Great South Gate, yet tour groups hardly come.\n\n"
                "Isuien is a “borrowed scenery” garden: beyond its pond you see the roof of Todaiji’s Great South Gate and Mt. Wakakusa as part of the view. If you see one garden in Nara, make it this one. Admission includes the Neiraku Museum. Closed on Tuesdays, and for garden maintenance in late September and from late December to mid-January.\n\n"
                "Next door, Yoshikien has a moss garden and a tea-house garden. It’s free, so if time is short, just look into Yoshikien for 10 minutes.\n\n"
                "Autumn colours in both: mid-November to early December.\n\nRecommended visit time: 10:20–11:00 (if you stop here, shift everything after by 40 minutes)"),
         gmaps=[gm("依水園", "Isuien", 34.68547, 135.83792, "依水園 奈良"), gm("吉城園", "Yoshikien", 34.68510, 135.83721, "吉城園 奈良")],
         links=[link("official", "依水園・寧楽美術館", "Isuien Garden & Neiraku Museum", "https://isuien.or.jp/"),
                link("official", "吉城園（奈良県）", "Yoshikien (Nara Prefecture, Japanese)", "https://www.pref.nara.jp/39910.htm")],
         info=info([row("hours", "依水園 9:30〜16:30（入園は16:00まで）", "Isuien 9:30–16:30 (last entry 16:00)"),
                    row("closed", "依水園：火曜（祝日なら開園して次の平日が休み）、9月下旬と12月末〜1月中旬の庭園整備期間", "Isuien: Tuesdays (open if a holiday, closed the next weekday); maintenance periods in late September and from late December to mid-January"),
                    row("fee", "依水園 1,200円（寧楽美術館を含む）", "Isuien ¥1,200 (includes the Neiraku Museum)"),
                    row("hours", "吉城園 9:00〜17:00（入園は16:30まで）、無料。2月24日〜28日は休み", "Yoshikien 9:00–17:00 (last entry 16:30), free. Closed 24–28 February")],
                   tip=T("依水園は公式サイト、吉城園は奈良県のページで確認しました。", "Isuien checked on its website; Yoshikien on Nara Prefecture’s page."))),
    dict(id="todaiji", name=T("東大寺 南大門・大仏殿", "Todaiji: Great South Gate & Great Buddha Hall"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
         blurb=T("高さ約15mの大仏さま。大仏殿は中に入った瞬間の大きさがすべてです。南大門の仁王像も見上げてください。",
                 "The Great Buddha, about 15 m tall. The moment you step inside the hall, the scale says it all. Look up at the guardians in the Great South Gate too."),
         lat=34.68899, lng=135.83987,
         text=T("東大寺（とうだいじ）南大門・大仏殿\n\nまず南大門（なんだいもん）。門の左右に、高さ8mを超える木の仁王像が向かい合って立っています。鎌倉時代に運慶・快慶たちが彫ったもの。みんな鹿を見ていて素通りするので、門の中で立ち止まって見上げてください。\n\n"
                "その先の大仏殿（だいぶつでん）は、世界最大級の木造建築です。入口は正面ではなく、左（西）側の回廊の端にあります。中に入ると、正面に大仏さま（盧舎那仏・るしゃなぶつ）。右回りに裏へ回ると、昔の東大寺の模型と、大仏さまの鼻の穴と同じ大きさの穴があいた柱があります（くぐれるのは子どもか細い人）。\n\n"
                "混むのは10時〜15時。朝は7:30（11〜3月は8:00）から開いているので、人の少ない大仏殿を見たいなら、興福寺より先にここへ来る手もあります。大仏殿の中は写真を撮れます（三脚は不可）。\n\n"
                "拝観料は現金だけです。\n\nおすすめ訪問時間：10:25〜11:25",
                "Todaiji: Great South Gate and Great Buddha Hall\n\nFirst the Great South Gate (Nandaimon). Inside it, left and right, two wooden guardian kings over 8 m tall face each other, carved by Unkei, Kaikei and their workshop in the Kamakura period. Most people walk through watching the deer, so stop inside the gate and look up.\n\n"
                "Beyond it, the Great Buddha Hall (Daibutsuden) is one of the largest wooden buildings in the world. The entrance is not in the middle but at the left (west) end of the cloister. Inside, the Great Buddha (Vairocana) sits straight ahead. Walk round clockwise to the back for models of the original temple and the pillar with a hole the size of the Buddha’s nostril (only children and slim adults fit through).\n\n"
                "It’s busiest from 10:00 to 15:00. The hall opens at 7:30 (8:00 from November to March), so for a quieter visit you could come here before Kofukuji. Photos are allowed inside the hall (no tripods).\n\n"
                "Admission is cash only.\n\nRecommended visit time: 10:25–11:25"),
         gmaps=[gm("東大寺 南大門", "Great South Gate", 34.68580, 135.83987, "東大寺 南大門"), gm("東大寺 大仏殿", "Great Buddha Hall", 34.68899, 135.83987, "東大寺 大仏殿")],
         links=[link("official", "東大寺 拝観時間・拝観料", "Todaiji hours and admission", "https://www.todaiji.or.jp/information/haikan/", "https://www.todaiji.or.jp/en/")],
         info=info([row("hours", "大仏殿：4〜10月 7:30〜17:30、11〜3月 8:00〜17:00", "Great Buddha Hall: April–October 7:30–17:30, November–March 8:00–17:00"),
                    row("fee", "大仏殿 800円（小学生400円）。東大寺ミュージアムとのセット券 1,200円。現金のみ", "Great Buddha Hall ¥800 (primary school children ¥400). Combined ticket with the Todaiji Museum ¥1,200. Cash only"),
                    row("closed", "休みなし", "Open daily")],
                   cash=True,
                   tip=T("時間と料金は東大寺の公式サイトで確認しました。お昼を早めに食べたい日は、南大門の手前の「東大寺門前 夢風ひろば」に食事の店が集まっています（店ごとに時間が違います）。写真の1・2枚目は2022年12月。",
                         "Hours and fees checked on Todaiji’s website. For an early lunch, Yumekaze Plaza just before the Great South Gate has a cluster of restaurants (hours differ by shop). The first two photos: December 2022."))),
    dict(id="nigatsudo", name=T("二月堂", "Nigatsudo Hall"), kind=T("お堂・展望（無料）", "Hall & viewpoint (free)"),
         blurb=T("大仏殿の裏の坂を上って10分。舞台から奈良の町と大仏殿の屋根を見下ろせます。無料で、夜も開いています。",
                 "Ten minutes up the slope behind the Great Buddha Hall. From its balcony you look down on Nara and the roof of the Great Buddha Hall. Free, and open at night."),
         lat=34.68927, lng=135.84427,
         text=T("二月堂（にがつどう）\n\n大仏殿で帰ってしまう人が多いのですが、奈良でいちばんの景色はこの先です。大仏殿を出たら右（東）へ。鐘楼の丘を越えるか、大仏殿の裏から土塀の続く石畳の坂（裏参道）を上ると、約10分で崖に張り出したお堂が見えてきます。\n\n"
                "石段を上った舞台からは、大仏殿の大屋根、奈良の町、その向こうに生駒山（いこまやま）。西向きなので、夕方は空と町が赤く染まります。舞台は24時間入れて無料。日が暮れると吊り灯籠に火が入り、昼とは別の場所になります。\n\n"
                "夕日に合わせたい人へ：冬は日の入りが17時前で、大仏殿が閉まる時間とほぼ同じです。順番を逆にして（興福寺→ならまちでお昼→春日大社→大仏殿→二月堂）、最後にここへ来るとちょうど夕暮れ。駅までは歩いて約30分です。\n\n"
                "舞台の北側に、無料の休憩所があります。隣の三月堂（法華堂）は東大寺でいちばん古い建物で、中の仏像を見るなら800円。3月1日〜14日の夜は「お水取り」の松明（たいまつ）で大変混みます。\n\nおすすめ訪問時間：11:35〜12:05",
                "Nigatsudo Hall\n\nMany people turn back at the Great Buddha Hall, but the best view in Nara is further on. Leaving the hall, go right (east). Either cross the bell-tower hill or take the stone-paved lane with earthen walls behind the hall; in about 10 minutes the hall appears, built out over the hillside.\n\n"
                "Climb the stone steps to the balcony: the great roof of the Buddha hall, the town of Nara, and Mt. Ikoma beyond. It faces west, so towards evening the sky and the town turn red. The balcony is open 24 hours and free. After dark the hanging lanterns are lit and it becomes a different place.\n\n"
                "If you want the sunset: in winter the sun sets before 17:00, about when the Great Buddha Hall closes. Reverse the order (Kofukuji → lunch in Naramachi → Kasuga Taisha → Great Buddha Hall → Nigatsudo) and you arrive here at dusk. It’s about 30 minutes’ walk back to the station.\n\n"
                "There is a free rest house on the north side of the balcony. Next door, the Sangatsudo (Hokkedo) is Todaiji’s oldest building; ¥800 to see the statues inside. On the evenings of 1–14 March the Omizutori fire ceremony draws big crowds.\n\nRecommended visit time: 11:35–12:05"),
         gmaps=[gm("二月堂", "Nigatsudo", 34.68927, 135.84427, "東大寺 二月堂")],
         links=[link("official", "東大寺 二月堂", "Todaiji: Nigatsudo (Japanese)", "https://www.todaiji.or.jp/information/nigatsudo/")],
         info=info([row("hours", "二月堂は24時間お参りできます（夜は静かに。三脚は使えません）", "Nigatsudo can be visited 24 hours a day (quietly at night; no tripods)"),
                    row("fee", "二月堂は無料。三月堂（法華堂）は8:30〜16:00・800円", "Nigatsudo is free. Sangatsudo (Hokkedo): 8:30–16:00, ¥800")],
                   tip=T("東大寺の公式サイトで確認しました。休憩所の開いている時間は確認できていません。",
                         "Checked on Todaiji’s website. The opening hours of the rest house could not be confirmed."))),
    dict(id="wakakusa", name=T("若草山", "Mt. Wakakusa"), kind=T("芝生の山・展望", "Grassy hill & view"),
         blurb=T("二月堂から春日大社へ向かう道の途中。芝生の斜面を20分上ると、奈良の町が全部見えます。冬は入れません。",
                 "On the way from Nigatsudo to Kasuga Taisha. Twenty minutes up the grass slope and all of Nara is below you. Closed in winter."),
         caution=T("冬は入山できません（12月第2日曜の翌日〜3月第3土曜の前日）", "Closed in winter (from the day after the 2nd Sunday of December to the day before the 3rd Saturday of March)"),
         lat=34.68930, lng=135.84920,
         text=T("若草山（わかくさやま）\n\n全体が芝生の、標高342mの山です。二月堂から手向山八幡宮（たむけやまはちまんぐう）の前を通って歩くと5分でふもとの北ゲート。入山料を払って芝生の斜面を上ります。\n\n"
                "最初の高まり（一重目）まで約20分。ここで奈良の町と大仏殿の屋根が見渡せるので、時間がなければここで引き返して十分です。山頂（三重目）までは片道40分ほど。上にも鹿がいます。\n\n"
                "日かげがなく、夏は暑いです。飲み物を持って。ゲートは北と南の2つがあり、約300m離れています。下りは南ゲートから出ると春日大社に近いです。\n\n"
                "入れるのは3月の第3土曜から12月の第2日曜まで（2026年は12月13日まで）。毎年1月の第4土曜には、山全体を焼く「若草山焼き」があります。\n\nおすすめ訪問時間：12:10〜12:55（ここに寄る日は、この先を45分ずつ遅らせます）",
                "Mt. Wakakusa\n\nA 342 m hill covered entirely in grass. From Nigatsudo, walk past Tamukeyama Hachimangu shrine and you reach the North Gate at its foot in 5 minutes. Pay the small fee and climb the grass slope.\n\n"
                "It takes about 20 minutes to the first shoulder. From there you already look over the town and the roof of the Great Buddha Hall, so turning back here is fine if time is short. The summit is about 40 minutes each way. There are deer up here too.\n\n"
                "There is no shade and it’s hot in summer; carry a drink. There are two gates, North and South, about 300 m apart. Leaving by the South Gate puts you closer to Kasuga Taisha.\n\n"
                "The hill is open from the third Saturday of March to the second Sunday of December (until 13 December in 2026). On the fourth Saturday of January the whole hillside is burned in the Wakakusa Yamayaki.\n\nRecommended visit time: 12:10–12:55 (if you climb, shift everything after by 45 minutes)"),
         gmaps=[gm("若草山 北ゲート", "Mt. Wakakusa North Gate", 34.68930, 135.84920, "若草山 北ゲート")],
         links=[link("official", "若草山（奈良公園クイックガイド）", "Mt. Wakakusa (Nara Park Quick Guide, Japanese)", "https://www.pref.nara.lg.jp/site/park/2585.html")],
         notices=[{"from": "2026-12-14", "to": "2027-03-19", "head": T("冬は入山できません", "Closed for winter"),
                   "text": T("若草山は3月の第3土曜（2027年は3月20日）まで入れません。ふもとから見上げるだけになります。", "Mt. Wakakusa is closed until the third Saturday of March (20 March 2027). You can only look up at it from the foot.")}],
         info=info([row("hours", "3月第3土曜〜12月第2日曜の9:00〜17:00（2026年は12月13日まで）", "Third Saturday of March to second Sunday of December, 9:00–17:00 (until 13 December in 2026)"),
                    row("fee", "150円（3歳〜小学生80円）", "¥150 (¥80 for ages 3 to primary school)")],
                   cash=True,
                   tip=T("奈良県の「奈良公園クイックガイド」で確認しました。上る時間は目安です。", "Checked on Nara Prefecture’s Nara Park Quick Guide. Climbing times are rough guides."))),
    dict(id="kasuga", name=T("春日大社", "Kasuga Taisha Shrine"), kind=T("神社（世界遺産）", "Shrine (World Heritage)"),
         blurb=T("森の中の朱色の社殿と、約3,000基の灯籠。参道の石灯籠のあいだから鹿が顔を出します。",
                 "Vermilion halls in the forest and some 3,000 lanterns. Deer look out from between the stone lanterns along the approach."),
         lat=34.68149, lng=135.84800,
         text=T("春日大社（かすがたいしゃ）\n\n二月堂からは、手向山八幡宮の前を通り、若草山のふもとのみやげ物屋の並ぶ道を南へ。歩いて約15分で、森の中の朱色の回廊に着きます。\n\n"
                "お参りだけなら無料で、幣殿（へいでん）の前まで入れます。その奥の「御本殿特別参拝」（700円）に入ると、朱色の回廊にずらりと下がる釣灯籠と、暗い部屋で灯籠に火を入れた様子を再現した「藤浪之屋（ふじなみのや）」が見られます。灯籠を見に来たなら、ここは入る価値があります。\n\n"
                "帰りは、二之鳥居から石灯籠の並ぶ参道をまっすぐ西へ。苔のついた灯籠のあいだに鹿が立っていて、写真を撮るならこの道です。途中の「春日荷茶屋（かすがにないぢゃや）」は春日大社の茶屋で、季節の野菜が入る万葉粥（まんようがゆ）が名物。ならまちまでお昼を待てないときに。\n\n"
                "ならまちへは、参道を下って一之鳥居の手前から南西へ、歩いて約25分です。\n\nおすすめ訪問時間：12:30〜13:15",
                "Kasuga Taisha Shrine\n\nFrom Nigatsudo, pass Tamukeyama Hachimangu and walk south along the lane of souvenir shops at the foot of Mt. Wakakusa. In about 15 minutes you reach the vermilion cloisters in the forest.\n\n"
                "Praying is free and takes you as far as the offering hall. Beyond it, the paid inner area (¥700) has the cloisters hung with rows of bronze lanterns and the Fujinami-no-ya, a dark room where lit lanterns recreate the lantern festival. If the lanterns are what you came for, it’s worth paying.\n\n"
                "Leave by the second torii and walk straight west down the approach lined with stone lanterns. Deer stand between the mossy lanterns; this is the path for photos. On the way, Kasuga Ninaijaya is the shrine’s own teahouse, known for Man’yo-gayu, rice porridge with seasonal vegetables: handy if you can’t wait for lunch in Naramachi.\n\n"
                "For Naramachi, go down the approach and head south-west before the first torii: about 25 minutes on foot.\n\nRecommended visit time: 12:30–13:15"),
         gmaps=[gm("春日大社", "Kasuga Taisha", 34.68149, 135.84800, "春日大社 本殿"), gm("春日荷茶屋", "Kasuga Ninaijaya teahouse", 34.68231, 135.84338, "春日荷茶屋")],
         links=[link("official", "春日大社 参拝案内", "Kasuga Taisha visitor information", "https://www.kasugataisha.or.jp/about/basic/", "https://www.kasugataisha.or.jp/en/"),
                link("official", "春日荷茶屋", "Kasuga Ninaijaya teahouse (Japanese)", "https://www.kasugataisha.or.jp/ninaijyaya/")],
         info=info([row("hours", "お参り：3〜10月 6:30〜17:30、11〜2月 7:00〜17:00", "Shrine: March–October 6:30–17:30, November–February 7:00–17:00"),
                    row("hours", "御本殿特別参拝 9:00〜16:00（祭事で入れない日・時間があります）", "Inner area (special visit) 9:00–16:00 (closed at times for ceremonies)"),
                    row("fee", "お参りは無料。御本殿特別参拝 700円、国宝殿 700円", "Praying is free. Inner area ¥700; Kasuga Taisha Museum ¥700"),
                    row("hours", "春日荷茶屋 10:30〜16:30（ラストオーダー16:00）、休みは不定（月ごとに公式サイトに掲載）。万葉粥 1,200円", "Kasuga Ninaijaya 10:30–16:30 (last orders 16:00); irregular closing days, listed monthly on the website. Man’yo-gayu ¥1,200")],
                   tip=T("春日大社の公式サイトで確認しました。4枚目の鳥居の写真は2022年12月。", "Checked on Kasuga Taisha’s website. The fourth photo (the torii): December 2022."))),
    dict(id="naramachi", name=T("ならまち", "Naramachi"), kind=T("古い町並み・お昼", "Old town & lunch"),
         blurb=T("格子の町家が残る、元興寺のまわりの古い町。遅めのお昼と、酒蔵「春鹿」のきき酒はここで。",
                 "The old quarter around Gangoji, with its latticed townhouses. Come here for a late lunch and a sake tasting at the Harushika brewery."),
         lat=34.67763, lng=135.83121,
         text=T("ならまち\n\n猿沢池の南に広がる、江戸〜明治の町家が残る一帯です。もとは全部、元興寺（がんごうじ）というお寺の境内でした。道は細く、車も少なく、公園側とは空気が違います。\n\n"
                "お昼：町家を使ったカフェや食事の店が、元興寺の北と西の通りに集まっています。この順番だと着くのは13時半を過ぎるので、ランチが14時ごろで終わる店に注意。月曜と火曜は休む店が多めです。確実に食べたいなら、駅前のアーケード（東向商店街・もちいどのセンター街）は通しで開いている店が多いです。\n\n"
                "見る所：\n・ならまち格子の家：昔の町家を再現した建物で、中まで無料で入れます。奥に細長い造りがよくわかります。\n・元興寺：世界遺産。屋根の一部に、1400年前の飛鳥時代の瓦が今も使われています。\n・今西清兵衛商店（いまにしせいべえしょうてん）：日本酒「春鹿（はるしか）」の蔵元。700円で5種類のきき酒ができます。私は2022年12月にここで飲みました。3〜5枚目の写真がそのときのものです。\n\n"
                "軒先に下がっている赤い布のぬいぐるみは「身代わり申（さる）」。庚申（こうしん）さんの魔よけです。\n\n"
                "帰りは、もちいどのセンター街のアーケードを北へ抜けて近鉄奈良駅まで歩いて約15分。三条通の角の中谷堂（なかたにどう）では、つきたてのよもぎ餅を売っています。\n\nおすすめ訪問時間：13:45〜15:30",
                "Naramachi\n\nThe quarter south of Sarusawa Pond, where townhouses from the Edo and Meiji periods survive. All of it was once the precinct of one temple, Gangoji. The lanes are narrow, there are few cars, and the mood is quite different from the park side.\n\n"
                "Lunch: cafés and restaurants in old townhouses are clustered on the streets north and west of Gangoji. On this route you arrive after 13:30, so watch out for places whose lunch ends around 14:00. Quite a few close on Mondays and Tuesdays. For a safe bet, the covered arcades by the station (Higashimuki and Mochiidono) have many places open right through the afternoon.\n\n"
                "What to see:\n• Naramachi Koshi-no-Ie: a reconstructed townhouse you can walk right through, free. You see how long and narrow these houses are.\n• Gangoji: a World Heritage temple. Part of its roof still carries tiles from the Asuka period, 1,400 years old.\n• Imanishi Seibei Shoten: the brewery of Harushika sake. ¥700 for a tasting of five kinds. I drank here in December 2022; photos 3–5 are from that day.\n\n"
                "The red cloth charms hanging under the eaves are “migawari-zaru”, monkey charms of the Koshin faith that take bad luck in your place.\n\n"
                "To go back, walk north through the Mochiidono arcade to Kintetsu-Nara Station, about 15 minutes. Nakatanidou, on the corner of Sanjo-dori, sells freshly pounded mugwort rice cakes.\n\nRecommended visit time: 13:45–15:30"),
         gmaps=[gm("元興寺", "Gangoji", 34.67763, 135.83121, "元興寺 奈良"), gm("ならまち格子の家", "Naramachi Koshi-no-Ie", 34.67502, 135.83067, "ならまち格子の家"),
                gm("今西清兵衛商店（春鹿）", "Imanishi Seibei Shoten (Harushika)", 34.67720, 135.83440, "今西清兵衛商店 春鹿"), gm("中谷堂", "Nakatanidou", 34.68193, 135.82886, "中谷堂 奈良")],
         links=[link("official", "春鹿 蔵元見学・きき酒", "Harushika brewery tasting (Japanese)", "https://www.harushika.com/visit-brewery/"),
                link("official", "元興寺", "Gangoji (Japanese)", "https://gangoji-tera.or.jp/about/"),
                link("official", "ならまち格子の家（奈良市）", "Naramachi Koshi-no-Ie (Nara City, Japanese)", "https://www.city.nara.lg.jp/site/shisetsu/6242.html"),
                link("official", "中谷堂", "Nakatanidou (Japanese)", "https://nakatanidou.jp/shop")],
         info=info([row("hours", "春鹿のきき酒：受付10:00〜16:30、700円で5種類。火曜休み（祝日なら翌日）、お盆と年末年始も休み", "Harushika tasting: reception 10:00–16:30, ¥700 for five kinds. Closed Tuesdays (next day if a holiday), mid-August and New Year"),
                    row("hours", "元興寺 9:00〜17:00（入門は16:30まで）、700円", "Gangoji 9:00–17:00 (last entry 16:30), ¥700"),
                    row("hours", "ならまち格子の家 9:00〜17:00、無料。月曜休み（祝日なら翌日）、祝日の翌日、12月26日〜1月5日も休み", "Naramachi Koshi-no-Ie 9:00–17:00, free. Closed Mondays (next day if a holiday), the day after a holiday, and 26 December – 5 January"),
                    row("hours", "中谷堂 10:00〜19:00（売り切れで早じまいあり）。よもぎ餅3個600円", "Nakatanidou 10:00–19:00 (may close early when sold out). Mugwort rice cakes ¥600 for three")],
                   tip=T("それぞれの公式サイト（格子の家は奈良市）で確認しました。中谷堂の休みは決まっていません（お店のSNSで告知）。写真の3〜5枚目は2022年12月。",
                         "Checked on each official website (Koshi-no-Ie on Nara City’s page). Nakatanidou has no fixed closing day (announced on its social media). Photos 3–5: December 2022."))),
    dict(id="heijo", name=T("平城宮跡", "Heijo Palace Site"), kind=T("都の跡（世界遺産）・寄り道", "Palace site (World Heritage), side trip"),
         blurb=T("1300年前の都の中心。広い野原に朱雀門と大極殿が復元されています。帰りの電車で途中下車して寄れます。無料。",
                 "The heart of the capital 1,300 years ago. On a wide open field, the Suzaku Gate and the Great Audience Hall have been rebuilt. Stop off on the train home. Free."),
         lat=34.69393, lng=135.79424,
         text=T("平城宮跡（へいじょうきゅうせき）\n\n奈良時代の都・平城京の宮殿があった場所です。建物はほとんど残っていませんが、1km四方の野原に、正門の朱雀門（すざくもん）と、天皇の儀式の場だった第一次大極殿（だいごくでん）が実物大で復元されています。敷地の中を近鉄電車が横切って走ります。\n\n"
                "行き方：帰り道の途中です。近鉄奈良から2駅目の大和西大寺駅で降り、南口から歩いて約20分で大極殿。見たあと朱雀門まで南へ歩いて約15分、そこから大和西大寺駅へ戻るか、バスで近鉄奈良駅・JR奈良駅へ。京都行きの特急・急行は大和西大寺に止まります。\n\n"
                "正直なところ：大極殿と朱雀門は16:30で閉まります（入場は16:00まで）。ならまちまで全部歩いた日には間に合いません。寄りたい日は、ならまちを短くするか、どこかを1つ外してください。建物の中に入らず、夕方の野原を歩くだけなら何時でも大丈夫です。\n\nおすすめ訪問時間：15:00〜16:20（ならまちを14:30に出る場合）",
                "Heijo Palace Site\n\nThis is where the palace of Heijo-kyo, the Nara-period capital, stood. Almost nothing original remains above ground, but on a field a kilometre square the main Suzaku Gate and the Former Great Audience Hall (Daigokuden), where the emperor held state ceremonies, have been rebuilt at full size. Kintetsu trains run right across the site.\n\n"
                "Getting there: it’s on your way home. Get off at Yamato-Saidaiji, two stops from Kintetsu-Nara, and walk about 20 minutes from the south exit to the Daigokuden. Then walk about 15 minutes south to the Suzaku Gate, and either return to Yamato-Saidaiji or take a bus to Kintetsu-Nara or JR Nara. Limited expresses and expresses for Kyoto stop at Yamato-Saidaiji.\n\n"
                "To be honest: the Daigokuden and the Suzaku Gate close at 16:30 (last entry 16:00). After walking the whole route to Naramachi you won’t make it. If you want this, cut Naramachi short or drop one stop. Just walking the open field in the evening light, without going inside, works at any hour.\n\nRecommended visit time: 15:00–16:20 (leaving Naramachi at 14:30)"),
         gmaps=[gm("第一次大極殿", "Former Great Audience Hall", 34.69393, 135.79424, "平城宮跡 第一次大極殿"), gm("朱雀門", "Suzaku Gate", 34.68693, 135.79428, "平城宮跡 朱雀門"),
                gm("大和西大寺駅", "Yamato-Saidaiji Station", 34.69380, 135.78268, "大和西大寺駅")],
         links=[link("official", "平城宮跡歴史公園 施設情報", "Heijo Palace Site Historical Park: facilities (Japanese)", "https://www.heijo-park.jp/information/facility/"),
                link("official", "平城宮跡歴史公園 アクセス", "Heijo Palace Site Historical Park: access (Japanese)", "https://www.heijo-park.jp/information/access/")],
         info=info([row("hours", "第一次大極殿・朱雀門 9:00〜16:30（入場は16:00まで）。平城宮いざない館 9:00〜17:00（入館は16:30まで）", "Daigokuden and Suzaku Gate 9:00–16:30 (last entry 16:00). Heijo Palace Izanai-kan 9:00–17:00 (last entry 16:30)"),
                    row("closed", "大極殿・朱雀門：月曜（祝日なら次の平日）、12月29日〜1月3日。いざない館：2・4・7・11月の第2月曜、12月29日〜1月1日", "Daigokuden and Suzaku Gate: Mondays (next weekday if a holiday), 29 Dec – 3 Jan. Izanai-kan: 2nd Monday of Feb, Apr, Jul and Nov; 29 Dec – 1 Jan"),
                    row("fee", "無料", "Free"),
                    row("train", "近鉄奈良 → 大和西大寺 約6分（急行・快速急行）。南口から大極殿・朱雀門ひろばへ歩いて約20分", "Kintetsu-Nara → Yamato-Saidaiji about 6 min (express or rapid express). About 20 min on foot from the south exit to the Daigokuden or Suzaku Gate Square"),
                    row("bus", "朱雀門ひろば前 → 近鉄奈良駅 約16分、JR奈良駅西口 約10分（奈良交通バス。運賃は要確認）", "Suzakumon Hiroba-mae → Kintetsu-Nara Station about 16 min, JR Nara Station west exit about 10 min (Nara Kotsu bus; fare: please check)")],
                   tip=T("平城宮跡歴史公園の公式サイトと乗換案内で確認しました。", "Checked on the Heijo Palace Site Historical Park website and a route planner."))),
    dict(id="horyuji", name=T("法隆寺", "Horyuji Temple"), kind=T("寺（世界遺産）・別に半日", "Temple (World Heritage), needs half a day"),
         blurb=T("世界でいちばん古い木造建築。奈良公園から電車と徒歩で約50分かかるので、同じ日に入れるなら何かを外します。",
                 "The oldest wooden buildings in the world. It’s about 50 minutes from Nara Park by train and on foot, so fitting it into the same day means dropping something."),
         caution=T("奈良公園と同じ日に全部は回れません", "Doesn’t fit with the whole Nara Park route in one day"),
         lat=34.61470, lng=135.73420,
         text=T("法隆寺（ほうりゅうじ）\n\n聖徳太子が建てたお寺で、金堂と五重塔は7世紀のもの。世界でいちばん古い木造建築です。興福寺の五重塔が見られない今、五重塔を見たい人にはここをすすめます。\n\n"
                "正直なところ：奈良公園のルートを全部歩いた日に法隆寺まで行くのは無理があります。JR奈良駅から大和路快速で11分、法隆寺駅から歩いて約20分（バスなら約8分）。近鉄奈良駅からJR奈良駅までも歩いて15分あり、片道で約50分みてください。中を見るのに1時間半はかかります。\n\n"
                "同じ日に入れるなら、午前は興福寺・東大寺・二月堂までにして、お昼を食べたら13時ごろJR奈良駅へ。13:45ごろの電車で14:30に法隆寺に着けば、閉門までゆっくり見られます。11月4日〜2月21日は16:30で閉まり、受付はその30分前までなので注意。帰りは法隆寺駅から奈良で乗り換えて京都へ、またはJRで大阪方面へも出られます。\n\n"
                "拝観券は西院伽藍（金堂・五重塔）、大宝蔵院（百済観音・玉虫厨子）、東院伽藍（夢殿）の共通で、現金のみです。\n\nおすすめ訪問時間：14:30〜16:15",
                "Horyuji Temple\n\nFounded by Prince Shotoku; its Golden Hall and five-storied pagoda date from the 7th century and are the oldest wooden buildings in the world. With Kofukuji’s pagoda hidden for now, this is where I’d send anyone who wants to see a five-storied pagoda.\n\n"
                "To be honest: going on to Horyuji after walking the whole Nara Park route is too much. It’s 11 minutes from JR Nara by Yamatoji Rapid, then about 20 minutes on foot from Horyuji Station (about 8 minutes by bus). Kintetsu-Nara to JR Nara is another 15 minutes’ walk, so allow about 50 minutes each way, and at least an hour and a half inside.\n\n"
                "To fit it into the same day, keep the morning to Kofukuji, Todaiji and Nigatsudo, have lunch, and head for JR Nara around 13:00. A train around 13:45 gets you to the temple by 14:30, with unhurried time until closing. From 4 November to 21 February it closes at 16:30, and tickets stop 30 minutes before. Afterwards, return via Nara to Kyoto, or continue by JR towards Osaka.\n\n"
                "One ticket covers the Western Precinct (Golden Hall and pagoda), the Gallery of Temple Treasures (Kudara Kannon, Tamamushi Shrine) and the Eastern Precinct (Hall of Dreams). Cash only.\n\nRecommended visit time: 14:30–16:15"),
         gmaps=[gm("法隆寺", "Horyuji", 34.61470, 135.73420, "法隆寺"), gm("JR法隆寺駅", "JR Horyuji Station", 34.60180, 135.73967, "JR法隆寺駅"),
                gm("JR奈良駅", "JR Nara Station", 34.68088, 135.81993, "JR奈良駅")],
         links=[link("official", "法隆寺 拝観案内", "Horyuji visitor information (Japanese)", "https://www.horyuji.or.jp/annai/"), JR],
         info=info([row("hours", "2月22日〜11月3日 8:00〜17:00、11月4日〜2月21日 8:00〜16:30（受付は30分前まで）", "22 Feb – 3 Nov 8:00–17:00; 4 Nov – 21 Feb 8:00–16:30 (tickets until 30 minutes before closing)"),
                    row("fee", "2,000円（中学生1,700円、小学生1,000円）。西院伽藍・大宝蔵院・東院伽藍の共通。現金のみ", "¥2,000 (junior high ¥1,700, primary ¥1,000) for the Western Precinct, Gallery of Temple Treasures and Eastern Precinct. Cash only"),
                    row("train", "JR奈良 → 法隆寺 大和路快速で11分・240円（日中は約15分おき）", "JR Nara → Horyuji 11 min by Yamatoji Rapid, ¥240 (about every 15 minutes in the daytime)"),
                    row("bus", "法隆寺駅 南口 → 法隆寺参道 約8分（奈良交通バス72番。運賃は要確認）。歩くと約20分", "Horyuji Station south exit → Horyuji Sando about 8 min (Nara Kotsu bus 72; fare: please check). About 20 min on foot")],
                   cash=True,
                   tip=T("時間と料金は法隆寺の公式サイト（2025年3月改定）、電車は乗換案内、バスの時間は斑鳩町のページで確認しました。",
                         "Hours and fees checked on Horyuji’s website (revised March 2025); trains on a route planner; bus time on Ikaruga Town’s page."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = PHOTOS[out["id"]]
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
PARK = [NO[k] for k in ("isuien", "todaiji", "nigatsudo", "wakakusa", "kasuga")]
data = {
    "id": "nara",
    "_note": "京都から日帰り 奈良のルート（nara/ のページ専用。形は eizan-line.json と同じ）。近鉄奈良駅→興福寺→奈良公園の鹿→（依水園・吉城園）→東大寺 南大門・大仏殿→二月堂→（若草山）→春日大社→ならまち。寄り道として平城宮跡と法隆寺。"
             "Toshi の写真は2022年12月28日（東大寺・鹿・春日大社・ならまちの春鹿・猿沢池）と2021〜2022年の駅の写真。手持ちが少ないので、ほかは Wikimedia Commons の写真（写真の上に撮影者とライセンスを表示）。"
             "info.checked は事実情報を確認した日（各施設の公式サイト・奈良県・奈良市、電車は乗換案内）。このファイルは scripts/build_nara_data.py で作る。",
    "sections": [{"first": NO["eki"], "last": NO["shika"], "day": 0}, {"first": NO["isuien"], "last": NO["wakakusa"], "day": 1},
                 {"first": NO["kasuga"], "last": NO["kasuga"], "day": 2}, {"first": NO["naramachi"], "last": NO["naramachi"], "day": 3},
                 {"first": NO["heijo"], "last": NO["horyuji"], "area": T("寄り道", "Side trips"), "title": T("時間をつくって足をのばす", "If you make the time")}],
    "focus": {"first": NO["eki"], "last": NO["naramachi"]},
    "plan": {"_note": "「選んで回る」の設定。近鉄奈良駅は必ず入る。奈良公園の鹿は、公園側の場所をどれか選ぶと入る。defaultMode: pick で最初から「選んで回る」、"
                      "defaultPicks は初めて開いたときに選んである定番の場所（scripts/sync_nara.py の差分）。",
             "defaultMode": "pick",
             "picks": [NO[k] for k in ("kofukuji", "isuien", "todaiji", "nigatsudo", "wakakusa", "kasuga", "naramachi", "heijo", "horyuji")],
             "defaultPicks": [NO[k] for k in ("kofukuji", "todaiji", "nigatsudo", "kasuga", "naramachi")],
             "auto": {str(NO["eki"]): {"always": True}, str(NO["shika"]): {"any": PARK}},
             "hints": [
                 H("horyuji", {"any": [NO["horyuji"]], "andAny": [NO["kasuga"], NO["naramachi"], NO["wakakusa"], NO["heijo"]]},
                   "法隆寺と、春日大社やならまちまでを同じ日に回るのは時間が足りません。午前を東大寺・二月堂までにして、13時ごろJR奈良駅へ向かうのが現実的です。",
                   "Horyuji plus Kasuga Taisha or Naramachi is too much for one day. Keep the morning to Todaiji and Nigatsudo and head for JR Nara around 13:00."),
                 H("heijo", {"any": [NO["heijo"]], "andAny": [NO["naramachi"]]},
                   "大極殿と朱雀門は16:00までに入ります。ならまちを14:30ごろに出て、近鉄奈良から大和西大寺へ。",
                   "Enter the Daigokuden and Suzaku Gate by 16:00: leave Naramachi around 14:30 and take Kintetsu to Yamato-Saidaiji."),
                 H("kasuga", {"any": [NO["kasuga"]], "none": [NO["todaiji"], NO["nigatsudo"], NO["wakakusa"]]},
                   "東大寺に寄らない日は、興福寺から三条通をまっすぐ東へ。一之鳥居から参道を歩いて約25分です。",
                   "Skipping Todaiji? From Kofukuji walk straight east along Sanjo-dori; from the first torii it’s about 25 minutes up the approach."),
                 H("naramachi", {"any": [NO["naramachi"]], "none": [NO["kasuga"], NO["wakakusa"]]},
                   "春日大社に寄らない日は、二月堂や大仏殿から興福寺・猿沢池へ戻って南へ。お昼に間に合う時間に着けます。",
                   "Skipping Kasuga Taisha? Walk back from Nigatsudo or the Great Buddha Hall past Kofukuji and Sarusawa Pond; you’ll reach Naramachi in good time for lunch."),
             ]},
    "photoBase": "../images/nara/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
