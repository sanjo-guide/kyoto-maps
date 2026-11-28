#!/usr/bin/env python3
"""札幌マップの写真クレジットを、3人の担当のファイルからまとめて1つにする（2026-11-29）。

使い方: python3 scripts/merge_sapporo_web_photos.py
- 入力: scripts/sapporo_web_photos_a.json（eki・jogai・hokudai・akarenga・tokeidai・odori）
        scripts/sapporo_web_photos_b.json（nijo・tanukikoji・beer・susukino・shiryokan）
        scripts/sapporo_web_photos_c.json（moiwa・jingu・zoo・shiroi・moerenuma）
- 出力: scripts/sapporo_web_photos.json（build_sapporo_data.py が読むファイル）
- 点検もする：
  - 16スポット全部そろっているか
  - 書かれている画像が images/sapporo/ にあるか
  - images/sapporo/ にあってJSONに書かれていない画像（担当が途中でやめたもの）
  - ライセンスが使ってよいものか（CC BY / CC BY-SA / CC0 / PD）
  - 同じ Commons の写真を2回使っていないか
  - sapporo/js/i18n.js の [スポットのid, 番号] が枚数の中に収まっているか
3つのファイルがそろっていなくても、あるぶんだけでまとめて、足りないものを知らせる。
"""
import json, os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{R}/images/sapporo"
ORDER = ["eki", "jogai", "hokudai", "akarenga", "tokeidai", "odori",
         "nijo", "tanukikoji", "beer", "susukino", "shiryokan",
         "moiwa", "jingu", "zoo", "shiroi", "moerenuma"]
PARTS = {"a": ["eki", "jogai", "hokudai", "akarenga", "tokeidai", "odori"],
         "b": ["nijo", "tanukikoji", "beer", "susukino", "shiryokan"],
         "c": ["moiwa", "jingu", "zoo", "shiroi", "moerenuma"]}
OK_LIC = ("CC BY", "CC0", "Public domain", "PD", "CC-BY")

out, problems, missing_parts = {}, [], []
for part, ids in PARTS.items():
    p = f"{R}/scripts/sapporo_web_photos_{part}.json"
    if not os.path.exists(p):
        missing_parts.append(part)
        continue
    d = json.load(open(p, encoding="utf-8"))
    for sid in ids:
        if sid not in d or not d[sid]:
            problems.append(f"{part}: {sid} の写真がない")
            continue
        out[sid] = d[sid]
    for sid in d:
        if sid not in ids:
            problems.append(f"{part}: 担当外の {sid} が入っている（無視した）")

seen = {}
for sid, items in out.items():
    for i, x in enumerate(items, 1):
        for k in ("file", "author", "license", "title"):
            if not x.get(k):
                problems.append(f"{sid}[{i}]: {k} が空")
        f = x.get("file", "")
        if not re.fullmatch(rf"{sid}-w\d+\.jpg", f):
            problems.append(f"{sid}[{i}]: ファイル名が {sid}-w<番号>.jpg の形でない（{f}）")
        if not os.path.exists(f"{IMG}/{f}"):
            problems.append(f"{sid}[{i}]: 画像がない（images/sapporo/{f}）")
        lic = x.get("license", "")
        if not any(lic.upper().startswith(o.upper()) for o in OK_LIC):
            problems.append(f"{sid}[{i}]: ライセンスを確かめてください（{lic}）")
        t = x.get("title", "")
        if t in seen:
            problems.append(f"{sid}[{i}]: {seen[t]} と同じ Commons の写真（{t}）")
        seen[t] = f"{sid}[{i}]"

# JSON に書かれていない画像
listed = {x["file"] for items in out.values() for x in items}
ondisk = {f for f in os.listdir(IMG) if f.endswith(".jpg")} if os.path.isdir(IMG) else set()
orphan = sorted(ondisk - listed)

# i18n.js の写真の指定が枚数の中に収まっているか
i18n = f"{R}/sapporo/js/i18n.js"
if os.path.exists(i18n):
    s = open(i18n, encoding="utf-8").read()
    for sid, n in re.findall(r'\[\s*"([a-z]+)",\s*(\d+)\s*\]', s):
        if sid not in out:
            problems.append(f"i18n.js: {sid} の写真がまだない")
        elif int(n) >= len(out[sid]):
            problems.append(f"i18n.js: [{sid}, {n}] は枚数（{len(out[sid])}枚）を超えている")

if missing_parts:
    print("まだ届いていない担当:", ", ".join(missing_parts))
print("スポットと枚数:", ", ".join(f"{s}:{len(out[s])}" for s in ORDER if s in out))
print("合計", sum(len(v) for v in out.values()), "枚 /", len(out), "スポット")
if orphan:
    print("JSONに書かれていない画像:", ", ".join(orphan))
if problems:
    print("\n--- 直すところ ---")
    for p in problems:
        print(" ", p)

json.dump({s: out[s] for s in ORDER if s in out}, open(f"{R}/scripts/sapporo_web_photos.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nwrote scripts/sapporo_web_photos.json")
sys.exit(1 if (problems or missing_parts) else 0)
