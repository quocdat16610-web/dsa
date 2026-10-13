"""Chuyên đề 4: Hai con trỏ."""
from collections import defaultdict
from .base import add, Rd, S, J, L, arr, lines, rstr

T = 4


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 10**5)
    hi = S(s, 10, 10**9)
    return lines(J(n, m), L(sorted(arr(r, n, -hi, hi))), L(sorted(arr(r, m, -hi, hi))))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n); b = rd.ints(m)
    i = j = 0; out = []
    while i < n or j < m:
        if j == m or (i < n and a[i] <= b[j]):
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return L(out)


add(T, "Trộn hai dãy", 1, """
Cho hai dãy đã sắp xếp không giảm. Hãy trộn thành một dãy không giảm.

Gợi ý: con trỏ `i` trên dãy `a`, con trỏ `j` trên dãy `b`; mỗi bước lấy phần tử nhỏ hơn. Độ phức tạp `O(n + m)`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 10^5). Hai dòng sau là hai dãy không giảm (|giá trị| ≤ 10^9).",
    "Một dòng gồm `n + m` số.", ["3 4\n1 3 5\n2 2 4 6\n"], _g, _sol, tags=["hai con trỏ"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5)
    a = arr(r, n, 1, S(s, 20, 10**9))
    x = a[0] + a[-1] if r.random() < .5 else r.randint(2, 2 * max(a))
    return lines(J(n, x), L(sorted(a)))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    i, j = 0, n - 1
    while i < j:
        if a[i] + a[j] == x:
            return "YES"
        if a[i] + a[j] < x:
            i += 1
        else:
            j -= 1
    return "NO"


add(T, "Tồn tại cặp có tổng x", 1, """
Cho dãy không giảm `a`. Có tồn tại hai chỉ số `i < j` mà `a_i + a_j = x` không?

Gợi ý: `i` ở đầu, `j` ở cuối. Tổng nhỏ hơn `x` → tăng `i`; lớn hơn → giảm `j`.
""", "Dòng đầu `n, x` (2 ≤ n ≤ 2·10^5, 1 ≤ x ≤ 2·10^9). Dòng sau là dãy không giảm (1 ≤ a_i ≤ 10^9).",
    "`YES` hoặc `NO`.", ["5 9\n1 2 4 5 8\n", "3 10\n1 2 3\n"], _g, _sol, tags=["hai con trỏ"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 10**5)
    hi = S(s, 10, 10**9)
    return lines(J(n, m), L(sorted(arr(r, n, 1, hi))), L(sorted(arr(r, m, 1, hi))))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n); b = rd.ints(m)
    i, out = 0, []
    for x in b:
        while i < n and a[i] < x:
            i += 1
        out.append(i)
    return L(out)


add(T, "Đếm phần tử nhỏ hơn", 1, """
Cho hai dãy không giảm `a` và `b`. Với mỗi `b_j`, đếm số phần tử `a_i < b_j`.

Yêu cầu giải bằng hai con trỏ trong `O(n + m)` (không dùng tìm kiếm nhị phân).
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 10^5). Hai dòng sau là hai dãy không giảm (1 ≤ giá trị ≤ 10^9).",
    "Một dòng gồm `m` số.", ["4 3\n1 3 3 7\n2 3 8\n"], _g, _sol, tags=["hai con trỏ"])


