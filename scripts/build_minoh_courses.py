#!/usr/bin/env python3
"""箕面マップの4つのコース（出発時間 2通り × 箕面温泉に入る/入らない）のデータを、1つの元から作る。

使い方: python3 scripts/build_minoh_courses.py
- 元: data/routes/minoh.json（手で直すのはこのファイルだけ。早めに出発・川のテラスでランチ・温泉に入る）
- 作るもの（COURSES）:
  - data/routes/minoh.json … 早めに出発＋温泉。時間を入れ直して上書き（何回実行しても同じ結果になる）
  - data/routes/minoh-noonsen.json … 早めに出発、温泉なし
  - data/routes/minoh-late.json … ゆっくり出発（10時ごろ）＋温泉。チンクエピュウは時間が合わないので外す
  - data/routes/minoh-late-noonsen.json … ゆっくり出発、温泉なし
  minoh.json 以外は直接直さない（実行のたびに作り直す）
- 時間（めやす）は TIMES、コースで変わる文章は COURSE_TEXT、コースによって足す文章は ADD
- 紹介ページ（minoh/js/i18n.js）の写真は、ここで付けるスポットの id で指定している
"""
import copy, json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = f'{R}/data/routes/minoh.json'
# (コースの id, ファイル名, 出発時間, 温泉に入るか)
COURSES = [
    ('early', 'minoh.json', 'early', True),
    ('early-noonsen', 'minoh-noonsen.json', 'early', False),
    ('late', 'minoh-late.json', 'late', True),
    ('late-noonsen', 'minoh-late-noonsen.json', 'late', False),
]

# スポットの id（名前から決める。番号はコースで変わるので、id で見分ける）
IDS = {
    '箕面萱野駅': 'kayano', '箕面萱野駅 バスのりば': 'bus', '勝尾寺': 'katsuoji', '箕面ビジターセンター': 'visitor',
    '杉の茶屋': 'sugi', '箕面大滝': 'falls', 'チンクエピュウ': 'cinque', '箕面温泉スパーガーデン': 'onsen',
    '箕面駅': 'minoh-st', 'あほや 牧落店': 'ahoya', '箕面ビール WAREHOUSE': 'beer', '牧落駅': 'makiochi',
    'ミスタードーナツ 箕面ショップ': 'misdo', '黒兵衛 箕面総本店': 'kurobee',
}
ORDER = ['kayano', 'bus', 'katsuoji', 'visitor', 'sugi', 'falls', 'cinque', 'onsen', 'minoh-st', 'misdo', 'ahoya', 'beer', 'kurobee', 'makiochi']

