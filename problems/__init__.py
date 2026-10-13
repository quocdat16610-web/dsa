"""Nạp toàn bộ bài tập và quản lý bộ test (cache nén gzip trên đĩa, tự dọn khi vượt dung lượng)."""
import gzip
import hashlib
import importlib
import inspect
import json
import os
import pkgutil
import threading

from .base import PROBLEMS, LEVELS, make_tests  # noqa: F401

_HERE = os.path.dirname(__file__)
CACHE_DIR = os.environ.get("DSA_TEST_CACHE", os.path.join(os.path.dirname(_HERE), "data", "tests"))
CACHE_LIMIT = int(float(os.environ.get("DSA_CACHE_GB", "2")) * (1 << 30))
_MODULE_HASH = {}
with open(os.path.join(_HERE, "base.py"), encoding="utf-8") as _f:
    _BASE_SRC = _f.read()

for _m in sorted(pkgutil.iter_modules([_HERE]), key=lambda m: m.name):
    if _m.name.startswith("t") and _m.name[1:3].isdigit():
        _mod = importlib.import_module(f"{__name__}.{_m.name}")
        _MODULE_HASH[_mod.T] = hashlib.sha1((_BASE_SRC + inspect.getsource(_mod)).encode()).hexdigest()[:12]

_locks = {}
_locks_guard = threading.Lock()
_mem = {}


def by_topic(topic):
    return [p for p in PROBLEMS.values() if p.topic == topic]


def _path(pid):
    return os.path.join(CACHE_DIR, f"{pid}.json.gz")


def is_cached(pid):
    path = _path(pid)
    if not os.path.exists(path):
        return False
    try:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            head = f.read(64)
        return f'"{_MODULE_HASH[PROBLEMS[pid].topic]}"' in head
    except OSError:
        return False


def _evict(keep):
    """Xoá các file test ít dùng gần đây nhất khi cache vượt CACHE_LIMIT."""
    try:
        files = [os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR) if f.endswith(".json.gz")]
        info = sorted(((os.path.getmtime(f), os.path.getsize(f), f) for f in files))
    except OSError:
        return
    total = sum(sz for _, sz, _ in info)
    for _, sz, f in info:
        if total <= CACHE_LIMIT:
            break
        if f == keep:
            continue
        try:
            os.remove(f); total -= sz
        except OSError:
            pass


def get_tests(pid):
    """Trả về list (input, output). Sinh lần đầu rồi lưu vào data/tests/ (nén gzip)."""
    p = PROBLEMS[pid]
    ver = _MODULE_HASH[p.topic]
    if pid in _mem and _mem[pid][0] == ver:
        return _mem[pid][1]
    with _locks_guard:
        lock = _locks.setdefault(pid, threading.Lock())
    with lock:
        if pid in _mem and _mem[pid][0] == ver:
            return _mem[pid][1]
        path = _path(pid)
        tests = None
        if os.path.exists(path):
            try:
                with gzip.open(path, "rt", encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("version") == ver:
                    tests = [tuple(t) for t in d["tests"]]
                    os.utime(path)
            except (OSError, ValueError, EOFError):
                tests = None
        if tests is None:
            tests = make_tests(p)
            os.makedirs(CACHE_DIR, exist_ok=True)
            tmp = path + f".{threading.get_ident()}.tmp"
            with gzip.open(tmp, "wt", encoding="utf-8", compresslevel=3) as f:
                json.dump({"version": ver, "tests": tests}, f)
            os.replace(tmp, path)
            _evict(path)
        if len(_mem) > 20:
            _mem.clear()
        _mem[pid] = (ver, tests)
        return tests