# 4 -----------------------------------------------------------------------
def _gpos(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, S(s, 10, 10**9))
    return lines(J(n, r.randint(1, max(1, sum(a) // r.choice([1, 2, 10, n])))), L(a))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    l = cur = best = 0
    for r_ in range(n):
        cur += a[r_]
        while cur > x:
            cur -= a[l]; l += 1
        best = max(best, r_ - l + 1)
    return best


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    return max([j - i for i in range(n) for j in range(i + 1, n + 1) if sum(a[i:j]) <= x] + [0])


add(T, "Đoạn dài nhất có tổng không vượt quá s", 1, """
Cho dãy `n` số **dương** và số `s`. Tìm độ dài lớn nhất của đoạn con liên tiếp có tổng ≤ s (in 0 nếu không có).

Gợi ý: cửa sổ trượt — tăng đầu phải `r`, khi tổng vượt `s` thì tăng đầu trái `l`. Mỗi con trỏ chỉ đi tiến nên `O(n)`.
""", "Dòng đầu `n, s` (1 ≤ n ≤ 2·10^5, 1 ≤ s ≤ 10^18). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Độ dài lớn nhất.",
    ["7 20\n2 6 4 3 6 8 9\n"], _gpos, _sol, brute=_br, tags=["hai con trỏ", "cửa sổ trượt"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    l = cur = 0; best = n + 1
    for r_ in range(n):
        cur += a[r_]
        while cur - a[l] >= x:
            cur -= a[l]; l += 1
        if cur >= x:
            best = min(best, r_ - l + 1)
    return best if best <= n else -1


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    return min([j - i for i in range(n) for j in range(i + 1, n + 1) if sum(a[i:j]) >= x] + [10**9]) if True else 0


def _br5(s):
    v = _br(s)
    return -1 if v == 10**9 else v


add(T, "Đoạn ngắn nhất có tổng ít nhất s", 2, """
Cho dãy `n` số dương. Tìm độ dài nhỏ nhất của đoạn con có tổng ≥ s, hoặc `-1` nếu không có.
""", "Dòng đầu `n, s` (1 ≤ n ≤ 2·10^5, 1 ≤ s ≤ 10^18). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Độ dài nhỏ nhất hoặc `-1`.",
    ["7 20\n2 6 4 3 6 8 9\n", "2 100\n1 2\n"], _gpos, _sol, brute=_br5, tags=["hai con trỏ", "cửa sổ trượt"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    l = cur = tot = 0
    for r_ in range(n):
        cur += a[r_]
        while cur > x:
            cur -= a[l]; l += 1
        tot += r_ - l + 1
    return tot


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if sum(a[i:j]) <= x)


add(T, "Đếm đoạn có tổng không vượt quá s", 2, """
Cho dãy `n` số dương. Đếm số đoạn con liên tiếp có tổng ≤ s.

Gợi ý: với mỗi đầu phải `r`, mọi đầu trái trong `[l, r]` đều hợp lệ → cộng `r - l + 1`.
""", "Dòng đầu `n, s` (1 ≤ n ≤ 2·10^5, 1 ≤ s ≤ 10^18). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số đoạn.",
    ["7 20\n2 6 4 3 6 8 9\n"], _gpos, _sol, brute=_br, tags=["hai con trỏ"])


# 7 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    l = cur = tot = 0
    for r_ in range(n):
        cur += a[r_]
        while cur - a[l] >= x and l < r_:
            cur -= a[l]; l += 1
        if cur >= x:
            tot += l + 1
    return tot


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if sum(a[i:j]) >= x)


add(T, "Đếm đoạn có tổng ít nhất s", 2, """
Cho dãy `n` số dương. Đếm số đoạn con liên tiếp có tổng ≥ s.

Gợi ý: với mỗi `r`, tìm `l` lớn nhất mà tổng `[l, r]` vẫn ≥ s; khi đó mọi đầu trái `1..l` đều hợp lệ.
""", "Dòng đầu `n, s` (1 ≤ n ≤ 2·10^5, 1 ≤ s ≤ 10^18). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số đoạn.",
    ["7 20\n2 6 4 3 6 8 9\n"], _gpos, _sol, brute=_br, tags=["hai con trỏ"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 10**5)
    hi = r.choice([3, 10, 1000, 10**9])
    return lines(J(n, m), L(sorted(arr(r, n, 1, hi))), L(sorted(arr(r, m, 1, hi))))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n); b = rd.ints(m)
    i = j = tot = 0
    while i < n and j < m:
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            v, ci, cj = a[i], 0, 0
            while i < n and a[i] == v:
                i += 1; ci += 1
            while j < m and b[j] == v:
                j += 1; cj += 1
            tot += ci * cj
    return tot


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); a = rd.ints(n); b = rd.ints(m)
    return sum(1 for x in a for y in b if x == y)


add(T, "Số cặp bằng nhau", 2, """
Cho hai dãy không giảm `a` và `b`. Đếm số cặp `(i, j)` mà `a_i = b_j`.

Gợi ý: khi gặp giá trị bằng nhau, đếm độ dài khối giá trị đó ở cả hai dãy rồi nhân lại.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 10^5). Hai dòng sau là hai dãy không giảm (1 ≤ giá trị ≤ 10^9).", "Số cặp.",
    ["8 7\n1 1 3 3 3 5 8 8\n1 3 3 4 5 5 5\n"], _g, _sol, brute=_br, tags=["hai con trỏ"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return rstr(r, n, "abcdefghijklmnopqrstuvwxyz"[:r.choice([2, 5, 26])])


def _sol(s):
    t = s.split()[0]
    last, l, best = {}, 0, 0
    for i, c in enumerate(t):
        if last.get(c, -1) >= l:
            l = last[c] + 1
        last[c] = i
        best = max(best, i - l + 1)
    return best


def _br(s):
    t = s.split()[0]
    return max(j - i for i in range(len(t)) for j in range(i + 1, len(t) + 1) if len(set(t[i:j])) == j - i)


add(T, "Xâu con dài nhất không lặp ký tự", 2, """
Cho xâu `s` gồm chữ cái thường. Tìm độ dài lớn nhất của một xâu con liên tiếp không có ký tự nào xuất hiện hai lần.
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 2·10^5).", "Độ dài lớn nhất.", ["abcabcbb\n", "bbbb\n"], _g, _sol,
    brute=_br, tags=["hai con trỏ", "xâu"])


# 10 ----------------------------------------------------------------------
def _gk(r, s):
    n = S(s, 1, 2 * 10**5)
    v = r.choice([3, 10, 100, n])
    return lines(J(n, r.randint(1, min(n, v))), L(arr(r, n, 1, v)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    cnt = defaultdict(int); l = best = 0
    for r_ in range(n):
        cnt[a[r_]] += 1
        while len(cnt) > k:
            cnt[a[l]] -= 1
            if cnt[a[l]] == 0:
                del cnt[a[l]]
            l += 1
        best = max(best, r_ - l + 1)
    return best


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return max(j - i for i in range(n) for j in range(i + 1, n + 1) if len(set(a[i:j])) <= k)


add(T, "Đoạn dài nhất có tối đa k giá trị phân biệt", 3, """
Tìm độ dài lớn nhất của đoạn con liên tiếp chứa **không quá** `k` giá trị khác nhau.

Gợi ý: dùng mảng/`map` đếm tần suất trong cửa sổ, và biến đếm số giá trị phân biệt.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 2·10^5).", "Độ dài lớn nhất.",
    ["6 2\n1 2 1 3 3 4\n"], _gk, _sol, brute=_br, tags=["hai con trỏ", "đếm tần suất"])


# 11 ----------------------------------------------------------------------
def _atmost(a, k):
    if k <= 0:
        return 0
    cnt = defaultdict(int); l = tot = 0
    for r_ in range(len(a)):
        cnt[a[r_]] += 1
        while len(cnt) > k:
            cnt[a[l]] -= 1
            if cnt[a[l]] == 0:
                del cnt[a[l]]
            l += 1
        tot += r_ - l + 1
    return tot


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return _atmost(a, k)


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if len(set(a[i:j])) <= k)


add(T, "Đếm đoạn có tối đa k giá trị phân biệt", 3, """
Đếm số đoạn con liên tiếp chứa **không quá** `k` giá trị khác nhau.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 2·10^5).", "Số đoạn.",
    ["5 2\n1 2 1 3 4\n"], _gk, _sol, brute=_br, tags=["hai con trỏ", "đếm tần suất"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    k = r.randint(1, min(n, S(s, 3, 1000)))
    a = arr(r, n, 1, k + r.choice([0, 0, 2, 50]))
    return lines(J(n, k), L(a))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    cnt = [0] * (k + 1); have = 0; l = 0; best = n + 1
    for r_ in range(n):
        v = a[r_]
        if v <= k:
            cnt[v] += 1
            if cnt[v] == 1:
                have += 1
        while have == k:
            best = min(best, r_ - l + 1)
            u = a[l]
            if u <= k:
                cnt[u] -= 1
                if cnt[u] == 0:
                    have -= 1
            l += 1
    return best if best <= n else -1


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    need = set(range(1, k + 1))
    v = [j - i for i in range(n) for j in range(i + 1, n + 1) if need <= set(a[i:j])]
    return min(v) if v else -1


add(T, "Đoạn ngắn nhất chứa đủ 1..k", 3, """
Tìm độ dài nhỏ nhất của đoạn con liên tiếp chứa **tất cả** các giá trị `1, 2, ..., k`. In `-1` nếu không tồn tại.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^6).", "Độ dài nhỏ nhất hoặc `-1`.",
    ["7 3\n2 5 1 2 3 1 4\n"], _g, _sol, brute=_br, tags=["hai con trỏ"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 3, 2000)
    a = arr(r, n, 1, S(s, 20, 10**9))
    x = sum(r.sample(a, 3)) if r.random() < .5 else r.randint(3, 3 * max(a))
    return lines(J(n, x), L(a))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); a = sorted(rd.ints(n))
    for i in range(n - 2):
        j, k = i + 1, n - 1
        t = x - a[i]
        while j < k:
            v = a[j] + a[k]
            if v == t:
                return "YES"
            if v < t:
                j += 1
            else:
                k -= 1
    return "NO"


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); a = rd.ints(n)
    from itertools import combinations
    return "YES" if any(sum(c) == x for c in combinations(a, 3)) else "NO"


add(T, "Tổng ba số", 3, """
Có tồn tại ba chỉ số phân biệt `i, j, k` mà `a_i + a_j + a_k = x` không?

Gợi ý: sắp xếp, cố định `i` rồi tìm cặp `(j, k)` bằng hai con trỏ → `O(n²)`.
""", "Dòng đầu `n, x` (3 ≤ n ≤ 2000, 1 ≤ x ≤ 3·10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "`YES` hoặc `NO`.",
    ["5 12\n1 9 3 5 2\n"], _g, _sol, brute=_br, tags=["hai con trỏ", "sắp xếp"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    al = "abcdefghijklmnopqrstuvwxyz"[:r.choice([3, 6, 26])]
    t = rstr(r, n, al)
    m = r.randint(1, min(n, S(s, 3, 100)))
    p = rstr(r, m, al)
    return lines(t, p)


def _sol(s):
    t, p = s.split()
    need = defaultdict(int)
    for c in p:
        need[c] += 1
    miss = len(need); have = defaultdict(int); l = 0; best = len(t) + 1
    for r_, c in enumerate(t):
        have[c] += 1
        if have[c] == need.get(c, -1):
            miss -= 1
        while miss == 0:
            best = min(best, r_ - l + 1)
            d = t[l]
            if have[d] == need.get(d, -1):
                miss += 1
            have[d] -= 1
            l += 1
    return best if best <= len(t) else -1


def _br(s):
    from collections import Counter
    t, p = s.split()
    cp = Counter(p)
    v = [j - i for i in range(len(t)) for j in range(i + 1, len(t) + 1)
         if not (cp - Counter(t[i:j]))]
    return min(v) if v else -1


add(T, "Cửa sổ nhỏ nhất chứa xâu mẫu", 3, """
Cho hai xâu `s` và `p`. Tìm độ dài nhỏ nhất của xâu con liên tiếp của `s` chứa mọi ký tự của `p`
(tính cả số lần lặp: nếu `p` có hai chữ `a` thì xâu con phải có ít nhất hai chữ `a`). In `-1` nếu không có.
""", "Dòng đầu là `s` (1 ≤ |s| ≤ 2·10^5). Dòng hai là `p` (1 ≤ |p| ≤ |s|). Chỉ gồm chữ cái thường.",
    "Độ dài nhỏ nhất hoặc `-1`.", ["adobecodebanc\nabc\n", "aa\naaa\n"], _g, _sol, brute=_br, tags=["hai con trỏ", "xâu"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    w = arr(r, n, 1, 10**4); v = arr(r, n, 1, 10**9)
    return lines(J(n, r.randint(1, S(s, 10, 10**9))), L(w), L(v))


def _sol(s):
    rd = Rd(s); n, x = rd.ints(2); w = rd.ints(n); v = rd.ints(n)
    l = cw = cv = best = 0
    for r_ in range(n):
        cw += w[r_]; cv += v[r_]
        while cw > x:
            cw -= w[l]; cv -= v[l]; l += 1
        best = max(best, cv)
    return best


def _br(s):
    rd = Rd(s); n, x = rd.ints(2); w = rd.ints(n); v = rd.ints(n)
    return max([sum(v[i:j]) for i in range(n) for j in range(i + 1, n + 1) if sum(w[i:j]) <= x] + [0])


add(T, "Đoạn có giá trị lớn nhất", 3, """
Có `n` món hàng xếp thành hàng, món `i` nặng `w_i` và có giá trị `v_i`. Chọn một đoạn liên tiếp có tổng khối lượng ≤ s
sao cho tổng giá trị lớn nhất (in 0 nếu không chọn được món nào).
""", "Dòng đầu `n, s` (1 ≤ n ≤ 2·10^5, 1 ≤ s ≤ 10^9). Dòng hai gồm `w_i` (1 ≤ w_i ≤ 10^4), dòng ba gồm `v_i` (1 ≤ v_i ≤ 10^9).",
    "Tổng giá trị lớn nhất.", ["4 5\n2 3 1 4\n10 1 7 20\n"], _g, _sol, brute=_br, tags=["hai con trỏ"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    pr = r.random()
    t = "".join("1" if r.random() < pr else "0" for _ in range(n))
    return lines(J(n, r.randint(0, min(n, max(3, t.count("1"))))), t)


def _cnt_atmost(t, k):
    if k < 0:
        return 0
    l = ones = tot = 0
    for r_, c in enumerate(t):
        ones += c == "1"
        while ones > k:
            ones -= t[l] == "1"; l += 1
        tot += r_ - l + 1
    return tot


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); t = rd.str()
    return _cnt_atmost(t, k) - _cnt_atmost(t, k - 1)


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); t = rd.str()
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if t[i:j].count("1") == k)


add(T, "Xâu con có đúng k chữ số 1", 4, """
Cho xâu nhị phân. Đếm số xâu con liên tiếp (khác rỗng) chứa **đúng** `k` chữ số `1`.

Gợi ý: `đúng(k) = không quá(k) - không quá(k-1)`; "không quá" đếm được bằng hai con trỏ.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 0 ≤ k ≤ n). Dòng sau là xâu nhị phân độ dài `n`.", "Số xâu con.",
    ["5 2\n10101\n", "3 0\n000\n"], _g, _sol, brute=_br, tags=["hai con trỏ", "đếm"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 3, 2 * 10**5)
    a = sorted(r.sample(range(1, S(s, 3 * n, 10**9) + 1), n))
    return lines(J(n, r.randint(1, max(1, (a[-1] - a[0]) // r.choice([1, 5, 100, n])))), L(a))


def _sol(s):
    rd = Rd(s); n, d = rd.ints(2); a = rd.ints(n)
    l = tot = 0
    for r_ in range(n):
        while a[r_] - a[l] > d:
            l += 1
        c = r_ - l
        tot += c * (c - 1) // 2
    return tot


def _br(s):
    rd = Rd(s); n, d = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if a[k] - a[i] <= d)


add(T, "Bộ ba điểm gần nhau", 3, """
Cho `n` điểm phân biệt trên trục số theo thứ tự tăng dần. Đếm số bộ ba điểm sao cho khoảng cách giữa hai điểm xa nhau nhất
trong bộ ba không vượt quá `d`.

Gợi ý: cố định điểm phải nhất `r`, hai điểm còn lại chọn tuỳ ý trong cửa sổ `[l, r-1]`.
""", "Dòng đầu `n, d` (3 ≤ n ≤ 2·10^5, 1 ≤ d ≤ 10^9). Dòng sau là `n` toạ độ tăng ngặt.", "Số bộ ba.",
    ["4 3\n1 2 3 4\n"], _g, _sol, brute=_br, tags=["hai con trỏ", "tổ hợp"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    pr = r.random()
    return lines(J(n, r.randint(0, n)), L("1" if r.random() < pr else "0" for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    l = z = best = 0
    for r_ in range(n):
        z += a[r_] == 0
        while z > k:
            z -= a[l] == 0; l += 1
        best = max(best, r_ - l + 1)
    return best


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return max([j - i for i in range(n) for j in range(i + 1, n + 1) if a[i:j].count(0) <= k] + [0])


add(T, "Chuỗi 1 dài nhất khi được đổi k số 0", 3, """
Cho dãy gồm các số 0 và 1. Bạn được đổi tối đa `k` số 0 thành số 1. Tìm độ dài lớn nhất của đoạn liên tiếp toàn số 1 có thể đạt được.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 0 ≤ k ≤ n). Dòng sau `n` số 0/1.", "Độ dài lớn nhất.",
    ["8 2\n1 0 1 1 0 0 1 1\n"], _g, _sol, brute=_br, tags=["hai con trỏ"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 10**5)
    hi = S(s, 20, 10**9)
    return lines(J(n, m, r.randint(1, 2 * hi)), L(arr(r, n, 1, hi)), L(arr(r, m, 1, hi)))


def _sol(s):
    rd = Rd(s); n, m, x = rd.ints(3); a = sorted(rd.ints(n)); b = sorted(rd.ints(m))
    i, j, best = 0, m - 1, 10**19
    while i < n and j >= 0:
        v = a[i] + b[j]
        best = min(best, abs(v - x))
        if v < x:
            i += 1
        else:
            j -= 1
    return best


def _br(s):
    rd = Rd(s); n, m, x = rd.ints(3); a = rd.ints(n); b = rd.ints(m)
    return min(abs(p + q - x) for p in a for q in b)


add(T, "Tổng gần x nhất", 3, """
Cho hai dãy `a` (độ dài `n`) và `b` (độ dài `m`) cùng số `x`. Chọn `a_i` và `b_j` sao cho `|a_i + b_j - x|` nhỏ nhất; in giá trị nhỏ nhất đó.
""", "Dòng đầu `n, m, x` (1 ≤ n, m ≤ 10^5, 1 ≤ x ≤ 2·10^9). Hai dòng sau là hai dãy (1 ≤ giá trị ≤ 10^9).", "Giá trị nhỏ nhất.",
    ["3 3 10\n1 4 7\n2 5 8\n"], _g, _sol, brute=_br, tags=["hai con trỏ", "sắp xếp"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    a = arr(r, n, 1, S(s, 10, 10**9))
    tot = sum(a)
    lo = r.randint(1, max(1, tot // r.choice([1, 3, 50, n])))
    return lines(J(n, lo, lo + r.randint(0, tot // 3 + 1)), L(a))


def _count_le(a, x):
    l = cur = tot = 0
    for r_ in range(len(a)):
        cur += a[r_]
        while cur > x:
            cur -= a[l]; l += 1
        tot += r_ - l + 1
    return tot


def _sol(s):
    rd = Rd(s); n, lo, hi = rd.ints(3); a = rd.ints(n)
    return _count_le(a, hi) - _count_le(a, lo - 1)


def _br(s):
    rd = Rd(s); n, lo, hi = rd.ints(3); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if lo <= sum(a[i:j]) <= hi)


add(T, "Đếm đoạn có tổng trong [L, R]", 4, """
Cho dãy `n` số dương. Đếm số đoạn con liên tiếp có tổng nằm trong đoạn `[L, R]`.

Gợi ý: `đếm(tổng ≤ R) - đếm(tổng ≤ L-1)`.
""", "Dòng đầu `n, L, R` (1 ≤ n ≤ 2·10^5, 1 ≤ L ≤ R ≤ 10^18). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số đoạn.",
    ["5 3 6\n1 2 3 4 5\n"], _g, _sol, brute=_br, tags=["hai con trỏ"])


# 21 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return _atmost(a, k) - _atmost(a, k - 1)


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if len(set(a[i:j])) == k)


add(T, "Đếm đoạn có đúng k giá trị phân biệt", 4, """
Đếm số đoạn con liên tiếp có **đúng** `k` giá trị khác nhau.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 2·10^5).", "Số đoạn.",
    ["5 2\n1 2 1 2 3\n"], _gk, _sol, brute=_br, tags=["hai con trỏ", "đếm tần suất"])


# 22 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    k = r.randint(1, min(n, S(s, 3, 1000)))
    a = arr(r, n, 1, k)
    for v in range(1, k + 1):
        if r.random() < .97:
            a[r.randrange(n)] = v
    return lines(J(n, k), L(a))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    if len(set(a)) < k:
        return -1
    b = a + a
    cnt = [0] * (k + 1); have = l = 0; best = n
    for r_ in range(2 * n):
        cnt[b[r_]] += 1
        if cnt[b[r_]] == 1:
            have += 1
        while have == k:
            best = min(best, r_ - l + 1)
            cnt[b[l]] -= 1
            if cnt[b[l]] == 0:
                have -= 1
            l += 1
    return best


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    if len(set(a)) < k:
        return -1
    best = n
    for i in range(n):
        seen = set()
        for ln in range(1, n + 1):
            seen.add(a[(i + ln - 1) % n])
            if len(seen) == k:
                best = min(best, ln); break
    return best


add(T, "Vòng hạt đủ màu", 5, """
Một vòng cổ có `n` hạt xếp thành **vòng tròn**, hạt `i` có màu `a_i ∈ [1, k]`. Tìm số hạt ít nhất của một đoạn liên tiếp
trên vòng tròn chứa đủ cả `k` màu. In `-1` nếu vòng cổ không có đủ `k` màu.

Gợi ý: nhân đôi dãy để xử lý vòng tròn, rồi áp dụng cửa sổ trượt như bài "đoạn ngắn nhất chứa đủ 1..k".
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 10^5). Dòng sau `n` số (1 ≤ a_i ≤ k).", "Số hạt ít nhất hoặc `-1`.",
    ["6 3\n1 2 2 2 3 1\n", "3 3\n1 1 2\n"], _g, _sol, brute=_br, tags=["hai con trỏ", "vòng tròn"])
