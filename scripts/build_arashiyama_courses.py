#!/usr/bin/env python3
"""嵐山マップの3つのコース（出発のしかた）のデータを、1つの元から作る。

使い方: python3 scripts/build_arashiyama_courses.py   （そのあと python3 scripts/sync_arashiyama.py）
- 元: data/routes/arashiyama.json（手で直すのはこのファイルだけ。9〜10時に出発するコース）
- 作るもの（COURSES）:
  - data/routes/arashiyama.json … 「late」9〜10時に出発（9:44のバス）。id・出典・一部の段落を入れ直して上書き（何回実行しても同じ結果）
  - data/routes/arashiyama-early.json … 「early」早朝に出発、愛宕念仏寺が開いている日（日・月・火・木・金）。
    9:00の開門に合わせて、8:39（日曜・祝日は8:41）のバスで上る。あとは元と同じ順で、約55分ずつ早い
  - data/routes/arashiyama-tenryuji.json … 「tenryuji」早朝に出発、水・土（愛宕念仏寺が休みの日）。
    天龍寺に8:30の開門で入り、北門から竹林へ。朝ごはんのあと奥嵯峨のお寺、お昼、渡月橋、モンキーパーク
  arashiyama.json 以外は直接直さない（実行のたびに作り直す）
- めやすの時間は TIMES、コースで入れ替える段落は SWAP、足す段落は ADD、一覧の短い紹介は BLURB、
  「選んで回る」の設定は PLAN、確認した出典と確認日は SOURCES（データの sources に入る）
- 紹介ページ（arashiyama/js/i18n.js の courseFor）の写真は、ここで付けるスポットの id で指定している
- オーナーの基準（2026-11-22）：昼に混む場所があるマップは「開門に合わせる早朝」と「9〜10時に出発」の両方を用意する。
  出発は京都の中心・三条のあたりを想定。時刻は公式サイトと乗換案内で確かめたものだけを書く
"""
import copy, json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = f'{R}/data/routes/arashiyama.json'
COURSES = [('late', 'arashiyama.json'), ('early', 'arashiyama-early.json'), ('tenryuji', 'arashiyama-tenryuji.json')]

IDS = {
    '京都河原町駅': 'kawaramachi', '桂駅': 'katsura', '阪急嵐山駅': 'hankyu', '阪急嵐山駅前 バスのりば': 'bus',
    '愛宕念仏寺': 'otagi', '嵯峨鳥居本の町並み': 'toriimoto', '化野念仏寺': 'adashino', '祇王寺': 'gioji', '二尊院': 'nisonin',
    '常寂光寺': 'jojakkoji', '大河内山荘庭園': 'okochi', '嵐山 竹林の小径': 'bamboo', '嵯峨野 竹林の小径・野宮神社': 'nonomiya',
    '天龍寺': 'tenryuji', '嵯峨野湯': 'saganoyu', '渡月橋': 'togetsukyo', '嵐山モンキーパークいわたやま': 'monkey',
    '京都の街なかへ（先斗町）': 'pontocho',
}
BASE_ORDER = ['kawaramachi', 'katsura', 'hankyu', 'bus', 'otagi', 'toriimoto', 'adashino', 'senno', 'gioji', 'nisonin', 'jojakkoji',
              'okochi', 'bamboo', 'nonomiya', 'tenryuji', 'saganoyu', 'togetsukyo', 'monkey', 'pontocho']
ORDER = {
    'late': BASE_ORDER,
    'early': BASE_ORDER,
    # 水・土：愛宕念仏寺とバスは外す。天龍寺→竹林→（朝ごはん）→奥嵯峨を北へ→戻ってお昼→渡月橋
    'tenryuji': ['kawaramachi', 'katsura', 'hankyu', 'tenryuji', 'bamboo', 'okochi', 'nonomiya', 'jojakkoji', 'nisonin', 'gioji',
                 'senno', 'adashino', 'toriimoto', 'saganoyu', 'togetsukyo', 'monkey', 'pontocho'],
}

# めやすの時間（各スポットの文章のいちばん下の行）。late は元のファイルの行をそのまま使う
DEP, VIS, MOV = ('おすすめ出発時間', 'Recommended departure time'), ('おすすめ訪問時間', 'Recommended visit time'), ('おすすめ移動時間', 'Recommended travel time')
TIMES = {
    'early': {
        'kawaramachi': (DEP, '平日7:50、日曜・祝日7:45', '7:50 on weekdays, 7:45 on Sundays and holidays'),
        'katsura': (MOV, '8:00ごろ', 'around 8:00'),
        'hankyu': (VIS, '8:15ごろ', 'about 8:15'),
        'bus': (DEP, '平日8:39、日曜・祝日8:41', '8:39 on weekdays, 8:41 on Sundays and holidays'),
        'otagi': (VIS, '9:00〜9:50', '9:00–9:50'),
        'toriimoto': (VIS, '9:55〜10:25', '9:55–10:25'),
        'adashino': (VIS, '10:35〜11:15', '10:35–11:15'),
        'senno': (VIS, '11:25〜12:05', '11:25–12:05'),
        'gioji': (VIS, '12:15〜12:45', '12:15–12:45'),
        'nisonin': (VIS, '12:55〜13:20', '12:55–13:20'),
        'jojakkoji': (VIS, '13:25〜14:00', '13:25–14:00'),
        'okochi': (VIS, '14:10〜14:50', '14:10–14:50'),
        'bamboo': (VIS, '14:10〜14:25', '14:10–14:25'),
        'nonomiya': (VIS, '14:25〜14:35', '14:25–14:35'),
        'tenryuji': (VIS, '14:40〜15:25', '14:40–15:25'),
        'saganoyu': (VIS, '15:35〜16:15', '15:35–16:15'),
        'togetsukyo': (VIS, '16:25〜16:45', '16:25–16:45'),
        'monkey': (VIS, '15:45ごろまでに入口へ', 'reach the entrance by about 15:45'),
        'pontocho': (MOV, '17:10〜', 'from 17:10'),
    },
    'tenryuji': {
        'kawaramachi': (DEP, '水曜7:50、土曜7:45', '7:50 on Wednesdays, 7:45 on Saturdays'),
        'katsura': (MOV, '8:00ごろ', 'around 8:00'),
        'hankyu': (VIS, '8:10ごろ', 'about 8:10'),
        'tenryuji': (VIS, '8:30〜9:15', '8:30–9:15'),
        'bamboo': (VIS, '9:15〜9:30', '9:15–9:30'),
        'okochi': (VIS, '9:30〜10:10', '9:30–10:10'),
        'nonomiya': (VIS, '9:35〜9:45（そのあと朝ごはん 9:55〜10:40）', '9:35–9:45 (then breakfast, 9:55–10:40)'),
        'jojakkoji': (VIS, '11:00〜11:35', '11:00–11:35'),
        'nisonin': (VIS, '11:40〜12:05', '11:40–12:05'),
        'gioji': (VIS, '12:15〜12:45', '12:15–12:45'),
        'senno': (VIS, '12:50〜13:35', '12:50–13:35'),
        'adashino': (VIS, '13:45〜14:25', '13:45–14:25'),
        'toriimoto': (VIS, '14:35〜15:05', '14:35–15:05'),
        'saganoyu': (VIS, '14:05〜14:45', '14:05–14:45'),
        'togetsukyo': (VIS, '14:10〜14:30', '14:10–14:30'),
        'monkey': (VIS, '14:40〜15:55', '14:40–15:55'),
        'pontocho': (MOV, '16:20〜', 'from 16:20'),
    },
}

