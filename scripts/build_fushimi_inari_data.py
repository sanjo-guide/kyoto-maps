#!/usr/bin/env python3
"""伏見稲荷から七条へ（伏見稲荷・東福寺・泉涌寺・三十三間堂・サウナの梅湯・Kyoto Beer Lab）のデータを、2つのコース分まとめて書き出す。

使い方: python3 scripts/build_fushimi_inari_data.py
- 作るもの（COURSES）:
  - data/routes/fushimi-inari.json … 「9〜10時に出発」
  - data/routes/fushimi-inari-early.json … 「早朝に出発」（三条5:24発の京阪で、6:00より前に入口へ）
  どちらも直接直さない（実行のたびに作り直す）
- 文章・料金・時間はこのファイルに書いてある。直したらこのスクリプトを実行し直す
  - BASE … スポットごとの、コースで変わらない内容（説明・料金・注意・リンク）
  - COURSES … コースごとの並び順、めやすの時間、そのコースでの行き方の一言、「選んで回る」の設定
- 紹介ページ（fushimi-inari/js/i18n.js）の写真は id で指定している
- 写真は images/fushimi-inari/<スポットのid>-<番号>.jpg を番号の順に全部使う
  （駅・伏見稲荷・東福寺・泉涌寺・三十三間堂は、2026-11-22 に images/higashiyama/ から移した）
- 2026-11-22 作成（オーナーの基準と案）: 東山マップから伏見稲荷〜三十三間堂を分け、高瀬川ぞいの銭湯とビールを足した。
  出発は京都の中心・三条のあたり。時刻と運賃は乗換案内で確認
"""
import copy, json, os, re, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_ID = "fushimi-inari"
IMG = f"{R}/images/{MAP_ID}"
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


def link(kind, ja, en, url):
    return {"kind": kind, "label": T(ja, en), "url": {"ja": url, "en": url}}


def row(kind, ja, en, until=None, frm=None):
    return {"kind": kind, "text": T(ja, en), "until": until, "from": frm}


def notice(head_ja, head_en, ja, en, url=None, frm=None, to=None):
    return {"from": frm, "to": to, "url": url, "head": T(head_ja, head_en), "text": T(ja, en)}


AUTUMN_END = "2026-12-06"   # 東福寺の、2026年秋の特別期間の最終日。過ぎると秋だけの行と注意書きは自動で消える


def info(rows, source, tip=None, verified=True, checked=CHECKED):
    d = {"rows": rows, "cash": False, "tip": tip, "checked": checked, "source": source}
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


