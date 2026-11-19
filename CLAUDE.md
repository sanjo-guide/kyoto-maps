# CLAUDE.md

京都の「1日観光ルート」を紹介するWebサイトのプロジェクト。

## プロジェクト概要

- **目的**: 京都を1日で巡るモデルルートを、地図・時間配分・移動手段つきで紹介する
- **想定読者**: 京都を訪れる国内外の観光客（初めて〜リピーター）
- **主なコンテンツ**: ルートごとの紹介ページ（スポット順、所要時間、移動方法、地図、Tips）

## 技術スタック

- フレームワーク: なし（静的 HTML / CSS / JS。ビルド不要）
- 地図: Leaflet 1.9.4（unpkg から読み込み）+ OpenStreetMap タイル
- ホスティング: GitHub Pages（予定。kyoto-momiji と同じ sanjo-guide アカウント）
- 経緯: 有料サービス PointMap+ で作っていたマップを自前サイトへ移行中

## コマンド

- ローカル確認: `python3 -m http.server 8000`（`.claude/launch.json` の `site`）→ http://localhost:8000/
- PointMap+ からの取り込み:
  1. `curl -s -X POST -H "Content-Type: application/json" https://api.pointmap.site/api/v1/release/map/view/<パス> -o _source/<名前>.json`
  2. `python3 scripts/import_pointmap.py _source/<名前>.json data/routes/<ルートID>.json <ルートID>`
  3. `python3 scripts/fetch_photos.py data/routes/<ルートID>.json <一時フォルダ>` — 写真をダウンロードして縮小し `images/<ルートID>/` に保存、JSON のパスも書き換える
  - 手順2を再実行するとルートJSONは上書きされる（写真パスも外部URLに戻る）。手で直した内容があるときは注意

## ディレクトリ構成

```
/
├── CLAUDE.md
├── index.html            # トップ（マップ一覧）
├── <ルートID>/index.html  # ルートごとのページ（body の data-route でデータを指定）
├── assets/map.js, map.css # 全ルート共通の地図ページ
├── data/routes/          # ルートデータ（1ルート = 1ファイル）
├── scripts/              # 取り込み・変換スクリプト
└── _source/              # PointMap+ の元データ（公開しない）
```

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
