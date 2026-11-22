/* Page texts in Japanese and English.
   Toshi 個人のマップ。4月中旬だけの春のマップ：京阪 天満橋駅→大阪城 西の丸庭園→造幣局 桜の通り抜け→毛馬桜之宮公園。
   Photos are [spot number, photo index] from data/routes/osaka-sakura.json.
   日時・料金は2026年11月21日に確認（造幣局の公式サイト＝2026年の開催情報、電車は乗換案内）。2027年の日程が出たら直す。
   「選んで回る」はないので、pick の文言は使われない。 */
window.OSAKA_SAKURA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '大阪 造幣局の桜の通り抜け Osaka Sakura MAP',
    titleMain: '造幣局の桜の通り抜け',
    titleSub: 'Osaka Mint cherry walk',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '4月中旬の1週間だけのマップです。造幣局は南門から北門への一方通行なので、番号の順に回ってください。点線は順番を示す線で、実際の道ではありません。',
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
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '行きたい場所の「行きたい」を押してください。',
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
      "kicker": "春だけのマップ（4月中旬の1週間）",
      "h1": "年に1週間だけ開く、造幣局の八重桜の道へ。",
      "lead": "このマップが使えるのは、造幣局の「桜の通り抜け」が開いている4月中旬の約1週間だけです（2026年は4月9日〜15日）。京都から京阪で天満橋へ。大阪城の西の丸庭園、造幣局の約560mの八重桜の道、大川沿いの桜並木を、午後から夕方にかけて歩きます。造幣局は事前の申し込みが必要です。",
      "favLabel": "いちばんの見どころ",
      "favName": "造幣局 桜の通り抜け",
      "favText": "140品種・331本（2026年）。ぼんぼりに灯が入る夕方がおすすめです。",
      "favPhoto": [
        3,
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "4月中旬の1週間だけ。2027年の日程は3月に発表されます（要確認）",
        "造幣局は事前申込制（インターネット・先着順）。申し込んだ時間帯に入ります",
        "通り抜けは一方通行で、中では飲食できません。日傘・自撮り棒・三脚も使えません",
        "大阪城のソメイヨシノは1週間ほど早く咲くので、重ならない年もあります",
        "京都の祇園四条から天満橋まで、京阪の特急で46分（490円）"
      ],
      "dayHead": "半日の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "15:16",
          "area": "天満橋・大阪城",
          "title": "西の丸庭園で、桜ごしの天守閣",
          "text": "天満橋駅から歩いて大阪城へ。芝生の庭から、桜の間に天守閣を見上げます（入園は16:30まで）。",
          "photo": [
            2,
            1
          ]
        },
        {
          "time": "17:15",
          "area": "造幣局",
          "title": "八重桜の通り抜け",
          "text": "南門から北門へ、約560mの一方通行。品種の札を見ながら、ぼんぼりの灯る道を歩きます。",
          "photo": [
            3,
            1
          ]
        },
        {
          "time": "18:15",
          "area": "大川",
          "title": "川沿いの桜並木を歩いて帰る",
          "text": "桜宮橋を渡って毛馬桜之宮公園へ。夕日の川沿いを歩いて、天満橋駅か桜ノ宮駅へ。",
          "note": "京都着は21時前",
          "photo": [
            4,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と料金",
      "dealsLead": "電車は京阪の祇園四条⇄天満橋が片道490円。現地はすべて歩きです。西の丸庭園は桜の時期350円、毛馬桜之宮公園は無料です。",
      "deals": [
        {
          "name": "京阪（祇園四条 ⇄ 天満橋）",
          "price": "片道490円",
          "text": "特急で46分、乗り換えなし。祇園四条14:30発→天満橋15:16着。帰りは天満橋20:04発→祇園四条20:50着。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "造幣局 桜の通り抜け",
          "price": "事前申込制",
          "best": "先に申し込む",
          "text": "2026年はインターネットで入場の時間帯を選ぶ先着順で、3月18日に受付が始まりました。2027年の日程と方法は、3月に造幣局の公式サイトで発表されます（要確認）。",
          "url": "https://www.mint.go.jp/enjoy/toorinuke/"
        },
        {
          "name": "大阪城 西の丸庭園",
          "price": "350円（桜の時期）",
          "text": "9:00〜17:00（入園は16:30まで）、月曜休み。夜桜のライトアップがある年は、夜も入れます（日程は要確認）。",
          "url": "https://osakacastlepark.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21日に確認しました（造幣局の公式サイトの2026年の開催情報、大阪周遊パスの公式サイトの施設案内、電車は乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "4月中旬だけのマップです",
          "text": "造幣局の桜の通り抜けが開いている約1週間のためのマップです。まず公式サイトで日程を見て、入場を申し込んでください。"
        },
        {
          "title": "番号の順に",
          "text": "1から4の順に回ると、天満橋駅から大阪城、造幣局の南門、北門を出て川沿いの桜並木へと歩けます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・おすすめの時間が見られます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです（写真は2025年4月と2026年4月）。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Osaka: the Mint cherry-blossom walk MAP',
    titleMain: 'Osaka Mint cherry walk',
    titleSub: '造幣局の桜の通り抜け',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'A map for one week in mid-April only. The Mint is one way from the south gate to the north gate, so follow the numbers. The dotted line shows the order, not the actual path.',
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
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
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
    pickNote: 'Tap “Want to go” on the places you like.',
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
      "kicker": "A spring-only map (one week in mid-April)",
      "h1": "The Mint’s avenue of double cherry blossoms, open one week a year.",
      "lead": "This map works only during the roughly one week in mid-April when the Japan Mint’s cherry-blossom walk is open (9–15 April in 2026). Take the Keihan line from Kyoto to Temmabashi, then walk Osaka Castle’s Nishinomaru Garden, the Mint’s 560 m of double-flowered cherries and the riverside avenue along the Okawa, from afternoon into evening. The Mint requires advance booking.",
      "favLabel": "Highlight",
      "favName": "Japan Mint cherry-blossom walk",
      "favText": "331 trees of 140 varieties (2026). Best towards evening, when the lanterns are lit.",
      "favPhoto": [
        3,
        0
      ],
      "whoHead": "Know before you go",
      "who": [
        "One week in mid-April only. Dates for 2027 are announced in March (please check)",
        "The Mint needs advance online booking, first come first served; you enter in your time slot",
        "The walk is one way, with no eating or drinking, parasols, selfie sticks or tripods",
        "The castle’s Somei-yoshino bloom about a week earlier, so in some years the two don’t overlap",
        "Gion-Shijo in Kyoto to Temmabashi: 46 min by Keihan limited express (¥490)"
      ],
      "dayHead": "Half a day, roughly like this",
      "from": "From",
      "day": [
        {
          "time": "15:16",
          "area": "Temmabashi & Osaka Castle",
          "title": "The tower through the blossoms at Nishinomaru",
          "text": "Walk from Temmabashi Station to the castle and look up at the tower between the cherry trees from the lawn garden (last entry 16:30).",
          "photo": [
            2,
            1
          ]
        },
        {
          "time": "17:15",
          "area": "Japan Mint",
          "title": "The double-cherry walk",
          "text": "One way from south gate to north gate, about 560 m, reading the name boards under the lit lanterns.",
          "photo": [
            3,
            1
          ]
        },
        {
          "time": "18:15",
          "area": "Okawa river",
          "title": "Home along the riverside cherries",
          "text": "Cross Sakuranomiya bridge into Kema Sakuranomiya Park and walk the river at sunset to Temmabashi or Sakuranomiya station.",
          "note": "Back in Kyoto before 21:00",
          "photo": [
            4,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "The Keihan line between Gion-Shijo and Temmabashi is ¥490 each way; everything in Osaka is on foot. Nishinomaru Garden is ¥350 in blossom season; Kema Sakuranomiya Park is free.",
      "deals": [
        {
          "name": "Keihan (Gion-Shijo ⇄ Temmabashi)",
          "price": "¥490 one way",
          "text": "46 min by limited express, direct. Gion-Shijo 14:30 → Temmabashi 15:16; back Temmabashi 20:04 → Gion-Shijo 20:50.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Japan Mint cherry-blossom walk",
          "price": "Advance booking",
          "best": "Book first",
          "text": "In 2026 you chose an entry time slot online, first come first served, and booking opened on 18 March. Dates and method for 2027 will be announced on the Mint’s official site in March (please check).",
          "url": "https://www.mint.go.jp/enjoy/toorinuke/"
        },
        {
          "name": "Osaka Castle Nishinomaru Garden",
          "price": "¥350 (blossom season)",
          "text": "9:00–17:00 (last entry 16:30), closed Mondays. In years with night illuminations it also opens in the evening (check the dates).",
          "url": "https://osakacastlepark.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 21, 2026 (the Mint’s official page for the 2026 event, the facility list on the Osaka Amazing Pass site; trains on a route planner).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "A mid-April map",
          "text": "It is for the week or so when the Mint’s cherry-blossom walk is open. First check the dates on the official site and book your entry."
        },
        {
          "title": "In number order",
          "text": "Follow 1 to 4: from Temmabashi Station to the castle, the Mint’s south gate, out of the north gate and along the riverside cherries."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees and suggested times."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi (photos from April 2025 and April 2026)."
    }
  }
};