# ---------------------------------------------------------------------------
# スポットごとの、コースで変わらない内容
# ---------------------------------------------------------------------------
BASE = dict(
    station=dict(
        name=T("伏見稲荷の駅（京阪・JR）", "Fushimi Inari stations (Keihan & JR)"), kind=T("駅", "Station"),
        blurb=T("三条からは京阪電車で乗り換えなしの約10分。京都駅からはJR奈良線で約5分です。",
                "About 10 minutes direct from Sanjo on the Keihan line, or about 5 minutes from Kyoto Station on the JR Nara Line."),
        lat=34.96717, lng=135.76926,
        body=T("伏見稲荷の駅（京阪 伏見稲荷駅・JR稲荷駅）\n\n京都の中心（三条・祇園四条）から行くなら、京阪電車が乗り換えなしで楽です。伏見稲荷駅で降りて、東へ歩いて約5分で大鳥居の前に着きます。\n\n京都駅からはJR奈良線の各駅停車で2駅、約5分。朱色に塗られた小さなJR稲荷駅を出ると、目の前が大鳥居です（写真はJR稲荷駅）。",
               "Fushimi Inari stations (Keihan Fushimi-Inari and JR Inari)\n\nFrom central Kyoto (Sanjo or Gion-Shijo), the Keihan line is the easy way: no changes. Get off at Fushimi-Inari and walk east for about 5 minutes to the great torii.\n\nFrom Kyoto Station it’s two stops, about 5 minutes, on a JR Nara Line local train. The little vermilion JR Inari Station opens right onto the torii (the photos show JR Inari Station)."),
        gmaps=[gm("京阪 伏見稲荷駅", "Keihan Fushimi-Inari Station", 34.96717, 135.76926, "京阪 伏見稲荷駅"),
               gm("JR稲荷駅", "JR Inari Station", 34.96717, 135.76926, "JR稲荷駅")],
        links=[link("timetable", "京阪電車（時刻表・運賃）", "Keihan Railway timetables", "https://www.keihan.co.jp/traffic/"),
               link("timetable", "JRおでかけネット（時刻表）", "JR West timetables (Japanese)", "https://www.jr-odekake.net/")],
        info=info([row("train", "京阪 三条→伏見稲荷 約10分・240円（乗り換えなし）。三条発は5:04・5:24・5:46（平日も土曜も同じ）", "Keihan, Sanjo → Fushimi-Inari: about 10 min, ¥240, no changes. First trains leave Sanjo at 5:04, 5:24 and 5:46 (weekdays and Saturdays alike)"),
                   row("train", "JR奈良線 京都→稲荷 約5分・150円", "JR Nara Line, Kyoto → Inari: about 5 min, ¥150")],
                  "京阪の時刻・運賃は乗換案内（2026-11-24 火曜と11-28 土曜の時刻で検索）。駅からの徒歩は伏見稲荷大社の公式サイト（交通アクセス）。JRの運賃は2026-11-20に乗換案内で確認",
                  tip=T("時刻と運賃は乗換案内で調べました（2026年11月の平日と土曜）。ダイヤは変わるので、前の晩に確かめてください。", "Times and fares are from a route planner (a weekday and a Saturday in November 2026). Timetables change, so check the night before."))),
    inari=dict(
        name=T("伏見稲荷大社", "Fushimi Inari Taisha"), kind=T("神社", "Shrine"),
        blurb=T("朱色の鳥居がすき間なく続く「千本鳥居」。入口に6:00に着けばまだ人が少なく、6:30にはもう多くなっています。",
                "The vermilion tunnels of the Thousand Torii. At the entrance by 6:00 it’s still quiet; by 6:30 the crowds are already building."),
        lat=34.96714, lng=135.77267,
        body=T("伏見稲荷大社（ふしみいなりたいしゃ）\n\n全国の稲荷神社の総本宮。楼門と本殿にお参りしたら、奥へ進んで千本鳥居へ。奉納された鳥居がすき間なく並び、朱色のトンネルが山の上まで続きます。あちこちにいるキツネの像は神さまのお使いで、口に鍵や玉をくわえています。\n\nどこまで上るかで、時間が大きく変わります。千本鳥居を抜けた奥社奉拝所（おくしゃほうはいしょ）で引き返すと、本殿から往復で30〜40分。京都の町が見える四ツ辻（よつつじ）まで上ると、往復で1時間半くらい。山頂を回って戻ると2時間ほどです。四ツ辻から上は石段が続くので、歩きやすい靴で。\n\n境内は自由にお参りできます（拝観料はありません）。\n\n鳥居の道から下りてきたあたりに、カフェの「Vermillion - cafe.」があります（深草開土口町5-31）。お店のインスタグラムでは8:30〜15:00（ラストオーダー14:30、ブランチは13:30まで）。定休日は書かれていないので、行く前にお店のSNSで確かめてください（要確認）。",
               "Fushimi Inari Taisha\n\nThe head shrine of all the Inari shrines in Japan. After the gate and the main hall, keep going to the Thousand Torii: donated gates set so close together that they make vermilion tunnels all the way up the hill. The fox statues are the god’s messengers, holding keys or jewels in their mouths.\n\nHow far you climb changes the time a lot. Turning back at the Okusha worship hall, just past the Thousand Torii, is 30–40 minutes there and back from the main hall. Up to Yotsutsuji, where the city comes into view, is about an hour and a half. The full loop over the summit is about two hours. Above Yotsutsuji it’s steps all the way, so wear proper shoes.\n\nThe grounds are free to enter.\n\nNear where the torii path comes back down is the café Vermillion - cafe. (5-31 Fukakusa Kaidoguchi-cho). Its Instagram gives 8:30–15:00 (last order 14:30; brunch until 13:30). Closing days aren’t listed, so check the café’s social media before you go (unconfirmed)."),
        gmaps=[gm("伏見稲荷大社", "Fushimi Inari Taisha", 34.96714, 135.77267, "伏見稲荷大社"),
               gm("Vermillion - cafe.", "Vermillion - cafe.", 34.96842, 135.77415, "Vermillion - cafe. 京都市伏見区深草開土口町5-31")],
        links=[link("official", "伏見稲荷大社 公式サイト", "Fushimi Inari Taisha (official)", "https://inari.jp/"),
               link("info", "ご参拝の皆様へ（境内の決まり）", "Rules for visitors (Japanese)", "https://inari.jp/request/"),
               link("official", "Vermillion（カフェ）公式サイト", "Vermillion café (official)", "https://www.vermillioncafe.com/")],
        info=info([row("fee", "伏見稲荷大社：無料", "Fushimi Inari Taisha: free"),
                   row("hours", "Vermillion - cafe.：8:30〜15:00（ラストオーダー14:30、ブランチは13:30まで）。お店のインスタグラムより。定休日と支払い方法は書かれていません（要確認）", "Vermillion - cafe.: 8:30–15:00 (last order 14:30; brunch until 13:30), per the café’s Instagram. Closing days and payment are not listed (unconfirmed)"),
                   row("hours", "早朝・夜に入れる時間は、公式サイトに書かれていません（要確認）。6:00ごろには入口から歩けました", "The official site doesn’t state early-morning or night hours (unconfirmed). It was possible to walk in from the entrance at about 6:00")],
                  "伏見稲荷大社 公式サイト（交通アクセス、ご参拝の皆様へ。2026-11-23 に早朝・夜の参拝時間の記載がないことを FAQ https://inari.jp/faq/ でも確かめ直した）。Vermillion - cafe. の住所は公式サイトのアクセスのページ（https://www.vermillioncafe.com/access）、営業時間はお店の公式インスタグラム（https://www.instagram.com/vermillion_cafe/ のプロフィール「8:30 - 15:00 (14:30 LO) Brunch(13:30 LO)」、2026-11-23 確認。最新はGoogleマップで、と書かれている）。定休日・支払い方法は記載なしで未確認。位置はオーナーが教えてくれた Googleマップの位置。早朝の混み方はオーナーの体験（6:00はまだ少なく、6:30には多い）。稲荷山の所要時間は公式サイトに記載がなく、目安",
                  tip=T("混み方はこのマップを作ったToshiの体験です。稲荷山を歩く時間は目安で、公式サイトには書かれていません。", "The crowd notes are the experience of Toshi, who made this map. Walking times on the hill are estimates; the official site doesn’t give them."), verified=False, checked="2026-11-23"),
        caution=T("食べ歩きはできません（飲食は無料休憩所だけ）", "No eating while walking (only in the free rest house)"),
        notices=[notice("境内で食べられるのは無料休憩所だけ", "Eat only in the free rest house",
                        "食べ歩き・立ち食いは禁止です（公式サイトの決まり）。ペットを連れての参拝、ドローン、細い参道で立ち止まって通行をふさぐ撮影もできません。",
                        "Eating while walking or standing is not allowed (official rule). No pets, no drones, and don’t block the narrow path to take photos.",
                        url="https://inari.jp/request/")]),
    tofukuji=dict(
        name=T("東福寺", "Tofuku-ji Temple"), kind=T("お寺", "Temple"),
        blurb=T("谷を埋めるもみじを、木の橋「通天橋」から見下ろします。開門は9:00（秋の通天橋は8:30）。",
                "Look down from the wooden Tsutenkyo bridge onto a valley of maples. Opens at 9:00 (the bridge from 8:30 in autumn)."),
        lat=34.97677, lng=135.77371,
        body=T("東福寺（とうふくじ）\n\n大きな禅寺で、境内の谷にかかる通天橋（つうてんきょう）から、もみじの谷を見下ろせます。秋は谷じゅうが赤くなり、新緑のころは一面の緑です。\n\n通天橋・開山堂と、本坊庭園（方丈の庭）は券が別です。秋の見ごろ（11月中ごろ〜12月はじめ）はとても混みます。\n\n境内の南には、塔頭（たっちゅう）の光明院（こうみょういん）があります。重森三玲がつくった苔と砂の庭「波心庭（はしんてい）」の寺で、拝観は朝7時ごろから日没ごろまで（季節で変わります）、拝観料500円です（公式サイト）。",
               "Tofuku-ji Temple\n\nA large Zen temple. From the Tsutenkyo bridge across the ravine in its grounds you look down on a valley of maples: all red in autumn, all green in early summer.\n\nThe bridge (with Kaisando hall) and the Hojo garden have separate tickets. It gets very crowded at the autumn peak (mid-November to early December).\n\nSouth of the main grounds is the sub-temple Komyo-in, with Hashin-tei, a garden of moss and sand by Mirei Shigemori. It is open from about 7:00 until about sunset (varying with the season), and admission is ¥500 (official site)."),
        gmaps=[gm("東福寺", "Tofuku-ji", 34.97677, 135.77371, "東福寺 通天橋")],
        links=[link("official", "東福寺 公式サイト（拝観案内）", "Tofuku-ji (official, Japanese)", "https://tofukuji.jp/guide/"),
               link("official", "光明院 公式サイト", "Komyo-in (official, Japanese)", "https://komyoin.jp/")],
        info=info([row("hours", "秋（11月14日〜12月6日）：通天橋 8:30〜16:00、本坊庭園 9:00〜16:00（16:30閉門）", "Autumn (14 Nov – 6 Dec): Tsutenkyo 8:30–16:00, Hojo garden 9:00–16:00 (gates close 16:30)", until=AUTUMN_END),
                   row("fee", "秋（2026年11月14日〜12月6日）：通天橋・開山堂 大人1,000円、本坊庭園 大人600円。共通券はありません", "Autumn (14 Nov – 6 Dec 2026): Tsutenkyo & Kaisando ¥1,000, Hojo garden ¥600 per adult. No combined ticket", until=AUTUMN_END),
                   row("hours", "4月1日〜11月13日 9:00〜16:00（16:30閉門）、12月7日〜3月31日 9:00〜15:30（16:00閉門）", "1 Apr – 13 Nov: 9:00–16:00 (gates close 16:30). 7 Dec – 31 Mar: 9:00–15:30 (close 16:00)"),
                   row("fee", "秋以外：通天橋・開山堂 大人600円、本坊庭園 大人600円、共通券 大人1,000円", "Outside autumn: Tsutenkyo & Kaisando ¥600, Hojo garden ¥600, combined ticket ¥1,000 per adult"),
                   row("hours", "光明院：通年 朝7時ごろ〜日没ごろ（季節で変わる）、拝観料500円", "Komyo-in: all year, from about 7:00 to about sunset (varies with the season); ¥500"),
                   row("train", "京阪・JR 東福寺駅から歩いて約10分", "About 10 min on foot from Tofukuji Station (Keihan / JR)")],
                  "東福寺 公式サイト（拝観案内）。秋の通天橋の料金は2026-11-20の確認。光明院は公式サイト https://komyoin.jp/ のページ下の「拝観時間／通年 午前7時ごろ〜日没ごろ迄（季節により変動）」「拝観料 500円」（2026-11-23 確認）。駅からの徒歩は地図で測った目安"),
        notices=[notice("秋は橋の上で写真を撮れないことがあります", "In autumn, photos on the bridges may be stopped",
                        "11月14日〜12月6日はとても混むので、通天橋と臥雲橋の上での撮影を遠慮するよう案内されることがあります（公式サイト）。この期間は共通券もありません。",
                        "From 14 November to 6 December it is so busy that you may be asked not to take photos on the Tsutenkyo and Gaunkyo bridges (official site). There is no combined ticket in this period either.",
                        url="https://tofukuji.jp/guide/", to=AUTUMN_END)]),
    sennyuji=dict(
        name=T("泉涌寺と雲龍院", "Sennyu-ji and Unryu-in"), kind=T("お寺", "Temple"),
        blurb=T("皇室とゆかりの深い「御寺（みてら）」。奥の雲龍院では、丸い窓から庭を眺めます。雲龍院は水曜休み（11月を除く）。",
                "The “Mitera”, a temple tied to the imperial family. At Unryu-in, further in, you view the garden through a round window. Unryu-in is closed on Wednesdays (except in November)."),
        lat=34.97810, lng=135.78010,
        body=T("泉涌寺（せんにゅうじ）と雲龍院（うんりゅういん）\n\n歴代の天皇のお墓がある、皇室の菩提寺です。大門をくぐると、仏殿へ向かって参道が下っていきます。木に囲まれた境内は、東山の中では人が少なく、静かです。\n\n奥にある別院の雲龍院では、「悟りの窓」と呼ばれる丸い窓や、障子の四角い窓ごしに庭を眺められます。拝観料は泉涌寺とは別です。\n\n参道の途中から少し入ると、朱色の橋の先に今熊野観音寺（いまくまのかんのんじ）もあります。",
               "Sennyu-ji and Unryu-in\n\nThe family temple of the imperial household, where generations of emperors are buried. From the main gate the approach slopes down to the Buddha hall. The wooded grounds are quiet, with far fewer people than the rest of Higashiyama.\n\nAt the sub-temple Unryu-in, further in, you look at the garden through the round “Window of Enlightenment” and square paper-screen windows. It has its own admission.\n\nJust off the approach, across a vermilion bridge, is Imakumano Kannon-ji."),
        gmaps=[gm("泉涌寺", "Sennyu-ji", 34.97810, 135.78010, "泉涌寺"), gm("雲龍院", "Unryu-in", 34.97727, 135.78040, "泉涌寺 雲龍院")],
        links=[link("official", "御寺 泉涌寺（拝観のご案内）", "Sennyu-ji (official, Japanese)", "https://www.mitera.org/guide/"),
               link("official", "泉涌寺別院 雲龍院（参拝ご案内）", "Unryu-in (official, Japanese)", "https://www.unryuin.jp/worship")],
        info=info([row("hours", "泉涌寺 3〜11月 9:00〜16:30（17:00閉門）、12〜2月 9:00〜16:00（16:30閉門）", "Sennyu-ji: Mar–Nov 9:00–16:30 (gates close 17:00); Dec–Feb 9:00–16:00 (close 16:30)"),
                   row("fee", "泉涌寺 伽藍拝観 大人500円・小中学生300円", "Sennyu-ji: ¥500 adults, ¥300 elementary/junior high"),
                   row("hours", "雲龍院 9:00〜17:00（受付16:30まで）", "Unryu-in: 9:00–17:00 (last entry 16:30)"),
                   row("closed", "雲龍院は水曜休み（11月を除く）。行事で休む日もあり、公式サイトのお知らせに出ます", "Unryu-in: closed Wednesdays (except November), plus some event days announced on its website"),
                   row("fee", "雲龍院 400円（泉涌寺とは別）", "Unryu-in: ¥400 (separate from Sennyu-ji)")],
                  "御寺 泉涌寺 公式サイト（拝観のご案内）、雲龍院 公式サイト（参拝ご案内）"),
        caution=T("雲龍院は水曜休み（11月を除く）", "Unryu-in closed Wednesdays (except November)"),
        notices=[notice("建物の中は撮影できません", "No photos inside the buildings",
                        "泉涌寺の建物の中は、写真・ビデオとも撮影禁止です（公式サイト）。雲龍院は水曜が休みです（11月を除く）。",
                        "Photos and video are not allowed inside Sennyu-ji’s buildings (official site). Unryu-in is closed on Wednesdays (except in November).",
                        url="https://www.mitera.org/guide/")]),
    # 三十三間堂は Toshi がまだ行っていない場所。文章は公式サイトの情報だけで書き、写真は Wikimedia Commons（_extra）。2026-11-21 追加
    # 三十三間堂は寺が画像の利用に許可を求めているので、公道（七条通）から撮った外観の写真だけ（CC0）
    sanjusangendo=dict(
        name=T("三十三間堂", "Sanjusangen-do"), kind=T("お寺", "Temple"),
        blurb=T("長さ約120mのお堂に、1,001体の千手観音が並びます。堂内は撮影できません。",
                "A hall about 120 m long holding 1,001 statues of the thousand-armed Kannon. No photos inside."),
        lat=34.98817, lng=135.77178,
        body=T("三十三間堂（さんじゅうさんげんどう）\n\n正式な名前は蓮華王院（れんげおういん）。南北に約120mある本堂（国宝）の中に、千手観音の立像が1,001体、段になって並んでいます。柱と柱の間が33あるので「三十三間堂」。観音像の前には風神・雷神と二十八部衆の像も立ち、すべて国宝です（公式サイトより）。\n\n靴を脱いで上がるので、脱ぎやすい靴が楽です。",
               "Sanjusangen-do\n\nOfficially Rengeo-in. Inside the main hall, a National Treasure about 120 m long from north to south, 1,001 standing statues of the thousand-armed Kannon are lined up in tiers. The name means “hall of 33 bays”, the spaces between its pillars. Statues of the Wind and Thunder Gods and 28 guardian deities stand in front, all National Treasures (from the official website).\n\nYou take your shoes off, so wear ones that slip on and off."),
        gmaps=[gm("三十三間堂", "Sanjusangen-do", 34.98817, 135.77178, "三十三間堂")],
        links=[link("official", "三十三間堂 公式サイト（拝観）", "Sanjusangen-do (official, Japanese)", "https://www.sanjusangendo.jp/visit/")],
        info=info([row("hours", "4月1日〜11月15日 8:30〜17:00、11月16日〜3月31日 9:00〜16:00（受付は30分前まで）。年中無休", "1 Apr – 15 Nov 8:30–17:00; 16 Nov – 31 Mar 9:00–16:00 (last entry 30 min before). Open every day"),
                   row("fee", "一般600円、中高生400円、小学生300円", "¥600 adults, ¥400 junior/senior high, ¥300 elementary"),
                   row("train", "京阪 七条駅から歩いて約7分。市バス「博物館三十三間堂前」すぐ", "7 min on foot from Keihan Shichijo Station. City bus stop “Hakubutsukan-Sanjusangendo-mae” is right outside")],
                  "三十三間堂 公式サイト（拝観 https://www.sanjusangendo.jp/visit/ と お知らせ「拝観時間変更のお知らせ」https://www.sanjusangendo.jp/news/1717/ ：令和8年11月16日〜令和9年3月31日は開門9:00・閉門16:00・受付15:30まで。夜間拝観は今年度なし）。2026-11-23 に確認。料金・年中無休・七条駅2番出口から徒歩約7分・バス停「博物館三十三間堂前」下車すぐも同じページ。堂内の撮影禁止は公式サイトの文には見当たらない（画像の利用は許可制と「画像の使用撮影について」に書かれている）", checked="2026-11-23"),
        caution=T("堂内は撮影禁止", "No photos inside"),
        notices=[notice("堂内は撮影できません", "No photos inside the hall",
                        "11月16日〜3月31日は受付が15:30までと早く閉まります。",
                        "From 16 November to 31 March last entry is as early as 15:30.",
                        url="https://www.sanjusangendo.jp/visit/")],
        _extra=[cc("sanjusangendo-1.jpg", "TKdows 2026", "CC0", "File:JP 日本 Japan 京都 Kyoto 七條通 Shichijo Dori Street tourism 三十三間堂 Sanjūsangen-dō Temples June 2026 N13P 07.jpg"),
                cc("sanjusangendo-2.jpg", "TKdows 2026", "CC0", "File:JP 日本 Japan 京都 Kyoto 七條通 Shichijo Dori Street tourism 三十三間堂 Sanjūsangen-dō Temples June 2026 N13P 40.jpg")]),
    umeyu=dict(
        name=T("サウナの梅湯", "Sauna no Umeyu (public bath)"), kind=T("銭湯", "Public bath"),
        blurb=T("高瀬川のほとりの銭湯。朝6:00から深夜2:00まで、木曜休み。大人550円、支払いは現金かPayPay。",
                "A neighbourhood bathhouse beside the Takase River. Open 6:00 to 2:00 at night, closed Thursdays. ¥550, cash or PayPay."),
        lat=34.99295, lng=135.76566,
        body=T("サウナの梅湯（うめゆ）\n\n高瀬川のほとりに建つ銭湯です。夜は「サウナの梅湯」の赤・黄・緑のネオンがつきます。歩いたあとの汗を流して、ひと休みするのにちょうどいい場所です。\n\nシャンプーとボディソープ、ドライヤーは備え付け。タオルは借りられます（フェイスタオル100円、バスタオルとのセット350円）。浴室にドライサウナがあり、入浴料だけで入れます。\n\n入れ墨・タトゥーの扱いは、公式サイトに書かれていません（要確認）。心配な人は、受付で聞いてから入ってください。お酒を飲んだあとは入れないので、ビールは銭湯のあとに。",
               "Sauna no Umeyu\n\nA public bathhouse on the bank of the Takase River. At night its red, yellow and green “Sauna no Umeyu” neon sign is lit. It’s a good place to wash off the day’s walking and rest.\n\nShampoo, body soap and hair dryers are provided. Towels can be rented (face towel ¥100, set with bath towel ¥350). There is a dry sauna in the bathing area, included in the bath fee.\n\nThe official website says nothing about tattoos (unconfirmed). If you’re unsure, ask at the front desk before you go in. You can’t bathe after drinking, so save the beer for afterwards."),
        gmaps=[gm("サウナの梅湯", "Sauna no Umeyu", 34.99295, 135.76566, "サウナの梅湯")],
        links=[link("official", "サウナの梅湯（ゆとなみ社）", "Sauna no Umeyu (operator’s site, Japanese)", "https://yutonamisha.com/sento/umeyu/")],
        info={"rows": [row("hours", "6:00〜26:00（深夜2:00）", "6:00–26:00 (2:00 at night)"),
                       row("closed", "木曜", "Thursdays"),
                       row("fee", "大人550円、中学生400円（生徒手帳などを見せた場合）、小学生200円。サウナも入浴料だけで入れます。貸しタオル：フェイスタオル100円、バスタオルとのセット350円", "¥550 adults, ¥400 junior high (with a student ID), ¥200 elementary. The sauna is included in the bath fee. Towel rental: face towel ¥100, set with bath towel ¥350"),
                       row("fee", "2027年3月31日までは、18歳以上の大人と一緒なら小学生以下は無料（京都府の事業。受付でQRコードから手続き）", "Until 31 March 2027, children up to elementary age are free with an adult aged 18+ (a Kyoto Prefecture scheme; register via a QR code at the counter)", until="2027-03-31"),
                       row("fee", "支払いは現金かPayPay", "Pay in cash or with PayPay"),
                       row("hours", "タトゥーがあっても入れます。最終受付は公式サイトに記載がありません（要確認）", "Tattoos are fine. Last entry is not stated on the official site (unconfirmed)"),
                       row("train", "京阪 清水五条駅から歩いて約10分、JR京都駅から約15分", "About 10 min on foot from Keihan Kiyomizu-Gojo Station, about 15 from JR Kyoto Station")],
              "cash": True, "tip": None, "checked": "2026-11-23", "verified": False,
              "source": "サウナが入浴料に含まれること・タトゥーがあっても入れることは、オーナーが実際に入った経験（2026-11-24 確認）。ゆとなみ社 公式サイトの梅湯のページ https://yutonamisha.com/sento/umeyu/（営業時間・定休日・料金・支払い「現金、paypay対応」・貸しタオル・アクセス。「お風呂の種類」にドライサウナ）。京都府浴場組合 https://1010.kyoto/spot/umeyu1/（梅湯は組合の銭湯。6:00〜26:00・木曜休み）と「銭湯の利用方法」https://1010.kyoto/how_to_use/（「この料金で、その銭湯内全てのお風呂に入れます」「中学生料金400円 身分証（生徒手帳等）提出の場合」「酔っている人は入れません」）。小学生以下の無料は京都府「子どもの入浴料金無料化事業」https://www.pref.kyoto.jp/seikatsu/nyuyokumuryo_kodomo.html（令和8年4月1日〜令和9年3月31日、組合加入の銭湯、大人18歳以上の同伴、QRコードで手続き）。以上 2026-11-23 確認。オーナーが撮った店頭の案内（2025-09-17）も「6:00〜26:00 定休日 木曜日」。タトゥーと最終受付は、ゆとなみ社のページ・「入浴のお約束」・組合のページのどれにも記載がなく未確認。位置は OpenStreetMap"},
        caution=T("木曜休み。現金かPayPay", "Closed Thursdays. Cash or PayPay"),
        notices=[notice("木曜は休み。支払いは現金かPayPay", "Closed Thursdays. Cash or PayPay only",
                        "クレジットカードは公式サイトの支払い方法に載っていません。タオルは借りられるので、手ぶらで入れます。お酒を飲んだあとは入れません。",
                        "Credit cards are not among the payment methods on the official site. Towels can be rented, so you can come empty-handed. You can’t bathe after drinking.",
                        url="https://yutonamisha.com/sento/umeyu/")]),
    beerlab=dict(
        name=T("Kyoto Beer Lab 本店", "Kyoto Beer Lab (main pub)"), kind=T("クラフトビール", "Craft beer"),
        blurb=T("高瀬川ぞいの小さなブリューパブ。13:00から23:00まで。梅湯から歩いてすぐです。",
                "A small brewpub on the Takase River, open 13:00–23:00, a short walk from Umeyu."),
        lat=34.99067, lng=135.76558,
        body=T("Kyoto Beer Lab（京都ビアラボ）本店\n\n2018年に高瀬川のほとりで始まったブリューパブで、店の中でビールを造っています。本店でしか飲めないビールもあります（公式サイトより）。店内のモニターに、その日つながっているビールの一覧が出ます。\n\n定休日と支払い方法は、公式サイトでは確かめられませんでした（要確認）。\n\n飲んだあとは、高瀬川に沿って北へ。五条通を渡ると木屋町通に入り、四条を過ぎて三条まで、川ぞいにお店が続きます。鴨川へ出て、河原を歩いて戻ることもできます。三条まで歩いて35〜40分です。",
               "Kyoto Beer Lab (main pub)\n\nA brewpub that opened beside the Takase River in 2018 and brews on the premises; some beers are only poured here (from the official website). A screen inside lists what’s on tap that day.\n\nClosing days and payment methods could not be confirmed on the official website (unconfirmed).\n\nAfterwards, follow the Takase River north. Across Gojo-dori you’re on Kiyamachi-dori, lined with places to eat and drink past Shijo all the way to Sanjo. Or cut across to the Kamo River and walk back along the bank. It’s 35–40 minutes on foot to Sanjo."),
        gmaps=[gm("Kyoto Beer Lab 本店", "Kyoto Beer Lab", 34.99067, 135.76558, "Kyoto Beer Lab 京都市下京区十禅師町201-3")],
        links=[link("official", "Kyoto Beer Lab 公式サイト", "Kyoto Beer Lab (official)", "https://kyotobeerlab.jp/")],
        info={"rows": [row("hours", "13:00〜23:00", "13:00–23:00"),
                       row("closed", "定休日は公式サイトに記載がありません（要確認）", "Closing days are not stated on the official site (unconfirmed)"),
                       row("fee", "値段と支払い方法は公式サイトで確かめられませんでした（要確認）", "Prices and payment methods could not be confirmed on the official site (unconfirmed)")],
              "cash": False, "tip": None, "checked": "2026-11-23", "verified": False,
              "source": "Kyoto Beer Lab 公式サイト https://kyotobeerlab.jp/ の Shop（本店の住所：下京区十禅師町201-3、営業時間 13:00〜23:00。2026-11-23 確認）。公式サイトの予約ボタン（TableCheck）は2号店 KBL THE GARAGE のもので、本店の予約の案内はない。定休日・値段・支払い方法は公式サイト（トップ・About・News）に記載がなく未確認。公式インスタグラムはログインしないと見られない。位置はオーナーの写真の位置情報。三条まで歩く時間は地図で測った目安"}),

)