# 一覧の見出し（紹介ページの「1日の流れ」の何番目か）。arashiyama/js/i18n.js の day の並びと合わせる
SECTIONS = {
    'late': [(('kawaramachi', 'hankyu'), 0), (('bus', 'adashino'), 1), (('senno', 'senno'), 2), (('gioji', 'okochi'), 3), (('bamboo', 'tenryuji'), 4), (('saganoyu', 'monkey'), 5), (('pontocho', 'pontocho'), 6)],
    'early': [(('kawaramachi', 'hankyu'), 0), (('bus', 'adashino'), 1), (('senno', 'senno'), 2), (('gioji', 'okochi'), 3), (('bamboo', 'tenryuji'), 4), (('saganoyu', 'monkey'), 5), (('pontocho', 'pontocho'), 6)],
    'tenryuji': [(('kawaramachi', 'hankyu'), 0), (('tenryuji', 'nonomiya'), 1), (('jojakkoji', 'toriimoto'), 3), (('saganoyu', 'monkey'), 5), (('pontocho', 'pontocho'), 6)],
}

CAFE_URL = 'https://bread-espresso.jp/shop/arashiyama-cafe.html'
BUS_URL = 'https://www.kyotobus.jp/route/timetable/schedule.html?stop_id=421_3'

# コースで入れ替える段落。段落の書き出し（starts）で見つけて丸ごと入れ替える。None は「その段落を外す」。
# コースの指定がなければ元のまま。文章の中の {no:id} は、そのコースでのスポットの番号に変わる
SWAP = [
    ('kawaramachi', {'ja': ('出発の時間は',), 'en': ('Work back from',)}, {
        'late': {
            'ja': '出発の時間は、{no:bus}番のバスから逆算します。9:44のバスに乗るなら、平日は9:04か9:08、土曜・日曜・祝日は9:04か9:15の電車で（嵐山に9:33、土日祝は9:37に着きます）。平日と土曜のバスは1時間に1本（9:44、10:44）です。',
            'en': 'Work back from the bus at stop {no:bus}. For the 9:44 bus, take the 9:04 or 9:08 train on weekdays, or the 9:04 or 9:15 on weekends and holidays (arriving in Arashiyama at 9:33, or 9:37 on weekends and holidays). On weekdays and Saturdays the bus runs once an hour (9:44, 10:44).',
        },
        'early': {
            'ja': '出発の時間は、{no:bus}番のバスから逆算します。愛宕念仏寺は9:00に開くので、乗るのは阪急嵐山駅前8:39発（日曜・祝日は8:41発）のバス。平日は7:50、日曜・祝日は7:45の電車に乗ると、嵐山に8:13（日曜・祝日は8:07）に着きます。次の8:01発（日曜・祝日は8:00発）でも間に合いますが、バスまでの時間が15分ほどしかありません。',
            'en': 'Work back from the bus at stop {no:bus}. Otagi Nenbutsu-ji opens at 9:00, so the bus to catch leaves Hankyu Arashiyama-ekimae at 8:39 (8:41 on Sundays and holidays). Take the 7:50 train on weekdays or the 7:45 on Sundays and holidays, and you reach Arashiyama at 8:13 (8:07 on Sundays and holidays). The next train, 8:01 (8:00 on Sundays and holidays), still makes it, but leaves only about 15 minutes for the bus.',
        },
        'tenryuji': {
            'ja': '出発の時間は、天龍寺の開門から逆算します。庭園は8:30に開くので、水曜は7:50、土曜は7:45の電車で（嵐山に8:13、土曜は8:07に着きます）。祝日の水曜は、土曜と同じ時刻です。駅から天龍寺までは、渡月橋を渡って歩いて15〜20分。',
            'en': 'Work back from the opening of Tenryu-ji. The garden opens at 8:30, so take the 7:50 train on a Wednesday or the 7:45 on a Saturday (arriving in Arashiyama at 8:13, or 8:07 on Saturdays). If the Wednesday is a holiday, use the Saturday times. From the station it is a 15–20 minute walk across Togetsukyo Bridge to Tenryu-ji.',
        },
    }),
    ('kawaramachi', {'ja': ('ゆっくり出たい日は',), 'en': ('For a slower morning',)}, {
        'late': {
            'ja': 'ゆっくり出たい日は、10:00ごろの電車で10:44のバスへ。あとの時間が全部1時間ずつ遅くなるので、{no:gioji}〜{no:jojakkoji}のお寺は1つにしてください。',
            'en': 'For a slower morning, take a train at about 10:00 for the 10:44 bus. Everything after that runs an hour later, so pick just one of the temples in {no:gioji}–{no:jojakkoji}.',
        },
        'early': None, 'tenryuji': None}),
    ('kawaramachi', {'ja': ('奥嵯峨（',), 'en': ('There are few places to eat',)}, {
        'late': {
            'ja': '奥嵯峨（{no:toriimoto}〜{no:okochi}番のあたり）は食事の店が少なめです。お昼は{no:senno}番の喫茶店を案内していますが、木曜は休みのようです（要確認）。心配な日は、パンやおにぎりを駅のまわりで買っておきましょう。',
            'en': 'There are few places to eat in Oku-Saga (around stops {no:toriimoto}–{no:okochi}). Lunch on this route is at the café at stop {no:senno}, but it seems to be closed on Thursdays (please check). If in doubt, buy bread or rice balls near the station.',
        },
        'early': {
            'ja': '朝ごはんは、出る前に食べるか、駅のまわりで買って行きましょう。お昼は{no:senno}番の喫茶店を案内していますが、木曜は休みのようです（要確認）。心配な日は、お昼のパンやおにぎりも一緒に買っておきましょう。',
            'en': 'Eat breakfast before you leave, or buy something near the station to take with you. Lunch on this route is at the café at stop {no:senno}, but it seems to be closed on Thursdays (please check). If in doubt, pick up bread or rice balls for lunch at the same time.',
        },
        'tenryuji': {
            'ja': '朝ごはんは、天龍寺と竹林を見たあと、10時ごろにカフェで食べる時間割です（{no:nonomiya}番に書いてあります）。それまでお腹がもたない人は、駅のまわりで軽いものを買って行きましょう。',
            'en': 'On this timetable, breakfast comes at a café at about 10:00, after Tenryu-ji and the bamboo grove (see stop {no:nonomiya}). If you can’t wait that long, buy something light near the station.',
        },
    }),
    ('hankyu', {'ja': ('桂川の南側にある',), 'en': ('The end of the Arashiyama Line',)}, {
        'early': {
            'ja': '桂川の南側にある、嵐山線の終点です。改札を出たら、駅前のバスのりばへ（次の{no:bus}番）。バスまで20〜30分あるので、先にのりばの場所を確かめておくと安心です。',
            'en': 'The end of the Arashiyama Line, on the south side of the Katsura River. Go through the ticket gates and head to the bus stop in front of the station (stop {no:bus}). You have 20–30 minutes before the bus, so find the stop first.',
        },
        'tenryuji': {
            'ja': '桂川の南側にある、嵐山線の終点です。改札を出たら、中之島を抜けて渡月橋を渡り、まっすぐ北へ。左側に天龍寺の入口があります。歩いて15〜20分です。',
            'en': 'The end of the Arashiyama Line, on the south side of the Katsura River. From the ticket gates, cross Nakanoshima and Togetsukyo Bridge and keep going north: the entrance to Tenryu-ji is on your left. Allow 15–20 minutes on foot.',
        },
    }),
    ('hankyu', {'ja': ('渡月橋はここから',), 'en': ('Togetsukyo Bridge is a short walk',)}, {
        'tenryuji': {
            'ja': '朝の渡月橋は、昼間よりずっと人が少ないことが多い時間です。午後にもう一度ゆっくり来ます（{no:togetsukyo}番）。',
            'en': 'In the early morning the bridge usually has far fewer people than in the daytime. You come back for a proper look in the afternoon (stop {no:togetsukyo}).',
        },
    }),
    ('bus', {'ja': ('清滝（きよたき）行きの',), 'en': ('Take route 92 or 94',)}, {
        'early': {
            'ja': '清滝（きよたき）行きの92系統に乗ります。平日は8:39発、日曜・祝日は8:41発。愛宕寺前には8:50（日曜・祝日は8:52）に着きます（京都バスの公式サイトの時刻表で2026年11月22日に確認）。',
            'en': 'Take route 92 bound for Kiyotaki: 8:39 on weekdays, 8:41 on Sundays and holidays. It reaches Otagidera-mae at 8:50 (8:52 on Sundays and holidays), per the Kyoto Bus timetable checked on Nov 22, 2026.',
        },
    }),
    ('bus', {'ja': ('平日と土曜は、乗り遅れると',), 'en': ('On weekdays and Saturdays, miss one',)}, {
        'early': {
            'ja': '乗り遅れると、次は平日9:44、日曜・祝日9:14です。急ぐときはタクシーで。愛宕念仏寺の公式サイトには、JR嵯峨嵐山駅の北口から約5分、およそ1,500円とあります。',
            'en': 'Miss it and the next bus is 9:44 on weekdays or 9:14 on Sundays and holidays. If you’re in a hurry, take a taxi: the temple’s website gives about 5 minutes and roughly ¥1,500 from the north exit of JR Saga-Arashiyama Station.',
        },
    }),
    ('bus', {'ja': ('水曜・土曜は愛宕念仏寺が休みです',), 'en': ('Otagi Nenbutsu-ji is closed on Wednesdays and Saturdays',)}, {
        'early': {
            'ja': '水曜・土曜は愛宕念仏寺が休みです。その日は、一覧の上のボタンで「早朝に出発（水・土）」を選んでください。天龍寺から始めるコースに変わります。',
            'en': 'Otagi Nenbutsu-ji is closed on Wednesdays and Saturdays. On those days choose “Early start (Wed & Sat)” with the buttons at the top of the list: the route changes to one that starts at Tenryu-ji.',
        },
    }),
    ('toriimoto', {'ja': ('お昼は12時すぎ', '朝が早い日は', 'お昼は'), 'en': ('Lunch comes after noon', 'After an early start')}, {
        'early': {
            'ja': '朝が早い日は、ここでひと休み。お昼は11時すぎです。朝のうちに平野屋が開いているかは確認できていません（要確認）。閉まっていたら、そのまま化野念仏寺へ。',
            'en': 'After an early start, this is the place for a rest. Lunch comes soon after 11:00. I couldn’t confirm whether Hiranoya is open this early in the morning (please check); if it’s closed, carry on to Adashino Nenbutsu-ji.',
        },
        'tenryuji': None,
    }),
    ('toriimoto', {'ja': ('ここから化野念仏寺までは',), 'en': ('From here it’s about a 10-minute walk downhill',)}, {
        'tenryuji': {
            'ja': 'このコースでは、化野念仏寺から坂を10分ほど上った先の寄り道です。坂の上の愛宕念仏寺は水曜・土曜が休みなので、平野屋のあたりで折り返します。嵐山の中心までは、同じ道を下って歩いて35〜40分。',
            'en': 'On this course it’s an extra: about 10 minutes uphill from Adashino Nenbutsu-ji. Otagi Nenbutsu-ji at the top is closed on Wednesdays and Saturdays, so turn round at Hiranoya. Central Arashiyama is 35–40 minutes’ walk back down the same road.',
        },
    }),
    ('adashino', {'ja': ('お昼は',), 'en': ('Have lunch',)}, {
        'late': {
            'ja': 'お昼は、ここから坂を10分ほど下った喫茶店「仙翁」で（次の{no:senno}番、12:25ごろ）。',
            'en': 'Have lunch at Senno, a café about 10 minutes’ walk downhill from here (stop {no:senno}, at about 12:25).',
        },
        'early': {
            'ja': 'お昼は、ここから坂を10分ほど下った喫茶店「仙翁」で（次の{no:senno}番、11:25ごろ）。',
            'en': 'Have lunch at Senno, a café about 10 minutes’ walk downhill from here (stop {no:senno}, at about 11:25).',
        },
        'tenryuji': {
            'ja': 'このコースでは、お昼のあとに10分ほど坂を上る寄り道です。足すと、渡月橋に着くのが15:00ごろになります。',
            'en': 'On this course it’s an extra after lunch, about 10 minutes uphill. Adding it puts you at Togetsukyo Bridge at about 15:00.',
        },
    }),
    ('nonomiya', {'ja': ('竹林の中を歩いて野宮神社まで',), 'en': ('Walk through the bamboo to Nonomiya Shrine',)}, {
        'late': {
            'ja': '竹林の中を歩いて野宮神社まで行ったら、少し戻って天龍寺の北門から庭園へ入ります（次の{no:tenryuji}番）。',
            'en': 'Walk through the bamboo to Nonomiya Shrine, then go back a little way and enter Tenryu-ji’s garden through its north gate (stop {no:tenryuji}).',
        },
        'early': {
            'ja': '竹林の中を歩いて野宮神社まで行ったら、少し戻って天龍寺の北門から庭園へ入ります（次の{no:tenryuji}番）。',
            'en': 'Walk through the bamboo to Nonomiya Shrine, then go back a little way and enter Tenryu-ji’s garden through its north gate (stop {no:tenryuji}).',
        },
        'tenryuji': {
            'ja': '朝ごはんはこのあと。天龍寺の近くの「エスプレッソと」（パンとエスプレッソと嵐山庭園のカフェ）は、8:00〜18:00、不定休です（お店の公式サイトで2026年11月22日に確認）。野宮神社から歩いて10分ほど。休みの日が決まっていないので、行く日に開いているかはお店の案内で確かめてください。',
            'en': 'Breakfast comes next. “Espresso to”, the café of Bread, Espresso & Arashiyama Garden near Tenryu-ji, is open 8:00–18:00 with irregular closing days (checked on its official website, Nov 22, 2026). It’s about 10 minutes on foot from Nonomiya Shrine. As the closing days aren’t fixed, check that it’s open on the day.',
        },
    }),
    ('tenryuji', {'ja': ('竹林の小径の途中にある北門から',), 'en': ('Enter through the north gate',)}, {
        'tenryuji': {
            'ja': 'このコースでは、開門の8:30に合わせて正面から入ります。庭園受付で拝観料を払って池の庭を歩き、奥の北門から出ると、そこが竹林の小径です（次の{no:bamboo}番）。開いてすぐは、昼間より静かに庭を眺められることが多い時間です。',
            'en': 'On this course you arrive for the 8:30 opening and go in from the front. Pay at the garden reception, walk round the pond garden, and leave by the north gate at the back: you step straight out onto the bamboo path (stop {no:bamboo}). Right after opening, the garden is usually quieter than in the daytime.',
        },
    }),
    ('saganoyu', {'ja': ('天龍寺の総門から歩いて6分ほど',), 'en': ('About 6 minutes on foot from Tenryu-ji’s main gate',)}, {
        'tenryuji': {
            'ja': 'このコースでは、奥嵯峨から下りてきたあとの寄り道です。お昼の{no:senno}番から歩いて30分ほど。寄ると、あとが45分ほど遅くなります。ここから渡月橋までは10分ほどです。',
            'en': 'On this course it’s an extra after you come down from Oku-Saga, about 30 minutes on foot from lunch at stop {no:senno}. Stopping here makes the rest about 45 minutes later. From here it’s about 10 minutes to Togetsukyo Bridge.',
        },
    }),
    ('monkey', {'ja': ('入園は16:00まで',), 'en': ('Last entry is 16:00',)}, {
        'late': {
            'ja': '入園は16:00まで（山頂は16:30まで）で、支払いは現金だけです。めやすの時間割どおりに歩くと間に合わないので、行く日は{no:gioji}〜{no:jojakkoji}のお寺を1つにして、嵯峨野湯を外してください。渡月橋に15:25ごろ着けます。',
            'en': 'Last entry is 16:00 (the summit closes at 16:30) and it’s cash only. The suggested timetable gets you here too late, so on a monkey day pick just one of the temples in {no:gioji}–{no:jojakkoji} and skip Sagano-yu: that puts you at the bridge at about 15:25.',
        },
        'early': {
            'ja': '入園は16:00まで（山頂は16:30まで）で、支払いは現金だけです。このコースでは、嵯峨野湯を外すと渡月橋に15:35ごろ、入口に15:45ごろ着けます。',
            'en': 'Last entry is 16:00 (the summit closes at 16:30) and it’s cash only. On this course, skip Sagano-yu and you reach the bridge at about 15:35 and the entrance at about 15:45.',
        },
        'tenryuji': {
            'ja': '入園は16:00まで（山頂は16:30まで）で、支払いは現金だけです。このコースでは14:40ごろに入口へ。山頂でゆっくりして、16時ごろに下りてきます。',
            'en': 'Last entry is 16:00 (the summit closes at 16:30) and it’s cash only. On this course you reach the entrance at about 14:40, with plenty of time at the top before coming down at about 16:00.',
        },
    }),
]

