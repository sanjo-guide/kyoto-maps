/* Page texts in Japanese and English.
   Toshi 個人のマップ。三条から阪急で京都の西山へ。鈴虫寺の説法の回に合わせて、地蔵院・浄住寺・苔乃茶屋・松尾大社を歩く。
   コースは2つ（最初の説法へ／9〜10時に出発）。intro は「9〜10時に出発」の内容で、introFor.early が app.js で上書きされる。
   浄住寺の公開が終わった日（scripts/sync_nishiyama.py の OFF_FROM）からは、introFor.lateOff / earlyOff がさらに上書きする。
   午後の嵐山・桂離宮と夜は、最後のスポットの文章で案内。
   Photos are [spot id, photo index] from data/routes/nishiyama.json（コースで番号が変わるので id で指定）。
   時刻・料金は2026年11月22日に確認（各寺社・施設の公式サイト、京都観光Navi、京都バスの時刻表、乗換案内）。 */
window.NISHIYAMA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 西山 Nishiyama MAP',
    titleMain: '京都 西山',
    titleSub: 'Nishiyama, Kyoto',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: "上のボタンで出発時間を選ぶと、回る順番と時間が変わります。どちらも最後は松尾大社で、午後は電車1駅の嵐山へ続けられます。点線は順番を示す線で、実際の道ではありません。",
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
    train: "電車・バス",
    closed: '休み',
    cash: '現金を用意してください',
    checked: "{d}に公式サイトや時刻表・乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。",
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
    swCourse: "出発時間",
    courseAria: "出発時間",
    courseEarly: "最初の説法へ\n河原町 8:00ごろ発",
    courseLate: "9〜10時に出発\n鈴虫寺は午後",
    swMode: "回り方",
    intro: {
      "kicker": "Toshiが歩いて作った京都のルート",
      "h1": "午前は竹と苔のお寺、午後は鈴虫の説法。夕方は、となり町の嵐山へ。",
      "lead": "嵐山の南の山すそを歩く1日です。9〜10時に三条のあたりを出て、上桂から浄住寺（12月13日まで）と地蔵院へ。苔寺の門前で早めのお昼にして、鈴虫寺は13:10の説法に入ります。お寺の混雑予想には、混む日も午後は空く場合があると書かれています。松尾大社のあとは電車で1駅の嵐山、夜は三条・先斗町へ。朝早く出られる人は、一覧の上のボタンで最初の説法に入るコースに切り替えてください。",
      "favLabel": "いちばんの見どころ",
      "favName": "地蔵院（竹の寺）",
      "favText": "竹林の参道と苔の庭。写真のハートの窓が見られるのは12月14日から。",
      "favPhoto": [
        "jizoin",
        0
      ],
      "whoHead": "行く前に知っておくこと",
      "who": [
        "京都河原町から阪急で20分ほど（桂で乗り換え。上桂200円、松尾大社240円）",
        "鈴虫寺の説法は9:00〜16:20の10回。予約なし、混むと1時間ほど待つことも。入門は16:30まで",
        "浄住寺の秋の特別拝観は12月13日まで（9:30〜16:30、受付16:00まで）",
        "地蔵院は12月13日まで毎日開いていますが、その間はハートの窓が見られません",
        "苔寺（西芳寺）は申し込んだ人だけ。オンラインは前日まで、往復はがきは1か月前まで",
        "現金を持って。苔乃茶屋の営業時間と、お寺の支払い方法は要確認",
        "お寺は石段があります。1日に歩くのは、嵐山まで入れて2時間ほど"
      ],
      "dayHead": "1日の流れ（9〜10時に出発）",
      "from": "",
      "day": [
        {
          "time": "9:55",
          "area": "山田",
          "title": "浄住寺と地蔵院",
          "text": "京都河原町9:18発の阪急で上桂へ。特別公開の浄住寺から、竹林の地蔵院へ歩きます。",
          "note": "土日祝は9:15発",
          "photo": [
            "jizoin",
            2
          ]
        },
        {
          "time": "11:40",
          "area": "苔寺の門前",
          "title": "早めのお昼",
          "text": "苔乃茶屋でとろろそばか、にしんそば。営業時間は要確認です。",
          "photo": [
            "kokenochaya",
            0
          ]
        },
        {
          "time": "12:40",
          "area": "松室",
          "title": "鈴虫寺、13:10の説法",
          "text": "30分前に受付へ。説法のあと、京都の町を見下ろす庭を回ります。",
          "photo": [
            "suzumushi",
            0
          ]
        },
        {
          "time": "14:20",
          "area": "松尾",
          "title": "お酒の神様と石の庭",
          "text": "松尾大社の庭園（16:00まで）と酒樽の壁。",
          "photo": [
            "matsuo",
            3
          ]
        },
        {
          "time": "15:17",
          "area": "嵐山",
          "title": "天龍寺と竹林、夕方の渡月橋",
          "text": "阪急で1駅。天龍寺の受付は16:50まで。詳しくは嵐山のマップへ。",
          "note": "15:19着・170円",
          "photo": [
            "matsuo",
            0
          ]
        },
        {
          "time": "18:00",
          "area": "帰り → 三条",
          "title": "夜は先斗町・木屋町で",
          "text": "京都河原町から歩いてすぐ。晩ごはんのあと鴨川ぞいを三条へ、21〜22時ごろまで。12月6日までは嵐山で宝厳院の夜の紅葉を見てから戻っても。",
          "note": "嵐山17:33発（土日祝17:27発）",
          "photo": [
            "matsuo",
            4
          ]
        }
      ],
      "timeSuffix": "〜",
      "dealsHead": "交通費と拝観料のめやす",
      "dealsLead": "電車は区間ごとの運賃、拝観料は場所ごとの料金です。天龍寺（500円）など、午後の寄り道は別です。",
      "deals": [
        {
          "name": "阪急",
          "price": "170〜240円",
          "text": "京都河原町→上桂200円、→松尾大社240円。松尾大社→嵐山170円、嵐山→京都河原町240円。交通系ICカードが使えます。",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "鈴虫寺",
          "price": "500円",
          "text": "お茶とお菓子つき。説法は30分ほど、9:00から16:20まで10回。",
          "url": "https://suzutera.or.jp/guide/"
        },
        {
          "name": "地蔵院",
          "price": "1,000円",
          "text": "12月13日まではだれでも1,000円。そのあと、日本に住んでいる人は当面500円。",
          "url": "https://www.takenotera-jizoin.jp/access/"
        },
        {
          "name": "浄住寺 秋の特別拝観",
          "price": "1,000円",
          "text": "12月13日まで、9:30〜16:30（受付16:00まで）。",
          "url": "https://jojuji.org/admission.html"
        },
        {
          "name": "松尾大社の庭園",
          "price": "500円",
          "text": "神像館と共通。16:00まで（日曜・祝日16:30）。",
          "url": "https://www.matsunoo.or.jp/guide03"
        }
      ],
      "dealsNote": "大人の運賃・料金です。2026年11月22日に確認しました（各寺社の公式サイト、京都観光Navi、京都バスの時刻表、乗換案内）。",
      "dealsMore": "確認したページを見る",
      "howHead": "このマップの使い方",
      "how": [
        {
          "title": "出発時間を選ぶ",
          "text": "一覧の上のボタンで「最初の説法へ」（京都河原町8:00ごろ発）と「9〜10時に出発」を切り替えます。順番と時間が変わります。"
        },
        {
          "title": "番号の順に",
          "text": "1から5の順に回ります。最後の松尾大社に、午後の続き、帰りの電車、夜の過ごし方を書いています。"
        },
        {
          "title": "行かない場所は外せます",
          "text": "「選んで回る」に切り替えると、行きたい場所だけを選べます。苔寺の申し込み方は苔乃茶屋のページにあります。"
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
      "early": {
        "h1": "鈴虫寺の最初の説法から、竹と苔のお寺へ。午後は嵐山か桂離宮。",
        "lead": "京都河原町を8時ごろに出て、鈴虫寺の9:00の説法に入ります。9:30に開くカフェでひと休みしてから、地蔵院と浄住寺（12月13日まで）へ。苔寺の門前でお昼、松尾大社の庭を見たら、午後は嵐山のモンキーパークと天龍寺、または申し込んでおいた桂離宮へ。夜は三条・先斗町に戻ります。",
        "dayHead": "1日の流れ（最初の説法へ）",
        "day": [
          {
            "time": "8:45",
            "area": "松室",
            "title": "鈴虫寺、最初の説法",
            "text": "京都河原町8:01発の阪急で松尾大社駅へ、歩いて15〜20分。9:00の回に入ります。",
            "note": "土日祝は8:00発",
            "photo": [
              "suzumushi",
              0
            ]
          },
          {
            "time": "9:50",
            "area": "苔寺の門前",
            "title": "朝のひと休み",
            "text": "9:30に開く BAMBOO COFFEE で休憩。朝ごはんは出る前に。",
            "photo": [
              "suzumushi",
              2
            ]
          },
          {
            "time": "10:30",
            "area": "山田",
            "title": "地蔵院と浄住寺",
            "text": "竹林の参道と苔の庭、特別公開の浄住寺。",
            "photo": [
              "jizoin",
              2
            ]
          },
          {
            "time": "12:05",
            "area": "苔寺の門前",
            "title": "門前でお昼",
            "text": "苔乃茶屋でおそば。営業時間は要確認です。",
            "photo": [
              "kokenochaya",
              0
            ]
          },
          {
            "time": "13:10",
            "area": "松尾",
            "title": "お酒の神様と石の庭",
            "text": "松尾大社の庭園と酒樽の壁、亀の井。",
            "photo": [
              "matsuo",
              3
            ]
          },
          {
            "time": "14:05",
            "area": "嵐山か桂",
            "title": "モンキーパークと天龍寺、または桂離宮",
            "text": "嵐山へは電車で1駅。桂離宮の15:00の回は、3日前までにネットで申し込みを。",
            "note": "嵐山14:07着",
            "photo": [
              "matsuo",
              0
            ]
          },
          {
            "time": "18:00",
            "area": "帰り → 三条",
            "title": "夜は先斗町・木屋町で",
            "text": "京都河原町から歩いてすぐ。晩ごはんのあと鴨川ぞいを三条へ、21〜22時ごろまで。12月6日までは嵐山で宝厳院の夜の紅葉を見てから戻っても。",
            "note": "嵐山17:33発（土日祝17:27発）",
            "photo": [
              "matsuo",
              4
            ]
          }
        ]
      },
      "lateOff": {
        "lead": "嵐山の南の山すそを歩く1日です。浄住寺の秋の公開は終わったので、4か所を回ります。10時ごろ京都河原町を出て地蔵院へ、苔寺の門前で早めのお昼にして、鈴虫寺は13:10の説法に入ります。松尾大社のあとは電車で1駅の嵐山、夜は三条・先斗町へ。地蔵院は休みの日が多い時期なので、行く前に拝観カレンダーを見てください。",
        "favText": "竹林の参道と苔の庭、ハートの形の窓（春と秋の寺宝特別拝観の間は見られません）。",
        "who": [
          "京都河原町から阪急で20分ほど（桂で乗り換え。上桂200円、松尾大社240円）",
          "鈴虫寺の説法は9:00〜16:20の10回。予約なし、混むと1時間ほど待つことも。入門は16:30まで",
          "浄住寺はいま拝観できません。次の特別公開は公式サイトで",
          "地蔵院は休みの日が多い時期があります（1〜2月、年末、ふだんの木・金）。拝観カレンダーを見てから",
          "苔寺（西芳寺）は申し込んだ人だけ。2027年1月12日〜2月26日は日々参拝が休み",
          "現金を持って。苔乃茶屋の営業時間と、お寺の支払い方法は要確認",
          "お寺は石段があります。1日に歩くのは、嵐山まで入れて2時間ほど"
        ],
        "day": [
          {
            "time": "10:40",
            "area": "山田",
            "title": "竹の寺・地蔵院",
            "text": "京都河原町9:58発の阪急で上桂へ。竹林の参道と苔の庭。休みの日が多い時期なので、拝観カレンダーを見てから。",
            "note": "土日祝は10:00発",
            "photo": [
              "jizoin",
              2
            ]
          },
          {
            "time": "11:40",
            "area": "苔寺の門前",
            "title": "早めのお昼",
            "text": "苔乃茶屋でとろろそばか、にしんそば。営業時間は要確認です。",
            "photo": [
              "kokenochaya",
              0
            ]
          },
          {
            "time": "12:40",
            "area": "松室",
            "title": "鈴虫寺、13:10の説法",
            "text": "30分前に受付へ。説法のあと、京都の町を見下ろす庭を回ります。",
            "photo": [
              "suzumushi",
              0
            ]
          },
          {
            "time": "14:20",
            "area": "松尾",
            "title": "お酒の神様と石の庭",
            "text": "松尾大社の庭園（16:00まで）と酒樽の壁。",
            "photo": [
              "matsuo",
              3
            ]
          },
          {
            "time": "15:17",
            "area": "嵐山",
            "title": "天龍寺と竹林、夕方の渡月橋",
            "text": "阪急で1駅。天龍寺の受付は16:50まで。詳しくは嵐山のマップへ。",
            "note": "15:19着・170円",
            "photo": [
              "matsuo",
              0
            ]
          },
          {
            "time": "18:00",
            "area": "帰り → 三条",
            "title": "夜は先斗町・木屋町で",
            "text": "京都河原町から歩いてすぐ。晩ごはんのあと鴨川ぞいを三条へ、21〜22時ごろまで。",
            "note": "嵐山17:33発（土日祝17:27発）",
            "photo": [
              "matsuo",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "阪急",
            "price": "170〜240円",
            "text": "京都河原町→上桂200円、→松尾大社240円。松尾大社→嵐山170円、嵐山→京都河原町240円。交通系ICカードが使えます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "鈴虫寺",
            "price": "500円",
            "text": "お茶とお菓子つき。説法は30分ほど、9:00から16:20まで10回。",
            "url": "https://suzutera.or.jp/guide/"
          },
          {
            "name": "地蔵院",
            "price": "1,000円",
            "text": "日本に住んでいる人は当面500円。春と秋の寺宝特別拝観の間は、だれでも1,000円。",
            "url": "https://www.takenotera-jizoin.jp/access/"
          },
          {
            "name": "松尾大社の庭園",
            "price": "500円",
            "text": "神像館と共通。16:00まで（日曜・祝日16:30）。",
            "url": "https://www.matsunoo.or.jp/guide03"
          }
        ]
      },
      "earlyOff": {
        "lead": "京都河原町を8時ごろに出て、鈴虫寺の9:00の説法に入ります。カフェでひと休みしてから地蔵院へ（浄住寺の秋の公開は終わりました）。苔寺の門前でお昼、松尾大社の庭を見たら、午後は嵐山か、申し込んでおいた桂離宮へ。夜は三条・先斗町に戻ります。地蔵院は行く前に拝観カレンダーを見てください。",
        "favText": "竹林の参道と苔の庭、ハートの形の窓（春と秋の寺宝特別拝観の間は見られません）。",
        "who": [
          "京都河原町から阪急で20分ほど（桂で乗り換え。上桂200円、松尾大社240円）",
          "鈴虫寺の説法は9:00〜16:20の10回。予約なし、混むと1時間ほど待つことも。入門は16:30まで",
          "浄住寺はいま拝観できません。次の特別公開は公式サイトで",
          "地蔵院は休みの日が多い時期があります（1〜2月、年末、ふだんの木・金）。拝観カレンダーを見てから",
          "苔寺（西芳寺）は申し込んだ人だけ。2027年1月12日〜2月26日は日々参拝が休み",
          "現金を持って。苔乃茶屋の営業時間と、お寺の支払い方法は要確認",
          "お寺は石段があります。1日に歩くのは、嵐山まで入れて2時間ほど"
        ],
        "day": [
          {
            "time": "8:45",
            "area": "松室",
            "title": "鈴虫寺、最初の説法",
            "text": "京都河原町8:01発の阪急で松尾大社駅へ、歩いて15〜20分。9:00の回に入ります。",
            "note": "土日祝は8:00発",
            "photo": [
              "suzumushi",
              0
            ]
          },
          {
            "time": "9:50",
            "area": "苔寺の門前",
            "title": "朝のひと休み",
            "text": "9:30に開く BAMBOO COFFEE で休憩。朝ごはんは出る前に。",
            "photo": [
              "suzumushi",
              2
            ]
          },
          {
            "time": "10:30",
            "area": "山田",
            "title": "竹の寺・地蔵院",
            "text": "竹林の参道と苔の庭。休みの日が多い時期なので、拝観カレンダーを見てから。",
            "photo": [
              "jizoin",
              2
            ]
          },
          {
            "time": "11:30",
            "area": "苔寺の門前",
            "title": "門前でお昼",
            "text": "苔乃茶屋でおそば。営業時間は要確認です。",
            "photo": [
              "kokenochaya",
              0
            ]
          },
          {
            "time": "12:30",
            "area": "松尾",
            "title": "お酒の神様と石の庭",
            "text": "松尾大社の庭園と酒樽の壁、亀の井。",
            "photo": [
              "matsuo",
              3
            ]
          },
          {
            "time": "14:05",
            "area": "嵐山か桂",
            "title": "モンキーパークと天龍寺、または桂離宮",
            "text": "嵐山へは電車で1駅。桂離宮の15:00の回は、3日前までにネットで申し込みを。",
            "note": "嵐山14:07着",
            "photo": [
              "matsuo",
              0
            ]
          },
          {
            "time": "18:00",
            "area": "帰り → 三条",
            "title": "夜は先斗町・木屋町で",
            "text": "京都河原町から歩いてすぐ。晩ごはんのあと鴨川ぞいを三条へ、21〜22時ごろまで。",
            "note": "嵐山17:33発（土日祝17:27発）",
            "photo": [
              "matsuo",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "阪急",
            "price": "170〜240円",
            "text": "京都河原町→上桂200円、→松尾大社240円。松尾大社→嵐山170円、嵐山→京都河原町240円。交通系ICカードが使えます。",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "鈴虫寺",
            "price": "500円",
            "text": "お茶とお菓子つき。説法は30分ほど、9:00から16:20まで10回。",
            "url": "https://suzutera.or.jp/guide/"
          },
          {
            "name": "地蔵院",
            "price": "1,000円",
            "text": "日本に住んでいる人は当面500円。春と秋の寺宝特別拝観の間は、だれでも1,000円。",
            "url": "https://www.takenotera-jizoin.jp/access/"
          },
          {
            "name": "松尾大社の庭園",
            "price": "500円",
            "text": "神像館と共通。16:00まで（日曜・祝日16:30）。",
            "url": "https://www.matsunoo.or.jp/guide03"
          }
        ]
      }
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kyoto: Nishiyama MAP',
    titleMain: 'Nishiyama, Kyoto',
    titleSub: '京都 西山',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: "Choose your start time with the buttons above: the order and times change. Both courses end at Matsunoo Taisha, one train stop from Arashiyama for the afternoon. The dotted line shows the order, not the actual path.",
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
    train: "Train & bus",
    closed: 'Closed',
    cash: 'Bring cash',
    checked: "Checked on official websites, timetables and a route planner on {d}. Details can change, so please check before you go.",
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
    swCourse: "Start time",
    courseAria: "Start time",
    courseEarly: "First talk at 9:00\nLeave about 8:00",
    courseLate: "Leave at 9–10\nTalk after lunch",
    swMode: "Stops",
    intro: {
      "kicker": "A Kyoto route, hand-walked by Toshi",
      "h1": "Bamboo and moss in the morning, a talk among crickets after lunch, Arashiyama by dusk.",
      "lead": "A day along the hills south of Arashiyama. Leave the Sanjo area at 9–10 for Jojuji (until 13 December) and Jizoin from Kami-Katsura, have an early lunch by the Moss Temple and join Suzumushi-dera’s 13:10 talk: the temple’s forecast says even busy days can be quieter after noon. After Matsunoo Taisha, Arashiyama is one train stop away; spend the evening back in Pontocho. If you can start early, switch to the first-talk course with the buttons above the list.",
      "favLabel": "Highlight",
      "favName": "Jizoin (the Bamboo Temple)",
      "favText": "A bamboo approach and a moss garden. The heart window in the photo can be seen from 14 December.",
      "favPhoto": [
        "jizoin",
        0
      ],
      "whoHead": "Good to know before you go",
      "who": [
        "About 20 min by Hankyu from Kyoto-Kawaramachi, changing at Katsura (¥200 to Kami-Katsura, ¥240 to Matsuo-taisha)",
        "Suzumushi-dera has ten talks, 9:00–16:20. No booking; you may wait about an hour. Last entry 16:30",
        "Jojuji’s autumn opening ends on 13 December (9:30–16:30, last entry 16:00)",
        "Jizoin is open daily until 13 December, but its heart window can’t be seen until then",
        "The Moss Temple needs an application: online by the day before, by postcard a month ahead",
        "Bring cash. The teahouse’s hours and the temples’ payment methods need checking",
        "The temples have stone steps. Expect about two hours of walking in all, Arashiyama included"
      ],
      "dayHead": "One day, roughly like this (leaving at 9–10)",
      "from": "From",
      "day": [
        {
          "time": "9:55",
          "area": "Yamada",
          "title": "Jojuji and Jizoin",
          "text": "Hankyu from Kyoto-Kawaramachi at 9:18 to Kami-Katsura: Jojuji’s special opening, then bamboo-lined Jizoin.",
          "note": "Weekends and holidays: 9:15",
          "photo": [
            "jizoin",
            2
          ]
        },
        {
          "time": "11:40",
          "area": "Moss Temple area",
          "title": "An early lunch",
          "text": "Soba with grated yam or herring at Koke-no-chaya. Its hours need checking.",
          "photo": [
            "kokenochaya",
            0
          ]
        },
        {
          "time": "12:40",
          "area": "Matsumuro",
          "title": "Suzumushi-dera, the 13:10 talk",
          "text": "At reception 30 minutes ahead; afterwards, the garden looking over Kyoto.",
          "photo": [
            "suzumushi",
            0
          ]
        },
        {
          "time": "14:20",
          "area": "Matsuo",
          "title": "The god of sake and stone gardens",
          "text": "Matsunoo Taisha’s gardens (until 16:00) and wall of sake barrels.",
          "photo": [
            "matsuo",
            3
          ]
        },
        {
          "time": "15:17",
          "area": "Arashiyama",
          "title": "Tenryu-ji, bamboo, the bridge at dusk",
          "text": "One stop by train. Tenryu-ji’s last entry is 16:50. See the Arashiyama map for more.",
          "note": "15:19, ¥170",
          "photo": [
            "matsuo",
            0
          ]
        },
        {
          "time": "18:00",
          "area": "Back → Sanjo",
          "title": "Evening in Pontocho and Kiyamachi",
          "text": "A short walk from Kyoto-Kawaramachi. Dinner, then along the Kamo river to Sanjo until 21:00 or 22:00. Until 6 December you could see Hogon-in’s lit-up maples in Arashiyama first.",
          "note": "Arashiyama 17:33 (weekends 17:27)",
          "photo": [
            "matsuo",
            4
          ]
        }
      ],
      "timeSuffix": "",
      "dealsHead": "Fares and entry fees",
      "dealsLead": "Train fares are per section and entry fees per place. Afternoon extras such as Tenryu-ji (¥500) are separate.",
      "deals": [
        {
          "name": "Hankyu",
          "price": "¥170–240",
          "text": "Kyoto-Kawaramachi to Kami-Katsura ¥200, to Matsuo-taisha ¥240; Matsuo-taisha to Arashiyama ¥170; Arashiyama back ¥240. IC cards work.",
          "url": "https://transit.yahoo.co.jp/"
        },
        {
          "name": "Suzumushi-dera",
          "price": "¥500",
          "text": "Tea and a sweet included. Talks of about 30 minutes, ten a day from 9:00 to 16:20.",
          "url": "https://suzutera.or.jp/guide/"
        },
        {
          "name": "Jizoin",
          "price": "¥1,000",
          "text": "¥1,000 for everyone until 13 December; afterwards residents of Japan pay ¥500 for now.",
          "url": "https://www.takenotera-jizoin.jp/access/"
        },
        {
          "name": "Jojuji autumn opening",
          "price": "¥1,000",
          "text": "Until 13 December, 9:30–16:30 (last entry 16:00).",
          "url": "https://jojuji.org/admission.html"
        },
        {
          "name": "Matsunoo’s gardens",
          "price": "¥500",
          "text": "Includes the statue hall. Until 16:00 (16:30 on Sundays and holidays).",
          "url": "https://www.matsunoo.or.jp/guide03"
        }
      ],
      "dealsNote": "Adult fares and fees, checked on Nov 22, 2026 (official websites, Kyoto Kanko Navi, Kyoto Bus timetables, a route planner).",
      "dealsMore": "See the source",
      "howHead": "How to use this map",
      "how": [
        {
          "title": "Pick a start time",
          "text": "The buttons above the list switch between “First talk at 9:00” (leave about 8:00) and “Leave at 9–10”. The order and times change."
        },
        {
          "title": "In number order",
          "text": "Go from 1 to 5. The last stop, Matsunoo Taisha, covers the afternoon, trains back and the evening."
        },
        {
          "title": "Skip what you like",
          "text": "Switch to “Choose stops” to pick only the places you want. How to apply for the Moss Temple is on the Koke-no-chaya page."
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
      "early": {
        "h1": "The first talk among crickets, then bamboo and moss. Arashiyama or Katsura villa after lunch.",
        "lead": "Leave Kyoto-Kawaramachi around 8:00 for Suzumushi-dera’s 9:00 talk. Rest at a café that opens at 9:30, then walk to Jizoin and Jojuji (until 13 December). After lunch by the Moss Temple and Matsunoo’s gardens, go on to Arashiyama’s Monkey Park and Tenryu-ji, or to Katsura Imperial Villa if you applied. The evening is back in Pontocho.",
        "dayHead": "One day, roughly like this (first talk)",
        "day": [
          {
            "time": "8:45",
            "area": "Matsumuro",
            "title": "Suzumushi-dera, the first talk",
            "text": "Hankyu from Kyoto-Kawaramachi at 8:01 to Matsuo-taisha, then 15–20 minutes on foot, for the 9:00 talk.",
            "note": "Weekends and holidays: 8:00",
            "photo": [
              "suzumushi",
              0
            ]
          },
          {
            "time": "9:50",
            "area": "Moss Temple area",
            "title": "A morning rest",
            "text": "BAMBOO COFFEE opens at 9:30. Have breakfast before you set out.",
            "photo": [
              "suzumushi",
              2
            ]
          },
          {
            "time": "10:30",
            "area": "Yamada",
            "title": "Jizoin and Jojuji",
            "text": "Bamboo, a moss garden and Jojuji’s special opening.",
            "photo": [
              "jizoin",
              2
            ]
          },
          {
            "time": "12:05",
            "area": "Moss Temple area",
            "title": "Lunch by the temple",
            "text": "Soba at Koke-no-chaya. Its hours need checking.",
            "photo": [
              "kokenochaya",
              0
            ]
          },
          {
            "time": "13:10",
            "area": "Matsuo",
            "title": "The god of sake and stone gardens",
            "text": "Matsunoo Taisha’s gardens, barrels and spring.",
            "photo": [
              "matsuo",
              3
            ]
          },
          {
            "time": "14:05",
            "area": "Arashiyama or Katsura",
            "title": "Monkeys and Tenryu-ji, or Katsura villa",
            "text": "One stop to Arashiyama. For the villa’s 15:00 tour, apply online at least three days ahead.",
            "note": "Arashiyama 14:07",
            "photo": [
              "matsuo",
              0
            ]
          },
          {
            "time": "18:00",
            "area": "Back → Sanjo",
            "title": "Evening in Pontocho and Kiyamachi",
            "text": "A short walk from Kyoto-Kawaramachi. Dinner, then along the Kamo river to Sanjo until 21:00 or 22:00. Until 6 December you could see Hogon-in’s lit-up maples in Arashiyama first.",
            "note": "Arashiyama 17:33 (weekends 17:27)",
            "photo": [
              "matsuo",
              4
            ]
          }
        ]
      },
      "lateOff": {
        "lead": "A day along the hills south of Arashiyama, with four stops now that Jojuji’s autumn opening is over. Leave Kyoto-Kawaramachi about 10:00 for Jizoin, have an early lunch by the Moss Temple and join Suzumushi-dera’s 13:10 talk. After Matsunoo Taisha, Arashiyama is one stop away; spend the evening back in Pontocho. Jizoin often closes in this season, so check its calendar first.",
        "favText": "A bamboo approach, a moss garden and a heart-shaped window (hidden during the spring and autumn treasure displays).",
        "who": [
          "About 20 min by Hankyu from Kyoto-Kawaramachi, changing at Katsura (¥200 to Kami-Katsura, ¥240 to Matsuo-taisha)",
          "Suzumushi-dera has ten talks, 9:00–16:20. No booking; you may wait about an hour. Last entry 16:30",
          "Jojuji is closed now; check its website for the next special opening",
          "Jizoin often closes in winter (January–February, year end) and usually on Thursdays and Fridays: check its calendar",
          "The Moss Temple needs an application, and has no regular visits 12 January – 26 February 2027",
          "Bring cash. The teahouse’s hours and the temples’ payment methods need checking",
          "The temples have stone steps. Expect about two hours of walking in all, Arashiyama included"
        ],
        "day": [
          {
            "time": "10:40",
            "area": "Yamada",
            "title": "Jizoin, the Bamboo Temple",
            "text": "Hankyu from Kyoto-Kawaramachi at 9:58 to Kami-Katsura. Bamboo and a moss garden; it often closes in this season, so check the calendar.",
            "note": "Weekends and holidays: 10:00",
            "photo": [
              "jizoin",
              2
            ]
          },
          {
            "time": "11:40",
            "area": "Moss Temple area",
            "title": "An early lunch",
            "text": "Soba with grated yam or herring at Koke-no-chaya. Its hours need checking.",
            "photo": [
              "kokenochaya",
              0
            ]
          },
          {
            "time": "12:40",
            "area": "Matsumuro",
            "title": "Suzumushi-dera, the 13:10 talk",
            "text": "At reception 30 minutes ahead; afterwards, the garden looking over Kyoto.",
            "photo": [
              "suzumushi",
              0
            ]
          },
          {
            "time": "14:20",
            "area": "Matsuo",
            "title": "The god of sake and stone gardens",
            "text": "Matsunoo Taisha’s gardens (until 16:00) and wall of sake barrels.",
            "photo": [
              "matsuo",
              3
            ]
          },
          {
            "time": "15:17",
            "area": "Arashiyama",
            "title": "Tenryu-ji, bamboo, the bridge at dusk",
            "text": "One stop by train. Tenryu-ji’s last entry is 16:50. See the Arashiyama map for more.",
            "note": "15:19, ¥170",
            "photo": [
              "matsuo",
              0
            ]
          },
          {
            "time": "18:00",
            "area": "Back → Sanjo",
            "title": "Evening in Pontocho and Kiyamachi",
            "text": "A short walk from Kyoto-Kawaramachi. Dinner, then along the Kamo river to Sanjo until 21:00 or 22:00.",
            "note": "Arashiyama 17:33 (weekends 17:27)",
            "photo": [
              "matsuo",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "Hankyu",
            "price": "¥170–240",
            "text": "Kyoto-Kawaramachi to Kami-Katsura ¥200, to Matsuo-taisha ¥240; Matsuo-taisha to Arashiyama ¥170; Arashiyama back ¥240. IC cards work.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Suzumushi-dera",
            "price": "¥500",
            "text": "Tea and a sweet included. Talks of about 30 minutes, ten a day from 9:00 to 16:20.",
            "url": "https://suzutera.or.jp/guide/"
          },
          {
            "name": "Jizoin",
            "price": "¥1,000",
            "text": "Residents of Japan pay ¥500 for now; ¥1,000 for everyone during the spring and autumn treasure displays.",
            "url": "https://www.takenotera-jizoin.jp/access/"
          },
          {
            "name": "Matsunoo’s gardens",
            "price": "¥500",
            "text": "Includes the statue hall. Until 16:00 (16:30 on Sundays and holidays).",
            "url": "https://www.matsunoo.or.jp/guide03"
          }
        ]
      },
      "earlyOff": {
        "lead": "Leave Kyoto-Kawaramachi around 8:00 for Suzumushi-dera’s 9:00 talk, rest at a café, then walk to Jizoin (Jojuji’s autumn opening is over). After lunch by the Moss Temple and Matsunoo’s gardens, go on to Arashiyama, or to Katsura Imperial Villa if you applied. The evening is back in Pontocho. Check Jizoin’s calendar before you go.",
        "favText": "A bamboo approach, a moss garden and a heart-shaped window (hidden during the spring and autumn treasure displays).",
        "who": [
          "About 20 min by Hankyu from Kyoto-Kawaramachi, changing at Katsura (¥200 to Kami-Katsura, ¥240 to Matsuo-taisha)",
          "Suzumushi-dera has ten talks, 9:00–16:20. No booking; you may wait about an hour. Last entry 16:30",
          "Jojuji is closed now; check its website for the next special opening",
          "Jizoin often closes in winter (January–February, year end) and usually on Thursdays and Fridays: check its calendar",
          "The Moss Temple needs an application, and has no regular visits 12 January – 26 February 2027",
          "Bring cash. The teahouse’s hours and the temples’ payment methods need checking",
          "The temples have stone steps. Expect about two hours of walking in all, Arashiyama included"
        ],
        "day": [
          {
            "time": "8:45",
            "area": "Matsumuro",
            "title": "Suzumushi-dera, the first talk",
            "text": "Hankyu from Kyoto-Kawaramachi at 8:01 to Matsuo-taisha, then 15–20 minutes on foot, for the 9:00 talk.",
            "note": "Weekends and holidays: 8:00",
            "photo": [
              "suzumushi",
              0
            ]
          },
          {
            "time": "9:50",
            "area": "Moss Temple area",
            "title": "A morning rest",
            "text": "BAMBOO COFFEE opens at 9:30. Have breakfast before you set out.",
            "photo": [
              "suzumushi",
              2
            ]
          },
          {
            "time": "10:30",
            "area": "Yamada",
            "title": "Jizoin, the Bamboo Temple",
            "text": "Bamboo and a moss garden. It often closes in this season, so check the calendar.",
            "photo": [
              "jizoin",
              2
            ]
          },
          {
            "time": "11:30",
            "area": "Moss Temple area",
            "title": "Lunch by the temple",
            "text": "Soba at Koke-no-chaya. Its hours need checking.",
            "photo": [
              "kokenochaya",
              0
            ]
          },
          {
            "time": "12:30",
            "area": "Matsuo",
            "title": "The god of sake and stone gardens",
            "text": "Matsunoo Taisha’s gardens, barrels and spring.",
            "photo": [
              "matsuo",
              3
            ]
          },
          {
            "time": "14:05",
            "area": "Arashiyama or Katsura",
            "title": "Monkeys and Tenryu-ji, or Katsura villa",
            "text": "One stop to Arashiyama. For the villa’s 15:00 tour, apply online at least three days ahead.",
            "note": "Arashiyama 14:07",
            "photo": [
              "matsuo",
              0
            ]
          },
          {
            "time": "18:00",
            "area": "Back → Sanjo",
            "title": "Evening in Pontocho and Kiyamachi",
            "text": "A short walk from Kyoto-Kawaramachi. Dinner, then along the Kamo river to Sanjo until 21:00 or 22:00.",
            "note": "Arashiyama 17:33 (weekends 17:27)",
            "photo": [
              "matsuo",
              4
            ]
          }
        ],
        "deals": [
          {
            "name": "Hankyu",
            "price": "¥170–240",
            "text": "Kyoto-Kawaramachi to Kami-Katsura ¥200, to Matsuo-taisha ¥240; Matsuo-taisha to Arashiyama ¥170; Arashiyama back ¥240. IC cards work.",
            "url": "https://transit.yahoo.co.jp/"
          },
          {
            "name": "Suzumushi-dera",
            "price": "¥500",
            "text": "Tea and a sweet included. Talks of about 30 minutes, ten a day from 9:00 to 16:20.",
            "url": "https://suzutera.or.jp/guide/"
          },
          {
            "name": "Jizoin",
            "price": "¥1,000",
            "text": "Residents of Japan pay ¥500 for now; ¥1,000 for everyone during the spring and autumn treasure displays.",
            "url": "https://www.takenotera-jizoin.jp/access/"
          },
          {
            "name": "Matsunoo’s gardens",
            "price": "¥500",
            "text": "Includes the statue hall. Until 16:00 (16:30 on Sundays and holidays).",
            "url": "https://www.matsunoo.or.jp/guide03"
          }
        ]
      }
    }
  }
};
