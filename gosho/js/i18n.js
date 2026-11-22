/* Page texts in Japanese and English.
   Toshi 個人のマップ。三条のあたりから歩きと地下鉄で回る、二条城と京都御所の1日ルート。
   コースは2つ（scripts/sync_gosho.py）：intro は「9〜10時に出発」の内容で、introFor.early（開城に合わせる）が app.js で上書きされる。
   Photos are [spot id, photo index]（コースで番号が変わるので id で指定）.
   時刻・料金は2026年11月21〜22日に確認（各施設の公式サイト、電車は乗換案内）。文章は scripts/build_gosho_data.py と合わせること */
window.GOSHO_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都の中心 二条城と京都御所 MAP',
    titleMain: '二条城と京都御所',
    titleSub: 'Nijo Castle & Imperial Palace',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '出発時間でコースを選べます。最初に選ばれている7か所が、時間割どおりに1日で回れる組み合わせです。晴明神社・仙洞御所・マンガミュージアムは寄り道なので、足すときは各スポットの案内を見てください。',
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
    credit: '写真・文章：Toshi（二条城の昼・神泉苑・晴明神社・蛤御門・仙洞御所・マンガミュージアム・錦市場のアーケードの写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は、最初に選ばれている7か所を回る場合の目安です。寄り道を足したら、そのぶん後ろにずらしてください。',
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
    swCourse: '出発時間',
    courseAria: '出発時間',
    courseEarly: '開城に合わせる\n（8時すぎ発・二条城8:45）',
    courseLate: '9〜10時に出発\n（二条城は14時すぎ）',
    swMode: '回り方',
    intro: {
      "kicker": "三条のあたりから、歩きと地下鉄で回る1日",
      "h1": "将軍の城から、天皇の御所へ。",
      "lead": "9〜10時に出る日は、寺町通を歩いて京都御苑へ。梨木神社の名水、人の少ない御苑の北側、予約なしで入れる京都御所を見て、御苑の中の休憩所でお昼。団体の多い昼を外して14時すぎに二条城へ行き、夕方は街なかへ戻って錦市場、夜は先斗町・木屋町で。8時すぎに出られる人は、一覧の上のボタンで「開城に合わせる」に切り替えてください。開城の8:45に二条城へ入る時間割になります。",
      "favLabel": "いちばんの見どころ",
      "favName": "京都御所の紫宸殿",
      "favText": "即位の礼が行われた正殿。朱色の承明門の柱のあいだから、正面に見えます。無料・予約なし。月曜休み。",
      "favPhoto": [
        "gosho",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "月曜は京都御所と仙洞御所が休み（祝日のときは翌日）。御苑の公園は毎日入れます",
        "京都御所は、冬（10〜2月）は15:20までに入場。中で飲食はできず、スーツケースは持ち込めません",
        "二条城は8:45開城、入城は16:00まで。12月と1月の火曜は二の丸御殿に入れません",
        "二条城の本丸御殿は事前予約制（WEBチケット、別に1,000円）",
        "仙洞御所は申し込みが必要で18歳以上。全員の本人確認の書類を（当日の整理券は朝8:40から、1日50人）",
        "水曜はマンガミュージアムが休み。錦市場は夕方早く閉まる店が多い",
        "歩くのは全部で8〜10km。御苑は玉砂利の道なので、歩きやすい靴で",
        "梅は2月中旬〜3月中旬、桃としだれ桜は3月中旬〜4月上旬。紅葉の写真は11月23日"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "day": [
        {
          "time": "9:45",
          "area": "寺町通・梨木神社",
          "title": "歩いて御苑へ。まず名水をひと口",
          "text": "三条のあたりから寺町通を北へ約30分。御苑の東の門の向かいが梨木神社です。京都三名水の「染井」の水を自由に飲めます。",
          "photo": [
            "nashinoki",
            0
          ]
        },
        {
          "time": "10:45",
          "area": "御苑の北側",
          "title": "もみじと松林の静かな道",
          "text": "御所の塀に沿って北へ。朔平門、近衞邸跡のしだれ桜、乾御門のあたりの紅葉。和菓子屋のカフェがある休憩所もあります。",
          "photo": [
            "kitagyoen",
            0
          ]
        },
        {
          "time": "11:25",
          "area": "京都御所",
          "title": "予約なしで御所の中へ、そのあとお昼",
          "text": "清所門から入り、紫宸殿、清涼殿、御池庭を約50分で。お昼は歩いて3分の中立売休憩所「檜垣」で（8:00〜18:30）。",
          "photo": [
            "gosho",
            1
          ]
        },
        {
          "time": "13:20",
          "area": "梅林・蛤御門",
          "title": "御苑の西側を南へ下って地下鉄へ",
          "text": "弾の跡が残る蛤御門、梅林、桃林。丸太町14:00発の地下鉄で、烏丸御池で乗り換えて二条城前へ（14:12着・220円）。",
          "photo": [
            "gyoen",
            0
          ]
        },
        {
          "time": "14:20",
          "area": "二条城",
          "title": "昼の団体のあとの城へ",
          "text": "まず二の丸御殿（受付16:10まで）、そのあと庭と本丸、天守閣跡。帰りに南の神泉苑に寄って、地下鉄で京都市役所前へ4分。",
          "note": "入城は16:00まで、閉城17:00",
          "photo": [
            "nijojo",
            0
          ]
        },
        {
          "time": "17:15",
          "area": "錦市場・先斗町・木屋町",
          "title": "街なかへ戻って、夜まで",
          "text": "開いている店で少し食べて、錦天満宮（20:00まで）へ。晩ごはんは先斗町か木屋町で。北へ歩けば三条です。",
          "note": "21〜22時ごろまで",
          "photo": [
            "nishiki",
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と料金のめやす",
      "dealsLead": "地下鉄は2回で440円（1回220円）。歩いて戻れる距離なので、一日券を買うほどではありません。京都御苑・京都御所・仙洞御所・神泉苑・梨木神社は無料です。",
      "deals": [
        {
          "name": "二条城",
          "price": "1,300円",
          "text": "入城と二の丸御殿のセット。本丸御殿は別に1,000円（WEBチケットの事前予約が必要）。",
          "url": "https://nijo-jocastle.city.kyoto.lg.jp/admission/fee/"
        },
        {
          "name": "京都御所・京都御苑",
          "price": "無料",
          "text": "御所は予約なしで入れます（月曜休み）。仙洞御所も無料ですが、申し込みが必要です。",
          "url": "https://kyoto-gosho.kunaicho.go.jp/visit"
        },
        {
          "name": "京都国際マンガミュージアム（寄り道）",
          "price": "1,200円",
          "text": "中高生400円、小学生200円。水曜休み、最終入館16:30。",
          "url": "https://kyotomm.jp/opentime-cost/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月21〜22日に確認しました（各施設の公式サイト、電車は乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間でコースを選ぶ",
          "text": "一覧の上のボタンで「開城に合わせる」か「9〜10時に出発」を選びます。回る順番と時間が変わります。"
        },
        {
          "title": "最初に選ばれている7か所が1日分",
          "text": "時間割どおりに回れる組み合わせです。寄り道（晴明神社・仙洞御所・マンガミュージアム）を足すと、行き方のヒントが出ます。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・電車の時刻・おすすめの時間が見られます。入口で困ること（休み・予約・受付の時刻）は、いちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです。借りた写真には撮影者の名前を載せています。",
      "from": ""
    },
    // 「開城に合わせる」（early）のときに intro を上書きする項目（scripts/sync_gosho.py の差分）
    introFor: {
      early: {
        "lead": "8時すぎに三条のあたりを出て、地下鉄で4分。開城の8:45に二条城へ入り、団体が増える前に二の丸御殿を見ます。神泉苑に寄って地下鉄で京都御苑へ。梅林と蛤御門、京都御所を見て、御苑の中の休憩所でお昼。午後は人の少ない御苑の北側と梨木神社へ回り、寺町通を歩いて街なかへ。夕方の錦市場、夜は先斗町・木屋町で。",
        "dayHead": "1日の流れ（開城に合わせる）",
        "day": [
          {
            "time": "8:45",
            "area": "二条城",
            "title": "開城と同時に二の丸御殿へ",
            "text": "京都市役所前8:24発の地下鉄で二条城前へ（8:28着・220円）。金のふすま絵と、うぐいす張りの廊下。そのあと庭と本丸、南の神泉苑へ。",
            "photo": [
              "nijojo",
              0
            ]
          },
          {
            "time": "11:20",
            "area": "京都御苑",
            "title": "しだれ桜・桃林・梅林・蛤御門",
            "text": "二条城前10:58発の地下鉄で丸太町へ（11:10着・220円）。御苑の西側を、花の林を見ながら北へ歩きます。",
            "photo": [
              "gyoen",
              0
            ]
          },
          {
            "time": "11:55",
            "area": "京都御所",
            "title": "予約なしで御所の中へ、そのあとお昼",
            "text": "清所門から入り、紫宸殿、清涼殿、御池庭を約50分で。お昼は歩いて3分の中立売休憩所「檜垣」で（8:00〜18:30）。",
            "photo": [
              "gosho",
              1
            ]
          },
          {
            "time": "13:50",
            "area": "御苑の北側・梨木神社",
            "title": "もみじと松林の静かな道、名水",
            "text": "乾御門のあたりの紅葉、近衞邸跡のしだれ桜。御所の東を南へ下って、梨木神社で「染井」の水を。",
            "photo": [
              "kitagyoen",
              0
            ]
          },
          {
            "time": "15:00",
            "area": "寺町通",
            "title": "歩いて街なかへ。途中でお茶を",
            "text": "古道具屋や紙の店が並ぶ寺町通を南へ。寺町二条の一保堂茶舗の喫茶室でひと休み（ラストオーダー16:30、第2水曜休み）。",
            "photo": [
              "nashinoki",
              0
            ]
          },
          {
            "time": "16:10",
            "area": "錦市場・先斗町・木屋町",
            "title": "京の台所から、夜の路地へ",
            "text": "店が閉まる前の錦市場で少しずつ食べて、錦天満宮へ。日が暮れたら鴨川を歩いて、先斗町か木屋町で晩ごはん。",
            "note": "21〜22時ごろまで",
            "photo": [
              "nishiki",
              0
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Central Kyoto: Nijo Castle & the Imperial Palace MAP',
    titleMain: 'Nijo Castle & Imperial Palace',
    titleSub: '二条城と京都御所',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Choose a course by start time. The seven places selected at first are the set that fits one day on the timetable. Seimei Shrine, the Sento Palace and the Manga Museum are side stops: see each entry before adding them.',
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
    credit: 'Photos and text: Toshi (the daytime photos of Nijo Castle and the photos of Shinsen-en, Seimei Shrine, the Hamaguri gate, the Sento Palace, the Manga Museum and the Nishiki arcade are from Wikimedia Commons; author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
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
    checkedDate: '22 November 2026',
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
    pickNote: 'Tap “Want to go” on the places you want to visit. Times assume the seven places selected at first; if you add side stops, push the later times back.',
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
    swCourse: 'Start time',
    courseAria: 'Start time',
    courseEarly: 'Castle at opening\n(leave 8:10, castle 8:45)',
    courseLate: 'Leave at 9–10\n(castle after 14:00)',
    swMode: 'Stops',
    intro: {
      "kicker": "A day on foot and by subway from the Sanjo area",
      "h1": "From the shogun’s castle to the emperor’s palace.",
      "lead": "Leaving at 9–10, walk up Teramachi-dori to the Imperial Palace Park. Taste the spring water at Nashinoki Shrine, see the quiet north side of the park and the Palace (free, no booking), and have lunch at the rest house inside the park. Go to Nijo Castle after 14:00, once the midday tour groups have thinned, then come back into town for Nishiki Market and an evening in Pontocho and Kiyamachi. Can you leave soon after 8:00? Switch to “Castle at opening” with the buttons above the list: the timetable then starts at Nijo Castle when it opens at 8:45.",
      "favLabel": "Highlight",
      "favName": "The Shishinden, Kyoto Imperial Palace",
      "favText": "The hall of enthronements, seen head-on between the vermilion pillars of the Jomeimon gate. Free, no booking. Closed Mondays.",
      "favPhoto": [
        "gosho",
        0
      ],
      "whoHead": "Before you go",
      "who": [
        "The Palace and the Sento Palace are closed on Mondays (the next day if a holiday). The park itself is open every day",
        "In winter (Oct–Feb) last entry to the Palace is 15:20. No eating inside, and no suitcases",
        "Nijo Castle opens at 8:45; last entry 16:00. No Ninomaru Palace on Tuesdays in December and January",
        "The castle’s Honmaru Palace is by advance booking (web ticket, ¥1,000 extra)",
        "The Sento Palace needs an application and is for ages 18+; ID for everyone (same-day tickets from 8:40, 50 a day)",
        "The Manga Museum is closed on Wednesdays. Many Nishiki Market shops close early in the evening",
        "You walk 8–10 km in all. The park paths are gravel: wear comfortable shoes",
        "Plums mid-Feb to mid-March, peach and weeping cherry mid-March to early April; the maple photos are from 23 November"
      ],
      "dayHead": "One day, roughly like this (leaving at 9–10)",
      "day": [
        {
          "time": "9:45",
          "area": "Teramachi-dori & Nashinoki Shrine",
          "title": "Walk to the park; first, a sip of spring water",
          "text": "About 30 minutes north up Teramachi-dori from the Sanjo area. Nashinoki Shrine is opposite the park’s east gate; anyone may drink the Somei water, one of Kyoto’s three famous wells.",
          "photo": [
            "nashinoki",
            0
          ]
        },
        {
          "time": "10:45",
          "area": "North side of the park",
          "title": "Quiet paths under maples and pines",
          "text": "North along the Palace wall: the Sakuheimon gate, the weeping cherries of the Konoe site, the maples near the Inui gate. There is a rest house with a sweet-maker’s café.",
          "photo": [
            "kitagyoen",
            0
          ]
        },
        {
          "time": "11:25",
          "area": "Imperial Palace",
          "title": "Walk in without a booking, then lunch",
          "text": "In by the Seishomon gate: Shishinden, Seiryoden and the pond garden in about 50 minutes. Lunch at Higaki in the Nakadachiuri rest house, 3 minutes away (8:00–18:30).",
          "photo": [
            "gosho",
            1
          ]
        },
        {
          "time": "13:20",
          "area": "Plum grove & Hamaguri gate",
          "title": "Down the west side of the park to the subway",
          "text": "The Hamaguri gate with its bullet marks, the plum and peach groves. Take the 14:00 subway from Marutamachi, change at Karasuma-Oike, and reach Nijojo-mae at 14:12 (¥220).",
          "photo": [
            "gyoen",
            0
          ]
        },
        {
          "time": "14:20",
          "area": "Nijo Castle",
          "title": "The castle after the midday groups",
          "text": "The Ninomaru Palace first (entry until 16:10), then the garden, the Honmaru and the keep base. Stop at Shinsen-en to the south, then 4 minutes by subway to Kyoto Shiyakusho-mae.",
          "note": "Last entry 16:00; closes 17:00",
          "photo": [
            "nijojo",
            0
          ]
        },
        {
          "time": "17:15",
          "area": "Nishiki Market, Pontocho & Kiyamachi",
          "title": "Back in town until late",
          "text": "Eat a little at the shops still open, then Nishiki Tenmangu (open until 20:00). Dinner in Pontocho or Kiyamachi; walk north and you are at Sanjo.",
          "note": "Out until 21:00–22:00",
          "photo": [
            "nishiki",
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and prices",
      "dealsLead": "Two subway rides, ¥440 in all (¥220 each). You can walk back, so a day pass isn’t worth it. The park, the Imperial Palace, the Sento Palace, Shinsen-en and Nashinoki Shrine are free.",
      "deals": [
        {
          "name": "Nijo Castle",
          "price": "¥1,300",
          "text": "Castle entry with the Ninomaru Palace. The Honmaru Palace is ¥1,000 extra (timed web ticket booked in advance).",
          "url": "https://nijo-jocastle.city.kyoto.lg.jp/admission/fee/"
        },
        {
          "name": "Imperial Palace & park",
          "price": "Free",
          "text": "No booking for the Palace (closed Mondays). The Sento Palace is also free but needs an application.",
          "url": "https://kyoto-gosho.kunaicho.go.jp/en/visit"
        },
        {
          "name": "Kyoto International Manga Museum (side stop)",
          "price": "¥1,200",
          "text": "Ages 12–18 ¥400, 6–12 ¥200. Closed Wednesdays; last entry 16:30.",
          "url": "https://kyotomm.jp/en/"
        }
      ],
      "dealsNote": "Adult fares and prices, checked on 21–22 November 2026 (official websites; trains on Yahoo! Transit).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose a course by start time",
          "text": "Use the buttons above the list: “Castle at opening” or “Leave at 9–10”. The order and the times change."
        },
        {
          "title": "The seven places selected at first are one day",
          "text": "They fit the timetable. Add a side stop (Seimei Shrine, the Sento Palace, the Manga Museum) and hints on how to fit it in appear."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map or “Spots” for photos, a description, prices, train times and a suggested time. Things that can stop you at the door (closed days, bookings, last entry) are shown at the top."
        },
        {
          "title": "Routes in Google Maps",
          "text": "“Open in Google Maps” on each spot takes you straight to route search."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map made by Toshi. Borrowed photos carry the photographer’s name.",
      "from": "From"
    },
    introFor: {
      early: {
        "lead": "Leave the Sanjo area soon after 8:00; the subway takes 4 minutes. Go into Nijo Castle as it opens at 8:45 and see the Ninomaru Palace before the tour groups build up. Stop at Shinsen-en, then take the subway to the Imperial Palace Park: the plum grove and Hamaguri gate, the Palace, and lunch at the rest house inside the park. In the afternoon, the quiet north side of the park and Nashinoki Shrine, then a walk back into town down Teramachi-dori. Nishiki Market in the late afternoon, Pontocho and Kiyamachi at night.",
        "dayHead": "One day, roughly like this (castle at opening)",
        "day": [
          {
            "time": "8:45",
            "area": "Nijo Castle",
            "title": "Into the Ninomaru Palace at opening time",
            "text": "The 8:24 subway from Kyoto Shiyakusho-mae reaches Nijojo-mae at 8:28 (¥220). Gold-leaf screens and floors that chirp underfoot; then the garden, the Honmaru and Shinsen-en to the south.",
            "photo": [
              "nijojo",
              0
            ]
          },
          {
            "time": "11:20",
            "area": "Imperial Palace Park",
            "title": "Weeping cherry, peach and plum groves, Hamaguri gate",
            "text": "The 10:58 subway from Nijojo-mae reaches Marutamachi at 11:10 (¥220). Walk north up the west side of the park past the flowering groves.",
            "photo": [
              "gyoen",
              0
            ]
          },
          {
            "time": "11:55",
            "area": "Imperial Palace",
            "title": "Walk in without a booking, then lunch",
            "text": "In by the Seishomon gate: Shishinden, Seiryoden and the pond garden in about 50 minutes. Lunch at Higaki in the Nakadachiuri rest house, 3 minutes away (8:00–18:30).",
            "photo": [
              "gosho",
              1
            ]
          },
          {
            "time": "13:50",
            "area": "North side of the park & Nashinoki Shrine",
            "title": "Quiet paths under maples and pines; spring water",
            "text": "Maples near the Inui gate, weeping cherries at the Konoe site. Walk down the east side of the Palace to Nashinoki Shrine and its Somei water.",
            "photo": [
              "kitagyoen",
              0
            ]
          },
          {
            "time": "15:00",
            "area": "Teramachi-dori",
            "title": "Walk back into town, with tea on the way",
            "text": "South down Teramachi-dori past antique dealers and paper shops. Rest in the tearoom of Ippodo Tea at Teramachi Nijo (last order 16:30; closed second Wednesday).",
            "photo": [
              "nashinoki",
              0
            ]
          },
          {
            "time": "16:10",
            "area": "Nishiki Market, Pontocho & Kiyamachi",
            "title": "From Kyoto’s kitchen to the lanes at night",
            "text": "Graze through Nishiki Market before the shops close, then Nishiki Tenmangu. After dark, walk by the Kamo river and have dinner in Pontocho or Kiyamachi.",
            "note": "Out until 21:00–22:00",
            "photo": [
              "nishiki",
              0
            ]
          }
        ]
      }
    }
  }
};
