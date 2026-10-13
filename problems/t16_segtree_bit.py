"""Chuyên đề 16: Cây phân đoạn (Segment Tree), cây Fenwick (BIT), đường quét (Sweep line)."""
from bisect import bisect_left, bisect_right
from .base import add, Rd, S, J, L, arr, lines

T = 16


class BIT:
    def __init__(self, n):
        self.n = n; self.t = [0] * (n + 1)

    def add(self, i, v):  # 1-based
        t, n = self.t, self.n
        while i <= n:
            t[i] += v; i += i & -i

    def sum(self, i):
        t, s = self.t, 0
        while i > 0:
            s += t[i]; i -= i & -i
        return s

    def kth(self, k):  # vị trí nhỏ nhất có tổng tiền tố ≥ k
        pos, LOG = 0, self.n.bit_length()
        for j in range(LOG, -1, -1):
            np_ = pos + (1 << j)
            if np_ <= self.n and self.t[np_] < k:
                pos = np_; k -= self.t[np_]
        return pos + 1


class Seg:
    """Cây phân đoạn lặp (bottom-up) cho phép toán kết hợp op với phần tử đơn vị e."""

    def __init__(self, a, op, e):
        n = 1
        while n < len(a):
            n *= 2
        self.n, self.op, self.e = n, op, e
        self.t = [e] * (2 * n)
        self.t[n:n + len(a)] = a
        for i in range(n - 1, 0, -1):
            self.t[i] = op(self.t[2 * i], self.t[2 * i + 1])

    def set(self, i, v):  # 0-based
        t, op = self.t, self.op
        i += self.n; t[i] = v; i //= 2
        while i:
            t[i] = op(t[2 * i], t[2 * i + 1]); i //= 2

    def query(self, l, r):  # [l, r)
        op = self.op; resl = resr = self.e; t = self.t
        l += self.n; r += self.n
        while l < r:
            if l & 1:
                resl = op(resl, t[l]); l += 1
            if r & 1:
                r -= 1; resr = op(t[r], resr)
            l //= 2; r //= 2
        return op(resl, resr)


class LazyAddMin:
    """Cộng trên đoạn, min trên đoạn (cây phân đoạn lười, đệ quy-free theo kiểu ACL)."""

    def __init__(self, a):
        n = len(a); self.size = 1
        while self.size < n:
            self.size *= 2
        self.log = self.size.bit_length() - 1
        INF = float("inf")
        self.d = [INF] * (2 * self.size); self.lz = [0] * self.size
        self.d[self.size:self.size + n] = a
        for i in range(self.size - 1, 0, -1):
            self.d[i] = min(self.d[2 * i], self.d[2 * i + 1])

    def _apply(self, k, v):
        self.d[k] += v
        if k < self.size:
            self.lz[k] += v

    def _push(self, k):
        if self.lz[k]:
            self._apply(2 * k, self.lz[k]); self._apply(2 * k + 1, self.lz[k]); self.lz[k] = 0

    def _upd(self, k):
        self.d[k] = min(self.d[2 * k], self.d[2 * k + 1])

    def range_add(self, l, r, v):  # [l, r)
        l += self.size; r += self.size
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._apply(l, v); l += 1
            if r & 1:
                r -= 1; self._apply(r, v)
            l >>= 1; r >>= 1
        l, r = l2, r2
        for i in range(1, self.log + 1):
            if ((l >> i) << i) != l:
                self._upd(l >> i)
            if ((r >> i) << i) != r:
                self._upd((r - 1) >> i)

    def range_min(self, l, r):
        l += self.size; r += self.size
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)
        res = float("inf")
        while l < r:
            if l & 1:
                res = min(res, self.d[l]); l += 1
            if r & 1:
                r -= 1; res = min(res, self.d[r])
            l >>= 1; r >>= 1
        return res


