/* Page texts in Japanese and English.
   Toshi 個人のマップ。大雪山の日帰り：旭岳と層雲峡（旭川から）。旭川駅のまわりのホテルを9〜10時に出て、バスで往復する1日。
   コースは2つ（一覧の上のボタン）：asahidake＝旭岳（最初に開く。data/routes/daisetsuzan.json）、sounkyo＝層雲峡（daisetsuzan-sounkyo.json）。
   intro はどちらのコースにも共通の項目で、コースで変わる項目は introFor[コース] が app.js で上書きされる（scripts/sync_daisetsuzan.py）。
   写真は [スポットの id, 写真の番号]。今は Wikimedia Commons の写真だけ（行った・食べたと書かない）。
   時刻・料金は2026年11月28日に確認（出典は data/routes/daisetsuzan*.json の sources）。直すときはこのファイルを直接直してよい */
window.DAISETSUZAN_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '大雪山の日帰り：旭岳と層雲峡 Daisetsuzan day trips from Asahikawa MAP',
    titleMain: '大雪山の日帰り',
    titleSub: 'Daisetsuzan day trips from Asahikawa',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号は回る順番です。上のボタンで、旭岳か層雲峡を選びます。最初は、時間割どおりに回れる場所が選ばれています。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '文章：Toshi（写真はすべて Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    bus: 'バス',
    closed: '休み',
    tattoo: 'タトゥー',
    food: '食事',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや公式の時刻表で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月28日',
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
    pickNote: '最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。旭川からのバスは、自動で入ります。',
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
    swCourse: '行き先',
    courseAria: '行き先',
    courseAsahidake: '旭岳\n（バス1時間48分）',
    courseSounkyo: '層雲峡\n（バス約2時間）',
    swMode: '回り方',
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "交通費・料金",
      "dealsMore": "公式サイトで見る",
      "dealsNote": "大人1人の金額です。2026年11月28日に、バス会社・ロープウェイ・各施設の公式サイトと乗換案内（12月3日・5日のダイヤ）で確認しました。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "行き先を選ぶ",
          "text": "一覧の上のボタンで「旭岳」か「層雲峡」を選びます。時間割と番号が変わります。1日で両方は回れません。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられます（東川の町、大函、氷瀑まつり）。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、最終バス・ロープウェイの運休・冬の服装・タトゥーの決まりなど、現地で困ることが先に出ます。時刻と料金は、その下にあります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（写真はまだ Wikimedia Commons のものだけで、公式サイトなどの情報をもとに紹介しています）。"
    },
    introFor: {
      "asahidake": {
        "kicker": "旭川から日帰り・一年中（ロープウェイの整備運休を除く）",
        "h1": "噴気を上げる、北海道でいちばん高い山の正面へ。",
        "lead": "標高1,600mの姿見駅を出ると、目の前に噴気を上げる旭岳（あさひだけ）。夏は姿見の池を一周、冬は晴れた日にスノーシューで歩きます。下りたら森の中の温泉へ。旭川駅からバスで1時間48分、ロープウェイで10分。帰りのバスは11:55・14:55・16:55発の3本だけなので、それに合わせた時間割です。",
        "favName": "姿見の池と旭岳",
        "favText": "ロープウェイの姿見駅から、夏は歩いて約20分。（写真：lumoplank / CC0）",
        "favPhoto": [
          "sugatami",
          0
        ],
        "who": [
          "帰りのバスは旭岳11:55・14:55・16:55発の3本だけ。16:55発が最終です",
          "ロープウェイは整備で止まる期間があります（2026年11月16日〜12月10日、2027年5月10日〜21日）。強風の日も止まります",
          "冬の山の上は雪と氷点下。スキーウェアに近い服、厚い手袋、帽子、冬の靴で。スノーシューはビジターセンターで1,000円（顔写真つきの身分証が要ります）",
          "バスの支払いにKitaca・Suicaの案内はありません。現金か、旭川駅前の案内所の券売機で",
          "タトゥー：公式サイトに「入れる」と書いているのはケイズハウス北海道（15:00から、900円、休みの日あり）",
          "旭岳温泉にATMはありません。現金は旭川で用意を"
        ],
        "dayHead": "旭岳の1日",
        "day": [
          {
            "time": "9:15",
            "area": "旭川",
            "title": "いで湯号で旭岳へ",
            "text": "旭川駅前9番のりば発、旭岳11:03着。片道2,300円。（写真：姒姓賢寧 / CC BY 4.0）",
            "photo": [
              "astart",
              0
            ],
            "note": "朝は7:15発も"
          },
          {
            "time": "11:05",
            "area": "旭岳",
            "title": "ビジターセンターで山の様子を聞く",
            "text": "無料。冬はここでスノーシューを借ります。（写真：Choi2451 / CC0）",
            "photo": [
              "avc",
              0
            ]
          },
          {
            "time": "11:40",
            "area": "旭岳",
            "title": "ロープウェイで姿見駅へ",
            "text": "約10分で標高1,600m。冬は20分おき。（写真：663highland / CC BY 2.5）",
            "photo": [
              "arope",
              0
            ]
          },
          {
            "time": "11:50",
            "area": "姿見",
            "title": "姿見の池と噴気",
            "text": "夏は一周約1時間。冬は見通しのよい日に、駅のまわりをスノーシューで。13:20発で下ります。（写真：663highland / CC BY 2.5）",
            "photo": [
              "sugatami",
              1
            ]
          },
          {
            "time": "14:20",
            "area": "旭岳温泉",
            "title": "森の中の温泉",
            "text": "お昼のあと、日帰り入浴へ。東川の町に寄る日は、14:55発のバスで（温泉はなし）。（写真：lumoplank / CC0）",
            "photo": [
              "aonsen",
              0
            ]
          },
          {
            "time": "16:55",
            "area": "帰り",
            "title": "最終バスで旭川へ",
            "text": "旭川駅18:33着。晩ごはんは駅前の買物公園のあたりで。（写真：lumoplank / CC0）",
            "photo": [
              "astart",
              1
            ],
            "note": "乗り遅れると戻れません"
          }
        ],
        "dealsLead": "旭川からの往復と、ロープウェイ・入浴料の分です。ビジターセンターと姿見の池の散策は無料。",
        "deals": [
          {
            "name": "いで湯号（66番）",
            "price": "片道2,300円",
            "text": "旭川駅〜旭岳。往復割引なし。現金か、案内所の券売機で。",
            "url": "https://www.asahikawa-denkikidou.jp/asahidaek_line/"
          },
          {
            "name": "旭岳ロープウェイ",
            "price": "往復3,000円",
            "text": "11月1日〜5月31日の金額。6月1日〜10月31日は3,500円。カード可。",
            "url": "https://asahidake.hokkaido.jp/ja/"
          },
          {
            "name": "スノーシュー（冬）",
            "price": "1,000円",
            "text": "旭岳ビジターセンターで。ストックつき、予約不可、顔写真つきの身分証が要ります。",
            "url": "https://www.asahidake-vc-2291.jp/rental_goods/"
          },
          {
            "name": "日帰り入浴",
            "price": "800〜1,200円",
            "text": "ケイズハウス900円、ベアモンテ1,140円、湧駒荘1,200円、白樺荘800円。",
            "url": "https://www.welcome-higashikawa.jp/onsen"
          },
          {
            "name": "東川で途中下車",
            "price": "1,450円＋1,110円",
            "text": "旭岳〜道草館1,450円、道草館〜旭川駅1,110円。",
            "url": "https://www.asahikawa-denkikidou.jp/manage/wp-content/uploads/2026/07/un66_2026.09.pdf"
          }
        ]
      },
      "sounkyo": {
        "kicker": "旭川から日帰り・一年中（冬は氷瀑まつり）",
        "h1": "断崖の谷の温泉街から、黒岳の5合目へ。",
        "lead": "層雲峡（そううんきょう）は、断崖の谷にある温泉街。旭川駅からバスで約2時間です。お昼を食べたら、ロープウェイで7分の5合目へ上がって、黒岳と谷を眺めます。7月〜10月はバスで、断崖を落ちる銀河・流星の滝へ。お風呂に入って、17:00発の最後のバスで旭川へ。1月下旬〜3月上旬の夜は、川原に氷の建物が並ぶ氷瀑まつりです。",
        "favName": "銀河の滝・流星の滝",
        "favText": "断崖を落ちる2本の滝。バスは7月〜10月だけです。（写真：lienyuan lee / CC BY 3.0）",
        "favPhoto": [
          "taki",
          0
        ],
        "who": [
          "旭川へ戻る最後のバスは層雲峡17:00発。そのあとは18:55発のバスで上川へ出て、JRに乗り継ぎます（旭川21:22着）",
          "黒岳ロープウェイは12:20の便が運休。冬は16:00まで（上り最終15:20）。毎年11月に整備で止まります",
          "滝と大函へのバスは7月1日〜10月31日だけ、1日1往復。ほかの季節はタクシー",
          "冬に開いている店は少なめです。現金を用意して、軽い食べ物を旭川で",
          "タトゥー：黒岳の湯の決まりは、公式の案内に書かれていません。電話で確認を（01658-5-3333）",
          "氷瀑まつりは2027年1月23日〜3月7日。平日は17:00から、土日祝は11:00から"
        ],
        "dayHead": "層雲峡の1日",
        "day": [
          {
            "time": "9:55",
            "area": "旭川",
            "title": "道北バスで層雲峡へ",
            "text": "旭川駅前8番のりば発、層雲峡11:54着。片道2,140円。（写真：Toshihiro Matsui / CC BY-SA 3.0）",
            "photo": [
              "sstart",
              0
            ],
            "note": "朝は6:55発も"
          },
          {
            "time": "11:55",
            "area": "温泉街",
            "title": "お昼",
            "text": "ラーメンの大雪山食堂か、洋食のビアグリル・キャニオン。（写真：Soica2001 / パブリックドメイン）",
            "photo": [
              "sgai",
              0
            ]
          },
          {
            "time": "12:40",
            "area": "黒岳",
            "title": "ロープウェイで5合目へ",
            "text": "7分で標高1,300m。屋上の展望台から黒岳と谷。12:20の便は運休です。（写真：pakku / CC BY 3.0）",
            "photo": [
              "kurodake",
              0
            ]
          },
          {
            "time": "12:50",
            "area": "峡谷",
            "title": "7月〜10月：バスで銀河・流星の滝",
            "text": "滝見台13:09着、13:49発で14:00に戻ります。この日のロープウェイは14:20発で。（写真：lienyuan lee / CC BY 3.0）",
            "photo": [
              "taki",
              1
            ]
          },
          {
            "time": "14:45",
            "area": "温泉街",
            "title": "黒岳の湯",
            "text": "日帰り入浴800円。3階に露天風呂。タトゥーの決まりは電話で確認を。（写真：Daigaku2051 / パブリックドメイン）",
            "photo": [
              "kuroyu",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "帰り",
            "title": "最後のバスで旭川へ",
            "text": "旭川駅前18:55着。氷瀑まつりの夜は、18:55発のバスで上川へ出てJRで。（写真：Outside147 / CC BY-SA 3.0）",
            "photo": [
              "hyobaku",
              0
            ]
          }
        ],
        "dealsLead": "旭川からの往復と、ロープウェイ・入浴料の分です。滝・大函・ビジターセンターは無料。",
        "deals": [
          {
            "name": "道北バス 層雲峡・上川線",
            "price": "片道2,140円",
            "text": "旭川駅前〜層雲峡。現金か、モバイルチケット。",
            "url": "https://www.dohokubus.com/files/kamikawa_souun.pdf"
          },
          {
            "name": "黒岳ロープウェイ",
            "price": "往復3,000円",
            "text": "小学生1,500円。夏のリフトは往復1,200円、セット3,900円。2027年6月1日から料金変更。",
            "url": "https://www.rinyu.co.jp/kurodake/about/"
          },
          {
            "name": "滝へのバス（7〜10月）",
            "price": "片道220円",
            "text": "層雲峡〜滝見台。1日1往復。",
            "url": "https://www.dohokubus.com/files/kamikawa_souun.pdf"
          },
          {
            "name": "黒岳の湯",
            "price": "800円",
            "text": "子ども400円。",
            "url": "https://sounkyo.net/stay/detail.html?content=25"
          },
          {
            "name": "氷瀑まつり",
            "price": "協力金1,000円",
            "text": "2027年1月23日〜3月7日。",
            "url": "https://sounkyo.net/hyoubaku/"
          },
          {
            "name": "遅い帰り（バス＋JR）",
            "price": "890円＋1,380円",
            "text": "層雲峡18:55→上川19:25、上川20:24→旭川21:22。",
            "url": "https://transit.yahoo.co.jp/search/result?to=%E6%97%AD%E5%B7%9D&y=2026&m=12&d=03&hh=19&m1=2&m2=5&type=1&ticket=normal&expkind=1&shin=1&ex=1&hb=1&lb=1&al=1&sr=1&s=0&userpass=1&ws=3&from=%E4%B8%8A%E5%B7%9D"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Daisetsuzan day trips from Asahikawa MAP',
    titleMain: 'Daisetsuzan day trips',
    titleSub: '旭岳と層雲峡（旭川から）',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Numbers show the order. Use the buttons above to choose Asahidake or Sounkyo. The places that fit the timetable are selected to start with. The dotted line shows the order, not the actual path.',
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
    credit: 'Text: Toshi (all photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    bus: 'Bus',
    closed: 'Closed',
    tattoo: 'Tattoos',
    food: 'Food',
    cash: 'Bring cash',
    checked: 'Checked on official websites and timetables on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 28, 2026',
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
    pickNote: 'The places that fit the timetable are selected to start with, and suggested times assume that set. The bus from Asahikawa is added automatically.',
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
    swCourse: 'Destination',
    courseAria: 'Destination',
    courseAsahidake: 'Asahidake\n(1 hr 48 min by bus)',
    courseSounkyo: 'Sounkyo\n(about 2 hr by bus)',
    swMode: 'How to go',
    intro: {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsMore": "See official site",
      "dealsNote": "Per adult. Checked on Nov 28, 2026 with the websites of the bus companies, ropeways and facilities, and a route planner (3 and 5 December timetables).",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose the destination",
          "text": "Use the buttons above the list: Asahidake or Sounkyo. The timetable and numbers change. You cannot do both in one day."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them (Higashikawa, Obako, the Ice Fall Festival)."
        },
        {
          "title": "Read the note at the top",
          "text": "Tap a number and what can catch you out comes first: last buses, ropeway closures, winter clothing, tattoo rules. Times and prices follow."
        },
        {
          "title": "Route search in Google Maps",
          "text": "Use “Open in Google Maps” on each spot to search a route straight away."
        }
      ],
      "cta": "View the map",
      "footer1": "An original map made by Toshi (for now all photos are from Wikimedia Commons, and the information comes from official websites and similar sources)."
    },
    introFor: {
      "asahidake": {
        "kicker": "Day trip from Asahikawa · all year (except ropeway maintenance)",
        "h1": "Face to face with Hokkaido’s highest mountain as it steams.",
        "lead": "Step out of Sugatami Station at 1,600 m and steaming Asahidake is right in front of you. Walk the loop around Sugatami Pond in summer, or go out on snowshoes on a clear winter day, then soak in a hot spring in the forest below. It is 1 hr 48 min by bus from Asahikawa Station and 10 minutes by ropeway. Buses back leave only at 11:55, 14:55 and 16:55, and the timetable is built around them.",
        "favName": "Sugatami Pond and Asahidake",
        "favText": "About 20 minutes on foot from the ropeway’s Sugatami Station in summer. (Photo: lumoplank / CC0)",
        "favPhoto": [
          "sugatami",
          0
        ],
        "who": [
          "Only three buses back: 11:55, 14:55 and 16:55 from Asahidake. The 16:55 is the last",
          "The ropeway closes for maintenance (16 Nov–10 Dec 2026, 10–21 May 2027) and stops in strong wind",
          "Winter at the top means snow and sub-zero cold: near-ski clothing, thick gloves, hat, winter boots. Snowshoes ¥1,000 at the Visitor Center (photo ID required)",
          "Kitaca and Suica are not listed for the bus. Pay cash or buy a ticket from the machine at the bus office in front of Asahikawa Station",
          "Tattoos: K’s House Hokkaido says on its website that they are fine (from 15:00, ¥900, closed some days)",
          "No ATM at Asahidake Onsen: bring cash from Asahikawa"
        ],
        "dayHead": "A day at Asahidake",
        "day": [
          {
            "time": "9:15",
            "area": "Asahikawa",
            "title": "Ideyu-go bus to Asahidake",
            "text": "From stop 9 outside Asahikawa Station; Asahidake 11:03. ¥2,300 one way. (Photo: 姒姓賢寧 / CC BY 4.0)",
            "photo": [
              "astart",
              0
            ],
            "note": "Earlier bus: 7:15"
          },
          {
            "time": "11:05",
            "area": "Asahidake",
            "title": "Ask about conditions at the Visitor Center",
            "text": "Free. In winter, rent snowshoes here. (Photo: Choi2451 / CC0)",
            "photo": [
              "avc",
              0
            ]
          },
          {
            "time": "11:40",
            "area": "Asahidake",
            "title": "Ropeway to Sugatami Station",
            "text": "About 10 minutes to 1,600 m. Every 20 minutes in winter. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "arope",
              0
            ]
          },
          {
            "time": "11:50",
            "area": "Sugatami",
            "title": "Sugatami Pond and the steam vents",
            "text": "A one-hour loop in summer; snowshoes around the station on clear winter days. Come down on the 13:20 car. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "sugatami",
              1
            ]
          },
          {
            "time": "14:20",
            "area": "Asahidake Onsen",
            "title": "A bath in the forest",
            "text": "After lunch, a day-use bath. To stop in Higashikawa instead, take the 14:55 bus (no bath). (Photo: lumoplank / CC0)",
            "photo": [
              "aonsen",
              0
            ]
          },
          {
            "time": "16:55",
            "area": "Return",
            "title": "Last bus to Asahikawa",
            "text": "Asahikawa Station 18:33. Dinner around the Kaimono Koen street by the station. (Photo: lumoplank / CC0)",
            "photo": [
              "astart",
              1
            ],
            "note": "Miss it and you are stuck"
          }
        ],
        "dealsLead": "The round trip from Asahikawa plus the ropeway and a bath. The Visitor Center and the walk at the top are free.",
        "deals": [
          {
            "name": "Ideyu-go bus (route 66)",
            "price": "¥2,300 one way",
            "text": "Asahikawa Station–Asahidake. No return discount. Cash, or a ticket from the machine at the bus office.",
            "url": "https://www.asahikawa-denkikidou.jp/asahidaek_line/"
          },
          {
            "name": "Asahidake Ropeway",
            "price": "¥3,000 return",
            "text": "1 Nov–31 May. ¥3,500 from 1 Jun to 31 Oct. Cards accepted.",
            "url": "https://asahidake.hokkaido.jp/en/"
          },
          {
            "name": "Snowshoes (winter)",
            "price": "¥1,000",
            "text": "At the Asahidake Visitor Center. Poles included, no reservations, photo ID required.",
            "url": "https://www.asahidake-vc-2291.jp/rental_goods/"
          },
          {
            "name": "Day bath",
            "price": "¥800–1,200",
            "text": "K’s House ¥900, Bear Monte ¥1,140, Yukomanso ¥1,200, Shirakabaso ¥800.",
            "url": "https://www.welcome-higashikawa.jp/onsen"
          },
          {
            "name": "Stopping in Higashikawa",
            "price": "¥1,450 + ¥1,110",
            "text": "Asahidake–Michikusa-kan ¥1,450, Michikusa-kan–Asahikawa Station ¥1,110.",
            "url": "https://www.asahikawa-denkikidou.jp/manage/wp-content/uploads/2026/07/un66_2026.09.pdf"
          }
        ]
      },
      "sounkyo": {
        "kicker": "Day trip from Asahikawa · all year (Ice Fall Festival in winter)",
        "h1": "From a hot-spring town in a gorge to the fifth station of Kurodake.",
        "lead": "Sounkyo is a hot-spring town in a gorge of sheer cliffs, about two hours by bus from Asahikawa Station. After lunch, ride the ropeway seven minutes up to the fifth station for Kurodake and the gorge. From July to October a bus runs to the Ginga and Ryusei falls, two falls down the cliff wall. A bath, then the last bus to Asahikawa at 17:00. From late January to early March, ice buildings fill the riverbank for the Ice Fall Festival.",
        "favName": "Ginga and Ryusei Falls",
        "favText": "Two falls down the gorge wall. The bus runs July–October only. (Photo: lienyuan lee / CC BY 3.0)",
        "favPhoto": [
          "taki",
          0
        ],
        "who": [
          "The last bus to Asahikawa leaves Sounkyo at 17:00. After that: the 18:55 bus to Kamikawa, then a JR train (Asahikawa 21:22)",
          "The Kurodake Ropeway has no 12:20 car. Winter hours end at 16:00 (last up 15:20). It closes for maintenance every November",
          "The bus to the falls and Obako runs only 1 July–31 October, once a day. Taxi in other seasons",
          "Few places are open in winter: carry cash and bring a snack from Asahikawa",
          "Tattoos: no rule is given for Kurodake-no-yu. Phone first (01658-5-3333)",
          "Ice Fall Festival: 23 January–7 March 2027, from 17:00 on weekdays and 11:00 at weekends and on holidays"
        ],
        "dayHead": "A day in Sounkyo",
        "day": [
          {
            "time": "9:55",
            "area": "Asahikawa",
            "title": "Dohoku Bus to Sounkyo",
            "text": "From stop 8 outside Asahikawa Station; Sounkyo 11:54. ¥2,140 one way. (Photo: Toshihiro Matsui / CC BY-SA 3.0)",
            "photo": [
              "sstart",
              0
            ],
            "note": "Earlier bus: 6:55"
          },
          {
            "time": "11:55",
            "area": "Town",
            "title": "Lunch",
            "text": "Ramen at Daisetsuzan Shokudo, or Western food at Beer Grill Canyon. (Photo: Soica2001 / public domain)",
            "photo": [
              "sgai",
              0
            ]
          },
          {
            "time": "12:40",
            "area": "Kurodake",
            "title": "Ropeway to the fifth station",
            "text": "Seven minutes to 1,300 m; a rooftop lookout over Kurodake and the gorge. There is no 12:20 car. (Photo: pakku / CC BY 3.0)",
            "photo": [
              "kurodake",
              0
            ]
          },
          {
            "time": "12:50",
            "area": "Gorge",
            "title": "July–October: bus to the Ginga and Ryusei falls",
            "text": "Takimidai 13:09; back on the 13:49, in town at 14:00. Ride the ropeway at 14:20 on this plan. (Photo: lienyuan lee / CC BY 3.0)",
            "photo": [
              "taki",
              1
            ]
          },
          {
            "time": "14:45",
            "area": "Town",
            "title": "Kurodake-no-yu",
            "text": "Day bath, ¥800, with an open-air bath on the top floor. Phone to check the tattoo rule. (Photo: Daigaku2051 / public domain)",
            "photo": [
              "kuroyu",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Return",
            "title": "Last bus to Asahikawa",
            "text": "Asahikawa Station 18:55. For the Ice Fall Festival at night, take the 18:55 bus to Kamikawa and the train. (Photo: Outside147 / CC BY-SA 3.0)",
            "photo": [
              "hyobaku",
              0
            ]
          }
        ],
        "dealsLead": "The round trip from Asahikawa plus the ropeway and a bath. The falls, Obako and the Visitor Center are free.",
        "deals": [
          {
            "name": "Dohoku Bus, Sounkyo–Kamikawa line",
            "price": "¥2,140 one way",
            "text": "Asahikawa Station–Sounkyo. Cash or a mobile ticket.",
            "url": "https://www.dohokubus.com/files/kamikawa_souun.pdf"
          },
          {
            "name": "Kurodake Ropeway",
            "price": "¥3,000 return",
            "text": "Children ¥1,500. Summer chairlift ¥1,200 return, combined ¥3,900. Fares change on 1 June 2027.",
            "url": "https://www.rinyu.co.jp/kurodake/about/"
          },
          {
            "name": "Bus to the falls (Jul–Oct)",
            "price": "¥220 one way",
            "text": "Sounkyo–Takimidai. One round trip a day.",
            "url": "https://www.dohokubus.com/files/kamikawa_souun.pdf"
          },
          {
            "name": "Kurodake-no-yu",
            "price": "¥800",
            "text": "Children ¥400.",
            "url": "https://sounkyo.net/stay/detail.html?content=25"
          },
          {
            "name": "Ice Fall Festival",
            "price": "¥1,000 contribution",
            "text": "23 January–7 March 2027.",
            "url": "https://sounkyo.net/hyoubaku/"
          },
          {
            "name": "Late return (bus + JR)",
            "price": "¥890 + ¥1,380",
            "text": "Sounkyo 18:55 → Kamikawa 19:25; Kamikawa 20:24 → Asahikawa 21:22.",
            "url": "https://transit.yahoo.co.jp/search/result?to=%E6%97%AD%E5%B7%9D&y=2026&m=12&d=03&hh=19&m1=2&m2=5&type=1&ticket=normal&expkind=1&shin=1&ex=1&hb=1&lb=1&al=1&sr=1&s=0&userpass=1&ws=3&from=%E4%B8%8A%E5%B7%9D"
          }
        ]
      }
    }
  }
};
