/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都からJRと近江鉄道で湖東へ、太郎坊宮・永源寺・百済寺・教林坊の紅葉をめぐる日帰りルート。
   Photos are [spot number, photo index] from data/routes/higashiomi.json.
   5・6番の西明寺と金剛輪寺は2026年11月21日に追加（Toshi はまだ行っていない。写真は Wikimedia Commons、情報は公式サイトと湖東三山のチラシ）。
   時刻・料金は2026年11月20日に確認（各寺社の公式サイト・東近江市観光協会、電車とバスは乗換案内）。 */
window.HIGASHIOMI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都から日帰り 湖東の紅葉 Higashiomi MAP',
    titleMain: '湖東の紅葉',
    titleSub: 'Autumn in Higashiomi',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '太郎坊宮・永源寺・百済寺・教林坊は、西から東へ回ってから安土に戻る順番です。5・6番の西明寺と金剛輪寺は彦根から入る別の回り方で、6か所全部は1日で回れません。「選んで回る」で行く場所を選んでください。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（西明寺と金剛輪寺の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月20日',
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
    pickNote: '行きたい場所の「行きたい」を押してください。近江八幡駅はいつもルートに入ります。6か所全部は1日で回れないので、時間は目安です。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたいお寺や神社を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    intro: {
      "kicker": "秋のマップ｜紅葉の見ごろは例年11月中旬〜下旬",
      "h1": "742段の石段の先の紅葉から、竹林のライトアップまで。",
      "lead": "紅葉の見ごろは例年11月中旬から下旬です（湖東三山観光振興協議会と各寺の案内より）。京都からJRと近江鉄道で、湖東（ことう）の山あいへ。とがった山の中腹にある太郎坊宮、愛知川の渓谷の永源寺、苔むした参道の百済寺を回り、最後は春と秋だけ公開される教林坊の夜の庭へ。湖東三山の残りの2つ、西明寺と金剛輪寺へは、彦根駅からのシャトルバス（2026年は11月19日〜29日）で行けます。",
      "favLabel": "いちばんの見どころ",
      "favName": "永源寺",
      "favText": "山門と方丈を包む一面のもみじ。夕方からはライトアップも。",
      "favPhoto": [
        4,
        2
      ],
      "whoHead": "こんな人におすすめ",
      "who": [
        "京都の人ごみを離れて、静かな紅葉を見たい人に",
        "京都から近江八幡まで新快速で約35分（680円）",
        "太郎坊宮は742段の石段。歩きやすい靴で",
        "バスは本数が少なく、永源寺→百済寺と教林坊の行き帰りはタクシーがおすすめ",
        "教林坊は春と秋だけの公開。ライトアップは2026年は12月6日まで",
        "湖東三山を3つとも回るなら、彦根駅10:00発のシャトルバスで西明寺→金剛輪寺→百済寺の順に（太郎坊宮・永源寺とは別の日に）"
      ],
      "dayHead": "1日の流れ（目安）",
      "from": "",
      "day": [
        {
          "time": "8:27",
          "area": "近江八幡 → 太郎坊宮",
          "title": "石段を登って、勝運の神社へ",
          "text": "近江鉄道で太郎坊宮前へ。742段の石段と夫婦岩を通って本殿へ。近江の平野が見渡せます。",
          "photo": [
            3,
            5
          ]
        },
        {
          "time": "11:43",
          "area": "永源寺",
          "title": "渓谷のもみじと禅寺",
          "text": "八日市からバスで永源寺へ。山門と方丈のもみじを見て、門前でお昼を。",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "14:40",
          "area": "百済寺",
          "title": "苔むした参道を上る",
          "text": "タクシーで百済寺へ。石垣の参道と仁王門、本坊の庭と遠望台からの眺め。",
          "photo": [
            7,
            0
          ]
        },
        {
          "time": "18:30",
          "area": "教林坊 → 京都",
          "title": "竹林と庭のライトアップ",
          "text": "バスとJRで安土へ、タクシーで教林坊へ。夜の庭を見てから、安土19:55発で京都へ。",
          "note": "京都着は20:41",
          "photo": [
            8,
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費のめやす",
      "dealsLead": "電車は京都から太郎坊宮前まで1,070円、八日市駅から永源寺へのバスが670円。帰りは百済寺本町→安土が980円、安土→京都が770円です。拝観料（永源寺600円・百済寺600円・教林坊1,000円）とタクシー代は別にかかります。",
      "deals": [
        {
          "name": "電車（京都→太郎坊宮前）",
          "price": "1,070円",
          "text": "京都7:16発のJRで近江八幡へ、近江鉄道八日市線に乗り換えて太郎坊宮前8:27着。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "バス（八日市駅→永源寺前）",
          "price": "670円",
          "text": "近江鉄道バス、約30分。1時間に1〜2本です。",
          "url": "https://www.ohmitetudo.co.jp/bus/access/eigenji/"
        },
        {
          "name": "湖東三山シャトルバス（2026年11月19日〜29日）",
          "price": "1回200〜1,000円",
          "text": "彦根駅西口から西明寺・金剛輪寺・百済寺へ。彦根駅→西明寺700円、西明寺→金剛輪寺200円、金剛輪寺→百済寺300円、百済寺→彦根駅1,000円。1日乗り放題の「もみじきっぷ」は2,500円（当日、彦根駅西口かバスの中で現金で）。",
          "url": "https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/"
        },
        {
          "name": "タクシー",
          "price": "",
          "text": "永源寺→百済寺、安土駅↔教林坊（約10分）。料金は要確認。前もって予約し、教林坊からの帰りの迎えも頼んでおくと安心です。永源寺タクシー 0748-27-1151、近江タクシー 0748-37-0106、滋賀第一交通 近江八幡営業所 0748-37-4000。",
          "url": "https://www.higashiomi.net/guide/access.html"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月20日に確認しました（各寺社の公式サイト、東近江市観光協会、電車とバスは乗換案内）。タクシー代は確認できていません。",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "最初は「選んで回る」",
          "text": "行きたいお寺や神社だけを選ぶと、駅とルートが自動で決まります。1日で回れるのは「太郎坊宮・永源寺・百済寺・教林坊」か「西明寺・金剛輪寺・百済寺（・教林坊）」の組み合わせです。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・バスの時刻・おすすめの時間が見られます。"
        },
        {
          "title": "あなたのルートの一言",
          "text": "選んだ組み合わせに合わせて、バスや帰り方の一言が出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。"
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Day trip from Kyoto: Autumn leaves in Higashiomi MAP',
    titleMain: 'Autumn in Higashiomi',
    titleSub: '湖東の紅葉',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Taroubou-gu, Eigenji, Hyakusaiji and Kyorinbo run west to east, then back to Azuchi. Nos. 5 and 6, Saimyoji and Kongorinji, are reached from Hikone instead, and all six won’t fit in one day. Use “Choose stops” to pick your places. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (the Saimyoji and Kongorinji photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 20, 2026',
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
    pickNote: 'Tap “Want to go” on the places you like. Omi-Hachiman Station is always on your route. All six places won’t fit in one day, so treat the times as a guide.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: 'Nothing chosen yet. Pick the temples and shrine you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      "kicker": "Autumn map | Leaves usually peak mid to late November",
      "h1": "From maples above 742 stone steps to a lantern-lit bamboo grove.",
      "lead": "The leaves usually peak from mid to late November (according to the Koto Sanzan tourism council and the temples). By JR and the Ohmi Railway from Kyoto into the hills east of Lake Biwa. Visit Taroubou-gu halfway up a pointed peak, Eigenji in the Echigawa valley and Hyakusaiji with its mossy approach, then end at the night garden of Kyorinbo, open only in spring and autumn. The other two Koto Sanzan temples, Saimyoji and Kongorinji, are reached by shuttle bus from Hikone Station (19–29 November in 2026).",
      "favLabel": "Highlight",
      "favName": "Eigenji",
      "favText": "The great gate and abbot’s hall wrapped in maples, lit up from dusk.",
      "favPhoto": [
        4,
        2
      ],
      "whoHead": "Good to know",
      "who": [
        "For quiet autumn leaves away from Kyoto’s crowds",
        "Kyoto to Omi-Hachiman is about 35 min by Special Rapid (¥680)",
        "Taroubou-gu means 742 stone steps; wear good shoes",
        "Buses are sparse: taxis are easiest from Eigenji to Hyakusaiji and to and from Kyorinbo",
        "Kyorinbo opens only in spring and autumn; the 2026 illumination runs until 6 December",
        "For all three Koto Sanzan temples, take the 10:00 shuttle bus from Hikone: Saimyoji, Kongorinji, then Hyakusaiji (on a different day from Taroubou-gu and Eigenji)"
      ],
      "dayHead": "One day, roughly like this",
      "from": "From",
      "day": [
        {
          "time": "8:27",
          "area": "Omi-Hachiman → Taroubou-gu",
          "title": "Up the steps to the shrine of victory",
          "text": "Ohmi Railway to Taroubougu-mae, then 742 steps and the Meoto-iwa rocks to the main hall, with views over the Omi plain.",
          "photo": [
            3,
            5
          ]
        },
        {
          "time": "11:43",
          "area": "Eigenji",
          "title": "A Zen temple in a maple valley",
          "text": "Bus from Yokaichi to Eigenji. See the gate and abbot’s hall in red, and have lunch on the approach.",
          "photo": [
            4,
            0
          ]
        },
        {
          "time": "14:40",
          "area": "Hyakusaiji",
          "title": "Up the mossy approach",
          "text": "Taxi to Hyakusaiji: stone-walled approach, the Nio gate, the garden and the lookout.",
          "photo": [
            7,
            0
          ]
        },
        {
          "time": "18:30",
          "area": "Kyorinbo → Kyoto",
          "title": "Bamboo and garden by lantern light",
          "text": "Bus and JR to Azuchi, taxi to Kyorinbo. See the night garden, then the 19:55 train from Azuchi.",
          "note": "Arrive Kyoto 20:41",
          "photo": [
            8,
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares",
      "dealsLead": "Trains from Kyoto to Taroubougu-mae are ¥1,070 and the bus from Yokaichi to Eigenji ¥670. Back: Hyakusaiji-honmachi → Azuchi ¥980, Azuchi → Kyoto ¥770. Admission (Eigenji ¥600, Hyakusaiji ¥600, Kyorinbo ¥1,000) and taxis are extra.",
      "deals": [
        {
          "name": "Train (Kyoto → Taroubougu-mae)",
          "price": "¥1,070",
          "text": "JR from Kyoto at 7:16 to Omi-Hachiman, change to the Ohmi Railway Yokaichi Line, arrive Taroubougu-mae 8:27.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Bus (Yokaichi → Eigenji-mae)",
          "price": "¥670",
          "text": "Ohmi Railway bus, about 30 min, 1–2 an hour.",
          "url": "https://www.ohmitetudo.co.jp/bus/access/eigenji/"
        },
        {
          "name": "Koto Sanzan shuttle bus (19–29 Nov 2026)",
          "price": "¥200–1,000 a ride",
          "text": "From Hikone Station west exit to Saimyoji, Kongorinji and Hyakusaiji. Hikone → Saimyoji ¥700, Saimyoji → Kongorinji ¥200, Kongorinji → Hyakusaiji ¥300, Hyakusaiji → Hikone ¥1,000. The “Momiji Kippu” day pass is ¥2,500 (cash on the day, at Hikone Station west exit or on the bus).",
          "url": "https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/"
        },
        {
          "name": "Taxis",
          "price": "",
          "text": "Eigenji → Hyakusaiji, and Azuchi Station ↔ Kyorinbo (about 10 min). Fares not confirmed. Book ahead, including the pick-up back from Kyorinbo. Eigenji Taxi 0748-27-1151, Ohmi Taxi 0748-37-0106, Shiga Daiichi Kotsu (Omi-Hachiman) 0748-37-4000.",
          "url": "https://www.higashiomi.net/guide/access.html"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 20, 2026 (temple and shrine websites, the Higashiomi tourism association, and a route planner for trains and buses). Taxi fares not confirmed.",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Starts in “Choose stops”",
          "text": "Pick only the temples and shrine you want; stations and the route follow automatically. A day fits either Taroubou-gu, Eigenji, Hyakusaiji and Kyorinbo, or Saimyoji, Kongorinji and Hyakusaiji (plus Kyorinbo)."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, to see photos, tips, fees, bus times and suggested times."
        },
        {
          "title": "Tips for your route",
          "text": "A short note on buses or getting home appears to match the places you choose."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions."
        }
      ],
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi."
    }
  }
};
