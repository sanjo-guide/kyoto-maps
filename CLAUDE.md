# CLAUDE.md

京都の「1日観光ルート」を紹介するWebサイトのプロジェクト。

## プロジェクト概要

- **目的**: 京都を1日で巡るモデルルートを、地図・時間配分・移動手段つきで紹介する
- **想定読者**: 京都を訪れる国内外の観光客（初めて〜リピーター）
- **主なコンテンツ**: ルートごとの紹介ページ（スポット順、所要時間、移動方法、地図、Tips）

## 技術スタック

- フレームワーク: なし（静的 HTML / CSS / JS。ビルド不要）
- 地図: Leaflet 1.9.4（vendor/ に同梱）。地図の種類は下の「ディレクトリ構成」を参照
- ホスティング: GitHub Pages — リポジトリ `sanjo-guide/kyoto-maps`（main ブランチのルートを公開）
  - 公開URL: https://sanjo-guide.github.io/kyoto-maps/ （叡山電鉄: …/eizan-line/、箕面: …/minoh/、金沢: …/kanazawa/）
  - 更新は `git push` するだけで1〜2分後に反映。CSS/JS を変えたら各ページの `?v=` の数字を上げる
  - このMacの GitHub ログインは GitHub CLI（gh）。ログインし直すときは `gh auth login --web`
- 注意: このフォルダは iCloud の「書類」同期の中にある。ファイルを短時間に上書きすると「◯◯ 2.jpg」のような重複ができることがあるので、コミット前に `git status` で確認する
- 古い試作版 `sanjo-guide/eizan-map` はホステル表記が残っていたため、2026-11-20 に非公開化（GitHub Pages 停止＋リポジトリ private）。本番はこちらの kyoto-maps
- 経緯: 有料サービス PointMap+ で作っていたマップを自前サイトへ移行中
- **このサイトは Toshi 個人のもの**（2026-11-20 オーナー決定）。勤務先のホステルの名前・ロゴ・「スタッフ」「ホステルから」などの表現は使わない（ファイル内のコメントにも書かない）。ホステルとして配るものは別（Cowork）で作る
- ルート型の「選んで回る」: データの `plan` に、自分で選ぶ場所（picks）と、駅・バス停など自動で入る場所の条件（auto: any / andAny / none）、組み合わせごとの一言（hints）を書く。`plan` がないマップでは切り替えボタンは出ない。季節営業の可能性がある店は spot の `caution` と notices（head付き）で注意書きを出す
- 叡山電鉄ルートのスタートは出町柳駅（1番）。旧番号（出町柳より前の2か所＝1・2）から2を引いた番号になっている。`#18` のような番号だけのリンクは旧番号として扱う

## コマンド

- ローカル確認: `python3 -m http.server 8000`（`.claude/launch.json` の `site`）→ http://localhost:8000/
- PointMap+ からの取り込み:
  1. `curl -s -X POST -H "Content-Type: application/json" https://api.pointmap.site/api/v1/release/map/view/<パス> -o _source/<名前>.json`
  2. `python3 scripts/import_pointmap.py _source/<名前>.json data/routes/<ルートID>.json <ルートID>`
  3. `python3 scripts/fetch_photos.py data/routes/<ルートID>.json <一時フォルダ>` — 写真をダウンロードして縮小し `images/<ルートID>/` に保存、JSON のパスも書き換える
  - 手順2を再実行するとルートJSONは上書きされる（写真パスも外部URLに戻る）。手で直した内容があるときは注意

## ディレクトリ構成

マップは2種類のデザインを使い分ける（2026-11-20 に統一）。

| 種類 | 使う場面 | 元にしたもの | 例 |
|---|---|---|---|
| ルート型 | 番号の順に回る1日ルート | 旧 eizan-map（非公開）の preview 版 | `eizan-line/`, `minoh/` |
| スポット紹介型 | 順番を決めずにおすすめを紹介 | sanjo-guide/kanazawa-guide | `kanazawa/` |

