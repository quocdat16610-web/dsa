#!/usr/bin/env python3
"""Sinh sẵn bộ test (song song nhiều tiến trình).

    python3 tools/build_tests.py           # tất cả
    python3 tools/build_tests.py 03 17     # chỉ chuyên đề 03 và 17
"""
import os
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _one(pid):
    from problems import get_tests
    t = time.time()
    get_tests(pid)
    return pid, time.time() - t


def main(topics):
    os.environ.setdefault("DSA_CACHE_GB", "100")
    from problems import PROBLEMS
    pids = sorted(p for p in PROBLEMS if not topics or p[:2] in topics)
    with Pool(os.cpu_count() or 2) as pool:
        for pid, dt in pool.imap_unordered(_one, pids):
            print(f"{pid} {dt:5.1f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
