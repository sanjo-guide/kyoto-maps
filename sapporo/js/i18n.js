/* Page texts in Japanese and English.
   Toshi 個人のマップ。札幌市内で1日（起点は札幌駅〜大通〜すすきののホテル）。
   コースは3つ（一覧の上のボタン）：late＝定番・9:15発（data/routes/sapporo.json）、
   early＝朝いちばん・7:00発（sapporo-early.json）、maruyama＝もう1日あるなら（sapporo-maruyama.json）。
   最初に開くのは late（scripts/sync_sapporo.py）。
   紹介ページは intro に introFor[コース] を上書きして使う。写真は [スポットの id, 写真の番号]。
   写真はすべて Wikimedia Commons（オーナーはまだ北海道の写真を持っていない。行った・食べたと書かない）。
   時刻・料金は2026年11月29日に確認（出典は data/routes/sapporo*.json の sources。データは scripts/build_sapporo_data.py）。
   このファイルは直接直してよい。直したら scripts/sync_sapporo.py の bump を上げてから sync を実行する */
window.SAPPORO_I18N = {
  ja: {
    htmlLang: "ja",
    docTitle: "札幌市内で1日 赤れんが庁舎・大通公園・藻岩山の夜景 Sapporo MAP",
    titleMain: "札幌市内で1日",
    titleSub: "A day in Sapporo",
    howto: "使い方",
    allMaps: "← マップ一覧",
    home: "マップ一覧",
    tabMap: "地図",
    menu: "メニュー",
    list: "一覧",
    listHead: "スポット一覧",
    listNote: "番号は回る順番です。上のボタンでコースを選べます。最初は、時間割どおりに回れる場所が選ばれています。点線は順番を示す線で、実際の道ではありません。",
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
    checkedDate: "2026年11月29日",
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
    pickNote: "最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。出発の駅と、晩ごはんのすすきのは、どの組み合わせでも入ります。",
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
    courseLate: "定番（9〜10時発）",
    courseEarly: "朝いちばん（7:00発）",
    courseMaruyama: "円山と白い恋人パーク",
    swMode: "回り方",
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "入場料・乗り物",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月29日に、各施設の公式サイト、札幌市交通局のページ、乗換案内（12月3日・5日のダイヤ）で確認しました。食事代は別です。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "コースを選ぶ",
          "text": "一覧の上のボタンで「定番」「朝いちばん」「円山と白い恋人パーク」を選べます。定番は9:15にホテルを出る1日、朝いちばんは朝6時から開く市場に合わせて7:00に出る1日、円山は札幌に2泊以上する人の2日目です。"
        },
        {
          "title": "行き先を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられ、そのときの行き方がひとことで出ます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、休館日・冬の歩道・ICカードと1日乗車券など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。ラーメン横丁は最後の番号（すすきの）の中にあります。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（公式サイトなどの情報と、Wikimedia Commons の写真で紹介しています）。"
    },
    introFor: {
      "late": {
        "kicker": "札幌市内で1日（定番：9:15にホテルを出る）",
        "h1": "赤れんがと時計台を見て、二条市場で海鮮。夜は藻岩山から光の海を見下ろす。",
        "lead": "札幌駅・大通・すすきののホテルを9:15に出て、歩いて赤れんが庁舎へ。時計台では10:30の時計の巻き上げ実演を見て、大通公園のテレビ塔に上がったら、二条市場で海鮮のお昼。午後はバスでサッポロビール博物館、そこから地下鉄で円山公園へ出て、バスとロープウェイで藻岩山。日が暮れたばかりの街の光を山頂から見て、夜はすすきので味噌ラーメンかジンギスカン。歩く距離をおさえて、雪の季節でもそのまま回れる順番にしてあります。",
        "favName": "藻岩山の夜景",
        "favText": "標高531mの展望台から、碁盤の目の光が石狩湾まで広がります。公式サイトのトップには、その日の日没と夜景の時刻が出ます（2026年11月29日は日没16:02、夜景16:22）。このコースでは16:35ごろに山頂に着きます。",
        "favPhoto": [
          "moiwa",
          0
        ],
        "who": [
          "赤れんが庁舎は8:45〜21:00（入館300円）。11月15日と12月29日〜1月3日は休館です",
          "時計台は8:45〜17:10（350円）、1月1日〜3日休館。重要文化財なので暖房が効ききれません。上着を着たまま見てください",
          "藻岩山は冬（12月〜3月）は11:00から。上りの最終は21:30。12月31日・1月1日は休業、2027年3月29日〜4月28日は整備点検で全館休業です",
          "サッポロビール博物館は11:00〜18:00（最終入館17:30）。試飲付きガイドツアーは要予約・月曜休止・日本語のみ。自由見学には英語などの音声ガイドがあります",
          "地下鉄・市電・市内のバスは Suica・Kitaca などのICカードで乗れます。地下鉄を3回以上使うなら1日乗車券（平日830円／土日祝520円）が得です",
          "12月から3月は歩道が凍ります。溝のある冬靴か滑り止めを。日の入りは12月で16時ごろ、札幌駅から大通・すすきのは地下街でつながっています",
          "11月20日〜12月25日は大通公園のホワイトイルミネーションとミュンヘン・クリスマス市。さっぽろ雪まつりは2027年2月4日〜11日",
          "このコースにお風呂はありません。温泉に入りたい人は「札幌から日帰り 温泉めぐり」のマップへ"
        ],
        "dayHead": "1日の流れ（定番。平日・土日祝とも）",
        "day": [
          {
            "time": "9:15",
            "area": "札幌駅・大通",
            "title": "ホテルを出て、歩いて赤れんが庁舎へ",
            "text": "札幌駅からも大通からも歩いて10分ほど。寒い日は地下街を通って行けます。",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "9:30",
            "area": "赤れんが庁舎",
            "title": "1888年の赤れんがと、前庭の池",
            "text": "5年あまりの改修を終えて2025年7月に再開館。八角塔に登る観覧もあります。",
            "photo": [
              "akarenga",
              0
            ]
          },
          {
            "time": "10:25",
            "area": "札幌市時計台",
            "title": "10:30の、時計の巻き上げ実演",
            "text": "1881年から動いている重りの塔時計。手で巻き上げる様子は1日1回だけです。",
            "photo": [
              "tokeidai",
              0
            ]
          },
          {
            "time": "11:10",
            "area": "大通公園・テレビ塔",
            "title": "90mの展望台から、碁盤の目を見下ろす",
            "text": "西へまっすぐ伸びる公園の奥に、夜に登る藻岩山が見えます。",
            "photo": [
              "odori",
              0
            ]
          },
          {
            "time": "12:30",
            "area": "二条市場",
            "title": "街なかの市場で、海鮮丼のお昼",
            "text": "創成川の東、狸小路1丁目から徒歩1分。12時台は混むので少し早めに。",
            "photo": [
              "nijo",
              0
            ]
          },
          {
            "time": "14:10",
            "area": "サッポロビール博物館",
            "title": "赤れんがの博物館と、工場直送のビール",
            "text": "自由見学は予約なし、音声ガイドは英語もあります。隣はジンギスカンのビール園。",
            "photo": [
              "beer",
              0
            ]
          },
          {
            "time": "16:35",
            "area": "藻岩山",
            "title": "日の入りから夜景へ",
            "text": "東区役所前15:27→円山公園15:49、16:00のバスで16:18。ロープウェイとミニケーブルカーで山頂。",
            "photo": [
              "moiwa",
              1
            ]
          },
          {
            "time": "19:05",
            "area": "すすきの",
            "title": "味噌ラーメンか、ジンギスカン",
            "text": "ラーメン横丁には17軒ほど。札幌駅までは地下鉄で11分、終電は0時すぎです。",
            "photo": [
              "susukino",
              0
            ]
          }
        ],
        "dealsLead": "地下鉄・市電・バスはICカードで乗れます。入場料は大人1人の金額です。",
        "deals": [
          {
            "name": "北海道庁旧本庁舎（赤れんが庁舎）",
            "price": "300円",
            "text": "8:45〜21:00（最終入館20:30）。大学生・高校生200円、中学生以下無料。八角塔観覧は別に1,200円。",
            "url": "https://www.hokkaido-redbrick.jp/"
          },
          {
            "name": "札幌市時計台",
            "price": "350円",
            "text": "8:45〜17:10（入館17:00まで）。大学生150円、小中学生・高校生は無料。10:30に巻き上げ実演。",
            "url": "https://sapporoshi-tokeidai.jp/inspect/guide.php"
          },
          {
            "name": "さっぽろテレビ塔 展望台",
            "price": "1,200円",
            "text": "9:00〜22:00（展望最終入場21:50）。小中学生600円、幼児無料。2027年1月1日は終日休業。",
            "url": "https://www.tv-tower.co.jp/pricetime.html"
          },
          {
            "name": "サッポロビール博物館（自由見学）",
            "price": "1,000円",
            "text": "11:00〜18:00（最終入館17:30）、予約不要。中学生〜20歳未満500円。試飲付きガイドツアーは2,000円（要予約・月曜休止）。",
            "url": "https://www.sapporobeer.jp/brewery/s_museum/kengaku/"
          },
          {
            "name": "藻岩山（ロープウェイ＋ミニケーブルカー）",
            "price": "往復2,100円",
            "text": "冬は11:00〜22:00、上り最終21:30。小人1,050円。ロープウェイだけの往復は1,400円。",
            "url": "https://mt-moiwa.jp/guide/"
          },
          {
            "name": "地下鉄の1日乗車券",
            "price": "830円／520円",
            "text": "平日は「地下鉄専用1日乗車券」830円、土日祝と12月29日〜1月3日は「ドニチカキップ」520円（現金のみ）。市電とバスには使えません。",
            "url": "https://www.city.sapporo.jp/st/josyaken/doni-chika/donichika.html"
          }
        ]
      },
      "early": {
        "kicker": "札幌市内で1日（朝いちばん：7:00にホテルを出る）",
        "h1": "朝6時から開く市場で海鮮丼。雪の北大を歩いて、街の真ん中へ。",
        "lead": "札幌の朝は市場から始まります。7:00にホテルを出て、地下鉄で二十四軒へ。場外市場の食堂で海鮮丼を食べたら、人のいない北海道大学の構内をポプラ並木まで歩いて、10:00に開く総合博物館（無料）へ。昼前に街の真ん中へ戻って、赤れんが庁舎、時計台、テレビ塔の展望台。お昼は狸小路のラーメンかスープカレー。午後はサッポロビール博物館、夕方からは藻岩山の夜景、夜はすすきの。早く出るぶん、1日に入る場所が2つ増えます。",
        "favName": "北海道大学のポプラ並木",
        "favText": "札幌駅のすぐ北。朝の構内は人が少なく、冬は雪に縁取られた並木道が奥まで続きます。総合博物館は入館無料（10:00〜17:00、月曜休館）。",
        "favPhoto": [
          "hokudai",
          0
        ],
        "who": [
          "場外市場は6:00〜15:00（大型店は17:00まで）。公式サイトがなく、時間は札幌市の観光サイトの情報です。店によって違い、現金だけの店もあります",
          "北海道大学総合博物館は10:00〜17:00、月曜休館（入館無料）。構内そのものはいつでも歩けます",
          "赤れんが庁舎は8:45〜21:00（300円）、時計台は8:45〜17:10（350円）。時計台の巻き上げ実演は10:30の1回だけなので、このコースでは見られません",
          "サッポロビール博物館は11:00〜18:00（最終入館17:30）。試飲付きガイドツアー（要予約・月曜休止）に入りたい人は、15:00以降の回を取ってください",
          "藻岩山は冬（12月〜3月）は11:00から、上りの最終は21:30。12月31日・1月1日は休業です",
          "このコースは地下鉄を4回以上使います。1日乗車券（平日830円／土日祝520円）のほうが安くなります",
          "12月から3月は歩道が凍ります。朝いちばんは除雪前のこともあるので、溝のある冬靴か滑り止めを",
          "日の入りは12月が16時ちょうどごろ、2月11日で17:00（国立天文台）。外を歩く北大と市場を午前に入れてあります"
        ],
        "dayHead": "1日の流れ（朝いちばん。平日・土日祝とも）",
        "day": [
          {
            "time": "7:00",
            "area": "札幌駅・大通",
            "title": "地下鉄東西線で二十四軒へ",
            "text": "大通7:13発→二十四軒7:22着（250円）。冬は地下街から地下鉄に乗れます。",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "7:30",
            "area": "場外市場",
            "title": "朝6時から開く市場で、海鮮丼",
            "text": "鮮魚店・青果店など約60店。食堂は8時前から開いている店が多いです。",
            "photo": [
              "jogai",
              0
            ]
          },
          {
            "time": "9:20",
            "area": "北海道大学",
            "title": "人のいない構内を、ポプラ並木まで",
            "text": "正門から北へ。10:00に開く総合博物館（無料）に恐竜とマンモスの標本があります。",
            "photo": [
              "hokudai",
              1
            ]
          },
          {
            "time": "11:10",
            "area": "赤れんが庁舎",
            "title": "1888年の赤れんがと、前庭の池",
            "text": "2025年7月に改修を終えて再開館。入館300円、21:00まで開いています。",
            "photo": [
              "akarenga",
              0
            ]
          },
          {
            "time": "12:05",
            "area": "札幌市時計台",
            "title": "1878年の演武場",
            "text": "ビルに囲まれて建っています。中は2階の広間に座って見られます。",
            "photo": [
              "tokeidai",
              0
            ]
          },
          {
            "time": "12:45",
            "area": "大通公園・テレビ塔",
            "title": "展望台から、碁盤の目と藻岩山",
            "text": "地上90m、エレベーターで60秒。夜に登る山が公園の奥に見えます。",
            "photo": [
              "odori",
              0
            ]
          },
          {
            "time": "13:40",
            "area": "狸小路",
            "title": "屋根のある商店街でお昼",
            "text": "東西1kmのアーケード。味噌ラーメン、スープカレー、海鮮がこの一帯にあります。",
            "photo": [
              "tanukikoji",
              0
            ]
          },
          {
            "time": "15:10",
            "area": "サッポロビール博物館",
            "title": "赤れんがの博物館と、工場直送のビール",
            "text": "自由見学は予約なしで入れます。音声ガイドは英語・韓国語・中国語もあります。",
            "photo": [
              "beer",
              0
            ]
          },
          {
            "time": "17:20",
            "area": "藻岩山",
            "title": "夜景をゆっくり見る",
            "text": "円山公園駅前からバス15分。市電からの無料シャトルは平日17:17からです。",
            "photo": [
              "moiwa",
              0
            ]
          },
          {
            "time": "19:20",
            "area": "すすきの",
            "title": "味噌ラーメンか、ジンギスカン",
            "text": "ラーメン横丁には17軒ほど。札幌駅までは地下鉄で11分です。",
            "photo": [
              "susukino",
              0
            ]
          }
        ],
        "dealsLead": "朝いちばんのコースは地下鉄を4回以上使うので、1日乗車券が得です。入場料は大人1人の金額です。",
        "deals": [
          {
            "name": "地下鉄の1日乗車券",
            "price": "830円／520円",
            "text": "平日は「地下鉄専用1日乗車券」830円、土日祝と12月29日〜1月3日は「ドニチカキップ」520円（現金のみ）。市電とバスには使えません。",
            "url": "https://www.city.sapporo.jp/st/josyaken/doni-chika/donichika.html"
          },
          {
            "name": "場外市場の海鮮丼",
            "price": "おおよそ1,500〜4,000円",
            "text": "店によって値段と時間が違います。公式サイトがないので、要確認です。現金だけの店もあります。",
            "url": "https://www.sapporo.travel/spot/facility/sapporo_central_wholesale_market/"
          },
          {
            "name": "北海道大学総合博物館",
            "price": "無料",
            "text": "10:00〜17:00、月曜休館（祝日は開館し、翌平日が休館）。構内を歩くのも無料です。",
            "url": "https://www.museum.hokudai.ac.jp/"
          },
          {
            "name": "北海道庁旧本庁舎（赤れんが庁舎）",
            "price": "300円",
            "text": "8:45〜21:00（最終入館20:30）。大学生・高校生200円、中学生以下無料。",
            "url": "https://www.hokkaido-redbrick.jp/"
          },
          {
            "name": "札幌市時計台",
            "price": "350円",
            "text": "8:45〜17:10（入館17:00まで）。小中学生・高校生は無料。",
            "url": "https://sapporoshi-tokeidai.jp/inspect/guide.php"
          },
          {
            "name": "サッポロビール博物館（自由見学）",
            "price": "1,000円",
            "text": "11:00〜18:00（最終入館17:30）、予約不要。ガイドツアーは2,000円（要予約・月曜休止・日本語のみ）。",
            "url": "https://www.sapporobeer.jp/brewery/s_museum/kengaku/"
          },
          {
            "name": "藻岩山（ロープウェイ＋ミニケーブルカー）",
            "price": "往復2,100円",
            "text": "冬は11:00〜22:00、上り最終21:30。円山公園駅前からのバスは片道240円。",
            "url": "https://mt-moiwa.jp/guide/"
          }
        ]
      },
      "maruyama": {
        "kicker": "札幌市内でもう1日（円山と白い恋人パーク：9:15にホテルを出る）",
        "h1": "森の中の神宮と、雪の動物園。午後はお菓子の工場のイルミネーション。",
        "lead": "札幌に2泊以上する人の2日目です。地下鉄で5分の円山公園へ出て、森の参道を歩いて北海道神宮へ。隣の円山動物園は、ホッキョクグマもユキヒョウも雪の日がいちばん元気な動物園です。園内でお昼にして、午後は地下鉄の西の終点、宮の沢の白い恋人パークへ。冬は16:00からイルミネーションが点きます。夕方に大通公園へ戻って、すすきので晩ごはん。小さな子どもと一緒でも回れる1日です。",
        "favName": "雪の円山動物園",
        "favText": "ホッキョクグマ館には水中が見えるトンネルがあります。冬期（11月〜2月末）は9:30〜16:00で、最終入園は15:30。毎月第2・第4水曜日が休園です。",
        "favPhoto": [
          "zoo",
          0
        ],
        "who": [
          "円山動物園は毎月第2・第4水曜日が休園（祝日のときは翌日）。11月と4月は第2水曜を含む週の月〜金、12月29日〜31日も休園です",
          "動物園は冬期（11月1日〜2月末）9:30〜16:00（最終入園15:30）、3月からは16:30まで。入園料は大人800円、中学生以下は無料",
          "白い恋人パークは年中無休。2026年12月1日〜2027年3月31日は10:00〜19:00で、イルミネーションは16:00から（無料）。有料エリアのチケット受付は16:30までです",
          "白い恋人パーク（西）とモエレ沼公園（北東）は街の反対側にあります。どちらか1つにしてください",
          "モエレ沼公園のガラスのピラミッドは月曜休館。「海の噴水」は冬は止まっています",
          "北海道神宮の開門・閉門の時刻は月ごとに変わり、決まった時刻表はありません。公式サイトのお知らせに毎月のように出るので、行く日の時刻を確かめてください",
          "動物園も神宮の参道も坂と雪道です。12月から3月は、溝のある冬靴か滑り止めを",
          "赤れんが庁舎・時計台・ビール博物館・藻岩山は「定番」のコースに入っています（上のボタンで切り替えられます）"
        ],
        "dayHead": "1日の流れ（もう1日あるなら。平日・土日祝とも）",
        "day": [
          {
            "time": "9:15",
            "area": "大通・札幌駅",
            "title": "地下鉄東西線で円山公園へ",
            "text": "大通9:32発→円山公園9:37着（5分・210円）。2番出口から公園へ。",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "9:55",
            "area": "北海道神宮・円山公園",
            "title": "森の参道を歩いて、開拓の守り神へ",
            "text": "1869年に祀られた神社。境内の約1,400本の桜と梅は4月末から5月初めに咲きます。",
            "photo": [
              "jingu",
              0
            ]
          },
          {
            "time": "11:00",
            "area": "円山動物園",
            "title": "雪の日が本番の動物園。お昼も園内で",
            "text": "ホッキョクグマの水中トンネル、ユキヒョウ、ゾウの泳ぐプール。大人800円。",
            "photo": [
              "zoo",
              1
            ]
          },
          {
            "time": "14:22",
            "area": "白い恋人パーク",
            "title": "お菓子の工場と、16:00からの光",
            "text": "円山公園14:04発→宮の沢14:15着、駅から徒歩7分。イルミネーションは無料です。",
            "photo": [
              "shiroi",
              0
            ]
          },
          {
            "time": "17:05",
            "area": "大通公園",
            "title": "イルミネーションの中を歩く",
            "text": "宮の沢16:42発→大通16:58着。テレビ塔の展望台は22:00まで開いています。",
            "photo": [
              "odori",
              0
            ]
          },
          {
            "time": "18:30",
            "area": "すすきの",
            "title": "味噌ラーメンか、ジンギスカン",
            "text": "大通から歩いて10分、冬は地下街で。ラーメン横丁には17軒ほどあります。",
            "photo": [
              "susukino",
              0
            ]
          }
        ],
        "dealsLead": "地下鉄だけで回れるコースです。入場料は大人1人の金額です。",
        "deals": [
          {
            "name": "札幌市円山動物園",
            "price": "800円",
            "text": "冬期（11月〜2月末）9:30〜16:00、最終入園15:30。中学生以下は無料。第2・第4水曜日は休園。",
            "url": "https://www.city.sapporo.jp/zoo/s077/166519.html"
          },
          {
            "name": "白い恋人パーク（有料エリア）",
            "price": "1,200円",
            "text": "16歳以上の料金。3歳以下は無料。イルミネーションと中庭は無料で見られます。",
            "url": "https://www.shiroikoibitopark.jp/"
          },
          {
            "name": "北海道神宮",
            "price": "無料",
            "text": "公式サイトに拝観料の記載はありません。開門・閉門の時刻は月ごとに変わるので、公式サイトのお知らせで確かめてください（要確認）。",
            "url": "http://www.hokkaidojingu.or.jp/"
          },
          {
            "name": "モエレ沼公園",
            "price": "無料",
            "text": "公園もガラスのピラミッドも無料。ピラミッドは9:00〜17:00、月曜休館。環状通東駅からバスです。",
            "url": "https://moerenumapark.jp/"
          },
          {
            "name": "さっぽろテレビ塔 展望台",
            "price": "1,200円",
            "text": "9:00〜22:00（展望最終入場21:50）。小中学生600円。夜のイルミネーションを上から見られます。",
            "url": "https://www.tv-tower.co.jp/pricetime.html"
          },
          {
            "name": "地下鉄の1日乗車券",
            "price": "830円／520円",
            "text": "平日は830円、土日祝と12月29日〜1月3日は520円（現金のみ）。このコースは地下鉄を4回使います。",
            "url": "https://www.city.sapporo.jp/st/josyaken/doni-chika/donichika.html"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: "en",
    docTitle: "A day in Sapporo — Red Brick Office, Odori Park and the night view from Mt. Moiwa",
    titleMain: "A day in Sapporo",
    titleSub: "札幌市内で1日",
    howto: "How to use",
    allMaps: "← All maps",
    home: "All maps",
    tabMap: "Map",
    menu: "Menu",
    list: "Spots",
    listHead: "All spots",
    listNote: "The numbers are the order you walk them. Pick a course with the buttons above. To start with, the places that fit the timetable are already chosen. The dotted line shows the order, not the actual streets.",
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
    checkedDate: "Nov 29, 2026",
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
    pickNote: "To start with, the places that fit the timetable are already chosen, and the suggested times are for that combination. The station you start from and dinner in Susukino are always included.",
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
    courseLate: "Classic (leave 9–10)",
    courseEarly: "Early start (leave 7:00)",
    courseMaruyama: "Maruyama & Shiroi Koibito",
    swMode: "How to go",
    intro: {
      "favLabel": "Best moment",
      "whoHead": "Good to know",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Admission and transport",
      "dealsMore": "See the official site or route planner",
      "dealsNote": "Prices are for one adult. Checked on 29 November 2026 against each place’s official website, the Sapporo transport bureau’s pages and a route planner (the 3 and 5 December timetable). Meals are extra.",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick a course",
          "text": "Use the buttons above the list to choose “Classic”, “Early start” or “Maruyama & Shiroi Koibito”. The classic day leaves your hotel at 9:15; the early day leaves at 7:00 for a market that opens at 06:00; Maruyama is a second day for anyone staying two nights or more."
        },
        {
          "title": "Swap places in and out",
          "text": "Only the places that fit the timetable are chosen at first. Tap “Want to go” / “Going” to swap them, and a line appears telling you how the day then works."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that trip people up at the door come first: closing days, icy pavements, IC cards and day passes. Times and prices are below them."
        },
        {
          "title": "Search the route in Google Maps",
          "text": "“Open in Google Maps” on each spot takes you straight to directions. The ramen alley is inside the last stop, Susukino."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi, put together from official websites and other sources, with photos from Wikimedia Commons."
    },
    introFor: {
      "late": {
        "kicker": "A day in central Sapporo (classic: leave your hotel at 9:15)",
        "h1": "Red brick and a clock tower, seafood at the market, and a sea of lights from Mt. Moiwa.",
        "lead": "Leave a hotel near Sapporo Station, Odori or Susukino at 9:15 and walk to the Red Brick Office. At the Clock Tower, watch the 10:30 winding of the clock; go up the TV Tower in Odori Park; then have a seafood lunch at Nijo Market. In the afternoon a bus takes you to the Sapporo Beer Museum, and the subway and another bus to the ropeway up Mt. Moiwa, where the city lights have just come on. Dinner is miso ramen or grilled lamb in Susukino. The walking is kept short and the order works just as well in the snow.",
        "favName": "The night view from Mt. Moiwa",
        "favText": "From the observatory, 531 m up, the grid of lights spreads all the way to Ishikari Bay. The front page of the operator’s site gives each day’s sunset and night-view times — on 29 November 2026, 16:02 and 16:22. On this course you reach the summit at about 16:35.",
        "favPhoto": [
          "moiwa",
          0
        ],
        "who": [
          "The Red Brick Office is open 8:45–21:00 (¥300), and closed on 15 November and 29 December – 3 January",
          "The Clock Tower is open 8:45–17:10 (¥350) and closed 1–3 January. As a protected building its heating cannot keep up in winter, so keep your coat on",
          "Mt. Moiwa starts at 11:00 in winter (December to March), with the last ride up at 21:30. Closed 31 December and 1 January, and for maintenance 29 March – 28 April 2027",
          "The Sapporo Beer Museum is open 11:00–18:00 (last entry 17:30). The tasting tour needs a booking, does not run on Mondays and is guided in Japanese only; the self-guided visit has an English audio guide",
          "Suica, Kitaca and the other IC cards work on the subway, tram and city buses. Three or more subway rides and a day pass is cheaper (¥830 on weekdays, ¥520 at weekends)",
          "From December to March the pavements turn to ice; wear winter boots with a deep tread or clip-on grips. Sunset is around 16:00 in December, and an underground walkway links the station, Odori and Susukino",
          "From 20 November to 25 December, Odori Park holds the White Illumination and the Munich Christmas Market. The Snow Festival runs 4–11 February 2027",
          "There is no hot spring on this course. For a bath, see the “Onsen day trips from Sapporo” map"
        ],
        "dayHead": "The day, hour by hour (classic; the same every day of the week)",
        "day": [
          {
            "time": "9:15",
            "area": "Sapporo Station / Odori",
            "title": "Leave the hotel and walk to the Red Brick Office",
            "text": "About ten minutes from either the station or Odori, and you can go underground on a cold day.",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "9:30",
            "area": "Red Brick Office",
            "title": "An 1888 brick building and the pond in its garden",
            "text": "Reopened in July 2025 after five years of restoration. You can also pay to climb the octagonal tower.",
            "photo": [
              "akarenga",
              0
            ]
          },
          {
            "time": "10:25",
            "area": "Sapporo Clock Tower",
            "title": "The 10:30 winding of the clock",
            "text": "A weight-driven tower clock running since 1881, wound by hand once a day.",
            "photo": [
              "tokeidai",
              0
            ]
          },
          {
            "time": "11:10",
            "area": "Odori Park & the TV Tower",
            "title": "Looking down on the grid from 90 m up",
            "text": "The park runs dead straight to the west, with tonight’s hill, Mt. Moiwa, behind it.",
            "photo": [
              "odori",
              0
            ]
          },
          {
            "time": "12:30",
            "area": "Nijo Market",
            "title": "A seafood bowl at a market in the middle of town",
            "text": "East of Sosei River, a minute from Tanukikoji 1-chome. Noon is busy, so come a little early.",
            "photo": [
              "nijo",
              0
            ]
          },
          {
            "time": "14:10",
            "area": "Sapporo Beer Museum",
            "title": "A red brick museum and beer brewed for the site",
            "text": "No booking needed for the self-guided visit, and the audio guide has English. Grilled lamb next door.",
            "photo": [
              "beer",
              0
            ]
          },
          {
            "time": "16:35",
            "area": "Mt. Moiwa",
            "title": "From sunset into the night view",
            "text": "Higashi-kuyakusho-mae 15:27 to Maruyama-koen 15:49, the 16:00 bus arriving 16:18, then the ropeway and cable car.",
            "photo": [
              "moiwa",
              1
            ]
          },
          {
            "time": "19:05",
            "area": "Susukino",
            "title": "Miso ramen, or grilled lamb",
            "text": "Some seventeen shops in the ramen alley. Sapporo Station is 11 minutes by subway, last trains after midnight.",
            "photo": [
              "susukino",
              0
            ]
          }
        ],
        "dealsLead": "IC cards work on the subway, tram and buses. Admission prices are for one adult.",
        "deals": [
          {
            "name": "Former Hokkaido Government Office (Red Brick)",
            "price": "¥300",
            "text": "8:45–21:00 (last entry 20:30). Students ¥200, junior high and younger free. The octagonal tower tour is ¥1,200 extra.",
            "url": "https://www.hokkaido-redbrick.jp/"
          },
          {
            "name": "Sapporo Clock Tower",
            "price": "¥350",
            "text": "8:45–17:10 (last entry 17:00). University students ¥150, school students up to high school free. Clock wound at 10:30.",
            "url": "https://sapporoshi-tokeidai.jp/english/"
          },
          {
            "name": "Sapporo TV Tower observatory",
            "price": "¥1,200",
            "text": "9:00–22:00 (last entry 21:50). School students ¥600, pre-school free. Closed all day on 1 January 2027.",
            "url": "https://www.tv-tower.co.jp/pricetime.html"
          },
          {
            "name": "Sapporo Beer Museum (self-guided)",
            "price": "¥1,000",
            "text": "11:00–18:00 (last entry 17:30), no booking. Ages 13–19 ¥500. The tasting tour is ¥2,000 (booking required, not on Mondays).",
            "url": "https://www.sapporobeer.jp/english/"
          },
          {
            "name": "Mt. Moiwa (ropeway + cable car)",
            "price": "¥2,100 return",
            "text": "11:00–22:00 in winter, last ride up 21:30. Children ¥1,050. The ropeway alone is ¥1,400 return.",
            "url": "https://mt-moiwa.jp/guide/"
          },
          {
            "name": "Subway day pass",
            "price": "¥830 / ¥520",
            "text": "¥830 on weekdays (Subway 1-Day Card); ¥520 at weekends, on holidays and 29 Dec – 3 Jan (Donichika Kippu, cash only). Subway only.",
            "url": "https://www.city.sapporo.jp/st/s107/77494.html"
          }
        ]
      },
      "early": {
        "kicker": "A day in central Sapporo (early start: leave your hotel at 7:00)",
        "h1": "A seafood bowl at a market open from 06:00, a snowy campus, then the centre of town.",
        "lead": "Sapporo’s morning begins at the market. Leave at 7:00, ride the subway to Nijuyonken, and have a seafood rice bowl at the Curb Market. Then walk the empty campus of Hokkaido University out to the poplar avenue, and go into its free museum when it opens at 10:00. Back in the centre before noon for the Red Brick Office, the Clock Tower and the TV Tower observatory; lunch is ramen or soup curry in the Tanukikoji arcade. The afternoon is the Sapporo Beer Museum, the evening the night view from Mt. Moiwa, and the night Susukino. Leaving early fits two more places into the day.",
        "favName": "The poplar avenue at Hokkaido University",
        "favText": "Just north of Sapporo Station. The campus is almost empty in the morning, and in winter the avenue runs away between walls of snow. The university museum is free (10:00–17:00, closed Mondays).",
        "favPhoto": [
          "hokudai",
          0
        ],
        "who": [
          "The Curb Market is open 6:00–15:00 (larger shops to 17:00). It has no official website, so the hours come from the city’s tourism site; individual shops differ and some take cash only",
          "The Hokkaido University Museum is open 10:00–17:00 and closed on Mondays (free). The campus itself is open at any hour",
          "The Red Brick Office is open 8:45–21:00 (¥300) and the Clock Tower 8:45–17:10 (¥350). The clock is wound only once a day, at 10:30, which this course misses",
          "The Sapporo Beer Museum is open 11:00–18:00 (last entry 17:30). If you want the tasting tour (booking required, not on Mondays), book a slot from 15:00",
          "Mt. Moiwa starts at 11:00 in winter (December to March), last ride up 21:30, and closes on 31 December and 1 January",
          "This course uses the subway four times or more, so a day pass works out cheaper (¥830 on weekdays, ¥520 at weekends)",
          "From December to March the pavements turn to ice, and first thing in the morning they may not be cleared yet. Wear winter boots with a deep tread, or clip-on grips",
          "Sunset is around 16:00 through December and 17:00 by 11 February (National Astronomical Observatory), so the outdoor parts — the market and the campus — come in the morning"
        ],
        "dayHead": "The day, hour by hour (early start; the same every day of the week)",
        "day": [
          {
            "time": "7:00",
            "area": "Sapporo Station / Odori",
            "title": "The Tozai subway line to Nijuyonken",
            "text": "Odori 7:13 → Nijuyonken 7:22 (¥250). In winter you can reach the subway underground.",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "7:30",
            "area": "Curb Market",
            "title": "A seafood bowl at a market open from 06:00",
            "text": "Some sixty fishmongers and greengrocers. Most of the restaurants open before 08:00.",
            "photo": [
              "jogai",
              0
            ]
          },
          {
            "time": "9:20",
            "area": "Hokkaido University",
            "title": "An empty campus, out to the poplar avenue",
            "text": "North from the main gate. The free museum, open at 10:00, has a dinosaur and mammoth material.",
            "photo": [
              "hokudai",
              1
            ]
          },
          {
            "time": "11:10",
            "area": "Red Brick Office",
            "title": "An 1888 brick building and the pond in its garden",
            "text": "Reopened in July 2025 after restoration. ¥300, and open until 21:00.",
            "photo": [
              "akarenga",
              0
            ]
          },
          {
            "time": "12:05",
            "area": "Sapporo Clock Tower",
            "title": "An 1878 drill hall",
            "text": "Hemmed in by office towers. Inside, you can sit in the upstairs hall.",
            "photo": [
              "tokeidai",
              0
            ]
          },
          {
            "time": "12:45",
            "area": "Odori Park & the TV Tower",
            "title": "The grid, and Mt. Moiwa, from the observatory",
            "text": "Ninety metres up, 60 seconds by lift. Tonight’s hill stands behind the park.",
            "photo": [
              "odori",
              0
            ]
          },
          {
            "time": "13:40",
            "area": "Tanukikoji",
            "title": "Lunch in a covered arcade",
            "text": "A kilometre of roofed street. Miso ramen, soup curry and seafood are all in these blocks.",
            "photo": [
              "tanukikoji",
              0
            ]
          },
          {
            "time": "15:10",
            "area": "Sapporo Beer Museum",
            "title": "A red brick museum and beer brewed for the site",
            "text": "The self-guided visit needs no booking, and the audio guide has English, Korean and Chinese.",
            "photo": [
              "beer",
              0
            ]
          },
          {
            "time": "17:20",
            "area": "Mt. Moiwa",
            "title": "Time to take the night view slowly",
            "text": "Fifteen minutes by bus from Maruyama-koen Station. The free shuttle from the tram only starts at 17:17 on weekdays.",
            "photo": [
              "moiwa",
              0
            ]
          },
          {
            "time": "19:20",
            "area": "Susukino",
            "title": "Miso ramen, or grilled lamb",
            "text": "Some seventeen shops in the ramen alley. Sapporo Station is 11 minutes by subway.",
            "photo": [
              "susukino",
              0
            ]
          }
        ],
        "dealsLead": "The early course uses the subway four times or more, so a day pass pays off. Admission prices are for one adult.",
        "deals": [
          {
            "name": "Subway day pass",
            "price": "¥830 / ¥520",
            "text": "¥830 on weekdays (Subway 1-Day Card); ¥520 at weekends, on holidays and 29 Dec – 3 Jan (Donichika Kippu, cash only). Subway only.",
            "url": "https://www.city.sapporo.jp/st/s107/77494.html"
          },
          {
            "name": "A seafood bowl at the Curb Market",
            "price": "roughly ¥1,500–4,000",
            "text": "Prices and hours vary by shop. The market has no official website, so this should be checked; some shops take cash only.",
            "url": "https://www.sapporo.travel/spot/facility/sapporo_central_wholesale_market/"
          },
          {
            "name": "Hokkaido University Museum",
            "price": "Free",
            "text": "10:00–17:00, closed Mondays (open on public holidays, closed the next weekday). Walking the campus is free too.",
            "url": "https://www.museum.hokudai.ac.jp/"
          },
          {
            "name": "Former Hokkaido Government Office (Red Brick)",
            "price": "¥300",
            "text": "8:45–21:00 (last entry 20:30). Students ¥200, junior high and younger free.",
            "url": "https://www.hokkaido-redbrick.jp/"
          },
          {
            "name": "Sapporo Clock Tower",
            "price": "¥350",
            "text": "8:45–17:10 (last entry 17:00). School students up to high school free.",
            "url": "https://sapporoshi-tokeidai.jp/english/"
          },
          {
            "name": "Sapporo Beer Museum (self-guided)",
            "price": "¥1,000",
            "text": "11:00–18:00 (last entry 17:30), no booking. The tasting tour is ¥2,000 (booking required, not on Mondays, Japanese only).",
            "url": "https://www.sapporobeer.jp/english/"
          },
          {
            "name": "Mt. Moiwa (ropeway + cable car)",
            "price": "¥2,100 return",
            "text": "11:00–22:00 in winter, last ride up 21:30. The bus from Maruyama-koen Station is ¥240 each way.",
            "url": "https://mt-moiwa.jp/guide/"
          }
        ]
      },
      "maruyama": {
        "kicker": "A second day in Sapporo (Maruyama & Shiroi Koibito: leave at 9:15)",
        "h1": "A shrine in the woods, a zoo in the snow, and a chocolate factory lit up for the evening.",
        "lead": "This is the second day for anyone staying two nights or more. Ride five minutes on the subway to Maruyama-koen, walk the forest approach to Hokkaido Jingu, and go next door to Maruyama Zoo, where the polar bears and snow leopards are at their best in the snow. Have lunch inside the zoo, then take the subway to its western terminus, Miyanosawa, for Shiroi Koibito Park, lit from 16:00 in winter. Come back to Odori Park towards evening and have dinner in Susukino. An easy day, young children included.",
        "favName": "Maruyama Zoo in the snow",
        "favText": "The polar bear house has a tunnel that lets you watch them underwater. In winter (November to the end of February) the zoo is open 9:30–16:00, with last entry at 15:30, and it closes on the second and fourth Wednesday of each month.",
        "favPhoto": [
          "zoo",
          0
        ],
        "who": [
          "Maruyama Zoo closes on the second and fourth Wednesday of each month (the next day if that is a holiday), for the whole Monday-to-Friday week containing the second Wednesday in November and April, and 29–31 December",
          "In winter (1 November – end of February) the zoo is open 9:30–16:00 (last entry 15:30); from March until 16:30. Adults ¥800, junior high school students and younger free",
          "Shiroi Koibito Park is open every day. From 1 December 2026 to 31 March 2027 it opens 10:00–19:00 with the lights on from 16:00 (free); the ticket desk for the paid area closes at 16:30",
          "Shiroi Koibito Park is in the west and Moerenuma Park in the north-east, on opposite sides of the city. Choose one",
          "The Glass Pyramid in Moerenuma Park closes on Mondays, and the Sea Fountain does not run in winter",
          "Hokkaido Jingu’s gate times change with the month and no fixed timetable is published; the shrine posts a notice almost every month, so look up the times for your date",
          "Both the zoo and the shrine approach are sloping and snowy. From December to March, wear winter boots with a deep tread or clip-on grips",
          "The Red Brick Office, the Clock Tower, the Beer Museum and Mt. Moiwa are on the “Classic” course (switch with the buttons above)"
        ],
        "dayHead": "The day, hour by hour (second day; the same every day of the week)",
        "day": [
          {
            "time": "9:15",
            "area": "Odori / Sapporo Station",
            "title": "The Tozai subway line to Maruyama-koen",
            "text": "Odori 9:32 → Maruyama-koen 9:37 (5 min, ¥210). Out of Exit 2 and into the park.",
            "photo": [
              "eki",
              0
            ]
          },
          {
            "time": "9:55",
            "area": "Hokkaido Jingu & Maruyama Park",
            "title": "A forest approach to the shrine of the settlers",
            "text": "Founded in 1869. Its 1,400 cherry and plum trees bloom in late April and early May.",
            "photo": [
              "jingu",
              0
            ]
          },
          {
            "time": "11:00",
            "area": "Maruyama Zoo",
            "title": "A zoo that comes alive in the snow — lunch inside",
            "text": "The polar bears’ underwater tunnel, snow leopards, and elephants swimming indoors. ¥800.",
            "photo": [
              "zoo",
              1
            ]
          },
          {
            "time": "14:22",
            "area": "Shiroi Koibito Park",
            "title": "A chocolate factory, and lights from 16:00",
            "text": "Maruyama-koen 14:04 → Miyanosawa 14:15, then seven minutes on foot. The illumination is free.",
            "photo": [
              "shiroi",
              0
            ]
          },
          {
            "time": "17:05",
            "area": "Odori Park",
            "title": "Walking through the illumination",
            "text": "Miyanosawa 16:42 → Odori 16:58. The TV Tower observatory stays open until 22:00.",
            "photo": [
              "odori",
              0
            ]
          },
          {
            "time": "18:30",
            "area": "Susukino",
            "title": "Miso ramen, or grilled lamb",
            "text": "Ten minutes’ walk from Odori, or underground in winter. Some seventeen shops in the ramen alley.",
            "photo": [
              "susukino",
              0
            ]
          }
        ],
        "dealsLead": "The whole course runs on the subway. Admission prices are for one adult.",
        "deals": [
          {
            "name": "Sapporo Maruyama Zoo",
            "price": "¥800",
            "text": "Winter (Nov – end of Feb) 9:30–16:00, last entry 15:30. Junior high and younger free. Closed the 2nd and 4th Wednesday.",
            "url": "https://www.city.sapporo.jp/zoo/s077/166519.html"
          },
          {
            "name": "Shiroi Koibito Park (paid area)",
            "price": "¥1,200",
            "text": "For ages 16 and up; under-4s free. The illumination and the courtyard are free to walk through.",
            "url": "https://www.shiroikoibitopark.jp/en/"
          },
          {
            "name": "Hokkaido Jingu",
            "price": "Free",
            "text": "No admission fee is listed. The gate times change every month; check the shrine’s notices.",
            "url": "http://www.hokkaidojingu.or.jp/"
          },
          {
            "name": "Moerenuma Park",
            "price": "Free",
            "text": "No admission charge is listed for the park or the pyramid. The pyramid is open 9:00–17:00, closed Mondays. Bus from Kanjo-dori-higashi Station.",
            "url": "https://moerenumapark.jp/"
          },
          {
            "name": "Sapporo TV Tower observatory",
            "price": "¥1,200",
            "text": "9:00–22:00 (last entry 21:50). School students ¥600. A view down onto the evening illumination.",
            "url": "https://www.tv-tower.co.jp/pricetime.html"
          },
          {
            "name": "Subway day pass",
            "price": "¥830 / ¥520",
            "text": "¥830 on weekdays; ¥520 at weekends, on holidays and 29 Dec – 3 Jan (cash only). This course uses the subway four times.",
            "url": "https://www.city.sapporo.jp/st/s107/77494.html"
          }
        ]
      }
    }
  }
};