# めやすの時間（各スポットの文章のいちばん下の行）。(日本語の見出し, 日本語, 英語の見出し, 英語)
ARR, DEP, VIS = ('おすすめ到着時間', 'Recommended arrival time'), ('おすすめ出発時間', 'Recommended departure time'), ('おすすめ訪問時間', 'Recommended visit time')
TIMES = {
    'early': {
        'kayano': (ARR, '9:00前', 'just before 9:00'),
        'bus': (DEP, '9:00', '9:00'),
        'katsuoji': (VIS, '9:30〜11:00', '9:30–11:00'),
        'visitor': (VIS, '11:40〜12:00', '11:40–12:00'),
        'sugi': (VIS, '12:30', '12:30'),
        'falls': (VIS, '12:35〜13:10', '12:35–13:10'),
        'cinque': (VIS, '13:50〜14:50', '13:50–14:50'),
        'onsen': (VIS, '15:05〜16:45', '15:05–16:45'),
        'minoh-st': (VIS, '17:00', '17:00'),
        'misdo': (VIS, '17:05〜17:25', '17:05–17:25'),
        'ahoya': (VIS, '17:40', '17:40'),
        'beer': (VIS, '18:05〜', '18:05–'),
        'kurobee': (VIS, '19:20〜', '19:20–'),
        'makiochi': (DEP, '20:10〜', '20:10–'),
    },
    'early-noonsen': {
        'kayano': (ARR, '9:00前', 'just before 9:00'),
        'bus': (DEP, '9:00', '9:00'),
        'katsuoji': (VIS, '9:30〜11:00', '9:30–11:00'),
        'visitor': (VIS, '11:40〜12:00', '11:40–12:00'),
        'sugi': (VIS, '12:30', '12:30'),
        'falls': (VIS, '12:35〜13:10', '12:35–13:10'),
        'cinque': (VIS, '13:50〜14:50', '13:50–14:50'),
        'minoh-st': (VIS, '16:10', '16:10'),
        'misdo': (VIS, '16:15〜16:35', '16:15–16:35'),
        'ahoya': (VIS, '16:50', '16:50'),
        'beer': (VIS, '17:15〜', '17:15–'),
        'kurobee': (VIS, '18:30〜', '18:30–'),
        'makiochi': (DEP, '19:20〜', '19:20–'),
    },
    'late': {
        'kayano': (ARR, '10:30ごろ', 'about 10:30'),
        'bus': (DEP, '平日10:30・土日祝10:40', '10:30 on weekdays, 10:40 on weekends and holidays'),
        'katsuoji': (VIS, '11:00〜12:30', '11:00–12:30'),
        'visitor': (VIS, '13:10〜13:30', '13:10–13:30'),
        'sugi': (VIS, '14:00', '14:00'),
        'falls': (VIS, '14:05〜14:40', '14:05–14:40'),
        'onsen': (VIS, '15:25〜17:05', '15:25–17:05'),
        'minoh-st': (VIS, '17:20', '17:20'),
        'misdo': (VIS, '17:25〜17:45', '17:25–17:45'),
        'ahoya': (VIS, '18:00', '18:00'),
        'beer': (VIS, '18:25〜', '18:25–'),
        'kurobee': (VIS, '19:40〜', '19:40–'),
        'makiochi': (DEP, '20:30〜', '20:30–'),
    },
    'late-noonsen': {
        'kayano': (ARR, '10:30ごろ', 'about 10:30'),
        'bus': (DEP, '平日10:30・土日祝10:40', '10:30 on weekdays, 10:40 on weekends and holidays'),
        'katsuoji': (VIS, '11:00〜12:30', '11:00–12:30'),
        'visitor': (VIS, '13:10〜13:40', '13:10–13:40'),
        'sugi': (VIS, '14:10', '14:10'),
        'falls': (VIS, '14:15〜15:00', '14:15–15:00'),
        'minoh-st': (VIS, '16:10', '16:10'),
        'misdo': (VIS, '16:15〜16:35', '16:15–16:35'),
        'ahoya': (VIS, '16:50', '16:50'),
        'beer': (VIS, '17:15〜', '17:15–'),
        'kurobee': (VIS, '18:30〜', '18:30–'),
        'makiochi': (DEP, '19:20〜', '19:20–'),
    },
}

# 一覧の見出し（紹介ページの「1日の流れ」の何番目か）。コースごとに i18n.js の day の並びと合わせる
SECTIONS = {
    'early': [(('kayano', 'bus'), 0), (('katsuoji',), 1), (('visitor', 'sugi', 'falls'), 2), (('cinque',), 3), (('onsen', 'minoh-st'), 4), (('misdo', 'ahoya', 'beer', 'kurobee', 'makiochi'), 5)],
    'early-noonsen': [(('kayano', 'bus'), 0), (('katsuoji',), 1), (('visitor', 'sugi', 'falls'), 2), (('cinque',), 3), (('minoh-st',), 4), (('misdo', 'ahoya', 'beer', 'kurobee', 'makiochi'), 5)],
    'late': [(('kayano', 'bus'), 0), (('katsuoji',), 1), (('visitor', 'sugi', 'falls'), 2), (('onsen', 'minoh-st'), 3), (('misdo', 'ahoya', 'beer', 'kurobee', 'makiochi'), 4)],
    'late-noonsen': [(('kayano', 'bus'), 0), (('katsuoji',), 1), (('visitor', 'sugi', 'falls'), 2), (('minoh-st',), 3), (('misdo', 'ahoya', 'beer', 'kurobee', 'makiochi'), 4)],
}

