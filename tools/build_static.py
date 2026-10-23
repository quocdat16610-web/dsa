#!/usr/bin/env python3
"""Xuất bản web tĩnh cho GitHub Pages.

    python3 tools/build_static.py site [owner/repo]

Tạo thư mục `site/` gồm giao diện + dữ liệu JSON (api/meta.json, api/topic/N.json, api/problem/PID.json).
Trên GitHub Pages, việc chấm bài được chuyển cho GitHub Actions thông qua issue (xem tools/gh_judge.py).
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from curriculum import TOPICS, topic_detail  # noqa: E402
from problems import LEVELS, PROBLEMS  # noqa: E402


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def main(out, repo):
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(os.path.join(ROOT, "static"), os.path.join(out, "static"))
    shutil.copy(os.path.join(ROOT, "static", "index.html"), os.path.join(out, "index.html"))
    open(os.path.join(out, ".nojekyll"), "w").close()
    cfg = {"mode": "static", "repo": repo}
    with open(os.path.join(out, "static", "config.js"), "w", encoding="utf-8") as f:
        f.write("window.DSA_CONFIG = " + json.dumps(cfg) + ";\n")
    probs = sorted((p.summary() for p in PROBLEMS.values()), key=lambda x: x["id"])
    dump(os.path.join(out, "api", "meta.json"),
         {"topics": TOPICS, "problems": probs, "levels": LEVELS, "langs": {"cpp": "GNU G++17", "py": "Python 3"},
          "total": len(probs)})
    for t in TOPICS:
        dump(os.path.join(out, "api", "topic", f"{t['id']}.json"), topic_detail(t["id"]))
    for pid, p in PROBLEMS.items():
        d = p.public()
        d["ready"] = True
        dump(os.path.join(out, "api", "problem", f"{pid}.json"), d)
    print(f"Đã xuất {len(PROBLEMS)} bài vào {out}/ (repo: {repo})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "site",
         sys.argv[2] if len(sys.argv) > 2 else os.environ.get("GITHUB_REPOSITORY", "quocdat16610-web/dsa"))
