"""Trình chấm bài kiểu Codeforces.

- Biên dịch (C++17 / Python 3), chạy lần lượt từng test, dừng ở test sai đầu tiên.
- Kết quả: Accepted, Wrong answer on test k, Time limit exceeded on test k,
  Memory limit exceeded on test k, Runtime error on test k, Compilation error.
- So sánh output theo token (bỏ qua khác biệt khoảng trắng / xuống dòng), giống checker mặc định của Codeforces.

CẢNH BÁO: code được chạy trực tiếp trên máy (chỉ giới hạn bằng rlimit), KHÔNG phải sandbox an toàn.
Chỉ dùng trong lớp học tin cậy, hoặc chạy server bên trong Docker.
"""
import os
import resource
import shutil
import signal
import subprocess
import tempfile
import threading
import time

LANGS = {
    "cpp": {"name": "GNU G++17", "file": "main.cpp",
            "compile": ["g++", "-std=c++17", "-O2", "-pipe", "-o", "main", "main.cpp"],
            "run": ["./main"], "tl_mult": 1.0},
    "py": {"name": "Python 3", "file": "main.py",
           "compile": None, "run": ["python3", "-S", "main.py"], "tl_mult": 3.0},
}

MAX_PARALLEL = max(1, (os.cpu_count() or 2) - 1)
_slots = threading.BoundedSemaphore(MAX_PARALLEL)


def available_langs():
    out = {}
    for k, v in LANGS.items():
        exe = (v["compile"] or v["run"])[0]
        if shutil.which(exe):
            out[k] = v["name"]
    return out


def _limits(cpu_sec, mem_mb):
    def f():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_sec, cpu_sec + 1))
        mem = mem_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_STACK, (mem, mem))
        resource.setrlimit(resource.RLIMIT_FSIZE, (64 << 20, 64 << 20))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    return f


def run_one(cmd, cwd, inp, tl_ms, ml_mb, extra_mem_mb=0):
    """Chạy chương trình với input `inp`. Trả về dict: status, time(ms), mem(KB), out, err."""
    in_path = os.path.join(cwd, "input.txt")
    out_path = os.path.join(cwd, "output.txt")
    err_path = os.path.join(cwd, "stderr.txt")
    with open(in_path, "w") as f:
        f.write(inp)
    cpu_sec = int(tl_ms / 1000) + 1
    with open(in_path) as fi, open(out_path, "w") as fo, open(err_path, "w") as fe:
        start = time.monotonic()
        proc = subprocess.Popen(cmd, cwd=cwd, stdin=fi, stdout=fo, stderr=fe,
                                preexec_fn=_limits(cpu_sec, ml_mb + extra_mem_mb))
        wall_limit = tl_ms / 1000 * 2.5 + 0.5
        killed = False
        while True:
            pid, status, ru = os.wait4(proc.pid, os.WNOHANG)
            if pid:
                break
            if time.monotonic() - start > wall_limit:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                killed = True
                pid, status, ru = os.wait4(proc.pid, 0)
                break
            time.sleep(0.002)
        proc.returncode = 0  # đã wait4 thủ công, tránh Popen wait lại
    cpu_ms = int((ru.ru_utime + ru.ru_stime) * 1000)
    mem_kb = ru.ru_maxrss
    with open(out_path, errors="replace") as f:
        out = f.read()
    with open(err_path, errors="replace") as f:
        err = f.read(4000)

    res = {"time": cpu_ms, "mem": mem_kb, "out": out, "err": err}
    sig = os.WTERMSIG(status) if os.WIFSIGNALED(status) else 0
    code = os.WEXITSTATUS(status) if os.WIFEXITED(status) else -sig
    if killed or sig == signal.SIGXCPU or cpu_ms > tl_ms:
        res["status"] = "TLE"
        res["time"] = max(cpu_ms, tl_ms)
    elif mem_kb > ml_mb * 1024 or (code != 0 and ("bad_alloc" in err or "MemoryError" in err)):
        res["status"] = "MLE"
    elif code != 0:
        res["status"] = "RE"
        res["exit"] = code
    else:
        res["status"] = "OK"
    return res


def check_tokens(expected, got):
    """Checker giống `wcmp` của Codeforces. Trả về (ok, message)."""
    a, b = expected.split(), got.split()
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return False, (f"{_ord(i + 1)} words differ - expected: '{_short(a[i])}', "
                           f"found: '{_short(b[i])}'")
    if len(a) > len(b):
        return False, f"Unexpected EOF in the participant output (expected {len(a)} tokens, found {len(b)})"
    if len(b) > len(a):
        return False, f"Extra tokens in the participant output (expected {len(a)} tokens, found {len(b)})"
    return True, f"{len(a)} tokens"


