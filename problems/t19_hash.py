"""Chuyên đề 19: Hash (băm xâu), so khớp xâu, Z-function, Manacher."""
from collections import Counter
from .base import add, Rd, S, J, L, arr, lines, rstr, rtree

T = 19
AL = "abcdefghijklmnopqrstuvwxyz"


def _alpha(r):
    return AL[:r.choice([1, 2, 3, 26])]


def zfunc(s):
    n = len(s); z = [0] * n; l = r = 0
    if n:
        z[0] = n
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def prefix_func(s):
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def occurrences(text, pat):
    z = zfunc(pat + "\x00" + text); m = len(pat)
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] >= m]


def manacher(s):
    t = "^#" + "#".join(s) + "#$"
    p = [0] * len(t); c = r = 0
    for i in range(1, len(t) - 1):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    return p


class Hasher:
    M = (1 << 61) - 1

    def __init__(self, s, base=911382323):
        M = self.M
        self.h = [0] * (len(s) + 1); self.p = [1] * (len(s) + 1)
        for i, c in enumerate(s):
            v = c if isinstance(c, int) else ord(c)
            self.h[i + 1] = (self.h[i] * base + v + 1) % M
            self.p[i + 1] = self.p[i] * base % M

    def get(self, l, r):  # [l, r)
        return (self.h[r] - self.h[l] * self.p[r - l]) % self.M


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5); al = _alpha(r)
    ln = max(1, min(20, 2 * 10**5 // n))
    return lines(str(n), *(rstr(r, r.randint(1, ln), al) for _ in range(n)))


add(T, "Đếm xâu phân biệt", 1, """
Cho `n` xâu. Có bao nhiêu xâu khác nhau?

Gợi ý: đưa vào `set<string>`, hoặc băm mỗi xâu thành một số (hash đa thức) rồi đếm số giá trị khác nhau.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau mỗi dòng một xâu chữ thường (tổng độ dài ≤ 2·10^5).", "Số xâu phân biệt.",
    ["4\nab\nba\nab\nc\n"], _g, lambda s: len(set(s.split()[1:])), tags=["hash", "set"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    al = _alpha(r)
    t = rstr(r, S(s, 1, 10**6), al)
    p = rstr(r, r.randint(1, max(1, min(len(t), S(s, 1, 1000)))), al)
    return lines(t, p)


add(T, "Đếm số lần xuất hiện", 1, """
Đếm số lần xâu mẫu `p` xuất hiện trong văn bản `t` (các lần xuất hiện có thể chồng lên nhau).

Gợi ý (hash lăn - rolling hash): `H(t[i..i+m)) = (h[i+m] - h[i]·B^m) mod M`. So sánh với `H(p)` trong `O(1)` cho mỗi vị trí.
(Hoặc dùng KMP / Z-function.)
""", "Dòng đầu là `t` (1 ≤ |t| ≤ 10^6). Dòng hai là `p` (1 ≤ |p| ≤ |t|).", "Số lần xuất hiện.",
    ["saippuakauppias\npp\n", "aaaaa\naa\n"], _g, lambda s: len(occurrences(*s.split())),
    brute=lambda s: (lambda t, p: sum(1 for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p))(*s.split()),
    tags=["hash", "so khớp xâu"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    al = AL[:r.choice([1, 2])] if r.random() < .5 else _alpha(r)
    t = rstr(r, n, al)
    qs = []
    for _ in range(q):
        ln = r.randint(1, max(1, n // r.choice([1, 10, 100])))
        a = r.randint(1, n - ln + 1); b = r.randint(1, n - ln + 1)
        qs.append(J(a, a + ln - 1, b, b + ln - 1))
    return lines(J(n, q), t, *qs)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str(); h = Hasher(t); out = []
    for _ in range(q):
        a, b, c, d = rd.ints(4)
        out.append("YES" if h.get(a - 1, b) == h.get(c - 1, d) else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str(); out = []
    for _ in range(q):
        a, b, c, d = rd.ints(4); out.append("YES" if t[a - 1:b] == t[c - 1:d] else "NO")
    return out


add(T, "So sánh xâu con", 2, """
Cho xâu `s` và `q` truy vấn `(a, b, c, d)` (hai đoạn cùng độ dài): `s[a..b]` có bằng `s[c..d]` không?

Gợi ý: tính hash tiền tố một lần, mỗi truy vấn so sánh hai hash trong `O(1)`. Dùng modulo lớn (ví dụ `2^61 - 1`) hoặc hai modulo
để tránh va chạm (đặc biệt là với test chống hash!).
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai là xâu `s`. `q` dòng sau mỗi dòng `a b c d`.", "Mỗi truy vấn in `YES`/`NO`.",
    ["7 3\nabacaba\n1 3 5 7\n1 2 3 4\n2 2 6 6\n"], _g, _sol, brute=_br, tags=["hash"])


# 4 -----------------------------------------------------------------------
def _gs(r, s):
    n = S(s, 1, 10**6)
    if r.random() < .5:
        base = rstr(r, r.randint(1, 10), _alpha(r))
        t = (base * (n // len(base) + 1))[:n]
        if r.random() < .3:
            i = r.randrange(n); t = t[:i] + r.choice(AL[:3]) + t[i + 1:]
        return t
    return rstr(r, n, AL[:r.choice([1, 2, 26])])


def _sol(s):
    t = s.split()[0]; n = len(t); z = zfunc(t)
    return L(p for p in range(1, n + 1) if p == n or z[p] == n - p)


def _br(s):
    t = s.split()[0]; n = len(t)
    return L(p for p in range(1, n + 1) if all(t[i] == t[i % p] for i in range(n)))


add(T, "Các chu kỳ của xâu", 3, """
Số `p` là **chu kỳ** của xâu `s` nếu `s` là tiền tố của xâu `s[1..p]` lặp lại vô hạn lần (tức `s_i = s_{i+p}` với mọi `i`).
In tất cả các chu kỳ theo thứ tự tăng dần.

Gợi ý: `p` là chu kỳ ⇔ `s[p..n)` bằng tiền tố độ dài `n - p` — kiểm tra bằng hash hoặc Z-function (`z[p] = n - p`).
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^6).", "Một dòng các chu kỳ.", ["abcababcab\n"], _gs, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 2000 else _sol(s), tags=["hash", "Z-function"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    t = s.split()[0]; n = len(t); z = zfunc(t)
    return L(k for k in range(1, n) if z[n - k] == k)


add(T, "Các biên của xâu", 3, """
**Biên** của xâu là một xâu con vừa là tiền tố vừa là hậu tố (và ngắn hơn chính xâu đó). In độ dài tất cả các biên theo thứ tự tăng dần
(in dòng trống nếu không có).

Gợi ý: so sánh hash tiền tố và hậu tố cùng độ dài; hoặc dùng hàm tiền tố KMP: các biên là `π[n-1], π[π[n-1]-1], ...`.
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^6).", "Một dòng các độ dài.", ["abcababcab\n"], _gs, _sol,
    brute=lambda s: (lambda t: L(k for k in range(1, len(t)) if t[:k] == t[-k:]))(s.split()[0]) if len(s.split()[0]) <= 3000 else _sol(s),
    tags=["hash", "KMP"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n)), rstr(r, n, _alpha(r)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); t = rd.str(); h = Hasher(t)
    return len({h.get(i, i + k) for i in range(n - k + 1)})


add(T, "Xâu con phân biệt độ dài k", 2, """
Đếm số xâu con (liên tiếp) **khác nhau** có độ dài đúng `k`.

Gợi ý: hash `n - k + 1` xâu con bằng hash lăn rồi đếm số giá trị khác nhau (sắp xếp hoặc `unordered_set`).
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng hai là xâu.", "Số xâu con phân biệt.",
    ["7 3\nabacaba\n"], _g, _sol,
    brute=lambda s: (lambda rd: (lambda n, k: (lambda t: len({t[i:i + k] for i in range(n - k + 1)}))(rd.str()))(*rd.ints(2)))(Rd(s)),
    tags=["hash"])


# 7 -----------------------------------------------------------------------
def _gp(r, s):
    n = S(s, 1, 10**6)
    al = AL[:r.choice([1, 2, 3, 26])]
    if r.random() < .4:
        half = rstr(r, n // 2, al); t = half + r.choice(["", r.choice(al)]) + half[::-1]
        t = rstr(r, r.randint(0, 5), al) + t
        return (t or r.choice(al))[:max(1, n)]
    return rstr(r, n, al)


def _sol(s):
    t = s.split()[0]; p = manacher(t)
    return max(p[1:-1])


def _br(s):
    t = s.split()[0]; n = len(t)
    return max(j - i for i in range(n) for j in range(i + 1, n + 1) if t[i:j] == t[i:j][::-1])


add(T, "Xâu con đối xứng dài nhất", 3, """
Tìm độ dài xâu con liên tiếp dài nhất đọc xuôi ngược như nhau.

Gợi ý: với mỗi tâm, tìm kiếm nhị phân bán kính lớn nhất bằng cách so sánh hash xuôi và hash ngược — `O(n log n)`.
(Thuật toán Manacher giải trong `O(n)`.)
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^6).", "Độ dài lớn nhất.", ["babad\n", "aaaa\n"], _gp, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 300 else _sol(s), tags=["hash", "Manacher", "xâu đối xứng"])


# 8 -----------------------------------------------------------------------
def _sol(s):
    p = manacher(s.split()[0])
    return sum((x + 1) // 2 for x in p[1:-1])


def _br(s):
    t = s.split()[0]; n = len(t)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if t[i:j] == t[i:j][::-1])


add(T, "Đếm xâu con đối xứng", 3, """
Đếm số cặp `(l, r)` mà xâu con `s[l..r]` đối xứng.

Gợi ý: với mỗi tâm (ký tự hoặc khe giữa hai ký tự), số xâu đối xứng có tâm đó bằng bán kính lớn nhất (tìm bằng hash + nhị phân, hoặc Manacher).
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^6).", "Số xâu con đối xứng (vừa `long long`).", ["aaa\n", "abc\n"], _gp, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 200 else _sol(s), tags=["hash", "Manacher"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    al = _alpha(r)
    a = rstr(r, S(s, 1, 10**5), al); b = rstr(r, S(s, 1, 10**5), al)
    if r.random() < .5 and len(a) > 2:
        i = r.randrange(len(a)); j = r.randrange(i, len(a)); k = r.randrange(len(b) + 1)
        b = (b[:k] + a[i:j + 1] + b[k:])[:10**5]
    return lines(a, b)


def _lcsub(a, b):
    ha, hb = Hasher(a), Hasher(b)

    def ok(k):
        if k == 0:
            return True
        seen = {ha.get(i, i + k) for i in range(len(a) - k + 1)}
        return any(hb.get(i, i + k) in seen for i in range(len(b) - k + 1))
    lo, hi = 0, min(len(a), len(b))
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(m):
            lo = m
        else:
            hi = m - 1
    return lo


def _br(s):
    a, b = s.split()
    return max([k for k in range(1, min(len(a), len(b)) + 1) if any(a[i:i + k] in b for i in range(len(a) - k + 1))] + [0])


add(T, "Xâu con chung dài nhất", 3, """
Tìm độ dài xâu con **liên tiếp** dài nhất xuất hiện trong cả hai xâu `a` và `b`.

Gợi ý: nếu có xâu chung độ dài `k` thì có xâu chung độ dài `k - 1` → tìm kiếm nhị phân `k`. Kiểm tra: đưa hash mọi xâu con độ dài `k` của `a`
vào tập, rồi kiểm tra các xâu con của `b`. Độ phức tạp `O((n + m) log)`.
""", "Hai dòng là hai xâu (độ dài 1..10^5).", "Độ dài lớn nhất.", ["xabcdy\nzzbcdabc\n"], _g, lambda s: _lcsub(*s.split()),
    brute=lambda s: _br(s) if sum(map(len, s.split())) <= 200 else _lcsub(*s.split()), tags=["hash", "tìm kiếm nhị phân"])


# 10 ----------------------------------------------------------------------
def _sol(s):
    t = s.split()[0]; n = len(t); tt = t + t
    # thuật toán Booth tìm vị trí xoay nhỏ nhất
    f = [-1] * (2 * n); k = 0
    for j in range(1, 2 * n):
        sj = tt[j]; i = f[j - k - 1]
        while i != -1 and sj != tt[k + i + 1]:
            if sj < tt[k + i + 1]:
                k = j - i - 1
            i = f[i]
        if sj != tt[k + i + 1]:
            if sj < tt[k]:
                k = j
            f[j - k] = -1
        else:
            f[j - k] = i + 1
    return tt[k:k + n]


add(T, "Phép xoay nhỏ nhất", 4, """
Phép xoay một xâu là chuyển một số ký tự đầu xuống cuối (ví dụ `abc → bca → cab`). Tìm phép xoay nhỏ nhất theo thứ tự từ điển.

Gợi ý: so sánh hai phép xoay bằng hash: tìm độ dài tiền tố chung dài nhất (nhị phân + hash trên `s + s`) rồi so ký tự tiếp theo.
Duyệt mọi phép xoay giữ ứng viên nhỏ nhất → `O(n log n)`. (Thuật toán Booth / Duval cho `O(n)`.)
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^6).", "Phép xoay nhỏ nhất.", ["acab\n", "bbb\n"], _gs, _sol,
    brute=lambda s: (lambda t: min(t[i:] + t[:i] for i in range(len(t))))(s.split()[0]) if len(s.split()[0]) <= 2000 else _sol(s),
    tags=["hash", "xoay vòng"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    al = AL[:r.choice([2, 3, 26])]
    t = rstr(r, S(s, 1, 10**5), al)
    q = S(s, 1, 10**4)
    pats = []
    for _ in range(q):
        if r.random() < .6 and len(t) >= 1:
            ln = r.randint(1, min(len(t), 30)); i = r.randint(0, len(t) - ln); pats.append(t[i:i + ln])
        else:
            pats.append(rstr(r, r.randint(1, 30), al))
    return lines(t, str(q), *pats)


def _sol(s):
    tok = s.split(); t = tok[0]; q = int(tok[1]); pats = tok[2:2 + q]
    h = Hasher(t); out = []; cache = {}
    for p in pats:
        k = len(p)
        if k > len(t):
            out.append(0); continue
        if k not in cache:
            cache[k] = Counter(h.get(i, i + k) for i in range(len(t) - k + 1))
        out.append(cache[k].get(Hasher(p).get(0, k), 0))
    return out


def _br(s):
    tok = s.split(); t = tok[0]; q = int(tok[1])
    return [sum(1 for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p) for p in tok[2:2 + q]]


add(T, "Nhiều mẫu", 3, """
Cho văn bản `t` và `q` mẫu (mỗi mẫu dài không quá 30). Với mỗi mẫu, đếm số lần xuất hiện trong `t`.

Gợi ý: chỉ có tối đa 30 độ dài khác nhau. Với mỗi độ dài `k`, đếm tần suất hash của mọi xâu con độ dài `k` của `t` (lưu vào `map`) một lần,
rồi trả lời các mẫu cùng độ dài.
""", "Dòng đầu là `t` (1 ≤ |t| ≤ 10^5). Dòng hai là `q` (1 ≤ q ≤ 10^4). `q` dòng sau là các mẫu (1 ≤ độ dài ≤ 30).",
    "Mỗi mẫu in một dòng.", ["abababa\n3\naba\nb\nabc\n"], _g, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["hash"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    return _gs(r, min(s, .1))


def _sol(s):
    t = s.split()[0]; n = len(t); h = Hasher(t)

    def ok(k):
        seen = set()
        for i in range(n - k + 1):
            v = h.get(i, i + k)
            if v in seen:
                return True
            seen.add(v)
        return False
    lo, hi = 0, n - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(m):
            lo = m
        else:
            hi = m - 1
    return lo


def _br(s):
    t = s.split()[0]; n = len(t)
    for k in range(n - 1, 0, -1):
        c = Counter(t[i:i + k] for i in range(n - k + 1))
        if max(c.values()) >= 2:
            return k
    return 0


add(T, "Xâu con lặp lại dài nhất", 4, """
Tìm độ dài xâu con dài nhất xuất hiện **ít nhất hai lần** trong `s` (hai lần xuất hiện có thể chồng nhau). In 0 nếu không có.

Gợi ý: tìm kiếm nhị phân độ dài + hash (kiểm tra trùng hash trong `n - k + 1` xâu con).
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^5).", "Độ dài lớn nhất.", ["banana\n", "abc\n"], _g, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 300 else _sol(s), tags=["hash", "tìm kiếm nhị phân"])


# 13 ----------------------------------------------------------------------
def _sol_fast(s):
    t = s.split()[0]; n = len(t); h = Hasher(t); tot = 0
    for k in range(1, n + 1):
        tot += len({h.get(i, i + k) for i in range(n - k + 1)})
    return tot


add(T, "Số xâu con phân biệt", 4, """
Đếm số xâu con (liên tiếp, khác rỗng) **khác nhau** của `s`.

Gợi ý: với mỗi độ dài `k`, đếm số hash khác nhau của các xâu con độ dài `k` — tổng `O(n²)` (đủ với `n ≤ 2000`).
(Với `n` lớn cần mảng hậu tố / automaton hậu tố.)
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 2000).", "Số xâu con phân biệt.", ["abab\n", "aaa\n"],
    lambda r, s: rstr(r, S(s, 1, 2000), AL[:r.choice([1, 2, 3, 26])]), _sol_fast,
    brute=lambda s: len({s.split()[0][i:j] for i in range(len(s.split()[0])) for j in range(i + 1, len(s.split()[0]) + 1)})
    if len(s.split()[0]) <= 300 else _sol_fast(s), tags=["hash"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    al = AL[:r.choice([2, 3, 26])]
    t = rstr(r, S(s, 1, 10**6), al)
    p = rstr(r, r.randint(1, max(1, min(len(t), S(s, 1, 1000)))), al)
    if r.random() < .5 and len(p) <= len(t):
        i = r.randint(0, len(t) - len(p)); seg = list(t[i:i + len(p)]); r.shuffle(seg); p = "".join(seg)
    return lines(t, p)


def _sol2(s):
    t, p = s.split(); m = len(p)
    if m > len(t):
        return 0
    need = [0] * 26; cur = [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    for c in t[:m]:
        cur[ord(c) - 97] += 1
    diff = sum(1 for i in range(26) if cur[i] != need[i]); cnt = int(diff == 0)
    for i in range(m, len(t)):
        for c, dlt in ((ord(t[i]) - 97, 1), (ord(t[i - m]) - 97, -1)):
            if cur[c] == need[c]:
                diff += 1
            cur[c] += dlt
            if cur[c] == need[c]:
                diff -= 1
        cnt += diff == 0
    return cnt


add(T, "Hoán vị của mẫu", 2, """
Đếm số vị trí `i` sao cho xâu con `t[i..i+|p|)` là một **hoán vị** (đảo chữ) của `p`.

Gợi ý: cửa sổ trượt độ dài `|p|`, giữ bảng đếm 26 chữ cái và số chữ cái đang "lệch" so với `p`.
(Hash kiểu tổng `Σ f(c)` với `f` ngẫu nhiên cũng giải được.)
""", "Dòng đầu là `t` (1 ≤ |t| ≤ 10^6). Dòng hai là `p` (1 ≤ |p| ≤ 1000).", "Số vị trí.",
    ["cbaebabacd\nabc\n"], _g, _sol2,
    brute=lambda s: (lambda t, p: sum(1 for i in range(len(t) - len(p) + 1) if sorted(t[i:i + len(p)]) == sorted(p)))(*s.split())
    if len(s.split()[0]) * len(s.split()[1]) <= 10**6 else _sol2(s), tags=["cửa sổ trượt", "hash"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 300), S(s, 1, 300)
    a, b = r.randint(1, n), r.randint(1, m)
    al = AL[:r.choice([1, 2, 3])]
    big = [rstr(r, m, al) for _ in range(n)]
    small = [rstr(r, b, al) for _ in range(a)]
    if r.random() < .5:
        x, y = r.randint(0, n - a), r.randint(0, m - b)
        small = [big[x + i][y:y + b] for i in range(a)]
    return lines(J(n, m), *big, J(a, b), *small)


def _sol(s):
    tok = s.split(); n, m = int(tok[0]), int(tok[1]); big = tok[2:2 + n]
    a, b = int(tok[2 + n]), int(tok[3 + n]); small = tok[4 + n:4 + n + a]
    M = (1 << 61) - 1; B1, B2 = 131, 137
    # hash theo hàng (độ dài b) cho mỗi hàng của bảng lớn
    rowh = []
    pb = pow(B1, b, M)
    for row in big:
        h = 0; hs = []
        for j, c in enumerate(row):
            h = (h * B1 + ord(c)) % M
            if j >= b:
                h = (h - ord(row[j - b]) * pb) % M
            if j >= b - 1:
                hs.append(h)
        rowh.append(hs)
    target = 0
    for row in small:
        h = 0
        for c in row:
            h = (h * B1 + ord(c)) % M
        target = (target * B2 + h) % M
    pa = pow(B2, a, M); cnt = 0
    for j in range(m - b + 1):
        h = 0
        for i in range(n):
            h = (h * B2 + rowh[i][j]) % M
            if i >= a:
                h = (h - rowh[i - a][j] * pa) % M
            if i >= a - 1 and h == target:
                cnt += 1
    return cnt


def _br(s):
    tok = s.split(); n, m = int(tok[0]), int(tok[1]); big = tok[2:2 + n]
    a, b = int(tok[2 + n]), int(tok[3 + n]); small = tok[4 + n:4 + n + a]
    return sum(1 for x in range(n - a + 1) for y in range(m - b + 1) if all(big[x + i][y:y + b] == small[i] for i in range(a)))


add(T, "Tìm ảnh con (hash 2D)", 4, """
Cho bảng ký tự lớn `n × m` và bảng mẫu `a × b`. Đếm số vị trí trong bảng lớn mà bảng mẫu khớp hoàn toàn.

Gợi ý (hash 2 chiều): hash lăn theo hàng cho mọi đoạn độ dài `b`, rồi coi mỗi giá trị đó là một "ký tự" và hash lăn theo cột với độ dài `a`
(dùng cơ số khác). Tổng `O(n·m)`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 300), `n` dòng là bảng lớn. Tiếp theo `a, b` (1 ≤ a ≤ n, 1 ≤ b ≤ m) và `a` dòng là bảng mẫu.",
    "Số vị trí khớp.", ["3 4\nabab\nbaba\nabab\n2 2\nab\nba\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 2500 else _sol(s), tags=["hash 2D"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    e1 = rtree(r, n)
    if r.random() < .5:  # cây thứ hai đẳng cấu: hoán vị nhãn nhưng giữ gốc 1
        perm = list(range(2, n + 1)); r.shuffle(perm); perm = [0, 1] + perm
        e2 = [(perm[a], perm[b]) for a, b in e1]; r.shuffle(e2)
    else:
        e2 = rtree(r, n)
    return lines(str(n), *(J(a, b) for a, b in e1), *(J(a, b) for a, b in e2))


def _canon(n, es, ids):
    adj = [[] for _ in range(n + 1)]
    for a, b in es:
        adj[a].append(b); adj[b].append(a)
    par = [0] * (n + 1); order = [1]; par[1] = -1
    for u in order:
        for v in adj[u]:
            if v != par[u]:
                par[v] = u; order.append(v)
    code = [0] * (n + 1); kids = [[] for _ in range(n + 1)]
    for u in reversed(order):
        key = tuple(sorted(kids[u]))
        code[u] = ids.setdefault(key, len(ids))
        if par[u] > 0:
            kids[par[u]].append(code[u])
    return code[1]


def _sol(s):
    rd = Rd(s); n = rd.int()
    e1 = [rd.ints(2) for _ in range(n - 1)]; e2 = [rd.ints(2) for _ in range(n - 1)]
    ids = {}
    return "YES" if _canon(n, e1, ids) == _canon(n, e2, ids) else "NO"


def _br(s):
    from itertools import permutations
    rd = Rd(s); n = rd.int()
    e1 = {frozenset(rd.ints(2)) for _ in range(n - 1)}; e2 = {frozenset(rd.ints(2)) for _ in range(n - 1)}
    if n > 7:
        return _sol(s)
    for p in permutations(range(2, n + 1)):
        mp = dict(zip(range(2, n + 1), p)); mp[1] = 1
        if {frozenset(mp[x] for x in e) for e in e1} == e2:
            return "YES"
    return "NO"


add(T, "Hai cây có gốc đẳng cấu", 4, """
Cho hai cây cùng `n` đỉnh, cả hai đều có gốc là đỉnh 1. Hai cây có **đẳng cấu** không (đổi nhãn các đỉnh, giữ gốc, để cây này thành cây kia)?

Gợi ý (hash cây / AHU): mã của một đỉnh = mã của **multiset đã sắp xếp** các mã con. Đánh số mỗi multiset khác nhau bằng `map<vector<int>, int>`
(dùng chung cho cả hai cây). Hai cây đẳng cấu ⇔ mã gốc bằng nhau.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n - 1` dòng là cạnh cây thứ nhất, `n - 1` dòng tiếp là cạnh cây thứ hai.", "`YES` hoặc `NO`.",
    ["3\n1 2\n2 3\n1 3\n3 2\n", "4\n1 2\n1 3\n1 4\n1 2\n2 3\n2 4\n"], _g, _sol, brute=_br, tags=["hash cây", "đẳng cấu"])


# 17 ----------------------------------------------------------------------
def _sol(s):
    t = s.split()[0]; n = len(t); z = zfunc(t)
    cnt = [0] * (n + 2)
    for i in range(n):
        cnt[z[i]] += 1
    for k in range(n - 1, 0, -1):
        cnt[k] += cnt[k + 1]
    res = [(k, cnt[k]) for k in range(1, n + 1) if z[n - k] == k]
    return lines(str(len(res)), *(J(k, c) for k, c in res)).rstrip("\n")


def _br(s):
    t = s.split()[0]; n = len(t); res = []
    for k in range(1, n + 1):
        if t[:k] == t[n - k:]:
            res.append((k, sum(1 for i in range(n - k + 1) if t[i:i + k] == t[:k])))
    return lines(str(len(res)), *(J(k, c) for k, c in res)).rstrip("\n")


add(T, "Tiền tố và hậu tố", 5, """
Với mỗi tiền tố của `s` đồng thời là hậu tố của `s` (kể cả chính `s`), in độ dài của nó và số lần nó xuất hiện như xâu con trong `s`.
Các dòng in theo độ dài tăng dần.

Gợi ý (Z-function): tiền tố độ dài `k` là hậu tố ⇔ `z[n - k] = k`. Số lần xuất hiện của tiền tố độ dài `k` = số vị trí `i` có `z[i] ≥ k`
→ đếm `z` theo giá trị rồi lấy tổng hậu tố.
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 10^6).", "Dòng đầu là số lượng `k`, `k` dòng sau mỗi dòng `độ_dài số_lần`.",
    ["ABACABA\n", "AAA\n"], lambda r, s: _gs(r, s).upper(), _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 300 else _sol(s), tags=["Z-function", "hash"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    al = AL[:r.choice([1, 2, 26])]
    a = rstr(r, S(s, 1, 10**6), al)
    if r.random() < .6:
        k = r.randint(0, len(a)); b = a[len(a) - k:] + rstr(r, S(s, 1, 10**6) - k if S(s, 1, 10**6) > k else 1, al)
    else:
        b = rstr(r, S(s, 1, 10**6), al)
    return lines(a, b)


def _sol(s):
    a, b = s.split()
    k = min(len(a), len(b))
    z = zfunc(b[:k] + "\x00" + a[len(a) - k:])
    best = 0
    for i in range(k + 1, 2 * k + 1):
        if z[i] == 2 * k + 1 - i:
            best = 2 * k + 1 - i; break
    return len(a) + len(b) - best


def _br(s):
    a, b = s.split()
    return min(len(a) + len(b) - k for k in range(0, min(len(a), len(b)) + 1) if a[len(a) - k:] == b[:k])


add(T, "Ghép xâu chồng nhau", 2, """
Tìm độ dài xâu ngắn nhất có `a` là **tiền tố** và `b` là **hậu tố**.

Gợi ý: cần phần chồng lớn nhất `k`: hậu tố độ dài `k` của `a` bằng tiền tố độ dài `k` của `b` — thử các `k` từ lớn tới nhỏ bằng hash, `O(n)`.
""", "Hai dòng là `a` và `b` (độ dài 1..10^6).", "Độ dài nhỏ nhất.", ["abcab\nabd\n", "aaa\naa\n"], _g, _sol,
    brute=lambda s: _br(s) if sum(map(len, s.split())) <= 3000 else _sol(s), tags=["hash", "Z-function"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    t = _gs(r, min(1.0, s * (2 * 10**5) / 10**6 + 0.0001))[:n]
    n = len(t)
    qs = []
    for _ in range(q):
        a, b = sorted((r.randint(1, n), r.randint(1, n)))
        qs.append(J(a, b, r.randint(1, b - a + 1)))
    return lines(J(n, q), t, *qs)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str(); h = Hasher(t); out = []
    for _ in range(q):
        a, b, d = rd.ints(3); a -= 1
        out.append("YES" if d == b - a or h.get(a, b - d) == h.get(a + d, b) else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); t = rd.str(); out = []
    for _ in range(q):
        a, b, d = rd.ints(3); seg = t[a - 1:b]
        out.append("YES" if all(seg[i] == seg[i + d] for i in range(len(seg) - d)) else "NO")
    return out


add(T, "Truy vấn chu kỳ", 4, """
Với truy vấn `(l, r, d)`: `d` có phải là chu kỳ của xâu con `s[l..r]` không (tức `s_i = s_{i+d}` với mọi `l ≤ i ≤ r - d`)?

Gợi ý: `d` là chu kỳ ⇔ `s[l..r-d] = s[l+d..r]` — so sánh hai hash trong `O(1)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai là xâu. `q` dòng sau mỗi dòng `l r d` (1 ≤ d ≤ r - l + 1).", "Mỗi truy vấn in `YES`/`NO`.",
    ["8 3\nabcabcab\n1 8 3\n1 8 2\n3 5 1\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["hash", "chu kỳ"])


# 20 ----------------------------------------------------------------------
class _HBIT:
    M = (1 << 61) - 1

    def __init__(self, n):
        self.n = n; self.t = [0] * (n + 1)

    def add(self, i, v):
        M = self.M
        while i <= self.n:
            self.t[i] = (self.t[i] + v) % M; i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s % self.M


def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    al = AL[:r.choice([1, 2, 26])]
    t = rstr(r, n, al)
    if r.random() < .5:
        t = (t[:n // 2] + t[:(n + 1) // 2][::-1])[:n]
    ops = []
    for _ in range(q):
        if r.random() < .4:
            ops.append(J(1, r.randint(1, n), r.choice(al)))
        else:
            a = r.randint(1, n); b = r.randint(a, min(n, a + r.choice([5, n])))
            ops.append(J(2, a, b))
    return lines(J(n, q), t, *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); t = list(rd.str())
    M = (1 << 61) - 1; B = 911382323
    pw = [1] * (n + 2)
    for i in range(1, n + 2):
        pw[i] = pw[i - 1] * B % M
    fw, bw = _HBIT(n), _HBIT(n)
    for i, c in enumerate(t):
        fw.add(i + 1, ord(c) * pw[i] % M); bw.add(i + 1, ord(c) * pw[n - 1 - i] % M)
    out = []
    for _ in range(q):
        typ = rd.int()
        if typ == 1:
            k, c = int(rd.str()) - 1, rd.str()
            d = ord(c) - ord(t[k]); t[k] = c
            fw.add(k + 1, d * pw[k] % M); bw.add(k + 1, d * pw[n - 1 - k] % M)
        else:
            a, b = rd.ints(2)
            f = (fw.sum(b) - fw.sum(a - 1)) % M  # = Σ c_i B^i, i ∈ [a-1, b-1]
            g = (bw.sum(b) - bw.sum(a - 1)) % M  # = Σ c_i B^(n-1-i)
            # chuẩn hoá: f · B^(n-b) so với g · B^(a-1)
            out.append("YES" if f * pw[n - b] % M == g * pw[a - 1] % M else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); t = list(rd.str()); out = []
    for _ in range(q):
        typ = rd.int()
        if typ == 1:
            k, c = int(rd.str()) - 1, rd.str(); t[k] = c
        else:
            a, b = rd.ints(2); seg = t[a - 1:b]; out.append("YES" if seg == seg[::-1] else "NO")
    return out


add(T, "Truy vấn đối xứng có cập nhật", 5, """
Cho xâu `s` và các thao tác:
- `1 k c`: đổi ký tự thứ `k` thành `c`;
- `2 a b`: xâu con `s[a..b]` có đối xứng không?

Gợi ý: hai cây Fenwick lưu hash xuôi `Σ s_i·B^i` và hash ngược `Σ s_i·B^(n-1-i)`. Cập nhật một ký tự = cộng hiệu vào hai BIT.
So sánh hai hash sau khi nhân luỹ thừa thích hợp để cùng "bậc".
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai là xâu. `q` dòng sau là các thao tác.", "Kết quả các thao tác loại 2.",
    ["7 5\naybabtu\n2 3 5\n1 3 x\n2 3 5\n1 5 x\n2 3 5\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["hash", "BIT"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    hi = r.choice([2, 5, 10**9])
    a = arr(r, S(s, 1, 10**5), 1, hi); b = arr(r, S(s, 1, 10**5), 1, hi)
    if r.random() < .5 and len(a) > 1:
        i = r.randrange(len(a)); j = r.randrange(i, len(a)); k = r.randrange(len(b) + 1)
        b = (b[:k] + a[i:j + 1] + b[k:])[:10**5]
    return lines(str(len(a)), L(a), str(len(b)), L(b))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); m = rd.int(); b = rd.ints(m)
    return _lcsub(a, b)


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n); m = rd.int(); b = rd.ints(m)
    best = 0
    prev = [0] * (m + 1)
    for i in range(n):
        cur = [0] * (m + 1)
        for j in range(m):
            if a[i] == b[j]:
                cur[j + 1] = prev[j] + 1; best = max(best, cur[j + 1])
        prev = cur
    return best


add(T, "Đoạn chung dài nhất của hai dãy", 3, """
Cho hai dãy số `a` và `b`. Tìm độ dài đoạn con **liên tiếp** dài nhất xuất hiện trong cả hai dãy.

Gợi ý: hash đa thức hoạt động với dãy số giống như với xâu (coi mỗi số là một "ký tự"). Tìm kiếm nhị phân độ dài + tập hash.
""", "Dòng đầu `n`, dòng hai là `a` (1 ≤ n ≤ 10^5). Dòng ba `m`, dòng bốn là `b` (1 ≤ m ≤ 10^5). Giá trị trong `[1, 10^9]`.",
    "Độ dài lớn nhất.", ["5\n1 2 3 2 1\n5\n3 2 1 4 7\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * len(s.split()) <= 10**5 else _sol(s), tags=["hash", "tìm kiếm nhị phân"])
