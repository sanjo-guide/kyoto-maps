"""PointMap+ の書き出しデータ（JSON）を、このサイト用のルートデータに変換する。

使い方:
  1. PointMap+ のデータを保存する
     curl -s -X POST -H "Content-Type: application/json" \
       https://api.pointmap.site/api/v1/release/map/view/<マップのパス> -o _source/<名前>.json
  2. 変換する
     python3 scripts/import_pointmap.py _source/<名前>.json data/routes/<ルートID>.json <ルートID>

変換後の JSON は手で直してよい（もう一度変換すると上書きされるので注意）。
"""
import json
import re
import sys
from datetime import date

JA_CHARS = re.compile(r"[぀-ヿ㐀-鿿！-｠]")

# 「英語は下にあります」系の案内文や区切り線は捨てる
NOISE = re.compile(
    r"^(an? )?english (description|explanation)|^the english explanation|^english description$|^⸻$",
    re.I,
)
TIME_JA = re.compile(r"^おすすめ(訪問|出発|移動)時間[:：]\s*(.+)$")
TIME_EN = re.compile(r"^Recommended (visit|travel|departure) time[s]?:\s*(.+)$", re.I)
HOURS_JA = re.compile(r"^営業時間[:：]\s*(.+)$")
HOURS_EN = re.compile(r"^Opening hours:\s*(.+)$", re.I)


def is_ja(text):
    letters = [c for c in text if not c.isspace()]
    if not letters:
        return False
    return len(JA_CHARS.findall(text)) / len(letters) > 0.15


def split_title(title):
    title = title.replace("　", " ").strip()
    # 日本語名のあとに英語名が続く形を分ける:
    # 例「鴨川デルタ(Kamogawa Delta)」「京阪 三条駅 Sanjo Station (Keihan Line)」
    for i, c in enumerate(title):
        prev_is_word = i > 0 and title[i - 1].isascii() and title[i - 1].isalnum()
        if c.isascii() and (c.isalpha() or c == "(") and not prev_is_word and JA_CHARS.search(title[:i]) and not JA_CHARS.search(title[i:]):
            ja, en = title[:i].strip(), title[i:].strip()
            # 英語名が丸ごと括弧に入っているときは外す
            if en.startswith("(") and en.endswith(")") and "(" not in en[1:-1] and ")" not in en[1:-1]:
                en = en[1:-1].strip()
            return ja, en
    return title, title


def split_text(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text.replace("\r", "")) if p.strip()]
    out = {"ja": [], "en": []}
    time = {"ja": None, "en": None}
    hours = {"ja": None, "en": None}
    for p in paras:
        lines = []
        for line in p.split("\n"):
            s = line.strip().replace("￼", "").strip()
            if not s or NOISE.search(s):
                continue
            if m := TIME_JA.match(s):
                time["ja"] = m.group(2).strip()
                continue
            if m := TIME_EN.match(s):
                time["en"] = m.group(2).strip()
                continue
            if m := HOURS_JA.match(s):
                hours["ja"] = m.group(1).strip()
                continue
            if m := HOURS_EN.match(s):
                hours["en"] = m.group(1).strip()
                continue
            lines.append(s)
        if not lines:
            continue
        block = "\n".join(lines)
        out["ja" if is_ja(block) else "en"].append(block)
    return out, time, hours


def main(src, dst, route_id):
    raw = json.load(open(src, encoding="utf-8"))
    rm = raw["release_map"]
    features = sorted(rm["release_map_content"]["feature_contents"], key=lambda f: f["order"])
    spots = []
    for f in features:
        name_ja, name_en = split_title(f["title"])
        desc, time, hours = split_text(f["text"] or "")
        # 本文の1行目が見出し（例「鴨川デルタ」「一乗寺駅から鞍馬方面へ」）なら分けておく
        heading = None
        if desc["ja"]:
            first = desc["ja"][0]
            if "\n" not in first and len(first) <= 50 and not re.search(r"[。！？]", first):
                heading = desc["ja"].pop(0)
                # 名前の繰り返しだけなら表示しない（英字・空白・括弧などを除いて比べる）
                norm = lambda s: re.sub(r"[\x00-\x7fÀ-ɏ\s（）〜・「」]", "", s)
                if not norm(heading) or norm(heading) in norm(name_ja):
                    heading = None
        spots.append(
            {
                "no": f["order"],
                "name": {"ja": name_ja, "en": name_en},
                "heading": heading,
                "lat": round(f["latitude"], 6),
                "lng": round(f["longitude"], 6),
                "color": f["map_marker_color"]["base_color"] if f.get("map_marker_color") else "#888888",
                "time": time,
                "hours": hours,
                "description": {"ja": "\n\n".join(desc["ja"]), "en": "\n\n".join(desc["en"])},
                "links": [{"label": l["title"], "url": l["url"]} for l in f["feature_links"]],
                "photos": [
                    {"src": i["image_url"], "alt": ""}
                    for i in sorted(f["feature_images"], key=lambda x: x["order"])
                ],
            }
        )
    route = {
        "id": route_id,
        "title": {"ja": rm["title"], "en": rm["title"]},
        "summary": {"ja": "", "en": ""},
        "area": "",
        "tags": [],
        "center": [rm["display_start_latitude"], rm["display_start_longitude"]],
        # ゲスト向けの注意書き（ページ下部に表示）
        "notice": {
            "ja": "掲載情報は2025年8月時点のものです。営業時間・料金・時刻表は、お出かけ前に公式サイト等でご確認ください。",
            "en": "Information as of August 2025. Opening hours, fees and timetables may change, so please check the official websites before you go.",
        },
        "source": {
            "imported_from": f"PointMap+ https://ihistory.site/pointmap/maps/{rm['path']}",
            "imported_on": date.today().isoformat(),
            "note": "料金・営業時間などの事実情報は PointMap+ 掲載時（2025年8月作成）の原稿のまま。公開前に要確認。",
        },
        "spots": spots,
    }
    with open(dst, "w", encoding="utf-8") as fp:
        json.dump(route, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    print(f"{len(spots)} spots, {sum(len(s['photos']) for s in spots)} photos -> {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
