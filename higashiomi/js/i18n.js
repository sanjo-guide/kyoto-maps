/* Page texts in Japanese and English.
   Toshi 個人のマップ。京都駅から日帰りで湖東の紅葉へ（2026-11-22 オーナーの指示で、起点を三条から京都駅に変えた）。
   コースは2つ（一覧の上のボタン）：eigenji＝太郎坊宮・永源寺と教林坊のライトアップ（data/routes/higashiomi.json）、
   sanzan＝彦根からの紅葉シャトルバスで湖東三山（higashiomi-sanzan.json）。どちらも scripts/build_higashiomi_data.py が作る。
   intro はどちらのコースにも共通の項目で、コースで変わる項目は introFor[コース] が app.js で上書きされる（scripts/sync_higashiomi.py）。
   湖東三山は日付でも変わる：11/30から introFor.sanzanTaxi、12/7からはさらに introFor.sanzanWinter（教林坊なし）が上書きされ、
   コースのボタンの文字も courseSanzanTaxi になる（日付は scripts/sync_higashiomi.py の TAXI_FROM・WINTER_FROM）。
   太郎坊宮・永源寺は12/7から introFor.eigenjiWinter が上書きされる（教林坊なし、京都駅18:12着）。
   写真は [スポットの id, 写真の番号]（コースで番号が変わるため）。
   西明寺と金剛輪寺は Toshi がまだ行っていない場所（写真は Wikimedia Commons、情報は公式サイトと湖東三山のチラシ）。
   時刻・料金は2026年11月22日に確認（各寺社の公式サイト・湖東三山のチラシ・近江鉄道、電車とバスは乗換案内。出典はデータの sources）。 */
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
    listNote: '番号は回る順番です。最初は時間割どおりの場所が選んであります。点線は順番を示す線で、実際の道ではありません。',
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
    bus: 'バス',
    taxi: 'タクシー',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトや乗換案内で確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトで確認できなかった情報があります（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月22日',
    noticeHead: 'この時期の注意',
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
    swCourse: 'コース',
    courseAria: 'コース',
    courseEigenji: '太郎坊宮・永源寺\n（9〜10時に出発）',
    courseSanzan: '湖東三山\n（8時台に出発）',
    courseSanzanTaxi: '湖東三山の2寺\n（9時半ごろ出発）',
    swMode: '回り方',
    modeAria: '回り方',
    modeAll: '全部回る',
    modePick: '選んで回る',
    pickNote: '行きたい場所の「行きたい」を押してください。選んだ場所だけが点線でつながり、スタートの駅は自動で入ります。めやすの時間は、最初に選んである組み合わせで回る場合のものです。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（駅を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたいお寺や神社を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '自動',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    intro: {
      kicker: '秋のマップ｜紅葉の見ごろは例年11月中旬〜下旬',
      favLabel: 'いちばんの見どころ',
      whoHead: '出かける前に',
      dayHead: '1日の流れ（目安）',
      from: '',
      timeSuffix: '',
      dealsHead: '交通費のめやす',
      dealsMore: '公式サイトで見る',
      howHead: 'このマップの使い方',
      cta: '地図を見る',
      footer1: 'Toshiが実際に歩いて作った、オリジナルマップです。'
    },
    introFor: {
      eigenji: {
        h1: '742段の石段の先の紅葉から、竹林のライトアップまで。',
        lead: '京都駅を10:00の新快速で出て、近江鉄道で太郎坊宮へ。とがった山の中腹の神社から近江の平野を見下ろしたら、バスで愛知川の渓谷の永源寺へ。遅めのお昼のあと夕方までもみじの中で過ごし、最後は春と秋だけ公開される教林坊の夜の庭へ。京都駅に戻るのは20:12です。',
        favName: '永源寺',
        favText: '山門と法堂を包む一面のもみじ。',
        favPhoto: ['eigenji', 2],
        dayHead: '1日の流れ（京都駅 10:00発）',
        who: [
          '京都駅10:00発の新快速と近江鉄道で、太郎坊宮前に10:57（1,070円）。三条のあたりからは、地下鉄で京都駅まで約15分',
          '太郎坊宮は742段の石段。歩きやすい靴で',
          '太郎坊宮から永源寺へのバスに乗るまで、食べる店はほぼない。お昼は永源寺で14時ごろなので、朝ごはんはしっかり',
          '教林坊は安土駅からタクシーで約10分（2,500円前後）。行きも帰りも前もって予約を',
          '教林坊のライトアップは2026年は12月6日まで（受付19:00まで）',
          '近江鉄道は2026年3月から ICOCA などの交通系ICカードで乗れる',
          '湖東三山（西明寺・百済寺・金剛輪寺）は、上の「湖東三山」のコースで'
        ],
        day: [
          { time: '10:00', area: '京都駅 → 近江八幡', title: 'JRの新快速で近江八幡へ', text: '京都駅10:00発の新快速「近江塩津」行きで、乗り換えなし。近江八幡に10:35（土日祝10:34）。10:42の近江鉄道に乗り換えて、太郎坊宮前に10:57。', photo: ['omihachimaneki', 1] },
          { time: '11:15', area: '太郎坊宮', title: '石段を登って、勝運の神社へ', text: '742段の石段と夫婦岩を通って本殿へ。近江の平野が見渡せます。12:41か12:59の電車で八日市へ。', photo: ['taroubou', 5] },
          { time: '13:45', area: '永源寺', title: '遅めのお昼と、渓谷のもみじ', text: '八日市13:15のバスで永源寺へ。まずお昼、それから山門と法堂のもみじ。16:24（土日祝16:25）のバスで帰ります。', photo: ['eigenji', 0] },
          { time: '18:00', area: '安土 → 教林坊', title: '竹林と庭のライトアップ', text: '近江鉄道とJRで安土17:44、タクシーで教林坊へ。19:00ごろまで夜の庭を。', photo: ['kyorinbo', 0] },
          { time: '20:12', area: '京都駅', title: '京都に戻って晩ごはん', text: '安土19:28発、近江八幡で新快速に乗り換えて京都駅20:12。街なかで21〜22時まで（三条・木屋町・先斗町へは地下鉄で約15分）。近江八幡で晩ごはんにする手もあります。', photo: ['kyorinbo', 3] }
        ],
        dealsLead: '京都駅から回って京都駅へ帰ると、電車とバスは合わせて3,990円（京都駅→太郎坊宮前1,070円、太郎坊宮前→八日市160円、八日市→永源寺前のバス670円、永源寺前→八日市のバス670円と八日市→安土650円、安土→京都駅770円）。拝観料（永源寺600円・教林坊1,000円）と、教林坊へのタクシー代（片道2,500円前後）は別です。',
        deals: [
          { name: '京都駅 → 太郎坊宮前', price: '1,070円', text: 'JR680円＋近江鉄道390円。帰りは安土→京都駅770円。三条のあたりからは、地下鉄で京都駅まで260円（烏丸御池で乗り換え）。', url: 'https://transit.yahoo.co.jp/' },
          { name: '八日市駅 → 永源寺前（近江鉄道バス）', price: '670円', text: '八日市駅1番のりば13:15発。帰りは永源寺前16:24（土日祝16:25）発。', url: 'https://www.ohmitetudo.co.jp/bus/access/eigenji/' },
          { name: 'タクシー（安土駅 ↔ 教林坊）', price: '片道2,500円前後', text: '約10分。金額は教林坊の公式サイトの目安。行きと帰りの迎えを予約しておきましょう。', url: 'https://kyourinbo.jimdofree.com/' }
        ],
        dealsNote: '大人の運賃・料金です。2026年11月22日に、近江鉄道バスの時刻表・教林坊と永源寺の公式サイト、電車は乗換案内で確認しました。',
        how: [
          { title: 'コースを選ぶ', text: '一覧の上のボタンで「太郎坊宮・永源寺」か「湖東三山」を選びます。コースによって、時間割と番号が変わります。' },
          { title: '行きたい場所を入れ替える', text: '最初は時間割どおりの3か所が選んであります。外した場所があると、帰り方などの一言が出ます。' },
          { title: '番号をタップ', text: '写真・説明・料金・電車とバスの時刻が見られます。入口で困ること（期間・タクシー・受付の時間）は、いちばん上の注意に。' },
          { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。' }
        ]
      },
      sanzan: {
        h1: '国宝の本堂を2つと、苔むした参道を、シャトルバスで。',
        lead: '湖東三山の西明寺・百済寺・金剛輪寺は、鈴鹿の山すそに離れて建っています。紅葉の時期（2026年は11月19日〜29日）だけ、彦根駅から3つのお寺を結ぶシャトルバスが出ます。京都駅を平日8:37・土日祝8:30の新快速で出て10:00のバスに乗り、西明寺の門前で近江牛のお昼、午後は百済寺、夕方は金剛輪寺。京都駅には18:42に戻ります。',
        favName: '西明寺',
        favText: '杉木立に並ぶ、国宝の本堂と三重塔。',
        favPhoto: ['saimyoji', 0],
        dayHead: 'シャトルバスの日の流れ（京都駅 8:37発、土日祝8:30発）',
        who: [
          '京都駅を平日8:37・土日祝8:30の新快速で出て、彦根駅10:00のシャトルバスへ（乗り換えなし・1,170円）。三条のあたりからは、地下鉄で京都駅まで約15分',
          'シャトルバスは路線バスの車両で座れないことも。もみじきっぷ（2,500円・現金）を買う人は、彦根駅発の便を予約できる',
          '西明寺の境内は持ち込みの飲食ができない。お昼は門前の千成亭ぎゅ〜じあむ（月・火は電話で確認）',
          '金剛輪寺は受付16:30まで。百済寺からのバスで15:43に着いたら、まっすぐ本堂へ',
          'シャトルバスのない日（11月30日から）は、京都駅9:34（土日祝9:37）発で河瀬へ。予約制の乗合タクシー（現金のみ）で西明寺と金剛輪寺の2つを回る。時刻は1番の駅の注意に',
          '西明寺と金剛輪寺の写真は Wikimedia Commons から（Toshi はまだ行っていません）'
        ],
        day: [
          { time: '8:37', area: '京都駅 → 彦根', title: 'JRの新快速で彦根へ', text: '京都駅8:37発で、乗り換えなしで彦根に9:31。土日祝は8:30発で9:20着。西口の4番のりばへ。', photo: ['hikoneeki', 0] },
          { time: '10:32', area: '西明寺', title: '国宝の本堂と三重塔、門前でお昼', text: '10:00のシャトルバスで西明寺へ。1時間ほどお参りして、門前で近江牛のお昼。12:32のバスで百済寺へ。', photo: ['saimyoji', 1] },
          { time: '13:10', area: '百済寺', title: '苔むした参道と天下遠望の庭', text: '仁王門をくぐって本堂へ。本坊の庭と遠望台から湖東の平野を。15:20のバスで金剛輪寺へ。', photo: ['hyakusaiji', 0] },
          { time: '15:43', area: '金剛輪寺', title: '千体地蔵の参道と血染めのもみじ', text: '受付は16:30まで。夕方の光の中の本堂と三重塔。16:43のバスで彦根駅へ。', photo: ['kongorinji', 0] },
          { time: '17:52', area: '彦根 → 京都駅', title: '新快速で京都へ、晩ごはん', text: '彦根17:52発で京都駅18:42（平日・土日祝とも）。街なかで21〜22時まで（三条・木屋町・先斗町へは地下鉄で約15分）。教林坊のライトアップに寄る手もあります。', photo: ['kongorinji', 2] }
        ],
        dealsLead: 'シャトルバスの日に京都駅から回って京都駅へ帰ると、電車とバスは合わせて4,640円（京都駅↔彦根1,170円×2、シャトルバス700＋500＋300＋800円）。もみじきっぷ（2,500円）にすると、3つのお寺の入山料が50円ずつ安くなり、彦根駅発のバスを予約できます。入山料は西明寺800円・百済寺600円・金剛輪寺800円。',
        deals: [
          { name: '京都駅 → 彦根', price: '1,170円', text: '新快速で乗り換えなし。帰りも1,170円。三条のあたりからは、地下鉄で京都駅まで260円（烏丸御池で乗り換え）。', url: 'https://transit.yahoo.co.jp/' },
          { name: '紅葉シャトルバス（2026年11月19日〜29日）', price: '1回200〜1,000円', text: '彦根駅→西明寺700円、西明寺→百済寺500円、百済寺→金剛輪寺300円、金剛輪寺→彦根駅800円。', url: 'https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/' },
          { name: 'もみじきっぷ（1日乗り放題）', price: '2,500円', text: '当日、彦根駅西口のバスのりばかバスの中で、現金で。こども1,250円。三山の入山料50円引き、クレフィール湖東の水、千成亭ぎゅ〜じあむのウーロン茶（食事をした人）。', url: 'https://kokokubus.rsvsys.jp/reservations/calendar?category=5' },
          { name: '乗合タクシー「愛のりタクシー」（シャトルバスのない日）', price: '1回400〜800円', text: '河瀬駅→西明寺800円、西明寺→金剛輪寺400円、金剛輪寺→稲枝駅800円。現金のみ。JRは京都駅→河瀬990円、稲枝→京都駅990円。12/29〜1/3は運休、乗る1時間前までに予約（近江タクシー彦根営業所 0749-22-1111）。', url: 'https://www.city.hikone.lg.jp/kurashi/kotsu_doro/3/6022.html' }
        ],
        dealsNote: '大人の運賃・料金です。2026年11月22日に、近江鉄道のシャトルバスの案内・湖東三山のチラシ・各寺の公式サイト・彦根市の愛のりタクシー時刻表、電車は乗換案内で確認しました。',
        how: [
          { title: 'コースを選ぶ', text: '一覧の上のボタンで「太郎坊宮・永源寺」か「湖東三山」を選びます。コースによって、時間割と番号が変わります。' },
          { title: '行きたい場所を入れ替える', text: '最初は三山が選んであります。教林坊を足すと、帰りに夜のライトアップへ寄る行き方が出ます。' },
          { title: '番号をタップ', text: '写真・説明・料金・シャトルバスの時刻が見られます。入口で困ること（現金だけ・予約・受付の時間）は、いちばん上の注意に。' },
          { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。' }
        ]
      },
      eigenjiWinter: {
        h1: '742段の石段の上の神社から、渓谷の禅寺へ。',
        lead: '京都駅を10:00の新快速で出て、近江鉄道で太郎坊宮へ。とがった山の中腹の神社から近江の平野を見下ろしたら、バスで愛知川の渓谷の永源寺へ。持ってきたお昼を食べて、拝観は閉まる16:00まで。京都駅に18:12に戻って、夜は街なかで。',
        favText: '渓谷に建つ禅寺の、大きな山門と法堂。',
        favPhoto: ['eigenji', 3],
        who: [
          '京都駅10:00発の新快速と近江鉄道で、太郎坊宮前に10:57（1,070円）。三条のあたりからは、地下鉄で京都駅まで約15分',
          '太郎坊宮は742段の石段。歩きやすい靴で',
          '紅葉の時期のあと、永源寺のまわりで食事の店が開いているかは要確認。お昼は京都駅で買って持っていく',
          '永源寺の拝観は16:00まで',
          '教林坊の夜のライトアップは12月6日で終わったので、このコースには入っていません',
          '近江鉄道は2026年3月から ICOCA などの交通系ICカードで乗れる',
          '湖東三山のうち西明寺・金剛輪寺は、上の「湖東三山」のコースで（予約制の乗合タクシー）'
        ],
        day: [
          { time: '10:00', area: '京都駅 → 近江八幡', title: 'JRの新快速で近江八幡へ', text: '京都駅10:00発の新快速「近江塩津」行きで、乗り換えなし。近江八幡に10:35（土日祝10:34）。10:42の近江鉄道に乗り換えて、太郎坊宮前に10:57。', photo: ['omihachimaneki', 1] },
          { time: '11:15', area: '太郎坊宮', title: '石段を登って、勝運の神社へ', text: '742段の石段と夫婦岩を通って本殿へ。近江の平野が見渡せます。12:41か12:59の電車で八日市へ。', photo: ['taroubou', 5] },
          { time: '13:45', area: '永源寺', title: 'お昼のあと、山門と法堂へ', text: '八日市13:15のバスで永源寺へ。持ってきたお昼を食べてから、閉まる16:00までゆっくりお参り。', photo: ['eigenji', 1] },
          { time: '16:24', area: '永源寺 → 京都駅', title: 'バスと近江鉄道、新快速で京都へ', text: '永源寺前16:24（土日祝16:25）のバス、八日市17:09の近江鉄道、近江八幡17:36の新快速と乗り継ぎます。', photo: ['eigenji', 3] },
          { time: '18:12', area: '京都駅', title: '京都に戻って、夜は街なか', text: '京都駅18:12着。三条・木屋町・先斗町へは地下鉄で約15分、18:30ごろから21〜22時まで晩ごはんを楽しめます。', photo: ['eigenji', 9] }
        ],
        dealsLead: '京都駅から回って京都駅へ帰ると、電車とバスは合わせて3,710円（京都駅→太郎坊宮前1,070円、太郎坊宮前→八日市160円、八日市→永源寺前のバス670円、永源寺前→京都駅1,810円）。永源寺の参拝志納料600円は別です。',
        deals: [
          { name: '京都駅 → 太郎坊宮前', price: '1,070円', text: 'JR680円＋近江鉄道390円。三条のあたりからは、地下鉄で京都駅まで260円（烏丸御池で乗り換え）。', url: 'https://transit.yahoo.co.jp/' },
          { name: '八日市駅 → 永源寺前（近江鉄道バス）', price: '670円', text: '八日市駅1番のりば13:15発。', url: 'https://www.ohmitetudo.co.jp/bus/access/eigenji/' },
          { name: '永源寺前 → 京都駅', price: '1,810円', text: 'バス670円＋近江鉄道460円＋JR680円。永源寺前16:24（土日祝16:25）発。', url: 'https://transit.yahoo.co.jp/' }
        ],
        dealsNote: '大人の運賃・料金です。2026年11月22日に、永源寺の公式サイト、電車とバスは乗換案内（12月のダイヤ）で確認しました。',
        how: [
          { title: 'コースを選ぶ', text: '一覧の上のボタンで「太郎坊宮・永源寺」か「湖東三山」を選びます。コースによって、時間割と番号が変わります。' },
          { title: '行きたい場所を入れ替える', text: '最初は太郎坊宮と永源寺が選んであります。どちらかを外すと、行き方などの一言が出ます。' },
          { title: '番号をタップ', text: '写真・説明・料金・電車とバスの時刻が見られます。入口で困ること（お昼・閉まる時間）は、いちばん上の注意に。' },
          { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。' }
        ]
      },
      sanzanTaxi: {
        h1: '国宝の本堂を2つ、乗合タクシーで。',
        lead: '2026年の紅葉シャトルバスは11月29日で終わりました。11月30日からは、予約制の乗合タクシーで湖東三山のうち西明寺と金剛輪寺を回ります。京都駅を平日9:34・土日祝9:37に出て、西明寺の門前でお昼、午後は金剛輪寺。京都駅には17:06に戻ります。',
        dayHead: '1日の流れ（京都駅 9:34発、土日祝9:37発）',
        who: [
          '京都駅を平日9:34・土日祝9:37の普通電車で出て、河瀬へ（乗り換えなし・990円）。三条のあたりからは、地下鉄で京都駅まで約15分',
          '乗合タクシーは3回とも予約。乗る1週間前から1時間前までに、近江タクシー彦根営業所 0749-22-1111へ。支払いは現金だけ',
          '乗合タクシーは12月29日〜1月3日は運休',
          '西明寺の境内は持ち込みの飲食ができない。門前の千成亭ぎゅ〜じあむは月・火が休み',
          '金剛輪寺から稲枝駅までは、停留所を回るので1時間12分。遅い便にするなら予約のときに',
          '百済寺は乗合タクシーの路線にないので別の日に',
          '12月6日までは、帰りに教林坊の夜のライトアップにも寄れる。一覧で選ぶと行き方が出る',
          '西明寺と金剛輪寺の写真は Wikimedia Commons から（Toshi はまだ行っていません）'
        ],
        day: [
          { time: '9:34', area: '京都駅 → 河瀬', title: 'JRの普通電車で河瀬へ', text: '京都駅9:34発で、乗り換えなしで河瀬に10:34。土日祝は9:37発で10:32着。東口で乗合タクシーを待ちます。', photo: ['kawaseeki', 0] },
          { time: '11:08', area: '西明寺', title: '国宝の本堂と三重塔、門前でお昼', text: '10:51発の乗合タクシーで西明寺へ。1時間ほどお参りして、門前で近江牛のお昼（月・火休み）。12:56のタクシーで金剛輪寺へ。', photo: ['saimyoji', 1] },
          { time: '13:03', area: '金剛輪寺', title: '千体地蔵の参道と国宝の本堂', text: '上りの参道を本堂と三重塔へ。帰りのタクシーまで1時間40分ほど、ゆっくり回れます。', photo: ['kongorinji', 0] },
          { time: '14:42', area: '金剛輪寺 → 稲枝', title: '乗合タクシーで駅へ', text: '停留所を回って稲枝駅に15:54。16:13発の電車に乗ります。', photo: ['kongorinji', 1] },
          { time: '17:06', area: '京都駅', title: '京都に戻って晩ごはん', text: '街なかで21〜22時まで（三条・木屋町・先斗町へは地下鉄で約15分）。もっとゆっくりするなら、15:42のタクシーで京都駅18:06、16:42のタクシーで19:06。', photo: ['kongorinji', 2] }
        ],
        dealsLead: '京都駅から回って京都駅へ帰ると、電車と乗合タクシーは合わせて3,980円（京都駅→河瀬990円、乗合タクシー800＋400＋800円、稲枝→京都駅990円）。入山料は西明寺800円・金剛輪寺800円。',
        deals: [
          { name: '京都駅 → 河瀬、稲枝 → 京都駅（JR）', price: '990円×2', text: '普通電車で乗り換えなし。三条のあたりからは、地下鉄で京都駅まで260円（烏丸御池で乗り換え）。', url: 'https://transit.yahoo.co.jp/' },
          { name: '乗合タクシー「愛のりタクシー」', price: '1回400〜800円', text: '河瀬駅→西明寺800円、西明寺→金剛輪寺400円、金剛輪寺→稲枝駅800円。現金のみ。2人以上でまとめて予約して同じ停留所から乗ると半額。', url: 'https://www.city.hikone.lg.jp/kurashi/kotsu_doro/3/6022.html' }
        ],
        dealsNote: '大人の運賃・料金です。2026年11月22日に、彦根市の愛のりタクシー時刻表・各寺の公式サイト、電車は乗換案内で確認しました。',
        how: [
          { title: 'コースを選ぶ', text: '一覧の上のボタンで「太郎坊宮・永源寺」か「湖東三山」を選びます。コースによって、時間割と番号が変わります。' },
          { title: '行きたい場所を入れ替える', text: '最初は西明寺と金剛輪寺が選んであります。入れ替えると、行き方などの一言が出ます。' },
          { title: '番号をタップ', text: '写真・説明・料金・乗合タクシーと電車の時刻が見られます。入口で困ること（予約・現金だけ・休みの日）は、いちばん上の注意に。' },
          { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。' }
        ]
      },
      sanzanWinter: {
        who: [
          '京都駅を平日9:34・土日祝9:37の普通電車で出て、河瀬へ（乗り換えなし・990円）。三条のあたりからは、地下鉄で京都駅まで約15分',
          '乗合タクシーは3回とも予約。乗る1週間前から1時間前までに、近江タクシー彦根営業所 0749-22-1111へ。支払いは現金だけ',
          '乗合タクシーは12月29日〜1月3日は運休',
          '西明寺の境内は持ち込みの飲食ができない。門前の千成亭ぎゅ〜じあむは月・火が休み',
          '金剛輪寺から稲枝駅までは、停留所を回るので1時間12分。遅い便にするなら予約のときに',
          '百済寺は乗合タクシーの路線にないので別の日に',
          '西明寺と金剛輪寺の写真は Wikimedia Commons から（Toshi はまだ行っていません）'
        ]
      }
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
    listNote: 'Numbers show the order. The places on the timetable are selected at first. The dotted line shows the order, not the actual path.',
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
    bus: 'Bus',
    taxi: 'Taxi',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on official websites and a route planner on {d}. Details can change, so please check before you go.',
    unchecked: 'Some of this could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 22, 2026',
    noticeHead: 'Note for this season',
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
    swCourse: 'Course',
    courseAria: 'Course',
    courseEigenji: 'Taroubou-gu & Eigenji\n(leave 9–10 am)',
    courseSanzan: 'Koto Sanzan temples\n(leave around 8 am)',
    courseSanzanTaxi: 'Two Koto Sanzan temples\n(leave around 9:30)',
    swMode: 'Stops',
    modeAria: 'How to go',
    modeAll: 'Full route',
    modePick: 'Choose stops',
    pickNote: 'Tap “Want to go” on the places you like. Only the chosen places are joined by the dotted line; the starting station is added automatically. Suggested times assume the places selected at first.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. stations)',
    pickEmpty: 'Nothing chosen yet. Pick the temples and shrine you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Auto',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      kicker: 'Autumn map | Leaves usually peak mid to late November',
      favLabel: 'Highlight',
      whoHead: 'Before you go',
      dayHead: 'One day, roughly like this',
      from: '',
      timeSuffix: '',
      dealsHead: 'Fares',
      dealsMore: 'See official site',
      howHead: 'How to use this map',
      cta: 'Open the map',
      footer1: 'An original map, hand-walked by Toshi.'
    },
    introFor: {
      eigenji: {
        h1: 'From maples above 742 stone steps to a lantern-lit bamboo grove.',
        lead: 'Leave Kyoto Station on the 10:00 Special Rapid and change to the Ohmi Railway for Taroubou-gu, a shrine halfway up a pointed peak with the Omi plain below. Then a bus into the Echigawa valley to Eigenji for a late lunch and the maples until late afternoon, and finally the night garden of Kyorinbo, open only in spring and autumn. Back at Kyoto Station at 20:12.',
        favName: 'Eigenji',
        favText: 'The great gate and lecture hall wrapped in maples.',
        favPhoto: ['eigenji', 2],
        dayHead: 'The day, leaving Kyoto Station at 10:00',
        who: [
          'The 10:00 Special Rapid from Kyoto Station and the Ohmi Railway get you to Taroubougu-mae at 10:57 (¥1,070). From around Sanjo, the subway to Kyoto Station takes about 15 minutes',
          'Taroubou-gu means 742 stone steps; wear good shoes',
          'There’s almost nowhere to eat until Eigenji, where lunch is around 14:00. Have a good breakfast',
          'Kyorinbo is about 10 min by taxi from Azuchi Station (around ¥2,500). Book both ways ahead',
          'The Kyorinbo illumination runs until 6 Dec in 2026 (last entry 19:00)',
          'Since March 2026 the Ohmi Railway takes ICOCA and other transport IC cards',
          'For the Koto Sanzan temples (Saimyoji, Hyakusaiji, Kongorinji), switch to the “Koto Sanzan” course above'
        ],
        day: [
          { time: '10:00', area: 'Kyoto Sta. → Omi-Hachiman', title: 'JR Special Rapid to Omi-Hachiman', text: 'The 10:00 Special Rapid for Omi-Shiotsu goes direct: Omi-Hachiman at 10:35 (10:34 at weekends). Change to the 10:42 Ohmi Railway; Taroubougu-mae at 10:57.', photo: ['omihachimaneki', 1] },
          { time: '11:15', area: 'Taroubou-gu', title: 'Up the steps to the shrine of victory', text: '742 steps and the Meoto-iwa rocks to the main hall, with the Omi plain below. Take the 12:41 or 12:59 train to Yokaichi.', photo: ['taroubou', 5] },
          { time: '13:45', area: 'Eigenji', title: 'A late lunch and the valley maples', text: 'The 13:15 bus from Yokaichi. Lunch first, then the gate and lecture hall in red. Leave on the 16:24 bus (16:25 at weekends).', photo: ['eigenji', 0] },
          { time: '18:00', area: 'Azuchi → Kyorinbo', title: 'Bamboo and garden by lantern light', text: 'Ohmi Railway and JR to Azuchi (17:44), then a taxi. Enjoy the night garden until about 19:00.', photo: ['kyorinbo', 0] },
          { time: '20:12', area: 'Kyoto Sta.', title: 'Dinner back in Kyoto', text: 'The 19:28 from Azuchi, with a change to the Special Rapid at Omi-Hachiman, reaches Kyoto Station at 20:12. The evening in town can run to 21:00–22:00 (Sanjo, Kiyamachi and Pontocho are about 15 min by subway). Or have dinner in Omihachiman.', photo: ['kyorinbo', 3] }
        ],
        dealsLead: 'From Kyoto Station and back, trains and buses come to ¥3,990 (Kyoto Station → Taroubougu-mae ¥1,070, Taroubougu-mae → Yokaichi ¥160, bus to Eigenji ¥670, bus back ¥670 plus Yokaichi → Azuchi ¥650, Azuchi → Kyoto Station ¥770). Admission (Eigenji ¥600, Kyorinbo ¥1,000) and the taxi to Kyorinbo (around ¥2,500 each way) are extra.',
        deals: [
          { name: 'Kyoto Station → Taroubougu-mae', price: '¥1,070', text: 'JR ¥680 + Ohmi Railway ¥390. Back from Azuchi to Kyoto Station ¥770. From around Sanjo, the subway to Kyoto Station is ¥260 (change at Karasuma Oike).', url: 'https://transit.yahoo.co.jp/' },
          { name: 'Yokaichi → Eigenji-mae (Ohmi bus)', price: '¥670', text: '13:15 from stop 1 at Yokaichi Station. Back from Eigenji-mae at 16:24 (16:25 at weekends).', url: 'https://www.ohmitetudo.co.jp/bus/access/eigenji/' },
          { name: 'Taxi (Azuchi Station ↔ Kyorinbo)', price: 'about ¥2,500 each way', text: 'About 10 minutes; the fare is the temple’s own estimate. Book the ride there and the pick-up back.', url: 'https://kyourinbo.jimdofree.com/' }
        ],
        dealsNote: 'Adult fares and fees, checked on Nov 22, 2026 (Ohmi bus timetable, the Kyorinbo and Eigenji websites, and a route planner for trains).',
        how: [
          { title: 'Choose a course', text: 'Use the buttons above the list to pick “Taroubou-gu & Eigenji” or “Koto Sanzan temples”. The timetable and numbering change with the course.' },
          { title: 'Swap places in and out', text: 'The three places on the timetable are selected at first. Drop one and a note on getting home appears.' },
          { title: 'Tap a number', text: 'See photos, tips, fees and train and bus times. Anything that could stop you at the door (dates, taxis, last entry) is in the note at the top.' },
          { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions.' }
        ]
      },
      sanzan: {
        h1: 'Two National Treasure halls and a mossy approach, by shuttle bus.',
        lead: 'The three Koto Sanzan temples, Saimyoji, Hyakusaiji and Kongorinji, stand far apart at the foot of the Suzuka hills. Only in the leaf season (19–29 Nov in 2026) does a shuttle bus link them from Hikone Station. Take the Special Rapid from Kyoto Station at 8:37 (8:30 at weekends and holidays) for the 10:00 bus, have Omi beef for lunch by Saimyoji’s gate, spend the afternoon at Hyakusaiji and late afternoon at Kongorinji. Back at Kyoto Station at 18:42.',
        favName: 'Saimyoji',
        favText: 'A National Treasure hall and pagoda among tall cedars.',
        favPhoto: ['saimyoji', 0],
        dayHead: 'A shuttle-bus day, leaving Kyoto Station at 8:37 (weekends 8:30)',
        who: [
          'Take the direct Special Rapid from Kyoto Station at 8:37 (8:30 at weekends and holidays; ¥1,170) for the 10:00 shuttle from Hikone. From around Sanjo, the subway to Kyoto Station takes about 15 minutes',
          'The shuttle is an ordinary bus and you may have to stand. With a Momiji Kippu (¥2,500, cash) you can book buses from Hikone',
          'No food or drink of your own at Saimyoji. Lunch is at Sennaritei Gyuseum by the gate (phone ahead on Mon/Tue)',
          'Kongorinji’s last entry is 16:30. Arriving on the 15:43 bus, head straight up to the main hall',
          'On days without the shuttle (from 30 Nov), take the 9:34 from Kyoto Station (9:37 at weekends) to Kawase, then bookable shared taxis (cash only) to two temples, Saimyoji and Kongorinji. Times are in the note at stop 1',
          'The Saimyoji and Kongorinji photos are from Wikimedia Commons (Toshi hasn’t been yet)'
        ],
        day: [
          { time: '8:37', area: 'Kyoto Sta. → Hikone', title: 'JR Special Rapid to Hikone', text: 'The 8:37 from Kyoto Station runs direct, reaching Hikone at 9:31. At weekends and holidays, take the 8:30 (Hikone 9:20). Go to stop 4 at the west exit.', photo: ['hikoneeki', 0] },
          { time: '10:32', area: 'Saimyoji', title: 'National Treasures, then lunch by the gate', text: 'The 10:00 shuttle to Saimyoji. An hour at the temple, Omi beef for lunch, then the 12:32 bus to Hyakusaiji.', photo: ['saimyoji', 1] },
          { time: '13:10', area: 'Hyakusaiji', title: 'Mossy approach and a garden with a view', text: 'Through the Nio gate to the main hall, then the garden and the lookout over the plain. The 15:20 bus to Kongorinji.', photo: ['hyakusaiji', 0] },
          { time: '15:43', area: 'Kongorinji', title: 'A thousand Jizo and blood-red maples', text: 'Last entry 16:30. The main hall and pagoda in late-afternoon light. The 16:43 bus to Hikone.', photo: ['kongorinji', 0] },
          { time: '17:52', area: 'Hikone → Kyoto Sta.', title: 'Back to Kyoto for dinner', text: 'The 17:52 from Hikone reaches Kyoto Station at 18:42 every day. The evening in town can run to 21:00–22:00 (Sanjo, Kiyamachi and Pontocho are about 15 min by subway), or stop at the Kyorinbo illumination on the way.', photo: ['kongorinji', 2] }
        ],
        dealsLead: 'On a shuttle day, trains and buses from Kyoto Station and back come to ¥4,640 (Kyoto Station ↔ Hikone ¥1,170 each way, shuttle ¥700 + ¥500 + ¥300 + ¥800). With the ¥2,500 Momiji Kippu, each temple’s admission is ¥50 cheaper and you can book buses from Hikone. Admission: Saimyoji ¥800, Hyakusaiji ¥600, Kongorinji ¥800.',
        deals: [
          { name: 'Kyoto Station → Hikone', price: '¥1,170', text: 'Direct by Special Rapid; ¥1,170 back too. From around Sanjo, the subway to Kyoto Station is ¥260 (change at Karasuma Oike).', url: 'https://transit.yahoo.co.jp/' },
          { name: 'Autumn shuttle bus (19–29 Nov 2026)', price: '¥200–1,000 a ride', text: 'Hikone → Saimyoji ¥700, Saimyoji → Hyakusaiji ¥500, Hyakusaiji → Kongorinji ¥300, Kongorinji → Hikone ¥800.', url: 'https://www.ohmitetudo.co.jp/bus/icoico/event/kotosanzanshuttlebus2026/' },
          { name: 'Momiji Kippu (day pass)', price: '¥2,500', text: 'Cash on the day, at the Hikone west-exit bus stop or on the bus; children ¥1,250. ¥50 off each temple, a bottle of water at Klefiel Koto, an oolong tea with a meal at Sennaritei Gyuseum.', url: 'https://kokokubus.rsvsys.jp/reservations/calendar?category=5' },
          { name: '“Ainori Taxi” shared taxi (days without the shuttle)', price: '¥400–800 a ride', text: 'Kawase → Saimyoji ¥800, Saimyoji → Kongorinji ¥400, Kongorinji → Inae ¥800. Cash only. JR: Kyoto Station → Kawase ¥990, Inae → Kyoto Station ¥990. Not running 29 Dec – 3 Jan; book at least 1 hour ahead (Ohmi Taxi Hikone, 0749-22-1111).', url: 'https://www.city.hikone.lg.jp/kurashi/kotsu_doro/3/6022.html' }
        ],
        dealsNote: 'Adult fares and fees, checked on Nov 22, 2026 (Ohmi Railway’s shuttle page, the Koto Sanzan leaflet, the temple websites, Hikone City’s Ainori Taxi timetables, and a route planner for trains).',
        how: [
          { title: 'Choose a course', text: 'Use the buttons above the list to pick “Taroubou-gu & Eigenji” or “Koto Sanzan temples”. The timetable and numbering change with the course.' },
          { title: 'Swap places in and out', text: 'The three temples are selected at first. Add Kyorinbo to see how to stop at its evening illumination on the way home.' },
          { title: 'Tap a number', text: 'See photos, tips, fees and shuttle times. Anything that could stop you at the door (cash only, booking, last entry) is in the note at the top.' },
          { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions.' }
        ]
      },
      eigenjiWinter: {
        h1: 'From a shrine above 742 stone steps to a Zen temple in the valley.',
        lead: 'Leave Kyoto Station on the 10:00 Special Rapid and change to the Ohmi Railway for Taroubou-gu, a shrine halfway up a pointed peak with the Omi plain below. Then a bus into the Echigawa valley to Eigenji: eat the lunch you brought and visit until it closes at 16:00. Back at Kyoto Station at 18:12 for an evening in town.',
        favText: 'A great gate and lecture hall in a river valley.',
        favPhoto: ['eigenji', 3],
        who: [
          'The 10:00 Special Rapid from Kyoto Station and the Ohmi Railway get you to Taroubougu-mae at 10:57 (¥1,070). From around Sanjo, the subway to Kyoto Station takes about 15 minutes',
          'Taroubou-gu means 742 stone steps; wear good shoes',
          'Places to eat around Eigenji after the leaf season are not confirmed. Buy lunch at Kyoto Station and bring it',
          'Eigenji closes at 16:00',
          'The Kyorinbo evening illumination ended on 6 December, so it isn’t on this course',
          'Since March 2026 the Ohmi Railway takes ICOCA and other transport IC cards',
          'For Saimyoji and Kongorinji, switch to the “Koto Sanzan” course above (bookable shared taxi)'
        ],
        day: [
          { time: '10:00', area: 'Kyoto Sta. → Omi-Hachiman', title: 'JR Special Rapid to Omi-Hachiman', text: 'The 10:00 Special Rapid for Omi-Shiotsu goes direct: Omi-Hachiman at 10:35 (10:34 at weekends). Change to the 10:42 Ohmi Railway; Taroubougu-mae at 10:57.', photo: ['omihachimaneki', 1] },
          { time: '11:15', area: 'Taroubou-gu', title: 'Up the steps to the shrine of victory', text: '742 steps and the Meoto-iwa rocks to the main hall, with the Omi plain below. Take the 12:41 or 12:59 train to Yokaichi.', photo: ['taroubou', 5] },
          { time: '13:45', area: 'Eigenji', title: 'Lunch, then the gate and lecture hall', text: 'The 13:15 bus from Yokaichi. Eat the lunch you brought, then take your time until the temple closes at 16:00.', photo: ['eigenji', 1] },
          { time: '16:24', area: 'Eigenji → Kyoto Sta.', title: 'Bus, Ohmi Railway and Special Rapid', text: 'The 16:24 bus (16:25 at weekends) from Eigenji-mae connects with the 17:09 Ohmi Railway from Yokaichi and the 17:36 Special Rapid from Omi-Hachiman.', photo: ['eigenji', 3] },
          { time: '18:12', area: 'Kyoto Sta.', title: 'An evening in town', text: 'Kyoto Station at 18:12. Sanjo, Kiyamachi and Pontocho are about 15 min by subway, so dinner can run from about 18:30 until 21:00–22:00.', photo: ['eigenji', 9] }
        ],
        dealsLead: 'From Kyoto Station and back, trains and buses come to ¥3,710 (Kyoto Station → Taroubougu-mae ¥1,070, Taroubougu-mae → Yokaichi ¥160, bus to Eigenji ¥670, Eigenji-mae → Kyoto Station ¥1,810). Eigenji admission of ¥600 is extra.',
        deals: [
          { name: 'Kyoto Station → Taroubougu-mae', price: '¥1,070', text: 'JR ¥680 + Ohmi Railway ¥390. From around Sanjo, the subway to Kyoto Station is ¥260 (change at Karasuma Oike).', url: 'https://transit.yahoo.co.jp/' },
          { name: 'Yokaichi → Eigenji-mae (Ohmi bus)', price: '¥670', text: '13:15 from stop 1 at Yokaichi Station.', url: 'https://www.ohmitetudo.co.jp/bus/access/eigenji/' },
          { name: 'Eigenji-mae → Kyoto Station', price: '¥1,810', text: 'Bus ¥670 + Ohmi Railway ¥460 + JR ¥680. Leave Eigenji-mae at 16:24 (16:25 at weekends).', url: 'https://transit.yahoo.co.jp/' }
        ],
        dealsNote: 'Adult fares and fees, checked on Nov 22, 2026 (the Eigenji website, and a route planner for December trains and buses).',
        how: [
          { title: 'Choose a course', text: 'Use the buttons above the list to pick “Taroubou-gu & Eigenji” or “Koto Sanzan temples”. The timetable and numbering change with the course.' },
          { title: 'Swap places in and out', text: 'Taroubou-gu and Eigenji are selected at first. Drop one and a note on getting around appears.' },
          { title: 'Tap a number', text: 'See photos, tips, fees and train and bus times. Anything that could stop you at the door (lunch, closing time) is in the note at the top.' },
          { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions.' }
        ]
      },
      sanzanTaxi: {
        h1: 'Two National Treasure halls, by shared taxi.',
        lead: 'The 2026 autumn shuttle ended on 29 November. From 30 November, a bookable shared taxi takes you to two of the Koto Sanzan temples, Saimyoji and Kongorinji. Leave Kyoto Station at 9:34 (9:37 at weekends and holidays), have lunch by Saimyoji’s gate and spend the afternoon at Kongorinji. Back at Kyoto Station at 17:06.',
        dayHead: 'The day, leaving Kyoto Station at 9:34 (weekends 9:37)',
        who: [
          'Take the direct local from Kyoto Station to Kawase at 9:34 (9:37 at weekends and holidays; ¥990). From around Sanjo, the subway to Kyoto Station takes about 15 minutes',
          'Book all three shared-taxi rides from a week to 1 hour ahead with Ohmi Taxi Hikone, 0749-22-1111. Cash only',
          'The shared taxi doesn’t run from 29 December to 3 January',
          'No food or drink of your own at Saimyoji. Sennaritei Gyuseum by the gate closes on Mondays and Tuesdays',
          'Kongorinji to Inae Station takes 1 hour 12 minutes, winding between stops. For a later ride, decide when you book',
          'Hyakusaiji is off the shared-taxi route, so save it for another day',
          'Until 6 December you can add the Kyorinbo evening illumination on the way home: select it in the list for directions',
          'The Saimyoji and Kongorinji photos are from Wikimedia Commons (Toshi hasn’t been yet)'
        ],
        day: [
          { time: '9:34', area: 'Kyoto Sta. → Kawase', title: 'JR local train to Kawase', text: 'The 9:34 from Kyoto Station runs direct, reaching Kawase at 10:34. At weekends and holidays, take the 9:37 (Kawase 10:32). Wait for the shared taxi at the east exit.', photo: ['kawaseeki', 0] },
          { time: '11:08', area: 'Saimyoji', title: 'National Treasures, then lunch by the gate', text: 'The 10:51 shared taxi to Saimyoji. An hour at the temple and Omi beef for lunch (closed Mon–Tue), then the 12:56 taxi to Kongorinji.', photo: ['saimyoji', 1] },
          { time: '13:03', area: 'Kongorinji', title: 'A thousand Jizo and a National Treasure hall', text: 'Up the approach to the main hall and pagoda. You have about 1 hour 40 minutes before the taxi back.', photo: ['kongorinji', 0] },
          { time: '14:42', area: 'Kongorinji → Inae', title: 'Shared taxi to the station', text: 'It winds between stops, reaching Inae Station at 15:54. Take the 16:13 train.', photo: ['kongorinji', 1] },
          { time: '17:06', area: 'Kyoto Sta.', title: 'Dinner back in Kyoto', text: 'The evening in town can run to 21:00–22:00 (Sanjo, Kiyamachi and Pontocho are about 15 min by subway). For more time at the temple, the 15:42 taxi gets you back at 18:06, the 16:42 at 19:06.', photo: ['kongorinji', 2] }
        ],
        dealsLead: 'From Kyoto Station and back, trains and shared taxis come to ¥3,980 (Kyoto Station → Kawase ¥990, shared taxi ¥800 + ¥400 + ¥800, Inae → Kyoto Station ¥990). Admission: Saimyoji ¥800, Kongorinji ¥800.',
        deals: [
          { name: 'Kyoto Station → Kawase, Inae → Kyoto Station (JR)', price: '¥990 × 2', text: 'Direct local trains. From around Sanjo, the subway to Kyoto Station is ¥260 (change at Karasuma Oike).', url: 'https://transit.yahoo.co.jp/' },
          { name: '“Ainori Taxi” shared taxi', price: '¥400–800 a ride', text: 'Kawase → Saimyoji ¥800, Saimyoji → Kongorinji ¥400, Kongorinji → Inae ¥800. Cash only. Half fare for two or more booked together from the same stop.', url: 'https://www.city.hikone.lg.jp/kurashi/kotsu_doro/3/6022.html' }
        ],
        dealsNote: 'Adult fares and fees, checked on Nov 22, 2026 (Hikone City’s Ainori Taxi timetables, the temple websites, and a route planner for trains).',
        how: [
          { title: 'Choose a course', text: 'Use the buttons above the list to pick “Taroubou-gu & Eigenji” or “Koto Sanzan temples”. The timetable and numbering change with the course.' },
          { title: 'Swap places in and out', text: 'Saimyoji and Kongorinji are selected at first. Change them and a note on getting around appears.' },
          { title: 'Tap a number', text: 'See photos, tips, fees and shared-taxi and train times. Anything that could stop you at the door (booking, cash only, closing days) is in the note at the top.' },
          { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions.' }
        ]
      },
      sanzanWinter: {
        who: [
          'Take the direct local from Kyoto Station to Kawase at 9:34 (9:37 at weekends and holidays; ¥990). From around Sanjo, the subway to Kyoto Station takes about 15 minutes',
          'Book all three shared-taxi rides from a week to 1 hour ahead with Ohmi Taxi Hikone, 0749-22-1111. Cash only',
          'The shared taxi doesn’t run from 29 December to 3 January',
          'No food or drink of your own at Saimyoji. Sennaritei Gyuseum by the gate closes on Mondays and Tuesdays',
          'Kongorinji to Inae Station takes 1 hour 12 minutes, winding between stops. For a later ride, decide when you book',
          'Hyakusaiji is off the shared-taxi route, so save it for another day',
          'The Saimyoji and Kongorinji photos are from Wikimedia Commons (Toshi hasn’t been yet)'
        ]
      }
    }
  }
};
