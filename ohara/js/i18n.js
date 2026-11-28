/* Page texts in Japanese and English.
   Toshi 個人のマップ。三条京阪前から京都バスで大原へ。コースは2つ（三千院の開門に合わせる／9〜10時に出発）。
   intro は「9〜10時に出発」の内容で、introFor.early が app.js で上書きされる（scripts/sync_ohara.py）。
   （宝泉院・実光院・来迎院と音無の滝・里の道・寂光院はオーナーの写真がない場所。写真は Wikimedia Commons）。
   Photos are [spot id, photo index] from data/routes/ohara.json（コースで番号が変わるので id で指定）。
   時刻・料金は2026年11月21〜22日に確認（京都バスの公式時刻表、各寺の公式サイト、乗換案内）。 */
window.OHARA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 大原 Ohara MAP',
    titleMain: '大原',
    titleSub: 'Ohara',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '上のボタンで出発時間を選ぶと、回る順番と時間が変わります。開門に合わせるコースは三千院が先、9〜10時発のコースは寂光院が先で三千院は午後です。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（宝泉院・実光院・来迎院と音無の滝・里の道・寂光院の写真と、三千院のわらべ地蔵の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: 'バス',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや時刻表で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月21〜22日',
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
    pickNote: '最初は、時間割どおりに1日で回れる組み合わせが選んであります。行かない所は外し、寄り道（音無の滝など）は「行きたい」を押して足してください。半日なら三千院と宝泉院だけで十分です。',
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "三千院の開門に合わせる\n三条京阪前 7:57発",
    courseLate: "9〜10時に出発\n三千院は午後",
    swMode: "回り方",
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
      "kicker": "Toshiが歩いて作った京都のルート",
      "h1": "杉木立の下の苔の庭と、額縁の庭でいただくお抹茶。三条からバス1本の山里、大原へ。",
      "lead": "京都の町の北、山に囲まれた大原の里まで、三条京阪前から京都バス1本です。9〜10時に出る日は、人の集まる三千院を14時すぎに回して、先に田んぼの中の道を歩き、谷の反対側の寂光院へ。お昼は11時半に早めに入り、宝泉院でお抹茶、団体が帰りはじめるころに三千院の苔の庭へ。夕方のバスで三条へ戻って、晩ごはんは先斗町・木屋町で。朝早く出られる人は、上のボタンで「三千院の開門に合わせる」コースに切り替えてください。私の写真は2024年11月、雨の日の夕方に撮ったものです。",
      "favLabel": "いちばんの見どころ",
      "favName": "三千院",
      "favText": "杉木立の下の苔と、もみじ。団体の多い10時〜昼すぎを外して、開門すぐか14時すぎに。雨の日と雨上がりがいちばんきれいです。",
      "favPhoto": [
        "sanzenin",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "行きも帰りも京都バス。三条京阪前から40〜50分・570円。秋の土日祝は混んで遅れます",
        "お昼の店は閉まるのが早い土地です。11時半ごろに入るのが楽。晩ごはんは街なかへ戻ってから",
        "三条京阪前まで乗り換えなしで帰れる最後のバスは17:47発。大原の最終は21:01発（国際会館駅前行き→地下鉄）",
        "拝観料は現金を用意。三千院700円＋宝泉院1,000円＋実光院600円＋寂光院600円",
        "実光院の受付は15:30まで。三千院は11月16:45、12〜2月16:30まで",
        "三千院と寂光院は谷の反対側で、歩いて35分ほど。歩きやすい靴で",
        "京都の町なかより気温が低いので、秋と冬は上着を1枚多く"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "from": "",
      "day": [
        {
          "time": "9:48",
          "area": "大原バス停 → 寂光院",
          "title": "先に、静かな寂光院へ",
          "text": "三条京阪前9:07発のバスで大原へ。国道を渡らずに西へ、田んぼの中の道を20分歩いて寂光院。（写真：PlusMinus / CC BY-SA 3.0）",
          "photo": [
            "jakkoin",
            0
          ]
        },
        {
          "time": "11:15",
          "area": "里の道・参道",
          "title": "11時半に早めのお昼",
          "text": "里の道を戻って参道を上り、三千院の門前あたりでお昼。昼の混雑の前に入ります。",
          "photo": [
            "sando",
            0
          ]
        },
        {
          "time": "12:40",
          "area": "宝泉院・実光院・三千院",
          "title": "額縁庭園でお抹茶、14時すぎに三千院",
          "text": "宝泉院の額縁庭園でお抹茶、実光院の庭を歩いて、団体が帰りはじめるころに三千院へ。苔の庭と往生極楽院、わらべ地蔵。",
          "photo": [
            "sanzenin",
            5
          ]
        },
        {
          "time": "16:27",
          "area": "帰り → 三条・先斗町",
          "title": "バスで三条へ、晩ごはんは街なかで",
          "text": "参道でしば漬を買って、16:27発のバスに。三条京阪前から三条大橋を渡れば先斗町・木屋町。21〜22時ごろまで楽しめます。",
          "note": "大原16:27発 → 三条京阪前17:10着。乗り換えなしの最後は17:47発",
          "photo": [
            "kaeri",
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と拝観料のめやす",
      "dealsLead": "三条京阪前からバスで往復すると1,140円。地下鉄・バス1日券（1,100円）のほうが少し安く、夜に地下鉄や市バスにも乗れます。拝観料は別で、全部回ると2,900円です（来迎院を除く）。",
      "deals": [
        {
          "name": "京都バス 17系統",
          "price": "570円",
          "text": "三条京阪前→大原 40〜50分。四条河原町から590円、出町柳駅前から490円。帰りも同じ運賃です。",
          "url": "https://www.kyotobus.jp/route/timetable/"
        },
        {
          "name": "地下鉄・バス1日券",
          "price": "1,100円",
          "text": "京都バスは大原バス停まで使えます。京都バスの車内では買えないので、地下鉄の駅の券売機で先に。",
          "url": "https://www.kyotobus.jp/route/fare/discount/pass/post-3.html"
        },
        {
          "name": "三千院",
          "price": "700円",
          "text": "9:00〜17:00（11月 8:45〜16:45、12〜2月 9:00〜16:30）。休みなし。",
          "url": "https://www.sanzenin.or.jp/guide/"
        },
        {
          "name": "宝泉院",
          "price": "1,000円",
          "text": "お抹茶とお菓子つき。9:00〜17:00（受付は16:30まで）。",
          "url": "http://www.hosenin.net/haikan/"
        },
        {
          "name": "寂光院",
          "price": "600円",
          "text": "9:00〜17:00（12〜2月は16:30まで）。",
          "url": "https://www.jakkoin.jp/haikan/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21〜22日に確認しました（京都バスの公式時刻表、各寺の公式サイト、乗換案内）。実光院は600円（お抹茶つき1,100円）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「三千院の開門に合わせる」（三条京阪前7:57発）と「9〜10時に出発」（9:07発）を切り替えます。回る順番と時間が変わります。"
        },
        {
          "title": "番号の順に",
          "text": "1から9の順に回ると、時間割どおりの1日になります。番号をタップすると、写真・説明・料金・おすすめの時間が見られます。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "最初は、1日で無理なく回れる組み合わせが選んであります。音無の滝などの寄り道は「行きたい」を押して足してください。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが歩いて作った、オリジナルマップです（宝泉院・実光院・来迎院と音無の滝・寂光院は、公式サイトなどの情報と Wikimedia Commons の写真で紹介しています）。"
    },
    introFor: {
      early: {
        "lead": "団体が来る前の三千院に、開いてすぐ入る朝のコースです。苔の庭を歩いたら、宝泉院でお抹茶のひと休み。11時半に早めのお昼を食べ、午後は田んぼの中の道を寂光院へ歩いて、14:27のバスで戻ります。15時すぎに三条。宿で休んで、夜は先斗町・木屋町へ。行きは朝7:57に三条京阪前を出るバスです。私の写真は2024年11月、雨の日の夕方に撮ったものです。",
        "favText": "11月は8:45、ほかの月は9:00に開きます。開門に合わせて行くと、団体が増える前に縁側に座れます。雨の日と雨上がりがいちばんきれいです。",
        "dayHead": "1日の流れ（三千院の開門に合わせる）",
        "day": [
          {
            "time": "8:38",
            "area": "参道・三千院",
            "title": "開いたばかりの三千院へ",
            "text": "三条京阪前7:57発のバスで大原へ（土日祝は8:49着）。川沿いの参道を上って、9時ごろ三千院。客殿の庭、苔の有清園、往生極楽院、わらべ地蔵。",
            "photo": [
              "sanzenin",
              5
            ]
          },
          {
            "time": "10:25",
            "area": "宝泉院",
            "title": "額縁庭園のお抹茶でひと休み",
            "text": "朝から歩いたあとの休憩に。畳に座って、柱を額縁にした庭を眺めます。（写真：Maechan0360 / CC BY-SA 3.0）",
            "photo": [
              "hosenin",
              0
            ]
          },
          {
            "time": "11:30",
            "area": "お昼・里の道・寂光院",
            "title": "早めのお昼のあと、谷の反対側へ",
            "text": "三千院の門前か参道で、混む前にお昼。参道を下り、田んぼの中の道を歩いて寂光院へ。（写真：PlusMinus / CC BY-SA 3.0）",
            "photo": [
              "jakkoin",
              0
            ]
          },
          {
            "time": "14:27",
            "area": "帰り → 三条・先斗町",
            "title": "15時すぎに三条。夜は街なかで",
            "text": "早起きした日なので、宿でひと休み。元気なら出町柳駅前で降りて鴨川デルタへ。晩ごはんは18時ごろから先斗町・木屋町で。",
            "note": "大原14:27発 → 出町柳駅前15:01着・三条京阪前15:10着",
            "photo": [
              "kaeri",
              0
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kyoto: Ohara MAP',
    titleMain: 'Ohara',
    titleSub: '大原',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Choose your start time with the buttons above: the order and the times change. The opening course does Sanzen-in first; the 9–10 course does Jakko-in first and Sanzen-in in the afternoon. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (photos of Hosen-in, Jikko-in, Raigo-in and the falls, the valley walk and Jakko-in, and the Warabe Jizo photo at Sanzen-in, are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Bus',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and timetables on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 21–22, 2026',
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
    pickNote: 'A set that fits one day as timed is chosen to begin with. Drop what you’ll skip and tap “Want to go” to add side trips (the Otonashi falls and so on). For a half day, Sanzen-in and Hosen-in are enough.',
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "Sanzen-in at opening\n7:57 from Sanjo",
    courseLate: "Leave at 9–10\nSanzen-in after lunch",
    swMode: "Stops",
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
      "kicker": "A Kyoto route, hand-walked by Toshi",
      "h1": "Moss under the cedars and matcha before a framed garden: Ohara, one bus ride from Sanjo.",
      "lead": "Ohara is a valley in the hills north of Kyoto, one Kyoto Bus ride from Sanjo-Keihan-mae. Leaving at 9–10, you save busy Sanzen-in for after 14:00 and first walk a lane through the fields to Jakko-in, across the valley. Sit down for an early lunch at 11:30, have matcha at Hosen-in, and reach Sanzen-in’s moss garden as the tour groups start to leave. A late-afternoon bus takes you back to Sanjo for dinner around Pontocho and Kiyamachi. If you can start early, switch to the “Sanzen-in at opening” course with the button above the list. My photos are from a rainy late afternoon in November 2024.",
      "favLabel": "Highlight",
      "favName": "Sanzen-in",
      "favText": "Moss under tall cedars, and maples. Avoid 10:00 to early afternoon, when the tour groups are there: come right at opening or after 14:00. Best in rain or just after.",
      "favPhoto": [
        "sanzenin",
        0
      ],
      "whoHead": "Know before you go",
      "who": [
        "Kyoto Bus both ways: 40–50 minutes from Sanjo-Keihan-mae, ¥570. Crowded and late on autumn weekends",
        "Lunch places here close early. Sitting down at about 11:30 is easiest; have dinner back in the city",
        "The last bus straight to Sanjo-Keihan-mae leaves at 17:47. The last bus of all is at 21:01 (to Kokusaikaikan station, then subway)",
        "Bring cash for entry fees: Sanzen-in ¥700 + Hosen-in ¥1,000 + Jikko-in ¥600 + Jakko-in ¥600",
        "Jikko-in’s last entry is 15:30. Sanzen-in closes at 16:45 in November, 16:30 Dec–Feb",
        "Sanzen-in and Jakko-in are on opposite sides of the valley, about 35 minutes’ walk apart. Wear comfortable shoes",
        "It’s cooler than central Kyoto: bring an extra layer in autumn and winter"
      ],
      "dayHead": "One day, roughly like this (leaving at 9–10)",
      "from": "From",
      "day": [
        {
          "time": "9:48",
          "area": "Ohara bus stop → Jakko-in",
          "title": "Quiet Jakko-in first",
          "text": "Take the 9:07 bus from Sanjo-Keihan-mae. From the stop head west, without crossing the main road, and walk 20 minutes between the fields to Jakko-in. (Photo: PlusMinus / CC BY-SA 3.0)",
          "photo": [
            "jakkoin",
            0
          ]
        },
        {
          "time": "11:15",
          "area": "Valley lane & the approach",
          "title": "Early lunch at 11:30",
          "text": "Walk back along the lane and up the approach, and have lunch around Sanzen-in’s gate before the midday rush.",
          "photo": [
            "sando",
            0
          ]
        },
        {
          "time": "12:40",
          "area": "Hosen-in, Jikko-in, Sanzen-in",
          "title": "Matcha at the framed garden, Sanzen-in after 14:00",
          "text": "Matcha in Hosen-in’s framed garden, a walk in Jikko-in’s garden, then Sanzen-in as the tour groups start to leave: the moss garden, Ojo Gokuraku-in and the little Jizo.",
          "photo": [
            "sanzenin",
            5
          ]
        },
        {
          "time": "16:27",
          "area": "Back → Sanjo & Pontocho",
          "title": "Bus to Sanjo, dinner in town",
          "text": "Buy pickles on the lane and catch the 16:27 bus. From Sanjo-Keihan-mae, cross Sanjo Ohashi bridge to Pontocho and Kiyamachi; the evening can run to 21:00–22:00.",
          "note": "Ohara 16:27 → Sanjo-Keihan-mae 17:10. Last direct bus 17:47",
          "photo": [
            "kaeri",
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "A return by bus from Sanjo-Keihan-mae is ¥1,140. The Subway & Bus 1-day Pass (¥1,100) is slightly cheaper and also covers the subway and city buses in the evening. Entry fees are extra: ¥2,900 for everything (not counting Raigo-in).",
      "deals": [
        {
          "name": "Kyoto Bus 17",
          "price": "¥570",
          "text": "Sanjo-Keihan-mae → Ohara, 40–50 minutes. ¥590 from Shijo-Kawaramachi, ¥490 from Demachiyanagi-ekimae. The same going back.",
          "url": "https://www.kyotobus.jp/route/timetable/"
        },
        {
          "name": "Subway & Bus 1-day Pass",
          "price": "¥1,100",
          "text": "Valid on Kyoto Bus as far as the Ohara stop. Not sold on Kyoto Bus: buy it first from a subway ticket machine.",
          "url": "https://www.kyotobus.jp/route/fare/discount/pass/post-3.html"
        },
        {
          "name": "Sanzen-in",
          "price": "¥700",
          "text": "9:00–17:00 (Nov 8:45–16:45, Dec–Feb 9:00–16:30). Open every day.",
          "url": "https://www.sanzenin.or.jp/guide/"
        },
        {
          "name": "Hosen-in",
          "price": "¥1,000",
          "text": "Matcha and a sweet included. 9:00–17:00 (last entry 16:30).",
          "url": "http://www.hosenin.net/haikan/"
        },
        {
          "name": "Jakko-in",
          "price": "¥600",
          "text": "9:00–17:00 (until 16:30 Dec–Feb).",
          "url": "https://www.jakkoin.jp/haikan/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on 21–22 November 2026 (Kyoto Bus’s official timetable, each temple’s website, a route planner). Jikko-in is ¥600 (¥1,100 with matcha).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose your start time",
          "text": "The buttons above the list switch between “Sanzen-in at opening” (the 7:57 from Sanjo-Keihan-mae) and “Leave at 9–10” (the 9:07). The order and times change."
        },
        {
          "title": "Follow the numbers",
          "text": "Stops 1 to 9 in order make the day as timed. Tap a number for photos, notes, fees and the suggested time."
        },
        {
          "title": "Drop what you’ll skip",
          "text": "A set that fits one day comfortably is chosen to begin with. Tap “Want to go” to add side trips such as the Otonashi falls."
        },
        {
          "title": "Directions in Google Maps",
          "text": "Each stop has an “Open in Google Maps” button for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi (Hosen-in, Jikko-in, Raigo-in and the falls, and Jakko-in are introduced from official websites and other sources, with photos from Wikimedia Commons)."
    },
    introFor: {
      early: {
        "lead": "Walk into Sanzen-in just after it opens, before the tour groups. After the moss garden, rest over matcha at Hosen-in. Have an early lunch at 11:30, walk between the fields to Jakko-in in the afternoon and take the 14:27 bus back. You are at Sanjo soon after 15:00: rest at your hotel, then head for Pontocho and Kiyamachi in the evening. The bus out leaves Sanjo-Keihan-mae at 7:57. My photos are from a rainy late afternoon in November 2024.",
        "favText": "Opens at 8:45 in November and 9:00 in other months. Arrive for opening and you can sit on the veranda before the tour groups build up. Best in rain or just after.",
        "dayHead": "One day, roughly like this (Sanzen-in at opening)",
        "day": [
          {
            "time": "8:38",
            "area": "The approach & Sanzen-in",
            "title": "Sanzen-in, just opened",
            "text": "Take the 7:57 bus from Sanjo-Keihan-mae (it arrives at 8:49 on weekends and holidays). Walk up the lane by the stream to reach Sanzen-in at about 9:00: the guest-hall garden, the moss garden, Ojo Gokuraku-in and the little Jizo.",
            "photo": [
              "sanzenin",
              5
            ]
          },
          {
            "time": "10:25",
            "area": "Hosen-in",
            "title": "A rest over matcha at the framed garden",
            "text": "A break after the morning’s walking. Sit on the tatami and look at the garden framed by the pillars. (Photo: Maechan0360 / CC BY-SA 3.0)",
            "photo": [
              "hosenin",
              0
            ]
          },
          {
            "time": "11:30",
            "area": "Lunch, valley lane, Jakko-in",
            "title": "Early lunch, then across the valley",
            "text": "Lunch at Sanzen-in’s gate or on the lane, before the rush. Walk down the lane and between the fields to Jakko-in. (Photo: PlusMinus / CC BY-SA 3.0)",
            "photo": [
              "jakkoin",
              0
            ]
          },
          {
            "time": "14:27",
            "area": "Back → Sanjo & Pontocho",
            "title": "At Sanjo soon after 15:00; evening in town",
            "text": "After an early start, rest at your hotel. If you still have energy, get off at Demachiyanagi-ekimae for the Kamo delta. Dinner around Pontocho and Kiyamachi from about 18:00.",
            "note": "Ohara 14:27 → Demachiyanagi-ekimae 15:01, Sanjo-Keihan-mae 15:10",
            "photo": [
              "kaeri",
              0
            ]
          }
        ]
      }
    }
  }
};
