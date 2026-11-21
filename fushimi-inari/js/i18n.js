/* Page texts in Japanese and English.
   Toshi 個人のマップ。伏見稲荷から東福寺・泉涌寺・三十三間堂へ北に歩き、夕方は高瀬川ぞいの銭湯（サウナの梅湯）と Kyoto Beer Lab、夜は木屋町を歩いて三条へ。
   コースは2つ：早朝に出発（三条5:24発の京阪で、6:00より前に入口へ）と、9〜10時に出発。
   intro は「9〜10時に出発」の内容で、introFor[コース] が app.js で上書きされる（scripts/sync_fushimi_inari.py）。
   Photos are [spot id, photo index]。
   料金・時間は2026年11月20日〜22日に確認（確認できなかったものはデータに「要確認」と書いてある）。 */
window.FUSHIMI_INARI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: "京都 伏見稲荷から七条へ｜千本鳥居・東福寺・銭湯とビール Fushimi Inari MAP",
    titleMain: "伏見稲荷から七条へ",
    titleSub: "Fushimi Inari to Shichijo",
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: "番号の順に、南から北へ歩きます。伏見稲荷は朝6:30にはもう人が多いので、人の少ない千本鳥居を歩きたい日は「早朝に出発」へ。点線は順番を示す線で、実際の道ではありません。",
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
    credit: "写真・文章：Toshi（三十三間堂の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトで確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: "最初は全部の場所が選ばれています。めやすの時間は、全部回るときの時間割です。行かない場所は「行く」を押して外してください。",
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: "まだ選んでいません。下の一覧から、行きたい場所を選んでください。",
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
    courseEarly: "早朝に出発\n（5時台）",
    courseLate: "9〜10時に出発",
    swMode: "回り方",
    // 9〜10時に出発（late）の内容。早朝に出発（early）は introFor.early で上書きする
    intro: {
      "kicker": "Toshiが歩いて作った1日ルート",
      "favLabel": "いちばんの見どころ",
      "favName": "伏見稲荷大社",
      "favText": "入口に6:00に着けば、千本鳥居はまだ人が少ないです。",
      "favPhoto": [
        "inari",
        0
      ],
      "whoHead": "こんな人におすすめ",
      "from": "",
      "timeSuffix": "〜",
      "dealsHead": "お金のめやす",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧のいちばん上のボタンで「早朝に出発」か「9〜10時に出発」を選びます。時間割と回る順番が切り替わります。"
        },
        {
          "title": "行かない場所を外す",
          "text": "最初は、1日で無理なく回れる場所が選ばれています。行かない場所は「行く」を押して外し、足したい場所は「行きたい」を押します。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・めやすの時間が見られます。入口で困ること（休み・撮影禁止など）は、いちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。公式サイトへのリンクもあります。"
        }
      ],
      "h1": "千本鳥居から東福寺、泉涌寺、三十三間堂へ。最後は高瀬川の銭湯とビール。",
      "lead": "伏見稲荷だけで終わらせず、北へ歩いて東福寺、泉涌寺、三十三間堂へ。夕方は高瀬川ぞいの銭湯「サウナの梅湯」で汗を流し、すぐ近くの Kyoto Beer Lab でビール。夜は木屋町を歩いて三条へ戻ります。伏見稲荷は朝6:30にはもう人が多いので、人の少ない鳥居の道を歩きたい人は、一覧の上のボタンで「早朝に出発」を選んでください。",
      "who": [
        "三条のあたりを9時すぎに出て、夜まで歩く1日",
        "伏見稲荷はこの時間、人でいっぱいです。人の少ない鳥居を歩きたい人は「早朝に出発」へ",
        "稲荷山は四ツ辻まで上る時間割。山頂まで行くなら、あと30分",
        "三十三間堂は冬（11月16日〜3月）は受付が15:30まで",
        "梅湯は木曜休み、現金かPayPay。タオルは借りられます",
        "雲龍院は水曜休み（11月を除く）"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "day": [
        {
          "time": "9:15",
          "area": "伏見稲荷",
          "title": "千本鳥居を四ツ辻まで",
          "text": "三条から京阪で約10分。9:35から11:15まで、鳥居の道を四ツ辻まで上って戻ります。",
          "note": "この時間は人でいっぱいです",
          "photo": [
            "inari",
            0
          ]
        },
        {
          "time": "11:15",
          "area": "伏見稲荷の参道",
          "title": "お昼ごはん",
          "text": "参道か駅のまわりで。境内では食べ歩きができません。",
          "photo": [
            "station",
            0
          ]
        },
        {
          "time": "12:20",
          "area": "東福寺 → 泉涌寺 → 三十三間堂",
          "title": "通天橋、御寺、千体の観音さま",
          "text": "東福寺の通天橋から谷を見下ろし、泉涌寺と雲龍院へ。坂を下りて、14:50に三十三間堂。",
          "note": "三十三間堂は冬、受付15:30まで",
          "photo": [
            "tofukuji",
            0
          ]
        },
        {
          "time": "15:50",
          "area": "高瀬川ぞい",
          "title": "銭湯とクラフトビール",
          "text": "サウナの梅湯で汗を流して（17:00まで）、歩いて5分の Kyoto Beer Lab へ。",
          "note": "梅湯は木曜休み",
          "photo": [
            "umeyu",
            0
          ]
        },
        {
          "time": "18:30",
          "area": "木屋町 → 三条",
          "title": "高瀬川に沿って歩いて帰る",
          "text": "高瀬川ぞいを北へ歩いて、三条に19時すぎ。途中の木屋町や先斗町で晩ごはんにすれば、21時ごろまで。",
          "photo": [
            "beerlab",
            2
          ]
        }
      ],
      "dealsLead": "電車は行きの240円だけ。あとは歩いて三条まで戻ります（拝観料・飲食は別）。",
      "deals": [
        {
          "name": "京阪電車（三条→伏見稲荷）",
          "price": "240円",
          "text": "乗り換えなしで約10分。準急か普通に乗ります。",
          "url": "https://www.keihan.co.jp/traffic/"
        },
        {
          "name": "サウナの梅湯",
          "price": "550円",
          "text": "大人の入浴料。貸しタオルは100円から。支払いは現金かPayPayです。",
          "url": "https://yutonamisha.com/sento/umeyu/"
        }
      ],
      "dealsNote": "大人の料金です。京阪は乗換案内、梅湯は公式サイトで、2026年11月22日に確認しました。"
    },
    introFor: {
      late: {
        "h1": "千本鳥居から東福寺、泉涌寺、三十三間堂へ。最後は高瀬川の銭湯とビール。",
        "lead": "伏見稲荷だけで終わらせず、北へ歩いて東福寺、泉涌寺、三十三間堂へ。夕方は高瀬川ぞいの銭湯「サウナの梅湯」で汗を流し、すぐ近くの Kyoto Beer Lab でビール。夜は木屋町を歩いて三条へ戻ります。伏見稲荷は朝6:30にはもう人が多いので、人の少ない鳥居の道を歩きたい人は、一覧の上のボタンで「早朝に出発」を選んでください。",
        "who": [
          "三条のあたりを9時すぎに出て、夜まで歩く1日",
          "伏見稲荷はこの時間、人でいっぱいです。人の少ない鳥居を歩きたい人は「早朝に出発」へ",
          "稲荷山は四ツ辻まで上る時間割。山頂まで行くなら、あと30分",
          "三十三間堂は冬（11月16日〜3月）は受付が15:30まで",
          "梅湯は木曜休み、現金かPayPay。タオルは借りられます",
          "雲龍院は水曜休み（11月を除く）"
        ],
        "dayHead": "1日の流れ（9〜10時に出発）",
        "day": [
          {
            "time": "9:15",
            "area": "伏見稲荷",
            "title": "千本鳥居を四ツ辻まで",
            "text": "三条から京阪で約10分。9:35から11:15まで、鳥居の道を四ツ辻まで上って戻ります。",
            "note": "この時間は人でいっぱいです",
            "photo": [
              "inari",
              0
            ]
          },
          {
            "time": "11:15",
            "area": "伏見稲荷の参道",
            "title": "お昼ごはん",
            "text": "参道か駅のまわりで。境内では食べ歩きができません。",
            "photo": [
              "station",
              0
            ]
          },
          {
            "time": "12:20",
            "area": "東福寺 → 泉涌寺 → 三十三間堂",
            "title": "通天橋、御寺、千体の観音さま",
            "text": "東福寺の通天橋から谷を見下ろし、泉涌寺と雲龍院へ。坂を下りて、14:50に三十三間堂。",
            "note": "三十三間堂は冬、受付15:30まで",
            "photo": [
              "tofukuji",
              0
            ]
          },
          {
            "time": "15:50",
            "area": "高瀬川ぞい",
            "title": "銭湯とクラフトビール",
            "text": "サウナの梅湯で汗を流して（17:00まで）、歩いて5分の Kyoto Beer Lab へ。",
            "note": "梅湯は木曜休み",
            "photo": [
              "umeyu",
              0
            ]
          },
          {
            "time": "18:30",
            "area": "木屋町 → 三条",
            "title": "高瀬川に沿って歩いて帰る",
            "text": "高瀬川ぞいを北へ歩いて、三条に19時すぎ。途中の木屋町や先斗町で晩ごはんにすれば、21時ごろまで。",
            "photo": [
              "beerlab",
              2
            ]
          }
        ],
        "dealsLead": "電車は行きの240円だけ。あとは歩いて三条まで戻ります（拝観料・飲食は別）。",
        "deals": [
          {
            "name": "京阪電車（三条→伏見稲荷）",
            "price": "240円",
            "text": "乗り換えなしで約10分。準急か普通に乗ります。",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "サウナの梅湯",
            "price": "550円",
            "text": "大人の入浴料。貸しタオルは100円から。支払いは現金かPayPayです。",
            "url": "https://yutonamisha.com/sento/umeyu/"
          }
        ],
        "dealsNote": "大人の料金です。京阪は乗換案内、梅湯は公式サイトで、2026年11月22日に確認しました。"
      },
      early: {
        "h1": "朝6時の千本鳥居。東福寺、泉涌寺、三十三間堂を歩いて、午後は銭湯とビール。",
        "lead": "伏見稲荷は、入口に6:00に着けばまだ人が少なく、6:30にはもう増えています。三条5:24発の京阪に乗って、人の少ない鳥居の道を四ツ辻まで。いったん三条へ戻って朝ごはんを食べ、9時すぎに出直して東福寺、泉涌寺、三十三間堂へ。午後は高瀬川ぞいの銭湯「サウナの梅湯」と Kyoto Beer Lab で、早起きの1日を終えます。",
        "who": [
          "早起きして、人の少ない千本鳥居を歩きたい人に",
          "三条5:24発の京阪で、5:40に入口へ。5:46発だと入口に6:00です",
          "11月〜2月の朝6時はまだ暗いです",
          "朝ごはんは三条へ戻って、7:00から開いているイノダコーヒ本店で",
          "梅湯は木曜休み、現金かPayPay。タオルは借りられます",
          "雲龍院は水曜休み（11月を除く）"
        ],
        "dayHead": "1日の流れ（早朝に出発）",
        "day": [
          {
            "time": "5:24",
            "area": "伏見稲荷",
            "title": "6時前に入口へ。人の少ない千本鳥居",
            "text": "三条5:24発の京阪で5:34に伏見稲荷駅。5:40から、鳥居の道を四ツ辻まで上って戻ります（7:30まで）。",
            "note": "6:30にはもう人が増えます",
            "photo": [
              "inari",
              0
            ]
          },
          {
            "time": "7:40",
            "area": "三条へ戻る",
            "title": "朝ごはんとひと休み",
            "text": "京阪で三条へ戻って（約10分）、7:00から開いているイノダコーヒ本店へ。9:20ごろの電車で出直します。",
            "note": "戻らない日は、朝ごはんを持っていく",
            "photo": [
              "station",
              0
            ]
          },
          {
            "time": "9:40",
            "area": "東福寺 → 泉涌寺 → 三十三間堂",
            "title": "通天橋、御寺、千体の観音さま",
            "text": "東福寺の通天橋から谷を見下ろし、泉涌寺と雲龍院へ。坂を下りて、12:20に三十三間堂。そのあと七条通でお昼（13:00〜）。",
            "photo": [
              "tofukuji",
              0
            ]
          },
          {
            "time": "14:05",
            "area": "高瀬川ぞい",
            "title": "銭湯とクラフトビール",
            "text": "サウナの梅湯でゆっくりして（15:20まで）、歩いて5分の Kyoto Beer Lab へ。",
            "note": "梅湯は木曜休み",
            "photo": [
              "umeyu",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "木屋町 → 三条",
            "title": "高瀬川に沿って歩いて帰る",
            "text": "高瀬川ぞいを北へ歩いて、三条に17時半すぎ。まだ元気なら、木屋町や先斗町で晩ごはんを。",
            "photo": [
              "beerlab",
              2
            ]
          }
        ],
        "dealsLead": "電車は3回で720円（伏見稲荷の行き帰りと、東福寺まで）。最後は歩いて三条まで戻ります（拝観料・飲食は別）。",
        "deals": [
          {
            "name": "京阪電車（三条→伏見稲荷）",
            "price": "240円",
            "text": "乗り換えなしで約10分。準急か普通に乗ります。",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "京阪電車（三条→東福寺）",
            "price": "240円",
            "text": "朝ごはんのあと、約6分。伏見稲荷から三条へ戻るときも240円です。",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "サウナの梅湯",
            "price": "550円",
            "text": "大人の入浴料。貸しタオルは100円から。支払いは現金かPayPayです。",
            "url": "https://yutonamisha.com/sento/umeyu/"
          }
        ],
        "dealsNote": "大人の料金です。京阪の時刻と運賃は乗換案内（11月24日 火曜と28日 土曜の時刻）、梅湯は公式サイトで、2026年11月22日に確認しました。"
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: "Fushimi Inari to Shichijo, Kyoto | Thousand Torii, Tofuku-ji, a bathhouse and beer MAP",
    titleMain: "Fushimi Inari to Shichijo",
    titleSub: "伏見稲荷から七条へ",
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: "Walk the stops in number order, south to north. Fushimi Inari is already busy by 6:30 in the morning: to walk the Thousand Torii with fewer people, switch to “Early start”. The dotted line shows the order, not the actual path.",
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
    credit: "Photos &amp; text: Toshi (the Sanjusangen-do photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on the official website on {d}. Details can change, so please check before you go.',
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
    pickNote: "The map opens with every place chosen, and the rough times are the timetable for the full route. Tap “Going” to drop a place you’ll skip.",
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: "Nothing chosen yet. Pick the places you want from the list below.",
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
    courseEarly: "Early start\n(before 6 am)",
    courseLate: "Leave at 9–10",
    swMode: "Stops",
    // 9〜10時に出発（late）の内容。早朝に出発（early）は introFor.early で上書きする
    intro: {
      "kicker": "A day route, hand-walked by Toshi",
      "favLabel": "Don’t miss",
      "favName": "Fushimi Inari Taisha",
      "favText": "Be at the entrance by 6:00 and the Thousand Torii still have few people.",
      "favPhoto": [
        "inari",
        0
      ],
      "whoHead": "Who it’s for",
      "from": "From",
      "timeSuffix": "",
      "dealsHead": "What it costs",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi.",
      "how": [
        {
          "title": "Choose your start time",
          "text": "Use the buttons at the top of the list to pick “Early start” or “Leave at 9–10”. The timetable and the order of the stops change with it."
        },
        {
          "title": "Drop what you don’t want",
          "text": "The map opens with a set of places that fits comfortably into one day. Tap “Going” to drop a place, or “Want to go” to add one."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, for photos, notes, fees and rough times. Anything that could stop you at the door (closing days, no-photo rules) is shown first."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions. There are links to official websites too."
        }
      ],
      "h1": "From the Thousand Torii to Tofuku-ji, Sennyu-ji and Sanjusangen-do, ending with a bathhouse and a beer by the Takase River.",
      "lead": "Don’t stop at Fushimi Inari: walk north to Tofuku-ji, Sennyu-ji and Sanjusangen-do. In the late afternoon, wash off the day at the public bath Sauna no Umeyu on the Takase River and have a beer at Kyoto Beer Lab nearby, then walk back to Sanjo through Kiyamachi. Fushimi Inari is already busy by 6:30 in the morning: to walk the torii path with fewer people, choose “Early start” with the buttons above the list.",
      "who": [
        "A day that leaves the Sanjo area after 9:00 and runs into the evening",
        "Fushimi Inari is full of people at this hour. For a quieter walk, use “Early start”",
        "The timetable climbs Mt. Inari as far as Yotsutsuji; add 30 minutes for the summit",
        "Sanjusangen-do: last entry 15:30 in winter (16 Nov – March)",
        "Umeyu: closed Thursdays, cash or PayPay; towels can be rented",
        "Unryu-in: closed Wednesdays (except November)"
      ],
      "dayHead": "The day (leaving at 9–10)",
      "day": [
        {
          "time": "9:15",
          "area": "Fushimi Inari",
          "title": "The Thousand Torii, up to Yotsutsuji",
          "text": "About 10 minutes from Sanjo on the Keihan line. From 9:35 to 11:15, climb the torii path to Yotsutsuji and back.",
          "note": "Full of people at this hour",
          "photo": [
            "inari",
            0
          ]
        },
        {
          "time": "11:15",
          "area": "The approach to Fushimi Inari",
          "title": "Lunch",
          "text": "On the approach or around the stations. You can’t eat while walking inside the shrine.",
          "photo": [
            "station",
            0
          ]
        },
        {
          "time": "12:20",
          "area": "Tofuku-ji → Sennyu-ji → Sanjusangen-do",
          "title": "A bridge over maples, the imperial temple, a thousand Kannon",
          "text": "Look down from Tofuku-ji’s Tsutenkyo bridge, visit Sennyu-ji and Unryu-in, then walk downhill to reach Sanjusangen-do at 14:50.",
          "note": "Sanjusangen-do: last entry 15:30 in winter",
          "photo": [
            "tofukuji",
            0
          ]
        },
        {
          "time": "15:50",
          "area": "Along the Takase River",
          "title": "Bathhouse and craft beer",
          "text": "Soak at Sauna no Umeyu (until 17:00), then walk 5 minutes to Kyoto Beer Lab.",
          "note": "Umeyu is closed on Thursdays",
          "photo": [
            "umeyu",
            0
          ]
        },
        {
          "time": "18:30",
          "area": "Kiyamachi → Sanjo",
          "title": "Walk home along the Takase River",
          "text": "Follow the river north to reach Sanjo soon after 19:00. Stop for dinner in Kiyamachi or Pontocho and the evening runs to about 21:00.",
          "photo": [
            "beerlab",
            2
          ]
        }
      ],
      "dealsLead": "The only train fare is ¥240 on the way out; you walk back to Sanjo at the end (temple fees, food and drink not included).",
      "deals": [
        {
          "name": "Keihan line (Sanjo → Fushimi-Inari)",
          "price": "¥240",
          "text": "About 10 minutes, no changes. Take a sub-express or a local.",
          "url": "https://www.keihan.co.jp/traffic/"
        },
        {
          "name": "Sauna no Umeyu",
          "price": "¥550",
          "text": "Adult bath fee. Towel rental from ¥100. Cash or PayPay.",
          "url": "https://yutonamisha.com/sento/umeyu/"
        }
      ],
      "dealsNote": "Adult prices, checked on Nov 22, 2026: Keihan on a route planner, Umeyu on its operator’s website."
    },
    introFor: {
      late: {
        "h1": "From the Thousand Torii to Tofuku-ji, Sennyu-ji and Sanjusangen-do, ending with a bathhouse and a beer by the Takase River.",
        "lead": "Don’t stop at Fushimi Inari: walk north to Tofuku-ji, Sennyu-ji and Sanjusangen-do. In the late afternoon, wash off the day at the public bath Sauna no Umeyu on the Takase River and have a beer at Kyoto Beer Lab nearby, then walk back to Sanjo through Kiyamachi. Fushimi Inari is already busy by 6:30 in the morning: to walk the torii path with fewer people, choose “Early start” with the buttons above the list.",
        "who": [
          "A day that leaves the Sanjo area after 9:00 and runs into the evening",
          "Fushimi Inari is full of people at this hour. For a quieter walk, use “Early start”",
          "The timetable climbs Mt. Inari as far as Yotsutsuji; add 30 minutes for the summit",
          "Sanjusangen-do: last entry 15:30 in winter (16 Nov – March)",
          "Umeyu: closed Thursdays, cash or PayPay; towels can be rented",
          "Unryu-in: closed Wednesdays (except November)"
        ],
        "dayHead": "The day (leaving at 9–10)",
        "day": [
          {
            "time": "9:15",
            "area": "Fushimi Inari",
            "title": "The Thousand Torii, up to Yotsutsuji",
            "text": "About 10 minutes from Sanjo on the Keihan line. From 9:35 to 11:15, climb the torii path to Yotsutsuji and back.",
            "note": "Full of people at this hour",
            "photo": [
              "inari",
              0
            ]
          },
          {
            "time": "11:15",
            "area": "The approach to Fushimi Inari",
            "title": "Lunch",
            "text": "On the approach or around the stations. You can’t eat while walking inside the shrine.",
            "photo": [
              "station",
              0
            ]
          },
          {
            "time": "12:20",
            "area": "Tofuku-ji → Sennyu-ji → Sanjusangen-do",
            "title": "A bridge over maples, the imperial temple, a thousand Kannon",
            "text": "Look down from Tofuku-ji’s Tsutenkyo bridge, visit Sennyu-ji and Unryu-in, then walk downhill to reach Sanjusangen-do at 14:50.",
            "note": "Sanjusangen-do: last entry 15:30 in winter",
            "photo": [
              "tofukuji",
              0
            ]
          },
          {
            "time": "15:50",
            "area": "Along the Takase River",
            "title": "Bathhouse and craft beer",
            "text": "Soak at Sauna no Umeyu (until 17:00), then walk 5 minutes to Kyoto Beer Lab.",
            "note": "Umeyu is closed on Thursdays",
            "photo": [
              "umeyu",
              0
            ]
          },
          {
            "time": "18:30",
            "area": "Kiyamachi → Sanjo",
            "title": "Walk home along the Takase River",
            "text": "Follow the river north to reach Sanjo soon after 19:00. Stop for dinner in Kiyamachi or Pontocho and the evening runs to about 21:00.",
            "photo": [
              "beerlab",
              2
            ]
          }
        ],
        "dealsLead": "The only train fare is ¥240 on the way out; you walk back to Sanjo at the end (temple fees, food and drink not included).",
        "deals": [
          {
            "name": "Keihan line (Sanjo → Fushimi-Inari)",
            "price": "¥240",
            "text": "About 10 minutes, no changes. Take a sub-express or a local.",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "Sauna no Umeyu",
            "price": "¥550",
            "text": "Adult bath fee. Towel rental from ¥100. Cash or PayPay.",
            "url": "https://yutonamisha.com/sento/umeyu/"
          }
        ],
        "dealsNote": "Adult prices, checked on Nov 22, 2026: Keihan on a route planner, Umeyu on its operator’s website."
      },
      early: {
        "h1": "The Thousand Torii at 6 am, then Tofuku-ji, Sennyu-ji and Sanjusangen-do, with a bathhouse and a beer in the afternoon.",
        "lead": "At Fushimi Inari, if you’re at the entrance by 6:00 there are still few people; by 6:30 the crowds are building. Take the 5:24 Keihan train from Sanjo and walk the torii path to Yotsutsuji while it’s calm. Go back to Sanjo for breakfast, set out again after 9:00 for Tofuku-ji, Sennyu-ji and Sanjusangen-do, and end your early day at the public bath Sauna no Umeyu and Kyoto Beer Lab on the Takase River.",
        "who": [
          "For early risers who want the Thousand Torii with fewer people",
          "The 5:24 Keihan train from Sanjo gets you to the entrance at 5:40; the 5:46 gets you there at 6:00",
          "At 6:00 it is still dark from November to February",
          "Breakfast back in Sanjo, at Inoda Coffee’s main shop (open from 7:00)",
          "Umeyu: closed Thursdays, cash or PayPay; towels can be rented",
          "Unryu-in: closed Wednesdays (except November)"
        ],
        "dayHead": "The day (early start)",
        "day": [
          {
            "time": "5:24",
            "area": "Fushimi Inari",
            "title": "At the entrance before six: the Thousand Torii with few people",
            "text": "The 5:24 Keihan train from Sanjo reaches Fushimi-Inari at 5:34. From 5:40, climb the torii path to Yotsutsuji and back (until 7:30).",
            "note": "Crowds are building by 6:30",
            "photo": [
              "inari",
              0
            ]
          },
          {
            "time": "7:40",
            "area": "Back to Sanjo",
            "title": "Breakfast and a rest",
            "text": "Ride the Keihan back to Sanjo (about 10 minutes) for Inoda Coffee’s main shop, open from 7:00. Set out again on a train at about 9:20.",
            "note": "Not going back? Bring breakfast",
            "photo": [
              "station",
              0
            ]
          },
          {
            "time": "9:40",
            "area": "Tofuku-ji → Sennyu-ji → Sanjusangen-do",
            "title": "A bridge over maples, the imperial temple, a thousand Kannon",
            "text": "Look down from Tofuku-ji’s Tsutenkyo bridge, visit Sennyu-ji and Unryu-in, then walk downhill to reach Sanjusangen-do at 12:20. Lunch afterwards on Shichijo-dori (from 13:00).",
            "photo": [
              "tofukuji",
              0
            ]
          },
          {
            "time": "14:05",
            "area": "Along the Takase River",
            "title": "Bathhouse and craft beer",
            "text": "Take your time at Sauna no Umeyu (until 15:20), then walk 5 minutes to Kyoto Beer Lab.",
            "note": "Umeyu is closed on Thursdays",
            "photo": [
              "umeyu",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Kiyamachi → Sanjo",
            "title": "Walk home along the Takase River",
            "text": "Follow the river north to reach Sanjo a little after 17:30. If you still have energy, have dinner in Kiyamachi or Pontocho.",
            "photo": [
              "beerlab",
              2
            ]
          }
        ],
        "dealsLead": "Three train rides, ¥720 in all (to Fushimi Inari and back, then to Tofuku-ji). You walk back to Sanjo at the end (temple fees, food and drink not included).",
        "deals": [
          {
            "name": "Keihan line (Sanjo → Fushimi-Inari)",
            "price": "¥240",
            "text": "About 10 minutes, no changes. Take a sub-express or a local.",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "Keihan line (Sanjo → Tofukuji)",
            "price": "¥240",
            "text": "After breakfast, about 6 minutes. The ride back from Fushimi-Inari to Sanjo is ¥240 too.",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "Sauna no Umeyu",
            "price": "¥550",
            "text": "Adult bath fee. Towel rental from ¥100. Cash or PayPay.",
            "url": "https://yutonamisha.com/sento/umeyu/"
          }
        ],
        "dealsNote": "Adult prices, checked on Nov 22, 2026: Keihan times and fares on a route planner (for Tuesday Nov 24 and Saturday Nov 28), Umeyu on its operator’s website."
      }
    }
  }
};
