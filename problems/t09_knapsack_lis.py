"""Chuyên đề 9: QHĐ cái túi (Knapsack), dãy con tăng dài nhất (LIS), xâu con chung dài nhất (LCS)."""
from bisect import bisect_left, bisect_right
from .base import add, Rd, S, J, L, arr, lines, rstr

T = 9
MOD = 10**9 + 7


def _items(r, s, n_hi, w_hi, v_hi):
    n = S(s, 1, n_hi)
    return n, [(r.randint(1, w_hi), r.randint(1, v_hi)) for _ in range(n)]


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, it = _items(r, s, 100, S(s, 10, 10**4), 10**9)
    return lines(J(n, r.randint(1, S(s, 10, 10**4))), *(J(w, v) for w, v in it))


def _sol(s):
    rd = Rd(s); n, W = rd.ints(2)
    dp = [0] * (W + 1)
    for _ in range(n):
        w, v = rd.ints(2)
        if w <= W:
            dp = dp[:w] + [max(a, b + v) for a, b in zip(dp[w:], dp)]
    return dp[W]


def _br(s):
    rd = Rd(s); n, W = rd.ints(2); it = [rd.ints(2) for _ in range(n)]
    best = 0
    for m in range(1 << n):
        if sum(it[i][0] for i in range(n) if m >> i & 1) <= W:
            best = max(best, sum(it[i][1] for i in range(n) if m >> i & 1))
    return best


