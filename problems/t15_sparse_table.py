"""Chuyên đề 15: Sparse table (bảng thưa), nhảy nhị phân trên mảng."""
from math import gcd
from .base import add, Rd, S, J, L, arr, lines

T = 15


class Sparse:
    """Bảng thưa cho phép toán lũy đẳng f (min, max, gcd, and, or...)."""

    def __init__(self, a, f):
        self.f = f
        self.t = [list(a)]
        j = 1
        while (1 << j) <= len(a):
            prev = self.t[-1]; h = 1 << (j - 1)
            self.t.append([f(prev[i], prev[i + h]) for i in range(len(a) - (1 << j) + 1)])
            j += 1

    def q(self, l, r):  # 0-based, đóng [l, r]
        k = (r - l + 1).bit_length() - 1
        row = self.t[k]
        return self.f(row[l], row[r - (1 << k) + 1])


def _gq(lo=1, hi=10**9, nmax=2 * 10**5, qmax=2 * 10**5):
    def g(r, s):
        n, q = S(s, 1, nmax), S(s, 1, qmax)
        a = arr(r, n, lo, r.choice([10, hi]))
        qs = []
        for _ in range(q):
            x, y = r.randint(1, n), r.randint(1, n)
            if r.random() < .3:
                y = min(n, x + r.randint(0, 5))
            qs.append(J(min(x, y), max(x, y)))
        return lines(J(n, q), L(a), *qs)
    return g


def _range_sol(f, post=None):
    def sol(s):
        rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
        sp = Sparse(a, f); out = []
        for _ in range(q):
            l, r = rd.ints(2)
            v = sp.q(l - 1, r - 1)
            out.append(post(v) if post else v)
        return out
    return sol


def _range_br(f):
    def br(s):
        rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
        for _ in range(q):
            l, r = rd.ints(2)
            v = a[l - 1]
            for x in a[l:r]:
                v = f(v, x)
            out.append(v)
        return out
    return br


