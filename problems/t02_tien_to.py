"""Chuyên đề 2: Tổng tiền tố, mảng hiệu."""
from collections import defaultdict
from .base import add, Rd, S, J, L, arr, lines, rstr

T = 2
MOD = 10**9 + 7


def qs(r, n, q):
    out = []
    for _ in range(q):
        a, b = r.randint(1, n), r.randint(1, n)
        out.append((min(a, b), max(a, b)))
    return out


def pref(a):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return p


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, q), L(arr(r, n, -10**9, 10**9)), *(J(a, b) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); p = pref(rd.ints(n))
    return [p[b] - p[a - 1] for a, b in (rd.ints(2) for _ in range(q))]


add(T, "Tổng đoạn", 1, """
Cho dãy `a_1..a_n` và `q` truy vấn, mỗi truy vấn hỏi tổng `a_l + a_{l+1} + ... + a_r`.

Gợi ý: `p[i] = a_1 + ... + a_i`, tổng đoạn `[l, r]` là `p[r] - p[l-1]`. Dùng `long long`!
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số `|a_i| ≤ 10^9`. `q` dòng sau mỗi dòng `l r` (1 ≤ l ≤ r ≤ n).",
    "Mỗi truy vấn in một dòng.", ["5 3\n1 2 3 4 5\n1 5\n2 3\n4 4\n"], _g, _sol, tags=["tiền tố"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *(J(a, b) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); p = pref(x % 2 == 0 for x in rd.ints(n))
    return [p[b] - p[a - 1] for a, b in (rd.ints(2) for _ in range(q))]


add(T, "Đếm số chẵn trong đoạn", 1, """
Cho dãy `a` gồm `n` số nguyên dương và `q` truy vấn `(l, r)`. Với mỗi truy vấn, đếm số phần tử chẵn trong đoạn `a_l..a_r`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `l r`.",
    "Mỗi truy vấn in một dòng.", ["5 2\n1 2 4 7 8\n1 5\n4 4\n"], _g, _sol, tags=["tiền tố"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, -S(s, 3, 10**4), S(s, 3, 10**4))
    if r.random() < .6 and n >= 3:
        i = r.randrange(n)
        left, right = sum(a[:i]), sum(a[i + 1:])
        j = r.randrange(i + 1, n) if i + 1 < n else None
        if j is not None:
            a[j] += left - right
    return lines(str(n), L(a))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    tot, left = sum(a), 0
    for i, x in enumerate(a):
        if left == tot - left - x:
            return i + 1
        left += x
    return -1


add(T, "Điểm cân bằng", 1, """
Tìm chỉ số `i` **nhỏ nhất** sao cho tổng các phần tử bên trái `i` bằng tổng các phần tử bên phải `i`
(không tính `a_i`; tổng của tập rỗng bằng 0). Nếu không tồn tại in `-1`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số nguyên (|a_i| ≤ 10^9).",
    "Chỉ số `i` (đánh số từ 1) hoặc `-1`.", ["5\n1 3 5 2 2\n", "3\n1 2 3\n"], _g, _sol, tags=["tiền tố"])


# 4 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, q), L(arr(r, n, 0, 10**9)),
                 *(J(a, b, r.randint(-10**4, 10**4)) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    d = [0] * (n + 2)
    for _ in range(q):
        l, r_, x = rd.ints(3)
        d[l] += x; d[r_ + 1] -= x
    c, out = 0, []
    for i in range(n):
        c += d[i + 1]
        out.append(a[i] + c)
    return L(out)


add(T, "Mảng hiệu", 1, """
Cho dãy `a` gồm `n` phần tử và `q` thao tác `(l, r, x)`: cộng `x` vào mọi phần tử `a_l..a_r`.
In dãy sau khi thực hiện tất cả thao tác.

Gợi ý: mảng hiệu `d[l] += x, d[r+1] -= x`; cuối cùng cộng dồn `d` để biết lượng cộng vào mỗi vị trí.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (0 ≤ a_i ≤ 10^9). `q` dòng sau `l r x` (|x| ≤ 10^4).",
    "Một dòng gồm `n` số là dãy cuối cùng.", ["5 2\n1 1 1 1 1\n1 3 2\n2 5 -1\n"], _g, _sol, tags=["mảng hiệu"])


# 5 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n)), L(arr(r, n, -10**9, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); p = pref(rd.ints(n))
    return max(p[i] - p[i - k] for i in range(k, n + 1))


add(T, "Đoạn dài k có tổng lớn nhất", 1, """
Cho dãy `n` số và số `k`. Tìm đoạn con gồm đúng `k` phần tử liên tiếp có tổng lớn nhất, in ra tổng đó.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^9).", "Tổng lớn nhất.",
    ["5 2\n1 -2 3 4 -1\n"], _g, _sol, tags=["tiền tố"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    q = S(s, 1, 10**5)
    rows = [L(arr(r, m, -10**6, 10**6)) for _ in range(n)]
    out = []
    for _ in range(q):
        a, b = sorted((r.randint(1, n), r.randint(1, n)))
        c, d = sorted((r.randint(1, m), r.randint(1, m)))
        out.append(J(a, c, b, d))
    return lines(J(n, m, q), *rows, *out)


def _sol(s):
    rd = Rd(s); n, m, q = rd.ints(3)
    P = [[0] * (m + 1)]
    for i in range(n):
        row = rd.ints(m)
        pr, acc = P[-1], [0] * (m + 1)
        run = 0
        for j in range(m):
            run += row[j]
            acc[j + 1] = pr[j + 1] + run
        P.append(acc)
    out = []
    for _ in range(q):
        x1, y1, x2, y2 = rd.ints(4)
        out.append(P[x2][y2] - P[x1 - 1][y2] - P[x2][y1 - 1] + P[x1 - 1][y1 - 1])
    return out


add(T, "Tổng hình chữ nhật (tiền tố 2D)", 2, """
Cho bảng `n × m` số nguyên và `q` truy vấn `(x1, y1, x2, y2)`: tính tổng các ô trong hình chữ nhật có góc trên trái `(x1, y1)` và góc dưới phải `(x2, y2)`.

Gợi ý: `P[i][j] = a[i][j] + P[i-1][j] + P[i][j-1] - P[i-1][j-1]`;
tổng = `P[x2][y2] - P[x1-1][y2] - P[x2][y1-1] + P[x1-1][y1-1]`.
""", "Dòng đầu `n, m, q` (1 ≤ n, m ≤ 500, 1 ≤ q ≤ 10^5). `n` dòng tiếp theo mỗi dòng `m` số (|a| ≤ 10^6). `q` dòng truy vấn (x1 ≤ x2, y1 ≤ y2).",
    "Mỗi truy vấn in một dòng.", ["3 3 2\n1 2 3\n4 5 6\n7 8 9\n1 1 2 2\n2 2 3 3\n"], _g, _sol, tags=["tiền tố 2D"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    q = S(s, 1, 10**5)
    out = []
    for _ in range(q):
        a, b = sorted((r.randint(1, n), r.randint(1, n)))
        c, d = sorted((r.randint(1, m), r.randint(1, m)))
        out.append(J(a, c, b, d, r.randint(-1000, 1000)))
    return lines(J(n, m, q), *out)


def _sol(s):
    rd = Rd(s); n, m, q = rd.ints(3)
    D = [[0] * (m + 2) for _ in range(n + 2)]
    for _ in range(q):
        x1, y1, x2, y2, v = rd.ints(5)
        D[x1][y1] += v; D[x1][y2 + 1] -= v; D[x2 + 1][y1] -= v; D[x2 + 1][y2 + 1] += v
    out, prev = [], [0] * (m + 2)
    for i in range(1, n + 1):
        cur, run, row = [0] * (m + 2), 0, D[i]
        for j in range(1, m + 1):
            run += row[j]
            cur[j] = prev[j] + run
        out.append(L(cur[1:m + 1]))
        prev = cur
    return out


add(T, "Mảng hiệu 2D", 2, """
Bảng `n × m` ban đầu toàn số 0. Có `q` thao tác `(x1, y1, x2, y2, v)`: cộng `v` vào mọi ô trong hình chữ nhật.
In bảng cuối cùng.

Gợi ý: `D[x1][y1] += v; D[x1][y2+1] -= v; D[x2+1][y1] -= v; D[x2+1][y2+1] += v`, sau đó tính tiền tố 2D của `D`.
""", "Dòng đầu `n, m, q` (1 ≤ n, m ≤ 500, 1 ≤ q ≤ 10^5). `q` dòng sau mỗi dòng `x1 y1 x2 y2 v` (|v| ≤ 1000).",
    "`n` dòng, mỗi dòng `m` số.", ["3 3 2\n1 1 2 2 5\n2 2 3 3 1\n"], _g, _sol, tags=["mảng hiệu 2D"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    v = S(s, 3, 10**4)
    a = arr(r, n, -v, v)
    return lines(J(n, r.randint(-3 * v, 3 * v)), L(a))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    cnt = defaultdict(int); cnt[0] = 1
    p = tot = 0
    for x in a:
        p += x
        tot += cnt[p - k]
        cnt[p] += 1
    return tot


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i, n) if sum(a[i:j + 1]) == k)


add(T, "Đếm đoạn con có tổng bằng k", 2, """
Đếm số đoạn con liên tiếp `a_l..a_r` có tổng đúng bằng `k`. Các phần tử có thể âm.

Gợi ý: đoạn `(l, r]` có tổng `k` ⇔ `p[r] - p[l] = k`. Duyệt `r`, dùng `map` đếm số lần xuất hiện của `p[r] - k` trong các tiền tố trước đó.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, |k| ≤ 10^9). Dòng sau `n` số (|a_i| ≤ 10^4).", "Số đoạn con.",
    ["5 3\n1 2 0 3 -3\n"], _g, _sol, brute=_br, tags=["tiền tố", "map"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, S(s, 5, 10**9))), L(arr(r, n, -10**9, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    cnt = defaultdict(int); cnt[0] = 1
    p = tot = 0
    for x in a:
        p = (p + x) % k
        tot += cnt[p]
        cnt[p] += 1
    return tot


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i, n) if sum(a[i:j + 1]) % k == 0)


