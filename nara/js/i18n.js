/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都（三条のあたり）・大阪（梅田〜難波のあたり）から近鉄で奈良へ。コースは2つ：
   「9〜10時に出発」（data/routes/nara.json）と「早朝に出発」（nara-early.json。大仏殿の開門に合わせる）。
   intro は「9〜10時に出発」の内容で、introFor.early が app.js で上書きされる（scripts/sync_nara.py）。
   Photos are [spot id, photo index]（コースで番号が変わるので id で指定）.
   時刻・料金は2026年11月21〜22日に確認（各施設の公式サイト・奈良県・奈良市、電車は乗換案内）。文章は scripts/build_nara_data.py と合わせること */
window.NARA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都・大阪から日帰り 奈良 Nara MAP',
    titleMain: '奈良',
    titleSub: 'Nara',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '上のボタンで出発時間を選ぶと、回る順番と時間が変わります。時間割どおりに1日で回れる6か所が最初から選んであります。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（借りた写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    bus: 'バス',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '最初は、時間割どおりに回れる6か所（東大寺・二月堂・春日大社・ならまち・春鹿・興福寺）が選んであります。行かない所は外し、気になる所は「行きたい」を押して足してください。時間はこの6か所を回る場合の目安です。',
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
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "早朝に出発\n大仏殿の開門へ",
    courseLate: "9〜10時に出発\n大仏殿は夕方",
    swMode: "回り方",
    intro: {
      "kicker": "京都・大阪から近鉄で。歩いて回る1日",
      "h1": "昼の大仏殿は避ける。朝いちばんか、夕方に。",
      "lead": "9〜10時に出る日は、先にならまちへ。早めのお昼と酒蔵「春鹿」のきき酒のあと、春日大社を通って、昼の団体が減る15時半すぎに大仏殿へ。二月堂の舞台で夕暮れを見て、奈良で晩ごはんを食べて帰ります。朝6時台の電車に乗れる人は、一覧の上のボタンで「早朝に出発」に切り替えてください。大仏殿の開門に合わせた時間割になります。",
      "favLabel": "いちばんの見どころ",
      "favName": "東大寺 大仏殿",
      "favText": "昼を外して、15時半すぎに。11〜3月は17:00に閉まるので、16:00までに入ります。",
      "favPhoto": [
        "todaiji",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "京都からは地下鉄の烏丸御池駅から約1時間・1,020円（乗り換えなしの急行もあります）。京阪の三条駅からは丹波橋で乗り換えて1,000円",
        "大阪からは大阪難波駅から近鉄の快速急行で35〜40分・680円（梅田からは地下鉄を足して920円）",
        "歩くのは全部で9〜10km。坂と砂利道があるので歩きやすい靴で",
        "東大寺・興福寺・法隆寺の拝観料は現金だけ。千円札と小銭を",
        "興福寺の五重塔は修理中で、覆いの中。外からは見えません（2030年代前半まで）",
        "鹿せんべいは買ったらすぐあげる。なくなったら両手を開いて見せる",
        "火曜は春鹿と依水園が休み。月曜は格子の家と平城宮跡の建物が休み",
        "春日大社の特別参拝は、毎月1・11・21日の午前と、12月20日〜1月7日は入れません",
        "11〜3月は大仏殿が17:00まで。若草山は冬（12月中旬〜3月中旬）は入れません"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "from": "",
      "day": [
        {
          "time": "10:18",
          "area": "興福寺",
          "title": "駅から5分、国宝館の阿修羅像",
          "text": "烏丸御池9:21発の急行（大阪難波からは9:34発の快速急行）で近鉄奈良へ。坂を上って興福寺の国宝館を見たら、猿沢池を通ってならまちへ下ります。",
          "photo": [
            "kofukuji",
            0
          ]
        },
        {
          "time": "11:30",
          "area": "ならまち・春鹿",
          "title": "早めのお昼と、酒蔵のきき酒",
          "text": "店が開いたばかりの時間にお昼。元興寺と格子の家を見て、13時すぎに春鹿で5種類のきき酒（700円）。",
          "photo": [
            "harushika",
            0
          ]
        },
        {
          "time": "14:10",
          "area": "飛火野・春日大社",
          "title": "静かな芝生の鹿と、森の中の灯籠",
          "text": "春鹿から歩いて15分の飛火野で鹿せんべい。石灯籠の参道を上って春日大社へ。特別参拝は16:00までです。",
          "photo": [
            "kasuga",
            0
          ]
        },
        {
          "time": "15:40",
          "area": "東大寺・二月堂",
          "title": "夕方の大仏殿から、夕暮れの二月堂へ",
          "text": "南大門の仁王像を見上げて大仏殿へ。坂を上った二月堂の舞台から、暮れていく奈良の町を見下ろします。歩いて駅のまわりかならまちへ戻って晩ごはん。",
          "note": "近鉄奈良19:46発 → 烏丸御池20:43着（大阪難波へは19:52発 → 20:28着）",
          "photo": [
            "nigatsudo",
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と拝観料のめやす",
      "dealsLead": "電車は京都（烏丸御池）から往復2,040円、大阪難波から往復1,360円。拝観料は国宝館900円＋大仏殿800円＋春日大社の特別参拝700円で2,400円、春鹿のきき酒が700円。お参りや二月堂、鹿、ならまち歩きは無料です。ほかに食事代。",
      "deals": [
        {
          "name": "地下鉄・近鉄（烏丸御池⇔近鉄奈良）",
          "price": "片道1,020円",
          "text": "竹田駅で乗り換え（乗り換えなしの急行もあります）。京都駅から近鉄に乗れば980円で、特急は＋520円。特急券はネットのチケットレスでも買えます。",
          "url": "https://www.kintetsu.co.jp/gyoumu/ticket/"
        },
        {
          "name": "近鉄（大阪難波⇔近鉄奈良）",
          "price": "片道680円",
          "text": "快速急行で35〜40分、乗り換えなし。梅田からは御堂筋線でなんばへ（240円）。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "東大寺 大仏殿",
          "price": "800円",
          "text": "東大寺ミュージアムとのセット券は1,200円。現金のみ。",
          "url": "https://www.todaiji.or.jp/information/haikan/"
        },
        {
          "name": "春鹿のきき酒",
          "price": "700円",
          "text": "5種類を1杯ずつ。受付は10:00〜16:30、火曜休み。20歳から。",
          "url": "https://www.harushika.com/visit-brewery/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21〜22日に確認しました（各施設の公式サイト、電車は乗換案内・11月28日土曜のダイヤ）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「早朝に出発」（大仏殿の開門へ）か「9〜10時に出発」（大仏殿は夕方）を選びます。回る順番と時間が変わります。"
        },
        {
          "title": "6か所が選んであります",
          "text": "時間割どおりに1日で回れる6か所です。行かない所は外し、庭園・若草山・平城宮跡・法隆寺は「行きたい」を押すと足せます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・時間・おすすめの時間が見られます。行き帰りの電車は1番の近鉄奈良駅に。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです。借りた写真には撮影者の名前を載せています。"
    },
    // 早朝に出発（early）のときに intro を上書きする項目（scripts/sync_nara.py の差分）
    introFor: {
      early: {
        "lead": "朝6時台の電車で奈良へ。まだ人の少ない奈良公園を歩いて、開門と同時に大仏殿に入ります。二月堂、春日大社と回って、10時半に開く春日大社の茶屋で朝ごはん。昼はならまちと酒蔵「春鹿」、最後に興福寺の国宝館を見て、16時前の電車で帰ります。",
        "favText": "11〜3月は8:00、4〜10月は7:30に開きます。開門に合わせて行くと、団体が増える前に見られます。",
        "dayHead": "1日の流れ（早朝に出発・11〜3月）",
        "day": [
          {
            "time": "7:22",
            "area": "奈良公園・東大寺・二月堂",
            "title": "8:00の開門に合わせて大仏殿へ",
            "text": "烏丸御池6:24発（大阪難波からは6:37発）で近鉄奈良へ。鹿のいる公園を歩いて南大門、8:00に大仏殿。そのあと坂を上って二月堂の舞台へ。4〜10月は7:30開門なので、1本早い電車で。",
            "photo": [
              "todaiji",
              0
            ]
          },
          {
            "time": "9:50",
            "area": "春日大社",
            "title": "お参りのあと、茶屋で朝ごはん",
            "text": "若草山のふもとを歩いて春日大社へ。参道の春日荷茶屋は10:30に開きます。万葉粥で朝ごはんと休憩。",
            "photo": [
              "kasuga",
              0
            ]
          },
          {
            "time": "11:40",
            "area": "ならまち・春鹿",
            "title": "町家の町と、酒蔵のきき酒",
            "text": "飛火野の芝生の横を通ってならまちへ。元興寺と格子の家を見て軽くお昼、13時すぎに春鹿で5種類のきき酒（700円）。",
            "photo": [
              "harushika",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "興福寺 → 帰り",
            "title": "最後に国宝館の阿修羅像",
            "text": "猿沢池の横の石段を上って興福寺へ。国宝館を見たら、駅まで歩いて7分です。元気な人は依水園か、帰りに平城宮跡へ。",
            "note": "近鉄奈良15:45発 → 烏丸御池16:44着（大阪難波へは15:36発 → 16:16着）",
            "photo": [
              "kofukuji",
              0
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto or Osaka: Nara MAP',
    titleMain: 'Nara',
    titleSub: '奈良',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Choose your start time with the buttons above: the order and the times change. The six stops that fit the timetable in one day are chosen to begin with. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (borrowed photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    bus: 'Bus',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
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
    pickNote: 'The six stops that fit the timetable (Todaiji, Nigatsudo, Kasuga Taisha, Naramachi, Harushika, Kofukuji) are chosen to begin with. Drop what you’ll skip and tap “Want to go” to add others. Times are for these six stops.',
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
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "Early start\nGreat Buddha at opening",
    courseLate: "Leave at 9–10\nGreat Buddha late",
    swMode: "Stops",
    intro: {
      "kicker": "From Kyoto or Osaka by Kintetsu: a day on foot",
      "h1": "Skip the Great Buddha at midday. Go first thing, or late.",
      "lead": "Leaving at 9–10, go to Naramachi first. After an early lunch and a sake tasting at the Harushika brewery, walk through Kasuga Taisha and reach the Great Buddha Hall after 15:30, when the midday tour groups have thinned out. Watch dusk from the balcony of Nigatsudo, have dinner in Nara, then go home. If you can catch a train soon after 6:00, switch to “Early start” with the buttons above the list: that timetable is built around the opening of the Great Buddha Hall.",
      "favLabel": "Highlight",
      "favName": "Todaiji: Great Buddha Hall",
      "favText": "Avoid midday and go after 15:30. From November to March it closes at 17:00, so be inside by 16:00.",
      "favPhoto": [
        "todaiji",
        0
      ],
      "whoHead": "Know before you go",
      "who": [
        "From Kyoto: about 1 hour from Karasuma Oike subway station, ¥1,020 (some expresses run straight through). From Keihan Sanjo, change at Tambabashi: ¥1,000",
        "From Osaka: 35–40 minutes from Osaka-Namba by Kintetsu rapid express, ¥680 (¥920 from Umeda, with the subway)",
        "9–10 km of walking in all, with slopes and gravel. Wear comfortable shoes",
        "Todaiji, Kofukuji and Horyuji take cash only. Bring ¥1,000 notes and coins",
        "Kofukuji’s five-storied pagoda is under repair inside a cover and can’t be seen (until the early 2030s)",
        "Hand deer crackers over as soon as you buy them; show both open hands when they’re gone",
        "On Tuesdays Harushika and Isuien are closed; on Mondays Koshi-no-Ie and the Heijo Palace buildings",
        "Kasuga Taisha’s paid inner area is closed on the mornings of the 1st, 11th and 21st, and from 20 December to 7 January",
        "From November to March the Great Buddha Hall closes at 17:00. Mt. Wakakusa is shut in winter (mid-December to mid-March)"
      ],
      "dayHead": "One day, leaving at 9–10",
      "from": "From",
      "day": [
        {
          "time": "10:18",
          "area": "Kofukuji",
          "title": "Five minutes from the station: the Ashura statue",
          "text": "Take the 9:21 express from Karasuma Oike (from Osaka-Namba, the 9:34 rapid express) to Kintetsu-Nara. Walk up to Kofukuji’s National Treasure Hall, then down past Sarusawa Pond to Naramachi.",
          "photo": [
            "kofukuji",
            0
          ]
        },
        {
          "time": "11:30",
          "area": "Naramachi & Harushika",
          "title": "An early lunch, then a sake tasting",
          "text": "Lunch just as the restaurants open. See Gangoji and Koshi-no-Ie, then soon after 13:00 taste five sakes at Harushika (¥700).",
          "photo": [
            "harushika",
            0
          ]
        },
        {
          "time": "14:10",
          "area": "Tobihino & Kasuga Taisha",
          "title": "Deer on a quiet lawn, lanterns in the forest",
          "text": "Feed the deer on the Tobihino lawn, 15 minutes’ walk from Harushika, then climb the lantern-lined approach to Kasuga Taisha. The inner area is open until 16:00.",
          "photo": [
            "kasuga",
            0
          ]
        },
        {
          "time": "15:40",
          "area": "Todaiji & Nigatsudo",
          "title": "The Great Buddha late in the day, then dusk at Nigatsudo",
          "text": "Look up at the guardians in the Great South Gate and enter the Great Buddha Hall. Climb to Nigatsudo’s balcony and watch the town below as the light goes. Walk back to the station area or Naramachi for dinner.",
          "note": "Kintetsu-Nara 19:46 → Karasuma Oike 20:43 (for Osaka-Namba: 19:52 → 20:28)",
          "photo": [
            "nigatsudo",
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and admission",
      "dealsLead": "Trains: ¥2,040 return from Kyoto (Karasuma Oike), ¥1,360 return from Osaka-Namba. Admission: National Treasure Hall ¥900 + Great Buddha Hall ¥800 + Kasuga Taisha inner area ¥700 = ¥2,400, plus ¥700 for the Harushika tasting. Praying, Nigatsudo, the deer and Naramachi are free. Meals are extra.",
      "deals": [
        {
          "name": "Subway + Kintetsu (Karasuma Oike ⇔ Kintetsu-Nara)",
          "price": "¥1,020 one way",
          "text": "Change at Takeda (some expresses run straight through). Boarding Kintetsu at Kyoto Station makes it ¥980; the limited express is ¥520 extra, and its tickets can be bought online, ticketless.",
          "url": "https://www.kintetsu.co.jp/gyoumu/ticket/"
        },
        {
          "name": "Kintetsu (Osaka-Namba ⇔ Kintetsu-Nara)",
          "price": "¥680 one way",
          "text": "35–40 minutes by rapid express, no change. From Umeda, take the Midosuji Line to Namba (¥240).",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Todaiji Great Buddha Hall",
          "price": "¥800",
          "text": "Combined ticket with the Todaiji Museum ¥1,200. Cash only.",
          "url": "https://www.todaiji.or.jp/information/haikan/"
        },
        {
          "name": "Harushika sake tasting",
          "price": "¥700",
          "text": "One cup each of five kinds. Reception 10:00–16:30, closed Tuesdays. Age 20 and over.",
          "url": "https://www.harushika.com/visit-brewery/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 21–22, 2026 (official sites of the venues; trains on a route planner, timetable for Saturday Nov 28).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose your start time",
          "text": "Use the buttons above the list: “Early start” (for the opening of the Great Buddha Hall) or “Leave at 9–10” (Great Buddha late in the day). The order and the times change."
        },
        {
          "title": "Six stops are chosen for you",
          "text": "They are the six that fit the timetable in one day. Drop what you’ll skip; tap “Want to go” to add the gardens, Mt. Wakakusa, the Heijo Palace site or Horyuji."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, hours and suggested times. Trains there and back are under no. 1, Kintetsu-Nara Station."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map made by Toshi. Borrowed photos carry the photographer’s name."
    },
    // 早朝に出発（early）のときに intro を上書きする項目（scripts/sync_nara.py の差分）
    introFor: {
      early: {
        "lead": "Take a train soon after 6:00. Walk through Nara Park while it is still nearly empty and enter the Great Buddha Hall as it opens. Go on to Nigatsudo and Kasuga Taisha, then have breakfast at the shrine’s teahouse when it opens at 10:30. Midday is for Naramachi and the Harushika sake brewery, with Kofukuji’s National Treasure Hall last, and a train home before 16:00.",
        "favText": "It opens at 8:00 from November to March and at 7:30 from April to October. Be there at opening and you see it before the tour groups build up.",
        "dayHead": "One day, early start (November–March)",
        "day": [
          {
            "time": "7:22",
            "area": "Nara Park, Todaiji & Nigatsudo",
            "title": "The Great Buddha Hall at its 8:00 opening",
            "text": "Take the 6:24 from Karasuma Oike (from Osaka-Namba, the 6:37) to Kintetsu-Nara. Walk through the park and its deer to the Great South Gate, enter the hall at 8:00, then climb to Nigatsudo’s balcony. From April to October the hall opens at 7:30: take one train earlier.",
            "photo": [
              "todaiji",
              0
            ]
          },
          {
            "time": "9:50",
            "area": "Kasuga Taisha",
            "title": "The shrine, then breakfast at its teahouse",
            "text": "Walk along the foot of Mt. Wakakusa to Kasuga Taisha. Kasuga Ninaijaya on the approach opens at 10:30: rice porridge for breakfast, and a rest.",
            "photo": [
              "kasuga",
              0
            ]
          },
          {
            "time": "11:40",
            "area": "Naramachi & Harushika",
            "title": "The old town and a sake tasting",
            "text": "Walk past the Tobihino lawn to Naramachi. See Gangoji and Koshi-no-Ie, have a light lunch, then soon after 13:00 taste five sakes at Harushika (¥700).",
            "photo": [
              "harushika",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "Kofukuji → home",
            "title": "Last, the Ashura statue",
            "text": "Climb the stone steps beside Sarusawa Pond to Kofukuji. After the National Treasure Hall the station is 7 minutes’ walk. Still have energy? Isuien, or the Heijo Palace site on the way home.",
            "note": "Kintetsu-Nara 15:45 → Karasuma Oike 16:44 (for Osaka-Namba: 15:36 → 16:16)",
            "photo": [
              "kofukuji",
              0
            ]
          }
        ]
      }
    }
  }
};
