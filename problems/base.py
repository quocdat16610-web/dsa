"""Khung định nghĩa bài tập.

Mỗi bài gồm: đề bài, các input mẫu, hàm sinh test `gen(r, s)` và lời giải mẫu `sol(inp)`.
- `r` là random.Random đã seed cố định theo mã bài -> test luôn giống nhau giữa các lần chạy.
- `s` là hệ số kích thước trong [0, 1]; s = 1 là test lớn nhất (dùng để bắt TLE).
- `sol` nhận chuỗi input, trả về chuỗi / số / list (list sẽ được in mỗi phần tử một dòng).
- `brute` (tuỳ chọn) là lời giải trâu, dùng để tự kiểm tra `sol` trên test nhỏ.
"""
import random
import types

LEVELS = {1: "Cơ bản", 2: "Dễ", 3: "Trung bình", 4: "Khá", 5: "Nâng cao"}

PROBLEMS = {}   # pid -> Problem
_counter = {}

# Hệ số kích thước của các test sinh tự động (sau các test mẫu)
SCALES = [0.0, 0.0, 0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 0.85, 1.0, 1.0, 1.0]


class Problem:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def summary(self):
        return {"id": self.id, "topic": self.topic, "title": self.title,
                "level": self.level, "tags": list(self.tags)}

    def public(self):
        d = self.summary()
        d.update(statement=self.statement, input=self.inp, output=self.out,
                 samples=[{"input": i, "output": norm(self.sol(i))} for i in self.samples],
                 tl=self.tl, ml=self.ml, note=self.note, checker=self.checker)
        return d


def _freeze(f):
    """Chụp lại globals của module tại thời điểm gọi add().

    Trong các file đề, tên `_g`, `_sol`, `_br` được định nghĩa lại cho mỗi bài; lambda/hàm tham chiếu
    các tên này phải dùng phiên bản ngay trước add() chứ không phải phiên bản cuối file.
    """
    if f is None or not isinstance(f, types.FunctionType):
        return f
    return types.FunctionType(f.__code__, dict(f.__globals__), f.__name__, f.__defaults__, f.__closure__)


def add(topic, title, level, statement, inp, out, samples, gen, sol, *,
        tags=(), tl=1000, ml=256, brute=None, note="", scales=None, checker="tokens"):
    idx = _counter.get(topic, 0) + 1
    _counter[topic] = idx
    pid = f"{topic:02d}{idx:02d}"
    if isinstance(samples, str):
        samples = [samples]
    PROBLEMS[pid] = Problem(id=pid, topic=topic, title=title, level=level,
                            statement=statement.strip(), inp=inp.strip(), out=out.strip(),
                            samples=[s if s.endswith("\n") else s + "\n" for s in samples],
                            gen=_freeze(gen), sol=_freeze(sol), tags=tuple(tags), tl=tl, ml=ml,
                            brute=_freeze(brute), note=note.strip(), scales=scales or SCALES, checker=checker)
    return PROBLEMS[pid]


def norm(x):
    """Chuẩn hoá kết quả của lời giải mẫu thành chuỗi."""
    if isinstance(x, (list, tuple)):
        x = "\n".join(map(str, x))
    x = str(x)
    return x if x.endswith("\n") else x + "\n"


def make_tests(p):
    r = random.Random("seed-" + p.id)
    inputs = list(p.samples)
    for s in p.scales:
        t = p.gen(r, s)
        inputs.append(t if t.endswith("\n") else t + "\n")
    return [(i, norm(p.sol(i))) for i in inputs]


# ----------------------------------------------------------------- tiện ích
class Rd:
    """Đọc token từ chuỗi input."""
    def __init__(self, s):
        self.t = s.split()
        self.i = 0

    def int(self):
        self.i += 1
        return int(self.t[self.i - 1])

    def ints(self, n):
        self.i += n
        return list(map(int, self.t[self.i - n:self.i]))

    def str(self):
        self.i += 1
        return self.t[self.i - 1]

    def strs(self, n):
        self.i += n
        return self.t[self.i - n:self.i]


def S(s, lo, hi):
    """Kích thước theo hệ số s, nằm trong [lo, hi]."""
    return max(lo, min(hi, int(lo + (hi - lo) * s)))


def J(*a):
    return " ".join(map(str, a))


def L(a):
    return " ".join(map(str, a))


