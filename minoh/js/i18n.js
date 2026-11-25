/* Page texts in Japanese and English.
   Toshi 個人のマップ。スタートは箕面萱野駅、ゴールは牧落駅。
   コースは4つ（出発時間 早め/ゆっくり × 箕面温泉に入る/入らない）。データは data/routes/minoh.json・minoh-noonsen.json・
   minoh-late.json・minoh-late-noonsen.json（4つとも scripts/build_minoh_courses.py が作る）。
   紹介ページのうちコースで変わる項目（lead・who・dayHead・day・how）は、各言語の introParts から
   このファイルのいちばん下で組み立てて introFor[コースの id] に入れる（app.js が読み込むときに intro に上書きする）。
   Photos are [spot id, photo index]（番号はコースで変わるので id で指定）.
   料金・時間は2026年11月20日〜21日に各社の公式サイトで確認。 */
window.MINOH_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '大阪 箕面｜箕面 Minoh MAP',
    titleMain: '大阪 箕面',
    titleSub: 'Minoh, Osaka',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号の順にめぐると1日で回れるルートです。上のボタンで、出発時間と、箕面温泉に入るかどうかを選べます。選ぶと番号と時間が変わります。「早めに出発」は梅田を8:30までに出て、川のテラスでランチ（現金だけ）。「ゆっくり出発」は10時ごろに出て、お昼は持って行きます。箕面温泉は、タトゥーがあるとカバーシール2枚で完全に隠せる場合しか入れません。点線は順番を示す線で、実際の道ではありません。',
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
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    closed: '休み',
    cable: 'ケーブル',
    tattoo: 'タトゥー',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトで確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月20日〜25日',
    noticeHead: 'この時期の注意',
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
    modeAria: '出発時間',
    modeAll: '早めに出発\n（川のテラスでランチ）',
    modePick: 'ゆっくり出発\n（10時ごろ）',
    swStart: '出発時間',
    swOnsen: '箕面温泉（タトゥーがある人は注意）',
    onsenAria: '箕面温泉に入るかどうか',
    onsenYes: '温泉に入る',
    onsenNo: '温泉に入らない',
    pickNote: '行きたい場所の「行きたい」を押してください。駅・バス停・ハイキング入口は、選んだ場所に合わせて自動で入ったり外れたりします。時間は全部回る場合の目安です。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（駅などを含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から行きたい場所を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '自動',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    intro: {
      kicker: 'Toshiが歩いて作った1日ルート',
      h1: '大阪の街から少し足をのばして、ダルマと森と滝の1日。',
      favLabel: 'いちばんの見どころ',
      favName: '勝尾寺',
      favText: 'お寺じゅうに、小さな赤い「勝ちダルマ」。',
      favPhoto: ['katsuoji', 0],
      whoHead: 'こんな人におすすめ',
      from: '',
      timeSuffix: '〜',
      dealsHead: '交通費のめやす',
      dealsLead: '梅田から出発して梅田へ戻ると、電車とバスで大人1人1,560円です（勝尾寺の入山料500円は別）。',
      deals: [
        { name: '御堂筋線・北大阪急行（梅田→箕面萱野）', price: '480円', text: '乗り換えなしの直通運転。なんばからは530円です。', url: 'https://www.kita-kyu.co.jp/enshin/index3.html' },
        { name: '阪急バス 30系統（箕面萱野→勝尾寺）', price: '800円', text: '2026年10月から現金不可。交通系ICカードかhanica、または8番のりばで買える専用乗車券（クレジットカードのみ）で乗ります。', url: 'https://www.hankyubus.co.jp/news/2026101.html' },
        { name: '阪急電車（牧落→大阪梅田）', price: '280円', text: '石橋阪大前で乗り換え。箕面駅から乗っても同じ料金です。', url: 'https://www.hankyu.co.jp/station/html/HK-58_mi_1_w.html' }
      ],
      dealsNote: '大人の普通運賃です。2026年11月20日に各社の公式サイトで確認しました。',
      dealsMore: '公式サイトで見る',
      howHead: 'このマップの使い方',
      cta: '地図を見る',
      footer1: 'Toshiが実際に歩いて作った、オリジナルマップです。'
    },
    // 紹介ページのうち、コースで変わるところ（下で組み立てる）
    introParts: {
      lead: 'ダルマだらけの勝尾寺から、森の山道を歩いて箕面大滝へ。川ぞいの滝道を下ったら、締めくくりは大阪名物のたこ焼きと地元のクラフトビール。実際に歩いて作った、大阪・箕面の1日ルートです。',
      leadPick: '出発時間（早め／ゆっくり）と、箕面温泉に入るかどうかを選べます。',
      leadNow: { early: '今は「早めに出発・温泉に入る」の流れです。', 'early-noonsen': '今は「早めに出発・温泉に入らない」の流れです。', late: '今は「ゆっくり出発・温泉に入る」の流れです。', 'late-noonsen': '今は「ゆっくり出発・温泉に入らない」の流れです。' },
      who: {
        common: [
          '大阪の街から日帰りで、山と滝の自然を楽しみたい人に',
          'スタートは箕面萱野駅。梅田から地下鉄で乗り換えなし、最速25分',
          '秋の紅葉シーズンは特におすすめ。夜は滝のライトアップも',
          '山道を歩く時間は約1時間10分（ほとんど下り坂）。途中で20分休みます。歩きやすい靴で'
        ],
        start: {
          early: ['梅田を8:30までに出て、お昼は川の上のテラスで。朝ゆっくりの人は「ゆっくり出発」（10時ごろ）に切り替えを'],
          late: ['10時ごろ出発。お昼は箕面萱野駅で買って、山の広場で食べます。梅田を8:30までに出られるなら「早めに出発」へ（川のテラスでランチ）']
        },
        cash: {
          early: ['バスは現金が使えず、川のテラスのランチは現金だけ。ICカードと現金の両方を持って行く'],
          late: ['バスは現金が使えません。交通系ICカードを用意']
        },
        onsen: {
          yes: ['タトゥーがある人は注意：箕面温泉は、専用のカバーシール2枚までで完全に隠せる場合だけ入れます。隠せない人は「温泉に入らない」を選んでください'],
          no: ['箕面温泉には入らない流れです。そのぶん滝と滝道でゆっくりできます（タトゥーがあって温泉に入れない人もこちら）']
        },
        end: ['締めくくりはたこ焼きと地ビール、シメにラーメン。途中で、日本のミスタードーナツの1号店にも寄ります。箕面ビールは木曜休み']
      },
      dayHead: { early: '1日の流れ（早めに出発・温泉に入る）', 'early-noonsen': '1日の流れ（早めに出発・温泉なし）', late: '1日の流れ（ゆっくり出発・温泉に入る）', 'late-noonsen': '1日の流れ（ゆっくり出発・温泉なし）' },
      day: {
        busE: { time: '9:00', area: '箕面萱野', title: 'バスで山の上のお寺へ', text: '駅前の8番のりばから、9:00発の直行バスで約22分。梅田は8:30までに出ます。', note: 'バスは現金不可。ICカードで', photo: ['bus', 0] },
        busL: { time: '10:30', area: '箕面萱野', title: 'お昼を買って、バスで山の上のお寺へ', text: '駅の横のファミリーマートでお昼を買って、8番のりばから直行バスで約22分。平日は10:30発、土日祝は10:40発。', note: 'バスは現金不可。ICカードで', photo: ['bus', 0] },
        templeE: { time: '9:30', area: '勝尾寺', title: 'ダルマだらけのお寺', text: '山門、池、多宝塔。境内のあちこちに小さな赤いダルマ。11:00まで1時間半。', photo: ['katsuoji', 1] },
        templeL: { time: '11:00', area: '勝尾寺', title: 'ダルマだらけのお寺', text: '山門、池、多宝塔。境内のあちこちに小さな赤いダルマ。12:30まで1時間半。', photo: ['katsuoji', 1] },
        walkE: { time: '11:00', area: '森の山道', title: '森を歩いて滝へ', text: 'ビジターセンターまで約40分、20分休んで、杉の茶屋まで約30分。歩く時間は合わせて約1時間10分。滝は12:35〜13:10。', badge: 'ハイキングあり', photo: ['falls', 0] },
        walkL: { time: '12:30', area: '森の山道', title: '森を歩いて滝へ。途中の広場でお昼', text: 'ビジターセンターまで約40分。前の「もみじ広場」でお昼を食べて20分休み、杉の茶屋まで約30分。滝は14:05〜14:40。', badge: 'ハイキングあり', photo: ['falls', 0] },
        walkLNo: { time: '12:30', area: '森の山道', title: '森を歩いて滝へ。途中の広場でお昼', text: 'ビジターセンターまで約40分。前の「もみじ広場」でお昼を食べて30分休み、杉の茶屋まで約30分。滝は14:15〜15:00、ゆっくりできます。', badge: 'ハイキングあり', photo: ['falls', 0] },
        lunch: { time: '13:10', area: '滝道', title: '川ぞいのテラスでランチ', text: '滝道を35〜40分下って、13:50ごろ川の上のテラス席へ。着いたらすぐ注文を。', note: '現金だけ・ラストオーダー14:30', photo: ['cinque', 0] },
        onsenE: { time: '15:05', area: '箕面温泉', title: '歩いたあとの温泉', text: '滝道から展望エレベーターで上がる日帰り温泉。ビールの前にひと風呂。16:45まで。', note: 'タトゥーはシール2枚で隠せる場合だけ', photo: ['onsen', 0] },
        onsenL: { time: '14:40', area: '滝道・箕面温泉', title: '滝道を下って温泉へ', text: '川ぞいの滝道を約40分。15:25ごろ、展望エレベーターで上がる日帰り温泉へ。17:05まで。', note: 'タトゥーはシール2枚で隠せる場合だけ', photo: ['onsen', 0] },
        strollE: { time: '14:50', area: '滝道・箕面駅', title: 'ランチのあとは滝道でのんびり', text: '駅までは歩いて10分ほど。瀧安寺にお参りしたり、もみじの天ぷらを買ったり、昆虫館に寄ったり。16:10ごろ箕面駅へ。', photo: ['minoh-st', 0] },
        strollL: { time: '15:00', area: '滝道・箕面駅', title: '滝道をゆっくり下る', text: '歩くだけなら約40分の道を、1時間10分かけて。お店をのぞいたり、瀧安寺にお参りしたり。16:10ごろ箕面駅へ。', photo: ['minoh-st', 0] },
        endE: { time: '17:05', area: '箕面・牧落', title: 'ドーナツ、たこ焼き、地ビール', text: 'ミスタードーナツの1号店でひと休みして、Toshiがいちばん好きなたこ焼き屋さんへ。18:05ごろから箕面ビールの直営店で乾杯、シメは黒兵衛のラーメン。牧落駅を20:10ごろ。', note: '箕面ビールは木曜休み（木曜は黒兵衛で晩ごはんを）・日曜は20時まで', photo: ['ahoya', 0] },
        endL: { time: '17:25', area: '箕面・牧落', title: 'ドーナツ、たこ焼き、地ビール', text: 'ミスタードーナツの1号店でひと休みして、Toshiがいちばん好きなたこ焼き屋さんへ。18:25ごろから箕面ビールの直営店で乾杯、シメは黒兵衛のラーメン。牧落駅を20:30ごろ。', note: '箕面ビールは木曜休み（木曜は黒兵衛で晩ごはんを）・日曜は20時まで', photo: ['ahoya', 0] },
        endNo: { time: '16:15', area: '箕面・牧落', title: 'ドーナツ、たこ焼き、地ビール', text: 'ミスタードーナツの1号店でひと休みして、Toshiがいちばん好きなたこ焼き屋さんへ。17:15ごろから箕面ビールの直営店で乾杯、シメは黒兵衛のラーメン。牧落駅を19:20ごろ。', note: '箕面ビールは木曜休み（木曜は黒兵衛で晩ごはんを）・日曜は20時まで', photo: ['ahoya', 0] }
      },
      howPick: { title: '出発時間と温泉を選ぶ', text: '「一覧」のいちばん上に、ボタンが2段あります。上は出発時間（「早めに出発」＝梅田を8:30までに出て川のテラスでランチ／「ゆっくり出発」＝10時ごろ出る、テラスのランチはなし）。下は箕面温泉に入るかどうか。タトゥーがあって温泉に入れない人は「温泉に入らない」を。押すと、番号と時間が変わります。' },
      howRest: [
        { title: '番号の順にめぐる', text: '1〜{n}の番号は、順番にめぐると1日で全部回れるように並んでいます。' },
        { title: '番号をタップ', text: '地図の番号か「一覧」をタップすると、写真・説明・おすすめの時間が見られます。' },
        { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。時刻表や公式サイトへのリンクもあります。' },
        { title: '時間は目安', text: '時間が足りなければスキップ、気に入った場所では長めに。自分のペースで調整してください。' }
      ]
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Minoh, Osaka | Minoh MAP',
    titleMain: 'Minoh, Osaka',
    titleSub: '大阪 箕面',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Follow the numbers for a one-day route. With the buttons above, choose your start time and whether to go to Minoh Onsen: the numbers and times change to match. “Early start” leaves Umeda by 8:30 and has lunch on the river terrace (cash only). “Late start” leaves around 10:00 and you carry your lunch. Minoh Onsen admits tattoos only if two cover stickers hide them completely. The dotted line shows the order, not the actual path.',
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
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    closed: 'Closed',
    cable: 'Cable car',
    tattoo: 'Tattoos',
    cash: 'Bring cash',
    checked: 'Checked on the official website on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 20–25, 2026',
    noticeHead: 'Right now',
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
    modeAria: 'Start time',
    modeAll: 'Early start\n(lunch on the river terrace)',
    modePick: 'Late start\n(around 10:00)',
    swStart: 'Start time',
    swOnsen: 'Minoh Onsen (check first if you have tattoos)',
    onsenAria: 'Minoh Onsen or not',
    onsenYes: 'With the onsen',
    onsenNo: 'No onsen',
    pickNote: 'Tap “Want to go” on the places you like. Stations, bus stops and the trail entrance are added or skipped automatically to match. Times are for the full route.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. stations)',
    pickEmpty: 'Nothing chosen yet. Pick the places you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Auto',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      kicker: 'A day trip, hand-walked by Toshi',
      h1: 'Daruma, forest and a waterfall, a short hop from central Osaka.',
      favLabel: 'Don’t miss',
      favName: 'Katsuoji Temple',
      favText: 'Little red “victory” daruma, all over the temple.',
      favPhoto: ['katsuoji', 0],
      whoHead: 'Who it’s for',
      from: 'From',
      timeSuffix: '',
      dealsHead: 'Getting around: fares',
      dealsLead: 'From Umeda and back again, trains and the bus cost ¥1,560 per adult (plus ¥500 admission at Katsuoji).',
      deals: [
        { name: 'Midosuji Line / Kita-Osaka Kyuko (Umeda → Minoh-Kayano)', price: '¥480', text: 'Runs straight through, no change. ¥530 from Namba.', url: 'https://www.kita-kyu.co.jp/enshin/index3.html' },
        { name: 'Hankyu Bus route 30 (Minoh-Kayano → Katsuoji)', price: '¥800', text: 'No cash since October 2026. Pay with an IC card (ICOCA, Suica, etc.), hanica, or a special ticket sold at stand 8 (credit card only).', url: 'https://www.hankyubus.co.jp/news/2026101.html' },
        { name: 'Hankyu train (Makiochi → Osaka-umeda)', price: '¥280', text: 'Change at Ishibashi Handai-mae. Same fare from Minoh Station.', url: 'https://www.hankyu.co.jp/station/html/HK-58_mi_1_w.html' }
      ],
      dealsNote: 'Adult single fares, checked on each operator’s official website on Nov 20, 2026.',
      dealsMore: 'See official site',
      howHead: 'How to use this map',
      cta: 'Open the map',
      footer1: 'An original map, hand-walked by Toshi.'
    },
    // the parts of the intro that change with the course (assembled at the bottom of this file)
    introParts: {
      lead: 'From Katsuoji, a temple full of daruma, walk through the forest to Minoh Falls. Follow the river path down into town, then finish with Osaka’s famous takoyaki and local craft beer. A one-day route in Minoh, Osaka, that I walked myself.',
      leadPick: 'You can choose your start time (early or late) and whether to go to the hot spring, Minoh Onsen.',
      leadNow: { early: 'This is the early start, with the onsen.', 'early-noonsen': 'This is the early start, without the onsen.', late: 'This is the late start, with the onsen.', 'late-noonsen': 'This is the late start, without the onsen.' },
      who: {
        common: [
          'A day out of the city: mountains, forest and a waterfall',
          'Starts at Minoh-Kayano Station, 25 min from Umeda by subway, no change',
          'Best in autumn, when the falls are lit up at night',
          'About 1 hour 10 minutes of walking on a forest trail, mostly downhill, with a 20-minute rest. Wear comfy shoes'
        ],
        start: {
          early: ['Leave Umeda by 8:30 and have lunch on a terrace over the river. Slow morning? Switch to “Late start” (around 10:00)'],
          late: ['Leave around 10:00. Buy lunch at Minoh-Kayano and eat it on a lawn in the hills. Can you leave Umeda by 8:30? Switch to “Early start” for lunch on the river terrace']
        },
        cash: {
          early: ['The bus takes no cash and the terrace lunch is cash only: carry both an IC card and cash'],
          late: ['The bus takes no cash: have an IC card ready']
        },
        onsen: {
          yes: ['Tattoos? Minoh Onsen lets you in only if no more than two of its cover stickers hide them completely. If they can’t, choose “No onsen”'],
          no: ['This version skips Minoh Onsen, so you get more time at the falls and on the river path (also the one to pick if your tattoos keep you out of the bath)']
        },
        end: ['Ends with takoyaki, local craft beer and a bowl of ramen, with a stop at Japan’s first Mister Donut on the way. Minoh Beer is closed on Thursdays']
      },
      dayHead: { early: 'One day, roughly like this (early start, with onsen)', 'early-noonsen': 'One day, roughly like this (early start, no onsen)', late: 'One day, roughly like this (late start, with onsen)', 'late-noonsen': 'One day, roughly like this (late start, no onsen)' },
      day: {
        busE: { time: '9:00', area: 'Minoh-Kayano', title: 'Bus up to a mountain temple', text: 'The 9:00 direct bus from stand 8 in front of the station, 22 minutes. Leave Umeda by 8:30.', note: 'No cash on the bus: use an IC card', photo: ['bus', 0] },
        busL: { time: '10:30', area: 'Minoh-Kayano', title: 'Buy lunch, then the bus up to a mountain temple', text: 'Buy lunch at the FamilyMart next to the station, then take the direct bus from stand 8, 22 minutes. It leaves at 10:30 on weekdays and 10:40 on weekends and holidays.', note: 'No cash on the bus: use an IC card', photo: ['bus', 0] },
        templeE: { time: '9:30', area: 'Katsuoji', title: 'A temple full of daruma', text: 'Gate, pond and pagoda, with little red daruma everywhere. An hour and a half, until 11:00.', photo: ['katsuoji', 1] },
        templeL: { time: '11:00', area: 'Katsuoji', title: 'A temple full of daruma', text: 'Gate, pond and pagoda, with little red daruma everywhere. An hour and a half, until 12:30.', photo: ['katsuoji', 1] },
        walkE: { time: '11:00', area: 'Forest walk', title: 'Walk the forest to the falls', text: 'About 40 minutes to the Visitor Center, a 20-minute rest, then about 30 minutes to Sugi no Chaya: 1 hour 10 minutes of walking in all. At the falls 12:35–13:10.', badge: 'Includes a hike', photo: ['falls', 0] },
        walkL: { time: '12:30', area: 'Forest walk', title: 'Walk the forest to the falls, with a picnic on the way', text: 'About 40 minutes to the Visitor Center. Eat your lunch on the lawn in front and rest for 20 minutes, then about 30 minutes to Sugi no Chaya. At the falls 14:05–14:40.', badge: 'Includes a hike', photo: ['falls', 0] },
        walkLNo: { time: '12:30', area: 'Forest walk', title: 'Walk the forest to the falls, with a picnic on the way', text: 'About 40 minutes to the Visitor Center. Eat your lunch on the lawn in front and rest for 30 minutes, then about 30 minutes to Sugi no Chaya. At the falls 14:15–15:00, with time to linger.', badge: 'Includes a hike', photo: ['falls', 0] },
        lunch: { time: '13:10', area: 'Takimichi', title: 'Lunch over the river', text: 'Walk 35–40 minutes down the riverside path to a terrace above the water, arriving about 13:50. Order as soon as you arrive.', note: 'Cash only · last order 14:30', photo: ['cinque', 0] },
        onsenE: { time: '15:05', area: 'Minoh Onsen', title: 'A hot spring after the walk', text: 'A day-use hot spring reached by a viewing elevator from the falls path: a bath before the beer. Until 16:45.', note: 'Tattoos: only if two stickers cover them', photo: ['onsen', 0] },
        onsenL: { time: '14:40', area: 'Takimichi & Minoh Onsen', title: 'Down the river path to a hot spring', text: 'About 40 minutes down the riverside path. At about 15:25, take the viewing elevator up to the day-use hot spring. Until 17:05.', note: 'Tattoos: only if two stickers cover them', photo: ['onsen', 0] },
        strollE: { time: '14:50', area: 'Takimichi & Minoh Station', title: 'A slow hour on the river path', text: 'The station is only about 10 minutes’ walk away. Visit Ryuanji Temple, buy momiji tempura, or drop into the Insect Museum. Reach Minoh Station at about 16:10.', photo: ['minoh-st', 0] },
        strollL: { time: '15:00', area: 'Takimichi & Minoh Station', title: 'Take the river path slowly', text: 'The walk alone is about 40 minutes; give it 1 hour 10 minutes. Look into the shops and visit Ryuanji Temple. Reach Minoh Station at about 16:10.', photo: ['minoh-st', 0] },
        endE: { time: '17:05', area: 'Minoh & Makiochi', title: 'Donuts, takoyaki & craft beer', text: 'A break at Japan’s first Mister Donut, then my favorite takoyaki shop. A toast at the Minoh Beer taproom from about 18:05, and ramen at Kurobee to finish. Train home from Makiochi at about 20:10.', note: 'Minoh Beer: closed Thursdays (have dinner at Kurobee instead), shuts at 20:00 on Sundays', photo: ['ahoya', 0] },
        endL: { time: '17:25', area: 'Minoh & Makiochi', title: 'Donuts, takoyaki & craft beer', text: 'A break at Japan’s first Mister Donut, then my favorite takoyaki shop. A toast at the Minoh Beer taproom from about 18:25, and ramen at Kurobee to finish. Train home from Makiochi at about 20:30.', note: 'Minoh Beer: closed Thursdays (have dinner at Kurobee instead), shuts at 20:00 on Sundays', photo: ['ahoya', 0] },
        endNo: { time: '16:15', area: 'Minoh & Makiochi', title: 'Donuts, takoyaki & craft beer', text: 'A break at Japan’s first Mister Donut, then my favorite takoyaki shop. A toast at the Minoh Beer taproom from about 17:15, and ramen at Kurobee to finish. Train home from Makiochi at about 19:20.', note: 'Minoh Beer: closed Thursdays (have dinner at Kurobee instead), shuts at 20:00 on Sundays', photo: ['ahoya', 0] }
      },
      howPick: { title: 'Choose your start time and the onsen', text: 'At the top of the “Spots” list there are two rows of buttons. The first is your start time: “Early start” (leave Umeda by 8:30, lunch on the river terrace) or “Late start” (leave around 10:00, no terrace lunch). The second is whether you go to Minoh Onsen. If tattoos keep you out of the bath, choose “No onsen”. The numbers and times change when you tap.' },
      howRest: [
        { title: 'Follow the numbers', text: 'Spots 1–{n} are in order. Follow them and you can see everything in one day.' },
        { title: 'Tap a number', text: 'Tap a number on the map, or open the list, to see photos, tips and suggested times.' },
        { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions. Some spots also link to timetables and official websites.' },
        { title: 'Times are rough guides', text: 'Short on time? Skip a spot. Love a place? Stay longer. Go at your own pace.' }
      ]
    }
  }
};