# コースで変わる段落。段落の書き出し（starts）で見つけて、丸ごと入れ替える
COURSE_TEXT = {
    'bus': {
        'starts': {'ja': ('大阪の中心を', '早めに出発のコース', 'ゆっくり出発のコース'), 'en': ('Leave central Osaka', 'On the early course', 'On the late course')},
        'early': {
            'ja': '早めに出発のコースでは、9:00発のバスに乗ります（平日も土日祝も9:00発があります）。梅田を8:30までに出ると、9:00前に箕面萱野駅に着きます。乗り遅れたら、次は平日9:30、土日祝9:20です。そのときは勝尾寺を短くして、11:00には歩き始めてください。遅れると、川のテラスのラストオーダー（14:30）に間に合いません。',
            'en': 'On the early course you take the 9:00 bus (it runs on weekdays, weekends and holidays). Leave Umeda by 8:30 and you reach Minoh-Kayano just before 9:00. If you miss it, the next bus is 9:30 on weekdays or 9:20 on weekends and holidays. In that case cut Katsuoji short and still start walking at 11:00, or you will miss last order (14:30) at the river terrace.',
        },
        'late': {
            'ja': 'ゆっくり出発のコースでは、平日は10:30発、土日祝は10:40発のバスに乗ります。梅田を10:00ごろに出ると、10:30ごろに箕面萱野駅に着きます。平日の10:30発に間に合わなければ、次は11:00発です（勝尾寺の時間が30分短くなります）。',
            'en': 'On the late course you take the 10:30 bus on weekdays or the 10:40 on weekends and holidays. Leave Umeda around 10:00 and you reach Minoh-Kayano at about 10:30. If you miss the 10:30 on a weekday, the next one is 11:00 (you get 30 minutes less at Katsuoji).',
        },
    },
}

