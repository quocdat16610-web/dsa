"""Chuyên đề 7: Đệ quy có nhớ, Quy hoạch động cơ bản."""
from bisect import bisect_right
from .base import add, Rd, S, J, L, arr, lines, rtree

T = 7
MOD = 10**9 + 7


# 1 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % MOD
    return a


add(T, "Số Fibonacci", 1, """
Dãy Fibonacci: `F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)`. Tính `F(n) mod (10^9 + 7)`.

Gợi ý: đệ quy thuần tuý gọi lại cùng một `F(k)` rất nhiều lần (độ phức tạp mũ). Hãy **ghi nhớ** kết quả (memoization)
hoặc tính từ dưới lên bằng vòng lặp — `O(n)`.
""", "Một số `n` (0 ≤ n ≤ 10^6).", "`F(n) mod 10^9+7`.", ["10\n", "0\n"],
    lambda r, s: str(r.randint(0, S(s, 2, 10**6))), _sol, tags=["QHĐ", "đệ quy có nhớ"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    n, k = map(int, s.split())
    dp = [0] * (n + 1); dp[0] = 1; win = 1
    for i in range(1, n + 1):
        dp[i] = win % MOD
        win += dp[i]
        if i - k >= 0:
            win -= dp[i - k]
    return dp[n]


def _br(s):
    n, k = map(int, s.split())
    dp = [1] + [0] * n
    for i in range(1, n + 1):
        dp[i] = sum(dp[max(0, i - k):i]) % MOD
    return dp[n]


add(T, "Leo cầu thang", 1, """
Cầu thang có `n` bậc. Mỗi bước bạn leo được từ 1 đến `k` bậc. Có bao nhiêu cách leo lên đúng bậc thứ `n`? (modulo `10^9 + 7`)

Gợi ý: `dp[i] = dp[i-1] + dp[i-2] + ... + dp[i-k]`, `dp[0] = 1`. Với `k` lớn, giữ tổng trượt để mỗi bước `O(1)`.
""", "Một dòng `n, k` (1 ≤ n ≤ 10^6, 1 ≤ k ≤ n).", "Số cách modulo 10^9+7.", ["4 2\n", "5 3\n"],
    lambda r, s: (lambda n: J(n, r.randint(1, n)))(S(s, 1, 10**6)), _sol, brute=_br, tags=["QHĐ"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5)
    return lines(str(n), L(arr(r, n, 1, 10**4)))


def _sol(s):
    rd = Rd(s); n = rd.int(); h = rd.ints(n)
    dp = [0] * n
    dp[1] = abs(h[1] - h[0])
    for i in range(2, n):
        dp[i] = min(dp[i - 1] + abs(h[i] - h[i - 1]), dp[i - 2] + abs(h[i] - h[i - 2]))
    return dp[-1]


add(T, "Ếch nhảy", 1, """
Có `n` hòn đá, hòn thứ `i` cao `h_i`. Chú ếch ở hòn 1, mỗi lần nhảy từ hòn `i` sang hòn `i+1` hoặc `i+2`,
tốn chi phí `|h_i - h_j|`. Tìm tổng chi phí nhỏ nhất để tới hòn `n`.

Gợi ý: `dp[i] = min(dp[i-1] + |h_i - h_{i-1}|, dp[i-2] + |h_i - h_{i-2}|)`.
""", "Dòng đầu `n` (2 ≤ n ≤ 10^5). Dòng sau `n` số (1 ≤ h_i ≤ 10^4).", "Chi phí nhỏ nhất.",
    ["4\n10 30 40 20\n"], _g, _sol, tags=["QHĐ"])


# 4 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**4)
    return lines(J(n, r.randint(1, 100)), L(arr(r, n, 1, 10**4)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); h = rd.ints(n)
    dp = [0] * n
    for i in range(1, n):
        hi = h[i]
        dp[i] = min(dp[j] + abs(hi - h[j]) for j in range(max(0, i - k), i))
    return dp[-1]


add(T, "Ếch nhảy xa", 1, """
Giống bài "Ếch nhảy" nhưng mỗi lần ếch có thể nhảy từ hòn `i` tới bất kỳ hòn `j` với `i < j ≤ i + k`.

Gợi ý: `dp[i] = min_{i-k ≤ j < i} (dp[j] + |h_i - h_j|)` — độ phức tạp `O(n·k)`.
""", "Dòng đầu `n, k` (2 ≤ n ≤ 2·10^4, 1 ≤ k ≤ 100). Dòng sau `n` số (1 ≤ h_i ≤ 10^4).", "Chi phí nhỏ nhất.",
    ["5 3\n10 30 40 50 20\n"], _g, _sol, tags=["QHĐ"])


# 5 -----------------------------------------------------------------------
def _gc(r, s):
    n = S(s, 1, 30)
    return lines(J(n, r.randint(1, S(s, 20, 10**5))), L(r.sample(range(1, S(s, 20, 10**5) + 1), n)))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); c = rd.ints(n)
    INF = 10**9
    dp = [0] + [INF] * x
    for v in range(1, x + 1):
        best = INF
        for ci in c:
            if ci <= v and dp[v - ci] + 1 < best:
                best = dp[v - ci] + 1
        dp[v] = best
    return dp[x] if dp[x] < INF else -1


add(T, "Đổi tiền ít đồng xu nhất", 2, """
Có `n` loại đồng xu mệnh giá `c_1..c_n` (mỗi loại dùng không giới hạn). Cần dùng ít đồng xu nhất để được tổng đúng `x`.
In số đồng xu ít nhất, hoặc `-1` nếu không thể.

Gợi ý: `dp[v] = 1 + min(dp[v - c_i])`. Lưu ý tham lam (lấy đồng lớn nhất trước) **không** đúng với mọi bộ mệnh giá!
""", "Dòng đầu `n, x` (1 ≤ n ≤ 30, 1 ≤ x ≤ 10^5). Dòng sau `n` mệnh giá phân biệt (1 ≤ c_i ≤ 10^5).", "Số đồng xu ít nhất hoặc `-1`.",
    ["3 11\n1 5 7\n", "1 3\n2\n"], _gc, _sol, tags=["QHĐ", "đổi tiền"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    dp = [1] + [0] * n
    for i in range(1, n + 1):
        dp[i] = sum(dp[max(0, i - 6):i]) % MOD
    return dp[n]


add(T, "Tung xúc xắc", 2, """
Đếm số cách tạo ra tổng `n` bằng cách tung xúc xắc (mặt 1..6) một hoặc nhiều lần; thứ tự các lần tung có ý nghĩa.
Ví dụ `n = 3` có 4 cách: `1+1+1, 1+2, 2+1, 3`. In kết quả modulo `10^9 + 7`.
""", "Một số `n` (1 ≤ n ≤ 10^6).", "Số cách modulo 10^9+7.", ["3\n", "7\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 10**6))), _sol, tags=["QHĐ", "đếm"])


# 7 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); c = rd.ints(n)
    dp = [1] + [0] * x
    for v in range(1, x + 1):
        t = 0
        for ci in c:
            if ci <= v:
                t += dp[v - ci]
        dp[v] = t % MOD
    return dp[x]


add(T, "Đếm cách đổi tiền (có thứ tự)", 2, """
Có `n` loại đồng xu. Đếm số **dãy** đồng xu (thứ tự có ý nghĩa) có tổng bằng `x`, modulo `10^9 + 7`.
Ví dụ mệnh giá `{2, 3, 5}`, `x = 9` có 8 cách như `2+2+5`, `2+5+2`, `5+2+2`, `3+3+3`, ...

Gợi ý: vòng ngoài duyệt tổng `v`, vòng trong duyệt đồng xu: `dp[v] = Σ dp[v - c_i]`.
""", "Dòng đầu `n, x` (1 ≤ n ≤ 30, 1 ≤ x ≤ 10^5). Dòng sau `n` mệnh giá phân biệt.", "Số cách modulo 10^9+7.",
    ["3 9\n2 3 5\n"], _gc, _sol, tags=["QHĐ", "đổi tiền"])


# 8 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); c = rd.ints(n)
    dp = [1] + [0] * x
    for ci in c:
        for v in range(ci, x + 1):
            dp[v] = (dp[v] + dp[v - ci]) % MOD
    return dp[x]


add(T, "Đếm cách đổi tiền (không thứ tự)", 2, """
Giống bài trước nhưng chỉ đếm số **tập hợp** (thứ tự không quan trọng): `2+2+5` và `5+2+2` tính là một cách.

Gợi ý: đổi thứ tự hai vòng lặp — vòng ngoài duyệt đồng xu, vòng trong duyệt tổng.
""", "Dòng đầu `n, x` (1 ≤ n ≤ 30, 1 ≤ x ≤ 10^5). Dòng sau `n` mệnh giá phân biệt.", "Số cách modulo 10^9+7.",
    ["3 9\n2 3 5\n"], _gc, _sol, tags=["QHĐ", "đổi tiền"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    n = int(s)
    dp = [0] * (n + 1)
    for v in range(1, n + 1):
        best, t = 10**9, v
        while t:
            d = t % 10; t //= 10
            if d and dp[v - d] < best:
                best = dp[v - d]
        dp[v] = best + 1
    return dp[n]


add(T, "Bớt chữ số", 2, """
Cho số `n`. Mỗi bước bạn trừ `n` đi một chữ số (khác 0) có mặt trong `n`. Cần ít nhất bao nhiêu bước để `n` về 0?
Ví dụ `27 → 20 → 18 → 10 → 9 → 0` (5 bước).
""", "Một số `n` (1 ≤ n ≤ 10^6).", "Số bước ít nhất.", ["27\n"],
    lambda r, s: str(r.randint(1, S(s, 1, 10**6))), _sol, tags=["QHĐ"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    return lines(str(n), *(L(arr(r, 3, 1, 10**4)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int()
    a = b = c = 0
    for _ in range(n):
        x, y, z = rd.ints(3)
        a, b, c = max(b, c) + x, max(a, c) + y, max(a, b) + z
    return max(a, b, c)


add(T, "Kỳ nghỉ hè", 2, """
Kỳ nghỉ kéo dài `n` ngày. Mỗi ngày bạn chọn một trong ba hoạt động: bơi (A), leo núi (B), làm bài tập (C),
đem lại độ vui `a_i, b_i, c_i`. Không được làm cùng một hoạt động hai ngày liên tiếp. Tìm tổng độ vui lớn nhất.

Gợi ý: `dp[i][j]` = độ vui lớn nhất sau `i` ngày nếu ngày `i` làm hoạt động `j`.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau mỗi dòng `a_i b_i c_i` (1 ≤ giá trị ≤ 10^4).", "Tổng độ vui lớn nhất.",
    ["3\n10 40 70\n20 50 80\n30 60 90\n"], _g, _sol, tags=["QHĐ"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 1000), S(s, 1, 1000)
    return lines(J(n, m), *(L(arr(r, m, 0, 10**6)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    prev = None
    for i in range(n):
        row = rd.ints(m); cur = [0] * m
        for j in range(m):
            best = max(prev[j] if prev else 0, cur[j - 1] if j else 0) if (prev or j) else 0
            cur[j] = best + row[j]
        prev = cur
    return prev[-1]


add(T, "Đường đi nhiều tiền nhất", 3, """
Robot đi từ ô `(1, 1)` tới ô `(n, m)` của bảng, mỗi bước chỉ sang phải hoặc xuống dưới, và nhặt tiền ở mọi ô đi qua.
Tìm tổng tiền lớn nhất nhặt được.

Gợi ý: `dp[i][j] = a[i][j] + max(dp[i-1][j], dp[i][j-1])`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 1000). `n` dòng sau mỗi dòng `m` số (0 ≤ a ≤ 10^6).", "Tổng tiền lớn nhất.",
    ["3 3\n1 3 1\n1 5 1\n4 2 1\n"], _g, _sol, tags=["QHĐ", "lưới"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 1000)
    p = r.choice([0, .05, .2, .35])
    g = [["*" if r.random() < p else "." for _ in range(n)] for _ in range(n)]
    return lines(str(n), *("".join(row) for row in g))


def _sol(s):
    rd = Rd(s); n = rd.int(); g = rd.strs(n)
    prev = [0] * n
    for i in range(n):
        cur = [0] * n
        for j in range(n):
            if g[i][j] == "*":
                continue
            if i == 0 and j == 0:
                cur[j] = 1
            else:
                cur[j] = (prev[j] + (cur[j - 1] if j else 0)) % MOD
        prev = cur
    return prev[-1]


add(T, "Đếm đường đi trên lưới", 3, """
Lưới `n × n` có một số ô bẫy `*`. Đếm số đường đi từ góc trên trái tới góc dưới phải, chỉ đi sang phải hoặc xuống dưới
và không đi vào ô bẫy. In kết quả modulo `10^9 + 7`.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). `n` dòng sau mỗi dòng `n` ký tự `.` hoặc `*`.", "Số đường đi modulo 10^9+7.",
    ["4\n....\n.*..\n...*\n*...\n"], _g, _sol, tags=["QHĐ", "lưới", "đếm"])


# 13 ----------------------------------------------------------------------
def _sol(s):
    a, b = map(int, s.split())
    INF = 10**9
    dp = [[0] * (b + 1) for _ in range(a + 1)]
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            if i == j:
                continue
            best = INF
            for k in range(1, i // 2 + 1):
                v = dp[k][j] + dp[i - k][j]
                if v < best:
                    best = v
            for k in range(1, j // 2 + 1):
                v = dp[i][k] + dp[i][j - k]
                if v < best:
                    best = v
            dp[i][j] = best + 1
    return dp[a][b]


add(T, "Cắt hình chữ nhật", 3, """
Cho hình chữ nhật `a × b`. Mỗi lần cắt bạn chọn một hình chữ nhật và cắt thẳng (dọc hoặc ngang) thành hai hình chữ nhật
có cạnh nguyên. Cần ít nhất bao nhiêu lần cắt để mọi mảnh đều là hình vuông?

Gợi ý: `dp[i][j]` = số lần cắt ít nhất cho hình `i × j`; thử mọi đường cắt. Độ phức tạp `O(a·b·(a+b))`.
""", "Một dòng `a, b` (1 ≤ a, b ≤ 100).", "Số lần cắt ít nhất.", ["3 5\n"],
    lambda r, s: J(r.randint(1, S(s, 1, 100)), r.randint(1, S(s, 1, 100))) if s < 1 else "100 99",
    _sol, tags=["QHĐ"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 0, 10**9)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    take = skip = 0
    for x in a:
        take, skip = skip + x, max(take, skip)
    return max(take, skip)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); best = 0
    for m in range(1 << n):
        if m & (m >> 1) == 0:
            best = max(best, sum(a[i] for i in range(n) if m >> i & 1))
    return best


add(T, "Trộm nhà", 3, """
Có `n` ngôi nhà trên một con phố, nhà `i` có `a_i` đồng. Không được lấy tiền ở hai nhà **kề nhau**. Lấy được nhiều nhất bao nhiêu?

Gợi ý: `dp[i] = max(dp[i-1], dp[i-2] + a_i)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ a_i ≤ 10^9).", "Tổng lớn nhất.",
    ["5\n2 7 9 3 1\n"], _g, _sol, brute=_br, tags=["QHĐ"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 1000)
    return lines(str(n), *(L(arr(r, i + 1, 0, 10**6)) for i in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int()
    rows = [rd.ints(i + 1) for i in range(n)]
    dp = rows[-1][:]
    for i in range(n - 2, -1, -1):
        dp = [rows[i][j] + max(dp[j], dp[j + 1]) for j in range(i + 1)]
    return dp[0]


add(T, "Tam giác số", 3, """
Tam giác số có `n` hàng, hàng `i` có `i` số. Đi từ đỉnh xuống đáy, mỗi bước xuống ô ngay dưới hoặc ô dưới bên phải.
Tìm tổng lớn nhất trên đường đi.

Gợi ý: tính từ đáy lên: `dp[i][j] = a[i][j] + max(dp[i+1][j], dp[i+1][j+1])`.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). Hàng thứ `i` trong `n` dòng sau gồm `i` số (0 ≤ a ≤ 10^6).", "Tổng lớn nhất.",
    ["4\n3\n7 4\n2 4 6\n8 5 9 3\n"], _g, _sol, tags=["QHĐ"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 100)
    return lines(str(n), L(arr(r, n, 1, S(s, 5, 1000))))


def _sol(s):
    rd = Rd(s); n = rd.int(); bits = 1
    for x in rd.ints(n):
        bits |= bits << x
    sums = [i for i in range(1, bits.bit_length()) if bits >> i & 1]
    return lines(str(len(sums)), L(sums))


add(T, "Các tổng có thể tạo", 3, """
Có `n` đồng xu (mỗi đồng dùng tối đa một lần) với mệnh giá `x_i`. Liệt kê tất cả tổng dương có thể tạo được.

Gợi ý: `can[s]` = có tạo được tổng `s` không; với mỗi đồng xu duyệt `s` **giảm dần** để mỗi đồng chỉ dùng một lần.
(Có thể tăng tốc bằng `bitset`: `b |= b << x`.)
""", "Dòng đầu `n` (1 ≤ n ≤ 100). Dòng sau `n` số (1 ≤ x_i ≤ 1000).", "Dòng đầu là số lượng tổng, dòng hai là các tổng tăng dần.",
    ["4\n4 2 5 2\n"], _g, _sol, tags=["QHĐ", "cái túi"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 150)
    return lines(str(n), L(arr(r, n + 1, 1, 100)))


def _sol(s):
    rd = Rd(s); n = rd.int(); d = rd.ints(n + 1)
    dp = [[0] * n for _ in range(n)]
    for ln in range(2, n + 1):
        for i in range(n - ln + 1):
            j = i + ln - 1
            dj1 = d[j + 1]; di = d[i]
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] + di * d[k + 1] * dj1 for k in range(i, j))
    return dp[0][n - 1]


add(T, "Nhân dãy ma trận", 4, """
Cần nhân `n` ma trận `M_1 · M_2 · ... · M_n`, ma trận `M_i` có kích thước `d_{i-1} × d_i`. Nhân ma trận `p × q` với `q × r`
tốn `p·q·r` phép nhân. Chọn cách đặt ngoặc để tổng số phép nhân ít nhất.

Gợi ý (QHĐ trên đoạn): `dp[i][j] = min_k (dp[i][k] + dp[k+1][j] + d_{i-1}·d_k·d_j)`, tính theo độ dài đoạn tăng dần.
""", "Dòng đầu `n` (1 ≤ n ≤ 150). Dòng sau `n + 1` số `d_0..d_n` (1 ≤ d_i ≤ 100).", "Số phép nhân ít nhất.",
    ["3\n10 30 5 60\n"], _g, _sol, tags=["QHĐ đoạn"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2000)
    return lines(str(n), L(arr(r, n, -10**9, 10**9)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    # dp[i][j] = (điểm người đi trước) - (điểm người kia) trên đoạn [i, j]
    dp = a[:]
    for ln in range(2, n + 1):
        dp = [max(a[i] - dp[i + 1], a[i + ln - 1] - dp[i]) for i in range(n - ln + 1)]
    return (sum(a) + dp[0]) // 2


add(T, "Trò chơi lấy số", 4, """
Có dãy `n` số. Hai người chơi lần lượt, mỗi lượt lấy số ở **đầu** hoặc **cuối** dãy và cộng vào điểm của mình.
Cả hai chơi tối ưu (mỗi người muốn tối đa điểm của mình). Tính điểm của người đi trước.

Gợi ý: `dp[i][j]` = (điểm người sắp đi) − (điểm người kia) trên đoạn `[i, j]`:
`dp[i][j] = max(a_i - dp[i+1][j], a_j - dp[i][j-1])`. Điểm người đi trước = `(tổng + dp[1][n]) / 2`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2000). Dòng sau `n` số (|a_i| ≤ 10^9).", "Điểm người đi trước.",
    ["4\n4 5 1 3\n"], _g, _sol, tags=["QHĐ đoạn", "trò chơi"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = S(s, 20, 10**9)
    out = []
    for _ in range(n):
        a = r.randint(1, hi); b = min(hi, a + r.randint(0, max(1, hi // r.choice([5, 100, 10000]))))
        out.append(J(a, b, r.randint(1, 10**9)))
    return lines(str(n), *out)


def _sol(s):
    rd = Rd(s); n = rd.int()
    pr = sorted((rd.ints(3) for _ in range(n)), key=lambda x: x[1])
    ends = [p[1] for p in pr]
    dp = [0] * (n + 1)
    for i, (a, b, p) in enumerate(pr):
        j = bisect_right(ends, a - 1, 0, i)
        dp[i + 1] = max(dp[i], dp[j] + p)
    return dp[n]


def _br(s):
    rd = Rd(s); n = rd.int(); pr = [rd.ints(3) for _ in range(n)]
    best = 0
    for m in range(1 << n):
        ch = sorted((pr[i] for i in range(n) if m >> i & 1))
        if all(ch[i][1] < ch[i + 1][0] for i in range(len(ch) - 1)):
            best = max(best, sum(c[2] for c in ch))
    return best


add(T, "Chọn dự án", 4, """
Có `n` dự án, dự án `i` diễn ra từ ngày `a_i` đến ngày `b_i` và có tiền thưởng `p_i`. Bạn chỉ làm được một dự án mỗi ngày
(hai dự án được chọn không được có chung ngày nào). Tìm tổng tiền thưởng lớn nhất.

Gợi ý: sắp xếp theo ngày kết thúc; `dp[i] = max(dp[i-1], dp[j] + p_i)` với `j` là số dự án kết thúc trước ngày `a_i`
(tìm bằng tìm kiếm nhị phân).
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `a b p` (1 ≤ a ≤ b ≤ 10^9, 1 ≤ p ≤ 10^9).", "Tiền thưởng lớn nhất.",
    ["4\n2 4 4\n3 6 6\n6 8 2\n5 7 3\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 12 else _sol(s), tags=["QHĐ", "tìm kiếm nhị phân"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 15)
    return lines(str(n), *(L(arr(r, n, 1, 10**6)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); c = [rd.ints(n) for _ in range(n)]
    INF = 10**18
    dp = [INF] * (1 << n); dp[0] = 0
    for m in range(1 << n):
        if dp[m] == INF:
            continue
        i = bin(m).count("1")
        if i == n:
            continue
        row = c[i]
        for j in range(n):
            if not m >> j & 1:
                v = dp[m] + row[j]
                if v < dp[m | 1 << j]:
                    dp[m | 1 << j] = v
    return dp[-1]


def _br(s):
    from itertools import permutations
    rd = Rd(s); n = rd.int(); c = [rd.ints(n) for _ in range(n)]
    return min(sum(c[i][p[i]] for i in range(n)) for p in permutations(range(n)))


add(T, "Phân công công việc", 4, """
Có `n` người và `n` công việc; người `i` làm việc `j` tốn chi phí `c[i][j]`. Mỗi người làm đúng một việc, mỗi việc do đúng
một người làm. Tìm tổng chi phí nhỏ nhất.

Gợi ý (QHĐ bitmask): `dp[mask]` = chi phí nhỏ nhất khi `popcount(mask)` người đầu tiên đã nhận các việc trong `mask`.
""", "Dòng đầu `n` (1 ≤ n ≤ 15). `n` dòng sau mỗi dòng `n` số (1 ≤ c ≤ 10^6).", "Chi phí nhỏ nhất.",
    ["3\n9 2 7\n6 4 3\n5 8 1\n"], _g, _sol, brute=_br, tags=["QHĐ bitmask"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 16)
    x = r.randint(10, 10**9)
    return lines(J(n, x), L(arr(r, n, 1, x)))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); w = rd.ints(n)
    best = [(0, 0)] * (1 << n)  # (số chuyến, khối lượng chuyến cuối)
    best[0] = (1, 0)
    for m in range(1, 1 << n):
        cand = (n + 1, 0)
        for i in range(n):
            if m >> i & 1:
                k, last = best[m ^ 1 << i]
                opt = (k, last + w[i]) if last + w[i] <= x else (k + 1, w[i])
                if opt < cand:
                    cand = opt
        best[m] = cand
    return best[-1][0]


def _br(s):
    from itertools import permutations
    rd = Rd(s); n, x = rd.ints(2); w = rd.ints(n)
    bestv = n
    for p in permutations(range(n)):
        k, cur = 1, 0
        for i in p:
            if cur + w[i] <= x:
                cur += w[i]
            else:
                k += 1; cur = w[i]
        bestv = min(bestv, k)
    return bestv


add(T, "Thang máy", 5, """
Có `n` người, người `i` nặng `w_i`; thang máy chở tối đa `x` kg mỗi chuyến. Cần ít nhất bao nhiêu chuyến để chở hết mọi người?

Gợi ý (QHĐ bitmask): `dp[mask]` = cặp (số chuyến ít nhất, khối lượng nhỏ nhất của chuyến cuối) khi đã chở xong tập `mask`.
Chuyển trạng thái bằng cách thêm một người vào chuyến cuối hoặc mở chuyến mới. Độ phức tạp `O(2^n · n)`.
""", "Dòng đầu `n, x` (1 ≤ n ≤ 16, 1 ≤ x ≤ 10^9). Dòng sau `n` số (1 ≤ w_i ≤ x).", "Số chuyến ít nhất.",
    ["4 10\n4 8 6 1\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 7 else _sol(s),
    tags=["QHĐ bitmask"], tl=1500)


# 22 ----------------------------------------------------------------------
def _g(r, s):
    n, k = S(s, 1, 10**5), r.randint(2, 20)
    if s >= 1:
        k = 20
    return lines(J(n, k), *(L(arr(r, k, 1, 10**4)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2)
    prev = [0] * k
    for _ in range(n):
        c = rd.ints(k)
        order = sorted(range(k), key=lambda j: prev[j])
        b1, b2 = order[0], order[1]
        prev = [c[j] + (prev[b2] if j == b1 else prev[b1]) for j in range(k)]
    return min(prev)


def _br(s):
    rd = Rd(s); n, k = rd.ints(2)
    prev = [0] * k
    for _ in range(n):
        c = rd.ints(k)
        prev = [c[j] + min(prev[t] for t in range(k) if t != j) for j in range(k)]
    return min(prev)


add(T, "Sơn nhà", 4, """
Có `n` ngôi nhà thẳng hàng và `k` màu sơn; sơn nhà `i` bằng màu `j` tốn `c[i][j]`. Hai nhà kề nhau phải khác màu.
Tìm tổng chi phí nhỏ nhất.

Gợi ý: `dp[i][j] = c[i][j] + min_{t ≠ j} dp[i-1][t]`. Để mỗi bước `O(k)` thay vì `O(k²)`, chỉ cần nhớ giá trị nhỏ nhất
và nhỏ nhì của hàng trước.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 10^5, 2 ≤ k ≤ 20). `n` dòng sau mỗi dòng `k` số (1 ≤ c ≤ 10^4).", "Chi phí nhỏ nhất.",
    ["3 3\n1 5 3\n2 9 4\n5 1 1\n"], _g, _sol, brute=_br, tags=["QHĐ"])


# 23 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, 10**9)), *(J(a, b) for a, b in rtree(r, n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); w = rd.ints(n)
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = rd.ints(2); adj[a - 1].append(b - 1); adj[b - 1].append(a - 1)
    par = [-1] * n; order = [0]; seen = [False] * n; seen[0] = True
    for u in order:
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True; par[v] = u; order.append(v)
    take = w[:]; skip = [0] * n
    for u in reversed(order):
        p = par[u]
        if p >= 0:
            take[p] += skip[u]; skip[p] += max(take[u], skip[u])
    return max(take[0], skip[0])


def _br(s):
    rd = Rd(s); n = rd.int(); w = rd.ints(n)
    es = [rd.ints(2) for _ in range(n - 1)]
    best = 0
    for m in range(1 << n):
        if all(not (m >> (a - 1) & 1 and m >> (b - 1) & 1) for a, b in es):
            best = max(best, sum(w[i] for i in range(n) if m >> i & 1))
    return best


add(T, "Tập độc lập trên cây", 5, """
Cho cây `n` đỉnh, đỉnh `i` có trọng số `w_i`. Chọn một tập đỉnh sao cho không có hai đỉnh nào kề nhau và tổng trọng số lớn nhất.

Gợi ý (QHĐ trên cây): `take[u] = w_u + Σ skip[con]`, `skip[u] = Σ max(take[con], skip[con])`.
Với `n` lớn nên duyệt bằng BFS/stack thay vì đệ quy để tránh tràn ngăn xếp.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng hai gồm `n` trọng số (1 ≤ w ≤ 10^9). `n - 1` dòng sau là các cạnh.",
    "Tổng trọng số lớn nhất.", ["5\n1 5 3 4 2\n1 2\n1 3\n2 4\n2 5\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 15 else _sol(s), tags=["QHĐ trên cây"])
