#!/usr/bin/env python3
"""姫路・明石・須磨（梅田〜難波のホテルから1日）のデータを書き出す。コースごとに1ファイル。

使い方: python3 scripts/build_himeji_data.py   （そのあと python3 scripts/sync_himeji.py）
- data/routes/himeji.json        … 「9〜10時に出発」（須磨浦山上遊園→明石でお昼→14時半ごろの姫路城→好古園→夕暮れのお城と晩ごはん→姫路から帰る）
- data/routes/himeji-early.json  … 「開城に合わせる」（姫路城の9:00の開城へ→好古園でひと休み→明石で遅いお昼→須磨浦山上遊園→舞子の夕日→舞子から帰る）
- 起点は梅田〜難波のあたりのホテル（2026-11-22 オーナーの指示。京都から来る人・帰る人の電車と終電は補足として書く）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- スポットの文章は「名前 → コースごとの行き方（pre）→ 共通の説明（body）→ コースごとの次へ（post）→ おすすめ訪問時間」の順に組み立てる
- 時間割は11月下旬（日の入り16:50ごろ）の土曜のダイヤで組んだ。JR・阪神・山陽電車・地下鉄の時刻と運賃は
  乗換案内（Yahoo!路線情報、2026-11-28 土曜。朝の姫路行きだけ 11-26 木曜も）で確認
- 写真は images/himeji/<スポットのid>-<番号>.jpg を番号の順に全部使う（書写山はネットの写真で、_extra にクレジット）
"""
import json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/himeji"
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


def notice(hja, hen, ja, en, to=None, url=None):
    d = {"head": T(hja, hen), "text": T(ja, en)}
    if to:
        d["from"], d["to"] = None, to
    if url:
        d["url"] = url
    return d


def info(rows, tip=None, verified=True, cash=False, source=None, checked=None):
    d = {"rows": rows, "cash": cash, "tip": tip, "checked": checked or CHECKED, "source": source or []}
    if not verified:
        d["verified"] = False
    return d


def photos(pid, extra=None):
    # extra: ネットから借りた写真（{"file", "credit": {"author", "license", "page"}}）。写真の上に撮影者とライセンスが出る
    taken = {x["file"] for x in (extra or [])}
    own = [f"{pid}-{i}.jpg" for i in sorted(PICKS.get(pid, [])) if f"{pid}-{i}.jpg" not in taken]
    out = own + (extra or [])
    assert out, pid
    return out


