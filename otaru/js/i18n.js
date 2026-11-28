/* Page texts in Japanese and English.
   Toshi 個人のマップ。小樽（札幌から日帰り）。写真はすべて Wikimedia Commons（だれかが行った・食べたとは書かない）。
   コースは3つ（一覧の上のボタン）：late＝9〜10時に出る（最初に開く。data/routes/otaru.json）、early＝7時台に出る（otaru-early.json）、
   yoichi＝余市の蒸溜所＋午後の小樽（otaru-yoichi.json）。intro はどのコースにも共通の項目で、コースで変わる項目は introFor[コース] が
   app.js で上書きされる（scripts/sync_otaru.py）。写真は [スポットの id, 写真の番号]。
   時刻・料金は2026年11月26日に確認（出典は data/routes/otaru.json の sources）。直すときはこのファイルを直接直してよい */
window.OTARU_I18N = {
  ja: {
    htmlLang: "ja",
    docTitle: "小樽 札幌から日帰り Otaru MAP",
    titleMain: "小樽",
    titleSub: "Otaru, a day trip from Sapporo",
    howto: "使い方",
    allMaps: "← マップ一覧",
    home: "マップ一覧",
    tabMap: "地図",
    menu: "メニュー",
    list: "一覧",
    listHead: "スポット一覧",
    listNote: "番号は回る順番です。冬（12〜3月）の日の入りに合わせた時間割で、夏の天狗山の時刻はスポットの中にあります。点線は順番を示す線で、実際の道ではありません。",
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
    checkedDate: "2026年11月26日",
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
    pickNote: "最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。札幌駅・小樽駅・帰りは、どの組み合わせでも入ります。",
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
    swCourse: "コース",
    courseAria: "コース",
    courseLate: "9〜10時に出る\n運河・堺町・夜景",
    courseEarly: "7時台に出る\n朝の運河・祝津",
    courseYoichi: "余市の蒸溜所\n＋午後の小樽",
    swMode: "回り方",
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "電車・バス・入場料",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月26日に、各施設の公式サイトと乗換案内（12月3日・5日のダイヤ）で確認しました。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "コースを選ぶ",
          "text": "一覧の上のボタンで「9〜10時に出る」「7時台に出る」「余市の蒸溜所」を選びます。時間割と番号が変わります。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、休みの日・現金のみ・予約・冬の注意など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
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
        "kicker": "札幌から日帰り（9〜10時に出る）",
        "h1": "線路の跡から、静かな運河の北の端へ。暗くなったら、山の上から港の明かり。",
        "lead": "いちばんの見どころは、ガス灯がつく夕方の運河です。この時間割は、冬の日の入りに合わせて浅草橋に戻ってくるように組んであります。日中は、市場の海鮮丼、人の少ない旧手宮線の跡と北運河、銀行街と堺町通り。明かりがついたら天狗山ロープウエイで港の夜景を見て、晩ごはん。札幌9:33の快速エアポートで出て、21時ごろ札幌に戻ります。",
        "favName": "浅草橋の夕暮れ",
        "favText": "12〜1月は16時すぎ、倉庫とガス灯が水面に映ります。（写真：Tan Wei Liang Byorn / CC BY-SA 4.0）",
        "favPhoto": [
          "asakusa",
          0
        ],
        "who": [
          "冬（12〜3月）の日の入りに合わせた時間割です。夏は天狗山を晩ごはんのあとに",
          "歩道は雪と氷。底に溝の深い、滑りにくい靴で",
          "日本銀行旧小樽支店金融資料館は水曜休み（外からも見られます）",
          "天狗山ロープウエイの冬の営業は11/28〜3/28。春と秋に運休の時期があります",
          "小樽の路線バスは1回240円で交通系ICカード可。駅にコインロッカーあり",
          "空港へ直接帰る日は、小樽から快速エアポートで乗り換えなし（時刻は小樽駅のスポットに）"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "9:33",
            "area": "札幌",
            "title": "快速エアポートで小樽へ",
            "text": "小樽10:07着。市場は駅のすぐ横です。（写真：皓月旗 / CC BY-SA 4.0）",
            "photo": [
              "otarueki",
              0
            ],
            "note": "小樽10:07"
          },
          {
            "time": "10:15",
            "area": "三角市場",
            "title": "早めのお昼に海鮮丼",
            "text": "12時前後より入りやすい時間。（写真：bryan... / CC BY-SA 2.0）",
            "photo": [
              "sankaku",
              1
            ]
          },
          {
            "time": "11:05",
            "area": "旧手宮線・北運河",
            "title": "線路の跡から運河の北の端へ",
            "text": "人の少ない北運河から、運河ぞいを南へ。（写真：inunami / CC BY 2.0）",
            "photo": [
              "temiya",
              0
            ]
          },
          {
            "time": "12:35",
            "area": "色内",
            "title": "1912年の日本銀行（無料）",
            "text": "昔の銀行の建物が並ぶ通り。水曜は休館。（写真：663highland / CC BY 2.5）",
            "photo": [
              "ginko",
              0
            ]
          },
          {
            "time": "13:40",
            "area": "堺町通り",
            "title": "ランプの喫茶とオルゴール",
            "text": "北一ホールでひと休みして、メルヘン交差点まで。（写真：663highland / CC BY 2.5）",
            "photo": [
              "kitaichi",
              0
            ]
          },
          {
            "time": "16:00",
            "area": "浅草橋",
            "title": "ガス灯がつくころの運河",
            "text": "12〜1月の日の入りは16:00〜16:45。（写真：ruiraykwok / CC BY-SA 3.0）",
            "photo": [
              "asakusa",
              1
            ]
          },
          {
            "time": "16:40",
            "area": "天狗山",
            "title": "バスとロープウエイで夜景",
            "text": "18:07のバスで駅前へ。夏は晩ごはんのあとに。（写真：wellincline / CC BY-SA 3.0）",
            "photo": [
              "tengu",
              0
            ]
          },
          {
            "time": "18:35",
            "area": "小樽",
            "title": "晩ごはん、20:22の電車で札幌へ",
            "text": "若鶏の半身揚げか、運河ぞいの倉庫のビール。札幌21:11着。（写真：Haha169 / CC BY-SA 4.0）",
            "photo": [
              "yuhan",
              0
            ],
            "note": "札幌21:11"
          }
        ],
        "dealsLead": "札幌〜小樽は片道800円（ICカード）。そのほかは、乗ったもの・入ったものの分だけです。",
        "deals": [
          {
            "name": "JR 札幌〜小樽",
            "price": "片道800円",
            "text": "快速エアポートで34分、普通で45〜50分。交通系ICカード可。JR北海道レールパス・札幌・登別エリアパスで乗れます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "小樽の路線バス",
            "price": "1回240円",
            "text": "交通系ICカード可。3回以上乗るなら、小樽駅前ターミナルの窓口で1日乗車券（800円）を。",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/access/"
          },
          {
            "name": "天狗山ロープウエイ",
            "price": "往復2,000円",
            "text": "冬の料金（夏は1,800円）。カード・電子マネー可。",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/hours-and-fees/"
          },
          {
            "name": "日本銀行旧小樽支店金融資料館",
            "price": "無料",
            "text": "水曜休み。12〜3月は10:00〜17:00。",
            "url": "https://www3.boj.or.jp/otaru-m/"
          },
          {
            "name": "若鶏時代なると 若鶏半身揚げ",
            "price": "1,190円",
            "text": "本店は11:00〜21:00（ラストオーダー20:30）。",
            "url": "http://otaru-naruto.jp/naruto/menu.html"
          },
          {
            "name": "小樽運河クルーズ（寄り道）",
            "price": "1,800円・2,000円",
            "text": "デイ・ナイト、約40分。チケットは公式サイト（英語あり）で出航の1時間前まで。",
            "url": "https://otaru.cc/price/"
          }
        ]
      },
      "early": {
        "kicker": "札幌から日帰り（7時台に出る）",
        "h1": "市場で朝ごはん、ランプの火入れ、開いたばかりの堺町。午後は祝津の屋敷と水族館。",
        "lead": "観光の人が増える前の小樽を歩くコースです。札幌7:14の電車で出て、三角市場で朝ごはん。人の少ない朝の浅草橋を見て、9時に北一ホールで石油ランプに火が入るところを見たら、店が開いたばかりの堺町通りへ。昼からはバスで祝津へ行き、小樽貴賓館でお昼と見学、おたる水族館。夜の運河を見て晩ごはん、札幌には20時ごろ戻ります。",
        "favName": "人の少ない朝の運河",
        "favText": "観光の人が増える前の時間です。（写真：bryan... / CC BY-SA 2.0）",
        "favPhoto": [
          "unga",
          1
        ],
        "who": [
          "札幌7:14発（すすきのからは6:55ごろの地下鉄で）",
          "北一ホールのランプの火入れは毎朝9:00〜9:30",
          "日本銀行の資料館は水曜休み。12〜3月は10:00から",
          "小樽貴賓館は現金のみ（1,300円）。11〜3月は入館15:30まで",
          "おたる水族館の冬期営業は12/12〜2/23（10:00〜16:00）。11/24〜12/11は休館",
          "祝津へのバスは小樽駅前12:00、帰りは16:32（どの日も）"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "7:14",
            "area": "札幌",
            "title": "朝の電車で小樽へ",
            "text": "小樽8:01着。（写真：皓月旗 / CC BY-SA 4.0）",
            "photo": [
              "otarueki",
              0
            ],
            "note": "小樽8:01"
          },
          {
            "time": "8:05",
            "area": "三角市場",
            "title": "市場の食堂で朝ごはん",
            "text": "朝6時・7時から開く店があります。（写真：bryan... / CC BY-SA 2.0）",
            "photo": [
              "sankaku",
              1
            ]
          },
          {
            "time": "8:50",
            "area": "浅草橋",
            "title": "人の少ない朝の運河",
            "text": "中央通りを下って12分ほど。（写真：bryan... / CC BY-SA 2.0）",
            "photo": [
              "unga",
              1
            ]
          },
          {
            "time": "9:05",
            "area": "堺町通り",
            "title": "ランプの火入れと、開店すぐの通り",
            "text": "北一ホールのあと、メルヘン交差点まで。（写真：663highland / CC BY 2.5）",
            "photo": [
              "kitaichi",
              1
            ]
          },
          {
            "time": "10:55",
            "area": "色内",
            "title": "日本銀行の資料館と線路の跡",
            "text": "11:52に駅前へ。（写真：663highland / CC BY 2.5）",
            "photo": [
              "ginko",
              0
            ]
          },
          {
            "time": "12:00",
            "area": "祝津",
            "title": "バスで祝津へ、貴賓館でお昼",
            "text": "終点のおたる水族館から坂を上ります。（写真：皓月旗 / CC BY-SA 4.0）",
            "photo": [
              "shukutsu",
              1
            ]
          },
          {
            "time": "14:15",
            "area": "おたる水族館",
            "title": "冬はペンギンの雪中さんぽ",
            "text": "16:10（冬の直行）か16:32のバスで小樽へ。（写真：切干大根 / CC BY-SA 4.0）",
            "photo": [
              "aq",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "小樽",
            "title": "夜の運河と晩ごはん",
            "text": "小樽19:27発で札幌20:01着。（写真：Haha169 / CC BY-SA 4.0）",
            "photo": [
              "yuhan",
              0
            ],
            "note": "札幌20:01"
          }
        ],
        "dealsLead": "札幌〜小樽は片道800円（ICカード）。祝津へのバスは片道240円です。",
        "deals": [
          {
            "name": "JR 札幌〜小樽",
            "price": "片道800円",
            "text": "快速エアポートで34分、普通で45〜50分。交通系ICカード可。JR北海道レールパス・札幌・登別エリアパスで乗れます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "小樽の路線バス",
            "price": "1回240円",
            "text": "交通系ICカード可。3回以上乗るなら、小樽駅前ターミナルの窓口で1日乗車券（800円）を。",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/access/"
          },
          {
            "name": "小樽貴賓館（旧青山別邸）",
            "price": "1,300円",
            "text": "現金のみ（カード・電子決済不可）。お食事は11:00〜14:30。",
            "url": "https://www.otaru-kihinkan.jp/aoyama_about/"
          },
          {
            "name": "おたる水族館",
            "price": "1,300円",
            "text": "冬期営業（12/12〜2/23）の料金。通常期の料金は公式サイトで。",
            "url": "https://otaru-aq.jp/guide/tickets/"
          },
          {
            "name": "日本銀行旧小樽支店金融資料館",
            "price": "無料",
            "text": "水曜休み。12〜3月は10:00〜17:00。",
            "url": "https://www3.boj.or.jp/otaru-m/"
          },
          {
            "name": "小樽運河クルーズ（寄り道）",
            "price": "1,800円・2,000円",
            "text": "デイ・ナイト、約40分。チケットは公式サイト（英語あり）で出航の1時間前まで。",
            "url": "https://otaru.cc/price/"
          }
        ]
      },
      "yoichi": {
        "kicker": "札幌から日帰り（余市の蒸溜所と小樽）",
        "h1": "午前は余市の蒸溜所、午後は小樽の銀行街と堺町。暗くなったら運河。",
        "lead": "ウイスキーの蒸溜所と小樽の町を、1日でつなぐコースです。余市と小樽の間の電車は1時間〜1時間20分おきなので、乗る電車を先に決めてあります。札幌8:41の電車で余市へ。予約しておいたニッカの蒸溜所のツアー（12〜1月はセミナー）に参加して、蒸溜所のレストランでお昼。13:43の電車で小樽に戻り、銀行街と堺町通りを歩いて、暗くなるころの浅草橋へ。晩ごはんのあとに天狗山の夜景を足すこともできます。",
        "favName": "石造りの蒸溜所",
        "favText": "とんがり屋根のキルン塔と、石の棟が並ぶ敷地。（写真：さかおり / CC BY-SA 4.0）",
        "favPhoto": [
          "nikka",
          0
        ],
        "who": [
          "蒸溜所の見学は予約制（公式の予約ページ、英語あり、4週間前から）。ツアーの案内は日本語だけ",
          "2026年12月〜2027年1月は無料ツアーなし、有料セミナーだけ（20歳以上・その日に運転しない人）",
          "蒸溜所は12/23〜1/7休み。その日は「9〜10時に出る」コースへ",
          "余市〜小樽の電車は1時間〜1時間20分おき。帰りの13:43を先に決めておく",
          "小樽〜余市でICカードが使えるかは未確認。きっぷが確実",
          "予約なしでも、ミュージアム・ショップ・レストランに入れます（最終入場15:30）"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "8:41",
            "area": "札幌",
            "title": "小樽で乗り換えて余市へ",
            "text": "余市10:00着。（写真：MaedaAkihiko / CC0）",
            "photo": [
              "yoichi",
              0
            ],
            "note": "余市10:00"
          },
          {
            "time": "10:05",
            "area": "余市",
            "title": "蒸溜所のミュージアムとツアー",
            "text": "予約した回に正門から。（写真：さかおり / CC BY-SA 4.0）",
            "photo": [
              "nikka",
              1
            ]
          },
          {
            "time": "12:00",
            "area": "余市",
            "title": "蒸溜所のレストランでお昼",
            "text": "RITA'S KITCHENは10:00〜15:50。（写真：さかおり / CC BY-SA 4.0）",
            "photo": [
              "nikka",
              4
            ]
          },
          {
            "time": "13:43",
            "area": "余市→小樽",
            "title": "電車で小樽へ",
            "text": "小樽14:09着。（写真：皓月旗 / CC BY-SA 4.0）",
            "photo": [
              "otarueki",
              0
            ]
          },
          {
            "time": "14:25",
            "area": "色内・堺町",
            "title": "銀行街と堺町通り",
            "text": "北一ホールでひと休み。（写真：663highland / CC BY 2.5）",
            "photo": [
              "kitaichi",
              0
            ]
          },
          {
            "time": "16:30",
            "area": "浅草橋",
            "title": "暗くなるころの運河",
            "text": "倉庫とガス灯が水面に映ります。（写真：Tan Wei Liang Byorn / CC BY-SA 4.0）",
            "photo": [
              "asakusa",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "小樽",
            "title": "晩ごはん、19:27の電車で札幌へ",
            "text": "天狗山に寄ると札幌着は22:03。（写真：Haha169 / CC BY-SA 4.0）",
            "photo": [
              "yuhan",
              0
            ],
            "note": "札幌20:01"
          }
        ],
        "dealsLead": "電車は札幌→余市1,380円、余市→小樽470円、小樽→札幌800円。蒸溜所のガイドツアーは無料です（予約制）。",
        "deals": [
          {
            "name": "JR 札幌→余市",
            "price": "1,380円",
            "text": "小樽で乗り換え。JR北海道レールパスで乗れます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "JR 余市→小樽",
            "price": "470円",
            "text": "昼は12:37・13:43・15:02発。高速バスなら560円。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "ニッカ 余市蒸溜所 ガイドツアー",
            "price": "無料",
            "text": "予約制・日本語のみ。12〜1月は有料セミナーだけ（11月の案内では3,000円・現金）。",
            "url": "https://reserva.be/nikkayoichi/news"
          },
          {
            "name": "JR 札幌〜小樽",
            "price": "片道800円",
            "text": "快速エアポートで34分、普通で45〜50分。交通系ICカード可。JR北海道レールパス・札幌・登別エリアパスで乗れます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "小樽の路線バス",
            "price": "1回240円",
            "text": "交通系ICカード可。3回以上乗るなら、小樽駅前ターミナルの窓口で1日乗車券（800円）を。",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/access/"
          },
          {
            "name": "小樽運河クルーズ（寄り道）",
            "price": "1,800円・2,000円",
            "text": "デイ・ナイト、約40分。チケットは公式サイト（英語あり）で出航の1時間前まで。",
            "url": "https://otaru.cc/price/"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: "en",
    docTitle: "Otaru MAP: a day trip from Sapporo",
    titleMain: "Otaru",
    titleSub: "小樽 札幌から日帰り",
    howto: "How to use",
    allMaps: "← All maps",
    home: "All maps",
    tabMap: "Map",
    menu: "Menu",
    list: "Spots",
    listHead: "All spots",
    listNote: "Numbers show the order. The timetable follows winter sunsets (December–March); summer times for Mt. Tengu are inside that spot. The dotted line shows the order, not the actual path.",
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
    checkedDate: "Nov 26, 2026",
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
    pickNote: "The places that fit the timetable are selected to start with, and suggested times assume that set. Sapporo Station, Otaru Station and the way back are always included.",
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
    swCourse: "Course",
    courseAria: "Course",
    courseLate: "Leave 9–10 am\nCanal, shops, night view",
    courseEarly: "Leave about 7 am\nMorning canal, Shukutsu",
    courseYoichi: "Yoichi distillery\n+ Otaru afternoon",
    swMode: "How to go",
    intro: {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Trains, buses and admission",
      "dealsMore": "See official site or route planner",
      "dealsNote": "Per adult. Checked on Nov 26, 2026 with the official sites and a route planner (3 and 5 December timetables).",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose a course",
          "text": "Use the buttons above the list: leave at 9–10 am, leave around 7 am, or the Yoichi distillery. The timetable and numbers change."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that could stop you at the door (closing days, cash only, bookings, winter tips) come first, with times and fees below."
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
        "kicker": "A day trip from Sapporo (leave at 9–10 am)",
        "h1": "From the old railway to the quiet end of the canal, then the harbour lights from the mountain.",
        "lead": "The best moment in Otaru is the canal at dusk, when the gas lamps come on, and this timetable follows winter sunsets to have you back at Asakusa Bridge for it. Before that: an early seafood bowl at the market, the old Temiya line and the quiet North Canal, the old bank street and Sakaimachi. Once the lamps are lit, ride the Mt. Tengu Ropeway for the harbour lights, then have dinner. Leave Sapporo on the 9:33 Rapid Airport; you are back around 21:00.",
        "favName": "Asakusa Bridge at dusk",
        "favText": "In December and January, just after 16:00, the warehouses and gas lamps reflect in the water. (Photo: Tan Wei Liang Byorn / CC BY-SA 4.0)",
        "favPhoto": [
          "asakusa",
          0
        ],
        "who": [
          "The timetable follows winter sunsets (December–March). In summer, go up Mt. Tengu after dinner",
          "Pavements are snow and ice. Wear boots with deep-tread soles",
          "The Bank of Japan museum closes on Wednesdays (you can still see it from outside)",
          "The ropeway’s winter season is 28 Nov–28 Mar; it closes for a while in spring and autumn",
          "City buses are ¥240 a ride and take IC cards. Lockers at Otaru Station",
          "Flying out the same day? The Rapid Airport runs from Otaru to New Chitose Airport without a change (times under Otaru Station)"
        ],
        "dayHead": "Your day",
        "day": [
          {
            "time": "9:33",
            "area": "Sapporo",
            "title": "Rapid Airport to Otaru",
            "text": "Arrive 10:07. The market is right beside the station. (Photo: 皓月旗 / CC BY-SA 4.0)",
            "photo": [
              "otarueki",
              0
            ],
            "note": "Otaru 10:07"
          },
          {
            "time": "10:15",
            "area": "Sankaku Market",
            "title": "An early seafood bowl",
            "text": "Easier before the noon rush. (Photo: bryan... / CC BY-SA 2.0)",
            "photo": [
              "sankaku",
              1
            ]
          },
          {
            "time": "11:05",
            "area": "Old Temiya line · North Canal",
            "title": "Along the old tracks to the quiet end of the canal",
            "text": "Then south along the canal path. (Photo: inunami / CC BY 2.0)",
            "photo": [
              "temiya",
              0
            ]
          },
          {
            "time": "12:35",
            "area": "Ironai",
            "title": "The 1912 Bank of Japan building (free)",
            "text": "A street of old banks. Closed Wednesdays. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "ginko",
              0
            ]
          },
          {
            "time": "13:40",
            "area": "Sakaimachi",
            "title": "A lamp-lit café and music boxes",
            "text": "A break at Kitaichi Hall, then on to Märchen Crossing. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "kitaichi",
              0
            ]
          },
          {
            "time": "16:00",
            "area": "Asakusa Bridge",
            "title": "The canal as the lamps come on",
            "text": "Sunset is 16:00–16:45 in December and January. (Photo: ruiraykwok / CC BY-SA 3.0)",
            "photo": [
              "asakusa",
              1
            ]
          },
          {
            "time": "16:40",
            "area": "Mt. Tengu",
            "title": "Bus and ropeway to the night view",
            "text": "Back on the 18:07 bus. In summer, go after dinner. (Photo: wellincline / CC BY-SA 3.0)",
            "photo": [
              "tengu",
              0
            ]
          },
          {
            "time": "18:35",
            "area": "Otaru",
            "title": "Dinner, then the 20:22 to Sapporo",
            "text": "Fried chicken or a canal-side brewpub. Sapporo 21:11. (Photo: Haha169 / CC BY-SA 4.0)",
            "photo": [
              "yuhan",
              0
            ],
            "note": "Sapporo 21:11"
          }
        ],
        "dealsLead": "Sapporo–Otaru is ¥800 each way on an IC card. Everything else you pay as you go.",
        "deals": [
          {
            "name": "JR Sapporo–Otaru",
            "price": "¥800 one way",
            "text": "34 minutes on the Rapid Airport, 45–50 on a local train. IC cards work. Covered by the JR Hokkaido Rail Pass and the Sapporo-Noboribetsu Area Pass.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Otaru city buses",
            "price": "¥240 a ride",
            "text": "IC cards work. Riding three times or more? Buy the ¥800 day pass at the Otaru Station bus terminal.",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/access/"
          },
          {
            "name": "Mt. Tengu Ropeway",
            "price": "¥2,000 return",
            "text": "Winter price (¥1,800 in summer). Cards and e-money accepted.",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/hours-and-fees/"
          },
          {
            "name": "Bank of Japan Otaru Museum",
            "price": "Free",
            "text": "Closed Wednesdays. 10:00–17:00 in December–March.",
            "url": "https://www3.boj.or.jp/otaru-m/"
          },
          {
            "name": "Naruto’s half fried chicken",
            "price": "¥1,190",
            "text": "Main shop open 11:00–21:00 (last order 20:30).",
            "url": "http://otaru-naruto.jp/naruto/menu.html"
          },
          {
            "name": "Otaru Canal Cruise (optional)",
            "price": "¥1,800 / ¥2,000",
            "text": "Day / night, about 40 minutes. Tickets online (English) up to an hour before.",
            "url": "https://otaru.cc/price/"
          }
        ]
      },
      "early": {
        "kicker": "A day trip from Sapporo (leave around 7 am)",
        "h1": "Breakfast at the market, the lamps being lit, Sakaimachi as it opens. Then a villa and an aquarium by the sea.",
        "lead": "Otaru before the day visitors arrive. Take the 7:14 train, eat breakfast at Sankaku Market, see Asakusa Bridge while it is quiet, watch the oil lamps being lit at Kitaichi Hall at 9:00, and walk Sakaimachi as the shops open. After noon, take the bus to Shukutsu for lunch and a look round Otaru Kihinkan, then Otaru Aquarium. See the canal at night, have dinner, and be back in Sapporo around 20:00.",
        "favName": "The canal in the early morning",
        "favText": "Before the day visitors arrive. (Photo: bryan... / CC BY-SA 2.0)",
        "favPhoto": [
          "unga",
          1
        ],
        "who": [
          "Leave Sapporo at 7:14 (from Susukino, take the subway around 6:55)",
          "The lamps at Kitaichi Hall are lit every morning from 9:00 to 9:30",
          "The Bank of Japan museum closes on Wednesdays and opens at 10:00 in December–March",
          "Otaru Kihinkan is cash only (¥1,300); in November–March last entry is 15:30",
          "Otaru Aquarium’s winter season is 12 Dec–23 Feb (10:00–16:00); it is closed 24 Nov–11 Dec",
          "The bus to Shukutsu leaves Otaru Station at 12:00; back at 16:32 (every day)"
        ],
        "dayHead": "Your day",
        "day": [
          {
            "time": "7:14",
            "area": "Sapporo",
            "title": "Morning train to Otaru",
            "text": "Arrive 8:01. (Photo: 皓月旗 / CC BY-SA 4.0)",
            "photo": [
              "otarueki",
              0
            ],
            "note": "Otaru 8:01"
          },
          {
            "time": "8:05",
            "area": "Sankaku Market",
            "title": "Breakfast at a market diner",
            "text": "Some open at 6:00 or 7:00. (Photo: bryan... / CC BY-SA 2.0)",
            "photo": [
              "sankaku",
              1
            ]
          },
          {
            "time": "8:50",
            "area": "Asakusa Bridge",
            "title": "The quiet canal in the morning",
            "text": "About 12 minutes down Chuo-dori. (Photo: bryan... / CC BY-SA 2.0)",
            "photo": [
              "unga",
              1
            ]
          },
          {
            "time": "9:05",
            "area": "Sakaimachi",
            "title": "Lamp lighting and a street just opening",
            "text": "Kitaichi Hall, then on to Märchen Crossing. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "kitaichi",
              1
            ]
          },
          {
            "time": "10:55",
            "area": "Ironai",
            "title": "The Bank of Japan museum and the old line",
            "text": "To the station by 11:52. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "ginko",
              0
            ]
          },
          {
            "time": "12:00",
            "area": "Shukutsu",
            "title": "Bus to Shukutsu, lunch at Kihinkan",
            "text": "Walk up the hill from the aquarium stop. (Photo: 皓月旗 / CC BY-SA 4.0)",
            "photo": [
              "shukutsu",
              1
            ]
          },
          {
            "time": "14:15",
            "area": "Otaru Aquarium",
            "title": "Penguins on the snow in winter",
            "text": "Back on the 16:10 direct bus (winter) or the 16:32. (Photo: 切干大根 / CC BY-SA 4.0)",
            "photo": [
              "aq",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Otaru",
            "title": "The canal at night and dinner",
            "text": "The 19:27 reaches Sapporo at 20:01. (Photo: Haha169 / CC BY-SA 4.0)",
            "photo": [
              "yuhan",
              0
            ],
            "note": "Sapporo 20:01"
          }
        ],
        "dealsLead": "Sapporo–Otaru is ¥800 each way on an IC card; the bus to Shukutsu is ¥240 each way.",
        "deals": [
          {
            "name": "JR Sapporo–Otaru",
            "price": "¥800 one way",
            "text": "34 minutes on the Rapid Airport, 45–50 on a local train. IC cards work. Covered by the JR Hokkaido Rail Pass and the Sapporo-Noboribetsu Area Pass.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Otaru city buses",
            "price": "¥240 a ride",
            "text": "IC cards work. Riding three times or more? Buy the ¥800 day pass at the Otaru Station bus terminal.",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/access/"
          },
          {
            "name": "Otaru Kihinkan (former Aoyama villa)",
            "price": "¥1,300",
            "text": "Cash only (no cards or e-money). Meals 11:00–14:30.",
            "url": "https://www.otaru-kihinkan.jp/aoyama_about/"
          },
          {
            "name": "Otaru Aquarium",
            "price": "¥1,300",
            "text": "Winter price (12 Dec–23 Feb). See the official site for regular-season fees.",
            "url": "https://otaru-aq.jp/guide/tickets/"
          },
          {
            "name": "Bank of Japan Otaru Museum",
            "price": "Free",
            "text": "Closed Wednesdays. 10:00–17:00 in December–March.",
            "url": "https://www3.boj.or.jp/otaru-m/"
          },
          {
            "name": "Otaru Canal Cruise (optional)",
            "price": "¥1,800 / ¥2,000",
            "text": "Day / night, about 40 minutes. Tickets online (English) up to an hour before.",
            "url": "https://otaru.cc/price/"
          }
        ]
      },
      "yoichi": {
        "kicker": "A day trip from Sapporo (Yoichi distillery and Otaru)",
        "h1": "The Yoichi whisky distillery in the morning; Otaru’s bank street and Sakaimachi in the afternoon; the canal after dark.",
        "lead": "A whisky distillery and the streets of Otaru in one day. Trains between Yoichi and Otaru run only every 60–80 minutes, so the timetable fixes which trains to catch. Take the 8:41 train to Yoichi. Join the Nikka distillery tour you booked (a seminar in December–January) and have lunch at the distillery restaurant. The 13:43 train takes you back to Otaru for the old bank street and Sakaimachi, then Asakusa Bridge as it gets dark. You can add the Mt. Tengu night view after dinner.",
        "favName": "The stone distillery",
        "favText": "Pagoda-roofed kiln towers and stone buildings across the grounds. (Photo: さかおり / CC BY-SA 4.0)",
        "favPhoto": [
          "nikka",
          0
        ],
        "who": [
          "Distillery tours need a booking on the official site (English available, four weeks ahead). Tours are in Japanese only",
          "From December 2026 to January 2027 there are no free tours, only a paid seminar (20 and over, not driving that day)",
          "The distillery is closed 23 Dec–7 Jan. On those days use the 9–10 am course",
          "Trains between Yoichi and Otaru are 60–80 minutes apart; plan around the 13:43 back",
          "It is not clear whether IC cards work between Otaru and Yoichi; a paper ticket is the safe choice",
          "Without a booking you can still visit the museum, shop and restaurant (last entry 15:30)"
        ],
        "dayHead": "Your day",
        "day": [
          {
            "time": "8:41",
            "area": "Sapporo",
            "title": "Change at Otaru for Yoichi",
            "text": "Arrive 10:00. (Photo: MaedaAkihiko / CC0)",
            "photo": [
              "yoichi",
              0
            ],
            "note": "Yoichi 10:00"
          },
          {
            "time": "10:05",
            "area": "Yoichi",
            "title": "The museum and your tour",
            "text": "Enter by the main gate for your booked slot. (Photo: さかおり / CC BY-SA 4.0)",
            "photo": [
              "nikka",
              1
            ]
          },
          {
            "time": "12:00",
            "area": "Yoichi",
            "title": "Lunch at the distillery restaurant",
            "text": "RITA’S KITCHEN is open 10:00–15:50. (Photo: さかおり / CC BY-SA 4.0)",
            "photo": [
              "nikka",
              4
            ]
          },
          {
            "time": "13:43",
            "area": "Yoichi → Otaru",
            "title": "Train to Otaru",
            "text": "Arrive 14:09. (Photo: 皓月旗 / CC BY-SA 4.0)",
            "photo": [
              "otarueki",
              0
            ]
          },
          {
            "time": "14:25",
            "area": "Ironai · Sakaimachi",
            "title": "The bank street and Sakaimachi",
            "text": "A break at Kitaichi Hall. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "kitaichi",
              0
            ]
          },
          {
            "time": "16:30",
            "area": "Asakusa Bridge",
            "title": "The canal as it gets dark",
            "text": "Warehouses and gas lamps in the water. (Photo: Tan Wei Liang Byorn / CC BY-SA 4.0)",
            "photo": [
              "asakusa",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Otaru",
            "title": "Dinner, then the 19:27 to Sapporo",
            "text": "With Mt. Tengu you reach Sapporo at 22:03. (Photo: Haha169 / CC BY-SA 4.0)",
            "photo": [
              "yuhan",
              0
            ],
            "note": "Sapporo 20:01"
          }
        ],
        "dealsLead": "Trains: Sapporo → Yoichi ¥1,380, Yoichi → Otaru ¥470, Otaru → Sapporo ¥800. The distillery tour itself is free (booking needed).",
        "deals": [
          {
            "name": "JR Sapporo → Yoichi",
            "price": "¥1,380",
            "text": "Change at Otaru. Covered by the JR Hokkaido Rail Pass.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "JR Yoichi → Otaru",
            "price": "¥470",
            "text": "Daytime trains at 12:37, 13:43, 15:02. Highway bus ¥560.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Nikka Yoichi guided tour",
            "price": "Free",
            "text": "Booking needed, Japanese only. Dec–Jan: paid seminar only (¥3,000 cash in the November notice).",
            "url": "https://reserva.be/nikkayoichi/news"
          },
          {
            "name": "JR Sapporo–Otaru",
            "price": "¥800 one way",
            "text": "34 minutes on the Rapid Airport, 45–50 on a local train. IC cards work. Covered by the JR Hokkaido Rail Pass and the Sapporo-Noboribetsu Area Pass.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Otaru city buses",
            "price": "¥240 a ride",
            "text": "IC cards work. Riding three times or more? Buy the ¥800 day pass at the Otaru Station bus terminal.",
            "url": "https://tenguyama.ckk.chuo-bus.co.jp/access/"
          },
          {
            "name": "Otaru Canal Cruise (optional)",
            "price": "¥1,800 / ¥2,000",
            "text": "Day / night, about 40 minutes. Tickets online (English) up to an hour before.",
            "url": "https://otaru.cc/price/"
          }
        ]
      }
    }
  }
};