def arr(r, n, lo, hi):
    return [r.randint(lo, hi) for _ in range(n)]


def lines(*rows):
    return "\n".join(rows) + "\n"


def rstr(r, n, alpha="abc"):
    return "".join(r.choice(alpha) for _ in range(n))


def rtree(r, n):
    """Cây ngẫu nhiên n đỉnh (1..n), trả về list cạnh (u, v)."""
    e = []
    for v in range(2, n + 1):
        lo = max(1, v - r.choice([1, 3, 10, v]))
        e.append((r.randint(lo, v - 1), v))
    perm = list(range(1, n + 1))
    r.shuffle(perm)
    perm = [0] + perm
    e = [(perm[a], perm[b]) for a, b in e]
    r.shuffle(e)
    return [(a, b) if r.random() < .5 else (b, a) for a, b in e]


def rgraph(r, n, m, connected=False, simple=True):
    """Đồ thị vô hướng n đỉnh m cạnh (không khuyên, không cạnh lặp nếu simple)."""
    m = min(m, n * (n - 1) // 2) if simple else m
    es, seen = [], set()
    if connected:
        for a, b in rtree(r, n):
            es.append((a, b)); seen.add((min(a, b), max(a, b)))
    tries = 0
    while len(es) < m and tries < 20 * m + 100:
        tries += 1
        a, b = r.randint(1, n), r.randint(1, n)
        if a == b:
            continue
        k = (min(a, b), max(a, b))
        if simple and k in seen:
            continue
        seen.add(k); es.append((a, b))
    r.shuffle(es)
    return es


def rdigraph(r, n, m, dag=False):
    es, seen = [], set()
    order = list(range(1, n + 1)); r.shuffle(order)
    pos = {v: i for i, v in enumerate(order)}
    m = min(m, n * (n - 1) // (2 if dag else 1))
    tries = 0
    while len(es) < m and tries < 20 * m + 100:
        tries += 1
        a, b = r.randint(1, n), r.randint(1, n)
        if a == b or (a, b) in seen:
            continue
        if dag and pos[a] > pos[b]:
            a, b = b, a
            if (a, b) in seen:
                continue
        seen.add((a, b)); es.append((a, b))
    return es


class SortedList:
    """Danh sách có thứ tự (chia căn), dùng cho lời giải mẫu thay cho multiset của C++."""
    B = 700

    def __init__(self, it=()):
        a = sorted(it)
        self.b = [a[i:i + self.B] for i in range(0, len(a), self.B)] or [[]]
        self.n = len(a)

    def __len__(self):
        return self.n

    def _blk(self, x, right=False):
        import bisect
        for i, blk in enumerate(self.b):
            if blk and (blk[-1] > x if right else blk[-1] >= x):
                return i
        return len(self.b) - 1

    def add(self, x):
        import bisect
        i = self._blk(x, True)
        bisect.insort(self.b[i], x)
        self.n += 1
        if len(self.b[i]) > 2 * self.B:
            blk = self.b[i]
            self.b[i:i + 1] = [blk[:self.B], blk[self.B:]]

    def remove(self, x):
        import bisect
        i = self._blk(x)
        blk = self.b[i]
        j = bisect.bisect_left(blk, x)
        if j == len(blk) or blk[j] != x:
            raise ValueError(x)
        blk.pop(j)
        self.n -= 1
        if not blk and len(self.b) > 1:
            self.b.pop(i)

    def bisect_left(self, x):
        import bisect
        c = 0
        for blk in self.b:
            if blk and blk[-1] >= x:
                return c + bisect.bisect_left(blk, x)
            c += len(blk)
        return c

    def bisect_right(self, x):
        import bisect
        c = 0
        for blk in self.b:
            if blk and blk[-1] > x:
                return c + bisect.bisect_right(blk, x)
            c += len(blk)
        return c

    def __getitem__(self, k):
        if k < 0:
            k += self.n
        for blk in self.b:
            if k < len(blk):
                return blk[k]
            k -= len(blk)
        raise IndexError

    def pop(self, k):
        if k < 0:
            k += self.n
        for i, blk in enumerate(self.b):
            if k < len(blk):
                v = blk.pop(k)
                self.n -= 1
                if not blk and len(self.b) > 1:
                    self.b.pop(i)
                return v
            k -= len(blk)
        raise IndexError
