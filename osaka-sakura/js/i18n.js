/* Page texts in Japanese and English.
   Toshi 個人のマップ。大阪 造幣局の桜の通り抜け（4月中旬の約1週間だけの春のマップ）。起点は梅田〜難波のホテル。
   コースは2つ（scripts/build_osaka_sakura_data.py）:
     late  … 造幣局は午後の枠（15時ごろ）。午前は大阪城、夜は天満（intro はこの内容）
     early … 造幣局は朝いちばんの枠（平日10:00・土日9:00）。午後は大阪城、夜は道頓堀（introFor.early で上書き）
   通り抜けの時期以外に開くと offKicker・offHow・offHowText・offLead・offNote が足される（日付は scripts/sync_osaka_sakura.py）。
   Photos are [spot id, photo index]（コースで番号が変わるので id で指定）.
   時刻・料金は2026年11月23日に確認（造幣局・大阪城公園の公式サイト、大阪観光局、電車は乗換案内）。造幣局の日程・申し込みは2026年の実績。 */
window.OSAKA_SAKURA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '大阪 造幣局の桜の通り抜け（春のマップ） Osaka Sakura MAP',
    titleMain: '造幣局の桜の通り抜け',
    titleSub: 'Osaka Mint cherry walk',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '上のボタンで、造幣局に入る時間帯（申し込んだ枠）を選ぶと、順番が変わります。造幣局は南門から北門への一方通行です。点線は順番を示す線で、実際の道ではありません。',
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
    hours: '時間',
    fee: '料金',
    train: '電車',
    cable: 'ケーブル',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや大阪観光局の案内、乗換案内で確認しました。造幣局の日程・申し込みは2026年の実績です。行く前にその年の発表を見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月23日',
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
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。外したときの回り方は、各スポットの「あなたのルートでは」に出ます。',
    pickCount: '選んだ場所 {n}か所',
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたい場所を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    offKicker: '春のマップ（4月中旬の約1週間）',
    offLead: 'いまは通り抜けをやっていません。日程・時間・申し込み方法は2026年の実績、電車は2026年12月の時刻で、来春は要確認です（例年3月に造幣局が発表）。',
    offNote: '4月中旬の約1週間だけのマップです。いまは通り抜けをやっていません。来春の日程・申し込み・時刻は要確認。',
    offHow: '春のマップです（いまは通り抜けをやっていません）',
    offHowText: '造幣局の桜の通り抜けが開く4月中旬の約1週間に使うマップで、いまは時期ではありません。',
    swCourse: '造幣局に入る時間帯',
    courseAria: '造幣局に入る時間帯',
    courseLate: '午後の枠（15時ごろ）\n9:30ごろ梅田・なんば発',
    courseEarly: '朝いちばんの枠（平日10時・土日9時）\n9:15ごろ（土日8:20ごろ）発',
    swMode: '回り方',
    intro: {
      "kicker": "Toshiが歩いて作った大阪の春のルート",
      "h1": "年に1週間だけ開く、造幣局の八重桜の道。午前は大阪城、夜は天満で。",
      "lead": "造幣局の「桜の通り抜け」が開く4月中旬の約1週間のためのマップです（2026年は4月9日〜15日）。入るには事前の申し込みが要り、申し込んだ時間帯にしか入れないので、その時間に合わせてコースを2つ作りました。このコースは午後（15時ごろ）の枠の人用。9:30ごろ梅田・なんばを出て、大阪城の西の丸庭園と玉造口の八重桜、JO-TERRACE でお昼、造幣局、大川沿いの桜並木、夜は天満で晩ごはん。朝の枠の人は一覧の上のボタンで切り替えてください。",
      "favLabel": "いちばんの見どころ",
      "favName": "造幣局 桜の通り抜け",
      "favText": "約560mの道に、140品種331本の八重桜（2026年）。品種ごとの名札を見ながら歩きます。",
      "favPhoto": [
        "mint",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "造幣局は事前申込制。申し込みのない人、時間帯の違う人は入れません。2026年は3月18日9:00に受付開始（来春は要確認）",
        "中は飲食禁止。日傘・自撮り棒・三脚は不可で、入口で手荷物の検査があります",
        "西の丸庭園は月曜休み。通り抜けの週にも月曜があります",
        "大阪城のソメイヨシノは造幣局の八重桜より早く咲きます。通り抜けの週の大阪城は、南東の玉造口の八重桜へ",
        "京都からは京阪の三条・祇園四条から天満橋まで特急で約50分・490円",
        "日程・時間は2026年の実績、電車は2026年12月の時刻。来春は要確認"
      ],
      "dayHead": "1日の流れ（造幣局は午後の枠）",
      "from": "",
      "day": [
        {
          "time": "10:00",
          "area": "天満橋 → 大阪城",
          "title": "西の丸庭園と天守閣",
          "text": "梅田から地下鉄で5分。橋の上から大川を見て、大手門へ。芝生の庭から桜ごしに天守閣を見上げます。",
          "note": "東梅田9:35発（土日祝9:30発）",
          "photo": [
            "nishinomaru",
            0
          ]
        },
        {
          "time": "12:30",
          "area": "大阪城",
          "title": "玉造口の八重桜、JO-TERRACE でお昼",
          "text": "城の南東の遅咲きの八重桜を見て、大阪城公園駅の前でお昼。たこ焼き、とんかつ、和定食、カフェなど。",
          "photo": [
            "nishinomaru",
            3
          ]
        },
        {
          "time": "15:00",
          "area": "造幣局",
          "title": "八重桜の通り抜け",
          "text": "南門から北門へ、約560mの一方通行。申し込んだ時間帯に合わせて南門へ。",
          "photo": [
            "mint",
            1
          ]
        },
        {
          "time": "16:00",
          "area": "大川 → 天満",
          "title": "川沿いの桜並木、夜は天満で",
          "text": "桜宮橋を渡って東岸の遊歩道へ。夕方は天神橋筋商店街と天満駅のまわりで晩ごはん、21〜22時ごろまで。",
          "note": "京都へはJR天満21:03発（土日祝21:11発）",
          "photo": [
            "kema",
            0
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と料金",
      "dealsLead": "梅田・なんばから天満橋までは地下鉄で190〜240円。あとは歩きです。造幣局は無料（事前申込制）、毛馬桜之宮公園も無料です。",
      "deals": [
        {
          "name": "造幣局 桜の通り抜け",
          "price": "無料・事前申込制",
          "best": "先に申し込む",
          "text": "2026年はインターネットで入場の時間帯を選ぶ先着順で、3月18日9:00に受付開始。来春の日程と方法は例年3月に造幣局の公式サイトで発表されます（要確認）。",
          "url": "https://www.mint.go.jp/enjoy/toorinuke/sakura_osaka_news_r8.html"
        },
        {
          "name": "大阪城 西の丸庭園",
          "price": "300円",
          "text": "2026年4月からの大人の料金。観桜ナイター期（3月下旬〜4月上旬）は350円。月曜休み。",
          "url": "https://www.osakacastlepark.jp/articles/detail.html?id=72"
        },
        {
          "name": "大阪城天守閣",
          "price": "1,200円",
          "text": "9:00〜18:00（入館は17:30まで）。",
          "url": "https://osaka-info.jp/spot/osaka-castle-main-keep/"
        },
        {
          "name": "地下鉄（東梅田 → 天満橋）",
          "price": "190円",
          "text": "谷町線で4〜5分。なんばからは谷町九丁目で乗り換えて240円。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "京阪（三条 → 天満橋）",
          "price": "490円",
          "text": "京都から来る人。特急で約50分、乗り換えなし。",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月23日に確認しました。造幣局の日程・申し込みは2026年の実績で、来春は要確認です。",
      "dealsMore": "確認したページを見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "まず造幣局に申し込む",
          "text": "通り抜けは申し込んだ時間帯にしか入れません。一覧の上のボタンで、申し込めた枠（午後か朝いちばん）に合わせてコースを選んでください。"
        },
        {
          "title": "番号の順に",
          "text": "番号の順に回ります。最後のスポットに、夕方と夜の続き、帰りの最終を書いています。"
        },
        {
          "title": "番号をタップ",
          "text": "地図の番号か「一覧」をタップすると、写真・説明・料金・おすすめの時間が見られます。"
        },
        {
          "title": "Googleマップでルート検索",
          "text": "各スポットの「Googleマップで開く」から、そのままルート検索できます。"
        }
      ],
      "cta": "地図を見る",
      "footer1": "Toshiが実際に歩いて作った、オリジナルマップです（写真は2025年4月と2026年4月）。"
    },
    introFor: {
      "early": {
        "h1": "朝いちばんの枠で八重桜の道へ。川沿いを歩いて大阪城、夜は道頓堀。",
        "lead": "造幣局の「桜の通り抜け」が開く4月中旬の約1週間のためのマップです（2026年は4月9日〜15日）。このコースは、その日の最初の枠（2026年は平日10:00・土日9:00）に申し込めた人用。造幣局のあと大川沿いを歩いて大阪城へ、JO-TERRACE でお昼、玉造口の八重桜と天守閣、西の丸庭園。夕方は中之島を歩いて、夜は道頓堀へ。午後の枠の人は一覧の上のボタンで切り替えてください。",
        "dayHead": "1日の流れ（造幣局は朝いちばんの枠）",
        "day": [
          {
            "time": "10:00",
            "area": "造幣局",
            "title": "最初の枠で八重桜の通り抜け",
            "text": "天満橋から南門まで歩いて約15分。土日祝は9:00の枠なので1時間早く。",
            "note": "東梅田9:17発（土日祝8:25発）",
            "photo": [
              "mint",
              0
            ]
          },
          {
            "time": "11:00",
            "area": "大川 → 大阪城",
            "title": "川沿いの桜並木を歩いて、お昼",
            "text": "桜宮橋を渡って東岸を下流へ。大阪城公園駅の前の JO-TERRACE でお昼。",
            "photo": [
              "kema",
              0
            ]
          },
          {
            "time": "13:10",
            "area": "大阪城",
            "title": "玉造口の八重桜、天守閣、西の丸庭園",
            "text": "遅咲きの八重桜を見てから天守閣へ。西の丸庭園は入園16:30まで、月曜休み。",
            "photo": [
              "nishinomaru",
              0
            ]
          },
          {
            "time": "16:15",
            "area": "中之島 → 道頓堀",
            "title": "中之島を歩いて、夜は道頓堀",
            "text": "天満橋から中之島公園を西へ、淀屋橋から地下鉄でなんばへ。晩ごはんは大阪のマップを見て、21〜22時ごろまで。",
            "note": "京都へはなんば21:39発（土日祝21:48発）",
            "photo": [
              "temmabashi",
              1
            ]
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Osaka: the Mint cherry-blossom walk, a spring map',
    titleMain: 'Osaka Mint cherry walk',
    titleSub: '造幣局の桜の通り抜け',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Choose your Mint entry slot with the buttons above and the order changes. The Mint is one way, south gate to north gate. The dotted line shows the order, not the actual path.',
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
    hours: 'Hours',
    fee: 'Fee',
    train: 'Train',
    cable: 'Cable car',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites, Osaka Info and a route planner on {d}. The Mint’s dates and booking are as in 2026; check that year’s announcement before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 23, 2026',
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
    pickNote: 'Tap “Want to go” on the places you like. Times assume the full route; what to do when you skip a place appears under “On your route” in each spot.',
    pickCount: '{n} places chosen',
    pickEmpty: 'Nothing chosen yet. Pick the places you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    offKicker: 'A spring map (about one week in mid-April)',
    offLead: 'The Mint walk is not open now. Dates, hours and booking are as in 2026 and trains as of December 2026, so please check for next spring (the Mint announces each March). ',
    offNote: 'A map for about one week in mid-April; the Mint walk is not open now. Please check next spring’s dates, booking and times. ',
    offHow: 'A spring map: the Mint walk is not open now',
    offHowText: 'This map is for the week in mid-April when the Mint opens its cherry walk; it isn’t that time now. ',
    swCourse: 'Your Mint entry slot',
    courseAria: 'Your Mint entry slot',
    courseLate: 'Afternoon slot (about 15:00)\nLeave Umeda or Namba about 9:30',
    courseEarly: 'First slot (10:00 weekdays, 9:00 weekends)\nLeave about 9:15 (weekends 8:20)',
    swMode: 'Stops',
    intro: {
      "kicker": "A spring route in Osaka, hand-walked by Toshi",
      "h1": "The Mint’s avenue of double cherries, open one week a year. The castle first, dinner in Tenma.",
      "lead": "This map is for the week or so in mid-April when the Japan Mint opens its cherry-blossom walk (9–15 April in 2026). You must book ahead and can enter only in your booked time slot, so there are two courses built around the slot. This one is for an afternoon slot (about 15:00): leave Umeda or Namba about 9:30 for Osaka Castle’s Nishinomaru Garden and the late cherries at Tamatsukuri-guchi, lunch at JO-TERRACE, then the Mint, the Okawa riverside and dinner in Tenma. With a morning slot, switch with the buttons above the list.",
      "favLabel": "The highlight",
      "favName": "The Japan Mint cherry walk",
      "favText": "331 trees of 140 varieties along 560 m (2026), each with its name board.",
      "favPhoto": [
        "mint",
        0
      ],
      "whoHead": "Before you go",
      "who": [
        "The Mint is by advance booking only; without a booking, or outside your slot, you can’t get in. Booking opened at 9:00 on 18 March in 2026 (please check for next spring)",
        "No food or drink inside, no parasols, selfie sticks or tripods, and bags are checked at the gate",
        "Nishinomaru Garden closes on Mondays, and the Mint week includes one",
        "The castle’s Somei-Yoshino bloom before the Mint’s double cherries; that week, head for the late cherries at Tamatsukuri-guchi",
        "From Kyoto, Keihan limited expresses run from Sanjo and Gion-Shijo to Temmabashi in about 50 minutes, ¥490",
        "Dates and hours as in 2026, trains as of December 2026. Please check for next spring"
      ],
      "dayHead": "One day, roughly like this (afternoon slot)",
      "from": "From",
      "day": [
        {
          "time": "10:00",
          "area": "Temmabashi → Osaka Castle",
          "title": "Nishinomaru Garden and the tower",
          "text": "Five minutes by subway from Umeda. See the river from the bridge, then the castle lawn with the tower above the blossom.",
          "note": "Higashi-Umeda 9:35 (weekends 9:30)",
          "photo": [
            "nishinomaru",
            0
          ]
        },
        {
          "time": "12:30",
          "area": "Osaka Castle",
          "title": "Late cherries and lunch at JO-TERRACE",
          "text": "Double cherries at Tamatsukuri-guchi, then lunch by Osakajokoen Station: takoyaki, tonkatsu, set meals, cafés.",
          "photo": [
            "nishinomaru",
            3
          ]
        },
        {
          "time": "15:00",
          "area": "Japan Mint",
          "title": "The cherry walk",
          "text": "560 m one way from the south gate to the north gate. Be at the south gate for your slot.",
          "photo": [
            "mint",
            1
          ]
        },
        {
          "time": "16:00",
          "area": "Okawa → Tenma",
          "title": "Riverside blossom, dinner in Tenma",
          "text": "Over Sakuranomiya bridge to the east-bank path, then dinner around Tenjinbashi-suji and Tenma Station until 21:00 or 22:00.",
          "note": "To Kyoto: JR Tenma 21:03 (weekends 21:11)",
          "photo": [
            "kema",
            0
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and fees",
      "dealsLead": "The subway from Umeda or Namba to Temmabashi is ¥190–240; the rest is on foot. The Mint is free (booking required), and so is the riverside park.",
      "deals": [
        {
          "name": "Japan Mint cherry walk",
          "price": "Free, booking required",
          "best": "Book first",
          "text": "In 2026 you chose an entry slot online, first come first served, from 9:00 on 18 March. Next spring’s dates and method are usually announced on the Mint’s website in March (please check).",
          "url": "https://www.mint.go.jp/enjoy/toorinuke/sakura_osaka_news_r8.html"
        },
        {
          "name": "Nishinomaru Garden",
          "price": "¥300",
          "text": "Adult fee from April 2026; ¥350 in the evening-opening season (late March – early April). Closed Mondays.",
          "url": "https://www.osakacastlepark.jp/articles/detail.html?id=72"
        },
        {
          "name": "Osaka Castle tower",
          "price": "¥1,200",
          "text": "9:00–18:00 (last entry 17:30).",
          "url": "https://osaka-info.jp/en/spot/osaka-castle-main-keep/"
        },
        {
          "name": "Subway (Higashi-Umeda → Temmabashi)",
          "price": "¥190",
          "text": "Tanimachi Line, 4–5 minutes. From Namba, change at Tanimachi 9-chome, ¥240.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Keihan (Sanjo → Temmabashi)",
          "price": "¥490",
          "text": "For guests from Kyoto: about 50 minutes by limited express, no change.",
          "url": "https://transit.yahoo.co.jp/"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on 23 Nov 2026. The Mint’s dates and booking are as in 2026; please check for next spring.",
      "dealsMore": "See the source",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Book the Mint first",
          "text": "You can enter the walk only in the slot you booked. Use the buttons above the list to pick the course for your slot (afternoon or first of the day)."
        },
        {
          "title": "Follow the numbers",
          "text": "Go in number order. The last spot carries on into the evening, with the last trains home."
        },
        {
          "title": "Tap a number",
          "text": "Tap a number on the map or open the list to see photos, notes, fees and suggested times."
        },
        {
          "title": "Directions in Google Maps",
          "text": "Each spot has an “Open in Google Maps” link for directions."
        }
      ],
      "cta": "View the map",
      "footer1": "An original map, walked and made by Toshi (photos from April 2025 and April 2026)."
    },
    introFor: {
      "early": {
        "h1": "The first slot of the day at the Mint, the river to the castle, Dotonbori at night.",
        "lead": "This map is for the week or so in mid-April when the Japan Mint opens its cherry-blossom walk (9–15 April in 2026). This course is for the first slot of the day (10:00 on weekdays and 9:00 at weekends in 2026): after the Mint, walk the Okawa riverside to Osaka Castle, lunch at JO-TERRACE, see the late cherries at Tamatsukuri-guchi, the tower and Nishinomaru Garden, stroll Nakanoshima in the late afternoon and spend the evening in Dotonbori. With an afternoon slot, switch with the buttons above the list.",
        "dayHead": "One day, roughly like this (first slot)",
        "day": [
          {
            "time": "10:00",
            "area": "Japan Mint",
            "title": "The cherry walk in the first slot",
            "text": "About 15 minutes’ walk from Temmabashi to the south gate. At weekends the first slot is 9:00, an hour earlier.",
            "note": "Higashi-Umeda 9:17 (weekends 8:25)",
            "photo": [
              "mint",
              0
            ]
          },
          {
            "time": "11:00",
            "area": "Okawa → Osaka Castle",
            "title": "Along the riverside, then lunch",
            "text": "Over Sakuranomiya bridge and downstream on the east bank, then lunch at JO-TERRACE by Osakajokoen Station.",
            "photo": [
              "kema",
              0
            ]
          },
          {
            "time": "13:10",
            "area": "Osaka Castle",
            "title": "Late cherries, the tower, Nishinomaru Garden",
            "text": "The double cherries at Tamatsukuri-guchi, then the tower. The garden’s last entry is 16:30; closed Mondays.",
            "photo": [
              "nishinomaru",
              0
            ]
          },
          {
            "time": "16:15",
            "area": "Nakanoshima → Dotonbori",
            "title": "Nakanoshima on foot, Dotonbori at night",
            "text": "West through Nakanoshima Park from Temmabashi, then the subway from Yodoyabashi to Namba. For dinner see the Osaka map; stay until 21:00 or 22:00.",
            "note": "To Kyoto: Namba 21:39 (weekends 21:48)",
            "photo": [
              "temmabashi",
              1
            ]
          }
        ]
      }
    }
  }
};
