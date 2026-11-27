/* Page texts in Japanese and English.
   Toshi 個人のマップ。札幌から日帰り 温泉めぐり（定山渓・登別）。札幌駅・大通・すすきののホテルを9〜10時に出る1日。
   コースは2つ（一覧の上のボタン）：jozankei＝定山渓温泉（最初に開く。data/routes/sapporo-onsen.json）、noboribetsu＝登別温泉（sapporo-onsen-noboribetsu.json）。
   intro はどちらのコースにも共通の項目で、コースで変わる項目は introFor[コース] が app.js で上書きされる（scripts/sync_sapporo_onsen.py）。
   写真は [スポットの id, 写真の番号]。今は Wikimedia Commons の写真だけ（行った・食べたと書かない）。
   時刻・料金は2026年11月26日に確認（出典は data/routes/sapporo-onsen*.json の sources）。直すときはこのファイルを直接直してよい */
window.SAPPORO_ONSEN_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '札幌から日帰り 温泉めぐり Hot-spring day trips from Sapporo MAP',
    titleMain: '札幌から日帰り 温泉めぐり',
    titleSub: 'Hot-spring day trips from Sapporo',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号は回る順番です。上のボタンで、定山渓温泉か登別温泉を選びます。最初は、時間割どおりに回れる場所が選ばれています。点線は順番を示す線で、実際の道ではありません。',
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
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月26日',
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
    pickNote: '最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。札幌からの行き帰りは、自動で入ります。',
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
    swCourse: '温泉地',
    courseAria: '温泉地',
    courseJozankei: '定山渓温泉\n（地下鉄とバスで1時間）',
    courseNoboribetsu: '登別温泉\n（特急で1時間14分）',
    swMode: '回り方',
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "交通費・入浴料",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月26日に、各施設・バス会社の公式サイトと乗換案内（12月3日・5日のダイヤ）で確認しました。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "温泉地を選ぶ",
          "text": "一覧の上のボタンで「定山渓温泉」か「登別温泉」を選びます。時間割と番号が変わります。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられます。冬に登別の遊歩道が通れない日は、クマ牧場に。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、タトゥーの決まり・予約・現金・冬の道など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
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
      "jozankei": {
        "kicker": "札幌から日帰り・一年中",
        "h1": "札幌から1時間。足湯と温泉卵と、谷の露天風呂。",
        "lead": "地下鉄とバスで1時間。川を見下ろす足湯、洞窟のお堂、温泉卵をつくる湯つぼを歩いて回り、午後は豊平峡温泉の露天風呂とインドカレー。夜は温泉街で食べてから、札幌駅行きのバスで帰ることもできます。",
        "favName": "豊平川の谷の温泉街",
        "favText": "札幌市の中にある温泉街です。足湯はどこも無料。（写真：t-konno / CC BY-SA 3.0）",
        "favPhoto": [
          "futami",
          0
        ],
        "who": [
          "タトゥー：定山渓の日帰り入浴は、公式サイトで断っているところが多いです。豊平峡温泉は記載がないので電話で確認を。足湯は無料で、だれでも",
          "予約なしなら地下鉄で真駒内へ、12番のバスで。札幌駅から直行のかっぱライナー号は予約制（前日17:00まで）",
          "じょうてつバスは交通系ICカード（Kitaca・Suicaなど）が使えます。JRのレールパスは使えません",
          "足湯の足ふきタオルは持っていくと便利（二見の足湯は自動販売機で300円）",
          "冬は雪で二見吊橋まで行けません。凍った道に、滑りにくい靴を",
          "1月20日〜2月28日の夜は雪灯路（ゆきとうろ）"
        ],
        "dayHead": "定山渓の1日",
        "day": [
          {
            "time": "9:52",
            "area": "札幌",
            "title": "地下鉄で真駒内へ、12番のバス",
            "text": "定山渓湯の町に11:01着。かっぱライナー号なら札幌駅9:35発・10:31着（予約制）。（写真：Ch1pabeck / CC BY-SA 4.0）",
            "photo": [
              "jstart",
              0
            ],
            "note": "すすきのは9:55"
          },
          {
            "time": "11:05",
            "area": "定山渓",
            "title": "川を見下ろす足湯、洞窟のお堂",
            "text": "二見の足湯から（雪のない季節は）二見吊橋へ。岩戸観音堂の洞窟に観音像33体。（写真：t-konno / CC BY-SA 3.0）",
            "photo": [
              "futami",
              0
            ]
          },
          {
            "time": "12:25",
            "area": "定山渓",
            "title": "お昼と温泉卵",
            "text": "温泉街の食堂でお昼。定山源泉公園の湯つぼで、約20分の温泉卵。（写真：MIKI Yoshihito / CC BY 2.0）",
            "photo": [
              "gensen",
              0
            ]
          },
          {
            "time": "14:50",
            "area": "豊平峡温泉",
            "title": "露天風呂とインドカレー",
            "text": "お風呂は21:45まで受付。タトゥーの決まりは電話で確認を。（写真：Soica2001 / パブリックドメイン）",
            "photo": [
              "hoheikyo",
              0
            ]
          },
          {
            "time": "20:00",
            "area": "帰り",
            "title": "最後のバスで札幌へ",
            "text": "豊平峡温泉20:00発、すすきの21:12着。温泉街で食べたら20:53発の札幌駅行き。（写真：T DMY / CC BY 3.0）",
            "photo": [
              "yoru",
              0
            ],
            "note": "すすきの21:12"
          }
        ],
        "dealsLead": "札幌からの往復と、入浴料・温泉卵の分です。足湯はどこも無料。",
        "deals": [
          {
            "name": "地下鉄＋12番のバス",
            "price": "片道1,040円",
            "text": "さっぽろ〜真駒内290円、真駒内駅〜定山渓湯の町750円。交通系ICカード可。",
            "url": "https://www.jotetsu.co.jp/bus/guide/qlqoi2000000005z.html"
          },
          {
            "name": "かっぱライナー号（予約制）",
            "price": "1,700円",
            "text": "札幌駅〜豊平峡温泉・定山渓車庫前の片道。ネット予約は1,460円。",
            "url": "https://www.jotetsu.co.jp/bus/kappa_liner/index.html"
          },
          {
            "name": "温泉街⇄豊平峡温泉",
            "price": "200円",
            "text": "12番のバスで16分。",
            "url": "https://www.jotetsu.co.jp/bus/times/260401/jyouzankeiyunomati.pdf"
          },
          {
            "name": "豊平峡温泉",
            "price": "1,300円",
            "text": "子ども600円。タオル220円・バスタオル500円（販売）。タトゥーは要確認。",
            "url": "https://hoheikyo.co.jp/onsen/"
          },
          {
            "name": "温泉卵セット",
            "price": "180円",
            "text": "卵3個とネット。定山渓物産館で。",
            "url": "https://jozankei.jp/oneday/ontama/"
          },
          {
            "name": "岩戸観音堂の洞窟",
            "price": "300円",
            "text": "子ども100円。お堂の参拝は無料。",
            "url": "https://jozankei.jp/en/spot/179/"
          }
        ]
      },
      "noboribetsu": {
        "kicker": "札幌から日帰り・一年中",
        "h1": "地獄谷の湯けむりと、川の天然足湯。",
        "lead": "特急で1時間14分。極楽通りでお昼を食べて、閻魔堂のからくり、湯気の上がる地獄谷、大湯沼へ。下りの途中の天然足湯で足を温め、夕方は日帰り入浴。晩ごはんを食べて、札幌に21:41に帰ります。",
        "favName": "地獄谷",
        "favText": "直径約450mの火口のあとから、1日に約1万トンの湯が湧いています。（写真：Kentaro Ohno / CC BY 2.0）",
        "favPhoto": [
          "jigoku",
          0
        ],
        "who": [
          "タトゥー：登別万世閣は公式に不可。夢元さぎり湯・第一滝本館は公式に記載がないので電話で確認を。大湯沼川の天然足湯は無料で、だれでも",
          "北海道の特急は全席指定。北海道レールパス・札幌−登別エリアパス（外国のパスポートの人向け）で乗れます",
          "道南バスは現金450円（小銭を）。パスは使えません",
          "登別温泉の手荷物預かりは16:30まで。夜まで残るなら、大きな荷物は札幌のホテルに",
          "冬は大湯沼・天然足湯への遊歩道が通行止めになることがあります。その日はクマ牧場へ",
          "夢元さぎり湯はタオルなしでは入れません（中で買えます）"
        ],
        "dayHead": "登別の1日",
        "day": [
          {
            "time": "9:45",
            "area": "札幌",
            "title": "特急北斗で登別へ",
            "text": "登別10:59着、11:13発のバスで登別温泉11:32着。（写真：MaedaAkihiko / CC BY-SA 4.0）",
            "photo": [
              "nstart",
              0
            ],
            "note": "特急は全席指定"
          },
          {
            "time": "11:35",
            "area": "極楽通り",
            "title": "お昼と閻魔堂",
            "text": "地獄ラーメンやみそラーメン。13:00に閻魔大王のからくり。（写真：lumoplank / CC0）",
            "photo": [
              "nlunch",
              0
            ]
          },
          {
            "time": "13:25",
            "area": "地獄谷",
            "title": "湯けむりの谷を木道で",
            "text": "谷の中ほどの鉄泉池まで。冬は凍るので滑りにくい靴で。（写真：Wpcpey / CC BY-SA 4.0）",
            "photo": [
              "jigoku",
              2
            ]
          },
          {
            "time": "14:00",
            "area": "大湯沼",
            "title": "大湯沼と天然足湯",
            "text": "温泉の川に足を入れる無料の足湯。冬は遊歩道が通行止めのことがあり、その日はクマ牧場へ。（写真：lumoplank / CC0）",
            "photo": [
              "oyunuma",
              0
            ]
          },
          {
            "time": "15:40",
            "area": "温泉街",
            "title": "日帰り入浴",
            "text": "夢元さぎり湯（500円）か第一滝本館（2,500円）。タトゥーは電話で確認を。（写真：Jiashiang / CC BY 2.0）",
            "photo": [
              "bath",
              0
            ]
          },
          {
            "time": "19:10",
            "area": "帰り",
            "title": "晩ごはんのあと、バスと特急で札幌へ",
            "text": "登別20:26発、札幌21:41着。最後は20:35のバスと21:21の特急（22:41着）。（写真：欅 / CC BY-SA 3.0）",
            "photo": [
              "nyoru",
              0
            ],
            "note": "札幌21:41"
          }
        ],
        "dealsLead": "札幌からの往復と、入浴料の分です。天然足湯と地獄谷は無料。",
        "deals": [
          {
            "name": "特急 札幌〜登別",
            "price": "片道4,890円",
            "text": "乗車券2,530円＋指定席2,360円（12月3日・5日の額）。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "札幌−登別エリアパス",
            "price": "10,000円〜",
            "text": "4日間。事前に買うと10,000円、駅で11,000円。外国のパスポートの人向け。バスは対象外。",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          },
          {
            "name": "道南バス 登別駅前〜登別温泉",
            "price": "片道450円",
            "text": "現金。中ドアのバスは整理券を取って降りるときに払います。",
            "url": "https://www.donanbus.co.jp/cms/wp-content/uploads/2026/09/2_R8.10.1_noboribetsu.pdf"
          },
          {
            "name": "夢元さぎり湯",
            "price": "500円",
            "text": "タオル400円で販売。休憩室つきの1日券710円。",
            "url": "https://sagiriyu-noboribetsu.com/"
          },
          {
            "name": "第一滝本館（日帰り入浴）",
            "price": "2,500円",
            "text": "バスタオル・フェイスタオル込み。18:00までに入館。",
            "url": "https://takimotokan.co.jp/ja/day_spa/"
          },
          {
            "name": "のぼりべつクマ牧場（寄り道）",
            "price": "3,200円",
            "text": "ロープウェイの往復込み。冬は最終入園15:50。",
            "url": "https://bearpark.jp/information/"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Hot-spring day trips from Sapporo MAP',
    titleMain: 'Hot-spring day trips from Sapporo',
    titleSub: '札幌から日帰り 温泉めぐり',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Numbers show the order. Use the buttons above to choose Jozankei or Noboribetsu. The places that fit the timetable are selected to start with. The dotted line shows the order, not the actual path.',
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
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 26, 2026',
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
    pickNote: 'The places that fit the timetable are selected to start with, and suggested times assume that set. The trip out from Sapporo and back is added automatically.',
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
    swCourse: 'Hot-spring town',
    courseAria: 'Hot-spring town',
    courseJozankei: 'Jozankei Onsen\n(1 hour by subway and bus)',
    courseNoboribetsu: 'Noboribetsu Onsen\n(74 min by express)',
    swMode: 'How to go',
    intro: {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Fares and bath fees",
      "dealsMore": "See official site or route planner",
      "dealsNote": "Per adult. Checked on Nov 26, 2026 with the facilities’ and bus companies’ websites and a route planner (3 and 5 December timetables).",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose the hot-spring town",
          "text": "Use the buttons above the list: Jozankei or Noboribetsu. The timetable and numbers change."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them. If the Noboribetsu trail is closed in winter, choose the Bear Park."
        },
        {
          "title": "Read the note at the top",
          "text": "Tap a number and what can stop you at the door comes first: tattoo rules, bookings, cash, icy paths. Times and prices follow."
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
      "jozankei": {
        "kicker": "Day trip from Sapporo · all year",
        "h1": "Foot baths, onsen eggs and an outdoor bath, an hour from Sapporo.",
        "lead": "An hour by subway and bus. Walk between a foot bath above the river, a cave shrine and a spring pot for cooking eggs, then spend the afternoon in the outdoor baths at Hoheikyo Onsen with an Indian curry. You can also eat in town and ride a bus straight back to Sapporo Station.",
        "favName": "A hot-spring town in a river valley",
        "favText": "Jozankei is inside Sapporo city. All the foot baths are free. (Photo: t-konno / CC BY-SA 3.0)",
        "favPhoto": [
          "futami",
          0
        ],
        "who": [
          "Tattoos: most day baths in Jozankei refuse them on their websites. Hoheikyo Onsen says nothing, so phone first. The foot baths are free and open to anyone",
          "No booking: subway to Makomanai, then the No. 12 bus. The direct Kappa Liner from Sapporo Station needs a reservation (by 17:00 the day before)",
          "Jotetsu buses take IC cards (Kitaca, Suica and others). Japan Rail passes are not valid",
          "Bring a small towel for the foot baths (Futami sells them for ¥300)",
          "In winter snow blocks the way to the Futami bridge, and paths are icy: wear shoes with grip",
          "Snow lanterns (Yukitouro) light the town in the evenings from 20 January to 28 February"
        ],
        "dayHead": "A day in Jozankei",
        "day": [
          {
            "time": "9:52",
            "area": "Sapporo",
            "title": "Subway to Makomanai, then the No. 12 bus",
            "text": "Jozankei Yunomachi at 11:01. Or the Kappa Liner: Sapporo Station 9:35, arriving 10:31 (reservation). (Photo: Ch1pabeck / CC BY-SA 4.0)",
            "photo": [
              "jstart",
              0
            ],
            "note": "Susukino 9:55"
          },
          {
            "time": "11:05",
            "area": "Jozankei",
            "title": "Foot bath over the river, cave shrine",
            "text": "From the Futami foot bath to the suspension bridge (when there is no snow), then 33 Kannon statues in the Iwato cave. (Photo: t-konno / CC BY-SA 3.0)",
            "photo": [
              "futami",
              0
            ]
          },
          {
            "time": "12:25",
            "area": "Jozankei",
            "title": "Lunch and onsen eggs",
            "text": "Lunch in a local diner, then eggs in the spring pot at Jozan Gensen Park (about 20 minutes). (Photo: MIKI Yoshihito / CC BY 2.0)",
            "photo": [
              "gensen",
              0
            ]
          },
          {
            "time": "14:50",
            "area": "Hoheikyo Onsen",
            "title": "Outdoor baths and Indian curry",
            "text": "Last entry for the baths 21:45. Phone first about tattoos. (Photo: Soica2001 / public domain)",
            "photo": [
              "hoheikyo",
              0
            ]
          },
          {
            "time": "20:00",
            "area": "Back",
            "title": "The last bus to Sapporo",
            "text": "Hoheikyo Onsen 20:00, Susukino 21:12. If you eat in town, the 20:53 runs to Sapporo Station. (Photo: T DMY / CC BY 3.0)",
            "photo": [
              "yoru",
              0
            ],
            "note": "Susukino 21:12"
          }
        ],
        "dealsLead": "The trip from Sapporo plus bath and egg costs. All the foot baths are free.",
        "deals": [
          {
            "name": "Subway + No. 12 bus",
            "price": "¥1,040 one way",
            "text": "Sapporo–Makomanai ¥290, Makomanai–Jozankei Yunomachi ¥750. IC cards OK.",
            "url": "https://www.jotetsu.co.jp/bus/guide/qlqoi2000000005z.html"
          },
          {
            "name": "Kappa Liner (reservation)",
            "price": "¥1,700",
            "text": "Sapporo Station to Hoheikyo Onsen or Jozankei Shako-mae, one way. ¥1,460 booked online.",
            "url": "https://www.jotetsu.co.jp/bus/kappa_liner/index.html"
          },
          {
            "name": "Town ⇄ Hoheikyo Onsen",
            "price": "¥200",
            "text": "16 minutes on the No. 12 bus.",
            "url": "https://www.jotetsu.co.jp/bus/times/260401/jyouzankeiyunomati.pdf"
          },
          {
            "name": "Hoheikyo Onsen",
            "price": "¥1,300",
            "text": "Children ¥600. Towel ¥220, bath towel ¥500 (for sale). Tattoos: please check.",
            "url": "https://hoheikyo.co.jp/onsen/"
          },
          {
            "name": "Onsen egg set",
            "price": "¥180",
            "text": "Three eggs and a net, from Jozankei Bussankan.",
            "url": "https://jozankei.jp/oneday/ontama/"
          },
          {
            "name": "Iwato Kannon-do cave",
            "price": "¥300",
            "text": "Children ¥100. The hall itself is free.",
            "url": "https://jozankei.jp/en/spot/179/"
          }
        ]
      },
      "noboribetsu": {
        "kicker": "Day trip from Sapporo · all year",
        "h1": "Steam over Hell Valley, and a foot bath in a hot river.",
        "lead": "74 minutes by limited express. Lunch on Gokuraku-dori, the mechanical King of Hell at Enma-do, the steaming Jigokudani valley and Oyunuma pond. Warm your feet in the natural foot bath on the way down, bathe in the late afternoon, have dinner and be back in Sapporo at 21:41.",
        "favName": "Jigokudani (Hell Valley)",
        "favText": "An old crater about 450 m across, where some 10,000 tonnes of hot water rise every day. (Photo: Kentaro Ohno / CC BY 2.0)",
        "favPhoto": [
          "jigoku",
          0
        ],
        "who": [
          "Tattoos: Noboribetsu Manseikaku refuses them on its website. Sagiriyu and Dai-ichi Takimotokan say nothing, so phone first. The natural foot bath is free and open to anyone",
          "Hokkaido’s limited expresses are all reserved seats. The Hokkaido Rail Pass and the Sapporo–Noboribetsu Area Pass (for non-Japanese passports) cover them",
          "The Donan bus costs ¥450 in cash (have coins). Rail passes do not cover it",
          "Left luggage in Noboribetsu Onsen closes at 16:30. Staying into the evening? Leave big bags at your Sapporo hotel",
          "In winter the trail to Oyunuma and the foot bath can close. On those days, go to the Bear Park",
          "Sagiriyu does not let you in without a small towel (you can buy one there)"
        ],
        "dayHead": "A day in Noboribetsu",
        "day": [
          {
            "time": "9:45",
            "area": "Sapporo",
            "title": "Limited express Hokuto to Noboribetsu",
            "text": "Noboribetsu 10:59, then the 11:13 bus to Noboribetsu Onsen (11:32). (Photo: MaedaAkihiko / CC BY-SA 4.0)",
            "photo": [
              "nstart",
              0
            ],
            "note": "All seats reserved"
          },
          {
            "time": "11:35",
            "area": "Gokuraku-dori",
            "title": "Lunch and Enma-do",
            "text": "“Hell ramen” or miso ramen, then the mechanical King of Hell at 13:00. (Photo: lumoplank / CC0)",
            "photo": [
              "nlunch",
              0
            ]
          },
          {
            "time": "13:25",
            "area": "Jigokudani",
            "title": "A boardwalk through the steam",
            "text": "Down to Tessen-ike in the middle of the valley. Icy in winter: wear shoes with grip. (Photo: Wpcpey / CC BY-SA 4.0)",
            "photo": [
              "jigoku",
              2
            ]
          },
          {
            "time": "14:00",
            "area": "Oyunuma",
            "title": "Oyunuma pond and the natural foot bath",
            "text": "A free foot bath in a hot river. If the trail is closed in winter, go to the Bear Park. (Photo: lumoplank / CC0)",
            "photo": [
              "oyunuma",
              0
            ]
          },
          {
            "time": "15:40",
            "area": "Onsen town",
            "title": "A day bath",
            "text": "Sagiriyu (¥500) or Dai-ichi Takimotokan (¥2,500). Phone first about tattoos. (Photo: Jiashiang / CC BY 2.0)",
            "photo": [
              "bath",
              0
            ]
          },
          {
            "time": "19:10",
            "area": "Back",
            "title": "Dinner, then bus and express to Sapporo",
            "text": "Noboribetsu 20:26, Sapporo 21:41. Last: the 20:35 bus and 21:21 express (22:41). (Photo: 欅 / CC BY-SA 3.0)",
            "photo": [
              "nyoru",
              0
            ],
            "note": "Sapporo 21:41"
          }
        ],
        "dealsLead": "The trip from Sapporo plus bath fees. Jigokudani and the natural foot bath are free.",
        "deals": [
          {
            "name": "Limited express Sapporo–Noboribetsu",
            "price": "¥4,890 one way",
            "text": "Fare ¥2,530 + reserved seat ¥2,360 (on 3 and 5 December).",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Sapporo–Noboribetsu Area Pass",
            "price": "from ¥10,000",
            "text": "4 days: ¥10,000 bought in advance, ¥11,000 at the station. For non-Japanese passports. Buses not included.",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          },
          {
            "name": "Donan bus, station ⇄ onsen",
            "price": "¥450 one way",
            "text": "Cash. On middle-door buses take a numbered ticket and pay when you get off.",
            "url": "https://www.donanbus.co.jp/cms/wp-content/uploads/2026/09/2_R8.10.1_noboribetsu.pdf"
          },
          {
            "name": "Sagiriyu",
            "price": "¥500",
            "text": "Towels for sale at ¥400. Day ticket with rest room ¥710.",
            "url": "https://sagiriyu-noboribetsu.com/"
          },
          {
            "name": "Dai-ichi Takimotokan (day bath)",
            "price": "¥2,500",
            "text": "Bath and face towels included. Enter by 18:00.",
            "url": "https://takimotokan.co.jp/ja/day_spa/"
          },
          {
            "name": "Noboribetsu Bear Park (optional)",
            "price": "¥3,200",
            "text": "Return ropeway included. Winter last entry 15:50.",
            "url": "https://bearpark.jp/information/"
          }
        ]
      }
    }
  }
};
