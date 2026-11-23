#!/usr/bin/env python3
"""京都から日帰り 比叡山延暦寺と坂本 のデータを2コース分書き出す。
  data/routes/hieizan.json        … 山を越える（坂本から上って八瀬へ下りる。コースの id は late。3月20日〜12月6日）
  data/routes/hieizan-early.json  … 冬：坂本から往復（コースの id は early。12月7日〜春。山内のバスが走らない時期）
（early / late は sync_higashiyama.py のコース切り替えの名前を借りているだけで、どちらも三条京阪9:01発）

使い方: python3 scripts/build_hieizan_data.py → python3 scripts/sync_hieizan.py
- 2026-11-22「ゲストが実際に回れる1日」として見直し：三条京阪から地下鉄東西線（京阪京津線へ直通）で坂本比叡山口へ、
  坂本ケーブル→東塔→（山内シャトルバス）峰道でお昼→横川→西塔→比叡山頂→叡山ロープウェイ・ケーブル→八瀬→三条で晩ごはん。
  冬は坂本ケーブルの往復で、お昼は坂本の鶴屋喜八。乗り遅れたときの次の便、最後のバスを入れた。
  早朝のコースは作っていない（延暦寺は9:00に開き、昼に激しく混む場所ではないため。秋の土日の坂本ケーブルの列は文章で案内）
- 文章・料金・時刻はこのファイルに書いてある。直したらこのスクリプトを実行し直す（データを直接直さない）
- 確かめたページは下の SOURCES（data の sources に入る）。時刻は乗換案内（Yahoo!路線情報）と各社の公式時刻表
- 写真は images/hieizan/ にある（足していない・入れ替えていない）。並べる順番は下の PHOTOS（自分の写真はファイル名だけ、
  ネットから借りた写真（Wikimedia Commons）は cc(...) で {"file", "credit": {"author", "license", "page"}} にする）
- オーナーの写真は少ない：東塔の鐘楼ともみじ・杉木立（2016年11月13日）、日吉大社の赤鳥居（同じ日）、山頂からの眺め（同じ日）、
  近江神宮（2025年1月18日）、八瀬のもみじとケーブル八瀬駅・八瀬比叡山口駅（2024年12月3日）。ほかは Wikimedia Commons。
  オーナーの写真がない場所（坂本の町・旧竹林院・坂本ケーブル・西塔・横川）は、文章にも行った日などは書かない
- 季節で変わるもの（2026年11月22日に確認）:
  比叡山内シャトルバスは 2026年3月20日〜12月6日（比叡山・びわ湖DMOの時刻表）。叡山ケーブル・ロープウェイの時刻表は平日12/4・土休日12/6まで。
  12月7日以降の叡山ケーブル・ロープウェイの運行は未発表（前の冬は2026年1月5日〜3月19日が運休）。2027年の再開日も未発表
  根本中堂は2026年1月から約2年間、堂内に入れない
- 2026-11-23「要確認」の調べ直し：叡山ケーブル・ロープウェイは現金のみ（京福電鉄のよくある質問）、時計館宝物館の料金と月曜休館（近江神宮）、
  根本中堂・修学ステージ・滋賀院門跡・坂本観光案内所を確かめ直した。12月7日以降の叡山ケーブル・ロープウェイとシャトルバスの運行、
  2027年の再開日、鶴屋喜八の1月からの定休日はまだ公式に出ていないので要確認のまま（冬のコースへの切り替え 12/7〜3/19 も変えていない）
"""
import json, os, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/hieizan"
CHECKED = "2026-11-22"


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

# ---------- リンク
YAHOO = "https://transit.yahoo.co.jp/"
DMO_TT = "https://www.hieizan.gr.jp/design/pdf/2026_spring_autumn.pdf"
ENR = link("official", "延暦寺 巡拝時間・料金", "Enryaku-ji: hours and fees (Japanese)", "https://www.hieizan.or.jp/tickets/")
ENRTOP = link("official", "比叡山延暦寺 公式サイト", "Enryaku-ji (official)", "https://www.hieizan.or.jp/")
TT = link("timetable", "比叡山の交通時刻表 2026年3月20日〜12月6日（シャトルバス・ケーブル・ロープウェイ・叡山電車。PDF）",
          "Mt. Hiei timetables, 20 Mar–6 Dec 2026 (shuttle bus, cable cars, ropeway, Eizan railway; PDF, Japanese)", DMO_TT)
TICKET = link("info", "比叡山のおトクなチケット一覧", "Mt. Hiei passes and tickets (Japanese)", "https://www.hieizan.gr.jp/ticket/")
FREEPASS = link("info", "比叡山フリーパス（叡山電車）", "Hieizan Free Pass (Eizan railway, Japanese)", "https://eizandensha.co.jp/good-value/")
SAKACABLE = link("official", "坂本ケーブル 時刻表・運賃", "Sakamoto Cable: timetable and fares (Japanese)", "https://sakamoto-cable.jp/guide/")
EIZANCABLE = link("timetable", "叡山ケーブル・ロープウェイ 時刻表", "Eizan Cable & Ropeway timetable (Japanese)", "https://www.keifuku.co.jp/cms/eizan_timetable/")
ROUTE = link("timetable", "乗換案内（Yahoo!路線情報）", "Route planner (Yahoo! Japan, Japanese)", YAHOO)
MINEMICHI = link("official", "比叡山峰道レストラン（営業時間・メニュー）", "Hieizan Minemichi Restaurant (hours and menu, Japanese)", "https://www.hieizan.co.jp/gourmet/minemichi/")
SARYO = link("official", "比叡茶寮 根本中堂前店", "Hiei Saryo tea room by the Konpon Chudo (Japanese)", "https://www.hieizan.co.jp/gourmet/tea_tyubai/")
TSURUYA = link("official", "手打蕎麦 鶴屋喜八 公式サイト（営業時間・定休日）", "Tsuruya Kihachi soba (official: hours and closed days, Japanese)", "https://www.tsurukisoba.com/")
KBUS_YASE = link("timetable", "京都バス「八瀬駅前」の時刻表", "Kyoto Bus: Yase-ekimae stop timetable (Japanese)", "https://www.kyotobus.jp/route/timetable/stop.html?stop_id=6255_1")
EIZANMAP = link("info", "叡山電鉄のマップ（夜の祇園四条・先斗町は24〜26番）", "My Eizan Railway map (evening stops 24–26)", "../eizan-line/#list")

# ---------- 確かめたページ（data の sources）
SOURCES = [
    {"what": "三条京阪 → 坂本比叡山口：地下鉄東西線びわ湖浜大津行（京阪京津線へ直通）9:01発 → びわ湖浜大津9:23着、9:27発（土日9:26発）→ 9:42着、620円。"
             "平日・土曜・日曜・12月の平日と土曜で同じ時刻。乗り遅れたら 平日9:13発（京阪山科→JR山科9:29発→比叡山坂本9:41、歩いて坂本比叡山口9:51）、土曜9:16発→10:01着。"
             "検索した日：2026年11月24日（火）・28日（土）・29日（日）、12月15日（火）・19日（土）", "url": YAHOO, "checked": CHECKED},
    {"what": "近江神宮に寄る：三条京阪 平日7:55発→近江神宮前8:26着、土曜8:03発→8:33着（520円）。近江神宮前→坂本比叡山口 平日9:14発→9:23着・9:24発→9:33着、土曜9:13発→9:22着・9:32発→9:42着（200円）",
     "url": YAHOO, "checked": CHECKED},
    {"what": "JR 京都→比叡山坂本 15分・320円（2026年11月24日 9:02発→9:17着）", "url": YAHOO, "checked": CHECKED},
    {"what": "比叡山内シャトルバス・比叡山ドライブバス・奥比叡ドライブバスの時刻と運賃（2026年3月20日〜12月6日。無印は毎日運行、Ⓐ土休日など、Ⓑ土休日、Ⓒ平日）。"
             "延暦寺バスセンター12:38→西塔12:41→峰道12:45→横川12:51。峰道13:45→横川13:51。横川15:00→西塔15:10、横川15:30→西塔15:40→比叡山頂15:50、横川16:10（最終）→西塔16:20→比叡山頂16:30。"
             "峰道→西塔 13:36→13:40。横川→比叡山頂 15:00→15:20。比叡山頂16:00発の奥比叡ドライブバス：横川16:22→おごと温泉駅16:41→堅田駅西口16:50。"
             "比叡山ドライブバス 比叡山頂15:05→三条京阪16:01、16:05→17:00（毎日）。運賃：延暦寺バスセンター→峰道390円、峰道→横川450円、横川→西塔600円、西塔→比叡山頂400円、山頂・東塔・バスセンター→西塔250円、横川→おごと温泉駅950円、比叡山頂→三条京阪840円。ICカード可",
     "url": DMO_TT, "checked": CHECKED},
    {"what": "叡山ケーブル（ケーブル八瀬⇔ケーブル比叡 9分）：12/4までの平日 毎時0・30分、12/6までの土休日 15分おき、最終18:15は下りのみ。叡山ロープウェイ（3分）：9時台は15・30・45分、10〜17時台は15分おき、最終18:00は下りのみ。運賃 ケーブル600円・ロープウェイ400円（片道）。"
             "叡山電車 八瀬比叡山口発 平日10〜16時台 0・15・30・45分、17時台 0・14・26・43・55分／土休日17時台 0・15・30・45分（紅葉シーズンは変更あり）、280円",
     "url": DMO_TT, "checked": CHECKED},
    {"what": "叡山ケーブル・ロープウェイの時刻表（平日・休日とも最終はケーブル18:15・ロープウェイ18:00で下りのみ）。比叡山頂駅〜比叡山頂バス停は徒歩約10分、八瀬比叡山口駅〜ケーブル八瀬は徒歩約5分、京都バス八瀬駅前〜ケーブル八瀬駅は徒歩約5分。"
             "時刻表は画像で、期間の記載なし（期間は比叡山・びわ湖DMOの時刻表 PDF による）。2026年12月7日以降の運行・冬期運休の掲載なし（11月23日に見直し）",
     "url": "https://www.keifuku.co.jp/cms/eizan_timetable/", "checked": "2026-11-23"},
    {"what": "叡山ケーブル・ロープウェイ よくあるご質問「PASMO、SuicaなどのICカードが使えますか？」→ 現金のみでのお支払い",
     "url": "https://www.keifuku.co.jp/cms/eizan_howto/", "checked": "2026-11-23"},
    {"what": "12月7日以降の叡山ケーブル・ロープウェイ、比叡山内シャトルバスの運行：京福電鉄のニュースリリース・叡山ケーブル・ロープウェイのお知らせ、比叡山・びわ湖DMOの交通案内とお知らせのどれにも、11月23日の時点で掲載なし（DMOの時刻表は2026年3月20日〜12月6日の1つだけ）",
     "url": "https://www.hieizan.gr.jp/timetable/", "checked": "2026-11-23"},
    {"what": "前の冬：叡山ケーブル・ロープウェイは2026年1月5日〜3月19日が冬期運休、3月20日から運行（京福電鉄 2025年12月12日のニュースリリース。"
             "同じ発表で、100周年ヘッドマークのケーブルカーの運行期間は2025年12月20日〜2026年1月4日、3月20日〜12月19日とされている）",
     "url": "https://www.keifuku.co.jp/cms/wp-content/uploads/7e3d683b72027669a0c8e4f49216f2ca.pdf", "checked": "2026-11-23"},
    {"what": "2022年度の冬：比叡山内シャトルバスを2022年12月5日〜2023年1月3日に毎日運行（比叡山頂〜東塔〜延暦寺バスセンターだけ。西塔・峰道・横川へは行かない）、1月4日〜3月17日は運休",
     "url": "https://www.hieizan.gr.jp/news/20221206-1887.html", "checked": "2026-11-23"},
    {"what": "叡山ケーブル600円・ロープウェイ400円（片道）。支払い方法の記載なし（現金のみは よくあるご質問）", "url": "https://www.keifuku.co.jp/cms/eizan_ticket/", "checked": "2026-11-23"},
    {"what": "坂本ケーブル：3〜11月 8:00〜17:30、12〜2月 8:30〜17:00、毎時0分・30分発（上り下り同時）、約11分。片道960円・往復1,830円",
     "url": "https://sakamoto-cable.jp/guide/", "checked": CHECKED},
    {"what": "坂本ケーブル：交通系ICカード・クレジットカード・QR決済のマークあり（トップページ）", "url": "https://sakamoto-cable.jp/", "checked": CHECKED},
    {"what": "延暦寺：東塔 9:00〜16:00（1年中）、西塔・横川 3〜11月9:00〜16:00・12〜2月9:30〜16:00、巡拝受付は15:45まで。巡拝料1,000円、国宝殿500円",
     "url": "https://www.hieizan.or.jp/tickets/", "checked": CHECKED},
    {"what": "西塔：東塔からシャトルバス5分、徒歩20分（未舗装、坂道、階段あり）。12〜2月は9:30〜16:00", "url": "https://www.hieizan.or.jp/grounds/saitou.html", "checked": CHECKED},
    {"what": "延暦寺の交通案内：シャトルバス 比叡山頂→東塔約6分→延暦寺バスセンター約1分→西塔約3分→峰道約4分→横川約6分。シャトルバスは冬期運休", "url": "https://www.hieizan.or.jp/access/", "checked": CHECKED},
    {"what": "日吉大社：参拝9:00〜16:00（門は10〜3月7:00、4〜9月6:00）、入苑協賛料500円、もみじ祭11月1日〜12月6日", "url": "https://hiyoshitaisha.jp/", "checked": CHECKED},
    {"what": "旧竹林院：9:00〜17:00（受付16:30まで）、大人330円、月曜（祝日なら翌日）・祝日の翌日・年末休み", "url": "https://www.hieizan.gr.jp/sakamoto/kyuchikurin-in", "checked": CHECKED},
    {"what": "比叡山峰道レストラン：10:00〜17:00（ラストオーダー16:30）、シャトルバス「峰道」下車すぐ。比叡山そば1,000円、平和丼1,400円など", "url": "https://www.hieizan.co.jp/gourmet/minemichi/", "checked": CHECKED},
    {"what": "比叡茶寮 根本中堂前店：9:00〜16:30（売店は17:00まで）。甘味と飲みもの", "url": "https://www.hieizan.co.jp/gourmet/tea_tyubai/", "checked": CHECKED},
    {"what": "手打蕎麦 鶴屋喜八：11:00〜16:00（L.O.15:30）。定休日の一覧（年の表示なし。日付はどれも2026年の月曜）1/26・2/16・3/23・4/20・5/25・6/29・7/27・8/24・25・10/26・12/21。大津市坂本4-11-40（生源寺の前）。"
             "2027年の定休日の掲載はなし（11月23日）。一覧にない9月28日も「本来定休日」とお知らせ（2026年9月26日）。定休日・臨時休業はホームページかInstagramで知らせる（団体予約のページ）",
     "url": "https://www.tsurukisoba.com/", "checked": "2026-11-23"},
    {"what": "鶴屋喜八【9月28日 特別営業のお知らせ】「9月28日は本来定休日ですが…特別営業」", "url": "https://www.tsurukisoba.com/info/1267/", "checked": "2026-11-23"},
    {"what": "近江神宮 時計館宝物館：9:30〜16:30（祝日以外の月曜は休館）、入館料 大人300円（団体210円）・小中学生150円（団体100円）、幼児無料。特別展のときは変わる場合あり",
     "url": "https://oumijingu.org/pages/98/", "checked": "2026-11-23"},
    {"what": "近江神宮：参拝時間 6:00〜18:00、時計館宝物館 9:30〜16:30（入館16:00まで）", "url": "https://oumijingu.org/", "checked": "2026-11-23"},
    {"what": "比叡山フリーパス 3,500円（出町柳駅・坂本観光案内所で、2026年3月20日〜12月6日）：叡山電車 出町柳〜八瀬比叡山口、叡山ケーブル・ロープウェイ、比叡山内シャトルバス、坂本ケーブル、江若バス（ケーブル坂本駅〜比叡山坂本駅）が乗り降り自由",
     "url": "https://eizandensha.co.jp/good-value/", "checked": CHECKED},
    {"what": "比叡山内バス1日乗車券 1,200円（シャトルバス車内・延暦寺バスセンター売店・出町柳駅、2026年3月20日〜12月6日、発売当日限り）", "url": "https://www.hieizan.gr.jp/ticket/", "checked": CHECKED},
    {"what": "ガーデンミュージアム比叡：11/1〜12/6 10:00〜17:00（入園16:30まで）、水曜休み、4/18〜11/23は1,200円・ほかの期間600円", "url": "https://www.hieizan.gr.jp/hieizan/garden-museum-hiei", "checked": CHECKED},
    {"what": "帰り：八瀬比叡山口17:00発→出町柳17:13着、出町柳17:22発→三条17:26着（2026年11月24日、秋ダイヤ）。土曜11月28日は秋ダイヤで17:03発・17:13発。"
             "京都バス17系統 八瀬駅前17:12発→三条京阪前17:40着、17:42発→18:10着（11月24日・28日）、370円。出町柳→三条 京阪240円",
     "url": YAHOO, "checked": CHECKED},
    {"what": "冬の帰り：坂本比叡山口→三条京阪 平日 17:11発（京阪、びわ湖浜大津で乗り換え）→17:55着・620円、比叡山坂本（JR、歩いて10分）17:01発→山科→三条京阪17:29着・17:32発→18:07着・500円。"
             "土曜 16:51発→17:34着、17:12発→17:55着（京阪）、JR17:13発→17:44着（2026年12月15日・19日で検索）", "url": YAHOO, "checked": CHECKED},
    {"what": "根本中堂：2026年1月から約2年間、堂内の拝観を停止。御前立の薬師如来と不滅の法灯は萬拝堂に特別奉安。十二神将は国宝殿で2027年12月まで（予定、国宝殿拝観料が別）。"
             "修学ステージは2026年11月まで、2026年12月から解体工事に着手しステージは閉鎖",
     "url": "https://www.hieizan.or.jp/news/post-2222/", "checked": "2026-11-23"},
    {"what": "修学ステージ「令和8年度12月頃まで見学可能（予定）」「解体工事が始まるため、令和8年12月頃までの予定」（改修のあらまし）", "url": "https://www.hieizan.or.jp/renovation/overview.html", "checked": "2026-11-23"},
    {"what": "根本中堂改修現場見学会：10月10日、11月7日・14日・21日・28日（土）10:00・11:00・14:00、各回90名先着。素屋根解体に伴い本年の開催で最後",
     "url": "https://www.hieizan.or.jp/experience/renovation.html", "checked": "2026-11-23"},
    {"what": "国宝殿 臨時休館：10月8日・9日、11月6日、12月8日（展示替え）", "url": "https://www.hieizan.or.jp/news/post-2209/", "checked": "2026-11-23"},
    {"what": "坂本観光案内所（坂本観光協会、大津市坂本6-1-13）：9時〜17時（12/29〜1/3は休み）", "url": "https://hieizansakamoto.jp/", "checked": "2026-11-23"},
    {"what": "滋賀院門跡：9:00〜16:00、大人500円", "url": "https://www.hieizan.gr.jp/sakamoto/shigainmonzeki", "checked": "2026-11-23"},
    {"what": "日吉大社 もみじまつり11月1日〜12月6日、ライトアップ11月14日〜12月6日 17:00〜20:00（赤鳥居〜西本宮楼門）、夜間の入苑料・駐車場は無料",
     "url": "https://hiyoshitaisha.jp/news/2026/1022-1.html", "checked": "2026-11-23"},
]

