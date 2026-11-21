/* Page texts in Japanese and English.
   Toshi 個人のマップ。大阪（梅田〜難波のあたりのホテル）から南海電車で加太へ、友ヶ島汽船で友ヶ島（沖ノ島）へ渡る日帰りルート。
   行きの船で2コース（late＝11:00の船、early＝9:00の船）。intro は共通の内容で、introFor[コース] が app.js で上書きされる
   （scripts/sync_tomogashima.py → sync_higashiyama.py）。写真は [スポットの id, 写真の番号]。
   時刻・運賃は2026年11月22日に確認（船は友ヶ島汽船の公式サイト、島は和歌山市の公式サイト、電車は乗換案内）。 */
window.TOMOGASHIMA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '友ヶ島・加太｜大阪から日帰り Tomogashima MAP',
    titleMain: '友ヶ島・加太',
    titleSub: 'Tomogashima & Kada',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '上のボタンで行きの船を選ぶと、時間割が変わります。島の中は、桟橋から歩いて回る順番です。行かない場所は「選んで回る」で外せます。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。「要確認」と書いたものは、公式サイトに書かれていなかった情報です。行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月22日',
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
    pickNote: '行きたい場所の「行きたい」を押してください。駅・港・桟橋はいつもルートに入ります。時間は全部回る場合の目安です。',
    swCourse: '行きの船',
    courseAria: '行きの船',
    courseEarly: '9:00の船\n（なんば6:38発）',
    courseLate: '11:00の船\n（なんば8:14発）',
    swMode: '回り方',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から、島で行きたい場所を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    intro: {
      "kicker": "大阪・梅田〜難波のホテルから日帰り",
      "favLabel": "いちばんの見どころ",
      "favName": "第3砲台跡",
      "favText": "苔とつたに包まれた、レンガのアーチと暗い通路。",
      "favPhoto": [
        "dai3",
        2
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "船は1日4往復だけ。3〜12月は水曜運休、1〜2月は土日祝だけ、12/29〜1/3は運休",
        "風と波でよく欠航します（2026年11月16〜21日は、出たのは1日だけ）。朝、公式サイトの運航連絡を見てから出発",
        "予約はできません。2便目からは当日の整理券（1便100人）。支払い方法は公式サイトに書かれていないので、現金を",
        "島に水道はなく、飲み物を買えるのは桟橋のまわりだけ。お昼は、なんばで買って持っていく",
        "島の中は山道を3.3km。歩くだけで1時間20分、見て回って3時間ほど。歩きやすい靴で",
        "京都の三条からは、京阪と地下鉄でなんばへ（11:00の船なら三条6:48発。加太まで1,690円）"
      ],
      "dayHead": "1日の流れ（11月下旬・木曜の目安）",
      "from": "",
      "timeSuffix": "〜",
      "dealsHead": "交通費のめやす",
      "dealsLead": "なんばから加太まで片道1,010円、友ヶ島汽船は往復2,800円。なんばからだと、合わせて大人1人4,820円です（梅田からは地下鉄の往復480円を足して5,300円）。",
      "deals": [
        {
          "name": "南海電車（なんば↔加太）",
          "price": "片道1,010円",
          "text": "なんばから特急サザンか急行で和歌山市へ、加太線に乗り換えて約1時間40分。サザンの自由席（なんば寄りの4両）は乗車券だけで乗れます。指定席は700円。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "友ヶ島汽船（往復）",
          "price": "大人2,800円",
          "text": "加太港発 9:00・11:00・13:00・16:00、友ヶ島発 9:30・11:30・13:30・16:30。片道約20分。こども1,250円。予約はできません。",
          "url": "https://tomogashimakisen.com/main/"
        },
        {
          "name": "加太観光デジタルきっぷ（南海）",
          "price": "2,120円",
          "text": "なんば〜和歌山市の往復と、加太線の1日乗り放題。ふつうに往復すると2,020円なので、これだけでは安くなりません。サザンの往復の指定席つき（2,670円）なら、別々に買うより750円安くなります。スマホとクレジットカードで、当日は15時までに買います。船の切符は入っていません。",
          "url": "https://www.nankai.co.jp/traffic/digital/kada_kanko.html"
        },
        {
          "name": "京都から来る人・京都へ帰る人",
          "price": "三条から片道1,690円",
          "text": "行き：三条6:48発の京阪で淀屋橋へ、御堂筋線でなんば8:03着、8:14発のサザン5号に乗れます（土曜は三条6:58発の特急）。9:00の船に乗るなら三条5:04発の始発です。帰り：加太17:27発で三条に20:20ごろ。最後は、なんば23:09発 → 淀屋橋23:33発の京阪特急で三条0:22着。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃です。2026年11月22日に確認しました（船は友ヶ島汽船の公式サイト、きっぷは南海電鉄の公式サイト、電車は乗換案内の11月26日・木曜と28日・土曜のダイヤ）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "行きの船を選ぶ",
          "text": "一覧の上のボタンで「9:00の船」か「11:00の船」を選びます。電車の時刻、島を歩く時間割、帰りの船が変わります。"
        },
        {
          "title": "島の中は選べる",
          "text": "「選んで回る」に切り替えると、島で行きたい場所だけを選べます。帰りの船に間に合うように、最後の場所を出る時刻も書いてあります。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・船と電車の時刻が見られます。欠航や運休日、現金のことは、いちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。島の中は道しるべに沿って歩きましょう。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが歩いて撮った写真と、公式サイトで確かめた情報で作ったオリジナルマップです。"
    },
    introFor: {
      "late": {
        "h1": "船で渡る無人島。森の中の、レンガの砲台跡へ。",
        "lead": "なんばを8:14に出る特急で、和歌山の港町・加太へ。港で整理券をもらって淡嶋神社にお参りし、11:00の船で友ヶ島に渡ります。島では5時間。苔むしたレンガの第3砲台跡、海を見渡す展望台でお昼、白い灯台、崩れたままの第2砲台跡をゆっくり歩いて、16:30の最終便で戻ります。晩ごはんは、なんばに戻って法善寺横丁か道頓堀で。もっと早く出られる人は、一覧の上のボタンで「9:00の船」を選んでください。午後に加太でお昼と温泉の時間ができます。9〜10時にホテルを出る人は13:00の船になります（加太港のスポットに書いてあります）。",
        "day": [
          {
            "time": "8:14",
            "area": "なんば → 加太",
            "title": "特急サザンで加太へ",
            "text": "和歌山市で加太線に乗り換えて9:58着。港まで歩いて、まず11:00の船の整理券を。",
            "photo": [
              "kadaeki",
              0
            ]
          },
          {
            "time": "10:22",
            "area": "加太",
            "title": "船の前に淡嶋神社",
            "text": "港から歩いて5分。人形がびっしり並ぶ神社に、船が出るまでの20分でお参り。",
            "photo": [
              "awashima",
              0
            ]
          },
          {
            "time": "11:20",
            "area": "友ヶ島",
            "title": "第3砲台跡と、展望台でお昼",
            "text": "桟橋から山道を25分。レンガのアーチを見て、展望台で持ってきたお昼を食べます。",
            "photo": [
              "dai3",
              0
            ]
          },
          {
            "time": "13:45",
            "area": "友ヶ島の西",
            "title": "海岸・灯台・第2砲台跡",
            "text": "海岸へ下りて、白い灯台と海に崩れた砲台跡へ。15:15に桟橋へ向かいます。",
            "photo": [
              "dai2",
              0
            ],
            "note": "16:30の船で加太へ"
          },
          {
            "time": "17:27",
            "area": "加太 → なんば",
            "title": "夜はなんばで",
            "text": "なんばに18:59着。法善寺横丁と道頓堀まで歩いて5分。",
            "photo": [
              "kadaeki2",
              0
            ],
            "note": "21時ごろまで"
          }
        ]
      },
      "early": {
        "h1": "朝いちばんの船で無人島へ。午後は加太でお昼と温泉。",
        "lead": "なんばを6:38に出る急行で加太へ向かい、9:00の最初の船で友ヶ島に渡ります。人の少ないうちに第3砲台跡を見て、展望台、海岸、灯台、第2砲台跡を4時間かけて歩き、13:30の船で加太へ。遅めのお昼に加太の魚を食べ、淡嶋神社にお参りして、時間があれば温泉。なんばには18時ごろ戻って、夜は法善寺横丁か道頓堀で。あとに16:30の便が残っているので、風で予定が変わる日もいちばん安心な船です。朝はもう少しゆっくりしたい人は、一覧の上のボタンで「11:00の船」を選んでください。",
        "day": [
          {
            "time": "6:38",
            "area": "なんば → 加太",
            "title": "急行で加太へ",
            "text": "和歌山市で加太線に乗り換えて8:19着。歩いて8:40に港へ。",
            "photo": [
              "kadaeki",
              0
            ]
          },
          {
            "time": "9:20",
            "area": "友ヶ島",
            "title": "人の少ない第3砲台跡へ",
            "text": "9:00の船で島へ。桟橋から山道を25分、レンガのアーチと展望台。",
            "photo": [
              "dai3",
              0
            ]
          },
          {
            "time": "11:30",
            "area": "友ヶ島の西",
            "title": "海岸・灯台・第2砲台跡",
            "text": "海岸へ下りて、白い灯台と海に崩れた砲台跡へ。12:45に桟橋へ向かいます。",
            "photo": [
              "dai2",
              0
            ],
            "note": "13:30の船で加太へ"
          },
          {
            "time": "13:55",
            "area": "加太",
            "title": "お昼、淡嶋神社、温泉",
            "text": "加太の魚で遅めのお昼（14:30オーダーストップ）。人形の並ぶ神社は17:00まで。",
            "photo": [
              "awashima",
              0
            ]
          },
          {
            "time": "16:25",
            "area": "加太 → なんば",
            "title": "夜はなんばで",
            "text": "なんばに17:59着。法善寺横丁と道頓堀まで歩いて5分。",
            "photo": [
              "kadaeki2",
              0
            ],
            "note": "21時ごろまで"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Tomogashima & Kada: a day trip from Osaka MAP',
    titleMain: 'Tomogashima & Kada',
    titleSub: '友ヶ島・加太',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Pick your outbound boat with the buttons above and the timetable changes. On the island the order follows the trails from the pier. Use “Choose stops” to drop places you’ll skip. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Anything marked “unconfirmed” was not stated on an official site. Please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 22, 2026',
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
    pickNote: 'Tap “Want to go” on the places you like. The stations, port and pier are always on your route. Times are for the full route.',
    swCourse: 'Outbound boat',
    courseAria: 'Outbound boat',
    courseEarly: '9:00 boat\n(Namba 6:38)',
    courseLate: '11:00 boat\n(Namba 8:14)',
    swMode: 'Stops',
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: 'Nothing chosen yet. Pick the places on the island you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      "kicker": "A day trip from a hotel in Osaka (Umeda–Namba)",
      "favLabel": "Don’t miss",
      "favName": "No. 3 Battery ruins",
      "favText": "Brick arches and dark passages wrapped in moss and ivy.",
      "favPhoto": [
        "dai3",
        2
      ],
      "whoHead": "Know before you go",
      "who": [
        "Only four boats a day. None on Wednesdays (Mar–Dec); weekends and holidays only in Jan–Feb; none 29 Dec – 3 Jan",
        "Boats are often cancelled for wind and waves (16–21 Nov 2026: they ran on one day). Check the operating notice on the ferry’s website before you leave",
        "No bookings. Same-day numbered tickets from the second boat (100 people a boat). The website doesn’t say how you can pay, so bring cash",
        "No tap water on the island, and drinks are sold only by the pier. Buy your lunch in Namba and carry it",
        "The island walk is 3.3 km of hill trails: 1 h 20 min of walking, about 3 hours with stops. Wear proper shoes",
        "From Sanjo in Kyoto, take Keihan and the subway to Namba (Sanjo 6:48 for the 11:00 boat; ¥1,690 to Kada)"
      ],
      "dayHead": "One day, roughly (late November, a Thursday)",
      "from": "From",
      "timeSuffix": "",
      "dealsHead": "Fares",
      "dealsLead": "Namba to Kada is ¥1,010 each way and the Tomogashima boat is ¥2,800 return: ¥4,820 per adult from Namba (¥5,300 from Umeda with the subway, ¥480 return).",
      "deals": [
        {
          "name": "Nankai trains (Namba ↔ Kada)",
          "price": "¥1,010 one way",
          "text": "A Southern limited express or an express from Namba to Wakayamashi, then the Kada Line: about 1 h 40 min. The Southern’s unreserved cars (the four at the Namba end) need only an ordinary ticket; reserved seats are ¥700.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Tomogashima Kisen (return)",
          "price": "Adults ¥2,800",
          "text": "From Kada 9:00, 11:00, 13:00, 16:00; from the island 9:30, 11:30, 13:30, 16:30. About 20 minutes each way. Children ¥1,250. No bookings.",
          "url": "https://tomogashimakisen.com/main/"
        },
        {
          "name": "Kada Kanko Digital Ticket (Nankai)",
          "price": "¥2,120",
          "text": "A Namba–Wakayamashi return plus a day of unlimited rides on the Kada Line. An ordinary return is ¥2,020, so on its own it saves nothing; the version with reserved Southern seats both ways (¥2,670) is ¥750 cheaper than buying them separately. Bought on a phone with a credit card, by 15:00 on the day. The boat is not included.",
          "url": "https://www.nankai.co.jp/traffic/digital/kada_kanko.html"
        },
        {
          "name": "From and back to Kyoto",
          "price": "¥1,690 one way from Sanjo",
          "text": "Out: the 6:48 Keihan from Sanjo to Yodoyabashi, the Midosuji Line to Namba (8:03), then Southern 5 at 8:14 (Saturdays: the 6:58 limited express from Sanjo). For the 9:00 boat it is the first train, 5:04 from Sanjo. Back: Kada 17:27 reaches Sanjo at about 20:20. The last connection is Namba 23:09 → Keihan limited express from Yodoyabashi 23:33 → Sanjo 0:22.",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares, checked on Nov 22, 2026 (boat on the Tomogashima Kisen website, ticket on the Nankai website, trains on a route planner for Thu 26 and Sat 28 Nov).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick your boat",
          "text": "Use the buttons above the list to choose the 9:00 or the 11:00 boat. Train times, the island timetable and your boat back all change."
        },
        {
          "title": "Choose on the island",
          "text": "Switch to “Choose stops” to pick only the places you want on the island. Each course tells you when to leave the last stop to make your boat."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, for photos, tips, and boat and train times. Cancellations, no-boat days and cash come first."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions. On the island, follow the signposts."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map made from Toshi’s own photos and facts checked on official websites."
    },
    introFor: {
      "late": {
        "h1": "An uninhabited island by boat, and brick gun batteries in the woods.",
        "lead": "Leave Namba on the 8:14 limited express for the little port of Kada in Wakayama. Get your numbered ticket at the port, visit Awashima Shrine, and cross to Tomogashima on the 11:00 boat. You have five hours on the island: the moss-covered brick No. 3 Battery, lunch at a lookout over the sea, a white lighthouse and the collapsed No. 2 Battery, all at an easy pace, then the last boat back at 16:30. Dinner is back in Namba, at Hozenji Yokocho or Dotonbori. If you can start earlier, choose the 9:00 boat with the buttons above the list: it leaves you an afternoon in Kada for lunch and a hot spring. If you leave your hotel at 9–10, your boat is the 13:00 (see the Kada Port stop).",
        "day": [
          {
            "time": "8:14",
            "area": "Namba → Kada",
            "title": "The Southern express to Kada",
            "text": "Change to the Kada Line at Wakayamashi, arriving 9:58. Walk to the port and get your ticket for the 11:00 boat first.",
            "photo": [
              "kadaeki",
              0
            ]
          },
          {
            "time": "10:22",
            "area": "Kada",
            "title": "Awashima Shrine before the boat",
            "text": "Five minutes from the port: twenty minutes at the shrine packed with dolls.",
            "photo": [
              "awashima",
              0
            ]
          },
          {
            "time": "11:20",
            "area": "Tomogashima",
            "title": "No. 3 Battery, lunch at the lookout",
            "text": "25 minutes up the trail from the pier to the brick arches, then eat the lunch you brought at the lookout.",
            "photo": [
              "dai3",
              0
            ]
          },
          {
            "time": "13:45",
            "area": "West side of the island",
            "title": "Beach, lighthouse, No. 2 Battery",
            "text": "Down to the shore, the white lighthouse and the battery collapsing into the sea. Head for the pier at 15:15.",
            "photo": [
              "dai2",
              0
            ],
            "note": "16:30 boat to Kada"
          },
          {
            "time": "17:27",
            "area": "Kada → Namba",
            "title": "Evening in Namba",
            "text": "Arrive Namba 18:59. Hozenji Yokocho and Dotonbori are 5 minutes’ walk.",
            "photo": [
              "kadaeki2",
              0
            ],
            "note": "Until about 21:00"
          }
        ]
      },
      "early": {
        "h1": "The first boat to an uninhabited island, then lunch and a hot spring in Kada.",
        "lead": "Take the 6:38 express from Namba to Kada and cross to Tomogashima on the first boat at 9:00. See the No. 3 Battery before most people arrive, then the lookout, the beach, the lighthouse and the No. 2 Battery over four hours, and come back on the 13:30. A late lunch of Kada fish, Awashima Shrine, a hot spring if there is time, and you are back in Namba around 18:00 for the evening. With the 16:30 still running after you, it is also the safest boat on a day when wind changes the schedule. For a slower morning, choose the 11:00 boat with the buttons above the list.",
        "day": [
          {
            "time": "6:38",
            "area": "Namba → Kada",
            "title": "Express to Kada",
            "text": "Change to the Kada Line at Wakayamashi, arriving 8:19. Walk to the port by 8:40.",
            "photo": [
              "kadaeki",
              0
            ]
          },
          {
            "time": "9:20",
            "area": "Tomogashima",
            "title": "The No. 3 Battery, before the crowds",
            "text": "The 9:00 boat, then 25 minutes up the trail to the brick arches and the lookout.",
            "photo": [
              "dai3",
              0
            ]
          },
          {
            "time": "11:30",
            "area": "West side of the island",
            "title": "Beach, lighthouse, No. 2 Battery",
            "text": "Down to the shore, the white lighthouse and the battery collapsing into the sea. Head for the pier at 12:45.",
            "photo": [
              "dai2",
              0
            ],
            "note": "13:30 boat to Kada"
          },
          {
            "time": "13:55",
            "area": "Kada",
            "title": "Lunch, Awashima Shrine, a bath",
            "text": "A late lunch of Kada fish (last orders 14:30). The shrine of dolls is open until 17:00.",
            "photo": [
              "awashima",
              0
            ]
          },
          {
            "time": "16:25",
            "area": "Kada → Namba",
            "title": "Evening in Namba",
            "text": "Arrive Namba 17:59. Hozenji Yokocho and Dotonbori are 5 minutes’ walk.",
            "photo": [
              "kadaeki2",
              0
            ],
            "note": "Until about 21:00"
          }
        ]
      }
    }
  }
};