def cc(file, author, license, title):
    return {"file": file, "credit": {"author": author, "license": license, "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))}}


PLANNER = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan)", "https://transit.yahoo.co.jp/")
SRC_PLANNER = "乗換案内（Yahoo!路線情報）2026-11-28（土）のダイヤ（朝の姫路行きは 11-26（木）も）"

# ---------------------------------------------------------------------------
# スポット（コースで変わらない部分）。コースで変わる行き方・時間・電車の行は下の COURSES に書く
# ---------------------------------------------------------------------------
S = dict(
    himejieki=dict(
        name=T("JR姫路駅", "JR Himeji Station"), kind=T("駅", "Station"),
        blurb=T("北口を出ると、大通りのいちばん奥に白い天守が見えます。お城の入口までは歩いて約20分。",
                "Out of the north exit, the white keep stands at the far end of the main street. About 20 minutes on foot to the castle entrance."),
        lat=34.82800, lng=134.69006,
        body=T("写真は、大手門の近くのお堀から見た天守です。\n\n"
               "駅のホームには立ち食いの「えきそば」があります。和風のだしに中華麺という姫路の駅の味で、天ぷらえきそばが550円。大阪・京都方面のホームの店は6:00〜23:00なので、帰りの電車を待つあいだにも食べられます。",
               "The photo shows the keep from the moat near the Otemon gate.\n\n"
               "On the station platforms there are stand-up Ekisoba counters: Chinese-style noodles in a Japanese dashi broth, Himeji’s station dish (tempura ekisoba ¥550). The one on the Osaka/Kyoto-bound platform is open 6:00–23:00, so you can eat while you wait for the train home."),
        gmaps=[gm("JR姫路駅", "JR Himeji Station", 34.82800, 134.69006, "JR姫路駅")],
        links=[link("official", "まねき食品 えきそばの店舗", "Maneki Ekisoba shops (official, Japanese)", "https://www.maneki-co.com/shop-list/?show=shop1"), PLANNER],
        rows=[row("hours", "えきそば：在来線上りホーム（大阪・京都方面）6:00〜23:00、下りホーム 6:00〜24:00。天ぷらえきそば550円",
                  "Ekisoba: Osaka/Kyoto-bound platform 6:00–23:00, westbound platform 6:00–24:00. Tempura ekisoba ¥550")],
        tip=T("電車の時刻と運賃は乗換案内（2026年11月の土曜のダイヤ。平日は時刻が変わります）、えきそばの時間と値段はまねき食品の公式サイトで確認しました。えきそばの休みの日は公式サイトに書かれていません。歩く時間は地図からの目安です。",
              "Train times and fares from a route planner (Saturday timetable, November 2026; weekday times differ). Ekisoba hours and price from the Maneki website, which gives no closing days. Walking times are estimates from the map."),
        source=["https://www.maneki-co.com/shop-list/?show=shop1", "https://www.maneki-co.com/products/ekisoba/", SRC_PLANNER]),
    himejijo=dict(
        name=T("姫路城", "Himeji Castle"), kind=T("城（世界遺産）", "Castle (World Heritage)"),
        blurb=T("白鷺城とも呼ばれる、真っ白な天守。木造の大天守の中を、急な階段で最上階まで上ります。",
                "The brilliant white keep, nicknamed the White Heron. Climb steep wooden stairs inside the great keep to the top floor."),
        caution=T("再入城できません。中は靴を脱ぎ、急な階段。大きな荷物はロッカーへ", "No re-entry. Shoes off and steep stairs inside; leave big bags in a locker"),
        lat=34.83933, lng=134.69402,
        body=T("江戸時代のはじめに建てられた天守が今も残る、世界遺産のお城です。白い漆喰の壁から「白鷺城（しらさぎじょう）」とも呼ばれます。"
               "菱の門から曲がりくねった坂と門をいくつも抜けて、大天守へ。中は木の柱と床がそのまま残り、急な階段で6階の最上階まで上れます。最上階の窓からは、姫路の町がまっすぐ駅まで見通せます。\n\n"
               "天守だけなら約1時間、西の丸の長い廊下「百間廊下」まで回ると1時間半〜2時間が、お城の案内している目安です。西の丸の廊下の窓からは、天守を横から眺められます。\n\n"
               "入城口より中に、食事のできる場所はありません。お弁当を広げるなら、入城口の外の三の丸広場で（屋根はありません）。",
               "A World Heritage castle whose early-Edo keep still stands. Its white plaster walls earned it the name “White Heron Castle”. "
               "From the Hishi gate, wind up through slopes and gates to the great keep. Inside, the original wooden pillars and floors remain, and steep stairs lead to the sixth, top floor, with a view straight down the city to the station.\n\n"
               "The castle suggests about 1 hour for the keep alone, and 1½–2 hours if you add the West Bailey and its long corridor, the Hyakken Roka. The corridor’s windows look at the keep from the side.\n\n"
               "There is nowhere to eat inside the ticket gate. For a picnic, use the Sannomaru lawn outside it (no shelter)."),
        gmaps=[gm("姫路城", "Himeji Castle", 34.83933, 134.69402, "姫路城")],
        links=[link("official", "姫路城 公式サイト", "Himeji Castle (official)", "https://www.himejicastle.jp/"),
               link("official", "デジタルチケット（日時指定）", "Digital tickets (timed)", "https://himejicastle-ticket.jp/"),
               link("info", "よくある質問（所要時間・荷物）", "FAQ (time needed, luggage; Japanese)", "https://www.himejicastle.jp/faq.html")],
        notices=[notice("入る前に", "Before you go in",
                        "入城券はその日かぎりで、一度出ると入り直せません。建物の中は靴を脱いで上がります（靴袋をもらえます）。エレベーターはなく、階段は急で狭いです。キャスターつきのかばんは入口のコインロッカー（有料・数に限りあり）へ。駅のロッカーに預けてから来るほうが確実です。\n"
                        "混む時期は入るまで1時間ほど待つことがある、とお城は案内しています。日にちが決まっているなら、日時指定のデジタルチケット（90日前から）を買っておけます。",
                        "Tickets are for that day only and there is no re-entry. Shoes come off inside (you get a bag for them). There are no lifts, and the stairs are steep and narrow. Wheeled bags must go in the coin lockers at the entrance (paid, limited), so it is safer to leave them at the station.\n"
                        "The castle says waits of about an hour can occur in busy periods. If your date is fixed, you can buy a timed digital ticket up to 90 days ahead.")],
        rows=[row("hours", "9:00〜17:00（入城は16:00まで。大天守に上るなら16:10までに天守の入口へ）", "9:00–17:00 (last entry 16:00; be at the keep entrance by 16:10 to go up)"),
              row("closed", "12月29日・30日", "29–30 December"),
              row("fee", "18歳以上 2,500円（姫路市民は1,000円）、18歳未満は無料。好古園との共通券 2,600円。カード・交通系ICカード・主なQR決済が使えます",
                  "Ages 18+ ¥2,500 (¥1,000 for Himeji residents); under 18 free. Combined ticket with Kokoen ¥2,600. Cards, IC transit cards and major QR payments accepted")],
        tip=T("時間・料金・支払い方法・所要時間は姫路城の公式サイト（よくある質問を含む）で確認しました。どの時間帯が混むかは公式サイトに書かれていません（年間の混雑予想カレンダーはあります）。",
              "Hours, fees, payment and time needed from the official Himeji Castle site and its FAQ. The site does not say which hours are busiest (it does publish a yearly crowd calendar)."),
        source=["https://www.himejicastle.jp/", "https://www.himejicastle.jp/faq.html"]),
    kokoen=dict(
        name=T("好古園", "Kokoen Garden"), kind=T("日本庭園・休憩", "Japanese garden & a rest"),
        blurb=T("お城の西の、9つの庭がつながる日本庭園。池の向こうに天守がのぞきます。園内のレストランと茶室で座って休めます。",
                "Nine linked gardens just west of the castle, with the keep peeking over the pond. Sit down at the restaurant or the tea house inside."),
        caution=T("入園は16:30まで（12月6日までは19:30まで）", "Last entry 16:30 (19:30 until 6 Dec)"),
        lat=34.83797, lng=134.68961,
        body=T("姫路城の西の御屋敷跡に造られた、9つの庭からなる日本庭園です。池泉回遊式の「御屋敷の庭」では、池の向こうに天守が見えます。入口はお城の入城口とは別で、大手門を出てお堀ぞいに西へ歩いて5分ほど。共通券（2,600円）なら、お城の券より100円高いだけで入れます。\n\n"
               "お城を歩いたあとに座れる場所が2つあります。レストラン「活水軒（かっすいけん）」は10:00〜16:00で、食事は11:00〜15:00（穴子丼のセット1,680円など）、コーヒー550円、抹茶のセット700円。席の予約はできません。茶室「双樹庵（そうじゅあん）」は正午〜16:00（受付15:40まで）で、抹茶とお菓子が800円です。\n\n"
               "写真は2024年9月の夜に撮ったものです。",
               "Nine gardens laid out on the site of the lords’ residences west of Himeji Castle. In the pond garden of the main residence, the keep rises beyond the water. The entrance is separate from the castle’s: out of the Otemon gate and about 5 minutes west along the moat. The combined ticket (¥2,600) costs only ¥100 more than the castle alone.\n\n"
               "Two places to sit after the castle: the restaurant Kassuiken is open 10:00–16:00 with meals 11:00–15:00 (conger-eel rice bowl set ¥1,680, for example), coffee ¥550 and a matcha set ¥700; no reservations. The tea house Sojuan is open noon–16:00 (last admission 15:40), matcha and a sweet ¥800.\n\n"
               "The photos were taken on an evening in September 2024."),
        gmaps=[gm("好古園", "Kokoen", 34.83797, 134.68961, "好古園 姫路")],
        links=[link("official", "好古園 公式サイト", "Kokoen (official, Japanese)", "https://himeji-machishin.jp/ryokka/kokoen/"),
               link("official", "レストラン 活水軒", "Kassuiken restaurant (official, Japanese)", "https://himeji-machishin.jp/ryokka/kokoen/kassuiken/index.html"),
               link("official", "茶室 双樹庵", "Sojuan tea house (official, Japanese)", "https://himeji-machishin.jp/ryokka/kokoen/soujyuan/index.html")],
        notices=[notice("紅葉会：12月6日まで夜も開園", "Autumn evenings until 6 December",
                        "2026年11月17日〜12月6日は20:00まで開いています（入園は19:30まで）。ライトアップは日没から。この期間の活水軒の夜の営業（17:00〜19:30）は、3日前までの予約が必要な特別メニューだけです。",
                        "From 17 November to 6 December 2026 the garden stays open until 20:00 (last entry 19:30), lit up from sunset. Kassuiken’s evening opening in this period (17:00–19:30) is a special menu only, booked at least 3 days ahead.",
                        to="2026-12-06", url="https://himeji-machishin.jp/ryokka/kokoen/info_detail.php?eid=00303")],
        rows=[row("hours", "9:00〜17:00（入園は16:30まで）", "9:00–17:00 (last entry 16:30)"),
              row("hours", "2026年11月17日〜12月6日は20:00まで（入園19:30まで）。ライトアップは日没から", "17 Nov – 6 Dec 2026: until 20:00 (last entry 19:30), lit up from sunset", until="2026-12-06"),
              row("hours", "活水軒 10:00〜16:00（食事11:00〜15:00、ラストオーダー15:30。混むと早く閉めることがあります）。双樹庵 正午〜16:00（受付15:40まで）",
                  "Kassuiken 10:00–16:00 (meals 11:00–15:00, last orders 15:30; may close early when busy). Sojuan noon–16:00 (last admission 15:40)"),
              row("closed", "12月29日・30日。双樹庵は12月21日〜1月5日も休み", "29–30 December. Sojuan also closed 21 Dec – 5 Jan"),
              row("fee", "大人400円、18歳未満は無料（姫路城との共通券 2,600円）", "¥400 adults, under 18 free (combined ticket with the castle ¥2,600)")],
        tip=T("時間と料金、活水軒・双樹庵の案内は好古園の公式サイトで確認しました。活水軒の休みの日と支払い方法は公式サイトに書かれていません。",
              "Hours, fees and the restaurant and tea house details from the Kokoen website, which does not give Kassuiken’s closing days or payment methods."),
        source=["https://himeji-machishin.jp/ryokka/kokoen/guidance/index.html", "https://himeji-machishin.jp/ryokka/kokoen/kassuiken/index.html",
                "https://himeji-machishin.jp/ryokka/kokoen/soujyuan/index.html", "https://himeji-machishin.jp/ryokka/kokoen/info_detail.php?eid=00303",
                "https://himeji-machishin.jp/ryokka/kokoen/info_detail.php?eid=00304"]),
    # 書写山 圓教寺は Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    shosha=dict(
        name=T("書写山 圓教寺", "Mt. Shosha Engyo-ji"), kind=T("寺・ロープウェイ（寄り道）", "Temple & ropeway (detour)"),
        blurb=T("ロープウェイで上る、山の上の大きなお寺。崖に張り出した摩尼殿と、3つのお堂が広場を囲む「三之堂」が見どころです。行くなら半日かかります。",
                "A big temple on a mountaintop, reached by ropeway. See Mani-den, built out over a cliff, and the three halls around a courtyard. Allow half a day."),
        caution=T("半日かかります。ロープウェイは2027年2月5日〜10月28日 運休", "Half a day. Ropeway closed 5 Feb – 28 Oct 2027"),
        lat=34.89143, lng=134.65754,
        body=T("姫路の町の北西、書写山の上にある天台宗のお寺です。西国三十三所の27番札所。ふもとからロープウェイで約4分上り、観音像が並ぶ参道を歩きます。\n\n"
               "最初に着くのが、崖に張り出すように建つ摩尼殿（まにでん）。そこから歩いて5〜6分の「三之堂（みつのどう）」は、大講堂・食堂（じきどう）・常行堂の3つのお堂が広場を囲む場所で、映画「ラスト サムライ」の撮影にも使われました（書写山ロープウェイの公式サイトより）。\n\n"
               "山上駅から摩尼殿までは約1km、歩いて15〜20分。志納所の前から摩尼殿の下まで、お寺のマイクロバス（往復500円）もあります。摩尼殿・三之堂・奥之院を回って約2時間が、お寺の案内している目安です。山道なので歩きやすい靴で。\n\n"
               "バスとロープウェイは、姫路駅前の神姫バス案内所で売っているセット券（1,700円）が、別々に払うより140円安くなります。姫路駅に着いたときに買っておきましょう。",
               "A Tendai temple on top of Mt. Shosha, north-west of Himeji, and No. 27 on the Saigoku Kannon pilgrimage. A ropeway takes about 4 minutes from the foot; from there you walk an approach lined with Kannon statues.\n\n"
               "First comes Mani-den, built out over a cliff. Five or six minutes further on are the Mitsu-no-do, three halls (the lecture hall, the long Jikido and the Jogyodo) around a courtyard, where scenes of “The Last Samurai” were filmed (according to the ropeway’s website).\n\n"
               "From the top station to Mani-den is about 1 km, 15–20 minutes on foot. The temple also runs a minibus from the entrance to just below Mani-den (¥500 return). The temple suggests about 2 hours for Mani-den, the three halls and the inner sanctuary. It’s a mountain path, so wear good shoes.\n\n"
               "The bus-and-ropeway set ticket (¥1,700), sold at the Shinki Bus office in front of Himeji Station, is ¥140 cheaper than paying separately. Buy it when you arrive at the station."),
        gmaps=[gm("圓教寺 摩尼殿", "Engyo-ji Mani-den", 34.89143, 134.65754, "書写山圓教寺 摩尼殿"),
               gm("書写山ロープウェイ（山麓駅）", "Shoshazan Ropeway (bottom station)", 34.87839, 134.66768, "書写山ロープウェイ 山麓駅")],
        links=[link("official", "書写山ロープウェイ 公式サイト（時刻・料金）", "Shoshazan Ropeway (official, Japanese)", "https://www.mt-shosha.info/category/charge/index.html"),
               link("official", "書寫山圓教寺 公式サイト（アクセス）", "Engyo-ji (official, Japanese)", "http://www.shosha.or.jp/access/"), PLANNER],
        notices=[notice("ロープウェイは2027年2月5日〜10月28日 運休", "Ropeway closed 5 Feb – 28 Oct 2027",
                        "大規模改修のため、書写山ロープウェイは2027年2月5日から10月28日まで運休します。お寺のマイクロバスも運休。圓教寺は開いていますが、登山道を歩いて上ります（片道30分〜1時間。圓教寺の公式サイトより）。",
                        "The ropeway is closed for major renovation from 5 February to 28 October 2027, and the temple minibus stops too. Engyo-ji stays open, but you have to walk up a trail (30 minutes to 1 hour each way, according to the temple).",
                        to="2027-10-28", url="https://www.mt-shosha.info/")],
        rows=[row("hours", "ロープウェイ 8:30から15分おき（毎時0・15・30・45分発）。下りの最終は、10月11日〜2月末が17:00（10月11日〜11月30日の日曜・祝日は18:00）、3月1日〜10月10日が18:00（4月1日〜10月10日の日曜・祝日は19:00）",
                  "Ropeway from 8:30, every 15 minutes. Last car down: 17:00 from 11 Oct to end of Feb (18:00 on Sundays and holidays 11 Oct – 30 Nov); 18:00 from 1 Mar to 10 Oct (19:00 on Sundays and holidays 1 Apr – 10 Oct)"),
              row("hours", "2026年11月21日〜23日は「書写山もみじまつり」。文化財の特別公開10:00〜16:00、紅葉のライトアップ17:00〜20:00（ロープウェイの下りは20:30まで）",
                  "21–23 Nov 2026: Shoshazan Momiji Festival. Special openings 10:00–16:00, autumn-leaf illumination 17:00–20:00 (ropeway down until 20:30)", until="2026-11-23"),
              row("closed", "ロープウェイは例年2月ごろ点検で運休。2027年は2月5日〜10月28日、改修工事で運休", "The ropeway closes for inspection around February each year; in 2027 it is closed 5 Feb – 28 Oct for renovation"),
              row("hours", "山上のマイクロバス（志納所前〜摩尼殿下）：8:55から。最終は、10月11日〜2月末が志納所前15:55発・摩尼殿下16:05発、3月1日〜10月10日が16:38発・16:45発。混むと早発・遅発あり",
                  "Minibus on the mountain (temple entrance ↔ below Mani-den): from 8:55. Last runs 11 Oct – end of Feb: 15:55 up, 16:05 back down; 1 Mar – 10 Oct: 16:38 and 16:45. Times can shift when busy"),
              row("hours", "納経（御朱印）の受付 9:00〜16:30", "Pilgrim stamp (goshuin) desk 9:00–16:30"),
              row("fee", "ロープウェイ 往復1,200円・片道700円（小人は半額）。圓教寺の志納金 中学生以上800円・小学生500円。山上のマイクロバス 往復500円",
                  "Ropeway ¥1,200 return, ¥700 one way (children half). Temple admission ¥800 (junior high and up), ¥500 elementary. Minibus on the mountain ¥500 return"),
              row("fee", "書写山ロープウェイ＋バス往復セット乗車券 1,700円（姫路駅前の神姫バス案内所で販売。別々に払うと1,840円）",
                  "Ropeway + return bus set ticket ¥1,700, sold at the Shinki Bus office in front of Himeji Station (¥1,840 if paid separately)"),
              row("train", "神姫バス：姫路駅北口10番のりば → 書写山ロープウェイ 約25〜30分・320円", "Shinki bus: Himeji Station north exit, stop 10 → Shoshazan Ropeway, about 25–30 min, ¥320")],
        checked="2026-11-24",
        tip=T("2026年11月24日に確認しました。ロープウェイの時刻・料金とセット券は書写山ロープウェイの公式サイト、志納金・マイクロバス・納経の時間は圓教寺の公式サイト、バスと電車は乗換案内（2026年11月の土曜と木曜のダイヤ）から。圓教寺の拝観時間は公式サイトに書かれていないので、ロープウェイとマイクロバスの最終に合わせてください（要確認）。",
              "Checked on 24 November 2026: ropeway times, fares and the set ticket on the ropeway’s website; admission, the minibus and the goshuin desk hours on the temple’s website; buses and trains on a route planner (Saturday and Thursday timetables, November 2026). The temple’s own opening hours are not given on its website, so plan around the last ropeway and minibus (please check)."),
        source=["https://www.mt-shosha.info/category/charge/index.html", "https://www.mt-shosha.info/category/access/index.html", "http://www.shosha.or.jp/access/",
                "圓教寺 公式サイト トップ（ロープウェイ運休中の参拝・納経の受付時間） http://www.shosha.or.jp/", "乗換案内（Yahoo!路線情報）2026-11-28（土）・11-26（木）のダイヤ"],
        _extra=[cc("shosha-1.jpg", "663highland", "CC BY 2.5", "File:Engyoji01s4592.jpg"),
                cc("shosha-2.jpg", "663highland", "CC BY 2.5", "File:Engyoji05s4592.jpg"),
                cc("shosha-3.jpg", "663highland", "CC BY 2.5", "File:Engyoji45n4592.jpg"),
                cc("shosha-4.jpg", "Umako", "CC0", "File:Himeji City Mt. Shosha Ropeway 250506.jpg")]),
    akashi=dict(
        name=T("明石 魚の棚と「たこ磯」の明石焼", "Akashi: Uonotana market & Takoiso akashiyaki"), kind=T("市場・お昼", "Market & lunch"),
        blurb=T("明石駅のすぐ南の、明石だこと魚の商店街。お昼はたこ磯で、だし汁につけて食べる明石焼（玉子焼）を。",
                "The fish-and-octopus arcade just south of Akashi Station. Lunch is akashiyaki (tamagoyaki) at Takoiso, dipped in dashi."),
        caution=T("木曜は休む店が多い。現金を用意", "Many shops close on Thursdays. Bring cash"),
        lat=34.64701, lng=134.99213,
        body=T("明石駅から南へ歩いて3分。明石の海でとれた魚やたこ、干物やかまぼこの店が並ぶアーケードの商店街です。お昼ごろからは、その日の昼にとれた魚「昼網」も並びます。\n\n"
               "お昼は、商店街の中ほど、弁天さまの隣にある「たこ磯」へ。白いのれんに赤い字で「玉子焼」。明石では明石焼のことを玉子焼と呼びます。ふわふわの玉子焼を、温かいだし汁につけて食べます。15個で一人前。たこと穴子の両方が入るミックス焼が1,000円です。席は28席。\n\n"
               "食べ終わったら、アーケードを端まで歩いてみてください。ゆでだこや焼き穴子を店先で売る店があり、玉子焼だけで足りなければここで足せます。\n\n"
               "時間が余ったら、明石駅の北口から歩いて5分の明石城跡（明石公園）へ。お堀と2つの櫓が、駅のホームからも見えます。",
               "Three minutes’ walk south of Akashi Station: an arcade of shops selling fish and octopus from the Akashi sea, dried fish and fish cakes. From around midday the day’s midday catch, “hiruami”, is on sale too.\n\n"
               "For lunch, go to Takoiso, halfway along next to the little Benten shrine: white curtain, red letters, 玉子焼. In Akashi, akashiyaki is called tamagoyaki. Dip the fluffy dumplings in warm dashi. A portion is 15; the “mix” with both octopus and conger eel is ¥1,000. There are 28 seats.\n\n"
               "Afterwards walk the arcade to the end. Some shops sell boiled octopus and grilled conger eel out front, handy if the dumplings were not enough.\n\n"
               "With time to spare, Akashi Castle ruins (Akashi Park) are 5 minutes from the station’s north exit; the moat and two turrets are visible from the platform."),
        gmaps=[gm("魚の棚商店街", "Uonotana", 34.64701, 134.99213, "魚の棚商店街 明石"), gm("たこ磯", "Takoiso", 34.64696, 134.99289, "たこ磯 明石 本町")],
        links=[link("official", "魚の棚商店街 公式サイト", "Uonotana shopping street (official, Japanese)", "https://www.uonotana.or.jp/"),
               link("info", "たこ磯（魚の棚商店街のお店のページ）", "Takoiso (shop page on the Uonotana site, Japanese)", "https://www.uonotana.or.jp/shop-057.html")],
        notices=[notice("木曜日と支払い", "Thursdays, and paying",
                        "木曜日は競りがないので、魚の棚は休む店が多くなります（たこ磯は定休日なし）。たこ磯の支払い方法は商店街のサイトに書かれていません。市場の店先も含めて、現金を用意しておくと安心です。",
                        "There is no fish auction on Thursdays, so many Uonotana shops close (Takoiso has no regular closing day). The arcade’s website does not say how you can pay at Takoiso; carry cash for it and for the market stalls.")],
        rows=[row("hours", "たこ磯 10:00〜19:00、定休日なし。魚の棚の営業時間は店ごとに違います", "Takoiso 10:00–19:00, open daily. Uonotana shop hours vary"),
              row("fee", "たこ磯：ミックス焼（たこ・穴子、15個）1,000円、あなご入（15個）800円", "Takoiso: mix (octopus and conger eel, 15 pieces) ¥1,000; conger eel (15) ¥800"),
              row("closed", "魚の棚は木曜に休む店が多い", "Many Uonotana shops close on Thursdays")],
        tip=T("たこ磯の時間・値段・席数は魚の棚商店街の公式サイトのお店のページで確認しました（たこだけの玉子焼の値段と、支払い方法は書かれていません）。",
              "Takoiso’s hours, prices and seats from its page on the Uonotana website (the price of the plain octopus version and payment methods are not given)."),
        source=["https://www.uonotana.or.jp/shop-057.html", "https://www.uonotana.or.jp/", SRC_PLANNER]),
    suma=dict(
        name=T("須磨浦公園（須磨浦山上遊園）", "Sumaura Park (Sumaura Sanjo Yuen)"), kind=T("ロープウェー・展望台", "Ropeway & lookout"),
        blurb=T("ロープウェーと、乗り心地がびっくりなカーレーターで山の上へ。回る喫茶店から、須磨の海と明石海峡大橋が見えます。",
                "Up by ropeway and the bumpy “Car-rator” to a hilltop. From the revolving café, look over the Suma sea and the Akashi Kaikyo Bridge."),
        caution=T("火曜休み。12月2日〜2月5日は土日祝だけ。山の上は現金のみ", "Closed Tuesdays; weekends and holidays only 2 Dec – 5 Feb. Cash only up top"),
        lat=34.63784, lng=135.10022,
        body=T("山陽電車の須磨浦公園駅を出てすぐ、ロープウェーで鉢伏山へ上ります。窓の外には須磨の海岸と神戸の街。"
               "山上駅からは、ベルトコンベアの上の小さなカゴに乗って進む「カーレーター」で、さらに上の回転展望閣へ。ガタガタ揺れる乗り心地は、ここでしか味わえません。\n\n"
               "回転展望閣の3階の喫茶コスモスは、床がゆっくり回ります（約55分で1回転）。晴れた日は、明石海峡大橋や関西空港まで見えます。\n\n"
               "切符は、ロープウェー・カーレーターの往復と展望閣がセットの回遊券Bコース（1,500円）を、ふもとの窓口で。カードやQR決済が使えるのはこの窓口だけで、山の上は喫茶コスモスも含めて現金です。回るのにかかる時間は、標準で70分と案内されています。",
               "Right outside Sanyo Railway’s Sumaura-koen Station, a ropeway climbs Mt. Hachibuse, with the Suma beach and Kobe below. "
               "From the top station, the “Car-rator”, little baskets riding on a conveyor belt, carries you up to the revolving observatory. Its rattling ride is like nothing else.\n\n"
               "Café Cosmos on the third floor of the observatory slowly revolves (about 55 minutes a turn). On clear days you can see the Akashi Kaikyo Bridge and even Kansai Airport.\n\n"
               "Buy the B-course round ticket (¥1,500: ropeway and Car-rator both ways plus the observatory) at the window at the bottom. That window is the only place that takes cards or QR payments; everything up top, Café Cosmos included, is cash. The park gives 70 minutes as the standard time for the round."),
        gmaps=[gm("須磨浦公園駅", "Sumaura-koen Station", 34.63784, 135.10022, "須磨浦公園駅"), gm("須磨浦山上遊園", "Sumaura Sanjo Yuen", 34.64190, 135.09421, "須磨浦山上遊園")],
        links=[link("official", "須磨浦山上遊園 公式サイト", "Sumaura Sanjo Yuen (official, Japanese)", "https://www.sumaura-yuen.jp/"),
               link("official", "営業時間と料金", "Hours and fares (official, Japanese)", "https://www.sumaura-yuen.jp/time_price.html")],
        cash=True,
        rows=[row("hours", "10:00〜17:00（最終入場16:30）。ロープウェーは毎時0・15・30・45分発", "10:00–17:00 (last entry 16:30). Ropeway every 15 minutes"),
              row("hours", "喫茶コスモス 10:10〜16:30（ラストオーダー15:30）。展望閣の屋上 10:10〜16:20。カーレーター 10:10〜16:50", "Café Cosmos 10:10–16:30 (last orders 15:30). Observatory roof 10:10–16:20. Car-rator 10:10–16:50"),
              row("closed", "火曜日（祝日は営業）。2026年12月2日〜2027年2月5日は土日祝だけ営業（12/12・13・19・20、1/16・17は休園）", "Tuesdays (open on holidays). 2 Dec 2026 – 5 Feb 2027: weekends and holidays only (closed 12, 13, 19, 20 Dec and 16, 17 Jan)"),
              row("fee", "回遊券 Bコース1,500円・Aコース（リフトも）2,100円。ばらで買うとロープウェー往復920円、カーレーター往復550円。喫茶コスモスの入場200円",
                  "Round tickets: B course ¥1,500, A course (with chairlift) ¥2,100. Separately: ropeway ¥920 return, Car-rator ¥550 return. Café Cosmos entry ¥200")],
        tip=T("時間・料金・支払い方法・冬の営業日は須磨浦山上遊園の公式サイトで確認しました。",
              "Hours, fares, payment and the winter opening days from the official website."),
        source=["https://www.sumaura-yuen.jp/time_price.html", "https://www.sumaura-yuen.jp/event/entry-709.html", SRC_PLANNER]),
    maiko=dict(
        name=T("舞子公園・明石海峡大橋", "Maiko Park & Akashi Kaikyo Bridge"), kind=T("公園・橋", "Park & bridge"),
        blurb=T("世界最大級のつり橋の真下の、海辺の公園。橋の中を歩けるプロムナードもあります。駅から歩いてすぐ。",
                "A seaside park right under one of the world’s longest suspension bridges, with a walkway inside the bridge. A few minutes from the station."),
        lat=34.63275, lng=135.03300,
        body=T("JR舞子駅・山陽電車の舞子公園駅から南へ歩いて約5分。淡路島へ渡る明石海峡大橋の真下の海辺の公園です。橋の向こうに淡路島が見え、夕日は西の海に沈みます。\n\n"
               "橋の桁の中に入れる「舞子海上プロムナード」は、海面から約47mの高さを歩く回廊です。床がガラスになった所から、下を通る船が見えます。",
               "About 5 minutes south of JR Maiko and Sanyo Maiko-koen stations: a seaside park right under the Akashi Kaikyo Bridge to Awaji Island. Awaji lies beyond the bridge and the sun goes down into the sea to the west.\n\n"
               "The Maiko Marine Promenade is a walkway inside the bridge girders, about 47 m above the sea, with glass floor panels to watch ships pass beneath."),
        gmaps=[gm("舞子公園", "Maiko Park", 34.63275, 135.03300, "舞子公園"), gm("JR舞子駅", "JR Maiko Station", 34.63351, 135.03382, "JR舞子駅")],
        links=[link("official", "舞子公園 公式サイト", "Maiko Park (official, Japanese)", "https://hyogo-maikopark.jp/"),
               link("official", "舞子海上プロムナード", "Maiko Marine Promenade (official, Japanese)", "https://hyogo-maikopark.jp/facility/f01/"), PLANNER],
        rows=[row("hours", "公園は出入り自由。舞子海上プロムナード 9:00〜18:00（入館は17:30まで。ゴールデンウィークと夏休みは19:00まで）", "The park is always open. Maiko Marine Promenade 9:00–18:00 (last entry 17:30; until 19:00 in Golden Week and the summer holidays)"),
              row("closed", "プロムナード：10〜3月は第2月曜（祝日なら翌日）、12月29日〜31日", "Promenade: 2nd Monday Oct–Mar (next day if a holiday), 29–31 Dec"),
              row("fee", "プロムナード 大人 平日250円・土日祝300円（高校生以下は無料）", "Promenade ¥250 weekdays, ¥300 weekends and holidays (free for high school and under)"),
              row("hours", "明石海峡大橋のライトアップ：日没〜23:00（土日祝と特定の日は24:00まで）。毎正時と毎時30分に5分間、色が変わります",
                  "Akashi Kaikyo Bridge light-up: sunset to 23:00 (to 24:00 on weekends, holidays and some special days). The colours change for 5 minutes on the hour and at half past")],
        tip=T("プロムナードの時間・休み・料金は舞子公園の公式サイト、橋のライトアップは本四高速（JB本四高速）の公式サイト、電車は乗換案内で確認しました。プロムナードの支払い方法は公式サイトに書かれていません。",
              "Promenade hours, closing days and fees from the Maiko Park website; the bridge light-up from the bridge operator (JB Honshi) website; trains on a route planner. The promenade’s payment methods are not given on its website."),
        source=["https://hyogo-maikopark.jp/facility/f01/", "本四高速 明石海峡大橋ライトアップスケジュール（2026-11-24 確認） https://www.jb-honshi.co.jp/customer_index/kanko_event/lightup/lightup-akashi.html", SRC_PLANNER]),
)