# コースによって足す段落（時間の行の前に、この順で足す）。(スポット, コース, 日本語, 英語)
ALL = ('late', 'early', 'tenryuji')
ADD = [
    ('kawaramachi', ALL,
     '京都の中心、三条通のあたりからは、河原町通を南へ歩いて10〜15分です。',
     'From the Sanjo-dori area in central Kyoto, it’s a 10–15 minute walk south along Kawaramachi-dori.'),
    ('otagi', ('early',),
     'このコースは、9:00の開門に合わせて着きます。バスは8:50ごろ着くので、門の前で少し待ちます。開いてすぐは、昼間より静かなことが多い時間です。',
     'This course gets you here for the 9:00 opening. The bus arrives at about 8:50, so you wait a little at the gate. Right after opening it is usually quieter than later in the day.'),
    ('bamboo', ('tenryuji',),
     'このコースでは、天龍寺の北門を出て9時すぎに歩きます。大河内山荘の前まで上って、同じ道を野宮神社のほうへ戻ります。朝は昼間より人が少ないことが多いですが、紅葉や桜の時期の土曜は、この時間でも人が出ています。',
     'On this course you walk it soon after 9:00, straight out of Tenryu-ji’s north gate. Go up as far as the entrance to Okochi Sanso, then come back the same way toward Nonomiya Shrine. Mornings usually have fewer people than midday, but on Saturdays in the autumn-leaf and cherry seasons it can be busy even at this hour.'),
    ('okochi', ('tenryuji',),
     'このコースでは、竹林を上りきったところで寄れます。9:00から開いていて、お抹茶つきなので、朝のひと休みにもなります。',
     'On this course you pass it at the top of the bamboo path. It opens at 9:00 and the matcha is included, so it also works as a morning rest.'),
    ('jojakkoji', ('tenryuji',),
     'このコースでは、朝ごはんのあとにここから奥嵯峨を北へ歩きます。カフェからは歩いて15〜20分です。',
     'On this course, this is where the walk north through Oku-Saga begins after breakfast. It’s 15–20 minutes on foot from the café.'),
    ('gioji', ('tenryuji',),
     'このコースでは、ここで折り返します。お昼は、歩いて5分ほどの喫茶店「仙翁」で（次の{no:senno}番）。',
     'On this course you turn round here. Lunch is at Senno, a café about 5 minutes’ walk away (stop {no:senno}).'),
    ('senno', ('late', 'early'),
     '化野念仏寺から坂を下って10分ほど。食べ終わったら、祇王寺までは歩いて5分ほどです。',
     'About 10 minutes downhill from Adashino Nenbutsu-ji. After lunch, Gio-ji is about 5 minutes’ walk away.'),
    ('senno', ('tenryuji',),
     '祇王寺から歩いて5分ほど。食べ終わったら、来た道を下って、渡月橋まで歩いて30分ほどです。',
     'About 5 minutes on foot from Gio-ji. After lunch, walk back down the way you came: Togetsukyo Bridge is about 30 minutes away.'),
    ('togetsukyo', ('early',),
     'このコースでは、明るいうちに橋に着きます。',
     'On this course you reach the bridge while it’s still light.'),
    ('pontocho', ALL,
     '先斗町は、四条通から三条通まで南北に続く細い路地です。晩ごはんのあと三条のほうへ歩けば、そのまま三条通に出られます。遅くまで開いている店もありますが、閉まる時間とラストオーダーは店ごとに違います。入る前に、表の案内で確かめてください。',
     'Pontocho is a narrow lane running north from Shijo-dori to Sanjo-dori. After dinner, keep walking north and you come out on Sanjo-dori. Some places stay open late, but closing times and last orders differ from shop to shop: check the sign outside before you go in.'),
    ('pontocho', ('early',),
     'このコースでは、嵐山を17:10ごろに出て、17:40ごろに京都河原町に着きます。',
     'On this course you leave Arashiyama at about 17:10 and reach Kyoto-kawaramachi at about 17:40.'),
    ('pontocho', ('tenryuji',),
     'このコースでは、嵐山を16:20ごろに出て、17時ごろに京都河原町に着きます。朝が早かったので、いったん休んでから晩ごはんに出るのもいいと思います。',
     'On this course you leave Arashiyama at about 16:20 and reach Kyoto-kawaramachi at about 17:00. After such an early start, a rest before heading out for dinner is a good idea.'),
]

