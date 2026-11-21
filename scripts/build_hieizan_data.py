#!/usr/bin/env python3
"""京都から日帰り 比叡山延暦寺と坂本 のデータ（data/routes/hieizan.json）を書き出す。

使い方: python3 scripts/build_hieizan_data.py
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 写真は images/hieizan/ にある。並べる順番は下の PHOTOS（自分の写真はファイル名だけ、
  ネットから借りた写真（Wikimedia Commons）は cc(...) で {"file", "credit": {"author", "license", "page"}} にする）
- オーナーの写真は少ない：東塔の鐘楼ともみじ・杉木立（2016年11月13日）、日吉大社の赤鳥居（同じ日）、山頂からの眺め（同じ日）、
  近江神宮（2025年1月18日）、八瀬のもみじとケーブル八瀬駅・八瀬比叡山口駅（2024年12月3日）。ほかは Wikimedia Commons。
  オーナーの写真がない場所（坂本の町・旧竹林院・坂本ケーブル・西塔・横川）は、文章にも行った日などは書かない
- 季節で変わるもの（2026年11月21日に確認）:
  叡山ケーブル・ロープウェイと比叡山内シャトルバスは 2026年3月20日〜12月6日。冬は運休（2027年の再開日は未発表）
  根本中堂は2026年1月から約2年間、堂内に入れない。修学ステージは2026年11月まで
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/hieizan"
OUT = f"{R}/data/routes/hieizan.json"
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


def own(pid, nums):
    return [f"{pid}-{i}.jpg" for i in nums]


H663 = ("663highland", "CC BY 2.5")
NEVIN = ("NevinThompson", "CC BY-SA 4.0")
KENPEI = ("KENPEI", "CC BY-SA 3.0")
PHOTOS = {
    "kyoto": [cc("kyoto-1.jpg", "SONIC BLOOMING", "CC BY-SA 4.0", "Hieizan-Sakamoto Station.jpg")],
    "omijingu": own("omijingu", range(1, 6)),
    "sakamoto": [cc("sakamoto-1.jpg", *NEVIN, "Stone path and water channel, Sakamoto, Otsu, August 2019.jpg"),
                 cc("sakamoto-2.jpg", "Motokoka", "CC BY-SA 4.0", "Ano Zumi.jpg"),
                 cc("sakamoto-3.jpg", *NEVIN, "Sakamoto street with stone wall, foot of Mount Hiei, Otsu, August 2019.jpg"),
                 cc("sakamoto-4.jpg", "Punkssand", "CC0", "坂本比叡山口駅駅舎.jpg")],
    "chikurin": [cc("chikurin-1.jpg", *H663, "Old chikurinin04st3200.jpg"),
                 cc("chikurin-2.jpg", *H663, "Old chikurinin01s4592.jpg"),
                 cc("chikurin-3.jpg", *H663, "Old chikurinin02st3200.jpg")],
    "hiyoshi": [cc("hiyoshi-1.jpg", *H663, "Hiyoshi-taisha nishihongu-romon01s4592.jpg"),
                "hiyoshi-2.jpg",
                cc("hiyoshi-3.jpg", *H663, "Hiyoshi-taisha03s4592.jpg"),
                cc("hiyoshi-4.jpg", *H663, "Hiyoshi-taisha nishihongu-honden01n4592.jpg"),
                cc("hiyoshi-5.jpg", *H663, "Hiyoshi-taisha omiyabashi01s4592.jpg"),
                cc("hiyoshi-6.jpg", *H663, "Hiyoshi-taisha higashihongu-romon02s4592.jpg")],
    "cable": [cc("cable-1.jpg", "Saigen Jiro", "CC0", "Cable car at Cable Sakamoto Station.jpg"),
              cc("cable-2.jpg", "Saigen Jiro", "CC0", "Cable Sakamoto Station, ekisha.jpg"),
              cc("cable-3.jpg", "江戸村のとくぞう", "CC BY-SA 4.0", "Cable Enryakuji Station 201125e.jpg"),
              cc("cable-4.jpg", *NEVIN, "Sakamoto Cable car approaching a tunnel, Otsu, August 2019.jpg"),
              cc("cable-5.jpg", *NEVIN, "Observation deck at the top of the Sakamoto Cable, Otsu, August 2019.jpg")],
    "toto": ["toto-1.jpg",
             cc("toto-2.jpg", *H663, "Enryakuji Konponchudo04n4272.jpg"),
             cc("toto-3.jpg", "Zairon", "CC BY 4.0", "Otsu Enryaku-ji Daikodo Exterior 1.jpg"),
             cc("toto-4.jpg", *H663, "Enryakuji Amidado02n3200.jpg"),
             cc("toto-5.jpg", *H663, "Enryakuji Amidado01n3200.jpg"),
             "toto-6.jpg", "toto-7.jpg", "toto-8.jpg",
             cc("toto-9.jpg", "Zairon", "CC BY 4.0", "Otsu Enryaku-ji View to Lake Biwa.jpg")],
    "saito": [cc("saito-1.jpg", *H663, "Enryakuji Ninaido01n3200.jpg"),
              cc("saito-2.jpg", *KENPEI, "Enryakuji Shakado.jpg"),
              cc("saito-3.jpg", *KENPEI, "Enryakuji ninaido.jpg"),
              cc("saito-4.jpg", *KENPEI, "Enryakuji jyodoin1.jpg"),
              cc("saito-5.jpg", *H663, "Enryakuji Saito01n3200.jpg"),
              cc("saito-6.jpg", "Suikotei", "CC BY 4.0", "Saito Shoro.jpg")],
    "yokawa": [cc("yokawa-1.jpg", "PlusMinus", "CC BY-SA 3.0", "Enryakuji yokawachudo.jpg"),
               cc("yokawa-2.jpg", *KENPEI, "Enryakuji yokawa cyudo2.jpg"),
               cc("yokawa-3.jpg", *KENPEI, "Enryakuji yokawa cyudo1.jpg"),
               cc("yokawa-4.jpg", "tataquax", "CC BY-SA 2.0", "延暦寺の元三大師堂.jpg"),
               cc("yokawa-5.jpg", "Suikotei", "CC BY 4.0", "Yokawa Shoro.jpg")],
    "sancho": ["sancho-1.jpg",
               cc("sancho-2.jpg", "Yasu", "CC BY-SA 3.0", "Eizan Ropeway.jpg"),
               cc("sancho-3.jpg", "Suikotei", "CC BY 4.0", "Eizan Ropeway at Hiei-Sancho Station 20260502 02.jpg"),
               cc("sancho-4.jpg", "江戸村のとくぞう", "CC BY-SA 4.0", "Rope Hiei Station 201125c.jpg")],
    "yase": own("yase", range(1, 8)),
}

ENR = link("official", "延暦寺 巡拝時間・料金", "Enryaku-ji: hours and fees (Japanese)", "https://www.hieizan.or.jp/tickets/")
ENRTOP = link("official", "比叡山延暦寺 公式サイト", "Enryaku-ji (official)", "https://www.hieizan.or.jp/")
TT = link("timetable", "比叡山・びわ湖 交通案内＆時刻表（シャトルバス・ケーブル）", "Mt. Hiei transport guide and timetables (Japanese)", "https://www.hieizan.gr.jp/timetable/")
TICKET = link("info", "比叡山のおトクなチケット一覧", "Mt. Hiei passes and tickets (Japanese)", "https://www.hieizan.gr.jp/ticket/")
SAKACABLE = link("official", "坂本ケーブル 時刻表・運賃", "Sakamoto Cable: timetable and fares (Japanese)", "https://sakamoto-cable.jp/guide/")
EIZANCABLE = link("timetable", "叡山ケーブル・ロープウェイ 時刻表", "Eizan Cable & Ropeway timetable (Japanese)", "https://www.keifuku.co.jp/cms/eizan_timetable/")

WINTER = {"from": None, "to": None, "url": "https://www.hieizan.gr.jp/timetable/",
          "head": T("12月7日から春まで、京都側のケーブル・ロープウェイと山内のシャトルバスは運休", "From 7 December until spring, the Kyoto-side cable car and ropeway and the shuttle bus on the mountain do not run"),
          "text": T("叡山ケーブル・ロープウェイ（八瀬側）と比叡山内シャトルバスの2026年の運行は12月6日（日）までです（平日のケーブルは12月4日まで）。2026年は3月20日に再開しました。2027年の再開日はまだ発表されていません（要確認）。\n\n"
                    "冬に行くなら、通年で動く坂本ケーブルで上り、東塔を見て、同じケーブルで坂本へ下ります。西塔へは歩いて片道20〜40分の山道。横川は歩くと片道100分以上かかるので、冬は行けないと考えてください。\n\n"
                    "山の上は京都の町よりずっと寒く、雪が積もる日があります。秋でも上着を1枚多く持ってください。",
                    "The Eizan Cable and Ropeway (Yase side) and the shuttle bus on Mt. Hiei run until Sunday 6 December in 2026 (the cable’s weekday service ends on 4 December). In 2026 they restarted on 20 March; the 2027 date has not been announced yet (please check).\n\n"
                    "In winter, go up by the Sakamoto Cable, which runs all year, see the Todo area and come back down the same way to Sakamoto. Saito is a 20–40 minute hill path each way on foot. Yokawa is more than 100 minutes’ walk each way: treat it as out of reach in winter.\n\n"
                    "The mountain is much colder than Kyoto and there is snow on some days. Even in autumn, bring one more layer.")}
CHUDO = {"from": None, "to": None, "url": "https://www.hieizan.or.jp/renovation/",
         "head": T("根本中堂は大改修中。2026年1月から約2年間、お堂の中には入れません", "Konpon Chudo is under major repair: the interior is closed for about two years from January 2026"),
         "text": T("国宝の根本中堂は2016年から約15年がかりの大改修中で、建物は工事の覆い（素屋根）の中です。2026年1月から約2年間は堂内の拝観ができません。\n\n"
                   "そのあいだ、ご本尊の御前立（おまえだち）の薬師如来像と「不滅の法灯」は、すぐ近くの萬拝堂（まんぱいどう）に移されていて、ふだんより近くでお参りできます。\n\n"
                   "屋根の高さまで上がれる見学用の「修学ステージ」は2026年11月まで（公式サイトの別のページでは12月頃まで）。12月から覆いの解体工事が始まり、ステージは閉まります。\n\n"
                   "根本中堂の十二神将像は修理を終えて、国宝殿に12体そろって展示されています（2027年12月までの予定。国宝殿は別に500円）。",
                   "The Konpon Chudo, a National Treasure, has been under a repair of about 15 years since 2016 and stands inside a scaffolding shed. For about two years from January 2026 you cannot go inside.\n\n"
                   "During that time the stand-in image of the hall’s Yakushi Buddha and the “Inextinguishable Dharma Light” have been moved to the Manpai-do hall close by, where you can see them from nearer than usual.\n\n"
                   "The visitors’ viewing stage, level with the eaves, is open until November 2026 (another page of the official site says around December). From December the shed starts coming down and the stage closes.\n\n"
                   "The hall’s Twelve Divine Generals have been restored and are shown together in the Kokuhoden museum (planned until December 2027; the museum is ¥500 extra).")}

S = [
    dict(id="kyoto", name=T("京都駅（JR湖西線で坂本へ）", "Kyoto Station (JR Kosei line)"), kind=T("駅", "Station"),
         blurb=T("京都駅からJR湖西線で比叡山坂本駅まで16分。近江神宮に寄る人は、大津京駅で京阪電車に乗り換えます。",
                 "16 minutes from Kyoto Station to Hieizan-Sakamoto on the JR Kosei line. For Omi Jingu, change to the Keihan line at Otsukyo."),
         lat=34.98586, lng=135.75876,
         text=T("京都駅（JR湖西線で坂本へ）\n\n"
                "比叡山は京都と滋賀の境にある山です。このマップは、滋賀側の坂本（さかもと）からケーブルカーで上がり、延暦寺を回って、京都側の八瀬（やせ）へ下ります。坂本の町と日吉大社は朝のほうが静かで、帰りは出町柳に着くので、この向きにしました。\n\n"
                "① まっすぐ坂本へ：京都駅（3番線）からJR湖西線で比叡山坂本駅へ。16〜18分・320円。平日は 7:47発→8:03着、8:13発→8:30着、8:19発（新快速）→8:37着。\n\n"
                "② 近江神宮に寄る：同じ湖西線で大津京（おおつきょう）駅まで10分・240円。歩いて5分の京阪大津京駅から、京阪石山坂本線で1駅の近江神宮前へ（200円）。平日は京都 7:47発→大津京 7:57着、京阪大津京 8:08発→近江神宮前 8:09着。\n\n"
                "湖西線は京都駅の3番線から出ることが多く、行き先は「近江舞子」「近江今津」「敦賀」など。同じホームから琵琶湖線（米原方面）も出ます。乗る前に「湖西線」と書いてあるか見てください。まちがえて琵琶湖線に乗ったら、次の山科で乗り換えられます。\n\n"
                "ICカードはJR・京阪・叡山電車・シャトルバスで使えます。京都側の叡山ケーブル・ロープウェイは現金だけです。\n\n"
                "京都駅前から比叡山へ直通のバス（比叡山ドライブバス）もありますが、1日3〜6便で、冬は走りません。\n\nおすすめ訪問時間：7:47発の電車に乗る",
                "Kyoto Station (JR Kosei line)\n\n"
                "Mt. Hiei stands on the border of Kyoto and Shiga. This route goes up by cable car from Sakamoto on the Shiga side, round Enryaku-ji, and down to Yase on the Kyoto side. Sakamoto and Hiyoshi Taisha are quieter in the morning, and you finish at Demachiyanagi, back in the city.\n\n"
                "1) Straight to Sakamoto: JR Kosei line from Kyoto Station (platform 3) to Hieizan-Sakamoto, 16–18 minutes, ¥320. On weekdays: 7:47→8:03, 8:13→8:30, 8:19 (rapid)→8:37.\n\n"
                "2) Via Omi Jingu: the same line as far as Otsukyo (10 min, ¥240). Walk 5 minutes to Keihan-Otsukyo station and ride one stop to Omijingu-mae (¥200). On weekdays: Kyoto 7:47→Otsukyo 7:57, Keihan-Otsukyo 8:08→Omijingu-mae 8:09.\n\n"
                "Kosei line trains mostly leave from platform 3, bound for Omi-Maiko, Omi-Imazu or Tsuruga. Biwako line trains (towards Maibara) use the same platform, so check that the sign says Kosei line. If you board the wrong one, change at Yamashina, the next stop.\n\n"
                "IC cards work on JR, Keihan, the Eizan railway and the shuttle bus. The Eizan Cable and Ropeway on the Kyoto side take cash only.\n\n"
                "There is also a direct bus from Kyoto Station to Mt. Hiei, but only 3–6 a day, and none in winter.\n\nRecommended visit time: take the 7:47 train"),
         gmaps=[gm("京都駅", "Kyoto Station", 34.98586, 135.75876, "京都駅"), gm("比叡山坂本駅", "Hieizan-Sakamoto Station", 35.07066, 135.87835, "比叡山坂本駅")],
         links=[TT, TICKET],
         notices=[WINTER],
         info=info([row("train", "京都 → 比叡山坂本：JR湖西線 16〜18分・320円。平日 7:47→8:03、8:13→8:30、8:19→8:37／土曜 7:49→8:05、8:15→8:30",
                        "Kyoto → Hieizan-Sakamoto: JR Kosei line, 16–18 min, ¥320. Weekdays 7:47→8:03, 8:13→8:30, 8:19→8:37; Saturdays 7:49→8:05, 8:15→8:30"),
                    row("train", "近江神宮に寄る：京都 → 大津京（JR 10分・240円）、歩いて5分、京阪大津京 → 近江神宮前（1分・200円）。平日 京都7:47発→近江神宮前8:09着／土曜 7:49発→8:13着",
                        "Via Omi Jingu: Kyoto → Otsukyo (JR, 10 min, ¥240), 5 min on foot, Keihan-Otsukyo → Omijingu-mae (1 min, ¥200). Weekdays Kyoto 7:47 → Omijingu-mae 8:09; Saturdays 7:49 → 8:13"),
                    row("train", "帰りを坂本にする日：比叡山坂本 → 京都 17:01、17:13、17:32発（平日。16〜18分・320円）",
                        "If you come back via Sakamoto: Hieizan-Sakamoto → Kyoto at 17:01, 17:13 and 17:32 (weekdays; 16–18 min, ¥320)")],
                   tip=T("電車の時刻と運賃は乗換案内（2026年11月24日（火）と28日（土）の時刻）で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Train times and fares were checked on a route planner for Tuesday 24 and Saturday 28 November 2026. The photo is from Wikimedia Commons (author and license shown on the photo)."))),
    dict(id="omijingu", name=T("近江神宮", "Omi Jingu"), kind=T("神社（寄り道）", "Shrine (side trip)"),
         blurb=T("朱色の楼門と、長い石段。百人一首の最初の歌を詠んだ天智天皇をまつる、かるたの神社です。",
                 "A vermilion gate at the top of a long flight of steps. The shrine of Emperor Tenji, author of the first poem of the Hyakunin Isshu, and home of competitive karuta."),
         lat=35.03244, lng=135.85131,
         text=T("近江神宮（おうみじんぐう）\n\n"
                "京阪の近江神宮前駅から歩いて約10分。大きな鳥居をくぐり、森の中の参道を上ると、石段の上に朱色の楼門が見えます（写真1枚目）。\n\n"
                "まつられているのは、1350年ほど前にこの大津に都を置いた天智天皇（てんじてんのう）です。神社ができたのは1940年。百人一首の1番目の歌が天智天皇の歌なので、競技かるたの名人・クイーンを決める試合がここで開かれます。漫画『ちはやふる』の舞台としても知られています。\n\n"
                "天智天皇は日本で初めて水時計（漏刻＝ろうこく）を作らせた人でもあり、境内に漏刻や日時計が置かれ、時計館宝物館があります。\n\n"
                "私が行ったのは2025年1月18日の朝。人が少なく、楼門に朝日が当たってきれいでした。写真5枚目は、花を浮かべた手水（ちょうず）です。\n\n"
                "参拝だけなら30分で足ります。延暦寺の3つのエリアを全部回る日は時間がきついので、ここは外すか、8:50には出てください。近江神宮前 9:00発の電車で坂本比叡山口に9:09に着きます。\n\nおすすめ訪問時間：8:20〜8:50",
                "Omi Jingu\n\n"
                "About 10 minutes on foot from Omijingu-mae station on the Keihan line. Pass under the big torii, walk up through the woods, and the vermilion gate appears at the top of the stone steps (photo 1).\n\n"
                "The shrine is dedicated to Emperor Tenji, who made Otsu his capital some 1,350 years ago; the shrine itself dates from 1940. The first poem of the Hyakunin Isshu is his, so the national karuta championship finals are held here, and the shrine is known as the setting of the manga Chihayafuru.\n\n"
                "Tenji also had Japan’s first water clock built. There are a water clock and sundials in the grounds, and a clock museum.\n\n"
                "I went on the morning of 18 January 2025: few people, and the gate catching the early sun. Photo 5 is the purification basin with flowers floating in it.\n\n"
                "Half an hour is enough for the shrine itself. If you plan to see all three areas of Enryaku-ji, time is tight: skip this, or leave by 8:50. The 9:00 train from Omijingu-mae reaches Sakamoto-hieizanguchi at 9:09.\n\nRecommended visit time: 8:20–8:50"),
         gmaps=[gm("近江神宮", "Omi Jingu", 35.03244, 135.85131, "近江神宮 大津市"), gm("近江神宮前駅", "Omijingu-mae Station", 35.02817, 135.85574, "近江神宮前駅")],
         links=[link("official", "近江神宮 公式サイト", "Omi Jingu (official, Japanese)", "https://oumijingu.org/")],
         info=info([row("hours", "参拝 6:00〜18:00", "Open for worship 6:00–18:00"),
                    row("fee", "参拝は無料。時計館宝物館は 9:30〜16:30（入館16:00まで）、料金は要確認", "Free. Clock museum 9:30–16:30 (last entry 16:00); its fee: please check"),
                    row("train", "近江神宮前 → 坂本比叡山口：京阪石山坂本線 9分・200円。平日 9:00、9:14、9:24発／土曜 9:13、9:32発", "Omijingu-mae → Sakamoto-hieizanguchi: Keihan Ishiyama-Sakamoto line, 9 min, ¥200. Weekdays 9:00, 9:14, 9:24; Saturdays 9:13, 9:32")],
                   tip=T("時間は近江神宮の公式サイト、電車は乗換案内（2026年11月24日・28日）で確認しました。駅から歩く時間は地図で測った目安です。", "Hours are from the shrine’s website; trains from a route planner (24 and 28 November 2026). The walking time from the station is measured on a map."))),
    dict(id="sakamoto", name=T("坂本の町（穴太衆積みの石垣）", "Sakamoto: the stone-wall town"), kind=T("門前町", "Temple town"),
         blurb=T("延暦寺のふもとの門前町。自然の石をそのまま積んだ「穴太衆積み」の石垣が、参道の両側に続きます。",
                 "The temple town at the foot of Enryaku-ji. Walls of uncut natural stone, laid by the Ano masons, line the avenue."),
         lat=35.07090, lng=135.86900,
         text=T("坂本の町（穴太衆積み＝あのうしゅうづみ の石垣）\n\n"
                "京阪の坂本比叡山口駅を出て、山のほうへ。日吉大社へまっすぐ上る広い参道が「日吉馬場（ひよしばんば）」です。日吉大社の入口まで歩いて約10分。JR比叡山坂本駅からは同じ道を約20分上ります（バスなら7分・250円。9:10発から30分おき）。\n\n"
                "道の両側の石垣を見てください。大きさも形もちがう自然の石を、削らずに組み合わせて積んであります。坂本にいた石工の集団「穴太衆」の仕事で、戦国時代には城の石垣にも使われた積み方です。「石の声を聞け」と伝えられてきたそうです。\n\n"
                "石垣の中は「里坊（さとぼう）」です。山の上で修行を終えた延暦寺のお坊さんが、年をとってから暮らした住まいで、今も多く残っています。ほとんどは中に入れません。門の外から見るだけにしてください。\n\n"
                "石垣がいちばん立派なのは、参道から南へ少し入った滋賀院門跡（しがいんもんぜき）のまわりです。歴代の天台座主（延暦寺の住職）が暮らした所で、中も拝観できます（9:00〜16:00、500円）。\n\n"
                "駅前の坂本観光案内所（9:00〜17:00）で地図がもらえます。「比叡山フリーパス」もここで買えます。\n\n"
                "お昼を坂本で食べるなら、駅のすぐ近くにそばの老舗「手打蕎麦 鶴屋喜八」があります（11:00〜16:00。建物は国の登録有形文化財）。帰りを坂本にする日に。\n\nおすすめ訪問時間：9:10〜9:30",
                "Sakamoto: the stone-wall town\n\n"
                "From Sakamoto-hieizanguchi station (Keihan), head towards the mountain. The wide avenue running straight up to Hiyoshi Taisha is the Hiyoshi-baba; the shrine entrance is about 10 minutes’ walk. From JR Hieizan-Sakamoto it is the same road, about 20 minutes uphill (or a bus: 7 min, ¥250, every 30 minutes from 9:10).\n\n"
                "Look at the walls on both sides. Natural stones of every size and shape are fitted together uncut. This is the work of the Ano-shu, a guild of masons based in Sakamoto, whose method was used for castle walls in the age of the warring states. Their saying was “listen to the voice of the stone”.\n\n"
                "Behind the walls are satobo: houses where Enryaku-ji’s priests retired after their training on the mountain. Many survive. Most are not open, so look from outside the gates.\n\n"
                "The finest walls are around Shiga-in Monzeki, a little south of the avenue, where the head abbots of the Tendai school lived. It is open to visitors (9:00–16:00, ¥500).\n\n"
                "The Sakamoto tourist information office in front of the station (9:00–17:00) has maps and also sells the Hieizan Free Pass.\n\n"
                "For lunch in Sakamoto there is a long-established soba restaurant, Tsuruya Kihachi, beside the station (11:00–16:00; the building is a Registered Tangible Cultural Property). Good for a day when you come back down this side.\n\nRecommended visit time: 9:10–9:30"),
         gmaps=[gm("日吉馬場（坂本の参道）", "Hiyoshi-baba avenue", 35.07090, 135.86900, "坂本比叡山口駅"),
                gm("滋賀院門跡", "Shiga-in Monzeki", 35.06947, 135.86721, "滋賀院門跡 大津市坂本")],
         links=[link("info", "穴太衆積みの石垣（比叡山・びわ湖DMO）", "Ano-shu stone walls (Hieizan-Biwako DMO, Japanese)", "https://www.hieizan.gr.jp/sakamoto/anoshu"),
                link("info", "坂本観光協会", "Sakamoto tourist association (Japanese)", "https://www.hieizansakamoto.jp/"),
                link("info", "手打蕎麦 鶴屋喜八（比叡山・びわ湖DMO）", "Tsuruya Kihachi soba (Hieizan-Biwako DMO, Japanese)", "https://www.hieizan.gr.jp/sakamoto/honke-tsuruki")],
         info=info([row("hours", "坂本比叡山口駅から日吉大社まで歩いて約10分、JR比叡山坂本駅からは約20分（日吉大社の案内）", "About 10 min on foot from Sakamoto-hieizanguchi station to Hiyoshi Taisha, about 20 from JR Hieizan-Sakamoto (shrine’s access page)"),
                    row("train", "江若バス：比叡山坂本駅 → 坂本比叡山口駅 → 日吉大社前 → ケーブル坂本駅 7分・250円。9:10、9:38、10:08発…（30分おき）", "Kojak bus: Hieizan-Sakamoto station → Sakamoto-hieizanguchi → Hiyoshi Taisha-mae → Cable Sakamoto, 7 min, ¥250. 9:10, 9:38, 10:08… (every 30 min)"),
                    row("hours", "坂本観光案内所 9:00〜17:00（12月29日〜1月3日は休み）", "Sakamoto tourist information office 9:00–17:00 (closed 29 Dec–3 Jan)"),
                    row("fee", "滋賀院門跡 9:00〜16:00、500円", "Shiga-in Monzeki 9:00–16:00, ¥500"),
                    row("hours", "手打蕎麦 鶴屋喜八 11:00〜16:00（15:30ラストオーダー。休みは店のサイトで要確認）", "Tsuruya Kihachi soba 11:00–16:00 (last orders 15:30; for closing days check the restaurant’s site)")],
                   tip=T("比叡山・びわ湖DMOと坂本観光協会の公式サイト、乗換案内で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the Hieizan-Biwako DMO and Sakamoto tourist association websites and a route planner. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="chikurin", name=T("旧竹林院", "Kyu Chikurin-in"), kind=T("里坊の庭", "Garden"),
         blurb=T("中に入れる数少ない里坊。苔と流れのある広い庭を、座敷から眺められます。",
                 "One of the few priests’ retirement villas you can enter: a broad garden of moss and running water, seen from the tatami rooms."),
         lat=35.07158, lng=135.86589,
         text=T("旧竹林院（きゅうちくりんいん）\n\n"
                "日吉馬場を上りきった、日吉大社の赤い鳥居の手前にあります。坂本に残る里坊のうち、中を見られる数少ない一つです。\n\n"
                "庭は約3,300㎡。山からの水を引いた流れと、苔、築山があり、茶室とあずまやが建っています。座敷に上がって座って眺め、そのあと庭に下りて歩けます。お抹茶もいただけます。\n\n"
                "石垣の外から見るだけでは分からない「里坊の中」が見られる場所なので、坂本の町に興味がある人はぜひ。見るのは20分ほどです。秋はもみじ、初夏は苔がきれいです。\n\n"
                "月曜が休みです（祝日なら翌日）。延暦寺を3エリアとも回る日は、ここか近江神宮のどちらかにしてください。\n\nおすすめ訪問時間：9:30〜9:50",
                "Kyu Chikurin-in\n\n"
                "At the top of the avenue, just before the red torii of Hiyoshi Taisha. Of the priests’ villas left in Sakamoto, this is one of the few you can go inside.\n\n"
                "The garden covers about 3,300 square metres: a stream led down from the hills, moss, artificial hills, a tea house and an arbour. Sit in the tatami rooms to look at it, then walk down into it. Matcha is served.\n\n"
                "From the lanes you only see the stone walls; here you see what is behind them. Allow about 20 minutes. Maples in autumn, moss in early summer.\n\n"
                "Closed on Mondays (the next day if Monday is a holiday). On a day when you want all three areas of Enryaku-ji, choose either this or Omi Jingu, not both.\n\nRecommended visit time: 9:30–9:50"),
         gmaps=[gm("旧竹林院", "Kyu Chikurin-in", 35.07158, 135.86589, "旧竹林院 大津市坂本")],
         links=[link("info", "旧竹林院（比叡山・びわ湖DMO）", "Kyu Chikurin-in (Hieizan-Biwako DMO)", "https://www.hieizan.gr.jp/sakamoto/kyuchikurin-in")],
         info=info([row("hours", "9:00〜17:00（受付は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                    row("fee", "大人330円、小学生160円", "¥330; elementary school children ¥160"),
                    row("closed", "月曜（祝日・休日のときは翌日）、祝日・休日の翌日、年末", "Mondays (the next day if a holiday), the day after a public holiday, and the year-end")],
                   tip=T("比叡山・びわ湖DMOの公式サイトで確認しました。2026年7〜9月は休業していましたが、再開しています（坂本観光協会のお知らせ）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the Hieizan-Biwako DMO website. It was closed from July to September 2026 and has reopened (Sakamoto tourist association notice). Photos are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
    dict(id="hiyoshi", name=T("日吉大社", "Hiyoshi Taisha"), kind=T("神社", "Shrine"),
         blurb=T("全国に約3,800ある日吉・日枝・山王神社の総本宮。森の中に国宝の本殿が2つあり、秋はもみじの名所です。",
                 "Head shrine of some 3,800 Hiyoshi, Hie and Sanno shrines across Japan: two National Treasure halls in the woods, and a well-known maple spot."),
         lat=35.07172, lng=135.86215,
         text=T("日吉大社（ひよしたいしゃ）\n\n"
                "比叡山のふもとに約2,100年前からあると伝わる神社で、延暦寺ができてからは、その守り神とされてきました。京都から見て北東（鬼門）にあたるので、都の魔よけの神社でもあります。\n\n"
                "赤い鳥居をくぐって受付を過ぎ、石の橋（大宮橋）を渡って森の中を上ります。順番は、\n\n"
                "・山王鳥居（さんのうとりい）：鳥居の上に山の形の屋根がのった、ここだけの形（写真3枚目）。\n"
                "・西本宮（にしほんぐう）：楼門をくぐると国宝の本殿。屋根のうしろがすぱっと切れたような「日吉造（ひえづくり）」という形です。楼門の軒下の四すみで、猿の彫刻が屋根を支えています。探してみてください。\n"
                "・東本宮（ひがしほんぐう）：歩いて5分ほど。こちらの本殿も国宝です。\n\n"
                "猿は日吉大社の神さまの使いで、「神猿（まさる）」と呼ばれます。「魔が去る」「勝る」にかけた縁起もので、お守りにもなっています。\n\n"
                "境内は広く、西本宮と東本宮を回って40分〜1時間。約3,000本のもみじがあり、見ごろは例年11月の中ごろから下旬です。私が行った2016年11月13日は、赤鳥居のまわりがもう真っ赤でした（写真2枚目）。\n\n"
                "坂本ケーブルの駅へは、赤鳥居の前から歩いて5分ほどです。\n\nおすすめ訪問時間：9:55〜10:45",
                "Hiyoshi Taisha\n\n"
                "A shrine said to have stood at the foot of Mt. Hiei for about 2,100 years, and regarded as the guardian of Enryaku-ji since the temple was founded. It lies north-east of Kyoto, the unlucky direction, so it also guarded the capital.\n\n"
                "Go under the red torii, past the ticket booth, over the stone Omiya bridge and up through the woods. In order:\n\n"
                "• Sanno torii: a torii with a gable on top, a shape found only here (photo 3).\n"
                "• Nishi Hongu (west shrine): through the two-storey gate is the main hall, a National Treasure, in the Hie style, with a roof that looks cut off square at the back. Under the four corners of the gate’s eaves, carved monkeys hold up the roof. See if you can find them.\n"
                "• Higashi Hongu (east shrine): about 5 minutes’ walk. Its main hall is a National Treasure too.\n\n"
                "The monkey is the messenger of the shrine’s gods and is called masaru, a lucky pun on “evil leaves” and “to excel”. You will see it on the charms.\n\n"
                "The grounds are large: allow 40 minutes to an hour for both shrines. There are about 3,000 maples, usually at their best from mid to late November. When I went on 13 November 2016 the ones round the red torii were already deep red (photo 2).\n\n"
                "The Sakamoto Cable station is about 5 minutes’ walk from the red torii.\n\nRecommended visit time: 9:55–10:45"),
         gmaps=[gm("日吉大社", "Hiyoshi Taisha", 35.07172, 135.86215, "日吉大社 大津市坂本")],
         links=[link("official", "日吉大社 公式サイト", "Hiyoshi Taisha (official, Japanese)", "https://hiyoshitaisha.jp/"),
                link("info", "もみじ祭・ライトアップのお知らせ", "Maple festival and light-up notice (Japanese)", "https://hiyoshitaisha.jp/news/2026/1022-1.html")],
         info=info([row("hours", "参拝 9:00〜16:00（門は10〜3月 7:00、4〜9月 6:00に開きます）", "Visiting hours 9:00–16:00 (gates open at 7:00 Oct–Mar, 6:00 Apr–Sep)"),
                    row("fee", "大人500円、中学生・高校生300円、小学生以下は無料", "¥500; junior high and high school ¥300; elementary and under free"),
                    row("hours", "もみじ祭 2026年11月1日〜12月6日。ライトアップは11月14日〜12月6日の17:00〜20:00（赤鳥居〜西本宮楼門。夜は無料）", "Maple festival 1 Nov–6 Dec 2026. Light-up 14 Nov–6 Dec, 17:00–20:00 (red torii to the west shrine gate; free at night)", until="2026-12-06")],
                   tip=T("日吉大社の公式サイトで確認しました。写真2枚目は私の写真（2016年11月）、ほかは Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the shrine’s website. Photo 2 is mine (November 2016); the others are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
    dict(id="cable", name=T("坂本ケーブル", "Sakamoto Cable"), kind=T("ケーブルカー", "Cable car"),
         blurb=T("長さ2,025m、日本でいちばん長いケーブルカー。11分で延暦寺の東塔のそばまで上がります。冬も動きます。",
                 "At 2,025 m, the longest cable car line in Japan: 11 minutes up to the edge of Enryaku-ji’s Todo area. It runs in winter too."),
         lat=35.06967, lng=135.86385,
         text=T("坂本ケーブル\n\n"
                "ケーブル坂本駅から、山の上のケーブル延暦寺駅まで2,025m。日本でいちばん長いケーブルカーです。1927年（昭和2年）の開業で、駅舎は国の登録有形文化財です。\n\n"
                "毎時0分と30分に出て、11分で着きます。上りと下りは同じ時刻に出ます。\n\n"
                "座る場所：上りは、進む向きと反対の「うしろ（下）の端」へ。上るにつれて、うしろの窓に琵琶湖が広がります。下りは逆に、先頭です。\n\n"
                "山上のケーブル延暦寺駅の前は展望台になっていて、琵琶湖が見下ろせます。ここから東塔の巡拝受付まで、杉の中の道を歩いて約10分です。\n\n"
                "片道960円、往復1,830円。帰りを京都側（八瀬）にする日は片道を買ってください。秋の週末は列ができるので、発車の15分前には駅に着いておくと安心です。\n\n"
                "帰りも坂本へ下りる日は、最終に気をつけて。山上発の最終は17:30（12〜2月は17:00）です。延暦寺は16:00に閉まるので、16:00か16:30に乗るのがちょうどいいです。\n\nおすすめ訪問時間：11:00発に乗る（11:11着）",
                "Sakamoto Cable\n\n"
                "From Cable Sakamoto station to Cable Enryakuji station on the mountain is 2,025 m: the longest cable car line in Japan. It opened in 1927, and its station building is a Registered Tangible Cultural Property.\n\n"
                "Cars leave on the hour and half hour and take 11 minutes; the up and down cars leave together.\n\n"
                "Where to sit: going up, take the rear (downhill) end, facing backwards. Lake Biwa opens out behind you as you climb. Coming down, take the front.\n\n"
                "Outside the top station is a viewing terrace over Lake Biwa. From there it is about 10 minutes’ walk through cedars to the Todo ticket gate.\n\n"
                "¥960 one way, ¥1,830 return. Buy a single if you are going down the Kyoto (Yase) side. On autumn weekends there is a queue: be at the station 15 minutes before departure.\n\n"
                "If you come back down to Sakamoto, mind the last car: 17:30 from the top (17:00 from December to February). Enryaku-ji closes at 16:00, so the 16:00 or 16:30 suits.\n\nRecommended visit time: take the 11:00 car (arrives 11:11)"),
         gmaps=[gm("ケーブル坂本駅", "Cable Sakamoto Station", 35.06967, 135.86385, "ケーブル坂本駅"), gm("ケーブル延暦寺駅", "Cable Enryakuji Station", 35.06649, 135.84388, "ケーブル延暦寺駅")],
         links=[SAKACABLE,
                link("info", "延暦寺・坂本周遊一日乗車券（比叡山・びわ湖DMO）", "Enryaku-ji & Sakamoto 1-day ticket (DMO, Japanese)", "https://www.hieizan.gr.jp/ticket/")],
         info=info([row("hours", "3〜11月：8:00〜17:30、毎時0分・30分発／12〜2月：8:30〜17:00。11分", "Mar–Nov: 8:00–17:30, on the hour and half hour / Dec–Feb: 8:30–17:00. 11 minutes"),
                    row("fee", "大人 片道960円・往復1,830円、小学生 片道480円・往復920円", "¥960 one way, ¥1,830 return; children ¥480 / ¥920"),
                    row("fee", "延暦寺・坂本周遊一日乗車券 2,500円：坂本ケーブル往復＋坂本のバス＋延暦寺の巡拝料つき。スマホで前の日までに買う（クレジットカード）。坂本から上って坂本へ下りる日に得です", "Enryaku-ji & Sakamoto 1-day ticket ¥2,500: cable return, the Sakamoto bus and Enryaku-ji admission. Buy online by the day before (credit card). A saving on a day when you go up and down the Sakamoto side", until="2026-12-06"),
                    row("train", "ケーブル坂本駅 ← JR比叡山坂本駅：バス7分・250円、歩くと約20分。京阪 坂本比叡山口駅からは歩いて約10分", "Cable Sakamoto ← JR Hieizan-Sakamoto: bus 7 min, ¥250, or about 20 min on foot. About 10 min on foot from Keihan Sakamoto-hieizanguchi")],
                   tip=T("坂本ケーブル（比叡山鉄道）の公式サイトで確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the Sakamoto Cable (Hieizan Railway) website. Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="toto", name=T("延暦寺 東塔（根本中堂）", "Enryaku-ji: Todo"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
         blurb=T("最澄が延暦寺を開いた場所。根本中堂、大講堂、阿弥陀堂が集まる中心のエリアです。根本中堂は工事中で中に入れません。",
                 "Where Saicho founded the temple: the central area, with the Konpon Chudo, the Great Lecture Hall and the Amida Hall. The Konpon Chudo is under repair and closed inside."),
         lat=35.07044, lng=135.84094,
         text=T("延暦寺 東塔（とうどう）\n\n"
                "延暦寺（えんりゃくじ）は、山の上に散らばる約100のお堂をまとめた呼び名で、「延暦寺」という一つの建物はありません。東塔・西塔・横川（よかわ）の3つのエリアがあり、巡拝券（1,000円）は3つ共通です。最初に入るエリアの受付で買ってください。\n\n"
                "東塔は、788年に最澄（さいちょう）がお堂を建てた、はじまりの場所です。法然・親鸞・栄西・道元・日蓮も、若いころこの山で学びました。\n\n"
                "・根本中堂（こんぽんちゅうどう）：延暦寺の本堂で国宝。今は大改修の覆いの中で、2026年1月から約2年間は中に入れません（上のお知らせを見てください）。写真2枚目は工事の前の姿です。\n"
                "・萬拝堂（まんぱいどう）：根本中堂の前の坂を上がった所。工事のあいだ、御前立の薬師如来と、1200年消えずに灯っている「不滅の法灯」がここに移されています。今はここが東塔の中心です。\n"
                "・大講堂（だいこうどう）：比叡山で学んだ各宗派の祖師の像が並びます。前の赤い鐘楼は、私の写真の1枚目（2016年11月13日。もみじが真っ赤でした）。\n"
                "・文殊楼（もんじゅろう）：根本中堂の向かいの急な石段の上にある門。\n"
                "・阿弥陀堂と東塔：西へ5分ほど上った高台。朱色のお堂と塔が並びます。\n"
                "・国宝殿：仏像の展示。根本中堂の十二神将が12体そろって見られます（別に500円）。\n\n"
                "見るのに1時間半〜2時間。お昼は東塔で食べるのが確実です。一隅会館（いちぐうかいかん）の地下にそば屋があり、延暦寺会館にも食事があります。\n\n"
                "全部のお堂が16:00に閉まります（受付は15:45まで）。西塔と横川にも行く日は、ここを13:00ごろに出ます。\n\nおすすめ訪問時間：11:25〜13:00（お昼を含む）",
                "Enryaku-ji: Todo (East Pagoda area)\n\n"
                "Enryaku-ji is the name for about a hundred halls scattered over the mountain; there is no single building called Enryaku-ji. It has three areas, Todo, Saito and Yokawa, and one ticket (¥1,000) covers all three. Buy it at the first gate you come to.\n\n"
                "Todo is where it began: Saicho built his first hall here in 788. Honen, Shinran, Eisai, Dogen and Nichiren all studied on this mountain when they were young.\n\n"
                "• Konpon Chudo: the main hall of Enryaku-ji and a National Treasure. It is inside a repair shed, and for about two years from January 2026 you cannot go in (see the note above). Photo 2 shows it before the work.\n"
                "• Manpai-do: up the slope in front of the Konpon Chudo. During the work the stand-in Yakushi image and the “Inextinguishable Dharma Light”, burning for 1,200 years, are kept here. For now this is the heart of Todo.\n"
                "• Daikodo (Great Lecture Hall): statues of the founders of the schools that grew out of Mt. Hiei. The red bell tower in front of it is my photo 1 (13 November 2016, with the maples deep red).\n"
                "• Monju-ro: the gate at the top of the steep steps facing the Konpon Chudo.\n"
                "• Amida Hall and the East Pagoda: on higher ground 5 minutes to the west, a vermilion hall and pagoda side by side.\n"
                "• Kokuhoden: the museum of Buddhist sculpture, where all twelve of the Konpon Chudo’s Divine Generals are on show (¥500 extra).\n\n"
                "Allow an hour and a half to two hours. Lunch is safest here: there is a soba shop in the basement of the Ichigu Kaikan rest house, and meals at the Enryakuji Kaikan.\n\n"
                "Every hall closes at 16:00 (last entry 15:45). If you are going on to Saito and Yokawa, leave here at about 13:00.\n\nRecommended visit time: 11:25–13:00 (including lunch)"),
         gmaps=[gm("延暦寺 東塔（根本中堂）", "Enryaku-ji Todo (Konpon Chudo)", 35.07044, 135.84094, "延暦寺 根本中堂"), gm("延暦寺バスセンター", "Enryakuji Bus Center", 35.07053, 135.83917, "延暦寺バスセンター")],
         links=[ENR, ENRTOP,
                link("official", "国宝根本中堂大改修（延暦寺）", "Konpon Chudo repair (official, Japanese)", "https://www.hieizan.or.jp/renovation/")],
         notices=[CHUDO, WINTER],
         info=info([row("hours", "東塔 9:00〜16:00（一年じゅう同じ。受付は15:45まで）", "Todo 9:00–16:00 all year (last entry 15:45)"),
                    row("fee", "巡拝料（東塔・西塔・横川 共通）大人1,000円、中学生・高校生600円、小学生300円。国宝殿は別に大人500円", "Admission (Todo, Saito and Yokawa together) ¥1,000; junior high and high school ¥600; elementary ¥300. Kokuhoden museum ¥500 extra"),
                    row("hours", "根本中堂の修学ステージ（工事を屋根の高さから見る台）は2026年11月まで。最後の現場見学会は11月28日（土）10:00・11:00・14:00、無料・各回先着90名", "The viewing stage at the Konpon Chudo (the works seen from eaves level) is open until November 2026. The last guided site tour is on Saturday 28 November at 10:00, 11:00 and 14:00: free, first 90 people each", until="2026-11-30"),
                    row("closed", "国宝殿は展示替えで2026年12月8日（火）休館", "The Kokuhoden is closed on Tuesday 8 December 2026 for a change of display", until="2026-12-08"),
                    row("train", "シャトルバス：延暦寺バスセンター → 西塔 3分・250円。毎時8分・38分発（13:08、13:38…）。2026年は12月6日まで", "Shuttle bus: Enryakuji Bus Center → Saito, 3 min, ¥250, at :08 and :38 past the hour (13:08, 13:38…). Runs until 6 December in 2026", until="2026-12-06")],
                   tip=T("延暦寺の公式サイト（巡拝時間・料金、根本中堂大改修、お知らせ）と乗換案内で確認しました。写真1・6〜8枚目は私の写真（2016年11月13日）、ほかは Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on Enryaku-ji’s website (hours and fees, the repair pages and news) and a route planner. Photos 1 and 6–8 are mine (13 November 2016); the others are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
    dict(id="saito", name=T("延暦寺 西塔（にない堂・釈迦堂）", "Enryaku-ji: Saito"), kind=T("寺", "Temple"),
         blurb=T("杉木立の中の静かなエリア。廊下でつながった2つのお堂「にない堂」と、山でいちばん古い建物の釈迦堂があります。",
                 "A quiet area among tall cedars: the twin halls joined by a corridor, and the Shaka Hall, the oldest building on the mountain."),
         lat=35.07430, lng=135.83395,
         text=T("延暦寺 西塔（さいとう）\n\n"
                "東塔から西へ約1km。シャトルバスなら延暦寺バスセンターから3分、歩くと山道を20〜40分です（舗装されていない坂と階段）。東塔より人がずっと少なく、杉の中にお堂が点々とあります。\n\n"
                "バス停から歩く順に、\n\n"
                "・にない堂：同じ形のお堂が2つ、渡り廊下でつながっています。左が常行堂（じょうぎょうどう）、右が法華堂（ほっけどう）。弁慶がこの廊下をてんびん棒にして2つのお堂をかついだ、という言い伝えから「にない堂」と呼ばれます。今も修行に使われていて、中には入れません。廊下の下をくぐって先へ進みます（写真1枚目）。\n"
                "・釈迦堂（しゃかどう）：石段を下りた広場の奥。西塔の本堂で、延暦寺に残る建物の中でいちばん古いものです。もとは三井寺（みいでら）の金堂で、1595年に秀吉がここへ移しました。\n"
                "・浄土院（じょうどいん）：東塔との境にある、最澄の墓所です。12年間山を下りない修行のお坊さんが、今も毎日、最澄が生きているかのように食事を供え、掃除をしています。庭はいつも掃き清められています。東塔から歩く道の途中にあります。\n\n"
                "にない堂と釈迦堂で40分ほど。浄土院まで歩くとプラス20分です。\n\n"
                "時間を節約するなら、東塔→西塔は片道だけ歩く手があります（浄土院の前を通ります）。雨の日やサンダルの日はバスにしてください。\n\nおすすめ訪問時間：13:11〜14:10",
                "Enryaku-ji: Saito (West Pagoda area)\n\n"
                "About 1 km west of Todo: 3 minutes by shuttle bus from the Enryakuji Bus Center, or a 20–40 minute hill path on foot (unpaved, with slopes and steps). There are far fewer people than at Todo, and the halls stand here and there among the cedars.\n\n"
                "In walking order from the bus stop:\n\n"
                "• Ninai-do: two identical halls joined by a raised corridor, the Jogyo-do on the left and the Hokke-do on the right. The name, “shouldering halls”, comes from the legend that the warrior monk Benkei lifted the pair with the corridor as a carrying pole. They are still used for training and are closed inside. You walk on under the corridor (photo 1).\n"
                "• Shaka-do: down the stone steps, at the back of the open ground. The main hall of Saito and the oldest building left at Enryaku-ji. It was the main hall of Mii-dera until Hideyoshi had it moved here in 1595.\n"
                "• Jodo-in: Saicho’s mausoleum, on the boundary with Todo. A monk on a twelve-year retreat, never leaving the mountain, still serves meals and sweeps here every day as if Saicho were alive. The garden is kept swept clean. It is on the path you walk from Todo.\n\n"
                "Allow about 40 minutes for the Ninai-do and Shaka-do, and 20 more if you walk to Jodo-in.\n\n"
                "One way to save time: walk between Todo and Saito in one direction only (the path passes Jodo-in). In rain, or in sandals, take the bus.\n\nRecommended visit time: 13:11–14:10"),
         gmaps=[gm("延暦寺 西塔（釈迦堂）", "Enryaku-ji Saito (Shaka-do)", 35.07430, 135.83395, "延暦寺 釈迦堂 西塔"), gm("浄土院", "Jodo-in", 35.07149, 135.83614, "延暦寺 浄土院")],
         links=[link("official", "西塔の案内（延暦寺）", "Saito area guide (official, Japanese)", "https://www.hieizan.or.jp/grounds/saitou.html"), TT],
         info=info([row("hours", "3〜11月 9:00〜16:00／12〜2月 9:30〜16:00（受付は15:45まで）", "Mar–Nov 9:00–16:00 / Dec–Feb 9:30–16:00 (last entry 15:45)"),
                    row("fee", "東塔の巡拝券で入れます（3エリア共通 1,000円）", "Covered by the ticket from Todo (¥1,000 for all three areas)"),
                    row("train", "シャトルバス：西塔 → 横川 10分・600円。毎時11分・41分発（14:11、14:41…）。西塔 → 延暦寺バスセンター・比叡山頂は毎時10分・40分発（最後は16:20）。2026年は12月6日まで", "Shuttle bus: Saito → Yokawa, 10 min, ¥600, at :11 and :41 (14:11, 14:41…). Saito → Bus Center and Hiei-sancho at :10 and :40 (last 16:20). Runs until 6 December in 2026", until="2026-12-06"),
                    row("hours", "東塔から歩くと20〜40分（延暦寺の案内は20分、比叡山・びわ湖DMOの案内は約40分。未舗装・坂・階段あり）", "On foot from Todo: 20–40 minutes (20 according to the temple, about 40 according to the DMO; unpaved, with slopes and steps)")],
                   tip=T("延暦寺の公式サイトと乗換案内（2026年11月24日）で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on Enryaku-ji’s website and a route planner (24 November 2026). Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="yokawa", name=T("延暦寺 横川（横川中堂）", "Enryaku-ji: Yokawa"), kind=T("寺", "Temple"),
         blurb=T("いちばん奥のエリア。石垣の上に朱色の舞台がせり出す横川中堂と、おみくじ発祥の元三大師堂。秋はもみじがきれいです。",
                 "The farthest area: the vermilion Yokawa Chudo standing out over its stone base, and the hall where omikuji fortune slips began. Good maples in autumn."),
         lat=35.09680, lng=135.84984,
         text=T("延暦寺 横川（よかわ）\n\n"
                "西塔から北へ約4km、シャトルバスで10分。歩くと100分以上かかるので、バスが走る季節（2026年は12月6日まで）だけ行ける場所です。ここまで来る人は少なく、3つのエリアの中でいちばん静かです。\n\n"
                "・横川中堂（よかわちゅうどう）：横川の本堂。斜面に柱を組んだ舞台造りで、朱色のお堂が船のように浮かんで見えます。遣唐使の船をモデルにしたといわれます。今の建物は1971年の再建。下の道から見上げた姿がいちばんきれいです（写真1枚目）。\n"
                "・元三大師堂（がんざんだいしどう）：横川中堂から歩いて5分ほど。10世紀に延暦寺を立て直した良源（りょうげん＝元三大師）をまつります。おみくじは元三大師が考えたものといわれ、ここが「おみくじ発祥の地」です。角の生えた鬼の姿の魔よけのお札「角大師（つのだいし）」もここのものです。\n"
                "・恵心堂（えしんどう）：『往生要集』を書いた源信（げんしん）ゆかりのお堂。中には入れません。\n\n"
                "バス停から横川中堂まで歩いて5分。中堂と元三大師堂で50分〜1時間です。\n\n"
                "帰りのバスは 15:00、15:30、最後が16:10発。お堂は16:00に閉まります。京都側へ下りる人は15:30発に乗ってください。乗り遅れると、歩いて帰る道はありません。\n\n"
                "飲みものは東塔で買っておくと安心です。\n\nおすすめ訪問時間：14:21〜15:30",
                "Enryaku-ji: Yokawa\n\n"
                "About 4 km north of Saito, 10 minutes by shuttle bus. On foot it is over 100 minutes, so you can only come while the bus runs (until 6 December in 2026). Few visitors get this far: it is the quietest of the three areas.\n\n"
                "• Yokawa Chudo: the main hall of Yokawa, built out over the slope on stilts, so the vermilion hall seems to float like a ship. It is said to be modelled on the ships of the envoys to Tang China. The present building dates from 1971. The best view is looking up from the path below (photo 1).\n"
                "• Ganzan Daishi-do: about 5 minutes’ walk from the Chudo, dedicated to Ryogen (Ganzan Daishi), who revived Enryaku-ji in the tenth century. He is credited with inventing omikuji, so this is known as their birthplace. The Tsuno Daishi charm against evil, a horned demon figure, also comes from here.\n"
                "• Eshin-do: a hall linked to Genshin, author of the Ojoyoshu. Closed inside.\n\n"
                "It is 5 minutes’ walk from the bus stop to the Chudo. Allow 50 minutes to an hour for the Chudo and the Ganzan Daishi-do.\n\n"
                "Buses back leave at 15:00, 15:30 and, the last, 16:10; the halls close at 16:00. If you are going down the Kyoto side, take the 15:30. Miss the last bus and there is no practical way back on foot.\n\n"
                "Buy drinks at Todo before you come.\n\nRecommended visit time: 14:21–15:30"),
         gmaps=[gm("延暦寺 横川中堂", "Enryaku-ji Yokawa Chudo", 35.09680, 135.84984, "延暦寺 横川中堂")],
         links=[link("official", "横川の案内（延暦寺）", "Yokawa area guide (official, Japanese)", "https://www.hieizan.or.jp/grounds/yokawa.html"), TT],
         info=info([row("hours", "3〜11月 9:00〜16:00／12〜2月 9:30〜16:00（受付は15:45まで）", "Mar–Nov 9:00–16:00 / Dec–Feb 9:30–16:00 (last entry 15:45)"),
                    row("fee", "東塔の巡拝券で入れます（3エリア共通 1,000円）", "Covered by the ticket from Todo (¥1,000 for all three areas)"),
                    row("train", "シャトルバス：横川 → 西塔 → 延暦寺バスセンター → 比叡山頂（20分・800円）。13:30、14:00、14:30、15:00、15:30、16:10発（最後）。2026年は12月6日まで", "Shuttle bus: Yokawa → Saito → Bus Center → Hiei-sancho (20 min, ¥800) at 13:30, 14:00, 14:30, 15:00, 15:30 and 16:10 (the last). Runs until 6 December in 2026", until="2026-12-06"),
                    row("fee", "比叡山内バス1日乗車券 1,200円（バスの車内、延暦寺バスセンターの売店で）。バスセンター→西塔250円＋西塔→横川600円＋横川→山頂800円＝1,650円なので、横川まで行くなら1日券が得", "Shuttle bus 1-day ticket ¥1,200 (sold on the bus and at the Bus Center shop). Bus Center→Saito ¥250 + Saito→Yokawa ¥600 + Yokawa→summit ¥800 = ¥1,650, so the day ticket pays if you go to Yokawa", until="2026-12-06")],
                   tip=T("延暦寺の公式サイト、比叡山・びわ湖DMOの時刻表（2026年3月20日〜12月6日）と乗換案内（2026年11月24日・28日）で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on Enryaku-ji’s website, the DMO timetable (20 March–6 December 2026) and a route planner (24 and 28 November 2026). Photos are from Wikimedia Commons (author and license shown on each photo)."))),
    dict(id="sancho", name=T("比叡山頂と叡山ロープウェイ・ケーブル", "Summit, Eizan Ropeway & Cable"), kind=T("ロープウェイ・ケーブル", "Ropeway & cable car"),
         blurb=T("山頂からロープウェイ3分とケーブルカー9分で、京都側の八瀬へ下ります。冬は運休です。",
                 "From the summit, 3 minutes by ropeway and 9 by cable car take you down to Yase on the Kyoto side. Closed in winter."),
         lat=35.06443, lng=135.82776,
         text=T("比叡山頂と叡山ロープウェイ・ケーブル\n\n"
                "シャトルバスの終点「比叡山頂」で降ります。ロープウェイの比叡山頂駅までは、バス停から歩いて約10分。ガーデンミュージアム比叡の横を通ります。乗り継ぎはこの10分を入れて考えてください。\n\n"
                "山頂のあたりは見晴らしがよく、晴れた日は遠くの山まで見えます（写真1枚目は2016年11月13日）。\n\n"
                "・ロープウェイ：比叡山頂駅→ロープ比叡駅 3分・400円。\n"
                "・歩いて1分で乗り換え。\n"
                "・ケーブルカー：ケーブル比叡駅→ケーブル八瀬駅 9分・600円。高低差561mは日本一で、かなり急です。下りは先頭に立つと、線路が落ちていくように見えます。\n\n"
                "どちらも現金だけです（ICカードもクレジットカードも使えません）。合わせて1,000円を用意してください。\n\n"
                "平日はケーブルが30分おき（毎時0分・30分）なので、ロープウェイは15分か45分発に乗ると待ちません。土日祝は15分おきです。下りの最終は、ロープウェイ18:00発・ケーブル18:15発。\n\n"
                "ガーデンミュージアム比叡は、モネなど印象派の絵をテーマにした庭園です。2026年は12月6日まで（水曜休み。秋は10:00〜17:00、入園16:30まで）。横川まで回った日は時間がありません。寄るなら横川を外してください。\n\n"
                "2026年の運行は12月6日（日）まで。冬は運休するので、坂本ケーブルで坂本へ下ります。\n\nおすすめ訪問時間：15:50に山頂着、16:15発のロープウェイ",
                "Summit, Eizan Ropeway & Cable\n\n"
                "Get off the shuttle bus at its last stop, Hiei-sancho. The ropeway’s summit station is about 10 minutes’ walk from the bus stop, past the Garden Museum Hiei. Count those 10 minutes into your connection.\n\n"
                "The summit area has open views, far across the hills on a clear day (photo 1: 13 November 2016).\n\n"
                "• Ropeway: Hiei-sancho → Rope Hiei, 3 minutes, ¥400.\n"
                "• One minute’s walk to change.\n"
                "• Cable car: Cable Hiei → Cable Yase, 9 minutes, ¥600. Its 561 m drop is the greatest of any cable car in Japan, and it is steep. Going down, stand at the front and the track seems to fall away.\n\n"
                "Both take cash only (no IC cards, no credit cards). Have ¥1,000 ready.\n\n"
                "On weekdays the cable car runs every 30 minutes (on the hour and half hour), so take the ropeway at :15 or :45 and you won’t wait. At weekends and on holidays it runs every 15 minutes. Last runs down: ropeway 18:00, cable car 18:15.\n\n"
                "The Garden Museum Hiei is a garden themed on Monet and the Impressionists. In 2026 it is open until 6 December (closed Wednesdays; 10:00–17:00 in autumn, last entry 16:30). After Yokawa there is no time for it: if you want it, drop Yokawa.\n\n"
                "Service in 2026 ends on Sunday 6 December. In winter, go back down to Sakamoto by the Sakamoto Cable instead.\n\nRecommended visit time: reach the summit at 15:50; ropeway at 16:15"),
         gmaps=[gm("叡山ロープウェイ 比叡山頂駅", "Eizan Ropeway, Hiei-sancho Station", 35.06443, 135.82776, "叡山ロープウェイ 比叡山頂駅"), gm("比叡山頂バス停", "Hiei-sancho bus stop", 35.06585, 135.83130, "ガーデンミュージアム比叡")],
         links=[EIZANCABLE,
                link("official", "叡山ケーブル・ロープウェイ 運賃", "Eizan Cable & Ropeway fares (Japanese)", "https://www.keifuku.co.jp/cms/eizan_ticket/"),
                link("info", "ガーデンミュージアム比叡（比叡山・びわ湖DMO）", "Garden Museum Hiei (DMO, Japanese)", "https://www.hieizan.gr.jp/hieizan/garden-museum-hiei")],
         notices=[WINTER],
         info=info([row("train", "ロープウェイ（比叡山頂発）：毎時0・15・30・45分、最終18:00。ケーブル（ケーブル比叡発）：平日 毎時0・30分、土日祝 0・15・30・45分、最終18:15。2026年は12月6日まで（平日は12月4日まで）", "Ropeway (from the summit): at :00, :15, :30, :45, last 18:00. Cable car (from Cable Hiei): weekdays :00 and :30; weekends and holidays :00, :15, :30, :45; last 18:15. Until 6 December in 2026 (weekdays until 4 December)", until="2026-12-06"),
                    row("fee", "ロープウェイ 片道400円、ケーブル 片道600円（現金のみ）", "Ropeway ¥400, cable car ¥600, one way (cash only)"),
                    row("hours", "比叡山頂バス停 → ロープウェイ比叡山頂駅：歩いて約10分（京福電鉄の案内）", "Hiei-sancho bus stop → ropeway summit station: about 10 min on foot (operator’s guide)"),
                    row("fee", "ガーデンミュージアム比叡：大人1,200円（11月24日〜12月6日は600円）、水曜休み、12月6日まで", "Garden Museum Hiei: ¥1,200 (¥600 from 24 Nov to 6 Dec); closed Wednesdays; open until 6 December", until="2026-12-06"),
                    row("closed", "冬は運休（2026年は12月7日から。2027年の再開日は要確認。2026年は3月20日に再開）", "Closed in winter (from 7 December 2026; 2027 restart date: please check. In 2026 it restarted on 20 March)")],
                   tip=T("京福電鉄（叡山ケーブル・ロープウェイ）の公式サイト、比叡山・びわ湖DMOの時刻表（2026年3月20日〜12月6日）と乗換案内で確認しました。写真1枚目は私の写真、ほかは Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                         "Checked on the Keifuku (Eizan Cable & Ropeway) website, the DMO timetable (20 March–6 December 2026) and a route planner. Photo 1 is mine; the others are from Wikimedia Commons (author and license shown on each photo)."), cash=True)),
    dict(id="yase", name=T("八瀬（もみじの小径）と叡山電車", "Yase & the Eizan railway"), kind=T("駅・もみじ", "Station & maples"),
         blurb=T("ケーブル八瀬駅のまわりは、もみじの名所。川を渡って5分の八瀬比叡山口駅から、叡山電車で出町柳へ14分です。",
                 "The foot of the cable car is a maple spot. Five minutes across the river is Yase-Hieizanguchi station: 14 minutes to Demachiyanagi by the Eizan railway."),
         lat=35.06692, lng=135.80865,
         text=T("八瀬（やせ）と叡山電車\n\n"
                "ケーブル八瀬駅を出ると、目の前がもみじの林です。駅のすぐ横に「もみじの小径（こみち）」という短い散歩道があります。私の写真は2024年12月3日のもので、12月に入っても真っ赤でした。町なかより色づきが遅い年もあります。\n\n"
                "坂を下り、高野川（たかのがわ）の橋を渡ると、叡山電車の八瀬比叡山口（やせひえいざんぐち）駅です。歩いて5分。橋の上から見る川ともみじもきれいです（写真6枚目）。\n\n"
                "1925年に開業した駅で、古い駅舎が残っています（写真1枚目）。ここから出町柳まで14分・280円。昼間は15分おきに出ています。\n\n"
                "出町柳からは京阪電車で三条・祇園四条へ。京都駅へは、京阪で東福寺まで行ってJR奈良線に乗り換えるのが早いです（17分・450円）。\n\n"
                "叡山電車の沿線（一乗寺・貴船・鞍馬）は、別の「叡山電鉄」のマップで紹介しています。\n\nおすすめ訪問時間：16:40〜17:00（17:00発の電車）",
                "Yase & the Eizan railway\n\n"
                "Step out of Cable Yase station and you are in a maple wood. Beside the station is a short path called Momiji-no-komichi. My photos are from 3 December 2024, when the leaves were still deep red. Some years the colour comes later here than in the city.\n\n"
                "Go down the slope and over the bridge across the Takano river to Yase-Hieizanguchi station on the Eizan railway: 5 minutes on foot. The river and maples from the bridge are worth a stop (photo 6).\n\n"
                "The station opened in 1925 and keeps its old building (photo 1). From here it is 14 minutes and ¥280 to Demachiyanagi, with trains every 15 minutes in the daytime.\n\n"
                "At Demachiyanagi the Keihan line takes you to Sanjo and Gion-Shijo. For Kyoto Station, the quickest way is Keihan to Tofukuji and one stop on the JR Nara line (17 min, ¥450).\n\n"
                "The places along the Eizan railway (Ichijoji, Kibune, Kurama) are on my separate Eizan Railway map.\n\nRecommended visit time: 16:40–17:00 (17:00 train)"),
         gmaps=[gm("ケーブル八瀬駅", "Cable Yase Station", 35.06692, 135.80865, "ケーブル八瀬駅"), gm("八瀬比叡山口駅", "Yase-Hieizanguchi Station", 35.06522, 135.80849, "八瀬比叡山口駅")],
         links=[link("timetable", "叡山電車 時刻表", "Eizan railway timetable (Japanese)", "https://eizandensha.co.jp/guide/#timetable"),
                link("info", "叡山電鉄のマップ（このサイト）", "My Eizan Railway map (this site)", "../eizan-line/")],
         info=info([row("train", "八瀬比叡山口 → 出町柳：叡山電車 14分・280円。10〜16時台は毎時0・15・30・45分発。平日の夕方は 16:45、17:00、17:15、17:28発", "Yase-Hieizanguchi → Demachiyanagi: Eizan railway, 14 min, ¥280. At :00, :15, :30, :45 from 10:00 to 16:59; on weekday evenings 16:45, 17:00, 17:15, 17:28"),
                    row("train", "出町柳 → 京都駅：京阪で東福寺、JR奈良線に乗り換え 17分・450円", "Demachiyanagi → Kyoto Station: Keihan to Tofukuji, then the JR Nara line; 17 min, ¥450"),
                    row("hours", "ケーブル八瀬駅 → 八瀬比叡山口駅：歩いて約5分", "Cable Yase → Yase-Hieizanguchi station: about 5 min on foot")],
                   tip=T("比叡山・びわ湖DMOの時刻表と乗換案内（2026年11月24日）で確認しました。秋は叡山電車が特別ダイヤになる日があります。",
                         "Checked on the DMO timetable and a route planner (24 November 2026). The Eizan railway runs a special timetable on some autumn days."))),
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
PICKS = [NO[k] for k in ("omijingu", "chikurin", "hiyoshi", "saito", "yokawa", "sancho")]
H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule, "text": T(ja, en)}

data = {
    "id": "hieizan",
    "_note": "京都から日帰り 比叡山延暦寺と坂本のルート（hieizan/ のページ専用。形は eizan-line.json と同じ）。"
             "京都駅→（JR湖西線。近江神宮は大津京で京阪に乗り換え）→坂本の町→旧竹林院→日吉大社→坂本ケーブル→東塔→西塔→横川→比叡山頂→叡山ロープウェイ・ケーブル→八瀬→叡山電車で出町柳。"
             "写真は Toshi の写真ライブラリから（東塔の鐘楼・もみじ・杉木立、日吉大社の赤鳥居、山頂の眺め＝2016年11月13日／近江神宮＝2025年1月18日／八瀬＝2024年12月3日。横の写真だけ・長辺1600px・位置情報なし。"
             "東塔の1枚目は下の人が写った部分を切ってある）。そのほかは Wikimedia Commons の写真（photos の要素が {file, credit}。ライセンスは Commons の API で2026年11月21日に確認）。"
             "info.checked は事実情報を確認した日（延暦寺・坂本ケーブル・京福電鉄・叡山電車・日吉大社・近江神宮・比叡山びわ湖DMO の公式サイト、乗換案内）。"
             "冬（2026年は12月7日〜）は叡山ケーブル・ロープウェイと山内シャトルバスが運休。until のついた行はその日を過ぎると消える。2027年の再開日・パスの値段が出たら直す。"
             "このファイルは scripts/build_hieizan_data.py で作る。",
    "sections": [{"first": 1, "last": 5, "day": 0}, {"first": 6, "last": 9, "day": 1}, {"first": 10, "last": 11, "day": 2}],
    "focus": {"first": NO["sakamoto"], "last": NO["yase"]},
    "plan": {"_note": "「選んで回る」の設定。京都駅・坂本の町・坂本ケーブル・東塔は必ず入る。八瀬は山頂（京都側へ下りる）を選ぶと入る。",
             "picks": PICKS,
             "auto": {str(NO["kyoto"]): {"always": True}, str(NO["sakamoto"]): {"always": True}, str(NO["cable"]): {"always": True},
                      str(NO["toto"]): {"always": True}, str(NO["yase"]): {"any": [NO["sancho"]]}},
             "hints": [
                 H("cable", {"any": PICKS, "none": [NO["sancho"]]},
                   "京都側へ下りない日（冬はこちらだけ）は、坂本ケーブルを往復で買います（1,830円）。山上発の最終は17:30、12〜2月は17:00。ケーブル坂本駅からJR比叡山坂本駅へは歩いて約20分、バスなら7分です。",
                   "Not going down the Kyoto side (the only choice in winter)? Buy a return on the Sakamoto Cable (¥1,830). The last car down is at 17:30, or 17:00 from December to February. From Cable Sakamoto it is about 20 minutes on foot, or 7 by bus, to JR Hieizan-Sakamoto."),
                 H("toto", {"any": PICKS, "none": [NO["saito"], NO["yokawa"]]},
                   "東塔だけなら、山の上は2時間で足ります。半日で回れます。",
                   "With Todo only, two hours on the mountain is enough: a half-day trip."),
                 H("sancho", {"any": [NO["sancho"]], "none": [NO["saito"], NO["yokawa"]]},
                   "東塔から比叡山頂へは、延暦寺バスセンターからシャトルバスで7分・250円（12月6日まで）。最後は16:48発です。",
                   "From Todo to the summit, take the shuttle bus from the Enryakuji Bus Center: 7 min, ¥250 (until 6 December). The last one leaves at 16:48."),
                 H("yokawa", {"any": [NO["yokawa"]], "none": [NO["saito"]]},
                   "横川へのバスは西塔を通ります。延暦寺バスセンター発は毎時8分・38分、横川まで13分。西塔を外すなら、そのまま乗っていてください。",
                   "The bus to Yokawa passes Saito. It leaves the Enryakuji Bus Center at :08 and :38 and takes 13 minutes to Yokawa. If you are skipping Saito, just stay on."),
                 H("yokawa", {"any": [NO["yokawa"]], "andAny": [NO["omijingu"]]},
                   "近江神宮と横川の両方に行く日は、時間がいっぱいです。近江神宮を8:50に出て、旧竹林院は外し、坂本ケーブルは11:00発までに乗ってください。",
                   "Omi Jingu and Yokawa on the same day leave no slack. Leave Omi Jingu at 8:50, skip Kyu Chikurin-in and be on the Sakamoto Cable by 11:00."),
                 H("yokawa", {"any": [NO["yokawa"]], "andAny": [NO["sancho"]]},
                   "横川まで行って京都側へ下りる日は、乗りものが多いので「比叡山フリーパス」（3,500円。坂本観光案内所か出町柳駅で、12月6日まで）がほぼ同じ値段で、切符を買う手間がなくなります。巡拝料は別です。",
                   "Going as far as Yokawa and down the Kyoto side means a lot of rides: the Hieizan Free Pass (¥3,500, from the Sakamoto tourist office or Demachiyanagi station, until 6 December) costs about the same as single fares and saves buying tickets. Temple admission is extra."),
             ]},
    "photoBase": "../images/hieizan/",
    "spots": spots,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, [(s["no"], s["id"], len(s["photos"])) for s in spots])
