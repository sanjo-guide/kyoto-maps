/* Page texts in Japanese and English.
   Toshi 個人のマップ。スタートは京都河原町駅、阪急嵐山駅からバスで愛宕念仏寺へ行き、坂を下って嵐山の中心へ。
   1〜7（バス〜化野念仏寺）は全員共通、8〜17 はゲストが選んで回る。
   Photos are [spot number, photo index] from data/routes/arashiyama.json.
   料金・時間は2026年11月20日に確認（公式サイトで確認できなかったものはデータに「要確認」と書いてある）。
   2026年11月22日に1日の時間割を見直した（バス 9:44→愛宕寺前 10:01、お昼は化野念仏寺のあと、先斗町は18:20ごろ）。 */
window.ARASHIYAMA_I18N = {
  ja: {
    htmlLang: 'ja',
    docTitle: '京都 嵐山・嵯峨野｜Arashiyama MAP',
    titleMain: '京都 嵐山・嵯峨野',
    titleSub: 'Arashiyama & Sagano, Kyoto',
    howto: '使い方',
    allMaps: '← マップ一覧',
    home: 'マップ一覧',
    tabMap: '地図',
    menu: 'メニュー',
    list: '一覧',
    listHead: 'スポット一覧',
    listNote: '1〜7（バスで愛宕念仏寺へ行き、坂を下って化野念仏寺まで）は全員共通。8〜17は、1日で無理なく回れる組み合わせが最初から選ばれています。番号の順に歩いてください。点線は順番を示す線で、実際の道ではありません。',
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
    credit: '写真・文章：Toshi（モンキーパークの写真の一部は Wikimedia Commons より。撮影者とライセンスを各写真に表示しています）<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: '写真：',
    loadError: '地図データを読み込めませんでした。再読み込みしてください。',
    hours: '時間',
    fee: '料金',
    closed: '休み',
    cash: '現金を用意してください',
    checked: '{d}に公式サイトで確認しました。変わることがあるので、行く前に公式サイトも見てください。',
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
    pickNote: '行かない場所は「行く」を押して外し、足したい場所は「行きたい」を押してください。1〜7（電車とバスで愛宕念仏寺へ行き、坂を下って化野念仏寺まで）と、帰りの18は全員共通です。時間は、最初から選ばれている場所を9:44のバスで回る場合の目安。大河内山荘とモンキーパークは、足すとほかを減らすことになります。',
    pickCount: '選んだ場所 {n}か所 ・ ルート全体 {t}か所（全員共通の場所を含む）',
    pickEmpty: 'まだ選んでいません。下の一覧の8〜17から、行きたい場所を選んでください。',
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
      h1: '山の上のお寺から、竹林と渡月橋へ。坂道を下る嵐山の1日。',
      lead: 'バスで奥嵯峨の山の上にある愛宕念仏寺へ。そこからは昔ながらの町並みを、坂道に沿って歩いて下るだけ。苔のお寺、竹林、天龍寺の庭、渡月橋まで、行きたい場所を選びながら嵐山の中心へ向かいます。',
      favLabel: 'いちばんの見どころ',
      favName: '愛宕念仏寺',
      favText: '1200体の、表情ゆたかな石の羅漢さん。',
      favPhoto: [5, 0],
      whoHead: 'こんな人におすすめ',
      who: [
        '嵐山の定番スポットも、静かな奥嵯峨も、両方楽しみたい人に',
        'スタートは京都河原町駅を9:00ごろ。阪急電車で嵐山まで約30分',
        '最初にバスで山の上へ。あとはほとんど下り坂を歩くだけ',
        '後半のお寺や名所は、行きたいところを選んで回る',
        '全部回ると歩く距離は約6km。歩きやすい靴で',
        '愛宕念仏寺は水曜・土曜がお休み',
        '奥嵯峨は食事の店が少なめ。パンやおにぎりを持っていくと安心',
        '拝観料は現金で用意を。モンキーパークは現金のみ'
      ],
      dayHead: '1日の流れ（目安）',
      from: '',
      day: [
        { time: '9:00', area: '京都河原町 → 嵐山', title: '阪急電車で嵐山へ', text: '京都河原町から約30分。桂で嵐山線に乗り換えます。', note: 'ゆっくり出る日は10:00ごろ発（バスは10:44）', photo: [3, 0] },
        { time: '9:44', area: '愛宕念仏寺 → 化野', title: 'バスで山の上へ、あとは坂を下るだけ', text: '10:01に愛宕寺前に着きます。羅漢さんを見たら、鳥居本の茶屋で団子を食べて、化野念仏寺まで下ります。', note: 'バスは平日・土曜は1時間に1本', badge: 'ここまでは全員同じルート', photo: [5, 1] },
        { time: '12:15', area: '化野念仏寺のあたり', title: 'お昼ごはん', text: '食事の店が少ないところです。開いていた店に入るか、持ってきたパンやおにぎりを。', note: '次に食事ができるのは16:30ごろの嵯峨野湯', photo: [6, 0] },
        { time: '13:10', area: '奥嵯峨', title: '苔と紅葉のお寺を選んで', text: '祇王寺、二尊院、常寂光寺。それぞれ歩いて5〜10分です。全部でなくても大丈夫。', note: '大河内山荘を足すと、あとが40分遅くなります', badge: '好きな場所を選ぶ', photo: [8, 0] },
        { time: '15:05', area: '竹林 → 天龍寺', title: '竹林の小径と天龍寺の庭', text: '竹林を歩いて野宮神社へ。天龍寺には北門から入って、池の庭を眺めます。', note: '天龍寺の庭園は16:50受付終了', photo: [12, 0] },
        { time: '16:30', area: '嵐山の中心', title: '銭湯カフェと渡月橋', text: '元銭湯のカフェでひと休みしたら、渡月橋へ。11月〜1月は、橋に着くころには暗くなっています。', note: 'モンキーパークは入園16:00まで・現金のみ。行く日はお寺を1つに', photo: [16, 0] },
        { time: '17:50', area: '京都の街なかへ', title: '夜は先斗町へ', text: '阪急電車で京都河原町へ戻ると18:20ごろ。先斗町で晩ごはんに。', photo: [18, 0] }
      ],
      timeSuffix: '〜',
      dealsHead: '交通費のめやす',
      dealsLead: '京都河原町から出発して京都河原町へ戻ると、電車とバスで大人1人710円です（拝観料は別）。',
      deals: [
        { name: '阪急電車（京都河原町→嵐山）', price: '240円', text: '桂で嵐山線に乗り換えます。交通系ICカードも使えます。', url: 'https://www.hankyu.co.jp/station/kawaramachi.html' },
        { name: '京都バス 92・94系統（阪急嵐山駅前→愛宕寺前）', price: '230円', text: '清滝行き。平日と土曜は1時間に1本（9:44、10:44）。日曜・祝日の午前は9:14、9:44、10:14、10:44。ICカードは降りるときにタッチ。', url: 'https://www.kyotobus.jp/route/timetable/schedule.html?stop_id=421_3' },
        { name: '阪急電車（嵐山→京都河原町）', price: '240円', text: '帰りも桂で乗り換えです。', url: 'https://www.hankyu.co.jp/station/arashiyama.html' }
      ],
      dealsNote: '大人の普通運賃です。2026年11月20日に阪急電鉄・京都バスの公式サイトで確認しました。「地下鉄・バス1日券」は阪急電車に使えないので、このルートではお得になりません。',
      dealsMore: '公式サイトで見る',
      howHead: 'このマップの使い方',
      how: [
        { title: '1〜7は番号の順に', text: '京都河原町から電車とバスで愛宕念仏寺へ行き、坂を下って化野念仏寺まで。ここまでは全員同じルートです。' },
        { title: '8〜17は選んで回る', text: '見どころが多くて1日では全部回れません。最初は、無理なく回れる組み合わせ（大河内山荘とモンキーパーク以外）が選ばれています。行かない場所は外し、足したい場所は「行きたい」を押してください。選んだ場所だけが地図の点線でつながります。' },
        { title: '番号をタップ', text: '地図の番号か「一覧」をタップすると、写真・説明・料金・おすすめの時間が見られます。' },
        { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのままルート検索できます。時刻表や公式サイトへのリンクもあります。' }
      ],
      cta: '地図を見る',
      footer1: 'Toshiが実際に歩いて作った、オリジナルマップです。'
    }
  },
  en: {
    htmlLang: 'en',
    docTitle: 'Arashiyama & Sagano, Kyoto | Arashiyama MAP',
    titleMain: 'Arashiyama & Sagano',
    titleSub: '京都 嵐山・嵯峨野',
    howto: 'How to use',
    allMaps: '← All maps',
    home: 'All maps',
    tabMap: 'Map',
    menu: 'Menu',
    list: 'Spots',
    listHead: 'All spots',
    listNote: 'Spots 1–7 (bus up to Otagi Nenbutsu-ji, then walk downhill to Adashino) are for everyone. In 8–17, a set that fits comfortably into one day is already chosen for you. Visit them in number order. The dotted line shows the order, not the actual path.',
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
    credit: 'Photos &amp; text: Toshi (some Monkey Park photos are from Wikimedia Commons; the author and license are shown on each photo)<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors',
    photoBy: 'Photo: ',
    loadError: 'Could not load the map data. Please reload.',
    hours: 'Hours',
    fee: 'Fee',
    closed: 'Closed',
    cash: 'Bring cash',
    checked: 'Checked on the official website on {d}. Details can change, so please check before you go.',
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
    pickNote: 'Tap “Going” to drop a place, or “Want to go” to add one. Spots 1–7 (train and bus up to Otagi Nenbutsu-ji, then downhill to Adashino) and the way home (18) are the same for everyone. Times assume the places chosen at the start and the 9:44 bus. Adding Okochi Sanso or the Monkey Park means dropping something else.',
    pickCount: '{n} places chosen · {t} stops in your route (incl. the shared ones)',
    pickEmpty: 'Nothing chosen yet. Pick the places you want from 8–17 in the list below.',
    pickAll: 'Choose all',
    pickNone: 'Clear all',
    pickOff: 'Want to go',
    pickOn: 'Going',
    autoTag: 'Everyone',
    autoOff: 'Not on your route',
    seasonHead: 'Possibly seasonal',
    hintHead: 'On your route',
    intro: {
      kicker: 'A day trip, hand-walked by Toshi',
      h1: 'From a mountain temple down to the bamboo grove and Togetsukyo: Arashiyama, all downhill.',
      lead: 'Take the bus up to Otagi Nenbutsu-ji, a temple in the hills of Sagano. From there you simply walk downhill along an old street. Moss temples, the bamboo grove, Tenryu-ji’s garden, Togetsukyo Bridge: pick the places you like on your way down to central Arashiyama.',
      favLabel: 'Don’t miss',
      favName: 'Otagi Nenbutsu-ji',
      favText: '1,200 stone rakan, each with its own face.',
      favPhoto: [5, 0],
      whoHead: 'Who it’s for',
      who: [
        'For both the famous sights of Arashiyama and quiet, hidden Sagano',
        'Leave Kyoto-kawaramachi Station at about 9:00; about 30 min to Arashiyama by Hankyu train',
        'Ride a bus up the hill first, then it’s almost all downhill on foot',
        'In the second half, pick the temples and sights you want to see',
        'About 6 km on foot if you see everything. Wear comfy shoes',
        'Otagi Nenbutsu-ji is closed on Wednesdays and Saturdays',
        'Few places to eat in Oku-Saga: bring bread or rice balls to be safe',
        'Bring cash for temple admissions. The Monkey Park is cash only'
      ],
      dayHead: 'One day, roughly like this',
      from: 'From',
      day: [
        { time: '9:00', area: 'Kawaramachi → Arashiyama', title: 'Hankyu train to Arashiyama', text: 'About 30 minutes from Kyoto-kawaramachi, changing at Katsura.', note: 'Slow morning? Leave at about 10:00 for the 10:44 bus', photo: [3, 0] },
        { time: '9:44', area: 'Otagi → Adashino', title: 'Bus up the hill, then walk down', text: 'The bus reaches Otagidera-mae at 10:01. See the stone rakan, have a dumpling at the teahouse in Toriimoto, then walk down to Adashino Nenbutsu-ji.', note: 'One bus an hour on weekdays and Saturdays', badge: 'Everyone does this part', photo: [5, 1] },
        { time: '12:15', area: 'Around Adashino', title: 'Lunch', text: 'There are few places to eat here. Eat where you find one open, or have the bread or rice balls you brought.', note: 'The next place for a meal is Sagano-yu, at about 16:30', photo: [6, 0] },
        { time: '13:10', area: 'Oku-Saga', title: 'Moss temples: take your pick', text: 'Gio-ji, Nison-in, Jojakko-ji, each 5–10 minutes’ walk apart. You don’t have to see all three.', note: 'Adding Okochi Sanso makes the rest 40 min later', badge: 'Pick what you like', photo: [8, 0] },
        { time: '15:05', area: 'Bamboo → Tenryu-ji', title: 'Bamboo grove & Zen garden', text: 'Walk the bamboo path to Nonomiya Shrine, then enter Tenryu-ji by the north gate for its pond garden.', note: 'Tenryu-ji garden: last entry 16:50', photo: [12, 0] },
        { time: '16:30', area: 'Central Arashiyama', title: 'Bathhouse café & Togetsukyo', text: 'Rest in a café in an old public bath, then on to the bridge. From November to January it’s dark by the time you get there.', note: 'Monkey Park: last entry 16:00, cash only. Pick just one temple that day', photo: [16, 0] },
        { time: '17:50', area: 'Back downtown', title: 'Pontocho in the evening', text: 'The Hankyu train gets you back to Kyoto-kawaramachi at about 18:20: dinner in Pontocho.', photo: [18, 0] }
      ],
      timeSuffix: '',
      dealsHead: 'Getting around: fares',
      dealsLead: 'From Kyoto-kawaramachi and back, trains and the bus cost ¥710 per adult (temple admission not included).',
      deals: [
        { name: 'Hankyu train (Kyoto-kawaramachi → Arashiyama)', price: '¥240', text: 'Change at Katsura for the Arashiyama Line. IC cards accepted.', url: 'https://www.hankyu.co.jp/station/kawaramachi.html' },
        { name: 'Kyoto Bus 92 / 94 (Hankyu Arashiyama-ekimae → Otagidera-mae)', price: '¥230', text: 'Bound for Kiyotaki. One bus an hour on weekdays and Saturdays (9:44, 10:44); on Sunday and holiday mornings 9:14, 9:44, 10:14 and 10:44. With an IC card, tap when you get off.', url: 'https://www.kyotobus.jp/route/timetable/schedule.html?stop_id=421_3' },
        { name: 'Hankyu train (Arashiyama → Kyoto-kawaramachi)', price: '¥240', text: 'Change at Katsura again on the way back.', url: 'https://www.hankyu.co.jp/station/arashiyama.html' }
      ],
      dealsNote: 'Adult single fares, checked on the Hankyu and Kyoto Bus official websites on Nov 20, 2026. The Subway & Bus One-day Pass doesn’t cover Hankyu trains, so it doesn’t save money on this route.',
      dealsMore: 'See official site',
      howHead: 'How to use this map',
      how: [
        { title: 'Spots 1–7 in order', text: 'Train and bus from Kyoto-kawaramachi up to Otagi Nenbutsu-ji, then walk downhill to Adashino Nenbutsu-ji. Everyone follows this part.' },
        { title: 'Pick from 8–17', text: 'There’s too much to see in one day. A set that fits comfortably (everything except Okochi Sanso and the Monkey Park) is chosen to start with. Drop the places you don’t want and tap “Want to go” to add others. Your chosen stops are joined by the dotted line on the map.' },
        { title: 'Tap a number', text: 'Tap a number on the map, or open the list, to see photos, tips, fees and suggested times.' },
        { title: 'Get directions', text: 'Use “Open in Google Maps” at each spot for directions. Some spots also link to timetables and official websites.' }
      ],
      cta: 'Open the map',
      footer1: 'An original map, hand-walked by Toshi.'
    }
  }
};

