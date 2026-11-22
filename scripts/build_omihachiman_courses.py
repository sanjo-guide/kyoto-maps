#!/usr/bin/env python3
"""近江八幡マップの「彦根城にも行く」コースのデータを、元のファイルから作る。

使い方: python3 scripts/build_omihachiman_courses.py   （そのあと python3 scripts/sync_omihachiman.py）
- 元: data/routes/omihachiman.json（手で直すのはこのファイルだけ。「近江八幡で1日」コース＝14か所。
  彦根の3か所は、このファイルの hikone.spots に入っている）
- 作るもの: data/routes/omihachiman-hikone.json（「彦根城にも行く」コース＝17か所。直接直さない。実行のたびに作り直す）
  元のファイルは書き換えない
- 回る順（ORDER）：近江八幡の町（1〜12は元と同じ番号）→ 13 近江八幡駅（彦根へ）→ 14 彦根駅 → 15 彦根城 → 16 玄宮園 → 17 ティファニー
- めやすの時間は TIMES、入れ替える段落は SWAP、丸ごと入れ替えるスポットは WHOLE、「選んで回る」の設定は PLAN
- 時刻は元のファイルの sources（乗換案内・近江鉄道バスの時刻表・公式サイト、2026-11-22）で確かめたもの。
  彦根城と玄宮園は入場が16:30までなので、近江八幡14:34発の新快速に乗る時間割にしてある
- 紹介ページ（omihachiman/js/i18n.js の introFor.hikone）の写真は、スポットの id で指定している
"""
import copy, json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = f'{R}/data/routes/omihachiman.json'
OUT = f'{R}/data/routes/omihachiman-hikone.json'

ORDER = ['start', 'omi-sta', 'hori', 'ropeway', 'summit', 'zuiryuji', 'himure', 'kubotaya', 'marutake', 'beer', 'shinmachi', 'collina',
         'goal', 'hikone-sta', 'castle', 'genkyuen', 'tiffany']

DEP, VIS, MOV = ('おすすめ出発時間', 'Recommended departure time'), ('おすすめ訪問時間', 'Recommended visit time'), ('おすすめ移動時間', 'Recommended travel time')
# めやすの時間（各スポットの文章のいちばん下の行）。ここにないスポットは元のまま
TIMES = {
    'ropeway': (MOV, '上り 11:15ごろ、下り 12:00ごろ', 'up at about 11:15, down at about 12:00'),
    'summit': (VIS, '11:20〜11:55', '11:20–11:55'),
    'zuiryuji': (VIS, '11:35〜11:55（寄るなら、山頂の散歩を短めに）', '11:35–11:55 (if you go in, keep the summit walk short)'),
    'himure': (VIS, '12:05〜12:20', '12:05–12:20'),
    'kubotaya': (VIS, '12:25〜13:20', '12:25–13:20'),
    'marutake': (VIS, '12:25〜13:20', '12:25–13:20'),
    'beer': (VIS, '13:20〜13:45（1杯だけ）', '13:20–13:45 (just the one)'),
    'shinmachi': (VIS, '13:20〜13:45', '13:20–13:45'),
    'collina': (VIS, '10:55〜11:50（八幡山のかわりに行く場合）', '10:55–11:50 (if you come here instead of Mt. Hachiman)'),
    'tiffany': (VIS, '18:15〜19:45', '18:15–19:45'),
}

