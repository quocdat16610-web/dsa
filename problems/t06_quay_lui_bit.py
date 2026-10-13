"""Chuyên đề 6: Đệ quy - Quay lui, Bitwise."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
from math import comb
from .base import add, Rd, S, J, L, arr, lines

T = 6
MOD = 10**9 + 7


def _small(lo, hi):
    """Sinh test chỉ là một số n trong [lo, hi], kích thước tăng dần theo s."""
    return lambda r, s: str(r.randint(lo, max(lo, S(s, lo, hi))) if s < 1 else hi)


# 1 -----------------------------------------------------------------------
def _fact(n):
    return 1 if n <= 1 else n * _fact(n - 1)


add(T, "Giai thừa", 1, """
Viết hàm **đệ quy** tính `n! = 1 · 2 · ... · n` (quy ước `0! = 1`).

Gợi ý: `fact(n) = n · fact(n - 1)`, điểm dừng `fact(0) = 1`. Với `n ≤ 20` kết quả vừa kiểu `long long`.
""", "Một số `n` (0 ≤ n ≤ 20).", "Giá trị `n!`.", ["5\n", "0\n"], _small(0, 20),
    lambda s: _fact(int(s)), tags=["đệ quy"])


# 2 -----------------------------------------------------------------------
add(T, "Liệt kê xâu nhị phân", 1, """
Liệt kê tất cả xâu nhị phân độ dài `n` theo thứ tự từ điển.

Gợi ý: hàm `gen(i)` thử đặt `0` rồi `1` vào vị trí `i`, gọi đệ quy `gen(i + 1)`; khi `i = n` thì in ra.
""", "Một số `n` (1 ≤ n ≤ 15).", "`2^n` dòng, mỗi dòng một xâu.", ["2\n"], _small(1, 15),
    lambda s: [format(i, "b").zfill(int(s)) for i in range(1 << int(s))], tags=["quay lui"])


# 3 -----------------------------------------------------------------------
add(T, "Liệt kê hoán vị", 1, """
Liệt kê tất cả hoán vị của `1, 2, ..., n` theo thứ tự từ điển, mỗi hoán vị trên một dòng.

Gợi ý: mảng `used[]` đánh dấu số đã dùng; tại mỗi vị trí thử các số chưa dùng theo thứ tự tăng dần.
""", "Một số `n` (1 ≤ n ≤ 8).", "`n!` dòng.", ["3\n"], _small(1, 8),
    lambda s: [L(p) for p in permutations(range(1, int(s) + 1))], tags=["quay lui"])


# 4 -----------------------------------------------------------------------
def _gq(lo, hi):
    def g(r, s):
        q = S(s, 1, 10**5)
        xs = []
        for _ in range(q):
            c = r.random()
            xs.append(1 << r.randint(0, 59) if c < .3 else r.randint(lo, hi))
        return lines(str(q), L(xs))
    return g


add(T, "Đếm bit 1", 1, """
Với mỗi số `x`, đếm số bit `1` trong biểu diễn nhị phân của nó.

Gợi ý: `x & (x - 1)` xoá bit 1 thấp nhất; hoặc dùng `__builtin_popcountll(x)`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Dòng sau `Q` số (0 ≤ x ≤ 10^18).", "Một dòng gồm `Q` số.",
    ["3\n5 0 255\n"], _gq(0, 10**18), lambda s: L(bin(int(x)).count("1") for x in s.split()[1:]), tags=["bitwise"])