# 1 -----------------------------------------------------------------------
add(T, "Min trên đoạn (RMQ)", 1, """
Cho dãy cố định (không có cập nhật) và `q` truy vấn `(l, r)`: tìm min của `a_l..a_r`.

Gợi ý (sparse table): `st[j][i]` = min của đoạn dài `2^j` bắt đầu tại `i`; `st[j][i] = min(st[j-1][i], st[j-1][i + 2^{j-1}])`.
Truy vấn: với `k = ⌊log2(r - l + 1)⌋`, đáp án `min(st[k][l], st[k][r - 2^k + 1])` — hai đoạn chồng nhau không sao vì `min` là **lũy đẳng**.
Xây `O(n log n)`, mỗi truy vấn `O(1)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["8 4\n3 2 4 5 1 1 5 3\n2 4\n5 6\n1 8\n3 3\n"], _gq(), _range_sol(min),
    brute=_range_br(min), tags=["sparse table", "RMQ"])


# 2 -----------------------------------------------------------------------
add(T, "Max trên đoạn", 1, """
Như bài trước nhưng hỏi giá trị **lớn nhất** trên đoạn `[l, r]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["5 2\n1 5 2 4 3\n1 3\n3 5\n"], _gq(), _range_sol(max), brute=_range_br(max),
    tags=["sparse table"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    mx, mn = Sparse(a, max), Sparse(a, min); out = []
    for _ in range(q):
        l, r = rd.ints(2)
        out.append(mx.q(l - 1, r - 1) - mn.q(l - 1, r - 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r = rd.ints(2); out.append(max(a[l - 1:r]) - min(a[l - 1:r]))
    return out


add(T, "Chênh lệch chiều cao", 2, """
`n` bạn học sinh đứng thành hàng, bạn `i` cao `a_i`. Với mỗi truy vấn `(l, r)`, cho biết chênh lệch giữa bạn cao nhất và thấp nhất trong nhóm `l..r`.

Gợi ý: hai bảng thưa, một cho max và một cho min.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["6 3\n1 7 3 4 2 5\n1 5\n4 6\n2 2\n"], _gq(), _sol, brute=_br, tags=["sparse table"])


# 4 -----------------------------------------------------------------------
def _gg(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    g = r.choice([1, 2, 6, 30])
    a = [g * r.randint(1, 10**9 // g) if r.random() < .9 else r.randint(1, 10**9) for _ in range(n)]
    qs = [sorted((r.randint(1, n), r.randint(1, n))) for _ in range(q)]
    return lines(J(n, q), L(a), *(J(x, y) for x, y in qs))


add(T, "UCLN trên đoạn", 2, """
Với mỗi truy vấn `(l, r)`, tính `gcd(a_l, ..., a_r)`.

Gợi ý: `gcd` cũng lũy đẳng (`gcd(x, x) = x`) nên dùng được bảng thưa với truy vấn `O(1)` (thêm `O(log)` cho phép `gcd`).
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["5 3\n12 18 24 9 6\n1 3\n2 5\n4 4\n"], _gg, _range_sol(gcd), brute=_range_br(gcd),
    tags=["sparse table", "gcd"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    sp = Sparse([(x, i) for i, x in enumerate(a)], min); out = []
    for _ in range(q):
        l, r = rd.ints(2); out.append(sp.q(l - 1, r - 1)[1] + 1)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r = rd.ints(2)
        seg = a[l - 1:r]; out.append(l + seg.index(min(seg)))
    return out


add(T, "Vị trí nhỏ nhất", 2, """
Với mỗi truy vấn `(l, r)`, in **vị trí** của phần tử nhỏ nhất trong đoạn; nếu có nhiều vị trí, in vị trí nhỏ nhất.

Gợi ý: lưu cặp `(giá trị, chỉ số)` trong bảng thưa — so sánh cặp tự động ưu tiên chỉ số nhỏ khi giá trị bằng nhau.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["6 2\n4 1 3 1 2 5\n1 6\n3 6\n"], _gq(), _sol, brute=_br, tags=["sparse table"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    so, sa = Sparse(a, lambda x, y: x | y), Sparse(a, lambda x, y: x & y); out = []
    for _ in range(q):
        l, r = rd.ints(2); out.append(J(so.q(l - 1, r - 1), sa.q(l - 1, r - 1)))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r = rd.ints(2); o, x = 0, (1 << 40) - 1
        for v in a[l - 1:r]:
            o |= v; x &= v
        out.append(J(o, x))
    return out


add(T, "OR và AND trên đoạn", 2, """
Với mỗi truy vấn `(l, r)`, in `a_l OR ... OR a_r` và `a_l AND ... AND a_r`.

Gợi ý: OR và AND đều lũy đẳng.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (0 ≤ a_i < 2^30). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in hai số trên một dòng.", ["4 2\n5 3 6 7\n1 2\n2 4\n"], _gq(0, 2**30 - 1), _sol, brute=_br,
    tags=["sparse table", "bitwise"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    g = r.choice([2, 3, 6])
    a = [g * r.randint(1, 1000) if r.random() < .85 else r.randint(1, 10**6) for _ in range(n)]
    return lines(str(n), L(a))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    sp = Sparse(a, gcd); l = best = 0
    for r_ in range(n):
        while l <= r_ and sp.q(l, r_) == 1:
            l += 1
        best = max(best, r_ - l + 1)
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); best = 0
    for i in range(n):
        g = 0
        for j in range(i, n):
            g = gcd(g, a[j])
            if g > 1:
                best = max(best, j - i + 1)
    return best


add(T, "Đoạn dài nhất có UCLN lớn hơn 1", 3, """
Tìm đoạn con liên tiếp dài nhất có UCLN lớn hơn 1 (in 0 nếu mọi phần tử đều bằng 1).

Gợi ý: hai con trỏ — khi `gcd(l..r) = 1` thì tăng `l`. Cần `gcd` của cửa sổ bất kỳ → bảng thưa.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^6).", "Độ dài lớn nhất.",
    ["6\n2 4 3 9 6 5\n"], _g, _sol, brute=_br, tags=["sparse table", "hai con trỏ", "gcd"])


# 8 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    # với mỗi r: các giá trị gcd của đoạn kết thúc tại r chỉ có O(log) giá trị khác nhau
    cur = []  # list (gcd, số đầu trái)
    tot = 0
    for x in a:
        nxt = []
        for g, c in cur + [(0, 1)]:
            ng = gcd(g, x)
            if nxt and nxt[-1][0] == ng:
                nxt[-1] = (ng, nxt[-1][1] + c)
            else:
                nxt.append((ng, c))
        cur = nxt
        tot += sum(c for g, c in cur if g == 1)
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); c = 0
    for i in range(n):
        g = 0
        for j in range(i, n):
            g = gcd(g, a[j]); c += g == 1
    return c


add(T, "Đếm đoạn có UCLN bằng 1", 3, """
Đếm số đoạn con liên tiếp có UCLN bằng 1.

Gợi ý: cố định đầu trái `l`; `gcd(l..r)` không tăng khi `r` tăng → tìm kiếm nhị phân `r` nhỏ nhất có `gcd = 1` bằng bảng thưa.
(Cách khác: với mỗi đầu phải, các giá trị gcd khác nhau chỉ có `O(log A)` giá trị.)
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^6).", "Số đoạn.",
    ["4\n2 3 4 6\n"], _g, _sol, brute=_br, tags=["sparse table", "tìm kiếm nhị phân", "gcd"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    a = arr(r, n, 1, r.choice([5, 10**9]))
    qs = [sorted((r.randint(1, n), r.randint(1, n))) for _ in range(q)]
    return lines(J(n, q), L(a), *(J(x, y) for x, y in qs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    nxt = [n] * (n + 1); st = []
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] <= a[i]:
            st.pop()
        nxt[i] = st[-1] if st else n
        st.append(i)
    LOG = max(1, n.bit_length())
    up = [nxt]
    for _ in range(1, LOG):
        p = up[-1]; up.append([p[p[i]] for i in range(n + 1)])
    out = []
    for _ in range(q):
        l, r_ = rd.ints(2); l -= 1; r_ -= 1
        c, u = 1, l
        for j in range(LOG - 1, -1, -1):
            if up[j][u] <= r_:
                u = up[j][u]; c += 1 << j
        out.append(c)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r_ = rd.ints(2); c, mx = 0, 0
        for x in a[l - 1:r_]:
            if x > mx:
                c += 1; mx = x
        out.append(c)
    return out


add(T, "Đếm kỷ lục trên đoạn", 3, """
Với truy vấn `(l, r)`: đi từ `a_l` tới `a_r`, đếm số lần gặp một phần tử **lớn hơn hẳn** mọi phần tử đã gặp trước đó (tính cả `a_l`).

Gợi ý (nhảy nhị phân): `nxt[i]` = vị trí phần tử lớn hơn hẳn gần nhất bên phải. Các "kỷ lục" chính là dãy `l, nxt[l], nxt[nxt[l]], ...`
→ bảng `up[j][i]` = nhảy `2^j` bước từ `i`, đếm số bước nhảy vẫn ≤ r.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["6 2\n1 3 2 5 4 6\n1 6\n3 5\n"], _g, _sol, brute=_br, tags=["nhảy nhị phân"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    return lines(J(n, q), L(r.randint(1, n) for _ in range(n)),
                 *(J(r.randint(1, n), r.randint(0, r.choice([10, 10**9]))) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); t = [x - 1 for x in rd.ints(n)]
    up = [t]
    for _ in range(29):
        p = up[-1]; up.append([p[p[i]] for i in range(n)])
    out = []
    for _ in range(q):
        x, k = rd.ints(2); x -= 1; j = 0
        while k:
            if k & 1:
                x = up[j][x]
            k >>= 1; j += 1
        out.append(x + 1)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); t = [x - 1 for x in rd.ints(n)]; out = []
    for _ in range(q):
        x, k = rd.ints(2); x -= 1
        seen = {}; step = 0
        while step < k:
            if x in seen:
                cyc = step - seen[x]
                k = step + (k - step) % cyc
                seen = {}
                if step >= k:
                    break
            seen[x] = step
            x = t[x]; step += 1
        out.append(x + 1)
    return out


add(T, "Dịch chuyển giữa các hành tinh", 3, """
Mỗi hành tinh `i` có một cổng dịch chuyển tới hành tinh `t_i`. Với truy vấn `(x, k)`: xuất phát ở hành tinh `x`, đi qua cổng `k` lần,
bạn ở hành tinh nào?

Gợi ý (nhảy nhị phân / binary lifting): `up[j][i]` = hành tinh sau `2^j` lần dịch chuyển từ `i`, `up[j][i] = up[j-1][up[j-1][i]]`.
Phân tích `k` thành tổng các luỹ thừa của 2.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `t_1..t_n`. `q` dòng sau mỗi dòng `x k` (0 ≤ k ≤ 10^9).",
    "Mỗi truy vấn in một dòng.", ["4 3\n2 1 1 4\n1 2\n3 4\n4 1\n"], _g, _sol, brute=_br, tags=["nhảy nhị phân", "đồ thị hàm"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 100), S(s, 1, 100)
    q = S(s, 1, 10**5)
    qs = []
    for _ in range(q):
        a, b = sorted((r.randint(1, n), r.randint(1, n))); c, d = sorted((r.randint(1, m), r.randint(1, m)))
        qs.append(J(a, c, b, d))
    return lines(J(n, m, q), *(L(arr(r, m, 1, 10**9)) for _ in range(n)), *qs)


def _sol(s):
    rd = Rd(s); n, m, q = rd.ints(3); a = [rd.ints(m) for _ in range(n)]
    rows = [Sparse(row, max) for row in a]  # bảng thưa theo cột cho từng hàng
    LOGM = len(rows[0].t)
    # col_tables[kc] = Sparse theo hàng của dãy rows[i].t[kc]
    tabs = []
    for kc in range(LOGM):
        width = len(rows[0].t[kc])
        cols = []
        for j in range(width):
            cols.append(Sparse([rows[i].t[kc][j] for i in range(n)], max))
        tabs.append(cols)
    out = []
    for _ in range(q):
        x1, y1, x2, y2 = rd.ints(4); x1 -= 1; y1 -= 1; x2 -= 1; y2 -= 1
        kc = (y2 - y1 + 1).bit_length() - 1
        out.append(max(tabs[kc][y1].q(x1, x2), tabs[kc][y2 - (1 << kc) + 1].q(x1, x2)))
    return out


def _br(s):
    rd = Rd(s); n, m, q = rd.ints(3); a = [rd.ints(m) for _ in range(n)]; out = []
    for _ in range(q):
        x1, y1, x2, y2 = rd.ints(4)
        out.append(max(a[i][j] for i in range(x1 - 1, x2) for j in range(y1 - 1, y2)))
    return out


add(T, "Bảng thưa 2 chiều", 4, """
Cho ma trận `n × m` cố định và `q` truy vấn `(x1, y1, x2, y2)`: tìm giá trị lớn nhất trong hình chữ nhật con.

Gợi ý: bảng thưa 2D `st[i][j][a][b]` = max của khối `2^a × 2^b` có góc trên trái `(i, j)`. Một truy vấn = max của 4 khối chồng nhau.
Bộ nhớ `O(n·m·log n·log m)`.
""", "Dòng đầu `n, m, q` (1 ≤ n, m ≤ 100, 1 ≤ q ≤ 10^5). `n` dòng sau là ma trận (1 ≤ a ≤ 10^9). `q` dòng truy vấn.",
    "Mỗi truy vấn in một dòng.", ["3 3 2\n1 2 3\n4 9 6\n7 8 5\n1 1 2 2\n2 3 3 3\n"], _g, _sol, brute=_br, tags=["sparse table 2D"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    g = r.choice([1, 2, 6])
    a = [g * r.choice([1, 2, 3, 4, 6, 12, 5, 7]) * r.choice([1, 1, 1, 11]) for _ in range(n)]
    return lines(str(n), L(a), str(q), L(r.choice(a) * r.choice([1, 1, 1, 2]) if r.random() < .8 else r.randint(1, 100) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    from collections import Counter
    total = Counter(); cur = []
    for x in a:
        nxt = []
        for g, c in cur + [(0, 1)]:
            ng = gcd(g, x)
            if nxt and nxt[-1][0] == ng:
                nxt[-1] = (ng, nxt[-1][1] + c)
            else:
                nxt.append((ng, c))
        cur = nxt
        for g, c in cur:
            total[g] += c
    q = rd.int()
    return L(total.get(x, 0) for x in rd.ints(q))


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    from collections import Counter
    c = Counter()
    for i in range(n):
        g = 0
        for j in range(i, n):
            g = gcd(g, a[j]); c[g] += 1
    q = rd.int()
    return L(c.get(x, 0) for x in rd.ints(q))


add(T, "Đếm đoạn theo UCLN", 4, """
Cho dãy `a` và `q` truy vấn `x`: đếm số đoạn con liên tiếp có UCLN đúng bằng `x`.

Gợi ý: với mỗi đầu phải `r`, các giá trị `gcd(l..r)` (với `l` thay đổi) chỉ có `O(log A)` giá trị khác nhau, tạo thành các khối liên tiếp
(có thể tìm biên khối bằng bảng thưa + tìm kiếm nhị phân, hoặc duy trì danh sách trực tiếp). Cộng dồn số đoạn cho từng giá trị vào `map`.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). Dòng ba `q` (1 ≤ q ≤ 10^5), dòng bốn gồm `q` số `x`.",
    "Một dòng gồm `q` số.", ["3\n2 6 3\n5\n1 2 3 4 6\n"], _g, _sol, brute=_br, tags=["gcd", "sparse table"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    a = arr(r, n, 1, r.choice([100, 10**9]))
    return lines(J(n, q), L(a), *(J(r.randint(1, n), r.randint(1, r.choice([100, 10**9]))) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    sp = Sparse(a, min); out = []
    for _ in range(q):
        l, k = rd.ints(2); l -= 1
        if a[l] <= k:
            out.append(l + 1); continue
        lo, hi = l, n - 1
        if sp.q(l, hi) > k:
            out.append(-1); continue
        while lo < hi:
            mid = (lo + hi) // 2
            if sp.q(l, mid) <= k:
                hi = mid
            else:
                lo = mid + 1
        out.append(lo + 1)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, k = rd.ints(2)
        out.append(next((i + 1 for i in range(l - 1, n) if a[i] <= k), -1))
    return out


add(T, "Vị trí đầu tiên không vượt quá k", 3, """
Với truy vấn `(l, k)`: tìm vị trí `r ≥ l` nhỏ nhất sao cho `a_r ≤ k`, hoặc `-1` nếu không có.

Gợi ý: `min(a_l..a_r)` không tăng khi `r` tăng → tìm kiếm nhị phân trên `r` với bảng thưa min (mỗi truy vấn `O(log n)`).
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l k`.",
    "Mỗi truy vấn in một dòng.", ["5 3\n5 3 4 1 2\n1 3\n3 2\n5 1\n"], _g, _sol, brute=_br, tags=["sparse table", "tìm kiếm nhị phân"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    bits = r.choice([4, 10, 30])
    return lines(J(n, r.randint(0, 2**bits - 1)), L(r.getrandbits(bits) & r.getrandbits(bits) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    sp = Sparse(a, lambda x, y: x | y); l = best = 0
    for r_ in range(n):
        while l <= r_ and sp.q(l, r_) > k:
            l += 1
        best = max(best, r_ - l + 1)
    return best


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n); best = 0
    for i in range(n):
        o = 0
        for j in range(i, n):
            o |= a[j]
            if o <= k:
                best = max(best, j - i + 1)
            else:
                break
    return best


add(T, "Đoạn dài nhất có OR không vượt quá k", 3, """
Tìm đoạn con liên tiếp dài nhất có `a_l OR ... OR a_r ≤ k` (in 0 nếu không có).

Gợi ý: OR của đoạn chỉ tăng khi mở rộng đoạn → hai con trỏ; OR của cửa sổ lấy bằng bảng thưa (không "trừ" được OR như tổng!).
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 0 ≤ k < 2^30). Dòng sau `n` số (0 ≤ a_i < 2^30).", "Độ dài lớn nhất.",
    ["5 5\n1 4 2 1 4\n"], _g, _sol, brute=_br, tags=["sparse table", "hai con trỏ"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, r.choice([n * 5, n, 10**9]))
    qs = [sorted((r.randint(1, n), r.randint(1, n))) for _ in range(q)]
    return lines(J(n, q), L(a), *(J(x, y) for x, y in qs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    nxt = [n] * n; last = {}
    for i in range(n - 1, -1, -1):
        nxt[i] = last.get(a[i], n); last[a[i]] = i
    sp = Sparse(nxt, min); out = []
    for _ in range(q):
        l, r_ = rd.ints(2)
        out.append("YES" if sp.q(l - 1, r_ - 1) <= r_ - 1 else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r_ = rd.ints(2); seg = a[l - 1:r_]
        out.append("YES" if len(set(seg)) < len(seg) else "NO")
    return out


add(T, "Đoạn có phần tử trùng", 3, """
Với truy vấn `(l, r)`: trong đoạn `a_l..a_r` có hai phần tử bằng nhau không?

Gợi ý: `nxt[i]` = vị trí tiếp theo có cùng giá trị với `a_i`. Đoạn có phần tử trùng ⇔ `min(nxt[l..r]) ≤ r`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in `YES` hoặc `NO`.", ["5 3\n1 2 3 1 2\n1 3\n1 4\n4 5\n"], _g, _sol, brute=_br, tags=["sparse table"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    a = []
    while len(a) < n:
        k = r.randint(1, 8); p = list(range(1, k + 1)); r.shuffle(p)
        if r.random() < .2:
            p[r.randrange(k)] = r.randint(1, k + 1)
        a += p
    a = a[:n]
    qs = []
    for _ in range(q):
        x = r.randint(1, n); y = min(n, x + r.randint(0, 8)) if r.random() < .8 else r.randint(x, n)
        qs.append(J(x, y))
    return lines(J(n, q), L(a), *qs)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    nxt = [n] * n; last = {}
    for i in range(n - 1, -1, -1):
        nxt[i] = last.get(a[i], n); last[a[i]] = i
    sn, smx, smn = Sparse(nxt, min), Sparse(a, max), Sparse(a, min)
    out = []
    for _ in range(q):
        l, r_ = rd.ints(2); l -= 1; r_ -= 1; ln = r_ - l + 1
        ok = smn.q(l, r_) == 1 and smx.q(l, r_) == ln and sn.q(l, r_) > r_
        out.append("YES" if ok else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r_ = rd.ints(2)
        out.append("YES" if sorted(a[l - 1:r_]) == list(range(1, r_ - l + 2)) else "NO")
    return out


add(T, "Đoạn là hoán vị", 4, """
Với truy vấn `(l, r)`: đoạn `a_l..a_r` có phải là một hoán vị của `1, 2, ..., r - l + 1` không?

Gợi ý: đoạn độ dài `len` là hoán vị ⇔ các phần tử đôi một khác nhau, `min = 1` và `max = len`. Cả ba điều kiện kiểm tra bằng bảng thưa.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in `YES` hoặc `NO`.", ["6 3\n2 1 3 1 2 2\n1 3\n2 4\n4 5\n"], _g, _sol, brute=_br, tags=["sparse table"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, r.choice([3, 1000, 10**9]))
    if r.random() < .5:
        a = sorted(a)
        for _ in range(n // 20):
            i = r.randrange(n); a[i] = r.randint(1, 10**9)
    qs = [sorted((r.randint(1, n), r.randint(1, n))) for _ in range(q)]
    return lines(J(n, q), L(a), *(J(x, y) for x, y in qs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    run = [1] * n
    for i in range(1, n):
        if a[i] > a[i - 1]:
            run[i] = run[i - 1] + 1
    end = [0] * n  # vị trí cuối của đoạn tăng chứa i
    end[n - 1] = n - 1
    for i in range(n - 2, -1, -1):
        end[i] = end[i + 1] if a[i + 1] > a[i] else i
    sp = Sparse(run, max); out = []
    for _ in range(q):
        l, r_ = rd.ints(2); l -= 1; r_ -= 1
        e = min(end[l], r_)
        best = e - l + 1
        if e < r_:
            best = max(best, sp.q(e + 1, r_))
        out.append(best)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        l, r_ = rd.ints(2); best = cur = 1
        for i in range(l, r_):
            cur = cur + 1 if a[i] > a[i - 1] else 1
            best = max(best, cur)
        out.append(best)
    return out


add(T, "Đoạn tăng dài nhất trong truy vấn", 4, """
Với truy vấn `(l, r)`: tìm độ dài đoạn con liên tiếp **tăng ngặt** dài nhất nằm trong `a_l..a_r`.

Gợi ý: `run[i]` = độ dài đoạn tăng kết thúc tại `i` (tính trên cả dãy). Phần đầu đoạn truy vấn (từ `l` tới hết đoạn tăng chứa `l`)
xử lý riêng vì `run` ở đó có thể "tràn" ra ngoài `l`; phần còn lại là `max(run)` trên đoạn → bảng thưa.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["7 3\n1 2 3 1 2 3 4\n1 7\n2 5\n4 4\n"], _g, _sol, brute=_br, tags=["sparse table"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    t = []
    while len(t) < n:
        if r.random() < .5:
            k = r.randint(1, 5); t += ["("] * k + [")"] * k
        else:
            t.append(r.choice("()"))
    t = "".join(t[:n])
    qs = [sorted((r.randint(1, n), r.randint(1, n))) for _ in range(q)]
    return lines(J(n, q), t, *(J(x, y) for x, y in qs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str()
    p = [0]
    for c in t:
        p.append(p[-1] + (1 if c == "(" else -1))
    sp = Sparse(p, min); out = []
    for _ in range(q):
        l, r_ = rd.ints(2)
        ok = p[r_] == p[l - 1] and sp.q(l, r_) >= p[l - 1]
        out.append("YES" if ok else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str(); out = []
    for _ in range(q):
        l, r_ = rd.ints(2); bal = 0; ok = True
        for c in t[l - 1:r_]:
            bal += 1 if c == "(" else -1
            if bal < 0:
                ok = False
        out.append("YES" if ok and bal == 0 else "NO")
    return out


add(T, "Dãy ngoặc đúng trên đoạn", 4, """
Cho xâu ngoặc `s` và `q` truy vấn `(l, r)`: xâu con `s[l..r]` có phải dãy ngoặc đúng không?

Gợi ý: `p[i]` = (số `(`) − (số `)`) trong `i` ký tự đầu. `s[l..r]` đúng ⇔ `p[r] = p[l-1]` và `min(p[l..r]) ≥ p[l-1]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai là xâu ngoặc độ dài `n`. `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in `YES` hoặc `NO`.", ["6 3\n(()())\n1 6\n2 3\n2 5\n"], _g, _sol, brute=_br, tags=["sparse table", "tiền tố"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, r.choice([10, 10**9]))
    return lines(str(n), L(a))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    mx, mn = Sparse(a, max), Sparse(a, min)
    r_ = 0; out = []
    for l in range(n):
        if r_ < l:
            r_ = l
        while r_ + 1 < n and mx.q(l, r_ + 1) <= 2 * mn.q(l, r_ + 1):
            r_ += 1
        out.append(r_ - l + 1)
    return L(out)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); out = []
    for l in range(n):
        mx = mn = a[l]; best = 1
        for r_ in range(l + 1, n):
            mx = max(mx, a[r_]); mn = min(mn, a[r_])
            if mx <= 2 * mn:
                best = r_ - l + 1
            else:
                break
        out.append(best)
    return L(out)


add(T, "Đội hình cân đối", 3, """
Với mỗi vị trí `l`, tìm độ dài lớn nhất của đoạn bắt đầu tại `l` sao cho phần tử lớn nhất không vượt quá **hai lần** phần tử nhỏ nhất.

Gợi ý: khi `l` tăng, đầu phải tốt nhất không giảm → hai con trỏ, max/min của cửa sổ lấy bằng bảng thưa (hoặc deque).
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["5\n3 5 7 4 9\n"], _g, _sol, brute=_br, tags=["sparse table", "hai con trỏ"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 2, 10**5), S(s, 1, 10**5)
    a = arr(r, n, 1, r.choice([2, 5, n]))
    qs = [sorted(r.sample(range(1, n + 1), 2)) for _ in range(q)]
    return lines(J(n, q), L(a), *(J(x, y) for x, y in qs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    reach = [min(n - 1, i + a[i]) for i in range(n)]
    sp = Sparse([(reach[i], i) for i in range(n)], max)
    # bước tham lam: từ đoạn [.., i] với tầm xa reach[i], bước tiếp theo nhảy tới j trong [i+1..reach[i]] có reach lớn nhất
    best = [sp.q(i, reach[i])[1] if reach[i] > i else i for i in range(n)]
    LOG = max(1, n.bit_length())
    up = [best]
    for _ in range(1, LOG):
        p = up[-1]; up.append([p[p[i]] for i in range(n)])
    out = []
    for _ in range(q):
        l, r_ = rd.ints(2); l -= 1; r_ -= 1
        if reach[l] >= r_:
            out.append(1); continue
        u, c = l, 0
        for j in range(LOG - 1, -1, -1):
            v = up[j][u]
            if reach[v] < r_:
                u = v; c += 1 << j
        v = best[u]
        if reach[v] < r_ or v == u:
            out.append(-1)
        else:
            out.append(c + 2)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    from collections import deque
    for _ in range(q):
        l, r_ = rd.ints(2); l -= 1; r_ -= 1
        d = {l: 0}; dq = deque([l]); res = -1
        while dq:
            u = dq.popleft()
            if u == r_:
                res = d[u]; break
            for v in range(u + 1, min(r_, u + a[u]) + 1):
                if v not in d:
                    d[v] = d[u] + 1; dq.append(v)
        out.append(res)
    return out


add(T, "Nhảy xa ít bước nhất", 5, """
Có `n` ô, từ ô `i` có thể nhảy tới bất kỳ ô `j` với `i < j ≤ i + a_i`. Với truy vấn `(l, r)` (l < r), tìm số bước nhảy ít nhất từ ô `l` tới ô `r`,
hoặc `-1` nếu không thể.

Gợi ý: tham lam — từ `i`, bước tiếp theo nên nhảy tới ô `j ∈ (i, i + a_i]` có `j + a_j` lớn nhất (tìm bằng bảng thưa argmax).
Gọi ô đó là `best[i]`; dùng nhảy nhị phân trên `best` để đếm số bước cho tới khi tầm với chạm `r`.
""", "Dòng đầu `n, q` (2 ≤ n ≤ 10^5, 1 ≤ q ≤ 10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ n). `q` dòng sau mỗi dòng `l r` (l < r).",
    "Mỗi truy vấn in một dòng.", ["6 3\n2 3 1 1 4 1\n1 5\n1 6\n3 4\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 200 else _sol(s), tags=["nhảy nhị phân", "tham lam", "sparse table"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 5 * 10**5); q = S(s, 1, 5 * 10**5)
    return J(n, q, r.randint(1, 10**9), r.randint(1, 10**9))


def _sol(s):
    n, q, seed_a, seed_q = map(int, s.split())
    M = 2**31
    x = seed_a; a = [0] * n
    for i in range(n):
        x = (x * 1103515245 + 12345) % M; a[i] = x
    sp = Sparse(a, min)
    y = seed_q; tot = 0
    for _ in range(q):
        y = (y * 1103515245 + 12345) % M; l = y % n
        y = (y * 1103515245 + 12345) % M; r_ = y % n
        if l > r_:
            l, r_ = r_, l
        tot += sp.q(l, r_)
    return tot


add(T, "RMQ siêu tốc", 2, """
Dữ liệu được sinh bằng công thức để tránh nhập quá lớn. Với `x_0 = A`, `x_{i+1} = (x_i · 1103515245 + 12345) mod 2^31`:
`a_i = x_{i+1}` với `i = 0..n-1`. Sau đó với `y_0 = B` và cùng công thức, truy vấn thứ `j` dùng hai số kế tiếp
`l = y mod n`, `r = y' mod n` (đổi chỗ nếu `l > r`, chỉ số từ 0).

Hãy in **tổng** các giá trị `min(a_l..a_r)` của `q` truy vấn. Với `n, q` tới `5·10^5`, truy vấn `O(1)` — đây là lúc bảng thưa thể hiện sức mạnh.
""", "Một dòng `n q A B` (1 ≤ n, q ≤ 5·10^5, 1 ≤ A, B ≤ 10^9).", "Tổng các kết quả (vừa `long long`).",
    ["5 3 1 2\n"], _g, _sol, tags=["sparse table", "RMQ"], tl=2000)
