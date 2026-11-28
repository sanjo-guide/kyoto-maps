/* Page texts in Japanese and English.
   Toshi 個人のマップ。神戸の1日ルート（起点は大阪の梅田〜難波のあたりのホテル。コースは1つ）：
   大阪梅田9:30発→神戸三宮→北野天満神社→北野異人館街→三宮のかつ丼→布引の滝→南京町→メリケンパーク・ポートタワー→夜のハーバーランド。
   Photos are [spot number, photo index] from data/routes/kobe.json（1 三宮・2 北野天満神社・3 異人館・4 七兵衛・5 布引の滝・6 メリケンパーク）.
   時刻・料金は2026年11月22日に確認（各施設・神戸市・神戸観光局の公式サイト、電車は乗換案内）。
   このファイルは直接直してよい（データは scripts/build_kobe_data.py）。 */
window.KOBE_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '神戸 1日ルート Kobe MAP',
    titleMain: '神戸',
    titleSub: 'Kobe',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号は回る順番です。午前に北野、三宮でお昼、午後に布引の滝、夕方から港へ。南京町と夜のハーバーランドは6番の中で案内しています。行かない場所は「選んで回る」で外せます。点線は順番を示す線で、実際の道ではありません。',
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
    pickNote: '行きたい場所の「行きたい」を押してください。神戸三宮駅はいつもルートに入ります。時間は全部回る場合の目安です。',
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
      "kicker": "大阪の梅田〜難波のホテルから1日",
      "h1": "午前は坂の上の異人館、午後は駅の裏の滝、夜は港のあかり。",
      "lead": "朝は北野坂を上って、坂の上の異人館へ。北野天満神社の境内からは、町と海が見下ろせます。お昼は三宮の高架下のかつ丼。午後は新幹線の新神戸駅のすぐ裏から山道に入り、4つの滝を上って布引の滝の雄滝へ。南京町でつまんでから海へ出て、メリケンパークで日の入りを迎え、明かりの入ったポートタワーを対岸から眺めて晩ごはんまで。大阪梅田から阪急の特急で27分、梅田を9:30に出る時間割です。",
      "favLabel": "いちばんの見どころ",
      "favName": "布引の滝（雄滝）",
      "favText": "新幹線の新神戸駅から歩いて15分で、落差43mの滝の前に立てます。入場料はいりません。",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "大阪に泊まって、神戸を1日で。梅田を9:30に出て、21時ごろの電車で帰る時間割です",
        "大阪梅田→神戸三宮は阪急の特急で27分・330円。難波からは阪神なんば線で乗り換えなし・420円",
        "坂と階段をよく歩きます（北野坂の上りが20分ほど、滝は階段の山道）。歩きやすい靴で",
        "異人館は館ごとに入館料がかかります。風見鶏の館と萌黄の館の2館券（800円）から",
        "ポートタワーは日時指定のチケット。夕暮れに上りたい日は、先に公式サイトで",
        "京都から来る人は、阪急で十三乗り換えの約1時間20分・640円。JRの新快速なら51分・1,110円"
      ],
      "dayHead": "1日の流れ（11月下旬・土曜の目安）",
      "from": "",
      "day": [
        {
          "time": "9:30",
          "area": "大阪梅田 → 神戸三宮",
          "title": "阪急の特急で27分",
          "text": "9:57に着いたら、山のほうへ北野坂をゆっくり上ります。難波からは阪神なんば線で9:37発、10:18着。",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "10:25",
          "area": "北野",
          "title": "天満神社から異人館へ",
          "text": "まず北野天満神社の境内から町と海を見下ろして、風見鶏の館と萌黄の館へ。入る館は2〜3館にしぼります。",
          "photo": [
            3,
            1
          ]
        },
        {
          "time": "12:20",
          "area": "三宮",
          "title": "高架下のかつ丼でお昼",
          "text": "北野坂を下って、阪急の駅のすぐ横の七兵衛へ。売り切れると閉まるので、お昼は遅くしません。",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "13:25",
          "area": "新神戸",
          "title": "駅の裏の滝と展望台",
          "text": "地下鉄で1駅。4つの滝を上って、みはらし展望台のベンチで休みます。15時には下りはじめます。",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "15:15",
          "area": "南京町 → メリケンパーク",
          "title": "つまんでから、港の日の入りへ",
          "text": "南京町を抜けて海へ。日の入りは16:50ごろ。16:30ごろの枠でポートタワーに上ると、明かりがつくまでを上から見られます。",
          "photo": [
            6,
            2
          ]
        },
        {
          "time": "18:00",
          "area": "ハーバーランド",
          "title": "対岸から夜景、モザイクで晩ごはん",
          "text": "海ぞいを歩いてモザイクへ。明かりの入ったポートタワーを眺めて、晩ごはん。飲食店は22:00までです。",
          "note": "神戸21:13発→大阪21:39着",
          "photo": [
            6,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と入場料のめやす",
      "dealsLead": "電車は大阪梅田から神戸三宮まで片道330円、帰りをJR神戸駅からにすると460円。地下鉄の往復420円と合わせて、交通費は1,200円ほど。入館料は別です。",
      "deals": [
        {
          "name": "大阪梅田 → 神戸三宮（阪急・阪神）",
          "price": "片道330円",
          "text": "阪急の特急で27分、10分おき。JRの新快速は大阪→三ノ宮21分・420円。難波からは阪神なんば線の快速急行で41分・420円、乗り換えなし。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "地下鉄 三宮 ⇄ 新神戸",
          "price": "片道210円",
          "text": "1駅・2分。布引の滝への行き帰りに。歩くと上り坂を約20分です。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "風見鶏の館・萌黄の館 2館共通券",
          "price": "800円",
          "text": "1館ずつなら各500円。高校生以下は無料。ほかの館は550〜1,100円です。",
          "url": "https://kobe-kazamidori.com/guide/"
        },
        {
          "name": "神戸ポートタワー",
          "price": "1,200円",
          "text": "展望フロア＋屋上デッキ。展望フロアだけなら1,000円。日時指定のチケット制で、当日券は枠に空きがあるときだけ。",
          "url": "https://www.kobe-port-tower.com/ticket/"
        },
        {
          "name": "京都から来る人・京都へ帰る人",
          "price": "片道640〜1,110円",
          "text": "行き：阪急の京都河原町8:46発→十三で乗り換え→神戸三宮10:07着・640円。JRは京都9:00発の新快速→三ノ宮9:51着・1,110円。帰り：JR神戸21:13発の新快速→京都22:09着。最後は神戸23:32発（三ノ宮23:36発）の新快速、阪急なら神戸三宮23:10発です。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日に確認しました（各施設・神戸市・神戸観光局の公式サイト、電車は乗換案内の11月28日・土曜のダイヤ）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "番号の順に",
          "text": "1から6の順に回ると、午前に北野、お昼に三宮、午後に滝、夕方から港へと動けます。「おすすめの時間」は、大阪梅田を9:30に出た日の目安です。"
        },
        {
          "title": "選んで回ることも",
          "text": "「選んで回る」に切り替えると、行きたい場所だけを選べます。外した場所に合わせて、行き方のひとことが出ます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・おすすめの時間が見られます。入る前に知っておきたいことは、いちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップ」から、そのままルート検索できます。南京町・モザイク・JR神戸駅は6番の中にあります。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kobe in one day MAP',
    titleMain: 'Kobe',
    titleSub: '神戸',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'The numbers are the order to go in: Kitano in the morning, lunch in Sannomiya, Nunobiki Falls after lunch, the harbour from late afternoon. Chinatown and Harborland at night are covered inside stop 6. Use “Choose stops” to drop places you’ll skip. The dotted line shows the order, not the actual path.',
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
    pickNote: 'Tap “Want to go” on the places you like. Sannomiya is always on your route. Times are for the full route.',
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
      "kicker": "One day from a hotel in Osaka (Umeda–Namba)",
      "h1": "Hillside houses in the morning, a waterfall behind the station after lunch, harbour lights at night.",
      "lead": "In the morning, walk up Kitano-zaka to the old foreign residences on the hill; from Kitano Tenman Shrine you look down over the town and the sea. Lunch is katsudon under the tracks in Sannomiya. After lunch, a trail starts right behind Shin-Kobe bullet-train station and climbs past four falls to Ontaki, the biggest of the Nunobiki Falls. Snack through Chinatown, watch the sun set at Meriken Park, and see the lit-up Port Tower from across the water before dinner. Osaka-Umeda is 27 minutes away by Hankyu limited express; the timetable starts from Umeda at 9:30.",
      "favLabel": "Highlight",
      "favName": "Nunobiki Falls (Ontaki)",
      "favText": "Fifteen minutes’ walk from Shin-Kobe bullet-train station, you stand in front of a 43 m waterfall. No admission charge.",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "Who it’s for",
      "who": [
        "Staying in Osaka and seeing Kobe in a day: leave Umeda at 9:30, take a train home around 21:00",
        "Osaka-Umeda to Kobe-Sannomiya is 27 min and ¥330 by Hankyu limited express; from Namba the Hanshin Namba Line runs direct for ¥420",
        "Plenty of slopes and steps (a 20-minute climb up Kitano-zaka, a trail of steps at the falls): wear good shoes",
        "Every house in Kitano charges admission. Start with the ¥800 ticket for the Weathercock and Moegi houses",
        "The Port Tower needs a timed ticket. For a dusk slot, buy on the official site beforehand",
        "From Kyoto: about 1 h 20 min by Hankyu with a change at Juso (¥640), or 51 min by JR Special Rapid (¥1,110)"
      ],
      "dayHead": "One day, roughly like this (a Saturday in late November)",
      "from": "From",
      "day": [
        {
          "time": "9:30",
          "area": "Osaka-Umeda → Kobe-Sannomiya",
          "title": "27 minutes by Hankyu",
          "text": "Arrive at 9:57 and walk slowly up Kitano-zaka towards the hills. From Namba, the Hanshin Namba Line leaves at 9:37 and arrives at 10:18.",
          "photo": [
            1,
            0
          ]
        },
        {
          "time": "10:25",
          "area": "Kitano",
          "title": "From the shrine to the houses",
          "text": "First look down over the town and the sea from Kitano Tenman Shrine, then visit the Weathercock and Moegi houses. Pick two or three houses to enter.",
          "photo": [
            3,
            1
          ]
        },
        {
          "time": "12:20",
          "area": "Sannomiya",
          "title": "Katsudon under the tracks",
          "text": "Down Kitano-zaka to Hichibei, right beside the Hankyu station. It closes when it sells out, so lunch is not left late.",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "13:25",
          "area": "Shin-Kobe",
          "title": "The falls and lookout behind the station",
          "text": "One stop by subway. Climb past four falls and rest on the benches at the Miharashi lookout. Start down by 15:00.",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "15:15",
          "area": "Chinatown → Meriken Park",
          "title": "A snack, then sunset at the harbour",
          "text": "Through Nankinmachi to the sea. Sunset is around 16:50; with a Port Tower slot around 16:30 you watch the lights come on from above.",
          "photo": [
            6,
            2
          ]
        },
        {
          "time": "18:00",
          "area": "Harborland",
          "title": "The night view, and dinner at Mosaic",
          "text": "Walk along the water to Mosaic, look back at the lit-up Port Tower, and have dinner. Restaurants stay open until 22:00.",
          "note": "Kobe 21:13 → Osaka 21:39",
          "photo": [
            6,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and admission",
      "dealsLead": "Osaka-Umeda to Kobe-Sannomiya is ¥330 one way; going home from JR Kobe Station costs ¥460. With ¥420 for the subway there and back, transport comes to about ¥1,200. Admission is extra.",
      "deals": [
        {
          "name": "Osaka-Umeda → Kobe-Sannomiya (Hankyu / Hanshin)",
          "price": "¥330 one way",
          "text": "27 min by Hankyu limited express, every 10 minutes. JR Special Rapid Osaka → Sannomiya is 21 min, ¥420. From Namba, the Hanshin Namba Line rapid express takes 41 min, ¥420, direct.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Subway Sannomiya ⇄ Shin-Kobe",
          "price": "¥210 one way",
          "text": "One stop, 2 minutes, to and from Nunobiki Falls. On foot it is about 20 minutes uphill.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Weathercock & Moegi combined ticket",
          "price": "¥800",
          "text": "¥500 each separately. Free for high school and under. Other houses cost ¥550–1,100.",
          "url": "https://kobe-kazamidori.com/guide/"
        },
        {
          "name": "Kobe Port Tower",
          "price": "¥1,200",
          "text": "Observation floors + rooftop deck; ¥1,000 for the floors only. Timed tickets; same-day tickets only if the slot has space.",
          "url": "https://www.kobe-port-tower.com/ticket/"
        },
        {
          "name": "To and from Kyoto",
          "price": "¥640–1,110 one way",
          "text": "Out: Hankyu from Kyoto-Kawaramachi 8:46, change at Juso, Kobe-Sannomiya 10:07, ¥640. JR Special Rapid from Kyoto 9:00, Sannomiya 9:51, ¥1,110. Back: JR Special Rapid from Kobe 21:13, Kyoto 22:09. The last ones are the Special Rapid from Kobe at 23:32 (Sannomiya 23:36) and Hankyu from Kobe-Sannomiya at 23:10.",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 22, 2026 (official sites of the venues, Kobe City and Feel KOBE; trains on a route planner, Saturday 28 November timetable).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "In number order",
          "text": "Follow 1 to 6: Kitano in the morning, lunch in Sannomiya, the falls after lunch, the harbour from late afternoon. Suggested times assume you leave Osaka-Umeda at 9:30."
        },
        {
          "title": "Or choose your stops",
          "text": "Switch to “Choose stops” to pick only the places you want. A short note tells you how the route changes."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees and suggested times. Things to know before you go in are shown at the top."
        },
        {
          "title": "Get directions",
          "text": "Use the Google Maps buttons at each spot for directions. Chinatown, Mosaic and JR Kobe Station are inside stop 6."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi."
    }
  }
};