/* コースごとの紹介ページ（lead・who・dayHead・day・how）を introParts から組み立てる。
   day の並びは、データの sections の day（何番目か）と合わせてある（scripts/build_minoh_courses.py の SECTIONS）。 */
(function () {
  var SEQ = {
    'early': ['busE', 'templeE', 'walkE', 'lunch', 'onsenE', 'endE'],
    'early-noonsen': ['busE', 'templeE', 'walkE', 'lunch', 'strollE', 'endNo'],
    'late': ['busL', 'templeL', 'walkL', 'onsenL', 'endL'],
    'late-noonsen': ['busL', 'templeL', 'walkLNo', 'strollL', 'endNo']
  };
  var COUNT = { 'early': 14, 'early-noonsen': 13, 'late': 13, 'late-noonsen': 12 };
  Object.keys(window.MINOH_I18N).forEach(function (l) {
    var t = window.MINOH_I18N[l], p = t.introParts;
    t.introFor = {};
    Object.keys(SEQ).forEach(function (id) {
      var start = id.indexOf('late') === 0 ? 'late' : 'early', onsen = /noonsen$/.test(id) ? 'no' : 'yes';
      t.introFor[id] = {
        lead: p.lead + (l === 'ja' ? '' : ' ') + p.leadPick + (l === 'ja' ? '' : ' ') + p.leadNow[id],
        who: p.who.common.concat(p.who.start[start], p.who.onsen[onsen], p.who.cash[start], p.who.end),
        dayHead: p.dayHead[id],
        day: SEQ[id].map(function (k) { return p.day[k]; }),
        how: [p.howPick].concat(p.howRest.map(function (h) { return { title: h.title, text: h.text.replace('{n}', COUNT[id]) }; }))
      };
    });
    // 何も選んでいないとき（早めに出発・温泉に入る）の内容を intro に入れておく
    Object.keys(t.introFor.early).forEach(function (k) { t.intro[k] = t.introFor.early[k]; });
  });
})();
