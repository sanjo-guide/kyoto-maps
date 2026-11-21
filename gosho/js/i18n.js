/* Page texts in Japanese and English.
   Toshi 個人のマップ。朝いちばんに二条城、地下鉄で京都御苑へ。京都御所と御苑を歩き、午後は錦市場へ下る京都の中心の1日ルート。
   Photos are [spot number, photo index] from data/routes/gosho.json.
   時刻・料金は2026年11月21日に確認（各施設の公式サイト、電車は乗換案内）。 */
window.GOSHO_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都の中心 二条城と京都御所 MAP',
    titleMain: '二条城と京都御所',
    titleSub: 'Nijo Castle & Imperial Palace',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '二条城から東の京都御苑へ進み、御苑を歩いてから南の錦市場へ下ります。全部は1日に入りきらないので、「選んで回る」で行きたい場所を選んでください。',
    back: '一覧',
    close: '閉じる',
    showAll: '全体を表示',
    seeDetails: '詳しく見る',
    prevPhoto: '前の写真',
    nextPhoto: '次の写真',
    suggested: 'おすすめの時間：',
    suggestedLabel: 'めやすの時間',
    gmapsOne: 'Googleマップで開く',
    gmapsMany: 'Googleマップ：',
    copy: 'このスポットのリンクをコピー',
    copied: 'コピーしました',
    spot1Howto: 'このマップの使い方を見る',
    credit: '写真・文章：Toshi（二条城の昼・神泉苑・晴明神社・蛤御門・仙洞御所・マンガミュージアム・錦市場のアーケードの写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    bus: 'バス',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月21日',
    noticeHead: 'お知らせ',
    more: '詳しく',
    linkKinds: { official: '公式サイト', timetable: '時刻表', info: '案内' },
    nextRoute: '次のスポットへの行き方',
    locate: '現在地',
    locating: '現在地を探しています…',
    locateErr: '現在地を取得できませんでした。端末の位置情報の設定を確認してください。',
    visitOff: '行ったら印を付ける',
    visitOn: '行った！',
    progress: '{n} / {t} か所 行った',
    reset: 'リセット',
    resetAsk: 'もう一度押すと、行った印をすべて消します',
    modeAria: '回り方',
    modeAll: '全部回る',
    modePick: '選んで回る',
    pickNote: '行きたい場所の「行きたい」を押してください。時間は、二条城・京都御苑・京都御所・錦市場を中心に回る場合の目安です。寄る場所を増やしたら、そのぶん後ろにずらしてください。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたい場所を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    intro: {
      "kicker": "Toshiが歩いて作った京都の1日ルート",
      "h1": "将軍の城から、天皇の御所へ。",
      "lead": "朝いちばんに二条城の二の丸御殿を見て、地下鉄で京都御苑へ。予約なし・無料で入れる京都御所と、梅・桜・紅葉の公園を歩き、午後は錦市場へ。一年じゅう回れる、京都の真ん中の1日です。",
      "favLabel": "いちばんの見どころ",
      "favName": "京都御所の紫宸殿",
      "favText": "即位の礼が行われた正殿。朱色の承明門の柱のあいだから、正面に見えます。無料・予約なし。",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "京都がはじめてで、町の真ん中を1日で見たい人に",
        "一年じゅう回れます。梅は2月中旬〜3月中旬、桃としだれ桜は3月中旬〜4月上旬、紅葉の写真は11月23日",
        "月曜は京都御所と仙洞御所が休み。水曜はマンガミュージアムが休み",
        "冬（10〜2月）は京都御所の入場が15:20まで。午前のうちに",
        "仙洞御所は申し込みが必要で18歳以上（当日券は朝8:40から先着50人）",
        "御苑は玉砂利の道。歩きやすい靴で"
      ],
      "dayHead": "1日の流れ（目安）",
      "day": [
        {
          "time": "8:45",
          "area": "二条城",
          "title": "開城と同時に二の丸御殿へ",
          "text": "金のふすま絵と、うぐいす張りの廊下。団体が来る前の朝がいちばん静かです。",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "11:10",
          "area": "京都御苑",
          "title": "しだれ桜・桃林・梅林・蛤御門",
          "text": "地下鉄で丸太町へ。御苑の西側を、花の林を見ながら北へ歩きます。",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "11:45",
          "area": "京都御所",
          "title": "予約なしで御所の中へ",
          "text": "清所門から入り、紫宸殿、清涼殿、御池庭を約50分で。お昼は中立売休憩所で。",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "13:20",
          "area": "御苑の北側",
          "title": "もみじと松林の静かな道",
          "text": "乾御門のあたりの紅葉、近衞邸跡のしだれ桜。東へ出ると梨木神社の名水。",
          "photo": [
            6,
            0
          ]
        },
        {
          "time": "15:30",
          "area": "錦市場",
          "title": "京の台所でひと休み",
          "text": "地下鉄で四条へ。買ったものは店の前で食べて、夕暮れは先斗町と鴨川へ。",
          "note": "仙洞御所やマンガミュージアムに寄る日は16:45ごろ",
          "photo": [
            10,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費のめやす",
      "dealsLead": "地下鉄は京都→二条城前が260円、二条城前→丸太町が220円、丸太町→四条が220円で、合わせて700円。京都御苑・京都御所・仙洞御所は無料です。",
      "deals": [
        {
          "name": "二条城",
          "price": "1,300円",
          "text": "入城と二の丸御殿のセット。本丸御殿は別に1,000円（WEBチケットの予約が必要）。",
          "url": "https://nijo-jocastle.city.kyoto.lg.jp/admission/fee/"
        },
        {
          "name": "京都御所・京都御苑",
          "price": "無料",
          "text": "御所は予約なしで入れます（月曜休み）。仙洞御所も無料ですが、申し込みが必要です。",
          "url": "https://kyoto-gosho.kunaicho.go.jp/visit"
        },
        {
          "name": "京都国際マンガミュージアム",
          "price": "1,200円",
          "text": "中高生400円、小学生200円。水曜休み、最終入館16:30。",
          "url": "https://kyotomm.jp/opentime-cost/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21日に確認しました（各施設の公式サイト、電車は乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "最初は「選んで回る」",
          "text": "見どころが多いので、行きたい場所だけを選んでください。選び方に合わせて、行き方のヒントが出ます。"
        },
        {
          "title": "西から東へ、そして南へ",
          "text": "二条城から東の京都御苑へ。御苑を北まで歩いたら、地下鉄で南の錦市場へ下ります。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・電車の時刻・おすすめの時間が見られます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。",
      "from": ""
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Central Kyoto: Nijo Castle & the Imperial Palace MAP',
    titleMain: 'Nijo Castle & Imperial Palace',
    titleSub: '二条城と京都御所',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'From Nijo Castle east to the Imperial Palace Park, through the park, then south to Nishiki Market. It won’t all fit in one day, so use “Choose stops” to pick where you want to go.',
    back: 'List',
    close: 'Close',
    showAll: 'Show all',
    seeDetails: 'See details',
    prevPhoto: 'Previous photo',
    nextPhoto: 'Next photo',
    suggested: 'Suggested time: ',
    suggestedLabel: 'Rough time',
    gmapsOne: 'Open in Google Maps',
    gmapsMany: 'Google Maps: ',
    copy: 'Copy link to this spot',
    copied: 'Link copied',
    spot1Howto: 'How to use this map',
    credit: 'Photos and text: Toshi (the daytime photos of Nijo Castle and the photos of Shinsen-en, Seimei Shrine, the Hamaguri gate, the Sento Palace, the Manga Museum and the Nishiki arcade are from Wikimedia Commons; author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    bus: 'Bus',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: '21 November 2026',
    noticeHead: 'Note',
    more: 'Details',
    linkKinds: { official: 'Official site', timetable: 'Timetable', info: 'Info' },
    nextRoute: 'Directions to the next stop',
    locate: 'My location',
    locating: 'Finding your location…',
    locateErr: 'Could not get your location. Please check your location settings.',
    visitOff: 'Mark as visited',
    visitOn: 'Visited!',
    progress: '{n} of {t} visited',
    reset: 'Reset',
    resetAsk: 'Tap again to clear all visited marks',
    modeAria: 'How to go',
    modeAll: 'Full route',
    modePick: 'Choose stops',
    pickNote: 'Tap “Want to go” on the places you want to visit. Times assume a day built around Nijo Castle, the Palace park, the Palace and Nishiki Market; if you add more stops, push the later times back.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: 'Nothing chosen yet. Pick the places you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      "kicker": "A one-day Kyoto route Toshi made on foot",
      "h1": "From the shogun’s castle to the emperor’s palace.",
      "lead": "Start at opening time in the Ninomaru Palace of Nijo Castle, then take the subway to the Imperial Palace Park. Walk through the Palace (free, no booking) and a park of plum, cherry and maple, and end the afternoon at Nishiki Market. A day in the middle of Kyoto that works in any season.",
      "favLabel": "Highlight",
      "favName": "The Shishinden, Kyoto Imperial Palace",
      "favText": "The hall of enthronements, seen head-on between the vermilion pillars of the Jomeimon gate. Free, no booking.",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "First time in Kyoto and want the centre of the city in one day",
        "Good all year. Plums mid-Feb to mid-March, peach and weeping cherry mid-March to early April; the maple photos are from 23 November",
        "The Palace and the Sento Palace are closed on Mondays; the Manga Museum on Wednesdays",
        "In winter (Oct–Feb) last entry to the Palace is 15:20, so go in the morning",
        "The Sento Palace needs an application and is for ages 18+ (same-day tickets from 8:40, first 50 people)",
        "The park paths are gravel: wear comfortable shoes"
      ],
      "dayHead": "One day, roughly like this",
      "day": [
        {
          "time": "8:45",
          "area": "Nijo Castle",
          "title": "Into the Ninomaru Palace at opening time",
          "text": "Gold-leaf screens and floors that chirp underfoot. It’s quietest before the tour groups arrive.",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "11:10",
          "area": "Imperial Palace Park",
          "title": "Weeping cherry, peach and plum groves, Hamaguri gate",
          "text": "Subway to Marutamachi, then north up the west side of the park past the flowering groves.",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "11:45",
          "area": "Imperial Palace",
          "title": "Walk in without a booking",
          "text": "In by the Seishomon gate: Shishinden, Seiryoden and the pond garden in about 50 minutes. Lunch at the Nakadachiuri rest house.",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "13:20",
          "area": "North side of the park",
          "title": "Quiet paths under maples and pines",
          "text": "Maples near the Inui gate, weeping cherries at the Konoe site; out to the east, the spring water of Nashinoki Shrine.",
          "photo": [
            6,
            0
          ]
        },
        {
          "time": "15:30",
          "area": "Nishiki Market",
          "title": "A break in “Kyoto’s kitchen”",
          "text": "Subway to Shijo. Eat what you buy in front of the shop, then walk to Pontocho and the Kamo river at dusk.",
          "note": "About 16:45 if you add the Sento Palace or the Manga Museum",
          "photo": [
            10,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares",
      "dealsLead": "Subway: Kyoto → Nijojo-mae ¥260, Nijojo-mae → Marutamachi ¥220, Marutamachi → Shijo ¥220; ¥700 in all. The park, the Imperial Palace and the Sento Palace are free.",
      "deals": [
        {
          "name": "Nijo Castle",
          "price": "¥1,300",
          "text": "Castle entry with the Ninomaru Palace. The Honmaru Palace is ¥1,000 extra (timed web ticket required).",
          "url": "https://nijo-jocastle.city.kyoto.lg.jp/admission/fee/"
        },
        {
          "name": "Imperial Palace & park",
          "price": "Free",
          "text": "No booking for the Palace (closed Mondays). The Sento Palace is also free but needs an application.",
          "url": "https://kyoto-gosho.kunaicho.go.jp/en/visit"
        },
        {
          "name": "Kyoto International Manga Museum",
          "price": "¥1,200",
          "text": "Ages 12–18 ¥400, 6–12 ¥200. Closed Wednesdays; last entry 16:30.",
          "url": "https://kyotomm.jp/en/"
        }
      ],
      "dealsNote": "Adult fares and prices, checked on 21 November 2026 (official websites; trains on Yahoo! Transit).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "It opens in “Choose stops”",
          "text": "There is a lot to see, so pick only the places you want. Hints on how to get around appear to match your choice."
        },
        {
          "title": "West to east, then south",
          "text": "From Nijo Castle east to the Imperial Palace Park; walk the park up to its north end, then take the subway south to Nishiki Market."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map or “Spots” for photos, a description, prices, train times and a suggested time."
        },
        {
          "title": "Routes in Google Maps",
          "text": "“Open in Google Maps” on each spot takes you straight to route search."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi.",
      "from": "From"
    }
  }
};
