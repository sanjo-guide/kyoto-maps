/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都駅→坂本（近江神宮・旧竹林院・日吉大社）→坂本ケーブル→延暦寺 東塔・西塔・横川→比叡山頂→叡山ロープウェイ・ケーブル→八瀬→叡山電車で出町柳。
   オーナーの写真は東塔の鐘楼ともみじ・日吉大社の赤鳥居・山頂の眺め（2016年11月）、近江神宮（2025年1月）、八瀬（2024年12月）。ほかは Wikimedia Commons。
   Photos are [spot number, photo index] from data/routes/hieizan.json.
   時刻・料金は2026年11月21日に確認（延暦寺・坂本ケーブル・京福電鉄・叡山電車・比叡山びわ湖DMOの公式サイト、乗換案内）。
   冬（2026年は12月7日〜）は叡山ケーブル・ロープウェイと山内シャトルバスが運休。2027年の再開日とパスの値段が出たら直す。 */
window.HIEIZAN_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から日帰り 比叡山延暦寺と坂本 Mt. Hiei MAP',
    titleMain: '比叡山延暦寺と坂本',
    titleSub: 'Mt. Hiei & Sakamoto',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '坂本の町と日吉大社を歩いてからケーブルカーで上がり、延暦寺の東塔・西塔・横川を回って、京都側の八瀬へ下りる順番です。冬（12月7日〜春）は京都側のケーブルと山内のバスが運休するので、東塔を見て坂本へ戻ります。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（私の写真は東塔の鐘楼ともみじ、日吉大社の赤鳥居、山頂の眺め、近江神宮、八瀬。そのほかは Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車・バス',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。半日なら日吉大社と東塔だけ。冬は「山頂とロープウェイ」「横川」を外してください。',
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
      "kicker": "Toshiが作った京都からの日帰りルート",
      "h1": "滋賀側からケーブルカーで上がり、延暦寺を回って、京都側へ下りる。",
      "lead": "比叡山延暦寺は、山の上に3つのエリアが離れてある大きなお寺です。京都からJRで16分の坂本で石垣の町と日吉大社を歩き、日本一長いケーブルカーで東塔へ。シャトルバスで西塔・横川を回り、ロープウェイとケーブルカーで八瀬へ下ります。この回り方ができるのは3月20日ごろから12月はじめまで（2026年は12月6日まで）。冬は京都側のケーブル・ロープウェイと山内のバスが運休するので、坂本から東塔を往復します。紅葉は10月下旬から11月。山の上は町よりずっと寒いです。根本中堂は大改修中で、今は中に入れません。",
      "favLabel": "いちばんの見どころ",
      "favName": "延暦寺 東塔",
      "favText": "最澄が寺を開いた場所。大講堂の鐘楼ともみじ（2016年11月13日）。",
      "favPhoto": [
        7,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "京都の町のお寺をひと通り見て、次は山の上の大きなお寺へ行きたい人に",
        "ケーブルカー2本とロープウェイに乗れます。乗りものが好きな人にも",
        "京都駅からJR湖西線で比叡山坂本駅まで16分・320円",
        "延暦寺は全部のお堂が16:00に閉まります（受付は15:45まで）。3エリア回るなら、坂本ケーブルは11:00発までに",
        "巡拝料は3エリア共通で1,000円。日吉大社500円。現金を用意（京都側のケーブル・ロープウェイは現金のみ）",
        "半日なら、日吉大社と東塔だけ。坂本ケーブルを往復します",
        "12月7日から春までは、京都側のケーブル・ロープウェイと山内のバスが運休。横川へは行けません",
        "山の上は寒いので、秋でも上着を1枚多く。西塔と横川は土の道と石段があります"
      ],
      "dayHead": "1日の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "7:47",
          "area": "坂本",
          "title": "坂本の町と日吉大社",
          "text": "京都駅からJR湖西線で坂本へ（近江神宮に寄る人は大津京で乗り換え）。穴太衆積みの石垣の参道を上り、旧竹林院の庭、日吉大社の西本宮と東本宮へ。",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "11:00",
          "area": "延暦寺",
          "title": "坂本ケーブルで東塔・西塔・横川へ",
          "text": "11:00発のケーブルカーで山の上へ。東塔を見てお昼、13:08発のバスで西塔、14:11発で横川へ。横川は15:30発のバスで出ます。（写真：PlusMinus / CC BY-SA 3.0）",
          "photo": [
            9,
            0
          ]
        },
        {
          "time": "15:50",
          "area": "八瀬",
          "title": "ロープウェイとケーブルで八瀬へ",
          "text": "比叡山頂から16:15発のロープウェイ、16:30発のケーブルカーで八瀬へ。もみじの中を歩いて、17:00発の叡山電車で出町柳へ。",
          "note": "出町柳に17:13着",
          "photo": [
            11,
            3
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と拝観料のめやす",
      "dealsLead": "全部回って京都側へ下りると、乗りものは JR 320円＋坂本ケーブル960円＋山内バス1日券1,200円＋ロープウェイとケーブル1,000円＋叡山電車280円＝3,760円。別に延暦寺1,000円、日吉大社500円です。横川に行かない日は、1日券やフリーパスを買わずに1回ずつ払うほうが安くなります。",
      "deals": [
        {
          "name": "延暦寺 巡拝料",
          "price": "1,000円",
          "text": "東塔・西塔・横川の3エリア共通。9:00〜16:00（西塔・横川は12〜2月 9:30から）。",
          "url": "https://www.hieizan.or.jp/tickets/"
        },
        {
          "name": "坂本ケーブル",
          "price": "960円",
          "text": "片道。往復は1,830円。毎時0分・30分発、11分。冬も動きます。",
          "url": "https://sakamoto-cable.jp/guide/"
        },
        {
          "name": "比叡山内バス1日乗車券",
          "price": "1,200円",
          "text": "山内シャトルバス（比叡山頂〜東塔〜西塔〜横川）が乗り放題。バスの車内で買えます。12月6日まで。",
          "url": "https://www.hieizan.gr.jp/ticket/"
        },
        {
          "name": "叡山ロープウェイ＋ケーブル",
          "price": "1,000円",
          "text": "ロープウェイ400円＋ケーブル600円（片道）。現金のみ。12月6日まで、冬は運休。",
          "url": "https://www.keifuku.co.jp/cms/eizan_ticket/"
        },
        {
          "name": "比叡山フリーパス",
          "price": "3,500円",
          "text": "坂本のバス・坂本ケーブル・山内バス・叡山ロープウェイとケーブル・叡山電車（出町柳まで）が1日乗り放題。坂本観光案内所か出町柳駅で。12月6日まで。巡拝料は別。",
          "url": "https://eizandensha.co.jp/good-value/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21日に確認しました（延暦寺・坂本ケーブル・京福電鉄・叡山電車・比叡山びわ湖DMOの公式サイト、乗換案内）。フリーパスは、坂本でバスに乗って横川まで行く日なら、1回ずつ払うより190円安くなります。坂本から上って坂本へ下りる日は「延暦寺・坂本周遊一日乗車券」（2,500円。巡拝料つき、前の日までにスマホで購入）が得です。パスと1日券の2027年の値段は、春の発表を確認してください。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "番号の順に",
          "text": "1から11の順に回ると、京都駅から坂本、ケーブルカーで延暦寺の3つのエリア、ロープウェイで八瀬へ下りるルートになります。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・おすすめの時間が見られます。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "「選んで回る」に切り替えると、行きたい場所だけを選べます。冬は「横川」と「山頂とロープウェイ」を外してください。帰り方の案内が出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（坂本の町・旧竹林院・坂本ケーブル・西塔・横川は、公式サイトなどの情報と Wikimedia Commons の写真で紹介しています）。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto: Mt. Hiei & Sakamoto MAP',
    titleMain: 'Mt. Hiei & Sakamoto',
    titleSub: '比叡山延暦寺と坂本',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Walk Sakamoto and Hiyoshi Taisha, ride the cable car up, see Enryaku-ji’s Todo, Saito and Yokawa areas, then go down to Yase on the Kyoto side. In winter (7 December to spring) the Kyoto-side cable car and the mountain bus do not run: see Todo and return to Sakamoto. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (my own photos: the Todo bell tower and maples, the red torii of Hiyoshi Taisha, the summit view, Omi Jingu and Yase; the rest are from Wikimedia Commons, with author and license shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train / bus',
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
    pickNote: 'Tap “Want to go” on the places you like. Times are for the full route. For a half day: Hiyoshi Taisha and Todo. In winter, leave out “Summit & ropeway” and “Yokawa”.',
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
      "kicker": "A day trip from Kyoto, by Toshi",
      "h1": "Up by cable car from the Shiga side, round Enryaku-ji, and down to Kyoto.",
      "lead": "Enryaku-ji on Mt. Hiei is a big temple in three areas spread over the mountain. From Sakamoto, 16 minutes from Kyoto by JR, you walk the stone-wall town and Hiyoshi Taisha, ride Japan’s longest cable car up to the Todo area, take the shuttle bus to Saito and Yokawa, and come down to Yase by ropeway and cable car. This full crossing works from about 20 March to early December (until 6 December in 2026). In winter the Kyoto-side cable car and ropeway and the mountain bus stop, so you go up from Sakamoto to Todo and back. Autumn colour runs from late October through November. It is much colder on the mountain than in town. The Konpon Chudo is under major repair and closed inside for now.",
      "favLabel": "Highlight",
      "favName": "Enryaku-ji: Todo",
      "favText": "Where Saicho founded the temple. The bell tower by the Great Lecture Hall, with maples (13 November 2016).",
      "favPhoto": [
        7,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "For people who have seen Kyoto’s city temples and want a big one on a mountain next",
        "Two cable cars and a ropeway: good if you like rides too",
        "16 minutes and ¥320 from Kyoto Station to Hieizan-Sakamoto on the JR Kosei line",
        "Every hall at Enryaku-ji closes at 16:00 (last entry 15:45). For all three areas, be on the Sakamoto Cable by 11:00",
        "Admission is ¥1,000 for all three areas; Hiyoshi Taisha ¥500. Bring cash (the Kyoto-side cable car and ropeway are cash only)",
        "Half a day? Hiyoshi Taisha and Todo, with a return on the Sakamoto Cable",
        "From 7 December until spring the Kyoto-side cable car and ropeway and the mountain bus do not run, and Yokawa is out of reach",
        "It is cold up there: one more layer, even in autumn. Saito and Yokawa have earth paths and stone steps"
      ],
      "dayHead": "One day, roughly like this",
      "from": "From",
      "day": [
        {
          "time": "7:47",
          "area": "Sakamoto",
          "title": "Sakamoto and Hiyoshi Taisha",
          "text": "JR Kosei line from Kyoto to Sakamoto (change at Otsukyo if you add Omi Jingu). Up the avenue of stone walls, the garden of Kyu Chikurin-in, then the west and east shrines of Hiyoshi Taisha.",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "11:00",
          "area": "Enryaku-ji",
          "title": "Cable car to Todo, Saito and Yokawa",
          "text": "The 11:00 cable car up the mountain. Todo and lunch, the 13:08 bus to Saito, the 14:11 on to Yokawa. Leave Yokawa on the 15:30 bus. (Photo: PlusMinus / CC BY-SA 3.0)",
          "photo": [
            9,
            0
          ]
        },
        {
          "time": "15:50",
          "area": "Yase",
          "title": "Ropeway and cable car down to Yase",
          "text": "From the summit, the 16:15 ropeway and the 16:30 cable car to Yase. Walk through the maples and take the 17:00 Eizan train to Demachiyanagi.",
          "note": "Demachiyanagi 17:13",
          "photo": [
            11,
            3
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "The full crossing to the Kyoto side costs, in rides: JR ¥320 + Sakamoto Cable ¥960 + mountain bus day ticket ¥1,200 + ropeway and cable car ¥1,000 + Eizan railway ¥280 = ¥3,760. Enryaku-ji (¥1,000) and Hiyoshi Taisha (¥500) are extra. On a day without Yokawa, single fares come out cheaper than the day ticket or the pass.",
      "deals": [
        {
          "name": "Enryaku-ji admission",
          "price": "¥1,000",
          "text": "One ticket for Todo, Saito and Yokawa. 9:00–16:00 (Saito and Yokawa from 9:30, Dec–Feb).",
          "url": "https://www.hieizan.or.jp/tickets/"
        },
        {
          "name": "Sakamoto Cable",
          "price": "¥960",
          "text": "One way; ¥1,830 return. On the hour and half hour, 11 minutes. Runs in winter too.",
          "url": "https://sakamoto-cable.jp/guide/"
        },
        {
          "name": "Mountain shuttle bus day ticket",
          "price": "¥1,200",
          "text": "Unlimited rides between the summit, Todo, Saito and Yokawa. Sold on the bus. Until 6 December.",
          "url": "https://www.hieizan.gr.jp/ticket/"
        },
        {
          "name": "Eizan Ropeway + Cable",
          "price": "¥1,000",
          "text": "Ropeway ¥400 + cable car ¥600, one way. Cash only. Until 6 December; closed in winter.",
          "url": "https://www.keifuku.co.jp/cms/eizan_ticket/"
        },
        {
          "name": "Hieizan Free Pass",
          "price": "¥3,500",
          "text": "One day on the Sakamoto bus, Sakamoto Cable, mountain bus, Eizan Ropeway and Cable and the Eizan railway to Demachiyanagi. From the Sakamoto tourist office or Demachiyanagi station. Until 6 December. Admission not included.",
          "url": "https://eizandensha.co.jp/good-value/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 21, 2026 (Enryaku-ji, Sakamoto Cable, Keifuku, Eizan railway and Hieizan-Biwako DMO websites; route planner). The Free Pass saves ¥190 over single fares on a day when you take the bus in Sakamoto and go as far as Yokawa. If you go up and down the Sakamoto side, the Enryaku-ji & Sakamoto 1-day ticket (¥2,500, admission included, bought online by the day before) is the better deal. For 2027 pass prices, check the spring announcements.",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "In number order",
          "text": "Follow 1 to 11: Kyoto Station to Sakamoto, the cable car up to the three areas of Enryaku-ji, and the ropeway down to Yase."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees and suggested times."
        },
        {
          "title": "Skip what you like",
          "text": "Switch to “Choose stops” to pick only the places you want. In winter, leave out Yokawa and “Summit & ropeway”: the map then tells you how to get back."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi (Sakamoto, Kyu Chikurin-in, the Sakamoto Cable, Saito and Yokawa are introduced from official websites and other sources, with photos from Wikimedia Commons)."
    }
  }
};
