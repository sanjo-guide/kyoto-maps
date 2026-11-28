/* Page texts in Japanese and English.
   Toshi 個人のマップ。姫路・明石・須磨の1日ルート（起点は大阪の梅田〜難波のあたりのホテル）。コースは2つ：
   9〜10時に出発（late）＝須磨浦山上遊園→明石でお昼→14時半ごろの姫路城→好古園→夕暮れのお城と晩ごはん→姫路から帰る
   開城に合わせる（early）＝9:00開城の姫路城→好古園でひと休み→明石で遅いお昼→須磨浦山上遊園→舞子の夕日→舞子から帰る
   intro は共通の内容で、introFor[コース] が app.js で上書きされる（scripts/sync_himeji.py → sync_higashiyama.py）。
   Photos are [spot id, photo index]。
   時刻・料金は2026年11月22日に確認（各施設の公式サイト、電車は乗換案内）。
   このファイルは直接直してよい（データは scripts/build_himeji_data.py）。 */
window.HIMEJI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '姫路・明石・須磨 1日ルート Himeji MAP',
    titleMain: '姫路・明石・須磨',
    titleSub: 'Himeji, Akashi & Suma',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号は回る順番です。「寄り道」と書いた場所や、最初に選ばれていない場所は、時間割に入っていません。点線は順番を示す線で、実際の道ではありません。',
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
    pickNote: '最初は、時間割どおりに回れる場所が選ばれています。寄り道を足したり、行かない場所を外したりしてください。姫路駅は、姫路城・好古園・書写山のどれかを選ぶと入ります。おすすめの時間は、最初の組み合わせで回るときの目安です。',
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
    courseEarly: '開城に合わせる\n（7時半発・姫路城9:00）',
    courseLate: '9〜10時に出発\n（姫路城は14時半ごろ）',
    swMode: '回り方',
    intro: {
      "kicker": "大阪の梅田〜難波のホテルから1日",
      "favLabel": "いちばんの見どころ",
      "favName": "姫路城",
      "favText": "真っ白な大天守。中の木の階段で最上階まで上れます。昼に人が集まるので、開城の9:00か、14時半ごろに。",
      "favPhoto": [
        "himejijo",
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "お城も海も、1日で。大阪の梅田〜難波のあたりに泊まっている人向けの時間割です",
        "昼に混みやすい姫路城は、9:00の開城か14時半ごろに。出発時間でコースを選べます",
        "姫路城は一度出ると入り直せません。中は靴を脱いで、急な木の階段を上ります",
        "須磨浦山上遊園は火曜休み。12月2日〜2月5日は土日祝だけ。山の上は現金のみ",
        "明石の魚の棚は木曜に休む店が多い",
        "京都から来る人は、京都駅から新快速で姫路まで乗り換えなしの約1時間35分（2,210円）。同じ時間割で回れます"
      ],
      "dayHead": "1日の流れ（11月下旬・土曜の目安）",
      "from": "",
      "timeSuffix": "〜",
      "dealsHead": "交通費と切符",
      "deals": [
        {
          "name": "姫路城・好古園 共通券",
          "price": "2,600円",
          "best": "どちらのコースもこれ",
          "text": "姫路城だけなら2,500円（18歳以上・姫路市外）、好古園だけなら400円。18歳未満は無料。カードや交通系ICカードで払えます。日にちが決まっていれば、日時指定のデジタルチケットを90日前から買えます。",
          "url": "https://www.himejicastle.jp/"
        },
        {
          "name": "須磨浦山上遊園 回遊券（Bコース）",
          "price": "1,500円",
          "text": "ロープウェー・カーレーターの往復と回転展望閣。ふもとの窓口で買います（カードが使えるのはこの窓口だけ）。リフトもつくAコースは2,100円。",
          "url": "https://www.sumaura-yuen.jp/time_price.html"
        },
        {
          "name": "京都から来る人・京都へ帰る人",
          "price": "片道1,510〜2,210円",
          "text": "行き：開城に合わせるなら京都7:14発の新快速（平日は6:53発）で姫路へ乗り換えなし・2,210円。9〜10時発のコースは京都9:00発の新快速で三ノ宮へ行き、阪神の特急に乗り換えて須磨浦公園10:27着・1,510円。帰りの最後：姫路22:56発の新快速（京都0:30着）、舞子からは23:11発（三ノ宮で新快速に乗り換え、京都0:30着）。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日に確認しました（各施設の公式サイト、電車は乗換案内の土曜のダイヤ）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「開城に合わせる」（姫路城の9:00の開城へ）か「9〜10時に出発」（姫路城は14時半ごろ）を選びます。回る順番と時間割が変わります。"
        },
        {
          "title": "寄り道を足す・外す",
          "text": "最初は時間割どおりの場所が選ばれています。書写山 圓教寺などの寄り道は「行きたい」を押すと入ります。行かない場所は外せます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・電車の時刻・おすすめの時間が見られます。休みの日や現金だけの場所は、いちばん上に出ます。"
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
        "h1": "海の見える山の上から、明石焼、午後の白鷺城、明かりの入った天守まで。",
        "lead": "朝は須磨浦のロープウェーとカーレーターで、海を見下ろす山の上へ。床がゆっくり回る喫茶店から、須磨の海と明石海峡大橋を眺めてコーヒーを。お昼は明石の魚の棚で、だしにつけて食べる明石焼。姫路城には人の多い昼を外して14時半ごろに入り、木の階段で大天守の最上階へ。好古園を歩いて外へ出るころ、天守に明かりが入ります。ホテルを出るのは9時15分ごろ。駅前で晩ごはんを食べて、新快速で大阪へ約1時間、21時半ごろにはホテルに戻れます。",
        "day": [
          {
            "time": "10:30",
            "area": "須磨浦公園",
            "title": "ロープウェーとカーレーター",
            "text": "阪神の特急で乗り換えなし。山の上の回る喫茶店で、朝のコーヒーを。",
            "photo": [
              "suma",
              1
            ]
          },
          {
            "time": "12:20",
            "area": "明石",
            "title": "魚の棚で明石焼のお昼",
            "text": "山陽電車で21分。たこ磯で玉子焼を食べてから、昼網の魚が並ぶ市場を歩きます。",
            "photo": [
              "akashi",
              2
            ]
          },
          {
            "time": "14:25",
            "area": "姫路城",
            "title": "午後の白鷺城へ",
            "text": "新快速で24分。大天守の最上階まで上り、西の丸の長い廊下へ。",
            "photo": [
              "himejijo",
              1
            ]
          },
          {
            "time": "16:15",
            "area": "好古園",
            "title": "夕方の日本庭園",
            "text": "入園は16:30まで。12月6日までは夜まで開いていて、紅葉のライトアップがあります。",
            "photo": [
              "kokoen",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "姫路駅前",
            "title": "明かりの入った天守と晩ごはん",
            "text": "日没から天守がライトアップ。大手前通りを駅へ戻って晩ごはん。",
            "photo": [
              "himejieki",
              0
            ],
            "note": "姫路19:26発→大阪20:28着"
          }
        ],
        "dealsLead": "梅田のホテルからだと、電車は4回で3,250円（阪神 大阪梅田→須磨浦公園740円、山陽電車→山陽明石390円、JR明石→姫路660円、姫路→大阪1,460円）。入場料は別で、須磨浦の回遊券1,500円、姫路城と好古園の共通券2,600円です。"
      },
      "early": {
        "h1": "9:00の開城に合わせて白鷺城へ。そのあとは明石焼と、橋に沈む夕日。",
        "lead": "9:00の開城に合わせて姫路城へ。人が集まる前の大天守を、最上階まで上ります。好古園のレストランで庭を見ながらひと休みして、明石の魚の棚で遅めのお昼に明石焼。須磨浦のロープウェーで山の上へ上り、最後は舞子で、明石海峡大橋に沈む夕日を見ます。ホテルを出るのは7時半ごろ。朝が早いので、明石で終わりにしても十分な1日です。",
        "day": [
          {
            "time": "9:10",
            "area": "姫路城",
            "title": "開いたばかりの白鷺城へ",
            "text": "大阪7:45発の新快速で姫路8:49着。まっすぐ大天守へ上ります。",
            "photo": [
              "himejijo",
              1
            ]
          },
          {
            "time": "11:05",
            "area": "好古園",
            "title": "庭を見ながら、朝ごはん代わりの休憩",
            "text": "園内のレストランの食事は11:00から。座って休んでから庭を歩きます。",
            "photo": [
              "kokoen",
              0
            ]
          },
          {
            "time": "12:55",
            "area": "明石",
            "title": "魚の棚で遅めのお昼",
            "text": "新快速で23分。たこ磯で、だしにつけて食べる玉子焼を。",
            "photo": [
              "akashi",
              2
            ]
          },
          {
            "time": "14:30",
            "area": "須磨浦公園",
            "title": "ロープウェーとカーレーター",
            "text": "山の上の回転展望閣へ。喫茶店のラストオーダーは15:30。",
            "photo": [
              "suma",
              1
            ]
          },
          {
            "time": "16:15",
            "area": "舞子",
            "title": "明石海峡大橋に沈む夕日",
            "text": "日の入りは16:50ごろ。橋の中のプロムナードを歩いてから海ぞいへ。",
            "photo": [
              "maiko",
              0
            ],
            "note": "舞子17:33発→大阪18:22着。三ノ宮で降りて晩ごはんも"
          }
        ],
        "dealsLead": "梅田のホテルからだと、電車は5回で3,600円（JR大阪→姫路1,460円、姫路→明石660円、山陽電車 山陽明石→須磨浦公園390円、須磨浦公園→舞子公園250円、JR舞子→大阪840円）。入場料は別で、姫路城と好古園の共通券2,600円、須磨浦の回遊券1,500円です。"
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Himeji, Akashi & Suma in one day: Himeji MAP',
    titleMain: 'Himeji, Akashi & Suma',
    titleSub: '姫路・明石・須磨',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'The numbers are the order of the day. Places marked “detour”, and any not chosen to begin with, are outside the timetable. The dotted line shows the order, not the actual path.',
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
    pickNote: 'The places that fit the timetable are chosen to begin with. Add detours or drop places you will skip. Himeji Station joins your route if you pick the castle, Kokoen or Mt. Shosha. Suggested times are for the starting combination.',
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
    courseEarly: 'Castle at opening\n(leave 7:30, castle 9:00)',
    courseLate: 'Leave at 9–10\n(castle around 14:30)',
    swMode: 'How to go',
    intro: {
      "kicker": "One day from a hotel between Umeda and Namba, Osaka",
      "favLabel": "Highlight",
      "favName": "Himeji Castle",
      "favText": "The brilliant white keep; climb its wooden stairs to the top floor. It fills up around midday, so go at the 9:00 opening or around 14:30.",
      "favPhoto": [
        "himejijo",
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "A castle and the sea in one day, timed for people staying around Umeda or Namba in Osaka",
        "Himeji Castle gets busy around midday: go at the 9:00 opening or around 14:30. Pick a course by start time",
        "No re-entry at the castle. Inside: shoes off and steep wooden stairs",
        "Sumaura Sanjo Yuen: closed Tuesdays; weekends and holidays only 2 Dec – 5 Feb; cash only up top",
        "Many shops in Akashi’s Uonotana close on Thursdays",
        "From Kyoto, the Special Rapid runs direct from Kyoto Station to Himeji in about 1 h 35 min (¥2,210); the same timetable works"
      ],
      "dayHead": "One day, roughly like this (a Saturday in late November)",
      "from": "From",
      "timeSuffix": "",
      "dealsHead": "Fares and tickets",
      "deals": [
        {
          "name": "Himeji Castle + Kokoen combined ticket",
          "price": "¥2,600",
          "best": "For either course",
          "text": "Castle only ¥2,500 (18+, non-residents), Kokoen only ¥400. Free under 18. Cards and IC transit cards accepted. If your date is fixed, timed digital tickets go on sale 90 days ahead.",
          "url": "https://www.himejicastle.jp/"
        },
        {
          "name": "Sumaura Sanjo Yuen round ticket (B)",
          "price": "¥1,500",
          "text": "Ropeway and Car-rator both ways plus the revolving observatory. Buy it at the window at the bottom (the only place that takes cards). Course A with the chairlift is ¥2,100.",
          "url": "https://www.sumaura-yuen.jp/time_price.html"
        },
        {
          "name": "Coming from, or going back to, Kyoto",
          "price": "¥1,510–2,210 one way",
          "text": "Out: for the castle at opening, the 7:14 Special Rapid from Kyoto (6:53 on weekdays) runs direct to Himeji, ¥2,210. For the 9–10 o’clock course, take the 9:00 Special Rapid to Sannomiya and change to the Hanshin limited express, reaching Sumaura-koen at 10:27, ¥1,510. Last trains back: the 22:56 Special Rapid from Himeji (Kyoto 0:30); from Maiko the 23:11 (change at Sannomiya, Kyoto 0:30).",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 22, 2026 (official sites of the venues; trains on a route planner, Saturday timetable).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick a start time",
          "text": "Use the buttons above the list: “Castle at opening” (Himeji Castle at 9:00) or “Leave at 9–10” (the castle around 14:30). The order and the timetable change."
        },
        {
          "title": "Add or drop detours",
          "text": "The places that fit the timetable are chosen to begin with. Tap “Want to go” to add a detour such as Mt. Shosha Engyo-ji, or drop places you will skip."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, train times and suggested times. Closing days and cash-only places are shown at the top."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map made from Toshi’s photos and facts checked on official websites."
    },
    introFor: {
      "late": {
        "h1": "A hilltop over the sea, akashiyaki, the White Heron Castle in the afternoon, and the keep lit up at dusk.",
        "lead": "Start on the Sumaura ropeway and Car-rator, up to a hilltop over the sea, and have coffee in a café whose floor slowly turns, looking out over the Suma coast and the Akashi Kaikyo Bridge. Lunch is akashiyaki, dipped in dashi, in Akashi’s fish arcade. Enter Himeji Castle around 14:30, after the midday crowd, and climb the wooden stairs to the top of the great keep. By the time you walk out of Kokoen garden, the keep is lit. You leave your hotel around 9:15; after dinner by the station it is about an hour to Osaka by Special Rapid, and you are back around 21:30.",
        "day": [
          {
            "time": "10:30",
            "area": "Sumaura Park",
            "title": "Ropeway and Car-rator",
            "text": "Direct on the Hanshin limited express. Morning coffee in the revolving café on the hilltop.",
            "photo": [
              "suma",
              1
            ]
          },
          {
            "time": "12:20",
            "area": "Akashi",
            "title": "Akashiyaki lunch at Uonotana",
            "text": "21 minutes on the Sanyo line. Tamagoyaki at Takoiso, then the market as the midday catch arrives.",
            "photo": [
              "akashi",
              2
            ]
          },
          {
            "time": "14:25",
            "area": "Himeji Castle",
            "title": "The White Heron in the afternoon",
            "text": "24 minutes by Special Rapid. Up to the top of the keep, then the long corridor of the West Bailey.",
            "photo": [
              "himejijo",
              1
            ]
          },
          {
            "time": "16:15",
            "area": "Kokoen",
            "title": "The garden in late afternoon",
            "text": "Last entry 16:30. Until 6 December it stays open into the evening with the autumn leaves lit up.",
            "photo": [
              "kokoen",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "By Himeji Station",
            "title": "The lit keep, then dinner",
            "text": "The castle is lit from sunset. Walk back down Otemae-dori for dinner.",
            "photo": [
              "himejieki",
              0
            ],
            "note": "Himeji 19:26 → Osaka 20:28"
          }
        ],
        "dealsLead": "From a hotel in Umeda: four train rides, ¥3,250 (Hanshin Osaka-Umeda → Sumaura-koen ¥740, Sanyo → Sanyo-Akashi ¥390, JR Akashi → Himeji ¥660, Himeji → Osaka ¥1,460). Admission is extra: Sumaura round ticket ¥1,500, castle and Kokoen combined ticket ¥2,600."
      },
      "early": {
        "h1": "The White Heron Castle at its 9:00 opening, then akashiyaki and sunset at the bridge.",
        "lead": "Be at Himeji Castle for its 9:00 opening and climb the great keep to the top floor before the crowds gather. Rest at the restaurant in Kokoen garden, have akashiyaki for a late lunch in Akashi’s fish arcade, ride the Sumaura ropeway up the hill, and end at Maiko with the sun going down by the Akashi Kaikyo Bridge. You leave your hotel around 7:30. It is an early start, so stopping after Akashi still makes a full day.",
        "day": [
          {
            "time": "9:10",
            "area": "Himeji Castle",
            "title": "The castle, just opened",
            "text": "Osaka 7:45 by Special Rapid, Himeji 8:49. Go straight up the great keep.",
            "photo": [
              "himejijo",
              1
            ]
          },
          {
            "time": "11:05",
            "area": "Kokoen",
            "title": "A late breakfast by the garden",
            "text": "The restaurant inside starts meals at 11:00. Sit down first, then walk the gardens.",
            "photo": [
              "kokoen",
              0
            ]
          },
          {
            "time": "12:55",
            "area": "Akashi",
            "title": "A late lunch at Uonotana",
            "text": "23 minutes by Special Rapid. Tamagoyaki dipped in dashi at Takoiso.",
            "photo": [
              "akashi",
              2
            ]
          },
          {
            "time": "14:30",
            "area": "Sumaura Park",
            "title": "Ropeway and Car-rator",
            "text": "Up to the revolving observatory. The café takes last orders at 15:30.",
            "photo": [
              "suma",
              1
            ]
          },
          {
            "time": "16:15",
            "area": "Maiko",
            "title": "Sunset at the Akashi Kaikyo Bridge",
            "text": "Sunset is around 16:50. Walk the promenade inside the bridge, then go down to the shore.",
            "photo": [
              "maiko",
              0
            ],
            "note": "Maiko 17:33 → Osaka 18:22, or stop at Sannomiya for dinner"
          }
        ],
        "dealsLead": "From a hotel in Umeda: five train rides, ¥3,600 (JR Osaka → Himeji ¥1,460, Himeji → Akashi ¥660, Sanyo Sanyo-Akashi → Sumaura-koen ¥390, Sumaura-koen → Maiko-koen ¥250, JR Maiko → Osaka ¥840). Admission is extra: castle and Kokoen combined ticket ¥2,600, Sumaura round ticket ¥1,500."
      }
    }
  }
};
