#!/usr/bin/env python3
"""写真を縮小してサイトに追加し、ルートJSONの photos を置き換える。

使い方:
  python3 scripts/add_photos.py <manifest.json>

manifest.json の形:
  {
    "route": "kanazawa",                       # data/routes/<route>.json
    "spots": {
      "1": [                                   # スポット番号（no）
        {"file": "/path/to/photo.jpg",
         "caption": {"ja": "志摩の抹茶", "en": "Matcha at Shima"},   # 省略可
         "credit": {"author": "...", "license": "CC BY-SA 4.0",      # 他人の写真のときだけ
                    "license_url": "...", "url": "..."}}
      ]
    }
  }

- 画像は長辺1600px（一覧用の thumbs は長辺320px）の JPEG にして images/<route>/ に保存する
- EXIF（撮影位置・カメラ情報など）は書き出さない
- manifest に載っているスポットの photos だけを置き換える（他のスポットはそのまま）
- 必要: Pillow（pip install pillow）
"""
import json
import os
import sys

from PIL import Image, ImageOps

FULL = 1600
THUMB = 320


def save(src, dst, size, quality):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((size, size), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)


def main(manifest_path):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    man = json.load(open(manifest_path, encoding="utf-8"))
    route = man["route"]
    data_path = os.path.join(root, "data", "routes", f"{route}.json")
    data = json.load(open(data_path, encoding="utf-8"))
    spots = {str(s["no"]): s for s in data["spots"]}

    for no, items in man["spots"].items():
        spot = spots[no]
        photos = []
        for k, item in enumerate(items, 1):
            name = f"{int(no):02d}-{k}.jpg"
            rel = f"images/{route}/{name}"
            rel_thumb = f"images/{route}/thumbs/{name}"
            save(item["file"], os.path.join(root, rel), FULL, 80)
            save(item["file"], os.path.join(root, rel_thumb), THUMB, 75)
            p = {"src": rel, "thumb": rel_thumb, "alt": ""}
            if item.get("caption"):
                p["caption"] = item["caption"]
            if item.get("credit"):
                p["credit"] = item["credit"]
            photos.append(p)
        spot["photos"] = photos
        print(f"spot {no}: {len(photos)} photos")

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
