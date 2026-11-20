#!/usr/bin/env python3
"""京都から日帰り 姫路・明石・須磨のデータ（data/routes/himeji.json）を書き出す。

使い方: python3 scripts/build_himeji_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/himeji/<スポットのid>-<番号>.jpg を番号の順に全部使う
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/himeji"
OUT = f"{R}/data/routes/himeji.json"
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


def photos(pid, extra=None):
    # extra: ネットから借りた写真（{"file", "credit": {"author", "license", "page"}}）。写真の上に撮影者とライセンスが出る
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    return own + (extra or [])


def cc(file, author, license, title):
    return {"file": file, "credit": {"author": author, "license": license, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}




JR = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
TRAIN_TIP = T("時刻と運賃は乗換案内（2026年11月の土曜のダイヤ）で確認しました。乗る前にもう一度確かめてください。",
              "Times and fares checked on a route planner (Saturday timetable, November 2026). Please check again before you travel.")

S = [
    dict(id="himejieki", name=T("JR姫路駅", "JR Himeji Station"), kind=T("駅（スタート）", "Station (start)"),
         blurb=T("京都から新快速で1時間36分、乗り換えなし。駅の北口を出ると、大通りの先に白い天守が見えます。",
                 "1 h 36 min from Kyoto by Special Rapid, no change. Out of the north exit, the white keep stands at the end of the main street."),
         lat=34.82800, lng=134.69006,
         text=T("JR姫路駅（ひめじえき）\n\n京都からJRの新快速で乗り換えなし。京都8:14発に乗ると、姫路に9:50に着きます（2,210円）。急ぐなら新幹線で約50分（自由席4,740円）。\n\n"
                "北口を出ると、まっすぐ延びる大手前通りの先に姫路城が見えます。お城の入口までは歩いて約20分。神姫バスで「大手門前」まで行き、歩いて5分という行き方もあります。写真は、お城の入口（大手門）近くのお堀から見た天守です。\n\nおすすめ到着時間：9:50",
                "JR Himeji Station\n\nDirect from Kyoto on the JR Special Rapid: leave at 8:14 and arrive at 9:50 (¥2,210). In a hurry, the Shinkansen takes about 50 minutes (¥4,740 unreserved).\n\n"
                "From the north exit, the castle stands at the end of the straight Otemae-dori. It’s about 20 minutes on foot to the entrance, or take a Shinki bus to “Otemon-mae” and walk 5 minutes. The photo shows the keep from the moat near the castle entrance (Otemon gate).\n\nRecommended arrival: 9:50"),
         gmaps=[gm("JR姫路駅", "JR Himeji Station", 34.82800, 134.69006, "JR姫路駅")],
         links=[JR],
         info=info([row("train", "京都8:14発（JR新快速）→ 姫路9:50着（乗り換えなし）", "Kyoto 8:14 (JR Special Rapid) → Himeji 9:50 (direct)"),
                    row("fee", "京都→姫路 2,210円（新幹線の自由席なら4,740円）", "Kyoto → Himeji ¥2,210 (¥4,740 by Shinkansen, unreserved)")],
                   tip=TRAIN_TIP)),
    dict(id="himejijo", name=T("姫路城", "Himeji Castle"), kind=T("城（世界遺産）", "Castle (World Heritage)"),
         blurb=T("白鷺城とも呼ばれる、真っ白な天守。木造の大天守の中を、急な階段で最上階まで上ります。",
                 "The brilliant white keep, nicknamed the White Heron. Climb steep wooden stairs inside the great keep to the top floor."),
         lat=34.83933, lng=134.69402,
         text=T("姫路城（ひめじじょう）\n\n江戸時代のはじめに建てられた天守が今も残る、世界遺産のお城です。白い漆喰の壁から「白鷺城（しらさぎじょう）」とも呼ばれます。"
                "菱の門から曲がりくねった坂と門をいくつも抜けて、大天守へ。中は木の柱と床がそのまま残り、急な階段で6階の最上階まで上れます。最上階の窓からは、姫路の町がまっすぐ駅まで見通せます。\n\n"
                "建物の中は靴を脱いで上がります（靴を入れる袋をもらえます）。西の丸の長い廊下「百間廊下」も見ておきたい所です。\n\n"
                "入城料は、2026年3月から姫路市外の大人が2,500円になりました。お城と好古園の共通券（2,600円）もあります。\n\nおすすめ訪問時間：10:10〜11:50",
                "Himeji Castle\n\nA World Heritage castle whose early-Edo keep still stands. Its white plaster walls earned it the name “White Heron Castle”. "
                "From the Hishi gate, wind up through slopes and gates to the great keep. Inside, the original wooden pillars and floors remain, and steep stairs lead to the sixth, top floor, with a view straight down the city to the station.\n\n"
                "Shoes come off inside (you’re given a bag for them). Don’t miss the long corridor of the West Bailey, the Hyakken Roka.\n\n"
                "Since March 2026, admission for adults who don’t live in Himeji is ¥2,500. A combined ticket with Kokoen garden is ¥2,600.\n\nRecommended visit time: 10:10–11:50"),
         gmaps=[gm("姫路城", "Himeji Castle", 34.83933, 134.69402, "姫路城")],
         links=[link("official", "姫路城 公式サイト", "Himeji Castle (official)", "https://www.himejicastle.jp/")],
         info=info([row("hours", "9:00〜17:00（入城は16:00まで）", "9:00–17:00 (last entry 16:00)"),
                    row("closed", "12月29日・30日", "29–30 December"),
                    row("fee", "18歳以上 2,500円（姫路市民は1,000円）、18歳未満は無料。好古園との共通券 2,600円", "Ages 18+ ¥2,500 (¥1,000 for Himeji residents); under 18 free. Combined ticket with Kokoen ¥2,600")],
                   tip=T("時間と料金は姫路城の公式サイトで確認しました。", "Hours and fees checked on the official Himeji Castle website."))),
    dict(id="kokoen", name=T("好古園", "Kokoen Garden"), kind=T("日本庭園", "Japanese garden"),
         blurb=T("お城の西の、9つの庭がつながる日本庭園。池の向こうに、天守が顔をのぞかせます。",
                 "Nine linked gardens just west of the castle, with the keep peeking over the pond."),
         lat=34.83797, lng=134.68961,
         text=T("好古園（こうこえん）\n\n姫路城の西の御屋敷跡に造られた、9つの庭からなる日本庭園です。池泉回遊式の「御屋敷の庭」では、池の向こうに天守が見えます。入口はお城の有料区域とは別です。\n\n"
                "写真は2024年9月の夜に撮ったもの。2026年秋は11月17日〜12月6日に夜間開園があり、20:00まで紅葉のライトアップが楽しめます。\n\n"
                "見終わったら駅へ戻り（歩いて約15分）、新快速で明石へ（姫路12:57発→明石13:20着・660円）。\n\nおすすめ訪問時間：11:55〜12:35",
                "Kokoen Garden\n\nNine gardens laid out on the site of the lords’ residences west of Himeji Castle. In the pond garden of the main residence, the keep rises beyond the water. The entrance is separate from the castle’s paid area.\n\n"
                "The photos were taken on an evening in September 2024. In autumn 2026 the garden opens in the evening from 17 November to 6 December, with the autumn leaves lit up until 20:00.\n\n"
                "Then walk back to the station (about 15 minutes) and take the Special Rapid to Akashi (Himeji 12:57 → Akashi 13:20, ¥660).\n\nRecommended visit time: 11:55–12:35"),
         gmaps=[gm("好古園", "Kokoen", 34.83797, 134.68961, "好古園 姫路")],
         links=[link("official", "好古園 公式サイト", "Kokoen (official, Japanese)", "https://himeji-machishin.jp/ryokka/kokoen/")],
         info=info([row("hours", "9:00〜17:00（入園は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                    row("hours", "2026年秋の夜間開園：11月17日〜12月6日、20:00まで（入園19:30まで）", "Autumn 2026 evening opening: 17 Nov – 6 Dec, until 20:00 (last entry 19:30)", until="2026-12-06"),
                    row("closed", "12月29日・30日", "29–30 December"),
                    row("fee", "大人400円、18歳未満は無料（姫路城との共通券 2,600円）", "¥400 adults, under 18 free (combined ticket with the castle ¥2,600)"),
                    row("train", "姫路12:57発（新快速）→ 明石13:20着・660円", "Himeji 12:57 (Special Rapid) → Akashi 13:20, ¥660")],
                   tip=T("時間と料金は好古園の公式サイト、電車は乗換案内で確認しました。", "Hours and fees checked on the Kokoen website; trains on a route planner."))),
    # 書写山 圓教寺は Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    dict(id="shosha", name=T("書写山 圓教寺", "Mt. Shosha Engyo-ji"), kind=T("寺・ロープウェイ", "Temple & ropeway"),
         blurb=T("ロープウェイで上る、山の上の大きなお寺。崖に張り出した摩尼殿と、3つのお堂が広場を囲む「三之堂」が見どころです。行くなら半日かかります。",
                 "A big temple on a mountaintop, reached by ropeway. See Mani-den, built out over a cliff, and the three halls around a courtyard. Allow half a day."),
         lat=34.89143, lng=134.65754,
         text=T("書写山 圓教寺（しょしゃざん えんぎょうじ）\n\n姫路の町の北西、書写山の上にある天台宗のお寺です。西国三十三所の27番札所。ふもとからロープウェイで約4分上り、観音像が並ぶ参道を歩きます。\n\n"
                "最初に着くのが、崖に張り出すように建つ摩尼殿（まにでん）。そこから歩いて5〜6分の「三之堂（みつのどう）」は、大講堂・食堂（じきどう）・常行堂の3つのお堂が広場を囲む場所で、映画「ラスト サムライ」の撮影にも使われました（書写山ロープウェイの公式サイトより）。\n\n"
                "山上駅から摩尼殿までは約1km、歩いて15〜20分。志納所の前から摩尼殿の下まで、お寺のマイクロバス（往復500円）もあります。摩尼殿・三之堂・奥之院を回って約2時間が、お寺の案内している目安です。山道なので歩きやすい靴で。\n\n"
                "バスとロープウェイは、姫路駅前の神姫バス案内所で売っているセット券（1,700円）が、別々に払うより140円安くなります。お城へ行く前に買っておきましょう。\n\n"
                "好古園を出たら、すぐ前のバス停「聴覚特別支援学校・好古園」から神姫バスで書写山ロープウェイへ（12:40発→13:07着・320円）。帰りは書写山ロープウェイ16:32発のバスで姫路駅北口に17:02着、17:11発の新快速で京都に18:44に着きます。\n\n"
                "書写山まで行くと、姫路で1日がほぼ終わります。須磨浦山上遊園（最終入場16:30）には間に合いません。\n\nおすすめ訪問時間：13:10〜16:30",
                "Mt. Shosha Engyo-ji\n\nA Tendai temple on top of Mt. Shosha, north-west of Himeji, and No. 27 on the Saigoku Kannon pilgrimage. A ropeway takes about 4 minutes from the foot; from there you walk an approach lined with Kannon statues.\n\n"
                "First comes Mani-den, built out over a cliff. Five or six minutes further on are the Mitsu-no-do, three halls (the lecture hall, the long Jikido and the Jogyodo) around a courtyard, where scenes of “The Last Samurai” were filmed (according to the ropeway’s website).\n\n"
                "From the top station to Mani-den is about 1 km, 15–20 minutes on foot. The temple also runs a minibus from the entrance to just below Mani-den (¥500 return). The temple suggests about 2 hours for Mani-den, the three halls and the inner sanctuary. It’s a mountain path, so wear good shoes.\n\n"
                "The bus-and-ropeway set ticket (¥1,700), sold at the Shinki Bus office in front of Himeji Station, is ¥140 cheaper than paying separately. Buy it before you go to the castle.\n\n"
                "After Kokoen, take the Shinki bus from the stop right outside (“Chokaku Tokubetsu Shien Gakko / Kokoen”) to Shoshazan Ropeway (12:40 → 13:07, ¥320). Coming back, the 16:32 bus reaches Himeji Station north exit at 17:02, and the 17:11 Special Rapid gets to Kyoto at 18:44.\n\n"
                "Going up Mt. Shosha takes most of the rest of your day in Himeji. You won’t make Sumaura Sanjo Yuen (last entry 16:30).\n\nRecommended visit time: 13:10–16:30"),
         gmaps=[gm("圓教寺 摩尼殿", "Engyo-ji Mani-den", 34.89143, 134.65754, "書写山圓教寺 摩尼殿"),
                gm("書写山ロープウェイ（山麓駅）", "Shoshazan Ropeway (bottom station)", 34.87839, 134.66768, "書写山ロープウェイ 山麓駅")],
         links=[link("official", "書写山ロープウェイ 公式サイト（時刻・料金）", "Shoshazan Ropeway (official, Japanese)", "https://www.mt-shosha.info/category/charge/index.html"),
                link("official", "書寫山圓教寺 公式サイト（アクセス）", "Engyo-ji (official, Japanese)", "http://www.shosha.or.jp/access/"), JR],
         notices=[{"from": None, "to": "2027-10-28", "url": "https://www.mt-shosha.info/",
                   "head": T("ロープウェイは2027年2月5日〜10月28日 運休", "Ropeway closed 5 Feb – 28 Oct 2027"),
                   "text": T("大規模改修のため、書写山ロープウェイは2027年2月5日から10月28日まで運休します。お寺のマイクロバスも運休。圓教寺は開いていますが、登山道を歩いて上ります（片道30分〜1時間。圓教寺の公式サイトより）。",
                             "The ropeway is closed for major renovation from 5 February to 28 October 2027, and the temple minibus stops too. Engyo-ji stays open, but you have to walk up a trail (30 minutes to 1 hour each way, according to the temple).")}],
         info={"rows": [row("hours", "ロープウェイ 8:30から15分おき（毎時0・15・30・45分発）。下りの最終は、10月11日〜2月末が17:00（10月11日〜11月30日の日曜・祝日は18:00）、3月1日〜10月10日が18:00（4月1日〜10月10日の日曜・祝日は19:00）",
                            "Ropeway from 8:30, every 15 minutes. Last car down: 17:00 from 11 Oct to end of Feb (18:00 on Sundays and holidays 11 Oct – 30 Nov); 18:00 from 1 Mar to 10 Oct (19:00 on Sundays and holidays 1 Apr – 10 Oct)"),
                        row("hours", "2026年11月21日〜23日は「書写山もみじまつり」。文化財の特別公開10:00〜16:00、紅葉のライトアップ17:00〜20:00（ロープウェイの下りは20:30まで）",
                            "21–23 Nov 2026: Shoshazan Momiji Festival. Special openings 10:00–16:00, autumn-leaf illumination 17:00–20:00 (ropeway down until 20:30)", until="2026-11-23"),
                        row("closed", "ロープウェイは例年2月ごろ点検で運休。2027年は2月5日〜10月28日、改修工事で運休", "The ropeway closes for inspection around February each year; in 2027 it is closed 5 Feb – 28 Oct for renovation"),
                        row("fee", "ロープウェイ 往復1,200円・片道700円（小人は半額）。圓教寺の志納金 中学生以上800円・小学生500円。山上のマイクロバス 往復500円",
                            "Ropeway ¥1,200 return, ¥700 one way (children half). Temple admission ¥800 (junior high and up), ¥500 elementary. Minibus on the mountain ¥500 return"),
                        row("fee", "書写山ロープウェイ＋バス往復セット乗車券 1,700円（姫路駅前の神姫バス案内所で販売。別々に払うと1,840円）",
                            "Ropeway + return bus set ticket ¥1,700, sold at the Shinki Bus office in front of Himeji Station (¥1,840 if paid separately)"),
                        row("train", "神姫バス：聴覚特別支援学校・好古園 12:40発 → 書写山ロープウェイ 13:07着・320円。姫路駅北口からは10番のりばで約25〜30分・320円",
                            "Shinki bus: Kokoen stop 12:40 → Shoshazan Ropeway 13:07, ¥320. From Himeji Station north exit, stop 10, about 25–30 min, ¥320"),
                        row("train", "帰り：書写山ロープウェイ16:32発（バス）→ 姫路駅北口17:02着、姫路17:11発（新快速）→ 京都18:44着。バス320円＋JR 2,210円",
                            "Return: bus from Shoshazan Ropeway 16:32 → Himeji Station north exit 17:02; Himeji 17:11 (Special Rapid) → Kyoto 18:44. Bus ¥320 + JR ¥2,210")],
               "cash": False, "checked": "2026-11-21",
               "tip": T("2026年11月21日に確認しました。ロープウェイの時刻・料金とセット券は書写山ロープウェイの公式サイト、志納金とマイクロバスは圓教寺の公式サイト、バスと電車は乗換案内（2026年11月の土曜のダイヤ）から。圓教寺の拝観時間は公式サイトに書かれていないので、ロープウェイの時間に合わせてください（要確認）。",
                        "Checked on 21 November 2026: ropeway times, fares and the set ticket on the ropeway’s website; admission and the minibus on the temple’s website; buses and trains on a route planner (Saturday timetable, November 2026). The temple’s own opening hours are not given on its website, so plan around the ropeway (please check).")},
         _extra=[cc("shosha-1.jpg", "663highland", "CC BY 2.5", "File:Engyoji01s4592.jpg"),
                 cc("shosha-2.jpg", "663highland", "CC BY 2.5", "File:Engyoji05s4592.jpg"),
                 cc("shosha-3.jpg", "663highland", "CC BY 2.5", "File:Engyoji45n4592.jpg"),
                 cc("shosha-4.jpg", "Umako", "CC0", "File:Himeji City Mt. Shosha Ropeway 250506.jpg")]),
    dict(id="akashi", name=T("明石 魚の棚と「たこ磯」の明石焼", "Akashi: Uonotana market & Takoiso akashiyaki"), kind=T("市場・ランチ", "Market & lunch"),
         blurb=T("明石駅のすぐ南の、明石だこと魚の商店街。お昼はたこ磯で、だし汁につけて食べる明石焼（玉子焼）を。",
                 "The fish-and-octopus arcade just south of Akashi Station. Lunch is akashiyaki (tamagoyaki) at Takoiso, dipped in dashi."),
         lat=34.64701, lng=134.99213,
         text=T("魚の棚（うおんたな）商店街と、たこ磯（たこいそ）\n\n明石駅から南へ歩いて3分。明石の海でとれた魚やたこ、干物やかまぼこの店が並ぶアーケードの商店街です。お昼ごろからは、その日の昼にとれた魚「昼網」も並びます。\n\n"
                "お昼は、商店街の中ほど、弁天さまの隣にある「たこ磯」へ。白いのれんに赤い字で「玉子焼」。明石では明石焼のことを玉子焼と呼びます。ふわふわの玉子焼を、温かいだし汁につけて食べます。\n\n"
                "木曜日は競りがないので、休む店が多くなります。明石駅の北口から歩いて5分の所には、明石城跡（明石公園）もあります。\n\n食べたら山陽電車の山陽明石駅から須磨浦公園へ（14:40発→14:55着・390円）。\n\nおすすめ訪問時間：13:25〜14:35",
                "Uonotana market and Takoiso\n\nThree minutes’ walk south of Akashi Station: an arcade of shops selling fish and octopus from the Akashi sea, dried fish and fish cakes. From around midday the day’s midday catch, “hiruami”, is on sale too.\n\n"
                "For lunch, go to Takoiso, halfway along next to the little Benten shrine: white curtain, red letters, 玉子焼. In Akashi, akashiyaki is called tamagoyaki. Dip the fluffy dumplings in warm dashi.\n\n"
                "Many shops close on Thursdays, when there is no fish auction. Akashi Castle ruins (Akashi Park) are 5 minutes’ walk from the north exit of Akashi Station.\n\nAfterwards take the Sanyo Railway from Sanyo-Akashi to Sumaura-koen (14:40 → 14:55, ¥390).\n\nRecommended visit time: 13:25–14:35"),
         gmaps=[gm("魚の棚商店街", "Uonotana", 34.64701, 134.99213, "魚の棚商店街 明石"), gm("たこ磯", "Takoiso", 34.64696, 134.99289, "たこ磯 明石 本町")],
         links=[link("official", "魚の棚商店街 公式サイト", "Uonotana shopping street (official, Japanese)", "https://www.uonotana.or.jp/"),
                link("info", "たこ磯（魚の棚商店街のお店のページ）", "Takoiso (shop page on the Uonotana site, Japanese)", "https://www.uonotana.or.jp/shop-057.html")],
         info=info([row("hours", "たこ磯（本店）10:00〜19:00、定休日なし。魚の棚の営業時間は店ごとに違います", "Takoiso (main shop) 10:00–19:00, open daily. Uonotana shop hours vary"),
                    row("closed", "魚の棚は木曜に休む店が多い", "Many Uonotana shops close on Thursdays"),
                    row("train", "山陽明石14:40発 → 須磨浦公園14:55着・390円（途中で1回乗り換え）", "Sanyo-Akashi 14:40 → Sumaura-koen 14:55, ¥390 (one change)")],
                   tip=T("魚の棚商店街の公式サイトで確認しました。たこ磯の値段は資料によって違うので、書いていません。", "Checked on the Uonotana website. Takoiso’s prices differ between sources, so they are not given here."))),
    dict(id="suma", name=T("須磨浦公園（須磨浦山上遊園）", "Sumaura Park (Sumaura Sanjo Yuen)"), kind=T("ロープウェー・展望台", "Ropeway & lookout"),
         blurb=T("ロープウェーと、乗り心地がびっくりなカーレーターで山の上へ。回る喫茶店から、須磨の海と明石海峡大橋が見えます。",
                 "Up by ropeway and the bumpy “Car-rator” to a hilltop. From the revolving café, look over the Suma sea and the Akashi Kaikyo Bridge."),
         lat=34.63784, lng=135.10022,
         text=T("須磨浦公園（すまうらこうえん）と須磨浦山上遊園\n\n山陽電車の須磨浦公園駅を出てすぐ、ロープウェーで鉢伏山へ上ります。窓の外には須磨の海岸と神戸の街。"
                "山上駅からは、ベルトコンベアの上の小さなカゴに乗って進む「カーレーター」で、さらに上の回転展望閣へ。ガタガタ揺れる乗り心地は、ここでしか味わえません。\n\n"
                "回転展望閣の3階の喫茶コスモスは、床がゆっくり回ります（約55分で1回転）。晴れた日は、明石海峡大橋や関西空港まで見えます。喫茶コスモスのラストオーダーは15:30、展望閣の屋上は16:20までなので、着いたら先に展望閣へ。\n\n"
                "最終入場は16:30。火曜日が休みです。帰りは須磨浦公園16:26発の山陽電車で舞子公園へ（16:41着・250円）。\n\nおすすめ訪問時間：15:00〜16:25",
                "Sumaura Park and Sumaura Sanjo Yuen\n\nRight outside Sanyo Railway’s Sumaura-koen Station, a ropeway climbs Mt. Hachibuse, with the Suma beach and Kobe below. "
                "From the top station, the “Car-rator”, little baskets riding on a conveyor belt, carries you up to the revolving observatory. Its rattling ride is like nothing else.\n\n"
                "Café Cosmos on the third floor of the observatory slowly revolves (about 55 minutes a turn). On clear days you can see the Akashi Kaikyo Bridge and even Kansai Airport. Café Cosmos takes last orders at 15:30 and the observatory roof closes at 16:20, so head up to the observatory first.\n\n"
                "Last entry is 16:30; closed on Tuesdays. Then take the 16:26 Sanyo train to Maiko-koen (arr. 16:41, ¥250).\n\nRecommended visit time: 15:00–16:25"),
         gmaps=[gm("須磨浦公園駅", "Sumaura-koen Station", 34.63784, 135.10022, "須磨浦公園駅"), gm("須磨浦山上遊園", "Sumaura Sanjo Yuen", 34.64190, 135.09421, "須磨浦山上遊園")],
         links=[link("official", "須磨浦山上遊園 公式サイト", "Sumaura Sanjo Yuen (official, Japanese)", "https://www.sumaura-yuen.jp/")],
         notices=[{"from": None, "to": "2027-02-05", "url": "https://www.sumaura-yuen.jp/event/entry-709.html",
                   "text": T("2026年12月2日〜2027年2月5日は土日祝だけの営業です（正月三が日は営業。12/12・13・19・20、1/16・17は休園）。",
                             "From 2 December 2026 to 5 February 2027 it opens on weekends and holidays only (open over New Year; closed 12, 13, 19, 20 Dec and 16, 17 Jan).")}],
         info=info([row("hours", "10:00〜17:00（最終入場16:30）。ロープウェーは毎時0・15・30・45分発", "10:00–17:00 (last entry 16:30). Ropeway every 15 minutes"),
                    row("hours", "喫茶コスモス 10:10〜16:30（ラストオーダー15:30）。展望閣の屋上 10:10〜16:20", "Café Cosmos 10:10–16:30 (last orders 15:30). Observatory roof 10:10–16:20"),
                    row("closed", "火曜日（祝日は営業）", "Tuesdays (open on holidays)"),
                    row("fee", "ロープウェー 往復920円、カーレーター 往復550円、喫茶コスモスの入場200円。回遊券 Bコース1,500円・Aコース（リフトも）2,100円",
                        "Ropeway ¥920 return, Car-rator ¥550 return, Café Cosmos entry ¥200. Round tickets: B course ¥1,500, A course (with chairlift) ¥2,100"),
                    row("train", "須磨浦公園16:26発（山陽電車）→ 舞子公園16:41着・250円", "Sumaura-koen 16:26 (Sanyo) → Maiko-koen 16:41, ¥250")],
                   tip=T("時間と料金は須磨浦山上遊園の公式サイトで確認しました。", "Hours and fees checked on the official website."))),
    dict(id="maiko", name=T("舞子公園・明石海峡大橋", "Maiko Park & Akashi Kaikyo Bridge"), kind=T("公園・夕日", "Park & sunset"),
         blurb=T("世界最大級のつり橋のたもとで、海に沈む夕日を。駅から歩いてすぐです。",
                 "Watch the sun go down by one of the world’s longest suspension bridges, a few minutes from the station."),
         lat=34.63275, lng=135.03300,
         text=T("舞子公園（まいここうえん）と明石海峡大橋\n\nJR舞子駅・山陽電車の舞子公園駅から南へ歩いて約5分。淡路島へ渡る明石海峡大橋の真下の海辺の公園です。"
                "橋の向こうに淡路島が見え、夕日は西の海に沈みます。橋の桁の中に入れる「舞子海上プロムナード」もあります。\n\n"
                "帰りはJR舞子駅から京都へ。17:38発に乗ると、途中で新快速に乗り換えて京都に18:59に着きます（1,640円）。\n\nこの時間で夕日に間に合うのは秋から冬です。夏は日の入りが19時ごろなので、帰りの電車を遅らせましょう。\n\nおすすめ訪問時間：16:45〜17:30",
                "Maiko Park and the Akashi Kaikyo Bridge\n\nAbout 5 minutes south of JR Maiko and Sanyo Maiko-koen stations: a seaside park right under the Akashi Kaikyo Bridge to Awaji Island. "
                "Awaji lies beyond the bridge and the sun goes down into the sea to the west. You can also walk inside the bridge girders on the Maiko Marine Promenade.\n\n"
                "Go home from JR Maiko: the 17:38, changing to the Special Rapid on the way, reaches Kyoto at 18:59 (¥1,640).\n\nThese times catch the sunset in autumn and winter. In summer the sun sets around 19:00, so take a later train.\n\nRecommended visit time: 16:45–17:30"),
         gmaps=[gm("舞子公園", "Maiko Park", 34.63275, 135.03300, "舞子公園"), gm("JR舞子駅", "JR Maiko Station", 34.63351, 135.03382, "JR舞子駅")],
         links=[link("official", "舞子公園 公式サイト", "Maiko Park (official, Japanese)", "https://hyogo-maikopark.jp/"), JR],
         info=info([row("hours", "舞子海上プロムナード 9:00〜18:00（最終入館は30分前）", "Maiko Marine Promenade 9:00–18:00 (last entry 30 min before)"),
                    row("closed", "プロムナード：10〜3月は第2月曜（祝日なら翌日）、12月29日〜31日", "Promenade: 2nd Monday Oct–Mar (next day if a holiday), 29–31 Dec"),
                    row("fee", "プロムナード 大人 平日250円・土日祝300円（高校生以下は無料）", "Promenade ¥250 weekdays, ¥300 weekends and holidays (free for high school and under)"),
                    row("train", "帰り：舞子17:38発 → 京都18:59着・1,640円（途中で新快速に乗り換え）", "Return: Maiko 17:38 → Kyoto 18:59, ¥1,640 (change to the Special Rapid on the way)")],
                   tip=T("舞子公園の公式サイトと乗換案内で確認しました。", "Checked on the Maiko Park website and a route planner."))),
]

spots = []
for i, s in enumerate(S, 1):
    s = dict(s)
    out = {"no": i, "id": s.pop("id")}
    out.update(s)
    out["photos"] = photos(out["id"], out.pop("_extra", None))
    out.setdefault("notices", [])
    spots.append(out)

NO = {s["id"]: s["no"] for s in spots}
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}
data = {
    "id": "himeji",
    "_note": "京都から日帰り 姫路・明石・須磨のルート（himeji/ のページ専用。形は eizan-line.json と同じ）。京都から新快速で姫路へ、姫路城と好古園→新快速で明石（魚の棚・たこ磯の明石焼）→山陽電車で須磨浦公園（ロープウェー・カーレーター）→舞子公園で明石海峡大橋の夕日→JR舞子駅から京都へ。"
             "写真は Toshi の写真ライブラリから選んだもの（須磨浦公園と明石は2023年6月16日の Nikon D7000、姫路城は2023年6月と2024年8・9月、好古園は2024年9月の夜、舞子は2023年7月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "書写山 圓教寺（2026-11-21 追加）は Toshi がまだ行っていない場所で、写真は Wikimedia Commons（photos の要素が {file, credit}）、文章は公式サイトの情報だけ。"
             "info.checked は事実情報を確認した日（各施設・商店街の公式サイト、電車は乗換案内）。このファイルは scripts/build_himeji_data.py で作る。",
    "sections": [{"first": 1, "last": 3, "day": 0},
                 {"first": NO["shosha"], "last": NO["shosha"], "area": T("書写山", "Mt. Shosha"), "title": T("ロープウェイで山の上のお寺へ", "Up the ropeway to a mountain temple")},
                 {"first": NO["akashi"], "last": NO["akashi"], "day": 1}, {"first": NO["suma"], "last": NO["suma"], "day": 2}, {"first": NO["maiko"], "last": NO["maiko"], "day": 3}],
    "plan": {"_note": "「選んで回る」の設定。姫路駅は姫路城・好古園・書写山のどれかを選ぶと入る。書写山は半日かかるので、須磨・舞子とは一緒に回れない（hints に書いてある）。defaultMode: pick で最初から「選んで回る」。",
             "defaultMode": "pick",
             "picks": [NO[k] for k in ("himejijo", "kokoen", "shosha", "akashi", "suma", "maiko")],
             "auto": {str(NO["himejieki"]): {"any": [NO["himejijo"], NO["kokoen"], NO["shosha"]]}},
             "hints": [
                 H("shosha", {"any": [NO["shosha"]], "andAny": [NO["suma"]]},
                   "書写山と須磨浦山上遊園（最終入場16:30）は、同じ日には回れません。どちらかにしてください。",
                   "Mt. Shosha and Sumaura Sanjo Yuen (last entry 16:30) don’t fit in the same day. Choose one."),
                 H("shosha", {"any": [NO["shosha"]], "andAny": [NO["akashi"], NO["maiko"]]},
                   "書写山のあとは、姫路17:11発の新快速で明石に17:35着。たこ磯は19:00までなので、明石焼は夕ごはんに。舞子の夕日は、秋と冬は日の入りが17時ごろなので間に合いません。",
                   "After Mt. Shosha, the 17:11 Special Rapid from Himeji reaches Akashi at 17:35. Takoiso is open until 19:00, so have akashiyaki for dinner. In autumn and winter the sun sets around 17:00, so you’ll miss the sunset at Maiko."),
                 H("shosha", {"any": [NO["shosha"]], "none": [NO["himejijo"], NO["kokoen"]]},
                   "お城に寄らない日は、姫路駅北口の10番のりばから神姫バスで書写山ロープウェイへ（約25〜30分・320円）。",
                   "Skipping the castle? Take the Shinki bus from stop 10 at Himeji Station north exit to Shoshazan Ropeway (about 25–30 min, ¥320)."),
                 H("akashi", {"any": [NO["akashi"]], "none": [NO["himejijo"], NO["kokoen"], NO["shosha"]]},
                   "姫路に寄らない日は、京都から新快速で明石へ直接行けます（乗り換えなし）。", "Skipping Himeji? The Special Rapid from Kyoto stops at Akashi (no change)."),
                 H("suma", {"any": [NO["suma"]], "none": [NO["maiko"]]},
                   "舞子に寄らない日は、須磨浦公園駅から山陽電車・阪急で京都河原町へ（約1時間45分・1,050円）。JR京都駅へは山陽電車と阪急で三宮へ出て新快速に乗り換え（1,510円）。",
                   "Not going to Maiko? From Sumaura-koen take the Sanyo and Hankyu lines to Kyoto-Kawaramachi (about 1 h 45 min, ¥1,050), or go to Sannomiya and change to the JR Special Rapid for Kyoto Station (¥1,510)."),
             ]},
    "photoBase": "../images/himeji/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
