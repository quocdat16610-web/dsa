"""Chuyên đề 8: Quy hoạch động đếm."""
from functools import lru_cache
from .base import add, Rd, S, J, L, arr, lines, rstr, rtree

T = 8
MOD = 10**9 + 7


@lru_cache(None)
def _facts(n):
    f = [1] * (n + 1)
    for i in range(1, n + 1):
        f[i] = f[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(f[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return f, inv


def C(n, k):
    if k < 0 or k > n or n < 0:
        return 0
    f, inv = _facts(2 * 10**6 + 5)
    return f[n] * inv[k] % MOD * inv[n - k] % MOD


# 1 -----------------------------------------------------------------------
def _sol(s):
    n, m = map(int, s.split())
    row = [1] * m
    for _ in range(n - 1):
        for j in range(1, m):
            row[j] = (row[j] + row[j - 1]) % MOD
    return row[-1]


add(T, "Đếm đường đi trên lưới", 1, """
Đếm số đường đi từ ô `(1, 1)` tới ô `(n, m)` của lưới, mỗi bước chỉ sang phải hoặc xuống dưới. In modulo `10^9 + 7`.

Gợi ý: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. (Thực ra đáp án là `C(n+m-2, n-1)` — hãy thử cả hai cách!)
""", "Một dòng `n, m` (1 ≤ n, m ≤ 1000).", "Số đường đi modulo 10^9+7.", ["2 3\n", "3 3\n"],
    lambda r, s: J(r.randint(1, S(s, 1, 1000)), r.randint(1, S(s, 1, 1000))), _sol, tags=["QHĐ đếm"],
    brute=lambda s: (lambda n, m: C(n + m - 2, n - 1))(*map(int, s.split())))


# 2 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    a, b = 1, 1  # kết thúc bằng 0, kết thúc bằng 1 (độ dài 1)
    for _ in range(n - 1):
        a, b = (a + b) % MOD, a
    return (a + b) % MOD


def _br(s):
    n = int(s)
    return sum(1 for m in range(1 << n) if m & (m >> 1) == 0) % MOD


add(T, "Xâu nhị phân không có hai số 1 liền nhau", 1, """
Đếm số xâu nhị phân độ dài `n` không chứa hai ký tự `1` đứng cạnh nhau, modulo `10^9 + 7`.

Gợi ý: `end0[i] = end0[i-1] + end1[i-1]`, `end1[i] = end0[i-1]`.
""", "Một số `n` (1 ≤ n ≤ 10^6).", "Số xâu modulo 10^9+7.", ["3\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 10**6))), _sol, brute=_br, tags=["QHĐ đếm"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, (a + b) % MOD
    return b


add(T, "Lát gạch 2 × n", 1, """
Đếm số cách lát kín hình chữ nhật `2 × n` bằng các viên gạch domino `1 × 2` (được xoay), modulo `10^9 + 7`.

Gợi ý: cột cuối hoặc là một viên dựng đứng (còn `2 × (n-1)`), hoặc hai viên nằm ngang chồng nhau (còn `2 × (n-2)`).
""", "Một số `n` (1 ≤ n ≤ 10^6).", "Số cách modulo 10^9+7.", ["3\n", "1\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 10**6))), _sol, tags=["QHĐ đếm"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    if n % 2:
        return 0
    # f(n) = 4 f(n-2) - f(n-4), f(0)=1, f(2)=3
    a, b = 1, 3
    for _ in range(n // 2 - 1):
        a, b = b, (4 * b - a) % MOD
    return b


def _br(s):
    n = int(s)

    @lru_cache(None)
    def go(col, mask):
        if col == n:
            return 1 if mask == 0 else 0
        res = 0

        def fill(row, cur, nxt):
            nonlocal res
            if row == 3:
                res_add(nxt)
                return
            if cur >> row & 1:
                fill(row + 1, cur, nxt)
                return
            fill(row + 1, cur | 1 << row, nxt | 1 << row)
            if row < 2 and not cur >> (row + 1) & 1:
                fill(row + 2, cur | 3 << row, nxt)
        acc = []

        def res_add(nx):
            acc.append(nx)
        fill(0, mask, 0)
        return sum(go(col + 1, nx) for nx in acc)
    return go(0, 0) % MOD


add(T, "Lát gạch 3 × n", 2, """
Đếm số cách lát kín hình chữ nhật `3 × n` bằng domino `1 × 2`, modulo `10^9 + 7`.

Gợi ý: với `n` lẻ đáp án là 0. Phân tích cột cuối cho công thức `f(n) = 4·f(n-2) - f(n-4)`; hoặc tổng quát hơn,
QHĐ theo cột với trạng thái là bitmask các ô đã bị lấp ở cột tiếp theo (broken profile).
""", "Một số `n` (1 ≤ n ≤ 10^6).", "Số cách modulo 10^9+7.", ["2\n", "8\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 10**6))), _sol,
    brute=lambda s: _br(s) if int(s) <= 30 else _sol(s), tags=["QHĐ đếm", "bitmask"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    dp = [1] + [0] * n
    for k in range(1, n + 1):
        for v in range(k, n + 1):
            dp[v] = (dp[v] + dp[v - k]) % MOD
    return dp[n]


add(T, "Phân hoạch số", 2, """
Đếm số cách viết `n` thành tổng các số nguyên dương **không kể thứ tự** (ví dụ `4 = 4 = 3+1 = 2+2 = 2+1+1 = 1+1+1+1`, 5 cách),
modulo `10^9 + 7`.

Gợi ý: đây là bài đổi tiền không thứ tự với các mệnh giá `1, 2, ..., n`.
""", "Một số `n` (1 ≤ n ≤ 2000).", "Số cách modulo 10^9+7.", ["4\n", "10\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 2000))), _sol, tags=["QHĐ đếm"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    dp = [1] + [0] * n
    for k in range(1, n + 1):
        for v in range(n, k - 1, -1):
            dp[v] = (dp[v] + dp[v - k]) % MOD
    return dp[n]


add(T, "Phân hoạch thành các số phân biệt", 2, """
Đếm số cách viết `n` thành tổng các số nguyên dương **đôi một khác nhau** (không kể thứ tự), modulo `10^9 + 7`.
Ví dụ `6 = 6 = 5+1 = 4+2 = 3+2+1` (4 cách).

Gợi ý: cái túi 0/1 — mỗi số `k` dùng tối đa một lần, duyệt tổng **giảm dần**.
""", "Một số `n` (1 ≤ n ≤ 2000).", "Số cách modulo 10^9+7.", ["6\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 2000))), _sol, tags=["QHĐ đếm", "cái túi"])


# 7 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    tot = n * (n + 1) // 2
    if tot % 2:
        return 0
    h = tot // 2
    dp = [1] + [0] * h
    for k in range(1, n + 1):
        for v in range(h, k - 1, -1):
            dp[v] = (dp[v] + dp[v - k]) % MOD
    return dp[h] * pow(2, MOD - 2, MOD) % MOD


add(T, "Chia hai tập bằng nhau", 2, """
Đếm số cách chia các số `1, 2, ..., n` thành hai tập có tổng bằng nhau (hai cách chỉ khác nhau bởi việc đổi tên hai tập
được tính là một), modulo `10^9 + 7`.

Gợi ý: đếm số tập con có tổng `n(n+1)/4`, rồi chia 2 (nhân nghịch đảo modulo của 2).
""", "Một số `n` (1 ≤ n ≤ 200).", "Số cách modulo 10^9+7.", ["7\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 200))), _sol, tags=["QHĐ đếm", "cái túi"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 2 * 10**4), r.randint(1, S(s, 2, 50))
    a = [r.randint(1, m) if r.random() < .3 else 0 for _ in range(n)]
    # đảm bảo các giá trị đã biết có thể hợp lệ phần nào (không bắt buộc)
    return lines(J(n, m), L(a))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n)
    dp = [0] * (m + 2)
    if a[0]:
        dp[a[0]] = 1
    else:
        dp[1:m + 1] = [1] * m
    for i in range(1, n):
        nd = [0] * (m + 2)
        for v in ([a[i]] if a[i] else range(1, m + 1)):
            nd[v] = (dp[v - 1] + dp[v] + dp[v + 1]) % MOD
        dp = nd
    return sum(dp) % MOD


add(T, "Mô tả dãy", 2, """
Một dãy `n` số nguyên trong `[1, m]` thoả mãn: hai số liền kề chênh lệch nhau không quá 1. Một số phần tử đã bị mất
(ghi là `0`). Đếm số cách khôi phục dãy, modulo `10^9 + 7`.

Gợi ý: `dp[i][v]` = số cách cho `i` phần tử đầu với `a_i = v`; `dp[i][v] = dp[i-1][v-1] + dp[i-1][v] + dp[i-1][v+1]`.
""", "Dòng đầu `n, m` (1 ≤ n ≤ 2·10^4, 1 ≤ m ≤ 50). Dòng sau `n` số (0 ≤ a_i ≤ m; 0 là phần tử bị mất).",
    "Số cách modulo 10^9+7.", ["3 5\n2 0 2\n"], _g, _sol, tags=["QHĐ đếm"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2000)
    return lines(str(n), L(arr(r, n, 1, r.choice([3, 100, 10**9]))))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    dp = [1] * n
    for i in range(n):
        ai = a[i]; t = 1
        for j in range(i):
            if a[j] < ai:
                t += dp[j]
        dp[i] = t % MOD
    return sum(dp) % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); c = 0
    for m in range(1, 1 << n):
        b = [a[i] for i in range(n) if m >> i & 1]
        c += all(b[i] < b[i + 1] for i in range(len(b) - 1))
    return c % MOD


add(T, "Đếm dãy con tăng", 3, """
Đếm số dãy con (không cần liên tiếp, chọn theo chỉ số, khác rỗng) **tăng ngặt** của dãy, modulo `10^9 + 7`.

Gợi ý: `dp[i]` = số dãy con tăng kết thúc tại `i` = `1 + Σ_{j<i, a_j<a_i} dp[j]`. Độ phức tạp `O(n²)`
(nâng cao: dùng cây Fenwick để đạt `O(n log n)`).
""", "Dòng đầu `n` (1 ≤ n ≤ 2000). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số dãy con modulo 10^9+7.",
    ["3\n1 3 2\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 15 else _sol(s), tags=["QHĐ đếm"])


# 10 ----------------------------------------------------------------------
def _sol(s):
    t = s.split()[0]
    dp, last = 1, {}  # dp = số dãy con phân biệt (kể cả rỗng)
    for c in t:
        nd = (2 * dp - last.get(c, 0)) % MOD
        last[c] = dp
        dp = nd
    return (dp - 1) % MOD


def _br(s):
    t = s.split()[0]; n = len(t)
    return len({"".join(t[i] for i in range(n) if m >> i & 1) for m in range(1, 1 << n)}) % MOD


add(T, "Số xâu con phân biệt", 3, """
Đếm số **xâu** khác rỗng phân biệt có thể nhận được bằng cách xoá một số ký tự (giữ nguyên thứ tự) của xâu `s`, modulo `10^9 + 7`.
Ví dụ `aba` cho 6 xâu: `a, b, ab, aa, ba, aba`.

Gợi ý: `dp[i] = 2·dp[i-1] - dp[last(s_i) - 1]` — trừ đi các xâu bị đếm trùng do lần xuất hiện trước của cùng ký tự.
""", "Một dòng là xâu `s` gồm chữ cái thường (1 ≤ |s| ≤ 10^5).", "Số xâu modulo 10^9+7.", ["aba\n", "aaa\n"],
    lambda r, s: rstr(r, S(s, 1, 10**5), "abcdefghijklmnopqrstuvwxyz"[:r.choice([1, 2, 4, 26])]), _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 14 else _sol(s), tags=["QHĐ đếm", "xâu"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    return lines(str(q), L(r.randint(0, S(s, 5, 10**6)) for _ in range(q)))


add(T, "Số Catalan", 3, """
Số Catalan `C_n` đếm rất nhiều thứ: số dãy ngoặc đúng gồm `n` cặp, số cây nhị phân `n` nút, số cách chia đa giác...
Công thức: `C_n = C(2n, n) / (n + 1)`. Với mỗi truy vấn `n`, in `C_n mod (10^9 + 7)`.

Gợi ý: tính trước giai thừa và nghịch đảo giai thừa tới `2·10^6`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Dòng sau `Q` số `n` (0 ≤ n ≤ 10^6).", "Một dòng gồm `Q` số.",
    ["4\n0 1 3 5\n"], _g,
    lambda s: L(C(2 * n, n) * pow(n + 1, MOD - 2, MOD) % MOD for n in map(int, s.split()[1:])),
    tags=["tổ hợp", "Catalan"])


# 12 ----------------------------------------------------------------------
@lru_cache(None)
def _towers(N):
    a, b = [0] * (N + 1), [0] * (N + 1)  # a: tầng trên cùng là 1 khối rộng 2; b: hai khối rộng 1
    a[1] = b[1] = 1
    for i in range(2, N + 1):
        a[i] = (2 * a[i - 1] + b[i - 1]) % MOD
        b[i] = (a[i - 1] + 4 * b[i - 1]) % MOD
    return [(a[i] + b[i]) % MOD for i in range(N + 1)]


def _g(r, s):
    q = S(s, 1, 100)
    return lines(str(q), *(str(r.randint(1, S(s, 3, 10**6))) for _ in range(q)))


add(T, "Đếm số toà tháp", 3, """
Xây một toà tháp rộng 2, cao `n` từ các khối hình chữ nhật (mỗi khối rộng 1 hoặc 2, cao tuỳ ý, cạnh nguyên).
Hai toà tháp khác nhau nếu cách chia thành các khối khác nhau. Với mỗi `n`, đếm số toà tháp modulo `10^9 + 7`.
Ví dụ `n = 2` có 8 toà tháp, `n = 6` có 2864 toà tháp.

Gợi ý: xét từ dưới lên, hai trạng thái ở mỗi tầng: tầng hiện tại thuộc một khối rộng 2, hoặc hai khối rộng 1.
Mỗi khối có thể "kéo dài" lên tầng trên hoặc kết thúc.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 100). `Q` dòng sau mỗi dòng một số `n` (1 ≤ n ≤ 10^6).", "Mỗi truy vấn in một dòng.",
    ["3\n2\n6\n1337\n"], _g, lambda s: [_towers(10**6)[int(x)] for x in s.split()[1:]], tags=["QHĐ đếm"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    m = S(s, 1, 1000)
    return J(m, r.randint(1, m), r.randint(0, S(s, 1, 1000)))


def _sol(s):
    m, p, k = map(int, s.split())
    dp = [0] * (m + 2); dp[p] = 1
    for _ in range(k):
        dp = [0] + [(dp[i - 1] + dp[i + 1]) % MOD for i in range(1, m + 1)] + [0]
    return sum(dp) % MOD


add(T, "Robot trên đoạn thẳng", 3, """
Robot đứng ở ô `p` trên dải ô `1..m`. Mỗi bước robot sang trái hoặc sang phải một ô và không được ra ngoài dải.
Đếm số cách đi đúng `k` bước, modulo `10^9 + 7`.
""", "Một dòng `m, p, k` (1 ≤ p ≤ m ≤ 1000, 0 ≤ k ≤ 1000).", "Số cách modulo 10^9+7.", ["3 1 2\n", "1 1 1\n"],
    _g, _sol, tags=["QHĐ đếm"])


# 14 ----------------------------------------------------------------------
def _cnt_noadj(n):
    """Số x trong [0, n] không có hai chữ số kề nhau bằng nhau."""
    if n < 0:
        return 0
    d = list(map(int, str(n)))

    @lru_cache(None)
    def go(i, prev, tight, started):
        if i == len(d):
            return 1
        lim = d[i] if tight else 9
        res = 0
        for x in range(lim + 1):
            if started and x == prev:
                continue
            res += go(i + 1, x, tight and x == lim, started or x != 0)
        return res
    return go(0, -1, True, False)


def _g(r, s):
    hi = S(s, 30, 10**18)
    a, b = sorted((r.randint(0, hi), r.randint(0, hi)))
    return J(a, b)


add(T, "Đếm số không có chữ số kề bằng nhau", 4, """
Đếm số số nguyên `x ∈ [a, b]` mà hai chữ số kề nhau bất kỳ của `x` đều khác nhau (ví dụ 1213 thoả, 1223 không thoả).

Gợi ý (QHĐ chữ số): `f(n)` = số số thoả mãn trong `[0, n]`; đáp án `f(b) - f(a-1)`. Trạng thái:
vị trí, chữ số trước, cờ "đang bám sát n" (tight), cờ "đã bắt đầu số" (để xử lý số 0 đứng đầu).
""", "Một dòng `a, b` (0 ≤ a ≤ b ≤ 10^18).", "Số lượng số thoả mãn.", ["123 321\n"], _g,
    lambda s: (lambda a, b: _cnt_noadj(b) - _cnt_noadj(a - 1))(*map(int, s.split())),
    brute=lambda s: (lambda a, b: sum(1 for x in range(a, b + 1) if all(p != q for p, q in zip(str(x), str(x)[1:]))))(*map(int, s.split())),
    tags=["QHĐ chữ số"])


# 15 ----------------------------------------------------------------------
def _sol(s):
    k, d = s.split()
    d = int(d)
    dp = [0] * d  # dp[r] = số cách (không bám sát) với tổng chữ số ≡ r
    tight = 0
    for ch in k:
        c = int(ch)
        nd = [0] * d
        for r_ in range(d):
            v = dp[r_]
            if v:
                for x in range(10):
                    nd[(r_ + x) % d] += v
        for x in range(c):
            nd[(tight + x) % d] += 1
        dp = [v % MOD for v in nd]
        tight = (tight + c) % d
    return (dp[0] + (1 if tight == 0 else 0) - 1) % MOD


def _g(r, s):
    ln = S(s, 1, 1000)
    k = str(r.randint(1, 9)) + "".join(str(r.randint(0, 9)) for _ in range(ln - 1))
    return lines(k, str(r.randint(1, 100)))


add(T, "Tổng chữ số chia hết cho D", 4, """
Đếm số số nguyên `x ∈ [1, K]` có tổng các chữ số chia hết cho `D`, modulo `10^9 + 7`. Lưu ý `K` có thể có tới 1000 chữ số.

Gợi ý (QHĐ chữ số): trạng thái là (vị trí, tổng chữ số mod D, tight). Nhớ trừ số 0.
""", "Dòng đầu là `K` (1 ≤ K < 10^1000). Dòng hai là `D` (1 ≤ D ≤ 100).", "Kết quả modulo 10^9+7.",
    ["30\n4\n", "1000000009\n1\n"], _g, _sol,
    brute=lambda s: (lambda k, d: sum(1 for x in range(1, k + 1) if sum(map(int, str(x))) % d == 0) % MOD)(*map(int, s.split()))
    if len(s.split()[0]) <= 5 else _sol(s), tags=["QHĐ chữ số"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 1000)
    return lines(str(n), "".join(r.choice("<>") for _ in range(n - 1)))


def _sol(s):
    rd = Rd(s); n = rd.int(); t = rd.str() if n > 1 else ""
    dp = [1]  # dp[j]: số cách với phần tử cuối có hạng j (0-based) trong i phần tử đầu
    for i in range(1, n):
        pre = [0]
        for v in dp:
            pre.append((pre[-1] + v) % MOD)
        if t[i - 1] == "<":
            dp = [pre[j] for j in range(i + 1)]
        else:
            dp = [(pre[i] - pre[j]) % MOD for j in range(i + 1)]
    return sum(dp) % MOD


def _br(s):
    from itertools import permutations
    rd = Rd(s); n = rd.int(); t = rd.str() if n > 1 else ""
    return sum(1 for p in permutations(range(n))
               if all((p[i] < p[i + 1]) == (t[i] == "<") for i in range(n - 1)))


add(T, "Hoán vị theo mẫu", 4, """
Cho xâu `t` độ dài `n - 1` gồm `<` và `>`. Đếm số hoán vị `p` của `1..n` thoả mãn: `p_i < p_{i+1}` nếu `t_i = '<'`,
và `p_i > p_{i+1}` nếu `t_i = '>'`. In modulo `10^9 + 7`.

Gợi ý: `dp[i][j]` = số cách xếp `i` phần tử đầu sao cho phần tử cuối có thứ hạng `j` trong số `i` phần tử đó.
Chuyển trạng thái bằng tổng tiền tố → `O(n²)`.
""", "Dòng đầu `n` (2 ≤ n ≤ 1000). Dòng sau là xâu `t` độ dài `n - 1`.", "Số hoán vị modulo 10^9+7.",
    ["4\n<><\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 8 else _sol(s), tags=["QHĐ đếm", "tiền tố"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n, k = S(s, 1, 1000), r.randint(1, S(s, 2, 1000))
    return lines(J(n, k), L(arr(r, n, 1, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    dp = [0] * k; dp[0] = 1
    for x in a:
        x %= k
        dp = [(dp[j] + dp[(j - x) % k]) % MOD for j in range(k)]
    return (dp[0] - 1) % MOD


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for m in range(1, 1 << n) if sum(a[i] for i in range(n) if m >> i & 1) % k == 0) % MOD


add(T, "Tập con có tổng chia hết cho k", 3, """
Đếm số tập con **khác rỗng** (theo chỉ số) của dãy có tổng chia hết cho `k`, modulo `10^9 + 7`.

Gợi ý: `dp[j]` = số tập con có tổng ≡ j (mod k). Thêm phần tử `x`: `dp'[j] = dp[j] + dp[(j - x) mod k]`.
""", "Dòng đầu `n, k` (1 ≤ n, k ≤ 1000). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số tập con modulo 10^9+7.",
    ["3 3\n1 2 3\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 15 else _sol(s), tags=["QHĐ đếm"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 16)
    p = r.choice([.3, .5, .8])
    return lines(str(n), *(L(1 if r.random() < p else 0 for _ in range(n)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = [rd.ints(n) for _ in range(n)]
    dp = [0] * (1 << n); dp[0] = 1
    for m in range(1 << n):
        if not dp[m]:
            continue
        i = bin(m).count("1")
        if i == n:
            continue
        for j in range(n):
            if a[i][j] and not m >> j & 1:
                dp[m | 1 << j] = (dp[m | 1 << j] + dp[m]) % MOD
    return dp[-1]


add(T, "Ghép cặp hoàn hảo", 4, """
Có `n` nam và `n` nữ; `a[i][j] = 1` nếu nam `i` và nữ `j` hợp nhau. Đếm số cách ghép thành `n` cặp (mỗi người đúng một cặp,
chỉ ghép những người hợp nhau), modulo `10^9 + 7`.

Gợi ý: `dp[mask]` = số cách ghép `popcount(mask)` nam đầu tiên với tập nữ `mask`.
""", "Dòng đầu `n` (1 ≤ n ≤ 16). `n` dòng sau mỗi dòng `n` số 0/1.", "Số cách modulo 10^9+7.",
    ["3\n0 1 1\n1 0 1\n1 1 1\n"], _g, _sol, tags=["QHĐ bitmask", "QHĐ đếm"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 50); k = r.randint(0, S(s, 3, 2 * 10**4))
    return lines(J(n, k), L(arr(r, n, 0, max(1, k // r.choice([1, 2, n])))))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    dp = [1] + [0] * k
    for ai in a:
        pre = [0]
        for v in dp:
            pre.append((pre[-1] + v) % MOD)
        dp = [(pre[j + 1] - pre[max(0, j - ai)]) % MOD for j in range(k + 1)]
    return dp[k]


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    dp = [1] + [0] * k
    for ai in a:
        dp = [sum(dp[j - t] for t in range(0, min(ai, j) + 1)) % MOD for j in range(k + 1)]
    return dp[k]


add(T, "Chia kẹo có giới hạn", 4, """
Chia **hết** đúng `K` viên kẹo cho `n` em bé, em thứ `i` nhận từ 0 đến `a_i` viên.
Đếm số cách chia, modulo `10^9 + 7`.

Gợi ý: `dp[i][j] = Σ_{t=0..a_i} dp[i-1][j-t]` — dùng tổng tiền tố để mỗi bước `O(K)`.
""", "Dòng đầu `n, K` (1 ≤ n ≤ 50, 0 ≤ K ≤ 2·10^4). Dòng sau `n` số (0 ≤ a_i ≤ K).", "Số cách modulo 10^9+7.",
    ["3 4\n1 2 3\n"], _g, _sol, brute=_br, tags=["QHĐ đếm", "tiền tố"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    h, w = S(s, 2, 10**5), S(s, 2, 10**5)
    n = min(S(s, 1, 1000), h * w - 2)
    cells = set()
    while len(cells) < n:
        x, y = r.randint(1, h), r.randint(1, w)
        if (x, y) not in ((1, 1), (h, w)):
            cells.add((x, y))
    return lines(J(h, w, n), *(J(x, y) for x, y in cells))


def _sol(s):
    rd = Rd(s); h, w, n = rd.ints(3)
    walls = sorted(tuple(rd.ints(2)) for _ in range(n))
    walls.append((h, w))
    f = []
    for i, (x, y) in enumerate(walls):
        v = C(x + y - 2, x - 1)
        for j in range(i):
            px, py = walls[j]
            if px <= x and py <= y:
                v -= f[j] * C(x - px + y - py, x - px)
        f.append(v % MOD)
    return f[-1]


def _br(s):
    rd = Rd(s); h, w, n = rd.ints(3)
    bad = {tuple(rd.ints(2)) for _ in range(n)}
    if h * w > 4 * 10**4:
        return _sol(s)
    dp = [[0] * (w + 1) for _ in range(h + 1)]
    for i in range(1, h + 1):
        for j in range(1, w + 1):
            if (i, j) in bad:
                continue
            dp[i][j] = 1 if i == j == 1 else (dp[i - 1][j] + dp[i][j - 1]) % MOD
    return dp[h][w]


add(T, "Lưới khổng lồ có tường", 5, """
Lưới `H × W` (rất lớn) có `N` ô tường. Đếm số đường đi từ `(1, 1)` tới `(H, W)` chỉ đi sang phải/xuống dưới, không đi qua ô tường,
modulo `10^9 + 7`.

Gợi ý: số đường đi tự do từ `(1,1)` tới `(x,y)` là `C(x+y-2, x-1)`. Sắp xếp các ô tường; `f[i]` = số đường đi tới tường `i`
**không đi qua tường nào khác trước đó** = `C(...) - Σ f[j] · (số đường từ tường j tới tường i)`. Coi `(H, W)` là "tường" cuối cùng.
Độ phức tạp `O(N²)`.
""", "Dòng đầu `H, W, N` (2 ≤ H, W ≤ 10^5, 1 ≤ N ≤ 1000). `N` dòng sau là toạ độ các ô tường (phân biệt, khác ô đầu và ô cuối).",
    "Số đường đi modulo 10^9+7.", ["3 4 2\n2 2\n1 4\n"], _g, _sol, brute=_br, tags=["QHĐ đếm", "tổ hợp"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 300)
    return J(n, r.randint(0, min(n * (n - 1) // 2, S(s, 5, 10**4))))


def _sol(s):
    n, k = map(int, s.split())
    dp = [1] + [0] * k
    for i in range(1, n + 1):
        pre = [0]
        for v in dp:
            pre.append((pre[-1] + v) % MOD)
        dp = [(pre[j + 1] - pre[max(0, j - i + 1)]) % MOD for j in range(k + 1)]
    return dp[k]


def _br(s):
    from itertools import permutations
    n, k = map(int, s.split())
    return sum(1 for p in permutations(range(n))
               if sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j]) == k) % MOD


add(T, "Hoán vị có k nghịch thế", 5, """
Nghịch thế của hoán vị `p` là cặp `i < j` mà `p_i > p_j`. Đếm số hoán vị của `1..n` có **đúng** `k` nghịch thế, modulo `10^9 + 7`.

Gợi ý: chèn số `i` vào hoán vị của `i - 1` số đầu tạo thêm từ `0` đến `i - 1` nghịch thế:
`dp[i][j] = Σ_{t=0..i-1} dp[i-1][j-t]` — tính bằng tổng tiền tố.
""", "Một dòng `n, k` (1 ≤ n ≤ 300, 0 ≤ k ≤ 10^4).", "Số hoán vị modulo 10^9+7.", ["4 1\n", "3 3\n"],
    _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 7 else _sol(s), tags=["QHĐ đếm", "tiền tố"])


# 22 ----------------------------------------------------------------------
def _g(r, s):
    al = "abcdefghijklmnopqrstuvwxyz"
    n = S(s, 1, 1000)
    p = rstr(r, r.randint(1, S(s, 1, 100)), al[:r.choice([1, 2, 26])])
    return lines(str(n), p)


def _sol(s):
    rd = Rd(s); n = rd.int(); p = rd.str(); m = len(p)
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k and p[i] != p[k]:
            k = fail[k - 1]
        if p[i] == p[k]:
            k += 1
        fail[i] = k
    nxt = [[0] * 26 for _ in range(m)]
    for st in range(m):
        for c in range(26):
            ch = chr(97 + c)
            if p[st] == ch:
                nxt[st][c] = st + 1
            else:
                nxt[st][c] = nxt[fail[st - 1]][c] if st else 0
    dp = [0] * m; dp[0] = 1
    for _ in range(n):
        nd = [0] * m
        for st in range(m):
            v = dp[st]
            if v:
                row = nxt[st]
                for c in range(26):
                    t = row[c]
                    if t < m:
                        nd[t] += v
        dp = [v % MOD for v in nd]
    return sum(dp) % MOD


def _br(s):
    from itertools import product
    rd = Rd(s); n = rd.int(); p = rd.str()
    if n > 4:
        return _sol(s)
    return sum(1 for t in product("abcdefghijklmnopqrstuvwxyz", repeat=n) if p not in "".join(t)) % MOD


add(T, "Xâu không chứa mẫu cấm", 5, """
Đếm số xâu độ dài `n` gồm chữ cái thường **không** chứa `p` như một xâu con liên tiếp, modulo `10^9 + 7`.

Gợi ý: QHĐ trên automaton KMP — trạng thái là độ dài tiền tố dài nhất của `p` đang khớp với hậu tố của xâu đã dựng.
Không được bước tới trạng thái `|p|`.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). Dòng hai là xâu `p` (1 ≤ |p| ≤ 100).", "Số xâu modulo 10^9+7.",
    ["2\nab\n", "3\naaa\n"], _g, _sol, brute=_br, tags=["QHĐ đếm", "KMP"], tl=2000)


# 23 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), *(J(a, b) for a, b in rtree(r, n)))


def _sol(s):
    rd = Rd(s); n = rd.int()
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = rd.ints(2); adj[a - 1].append(b - 1); adj[b - 1].append(a - 1)
    par = [-1] * n; order = [0]; seen = [False] * n; seen[0] = True
    for u in order:
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True; par[v] = u; order.append(v)
    w = [1] * n; b = [1] * n  # w: u trắng, b: u đen
    for u in reversed(order):
        p = par[u]
        if p >= 0:
            w[p] = w[p] * (w[u] + b[u]) % MOD
            b[p] = b[p] * w[u] % MOD
    return (w[0] + b[0]) % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); es = [rd.ints(2) for _ in range(n - 1)]
    return sum(1 for m in range(1 << n) if all(not (m >> (a - 1) & 1 and m >> (b - 1) & 1) for a, b in es)) % MOD


add(T, "Tô màu cây", 4, """
Tô mỗi đỉnh của cây `n` đỉnh bằng màu trắng hoặc đen sao cho không có hai đỉnh **đen** nào kề nhau. Đếm số cách tô, modulo `10^9 + 7`.

Gợi ý: `trắng[u] = Π (trắng[con] + đen[con])`, `đen[u] = Π trắng[con]`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Số cách modulo 10^9+7.",
    ["3\n1 2\n2 3\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 15 else _sol(s), tags=["QHĐ trên cây", "QHĐ đếm"])