TITLE = dict(
    himejieki=T("JR姫路駅（ひめじえき）", "JR Himeji Station"),
    himejijo=T("姫路城（ひめじじょう）", "Himeji Castle"),
    kokoen=T("好古園（こうこえん）", "Kokoen Garden"),
    shosha=T("書写山 圓教寺（しょしゃざん えんぎょうじ）", "Mt. Shosha Engyo-ji"),
    akashi=T("魚の棚（うおんたな）商店街と、たこ磯（たこいそ）", "Uonotana market and Takoiso"),
    suma=T("須磨浦公園（すまうらこうえん）と須磨浦山上遊園", "Sumaura Park and Sumaura Sanjo Yuen"),
    maiko=T("舞子公園（まいここうえん）と明石海峡大橋", "Maiko Park and the Akashi Kaikyo Bridge"),
)

# 帰りの電車（姫路から。夜の時刻は土曜のダイヤ）
HOME_HIMEJI = T("帰りは姫路駅から新快速で大阪まで乗り換えなしの62分（1,460円）。姫路19:26発→大阪20:28着、19:41発→20:43着、20:16発→21:18着、20:37発→21:39着。なんばへは大阪駅から歩いて西梅田へ出て、四つ橋線で8分（240円）。\n\n"
                "新快速の最後は姫路22:56発（大阪0:00着、京都0:30着）。なんばまで帰るなら、これが四つ橋線の最終（西梅田0:07発）に間に合う最後です。大阪までの最終は22:58発（西明石で乗り換え、大阪0:46着）。\n\n"
                "京都へ帰る人も同じ新快速で乗り換えなし（20:16発→京都21:49着・2,210円）。",
                "Go home by Special Rapid from Himeji: 62 minutes direct to Osaka (¥1,460). Himeji 19:26 → Osaka 20:28, 19:41 → 20:43, 20:16 → 21:18, 20:37 → 21:39. For Namba, walk from Osaka Station to Nishi-Umeda and take the Yotsubashi Line (8 min, ¥240).\n\n"
                "The last Special Rapid leaves Himeji at 22:56 (Osaka 0:00, Kyoto 0:30); for Namba it is the last one that connects with the final Yotsubashi Line train (Nishi-Umeda 0:07). The very last train to Osaka is the 22:58 (change at Nishi-Akashi, Osaka 0:46).\n\n"
                "For Kyoto, stay on the same Special Rapid (20:16 → Kyoto 21:49, ¥2,210).")

