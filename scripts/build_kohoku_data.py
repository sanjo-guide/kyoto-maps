#!/usr/bin/env python3
"""京都から日帰り 海津大崎の桜と長浜のデータ（data/routes/kohoku.json）を書き出す。

使い方: python3 scripts/build_higashiomi_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/kohoku/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/kohoku"
OUT = f"{R}/data/routes/kohoku.json"
CHECKED = "2026-11-20"
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


def photos(pid):
    return [f"{pid}-{i}.jpg" for i in sorted(PICKS[pid])]




JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
SAKURA = link("official", "海津大崎の桜（びわ湖高島観光協会）", "Kaizu-Osaki cherry blossoms (Takashima tourism, Japanese)", "https://takashima-kanko.jp/sakura/")
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。春はダイヤが変わっていることがあるので、行く前に確かめてください。",
              "Times and fares checked on a route planner (Saturday timetable, November 2026). Timetables may change by spring, so check before you go.")
SEASON = {"from": None, "to": None, "url": "https://takashima-kanko.jp/sakura/",
          "head": T("桜の見ごろは4月上旬〜中旬", "Cherry blossoms: early to mid April"),
          "text": T("海津大崎の桜は、例年4月はじめに咲きはじめ、5〜6日で満開になります（京都市内より1週間ほど遅め）。見ごろの土日は、湖岸の道で交通規制があります。",
                    "The Kaizu-Osaki cherries usually open in early April and are in full bloom 5–6 days later, about a week after Kyoto city. On peak weekends the lakeside road has traffic restrictions.")}

S = [
    dict(id="makino", name=T("マキノ駅・マキノサニービーチ（知内浜）", "Makino Station & Makino Sunny Beach"), kind=T("駅・浜辺", "Station & beach"),
         blurb=T("湖西線のマキノ駅から湖へ。白い砂浜と松並木の浜辺に、桜が咲きます。",
                 "From Makino Station on the Kosei Line down to the lake: a white-sand beach lined with pines, and cherries in bloom."),
         lat=35.45351, lng=136.06021,
         text=T("マキノ駅とマキノサニービーチ（知内浜・ちないはま）\n\n京都からJR湖西線で、近江今津で乗り換えてマキノへ。京都7:00発に乗ると、マキノに8:12に着きます（1,170円）。新快速なら乗り換えなしで約1時間15分です。\n\n"
                "駅から湖の方へ歩いて約20分で、白砂青松百選のマキノサニービーチ。浜辺の桜の向こうに、これから歩く海津大崎の山並みが見えます。\n\n"
                "駅の観光案内所ではレンタサイクルも借りられます（1日1,000円〜、台数に限りあり）。海津大崎の桜並木まで、自転車なら30分ほどです。\n\nおすすめ訪問時間：8:30〜9:00",
                "Makino Station and Makino Sunny Beach (Chinai beach)\n\nFrom Kyoto take the JR Kosei Line, changing at Omi-Imazu: leave at 7:00 and reach Makino at 8:12 (¥1,170). A direct Special Rapid takes about 1 h 15 min.\n\n"
                "Walk about 20 minutes towards the lake to Makino Sunny Beach, one of Japan’s 100 best white-sand-and-pine shores. Beyond the cherries on the beach rise the hills of Kaizu-Osaki, where you’re heading.\n\n"
                "The tourist information office in the station rents bicycles (from ¥1,000 a day, limited numbers). It’s about 30 minutes by bike to the cherry avenue.\n\nRecommended visit time: 8:30–9:00"),
         gmaps=[gm("マキノサニービーチ", "Makino Sunny Beach", 35.45351, 136.06021, "マキノサニービーチ"), gm("JRマキノ駅", "JR Makino Station", 35.46121, 136.06009, "JRマキノ駅")],
         links=[SAKURA, link("official", "びわ湖高島レンタサイクル", "Takashima rental bicycles (Japanese)", "https://takashima-kanko.jp/guide/rentalcycle.html"), JR],
         notices=[SEASON],
         info=info([row("train", "京都7:00発 → 近江今津で乗り換え → マキノ8:12着（新快速なら京都8:15発→マキノ9:30着、乗り換えなし）", "Kyoto 7:00 → change at Omi-Imazu → Makino 8:12 (or Special Rapid Kyoto 8:15 → Makino 9:30, direct)"),
                    row("fee", "京都→マキノ 1,170円。レンタサイクル 1日1,000円（電動は2,000円）", "Kyoto → Makino ¥1,170. Rental bike ¥1,000 a day (e-bike ¥2,000)")],
                   tip=TRAIN_TIP)),
    dict(id="kaizu", name=T("海津の石積み", "Kaizu stone embankment"), kind=T("町並み", "Old lakeside village"),
         blurb=T("湖の波から家を守るために積まれた、江戸時代の石垣が続く湖岸の集落。",
                 "A lakeside village behind an Edo-period stone wall built to keep the waves off the houses."),
         lat=35.46400, lng=136.07890,
         text=T("海津（かいづ）の石積み\n\n湖北から敦賀へ向かう道の港町として栄えた海津には、江戸時代に波から家を守るために積まれた石垣が、湖岸に約1.2km残っています。"
                "「海津・西浜・知内の水辺景観」として、国の重要文化的景観に選ばれています。\n\n"
                "古いお寺や町家が並ぶ通りを歩いて、桜並木の入口へ向かいましょう。\n\nおすすめ訪問時間：9:15〜9:45",
                "Kaizu stone embankment\n\nKaizu prospered as a lake port on the road north to Tsuruga. About 1.2 km of the stone wall built in the Edo period to protect the houses from the waves still lines the shore. "
                "The waterside landscape of Kaizu, Nishihama and Chinai is a nationally designated Important Cultural Landscape.\n\n"
                "Stroll the street of old temples and townhouses towards the start of the cherry avenue.\n\nRecommended visit time: 9:15–9:45"),
         gmaps=[gm("海津の石積み", "Kaizu stone embankment", 35.46400, 136.07890, "海津の石積み 高島市")],
         links=[link("official", "海津の石積み（びわ湖高島観光協会）", "Kaizu stone embankment (Takashima tourism, Japanese)", "https://takashima-kanko.jp/spot/2018/06/post_170.html")],
         info=info([row("hours", "マキノ駅から歩いて約20分", "About 20 min on foot from Makino Station")],
                   tip=T("びわ湖高島観光協会のサイトで確認しました。", "Checked on the Takashima tourism association website."))),
    dict(id="sakura", name=T("海津大崎の桜並木", "Kaizu-Osaki cherry avenue"), kind=T("桜並木", "Cherry avenue"),
         blurb=T("湖岸の道に約4km、ソメイヨシノが約800本。湖に枝を伸ばす桜のトンネルを歩きます。",
                 "About 800 cherry trees along 4 km of lakeshore road, branches reaching out over the water."),
         lat=35.45414, lng=136.08334,
         text=T("海津大崎（かいづおおさき）の桜並木\n\n日本さくら名所100選のひとつ。湖岸に沿って約4km、ソメイヨシノ約800本が続きます。"
                "湖に張り出すように咲く桜と、その向こうの竹生島や湖北の山並みは、ここだけの景色です。\n\n"
                "並木口から大崎寺までは約2km、歩いて約30分。写真を撮りながらだと1時間はみておきましょう。見ごろの土日は交通規制があり、道は歩く人でにぎわいます。\n\nおすすめ訪問時間：9:50〜10:50",
                "Kaizu-Osaki cherry avenue\n\nOne of Japan’s 100 best cherry-blossom spots: about 800 Somei-Yoshino trees along some 4 km of the lakeshore. "
                "Cherries leaning out over the water, with Chikubu Island and the northern hills beyond, make a view found nowhere else.\n\n"
                "From the avenue’s entrance to Osakiji temple is about 2 km, around 30 minutes on foot; allow an hour with photo stops. On peak weekends there are traffic restrictions and the road is busy with walkers.\n\nRecommended visit time: 9:50–10:50"),
         gmaps=[gm("海津大崎", "Kaizu-Osaki", 35.45414, 136.08334, "海津大崎 桜")],
         links=[SAKURA, link("official", "交通規制の案内（2026年）", "Traffic restrictions (2026, Japanese)", "https://takashima-kanko.jp/sakura/regulation.html")],
         notices=[SEASON],
         info=info([row("hours", "並木口から大崎寺まで約2km・歩いて約30分（マキノ駅からは約4km・約60分）", "About 2 km / 30 min on foot from the avenue entrance to Osakiji (about 4 km / 60 min from Makino Station)")],
                   tip=T("びわ湖高島観光協会のサイトで確認しました。", "Checked on the Takashima tourism association website."))),
    dict(id="osakiji", name=T("大崎寺・海津大崎港", "Osakiji Temple & Kaizu-Osaki pier"), kind=T("寺・船着き場", "Temple & pier"),
         blurb=T("桜並木の先の、湖に突き出た岬のお寺。桜の時期は、長浜や今津からの桜クルーズの船が着きます。",
                 "A temple on the headland at the end of the avenue. In season, cherry cruises from Nagahama and Imazu call at the pier."),
         lat=35.45021, lng=136.08711,
         text=T("大崎寺（おおさきじ）と海津大崎港\n\n「大崎観音」と呼ばれる、奈良時代に開かれたと伝わるお寺です。県道の第一トンネルの手前の石段を上ると、本堂の前の展望台から琵琶湖が見渡せます。\n\n"
                "桜の時期には、琵琶湖汽船（長浜港・今津港発着）などの「桜クルーズ」の船がここに寄ります。2026年は4月15日まで運航しました。次の春の運航は、各社の発表を確かめてください。\n\n"
                "帰りは、海津1区のバス停まで歩いて約30分、コミュニティバスでマキノ駅へ（約6分・220円）。\n\nおすすめ訪問時間：10:50〜11:10",
                "Osakiji Temple and Kaizu-Osaki pier\n\nKnown as “Osaki Kannon”, said to have been founded in the Nara period. Climb the steps just before the first road tunnel; from the terrace in front of the main hall you look out over Lake Biwa.\n\n"
                "In cherry season, Biwako Kisen and other “cherry cruises” (from Nagahama and Imazu ports) call here; in 2026 they ran until 15 April. Check the operators’ announcements for next spring.\n\n"
                "To go back, walk about 30 minutes to the Kaizu 1-ku bus stop and take the community bus to Makino Station (about 6 min, ¥220).\n\nRecommended visit time: 10:50–11:10"),
         gmaps=[gm("大崎寺", "Osakiji", 35.45021, 136.08711, "大崎寺 高島市マキノ町海津")],
         links=[link("official", "大崎寺（びわ湖高島観光協会）", "Osakiji (Takashima tourism, Japanese)", "https://takashima-kanko.jp/spot/2018/06/post_71.html"),
                link("official", "琵琶湖汽船 海津大崎桜クルーズ", "Biwako Kisen cherry cruise (Japanese)", "https://www.biwakokisen.co.jp/season_event/5972/")],
         info=info([row("train", "海津1区 → マキノ駅 コミュニティバス（国境線）約6分・220円（大崎寺から海津1区まで歩いて約30分）", "Kaizu 1-ku → Makino Station, community bus (Kokkyo line) about 6 min, ¥220 (30 min walk from Osakiji to the stop)")],
                   tip=T("拝観料は公式の案内に書かれていません（要確認）。", "Admission isn’t given in the official information (please check)."))),
    dict(id="oura", name=T("大浦の湖岸（奥びわ湖）", "Oura lakeshore (Oku-Biwako)"), kind=T("湖岸の桜", "Lakeside cherries"),
         blurb=T("大崎の先、湖岸の道をさらに東へ。人の少ない入り江に桜が咲く、奥びわ湖の静かな景色。",
                 "Further east along the lakeshore road beyond Osaki: quiet coves of cherries at the far north of Lake Biwa."),
         lat=35.48641, lng=136.11764,
         text=T("大浦（おおうら）の湖岸\n\n大崎寺から湖岸の道をさらに東へ、歩いて約1時間半（約6km）。トンネルを抜けると、入り江に沿って桜が続く大浦の集落に出ます。海津大崎よりも人が少なく、静かに桜を見られます。\n\n"
                "大浦から永原駅までは歩いて約30分（約2km）。永原13:56発の電車で、近江塩津で乗り換えて長浜に14:27に着きます（510円）。\n\n"
                "長い道のりなので、歩くのに自信がない日は、大崎寺からマキノ駅に戻りましょう。\n\nおすすめ訪問時間：12:40〜13:10",
                "Oura lakeshore\n\nFrom Osakiji, continue east along the lakeshore road: about 1 h 30 min on foot (about 6 km). Through the tunnels you reach the village of Oura, with cherries along its coves, quieter than Kaizu-Osaki.\n\n"
                "From Oura it’s about 30 minutes’ walk (2 km) to Nagahara Station. The 13:56 train, changing at Omi-Shiotsu, reaches Nagahama at 14:27 (¥510).\n\n"
                "It’s a long walk, so if you’re not up to it, go back from Osakiji to Makino Station instead.\n\nRecommended visit time: 12:40–13:10"),
         gmaps=[gm("大浦", "Oura", 35.48641, 136.11764, "長浜市西浅井町大浦"), gm("JR永原駅", "JR Nagahara Station", 35.49900, 136.12267, "JR永原駅")],
         links=[JR],
         notices=[SEASON],
         info=info([row("train", "永原13:56発 → 近江塩津で乗り換え → 長浜14:27着・510円（毎時56分発）", "Nagahara 13:56 → change at Omi-Shiotsu → Nagahama 14:27, ¥510 (hourly at :56)"),
                    row("hours", "大崎寺から大浦まで歩いて約1時間半、大浦から永原駅まで約30分", "About 1 h 30 min on foot from Osakiji to Oura, then about 30 min to Nagahara Station")],
                   tip=TRAIN_TIP)),
    dict(id="nagahamaeki", name=T("JR長浜駅", "JR Nagahama Station"), kind=T("駅", "Station"),
         blurb=T("秀吉が開いた城下町・長浜へ。駅のまわりに、お城も庭園も古い町並みも歩いて回れる範囲にあります。",
                 "Nagahama, the castle town founded by Hideyoshi: the castle, a garden and the old streets are all within walking distance of the station."),
         lat=35.37845, lng=136.26532,
         text=T("JR長浜駅（ながはまえき）\n\n豊臣秀吉が初めて城を持った城下町・長浜の玄関口です。西口を出ると長浜城（豊公園）、慶雲館、長浜鉄道スクエア、東口の先には黒壁スクエアの古い町並みが、どれも歩いて数分の所にあります。\n\n"
                "京都からは新快速で乗り換えなし（約1時間15分・1,340円）。\n\nおすすめ到着時間：14:27",
                "JR Nagahama Station\n\nGateway to Nagahama, the castle town where Toyotomi Hideyoshi first held a castle. West of the station are Nagahama Castle (Hoko Park), Keiunkan and the Railway Square; beyond the east side, the old streets of Kurokabe Square: all a few minutes’ walk.\n\n"
                "From Kyoto it’s direct by Special Rapid (about 1 h 15 min, ¥1,340).\n\nRecommended arrival: 14:27"),
         gmaps=[gm("JR長浜駅", "JR Nagahama Station", 35.37845, 136.26532, "JR長浜駅")],
         links=[JR],
         info=info([row("fee", "京都→長浜 1,340円（新快速で乗り換えなし）", "Kyoto → Nagahama ¥1,340 (Special Rapid, direct)")], tip=TRAIN_TIP)),
    dict(id="nagahamajo", name=T("長浜城・豊公園", "Nagahama Castle & Hoko Park"), kind=T("城・公園", "Castle & park"),
         blurb=T("湖のほとりに建つ長浜城と、約600本の桜の豊公園。天守からは琵琶湖が見渡せます。",
                 "Nagahama Castle on the lakeshore, and Hoko Park with some 600 cherry trees. The keep looks out over Lake Biwa."),
         lat=35.37766, lng=136.26128,
         text=T("長浜城（ながはまじょう）と豊公園（ほうこうえん）\n\n秀吉が築いた長浜城の跡に、昭和58年に再建された天守が建ち、中は長浜城歴史博物館になっています。最上階の展望台からは、琵琶湖と竹生島が見渡せます。\n\n"
                "まわりの豊公園は、約600本の桜が咲く日本さくら名所100選のひとつ。例年4月上旬〜中旬が見ごろで、海津大崎より少し早めです。\n\nおすすめ訪問時間：14:35〜15:25",
                "Nagahama Castle and Hoko Park\n\nOn the site of the castle Hideyoshi built stands a keep rebuilt in 1983, now the Nagahama Castle History Museum. From the top-floor lookout you see Lake Biwa and Chikubu Island.\n\n"
                "Hoko Park around it, with about 600 cherry trees, is one of Japan’s 100 best cherry spots; blossoms usually peak in early to mid April, a little earlier than Kaizu-Osaki.\n\nRecommended visit time: 14:35–15:25"),
         gmaps=[gm("長浜城歴史博物館", "Nagahama Castle History Museum", 35.37766, 136.26128, "長浜城歴史博物館")],
         links=[link("official", "長浜城歴史博物館 公式サイト", "Nagahama Castle History Museum (official, Japanese)", "https://nagahama-rekihaku.jp/")],
         info=info([row("hours", "9:00〜17:00（受付は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                    row("closed", "月曜（祝日・休日なら次の平日）、12月27日〜1月2日", "Mondays (next weekday if a holiday), 27 Dec – 2 Jan"),
                    row("fee", "大人500円、小中学生200円（豊公園は無料）", "¥500 adults, ¥200 children (Hoko Park free)")],
                   tip=T("長浜城歴史博物館と長浜市の公式サイトで確認しました。", "Checked on the museum and Nagahama City websites."))),
    dict(id="keiunkan", name=T("慶雲館", "Keiunkan"), kind=T("庭園・迎賓館", "Garden & guesthouse"),
         blurb=T("明治天皇を迎えるために建てられた迎賓館と庭園。冬は大きな梅の盆栽が並ぶ「盆梅展」の会場になります。",
                 "A guesthouse and garden built to receive Emperor Meiji. In winter it hosts the Bonbai-ten, an exhibition of huge plum bonsai."),
         lat=35.37581, lng=136.26634,
         text=T("慶雲館（けいうんかん）\n\n明治20年に明治天皇の休憩所として建てられた迎賓館です。広い日本庭園は、近代日本庭園の先駆けといわれる7代目小川治兵衛（植治）の作。\n\n"
                "1月中旬〜3月はじめは「長浜盆梅展」の会場になり、樹齢数百年の梅の盆栽が座敷いっぱいに並びます。写真は2025年1月の盆梅展のもの。2027年は1月10日〜3月10日の予定です。\n\n"
                "春の桜の時期は、ふだんの公開（庭園と建物）です。\n\nおすすめ訪問時間：15:35〜16:05",
                "Keiunkan\n\nBuilt in 1887 as a resting place for Emperor Meiji. The large Japanese garden is by Ogawa Jihei VII (Ueji), a pioneer of modern Japanese gardens.\n\n"
                "From mid January to early March it hosts the Nagahama Bonbai-ten: plum bonsai, some centuries old, filling the rooms. The photos are from the January 2025 show; in 2027 it runs from 10 January to 10 March.\n\n"
                "In cherry season it’s the regular opening (garden and buildings).\n\nRecommended visit time: 15:35–16:05"),
         gmaps=[gm("慶雲館", "Keiunkan", 35.37581, 136.26634, "慶雲館 長浜")],
         links=[link("official", "慶雲館（長浜観光協会）", "Keiunkan (Nagahama tourism, Japanese)", "https://kitabiwako.jp/keiunkan/guidance.html"),
                link("official", "長浜盆梅展 公式サイト", "Nagahama Bonbai-ten (official, Japanese)", "https://bonbai.jp/")],
         notices=[{"from": None, "to": "2027-01-09", "url": "https://kitabiwako.jp/spot/spot_1703",
                   "text": T("2026年12月1日〜2027年1月9日は、盆梅展の準備のため休館です。", "Closed 1 Dec 2026 – 9 Jan 2027 to prepare for the bonsai exhibition.")}],
         info=info([row("hours", "9:30〜17:00（入館は16:30まで）", "9:30–17:00 (last entry 16:30)"),
                    row("fee", "大人300円、小中学生150円", "¥300 adults, ¥150 children"),
                    row("hours", "長浜盆梅展 2027：1月10日〜3月10日 9:00〜17:00（入館16:30まで）、大人1,000円", "Bonbai-ten 2027: 10 Jan – 10 Mar, 9:00–17:00 (last entry 16:30), ¥1,000 adults", until="2027-03-10"),
                    row("closed", "盆梅展の前（12月1日ごろ〜1月9日）と後（3月11日〜下旬）は休館", "Closed before (about 1 Dec – 9 Jan) and after (11 Mar to late March) the bonsai exhibition")],
                   tip=T("長浜観光協会と長浜盆梅展の公式サイトで確認しました。", "Checked on the Nagahama tourism and Bonbai-ten websites."))),
    dict(id="tetsudo", name=T("長浜鉄道スクエア", "Nagahama Railway Square"), kind=T("鉄道の博物館", "Railway museum"),
         blurb=T("現存する日本最古の駅舎「旧長浜駅舎」と、蒸気機関車・電気機関車の展示。",
                 "Japan’s oldest surviving station building, plus steam and electric locomotives."),
         lat=35.37670, lng=136.26600,
         text=T("長浜鉄道スクエア\n\n明治15年に建てられた旧長浜駅舎は、現存する日本で最も古い駅舎です。となりの展示館には、D51形蒸気機関車やED70形電気機関車が並んでいます。\n\n"
                "長浜駅の西口から歩いて3分。入館は16:30までなので、時間に気をつけて。\n\nおすすめ訪問時間：16:10〜16:30",
                "Nagahama Railway Square\n\nThe old Nagahama Station building of 1882 is the oldest surviving station building in Japan. Next door, the exhibition hall shows a D51 steam locomotive and an ED70 electric locomotive.\n\n"
                "Three minutes from the west exit of Nagahama Station. Last entry is 16:30, so watch the time.\n\nRecommended visit time: 16:10–16:30"),
         gmaps=[gm("長浜鉄道スクエア", "Nagahama Railway Square", 35.37670, 136.26600, "長浜鉄道スクエア")],
         links=[link("official", "長浜鉄道スクエア（長浜観光協会）", "Nagahama Railway Square (Japanese)", "https://kitabiwako.jp/tetsudou/guidance.html")],
         info=info([row("hours", "9:30〜17:00（入館は16:30まで）", "9:30–17:00 (last entry 16:30)"),
                    row("closed", "12月29日〜1月3日", "29 Dec – 3 Jan"),
                    row("fee", "大人500円、小中学生200円", "¥500 adults, ¥200 children")],
                   tip=T("長浜観光協会の公式サイトで確認しました。", "Checked on the Nagahama tourism website."))),
    dict(id="kurokabe", name=T("黒壁スクエア", "Kurokabe Square"), kind=T("古い町並み・ガラス", "Old streets & glass"),
         blurb=T("黒い漆喰壁の明治の銀行を生かしたガラス館を中心に、古い町家のお店やギャラリーが並ぶ町並み。",
                 "Old merchant houses turned into shops and galleries, centred on a black-walled Meiji bank that is now a glass house."),
         lat=35.38068, lng=136.26708,
         text=T("黒壁（くろかべ）スクエア\n\n明治33年に建てられた銀行の建物「黒壁一號館（黒壁ガラス館）」を中心に、江戸から明治の町家を生かしたガラスのお店、ギャラリー、カフェが並びます。"
                "北国街道沿いの古い通りや、大通寺の表参道、町の中を流れる米川も歩いてみましょう。\n\n"
                "長浜駅から歩いて約5分。帰りは長浜17:57発の新快速で、京都に19:12に着きます（1,340円）。\n\nおすすめ訪問時間：16:45〜17:45",
                "Kurokabe Square\n\nCentred on Kurokabe No. 1, a bank built in 1900 and now the Kurokabe Glass House, the old Edo- and Meiji-era townhouses hold glass shops, galleries and cafés. "
                "Wander the old Hokkoku-kaido street, the approach to Daitsuji temple and the little Yone river running through town.\n\n"
                "About 5 minutes from Nagahama Station. Head home on the 17:57 Special Rapid, arriving in Kyoto at 19:12 (¥1,340).\n\nRecommended visit time: 16:45–17:45"),
         gmaps=[gm("黒壁ガラス館", "Kurokabe Glass House", 35.38068, 136.26708, "黒壁ガラス館")],
         links=[link("official", "黒壁スクエア 公式サイト", "Kurokabe (official, Japanese)", "https://www.kurokabe.co.jp/"), JR],
         info=info([row("hours", "黒壁スクエアのお店 10:00〜18:00（冬は17:00まで）。黒壁ガラス館 10:00〜17:00", "Kurokabe shops 10:00–18:00 (17:00 in winter). Kurokabe Glass House 10:00–17:00"),
                    row("train", "帰り：長浜17:57発（新快速）→ 京都19:12着・1,340円", "Return: Nagahama 17:57 (Special Rapid) → Kyoto 19:12, ¥1,340")],
                   tip=T("黒壁と長浜米原観光協会の公式サイト、電車は乗換案内で確認しました。", "Checked on the Kurokabe and Nagahama-Maibara tourism websites; trains on a route planner."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"])
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
KAIZU = [NO[k] for k in ("kaizu", "sakura", "osakiji")]
NAGA = [NO[k] for k in ("nagahamajo", "keiunkan", "tetsudo", "kurokabe")]
data = {
    "id": "kohoku",
    "_note": "京都から日帰り 海津大崎の桜と長浜のルート（kohoku/ のページ専用。形は eizan-line.json と同じ）。京都から湖西線でマキノへ、知内浜→海津の石積み→海津大崎の桜並木→大崎寺→（歩いて）大浦の湖岸→永原駅→長浜（長浜城・豊公園→慶雲館→長浜鉄道スクエア→黒壁スクエア）→京都。"
             "写真は Toshi の写真ライブラリから選んだもの（海津大崎は2025年4月12日と2026年4月3日、Nikon D7000 を含む。長浜は2025年1月13〜14日で、慶雲館は盆梅展。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "距離は OpenStreetMap の徒歩ルート（OSRM）で測った目安。info.checked は事実情報を確認した日（びわ湖高島観光協会・長浜の各施設の公式サイト、電車は乗換案内）。このファイルは scripts/build_kohoku_data.py で作る。",
    "sections": [{"first": 1, "last": 2, "day": 0}, {"first": 3, "last": 4, "day": 1}, {"first": 5, "last": 6, "day": 2}, {"first": 7, "last": 10, "day": 3}],
    "plan": {"_note": "「選んで回る」の設定。マキノ駅（とサニービーチ）は海津の場所を選ぶと入る。長浜駅は長浜の場所を選ぶと入る。defaultMode: pick。",
             "defaultMode": "pick",
             "picks": KAIZU + [NO["oura"]] + NAGA,
             "auto": {str(NO["makino"]): {"any": KAIZU}, str(NO["nagahamaeki"]): {"any": NAGA}},
             "hints": [
                 H("osakiji", {"any": [NO["osakiji"]], "andAny": NAGA, "none": [NO["oura"]]},
                   "大浦に行かない日は、大崎寺から海津1区のバス停まで歩いて約30分、コミュニティバスでマキノ駅へ。マキノから毎時51分発の電車で、近江塩津で乗り換えて長浜へ（36分・680円）。",
                   "Skipping Oura? Walk about 30 min from Osakiji to the Kaizu 1-ku stop and take the community bus to Makino. Trains leave Makino at :51 each hour; change at Omi-Shiotsu for Nagahama (36 min, ¥680)."),
                 H("osakiji", {"any": [NO["osakiji"]], "none": [NO["oura"]] + NAGA},
                   "帰りはマキノ駅から京都へ。新快速で乗り換えなし、約1時間10分です。",
                   "Go home from Makino Station: the Special Rapid runs direct to Kyoto in about 1 h 10 min."),
                 H("nagahamaeki", {"any": NAGA, "none": KAIZU + [NO["oura"]]},
                   "京都から長浜へは新快速で乗り換えなし、約1時間15分（1,340円）です。",
                   "From Kyoto, the Special Rapid runs direct to Nagahama in about 1 h 15 min (¥1,340)."),
             ]},
    "photoBase": "../images/kohoku/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
