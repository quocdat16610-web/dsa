"""Chuyên đề 14: Max, Min trên đoạn tịnh tiến (deque đơn điệu, ngăn xếp đơn điệu)."""
from collections import deque
from .base import add, Rd, S, J, L, arr, lines

T = 14
MOD = 10**9 + 7


def win_max(a, k, sign=1):
    dq, out = deque(), []
    for i, x in enumerate(a):
        while dq and sign * a[dq[-1]] <= sign * x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(a[dq[0]])
    return out


def _gk(r, s, lo=1, hi=10**9):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, lo, r.choice([5, hi]))
    if r.random() < .2:
        a.sort(reverse=r.random() < .5)
    return lines(J(n, r.randint(1, n)), L(a))


def _ga(r, s, lo=1, hi=10**9):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, lo, r.choice([5, hi]))
    if r.random() < .2:
        a.sort(reverse=r.random() < .5)
    return lines(str(n), L(a))


# 1 -----------------------------------------------------------------------
add(T, "Max trên cửa sổ trượt", 1, """
Với mỗi đoạn con độ dài `k` (từ trái sang phải), in phần tử lớn nhất.

Gợi ý: deque lưu **chỉ số**, giá trị giảm dần từ đầu tới cuối. Thêm `i`: bỏ các phần tử cuối có giá trị ≤ `a_i`.
Bỏ phần tử đầu nếu nó đã ra khỏi cửa sổ. Đầu deque luôn là max. Mỗi chỉ số vào/ra deque một lần → `O(n)`.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n - k + 1` số.",
    ["8 3\n1 3 -1 -3 5 3 6 7\n"], _gk, lambda s: (lambda rd: (lambda n, k: L(win_max(rd.ints(n), k)))(*rd.ints(2)))(Rd(s)),
    brute=lambda s: (lambda rd: (lambda n, k: (lambda a: L(max(a[i:i + k]) for i in range(n - k + 1)))(rd.ints(n)))(*rd.ints(2)))(Rd(s)),
    tags=["deque đơn điệu"])


# 2 -----------------------------------------------------------------------
add(T, "Min trên cửa sổ trượt", 1, """
Với mỗi đoạn con độ dài `k`, in phần tử nhỏ nhất.

Gợi ý: giống bài max nhưng deque giữ giá trị **tăng dần**.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n - k + 1` số.",
    ["8 3\n1 3 2 4 5 3 6 7\n"], _gk, lambda s: (lambda rd: (lambda n, k: L(win_max(rd.ints(n), k, -1)))(*rd.ints(2)))(Rd(s)),
    brute=lambda s: (lambda rd: (lambda n, k: (lambda a: L(min(a[i:i + k]) for i in range(n - k + 1)))(rd.ints(n)))(*rd.ints(2)))(Rd(s)),
    tags=["deque đơn điệu"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    res = [-1] * n; st = []
    for i in range(n - 1, -1, -1):
        while st and st[-1] <= a[i]:
            st.pop()
        res[i] = st[-1] if st else -1
        st.append(a[i])
    return L(res)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return L(next((a[j] for j in range(i + 1, n) if a[j] > a[i]), -1) for i in range(n))


add(T, "Phần tử lớn hơn tiếp theo", 1, """
Với mỗi `a_i`, in giá trị của phần tử **đầu tiên bên phải** lớn hơn hẳn `a_i`, hoặc `-1` nếu không có.

Gợi ý: ngăn xếp đơn điệu. Duyệt từ phải sang trái, bỏ khỏi ngăn xếp các phần tử ≤ `a_i`; đỉnh còn lại là đáp án.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["5\n4 5 2 25 10\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    res = []; st = []
    for i, x in enumerate(a):
        while st and a[st[-1]] >= x:
            st.pop()
        res.append(st[-1] + 1 if st else 0)
        st.append(i)
    return L(res)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return L(next((j + 1 for j in range(i - 1, -1, -1) if a[j] < a[i]), 0) for i in range(n))


add(T, "Giá trị nhỏ hơn gần nhất", 2, """
Với mỗi vị trí `i`, tìm vị trí `j < i` **gần nhất** mà `a_j < a_i`. In `j` (đánh số từ 1), hoặc `0` nếu không có.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["8\n2 5 1 4 8 3 2 5\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return L(x - y for x, y in zip(win_max(a, k), win_max(a, k, -1)))


add(T, "Biên độ dao động", 2, """
Với mỗi đoạn con độ dài `k`, in hiệu giữa phần tử lớn nhất và nhỏ nhất của đoạn.

Gợi ý: chạy song song hai deque (max và min).
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n - k + 1` số.",
    ["6 3\n1 5 2 8 3 3\n"], _gk, _sol,
    brute=lambda s: (lambda rd: (lambda n, k: (lambda a: L(max(a[i:i + k]) - min(a[i:i + k]) for i in range(n - k + 1)))(rd.ints(n)))(*rd.ints(2)))(Rd(s)),
    tags=["deque đơn điệu"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    res = []; st = []
    for i, x in enumerate(a):
        while st and a[st[-1]] <= x:
            st.pop()
        res.append(i - st[-1] if st else i + 1)
        st.append(i)
    return L(res)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); out = []
    for i in range(n):
        j = i
        while j >= 0 and a[j] <= a[i]:
            j -= 1
        out.append(i - j)
    return L(out)


add(T, "Chuỗi ngày giá không cao hơn", 2, """
Giá cổ phiếu ngày `i` là `a_i`. Với mỗi ngày, đếm số ngày liên tiếp **kết thúc tại hôm nay** (tính cả hôm nay, đi ngược về trước)
mà giá không vượt quá giá hôm nay.

Gợi ý: tìm vị trí gần nhất bên trái có giá **lớn hơn hẳn** bằng ngăn xếp đơn điệu.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["7\n100 80 60 70 60 75 85\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu"])


# 7 -----------------------------------------------------------------------
def _hist(h):
    st, best = [], 0
    for i, x in enumerate(h + [0]):
        start = i
        while st and st[-1][1] >= x:
            j, y = st.pop()
            best = max(best, y * (i - j)); start = j
        st.append((start, x))
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); h = rd.ints(n)
    return max(min(h[i:j + 1]) * (j - i + 1) for i in range(n) for j in range(i, n))


add(T, "Hình chữ nhật lớn nhất trong biểu đồ", 2, """
Biểu đồ cột gồm `n` cột rộng 1, cột `i` cao `h_i`. Tìm diện tích hình chữ nhật lớn nhất nằm gọn trong biểu đồ.

Gợi ý: với mỗi cột, tìm cột thấp hơn gần nhất bên trái và bên phải (ngăn xếp đơn điệu); hình chữ nhật có chiều cao `h_i`
trải từ sau cột trái tới trước cột phải.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ h_i ≤ 10^9).", "Diện tích lớn nhất.",
    ["7\n2 1 5 6 2 3 1\n"], lambda r, s: _ga(r, s, 0), lambda s: _hist(list(map(int, s.split()[1:]))), brute=_br,
    tags=["ngăn xếp đơn điệu"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 1000), S(s, 1, 1000)
    p = r.choice([.5, .8, .95])
    return lines(J(n, m), *("".join("1" if r.random() < p else "0" for _ in range(m)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    h = [0] * m; best = 0
    for _ in range(n):
        row = rd.str()
        h = [h[j] + 1 if row[j] == "1" else 0 for j in range(m)]
        best = max(best, _hist(h))
    return best


add(T, "Hình chữ nhật toàn số 1", 3, """
Cho ma trận nhị phân `n × m`. Tìm diện tích hình chữ nhật con lớn nhất chỉ gồm số `1`.

Gợi ý: với mỗi hàng, `h[j]` = số ô `1` liên tiếp kéo lên trên tính từ hàng đó. Mỗi hàng là một bài "hình chữ nhật lớn nhất trong biểu đồ".
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 1000). `n` dòng sau mỗi dòng xâu 0/1 độ dài `m`.", "Diện tích lớn nhất.",
    ["4 5\n10100\n10111\n11111\n10010\n"], _g, _sol, tags=["ngăn xếp đơn điệu"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    left = [0] * n; right = [0] * n; st = []
    for i in range(n):
        while st and a[st[-1]] > a[i]:
            st.pop()
        left[i] = i - (st[-1] if st else -1); st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        right[i] = (st[-1] if st else n) - i; st.append(i)
    return sum(a[i] * left[i] * right[i] for i in range(n)) % MOD


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); tot = 0
    for i in range(n):
        mn = a[i]
        for j in range(i, n):
            mn = min(mn, a[j]); tot += mn
    return tot % MOD


add(T, "Tổng min của mọi đoạn con", 3, """
Tính tổng giá trị nhỏ nhất của tất cả các đoạn con liên tiếp, modulo `10^9 + 7`.

Gợi ý (kỹ thuật đóng góp): `a_i` là min của `L_i · R_i` đoạn, trong đó `L_i`, `R_i` là số vị trí có thể mở rộng sang trái/phải.
Cẩn thận phần tử bằng nhau: một bên dùng `<`, bên kia dùng `≤` để không đếm trùng.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Kết quả modulo 10^9+7.",
    ["4\n3 1 2 4\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu", "đóng góp"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = r.choice([10, 1000, 10**9])
    return lines(J(n, r.randint(0, hi // r.choice([1, 3, 30]))), L(arr(r, n, 1, hi)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    mx, mn = deque(), deque(); l = best = 0
    for i, x in enumerate(a):
        while mx and a[mx[-1]] <= x:
            mx.pop()
        mx.append(i)
        while mn and a[mn[-1]] >= x:
            mn.pop()
        mn.append(i)
        while a[mx[0]] - a[mn[0]] > k:
            l += 1
            if mx[0] < l:
                mx.popleft()
            if mn[0] < l:
                mn.popleft()
        best = max(best, i - l + 1)
    return best


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return max(j - i for i in range(n) for j in range(i + 1, n + 1) if max(a[i:j]) - min(a[i:j]) <= k)


add(T, "Đoạn dài nhất có biên độ nhỏ", 3, """
Tìm đoạn con liên tiếp dài nhất mà (max − min) ≤ k.

Gợi ý: hai con trỏ + hai deque đơn điệu giữ max và min của cửa sổ hiện tại.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 0 ≤ k ≤ 10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Độ dài lớn nhất.",
    ["6 2\n1 3 6 7 9 8\n"], _g, _sol, brute=_br, tags=["deque đơn điệu", "hai con trỏ"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a_ = r.randint(1, n); b_ = r.randint(a_, n)
    return lines(J(n, a_, b_), L(arr(r, n, -10**9, 10**9)))


def _sol(s):
    rd = Rd(s); n, A, B = rd.ints(3); a = rd.ints(n)
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    dq = deque(); best = -10**30
    for r_ in range(A, n + 1):
        j = r_ - A
        while dq and p[dq[-1]] >= p[j]:
            dq.pop()
        dq.append(j)
        if dq[0] < r_ - B:
            dq.popleft()
        best = max(best, p[r_] - p[dq[0]])
    return best


def _br(s):
    rd = Rd(s); n, A, B = rd.ints(3); a = rd.ints(n)
    return max(sum(a[i:j]) for i in range(n) for j in range(i + A, min(n, i + B) + 1))


add(T, "Đoạn con có tổng lớn nhất với độ dài giới hạn", 3, """
Tìm đoạn con liên tiếp có độ dài trong `[A, B]` với tổng lớn nhất.

Gợi ý: tổng đoạn `(l, r] = p[r] - p[l]` với `r - B ≤ l ≤ r - A`. Khi `r` tăng, cửa sổ các `l` hợp lệ trượt sang phải →
dùng deque giữ min của `p[l]`.
""", "Dòng đầu `n, A, B` (1 ≤ A ≤ B ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^9).", "Tổng lớn nhất.",
    ["8 1 2\n-1 3 -2 5 3 -5 2 2\n"], _g, _sol, brute=_br, tags=["deque đơn điệu", "tiền tố"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n)), L(arr(r, n, -10**4, 10**4)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    dp = [0] * n; dp[0] = a[0]; dq = deque([0])
    for i in range(1, n):
        if dq[0] < i - k:
            dq.popleft()
        dp[i] = a[i] + dp[dq[0]]
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return dp[-1]


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    dp = [0] * n; dp[0] = a[0]
    for i in range(1, n):
        dp[i] = a[i] + max(dp[max(0, i - k):i])
    return dp[-1]


add(T, "Nhảy ô lấy điểm", 3, """
Có `n` ô, ô `i` có điểm `a_i` (có thể âm). Bạn đứng ở ô 1 (được điểm ô 1), mỗi bước nhảy về phía trước tối đa `k` ô, phải kết thúc ở ô `n`.
Tổng điểm các ô đã đứng lớn nhất là bao nhiêu?

Gợi ý: `dp[i] = a_i + max(dp[i-k..i-1])` — `O(n·k)` quá chậm. Max trên cửa sổ trượt bằng deque → `O(n)`
(đây là kỹ thuật **tối ưu QHĐ bằng deque**).
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^4).", "Tổng điểm lớn nhất.",
    ["6 2\n1 -1 -2 4 -7 3\n"], _g, _sol, brute=_br, tags=["deque đơn điệu", "tối ưu QHĐ"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, -r.choice([10, 10**5]), 10**5)
    return lines(J(n, r.randint(1, max(1, sum(x for x in a if x > 0) // r.choice([1, 3, 50])))), L(a))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    dq = deque(); best = n + 1
    for i in range(n + 1):
        while dq and p[i] - p[dq[0]] >= k:
            best = min(best, i - dq.popleft())
        while dq and p[dq[-1]] >= p[i]:
            dq.pop()
        dq.append(i)
    return best if best <= n else -1


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    v = [j - i for i in range(n) for j in range(i + 1, n + 1) if sum(a[i:j]) >= k]
    return min(v) if v else -1


add(T, "Đoạn ngắn nhất có tổng ≥ k (có số âm)", 4, """
Cho dãy có thể chứa số âm. Tìm độ dài nhỏ nhất của đoạn con có tổng ≥ k, hoặc `-1`. (Hai con trỏ thông thường **sai** khi có số âm!)

Gợi ý: deque các chỉ số tiền tố với `p` tăng dần. Tại `i`: trong khi `p[i] - p[đầu] ≥ k` thì cập nhật đáp án và bỏ đầu;
sau đó bỏ khỏi cuối những `p` ≥ `p[i]` (chúng không bao giờ tốt hơn `i`).
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 1 ≤ k ≤ 10^9). Dòng sau `n` số (|a_i| ≤ 10^5).", "Độ dài nhỏ nhất hoặc `-1`.",
    ["3 3\n2 -1 2\n"], _g, _sol, brute=_br, tags=["deque đơn điệu", "tiền tố"])


# 14 ----------------------------------------------------------------------
def _contrib(a, cmp_strict, cmp_weak):
    n = len(a)
    left = [0] * n; right = [0] * n; st = []
    for i in range(n):
        while st and cmp_strict(a[st[-1]], a[i]):
            st.pop()
        left[i] = i - (st[-1] if st else -1); st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and cmp_weak(a[st[-1]], a[i]):
            st.pop()
        right[i] = (st[-1] if st else n) - i; st.append(i)
    return sum(a[i] * left[i] * right[i] for i in range(n))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    mx = _contrib(a, lambda x, y: x < y, lambda x, y: x <= y)
    mn = _contrib(a, lambda x, y: x > y, lambda x, y: x >= y)
    return mx - mn


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); tot = 0
    for i in range(n):
        mx = mn = a[i]
        for j in range(i, n):
            mx = max(mx, a[j]); mn = min(mn, a[j]); tot += mx - mn
    return tot


add(T, "Tổng biên độ mọi đoạn con", 4, """
Tính `Σ (max - min)` trên tất cả các đoạn con liên tiếp.

Gợi ý: `Σ max - Σ min`, mỗi tổng tính bằng kỹ thuật đóng góp với ngăn xếp đơn điệu. Kết quả tối đa cỡ `2·10^16` — vừa `long long`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^6).", "Kết quả.",
    ["3\n1 3 2\n"], lambda r, s: _ga(r, s, 1, 10**6), _sol, brute=_br, tags=["ngăn xếp đơn điệu", "đóng góp"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    return lines(J(n, m, r.randint(1, n), r.randint(1, m)), *(L(arr(r, m, 1, 10**9)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m, A, B = rd.ints(4); a = [rd.ints(m) for _ in range(n)]
    rows = [win_max(row, B) for row in a]  # n × (m-B+1)
    cols = [win_max([rows[i][j] for i in range(n)], A) for j in range(m - B + 1)]  # (m-B+1) × (n-A+1)
    return [L(cols[j][i] for j in range(m - B + 1)) for i in range(n - A + 1)]


def _br(s):
    rd = Rd(s); n, m, A, B = rd.ints(4); a = [rd.ints(m) for _ in range(n)]
    return [L(max(a[x][y] for x in range(i, i + A) for y in range(j, j + B)) for j in range(m - B + 1)) for i in range(n - A + 1)]


add(T, "Max trên cửa sổ 2D", 4, """
Cho ma trận `n × m`. Với mọi hình chữ nhật con kích thước `A × B` (A hàng, B cột), in phần tử lớn nhất — kết quả là ma trận
`(n-A+1) × (m-B+1)`.

Gợi ý: trượt cửa sổ độ dài `B` trên từng hàng (deque), được ma trận trung gian; rồi trượt cửa sổ độ dài `A` trên từng cột của nó.
""", "Dòng đầu `n, m, A, B` (1 ≤ A ≤ n ≤ 500, 1 ≤ B ≤ m ≤ 500). `n` dòng sau mỗi dòng `m` số (1 ≤ a ≤ 10^9).",
    "Ma trận kết quả.", ["3 3 2 2\n1 2 3\n4 5 6\n7 8 1\n"], _g, _sol, brute=_br, tags=["deque đơn điệu", "2D"])


# 16 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); h = rd.ints(n)
    st, tot = [], 0
    for i, x in enumerate(h):
        while st and h[st[-1]] < x:
            mid = st.pop()
            if not st:
                break
            l = st[-1]
            tot += (min(h[l], x) - h[mid]) * (i - l - 1)
        st.append(i)
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); h = rd.ints(n)
    lm = [0] * n; rm = [0] * n
    for i in range(n):
        lm[i] = max(lm[i - 1] if i else 0, h[i])
    for i in range(n - 1, -1, -1):
        rm[i] = max(rm[i + 1] if i < n - 1 else 0, h[i])
    return sum(min(lm[i], rm[i]) - h[i] for i in range(n))


add(T, "Hứng nước mưa", 3, """
Địa hình gồm `n` cột rộng 1, cột `i` cao `h_i`. Sau cơn mưa, lượng nước đọng lại giữa các cột là bao nhiêu?

Gợi ý: ngăn xếp đơn điệu giảm — khi gặp cột cao hơn đỉnh ngăn xếp, "đáy" vừa bị bật ra cùng hai bờ tạo thành một lớp nước.
(Cách khác: nước tại `i` = `min(max trái, max phải) - h_i`.)
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ h_i ≤ 10^9).", "Lượng nước.",
    ["12\n0 1 0 2 1 0 1 3 2 1 2 1\n"], lambda r, s: _ga(r, s, 0), _sol, brute=_br, tags=["ngăn xếp đơn điệu"])


# 17 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); h = rd.ints(n)
    res = [0] * n; st = []
    for i in range(n - 1, -1, -1):
        c = 0
        while st and st[-1] < h[i]:
            st.pop(); c += 1
        if st:
            c += 1
        res[i] = c
        while st and st[-1] == h[i]:
            st.pop()
        st.append(h[i])
    return L(res)


def _br(s):
    rd = Rd(s); n = rd.int(); h = rd.ints(n); out = []
    for i in range(n):
        c, mx = 0, 0
        for j in range(i + 1, n):
            if mx < h[j] and h[i] > mx:
                c += 1
            mx = max(mx, h[j])
            if mx >= h[i]:
                break
        out.append(c)
    return L(out)


add(T, "Nhìn thấy bao nhiêu người", 3, """
`n` người đứng thành hàng, người `i` cao `h_i`. Người `i` **nhìn thấy** người `j > i` nếu mọi người đứng giữa họ đều thấp hơn hẳn
`min(h_i, h_j)`. Với mỗi người, đếm số người phía bên phải mà họ nhìn thấy.

Gợi ý: duyệt từ phải sang trái với ngăn xếp giảm dần; người `i` thấy tất cả những người bị bật khỏi ngăn xếp (thấp hơn mình),
cộng thêm người đầu tiên còn lại (nếu có).
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ h_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["6\n10 6 8 5 11 9\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu"])


# 18 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    left = [-1] * n; right = [n] * n; st = []
    for i in range(n):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        left[i] = st[-1] if st else -1; st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] >= a[i]:
            st.pop()
        right[i] = st[-1] if st else n; st.append(i)
    ans = [0] * (n + 2)
    for i in range(n):
        ln = right[i] - left[i] - 1
        ans[ln] = max(ans[ln], a[i])
    for k in range(n - 1, 0, -1):
        ans[k] = max(ans[k], ans[k + 1])
    return L(ans[1:n + 1])


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return L(max(min(a[i:i + k]) for i in range(n - k + 1)) for k in range(1, n + 1))


add(T, "Max của min theo mọi độ dài", 5, """
Với mỗi `k = 1..n`, xét mọi đoạn con độ dài `k`, lấy min của từng đoạn, rồi lấy max của các min đó. In `n` giá trị.

Gợi ý: `a_i` là min của đoạn dài nhất `[left_i + 1, right_i - 1]` (độ dài `len_i`) — nên nó là ứng viên cho mọi `k ≤ len_i`.
Ghi `ans[len_i] = max(ans[len_i], a_i)` rồi lấy max hậu tố.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["7\n10 20 30 50 10 70 30\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2000)
    a = arr(r, n, 1, r.choice([10, 10**6]))
    return lines(J(n, r.randint(max(a), max(a) * r.choice([1, 3, 20]))), L(a))


def _sol(s):
    rd = Rd(s); n, lim = rd.ints(2); a = rd.ints(n)
    INF = 10**30
    dp = [0] + [INF] * n
    for i in range(1, n + 1):
        mx, tot, best = 0, 0, INF
        for j in range(i, 0, -1):
            tot += a[j - 1]
            if tot > lim:
                break
            if a[j - 1] > mx:
                mx = a[j - 1]
            v = dp[j - 1] + mx
            if v < best:
                best = v
        dp[i] = best
    return dp[n]


add(T, "Cắt dãy", 4, """
Chia dãy `n` số thành các đoạn liên tiếp sao cho tổng mỗi đoạn không vượt quá `M`. Chi phí của một cách chia là tổng các **giá trị lớn nhất**
của từng đoạn. Tìm chi phí nhỏ nhất (đảm bảo mọi `a_i ≤ M`).

Gợi ý: `dp[i] = min_j (dp[j] + max(a_{j+1..i}))` với tổng đoạn ≤ M. Với `n ≤ 2000`, `O(n²)` là đủ
(nâng cao: deque đơn điệu + multiset cho `O(n log n)`).
""", "Dòng đầu `n, M` (1 ≤ n ≤ 2000, 1 ≤ M ≤ 10^9). Dòng sau `n` số (1 ≤ a_i ≤ M).", "Chi phí nhỏ nhất.",
    ["8 17\n2 2 2 8 1 8 2 1\n"], _g, _sol, tags=["QHĐ", "deque đơn điệu"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, -10**9, 10**9)))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    b = a + a; p = [0]
    for x in b:
        p.append(p[-1] + x)
    dq = deque([0]); best = -10**30
    for r_ in range(1, 2 * n + 1):
        if dq[0] < r_ - n:
            dq.popleft()
        best = max(best, p[r_] - p[dq[0]])
        while dq and p[dq[-1]] >= p[r_]:
            dq.pop()
        dq.append(r_)
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return max(sum(a[(i + t) % n] for t in range(ln)) for i in range(n) for ln in range(1, n + 1))


add(T, "Đoạn con lớn nhất trên vòng tròn", 4, """
Dãy số được xếp trên **vòng tròn** (phần tử cuối kề phần tử đầu). Tìm đoạn con liên tiếp (khác rỗng, không dài quá `n`) có tổng lớn nhất.

Gợi ý: nhân đôi dãy; đoạn `(l, r]` hợp lệ khi `r - n ≤ l < r`. Dùng deque giữ min `p[l]` trên cửa sổ trượt.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^9).", "Tổng lớn nhất.",
    ["4\n5 -3 -3 5\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 60 else _sol(s),
    tags=["deque đơn điệu", "vòng tròn"])


# 21 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    st = []  # chỉ số có giá trị giảm ngặt (ứng viên cho i)
    for i in range(n):
        if not st or a[i] < a[st[-1]]:
            st.append(i)
    best = 0
    for j in range(n - 1, -1, -1):
        while st and a[st[-1]] <= a[j]:
            best = max(best, j - st.pop())
    return best


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return max(j - i for i in range(n) for j in range(i, n) if a[i] <= a[j])


add(T, "Khoảng cách xa nhất", 3, """
Tìm giá trị lớn nhất của `j - i` với `i ≤ j` và `a_i ≤ a_j`.

Gợi ý: chỉ những `i` là **min tiền tố mới** (nhỏ hơn mọi phần tử trước nó) mới có thể là đáp án → lưu chúng vào ngăn xếp.
Duyệt `j` từ phải sang trái và bật ngăn xếp khi `a_{đỉnh} ≤ a_j`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Khoảng cách lớn nhất.",
    ["9\n34 8 10 3 2 80 30 33 1\n"], _ga, _sol, brute=_br, tags=["ngăn xếp đơn điệu"])
