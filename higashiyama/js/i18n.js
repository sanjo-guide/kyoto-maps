/* Page texts in Japanese and English.
   Toshi 個人のマップ。清水寺から北へ、高台寺・八坂神社・南禅寺・永観堂・銀閣寺まで歩く。
   コースは2つ：早朝に出発（6:00の開門に清水寺）と、9〜10時に出発。出発は京都の中心・三条のあたりを想定。
   intro は「9〜10時に出発」の内容で、introFor[コース] が app.js で上書きされる（scripts/sync_higashiyama.py）。
   Photos are [spot id, photo index]（番号はコースで変わるので id で指定）。
   料金・時間は2026年11月20日〜22日に確認（確認できなかったものはデータに「要確認」と書いてある）。 */
window.HIGASHIYAMA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: "京都 東山｜清水寺・南禅寺・銀閣寺 Higashiyama MAP",
    titleMain: '京都 東山',
    titleSub: 'Higashiyama, Kyoto',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: "番号の順に歩くと、時間割どおりに回れます。清水寺と坂道は昼間とても混むので、人の少ない時間に歩きたい日は「早朝に出発」へ。点線は順番を示す線で、実際の道ではありません。",
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
    credit: "写真・文章：Toshi（哲学の道・銀閣寺、無鄰菴、真如堂と、青蓮院の一部の写真は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    train: '電車',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトで確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: "最初は、1日で無理なく回れる場所が選ばれています。めやすの時間は、この組み合わせの時間割です。足したい場所の「行きたい」を押すと、回り方の注意が出ます。",
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: "まだ選んでいません。下の一覧から、行きたい場所を選んでください。",
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "早朝に出発\n（5時台）",
    courseLate: "9〜10時に出発",
    swMode: "回り方",
    // 9〜10時に出発（late）の内容。早朝に出発（early）は introFor.early で上書きする
    intro: {
      "kicker": "Toshiが歩いて作った1日ルート",
      "favLabel": "いちばんの見どころ",
      "favName": "清水寺",
      "favText": "朝6:00に開きます。「清水の舞台」から京都の町を一望。",
      "favPhoto": [
        "kiyomizu",
        0
      ],
      "whoHead": "こんな人におすすめ",
      "from": "",
      "timeSuffix": "〜",
      "dealsHead": "交通費のめやす",
      "dealsMore": "公式サイトで見る",
      "howHead": "このマップの使い方",
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです。",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧のいちばん上のボタンで「早朝に出発」か「9〜10時に出発」を選びます。時間割と回る順番が切り替わります。"
        },
        {
          "title": "行かない場所を外す",
          "text": "最初は、1日で無理なく回れる場所が選ばれています。行かない場所は「行く」を押して外し、足したい場所は「行きたい」を押します。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・めやすの時間が見られます。入口で困ること（休み・撮影禁止など）は、いちばん上に出ます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。公式サイトへのリンクもあります。"
        }
      ],
      "h1": "清水の舞台から、南禅寺の水路閣、哲学の道、銀閣寺へ。東山を北へ歩く1日。",
      "lead": "三条を9時すぎに出て、清水寺から坂道を下り、高台寺、八坂神社、南禅寺、哲学の道を歩いて銀閣寺まで。18時ごろに街なかへ戻ります。清水寺と坂道は昼間とても混むので、人の少ない時間に歩きたい人は、一覧の上のボタンで「早朝に出発」を選んでください。",
      "who": [
        "三条のあたりを9時すぎに出て、18時ごろに戻る1日",
        "清水寺と産寧坂・二年坂は、昼間とても混みます。静かに歩きたい人は「早朝に出発」へ",
        "歩くのは全部で約9km。坂と石段が多いので、歩きやすい靴で",
        "銀閣寺は17:00まで（12〜2月は16:30）。南禅寺を15:25に出ます",
        "青蓮院・無鄰菴・永観堂・真如堂・金戒光明寺は時間割の外。足し方は各スポットに書いてあります",
        "伏見稲荷は別のマップ「伏見稲荷から七条へ」にあります"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "day": [
        {
          "time": "9:15",
          "area": "清水寺 → 八坂の塔",
          "title": "清水の舞台と石畳の坂道",
          "text": "三条から京阪で清水五条へ、坂を上って9:50に清水寺。産寧坂・二年坂を下って、八坂の塔へ。",
          "note": "昼間はとても混みます",
          "photo": [
            "kiyomizu",
            0
          ]
        },
        {
          "time": "11:50",
          "area": "ねねの道のあたり",
          "title": "お昼ごはん",
          "text": "八坂の塔から高台寺へ向かう道で。人の多い場所なので、12時より前に入るのがおすすめです。",
          "photo": [
            "yasakatower",
            0
          ]
        },
        {
          "time": "12:45",
          "area": "高台寺 → 八坂神社",
          "title": "ねねの寺と祇園の八坂さん",
          "text": "高台寺の庭と竹林を歩いて、八坂神社と円山公園へ。",
          "photo": [
            "kodaiji",
            0
          ]
        },
        {
          "time": "14:50",
          "area": "南禅寺 → 銀閣寺",
          "title": "水路閣から哲学の道へ",
          "text": "南禅寺の三門と水路閣を見て、哲学の道を歩いて銀閣寺へ（16:05〜16:40）。",
          "note": "銀閣寺は17:00まで（12〜2月は16:30）",
          "photo": [
            "nanzenji",
            0
          ]
        },
        {
          "time": "17:00",
          "area": "街なかへ",
          "title": "バスで戻って、夜は祇園・先斗町へ",
          "text": "銀閣寺道から市バスで戻ると18時ごろ。秋の夜は、高台寺（12月13日まで22:00閉門）、清水寺（11月30日まで21:30閉門）、青蓮院・永観堂・金戒光明寺（12月6日まで）のライトアップがあります。ほかの時期は、祇園や先斗町（ぽんとちょう）で晩ごはんを。",
          "photo": [
            "yasaka",
            0
          ]
        }
      ],
      "dealsLead": "行きは京阪電車で180円、帰りは市バスで230円。あとは歩きます（拝観料は別）。",
      "deals": [
        {
          "name": "京阪電車（三条→清水五条）",
          "price": "180円",
          "text": "約3分。清水五条駅から清水寺まで、坂を上って歩いて約25分です。",
          "url": "https://www.keihan.co.jp/traffic/"
        },
        {
          "name": "帰り：市バス（銀閣寺道から）",
          "price": "230円",
          "text": "四条河原町・三条京阪・京都駅のほうへ。どの系統がどこを通るかは、バス停の案内で確かめてください。",
          "url": "https://www.city.kyoto.lg.jp/kotsu/"
        }
      ],
      "dealsNote": "大人の運賃です。京阪は2026年11月22日に乗換案内で、市バスは11月20日に京都市交通局で確認しました。"
    },
    introFor: {
      late: {
        "h1": "清水の舞台から、南禅寺の水路閣、哲学の道、銀閣寺へ。東山を北へ歩く1日。",
        "lead": "三条を9時すぎに出て、清水寺から坂道を下り、高台寺、八坂神社、南禅寺、哲学の道を歩いて銀閣寺まで。18時ごろに街なかへ戻ります。清水寺と坂道は昼間とても混むので、人の少ない時間に歩きたい人は、一覧の上のボタンで「早朝に出発」を選んでください。",
        "who": [
          "三条のあたりを9時すぎに出て、18時ごろに戻る1日",
          "清水寺と産寧坂・二年坂は、昼間とても混みます。静かに歩きたい人は「早朝に出発」へ",
          "歩くのは全部で約9km。坂と石段が多いので、歩きやすい靴で",
          "銀閣寺は17:00まで（12〜2月は16:30）。南禅寺を15:25に出ます",
          "青蓮院・無鄰菴・永観堂・真如堂・金戒光明寺は時間割の外。足し方は各スポットに書いてあります",
          "伏見稲荷は別のマップ「伏見稲荷から七条へ」にあります"
        ],
        "dayHead": "1日の流れ（9〜10時に出発）",
        "day": [
          {
            "time": "9:15",
            "area": "清水寺 → 八坂の塔",
            "title": "清水の舞台と石畳の坂道",
            "text": "三条から京阪で清水五条へ、坂を上って9:50に清水寺。産寧坂・二年坂を下って、八坂の塔へ。",
            "note": "昼間はとても混みます",
            "photo": [
              "kiyomizu",
              0
            ]
          },
          {
            "time": "11:50",
            "area": "ねねの道のあたり",
            "title": "お昼ごはん",
            "text": "八坂の塔から高台寺へ向かう道で。人の多い場所なので、12時より前に入るのがおすすめです。",
            "photo": [
              "yasakatower",
              0
            ]
          },
          {
            "time": "12:45",
            "area": "高台寺 → 八坂神社",
            "title": "ねねの寺と祇園の八坂さん",
            "text": "高台寺の庭と竹林を歩いて、八坂神社と円山公園へ。",
            "photo": [
              "kodaiji",
              0
            ]
          },
          {
            "time": "14:50",
            "area": "南禅寺 → 銀閣寺",
            "title": "水路閣から哲学の道へ",
            "text": "南禅寺の三門と水路閣を見て、哲学の道を歩いて銀閣寺へ（16:05〜16:40）。",
            "note": "銀閣寺は17:00まで（12〜2月は16:30）",
            "photo": [
              "nanzenji",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "街なかへ",
            "title": "バスで戻って、夜は祇園・先斗町へ",
            "text": "銀閣寺道から市バスで戻ると18時ごろ。秋の夜は、高台寺（12月13日まで22:00閉門）、清水寺（11月30日まで21:30閉門）、青蓮院・永観堂・金戒光明寺（12月6日まで）のライトアップがあります。ほかの時期は、祇園や先斗町（ぽんとちょう）で晩ごはんを。",
            "photo": [
              "yasaka",
              0
            ]
          }
        ],
        "dealsLead": "行きは京阪電車で180円、帰りは市バスで230円。あとは歩きます（拝観料は別）。",
        "deals": [
          {
            "name": "京阪電車（三条→清水五条）",
            "price": "180円",
            "text": "約3分。清水五条駅から清水寺まで、坂を上って歩いて約25分です。",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "帰り：市バス（銀閣寺道から）",
            "price": "230円",
            "text": "四条河原町・三条京阪・京都駅のほうへ。どの系統がどこを通るかは、バス停の案内で確かめてください。",
            "url": "https://www.city.kyoto.lg.jp/kotsu/"
          }
        ],
        "dealsNote": "大人の運賃です。京阪は2026年11月22日に乗換案内で、市バスは11月20日に京都市交通局で確認しました。"
      },
      early: {
        "h1": "朝6時、開いたばかりの清水寺へ。八坂の塔と坂道を、店が開く前に歩く。",
        "lead": "清水寺は朝6:00に開きます。三条を5時すぎに歩いて出て、八坂の塔と坂道の写真を撮りながら上り、開門に合わせて舞台へ。8:00に二年坂のスターバックスが開いたら朝ごはんにして、9:00の開門に高台寺へ。そのあと八坂神社、青蓮院、南禅寺、永観堂、金戒光明寺、真如堂、銀閣寺まで歩きます。",
        "who": [
          "早起きして、人の少ない清水寺と坂道を歩きたい人に",
          "三条から八坂の塔まで歩いて約30分。5時台に動いている電車は京阪だけです",
          "11月〜2月の朝6時はまだ暗いです",
          "朝ごはんは8:00から、二年坂のスターバックスで",
          "歩くのは全部で約11km。長い1日なので、行かない場所は外してください",
          "真如堂は受付15:45まで、銀閣寺は17:00まで。16:45ごろ銀閣寺で終わります"
        ],
        "dayHead": "1日の流れ（早朝に出発）",
        "day": [
          {
            "time": "5:05",
            "area": "八坂の塔 → 清水寺",
            "title": "開門前の塔と坂道、6:00の清水寺",
            "text": "三条から歩いて5:35に八坂の塔。二年坂・産寧坂を上って、6:00の開門に清水寺へ（7:15まで）。",
            "note": "11月〜2月は、6時はまだ暗い",
            "photo": [
              "yasakatower",
              0
            ]
          },
          {
            "time": "8:00",
            "area": "二年坂",
            "title": "朝ごはんとひと休み",
            "text": "坂をゆっくり下って、8:00に開く町家のスターバックスへ。9:00に高台寺が開くまで休みます。",
            "photo": [
              "sanneizaka",
              0
            ]
          },
          {
            "time": "9:00",
            "area": "高台寺 → 八坂神社 → 青蓮院",
            "title": "ねねの寺、祇園の八坂さん、大クスノキの青蓮院",
            "text": "開門に合わせて高台寺と圓徳院へ。ねねの道を歩いて八坂神社と円山公園、10:50に青蓮院。",
            "photo": [
              "kodaiji",
              0
            ]
          },
          {
            "time": "11:55",
            "area": "南禅寺 → 永観堂",
            "title": "三門と水路閣、お昼、永観堂",
            "text": "南禅寺の三門に上って水路閣へ。12:45からお昼を食べて、13:40に永観堂。",
            "note": "永観堂の受付は16:00まで",
            "photo": [
              "nanzenji",
              0
            ]
          },
          {
            "time": "14:45",
            "area": "くろ谷 → 真如堂 → 銀閣寺",
            "title": "丘の上のお寺を2つ、最後に銀閣寺",
            "text": "金戒光明寺の山門をくぐり、となりの真如堂へ（15:15〜15:45）。坂を下りて哲学の道を歩き、16:10に銀閣寺。",
            "note": "真如堂の受付は15:45まで",
            "photo": [
              "ginkakuji",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "街なかへ",
            "title": "バスで戻って、夜は祇園・先斗町へ",
            "text": "銀閣寺道から市バスで戻ると17時半〜18時ごろ。秋の夜は、高台寺（12月13日まで22:00閉門）、清水寺（11月30日まで21:30閉門）、青蓮院・永観堂・金戒光明寺（12月6日まで）のライトアップがあります。ほかの時期は、祇園や先斗町（ぽんとちょう）で晩ごはんを。",
            "photo": [
              "yasaka",
              0
            ]
          }
        ],
        "dealsLead": "行きは歩き。帰りは銀閣寺道から市バスで230円です（拝観料は別）。",
        "deals": [
          {
            "name": "行き：歩き（電車なら京阪）",
            "price": "180円",
            "text": "三条から八坂の塔まで歩いて約30分。京阪は三条5:04発・5:24発で清水五条まで約3分、駅から坂を上って約20分です。",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "帰り：市バス（銀閣寺道から）",
            "price": "230円",
            "text": "四条河原町・三条京阪・京都駅のほうへ。どの系統がどこを通るかは、バス停の案内で確かめてください。",
            "url": "https://www.city.kyoto.lg.jp/kotsu/"
          }
        ],
        "dealsNote": "大人の運賃です。京阪の時刻と運賃は2026年11月22日に乗換案内で（11月24日 火曜の時刻）、市バスは11月20日に京都市交通局で確認しました。"
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: "Higashiyama, Kyoto | Kiyomizu-dera, Nanzen-ji, Ginkaku-ji MAP",
    titleMain: 'Higashiyama, Kyoto',
    titleSub: '京都 東山',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: "Walk the stops in number order to follow the timetable. Kiyomizu-dera and the lanes below it are very crowded in the daytime: to walk them with fewer people, switch to “Early start”. The dotted line shows the order, not the actual path.",
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
    credit: "Photos &amp; text: Toshi (the photos of the Philosopher’s Path and Ginkaku-ji, Murin-an and Shinnyo-do, and some of Shoren-in, are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors",
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on the official website on {d}. Details can change, so please check before you go.',
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
    pickNote: "The map opens with a set of places that fits comfortably into one day, and the rough times are the timetable for that set. Tap “Want to go” to add a place and a note on how to fit it in appears.",
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: "Nothing chosen yet. Pick the places you want from the list below.",
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "Early start\n(before 6 am)",
    courseLate: "Leave at 9–10",
    swMode: "Stops",
    // 9〜10時に出発（late）の内容。早朝に出発（early）は introFor.early で上書きする
    intro: {
      "kicker": "A day route, hand-walked by Toshi",
      "favLabel": "Don’t miss",
      "favName": "Kiyomizu-dera",
      "favText": "Open from 6:00 in the morning, with Kyoto spread out below the wooden stage.",
      "favPhoto": [
        "kiyomizu",
        0
      ],
      "whoHead": "Who it’s for",
      "from": "From",
      "timeSuffix": "",
      "dealsHead": "Getting around: fares",
      "dealsMore": "See official site",
      "howHead": "How to use this map",
      "cta": "Open the map",
      "footer1": "An original map, hand-walked by Toshi.",
      "how": [
        {
          "title": "Choose your start time",
          "text": "Use the buttons at the top of the list to pick “Early start” or “Leave at 9–10”. The timetable and the order of the stops change with it."
        },
        {
          "title": "Drop what you don’t want",
          "text": "The map opens with a set of places that fits comfortably into one day. Tap “Going” to drop a place, or “Want to go” to add one."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map, or open the list, for photos, notes, fees and rough times. Anything that could stop you at the door (closing days, no-photo rules) is shown first."
        },
        {
          "title": "Get directions",
          "text": "Use “Open in Google Maps” at each spot for directions. There are links to official websites too."
        }
      ],
      "h1": "From the Kiyomizu stage to Nanzen-ji’s aqueduct, the Philosopher’s Path and Ginkaku-ji: a day walking north through Higashiyama.",
      "lead": "Leave Sanjo a little after 9:00, walk down the lanes from Kiyomizu-dera, then on to Kodai-ji, Yasaka Shrine, Nanzen-ji and along the Philosopher’s Path to Ginkaku-ji, getting back downtown at about 18:00. Kiyomizu-dera and its lanes are very crowded in the daytime: to walk them with fewer people, choose “Early start” with the buttons above the list.",
      "who": [
        "A day that leaves the Sanjo area after 9:00 and is back at about 18:00",
        "Kiyomizu-dera, Sannenzaka and Ninenzaka are very crowded by day. For a quieter walk, use “Early start”",
        "About 9 km on foot in all, with slopes and stone steps. Wear proper shoes",
        "Ginkaku-ji closes at 17:00 (16:30 Dec–Feb): you leave Nanzen-ji at 15:25",
        "Shoren-in, Murin-an, Eikan-do, Shinnyo-do and Konkai Komyo-ji are outside the timetable; each spot explains how to fit it in",
        "Fushimi Inari is on a separate map, “Fushimi Inari to Shichijo”"
      ],
      "dayHead": "The day (leaving at 9–10)",
      "day": [
        {
          "time": "9:15",
          "area": "Kiyomizu-dera → Yasaka Pagoda",
          "title": "The Kiyomizu stage and stone-paved lanes",
          "text": "Keihan train from Sanjo to Kiyomizu-Gojo, then uphill to reach Kiyomizu-dera at 9:50. Walk down Sannenzaka and Ninenzaka to Yasaka Pagoda.",
          "note": "Very crowded in the daytime",
          "photo": [
            "kiyomizu",
            0
          ]
        },
        {
          "time": "11:50",
          "area": "Around Nene-no-michi",
          "title": "Lunch",
          "text": "On the way from the pagoda to Kodai-ji. It’s a busy area, so try to sit down before noon.",
          "photo": [
            "yasakatower",
            0
          ]
        },
        {
          "time": "12:45",
          "area": "Kodai-ji → Yasaka Shrine",
          "title": "Nene’s temple and Gion’s shrine",
          "text": "Walk the garden and bamboo path of Kodai-ji, then on to Yasaka Shrine and Maruyama Park.",
          "photo": [
            "kodaiji",
            0
          ]
        },
        {
          "time": "14:50",
          "area": "Nanzen-ji → Ginkaku-ji",
          "title": "From the aqueduct to the Philosopher’s Path",
          "text": "See Nanzen-ji’s gate and aqueduct, then walk the Philosopher’s Path to Ginkaku-ji (16:05–16:40).",
          "note": "Ginkaku-ji closes at 17:00 (16:30 Dec–Feb)",
          "photo": [
            "nanzenji",
            0
          ]
        },
        {
          "time": "17:00",
          "area": "Back downtown",
          "title": "Bus back, then Gion or Pontocho for the evening",
          "text": "A city bus from Ginkakuji-michi gets you back at about 18:00. On autumn evenings Kodai-ji (open until 22:00 through 13 Dec), Kiyomizu-dera (until 21:30 through 30 Nov), Shoren-in, Eikan-do and Konkai Komyo-ji (through 6 Dec) are lit up. At other times of year, have dinner in Gion or Pontocho.",
          "photo": [
            "yasaka",
            0
          ]
        }
      ],
      "dealsLead": "¥180 by Keihan train on the way out and ¥230 by city bus on the way back; the rest is on foot (temple fees not included).",
      "deals": [
        {
          "name": "Keihan line (Sanjo → Kiyomizu-Gojo)",
          "price": "¥180",
          "text": "About 3 minutes. From Kiyomizu-Gojo Station it’s about 25 minutes uphill on foot to Kiyomizu-dera.",
          "url": "https://www.keihan.co.jp/traffic/"
        },
        {
          "name": "Way back: city bus (from Ginkakuji-michi)",
          "price": "¥230",
          "text": "Toward Shijo-Kawaramachi, Sanjo-Keihan or Kyoto Station. Check the sign at the stop for which route goes where.",
          "url": "https://www.city.kyoto.lg.jp/kotsu/"
        }
      ],
      "dealsNote": "Adult fares. Keihan checked on a route planner on Nov 22, 2026; city bus checked with the Kyoto City Transportation Bureau on Nov 20."
    },
    introFor: {
      late: {
        "h1": "From the Kiyomizu stage to Nanzen-ji’s aqueduct, the Philosopher’s Path and Ginkaku-ji: a day walking north through Higashiyama.",
        "lead": "Leave Sanjo a little after 9:00, walk down the lanes from Kiyomizu-dera, then on to Kodai-ji, Yasaka Shrine, Nanzen-ji and along the Philosopher’s Path to Ginkaku-ji, getting back downtown at about 18:00. Kiyomizu-dera and its lanes are very crowded in the daytime: to walk them with fewer people, choose “Early start” with the buttons above the list.",
        "who": [
          "A day that leaves the Sanjo area after 9:00 and is back at about 18:00",
          "Kiyomizu-dera, Sannenzaka and Ninenzaka are very crowded by day. For a quieter walk, use “Early start”",
          "About 9 km on foot in all, with slopes and stone steps. Wear proper shoes",
          "Ginkaku-ji closes at 17:00 (16:30 Dec–Feb): you leave Nanzen-ji at 15:25",
          "Shoren-in, Murin-an, Eikan-do, Shinnyo-do and Konkai Komyo-ji are outside the timetable; each spot explains how to fit it in",
          "Fushimi Inari is on a separate map, “Fushimi Inari to Shichijo”"
        ],
        "dayHead": "The day (leaving at 9–10)",
        "day": [
          {
            "time": "9:15",
            "area": "Kiyomizu-dera → Yasaka Pagoda",
            "title": "The Kiyomizu stage and stone-paved lanes",
            "text": "Keihan train from Sanjo to Kiyomizu-Gojo, then uphill to reach Kiyomizu-dera at 9:50. Walk down Sannenzaka and Ninenzaka to Yasaka Pagoda.",
            "note": "Very crowded in the daytime",
            "photo": [
              "kiyomizu",
              0
            ]
          },
          {
            "time": "11:50",
            "area": "Around Nene-no-michi",
            "title": "Lunch",
            "text": "On the way from the pagoda to Kodai-ji. It’s a busy area, so try to sit down before noon.",
            "photo": [
              "yasakatower",
              0
            ]
          },
          {
            "time": "12:45",
            "area": "Kodai-ji → Yasaka Shrine",
            "title": "Nene’s temple and Gion’s shrine",
            "text": "Walk the garden and bamboo path of Kodai-ji, then on to Yasaka Shrine and Maruyama Park.",
            "photo": [
              "kodaiji",
              0
            ]
          },
          {
            "time": "14:50",
            "area": "Nanzen-ji → Ginkaku-ji",
            "title": "From the aqueduct to the Philosopher’s Path",
            "text": "See Nanzen-ji’s gate and aqueduct, then walk the Philosopher’s Path to Ginkaku-ji (16:05–16:40).",
            "note": "Ginkaku-ji closes at 17:00 (16:30 Dec–Feb)",
            "photo": [
              "nanzenji",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Back downtown",
            "title": "Bus back, then Gion or Pontocho for the evening",
            "text": "A city bus from Ginkakuji-michi gets you back at about 18:00. On autumn evenings Kodai-ji (open until 22:00 through 13 Dec), Kiyomizu-dera (until 21:30 through 30 Nov), Shoren-in, Eikan-do and Konkai Komyo-ji (through 6 Dec) are lit up. At other times of year, have dinner in Gion or Pontocho.",
            "photo": [
              "yasaka",
              0
            ]
          }
        ],
        "dealsLead": "¥180 by Keihan train on the way out and ¥230 by city bus on the way back; the rest is on foot (temple fees not included).",
        "deals": [
          {
            "name": "Keihan line (Sanjo → Kiyomizu-Gojo)",
            "price": "¥180",
            "text": "About 3 minutes. From Kiyomizu-Gojo Station it’s about 25 minutes uphill on foot to Kiyomizu-dera.",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "Way back: city bus (from Ginkakuji-michi)",
            "price": "¥230",
            "text": "Toward Shijo-Kawaramachi, Sanjo-Keihan or Kyoto Station. Check the sign at the stop for which route goes where.",
            "url": "https://www.city.kyoto.lg.jp/kotsu/"
          }
        ],
        "dealsNote": "Adult fares. Keihan checked on a route planner on Nov 22, 2026; city bus checked with the Kyoto City Transportation Bureau on Nov 20."
      },
      early: {
        "h1": "Kiyomizu-dera at 6 am, just as it opens, with Yasaka Pagoda and the lanes before the shops wake up.",
        "lead": "Kiyomizu-dera opens at 6:00. Leave Sanjo on foot a little after 5:00, photograph Yasaka Pagoda and the lanes on your way up, and be at the stage for opening. When the Starbucks on Ninenzaka opens at 8:00, have breakfast, then go into Kodai-ji when it opens at 9:00. From there walk on to Yasaka Shrine, Shoren-in, Nanzen-ji, Eikan-do, Konkai Komyo-ji, Shinnyo-do and Ginkaku-ji.",
        "who": [
          "For early risers who want Kiyomizu-dera and the lanes with fewer people",
          "About 30 minutes on foot from Sanjo to Yasaka Pagoda. The only trains running before six are on the Keihan line",
          "At 6:00 it is still dark from November to February",
          "Breakfast from 8:00 at the Starbucks on Ninenzaka",
          "About 11 km on foot in all. It’s a long day, so drop the places you can live without",
          "Shinnyo-do’s last entry is 15:45 and Ginkaku-ji closes at 17:00; you finish at Ginkaku-ji at about 16:45"
        ],
        "dayHead": "The day (early start)",
        "day": [
          {
            "time": "5:05",
            "area": "Yasaka Pagoda → Kiyomizu-dera",
            "title": "The pagoda and lanes before opening, Kiyomizu-dera at 6:00",
            "text": "Walk from Sanjo to reach Yasaka Pagoda at 5:35. Climb Ninenzaka and Sannenzaka to be at Kiyomizu-dera for the 6:00 opening (until 7:15).",
            "note": "Still dark at 6:00 from November to February",
            "photo": [
              "yasakatower",
              0
            ]
          },
          {
            "time": "8:00",
            "area": "Ninenzaka",
            "title": "Breakfast and a rest",
            "text": "Come slowly back down the lanes to the townhouse Starbucks, which opens at 8:00, and rest until Kodai-ji opens at 9:00.",
            "photo": [
              "sanneizaka",
              0
            ]
          },
          {
            "time": "9:00",
            "area": "Kodai-ji → Yasaka Shrine → Shoren-in",
            "title": "Nene’s temple, Gion’s shrine and the camphor trees of Shoren-in",
            "text": "Go into Kodai-ji and Entoku-in at opening, walk Nene-no-michi to Yasaka Shrine and Maruyama Park, and reach Shoren-in at 10:50.",
            "photo": [
              "kodaiji",
              0
            ]
          },
          {
            "time": "11:55",
            "area": "Nanzen-ji → Eikan-do",
            "title": "The gate and aqueduct, lunch, Eikan-do",
            "text": "Climb Nanzen-ji’s gate and walk to the aqueduct. Lunch from 12:45, then Eikan-do at 13:40.",
            "note": "Eikan-do: last entry 16:00",
            "photo": [
              "nanzenji",
              0
            ]
          },
          {
            "time": "14:45",
            "area": "Kurodani → Shinnyo-do → Ginkaku-ji",
            "title": "Two hilltop temples, then Ginkaku-ji",
            "text": "Pass under the great gate of Konkai Komyo-ji and on to Shinnyo-do next door (15:15–15:45). Walk down the hill and along the Philosopher’s Path to reach Ginkaku-ji at 16:10.",
            "note": "Shinnyo-do: last entry 15:45",
            "photo": [
              "ginkakuji",
              0
            ]
          },
          {
            "time": "17:00",
            "area": "Back downtown",
            "title": "Bus back, then Gion or Pontocho for the evening",
            "text": "A city bus from Ginkakuji-michi gets you back at about 17:30–18:00. On autumn evenings Kodai-ji (open until 22:00 through 13 Dec), Kiyomizu-dera (until 21:30 through 30 Nov), Shoren-in, Eikan-do and Konkai Komyo-ji (through 6 Dec) are lit up. At other times of year, have dinner in Gion or Pontocho.",
            "photo": [
              "yasaka",
              0
            ]
          }
        ],
        "dealsLead": "You walk out. The way back is ¥230 by city bus from Ginkakuji-michi (temple fees not included).",
        "deals": [
          {
            "name": "Way out: on foot (or the Keihan line)",
            "price": "¥180",
            "text": "About 30 minutes on foot from Sanjo to Yasaka Pagoda. Keihan trains leave Sanjo at 5:04 and 5:24, about 3 minutes to Kiyomizu-Gojo, then a 20-minute climb.",
            "url": "https://www.keihan.co.jp/traffic/"
          },
          {
            "name": "Way back: city bus (from Ginkakuji-michi)",
            "price": "¥230",
            "text": "Toward Shijo-Kawaramachi, Sanjo-Keihan or Kyoto Station. Check the sign at the stop for which route goes where.",
            "url": "https://www.city.kyoto.lg.jp/kotsu/"
          }
        ],
        "dealsNote": "Adult fares. Keihan times and fares are from a route planner on Nov 22, 2026 (for Tuesday, Nov 24); city bus checked with the Kyoto City Transportation Bureau on Nov 20."
      }
    }
  }
};
