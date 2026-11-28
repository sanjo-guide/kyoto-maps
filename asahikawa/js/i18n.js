/* Page texts in Japanese and English.
   Toshi 個人のマップ。旭山動物園と旭川の町（起点は旭川駅のまわりのホテル。札幌から特急で日帰りの人向けの時刻も補足）。
   コースは季節で2つ（一覧の上のボタン）：early＝冬（動物園の冬期開園 11/11〜4/7。data/routes/asahikawa-winter.json）、
   late＝雪のない季節（夏期開園 4/29〜11/3。asahikawa.json）。最初はその日の日付に合う方で開く（scripts/sync_asahikawa.py）。
   1 旭川駅・2 旭山動物園・3 男山・4 髙砂酒造・5 三浦綾子記念文学館と見本林・6 買物公園とラーメン・7 常磐公園と旭橋・8 5・7小路ふらりーと・9 旭川駅（帰り）。
   紹介ページは intro に introFor[コース] を上書きして使う。写真は [スポットの id, 写真の番号]。
   写真はすべて Wikimedia Commons（オーナーはまだ北海道の写真を持っていない。行った・食べたと書かない）。
   時刻・料金は2026年11月28日に確認（出典は data/routes/asahikawa*.json の sources。データは scripts/build_asahikawa_data.py）。
   このファイルは直接直してよい。直したら scripts/sync_asahikawa.py の bump を上げてから sync を実行する */