# ---------------------------------------------------------------------------
# コース
# ---------------------------------------------------------------------------
LATE = dict(
    id="late", file="himeji.json",
    order=["suma", "maiko", "akashi", "himejijo", "kokoen", "himejieki", "shosha"],
    default=["suma", "akashi", "himejijo", "kokoen"],
    sections=[("suma", "maiko", "須磨・舞子", "Suma & Maiko", "朝は海を見下ろす山の上へ", "Start on a hilltop above the sea"),
              ("akashi", "akashi", "明石", "Akashi", "魚の棚で明石焼のお昼", "Akashiyaki lunch in the fish arcade"),
              ("himejijo", "himejieki", "姫路", "Himeji", "午後のお城、夕暮れ、晩ごはん", "The castle in the afternoon, dusk and dinner"),
              ("shosha", "shosha", "書写山", "Mt. Shosha", "行くなら半日の寄り道", "A half-day detour")],
    spots=dict(
        suma=dict(
            pre=T("このコースは、海ぞいを西へ進んで、姫路城には午後に着きます。最初の目的地はここ。\n\n"
                  "梅田のあたりのホテルを9:15ごろに出て、阪神の大阪梅田駅へ。9:30発の特急「須磨浦公園行」に乗れば、乗り換えなしで10:27に着きます（740円）。なんばのあたりからは、阪神なんば線の大阪難波9:17発の快速急行で神戸三宮へ（9:58着）、同じ特急（10:01発）に乗り換えます（830円）。\n\n"
                  "京都から来る人は、京都9:00発の新快速で三ノ宮へ（9:51着）。阪神の神戸三宮駅まで歩いて、10:01発の同じ特急に乗れます（1,510円）。",
                  "This course works west along the coast and reaches Himeji Castle in the afternoon. The first stop is here.\n\n"
                  "Leave a hotel around Umeda at about 9:15 for Hanshin’s Osaka-Umeda Station. The 9:30 limited express bound for Sumaura-koen gets there at 10:27 with no change (¥740). From around Namba, take the 9:17 rapid express on the Hanshin Namba Line from Osaka-Namba to Kobe-Sannomiya (9:58) and change to the same limited express (10:01); ¥830.\n\n"
                  "From Kyoto: the 9:00 Special Rapid to Sannomiya (9:51), walk to Hanshin Kobe-Sannomiya, and board that same 10:01 limited express (¥1,510)."),
            post=T("10:30のロープウェーで上り、まず回転展望閣へ。喫茶コスモスで朝のコーヒーを飲みながら1周するくらいの時間があります。11:45ごろのロープウェーで下りて、須磨浦公園11:56発の山陽電車で山陽明石へ（12:17着・乗り換えなし・390円）。",
                   "Take the 10:30 ropeway and go straight to the revolving observatory; there is time for a morning coffee at Café Cosmos while the floor makes a turn. Come down on the ropeway around 11:45 and take the 11:56 Sanyo train to Sanyo-Akashi (12:17, direct, ¥390)."),
            time=T("10:30〜11:50", "10:30–11:50"),
            notices=[notice("火曜と、冬の平日は休み", "Closed Tuesdays and winter weekdays",
                            "火曜日（祝日は営業）と、2026年12月2日〜2027年2月5日の平日は休みです（この期間は土日祝だけ。12/12・13・19・20、1/16・17も休園）。その日は代わりに舞子公園へ：大阪9:30発の新快速に乗り、神戸で各駅停車に乗り換えて舞子10:19着（840円）。橋のプロムナードを歩いて、舞子公園11:53発の直通特急で山陽明石へ（4分・250円）。",
                            "Closed on Tuesdays (open on holidays) and on weekdays from 2 December 2026 to 5 February 2027 (weekends and holidays only in that period; also closed 12, 13, 19, 20 Dec and 16, 17 Jan). On those days go to Maiko Park instead: the 9:30 Special Rapid from Osaka, change to a local at Kobe, Maiko 10:19 (¥840). Walk the bridge promenade, then take the 11:53 limited express from Maiko-koen to Sanyo-Akashi (4 min, ¥250).")],
            rows=[row("train", "行き：大阪梅田（阪神）9:30発 特急 → 須磨浦公園10:27着・740円（乗り換えなし）。大阪難波9:17発 → 神戸三宮で乗り換え → 10:27着・830円",
                      "Getting there: Osaka-Umeda (Hanshin) 9:30 limited express → Sumaura-koen 10:27, ¥740, direct. Osaka-Namba 9:17 → change at Kobe-Sannomiya → 10:27, ¥830"),
                  row("train", "次へ：須磨浦公園11:56発（山陽電車）→ 山陽明石12:17着・390円", "Next: Sumaura-koen 11:56 (Sanyo) → Sanyo-Akashi 12:17, ¥390")]),
        maiko=dict(
            kind=T("公園・橋（寄り道）", "Park & bridge (detour)"),
            pre=T("このコースでは寄り道です。舞子公園駅は、須磨浦公園と明石のあいだにあります（須磨浦公園から山陽電車で14分・250円）。須磨浦山上遊園が休みの日は、ここを朝の目的地にしてください。",
                  "A detour on this course. Maiko-koen Station is between Sumaura-koen and Akashi (14 minutes from Sumaura-koen on the Sanyo line, ¥250). On days when Sumaura Sanjo Yuen is closed, make this your morning stop instead."),
            post=T("明石へは、舞子公園11:53発か12:08発の直通特急で4分（250円）。",
                   "For Akashi, the limited express from Maiko-koen at 11:53 or 12:08 takes 4 minutes (¥250)."),
            time=T("寄り道（40分ほど）", "Detour (about 40 minutes)"),
            rows=[row("train", "須磨浦公園11:26発 → 舞子公園11:40着・250円。舞子公園12:08発（直通特急）→ 山陽明石12:12着・250円",
                      "Sumaura-koen 11:26 → Maiko-koen 11:40, ¥250. Maiko-koen 12:08 (limited express) → Sanyo-Akashi 12:12, ¥250")]),
        akashi=dict(
            pre=T("山陽明石駅からもJR明石駅からも、南へ歩いて3分です。12:20ごろに着いて、先にたこ磯でお昼、そのあと市場を歩く順番がおすすめ。昼網の魚が並びはじめる時間です。",
                  "Three minutes’ walk south of either Sanyo-Akashi or JR Akashi Station. Arrive around 12:20, eat at Takoiso first, then walk the market, just as the midday catch starts to appear."),
            post=T("JR明石駅13:38発の新快速で姫路へ（14:02着・660円）。乗り遅れても、次は13:53発（14:17着）です。",
                   "Take the 13:38 Special Rapid from JR Akashi to Himeji (14:02, ¥660). If you miss it, the next is 13:53 (arr. 14:17)."),
            time=T("12:20〜13:30", "12:20–13:30"),
            rows=[row("train", "次へ：明石13:38発（JR新快速）→ 姫路14:02着・660円", "Next: Akashi 13:38 (JR Special Rapid) → Himeji 14:02, ¥660")]),
        himejijo=dict(
            pre=T("姫路駅に14:02に着いたら、北口から大手前通りをまっすぐ歩いて、14:25ごろに入城口へ。入城は16:00までなので、明石を出るのが遅れた日も14:08発の新快速（姫路14:32着）までには乗ってください。\n\n"
                  "午後は、朝から来た団体や日帰りの人が帰りはじめる時間です（どのくらい空くかは日によります）。西日が白い壁に当たる時間でもあります。",
                  "Arrive at Himeji at 14:02, walk straight up Otemae-dori from the north exit, and reach the ticket gate around 14:25. Last entry is 16:00, so even on a slow day leave Akashi by the 14:08 Special Rapid (Himeji 14:32).\n\n"
                  "By mid-afternoon the morning’s tour groups and day-trippers are starting to leave (how quiet it gets depends on the day), and the low sun falls on the white walls."),
            post=T("先に大天守へ上り、下りてから西の丸へ。16:10ごろに出て、好古園へ向かいます（入園は16:30まで）。",
                   "Go up the great keep first, then the West Bailey. Leave around 16:10 for Kokoen (last entry 16:30)."),
            time=T("14:25〜16:10", "14:25–16:10")),
        kokoen=dict(
            pre=T("お城を16:10ごろに出れば、16:15には入れます。ふだんは17:00に閉まるので、歩けるのは45分ほど。池のある「御屋敷の庭」を先に見てください。活水軒と双樹庵は16:00までなので、このコースでは間に合いません。\n\n"
                  "12月6日までは20:00まで開いていて、日が暮れるとライトアップが始まります。この期間は急がず、暗くなるまで庭にいるのがおすすめです。",
                  "Leave the castle around 16:10 and you are in by 16:15. The garden normally closes at 17:00, so you have about 45 minutes: see the pond garden of the main residence first. Kassuiken and Sojuan both close at 16:00, too early for this course.\n\n"
                  "Until 6 December the garden stays open until 20:00 and is lit up once the sun goes down. In that period, take your time and stay until dark."),
            post=T("出たら、お堀ぞいに大手門の前へ戻ります。", "When you leave, walk back along the moat to the front of the Otemon gate."),
            time=T("16:15〜17:00", "16:15–17:00")),
        himejieki=dict(
            name=T("夕暮れのお城と、姫路駅前の晩ごはん", "The castle at dusk, and dinner by Himeji Station"),
            title=T("夕暮れの姫路城と、姫路駅（ひめじえき）前の晩ごはん", "The castle at dusk, and dinner by Himeji Station"), kind=T("夕景・晩ごはん・帰り", "Dusk, dinner & the way home"),
            blurb=T("日が沈むと、天守に明かりが入ります。大手前通りを駅へ戻って晩ごはん、新快速で大阪へ約1時間。",
                    "At sunset the keep is lit. Walk back down Otemae-dori for dinner, then about an hour to Osaka by Special Rapid."),
            pre=T("11月下旬の日の入りは16:50ごろ。姫路城のライトアップは日没から24:00までで、好古園を出るころ、ちょうど天守が白く浮かびます。大手門の前のお堀の橋と、その南の大手前公園から、正面の姿が見えます。毎日20:00と21:00には、色が変わる15分間の演出もあります。\n\n"
                  "17:30ごろから大手前通りを駅へ歩いて約15分。通りの東に並行するアーケードの商店街と駅のまわりに、居酒屋や食堂が集まっています。姫路のおでんは、しょうが醤油をかけて食べます。\n\n",
                  "Sunset in late November is around 16:50. The castle is lit from sunset to midnight, so the keep is glowing white just as you leave Kokoen. The bridge over the moat at the Otemon gate, and Otemae Park just south of it, face it head-on. Every day at 20:00 and 21:00 there is also a 15-minute colour show.\n\n"
                  "From about 17:30 walk back down Otemae-dori to the station, about 15 minutes. The covered shopping arcades running parallel to the east, and the streets around the station, are where the izakaya and diners are. Himeji-style oden is eaten with ginger soy sauce.\n\n"),
            post=HOME_HIMEJI,
            time=T("17:00〜19:30（20:00の演出を見るなら20:30まで）", "17:00–19:30 (to 20:30 if you stay for the 20:00 show)"),
            links=[link("official", "姫路城 公式サイト（ライトアップ）", "Himeji Castle (official; light-up)", "https://www.himejicastle.jp/")],
            rows=[row("hours", "姫路城のライトアップ：日没〜24:00。20:00と21:00に各15分の特別演出（姫路城の公式サイト）", "Castle light-up: sunset to 24:00, with 15-minute special shows at 20:00 and 21:00 (official castle site)"),
                  row("train", "帰り：姫路19:26発（新快速）→ 大阪20:28着・1,460円。19:41発、20:16発、20:37発もあり。京都へは20:16発→21:49着・2,210円",
                      "Home: Himeji 19:26 (Special Rapid) → Osaka 20:28, ¥1,460; also 19:41, 20:16, 20:37. For Kyoto, 20:16 → 21:49, ¥2,210"),
                  row("train", "最後の新快速：姫路22:56発 → 大阪0:00着・京都0:30着。大阪までの最終は22:58発（0:46着）", "Last Special Rapid: Himeji 22:56 → Osaka 0:00, Kyoto 0:30. Last train to Osaka: 22:58 (arr. 0:46)")]),
        shosha=dict(
            pre=T("このコースの時間割には入りません。9〜10時に出て書写山へ行くなら、須磨と明石をやめて、大阪9:30発の新快速で姫路へ直行します（10:33着・1,460円）。"
                  "駅北口の10番のりば10:55発のバスで書写山ロープウェイへ（11:27着、平日は11:25着・320円）。11:30のロープウェイで上り、お寺を2時間ほど回ります。"
                  "13:45ごろのロープウェイで下りて、14:11発のバスに乗り、「姫路城大手門前」で降ります（14:33着）。そのままお城へ入れば、入城の16:00に十分間に合います。"
                  "お昼を食べる時間がとりにくいので、姫路駅に着いたら、降りたホームのえきそばで早めに済ませておくと楽です。",
                  "This does not fit the course as timed. To see Mt. Shosha on a 9–10 o’clock start, skip Suma and Akashi and go straight to Himeji on the 9:30 Special Rapid from Osaka (10:33, ¥1,460). "
                  "Take the 10:55 bus from stop 10 at the north exit to Shoshazan Ropeway (11:27, or 11:25 on weekdays; ¥320). Ride the 11:30 ropeway up and allow about two hours at the temple. "
                  "Come down around 13:45, take the 14:11 bus and get off at “Himeji-jo Otemon-mae” (14:33). Walk straight into the castle, well before the 16:00 last entry. "
                  "There is little time for lunch, so an early bowl of ekisoba on the platform when you arrive at Himeji makes it easier."),
            rows=[row("train", "行き：姫路駅北口10番のりば 10:55発（神姫バス）→ 書写山ロープウェイ 11:27着（平日11:25着）・320円",
                      "Getting there: Himeji Station north exit, stop 10, 10:55 (Shinki bus) → Shoshazan Ropeway 11:27 (weekdays 11:25), ¥320"),
                  row("train", "帰り：書写山ロープウェイ14:11発（バス）→ 姫路城大手門前14:33着（土曜・木曜とも）。乗り遅れたら次は14:31発（14:53着）",
                      "Back: Shoshazan Ropeway 14:11 (bus) → Himeji-jo Otemon-mae 14:33 (same on Saturdays and Thursdays). If you miss it, the next is 14:31 (arr. 14:53)")],
            time=T("寄り道（往復のバスを入れて約4時間）", "Detour (about 4 hours including the buses)")),
    ),
    hints=[
        ("maiko", {"any": ["maiko"], "andAny": ["suma"]},
         "須磨と舞子の両方に寄ると、明石のお昼が40分ほど遅くなり、お城に入るのは15時ごろになります。その日は好古園を外すか、須磨を11:26発の電車で出てください。",
         "With both Suma and Maiko, lunch in Akashi slips by about 40 minutes and you reach the castle around 15:00. Drop Kokoen that day, or leave Suma on the 11:26 train."),
        ("maiko", {"any": ["maiko"], "none": ["suma"]},
         "須磨に寄らない日は、大阪9:30発の新快速に乗り、神戸で各駅停車に乗り換えて舞子へ（10:19着・840円）。",
         "Skipping Suma? Take the 9:30 Special Rapid from Osaka and change to a local at Kobe for Maiko (10:19, ¥840)."),
        ("akashi", {"any": ["akashi"], "none": ["suma", "maiko"]},
         "須磨と舞子に寄らない日は、大阪から新快速で明石へ乗り換えなし（約38分・960円）。たこ磯は10:00からです。",
         "Skipping Suma and Maiko? The Special Rapid from Osaka stops at Akashi (about 38 min, ¥960). Takoiso opens at 10:00."),
        ("himejijo", {"any": ["himejijo"], "none": ["suma", "maiko", "akashi"]},
         "姫路だけの日は、大阪9:30発の新快速で姫路10:33着（1,460円）。お城に入るのは11時ごろで、1日でいちばん人が多くなりやすい時間です。お城を先にしたいなら、「開城に合わせる」コースのほうが楽です。",
         "Himeji only? The 9:30 Special Rapid from Osaka arrives at 10:33 (¥1,460), putting you at the castle around 11:00, likely the busiest part of the day. If the castle comes first, the “castle at opening” course is easier."),
        ("shosha", {"any": ["shosha"], "andAny": ["suma", "maiko", "akashi"]},
         "書写山は往復のバスを入れて約4時間。須磨・明石と同じ日には入りません。書写山へ行く日は、大阪から姫路へ直行してください。",
         "Mt. Shosha takes about 4 hours with the buses and does not fit with Suma and Akashi. On a Mt. Shosha day, go straight from Osaka to Himeji."),
        ("kokoen", {"any": ["kokoen"], "none": ["himejijo"]},
         "お城に入らない日は、活水軒（食事は15:00まで）や双樹庵（受付15:40まで）に間に合う時間に来られます。",
         "Without the castle, you can get here in time for Kassuiken (meals until 15:00) or Sojuan (last admission 15:40)."),
    ],
)

