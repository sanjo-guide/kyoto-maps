/* Page texts in Japanese and English.
   Toshi 個人のマップ。三条から市バスで京都の北へ。今宮神社のあぶり餅と、鷹峯の源光庵・常照寺・光悦寺。
   コースは2つ（鷹峯の開門に合わせる／9〜10時に出発）。intro は「9〜10時に出発」の内容で、introFor.early が
   app.js で上書きされる（scripts/sync_takagamine.py）。大徳寺・しょうざん・金閣寺は最後のスポットの文章で案内。
   Photos are [spot id, photo index] from data/routes/takagamine.json（コースで番号が変わるので id で指定）。
   時刻・料金は2026年11月22日に確認（京都市交通局の時刻表、各寺社・施設の公式サイト、京都観光Navi、乗換案内）。 */
window.TAKAGAMINE_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 今宮神社と鷹峯 Takagamine MAP',
    titleMain: '今宮神社と鷹峯',
    titleSub: 'Imamiya & Takagamine',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '上のボタンで出発時間を選ぶと、回る順番と時間が変わります。開門に合わせるコースは鷹峯が先、9〜10時発のコースは今宮神社から。鷹峯の3つのお寺は歩いて数分ずつです。点線は順番を示す線で、実際の道ではありません。',
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
    train: 'バス・電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや時刻表・乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。外したときの行き方は、各スポットの「あなたのルートでは」に出ます。',
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "鷹峯の開門に合わせる\n二条駅前 8:10発",
    courseLate: "9〜10時に出発\n今宮神社から",
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
      "h1": "千年続くあぶり餅と、鷹峯の3つのお寺。お昼はしょうざん、夕方は金閣寺へ。",
      "lead": "京都の北、今宮神社の門前で平安時代から続くあぶり餅を食べたら、市バスで鷹峯（たかがみね）へ。丸窓の源光庵、吉野太夫の赤門の常照寺、本阿弥光悦の芸術村の跡の光悦寺は、歩いて数分ずつです。9〜10時に出る日は、四条河原町から市バス1本で今宮神社へ。鷹峯のあとは坂を下って、しょうざんリゾート京都の庭園の中でお昼。そのまま歩いて金閣寺へ下り、夕方のバスで三条に戻って、夜は先斗町・木屋町で。朝早く出られる人は、上のボタンで「鷹峯の開門に合わせる」コースに切り替えてください。紅葉の見ごろは例年11月中旬〜下旬です（京都観光Naviの紅葉だより）。",
      "favLabel": "いちばんの見どころ",
      "favName": "光悦寺",
      "favText": "もみじのトンネルの参道と、竹を斜めに組んだ光悦垣。",
      "favPhoto": [
        "koetsuji",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "三条からは市バスで。四条河原町から46系統で今宮神社前まで約35分・230円",
        "あぶり餅の2軒は水曜休み（1日・15日・祝日なら翌日）。12月16日〜31日も休み",
        "光悦寺は紅葉の時期は8:30から・500円。毎年11月10日〜13日は拝観できません",
        "源光庵は本堂に上がるので、靴を入れる袋を持って。拝観料は400円（紅葉の時期は500円）",
        "お昼はしょうざんのわかどりか楼蘭。ラストオーダーが14時なので、13時半までに",
        "鷹峯の3つのお寺は歩いて2〜5分ずつ。しょうざんへ15分、金閣寺へはそこから25分ほど歩きます",
        "帰りの市バス59系統（金閣寺道→河原町三条）の最終は20:39。12月6日まではしょうざんの夜のライトアップも"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "from": "",
      "day": [
        {
          "time": "10:11",
          "area": "紫野",
          "title": "今宮神社とあぶり餅",
          "text": "四条河原町9:36発の市バス46系統で今宮神社前へ。お参りして、東門の前の茶店であぶり餅を。",
          "note": "日祝は9:39発→10:14着",
          "photo": [
            "imamiya",
            1
          ]
        },
        {
          "time": "11:08",
          "area": "鷹峯",
          "title": "源光庵・常照寺・光悦寺",
          "text": "佛教大学前11:04発の市バス6系統で鷹峯へ。丸窓の源光庵、赤い吉野門の常照寺、もみじの参道の光悦寺。",
          "photo": [
            "genkoan",
            0
          ]
        },
        {
          "time": "13:30",
          "area": "鷹峯 → 衣笠",
          "title": "しょうざんでお昼、そして金閣寺へ",
          "text": "坂を下ってしょうざんでお昼と庭園。歩いて金閣寺へ下りて、15時半ごろに入ります（17:00まで）。",
          "photo": [
            "koetsuji",
            5
          ]
        },
        {
          "time": "16:35",
          "area": "帰り → 三条",
          "title": "バスで三条へ、夜は街なかで",
          "text": "金閣寺道から市バス59系統で河原町三条へ約30分。晩ごはんは先斗町・木屋町で、21〜22時ごろまで。12月6日までは、しょうざんの夜の紅葉ライトアップ（17:30〜20:00）に回っても。",
          "note": "平日16:35発→河原町三条17:05着",
          "photo": [
            "joshoji",
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と拝観料のめやす",
      "dealsLead": "市バスは1回230円。9〜10時発のコースは46・6・59系統の3回で690円です。地下鉄も使う日や、寄り道でバスに乗る回数が増える日は、地下鉄・バス1日券（1,100円）も。拝観料（紅葉の時期の光悦寺・源光庵500円、常照寺400円、金閣寺500円など）は別です。",
      "deals": [
        {
          "name": "市バス",
          "price": "1回230円",
          "text": "四条河原町→今宮神社前（46系統）、佛教大学前→鷹峯源光庵前（6・北1系統）、金閣寺道→河原町三条（59系統）。",
          "url": "https://www2.city.kyoto.lg.jp/kotsu/busdia/bustime.htm"
        },
        {
          "name": "光悦寺",
          "price": "500円（紅葉の時期）",
          "text": "ふだんは400円。8:00〜17:00（紅葉の時期は8:30から）。毎年11月10日〜13日は休み。",
          "url": "https://ja.kyoto.travel/tourism/single01.php?category_id=7&tourism_id=279"
        },
        {
          "name": "源光庵",
          "price": "500円（紅葉の時期）",
          "text": "ふだんは400円。9:00〜17:00（受付16:30まで）。法要の日は拝観を止めることあり。",
          "url": "https://www.kyoto-kankou.or.jp/info_search/9493"
        },
        {
          "name": "常照寺",
          "price": "400円",
          "text": "8:30〜17:00。",
          "url": "http://tsakae.justhpbs.jp/joshoji/toppage.html"
        },
        {
          "name": "しょうざん 日本庭園",
          "price": "500円",
          "text": "9:00〜17:00、無休。しょうざんの店で食事をした人は300円。",
          "url": "https://www.shozan.co.jp/sansaku/index.html"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日・23日に確認しました（京都市交通局の時刻表、各寺社・施設の公式サイト、京都観光Navi、京都府観光連盟、乗換案内）。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「鷹峯の開門に合わせる」（二条駅前8:10発）と「9〜10時に出発」（四条河原町9:36発）を切り替えます。回る順番と時間が変わります。"
        },
        {
          "title": "番号の順に",
          "text": "1から4の順に回ると、時間割どおりの1日になります。最後のスポットに、お昼、そのあとの寄り道、帰りのバスと夜を書いています。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "「選んで回る」に切り替えると、行きたい場所だけを選べます。外したときの行き方も出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。"
    },
    introFor: {
      early: {
          "lead": "二条駅前8:10発の市バス6系統で鷹峯へ。8:30に開く常照寺から歩き始めて、9時の開門と同時に源光庵へ入り、人が少ないうちに迷いの窓と悟りの窓の前に座ります。朝の光悦寺のもみじの参道を歩いたら、バスで下りて今宮神社へ。あぶり餅で遅めの朝ごはんのかわりにひと休み。歩いて大徳寺へ回り、塔頭の庭を見て、境内の泉仙でお昼。午後は市バスで金閣寺へ。12月6日までは、しょうざんの夜の紅葉ライトアップもあります。",
          "favText": "9時の開門に合わせて行くと、人が増える前に、迷いの窓と悟りの窓の前に座れます。",
          "favName": "源光庵",
          "favPhoto": [
            "genkoan",
            0
          ],
          "dayHead": "1日の流れ（鷹峯の開門に合わせる）",
          "day": [
            {
              "time": "8:32",
              "area": "鷹峯",
              "title": "常照寺から、開門の源光庵へ",
              "text": "京都市役所前7:55発の地下鉄で二条へ、二条駅前8:10発の市バス6系統で鷹峯へ。常照寺を見て、9時に源光庵。",
              "note": "土休日は8:01発・8:13発→8:33着",
              "photo": [
                "joshoji",
                0
              ]
            },
            {
              "time": "9:45",
              "area": "鷹峯",
              "title": "朝の光悦寺",
              "text": "もみじのトンネルの参道を、人の少ないうちに。10:38発の市バス6系統で下ります。",
              "photo": [
                "koetsuji",
                0
              ]
            },
            {
              "time": "10:55",
              "area": "紫野",
              "title": "今宮神社であぶり餅",
              "text": "佛教大学前から歩いて5〜7分。お参りして、茶店に座って遅めの朝ごはんのかわりに。",
              "photo": [
                "imamiya",
                1
              ]
            },
            {
              "time": "11:45",
              "area": "大徳寺 → 金閣寺",
              "title": "大徳寺の塔頭と、泉仙でお昼",
              "text": "黄梅院（12月6日まで）か大仙院の庭を見て、境内の泉仙で精進料理。午後は市バス12系統で金閣寺へ6分。帰りは59系統で河原町三条へ、夜は街なかで。",
              "photo": [
                "koetsuji",
                5
              ]
            }
          ]
        }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kyoto: Imamiya & Takagamine MAP',
    titleMain: 'Imamiya & Takagamine',
    titleSub: '今宮神社と鷹峯',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Choose your start time with the buttons above: the order and the times change. The opening course does Takagamine first; the 9–10 course starts at Imamiya Shrine. The three Takagamine temples are a few minutes apart. The dotted line shows the order, not the actual path.',
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
    train: 'Bus & train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites, timetables and a route planner on {d}. Details can change, so please check before you go.',
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
    pickNote: 'Tap “Want to go” on the places you like. Times are for the full route. If you skip a place, “On your route” at each spot tells you how to get there.',
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "Takagamine at opening\n8:10 from Nijo",
    courseLate: "Leave at 9–10\nImamiya first",
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
      "h1": "A thousand-year-old snack and three temples at Takagamine. Lunch at Shozan, then down to Kinkaku-ji.",
      "lead": "In the north of Kyoto, eat aburi-mochi outside Imamiya Shrine, a treat sold here since the Heian period, then take the city bus up to Takagamine. Genkoan with its round windows, Joshoji with Yoshino Tayu’s red gate and Koetsuji on the site of Hon’ami Koetsu’s artists’ village are a few minutes apart. Leaving at 9–10, one city bus takes you from Shijo-Kawaramachi to Imamiya. After Takagamine, walk downhill to lunch inside the gardens of Shozan Resort Kyoto, carry on down to Kinkaku-ji, and take an early-evening bus back to Sanjo for dinner in Pontocho or Kiyamachi. If you can start early, switch to the “Takagamine at opening” course with the buttons above. The leaves usually peak in mid to late November (Kyoto City’s autumn-leaf report).",
      "favLabel": "Highlight",
      "favName": "Koetsuji",
      "favText": "A tunnel of maples along the approach, and the diagonal bamboo Koetsu fence.",
      "favPhoto": [
        "koetsuji",
        0
      ],
      "whoHead": "Good to know before you go",
      "who": [
        "From Sanjo it’s the city bus: no. 46 from Shijo-Kawaramachi to Imamiya-jinja-mae, about 35 min, ¥230",
        "Both aburi-mochi shops close on Wednesdays (Thursday if the 1st, 15th or a holiday) and 16–31 December",
        "Koetsuji opens at 8:30 and costs ¥500 in autumn; it is closed every year 10–13 November",
        "At Genkoan you take your shoes off: bring a bag for them. Admission ¥400 (¥500 in autumn)",
        "Lunch at Shozan’s Wakadori or Louran. Last orders are at 14:00, so arrive by 13:30",
        "The three Takagamine temples are 2–5 min apart on foot; then 15 min to Shozan and about 25 more to Kinkaku-ji",
        "The last city bus 59 (Kinkakuji-michi → Kawaramachi-Sanjo) leaves at 20:39. Until 6 Dec, Shozan’s garden is lit up in the evening"
      ],
      "dayHead": "One day, roughly like this (leaving at 9–10)",
      "from": "From",
      "day": [
        {
          "time": "10:11",
          "area": "Murasakino",
          "title": "Imamiya Shrine and aburi-mochi",
          "text": "City bus 46 from Shijo-Kawaramachi at 9:36. Visit the shrine, then aburi-mochi at a teahouse by the east gate.",
          "note": "Sundays and holidays: 9:39 → 10:14",
          "photo": [
            "imamiya",
            1
          ]
        },
        {
          "time": "11:08",
          "area": "Takagamine",
          "title": "Genkoan, Joshoji, Koetsuji",
          "text": "City bus 6 from Bukkyo-daigaku-mae at 11:04 up to Takagamine: Genkoan’s round windows, Joshoji’s red Yoshino gate and Koetsuji’s maple approach.",
          "photo": [
            "genkoan",
            0
          ]
        },
        {
          "time": "13:30",
          "area": "Takagamine → Kinugasa",
          "title": "Lunch at Shozan, then Kinkaku-ji",
          "text": "Walk downhill to Shozan for lunch and its garden, then on foot down to Kinkaku-ji, in by about 15:30 (closes 17:00).",
          "photo": [
            "koetsuji",
            5
          ]
        },
        {
          "time": "16:35",
          "area": "Back → Sanjo",
          "title": "Bus to Sanjo, evening in town",
          "text": "City bus 59 from Kinkakuji-michi to Kawaramachi-Sanjo, about 30 minutes. Dinner in Pontocho or Kiyamachi, until 21:00 or 22:00. Until 6 December you could go to Shozan’s evening light-up (17:30–20:00) instead.",
          "note": "Weekdays 16:35 → Kawaramachi-Sanjo 17:05",
          "photo": [
            "joshoji",
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and entry fees",
      "dealsLead": "City buses are ¥230 a ride; the 9–10 course uses three (46, 6 and 59): ¥690. If you also take the subway or add side trips, the Subway & Bus 1-day Pass (¥1,100) may pay off. Entry fees (Koetsuji and Genkoan ¥500 in autumn, Joshoji ¥400, Kinkaku-ji ¥500, etc.) are extra.",
      "deals": [
        {
          "name": "City bus",
          "price": "¥230 a ride",
          "text": "Shijo-Kawaramachi → Imamiya-jinja-mae (46); Bukkyo-daigaku-mae → Takagamine-Genkoan-mae (6, Kita-1); Kinkakuji-michi → Kawaramachi-Sanjo (59).",
          "url": "https://www2.city.kyoto.lg.jp/kotsu/busdia/bustime.htm"
        },
        {
          "name": "Koetsuji",
          "price": "¥500 (autumn)",
          "text": "Usually ¥400. 8:00–17:00 (from 8:30 in autumn). Closed 10–13 November.",
          "url": "https://ja.kyoto.travel/tourism/single01.php?category_id=7&tourism_id=279"
        },
        {
          "name": "Genkoan",
          "price": "¥500 (autumn)",
          "text": "Usually ¥400. 9:00–17:00 (last entry 16:30). Visits may stop on days of temple services.",
          "url": "https://www.kyoto-kankou.or.jp/info_search/9493"
        },
        {
          "name": "Joshoji",
          "price": "¥400",
          "text": "8:30–17:00.",
          "url": "http://tsakae.justhpbs.jp/joshoji/toppage.html"
        },
        {
          "name": "Shozan garden",
          "price": "¥500",
          "text": "9:00–17:00, open every day. ¥300 if you ate at one of Shozan’s restaurants.",
          "url": "https://www.shozan.co.jp/sansaku/index.html"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on 22–23 Nov 2026 (Kyoto City bus timetables, temple and garden websites, Kyoto Kanko Navi, Kyoto Prefecture tourism guide, a route planner).",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick a start time",
          "text": "Use the buttons above the list to switch between “Takagamine at opening” (8:10 from Nijo-eki-mae) and “Leave at 9–10” (9:36 from Shijo-Kawaramachi). The order and times change."
        },
        {
          "title": "In number order",
          "text": "Follow 1 to 4 for the day as timed. The last spot covers lunch, where to go next, the bus back and the evening."
        },
        {
          "title": "Skip what you like",
          "text": "Switch to “Choose stops” to pick only the places you want; it also tells you how to get there."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi."
    },
    introFor: {
      early: {
          "lead": "Take city bus 6 from Nijo-eki-mae at 8:10 up to Takagamine. Start at Joshoji, open from 8:30, and walk into Genkoan as it opens at 9:00 to sit at its two windows before the crowds. Walk Koetsuji’s maple approach in the morning, then take the bus down to Imamiya Shrine and rest over aburi-mochi in place of a late breakfast. Walk on to Daitoku-ji for a sub-temple garden and a Buddhist vegetarian lunch at Izusen inside the precinct. In the afternoon, a short bus ride to Kinkaku-ji. Until 6 December, Shozan’s garden is also lit up in the evening.",
          "favText": "Arrive for the 9:00 opening and you can sit at the two windows before it fills up.",
          "favName": "Genkoan",
          "favPhoto": [
            "genkoan",
            0
          ],
          "dayHead": "One day, roughly like this (Takagamine at opening)",
          "day": [
            {
              "time": "8:32",
              "area": "Takagamine",
              "title": "Joshoji, then Genkoan at opening",
              "text": "Subway from Kyoto Shiyakusho-mae at 7:55 to Nijo, then city bus 6 from Nijo-eki-mae at 8:10. Joshoji first, Genkoan at 9:00.",
              "note": "Weekends and holidays: 8:01 and 8:13 → 8:33",
              "photo": [
                "joshoji",
                0
              ]
            },
            {
              "time": "9:45",
              "area": "Takagamine",
              "title": "Koetsuji in the morning",
              "text": "The maple approach while it’s quiet. Down on city bus 6 at 10:38.",
              "photo": [
                "koetsuji",
                0
              ]
            },
            {
              "time": "10:55",
              "area": "Murasakino",
              "title": "Aburi-mochi at Imamiya",
              "text": "5–7 minutes’ walk from Bukkyo-daigaku-mae. Visit the shrine and sit down at a teahouse: a late breakfast and a rest.",
              "photo": [
                "imamiya",
                1
              ]
            },
            {
              "time": "11:45",
              "area": "Daitoku-ji → Kinkaku-ji",
              "title": "Daitoku-ji’s gardens and lunch at Izusen",
              "text": "Obai-in (until 6 Dec) or Daisen-in, then vegetarian lunch at Izusen in the precinct. In the afternoon, city bus 12 to Kinkaku-ji in 6 minutes; back on bus 59 to Kawaramachi-Sanjo for the evening in town.",
              "photo": [
                "koetsuji",
                5
              ]
            }
          ]
        }
    }
  }
};
