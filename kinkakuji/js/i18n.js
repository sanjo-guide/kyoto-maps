/* Page texts in Japanese and English.
   Toshi 個人のマップ。金閣寺・龍安寺・仁和寺・大徳寺・平野神社・北野天満宮を回る、京都の北西の1日ルート。
   コースは2つ：early（早朝。龍安寺8:00・金閣寺9:00の開門に合わせる）と late（9〜10時に出発。金閣寺は夕方）。
   コースで変わる文言は courseFor[コース] に書き、js/app.js が上書きする（何も選んでいないときは early）。
   Photos are [spot id, photo index]（番号はコースで変わるので id で指定）。データは data/routes/kinkakuji.json と kinkakuji-late.json。
   料金・時間・時刻は2026年11月22日に各公式サイトで確認（出典はデータの sources、scripts/build_kinkakuji_data.py）。 */
window.KINKAKUJI_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 金閣寺・龍安寺・仁和寺・北野天満宮 Kinkaku-ji MAP',
    titleMain: '金閣寺〜北野',
    titleSub: 'Kinkaku-ji to Kitano',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '',   // コースごと（courseFor）
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
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトで確認しました。変わることがあるので、行く前に公式サイトも見てください。',
    unchecked: '{d}の時点で、公式サイトでは確認できなかった情報です（要確認）。行く前に最新の情報を確かめてください。',
    checkedDate: '2026年11月22日',
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
    swCourse: 'コース（出発の時間）',
    courseAria: 'コース',
    courseEarly: '早朝コース\n龍安寺8時・金閣寺9時',
    courseLate: '9〜10時に出発\n金閣寺は夕方',
    swMode: '回り方',
    modeAria: '回り方',
    modeAll: '全部回る',
    modePick: '選んで回る',
    pickNote: '行きたい場所の「行きたい」を押してください。時間は全部回る場合の目安です。バスや電車の時刻は、全部回る場合のものです。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧から、行きたい場所を選んでください。',
    pickAll: 'すべて選ぶ',
    pickNone: 'すべて外す',
    pickOff: '行きたい',
    pickOn: '行く',
    autoTag: '全員共通',
    autoOff: '今回は通りません',
    seasonHead: '季節営業の可能性',
    hintHead: 'あなたのルートでは',
    intro: {
      kicker: 'Toshiが歩いて作った1日ルート',
      h1: '金色の金閣、静かな石庭、遅咲きの御室桜。京都の北西を1日で。',
      favLabel: 'いちばんの見どころ',
      favName: '金閣寺',
      favText: '池に映る金色の舎利殿。写真は雪の朝（2026年2月）。',
      favPhoto: ['kinkakuji', 0],
      whoHead: 'こんな人におすすめ',
      from: '',
      timeSuffix: '〜',
      dealsHead: '交通費・拝観料のめやす',
      dealsNote: '大人の運賃・料金です。拝観料・嵐電の運賃・バスと嵐電の時刻は2026年11月22日に各公式サイトで、市バスの運賃は2026年11月20日に京都市交通局で確認しました。バスは道の混み方でおくれることがあります。',
      dealsMore: '公式サイトで見る',
      howHead: 'このマップの使い方',
      cta: '地図を見る',
      footer1: 'Toshiが実際に歩いて作った、オリジナルマップです。'
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Kinkaku-ji, Ryoan-ji, Ninna-ji & Kitano Tenmangu, Kyoto MAP',
    titleMain: 'Kinkaku-ji to Kitano',
    titleSub: '金閣寺〜北野',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: '',   // per course (courseFor)
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
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on the official websites on {d}. Details can change, so please check before you go.',
    unchecked: 'Could not be confirmed on an official website as of {d}. Please check the latest information before you go.',
    checkedDate: 'Nov 22, 2026',
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
    swCourse: 'Course (start time)',
    courseAria: 'Course',
    courseEarly: 'Early course\nRyoan-ji at 8:00',
    courseLate: 'Start at 9–10\nKinkaku-ji at 15:30',
    swMode: 'How to go',
    modeAria: 'How to go',
    modeAll: 'Full route',
    modePick: 'Choose stops',
    pickNote: 'Tap “Want to go” on the places you like. Times, including bus and tram times, are for the full route.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: 'Nothing chosen yet. Pick the places you want from the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      kicker: 'A day route, hand-walked by Toshi',
      h1: 'A golden pavilion, a silent rock garden and late-blooming cherries: north-west Kyoto in a day.',
      favLabel: 'Don’t miss',
      favName: 'Kinkaku-ji',
      favText: 'The golden pavilion reflected in its pond, here on a snowy morning (February 2026).',
      favPhoto: ['kinkakuji', 0],
      whoHead: 'Who it’s for',
      from: 'From',
      timeSuffix: '',
      dealsHead: 'Fares and fees',
      dealsNote: 'Adult prices. Entry fees, the tram fare, and bus and tram times were checked on the official websites on Nov 22, 2026; the city bus fare with the Kyoto City Transportation Bureau on Nov 20, 2026. Buses can run late in traffic.',
      dealsMore: 'See official site',
      howHead: 'How to use this map',
      cta: 'Open the map',
      footer1: 'An original map, hand-walked by Toshi.'
    }
  }
};