VIS, ARR = ("おすすめ訪問時間", "Recommended visit time"), ("おすすめ到着時間", "Recommended arrival time")

DARK_AT_SIX = notice("11月〜2月の朝6時はまだ暗い", "At 6:00 it is still dark from November to February",
                     "この時期の日の出は6時すぎ〜7時すぎです。暗い道や石段では足もとに気をつけて。写真が目当ての日は、明るくなる時間も考えて出発を決めてください。",
                     "Sunrise in these months is between just after 6:00 and just after 7:00. Watch your step on dark lanes and stone steps. If you’re here for photos, plan your start around the light.",
                     frm="2026-11-01", to="2027-02-28")

# ---------------------------------------------------------------------------
# コースごとの並び順・時間・行き方
#   order の1件 = (スポットの id, 時間の見出し, 時間（日本語）, 時間（英語）, このコースでの行き方・過ごし方)
# ---------------------------------------------------------------------------
BREAKFAST_J = "朝ごはんは、京阪で三条へ戻って（約10分・240円）、7:00から開いているイノダコーヒ本店へ（三条駅から歩いて約15分、烏丸御池駅から約5分。予約はできません）。ひと休みしたら、9:20ごろの電車で東福寺へ向かいます。\n\n戻らずに続けたい日は、朝ごはんを前の晩に買って持っていってください。東福寺が開くのは9:00です。"
BREAKFAST_E = "For breakfast, ride the Keihan back to Sanjo (about 10 min, ¥240) and go to Inoda Coffee’s main shop, open from 7:00 (about 15 minutes on foot from Sanjo Station, 5 from Karasuma Oike; no reservations). After a rest, take a train at about 9:20 to Tofuku-ji.\n\nIf you’d rather not go back, buy breakfast the night before and bring it. Tofuku-ji doesn’t open until 9:00."
SECTIONS = [dict(first="station", last="inari", day=0), dict(first="tofukuji", last="sanjusangendo", day=2), dict(first="umeyu", last="beerlab", day=3)]
ALL = ["inari", "tofukuji", "sennyuji", "sanjusangendo", "umeyu", "beerlab"]
THU = ("umeyu", dict(any=["umeyu"], andAny=["beerlab"]), None, None,
       "梅湯は木曜が休みです。木曜は、三十三間堂からまっすぐ Kyoto Beer Lab へ（歩いて約15分）。",
       "Umeyu is closed on Thursdays. On a Thursday, walk straight from Sanjusangen-do to Kyoto Beer Lab (about 15 minutes).")