add(T, "Cái túi 0/1", 1, """
Có `n` đồ vật, vật `i` nặng `w_i` và có giá trị `v_i`. Túi chịu được tổng khối lượng `W`. Mỗi vật lấy tối đa một lần.
Tìm tổng giá trị lớn nhất.

Gợi ý: `dp[j]` = giá trị lớn nhất với tổng khối lượng ≤ j. Với mỗi vật duyệt `j` **giảm dần**:
`dp[j] = max(dp[j], dp[j - w] + v)`.
""", "Dòng đầu `n, W` (1 ≤ n ≤ 100, 1 ≤ W ≤ 10^4). `n` dòng sau mỗi dòng `w v` (1 ≤ w ≤ 10^4, 1 ≤ v ≤ 10^9).",
    "Giá trị lớn nhất.", ["3 8\n3 30\n4 50\n5 60\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 14 else _sol(s), tags=["cái túi"])


# 2 -----------------------------------------------------------------------
def _lis(a, strict=True):
    t = []
    for x in a:
        i = bisect_left(t, x) if strict else bisect_right(t, x)
        if i == len(t):
            t.append(x)
        else:
            t[i] = x
    return len(t)


def _g(r, s):
    n = S(s, 1, 1000)
    return lines(str(n), L(arr(r, n, 1, r.choice([5, 1000, 10**9]))))


def _br_lis(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


add(T, "Dãy con tăng dài nhất (cơ bản)", 1, """
Tìm độ dài dãy con (không cần liên tiếp) **tăng ngặt** dài nhất.

Gợi ý: `dp[i]` = độ dài LIS kết thúc tại `i` = `1 + max(dp[j])` với `j < i` và `a_j < a_i`. Độ phức tạp `O(n²)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Độ dài LIS.",
    ["6\n5 2 8 6 3 6\n"], _g, lambda s: _lis(list(map(int, s.split()[1:]))), brute=_br_lis, tags=["LIS"])


# 3 -----------------------------------------------------------------------
def _lcs(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0]
        for j, cb in enumerate(b):
            cur.append(prev[j] + 1 if ch == cb else (cur[j] if cur[j] > prev[j + 1] else prev[j + 1]))
        prev = cur
    return prev[-1]


def _g_two_str(r, s):
    al = "abcdefghijklmnopqrstuvwxyz"[:r.choice([2, 4, 26])]
    return lines(rstr(r, S(s, 1, 1000), al), rstr(r, S(s, 1, 1000), al))


add(T, "Xâu con chung dài nhất", 1, """
Cho hai xâu `a` và `b`. Tìm độ dài xâu con chung dài nhất (LCS) — xâu nhận được từ cả `a` và `b` bằng cách xoá bớt ký tự.

Gợi ý: `dp[i][j] = dp[i-1][j-1] + 1` nếu `a_i = b_j`, ngược lại `max(dp[i-1][j], dp[i][j-1])`.
""", "Hai dòng là hai xâu chữ cái thường (độ dài 1..1000).", "Độ dài LCS.", ["abcbdab\nbdcaba\n"],
    _g_two_str, lambda s: _lcs(*s.split()), tags=["LCS"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, W = rd.ints(2)
    it = [rd.ints(2) for _ in range(n)]
    dp = [0] * (W + 1)
    for j in range(1, W + 1):
        best = dp[j - 1]
        for w, v in it:
            if w <= j and dp[j - w] + v > best:
                best = dp[j - w] + v
        dp[j] = best
    return dp[W]


def _g(r, s):
    n, it = _items(r, s, 50, S(s, 10, 10**4), 10**6)
    return lines(J(n, r.randint(1, S(s, 10, 2 * 10**4))), *(J(w, v) for w, v in it))


add(T, "Cái túi không giới hạn", 2, """
Giống bài cái túi 0/1, nhưng mỗi loại đồ vật được lấy **bao nhiêu lần cũng được**.

Gợi ý: duyệt `j` **tăng dần** (để vật vừa lấy có thể được lấy tiếp).
""", "Dòng đầu `n, W` (1 ≤ n ≤ 50, 1 ≤ W ≤ 2·10^4). `n` dòng sau mỗi dòng `w v` (1 ≤ w ≤ 10^4, 1 ≤ v ≤ 10^6).",
    "Giá trị lớn nhất.", ["2 10\n3 4\n4 6\n"], _g, _sol, tags=["cái túi"])


# 5 -----------------------------------------------------------------------
def _g(r, s):
    n, it = _items(r, s, 100, 10**9, 100)
    return lines(J(n, r.randint(1, 10**9 * max(1, n // 3))), *(J(w, v) for w, v in it))


def _sol(s):
    rd = Rd(s); n, W = rd.ints(2); it = [rd.ints(2) for _ in range(n)]
    V = sum(v for _, v in it)
    INF = 10**19
    dp = [0] + [INF] * V  # dp[v] = khối lượng nhỏ nhất để đạt giá trị v
    for w, v in it:
        dp = dp[:v] + [min(a, b + w) for a, b in zip(dp[v:], dp)]
    return max(v for v in range(V + 1) if dp[v] <= W)


add(T, "Cái túi với khối lượng lớn", 2, """
Cái túi 0/1 nhưng khối lượng rất lớn (`W ≤ 10^9`) còn giá trị nhỏ (`v_i ≤ 100`, `n ≤ 100`).

Gợi ý: đổi vai trò! `dp[v]` = khối lượng **nhỏ nhất** để đạt tổng giá trị đúng `v`. Đáp án là `v` lớn nhất có `dp[v] ≤ W`.
""", "Dòng đầu `n, W` (1 ≤ n ≤ 100, 1 ≤ W ≤ 10^11). `n` dòng sau mỗi dòng `w v` (1 ≤ w ≤ 10^9, 1 ≤ v ≤ 100).",
    "Giá trị lớn nhất.", ["3 8\n3 30\n4 50\n5 60\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 14 else _sol(s), tags=["cái túi"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, r.choice([10, 10**5, 10**9]))
    if r.random() < .3:
        a.sort(reverse=r.random() < .5)
    return lines(str(n), L(a))


add(T, "Dãy con tăng dài nhất (n lớn)", 2, """
Tìm độ dài LIS (tăng ngặt) với `n ≤ 2·10^5`.

Gợi ý: mảng `t[k]` = giá trị cuối **nhỏ nhất** của một dãy con tăng độ dài `k+1`. Với mỗi `x`, thay `t[lower_bound(x)]` bằng `x`
(hoặc thêm vào cuối). Đáp án là kích thước `t`. Độ phức tạp `O(n log n)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Độ dài LIS.",
    ["8\n7 3 5 3 6 2 9 8\n"], _g, lambda s: _lis(list(map(int, s.split()[1:]))), brute=_br_lis, tags=["LIS", "tìm kiếm nhị phân"])


# 7 -----------------------------------------------------------------------
add(T, "Dãy con không giảm dài nhất", 2, """
Tìm độ dài dãy con **không giảm** (cho phép bằng nhau) dài nhất.

Gợi ý: như LIS `O(n log n)` nhưng dùng `upper_bound` thay cho `lower_bound`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Độ dài lớn nhất.",
    ["6\n1 3 3 2 2 2\n"], _g, lambda s: _lis(list(map(int, s.split()[1:])), strict=False), tags=["LIS"])


# 8 -----------------------------------------------------------------------
def _edit(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


add(T, "Khoảng cách chỉnh sửa", 2, """
Khoảng cách chỉnh sửa (Levenshtein) giữa hai xâu là số thao tác ít nhất để biến `a` thành `b`, mỗi thao tác là
**thêm**, **xoá** hoặc **thay** một ký tự.

Gợi ý: `dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (a_i ≠ b_j))`.
""", "Hai dòng là hai xâu chữ cái thường (độ dài 1..1000).", "Khoảng cách chỉnh sửa.", ["love\nmovie\n"],
    _g_two_str, lambda s: _edit(*s.split()), tags=["QHĐ xâu"])


# 9 -----------------------------------------------------------------------
add(T, "Xoá ít nhất để dãy tăng", 2, """
Xoá ít phần tử nhất sao cho dãy còn lại tăng ngặt. In số phần tử cần xoá.

Gợi ý: giữ lại nhiều nhất = LIS.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số phần tử cần xoá.",
    ["5\n1 5 2 3 3\n"], _g, lambda s: int(s.split()[0]) - _lis(list(map(int, s.split()[1:]))), tags=["LIS"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 100)
    return lines(str(n), L(arr(r, n, 1, S(s, 5, 1000))))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); tot = sum(a)
    bits = 1
    for x in a:
        bits |= bits << x
    return min(abs(tot - 2 * v) for v in range(tot + 1) if bits >> v & 1)


add(T, "Chia hai nhóm gần bằng nhau", 2, """
Chia `n` số thành hai nhóm (một nhóm có thể rỗng) sao cho chênh lệch tổng hai nhóm nhỏ nhất. Khác bài "Chia táo" ở chỗ
`n` lớn hơn nhưng giá trị nhỏ.

Gợi ý: cái túi đánh dấu `can[s]` = có tạo được tổng `s` không. Đáp án `min |tổng - 2s|`.
""", "Dòng đầu `n` (1 ≤ n ≤ 100). Dòng sau `n` số (1 ≤ a_i ≤ 1000).", "Chênh lệch nhỏ nhất.",
    ["4\n1 6 11 5\n"], _g, _sol, tags=["cái túi"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 100)
    return lines(J(n, r.randint(1, S(s, 10, 10**4))),
                 *(J(r.randint(1, S(s, 10, 2000)), r.randint(1, 10**6), r.randint(1, 100)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, W = rd.ints(2)
    dp = [0] * (W + 1)
    for _ in range(n):
        w, v, k = rd.ints(3)
        c = 1
        while k > 0:
            t = min(c, k); k -= t; c *= 2
            ww, vv = w * t, v * t
            if ww <= W:
                dp = dp[:ww] + [max(a, b + vv) for a, b in zip(dp[ww:], dp)]
    return dp[W]


def _brb(s):
    rd = Rd(s); n, W = rd.ints(2)
    dp = [0] * (W + 1)
    for _ in range(n):
        w, v, k = rd.ints(3)
        dp = [max(dp[j - c * w] + c * v for c in range(0, min(k, j // w) + 1)) for j in range(W + 1)]
    return dp[W]


add(T, "Cái túi có giới hạn số lượng", 3, """
Có `n` loại đồ vật, loại `i` nặng `w_i`, giá trị `v_i` và có `k_i` cái. Tìm tổng giá trị lớn nhất với tổng khối lượng ≤ W.

Gợi ý (tách nhị phân): tách `k` cái thành các gói `1, 2, 4, ..., còn lại` — mọi số lượng từ 0 đến `k` đều ghép được từ các gói.
Sau đó làm cái túi 0/1 với các gói. Độ phức tạp `O(W · Σ log k_i)`.
""", "Dòng đầu `n, W` (1 ≤ n ≤ 100, 1 ≤ W ≤ 10^4). `n` dòng sau mỗi dòng `w v k` (1 ≤ w ≤ 2000, 1 ≤ v ≤ 10^6, 1 ≤ k ≤ 100).",
    "Giá trị lớn nhất.", ["2 10\n3 5 2\n4 7 3\n"], _g, _sol, brute=_brb, tags=["cái túi"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    return rstr(r, S(s, 1, 1000), "abcdefghijklmnopqrstuvwxyz"[:r.choice([2, 3, 26])])


add(T, "Dãy con đối xứng dài nhất", 3, """
Tìm độ dài dãy con (không cần liên tiếp) dài nhất của xâu `s` mà đọc xuôi hay ngược đều giống nhau.

Gợi ý: chính là LCS của `s` và xâu đảo ngược của `s`. Hoặc QHĐ đoạn: `dp[i][j]`.
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 1000).", "Độ dài lớn nhất.", ["bbbab\n", "abcd\n"], _g,
    lambda s: _lcs(s.split()[0], s.split()[0][::-1]), tags=["LCS", "xâu đối xứng"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 50)
    return lines(J(n, r.randint(1, S(s, 5, 100)), r.randint(1, S(s, 5, 100))),
                 *(J(r.randint(1, 50), r.randint(1, 50), r.randint(1, 10**6)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, W, V = rd.ints(3)
    dp = [[0] * (V + 1) for _ in range(W + 1)]
    for _ in range(n):
        w, vol, val = rd.ints(3)
        for i in range(W, w - 1, -1):
            row, src = dp[i], dp[i - w]
            for j in range(V, vol - 1, -1):
                if src[j - vol] + val > row[j]:
                    row[j] = src[j - vol] + val
    return dp[W][V]


def _br(s):
    rd = Rd(s); n, W, V = rd.ints(3); it = [rd.ints(3) for _ in range(n)]
    best = 0
    for m in range(1 << n):
        ch = [it[i] for i in range(n) if m >> i & 1]
        if sum(c[0] for c in ch) <= W and sum(c[1] for c in ch) <= V:
            best = max(best, sum(c[2] for c in ch))
    return best


add(T, "Cái túi hai ràng buộc", 3, """
Mỗi vật có khối lượng `w_i`, thể tích `u_i` và giá trị `v_i`. Túi chịu được khối lượng ≤ W và thể tích ≤ V. Mỗi vật lấy tối đa một lần.
Tìm tổng giá trị lớn nhất.

Gợi ý: thêm một chiều cho QHĐ: `dp[w][u]`.
""", "Dòng đầu `n, W, V` (1 ≤ n ≤ 50, 1 ≤ W, V ≤ 100). `n` dòng sau mỗi dòng `w u v` (1 ≤ w, u ≤ 50, 1 ≤ v ≤ 10^6).",
    "Giá trị lớn nhất.", ["3 5 5\n2 3 10\n3 2 15\n3 3 12\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 14 else _sol(s), tags=["cái túi"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    al = "abc"[:r.choice([2, 3])] if r.random() < .5 else "abcdefghij"
    return lines(*(rstr(r, S(s, 1, 100), al) for _ in range(3)))


def _sol(s):
    a, b, c = s.split()
    nb, nc = len(b), len(c)
    prev = [[0] * (nc + 1) for _ in range(nb + 1)]
    for ca in a:
        cur = [[0] * (nc + 1) for _ in range(nb + 1)]
        for j in range(1, nb + 1):
            cb = b[j - 1]; cj, pj, cj1, pj1 = cur[j], prev[j], cur[j - 1], prev[j - 1]
            for k in range(1, nc + 1):
                if ca == cb == c[k - 1]:
                    cj[k] = pj1[k - 1] + 1
                else:
                    cj[k] = max(pj[k], cj1[k], cj[k - 1])
        prev = cur
    return prev[nb][nc]


add(T, "LCS của ba xâu", 3, """
Tìm độ dài xâu con chung dài nhất của **ba** xâu.

Gợi ý: `dp[i][j][k]` — mở rộng trực tiếp công thức LCS hai xâu. `O(n³)`.
""", "Ba dòng là ba xâu chữ cái thường (độ dài 1..100).", "Độ dài LCS.", ["abcd\nacbd\nabd\n"], _g, _sol, tags=["LCS"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2000)
    return lines(str(n), L(arr(r, n, 1, r.choice([5, 50, 10**9]))))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    ln = [1] * n; ct = [1] * n
    for i in range(n):
        ai = a[i]; bl, bc = 1, 1
        for j in range(i):
            if a[j] < ai:
                l2 = ln[j] + 1
                if l2 > bl:
                    bl, bc = l2, ct[j]
                elif l2 == bl:
                    bc += ct[j]
        ln[i], ct[i] = bl, bc % MOD
    m = max(ln)
    return sum(ct[i] for i in range(n) if ln[i] == m) % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    best, cnt = 0, 0
    for m in range(1, 1 << n):
        b = [a[i] for i in range(n) if m >> i & 1]
        if all(b[i] < b[i + 1] for i in range(len(b) - 1)):
            if len(b) > best:
                best, cnt = len(b), 1
            elif len(b) == best:
                cnt += 1
    return cnt % MOD


add(T, "Đếm số dãy con tăng dài nhất", 4, """
Đếm số dãy con tăng ngặt có độ dài **bằng** độ dài LIS (hai dãy con khác nhau nếu tập chỉ số khác nhau), modulo `10^9 + 7`.

Gợi ý: song song với `len[i]` (độ dài LIS kết thúc tại `i`), lưu `cnt[i]` = số dãy đạt độ dài đó.
""", "Dòng đầu `n` (1 ≤ n ≤ 2000). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số dãy modulo 10^9+7.",
    ["5\n1 3 5 4 7\n", "4\n2 2 2 2\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 14 else _sol(s), tags=["LIS", "QHĐ đếm"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    a = list(range(1, n + 1)); b = a[:]
    r.shuffle(a)
    if r.random() < .5:
        b = a[:]
        for _ in range(r.randint(1, max(1, n // 10))):
            i, j = r.randrange(n), r.randrange(n); b[i], b[j] = b[j], b[i]
    else:
        r.shuffle(b)
    return lines(str(n), L(a), L(b))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); b = rd.ints(n)
    pos = [0] * (n + 1)
    for i, x in enumerate(a):
        pos[x] = i
    return _lis([pos[x] for x in b])


add(T, "LCS của hai hoán vị", 4, """
Cho hai hoán vị `a`, `b` của `1..n` với `n ≤ 10^5`. Tìm độ dài xâu con chung dài nhất. (QHĐ `O(n²)` quá chậm!)

Gợi ý: đổi mỗi phần tử của `b` thành vị trí của nó trong `a`. Dãy con chung ⇔ dãy con **tăng** của dãy mới → LIS `O(n log n)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). Hai dòng sau là hai hoán vị.", "Độ dài LCS.",
    ["5\n1 2 3 4 5\n3 1 2 5 4\n"], _g, _sol, brute=lambda s: (lambda rd: (lambda n: _lcs(rd.ints(n), rd.ints(n)))(rd.int()))(Rd(s)),
    tags=["LCS", "LIS"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = r.choice([5, 100, 10**9])
    return lines(str(n), *(J(r.randint(1, hi), r.randint(1, hi)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int()
    env = sorted((rd.ints(2) for _ in range(n)), key=lambda e: (e[0], -e[1]))
    return _lis([h for _, h in env])


def _br(s):
    rd = Rd(s); n = rd.int(); env = sorted(tuple(rd.ints(2)) for _ in range(n))
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if env[j][0] < env[i][0] and env[j][1] < env[i][1]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


add(T, "Búp bê Nga", 4, """
Có `n` phong bì, phong bì `i` có kích thước `w_i × h_i`. Phong bì A lồng được vào B nếu `w_A < w_B` **và** `h_A < h_B`
(không xoay). Tìm số phong bì nhiều nhất có thể lồng liên tiếp vào nhau.

Gợi ý: sắp xếp theo `w` tăng dần, **cùng `w` thì `h` giảm dần** (để không chọn hai phong bì cùng `w`), rồi tìm LIS theo `h`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `w h` (1 ≤ w, h ≤ 10^9).", "Số phong bì nhiều nhất.",
    ["4\n5 4\n6 4\n6 7\n2 3\n"], _g, _sol, brute=_br, tags=["LIS", "sắp xếp"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    g = S(s, 1, 50)
    W = r.randint(1, S(s, 10, 10**4))
    out = [J(g, W)]
    for _ in range(g):
        k = r.randint(1, 4)
        out.append(str(k))
        out += [J(r.randint(1, max(1, W // r.choice([1, 3, 10]))), r.randint(1, 10**6)) for _ in range(k)]
    return lines(*out)


def _sol(s):
    rd = Rd(s); g, W = rd.ints(2)
    dp = [0] * (W + 1)
    for _ in range(g):
        k = rd.int(); it = [rd.ints(2) for _ in range(k)]
        nd = dp[:]
        for w, v in it:
            if w <= W:
                cand = dp[:w] + [b + v for b in dp[:W + 1 - w]]
                nd = [max(a, c) if j >= w else a for j, (a, c) in enumerate(zip(nd, cand))]
        dp = nd
    return dp[W]


def _br(s):
    from itertools import product
    rd = Rd(s); g, W = rd.ints(2)
    groups = []
    for _ in range(g):
        k = rd.int(); groups.append([(0, 0)] + [tuple(rd.ints(2)) for _ in range(k)])
    if g > 6:
        return _sol(s)
    return max(sum(v for _, v in ch) for ch in product(*groups) if sum(w for w, _ in ch) <= W)


add(T, "Cái túi theo nhóm", 4, """
Các đồ vật chia thành `g` nhóm; từ mỗi nhóm được chọn **tối đa một** vật. Tổng khối lượng ≤ W, tối đa hoá tổng giá trị.

Gợi ý: với mỗi nhóm, tính `dp` mới từ `dp` cũ (của các nhóm trước) — không cập nhật tại chỗ để tránh chọn hai vật cùng nhóm.
""", "Dòng đầu `g, W` (1 ≤ g ≤ 50, 1 ≤ W ≤ 10^4). Với mỗi nhóm: một dòng `k` (1 ≤ k ≤ 4), sau đó `k` dòng `w v` (1 ≤ w ≤ 10^4, 1 ≤ v ≤ 10^6).",
    "Giá trị lớn nhất.", ["2 5\n2\n2 3\n3 4\n2\n2 5\n4 7\n"], _g, _sol, brute=_br, tags=["cái túi"])


# 19 -----------------------------------------------------------------------
def _g_seq(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, r.choice([5, 10**9]))))


def _br_piles(s):
    """Tham lam trực tiếp: đặt mỗi tên lửa vào hệ thống đầu tiên còn bắn được (độ cao cuối ≥ x)."""
    piles = []
    for x in map(int, s.split()[1:]):
        for i, p in enumerate(piles):
            if p >= x:
                piles[i] = x
                break
        else:
            piles.append(x)
    return len(piles)


add(T, "Phủ bằng dãy không tăng", 4, """
Cần chia dãy thành ít nhất bao nhiêu dãy con **không tăng** (mỗi phần tử thuộc đúng một dãy con, giữ nguyên thứ tự)?

Ví dụ thực tế: các tên lửa bay tới theo thứ tự với độ cao `a_i`; một hệ thống đánh chặn chỉ bắn được độ cao không tăng dần.
Cần ít nhất bao nhiêu hệ thống?

Gợi ý (định lý Dilworth): số dãy không tăng tối thiểu = độ dài dãy con **tăng ngặt** dài nhất.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số dãy tối thiểu.",
    ["8\n389 207 155 300 299 170 158 65\n"], _g_seq, lambda s: _lis(list(map(int, s.split()[1:]))),
    brute=_br_piles, tags=["LIS", "tham lam"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 1000), S(s, 1, 1000)
    hi = r.choice([5, 30, 10**9])
    return lines(J(n, m), L(arr(r, n, 1, hi)), L(arr(r, m, 1, hi)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n); b = rd.ints(m)
    dp = [0] * m  # dp[j] = LCIS kết thúc bằng b_j
    for x in a:
        cur = 0
        for j in range(m):
            if b[j] == x:
                if cur + 1 > dp[j]:
                    dp[j] = cur + 1
            elif b[j] < x and dp[j] > cur:
                cur = dp[j]
    return max(dp + [0])


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n); b = rd.ints(m)
    best = 0
    for mk in range(1 << n):
        c = [a[i] for i in range(n) if mk >> i & 1]
        if all(c[i] < c[i + 1] for i in range(len(c) - 1)):
            it = iter(b)
            if all(any(x == y for y in it) for x in c):
                best = max(best, len(c))
    return best


add(T, "Dãy con chung tăng dài nhất", 5, """
Tìm độ dài dãy dài nhất vừa là dãy con của `a`, vừa là dãy con của `b`, và **tăng ngặt** (LCIS).

Gợi ý: `dp[j]` = độ dài LCIS kết thúc tại `b_j`. Duyệt `a_i`; khi quét `j`, giữ `cur` = max `dp[j']` với `b_{j'} < a_i`;
nếu `b_j = a_i` thì `dp[j] = max(dp[j], cur + 1)`. Độ phức tạp `O(n·m)`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 1000). Hai dòng sau là hai dãy (1 ≤ giá trị ≤ 10^9).", "Độ dài LCIS.",
    ["5 4\n1 4 2 5 3\n4 2 3 5\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 12 else _sol(s), tags=["LIS", "LCS"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 300)
    W = r.randint(1, S(s, 5, 300))
    out = [J(n, W)]
    for i in range(1, n + 1):
        p = 0 if i == 1 or r.random() < .1 else r.randint(1, i - 1)
        out.append(J(p, r.randint(1, max(1, W // 3)), r.randint(1, 10**6)))
    return lines(*out)


def _sol(s):
    rd = Rd(s); n, W = rd.ints(2)
    par, w, v = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    ch = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        par[i], w[i], v[i] = rd.ints(3); ch[par[i]].append(i)
    # duyệt DFS tiền thứ tự từ gốc ảo 0; sz = kích thước cây con
    order, stack = [], [0]
    while stack:
        u = stack.pop(); order.append(u)
        stack.extend(reversed(ch[u]))
    pos = {u: i for i, u in enumerate(order)}
    sz = [1] * (n + 1)
    for u in reversed(order):
        if u:
            sz[par[u]] += sz[u]
    m = len(order)
    NEG = -1
    # f[i][c] = giá trị lớn nhất khi xét các đỉnh order[i..m-1] với tổng khối lượng c
    f = [[0] * (W + 1) for _ in range(m + 1)]
    for i in range(m - 1, 0, -1):
        u = order[i]
        skip = f[i + sz[u]]
        take = f[i + 1]
        wu, vu = w[u], v[u]
        row = skip[:]
        for c in range(wu, W + 1):
            val = take[c - wu] + vu
            if val > row[c]:
                row[c] = val
        f[i] = row
    return f[1][W]


def _br(s):
    rd = Rd(s); n, W = rd.ints(2)
    it = [rd.ints(3) for _ in range(n)]
    best = 0
    for m in range(1 << n):
        ok = all(it[i][0] == 0 or m >> (it[i][0] - 1) & 1 for i in range(n) if m >> i & 1)
        if ok and sum(it[i][1] for i in range(n) if m >> i & 1) <= W:
            best = max(best, sum(it[i][2] for i in range(n) if m >> i & 1))
    return best


add(T, "Chọn môn học có tiên quyết", 5, """
Có `n` môn học. Môn `i` có môn tiên quyết `p_i` (`p_i = 0` nếu không có, đảm bảo `p_i < i`), cần `w_i` tín chỉ và đem lại
`v_i` điểm. Muốn học môn `i` thì phải học môn `p_i`. Tổng số tín chỉ không vượt quá `W`. Tìm tổng điểm lớn nhất.

Gợi ý (cái túi trên cây): duyệt các đỉnh theo thứ tự DFS. Tại đỉnh `u` (vị trí `i`) có hai lựa chọn: **bỏ** `u` — phải bỏ luôn
cả cây con, nhảy tới vị trí `i + size(u)`; hoặc **lấy** `u` rồi xét tiếp vị trí `i + 1`. Độ phức tạp `O(n·W)`.
""", "Dòng đầu `n, W` (1 ≤ n, W ≤ 300). `n` dòng sau, dòng `i` gồm `p_i w_i v_i` (1 ≤ w_i ≤ 300, 1 ≤ v_i ≤ 10^6).",
    "Tổng điểm lớn nhất.", ["4 5\n0 2 3\n1 2 4\n0 3 5\n2 1 10\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 14 else _sol(s), tags=["cái túi", "QHĐ trên cây"])


# 22 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    dp = a[:]
    for i in range(n):
        ai, best = a[i], 0
        for j in range(i):
            if a[j] < ai and dp[j] > best:
                best = dp[j]
        dp[i] = best + ai
    return max(dp)


add(T, "Dãy con tăng có tổng lớn nhất", 2, """
Tìm dãy con tăng ngặt có **tổng** các phần tử lớn nhất, in tổng đó.

Gợi ý: như LIS `O(n²)`, nhưng `dp[i]` lưu tổng lớn nhất thay vì độ dài.
""", "Dòng đầu `n` (1 ≤ n ≤ 2000). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Tổng lớn nhất.",
    ["5\n1 101 2 3 100\n"], lambda r, s: (lambda n: lines(str(n), L(arr(r, n, 1, r.choice([10, 10**9])))))(S(s, 1, 2000)),
    _sol, tags=["LIS"])