# 一覧の短い紹介（コースで変えるものだけ）
BLURB = {
    'early': {
        'kawaramachi': ('スタートは四条通の地下にある阪急電車の駅。嵐山へは「桂」で乗り換えて約30分です。愛宕念仏寺の開門（9:00）に合わせて、7:50ごろの電車で。',
                        'The start: the Hankyu station under Shijo-dori. Arashiyama is about 30 minutes away with one change at Katsura. Take a train at about 7:50 to be at Otagi Nenbutsu-ji for its 9:00 opening.'),
        'bus': ('京都バス（92系統、清滝行き）で「愛宕寺前」まで11分。平日8:39発、日曜・祝日8:41発に乗ると、9:00の開門に間に合います。',
                'Kyoto Bus 92 (for Kiyotaki) to Otagidera-mae takes 11 minutes. The 8:39 (8:41 on Sundays and holidays) gets you there for the 9:00 opening.'),
        'pontocho': ('阪急嵐山駅から電車で京都河原町へ戻ると17:40ごろ。鴨川ぞいの細い路地、先斗町で晩ごはんに。',
                     'The train from Hankyu Arashiyama gets you back to Kyoto-kawaramachi at about 17:40: time for dinner in Pontocho, the narrow lane by the Kamo River.'),
    },
    'tenryuji': {
        'kawaramachi': ('スタートは四条通の地下にある阪急電車の駅。嵐山へは「桂」で乗り換えて約30分です。天龍寺の開門（8:30）に合わせて、7:50ごろの電車で。',
                        'The start: the Hankyu station under Shijo-dori. Arashiyama is about 30 minutes away with one change at Katsura. Take a train at about 7:50 to be at Tenryu-ji for its 8:30 opening.'),
        'hankyu': ('嵐山に到着。朝の渡月橋を渡って、天龍寺まで歩きます。帰りもこの駅から京都河原町へ戻ります。',
                   'Welcome to Arashiyama. Walk across Togetsukyo Bridge in the morning quiet to Tenryu-ji. You come back to this station at the end of the day.'),
        'tenryuji': ('嵐山を代表する禅寺で、世界遺産。嵐山を背にした池の庭「曹源池庭園」は、ゆっくり眺めていたくなる美しさです。8:30の開門に合わせて入り、北門から竹林へ出ます。',
                     'Arashiyama’s great Zen temple and a World Heritage site. Its pond garden, with the hills of Arashiyama behind it, is one to sit and gaze at. Arrive for the 8:30 opening and leave by the north gate into the bamboo.'),
        'bamboo': ('高い竹が両側から空をおおう、嵐山でいちばん有名な小道。天龍寺の北門を出ると、もう竹林の中です。',
                   'Arashiyama’s most famous path, where tall bamboo closes over the sky on both sides. Step out of Tenryu-ji’s north gate and you’re already in it.'),
        'toriimoto': ('化野念仏寺の先に続く坂道。茅葺き屋根の茶屋や町家が残る、昔ながらの町並みです。朱色の鳥居の前の茶屋でひと休みも。',
                      'The lane that climbs on past Adashino Nenbutsu-ji. Thatched teahouses and old townhouses line the way. Stop for tea by the red torii gate.'),
        'pontocho': ('阪急嵐山駅から電車で京都河原町へ戻ると17時ごろ。ひと休みしてから、鴨川ぞいの細い路地、先斗町で晩ごはんに。',
                     'The train from Hankyu Arashiyama gets you back to Kyoto-kawaramachi at about 17:00. Take a rest, then have dinner in Pontocho, the narrow lane by the Kamo River.'),
    },
}