# コースによって足す段落（時間の行の前に、この順で足す）。(スポット, どのコースに足すか, 日本語, 英語)
# when は (出発時間, 温泉) で、None は「どちらでも」
ADD = [
    ('bus', ('early', None),
     'このバスは現金が使えません。反対に、川のテラスのランチ（チンクエピュウ）は現金だけです。ICカードと現金の両方を持って行きましょう。',
     'This bus does not take cash. The river terrace where you have lunch (Cinque Piu) is the opposite: cash only. Carry both an IC card and cash.'),
    ('katsuoji', (None, None),
     '勝尾寺から箕面ビジターセンターまでは約1.8km、ゆっくり歩いて約40分です。',
     'From Katsuoji to the Minoh Visitor Center it is about 1.8 km, around 40 minutes at an easy pace.'),
    ('visitor', (None, None),
     'ここで20分ほど休みましょう。ビジターセンターから杉の茶屋までは約1.5km、ゆっくり歩いて約30分です。杉の茶屋から滝までは約5分。',
     'Rest here for about 20 minutes. From the Visitor Center to Sugi no Chaya it is about 1.5 km, around 30 minutes at an easy pace. From Sugi no Chaya to the falls takes about 5 minutes.'),
    ('onsen', (None, True),
     'タトゥーのある人へ：入れ墨・タトゥーのある人は入れません。温泉が売っている専用のカバーシール2枚までで完全に隠せる場合だけ入れます。隠せない人は、一覧の上のボタンで「温泉に入らない」を選んでください。',
     'If you have tattoos: people with tattoos are not admitted, unless the tattoos can be completely covered with no more than two of the cover stickers the onsen sells. If you can’t cover them, choose “No onsen” with the buttons at the top of the list.'),
    ('beer', (None, None),
     '木曜日はお休みです。木曜に行く人は、たこ焼きのあと、すぐ近くの黒兵衛のラーメンを晩ごはんにしましょう。日曜は20:00に閉まります（ラストオーダー19:30）。',
     'It is closed on Thursdays: if you come on a Thursday, have dinner at Kurobee, the ramen shop just nearby, after the takoyaki. On Sundays it closes at 20:00 (last order 19:30).'),
    # 早めに出発
    ('falls', ('early', None),
     '早めに出発のコースでは、13:10ごろに滝を出ます。川のテラスのチンクエピュウまで、滝道を下って35〜40分です。',
     'On the early course, leave the falls at about 13:10. The river terrace, Cinque Piu, is 35–40 minutes down the Takimichi.'),
    ('cinque', ('early', None),
     'このコースでは13:50ごろに着きます。ラストオーダーの14:30まで40分しかないので、着いたらすぐに注文してください。',
     'On this course you arrive at about 13:50. That leaves only 40 minutes before last order at 14:30, so order as soon as you arrive.'),
    ('cinque', ('early', False),
     '温泉に入らないコースでは、ランチのあと1時間ほど自由に使えます。ここから箕面駅までは歩いて10分ほどなので、16:10ごろに駅に着けば大丈夫です。すぐ近くの瀧安寺（りゅうあんじ）にお参りしたり、滝道のお店でもみじの天ぷらを買ったり。滝道ぞいの箕面公園昆虫館もおすすめです。中の「放蝶園（ほうちょうえん）」では、一年中たくさんのチョウが飛んでいます（10:00〜17:00、受付は16:30まで、火曜休み、高校生以上280円）。',
     'On the no-onsen course you have about an hour free after lunch. Minoh Station is only about 10 minutes’ walk from here, and you just need to be there by about 16:10. Visit Ryuanji Temple, or buy momiji tempura at one of the shops on the path. The Minoh Park Insect Museum on the Takimichi is worth a stop too: its butterfly garden has butterflies flying around you all year (10:00–17:00, last entry 16:30, closed Tuesdays, ¥280 for high-school age and up).'),
    # ゆっくり出発（お昼ごはんの案内）。確認した日と出典は SOURCES
    ('kayano', ('late', None),
     'ゆっくり出発のコースは、山の中でお昼の時間になります。勝尾寺から滝までの山道ぞいで、食事のできるお店は確認できていません。お昼ごはんは、ここで買って持って行きましょう。駅の横のみのおキューズモール STATION棟1階に、ファミリーマートがあります（24時間営業）。',
     'On the late course, lunchtime comes while you are up in the hills. I could not confirm any place serving meals on the trail between Katsuoji and the falls, so buy lunch here and carry it. There is a FamilyMart on the 1st floor of the STATION building of Minoh Q’s Mall, next to the station (open 24 hours).'),
    ('katsuoji', ('late', None),
     'お昼について：公式サイトの境内マップには、食事のできるお店はのっていません。箕面萱野駅で買ったお昼を、次のビジターセンターの広場で食べましょう。',
     'About lunch: the temple’s official precinct map shows no place to eat. Eat the lunch you bought at Minoh-Kayano at the Visitor Center, the next stop.'),
    ('visitor', ('late', None),
     'ゆっくり出発のコースでは、ここでお昼にします。ビジターセンターのある政ノ茶屋園地（まさのちゃやえんち）には、お弁当を広げて休める「もみじ広場」があります（箕面市観光協会の案内より）。野生のサルがいるので、食べ物を出しっぱなしにしないで、ゴミは持ち帰ってください。',
     'On the late course, this is your lunch stop. The Masa-no-chaya area around the Visitor Center has the “Momiji Hiroba”, a lawn where you can sit down with a packed lunch (per the Minoh Tourism Association). Wild monkeys live here, so don’t leave food out, and take your rubbish with you.'),
    ('falls', ('late', True),
     'ゆっくり出発のコースでは、14:40ごろに滝を出て、滝道を約40分下って箕面温泉へ向かいます。',
     'On the late course, leave the falls at about 14:40 and walk about 40 minutes down the Takimichi to Minoh Onsen.'),
    ('falls', ('late', False),
     '温泉に入らないコースでは、滝でゆっくりできます。15:00ごろに滝を出て、滝道を1時間10分ほどかけて下りましょう（歩くだけなら約40分）。16:10ごろに箕面駅に着けば大丈夫です。下のほうまで来たら、瀧安寺（りゅうあんじ）にお参りしたり、滝道のお店でもみじの天ぷらを買ったり。滝道ぞいの箕面公園昆虫館もおすすめです。中の「放蝶園（ほうちょうえん）」では、一年中たくさんのチョウが飛んでいます（10:00〜17:00、受付は16:30まで、火曜休み、高校生以上280円）。',
     'On the no-onsen course you can take your time at the falls. Leave at about 15:00 and give yourself around 1 hour 10 minutes for the Takimichi (the walk alone is about 40 minutes); you just need to reach Minoh Station by about 16:10. Near the bottom you can visit Ryuanji Temple, or buy momiji tempura at one of the shops on the path. The Minoh Park Insect Museum on the Takimichi is worth a stop too: its butterfly garden has butterflies flying around you all year (10:00–17:00, last entry 16:30, closed Tuesdays, ¥280 for high-school age and up).'),
    ('falls', ('late', None),
     'お昼がまだの人へ：滝道ぞいには、うどんや喫茶など、食事のできるお店が何軒もあります（箕面市観光協会の「グルメ」の一覧にのっています）。ただ、午後の何時まで開いているかはお店ごとに違い、確認できていません（要確認）。川のテラスのチンクエピュウはラストオーダーが14:30なので、このコースでは間に合いません。',
     'Still need lunch? There are several places to eat along the Takimichi, such as udon shops and cafés (see the Minoh Tourism Association’s “Gourmet” list). How late each one stays open in the afternoon differs, and I could not confirm it (please check). The river terrace, Cinque Piu, takes last orders at 14:30, so it is out of reach on this course.'),
]

