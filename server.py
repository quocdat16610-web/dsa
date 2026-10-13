#!/usr/bin/env python3
"""Máy chủ web cho công cụ soạn giáo án & luyện tập thuật toán (chỉ dùng thư viện chuẩn Python).

Chạy:   python3 server.py            → mở http://localhost:8000
        python3 server.py --port 9000 --host 0.0.0.0
        python3 server.py --prebuild  → sinh sẵn toàn bộ bộ test ở nền
"""
import argparse
import json
import mimetypes
import os
import sys
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from curriculum import TOPICS, topic_detail  # noqa: E402
from judge.judge import available_langs, judge, run_custom  # noqa: E402
from problems import LEVELS, PROBLEMS, get_tests, is_cached  # noqa: E402

STATIC = os.path.join(ROOT, "static")
DATA = os.path.join(ROOT, "data")
SUB_FILE = os.path.join(DATA, "submissions.jsonl")
MAX_BODY = 256 * 1024
_sub_lock = threading.Lock()
_warming = set()
_warm_lock = threading.Lock()


def warm(pid):
    """Sinh test ở nền để lần nộp đầu tiên không phải chờ."""
    with _warm_lock:
        if pid in _warming:
            return
        _warming.add(pid)

    def job():
        try:
            get_tests(pid)
        finally:
            with _warm_lock:
                _warming.discard(pid)
    threading.Thread(target=job, daemon=True).start()


def save_submission(rec):
    os.makedirs(DATA, exist_ok=True)
    with _sub_lock, open(SUB_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_submissions(user=None, pid=None, limit=100):
    if not os.path.exists(SUB_FILE):
        return []
    out = []
    with _sub_lock, open(SUB_FILE, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if user and r.get("user") != user:
                continue
            if pid and r.get("pid") != pid:
                continue
            out.append(r)
    return out[::-1][:limit]


def meta():
    probs = sorted((p.summary() for p in PROBLEMS.values()), key=lambda x: x["id"])
    return {"topics": TOPICS, "problems": probs, "levels": LEVELS, "langs": available_langs(),
            "total": len(probs)}


class Handler(BaseHTTPRequestHandler):
    server_version = "DSA-Tool/1.0"

    def log_message(self, fmt, *args):  # gọn log
        sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    # ------------------------------------------------------------ tiện ích
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _err(self, code, msg):
        self._json({"error": msg}, code)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            raise ValueError("Dữ liệu gửi lên quá lớn")
        raw = self.rfile.read(n) if n else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def _static(self, rel):
        path = os.path.normpath(os.path.join(STATIC, rel))
        if not path.startswith(STATIC) or not os.path.isfile(path):
            return self._err(404, "Không tìm thấy")
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript",):
            ctype += "; charset=utf-8"
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ------------------------------------------------------------ GET
    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        p = u.path
        try:
            if p in ("/", "/index.html"):
                return self._static("index.html")
            if p.startswith("/static/"):
                return self._static(p[len("/static/"):])
            if p == "/api/meta":
                return self._json(meta())
            if p.startswith("/api/topic/"):
                tid = int(p.rsplit("/", 1)[1])
                d = topic_detail(tid)
                return self._json(d) if d else self._err(404, "Không có chuyên đề")
            if p.startswith("/api/problem/"):
                pid = p.rsplit("/", 1)[1]
                if pid not in PROBLEMS:
                    return self._err(404, "Không có bài")
                pr = PROBLEMS[pid].public()
                pr["ready"] = is_cached(pid)
                if not pr["ready"]:
                    warm(pid)
                return self._json(pr)
            if p == "/api/submissions":
                return self._json(load_submissions(q.get("user"), q.get("pid"), int(q.get("limit", 100))))
            if p == "/api/status":
                ready = sum(1 for pid in PROBLEMS if is_cached(pid))
                return self._json({"ready": ready, "total": len(PROBLEMS), "warming": sorted(_warming)})
            return self._err(404, "Không tìm thấy")
        except Exception as e:  # noqa: BLE001
            return self._err(500, f"{type(e).__name__}: {e}")

    # ------------------------------------------------------------ POST
    def do_POST(self):
        p = urlparse(self.path).path
        try:
            body = self._body()
        except (ValueError, UnicodeDecodeError) as e:
            return self._err(400, str(e))
        try:
            if p == "/api/submit":
                pid, lang, code = body.get("pid"), body.get("lang", "cpp"), body.get("code", "")
                if pid not in PROBLEMS:
                    return self._err(404, "Không có bài")
                if not code.strip():
                    return self._err(400, "Chưa có code")
                pr = PROBLEMS[pid]
                t0 = time.time()
                tests = get_tests(pid)
                res = judge(code, lang, tests, pr.tl, pr.ml, checker=pr.checker)
                rec = {"id": uuid.uuid4().hex[:10], "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                       "user": (body.get("user") or "khách")[:40], "pid": pid, "title": pr.title,
                       "lang": lang, "verdict": res["verdict"], "ok": res["ok"],
                       "ms": res.get("time", 0), "kb": res.get("mem", 0), "code": code[:100000]}
                save_submission(rec)
                res["id"] = rec["id"]
                res["elapsed"] = round(time.time() - t0, 2)
                return self._json(res)
            if p == "/api/run":
                res = run_custom(body.get("code", ""), body.get("lang", "cpp"), body.get("input", ""))
                return self._json(res)
            return self._err(404, "Không tìm thấy")
        except Exception as e:  # noqa: BLE001
            return self._err(500, f"{type(e).__name__}: {e}")


def prebuild():
    def job():
        t0 = time.time()
        for i, pid in enumerate(sorted(PROBLEMS)):
            get_tests(pid)
            if (i + 1) % 20 == 0:
                print(f"[prebuild] {i + 1}/{len(PROBLEMS)} bài ({time.time() - t0:.0f}s)", file=sys.stderr)
        print("[prebuild] xong", file=sys.stderr)
    threading.Thread(target=job, daemon=True).start()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--prebuild", action="store_true", help="sinh sẵn toàn bộ bộ test ở nền")
    a = ap.parse_args()
    if a.prebuild:
        prebuild()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"Đang chạy tại http://{a.host}:{a.port}  ({len(PROBLEMS)} bài, ngôn ngữ: {', '.join(available_langs().values())})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")


if __name__ == "__main__":
    main()