# お昼の店（2026-11-22 オーナーが教えてくれた3軒）。仙翁を1つのスポットにして、茶房さがの・寿楽庵は同じスポットの中で紹介する。
# 位置はオーナーが Googleマップで教えてくれたもの。仙翁と茶房さがのはオーナーが行った店（感想は仙翁の「ビーフカレーが美味しかった」だけ書く）、
# 寿楽庵は行っていない店（中立に書く）。3軒とも公式サイト・公式SNSは見つからず、値段と「現金のみ」はオーナーが撮った店頭・店内の写真から、
# 時間と休みは食べログ・じゃらんから（要確認）。写真 senno-1〜4 は2025年10月10日（外観・ビーフカレー・店頭のメニュー2枚）
TABELOG_SENNO = 'https://tabelog.com/kyoto/A2601/A260403/26021386/'
TABELOG_SAGANO = 'https://tabelog.com/kyoto/A2601/A260403/26009893/'
JALAN_JURAKUAN = 'https://www.jalan.net/gourmet/grm_guide000000177770/'
def _g(ja, en, lat, lng):
    return {'label': {'ja': ja, 'en': en}, 'lat': lat, 'lng': lng, 'url': f'https://www.google.com/maps/search/?api=1&query={lat}%2C{lng}'}
def _l(ja, en, url):
    return {'kind': 'info', 'label': {'ja': ja, 'en': en}, 'url': {'ja': url, 'en': url}}
SENNO = {
    'id': 'senno',
    'name': {'ja': '仙翁（お昼ごはん）', 'en': 'Senno (lunch)'},
    'kind': {'ja': '喫茶店・お昼', 'en': 'Café & lunch'},
    'blurb': {'ja': '祇王寺の手前にある喫茶店。カレーが5種類とパスタがあって、奥嵯峨でお昼を食べるのにちょうどいい場所です。現金だけ。',
              'en': 'A café just before Gio-ji, with five kinds of curry and pasta: a handy place for lunch in Oku-Saga. Cash only.'},
    'lat': 35.02318, 'lng': 135.66871,
    'photos': ['senno-1.jpg', 'senno-2.jpg', 'senno-3.jpg', 'senno-4.jpg'],
    'text': {
        'ja': '\n\n'.join([
            '仙翁（せんおう）',
            '奥嵯峨は食事の店が少ないので、お昼はここで。私はビーフカレーを食べました。美味しかったです（写真は2025年10月）。',
            '店頭のメニュー（2025年10月の写真）では、カレーは欧風ビーフ、ローストスパイスビーフ、バターチキン、キーマ、チキンの5種類で、どれも税込1,300円。パスタも1,300円、ケーキは800円、コーヒーは550円からでした。1人1品の注文が必要で、支払いは現金だけです。',
            '時間と休みは、お店の公式の案内が見つかりませんでした。食べログでは9:00〜15:30、木曜休みとなっています（要確認）。',
            '休みや満席のときは、すぐ隣の「茶房さがの」へ。店頭のメニュー（2024年7月の写真）には、ビーフカレーとエビピラフが900円、スパゲティが750〜1,000円、サンドイッチ、甘味がありました。時間と休みは確認できていません（要確認）。食べログではカード・電子マネーとも不可となっているので、ここも現金で。',
            'もう1軒、化野念仏寺のほうへ150メートルほど戻ったところに「寿楽庵（じゅらくあん）」があります。じゃらんの情報では11:00〜17:00、不定休、わらびもちとお薄のセットが730円（要確認）。食事のメニューは確認できていません。',
            'おすすめ訪問時間：12:25〜13:00',
        ]),
        'en': '\n\n'.join([
            'Senno',
            'There are few places to eat in Oku-Saga, so have lunch here. I had the beef curry, and it was good (photos from October 2025).',
            'On the menu board outside (photographed in October 2025) there were five curries, European-style beef, roast spice beef, butter chicken, keema and chicken, each ¥1,300 including tax. Pasta was also ¥1,300, cakes ¥800 and coffee from ¥550. Each person needs to order one item, and it’s cash only.',
            'I couldn’t find the café’s own information on hours and closing days. Tabelog lists 9:00–15:30, closed Thursdays (please check).',
            'If it’s closed or full, try Sabo Sagano, right next door. Its menu board (photographed in July 2024) had beef curry and shrimp pilaf at ¥900, spaghetti at ¥750–1,000, sandwiches and Japanese sweets. I couldn’t confirm its hours or closing days (please check). Tabelog lists it as taking neither cards nor e-money, so bring cash here too.',
            'One more: Jurakuan, about 150 meters back toward Adashino Nenbutsu-ji. Jalan lists it as open 11:00–17:00 with irregular closing days, and a warabi-mochi and matcha set at ¥730 (please check). I couldn’t confirm what meals it serves.',
            'Recommended visit time: 12:25–13:00',
        ]),
    },
    'gmaps': [_g('仙翁', 'Senno', 35.02318, 135.66871), _g('茶房さがの', 'Sabo Sagano', 35.02337, 135.66875), _g('寿楽庵', 'Jurakuan', 35.02467, 135.66844)],
    'links': [_l('食べログ：仙翁', 'Tabelog: Senno (Japanese)', TABELOG_SENNO), _l('食べログ：茶房さがの', 'Tabelog: Sabo Sagano (Japanese)', TABELOG_SAGANO),
              _l('じゃらん：寿楽庵', 'Jalan: Jurakuan (Japanese)', JALAN_JURAKUAN)],
    'info': {
        'rows': [
            {'kind': 'hours', 'text': {'ja': '仙翁：9:00〜15:30（食べログの情報。要確認）', 'en': 'Senno: 9:00–15:30 (per Tabelog; please check)'}, 'until': None, 'from': None},
            {'kind': 'closed', 'text': {'ja': '仙翁：木曜日（食べログの情報。要確認）', 'en': 'Senno: Thursdays (per Tabelog; please check)'}, 'until': None, 'from': None},
            {'kind': 'fee', 'text': {'ja': '仙翁：カレー・パスタ 各1,300円（税込）、ケーキ800円、コーヒー550円から（2025年10月の店頭のメニュー）。現金のみ',
                                     'en': 'Senno: curry and pasta ¥1,300 each (tax incl.), cakes ¥800, coffee from ¥550 (menu board, October 2025). Cash only'}, 'until': None, 'from': None},
        ],
        'cash': True,
        'tip': {'ja': '3軒とも、お店の公式サイトや公式SNSは見つかりませんでした。値段は店頭のメニューの写真から、時間と休みは食べログ・じゃらんからです。',
                'en': 'None of the three has an official website or social account that I could find. Prices are from photos of the menu boards; hours and closing days are from Tabelog and Jalan.'},
        'checked': '2026-11-22',
        'verified': False,
        'source': '値段・1人1品・現金のみ：オーナーが撮った仙翁の店頭と店内の写真（2025-10-10）、茶房さがのの店頭の写真（2024-07-30）。時間・休み：食べログ（仙翁）、じゃらん（寿楽庵）。茶房さがのの時間は食べログにも記載なし',
    },
    'notices': [{
        'from': None, 'to': None, 'url': None,
        'head': {'ja': '現金だけです', 'en': 'Cash only'},
        'text': {'ja': '仙翁の店内に「We only accept cash」と書いてあります（2025年10月の写真）。1人1品の注文が必要です。木曜は休みのようです（要確認）。',
                 'en': 'A sign inside Senno says “We only accept cash” (photographed in October 2025). Each person needs to order one item. It seems to be closed on Thursdays (please check).'},
    }],
    'caution': {'ja': '現金だけ・木曜は休みのよう（要確認）', 'en': 'Cash only · seems closed Thursdays (please check)'},
}
TOGETSU_WINTER = {'ja': '11月〜1月は、めやすの時間（17:20ごろ）に着くともう暗くなっています。明るいうちに橋を見たい日は、{no:gioji}〜{no:jojakkoji}のお寺を1つ減らすか、嵯峨野湯を外してください。',
                  'en': 'From November to January it’s already dark at the suggested time (about 17:20). To see the bridge in daylight, drop one of the temples in {no:gioji}–{no:jojakkoji}, or skip Sagano-yu.'}

