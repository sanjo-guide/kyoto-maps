/* Page texts in Japanese and English.
   Toshi 個人のマップ。三条から地下鉄とJRバスで高雄へ。コースは2つ（神護寺の開門に合わせる／9〜10時に出発）。
   intro は「9〜10時に出発」の内容で、introFor.early が app.js で上書きされる（scripts/sync_takao.py）。
   （高山寺はオーナーが行っていない場所。写真は Wikimedia Commons）。
   Photos are [spot id, photo index] from data/routes/takao.json（コースで番号が変わるので id で指定）。
   時刻・料金は2026年11月22日に確認（JRバスと京都市交通局の時刻表、各寺の公式サイト、高雄保勝会、乗換案内）。 */
window.TAKAO_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 高雄の紅葉 Takao MAP',
    titleMain: '高雄の紅葉',
    titleSub: 'Autumn in Takao',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '上のボタンで出発時間を選ぶと、回る順番と時間が変わります。開門に合わせるコースは神護寺が先、9〜10時発のコースは栂ノ尾の高山寺から谷を下って、神護寺は午後です。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（高山寺の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: 'バス・電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや時刻表で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。1か所だけの日の帰り方は、各スポットの「あなたのルートでは」に出ます。',
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "神護寺の開門に合わせる\n二条駅前 7:36発",
    courseLate: "9〜10時に出発\n高山寺から谷を下る",
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
      "h1": "もみじの長い石段を上って、神護寺へ。清滝川の谷に並ぶ、3つの山寺を歩く1日。",
      "lead": "朱の橋を渡る西明寺、縁側に座る高山寺の石水院、長い石段の上の神護寺。高雄（たかお）・槇尾（まきのお）・栂尾（とがのお）の「三尾（さんび）」は、京都の北西の山あいにあります。三条から地下鉄で二条へ出て、JRバスで約40分。9〜10時に出る日は、バスの終点の栂ノ尾まで乗って高山寺から歩き始め、門前の茶屋で早めのお昼。川沿いに西明寺、高雄橋を渡って、午後に神護寺の石段を上ります。15時台のバスで戻り、12月6日までは北野天満宮のもみじ苑に寄り道も。朝早く出られる人は、上のボタンで「神護寺の開門に合わせる」コースに切り替えてください。写真は2024年11月19日に撮ったものです（高山寺は Wikimedia Commons）。",
      "favLabel": "いちばんの見どころ",
      "favName": "神護寺",
      "favText": "もみじに囲まれた長い石段と、楼門の先の広い境内。16時に閉まるので、このコースでは14時すぎに。",
      "favPhoto": [
        "jingoji",
        1
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "三条から地下鉄東西線で二条へ（6〜8分・220円）、二条駅前からJRバス（230円）。JRバスは三条を通りません",
        "紅葉の週末はバスが混みます。座って行きたい人は、始発の京都駅前から",
        "お昼の店は谷の茶屋だけ。11時半ごろに入ると楽です。高雄は日が暮れると店が閉まります",
        "神護寺は9:00〜16:00。高雄バス停から石段を上って約20分。歩きやすい靴で",
        "拝観料：神護寺1,000円、西明寺700円、高山寺の石水院1,000円（秋は入山料500円が別に）",
        "帰りのJRバスの最終は高雄20:06発。市バス8系統の四条烏丸行きは20:16発が最後",
        "山あいなので、上着を1枚多く"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "from": "",
      "day": [
        {
          "time": "10:26",
          "area": "栂尾",
          "title": "終点の栂ノ尾から、高山寺へ",
          "text": "二条駅前9:46発のJRバスで終点へ。石水院の縁側に座って、門前の茶屋で11時半前に早めのお昼。（写真：663highland / CC BY 2.5）",
          "photo": [
            "kosanji",
            0
          ]
        },
        {
          "time": "12:30",
          "area": "槇尾",
          "title": "指月橋を渡って西明寺",
          "text": "国道を歩いて15分。朱の橋と、表門ごしの本堂。",
          "photo": [
            "saimyoji",
            0
          ]
        },
        {
          "time": "13:35",
          "area": "高雄",
          "title": "高雄橋から、神護寺の石段へ",
          "text": "川沿いの道を下って高雄橋へ。もみじの石段を上って、14時すぎに神護寺。16時に閉まります。",
          "photo": [
            "jingoji",
            0
          ]
        },
        {
          "time": "15:36",
          "area": "帰り → 北野・三条",
          "title": "バスで戻って、夜は街なかで",
          "text": "12月6日までは北野白梅町で降りて北野天満宮のもみじ苑へ（夜はライトアップ）。そのまま二条駅前まで乗れば、地下鉄で三条へ。晩ごはんは先斗町・木屋町で、21〜22時ごろまで。",
          "note": "高雄15:36発 → 北野白梅町16:03着・二条駅前16:15着",
          "photo": [
            "kiyotaki",
            2
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と拝観料のめやす",
      "dealsLead": "三条から地下鉄東西線（京都市役所前・三条京阪〜二条、220円）とJRバスで往復すると900円。寄り道でバスに乗る回数が増えるなら、地下鉄・バス1日券（1,100円。JRバスは京都駅前〜栂ノ尾で使えます）も。拝観料は別で、3つのお寺を回ると秋は3,200円です。",
      "deals": [
        {
          "name": "JRバス 高雄・京北線",
          "price": "230円",
          "text": "京都駅前〜栂ノ尾は230円均一。二条駅前9:46発→栂ノ尾10:26着。帰りの最終は高雄20:06発。",
          "url": "https://www.nishinihonjrbus.co.jp/route/kyoto/"
        },
        {
          "name": "神護寺",
          "price": "1,000円",
          "text": "9:00〜16:00、年中無休（中学生以上。2024年7月から）。",
          "url": "http://jingoji.or.jp/"
        },
        {
          "name": "西明寺",
          "price": "700円",
          "text": "9:00〜17:00（受付は16:30まで）。中・高生500円。",
          "url": "https://www.saimyoji.or.jp/"
        },
        {
          "name": "高山寺",
          "price": "1,000円（秋は＋500円）",
          "text": "石水院1,000円。秋（2026年は12月上旬まで）は入山料500円が別に。8:30〜17:00。",
          "url": "https://kosanji.com/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日に確認しました（JRバスと京都市交通局の時刻表・運賃表、各寺の公式サイト、乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「神護寺の開門に合わせる」（二条駅前7:36発）と「9〜10時に出発」（9:46発）を切り替えます。回る順番と時間が変わります。"
        },
        {
          "title": "番号の順に",
          "text": "1から4の順に回ると、時間割どおりの1日になります。最後のスポットに、帰りのバス、寄り道、街なかの夜を書いています。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "「選んで回る」に切り替えると、行きたい場所だけを選べます。外したときの帰り方も出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです（高山寺は、公式サイトの情報と Wikimedia Commons の写真で紹介しています）。"
    },
    introFor: {
      early: {
        "lead": "茶屋が開く前の高雄橋を渡って、9時の開門と同時に神護寺へ。人が増える前に、金堂の石段の上から境内を見下ろします。石段の茶屋でもみじ餅とお抹茶のひと休み。川沿いに西明寺へ歩いて、槇ノ尾で12時前にお昼。午後は高山寺の石水院に座って、14:34のバスで戻ります。帰りに仁和寺や北野天満宮へ寄っても、夜は街なかでゆっくりできます。行きは朝7:36に二条駅前を出るJRバスです。写真は2024年11月19日に撮ったものです（高山寺は Wikimedia Commons）。",
        "favText": "9:00の開門に合わせて行くと、人が増える前に金堂の石段の上から境内を見下ろせます。",
        "dayHead": "1日の流れ（神護寺の開門に合わせる）",
        "day": [
          {
            "time": "8:14",
            "area": "高雄",
            "title": "朝の高雄橋から、開門の神護寺へ",
            "text": "二条駅前7:36発のJRバスで高雄へ。朝ごはんは出る前に。高雄橋を渡り、石段を上って9時に神護寺。",
            "photo": [
              "jingoji",
              1
            ]
          },
          {
            "time": "10:15",
            "area": "高雄 → 槇尾",
            "title": "茶屋でひと休みして、西明寺",
            "text": "石段の茶屋でもみじ餅とお抹茶。清滝川沿いを歩いて西明寺へ。12時前に槇ノ尾でお昼。",
            "photo": [
              "saimyoji",
              0
            ]
          },
          {
            "time": "12:55",
            "area": "栂尾",
            "title": "高山寺の石水院",
            "text": "縁側から一歩下がって畳に座ると、柱が額縁になります。帰りは栂ノ尾で始まる14:34のバスで。（写真：663highland / CC BY 2.5）",
            "photo": [
              "kosanji",
              0
            ]
          },
          {
            "time": "14:34",
            "area": "帰り → 仁和寺・北野・三条",
            "title": "寄り道してから、夜は街なかで",
            "text": "御室仁和寺14:52着で仁和寺へ。12月6日までは嵐電で北野白梅町へ出て、北野天満宮のもみじ苑も。まっすぐ帰るなら二条駅前15:15着。晩ごはんは先斗町・木屋町で。",
            "note": "栂ノ尾14:34発 → 御室仁和寺14:52着・二条駅前15:15着",
            "photo": [
              "kiyotaki",
              2
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kyoto: Autumn in Takao MAP',
    titleMain: 'Autumn in Takao',
    titleSub: '高雄の紅葉',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Choose your start time with the buttons above: the order and the times change. The opening course does Jingoji first; the 9–10 course starts at Kosanji in Toganoo, works down the valley and leaves Jingoji for the afternoon. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (the Kosanji photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Bus & train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and timetables on {d}. Details can change, so please check before you go.',
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
    pickNote: 'Tap “Want to go” on the places you like. Times are for the full route. If you pick only one place, “On your route” at that spot tells you how to get back.',
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "Jingoji at opening\n7:36 from Nijo",
    courseLate: "Leave at 9–10\nKosanji first, downhill",
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
      "h1": "Up the long maple-lined stairway to Jingoji: a day walking three mountain temples in the Kiyotaki valley.",
      "lead": "Saimyoji over a vermilion bridge, Kosanji’s Sekisuiin where you sit on the veranda, and Jingoji at the top of its long stairway. Takao, Makinoo and Toganoo, the “three o’s” of north-west Kyoto, are about 40 minutes from Sanjo: the subway to Nijo, then the JR Bus. Leaving at 9–10, ride to Toganoo at the end of the line, start at Kosanji and have an early lunch at a teahouse by its gate. Follow the river to Saimyoji, cross the Takao bridge and climb to Jingoji in the afternoon. Head back on a bus in the 15:00 hour; until 6 December you can stop at Kitano Tenmangu’s maple garden. If you can start early, switch to the “Jingoji at opening” course with the buttons above. My photos were taken on 19 November 2024 (Kosanji’s are from Wikimedia Commons).",
      "favLabel": "Highlight",
      "favName": "Jingoji",
      "favText": "The long maple-lined stairway and the wide precinct beyond the gate. It closes at 16:00; on this course you arrive just after 14:00.",
      "favPhoto": [
        "jingoji",
        1
      ],
      "whoHead": "Good to know before you go",
      "who": [
        "Tozai subway from Sanjo to Nijo (6–8 min, ¥220), then JR Bus from Nijo-eki-mae (¥230). JR Bus doesn’t run through Sanjo",
        "Buses are crowded on autumn weekends. For a seat, board at the first stop, Kyoto Station",
        "Lunch means the valley’s teahouses. Around 11:30 is easiest. Takao shuts down after dark",
        "Jingoji is open 9:00–16:00, about 20 minutes up the steps from the Takao stop. Wear comfortable shoes",
        "Entry: Jingoji ¥1,000, Saimyoji ¥700, Kosanji’s Sekisuiin ¥1,000 (plus ¥500 in autumn)",
        "Last JR Bus back leaves Takao at 20:06; the last city bus 8 to Shijo-Karasuma at 20:16",
        "It’s a mountain valley: bring an extra layer"
      ],
      "dayHead": "One day, roughly like this (leaving at 9–10)",
      "from": "From",
      "day": [
        {
          "time": "10:26",
          "area": "Toganoo",
          "title": "From the end of the line to Kosanji",
          "text": "The 9:46 JR Bus from Nijo-eki-mae to the last stop. Sit on Sekisuiin’s veranda, then an early lunch at a teahouse by the gate before 11:30. (Photo: 663highland / CC BY 2.5)",
          "photo": [
            "kosanji",
            0
          ]
        },
        {
          "time": "12:30",
          "area": "Makinoo",
          "title": "Across the Shigetsu bridge to Saimyoji",
          "text": "15 minutes down the road. The red bridge, and the main hall framed by the gate.",
          "photo": [
            "saimyoji",
            0
          ]
        },
        {
          "time": "13:35",
          "area": "Takao",
          "title": "From Takao bridge up to Jingoji",
          "text": "Follow the river down to Takao bridge and climb the maple stairs to reach Jingoji just after 14:00. It closes at 16:00.",
          "photo": [
            "jingoji",
            0
          ]
        },
        {
          "time": "15:36",
          "area": "Back → Kitano, Sanjo",
          "title": "Back by bus, evening in town",
          "text": "Until 6 December, get off at Kitano-Hakubaicho for Kitano Tenmangu’s maple garden (lit up after dark). Or ride on to Nijo-eki-mae and take the subway to Sanjo. Dinner in Pontocho or Kiyamachi, until 21:00 or 22:00.",
          "note": "Takao 15:36 → Kitano-Hakubaicho 16:03, Nijo-eki-mae 16:15",
          "photo": [
            "kiyotaki",
            2
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and entry fees",
      "dealsLead": "A return trip from Sanjo by the Tozai subway (to Nijo, ¥220) and JR Bus is ¥900. If side trips add more bus rides, the Subway & Bus 1-day Pass (¥1,100; valid on JR Bus between Kyoto Station and Toganoo) may pay off. Temple entry is extra: ¥3,200 for all three in autumn.",
      "deals": [
        {
          "name": "JR Bus Takao–Keihoku line",
          "price": "¥230",
          "text": "Flat ¥230 from Kyoto Station to Toganoo. Nijo-eki-mae 9:46 → Toganoo 10:26. Last bus back leaves Takao at 20:06.",
          "url": "https://www.nishinihonjrbus.co.jp/route/kyoto/"
        },
        {
          "name": "Jingoji",
          "price": "¥1,000",
          "text": "9:00–16:00, open daily (junior high and up; since July 2024).",
          "url": "http://jingoji.or.jp/"
        },
        {
          "name": "Saimyoji",
          "price": "¥700",
          "text": "9:00–17:00 (last entry 16:30). Junior high and high school ¥500.",
          "url": "https://www.saimyoji.or.jp/"
        },
        {
          "name": "Kosanji",
          "price": "¥1,000 (+¥500 in autumn)",
          "text": "Sekisuiin ¥1,000. In autumn (until early December in 2026) a separate ¥500 entry fee. 8:30–17:00.",
          "url": "https://kosanji.com/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 22, 2026 (JR Bus and Kyoto City bus timetables and fare tables, temple websites, a route planner).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick a start time",
          "text": "Use the buttons above the list to switch between “Jingoji at opening” (7:36 from Nijo-eki-mae) and “Leave at 9–10” (9:46). The order and times change."
        },
        {
          "title": "In number order",
          "text": "Follow 1 to 4 for the day as timed. The last spot covers the bus back, stops on the way home and the evening in town."
        },
        {
          "title": "Skip what you like",
          "text": "Switch to “Choose stops” to pick only the places you want; it also tells you how to get back."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi (Kosanji is introduced from its official website, with photos from Wikimedia Commons)."
    },
    introFor: {
      early: {
        "lead": "Cross the Takao bridge before the teahouses open and walk into Jingoji as it opens at 9:00, then look down over the precinct from the top of the main hall’s steps before it fills up. Rest with momiji-mochi and matcha at a teahouse on the steps, walk along the river to Saimyoji and have lunch at Makinoo before noon. In the afternoon sit at Kosanji’s Sekisuiin, then take the 14:34 bus back. Stop at Ninna-ji or Kitano Tenmangu on the way and still have an easy evening in town. The bus out is the 7:36 JR Bus from Nijo-eki-mae. My photos were taken on 19 November 2024 (Kosanji’s are from Wikimedia Commons).",
        "favText": "Arrive for the 9:00 opening and you can look down over the precinct from the top of the main hall’s steps before it fills up.",
        "dayHead": "One day, roughly like this (Jingoji at opening)",
        "day": [
          {
            "time": "8:14",
            "area": "Takao",
            "title": "Takao bridge in the morning, Jingoji at opening",
            "text": "The 7:36 JR Bus from Nijo-eki-mae to Takao. Have breakfast before you go. Cross the bridge and climb the steps to be at Jingoji at 9:00.",
            "photo": [
              "jingoji",
              1
            ]
          },
          {
            "time": "10:15",
            "area": "Takao → Makinoo",
            "title": "A teahouse break, then Saimyoji",
            "text": "Momiji-mochi and matcha at a teahouse on the steps, then along the river to Saimyoji. Lunch at Makinoo before noon.",
            "photo": [
              "saimyoji",
              0
            ]
          },
          {
            "time": "12:55",
            "area": "Toganoo",
            "title": "Sekisuiin at Kosanji",
            "text": "Sit on the tatami a step back from the veranda and the pillars frame the view. Go back on the 14:34, which starts at Toganoo. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "kosanji",
              0
            ]
          },
          {
            "time": "14:34",
            "area": "Back → Ninna-ji, Kitano, Sanjo",
            "title": "A stop on the way, then the evening in town",
            "text": "Omuro-Ninnaji at 14:52 for Ninna-ji. Until 6 December, take the Randen tram to Kitano-Hakubaicho for Kitano Tenmangu’s maple garden too. Straight back, you reach Nijo-eki-mae at 15:15. Dinner in Pontocho or Kiyamachi.",
            "note": "Toganoo 14:34 → Omuro-Ninnaji 14:52, Nijo-eki-mae 15:15",
            "photo": [
              "kiyotaki",
              2
            ]
          }
        ]
      }
    }
  }
};
