/* 2026年11月24日（火）の箕面マップ。i18n.js の文言のうち、今日用に変えるところを上書きする。
   「使い方」のページ（intro）を、きょうのしおりにする。app.js の renderIntro が x.blocks の順に組み立てる。 */
(function () {
  var I = window.MINOH_I18N;

  /* ---------- 日本語 ---------- */
  var ja = I.ja;
  ja.docTitle = '箕面 旅のしおり｜2026年11月24日';
  ja.titleMain = '箕面 旅のしおり';
  ja.titleSub = '11月24日（火）';
  ja.howto = 'しおり';
  ja.credit = '写真：トシ<br>地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors';
  ja.spot1Howto = 'きょうのしおりを見る';
  ja.listHead = 'きょうのルート';
  ja.listNote = '番号の順にめぐる、きょう（11月24日・火曜）の流れです。時間はYahoo!路線情報で11/24のダイヤを調べて決めました。点線は順番を示す線で、実際の道ではありません。';
  ja.checkedDate = '2026年11月20日〜24日';
  ja.intro = {
    kicker: '2026年11月24日（火）・平日ダイヤ',
    h1: '箕面 旅のしおり',
    lead: 'でんでん・タロちゃん・トシの3人で。勝尾寺でダルマ、森の山道を歩いて箕面大滝のライトアップ、締めは海鮮の晩ごはんと箕面ビール。',
    favLabel: 'いちばんの見どころ',
    favName: '勝尾寺',
    favText: 'お寺じゅうに、小さな赤い「勝ちダルマ」。',
    favPhoto: ['katsuoji', 0],
    members: ['でんでん', 'タロちゃん', 'トシ'],
    keysHead: 'きょうのポイント',
    keys: [
      { tone: 'ok', badge: '間に合う', title: '勝尾寺の受付には余裕あり', text: '13:52に着いて、受付の締め切りは16:30（平日は17:00に閉まる）。最終バス（萱野15:00発→15:22着）でも入れます。' },
      { tone: 'warn', badge: '要注意', title: '山道は明るいうちに。勝尾寺は15:00に出る', text: 'きょうの日の入りは16:49。勝尾寺〜杉の茶屋の山道はライトアップされない区間です。15:20までに出られなければ、山道はやめて下の「プランB」へ。' },
      { tone: 'night', badge: '夜もOK', title: '滝と滝道はライトアップ中', text: 'もみじまつり（11/14〜12/6）は毎日、日没〜21:30。17時をすぎて滝にいても大丈夫です。' }
    ],
    koyoHead: '紅葉のようす（ウェザーニュース）',
    koyo: [
      { name: '勝尾寺', level: '見頃', detail: '7〜8割色づき・11月23日時点', fall: '落葉はじめ 12月7日ごろ〜（予想）', quote: '「青空に赤いもみじが映えてとてもきれいでした」（11月22日の投稿）', url: 'https://weathernews.jp/koyo/spot/26222/' },
      { name: '箕面公園', level: '見頃', detail: '7〜8割色づき・11月20日時点', fall: '落葉はじめ 12月5日ごろ〜（予想）', quote: '「想像を超えて綺麗でした。滝道散策も楽しかった」（11月23日の投稿）', url: 'https://weathernews.jp/koyo/spot/26202/' }
    ],
    koyoNote: '11月24日に確認。きょうの発表はまだなので、いちばん新しい情報です。',
    koyoMore: 'ウェザーニュースで見る',
    dayHead: '1日の流れ',
    timeSuffix: '',
    day: [
      { time: '12:02', area: '阪急 烏丸', title: '特急で大阪方面へ', text: '2号線から大阪梅田行きの特急。12:33 淡路で普通に乗りかえて12:39 南方。歩いて約4分の西中島南方へ。', note: 'ICカードで' },
      { time: '12:50', area: '西中島南方', title: '御堂筋線で箕面萱野へ', text: '箕面萱野行きで乗りかえなし。13:11に着いたら、駅前の8番のりばへ。', photo: ['kayano', 0] },
      { time: '13:30', area: '箕面萱野', title: 'バスで山の上のお寺へ', text: '阪急バス30系統の直行バスで約22分、13:52 勝尾寺着。大人800円。乗り遅れたら14:00発。', note: '現金不可・ICカードで', photo: ['bus', 0] },
      { time: '13:55', area: '勝尾寺', title: 'ダルマだらけのお寺', text: '山門、池、多宝塔。境内のあちこちに小さな赤いダルマ。入山料500円。トイレはここで。', note: '受付は16:30まで', photo: ['katsuoji', 1] },
      { time: '15:00', area: '森の山道', title: '明るいうちに森を歩いて滝へ', text: 'ビジターセンター（きょうは火曜で休館）まで約40分、もみじ広場で10分休んで、杉の茶屋まで約30分。', badge: 'ハイキングあり', note: '遅くても15:20に出発', photo: ['visitor', 2] },
      { time: '16:25', area: '箕面大滝', title: '明るい滝と、灯りのついた滝', text: '16:49の日の入りからライトアップ。17:15ごろまでゆっくり。野生のサルに食べ物を見せないで。', note: 'ライトアップ 日没〜21:30', photo: ['falls', 2] },
      { time: '17:15', area: '滝道', title: 'ライトアップの滝道を下る', text: '川ぞいの道を約40分。滝道ぞい・瀧安寺・西江寺も灯りがともります。18:05ごろ箕面駅。', photo: ['minoh-st', 4] },
      { time: '18:10', area: '箕面', title: '海鮮処 ぎょぎょぎょで晩ごはん', text: '箕面駅から南へ歩いて約5分。お魚ひとすじの和食店。刺身の盛り合わせに、もう一品の魚を煮る・揚げる・焼くから選べる定食が人気。19:15ごろまで。', note: '夜17:00〜・L.O.21:00・水曜休', photo: ['gyogyo', 0] },
      { time: '19:35', area: '牧落', title: '箕面ビールで乾杯', text: 'ぎょぎょぎょから歩いて約15〜20分。平日は21:00まで（ラストオーダー20:30）。W-IPAと名物のスタウトを。20:15ごろお店を出る。', photo: ['beer', 1] },
      { time: '20:30', area: '牧落 → 烏丸', title: '阪急で京都へ', text: '石橋阪大前 20:40発の急行 → 十三 20:53発の準特急 → 21:33 烏丸着。1本遅れたら20:39発（21:43着）、20:52発（21:55着）。', photo: ['makiochi', 2] }
    ],
    planHead: '予定がずれたら',
    plans: [
      { title: '烏丸 12:02 に乗れなかった', sub: '次の特急でも勝尾寺には間に合います', html: '<p><b>12:22 烏丸発の特急</b>で高槻市へ、準急に乗りかえて南茨木 → 大阪モノレール → 千里中央で北大阪急行 → <b>13:19 箕面萱野着</b>。13:30のバスまで11分なので、8番のりばへ急いで。</p><p>間に合わなければ<b>14:00発</b>のバス（14:22 勝尾寺着）。勝尾寺は40〜50分にして、<b>15:15ごろには歩きはじめて</b>ください。</p>' },
      { title: 'プランB：山道を歩かない', sub: '勝尾寺を15:20までに出られない・雨・疲れたとき', html: '<p>勝尾寺からバスで下りて、箕面駅から<b>ライトアップの滝道を上って</b>滝へ。滝道は明るく、人もいます。</p><ul><li><b>16:20</b> 勝尾寺発のバス（30系統・800円）→ 16:41 箕面萱野。勝尾寺発はほかに15:50、16:50、最終17:05。</li><li><b>17:00</b> 箕面萱野発（36系統・250円）→ 17:15 阪急箕面駅。15:50のバスなら16:30発（21系統）→ 16:45。</li><li><b>17:15</b> 滝道を上って約45分。18:00ごろ灯りのついた滝へ。</li><li><b>18:20</b> 下って19:00ごろ箕面駅 → 歩いて約5分のぎょぎょぎょで晩ごはん（ラストオーダー21:00）。箕面ビールはラストオーダー20:30なので、間に合わなければ晩ごはんのあと箕面駅から帰ります（石橋阪大前・十三で乗りかえ）。</li></ul><p class="sh-small">バス代が1人1,050円ふえます。</p>' },
      { title: '箕面ビールに入れなかった', sub: '帰りの電車はゆっくりでも大丈夫', html: '<p>牧落から烏丸へは 21:33発（22:43着）、21:45発（22:53着）、21:57発（23:05着）もあります。</p>' }
    ],
    whoHead: '持ち物',
    who: [
      '交通系ICカード（ICOCAなど）に1人2,200円以上。勝尾寺行きのバスは現金不可、車内でチャージもできません',
      '現金も少し（勝尾寺の入山料500円、晩ごはん用）',
      '晩ごはんのぎょぎょぎょは小さなお店。先に電話（070-1741-0804）で3人分を予約しておくと安心',
      '歩きやすい靴。山道は約1時間10分（ほとんど下り）',
      '上着。夕方の山と滝は冷えます',
      'スマホの充電・モバイルバッテリー。夜の滝道で写真を撮るとすぐ減ります'
    ],
    dealsHead: '交通費のめやす（1人・ICカード）',
    dealsLead: '合計 2,170円（勝尾寺の入山料500円は別）。',
    deals: [
      { name: '烏丸 → 箕面萱野（阪急・御堂筋線）', price: '890円', text: '淡路・南方で乗りかえ、西中島南方から御堂筋線。' },
      { name: '箕面萱野 → 勝尾寺（阪急バス）', price: '800円', text: '2026年10月から現金不可。ICカードかクレジットカードで買う専用乗車券。', url: 'https://www.hankyubus.co.jp/news/2026101.html' },
      { name: '牧落 → 烏丸（阪急）', price: '480円', text: '石橋阪大前・十三で乗りかえ。' }
    ],
    dealsMore: '公式サイトで見る',
    dealsNote: '',
    srcHead: '確かめたこと',
    src: [
      '電車・バスの時刻：<a href="https://transit.yahoo.co.jp/" target="_blank" rel="noopener">Yahoo!路線情報</a>で「2026年11月24日（火）」を指定して検索。',
      '勝尾寺の時間（平日8:00〜17:00、受付は閉まる30分前まで）・入山料：11月20日に<a href="https://katsuo-ji-temple.or.jp/access/" target="_blank" rel="noopener">公式サイト</a>で確認（電話 072-721-7010）。',
      '滝のライトアップ：<a href="https://www.mino-park.jp/event/art/1087/" target="_blank" rel="noopener">箕面公園「2026秋のライトアップ」</a>（11/14〜12/6 毎日、日没〜21:30）',
      '日の入り 16:49（大阪）：<a href="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s2711.html" target="_blank" rel="noopener">国立天文台 暦計算室</a>',
      'ビジターセンターは火曜休館：<a href="https://minohkankou.net/sights/319/" target="_blank" rel="noopener">箕面市観光協会</a>',
      '箕面ビールの営業時間：<a href="https://www.minoh-beer.jp/store/" target="_blank" rel="noopener">箕面ビール 店舗案内</a>',
      '晩ごはんの海鮮処 ぎょぎょぎょ：<a href="https://news.minoh.net/chiisanaomiseouen/%E6%B5%B7%E9%AE%AE%E5%87%A6%E3%80%80%E9%B1%BB%E3%80%80%E3%81%8E%E3%82%87%E3%81%8E%E3%82%87%E3%81%8E%E3%82%87/" target="_blank" rel="noopener">みのおどっとねっと</a>（2024年8月の案内：夜17:00〜21:00 L.O.、水曜休）',
      '紅葉：ウェザーニュース「<a href="https://weathernews.jp/koyo/spot/26222/" target="_blank" rel="noopener">勝尾寺</a>」「<a href="https://weathernews.jp/koyo/spot/26202/" target="_blank" rel="noopener">明治の森箕面国定公園</a>」'
    ],
    howHead: 'このマップの使い方',
    how: [
      { title: '番号の順にめぐる', text: '1〜10の番号が、きょう回る順番です。' },
      { title: '番号をタップ', text: '地図の番号か「一覧」をタップすると、写真・説明・きょうの時間が見られます。' },
      { title: '行ったら印を付ける', text: 'スポットの「行ったら印を付ける」で、どこまで来たかがわかります。' },
      { title: 'Googleマップでルート検索', text: '各スポットの「Googleマップで開く」から、そのまま道案内できます。' }
    ],
    cta: '地図を見る',
    footer1: 'でんでん・タロちゃん・トシの箕面旅行のしおりです。遅れや運休は当日の運行情報で確認してください。雨の日は山道がすべりやすいので、プランBがおすすめです。'
  };

  /* ---------- English ---------- */
  var en = I.en;
  en.docTitle = 'Minoh trip plan | Nov 24, 2026';
  en.titleMain = 'Minoh trip plan';
  en.titleSub = 'Tue, Nov 24';
  en.howto = 'Plan';
  en.credit = 'Photos: Toshi<br>Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors';
  en.spot1Howto = 'See today’s plan';
  en.listHead = 'Today’s route';
  en.listNote = 'Follow the numbers: this is our plan for today, Tuesday Nov 24. Times come from Yahoo! Transit for the Nov 24 timetable. The dotted line shows the order, not the actual path.';
  en.intro = {
    kicker: 'Tuesday, Nov 24, 2026 · weekday timetable',
    h1: 'Minoh trip plan',
    lead: 'Denden, Taro-chan and Toshi. Daruma at Katsuoji, a forest walk to Minoh Falls lit up at dusk, then a seafood dinner and Minoh Beer.',
    favLabel: 'Don’t miss',
    favName: 'Katsuoji',
    favText: 'Little red “winning daruma” all over the temple.',
    favPhoto: ['katsuoji', 0],
    members: ['Denden', 'Taro-chan', 'Toshi'],
    keysHead: 'Today in three lines',
    keys: [
      { tone: 'ok', badge: 'On time', title: 'Plenty of time for Katsuoji', text: 'We arrive at 13:52; last entry is 16:30 (it closes at 17:00 on weekdays). Even the last bus up (15:00, arr. 15:22) makes it.' },
      { tone: 'warn', badge: 'Careful', title: 'Walk the forest in daylight: leave Katsuoji at 15:00', text: 'Sunset is 16:49 and the trail from Katsuoji to Sugi no Chaya is not lit. If we can’t leave by 15:20, skip the trail and use Plan B below.' },
      { tone: 'night', badge: 'After dark', title: 'The falls and the river path are lit up', text: 'Momiji festival (Nov 14 – Dec 6): every evening, sunset to 21:30. Being at the falls after 17:00 is fine.' }
    ],
    koyoHead: 'Autumn leaves (Weathernews)',
    koyo: [
      { name: 'Katsuoji', level: 'At their best', detail: '70–80% turned · as of Nov 23', fall: 'Leaves start falling about Dec 7 (forecast)', quote: '“Red maples against a blue sky, really beautiful.” (post on Nov 22)', url: 'https://weathernews.jp/koyo/spot/26222/' },
      { name: 'Minoh Park', level: 'At their best', detail: '70–80% turned · as of Nov 20', fall: 'Leaves start falling about Dec 5 (forecast)', quote: '“More beautiful than I imagined, and the river path was fun.” (post on Nov 23)', url: 'https://weathernews.jp/koyo/spot/26202/' }
    ],
    koyoNote: 'Checked on Nov 24. Today’s update isn’t out yet, so this is the latest.',
    koyoMore: 'See on Weathernews (Japanese)',
    dayHead: 'The day',
    timeSuffix: '',
    day: [
      { time: '12:02', area: 'Hankyu Karasuma', title: 'Limited express toward Osaka', text: 'Platform 2, for Osaka-umeda. Change at Awaji (12:33) to a local for Minamikata (12:39), then walk about 4 minutes to Nishinakajima-Minamigata.', note: 'Use an IC card' },
      { time: '12:50', area: 'Nishinakajima-Minamigata', title: 'Midosuji Line to Minoh-Kayano', text: 'No change needed. Arrive 13:11 and go to bus stand 8.', photo: ['kayano', 0] },
      { time: '13:30', area: 'Minoh-Kayano', title: 'Bus up to the temple', text: 'Hankyu Bus route 30, direct, 22 minutes: Katsuoji 13:52. ¥800. Next bus 14:00.', note: 'No cash: IC card', photo: ['bus', 0] },
      { time: '13:55', area: 'Katsuoji', title: 'A temple full of daruma', text: 'Gate, pond and pagoda, with little red daruma everywhere. Admission ¥500. Use the toilets here.', note: 'Last entry 16:30', photo: ['katsuoji', 1] },
      { time: '15:00', area: 'Forest walk', title: 'Walk the forest in daylight', text: 'About 40 minutes to the Visitor Center (closed on Tuesdays), a 10-minute rest, then about 30 minutes to Sugi no Chaya.', badge: 'Includes a hike', note: 'Leave by 15:20 at the latest', photo: ['visitor', 2] },
      { time: '16:25', area: 'Minoh Falls', title: 'The falls by day and lit up', text: 'Lights come on at sunset (16:49). Stay until about 17:15. Don’t show food to the wild monkeys.', note: 'Lit sunset–21:30', photo: ['falls', 2] },
      { time: '17:15', area: 'Takimichi', title: 'Down the lit riverside path', text: 'About 40 minutes. The path, Ryuanji and Saikoji are lit. Minoh Station at about 18:05.', photo: ['minoh-st', 4] },
      { time: '18:10', area: 'Minoh', title: 'Seafood dinner at Gyogyogyo', text: 'About 5 minutes south of Minoh Station. A small restaurant all about fish: try the set with a sashimi platter plus one more fish, simmered, fried or grilled. Until about 19:15.', note: 'From 17:00 · last order 21:00 · closed Wed', photo: ['gyogyo', 0] },
      { time: '19:35', area: 'Makiochi', title: 'Cheers at Minoh Beer', text: 'About 15–20 minutes on foot from Gyogyogyo. Open until 21:00 on weekdays (last order 20:30). Try the W-IPA and the famous Stout. Leave at about 20:15.', photo: ['beer', 1] },
      { time: '20:30', area: 'Makiochi → Karasuma', title: 'Hankyu back to Kyoto', text: '20:40 express from Ishibashi Handai-mae → 20:53 semi-limited express from Juso → Karasuma 21:33. Later trains: 20:39 (arr. 21:43), 20:52 (arr. 21:55).', photo: ['makiochi', 2] }
    ],
    planHead: 'If plans change',
    plans: [
      { title: 'Missed the 12:02 from Karasuma', sub: 'The next limited express still works', html: '<p>Take the <b>12:22 limited express</b> to Takatsuki-shi, change to a semi-express to Minami-Ibaraki, then the Osaka Monorail and the Kita-Osaka Kyuko from Senri-Chuo: <b>Minoh-Kayano 13:19</b>. Hurry to stand 8 for the 13:30 bus.</p><p>Otherwise take the <b>14:00 bus</b> (Katsuoji 14:22), keep Katsuoji to 40–50 minutes and <b>start walking by about 15:15</b>.</p>' },
      { title: 'Plan B: skip the forest trail', sub: 'If we can’t leave Katsuoji by 15:20, it rains, or we’re tired', html: '<p>Take the bus down from Katsuoji, then walk <b>up the lit riverside path</b> from Minoh Station to the falls.</p><ul><li><b>16:20</b> bus from Katsuoji (route 30, ¥800) → Minoh-Kayano 16:41. Other buses: 15:50, 16:50, last 17:05.</li><li><b>17:00</b> from Minoh-Kayano (route 36, ¥250) → Hankyu Minoh Station 17:15. After the 15:50 bus: 16:30 (route 21) → 16:45.</li><li><b>17:15</b> walk up about 45 minutes: the lit falls at about 18:00.</li><li><b>18:20</b> walk down to Minoh Station (about 19:00), then dinner at Gyogyogyo, 5 minutes away (last order 21:00). Minoh Beer takes last orders at 20:30, so if it’s too late, go home from Minoh Station after dinner (change at Ishibashi Handai-mae and Juso).</li></ul><p class="sh-small">Buses cost ¥1,050 more per person.</p>' },
      { title: 'Couldn’t get into Minoh Beer', sub: 'There are later trains home', html: '<p>Makiochi to Karasuma also at 21:33 (arr. 22:43), 21:45 (arr. 22:53) and 21:57 (arr. 23:05).</p>' }
    ],
    whoHead: 'Bring',
    who: [
      'An IC card (ICOCA etc.) with at least ¥2,200. The Katsuoji bus takes no cash, and you can’t top up on board',
      'Some cash (Katsuoji ¥500, dinner)',
      'Gyogyogyo is small: call ahead to book for three (070-1741-0804)',
      'Comfortable shoes: about 1 hour 10 minutes on the trail, mostly downhill',
      'A jacket: the hills and the falls get cold in the evening',
      'A charged phone or power bank: night photos drain it fast'
    ],
    dealsHead: 'Fares (per person, IC card)',
    dealsLead: '¥2,170 in total (plus ¥500 for Katsuoji).',
    deals: [
      { name: 'Karasuma → Minoh-Kayano (Hankyu, Midosuji Line)', price: '¥890', text: 'Change at Awaji and Minamikata; Midosuji Line from Nishinakajima-Minamigata.' },
      { name: 'Minoh-Kayano → Katsuoji (Hankyu Bus)', price: '¥800', text: 'No cash since Oct 2026. IC card, or a ticket bought by credit card at the stand.', url: 'https://www.hankyubus.co.jp/news/2026101.html' },
      { name: 'Makiochi → Karasuma (Hankyu)', price: '¥480', text: 'Change at Ishibashi Handai-mae and Juso.' }
    ],
    dealsMore: 'Official site',
    dealsNote: '',
    srcHead: 'What we checked',
    src: [
      'Train and bus times: <a href="https://transit.yahoo.co.jp/" target="_blank" rel="noopener">Yahoo! Transit</a>, searched for Tue Nov 24, 2026.',
      'Katsuoji hours (weekdays 8:00–17:00, last entry 30 min before closing) and admission: checked on the <a href="https://katsuo-ji-temple.or.jp/access/" target="_blank" rel="noopener">official site</a> on Nov 20 (phone 072-721-7010).',
      'Falls light-up: <a href="https://www.mino-park.jp/event/art/1087/" target="_blank" rel="noopener">Minoh Park, autumn light-up 2026</a> (Nov 14 – Dec 6, daily, sunset–21:30)',
      'Sunset 16:49 (Osaka): <a href="https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s2711.html" target="_blank" rel="noopener">National Astronomical Observatory of Japan</a>',
      'Visitor Center closed on Tuesdays: <a href="https://minohkankou.net/sights/319/" target="_blank" rel="noopener">Minoh Tourism Association</a>',
      'Minoh Beer hours: <a href="https://www.minoh-beer.jp/store/" target="_blank" rel="noopener">Minoh Beer stores</a>',
      'Dinner at Gyogyogyo: <a href="https://news.minoh.net/chiisanaomiseouen/%E6%B5%B7%E9%AE%AE%E5%87%A6%E3%80%80%E9%B1%BB%E3%80%80%E3%81%8E%E3%82%87%E3%81%8E%E3%82%87%E3%81%8E%E3%82%87/" target="_blank" rel="noopener">Minoh local news</a> (Aug 2024: evenings 17:00–21:00 last order, closed Wed)',
      'Autumn leaves: Weathernews (<a href="https://weathernews.jp/koyo/spot/26222/" target="_blank" rel="noopener">Katsuoji</a>, <a href="https://weathernews.jp/koyo/spot/26202/" target="_blank" rel="noopener">Minoh Park</a>)'
    ],
    howHead: 'How to use this map',
    how: [
      { title: 'Follow the numbers', text: 'Spots 1–10 are in today’s order.' },
      { title: 'Tap a number', text: 'Tap a number on the map, or open the list, for photos, tips and today’s times.' },
      { title: 'Mark where you’ve been', text: 'Tap “Mark as visited” at each spot to keep track.' },
      { title: 'Directions', text: 'Use “Open in Google Maps” at each spot for walking directions.' }
    ],
    cta: 'Open the map',
    footer1: 'The trip plan for Denden, Taro-chan and Toshi. Check live service updates on the day. If it rains, the forest trail gets slippery: use Plan B.'
  };
})();