EARLY = dict(
    id="early", file="himeji-early.json",
    order=["himejieki", "himejijo", "kokoen", "shosha", "akashi", "suma", "maiko"],
    default=["himejijo", "kokoen", "akashi", "suma", "maiko"],
    sections=[("himejieki", "kokoen", "姫路", "Himeji", "開城に合わせてお城へ、そのあと庭でひと休み", "The castle at opening, then a rest in the garden"),
              ("shosha", "shosha", "書写山", "Mt. Shosha", "行くなら午後いっぱいの寄り道", "A detour for the whole afternoon"),
              ("akashi", "akashi", "明石", "Akashi", "魚の棚で遅めのお昼", "A late lunch in the fish arcade"),
              ("suma", "maiko", "須磨・舞子", "Suma & Maiko", "海の見える山の上から、橋の夕日へ", "From a hilltop over the sea to sunset at the bridge")],
    spots=dict(
        himejieki=dict(
            kind=T("駅（スタート）", "Station (start)"),
            pre=T("姫路城は9:00に開きます。土曜・日曜・祝日は、大阪7:45発の新快速に乗ると姫路に8:49に着き、歩いて9:10ごろに入城口です（1,460円）。梅田のあたりのホテルなら7:30ごろ、なんばのあたりなら7:10ごろに出て、四つ橋線（なんば7:23発→西梅田7:31着・240円）で大阪駅へ。\n\n"
                  "平日は大阪7:27発の新快速があり、姫路8:32着。開く前に入城口に着けます。土日祝に9:00ちょうどに着きたいなら、大阪6:46発の快速（姫路8:21着）になります。\n\n"
                  "京都から来る人は、同じ新快速が京都7:14発です（平日は6:53発。2,210円）。三条のあたりからは、地下鉄で京都駅まで乗り換えを入れて約20分（260円）。\n\n"
                  "姫路駅の北口（姫路城口）を出ると、まっすぐ延びる大手前通りの先に姫路城が見えます。入城口までは歩いて約20分。神姫バスで「大手門前」まで乗り、そこから歩いて5分という行き方もあります。",
                  "The castle opens at 9:00. On Saturdays, Sundays and holidays, the 7:45 Special Rapid from Osaka reaches Himeji at 8:49, and you are at the ticket gate around 9:10 on foot (¥1,460). Leave a hotel around Umeda at about 7:30; from around Namba, leave about 7:10 and take the Yotsubashi Line (Namba 7:23 → Nishi-Umeda 7:31, ¥240) to Osaka Station.\n\n"
                  "On weekdays there is a 7:27 Special Rapid from Osaka, arriving 8:32, which gets you to the gate before it opens. To be there at 9:00 sharp on a weekend, it has to be the 6:46 rapid from Osaka (Himeji 8:21).\n\n"
                  "From Kyoto, the same Special Rapid leaves at 7:14 (6:53 on weekdays; ¥2,210). From around Sanjo, allow about 20 minutes by subway to Kyoto Station including the change (¥260).\n\n"
                  "From Himeji’s north exit (Himeji Castle exit), the castle stands at the end of the dead-straight Otemae-dori. It is about 20 minutes on foot to the ticket gate, or take a Shinki bus to “Otemon-mae” and walk 5 minutes."),
            post=T("朝ごはんを食べずに出てきた人は、えきそばを1杯食べてから歩いても、開城の少しあとには着けます。お城を出るまで2時間ほど何も食べられないので、何か入れておくと楽です。",
                   "If you left without breakfast, a bowl of ekisoba before you walk still gets you there soon after opening. You will not be able to eat for about two hours once inside, so it helps."),
            time=T("8:49", "8:49"), timeLabel=T("おすすめ到着時間：", "Recommended arrival: "),
            rows=[row("train", "行き：大阪7:45発（JR新快速）→ 姫路8:49着・1,460円（土日祝）。平日は7:27発→8:32着", "Getting there: Osaka 7:45 (JR Special Rapid) → Himeji 8:49, ¥1,460 (weekends and holidays). Weekdays: 7:27 → 8:32"),
                  row("train", "京都から：京都7:14発（同じ新快速）→ 姫路8:49着・2,210円（平日は6:53発→8:32着）", "From Kyoto: 7:14 (the same Special Rapid) → Himeji 8:49, ¥2,210 (weekdays 6:53 → 8:32)")]),
        himejijo=dict(
            pre=T("駅から大手前通りを歩いて、9:10ごろに入城口へ。朝いちばんは、団体や日帰りの人が着く前です（混み具合は日によります。桜や連休の時期は朝から並ぶことがあります）。",
                  "Walk up Otemae-dori from the station and reach the ticket gate around 9:10, ahead of most tour groups and day-trippers (it varies by day; in cherry-blossom season and on long weekends there can be queues from the start)."),
            post=T("入ったら寄り道せずに大天守へ。上の階ほど狭く、人が増えると階段で待つことになります。天守を下りてから、西の丸をゆっくり歩いてください。11:00ごろに出て、好古園へ。",
                   "Once in, go straight to the great keep: the upper floors are small, and the stairs back up when it fills. Take the West Bailey slowly afterwards. Leave around 11:00 for Kokoen."),
            time=T("9:10〜11:00", "9:10–11:00")),
        kokoen=dict(
            pre=T("お城を出たら、ここで朝ごはん代わりの休憩を。活水軒の食事は11:00からなので、ちょうど始まる時間に着きます。席の予約はできないので、先に活水軒に入り、そのあと庭を歩く順番が確実です。軽く済ませて、明石で明石焼を食べる余裕を残しておくのもいいと思います。",
                  "After the castle, this is your breakfast-and-rest stop. Kassuiken starts serving meals at 11:00, just as you arrive. It takes no reservations, so eat first and walk the gardens afterwards. Keep it light if you want room for akashiyaki in Akashi."),
            post=T("12:00ごろに出て、姫路駅まで歩いて約20分。姫路12:27発の新快速で明石へ（12:50着・660円）。次は12:42発（13:05着）です。",
                   "Leave around 12:00; it is about 20 minutes on foot to Himeji Station. Take the 12:27 Special Rapid to Akashi (12:50, ¥660); the next is 12:42 (arr. 13:05)."),
            time=T("11:05〜12:00", "11:05–12:00"),
            rows=[row("train", "次へ：姫路12:27発（JR新快速）→ 明石12:50着・660円", "Next: Himeji 12:27 (JR Special Rapid) → Akashi 12:50, ¥660")]),
        shosha=dict(
            pre=T("行くなら、明石・須磨・舞子の代わりに午後をまるごと使います。好古園を出たら、すぐ前のバス停「聴覚特別支援学校・好古園」から神姫バスで書写山ロープウェイへ（12:40発→13:07着・320円）。",
                  "If you go, it replaces Akashi, Suma and Maiko and takes the whole afternoon. After Kokoen, take the Shinki bus from the stop right outside (“Chokaku Tokubetsu Shien Gakko / Kokoen”) to Shoshazan Ropeway (12:40 → 13:07, ¥320)."),
            post=T("帰りは書写山ロープウェイ16:32発のバスで姫路駅北口に17:02着（平日は17:05着）。駅前で晩ごはんを食べて、明かりの入ったお城を大手前通りから眺めてから帰れます（ライトアップは日没〜24:00）。姫路17:11発の新快速なら大阪18:13着、17:26発なら18:28着、そのあとも19:26発（20:28着）、20:16発（21:18着）などがあります（1,460円）。京都へは17:11発→18:44着（2,210円）。",
                   "Coming back, the 16:32 bus reaches Himeji Station north exit at 17:02 (17:05 on weekdays). Have dinner by the station and look up Otemae-dori at the lit castle before you go (lit from sunset to midnight). The 17:11 Special Rapid reaches Osaka at 18:13 and the 17:26 at 18:28; later ones include 19:26 (20:28) and 20:16 (21:18); ¥1,460. For Kyoto, 17:11 → 18:44 (¥2,210)."),
            time=T("13:10〜16:30", "13:10–16:30"),
            rows=[row("train", "行き：聴覚特別支援学校・好古園 12:40発（神姫バス）→ 書写山ロープウェイ 13:07着・320円", "Getting there: Kokoen stop 12:40 (Shinki bus) → Shoshazan Ropeway 13:07, ¥320"),
                  row("train", "帰り：書写山ロープウェイ16:32発（バス）→ 姫路駅北口17:02着（平日17:05着）、姫路17:11発か17:26発（新快速）→ 大阪18:13着・18:28着・1,460円", "Return: bus from Shoshazan Ropeway 16:32 → Himeji Station north exit 17:02 (weekdays 17:05); Himeji 17:11 or 17:26 (Special Rapid) → Osaka 18:13 / 18:28, ¥1,460")]),
        akashi=dict(
            pre=T("JR明石駅に12:50に着いて、南へ歩いて3分。13時ごろは昼網の魚が並んでいる時間です。先にたこ磯で遅めのお昼、そのあと市場を歩きます。",
                  "Arrive at JR Akashi at 12:50; the arcade is 3 minutes south. Around 13:00 the midday catch is on the stalls. Have a late lunch at Takoiso first, then walk the market."),
            post=T("山陽電車の山陽明石駅（JRの駅のすぐ南）から須磨浦公園へ。14:04発の普通なら乗り換えなし、14:10発の直通特急なら山陽垂水で乗り換えて、どちらも14:25着（390円）。",
                   "Go on from Sanyo-Akashi Station (just south of the JR station) to Sumaura-koen: the 14:04 local runs through, or take the 14:10 limited express and change at Sanyo-Tarumi. Both arrive at 14:25 (¥390)."),
            time=T("12:55〜14:00", "12:55–14:00"),
            rows=[row("train", "次へ：山陽明石14:04発（山陽電車）→ 須磨浦公園14:25着・390円", "Next: Sanyo-Akashi 14:04 (Sanyo) → Sumaura-koen 14:25, ¥390")]),
        suma=dict(
            pre=T("14:25に着いて、14:30のロープウェーで上ります。喫茶コスモスのラストオーダーは15:30、展望閣の屋上は16:20までなので、着いたら先に展望閣へ。",
                  "Arrive at 14:25 and take the 14:30 ropeway. Café Cosmos takes last orders at 15:30 and the observatory roof closes at 16:20, so head for the observatory first."),
            post=T("15:45ごろのロープウェーで下りて、須磨浦公園15:56発の山陽電車で舞子公園へ（16:10着・250円）。",
                   "Come down on the ropeway around 15:45 and take the 15:56 Sanyo train to Maiko-koen (16:10, ¥250)."),
            time=T("14:30〜15:50", "14:30–15:50"),
            notices=[notice("火曜と、冬の平日は休み", "Closed Tuesdays and winter weekdays",
                            "火曜日（祝日は営業）と、2026年12月2日〜2027年2月5日の平日は休みです（この期間は土日祝だけ。12/12・13・19・20、1/16・17も休園）。その日は明石でゆっくりして明石城跡まで歩き、山陽明石から直通特急で舞子公園へ（4分・250円）。",
                            "Closed on Tuesdays (open on holidays) and on weekdays from 2 December 2026 to 5 February 2027 (weekends and holidays only in that period; also closed 12, 13, 19, 20 Dec and 16, 17 Jan). On those days linger in Akashi, walk up to the castle ruins, and take the limited express from Sanyo-Akashi to Maiko-koen (4 min, ¥250).")],
            rows=[row("train", "次へ：須磨浦公園15:56発（山陽電車）→ 舞子公園16:10着・250円", "Next: Sumaura-koen 15:56 (Sanyo) → Maiko-koen 16:10, ¥250")]),
        maiko=dict(
            kind=T("公園・夕日", "Park & sunset"),
            blurb=T("世界最大級のつり橋のたもとで、海に沈む夕日を。駅から歩いてすぐです。",
                    "Watch the sun go down by one of the world’s longest suspension bridges, a few minutes from the station."),
            pre=T("16:10に舞子公園駅に着きます。11月下旬の日の入りは16:50ごろ。先にプロムナードを歩いて（入館は17:30まで）、日が沈む時間に海ぞいの松林へ下りるとちょうどいい順番です。この時間割で夕日に合うのは秋から冬で、夏は日の入りが19時ごろになります。",
                  "You reach Maiko-koen Station at 16:10. Sunset in late November is around 16:50. Walk the promenade first (last entry 17:30), then come down to the pines by the water as the sun sets. This timing suits autumn and winter; in summer the sun sets around 19:00."),
            post=T("帰りはJR舞子駅から。17:33発の快速で大阪に18:22着（840円・乗り換えなし）。朝が早かった日は、これでホテルに戻って近くで晩ごはんにするのが楽です。\n\n"
                   "まだ元気なら、同じ快速を三ノ宮で降りて（17:53着・320円）、神戸で晩ごはん。南京町や元町のあたりへは歩いて10分ほどです（神戸のマップも見てください）。三ノ宮からは新快速で大阪まで21分（20:07発→20:28着・420円）。\n\n"
                   "舞子から大阪への最終は23:45発（0:46着）。京都へは17:38発に乗り、神戸で新快速に乗り換えて18:59着（1,640円）。京都への最後は舞子23:11発（三ノ宮で新快速に乗り換え、0:30着）です。",
                   "Go home from JR Maiko: the 17:33 rapid reaches Osaka at 18:22 (¥840, direct). After the early start, heading back and eating near your hotel is the easy option.\n\n"
                   "If you still have energy, get off that same train at Sannomiya (17:53, ¥320) for dinner in Kobe; Nankinmachi and Motomachi are about 10 minutes on foot (see the Kobe map). From Sannomiya the Special Rapid takes 21 minutes to Osaka (20:07 → 20:28, ¥420).\n\n"
                   "The last train from Maiko to Osaka is the 23:45 (arr. 0:46). For Kyoto, take the 17:38 and change to the Special Rapid at Kobe (Kyoto 18:59, ¥1,640); the last connection leaves Maiko at 23:11 (change at Sannomiya, Kyoto 0:30)."),
            time=T("16:15〜17:25", "16:15–17:25"),
            rows=[row("train", "帰り：舞子17:33発（JR快速）→ 大阪18:22着・840円。三ノ宮で降りるなら17:53着・320円、三ノ宮20:07発（新快速）→ 大阪20:28着・420円",
                      "Home: Maiko 17:33 (JR rapid) → Osaka 18:22, ¥840. Or off at Sannomiya 17:53 (¥320), then Sannomiya 20:07 (Special Rapid) → Osaka 20:28, ¥420"),
                  row("train", "最終：舞子23:45発 → 大阪0:46着。京都へは舞子23:11発 → 三ノ宮で新快速に乗り換え → 京都0:30着・1,640円", "Last trains: Maiko 23:45 → Osaka 0:46. For Kyoto, Maiko 23:11 → change to the Special Rapid at Sannomiya → Kyoto 0:30, ¥1,640")]),
    ),
    hints=[
        ("shosha", {"any": ["shosha"], "andAny": ["akashi", "suma", "maiko"]},
         "書写山に行く日は、姫路で1日が終わります。明石・須磨・舞子は外してください（須磨浦山上遊園の最終入場16:30にも、舞子の夕日にも間に合いません）。明石焼だけは、姫路17:11発の新快速で明石17:35着、19:00までのたこ磯で晩ごはんにできます。",
         "A Mt. Shosha day ends in Himeji: drop Akashi, Suma and Maiko (you would miss both the 16:30 last entry at Sumaura and the sunset at Maiko). Akashiyaki alone still works as dinner: the 17:11 Special Rapid reaches Akashi at 17:35, and Takoiso is open until 19:00."),
        ("shosha", {"any": ["shosha"], "none": ["kokoen"]},
         "好古園に寄らない日は、姫路駅北口の10番のりばから神姫バスで書写山ロープウェイへ（約25〜30分・320円）。",
         "Skipping Kokoen? Take the Shinki bus from stop 10 at Himeji Station north exit to Shoshazan Ropeway (about 25–30 min, ¥320)."),
        ("maiko", {"any": ["maiko"], "none": ["suma"]},
         "須磨に寄らない日は、山陽明石から直通特急で舞子公園へ4分（250円）。日の入りまで時間があるので、明石で明石城跡まで歩くか、舞子のプロムナードをゆっくりどうぞ。",
         "Skipping Suma? The limited express from Sanyo-Akashi reaches Maiko-koen in 4 minutes (¥250). There is time before sunset, so walk up to Akashi Castle ruins or take the promenade slowly."),
        ("suma", {"any": ["suma"], "none": ["maiko"]},
         "舞子に寄らない日は、須磨浦公園15:55発の電車に乗り、次の山陽須磨で阪神の特急「大阪梅田行」に乗り換えて16:52着（740円）。",
         "Not going to Maiko? Take the 15:55 from Sumaura-koen one stop to Sanyo-Suma and change to the Hanshin limited express for Osaka-Umeda (16:52, ¥740)."),
        ("akashi", {"any": ["akashi"], "none": ["suma", "maiko", "shosha"]},
         "明石で終わる日は、JR明石駅から新快速で大阪まで約38分（960円）。",
         "Ending in Akashi? The Special Rapid from JR Akashi reaches Osaka in about 38 minutes (¥960)."),
    ],
)
NOTE_HEAD = ("姫路・明石・須磨の1日ルート（himeji/ のページ専用。形は eizan-line.json と同じ）。起点は大阪の梅田〜難波のあたりのホテル。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む"
             "（himeji.json＝9〜10時に出発して姫路城は14時半ごろ、himeji-early.json＝姫路城の9:00の開城に合わせる）。このファイル：")
