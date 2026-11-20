/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都から新快速で姫路へ、姫路城・好古園・明石の魚の棚（たこ磯）・須磨浦公園・舞子公園を回り、海沿いを京都の方へ戻る日帰りルート。
   Photos are [spot number, photo index] from data/routes/himeji.json.
   時刻・料金は2026年11月20日に確認（各施設の公式サイト、電車は乗換案内）。 */
window.HIMEJI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から日帰り 姫路・明石・須磨 Himeji MAP',
    titleMain: '姫路・明石・須磨',
    titleSub: 'Himeji, Akashi & Suma',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '姫路から明石、須磨へと東へ進み、最後は夕日を見るために舞子まで少し戻ります。4番の書写山は半日かかる寄り道で、須磨・舞子とは同じ日に回れません。行かない場所は「選んで回る」で外せます。点線は順番を示す線で、実際の道ではありません。',
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
    checkedDate: '2026年11月20日',
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
    pickNote: '行きたい場所の「行きたい」を押してください。姫路駅は姫路城・好古園・書写山のどれかを選ぶと入ります。時間は、書写山を除く5か所を回る場合の目安です。',
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
      "kicker": "Toshiが歩いて作った日帰りルート",
      "h1": "白鷺城から、明石焼と海の見えるロープウェーへ。",
      "lead": "京都から新快速で姫路へ。世界遺産の姫路城と好古園を見たら、明石の魚の棚で明石焼のお昼。須磨浦公園のロープウェーとカーレーターで山の上へ上り、最後は舞子で明石海峡大橋に沈む夕日を。海沿いを京都の方へ戻りながら回ります。",
      "favLabel": "いちばんの見どころ",
      "favName": "姫路城",
      "favText": "真っ白な大天守。中の木の階段で最上階まで上れます。",
      "favPhoto": [
        2,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "お城も海も、1日で欲ばりたい人に",
        "京都から姫路まで新快速で1時間36分（2,210円）",
        "姫路城の中は急な木の階段。靴を脱いで上がります",
        "須磨浦山上遊園は火曜休み・16:30最終入場。冬（12/2〜2/5）は土日祝だけ",
        "姫路でもう1か所なら、ロープウェイで上る書写山 圓教寺（半日。須磨・舞子の代わりに）",
        "魚の棚は木曜に休む店が多い"
      ],
      "dayHead": "1日の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "9:50",
          "area": "姫路",
          "title": "白鷺城と好古園",
          "text": "大手前通りをまっすぐ歩いて姫路城へ。大天守の最上階まで上り、好古園の池のほとりへ。",
          "photo": [
            2,
            1
          ]
        },
        {
          "time": "13:25",
          "area": "明石",
          "title": "魚の棚で明石焼のお昼",
          "text": "新快速で明石へ。魚の棚商店街のたこ磯で、だしにつけて食べる玉子焼を。",
          "photo": [
            5,
            2
          ]
        },
        {
          "time": "15:00",
          "area": "須磨浦公園",
          "title": "ロープウェーとカーレーター",
          "text": "山陽電車で須磨浦公園へ。ロープウェーとカーレーターで山の上の回転展望閣へ。",
          "photo": [
            6,
            1
          ]
        },
        {
          "time": "16:45",
          "area": "舞子 → 京都",
          "title": "明石海峡大橋に沈む夕日",
          "text": "舞子公園で橋と淡路島の夕景を見てから、JR舞子駅から京都へ。",
          "note": "京都着は18:59",
          "photo": [
            7,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費のめやす",
      "dealsLead": "電車は京都→姫路が2,210円、姫路→明石660円、山陽電車が明石→須磨浦公園390円・須磨浦公園→舞子公園250円、舞子→京都1,640円。合わせて約5,150円です。入城料などは別です。",
      "deals": [
        {
          "name": "JR（京都→姫路）",
          "price": "片道2,210円",
          "text": "新快速で乗り換えなし、1時間36分。京都8:14発→姫路9:50着。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "姫路城・好古園 共通券",
          "price": "2,600円",
          "text": "姫路城だけなら2,500円（18歳以上・姫路市外）、好古園だけなら400円。18歳未満は無料。",
          "url": "https://www.himejicastle.jp/"
        },
        {
          "name": "須磨浦山上遊園 回遊券（Bコース）",
          "price": "1,500円",
          "text": "ロープウェー・カーレーターの往復と回転展望閣。リフトもつくAコースは2,100円。",
          "url": "https://www.sumaura-yuen.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月20日に確認しました（各施設の公式サイト、電車は乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "最初は「選んで回る」",
          "text": "行きたい場所だけを選ぶと、駅とルートが自動で決まります。書写山は半日かかるので、須磨・舞子と一緒には選べません。"
        },
        {
          "title": "西から東へ、最後に夕日",
          "text": "姫路から明石、須磨へと東へ進み、最後は夕日を見るために舞子まで少し戻ります。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・電車の時刻・おすすめの時間が見られます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto: Himeji, Akashi & Suma MAP',
    titleMain: 'Himeji, Akashi & Suma',
    titleSub: '姫路・明石・須磨',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'From Himeji east to Akashi and Suma, then a short way back west to Maiko for the sunset. No. 4, Mt. Shosha, is a half-day side trip that doesn’t fit with Suma and Maiko. Use “Choose stops” to drop places you’ll skip. The dotted line shows the order, not the actual path.',
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
    checkedDate: 'Nov 20, 2026',
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
    pickNote: 'Tap “Want to go” on the places you like. Himeji Station joins your route if you pick the castle, Kokoen or Mt. Shosha. Times are for the five stops without Mt. Shosha.',
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
      "kicker": "A day trip, hand-walked by Toshi",
      "h1": "From the White Heron Castle to akashiyaki and a ropeway over the sea.",
      "lead": "Special Rapid from Kyoto to Himeji. See World Heritage Himeji Castle and Kokoen garden, lunch on akashiyaki at Akashi’s Uonotana market, ride the ropeway and the Car-rator up Sumaura Park, and end with the sunset behind the Akashi Kaikyo Bridge at Maiko, working your way back towards Kyoto along the coast.",
      "favLabel": "Highlight",
      "favName": "Himeji Castle",
      "favText": "The brilliant white keep; climb its wooden stairs to the top floor.",
      "favPhoto": [
        2,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "For castles and the sea in one day",
        "Kyoto to Himeji is 1 h 36 min by Special Rapid (¥2,210)",
        "Inside the castle: steep wooden stairs, shoes off",
        "Sumaura Sanjo Yuen: closed Tuesdays, last entry 16:30; weekends only 2 Dec – 5 Feb",
        "One more in Himeji: Mt. Shosha Engyo-ji by ropeway (half a day, instead of Suma and Maiko)",
        "Many Uonotana shops close on Thursdays"
      ],
      "dayHead": "One day, roughly like this",
      "from": "From",
      "day": [
        {
          "time": "9:50",
          "area": "Himeji",
          "title": "The White Heron Castle and Kokoen",
          "text": "Walk straight up Otemae-dori to the castle, climb to the top of the keep, then stroll the Kokoen pond garden.",
          "photo": [
            2,
            1
          ]
        },
        {
          "time": "13:25",
          "area": "Akashi",
          "title": "Akashiyaki lunch at Uonotana",
          "text": "Special Rapid to Akashi; tamagoyaki dipped in dashi at Takoiso in the Uonotana arcade.",
          "photo": [
            5,
            2
          ]
        },
        {
          "time": "15:00",
          "area": "Sumaura Park",
          "title": "Ropeway and Car-rator",
          "text": "Sanyo Railway to Sumaura-koen, then up by ropeway and Car-rator to the revolving observatory.",
          "photo": [
            6,
            1
          ]
        },
        {
          "time": "16:45",
          "area": "Maiko → Kyoto",
          "title": "Sunset behind the bridge",
          "text": "Watch the sun set behind the bridge and Awaji Island at Maiko Park, then head home from JR Maiko.",
          "note": "Arrive Kyoto 18:59",
          "photo": [
            7,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares",
      "dealsLead": "Trains: Kyoto → Himeji ¥2,210, Himeji → Akashi ¥660, Sanyo Railway Akashi → Sumaura-koen ¥390 and Sumaura-koen → Maiko-koen ¥250, Maiko → Kyoto ¥1,640: about ¥5,150 in all. Admission is extra.",
      "deals": [
        {
          "name": "JR (Kyoto → Himeji)",
          "price": "¥2,210 one way",
          "text": "Special Rapid, direct, 1 h 36 min. Kyoto 8:14 → Himeji 9:50.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Himeji Castle + Kokoen combined ticket",
          "price": "¥2,600",
          "text": "Castle only ¥2,500 (18+, non-residents), Kokoen only ¥400. Free under 18.",
          "url": "https://www.himejicastle.jp/"
        },
        {
          "name": "Sumaura Sanjo Yuen round ticket (B)",
          "price": "¥1,500",
          "text": "Ropeway and Car-rator return plus the revolving observatory. Course A with the chairlift is ¥2,100.",
          "url": "https://www.sumaura-yuen.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 20, 2026 (official sites of the venues; trains on a route planner).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Starts in “Choose stops”",
          "text": "Pick only the places you want; stations and the route follow automatically. Mt. Shosha takes half a day, so it can’t be combined with Suma and Maiko."
        },
        {
          "title": "West to east, then the sunset",
          "text": "From Himeji east to Akashi and Suma, then a short way back west to Maiko for the sunset."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, train times and suggested times."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi."
    }
  }
};
