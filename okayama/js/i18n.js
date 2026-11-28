/* Page texts in Japanese and English.
   Toshi 個人のマップ。岡山と倉敷。日帰りの時間割は作らない（2026-11-22 オーナー：1泊した方が良い場所。もしくは京都・大阪〜広島の移動中に立ち寄る場所）。
   コースは2つ（一覧の上のボタン）：stay＝1泊2日（最初に開く。data/routes/okayama.json）、stop＝移動の途中に立ち寄る（okayama-stop.json）。
   intro はどちらのコースにも共通の項目で、コースで変わる項目は introFor[コース] が app.js で上書きされる（scripts/sync_okayama.py）。
   写真は [スポットの id, 写真の番号]。オーナーの写真は岡山城・月見橋・岡山駅・路面電車だけ。ほかは Wikimedia Commons（行った・食べたと書かない）。
   時刻・料金は2026年11月22日に確認（出典は data/routes/okayama.json の sources）。直すときはこのファイルを直接直してよい */
window.OKAYAMA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '岡山と倉敷 Okayama & Kurashiki MAP',
    titleMain: '岡山と倉敷',
    titleSub: 'Okayama & Kurashiki',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '番号は回る順番です。「1泊2日」は見出しとラベルで1日目・2日目が分かります。「立ち寄る」は、最初は岡山城と後楽園だけです。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（後楽園・吉備津神社・倉敷の写真と、改修後の岡山城の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
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
    pickNote: '最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。駅と路面電車は、選んだ場所に合わせて入ります。',
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
    swCourse: '旅の形',
    courseAria: '旅の形',
    courseStay: '1泊2日\n（夜と朝の倉敷）',
    courseStop: '移動の途中に立ち寄る\n（京都・大阪→広島）',
    swMode: '回り方',
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "きっぷ・荷物・入場料",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月22日に、各施設・JRの公式サイトと乗換案内（11月25日・28日・29日のダイヤ）で確認しました。指定席は日によって変わります。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "旅の形を選ぶ",
          "text": "一覧の上のボタンで「1泊2日」か「移動の途中に立ち寄る」を選びます。時間割と番号が変わります。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、荷物・きっぷ・休みの日など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（写真のある岡山城と岡山駅のほかは、公式サイトなどの情報と Wikimedia Commons の写真で紹介しています）。"
    },
    introFor: {
      "stay": {
        "kicker": "京都・大阪から1泊2日",
        "h1": "昼は黒いお城と大名の庭。夜と朝は、白壁の倉敷。",
        "lead": "黒い板張りの天守の岡山城から、月見橋を渡って大名の庭・後楽園へ。夕方に倉敷へ移り、明かりのつく川ぞいで晩ごはんを食べて、そのまま泊まります。2日目は店が開く前の静かな白壁の町を歩き、9時の開館と同時に大原美術館へ。午後は吉備津神社の長い廻廊を歩いて、京都・大阪へ帰るか、広島へ進みます。",
        "favName": "夜と朝の倉敷川",
        "favText": "夜は21時（4〜9月は22時）まで明かりがつき、朝は店が開く前の静かな時間です。（写真：Suicasmo / CC BY-SA 4.0）",
        "favPhoto": [
          "bikan",
          0
        ],
        "who": [
          "宿は倉敷美観地区のまわりがいちばん楽。倉敷駅・岡山駅のまわりでも回れます",
          "荷物は岡山駅のねこのてステーションに13:30までに預けると、指定の宿へ届きます（1,500円）",
          "大原美術館は月曜休み。2日目が月曜なら、1日目と2日目を入れ替え",
          "美術館は12〜2月は15:00まで。この時間割は朝9:00に入るので、冬もそのまま回れます",
          "川舟は雨で中止。WEB予約は30日前から。最初の時間割には入れていません",
          "連休と年末年始は、のぞみに自由席がない日があります"
        ],
        "dayHead": "2日間の流れ",
        "day": [
          {
            "time": "9:25",
            "area": "1日目・京都",
            "title": "のぞみで岡山へ",
            "text": "10:25着。新大阪からは9:41発の同じ列車です。荷物を預けて路面電車へ。",
            "photo": [
              "kyoto",
              0
            ],
            "note": "新大阪は9:41"
          },
          {
            "time": "11:05",
            "area": "1日目・岡山",
            "title": "岡山城、月見橋、後楽園",
            "text": "お城から橋を渡って庭へ。13:20から正門の外の四季彩でお昼。（写真：Fjkelfeimvvn / CC BY 3.0）",
            "photo": [
              "korakuen",
              0
            ]
          },
          {
            "time": "15:20",
            "area": "1日目・倉敷",
            "title": "明るいうちに町の高いところへ",
            "text": "宿に寄ってからアイビースクエアへ。16:30に阿智神社から瓦屋根を見下ろします。（写真：Zairon / CC BY 4.0）",
            "photo": [
              "achi",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "1日目・夜",
            "title": "明かりのつく川ぞいと晩ごはん",
            "text": "18:15ごろ晩ごはん。照明の消える21:00までもう一度歩いて、倉敷に泊まります。（写真：ノボホショコロトソ / CC BY 4.0）",
            "photo": [
              "honmachi",
              2
            ],
            "note": "21:00ごろまで"
          },
          {
            "time": "7:30",
            "area": "2日目・倉敷",
            "title": "店が開く前の町、9時に美術館",
            "text": "本町・東町と川ぞいを歩いて、開館と同時に大原美術館へ。お昼は11:30ごろ。（写真：Miya.m / CC BY-SA 4.0）",
            "photo": [
              "boat",
              3
            ]
          },
          {
            "time": "14:20",
            "area": "2日目・吉備津",
            "title": "国宝の本殿と長い廻廊",
            "text": "倉敷13:11発で岡山へ戻り、13:52発の桃太郎線で15分。15:47発で岡山へ。（写真：hiyang.on.flickr / CC BY 2.0）",
            "photo": [
              "kibitsu",
              0
            ]
          },
          {
            "time": "16:20",
            "area": "2日目・岡山駅",
            "title": "京都・大阪へ、または広島へ",
            "text": "京都17:20、新大阪17:04。広島へは16:26発で17:02着です。",
            "photo": [
              "kaeri",
              0
            ]
          }
        ],
        "dealsLead": "新幹線は片道ずつ、入場料は入った場所の分だけかかります。岡山〜倉敷はJRで片道330円、岡山〜吉備津は210円、路面電車は1回160円です。",
        "deals": [
          {
            "name": "新幹線 京都〜岡山",
            "price": "片道7,140円",
            "text": "自由席。のぞみの指定席は8,100円（11月25日）、8,300円（28日）。新大阪〜岡山は自由席5,610円、指定席6,460円（25日）。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "2日目に広島へ進む",
            "price": "片道5,610円",
            "text": "岡山→広島の自由席。京都→広島の乗車券（6,600円）を通しで買えば3日間有効で、岡山で途中下車できます。特急券は岡山で区切って2枚。",
            "url": "https://railway.jr-central.co.jp/ticket-rule/rule05.html"
          },
          {
            "name": "荷物を宿へ",
            "price": "1,500円",
            "text": "岡山駅のねこのてステーションに13:30までに預けると、指定の宿に17:00ごろ届きます。",
            "url": "https://www.okayama-kanko.jp/spot/detail_10022.html"
          },
          {
            "name": "岡山城・後楽園 共通券",
            "price": "800円",
            "text": "別々だと500円ずつ。お城は17:30まで、後楽園は17:00まで（3月20日〜9月は18:00）。",
            "url": "https://okayama-castle.jp/guide/"
          },
          {
            "name": "大原美術館",
            "price": "2,000円",
            "text": "月曜休み（祝日は開館）。12〜2月は15:00まで。館内は撮影禁止。",
            "url": "https://www.ohara.or.jp/visitor_info/"
          },
          {
            "name": "くらしき川舟流し（寄り道）",
            "price": "1,000円",
            "text": "約20分。WEB予約は30日前から、当日券は9:00から倉敷館で。",
            "url": "https://kankou-kurashiki.jp/special/kawafune/"
          }
        ]
      },
      "stop": {
        "kicker": "京都・大阪から広島への途中に",
        "h1": "広島へ行く途中、岡山で4時間40分。",
        "lead": "新幹線を岡山で降りて、荷物を駅に預け、路面電車で城下へ。黒い天守の岡山城から月見橋を渡って後楽園を歩き、お昼を食べたら、15:06ののぞみで広島へ（15:42着）。京都9:25発ののぞみで来れば、岡山にいられるのは4時間40分です。倉敷に寄りたいときは、お城と庭のかわりに。両方は立ち寄りの時間には入らないので、1泊2日のコースをすすめます。",
        "favName": "月見橋から見る岡山城",
        "favText": "川の上に黒い天守。お城から後楽園へ渡る橋の上からの眺めです（2021年3月、改修の前）。",
        "favPhoto": [
          "tsukimi",
          0
        ],
        "who": [
          "3時間なら後楽園だけ。4時間40分あればお城・後楽園・お昼",
          "5時間半あれば、かわりに倉敷の美術館と町並み（広島16:27着）。両方なら9時間はかかるので泊まりで",
          "スマートEXの通しの予約では途中下車できません。岡山で区切って予約を",
          "紙の乗車券は広島まで1枚で途中下車できます。特急券は岡山で区切って2枚",
          "荷物は新幹線の改札を出てすぐ。一時預かりは20:00まで・160cmまで（600円か800円）",
          "160cmを超える荷物は座席の予約が必要。自由席には持ち込めません"
        ],
        "dayHead": "立ち寄る日の流れ（岡山だけ）",
        "day": [
          {
            "time": "9:25",
            "area": "京都",
            "title": "のぞみで岡山へ",
            "text": "10:25着。新大阪からは9:41発の同じ列車。特急券は岡山までの分です。",
            "photo": [
              "kyoto",
              0
            ],
            "note": "新大阪は9:41"
          },
          {
            "time": "10:25",
            "area": "岡山駅",
            "title": "まず荷物を預ける",
            "text": "改札を出てすぐのねこのてステーションかロッカーへ。10:44の路面電車で城下に10:52着。",
            "photo": [
              "okayamaeki",
              0
            ]
          },
          {
            "time": "11:05",
            "area": "岡山城",
            "title": "天守と月見橋",
            "text": "天守を見学して、月見橋でふり返ります。",
            "photo": [
              "tsukimi",
              0
            ]
          },
          {
            "time": "12:15",
            "area": "後楽園",
            "title": "庭を1時間、そのあとお昼",
            "text": "13:20から正門の外の四季彩で。14:25の路面電車で駅へ戻ります。（写真：Fjkelfeimvvn / CC BY 3.0）",
            "photo": [
              "korakuen",
              0
            ]
          },
          {
            "time": "15:06",
            "area": "岡山駅",
            "title": "のぞみで広島へ",
            "text": "広島に15:42着。夕方の広島がまだ使えます。",
            "photo": [
              "kaeri",
              0
            ],
            "note": "広島15:42"
          }
        ],
        "dealsLead": "岡山で1回降りると、通しで乗るより高くなります。買い方ごとの合計です（岡山〜倉敷などの寄り道の分は別）。",
        "deals": [
          {
            "name": "京都→岡山→広島（乗車券は通し）",
            "price": "12,530円",
            "text": "乗車券6,600円＋自由席特急券3,400円＋2,530円。区間ごとに全部買うと12,750円、寄らなければ10,770円。",
            "url": "https://railway.jr-central.co.jp/ticket-rule/rule05.html"
          },
          {
            "name": "新大阪→岡山→広島（乗車券は通し）",
            "price": "10,780円",
            "text": "乗車券5,720円＋自由席特急券2,530円＋2,530円。区間ごとだと11,220円、寄らなければ9,890円。",
            "url": "https://railway.jr-central.co.jp/ticket-rule/rule05.html"
          },
          {
            "name": "スマートEXを2つに分ける",
            "price": "14,160円",
            "text": "京都から（7,900円＋6,260円）。新大阪からは12,520円。のぞみ指定席・通常期の額で、日によって上下します。通しの予約では途中下車できません。",
            "url": "https://smart-ex.jp/product/plan/service/"
          },
          {
            "name": "倉敷に寄る場合",
            "price": "12,640円〜",
            "text": "京都→倉敷7,470円＋倉敷→広島5,170円（福山乗り換え）。岡山乗り換えだと合計13,410円。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "荷物の一時預かり",
            "price": "600円・800円",
            "text": "3辺120cmまで600円、160cmまで800円。8:00〜20:00。ロッカーの料金は要確認。",
            "url": "https://www.okayama-kanko.jp/spot/detail_10022.html"
          },
          {
            "name": "岡山城・後楽園 共通券",
            "price": "800円",
            "text": "別々だと500円ずつ。路面電車は片道160円。",
            "url": "https://okayama-castle.jp/guide/"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Okayama & Kurashiki MAP',
    titleMain: 'Okayama & Kurashiki',
    titleSub: '岡山と倉敷',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Numbers show the order. The overnight course marks Day 1 and Day 2 in the headings and labels. The stopover starts with just the castle and Korakuen. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (photos of Korakuen, Kibitsu Shrine and Kurashiki, and of Okayama Castle after its renovation, are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
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
    pickNote: 'The places that fit the timetable are selected to start with, and suggested times assume that set. Stations and the tram follow what you pick.',
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
    swCourse: 'Type of trip',
    courseAria: 'Type of trip',
    courseStay: 'Two days, one night\n(Kurashiki by night)',
    courseStop: 'Stop on the way\n(Kyoto/Osaka → Hiroshima)',
    swMode: 'How to go',
    intro: {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Tickets, bags and admission",
      "dealsMore": "See official site or route planner",
      "dealsNote": "Per adult. Checked on Nov 22, 2026 with the official sites and a route planner (25, 28 and 29 November timetables). Reserved-seat prices vary by date.",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose the type of trip",
          "text": "Use the buttons above the list: two days with a night, or a stop on the way. The timetable and numbers change."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that could stop you at the door (bags, tickets, closing days) come first, with times and fees below."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi (apart from Okayama Castle and Okayama Station, put together from official websites and other sources, with photos from Wikimedia Commons)."
    },
    introFor: {
      "stay": {
        "kicker": "Two days and a night from Kyoto or Osaka",
        "h1": "A black castle and a lord’s garden by day; white-walled Kurashiki by night and morning.",
        "lead": "Cross Tsukimi bridge from Okayama Castle and its black-boarded keep to Korakuen, a feudal lord’s garden. Move to Kurashiki late in the afternoon for dinner by the lamp-lit canal, and stay the night. On day 2 walk the quiet white-walled town before the shops open and enter the Ohara Museum as it opens at 9:00. In the afternoon, walk the long corridor at Kibitsu Shrine, then go home to Kyoto or Osaka, or on to Hiroshima.",
        "favName": "The canal at night and in the morning",
        "favText": "Lit until 21:00 (22:00 April–September), and quiet in the morning before the shops open. (Photo: Suicasmo / CC BY-SA 4.0)",
        "favPhoto": [
          "bikan",
          0
        ],
        "who": [
          "Staying by the Kurashiki old quarter is easiest. Around Kurashiki or Okayama Station works too",
          "Hand bags to Nekonote Station at Okayama by 13:30 for delivery to listed hotels (¥1,500)",
          "The Ohara Museum closes on Mondays: if day 2 is a Monday, swap the days",
          "The museum closes at 15:00 from December to February; this plan goes at 9:00, so it works in winter",
          "Boats stop in rain. Online booking opens 30 days ahead; the boat is not in the starting plan",
          "On some holiday periods every Nozomi seat is reserved"
        ],
        "dayHead": "The two days",
        "day": [
          {
            "time": "9:25",
            "area": "Day 1 · Kyoto",
            "title": "Nozomi to Okayama",
            "text": "Arrive 10:25. From Shin-Osaka it is the same train at 9:41. Stow bags, then the tram.",
            "photo": [
              "kyoto",
              0
            ],
            "note": "Shin-Osaka 9:41"
          },
          {
            "time": "11:05",
            "area": "Day 1 · Okayama",
            "title": "Castle, Tsukimi bridge, Korakuen",
            "text": "Over the bridge from castle to garden, then lunch from 13:20 at Shikisai outside the main gate. (Photo: Fjkelfeimvvn / CC BY 3.0)",
            "photo": [
              "korakuen",
              0
            ]
          },
          {
            "time": "15:20",
            "area": "Day 1 · Kurashiki",
            "title": "The hilltop before dark",
            "text": "Drop in at your hotel, then Ivy Square, and look down on the roofs from Achi Shrine at 16:30. (Photo: Zairon / CC BY 4.0)",
            "photo": [
              "achi",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Day 1 · evening",
            "title": "Lamp-lit canal and dinner",
            "text": "Dinner at about 18:15, another walk until the lights go off at 21:00, and a night in Kurashiki. (Photo: ノボホショコロトソ / CC BY 4.0)",
            "photo": [
              "honmachi",
              2
            ],
            "note": "until about 21:00"
          },
          {
            "time": "7:30",
            "area": "Day 2 · Kurashiki",
            "title": "Quiet streets, museum at 9:00",
            "text": "Walk Honmachi, Higashimachi and the canal, then the Ohara Museum as it opens. Lunch at about 11:30. (Photo: Miya.m / CC BY-SA 4.0)",
            "photo": [
              "boat",
              3
            ]
          },
          {
            "time": "14:20",
            "area": "Day 2 · Kibitsu",
            "title": "A National Treasure and a long corridor",
            "text": "The 13:11 to Okayama, then the 13:52 Momotaro line, 15 minutes. Return on the 15:47. (Photo: hiyang.on.flickr / CC BY 2.0)",
            "photo": [
              "kibitsu",
              0
            ]
          },
          {
            "time": "16:20",
            "area": "Day 2 · Okayama",
            "title": "Home, or on to Hiroshima",
            "text": "Kyoto 17:20, Shin-Osaka 17:04. For Hiroshima, the 16:26 arrives 17:02.",
            "photo": [
              "kaeri",
              0
            ]
          }
        ],
        "dealsLead": "Shinkansen fares are per direction. Okayama–Kurashiki is ¥330 each way by JR, Okayama–Kibitsu ¥210, and the tram ¥160 a ride.",
        "deals": [
          {
            "name": "Shinkansen Kyoto–Okayama",
            "price": "¥7,140 one way",
            "text": "Unreserved. Reserved Nozomi: ¥8,100 (25 Nov), ¥8,300 (28 Nov). Shin-Osaka–Okayama: ¥5,610 unreserved, ¥6,460 reserved (25 Nov).",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "On to Hiroshima on day 2",
            "price": "¥5,610 one way",
            "text": "Okayama–Hiroshima unreserved. A through Kyoto–Hiroshima fare ticket (¥6,600) is valid three days with a stopover; buy two express tickets split at Okayama.",
            "url": "https://railway.jr-central.co.jp/ticket-rule/rule05.html"
          },
          {
            "name": "Bags to your hotel",
            "price": "¥1,500",
            "text": "Hand in at Nekonote Station by 13:30; listed hotels receive them by about 17:00.",
            "url": "https://www.okayama-kanko.jp/spot/detail_10022.html"
          },
          {
            "name": "Castle + Korakuen ticket",
            "price": "¥800",
            "text": "¥500 each separately. Castle until 17:30; garden until 17:00 (18:00 from 20 March to September).",
            "url": "https://okayama-castle.jp/guide/"
          },
          {
            "name": "Ohara Museum of Art",
            "price": "¥2,000",
            "text": "Closed Mondays (open on holidays). Until 15:00 Dec–Feb. No photos inside.",
            "url": "https://www.ohara.or.jp/visitor_info/"
          },
          {
            "name": "River boat (optional)",
            "price": "¥1,000",
            "text": "About 20 minutes. Online from 30 days ahead; same-day tickets from 9:00 at Kurashiki-kan.",
            "url": "https://kankou-kurashiki.jp/special/kawafune/"
          }
        ]
      },
      "stop": {
        "kicker": "On the way from Kyoto or Osaka to Hiroshima",
        "h1": "4 hours 40 in Okayama, on the way to Hiroshima.",
        "lead": "Step off the Shinkansen at Okayama, leave your bags at the station and take the tram to Shiroshita. Cross Tsukimi bridge from the black keep of Okayama Castle to Korakuen, have lunch, and catch the 15:06 Nozomi to Hiroshima (15:42). Coming from Kyoto on the 9:25 Nozomi, that gives you 4 hours 40 in Okayama. Kurashiki can replace the castle and garden. Both don’t fit in a stopover; for both, take the overnight course.",
        "favName": "Okayama Castle from Tsukimi bridge",
        "favText": "The black keep above the river, from the bridge to Korakuen (March 2021, before the renovation).",
        "favPhoto": [
          "tsukimi",
          0
        ],
        "who": [
          "3 hours: Korakuen only. 4 hours 40: castle, garden and lunch",
          "5½ hours: Kurashiki’s museum and old quarter instead (Hiroshima 16:27). Both take 9 hours or more, so stay overnight",
          "A through smartEX booking allows no stopover: split it at Okayama",
          "One paper fare ticket to Hiroshima allows a stopover; buy two express tickets, split at Okayama",
          "Bag storage just outside the Shinkansen gates: until 20:00, up to 160 cm (¥600 or ¥800)",
          "Bags over 160 cm need a reserved baggage seat and are not allowed in unreserved cars"
        ],
        "dayHead": "The stopover (Okayama only)",
        "day": [
          {
            "time": "9:25",
            "area": "Kyoto",
            "title": "Nozomi to Okayama",
            "text": "Arrive 10:25. From Shin-Osaka, the same train at 9:41. Your express ticket runs to Okayama.",
            "photo": [
              "kyoto",
              0
            ],
            "note": "Shin-Osaka 9:41"
          },
          {
            "time": "10:25",
            "area": "Okayama Sta.",
            "title": "Bags first",
            "text": "Nekonote Station or the lockers, just outside the gates. The 10:44 tram reaches Shiroshita at 10:52.",
            "photo": [
              "okayamaeki",
              0
            ]
          },
          {
            "time": "11:05",
            "area": "Okayama Castle",
            "title": "The keep and Tsukimi bridge",
            "text": "See the keep, then look back at it from the bridge.",
            "photo": [
              "tsukimi",
              0
            ]
          },
          {
            "time": "12:15",
            "area": "Korakuen",
            "title": "An hour in the garden, then lunch",
            "text": "From 13:20 at Shikisai outside the main gate. The 14:25 tram back. (Photo: Fjkelfeimvvn / CC BY 3.0)",
            "photo": [
              "korakuen",
              0
            ]
          },
          {
            "time": "15:06",
            "area": "Okayama Sta.",
            "title": "Nozomi to Hiroshima",
            "text": "Arrive 15:42, with the late afternoon left for Hiroshima.",
            "photo": [
              "kaeri",
              0
            ],
            "note": "Hiroshima 15:42"
          }
        ],
        "dealsLead": "Getting off once costs more than riding through. These are totals by way of buying; side trips are extra.",
        "deals": [
          {
            "name": "Kyoto → Okayama → Hiroshima (through fare)",
            "price": "¥12,530",
            "text": "Fare ¥6,600 + unreserved express ¥3,400 + ¥2,530. Section by section: ¥12,750. Without stopping: ¥10,770.",
            "url": "https://railway.jr-central.co.jp/ticket-rule/rule05.html"
          },
          {
            "name": "Shin-Osaka → Okayama → Hiroshima (through fare)",
            "price": "¥10,780",
            "text": "Fare ¥5,720 + unreserved express ¥2,530 + ¥2,530. By section: ¥11,220. Without stopping: ¥9,890.",
            "url": "https://railway.jr-central.co.jp/ticket-rule/rule05.html"
          },
          {
            "name": "Two smartEX bookings",
            "price": "¥14,160",
            "text": "From Kyoto (¥7,900 + ¥6,260); ¥12,520 from Shin-Osaka. Reserved Nozomi in the regular season; varies by date. A through booking allows no stopover.",
            "url": "https://smart-ex.jp/product/plan/service/"
          },
          {
            "name": "Stopping in Kurashiki",
            "price": "from ¥12,640",
            "text": "Kyoto–Kurashiki ¥7,470 + Kurashiki–Hiroshima ¥5,170 via Fukuyama. ¥13,410 changing at Okayama.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Bag storage",
            "price": "¥600 / ¥800",
            "text": "Up to 120 cm ¥600, up to 160 cm ¥800. 8:00–20:00. Locker prices not confirmed.",
            "url": "https://www.okayama-kanko.jp/spot/detail_10022.html"
          },
          {
            "name": "Castle + Korakuen ticket",
            "price": "¥800",
            "text": "¥500 each separately. The tram is ¥160 each way.",
            "url": "https://okayama-castle.jp/guide/"
          }
        ]
      }
    }
  }
};