# チンクエピュウ：現金だけ（公式サイト cinquepiu.jp/terrace/ に「精算は現金のみ」）。目立つ注意書きにする
CINQUE_NOTICE = {
    'from': None, 'to': None, 'url': 'https://cinquepiu.jp/terrace/',
    'head': {'ja': '現金だけです', 'en': 'Cash only'},
    'text': {'ja': 'カードも交通系ICカードも使えません。先に注文とお会計をしてから、席に案内されます。勝尾寺へのバスは現金が使えないので、現金を持たずに来てしまいがちです。現金は大阪の街で用意しておきましょう。箕面萱野駅の横のみのおキューズモールにも、銀行（三井住友銀行・関西みらい銀行）とファミリーマートがあります（海外のカードで引き出せるかは要確認）。',
             'en': 'No cards and no IC cards. You order and pay first, then you are shown to a seat. The bus to Katsuoji doesn’t take cash, so it is easy to arrive here without any. Bring cash from the city. Minoh Q’s Mall next to Minoh-Kayano Station also has banks (SMBC and Kansai Mirai Bank) and a FamilyMart (I could not confirm whether overseas cards work there).'},
}

# 箕面温泉スパーガーデン：2026-11-21 に公式サイト（https://www.ooedoonsen.jp/minoh-spa/）で確認した内容に入れ替える。
# 2026-11-24 に見直し：シールの大きさ・値段はグループ共通のFAQ（faq.ooedoonsen.jp/45）、入湯税は箕面市のページで確認。休館日は記載なし（要確認）
ONSEN_URL = 'https://www.ooedoonsen.jp/minoh-spa/'
ONSEN = {
    'info': {
        'rows': [
            {'kind': 'hours', 'text': {'ja': '9:00〜23:45（最終入館22:45）', 'en': '9:00–23:45 (last entry 22:45)'}, 'until': None, 'from': None},
            {'kind': 'fee', 'text': {
                'ja': '17時までに入る場合：大人 平日2,420円・土日祝2,860円・繁忙日3,190円、小学生1,320円、幼児770円、3歳未満は無料。17時以降に入ると大人2,090円。別に入湯税（日帰り75円、12歳未満はかかりません）',
                'en': 'Entering before 17:00: adults ¥2,420 on weekdays, ¥2,860 on weekends and holidays, ¥3,190 on peak days; elementary school children ¥1,320; preschoolers ¥770; under 3 free. Entering after 17:00: adults ¥2,090. Plus bathing tax (¥75 for a day visit; none for under 12)'}, 'until': None, 'from': None},
            {'kind': 'tattoo', 'text': {
                'ja': '入れ墨・タトゥーのある人は入れません。温泉指定の有料カバーシール2枚以内で完全に隠せる場合だけ入れます',
                'en': 'No entry with tattoos, unless they can be completely covered with at most two of the onsen’s own paid cover stickers'}, 'until': None, 'from': None},
        ],
        'cash': False,
        'verified': True,
        'tip': {'ja': '休館日は公式サイトに書かれていません（要確認）。阪急箕面駅からは歩いて約5分。食べ物・飲み物の持ち込みはできません。中学生以下は保護者と一緒に、22:00まで。',
                'en': 'Closing days are not on the official website (please check). It is about 5 minutes on foot from Hankyu Minoh Station. You can’t bring in food or drink. Children of junior-high age and under must be with a parent or guardian and leave by 22:00.'},
        'checked': '2026-11-24',
    },
    'links': [
        {'kind': 'official', 'label': {'ja': '箕面温泉スパーガーデン 公式サイト（営業時間・料金）', 'en': 'Minoh Onsen Spa Garden: official site (Japanese)'}, 'url': {'ja': ONSEN_URL, 'en': ONSEN_URL}},
        {'kind': 'info', 'label': {'ja': 'リニューアルの紹介記事（ウォーカープラス 2026年11月）', 'en': 'Article on the reopening (Walker Plus, Nov 2026, Japanese)'},
         'url': {'ja': 'https://www.walkerplus.com/article/1447739/', 'en': 'https://www.walkerplus.com/article/1447739/'}},
    ],
    'caution': {'ja': 'タトゥーは、カバーシール2枚で完全に隠せる場合だけ入れます', 'en': 'Tattoos: entry only if two cover stickers hide them completely'},
    'notices': [{
        'from': None, 'to': None, 'url': ONSEN_URL,
        'head': {'ja': 'タトゥーがある人へ', 'en': 'If you have tattoos'},
        'text': {'ja': '入れ墨・タトゥーのある人は入れません。入れるのは、温泉が売っている専用のカバーシール（有料）2枚までで、タトゥーを完全に隠せる場合だけです（公式サイトで確認）。シール2枚で隠しきれない大きさ（腕全体、背中など）のタトゥーは入れません。シールは1枚10cm×14cm（はがきより少し小さいくらい）で、1枚220円（税込）。フロントで売っています（大江戸温泉物語グループのよくある質問より）。隠せない人は、一覧の上のボタンで「温泉に入らない」を選んでください。温泉を外した時間割に変わります。',
                 'en': 'People with tattoos are not admitted. The only exception: your tattoos can be completely covered with no more than two of the paid cover stickers the onsen sells (confirmed on the official website). Anything too big for two stickers, such as a sleeve or a back piece, cannot enter. Each sticker is 10 cm × 14 cm (a little smaller than a postcard) and costs ¥220 including tax, sold at the front desk (per the Ooedo Onsen Monogatari group FAQ). If you can’t cover yours, choose “No onsen” with the buttons at the top of the list: the timetable changes to one without the onsen.'},
    }],
}

