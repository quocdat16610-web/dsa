#!/usr/bin/env python3
"""Chấm bài trên GitHub Actions từ một issue do trang web (GitHub Pages) tạo ra.

    python3 tools/gh_judge.py parse     # đọc issue → work/sub.json, ghi `topic`, `valid` vào $GITHUB_OUTPUT
    python3 tools/gh_judge.py judge     # chấm → out/result.json (chạy bài nộp bằng người dùng sandbox)
    python3 tools/gh_judge.py comment   # out/result.json → comment.md, ghi `label` vào $GITHUB_OUTPUT

Định dạng issue (trang web tự sinh):
    tiêu đề: [DSA] Nộp 0201 cpp #ab12cd
    nội dung: <!-- dsa {"type": "submit", "pid": "0201", "lang": "cpp", "user": "..."} -->
              ...
              ````cpp
              <code>
              ````
              (với type = "run": thêm một khối ```` thứ hai chứa input)
"""
import base64
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
WORK = os.path.join(ROOT, "work")
OUT = os.path.join(ROOT, "out")
MAX_CODE = 64 * 1024


def gh_output(**kv):
    path = os.environ.get("GITHUB_OUTPUT")
    lines = "".join(f"{k}={v}\n" for k, v in kv.items())
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(lines)
    else:
        print(lines, end="")


def load_event():
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        return json.load(f)


def parse_issue(title, body):
    body = (body or "").replace("\r\n", "\n")
    m = re.search(r"<!--\s*dsa\s+(\{.*?\})\s*-->", body, re.S)
    if not m:
        return None, "Không tìm thấy thông tin bài nộp (dòng <!-- dsa {...} -->). Hãy nộp từ trang web."
    try:
        meta = json.loads(m.group(1))
    except ValueError:
        return None, "Thông tin bài nộp bị hỏng."
    typ = meta.get("type")
    lang = meta.get("lang")
    pid = str(meta.get("pid", ""))
    if typ not in ("submit", "run"):
        return None, "Loại yêu cầu không hợp lệ."
    if lang not in ("cpp", "py"):
        return None, "Ngôn ngữ không hợp lệ (chỉ hỗ trợ cpp, py)."
    if typ == "submit" and not re.fullmatch(r"\d{4}", pid):
        return None, "Mã bài không hợp lệ."
    blocks = re.findall(r"^````[\w+]*\n(.*?)\n?^````\s*$", body, re.S | re.M)
    if not blocks or not blocks[0].strip():
        return None, "Không tìm thấy code (khối ```` ... ````)."
    code = blocks[0]
    if len(code) > MAX_CODE:
        return None, "Code quá dài (tối đa 64 KB)."
    sub = {"type": typ, "lang": lang, "pid": pid if typ == "submit" else "",
           "user": re.sub(r"[^\w .\-@À-ỹ]", "", str(meta.get("user", "")))[:40] or "khách",
           "tag": re.sub(r"\W", "", str(meta.get("tag", "")))[:12], "code": code,
           "input": blocks[1] + "\n" if typ == "run" and len(blocks) > 1 else ""}
    return sub, None


def cmd_parse():
    ev = load_event()
    issue = ev.get("issue", {})
    sub, err = parse_issue(issue.get("title", ""), issue.get("body", ""))
    os.makedirs(WORK, exist_ok=True)
    os.chmod(WORK, 0o700)
    if sub and sub["type"] == "submit":
        from problems import PROBLEMS
        if sub["pid"] not in PROBLEMS:
            sub, err = None, f"Không có bài {sub['pid']}."
    with open(os.path.join(WORK, "sub.json"), "w", encoding="utf-8") as f:
        json.dump({"sub": sub, "error": err}, f, ensure_ascii=False)
    topic = sub["pid"][:2] if sub and sub["pid"] else "00"
    gh_output(topic=topic, valid="true" if sub else "false")


