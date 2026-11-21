/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都から日帰りの大阪：大阪城→黒門市場→法善寺横丁→道頓堀→新世界・通天閣→うめきた公園→梅田スカイビル（基本コース）と、寄り道（大阪天満宮・四天王寺・あべのハルカス・住吉大社・海遊館・中之島）。
   Photos are [spot number, photo index] from data/routes/osaka.json.
   時刻・料金は2026年11月21日に確認（各施設・大阪周遊パス・Osaka Metro の公式サイト、電車は乗換案内）。
   このファイルは scratchpad の osaka/tools/mk_i18n.py + i18n_osaka.py で作った（直すときはこのファイルを直接直してよい）。 */
window.OSAKA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から日帰り 大阪 Osaka MAP',
    titleMain: '大阪',
    titleSub: 'Osaka',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '朝の大阪城から南のミナミ・新世界へ下り、夕方に北の梅田へ戻る順番です。「寄り道」と書いた場所は、基本コースには入っていません。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（書写山 圓教寺の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
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
    pickNote: '最初は基本コースの7か所が選ばれています。寄り道を足したり、行かない場所を外したりしてください。時間は基本コースの目安です。',
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
      "kicker": "京都から電車で30〜50分",
      "h1": "大阪城から道頓堀、串カツ、夕暮れの展望台まで。大阪を1日で。",
      "lead": "朝は大阪城。昼は黒門市場と道頓堀で食べ歩き、午後は通天閣の下で串カツ。夕方に梅田へ戻って、屋根のない展望台から夕日と夜景を見て帰ります。地下鉄で3回動くだけのコースに、時間があれば足せる寄り道を6つ付けました。",
      "favLabel": "いちばんの見どころ",
      "favName": "道頓堀・戎橋",
      "favText": "グリコの看板は、橋の下の遊歩道から。昼と夜で2回見たい場所です。",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "はじめての大阪を、1日でひと通り見たい人に",
        "京都から京阪で48分（490円）、JRで28分（580円）、阪急で47分（410円）",
        "食べ歩きは現金の店が多い。千円札と小銭を",
        "展望台は1つで十分。夕日なら梅田スカイビル（日の入りの30〜40分前に）",
        "海遊館は遠いので別枠。入れるなら半日かかります"
      ],
      "dayHead": "1日の流れ（基本コースの目安）",
      "from": "",
      "day": [
        {
          "time": "9:30",
          "area": "大阪城",
          "title": "お堀と石垣、天守閣の8階へ",
          "text": "京阪の天満橋駅から歩いて大手門へ。切符売り場が混む前の9時台に天守閣へ上ります。",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "11:50",
          "area": "ミナミ",
          "title": "黒門市場と道頓堀で食べ歩き",
          "text": "黒門市場でお昼をつまみ、法善寺横丁を抜けて戎橋へ。グリコの看板とたこ焼き。",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "14:15",
          "area": "新世界",
          "title": "通天閣の下で串カツ",
          "text": "御堂筋線で動物園前へ。派手な看板の通りを歩いて、串カツを5〜6本。",
          "photo": [
            6,
            0
          ]
        },
        {
          "time": "15:50",
          "area": "梅田 → 京都",
          "title": "うめきた公園から空中庭園展望台へ",
          "text": "芝生の公園を抜けてスカイビルへ。屋上で夕日と夜景を見たら、梅田から京都へ。",
          "note": "京都着は19時ごろ",
          "photo": [
            12,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と切符",
      "dealsLead": "基本コースの電車は、京都からの往復（京阪490円＋阪急410円など）と、地下鉄3回（190円＋190円＋240円＝620円）。合わせて約1,500円です。入場料は別で、大阪城天守閣1,200円、空中庭園展望台2,000円。",
      "deals": [
        {
          "name": "京都 ⇄ 大阪（片道）",
          "price": "410〜580円",
          "text": "京阪：祇園四条→天満橋 48分・490円（大阪城に近い）。JR新快速：京都→大阪 28分・580円。阪急：京都河原町→大阪梅田 47分・410円。行きと帰りで別の会社を使ってかまいません。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "エンジョイエコカード（地下鉄1日乗車券）",
          "price": "平日820円・土日祝620円",
          "best": "土日祝はこれ",
          "text": "地下鉄とシティバスが1日乗り放題。基本コースは地下鉄3回で620円なので、土日祝は元が取れます。見せると大阪城天守閣が120円引き、空中庭園展望台とハルカス300が10%引きになるので、平日でも入場するなら得です。駅の券売機で買えます。",
          "url": "https://subway.osakametro.co.jp/guide/page/enjoy-eco.php"
        },
        {
          "name": "大阪周遊パス（1日）",
          "price": "3,500円",
          "text": "地下鉄・バスと市内の私鉄が乗り放題で、大阪城天守閣（1,200円）や通天閣（1,500円）など約40か所が無料。ただし空中庭園展望台が無料なのは15時までの入場だけで、ハルカス300と海遊館は対象外です。このコースで夕日を見るなら元は取れません。通天閣に上り、とんぼりリバークルーズにも乗る日向きです。スマホで買うQRコードの切符です。",
          "url": "https://osaka-amazing-pass.com/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21日に確認しました（Osaka Metro・大阪周遊パス・各施設の公式サイト、電車は乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "最初は基本コースの7か所",
          "text": "「選んで回る」で、大阪城・黒門市場・法善寺横丁・道頓堀・新世界・うめきた公園・スカイビルが選ばれた状態で開きます。"
        },
        {
          "title": "寄り道を足す・外す",
          "text": "大阪天満宮、四天王寺、ハルカス、住吉大社、海遊館、中之島は「行きたい」を押すと入ります。行かない場所は外せます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・地下鉄の乗り方・おすすめの時間が見られます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが歩いた写真と、公式サイトで確かめた情報で作ったオリジナルマップです。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto: Osaka MAP',
    titleMain: 'Osaka',
    titleSub: '大阪',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'From the castle in the morning, south to Minami and Shinsekai, then back north to Umeda for the evening. Places marked “detour” are not part of the basic course. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (the Mt. Shosha Engyo-ji photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 21, 2026',
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
    pickNote: 'The 7 stops of the basic course are chosen to begin with. Add detours or drop places you’ll skip. Times are for the basic course.',
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
      "kicker": "30–50 minutes by train from Kyoto",
      "h1": "The castle, Dotonbori, kushikatsu and a sunset observation deck: Osaka in one day.",
      "lead": "Osaka Castle in the morning. Eat your way through Kuromon Market and Dotonbori at midday, then kushikatsu under Tsutenkaku tower in the afternoon. Go back up to Umeda towards evening and watch the sunset and night view from an open-air rooftop before the train home. The course needs only three subway rides, with six detours to add if you have time.",
      "favLabel": "Highlight",
      "favName": "Dotonbori & Ebisubashi",
      "favText": "See the Glico sign from the riverside walk below the bridge. Worth seeing twice, by day and at night.",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "For a first visit: the main sights of Osaka in one day",
        "From Kyoto: Keihan 48 min (¥490), JR 28 min (¥580), Hankyu 47 min (¥410)",
        "Street-food stalls are often cash only: bring ¥1,000 notes and coins",
        "One observatory is enough. For sunset, the Umeda Sky Building, 30–40 minutes before",
        "The aquarium is far out west: half a day if you add it"
      ],
      "dayHead": "One day, roughly like this (basic course)",
      "from": "From",
      "day": [
        {
          "time": "9:30",
          "area": "Osaka Castle",
          "title": "Moats, stone walls and the tower’s 8th floor",
          "text": "Walk from Keihan Temmabashi Station to the Otemon gate, and go up the tower in the 9 o’clock hour before the ticket queue builds.",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "11:50",
          "area": "Minami",
          "title": "Eating through Kuromon and Dotonbori",
          "text": "Lunch on the hoof at Kuromon Market, through Hozenji Yokocho to Ebisubashi: the Glico sign and takoyaki.",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "14:15",
          "area": "Shinsekai",
          "title": "Kushikatsu under Tsutenkaku",
          "text": "Midosuji Line to Dobutsuen-mae. Walk the street of loud signs and order five or six skewers.",
          "photo": [
            6,
            0
          ]
        },
        {
          "time": "15:50",
          "area": "Umeda → Kyoto",
          "title": "Through Umekita Park to the rooftop",
          "text": "Cross the lawn park to the Sky Building, watch sunset and the night view from the roof, then take a train from Umeda.",
          "note": "Back in Kyoto about 19:00",
          "photo": [
            12,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and tickets",
      "dealsLead": "Trains for the basic course: Kyoto and back (for example Keihan ¥490 + Hankyu ¥410) and three subway rides (¥190 + ¥190 + ¥240 = ¥620), about ¥1,500 in all. Admission is extra: castle tower ¥1,200, Sky Building observatory ¥2,000.",
      "deals": [
        {
          "name": "Kyoto ⇄ Osaka (one way)",
          "price": "¥410–580",
          "text": "Keihan: Gion-Shijo → Temmabashi, 48 min, ¥490 (closest to the castle). JR Special Rapid: Kyoto → Osaka, 28 min, ¥580. Hankyu: Kyoto-Kawaramachi → Osaka-Umeda, 47 min, ¥410. You can use different lines out and back.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Enjoy Eco Card (subway 1-day ticket)",
          "price": "¥820 weekdays / ¥620 weekends & holidays",
          "best": "Best at weekends",
          "text": "Unlimited subway and city buses for a day. The basic course is three rides for ¥620, so it pays at weekends. Showing it also takes ¥120 off the castle tower and 10% off the Sky Building observatory and Harukas 300, so it is worth it on weekdays too if you go in. Sold at station ticket machines.",
          "url": "https://subway.osakametro.co.jp/guide/page/enjoy-eco.php"
        },
        {
          "name": "Osaka Amazing Pass (1 day)",
          "price": "¥3,500",
          "text": "Unlimited subway, buses and private railways in the city, plus free entry to about 40 places including the castle tower (¥1,200) and Tsutenkaku (¥1,500). But the Sky Building observatory is free only for entry until 15:00, and Harukas 300 and the aquarium are not included. If you want the sunset, it does not pay on this course. It suits a day when you also go up Tsutenkaku and take the Tombori River Cruise. It is a QR ticket bought on your phone.",
          "url": "https://osaka-amazing-pass.com/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 21, 2026 (Osaka Metro, Osaka Amazing Pass and venue websites; trains on a route planner).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Starts with the 7-stop basic course",
          "text": "It opens in “Choose stops” with the castle, Kuromon Market, Hozenji Yokocho, Dotonbori, Shinsekai, Umekita Park and the Sky Building already chosen."
        },
        {
          "title": "Add or drop detours",
          "text": "Tap “Want to go” to add Osaka Temmangu, Shitennoji, Harukas, Sumiyoshi Taisha, the aquarium or Nakanoshima. Drop any place you’ll skip."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, which subway to take and suggested times."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map made from Toshi’s own walks and photos, with facts checked on official sites."
    }
  }
};