```
/
├── CLAUDE.md
├── index.html              # トップ（マップ一覧）。2つの型と同じフォント・色で、CSS/JS は中に直書き
├── eizan-line/             # ルート型: index.html, css/, js/app.js, js/i18n.js
│                           #   データは data/routes/eizan-line.json、写真は images/eizan-line/
├── minoh/                  # ルート型（大阪・箕面）。eizan-line/ の複製で、i18n.js だけ箕面専用
│                           #   データは data/routes/minoh.json、写真は images/minoh/
├── kanazawa/               # スポット紹介型: index.html, css/, js/app.js, js/data.js, img/
├── kanazawa-daytrips/      # 旧URL。kanazawa/#trips へ転送するだけ
├── assets/basemap.js       # 全マップ共通の地図スタイル
├── vendor/                 # Leaflet 1.9.4、MapLibre
├── data/routes/            # ルート型のデータ
├── images/                 # ルート型の写真
├── scripts/                # PointMap+ からの取り込み・写真縮小
└── _source/                # PointMap+ の元データ（公開しない）
```

- 金沢の写真: `kanazawa/img/hq-*.jpg` は写真アプリの全候補（6,667枚、Nikon D7000含む）から選んだ高画質版（旧 kyoto-maps の金沢マップ由来）。それ以外は kanazawa-guide 由来で、横552px前後の小さい写真がある。各スポットは高画質版を先に並べ、足りない分だけ kanazawa-guide の写真で補っている（最大10枚）
- 酒楽（しゅらく）の紹介文は2026-11-20にオーナーが書いたもの。消さないこと
- 箕面の写真: 写真アプリから GPS（Nikon D7000 は撮影時刻）で各スポットの候補（約2,000枚）を集め、全部見て1か所10枚以内に絞ったもの。元は iCloud にあり、`osxphotos export … --download-missing` で書き出して長辺1600px・位置情報なしに縮小した
- minoh/ は eizan-line/ の index.html・css・app.js をそのまま写して、データのパス・保存キー（kyoto-maps-minoh-…）・タイトルだけ変えている。ルート型のテンプレートを直したら `python3 scripts/sync_minoh.py` で minoh/ に写し直す（新しい文言キーは minoh/js/i18n.js に手で足す）
- 新しいマップを作るときは、どちらの型かを決めて既存のフォルダを複製し、データと文言だけ差し替える。トップページ（index.html）の該当する段にカードを足す
- 言語の選択は localStorage の `kyoto-maps-lang`（ルート型）と `kanazawa-lang`（金沢）に保存。トップページで選ぶと両方に書き込む
- 地図の見た目は全マップ共通で `assets/basemap.js`（Googleマップ / Appleマップに近い配色。町名・お店の名前は出さず、市町村・駅・川・大きな道だけ）。データは OpenFreeMap（OpenStreetMap）。オーナーの希望（2026-11-20）なので、新しいマップでも必ずこれを使う
- 金沢のページは「金沢市内」「日帰り」をタブで切り替える。日帰りはエリア見出し（加賀温泉・五箇山・氷見・富山・福井）の下に場所ごとのカードを並べる形（オーナーの希望）
- `scripts/import_pointmap.py` の出力は旧形式。ルート型に使うときは eizan-line.json の形（kind, blurb, sections, gmaps, links, info, notices）に合わせて手直しが必要

## ルートデータの方針

- ルート情報はページに直書きせず、データファイル（JSON / Markdown frontmatter 等）で管理する
- 1ルートあたりの想定項目:
  - `id`, `title`, `summary`, `area`（東山・嵐山・伏見など）, `season`, `tags`
  - `spots`: 順番つきのスポット一覧（名前、緯度経度、滞在目安、到着予定時刻、説明）
  - `transport`: スポット間の移動手段と所要時間（徒歩・バス・電車など）
  - `tips`: 混雑回避、予約要否、拝観料などの注意点
- 緯度経度は小数点以下5〜6桁程度で記録する

## コンテンツ・表記ルール

- 文章は日本語を基本とする（多言語対応は将来検討）
- 寺社名・地名は正式名称を使い、初出で読み仮名を付ける（例: 清水寺（きよみずでら））
- 拝観料・営業時間・アクセスなどの事実情報は変わりやすいので、出典と確認日をデータに残す
- 推測で事実情報（料金・時間・休業日）を書かない。不明な場合は「要確認」と明記する

## 画像・著作権

- 使用する写真は自分で撮影したもの、またはライセンスが明確なもの（CC等）のみ
- 出典・ライセンス表記が必要な画像はクレジットを必ず記載する
- 地図タイルの利用規約・帰属表示（例: © OpenStreetMap contributors）を守る

## 実装方針

- モバイルファースト（観光中にスマホで見る想定）
- 軽量・高速表示を優先（画像は最適化、不要なJSを避ける）
- アクセシビリティ: 画像に alt、十分なコントラスト、地図以外でもルートが分かるテキスト情報を併記