# 段落の入れ替え。段落の書き出し（日本語・英語）で見つけて丸ごと入れ替える。None は「その段落を外す」
SWAP = [
    ('hori', ('着いたらまず', 'Take a first turn'), {
        'ja': '着いたらまず、ここをひと回り。彦根へ行く日は午後にゆっくり歩く時間がないので、石畳の道はこのときに歩いておきましょう。',
        'en': 'Take a turn around it when you arrive. On a Hikone day there is no time for a slow walk in the afternoon, so do the stone path now.'}),
    ('hori', ('舟で回る', 'The Hachimanbori boat tour'), {
        'ja': '舟で回る「八幡堀めぐり」は10:00〜16:00、大人1,500円、約30分。彦根へ行く日に乗るなら、八幡山に上るのをやめて、この時間に。予約なしで乗れるのは2人以上から。1人のときは乗り場で聞いてみてください。',
        'en': 'The Hachimanbori boat tour runs 10:00–16:00: ¥1,500 per adult, about 30 minutes. To fit it into a Hikone day, take it now and skip Mt. Hachiman. Walk-ups are for two or more people; if you’re alone, ask at the landing.'}),
    ('summit', ('山頂の駅から西の丸跡', 'The West Bailey ruins'), {
        'ja': '山頂の駅から西の丸跡まで歩いて約3分。琵琶湖と対岸の山々が見えるのは、この西の丸跡のあたりです。反対側からは、近江八幡の町や田んぼ、西の湖（にしのこ）まで見えます。山の上をぐるっと回る遊歩道は1周約30分。彦根へ行く日は、12:00ごろのロープウェーで下りてください。',
        'en': 'The West Bailey ruins are about 3 minutes’ walk from the top station; this is where you look out over Lake Biwa to the mountains beyond. The other side looks over the town, the rice fields and Lake Nishinoko. The path around the summit takes about 30 minutes. On a Hikone day, take the ropeway down at about 12:00.'}),
    ('beer', ('金曜・土曜は20:00まで', 'On Fridays and Saturdays'), {
        'ja': '彦根へ行く日は、お昼のあとに1杯だけ。13:55（土日祝は14:00）のバスに乗るので、13:45には店を出てください。',
        'en': 'On a Hikone day, make it one quick beer after lunch. Leave by 13:45 for the 13:55 bus (14:00 on weekends and holidays).'}),
    ('shinmachi', ('ラ コリーナ（12番）', 'La Collina (stop 12)'), {
        'ja': 'ビールを飲まない人は、お昼のあとの時間をこの通りで。バス停「八幡堀八幡山ロープウェー口」へは歩いて5分ほどです。13:55（土日祝は14:00）のバスで駅へ戻ります。',
        'en': 'Not having a beer? Spend the time after lunch on this street instead. The “Hachimanbori Hachimanyama Ropeway-guchi” bus stop is about 5 minutes’ walk; take the 13:55 bus (14:00 on weekends and holidays) back to the station.'}),
    ('tiffany', ('ラ コリーナからのバスで', 'The bus from La Collina'), {
        'ja': '彦根の帰りに、近江八幡で途中下車して晩ごはんにする場合です。彦根17:52発の新快速で近江八幡に18:06着。ディナーのラストオーダーは20:00です。食事のあとは駅まで歩いてすぐ。20:06（土日祝は20:13）の新快速に乗ると、山科で地下鉄に乗り換えて三条京阪に21:00ごろ着きます。',
        'en': 'This is for breaking the journey back from Hikone for dinner. The 17:52 Special Rapid from Hikone reaches Omi-Hachiman at 18:06. Last orders for dinner are at 20:00. The station is a short walk away afterwards: take the 20:06 Special Rapid (20:13 on weekends and holidays), change to the subway at Yamashina, and you are back at Sanjo Keihan at about 21:00.'}),
]

