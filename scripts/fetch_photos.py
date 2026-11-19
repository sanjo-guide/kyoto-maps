"""ルートデータに入っている外部の写真（PointMap+ のサーバー上）をダウンロードし、
スマホ向けに縮小してプロジェクト内に保存する。ルートJSONの写真パスも書き換える。

使い方:
  python3 scripts/fetch_photos.py data/routes/<ルートID>.json <ダウンロード用の一時フォルダ>

- 本体: images/<ルートID>/<番号>-<連番>.jpg（長辺1080px）
- サムネイル: images/<ルートID>/thumbs/<番号>-<連番>.jpg（長辺240px）
- 縮小には macOS 標準の sips を使う
- すでに変換済みの写真（src が http で始まらないもの）は飛ばす
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MAIN_SIZE, MAIN_QUALITY = 1080, 65
THUMB_SIZE, THUMB_QUALITY = 240, 70


def sips(src, dst, size, quality):
    subprocess.run(
        ["sips", "-Z", str(size), "-s", "format", "jpeg", "-s", "formatOptions", str(quality), str(src), "--out", str(dst)],
        check=True, capture_output=True,
    )


def work(job):
    url, raw, main, thumb = job
    if not raw.exists():
        subprocess.run(["curl", "-sfL", "--retry", "3", "-o", str(raw), url], check=True)
    sips(raw, main, MAIN_SIZE, MAIN_QUALITY)
    sips(raw, thumb, THUMB_SIZE, THUMB_QUALITY)
    return main


def main(route_path, cache_dir):
    route_path = Path(route_path)
    route = json.loads(route_path.read_text(encoding="utf-8"))
    rid = route["id"]
    out = Path("images") / rid
    (out / "thumbs").mkdir(parents=True, exist_ok=True)
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)

    jobs, targets = [], []
    for spot in route["spots"]:
        for k, photo in enumerate(spot["photos"], 1):
            if not photo["src"].startswith("http"):
                continue
            name = f"{spot['no']:02d}-{k}.jpg"
            url = photo["src"]
            raw = cache / (f"{spot['no']:02d}-{k}" + Path(url).suffix.lower())
            jobs.append((url, raw, out / name, out / "thumbs" / name))
            targets.append((photo, url, name))

    print(f"{len(jobs)} photos to process")
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, _ in enumerate(ex.map(work, jobs), 1):
            if i % 20 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)}", flush=True)

    for photo, url, name in targets:
        photo["original"] = url
        photo["src"] = f"images/{rid}/{name}"
        photo["thumb"] = f"images/{rid}/thumbs/{name}"

    route_path.write_text(json.dumps(route, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(p.stat().st_size for p in out.rglob("*.jpg"))
    print(f"done: images/{rid} ({total / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