/* コースごとの文言。js/app.js が、選ばれているコースのぶんで上の文言を上書きする（intro の中は項目ごと）。
   day の並びは、データの sections の day（何番目か）と合わせてある（scripts/build_kinkakuji_data.py の COURSES）。
   時刻は京都市交通局の時刻表（2026年3月20日改正）と京福電気鉄道の時刻表。変えるときは build スクリプトの文章も一緒に直す。 */
(function () {
  var BUS = 'https://www2.city.kyoto.lg.jp/kotsu/busdia/bustime.htm';
  var RANDEN = 'https://www.keifuku.co.jp/randen_timetable.php';
  var KINKAKU = 'https://www.shokoku-ji.jp/kinkakuji/access/';

  window.KINKAKUJI_I18N.ja.courseFor = {
    early: {
      listNote: '早朝コース：龍安寺（8:00）→ 金閣寺（9:00）→ 大徳寺でお昼 → 仁和寺 → 平野神社 → 北野天満宮。河原町三条を7:11に出るバスで始まります。行かない場所は「選んで回る」で外せます。点線は順番を示す線で、実際の道ではありません。',
      intro: {
        lead: '龍安寺の石庭に朝8時の開門で入り、9時の開門に合わせて金閣寺へ。人が増える前にこの2つを見てから、大徳寺でひと休みとお昼。午後は仁和寺、平野神社、北野天満宮を回ります。京都の中心・三条のあたりを朝7時すぎに出る、早起きのコースです。朝ゆっくり出たい人は、一覧の上のボタンで「9〜10時に出発」に切り替えてください。',
        who: [
          '金閣寺と龍安寺を、人が増える前に見たい人に',
          '河原町三条 7:11発の市バス59系統で出発（京都市役所前は7:13）',
          '12〜2月は龍安寺の開門が8:30。バスを1本おそくします',
          '朝ごはんは出発前に。お昼は11時すぎ、大徳寺の境内で精進料理（4,500円から）',
          '乗りものは市バス3回と嵐電2回。あとは歩きです',
          '夕方は北野天満宮と上七軒。夜は、秋ならもみじ苑のライトアップ、または街なかへ'
        ],
        dayHead: '1日の流れ（早朝コース）',
        day: [
          { time: '7:11', area: '龍安寺', title: '8時の開門で石庭へ', text: '市バス59系統で「龍安寺前」へ（平日7:44着、土日祝7:43着）。8:00に入って、縁側から石庭を眺めます。8:35ごろ出て、きぬかけの路を歩いて金閣寺へ20〜25分。', note: '12〜2月は8:30開門', photo: ['ryoanji', 0] },
          { time: '9:00', area: '金閣寺', title: '開門に合わせて金閣へ', text: '池のほとりから金閣を眺めて、裏山の庭をぐるっと一周。9:45ごろ出口へ。', photo: ['kinkakuji', 1] },
          { time: '10:10', area: '大徳寺', title: '禅寺でひと休みとお昼', text: '「金閣寺道」からバスで約6分。石畳の道を歩いて、大仙院でお抹茶。お昼は11:15ごろ、境内の泉仙 大慈院店で精進料理。', note: '精進料理は4,500円から', photo: ['daitokuji', 0] },
          { time: '12:55', area: '仁和寺', title: '二王門から五重塔へ', text: '「大徳寺前」12:19発のバスで北野白梅町へ。嵐電に乗りかえて、御室仁和寺駅に12:48着。御所庭園も入れて1時間あまり。', note: '御室桜は4月中ごろ', photo: ['ninnaji', 0] },
          { time: '14:35', area: '北野', title: '桜の神社と天神さん', text: '嵐電で北野白梅町へ戻り、平野神社、北野天満宮へ。16:30ごろ東の門を出て、花街の上七軒を歩きます。', note: '毎月25日は縁日', photo: ['hirano', 0] },
          { time: '17:30', area: '夜', title: '夜の過ごし方', text: '11月13日〜12月6日（2026年）は、もみじ苑のライトアップが20:00まで。街なかへ戻るなら、「北野天満宮前」から市バス10系統で河原町三条へ約25分。三条・木屋町・先斗町で21〜22時ごろまで。', note: '写真は秋のライトアップ', photo: ['kitano', 5] }
        ],
        dealsLead: '市バスに3回、嵐電に2回乗ります。夜に街なかへバスで戻るなら、市バスがもう1回。',
        deals: [
          { name: '市バス（1回）', price: '230円', text: '河原町三条→龍安寺前、金閣寺道→大徳寺前、大徳寺前→北野白梅町。運賃は降りるときに払います。', url: BUS },
          { name: '嵐電（1回）', price: '250円', text: '北野白梅町〜御室仁和寺を行きと帰りで2回。降りるときに現金かICカードで。', url: RANDEN },
          { name: '拝観料', price: '500円〜', text: '龍安寺600円、金閣寺500円、大仙院500円、仁和寺の御所庭園800円（大人）。季節の特別公開やもみじ苑は別です。', url: KINKAKU }
        ],
        how: [
          { title: 'コースを選ぶ', text: '「一覧」の上のボタンで、「早朝コース」か「9〜10時に出発」を選べます。押すと、順番と時間が切り替わります。' },
          { title: '番号の順に', text: '1から6の順に回ります。バスや嵐電の時刻は、それぞれの場所のページに書いてあります。' },
          { title: '行きたい場所だけ選ぶ', text: '「選んで回る」に切り替えると、行きたい場所だけを点線でつなげます。' },
          { title: '番号をタップ', text: '地図の番号か「一覧」をタップすると、写真・説明・拝観時間・料金・おすすめの時間が見られます。' },
          { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。公式サイトや時刻表へのリンクもあります。' }
        ]
      }
    },
    late: {
      listNote: '9〜10時に出発するコース：北野天満宮 → 早めのお昼 → 平野神社 → 仁和寺 → 龍安寺 → 夕方の金閣寺。河原町三条を9:31に出るバスで始まります。大徳寺は入りません。点線は順番を示す線で、実際の道ではありません。',
      intro: {
        lead: '三条のあたりを9時半ごろに出て、北野天満宮から始めます。早めのお昼のあと、平野神社、嵐電で仁和寺、歩いて龍安寺、最後に夕方の金閣寺へ。金閣寺がいちばん混むと言われる昼前後を外した順番です。金閣寺と龍安寺に開門と同時に入りたい人は、一覧の上のボタンで「早朝コース」に切り替えてください。',
        who: [
          '朝はゆっくり、9時半ごろに出たい人に',
          '河原町三条 9:31発の市バス10系統で北野天満宮へ（京都市役所前は9:33）',
          '金閣寺は15:30ごろ。昼前後の混む時間は外しますが、空いているとは限りません',
          'お昼は11時、北野天満宮前のとようけ茶屋で豆腐の丼（木・金曜は休み）',
          '大徳寺はこのコースに入りません。行きたい人は早朝コースへ',
          '16:35ごろのバスで街なかへ戻って、夜は三条・木屋町・先斗町で'
        ],
        dayHead: '1日の流れ（9〜10時に出発）',
        day: [
          { time: '9:31', area: '北野', title: '天神さんから始めて、早めのお昼', text: '市バス10系統で「北野天満宮前」へ（9:57着）。お参りのあと、11:00に開くとようけ茶屋でお昼。12:00ごろ、歩いてすぐの平野神社へ。', note: 'とようけ茶屋は木・金曜休み', photo: ['kitano', 0] },
          { time: '12:45', area: '仁和寺', title: '二王門から五重塔へ', text: '北野白梅町12:33発の嵐電で約5分。御所庭園も入れて1時間あまり。14:00ごろ出ます。', note: '御室桜は4月中ごろ', photo: ['ninnaji', 0] },
          { time: '14:15', area: '龍安寺', title: '午後の石庭', text: 'きぬかけの路を歩いて約15分。縁側に座って石庭を眺めます。15:00ごろ出て、歩くかバスで金閣寺へ。', note: '12〜2月は16:30まで', photo: ['ryoanji', 0] },
          { time: '15:30', area: '金閣寺', title: '夕方の金閣、そのあと街なかへ', text: '閉門は17:00。「金閣寺道」16:35発（土日祝は16:40発）の市バス59系統で、河原町三条へ約30分。夜は三条・木屋町・先斗町で21〜22時ごろまで。', note: '昼前後の混む時間を外す', photo: ['kinkakuji', 1] }
        ],
        dealsLead: '市バスに2回（龍安寺から金閣寺もバスなら3回）、嵐電に1回乗ります。',
        deals: [
          { name: '市バス（1回）', price: '230円', text: '河原町三条→北野天満宮前、金閣寺道→河原町三条。運賃は降りるときに払います。', url: BUS },
          { name: '嵐電（1回）', price: '250円', text: '北野白梅町→御室仁和寺。降りるときに現金かICカードで。', url: RANDEN },
          { name: '拝観料', price: '500円〜', text: '仁和寺の御所庭園800円、龍安寺600円、金閣寺500円（大人）。季節の特別公開やもみじ苑は別です。', url: KINKAKU }
        ],
        how: [
          { title: 'コースを選ぶ', text: '「一覧」の上のボタンで、「早朝コース」か「9〜10時に出発」を選べます。押すと、順番と時間が切り替わります。' },
          { title: '番号の順に', text: '1から5の順に回ります。バスや嵐電の時刻は、それぞれの場所のページに書いてあります。' },
          { title: '行きたい場所だけ選ぶ', text: '「選んで回る」に切り替えると、行きたい場所だけを点線でつなげます。' },
          { title: '番号をタップ', text: '地図の番号か「一覧」をタップすると、写真・説明・拝観時間・料金・おすすめの時間が見られます。' },
          { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。公式サイトや時刻表へのリンクもあります。' }
        ]
      }
    }
  };

  window.KINKAKUJI_I18N.en.courseFor = {
    early: {
      listNote: 'Early course: Ryoan-ji (8:00) → Kinkaku-ji (9:00) → lunch at Daitoku-ji → Ninna-ji → Hirano Shrine → Kitano Tenmangu. It starts with the 7:11 bus from Kawaramachi-Sanjo. Use “Choose stops” to drop places you’ll skip. The dotted line shows the order, not the actual path.',
      intro: {
        lead: 'Walk into Ryoan-ji’s rock garden when it opens at 8:00, then be at Kinkaku-ji for its 9:00 opening. With those two seen before the crowds build, rest and have lunch at Daitoku-ji, and spend the afternoon at Ninna-ji, Hirano Shrine and Kitano Tenmangu. It’s an early start: you leave the Sanjo area in central Kyoto just after 7:00. Prefer a slow morning? Switch to “Start at 9–10” with the buttons at the top of the list.',
        who: [
          'For seeing Kinkaku-ji and Ryoan-ji before the crowds build',
          'Starts with city bus 59 from Kawaramachi-Sanjo at 7:11 (Kyoto Shiyakusho-mae at 7:13)',
          'December–February: Ryoan-ji opens at 8:30, so you take a later bus',
          'Eat breakfast before you leave. Lunch is just after 11:00: Buddhist vegetarian food inside Daitoku-ji (from ¥4,500)',
          'Three city bus rides and two tram rides; the rest is on foot',
          'Late afternoon at Kitano Tenmangu and Kamishichiken. In the evening: the maple light-up in autumn, or back downtown'
        ],
        dayHead: 'One day, roughly like this (early course)',
        day: [
          { time: '7:11', area: 'Ryoan-ji', title: 'The rock garden at the 8:00 opening', text: 'City bus 59 to “Ryoanji-mae” (arrives 7:44 on weekdays, 7:43 on weekends and holidays). Go in at 8:00 and sit on the veranda. Leave at about 8:35 and walk the Kinukake-no-michi road to Kinkaku-ji, 20–25 minutes.', note: 'Opens 8:30 Dec–Feb', photo: ['ryoanji', 0] },
          { time: '9:00', area: 'Kinkaku-ji', title: 'The golden pavilion as it opens', text: 'See the pavilion from the pond, loop through the hillside garden, and reach the exit at about 9:45.', photo: ['kinkakuji', 1] },
          { time: '10:10', area: 'Daitoku-ji', title: 'A rest and lunch in a Zen temple', text: 'About 6 minutes by bus from “Kinkakuji-michi”. Walk the stone paths and have matcha at Daisen-in. Lunch at about 11:15: vegetarian temple food at Izusen Daiji-in, inside the grounds.', note: 'Set meals from ¥4,500', photo: ['daitokuji', 0] },
          { time: '12:55', area: 'Ninna-ji', title: 'From the great gate to the pagoda', text: 'The 12:19 bus from “Daitokuji-mae” to Kitano-Hakubaicho, then the Randen tram, reaching Omuro-Ninnaji at 12:48. A little over an hour, with the palace garden.', note: 'Omuro cherries peak in mid-April', photo: ['ninnaji', 0] },
          { time: '14:35', area: 'Kitano', title: 'A cherry shrine and Tenjin-san', text: 'Tram back to Kitano-Hakubaicho, then Hirano Shrine and Kitano Tenmangu. Leave by the east gate at about 16:30 and walk through Kamishichiken, a geisha district.', note: 'Market day on the 25th', photo: ['hirano', 0] },
          { time: '17:30', area: 'Evening', title: 'The evening', text: 'From 13 November to 6 December 2026 the maple garden is lit up until 20:00. To go back downtown, city bus 10 from “Kitano Tenmangu-mae” reaches Kawaramachi-Sanjo in about 25 minutes; Sanjo, Kiyamachi and Pontocho are good until 21:00–22:00.', note: 'Photo: the autumn light-up', photo: ['kitano', 5] }
        ],
        dealsLead: 'Three city bus rides and two tram rides. Add one more bus ride if you go back downtown by bus in the evening.',
        deals: [
          { name: 'Kyoto city bus (one ride)', price: '¥230', text: 'Kawaramachi-Sanjo → Ryoanji-mae, Kinkakuji-michi → Daitokuji-mae, Daitokuji-mae → Kitano-Hakubaicho. Pay as you get off.', url: BUS },
          { name: 'Randen tram (one ride)', price: '¥250', text: 'Kitano-Hakubaicho – Omuro-Ninnaji, there and back. Pay as you get off, cash or IC card.', url: RANDEN },
          { name: 'Entry fees', price: 'from ¥500', text: 'Ryoan-ji ¥600, Kinkaku-ji ¥500, Daisen-in ¥500, Ninna-ji’s palace garden ¥800 (adults). Seasonal openings and the maple garden are extra.', url: KINKAKU }
        ],
        how: [
          { title: 'Choose a course', text: 'With the buttons at the top of the “Spots” list, choose “Early course” or “Start at 9–10”. The order and the times change when you tap.' },
          { title: 'In number order', text: 'Follow 1 to 6. Bus and tram times are on each spot’s page.' },
          { title: 'Pick only what you want', text: 'Switch to “Choose stops” to join just the places you want with the dotted line.' },
          { title: 'Tap a number', text: 'Tap a number on the map, or open the list, to see photos, tips, opening hours, fees and suggested times.' },
          { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions. Some spots also link to official websites and timetables.' }
        ]
      }
    },
    late: {
      listNote: 'Starting at 9–10: Kitano Tenmangu → an early lunch → Hirano Shrine → Ninna-ji → Ryoan-ji → Kinkaku-ji in the late afternoon. It starts with the 9:31 bus from Kawaramachi-Sanjo. Daitoku-ji is not on this course. The dotted line shows the order, not the actual path.',
      intro: {
        lead: 'Leave the Sanjo area at about 9:30 and start at Kitano Tenmangu. After an early lunch, go on to Hirano Shrine, ride the Randen tram to Ninna-ji, walk to Ryoan-ji, and finish at Kinkaku-ji in the late afternoon. The order keeps you away from Kinkaku-ji around midday, which is said to be its busiest time. Want to be at Kinkaku-ji and Ryoan-ji the moment they open? Switch to “Early course” with the buttons at the top of the list.',
        who: [
          'For a slow morning, leaving at about 9:30',
          'Starts with city bus 10 from Kawaramachi-Sanjo at 9:31 (Kyoto Shiyakusho-mae at 9:33)',
          'Kinkaku-ji at about 15:30: outside the midday rush, though it may still be busy',
          'Lunch at 11:00: tofu on rice at Toyouke-jaya, in front of Kitano Tenmangu (closed Thursdays and Fridays)',
          'Daitoku-ji is not on this course. For that, take the early course',
          'Bus back downtown at about 16:35, and an evening around Sanjo, Kiyamachi and Pontocho'
        ],
        dayHead: 'One day, roughly like this (starting at 9–10)',
        day: [
          { time: '9:31', area: 'Kitano', title: 'Start at Tenjin-san, then an early lunch', text: 'City bus 10 to “Kitano Tenmangu-mae” (arrives 9:57). After the shrine, lunch at Toyouke-jaya, which opens at 11:00. At about 12:00, walk the short way to Hirano Shrine.', note: 'Toyouke-jaya: closed Thu & Fri', photo: ['kitano', 0] },
          { time: '12:45', area: 'Ninna-ji', title: 'From the great gate to the pagoda', text: 'About 5 minutes on the 12:33 Randen tram from Kitano-Hakubaicho. A little over an hour, with the palace garden. Leave at about 14:00.', note: 'Omuro cherries peak in mid-April', photo: ['ninnaji', 0] },
          { time: '14:15', area: 'Ryoan-ji', title: 'The rock garden in the afternoon', text: 'About 15 minutes on foot along the Kinukake-no-michi road. Sit on the veranda with the garden. Leave at about 15:00 and walk or take the bus to Kinkaku-ji.', note: 'Closes 16:30 Dec–Feb', photo: ['ryoanji', 0] },
          { time: '15:30', area: 'Kinkaku-ji', title: 'The golden pavilion late in the day, then downtown', text: 'The gate closes at 17:00. City bus 59 from “Kinkakuji-michi” at 16:35 (16:40 on weekends and holidays) reaches Kawaramachi-Sanjo in about 30 minutes. Spend the evening around Sanjo, Kiyamachi and Pontocho, until 21:00–22:00.', note: 'Outside the midday rush', photo: ['kinkakuji', 1] }
        ],
        dealsLead: 'Two city bus rides (three if you also ride from Ryoan-ji to Kinkaku-ji) and one tram ride.',
        deals: [
          { name: 'Kyoto city bus (one ride)', price: '¥230', text: 'Kawaramachi-Sanjo → Kitano Tenmangu-mae, and Kinkakuji-michi → Kawaramachi-Sanjo. Pay as you get off.', url: BUS },
          { name: 'Randen tram (one ride)', price: '¥250', text: 'Kitano-Hakubaicho → Omuro-Ninnaji. Pay as you get off, cash or IC card.', url: RANDEN },
          { name: 'Entry fees', price: 'from ¥500', text: 'Ninna-ji’s palace garden ¥800, Ryoan-ji ¥600, Kinkaku-ji ¥500 (adults). Seasonal openings and the maple garden are extra.', url: KINKAKU }
        ],
        how: [
          { title: 'Choose a course', text: 'With the buttons at the top of the “Spots” list, choose “Early course” or “Start at 9–10”. The order and the times change when you tap.' },
          { title: 'In number order', text: 'Follow 1 to 5. Bus and tram times are on each spot’s page.' },
          { title: 'Pick only what you want', text: 'Switch to “Choose stops” to join just the places you want with the dotted line.' },
          { title: 'Tap a number', text: 'Tap a number on the map, or open the list, to see photos, tips, opening hours, fees and suggested times.' },
          { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions. Some spots also link to official websites and timetables.' }
        ]
      }
    }
  };
})();