window.ASAHIKAWA_I18N = {
  ja: {
    htmlLang: "ja",
    docTitle: "旭山動物園と旭川の町 旭川駅から1日 Asahikawa MAP",
    titleMain: "旭山動物園と旭川の町",
    titleSub: "Asahiyama Zoo & Asahikawa",
    howto: "使い方",
    allMaps: "← マップ一覧",
    home: "マップ一覧",
    tabMap: "地図",
    menu: "メニュー",
    list: "一覧",
    listHead: "スポット一覧",
    listNote: "番号は回る順番です。最初は、時間割どおりに回れる場所が選ばれています。午後の3〜5番（男山・髙砂酒造・文学館）は、どれか1つを選ぶ場所です。点線は順番を示す線で、実際の道ではありません。",
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
    credit: "文章：Toshi<br>写真：Wikimedia Commons（撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: "写真：",
    loadError: "地図データを読み込めませんでした。再読み込みしてください。",
    hours: "時間",
    fee: "料金",
    train: "電車",
    bus: "バス",
    walk: "歩く",
    pay: "支払い",
    reserve: "予約",
    tattoo: "タトゥー",
    season: "季節",
    closed: "休み",
    cash: "現金を用意してください",
    checked: "{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。",
    unchecked: "{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。",
    checkedDate: "2026年11月28日",
    noticeHead: "お知らせ",
    more: "詳しく",
    linkKinds: {
      "official": "公式サイト",
      "timetable": "時刻表",
      "info": "案内"
    },
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
    pickNote: "最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。旭川駅（出発と帰り）は、どの組み合わせでも入ります。",
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
    courseEarly: "冬\n11月11日〜4月7日",
    courseLate: "雪のない季節\n4月29日〜11月3日",
    swMode: "回り方",
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "バス・入園料・特急",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月28日に、各施設の公式サイト、旭川電気軌道の時刻表、乗換案内（12月3日・5日のダイヤ）で確認しました。食事代は別です。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "季節を選ぶ",
          "text": "一覧の上のボタンで「冬」と「雪のない季節」を選べます。最初は、その日の日付に合う方で開きます。動物園の開く時間が違うので、時間割が変わります。"
        },
        {
          "title": "午後の行き先を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと、男山・髙砂酒造・文学館などを入れ替えられ、そのときの行き方がひとことで出ます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、休みの日・バスの払い方・冬の服装など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。ラーメンの店は6番、新子焼きの店は8番の中にあります。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（公式サイトなどの情報と、Wikimedia Commons の写真で紹介しています）。"
    },
    introFor: {
      "early": {
        "kicker": "旭川駅から1日（冬：11月11日〜4月7日）",
        "h1": "雪の上をペンギンが歩く動物園。暗くなったら、酒蔵とラーメンと焼き鳥の小路。",
        "lead": "冬の旭山動物園（あさひやまどうぶつえん）は10:30から15:30まで。旭川駅前9:40のバスで行くと、11:00のペンギンの散歩に間に合います。14:10のバスで町に戻ったら、歩いて行ける髙砂酒造へ。16時には暗くなるので、あとは買物公園で旭川ラーメン、夜は焼き鳥の煙が流れる「5・7小路ふらりーと」で新子焼き。旭川に泊まる人も、札幌から特急で日帰りする人も使える時間割です。",
        "favName": "ペンギンの散歩",
        "favText": "雪が積もってから3月中旬ごろまで、11:00と14:30。キングペンギンが、目の前の雪道を歩いていきます。（写真：欅 (Keyaki) / CC BY-SA 3.0）",
        "favPhoto": [
          "zoo",
          0
        ],
        "who": [
          "動物園は12月30日〜1月1日が休み。ペンギンの散歩は雪が積もってから（例年12月下旬ごろ〜）で、始まる日は動物園のSNSで発表されます",
          "1月の旭川は平年で最高−3.3℃・最低−11.7℃。ダウン、帽子、手袋、すべりにくい靴を。動物園は坂が多く、外に3時間います",
          "動物園へのバスは片道670円で、SuicaなどのICカードは使えません。現金か、駅前のバス案内所の券売機のきっぷで",
          "動物園は再入園ができません。お昼は園内の食堂で",
          "日の入りは12月が16時前、2月が16:45ごろ。外を歩く場所は明るいうちに回る順番にしてあります",
          "札幌から日帰りなら、札幌8:00発の特急で旭川9:25。帰りは20:00発か21:00発、最終は22:00発。特急は全席指定（片道5,440円）",
          "2月6日〜11日は旭川冬まつり（常磐公園と旭橋の河畔）。2月5日〜7日は動物園が夜8時半まで開きます"
        ],
        "dayHead": "1日の流れ（冬。平日・土日祝とも）",
        "day": [
          {
            "time": "9:40",
            "area": "旭川駅",
            "title": "駅前の6番のりばからバス",
            "text": "動物園まで約40分、670円を現金で。札幌8:00発の特急で来た人も、このバスに乗れます。（写真：Nagono / CC BY-SA 3.0）",
            "photo": [
              "eki",
              1
            ]
          },
          {
            "time": "10:22",
            "area": "旭山動物園",
            "title": "11:00のペンギンの散歩へ",
            "text": "開園は10:30。散歩のあとは、ぺんぎん館の水中トンネル、あざらし館、ほっきょくぐま館。お昼は園内で。（写真：なよろ / CC BY-SA 4.0）",
            "photo": [
              "zoo",
              1
            ]
          },
          {
            "time": "14:10",
            "area": "動物園 → 旭川駅",
            "title": "バスで町へ戻る",
            "text": "駅に14:54。14:30の散歩も見る日は15:10のバスで。（写真：pelican from Tokyo, Japan / CC BY-SA 2.0）",
            "photo": [
              "zoo",
              3
            ]
          },
          {
            "time": "15:15",
            "area": "髙砂酒造",
            "title": "明治の酒蔵で試飲",
            "text": "駅から歩いて15分。17:00まで。男山や文学館に入れ替えることもできます。（写真：Jennifer Feuchter / CC BY 2.0）",
            "photo": [
              "takasago",
              0
            ]
          },
          {
            "time": "16:20",
            "area": "買物公園",
            "title": "暗くなった通りを歩いて、旭川ラーメン",
            "text": "梅光軒は17:00から夜の営業。山頭火は午後も開いています。（写真：Koji1970327 / CC BY-SA 3.0）",
            "photo": [
              "kaimono",
              2
            ]
          },
          {
            "time": "18:00",
            "area": "5・7小路ふらりーと",
            "title": "焼き鳥の小路で新子焼き",
            "text": "若鶏の半身を炭火で焼いた旭川の名物。ぎんねこは月曜休みです。（写真：久保竜弥 / CC BY-SA 4.0）",
            "photo": [
              "furari",
              0
            ]
          },
          {
            "time": "21:00",
            "area": "旭川駅",
            "title": "札幌へ帰る人は21:00発",
            "text": "札幌22:25着。最終は22:00発です。泊まる人は歩いてホテルへ。（写真：Shoyuramen / CC BY-SA 3.0）",
            "note": "旭川21:00発→札幌22:25着",
            "photo": [
              "kaeri",
              0
            ]
          }
        ],
        "dealsLead": "バスは現金で払います（SuicaなどのICカードは使えません）。特急は全席指定です。",
        "deals": [
          {
            "name": "旭川駅 ⇄ 旭山動物園（バス）",
            "price": "片道670円",
            "text": "旭川電気軌道の41番・47番、約40分。現金か、バス案内所の券売機のきっぷ。SuicaなどのICカードは使えません。",
            "url": "https://www.asahikawa-denkikidou.jp/schedule/zoo-airport-timetable/"
          },
          {
            "name": "旭山動物園",
            "price": "1,000円（2027年4月29日から1,400円）",
            "text": "中学生以下は無料。Webチケットもあります。再入園はできません。",
            "url": "https://www.city.asahikawa.hokkaido.jp/asahiyamazoo/generalinformation/d052849.html"
          },
          {
            "name": "男山 酒造り資料舘",
            "price": "無料（試飲は有料）",
            "text": "道北バスで1条8丁目から25〜30分、片道260〜350円（乗る系統で違います）。現金で。",
            "url": "https://www.otokoyama.com/museum/"
          },
          {
            "name": "髙砂酒造 明治酒蔵",
            "price": "入場無料",
            "text": "駅から歩いて15分。蔵の中の見学は予約制（無料）。",
            "url": "https://takasagoshuzo.com/meiji-sakagura/"
          },
          {
            "name": "三浦綾子記念文学館",
            "price": "700円",
            "text": "学生300円、小中高生は無料。見本林を歩くだけなら無料です。",
            "url": "https://www.hyouten.com/info"
          },
          {
            "name": "札幌 ⇄ 旭川（特急）",
            "price": "片道5,440円",
            "text": "約1時間25分、全席指定。北海道レールパスで乗れます（先に指定席券を受け取る）。",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          }
        ]
      },
      "late": {
        "kicker": "旭川駅から1日（雪のない季節：4月29日〜11月3日）",
        "h1": "朝いちばんに動物園、午後は酒蔵。夕方の旭橋を見て、焼き鳥の小路へ。",
        "lead": "雪のない季節の旭山動物園（あさひやまどうぶつえん）は9:30に開きます。旭川駅前9:10のバスで行って、混む前にペンギン・アザラシ・ホッキョクグマを。昼すぎに町へ戻って、バスで酒蔵の男山へ。買物公園で旭川ラーメンを食べたら、常磐公園を抜けて、石狩川にかかる旭橋を夕方の光で見ます。夜は「5・7小路ふらりーと」で新子焼き。",
        "favName": "夕方の旭橋",
        "favText": "1932年にできた鉄のアーチ橋。常磐公園の北の土手に上がると、石狩川の向こうに見えます。（写真：MIKI Yoshihito / CC BY 4.0）",
        "favPhoto": [
          "tokiwa",
          0
        ],
        "who": [
          "動物園は4月8日〜28日と11月4日〜10日が休み。10月16日からは16:30に閉まります",
          "2027年4月29日から、動物園の入園料は1,400円になります（いまは1,000円）",
          "動物園へのバスは片道670円で、SuicaなどのICカードは使えません。現金か、駅前のバス案内所の券売機のきっぷで",
          "このコースのバスの時刻は2026年の夏のものです。2027年の時刻表が出たら確かめてください",
          "動物園は再入園ができません。お昼は園内の食堂で。夏休みと連休は昼前から混みます",
          "9月からは日の入りが早くなります（9月の終わりは17:15ごろ）。男山から戻ったら、ラーメンの前に常磐公園と旭橋へ",
          "札幌から日帰りなら、札幌8:00発の特急で旭川9:25、9:40のバスで動物園へ。帰りは20:00発か21:00発、最終は22:00発。特急は全席指定（片道5,440円）"
        ],
        "dayHead": "1日の流れ（雪のない季節。バスは2026年夏の時刻）",
        "day": [
          {
            "time": "9:10",
            "area": "旭川駅",
            "title": "駅前の6番のりばからバス",
            "text": "動物園まで約40分、670円を現金で。開園に合わせるなら8:40発。（写真：Nesnad / CC BY 4.0）",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "9:49",
            "area": "旭山動物園",
            "title": "混む前に、人気の3つの館へ",
            "text": "水中トンネルのぺんぎん館、あざらし館、ほっきょくぐま館。お昼は園内で。（写真：pelican from Tokyo, Japan / CC BY-SA 2.0）",
            "photo": [
              "zoo",
              2
            ]
          },
          {
            "time": "13:40",
            "area": "動物園 → 旭川駅",
            "title": "バスで町へ戻る",
            "text": "駅に14:23。1条8丁目のバス停まで歩いて5分。（写真：欅 (Keyaki) / CC BY-SA 3.0）",
            "photo": [
              "zoo",
              5
            ]
          },
          {
            "time": "14:40",
            "area": "男山",
            "title": "バスで酒蔵へ",
            "text": "15:09に永山2条6丁目。浮世絵と昔の道具の資料舘は無料、試飲は16:30まで。（写真：pakku / CC BY 3.0）",
            "photo": [
              "otoko",
              0
            ]
          },
          {
            "time": "16:54",
            "area": "買物公園",
            "title": "早めの晩ごはんに旭川ラーメン",
            "text": "バスを降りた1条8丁目のそばに山頭火、1本北に梅光軒（17:00から）。（写真：Nesnad / CC BY 4.0）",
            "photo": [
              "kaimono",
              3
            ]
          },
          {
            "time": "18:00",
            "area": "常磐公園・旭橋",
            "title": "池の公園から、夕方の橋へ",
            "text": "買物公園を北へ歩いて15分。土手に上がると石狩川と旭橋。（写真：pakku / CC BY 3.0）",
            "photo": [
              "tokiwa",
              1
            ]
          },
          {
            "time": "19:10",
            "area": "5・7小路ふらりーと",
            "title": "焼き鳥の小路で新子焼き",
            "text": "若鶏の半身を炭火で焼いた旭川の名物。ぎんねこは月曜休みです。札幌へ帰る人は21:00発（22:25着）、最終は22:00発。（写真：久保竜弥 / CC BY-SA 4.0）",
            "note": "旭川21:00発→札幌22:25着",
            "photo": [
              "furari",
              0
            ]
          }
        ],
        "dealsLead": "バスは現金で払います（SuicaなどのICカードは使えません）。特急は全席指定です。",
        "deals": [
          {
            "name": "旭川駅 ⇄ 旭山動物園（バス）",
            "price": "片道670円",
            "text": "旭川電気軌道の41番・47番、約40分。現金か、バス案内所の券売機のきっぷ。SuicaなどのICカードは使えません。",
            "url": "https://www.asahikawa-denkikidou.jp/schedule/zoo-airport-timetable/"
          },
          {
            "name": "旭山動物園",
            "price": "1,000円（2027年4月29日から1,400円）",
            "text": "中学生以下は無料。Webチケットもあります。再入園はできません。",
            "url": "https://www.city.asahikawa.hokkaido.jp/asahiyamazoo/generalinformation/d052849.html"
          },
          {
            "name": "男山 酒造り資料舘",
            "price": "無料（試飲は有料）",
            "text": "道北バスで1条8丁目から25〜30分、片道260〜350円（乗る系統で違います）。現金で。",
            "url": "https://www.otokoyama.com/museum/"
          },
          {
            "name": "髙砂酒造 明治酒蔵",
            "price": "入場無料",
            "text": "駅から歩いて15分。蔵の中の見学は予約制（無料）。",
            "url": "https://takasagoshuzo.com/meiji-sakagura/"
          },
          {
            "name": "三浦綾子記念文学館",
            "price": "700円",
            "text": "学生300円、小中高生は無料。見本林を歩くだけなら無料です。",
            "url": "https://www.hyouten.com/info"
          },
          {
            "name": "札幌 ⇄ 旭川（特急）",
            "price": "片道5,440円",
            "text": "約1時間25分、全席指定。北海道レールパスで乗れます（先に指定席券を受け取る）。",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: "en",
    docTitle: "Asahiyama Zoo & Asahikawa: a day from Asahikawa Station MAP",
    titleMain: "Asahiyama Zoo & Asahikawa",
    titleSub: "旭山動物園と旭川の町",
    howto: "How to use",
    allMaps: "← All maps",
    home: "All maps",
    tabMap: "Map",
    menu: "Menu",
    list: "Spots",
    listHead: "All spots",
    listNote: "The numbers are the order to go in. The stops that fit the timetable are chosen to begin with. Nos. 3–5 (Otokoyama, Takasago, the literature museum) are afternoon options: pick one. The dotted line only shows the order; it is not the actual path.",
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
    credit: "Text: Toshi<br>Photos: Wikimedia Commons (the photographer and licence are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: "Photo: ",
    loadError: "Could not load the map data. Please reload.",
    hours: "Hours",
    fee: "Fee",
    train: "Train",
    bus: "Bus",
    walk: "On foot",
    pay: "Paying",
    reserve: "Booking",
    tattoo: "Tattoos",
    season: "Season",
    closed: "Closed",
    cash: "Bring cash",
    checked: "Checked on official websites and a route planner on {d}. Details can change, so please check before you go.",
    unchecked: "Could not be confirmed on an official website as of {d}. Please check the latest information before you go.",
    checkedDate: "Nov 28, 2026",
    noticeHead: "Note",
    more: "Details",
    linkKinds: {
      "official": "Official site",
      "timetable": "Timetable",
      "info": "Info"
    },
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
    pickNote: "The stops that fit the timetable are chosen to begin with, and the suggested times assume that combination. Asahikawa Station (start and return) is always on your route.",
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
    courseEarly: "Winter\n11 Nov – 7 Apr",
    courseLate: "Snow-free season\n29 Apr – 3 Nov",
    swMode: "How to go",
    intro: {
      "favLabel": "Best moment",
      "whoHead": "Good to know",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Buses, admission and trains",
      "dealsMore": "See the official site or route planner",
      "dealsNote": "Prices are per adult, checked on 28 November 2026 on each official website, the bus operator’s timetable and a route planner (timetables for 3 and 5 December). Meals are extra.",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick the season",
          "text": "The buttons above the list switch between “Winter” and “Snow-free season”. The map opens on the one that matches today’s date. The zoo’s hours differ, so the timetable changes."
        },
        {
          "title": "Swap the afternoon stop",
          "text": "Only the stops that fit the timetable are chosen to begin with. Tap “Want to go” / “Going” to swap in Otokoyama, Takasago or the literature museum; a short note tells you how to get there."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that can stop you at the door come first: closing days, how to pay on the bus, what to wear in winter. Times and prices are below."
        },
        {
          "title": "Directions in Google Maps",
          "text": "“Open in Google Maps” on each stop takes you straight to directions. The ramen shops are inside no. 6 and the grilled-chicken shop inside no. 8."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi, put together from official websites and other sources, with photos from Wikimedia Commons."
    },
    introFor: {
      "early": {
        "kicker": "A day from Asahikawa Station (winter: 11 November – 7 April)",
        "h1": "Penguins walking on snow at the zoo; after dark, a sake brewery, ramen and an alley of yakitori.",
        "lead": "In winter Asahiyama Zoo is open only from 10:30 to 15:30. The 9:40 bus from Asahikawa Station gets you there in time for the 11:00 penguin walk. Back in town on the 14:10 bus, walk to the Takasago sake brewery. It is dark by 16:00, so the rest is indoors: Asahikawa ramen on the pedestrian mall, then shinko-yaki grilled chicken in the smoky Furarito alley. The timetable works whether you are staying in Asahikawa or coming from Sapporo for the day.",
        "favName": "The penguin walk",
        "favText": "From when the snow settles until about mid-March, at 11:00 and 14:30: king penguins waddle along the snow path right in front of you. (Photo: 欅 (Keyaki) / CC BY-SA 3.0)",
        "favPhoto": [
          "zoo",
          0
        ],
        "who": [
          "The zoo is closed 30 December – 1 January. The penguin walk starts once snow has settled (usually from late December); the start date is announced on the zoo’s social media",
          "January in Asahikawa averages a high of −3.3°C and a low of −11.7°C. Bring a down jacket, hat, gloves and grippy shoes: the zoo is hilly and you will be outside for three hours",
          "The zoo bus costs ¥670 each way and does not take Suica or other IC cards. Pay cash, or buy tickets from the machine at the bus information centre by the station",
          "There is no re-entry at the zoo: have lunch at one of its restaurants",
          "Sunset is just before 16:00 in December and about 16:45 in February. The outdoor stops come first, while it is light",
          "Day trip from Sapporo: the 8:00 limited express reaches Asahikawa at 9:25. Return on the 20:00 or 21:00; the last train is the 22:00. All seats are reserved (¥5,440 each way)",
          "The Asahikawa Winter Festival runs 6–11 February (Tokiwa Park and the riverbank by Asahibashi). On 5–7 February the zoo stays open until 20:30"
        ],
        "dayHead": "The day at a glance (winter; same every day)",
        "day": [
          {
            "time": "9:40",
            "area": "Asahikawa Station",
            "title": "Bus from stop 6 outside the station",
            "text": "About 40 minutes to the zoo, ¥670 in cash. The 8:00 limited express from Sapporo connects with this bus. (Photo: Nagono / CC BY-SA 3.0)",
            "photo": [
              "eki",
              1
            ]
          },
          {
            "time": "10:22",
            "area": "Asahiyama Zoo",
            "title": "Straight to the 11:00 penguin walk",
            "text": "Gates open at 10:30. After the walk: the underwater tunnel in the Penguin House, the Seal House and the Polar Bear House. Lunch inside the zoo. (Photo: なよろ / CC BY-SA 4.0)",
            "photo": [
              "zoo",
              1
            ]
          },
          {
            "time": "14:10",
            "area": "Zoo → Asahikawa Station",
            "title": "Bus back to town",
            "text": "Back at the station at 14:54. To see the 14:30 walk too, take the 15:10 bus. (Photo: pelican from Tokyo, Japan / CC BY-SA 2.0)",
            "photo": [
              "zoo",
              3
            ]
          },
          {
            "time": "15:15",
            "area": "Takasago brewery",
            "title": "Tasting in a 1909 brewery building",
            "text": "15 minutes’ walk from the station; open until 17:00. You can swap in Otokoyama or the literature museum instead. (Photo: Jennifer Feuchter / CC BY 2.0)",
            "photo": [
              "takasago",
              0
            ]
          },
          {
            "time": "16:20",
            "area": "Kaimono Koen mall",
            "title": "The mall after dark, then Asahikawa ramen",
            "text": "Baikohken reopens at 17:00; Santouka is open through the afternoon. (Photo: Koji1970327 / CC BY-SA 3.0)",
            "photo": [
              "kaimono",
              2
            ]
          },
          {
            "time": "18:00",
            "area": "Furarito alley",
            "title": "Shinko-yaki in the yakitori alley",
            "text": "Half a young chicken grilled over charcoal, Asahikawa’s local dish. Ginneko is closed on Mondays. (Photo: 久保竜弥 / CC BY-SA 4.0)",
            "photo": [
              "furari",
              0
            ]
          },
          {
            "time": "21:00",
            "area": "Asahikawa Station",
            "title": "For Sapporo: the 21:00",
            "text": "Arrives Sapporo 22:25; the last train leaves at 22:00. Staying over? Walk back to your hotel. (Photo: Shoyuramen / CC BY-SA 3.0)",
            "note": "Asahikawa 21:00 → Sapporo 22:25",
            "photo": [
              "kaeri",
              0
            ]
          }
        ],
        "dealsLead": "Buses are paid in cash (no Suica or other IC cards). All limited express seats are reserved.",
        "deals": [
          {
            "name": "Asahikawa Station ⇄ Asahiyama Zoo (bus)",
            "price": "¥670 each way",
            "text": "Asahikawa Denki Kido routes 41 and 47, about 40 minutes. Cash, or a ticket from the machine at the bus information centre. No Suica or other IC cards.",
            "url": "https://www.asahikawa-denkikidou.jp/schedule/zoo-airport-timetable/"
          },
          {
            "name": "Asahiyama Zoo",
            "price": "¥1,000 (¥1,400 from 29 Apr 2027)",
            "text": "Free for junior high school students and younger. Web tickets available. No re-entry.",
            "url": "https://www.city.asahikawa.hokkaido.jp/asahiyamazoo/generalinformation/d052849.html"
          },
          {
            "name": "Otokoyama Sake Brewery Museum",
            "price": "Free (tastings are paid)",
            "text": "25–30 minutes by Dohoku Bus from 1-jo 8-chome, ¥260–350 each way depending on the route. Cash.",
            "url": "https://www.otokoyama.com/museum/"
          },
          {
            "name": "Takasago Meiji Sakagura",
            "price": "Free entry",
            "text": "15 minutes’ walk from the station. Tours inside the brewery are by booking (free).",
            "url": "https://takasagoshuzo.com/meiji-sakagura/"
          },
          {
            "name": "Miura Ayako Literature Museum",
            "price": "¥700",
            "text": "Students ¥300, school pupils free. Walking in the forest is free.",
            "url": "https://www.hyouten.com/info"
          },
          {
            "name": "Sapporo ⇄ Asahikawa (limited express)",
            "price": "¥5,440 each way",
            "text": "About 1 hour 25 minutes, all seats reserved. Covered by the Hokkaido Rail Pass (collect a seat reservation first).",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          }
        ]
      },
      "late": {
        "kicker": "A day from Asahikawa Station (snow-free season: 29 April – 3 November)",
        "h1": "The zoo first thing, a sake brewery after lunch, the bridge at dusk, then the yakitori alley.",
        "lead": "Outside winter, Asahiyama Zoo opens at 9:30. Take the 9:10 bus from Asahikawa Station and see the penguins, seals and polar bears before the crowds. Head back to town after lunch and ride a city bus to the Otokoyama sake brewery. After Asahikawa ramen on the pedestrian mall, cross Tokiwa Park to see Asahibashi Bridge over the Ishikari River in evening light, and end with shinko-yaki grilled chicken in Furarito alley.",
        "favName": "Asahibashi Bridge at dusk",
        "favText": "A steel arch bridge of 1932. Climb the embankment north of Tokiwa Park and it is there across the Ishikari River. (Photo: MIKI Yoshihito / CC BY 4.0)",
        "favPhoto": [
          "tokiwa",
          0
        ],
        "who": [
          "The zoo is closed 8–28 April and 4–10 November, and closes at 16:30 from 16 October",
          "From 29 April 2027 zoo admission is ¥1,400 (now ¥1,000)",
          "The zoo bus costs ¥670 each way and does not take Suica or other IC cards. Pay cash, or buy tickets from the machine at the bus information centre by the station",
          "Bus times in this course are from summer 2026: check again once the 2027 timetable is out",
          "There is no re-entry at the zoo: have lunch at one of its restaurants. In the summer holidays and on long weekends it is crowded from late morning",
          "From September the sun sets earlier (about 17:15 at the end of the month): after Otokoyama, go to Tokiwa Park and the bridge before ramen",
          "Day trip from Sapporo: the 8:00 limited express reaches Asahikawa at 9:25 for the 9:40 bus to the zoo. Return on the 20:00 or 21:00; the last train is the 22:00. All seats are reserved (¥5,440 each way)"
        ],
        "dayHead": "The day at a glance (snow-free season; 2026 summer bus times)",
        "day": [
          {
            "time": "9:10",
            "area": "Asahikawa Station",
            "title": "Bus from stop 6 outside the station",
            "text": "About 40 minutes to the zoo, ¥670 in cash. For opening time, take the 8:40. (Photo: Nesnad / CC BY 4.0)",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "9:49",
            "area": "Asahiyama Zoo",
            "title": "The three popular houses before the crowds",
            "text": "The Penguin House with its underwater tunnel, the Seal House and the Polar Bear House. Lunch inside the zoo. (Photo: pelican from Tokyo, Japan / CC BY-SA 2.0)",
            "photo": [
              "zoo",
              2
            ]
          },
          {
            "time": "13:40",
            "area": "Zoo → Asahikawa Station",
            "title": "Bus back to town",
            "text": "Back at the station at 14:23; five minutes’ walk to the 1-jo 8-chome bus stop. (Photo: 欅 (Keyaki) / CC BY-SA 3.0)",
            "photo": [
              "zoo",
              5
            ]
          },
          {
            "time": "14:40",
            "area": "Otokoyama",
            "title": "City bus to the sake brewery",
            "text": "Arrive Nagayama 2-jo 6-chome at 15:09. The museum of prints and old tools is free; tastings until 16:30. (Photo: pakku / CC BY 3.0)",
            "photo": [
              "otoko",
              0
            ]
          },
          {
            "time": "16:54",
            "area": "Kaimono Koen mall",
            "title": "Asahikawa ramen as an early dinner",
            "text": "Santouka is by the 1-jo 8-chome stop; Baikohken is a block north (from 17:00). (Photo: Nesnad / CC BY 4.0)",
            "photo": [
              "kaimono",
              3
            ]
          },
          {
            "time": "18:00",
            "area": "Tokiwa Park & Asahibashi",
            "title": "Through the park to the bridge at dusk",
            "text": "15 minutes’ walk north up the mall. Climb the embankment for the Ishikari River and the bridge. (Photo: pakku / CC BY 3.0)",
            "photo": [
              "tokiwa",
              1
            ]
          },
          {
            "time": "19:10",
            "area": "Furarito alley",
            "title": "Shinko-yaki in the yakitori alley",
            "text": "Half a young chicken grilled over charcoal, Asahikawa’s local dish. Ginneko is closed on Mondays. For Sapporo, take the 21:00 (arriving 22:25); the last train is the 22:00. (Photo: 久保竜弥 / CC BY-SA 4.0)",
            "note": "Asahikawa 21:00 → Sapporo 22:25",
            "photo": [
              "furari",
              0
            ]
          }
        ],
        "dealsLead": "Buses are paid in cash (no Suica or other IC cards). All limited express seats are reserved.",
        "deals": [
          {
            "name": "Asahikawa Station ⇄ Asahiyama Zoo (bus)",
            "price": "¥670 each way",
            "text": "Asahikawa Denki Kido routes 41 and 47, about 40 minutes. Cash, or a ticket from the machine at the bus information centre. No Suica or other IC cards.",
            "url": "https://www.asahikawa-denkikidou.jp/schedule/zoo-airport-timetable/"
          },
          {
            "name": "Asahiyama Zoo",
            "price": "¥1,000 (¥1,400 from 29 Apr 2027)",
            "text": "Free for junior high school students and younger. Web tickets available. No re-entry.",
            "url": "https://www.city.asahikawa.hokkaido.jp/asahiyamazoo/generalinformation/d052849.html"
          },
          {
            "name": "Otokoyama Sake Brewery Museum",
            "price": "Free (tastings are paid)",
            "text": "25–30 minutes by Dohoku Bus from 1-jo 8-chome, ¥260–350 each way depending on the route. Cash.",
            "url": "https://www.otokoyama.com/museum/"
          },
          {
            "name": "Takasago Meiji Sakagura",
            "price": "Free entry",
            "text": "15 minutes’ walk from the station. Tours inside the brewery are by booking (free).",
            "url": "https://takasagoshuzo.com/meiji-sakagura/"
          },
          {
            "name": "Miura Ayako Literature Museum",
            "price": "¥700",
            "text": "Students ¥300, school pupils free. Walking in the forest is free.",
            "url": "https://www.hyouten.com/info"
          },
          {
            "name": "Sapporo ⇄ Asahikawa (limited express)",
            "price": "¥5,440 each way",
            "text": "About 1 hour 25 minutes, all seats reserved. Covered by the Hokkaido Rail Pass (collect a seat reservation first).",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          }
        ]
      }
    }
  }
};
