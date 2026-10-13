"""Chuyên đề 3: Tìm kiếm nhị phân (trên mảng và trên đáp án)."""
from bisect import bisect_left, bisect_right
from math import gcd, isqrt
from .base import add, Rd, S, J, L, arr, lines

T = 3


def sorted_arr(r, n, hi, dup=True):
    if dup:
        return sorted(arr(r, n, 1, hi))
    return sorted(r.sample(range(1, max(hi, 2 * n) + 1), n))


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    a = sorted_arr(r, n, S(s, 20, 10**9), dup=False)
    xs = [r.choice(a) if r.random() < .5 else r.randint(1, a[-1] + 1) for _ in range(q)]
    return lines(J(n, q), L(a), L(xs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    out = []
    for x in rd.ints(q):
        i = bisect_left(a, x)
        out.append(i + 1 if i < n and a[i] == x else -1)
    return L(out)


add(T, "Tìm vị trí", 1, """
Cho dãy `a` gồm `n` số **tăng ngặt** và `q` truy vấn `x`. Với mỗi truy vấn in vị trí của `x` trong dãy (đánh số từ 1), hoặc `-1` nếu không có.

Gợi ý: giữ đoạn `[lo, hi]` chứa đáp án; so sánh `a[mid]` với `x` để bỏ đi một nửa. Mỗi truy vấn `O(log n)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai là dãy tăng ngặt (1 ≤ a_i ≤ 10^9). Dòng ba gồm `q` số `x`.",
    "Một dòng gồm `q` số.", ["5 3\n1 3 5 7 9\n7 2 1\n"], _g, _sol, tags=["tìm kiếm nhị phân"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    hi = S(s, 20, 10**9)
    return lines(J(n, q), L(arr(r, n, 1, hi)), L(arr(r, q, 0, hi + 1)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = sorted(rd.ints(n))
    return L(bisect_right(a, x) for x in rd.ints(q))


add(T, "Đếm số phần tử không vượt quá x", 1, """
Cho dãy `a` (chưa sắp xếp) và `q` truy vấn `x`. Với mỗi truy vấn đếm số phần tử `a_i ≤ x`.

Gợi ý: sắp xếp dãy, rồi dùng `upper_bound(a, a + n, x) - a`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). Dòng ba gồm `q` số `x` (0 ≤ x ≤ 10^9 + 1).",
    "Một dòng gồm `q` số.", ["5 3\n5 1 4 2 2\n2 0 10\n"], _g, _sol, tags=["tìm kiếm nhị phân", "sắp xếp"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    hi = S(s, 5, 10**5)
    return lines(J(n, q), L(sorted(arr(r, n, 1, hi))), L(arr(r, q, 1, hi + 1)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n)
    return L(bisect_right(a, x) - bisect_left(a, x) for x in rd.ints(q))


add(T, "Số lần xuất hiện", 1, """
Cho dãy `a` **không giảm** và `q` truy vấn `x`. Đếm số lần `x` xuất hiện trong dãy.

Gợi ý: `upper_bound(x) - lower_bound(x)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai là dãy không giảm. Dòng ba gồm `q` số `x`.",
    "Một dòng gồm `q` số.", ["6 3\n1 2 2 2 5 5\n2 5 3\n"], _g, _sol, tags=["tìm kiếm nhị phân"])


# 4 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    xs = []
    for _ in range(q):
        c = r.random()
        if c < .3:
            k = r.randint(0, 10**9); xs.append(k * k)
        elif c < .5:
            k = r.randint(1, 10**9); xs.append(k * k - 1)
        else:
            xs.append(r.randint(0, S(s, 100, 10**18)))
    return lines(str(q), *map(str, xs))


add(T, "Căn bậc hai nguyên", 1, """
Với mỗi số `n`, in ra số nguyên `x` lớn nhất thoả `x² ≤ n`.

Lưu ý: hàm `sqrt` của C++ dùng số thực nên có thể sai với `n` lớn — hãy dùng tìm kiếm nhị phân trên `x ∈ [0, 10^9]`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). `Q` dòng sau mỗi dòng một số `n` (0 ≤ n ≤ 10^18).",
    "Mỗi số in một dòng.", ["4\n0\n15\n16\n1000000000000000000\n"], _g,
    lambda s: [isqrt(x) for x in list(map(int, s.split()))[1:]], tags=["tìm kiếm nhị phân"])


# 5 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    hi = S(s, 20, 10**9)
    qs = [sorted((r.randint(1, hi), r.randint(1, hi))) for _ in range(q)]
    return lines(J(n, q), L(arr(r, n, 1, hi)), *(J(a, b) for a, b in qs))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = sorted(rd.ints(n))
    return [bisect_right(a, b) - bisect_left(a, x) for x, b in (rd.ints(2) for _ in range(q))]


add(T, "Đếm phần tử trong khoảng giá trị", 2, """
Cho dãy `a` và `q` truy vấn `(L, R)`. Với mỗi truy vấn đếm số phần tử có giá trị trong `[L, R]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` số (1 ≤ a_i ≤ 10^9). `q` dòng sau mỗi dòng `L R` (L ≤ R).",
    "Mỗi truy vấn in một dòng.", ["5 2\n10 1 10 3 4\n1 10\n2 9\n"], _g, _sol, tags=["tìm kiếm nhị phân"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5)
    hi = S(s, 20, 10**9)
    return lines(J(n, r.randint(1, 2 * hi)), L(arr(r, n, 1, hi)))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = sorted(rd.ints(n))
    tot = 0
    for i, v in enumerate(a):
        j = bisect_right(a, x - v, 0, i)
        tot += j
    return tot


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] + a[j] <= x)


add(T, "Cặp có tổng không vượt quá x", 2, """
Đếm số cặp chỉ số `i < j` sao cho `a_i + a_j ≤ x`.

Gợi ý: sắp xếp; với mỗi `j`, đếm số `i < j` có `a_i ≤ x - a_j` bằng `upper_bound`. Kết quả có thể lớn — dùng `long long`.
""", "Dòng đầu `n, x` (2 ≤ n ≤ 2·10^5, 1 ≤ x ≤ 2·10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số cặp.",
    ["4 5\n1 2 3 4\n"], _g, _sol, brute=_br, tags=["tìm kiếm nhị phân", "sắp xếp"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, S(s, 20, 10**9))
    return lines(J(n, r.randint(1, sum(a))), L(a))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    lo, hi = 1, max(a)
    while lo < hi:
        m = (lo + hi + 1) // 2
        if sum(x // m for x in a) >= k:
            lo = m
        else:
            hi = m - 1
    return lo


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return max(m for m in range(1, max(a) + 1) if sum(x // m for x in a) >= k)


add(T, "Chia kẹo", 2, """
Có `n` túi kẹo, túi thứ `i` có `a_i` viên. Cô giáo muốn chia cho `k` học sinh, mỗi em nhận **cùng số** `x` viên
và các viên của một em phải lấy từ **một túi duy nhất** (một túi có thể chia cho nhiều em). Tìm `x` lớn nhất.
Dữ liệu đảm bảo `x ≥ 1` luôn thoả mãn.

Gợi ý (tìm kiếm nhị phân trên đáp án): với `x` cố định, số em chia được là `Σ ⌊a_i / x⌋` — hàm này giảm theo `x`.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 1 ≤ k ≤ Σa_i). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Giá trị `x` lớn nhất.",
    ["3 7\n10 5 7\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, S(s, 20, 10**9))), L(arr(r, n, 1, S(s, 10, 10**9))))


def _sol(s):
    rd = Rd(s); n, t = rd.ints(2); a = rd.ints(n)
    lo, hi = 1, min(a) * t
    while lo < hi:
        m = (lo + hi) // 2
        if sum(m // x for x in a) >= t:
            hi = m
        else:
            lo = m + 1
    return lo


add(T, "Nhà máy", 2, """
Nhà máy có `n` máy, máy thứ `i` cần `a_i` giây để làm ra một sản phẩm. Các máy chạy song song.
Hỏi thời gian ít nhất để làm được `t` sản phẩm.

Gợi ý: sau `m` giây làm được `Σ ⌊m / a_i⌋` sản phẩm. Tìm `m` nhỏ nhất để giá trị này ≥ t. Cận trên `min(a)·t` có thể tới `10^18`.
""", "Dòng đầu `n, t` (1 ≤ n ≤ 2·10^5, 1 ≤ t ≤ 10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Thời gian nhỏ nhất.",
    ["3 7\n3 2 5\n"], _g, _sol, tags=["chặt nhị phân đáp án"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    xs = []
    for _ in range(q):
        if r.random() < .3:
            k = r.randint(1, 10**9); xs.append(k * (k + 1) // 2)
        else:
            xs.append(r.randint(1, S(s, 50, 10**18)))
    return lines(str(q), *map(str, xs))


def _f(n):
    x = isqrt(2 * n)
    while x * (x + 1) // 2 < n:
        x += 1
    while x > 0 and (x - 1) * x // 2 >= n:
        x -= 1
    return x


add(T, "Số tam giác", 2, """
Với mỗi số `n`, tìm số nguyên dương `x` nhỏ nhất sao cho `1 + 2 + ... + x ≥ n`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). `Q` dòng sau mỗi dòng một số `n` (1 ≤ n ≤ 10^18).",
    "Mỗi số in một dòng.", ["3\n1\n6\n7\n"], _g,
    lambda s: [_f(x) for x in list(map(int, s.split()))[1:]], tags=["tìm kiếm nhị phân"])


# 10 ----------------------------------------------------------------------
def _ok_div(a, k, m):
    parts, cur = 1, 0
    for x in a:
        if x > m:
            return False
        if cur + x > m:
            parts += 1; cur = x
        else:
            cur += x
    return parts <= k


def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n)), L(arr(r, n, 1, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    lo, hi = max(a), sum(a)
    while lo < hi:
        m = (lo + hi) // 2
        if _ok_div(a, k, m):
            hi = m
        else:
            lo = m + 1
    return lo


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    from itertools import combinations
    best = None
    for cuts in combinations(range(1, n), k - 1):
        b = [0, *cuts, n]
        v = max(sum(a[b[i]:b[i + 1]]) for i in range(k))
        best = v if best is None else min(best, v)
    return best


add(T, "Chia dãy", 3, """
Chia dãy `n` số dương thành **đúng** `k` đoạn liên tiếp khác rỗng sao cho tổng lớn nhất của các đoạn là nhỏ nhất.
In ra giá trị nhỏ nhất đó.

Gợi ý: kiểm tra "có chia được thành ≤ k đoạn, mỗi đoạn tổng ≤ m không?" bằng tham lam. (Chia được ≤ k đoạn thì tách thêm để có đúng k đoạn.)
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Giá trị nhỏ nhất.",
    ["5 3\n2 4 7 3 5\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án", "tham lam"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5)
    a = r.sample(range(0, S(s, 3 * n, 10**9) + 1), n)
    return lines(J(n, r.randint(2, n)), L(a))


def _sol(s):
    rd = Rd(s); n, c = rd.ints(2); a = sorted(rd.ints(n))

    def ok(d):
        cnt, last = 1, a[0]
        for x in a:
            if x - last >= d:
                cnt += 1; last = x
        return cnt >= c
    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(m):
            lo = m
        else:
            hi = m - 1
    return lo


def _br(s):
    rd = Rd(s); n, c = rd.ints(2); a = sorted(rd.ints(n))
    from itertools import combinations
    return max(min(b[i + 1] - b[i] for i in range(c - 1)) for b in combinations(a, c))


add(T, "Chuồng bò", 3, """
Có `n` chuồng nằm trên một đường thẳng tại toạ độ `x_1..x_n` (phân biệt). Cần nhốt `c` con bò vào `c` chuồng khác nhau
sao cho **khoảng cách nhỏ nhất** giữa hai con bò bất kỳ là lớn nhất. In ra khoảng cách đó.

Gợi ý: với khoảng cách `d`, đặt tham lam từ trái sang phải. Tìm `d` lớn nhất đặt được đủ `c` con.
""", "Dòng đầu `n, c` (2 ≤ c ≤ n ≤ 2·10^5). Dòng sau `n` toạ độ phân biệt (0 ≤ x_i ≤ 10^9).", "Khoảng cách lớn nhất.",
    ["5 3\n1 2 8 4 9\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án", "tham lam"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, 0, S(s, 20, 10**9))
    tot = sum(a)
    return lines(J(n, r.randint(0, tot)), L(a))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n)
    lo, hi = 0, max(a)
    while lo < hi:
        h = (lo + hi + 1) // 2
        if sum(x - h for x in a if x > h) >= m:
            lo = h
        else:
            hi = h - 1
    return lo


add(T, "Đốn gỗ", 3, """
Có `n` cây cao `a_1..a_n`. Bác tiều phu đặt lưỡi cưa ở độ cao `H` và cắt ngang tất cả các cây — mỗi cây cao hơn `H`
cho phần gỗ `a_i - H`. Cần lấy được **ít nhất** `M` mét gỗ. Tìm `H` lớn nhất (H nguyên, H ≥ 0).
""", "Dòng đầu `n, M` (1 ≤ n ≤ 2·10^5, 0 ≤ M ≤ Σa_i). Dòng sau `n` số (0 ≤ a_i ≤ 10^9).", "Giá trị `H` lớn nhất.",
    ["4 7\n20 15 10 17\n"], _g, _sol, tags=["chặt nhị phân đáp án"])


# 13 ----------------------------------------------------------------------
def _z(n):
    c = 0
    while n:
        n //= 5; c += n
    return c


def _sol(s):
    out = []
    for k in list(map(int, s.split()))[1:]:
        lo, hi = 0, 5 * k
        while lo < hi:
            m = (lo + hi) // 2
            if _z(m) >= k:
                hi = m
            else:
                lo = m + 1
        out.append(lo)
    return out


add(T, "Chữ số 0 tận cùng của giai thừa", 3, """
Với mỗi `k`, tìm số `n` nhỏ nhất sao cho `n!` có **ít nhất** `k` chữ số 0 tận cùng.

Gợi ý: số chữ số 0 tận cùng của `n!` là `⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ...` — hàm tăng theo `n`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^4). `Q` dòng sau mỗi dòng một số `k` (1 ≤ k ≤ 10^17).", "Mỗi truy vấn in một dòng.",
    ["3\n1\n5\n6\n"],
    lambda r, s: (lambda q: lines(str(q), *(str(r.randint(1, S(s, 30, 10**17))) for _ in range(q))))(S(s, 1, 10**4)),
    _sol, tags=["chặt nhị phân đáp án"])


# 14 ----------------------------------------------------------------------
def _sol(s):
    n, m, k = Rd(s).ints(3)
    if n > m:
        n, m = m, n
    lo, hi = 1, n * m
    while lo < hi:
        x = (lo + hi) // 2
        c = 0
        top = min(n, x)
        i = 1
        while i <= top:  # gom khối các i có cùng x // i
            q = x // i
            j = min(top, x // q)
            c += min(m, q) * (j - i + 1)
            i = j + 1
        if c >= k:
            hi = x
        else:
            lo = x + 1
    return lo


def _br(s):
    n, m, k = Rd(s).ints(3)
    return sorted(i * j for i in range(1, n + 1) for j in range(1, m + 1))[k - 1]


def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 10**5)
    return J(n, m, r.randint(1, n * m))


add(T, "Số thứ k trong bảng cửu chương", 3, """
Bảng `n × m` có ô `(i, j)` chứa số `i·j`. Sắp xếp `n·m` số này tăng dần; số đứng ở vị trí thứ `k` là bao nhiêu?

Gợi ý: số ô có giá trị ≤ x là `Σ_i min(m, ⌊x / i⌋)`. Tìm `x` nhỏ nhất để số này ≥ k.
""", "Một dòng `n, m, k` (1 ≤ n, m ≤ 10^5, 1 ≤ k ≤ n·m).", "Số thứ `k`.",
    ["2 3 4\n", "3 3 5\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án"])


# 15 ----------------------------------------------------------------------
def _sol(s):
    out = []
    for c in list(map(int, s.split()))[1:]:
        lo, hi = 0.0, 1e6
        for _ in range(100):
            m = (lo + hi) / 2
            if m * m * m + m < c:
                lo = m
            else:
                hi = m
        out.append(f"{lo:.6f}")
    return out


add(T, "Tìm kiếm nhị phân trên số thực", 3, """
Với mỗi `C`, tìm số thực `x ≥ 0` thoả mãn `x³ + x = C`. In `x` với 6 chữ số thập phân (chấp nhận sai số `10^-6`).

Gợi ý: hàm `f(x) = x³ + x` đồng biến. Lặp chia đôi khoảng `[0, 10^6]` khoảng 100 lần là đủ chính xác.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^4). `Q` dòng sau mỗi dòng một số nguyên `C` (0 ≤ C ≤ 10^15).", "Mỗi truy vấn in một số thực.",
    ["3\n2\n0\n10\n"],
    lambda r, s: (lambda q: lines(str(q), *(str(r.randint(0, S(s, 30, 10**15))) for _ in range(q))))(S(s, 1, 10**4)),
    _sol, checker="float", tags=["tìm kiếm nhị phân", "số thực"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = 2 * S(s, 0, 10**5) + 1
    return lines(J(n, r.randint(0, S(s, 10, 10**9))), L(arr(r, n, 1, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = sorted(rd.ints(n))
    h = a[n // 2:]
    lo, hi = h[0], h[0] + k
    while lo < hi:
        m = (lo + hi + 1) // 2
        need = 0
        for x in h:
            if x >= m:
                break
            need += m - x
        if need <= k:
            lo = m
        else:
            hi = m - 1
    return lo


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = sorted(rd.ints(n))
    for _ in range(k):
        a[n // 2] += 1
        a.sort()
    return a[n // 2]


add(T, "Trung vị lớn nhất", 4, """
Cho dãy `n` số (`n` lẻ) và `k` thao tác; mỗi thao tác tăng một phần tử bất kỳ thêm 1. Hãy làm cho **trung vị**
(phần tử đứng giữa sau khi sắp xếp) lớn nhất có thể.

Gợi ý: chỉ cần tăng nửa sau của dãy đã sắp xếp. Để trung vị ≥ m cần `Σ max(0, m - a_i)` với `i` từ giữa tới cuối.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 200001, n lẻ, 0 ≤ k ≤ 10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Trung vị lớn nhất.",
    ["3 2\n1 3 5\n", "5 5\n1 2 1 1 1\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    return lines(J(n, r.randint(1, n * n)), L(arr(r, n, 1, 10**9)), L(arr(r, n, 1, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = sorted(rd.ints(n)); b = sorted(rd.ints(n))
    lo, hi = a[0] + b[0], a[-1] + b[-1]
    while lo < hi:
        m = (lo + hi) // 2
        c, j = 0, n - 1
        for x in a:
            while j >= 0 and x + b[j] > m:
                j -= 1
            c += j + 1
        if c >= k:
            hi = m
        else:
            lo = m + 1
    return lo


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n); b = rd.ints(n)
    return sorted(x + y for x in a for y in b)[k - 1]


add(T, "Tổng cặp nhỏ thứ k", 4, """
Cho hai dãy `a`, `b` cùng độ dài `n`. Xét `n²` tổng `a_i + b_j`; sắp xếp tăng dần, in ra số đứng ở vị trí `k`.

Gợi ý: chặt nhị phân giá trị `m`; đếm số cặp có tổng ≤ m bằng hai con trỏ trên hai dãy đã sắp xếp (`O(n)`).
""", "Dòng đầu `n, k` (1 ≤ n ≤ 10^5, 1 ≤ k ≤ n²). Hai dòng sau là dãy `a` và `b` (1 ≤ a_i, b_i ≤ 10^9).", "Số thứ `k`.",
    ["3 4\n1 2 3\n1 2 3\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án", "hai con trỏ"], tl=2000)


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5)
    return lines(J(n, r.randint(1, n * (n - 1) // 2)), L(arr(r, n, 1, S(s, 50, 10**9))))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = sorted(rd.ints(n))
    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        m = (lo + hi) // 2
        c, i = 0, 0
        for j in range(n):
            while a[j] - a[i] > m:
                i += 1
            c += j - i
        if c >= k:
            hi = m
        else:
            lo = m + 1
    return lo


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sorted(abs(a[i] - a[j]) for i in range(n) for j in range(i + 1, n))[k - 1]


add(T, "Khoảng cách nhỏ thứ k", 4, """
Cho `n` số. Xét tất cả `n(n-1)/2` cặp `i < j` với khoảng cách `|a_i - a_j|`. Tìm khoảng cách nhỏ thứ `k`.
""", "Dòng đầu `n, k` (2 ≤ n ≤ 10^5, 1 ≤ k ≤ n(n-1)/2). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Khoảng cách thứ `k`.",
    ["4 3\n1 3 1 7\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án", "hai con trỏ"], tl=2000)


# 19 ----------------------------------------------------------------------
def _lcm(a, b):
    return a // gcd(a, b) * b


def _cnt3(x, a, b, c):
    ab, bc, ca = _lcm(a, b), _lcm(b, c), _lcm(c, a)
    return x // a + x // b + x // c - x // ab - x // bc - x // ca + x // _lcm(ab, c)


def _sol(s):
    rd = Rd(s); q = rd.int(); out = []
    for _ in range(q):
        k, a, b, c = rd.ints(4)
        lo, hi = 1, min(a, b, c) * k
        while lo < hi:
            m = (lo + hi) // 2
            if _cnt3(m, a, b, c) >= k:
                hi = m
            else:
                lo = m + 1
        out.append(lo)
    return out


def _br(s):
    rd = Rd(s); q = rd.int(); out = []
    for _ in range(q):
        k, a, b, c = rd.ints(4)
        x = 0
        while k:
            x += 1
            if x % a == 0 or x % b == 0 or x % c == 0:
                k -= 1
        out.append(x)
    return out


def _g(r, s):
    q = S(s, 1, 10**4)
    return lines(str(q), *(J(r.randint(1, S(s, 20, 10**9)), *arr(r, 3, 1, S(s, 10, 10**9))) for _ in range(q)))


add(T, "Số thứ k chia hết", 4, """
Với mỗi truy vấn `(k, a, b, c)`, tìm số nguyên dương nhỏ thứ `k` chia hết cho **ít nhất một** trong ba số `a, b, c`.

Gợi ý: số lượng số trong `[1, x]` thoả mãn tính bằng bao hàm - loại trừ với BCNN. Cẩn thận tràn số khi tính BCNN
(có thể dùng `__int128` hoặc chặn trên).
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^4). `Q` dòng sau mỗi dòng `k a b c` (1 ≤ k, a, b, c ≤ 10^9).", "Mỗi truy vấn in một dòng.",
    ["2\n4 2 3 5\n5 2 4 6\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án", "bao hàm loại trừ"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    rows = [L(arr(r, m, 0, 1000)) for _ in range(n)]
    return lines(J(n, m, r.randint(0, 500 * min(n, m) ** 2)), *rows)


def _sol(s):
    rd = Rd(s); n, m, lim = rd.ints(3)
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        row = rd.ints(m); run = 0
        Pi, Pp = P[i], P[i - 1]
        for j in range(1, m + 1):
            run += row[j - 1]
            Pi[j] = Pp[j] + run

    def ok(k):
        for i in range(k, n + 1):
            Pi, Pk = P[i], P[i - k]
            for j in range(k, m + 1):
                if Pi[j] - Pk[j] - Pi[j - k] + Pk[j - k] <= lim:
                    return True
        return False
    lo, hi = 0, min(n, m)
    while lo < hi:
        k = (lo + hi + 1) // 2
        if ok(k):
            lo = k
        else:
            hi = k - 1
    return lo


add(T, "Hình vuông lớn nhất có tổng không vượt quá S", 4, """
Cho bảng `n × m` số không âm và số `S`. Tìm cạnh `k` lớn nhất sao cho tồn tại một hình vuông con `k × k`
có tổng các ô ≤ S. In `0` nếu không có.

Gợi ý: nếu tồn tại hình vuông cạnh `k` thoả mãn thì cũng tồn tại cạnh `k-1` (các ô không âm) → chặt nhị phân `k`,
kiểm tra bằng tiền tố 2D.
""", "Dòng đầu `n, m, S` (1 ≤ n, m ≤ 500, 0 ≤ S ≤ 10^9). `n` dòng sau mỗi dòng `m` số (0 ≤ a ≤ 1000).", "Cạnh lớn nhất.",
    ["3 3 10\n1 2 3\n4 1 1\n9 1 1\n"], _g, _sol, tags=["chặt nhị phân đáp án", "tiền tố 2D"], tl=2000)


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n)), L(arr(r, n, 1, r.choice([n, 10**9]))))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    vals = sorted(set(a))

    def ok(x):
        p, mn, pre = 0, 0, [0] * (n + 1)
        for i in range(n):
            pre[i + 1] = pre[i] + (1 if a[i] >= x else -1)
        for i in range(k, n + 1):
            mn = min(mn, pre[i - k])
            if pre[i] - mn > 0:
                return True
        return False
    lo, hi = 0, len(vals) - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(vals[m]):
            lo = m
        else:
            hi = m - 1
    return vals[lo]


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    best = 0
    for i in range(n):
        for j in range(i + k, n + 1):
            b = sorted(a[i:j])
            best = max(best, b[(len(b) - 1) // 2])
    return best


add(T, "Trung vị đoạn con lớn nhất", 5, """
Trung vị của một dãy độ dài `len` là phần tử ở vị trí `⌊(len+1)/2⌋` sau khi sắp xếp tăng dần.
Tìm trung vị lớn nhất trong số các đoạn con liên tiếp có độ dài **ít nhất** `k`.

Gợi ý: chặt nhị phân giá trị `x`: "có đoạn dài ≥ k với trung vị ≥ x?" — đổi `a_i ≥ x` thành `+1`, còn lại `-1`;
cần đoạn dài ≥ k có tổng > 0 → dùng tiền tố và min tiền tố.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Trung vị lớn nhất.",
    ["5 3\n1 2 3 2 1\n", "4 2\n1 2 3 4\n"], _g, _sol, brute=_br, tags=["chặt nhị phân đáp án", "tiền tố"], tl=2000)


# 22 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**4)
    return lines(J(n, r.randint(1, n)), *(J(r.randint(1, 10**6), r.randint(1, 10**6)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2)
    it = [rd.ints(2) for _ in range(n)]
    lo, hi = 0.0, 1e6 + 1
    for _ in range(60):
        m = (lo + hi) / 2
        v = sorted((a - m * b for a, b in it), reverse=True)
        if sum(v[:k]) >= 0:
            lo = m
        else:
            hi = m
    return f"{lo:.6f}"


add(T, "Tối đa hoá tỉ số", 5, """
Có `n` món đồ, món `i` có giá trị `a_i` và khối lượng `b_i`. Chọn **đúng** `k` món sao cho tỉ số
`(Σ a) / (Σ b)` lớn nhất. In tỉ số đó (sai số cho phép `10^-6`).

Gợi ý (quy hoạch phân số): tỉ số ≥ x ⇔ `Σ (a_i - x·b_i) ≥ 0`. Với `x` cố định, chọn `k` món có `a_i - x·b_i` lớn nhất.
Chặt nhị phân trên số thực `x`.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^4). `n` dòng sau mỗi dòng `a_i b_i` (1 ≤ a_i, b_i ≤ 10^6).",
    "Tỉ số lớn nhất.", ["3 2\n2 2\n5 3\n2 1\n"], _g, _sol, checker="float",
    tags=["chặt nhị phân đáp án", "số thực"], tl=2000)