# 早朝（愛宕念仏寺の日）のバス：時刻の行・注意書きを入れ替える
EARLY_BUS = {
    'rows0': {'ja': '清滝行き：平日 7:11、7:55、8:39、9:44発／日曜・祝日 7:13、7:55、8:41、9:14、9:44発。そのあとは16:44まで毎時44分発（日曜・祝日は10:14も）',
              'en': 'For Kiyotaki: 7:11, 7:55, 8:39 and 9:44 on weekdays; 7:13, 7:55, 8:41, 9:14 and 9:44 on Sundays and holidays. After that, every hour at :44 until 16:44 (also 10:14 on Sundays and holidays)'},
    'source': '京都バス公式サイトの時刻表・運賃（阪急嵐山駅前、平日・休日の現行ダイヤ。8:39発→愛宕寺前8:50、休日8:41発→8:52）',
    'notice': {
        'from': None, 'to': None, 'url': BUS_URL,
        'head': {'ja': '乗るのは8:39（日曜・祝日は8:41）', 'en': 'Catch the 8:39 (8:41 on Sundays and holidays)'},
        'text': {'ja': '愛宕念仏寺の開門（9:00）に間に合うバスです。乗り遅れると、次は平日9:44、日曜・祝日9:14。電車を降りたら、先にのりばへ。',
                 'en': 'This is the bus that gets you to Otagi Nenbutsu-ji for its 9:00 opening. Miss it and the next is 9:44 on weekdays or 9:14 on Sundays and holidays. Go to the bus stop as soon as you get off the train.'},
    },
    'caution': {'ja': '8:39発（日曜・祝日は8:41発）。次は平日9:44', 'en': '8:39 bus (8:41 Sundays and holidays); next 9:44 on weekdays'},
}
EARLY_OTAGI_NOTICE = {
    'ja': '毎週水曜日と土曜日は入れません。その日は、一覧の上のボタンで「早朝に出発（水・土）」を選んでください。天龍寺の開門から始めるコースに変わります。',
    'en': 'The temple is closed every Wednesday and Saturday. On those days choose “Early start (Wed & Sat)” with the buttons at the top of the list: the route changes to one that starts with the opening of Tenryu-ji.',
}

# 「選んで回る」の設定（early と tenryuji。late は元のファイルのまま）。番号ではなく id で書く
PLAN = {
    'late': {
        'note': '「選んで回る」の設定。picks は自分で選ぶ場所。auto は全員共通でいつもルートに入る場所（電車・バスと、愛宕念仏寺から化野念仏寺まで坂を下る部分、帰りの先斗町。オーナーの希望 2026-11-20）。defaultMode: pick で最初から「選んで回る」、defaultPicks（最初から選ばれている場所）は1日で無理なく回れる組み合わせで、各スポットの「おすすめ◯◯時間」はこの組み合わせの時間割（2026-11-22 の見直し）。大河内山荘とモンキーパークは時間割の外の寄り道で、足したときの回り方は hints に書いてある。scripts/build_arashiyama_courses.py が作る（番号はここで付く）。',
        'picks': ['senno', 'gioji', 'nisonin', 'jojakkoji', 'okochi', 'bamboo', 'nonomiya', 'tenryuji', 'saganoyu', 'togetsukyo', 'monkey'],
        'auto': ['kawaramachi', 'katsura', 'hankyu', 'bus', 'otagi', 'toriimoto', 'adashino', 'pontocho'],
        'defaultPicks': ['senno', 'gioji', 'nisonin', 'jojakkoji', 'bamboo', 'nonomiya', 'tenryuji', 'saganoyu', 'togetsukyo'],
        'hints': [
            ('okochi', {'any': ['okochi']},
             '大河内山荘を足すと、このあとが40分ほど遅くなります（天龍寺に16:15ごろ。庭園の受付は16:50まで）。{no:gioji}〜{no:jojakkoji}のお寺を1つ外すと、もとの時間に戻ります。',
             'Adding Okochi Sanso pushes everything after it back by about 40 minutes (Tenryu-ji at about 16:15; garden last entry 16:50). Drop one of the temples in {no:gioji}–{no:jojakkoji} to get back on time.'),
            ('tenryuji', {'any': ['okochi'], 'andAny': ['tenryuji']},
             '大河内山荘に寄った日は、北門に着くのが16:15ごろ。庭園は17:00に閉まるので、建物の中（受付16:30まで）より庭を先に。',
             'After Okochi Sanso you reach the north gate at about 16:15. The garden closes at 17:00, so see the garden before the buildings (last entry 16:30).'),
            ('monkey', {'any': ['monkey'], 'andAny': ['saganoyu']},
             '嵯峨野湯に寄ると、16:00の入園に間に合いません。どちらか1つにしてください。',
             'With a stop at Sagano-yu you won’t make the 16:00 last entry. Choose one or the other.'),
            ('monkey', {'any': ['monkey'], 'andAny': ['gioji', 'nisonin', 'jojakkoji', 'okochi']},
             '入園は16:00まで。{no:gioji}〜{no:okochi}は1つだけにすると、天龍寺を15:15ごろに出て、入口に15:35ごろ着けます。2つ以上選んでいるなら、減らしてください。',
             'Last entry is 16:00. With just one of {no:gioji}–{no:okochi} you leave Tenryu-ji at about 15:15 and reach the entrance at about 15:35. If you’ve picked two or more, drop some.'),
            ('saganoyu', {'any': ['saganoyu'], 'none': ['gioji', 'nisonin', 'jojakkoji', 'okochi']},
             '{no:gioji}〜{no:okochi}を選ばない日は、お昼のあと竹林へまっすぐ下りて、天龍寺のあと14時すぎにここへ着けます。',
             'If you skip {no:gioji}–{no:okochi}, you can walk straight down to the bamboo grove after lunch and reach here soon after 14:00, following Tenryu-ji.'),
        ],
    },
    'early': {
        'note': '早朝に出発（愛宕念仏寺が開いている日）の「選んで回る」。元（9〜10時に出発）と同じ形で、時間が約55分ずつ早い。scripts/build_arashiyama_courses.py が作る。',
        'picks': ['senno', 'gioji', 'nisonin', 'jojakkoji', 'okochi', 'bamboo', 'nonomiya', 'tenryuji', 'saganoyu', 'togetsukyo', 'monkey'],
        'auto': ['kawaramachi', 'katsura', 'hankyu', 'bus', 'otagi', 'toriimoto', 'adashino', 'pontocho'],
        'defaultPicks': ['senno', 'gioji', 'nisonin', 'jojakkoji', 'bamboo', 'nonomiya', 'tenryuji', 'saganoyu', 'togetsukyo'],
        'hints': [
            ('okochi', {'any': ['okochi']},
             '大河内山荘を足すと、このあとが40分ほど遅くなります（天龍寺に15:20ごろ、渡月橋は17時すぎ）。{no:gioji}〜{no:jojakkoji}のお寺を1つ外すと、もとの時間に戻ります。',
             'Adding Okochi Sanso pushes everything after it back by about 40 minutes (Tenryu-ji at about 15:20, the bridge after 17:00). Drop one of the temples in {no:gioji}–{no:jojakkoji} to get back on time.'),
            ('monkey', {'any': ['monkey'], 'andAny': ['saganoyu']},
             '嵯峨野湯に寄ると、16:00の入園に間に合いません。どちらか1つにしてください。',
             'With a stop at Sagano-yu you won’t make the 16:00 last entry. Choose one or the other.'),
            ('monkey', {'any': ['monkey'], 'none': ['saganoyu']},
             '入園は16:00まで。嵯峨野湯を外したので、天龍寺を15:25ごろに出て、入口に15:45ごろ着けます。大河内山荘も足すなら、{no:gioji}〜{no:jojakkoji}のお寺を1つ減らしてください。',
             'Last entry is 16:00. Without Sagano-yu you leave Tenryu-ji at about 15:25 and reach the entrance at about 15:45. If you add Okochi Sanso as well, drop one of the temples in {no:gioji}–{no:jojakkoji}.'),
            ('saganoyu', {'any': ['saganoyu'], 'none': ['gioji', 'nisonin', 'jojakkoji', 'okochi']},
             '{no:gioji}〜{no:okochi}を選ばない日は、お昼のあと竹林へまっすぐ下りて、天龍寺のあと13時すぎにここへ着けます。',
             'If you skip {no:gioji}–{no:okochi}, you can walk straight down to the bamboo grove after lunch and reach here soon after 13:00, following Tenryu-ji.'),
        ],
    },
    'tenryuji': {
        'note': '早朝に出発（水・土＝愛宕念仏寺が休みの日）の「選んで回る」。天龍寺と竹林は全員共通。大河内山荘・化野念仏寺・鳥居本・嵯峨野湯は時間割の外の寄り道。scripts/build_arashiyama_courses.py が作る。',
        'picks': ['okochi', 'nonomiya', 'jojakkoji', 'nisonin', 'gioji', 'senno', 'adashino', 'toriimoto', 'saganoyu', 'togetsukyo', 'monkey'],
        'auto': ['kawaramachi', 'katsura', 'hankyu', 'tenryuji', 'bamboo', 'pontocho'],
        'defaultPicks': ['nonomiya', 'jojakkoji', 'nisonin', 'gioji', 'senno', 'togetsukyo', 'monkey'],
        'hints': [
            ('okochi', {'any': ['okochi']},
             '大河内山荘を足すと、このあとが40分ほど遅くなります（朝ごはんが10:35ごろ、お昼が13:30ごろ）。',
             'Adding Okochi Sanso pushes everything after it back by about 40 minutes (breakfast at about 10:35, lunch at about 13:30).'),
            ('adashino', {'any': ['adashino'], 'none': ['toriimoto']},
             'お昼のあとに化野念仏寺を足すと、渡月橋に着くのが15:00ごろになります。モンキーパーク（入園16:00まで）には間に合います。',
             'Adding Adashino after lunch puts you at the bridge at about 15:00. You still make the Monkey Park (last entry 16:00).'),
            ('toriimoto', {'any': ['toriimoto']},
             '鳥居本まで上ると、渡月橋に着くのは15:45ごろ。モンキーパーク（入園16:00まで）にはぎりぎりなので、どちらか1つにしてください。',
             'Going up to Toriimoto puts you at the bridge at about 15:45, cutting it very fine for the Monkey Park (last entry 16:00). Choose one or the other.'),
            ('saganoyu', {'any': ['saganoyu']},
             '嵯峨野湯に寄ると、あとが45分ほど遅くなります（モンキーパークの入口に15:25ごろ）。',
             'A stop at Sagano-yu makes the rest about 45 minutes later (Monkey Park entrance at about 15:25).'),
        ],
    },
}