LATE_LINKS = {
    'kayano': {'kind': 'info', 'label': {'ja': 'みのおキューズモール：ファミリーマート（STATION棟1階）', 'en': 'Minoh Q’s Mall: FamilyMart, STATION 1F (Japanese)'},
               'url': 'https://qs-mall.jp/minoh/shop/detail/330128002?tenant_cd=330128002'},
    'visitor': {'kind': 'info', 'label': {'ja': '箕面市観光協会：箕面ビジターセンター（もみじ広場）', 'en': 'Minoh Tourism Association: Visitor Center and Momiji Hiroba (Japanese)'},
                'url': 'https://minohkankou.net/sights/319/'},
    'falls': {'kind': 'info', 'label': {'ja': '箕面市観光協会：グルメ（滝道のお店の一覧）', 'en': 'Minoh Tourism Association: places to eat (Japanese)'},
              'url': 'https://minohkankou.net/sights/gourmets/'},
}
SOURCES = [
    {'what': '箕面萱野駅のファミリーマート（みのおキューズモール STATION 1F・24時間）', 'url': 'https://qs-mall.jp/minoh/shop/detail/330128002?tenant_cd=330128002', 'checked': '2026-11-21'},
    {'what': '政ノ茶屋園地の「もみじ広場」（お弁当を広げて休憩できる）', 'url': 'https://minohkankou.net/sights/319/', 'checked': '2026-11-21'},
    {'what': '滝道ぞいの食事のできる店の一覧（各店の営業時間は未確認）', 'url': 'https://minohkankou.net/sights/gourmets/', 'checked': '2026-11-21'},
    {'what': '箕面温泉スパーガーデンの営業時間・入館料・タトゥーの決まり（「入れ墨・タトゥーのある方（当館指定の有料カバーシール2枚以内で完全に覆える場合を除く）」）・アクセス（公式サイト。休館日、カバーシールの大きさ・値段、入湯税の金額は記載なし）', 'url': ONSEN_URL, 'checked': '2026-11-24'},
    {'what': 'チンクエピュウ テラス：1オーダー制・精算は現金のみ・11:30〜15:00（ラストオーダー14:30）・雨天休み', 'url': 'https://cinquepiu.jp/terrace/', 'checked': '2026-11-24'},
    {'what': 'みのおキューズモールの銀行（三井住友銀行 みのおキューズモール店・関西みらい銀行。アクセスのページの一覧に記載）', 'url': 'https://qs-mall.jp/minoh/access/', 'checked': '2026-11-21'},
    {'what': '箕面公園昆虫館：10:00〜17:00（最終受付16:30）・火曜休館・高校生以上280円。放蝶園は一年中チョウが飛んでいる（公式サイトの「放蝶園」のページ）', 'url': 'https://www.mino-konchu.jp/c8060.html', 'checked': '2026-11-22'},
    {'what': 'カバーシール：大江戸温泉物語グループ共通のよくある質問「【ご入浴】タトゥーを入れていますが、浴場は利用できますか」。10cm×14cmのカバーシール2枚で完全に覆える大きさなら利用可、1枚220円（税込）でフロントで販売、温浴施設も同じ条件で入館可（以前の6.5cm×10.5cmは誤り）', 'url': 'https://faq.ooedoonsen.jp/45', 'checked': '2026-11-24'},
    {'what': '箕面市の入湯税：日帰りで入湯するかた75円/日（宿泊200円）。12歳未満は課税されない（箕面市「入湯税」のページ、更新日2023年7月24日）', 'url': 'https://www.city.minoh.lg.jp/zeimu/shiminzeikoukai/nyuutouzei.html', 'checked': '2026-11-24'},
    {'what': '勝尾寺の中の食事処：公式サイトの境内マップ（1〜29の施設。無料休憩所・喫煙所などはあるが、食事処はない）とサイトマップの全ページに記載なし。おみやげのページは「準備中」', 'url': 'https://katsuo-ji-temple.or.jp/seasons/map.php', 'checked': '2026-11-24'},
    {'what': '杉の茶屋：箕面市観光協会のページは「定休日 不定休」だけで、営業時間の記載なし（要確認のまま）', 'url': 'https://minohkankou.net/sights/1493/', 'checked': '2026-11-24'},
    {'what': 'あほや 牧落店：公式サイト・公式SNSは見つからず、箕面市観光協会のサイトにも掲載なし（「あほや」で検索して0件）。営業時間は要確認のまま', 'url': 'https://minohkankou.net/?s=%E3%81%82%E3%81%BB%E3%82%84', 'checked': '2026-11-24'},
    {'what': '阪急バス30系統 箕面萱野駅8番のりば発の時刻（2026年2月1日現在の時刻表。平日 毎時00・30分、土休日 9:00〜12:40は20分ごと・13:00〜15:00は30分ごと）', 'url': 'https://transfer-cloud.navitime.biz/hankyubus/courses/timetables?busstop=00021386&timetable-id=202106', 'checked': '2026-11-21'},
    {'what': 'ミスタードーナツ 箕面ショップ：営業時間9:00〜20:00、住所 箕面6丁目1番30、クレジットカード・交通系電子マネー・PayPayなど可（ミスタードーナツ公式の店舗検索）', 'url': 'https://md.mapion.co.jp/b/misterdonut/info/0001/', 'checked': '2026-11-25'},
    {'what': 'ミスタードーナツの1号店：1971年4月、大阪府箕面市に第1号店をオープン（ダスキン公式の沿革）', 'url': 'https://www.duskin.co.jp/company/history/', 'checked': '2026-11-25'},
    {'what': '箕面ショップが日本の1号店で、2020年1月に創業当時の白とオレンジの姿に改装、店内に当時の写真を展示（トラベル Watch 2020-01-24）', 'url': 'https://travel.watch.impress.co.jp/docs/news/1231168.html', 'checked': '2026-11-25'},
    {'what': '黒兵衛 箕面総本店：公式サイト（kurobee.info）は中身のないページで、営業時間は確認できず。Retty では 11:00〜翌1:30・無休・カード不可・PayPay可・牧落3-13-13（要確認のまま）。麺の硬さの表と「食べ放題コーナー」は店内の掲示（2026-11-24 の写真）', 'url': 'https://retty.me/restaurant/100000064015/', 'checked': '2026-11-25'},
]