# ---------- お知らせ
SEASON = {"from": None, "to": None, "url": DMO_TT,
          "head": T("山を越えられるのは12月6日まで（2026年）。12月7日からは「冬：坂本から往復」のコースで",
                    "The crossing works until 6 December (2026). From 7 December use the “Winter: up and back from Sakamoto” course"),
          "text": T("このコースは、山の上のシャトルバス（東塔・西塔・峰道・横川・比叡山頂を結ぶバス）が走る日だけ回れます。2026年は3月20日〜12月6日です。\n\n"
                    "12月7日からはシャトルバスが運休し、横川と比叡山頂へはバスで行けません。京都側の叡山ケーブル・ロープウェイの時刻表も、平日は12月4日、土日祝は12月6日までのものしか出ていません。それより後の運行は、11月23日の時点で公式サイトに出ていません（要確認。前の冬は2026年1月5日〜3月19日が運休でした）。\n\n"
                    "冬は一覧の上のボタンで「冬：坂本から往復」に切り替えてください。坂本ケーブルは1年中動いています（12〜2月は8:30〜17:00）。2027年の運行開始日はまだ発表されていません（要確認）。",
                    "This course only works on days when the shuttle bus on the mountain runs (linking Todo, Saito, Minemichi, Yokawa and the summit). In 2026 that is 20 March to 6 December.\n\n"
                    "From 7 December the shuttle bus stops, so Yokawa and the summit are out of reach by bus. The published timetable for the Kyoto-side Eizan Cable and Ropeway also runs only to 4 December on weekdays and 6 December at weekends; nothing later had been announced on 23 November (please check; last winter they were closed from 5 January to 19 March 2026).\n\n"
                    "In winter, switch to “Winter: up and back from Sakamoto” with the buttons above the list. The Sakamoto Cable runs all year (8:30–17:00 from December to February). The 2027 start date has not been announced yet (please check).")}
WINTER = {"from": None, "to": None, "url": "https://sakamoto-cable.jp/guide/",
          "head": T("冬は山の上のバスが走りません。坂本ケーブルで上り下りします", "In winter the mountain bus doesn’t run: go up and down by the Sakamoto Cable"),
          "text": T("12月7日から春（2026年は3月20日に再開）までは、山の上のシャトルバスが運休します。横川と比叡山頂へは行けないと考えてください。西塔へは東塔から歩いて行けます（片道20〜40分）。\n\n"
                    "坂本ケーブルは1年中動きます。12〜2月は8:30〜17:00（毎時0分・30分発）、3月は8:00〜17:30。下りの最終に乗り遅れると、歩いて下りる道しかありません。\n\n"
                    "年末年始に、比叡山頂と東塔のあいだだけシャトルバスが臨時で走った年もあります（2022年度は12月5日〜1月3日。西塔・横川へは行きませんでした）。この冬の運行は、11月23日の時点で発表されていません（要確認）。\n\n"
                    "山の上は京都の町よりずっと寒く、雪が積もる日があります。手袋と滑りにくい靴を。雪の日は西塔へ歩かず、東塔だけにしてください。",
                    "From 7 December until spring (in 2026 it restarted on 20 March) the shuttle bus on the mountain does not run, so treat Yokawa and the summit as out of reach. You can walk from Todo to Saito (20–40 minutes each way).\n\n"
                    "The Sakamoto Cable runs all year: 8:30–17:00 from December to February (on the hour and half hour), 8:00–17:30 in March. Miss the last car down and the only way is on foot.\n\n"
                    "In some years a special shuttle bus has run over New Year between the summit and Todo only (5 December to 3 January in the 2022 season; it did not go to Saito or Yokawa). Nothing had been announced for this winter on 23 November (please check).\n\n"
                    "It is much colder up there than in Kyoto, and snow settles on some days. Bring gloves and shoes with grip. On a snowy day, skip the walk to Saito and see Todo only.")}
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

EVENING_JA = ("夜は三条で\n"
              "三条駅の上が三条大橋です。橋を西へ渡ると、木屋町通（きやまちどおり）と先斗町（ぽんとちょう）まで歩いて5分ほど。先斗町は三条通から四条通まで続く石畳の細い路地で、料理屋や居酒屋が並び、表にお品書きを出している店が多いので、歩きながら決められます。"
              "閉まる時間とラストオーダーは店ごとに違うので、入る前に表の案内で確かめてください。山の上はよく歩くので、宿で一度休んでから18時半ごろに出るくらいがちょうどいいです。そのまま21〜22時ごろまで街なかで過ごせます。\n\n"
              "お店を決めておきたい人は、同じサイトの叡山電鉄のマップの24〜26番（祇園四条・ともしび3rd・先斗町）も見てください。")
EVENING_EN = ("Evening in Sanjo\n"
              "Sanjo station is right under Sanjo Ohashi bridge. Cross it to the west and Kiyamachi-dori and Pontocho are about 5 minutes away. Pontocho is a narrow stone-paved alley from Sanjo-dori to Shijo-dori, lined with small restaurants and izakaya; many post their menus outside, so you can choose as you walk. "
              "Closing times and last orders differ, so check the sign at the door. You will have walked a lot on the mountain: rest at your hotel and head out around 18:30. You can stay out in town until 21:00–22:00.\n\n"
              "If you’d rather have a place picked out, see stops 24–26 (Gion-Shijo, Tomoshibi 3rd, Pontocho) on the Eizan Railway map on this site.")


def time_ja(t): return f"\n\nおすすめ訪問時間：{t}"
def time_en(t): return f"\n\nRecommended visit time: {t}"