# 丸ごと入れ替えるスポット（名前・種類・一覧の短い紹介・文章・時刻の行など）
WHOLE = {
    'collina': {
        'blurb': {'ja': '草屋根の建物と、焼きたてのバームクーヘン。彦根へ行く日は、八幡山のかわりに朝いちばんで。',
                  'en': 'A grass-roofed building and freshly baked baumkuchen. On a Hikone day, come first thing instead of going up Mt. Hachiman.'},
        'text': {'ja': '''ラ コリーナ近江八幡（ら こりーな おうみはちまん）

彦根へ行く日は、八幡山（4〜6番）とラ コリーナの両方は入りません。こちらを選ぶなら、駅の6番のりば10:45発のバスをそのまま「北之庄 ラ コリーナ前」まで乗ってください（10:54着・410円）。

焼きたてのバームクーヘンは、メインショップのクラブハリエやバームファクトリーで。草屋根のメインショップは、建築家・藤森照信（ふじもりてるのぶ）さんの設計。買い物をしなくても、田んぼのまわりの道や木の回廊を歩けます。

土日祝と連休は、公式サイトの混雑予想が朝から夕方まで「大混雑」になる日があります。買い物やカフェは並ぶつもりで。行く日の混み具合は、公式サイトの「混雑予想」で見られます。

八幡堀へ戻るバスは、平日11:52発、土日祝11:57発（3分・280円）。駅へ向かうバスと同じのりばで、道路の向かい側です。歩くと20〜25分。八幡堀に着いたら、日牟禮八幡宮（7番）とお昼へ。''',
                 'en': '''La Collina Omihachiman

A Hikone day has no room for both Mt. Hachiman (stops 4–6) and La Collina. If you choose this, stay on the 10:45 bus from stop 6 at the station all the way to “Kitanosho La Collina-mae” (arrives 10:54, ¥410).

Get freshly baked baumkuchen at Club Harie in the main shop or at the Baum Factory. The grass-roofed main shop is by architect Terunobu Fujimori. Even without shopping, you can walk the paths round the rice field and the timber colonnade.

On weekends, holidays and long weekends, the official crowd forecast can show “very crowded” from morning to evening, so expect queues at the shops and cafés. The forecast for your day is on the official website.

Buses back to the canal leave at 11:52 on weekdays and 11:57 on weekends and holidays (3 minutes, ¥280), from the same stop as buses for the station, across the road. On foot it is 20–25 minutes. From the canal, go on to Himure Hachimangu Shrine (stop 7) and lunch.'''},
    },
    'goal': {
        'name': {'ja': '近江八幡駅（彦根へ）', 'en': 'Omi-Hachiman Station (on to Hikone)'},
        'kind': {'ja': '駅', 'en': 'Station'},
        'blurb': {'ja': '八幡堀13:55（土日祝は14:00）のバスで駅へ戻り、14:34発の新快速で彦根へ。14分で着きます。',
                  'en': 'Take the 13:55 bus from the canal (14:00 on weekends and holidays) back to the station, then the 14:34 Special Rapid to Hikone: 14 minutes.'},
        'text': {'ja': '''近江八幡駅（おうみはちまんえき）

バス停「八幡堀八幡山ロープウェー口」から、平日は13:55発（駅に14:10着）、土日祝は14:00発（14:15着）のバスで駅へ戻ります。260円。土日祝は13:45発（14:00着）もあります。

駅からは、京都と反対方向の14:34発の新快速「近江塩津（おうみしおつ）」行きに乗って、彦根に14:48着。420円です。乗り遅れたら、14:52発の普通（15:12着）か、15:04発の新快速（15:18着）で。

駅には近江鉄道（おうみてつどう）の電車も乗り入れていて、青いカラフルな車両に出会えることも。''',
                 'en': '''Omi-Hachiman Station

From the “Hachimanbori Hachimanyama Ropeway-guchi” stop, take the 13:55 bus on weekdays (station 14:10) or the 14:00 on weekends and holidays (station 14:15). ¥260. On weekends and holidays there is also a 13:45 (station 14:00).

At the station, board the 14:34 Special Rapid for Omi-Shiotsu, heading away from Kyoto. It reaches Hikone at 14:48 (¥420). If you miss it, take the 14:52 local (arrives 15:12) or the 15:04 Special Rapid (arrives 15:18).

Ohmi Railway trains also use this station; you might spot one of their colourful blue cars.'''},
        'time': (DEP, '14:34の新快速', 'the 14:34 Special Rapid'),
        'rows': [
            ('bus', '八幡堀八幡山ロープウェー口 → 近江八幡駅 約15分・260円。平日13:55発、土日祝14:00発', 'Hachimanbori Hachimanyama Ropeway-guchi → station: about 15 min, ¥260. 13:55 on weekdays, 14:00 on weekends and holidays'),
            ('train', '近江八幡14:34発 → 彦根14:48着（新快速・420円）', 'Omi-Hachiman 14:34 → Hikone 14:48 (Special Rapid, ¥420)'),
        ],
    },
}

SECTIONS = [(('start', 'omi-sta'), 0), (('hori', 'zuiryuji'), 1), (('himure', 'marutake'), 2), (('beer', 'shinmachi'), 3),
            (('collina', 'collina'), {'area': {'ja': '北之庄', 'en': 'Kitanosho'}, 'title': {'ja': '八幡山のかわりに行くなら', 'en': 'Instead of Mt. Hachiman'}}),
            (('goal', 'hikone-sta'), 4), (('castle', 'genkyuen'), 5), (('tiffany', 'tiffany'), 6)]

PICKS = ['hori', 'summit', 'zuiryuji', 'himure', 'kubotaya', 'marutake', 'beer', 'shinmachi', 'collina', 'castle', 'genkyuen', 'tiffany']
DEFAULT_PICKS = ['hori', 'summit', 'himure', 'kubotaya', 'beer', 'castle', 'genkyuen']
ONE_LUNCH = {'ja': '久ぼ多屋とまるたけ近江西川はすぐ近く。ランチはどちらか1軒で十分です。', 'en': 'Kubotaya and Marutake are next door to each other; one lunch is plenty.'}
BOTH = {'ja': '彦根へ行く日は、八幡山とラ コリーナの両方は入りません。どちらか1つにしてください。',
        'en': 'A Hikone day has no room for both Mt. Hachiman and La Collina. Please choose one.'}


def last_line(text, lab, val, lang):
    p = text.split('\n\n')
    line = lab[0 if lang == 'ja' else 1] + ('：' if lang == 'ja' else ': ') + val
    if p[-1].startswith(('おすすめ', 'Recommended')):
        p[-1] = line
    else:
        p.append(line)
    return '\n\n'.join(p)