def check_float(expected, got, eps=1e-6):
    """So sánh số thực với sai số tuyệt đối hoặc tương đối eps."""
    a, b = expected.split(), got.split()
    if len(a) != len(b):
        return False, f"expected {len(a)} numbers, found {len(b)}"
    for i, (x, y) in enumerate(zip(a, b)):
        try:
            fx, fy = float(x), float(y)
        except ValueError:
            return False, f"{_ord(i + 1)} token is not a number: '{_short(y)}'"
        if not (abs(fx - fy) <= eps or abs(fx - fy) <= eps * abs(fx)):
            return False, f"{_ord(i + 1)} numbers differ - expected: '{x}', found: '{_short(y)}', error = {abs(fx - fy):.3g}"
    return True, f"{len(a)} numbers"


CHECKERS = {"tokens": check_tokens, "float": check_float}


def _ord(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def _short(s, n=40):
    return s if len(s) <= n else s[:n] + "..."


def _clip(s, n=400):
    return s if len(s) <= n else s[:n] + "\n..."


VERDICT_TEXT = {"TLE": "Time limit exceeded", "MLE": "Memory limit exceeded", "RE": "Runtime error",
                "WA": "Wrong answer"}


def judge(code, lang, tests, tl_ms=1000, ml_mb=256, stop_on_fail=True, checker="tokens"):
    """Chấm `code` trên danh sách tests [(input, expected_output)]."""
    if lang not in LANGS:
        return {"verdict": "Unknown language", "ok": False, "tests": []}
    L = LANGS[lang]
    tl = int(tl_ms * L["tl_mult"])
    with _slots:
        wd = tempfile.mkdtemp(prefix="judge_")
        try:
            with open(os.path.join(wd, L["file"]), "w") as f:
                f.write(code)
            if L["compile"]:
                try:
                    c = subprocess.run(L["compile"], cwd=wd, capture_output=True, text=True, timeout=60)
                except subprocess.TimeoutExpired:
                    return {"verdict": "Compilation error", "ok": False, "compile": "Biên dịch quá lâu", "tests": []}
                if c.returncode != 0:
                    return {"verdict": "Compilation error", "ok": False,
                            "compile": _clip(c.stderr, 4000), "tests": []}
            elif lang == "py":
                c = subprocess.run(["python3", "-m", "py_compile", L["file"]], cwd=wd,
                                   capture_output=True, text=True, timeout=30)
                if c.returncode != 0:
                    return {"verdict": "Compilation error", "ok": False,
                            "compile": _clip(c.stderr, 4000), "tests": []}
            results, max_t, max_m = [], 0, 0
            verdict = "Accepted"
            extra = 64 if lang == "py" else 0
            for i, (inp, exp) in enumerate(tests, 1):
                r = run_one(L["run"], wd, inp, tl, ml_mb, extra)
                max_t, max_m = max(max_t, r["time"]), max(max_m, r["mem"])
                item = {"test": i, "time": r["time"], "mem": r["mem"], "input": _clip(inp),
                        "output": _clip(r["out"]), "answer": _clip(exp)}
                if r["status"] == "OK":
                    ok, msg = CHECKERS[checker](exp, r["out"])
                    item["status"] = "OK" if ok else "WA"
                    item["checker"] = ("ok " if ok else "wrong answer ") + msg
                else:
                    item["status"] = r["status"]
                    item["checker"] = r["err"][-1500:] if r["status"] == "RE" else ""
                    if "exit" in r:
                        item["checker"] = f"Exit code {r['exit']}\n" + item["checker"]
                results.append(item)
                if item["status"] != "OK":
                    verdict = f"{VERDICT_TEXT[item['status']]} on test {i}"
                    if stop_on_fail:
                        break
            return {"verdict": verdict, "ok": verdict == "Accepted", "time": max_t, "mem": max_m,
                    "tests": results, "total": len(tests)}
        finally:
            shutil.rmtree(wd, ignore_errors=True)


def run_custom(code, lang, inp, tl_ms=2000, ml_mb=256):
    """Chạy thử với input tự nhập (giống Custom invocation của Codeforces)."""
    r = judge(code, lang, [(inp, "")], tl_ms, ml_mb, stop_on_fail=True)
    if r.get("tests"):
        t = r["tests"][0]
        st = t["status"]
        return {"verdict": "OK" if st in ("OK", "WA") else VERDICT_TEXT.get(st, st),
                "time": t["time"], "mem": t["mem"], "output": t["output"] if st in ("OK", "WA") else "",
                "error": t["checker"] if st not in ("OK", "WA") else ""}
    return {"verdict": r["verdict"], "error": r.get("compile", ""), "output": ""}