def cmd_judge():
    with open(os.path.join(WORK, "sub.json"), encoding="utf-8") as f:
        d = json.load(f)
    sub, err = d["sub"], d["error"]
    os.makedirs(OUT, exist_ok=True)
    res = {"error": err}
    if sub:
        from judge.judge import judge, run_custom
        from problems import PROBLEMS, get_tests
        if sub["type"] == "submit":
            p = PROBLEMS[sub["pid"]]
            res = judge(sub["code"], sub["lang"], get_tests(sub["pid"]), p.tl, p.ml, checker=p.checker)
            res.update(pid=p.id, title=p.title)
        else:
            res = run_custom(sub["code"], sub["lang"], sub["input"])
        res.update(type=sub["type"], lang=sub["lang"], user=sub["user"], tag=sub["tag"])
    with open(os.path.join(OUT, "result.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False)


def _pre(s, n=1500):
    s = s if len(s) <= n else s[:n] + "\n..."
    return "<pre>" + html.escape(s) + "</pre>"


def build_comment(res):
    if not res:
        res = {"error": "Không chấm được (lỗi hệ thống). Hãy thử nộp lại."}
    if res.get("error") and "verdict" not in res:
        body = f"⚠️ **Không chấm được:** {html.escape(res['error'])}"
        label = "dsa-loi"
    elif res.get("type") == "run":
        body = (f"▷ **Chạy thử** ({html.escape(res.get('lang', ''))}): `{html.escape(res.get('verdict', ''))}`"
                f" · {res.get('time', 0)} ms · {round(res.get('mem', 0) / 1024)} MB\n\n**Output**\n{_pre(res.get('output', ''))}")
        if res.get("error"):
            body += f"\n**Lỗi**\n{_pre(res['error'])}"
        label = "dsa-chay-thu"
    else:
        ok = res.get("ok")
        body = f"{'✅' if ok else '❌'} **{html.escape(res.get('verdict', ''))}** — bài {res.get('pid')} {html.escape(res.get('title', ''))}"
        if res.get("tests"):
            body += f" · {res.get('time', 0)} ms · {round(res.get('mem', 0) / 1024)} MB\n\n| Test | Kết quả | Thời gian | Bộ nhớ |\n|---|---|---|---|\n"
            for t in res["tests"][-30:]:
                body += f"| {t['test']} | {t['status']} | {t['time']} ms | {round(t['mem'] / 1024)} MB |\n"
            bad = next((t for t in res["tests"] if t["status"] != "OK"), None)
            if bad:
                body += f"\n<details><summary>Chi tiết test {bad['test']}</summary>\n\n**Input**\n{_pre(bad['input'])}\n"
                if bad["status"] == "WA":
                    body += f"**Output của bạn**\n{_pre(bad['output'])}\n**Đáp án**\n{_pre(bad['answer'])}\n"
                if bad.get("checker"):
                    body += f"**Checker**\n{_pre(bad['checker'])}\n"
                body += "</details>\n"
        if res.get("compile"):
            body += f"\n**Thông báo biên dịch**\n{_pre(res['compile'], 3000)}"
        label = "dsa-accepted" if ok else "dsa-rejected"
    slim = dict(res)
    blob = base64.b64encode(json.dumps(slim, ensure_ascii=False).encode()).decode()
    if len(blob) > 50000:  # giữ comment dưới giới hạn 65536 ký tự của GitHub
        for t in slim.get("tests", []):
            for k in ("input", "output", "answer"):
                t[k] = t.get(k, "")[:200]
        blob = base64.b64encode(json.dumps(slim, ensure_ascii=False).encode()).decode()
    body += f"\n\n<!-- dsa-result:{blob} -->\n_Chấm tự động bởi GitHub Actions._"
    return body, label


def cmd_comment():
    path = os.path.join(OUT, "result.json")
    res = None
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                res = json.load(f)
        except ValueError:
            res = None
    body, label = build_comment(res)
    with open(os.path.join(ROOT, "comment.md"), "w", encoding="utf-8") as f:
        f.write(body)
    gh_output(label=label)


if __name__ == "__main__":
    {"parse": cmd_parse, "judge": cmd_judge, "comment": cmd_comment}[sys.argv[1]]()