SOURCES = [
    {'what': '愛宕念仏寺：9:00〜16:00、水曜・土曜休み、拝観料1,000円。タクシーはJR嵯峨嵐山駅北口から5分・およそ1,500円（公式サイトの拝観案内）', 'url': 'https://www.otagiji.com/visit-jp', 'checked': '2026-11-22'},
    {'what': '京都バス 阪急嵐山駅前発 清滝行き（現行ダイヤ）：平日 7:11・7:55・8:39・9:44…、土曜 7:13・7:55・8:41・9:44…、休日 7:13・7:55・8:41・9:14・9:44・10:14・10:44…。平日8:39発（92系統）は愛宕寺前8:50、休日8:41発は8:52。運賃230円', 'url': BUS_URL, 'checked': '2026-11-22'},
    {'what': '天龍寺：庭園 8:30〜17:00（受付16:50まで）、北門受付も同じ。2026年11月14日〜30日は特別早朝参拝で庭園受付7:30〜（北門は8:30〜）。庭園500円', 'url': 'https://www.tenryuji.com/visit/', 'checked': '2026-11-22'},
    {'what': '阪急 京都河原町→嵐山（桂で乗り換え、240円）。2026年11月24日（火）：7:50発→8:13着、8:01発→8:26着、9:04発・9:08発→9:33着。11月28日（土）：7:45発→8:07着。11月29日（日）：7:45発→8:07着、8:00発→8:23着、9:04発・9:15発→9:37着', 'url': 'https://transit.yahoo.co.jp/', 'checked': '2026-11-22'},
    {'what': '阪急 嵐山→京都河原町（桂で乗り換え）。2026年11月24日（火）：17:12発→17:37着、17:20発→17:46着。11月29日（日）：17:09発→17:33着（臨時）、17:14発→17:38着。16時台の時刻は調べていない（約25〜30分として書いた）', 'url': 'https://transit.yahoo.co.jp/', 'checked': '2026-11-22'},
    {'what': 'パンとエスプレッソと嵐山庭園「エスプレッソと」（カフェ）：8:00〜18:00、不定休。ラストオーダー・朝のメニュー・支払い方法は記載なし（公式サイトの店舗ページ）', 'url': CAFE_URL, 'checked': '2026-11-22'},
    {'what': '天龍寺 篩月（精進料理）：11:00〜14:00、木曜休み、要予約（雪は2日前まで）。予約なしでは入れないので、ルートには入れていない', 'url': 'https://www.tenryuji.com/shigetsu/', 'checked': '2026-11-22'},
    {'what': '鮎茶屋 平野屋：公式サイトのトップとお品書きに営業時間・定休日の記載なし（要確認）', 'url': 'https://ayuchaya-hiranoya.com/', 'checked': '2026-11-22'},
    {'what': '仙翁：カレー5種（欧風ビーフ・ローストスパイスビーフ・バターチキン・キーマ・チキン）各税込1,300円、パスタ1,300円、ケーキ800円、コーヒー550円〜、1人1品、現金のみ（店内の掲示「We only accept cash」）。オーナーが2025-10-10に撮った店頭のメニューと店内の写真から。公式サイト・公式SNSは見つからず（食べログにある旧ホームページのURLは404）', 'url': None, 'checked': '2026-11-22'},
    {'what': '仙翁（読みはセンオウ）：9:00〜15:30、木曜休み。食べログの情報（お店の公式情報ではない。要確認）。食べログは「カード可・電子マネー可」としているが、店内の掲示（2025年10月）は現金のみ', 'url': TABELOG_SENNO, 'checked': '2026-11-22'},
    {'what': '茶房さがの：ビーフカレー900円、エビピラフ900円、スパゲティ750〜1,000円、ミックスサンド、甘味。オーナーが2024-07-30に撮った店頭のメニューの写真から（値段は変わっている可能性あり）。営業時間・定休日は食べログにも記載なし（要確認）。食べログではカード・電子マネー・QR決済とも不可', 'url': TABELOG_SAGANO, 'checked': '2026-11-22'},
    {'what': '寿楽庵（ジュラクアン）：11時〜17時、不定休、わらびもち・お薄セット730円。じゃらんの情報（お店の公式情報ではない。要確認）。公式サイト・公式SNSは見つからず、食事のメニューと支払い方法は未確認', 'url': JALAN_JURAKUAN, 'checked': '2026-11-22'},
    {'what': '3軒の位置はオーナーが Googleマップで調べたもの（仙翁 35.02318, 135.66871／茶房さがの 35.02337, 135.66875／寿楽庵 35.02467, 135.66844）。化野念仏寺→仙翁 約10分、仙翁→祇王寺 約5分、仙翁→渡月橋 約30分は地図上の距離からのめやす', 'url': None, 'checked': '2026-11-22'},
    {'what': '歩く時間（阪急嵐山駅→天龍寺 15〜20分、野宮神社→エスプレッソと 約10分、エスプレッソと→常寂光寺 15〜20分、祇王寺→化野念仏寺 約10分、祇王寺→嵯峨野湯 約30分、鳥居本→嵐山の中心 35〜40分）は地図上の距離からのめやす。実際に歩いて測ったものではない', 'url': None, 'checked': '2026-11-22'},
]

