/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都の南、京阪沿線の春のルート。コースは3つ（scripts/build_yawata_data.py）:
     kawazu … 3月：淀水路の河津桜（intro はこの内容）
     sakura … 3月末〜4月上旬：背割堤の桜。9:30ごろ発（introFor.sakura で上書き）
     early  … 3月末〜4月上旬：背割堤の開園9:00へ（introFor.early で上書き）
   春以外に開くと offKicker・offHow・offHowText・offLead・offNote が足される（日付は scripts/sync_yawata.py）。
   Photos are [spot id, photo index]（コースで番号が変わるので id で指定）.
   時刻・料金は2026年11月22日に確認（各公式サイト、観光協会、電車は乗換案内）。春の日程・料金は2026年春の実績。 */
window.YAWATA_I18N = {
  ja: {
    htmlLang: "ja",
    docTitle: "京都 淀・八幡の桜（春のマップ） Yawata MAP",
    titleMain: "淀・八幡の桜",
    titleSub: "Yodo & Yawata cherries",
    howto: "使い方",
    allMaps: "← マップ一覧",
    home: "マップ一覧",
    tabMap: "地図",
    menu: "メニュー",
    list: "一覧",
    listHead: "スポット一覧",
    listNote: "上のボタンで時期と出発時間を選ぶと、場所と順番が変わります。点線は順番を示す線で、実際の道ではありません。",
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
    hours: "時間",
    fee: "料金",
    train: "電車",
    closed: "休み",
    cash: '現金を用意してください',
    checked: "{d}に公式サイトや観光協会の案内、乗換案内で確認しました。春の日程・料金は2026年の実績です。行く前にその年の発表を見てください。",
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: "2026年11月22日",
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
    pickNote: "行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。外したときの回り方は、各スポットの「あなたのルートでは」に出ます。",
    pickCount: "選んだ場所 {n}か所",
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたい場所を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    offKicker: "春のマップ（3月〜4月上旬）",
    offLead: "いまは見ごろの時期ではありません。日程・料金は2026年春の実績、電車は2026年11月の時刻で、来春は要確認です。",
    offNote: "春（3月〜4月上旬）のマップです。いまは見ごろの時期ではありません。来春の日程・料金・時刻は要確認。",
    cable: "ケーブル",
    swCourse: "行く時期・出発時間",
    courseAria: "行く時期・出発時間",
    courseKawazu: "3月：淀の河津桜\n9:30ごろ三条発",
    courseSakura: "3月末〜4月上旬：背割堤の桜\n9:30ごろ三条発",
    courseEarly: "3月末〜4月上旬：背割堤の開園9:00へ\n8:10ごろ三条発",
    swMode: "回り方",
    offHow: "春のマップです（いまは季節外）",
    offHowText: "3月〜4月上旬に使うマップで、いまは桜の時期ではありません。",
    intro: {
      "kicker": "Toshiが歩いて作った京都の春のルート",
      "h1": "3月は淀の河津桜。山の上の国宝に寄って、夜は伏見の酒蔵の町。",
      "lead": "細い水路に沿って、約1.3kmに約300本の河津桜。京都でひと足早いお花見を、淀で。そのあとは1駅となりの八幡で100年以上続く朝日屋の鯖寿司、ケーブルで山の上の国宝・石清水八幡宮、3つの川が見渡せる展望塔へ。夜は伏見の酒蔵の町で晩ごはん。淀の河津桜（例年3月上旬〜中旬）と背割堤の桜（例年3月末〜4月上旬）は咲く時期が違うので、コースを分けました。このコースは3月用で、9:30ごろ三条を出ます。4月に行く人は一覧の上のボタンで切り替えてください。",
      "favLabel": "いちばんの見どころ",
      "favName": "淀水路の河津桜",
      "favText": "細い水路に約1.3km、約300本。京都でひと足早いお花見です。",
      "favPhoto": [
        "yodo",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "河津桜の例年の見ごろは3月上旬〜中旬。年によって2週間ほどずれます",
        "淀駅は改札の外にトイレがありません。降りたら改札を出る前に",
        "月曜は朝日屋も走井餅も休み。お弁当を持って。火曜は朝日屋と伏見の黄桜酒場が休み",
        "展望塔の最終受付は16:20。3月の背割堤はまだ咲いていません",
        "ケーブルは毎時15分・45分発、最終18:15。下りは石段の表参道を歩いて30〜35分",
        "春の日程・料金は2026年の実績、電車は2026年11月の時刻。来春は要確認"
      ],
      "dayHead": "1日の流れ（3月：淀の河津桜）",
      "from": "",
      "day": [
        {
          "time": "10:05",
          "area": "淀",
          "title": "水路沿いの河津桜",
          "text": "三条から京阪で20分あまり、駅から歩いて10分。帰りに淀城跡と與杼神社へ。",
          "note": "三条9:29発（土日祝9:26発）",
          "photo": [
            "yodo",
            0
          ]
        },
        {
          "time": "11:50",
          "area": "八幡",
          "title": "駅前でお昼",
          "text": "1駅移って、100年以上続く朝日屋の鯖寿司。月・火は休みです。",
          "note": "淀11:38発（土日祝11:37発）",
          "photo": [
            "iwashimizu",
            7
          ]
        },
        {
          "time": "12:55",
          "area": "男山",
          "title": "石清水八幡宮と展望台",
          "text": "ケーブルで山の上の国宝へ。帰りは表参道を歩き、門前で走井餅。",
          "photo": [
            "iwashimizu",
            0
          ]
        },
        {
          "time": "15:30",
          "area": "三川合流",
          "title": "3つの川の展望塔",
          "text": "さくらであい館の展望塔から川と京都の町を眺めます。",
          "note": "最終受付16:20",
          "photo": [
            "deaikan",
            1
          ]
        },
        {
          "time": "17:00",
          "area": "伏見 → 三条",
          "title": "酒蔵の町で晩ごはん",
          "text": "川沿いを歩いて、18:00ごろ黄桜酒場へ。20:06に三条へ戻り、先斗町・木屋町で21〜22時ごろまで。",
          "note": "火曜は祇園四条へ直帰",
          "photo": [
            "iwashimizu",
            5
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と料金のめやす",
      "dealsLead": "淀水路、石清水八幡宮の境内、背割堤は無料です。桜まつりの協力金や有料になる時期の展望塔は別にかかります。",
      "deals": [
        {
          "name": "京阪 三条→淀",
          "price": "360円",
          "text": "丹波橋で乗り換え、22〜24分。淀→石清水八幡宮は240円。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "石清水八幡宮参道ケーブル",
          "price": "片道300円",
          "text": "往復600円。8:10〜18:15、約3分。",
          "url": "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
        },
        {
          "name": "石清水八幡宮→中書島",
          "price": "320円",
          "text": "9〜10分。中書島→三条も320円。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "石清水八幡宮→祇園四条",
          "price": "360円",
          "text": "25分ほど。三条までは400円。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日に確認しました。春の日程・料金は2026年の実績で、来春は要確認です。",
      "dealsMore": "確認したページを見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "行く時期を選ぶ（春のマップです）",
          "text": "一覧の上のボタンで「3月：淀の河津桜」と「3月末〜4月上旬：背割堤」を切り替えます。背割堤は昼に混むので、開園9:00に合わせるコースもあります。"
        },
        {
          "title": "番号の順に",
          "text": "番号の順に回ります。最後のスポットに、夕方の続き、夜、帰りの最終を書いています。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "「選んで回る」に切り替えて外すと、そのときの行き方が出ます。"
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
      "sakura": {
        "h1": "午前は山の上の国宝、午後は1.4kmの桜のトンネル。夜は祇園の夜桜へ。",
        "lead": "木津川と宇治川にはさまれた堤防に、約220本のソメイヨシノが1.4kmのトンネルになります。人の多い堤防はあとに回して、先にケーブルで山の上の石清水八幡宮へ。駅前でお昼、展望塔から並木を見下ろしてから、桜の下を歩きます。夕方は祇園四条に戻って夜桜と晩ごはん。背割堤が見ごろになる3月末〜4月上旬用のコースで、9:30ごろ三条を出ます。人の少ないうちに歩きたい人は開園9:00のコースへ、3月の河津桜の人は3月のコースへ切り替えてください。",
        "favName": "背割堤の桜並木",
        "favText": "木津川と宇治川の間に、約220本のソメイヨシノのトンネル。",
        "favPhoto": [
          "sewaritei",
          0
        ],
        "who": [
          "背割堤の例年の見ごろは3月末〜4月上旬。開園は9:00〜17:00",
          "さくらまつりは入場時に運営協力金（2026年は1人100円以上）。支払い方法は要確認なので小銭を",
          "展望塔の最終受付は16:20。2026年のまつりの間は300円でした",
          "一般の駐車場はなし。電車で。堤防の上は自転車の押し歩きも禁止",
          "月曜は朝日屋も走井餅も休み。火曜は朝日屋が休み。お弁当か会場の屋台で",
          "春の日程・料金は2026年の実績、電車は2026年11月の時刻。来春は要確認"
        ],
        "dayHead": "1日の流れ（背割堤の桜）",
        "day": [
          {
            "time": "10:25",
            "area": "男山",
            "title": "石清水八幡宮へケーブルで",
            "text": "人の多い堤防はあとに。国宝の社殿と展望台、帰りは表参道を歩きます。",
            "note": "三条9:29発（土日祝9:26発）",
            "photo": [
              "iwashimizu",
              0
            ]
          },
          {
            "time": "12:30",
            "area": "八幡",
            "title": "駅前で鯖寿司",
            "text": "朝日屋でお昼。月・火は休みなので、お弁当か会場の屋台で。",
            "photo": [
              "iwashimizu",
              7
            ]
          },
          {
            "time": "13:40",
            "area": "三川合流",
            "title": "先に展望塔へ",
            "text": "列ができても受付に間に合うよう、堤防より先に上がります。",
            "note": "最終受付16:20",
            "photo": [
              "deaikan",
              0
            ]
          },
          {
            "time": "14:30",
            "area": "背割堤",
            "title": "桜のトンネル",
            "text": "行きは堤防の上、帰りは芝生から。出たら門前の走井餅でひと休み。",
            "note": "閉園17:00",
            "photo": [
              "sewaritei",
              2
            ]
          },
          {
            "time": "18:00",
            "area": "祇園 → 三条",
            "title": "夜桜と晩ごはん",
            "text": "祇園白川と円山公園へ（2026年は18:00〜22:00に点灯。来春は要確認）。そのあと先斗町・木屋町で21〜22時ごろまで。",
            "note": "八幡17:14発（土日祝17:12発）",
            "photo": [
              "sewaritei",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "京阪 三条→石清水八幡宮",
            "price": "400円",
            "text": "25〜28分。帰りの祇園四条までは360円。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "石清水八幡宮参道ケーブル",
            "price": "片道300円",
            "text": "往復600円。8:10〜18:15、約3分。",
            "url": "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
          },
          {
            "name": "背割堤の運営協力金",
            "price": "100円以上",
            "text": "さくらまつりの間。2026年の実績で、来春は要確認。",
            "url": "https://www.yodogawa-park.jp/cms/wp-content/uploads/2026/03/bb7e63930cdcd26969e16163becee2c9.pdf"
          },
          {
            "name": "展望塔（さくらまつりの間）",
            "price": "300円",
            "text": "子ども100円。2026年の実績で、来春は要確認。ふだんは無料。",
            "url": "https://totteoki.kyoto.travel/wp-content/uploads/2026/03/kyotoyawatasansaku-chirashi_compressed.pdf"
          }
        ]
      },
      "early": {
        "h1": "開園の9:00に桜のトンネルへ。午後は伏見の酒蔵、夜は祇園の夜桜。",
        "lead": "昼に混み合う前の、朝の桜のトンネルへ。開館の9:00に展望塔に上がって並木を見下ろし、背割堤を歩いたら、門前の走井餅でひと休み。そのあと石清水八幡宮、遅めのお昼、伏見の月桂冠大倉記念館、夜は祇園の夜桜へ。3月末〜4月上旬用のコースで、8:10ごろ三条を出ます。朝ゆっくりしたい人は9:30ごろ発のコースに切り替えてください。",
        "favName": "背割堤の桜並木",
        "favText": "昼に人が増える前に、約1.4kmの桜のトンネルへ。",
        "favPhoto": [
          "sewaritei",
          0
        ],
        "who": [
          "背割堤の例年の見ごろは3月末〜4月上旬。開園は9:00〜17:00",
          "さくらまつりは入場時に運営協力金（2026年は1人100円以上）。支払い方法は要確認なので小銭を",
          "展望塔の最終受付は16:20。2026年のまつりの間は300円でした",
          "一般の駐車場はなし。電車で。堤防の上は自転車の押し歩きも禁止",
          "月曜は朝日屋も走井餅も休み。火曜は朝日屋が休み。お弁当か会場の屋台で",
          "春の日程・料金は2026年の実績、電車は2026年11月の時刻。来春は要確認",
          "月桂冠大倉記念館は受付16:00まで、現金不可。混む日は前日16:30までに予約を"
        ],
        "dayHead": "1日の流れ（背割堤の開園へ）",
        "day": [
          {
            "time": "9:00",
            "area": "三川合流",
            "title": "開館に合わせて展望塔",
            "text": "列ができる前に上がって、並木を見下ろします。",
            "note": "三条8:11発（土日祝8:12発）",
            "photo": [
              "deaikan",
              0
            ]
          },
          {
            "time": "9:35",
            "area": "背割堤",
            "title": "桜のトンネルと朝のひと休み",
            "text": "並木を歩いたら、門前の走井餅（9:00から、月曜休み）へ。",
            "photo": [
              "sewaritei",
              2
            ]
          },
          {
            "time": "11:55",
            "area": "男山",
            "title": "石清水八幡宮",
            "text": "ケーブルで上がって、表参道を歩いて下ります。",
            "photo": [
              "iwashimizu",
              0
            ]
          },
          {
            "time": "13:55",
            "area": "八幡",
            "title": "遅めのお昼",
            "text": "駅前の朝日屋で鯖寿司。月・火は休みです。",
            "photo": [
              "iwashimizu",
              7
            ]
          },
          {
            "time": "15:35",
            "area": "伏見",
            "title": "月桂冠大倉記念館",
            "text": "おみやげときき酒つきで600円。受付16:00まで、現金不可。",
            "note": "八幡15:13発",
            "photo": [
              "deaikan",
              2
            ]
          },
          {
            "time": "18:00",
            "area": "祇園 → 三条",
            "title": "夜桜と晩ごはん",
            "text": "祇園白川と円山公園へ（2026年は18:00〜22:00に点灯。来春は要確認）。そのあと先斗町・木屋町で21〜22時ごろまで。",
            "note": "中書島17:27発（土日祝17:26発）",
            "photo": [
              "sewaritei",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "京阪 三条→石清水八幡宮",
            "price": "400円",
            "text": "25〜28分。帰りの祇園四条までは360円。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "石清水八幡宮参道ケーブル",
            "price": "片道300円",
            "text": "往復600円。8:10〜18:15、約3分。",
            "url": "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
          },
          {
            "name": "背割堤の運営協力金",
            "price": "100円以上",
            "text": "さくらまつりの間。2026年の実績で、来春は要確認。",
            "url": "https://www.yodogawa-park.jp/cms/wp-content/uploads/2026/03/bb7e63930cdcd26969e16163becee2c9.pdf"
          },
          {
            "name": "展望塔（さくらまつりの間）",
            "price": "300円",
            "text": "子ども100円。2026年の実績で、来春は要確認。ふだんは無料。",
            "url": "https://totteoki.kyoto.travel/wp-content/uploads/2026/03/kyotoyawatasansaku-chirashi_compressed.pdf"
          },
          {
            "name": "月桂冠大倉記念館",
            "price": "600円",
            "text": "20歳以上。おみやげときき酒つき、現金不可。",
            "url": "https://www.gekkeikan.co.jp/enjoy/museum/access/"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: "en",
    docTitle: "Kyoto: Yodo & Yawata cherries, a spring map",
    titleMain: "Yodo & Yawata cherries",
    titleSub: "淀・八幡の桜",
    howto: "How to use",
    allMaps: "← All maps",
    home: "All maps",
    tabMap: "Map",
    menu: "Menu",
    list: "Spots",
    listHead: "All spots",
    listNote: "Choose the season and start time with the buttons above: the stops and order change. The dotted line shows the order, not the actual path.",
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
    hours: "Hours",
    fee: "Fee",
    train: "Train",
    closed: "Closed",
    cash: 'Bring cash',
    checked: "Checked on official websites, tourism association pages and a route planner on {d}. Spring dates and fees are from 2026, so check that year’s announcement before you go.",
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: "Nov 22, 2026",
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
    pickNote: "Tap “Want to go” on the places you like. Times are for the full route. If you skip a place, see “On your route” at each spot for what changes.",
    pickCount: "{n} places chosen",
    pickEmpty: 'Nothing chosen yet. Pick the places you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    offKicker: "A spring map (March to early April)",
    offLead: "The blossoms aren’t at their best now. Dates and fees are from spring 2026 and train times from November 2026, so please check for next spring. ",
    offNote: "A map for March to early April; the blossoms aren’t at their best now. Please check next spring’s dates, fees and times. ",
    cable: "Cable car",
    swCourse: "Season & start time",
    courseAria: "Season and start time",
    courseKawazu: "March: Kawazu cherries at Yodo\nLeave Sanjo about 9:30",
    courseSakura: "Late Mar – early Apr: Sewaritei\nLeave Sanjo about 9:30",
    courseEarly: "Late Mar – early Apr: Sewaritei at 9:00 opening\nLeave Sanjo about 8:10",
    swMode: "Stops",
    offHow: "A spring map: out of season now",
    offHowText: "This map is for March to early April; it isn’t cherry season now. ",
    intro: {
      "kicker": "A spring route south of Kyoto, hand-walked by Toshi",
      "h1": "Kawazu cherries in March, a shrine on a hill, dinner among sake breweries.",
      "lead": "About 300 Kawazu cherry trees along 1.3 km of narrow canal at Yodo: an early taste of spring in Kyoto. Then mackerel sushi in Yawata, one stop on, from Asahiya, open for over 100 years; a cable car up to Iwashimizu Hachimangu, a national treasure on the hill; the tower over three rivers; and dinner in Fushimi’s sake district. Yodo’s Kawazu cherries (usually early to mid March) and Sewaritei (usually late March to early April) bloom at different times, so they have separate courses. This one is for March and leaves Sanjo about 9:30. Coming in April? Switch with the buttons above the list.",
      "favLabel": "Highlight",
      "favName": "Kawazu cherries at Yodo",
      "favText": "About 300 trees along 1.3 km of narrow canal, ahead of the main season.",
      "favPhoto": [
        "yodo",
        0
      ],
      "whoHead": "Good to know before you go",
      "who": [
        "The Kawazu cherries are usually best in early to mid March, but can shift by two weeks",
        "There are no toilets outside Yodo Station’s ticket gates: go before you leave",
        "On Mondays Asahiya and Hashiriimochi are both closed: bring lunch. On Tuesdays Asahiya and Kizakura Sakaba close",
        "Last entry to the tower is 16:20. Sewaritei isn’t in bloom yet in March",
        "Cable car at :15 and :45, last at 18:15. The walk down is 30–35 minutes with stone steps",
        "Spring dates and fees are from 2026, train times from November 2026: please check for next spring"
      ],
      "dayHead": "One day, roughly like this (March)",
      "from": "From",
      "day": [
        {
          "time": "10:05",
          "area": "Yodo",
          "title": "Kawazu cherries by the canal",
          "text": "A little over 20 minutes by Keihan, then 10 on foot. Stop at the castle ruins and shrine on the way back.",
          "note": "Sanjo 9:29 (weekends 9:26)",
          "photo": [
            "yodo",
            0
          ]
        },
        {
          "time": "11:50",
          "area": "Yawata",
          "title": "Lunch by the station",
          "text": "One stop on: mackerel sushi at century-old Asahiya. Closed Mondays and Tuesdays.",
          "note": "Yodo 11:38 (weekends 11:37)",
          "photo": [
            "iwashimizu",
            7
          ]
        },
        {
          "time": "12:55",
          "area": "Mt. Otokoyama",
          "title": "The shrine and lookout",
          "text": "Cable car up to the National Treasure. Walk down for rice cakes at the gate.",
          "photo": [
            "iwashimizu",
            0
          ]
        },
        {
          "time": "15:30",
          "area": "Three rivers",
          "title": "The observation tower",
          "text": "Rivers and the city from Sakura Deaikan’s tower.",
          "note": "Last entry 16:20",
          "photo": [
            "deaikan",
            1
          ]
        },
        {
          "time": "17:00",
          "area": "Fushimi → Sanjo",
          "title": "Dinner in the sake town",
          "text": "Walk the canal, dinner at Kizakura Sakaba about 18:00. Back at Sanjo at 20:06, then Pontocho or Kiyamachi until 21:00 or 22:00.",
          "note": "Tuesdays: straight to Gion",
          "photo": [
            "iwashimizu",
            5
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "The Yodo canal, shrine grounds and Sewaritei are free. Festival contributions and the tower in busy periods cost extra.",
      "deals": [
        {
          "name": "Keihan Sanjo → Yodo",
          "price": "¥360",
          "text": "Change at Tambabashi, 22–24 min. Yodo → Iwashimizu-hachimangu ¥240.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Iwashimizu Sando cable car",
          "price": "¥300 one way",
          "text": "¥600 return. 8:10–18:15, about 3 min.",
          "url": "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
        },
        {
          "name": "Iwashimizu-hachimangu → Chushojima",
          "price": "¥320",
          "text": "9–10 min. Chushojima → Sanjo is also ¥320.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Iwashimizu-hachimangu → Gion-Shijo",
          "price": "¥360",
          "text": "About 25 min. ¥400 to Sanjo.",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 22, 2026. Spring dates and fees are from 2026; please check for next spring.",
      "dealsMore": "See the source",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick your season (this is a spring map)",
          "text": "The buttons above the list switch between Yodo in March and Sewaritei in late March to early April. Sewaritei is crowded around midday, so there is also a 9:00-opening course."
        },
        {
          "title": "In number order",
          "text": "Follow the numbers. The last stop covers the late afternoon, the evening and last trains."
        },
        {
          "title": "Skip what you like",
          "text": "Switch to “Choose stops” to drop a place, and see what changes."
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
      "sakura": {
        "h1": "A hilltop shrine, 1.4 km of blossom overhead, then Gion after dark.",
        "lead": "Between the Kizu and Uji rivers, about 220 Somei-yoshino cherries make a 1.4 km tunnel along the levee. Save the crowded levee for later and ride the cable car up to Iwashimizu Hachimangu first. Lunch by the station, then look down on the avenue from the tower before walking under the blossom. In the evening, back to Gion-Shijo for lamplit cherries and dinner. This course is for Sewaritei’s season, late March to early April, leaving Sanjo about 9:30. For fewer people switch to the 9:00-opening course; for Kawazu cherries, to the March course.",
        "favName": "Sewaritei cherry avenue",
        "favText": "About 220 trees form a tunnel between two rivers.",
        "favPhoto": [
          "sewaritei",
          0
        ],
        "who": [
          "Sewaritei is usually best late March to early April. The park opens 9:00–17:00",
          "The festival asks a contribution on entry (¥100+ in 2026). Payment methods aren’t stated, so bring coins",
          "Last entry to the tower is 16:20. It cost ¥300 during the 2026 festival",
          "No public parking: come by train. No bicycles on the top path, even pushed",
          "On Mondays Asahiya and Hashiriimochi close; on Tuesdays Asahiya. Bring lunch or use the festival stalls",
          "Spring dates and fees are from 2026, train times from November 2026: please check for next spring"
        ],
        "dayHead": "One day, roughly like this (Sewaritei)",
        "day": [
          {
            "time": "10:25",
            "area": "Mt. Otokoyama",
            "title": "Cable car to the shrine",
            "text": "The levee can wait. See the National Treasure and lookout, then walk down.",
            "note": "Sanjo 9:29 (weekends 9:26)",
            "photo": [
              "iwashimizu",
              0
            ]
          },
          {
            "time": "12:30",
            "area": "Yawata",
            "title": "Mackerel sushi",
            "text": "Lunch at Asahiya by the station. Closed Mondays and Tuesdays: bring a picnic or use the stalls.",
            "photo": [
              "iwashimizu",
              7
            ]
          },
          {
            "time": "13:40",
            "area": "Three rivers",
            "title": "The tower first",
            "text": "Go up before the levee, so a queue can’t cost you the last entry.",
            "note": "Last entry 16:20",
            "photo": [
              "deaikan",
              0
            ]
          },
          {
            "time": "14:30",
            "area": "Sewaritei",
            "title": "The tunnel of blossom",
            "text": "Out along the top, back on the grass, then rice cakes by the shrine gate.",
            "note": "Closes 17:00",
            "photo": [
              "sewaritei",
              2
            ]
          },
          {
            "time": "18:00",
            "area": "Gion → Sanjo",
            "title": "Cherries by night, and dinner",
            "text": "Gion Shirakawa and Maruyama Park (lit 18:00–22:00 in 2026; please check for next spring), then Pontocho or Kiyamachi until 21:00 or 22:00.",
            "note": "Yawata 17:14 (weekends 17:12)",
            "photo": [
              "sewaritei",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "Keihan Sanjo → Iwashimizu-hachimangu",
            "price": "¥400",
            "text": "25–28 min. ¥360 back to Gion-Shijo.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Iwashimizu Sando cable car",
            "price": "¥300 one way",
            "text": "¥600 return. 8:10–18:15, about 3 min.",
            "url": "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
          },
          {
            "name": "Sewaritei festival contribution",
            "price": "¥100 or more",
            "text": "During the festival, as in 2026. Please check for next spring.",
            "url": "https://www.yodogawa-park.jp/cms/wp-content/uploads/2026/03/bb7e63930cdcd26969e16163becee2c9.pdf"
          },
          {
            "name": "Tower during the festival",
            "price": "¥300",
            "text": "Children ¥100, as in 2026; please check for next spring. Usually free.",
            "url": "https://totteoki.kyoto.travel/wp-content/uploads/2026/03/kyotoyawatasansaku-chirashi_compressed.pdf"
          }
        ]
      },
      "early": {
        "h1": "The tunnel of blossom at 9:00, sake after lunch, Gion after dark.",
        "lead": "The tunnel of blossom in the morning, before the midday crowds. Go up the tower when it opens at 9:00 to look down on the avenue, walk the levee, then rest at Hashiriimochi. After that: the hilltop shrine, a late lunch, Gekkeikan’s sake museum in Fushimi and cherries by night in Gion. This course is for late March to early April and leaves Sanjo about 8:10. For a slower morning switch to the 9:30 course.",
        "favName": "Sewaritei cherry avenue",
        "favText": "1.4 km of blossom overhead, before the midday crowds.",
        "favPhoto": [
          "sewaritei",
          0
        ],
        "who": [
          "Sewaritei is usually best late March to early April. The park opens 9:00–17:00",
          "The festival asks a contribution on entry (¥100+ in 2026). Payment methods aren’t stated, so bring coins",
          "Last entry to the tower is 16:20. It cost ¥300 during the 2026 festival",
          "No public parking: come by train. No bicycles on the top path, even pushed",
          "On Mondays Asahiya and Hashiriimochi close; on Tuesdays Asahiya. Bring lunch or use the festival stalls",
          "Spring dates and fees are from 2026, train times from November 2026: please check for next spring",
          "Gekkeikan’s museum: last entry 16:00, no cash. On busy days book by 16:30 the day before"
        ],
        "dayHead": "One day, roughly like this (9:00 opening)",
        "day": [
          {
            "time": "9:00",
            "area": "Three rivers",
            "title": "The tower at opening",
            "text": "Up before the queue builds, to look down the avenue.",
            "note": "Sanjo 8:11 (weekends 8:12)",
            "photo": [
              "deaikan",
              0
            ]
          },
          {
            "time": "9:35",
            "area": "Sewaritei",
            "title": "Blossom, then a morning rest",
            "text": "Walk the avenue, then Hashiriimochi by the shrine gate (from 9:00, closed Mondays).",
            "photo": [
              "sewaritei",
              2
            ]
          },
          {
            "time": "11:55",
            "area": "Mt. Otokoyama",
            "title": "Iwashimizu Hachimangu",
            "text": "Cable car up, the main approach down.",
            "photo": [
              "iwashimizu",
              0
            ]
          },
          {
            "time": "13:55",
            "area": "Yawata",
            "title": "A late lunch",
            "text": "Mackerel sushi at Asahiya by the station. Closed Mondays and Tuesdays.",
            "photo": [
              "iwashimizu",
              7
            ]
          },
          {
            "time": "15:35",
            "area": "Fushimi",
            "title": "Gekkeikan sake museum",
            "text": "¥600 with a gift and tasting. Last entry 16:00, no cash.",
            "note": "Yawata 15:13",
            "photo": [
              "deaikan",
              2
            ]
          },
          {
            "time": "18:00",
            "area": "Gion → Sanjo",
            "title": "Cherries by night, and dinner",
            "text": "Gion Shirakawa and Maruyama Park (lit 18:00–22:00 in 2026; please check for next spring), then Pontocho or Kiyamachi until 21:00 or 22:00.",
            "note": "Chushojima 17:27 (weekends 17:26)",
            "photo": [
              "sewaritei",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "Keihan Sanjo → Iwashimizu-hachimangu",
            "price": "¥400",
            "text": "25–28 min. ¥360 back to Gion-Shijo.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Iwashimizu Sando cable car",
            "price": "¥300 one way",
            "text": "¥600 return. 8:10–18:15, about 3 min.",
            "url": "https://www.keihan.co.jp/traffic/time-fare/iwashimizu.html"
          },
          {
            "name": "Sewaritei festival contribution",
            "price": "¥100 or more",
            "text": "During the festival, as in 2026. Please check for next spring.",
            "url": "https://www.yodogawa-park.jp/cms/wp-content/uploads/2026/03/bb7e63930cdcd26969e16163becee2c9.pdf"
          },
          {
            "name": "Tower during the festival",
            "price": "¥300",
            "text": "Children ¥100, as in 2026; please check for next spring. Usually free.",
            "url": "https://totteoki.kyoto.travel/wp-content/uploads/2026/03/kyotoyawatasansaku-chirashi_compressed.pdf"
          },
          {
            "name": "Gekkeikan sake museum",
            "price": "¥600",
            "text": "Age 20 and over, with a gift and tasting. No cash.",
            "url": "https://www.gekkeikan.co.jp/enjoy/museum/access/"
          }
        ]
      }
    }
  }
};
