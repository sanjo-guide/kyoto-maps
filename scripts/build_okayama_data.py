#!/usr/bin/env python3
"""岡山と倉敷（岡山城・後楽園・倉敷美観地区。京都から新幹線で日帰り）のデータ（data/routes/okayama.json）を書き出す。

使い方: python3 scripts/build_okayama_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/okayama/ にある。並べる順番は下の PHOTOS（自分の写真はファイル名だけ、
  ネットから借りた写真（Wikimedia Commons）は cc(...) で {"file", "credit": {"author", "license", "page"}} にする。
  ページでは写真の上に撮影者とライセンスが出る）
- オーナーの写真は少ない：岡山城と月見橋（2021年3月9日、iPhone。天守は2022年の改修の前）、
  岡山駅の新幹線（2025年9月13日 Nikon D7000、2021年3月10日）、駅前の噴水（2023年8月22日）、路面電車 MOMO（2023年8月6日）。
  後楽園・吉備津神社・倉敷はオーナーの写真がない場所なので、文章にも行った日などは書かない
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/okayama"
OUT = f"{R}/data/routes/okayama.json"
CHECKED = "2026-11-21"


def T(ja, en):
    return {"ja": ja, "en": en}


def gm(ja, en, lat, lng, q):
    return {"label": T(ja, en), "lat": lat, "lng": lng, "url": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)}


def link(kind, ja, en, url_ja, url_en=None):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url_ja, "en": url_en or url_ja}}


def row(kind, ja, en, until=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": None}


def info(rows, tip=None, verified=True, cash=False):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": CHECKED}
    if not verified:
        d["verified"] = False
    return d


def cc(file, author, license, title):
    """Wikimedia Commons の写真。title は Commons のファイル名（File: のあと）。"""
    return {"file": file, "credit": {"author": author, "license": license,
                                     "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))}}


# ネットから借りた写真の一覧（scratchpad の okayama/scr/dl.py が書き出したもの。ファイル名・撮影者・ライセンス・Commons のファイル名）
WEB = json.load(open(f"{R}/scripts/okayama_web_photos.json", encoding="utf-8"))
W = lambda sid: [cc(x["file"], x["author"], x["license"], x["title"]) for x in WEB.get(sid, [])]

PHOTOS = {
    "kyoto": ["eki-1.jpg"],
    "okayamaeki": ["eki-3.jpg"] + W("okayamaeki"),
    "tram": ["tram-1.jpg"] + W("tram"),
    "castle": W("castle") + ["castle-1.jpg"],
    "tsukimi": ["tsukimi-1.jpg", "tsukimi-2.jpg", "tsukimi-3.jpg"],
    "korakuen": W("korakuen"),
    "kibitsu": W("kibitsu"),
    "lunch": W("lunch"),
    "bikan": W("bikan"),
    "ohara": W("ohara"),
    "boat": W("boat"),
    "ivy": W("ivy"),
    "honmachi": W("honmachi"),
    "achi": W("achi"),
    "kaeri": ["eki-4.jpg"],
}

JR = link("timetable", "JRおでかけネット（時刻・運賃）", "JR West timetables and fares", "https://www.jr-odekake.net/", "https://www.westjr.co.jp/global/en/")
OKADEN = link("official", "岡山電気軌道（路面電車）", "Okayama Electric Tramway (Japanese)", "https://okayama-kido.co.jp/tram/route-map/")
CASTLE = link("official", "岡山城 公式サイト", "Okayama Castle (official)", "https://okayama-castle.jp/guide", "https://okayama-castle.jp/home-en/")
KORAKUEN = link("official", "岡山後楽園 公式サイト", "Okayama Korakuen (official)", "https://okayama-korakuen.jp/goriyo/441.html", "https://okayama-korakuen.jp/foregin_taravelers.html")
KAWAFUNE = link("official", "くらしき川舟流し 公式ページ（WEB予約）", "Kurashiki river boat: official page and online booking (Japanese)", "https://kankou-kurashiki.jp/special/kawafune/")
KTABI = link("info", "倉敷観光WEB", "Kurashiki tourism website", "https://www.kurashiki-tabi.jp/", "https://www.kurashiki-tabi.jp/en/")

YAKAN = {"from": None, "to": "2026-11-29", "url": "https://okayama-korakuen.jp/",
         "head": T("11月29日まで、後楽園と岡山城は夜も開いています", "Until 29 November the garden and castle stay open at night"),
         "text": T("2026年11月20日〜29日は、後楽園の「秋の幻想庭園」（8:00〜20:30、入園は20:00まで）と、岡山城の「秋の烏城灯源郷」（17:00〜20:30、天守の入場は20:00まで）があります。この期間に夜の岡山を見たい人は、順番を逆にして、先に倉敷、夕方から岡山にしてください。",
                   "From 20 to 29 November 2026, Korakuen holds its autumn night opening (8:00–20:30, last entry 20:00) and Okayama Castle is lit up (17:00–20:30, last entry to the keep 20:00). To see Okayama at night in this period, reverse the day: Kurashiki first, Okayama from late afternoon.")}
WINTER = {"from": None, "to": None, "url": "https://www.ohara.or.jp/visit/",
          "head": T("12〜2月は倉敷を先に", "December to February: do Kurashiki first"),
          "text": T("12〜2月は、大原美術館が15:00に閉まります（入館は14:30まで）。川舟も1〜2月は土・日・祝だけです。冬に美術館へ行く人は、順番を逆にして、午前に倉敷、午後に岡山（後楽園は17:00まで、岡山城は17:30まで）にしてください。",
                    "From December to February the Ohara Museum closes at 15:00 (last entry 14:30), and in January and February the boats run only at weekends and on holidays. If you want the museum in winter, reverse the day: Kurashiki in the morning, Okayama in the afternoon (Korakuen until 17:00, the castle until 17:30).")}

S = [
    dict(id="kyoto", name=T("京都駅（新幹線）", "Kyoto Station (Shinkansen)"), kind=T("駅", "Station"),
         blurb=T("のぞみで岡山まで約1時間。自由席で片道7,140円、往復14,280円。このサイトでいちばん交通費がかかる日帰りです。",
                 "About an hour to Okayama by Nozomi. ¥7,140 one way unreserved, ¥14,280 return: the most expensive day trip on this site."),
         lat=34.98535, lng=135.75877,
         text=T("京都駅（きょうとえき）から新幹線で岡山へ\n\n京都から岡山まで、のぞみで約1時間です。乗り換えはありません。平日・土曜とも 7:41発 のぞみ103号 → 岡山 8:41着。その前に 7:20発 ひかり731号 → 8:23着もあります。\n\n"
                "先にお金の話をします。自由席で片道7,140円（乗車券3,740円＋特急券3,400円）、往復で14,280円。指定席は片道8,100円でした（2026年11月25日の例。時期で変わります）。岡山〜倉敷の往復660円、入場料などを足すと、1日で2万円近くになります。このサイトの日帰りの中でいちばん高いルートです。\n\n"
                "それでも、新幹線なら朝7時台に出て、夜7時半には京都に戻れます。岡山城と後楽園、倉敷の町並みを1日で両方見られるのは、新幹線だからです。\n\n"
                "少し安くするなら、帰りを「さくら」や「こだま」で新大阪まで、そこから新快速にすると6,270円（のぞみより約30分多くかかります）。JR西日本のネット予約の割引きっぷは、時期と列車で値段が変わるので、公式サイトで確認してください。\n\n"
                "のぞみの自由席は1・2号車です。朝の下りは、発車の10分前にホームに並べばたいてい座れます。新神戸から先はトンネルが多く、景色はあまり見えません。\n\n"
                "写真は岡山駅のホームで撮った新幹線です（2025年9月）。\n\nおすすめ訪問時間：7:41発（京都駅には7:25ごろ）",
                "Kyoto Station: Shinkansen to Okayama\n\nOkayama is about an hour from Kyoto by Nozomi, with no change. On weekdays and Saturdays alike, Nozomi 103 leaves at 7:41 and arrives at 8:41. Before it, Hikari 731 leaves at 7:20 and arrives at 8:23.\n\n"
                "Money first. An unreserved seat is ¥7,140 one way (fare ¥3,740 + express charge ¥3,400), ¥14,280 return. A reserved seat was ¥8,100 one way (on 25 November 2026; it varies with the season). Add ¥660 for Okayama–Kurashiki and back, plus admissions, and the day comes close to ¥20,000. It is the most expensive day trip on this site.\n\n"
                "What you get for it: leave after 7:00, be back in Kyoto by 19:30, and see both Okayama’s castle and garden and the old quarter of Kurashiki in one day. Only the Shinkansen makes that possible.\n\n"
                "To save a little, come back by Sakura or Kodama to Shin-Osaka and change to a Special Rapid: ¥6,270, about 30 minutes slower than the Nozomi. JR West’s online discount tickets change price by season and train, so check the official site.\n\n"
                "Unreserved seats on the Nozomi are in cars 1 and 2. On a morning westbound train, be on the platform ten minutes before departure and you will usually get a seat. Beyond Shin-Kobe it is mostly tunnels, so don’t expect much of a view.\n\n"
                "The photo is a Shinkansen at Okayama Station (September 2025).\n\nRecommended visit time: the 7:41 train (be at Kyoto Station by about 7:25)"),
         gmaps=[gm("京都駅 新幹線のりば", "Kyoto Station (Shinkansen gates)", 34.98535, 135.75877, "京都駅 新幹線中央口")],
         links=[JR],
         notices=[WINTER, YAKAN],
         info=info([row("train", "京都 → 岡山：のぞみ103号 7:41発 → 8:41着／ひかり731号 7:20発 → 8:23着（平日・土曜とも）。次は 8:03発 → 9:03着",
                        "Kyoto → Okayama: Nozomi 103, 7:41 → 8:41; Hikari 731, 7:20 → 8:23 (weekdays and Saturdays). Next: 8:03 → 9:03"),
                    row("fee", "自由席 片道7,140円（往復14,280円）。指定席は片道8,100円（11月25日の例）",
                        "Unreserved ¥7,140 one way (¥14,280 return). Reserved ¥8,100 one way (on 25 November)"),
                    row("train", "帰り：岡山 → 京都 のぞみ 18:20発 → 19:19着、18:28発 → 19:28着。遅い時間は 21:44発 → 22:45着",
                        "Back: Okayama → Kyoto by Nozomi, 18:20 → 19:19 or 18:28 → 19:28. Late: 21:44 → 22:45")],
                   tip=T("時刻と運賃は乗換案内（2026年11月25日（水）と28日（土））で確認しました。指定席の値段は時期で変わります。",
                         "Times and fares were checked on a route planner for Wednesday 25 and Saturday 28 November 2026. Reserved-seat prices vary with the season."))),
    dict(id="okayamaeki", name=T("岡山駅", "Okayama Station"), kind=T("駅", "Station"),
         blurb=T("新幹線を降りたら「後楽園口（東口）」へ。駅前に桃太郎の像と噴水、その先に路面電車ののりばがあります。",
                 "Off the Shinkansen, head for the Korakuen (east) exit: the Momotaro statue and a fountain, then the tram stop."),
         lat=34.66640, lng=133.91850,
         text=T("岡山駅（おかやまえき）\n\n新幹線の改札を出たら、「後楽園口（東口）」へ下ります。反対側の「運動公園口（西口）」に出ないように。\n\n"
                "駅前の広場に、犬・猿・きじを連れた桃太郎の像と、たんぽぽの綿毛の形の噴水があります（写真は2023年8月の夕方）。岡山は桃太郎の話のふるさとです。\n\n"
                "お城と後楽園へは、駅前からまっすぐ東へのびる「桃太郎大通り」を行きます。路面電車で城下（しろした）まで行って歩くのがいちばん楽です。歩いても行けますが、後楽園まで約25分かかります。\n\n"
                "ここで決めておくこと：\n"
                "・荷物があれば、駅のコインロッカーへ。昼に倉敷へ行くとき、もう一度この駅を通ります。\n"
                "・倉敷の川舟に乗りたい人は、まだ予約していなければ、今スマホでWEB予約の空きを見てください（11番のスポット）。\n"
                "・帰りの新幹線は自由席なら予約はいりません。\n\n"
                "岡山のおみやげ（きびだんごなど）は、帰りの乗り換えのときに、新幹線の改札の前の店で買えます。\n\nおすすめ訪問時間：8:41〜8:55",
                "Okayama Station\n\nFrom the Shinkansen gates, go down to the Korakuen exit (east side). Don’t come out on the opposite Undo-koen (west) side.\n\n"
                "In the square are a statue of Momotaro with his dog, monkey and pheasant, and a fountain shaped like a dandelion clock (my photo is from an August evening in 2023). Okayama is the home of the Momotaro folk tale.\n\n"
                "The castle and Korakuen are straight east along Momotaro-odori, the avenue that starts at the station. Easiest is the tram to Shiroshita and then on foot. You can walk the whole way, but it is about 25 minutes to Korakuen.\n\n"
                "Things to settle here:\n"
                "• Leave bags in the station’s coin lockers. You pass through this station again at midday on the way to Kurashiki.\n"
                "• If you want the canal boat in Kurashiki and haven’t booked, check the online booking on your phone now (see stop 11).\n"
                "• No booking is needed for an unreserved seat home.\n\n"
                "Okayama souvenirs (kibi-dango and so on) can be bought at the shops in front of the Shinkansen gates when you change trains on the way back.\n\nRecommended visit time: 8:41–8:55"),
         gmaps=[gm("岡山駅 後楽園口（東口）", "Okayama Station, Korakuen exit", 34.66640, 133.91850, "岡山駅 東口 桃太郎像")],
         links=[JR, link("info", "岡山観光WEB", "Okayama Prefecture tourism website", "https://www.okayama-kanko.jp/", "https://www.okayama-japan.jp/en/")],
         info=info([row("hours", "岡山駅から後楽園まで歩いて約25分、タクシーで約10分（後楽園の案内）", "Okayama Station to Korakuen: about 25 min on foot, about 10 min by taxi (garden’s access page)"),
                    row("train", "岡山 → 倉敷：JR山陽本線・伯備線で16〜17分・330円。昼は1時間に4本ほど", "Okayama → Kurashiki: JR Sanyo or Hakubi line, 16–17 min, ¥330; about four trains an hour at midday")],
                   tip=T("歩く時間は後楽園の公式サイト、電車は乗換案内（2026年11月25日）で確認しました。", "Walking time from Korakuen’s website; trains from a route planner (25 November 2026)."))),
    dict(id="tram", name=T("路面電車（岡山駅前 → 城下）", "Tram: Okayama-ekimae → Shiroshita"), kind=T("路面電車", "Tram"),
         blurb=T("駅前から「東山」行きで3つ目の城下まで。160円、交通系ICカードが使えます。",
                 "From the station, a Higashiyama-bound tram to Shiroshita, the third stop. ¥160; IC cards accepted."),
         lat=34.66575, lng=133.92895,
         text=T("岡山の路面電車（ろめんでんしゃ）\n\n岡山電気軌道、通称「おかでん」。明治45年（1912年）から走っている、日本でいちばん短い部類の路面電車です。\n\n"
                "のりばは駅前の広場の先、大通りのまん中にあります。行き先は2つ。「東山（ひがしやま）」行きに乗ってください。「清輝橋（せいきばし）」行きは途中で右へ曲がってしまいます。\n\n"
                "3つ目の「城下（しろした）」で降ります。運賃はどこまで乗っても160円。うしろのドアから乗って、降りるときに前で払います。ICOCA や Suica などの交通系ICカードが使えます（車内でチャージはできません）。\n\n"
                "城下から岡山城までは歩いて約10分。電停から東へ、旭川（あさひがわ）のほうへ進むと、黒い天守が見えてきます。\n\n"
                "1日乗車券は400円です。3回乗らないと元がとれないので、このルート（往復2回）では買わなくて大丈夫です。\n\n"
                "写真の青い電車は低床車の「MOMO」（2023年8月、岡山駅前）。走る日と時刻は決まっていて、検査で休む日もあります。黒い「KURO」や、子どもに人気の「チャギントン電車」（予約制の観光電車）も走っています。\n\n"
                "乗らずに歩く人は、桃太郎大通りをまっすぐ東へ。城下まで約1km、15分ほどです。\n\nおすすめ訪問時間：8:55〜9:10",
                "The Okayama tram\n\nOkayama Electric Tramway, “Okaden” to locals, has run since 1912 and is among the shortest tram systems in Japan.\n\n"
                "The stop is beyond the station square, in the middle of the avenue. There are two destinations: take a tram for Higashiyama. Trams for Seikibashi turn off to the right partway.\n\n"
                "Get off at Shiroshita, the third stop. The fare is a flat ¥160. Board at the rear door and pay at the front as you get off. ICOCA, Suica and other transport IC cards work (you can’t top them up on board).\n\n"
                "From Shiroshita it is about ten minutes on foot to the castle. Walk east from the stop towards the Asahi river and the black keep comes into view.\n\n"
                "A one-day pass is ¥400. It needs three rides to pay off, so on this route (two rides) you don’t need it.\n\n"
                "The blue tram in the photo is the low-floor MOMO (August 2023, at Okayama-ekimae). It runs on set days and times and is sometimes out for inspection. There is also the black KURO, and the Chuggington tram for children (a sightseeing tram, by reservation).\n\n"
                "Walking instead? Go straight east along Momotaro-odori: about 1 km, 15 minutes, to Shiroshita.\n\nRecommended visit time: 8:55–9:10"),
         gmaps=[gm("城下電停", "Shiroshita tram stop", 34.66575, 133.92895, "城下駅 岡山電気軌道"), gm("岡山駅前電停", "Okayama-ekimae tram stop", 34.66585, 133.91960, "岡山駅前駅 岡山電気軌道")],
         links=[OKADEN],
         info=info([row("train", "岡山駅前 → 城下：東山行きで3つ目、約5〜8分。日中は数分おき", "Okayama-ekimae → Shiroshita: third stop on a Higashiyama tram, about 5–8 min; every few minutes in the daytime"),
                    row("fee", "大人160円、子ども80円（全線同じ）。1日乗車券は大人400円", "¥160, children ¥80 (flat fare). One-day pass ¥400"),
                    row("hours", "城下から岡山城まで歩いて約10分（岡山城の案内）", "Shiroshita to the castle: about 10 min on foot (castle’s access page)")],
                   tip=T("運賃と1日乗車券は岡山電気軌道の公式サイト、時刻は乗換案内で確認しました。MOMO の運行日は公式サイトの「運行に関する情報」に出ます。",
                         "Fare and day pass from the tramway’s website; times from a route planner. MOMO’s running days are posted in the service news on the official site."))),
    dict(id="castle", name=T("岡山城", "Okayama Castle"), kind=T("城", "Castle"),
         blurb=T("黒い板張りの天守から「烏城（うじょう）」と呼ばれる城。2022年に改修が終わり、中は新しい展示室です。",
                 "The “Crow Castle”, named for its black-boarded keep. Renovated in 2022, with new exhibition rooms inside."),
         lat=34.66515, lng=133.93605,
         text=T("岡山城（おかやまじょう）\n\n豊臣秀吉に可愛がられた宇喜多秀家（うきたひでいえ）が築いた城で、天守は1597年の完成と伝わります。外の壁が黒い板で覆われているので、別名は「烏城（うじょう）」。カラスの城です。金箔の瓦が使われていたので「金烏城（きんうじょう）」とも呼ばれます。\n\n"
                "天守は明治のあとも残っていましたが、1945年の空襲で焼けました。今の天守は1966年に建て直されたコンクリートの建物で、2022年11月に「令和の大改修」が終わりました。外の黒と金がくっきりして、中の展示も新しくなっています（私の写真は改修前の2021年3月。今はもっと黒く、金のしゃちほこが光っています）。\n\n"
                "見るところ：\n"
                "・天守の土台。四角ではなく、いびつな五角形です。もとの丘の形に合わせたためといわれます。石垣を横から見るとよく分かります。\n"
                "・月見櫓（つきみやぐら）。本丸の北西の角にある、江戸時代のはじめから残る本物の櫓です。戦災をまぬがれました。\n"
                "・天守の最上階。旭川と後楽園を上から見下ろせます。\n\n"
                "正直に言うと、天守の中は博物館です。古い木の階段や柱はありません。公式サイトによると見学は50〜60分。時間が足りない日は、中に入らず、外から眺めるだけでも十分きれいです。いちばんいい角度は、このあと渡る月見橋と、その先の川べりから。\n\n"
                "エレベーターは4階まで。5・6階は階段です。\n\n"
                "入場券は、後楽園との共通券（800円）がお得です。別々に買うと500円＋500円で1,000円。先に行くほうの窓口で買ってください。\n\nおすすめ訪問時間：9:15〜10:05",
                "Okayama Castle\n\nBuilt by Ukita Hideie, a favourite of Toyotomi Hideyoshi; the keep is said to have been finished in 1597. Its outer walls are clad in black boards, hence the nickname U-jo, “Crow Castle”. Gilded roof tiles earned it another: Kin-u-jo, the “Golden Crow Castle”.\n\n"
                "The keep outlasted the Meiji period but burned in the air raid of 1945. Today’s is a concrete rebuild of 1966, and a major renovation was completed in November 2022: the black and gold outside are sharper and the displays are new. (My photo is from March 2021, before the work. It is blacker now, with gold shachihoko on the roof.)\n\n"
                "What to look at:\n"
                "• The base of the keep. It is not square but an irregular pentagon, said to follow the shape of the original hill. You see it best from beside the stone wall.\n"
                "• Tsukimi-yagura, the “moon-viewing turret” at the north-west corner of the main enclosure: an original from the early Edo period that survived the war.\n"
                "• The top floor, looking down on the Asahi river and Korakuen.\n\n"
                "To be honest, the inside is a museum: no old timber stairs or pillars. The castle’s own site says a visit takes 50–60 minutes. If you are short of time, skip the interior; the castle is handsome enough from outside. The best angles are from Tsukimi bridge, which you cross next, and the riverbank beyond it.\n\n"
                "The lift goes to the 4th floor; the 5th and 6th are by stairs.\n\n"
                "Buy the combined ticket with Korakuen (¥800). Separately they are ¥500 + ¥500 = ¥1,000. Get it at whichever you visit first.\n\nRecommended visit time: 9:15–10:05"),
         gmaps=[gm("岡山城 天守", "Okayama Castle keep", 34.66515, 133.93605, "岡山城 天守閣")],
         links=[CASTLE],
         info=info([row("hours", "9:00〜17:30（入場は17:00まで）", "9:00–17:30 (last entry 17:00)"),
                    row("closed", "12月29日〜31日。荒天や点検で休む日があります", "29–31 December; may also close for bad weather or inspections"),
                    row("fee", "大人（15歳以上）500円、中学生以下無料。後楽園との共通券800円", "¥500 (15 and over); junior high and under free. Combined ticket with Korakuen ¥800"),
                    row("hours", "「秋の烏城灯源郷」11月20日〜29日は17:00〜20:30（入場は20:00まで）", "Autumn illumination, 20–29 November: 17:00–20:30 (last entry 20:00)", until="2026-11-29")],
                   tip=T("岡山城の公式サイトで確認しました。支払いはクレジットカード・交通系ICカード・QRコード決済も使えます。", "Checked on the castle’s website. Credit cards, transport IC cards and QR payments are accepted."))),
    dict(id="tsukimi", name=T("月見橋", "Tsukimi bridge"), kind=T("橋", "Bridge"),
         blurb=T("岡山城と後楽園をつなぐ、旭川の歩行者の橋。ふり返ると、川の上に天守が立って見えます。",
                 "The footbridge over the Asahi river between the castle and Korakuen. Look back for the keep standing above the water."),
         lat=34.66640, lng=133.93486,
         text=T("月見橋（つきみばし）\n\n天守の北側の「廊下門（ろうかもん）」を出て坂を下ると、旭川に架かる鉄の橋があります。歩く人だけの橋で、渡った先が後楽園の南門です。お城から後楽園へは、この橋がいちばん近道です。\n\n"
                "橋のまん中でふり返ってください。石垣の上に天守が立ち、下を川が流れる、岡山城のいちばんいい眺めです（写真1枚目。2021年3月）。朝は天守に日が当たります。\n\n"
                "渡ったら右へ。川べりの道を少し歩くと、川と天守がいっしょに入る写真が撮れます（写真3枚目）。\n\n"
                "川には手こぎのボートや、桃の形のボートが出ている日があります。\n\nおすすめ訪問時間：10:05〜10:15",
                "Tsukimi bridge\n\nLeave the keep by the Roka-mon gate on its north side and walk down the slope to an iron bridge over the Asahi river. It is for pedestrians only, and on the far side is Korakuen’s south gate. This is the shortest way from the castle to the garden.\n\n"
                "Stop in the middle and look back: the keep on its stone walls with the river below is the best view of Okayama Castle (photo 1, March 2021). In the morning the sun is on the keep.\n\n"
                "Across the bridge, turn right. A little way along the riverside path you can get the river and the keep in one frame (photo 3).\n\n"
                "On some days there are rowing boats and peach-shaped pedal boats on the river.\n\nRecommended visit time: 10:05–10:15"),
         gmaps=[gm("月見橋", "Tsukimi bridge", 34.66640, 133.93486, "月見橋 岡山市北区")],
         links=[],
         info=info([row("hours", "自由に渡れます。岡山城の天守から後楽園の南門まで歩いて約5分", "Free to cross. About 5 minutes on foot from the keep to Korakuen’s south gate")],
                   tip=T("歩く時間は地図（OpenStreetMap）で測った目安です。", "The walking time is an estimate from OpenStreetMap."))),
    dict(id="korakuen", name=T("岡山後楽園", "Okayama Korakuen"), kind=T("庭園（日本三名園）", "Garden"),
         blurb=T("約300年前に岡山藩主がつくった庭。広い芝生と池のむこうに、岡山城の天守が見えます。",
                 "A garden laid out by the lord of Okayama about 300 years ago: wide lawns and ponds, with the castle keep beyond."),
         lat=34.66780, lng=133.93560,
         text=T("岡山後楽園（おかやまこうらくえん）\n\n岡山藩主の池田綱政（いけだつなまさ）が、自分のやすらぎの場としてつくらせた庭です。金沢の兼六園、水戸の偕楽園と並ぶ「日本三名園」で、国の特別名勝。\n\n"
                "ほかの大名庭園とちがうのは、広さと明るさです。まん中が大きな芝生で、空が広く、園のどこからでも遠くまで見えます。水路（曲水）が園内をぐるりと流れています。\n\n"
                "月見橋から来ると南門に着きます。入ったら、次の順に歩くとむだがありません。\n\n"
                "・唯心山（ゆいしんざん）：高さ数メートルの築山。上ると芝生・池・茶畑が一度に見えます。まずここへ。\n"
                "・流店（りゅうてん）：建物のまん中を水路が通る、めずらしい休憩所。\n"
                "・沢の池（さわのいけ）：園の中心の池。島が3つあります。\n"
                "・延養亭（えんようてい）：藩主が座って庭を眺めた建物。その前から見る、芝生と池と唯心山、その奥の山までの眺めが、この庭の「正面」です。\n"
                "・井田（せいでん）と茶畑：昔は園内に田畑が広がっていた名残です。\n"
                "・鶴舎（かくしゃ）：タンチョウが飼われています。\n\n"
                "天守がいちばんよく見えるのは、沢の池の北側から南をふり返ったとき。庭の向こうにお城が入ります。\n\n"
                "ひと回り1時間ほど。日かげが少ないので、夏は帽子と水を。春は桜と梅林、6月は花菖蒲、夏は蓮、秋はもみじの林（千入の森）が見ごろです。\n\n"
                "帰りは、南門から月見橋を戻って城下電停へ（約15分）か、正門を出て鶴見橋を渡り城下電停へ（約10分）。正門の前からは岡山駅行きのバスも出ています。\n\nおすすめ訪問時間：10:15〜11:25",
                "Okayama Korakuen\n\nIkeda Tsunamasa, lord of Okayama, had this garden made as his own place of rest. With Kenroku-en in Kanazawa and Kairaku-en in Mito it is one of Japan’s “three great gardens”, and a Special Place of Scenic Beauty.\n\n"
                "What sets it apart from other daimyo gardens is space and light. The middle is a great lawn under an open sky, and you can see far from anywhere inside. A stream winds all the way round.\n\n"
                "From Tsukimi bridge you arrive at the south gate. This order wastes no steps:\n\n"
                "• Yuishinzan: a small artificial hill a few metres high. From the top you take in lawns, ponds and the tea field at once. Go here first.\n"
                "• Ryuten: an unusual rest pavilion with the stream running through the middle of it.\n"
                "• Sawa-no-ike: the central pond, with three islands.\n"
                "• Enyo-tei: the house where the lord sat to look at the garden. The view from in front of it, across lawn, pond and Yuishinzan to the hills behind, is the garden’s “front”.\n"
                "• Seiden and the tea field: reminders that much of the garden was once rice fields and farm plots.\n"
                "• The crane aviary, with red-crowned cranes.\n\n"
                "The keep shows best when you stand north of Sawa-no-ike and look back south: the castle sits beyond the garden.\n\n"
                "Allow about an hour for a circuit. There is little shade, so bring a hat and water in summer. Cherry blossom and the plum grove in spring, irises in June, lotus in summer, and the maple grove (Chishio-no-mori) in autumn.\n\n"
                "To leave, go back over Tsukimi bridge from the south gate to the Shiroshita tram stop (about 15 min), or out of the main gate and over Tsurumi bridge to Shiroshita (about 10 min). Buses for Okayama Station also leave from in front of the main gate.\n\nRecommended visit time: 10:15–11:25"),
         gmaps=[gm("後楽園 南門", "Korakuen south gate", 34.66690, 133.93470, "岡山後楽園 南門"), gm("後楽園 正門", "Korakuen main gate", 34.66930, 133.93420, "岡山後楽園 正門")],
         links=[KORAKUEN, link("info", "後楽園の花だより", "What’s in bloom at Korakuen (Japanese)", "https://okayama-korakuen.jp/hanadayori/index.html")],
         info=info([row("hours", "10月1日〜3月19日 8:00〜17:00（入園は16:45まで）／3月20日〜9月30日 7:30〜18:00（入園は17:45まで）", "1 Oct–19 Mar 8:00–17:00 (last entry 16:45) / 20 Mar–30 Sep 7:30–18:00 (last entry 17:45)"),
                    row("hours", "「秋の幻想庭園」11月20日〜29日は8:00〜20:30（入園は20:00まで）", "Autumn night opening, 20–29 November: 8:00–20:30 (last entry 20:00)", until="2026-11-29"),
                    row("closed", "休みなし", "Open every day"),
                    row("fee", "大人500円、65歳以上200円、高校生以下無料（2027年3月31日まで）。岡山城との共通券800円（シニア用の共通券はありません）", "¥500; 65 and over ¥200; high school and under free (until 31 March 2027). Combined ticket with the castle ¥800 (no senior combined ticket)"),
                    row("train", "帰り：城下 → 岡山駅前 路面電車で約7分・160円。正門前からは岡電バス・宇野バスで岡山駅へ10〜15分", "Back: tram Shiroshita → Okayama-ekimae, about 7 min, ¥160. Or Okaden and Uno buses from the main gate to Okayama Station, 10–15 min")],
                   tip=T("後楽園の公式サイトで確認しました（入園案内は2026年4月1日更新）。共通券は、行事や休館で売らない日があります。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the garden’s website (admission page updated 1 April 2026). The combined ticket is not sold on some event or closure days. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="kibitsu", name=T("吉備津神社", "Kibitsu Shrine"), kind=T("神社（国宝の本殿と長い廻廊）", "Shrine"),
         blurb=T("桃太郎のもとになった話が伝わる神社。国宝の本殿と、山すそをまっすぐ下る長い廻廊があります。岡山駅からJRで約15分。",
                 "The shrine of the legend behind Momotaro: a National Treasure main hall and a long roofed corridor running down the hillside. About 15 minutes by JR from Okayama."),
         lat=34.67068, lng=133.85061,
         text=T("吉備津神社（きびつじんじゃ）\n\n岡山駅からJR桃太郎線（吉備線）で4つ目の吉備津駅へ、そこから松並木の参道を歩いて約10分です。\n\n"
                "まつられているのは吉備津彦命（きびつひこのみこと）。この土地で温羅（うら）という鬼を退治したという話が伝わり、それが桃太郎のもとになったといわれます。\n\n"
                "見るところは2つです。\n\n"
                "・本殿と拝殿（国宝）：屋根が2つ並んでつながった「吉備津造り（きびつづくり）」という、ここだけの形。今の建物は室町時代、約600年前の再建です。横に回って、屋根の形を見てください。\n"
                "・廻廊（かいろう）：本殿の横から、山のすそに沿って南へまっすぐ下る屋根つきの長い廊下。地面の傾きに合わせてゆるく波うっています。上から見下ろすのと、下から見上げるのと、両方どうぞ。写真を撮るなら、人が少ない朝か、午後の遅い時間に。\n\n"
                "廻廊の途中に御竈殿（おかまでん）があり、釜の鳴る音で吉凶を占う「鳴釜神事（なるかましんじ）」が行われます（金曜は休み）。\n\n"
                "ここを入れると、往復の電車と合わせて約2時間かかります。電車は1時間に1本ほどなので、時刻を先に決めてください。後楽園のあと、岡山12:12発 → 吉備津12:26着、帰りは吉備津13:21発 → 岡山13:36着、13:50発の山陽本線で倉敷14:07着。倉敷に着くのが2時間ほど遅くなるので、その日は大原美術館か川舟のどちらかにしぼることになります。\n\n"
                "お昼は岡山駅で買って行くか、倉敷に着いてから遅めに。\n\nおすすめ訪問時間：12:35〜13:10",
                "Kibitsu Shrine\n\nFrom Okayama take the JR Momotaro line (Kibi line) four stops to Kibitsu, then walk about ten minutes up an avenue of pines.\n\n"
                "The shrine is dedicated to Kibitsuhiko-no-mikoto, who by local legend defeated an ogre called Ura here: the story said to lie behind Momotaro.\n\n"
                "Two things to see.\n\n"
                "• The main hall and worship hall (National Treasure): two roofs joined side by side in a style found only here, called Kibitsu-zukuri. The present building dates from the Muromachi period, about 600 years ago. Walk round to the side to see the roof.\n"
                "• The corridor: a long roofed passage running straight down the foot of the hill from beside the main hall, rising and dipping gently with the ground. Look down it from the top and up it from the bottom. For photos, come in the morning or late in the afternoon when few people are about.\n\n"
                "Partway along is the Okama-den, where the Narukama ritual tells fortunes by the sound of a boiling cauldron (not on Fridays).\n\n"
                "Adding this takes about two hours with the trains, which run only about once an hour, so fix your times first. After Korakuen: Okayama 12:12 → Kibitsu 12:26; back on the 13:21 → Okayama 13:36, then the 13:50 Sanyo line train → Kurashiki 14:07. You reach Kurashiki about two hours later, so that day choose either the Ohara Museum or the boat.\n\n"
                "Buy lunch at Okayama Station to take along, or eat late in Kurashiki.\n\nRecommended visit time: 12:35–13:10"),
         gmaps=[gm("吉備津神社", "Kibitsu Shrine", 34.67068, 133.85061, "吉備津神社 岡山市"), gm("吉備津駅", "Kibitsu Station", 34.67441, 133.84605, "吉備津駅")],
         links=[link("official", "吉備津神社 公式サイト", "Kibitsu Shrine (official)", "https://www.kibitujinja.com/", "https://www.kibitujinja.com/en/"), JR],
         info=info([row("hours", "参拝 5:00〜18:00。鳴釜神事は9:00〜14:00", "Open 5:00–18:00. Narukama ritual 9:00–14:00"),
                    row("closed", "鳴釜神事は金曜休み", "No Narukama ritual on Fridays"),
                    row("fee", "境内は自由に参拝できます", "The grounds are free to enter"),
                    row("train", "岡山 → 吉備津：JR桃太郎線 14〜17分・210円。岡山発 9:29、10:22、11:12、12:12、13:03、13:52／吉備津発 10:46、11:36、12:36、13:21、14:17、15:17（平日）",
                        "Okayama → Kibitsu: JR Momotaro line, 14–17 min, ¥210. From Okayama 9:29, 10:22, 11:12, 12:12, 13:03, 13:52; from Kibitsu 10:46, 11:36, 12:36, 13:21, 14:17, 15:17 (weekdays)")],
                   tip=T("参拝時間と神事は吉備津神社の公式サイト、電車は乗換案内（2026年11月25日）で確認しました。駅から歩いて約10分も公式サイトの案内です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Hours and the ritual from the shrine’s website; trains from a route planner (25 November 2026). The 10-minute walk from the station is the shrine’s own figure. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="lunch", name=T("倉敷駅から美観地区へ・お昼", "Kurashiki Station to the old quarter, and lunch"), kind=T("駅・お昼", "Station & lunch"),
         blurb=T("岡山から電車で16〜17分。倉敷駅の南口から美観地区まで歩いて10〜15分です。着いたらまずお昼を。",
                 "16–17 minutes by train from Okayama, then 10–15 minutes on foot from the south exit to the old quarter. Lunch first."),
         lat=34.59860, lng=133.76890,
         text=T("倉敷駅（くらしきえき）から美観地区へ\n\n岡山駅の在来線ホームから、山陽本線か伯備線（はくびせん）の電車で4つ目が倉敷です。16〜17分・330円。12:04発 → 12:20着。特急「やくも」も倉敷に止まりますが、特急料金がかかるので、ふつうの電車で十分です。\n\n"
                "倉敷駅は南口へ。美観地区までの道は2つあります。\n"
                "・倉敷中央通り：駅前からまっすぐ南へのびる大通り。分かりやすい道です。\n"
                "・商店街：駅前の左手からアーケードの「倉敷センター街」「えびす通り」「本通り」と続きます。雨の日はこちら。古い店が残っていて、歩いていて楽しいのもこちらです。出口が美観地区の北の入口です。\n\n"
                "どちらも歩いて10〜15分。\n\n"
                "お昼について。美観地区の中と商店街に、うどん・そば、定食、町家のカフェがたくさんあります。岡山らしいものなら、ままかり（小魚の酢漬け）、ばら寿司、ぶっかけうどん。\n\n"
                "・本町通りの「三宅商店」は、江戸時代の終わりの町家を使ったカフェで、野菜のカレーと季節のパフェが知られています。\n"
                "・倉敷アイビースクエアの中には、和食と洋食のレストランがあります。席が多いので、どこも並んでいるときに。\n\n"
                "12時台はどの店も混みます。川舟の時間を決めている人は、舟の時間から逆算して、軽く食べるか、時間をずらしてください。店の営業日と時間は店ごとにちがうので、行きたい店があれば先に調べてください。月曜休みの店が多めです。\n\nおすすめ訪問時間：12:20〜13:30",
                "Kurashiki Station to the old quarter\n\nFrom the local platforms at Okayama, Kurashiki is the fourth stop on the Sanyo or Hakubi line: 16–17 minutes, ¥330. The 12:04 arrives at 12:20. The Yakumo limited express stops at Kurashiki too, but costs extra; the ordinary trains are fine.\n\n"
                "Leave Kurashiki Station by the south exit. There are two ways to the Bikan quarter.\n"
                "• Kurashiki Chuo-dori: the main avenue straight south from the station. Hard to get lost.\n"
                "• The shopping arcades: from the left of the station square, the covered Center-gai, Ebisu-dori and Hon-dori follow one another. Take these in rain. They also have more old shops and are the nicer walk. They come out at the north entrance of the old quarter.\n\n"
                "Either way is 10–15 minutes on foot.\n\n"
                "Lunch. The old quarter and the arcades are full of udon and soba shops, set-meal places and cafes in old townhouses. For something local: mamakari (small fish in vinegar), bara-zushi (scattered sushi) and bukkake udon.\n\n"
                "• Miyake Shoten on Honmachi street is a cafe in a late-Edo townhouse, known for its vegetable curry and seasonal parfaits.\n"
                "• Kurashiki Ivy Square has Japanese and Western restaurants with plenty of seats: useful when everywhere else has a queue.\n\n"
                "Everything is busy between 12:00 and 13:00. If you have a boat time, work back from it and eat lightly or off-peak. Opening days and hours differ from place to place, so check ahead if you have somewhere in mind. Many close on Mondays.\n\nRecommended visit time: 12:20–13:30"),
         gmaps=[gm("倉敷駅 南口", "Kurashiki Station, south exit", 34.60085, 133.76610, "倉敷駅 南口"), gm("三宅商店", "Miyake Shoten", 34.59640, 133.77290, "三宅商店 倉敷市本町")],
         links=[link("official", "三宅商店 公式サイト", "Miyake Shoten (official, Japanese)", "https://miyakeshouten.com/"), KTABI, JR],
         info=info([row("train", "岡山 → 倉敷：16〜17分・330円。岡山発 12:04、12:18、12:32、12:40、12:53（平日）", "Okayama → Kurashiki: 16–17 min, ¥330. From Okayama at 12:04, 12:18, 12:32, 12:40, 12:53 (weekdays)"),
                    row("hours", "倉敷駅から美観地区まで歩いて10〜15分", "Kurashiki Station to the old quarter: 10–15 min on foot"),
                    row("hours", "店の営業時間と休みは店ごとにちがいます（要確認）", "Restaurant hours and closing days vary (please check)")],
                   tip=T("電車は乗換案内（2026年11月25日）、歩く時間は倉敷の観光案内（駅から約10〜15分）で確認しました。三宅商店は公式サイトで建物とメニューを確認しましたが、営業時間はここに書いていません。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Trains from a route planner (25 November 2026); the walking time from Kurashiki’s tourist information (10–15 min). Miyake Shoten’s building and menu were checked on its website; its hours are not given here. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="bikan", name=T("倉敷川と白壁の町並み", "Kurashiki canal and the white-walled quarter"), kind=T("町並み", "Old quarter"),
         blurb=T("柳の並ぶ川の両側に、白壁と黒い瓦の蔵や屋敷が続きます。今橋から中橋、高砂橋まで、歩いて10分ほどの範囲です。",
                 "Willows along a canal, with white-walled, black-tiled storehouses and merchant houses on both banks. From Imabashi to Nakabashi and Takasago-bashi is about ten minutes on foot."),
         lat=34.59610, lng=133.77105,
         text=T("倉敷川（くらしきがわ）と白壁の町並み\n\n倉敷は江戸時代、幕府が直接おさめる「天領」でした。まわりの村の米や綿がこの川に集められ、舟で運び出されました。川ぞいの蔵と屋敷は、その商人たちのものです。\n\n"
                "歩く順番：\n\n"
                "・今橋（いまばし）：大原美術館の前の石の橋。欄干に龍が彫ってあります。ここから川下を見るのが、絵はがきの眺めです。\n"
                "・有隣荘（ゆうりんそう）：今橋の向かい、緑がかった瓦の屋敷。大原家の別邸で、ふだんは外から見るだけです。\n"
                "・中橋（なかばし）と倉敷館：川が直角に曲がるところ。まん中が盛り上がった石の橋と、洋風の木造の倉敷館（観光案内所）が並びます。川舟の当日券はここで売っています。倉敷館にはコインロッカーとトイレがあります。\n"
                "・倉敷民藝館、倉敷考古館：どちらも古い米蔵を使った小さな館。白い壁に、瓦を貼って目地を白いしっくいで盛り上げた「なまこ壁」が見られます。\n"
                "・高砂橋（たかさごばし）：川舟が折り返すあたり。ここまで来ると人が減ります。\n\n"
                "中橋から南へ3分ほどのところに「倉敷デニムストリート」があります。倉敷市の児島（こじま）は国産ジーンズが最初に作られた町で、そのデニムの店を集めた一角です。青い肉まんの「デニムまん」とラムネ味の青い「デニムソフト」を売っています。買い物をしないなら5分で見終わるので、時間がない日は通りすぎて大丈夫です（営業時間は公式に確認できていません）。\n\n"
                "電線は地面の下に埋められていて、空がすっきりしています。\n\n"
                "昼すぎは団体でにぎやかです。写真を撮るなら、夕方、店が閉まりはじめる17時ごろからがきれいです。日が暮れると川ぞいに明かりがつきます。帰りの電車まで時間があれば、もう一度川ぞいを通って駅へ戻ってください。\n\nおすすめ訪問時間：13:30〜14:00",
                "Kurashiki canal and the white-walled quarter\n\nIn the Edo period Kurashiki was governed directly by the shogunate. Rice and cotton from the surrounding villages were gathered on this canal and shipped out by boat; the storehouses and residences along it belonged to the merchants who handled them.\n\n"
                "A walking order:\n\n"
                "• Imabashi: the stone bridge in front of the Ohara Museum, with dragons carved on its parapet. The view downstream from here is the postcard one.\n"
                "• Yurinso: the house with greenish roof tiles opposite Imabashi, a villa of the Ohara family. Normally seen from outside only.\n"
                "• Nakabashi and Kurashiki-kan: where the canal turns a right angle. A humpbacked stone bridge stands beside the Western-style wooden Kurashiki-kan, now the tourist office. Same-day boat tickets are sold here; it also has coin lockers and toilets.\n"
                "• Kurashiki Museum of Folkcraft and the Archaeological Museum: small museums in old rice storehouses. Look for namako walls: tiles set on the wall with raised white plaster joints.\n"
                "• Takasago-bashi: about where the boats turn round. Fewer people come this far.\n\n"
                "About three minutes south of Nakabashi is Kurashiki Denim Street. Kojima, in the south of the city, is where Japan’s first domestic jeans were made, and this corner gathers its denim shops. It sells blue “denim-man” meat buns and blue ramune-flavoured soft-serve. If you aren’t shopping, five minutes is enough, so walk past when time is short (its opening hours could not be confirmed officially).\n\n"
                "The power lines are buried, so the sky is clear of wires.\n\n"
                "Early afternoon is busy with tour groups. For photos, the light is best from around 17:00, as the shops begin to close. After dusk lamps come on along the canal. If you have time before your train, walk the canal once more on your way back to the station.\n\nRecommended visit time: 13:30–14:00"),
         gmaps=[gm("中橋・倉敷館", "Nakabashi & Kurashiki-kan", 34.59582, 133.77176, "倉敷館観光案内所"), gm("今橋", "Imabashi", 34.59640, 133.77065, "今橋 倉敷美観地区"), gm("倉敷デニムストリート", "Kurashiki Denim Street", 34.59453, 133.77124, "倉敷デニムストリート")],
         links=[KTABI],
         info=info([row("hours", "町並みは自由に歩けます。倉敷館観光案内所 9:00〜18:00（年末年始は休み）", "The quarter is free to walk. Kurashiki-kan tourist office 9:00–18:00 (closed over New Year)"),
                    row("hours", "倉敷民藝館・倉敷考古館・有隣荘の公開日と料金は、ここでは確認していません（要確認）", "Opening days and fees of the Folkcraft Museum, the Archaeological Museum and Yurinso were not checked here (please check)")],
                   tip=T("倉敷館の時間は倉敷観光コンベンションビューローと岡山観光WEBで確認しました。橋や建物の説明は岡山観光WEBの記事によります。デニムストリートの営業時間は、サイトによって9:30からと10:00からの両方があり、確かめられませんでした。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Kurashiki-kan’s hours from the Kurashiki Convention and Visitors Bureau and the Okayama tourism website, which is also the source for the bridges and buildings. Sites disagree on Denim Street’s opening time (9:30 or 10:00), so it is left unconfirmed. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="ohara", name=T("大原美術館", "Ohara Museum of Art"), kind=T("美術館", "Art museum"),
         blurb=T("1930年に開いた、日本で最初の西洋美術の美術館。エル・グレコ「受胎告知」やモネ「睡蓮」があります。月曜休み。",
                 "Opened in 1930, Japan’s first museum of Western art, with El Greco’s Annunciation and Monet’s Water Lilies. Closed Mondays."),
         lat=34.59603, lng=133.77044,
         text=T("大原美術館（おおはらびじゅつかん）\n\n倉敷の実業家・大原孫三郎（おおはらまごさぶろう）が、画家の児島虎次郎（こじまとらじろう）にヨーロッパで集めさせた絵をもとに、1930年に開いた美術館です。西洋美術を中心にした私立の美術館として、日本で最初のものです。今橋の前に、ギリシャ神殿のような柱の本館が立っています。\n\n"
                "有名なのは、エル・グレコ「受胎告知」と、モネ「睡蓮」。ほかにもゴーギャン、マティスなど、教科書で見た名前が並びます。小さな町の川べりに、この絵がそろっていること自体が、倉敷のいちばんの驚きです。\n\n"
                "入館券は1枚で、本館、工芸・東洋館、児島虎次郎記念館の3つに入れます。建物ごとにスタンプを押す形で、押していない建物は別の日にも使えます（期限なし）。分館は長いあいだ休館中です。\n\n"
                "回り方：時間が1時間なら、本館だけにしぼってください。工芸・東洋館は、古い米蔵をつないだ建物で、棟方志功の版画や濱田庄司たちの焼き物があります。建物そのものも見ものなので、あと30分あればこちらも。\n\n"
                "入館料は2,000円。安くはありませんが、絵が好きな人は外さないでください。絵に興味がなければ、外から本館と今橋を眺めて、その分を川舟や本町の散歩に回すのも手です。\n\n"
                "月曜は休みです（祝日のときは開館。8月は休みなし）。12〜2月は15:00に閉まります。\n\nおすすめ訪問時間：14:00〜15:10",
                "Ohara Museum of Art\n\nThe Kurashiki industrialist Ohara Magosaburo had the painter Kojima Torajiro collect pictures in Europe, and in 1930 opened this museum around them: the first private museum in Japan centred on Western art. The main building, with columns like a Greek temple, stands in front of Imabashi.\n\n"
                "The best-known works are El Greco’s Annunciation and Monet’s Water Lilies, alongside Gauguin, Matisse and other names from the textbooks. That these paintings hang beside a canal in a small town is the biggest surprise Kurashiki has.\n\n"
                "One ticket covers three buildings: the Main Gallery, the Craft and Asian Art Gallery, and the Kojima Torajiro Memorial Hall. Each stamps your ticket, and any building left unstamped can be visited another day (no expiry). The Annex is closed long-term.\n\n"
                "How to do it: with one hour, keep to the Main Gallery. The Craft and Asian Art Gallery is a row of old rice storehouses joined together, with prints by Munakata Shiko and pottery by Hamada Shoji and others; the building itself is worth seeing, so add it if you have another 30 minutes.\n\n"
                "Admission is ¥2,000. Not cheap, but don’t drop it if you like painting. If you don’t, look at the main building and Imabashi from outside and spend the time on the boat or the Honmachi streets instead.\n\n"
                "Closed on Mondays (open when Monday is a holiday; no closing days in August). From December to February it closes at 15:00.\n\nRecommended visit time: 14:00–15:10"),
         gmaps=[gm("大原美術館 本館", "Ohara Museum of Art, Main Gallery", 34.59603, 133.77044, "大原美術館")],
         links=[link("official", "大原美術館 公式サイト", "Ohara Museum of Art (official)", "https://www.ohara.or.jp/visit/", "https://www.ohara.or.jp/en/")],
         notices=[WINTER],
         info=info([row("hours", "3〜11月 9:00〜17:00（入館は16:30まで）／12〜2月 9:00〜15:00（入館は14:30まで）。児島虎次郎記念館は10:00から", "Mar–Nov 9:00–17:00 (last entry 16:30) / Dec–Feb 9:00–15:00 (last entry 14:30). Kojima Torajiro Memorial Hall opens at 10:00"),
                    row("closed", "月曜（祝日・振替休日のときは開館。8月は休みなし）。臨時の休館と年末の休みは公式サイトのカレンダーで", "Mondays (open on public holidays; no closing days in August). For temporary and year-end closures see the calendar on the official site"),
                    row("fee", "一般2,000円、小学生〜高校生（18歳未満）500円。本館、工芸・東洋館、児島虎次郎記念館に入れます", "¥2,000; school pupils under 18 ¥500. Covers the Main Gallery, the Craft and Asian Art Gallery and the Kojima Torajiro Memorial Hall")],
                   tip=T("大原美術館の公式サイトで確認しました。現金のほか、クレジットカード・電子マネー・QRコード決済が使えます。収蔵作品の説明は岡山観光WEBにもよります。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the museum’s website. Cash, credit cards, e-money and QR payments are accepted. Notes on the collection also draw on the Okayama tourism website. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="boat", name=T("くらしき川舟流し", "Kurashiki river boat"), kind=T("川舟（約20分）", "Canal boat (about 20 min)"),
         blurb=T("船頭さんが竿で進める小さな舟で、倉敷川を約20分。1艘6人で、券は昼すぎに売り切れる日が多いです。WEB予約を。",
                 "Twenty minutes on the canal in a small boat poled by a boatman. Six seats a boat, and tickets are often gone by early afternoon: book online."),
         lat=34.59570, lng=133.77150,
         text=T("くらしき川舟流し（かわふねながし）\n\nすげ笠をかぶって、小さな和舟で倉敷川を往復します。約20分。水面は道より低いので、石垣と白壁を下から見上げることになり、歩くのとはちがう町に見えます。中橋の下をくぐるときに、船頭さんが橋の話をしてくれます（日本語）。\n\n"
                "いちばん大事なのは、券のとり方です。1艘に6人しか乗れず、30分おきにしか出ません。\n\n"
                "① WEB予約（おすすめ）：2026年10月から、乗る日の30日前の午前0時から予約できるようになりました。席の半分ほどがWEB用です。京都を出る前に、15:00か15:30の便をとっておけば、このルートの時間に合います。当日は出発の10分前までに、乗り場へ直接行きます。\n\n"
                "② 当日券：朝9:00から、倉敷館観光案内所（中橋の横）で、便ごとに先着順で売ります。昼すぎには売り切れていることが多いので、このルートのように午後に倉敷へ着く人は、当日券をあてにしないでください。それでも着いたらすぐ倉敷館で聞いてみる価値はあります。WEBが満席でも、当日券の分は別にあります。\n\n"
                "乗り場は、倉敷館の前の川をはさんだ向こう岸です。\n\n"
                "乗り遅れると払い戻しはありません。大原美術館のあとに乗る人は、舟の時間の15分前には美術館を出てください。日傘は使えません。雨や強い風の日は中止で、そのときは当日中に倉敷館で払い戻しです。\n\n"
                "3〜12月は第2月曜が休み、1〜2月は土・日・祝だけ。7〜9月は15:00が最終便です。\n\nおすすめ訪問時間：15:20集合、15:30発〜15:50",
                "Kurashiki river boat\n\nIn a sedge hat, you go up and down the canal in a small wooden boat: about 20 minutes. The water is lower than the street, so you look up at the stone banks and white walls, and the town looks different from on foot. Under Nakabashi the boatman tells the story of the bridge (in Japanese).\n\n"
                "What matters is how you get a ticket. A boat takes only six, and they leave only every 30 minutes.\n\n"
                "1) Book online (recommended): since October 2026 you can book from midnight 30 days before the day. About half the seats are sold this way. Book the 15:00 or 15:30 boat before you leave Kyoto and it fits this route. On the day, go straight to the landing at least 10 minutes before departure.\n\n"
                "2) Same-day tickets: sold from 9:00 at the Kurashiki-kan tourist office (beside Nakabashi), first come first served for each departure. They are often sold out by early afternoon, so if you arrive in Kurashiki after lunch, as on this route, don’t count on them. It is still worth asking at Kurashiki-kan as soon as you arrive: same-day seats are kept separate even when online booking is full.\n\n"
                "The landing is on the bank opposite Kurashiki-kan.\n\n"
                "Miss your boat and there is no refund. If you ride after the Ohara Museum, leave the museum 15 minutes before your time. Parasols are not allowed. Boats are cancelled in rain or strong wind; refunds are given the same day at Kurashiki-kan.\n\n"
                "No boats on the second Monday of the month from March to December; weekends and holidays only in January and February. From July to September the last boat is at 15:00.\n\nRecommended visit time: meet 15:20 for the 15:30 boat, back 15:50"),
         gmaps=[gm("川舟乗り場", "Boat landing", 34.59570, 133.77150, "くらしき川舟流し 乗船場"), gm("倉敷館観光案内所（当日券）", "Kurashiki-kan tourist office (same-day tickets)", 34.59582, 133.77176, "倉敷館観光案内所")],
         links=[KAWAFUNE, link("info", "運航状況（Instagram）", "Today’s operation (Instagram, Japanese)", "https://www.instagram.com/kurashiki_riverboat/")],
         caution=T("券は売り切れます。WEB予約を", "Tickets sell out: book online"),
         info=info([row("hours", "9:30始発〜17:00最終、30分おき。約20分。7月1日〜9月30日は15:00が最終", "First boat 9:30, last 17:00, every 30 min; about 20 min. Last boat 15:00 from 1 July to 30 September"),
                    row("closed", "3〜12月は第2月曜（祝日は運航）。1〜2月は土・日・祝だけ運航。12月29日〜1月3日は休み。雨・強風・水位が低い日は中止", "Second Monday of the month, Mar–Dec (runs on holidays). Jan–Feb: weekends and holidays only. No boats 29 Dec–3 Jan. Cancelled in rain, strong wind or low water"),
                    row("fee", "大人1,000円、5歳〜小学生500円、5歳未満無料（2026年10月から）", "¥1,000; age 5 to elementary school ¥500; under 5 free (since October 2026)"),
                    row("hours", "WEB予約は乗る日の30日前の0:00から（1日14便・各6席）。当日券は9:00から倉敷館観光案内所で先着順", "Online booking opens at 0:00 thirty days ahead (14 boats a day, 6 seats each). Same-day tickets from 9:00 at Kurashiki-kan, first come first served"),
                    row("hours", "夜の川舟：10月・11月の土曜 18:00〜19:00（30分おき3便）", "Evening boats: Saturdays in October and November, 18:00–19:00 (three boats, every 30 min)", until="2026-11-28")],
                   tip=T("倉敷観光コンベンションビューローの公式ページと岡山観光WEB（2026年11月2日の記事）で確認しました。「昼すぎには売り切れることが多い」は岡山観光WEBの記事によります。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the Kurashiki Convention and Visitors Bureau’s official page and the Okayama tourism website (article of 2 November 2026), which is the source for tickets often selling out by early afternoon. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="ivy", name=T("倉敷アイビースクエア", "Kurashiki Ivy Square"), kind=T("赤れんがの工場あと", "Former brick mill"),
         blurb=T("明治22年に建った紡績工場を、ホテルと広場に作りかえた場所。つたのからむ赤れんがの壁に囲まれた中庭は、自由に歩けます。",
                 "A cotton mill of 1889 turned into a hotel and courtyards. You can walk freely in the square enclosed by ivy-covered red-brick walls."),
         lat=34.59470, lng=133.77350,
         text=T("倉敷アイビースクエア\n\n白壁の町並みのすぐ東に、赤れんがの大きな建物があります。1889年（明治22年）に建てられた倉敷紡績所（今のクラボウ）の最初の工場です。大原美術館をつくった大原家の会社で、倉敷が蔵の町から工場の町へ変わった出発点です。\n\n"
                "1970年代、ふえる観光客のために、工場の外の壁と骨組みを残してホテルに作りかえました。設計は倉敷出身の建築家・浦辺鎮太郎（うらべしずたろう）。ここは江戸時代の代官所のあとでもあります。\n\n"
                "見るところは中庭です。泊まらなくても入れます。れんがの壁いっぱいのつた（アイビー）は、もともと工場の中の温度を下げるために植えられたものだそうです。夏は緑、秋は赤くなり、冬は葉が落ちて、つるだけが壁に残ります。\n\n"
                "敷地の中に、クラボウの歴史を見せる倉紡記念館（創業のころの綿の倉庫）、陶芸の体験ができる愛美工房、みやげ物の店、カフェがあります。トイレも借りられるので、休憩にちょうどいい場所です。\n\n"
                "西の門から入って中庭を抜け、東の門から出ると、次の本町・東町の通りへ近道になります。\n\nおすすめ訪問時間：16:00〜16:25",
                "Kurashiki Ivy Square\n\nJust east of the white-walled streets stands a large red-brick complex: the first mill of the Kurashiki Spinning Works (today’s Kurabo), built in 1889. It was the Ohara family’s company, the same family that founded the museum, and the starting point of Kurashiki’s change from a storehouse town to a mill town.\n\n"
                "In the 1970s, with tourist numbers growing, the mill was rebuilt as a hotel, keeping its outer walls and frame. The architect was Urabe Shizutaro, a Kurashiki native. The site was also that of the Edo-period magistrate’s office.\n\n"
                "The thing to see is the courtyard, open to non-guests. The ivy that covers the brick walls is said to have been planted to keep the mill cooler inside. It is green in summer, red in autumn, and in winter only the bare vines cling to the brick.\n\n"
                "On the grounds are the Kurabo Memorial Hall (in a cotton warehouse from the founding years), a pottery workshop, souvenir shops and a cafe. There are toilets too, so it is a good place for a break.\n\n"
                "Enter by the west gate, cross the courtyard and leave by the east gate for a short cut to Honmachi and Higashimachi.\n\nRecommended visit time: 16:00–16:25"),
         gmaps=[gm("倉敷アイビースクエア", "Kurashiki Ivy Square", 34.59470, 133.77350, "倉敷アイビースクエア")],
         links=[link("official", "倉敷アイビースクエア 公式サイト", "Kurashiki Ivy Square (official)", "https://www.ivysquare.co.jp/history/", "https://www.ivysquare.co.jp/english/")],
         info=info([row("hours", "中庭は自由に歩けます", "The courtyard is free to walk through"),
                    row("fee", "倉紡記念館の時間と入館料は、公式サイトで確認できませんでした（要確認）", "Hours and fee of the Kurabo Memorial Hall could not be confirmed on the official site (please check)")],
                   tip=T("建物の歴史は倉敷アイビースクエアの公式サイト（歴史のページ）で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "The history is from Ivy Square’s official website. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="honmachi", name=T("本町・東町", "Honmachi & Higashimachi"), kind=T("町家の通り", "Townhouse streets"),
         blurb=T("川ぞいより一本北の、職人と商人の通り。格子の町家が続き、川ぞいより静かです。",
                 "The craftsmen’s and merchants’ street one block north of the canal: latticed townhouses, and quieter than the waterside."),
         lat=34.59640, lng=133.77400,
         text=T("本町（ほんまち）・東町（ひがしまち）\n\n倉敷川ぞいが蔵と大きな屋敷の町なら、こちらは人が住んで商売をしてきた通りです。鶴形山（つるがたやま）のふもとを東西にのびる昔の街道で、川ぞいよりも古くからの町だといわれます。\n\n"
                "格子の窓、白いしっくいと黒い焼き板の壁、2階の小さな窓（倉敷窓）。そういう町家が、今は帆布やマスキングテープの店、ガラスや器の店、カフェになっています。\n\n"
                "アイビースクエアの東の門から北へ出ると本町通りに当たります。右（東）へ行くと東町で、店が減って、ふつうの暮らしの通りになります。観光客はほとんど来ません。東町の端まで歩いて戻っても15分ほどです。\n\n"
                "左（西）へ戻ると、阿智神社への石段の下を通って、川ぞいの中橋のほうへ出ます。\n\n"
                "倉敷のみやげを買うなら、川ぞいよりこの通りで。倉敷帆布のバッグや、倉敷生まれのマスキングテープは、ここで選べます。店は17時から18時に閉まるところが多いので、買い物は16時台に。\n\nおすすめ訪問時間：16:25〜16:55",
                "Honmachi and Higashimachi\n\nIf the canal is the district of storehouses and grand residences, this is the street where people lived and traded. It is an old highway running east–west along the foot of Tsurugata hill, and is said to be older as a settlement than the waterside.\n\n"
                "Lattice windows, white plaster and charred-board walls, small upstairs windows. Townhouses like these now hold shops for canvas goods and masking tape, glass and ceramics, and cafes.\n\n"
                "Go north from Ivy Square’s east gate and you meet Honmachi street. Turn right (east) for Higashimachi, where the shops thin out and it becomes an ordinary residential street; hardly any tourists come. To the end of Higashimachi and back takes about 15 minutes.\n\n"
                "Turning left (west) takes you past the foot of the steps to Achi Shrine and out towards Nakabashi on the canal.\n\n"
                "For Kurashiki souvenirs, shop here rather than on the canal: bags of Kurashiki canvas, and masking tape, which was born in Kurashiki. Many shops close between 17:00 and 18:00, so shop before 17:00.\n\nRecommended visit time: 16:25–16:55"),
         gmaps=[gm("本町通り", "Honmachi street", 34.59640, 133.77400, "倉敷市本町 本町通り"), gm("東町", "Higashimachi", 34.59672, 133.77706, "倉敷市東町")],
         links=[KTABI],
         info=info([row("hours", "通りは自由に歩けます。店は17〜18時に閉まるところが多く、休みは店ごとにちがいます（要確認）", "Free to walk. Many shops close between 17:00 and 18:00; closing days vary (please check)")],
                   tip=T("通りの説明は倉敷観光WEBによります。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "The description draws on the Kurashiki tourism website. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="achi", name=T("阿智神社", "Achi Shrine"), kind=T("神社（町を見下ろす丘）", "Shrine on the hill"),
         blurb=T("美観地区のすぐ北、鶴形山の上の神社。石段を上ると、瓦屋根の町並みを上から見られます。",
                 "The shrine on Tsurugata hill, just north of the old quarter. Climb the stone steps for a view over the tiled roofs."),
         lat=34.59720, lng=133.77344,
         text=T("阿智神社（あちじんじゃ）\n\n倉敷の町の氏神さまです。本町通りから、長い石段を上ります。3〜4分。\n\n"
                "上りきって、ふり返ってください。美観地区の瓦屋根が足もとに広がります。下を歩いているときには見えなかった、蔵の屋根の重なりが分かります。境内の南の端の絵馬殿からも同じ眺めです。夕方、屋根に日が当たる時間がきれいです。\n\n"
                "境内は木が多く、下のにぎわいが聞こえなくなります。春は「阿知の藤（あちのふじ）」という古い藤が咲きます。\n\n"
                "お参りはいつでもできますが、お守りの授与所は17:00まで。日が暮れると石段は暗いので、秋と冬は明るいうちに上ってください（11月の日の入りは17時ごろ）。そのときは、本町・東町より先にここへ。\n\n"
                "倉敷駅へは、石段を下りて本町通りを西へ、商店街を抜けて歩いて約15分です。\n\nおすすめ訪問時間：16:55〜17:15",
                "Achi Shrine\n\nThe guardian shrine of Kurashiki. A long flight of stone steps climbs from Honmachi street: three or four minutes.\n\n"
                "At the top, turn round. The tiled roofs of the old quarter spread below you, and you see how the storehouse roofs overlap, which you can’t from the street. The votive-tablet hall at the south edge of the grounds has the same view. It is at its best late in the afternoon with the sun on the roofs.\n\n"
                "The grounds are wooded, and the bustle below fades away. In spring an old wisteria, the Achi-no-fuji, flowers here.\n\n"
                "You can visit at any hour, but the amulet office closes at 17:00. The steps are dark after sunset, so in autumn and winter climb while it is light (sunset is around 17:00 in November): come here before Honmachi and Higashimachi.\n\n"
                "For Kurashiki Station, go down the steps, west along Honmachi street and through the arcades: about 15 minutes on foot.\n\nRecommended visit time: 16:55–17:15"),
         gmaps=[gm("阿智神社", "Achi Shrine", 34.59720, 133.77344, "阿智神社 倉敷市本町")],
         links=[link("official", "阿智神社 公式サイト", "Achi Shrine (official, Japanese)", "https://achi.or.jp/")],
         info=info([row("hours", "参拝はいつでも。授与所 9:00〜17:00", "Open at all hours. Amulet office 9:00–17:00"),
                    row("fee", "無料", "Free"),
                    row("hours", "倉敷駅から歩いて約15分（神社の案内）", "About 15 min on foot from Kurashiki Station (shrine’s access note)")],
                   tip=T("阿智神社の公式サイトで確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the shrine’s website. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="kaeri", name=T("倉敷駅（帰り）", "Kurashiki Station (going home)"), kind=T("駅", "Station"),
         blurb=T("倉敷17:44発 → 岡山18:00着、のぞみ18:20発 → 京都19:19着。岡山駅の乗り換えは10分みてください。",
                 "Kurashiki 17:44 → Okayama 18:00, then Nozomi 18:20 → Kyoto 19:19. Allow ten minutes to change at Okayama."),
         lat=34.60106, lng=133.76609,
         text=T("倉敷駅から京都へ帰る\n\n美観地区から倉敷駅まで歩いて10〜15分。岡山行きの電車は1時間に4〜5本あります。\n\n"
                "・倉敷17:44発 → 岡山18:00着。のぞみ50号 18:20発 → 京都19:19着。\n"
                "・1本遅らせて、倉敷18:13発 → 岡山18:30着。のぞみは1時間に3〜4本あるので、次に来たものに乗れば、20時すぎには京都です。\n\n"
                "岡山駅では、在来線のホームから新幹線の改札まで、のりかえ口を通って5分ほど。自由席に並ぶ時間を入れて、10分はみてください。きびだんごなどのおみやげと駅弁は、新幹線の改札の前で買えます。\n\n"
                "倉敷で夕ごはんを食べて、明かりのついた川ぞいを歩いてから帰るのもおすすめです。その場合も、岡山21:44発ののぞみ108号（京都22:45着）まであります。これを逃すと、乗り換えが必要になり、京都に着くのは23:30ごろです。\n\n"
                "写真は岡山駅の新幹線ホーム（2021年3月）。\n\nおすすめ訪問時間：17:44発（京都に19:19着）",
                "Kurashiki Station: back to Kyoto\n\nIt is 10–15 minutes on foot from the old quarter to Kurashiki Station. There are four or five trains an hour to Okayama.\n\n"
                "• Kurashiki 17:44 → Okayama 18:00. Nozomi 50 at 18:20 → Kyoto 19:19.\n"
                "• Or one later: Kurashiki 18:13 → Okayama 18:30. There are three or four Nozomi an hour, so take the next one and you are in Kyoto soon after 20:00.\n\n"
                "At Okayama it takes about five minutes from the local platforms through the transfer gate to the Shinkansen. Allow ten, with time to queue for an unreserved seat. Kibi-dango and other souvenirs, and boxed meals, are sold in front of the Shinkansen gates.\n\n"
                "Staying for dinner in Kurashiki and a walk along the lit canal is a good way to end the day too. The Nozomi 108 leaves Okayama at 21:44 (Kyoto 22:45). After that you have to change trains and reach Kyoto around 23:30.\n\n"
                "The photo is the Shinkansen platform at Okayama (March 2021).\n\nRecommended visit time: the 17:44 train (Kyoto 19:19)"),
         gmaps=[gm("倉敷駅", "Kurashiki Station", 34.60106, 133.76609, "倉敷駅")],
         links=[JR],
         info=info([row("train", "倉敷 → 岡山：16〜18分・330円。倉敷発 17:39、17:44、18:13、18:18（平日）", "Kurashiki → Okayama: 16–18 min, ¥330. From Kurashiki at 17:39, 17:44, 18:13, 18:18 (weekdays)"),
                    row("train", "岡山 → 京都：のぞみ 18:20発 → 19:19着、18:28発 → 19:28着。遅い時間は 21:44発 → 22:45着", "Okayama → Kyoto: Nozomi 18:20 → 19:19, 18:28 → 19:28. Late: 21:44 → 22:45"),
                    row("fee", "のぞみ自由席 7,140円。さくら＋新大阪から新快速なら6,270円（18:14発 → 京都19:44着）", "Nozomi unreserved ¥7,140. Sakura + Special Rapid from Shin-Osaka: ¥6,270 (18:14 → Kyoto 19:44)")],
                   tip=T("時刻と運賃は乗換案内（2026年11月25日（水））で確認しました。", "Times and fares were checked on a route planner for Wednesday 25 November 2026."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = PHOTOS[out["id"]]
    assert out["photos"], out["id"]
    for p in out["photos"]:
        f = p if isinstance(p, str) else p["file"]
        assert os.path.exists(f"{IMG}/{f}"), f
    out.setdefault("notices", [])
    spots.append(out)
NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
OKA = [NO[k] for k in ("tram", "castle", "tsukimi", "korakuen")]
KURA = [NO[k] for k in ("bikan", "ohara", "boat", "ivy", "honmachi", "achi")]

data = {
    "id": "okayama",
    "_note": "岡山と倉敷のルート（okayama/ のページ専用。形は eizan-line.json と同じ）。京都駅→（新幹線）岡山駅→路面電車→岡山城→月見橋→後楽園→（吉備津神社）→（JR）倉敷→倉敷川・大原美術館・川舟・アイビースクエア・本町東町・阿智神社→倉敷駅→京都。"
             "オーナーの写真は岡山城と月見橋（2021年3月9日）、岡山駅（2021年・2023年・2025年）、路面電車（2023年8月6日）だけ。"
             "後楽園・吉備津神社・倉敷と、改修後の岡山城は Wikimedia Commons の写真（photos の要素が {file, credit}。一覧は scripts/okayama_web_photos.json。ライセンスは Commons の API で2026年11月21日に確認）。"
             "info.checked は事実情報を確認した日（各施設の公式サイト、乗換案内）。倉紡記念館の時間と料金、倉敷民藝館などの料金は確認できず要確認。このファイルは scripts/build_okayama_data.py で作る。",
    "sections": [{"first": 1, "last": NO["korakuen"], "day": 0}, {"first": NO["kibitsu"], "last": NO["kibitsu"], "day": 1}, {"first": NO["lunch"], "last": NO["kaeri"], "day": 2}],
    "focus": {"first": 2, "last": NO["kaeri"]},
    "plan": {"_note": "「選んで回る」の設定。京都駅と岡山駅は必ず入る。倉敷駅（行きのお昼・帰り）は倉敷の場所をどれか選ぶと入る。",
             "picks": OKA + [NO["kibitsu"]] + KURA,
             "auto": {str(NO["kyoto"]): {"always": True}, str(NO["okayamaeki"]): {"always": True},
                      str(NO["lunch"]): {"any": KURA}, str(NO["kaeri"]): {"any": KURA}},
             "hints": [
                 H("kibitsu", {"any": [NO["kibitsu"]], "andAny": [NO["ohara"]], "none": []},
                   "吉備津神社に寄ると、倉敷に着くのは14:07です。大原美術館の入館は16:30まで（12〜2月は14:30まで）なので、着いたらお昼の前に美術館へ。川舟は外すか、16:00以降の便を先にWEB予約してください。",
                   "With Kibitsu Shrine you reach Kurashiki at 14:07. Last entry to the Ohara Museum is 16:30 (14:30 from December to February), so go to the museum before eating. Drop the boat, or book a boat after 16:00 online beforehand."),
                 H("kibitsu", {"any": [NO["kibitsu"]], "none": KURA},
                   "倉敷に行かない日は、吉備津神社でゆっくりできます。帰りは吉備津発 14:17 か 15:17 で岡山へ。",
                   "Not going to Kurashiki? Then take your time at Kibitsu Shrine and come back to Okayama on the 14:17 or 15:17."),
                 H("lunch", {"any": KURA, "none": OKA + [NO["kibitsu"]]},
                   "倉敷だけの日は、岡山駅で新幹線から在来線に乗り換えて、そのまま倉敷へ（岡山8:41着なら、倉敷に9:15ごろ）。9:00から倉敷館で川舟の当日券を売っています。大原美術館も9:00から。",
                   "Kurashiki only? Change from the Shinkansen to a local train at Okayama and go straight there (arriving Okayama 8:41, you are in Kurashiki by about 9:15). Same-day boat tickets go on sale at Kurashiki-kan at 9:00, and the Ohara Museum opens at 9:00 too."),
                 H("boat", {"any": [NO["boat"]], "none": []},
                   "川舟は、京都を出る前にWEB予約を（乗る日の30日前から）。午後に着いてからの当日券は、売り切れていることが多いです。",
                   "Book the boat online before you leave Kyoto (from 30 days ahead). Same-day tickets are often gone by the time you arrive in the afternoon."),
                 H("castle", {"any": [NO["castle"]], "andAny": [NO["korakuen"]], "none": []},
                   "岡山城と後楽園の両方に入るなら、共通券（800円）を。別々だと1,000円です。",
                   "Going into both the castle and Korakuen? Buy the combined ticket (¥800) instead of ¥1,000 separately."),
                 H("korakuen", {"any": [NO["korakuen"]], "none": [NO["castle"], NO["tsukimi"]]},
                   "後楽園だけなら、城下電停から鶴見橋を渡って正門へ（歩いて約10分）。岡山駅前から正門前までのバスもあります。",
                   "Korakuen only? From the Shiroshita tram stop cross Tsurumi bridge to the main gate (about 10 min on foot). There are also buses from Okayama Station to the main gate."),
                 H("achi", {"any": [NO["achi"]], "none": []},
                   "秋と冬は17時ごろに暗くなります。阿智神社は、本町・東町より先に上ってください。",
                   "In autumn and winter it is dark by about 17:00. Climb to Achi Shrine before walking Honmachi and Higashimachi."),
             ]},
    "photoBase": "../images/okayama/",
    "spots": spots,
}
for h in data["plan"]["hints"]:
    if h["rule"].get("none") == []:
        del h["rule"]["none"]
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