def build(W):
    """W=True: 冬：坂本から往復（early）。W=False: 山を越える（late）"""
    S = {}

    # ---------- 1 三条から坂本へ
    if W:
        k_ja = ("このコースは冬（12月7日〜春）の回り方です。山の上のシャトルバスが走らないので、坂本で日吉大社とお昼をすませてから坂本ケーブルで東塔へ上がり、西塔まで歩いて、同じケーブルで坂本へ下ります。夕暮れの石垣の町を歩いて、18時ごろ三条に戻ります。\n\n")
        k_en = ("This is the winter course (7 December to spring). With no shuttle bus on the mountain, you see Hiyoshi Taisha and have lunch in Sakamoto, ride the Sakamoto Cable up to Todo, walk on to Saito, and come down the same way. Then the stone-walled town at dusk, and back in Sanjo around 18:00.\n\n")
    else:
        k_ja = ("このコースは、坂本から上って山の上をバスで回り、京都側の八瀬へ下ります。日吉大社も延暦寺も16時に閉まるので、ふもとの神社を朝に、山の上を昼に回ります。ロープウェイとケーブルで下りると、17時半ごろ三条に戻れます。山の上のバスが走る3月20日〜12月6日（2026年）だけのコースです。\n\n")
        k_en = ("This course goes up from Sakamoto, round the mountain by bus, and down to Yase on the Kyoto side. Hiyoshi Taisha and Enryaku-ji both close at 16:00, so the shrine comes in the morning and the mountain in the middle of the day. Down by ropeway and cable car, you are back in Sanjo by about 17:30. It only works while the mountain bus runs: 20 March to 6 December in 2026.\n\n")
    S["kyoto"] = dict(
        name=T("三条から坂本へ", "From Sanjo to Sakamoto"), kind=T("電車（スタート）", "Train (start)"),
        blurb=T("三条京阪9:01発の地下鉄東西線「びわ湖浜大津行き」に乗り、浜大津で1回乗り換えて坂本比叡山口9:42着。平日も土日も同じ時刻です。",
                "Take the 9:01 Tozai line train for Biwako-Hamaotsu from Sanjo-Keihan, change once at Hamaotsu, and reach Sakamoto-hieizanguchi at 9:42. Same times every day."),
        caution=T("「六地蔵行き」は大津へ行きません。行き先を確かめて", "Trains for Rokujizo don’t go to Otsu: check the destination"),
        lat=35.00870, lng=135.77250,
        text=T("三条から坂本へ\n\n"
               "比叡山は京都と滋賀の境にある山です。延暦寺は山の上に3つのエリア（東塔・西塔・横川）が離れてある大きなお寺で、滋賀側の坂本（さかもと）と京都側の八瀬（やせ）の両方からケーブルカーで上がれます。\n\n"
               + k_ja +
               "行き方（平日も土日も同じ時刻）\n"
               "三条京阪（さんじょうけいはん）駅から、地下鉄東西線の「びわ湖浜大津行き」に乗ります。電車はそのまま京阪京津線に入って山を越え、大津へ。終点のびわ湖浜大津で、京阪石山坂本線の「坂本比叡山口行き」に乗り換えます。\n"
               "・三条京阪 9:01発 → びわ湖浜大津 9:23着・9:27発（土日は9:26発）→ 坂本比叡山口 9:42着。620円（ICカードで乗れます）。\n\n"
               "東西線には「六地蔵行き」もあり、こちらは大津へ行きません。ホームの表示で「びわ湖浜大津」を確かめてください。\n\n"
               "乗り遅れたら\n"
               "・平日：9:13発の同じ電車で京阪山科まで行き、となりのJR山科駅（歩いて1分）9:29発の湖西線に乗り換え。比叡山坂本9:41着、坂を上って坂本比叡山口まで歩いて10分。630円。\n"
               "・土曜：9:16発 → 坂本比叡山口 10:01着（びわ湖浜大津で乗り換え）。\n\n"
               "京都駅の近くに泊まっている人は、JR湖西線で比叡山坂本駅まで15分・320円（写真はこの駅）。坂本比叡山口駅まで坂を歩いて10分です。"
               + time_ja("三条京阪 9:01発"),
               "From Sanjo to Sakamoto\n\n"
               "Mt. Hiei stands on the border of Kyoto and Shiga. Enryaku-ji is a big temple in three areas spread over the top (Todo, Saito and Yokawa), and you can ride a cable car up from either Sakamoto on the Shiga side or Yase on the Kyoto side.\n\n"
               + k_en +
               "Getting there (same times on weekdays and weekends)\n"
               "From Sanjo-Keihan station, take the Tozai subway line train for Biwako-Hamaotsu. It runs straight on to the Keihan Keishin line, over the hills to Otsu. At the end, Biwako-Hamaotsu, change to the Keihan Ishiyama-Sakamoto line for Sakamoto-hieizanguchi.\n"
               "• Sanjo-Keihan 9:01 → Biwako-Hamaotsu 9:23, dep. 9:27 (9:26 at weekends) → Sakamoto-hieizanguchi 9:42. ¥620 (IC cards OK).\n\n"
               "Some Tozai line trains go to Rokujizo instead and never reach Otsu. Check the platform sign says Biwako-Hamaotsu.\n\n"
               "If you miss it\n"
               "• Weekdays: take the 9:13 as far as Keihan-Yamashina, walk a minute to JR Yamashina and catch the 9:29 Kosei line train. Hieizan-Sakamoto 9:41, then 10 minutes uphill on foot to Sakamoto-hieizanguchi. ¥630.\n"
               "• Saturdays: the 9:16 → Sakamoto-hieizanguchi 10:01 (change at Biwako-Hamaotsu).\n\n"
               "Staying near Kyoto Station? The JR Kosei line takes 15 minutes (¥320) to Hieizan-Sakamoto (the station in the photo), then it is a 10-minute walk uphill to Sakamoto-hieizanguchi."
               + time_en("leave Sanjo-Keihan at 9:01")),
        gmaps=[gm("三条京阪駅", "Sanjo-Keihan Station", 35.00870, 135.77250, "三条京阪駅"),
               gm("坂本比叡山口駅", "Sakamoto-hieizanguchi Station", None, None, "坂本比叡山口駅")],
        links=[ROUTE, TT, TICKET],
        notices=[WINTER if W else SEASON],
        info=info([row("train", "三条京阪 9:01発（地下鉄東西線 びわ湖浜大津行）→ びわ湖浜大津 9:23着・9:27発（土日9:26発）→ 坂本比叡山口 9:42着。620円。平日も土日も、12月も同じ",
                       "Sanjo-Keihan 9:01 (Tozai line for Biwako-Hamaotsu) → Biwako-Hamaotsu 9:23, dep. 9:27 (weekends 9:26) → Sakamoto-hieizanguchi 9:42. ¥620. Same on weekdays, weekends and in December"),
                   row("train", "乗り遅れたら：平日 9:13発（京阪山科でJRに乗り換え、比叡山坂本9:41着、歩いて10分）／土曜 9:16発 → 坂本比叡山口 10:01着",
                       "If you miss it: weekdays 9:13 (change to JR at Yamashina, Hieizan-Sakamoto 9:41, 10 min walk) / Saturdays 9:16 → Sakamoto-hieizanguchi 10:01"),
                   row("train", "京都駅から：JR湖西線 京都 → 比叡山坂本 15分・320円（9:02発 → 9:17着）", "From Kyoto Station: JR Kosei line to Hieizan-Sakamoto, 15 min, ¥320 (9:02 → 9:17)")],
                  tip=T("時刻と運賃は乗換案内で確認しました（2026年11月24日（火）・28日（土）・29日（日）と12月15日（火）・19日（土）の時刻）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Times and fares were checked on a route planner for 24, 28 and 29 November and 15 and 19 December 2026. The photo is from Wikimedia Commons (author and license shown on the photo).")))

    # ---------- 2 近江神宮（寄り道）
    S["omijingu"] = dict(
        name=T("近江神宮", "Omi Jingu"), kind=T("神社（寄り道）", "Shrine (side trip)"),
        blurb=T("朱色の楼門と、長い石段。百人一首の最初の歌を詠んだ天智天皇をまつる、かるたの神社です。寄るなら三条を8時前に。",
                "A vermilion gate at the top of a long flight of steps: the shrine of Emperor Tenji, author of the first Hyakunin Isshu poem, and home of competitive karuta. Leave Sanjo before 8:00 to fit it in."),
        lat=35.03244, lng=135.85131,
        text=T("近江神宮（おうみじんぐう）\n\n"
               "京阪の近江神宮前駅から歩いて約10分。大きな鳥居をくぐり、森の中の参道を上ると、石段の上に朱色の楼門が見えます（写真1枚目）。\n\n"
               "まつられているのは、1350年ほど前にこの大津に都を置いた天智天皇（てんじてんのう）です。神社ができたのは1940年。百人一首の1番目の歌が天智天皇の歌なので、競技かるたの名人・クイーンを決める試合がここで開かれます。漫画『ちはやふる』の舞台としても知られています。\n\n"
               "天智天皇は日本で初めて水時計（漏刻＝ろうこく）を作らせた人でもあり、境内に漏刻や日時計が置かれ、時計館宝物館があります。\n\n"
               "私が行ったのは2025年1月18日の朝。人が少なく、楼門に朝日が当たってきれいでした。写真5枚目は、花を浮かべた手水（ちょうず）です。\n\n"
               "寄る日の行き方\n"
               "坂本へ行く途中の駅なので、早めに出て途中で降ります。三条京阪 平日7:55発（土曜8:03発）の「びわ湖浜大津行き」→ びわ湖浜大津で乗り換え → 近江神宮前 8:26着（土曜8:33着）。520円。\n"
               "参拝は30分ほど。近江神宮前 平日9:14発（土曜9:13発）で坂本比叡山口9:23着（9:22着）、200円。次の平日9:24発・土曜9:32発でも9:33・9:42に着いて、このあとの予定に間に合います。"
               + time_ja("8:30〜9:10"),
               "Omi Jingu\n\n"
               "About 10 minutes on foot from Omijingu-mae station on the Keihan line. Pass under the big torii, walk up through the woods, and the vermilion gate appears at the top of the stone steps (photo 1).\n\n"
               "The shrine is dedicated to Emperor Tenji, who made Otsu his capital some 1,350 years ago; the shrine itself dates from 1940. The first poem of the Hyakunin Isshu is his, so the national karuta championship finals are held here, and the shrine is known as the setting of the manga Chihayafuru.\n\n"
               "Tenji also had Japan’s first water clock built. There are a water clock and sundials in the grounds, and a clock museum.\n\n"
               "I went on the morning of 18 January 2025: few people, and the gate catching the early sun. Photo 5 is the purification basin with flowers floating in it.\n\n"
               "How to fit it in\n"
               "It is on the way to Sakamoto, so leave earlier and stop off. Sanjo-Keihan 7:55 on weekdays (8:03 on Saturdays), train for Biwako-Hamaotsu → change at Biwako-Hamaotsu → Omijingu-mae 8:26 (Saturdays 8:33). ¥520.\n"
               "Allow half an hour. Then the 9:14 on weekdays (9:13 on Saturdays) from Omijingu-mae to Sakamoto-hieizanguchi, arriving 9:23 (9:22), ¥200. The next ones, 9:24 on weekdays and 9:32 on Saturdays (arr. 9:33 and 9:42), still keep you on schedule."
               + time_en("8:30–9:10")),
        gmaps=[gm("近江神宮", "Omi Jingu", 35.03244, 135.85131, "近江神宮 大津市"), gm("近江神宮前駅", "Omijingu-mae Station", 35.02817, 135.85574, "近江神宮前駅")],
        links=[link("official", "近江神宮 公式サイト", "Omi Jingu (official, Japanese)", "https://oumijingu.org/"), ROUTE],
        info=info([row("hours", "参拝 6:00〜18:00", "Open for worship 6:00–18:00"),
                   row("fee", "参拝は無料。時計館宝物館は 9:30〜16:30（入館16:00まで）、大人300円・小中学生150円。祝日以外の月曜は休館",
                       "Free. Clock museum 9:30–16:30 (last entry 16:00), ¥300; elementary and junior high ¥150. Closed on Mondays unless a public holiday"),
                   row("train", "三条京阪 → 近江神宮前：平日 7:55発 → 8:26着／土曜 8:03発 → 8:33着（びわ湖浜大津で乗り換え、520円）",
                       "Sanjo-Keihan → Omijingu-mae: weekdays 7:55 → 8:26 / Saturdays 8:03 → 8:33 (change at Biwako-Hamaotsu, ¥520)"),
                   row("train", "近江神宮前 → 坂本比叡山口（9分・200円）：平日 9:14、9:24発／土曜 9:13、9:32発",
                       "Omijingu-mae → Sakamoto-hieizanguchi (9 min, ¥200): weekdays 9:14, 9:24 / Saturdays 9:13, 9:32")],
                  tip=T("参拝時間と時計館宝物館は近江神宮の公式サイト（2026年11月23日）、電車は乗換案内（11月24日・28日の時刻）で確認しました。駅から歩く時間は地図で測った目安です。",
                        "Hours and the clock museum from the shrine’s website (23 November 2026); trains from a route planner (24 and 28 November). The walking time from the station is measured on a map.")))

    # ---------- 坂本の町（山を越える日は朝、冬は帰りに）
    sakamoto_common_ja = ("道の両側の石垣を見てください。大きさも形もちがう自然の石を、削らずに組み合わせて積んであります。坂本にいた石工の集団「穴太衆（あのうしゅう）」の仕事で、戦国時代には城の石垣にも使われた積み方です。\n\n"
                          "石垣の中は「里坊（さとぼう）」です。山の上で修行を終えた延暦寺のお坊さんが、年をとってから暮らした住まいで、今も多く残っています。ほとんどは中に入れないので、門の外から見るだけにしてください。中を見られるのは旧竹林院です。\n\n"
                          "石垣がいちばん立派なのは、参道から南へ少し入った滋賀院門跡（しがいんもんぜき）のまわりです。歴代の天台座主（延暦寺の住職）が暮らした所で、中も拝観できます（9:00〜16:00、500円）。")
    sakamoto_common_en = ("Look at the walls on both sides. Natural stones of every size and shape are fitted together uncut. This is the work of the Ano-shu, a guild of masons based in Sakamoto, whose method was used for castle walls in the age of the warring states.\n\n"
                          "Behind the walls are satobo: houses where Enryaku-ji’s priests retired after their training on the mountain. Many survive, but most are not open, so look from outside the gates. Kyu Chikurin-in is the one you can go into.\n\n"
                          "The finest walls are around Shiga-in Monzeki, a little south of the avenue, where the head abbots of the Tendai school lived. It is open to visitors (9:00–16:00, ¥500).")
    if W:
        S["sakamoto"] = dict(
            name=T("坂本の町と、帰りの電車", "Sakamoto at dusk & the train back"), kind=T("門前町・帰り", "Temple town & return"),
            blurb=T("ケーブルを下りたら、穴太衆積みの石垣の参道を駅まで歩いて下ります。17:11の京阪で三条へ、夜は先斗町。",
                    "Off the cable car, walk down the avenue of uncut-stone walls to the station. The 17:11 Keihan train to Sanjo, then an evening in Pontocho."),
            caution=T("坂本ケーブルの下りの最終は17:00（12〜2月）", "Last Sakamoto Cable down: 17:00 (Dec–Feb)"),
            lat=35.07090, lng=135.86900,
            text=T("坂本の町（穴太衆積み＝あのうしゅうづみ の石垣）と、帰りの電車\n\n"
                   "ケーブル坂本駅に16:41に着いたら、日吉大社の赤い鳥居の前を通って、広い参道「日吉馬場（ひよしばんば）」を駅まで下ります。朝に上った道ですが、冬の夕方は人が少なく、石垣が夕日で赤く見える時間です。駅まで15〜20分。\n\n"
                   + sakamoto_common_ja + "\n\n"
                   "帰りの電車（坂本比叡山口から）\n"
                   "・平日：17:11発（京阪。びわ湖浜大津で乗り換え）→ 三条京阪 17:55着、620円。\n"
                   "・土曜：16:51発 → 17:34着、17:12発 → 17:55着（京阪）。\n"
                   "・JRでも帰れます。坂を10分下りた比叡山坂本駅から湖西線で山科へ、地下鉄東西線に乗り換えて三条京阪へ。平日17:01発 → 17:29着、17:32発 → 18:07着（500円）。\n\n"
                   "坂本ケーブルを17:00の最終で下りた日は、比叡山坂本17:32発のJRが目安です（ケーブル坂本駅から歩いて約20分）。\n\n"
                   + EVENING_JA + time_ja("16:45〜17:10"),
                   "Sakamoto: the stone-wall town, and the train back\n\n"
                   "Off the cable car at 16:41, pass the red torii of Hiyoshi Taisha and walk down the broad avenue, the Hiyoshi-baba, to the station. You came up it this morning, but on a winter evening it is quiet and the walls glow in the low sun. 15–20 minutes to the station.\n\n"
                   + sakamoto_common_en + "\n\n"
                   "Trains back (from Sakamoto-hieizanguchi)\n"
                   "• Weekdays: 17:11 (Keihan, change at Biwako-Hamaotsu) → Sanjo-Keihan 17:55, ¥620.\n"
                   "• Saturdays: 16:51 → 17:34, 17:12 → 17:55 (Keihan).\n"
                   "• Or JR: 10 minutes downhill to Hieizan-Sakamoto, Kosei line to Yamashina, then the Tozai line to Sanjo-Keihan. Weekdays 17:01 → 17:29, 17:32 → 18:07 (¥500).\n\n"
                   "If you came down on the last car at 17:00, aim for the 17:32 JR train from Hieizan-Sakamoto (about 20 minutes’ walk from Cable Sakamoto).\n\n"
                   + EVENING_EN + time_en("16:45–17:10")),
            gmaps=[gm("日吉馬場（坂本の参道）", "Hiyoshi-baba avenue", 35.07090, 135.86900, "坂本比叡山口駅"),
                   gm("滋賀院門跡", "Shiga-in Monzeki", 35.06947, 135.86721, "滋賀院門跡 大津市坂本"),
                   gm("先斗町", "Pontocho", 35.00590, 135.77100, "先斗町 京都")],
            links=[ROUTE, link("info", "穴太衆積みの石垣（比叡山・びわ湖DMO）", "Ano-shu stone walls (Hieizan-Biwako DMO, Japanese)", "https://www.hieizan.gr.jp/sakamoto/anoshu"), EIZANMAP],
            info=info([row("train", "坂本比叡山口 → 三条京阪（京阪、浜大津で乗り換え、620円）：平日 17:11発 → 17:55着／土曜 16:51発 → 17:34着、17:12発 → 17:55着",
                           "Sakamoto-hieizanguchi → Sanjo-Keihan (Keihan, change at Hamaotsu, ¥620): weekdays 17:11 → 17:55 / Saturdays 16:51 → 17:34, 17:12 → 17:55"),
                       row("train", "JR：比叡山坂本 → 山科 → 三条京阪（500円）：平日 17:01発 → 17:29着、17:32発 → 18:07着／土曜 17:13発 → 17:44着",
                           "JR: Hieizan-Sakamoto → Yamashina → Sanjo-Keihan (¥500): weekdays 17:01 → 17:29, 17:32 → 18:07 / Saturdays 17:13 → 17:44"),
                       row("fee", "滋賀院門跡 9:00〜16:00、500円", "Shiga-in Monzeki 9:00–16:00, ¥500")],
                      tip=T("電車は乗換案内（2026年12月15日（火）・19日（土）の時刻）で確認しました。滋賀院門跡は比叡山・びわ湖DMOのサイトで確認しました（2026年11月23日）。先斗町の店の営業時間は、1軒ずつは確かめていません。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                            "Trains were checked on a route planner for 15 and 19 December 2026. Shiga-in Monzeki was checked on the DMO website on 23 November 2026. Opening hours of individual places in Pontocho were not checked. Photos are from Wikimedia Commons (author and license shown on each photo).")))
    else:
        S["sakamoto"] = dict(
            name=T("坂本の町（穴太衆積みの石垣）", "Sakamoto: the stone-wall town"), kind=T("門前町", "Temple town"),
            blurb=T("延暦寺のふもとの門前町。自然の石をそのまま積んだ「穴太衆積み」の石垣が、参道の両側に続きます。駅前の案内所でフリーパスも。",
                    "The temple town at the foot of Enryaku-ji, with walls of uncut stone along the avenue. The tourist office by the station sells the Free Pass."),
            lat=35.07090, lng=135.86900,
            text=T("坂本の町（穴太衆積み＝あのうしゅうづみ の石垣）\n\n"
                   "坂本比叡山口駅を出て、山のほうへ。日吉大社へまっすぐ上る広い参道が「日吉馬場（ひよしばんば）」です。日吉大社の入口まで歩いて約10分。\n\n"
                   "駅前の坂本観光案内所（9:00〜17:00）で地図がもらえます。ここで「比叡山フリーパス」（3,500円。2026年は12月6日まで）を買っておくと、このあと乗る坂本ケーブル・山の上のシャトルバス・叡山ロープウェイとケーブル・叡山電車に、切符を買わずに乗れます。このコースどおりに1回ずつ払うと3,440円なので、差は60円。京都側の叡山ロープウェイとケーブルは現金のみで、ICカードが使えないので、パスがあると切符を買う手間がはぶけます。\n\n"
                   + sakamoto_common_ja + "\n\n"
                   "坂本でそばを食べるなら、駅の近く、生源寺（しょうげんじ）の前に手打蕎麦 鶴屋喜八があります（11:00〜16:00）。山を越える日は朝に通るだけなので、冬のコースのお昼にしています。"
                   + time_ja("9:42〜10:00"),
                   "Sakamoto: the stone-wall town\n\n"
                   "From Sakamoto-hieizanguchi station, head towards the mountain. The wide avenue running straight up to Hiyoshi Taisha is the Hiyoshi-baba; the shrine entrance is about 10 minutes’ walk.\n\n"
                   "The Sakamoto tourist information office by the station (9:00–17:00) has maps. Buy the Hieizan Free Pass here (¥3,500, on sale until 6 December in 2026) and you can ride the Sakamoto Cable, the mountain shuttle bus, the Eizan Ropeway and Cable and the Eizan railway without buying tickets. Paying each fare on this course comes to ¥3,440, so the difference is ¥60. The Kyoto-side Eizan Ropeway and Cable take cash only (no IC cards), so the pass saves buying tickets there.\n\n"
                   + sakamoto_common_en + "\n\n"
                   "For soba in Sakamoto, Tsuruya Kihachi is near the station, in front of Shogen-ji (11:00–16:00). On this course you only pass in the morning; it is the lunch stop on the winter course."
                   + time_en("9:42–10:00")),
            gmaps=[gm("日吉馬場（坂本の参道）", "Hiyoshi-baba avenue", 35.07090, 135.86900, "坂本比叡山口駅"),
                   gm("滋賀院門跡", "Shiga-in Monzeki", 35.06947, 135.86721, "滋賀院門跡 大津市坂本")],
            links=[link("info", "穴太衆積みの石垣（比叡山・びわ湖DMO）", "Ano-shu stone walls (Hieizan-Biwako DMO, Japanese)", "https://www.hieizan.gr.jp/sakamoto/anoshu"),
                   link("info", "坂本観光協会", "Sakamoto tourist association (Japanese)", "https://www.hieizansakamoto.jp/"), FREEPASS],
            info=info([row("hours", "坂本比叡山口駅から日吉大社まで歩いて約10分", "About 10 min on foot from Sakamoto-hieizanguchi station to Hiyoshi Taisha"),
                       row("hours", "坂本観光案内所 9:00〜17:00（12月29日〜1月3日は休み）", "Sakamoto tourist information office 9:00–17:00 (closed 29 Dec–3 Jan)"),
                       row("fee", "比叡山フリーパス 3,500円：坂本ケーブル・山内シャトルバス・叡山ロープウェイとケーブル・叡山電車（八瀬比叡山口〜出町柳）・江若バス（ケーブル坂本駅〜比叡山坂本駅）が1日乗り降り自由。坂本観光案内所か出町柳駅で（ネット販売なし）",
                           "Hieizan Free Pass ¥3,500: one day on the Sakamoto Cable, mountain shuttle bus, Eizan Ropeway and Cable, Eizan railway (Yase-Hieizanguchi–Demachiyanagi) and the Kojak bus (Cable Sakamoto–Hieizan-Sakamoto). From the Sakamoto tourist office or Demachiyanagi station (not online)", until="2026-12-06"),
                       row("fee", "滋賀院門跡 9:00〜16:00、500円", "Shiga-in Monzeki 9:00–16:00, ¥500")],
                      tip=T("フリーパスは叡山電車の公式サイト（2026年11月22日）、案内所と滋賀院門跡は坂本観光協会・比叡山びわ湖DMOのサイト（11月23日）、叡山ロープウェイとケーブルの払い方は京福電鉄のよくある質問（11月23日）で確認しました。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                            "The Free Pass was checked on the Eizan railway website (22 November 2026); the tourist office and Shiga-in on the Sakamoto tourist association and DMO websites, and payment on the Eizan Ropeway and Cable on Keifuku’s FAQ (23 November). Photos are from Wikimedia Commons (author and license shown on each photo).")))

    # ---------- 旧竹林院
    S["chikurin"] = dict(
        name=T("旧竹林院", "Kyu Chikurin-in"), kind=T("里坊の庭", "Garden"),
        blurb=T("中に入れる数少ない里坊。苔と流れのある広い庭を、座敷から眺められます。月曜休み。",
                "One of the few priests’ villas you can enter: a broad garden of moss and running water, seen from the tatami rooms. Closed Mondays."),
        caution=T("月曜休み（祝日なら翌日）・祝日の翌日も休み", "Closed Mondays (next day if a holiday) and the day after a holiday"),
        lat=35.07158, lng=135.86589,
        text=T("旧竹林院（きゅうちくりんいん）\n\n"
               "日吉馬場を上りきった、日吉大社の赤い鳥居の手前にあります。坂本に残る里坊のうち、中を見られる数少ない一つです。\n\n"
               "庭は約3,300㎡。山からの水を引いた流れと、苔、築山があり、茶室とあずまやが建っています。座敷に上がって座って眺め、そのあと庭に下りて歩けます。お抹茶もいただけます。\n\n"
               "石垣の外から見るだけでは分からない「里坊の中」が見られる場所です。見るのは20分ほど。秋はもみじ、初夏は苔がきれいです。\n\n"
               + ("冬のコースでは、朝いちばんにここへ。9:00に開くので、坂本比叡山口9:42着でちょうどいい時間です。月曜（祝日なら翌日）と祝日の翌日は休みなので、その日は日吉大社からどうぞ。"
                  if W else
                  "山を越える日は時間に余裕がないので、最初は外してあります。寄るなら坂本ケーブルを11:30発にして、東塔の次のバスを13:08発にずらします（一覧の中に組み直し方が出ます）。月曜（祝日なら翌日）と祝日の翌日は休みです。")
               + time_ja("9:55〜10:20" if W else "9:55〜10:20（寄るとき）"),
               "Kyu Chikurin-in\n\n"
               "At the top of the avenue, just before the red torii of Hiyoshi Taisha. Of the priests’ villas left in Sakamoto, this is one of the few you can go inside.\n\n"
               "The garden covers about 3,300 square metres: a stream led down from the hills, moss, artificial hills, a tea house and an arbour. Sit in the tatami rooms to look at it, then walk down into it. Matcha is served.\n\n"
               "From the lanes you only see the stone walls; here you see what is behind them. Allow about 20 minutes. Maples in autumn, moss in early summer.\n\n"
               + ("On the winter course this is your first stop. It opens at 9:00, which suits the 9:42 arrival. It is closed on Mondays (the next day if Monday is a holiday) and the day after a holiday; on those days start with Hiyoshi Taisha."
                  if W else
                  "The crossing day is tight, so it is left out at first. To add it, take the 11:30 Sakamoto Cable and the 13:08 bus from Todo instead (the list then shows how to adjust). Closed on Mondays (the next day if Monday is a holiday) and the day after a holiday.")
               + time_en("9:55–10:20" if W else "9:55–10:20 (if you add it)")),
        gmaps=[gm("旧竹林院", "Kyu Chikurin-in", 35.07158, 135.86589, "旧竹林院 大津市坂本")],
        links=[link("info", "旧竹林院（比叡山・びわ湖DMO）", "Kyu Chikurin-in (Hieizan-Biwako DMO)", "https://www.hieizan.gr.jp/sakamoto/kyuchikurin-in")],
        info=info([row("hours", "9:00〜17:00（受付は16:30まで）", "9:00–17:00 (last entry 16:30)"),
                   row("fee", "大人330円、小学生160円", "¥330; elementary school children ¥160"),
                   row("closed", "月曜（祝日・休日のときは翌日）、祝日・休日の翌日、年末", "Mondays (the next day if a holiday), the day after a public holiday, and the year-end")],
                  tip=T("比叡山・びわ湖DMOの公式サイトで確認しました（2026年11月22日）。払い方は書かれていないので、現金があると確実です。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Checked on the Hieizan-Biwako DMO website (22 November 2026). Payment methods aren’t stated, so cash is the safe choice. Photos are from Wikimedia Commons (author and license shown on each photo)."), cash=True))

    # ---------- 日吉大社
    hiyoshi_common_ja = ("比叡山のふもとに約2,100年前からあると伝わる神社で、延暦寺ができてからは、その守り神とされてきました。京都から見て北東（鬼門）にあたるので、都の魔よけの神社でもあります。\n\n"
                         "赤い鳥居をくぐって受付を過ぎ、石の橋（大宮橋）を渡って森の中を上ります。順番は、\n\n"
                         "・山王鳥居（さんのうとりい）：鳥居の上に山の形の屋根がのった、ここだけの形（写真3枚目）。\n"
                         "・西本宮（にしほんぐう）：楼門をくぐると国宝の本殿。屋根のうしろがすぱっと切れたような「日吉造（ひえづくり）」という形です。楼門の軒下の四すみで、猿の彫刻が屋根を支えています。探してみてください。\n"
                         "・東本宮（ひがしほんぐう）：歩いて5分ほど。こちらの本殿も国宝です。\n\n"
                         "猿は日吉大社の神さまの使いで、「神猿（まさる）」と呼ばれます。「魔が去る」「勝る」にかけた縁起もので、お守りにもなっています。\n\n"
                         "約3,000本のもみじがあり、見ごろは例年11月の中ごろから下旬です。私が行った2016年11月13日は、赤鳥居のまわりがもう真っ赤でした（写真2枚目）。\n\n")
    hiyoshi_common_en = ("A shrine said to have stood at the foot of Mt. Hiei for about 2,100 years, and regarded as the guardian of Enryaku-ji since the temple was founded. It lies north-east of Kyoto, the unlucky direction, so it also guarded the capital.\n\n"
                         "Go under the red torii, past the ticket booth, over the stone Omiya bridge and up through the woods. In order:\n\n"
                         "• Sanno torii: a torii with a gable on top, a shape found only here (photo 3).\n"
                         "• Nishi Hongu (west shrine): through the two-storey gate is the main hall, a National Treasure, in the Hie style, with a roof that looks cut off square at the back. Under the four corners of the gate’s eaves, carved monkeys hold up the roof. See if you can find them.\n"
                         "• Higashi Hongu (east shrine): about 5 minutes’ walk. Its main hall is a National Treasure too.\n\n"
                         "The monkey is the messenger of the shrine’s gods and is called masaru, a lucky pun on “evil leaves” and “to excel”. You will see it on the charms.\n\n"
                         "There are about 3,000 maples, usually at their best from mid to late November. When I went on 13 November 2016 the ones round the red torii were already deep red (photo 2).\n\n")
    if W:
        h_ja = ("西本宮と東本宮を回って40〜50分。出たら、日吉馬場を駅のほうへ10分ほど下って、お昼にします。\n\n"
                "お昼：手打蕎麦 鶴屋喜八（つるやきはち）\n"
                "生源寺（しょうげんじ）の前の、延暦寺に代々そばを納めてきた店です。11:00〜16:00（ラストオーダー15:30）。休みは公式サイトに日付の一覧があり、12月は21日です。1月からの休みはまだ載っていません（要確認）。一覧にない休みの日もあるので、行く前に公式サイトかInstagramで確かめてください。\n\n"
                "食べたら、坂をもう一度上ってケーブル坂本駅へ（歩いて約20分）。12:30発の坂本ケーブルに乗ります。")
        h_en = ("Allow 40–50 minutes for the west and east shrines. Then walk about 10 minutes back down the avenue towards the station for lunch.\n\n"
                "Lunch: Tsuruya Kihachi soba\n"
                "In front of Shogen-ji, a soba maker that has supplied Enryaku-ji for generations. 11:00–16:00 (last orders 15:30). Its website lists closing dates: in December it is the 21st. Dates from January are not listed yet (please check), and there are closing days missing from the list, so check its website or Instagram before you go.\n\n"
                "After lunch, walk back up to Cable Sakamoto station (about 20 minutes) for the 12:30 Sakamoto Cable.")
        h_time = ("10:25〜11:10（お昼 11:20〜12:00）", "10:25–11:10 (lunch 11:20–12:00)")
    else:
        h_ja = ("西本宮と東本宮を回って40分〜1時間。坂本ケーブルの駅へは、赤鳥居の前から歩いて5分ほどです。11:00発のケーブルに乗るので、10:50には鳥居を出てください。")
        h_en = ("Allow 40 minutes to an hour for both shrines. The Sakamoto Cable station is about 5 minutes’ walk from the red torii. You are catching the 11:00 cable car, so leave the torii by 10:50.")
        h_time = ("10:00〜10:50", "10:00–10:50")
    S["hiyoshi"] = dict(
        name=T("日吉大社", "Hiyoshi Taisha"), kind=T("神社", "Shrine"),
        blurb=T("全国に約3,800ある日吉・日枝・山王神社の総本宮。森の中に国宝の本殿が2つあり、秋はもみじの名所です。16:00まで。",
                "Head shrine of some 3,800 Hiyoshi, Hie and Sanno shrines across Japan: two National Treasure halls in the woods, and a well-known maple spot. Open until 16:00."),
        lat=35.07172, lng=135.86215,
        text=T("日吉大社（ひよしたいしゃ）\n\n" + hiyoshi_common_ja + h_ja + time_ja(h_time[0]),
               "Hiyoshi Taisha\n\n" + hiyoshi_common_en + h_en + time_en(h_time[1])),
        gmaps=[gm("日吉大社", "Hiyoshi Taisha", 35.07172, 135.86215, "日吉大社 大津市坂本")]
              + ([gm("手打蕎麦 鶴屋喜八", "Tsuruya Kihachi soba", None, None, "手打蕎麦 鶴屋喜八 大津市坂本")] if W else []),
        links=[link("official", "日吉大社 公式サイト", "Hiyoshi Taisha (official, Japanese)", "https://hiyoshitaisha.jp/"),
               link("info", "もみじ祭・ライトアップのお知らせ", "Maple festival and light-up notice (Japanese)", "https://hiyoshitaisha.jp/news/2026/1022-1.html")]
              + ([TSURUYA] if W else []),
        info=info([row("hours", "参拝 9:00〜16:00（門は10〜3月 7:00、4〜9月 6:00に開きます）", "Visiting hours 9:00–16:00 (gates open at 7:00 Oct–Mar, 6:00 Apr–Sep)"),
                   row("fee", "大人500円、中学生・高校生300円、小学生以下は無料", "¥500; junior high and high school ¥300; elementary and under free"),
                   row("hours", "もみじ祭 2026年11月1日〜12月6日。ライトアップは11月14日〜12月6日の17:00〜20:00（赤鳥居〜西本宮楼門。夜は無料）", "Maple festival 1 Nov–6 Dec 2026. Light-up 14 Nov–6 Dec, 17:00–20:00 (red torii to the west shrine gate; free at night)", until="2026-12-06")]
                  + ([row("hours", "手打蕎麦 鶴屋喜八：11:00〜16:00（ラストオーダー15:30）。定休日は公式サイトの日付の一覧で、12月は21日。1月からはまだ載っていない（要確認）。一覧にない休みもあるので、公式サイトかInstagramで確かめて",
                          "Tsuruya Kihachi soba: 11:00–16:00 (last orders 15:30). Closing dates are listed on its website: 21 December; dates from January not listed yet (please check). Some closing days are missing from the list, so check its website or Instagram")] if W else []),
                  tip=T("日吉大社の公式サイトで確認しました（時間と料金は2026年11月22日、ライトアップは11月23日）。" + ("鶴屋喜八は店の公式サイト（11月23日）。" if W else "") + "写真2枚目は私の写真（2016年11月）、ほかは Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Checked on the shrine’s website (hours and fees on 22 November 2026, the light-up on 23 November). " + ("Tsuruya Kihachi on its own website (23 November). " if W else "") + "Photo 2 is mine (November 2016); the others are from Wikimedia Commons (author and license shown on each photo)."), cash=True))

    # ---------- 坂本ケーブル
    if W:
        c_ja = ("冬のコースは12:30発で上がり、帰りは16:30発で下ります。往復1,830円。12〜2月の下りの最終は17:00（3月は17:30）。乗り遅れると歩いて下りる道しかないので、西塔から戻るのが遅れたら16:30を見送って17:00に。")
        c_en = ("On the winter course you go up on the 12:30 and come down on the 16:30. Return ticket ¥1,830. The last car down is at 17:00 from December to February (17:30 in March). Miss it and the only way is on foot, so if you are late back from Saito, let the 16:30 go and take the 17:00.")
        c_time = ("12:30発に乗る（12:41着）", "take the 12:30 (arrives 12:41)")
    else:
        c_ja = ("山を越える日は片道（960円）か、坂本で買ったフリーパスで。11:00発に乗ります。乗り遅れたら11:30発（東塔を少し短くして、12:38のバスに乗る）。秋の週末は列ができるので、発車の15分前には駅に着いておくと安心です。\n\n"
                "延暦寺を見たあと坂本へ戻る場合の最終は、山上発17:30（12〜2月は17:00）です。")
        c_en = ("On the crossing, buy a single (¥960) or use the Free Pass from Sakamoto. Take the 11:00; if you miss it, the 11:30 (spend a little less time at Todo and still catch the 12:38 bus). On autumn weekends there is a queue: be at the station 15 minutes before departure.\n\n"
                "If you ever need to come back down to Sakamoto instead, the last car from the top is at 17:30 (17:00 from December to February).")
        c_time = ("11:00発に乗る（11:11着）", "take the 11:00 (arrives 11:11)")
    S["cable"] = dict(
        name=T("坂本ケーブル", "Sakamoto Cable"), kind=T("ケーブルカー", "Cable car"),
        blurb=T("長さ2,025m、日本でいちばん長いケーブルカー。11分で延暦寺の東塔のそばまで上がります。1年中動きます。ICカード・クレジットカード可。",
                "At 2,025 m, the longest cable car line in Japan: 11 minutes up to the edge of Enryaku-ji’s Todo area. Runs all year; IC cards and credit cards accepted."),
        lat=35.06967, lng=135.86385,
        text=T("坂本ケーブル\n\n"
               "ケーブル坂本駅から、山の上のケーブル延暦寺駅まで2,025m。日本でいちばん長いケーブルカーです。1927年（昭和2年）の開業で、駅舎は国の登録有形文化財です。\n\n"
               "毎時0分と30分に出て、約11分で着きます。上りと下りは同じ時刻に出ます。3〜11月は8:00〜17:30、12〜2月は8:30〜17:00。\n\n"
               "座る場所：上りは、進む向きと反対の「うしろ（下）の端」へ。上るにつれて、うしろの窓に琵琶湖が広がります。下りは逆に、先頭です。\n\n"
               "山上のケーブル延暦寺駅の前は展望台になっていて、琵琶湖が見下ろせます。ここから東塔まで、杉の中の道を歩いて10分ほどです。\n\n"
               + c_ja + time_ja(c_time[0]),
               "Sakamoto Cable\n\n"
               "From Cable Sakamoto station to Cable Enryakuji station on the mountain is 2,025 m: the longest cable car line in Japan. It opened in 1927, and its station building is a Registered Tangible Cultural Property.\n\n"
               "Cars leave on the hour and half hour and take about 11 minutes; the up and down cars leave together. 8:00–17:30 from March to November, 8:30–17:00 from December to February.\n\n"
               "Where to sit: going up, take the rear (downhill) end, facing backwards. Lake Biwa opens out behind you as you climb. Coming down, take the front.\n\n"
               "Outside the top station is a viewing terrace over Lake Biwa. From there it is about 10 minutes’ walk through cedars to Todo.\n\n"
               + c_en + time_en(c_time[1])),
        gmaps=[gm("ケーブル坂本駅", "Cable Sakamoto Station", 35.06967, 135.86385, "ケーブル坂本駅"), gm("ケーブル延暦寺駅", "Cable Enryakuji Station", 35.06649, 135.84388, "ケーブル延暦寺駅")],
        links=[SAKACABLE] + ([] if W else [FREEPASS]),
        info=info([row("hours", "3〜11月：8:00〜17:30、12〜2月：8:30〜17:00。毎時0分・30分発（上りと下りが同時に出る）、約11分", "Mar–Nov: 8:00–17:30; Dec–Feb: 8:30–17:00. On the hour and half hour (up and down cars leave together), about 11 min"),
                   row("fee", "大人 片道960円・往復1,830円、小学生 片道480円・往復920円。交通系ICカード・クレジットカード・QR決済が使えます", "¥960 one way, ¥1,830 return; children ¥480 / ¥920. IC cards, credit cards and QR payments accepted"),
                   row("hours", "ケーブル坂本駅 ← 日吉大社の赤鳥居から歩いて約5分。ケーブル延暦寺駅 → 東塔は歩いて約10分（どちらも地図で見た目安）", "Cable Sakamoto ← about 5 min on foot from the red torii of Hiyoshi Taisha. Cable Enryakuji → Todo about 10 min on foot (both estimated from the map)")],
                  tip=T("坂本ケーブル（比叡山鉄道）の公式サイトで確認しました（2026年11月22日）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Checked on the Sakamoto Cable (Hieizan Railway) website on 22 November 2026. Photos are from Wikimedia Commons (author and license shown on each photo).")))

    # ---------- 東塔
    toto_common_ja = ("延暦寺（えんりゃくじ）は、山の上に散らばる約100のお堂をまとめた呼び名で、「延暦寺」という一つの建物はありません。東塔・西塔・横川（よかわ）の3つのエリアがあり、巡拝券（1,000円）は3つ共通です。最初に入る東塔の受付で買って、なくさないように持っていてください。\n\n"
                      "東塔は、788年に最澄（さいちょう）がお堂を建てた、はじまりの場所です。法然・親鸞・栄西・道元・日蓮も、若いころこの山で学びました。\n\n"
                      "・根本中堂（こんぽんちゅうどう）：延暦寺の本堂で国宝。今は大改修の覆いの中で、2026年1月から約2年間は中に入れません（上のお知らせを見てください）。写真2枚目は工事の前の姿です。\n"
                      "・萬拝堂（まんぱいどう）：根本中堂の前の坂を上がった所。工事のあいだ、御前立の薬師如来と、1200年消えずに灯っている「不滅の法灯」がここに移されています。今はここが東塔の中心です。\n"
                      "・大講堂（だいこうどう）：比叡山で学んだ各宗派の祖師の像が並びます。前の赤い鐘楼は、私の写真の1枚目（2016年11月13日。もみじが真っ赤でした）。\n"
                      "・文殊楼（もんじゅろう）：根本中堂の向かいの急な石段の上にある門。\n"
                      "・阿弥陀堂と東塔：西へ5分ほど上った高台。朱色のお堂と塔が並びます。\n"
                      "・国宝殿：仏像の展示。根本中堂の十二神将が12体そろって見られます（別に500円）。\n\n"
                      "ひと休みは、根本中堂前の広場の売店にある比叡茶寮（9:00〜16:30）で。ゆば饅頭やぜんざい、甘酒、コーヒーがあります。食事の店ではありません。\n\n")
    toto_common_en = ("Enryaku-ji is the name for about a hundred halls scattered over the mountain; there is no single building called Enryaku-ji. It has three areas, Todo, Saito and Yokawa, and one ticket (¥1,000) covers all three. Buy it at the Todo gate, your first, and keep it safe.\n\n"
                      "Todo is where it began: Saicho built his first hall here in 788. Honen, Shinran, Eisai, Dogen and Nichiren all studied on this mountain when they were young.\n\n"
                      "• Konpon Chudo: the main hall of Enryaku-ji and a National Treasure. It is inside a repair shed, and for about two years from January 2026 you cannot go in (see the note above). Photo 2 shows it before the work.\n"
                      "• Manpai-do: up the slope in front of the Konpon Chudo. During the work the stand-in Yakushi image and the “Inextinguishable Dharma Light”, burning for 1,200 years, are kept here. For now this is the heart of Todo.\n"
                      "• Daikodo (Great Lecture Hall): statues of the founders of the schools that grew out of Mt. Hiei. The red bell tower in front of it is my photo 1 (13 November 2016, with the maples deep red).\n"
                      "• Monju-ro: the gate at the top of the steep steps facing the Konpon Chudo.\n"
                      "• Amida Hall and the East Pagoda: on higher ground 5 minutes to the west, a vermilion hall and pagoda side by side.\n"
                      "• Kokuhoden: the museum of Buddhist sculpture, where all twelve of the Konpon Chudo’s Divine Generals are on show (¥500 extra).\n\n"
                      "For a break, the Hiei Saryo tea corner in the shop on the square in front of the Konpon Chudo (9:00–16:30) has yuba buns, zenzai, amazake and coffee. It is not a place for a meal.\n\n")
    if W:
        t_ja = ("冬のコースは12:55〜14:15に東塔を回り、そのあと西塔まで歩きます（片道20〜40分）。雪の日や、足元が心配な日は西塔へ行かず、東塔をゆっくり見て15:00か15:30のケーブルで下りてください。")
        t_en = ("On the winter course you see Todo from 12:55 to 14:15, then walk on to Saito (20–40 minutes each way). On a snowy day, or if you are unsure of your footing, skip Saito, take your time at Todo and go down on the 15:00 or 15:30 cable car.")
        t_time = ("12:55〜14:15", "12:55–14:15")
    else:
        t_ja = ("このコースでは東塔に1時間ほど。延暦寺バスセンター（東塔の西の端）12:38発のシャトルバスで峰道へお昼に行きます。乗り遅れたら13:08発（峰道13:15着）。\n\n"
                "シャトルバスに3回以上乗るので、フリーパスを持っていない人は「比叡山内バス1日乗車券」（1,200円。バスの中か、延暦寺バスセンターの売店で）を。このコースどおりに1回ずつ払うと1,840円です。ICカードでも乗れます。")
        t_en = ("On this course you have about an hour at Todo. Then take the 12:38 shuttle bus from the Enryakuji Bus Center (at the west end of Todo) to Minemichi for lunch. If you miss it, the 13:08 (Minemichi 13:15).\n\n"
                "You will ride the shuttle bus at least three times, so without the Free Pass buy the mountain bus day ticket (¥1,200, on the bus or at the Bus Center shop). Paying each ride on this course comes to ¥1,840. IC cards also work.")
        t_time = ("11:25〜12:35", "11:25–12:35")
    S["toto"] = dict(
        name=T("延暦寺 東塔（根本中堂）", "Enryaku-ji: Todo"), kind=T("寺（世界遺産）", "Temple (World Heritage)"),
        blurb=T("最澄が延暦寺を開いた場所。根本中堂、大講堂、阿弥陀堂が集まる中心のエリアです。根本中堂は工事中で中に入れません。巡拝受付は15:45まで。",
                "Where Saicho founded the temple: the central area, with the Konpon Chudo, the Great Lecture Hall and the Amida Hall. The Konpon Chudo is under repair and closed inside. Last entry 15:45."),
        caution=T("根本中堂は工事中で中に入れません（萬拝堂でお参り）", "Konpon Chudo closed inside for repairs (worship at the Manpai-do)"),
        lat=35.07044, lng=135.84094,
        text=T("延暦寺 東塔（とうどう）\n\n" + toto_common_ja + t_ja + time_ja(t_time[0]),
               "Enryaku-ji: Todo (East Pagoda area)\n\n" + toto_common_en + t_en + time_en(t_time[1])),
        gmaps=[gm("延暦寺 東塔（根本中堂）", "Enryaku-ji Todo (Konpon Chudo)", 35.07044, 135.84094, "延暦寺 根本中堂"), gm("延暦寺バスセンター", "Enryakuji Bus Center", 35.07053, 135.83917, "延暦寺バスセンター")],
        links=[ENR, ENRTOP, link("official", "国宝根本中堂大改修（延暦寺）", "Konpon Chudo repair (official, Japanese)", "https://www.hieizan.or.jp/renovation/"), SARYO] + ([] if W else [TT]),
        notices=[CHUDO] + ([WINTER] if W else []),
        info=info([row("hours", "東塔 9:00〜16:00（1年中同じ。巡拝受付は15:45まで）", "Todo 9:00–16:00 all year (last entry 15:45)"),
                   row("fee", "巡拝料（東塔・西塔・横川 共通）大人1,000円、中学生・高校生600円、小学生300円。国宝殿は別に大人500円", "Admission (Todo, Saito and Yokawa together) ¥1,000; junior high and high school ¥600; elementary ¥300. Kokuhoden museum ¥500 extra"),
                   row("hours", "根本中堂の最後の現場見学会は11月28日（土）10:00・11:00・14:00、無料・各回先着90名", "The last guided site tour of the Konpon Chudo works is on Saturday 28 November at 10:00, 11:00 and 14:00: free, first 90 people each", until="2026-11-28"),
                   row("closed", "国宝殿は展示替えで2026年12月8日（火）休館", "The Kokuhoden is closed on Tuesday 8 December 2026 for a change of display", until="2026-12-08"),
                   row("hours", "比叡茶寮 根本中堂前店 9:00〜16:30（甘味と飲みもの。売店は17:00まで）", "Hiei Saryo tea corner by the Konpon Chudo 9:00–16:30 (sweets and drinks; the shop until 17:00)")]
                  + ([] if W else [row("train", "シャトルバス：延暦寺バスセンター → 西塔 → 峰道 → 横川。12:38発 → 峰道12:45着、13:08発 → 峰道13:15着（毎日。2026年3月20日〜12月6日の時刻）。バスセンター→峰道390円、1日乗車券1,200円",
                                       "Shuttle bus: Enryakuji Bus Center → Saito → Minemichi → Yokawa. 12:38 → Minemichi 12:45, 13:08 → Minemichi 13:15 (daily; timetable for 20 Mar–6 Dec 2026). Bus Center → Minemichi ¥390; day ticket ¥1,200")]),
                  tip=T("延暦寺の公式サイト（巡拝時間・料金は2026年11月22日、根本中堂の改修と見学会は11月23日）、比叡茶寮は比叡山ドライブウェイの公式サイト、バスは比叡山・びわ湖DMOの時刻表（PDF）で確認しました。写真1・6〜8枚目は私の写真（2016年11月13日）、ほかは Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Checked on Enryaku-ji’s website (hours and fees on 22 November 2026; the repair and tours on 23 November), the Hieizan Driveway company’s site for the tea corner, and the DMO timetable (PDF) for the bus. Photos 1 and 6–8 are mine (13 November 2016); the others are from Wikimedia Commons (author and license shown on each photo)."), cash=True))

    # ---------- 横川（山を越える日だけ）
    if not W:
        S["yokawa"] = dict(
            name=T("延暦寺 横川（横川中堂）", "Enryaku-ji: Yokawa"), kind=T("寺", "Temple"),
            blurb=T("途中の峰道でお昼にしてから、いちばん奥のエリアへ。朱色の舞台がせり出す横川中堂と、おみくじ発祥の元三大師堂。",
                    "Lunch at Minemichi on the way, then the farthest area: the vermilion Yokawa Chudo standing out over its stone base, and the hall where omikuji began."),
            caution=T("帰りのバスは15:00発。最後は16:10発", "Bus back at 15:00; the last at 16:10"),
            lat=35.09680, lng=135.84984,
            text=T("延暦寺 横川（よかわ）\n\n"
                   "お昼は峰道で\n"
                   "東塔の延暦寺バスセンター12:38発のバスに乗り、西塔の次の「峰道（みねみち）」で降ります（7分・390円）。バス停の前が比叡山峰道レストランで、大きな窓から琵琶湖を見下ろして食べられます（10:00〜17:00、ラストオーダー16:30）。比叡山そば1,000円、ごま豆腐や湯葉の入った精進のあんかけ丼「平和丼」1,400円、近江牛のカレー1,300円など。\n\n"
                   "峰道13:45発のバスで横川へ（6分・450円）。乗り遅れたら14:15発（横川14:21着）。\n\n"
                   "横川\n"
                   "西塔から北へ約4km。バスが走る季節（2026年は12月6日まで）だけ行ける場所で、ここまで来る人は少なく、3つのエリアの中でいちばん静かです。\n\n"
                   "・横川中堂（よかわちゅうどう）：横川の本堂。斜面に柱を組んだ舞台造りで、朱色のお堂が船のように浮かんで見えます。遣唐使の船をモデルにしたといわれます。今の建物は1971年の再建。下の道から見上げた姿がいちばんきれいです（写真1枚目）。\n"
                   "・元三大師堂（がんざんだいしどう）：横川中堂から歩いて5分ほど。10世紀に延暦寺を立て直した良源（りょうげん＝元三大師）をまつります。おみくじは元三大師が考えたものといわれ、ここが「おみくじ発祥の地」です。角の生えた鬼の姿の魔よけのお札「角大師（つのだいし）」もここのものです。\n"
                   "・恵心堂（えしんどう）：『往生要集』を書いた源信（げんしん）ゆかりのお堂。中には入れません。\n\n"
                   "バス停から横川中堂まで歩いて5分。中堂と元三大師堂で1時間ほどです。\n\n"
                   "帰りのバス\n"
                   "横川15:00発で西塔へ（10分・600円）。乗り遅れたら15:30発（西塔15:40着。そのまま比叡山頂へ行けます）。最後は16:10発で、比叡山頂16:30着。\n"
                   "16:10にも乗り遅れたら、比叡山頂から来る奥比叡ドライブバスが横川16:22発で山を下り、おごと温泉駅16:41着（950円）。そこからJR湖西線で京都へ帰れます。これが山の上から出る最後のバスです。"
                   + time_ja("13:51〜14:55"),
                   "Enryaku-ji: Yokawa\n\n"
                   "Lunch at Minemichi\n"
                   "Take the 12:38 bus from the Enryakuji Bus Center at Todo and get off at Minemichi, the stop after Saito (7 minutes, ¥390). Right by the stop is the Hieizan Minemichi Restaurant, with big windows over Lake Biwa (10:00–17:00, last orders 16:30). Hieizan soba ¥1,000, the Heiwa-don, a temple-style bowl with sesame tofu and yuba in a thick sauce, ¥1,400, Omi beef curry ¥1,300 and more.\n\n"
                   "Then the 13:45 bus to Yokawa (6 minutes, ¥450). If you miss it, the 14:15 (Yokawa 14:21).\n\n"
                   "Yokawa\n"
                   "About 4 km north of Saito, and only reachable while the bus runs (until 6 December in 2026). Few visitors get this far: it is the quietest of the three areas.\n\n"
                   "• Yokawa Chudo: the main hall of Yokawa, built out over the slope on stilts, so the vermilion hall seems to float like a ship. It is said to be modelled on the ships of the envoys to Tang China. The present building dates from 1971. The best view is looking up from the path below (photo 1).\n"
                   "• Ganzan Daishi-do: about 5 minutes’ walk from the Chudo, dedicated to Ryogen (Ganzan Daishi), who revived Enryaku-ji in the tenth century. He is credited with inventing omikuji, so this is known as their birthplace. The Tsuno Daishi charm against evil, a horned demon figure, also comes from here.\n"
                   "• Eshin-do: a hall linked to Genshin, author of the Ojoyoshu. Closed inside.\n\n"
                   "It is 5 minutes’ walk from the bus stop to the Chudo. Allow about an hour for the Chudo and the Ganzan Daishi-do.\n\n"
                   "The bus back\n"
                   "The 15:00 from Yokawa to Saito (10 minutes, ¥600). If you miss it, the 15:30 (Saito 15:40; it carries on to the summit). The last is the 16:10, reaching the summit at 16:30.\n"
                   "Miss the 16:10 too and there is still the Oku-Hiei Drive Bus from the summit, leaving Yokawa at 16:22 down the mountain to Ogoto-onsen station (16:41, ¥950), where the JR Kosei line takes you back to Kyoto. That is the last bus off the mountain."
                   + time_en("13:51–14:55")),
            gmaps=[gm("延暦寺 横川中堂", "Enryaku-ji Yokawa Chudo", 35.09680, 135.84984, "延暦寺 横川中堂"),
                   gm("比叡山峰道レストラン", "Hieizan Minemichi Restaurant", None, None, "比叡山峰道レストラン")],
            links=[link("official", "横川の案内（延暦寺）", "Yokawa area guide (official, Japanese)", "https://www.hieizan.or.jp/grounds/yokawa.html"), MINEMICHI, TT],
            info=info([row("hours", "3〜11月 9:00〜16:00／12月 9:30〜16:00（巡拝受付は15:45まで）。東塔の巡拝券で入れます", "Mar–Nov 9:00–16:00 / Dec 9:30–16:00 (last entry 15:45). Your Todo ticket covers it"),
                       row("hours", "比叡山峰道レストラン 10:00〜17:00（ラストオーダー16:30）。シャトルバス「峰道」下車すぐ", "Hieizan Minemichi Restaurant 10:00–17:00 (last orders 16:30), right by the Minemichi bus stop"),
                       row("train", "峰道 → 横川：13:45、14:15発（6分・450円）。横川 → 西塔：15:00、15:30発（10分・600円）。横川 → 比叡山頂：16:10発が最後（16:30着）。どれも毎日、2026年3月20日〜12月6日の時刻",
                           "Minemichi → Yokawa: 13:45, 14:15 (6 min, ¥450). Yokawa → Saito: 15:00, 15:30 (10 min, ¥600). Yokawa → summit: the 16:10 is the last (arr. 16:30). All daily; timetable for 20 Mar–6 Dec 2026"),
                       row("train", "最後の手：奥比叡ドライブバス 横川16:22発 → おごと温泉駅16:41着（950円）", "Last resort: Oku-Hiei Drive Bus, Yokawa 16:22 → Ogoto-onsen station 16:41 (¥950)")],
                      tip=T("延暦寺の公式サイト、比叡山峰道レストランの公式サイト、比叡山・びわ湖DMOの時刻表（PDF、2026年3月20日〜12月6日）で確認しました（2026年11月22日）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                            "Checked on Enryaku-ji’s website, the restaurant’s website and the DMO timetable (PDF, 20 March–6 December 2026) on 22 November 2026. Photos are from Wikimedia Commons (author and license shown on each photo).")))

    # ---------- 西塔
    saito_common_ja = ("東塔から西へ約1km。杉木立の中にお堂が点々とあり、東塔より人がずっと少ない場所です。\n\n"
                       "・にない堂：同じ形のお堂が2つ、渡り廊下でつながっています。左が常行堂（じょうぎょうどう）、右が法華堂（ほっけどう）。弁慶がこの廊下をてんびん棒にして2つのお堂をかついだ、という言い伝えから「にない堂」と呼ばれます。今も修行に使われていて、中には入れません。廊下の下をくぐって先へ進みます（写真1枚目）。\n"
                       "・釈迦堂（しゃかどう）：石段を下りた広場の奥。西塔の本堂で、延暦寺に残る建物の中でいちばん古いものです。もとは三井寺（みいでら）の金堂で、1595年に秀吉がここへ移しました。\n"
                       "・浄土院（じょうどいん）：東塔との境にある、最澄の墓所です。12年間山を下りない修行のお坊さんが、今も毎日、最澄が生きているかのように食事を供え、掃除をしています。東塔から歩く道の途中にあります。\n\n")
    saito_common_en = ("About 1 km west of Todo: halls here and there among tall cedars, with far fewer people than at Todo.\n\n"
                       "• Ninai-do: two identical halls joined by a raised corridor, the Jogyo-do on the left and the Hokke-do on the right. The name, “shouldering halls”, comes from the legend that the warrior monk Benkei lifted the pair with the corridor as a carrying pole. They are still used for training and are closed inside. You walk on under the corridor (photo 1).\n"
                       "• Shaka-do: down the stone steps, at the back of the open ground. The main hall of Saito and the oldest building left at Enryaku-ji. It was the main hall of Mii-dera until Hideyoshi had it moved here in 1595.\n"
                       "• Jodo-in: Saicho’s mausoleum, on the boundary with Todo. A monk on a twelve-year retreat, never leaving the mountain, still serves meals and sweeps here every day as if Saicho were alive. It is on the path from Todo.\n\n")
    if W:
        s_ja = ("冬は歩いて行きます。東塔から、浄土院の前を通る山道で西塔へ。延暦寺の案内では20分、比叡山・びわ湖DMOの案内では約40分。未舗装で、坂と石段があります。14:15に東塔を出て、14:50ごろ着く見込みです。\n\n"
                "西塔は12〜2月は9:30〜16:00（巡拝受付は15:45まで）。にない堂と釈迦堂で30分ほど。15:25には戻り始めてください。ケーブル延暦寺駅まで、来た道を30〜50分。16:30のケーブルに乗ります（最終は17:00）。\n\n"
                "雪や凍った道のときは無理をしないで、東塔だけにしてください。山の上は日が傾くと急に冷えます。")
        s_en = ("In winter you walk: the hill path from Todo passes Jodo-in on the way to Saito. The temple says 20 minutes, the DMO about 40. It is unpaved, with slopes and stone steps. Leave Todo at 14:15 and expect to arrive about 14:50.\n\n"
                "From December to February Saito is open 9:30–16:00 (last entry 15:45). The Ninai-do and Shaka-do take about 30 minutes. Start back by 15:25: 30–50 minutes the way you came to Cable Enryakuji station, for the 16:30 car down (the last is 17:00).\n\n"
                "If there is snow or ice, don’t push it: see Todo only. It gets cold fast up here once the sun drops.")
        s_time = ("14:50〜15:25", "14:50–15:25")
    else:
        s_ja = ("このコースでは横川からバスで来ます（15:10着）。にない堂と釈迦堂で30分ほど。巡拝受付は15:45までです。\n\n"
                "西塔15:40発のバスで比叡山頂へ（10分・400円。東塔のバスセンターを通ります）。乗り遅れたら16:20発が最後（16:30着）。浄土院は東塔へ歩く道の途中なので、このコースでは通りません。")
        s_en = ("On this course you arrive by bus from Yokawa at 15:10. The Ninai-do and Shaka-do take about 30 minutes. Last entry is 15:45.\n\n"
                "Then the 15:40 bus to the summit (10 minutes, ¥400, via the Bus Center at Todo). If you miss it, the 16:20 is the last (arr. 16:30). Jodo-in lies on the footpath to Todo, so this course doesn’t pass it.")
        s_time = ("15:10〜15:40", "15:10–15:40")
    S["saito"] = dict(
        name=T("延暦寺 西塔（にない堂・釈迦堂）", "Enryaku-ji: Saito"), kind=T("寺", "Temple"),
        blurb=T("杉木立の中の静かなエリア。廊下でつながった2つのお堂「にない堂」と、山でいちばん古い建物の釈迦堂。" + ("冬は東塔から歩いて往復。" if W else "15:40のバスで山頂へ。"),
                "A quiet area among tall cedars: the twin halls joined by a corridor, and the Shaka Hall, the oldest building on the mountain. " + ("In winter, walk there and back from Todo." if W else "The 15:40 bus takes you on to the summit.")),
        caution=(T("歩いて片道20〜40分。雪の日はやめて東塔だけに", "20–40 min walk each way; skip it on snowy days") if W
                 else T("巡拝受付は15:45まで。山頂へのバスの最後は16:20", "Last entry 15:45; last bus to the summit 16:20")),
        lat=35.07430, lng=135.83395,
        text=T("延暦寺 西塔（さいとう）\n\n" + saito_common_ja + s_ja + time_ja(s_time[0]),
               "Enryaku-ji: Saito (West Pagoda area)\n\n" + saito_common_en + s_en + time_en(s_time[1])),
        gmaps=[gm("延暦寺 西塔（釈迦堂）", "Enryaku-ji Saito (Shaka-do)", 35.07430, 135.83395, "延暦寺 釈迦堂 西塔"), gm("浄土院", "Jodo-in", 35.07149, 135.83614, "延暦寺 浄土院")],
        links=[link("official", "西塔の案内（延暦寺）", "Saito area guide (official, Japanese)", "https://www.hieizan.or.jp/grounds/saitou.html")] + ([] if W else [TT]),
        notices=[WINTER] if W else [],
        info=info([row("hours", "3〜11月 9:00〜16:00／12〜2月 9:30〜16:00（巡拝受付は15:45まで）", "Mar–Nov 9:00–16:00 / Dec–Feb 9:30–16:00 (last entry 15:45)"),
                   row("fee", "東塔の巡拝券で入れます（3エリア共通 1,000円）", "Covered by the ticket from Todo (¥1,000 for all three areas)"),
                   row("hours", "東塔から歩くと20〜40分（延暦寺の案内は20分、比叡山・びわ湖DMOの案内は約40分。未舗装・坂・階段あり）", "On foot from Todo: 20–40 minutes (20 according to the temple, about 40 according to the DMO; unpaved, with slopes and steps)")]
                  + ([] if W else [row("train", "西塔 → 比叡山頂：15:40発（15:50着）、16:20発が最後（16:30着）。10分・400円。毎日、2026年3月20日〜12月6日の時刻",
                                       "Saito → summit: 15:40 (arr. 15:50); the 16:20 is the last (arr. 16:30). 10 min, ¥400. Daily; timetable for 20 Mar–6 Dec 2026")]),
                  tip=T("延暦寺の公式サイトと比叡山・びわ湖DMOの時刻表（PDF）で確認しました（2026年11月22日）。写真は Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                        "Checked on Enryaku-ji’s website and the DMO timetable (PDF) on 22 November 2026. Photos are from Wikimedia Commons (author and license shown on each photo).")))

    # ---------- 比叡山頂と叡山ロープウェイ・ケーブル（山を越える日だけ）
    if not W:
        S["sancho"] = dict(
            name=T("比叡山頂と叡山ロープウェイ・ケーブル", "Summit, Eizan Ropeway & Cable"), kind=T("ロープウェイ・ケーブル", "Ropeway & cable car"),
            blurb=T("バス停から歩いて10分のロープウェイで3分、ケーブルカーで9分。京都側の八瀬へ下ります。16:15のロープウェイに。",
                    "Ten minutes’ walk from the bus stop, then 3 minutes by ropeway and 9 by cable car down to Yase on the Kyoto side. Aim for the 16:15 ropeway."),
            caution=T("バス停からロープウェイまで歩いて10分。下りの最終はロープウェイ18:00", "10 min walk from the bus to the ropeway; last ropeway down 18:00"),
            lat=35.06443, lng=135.82776,
            text=T("比叡山頂と叡山ロープウェイ・ケーブル\n\n"
                   "シャトルバスの終点「比叡山頂」に15:50に着きます。ロープウェイの比叡山頂駅までは、バス停から歩いて約10分。ガーデンミュージアム比叡の横を通ります。\n\n"
                   "山頂のあたりは見晴らしがよく、晴れた日は遠くの山まで見えます（写真1枚目は2016年11月13日）。\n\n"
                   "下り方\n"
                   "・ロープウェイ：比叡山頂駅 → ロープ比叡駅 3分・400円。\n"
                   "・歩いて1分で乗り換え。\n"
                   "・ケーブルカー：ケーブル比叡駅 → ケーブル八瀬駅 9分・600円。高低差561mは日本一で、かなり急です。下りは先頭に立つと、線路が落ちていくように見えます。\n\n"
                   "平日はケーブルが30分おき（毎時0分・30分）なので、16:15発のロープウェイ → 16:30発のケーブルで、八瀬16:39着。乗り遅れたら16:45発 → 17:00発で17:09着。土日祝はどちらも15分おきです。下りの最終は、ロープウェイ18:00発・ケーブル18:15発。\n\n"
                   "叡山ロープウェイとケーブルは現金のみで、ICカードは使えません。フリーパスがない人は、現金を1,000円用意しておいてください。\n\n"
                   "ロープウェイに乗らず、バスで三条へ直接帰ることもできます。比叡山頂16:05発の比叡山ドライブバスで三条京阪17:00着（840円、毎日）。\n\n"
                   "ガーデンミュージアム比叡は、モネなど印象派の絵をテーマにした庭園です（12月6日まで、水曜休み。秋は10:00〜17:00、入園16:30まで。11月24日からは600円）。このコースでは時間がありません。寄るなら横川を外してください。\n\n"
                   "2026年は12月6日（日）までのコースです（ケーブル・ロープウェイの平日の時刻表は12月4日まで）。"
                   + time_ja("15:50に山頂着、16:15発のロープウェイ"),
                   "Summit, Eizan Ropeway & Cable\n\n"
                   "The shuttle bus reaches its last stop, Hiei-sancho, at 15:50. The ropeway’s summit station is about 10 minutes’ walk from the bus stop, past the Garden Museum Hiei.\n\n"
                   "The summit area has open views, far across the hills on a clear day (photo 1: 13 November 2016).\n\n"
                   "Going down\n"
                   "• Ropeway: Hiei-sancho → Rope Hiei, 3 minutes, ¥400.\n"
                   "• One minute’s walk to change.\n"
                   "• Cable car: Cable Hiei → Cable Yase, 9 minutes, ¥600. Its 561 m drop is the greatest of any cable car in Japan, and it is steep. Going down, stand at the front and the track seems to fall away.\n\n"
                   "On weekdays the cable car runs every 30 minutes (on the hour and half hour), so the 16:15 ropeway connects with the 16:30 cable car, reaching Yase at 16:39. Miss it and the 16:45 and 17:00 get you there at 17:09. At weekends and on holidays both run every 15 minutes. Last runs down: ropeway 18:00, cable car 18:15.\n\n"
                   "The Eizan Ropeway and Cable take cash only; IC cards are not accepted. Without the Free Pass, have ¥1,000 in cash ready.\n\n"
                   "You can also skip the ropeway and take a bus straight to Sanjo: the 16:05 Hieizan Drive Bus from the summit reaches Sanjo-Keihan at 17:00 (¥840, daily).\n\n"
                   "The Garden Museum Hiei is a garden themed on Monet and the Impressionists (until 6 December, closed Wednesdays; 10:00–17:00 in autumn, last entry 16:30; ¥600 from 24 November). There is no time for it on this course: drop Yokawa if you want it.\n\n"
                   "In 2026 this course runs until Sunday 6 December (the weekday timetable for the cable car and ropeway ends on 4 December)."
                   + time_en("reach the summit at 15:50; ropeway at 16:15")),
            gmaps=[gm("叡山ロープウェイ 比叡山頂駅", "Eizan Ropeway, Hiei-sancho Station", 35.06443, 135.82776, "叡山ロープウェイ 比叡山頂駅"), gm("比叡山頂バス停", "Hiei-sancho bus stop", 35.06585, 135.83130, "ガーデンミュージアム比叡")],
            links=[EIZANCABLE, link("official", "叡山ケーブル・ロープウェイ 運賃", "Eizan Cable & Ropeway fares (Japanese)", "https://www.keifuku.co.jp/cms/eizan_ticket/"), TT,
                   link("info", "ガーデンミュージアム比叡（比叡山・びわ湖DMO）", "Garden Museum Hiei (DMO, Japanese)", "https://www.hieizan.gr.jp/hieizan/garden-museum-hiei")],
            notices=[SEASON],
            info=info([row("train", "ロープウェイ（比叡山頂発）：9時台 15・30・45分、10〜17時台 15分おき、最終18:00。ケーブル（ケーブル比叡発）：平日 毎時0・30分、土日祝 15分おき、最終18:15。時刻表は平日12月4日・土日祝12月6日まで",
                           "Ropeway (from the summit): at :15, :30, :45 in the 9 o’clock hour, then every 15 min, last 18:00. Cable car (from Cable Hiei): weekdays :00 and :30; weekends and holidays every 15 min; last 18:15. Timetable valid to 4 Dec (weekdays) and 6 Dec (weekends)"),
                       row("fee", "ロープウェイ 片道400円、ケーブル 片道600円。現金のみ（ICカードは使えません）", "Ropeway ¥400, cable car ¥600, one way. Cash only (no IC cards)"),
                       row("hours", "比叡山頂バス停 → ロープウェイ比叡山頂駅：歩いて約10分（京福電鉄の案内）", "Hiei-sancho bus stop → ropeway summit station: about 10 min on foot (operator’s guide)"),
                       row("train", "バスで三条へ：比叡山ドライブバス 比叡山頂15:05発 → 三条京阪16:01着、16:05発 → 17:00着（毎日、840円）", "By bus to Sanjo: Hieizan Drive Bus from the summit 15:05 → Sanjo-Keihan 16:01, 16:05 → 17:00 (daily, ¥840)"),
                       row("fee", "ガーデンミュージアム比叡：大人1,200円（11月24日〜12月6日は600円）、水曜休み、12月6日まで", "Garden Museum Hiei: ¥1,200 (¥600 from 24 Nov to 6 Dec); closed Wednesdays; open until 6 December", until="2026-12-06")],
                      tip=T("京福電鉄（叡山ケーブル・ロープウェイ）の公式サイト（払い方はよくある質問、11月23日）、比叡山・びわ湖DMOの時刻表（PDF、2026年3月20日〜12月6日）とガーデンミュージアム比叡の案内で確認しました（2026年11月22日）。写真1枚目は私の写真、ほかは Wikimedia Commons から（撮影者とライセンスを写真の上に表示）。",
                            "Checked on the Keifuku (Eizan Cable & Ropeway) website (payment on its FAQ, 23 November), the DMO timetable (PDF, 20 March–6 December 2026) and the Garden Museum page on 22 November 2026. Photo 1 is mine; the others are from Wikimedia Commons (author and license shown on each photo)."), cash=True))

        # ---------- 八瀬と帰り・夜
        S["yase"] = dict(
            name=T("八瀬（もみじの小径）と、帰り・夜", "Yase, the way back & the evening"), kind=T("駅・もみじ・夜", "Station, maples & evening"),
            blurb=T("ケーブル八瀬駅のまわりはもみじの名所。叡山電車で出町柳へ14分、京阪で三条へ。夜は先斗町・木屋町で。",
                    "The foot of the cable car is a maple spot. 14 minutes to Demachiyanagi by the Eizan railway, then Keihan to Sanjo. Evening in Pontocho and Kiyamachi."),
            lat=35.06692, lng=135.80865,
            text=T("八瀬（やせ）と、帰り・夜\n\n"
                   "ケーブル八瀬駅を出ると、目の前がもみじの林です。駅のすぐ横に「もみじの小径（こみち）」という短い散歩道があります。私の写真は2024年12月3日のもので、12月に入っても真っ赤でした。町なかより色づきが遅い年もあります。\n\n"
                   "坂を下り、高野川（たかのがわ）の橋を渡ると、叡山電車の八瀬比叡山口（やせひえいざんぐち）駅です。歩いて5分。橋の上から見る川ともみじもきれいです（写真6枚目）。1925年に開業した駅で、古い駅舎が残っています（写真1枚目）。\n\n"
                   "帰り方\n"
                   "・叡山電車：八瀬比叡山口17:00発 → 出町柳17:13着（280円）。昼間から17時台は15分おきくらいで、平日は17:14、17:26発…。秋は臨時の時刻になる日があります。出町柳で京阪に乗り換えて三条へ3〜4分（240円）。17:22発なら三条17:26着。\n"
                   "・京都バス：八瀬駅前（駅から歩いてすぐ）17:12発の17系統で三条京阪前17:40着（370円、乗り換えなし）。次は17:42発（18:10着）。秋の夕方は道が混んで遅れることがあります。\n\n"
                   "出町柳で降りて、鴨川デルタ（川が合わさる三角の河原と飛び石。駅から歩いて3分）に寄ってから京阪に乗るのもいい時間です。\n\n"
                   + EVENING_JA + "\n\n"
                   "叡山電車の沿線（一乗寺・貴船・鞍馬）は、別の「叡山電鉄」のマップで紹介しています。"
                   + time_ja("16:40〜17:00（17:00発の電車）"),
                   "Yase, the way back & the evening\n\n"
                   "Step out of Cable Yase station and you are in a maple wood. Beside the station is a short path called Momiji-no-komichi. My photos are from 3 December 2024, when the leaves were still deep red. Some years the colour comes later here than in the city.\n\n"
                   "Go down the slope and over the bridge across the Takano river to Yase-Hieizanguchi station on the Eizan railway: 5 minutes on foot. The river and maples from the bridge are worth a stop (photo 6). The station opened in 1925 and keeps its old building (photo 1).\n\n"
                   "Getting back\n"
                   "• Eizan railway: Yase-Hieizanguchi 17:00 → Demachiyanagi 17:13 (¥280). About every 15 minutes through the afternoon; on weekdays then 17:14, 17:26… Some autumn days run a special timetable. Change at Demachiyanagi to the Keihan line for Sanjo, 3–4 minutes (¥240): the 17:22 reaches Sanjo at 17:26.\n"
                   "• Kyoto Bus: from Yase-ekimae (right by the station), bus 17 at 17:12 to Sanjo-Keihan-mae, 17:40 (¥370, no change). Next at 17:42 (18:10). On autumn evenings traffic can make it late.\n\n"
                   "At Demachiyanagi you could also walk 3 minutes to the Kamo delta, where two rivers meet, with stepping stones, before taking the Keihan train.\n\n"
                   + EVENING_EN + "\n\n"
                   "The places along the Eizan railway (Ichijoji, Kibune, Kurama) are on my separate Eizan Railway map."
                   + time_en("16:40–17:00 (17:00 train)")),
            gmaps=[gm("ケーブル八瀬駅", "Cable Yase Station", 35.06692, 135.80865, "ケーブル八瀬駅"), gm("八瀬比叡山口駅", "Yase-Hieizanguchi Station", 35.06522, 135.80849, "八瀬比叡山口駅"),
                   gm("先斗町", "Pontocho", 35.00590, 135.77100, "先斗町 京都")],
            links=[link("timetable", "叡山電車 時刻表", "Eizan railway timetable (Japanese)", "https://eizandensha.co.jp/guide/#timetable"), KBUS_YASE, ROUTE,
                   link("info", "叡山電鉄のマップ（このサイト）", "My Eizan Railway map (this site)", "../eizan-line/"), EIZANMAP],
            info=info([row("train", "八瀬比叡山口 → 出町柳：叡山電車 14分・280円。10〜16時台は毎時0・15・30・45分発、平日17時台は0・14・26・43・55分、土日祝17時台は0・15・30・45分（紅葉の時期は変わる日あり）",
                           "Yase-Hieizanguchi → Demachiyanagi: Eizan railway, 14 min, ¥280. At :00, :15, :30, :45 from 10:00 to 16:59; in the 17 o’clock hour :00, :14, :26, :43, :55 on weekdays and :00, :15, :30, :45 at weekends (special timetable on some autumn days)"),
                       row("train", "出町柳 → 三条：京阪 3〜4分・240円", "Demachiyanagi → Sanjo: Keihan, 3–4 min, ¥240"),
                       row("train", "京都バス17系統：八瀬駅前 17:12発 → 三条京阪前 17:40着、17:42発 → 18:10着（370円）", "Kyoto Bus 17: Yase-ekimae 17:12 → Sanjo-Keihan-mae 17:40, 17:42 → 18:10 (¥370)"),
                       row("hours", "ケーブル八瀬駅 → 八瀬比叡山口駅・八瀬駅前バス停：歩いて約5分", "Cable Yase → Yase-Hieizanguchi station or Yase-ekimae bus stop: about 5 min on foot")],
                      tip=T("叡山電車は比叡山・びわ湖DMOの時刻表（PDF）と乗換案内（2026年11月24日・28日）、京都バスは乗換案内（11月24日・28日）、歩く時間は京福電鉄の案内で確認しました。先斗町の店の営業時間は、1軒ずつは確かめていません。",
                            "The Eizan railway was checked on the DMO timetable (PDF) and a route planner (24 and 28 November 2026); Kyoto Bus on a route planner (same dates); walking times from Keifuku’s guide. Opening hours of individual places in Pontocho were not checked.")))

    # ---------- 並べる
    if W:
        order = ["kyoto", "omijingu", "chikurin", "hiyoshi", "cable", "toto", "saito", "sakamoto"]
        pick_ids = ["omijingu", "chikurin", "hiyoshi", "saito"]
        default = ["chikurin", "hiyoshi", "saito"]
        always = ["kyoto", "cable", "toto", "sakamoto"]
    else:
        order = ["kyoto", "omijingu", "sakamoto", "chikurin", "hiyoshi", "cable", "toto", "yokawa", "saito", "sancho", "yase"]
        pick_ids = ["omijingu", "chikurin", "hiyoshi", "yokawa", "saito"]
        default = ["hiyoshi", "yokawa", "saito"]
        always = ["kyoto", "sakamoto", "cable", "toto", "sancho", "yase"]
    spots = []
    for i, sid in enumerate(order, 1):
        s = dict(S[sid])
        out = {"no": i, "id": sid}
        out.update(s)
        out["photos"] = PHOTOS[sid]
        for p in out["photos"]:
            f = p if isinstance(p, str) else p["file"]
            assert os.path.exists(f"{IMG}/{f}"), f
        out.setdefault("notices", [])
        spots.append(out)
    NO = {s["id"]: s["no"] for s in spots}
    ALLP = sorted(NO[k] for k in pick_ids)
    # rule は any が必須（テンプレートの ruleOk）。none だけの条件には「どれか1つでも選んでいれば」の any を足す
    H = lambda spot, rule, ja, en: {"spot": NO[spot], "rule": rule if "any" in rule else dict(rule, any=ALLP), "from": None, "to": None, "text": T(ja, en)}
    OMI = H("kyoto", {"any": [NO["omijingu"]]},
            "近江神宮に寄るので、三条京阪を平日7:55発（土曜8:03発）の「びわ湖浜大津行き」に乗ります。近江神宮前8:26着（土曜8:33着）。参拝のあと平日9:14発（土曜9:13発）で坂本比叡山口へ。そこからはふつうの時間割どおりです。",
            "You chose Omi Jingu: take the 7:55 (Saturdays 8:03) train for Biwako-Hamaotsu from Sanjo-Keihan, reaching Omijingu-mae at 8:26 (8:33). After the shrine, the 9:14 (Saturdays 9:13) to Sakamoto-hieizanguchi, and from there the timetable is as usual.")
    if W:
        sections = [{"first": NO["kyoto"], "last": NO["omijingu"], "day": 0}, {"first": NO["chikurin"], "last": NO["hiyoshi"], "day": 1},
                    {"first": NO["cable"], "last": NO["toto"], "day": 2}, {"first": NO["saito"], "last": NO["saito"], "day": 3},
                    {"first": NO["sakamoto"], "last": NO["sakamoto"], "day": 4}]
        hints = [OMI,
                 H("toto", {"none": [NO["saito"]]},
                   "西塔へ行かない日は、東塔を15時ごろまでゆっくり見て、15:30のケーブルで下りてください。坂本の石垣の町を歩いて、16時台の電車で三条へ（17時前後に着きます）。",
                   "Not going to Saito? Take your time at Todo until about 15:00 and ride the 15:30 cable car down. Walk the stone-walled town and catch a train in the 16 o’clock hour (back in Sanjo around 17:00)."),
                 H("hiyoshi", {"none": [NO["chikurin"]]},
                   "旧竹林院に寄らない日（月曜など）は、日吉大社に9:55ごろ入れます。ゆっくり見ても、11時に鶴屋喜八が開くのにちょうどいい時間です。",
                   "Skipping Kyu Chikurin-in (closed on Mondays, for instance)? You can be at Hiyoshi Taisha by about 9:55, and even at a slow pace you’ll reach Tsuruya Kihachi as it opens at 11:00.")]
        plan_note = "「選んで回る」の設定。三条からの電車・坂本ケーブル・東塔・坂本の町（帰り）はいつも入る。defaultPicks は時間割どおりの組み合わせ。"
        focus = {"first": NO["chikurin"], "last": NO["sakamoto"]}
        note = ("冬：坂本から往復のコース（early）。三条京阪9:01→坂本比叡山口9:42→旧竹林院→日吉大社→鶴屋喜八でお昼11:20→坂本ケーブル12:30→東塔→歩いて西塔→坂本ケーブル16:30→夕暮れの坂本→京阪17:11→三条17:55→先斗町。"
                "12月7日〜春（山内シャトルバスが運休の時期）用。")
    else:
        sections = [{"first": NO["kyoto"], "last": NO["omijingu"], "day": 0}, {"first": NO["sakamoto"], "last": NO["hiyoshi"], "day": 1},
                    {"first": NO["cable"], "last": NO["toto"], "day": 2}, {"first": NO["yokawa"], "last": NO["yokawa"], "day": 3},
                    {"first": NO["saito"], "last": NO["sancho"], "day": 4}, {"first": NO["yase"], "last": NO["yase"], "day": 5}]
        hints = [OMI,
                 H("chikurin", {"any": [NO["chikurin"]]},
                   "旧竹林院に寄るなら：9:55〜10:20に旧竹林院、10:25〜11:15に日吉大社、坂本ケーブルは11:30発。東塔は13:00まで見て、13:08のバスで峰道へ（お昼13:15〜）。峰道14:15発で横川14:21着、そのあとは同じ（横川15:00発）です。",
                   "Adding Kyu Chikurin-in: the garden 9:55–10:20, Hiyoshi Taisha 10:25–11:15, the 11:30 Sakamoto Cable. Stay at Todo until 13:00 and take the 13:08 bus to Minemichi (lunch from 13:15). The 14:15 from Minemichi reaches Yokawa at 14:21; after that it is the same (the 15:00 from Yokawa)."),
                 H("toto", {"none": [NO["yokawa"]]},
                   "横川へ行かない日は、12:38のバスで峰道へ行ってお昼、峰道13:36発で西塔13:40着。西塔をゆっくり見て14:40発で比叡山頂14:50着。ガーデンミュージアム比叡（12月6日まで、水曜休み、入園16:30まで）に寄って、16:15のロープウェイで下りても時間があります。",
                   "Not going to Yokawa? Take the 12:38 bus to Minemichi for lunch, then the 13:36 to Saito (13:40). After a slow look round, the 14:40 reaches the summit at 14:50: time for the Garden Museum Hiei (until 6 December, closed Wednesdays, last entry 16:30) before the 16:15 ropeway."),
                 H("yokawa", {"any": [NO["yokawa"]], "none": [NO["saito"]]},
                   "西塔へ行かない日は、横川15:00発のバスに乗ったまま比叡山頂へ（15:20着）。15:45のロープウェイで、八瀬に16時過ぎに着きます。",
                   "Not going to Saito? Stay on the 15:00 bus from Yokawa to the summit (15:20). The 15:45 ropeway gets you to Yase just after 16:00."),
                 H("cable", {"none": [NO["hiyoshi"]]},
                   "日吉大社に寄らない日は、坂本比叡山口9:42着から歩いて約15分で、10:00か10:30のケーブルに乗れます。東塔で時間が増えるので、国宝殿（500円）もゆっくり見られます。",
                   "Skipping Hiyoshi Taisha? From the 9:42 arrival it is about 15 minutes on foot to the cable car: take the 10:00 or 10:30. That gives you more time at Todo, including the Kokuhoden museum (¥500).")]
        plan_note = "「選んで回る」の設定。三条からの電車・坂本の町・坂本ケーブル・東塔・山頂とロープウェイ・八瀬はいつも入る。defaultPicks は時間割どおりの組み合わせ。"
        focus = {"first": NO["sakamoto"], "last": NO["yase"]}
        note = ("山を越えるコース（late。最初に開く。12月7日〜3月19日は日付で冬のコースが開く）。三条京阪9:01→坂本比叡山口9:42→坂本の町→日吉大社→坂本ケーブル11:00→東塔→バス12:38→峰道でお昼→13:45→横川→15:00→西塔→15:40→比叡山頂15:50→ロープウェイ16:15→ケーブル16:30→八瀬16:39→叡山電車17:00→出町柳→三条17:26→先斗町。"
                "山内シャトルバスが走る3月20日〜12月6日（2026年）だけ。")
    data = {
        "id": "hieizan",
        "course": "early" if W else "late",
        "_note": "京都から日帰り 比叡山延暦寺と坂本のルート（hieizan/ のページ専用。形は eizan-line.json と同じ）。" + note +
                 "2026-11-22 に「ゲストが実際に回れる1日」として見直し、2つのコース（一覧の上のボタン）に分けた。三条からの電車、乗り遅れたときの次の便、お昼（峰道レストラン・鶴屋喜八）、最後のバス、夜の過ごし方を足した。"
                 "写真は Toshi の写真ライブラリから（東塔の鐘楼・もみじ・杉木立、日吉大社の赤鳥居、山頂の眺め＝2016年11月13日／近江神宮＝2025年1月18日／八瀬＝2024年12月3日）。そのほかは Wikimedia Commons（photos の要素が {file, credit}）。"
                 "店名を出したのは、公式サイトで時間を確かめた比叡山峰道レストラン・比叡茶寮・手打蕎麦 鶴屋喜八だけ（Toshi が行ったとは書いていない）。延暦寺会館の食事は公式で確かめられず、名前を出していない。"
                 "確かめたページは sources。until のついた行はその日を過ぎると消える。2027年の運行期間・パスの値段が出たら直す。このファイルは scripts/build_hieizan_data.py で作る。",
        "sections": sections,
        "focus": focus,
        "plan": {"_note": plan_note, "defaultMode": "pick",
                 "picks": sorted(NO[k] for k in pick_ids), "defaultPicks": sorted(NO[k] for k in default),
                 "auto": {str(NO[k]): {"always": True} for k in always}, "hints": hints},
        "photoBase": "../images/hieizan/",
        "spots": spots,
        "sources": SOURCES,
    }
    out = f"{R}/data/routes/hieizan{'-early' if W else ''}.json"
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, [(s["no"], s["id"], len(s["photos"])) for s in spots])


build(False)
build(True)
