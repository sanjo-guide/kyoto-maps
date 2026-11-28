/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都から京阪で大津へ。琵琶湖疏水と三井寺（園城寺）の桜のライトアップを歩く、春の夜のルート。
   Photos are [spot number, photo index] from data/routes/miidera.json.
   三条17:16発 → 18:00の受付 → 大門・金堂・三重塔・観音堂 → 帰りに疏水 → 20:39発で三条へ。時刻を直すときは scripts/build_miidera_data.py も。
   春の日程・料金は2026年春の実績、電車は2026年11月のダイヤ。2026年11月23日に確認（出典は data の sources）。
   off… の文言は、春以外に開いたときに出る（scripts/sync_miidera.py）。 */
window.MIIDERA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から春の夜に 三井寺の夜桜 Miidera MAP',
    titleMain: '三井寺の夜桜',
    titleSub: 'Miidera by night',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '三条京阪17:16発で18:00の受付へ。疏水の桜は、暗くなってから帰り道に見ます。昼から来る人の過ごし方は1番に。点線は順番を示す線で、実際の道ではありません。',
    offKicker: '春の夜だけのマップ（いまは季節外）',
    offLead: 'いまは春のライトアップをしていません。日程・料金は2026年春の実績、電車は2026年11月の時刻で、来春は要確認です。',
    offNote: '春の夜だけのマップです。いまは春のライトアップをしていません（来春の日程は未発表・要確認）。',
    offHow: '春のライトアップは、いまはやっていません',
    offHowText: '2026年の回は4月12日で終わりました。来春の日程・料金は未発表なので要確認。春に行くときは、',
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
    day: '昼の拝観',
    meal: '食事',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月23日',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。',
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
      "kicker": "Toshiが歩いて作った春の夜のルート",
      "h1": "照らされた国宝の金堂と、帰り道の疏水の桜。",
      "lead": "春の約3週間だけ、三井寺（園城寺）の境内と琵琶湖疏水の桜が夜に照らされます。18:00に大門をくぐって、国宝の金堂で暗くなるのを待ち、桜がピンクや紫に変わったら三重塔、高台の観音堂の夜景へ。帰りは、両岸の桜が照らされた疏水に沿って駅へ。三条から電車で30分、21時すぎには三条に戻れます（2026年は3月25日〜4月12日。来春は要確認）。",
      "favLabel": "いちばんの見どころ",
      "favName": "琵琶湖疏水の夜桜",
      "favText": "暗くなった水路の両岸に、照らされた桜が続きます。",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "行く前に",
      "who": [
        "三条京阪から「びわ湖浜大津」行きで約30分・520円。「六地蔵」行きは大津へ行きません",
        "夜の拝観は2026年春の実績で1,500円。昼の800円とは別です（来春は要確認）",
        "昼から来る人は1番へ。坂本・昼の三井寺・疏水船と、大谷のうなぎ屋で早めの晩ごはん",
        "三条に戻るのは21時すぎ。夕方に出る人は、軽く食べてから",
        "暗い石段があります。歩きやすい靴と上着で"
      ],
      "dayHead": "夜の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "17:16",
          "area": "三条 → 大津",
          "title": "地下鉄から京阪京津線へ",
          "text": "三条京阪17:16発の「びわ湖浜大津」行き。終点で乗り換えて三井寺17:46着（土日祝17:42着）。疏水に沿って大門へ。",
          "note": "520円",
          "photo": [
            5,
            2
          ]
        },
        {
          "time": "18:00",
          "area": "三井寺",
          "title": "大門で夜の受付",
          "text": "昼とは別料金。千本を超える桜の境内へ。",
          "note": "受付21:00まで",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "18:20",
          "area": "三井寺",
          "title": "金堂で暗くなるのを待つ",
          "text": "日没は18:12〜18:26ごろ。暗くなると参道の桜がピンクや紫に変わります。",
          "note": "",
          "photo": [
            2,
            4
          ]
        },
        {
          "time": "18:55",
          "area": "三井寺",
          "title": "三重塔から観音堂の夜景へ",
          "text": "塔の影を見てから南へ。19:15に観音堂、19:40には下りはじめます。",
          "note": "石段あり",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "20:00",
          "area": "帰り道",
          "title": "暗くなった疏水の桜",
          "text": "大津閘門から第一トンネルへ続く並木。無料で、点灯は21:30まで（2026年春）。",
          "note": "駅へ5分",
          "photo": [
            5,
            0
          ]
        },
        {
          "time": "20:39",
          "area": "大津 → 三条",
          "title": "三条に戻って夜の続き",
          "text": "三条京阪21:08着（土日祝21:07着）。祇園白川か円山公園の夜桜（2026年春は22:00まで。期間は短め）か、木屋町・先斗町で晩ごはん。",
          "note": "最終23:17発",
          "photo": [
            5,
            1
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "交通費・拝観料のめやす",
      "dealsLead": "三条京阪から片道520円。拝観料は2026年春の実績で、来春は要確認です。",
      "deals": [
        {
          "name": "三井寺 春のライトアップ（2026年春の実績）",
          "price": "1,500円",
          "text": "2026年は3月25日〜4月12日、18:00〜21:30（受付21:00まで）。小中高生700円。来春は要確認。",
          "url": "https://miidera1200.jp/2026lightup-spring/"
        },
        {
          "name": "三条京阪 → 三井寺",
          "price": "520円",
          "text": "びわ湖浜大津で乗り換え。京都市役所前からは540円、京都駅からはJRと京阪で440円。",
          "url": "https://transit.yahoo.co.jp/search/result?from=%E4%B8%89%E6%9D%A1%E4%BA%AC%E9%98%AA&to=%E4%B8%89%E4%BA%95%E5%AF%BA&y=2026&m=12&d=02&hh=17&m1=1&m2=5&type=1&ticket=normal&expkind=1&ws=3&s=0"
        },
        {
          "name": "琵琶湖疏水の夜桜（2026年春の実績）",
          "price": "無料",
          "text": "2026年は3月25日〜4月12日、18:00〜21:30点灯。来春は要確認。",
          "url": "https://otsu.or.jp/tripideas/otsu-sakura/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月23日に確認しました（春の分は2026年の実績、電車は2026年11月のダイヤ）。",
      "dealsMore": "詳しく見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "三条京阪17:16発で",
          "text": "三条京阪17:16発の「びわ湖浜大津」行きに乗れば、18:00の夜の受付に間に合います。1から5の順に、お寺が先、疏水は暗くなった帰り道に。"
        },
        {
          "title": "受付は21:00、点灯は21:30まで",
          "text": "2026年春の実績です（来春は要確認）。全部見るなら19:30までに大門へ。帰りは20:39発が基本で、最終は23:17発。"
        },
        {
          "title": "昼から来る人は1番へ",
          "text": "9時台に出て坂本と昼の三井寺を回る時間割、疏水船、早めの晩ごはんが書いてあります。"
        },
        {
          "title": "番号をタップ",
          "text": "地図か「一覧」の番号で、注意・時間・料金。「Googleマップで開く」からルート検索もできます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'A spring evening from Kyoto: Miidera by night MAP',
    titleMain: 'Miidera by night',
    titleSub: '三井寺の夜桜',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'The 17:16 from Sanjo Keihan for 18:00 entry, and the canal cherries after dark on the way back. If you come earlier in the day, see stop 1. The dotted line shows the order, not the actual path.',
    offKicker: 'Spring evenings only (out of season now)',
    offLead: 'The spring light-up isn’t on now. Dates and fees are from spring 2026 and train times from November 2026, so please check for next spring. ',
    offNote: 'A map for spring evenings only: the spring light-up isn’t on now, and next spring’s dates haven’t been announced. ',
    offHow: 'The spring light-up isn’t on now',
    offHowText: 'The 2026 run ended on 12 April, and next spring’s dates and fees are still to be announced. For spring, the plan is this. ',
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
    day: 'Daytime',
    meal: 'Meals',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 23, 2026',
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
    pickNote: 'Tap “Want to go” on the places you like. Times are for the full route.',
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
      "kicker": "A spring evening route, hand-walked by Toshi",
      "h1": "A lit National Treasure hall, and canal cherries on the way back.",
      "lead": "For only about three weeks each spring, the cherries at Miidera (Onjoji) and along the Lake Biwa Canal are lit at night. Enter by the great gate at 18:00 and wait at the National Treasure main hall for dark, when the blossom turns pink and violet under the lights, then go on to the pagoda and the night view from the Kannon hall on the hill. On the way back, walk the canal with lit cherries on both banks. Otsu is 30 minutes by train from Sanjo, and you are back just after 21:00 (25 March – 12 April in 2026; please check for next spring).",
      "favLabel": "Highlight",
      "favName": "The canal cherries at night",
      "favText": "Lit cherries along both banks of the dark waterway.",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "Before you go",
      "who": [
        "About 30 min and ¥520 from Sanjo Keihan on a train for Biwako-Hamaotsu. Trains for Rokujizo don’t go to Otsu",
        "The evening ticket was ¥1,500 in spring 2026, separate from the ¥800 day ticket (please check for next spring)",
        "Coming earlier? See stop 1: Sakamoto, Miidera by day, the canal boat and an early eel dinner at Otani",
        "You’re back in Sanjo after 21:00, so have a snack if you set out in the evening",
        "There are dark stone steps: wear good shoes and bring a jacket"
      ],
      "dayHead": "The evening, roughly like this",
      "from": "",
      "day": [
        {
          "time": "17:16",
          "area": "Sanjo → Otsu",
          "title": "Subway straight onto the Keishin line",
          "text": "The 17:16 from Sanjo Keihan for Biwako-Hamaotsu. Change there for Miidera at 17:46 (17:42 weekends and holidays), then follow the canal to the Daimon.",
          "note": "¥520",
          "photo": [
            5,
            2
          ]
        },
        {
          "time": "18:00",
          "area": "Miidera",
          "title": "Evening entry at the Daimon",
          "text": "A separate ticket from the daytime, into grounds with over a thousand cherry trees.",
          "note": "Last entry 21:00",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "18:20",
          "area": "Miidera",
          "title": "Wait for dark at the main hall",
          "text": "Sunset is around 18:12–18:26. As it gets dark the avenue turns pink and violet.",
          "note": "",
          "photo": [
            2,
            4
          ]
        },
        {
          "time": "18:55",
          "area": "Miidera",
          "title": "The pagoda, then the view from the Kannon hall",
          "text": "See the pagoda’s silhouette, then head south: Kannon hall at 19:15, start down by 19:40.",
          "note": "Steps",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "20:00",
          "area": "On the way back",
          "title": "The canal in the dark",
          "text": "The avenue from the Otsu lock to the first tunnel. Free, lit until 21:30 (spring 2026).",
          "note": "5 min to train",
          "photo": [
            5,
            0
          ]
        },
        {
          "time": "20:39",
          "area": "Otsu → Sanjo",
          "title": "The rest of the night in Sanjo",
          "text": "Sanjo Keihan 21:08 (21:07 weekends and holidays). Night cherries at Gion Shirakawa or Maruyama Park (until 22:00 in spring 2026, for a shorter season), or dinner around Kiyamachi and Pontocho.",
          "note": "Last 23:17",
          "photo": [
            5,
            1
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "¥520 each way from Sanjo Keihan. Admission is as in spring 2026; please check for next spring.",
      "deals": [
        {
          "name": "Miidera spring illumination (spring 2026)",
          "price": "¥1,500",
          "text": "25 Mar – 12 Apr 2026, 18:00–21:30 (last entry 21:00). ¥700 for school pupils. Please check for next spring.",
          "url": "https://miidera1200.jp/2026lightup-spring/"
        },
        {
          "name": "Sanjo Keihan → Miidera",
          "price": "¥520",
          "text": "Change at Biwako-Hamaotsu. ¥540 from Kyoto Shiyakusho-mae, ¥440 from Kyoto Station by JR and Keihan.",
          "url": "https://transit.yahoo.co.jp/search/result?from=%E4%B8%89%E6%9D%A1%E4%BA%AC%E9%98%AA&to=%E4%B8%89%E4%BA%95%E5%AF%BA&y=2026&m=12&d=02&hh=17&m1=1&m2=5&type=1&ticket=normal&expkind=1&ws=3&s=0"
        },
        {
          "name": "Canal cherries (spring 2026)",
          "price": "Free",
          "text": "Lit 18:00–21:30, 25 Mar – 12 Apr 2026. Please check for next spring.",
          "url": "https://otsu.or.jp/tripideas/otsu-sakura/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 23, 2026 (spring details as held in 2026; trains on the November 2026 timetable).",
      "dealsMore": "Details",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Take the 17:16 from Sanjo Keihan",
          "text": "Take the 17:16 from Sanjo Keihan for Biwako-Hamaotsu to make 18:00 entry. Follow 1 to 5: the temple first, the canal after dark on your way back."
        },
        {
          "title": "Entry until 21:00, lights until 21:30",
          "text": "As in spring 2026 (please check for next spring). Be at the Daimon by 19:30 to see it all. The 20:39 is the train back; the last is 23:17."
        },
        {
          "title": "Coming earlier? See stop 1",
          "text": "A timetable for leaving around 9:30 via Sakamoto and Miidera by day, the canal boat, and an early dinner."
        },
        {
          "title": "Tap a number",
          "text": "On the map or in the list, for warnings, times and fees. “Open in Google Maps” gives directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi."
    }
  }
};