# 5 -----------------------------------------------------------------------
add(T, "Luỹ thừa của 2", 1, """
Với mỗi số `x`, cho biết `x` có phải là luỹ thừa của 2 (1, 2, 4, 8, ...) hay không.

Gợi ý: `x > 0 && (x & (x - 1)) == 0`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Dòng sau `Q` số (1 ≤ x ≤ 10^18).", "Một dòng gồm `Q` từ `YES`/`NO`.",
    ["4\n1 6 64 100\n"], _gq(1, 10**18),
    lambda s: L("YES" if (int(x) & (int(x) - 1)) == 0 else "NO" for x in s.split()[1:]), tags=["bitwise"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n = r.randint(1, S(s, 1, 16)) if s < 1 else 16
    return J(n, r.randint(1, n) if s < 1 else 8)


add(T, "Liệt kê tổ hợp", 2, """
Liệt kê tất cả tập con gồm `k` phần tử của `{1, 2, ..., n}`, mỗi tập in các phần tử tăng dần, các tập theo thứ tự từ điển.

Gợi ý: `gen(i, start)` chọn phần tử thứ `i` trong `[start, n]`, phần tử tiếp theo phải lớn hơn.
""", "Một dòng `n, k` (1 ≤ k ≤ n ≤ 16).", "Mỗi dòng một tổ hợp.", ["4 2\n"], _g,
    lambda s: (lambda n, k: [L(c) for c in combinations(range(1, n + 1), k)])(*map(int, s.split())), tags=["quay lui"])


# 7 -----------------------------------------------------------------------
def _subset_sums(a):
    sums = [0]
    for x in a:
        sums += [v + x for v in sums]
    return sums


def _g(r, s):
    n = S(s, 1, 20)
    a = arr(r, n, 1, r.choice([5, 20, 10**9]))
    x = sum(r.sample(a, r.randint(0, n))) if r.random() < .7 else r.randint(0, sum(a))
    return lines(J(n, x), L(a))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    return _subset_sums(a).count(x)


add(T, "Đếm tập con có tổng x", 2, """
Cho `n` số nguyên dương. Đếm số tập con (theo chỉ số, kể cả tập rỗng) có tổng đúng bằng `x`.

Gợi ý: quay lui "chọn / không chọn" từng phần tử — `2^n` trạng thái.
""", "Dòng đầu `n, x` (1 ≤ n ≤ 20, 0 ≤ x ≤ 2·10^10). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số tập con.",
    ["4 5\n1 2 3 4\n"], _g, _sol, tags=["quay lui", "bitmask"])


# 8 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); tot = sum(a)
    return min(abs(tot - 2 * v) for v in _subset_sums(a))


add(T, "Chia táo", 2, """
Có `n` quả táo với khối lượng `p_i`. Chia táo thành hai nhóm sao cho chênh lệch tổng khối lượng hai nhóm là nhỏ nhất.
""", "Dòng đầu `n` (1 ≤ n ≤ 20). Dòng sau `n` số (1 ≤ p_i ≤ 10^9).", "Chênh lệch nhỏ nhất.",
    ["5\n3 2 7 4 1\n"], lambda r, s: (lambda n: lines(str(n), L(arr(r, n, 1, 10**9))))(S(s, 1, 20)), _sol,
    tags=["quay lui"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 0, 10**5)
    pool = arr(r, n + 1, 1, 10**9)
    a = pool[:n] * 2 + [pool[n]]
    r.shuffle(a)
    return lines(str(len(a)), L(a))


def _sol(s):
    x = 0
    for v in s.split()[1:]:
        x ^= int(v)
    return x


add(T, "Số lẻ loi", 1, """
Trong dãy có `2m + 1` số, mọi giá trị đều xuất hiện **chẵn** lần trừ đúng một giá trị xuất hiện lẻ lần. Tìm giá trị đó.

Gợi ý: XOR tất cả các số — các cặp giống nhau triệt tiêu (`x xor x = 0`). Không cần mảng!
""", "Dòng đầu `n` (n lẻ, 1 ≤ n ≤ 2·10^5 + 1). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Giá trị xuất hiện lẻ lần.",
    ["5\n4 7 4 9 7\n"], _g, _sol, tags=["bitwise", "xor"])


# 10 ----------------------------------------------------------------------
add(T, "Mã Gray", 2, """
Mã Gray `n` bit là cách sắp xếp tất cả `2^n` xâu nhị phân độ dài `n` sao cho hai xâu liên tiếp khác nhau đúng một bit.
In mã Gray phản xạ chuẩn: xâu thứ `i` (từ 0) là biểu diễn nhị phân `n` bit của `i xor (i >> 1)`.
""", "Một số `n` (1 ≤ n ≤ 16).", "`2^n` dòng.", ["2\n"], _small(1, 16),
    lambda s: [format(i ^ (i >> 1), "b").zfill(int(s)) for i in range(1 << int(s))], tags=["bitwise", "đệ quy"])


# 11 ----------------------------------------------------------------------
@lru_cache(None)
def _queens(n):
    full = (1 << n) - 1

    def go(cols, d1, d2):
        if cols == full:
            return 1
        c, free = 0, full & ~(cols | d1 | d2)
        while free:
            b = free & -free
            free ^= b
            c += go(cols | b, ((d1 | b) << 1) & full, (d2 | b) >> 1)
        return c
    return go(0, 0, 0)


add(T, "N quân hậu", 3, """
Đếm số cách đặt `n` quân hậu lên bàn cờ `n × n` sao cho không có hai quân nào ăn nhau (cùng hàng, cùng cột hoặc cùng đường chéo).

Gợi ý: đặt lần lượt từng hàng; mảng đánh dấu cột, đường chéo chính (`i - j`) và đường chéo phụ (`i + j`).
""", "Một số `n` (1 ≤ n ≤ 12).", "Số cách đặt.", ["4\n", "1\n"], _small(1, 12), lambda s: _queens(int(s)),
    tags=["quay lui"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    p = r.choice([0, .1, .2, .4])
    return lines(*("".join("*" if r.random() < p else "." for _ in range(8)) for _ in range(8)))


def _sol(s):
    b = s.split()

    def go(i, cols, d1, d2):
        if i == 8:
            return 1
        c = 0
        for j in range(8):
            if b[i][j] == "." and not (cols >> j & 1) and not (d1 >> (i + j) & 1) and not (d2 >> (i - j + 7) & 1):
                c += go(i + 1, cols | 1 << j, d1 | 1 << (i + j), d2 | 1 << (i - j + 7))
        return c
    return go(0, 0, 0, 0)


add(T, "Bàn cờ có ô cấm", 3, """
Đếm số cách đặt 8 quân hậu lên bàn cờ `8 × 8` không ăn nhau, biết các ô đánh dấu `*` bị cấm (không được đặt hậu).
""", "8 dòng, mỗi dòng 8 ký tự `.` (ô trống) hoặc `*` (ô cấm).", "Số cách đặt.",
    ["........\n........\n..*.....\n........\n........\n.....**.\n...*....\n........\n"], _g, _sol, tags=["quay lui"])


# 13 ----------------------------------------------------------------------
def _brackets(n):
    out = []

    def go(cur, op, cl):
        if len(cur) == 2 * n:
            out.append(cur); return
        if op < n:
            go(cur + "(", op + 1, cl)
        if cl < op:
            go(cur + ")", op, cl + 1)
    go("", 0, 0)
    return out


add(T, "Dãy ngoặc đúng", 3, """
Liệt kê tất cả dãy ngoặc đúng gồm `n` cặp ngoặc tròn, theo thứ tự từ điển (`(` đứng trước `)`).

Gợi ý: chỉ đặt `(` khi số ngoặc mở < n; chỉ đặt `)` khi số ngoặc đóng < số ngoặc mở.
""", "Một số `n` (1 ≤ n ≤ 10).", "Mỗi dòng một dãy ngoặc.", ["3\n"], _small(1, 10),
    lambda s: _brackets(int(s)), tags=["quay lui"])


# 14 ----------------------------------------------------------------------
def _parts(n):
    out = []

    def go(rem, mx, cur):
        if rem == 0:
            out.append(" ".join(map(str, cur))); return
        for v in range(min(rem, mx), 0, -1):
            cur.append(v); go(rem - v, v, cur); cur.pop()
    go(n, n, [])
    return out


add(T, "Phân tích số thành tổng", 3, """
Liệt kê mọi cách viết `n` thành tổng các số nguyên dương, mỗi cách viết các số hạng **không tăng**.
Thứ tự in: thứ tự từ điển **giảm dần** (cách đầu tiên là `n`, cách cuối cùng là `1 1 ... 1`).

Ví dụ `n = 4`: `4`, `3 1`, `2 2`, `2 1 1`, `1 1 1 1`.
""", "Một số `n` (1 ≤ n ≤ 25).", "Mỗi dòng một cách phân tích.", ["4\n"], _small(1, 25),
    lambda s: _parts(int(s)), tags=["quay lui"])


# 15 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); o = 0
    for x in rd.ints(n):
        o |= x
    return o % MOD * pow(2, n - 1, MOD) % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); tot = 0
    for m in range(1 << n):
        x = 0
        for i in range(n):
            if m >> i & 1:
                x ^= a[i]
        tot += x
    return tot % MOD


add(T, "Tổng XOR của mọi tập con", 3, """
Tính tổng giá trị XOR của tất cả `2^n` tập con của dãy (XOR của tập rỗng là 0), modulo `10^9 + 7`.

Gợi ý: một bit có mặt trong ít nhất một phần tử thì nó bật trong đúng một nửa số tập con. Đáp án = `(OR toàn dãy) · 2^(n-1)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ a_i ≤ 10^9).", "Kết quả modulo 10^9+7.",
    ["3\n1 2 3\n"], lambda r, s: (lambda n: lines(str(n), L(arr(r, n, 0, r.choice([7, 10**9])))))(S(s, 1, 2 * 10**5)),
    _sol, brute=_br, tags=["bitwise", "toán"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = r.choice([7, 255, 2**20 - 1])
    return lines(J(n, r.randint(0, hi)), L(arr(r, n, 0, hi)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); c = Counter(); tot = 0
    for x in rd.ints(n):
        tot += c[x ^ k]; c[x] += 1
    return tot


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] ^ a[j] == k)


add(T, "Cặp có XOR bằng k", 3, """
Đếm số cặp `i < j` mà `a_i xor a_j = k`.

Gợi ý: `a_i xor a_j = k ⇔ a_i = a_j xor k`. Duyệt `j`, đếm số lần `a_j xor k` đã xuất hiện.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 0 ≤ k < 2^20). Dòng sau `n` số (0 ≤ a_i < 2^20).", "Số cặp.",
    ["4 3\n1 2 3 0\n"], _g, _sol, brute=_br, tags=["bitwise", "map"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10)
    w = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = r.randint(1, 1000)
    return lines(str(n), *(L(row) for row in w))


def _sol(s):
    rd = Rd(s); n = rd.int(); w = [rd.ints(n) for _ in range(n)]
    INF = 10**18
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for m in range(1 << n):
        if not m & 1:
            continue
        for u in range(n):
            if dp[m][u] == INF:
                continue
            for v in range(n):
                if not m >> v & 1:
                    nm = m | 1 << v
                    if dp[m][u] + w[u][v] < dp[nm][v]:
                        dp[nm][v] = dp[m][u] + w[u][v]
    full = (1 << n) - 1
    return min(dp[full][u] + w[u][0] for u in range(1, n))


def _br(s):
    rd = Rd(s); n = rd.int(); w = [rd.ints(n) for _ in range(n)]
    best = 10**18
    for p in permutations(range(1, n)):
        path = (0,) + p + (0,)
        best = min(best, sum(w[path[i]][path[i + 1]] for i in range(n)))
    return best


add(T, "Người du lịch", 4, """
Có `n` thành phố, chi phí đi giữa thành phố `i` và `j` là `c[i][j]`. Xuất phát từ thành phố 1, đi qua mỗi thành phố
đúng một lần rồi quay về thành phố 1. Tìm tổng chi phí nhỏ nhất.

Gợi ý: quay lui thử mọi thứ tự, kèm **nhánh cận**: nếu chi phí hiện tại + (số bước còn lại × cạnh nhỏ nhất) ≥ kết quả tốt nhất thì cắt.
""", "Dòng đầu `n` (2 ≤ n ≤ 10). `n` dòng sau là ma trận chi phí đối xứng (`c[i][i] = 0`, 1 ≤ c ≤ 1000).", "Chi phí nhỏ nhất.",
    ["4\n0 20 35 10\n20 0 15 25\n35 15 0 30\n10 25 30 0\n"], _g, _sol, brute=_br, tags=["quay lui", "nhánh cận"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 20)
    items = [J(r.randint(1, 10**9), r.randint(1, 10**9)) for _ in range(n)]
    return lines(J(n, r.randint(1, 10**9 * max(1, n // 2))), *items)


def _sol(s):
    rd = Rd(s); n, W = rd.ints(2)
    it = [rd.ints(2) for _ in range(n)]
    ws, vs = [0], [0]
    for w, v in it:
        ws += [x + w for x in ws]; vs += [x + v for x in vs]
    return max(v for w, v in zip(ws, vs) if w <= W)


add(T, "Cái túi với n nhỏ", 4, """
Có `n` đồ vật, vật `i` nặng `w_i` và có giá trị `v_i`. Chọn một tập vật có tổng khối lượng ≤ W và tổng giá trị lớn nhất.
Lưu ý khối lượng rất lớn nên không dùng được quy hoạch động theo khối lượng — nhưng `n` nhỏ.

Gợi ý: duyệt mọi tập con bằng quay lui hoặc bitmask `0..2^n - 1`.
""", "Dòng đầu `n, W` (1 ≤ n ≤ 20, 1 ≤ W ≤ 10^10). `n` dòng sau mỗi dòng `w_i v_i` (1 ≤ w_i, v_i ≤ 10^9).",
    "Giá trị lớn nhất.", ["3 10\n5 10\n4 40\n6 30\n"], _g, _sol, tags=["bitmask", "quay lui"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 40)
    a = arr(r, n, 1, r.choice([3, 10, 10**9]))
    x = sum(r.sample(a, r.randint(0, n))) if r.random() < .7 else r.randint(1, sum(a))
    return lines(J(n, x), L(a))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    left = Counter(_subset_sums(a[:n // 2]))
    return sum(left[x - v] for v in _subset_sums(a[n // 2:]) if x - v in left)


add(T, "Gặp nhau ở giữa", 4, """
Cho `n ≤ 40` số nguyên dương. Đếm số tập con có tổng đúng bằng `x`. (`2^40` quá lớn để duyệt hết!)

Gợi ý (meet in the middle): chia dãy làm hai nửa, liệt kê `2^20` tổng tập con của mỗi nửa. Với mỗi tổng `v` của nửa phải,
đếm số tổng bằng `x - v` ở nửa trái (sắp xếp + tìm kiếm nhị phân, hoặc hai con trỏ).
""", "Dòng đầu `n, x` (1 ≤ n ≤ 40, 1 ≤ x ≤ 10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số tập con.",
    ["4 5\n1 2 3 2\n"], _g, _sol, brute=lambda s: _sol(s) if int(s.split()[0]) > 20 else
    (lambda rd: (lambda n, x: _subset_sums(rd.ints(n)).count(x))(*rd.ints(2)))(Rd(s)),
    tags=["meet in the middle"], tl=2000)


# 20 ----------------------------------------------------------------------
def _cntk(n, k):
    """Số x trong [1, n] có đúng k bit 1."""
    res, ones = 0, 0
    for b in range(60, -1, -1):
        if n >> b & 1:
            if k - ones >= 0:
                res += comb(b, k - ones)
            ones += 1
    if bin(n).count("1") == k:
        res += 1
    if k == 0:
        res -= 1  # bỏ số 0
    return res


def _g(r, s):
    q = S(s, 1, 10**4)
    return lines(str(q), *(J(r.randint(1, S(s, 50, 10**18)), r.randint(0, 60)) for _ in range(q)))


add(T, "Đếm số có k bit 1", 4, """
Với mỗi truy vấn `(n, k)`, đếm số số nguyên `x ∈ [1, n]` có đúng `k` bit 1 trong biểu diễn nhị phân.

Gợi ý: duyệt các bit của `n` từ cao xuống thấp; khi gặp bit 1 tại vị trí `b`, nếu đặt bit đó bằng 0 thì `b` bit thấp hơn
được chọn tự do → cộng `C(b, k - số bit 1 đã gặp)`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^4). `Q` dòng sau mỗi dòng `n k` (1 ≤ n ≤ 10^18, 0 ≤ k ≤ 60).", "Mỗi truy vấn in một dòng.",
    ["3\n10 2\n7 3\n5 0\n"], _g,
    lambda s: (lambda rd: [_cntk(*rd.ints(2)) for _ in range(rd.int())])(Rd(s)),
    brute=lambda s: (lambda rd: [(lambda n, k: sum(1 for x in range(1, min(n, 3000) + 1) if bin(x).count("1") == k))(*rd.ints(2))
                                 for _ in range(rd.int())])(Rd(s)) if all(int(v) <= 3000 for v in s.split()[1::2]) else
    (lambda rd: [_cntk(*rd.ints(2)) for _ in range(rd.int())])(Rd(s)),
    tags=["bitwise", "tổ hợp"])


# 21 ----------------------------------------------------------------------
B21 = 16


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    f = [0] * (1 << B21)
    for x in a:
        f[x] += 1
    g = f[:]
    for b in range(B21):
        bit = 1 << b
        for m in range(1 << B21):
            if m & bit:
                g[m] += g[m ^ bit]
    full = (1 << B21) - 1
    tot = sum(f[x] * g[full ^ x] for x in range(1 << B21) if f[x])
    tot -= f[0]  # cặp (0, 0) với chính nó
    return tot // 2


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] & a[j] == 0)


def _g(r, s):
    n = S(s, 2, 10**5)
    mode = r.random()
    if mode < .5:
        a = [r.getrandbits(16) & r.getrandbits(16) & r.getrandbits(16) for _ in range(n)]
    else:
        a = arr(r, n, 0, (1 << B21) - 1)
    return lines(str(n), L(a))


add(T, "Cặp có AND bằng 0", 5, """
Đếm số cặp `i < j` mà `a_i AND a_j = 0`.

Gợi ý (SOS DP - tổng trên tập con): gọi `g[m]` = số phần tử là **tập con** của mặt nạ `m`. Tính `g` trong `O(16 · 2^16)`.
`a_j` thoả mãn với `a_i` khi `a_j` là tập con của phần bù của `a_i`. Nhớ trừ trường hợp `i = j` và chia 2.
""", "Dòng đầu `n` (2 ≤ n ≤ 10^5). Dòng sau `n` số (0 ≤ a_i < 2^16).", "Số cặp.",
    ["4\n1 2 3 4\n"], _g, _sol, brute=_br, tags=["bitmask", "SOS DP"])


# 22 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); tot = 0
    for b in range(31):
        c = sum(x >> b & 1 for x in a)
        tot += c * (c - 1) // 2 << b
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(a[i] & a[j] for i in range(n) for j in range(i + 1, n))


add(T, "Tổng AND của mọi cặp", 3, """
Tính `Σ_{i<j} (a_i AND a_j)`.

Gợi ý: xét riêng từng bit `b`: nếu có `c` số bật bit `b` thì bit đó đóng góp `C(c, 2) · 2^b`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ a_i ≤ 10^9).", "Kết quả (vừa `long long`).",
    ["3\n5 3 7\n"], lambda r, s: (lambda n: lines(str(n), L(arr(r, n, 0, 10**9))))(S(s, 1, 2 * 10**5)), _sol,
    brute=_br, tags=["bitwise"])