COURSES = [
    dict(
        id="late", file="fushimi-inari.json",
        note="「9〜10時に出発」コース。三条を9:15ごろの京阪で出て、伏見稲荷（9:35〜11:15、四ツ辻まで）→参道でお昼→東福寺→泉涌寺・雲龍院→三十三間堂（冬は受付15:30まで）→サウナの梅湯→Kyoto Beer Lab→高瀬川・木屋町を歩いて三条へ（19時すぎ。そのまま木屋町・先斗町で21時ごろまで）。",
        order=[
            ("station", ARR, "9:25（三条 9:15ごろ発）", "9:25 (leaving Sanjo at about 9:15)",
             T("三条駅から京阪電車の淀屋橋方面行きに乗って約10分。準急か普通に乗ってください（特急は伏見稲荷に止まりません）。",
               "About 10 minutes from Sanjo on a Keihan train bound for Yodoyabashi. Take a sub-express or local: limited expresses don’t stop at Fushimi-Inari.")),
            ("inari", VIS, "9:35〜11:15", "9:35–11:15",
             T("この時間は、もう鳥居の道が人でいっぱいです（朝6:30には、もう人が多くなります）。人の少ない千本鳥居を歩きたい日は、一覧の上のボタンで「早朝に出発」に切り替えてください。\n\n四ツ辻まで上って戻るとちょうどこの時間。お昼は、下りてきてから参道か駅のまわり、または Vermillion - cafe. で（11:15〜12:00）。境内では食べ歩きができません。",
               "By this time the torii path is already full of people (it is already busy by 6:30 in the morning). To walk the Thousand Torii with fewer people, switch to “Early start” with the buttons above the list.\n\nUp to Yotsutsuji and back fits this slot. Have lunch afterwards on the approach, around the stations, or at Vermillion - cafe. (11:15–12:00). You can’t eat while walking inside the shrine.")),
            ("tofukuji", VIS, "12:20〜13:15", "12:20–13:15",
             T("伏見稲荷から北へ歩いて約20分。電車なら京阪で伏見稲荷駅から2駅の東福寺駅で降りて、歩いて約10分です。",
               "About 20 minutes’ walk north of Fushimi Inari. By train, it’s two stops on the Keihan line from Fushimi-Inari to Tofukuji, then about 10 minutes on foot.")),
            ("sennyuji", VIS, "13:30〜14:25", "13:30–14:25",
             T("東福寺から歩いて約15分。最後は泉涌寺道の坂を上ります。",
               "About 15 minutes on foot from Tofuku-ji, ending with the climb up Sennyuji-michi.")),
            ("sanjusangendo", VIS, "14:50〜15:30", "14:50–15:30",
             T("泉涌寺から坂を下り、東大路通を北へ、七条通を西へ歩いて約25分。疲れていたら、東福寺駅まで戻って京阪で1駅の七条駅へ（駅から歩いて約7分）。",
               "About 25 minutes on foot from Sennyu-ji: down the slope, north along Higashioji-dori, then west on Shichijo-dori. If you’re tired, go back to Tofukuji Station and ride the Keihan one stop to Shichijo (about 7 minutes’ walk from there).")),
            ("umeyu", VIS, "15:50〜17:00", "15:50–17:00",
             T("三十三間堂から七条通を西へ、鴨川を渡って高瀬川に出たら、川に沿って北へ。歩いて約15分です。",
               "From Sanjusangen-do walk west on Shichijo-dori, cross the Kamo River to the Takase River, then follow it north: about 15 minutes.")),
            ("beerlab", VIS, "17:10〜18:30", "17:10–18:30",
             T("梅湯から高瀬川に沿って南へ、歩いて約5分。\n\n18:30に出て北へ歩くと、三条に19時すぎ。途中の木屋町や先斗町（ぽんとちょう）で晩ごはんにすれば、21時ごろまで過ごせます。",
               "About 5 minutes’ walk south along the Takase River from Umeyu.\n\nLeave at 18:30 and walk north to reach Sanjo soon after 19:00. Stop for dinner in Kiyamachi or Pontocho on the way and the evening runs to about 21:00.")),
        ],
        sections=SECTIONS, default=ALL, auto=["station"],
        extra_notices={"sanjusangendo": [notice("冬は受付が15:30まで", "In winter, last entry is 15:30",
                                                 "11月16日〜3月31日は16:00に閉まり、受付は15:30までです。このコースでは14:50に着くので、泉涌寺を14:25までに出てください。",
                                                 "From 16 November to 31 March it closes at 16:00, with last entry at 15:30. This course arrives at 14:50, so leave Sennyu-ji by 14:25.",
                                                 frm="2026-11-16", to="2027-03-31")]},
        hints=[THU,
               ("sanjusangendo", dict(any=["sanjusangendo"], none=["sennyuji"]), None, None,
                "泉涌寺に寄らない日は、東福寺駅から京阪電車で七条駅へ1駅。駅から歩いて約7分です。",
                "Skipping Sennyu-ji? Ride the Keihan line one stop from Tofukuji to Shichijo, then walk about 7 minutes.")]),
    dict(
        id="early", file="fushimi-inari-early.json",
        note="「早朝に出発」コース。三条5:24発の京阪で伏見稲荷へ（5:34着、入口に5:40。5:46発なら入口に6:00）。7:30ごろまで歩いたら、京阪で三条へ戻って朝ごはん（イノダコーヒ本店 7:00〜）と休憩。9:21ごろの京阪で東福寺へ、泉涌寺・雲龍院、三十三間堂、（お昼）、サウナの梅湯、Kyoto Beer Lab（13:00〜）、高瀬川・木屋町を歩いて三条へ（17時半ごろ）。伏見稲荷のまわりで早朝に開いている朝ごはんの店は、公式サイトで確かめられなかったので店名を出していない。",
        order=[
            ("station", ARR, "5:34（三条 5:24発）", "5:34 (the 5:24 from Sanjo)",
             T("三条駅5:24発の京阪電車に乗ると、5:34に伏見稲荷駅に着き、5:40ごろ大鳥居の前に立てます。次の5:46発だと5:56着で、入口にちょうど6:00。その次の電車では、入口に着くのが6時を過ぎます。",
               "The 5:24 Keihan train from Sanjo reaches Fushimi-Inari at 5:34, putting you in front of the great torii at about 5:40. The next one, at 5:46, arrives at 5:56: at the entrance right on 6:00. With any later train you reach the entrance after six.")),
            ("inari", VIS, "5:40〜7:30", "5:40–7:30",
             T("入口に6:00に着けばまだ人は少なく、6:30にはもう増えています。先に千本鳥居へ行き、四ツ辻まで上ってから、帰りに本殿へお参りすると、鳥居の道を人の少ないうちに歩けます。\n\n下りてきたら7:30ごろ。" + BREAKFAST_J,
               "At the entrance by 6:00 there are still few people; by 6:30 the crowds are already building. Go to the Thousand Torii first, climb to Yotsutsuji, and pray at the main hall on the way back: that way you walk the torii path before it fills up.\n\nYou’ll be down at about 7:30. " + BREAKFAST_E)),
            ("tofukuji", VIS, "9:40〜10:40", "9:40–10:40",
             T("三条駅から京阪電車で東福寺駅へ（約6分・240円。9:21発で9:27着）、駅から歩いて約10分。伏見稲荷から直接来るなら、歩いて約20分です。",
               "Take the Keihan line from Sanjo to Tofukuji (about 6 min, ¥240; the 9:21 arrives at 9:27), then walk about 10 minutes. Coming straight from Fushimi Inari, it’s about 20 minutes on foot.")),
            ("sennyuji", VIS, "10:55〜11:55", "10:55–11:55",
             T("東福寺から歩いて約15分。最後は泉涌寺道の坂を上ります。",
               "About 15 minutes on foot from Tofuku-ji, ending with the climb up Sennyuji-michi.")),
            ("sanjusangendo", VIS, "12:20〜13:00", "12:20–13:00",
             T("泉涌寺から坂を下り、東大路通を北へ、七条通を西へ歩いて約25分。疲れていたら、東福寺駅まで戻って京阪で1駅の七条駅へ（駅から歩いて約7分）。\n\nお昼は見終わってから、七条通のあたりで（13:00〜13:50）。",
               "About 25 minutes on foot from Sennyu-ji: down the slope, north along Higashioji-dori, then west on Shichijo-dori. If you’re tired, go back to Tofukuji Station and ride the Keihan one stop to Shichijo (about 7 minutes’ walk from there).\n\nHave lunch afterwards around Shichijo-dori (13:00–13:50).")),
            ("umeyu", VIS, "14:05〜15:20", "14:05–15:20",
             T("七条通を西へ、鴨川を渡って高瀬川に出たら、川に沿って北へ。三十三間堂から歩いて約15分です。朝5時台から歩いた日なので、ここでゆっくり。",
               "Walk west on Shichijo-dori, cross the Kamo River to the Takase River, then follow it north: about 15 minutes from Sanjusangen-do. You’ve been on your feet since before six, so take your time here.")),
            ("beerlab", VIS, "15:30〜17:00", "15:30–17:00",
             T("梅湯から高瀬川に沿って南へ、歩いて約5分。\n\n17:00に出て北へ歩くと、三条に17時半すぎ。早起きした日なので、ここで終わりにしても十分です。まだ元気なら、木屋町や先斗町（ぽんとちょう）で晩ごはんを。",
               "About 5 minutes’ walk south along the Takase River from Umeyu.\n\nLeave at 17:00 and walk north to reach Sanjo a little after 17:30. After such an early start, that’s a full day. If you still have energy, have dinner in Kiyamachi or Pontocho.")),
        ],
        sections=SECTIONS, default=ALL, auto=["station"],
        extra_notices={"inari": [DARK_AT_SIX],
                       "tofukuji": [notice("紅葉の時期は、通天橋が8:30に開きます", "In the autumn-leaf season the bridge opens at 8:30",
                                           "11月14日〜12月6日は、伏見稲荷から三条へ戻らずに歩いて（約20分）、8:30の開門に並ぶこともできます。その日は朝ごはんを持っていってください。",
                                           "From 14 November to 6 December you can skip the trip back to Sanjo and walk straight from Fushimi Inari (about 20 minutes) to queue for the 8:30 opening. Bring breakfast with you that day.",
                                           to=AUTUMN_END)]},
        hints=[THU,
               ("sanjusangendo", dict(any=["sanjusangendo"], none=["sennyuji"]), None, None,
                "泉涌寺に寄らない日は、東福寺駅から京阪電車で七条駅へ1駅。駅から歩いて約7分です。",
                "Skipping Sennyu-ji? Ride the Keihan line one stop from Tofukuji to Shichijo, then walk about 7 minutes.")]),
]