TIME_LINE = {'ja': re.compile(r'^おすすめ(?:訪問|出発|到着)時間\s*[：:]'), 'en': re.compile(r'^Recommended (?:visit|departure|arrival) time\s*:')}


def on(when, start, onsen):
    return when[0] in (None, start) and when[1] in (None, onsen)


def paras(text):
    return text.split('\n\n')


def set_text(spot, cid, start, onsen, no_of):
    """コースに合わせて、1つのスポットの文章を作り直す。"""
    sid = spot['id']
    for li, l in enumerate(('ja', 'en')):
        ps = paras(spot['text'][l])
        # 時間の行と、このスクリプトが足した段落はいったん外す（何回実行しても増えないように）
        added = {a[2 + li] for a in ADD if a[0] == sid}
        ps = [p for p in ps if not TIME_LINE[l].match(p) and p not in added]
        # コースで変わる段落を入れ替える
        ct = COURSE_TEXT.get(sid)
        if ct:
            hit = [i for i, p in enumerate(ps) if p.startswith(ct['starts'][l])]
            assert len(hit) == 1, (sid, l, hit)
            ps[hit[0]] = ct[start][l]
        # 足す段落
        ps += [a[2 + li] for a in ADD if a[0] == sid and on(a[1], start, onsen)]
        head, ja, en = TIMES[cid][sid]
        ps.append(f'{head[0]}：{ja}' if l == 'ja' else f'{head[1]}: {en}')
        t = '\n\n'.join(ps)
        # 文章の中の「次の◯番」は、そのコースの番号に直す
        if sid == 'kayano':
            t = re.sub(r'（次の\d+番）', f"（次の{no_of['bus']}番）", t); t = re.sub(r'\(stop \d+\)', f"(stop {no_of['bus']})", t)
        if sid in ('minoh-st', 'misdo', 'kurobee'):
            nxt = no_of[{'minoh-st': 'misdo', 'misdo': 'ahoya', 'kurobee': 'makiochi'}[sid]]
            t = re.sub(r'（次の\d+番）', f"（次の{nxt}番）", t); t = re.sub(r'\(stop \d+\)', f"(stop {nxt})", t)
        if sid == 'falls':
            t = t.replace('約40分（約2.7km）', '約40分（約2.8km）').replace('about 40 minutes (about 2.7 km)', 'about 40 minutes (about 2.8 km)')
        spot['text'][l] = t


