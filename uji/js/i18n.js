/* Page texts in Japanese and English.
   Toshi 個人のマップ。三条から京阪電車で宇治（平等院・表参道・宇治川・宇治上神社）へ、午後から夜は伏見（寺田屋・鳥せい本店・月桂冠大倉記念館・十石舟・キザクラカッパカントリー）を回る1日ルート。
   コースは2つ：early（平等院の8:45の開門に合わせる。三条7:49発）と late（9〜10時に出発。三条9:26発）。何も選んでいないときは late。
   intro はどちらのコースにも共通の項目で、コースで変わる項目（h1・lead・who・dayHead・day）は introFor[コース] が app.js で上書きされる（scripts/sync_uji.py）。
   Photos are [spot id, photo index]（番号はコースで変わるので id で指定。紹介ページには自分の写真だけを使う）。データは data/routes/uji.json と uji-early.json。
   時刻・料金は2026年11月22日に確認（各公式サイト、電車は乗換案内）。 */
window.UJI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 宇治と伏見 Uji & Fushimi MAP',
    titleMain: '宇治と伏見',
    titleSub: 'Uji & Fushimi',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '宇治から伏見へ、京阪電車でつなぐ1日です。上のボタンで出発時間を選ぶと、時間割と順番が変わります。時間は寄り道なしで回るときの目安で、「寄り道」と書いた3か所は行く日だけ足してください。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（一部の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月21日〜23日',
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
    pickNote: '最初は、1日で回れる10か所が選ばれています。めやすの時間は、この10か所を回るときの時間割です。行かない場所は「行く」を押して外し、寄り道は「行きたい」を押して足してください。駅は自動で入ります。宇治だけ、伏見だけの半日にもできます。',
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
    swCourse: '出発時間',
    courseAria: '出発時間',
    courseEarly: '開門に合わせる\n（三条 7:49発）',
    courseLate: '9〜10時に出発\n（三条 9:26発）',
    swMode: '回り方',
    intro: {
      "kicker": "Toshiが作った1日ルート",
      "favLabel": "いちばんの見どころ",
      "favName": "平等院 鳳凰堂",
      "favText": "池の正面の岸から。午前は正面に日が当たります。中に入る券は9:10から先着順。",
      "favPhoto": [
        "byodoin",
        0
      ],
      "whoHead": "行く前に知っておきたいこと",
      "from": "",
      "timeSuffix": "〜",
      "dealsHead": "お金のめやす",
      "dealsLead": "電車は三条→京阪宇治400円、京阪宇治→中書島320円、伏見桃山→三条320円。合わせて1,040円です。お得な切符を買うほどの距離ではありません。",
      "deals": [
        {
          "name": "平等院",
          "price": "700円＋300円",
          "text": "庭園とミュージアムで700円。鳳凰堂の中に入るなら、庭園の中の受付で別に300円（現金のみ）。拝観券はカードや電子マネーも使えます。",
          "url": "https://www.byodoin.or.jp/guide/"
        },
        {
          "name": "月桂冠大倉記念館",
          "price": "600円",
          "text": "きき酒3種類とおちょこ付き。支払いはキャッシュレスだけ。",
          "url": "https://www.gekkeikan.co.jp/enjoy/museum/access/"
        },
        {
          "name": "十石舟",
          "price": "1,900円",
          "text": "約55分。空席があれば予約なしで乗れ、支払いは当日現金。3月下旬〜12月上旬。",
          "url": "https://kyoto-fushimi.or.jp/fune"
        }
      ],
      "dealsNote": "大人の料金です。2026年11月22日・23日に確認しました（各公式サイト、電車は乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「開門に合わせる」か「9〜10時に出発」を選ぶと、時間割と順番がそのコースに変わります。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・電車の時刻・おすすめの時間が見られます。"
        },
        {
          "title": "行かない場所は外す",
          "text": "最初は、1日で回れる10か所が選ばれています。「寄り道」の3か所を足したり、宇治だけ・伏見だけの半日にしたりできます。駅は自動で決まります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが歩いた場所に、まだ行けていない名所を足して作ったオリジナルマップです。"
    },
    introFor: {
      "late": {
        "h1": "平等院と抹茶のあと、酒蔵の町できき酒。夜は蔵元の店と地ビール。",
        "lead": "池の向こうに建つ平等院の鳳凰堂、表参道の抹茶、朱色の朝霧橋を渡った先の世界遺産・宇治上神社。帰り道の伏見では、月桂冠大倉記念館のきき酒、柳の川の十石舟、夜は酒蔵を使った店で焼き鳥と地ビール。三条から京阪電車で宇治へ行き、帰りに酒蔵の町で夜まで過ごす1日です。平等院の鳳凰堂の中に入る券は先着順なので、中を見たい人は、一覧の上のボタンで「開門に合わせる」を選んでください。",
        "who": [
          "三条を9:26の電車で出て、20:30ごろに戻る1日",
          "平等院の鳳凰堂の中に入る券（300円）は先着順。この時間だと遠い回か、もうないことも。中を見たい人は「開門に合わせる」へ",
          "月桂冠大倉記念館は現金が使えません。受付は16:00まで。土日は公式サイトで予約を",
          "十石舟は3月下旬〜12月上旬だけ（2026年は12月6日まで）。冬は川沿いを歩きます",
          "寺田屋の時間は公式で確かめられませんでした（要確認）。月曜は鳥せい本店、火曜はキザクラが休み",
          "お酒を飲むので、車や自転車では行かないこと"
        ],
        "dayHead": "1日の流れ（9〜10時に出発）",
        "day": [
          {
            "time": "9:59",
            "area": "宇治・平等院と表参道",
            "title": "まず内部拝観の券、それからお昼と抹茶",
            "text": "三条9:26発の京阪で宇治へ。平等院に入ったらまず券の受付へ行き、庭園とミュージアムを見ます。11:45から表参道でお昼と中村藤吉。",
            "note": "お堂の中の券は、この時間だとないことも",
            "photo": [
              "byodoin",
              1
            ]
          },
          {
            "time": "13:05",
            "area": "宇治川と宇治上神社",
            "title": "朱色の橋を渡って世界遺産の神社へ",
            "text": "塔の島から朝霧橋を渡り、宇治神社と宇治上神社へ。京阪宇治14:17発の電車で伏見へ向かいます。",
            "photo": [
              "tonoshima",
              1
            ]
          },
          {
            "time": "14:33",
            "area": "伏見・寺田屋ときき酒",
            "title": "受付の時間に間に合うように",
            "text": "中書島駅から寺田屋（14:42）、月桂冠大倉記念館（15:05、受付は16:00まで）へ。そのあと十石舟の最終便か、川沿いの散歩。",
            "note": "記念館は現金が使えません",
            "photo": [
              "gekkeikan",
              1
            ]
          },
          {
            "time": "17:25",
            "area": "伏見の夜",
            "title": "蔵元の店で焼き鳥、締めに地ビール",
            "text": "鳥せい本店で夜ごはん、歩いて2分のキザクラカッパカントリーでビール。伏見桃山20:12発で、三条に20:27。",
            "note": "月曜は鳥せい、火曜はキザクラが休み",
            "photo": [
              "torisei",
              1
            ]
          }
        ]
      },
      "early": {
        "h1": "開門の平等院へ。抹茶でひと休みして、午後は酒蔵の町。",
        "lead": "平等院が開く8:45に合わせて、三条を7:49の電車で出るコースです。鳳凰堂の中に入る券は先着順で、朝いちばんなら早い回を取りやすく、池の正面に日が当たる時間に写真が撮れます。見終わるころに表参道の中村藤吉が開くので、そこでひと休み。宇治川を渡って宇治上神社を見たら、昼に京阪電車で伏見へ。蔵元の店でお昼、月桂冠大倉記念館のきき酒、十石舟、夜はキザクラの地ビールまで。",
        "who": [
          "三条を7:49の電車で出ます。8:01発でも開門には間に合います",
          "平等院に入ったら、写真より先に内部拝観の受付へ（券は9:10から、最初の回は9:30）",
          "月桂冠大倉記念館は現金が使えません。受付は16:00まで。土日は公式サイトで予約を",
          "十石舟は3月下旬〜12月上旬だけ（2026年は12月6日まで。11月25日からは最終便15:40）",
          "寺田屋の時間は公式で確かめられませんでした（要確認）。月曜は鳥せい本店、火曜はキザクラが休み",
          "お酒を飲むので、車や自転車では行かないこと。きき酒はお昼を食べてから"
        ],
        "dayHead": "1日の流れ（開門に合わせる）",
        "day": [
          {
            "time": "8:22",
            "area": "宇治・平等院",
            "title": "8:45の開門に合わせて鳳凰堂へ",
            "text": "京阪宇治駅から宇治橋を渡って平等院へ。まず内部拝観の券を取り、池の正面から写真を。10:20から表参道の中村藤吉でひと休み。",
            "note": "三条 7:49発",
            "photo": [
              "byodoin",
              1
            ]
          },
          {
            "time": "11:10",
            "area": "宇治川と宇治上神社",
            "title": "朱色の橋を渡って世界遺産の神社へ",
            "text": "塔の島から朝霧橋を渡り、宇治神社と宇治上神社へ。京阪宇治12:28発の電車で伏見へ向かいます。",
            "photo": [
              "tonoshima",
              1
            ]
          },
          {
            "time": "12:44",
            "area": "伏見・寺田屋とお昼",
            "title": "龍馬の船宿と、蔵元の店のお昼",
            "text": "中書島駅から寺田屋へ。竜馬通りを歩いて、酒蔵を使った鳥せい本店で13:20からお昼。",
            "note": "月曜は鳥せいが休み",
            "photo": [
              "torisei",
              1
            ]
          },
          {
            "time": "14:20",
            "area": "伏見・酒蔵と十石舟",
            "title": "きき酒と、柳の川の舟",
            "text": "月桂冠大倉記念館でコイン3枚のきき酒。裏の乗り場から十石舟に乗ります。冬は川沿いを歩いて、御香宮神社へ。",
            "note": "記念館は現金が使えません",
            "photo": [
              "gekkeikan",
              1
            ]
          },
          {
            "time": "17:00",
            "area": "伏見の夜",
            "title": "酒蔵のレストランで地ビール",
            "text": "17:00に開くキザクラカッパカントリーで夜ごはん。伏見桃山18:48発で、三条に19:04。早起きした日なので、舟のあとまっすぐ帰ってもかまいません。",
            "note": "火曜はキザクラが休み",
            "photo": [
              "kizakura",
              1
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kyoto: Uji & Fushimi MAP',
    titleMain: 'Uji & Fushimi',
    titleSub: '宇治と伏見',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Uji first, then the Keihan train to Fushimi. Pick your start time with the buttons above and the timetable and order change. Times assume no detours; add the three stops marked “detour” only on days you want them. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (some photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 21–23, 2026',
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
    pickNote: 'The ten stops that fit one day start out selected, and the suggested times are the timetable for those ten. Tap “Going” to drop a place, or “Want to go” to add a detour. Stations join your route automatically. You can also make it a half day: Uji only or Fushimi only.',
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
    swCourse: 'Start time',
    courseAria: 'Start time',
    courseEarly: 'At opening time\n(7:49 from Sanjo)',
    courseLate: 'Leave at 9–10\n(9:26 from Sanjo)',
    swMode: 'Stops',
    intro: {
      "kicker": "A one-day route by Toshi",
      "favLabel": "Highlight",
      "favName": "Byodoin Phoenix Hall",
      "favText": "From the bank straight across the pond; the front is sunlit in the morning. Interior tickets from 9:10, first come, first served.",
      "favPhoto": [
        "byodoin",
        0
      ],
      "whoHead": "Good to know before you go",
      "from": "From",
      "timeSuffix": "",
      "dealsHead": "Costs",
      "dealsLead": "Trains: Sanjo → Keihan Uji ¥400, Keihan Uji → Chushojima ¥320, Fushimi-Momoyama → Sanjo ¥320: ¥1,040 in all. The distances are too short for a pass to pay off.",
      "deals": [
        {
          "name": "Byodoin",
          "price": "¥700 + ¥300",
          "text": "¥700 for the garden and museum. To go inside the Phoenix Hall, pay ¥300 more, in cash only, at the desk in the garden. The main ticket can be paid by card or e-money.",
          "url": "https://www.byodoin.or.jp/en/"
        },
        {
          "name": "Gekkeikan Okura Sake Museum",
          "price": "¥600",
          "text": "Includes three tastings and a sake cup. Cashless payment only.",
          "url": "https://www.gekkeikan.co.jp/enjoy/museum/access/"
        },
        {
          "name": "Jikkokubune boat",
          "price": "¥1,900",
          "text": "About 55 minutes. No reservation needed if seats are free; pay in cash on the day. Late March to early December.",
          "url": "https://kyoto-fushimi.or.jp/fune"
        }
      ],
      "dealsNote": "Adult prices, checked on 22–23 Nov 2026 (official sites; trains on a route planner).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick your start time",
          "text": "Use the buttons above the list to choose “At opening time” or “Leave at 9–10”. The timetable and the order change to match."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, train times and suggested times."
        },
        {
          "title": "Drop what you don’t want",
          "text": "The ten stops that fit one day start out selected. Add any of the three detours, or make it a half day of Uji only or Fushimi only. Stations follow automatically."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map: places Toshi has walked, plus the well-known sights he hasn’t reached yet."
    },
    introFor: {
      "late": {
        "h1": "Byodoin and matcha, then sake tasting in the brewery town, with dinner and craft beer to finish.",
        "lead": "Byodoin’s Phoenix Hall across its pond, matcha on the approach street, and over a vermilion bridge to World Heritage Ujigami Shrine. On the way back, Fushimi: a sake tasting at the Gekkeikan museum, a boat on the willow-lined canal, then yakitori in a converted storehouse and a craft beer. A day in Uji and, on the way home, the brewery town until evening, all by Keihan train from Sanjo. Tickets to go inside Byodoin’s Phoenix Hall are first come, first served, so if you want to see the interior choose “At opening time” with the buttons above the list.",
        "who": [
          "A day that leaves Sanjo on the 9:26 train and is back at about 20:30",
          "Phoenix Hall interior tickets (¥300) are first come, first served. At this hour you may get a late slot or none; for the interior, use “At opening time”",
          "The Gekkeikan museum takes no cash. Last entry 16:00; book online for weekends",
          "The jikkokubune boats run late March to early December only (until 6 Dec in 2026). In winter, walk the bank",
          "Teradaya’s hours could not be confirmed officially (unconfirmed). Torisei closes on Mondays, Kizakura on Tuesdays",
          "You’ll be drinking: don’t come by car or bicycle"
        ],
        "dayHead": "One day, roughly like this (leaving at 9–10)",
        "day": [
          {
            "time": "9:59",
            "area": "Uji: Byodoin & Omotesando",
            "title": "Interior ticket first, then lunch and matcha",
            "text": "The 9:26 Keihan train from Sanjo. At Byodoin go to the interior-ticket desk first, then see the garden and museum. From 11:45, lunch on Omotesando and Nakamura Tokichi.",
            "note": "Interior tickets may be gone by this hour",
            "photo": [
              "byodoin",
              1
            ]
          },
          {
            "time": "13:05",
            "area": "Uji River & Ujigami Shrine",
            "title": "Over the vermilion bridge to a World Heritage shrine",
            "text": "Cross from Tonoshima island over Asagiri Bridge to Uji Shrine and Ujigami Shrine, then take the 14:17 train from Keihan Uji to Fushimi.",
            "photo": [
              "tonoshima",
              1
            ]
          },
          {
            "time": "14:33",
            "area": "Fushimi: Teradaya & tasting",
            "title": "In time for the last entries",
            "text": "From Chushojima Station to Teradaya (14:42) and the Gekkeikan museum (15:05; last entry 16:00). Then the last jikkokubune boat, or a walk along the canal.",
            "note": "The museum takes no cash",
            "photo": [
              "gekkeikan",
              1
            ]
          },
          {
            "time": "17:25",
            "area": "Fushimi in the evening",
            "title": "Yakitori at the brewery, then a craft beer",
            "text": "Dinner at Torisei, then a beer at Kizakura Kappa Country two minutes away. The 20:12 from Fushimi-Momoyama reaches Sanjo at 20:27.",
            "note": "Torisei closes Mondays, Kizakura Tuesdays",
            "photo": [
              "torisei",
              1
            ]
          }
        ]
      },
      "early": {
        "h1": "Byodoin as it opens, a matcha break, then the brewery town.",
        "lead": "This course leaves Sanjo on the 7:49 train to be at Byodoin when it opens at 8:45. Tickets to go inside the Phoenix Hall are first come, first served; first thing in the morning you are likely to get an early slot, and you take your photo while the front of the hall is in the sun. Nakamura Tokichi on the approach street opens just as you finish, so rest there. Cross the river to Ujigami Shrine, then take the Keihan train to Fushimi at midday: lunch at a brewery restaurant, a tasting at the Gekkeikan museum, the canal boat, and craft beer at Kizakura in the evening.",
        "who": [
          "Leave Sanjo on the 7:49 train. The 8:01 still gets you there for the opening",
          "At Byodoin go to the interior-ticket desk before taking photos (tickets from 9:10, first visit 9:30)",
          "The Gekkeikan museum takes no cash. Last entry 16:00; book online for weekends",
          "The jikkokubune boats run late March to early December only (until 6 Dec in 2026; last boat 15:40 from 25 Nov)",
          "Teradaya’s hours could not be confirmed officially (unconfirmed). Torisei closes on Mondays, Kizakura on Tuesdays",
          "You’ll be drinking: don’t come by car or bicycle, and taste after lunch"
        ],
        "dayHead": "One day, roughly like this (at opening time)",
        "day": [
          {
            "time": "8:22",
            "area": "Uji: Byodoin",
            "title": "To the Phoenix Hall for the 8:45 opening",
            "text": "From Keihan Uji Station, over Uji Bridge to Byodoin. Get your interior ticket first, then take the photo across the pond. From 10:20, a break at Nakamura Tokichi on the approach street.",
            "note": "The 7:49 from Sanjo",
            "photo": [
              "byodoin",
              1
            ]
          },
          {
            "time": "11:10",
            "area": "Uji River & Ujigami Shrine",
            "title": "Over the vermilion bridge to a World Heritage shrine",
            "text": "Cross from Tonoshima island over Asagiri Bridge to Uji Shrine and Ujigami Shrine, then take the 12:28 train from Keihan Uji to Fushimi.",
            "photo": [
              "tonoshima",
              1
            ]
          },
          {
            "time": "12:44",
            "area": "Fushimi: Teradaya & lunch",
            "title": "Ryoma’s boat inn and a brewery lunch",
            "text": "From Chushojima Station to Teradaya, then up Ryoma-dori to lunch from 13:20 at Torisei, in a converted sake storehouse.",
            "note": "Torisei closes on Mondays",
            "photo": [
              "torisei",
              1
            ]
          },
          {
            "time": "14:20",
            "area": "Fushimi: breweries & the boat",
            "title": "Sake tasting and a willow-lined canal",
            "text": "Three coins, three sakes at the Gekkeikan museum, then the jikkokubune from the landing behind it. In winter, walk the bank and go on to Gokonomiya Shrine.",
            "note": "The museum takes no cash",
            "photo": [
              "gekkeikan",
              1
            ]
          },
          {
            "time": "17:00",
            "area": "Fushimi in the evening",
            "title": "Craft beer in a brewery restaurant",
            "text": "Dinner at Kizakura Kappa Country when it opens at 17:00. The 18:48 from Fushimi-Momoyama reaches Sanjo at 19:04. After the early start, heading home straight after the boat is fine too.",
            "note": "Kizakura closes on Tuesdays",
            "photo": [
              "kizakura",
              1
            ]
          }
        ]
      }
    }
  }
};
