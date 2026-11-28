/* Page texts in Japanese and English.
   Toshi 個人のマップ。函館で1日。写真はすべて Wikimedia Commons（だれかが行った・食べたとは書かない）。
   コースは3つ（一覧の上のボタン）：late＝9〜10時に出る（最初に開く。data/routes/hakodate.json）、early＝6時台に出る（hakodate-early.json）、
   sapporo＝札幌から1泊2日（hakodate-sapporo.json）。intro はどのコースにも共通の項目で、コースで変わる項目は introFor[コース] が
   app.js で上書きされる（scripts/sync_hakodate.py）。写真は [スポットの id, 写真の番号]。
   時刻・料金は2026年11月28日に確認（出典は data/routes/hakodate.json の sources）。直すときはこのファイルを直接直してよい */
window.HAKODATE_I18N = {
  ja: {
    htmlLang: "ja",
    docTitle: "函館で1日 Hakodate MAP",
    titleMain: "函館",
    titleSub: "One day in Hakodate",
    howto: "使い方",
    allMaps: "← マップ一覧",
    home: "マップ一覧",
    tabMap: "地図",
    menu: "メニュー",
    list: "一覧",
    listHead: "スポット一覧",
    listNote: "番号は回る順番です。冬（12〜1月）の日の入りに合わせた時間割で、ほかの季節の函館山の時刻はスポットの中にあります。点線は順番を示す線で、実際の道ではありません。",
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
    checkedDate: "2026年11月28日",
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
    pickNote: "最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。函館駅は、どの組み合わせでも入ります。",
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
    courseLate: "9〜10時に出る\n朝市・五稜郭・夜景",
    courseEarly: "6時台に出る\n朝の元町・湯の川",
    courseSapporo: "札幌から\n1泊2日",
    swMode: "回り方",
    intro: {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "市電・ロープウェイ・入場料",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月28日に、各施設の公式サイトと乗換案内（12月3日・5日のダイヤ）で確認しました。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "コースを選ぶ",
          "text": "一覧の上のボタンで「9〜10時に出る」「6時台に出る」「札幌から1泊2日」を選びます。時間割と番号が変わります。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、休みの日・現金のみ・タトゥー・冬の注意など、入口で困ることが先に出ます。時刻と料金は、その下にあります。"
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
        "kicker": "函館で1日（9〜10時に出る）",
        "h1": "朝市で朝ごはん、星の形の城。日が沈む前に山へ上がって、町の明かりを待つ。",
        "lead": "函館山の夜景は、空に青みが残る日の入りの20〜30分あとがいちばんきれいです。この時間割は、そのころ山の上にいられるように組んであります。函館駅のまわりのホテルを9:30に出て、朝市で朝ごはん。市電で五稜郭へ行ってタワーと公園を歩き、お昼のあと元町の坂と教会へ。日の入りの30分前にロープウェイで上がり、下りたら明かりのついた赤レンガ倉庫と晩ごはんです。",
        "favName": "函館山の夜景",
        "favText": "空に青みが残る、日の入りの20〜30分あとがいちばんきれいです。（写真：Perry Li / CC BY-SA 2.0）",
        "favPhoto": [
          "ropeway",
          0
        ],
        "who": [
          "市電は1回250〜300円、1日乗車券800円。SuicaなどのICカードも使えます",
          "函館山は、日の入りの30〜40分前の便で上へ（12月は15:30ごろ）。雲と強い風の日は見えません",
          "冬の坂と歩道は凍ります。底に溝の深い、滑りにくい靴で",
          "朝市は14時すぎに閉まります",
          "ハリストス正教会の中は撮影不可。12/25〜2月末は中に入れません",
          "湯の川温泉の日帰り入浴は、タトゥーの決まりが公式に書かれていません（足湯はだれでも）"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "9:30",
            "area": "函館駅",
            "title": "駅の横の朝市で朝ごはん",
            "text": "どんぶり横丁市場で、店の前のメニューを見て決めます。（写真：bryan... / CC BY-SA 2.0）",
            "photo": [
              "asaichi",
              0
            ]
          },
          {
            "time": "11:10",
            "area": "五稜郭",
            "title": "タワーから星の形を見て、公園へ",
            "text": "市電は函館駅前10:32発。奉行所は靴を脱いで入ります。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "tower",
              0
            ],
            "note": "市電10:32"
          },
          {
            "time": "13:00",
            "area": "五稜郭",
            "title": "塩ラーメンかハンバーガーのお昼",
            "text": "タワーのすぐそばに2軒。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "hiru",
              0
            ]
          },
          {
            "time": "14:35",
            "area": "元町",
            "title": "八幡坂と教会",
            "text": "市電は五稜郭公園前13:58発。坂の上から港を見下ろします。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "hachiman",
              0
            ],
            "note": "市電13:58"
          },
          {
            "time": "15:30",
            "area": "函館山",
            "title": "ロープウェイで上がって、暗くなるのを待つ",
            "text": "12月の日の入りは16:07ごろ。17:00ごろ下りの列へ。（写真：Perry Li / CC BY-SA 2.0）",
            "photo": [
              "ropeway",
              0
            ],
            "note": "往復1,800円"
          },
          {
            "time": "17:30",
            "area": "ベイエリア",
            "title": "夜の赤レンガ倉庫と晩ごはん",
            "text": "12月は18:00にツリーの点灯式と花火。（写真：掬茶 / CC BY-SA 4.0）",
            "photo": [
              "kanemori",
              0
            ]
          }
        ],
        "dealsLead": "市電に3回乗るので、1日乗車券（800円）が楽です。そのほかは、入ったものの分だけ。",
        "deals": [
          {
            "name": "市電1日乗車券",
            "price": "800円",
            "text": "車内・駅の観光案内所で。1回ずつ払うと250〜300円。",
            "url": "https://www.city.hakodate.hokkaido.jp/tram/value-ticket/"
          },
          {
            "name": "函館山ロープウェイ",
            "price": "往復1,800円",
            "text": "カード・電子マネー可。15分おき。",
            "url": "https://334.co.jp/ropeway/price/"
          },
          {
            "name": "五稜郭タワー",
            "price": "1,200円",
            "text": "9:00〜18:00、休みなし。",
            "url": "https://www.goryokaku-tower.co.jp/price/"
          },
          {
            "name": "箱館奉行所",
            "price": "500円",
            "text": "11〜3月は受付16:45まで。公園は無料。",
            "url": "https://hakodate-bugyosho.jp/information/"
          },
          {
            "name": "旧函館区公会堂（寄り道）",
            "price": "300円",
            "text": "11〜3月は17:00まで。",
            "url": "https://hakodate-kokaido.jp/"
          },
          {
            "name": "ハリストス正教会",
            "price": "献金200円",
            "text": "日曜は13:00から。12/25〜2月末は拝観休止。",
            "url": "https://www.orthodox-hakodate.jp/services"
          },
          {
            "name": "湯の川温泉の日帰り入浴（寄り道）",
            "price": "550〜1,200円",
            "text": "足湯は無料（9:00〜21:00）。",
            "url": "https://hakodate-yunokawa.jp/dayspa/"
          }
        ]
      },
      "early": {
        "kicker": "函館で1日（6時台に出る）",
        "h1": "団体の人が来る前の朝市。人も車もいない八幡坂。最後は温泉であたたまる。",
        "lead": "昼は人と車でいっぱいの八幡坂も、朝8時は静かです。6:30にホテルを出て、空いている朝市で朝ごはん。海ぞいを歩いて、8時の八幡坂と元町へ。開いたばかりの公会堂と教会を見て、赤レンガ倉庫でひと休み。昼は五稜郭、夕方は函館山の夜景、最後に市電で湯の川温泉へ行ってから晩ごはんです。",
        "favName": "朝8時の八幡坂",
        "favText": "昼は人と車でいっぱいの坂が、この時間は静かです。（写真：くろふね / CC BY 4.0）",
        "favPhoto": [
          "hachiman",
          0
        ],
        "who": [
          "市電は1回250〜300円、1日乗車券800円。SuicaなどのICカードも使えます",
          "函館山は、日の入りの30〜40分前の便で上へ（12月は15:30ごろ）。雲と強い風の日は見えません",
          "冬の坂と歩道は凍ります。底に溝の深い、滑りにくい靴で",
          "12〜1月の日の出は7時ごろ。朝市に着くときはまだ暗いです",
          "ハリストス正教会は10:00から（日曜は13:00から。12/25〜2月末は中に入れません）",
          "湯の川温泉の日帰り入浴は、タトゥーの決まりが公式に書かれていません（足湯はだれでも）"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "6:35",
            "area": "函館駅",
            "title": "空いている朝市で朝ごはん",
            "text": "1〜4月は6:00から、5〜12月は5:00から。（写真：bryan... / CC BY-SA 2.0）",
            "photo": [
              "asaichi",
              0
            ]
          },
          {
            "time": "8:00",
            "area": "元町",
            "title": "人のいない八幡坂と大三坂",
            "text": "朝市から海ぞいを歩いて30分。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "hachiman",
              0
            ]
          },
          {
            "time": "9:00",
            "area": "元町",
            "title": "開いたばかりの公会堂、10時に教会",
            "text": "バルコニーから港が見えます。（写真：掬茶 / CC BY-SA 4.0）",
            "photo": [
              "kokaido",
              0
            ],
            "note": "300円"
          },
          {
            "time": "10:30",
            "area": "ベイエリア",
            "title": "赤レンガ倉庫でひと休み",
            "text": "店は9:30から。（写真：掬茶 / CC BY-SA 4.0）",
            "photo": [
              "kanemori",
              0
            ]
          },
          {
            "time": "12:05",
            "area": "五稜郭",
            "title": "お昼、タワー、公園",
            "text": "市電は十字街11:22発。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "tower",
              0
            ],
            "note": "市電11:22"
          },
          {
            "time": "15:30",
            "area": "函館山",
            "title": "日の入り前に上がって夜景を待つ",
            "text": "市電は五稜郭公園前14:46発。（写真：Perry Li / CC BY-SA 2.0）",
            "photo": [
              "ropeway",
              0
            ],
            "note": "市電14:46"
          },
          {
            "time": "18:15",
            "area": "湯の川温泉",
            "title": "足湯かお風呂、戻って晩ごはん",
            "text": "市電は十字街17:39発、帰りは19:37発。（写真：OraMAAG / CC BY 4.0）",
            "photo": [
              "yunokawa",
              0
            ],
            "note": "市電17:39"
          }
        ],
        "dealsLead": "市電に4回乗ります。1日乗車券（800円）を買ってください。",
        "deals": [
          {
            "name": "市電1日乗車券",
            "price": "800円",
            "text": "車内・駅の観光案内所で。1回ずつ払うと250〜300円。",
            "url": "https://www.city.hakodate.hokkaido.jp/tram/value-ticket/"
          },
          {
            "name": "旧函館区公会堂",
            "price": "300円",
            "text": "9:00から。11〜3月は17:00まで。",
            "url": "https://hakodate-kokaido.jp/"
          },
          {
            "name": "ハリストス正教会",
            "price": "献金200円",
            "text": "10:00から（日曜13:00から）。12/25〜2月末は拝観休止。",
            "url": "https://www.orthodox-hakodate.jp/services"
          },
          {
            "name": "五稜郭タワー",
            "price": "1,200円",
            "text": "9:00〜18:00、休みなし。",
            "url": "https://www.goryokaku-tower.co.jp/price/"
          },
          {
            "name": "箱館奉行所",
            "price": "500円",
            "text": "11〜3月は受付16:45まで。",
            "url": "https://hakodate-bugyosho.jp/information/"
          },
          {
            "name": "函館山ロープウェイ",
            "price": "往復1,800円",
            "text": "カード・電子マネー可。",
            "url": "https://334.co.jp/ropeway/price/"
          },
          {
            "name": "湯の川温泉の日帰り入浴",
            "price": "550〜1,200円",
            "text": "足湯は無料（9:00〜21:00）。",
            "url": "https://hakodate-yunokawa.jp/dayspa/"
          }
        ]
      },
      "sapporo": {
        "kicker": "札幌から1泊2日",
        "h1": "着いた日の夕方は、函館山の夜景。次の日は五稜郭と温泉。",
        "lead": "札幌から特急で3時間50分。1泊すると、着いた日の夕方に函館山、次の日に開いたばかりの五稜郭と湯の川温泉まで回れます。札幌8:43の特急北斗で函館へ（12:33着）。朝市でお昼を食べて、赤レンガ倉庫、八幡坂と教会、夕暮れの函館山へ。2日目は開いたばかりの五稜郭タワーと公園、湯の川温泉を回って、17:55の特急で札幌に21:41に戻ります。",
        "favName": "函館山の夜景",
        "favText": "1日目に雲で見えなくても、2日目の夕方にもう一度上がれます（帰りは18:43の最終）。（写真：Perry Li / CC BY-SA 2.0）",
        "favPhoto": [
          "ropeway",
          0
        ],
        "who": [
          "特急北斗は全部の席が指定席。片道9,770円。行きと帰りの席を先に取ります",
          "JR北海道レールパス（全線）なら指定席も追加料金なし",
          "帰りの最終は函館18:43発（札幌22:41着）",
          "市電は1回250〜300円、1日乗車券800円。SuicaなどのICカードも使えます",
          "函館山は、日の入りの30〜40分前の便で上へ（12月は15:30ごろ）。雲と強い風の日は見えません",
          "冬の坂と歩道は凍ります。底に溝の深い、滑りにくい靴で",
          "湯の川温泉の日帰り入浴は、タトゥーの決まりが公式に書かれていません（足湯はだれでも）"
        ],
        "dayHead": "2日間の流れ",
        "day": [
          {
            "time": "8:43",
            "area": "1日目 札幌",
            "title": "特急北斗6号で函館へ",
            "text": "函館12:33着。先にホテルに荷物を預けます。（写真：ノボホショコロトソ / CC BY 4.0）",
            "photo": [
              "sapporo",
              0
            ],
            "note": "函館12:33"
          },
          {
            "time": "12:45",
            "area": "1日目 函館駅",
            "title": "朝市でお昼の海鮮丼",
            "text": "市場は14時すぎに閉まります。（写真：bryan... / CC BY-SA 2.0）",
            "photo": [
              "asaichi",
              0
            ]
          },
          {
            "time": "13:55",
            "area": "1日目 元町",
            "title": "赤レンガ倉庫、八幡坂、教会",
            "text": "市電は函館駅前13:43発。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "hachiman",
              0
            ],
            "note": "市電13:43"
          },
          {
            "time": "15:30",
            "area": "1日目 函館山",
            "title": "日の入り前に上がって夜景を待つ",
            "text": "下りたら、明かりのついた倉庫を通って晩ごはんへ。（写真：Perry Li / CC BY-SA 2.0）",
            "photo": [
              "ropeway",
              0
            ],
            "note": "往復1,800円"
          },
          {
            "time": "9:15",
            "area": "2日目 五稜郭",
            "title": "開いたばかりのタワーと公園",
            "text": "市電は函館駅前8:41発。11時に早めのお昼。（写真：くろふね / CC BY 4.0）",
            "photo": [
              "tower",
              0
            ],
            "note": "市電8:41"
          },
          {
            "time": "12:25",
            "area": "2日目 湯の川温泉",
            "title": "足湯、サルの温泉、お風呂",
            "text": "市電は五稜郭公園前12:11発。帰りは15:04発。（写真：OraMAAG / CC BY 4.0）",
            "photo": [
              "yunokawa",
              0
            ],
            "note": "市電12:11"
          },
          {
            "time": "17:55",
            "area": "2日目 函館駅",
            "title": "特急北斗19号で札幌へ",
            "text": "札幌21:41着。（写真：Suikotei / CC BY-SA 4.0）",
            "photo": [
              "kaeri",
              0
            ],
            "note": "札幌21:41"
          }
        ],
        "dealsLead": "特急は往復19,540円（片道9,770円）。函館では、市電と、入ったものの分だけです。",
        "deals": [
          {
            "name": "特急北斗 札幌〜函館",
            "price": "片道9,770円",
            "text": "乗車券6,600円＋指定席3,170円。全車指定席。レールパスも使えます。",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          },
          {
            "name": "市電",
            "price": "1回250〜300円",
            "text": "1日目は2回、2日目は3回。2日目は1日乗車券（800円）を。",
            "url": "https://www.city.hakodate.hokkaido.jp/tram/value-ticket/"
          },
          {
            "name": "函館山ロープウェイ",
            "price": "往復1,800円",
            "text": "カード・電子マネー可。",
            "url": "https://334.co.jp/ropeway/price/"
          },
          {
            "name": "五稜郭タワー",
            "price": "1,200円",
            "text": "9:00〜18:00、休みなし。",
            "url": "https://www.goryokaku-tower.co.jp/price/"
          },
          {
            "name": "箱館奉行所",
            "price": "500円",
            "text": "11〜3月は受付16:45まで。",
            "url": "https://hakodate-bugyosho.jp/information/"
          },
          {
            "name": "湯の川温泉の日帰り入浴",
            "price": "550〜1,200円",
            "text": "足湯は無料。熱帯植物園は300円。",
            "url": "https://hakodate-yunokawa.jp/dayspa/"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: "en",
    docTitle: "Hakodate MAP: one day in Hakodate",
    titleMain: "Hakodate",
    titleSub: "函館で1日",
    howto: "How to use",
    allMaps: "← All maps",
    home: "All maps",
    tabMap: "Map",
    menu: "Menu",
    list: "Spots",
    listHead: "All spots",
    listNote: "Numbers show the order. The timetable follows December–January sunsets; times for Mt. Hakodate in other seasons are inside that spot. The dotted line shows the order, not the actual path.",
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
    checkedDate: "Nov 28, 2026",
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
    pickNote: "The places that fit the timetable are selected to start with, and suggested times assume that set. Hakodate Station is always included.",
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
    courseLate: "Leave 9–10 am\nMarket, fort, night view",
    courseEarly: "Leave about 6:30\nQuiet slopes, onsen",
    courseSapporo: "From Sapporo\n2 days, 1 night",
    swMode: "How to go",
    intro: {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Trams, ropeway and admission",
      "dealsMore": "See official site or route planner",
      "dealsNote": "Per adult. Checked on Nov 28, 2026 with the official sites and a route planner (3 and 5 December timetables).",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose a course",
          "text": "Use the buttons above the list: leave at 9–10 am, leave around 6:30, or two days from Sapporo. The timetable and numbers change."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that could stop you at the door (closing days, cash only, tattoos, winter tips) come first, with times and fees below."
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
        "kicker": "One day in Hakodate (leave 9–10 am)",
        "h1": "Breakfast at the market, a star-shaped fort, then up the mountain before sunset to wait for the lights.",
        "lead": "The night view from Mt. Hakodate is best 20–30 minutes after sunset, while some blue is left in the sky, and this timetable puts you on top at that moment. Leave a hotel near Hakodate Station at 9:30 and eat breakfast at the morning market. Take the tram to Goryokaku for the tower and the park, have lunch, then walk the slopes and churches of Motomachi. Ride the ropeway up 30 minutes before sunset; afterwards, the floodlit red-brick warehouses and dinner.",
        "favName": "The night view from Mt. Hakodate",
        "favText": "Best 20–30 minutes after sunset, while some blue is left in the sky. (Photo: Perry Li / CC BY-SA 2.0)",
        "favPhoto": [
          "ropeway",
          0
        ],
        "who": [
          "Trams cost ¥250–300 a ride; a day pass is ¥800. Suica and other IC cards work",
          "For Mt. Hakodate, ride up 30–40 minutes before sunset (about 15:30 in December). Cloud or strong wind means no view",
          "Slopes and pavements freeze in winter: wear shoes with deep tread",
          "The morning market closes soon after 14:00",
          "No photos inside the Orthodox church; no visits inside from 25 December to the end of February",
          "Day baths at Yunokawa Onsen do not state a tattoo rule on their sites (the foot bath is open to all)"
        ],
        "dayHead": "The day",
        "day": [
          {
            "time": "9:30",
            "area": "Hakodate Station",
            "title": "Breakfast at the market by the station",
            "text": "Look at the menus outside the Donburi Yokocho restaurants and choose. (Photo: bryan... / CC BY-SA 2.0)",
            "photo": [
              "asaichi",
              0
            ]
          },
          {
            "time": "11:10",
            "area": "Goryokaku",
            "title": "See the star from the tower, then the park",
            "text": "Tram from Hakodate-ekimae at 10:32. Shoes off in the Magistrate’s Office. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "tower",
              0
            ],
            "note": "Tram 10:32"
          },
          {
            "time": "13:00",
            "area": "Goryokaku",
            "title": "Lunch: salt ramen or a local burger",
            "text": "Two places right by the tower. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "hiru",
              0
            ]
          },
          {
            "time": "14:35",
            "area": "Motomachi",
            "title": "Hachiman-zaka and the churches",
            "text": "Tram from Goryokaku-Koen-mae at 13:58. Look down the slope to the harbour. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "hachiman",
              0
            ],
            "note": "Tram 13:58"
          },
          {
            "time": "15:30",
            "area": "Mt. Hakodate",
            "title": "Ride up and wait for dark",
            "text": "Sunset in December is about 16:07. Join the queue down around 17:00. (Photo: Perry Li / CC BY-SA 2.0)",
            "photo": [
              "ropeway",
              0
            ],
            "note": "Return ¥1,800"
          },
          {
            "time": "17:30",
            "area": "Bay area",
            "title": "The warehouses at night, and dinner",
            "text": "In December the tree is relit with fireworks at 18:00. (Photo: 掬茶 / CC BY-SA 4.0)",
            "photo": [
              "kanemori",
              0
            ]
          }
        ],
        "dealsLead": "You ride the tram three times, so the day pass (¥800) is simplest. Everything else you pay as you go.",
        "deals": [
          {
            "name": "Tram day pass",
            "price": "¥800",
            "text": "On the tram or at the station’s tourist information centre. Single rides are ¥250–300.",
            "url": "https://www.city.hakodate.hokkaido.jp/tram/value-ticket/"
          },
          {
            "name": "Mt. Hakodate Ropeway",
            "price": "Return ¥1,800",
            "text": "Cards and e-money accepted. Every 15 minutes.",
            "url": "https://334.co.jp/ropeway/price/"
          },
          {
            "name": "Goryokaku Tower",
            "price": "¥1,200",
            "text": "9:00–18:00, every day.",
            "url": "https://www.goryokaku-tower.co.jp/price/"
          },
          {
            "name": "Hakodate Magistrate’s Office",
            "price": "¥500",
            "text": "Last entry 16:45 from November to March. The park is free.",
            "url": "https://hakodate-bugyosho.jp/information/"
          },
          {
            "name": "Old Public Hall (optional)",
            "price": "¥300",
            "text": "Until 17:00 from November to March.",
            "url": "https://hakodate-kokaido.jp/"
          },
          {
            "name": "Orthodox Church",
            "price": "Donation ¥200",
            "text": "Sundays from 13:00. No visits 25 Dec–end of Feb.",
            "url": "https://www.orthodox-hakodate.jp/services"
          },
          {
            "name": "Day bath at Yunokawa Onsen (optional)",
            "price": "¥550–1,200",
            "text": "The foot bath is free (9:00–21:00).",
            "url": "https://hakodate-yunokawa.jp/dayspa/"
          }
        ]
      },
      "early": {
        "kicker": "One day in Hakodate (leave about 6:30)",
        "h1": "The market before the tour groups, Hachiman-zaka with nobody on it, and a hot spring to end the day.",
        "lead": "Hachiman-zaka is full of people and cars by day; at 8 am it is quiet. Leave your hotel at 6:30 for breakfast at a quiet market. Walk along the water to Hachiman-zaka and Motomachi at 8:00, see the Public Hall and the churches as they open, and rest at the warehouses. Goryokaku at midday, the night view from Mt. Hakodate at dusk, then the tram to Yunokawa Onsen before dinner.",
        "favName": "Hachiman-zaka at 8 am",
        "favText": "The slope is full of people and cars by day. At this hour it is quiet. (Photo: くろふね / CC BY 4.0)",
        "favPhoto": [
          "hachiman",
          0
        ],
        "who": [
          "Trams cost ¥250–300 a ride; a day pass is ¥800. Suica and other IC cards work",
          "For Mt. Hakodate, ride up 30–40 minutes before sunset (about 15:30 in December). Cloud or strong wind means no view",
          "Slopes and pavements freeze in winter: wear shoes with deep tread",
          "Sunrise is about 7:00 in December and January, so it is still dark when you reach the market",
          "The Orthodox church opens at 10:00 (13:00 on Sundays; no visits inside 25 Dec–end of Feb)",
          "Day baths at Yunokawa Onsen do not state a tattoo rule on their sites (the foot bath is open to all)"
        ],
        "dayHead": "The day",
        "day": [
          {
            "time": "6:35",
            "area": "Hakodate Station",
            "title": "Breakfast at a quiet market",
            "text": "Open from 6:00 January–April, from 5:00 May–December. (Photo: bryan... / CC BY-SA 2.0)",
            "photo": [
              "asaichi",
              0
            ]
          },
          {
            "time": "8:00",
            "area": "Motomachi",
            "title": "Hachiman-zaka and Daisan-zaka with no one about",
            "text": "A 30-minute walk along the water from the market. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "hachiman",
              0
            ]
          },
          {
            "time": "9:00",
            "area": "Motomachi",
            "title": "The Public Hall as it opens; the church at 10",
            "text": "The balcony looks over the harbour. (Photo: 掬茶 / CC BY-SA 4.0)",
            "photo": [
              "kokaido",
              0
            ],
            "note": "¥300"
          },
          {
            "time": "10:30",
            "area": "Bay area",
            "title": "A break at the warehouses",
            "text": "Shops open at 9:30. (Photo: 掬茶 / CC BY-SA 4.0)",
            "photo": [
              "kanemori",
              0
            ]
          },
          {
            "time": "12:05",
            "area": "Goryokaku",
            "title": "Lunch, the tower, the park",
            "text": "Tram from Jujigai at 11:22. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "tower",
              0
            ],
            "note": "Tram 11:22"
          },
          {
            "time": "15:30",
            "area": "Mt. Hakodate",
            "title": "Up before sunset to wait for the lights",
            "text": "Tram from Goryokaku-Koen-mae at 14:46. (Photo: Perry Li / CC BY-SA 2.0)",
            "photo": [
              "ropeway",
              0
            ],
            "note": "Tram 14:46"
          },
          {
            "time": "18:15",
            "area": "Yunokawa Onsen",
            "title": "Foot bath or a soak, then back for dinner",
            "text": "Tram from Jujigai at 17:39; back at 19:37. (Photo: OraMAAG / CC BY 4.0)",
            "photo": [
              "yunokawa",
              0
            ],
            "note": "Tram 17:39"
          }
        ],
        "dealsLead": "You ride the tram four times: buy the day pass (¥800).",
        "deals": [
          {
            "name": "Tram day pass",
            "price": "¥800",
            "text": "On the tram or at the station’s tourist information centre. Single rides are ¥250–300.",
            "url": "https://www.city.hakodate.hokkaido.jp/tram/value-ticket/"
          },
          {
            "name": "Old Public Hall",
            "price": "¥300",
            "text": "From 9:00. Until 17:00 from November to March.",
            "url": "https://hakodate-kokaido.jp/"
          },
          {
            "name": "Orthodox Church",
            "price": "Donation ¥200",
            "text": "From 10:00 (Sundays 13:00). No visits 25 Dec–end of Feb.",
            "url": "https://www.orthodox-hakodate.jp/services"
          },
          {
            "name": "Goryokaku Tower",
            "price": "¥1,200",
            "text": "9:00–18:00, every day.",
            "url": "https://www.goryokaku-tower.co.jp/price/"
          },
          {
            "name": "Hakodate Magistrate’s Office",
            "price": "¥500",
            "text": "Last entry 16:45 from November to March.",
            "url": "https://hakodate-bugyosho.jp/information/"
          },
          {
            "name": "Mt. Hakodate Ropeway",
            "price": "Return ¥1,800",
            "text": "Cards and e-money accepted.",
            "url": "https://334.co.jp/ropeway/price/"
          },
          {
            "name": "Day bath at Yunokawa Onsen",
            "price": "¥550–1,200",
            "text": "The foot bath is free (9:00–21:00).",
            "url": "https://hakodate-yunokawa.jp/dayspa/"
          }
        ]
      },
      "sapporo": {
        "kicker": "Two days from Sapporo",
        "h1": "The night view from Mt. Hakodate on the evening you arrive; Goryokaku and a hot spring the next day.",
        "lead": "Hakodate is three hours fifty from Sapporo by express. Stay one night and you get the night view on the evening you arrive, and Goryokaku as it opens and Yunokawa Onsen the next day. Take the 8:43 Hokuto limited express from Sapporo (Hakodate 12:33). Lunch at the morning market, then the warehouses, Hachiman-zaka and the churches, and Mt. Hakodate at dusk. On day 2, Goryokaku Tower as it opens, the park and Yunokawa Onsen, then the 17:55 back, reaching Sapporo at 21:41.",
        "favName": "The night view from Mt. Hakodate",
        "favText": "If cloud hides it on day 1, you can go up again on day 2 (and take the last train at 18:43). (Photo: Perry Li / CC BY-SA 2.0)",
        "favPhoto": [
          "ropeway",
          0
        ],
        "who": [
          "Every seat on the Hokuto is reserved. ¥9,770 one way. Book both directions first",
          "With the JR Hokkaido Rail Pass (all lines) reserved seats cost nothing extra",
          "The last train back leaves Hakodate at 18:43 (Sapporo 22:41)",
          "Trams cost ¥250–300 a ride; a day pass is ¥800. Suica and other IC cards work",
          "For Mt. Hakodate, ride up 30–40 minutes before sunset (about 15:30 in December). Cloud or strong wind means no view",
          "Slopes and pavements freeze in winter: wear shoes with deep tread",
          "Day baths at Yunokawa Onsen do not state a tattoo rule on their sites (the foot bath is open to all)"
        ],
        "dayHead": "The two days",
        "day": [
          {
            "time": "8:43",
            "area": "Day 1 · Sapporo",
            "title": "Hokuto 6 to Hakodate",
            "text": "Arrives 12:33. Drop your bags at the hotel first. (Photo: ノボホショコロトソ / CC BY 4.0)",
            "photo": [
              "sapporo",
              0
            ],
            "note": "Hakodate 12:33"
          },
          {
            "time": "12:45",
            "area": "Day 1 · Hakodate Station",
            "title": "A seafood bowl for lunch at the market",
            "text": "The market closes soon after 14:00. (Photo: bryan... / CC BY-SA 2.0)",
            "photo": [
              "asaichi",
              0
            ]
          },
          {
            "time": "13:55",
            "area": "Day 1 · Motomachi",
            "title": "Warehouses, Hachiman-zaka, churches",
            "text": "Tram from Hakodate-ekimae at 13:43. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "hachiman",
              0
            ],
            "note": "Tram 13:43"
          },
          {
            "time": "15:30",
            "area": "Day 1 · Mt. Hakodate",
            "title": "Up before sunset to wait for the lights",
            "text": "Afterwards, walk through the floodlit warehouses to dinner. (Photo: Perry Li / CC BY-SA 2.0)",
            "photo": [
              "ropeway",
              0
            ],
            "note": "Return ¥1,800"
          },
          {
            "time": "9:15",
            "area": "Day 2 · Goryokaku",
            "title": "The tower as it opens, and the park",
            "text": "Tram from Hakodate-ekimae at 8:41. An early lunch at 11:00. (Photo: くろふね / CC BY 4.0)",
            "photo": [
              "tower",
              0
            ],
            "note": "Tram 8:41"
          },
          {
            "time": "12:25",
            "area": "Day 2 · Yunokawa Onsen",
            "title": "Foot bath, bathing monkeys, a soak",
            "text": "Tram from Goryokaku-Koen-mae at 12:11; back at 15:04. (Photo: OraMAAG / CC BY 4.0)",
            "photo": [
              "yunokawa",
              0
            ],
            "note": "Tram 12:11"
          },
          {
            "time": "17:55",
            "area": "Day 2 · Hakodate Station",
            "title": "Hokuto 19 back to Sapporo",
            "text": "Arrives Sapporo 21:41. (Photo: Suikotei / CC BY-SA 4.0)",
            "photo": [
              "kaeri",
              0
            ],
            "note": "Sapporo 21:41"
          }
        ],
        "dealsLead": "The express is ¥19,540 return (¥9,770 each way). In Hakodate you pay for trams and whatever you enter.",
        "deals": [
          {
            "name": "Hokuto limited express, Sapporo–Hakodate",
            "price": "¥9,770 one way",
            "text": "Fare ¥6,600 + reserved seat ¥3,170. All seats reserved. Rail passes are valid.",
            "url": "https://www.jrhokkaido.co.jp/global/english/ticket/railpass/index.html"
          },
          {
            "name": "Tram",
            "price": "¥250–300 a ride",
            "text": "Two rides on day 1, three on day 2: buy the day pass (¥800) on day 2.",
            "url": "https://www.city.hakodate.hokkaido.jp/tram/value-ticket/"
          },
          {
            "name": "Mt. Hakodate Ropeway",
            "price": "Return ¥1,800",
            "text": "Cards and e-money accepted.",
            "url": "https://334.co.jp/ropeway/price/"
          },
          {
            "name": "Goryokaku Tower",
            "price": "¥1,200",
            "text": "9:00–18:00, every day.",
            "url": "https://www.goryokaku-tower.co.jp/price/"
          },
          {
            "name": "Hakodate Magistrate’s Office",
            "price": "¥500",
            "text": "Last entry 16:45 from November to March.",
            "url": "https://hakodate-bugyosho.jp/information/"
          },
          {
            "name": "Day bath at Yunokawa Onsen",
            "price": "¥550–1,200",
            "text": "The foot bath is free. The tropical garden is ¥300.",
            "url": "https://hakodate-yunokawa.jp/dayspa/"
          }
        ]
      }
    }
  }
};
