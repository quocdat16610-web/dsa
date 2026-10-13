"""Chuyên đề 1: Sàng nguyên tố & các bài toán số học."""
from bisect import bisect_right
from functools import lru_cache
from math import gcd, isqrt
from .base import add, Rd, S, J, L, arr, lines

T = 1
MOD = 10**9 + 7


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


@lru_cache(None)
def sieve(n):
    b = bytearray([1]) * (n + 1)
    b[0] = 0
    if n >= 1:
        b[1] = 0
    for i in range(2, isqrt(n) + 1):
        if b[i]:
            b[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return b


@lru_cache(None)
def primes(n):
    b = sieve(n)
    return [i for i in range(n + 1) if b[i]]


@lru_cache(None)
def spf(n):
    sp = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if sp[i] == i:
            for j in range(i * i, n + 1, i):
                if sp[j] == j:
                    sp[j] = i
    return sp


def factor(n):
    f, d = [], 2
    while d * d <= n:
        if n % d == 0:
            k = 0
            while n % d == 0:
                n //= d; k += 1
            f.append((d, k))
        d += 1 if d == 2 else 2
    if n > 1:
        f.append((n, 1))
    return f


def rand_num(r, hi):
    """Số ngẫu nhiên có xen lẫn số nguyên tố, bình phương số nguyên tố, số nhiều ước."""
    c = r.random()
    if c < .45 and hi <= 10**6:
        ps = primes(10**6)
        k = bisect_right(ps, hi)
        if k == 0:
            return 1
        p = ps[r.randrange(k)]
        if c < .3:
            return p
        k2 = bisect_right(ps, isqrt(hi))
        return ps[r.randrange(k2)] ** 2 if k2 else p
    if c < .3:
        x = r.randint(1, hi)
        while not is_prime(x) and x < hi:
            x += 1
        return x if is_prime(x) else 2
    if c < .45:
        p = r.randint(1, isqrt(hi))
        while not is_prime(p):
            p += 1
        return p * p if p * p <= hi else 4
    if c < .6:
        x = 1
        for p in (2, 3, 5, 7, 11, 13):
            while x * p <= hi and r.random() < .6:
                x *= p
        return x
    return r.randint(1, hi)


# 1 -----------------------------------------------------------------------
def _g(r, s):
    t = S(s, 1, 1000)
    xs = [rand_num(r, 10**9) for _ in range(t)]
    if s == 0:
        xs = [1, 2, 3, 4, 561, 1000000007][:t + 5]
    return lines(str(len(xs)), *map(str, xs))


add(T, "Kiểm tra số nguyên tố", 1, """
Cho `T` số nguyên dương. Với mỗi số `n`, hãy cho biết `n` có phải số nguyên tố hay không.

Gợi ý: chỉ cần thử chia `n` cho các số từ 2 đến `√n`.
""", "Dòng đầu là `T` (1 ≤ T ≤ 1000). `T` dòng sau, mỗi dòng một số `n` (1 ≤ n ≤ 10^9).",
    "Với mỗi số in `YES` nếu là số nguyên tố, ngược lại in `NO`.",
    ["4\n1\n2\n9\n13\n"], _g,
    lambda s: ["YES" if is_prime(x) else "NO" for x in Rd(s).t[1:] for x in [int(x)]],
    tags=["nguyên tố"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    a, b = Rd(s).ints(2)
    g = gcd(a, b)
    return J(g, a // g * b)


add(T, "UCLN và BCNN", 1, """
Cho hai số nguyên dương `a` và `b`. Tính ước chung lớn nhất và bội chung nhỏ nhất của chúng.

Gợi ý: thuật toán Euclid `gcd(a, b) = gcd(b, a mod b)`, và `lcm(a, b) = a / gcd(a, b) * b`
(chia trước rồi mới nhân để tránh tràn số).
""", "Một dòng gồm hai số `a`, `b` (1 ≤ a, b ≤ 10^9).",
    "In ra `gcd(a, b)` và `lcm(a, b)` cách nhau một dấu cách.",
    ["12 18\n", "7 5\n"],
    lambda r, s: J(r.randint(1, S(s, 20, 10**9)), r.randint(1, S(s, 20, 10**9))) if r.random() < .5
    else (lambda g: J(g * r.randint(1, 1000), g * r.randint(1, 1000)))(r.randint(1, S(s, 5, 10**6))),
    _sol, tags=["gcd"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    n = Rd(s).int()
    c = 1
    for _, k in factor(n):
        c *= k + 1
    return c


add(T, "Đếm số ước", 1, """
Cho số nguyên dương `n`. Hãy đếm số ước dương của `n`.

Ví dụ: 12 có 6 ước là 1, 2, 3, 4, 6, 12.

Gợi ý: các ước đi theo cặp `(d, n/d)` nên chỉ cần duyệt `d ≤ √n`.
""", "Một số nguyên `n` (1 ≤ n ≤ 10^12).", "Số ước dương của `n`.",
    ["12\n", "1\n"], lambda r, s: str(rand_num(r, S(s, 50, 10**12))), _sol, tags=["ước số"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    n = Rd(s).int()
    return " * ".join(f"{p}^{k}" if k > 1 else str(p) for p, k in factor(n))


add(T, "Phân tích thừa số nguyên tố", 1, """
Cho số nguyên `n ≥ 2`. Hãy phân tích `n` ra thừa số nguyên tố.

In các thừa số theo thứ tự tăng dần, dạng `p1^k1 * p2^k2 * ...`; nếu số mũ bằng 1 thì chỉ in `p`.
Ví dụ `360 = 2^3 * 3^2 * 5`.
""", "Một số nguyên `n` (2 ≤ n ≤ 10^12).", "Dạng phân tích của `n` (các phần cách nhau bởi ` * `).",
    ["360\n", "97\n"], lambda r, s: str(max(2, rand_num(r, S(s, 50, 10**12)))), _sol,
    tags=["phân tích"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    n = Rd(s).int()
    return sum(sieve(n))


add(T, "Đếm số nguyên tố", 1, """
Đếm số lượng số nguyên tố không vượt quá `n`.

Gợi ý: dùng sàng Eratosthenes — với mỗi số nguyên tố `i`, đánh dấu các bội `i*i, i*i+i, ...` là hợp số.
Độ phức tạp `O(n log log n)`.
""", "Một số nguyên `n` (1 ≤ n ≤ 5·10^6).", "Số lượng số nguyên tố ≤ n.",
    ["10\n", "1\n"], lambda r, s: str(S(s, 1, 5 * 10**6) if s < 1 else r.randint(4 * 10**6, 5 * 10**6)),
    _sol, tags=["sàng"])


# 6 -----------------------------------------------------------------------
N6 = 10**6


def _g(r, s):
    q = S(s, 1, 10**5)
    xs = [rand_num(r, S(s, 30, N6)) for _ in range(q)]
    return lines(str(q), L(xs))


add(T, "Truy vấn số nguyên tố", 2, """
Cho `Q` truy vấn, mỗi truy vấn là một số `x`. Với mỗi truy vấn, in `YES` nếu `x` là số nguyên tố, ngược lại in `NO`.

Số truy vấn lớn nên không thể kiểm tra từng số bằng `√x` — hãy sàng trước một lần.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Dòng sau gồm `Q` số `x` (1 ≤ x ≤ 10^6).",
    "In `Q` dòng, mỗi dòng `YES` hoặc `NO`.",
    ["5\n1 2 3 4 5\n"], _g,
    lambda s: (lambda b: ["YES" if b[x] else "NO" for x in Rd(s).ints(int(s.split()[0]) + 1)[1:]])(sieve(N6)),
    tags=["sàng"])


# 7 -----------------------------------------------------------------------
@lru_cache(None)
def pcnt(n):
    b, c, out = sieve(n), 0, [0] * (n + 1)
    for i in range(n + 1):
        c += b[i]
        out[i] = c
    return out


def _g(r, s):
    q = S(s, 1, 10**5)
    m = S(s, 20, N6)
    qs = []
    for _ in range(q):
        a, b = r.randint(1, m), r.randint(1, m)
        qs.append(J(min(a, b), max(a, b)))
    return lines(str(q), *qs)


def _sol(s):
    rd = Rd(s); q = rd.int(); c = pcnt(N6)
    return [c[b] - c[a - 1] for a, b in (rd.ints(2) for _ in range(q))]


add(T, "Số nguyên tố trong đoạn", 2, """
Có `Q` truy vấn, mỗi truy vấn gồm hai số `l, r`. Hãy đếm số số nguyên tố trong đoạn `[l, r]`.

Gợi ý: sàng nguyên tố rồi lập mảng cộng dồn `cnt[i]` = số số nguyên tố ≤ i. Kết quả là `cnt[r] - cnt[l-1]`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Mỗi dòng sau gồm `l, r` (1 ≤ l ≤ r ≤ 10^6).",
    "Với mỗi truy vấn in ra một số trên một dòng.",
    ["3\n1 10\n11 20\n4 4\n"], _g, _sol, tags=["sàng", "tiền tố"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    return lines(str(q), *(J(r.randint(0, 10**18), r.randint(0, S(s, 10, 10**18))) for _ in range(q)))


def _sol(s):
    rd = Rd(s); q = rd.int()
    return [pow(a, b, MOD) for a, b in (rd.ints(2) for _ in range(q))]


add(T, "Luỹ thừa nhanh", 2, """
Cho `Q` truy vấn, mỗi truy vấn gồm `a, b`. Tính `a^b mod (10^9 + 7)`. Quy ước `0^0 = 1`.

Gợi ý: luỹ thừa nhị phân — `a^b = (a^(b/2))^2` (nhân thêm `a` nếu `b` lẻ), độ phức tạp `O(log b)`.
Nhớ lấy `a mod` trước khi nhân để không tràn `long long`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Mỗi dòng sau gồm `a, b` (0 ≤ a, b ≤ 10^18).",
    "Mỗi truy vấn in kết quả trên một dòng.",
    ["3\n2 10\n3 0\n1000000008 2\n"], _g, _sol, tags=["luỹ thừa", "modulo"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    return lines(str(q), L(r.randint(1, MOD - 1) for _ in range(q)))


add(T, "Nghịch đảo modulo", 2, """
Cho `Q` số `a`. Với mỗi số, tìm `x` (0 ≤ x < 10^9+7) sao cho `a·x ≡ 1 (mod 10^9+7)`.

Gợi ý: vì `p = 10^9+7` nguyên tố nên theo định lý Fermat nhỏ, `a^(p-2)` chính là nghịch đảo của `a`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Dòng sau gồm `Q` số `a` (1 ≤ a < 10^9+7).",
    "In `Q` dòng là các nghịch đảo tương ứng.",
    ["3\n1 2 3\n"], _g,
    lambda s: [pow(a, MOD - 2, MOD) for a in list(map(int, s.split()))[1:]], tags=["modulo"])


# 10 ----------------------------------------------------------------------
@lru_cache(None)
def dcount(n):
    d = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            d[j] += 1
    return d


def _sol(s):
    sp, out = spf(N6), []
    for x in list(map(int, s.split()))[1:]:
        c = 1
        while x > 1:
            p, k = sp[x], 0
            while x % p == 0:
                x //= p; k += 1
            c *= k + 1
        out.append(c)
    return out


add(T, "Số ước - nhiều truy vấn", 2, """
Cho `Q` số `x`. Với mỗi số hãy đếm số ước dương của nó.

Gợi ý: sàng "ước nguyên tố nhỏ nhất" `spf[x]`, khi đó phân tích một số chỉ mất `O(log x)`:
lặp `p = spf[x]`, chia `x` cho `p` đến khi hết.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 2·10^5). Dòng sau gồm `Q` số `x` (1 ≤ x ≤ 10^6).",
    "In `Q` dòng, mỗi dòng là số ước của số tương ứng.",
    ["4\n1 12 7 720720\n"],
    lambda r, s: (lambda q: lines(str(q), L(rand_num(r, N6) for _ in range(q))))(S(s, 1, 2 * 10**5)),
    _sol, tags=["sàng", "ước số"])


# 11 ----------------------------------------------------------------------
def _sol(s):
    n = Rd(s).int(); b = sieve(max(n, 2))
    return sum(1 for p in range(2, n - 1) if b[p] and b[p + 2])


add(T, "Cặp số nguyên tố sinh đôi", 3, """
Hai số nguyên tố `p` và `p + 2` gọi là một cặp sinh đôi (ví dụ (3, 5), (5, 7), (11, 13)).
Đếm số cặp sinh đôi mà cả hai số đều không vượt quá `n`.
""", "Một số nguyên `n` (1 ≤ n ≤ 5·10^6).", "Số cặp sinh đôi.",
    ["13\n", "4\n"], lambda r, s: str(S(s, 1, 5 * 10**6) - (r.randint(0, 10) if s else 0)), _sol,
    tags=["sàng"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5)
    g = r.randint(1, 1000)
    a = [g * r.randint(1, 10**6 // g) for _ in range(n)]
    for _ in range(r.randint(0, 2)):
        a[r.randrange(n)] = r.randint(1, 10**6)
    return lines(str(n), L(a))


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    pre, suf = [0] * (n + 1), [0] * (n + 2)
    for i in range(n):
        pre[i + 1] = gcd(pre[i], a[i])
    for i in range(n - 1, -1, -1):
        suf[i + 1] = gcd(suf[i + 2], a[i])
    return max(gcd(pre[i], suf[i + 2]) for i in range(n))


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    best = 0
    for i in range(n):
        g = 0
        for j in range(n):
            if j != i:
                g = gcd(g, a[j])
        best = max(best, g)
    return best


add(T, "Xoá một phần tử để UCLN lớn nhất", 3, """
Cho dãy `a` gồm `n` số nguyên dương. Bạn phải xoá **đúng một** phần tử. Hãy làm sao để UCLN của các phần tử còn lại lớn nhất có thể và in ra giá trị đó.

Gợi ý: UCLN tiền tố `pre[i]` và UCLN hậu tố `suf[i]`; xoá `a[i]` cho kết quả `gcd(pre[i-1], suf[i+1])`.
""", "Dòng đầu `n` (2 ≤ n ≤ 2·10^5). Dòng sau gồm `n` số `a_i` (1 ≤ a_i ≤ 10^6).",
    "UCLN lớn nhất đạt được.", ["3\n12 15 18\n", "2\n7 9\n"], _g, _sol, brute=_br,
    tags=["gcd", "tiền tố"])


# 13 ----------------------------------------------------------------------
@lru_cache(None)
def phis(n):
    ph = list(range(n + 1))
    for i in range(2, n + 1):
        if ph[i] == i:
            for j in range(i, n + 1, i):
                ph[j] -= ph[j] // i
    return ph


add(T, "Hàm phi Euler", 3, """
Hàm `φ(x)` là số các số nguyên trong `[1, x]` nguyên tố cùng nhau với `x`. Ví dụ `φ(9) = 6`.
Cho `Q` số `x`, tính `φ(x)` cho từng số.

Gợi ý: `φ(x) = x · Π (1 - 1/p)` với `p` là các ước nguyên tố của `x`. Có thể sàng phi cho mọi số ≤ 10^6.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 2·10^5). Dòng sau `Q` số `x` (1 ≤ x ≤ 10^6).",
    "In `Q` dòng là giá trị `φ(x)`.", ["4\n1 9 10 13\n"],
    lambda r, s: (lambda q: lines(str(q), L(rand_num(r, N6) for _ in range(q))))(S(s, 1, 2 * 10**5)),
    lambda s: (lambda ph: [ph[x] for x in list(map(int, s.split()))[1:]])(phis(N6)),
    tags=["phi Euler", "sàng"])


# 14 ----------------------------------------------------------------------
@lru_cache(None)
def facts(n):
    f = [1] * (n + 1)
    for i in range(1, n + 1):
        f[i] = f[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(f[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return f, inv


def C(n, k):
    if k < 0 or k > n:
        return 0
    f, inv = facts(10**6)
    return f[n] * inv[k] % MOD * inv[n - k] % MOD


def _g(r, s):
    q = S(s, 1, 10**5)
    m = S(s, 10, 10**6)
    out = []
    for _ in range(q):
        n = r.randint(0, m)
        out.append(J(n, r.randint(0, n + (1 if r.random() < .1 else 0))))
    return lines(str(q), *out)


def _sol(s):
    rd = Rd(s); q = rd.int()
    return [C(n, k) for n, k in (rd.ints(2) for _ in range(q))]


add(T, "Tổ hợp chập k", 3, """
Có `Q` truy vấn `(n, k)`, hãy tính `C(n, k) mod (10^9 + 7)` — số cách chọn `k` phần tử từ `n` phần tử.
Nếu `k > n` thì kết quả là 0.

Gợi ý: tính trước `n!` và `(n!)^(-1)` (nghịch đảo modulo) cho mọi `n ≤ 10^6`, khi đó
`C(n, k) = n! · (k!)^(-1) · ((n-k)!)^(-1)`.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Mỗi dòng sau gồm `n, k` (0 ≤ n ≤ 10^6, 0 ≤ k ≤ n + 1).",
    "Mỗi truy vấn in một dòng.", ["3\n5 2\n10 0\n3 4\n"], _g, _sol, tags=["tổ hợp", "modulo"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    ps = primes(10**6)
    xs = []
    for _ in range(q):
        if r.random() < .4:
            p = ps[r.randrange(len(ps))] if s > .3 else r.choice(ps[:50])
            xs.append(p * p)
        else:
            xs.append(r.randint(1, S(s, 100, 10**12)))
    return lines(str(q), L(xs))


def _sol(s):
    b = sieve(10**6)
    out = []
    for x in list(map(int, s.split()))[1:]:
        t = isqrt(x)
        out.append("YES" if t * t == x and b[t] else "NO")
    return out


add(T, "Số T-prime", 3, """
Một số nguyên dương gọi là **T-prime** nếu nó có đúng 3 ước dương. Ví dụ 4 có ba ước 1, 2, 4 nên là T-prime.
Cho `Q` số, với mỗi số hãy cho biết nó có phải T-prime không.

Gợi ý: số có đúng 3 ước khi và chỉ khi nó là bình phương của một số nguyên tố.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Dòng sau gồm `Q` số `x` (1 ≤ x ≤ 10^12).",
    "Mỗi số in `YES` hoặc `NO` trên một dòng.", ["3\n4 5 6\n"], _g, _sol, tags=["sàng"])


# 16 ----------------------------------------------------------------------
@lru_cache(None)
def omega_pref():
    n = N6
    om = bytearray(n + 1)
    for p in primes(n):
        for j in range(p, n + 1, p):
            om[j] += 1
    pref = [[0] * (n + 1) for _ in range(8)]
    for k in range(8):
        c, row = 0, pref[k]
        for i in range(1, n + 1):
            if om[i] == k:
                c += 1
            row[i] = c
    return pref


def _g(r, s):
    q = S(s, 1, 10**5)
    return lines(str(q), *(J(r.randint(1, S(s, 50, N6)), r.choice([0, 1, 1, 2, 2, 3, 4, 7])) for _ in range(q)))


def _sol(s):
    rd = Rd(s); q = rd.int(); pr = omega_pref()
    return [pr[k][n] for n, k in (rd.ints(2) for _ in range(q))]


add(T, "Số có đúng K ước nguyên tố", 3, """
Có `Q` truy vấn `(n, k)`. Với mỗi truy vấn, đếm số số nguyên `x` thoả `1 ≤ x ≤ n` và `x` có **đúng `k` ước nguyên tố phân biệt**.
(Số 1 có 0 ước nguyên tố; 12 = 2²·3 có 2 ước nguyên tố phân biệt.)
""", "Dòng đầu `Q` (1 ≤ Q ≤ 10^5). Mỗi dòng sau gồm `n, k` (1 ≤ n ≤ 10^6, 0 ≤ k ≤ 7).",
    "Mỗi truy vấn in một dòng.", ["3\n10 1\n10 2\n30 3\n"], _g, _sol, tags=["sàng", "tiền tố"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    hi = r.randint(1, S(s, 100, 10**12))
    lo = max(1, hi - S(s, 50, 10**6) + 1) if r.random() < .8 else r.randint(1, hi)
    if hi - lo > 10**6:
        lo = hi - 10**6
    return J(lo, hi)


def _sol(s):
    lo, hi = Rd(s).ints(2)
    seg = bytearray([1]) * (hi - lo + 1)
    for p in primes(isqrt(hi) + 1):
        st = max(p * p, (lo + p - 1) // p * p)
        if st > hi:
            continue
        seg[st - lo::p] = bytearray(len(range(st, hi + 1, p)))
    if lo == 1:
        seg[0] = 0
    return sum(seg)


add(T, "Sàng trên đoạn", 4, """
Đếm số số nguyên tố trong đoạn `[L, R]`. Lưu ý `R` có thể tới `10^12` nên không thể sàng từ 1 đến `R`.

Gợi ý (sàng đoạn): sàng các số nguyên tố `p ≤ √R`, sau đó với mỗi `p` gạch bỏ các bội của `p` nằm trong `[L, R]`
(bắt đầu từ `max(p·p, ⌈L/p⌉·p)`). Mảng đánh dấu chỉ cần `R - L + 1` phần tử.
""", "Một dòng gồm `L, R` (1 ≤ L ≤ R ≤ 10^12, R - L ≤ 10^6).", "Số số nguyên tố trong đoạn.",
    ["1 10\n", "100 200\n"], _g, _sol, tags=["sàng đoạn"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    ps = primes(100)
    k = S(s, 1, 15)
    chosen = sorted(r.sample(ps, k))
    return lines(J(r.randint(1, S(s, 1000, 10**18)), k), L(chosen))


def _sol(s):
    return _ie(s)


def _ie(s):
    rd = Rd(s); n, k = rd.ints(2); p = rd.ints(k)
    tot = 0
    for mask in range(1, 1 << k):
        prod, bits = 1, 0
        for i in range(k):
            if mask >> i & 1:
                prod *= p[i]; bits += 1
                if prod > n:
                    break
        if prod <= n:
            tot += n // prod if bits % 2 else -(n // prod)
    return tot


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); p = rd.ints(k)
    return sum(1 for x in range(1, n + 1) if any(x % q == 0 for q in p)) if n <= 10**5 else _ie(s)


add(T, "Bao hàm - loại trừ", 4, """
Cho `n` và `k` số nguyên tố phân biệt `p_1, ..., p_k`. Đếm số số nguyên trong `[1, n]` chia hết cho **ít nhất một** trong các `p_i`.

Gợi ý: nguyên lý bao hàm - loại trừ: duyệt mọi tập con khác rỗng (bitmask), cộng `n / tích` nếu tập con có lẻ phần tử, trừ nếu chẵn.
Cẩn thận tích có thể vượt `10^18` — dừng sớm khi tích đã lớn hơn `n`.
""", "Dòng đầu gồm `n, k` (1 ≤ n ≤ 10^18, 1 ≤ k ≤ 15). Dòng sau gồm `k` số nguyên tố phân biệt nhỏ hơn 100.",
    "Một số duy nhất là đáp án.", ["10 2\n2 3\n"], _g, _sol, brute=_br, tags=["bao hàm loại trừ", "bitmask"])


# 19 ----------------------------------------------------------------------
def _sol(s):
    n = Rd(s).int()
    # sum_{d | n} d * phi(n / d)  -- hàm nhân tính: với p^k: (k+1)p^k - k p^(k-1)
    res = 1
    for p, k in factor(n):
        res *= (k + 1) * p**k - k * p**(k - 1)
    return res


def _br(s):
    n = Rd(s).int()
    return sum(gcd(i, n) for i in range(1, n + 1))


add(T, "Tổng UCLN", 4, """
Cho `n`, tính `gcd(1, n) + gcd(2, n) + ... + gcd(n, n)`.

Gợi ý: số các `i` có `gcd(i, n) = d` đúng bằng `φ(n/d)`. Vậy kết quả là `Σ_{d | n} d · φ(n/d)`.
""", "Một số nguyên `n` (1 ≤ n ≤ 10^12).", "Kết quả (vừa kiểu `long long`).",
    ["6\n", "1\n"], lambda r, s: str(rand_num(r, S(s, 30, 10**12))), _sol, brute=_br,
    tags=["phi Euler", "gcd"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 100)
    xs = [2 * r.randint(2, S(s, 10, 5 * 10**5)) for _ in range(q)]
    return lines(str(q), L(xs))


def _sol(s):
    b = sieve(N6); ps = primes(N6)
    out = []
    for n in list(map(int, s.split()))[1:]:
        c = 0
        for p in ps:
            if 2 * p > n:
                break
            c += b[n - p]
        out.append(c)
    return out


add(T, "Giả thuyết Goldbach", 4, """
Giả thuyết Goldbach: mọi số chẵn lớn hơn 2 đều viết được thành tổng hai số nguyên tố.
Cho `Q` số chẵn `n`, đếm số cặp `(p, q)` nguyên tố với `p ≤ q` và `p + q = n`.

Ví dụ `10 = 3 + 7 = 5 + 5` nên có 2 cách.
""", "Dòng đầu `Q` (1 ≤ Q ≤ 100). Dòng sau `Q` số chẵn `n` (4 ≤ n ≤ 10^6).",
    "Mỗi số in kết quả trên một dòng.", ["3\n4 10 100\n"], _g, _sol, tags=["sàng"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5)
    a = arr(r, n, 1, S(s, 10, 10**6))
    if r.random() < .5:
        a = [x * r.choice([1, 2, 6, 30]) % (10**6) + 1 for x in a]
    return lines(str(n), L(a))


@lru_cache(None)
def mobius(n):
    mu = [1] * (n + 1)
    isc = bytearray(n + 1)
    for p in primes(n):
        for j in range(p, n + 1, p):
            mu[j] = -mu[j]
        for j in range(p * p, n + 1, p * p):
            mu[j] = 0
    return mu


def _sol(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    m = max(a)
    cnt = [0] * (m + 1)
    for x in a:
        cnt[x] += 1
    mu = mobius(m)
    tot = 0
    for d in range(1, m + 1):
        if mu[d]:
            c = sum(cnt[d::d])
            tot += mu[d] * c * (c - 1) // 2
    return tot


def _br(s):
    rd = Rd(s); n = rd.int(); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if gcd(a[i], a[j]) == 1)


add(T, "Đếm cặp nguyên tố cùng nhau", 5, """
Cho dãy `a` gồm `n` số. Đếm số cặp chỉ số `i < j` mà `gcd(a_i, a_j) = 1`.

Gợi ý: gọi `c(d)` là số phần tử chia hết cho `d`. Theo công thức nghịch đảo Möbius,
đáp án = `Σ_d μ(d) · c(d)·(c(d)-1)/2`. Tính `c(d)` bằng cách duyệt bội — tổng độ phức tạp `O(M log M)`.
""", "Dòng đầu `n` (2 ≤ n ≤ 10^5). Dòng sau `n` số `a_i` (1 ≤ a_i ≤ 10^6).", "Số cặp thoả mãn.",
    ["4\n1 2 3 4\n", "3\n2 4 6\n"], _g, _sol, brute=_br, tags=["möbius", "đếm"], tl=2000)


# 22 ----------------------------------------------------------------------
def _sol(s):
    n = Rd(s).int()
    tot, d = 0, 1
    while d <= n:
        q = n // d
        e = n // q
        tot += q * ((d + e) * (e - d + 1) // 2)
        d = e + 1
    return tot % MOD


def _br(s):
    n = Rd(s).int()
    return sum(d * (n // d) for d in range(1, n + 1)) % MOD


add(T, "Tổng các ước của 1..n", 5, """
Gọi `σ(x)` là tổng các ước dương của `x`. Tính `σ(1) + σ(2) + ... + σ(n)` modulo `10^9 + 7`.

Gợi ý: đổi thứ tự tổng — mỗi `d` là ước của đúng `⌊n/d⌋` số, nên đáp án = `Σ d·⌊n/d⌋`.
Giá trị `⌊n/d⌋` chỉ có `O(√n)` giá trị khác nhau → gom các `d` có cùng `⌊n/d⌋` thành một khối.
""", "Một số nguyên `n` (1 ≤ n ≤ 10^10).", "Kết quả modulo 10^9+7.",
    ["5\n", "1\n"], lambda r, s: str(r.randint(max(1, S(s, 1, 10**10) // 2), S(s, 10, 10**10))), _sol,
    brute=_br, tags=["chia khối", "ước số"])
