/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都から新幹線で岡山へ、岡山城・月見橋・後楽園、（吉備津神社）、倉敷美観地区を回る1日ルート
   （オーナーの写真は岡山城・月見橋・岡山駅・路面電車だけ。後楽園・吉備津神社・倉敷は行っていない場所で、写真は Wikimedia Commons）。
   Photos are [spot number, photo index] from data/routes/okayama.json.
   時刻・料金は2026年11月21日に確認（各施設の公式サイト、乗換案内）。
   intro の文章は scratchpad の okayama/scr/mk_i18n.py で書き出したもの。直すときはこのファイルを直接直してよい */
window.OKAYAMA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '岡山と倉敷 Okayama & Kurashiki MAP',
    titleMain: '岡山と倉敷',
    titleSub: 'Okayama & Kurashiki',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '午前は岡山（お城と後楽園）、午後は電車で16分の倉敷へ行く順番です。12〜2月と、後楽園が夜も開く時期は、順番を逆にしてください（1番のお知らせ）。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（後楽園・吉備津神社・倉敷の写真と、改修後の岡山城の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや時刻表で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。岡山だけ、倉敷だけの日にもできます。',
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
      "kicker": "京都から新幹線で日帰り",
      "h1": "新幹線で1時間。黒いお城と大名の庭、午後は白壁の倉敷へ。",
      "lead": "午前は岡山で、黒い天守の岡山城と、日本三名園の後楽園。午後は電車で16分の倉敷へ移って、柳の川ぞいに蔵が並ぶ美観地区を歩きます。一年じゅう行けます。先に書いておくと、新幹線の往復だけで14,280円かかり、このサイトでいちばん高い日帰りです。私が撮った写真は岡山城と岡山駅だけで、後楽園と倉敷は行ったことがなく、公式サイトなどで調べた情報と Wikimedia Commons の写真で紹介しています。",
      "favLabel": "いちばんの見どころ",
      "favName": "倉敷川の町並み",
      "favText": "柳と白壁と石の橋。店が閉まりはじめる夕方がいちばんきれいです。（写真：Suicasmo / CC BY-SA 4.0）",
      "favPhoto": [
        9,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "京都から少し遠くへ、1日で行って帰りたい人に",
        "のぞみで約1時間。自由席で片道7,140円、往復14,280円（指定席は片道8,100円前後）",
        "岡山城と後楽園は共通券800円。別々に買うと1,000円",
        "大原美術館は月曜休み、2,000円。12〜2月は15:00に閉まります",
        "川舟は1艘6人。券は昼すぎに売り切れる日が多いので、京都を出る前にWEB予約を（乗る日の30日前から）",
        "12〜2月は順番を逆に：午前に倉敷、午後に岡山",
        "入場料はカードや交通系ICカードが使えるところが多いです（岡山城・後楽園・大原美術館）",
        "よく歩きます。岡山で約3km、倉敷で約4km"
      ],
      "dayHead": "1日の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "8:41",
          "area": "岡山",
          "title": "岡山城と後楽園",
          "text": "京都7:41発ののぞみで岡山へ。路面電車で城下まで行き、岡山城、月見橋、後楽園の順に歩きます。",
          "photo": [
            5,
            0
          ]
        },
        {
          "time": "12:12",
          "area": "吉備津神社",
          "title": "（寄り道）国宝の本殿と長い廻廊",
          "text": "桃太郎の話のもとになった神社。岡山駅からJRで約15分。寄ると倉敷に着くのが2時間ほど遅くなります。（写真：hiyang.on.flickr / CC BY 2.0）",
          "photo": [
            7,
            0
          ]
        },
        {
          "time": "12:20",
          "area": "倉敷",
          "title": "白壁の町、美術館、川舟",
          "text": "お昼のあと、倉敷川ぞい、大原美術館、川舟、アイビースクエア、本町・東町、阿智神社。倉敷17:44発で岡山へ戻り、のぞみで京都へ。（写真：Suicasmo / CC BY-SA 4.0）",
          "note": "京都に19:19着",
          "photo": [
            9,
            1
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と入場料のめやす",
      "dealsLead": "全部回ると、新幹線14,280円＋岡山〜倉敷660円＋路面電車320円＋入場料3,800円（岡山城と後楽園の共通券800円、大原美術館2,000円、川舟1,000円）で、合わせて約19,000円です。お昼は別です。",
      "deals": [
        {
          "name": "新幹線 京都〜岡山",
          "price": "往復14,280円",
          "text": "のぞみ自由席で片道7,140円、約1時間。帰りを「さくら」＋新快速にすると片道6,270円。",
          "url": "https://www.jr-odekake.net/"
        },
        {
          "name": "岡山城・後楽園 共通券",
          "price": "800円",
          "text": "別々だと500円＋500円。岡山城 9:00〜17:30、後楽園 8:00〜17:00（3月20日〜9月は7:30〜18:00）。",
          "url": "https://okayama-castle.jp/guide"
        },
        {
          "name": "大原美術館",
          "price": "2,000円",
          "text": "9:00〜17:00（12〜2月は15:00まで）。月曜休み。本館、工芸・東洋館、児島虎次郎記念館に入れます。",
          "url": "https://www.ohara.or.jp/visit/"
        },
        {
          "name": "くらしき川舟流し",
          "price": "1,000円",
          "text": "約20分、30分おき。WEB予約は30日前から。当日券は9:00から倉敷館で先着順。",
          "url": "https://kankou-kurashiki.jp/special/kawafune/"
        },
        {
          "name": "路面電車",
          "price": "160円",
          "text": "岡山駅前〜城下。どこまで乗っても160円。交通系ICカードが使えます。",
          "url": "https://okayama-kido.co.jp/tram/route-map/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21日に確認しました（各施設の公式サイト、乗換案内）。岡山〜倉敷はJRで片道330円。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "番号の順に",
          "text": "1から15の順に回ると、京都駅から岡山のお城と庭、倉敷の町並みを回って京都へ帰るルートになります。7番の吉備津神社は寄り道です。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・おすすめの時間が見られます。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "「選んで回る」に切り替えると、行きたい場所だけを選べます。岡山だけ、倉敷だけにしたときの行き方も出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（岡山城と岡山駅のほかは、公式サイトなどの情報と Wikimedia Commons の写真で紹介しています）。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Okayama & Kurashiki MAP',
    titleMain: 'Okayama & Kurashiki',
    titleSub: '岡山と倉敷',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Okayama in the morning (castle and garden), then Kurashiki, 16 minutes away by train, in the afternoon. From December to February, and when Korakuen is open at night, reverse the order (see the notes at stop 1). The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (photos of Korakuen, Kibitsu Shrine and Kurashiki, and of Okayama Castle after its renovation, are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and timetables on {d}. Details can change, so please check before you go.',
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
    pickNote: 'Tap “Want to go” on the places you like. Times are for the full route. You can also make it an Okayama-only or Kurashiki-only day.',
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
      "kicker": "A day trip from Kyoto by Shinkansen",
      "h1": "An hour by Shinkansen: a black castle and a lord’s garden, then white-walled Kurashiki.",
      "lead": "The morning is Okayama: the black keep of Okayama Castle and Korakuen, one of Japan’s three great gardens. In the afternoon you move 16 minutes by train to Kurashiki and walk its old quarter of storehouses along a willow-lined canal. It works all year. Up front: the Shinkansen alone is ¥14,280 return, which makes this the most expensive day trip on this site. Only the photos of Okayama Castle and Okayama Station are mine; I have not been to Korakuen or Kurashiki, and those parts are put together from official websites and other sources, with photos from Wikimedia Commons.",
      "favLabel": "Highlight",
      "favName": "The Kurashiki canal",
      "favText": "Willows, white walls and stone bridges. Best late in the afternoon, as the shops begin to close. (Photo: Suicasmo / CC BY-SA 4.0)",
      "favPhoto": [
        9,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "For anyone who wants to go a bit further from Kyoto and still be back the same day",
        "About 1 hour by Nozomi: ¥7,140 one way unreserved, ¥14,280 return (reserved about ¥8,100 one way)",
        "Okayama Castle + Korakuen combined ticket ¥800, against ¥1,000 separately",
        "The Ohara Museum is closed on Mondays; ¥2,000. From December to February it closes at 15:00",
        "The canal boats take six people each and tickets are often gone by early afternoon: book online before you leave Kyoto (from 30 days ahead)",
        "December to February, reverse the day: Kurashiki in the morning, Okayama in the afternoon",
        "Cards and transport IC cards are accepted for admission at most places (castle, Korakuen, Ohara Museum)",
        "Plenty of walking: about 3 km in Okayama and 4 km in Kurashiki"
      ],
      "dayHead": "One day, roughly like this",
      "from": "From",
      "day": [
        {
          "time": "8:41",
          "area": "Okayama",
          "title": "Okayama Castle and Korakuen",
          "text": "The 7:41 Nozomi from Kyoto. Tram to Shiroshita, then on foot: the castle, Tsukimi bridge, Korakuen.",
          "photo": [
            5,
            0
          ]
        },
        {
          "time": "12:12",
          "area": "Kibitsu Shrine",
          "title": "(Side trip) A National Treasure hall and a long corridor",
          "text": "The shrine of the legend behind Momotaro, about 15 minutes by JR from Okayama. It puts you in Kurashiki about two hours later. (Photo: hiyang.on.flickr / CC BY 2.0)",
          "photo": [
            7,
            0
          ]
        },
        {
          "time": "12:20",
          "area": "Kurashiki",
          "title": "White walls, the museum, the boat",
          "text": "After lunch: the canal, the Ohara Museum, the boat, Ivy Square, Honmachi and Higashimachi, Achi Shrine. The 17:44 from Kurashiki back to Okayama, then a Nozomi to Kyoto. (Photo: Suicasmo / CC BY-SA 4.0)",
          "note": "Kyoto 19:19",
          "photo": [
            9,
            1
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "Doing everything: Shinkansen ¥14,280 + Okayama–Kurashiki ¥660 + tram ¥320 + admissions ¥3,800 (castle and Korakuen combined ¥800, Ohara Museum ¥2,000, boat ¥1,000) comes to about ¥19,000, before lunch.",
      "deals": [
        {
          "name": "Shinkansen Kyoto–Okayama",
          "price": "¥14,280 return",
          "text": "¥7,140 one way by Nozomi, unreserved; about 1 hour. Coming back by Sakura + Special Rapid is ¥6,270.",
          "url": "https://www.westjr.co.jp/global/en/"
        },
        {
          "name": "Castle + Korakuen combined ticket",
          "price": "¥800",
          "text": "Separately ¥500 + ¥500. Castle 9:00–17:30; Korakuen 8:00–17:00 (7:30–18:00 from 20 March to September).",
          "url": "https://okayama-castle.jp/home-en/"
        },
        {
          "name": "Ohara Museum of Art",
          "price": "¥2,000",
          "text": "9:00–17:00 (until 15:00 Dec–Feb). Closed Mondays. Covers the Main Gallery, the Craft and Asian Art Gallery and the Kojima Torajiro Memorial Hall.",
          "url": "https://www.ohara.or.jp/en/"
        },
        {
          "name": "Kurashiki river boat",
          "price": "¥1,000",
          "text": "About 20 min, every 30 min. Online booking from 30 days ahead; same-day tickets from 9:00 at Kurashiki-kan, first come first served.",
          "url": "https://kankou-kurashiki.jp/special/kawafune/"
        },
        {
          "name": "Tram",
          "price": "¥160",
          "text": "Okayama-ekimae to Shiroshita. Flat fare; transport IC cards accepted.",
          "url": "https://okayama-kido.co.jp/tram/route-map/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 21, 2026 (official websites, route planner). Okayama–Kurashiki by JR is ¥330 each way.",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "In number order",
          "text": "Follow 1 to 15: from Kyoto Station to Okayama’s castle and garden, round the old quarter of Kurashiki and back to Kyoto. Stop 7, Kibitsu Shrine, is a side trip."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees and suggested times."
        },
        {
          "title": "Skip what you like",
          "text": "Switch to “Choose stops” to pick only the places you want. It also tells you how to go if you do only Okayama or only Kurashiki."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi (apart from Okayama Castle and Okayama Station, it is put together from official websites and other sources, with photos from Wikimedia Commons)."
    }
  }
};