def main():
    base = json.load(open(BASE, encoding='utf-8'))
    by = {s['id']: copy.deepcopy(s) for s in base['spots'] + base['hikone']['spots']}
    assert sorted(by) == sorted(ORDER), sorted(set(by) ^ set(ORDER))
    for sid, w in WHOLE.items():
        s = by[sid]
        for k in ('name', 'kind', 'blurb', 'text'):
            if k in w:
                s[k] = copy.deepcopy(w[k])
        if 'time' in w:
            lab, ja, en = w['time']
            s['text'] = {'ja': last_line(s['text']['ja'], lab, ja, 'ja'), 'en': last_line(s['text']['en'], lab, en, 'en')}
        if 'rows' in w:
            s['info']['rows'] = [{'kind': k, 'text': {'ja': ja, 'en': en}, 'until': None, 'from': None} for k, ja, en in w['rows']]
    for sid, starts, new in SWAP:
        for i, l in enumerate(('ja', 'en')):
            p = by[sid]['text'][l].split('\n\n')
            hit = [k for k, x in enumerate(p) if x.startswith(starts[i])]
            assert len(hit) == 1, (sid, starts[i])
            if new is None:
                p.pop(hit[0])
            else:
                p[hit[0]] = new[l]
            by[sid]['text'][l] = '\n\n'.join(p)
    for sid, (lab, ja, en) in TIMES.items():
        by[sid]['text'] = {'ja': last_line(by[sid]['text']['ja'], lab, ja, 'ja'), 'en': last_line(by[sid]['text']['en'], lab, en, 'en')}
    # ラ コリーナ：帰りのバスの行と、駅へのバスの時刻は、このコースでは八幡堀へ戻るバスにする
    by['collina']['info']['rows'][2] = {'kind': 'bus', 'text': {
        'ja': 'ラ コリーナ前 → 八幡堀八幡山ロープウェー口 3分・280円。平日11:52発、土日祝11:57発',
        'en': 'La Collina-mae → Hachimanbori Hachimanyama Ropeway-guchi: 3 min, ¥280. 11:52 on weekdays, 11:57 on weekends and holidays'}, 'until': None, 'from': None}
    no = {sid: i + 1 for i, sid in enumerate(ORDER)}
    spots = []
    for sid in ORDER:
        s = by[sid]
        s['no'] = no[sid]
        spots.append(dict([('no', s['no'])] + [(k, v) for k, v in s.items() if k != 'no']))
    # 文章の中の番号（○番）が、このコースの番号と合っているかを確かめる（元のファイルの 13番・14番 が残っていないこと）
    for s in spots:
        if s['id'] in ('hikone-sta', 'castle', 'genkyuen'):
            continue
        for l in ('ja', 'en'):
            assert '13番' not in s['text'][l] and '14番' not in s['text'][l] and 'stop 13' not in s['text'][l] and 'stop 14' not in s['text'][l], (s['id'], l)
    sections = []
    for (a, b), d in SECTIONS:
        sec = {'first': no[a], 'last': no[b]}
        sec.update({'day': d} if isinstance(d, int) else d)
        sections.append(sec)
    out = {
        'id': 'omihachiman-hikone',
        'course': 'hikone',
        '_note': '近江八幡マップの「彦根城にも行く」コース。scripts/build_omihachiman_courses.py が data/routes/omihachiman.json から作る。このファイルは直接直さない。',
        'sections': sections,
        'focus': {'first': no['omi-sta'], 'last': no['goal']},
        'photoBase': base['photoBase'],
        'plan': {
            '_note': '「選んで回る」の設定。defaultPicks は時間割どおりの組み合わせ（八幡堀→八幡山→日牟禮八幡宮→お昼→1杯→彦根城→玄宮園）。駅は必ず入り、ロープウェーは山頂か瑞龍寺を選ぶと入る。',
            'defaultMode': 'pick',
            'picks': [no[x] for x in PICKS],
            'defaultPicks': [no[x] for x in DEFAULT_PICKS],
            'auto': {str(no['start']): {'always': True}, str(no['omi-sta']): {'always': True}, str(no['ropeway']): {'any': [no['summit'], no['zuiryuji']]},
                     str(no['goal']): {'always': True}, str(no['hikone-sta']): {'always': True}},
            'hints': [
                {'spot': no['kubotaya'], 'rule': {'any': [no['kubotaya']], 'andAny': [no['marutake']]}, 'text': ONE_LUNCH},
                {'spot': no['marutake'], 'rule': {'any': [no['marutake']], 'andAny': [no['kubotaya']]}, 'text': ONE_LUNCH},
                {'spot': no['collina'], 'rule': {'any': [no['collina']], 'andAny': [no['summit'], no['zuiryuji']]}, 'text': BOTH},
                {'spot': no['ropeway'], 'rule': {'any': [no['summit'], no['zuiryuji']], 'andAny': [no['collina']]}, 'text': BOTH},
            ],
        },
        'sources': base['sources'],
        'spots': spots,
    }
    open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('wrote', os.path.relpath(OUT, R), len(spots), 'spots')


if __name__ == '__main__':
    main()