add(T, "Đoạn con chia hết cho k", 2, """
Đếm số đoạn con liên tiếp có tổng chia hết cho `k`.

Gợi ý: hai tiền tố có cùng số dư khi chia `k` cho ta một đoạn chia hết. Lưu ý trong C++ `x % k` có thể âm —
dùng `((x % k) + k) % k`.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 1 ≤ k ≤ 10^9). Dòng sau `n` số (|a_i| ≤ 10^9).", "Số đoạn con.",
    ["5 3\n1 2 3 4 5\n"], _g, _sol, brute=_br, tags=["tiền tố", "modulo"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    pr = r.random()
    return lines(str(n), "".join("1" if r.random() < pr else "0" for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); t = rd.str()
    first = {0: 0}; p = best = 0
    for i, ch in enumerate(t, 1):
        p += 1 if ch == "1" else -1
        if p in first:
            best = max(best, i - first[p])
        else:
            first[p] = i
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); t = rd.str()
    return max([j - i for i in range(n) for j in range(i + 1, n + 1) if t[i:j].count("1") * 2 == j - i] + [0])


add(T, "Xâu nhị phân cân bằng dài nhất", 2, """
Cho xâu nhị phân độ dài `n`. Tìm độ dài lớn nhất của một xâu con liên tiếp có số chữ `0` bằng số chữ `1`.

Gợi ý: đổi `0 → -1`, bài toán thành tìm đoạn dài nhất có tổng 0: lưu vị trí xuất hiện **đầu tiên** của mỗi giá trị tiền tố.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau là xâu nhị phân.", "Độ dài lớn nhất (0 nếu không có).",
    ["6\n110100\n", "3\n111\n"], _g, _sol, brute=_br, tags=["tiền tố", "map"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, -10**9, 10**9)
    if r.random() < .3:
        a = arr(r, n, -10**9, -1)
    return lines(str(n), L(a))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    best, mn, p = -10**30, 0, 0
    for x in a:
        p += x
        best = max(best, p - mn)
        mn = min(mn, p)
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return max(sum(a[i:j + 1]) for i in range(n) for j in range(i, n))


add(T, "Đoạn con có tổng lớn nhất", 3, """
Tìm đoạn con liên tiếp **khác rỗng** có tổng lớn nhất.

Gợi ý: tổng đoạn kết thúc tại `r` lớn nhất = `p[r] - min(p[0..r-1])`. (Đây cũng chính là thuật toán Kadane.)
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^9).", "Tổng lớn nhất.",
    ["5\n-1 2 3 -7 4\n", "3\n-5 -2 -9\n"], _g, _sol, brute=_br, tags=["tiền tố", "Kadane"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, q), L(arr(r, n, 0, 2**30 - 1)), *(J(a, b) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    p = [0]
    for x in a:
        p.append(p[-1] ^ x)
    return [p[b] ^ p[a_ - 1] for a_, b in (rd.ints(2) for _ in range(q))]


add(T, "XOR đoạn", 3, """
Cho dãy `a` và `q` truy vấn `(l, r)`, tính `a_l xor a_{l+1} xor ... xor a_r`.

Gợi ý: XOR cũng có "tiền tố": `x[r] xor x[l-1]` vì `v xor v = 0`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (0 ≤ a_i < 2^30). `q` dòng sau `l r`.",
    "Mỗi truy vấn in một dòng.", ["4 2\n1 2 3 4\n1 3\n2 4\n"], _g, _sol, tags=["tiền tố", "xor"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    al = "abcdefghijklmnopqrstuvwxyz"[:r.choice([2, 5, 26])]
    return lines(J(n, q), rstr(r, n, al), *(J(a, b, r.choice(al)) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str()
    P = {c: [0] * (n + 1) for c in set(t)}
    for c, row in P.items():
        run = 0
        for i, ch in enumerate(t):
            run += ch == c
            row[i + 1] = run
    out = []
    for _ in range(q):
        l, r_, c = int(rd.str()), int(rd.str()), rd.str()
        out.append(P[c][r_] - P[c][l - 1] if c in P else 0)
    return out


add(T, "Đếm ký tự trong đoạn", 3, """
Cho xâu `s` gồm chữ cái thường và `q` truy vấn `(l, r, c)`: đếm số lần ký tự `c` xuất hiện trong `s[l..r]`.

Gợi ý: 26 mảng tiền tố, `cnt[c][i]` = số ký tự `c` trong `i` ký tự đầu tiên.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai là xâu `s`. `q` dòng sau mỗi dòng `l r c`.",
    "Mỗi truy vấn in một dòng.", ["7 3\nabacaba\n1 7 a\n2 4 b\n3 3 z\n"], _g, _sol, tags=["tiền tố", "xâu"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    m = S(s, 10, 10**6)
    segs = [sorted((r.randint(1, m), r.randint(1, m))) for _ in range(n)]
    return lines(J(n, r.randint(1, max(1, min(n, 5 + n // 50)))), *(J(a, b) for a, b in segs))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2)
    d = [0] * (10**6 + 2)
    for _ in range(n):
        a, b = rd.ints(2)
        d[a] += 1; d[b + 1] -= 1
    c = tot = 0
    for i in range(1, 10**6 + 1):
        c += d[i]
        if c >= k:
            tot += 1
    return tot


add(T, "Điểm được phủ ít nhất k lần", 3, """
Cho `n` đoạn thẳng `[l_i, r_i]` trên trục số nguyên. Đếm số điểm nguyên được phủ bởi **ít nhất** `k` đoạn.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `l r` (1 ≤ l ≤ r ≤ 10^6).",
    "Số điểm nguyên thoả mãn.", ["3 2\n1 5\n3 8\n4 4\n"], _g, _sol, tags=["mảng hiệu"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 0, 10**9)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(x * (i + 1) * (n - i) for i, x in enumerate(a)) % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(sum(a[i:j + 1]) for i in range(n) for j in range(i, n)) % MOD


add(T, "Tổng của mọi đoạn con", 3, """
Tính tổng của tổng tất cả các đoạn con liên tiếp của dãy, lấy modulo `10^9 + 7`.

Gợi ý: `a_i` thuộc đúng `i · (n - i + 1)` đoạn con (chỉ số từ 1).
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ a_i ≤ 10^9).", "Kết quả modulo 10^9+7.",
    ["3\n1 2 3\n"], _g, _sol, brute=_br, tags=["đóng góp", "đếm"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, q), *(J(a, b) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2)
    d1 = [0] * (n + 3); d2 = [0] * (n + 3)
    # cộng (i - l + 1) cho i trong [l, r]: = i*1 + (1 - l)
    for _ in range(q):
        l, r_ = rd.ints(2)
        d1[l] += 1; d1[r_ + 1] -= 1
        d2[l] += 1 - l; d2[r_ + 1] -= 1 - l
    out, c1, c2 = [], 0, 0
    for i in range(1, n + 1):
        c1 += d1[i]; c2 += d2[i]
        out.append(c1 * i + c2)
    return L(out)


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = [0] * (n + 1)
    for _ in range(q):
        l, r_ = rd.ints(2)
        for i in range(l, r_ + 1):
            a[i] += i - l + 1
    return L(a[1:])


add(T, "Cộng cấp số cộng", 4, """
Dãy `n` phần tử ban đầu toàn 0. Mỗi thao tác `(l, r)` cộng `1` vào `a_l`, cộng `2` vào `a_{l+1}`, ..., cộng `r-l+1` vào `a_r`.
In dãy sau `q` thao tác.

Gợi ý: lượng cộng vào vị trí `i` là `i - l + 1 = 1·i + (1 - l)`. Dùng hai mảng hiệu: một cho hệ số của `i`, một cho hằng số.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `q` dòng sau mỗi dòng `l r`.", "Một dòng gồm `n` số.",
    ["5 2\n1 3\n2 5\n"], _g, _sol, brute=_br, tags=["mảng hiệu"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 100), S(s, 1, 100)
    return lines(J(n, m), *(L(arr(r, m, -100, 100)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    a = [rd.ints(m) for _ in range(n)]
    best = -10**18
    for top in range(n):
        col = [0] * m
        for bot in range(top, n):
            row = a[bot]
            cur, mn, p = -10**18, 0, 0
            for j in range(m):
                col[j] += row[j]
                p += col[j]
                if p - mn > cur:
                    cur = p - mn
                if p < mn:
                    mn = p
            if cur > best:
                best = cur
    return best


def _br(s):
    rd = Rd(s); n, m = rd.ints(2)
    a = [rd.ints(m) for _ in range(n)]
    return max(sum(a[i][j] for i in range(x1, x2 + 1) for j in range(y1, y2 + 1))
               for x1 in range(n) for x2 in range(x1, n) for y1 in range(m) for y2 in range(y1, m))


add(T, "Hình chữ nhật con có tổng lớn nhất", 4, """
Cho bảng `n × m`. Tìm hình chữ nhật con (khác rỗng) có tổng lớn nhất.

Gợi ý: cố định hàng trên `top` và hàng dưới `bot`, nén các cột lại thành dãy 1 chiều rồi chạy Kadane. Độ phức tạp `O(n²·m)`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 100). `n` dòng sau mỗi dòng `m` số (|a| ≤ 100).", "Tổng lớn nhất.",
    ["2 3\n1 -2 3\n-1 5 -6\n"], _g, _sol, brute=_br, tags=["tiền tố 2D", "Kadane"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 100), S(s, 1, 100)
    return lines(J(n, m), *(L(arr(r, m, -3, 3)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    a = [rd.ints(m) for _ in range(n)]
    if n > m:
        a = [list(c) for c in zip(*a)]; n, m = m, n
    tot = 0
    for top in range(n):
        col = [0] * m
        for bot in range(top, n):
            row = a[bot]
            cnt = {0: 1}; p = 0
            for j in range(m):
                col[j] += row[j]
                p += col[j]
                c = cnt.get(p, 0)
                tot += c
                cnt[p] = c + 1
    return tot


def _br(s):
    rd = Rd(s); n, m = rd.ints(2)
    a = [rd.ints(m) for _ in range(n)]
    return sum(1 for x1 in range(n) for x2 in range(x1, n) for y1 in range(m) for y2 in range(y1, m)
               if sum(a[i][j] for i in range(x1, x2 + 1) for j in range(y1, y2 + 1)) == 0)


add(T, "Đếm hình chữ nhật con có tổng 0", 4, """
Đếm số hình chữ nhật con của bảng `n × m` có tổng các phần tử bằng 0.

Gợi ý: cố định cặp hàng, nén cột, đưa về bài "đếm đoạn con có tổng bằng 0" với `map`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 100). `n` dòng sau mỗi dòng `m` số (|a| ≤ 3).", "Số hình chữ nhật.",
    ["2 2\n1 -1\n-1 1\n"], _g, _sol, brute=_br, tags=["tiền tố 2D", "map"], tl=2000)


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, -2, 2) if r.random() < .5 else [r.choice([0, 0, 1, -1]) for _ in range(n)]
    return lines(str(n), L(a))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    tot = sum(a)
    if tot % 3:
        return 0
    t = tot // 3
    p, cnt_first, ans = 0, 0, 0
    for i in range(n - 1):
        p += a[i]
        if p == 2 * t and i >= 1:
            ans += cnt_first
        if p == t:
            cnt_first += 1
    return ans


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(1 for i in range(1, n) for j in range(i + 1, n)
               if sum(a[:i]) == sum(a[i:j]) == sum(a[j:]))


add(T, "Chia dãy thành ba phần bằng nhau", 4, """
Đếm số cách chọn hai vị trí cắt `1 ≤ i < j < n` để chia dãy thành ba đoạn khác rỗng `a[1..i]`, `a[i+1..j]`, `a[j+1..n]`
có tổng bằng nhau.

Gợi ý: tổng mỗi phần phải là `S/3`. Duyệt điểm cắt thứ hai, đếm số điểm cắt thứ nhất hợp lệ phía trước.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^9).", "Số cách cắt.",
    ["5\n1 2 3 0 3\n", "4\n0 1 -1 0\n"], _g, _sol, brute=_br, tags=["tiền tố", "đếm"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, q), L(arr(r, n, -10**6, 10**6)), *(J(a, b) for a, b in qs(r, n, q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    p, w = [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        p[i] = p[i - 1] + a[i - 1]
        w[i] = w[i - 1] + a[i - 1] * i
    out = []
    for _ in range(q):
        l, r_ = rd.ints(2)
        out.append((w[r_] - w[l - 1]) - (l - 1) * (p[r_] - p[l - 1]))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    out = []
    for _ in range(q):
        l, r_ = rd.ints(2)
        out.append(sum(a[i - 1] * (i - l + 1) for i in range(l, r_ + 1)))
    return out


add(T, "Tổng có trọng số", 4, """
Cho dãy `a` và `q` truy vấn `(l, r)`. Tính `1·a_l + 2·a_{l+1} + ... + (r-l+1)·a_r`.

Gợi ý: `Σ (i - l + 1)·a_i = Σ i·a_i - (l-1)·Σ a_i` → cần hai mảng tiền tố: của `a_i` và của `i·a_i`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai `n` số (|a_i| ≤ 10^6). `q` dòng sau `l r`.",
    "Mỗi truy vấn in một dòng.", ["4 2\n1 2 3 4\n1 4\n2 3\n"], _g, _sol, brute=_br, tags=["tiền tố"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    return lines(str(n), L(arr(r, n, 0, 10**9)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    tot = 0
    for b in range(30):
        c = [1, 0]; px = 0; cnt = 0
        for x in a:
            px ^= (x >> b) & 1
            cnt += c[px ^ 1]
            c[px] += 1
        tot += cnt << b
    return tot % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    tot = 0
    for i in range(n):
        x = 0
        for j in range(i, n):
            x ^= a[j]
            tot += x
    return tot % MOD


add(T, "Tổng XOR của mọi đoạn con", 5, """
Tính tổng giá trị XOR của tất cả các đoạn con liên tiếp, lấy modulo `10^9 + 7`.

Gợi ý: xét từng bit `b`. Đoạn `(l, r]` có bit `b` bằng 1 khi tiền tố XOR tại `l` và `r` khác nhau ở bit `b`.
Đếm số cặp tiền tố khác bit → nhân `2^b`.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). Dòng sau `n` số (0 ≤ a_i ≤ 10^9).", "Kết quả modulo 10^9+7.",
    ["3\n1 2 3\n"], _g, _sol, brute=_br, tags=["tiền tố", "xor", "bit"], tl=1500)
