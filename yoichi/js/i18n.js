/* Page texts in Japanese and English.
   Toshi 個人のマップ。余市（札幌から日帰り）。写真はすべて Wikimedia Commons（だれかが行った・食べたとは書かない）。
   コースは2つ（一覧の上のボタン）：late＝4月中旬〜12月中旬（data/routes/yoichi.json）、early＝冬・12月中旬〜4月上旬（yoichi-winter.json）。
   どちらで開くかは日付で決まる（scripts/sync_yoichi.py の WINTER_FROM / WINTER_TO）。intro はどのコースにも共通の項目で、
   コースで変わる項目は introFor[コース] が app.js で上書きされる。写真は [スポットの id, 写真の番号]（冬の余市駅は雪の写真が0番）。
   時刻・料金は2026年11月27日に確認（出典は data/routes/yoichi.json の sources）。直すときはこのファイルを直接直してよい */
window.YOICHI_I18N = {
  ja: {
    htmlLang: "ja",
    docTitle: "余市 札幌から日帰り Yoichi MAP",
    titleMain: "余市",
    titleSub: "Yoichi, a day trip from Sapporo",
    howto: "使い方",
    allMaps: "← マップ一覧",
    home: "マップ一覧",
    tabMap: "地図",
    menu: "メニュー",
    list: "一覧",
    listHead: "スポット一覧",
    listNote: "番号は回る順番です。電車の時刻は平日も土曜も同じです。点線は順番を示す線で、実際の道ではありません。",
    back: "一覧",
    close: "閉じる",
    showAll: "全体を表示",
    seeDetails: "詳しく見る",
    prevPhoto: "前の写真",
    nextPhoto: "次の写真",
    suggested: "おすすめの時間：",
    suggestedLabel: "めやすの時間",
    gmapsOne: "Googleマップで開く",
    gmapsMany: "Googleマップ：",
    copy: "このスポットのリンクをコピー",
    copied: "コピーしました",
    spot1Howto: "このマップの使い方を見る",
    credit: "文章：Toshi／写真：Wikimedia Commons（撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: "写真：",
    loadError: "地図データを読み込めませんでした。再読み込みしてください。",
    hours: "時間",
    fee: "料金",
    train: "電車",
    bus: "バス",
    closed: "休み",
    cash: "現金を用意してください",
    checked: "{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。",
    unchecked: "{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。",
    checkedDate: "2026年11月27日",
    noticeHead: "お知らせ",
    more: "詳しく",
    linkKinds: {"official": "公式サイト", "timetable": "時刻表", "info": "案内"},
    nextRoute: "次のスポットへの行き方",
    locate: "現在地",
    locating: "現在地を探しています…",
    locateErr: "現在地を取得できませんでした。端末の位置情報の設定を確認してください。",
    visitOff: "行ったら印を付ける",
    visitOn: "行った！",
    progress: "{n} / {t} か所 行った",
    reset: "リセット",
    resetAsk: "もう一度押すと、行った印をすべて消します",
    modeAria: "回り方",
    modeAll: "全部回る",
    modePick: "選んで回る",
    pickNote: "最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。札幌駅・余市駅・晩ごはんと帰りは、どの組み合わせでも入ります。",
    pickCount: "選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）",
    pickEmpty: "まだ選んでいません。下の一覧から、行きたい場所を選んでください。",
    pickAll: "すべて選ぶ",
    pickNone: "すべて外す",
    pickOff: "行きたい",
    pickOn: "行く",
    autoTag: "全員共通",
    autoOff: "今回は通りません",
    seasonHead: "季節営業の可能性",
    hintHead: "あなたのルートでは",
    swCourse: "季節",
    courseAria: "季節",
    courseLate: "4月中旬〜12月中旬\n浜の史跡も",
    courseEarly: "冬\n12月中旬〜4月上旬",
    swMode: "回り方",
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "電車・バス・入場料",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月27日に、各施設の公式サイトと乗換案内（12月3日・5日のダイヤ）で確認しました。タクシー代は別です。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "季節を選ぶ",
          "text": "一覧の上のボタンで「4月中旬〜12月中旬」と「冬」を選べます。最初は、その日の日付に合う方で開きます。時間割と番号が変わります。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、休みの日・予約・タトゥー・冬の注意など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（公式サイトなどの情報と、Wikimedia Commons の写真で紹介しています）。"
    },
    introFor: {
      "late": {
        "kicker": "札幌から日帰り（4月中旬〜12月中旬）",
        "h1": "朝はウイスキーの蒸溜所、午後はワインとニシン漁の浜。最後は温泉とすし。",
        "lead": "余市（よいち）は、ニッカの石造りの蒸溜所と、ニシン漁で栄えた浜の町。札幌8:41の電車で出て、予約しておいた蒸溜所のツアーに参加し、敷地の中のレストランでお昼。タクシーでワイナリーへ行って飲み比べ、ニシン漁で栄えた浜の漁場と運上家、シリパ岬の見える浜を歩きます。駅の近くの温泉と回転ずしで1日を終えて、19:26の電車で札幌20:41着。ツアーの予約、休みの曜日、きっぷの買い方も先に書いてあります。",
        "favName": "ニッカの石造りの蒸溜所",
        "favText": "とんがり屋根のキルン塔と、石の棟が並ぶ敷地。（写真：さかおり / CC BY-SA 4.0）",
        "favPhoto": [
          "nikka",
          0
        ],
        "who": [
          "蒸溜所のツアーは予約制（公式の予約ページ、英語あり、4週間前から）。案内は日本語だけ",
          "2026年12月〜2027年1月は無料ツアーなし、有料のセミナーだけ（20歳以上・その日に運転しない人）",
          "福原漁場・運上家は月曜休み。2026年は12月13日まで",
          "余市ワイナリーは火曜休み。行き帰りはタクシーで",
          "小樽〜余市でICカードが使えるかは未確認。札幌できっぷを買うのが確実",
          "積丹の神威岬へは路線バスが美国（びくに）までで、このマップには入れていません"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "8:41",
            "area": "札幌",
            "title": "小樽で乗り換えて余市へ",
            "text": "余市10:00着。蒸溜所は駅から歩いて5分。（写真：MaedaAkihiko / CC0）",
            "photo": [
              "eki",
              0
            ],
            "note": "余市10:00"
          },
          {
            "time": "10:05",
            "area": "余市",
            "title": "蒸溜所のツアーとお昼",
            "text": "予約した回に。お昼は敷地の中のレストランで。（写真：さかおり / CC BY-SA 4.0）",
            "photo": [
              "nikka",
              1
            ]
          },
          {
            "time": "13:10",
            "area": "黒川町",
            "title": "ワイナリーで飲み比べ",
            "text": "カフェで余市ワインの3杯セット。（写真：daita saru / CC BY 2.0）",
            "photo": [
              "winery",
              0
            ]
          },
          {
            "time": "14:30",
            "area": "浜中町",
            "title": "ニシン漁の漁場",
            "text": "番屋と蔵が当時の姿で残ります。（写真：さかおり / CC BY-SA 4.0）",
            "photo": [
              "fuku",
              0
            ]
          },
          {
            "time": "15:35",
            "area": "入舟町",
            "title": "運上家とモイレの浜",
            "text": "1853年の建物と、湾の向こうのシリパ岬。（写真：さかおり / CC BY-SA 4.0）",
            "photo": [
              "unjo",
              0
            ]
          },
          {
            "time": "16:50",
            "area": "入舟町",
            "title": "温泉",
            "text": "檜の露天風呂とサウナ、500円。（写真：heriheri / CC BY 3.0）",
            "photo": [
              "onsen",
              0
            ]
          },
          {
            "time": "18:10",
            "area": "大川町",
            "title": "回転ずし、19:26の電車で札幌へ",
            "text": "余市・小樽の沿岸の魚。（写真：Opqr / CC BY-SA 4.0）",
            "photo": [
              "kaeri",
              0
            ],
            "note": "札幌20:41"
          }
        ],
        "dealsLead": "電車は札幌〜余市が片道1,380円。蒸溜所のツアーは無料（予約制）、漁場・運上家は1か所300円、温泉は500円。ワイナリーへの行き帰りはタクシーです。",
        "deals": [
          {
            "name": "JR 札幌→余市",
            "price": "1,380円",
            "text": "小樽で乗り換え、1時間20分ほど。JR北海道レールパスで乗れます。帰りも同じ運賃です。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "高速バス 札幌駅前→余市",
            "price": "1,290円",
            "text": "乗り換えなし、予約なし、交通系ICカード可。往復2,420円。",
            "url": "https://www.chuo-bus.co.jp/highway/?t=39&ope=list&o=1"
          },
          {
            "name": "ニッカ 余市蒸溜所 ガイドツアー",
            "price": "無料",
            "text": "予約制・日本語のみ。12〜1月は有料セミナーだけ（11月の案内では3,000円・現金）。",
            "url": "https://reserva.be/nikkayoichi/news"
          },
          {
            "name": "福原漁場・運上家・水産博物館",
            "price": "各300円",
            "text": "4施設の共通券（フゴッペ洞窟を含む）は960円、2日間有効。",
            "url": "https://www.town.yoichi.hokkaido.jp/kurashi/kurashinojouhou/kyouiku-bunka/bunkazai-kaikan.html"
          },
          {
            "name": "余市川温泉 宇宙の湯",
            "price": "500円",
            "text": "フェイスタオル250円。カード・QR決済可。タトゥーは受付で確認。",
            "url": "https://yoichigawa.com/free/ohuro"
          }
        ]
      },
      "early": {
        "kicker": "札幌から日帰り（冬：12月中旬〜4月上旬）",
        "h1": "雪の蒸溜所でウイスキー、ワイナリーで飲み比べ。白い岬を見て、温泉とすし。",
        "lead": "雪の積もった蒸溜所、ワインの飲み比べ、浜から見る白いシリパ岬。冬は浜の漁場や博物館が閉まるので、開いている場所をつないだ1日です。札幌8:41の電車で余市へ。12〜1月はニッカの蒸溜所の有料セミナー（予約制）、蒸溜所でお昼。タクシーでワイナリーへ行き、明るいうちに雪のシリパ岬を浜から見て、温泉で温まってから回転ずし。18:35の電車で札幌19:58着です。",
        "favName": "ニッカの石造りの蒸溜所",
        "favText": "とんがり屋根のキルン塔と、石の棟が並ぶ敷地。（写真：さかおり / CC BY-SA 4.0）",
        "favPhoto": [
          "nikka",
          0
        ],
        "who": [
          "蒸溜所は12月23日〜1月7日休み。その週は小樽のマップがおすすめ",
          "12〜1月はセミナーだけ（有料・予約制・20歳以上・その日に運転しない人）。予約ページは英語あり",
          "余市ワイナリーは火曜休み、1〜4月は火・水曜休み",
          "歩道は雪と氷。底に溝の深い、滑りにくい靴で",
          "12月は16時ごろ日没。浜へは明るいうちに",
          "温泉のタトゥーの決まりは公式サイトに書いていません（受付で確認）"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "8:41",
            "area": "札幌",
            "title": "小樽で乗り換えて余市へ",
            "text": "余市10:00着。（写真：スミス1919 / CC BY 4.0）",
            "photo": [
              "eki",
              0
            ],
            "note": "余市10:00"
          },
          {
            "time": "10:30",
            "area": "余市",
            "title": "蒸溜所のセミナーとお昼",
            "text": "12〜1月は有料のセミナー。お昼は敷地の中のレストランで。（写真：さかおり / CC BY-SA 4.0）",
            "photo": [
              "nikka",
              1
            ]
          },
          {
            "time": "13:10",
            "area": "黒川町",
            "title": "ワイナリーで飲み比べ",
            "text": "カフェで余市ワインの3杯セット。（写真：daita saru / CC BY 2.0）",
            "photo": [
              "winery",
              0
            ]
          },
          {
            "time": "14:30",
            "area": "入舟町",
            "title": "モイレの浜からシリパ岬",
            "text": "雪の浜には下りず、入り口から。（写真：Karl Trautman / CC BY 4.0）",
            "photo": [
              "moire",
              0
            ]
          },
          {
            "time": "15:15",
            "area": "入舟町",
            "title": "温泉で温まる",
            "text": "檜の露天風呂とサウナ、500円。（写真：heriheri / CC BY 3.0）",
            "photo": [
              "onsen",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "大川町",
            "title": "回転ずし、18:35の電車で札幌へ",
            "text": "ゆっくりなら19:26発。（写真：スミス1919 / CC BY-SA 4.0）",
            "photo": [
              "kaeri",
              1
            ],
            "note": "札幌19:58"
          }
        ],
        "dealsLead": "電車は札幌〜余市が片道1,380円。蒸溜所のセミナーは有料（予約制）、温泉は500円。ワイナリーと浜への移動はタクシーです。",
        "deals": [
          {
            "name": "JR 札幌→余市",
            "price": "1,380円",
            "text": "小樽で乗り換え、1時間20分ほど。JR北海道レールパスで乗れます。帰りも同じ運賃です。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "高速バス 札幌駅前→余市",
            "price": "1,290円",
            "text": "乗り換えなし、予約なし、交通系ICカード可。往復2,420円。",
            "url": "https://www.chuo-bus.co.jp/highway/?t=39&ope=list&o=1"
          },
          {
            "name": "ニッカ キーモルトセミナー（12〜1月）",
            "price": "予約ページで",
            "text": "約90分。11月の案内では3,000円・現地で現金。20歳以上・その日に運転しない人。",
            "url": "https://reserva.be/nikkayoichi/news"
          },
          {
            "name": "余市川温泉 宇宙の湯",
            "price": "500円",
            "text": "フェイスタオル250円。カード・QR決済可。タトゥーは受付で確認。",
            "url": "https://yoichigawa.com/free/ohuro"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: "en",
    docTitle: "Yoichi MAP: a day trip from Sapporo",
    titleMain: "Yoichi",
    titleSub: "余市 札幌から日帰り",
    howto: "How to use",
    allMaps: "← All maps",
    home: "All maps",
    tabMap: "Map",
    menu: "Menu",
    list: "Spots",
    listHead: "All spots",
    listNote: "Numbers show the order. Train times are the same on weekdays and Saturdays. The dotted line shows the order, not the actual path.",
    back: "List",
    close: "Close",
    showAll: "Show all",
    seeDetails: "See details",
    prevPhoto: "Previous photo",
    nextPhoto: "Next photo",
    suggested: "Suggested time: ",
    suggestedLabel: "Rough time",
    gmapsOne: "Open in Google Maps",
    gmapsMany: "Google Maps: ",
    copy: "Copy link to this spot",
    copied: "Link copied",
    spot1Howto: "How to use this map",
    credit: "Text: Toshi / Photos: Wikimedia Commons (the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: "Photo: ",
    loadError: "Could not load the map data. Please reload.",
    hours: "Hours",
    fee: "Fee",
    train: "Train",
    bus: "Bus",
    closed: "Closed",
    cash: "Bring cash",
    checked: "Checked on official websites and a route planner on {d}. Details can change, so please check before you go.",
    unchecked: "Could not be confirmed on an official website as of {d}. Please check the latest information before you go.",
    checkedDate: "Nov 27, 2026",
    noticeHead: "Note",
    more: "Details",
    linkKinds: {"official": "Official site", "timetable": "Timetable", "info": "Info"},
    nextRoute: "Directions to the next stop",
    locate: "My location",
    locating: "Finding your location…",
    locateErr: "Could not get your location. Please check your location settings.",
    visitOff: "Mark as visited",
    visitOn: "Visited!",
    progress: "{n} of {t} visited",
    reset: "Reset",
    resetAsk: "Tap again to clear all visited marks",
    modeAria: "How to go",
    modeAll: "Full route",
    modePick: "Choose stops",
    pickNote: "The places that fit the timetable are selected to start with, and suggested times assume that set. Sapporo Station, Yoichi Station and dinner with the train back are always included.",
    pickCount: "{n} places chosen · {t} stops in your route (incl. the shared ones)",
    pickEmpty: "Nothing chosen yet. Pick the places you want from the list below.",
    pickAll: "Choose all",
    pickNone: "Clear all",
    pickOff: "Want to go",
    pickOn: "Going",
    autoTag: "Everyone",
    autoOff: "Not on your route",
    seasonHead: "Possibly seasonal",
    hintHead: "On your route",
    swCourse: "Season",
    courseAria: "Season",
    courseLate: "Mid-Apr – mid-Dec\nwith the shore sites",
    courseEarly: "Winter\nmid-Dec – early Apr",
    swMode: "How to go",
    intro: {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Trains, buses and admission",
      "dealsMore": "See official site or route planner",
      "dealsNote": "Per adult. Checked on Nov 27, 2026 with the official sites and a route planner (3 and 5 December timetables). Taxi fares are extra.",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose the season",
          "text": "Use the buttons above the list: mid-April to mid-December, or winter. The map opens on the one that fits today’s date. The timetable and numbers change."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that could stop you at the door (closing days, bookings, tattoos, winter tips) come first, with times and fees below."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi, put together from official websites and other sources, with photos from Wikimedia Commons."
    },
    introFor: {
      "late": {
        "kicker": "A day trip from Sapporo (mid-April to mid-December)",
        "h1": "Whisky in the morning, then wine and the old herring shore. A hot spring and sushi to end.",
        "lead": "Yoichi is a seaside town with Nikka’s stone whisky distillery and an old herring-fishing shore. Take the 8:41 train for a booked distillery tour and lunch in the restaurant on the grounds. A taxi to the winery for a tasting flight, then the herring fishery, the Unjoya trading post and the beach facing Cape Shiripa. Finish with a hot spring and conveyor-belt sushi near the station, and the 19:26 train back (Sapporo 20:41). Tour booking, closing days and which ticket to buy are covered up front.",
        "favName": "Nikka’s stone distillery",
        "favText": "Pagoda-roofed kiln towers and stone buildings. (Photo: さかおり / CC BY-SA 4.0)",
        "favPhoto": [
          "nikka",
          0
        ],
        "who": [
          "Distillery tours need a booking (official booking site in English, four weeks ahead). Tours are in Japanese only",
          "December 2026–January 2027: no free tours, only a paid seminar (20+, not driving that day)",
          "The fishery and Unjoya close on Mondays; open until 13 December in 2026",
          "Yoichi Winery closes on Tuesdays. Go by taxi",
          "Not confirmed whether IC cards work between Otaru and Yoichi; buy a ticket in Sapporo",
          "Cape Kamui in Shakotan isn’t included: buses from Yoichi only go as far as Bikuni"
        ],
        "dayHead": "Your day",
        "day": [
          {
            "time": "8:41",
            "area": "Sapporo",
            "title": "Change at Otaru for Yoichi",
            "text": "Yoichi 10:00; the distillery is 5 minutes’ walk. (Photo: MaedaAkihiko / CC0)",
            "photo": [
              "eki",
              0
            ],
            "note": "Yoichi 10:00"
          },
          {
            "time": "10:05",
            "area": "Yoichi",
            "title": "Distillery tour and lunch",
            "text": "Your booked slot, then lunch on site. (Photo: さかおり / CC BY-SA 4.0)",
            "photo": [
              "nikka",
              1
            ]
          },
          {
            "time": "13:10",
            "area": "Kurokawa",
            "title": "A wine flight at the winery",
            "text": "Three glasses of Yoichi wine in the café. (Photo: daita saru / CC BY 2.0)",
            "photo": [
              "winery",
              0
            ]
          },
          {
            "time": "14:30",
            "area": "Hamanaka",
            "title": "The herring fishery",
            "text": "Bunkhouse and storehouses as they were. (Photo: さかおり / CC BY-SA 4.0)",
            "photo": [
              "fuku",
              0
            ]
          },
          {
            "time": "15:35",
            "area": "Irifune",
            "title": "The Unjoya and Moire beach",
            "text": "An 1853 building and Cape Shiripa across the bay. (Photo: さかおり / CC BY-SA 4.0)",
            "photo": [
              "unjo",
              0
            ]
          },
          {
            "time": "16:50",
            "area": "Irifune",
            "title": "Hot spring",
            "text": "Cedar outdoor bath and sauna, ¥500. (Photo: heriheri / CC BY 3.0)",
            "photo": [
              "onsen",
              0
            ]
          },
          {
            "time": "18:10",
            "area": "Okawa",
            "title": "Sushi, then the 19:26 to Sapporo",
            "text": "Fish from the Yoichi and Otaru coast. (Photo: Opqr / CC BY-SA 4.0)",
            "photo": [
              "kaeri",
              0
            ],
            "note": "Sapporo 20:41"
          }
        ],
        "dealsLead": "Trains: ¥1,380 each way between Sapporo and Yoichi. The distillery tour is free (booking needed), the fishery and Unjoya ¥300 each, the hot spring ¥500. Taxis to and from the winery are extra.",
        "deals": [
          {
            "name": "JR Sapporo → Yoichi",
            "price": "¥1,380",
            "text": "Change at Otaru; about 1 hr 20 min. Covered by the JR Hokkaido Rail Pass. Same fare back.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Highway bus Sapporo → Yoichi",
            "price": "¥1,290",
            "text": "No change, no booking, IC cards work. Return ¥2,420.",
            "url": "https://www.chuo-bus.co.jp/highway/?t=39&ope=list&o=1"
          },
          {
            "name": "Nikka Yoichi guided tour",
            "price": "Free",
            "text": "Booking needed, Japanese only. Dec–Jan: paid seminar only (¥3,000 cash in the November notice).",
            "url": "https://reserva.be/nikkayoichi/news"
          },
          {
            "name": "Fukuhara fishery, Unjoya, fisheries museum",
            "price": "¥300 each",
            "text": "Combined ticket for four sites (incl. Fugoppe Cave) ¥960, valid two days.",
            "url": "https://www.town.yoichi.hokkaido.jp/kurashi/kurashinojouhou/kyouiku-bunka/bunkazai-kaikan.html"
          },
          {
            "name": "Uchu no Yu hot spring",
            "price": "¥500",
            "text": "Face towel ¥250. Cards and QR payments accepted. Ask about tattoos at reception.",
            "url": "https://yoichigawa.com/free/ohuro"
          }
        ]
      },
      "early": {
        "kicker": "A day trip from Sapporo (winter: mid-December to early April)",
        "h1": "Whisky at a snowy distillery, a wine flight, a white cape, then a hot spring and sushi.",
        "lead": "A distillery under snow, a wine flight, and Cape Shiripa white across the bay. In winter the fishery and museums close, so this day links the places that stay open. Take the 8:41 train to Yoichi; in December–January the Nikka distillery runs a paid seminar (booking needed), then lunch on site. A taxi to the winery, Cape Shiripa in the snow from the beach while it is light, a hot soak and conveyor-belt sushi before the 18:35 train (Sapporo 19:58).",
        "favName": "Nikka’s stone distillery",
        "favText": "Pagoda-roofed kiln towers and stone buildings. (Photo: さかおり / CC BY-SA 4.0)",
        "favPhoto": [
          "nikka",
          0
        ],
        "who": [
          "The distillery closes 23 December–7 January; that week, the Otaru map is the better day",
          "December–January: paid seminar only (booking, 20+, not driving that day). The booking site has English",
          "Yoichi Winery closes on Tuesdays, and also Wednesdays from January to April",
          "Pavements are snow and ice. Wear boots with deep-tread soles",
          "Sunset is around 16:00 in December. Visit the beach while it is light",
          "The hot spring’s website says nothing about tattoos (ask at reception)"
        ],
        "dayHead": "Your day",
        "day": [
          {
            "time": "8:41",
            "area": "Sapporo",
            "title": "Change at Otaru for Yoichi",
            "text": "Yoichi 10:00. (Photo: スミス1919 / CC BY 4.0)",
            "photo": [
              "eki",
              0
            ],
            "note": "Yoichi 10:00"
          },
          {
            "time": "10:30",
            "area": "Yoichi",
            "title": "Distillery seminar and lunch",
            "text": "A paid seminar in December–January, then lunch on site. (Photo: さかおり / CC BY-SA 4.0)",
            "photo": [
              "nikka",
              1
            ]
          },
          {
            "time": "13:10",
            "area": "Kurokawa",
            "title": "A wine flight at the winery",
            "text": "Three glasses of Yoichi wine in the café. (Photo: daita saru / CC BY 2.0)",
            "photo": [
              "winery",
              0
            ]
          },
          {
            "time": "14:30",
            "area": "Irifune",
            "title": "Cape Shiripa from Moire beach",
            "text": "Look from the entrance; don’t walk out on the snow. (Photo: Karl Trautman / CC BY 4.0)",
            "photo": [
              "moire",
              0
            ]
          },
          {
            "time": "15:15",
            "area": "Irifune",
            "title": "Warm up in a hot spring",
            "text": "Cedar outdoor bath and sauna, ¥500. (Photo: heriheri / CC BY 3.0)",
            "photo": [
              "onsen",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Okawa",
            "title": "Sushi, then the 18:35 to Sapporo",
            "text": "Or the 19:26 for a slower evening. (Photo: スミス1919 / CC BY-SA 4.0)",
            "photo": [
              "kaeri",
              1
            ],
            "note": "Sapporo 19:58"
          }
        ],
        "dealsLead": "Trains: ¥1,380 each way between Sapporo and Yoichi. The distillery seminar is paid (booking needed) and the hot spring is ¥500. Taxis to the winery and the beach are extra.",
        "deals": [
          {
            "name": "JR Sapporo → Yoichi",
            "price": "¥1,380",
            "text": "Change at Otaru; about 1 hr 20 min. Covered by the JR Hokkaido Rail Pass. Same fare back.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Highway bus Sapporo → Yoichi",
            "price": "¥1,290",
            "text": "No change, no booking, IC cards work. Return ¥2,420.",
            "url": "https://www.chuo-bus.co.jp/highway/?t=39&ope=list&o=1"
          },
          {
            "name": "Nikka Key Malt Seminar (Dec–Jan)",
            "price": "See booking site",
            "text": "About 90 minutes. ¥3,000 cash on the day in the November notice. 20+ and not driving that day.",
            "url": "https://reserva.be/nikkayoichi/news"
          },
          {
            "name": "Uchu no Yu hot spring",
            "price": "¥500",
            "text": "Face towel ¥250. Cards and QR payments accepted. Ask about tattoos at reception.",
            "url": "https://yoichigawa.com/free/ohuro"
          }
        ]
      }
    }
  }
};
