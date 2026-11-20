/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都から湖西線でマキノへ、海津大崎の桜並木を歩いて大崎寺・大浦へ、午後は長浜（長浜城・慶雲館・長浜鉄道スクエア・黒壁スクエア）を回る春の日帰りルート。竹生島はオーナーが行っていない場所で、写真は Wikimedia Commons。
   Photos are [spot number, photo index] from data/routes/kohoku.json.
   時刻・料金は2026年11月21日に確認（びわ湖高島観光協会・長浜の各施設・琵琶湖汽船の公式サイト、電車は乗換案内）。 */
window.KOHOKU_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から日帰り 海津大崎の桜と長浜 Kaizu-Osaki MAP',
    titleMain: '海津大崎の桜と長浜',
    titleSub: 'Kaizu-Osaki & Nagahama',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '前半はマキノから湖岸を東へ歩く海津大崎、後半は長浜の町歩きです。竹生島へは船で渡ります（大浦とは同じ日に回れません）。行かない場所は「選んで回る」で外せます。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（竹生島の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
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
    pickNote: '行きたい場所の「行きたい」を押してください。マキノ駅と長浜駅は、選んだ場所に合わせて自動で入ります。時間は竹生島に寄らない場合の目安です（竹生島は船の時刻に合わせます。大浦とは同じ日に回れません）。',
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
      "kicker": "Toshiが歩いて作った日帰りルート",
      "h1": "湖に枝をのばす桜の道を、どこまでも。",
      "lead": "春の桜のマップです。海津大崎の桜の見ごろは例年4月上旬〜中旬（びわ湖高島観光協会。満開は2024年が4月8日、2025年が4月12日）。京都から湖西線でマキノへ。琵琶湖の岸に約4km続く桜並木を歩いて、大崎寺へ。元気があれば大浦の入り江まで歩くか、船で竹生島へ。午後は秀吉の城下町・長浜で、お城と古い町並みを。",
      "favLabel": "いちばんの見どころ",
      "favName": "海津大崎の桜並木",
      "favText": "約800本の桜が、湖岸に約4km続きます。",
      "favPhoto": [
        3,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "湖と桜の景色を、ゆっくり歩いて楽しみたい人に",
        "京都からマキノまで約1時間10分（1,170円）",
        "海津大崎の桜は例年4月上旬〜中旬。見ごろの土日は交通規制あり",
        "マキノ駅で9:00から自転車を借りられます（1日1,000円・高島市内だけ）",
        "大崎寺から大浦・永原駅までは歩いて約2時間。無理せずマキノに戻っても",
        "長浜に着く14時半ごろまでお昼の時間はとっていません",
        "竹生島へは今津港13:10発の船で（3,600円＋入島料600円）。大浦とは同じ日に回れません"
      ],
      "dayHead": "1日の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "8:12",
          "area": "マキノ → 海津",
          "title": "白い砂浜と石積みの町",
          "text": "マキノ駅から知内浜へ。湖岸の石積みが続く海津の町を歩いて、桜並木の入口へ。",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "9:50",
          "area": "海津大崎",
          "title": "約4kmの桜並木",
          "text": "湖に枝をのばす桜の道を、大崎寺まで。桜クルーズの船が着く港も。",
          "photo": [
            3,
            1
          ]
        },
        {
          "time": "12:40",
          "area": "大浦 → 永原",
          "title": "静かな奥びわ湖の桜",
          "text": "湖岸の道をさらに東へ、大浦の入り江へ。永原駅から長浜へ向かいます。",
          "photo": [
            5,
            0
          ]
        },
        {
          "time": "14:35",
          "area": "長浜",
          "title": "秀吉の城下町",
          "text": "長浜城と豊公園の桜、慶雲館、旧長浜駅舎を見て、黒壁スクエアの古い町並みへ。",
          "note": "京都着は19:12",
          "photo": [
            11,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費のめやす",
      "dealsLead": "電車は京都→マキノが1,170円、永原→長浜が510円（マキノからなら680円）、長浜→京都が1,340円。合わせて約3,000円です。入館料と竹生島の船は別です。",
      "deals": [
        {
          "name": "JR（京都→マキノ）",
          "price": "片道1,170円",
          "text": "京都7:00発→近江今津で乗り換え→マキノ8:12着。新快速なら乗り換えなしで約1時間15分。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "びわ湖高島レンタサイクル",
          "price": "1日1,000円",
          "text": "マキノ駅の観光案内所で普通自転車を。9:00〜17:00、台数に限りあり。2027年5月9日までは予約できません。高島市内だけで使えます（大浦は長浜市）。",
          "url": "https://takashima-kanko.jp/guide/rentalcycle.html"
        },
        {
          "name": "琵琶湖汽船 竹生島クルーズ",
          "price": "3,600円〜",
          "text": "今津港→竹生島→長浜港のびわ湖横断が3,600円、長浜港からの往復が3,800円。入島料600円は別。2027年4月からの時刻と料金は未発表。",
          "url": "https://www.biwakokisen.co.jp/cruise/chikubu/price_time/"
        },
        {
          "name": "JR（長浜→京都）",
          "price": "1,340円",
          "text": "新快速で乗り換えなし、約1時間15分。長浜17:57発→京都19:12着、次は18:28発→京都19:42着。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21日に確認しました（びわ湖高島観光協会・長浜の各施設・琵琶湖汽船の公式サイト、電車は乗換案内）。春はダイヤが変わっていることがあります。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "最初は「選んで回る」",
          "text": "行きたい場所だけを選ぶと、駅とルートが自動で決まります。全部回るなら「すべて選ぶ」を。"
        },
        {
          "title": "前半は海津、後半は長浜",
          "text": "海津大崎だけ、長浜だけの日帰りにもできます。選んだ組み合わせに合わせて、帰り方の一言が出ます。"
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
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです（竹生島は、公式サイトの情報と Wikimedia Commons の写真で紹介しています）。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto: Kaizu-Osaki cherries & Nagahama MAP',
    titleMain: 'Kaizu-Osaki & Nagahama',
    titleSub: '海津大崎の桜と長浜',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'First Kaizu-Osaki, walking east along the lake from Makino; then a stroll around Nagahama. Chikubushima is reached by boat (not on the same day as Oura). Use “Choose stops” to drop places you’ll skip. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (the Chikubushima photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
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
    pickNote: 'Tap “Want to go” on the places you like. Makino and Nagahama stations join your route automatically. Times assume you skip Chikubushima (the island follows the boat times, and can’t be combined with Oura).',
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
      "kicker": "A day trip, hand-walked by Toshi",
      "h1": "A road of cherries reaching out over the lake.",
      "lead": "A spring cherry-blossom map. The Kaizu-Osaki cherries usually peak in early to mid April (Takashima tourism association; full bloom was 8 April in 2024 and 12 April in 2025). Take the Kosei Line from Kyoto to Makino and walk the 4 km cherry avenue along Lake Biwa to Osakiji. Then either walk on to the coves of Oura or take a boat to Chikubushima; in the afternoon, the castle and old streets of Hideyoshi’s town, Nagahama.",
      "favLabel": "Highlight",
      "favName": "Kaizu-Osaki cherry avenue",
      "favText": "About 800 cherry trees along 4 km of lakeshore.",
      "favPhoto": [
        3,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "For a long, slow walk among lake views and cherries",
        "Kyoto to Makino in about 1 h 10 min (¥1,170)",
        "Kaizu-Osaki blooms in early to mid April; peak weekends have traffic restrictions",
        "Bikes for rent at Makino Station from 9:00 (¥1,000 a day, Takashima city only)",
        "Osakiji to Oura and Nagahara Station is about 2 hours on foot; or head back to Makino",
        "No lunch stop is planned before you reach Nagahama around 14:30",
        "Chikubushima: 13:10 boat from Imazu (¥3,600 plus ¥600 island fee); not on the same day as Oura"
      ],
      "dayHead": "One day, roughly like this",
      "from": "From",
      "day": [
        {
          "time": "8:12",
          "area": "Makino → Kaizu",
          "title": "White sand and a stone-walled village",
          "text": "From Makino Station to Chinai beach, then through Kaizu along its stone embankment to the start of the avenue.",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "9:50",
          "area": "Kaizu-Osaki",
          "title": "Four kilometres of cherries",
          "text": "Walk the cherry road over the water to Osakiji, where the cherry cruises call.",
          "photo": [
            3,
            1
          ]
        },
        {
          "time": "12:40",
          "area": "Oura → Nagahara",
          "title": "Quiet cherries at the top of the lake",
          "text": "Carry on east to the coves of Oura, then take the train from Nagahara to Nagahama.",
          "photo": [
            5,
            0
          ]
        },
        {
          "time": "14:35",
          "area": "Nagahama",
          "title": "Hideyoshi’s castle town",
          "text": "Nagahama Castle and Hoko Park’s cherries, Keiunkan and the old station, then the old streets of Kurokabe Square.",
          "note": "Arrive Kyoto 19:12",
          "photo": [
            11,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares",
      "dealsLead": "Trains: Kyoto → Makino ¥1,170, Nagahara → Nagahama ¥510 (¥680 from Makino), Nagahama → Kyoto ¥1,340: about ¥3,000 in all. Admission and the Chikubushima boat are extra.",
      "deals": [
        {
          "name": "JR (Kyoto → Makino)",
          "price": "¥1,170 one way",
          "text": "Kyoto 7:00 → change at Omi-Imazu → Makino 8:12. Direct Special Rapid about 1 h 15 min.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Takashima rental bikes",
          "price": "¥1,000 a day",
          "text": "Ordinary bicycles at the tourist office in Makino Station, 9:00–17:00, limited numbers. No bookings until 9 May 2027. For use within Takashima city only (Oura is in Nagahama city).",
          "url": "https://takashima-kanko.jp/guide/rentalcycle.html"
        },
        {
          "name": "Biwako Kisen Chikubushima cruise",
          "price": "from ¥3,600",
          "text": "Imazu → island → Nagahama crossing ¥3,600; round trip from Nagahama ¥3,800. The ¥600 island fee is extra. Times and fares from April 2027 not yet announced.",
          "url": "https://www.biwakokisen.co.jp/cruise/chikubu/price_time/"
        },
        {
          "name": "JR (Nagahama → Kyoto)",
          "price": "¥1,340",
          "text": "Special Rapid, direct, about 1 h 15 min. Nagahama 17:57 → Kyoto 19:12; next 18:28 → Kyoto 19:42.",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 21, 2026 (Takashima tourism and Nagahama venues’ and Biwako Kisen’s official sites; trains on a route planner). Timetables may change by spring.",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Starts in “Choose stops”",
          "text": "Pick only the places you want; stations and the route follow automatically. To see everything, tap “Choose all”."
        },
        {
          "title": "Kaizu first, Nagahama after",
          "text": "You can also make it a Kaizu-only or Nagahama-only day; a note on getting home matches what you pick."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, train times and suggested times."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi (Chikubushima is introduced from official websites, with photos from Wikimedia Commons)."
    }
  }
};