TIME_LINE = {'ja': re.compile(r'^おすすめ(?:訪問|出発|到着|移動)時間\s*[：:]'), 'en': re.compile(r'^Recommended (?:visit|departure|arrival|travel) time\s*:')}


def nums(text, no_of):
    return re.sub(r'\{no:([a-z]+)\}', lambda m: str(no_of[m.group(1)]), text)


def set_text(spot, cid, no_of, base_no):
    sid = spot['id']
    for li, l in enumerate(('ja', 'en')):
        ps = spot['text'][l].split('\n\n')
        time_line = [p for p in ps if TIME_LINE[l].match(p)]
        # 時間の行と、このスクリプトが足した段落はいったん外す（何回実行しても増えないように）
        added = {nums(a[2 + li], base_no) for a in ADD if a[0] == sid}
        ps = [p for p in ps if not TIME_LINE[l].match(p) and p not in added]
        for s_id, starts, by in SWAP:
            if s_id != sid or cid not in by:
                continue
            hit = [i for i, p in enumerate(ps) if p.startswith(starts[l])]
            assert len(hit) == 1, (sid, cid, l, starts[l], hit)
            if by[cid] is None:
                del ps[hit[0]]
            else:
                ps[hit[0]] = nums(by[cid][l], no_of)
        ps += [nums(a[2 + li], no_of) for a in ADD if a[0] == sid and cid in a[1]]
        if cid in TIMES:
            head, ja, en = TIMES[cid][sid]
            ps.append(f'{head[0]}：{ja}' if l == 'ja' else f'{head[1]}: {en}')
        else:
            assert len(time_line) == 1, (sid, l)
            ps += time_line
        spot['text'][l] = '\n\n'.join(ps)


def build(base, cid):
    d = copy.deepcopy(base)
    by_id = {s['id']: s for s in d['spots']}
    base_no = {s['id']: s['no'] for s in base['spots']}
    keep = [by_id[i] for i in ORDER[cid]]
    no_of = {s['id']: i + 1 for i, s in enumerate(keep)}
    for s in keep:
        s['no'] = no_of[s['id']]
        set_text(s, cid, no_of, base_no)
        b = BLURB.get(cid, {}).get(s['id'])
        if b:
            s['blurb'] = {'ja': b[0], 'en': b[1]}
    d['spots'] = keep
    d['sections'] = [{'first': no_of[a], 'last': no_of[b], 'day': day} for (a, b), day in SECTIONS[cid]]
    assert d['sections'][0]['first'] == 1 and d['sections'][-1]['last'] == len(keep)
    assert all(a['last'] + 1 == b['first'] for a, b in zip(d['sections'], d['sections'][1:]))
    d['focus'] = {'first': 3, 'last': len(keep) - 1}
    sp = {s['id']: s for s in keep}

    if cid == 'early':
        bus = sp['bus']
        bus['info']['rows'][0]['text'] = copy.deepcopy(EARLY_BUS['rows0'])
        bus['info']['source'] = EARLY_BUS['source']
        bus['info']['checked'] = '2026-11-22'
        bus['notices'] = [copy.deepcopy(EARLY_BUS['notice'])]
        bus['caution'] = copy.deepcopy(EARLY_BUS['caution'])
        sp['otagi']['notices'][0]['text'] = copy.deepcopy(EARLY_OTAGI_NOTICE)
    if cid == 'tenryuji':
        # 朝ごはんのカフェ（公式サイトで営業時間を確認できた店）を、野宮神社のところに案内する
        n = sp['nonomiya']
        n['gmaps'] = n['gmaps'] + [{
            'label': {'ja': '朝ごはん：エスプレッソと', 'en': 'Breakfast: Espresso to'}, 'lat': 35.01482, 'lng': 135.67492,
            'url': 'https://www.google.com/maps/search/?api=1&query=%E3%83%91%E3%83%B3%E3%81%A8%E3%82%A8%E3%82%B9%E3%83%97%E3%83%AC%E3%83%83%E3%82%BD%E3%81%A8%E5%B5%90%E5%B1%B1%E5%BA%AD%E5%9C%92'}]
        n['links'] = n['links'] + [{'kind': 'official', 'label': {'ja': 'パンとエスプレッソと嵐山庭園「エスプレッソと」（朝ごはん）', 'en': 'Bread, Espresso & Arashiyama Garden: café (Japanese)'},
                                    'url': {'ja': CAFE_URL, 'en': CAFE_URL}}]
        n['info']['rows'] = n['info']['rows'] + [{'kind': 'hours', 'text': {'ja': '朝ごはんの「エスプレッソと」：8:00〜18:00、不定休', 'en': 'Breakfast café “Espresso to”: 8:00–18:00, irregular closing days'}, 'until': None, 'from': None}]
        n['info']['checked'] = '2026-11-22'
        n['info']['source'] = '野宮神社は2026-11-20の確認。カフェの時間はパンとエスプレッソと 公式サイト（2026-11-22）'
    if cid == 'late':
        for x in sp['togetsukyo']['notices']:
            if (x.get('head') or {}).get('ja') == '冬は17時ごろに暗くなります':
                x['text'] = {l: nums(TOGETSU_WINTER[l], no_of) for l in ('ja', 'en')}
    if cid in ('early', 'tenryuji'):
        # 「冬は17時ごろに暗くなります」（9〜10時に出発の時間割の注意）は、早いコースでは出さない
        t = sp['togetsukyo']
        t['notices'] = [x for x in t['notices'] if (x.get('head') or {}).get('ja') != '冬は17時ごろに暗くなります']
    if cid in PLAN:
        p = PLAN[cid]
        assert set(p['picks']) | set(p['auto']) == set(ORDER[cid]) and not set(p['picks']) & set(p['auto'])
        d['plan'] = {
            '_note': p['note'],
            'picks': sorted(no_of[i] for i in p['picks']),
            'auto': {str(no_of[i]): {'always': True} for i in sorted(p['auto'], key=lambda i: no_of[i])},
            'hints': [{'spot': no_of[spot], 'rule': {k: [no_of[i] for i in v] for k, v in rule.items()},
                       'text': {'ja': nums(ja, no_of), 'en': nums(en, no_of)}} for spot, rule, ja, en in p['hints']],
            'defaultMode': 'pick',
            'defaultPicks': sorted(no_of[i] for i in p['defaultPicks']),
        }
    d['course'] = cid
    return d


def main():
    base = json.load(open(BASE, encoding='utf-8'))
    spots = []
    for s in base['spots']:
        sid = s.get('id') or IDS[s['name']['ja']]
        spots.append({'no': s['no'], 'id': sid, **{k: v for k, v in s.items() if k not in ('no', 'id')}})
    # お昼の店（仙翁）を化野念仏寺のあとに入れる（何回実行しても同じ結果になるように、いったん外してから入れ直す）
    spots = [s for s in spots if s['id'] != 'senno']
    at = [s['id'] for s in spots].index('adashino') + 1
    spots[at:at] = [{'no': 0, **copy.deepcopy(SENNO)}]
    for i, s in enumerate(spots):
        s['no'] = i + 1
    base['spots'] = spots
    assert [s['id'] for s in spots] == BASE_ORDER, [s['id'] for s in spots]
    for cid, fname in COURSES:
        d = build(base, cid)
        if cid != 'late':
            d['_note'] = (f'京都 嵐山・嵯峨野マップのコース「{cid}」のデータ。scripts/build_arashiyama_courses.py が data/routes/arashiyama.json から作る。'
                          'このファイルは直接直さない（直すのは arashiyama.json かスクリプト）。')
        d['sources'] = SOURCES
        open(f'{R}/data/routes/{fname}', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
        print(fname, cid, len(d['spots']), 'spots')


if __name__ == '__main__':
    main()