def _qs(r, n, q):
    out = []
    for _ in range(q):
        a, b = r.randint(1, n), r.randint(1, n)
        out.append((min(a, b), max(a, b)))
    return out


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    ops = []
    for _ in range(q):
        if r.random() < .5:
            ops.append(J(1, r.randint(1, n), r.randint(1, 10**9)))
        else:
            a, b = _qs(r, n, 1)[0]; ops.append(J(2, a, b))
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = [0] + rd.ints(n)
    b = BIT(n)
    for i in range(1, n + 1):
        b.add(i, a[i])
    out = []
    for _ in range(q):
        t, x, y = rd.ints(3)
        if t == 1:
            b.add(x, y - a[x]); a[x] = y
        else:
            out.append(b.sum(y) - b.sum(x - 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = [0] + rd.ints(n); out = []
    for _ in range(q):
        t, x, y = rd.ints(3)
        if t == 1:
            a[x] = y
        else:
            out.append(sum(a[x:y + 1]))
    return out


add(T, "Tổng đoạn có cập nhật", 1, """
Cho dãy `a` và `q` thao tác:
- `1 k u`: gán `a_k = u`;
- `2 l r`: in tổng `a_l + ... + a_r`.

Gợi ý: mảng cộng dồn bị hỏng khi có cập nhật. Dùng **cây Fenwick (BIT)**: `add(i, v)` và `sum(i)` đều `O(log n)`.
Gán `a_k = u` tương đương cộng thêm `u - a_k`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau là các thao tác.",
    "Kết quả các thao tác loại 2.", ["5 4\n1 2 3 4 5\n2 1 5\n1 3 10\n2 2 4\n2 3 3\n"], _g, _sol, brute=_br, tags=["BIT"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    st = Seg(a, min, float("inf")); out = []
    for _ in range(q):
        t, x, y = rd.ints(3)
        if t == 1:
            st.set(x - 1, y)
        else:
            out.append(st.query(x - 1, y))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = [0] + rd.ints(n); out = []
    for _ in range(q):
        t, x, y = rd.ints(3)
        if t == 1:
            a[x] = y
        else:
            out.append(min(a[x:y + 1]))
    return out


add(T, "Min đoạn có cập nhật", 1, """
Cho dãy `a` và `q` thao tác:
- `1 k u`: gán `a_k = u`;
- `2 l r`: in min của `a_l..a_r`.

Gợi ý: **cây phân đoạn** — mỗi nút quản lý một đoạn và lưu min của đoạn đó. Cập nhật đi từ lá lên gốc, truy vấn ghép `O(log n)` nút.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau là các thao tác.",
    "Kết quả các thao tác loại 2.", ["5 4\n3 1 4 1 5\n2 1 5\n1 2 9\n2 1 3\n2 3 5\n"], _g, _sol, brute=_br, tags=["segment tree"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    ops = []
    for _ in range(q):
        if r.random() < .5:
            a, b = _qs(r, n, 1)[0]; ops.append(J(1, a, b, r.randint(1, 10**9)))
        else:
            ops.append(J(2, r.randint(1, n)))
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    b = BIT(n + 1); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            l, r_, u = rd.ints(3); b.add(l, u); b.add(r_ + 1, -u)
        else:
            k = rd.int(); out.append(a[k - 1] + b.sum(k))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            l, r_, u = rd.ints(3)
            for i in range(l - 1, r_):
                a[i] += u
        else:
            out.append(a[rd.int() - 1])
    return out


add(T, "Cộng đoạn, hỏi điểm", 2, """
Thao tác:
- `1 l r u`: cộng `u` vào mọi `a_l..a_r`;
- `2 k`: in giá trị `a_k`.

Gợi ý: BIT trên **mảng hiệu**: cộng đoạn = `add(l, u), add(r + 1, -u)`; giá trị tại `k` = `a_k ban đầu + sum(k)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau là các thao tác (1 ≤ u ≤ 10^9).",
    "Kết quả các thao tác loại 2.", ["4 4\n1 2 3 4\n1 1 3 5\n2 2\n1 2 4 1\n2 4\n"], _g, _sol, brute=_br, tags=["BIT", "mảng hiệu"])


# 4 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, r.choice([5, n, 10**9]))))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    vals = sorted(set(a)); idx = {v: i + 1 for i, v in enumerate(vals)}
    b = BIT(len(vals)); tot = 0
    for i, x in enumerate(a):
        tot += i - b.sum(idx[x])
        b.add(idx[x], 1)
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


add(T, "Đếm nghịch thế", 2, """
Đếm số cặp `i < j` mà `a_i > a_j`.

Gợi ý: nén giá trị về `1..m`. Duyệt từ trái sang phải; số phần tử đứng trước và lớn hơn `a_j` = `j - (số phần tử trước ≤ a_j)`,
đếm bằng BIT. (Cách khác: sắp xếp trộn — merge sort.)
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số nghịch thế.",
    ["5\n2 4 1 3 5\n"], _g, _sol, brute=_br, tags=["BIT", "nén số"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    b1, b2 = BIT(n + 1), BIT(n + 1)
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)

    def radd(l, r_, v):
        b1.add(l, v); b1.add(r_ + 1, -v); b2.add(l, v * (l - 1)); b2.add(r_ + 1, -v * r_)

    def psum(i):
        return b1.sum(i) * i - b2.sum(i) + pre[i]
    out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            l, r_, v = rd.ints(3); radd(l, r_, v)
        else:
            l, r_ = rd.ints(2); out.append(psum(r_) - psum(l - 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            l, r_, v = rd.ints(3)
            for i in range(l - 1, r_):
                a[i] += v
        else:
            l, r_ = rd.ints(2); out.append(sum(a[l - 1:r_]))
    return out


def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    ops = []
    for _ in range(q):
        a, b = _qs(r, n, 1)[0]
        ops.append(J(1, a, b, r.randint(-10**6, 10**6)) if r.random() < .5 else J(2, a, b))
    return lines(J(n, q), L(arr(r, n, -10**9, 10**9)), *ops)


add(T, "Cộng đoạn, tổng đoạn", 2, """
Thao tác:
- `1 l r v`: cộng `v` vào mọi `a_l..a_r`;
- `2 l r`: in tổng `a_l..a_r`.

Gợi ý: hai BIT `B1`, `B2`: cộng đoạn `[l, r]` ⇒ `B1.add(l, v), B1.add(r+1, -v), B2.add(l, v·(l-1)), B2.add(r+1, -v·r)`;
tổng tiền tố `[1, i]` = `B1.sum(i)·i - B2.sum(i)`. (Hoặc cây phân đoạn có lan truyền lười.)
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (|a_i| ≤ 10^9). `q` dòng sau là các thao tác (|v| ≤ 10^6).",
    "Kết quả các thao tác loại 2.", ["5 3\n1 2 3 4 5\n1 2 4 10\n2 1 5\n2 4 5\n"], _g, _sol, brute=_br, tags=["BIT", "lazy"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, m), L(arr(r, n, 1, 10**9)), L(arr(r, m, 1, r.choice([10**9, 10**9 // 2]))))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); h = rd.ints(n)
    size = 1
    while size < n:
        size *= 2
    t = [0] * (2 * size); t[size:size + n] = h
    for i in range(size - 1, 0, -1):
        t[i] = max(t[2 * i], t[2 * i + 1])
    out = []
    for g in rd.ints(m):
        if t[1] < g:
            out.append(0); continue
        i = 1
        while i < size:
            i = 2 * i if t[2 * i] >= g else 2 * i + 1
        out.append(i - size + 1)
        t[i] -= g; i //= 2
        while i:
            t[i] = max(t[2 * i], t[2 * i + 1]); i //= 2
    return L(out)


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); h = rd.ints(n); out = []
    for g in rd.ints(m):
        j = next((i for i in range(n) if h[i] >= g), -1)
        if j < 0:
            out.append(0)
        else:
            h[j] -= g; out.append(j + 1)
    return L(out)


add(T, "Đặt phòng khách sạn", 3, """
Có `n` khách sạn trên một con đường, khách sạn `i` còn `h_i` phòng trống. Lần lượt có `m` đoàn khách, đoàn thứ `j` cần `g_j` phòng và sẽ chọn
khách sạn **đầu tiên** (gần nhất) còn đủ phòng. In số hiệu khách sạn mỗi đoàn ở (0 nếu không có).

Gợi ý: cây phân đoạn lưu max số phòng; "đi xuống" từ gốc: nếu con trái có max ≥ g thì sang trái, ngược lại sang phải — `O(log n)`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). Dòng hai gồm `h_i`, dòng ba gồm `g_j` (1 ≤ giá trị ≤ 10^9).", "Một dòng gồm `m` số.",
    ["8 5\n3 2 4 1 5 5 2 6\n4 4 7 1 1\n"], _g, _sol, brute=_br, tags=["segment tree", "đi xuống trên cây"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, 10**9)), L(r.randint(1, n - i) for i in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    b = BIT(n)
    for i in range(1, n + 1):
        b.add(i, 1)
    out = []
    for p in rd.ints(n):
        k = b.kth(p); out.append(a[k - 1]); b.add(k, -1)
    return L(out)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return L(a.pop(p - 1) for p in rd.ints(n))


add(T, "Xoá khỏi danh sách", 3, """
Danh sách ban đầu gồm `n` số. Lần lượt thực hiện `n` thao tác: xoá phần tử đứng ở vị trí thứ `p` (đếm từ 1 trong danh sách **hiện tại**)
và in nó ra.

Gợi ý: BIT đánh dấu phần tử còn tồn tại (1) hay đã xoá (0). Phần tử thứ `p` là vị trí nhỏ nhất có tổng tiền tố bằng `p`
→ tìm bằng nhảy nhị phân trên BIT trong `O(log n)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a ≤ 10^9). Dòng ba gồm `n` vị trí `p` (hợp lệ tại thời điểm xoá).",
    "Một dòng gồm `n` số đã xoá.", ["5\n2 6 1 4 2\n3 1 3 1 1\n"], _g, _sol, brute=_br, tags=["BIT", "phần tử thứ k"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    hi = r.choice([100, 10**9])
    ops = []
    for _ in range(q):
        if r.random() < .5:
            ops.append(J("!", r.randint(1, n), r.randint(1, hi)))
        else:
            a, b = sorted((r.randint(1, hi), r.randint(1, hi))); ops.append(J("?", a, b))
    return lines(J(n, q), L(arr(r, n, 1, hi)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); p = rd.ints(n)
    ops = [(rd.str(), int(rd.str()), int(rd.str())) for _ in range(q)]
    vals = sorted(set(p) | {x for t, k, x in ops if t == "!"})
    idx = {v: i + 1 for i, v in enumerate(vals)}
    b = BIT(len(vals))
    for x in p:
        b.add(idx[x], 1)
    out = []
    for t, x, y in ops:
        if t == "!":
            b.add(idx[p[x - 1]], -1); p[x - 1] = y; b.add(idx[y], 1)
        else:
            out.append(b.sum(bisect_right(vals, y)) - b.sum(bisect_left(vals, x)))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); p = rd.ints(n); out = []
    for _ in range(q):
        t, x, y = rd.str(), int(rd.str()), int(rd.str())
        if t == "!":
            p[x - 1] = y
        else:
            out.append(sum(1 for v in p if x <= v <= y))
    return out


add(T, "Truy vấn lương", 3, """
Công ty có `n` nhân viên với mức lương `p_i`. Thao tác:
- `! k x`: lương nhân viên `k` đổi thành `x`;
- `? a b`: đếm số nhân viên có lương trong `[a, b]`.

Gợi ý: xử lý **offline** — đọc hết các thao tác để biết mọi giá trị lương xuất hiện, nén về `1..m`, rồi dùng BIT đếm số người theo mức lương.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `p_i`. `q` dòng sau là các thao tác (1 ≤ giá trị ≤ 10^9).",
    "Kết quả các thao tác `?`.", ["5 3\n3 7 2 2 5\n? 2 3\n! 3 6\n? 2 5\n"], _g, _sol, brute=_br, tags=["BIT", "offline", "nén số"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    ops = []
    for _ in range(q):
        a, b = _qs(r, n, 1)[0]
        ops.append(J(1, a, b, r.randint(-10**4, 10**4)) if r.random() < .5 else J(2, a, b))
    return lines(J(n, q), L(arr(r, n, -10**9, 10**9)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    st = LazyAddMin(a); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            l, r_, v = rd.ints(3); st.range_add(l - 1, r_, v)
        else:
            l, r_ = rd.ints(2); out.append(st.range_min(l - 1, r_))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            l, r_, v = rd.ints(3)
            for i in range(l - 1, r_):
                a[i] += v
        else:
            l, r_ = rd.ints(2); out.append(min(a[l - 1:r_]))
    return out


add(T, "Cộng đoạn, min đoạn (lan truyền lười)", 4, """
Thao tác:
- `1 l r v`: cộng `v` vào mọi `a_l..a_r`;
- `2 l r`: in min của `a_l..a_r`.

Gợi ý: cây phân đoạn với **lan truyền lười** (lazy propagation): mỗi nút lưu thêm `lazy` = lượng cần cộng cho cả đoạn nhưng chưa đẩy xuống con.
Chỉ đẩy (`push`) khi cần đi xuống. Mỗi thao tác `O(log n)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` số (|a_i| ≤ 10^9). `q` dòng sau là các thao tác (|v| ≤ 10^4).",
    "Kết quả các thao tác loại 2.", ["5 4\n5 3 8 6 1\n2 1 4\n1 2 3 -4\n2 1 5\n2 3 5\n"], _g, _sol, brute=_br, tags=["segment tree", "lazy"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, r.choice([3, 100, n, 10**9]))
    return lines(J(n, q), L(a), *(J(x, y) for x, y in _qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    qs = sorted(((rd.ints(2), i) for i in range(q)), key=lambda x: x[0][1])
    b = BIT(n); last = {}; ans = [0] * q; j = 0
    for i, x in enumerate(a, 1):
        if x in last:
            b.add(last[x], -1)
        last[x] = i; b.add(i, 1)
        while j < q and qs[j][0][1] == i:
            (l, r_), k = qs[j]; ans[k] = b.sum(r_) - b.sum(l - 1); j += 1
    return ans


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r_ = rd.ints(2); out.append(len(set(a[l - 1:r_])))
    return out


add(T, "Số giá trị phân biệt trên đoạn", 4, """
Với mỗi truy vấn `(l, r)`, đếm số giá trị khác nhau trong `a_l..a_r`.

Gợi ý (offline): sắp xếp truy vấn theo `r`. Duyệt `i` từ trái sang phải, chỉ giữ dấu `1` tại **lần xuất hiện cuối cùng** của mỗi giá trị
(xoá dấu ở lần xuất hiện trước). Khi tới `i = r`, đáp án các truy vấn có đầu phải `r` là tổng dấu trên `[l, r]` — dùng BIT.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["5 3\n3 2 3 1 2\n1 3\n2 4\n1 5\n"], _g, _sol, brute=_br, tags=["BIT", "offline"])


# 11 ----------------------------------------------------------------------
def _node(x):
    return (x, max(x, 0), max(x, 0), max(x, 0))  # tổng, max tiền tố, max hậu tố, max đoạn con (cho phép rỗng)


def _merge(a, b):
    return (a[0] + b[0], max(a[1], a[0] + b[1]), max(b[2], b[0] + a[2]), max(a[3], b[3], a[2] + b[1]))


def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    return lines(J(n, q), L(arr(r, n, -10**9, 10**9)), *(J(r.randint(1, n), r.randint(-10**9, 10**9)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    st = Seg([_node(x) for x in a], _merge, (0, 0, 0, 0)); out = []
    for _ in range(q):
        k, x = rd.ints(2); st.set(k - 1, _node(x)); out.append(st.t[1][3])
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        k, x = rd.ints(2); a[k - 1] = x
        best = cur = 0
        for v in a:
            cur = max(0, cur + v); best = max(best, cur)
        out.append(best)
    return out


add(T, "Đoạn con tổng lớn nhất có cập nhật", 4, """
Sau mỗi thao tác gán `a_k = x`, in tổng lớn nhất của một đoạn con liên tiếp (cho phép đoạn rỗng, tổng 0).

Gợi ý: mỗi nút cây phân đoạn lưu 4 giá trị: tổng, max tiền tố, max hậu tố, max đoạn con. Ghép hai nút `A`, `B`:
`best = max(A.best, B.best, A.suf + B.pre)` ...
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` số (|a_i| ≤ 10^9). `q` dòng sau mỗi dòng `k x`.",
    "Sau mỗi thao tác in một dòng.", ["5 3\n1 2 -3 5 -1\n2 6\n3 -2\n5 1\n"], _g, _sol, brute=_br, tags=["segment tree"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = r.choice([100, 10**9])
    segs = []
    for _ in range(n):
        a = r.randint(0, hi); segs.append(J(a, min(hi, a + r.randint(1, max(1, hi // r.choice([5, 100, 10**4]))))))
    return lines(str(n), *segs)


def _sol(s):
    rd = Rd(s); n = rd.int()
    segs = sorted(tuple(rd.ints(2)) for _ in range(n))
    tot, cl, cr = 0, None, None
    for a, b in segs:
        if cr is None or a > cr:
            if cr is not None:
                tot += cr - cl
            cl, cr = a, b
        else:
            cr = max(cr, b)
    return tot + (cr - cl)


def _br(s):
    rd = Rd(s); n = rd.int(); segs = [rd.ints(2) for _ in range(n)]
    if max(b for _, b in segs) > 2000:
        return _sol(s)
    cov = set()
    for a, b in segs:
        cov.update(range(a, b))
    return len(cov)


add(T, "Độ dài phủ", 2, """
Có `n` đoạn thẳng `[a_i, b_i]` trên trục số (`a_i < b_i`). Tính tổng độ dài phần trục số được phủ bởi ít nhất một đoạn.

Gợi ý (đường quét): sắp xếp theo đầu trái, gộp các đoạn chồng nhau; hoặc quét qua các sự kiện "mở/đóng" và cộng độ dài khi bộ đếm > 0.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `a b` (0 ≤ a < b ≤ 10^9).", "Tổng độ dài.",
    ["3\n1 5\n3 7\n10 12\n"], _g, _sol, brute=_br, tags=["sweep line"])


# 13 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int()
    ev = []
    for _ in range(n):
        a, b = rd.ints(2); ev.append((a, 1)); ev.append((b, -1))
    ev.sort(key=lambda e: (e[0], e[1]))  # đóng trước mở tại cùng thời điểm
    cur = best = 0
    for _, d in ev:
        cur += d; best = max(best, cur)
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); segs = [rd.ints(2) for _ in range(n)]
    pts = {a for a, _ in segs}
    return max(sum(1 for a, b in segs if a <= p < b) for p in pts)


add(T, "Nhiều khách nhất cùng lúc", 2, """
Nhà hàng có `n` khách, khách `i` đến lúc `a_i` và rời đi lúc `b_i` (khách rời đi lúc `t` và khách đến lúc `t` **không** gặp nhau).
Hỏi lúc đông nhất có bao nhiêu khách?

Gợi ý: tạo sự kiện `(a_i, +1)` và `(b_i, -1)`, sắp xếp theo thời gian (cùng thời điểm thì `-1` trước), quét và theo dõi bộ đếm.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `a b` (0 ≤ a < b ≤ 10^9).", "Số khách nhiều nhất.",
    ["3\n5 8\n2 4\n3 9\n"], _g, _sol, brute=_br, tags=["sweep line"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 1000)
    hi = r.choice([20, 10**4, 10**9])
    out = []
    for _ in range(n):
        x1, y1 = r.randint(0, hi - 1), r.randint(0, hi - 1)
        out.append(J(x1, y1, r.randint(x1 + 1, min(hi, x1 + max(1, hi // r.choice([2, 10, 100])))),
                     r.randint(y1 + 1, min(hi, y1 + max(1, hi // r.choice([2, 10, 100]))))))
    return lines(str(n), *out)


def _sol(s):
    rd = Rd(s); n = rd.int(); rects = [rd.ints(4) for _ in range(n)]
    ys = sorted({y for r_ in rects for y in (r_[1], r_[3])})
    yi = {y: i for i, y in enumerate(ys)}
    m = len(ys) - 1
    size = 1
    while size < max(1, m):
        size *= 2
    cnt = [0] * (2 * size); cov = [0] * (2 * size)
    lens = [0] * (2 * size)
    for i in range(m):
        lens[size + i] = ys[i + 1] - ys[i]
    for i in range(size - 1, 0, -1):
        lens[i] = lens[2 * i] + lens[2 * i + 1]

    def upd(node, nl, nr, l, r_, v):
        if r_ <= nl or nr <= l:
            return
        if l <= nl and nr <= r_:
            cnt[node] += v
        else:
            mid = (nl + nr) // 2
            upd(2 * node, nl, mid, l, r_, v); upd(2 * node + 1, mid, nr, l, r_, v)
        if cnt[node]:
            cov[node] = lens[node]
        elif node >= size:
            cov[node] = 0
        else:
            cov[node] = cov[2 * node] + cov[2 * node + 1]
    ev = []
    for x1, y1, x2, y2 in rects:
        ev.append((x1, 1, yi[y1], yi[y2])); ev.append((x2, -1, yi[y1], yi[y2]))
    ev.sort()
    area, px = 0, ev[0][0]
    for x, v, a, b in ev:
        area += cov[1] * (x - px); px = x
        upd(1, 0, size, a, b, v)
    return area


def _br(s):
    rd = Rd(s); n = rd.int(); rects = [rd.ints(4) for _ in range(n)]
    xs = sorted({x for r_ in rects for x in (r_[0], r_[2])})
    area = 0
    for i in range(len(xs) - 1):
        xa, xb = xs[i], xs[i + 1]
        iv = sorted((y1, y2) for x1, y1, x2, y2 in rects if x1 <= xa and xb <= x2)
        tot, cl, cr = 0, None, None
        for a, b in iv:
            if cr is None or a > cr:
                if cr is not None:
                    tot += cr - cl
                cl, cr = a, b
            else:
                cr = max(cr, b)
        if cr is not None:
            tot += cr - cl
        area += tot * (xb - xa)
    return area


add(T, "Diện tích hợp các hình chữ nhật", 5, """
Cho `n` hình chữ nhật có cạnh song song trục toạ độ, hình `i` có góc dưới trái `(x1, y1)` và góc trên phải `(x2, y2)`.
Tính diện tích phần mặt phẳng bị phủ bởi ít nhất một hình.

Gợi ý (đường quét + cây phân đoạn): quét đường thẳng đứng theo `x`; mỗi hình tạo sự kiện "mở" tại `x1` và "đóng" tại `x2` trên đoạn `[y1, y2)`.
Cây phân đoạn trên các toạ độ `y` đã nén lưu `cnt` (số hình phủ trọn nút) và `cov` (độ dài được phủ). Diện tích cộng thêm `cov(gốc) × Δx`.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). `n` dòng sau mỗi dòng `x1 y1 x2 y2` (0 ≤ x1 < x2 ≤ 10^9, 0 ≤ y1 < y2 ≤ 10^9).", "Diện tích (vừa `long long`).",
    ["2\n0 0 2 2\n1 1 3 3\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 200 else _sol(s), tags=["sweep line", "segment tree"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    hi = r.choice([20, 10**6])
    out = []
    for _ in range(n):
        if r.random() < .5:
            y = r.randint(-hi, hi); a = r.randint(-hi, hi); out.append(J(a, y, min(hi, a + r.randint(1, hi)), y))
        else:
            x = r.randint(-hi, hi); a = r.randint(-hi, hi); out.append(J(x, a, x, min(hi, a + r.randint(1, hi))))
    return lines(str(n), *out)


def _sol(s):
    rd = Rd(s); n = rd.int(); segs = [rd.ints(4) for _ in range(n)]
    ev = []; ys = set()
    for x1, y1, x2, y2 in segs:
        if y1 == y2:
            ev.append((x1, 0, y1, 0)); ev.append((x2, 2, y1, 0)); ys.add(y1)
        else:
            ev.append((x1, 1, y1, y2))
    ys = sorted(ys); idx = {y: i + 1 for i, y in enumerate(ys)}
    b = BIT(len(ys)); tot = 0
    ev.sort()
    for x, t, y1, y2 in ev:
        if t == 0:
            b.add(idx[y1], 1)
        elif t == 2:
            b.add(idx[y1], -1)
        else:
            tot += b.sum(bisect_right(ys, y2)) - b.sum(bisect_left(ys, y1))
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); segs = [rd.ints(4) for _ in range(n)]
    hs = [s_ for s_ in segs if s_[1] == s_[3]]; vs = [s_ for s_ in segs if s_[0] == s_[2]]
    return sum(1 for h in hs for v in vs if h[0] <= v[0] <= h[2] and v[1] <= h[1] <= v[3])


add(T, "Giao điểm đoạn ngang và dọc", 4, """
Có `n` đoạn thẳng, mỗi đoạn hoặc **nằm ngang** hoặc **thẳng đứng** (đầu mút nguyên, độ dài dương). Không có hai đoạn ngang nào cùng nằm trên
một đường thẳng và chồng nhau, tương tự với đoạn dọc. Đếm số cặp (đoạn ngang, đoạn dọc) cắt nhau (kể cả chạm đầu mút).

Gợi ý: quét theo `x`. Sự kiện: đoạn ngang mở (thêm `y` vào BIT), đoạn dọc (đếm số `y` đang mở trong `[y1, y2]`), đoạn ngang đóng (xoá `y`).
Tại cùng `x`: mở → hỏi → đóng.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau mỗi dòng `x1 y1 x2 y2` (x1 ≤ x2, y1 ≤ y2, |toạ độ| ≤ 10^6).", "Số giao điểm.",
    ["3\n2 3 7 3\n3 1 3 5\n6 2 6 6\n"], _g, _sol, brute=_br, tags=["sweep line", "BIT"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = r.choice([10, 1000, 10**9])
    segs = set()
    while len(segs) < n:
        a = r.randint(1, hi); segs.add((a, r.randint(a, min(hi, a + max(1, hi // r.choice([1, 5, 50]))))))
        if len(segs) < n and hi == 10 and len(segs) >= 55:
            break
    segs = list(segs); r.shuffle(segs)
    return lines(str(len(segs)), *(J(a, b) for a, b in segs))


def _sol(s):
    rd = Rd(s); n = rd.int(); segs = [tuple(rd.ints(2)) for _ in range(n)]
    order = sorted(range(n), key=lambda i: (segs[i][0], -segs[i][1]))
    ys = sorted({b for _, b in segs}); idx = {y: i + 1 for i, y in enumerate(ys)}; m = len(ys)
    contains = [0] * n; contained = [0] * n
    b = BIT(m)
    for i in reversed(order):  # các đoạn đã thêm có a lớn hơn (hoặc bằng và b nhỏ hơn)
        contains[i] = b.sum(idx[segs[i][1]]); b.add(idx[segs[i][1]], 1)
    b = BIT(m)
    for k, i in enumerate(order):
        contained[i] = k - b.sum(idx[segs[i][1]] - 1); b.add(idx[segs[i][1]], 1)
    return lines(L(contains), L(contained)).rstrip("\n")


def _br(s):
    rd = Rd(s); n = rd.int(); segs = [tuple(rd.ints(2)) for _ in range(n)]
    c1 = [sum(1 for j in range(n) if j != i and segs[i][0] <= segs[j][0] and segs[j][1] <= segs[i][1]) for i in range(n)]
    c2 = [sum(1 for j in range(n) if j != i and segs[j][0] <= segs[i][0] and segs[i][1] <= segs[j][1]) for i in range(n)]
    return lines(L(c1), L(c2)).rstrip("\n")


add(T, "Đoạn lồng nhau", 4, """
Cho `n` đoạn `[a_i, b_i]` đôi một khác nhau. Đoạn `i` **chứa** đoạn `j` nếu `a_i ≤ a_j` và `b_j ≤ b_i`.
Với mỗi đoạn, đếm số đoạn khác mà nó chứa, và số đoạn khác chứa nó.

Gợi ý: sắp xếp theo `a` tăng dần, cùng `a` thì `b` giảm dần. Khi đó các đoạn chứa đoạn `i` đều đứng **trước** nó và có `b ≥ b_i`;
các đoạn bị `i` chứa đứng **sau** và có `b ≤ b_i` → đếm bằng BIT trên `b` đã nén.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `a b` (1 ≤ a ≤ b ≤ 10^9), các đoạn đôi một khác nhau.",
    "Dòng đầu gồm `n` số (số đoạn mà mỗi đoạn chứa), dòng hai gồm `n` số (số đoạn chứa mỗi đoạn).",
    ["4\n1 6\n2 4\n4 8\n3 6\n"], _g, _sol, brute=_br, tags=["BIT", "sweep line"])


# 17 ----------------------------------------------------------------------
class _PolySeg:
    """Cộng cấp số cộng (1, 2, 3, ...) lên đoạn, tổng đoạn. Lazy lưu (a, d): cộng a + d·(i - l) tại vị trí i của nút."""

    def __init__(self, a):
        n = len(a); self.n = n
        self.sum = [0] * (4 * n); self.la = [0] * (4 * n); self.ld = [0] * (4 * n)
        self._build(1, 0, n - 1, a)

    def _build(self, k, l, r, a):
        if l == r:
            self.sum[k] = a[l]; return
        m = (l + r) // 2
        self._build(2 * k, l, m, a); self._build(2 * k + 1, m + 1, r, a)
        self.sum[k] = self.sum[2 * k] + self.sum[2 * k + 1]

    def _apply(self, k, l, r, a, d):
        ln = r - l + 1
        self.sum[k] += a * ln + d * ln * (ln - 1) // 2
        self.la[k] += a; self.ld[k] += d

    def _push(self, k, l, r):
        if self.la[k] or self.ld[k]:
            m = (l + r) // 2
            a, d = self.la[k], self.ld[k]
            self._apply(2 * k, l, m, a, d)
            self._apply(2 * k + 1, m + 1, r, a + d * (m + 1 - l), d)
            self.la[k] = self.ld[k] = 0

    def update(self, ql, qr, k=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self._apply(k, l, r, l - ql + 1, 1); return
        self._push(k, l, r)
        m = (l + r) // 2
        self.update(ql, qr, 2 * k, l, m); self.update(ql, qr, 2 * k + 1, m + 1, r)
        self.sum[k] = self.sum[2 * k] + self.sum[2 * k + 1]

    def query(self, ql, qr, k=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.sum[k]
        self._push(k, l, r)
        m = (l + r) // 2
        return self.query(ql, qr, 2 * k, l, m) + self.query(ql, qr, 2 * k + 1, m + 1, r)


def _g(r, s):
    n, q = S(s, 1, 5 * 10**4), S(s, 1, 5 * 10**4)
    ops = []
    for _ in range(q):
        a, b = _qs(r, n, 1)[0]; ops.append(J(1 if r.random() < .5 else 2, a, b))
    return lines(J(n, q), L(arr(r, n, 1, 10**6)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); st = _PolySeg(rd.ints(n)); out = []
    for _ in range(q):
        t, a, b = rd.ints(3)
        if t == 1:
            st.update(a - 1, b - 1)
        else:
            out.append(st.query(a - 1, b - 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); x = rd.ints(n); out = []
    for _ in range(q):
        t, a, b = rd.ints(3)
        if t == 1:
            for i in range(a - 1, b):
                x[i] += i - a + 2
        else:
            out.append(sum(x[a - 1:b]))
    return out


add(T, "Cộng cấp số cộng trên đoạn", 5, """
Thao tác:
- `1 a b`: cộng 1 vào `x_a`, 2 vào `x_{a+1}`, ..., `b - a + 1` vào `x_b`;
- `2 a b`: in tổng `x_a + ... + x_b`.

Gợi ý: lazy lưu cặp `(đầu, công sai)` của cấp số cộng cần cộng vào cả nút. Hai cấp số cộng cộng lại vẫn là cấp số cộng!
Khi đẩy xuống con phải, số hạng đầu phải dịch đi `công sai × (độ dài con trái)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 5·10^4). Dòng hai gồm `n` số (1 ≤ x_i ≤ 10^6). `q` dòng sau là các thao tác.",
    "Kết quả các thao tác loại 2.", ["5 3\n4 2 3 1 7\n2 1 5\n1 1 5\n2 1 5\n"], _g, _sol, brute=_br, tags=["segment tree", "lazy"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    ops = []
    for _ in range(q):
        ops.append(J(1, r.randint(1, n), r.randint(1, 10**9)) if r.random() < .4 else J(2, r.randint(1, n)))
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); p = rd.ints(n)
    INF = float("inf")
    left = Seg([p[i] - i for i in range(n)], min, INF)   # dùng cho j ≤ k: p_j - j + k
    right = Seg([p[i] + i for i in range(n)], min, INF)  # dùng cho j ≥ k: p_j + j - k
    out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            k, x = rd.ints(2); k -= 1; left.set(k, x - k); right.set(k, x + k)
        else:
            k = rd.int() - 1
            out.append(min(left.query(0, k + 1) + k, right.query(k, n) - k))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); p = rd.ints(n); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            k, x = rd.ints(2); p[k - 1] = x
        else:
            k = rd.int() - 1; out.append(min(p[j] + abs(j - k) for j in range(n)))
    return out


add(T, "Đặt pizza", 4, """
Có `n` toà nhà thẳng hàng, mỗi toà có một tiệm pizza; pizza ở toà `j` giá `p_j`, giao từ toà `j` tới toà `k` tốn thêm `|j - k|`.
Thao tác:
- `1 k x`: giá pizza ở toà `k` đổi thành `x`;
- `2 k`: người ở toà `k` muốn mua pizza — chi phí nhỏ nhất là bao nhiêu?

Gợi ý: tách trị tuyệt đối: với `j ≤ k` chi phí là `(p_j - j) + k`; với `j ≥ k` là `(p_j + j) - k`.
Hai cây phân đoạn min cho `p_j - j` và `p_j + j`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` giá (1 ≤ p ≤ 10^9). `q` dòng sau là các thao tác.",
    "Kết quả các thao tác loại 2.", ["6 3\n8 6 4 5 7 5\n2 2\n1 5 1\n2 2\n"], _g, _sol, brute=_br, tags=["segment tree"])


# 19 ----------------------------------------------------------------------
class _FlipSeg:
    def __init__(self, bits):
        n = len(bits); self.n = n
        self.c = [0] * (4 * n); self.lz = [False] * (4 * n); self.ln = [0] * (4 * n)
        self._build(1, 0, n - 1, bits)

    def _build(self, k, l, r, b):
        self.ln[k] = r - l + 1
        if l == r:
            self.c[k] = b[l]; return
        m = (l + r) // 2
        self._build(2 * k, l, m, b); self._build(2 * k + 1, m + 1, r, b)
        self.c[k] = self.c[2 * k] + self.c[2 * k + 1]

    def _flip(self, k):
        self.c[k] = self.ln[k] - self.c[k]; self.lz[k] = not self.lz[k]

    def _push(self, k):
        if self.lz[k]:
            self._flip(2 * k); self._flip(2 * k + 1); self.lz[k] = False

    def flip(self, ql, qr, k=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self._flip(k); return
        self._push(k)
        m = (l + r) // 2
        self.flip(ql, qr, 2 * k, l, m); self.flip(ql, qr, 2 * k + 1, m + 1, r)
        self.c[k] = self.c[2 * k] + self.c[2 * k + 1]

    def count(self, ql, qr, k=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.c[k]
        self._push(k)
        m = (l + r) // 2
        return self.count(ql, qr, 2 * k, l, m) + self.count(ql, qr, 2 * k + 1, m + 1, r)


def _g(r, s):
    n, q = S(s, 1, 5 * 10**4), S(s, 1, 5 * 10**4)
    ops = [J(r.randint(1, 2), *_qs(r, n, 1)[0]) for _ in range(q)]
    return lines(J(n, q), "".join(r.choice("01") for _ in range(n)), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); st = _FlipSeg([int(c) for c in rd.str()]); out = []
    for _ in range(q):
        t, a, b = rd.ints(3)
        if t == 1:
            st.flip(a - 1, b - 1)
        else:
            out.append(st.count(a - 1, b - 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); x = [int(c) for c in rd.str()]; out = []
    for _ in range(q):
        t, a, b = rd.ints(3)
        if t == 1:
            for i in range(a - 1, b):
                x[i] ^= 1
        else:
            out.append(sum(x[a - 1:b]))
    return out


add(T, "Bật tắt đèn", 4, """
Dãy `n` bóng đèn, trạng thái cho bởi xâu 0/1. Thao tác:
- `1 a b`: đảo trạng thái mọi bóng từ `a` tới `b`;
- `2 a b`: đếm số bóng đang sáng từ `a` tới `b`.

Gợi ý: lazy là cờ "cần đảo"; đảo một nút: `cnt = độ dài - cnt`, và lật cờ lazy (đảo hai lần = không đảo).
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 5·10^4). Dòng hai là xâu 0/1 độ dài `n`. `q` dòng sau là các thao tác.",
    "Kết quả các thao tác loại 2.", ["5 4\n10110\n2 1 5\n1 2 4\n2 1 5\n2 3 3\n"], _g, _sol, brute=_br, tags=["segment tree", "lazy"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    hi = r.choice([20, 10**9])
    pts = [J(r.randint(1, hi), r.randint(1, hi)) for _ in range(n)]
    qs = []
    for _ in range(q):
        a, b = sorted((r.randint(1, hi), r.randint(1, hi))); c, d = sorted((r.randint(1, hi), r.randint(1, hi)))
        qs.append(J(a, c, b, d))
    return lines(J(n, q), *pts, *qs)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2)
    pts = sorted(tuple(rd.ints(2)) for _ in range(n))
    ys = sorted({y for _, y in pts}); m = len(ys)
    ev = []  # (x, sign, y1, y2, id)
    for i in range(q):
        x1, y1, x2, y2 = rd.ints(4)
        ev.append((x2, 1, y1, y2, i)); ev.append((x1 - 1, -1, y1, y2, i))
    ev.sort()
    b = BIT(m); ans = [0] * q; j = 0
    for x, sg, y1, y2, i in ev:
        while j < n and pts[j][0] <= x:
            b.add(bisect_left(ys, pts[j][1]) + 1, 1); j += 1
        ans[i] += sg * (b.sum(bisect_right(ys, y2)) - b.sum(bisect_left(ys, y1)))
    return ans


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); pts = [rd.ints(2) for _ in range(n)]; out = []
    for _ in range(q):
        x1, y1, x2, y2 = rd.ints(4)
        out.append(sum(1 for x, y in pts if x1 <= x <= x2 and y1 <= y <= y2))
    return out


add(T, "Đếm điểm trong hình chữ nhật", 4, """
Cho `n` điểm trên mặt phẳng và `q` truy vấn `(x1, y1, x2, y2)`: đếm số điểm nằm trong (hoặc trên biên) hình chữ nhật.

Gợi ý (offline + đường quét): `cnt(x1..x2, y1..y2) = F(x2) - F(x1 - 1)` với `F(X)` = số điểm có `x ≤ X` và `y ∈ [y1, y2]`.
Sắp xếp điểm và các mốc `X` theo hoành độ, thêm dần điểm vào BIT theo tung độ đã nén.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n` dòng là các điểm, `q` dòng là truy vấn (1 ≤ toạ độ ≤ 10^9, x1 ≤ x2, y1 ≤ y2).",
    "Mỗi truy vấn in một dòng.", ["4 2\n1 1\n2 3\n3 2\n5 5\n1 1 3 3\n2 2 5 5\n"], _g, _sol, brute=_br, tags=["BIT", "offline", "sweep line"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, r.choice([10, 10**9]))))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    vals = sorted(set(a)); b = BIT(len(vals)); tot = 0
    for i in range(n - 1, -1, -1):  # đếm j > i có 2·a_j < a_i
        tot += b.sum(bisect_left(vals, (a[i] + 1) // 2))
        b.add(bisect_left(vals, a[i]) + 1, 1)
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > 2 * a[j])


add(T, "Nghịch thế quan trọng", 3, """
Đếm số cặp `i < j` mà `a_i > 2·a_j`.

Gợi ý: duyệt từ phải sang trái, BIT đếm các `a_j` đã gặp; với `a_i` cần đếm số `a_j < a_i / 2`, tức `a_j ≤ ⌈a_i/2⌉ - 1`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số cặp.",
    ["5\n1 3 2 3 1\n"], _g, _sol, brute=_br, tags=["BIT", "nén số"])