NOTE_HEAD = "伏見稲荷から七条への1日ルート（fushimi-inari/ のページ専用。形は eizan-line.json と同じ）。一覧の上のボタンで2つのコースを切り替え、コースごとに別のファイルを読む（fushimi-inari.json＝9〜10時に出発、fushimi-inari-early.json＝早朝に出発）。このファイル："
NOTE_TAIL = " 三十三間堂は Toshi がまだ行っていない場所（写真は公道から撮った外観だけ・Wikimedia Commons の CC0。寺が境内の写真の利用に許可を求めているため）。 写真は Toshi の写真ライブラリから選んだもの（長辺1600px・位置情報なし）。info.source は確認した出典、info.checked は確認日、info.verified=false は公式サイトで確認できなかった情報がある（要確認）。入口で困ること（休み・撮影禁止・入口の場所）は caution と head つきの notices。plan.defaultPicks は最初から選ばれている場所で、各スポットの「おすすめ◯◯時間」はこの組み合わせの時間割。このファイルは scripts/build_fushimi_inari_data.py で作る（直接直さない）。"


def build(c):
    order = c["order"]
    NO = {x[0]: i for i, x in enumerate(order, 1)}
    spots = []
    for sid, (lj, le), tj, te, go in order:
        b = copy.deepcopy(BASE[sid])
        body = b.pop("body")
        text = T(body["ja"] + ("\n\n" + go["ja"] if go else "") + f"\n\n{lj}：{tj}",
                 body["en"] + ("\n\n" + go["en"] if go else "") + f"\n\n{le}: {te}")
        out = {"no": NO[sid], "id": sid}
        out.update(b)
        out["text"] = text
        out["photos"] = photos(sid, out.pop("_extra", None))
        out["notices"] = c.get("extra_notices", {}).get(sid, []) + out.get("notices", [])
        spots.append(out)
    auto = c.get("auto", [])
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
        "plan": {"_note": "「選んで回る」の設定。defaultPicks は1日で無理なく回れる組み合わせ（時間割どおり）。それ以外は時間割の外で、足したときの回り方は各スポットの文章と hints（from〜to の間だけ出る）。",
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