NOTE_TAIL = (" 写真は Toshi の写真ライブラリから選んだもの（須磨浦公園と明石は2023年6月16日の Nikon D7000、姫路城は2023年6月と2024年8・9月、好古園は2024年9月の夜、舞子は2023年7月。1か所10枚以内・横の写真だけ・長辺1600px・位置情報なし）。"
             "書写山 圓教寺は Toshi がまだ行っていない場所で、写真は Wikimedia Commons（photos の要素が {file, credit}）、文章は公式サイトの情報だけ。"
             "info.source は確認した出典、info.checked は確認日。入口で困ること（休み・現金・再入城不可・運休）は caution と head つきの notices。"
             "店名を出しているのは、Toshi の写真がある「たこ磯」と、公式サイトで時間を確かめた活水軒・双樹庵（好古園の中）・えきそば（姫路駅のホーム）だけ。"
             "plan.defaultPicks は最初から選ばれている場所で、各スポットの「おすすめ訪問時間」はこの組み合わせの時間割（11月下旬・土曜のダイヤ）。このファイルは scripts/build_himeji_data.py で作る（直接直さない）。")


def build(c):
    cs = c["spots"]
    spots = []
    for i, sid in enumerate(c["order"], 1):
        b, o = S[sid], cs.get(sid, {})
        parts = [o.get("title") or TITLE[sid], o.get("pre"), b["body"], o.get("post")]
        tm = o["time"]
        lead = o.get("timeLabel") or T("おすすめ訪問時間：", "Recommended visit time: ")
        text = {}
        for lang in ("ja", "en"):
            text[lang] = "\n\n".join(p[lang].strip() for p in parts if p) + "\n\n" + lead[lang] + tm[lang]
        out = {"no": i, "id": sid, "name": o.get("name") or b["name"], "kind": o.get("kind") or b["kind"], "blurb": o.get("blurb") or b["blurb"], "lat": b["lat"], "lng": b["lng"]}
        if b.get("caution"):
            out["caution"] = b["caution"]
        out["text"] = text
        out["gmaps"] = b["gmaps"]
        out["links"] = b["links"] + [l for l in o.get("links", []) if l["url"] not in [x["url"] for x in b["links"]]]
        out["info"] = info(b["rows"] + o.get("rows", []), tip=b["tip"], verified=b.get("verified", True), cash=b.get("cash", False), source=b.get("source"), checked=b.get("checked"))
        out["photos"] = photos(sid, b.get("_extra"))
        out["notices"] = o.get("notices", []) + b.get("notices", [])
        spots.append(out)
    NO = {s["id"]: s["no"] for s in spots}
    N = lambda ids: [NO[k] for k in ids]
    castle = N(["himejijo", "kokoen", "shosha"])
    data = {
        "id": "himeji", "course": c["id"],
        "_note": NOTE_HEAD + c["file"] + "。" + NOTE_TAIL,
        "sections": [{"first": NO[a], "last": NO[b], "area": T(aj, ae), "title": T(tj, te)} for a, b, aj, ae, tj, te in c["sections"]],
        "plan": {"_note": "「選んで回る」の設定。姫路駅だけは、姫路城・好古園・書写山のどれかを選ぶと自動で入る。defaultMode: pick で最初から「選んで回る」、defaultPicks は1日で無理なく回れる組み合わせ（時間割どおり）。それ以外は時間割の外の寄り道。",
                 "defaultMode": "pick",
                 "picks": [s["no"] for s in spots if s["id"] != "himejieki"],
                 "defaultPicks": N(c["default"]),
                 "auto": {str(NO["himejieki"]): {"any": castle}},
                 "hints": [{"spot": NO[sp], "rule": {k: N(v) for k, v in rule.items()}, "text": T(ja, en)} for sp, rule, ja, en in c["hints"]]},
        "photoBase": "../images/himeji/",
        "spots": spots,
    }
    out = f"{R}/data/routes/{c['file']}"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


assert set(LATE["order"]) == set(EARLY["order"]) == set(S)
for c in (LATE, EARLY):
    build(c)
