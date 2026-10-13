"""Nạp toàn bộ bài tập và quản lý bộ test (có cache trên đĩa)."""
import hashlib
import importlib
import inspect
import json
import os
import pkgutil
import threading

from .base import PROBLEMS, LEVELS, make_tests  # noqa: F401

_HERE = os.path.dirname(__file__)
CACHE_DIR = os.path.join(os.path.dirname(_HERE), "data", "tests")
_MODULE_HASH = {}
with open(os.path.join(_HERE, "base.py"), encoding="utf-8") as _f:
    _BASE_SRC = _f.read()

for _m in sorted(pkgutil.iter_modules([_HERE]), key=lambda m: m.name):
    if _m.name.startswith("t") and _m.name[1:3].isdigit():
        _mod = importlib.import_module(f"{__name__}.{_m.name}")
        _MODULE_HASH[_mod.T] = hashlib.sha1((_BASE_SRC + inspect.getsource(_mod)).encode()).hexdigest()[:12]

_locks = {}
_mem = {}


def by_topic(topic):
    return [p for p in PROBLEMS.values() if p.topic == topic]


def get_tests(pid):
    """Trả về list (input, output). Sinh lần đầu rồi lưu vào data/tests/."""
    p = PROBLEMS[pid]
    ver = _MODULE_HASH[p.topic]
    if pid in _mem and _mem[pid][0] == ver:
        return _mem[pid][1]
    lock = _locks.setdefault(pid, threading.Lock())
    with lock:
        if pid in _mem and _mem[pid][0] == ver:
            return _mem[pid][1]
        path = os.path.join(CACHE_DIR, f"{pid}.json")
        tests = None
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("version") == ver:
                    tests = [tuple(t) for t in d["tests"]]
            except (OSError, ValueError):
                tests = None
        if tests is None:
            tests = make_tests(p)
            os.makedirs(CACHE_DIR, exist_ok=True)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump({"version": ver, "tests": tests}, f)
            os.replace(tmp, path)
        _mem.clear() if len(_mem) > 40 else None
        _mem[pid] = (ver, tests)
        return tests