/* コース（出発のしかた）の切り替え。2026年11月22日に追加。
   一覧の上のボタンで3つから選ぶ：early＝早朝に出発・愛宕念仏寺の開門へ（日・月・火・木・金）／
   tenryuji＝早朝に出発・天龍寺の開門へ（水・土＝愛宕念仏寺が休みの日）／late＝9〜10時に出発（これまでの内容）。
   コースごとにデータファイルが別（scripts/build_arashiyama_courses.py が作る）。
   courseFor[コース] に書いた文言で上の文言を上書きする（intro は項目ごとに上書き。app.js が読み込むときに行う）。
   day の並びは、データの sections の day（何番目か）と合わせてある（build_arashiyama_courses.py の SECTIONS）。
   写真は [スポットの id, 写真の番号]。時刻は公式サイトと乗換案内で2026年11月22日に確認（出典はデータの sources）。 */
(function () {
  var J = window.ARASHIYAMA_I18N.ja, E = window.ARASHIYAMA_I18N.en;

  J.swCourse = '出発のしかた（愛宕念仏寺は水・土がお休み）';
  J.courseAria = '出発のしかた';
  J.courseEarly = '早朝に出発：愛宕念仏寺の開門へ（日・月・火・木・金）';
  J.courseTenryuji = '早朝に出発：天龍寺の開門へ（水・土）';
  J.courseLate = '9〜10時に出発';
  E.swCourse = 'When you start (Otagi Nenbutsu-ji is closed Wed & Sat)';
  E.courseAria = 'When you start';
  E.courseEarly = 'Early start: Otagi Nenbutsu-ji at opening (Sun, Mon, Tue, Thu, Fri)';
  E.courseTenryuji = 'Early start: Tenryu-ji at opening (Wed & Sat)';
  E.courseLate = 'Leave at 9–10 am';

  var jd = J.intro.day, ed = E.intro.day;
  function day(base, o) { var r = {}, k; for (k in base) r[k] = base[k]; for (k in o) r[k] = o[k]; return r; }
  function ins(list, at, item) { return list.slice(0, at).concat([item], list.slice(at)); }
  var NOTE22_JA = '大人の普通運賃です。2026年11月22日に京都バスの公式サイトと乗換案内で確認しました。「地下鉄・バス1日券」は阪急電車に使えないので、このルートではお得になりません。';
  var NOTE22_EN = 'Adult single fares, checked on the Kyoto Bus website and a route planner on Nov 22, 2026. The Subway & Bus One-day Pass doesn’t cover Hankyu trains, so it doesn’t save money on this route.';

  J.courseFor = {
    late: {
      intro: {
        who: ins(J.intro.who, 2, '京都の中心・三条のあたりからは、京都河原町駅まで歩いて10〜15分')
      }
    },
    early: {
      pickNote: '行かない場所は「行く」を押して外し、足したい場所は「行きたい」を押してください。1〜7（電車とバスで愛宕念仏寺へ行き、坂を下って化野念仏寺まで）と、帰りの18は全員共通です。時間は、最初から選ばれている場所を8:39のバス（日曜・祝日は8:41）で回る場合の目安。大河内山荘とモンキーパークは、足すとほかを減らすことになります。',
      intro: {
        lead: 'バスで奥嵯峨の山の上にある愛宕念仏寺へ。9:00の開門に合わせて着く、早起きのコースです。そこからは昔ながらの町並みを、坂道に沿って歩いて下るだけ。苔のお寺、竹林、天龍寺の庭、渡月橋まで、行きたい場所を選びながら嵐山の中心へ向かいます。',
        who: [
          '愛宕念仏寺が開いている日（日・月・火・木・金）に、開門に合わせて行きたい人に',
          '水曜・土曜は愛宕念仏寺がお休み。一覧の上のボタンで「天龍寺の開門へ」に切り替え',
          'スタートは京都河原町駅を平日7:50、日曜・祝日7:45。三条のあたりからは駅まで歩いて10〜15分',
          '朝ごはんは出る前に。鳥居本の茶屋でひと休みして、お昼は11時すぎ',
          '最初にバスで山の上へ。あとはほとんど下り坂を歩くだけ',
          '全部回ると歩く距離は約6km。歩きやすい靴で',
          '奥嵯峨は食事の店が少なめ。パンやおにぎりを持っていくと安心',
          '拝観料は現金で用意を。モンキーパークは現金のみ'
        ],
        day: [
          day(jd[0], { time: '7:50', title: '早い電車で嵐山へ', text: '京都河原町から約30分。桂で嵐山線に乗り換えて、8:13に嵐山に着きます。', note: '日曜・祝日は7:45発（8:07着）', photo: ['hankyu', 0] }),
          day(jd[1], { time: '8:39', title: '開門に合わせて、バスで山の上へ', text: '8:50に愛宕寺前に着いて、9:00の開門を待ちます。羅漢さんを見たら、鳥居本の茶屋でひと休みして、化野念仏寺まで下ります。', note: '日曜・祝日は8:41発。乗り遅れると次は平日9:44', photo: ['otagi', 1] }),
          day(jd[2], { time: '11:20', note: '次に食事ができるのは15:35ごろの嵯峨野湯', photo: ['toriimoto', 0] }),
          day(jd[3], { time: '12:15', photo: ['gioji', 0] }),
          day(jd[4], { time: '14:10', photo: ['bamboo', 0] }),
          day(jd[5], { time: '15:35', text: '元銭湯のカフェでひと休みしたら、明るいうちに渡月橋へ。', note: 'モンキーパークは入園16:00まで・現金のみ。行く日は嵯峨野湯を外す', photo: ['togetsukyo', 0] }),
          day(jd[6], { time: '17:10', text: '阪急電車で京都河原町へ戻ると17:40ごろ。先斗町で晩ごはんに。', photo: ['pontocho', 0] })
        ],
        deals: [
          J.intro.deals[0],
          day(J.intro.deals[1], { name: '京都バス 92系統（阪急嵐山駅前→愛宕寺前）', text: '清滝行き。平日は8:39発、日曜・祝日は8:41発に乗ります（次は平日9:44、日曜・祝日9:14）。ICカードは降りるときにタッチ。' }),
          J.intro.deals[2]
        ],
        dealsNote: NOTE22_JA
      }
    },
    tenryuji: {
      listNote: '1〜5（電車で嵐山へ行き、天龍寺と竹林まで）は全員共通。6〜15は、1日で無理なく回れる組み合わせが最初から選ばれています。番号の順に歩いてください。点線は順番を示す線で、実際の道ではありません。',
      pickNote: '行かない場所は「行く」を押して外し、足したい場所は「行きたい」を押してください。1〜5（電車で嵐山へ行き、天龍寺と竹林まで）と、帰りの16は全員共通です。時間は、最初から選ばれている場所を回る場合の目安。大河内山荘・化野念仏寺・鳥居本は、足すとあとの時間が遅くなります。',
      pickEmpty: 'まだ選んでいません。下の一覧の6〜15から、行きたい場所を選んでください。',
      intro: {
        h1: '開門に合わせて天龍寺へ。朝の竹林から、苔のお寺と渡月橋へ。',
        lead: '愛宕念仏寺がお休みの水曜・土曜のための、早起きのコースです。8:30の開門に合わせて天龍寺の庭に入り、北門からそのまま竹林へ。朝ごはんのあとは奥嵯峨の苔のお寺を歩いて、午後は渡月橋とモンキーパークへ。',
        favName: '天龍寺の庭と、朝の竹林',
        favText: '開門に合わせて庭に入り、北門を出ると竹林です。',
        favPhoto: ['tenryuji', 0],
        who: [
          '水曜・土曜（愛宕念仏寺がお休みの日）に、朝早くから嵐山を歩きたい人に',
          'スタートは京都河原町駅を水曜7:50、土曜7:45。三条のあたりからは駅まで歩いて10〜15分',
          '天龍寺の庭園は8:30に開きます。駅から渡月橋を渡って歩いて15〜20分',
          '朝ごはんは、天龍寺と竹林のあと、10時ごろにカフェで',
          '奥嵯峨のお寺は、行きたいところを選んで回る',
          '歩く距離は長め（めやすで8〜9km、モンキーパークの山道を含む）。歩きやすい靴で',
          '拝観料は現金で用意を。モンキーパークは現金のみ'
        ],
        day: [
          day(jd[0], { time: '7:50', title: '早い電車で嵐山へ', text: '京都河原町から約30分。桂で乗り換えて、8:13に嵐山に着きます。朝の渡月橋を渡って、天龍寺まで歩きます。', note: '土曜は7:45発（8:07着）', photo: ['hankyu', 0] }),
          { time: '8:30', area: '天龍寺 → 竹林', title: '開門に合わせて天龍寺、そのまま竹林へ', text: '池の庭を歩いて北門を出ると、そこが竹林の小径。野宮神社までお参りします。', note: '大河内山荘は9:00から。足すと、あとが40分遅くなります', badge: 'ここまでは全員同じルート', photo: ['tenryuji', 0] },
          { time: '9:55', area: '天龍寺の近く', title: '朝ごはん', text: 'カフェ「エスプレッソと」は8:00から開いています（不定休）。ここで朝ごはんにして、ひと休み。', note: '行く日に開いているかは、お店の案内で確かめて', photo: ['nonomiya', 0] },
          { time: '11:00', area: '奥嵯峨', title: '苔と紅葉のお寺を北へ', text: '常寂光寺、二尊院、祇王寺。それぞれ歩いて5〜10分です。祇王寺で折り返します。', note: '化野念仏寺と鳥居本は寄り道。足すとお昼が遅くなります', badge: '好きな場所を選ぶ', photo: ['gioji', 0] },
          { time: '13:15', area: '嵐山の中心', title: 'お昼、渡月橋、モンキーパーク', text: '元銭湯のカフェでお昼にしたら、渡月橋を渡ってモンキーパークへ。', note: 'モンキーパークは入園16:00まで・現金のみ', photo: ['togetsukyo', 0] },
          { time: '16:20', area: '京都の街なかへ', title: 'ひと休みして、夜は先斗町へ', text: '阪急電車で京都河原町へ戻ると17時ごろ。少し休んでから、先斗町で晩ごはんに。', photo: ['pontocho', 0] }
        ],
        dealsLead: '京都河原町から出発して京都河原町へ戻ると、電車で大人1人480円です（拝観料は別）。このコースはバスに乗りません。',
        deals: [J.intro.deals[0], J.intro.deals[2]],
        dealsNote: '大人の普通運賃です。2026年11月22日に乗換案内で確認しました。',
        how: [
          { title: '1〜5は番号の順に', text: '京都河原町から電車で嵐山へ行き、天龍寺と竹林まで。ここまでは全員同じルートです。' },
          { title: '6〜15は選んで回る', text: '最初は、無理なく回れる組み合わせ（大河内山荘・化野念仏寺・鳥居本以外）が選ばれています。行かない場所は外し、足したい場所は「行きたい」を押してください。選んだ場所だけが地図の点線でつながります。' },
          J.intro.how[2], J.intro.how[3]
        ]
      }
    }
  };

  E.courseFor = {
    late: {
      intro: {
        who: ins(E.intro.who, 2, 'From the Sanjo area in central Kyoto, Kyoto-kawaramachi Station is a 10–15 minute walk')
      }
    },
    early: {
      pickNote: 'Tap “Going” to drop a place, or “Want to go” to add one. Spots 1–7 (train and bus up to Otagi Nenbutsu-ji, then downhill to Adashino) and the way home (18) are the same for everyone. Times assume the places chosen at the start and the 8:39 bus (8:41 on Sundays and holidays). Adding Okochi Sanso or the Monkey Park means dropping something else.',
      intro: {
        lead: 'Take the bus up to Otagi Nenbutsu-ji, a temple in the hills of Sagano. This is the early course: you arrive as it opens at 9:00. From there you simply walk downhill along an old street. Moss temples, the bamboo grove, Tenryu-ji’s garden, Togetsukyo Bridge: pick the places you like on your way down to central Arashiyama.',
        who: [
          'For days when Otagi Nenbutsu-ji is open (Sun, Mon, Tue, Thu, Fri) and you want to be there as it opens',
          'It’s closed on Wednesdays and Saturdays: switch to “Tenryu-ji at opening” with the buttons at the top of the list',
          'Leave Kyoto-kawaramachi Station at 7:50 on weekdays, 7:45 on Sundays and holidays; the station is 10–15 minutes on foot from the Sanjo area',
          'Have breakfast before you leave. Rest at the teahouse in Toriimoto; lunch is soon after 11:00',
          'Ride a bus up the hill first, then it’s almost all downhill on foot',
          'About 6 km on foot if you see everything. Wear comfy shoes',
          'Few places to eat in Oku-Saga: bring bread or rice balls to be safe',
          'Bring cash for temple admissions. The Monkey Park is cash only'
        ],
        day: [
          day(ed[0], { time: '7:50', title: 'An early train to Arashiyama', text: 'About 30 minutes from Kyoto-kawaramachi, changing at Katsura. You reach Arashiyama at 8:13.', note: 'Sundays and holidays: leave at 7:45 (arrive 8:07)', photo: ['hankyu', 0] }),
          day(ed[1], { time: '8:39', title: 'Bus up the hill for the opening', text: 'The bus reaches Otagidera-mae at 8:50; wait for the gate to open at 9:00. See the stone rakan, rest at the teahouse in Toriimoto, then walk down to Adashino Nenbutsu-ji.', note: 'Sundays and holidays: 8:41. Miss it and the next is 9:44 on weekdays', photo: ['otagi', 1] }),
          day(ed[2], { time: '11:20', note: 'The next place for a meal is Sagano-yu, at about 15:35', photo: ['toriimoto', 0] }),
          day(ed[3], { time: '12:15', photo: ['gioji', 0] }),
          day(ed[4], { time: '14:10', photo: ['bamboo', 0] }),
          day(ed[5], { time: '15:35', text: 'Rest in a café in an old public bath, then on to the bridge while it’s still light.', note: 'Monkey Park: last entry 16:00, cash only. Skip Sagano-yu that day', photo: ['togetsukyo', 0] }),
          day(ed[6], { time: '17:10', text: 'The Hankyu train gets you back to Kyoto-kawaramachi at about 17:40: dinner in Pontocho.', photo: ['pontocho', 0] })
        ],
        deals: [
          E.intro.deals[0],
          day(E.intro.deals[1], { name: 'Kyoto Bus 92 (Hankyu Arashiyama-ekimae → Otagidera-mae)', text: 'Bound for Kiyotaki. Take the 8:39 on weekdays or the 8:41 on Sundays and holidays (next: 9:44 on weekdays, 9:14 on Sundays and holidays). With an IC card, tap when you get off.' }),
          E.intro.deals[2]
        ],
        dealsNote: NOTE22_EN
      }
    },
    tenryuji: {
      listNote: 'Spots 1–5 (train to Arashiyama, then Tenryu-ji and the bamboo grove) are for everyone. In 6–15, a set that fits comfortably into one day is already chosen for you. Visit them in number order. The dotted line shows the order, not the actual path.',
      pickNote: 'Tap “Going” to drop a place, or “Want to go” to add one. Spots 1–5 (train to Arashiyama, then Tenryu-ji and the bamboo grove) and the way home (16) are the same for everyone. Times assume the places chosen at the start. Adding Okochi Sanso, Adashino or Toriimoto makes everything after it later.',
      pickEmpty: 'Nothing chosen yet. Pick the places you want from 6–15 in the list below.',
      intro: {
        h1: 'Tenryu-ji as it opens, then the bamboo grove in the morning, moss temples and Togetsukyo.',
        lead: 'An early course for Wednesdays and Saturdays, when Otagi Nenbutsu-ji is closed. Walk into Tenryu-ji’s garden as it opens at 8:30 and leave by the north gate, straight into the bamboo grove. After breakfast, walk the moss temples of Oku-Saga; in the afternoon, Togetsukyo Bridge and the Monkey Park.',
        favName: 'Tenryu-ji’s garden and the morning bamboo',
        favText: 'Go in as the garden opens; the north gate leads straight into the bamboo.',
        favPhoto: ['tenryuji', 0],
        who: [
          'For an early walk around Arashiyama on a Wednesday or Saturday, when Otagi Nenbutsu-ji is closed',
          'Leave Kyoto-kawaramachi Station at 7:50 on Wednesdays, 7:45 on Saturdays; the station is 10–15 minutes on foot from the Sanjo area',
          'Tenryu-ji’s garden opens at 8:30. It’s a 15–20 minute walk from the station, across Togetsukyo Bridge',
          'Breakfast is at a café at about 10:00, after Tenryu-ji and the bamboo grove',
          'In Oku-Saga, pick the temples you want to see',
          'A long walk (roughly 8–9 km, including the Monkey Park hill). Wear comfy shoes',
          'Bring cash for temple admissions. The Monkey Park is cash only'
        ],
        day: [
          day(ed[0], { time: '7:50', title: 'An early train to Arashiyama', text: 'About 30 minutes from Kyoto-kawaramachi, changing at Katsura; you reach Arashiyama at 8:13. Walk across Togetsukyo Bridge to Tenryu-ji.', note: 'Saturdays: leave at 7:45 (arrive 8:07)', photo: ['hankyu', 0] }),
          { time: '8:30', area: 'Tenryu-ji → Bamboo', title: 'Tenryu-ji at opening, then the bamboo', text: 'Walk round the pond garden and leave by the north gate, straight onto the bamboo path. Carry on to Nonomiya Shrine.', note: 'Okochi Sanso opens at 9:00; adding it makes the rest 40 min later', badge: 'Everyone does this part', photo: ['tenryuji', 0] },
          { time: '9:55', area: 'Near Tenryu-ji', title: 'Breakfast', text: 'The café “Espresso to” opens at 8:00 (irregular closing days). Have breakfast and a rest here.', note: 'Check that it’s open on the day', photo: ['nonomiya', 0] },
          { time: '11:00', area: 'Oku-Saga', title: 'Moss temples, heading north', text: 'Jojakko-ji, Nison-in, Gio-ji, each 5–10 minutes’ walk apart. Turn round at Gio-ji.', note: 'Adashino and Toriimoto are extras: adding them makes lunch later', badge: 'Pick what you like', photo: ['gioji', 0] },
          { time: '13:15', area: 'Central Arashiyama', title: 'Lunch, Togetsukyo, Monkey Park', text: 'Have lunch at the café in an old public bath, then cross the bridge to the Monkey Park.', note: 'Monkey Park: last entry 16:00, cash only', photo: ['togetsukyo', 0] },
          { time: '16:20', area: 'Back downtown', title: 'A rest, then Pontocho', text: 'The Hankyu train gets you back to Kyoto-kawaramachi at about 17:00. Rest a little, then dinner in Pontocho.', photo: ['pontocho', 0] }
        ],
        dealsLead: 'From Kyoto-kawaramachi and back, the trains cost ¥480 per adult (temple admission not included). This course doesn’t use the bus.',
        deals: [E.intro.deals[0], E.intro.deals[2]],
        dealsNote: 'Adult single fares, checked with a route planner on Nov 22, 2026.',
        how: [
          { title: 'Spots 1–5 in order', text: 'Train from Kyoto-kawaramachi to Arashiyama, then Tenryu-ji and the bamboo grove. Everyone follows this part.' },
          { title: 'Pick from 6–15', text: 'A set that fits comfortably (everything except Okochi Sanso, Adashino and Toriimoto) is chosen to start with. Drop the places you don’t want and tap “Want to go” to add others. Your chosen stops are joined by the dotted line on the map.' },
          E.intro.how[2], E.intro.how[3]
        ]
      }
    }
  };

  // 使い方のいちばん上に、コースの選び方を足す（どのコースでも）
  var HOW = {
    ja: { title: '出発のしかたを選ぶ', text: '一覧の上のボタンで、3つのコースから選べます。早朝に出て愛宕念仏寺の開門（9:00）へ行くコース（日・月・火・木・金）、早朝に出て天龍寺の開門（8:30）へ行くコース（愛宕念仏寺がお休みの水・土）、9〜10時に出発するコース。いま開いているのは「{c}」です。' },
    en: { title: 'Choose when you start', text: 'The buttons at the top of the list switch between three courses: an early start for the 9:00 opening of Otagi Nenbutsu-ji (Sun, Mon, Tue, Thu, Fri), an early start for the 8:30 opening of Tenryu-ji (Wed and Sat, when Otagi Nenbutsu-ji is closed), and a 9–10 am start. You are looking at “{c}”.' }
  };
  var NAME = { early: 'courseEarly', tenryuji: 'courseTenryuji', late: 'courseLate' };
  [['ja', J], ['en', E]].forEach(function (x) {
    var l = x[0], t = x[1];
    Object.keys(NAME).forEach(function (id) {
      var o = t.courseFor[id].intro;
      o.how = [{ title: HOW[l].title, text: HOW[l].text.replace('{c}', t[NAME[id]]) }].concat(o.how || t.intro.how);
    });
  });
})();
