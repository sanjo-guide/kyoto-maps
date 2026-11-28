/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都7:32の特急で出発。コースは2つ（一覧の上のボタン）：late＝城崎温泉だけ（9:52着。最初に開く）、early＝竹田城跡に寄ってから城崎温泉（14:35着）。
   intro は共通の項目で、コースで変わる項目（h1・lead・who・day）は introFor[コース] が app.js で上書きされる（scripts/sync_kinosaki.py）。
   Photos are [spot id, photo index] from data/routes/kinosaki.json / kinosaki-early.json.
   料金・時間は2026年11月22日に確認（外湯は城崎温泉観光協会、タトゥーは Visit Kinosaki、竹田城跡は朝来市の公式ホームページ、天空バスは全但バス、電車は乗換案内）。
   2026年11月24日に要確認を見直し（外湯の支払い＝Visit Kinosaki のよくある質問、温泉寺＝公式サイトと Visit Kinosaki、12月からの天空バスはまだ未発表）。 */
window.KINOSAKI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から日帰り 城崎温泉・竹田城跡 Kinosaki Onsen MAP',
    titleMain: '城崎温泉',
    titleSub: 'Kinosaki Onsen',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '外湯は6か所（駅のとなりのさとの湯は休み）で、曜日ごとに休みます：月＝地蔵湯、火＝鴻の湯、水＝一の湯・まんだら湯、木＝御所の湯・柳湯。どこもタトゥーOK。帰りの最後の特急は18:53発です。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（温泉寺とロープウェイの写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    bus: 'バス',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトなどで確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '最初は、時間割どおりに回れる組み合わせが選ばれています。めやすの時間は、その組み合わせで回るときのものです。休みの外湯は「行く」を押して外し、代わりの外湯の「行きたい」を押してください。駅は自動で入ります。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたい外湯を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    swCourse: 'コース',
    courseAria: 'コース',
    courseEarly: '竹田城跡に寄る\n（城崎 14:35着）',
    courseLate: '城崎温泉だけ\n（城崎 9:52着）',
    swMode: '回り方',
    intro: {
      kicker: 'Toshiが歩いて作った日帰りルート',
      favLabel: 'いちばんの見どころ',
      favName: '外湯めぐり',
      favText: '柳並木の川沿いに外湯が並びます。1か所800円、1日券は1,500円。どこもタトゥーOK。',
      favPhoto: ['river', 0],
      whoHead: '出かける前に',
      dayHead: '1日の流れ（目安）',
      from: '',
      timeSuffix: '〜',
      dealsHead: '交通費・料金のめやす',
      dealsLead: '特急は京都から城崎温泉まで片道5,370〜5,570円（指定席。日によって変わります）。竹田城跡に寄る日の行きは、京都→竹田4,700〜4,900円と竹田→城崎温泉860円です。',
      deals: [
        { name: '特急（京都↔城崎温泉）', price: '片道5,370円〜', text: '乗車券2,640円＋指定席2,730〜2,930円。行きは7:32発のきのさき1号、帰りは18:53発（福知山で乗り換え。最後の特急）か16:31発（乗り換えなし）。', url: 'https://www.jr-odekake.net/' },
        { name: '外湯めぐり1日券「ゆめぱ」', price: '1,500円', text: '外湯の窓口で買えて、その日は入り放題。1か所だけなら800円なので、2か所入るなら1日券です。', url: 'https://kinosaki-spa.gr.jp/about/spa/7onsen/' },
        { name: '城崎温泉ロープウェイ', price: '往復1,200円', text: '山頂駅まで。11月1日〜1月31日は上りの最終16:30、下りの最終16:50。第2・第4木曜休み。', url: 'https://www.kinosaki-ropeway.jp/ropeway' },
        { name: '竹田城跡', price: '500円', text: '高校生以上。中学生以下は無料。1月4日〜2月末は冬の閉山で入れません。', url: 'https://www.city.asago.hyogo.jp/site/takeda/' },
        { name: '天空バス（竹田駅↔竹田城跡）', price: '1日券500円', text: '片道300円なので、往復なら1日フリー乗車券。現金のみ。9〜11月は竹田駅10:05発、帰りは竹田城跡12:15発か12:50発。12月からの時刻は11月24日の時点で未発表です（要確認）。', url: 'https://www.zentanbus.co.jp/local_bus/tenkubus/' }
      ],
      dealsNote: '大人の運賃・料金です。2026年11月22日に確認しました（電車は乗換案内、外湯は城崎温泉観光協会、ロープウェイは公式サイト、竹田城跡は朝来市の公式ホームページ、天空バスは全但バス）。',
      dealsMore: '公式サイトで見る',
      howHead: 'このマップの使い方',
      how: [
        { title: 'コースを選ぶ', text: '一覧の上のボタンで「城崎温泉だけ」か「竹田城跡に寄る」を選ぶと、時間割と順番がそのコースに変わります。どちらも京都7:32発です。' },
        { title: '休みの外湯は外す', text: '最初は、時間割どおりに回れる外湯が選ばれています。外湯は曜日ごとに休むので、休みの外湯は「行く」を押して外し、代わりの外湯を選んでください。' },
        { title: '番号をタップ', text: '地図の番号か「一覧」をタップすると、写真・説明・営業時間・休みの日・おすすめの時間が見られます。' },
        { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。公式サイトへのリンクもあります。' }
      ],
      cta: '地図を見る',
      footer1: 'Toshiが実際に歩いて作った、オリジナルマップです。'
    },
    introFor: {
      "late": {
        "h1": "柳並木の温泉街で、外湯を4つとロープウェイ。京都から日帰りで城崎温泉。",
        "lead": "太鼓橋のかかる大谿川に柳が並び、その川沿いに外湯が点在する温泉街。1日券「ゆめぱ」を持って、洞窟風呂の一の湯、露天風呂のある御所の湯、ロープウェイで大師山に上ったあとの鴻の湯と、湯から湯へ歩きます。夕方は灯りのつく川沿いで早めの晩ごはん。京都7:32の特急に乗れば乗り換えなしで9:52に着き、帰りは18:53の最後の特急です（16:31の特急で早めに帰って、京都で晩ごはんにもできます）。外湯はどこもタトゥーOKです。",
        "who": [
          "三条のあたりを6:45ごろに出て、21:40ごろに戻る1日（16:31発で帰れば19:30ごろ）",
          "外湯はどこもタトゥーOK。隠す必要もなし（公式観光サイト Visit Kinosaki の案内）",
          "外湯は曜日ごとに休み：月＝地蔵湯、火＝鴻の湯、水＝一の湯・まんだら湯、木＝御所の湯・柳湯",
          "1か所800円、1日券「ゆめぱ」1,500円。2か所入るなら1日券",
          "ロープウェイは11〜1月、上りの最終16:30・下りの最終16:50（第2・第4木曜休み）",
          "帰りの最後の特急は18:53発。指定席は行きと一緒に買っておく",
          "7:32に乗り遅れても、8:38発（福知山乗り換え）で10:58に着きます"
        ],
        "dayHead": "1日の流れ（城崎温泉だけ）",
        "day": [
          {
            "time": "6:45",
            "area": "三条のあたり → 京都駅",
            "title": "7:32の特急で出発",
            "text": "地下鉄で京都駅へ。特急きのさき1号は乗り換えなしで9:52に城崎温泉に着きます。",
            "photo": [
              "kyoto",
              0
            ]
          },
          {
            "time": "9:52",
            "area": "城崎温泉駅 → 地蔵湯 → 一の湯",
            "title": "午前の外湯とお昼",
            "text": "駅に近い地蔵湯で1日券を買い、柳並木の川沿いを歩いて一の湯へ。12時ごろにお昼。",
            "photo": [
              "river",
              1
            ]
          },
          {
            "time": "13:10",
            "area": "御所の湯 → ロープウェイ → 鴻の湯",
            "title": "温泉街の奥へ",
            "text": "御所の湯のあと、14:10のロープウェイで大師山の上へ。下りたら、となりの鴻の湯に入ります。",
            "badge": "冬は上りの最終16:30",
            "photo": [
              "gosho",
              0
            ]
          },
          {
            "time": "16:20",
            "area": "まんだら湯 → 柳湯",
            "title": "15時に開く外湯",
            "text": "駅へ戻りながら、もう1つ入りたい人に。入らないなら、お土産を見たり早めの晩ごはんへ。",
            "badge": "入りたい人だけ",
            "photo": [
              "mandara",
              0
            ]
          },
          {
            "time": "17:15",
            "area": "夜の温泉街 → 京都へ",
            "title": "早めの晩ごはんと、灯りの川沿い",
            "text": "城崎で晩ごはんを済ませて、18:35に駅へ。18:53の特急で京都21:20着。",
            "note": "18:53が最後の特急です",
            "photo": [
              "night",
              0
            ]
          }
        ]
      },
      "early": {
        "h1": "天空の城から、柳並木の温泉街へ。竹田城跡と城崎温泉を1日で。",
        "lead": "山の上に石垣だけが残る「天空の城」竹田城跡。石垣の上からは、但馬の山と町が360度見渡せます。午後は電車で城崎温泉へ行き、柳並木の川沿いで外湯を3つ。洞窟風呂の一の湯、露天風呂のある御所の湯に入り、早めの晩ごはんのあと18:53の特急で京都へ（21:20着）。京都7:32の特急を和田山で乗り換えて竹田9:36着、10:05の天空バスで城跡へ上がり、12:30に駅へ戻ってお昼、13:34の電車で城崎温泉へ（14:35着）。電車とバスの本数が少ないので、時刻どおりに動く1日です。",
        "who": [
          "三条のあたりを6:45ごろに出て、21:40ごろに戻る長い1日",
          "天空バスは現金のみ（1日券500円）。歩いて登る駅裏の道は閉鎖中",
          "竹田13:34発の電車は必ず。次は15:23発で、城崎温泉に着くのは17:40",
          "城崎の外湯は3つがちょうどいい量。どこもタトゥーOK",
          "外湯は曜日ごとに休み：月＝地蔵湯、火＝鴻の湯、水＝一の湯・まんだら湯、木＝御所の湯・柳湯",
          "竹田城跡は1月4日〜2月末は閉山。12月からの天空バスの時刻は未発表（要確認）",
          "帰りの最後の特急は18:53発。指定席は行きと一緒に買っておく"
        ],
        "dayHead": "1日の流れ（竹田城跡に寄る）",
        "day": [
          {
            "time": "6:45",
            "area": "三条のあたり → 京都駅",
            "title": "7:32の特急で出発",
            "text": "特急きのさき1号を和田山で降りて、播但線に乗り換え。竹田に9:36に着きます。",
            "photo": [
              "kyoto",
              0
            ]
          },
          {
            "time": "10:05",
            "area": "竹田城跡 → 竹田駅",
            "title": "天空の城の石垣を歩く",
            "text": "10:05の天空バスで山の中腹へ、そこから歩いて20分。12:15のバスで駅に戻ってお昼、13:34の電車に乗ります。",
            "badge": "13:34発は必ず",
            "photo": [
              "takeda",
              0
            ]
          },
          {
            "time": "14:35",
            "area": "城崎温泉駅 → 地蔵湯 → 大谿川",
            "title": "柳並木の温泉街へ",
            "text": "駅に近い地蔵湯で1日券を買って、まず1つ目。柳並木と太鼓橋の川沿いを歩きます。",
            "photo": [
              "river",
              1
            ]
          },
          {
            "time": "15:40",
            "area": "一の湯 → 御所の湯",
            "title": "外湯をあと2つ",
            "text": "洞窟風呂の一の湯と、露天風呂のある御所の湯。休みの曜日は柳湯かまんだら湯に替えます。",
            "photo": [
              "ichi",
              0
            ]
          },
          {
            "time": "17:15",
            "area": "夜の温泉街 → 京都へ",
            "title": "早めの晩ごはんと、灯りの川沿い",
            "text": "城崎で晩ごはんを済ませて、18:35に駅へ。18:53の特急で京都21:20着。",
            "note": "18:53が最後の特急です",
            "photo": [
              "night",
              0
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto: Kinosaki Onsen & Takeda Castle MAP',
    titleMain: 'Kinosaki Onsen',
    titleSub: '城崎温泉',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Six bathhouses (Sato-no-yu by the station is closed), each shut one day a week: Mon Jizo-yu · Tue Kou-no-yu · Wed Ichi-no-yu, Mandara-yu · Thu Gosho-no-yu, Yanagi-yu. Tattoos are fine at all of them. The last express back leaves at 18:53. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (the Onsen-ji and ropeway photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    bus: 'Bus',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and similar sources on {d}. Details can change, so please check before you go.',
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
    pickNote: 'A set that fits the timetable is chosen to start with, and the rough times are for that set. Tap “Going” to drop a bath that is closed today and “Want to go” on another one instead. Stations are added automatically.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: 'Nothing chosen yet. Pick the baths you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    swCourse: 'Course',
    courseAria: 'Course',
    courseEarly: 'With Takeda Castle\n(Kinosaki 14:35)',
    courseLate: 'Kinosaki only\n(arrive 9:52)',
    swMode: 'Stops',
    intro: {
      kicker: 'A day trip, hand-walked by Toshi',
      favLabel: 'Don’t miss',
      favName: 'Bathhouse hopping',
      favText: 'Public baths along a willow-lined river: ¥800 each or ¥1,500 for a day pass. Tattoos are fine at all of them.',
      favPhoto: ['river', 0],
      whoHead: 'Before you go',
      dayHead: 'One day, roughly like this',
      from: 'From',
      timeSuffix: '',
      dealsHead: 'Fares and fees',
      dealsLead: 'The express from Kyoto to Kinosaki Onsen is ¥5,370–5,570 each way (reserved seat; it depends on the day). Via Takeda Castle, the way out is ¥4,700–4,900 (Kyoto → Takeda) plus ¥860 (Takeda → Kinosaki Onsen).',
      deals: [
        { name: 'Limited express (Kyoto ↔ Kinosaki Onsen)', price: 'from ¥5,370 one way', text: 'Fare ¥2,640 + reserved seat ¥2,730–2,930. Out on the 7:32 Kinosaki No. 1; back on the 18:53 (change at Fukuchiyama; the last express) or the 16:31 (direct).', url: 'https://www.jr-odekake.net/' },
        { name: '“Yumepa” onsen day pass', price: '¥1,500', text: 'Sold at the bathhouse counters; unlimited baths that day. A single bath is ¥800, so the pass pays from two baths.', url: 'https://visitkinosaki.com/about-kinosaki/the-7-mystic-onsen/' },
        { name: 'Kinosaki Ropeway', price: '¥1,200 return', text: 'To the top station. From 1 Nov to 31 Jan the last car up is 16:30 and the last down 16:50. Closed 2nd and 4th Thursdays.', url: 'https://www.kinosaki-ropeway.jp/ropeway' },
        { name: 'Takeda Castle Ruins', price: '¥500', text: 'High school and up; junior high and under free. Closed for winter 4 Jan – end of Feb.', url: 'https://www.city.asago.hyogo.jp/site/takeda/' },
        { name: 'Tenku Bus (Takeda Station ↔ castle)', price: '¥500 day pass', text: '¥300 each way, so buy the 1-day pass for a return trip. Cash only. Sep–Nov: leaves Takeda Station at 10:05; back from the castle stop at 12:15 or 12:50. Times from December had not been published as of 24 Nov (please check).', url: 'https://www.zentanbus.co.jp/local_bus/tenkubus/' }
      ],
      dealsNote: 'Adult prices, checked on Nov 22, 2026 (trains on a route planner, baths with the Kinosaki Onsen Tourism Association, the ropeway on its official site, the castle on Asago City’s official site, the Tenku Bus with Zentan Bus).',
      dealsMore: 'See official site',
      howHead: 'How to use this map',
      how: [
        { title: 'Choose a course', text: 'Use the buttons above the list to choose “Kinosaki only” or “With Takeda Castle”; the timetable and order change to match. Both leave Kyoto at 7:32.' },
        { title: 'Drop the closed bath', text: 'The baths that fit the timetable are chosen to start with. Each bath closes one day a week, so tap “Going” to drop the closed one and pick another instead.' },
        { title: 'Tap a number', text: 'Tap a number on the map, or open the list, to see photos, tips, opening hours, closing days and suggested times.' },
        { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions. Some spots also link to official websites.' }
      ],
      cta: 'Open the map',
      footer1: 'An original map, hand-walked by Toshi.'
    },
    introFor: {
      "late": {
        "h1": "Four baths and a ropeway in a willow-lined onsen town: Kinosaki, a day trip from Kyoto.",
        "lead": "Willows and arched stone bridges line the Otani River, with the public baths spread along the water. With the Yumepa day pass, walk from bath to bath: the cave bath at Ichi-no-yu, the open-air bath at Gosho-no-yu, and Kou-no-yu after the ropeway up Mt. Daishi. In the evening, an early dinner by the lamp-lit river. The 7:32 express from Kyoto runs direct, arriving at 9:52, and the 18:53 is the last express home (or take the 16:31 and have dinner in Kyoto). Tattoos are fine at every public bath.",
        "who": [
          "Leave the Sanjo area around 6:45, back about 21:40 (about 19:30 if you take the 16:31)",
          "Tattoos are fine at every bathhouse, no need to cover them (per Visit Kinosaki, the official tourism site)",
          "Each bath closes one day a week: Mon Jizo-yu · Tue Kou-no-yu · Wed Ichi-no-yu, Mandara-yu · Thu Gosho-no-yu, Yanagi-yu",
          "¥800 per bath; “Yumepa” day pass ¥1,500, worth it from two baths",
          "Ropeway, Nov–Jan: last car up 16:30, last down 16:50 (closed 2nd and 4th Thursdays)",
          "The last express back leaves at 18:53. Buy your return seat with the outbound one",
          "Miss the 7:32? The 8:38 (change at Fukuchiyama) gets you there at 10:58"
        ],
        "dayHead": "The day (Kinosaki only)",
        "day": [
          {
            "time": "6:45",
            "area": "Sanjo area → Kyoto Station",
            "title": "Off on the 7:32 express",
            "text": "Subway to Kyoto Station. The Kinosaki No. 1 runs direct, arriving at 9:52.",
            "photo": [
              "kyoto",
              0
            ]
          },
          {
            "time": "9:52",
            "area": "Kinosaki Station → Jizo-yu → Ichi-no-yu",
            "title": "Morning baths and lunch",
            "text": "Buy the day pass at Jizo-yu near the station, walk the willow-lined river to Ichi-no-yu, and have lunch around noon.",
            "photo": [
              "river",
              1
            ]
          },
          {
            "time": "13:10",
            "area": "Gosho-no-yu → ropeway → Kou-no-yu",
            "title": "To the far end of town",
            "text": "After Gosho-no-yu, take the 14:10 ropeway up Mt. Daishi. Back down, Kou-no-yu is next door.",
            "badge": "Winter: last car up 16:30",
            "photo": [
              "gosho",
              0
            ]
          },
          {
            "time": "16:20",
            "area": "Mandara-yu → Yanagi-yu",
            "title": "The baths that open at 15:00",
            "text": "For one more bath on the way back to the station. Otherwise browse the shops or go for an early dinner.",
            "badge": "Optional",
            "photo": [
              "mandara",
              0
            ]
          },
          {
            "time": "17:15",
            "area": "Evening → back to Kyoto",
            "title": "Early dinner and the lit-up river",
            "text": "Eat in Kinosaki and be at the station by 18:35. The 18:53 express reaches Kyoto at 21:20.",
            "note": "The 18:53 is the last express",
            "photo": [
              "night",
              0
            ]
          }
        ]
      },
      "early": {
        "h1": "From the castle in the sky to a willow-lined onsen town: Takeda Castle and Kinosaki in one day.",
        "lead": "Takeda Castle, the “castle in the sky”, is only stone walls on a mountaintop, with the hills and towns of Tajima all around you. In the afternoon, three public baths along the willow-lined river in Kinosaki Onsen, including the cave bath at Ichi-no-yu and the open-air bath at Gosho-no-yu, then an early dinner and the 18:53 express back to Kyoto (21:20). Take the 7:32 express from Kyoto, change at Wadayama for Takeda (9:36) and ride the 10:05 Tenku Bus up to the ruins; back at the station at 12:30 for lunch, then the 13:34 train to Kinosaki Onsen (14:35). Trains and buses are few, so this day runs to the clock.",
        "who": [
          "A long day: leave the Sanjo area around 6:45, back about 21:40",
          "The Tenku Bus is cash only (day pass ¥500). The walking trails from the station are closed",
          "Don’t miss the 13:34 from Takeda: the next is 15:23, reaching Kinosaki at 17:40",
          "Three baths is the right amount in Kinosaki. Tattoos are fine at all of them",
          "Each bath closes one day a week: Mon Jizo-yu · Tue Kou-no-yu · Wed Ichi-no-yu, Mandara-yu · Thu Gosho-no-yu, Yanagi-yu",
          "Takeda Castle is closed 4 Jan – end of Feb. Tenku Bus times from December are not yet published (please check)",
          "The last express back leaves at 18:53. Buy your return seat with the outbound one"
        ],
        "dayHead": "The day (with Takeda Castle)",
        "day": [
          {
            "time": "6:45",
            "area": "Sanjo area → Kyoto Station",
            "title": "Off on the 7:32 express",
            "text": "Get off the Kinosaki No. 1 at Wadayama and change to the Bantan Line, arriving in Takeda at 9:36.",
            "photo": [
              "kyoto",
              0
            ]
          },
          {
            "time": "10:05",
            "area": "Takeda Castle → Takeda Station",
            "title": "Walls of the castle in the sky",
            "text": "The 10:05 Tenku Bus halfway up, then a 20-minute walk. Back on the 12:15 bus for lunch by the station and the 13:34 train.",
            "badge": "Don’t miss the 13:34",
            "photo": [
              "takeda",
              0
            ]
          },
          {
            "time": "14:35",
            "area": "Kinosaki Station → Jizo-yu → Otani River",
            "title": "Into the willow-lined town",
            "text": "Buy the day pass at Jizo-yu near the station for your first bath, then walk the river with its willows and arched bridges.",
            "photo": [
              "river",
              1
            ]
          },
          {
            "time": "15:40",
            "area": "Ichi-no-yu → Gosho-no-yu",
            "title": "Two more baths",
            "text": "Ichi-no-yu with its cave bath and Gosho-no-yu with its open-air bath. On their closed days, use Yanagi-yu or Mandara-yu.",
            "photo": [
              "ichi",
              0
            ]
          },
          {
            "time": "17:15",
            "area": "Evening → back to Kyoto",
            "title": "Early dinner and the lit-up river",
            "text": "Eat in Kinosaki and be at the station by 18:35. The 18:53 express reaches Kyoto at 21:20.",
            "note": "The 18:53 is the last express",
            "photo": [
              "night",
              0
            ]
          }
        ]
      }
    }
  }
};
