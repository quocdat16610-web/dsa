"""Kiểm tra toàn bộ ngân hàng bài tập.

    python3 tests/validate.py            # tất cả
    python3 tests/validate.py 03 0405    # chỉ chuyên đề 03 và bài 0405

- Sinh toàn bộ test, đo thời gian lời giải mẫu.
- Với bài có `brute`: đối chiếu lời giải mẫu với lời giải trâu trên 40 test nhỏ.
- Kiểm tra test mẫu có output khớp, input không rỗng.
"""
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from problems import PROBLEMS, get_tests  # noqa: E402
from problems.base import norm  # noqa: E402


def main(filters):
    bad = 0
    total_t = 0
    for pid, p in sorted(PROBLEMS.items()):
        if filters and not any(pid.startswith(f) for f in filters):
            continue
        t0 = time.time()
        try:
            tests = get_tests(pid)
            assert all(i.strip() for i, _ in tests), "input rỗng"
            if p.brute:
                r = random.Random(1)
                for k in range(40):
                    inp = p.gen(r, 0.0)
                    inp = inp if inp.endswith("\n") else inp + "\n"
                    a, b = norm(p.sol(inp)), norm(p.brute(inp))
                    assert a.split() == b.split(), f"sol != brute\ninput:\n{inp[:300]}\nsol: {a[:200]}\nbrute: {b[:200]}"
                for inp in p.samples:
                    assert norm(p.sol(inp)).split() == norm(p.brute(inp)).split(), "sample sol != brute"
            dt = time.time() - t0
            total_t += dt
            mx = max(len(i) for i, _ in tests)
            flag = "  CHẬM" if dt > 15 else ""
            print(f"{pid} L{p.level} {p.title[:40]:40s} {len(tests):2d} tests  max_in={mx:>8d}B  {dt:5.1f}s{flag}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"{pid} LỖI: {type(e).__name__}: {e}")
    print(f"\nTổng: {len(PROBLEMS)} bài, lỗi: {bad}, thời gian: {total_t:.0f}s")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
