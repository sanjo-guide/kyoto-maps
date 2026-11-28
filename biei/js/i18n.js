/* Page texts in Japanese and English.
   Toshi 個人のマップ。美瑛・青い池と富良野（旭川から日帰り）。写真はすべて Wikimedia Commons（だれかが行った・食べたとは書かない）。
   コースは3つ（一覧の上のボタン）：late＝雪のない季節（data/routes/biei.json）、early＝冬・11月〜4月中旬（biei-winter.json）、
   furano＝花畑・5〜10月（biei-furano.json）。最初にどれで開くかは日付で決まる（scripts/sync_biei.py の WINTER_FROM / WINTER_TO）。
   intro はどのコースにも共通の項目で、コースで変わる項目は introFor[コース] が app.js で上書きされる。
   写真は [スポットの id, 写真の番号]（冬のコースは雪・夜の写真が0番になるように並べ替えてある）。
   時刻・料金は2026年11月28日に確認（出典は data/routes/biei.json の sources）。直すときはこのファイルを直接直してよい */
window.BIEI_I18N = {
  "ja": {
    "htmlLang": "ja",
    "docTitle": "美瑛・青い池と富良野 旭川から日帰り Biei MAP",
    "titleMain": "美瑛・青い池",
    "titleSub": "Biei, a day trip from Asahikawa",
    "howto": "使い方",
    "allMaps": "← マップ一覧",
    "home": "マップ一覧",
    "tabMap": "地図",
    "menu": "メニュー",
    "list": "一覧",
    "listHead": "スポット一覧",
    "listNote": "番号は回る順番です。電車とバスの時刻は平日も土日も同じです（2026年12月のダイヤ）。点線は順番を示す線で、実際の道ではありません。",
    "back": "一覧",
    "close": "閉じる",
    "showAll": "全体を表示",
    "seeDetails": "詳しく見る",
    "prevPhoto": "前の写真",
    "nextPhoto": "次の写真",
    "suggested": "おすすめの時間：",
    "suggestedLabel": "めやすの時間",
    "gmapsOne": "Googleマップで開く",
    "gmapsMany": "Googleマップ：",
    "copy": "このスポットのリンクをコピー",
    "copied": "コピーしました",
    "spot1Howto": "このマップの使い方を見る",
    "credit": "文章：Toshi／写真：Wikimedia Commons（撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    "photoBy": "写真：",
    "loadError": "地図データを読み込めませんでした。再読み込みしてください。",
    "hours": "時間",
    "fee": "料金",
    "train": "電車",
    "bus": "バス",
    "closed": "休み",
    "cash": "現金を用意してください",
    "checked": "{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。",
    "unchecked": "{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。",
    "checkedDate": "2026年11月28日",
    "noticeHead": "お知らせ",
    "more": "詳しく",
    "linkKinds": {
      "official": "公式サイト",
      "timetable": "時刻表",
      "info": "案内"
    },
    "nextRoute": "次のスポットへの行き方",
    "locate": "現在地",
    "locating": "現在地を探しています…",
    "locateErr": "現在地を取得できませんでした。端末の位置情報の設定を確認してください。",
    "visitOff": "行ったら印を付ける",
    "visitOn": "行った！",
    "progress": "{n} / {t} か所 行った",
    "reset": "リセット",
    "resetAsk": "もう一度押すと、行った印をすべて消します",
    "modeAria": "回り方",
    "modeAll": "全部回る",
    "modePick": "選んで回る",
    "pickNote": "最初は、時間割どおりに回れる場所が選ばれています。おすすめの時間は、その組み合わせのときの目安です。旭川駅・乗り換えの駅・帰りの電車は、どの組み合わせでも入ります。",
    "pickCount": "選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）",
    "pickEmpty": "まだ選んでいません。下の一覧から、行きたい場所を選んでください。",
    "pickAll": "すべて選ぶ",
    "pickNone": "すべて外す",
    "pickOff": "行きたい",
    "pickOn": "行く",
    "autoTag": "全員共通",
    "autoOff": "今回は通りません",
    "seasonHead": "季節営業の可能性",
    "hintHead": "あなたのルートでは",
    "swCourse": "季節とコース",
    "courseAria": "季節とコース",
    "courseLate": "雪のない季節\n丘・青い池・温泉",
    "courseEarly": "冬 11〜4月中旬\n青い池のライトアップ",
    "courseFurano": "花畑 5〜10月\nファーム富田も",
    "swMode": "回り方",
    "intro": {
      "favLabel": "いちばんの見どころ",
      "whoHead": "先に知っておくこと",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "電車・バス・入場料",
      "dealsMore": "公式サイト・乗換案内で見る",
      "dealsNote": "大人1人の金額です。2026年11月28日に、各施設・バス会社の公式サイトと乗換案内（12月3日・5日のダイヤ）で確認しました。",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "季節とコースを選ぶ",
          "text": "一覧の上のボタンで「冬」「雪のない季節」「花畑」を選べます。最初は、その日の日付に合う方で開きます。時間割と番号が変わります。"
        },
        {
          "title": "行きたい場所を入れ替える",
          "text": "最初は、時間割どおりに回れる場所だけが選んであります。「行きたい」「行く」を押すと入れ替えられ、そのときの回り方のヒントが出ます。"
        },
        {
          "title": "いちばん上のお知らせを読む",
          "text": "番号をタップすると、最終バス・予約・タトゥー・寒さなど、現地で困ることが先に出ます。時刻と料金は、その下にあります。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが作った、オリジナルマップです（公式サイトなどの情報と、Wikimedia Commons の写真で紹介しています）。"
    },
    "introFor": {
      "late": {
        "kicker": "旭川から日帰り（雪のない季節：4月下旬〜10月）",
        "h1": "午前は自転車で丘、午後はバスで青い池と滝。温泉に入って帰る。",
        "lead": "車がなくても回れる美瑛の1日です。旭川9:38の電車で美瑛へ。駅前で電動自転車を借りて、パッチワークの路の丘と木を回ります。石の倉庫の道の駅でお昼を食べ、13:45のバスで白金青い池へ。同じ青い色の川に落ちる白ひげの滝を見て、白金温泉に入り、美瑛の町で晩ごはん。18:40の電車で旭川19:13着です。",
        "favName": "白金 青い池",
        "favText": "立ち枯れのカラマツと青い水。（写真：MaedaAkihiko / CC BY-SA 4.0）",
        "favPhoto": [
          "pond",
          0
        ],
        "who": [
          "車なしで回れます：JR富良野線、道北バス、丘は電動自転車（駅前で借りる。料金と営業期間は店で確認）",
          "白金へのバスは1日に数本。美瑛へ戻る最終は白金温泉18:02発",
          "青い池は、晴れた日の13〜15時がいちばん混みます",
          "丘の木はどれも農家の畑の中。道から畑へ入らない",
          "温泉のタトゥーの決まりは、どの宿の公式サイトにも書かれていません（行く前に電話で確認）",
          "富良野線でICカードが使えるかは未確認。券売機できっぷを買うのが確実",
          "時刻は2026年12月のダイヤ。2027年春のダイヤ改正のあとは乗換案内で確かめてください"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "9:38",
            "area": "旭川",
            "title": "富良野線で美瑛へ",
            "text": "美瑛10:12着。駅前で電動自転車を借ります。（写真：LR0725 / CC BY-SA 4.0）",
            "photo": [
              "eki",
              0
            ],
            "note": "美瑛10:12"
          },
          {
            "time": "10:45",
            "area": "パッチワークの路",
            "title": "北西の丘とケンとメリーの木",
            "text": "展望台から丘と山並み。（写真：Choi2451 / CC0）",
            "photo": [
              "hokusei",
              0
            ]
          },
          {
            "time": "11:45",
            "area": "パッチワークの路",
            "title": "セブンスターの木",
            "text": "区画ごとに色の違う畑。（写真：Babiesan / CC BY-SA 3.0）",
            "photo": [
              "seven",
              0
            ]
          },
          {
            "time": "12:40",
            "area": "美瑛駅前",
            "title": "石の倉庫の道の駅でお昼",
            "text": "食堂は14:30ラストオーダー。（写真：Route275 / CC BY-SA 3.0）",
            "photo": [
              "machi",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "白金",
            "title": "青い池",
            "text": "13:45のバスで。15:07のバスで先へ。（写真：MaedaAkihiko / CC BY-SA 4.0）",
            "photo": [
              "pond",
              1
            ]
          },
          {
            "time": "15:15",
            "area": "白金温泉",
            "title": "白ひげの滝と温泉",
            "text": "橋の上から滝と青い川。（写真：RJD / CC BY 3.0）",
            "photo": [
              "falls",
              0
            ]
          },
          {
            "time": "17:15",
            "area": "美瑛駅前",
            "title": "晩ごはん、18:40の電車で旭川へ",
            "text": "まっすぐ帰るなら17:39発。（写真：欅 / CC BY-SA 3.0）",
            "photo": [
              "kaeri",
              0
            ],
            "note": "旭川19:13"
          }
        ],
        "dealsLead": "電車は旭川〜美瑛が片道680円。バスは美瑛駅前から青い池まで800円、白金温泉から美瑛駅前まで900円。丘・青い池・滝は見るだけなら無料です。",
        "deals": [
          {
            "name": "JR 旭川→美瑛",
            "price": "680円",
            "text": "富良野線で34分、1時間に1本ほど。JR北海道レールパスで乗れます。ICカードが使えるかは未確認なので、きっぷを。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "道北バス 美瑛駅前→青い池／白金温泉",
            "price": "800円／900円",
            "text": "青い池入口〜白金温泉は220円。降りるときに払います。1日フリーパスもあります（値段は販売ページで）。",
            "url": "https://www.dohokubus.com/files/houmen/kaguraoka_biei_heijitu.pdf"
          },
          {
            "name": "白金温泉 日帰り入浴",
            "price": "1,200円〜1,530円",
            "text": "森の雫 RIN・碧の美 ゆゆ 1,200円、ホテルパークヒルズ 1,530円。タオルは別。タトゥーは行く前に電話で確認を。",
            "url": "https://www.biei-hokkaido.jp/ja/hot-spring"
          },
          {
            "name": "電動自転車（駅前の貸自転車）",
            "price": "店で確認",
            "text": "観光協会の「美瑛のめぐり方」に店の一覧。電動で1kmあたり4〜5分が目安。",
            "url": "https://www.biei-hokkaido.jp/ja/cruise"
          }
        ]
      },
      "early": {
        "kicker": "旭川から日帰り（冬：11月〜4月中旬）",
        "h1": "雪の丘の1本の木、青い川に落ちる滝、温泉。日が沈んだら、青い池のライトアップ。",
        "lead": "冬の美瑛を、車なしで回る1日です。旭川9:38の電車で美瑛へ。予約しておいた小さなバスでクリスマスツリーの木を見て、町でお昼。13:45のバスで白金へ行き、青い川と白ひげの滝を明るいうちに見て、温泉で温まります。日が沈んだら16:32のバスで青い池へ。雪の池と枯れ木が光に浮かぶのを見て、18:05の最終バスで美瑛に戻り、18:40の電車で旭川19:13着です。金・土曜は、予約制のライトアップのバスを使う回り方も紹介しています。",
        "favName": "青い池のライトアップ",
        "favText": "2027年4月21日まで毎晩。12月は16:30に点灯します。（写真：Calistemon / CC BY-SA 4.0）",
        "favPhoto": [
          "pond",
          0
        ],
        "who": [
          "12〜3月は最低気温が−15℃を下回ります。青い池では日が沈んでから1時間以上、外にいます（暖まれる建物は開いていません）",
          "美瑛へ戻る最終バスは青い池入口18:05発。乗り遅れるとタクシーだけです",
          "クリスマスツリーライナーは予約制（2日前まで、12月1日〜2月28日）",
          "金・土曜は、観光協会の「美遊バス ライトアップコース」（予約制、4,000円から）で回るほうが楽です",
          "冬は青い池の水面が雪の下です。青い水が見られるのは、白ひげの滝の下の川",
          "12月は16時ごろに日が沈みます。3月・4月は点灯が18時以降で、最終バスでは見られません",
          "温泉のタトゥーの決まりは、どの宿の公式サイトにも書かれていません（行く前に電話で確認）",
          "年末年始はバスが特別ダイヤ、道の駅は休みです"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "9:38",
            "area": "旭川",
            "title": "富良野線で美瑛へ",
            "text": "美瑛10:12着。10:35までにバスの受付を。（写真：Olegushka / CC BY-SA 4.0）",
            "photo": [
              "eki",
              0
            ],
            "note": "美瑛10:12"
          },
          {
            "time": "10:45",
            "area": "美瑛の丘",
            "title": "クリスマスツリーの木",
            "text": "予約制のライナーで往復1時間。（写真：oyakata / CC BY 3.0）",
            "photo": [
              "xmas",
              0
            ]
          },
          {
            "time": "11:50",
            "area": "美瑛駅前",
            "title": "石の倉庫の道の駅でお昼",
            "text": "13:45のバスまで町で過ごします。（写真：Route275 / CC BY-SA 3.0）",
            "photo": [
              "machi",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "白金温泉",
            "title": "白ひげの滝",
            "text": "明るいうちに、青い川と滝を。（写真：663highland / CC BY 2.5）",
            "photo": [
              "falls",
              0
            ]
          },
          {
            "time": "14:45",
            "area": "白金温泉",
            "title": "温泉で温まる",
            "text": "16:15に出て、厚着をし直します。（写真：Kenneth Lee Sutherla… / CC BY 3.0）",
            "photo": [
              "onsen",
              0
            ]
          },
          {
            "time": "16:40",
            "area": "白金",
            "title": "青い池のライトアップ",
            "text": "16:32のバスで。帰りは18:05の最終バス。（写真：Tomoki Nagahira / CC BY 3.0）",
            "photo": [
              "pond",
              1
            ]
          },
          {
            "time": "18:40",
            "area": "美瑛",
            "title": "電車で旭川へ",
            "text": "乗り遅れたら19:54発。最終は21:19発。（写真：欅 / CC BY-SA 3.0）",
            "photo": [
              "kaeri",
              0
            ],
            "note": "旭川19:13"
          }
        ],
        "dealsLead": "電車は旭川〜美瑛が片道680円。バスは美瑛駅前から白金温泉まで900円、白金温泉から青い池まで220円、青い池から美瑛駅前まで800円。ライトアップは見るだけなら無料です。",
        "deals": [
          {
            "name": "JR 旭川→美瑛",
            "price": "680円",
            "text": "富良野線で34分、1時間に1本ほど。JR北海道レールパスで乗れます。ICカードが使えるかは未確認なので、きっぷを。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "道北バス 美瑛駅前→青い池／白金温泉",
            "price": "800円／900円",
            "text": "青い池入口〜白金温泉は220円。降りるときに払います。1日フリーパスもあります（値段は販売ページで）。",
            "url": "https://www.dohokubus.com/files/houmen/kaguraoka_biei_heijitu.pdf"
          },
          {
            "name": "クリスマスツリーライナー",
            "price": "2,000円から",
            "text": "12月1日〜2月28日（12月31日〜1月5日運休）。10:45・13:20・14:50発、約1時間。予約は2日前まで。",
            "url": "https://www.biei-hokkaido.jp/ja/202627ws"
          },
          {
            "name": "美遊バス ライトアップコース（金・土）",
            "price": "4,000円から",
            "text": "2027年2月13日まで。美瑛16:35発、18:30着（2月は19:00）。ビルケの森と青い池。予約は2日前まで。",
            "url": "https://www.biei-hokkaido.jp/ja/202627ws"
          },
          {
            "name": "白金温泉 日帰り入浴",
            "price": "1,200円〜1,530円",
            "text": "森の雫 RIN・碧の美 ゆゆ 1,200円、ホテルパークヒルズ 1,530円。タオルは別。タトゥーは行く前に電話で確認を。",
            "url": "https://www.biei-hokkaido.jp/ja/hot-spring"
          }
        ]
      },
      "furano": {
        "kicker": "旭川から日帰り（花の季節：5月〜10月はじめ）",
        "h1": "富良野線で花畑を2つ。中富良野のファーム富田と、美馬牛の四季彩の丘。",
        "lead": "電車と歩きで花畑を回る1日です。旭川9:38の電車で中富良野10:46着、歩いて25分のファーム富田で花畑を見て、園内でお昼。13:27の電車で美馬牛（びばうし）へ戻り、歩いて30分の四季彩の丘へ。16:18の電車で美瑛に出て、石の倉庫の道の駅と町を歩き、晩ごはんのあと18:40の電車で旭川19:13着です。このコースに青い池は入っていません。",
        "favName": "ファーム富田の花畑",
        "favText": "斜面に並ぶ花の帯。（写真：663highland / CC BY 2.5）",
        "favPhoto": [
          "tomita",
          0
        ],
        "who": [
          "駅から花畑まで、片道25〜30分の歩きが2回あります。帽子と飲み物を",
          "電車は1時間に1本ほど。中富良野13:27発を逃すと、次は15:55発です",
          "ラベンダーの見ごろは年によって違います。行く前にファーム富田の公式サイトで花の様子を",
          "四季彩の丘は7〜9月だけ入場料800円（窓口は現金のみ）。ファーム富田の入園料は要確認",
          "夏の観光列車ノロッコ号と臨時のラベンダー畑駅は、2027年の運転日が未発表です",
          "時刻は2026年12月のダイヤ。2027年春のダイヤ改正のあとは乗換案内で確かめてください"
        ],
        "dayHead": "1日の流れ",
        "day": [
          {
            "time": "9:38",
            "area": "旭川",
            "title": "富良野線で中富良野へ",
            "text": "美瑛を通って10:46着。（写真：Nesnad / CC BY 4.0）",
            "photo": [
              "asahikawa",
              0
            ],
            "note": "中富良野10:46"
          },
          {
            "time": "11:15",
            "area": "中富良野",
            "title": "ファーム富田とお昼",
            "text": "12:55には駅へ歩き始めます。（写真：Maga-chan / CC BY-SA 2.1 jp）",
            "photo": [
              "tomita",
              1
            ]
          },
          {
            "time": "13:45",
            "area": "美馬牛",
            "title": "赤い屋根の駅から歩く",
            "text": "四季彩の丘まで30分。（写真：Alberth2 / CC BY 3.0）",
            "photo": [
              "bibaushi",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "美馬牛",
            "title": "四季彩の丘",
            "text": "花の帯と十勝岳の山並み。（写真：lumoplank / CC0）",
            "photo": [
              "shikisai",
              0
            ]
          },
          {
            "time": "16:30",
            "area": "美瑛駅前",
            "title": "石の倉庫の道の駅と町",
            "text": "美馬牛16:18発で美瑛16:25着。（写真：Route275 / CC BY-SA 3.0）",
            "photo": [
              "machi",
              0
            ]
          },
          {
            "time": "18:40",
            "area": "美瑛",
            "title": "晩ごはんのあと、電車で旭川へ",
            "text": "まっすぐ帰るなら17:39発。（写真：欅 / CC BY-SA 3.0）",
            "photo": [
              "kaeri",
              0
            ],
            "note": "旭川19:13"
          }
        ],
        "dealsLead": "電車は旭川→中富良野1,380円、中富良野→美馬牛470円、美馬牛→美瑛320円、美瑛→旭川680円。四季彩の丘は7〜9月だけ800円です。",
        "deals": [
          {
            "name": "JR 旭川→中富良野",
            "price": "1,380円",
            "text": "富良野線で1時間8分。JR北海道レールパスで乗れます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "JR 中富良野→美馬牛→美瑛→旭川",
            "price": "470円＋320円＋680円",
            "text": "乗るたびにきっぷを買います。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "四季彩の丘",
            "price": "800円（7〜9月）",
            "text": "ほかの月は入場料の案内なし。園内の乗りものとアルパカ牧場は別料金。",
            "url": "http://www.shikisainooka.jp/about/guide/"
          },
          {
            "name": "ファーム富田",
            "price": "要確認",
            "text": "入園料は公式サイトで確かめられませんでした。営業時間の外は入れません。",
            "url": "https://www.farm-tomita.co.jp/"
          }
        ]
      }
    }
  },
  "en": {
    "htmlLang": "en",
    "docTitle": "Biei MAP: the Blue Pond and Furano, a day trip from Asahikawa",
    "titleMain": "Biei & the Blue Pond",
    "titleSub": "美瑛・青い池 旭川から日帰り",
    "howto": "How to use",
    "allMaps": "← All maps",
    "home": "All maps",
    "tabMap": "Map",
    "menu": "Menu",
    "list": "Spots",
    "listHead": "All spots",
    "listNote": "Numbers show the order. Train and bus times are the same on weekdays and weekends (December 2026 timetable). The dotted line shows the order, not the actual path.",
    "back": "List",
    "close": "Close",
    "showAll": "Show all",
    "seeDetails": "See details",
    "prevPhoto": "Previous photo",
    "nextPhoto": "Next photo",
    "suggested": "Suggested time: ",
    "suggestedLabel": "Rough time",
    "gmapsOne": "Open in Google Maps",
    "gmapsMany": "Google Maps: ",
    "copy": "Copy link to this spot",
    "copied": "Link copied",
    "spot1Howto": "How to use this map",
    "credit": "Text: Toshi / Photos: Wikimedia Commons (the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    "photoBy": "Photo: ",
    "loadError": "Could not load the map data. Please reload.",
    "hours": "Hours",
    "fee": "Fee",
    "train": "Train",
    "bus": "Bus",
    "closed": "Closed",
    "cash": "Bring cash",
    "checked": "Checked on official websites and a route planner on {d}. Details can change, so please check before you go.",
    "unchecked": "Could not be confirmed on an official website as of {d}. Please check the latest information before you go.",
    "checkedDate": "Nov 28, 2026",
    "noticeHead": "Note",
    "more": "Details",
    "linkKinds": {
      "official": "Official site",
      "timetable": "Timetable",
      "info": "Info"
    },
    "nextRoute": "Directions to the next stop",
    "locate": "My location",
    "locating": "Finding your location…",
    "locateErr": "Could not get your location. Please check your location settings.",
    "visitOff": "Mark as visited",
    "visitOn": "Visited!",
    "progress": "{n} of {t} visited",
    "reset": "Reset",
    "resetAsk": "Tap again to clear all visited marks",
    "modeAria": "How to go",
    "modeAll": "Full route",
    "modePick": "Choose stops",
    "pickNote": "The places that fit the timetable are selected to start with, and suggested times assume that set. Asahikawa Station, the station where you change and the train back are always included.",
    "pickCount": "{n} places chosen · {t} stops in your route (incl. the shared ones)",
    "pickEmpty": "Nothing chosen yet. Pick the places you want from the list below.",
    "pickAll": "Choose all",
    "pickNone": "Clear all",
    "pickOff": "Want to go",
    "pickOn": "Going",
    "autoTag": "Everyone",
    "autoOff": "Not on your route",
    "seasonHead": "Possibly seasonal",
    "hintHead": "On your route",
    "swCourse": "Season and course",
    "courseAria": "Season and course",
    "courseLate": "No snow\nHills, pond, onsen",
    "courseEarly": "Winter Nov–mid-Apr\nBlue Pond light-up",
    "courseFurano": "Flowers May–Oct\nwith Farm Tomita",
    "swMode": "How to go",
    "intro": {
      "favLabel": "Highlight",
      "whoHead": "Know before you go",
      "from": "",
      "timeSuffix": "",
      "dealsHead": "Trains, buses and admission",
      "dealsMore": "See official site or route planner",
      "dealsNote": "Per adult. Checked on Nov 28, 2026 with the official sites of each place and bus company and a route planner (3 and 5 December timetables).",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Choose the season and course",
          "text": "Use the buttons above the list: winter, snow-free season, or flower fields. The map opens on the one that fits today’s date. The timetable and numbers change."
        },
        {
          "title": "Swap places",
          "text": "Only the places that fit the timetable are selected to start with. Tap “Want to go” or “Going” to change them, and a hint for your combination appears."
        },
        {
          "title": "Read the notes at the top",
          "text": "Tap a number and the things that could catch you out (the last bus, bookings, tattoos, the cold) come first, with times and fees below."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map by Toshi, put together from official websites and photos from Wikimedia Commons."
    },
    "introFor": {
      "late": {
        "kicker": "A day trip from Asahikawa (snow-free season: late April–October)",
        "h1": "Hills by bike in the morning, the Blue Pond and a waterfall by bus in the afternoon, then a hot spring.",
        "lead": "A day in Biei without a car. Take the 9:38 train from Asahikawa, rent an e-bike by the station and ride to the trees and lookouts of Patchwork Road. Lunch at the stone-warehouse roadside station, then the 13:45 bus to the Shirogane Blue Pond. See Shirahige Falls dropping into a river of the same blue, soak at Shirogane Onsen and have dinner in Biei before the 18:40 train (Asahikawa 19:13).",
        "favName": "Shirogane Blue Pond",
        "favText": "Dead larch trunks standing in blue water. (Photo: MaedaAkihiko / CC BY-SA 4.0)",
        "favPhoto": [
          "pond",
          0
        ],
        "who": [
          "No car needed: the JR Furano Line, Dohoku Bus, and an e-bike for the hills (rent by the station; ask the shop about price and season)",
          "Only a few buses a day run to Shirogane. The last one back leaves Shirogane Onsen at 18:02",
          "The Blue Pond is busiest from 13:00 to 15:00 on sunny days",
          "Every famous tree stands in a farmer’s field. Stay on the road",
          "None of the hotels states a tattoo policy on its site; phone before you go",
          "IC cards on the Furano Line are unconfirmed. Buy a paper ticket",
          "Times are from the December 2026 timetable. Re-check after the spring 2027 revision"
        ],
        "dayHead": "The day at a glance",
        "day": [
          {
            "time": "9:38",
            "area": "Asahikawa",
            "title": "The Furano Line to Biei",
            "text": "Arrive 10:12 and rent an e-bike by the station. (Photo: LR0725 / CC BY-SA 4.0)",
            "photo": [
              "eki",
              0
            ],
            "note": "Biei 10:12"
          },
          {
            "time": "10:45",
            "area": "Patchwork Road",
            "title": "Hokusei-no-oka and the Ken & Mary Tree",
            "text": "Hills and mountains from the lookout. (Photo: Choi2451 / CC0)",
            "photo": [
              "hokusei",
              0
            ]
          },
          {
            "time": "11:45",
            "area": "Patchwork Road",
            "title": "Seven Stars Tree",
            "text": "Fields in different colours. (Photo: Babiesan / CC BY-SA 3.0)",
            "photo": [
              "seven",
              0
            ]
          },
          {
            "time": "12:40",
            "area": "Biei Station",
            "title": "Lunch at the stone-warehouse roadside station",
            "text": "Canteen last orders 14:30. (Photo: Route275 / CC BY-SA 3.0)",
            "photo": [
              "machi",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "Shirogane",
            "title": "The Blue Pond",
            "text": "By the 13:45 bus; onward on the 15:07. (Photo: MaedaAkihiko / CC BY-SA 4.0)",
            "photo": [
              "pond",
              1
            ]
          },
          {
            "time": "15:15",
            "area": "Shirogane Onsen",
            "title": "Shirahige Falls and a hot spring",
            "text": "Falls and blue river from the bridge. (Photo: RJD / CC BY 3.0)",
            "photo": [
              "falls",
              0
            ]
          },
          {
            "time": "17:15",
            "area": "Biei Station",
            "title": "Dinner, then the 18:40 to Asahikawa",
            "text": "Or go straight back on the 17:39. (Photo: 欅 / CC BY-SA 3.0)",
            "photo": [
              "kaeri",
              0
            ],
            "note": "Asahikawa 19:13"
          }
        ],
        "dealsLead": "The train is ¥680 each way between Asahikawa and Biei. The bus is ¥800 from Biei Station to the Blue Pond and ¥900 from Shirogane Onsen back to Biei. The hills, the pond and the falls cost nothing to see.",
        "deals": [
          {
            "name": "JR Asahikawa → Biei",
            "price": "¥680",
            "text": "34 minutes on the Furano Line, about one train an hour. Covered by the JR Hokkaido Rail Pass. IC cards are unconfirmed, so buy a ticket.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Dohoku Bus: Biei Station → Blue Pond / Shirogane Onsen",
            "price": "¥800 / ¥900",
            "text": "Blue Pond to Shirogane Onsen is ¥220. Pay when you get off. A one-day pass is also sold (see the booking site for the price).",
            "url": "https://www.dohokubus.com/files/houmen/kaguraoka_biei_heijitu.pdf"
          },
          {
            "name": "Day bath at Shirogane Onsen",
            "price": "¥1,200–1,530",
            "text": "RIN and Yuyu ¥1,200, Hotel Park Hills ¥1,530; towels extra. If you have tattoos, phone ahead.",
            "url": "https://www.biei-hokkaido.jp/ja/hot-spring"
          },
          {
            "name": "E-bike rental by the station",
            "price": "Ask the shop",
            "text": "Shops are listed on the tourism association’s “getting around” page (Japanese). Allow 4–5 minutes per km.",
            "url": "https://www.biei-hokkaido.jp/ja/cruise"
          }
        ]
      },
      "early": {
        "kicker": "A day trip from Asahikawa (winter: November–mid-April)",
        "h1": "A lone tree on a snowy hill, a waterfall into a blue river, a hot spring, and after dark the Blue Pond lit up.",
        "lead": "A car-free winter day in Biei. Take the 9:38 train from Asahikawa, ride a small pre-booked bus to the Christmas Tree and have lunch in town. The 13:45 bus takes you to Shirogane for the blue river and Shirahige Falls in daylight, then a hot spring to warm up. After sunset, the 16:32 bus drops you at the Blue Pond, where lights pick out the snow-covered pond and its dead trees. The last bus at 18:05 returns you to Biei for the 18:40 train (Asahikawa 19:13). For Fridays and Saturdays we also describe a version using the bookable light-up tour bus.",
        "favName": "The Blue Pond light-up",
        "favText": "Nightly until 21 April 2027; from 16:30 in December. (Photo: Calistemon / CC BY-SA 4.0)",
        "favPhoto": [
          "pond",
          0
        ],
        "who": [
          "From December to March the lows drop below −15°C. At the Blue Pond you are outdoors for over an hour after dark, with no building open to warm up in",
          "The last bus back to Biei leaves the Blue Pond stop at 18:05. Miss it and only a taxi remains",
          "The Christmas Tree Liner must be booked two days ahead (1 December–28 February)",
          "On Fridays and Saturdays the tourism association’s bookable Biyu Bus light-up tour (from ¥4,000) is the easier way",
          "In winter the pond itself is under snow. The blue water you can see is the river below Shirahige Falls",
          "The sun sets around 16:00 in December. In March and April the lights come on after 18:00, too late for the last bus",
          "None of the hotels states a tattoo policy on its site; phone before you go",
          "Over New Year the buses run a special timetable and the roadside stations close"
        ],
        "dayHead": "The day at a glance",
        "day": [
          {
            "time": "9:38",
            "area": "Asahikawa",
            "title": "The Furano Line to Biei",
            "text": "Arrive 10:12; check in for the bus by 10:35. (Photo: Olegushka / CC BY-SA 4.0)",
            "photo": [
              "eki",
              0
            ],
            "note": "Biei 10:12"
          },
          {
            "time": "10:45",
            "area": "Biei hills",
            "title": "The Christmas Tree",
            "text": "An hour’s round trip on the bookable Liner. (Photo: oyakata / CC BY 3.0)",
            "photo": [
              "xmas",
              0
            ]
          },
          {
            "time": "11:50",
            "area": "Biei Station",
            "title": "Lunch at the stone-warehouse roadside station",
            "text": "Stay in town until the 13:45 bus. (Photo: Route275 / CC BY-SA 3.0)",
            "photo": [
              "machi",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "Shirogane Onsen",
            "title": "Shirahige Falls",
            "text": "The blue river and falls while it is light. (Photo: 663highland / CC BY 2.5)",
            "photo": [
              "falls",
              0
            ]
          },
          {
            "time": "14:45",
            "area": "Shirogane Onsen",
            "title": "Warm up in a hot spring",
            "text": "Out by 16:15 and wrap up again. (Photo: Kenneth Lee Sutherla… / CC BY 3.0)",
            "photo": [
              "onsen",
              0
            ]
          },
          {
            "time": "16:40",
            "area": "Shirogane",
            "title": "The Blue Pond light-up",
            "text": "By the 16:32 bus; back on the last bus at 18:05. (Photo: Tomoki Nagahira / CC BY 3.0)",
            "photo": [
              "pond",
              1
            ]
          },
          {
            "time": "18:40",
            "area": "Biei",
            "title": "The train to Asahikawa",
            "text": "If you miss it, the 19:54; the last is 21:19. (Photo: 欅 / CC BY-SA 3.0)",
            "photo": [
              "kaeri",
              0
            ],
            "note": "Asahikawa 19:13"
          }
        ],
        "dealsLead": "The train is ¥680 each way between Asahikawa and Biei. The bus is ¥900 from Biei Station to Shirogane Onsen, ¥220 on to the Blue Pond and ¥800 from the pond back to Biei. The light-up itself is free to see.",
        "deals": [
          {
            "name": "JR Asahikawa → Biei",
            "price": "¥680",
            "text": "34 minutes on the Furano Line, about one train an hour. Covered by the JR Hokkaido Rail Pass. IC cards are unconfirmed, so buy a ticket.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Dohoku Bus: Biei Station → Blue Pond / Shirogane Onsen",
            "price": "¥800 / ¥900",
            "text": "Blue Pond to Shirogane Onsen is ¥220. Pay when you get off. A one-day pass is also sold (see the booking site for the price).",
            "url": "https://www.dohokubus.com/files/houmen/kaguraoka_biei_heijitu.pdf"
          },
          {
            "name": "Christmas Tree Liner",
            "price": "From ¥2,000",
            "text": "1 December–28 February (not 31 December–5 January). 10:45, 13:20 and 14:50, about an hour. Book two days ahead.",
            "url": "https://www.biei-hokkaido.jp/ja/202627ws"
          },
          {
            "name": "Biyu Bus light-up tour (Fri, Sat)",
            "price": "From ¥4,000",
            "text": "Until 13 February 2027. Leaves Biei 16:35, back 18:30 (19:00 in February). Birch forest and Blue Pond. Book two days ahead.",
            "url": "https://www.biei-hokkaido.jp/ja/202627ws"
          },
          {
            "name": "Day bath at Shirogane Onsen",
            "price": "¥1,200–1,530",
            "text": "RIN and Yuyu ¥1,200, Hotel Park Hills ¥1,530; towels extra. If you have tattoos, phone ahead.",
            "url": "https://www.biei-hokkaido.jp/ja/hot-spring"
          }
        ]
      },
      "furano": {
        "kicker": "A day trip from Asahikawa (flower season: May–early October)",
        "h1": "Two flower gardens along the Furano Line: Farm Tomita in Nakafurano and Shikisai-no-oka at Bibaushi.",
        "lead": "A day of flower fields by train and on foot. The 9:38 from Asahikawa reaches Nakafurano at 10:46; walk 25 minutes to Farm Tomita, see the fields and have lunch there. Take the 13:27 back to Bibaushi and walk 30 minutes to Shikisai-no-oka. The 16:18 brings you to Biei for the stone-warehouse roadside station, a stroll and dinner before the 18:40 train (Asahikawa 19:13). The Blue Pond is not part of this course.",
        "favName": "The fields of Farm Tomita",
        "favText": "Bands of flowers across the slope. (Photo: 663highland / CC BY 2.5)",
        "favPhoto": [
          "tomita",
          0
        ],
        "who": [
          "Two walks of 25–30 minutes each way between station and garden. Bring a hat and a drink",
          "Trains run about once an hour. Miss the 13:27 from Nakafurano and the next is 15:55",
          "Peak lavender varies by year. Check Farm Tomita’s site for the latest before you go",
          "Shikisai-no-oka charges ¥800 only from July to September (cash at the counter). Farm Tomita’s admission is unconfirmed",
          "Dates for the summer Norokko train and the temporary Lavender-Batake Station have not been announced for 2027",
          "Times are from the December 2026 timetable. Re-check after the spring 2027 revision"
        ],
        "dayHead": "The day at a glance",
        "day": [
          {
            "time": "9:38",
            "area": "Asahikawa",
            "title": "The Furano Line to Nakafurano",
            "text": "Via Biei, arriving 10:46. (Photo: Nesnad / CC BY 4.0)",
            "photo": [
              "asahikawa",
              0
            ],
            "note": "Nakafurano 10:46"
          },
          {
            "time": "11:15",
            "area": "Nakafurano",
            "title": "Farm Tomita and lunch",
            "text": "Start back to the station by 12:55. (Photo: Maga-chan / CC BY-SA 2.1 jp)",
            "photo": [
              "tomita",
              1
            ]
          },
          {
            "time": "13:45",
            "area": "Bibaushi",
            "title": "On foot from the red-roofed station",
            "text": "Thirty minutes to Shikisai-no-oka. (Photo: Alberth2 / CC BY 3.0)",
            "photo": [
              "bibaushi",
              0
            ]
          },
          {
            "time": "14:15",
            "area": "Bibaushi",
            "title": "Shikisai-no-oka",
            "text": "Bands of flowers and the Tokachi range. (Photo: lumoplank / CC0)",
            "photo": [
              "shikisai",
              0
            ]
          },
          {
            "time": "16:30",
            "area": "Biei Station",
            "title": "The stone-warehouse roadside station and town",
            "text": "The 16:18 from Bibaushi arrives 16:25. (Photo: Route275 / CC BY-SA 3.0)",
            "photo": [
              "machi",
              0
            ]
          },
          {
            "time": "18:40",
            "area": "Biei",
            "title": "Dinner, then the train to Asahikawa",
            "text": "Or go straight back on the 17:39. (Photo: 欅 / CC BY-SA 3.0)",
            "photo": [
              "kaeri",
              0
            ],
            "note": "Asahikawa 19:13"
          }
        ],
        "dealsLead": "Trains: Asahikawa → Nakafurano ¥1,380, Nakafurano → Bibaushi ¥470, Bibaushi → Biei ¥320, Biei → Asahikawa ¥680. Shikisai-no-oka charges ¥800 from July to September only.",
        "deals": [
          {
            "name": "JR Asahikawa → Nakafurano",
            "price": "¥1,380",
            "text": "1 hr 8 min on the Furano Line. Covered by the JR Hokkaido Rail Pass.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "JR Nakafurano → Bibaushi → Biei → Asahikawa",
            "price": "¥470 + ¥320 + ¥680",
            "text": "Buy a ticket for each ride.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Shikisai-no-oka",
            "price": "¥800 (Jul–Sep)",
            "text": "No admission listed for other months. Rides and the alpaca farm cost extra.",
            "url": "http://www.shikisainooka.jp/en/"
          },
          {
            "name": "Farm Tomita",
            "price": "Please check",
            "text": "Admission could not be confirmed on the official site. No entry outside opening hours.",
            "url": "https://www.farm-tomita.co.jp/en/"
          }
        ]
      }
    }
  }
};
