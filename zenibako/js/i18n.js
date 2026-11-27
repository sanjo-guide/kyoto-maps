/* Page texts in Japanese and English.
   Toshi 個人のマップ。銭函と朝里（札幌から日帰り。起点は札幌駅〜大通〜すすきののホテル。コースは1つ、冬もこのまま回れる）：
   札幌10:00発→1 札幌駅・2 銭函駅・3 豊足神社・4 銭函の浜とお昼（しろくまコーヒー／手打ちそば 春別）→5 朝里駅→中央バス13番→6 朝里川温泉→7 小樽倉庫No.1・8 小樽駅→札幌。
   写真はすべて Wikimedia Commons（オーナーはまだ北海道の写真を持っていない。行った・食べたと書かない）。写真は [スポットの番号, 写真の番号]。
   時刻・料金は2026年11月26日に確認（出典は data/routes/zenibako.json の sources。データは scripts/build_zenibako_data.py）。
   このファイルは直接直してよい。直したら scripts/sync_zenibako.py の EXTRA の js/i18n.js を上げてから sync を実行する */
window.ZENIBAKO_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '銭函と朝里 札幌から日帰り Zenibako MAP',
    titleMain: '銭函と朝里',
    titleSub: 'Zenibako & Asari',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号は回る順番です。午前は銭函、午後は朝里と朝里川温泉、夜は小樽。お昼のそば屋と醸造所の見学は、4番と2番の中で案内しています。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '文章：Toshi<br>写真：Wikimedia Commons（撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    bus: 'バス',
    walk: '歩く',
    pay: '支払い',
    reserve: '予約',
    tattoo: 'タトゥー',
    season: '季節',
    closed: '休み',
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
    pickNote: '行きたい場所の「行きたい」を押してください。札幌駅・銭函駅・小樽駅はいつもルートに入ります。時間は全部回る場合の目安です。',
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
      "kicker": "札幌から日帰り",
      "h1": "小樽の手前で降りる。海べりの駅、丘の上の神社、谷の温泉。",
      "lead": "札幌から快速で21分の銭函（ぜにばこ）は、ニシン漁で栄えた海べりの小さな町。1931年の駅舎と丘の上の神社を見て、駅の目の前の浜でお昼にします。午後は海のすぐそばを走る電車で朝里（あさり）へ、バスで谷を上って朝里川温泉。夜は小樽の運河沿いでビールと晩ごはんを食べて、札幌に帰ります。",
      "favLabel": "いちばんの見どころ",
      "favName": "銭函から朝里への車窓",
      "favText": "線路のすぐ横が海です。札幌の側から乗るなら、進行方向の右側に座ってください。（写真：Takeshi Aida / CC BY-SA 4.0）",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "先に知っておくこと",
      "who": [
        "札幌駅から快速で21分。大通・すすきののホテルを9:35ごろに出て、小樽20:57発の電車で21:44に札幌に戻る時間割です",
        "冬（12〜3月）もこの時間割で回れます。外を歩くのは14時半ごろまでで、あとは温泉と店の中。すべりにくい靴で",
        "温泉のタトゥーの決まりは、公式サイトに書かれていません（要確認）。貸切の家族風呂（要予約）があります",
        "中央バスはICカードか現金で、現金はおつりが出ません。千円札と小銭を。北海道レールパスで乗れるのはJRだけです",
        "小樽ビール銭函醸造所の見学は、1週間前までの電話予約（日本語）だけ。時間割には入れていません",
        "夏（7〜8月）は銭函の海水浴場が開きます。泳ぐなら水着とタオルを"
      ],
      "dayHead": "1日の流れ（平日・土曜の目安）",
      "from": "",
      "day": [
        {
          "time": "10:00",
          "area": "札幌 → 銭函",
          "title": "快速エアポートで21分",
          "text": "10:21に銭函へ。1931年の駅舎と、ホームに飾られた「銭函」を見てから町へ。（写真：Keiichi Yasu / CC BY-SA 2.0）",
          "photo": [
            2,
            1
          ]
        },
        {
          "time": "10:40",
          "area": "銭函",
          "title": "駅の裏の丘の神社",
          "text": "坂を5分上って豊足神社へ。境内には、この浜で見つかった日露戦争の機雷の残骸があります。（写真：禁樹なずな / CC BY-SA 4.0）",
          "photo": [
            3,
            0
          ]
        },
        {
          "time": "11:10",
          "area": "銭函",
          "title": "浜を歩いて、海の前でお昼",
          "text": "湾の向こうに増毛の山。お昼は浜の前のしろくまコーヒーか、少し歩いて手打ちそば 春別へ。（写真：くろふね / CC BY 3.0）",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "13:22",
          "area": "銭函 → 朝里",
          "title": "海すれすれを走る電車",
          "text": "右側の窓に海。朝里の石の浜で電車と海を眺めて、14:27のバスで温泉へ。（写真：Takeshi Aida / CC BY-SA 4.0）",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "14:39",
          "area": "朝里川温泉",
          "title": "谷の温泉で3時間",
          "text": "露天風呂とフィンランド式サウナ。17:56のバスで小樽へ下ります。（写真：RJD / CC BY 3.0）",
          "photo": [
            6,
            1
          ]
        },
        {
          "time": "18:50",
          "area": "小樽",
          "title": "運河沿いの醸造所で晩ごはん",
          "text": "小樽倉庫No.1で、店の中で造る小樽ビール。木曜と土曜は飲み放題の日です。（写真：Braveheart / CC BY-SA 4.0）",
          "photo": [
            7,
            0
          ]
        },
        {
          "time": "20:57",
          "area": "小樽 → 札幌",
          "title": "札幌に21:44",
          "text": "次は21:16発。最終は23:08発です。（写真：SElefant / CC BY-SA 3.0）",
          "note": "小樽20:57発→札幌21:44着",
          "photo": [
            8,
            1
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "交通費と入浴料のめやす",
      "dealsLead": "JRは3回乗ります（札幌→銭函、銭函→朝里、小樽→札幌）。交通系ICカードなら、きっぷを買わずに乗れます。バス代と入浴料は別です。",
      "deals": [
        {
          "name": "札幌 → 銭函（JR）",
          "price": "片道470円",
          "text": "快速エアポートで21分。交通系ICカードと北海道レールパスで乗れます。指定席の車両だけは別料金です。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "銭函 → 朝里（JR）",
          "price": "片道310円",
          "text": "8分。札幌の側から乗るときは、海は進行方向の右側です。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "中央バス13番（朝里町 → 温泉南 → 小樽駅前）",
          "price": "要確認",
          "text": "運賃は公式の時刻表に出ていません。小樽築港駅〜温泉南は410円（朝里川温泉ホテルの案内）。ICカードか現金で、現金はおつりが出ません。",
          "url": "https://www.chuo-bus.co.jp/support/faq/"
        },
        {
          "name": "朝里川温泉ホテル 日帰り入浴",
          "price": "850円",
          "text": "土日祝・年末年始は1,000円。タオルは別（フェイスタオル200円、バスタオルの貸し出し200円）。貸切の家族風呂は60分3,000円・要予約。",
          "url": "https://asarigawaonsenhotel.com/"
        },
        {
          "name": "小樽 → 札幌（JR）",
          "price": "片道800円",
          "text": "20:57発で札幌21:44着。最終は23:08発です。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "小樽倉庫No.1 木曜・土曜の飲み放題",
          "price": "2時間2,600円",
          "text": "ビールの飲み放題、予約なしで。料理は別。醸造所の見学（試飲なし）は無料です。",
          "url": "https://otarubeer.com/jp/Ppage_id=357.html"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月26日に、各施設の公式サイト、北海道中央バスの時刻表（2026年4月1日改定）、乗換案内（12月3日・5日のダイヤ）で確認しました。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "番号の順に",
          "text": "1から8の順に回ると、午前は銭函、午後は朝里と温泉、夜は小樽。「おすすめの時間」は、札幌を10:00に出た日の目安です（平日・土曜）。"
        },
        {
          "title": "選んで回ることも",
          "text": "「選んで回る」に切り替えると、行かない場所を外せます。外したときの行き方は、ひとことで出ます。"
        },
        {
          "title": "番号をタップ",
          "text": "写真・説明・時刻・料金が見られます。予約、タトゥー、バスの払い方など、入口で困ることはいちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップ」から、そのままルート検索できます。お昼のそば屋と醸造所は、4番と2番の中にあります。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（公式サイトなどの情報と、Wikimedia Commons の写真で紹介しています）。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Zenibako & Asari: a day trip from Sapporo MAP',
    titleMain: 'Zenibako & Asari',
    titleSub: '銭函と朝里',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'The numbers are the order to go in: Zenibako in the morning, Asari and Asarigawa Onsen in the afternoon, Otaru in the evening. The soba restaurant and the brewery tour are covered inside stops 4 and 2. The dotted line only shows the order; it is not the actual path.',
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
    credit: 'Text: Toshi<br>Photos: Wikimedia Commons (the photographer and licence are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    bus: 'Bus',
    walk: 'On foot',
    pay: 'Paying',
    reserve: 'Booking',
    tattoo: 'Tattoos',
    season: 'Season',
    closed: 'Closed',
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
    pickNote: 'Tap “Want to go” on the places you like. Sapporo, Zenibako and Otaru stations are always on your route. Times are for the full route.',
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
      "kicker": "A day trip from Sapporo",
      "h1": "Get off before Otaru: a seaside station, a hilltop shrine, a hot spring up the valley.",
      "lead": "Zenibako, 21 minutes from Sapporo by rapid train, is a small seaside town that grew on herring fishing. See the 1931 station and the shrine on the hill, then have lunch on the beach right outside the station. In the afternoon the train runs along the water’s edge to Asari, and a bus climbs the valley to Asarigawa Onsen. End the day with beer and dinner by the Otaru canal, then ride back to Sapporo.",
      "favLabel": "Best moment",
      "favName": "The train from Zenibako to Asari",
      "favText": "The sea runs right beside the tracks. Coming from the Sapporo side, sit on the right. (Photo: Takeshi Aida / CC BY-SA 4.0)",
      "favPhoto": [
        5,
        0
      ],
      "whoHead": "Good to know",
      "who": [
        "21 minutes from Sapporo by rapid train. Leave your hotel around Odori or Susukino at about 9:35; the 20:57 train from Otaru gets you back to Sapporo at 21:44",
        "This plan works in winter (Dec–Mar) too: the outdoor parts end around 14:30, then it is the hot spring and indoors. Wear shoes with grippy soles",
        "The hot spring publishes no tattoo policy (please check). It has a private family bath you can book",
        "The bus takes IC cards or cash, and gives no change: carry ¥1,000 notes and coins. The Hokkaido Rail Pass covers JR trains only",
        "The Zenibako brewery tour is by phone booking only (in Japanese), at least a week ahead, so it is not in the timetable",
        "In summer (Jul–Aug) Zenibako’s swimming beach opens. Bring swimwear and a towel if you want to swim"
      ],
      "dayHead": "The day at a glance (weekdays and Saturdays)",
      "from": "",
      "day": [
        {
          "time": "10:00",
          "area": "Sapporo → Zenibako",
          "title": "21 minutes on the Rapid Airport",
          "text": "Arrive 10:21. See the 1931 station house and the money box on the platform, then head into town. (Photo: Keiichi Yasu / CC BY-SA 2.0)",
          "photo": [
            2,
            1
          ]
        },
        {
          "time": "10:40",
          "area": "Zenibako",
          "title": "The shrine on the hill",
          "text": "Five minutes uphill to Toyotari Shrine, where the remains of a Russo-Japanese War mine found on this beach are kept. (Photo: 禁樹なずな / CC BY-SA 4.0)",
          "photo": [
            3,
            0
          ]
        },
        {
          "time": "11:10",
          "area": "Zenibako",
          "title": "The beach, then lunch by the sea",
          "text": "Mountains across the bay. Lunch at Shirokuma Coffee on the beach, or a short walk to Shunbetsu for soba. (Photo: くろふね / CC BY 3.0)",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "13:22",
          "area": "Zenibako → Asari",
          "title": "Along the water’s edge",
          "text": "The sea is on the right. Watch the trains from the stony shore at Asari, then take the 14:27 bus. (Photo: Takeshi Aida / CC BY-SA 4.0)",
          "photo": [
            5,
            1
          ]
        },
        {
          "time": "14:39",
          "area": "Asarigawa Onsen",
          "title": "Three hours at a valley hot spring",
          "text": "Outdoor bath and Finnish sauna, then the 17:56 bus down to Otaru. (Photo: RJD / CC BY 3.0)",
          "photo": [
            6,
            1
          ]
        },
        {
          "time": "18:50",
          "area": "Otaru",
          "title": "Dinner in a canal-side brewery",
          "text": "Otaru Beer brewed on the spot at Otaru Soko No.1. Thursdays and Saturdays are all-you-can-drink days. (Photo: Braveheart / CC BY-SA 4.0)",
          "photo": [
            7,
            0
          ]
        },
        {
          "time": "20:57",
          "area": "Otaru → Sapporo",
          "title": "Sapporo at 21:44",
          "text": "The next train is at 21:16; the last at 23:08. (Photo: SElefant / CC BY-SA 3.0)",
          "note": "Otaru 20:57 → Sapporo 21:44",
          "photo": [
            8,
            1
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and bath fees",
      "dealsLead": "You ride JR three times (Sapporo → Zenibako, Zenibako → Asari, Otaru → Sapporo). With an IC card you don’t need to buy tickets. The bus and the bath are extra.",
      "deals": [
        {
          "name": "Sapporo → Zenibako (JR)",
          "price": "¥470 one way",
          "text": "21 minutes on the Rapid Airport. IC cards and the Hokkaido Rail Pass are accepted. Only the reserved car costs extra.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Zenibako → Asari (JR)",
          "price": "¥310 one way",
          "text": "8 minutes. Coming from the Sapporo side, the sea is on the right.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Chuo Bus no. 13 (Asarimachi → Onsen-minami → Otaru Station)",
          "price": "Please check",
          "text": "The official timetable gives no fares. Otaru-Chikko Station to Onsen-minami is ¥410, according to Asarigawa Onsen Hotel. IC card or cash; no change is given.",
          "url": "https://www.chuo-bus.co.jp/support/faq/"
        },
        {
          "name": "Asarigawa Onsen Hotel, day bathing",
          "price": "¥850",
          "text": "¥1,000 on weekends, holidays and over New Year. Towels extra (face towel ¥200, bath towel rental ¥200). Private family bath ¥3,000 for 60 minutes, booking required.",
          "url": "https://asarigawaonsenhotel.com/en/"
        },
        {
          "name": "Otaru → Sapporo (JR)",
          "price": "¥800 one way",
          "text": "The 20:57 reaches Sapporo at 21:44. The last train is at 23:08.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Otaru Soko No.1, Thursday and Saturday beer deal",
          "price": "¥2,600 for 2 hours",
          "text": "All-you-can-drink beer, no booking needed. Food extra. The self-guided brewery visit (no tasting) is free.",
          "url": "https://otarubeer.com/jp/Ppage_id=357.html"
        }
      ],
      "dealsNote": "Adult fares and prices, checked on 26 November 2026 on each official website, Chuo Bus’s timetable (revised 1 April 2026) and a route planner (timetables for 3 and 5 December).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "In number order",
          "text": "Follow 1 to 8: Zenibako in the morning, Asari and the hot spring in the afternoon, Otaru in the evening. Suggested times assume you leave Sapporo at 10:00 on a weekday or Saturday."
        },
        {
          "title": "Or choose your stops",
          "text": "Switch to “Choose stops” to drop places you don’t want. A short note tells you how the route changes."
        },
        {
          "title": "Tap a number",
          "text": "See photos, tips, times and fees. Things that can stop you at the door — bookings, tattoos, paying on the bus — are shown at the top."
        },
        {
          "title": "Get directions",
          "text": "Use the Google Maps buttons at each spot for directions. The soba restaurant and the brewery are inside stops 4 and 2."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi, made from official information and photos from Wikimedia Commons."
    }
  }
};
