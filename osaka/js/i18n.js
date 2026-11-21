/* Page texts in Japanese and English.
   Toshi 個人のマップ。大阪の1日ルート（起点は梅田〜難波のあたりのホテル）。コースは2つ：
   9〜10時に出発（late）＝黒門市場→新世界→四天王寺→15時ごろの大阪城→法善寺横丁→夜の道頓堀→淀屋橋の無料テラス
   朝早く出発（early）＝9:00の大阪城天守閣→黒門市場→新世界→四天王寺→うめきた公園→スカイビルの夕日→法善寺横丁→夜の道頓堀
   intro は共通の内容で、introFor[コース] が app.js で上書きされる（scripts/sync_osaka.py → sync_higashiyama.py）。
   Photos are [spot id, photo index]。
   時刻・料金は2026年11月22日に確認（各施設・Osaka Metro の公式サイト、電車は乗換案内）。
   このファイルは直接直してよい（データは scripts/build_osaka_data.py）。 */
window.OSAKA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: "大阪 1日ルート Osaka MAP",
    titleMain: "大阪",
    titleSub: "Osaka",
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: "番号は回る順番です。「寄り道」と書いた場所や、最初に選ばれていない場所は、時間割に入っていません。点線は順番を示す線で、実際の道ではありません。",
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
    credit: "写真・文章：Toshi（一部の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: "2026年11月22日",
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
    pickNote: "最初は、時間割どおりに回れる場所が選ばれています。寄り道を足したり、行かない場所を外したりしてください。おすすめの時間は、最初の組み合わせで回るときの目安です。",
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
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "朝早く出発\n（8時すぎ・天守閣9:00）",
    courseLate: "9〜10時に出発\n（天守閣は15時ごろ）",
    swMode: "回り方",
    intro: {
      "kicker": "梅田〜難波のホテルから1日",
      "favLabel": "いちばんの見どころ",
      "favName": "夜の道頓堀",
      "favText": "グリコの看板は、橋の下の遊歩道から。看板に明かりが入る日暮れからが本番です。",
      "favPhoto": [
        "dotonbori",
        3
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "はじめての大阪を1日で。梅田〜難波のあたりに泊まっている人向けの時間割です",
        "昼に切符の列が伸びやすい大阪城天守閣は、9:00の開館か15時ごろに。出発時間でコースを選べます",
        "食べるのは3回：黒門市場でつまむ、新世界で串カツ、夜の道頓堀でたこ焼きと晩ごはん",
        "市場と屋台は現金だけの店が多い。千円札と小銭を",
        "京都から来る人は京阪か阪急で45〜50分。帰りは、なんばを23時までに出れば間に合います"
      ],
      "dayHead": "1日の流れ（11月下旬の目安）",
      "from": "",
      "timeSuffix": "〜",
      "dealsHead": "交通費と切符",
      "deals": [
        {
          "name": "エンジョイエコカード（地下鉄1日乗車券）",
          "price": "平日820円・土日祝620円",
          "best": "どちらのコースもこれ",
          "text": "地下鉄とシティバスが1日乗り放題。どちらのコースも地下鉄に5回ほど乗って1,000円を超えるので、平日でも元が取れます。見せると大阪城天守閣が120円引き、空中庭園展望台とハルカス300が10%引き。駅の券売機で買えます。",
          "url": "https://subway.osakametro.co.jp/guide/page/enjoy-eco.php"
        },
        {
          "name": "大阪周遊パス（1日）",
          "price": "3,500円",
          "text": "地下鉄・バスと市内の私鉄が乗り放題で、大阪城天守閣（1,200円）や通天閣（1,500円）など約40か所が無料。ただし空中庭園展望台が無料なのは15時までの入場だけで、ハルカス300と海遊館は対象外です。天守閣と通天閣の両方に入り、ほかの無料の施設にも寄る日でないと元は取れません。スマホで買うQRコードの切符です。",
          "url": "https://osaka-amazing-pass.com/"
        },
        {
          "name": "京都から来る人・京都へ帰る人",
          "price": "片道410〜580円",
          "text": "行き：京阪の三条→天満橋 特急49分・490円（大阪城に近い）、三条→北浜 特急50分・490円（堺筋線に乗り換えて日本橋・黒門市場へ）。阪急の京都河原町→大阪梅田 特急43分・410円。JRの京都→大阪 新快速で約30分・580円。帰りの最後：京阪の特急は淀屋橋23:33発（三条0:22着）、阪急は大阪梅田23:45発の急行（京都河原町0:34着）、JRは大阪0:00発の新快速（京都0:30着）。なんばから淀屋橋まで6分、梅田まで8分なので、なんばを23時までに出れば間に合います。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日に確認しました（Osaka Metro と各施設の公式サイト、電車は乗換案内の土曜のダイヤ。大阪周遊パスとエンジョイエコカードの割引は11月21日の確認）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「朝早く出発」（大阪城天守閣の9:00の開館へ）か「9〜10時に出発」（天守閣は15時ごろ）を選びます。回る順番と時間割が変わります。"
        },
        {
          "title": "寄り道を足す・外す",
          "text": "最初は時間割どおりの場所が選ばれています。ハルカス、住吉大社、海遊館などは「行きたい」を押すと入ります。行かない場所は外せます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・地下鉄の乗り方・おすすめの時間が見られます。現金だけの店や休みの日は、いちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiの写真と、公式サイトで確かめた情報で作ったオリジナルマップです。"
    },
    introFor: {
      "late": {
        "h1": "市場、串カツ、15時の大阪城、そして夜の道頓堀。大阪を1日で。",
        "lead": "ホテルを9時45分ごろに出て、まず黒門市場へ。新世界で串カツを食べ、四天王寺でひと休みしてから、昼の混む時間を外して15時ごろに大阪城の天守閣へ上ります。日が暮れたら法善寺横丁と道頓堀へ。たこ焼きと晩ごはんのあと、帰り道の淀屋橋で無料の夜景を見て、21時半ごろホテルに戻ります。天守閣に開館と同時に入りたい人、夕日を展望台で見たい人は、一覧の上のボタンで「朝早く出発」を選んでください。",
        "day": [
          {
            "time": "10:10",
            "area": "日本橋",
            "title": "黒門市場でつまむ",
            "text": "昼前の歩きやすい時間に、焼きたての貝や串、果物を2〜3品。",
            "photo": [
              "kuromon",
              0
            ]
          },
          {
            "time": "11:30",
            "area": "新世界",
            "title": "通天閣の下で串カツ",
            "text": "でんでんタウンを歩いて約20分。店が開いたばかりの時間にお昼。",
            "photo": [
              "shinsekai",
              0
            ]
          },
          {
            "time": "13:10",
            "area": "四天王寺",
            "title": "静かな境内でひと休み",
            "text": "新世界から歩いて14分。五重塔を見て、池のそばのベンチで休みます。",
            "photo": [
              "shitennoji",
              0
            ]
          },
          {
            "time": "14:25",
            "area": "大阪城",
            "title": "15時ごろの天守閣へ",
            "text": "谷町線で5分。天守閣に上り、帰りは西日の当たる石垣とお堀ぞいを歩きます。",
            "photo": [
              "castle",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "ミナミ",
            "title": "法善寺横丁から夜の道頓堀へ",
            "text": "提灯の路地を抜けて戎橋へ。たこ焼き、うどんか串カツの晩ごはん、グリコの看板。",
            "photo": [
              "dotonbori",
              2
            ],
            "note": "20:30ごろまで"
          },
          {
            "time": "20:45",
            "area": "淀屋橋",
            "title": "無料のテラスで夜景",
            "text": "帰り道に、駅の真上のビルの30階へ。",
            "photo": [
              "nakanoshima",
              0
            ],
            "note": "ホテルに21:30ごろ"
          }
        ],
        "dealsLead": "梅田のホテルからだと、地下鉄は5回（240円＋190円＋240円＋190円＋190円＝1,050円）。入場料は別で、大阪城天守閣1,200円、四天王寺の中心伽藍500円です。"
      },
      "early": {
        "h1": "9:00の天守閣から、串カツ、屋上の夕日、夜の道頓堀まで。",
        "lead": "ホテルを8時10分ごろに出て、9:00の開館に合わせて大阪城の天守閣へ。切符の列が伸びる前に上ったら、黒門市場でつまみ、新世界で串カツ。四天王寺を歩いて梅田へ戻り、うめきた公園の芝生で休んでから、スカイビルの屋上で夕日を見ます。暗くなったら夜の道頓堀へ。長い1日なので、スカイビルで終わりにしてもかまいません。朝はゆっくりしたい人は、一覧の上のボタンで「9〜10時に出発」を選んでください。",
        "day": [
          {
            "time": "9:00",
            "area": "大阪城",
            "title": "開館と同時に天守閣へ",
            "text": "谷町四丁目駅から歩いて約18分。8階まで上ったら、お堀ぞいを歩いて戻ります。",
            "photo": [
              "castle",
              0
            ]
          },
          {
            "time": "11:10",
            "area": "日本橋",
            "title": "黒門市場でつまむ",
            "text": "焼きたての貝や串、果物を2〜3品。お昼は次の新世界で。",
            "photo": [
              "kuromon",
              0
            ]
          },
          {
            "time": "12:20",
            "area": "新世界",
            "title": "通天閣の下で串カツ",
            "text": "でんでんタウンを歩いて約20分。列が長ければ、先に通りを歩いてから。",
            "photo": [
              "shinsekai",
              0
            ]
          },
          {
            "time": "14:00",
            "area": "四天王寺",
            "title": "静かな境内でひと休み",
            "text": "新世界から歩いて14分。五重塔を見て、池のそばのベンチで休みます。",
            "photo": [
              "shitennoji",
              0
            ]
          },
          {
            "time": "15:30",
            "area": "梅田",
            "title": "うめきた公園からスカイビルの屋上へ",
            "text": "芝生で足を休めて、日の入りの30〜40分前に屋上へ。",
            "photo": [
              "skybldg",
              0
            ],
            "note": "夕日は16:50ごろ"
          },
          {
            "time": "18:05",
            "area": "ミナミ",
            "title": "法善寺横丁から夜の道頓堀へ",
            "text": "提灯の路地を抜けて戎橋へ。たこ焼き、うどんか串カツの晩ごはん、グリコの看板。",
            "photo": [
              "dotonbori",
              2
            ],
            "note": "21:00ごろまで"
          }
        ],
        "dealsLead": "梅田のホテルからだと、地下鉄は5回（240円＋190円＋240円＋240円＋240円＝1,150円）。入場料は別で、大阪城天守閣1,200円、四天王寺の中心伽藍500円、空中庭園展望台2,000円です。"
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: "Osaka in one day: Osaka MAP",
    titleMain: "Osaka",
    titleSub: "大阪",
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: "The numbers are the order of the day. Places marked “detour”, and any not chosen to begin with, are outside the timetable. The dotted line shows the order, not the actual path.",
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
    credit: "Photos &amp; text: Toshi (some photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: "Nov 22, 2026",
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
    pickNote: "The stops that fit the timetable are chosen to begin with. Add detours or drop places you’ll skip. Suggested times assume that starting set.",
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
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "Early start\n(8 am, tower at 9:00)",
    courseLate: "Leave at 9–10\n(tower around 15:00)",
    swMode: "Stops",
    intro: {
      "kicker": "One day from a hotel between Umeda and Namba",
      "favLabel": "Highlight",
      "favName": "Dotonbori at night",
      "favText": "See the Glico sign from the riverside walk below the bridge. It comes into its own once the signs light up at dusk.",
      "favPhoto": [
        "dotonbori",
        3
      ],
      "whoHead": "Who it’s for",
      "who": [
        "A first visit to Osaka in one day, timed for people staying between Umeda and Namba",
        "The castle tower, whose ticket queue tends to build around midday, at its 9:00 opening or at about 15:00: pick a course by start time",
        "Three rounds of eating: bites at Kuromon Market, kushikatsu in Shinsekai, takoyaki and dinner in Dotonbori at night",
        "Market stalls and street food are often cash only: bring ¥1,000 notes and coins",
        "From Kyoto it is 45–50 minutes by Keihan or Hankyu. Going back, leave Namba by 23:00"
      ],
      "dayHead": "One day, roughly like this (late November)",
      "from": "From",
      "timeSuffix": "",
      "dealsHead": "Fares and tickets",
      "deals": [
        {
          "name": "Enjoy Eco Card (subway 1-day ticket)",
          "price": "¥820 weekdays / ¥620 weekends & holidays",
          "best": "Best for both courses",
          "text": "Unlimited subway and city buses for a day. Either course means about five subway rides, over ¥1,000 in single fares, so it pays even on weekdays. Showing it also takes ¥120 off the castle tower and 10% off the Sky Building observatory and Harukas 300. Sold at station ticket machines.",
          "url": "https://subway.osakametro.co.jp/guide/page/enjoy-eco.php"
        },
        {
          "name": "Osaka Amazing Pass (1 day)",
          "price": "¥3,500",
          "text": "Unlimited subway, buses and private railways in the city, plus free entry to about 40 places including the castle tower (¥1,200) and Tsutenkaku (¥1,500). But the Sky Building observatory is free only for entry until 15:00, and Harukas 300 and the aquarium are not included. It only pays if you go into both the castle tower and Tsutenkaku and use other free facilities too. It is a QR ticket bought on your phone.",
          "url": "https://osaka-amazing-pass.com/"
        },
        {
          "name": "Coming from, or going back to, Kyoto",
          "price": "¥410–580 one way",
          "text": "Out: Keihan Sanjo → Temmabashi, limited express 49 min, ¥490 (close to the castle); Sanjo → Kitahama, 50 min, ¥490 (change to the Sakaisuji Line for Nippombashi and Kuromon Market). Hankyu Kyoto-Kawaramachi → Osaka-Umeda, limited express 43 min, ¥410. JR Kyoto → Osaka, Special Rapid about 30 min, ¥580. Last trains back: Keihan limited express from Yodoyabashi 23:33 (Sanjo 0:22); Hankyu express from Osaka-Umeda 23:45 (Kyoto-Kawaramachi 0:34); JR Special Rapid from Osaka 0:00 (Kyoto 0:30). Namba is 6 minutes from Yodoyabashi and 8 from Umeda, so leave Namba by 23:00.",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 22, 2026 (Osaka Metro and venue websites; trains on a route planner, Saturday timetable; the Osaka Amazing Pass and Enjoy Eco Card discounts were checked on Nov 21).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose a start time",
          "text": "With the buttons above the list, pick “Early start” (the castle tower at its 9:00 opening) or “Leave at 9–10” (the tower at about 15:00). The order and the timetable change."
        },
        {
          "title": "Add or drop detours",
          "text": "The stops that fit the timetable are chosen to begin with. Tap “Want to go” to add Harukas, Sumiyoshi Taisha, the aquarium and others. Drop any place you’ll skip."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, which subway to take and suggested times. Cash-only shops and closing days are shown at the top."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map made from Toshi’s photos, with facts checked on official sites."
    },
    introFor: {
      "late": {
        "h1": "A market, kushikatsu, the castle at three, then Dotonbori at night: Osaka in one day.",
        "lead": "Leave your hotel about 9:45 and start at Kuromon Market. Eat kushikatsu in Shinsekai, rest at Shitennoji, then go up the castle tower at about 15:00, after the midday crush. Once it is dark, Hozenji Yokocho and Dotonbori: takoyaki and dinner, then a free night view at Yodoyabashi on the way back, and you are at your hotel around 21:30. To be at the tower when it opens, or to watch the sunset from an observation deck, choose “Early start” with the buttons above the list.",
        "day": [
          {
            "time": "10:10",
            "area": "Nippombashi",
            "title": "Bites at Kuromon Market",
            "text": "Before the lunchtime crowd: two or three things from the grills and fruit stalls.",
            "photo": [
              "kuromon",
              0
            ]
          },
          {
            "time": "11:30",
            "area": "Shinsekai",
            "title": "Kushikatsu under Tsutenkaku",
            "text": "About 20 minutes on foot through Den Den Town. Lunch just as the shops open.",
            "photo": [
              "shinsekai",
              0
            ]
          },
          {
            "time": "13:10",
            "area": "Shitennoji",
            "title": "A rest in quiet temple grounds",
            "text": "Fourteen minutes’ walk from Shinsekai. See the pagoda, then sit by the pond.",
            "photo": [
              "shitennoji",
              0
            ]
          },
          {
            "time": "14:25",
            "area": "Osaka Castle",
            "title": "The tower at about 15:00",
            "text": "Five minutes on the Tanimachi Line. Go up the tower, then walk out along the moat in the low sun.",
            "photo": [
              "castle",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Minami",
            "title": "Hozenji Yokocho, then Dotonbori at night",
            "text": "Through the lantern-lit lane to Ebisubashi: takoyaki, udon or kushikatsu for dinner, the Glico sign.",
            "photo": [
              "dotonbori",
              2
            ],
            "note": "Until about 20:30"
          },
          {
            "time": "20:45",
            "area": "Yodoyabashi",
            "title": "A night view from a free terrace",
            "text": "On the way back, up to the 30th floor of the tower above the station.",
            "photo": [
              "nakanoshima",
              0
            ],
            "note": "At your hotel about 21:30"
          }
        ],
        "dealsLead": "From a hotel in Umeda this course is five subway rides (¥240 + ¥190 + ¥240 + ¥190 + ¥190 = ¥1,050). Admission is extra: castle tower ¥1,200, Shitennoji central precinct ¥500."
      },
      "early": {
        "h1": "The castle tower at 9:00, kushikatsu, a rooftop sunset and Dotonbori at night.",
        "lead": "Leave your hotel about 8:10 and be at the castle tower for its 9:00 opening, before the ticket queue builds. Then bites at Kuromon Market and kushikatsu in Shinsekai. Walk through Shitennoji, go back up to Umeda, rest on the lawn of Umekita Park and watch the sunset from the roof of the Sky Building. After dark, Dotonbori. It is a long day, so it is fine to finish at the Sky Building. For a slower morning, choose “Leave at 9–10” with the buttons above the list.",
        "day": [
          {
            "time": "9:00",
            "area": "Osaka Castle",
            "title": "Into the tower as it opens",
            "text": "About 18 minutes’ walk from Tanimachi 4-chome Station. Up to the 8th floor, then back along the moat.",
            "photo": [
              "castle",
              0
            ]
          },
          {
            "time": "11:10",
            "area": "Nippombashi",
            "title": "Bites at Kuromon Market",
            "text": "Two or three things from the grills and fruit stalls. Lunch proper is next.",
            "photo": [
              "kuromon",
              0
            ]
          },
          {
            "time": "12:20",
            "area": "Shinsekai",
            "title": "Kushikatsu under Tsutenkaku",
            "text": "About 20 minutes on foot through Den Den Town. If the queues are long, walk the street first.",
            "photo": [
              "shinsekai",
              0
            ]
          },
          {
            "time": "14:00",
            "area": "Shitennoji",
            "title": "A rest in quiet temple grounds",
            "text": "Fourteen minutes’ walk from Shinsekai. See the pagoda, then sit by the pond.",
            "photo": [
              "shitennoji",
              0
            ]
          },
          {
            "time": "15:30",
            "area": "Umeda",
            "title": "Umekita Park, then the Sky Building roof",
            "text": "Rest on the lawn, and go up 30–40 minutes before sunset.",
            "photo": [
              "skybldg",
              0
            ],
            "note": "Sunset about 16:50"
          },
          {
            "time": "18:05",
            "area": "Minami",
            "title": "Hozenji Yokocho, then Dotonbori at night",
            "text": "Through the lantern-lit lane to Ebisubashi: takoyaki, udon or kushikatsu for dinner, the Glico sign.",
            "photo": [
              "dotonbori",
              2
            ],
            "note": "Until about 21:00"
          }
        ],
        "dealsLead": "From a hotel in Umeda this course is five subway rides (¥240 + ¥190 + ¥240 + ¥240 + ¥240 = ¥1,150). Admission is extra: castle tower ¥1,200, Shitennoji central precinct ¥500, Sky Building observatory ¥2,000."
      }
    }
  }
};