def build(base, cid, start, onsen):
    d = copy.deepcopy(base)
    keep = [s for s in d['spots'] if s['id'] in TIMES[cid]]
    assert [s['id'] for s in keep] == [i for i in ORDER if i in TIMES[cid]]
    assert ('onsen' in TIMES[cid]) == onsen and ('cinque' in TIMES[cid]) == (start == 'early')
    no_of = {s['id']: i + 1 for i, s in enumerate(keep)}
    for s in keep:
        s['no'] = no_of[s['id']]
        set_text(s, cid, start, onsen, no_of)
        if start == 'late' and s['id'] in LATE_LINKS:
            k = LATE_LINKS[s['id']]
            s['links'] = s['links'] + [{'kind': k['kind'], 'label': k['label'], 'url': {'ja': k['url'], 'en': k['url']}}]
    d['spots'] = keep
    d['sections'] = [{'first': no_of[ids[0]], 'last': no_of[ids[-1]], 'day': day} for ids, day in SECTIONS[cid]]
    assert d['sections'][0]['first'] == 1 and d['sections'][-1]['last'] == len(keep)
    assert all(a['last'] + 1 == b['first'] for a, b in zip(d['sections'], d['sections'][1:]))
    d['course'] = cid
    return d


def main():
    base = json.load(open(BASE, encoding='utf-8'))
    # id を付ける（no のすぐ後ろに入れる）
    spots = []
    for s in base['spots']:
        sid = s.get('id') or IDS[s['name']['ja']]
        spots.append({'no': s['no'], 'id': sid, **{k: v for k, v in s.items() if k not in ('no', 'id')}})
    base['spots'] = spots
    assert [s['id'] for s in spots] == ORDER, [s['id'] for s in spots]
    # バスの時刻は 2026-11-21 に阪急バスの時刻表で確かめ直した
    next(s for s in spots if s['id'] == 'bus')['info']['checked'] = '2026-11-21'
    next(s for s in spots if s['id'] == 'onsen').update(copy.deepcopy(ONSEN))

    # チンクエピュウの「現金だけです」（元のファイルに手で書いた注意書きがあれば、その前に置く）
    cq = next(s for s in spots if s['id'] == 'cinque')
    cq['notices'] = [copy.deepcopy(CINQUE_NOTICE)] + [n for n in cq['notices'] if (n.get('head') or {}).get('ja') != CINQUE_NOTICE['head']['ja']]
    cq['caution'] = {'ja': '現金だけ（カード・ICカード不可）・ラストオーダー14:30・雨の日は休み', 'en': 'Cash only (no cards, no IC cards) · last order 14:30 · closed when it rains'}

    for cid, fname, start, onsen in COURSES:
        d = build(base, cid, start, onsen)
        if fname != 'minoh.json':
            d['_note'] = (f'大阪・箕面マップのコース「{cid}」のデータ。scripts/build_minoh_courses.py が data/routes/minoh.json から作る。'
                          'このファイルは直接直さない（直すのは minoh.json かスクリプト）。')
        d['sources'] = SOURCES
        open(f'{R}/data/routes/{fname}', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
        print(fname, cid, len(d['spots']), 'spots')


if __name__ == '__main__':
    main()
