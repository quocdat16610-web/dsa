"""Chuyên đề 20: Trie (cây tiền tố), trie nhị phân cho XOR, Aho-Corasick."""
from collections import deque
from .base import add, Rd, S, J, L, arr, lines, rstr, rtree

T = 20
AL = "abcdefghijklmnopqrstuvwxyz"
B = 30


class Trie:
    def __init__(self):
        self.ch = [{}]; self.cnt = [0]; self.end = [0]

    def insert(self, w):
        u = 0; ch = self.ch
        self.cnt[0] += 1
        for c in w:
            nxt = ch[u].get(c)
            if nxt is None:
                nxt = len(ch); ch[u][c] = nxt; ch.append({}); self.cnt.append(0); self.end.append(0)
            u = nxt; self.cnt[u] += 1
        self.end[u] += 1
        return u

    def walk(self, w):
        u = 0
        for c in w:
            u = self.ch[u].get(c)
            if u is None:
                return None
        return u


class BinTrie:
    def __init__(self, bits=B):
        self.bits = bits; self.c = [[0, 0]]; self.cnt = [0]

    def add(self, x, d=1):
        u = 0; self.cnt[0] += d
        for b in range(self.bits - 1, -1, -1):
            k = x >> b & 1
            if not self.c[u][k]:
                self.c[u][k] = len(self.c); self.c.append([0, 0]); self.cnt.append(0)
            u = self.c[u][k]; self.cnt[u] += d

    def max_xor(self, x):
        u = 0; res = 0
        for b in range(self.bits - 1, -1, -1):
            k = x >> b & 1; want = self.c[u][k ^ 1]
            if want and self.cnt[want] > 0:
                res |= 1 << b; u = want
            else:
                u = self.c[u][k]
        return res

    def count_less(self, x, k):
        """Số phần tử y trong trie có x xor y < k."""
        u = 0; res = 0
        for b in range(self.bits - 1, -1, -1):
            xb, kb = x >> b & 1, k >> b & 1
            if kb:
                same = self.c[u][xb]
                if same:
                    res += self.cnt[same]
                u = self.c[u][xb ^ 1]
            else:
                u = self.c[u][xb]
            if not u:
                return res
        return res


def _words(r, n, maxlen, al):
    return [rstr(r, r.randint(1, maxlen), al) for _ in range(n)]


def _wg(r, s, nmax=10**5, total=2 * 10**5):
    n = S(s, 1, nmax); al = AL[:r.choice([2, 3, 26])]
    ml = max(1, min(30, total // n))
    return n, _words(r, n, ml, al), al, ml


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, ws, al, ml = _wg(r, s)
    q = S(s, 1, 10**5)
    qs = [w[:r.randint(1, len(w))] if r.random() < .6 else rstr(r, r.randint(1, ml), al) for w in (r.choice(ws) for _ in range(q))]
    return lines(J(n, q), *ws, *qs)


def _sol(s):
    t = s.split(); n, q = int(t[0]), int(t[1]); tr = Trie()
    for w in t[2:2 + n]:
        tr.insert(w)
    out = []
    for p in t[2 + n:2 + n + q]:
        u = tr.walk(p); out.append(tr.cnt[u] if u is not None else 0)
    return out


def _br(s):
    t = s.split(); n, q = int(t[0]), int(t[1]); ws = t[2:2 + n]
    return [sum(1 for w in ws if w.startswith(p)) for p in t[2 + n:2 + n + q]]


add(T, "Đếm từ theo tiền tố", 1, """
Từ điển có `n` từ (có thể trùng). Với mỗi truy vấn `p`, đếm số từ trong từ điển có tiền tố là `p`.

Gợi ý (**Trie**): mỗi nút là một tiền tố, lưu `cnt` = số từ đi qua nút. Chèn từ: đi theo các ký tự, tăng `cnt`.
Truy vấn: đi theo `p`; nếu rơi ra ngoài trie thì đáp án 0.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n` dòng là các từ, `q` dòng là truy vấn (tổng độ dài ≤ 4·10^5).", "Mỗi truy vấn in một dòng.",
    ["4 3\napple\napp\napply\nbanana\napp\nappl\nb\n"], _g, _sol,
    brute=lambda s: _br(s) if len(s) <= 10**5 else _sol(s), tags=["trie"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 2 * 10**5); al = AL[:r.choice([2, 3, 26])]; ml = r.choice([3, 8, 20])
    pool = _words(r, max(1, q // 3), ml, al); ops = []
    for _ in range(q):
        ops.append(J("add" if r.random() < .5 else "find", r.choice(pool) if r.random() < .7 else rstr(r, r.randint(1, ml), al)))
    return lines(str(q), *ops)


def _sol(s):
    t = s.split(); q = int(t[0]); tr = Trie(); out = []
    for i in range(q):
        op, w = t[1 + 2 * i], t[2 + 2 * i]
        if op == "add":
            tr.insert(w)
        else:
            u = tr.walk(w); out.append("YES" if u is not None and tr.end[u] else "NO")
    return out


def _br(s):
    t = s.split(); q = int(t[0]); st = set(); out = []
    for i in range(q):
        op, w = t[1 + 2 * i], t[2 + 2 * i]
        if op == "add":
            st.add(w)
        else:
            out.append("YES" if w in st else "NO")
    return out


add(T, "Từ điển", 1, """
Thực hiện `q` thao tác: `add w` thêm từ `w` vào từ điển; `find w` hỏi `w` có trong từ điển không.

Gợi ý: trie với cờ `end[u]` đánh dấu nút kết thúc một từ. (Chú ý: `find app` sau khi chỉ thêm `apple` phải là `NO`.)
""", "Dòng đầu `q` (1 ≤ q ≤ 2·10^5). `q` dòng sau là các thao tác (tổng độ dài ≤ 10^6).", "Kết quả các thao tác `find`.",
    ["5\nadd apple\nfind app\nadd app\nfind app\nfind ap\n"], _g, _sol, brute=_br, tags=["trie"])


# 3 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5); al = AL[:r.choice([1, 2, 26])]
    base = rstr(r, r.randint(0, 50), al)
    return lines(str(n), *(base[:r.randint(len(base) // 2, len(base))] + rstr(r, r.randint(1, 5), al) for _ in range(n)))


def _sol(s):
    ws = s.split()[1:]; tr = Trie()
    for w in ws:
        tr.insert(w)
    u = 0; res = []; n = len(ws)
    while len(tr.ch[u]) == 1 and tr.end[u] == 0:
        c, v = next(iter(tr.ch[u].items()))
        if tr.cnt[v] != n:
            break
        res.append(c); u = v
    return "".join(res) if res else "-"


def _br(s):
    import os.path
    p = os.path.commonprefix(s.split()[1:])
    return p if p else "-"


add(T, "Tiền tố chung dài nhất", 1, """
Tìm tiền tố chung dài nhất của tất cả `n` từ. In `-` nếu tiền tố chung rỗng.

Gợi ý: chèn mọi từ vào trie, đi từ gốc xuống khi nút hiện tại có đúng một con và con đó được **tất cả** `n` từ đi qua.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau là các từ (tổng độ dài ≤ 10^6).", "Tiền tố chung dài nhất hoặc `-`.",
    ["3\nflower\nflow\nflight\n", "2\ndog\ncar\n"], _g, _sol, brute=_br, tags=["trie"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    tr = Trie()
    for w in s.split()[1:]:
        tr.insert(w)
    return len(tr.ch) - 1


add(T, "Số nút của trie", 1, """
Chèn `n` từ vào một trie rỗng. Trie có bao nhiêu nút (không tính nút gốc)?

Gợi ý: số nút = số **tiền tố khác rỗng phân biệt** của các từ. Hãy tự cài trie bằng mảng `next[N][26]`.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau là các từ (tổng độ dài ≤ 2·10^5).", "Số nút.",
    ["3\nabc\nabd\nb\n"], lambda r, s: (lambda n, ws, al, ml: lines(str(n), *ws))(*_wg(r, s)), _sol,
    brute=lambda s: len({w[:i] for w in s.split()[1:] for i in range(1, len(w) + 1)}), tags=["trie"])


# 5 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    nums = set()
    while len(nums) < n:
        nums.add("".join(r.choice("0123456789"[:r.choice([2, 10])]) for _ in range(r.randint(1, 10))))
    nums = list(nums)
    r.shuffle(nums)
    return lines(str(len(nums)), *nums)


def _sol(s):
    ws = sorted(s.split()[1:])
    return "NO" if any(ws[i + 1].startswith(ws[i]) for i in range(len(ws) - 1)) else "YES"


add(T, "Danh bạ nhất quán", 2, """
Danh bạ có `n` số điện thoại phân biệt. Danh bạ **nhất quán** nếu không có số nào là tiền tố của số khác (khi bấm số này, tổng đài không
nhầm sang số kia). In `YES` nếu nhất quán, ngược lại `NO`.

Gợi ý: chèn vào trie; không nhất quán nếu khi chèn ta đi qua một nút kết thúc, hoặc kết thúc tại một nút đã có con.
(Cách khác: sắp xếp, chỉ cần kiểm tra các cặp kề nhau.)
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau là các số (chữ số, độ dài 1..10, đôi một khác nhau).", "`YES` hoặc `NO`.",
    ["3\n911\n97625999\n91125426\n", "3\n113\n12340\n123440\n"], _g, _sol,
    brute=lambda s: ("NO" if any(a != b and b.startswith(a) for a in s.split()[1:] for b in s.split()[1:]) else "YES")
    if int(s.split()[0]) <= 300 else _sol(s), tags=["trie"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    t = s.split(); n, q = int(t[0]), int(t[1]); ws = t[2:2 + n]
    tr = Trie(); best = {}
    for w in ws:
        tr.insert(w)
    # từ nhỏ nhất theo từ điển trong cây con của mỗi nút: duyệt các từ đã sắp xếp
    distinct = sorted(set(ws)); dcount = [0] * len(tr.ch); small = [None] * len(tr.ch)
    for w in distinct:
        u = 0
        for c in w:
            u = tr.ch[u][c]; dcount[u] += 1
            if small[u] is None:
                small[u] = w
    out = []
    for p in t[2 + n:2 + n + q]:
        u = tr.walk(p)
        out.append(J(dcount[u], small[u]) if u is not None else "0 -1")
    return out


def _br(s):
    t = s.split(); n, q = int(t[0]), int(t[1]); ws = sorted(set(t[2:2 + n])); out = []
    for p in t[2 + n:2 + n + q]:
        m = [w for w in ws if w.startswith(p)]
        out.append(J(len(m), m[0]) if m else "0 -1")
    return out


add(T, "Gợi ý tự động", 2, """
Từ điển có `n` từ. Với mỗi tiền tố `p` người dùng gõ, in số từ **khác nhau** trong từ điển bắt đầu bằng `p`, và từ nhỏ nhất theo thứ tự từ điển
trong số đó (in `0 -1` nếu không có).

Gợi ý: mỗi nút trie lưu thêm "số từ phân biệt trong cây con" và "từ nhỏ nhất trong cây con" (chèn các từ theo thứ tự đã sắp xếp,
nút nào chưa có thì gán từ hiện tại).
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n` dòng là các từ, `q` dòng là tiền tố (tổng độ dài ≤ 4·10^5).", "Mỗi truy vấn in một dòng.",
    ["5 3\ncar\ncat\ncart\ndog\ncar\nca\ncar\nz\n"], _g, _sol,
    brute=lambda s: _br(s) if len(s) <= 2 * 10**4 else _sol(s), tags=["trie"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5)
    bits = r.choice([3, 10, 30])
    return lines(str(n), L(r.getrandbits(bits) for _ in range(n)))


def _sol(s):
    a = list(map(int, s.split()[1:])); tr = BinTrie(); best = 0
    tr.add(a[0])
    for x in a[1:]:
        best = max(best, tr.max_xor(x)); tr.add(x)
    return best


def _br(s):
    a = list(map(int, s.split()[1:]))
    return max(a[i] ^ a[j] for i in range(len(a)) for j in range(i + 1, len(a)))


add(T, "Cặp có XOR lớn nhất", 2, """
Tìm giá trị lớn nhất của `a_i xor a_j` với `i < j`.

Gợi ý (**trie nhị phân**): chèn các số dưới dạng xâu 30 bit (từ bit cao xuống). Với mỗi `x`, đi từ gốc và **ưu tiên** nhánh có bit ngược với bit của `x`
(tham lam theo bit cao nhất). Mỗi truy vấn `O(30)`.
""", "Dòng đầu `n` (2 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ a_i < 2^30).", "XOR lớn nhất.",
    ["6\n3 10 5 25 2 8\n"], _g, _sol, brute=_br, tags=["trie nhị phân", "xor"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5); al = AL[:r.choice([1, 2, 3])]
    ws = set()
    for _ in range(n):
        w = rstr(r, r.randint(1, 3), al)
        while r.random() < .7 and len(w) < 30:
            w += r.choice(al)
            if r.random() < .8:
                ws.add(w)
        ws.add(w)
    ws = list(ws)[:n]; r.shuffle(ws)
    return lines(str(len(ws)), *ws)


def _sol(s):
    ws = set(s.split()[1:])
    good = {""}
    for w in sorted(ws, key=len):
        if w[:-1] in good:
            good.add(w)
    good.discard("")
    if not good:
        return "-"
    return min(good, key=lambda w: (-len(w), w))


add(T, "Từ dài nhất xây dần", 2, """
Tìm từ dài nhất trong từ điển mà **mọi tiền tố** của nó (dài 1, 2, ..., trừ chính nó) cũng là từ trong từ điển. Nếu có nhiều từ, in từ nhỏ nhất
theo thứ tự từ điển. In `-` nếu không có từ nào (khi không có từ nào dài 1).

Gợi ý: trong trie, chỉ được đi xuống qua những nút là nút kết thúc của một từ; DFS tìm nút sâu nhất (ưu tiên ký tự nhỏ).
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau là các từ phân biệt (độ dài ≤ 30).", "Từ cần tìm hoặc `-`.",
    ["7\na\nbanana\napp\nappl\nap\napply\napple\n"], _g, _sol,
    brute=lambda s: (lambda ws: min([w for w in ws if all(w[:i] in ws for i in range(1, len(w)))] or ["-"], key=lambda w: (-len(w) if w != "-" else 0, w)))(set(s.split()[1:])),
    tags=["trie"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    a = list(map(int, s.split()[1:])); tr = BinTrie(); tr.add(0); px = 0; best = 0
    for x in a:
        px ^= x; best = max(best, tr.max_xor(px)); tr.add(px)
    return best


def _br(s):
    a = list(map(int, s.split()[1:])); best = 0
    for i in range(len(a)):
        x = 0
        for j in range(i, len(a)):
            x ^= a[j]; best = max(best, x)
    return best


add(T, "Đoạn con có XOR lớn nhất", 3, """
Tìm giá trị XOR lớn nhất của một đoạn con liên tiếp (khác rỗng).

Gợi ý: XOR đoạn `(l, r] = p[r] xor p[l]` với `p` là XOR tiền tố. Bài toán trở thành "cặp có XOR lớn nhất" giữa các tiền tố — trie nhị phân.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (0 ≤ a_i < 2^30).", "XOR lớn nhất.",
    ["4\n1 2 3 4\n"], lambda r, s: (lambda n: lines(str(n), L(r.getrandbits(r.choice([3, 30])) for _ in range(n))))(S(s, 1, 2 * 10**5)),
    _sol, brute=_br, tags=["trie nhị phân", "xor", "tiền tố"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    al = AL[:r.choice([1, 2, 3])]
    k = S(s, 1, 10**4)
    ws = list({rstr(r, r.randint(1, r.choice([2, 5, 30])), al) for _ in range(k)})
    t = "".join(r.choice(ws) for _ in range(S(s, 1, 5000)))[:5000] if r.random() < .7 else rstr(r, S(s, 1, 5000), al)
    return lines(t, str(len(ws)), *ws)


def _sol(s):
    tok = s.split(); t = tok[0]; k = int(tok[1]); tr = Trie()
    for w in tok[2:2 + k]:
        tr.insert(w)
    n = len(t); MOD = 10**9 + 7; dp = [0] * (n + 1); dp[n] = 1
    ch, end = tr.ch, tr.end
    for i in range(n - 1, -1, -1):
        u = 0; tot = 0; j = i
        while j < n:
            u = ch[u].get(t[j])
            if u is None:
                break
            j += 1
            if end[u]:
                tot += dp[j]
        dp[i] = tot % MOD
    return dp[0]


def _br(s):
    tok = s.split(); t = tok[0]; k = int(tok[1]); ws = set(tok[2:2 + k]); n = len(t)
    dp = [0] * (n + 1); dp[n] = 1
    for i in range(n - 1, -1, -1):
        dp[i] = sum(dp[j] for j in range(i + 1, n + 1) if t[i:j] in ws) % (10**9 + 7)
    return dp[0]


add(T, "Ghép từ", 3, """
Cho xâu `t` và từ điển `k` từ phân biệt. Đếm số cách tách `t` thành dãy các từ trong từ điển (mỗi từ dùng bao nhiêu lần cũng được), modulo `10^9 + 7`.

Gợi ý: `dp[i]` = số cách tách hậu tố `t[i..]`. Từ vị trí `i`, đi dọc trie theo `t[i], t[i+1], ...`; mỗi khi gặp nút kết thúc tại `j`, cộng `dp[j+1]`.
""", "Dòng đầu là `t` (1 ≤ |t| ≤ 5000). Dòng hai là `k` (1 ≤ k ≤ 10^4). `k` dòng sau là các từ (tổng độ dài ≤ 10^6).",
    "Số cách modulo 10^9+7.", ["ababc\n4\nab\nabab\nc\ncb\n"], _g, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) <= 300 else _sol(s), tags=["trie", "QHĐ"])


# 11 ----------------------------------------------------------------------
def _sol(s):
    t = s.split()[0]; tr = Trie()
    for i in range(len(t)):
        tr.insert(t[i:])
    return len(tr.ch) - 1


add(T, "Trie các hậu tố", 3, """
Đếm số xâu con khác rỗng phân biệt của `s` bằng cách dựng **trie của tất cả các hậu tố**: mỗi nút (trừ gốc) tương ứng đúng một xâu con phân biệt.

Gợi ý: chèn lần lượt các hậu tố `s[i..n)` vào trie. Số nút tối đa `n(n+1)/2` — đủ nhỏ với `n ≤ 1000`.
""", "Một dòng là xâu `s` (1 ≤ |s| ≤ 1000).", "Số xâu con phân biệt.", ["abab\n"],
    lambda r, s: rstr(r, S(s, 1, 1000), AL[:r.choice([1, 2, 26])]), _sol,
    brute=lambda s: len({s.split()[0][i:j] for i in range(len(s.split()[0])) for j in range(i + 1, len(s.split()[0]) + 1)}),
    tags=["trie"])


# 12 ----------------------------------------------------------------------
def _sol(s):
    tr = Trie()
    for w in s.split()[1:]:
        tr.insert(w)
    return sum(c * (c - 1) // 2 for c in tr.cnt[1:])


def _br(s):
    import os.path
    ws = s.split()[1:]
    return sum(len(os.path.commonprefix([ws[i], ws[j]])) for i in range(len(ws)) for j in range(i + 1, len(ws)))


add(T, "Tổng tiền tố chung của mọi cặp", 3, """
Tính `Σ_{i<j} LCP(s_i, s_j)` — tổng độ dài tiền tố chung dài nhất của mọi cặp từ.

Gợi ý: cặp `(i, j)` đóng góp 1 cho mỗi nút trie mà cả hai cùng đi qua. Vậy đáp án = `Σ_{nút ≠ gốc} C(cnt, 2)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau là các từ (tổng độ dài ≤ 2·10^5).", "Tổng (vừa `long long`).",
    ["3\nabc\nabd\nab\n"], lambda r, s: (lambda n, ws, al, ml: lines(str(n), *ws))(*_wg(r, s)), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 300 else _sol(s), tags=["trie", "đếm"])


# 13 ----------------------------------------------------------------------
def _sol(s):
    ws = s.split()[1:]; tr = Trie()
    for w in ws:
        tr.insert(w)
    tot = 0
    for w in ws:
        u = 0
        for c in w:
            u = tr.ch[u][c]; tot += tr.end[u]
        tot -= 1  # chính nó
    return tot


def _br(s):
    ws = s.split()[1:]
    return sum(1 for i in range(len(ws)) for j in range(len(ws)) if i != j and ws[j].startswith(ws[i]))


add(T, "Cặp tiền tố", 3, """
Đếm số cặp có thứ tự `(i, j)` với `i ≠ j` mà từ `s_i` là tiền tố của từ `s_j` (hai từ giống nhau cũng tính là tiền tố của nhau).

Gợi ý: với mỗi từ `s_j`, đi dọc trie theo `s_j` và cộng số từ **kết thúc** tại mỗi nút đi qua, trừ đi chính nó.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau là các từ (tổng độ dài ≤ 2·10^5).", "Số cặp.",
    ["4\na\nab\nab\nb\n"], lambda r, s: (lambda n, ws, al, ml: lines(str(n), *ws))(*_wg(r, s)), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 300 else _sol(s), tags=["trie"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5); bits = r.choice([4, 12, 30])
    return lines(J(n, r.randint(0, 2**bits)), L(r.getrandbits(bits) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    tr = BinTrie(31); tot = 0
    for x in a:
        tot += tr.count_less(x, k); tr.add(x)
    return tot


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] ^ a[j] < k)


add(T, "Cặp có XOR nhỏ hơn k", 4, """
Đếm số cặp `i < j` mà `a_i xor a_j < k`.

Gợi ý: trie nhị phân lưu số lượng trong mỗi nút. Với `x` và `k`, đi từ bit cao: nếu bit của `k` là 1 thì mọi `y` có bit **giống** `x` ở đây
cho XOR bit 0 < 1 → cộng cả nhánh đó, rồi đi tiếp sang nhánh ngược; nếu bit của `k` là 0 thì bắt buộc đi nhánh giống.
""", "Dòng đầu `n, k` (2 ≤ n ≤ 10^5, 0 ≤ k ≤ 2^30). Dòng sau `n` số (0 ≤ a_i < 2^30).", "Số cặp.",
    ["4 3\n1 2 3 4\n"], _g, _sol, brute=_br, tags=["trie nhị phân", "xor"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 2 * 10**5); bits = r.choice([4, 30])
    ops = []; live = [0]
    for _ in range(q):
        t = r.random()
        if t < .4:
            x = r.getrandbits(bits); ops.append(J("+", x)); live.append(x)
        elif t < .6 and len(live) > 1:
            i = r.randrange(1, len(live)); x = live.pop(i); ops.append(J("-", x))
        else:
            ops.append(J("?", r.getrandbits(bits)))
    return lines(str(q), *ops)


def _sol(s):
    t = s.split(); q = int(t[0]); tr = BinTrie(); tr.add(0); out = []
    for i in range(q):
        op, x = t[1 + 2 * i], int(t[2 + 2 * i])
        if op == "+":
            tr.add(x)
        elif op == "-":
            tr.add(x, -1)
        else:
            out.append(tr.max_xor(x))
    return out


def _br(s):
    from collections import Counter
    t = s.split(); q = int(t[0]); ms = Counter([0]); out = []
    for i in range(q):
        op, x = t[1 + 2 * i], int(t[2 + 2 * i])
        if op == "+":
            ms[x] += 1
        elif op == "-":
            ms[x] -= 1
        else:
            out.append(max(x ^ y for y, c in ms.items() if c > 0))
    return out


add(T, "Tập hợp XOR", 4, """
Ban đầu tập (multiset) chỉ có số 0. Thao tác:
- `+ x`: thêm `x`;
- `- x`: xoá **một** số `x` (đảm bảo đang có);
- `? x`: in giá trị lớn nhất của `x xor y` với `y` trong tập.

Gợi ý: trie nhị phân với bộ đếm ở mỗi nút; xoá = giảm bộ đếm. Khi tìm XOR lớn nhất chỉ đi vào nút có bộ đếm > 0.
""", "Dòng đầu `q` (1 ≤ q ≤ 2·10^5). `q` dòng sau là các thao tác (0 ≤ x < 2^30).", "Kết quả các thao tác `?`.",
    ["7\n+ 8\n+ 9\n+ 11\n+ 6\n+ 1\n? 3\n- 8\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 2000 else _sol(s),
    tags=["trie nhị phân", "xor"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5); al = AL[:r.choice([2, 3])]
    ws = [rstr(r, r.randint(1, 8), al) for _ in range(n)]
    q = S(s, 1, 10**4)
    qs = []
    for _ in range(q):
        w = list(r.choice(ws)) if r.random() < .7 else list(rstr(r, r.randint(1, 8), al))
        for i in range(len(w)):
            if r.random() < .3:
                w[i] = "?"
        qs.append("".join(w))
    return lines(J(n, q), *ws, *qs)


def _sol(s):
    t = s.split(); n, q = int(t[0]), int(t[1]); tr = Trie()
    for w in t[2:2 + n]:
        tr.insert(w)
    ch, end = tr.ch, tr.end
    out = []
    for p in t[2 + n:2 + n + q]:
        cur = [0]
        for c in p:
            nxt = []
            for u in cur:
                if c == "?":
                    nxt.extend(ch[u].values())
                elif c in ch[u]:
                    nxt.append(ch[u][c])
            cur = nxt
            if not cur:
                break
        out.append(sum(end[u] for u in cur))
    return out


def _br(s):
    t = s.split(); n, q = int(t[0]), int(t[1]); ws = t[2:2 + n]; out = []
    for p in t[2 + n:2 + n + q]:
        out.append(sum(1 for w in ws if len(w) == len(p) and all(a == "?" or a == b for a, b in zip(p, w))))
    return out


add(T, "Khớp mẫu có ký tự đại diện", 4, """
Từ điển có `n` từ (có thể trùng, chỉ gồm chữ `a..c`, độ dài ≤ 8). Mỗi truy vấn là một mẫu cùng bảng chữ cái, trong đó `?` khớp với **một** ký tự bất kỳ.
Đếm số từ (tính cả lặp) khớp hoàn toàn với mẫu (cùng độ dài).

Gợi ý: DFS trên trie theo mẫu: gặp ký tự thường thì đi một nhánh, gặp `?` thì đi tất cả các nhánh con.
""", "Dòng đầu `n, q` (1 ≤ n ≤ 10^5, 1 ≤ q ≤ 10^4). `n` dòng là các từ, `q` dòng là các mẫu (độ dài ≤ 8).", "Mỗi truy vấn in một dòng.",
    ["4 3\nabc\nabb\nacc\nab\na?c\n??\nb??\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["trie", "DFS"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5)
    es = rtree(r, n); bits = r.choice([3, 30])
    return lines(str(n), *(J(a, b, r.getrandbits(bits)) for a, b in es))


def _sol(s):
    rd = Rd(s); n = rd.int()
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b, w = rd.ints(3); adj[a].append((b, w)); adj[b].append((a, w))
    px = [-1] * (n + 1); px[1] = 0; st = [1]
    while st:
        u = st.pop()
        for v, w in adj[u]:
            if px[v] < 0:
                px[v] = px[u] ^ w; st.append(v)
    tr = BinTrie(); best = 0; tr.add(px[1])
    for v in range(2, n + 1):
        best = max(best, tr.max_xor(px[v])); tr.add(px[v])
    return best


def _br(s):
    rd = Rd(s); n = rd.int()
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b, w = rd.ints(3); adj[a].append((b, w)); adj[b].append((a, w))
    best = 0
    for src in range(1, n + 1):
        d = {src: 0}; st = [src]
        while st:
            u = st.pop()
            for v, w in adj[u]:
                if v not in d:
                    d[v] = d[u] ^ w; st.append(v)
        best = max(best, max(d.values()))
    return best


add(T, "Đường đi XOR lớn nhất trên cây", 4, """
Cây có trọng số trên cạnh. Độ dài XOR của đường đi là XOR các trọng số trên đường đi. Tìm đường đi có độ dài XOR lớn nhất.

Gợi ý: `xor(u, v) = d[u] xor d[v]` với `d[x]` = XOR từ gốc tới `x` (phần chung tự triệt tiêu). Bài toán thành "cặp XOR lớn nhất" trên các `d[x]`.
""", "Dòng đầu `n` (2 ≤ n ≤ 10^5). `n - 1` dòng sau mỗi dòng `u v w` (0 ≤ w < 2^30).", "XOR lớn nhất.",
    ["4\n1 2 3\n2 3 4\n2 4 6\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 300 else _sol(s), tags=["trie nhị phân", "cây"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5); bits = r.choice([3, 12, 30])
    return lines(J(n, r.randint(0, 2**bits)), L(r.getrandbits(bits) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    tr = BinTrie(31); tr.add(0); px = 0; less = 0
    for x in a:
        px ^= x; less += tr.count_less(px, k); tr.add(px)
    return n * (n + 1) // 2 - less


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n); c = 0
    for i in range(n):
        x = 0
        for j in range(i, n):
            x ^= a[j]; c += x >= k
    return c


add(T, "Đếm đoạn có XOR không nhỏ hơn k", 4, """
Đếm số đoạn con liên tiếp có XOR ≥ k.

Gợi ý: XOR tiền tố + đếm số cặp tiền tố có XOR `< k` bằng trie nhị phân; lấy tổng số đoạn trừ đi.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 10^5, 0 ≤ k ≤ 2^30). Dòng sau `n` số (0 ≤ a_i < 2^30).", "Số đoạn.",
    ["3 2\n1 2 3\n"], _g, _sol, brute=_br, tags=["trie nhị phân", "xor"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5); bits = r.choice([5, 30])
    return lines(J(n, q), L(r.getrandbits(bits) for _ in range(n)),
                 *(J(r.getrandbits(bits), r.getrandbits(bits)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); a = sorted(rd.ints(n))
    qs = sorted((rd.ints(2) + [i] for i in range(q)), key=lambda x: x[1])
    tr = BinTrie(); j = 0; ans = [-1] * q
    for x, m, i in qs:
        while j < n and a[j] <= m:
            tr.add(a[j]); j += 1
        if j:
            ans[i] = tr.max_xor(x)
    return ans


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); a = rd.ints(n); out = []
    for _ in range(q):
        x, m = rd.ints(2); c = [x ^ v for v in a if v <= m]
        out.append(max(c) if c else -1)
    return out


add(T, "XOR lớn nhất có giới hạn", 5, """
Cho dãy `a` và `q` truy vấn `(x, m)`: tìm giá trị lớn nhất của `x xor a_i` với các `a_i ≤ m`; in `-1` nếu không có `a_i` nào ≤ m.

Gợi ý (offline): sắp xếp `a` tăng dần và truy vấn theo `m` tăng dần; trước khi trả lời truy vấn, chèn vào trie mọi `a_i ≤ m`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` số. `q` dòng sau mỗi dòng `x m` (giá trị < 2^30).", "Mỗi truy vấn in một dòng.",
    ["5 3\n0 1 2 3 4\n3 1\n1 3\n5 6\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["trie nhị phân", "offline"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    al = AL[:r.choice([1, 2, 3])]
    t = rstr(r, S(s, 1, 10**5), al)
    k = S(s, 1, 10**4)
    ps = []
    for _ in range(k):
        if r.random() < .6:
            ln = r.randint(1, min(len(t), 20)); i = r.randint(0, len(t) - ln); ps.append(t[i:i + ln])
        else:
            ps.append(rstr(r, r.randint(1, 20), al))
    return lines(t, str(k), *ps)


def _sol(s):
    tok = s.split(); t = tok[0]; k = int(tok[1]); tr = Trie()
    for p in tok[2:2 + k]:
        tr.insert(p)
    ch, end = tr.ch, tr.end
    m = len(ch); fail = [0] * m; out = end[:]  # out[u] = số mẫu kết thúc tại u hoặc các liên kết hậu tố của u
    goto = [dict() for _ in range(m)]
    q = deque()
    for c, v in ch[0].items():
        q.append(v)
    while q:
        u = q.popleft()
        out[u] += out[fail[u]]
        for c, v in ch[u].items():
            f = fail[u]
            while f and c not in ch[f]:
                f = fail[f]
            fail[v] = ch[f][c] if c in ch[f] and ch[f][c] != v else 0
            q.append(v)
    tot = 0; u = 0
    for c in t:
        while u and c not in ch[u]:
            u = fail[u]
        u = ch[u].get(c, 0)
        tot += out[u]
    return tot


def _br(s):
    tok = s.split(); t = tok[0]; k = int(tok[1])
    return sum(sum(1 for i in range(len(t) - len(p) + 1) if t.startswith(p, i)) for p in tok[2:2 + k])


add(T, "Aho-Corasick", 5, """
Cho văn bản `t` và `k` mẫu (có thể trùng nhau). Tính tổng số lần xuất hiện của **tất cả** các mẫu trong `t` (mỗi mẫu trùng tính riêng).

Gợi ý (**Aho-Corasick**): dựng trie các mẫu, thêm **liên kết hậu tố** (fail link) bằng BFS như KMP trên trie. `out[u]` = số mẫu kết thúc tại `u`
cộng `out[fail[u]]`. Duyệt văn bản một lần trên automaton, cộng `out` của trạng thái hiện tại. Độ phức tạp `O(|t| + Σ|p|)`.
""", "Dòng đầu là `t` (1 ≤ |t| ≤ 10^5). Dòng hai là `k` (1 ≤ k ≤ 10^4). `k` dòng sau là các mẫu (độ dài ≤ 20).", "Tổng số lần xuất hiện.",
    ["ababa\n3\naba\nb\nab\n"], _g, _sol,
    brute=lambda s: _br(s) if len(s.split()[0]) * int(s.split()[1]) <= 2 * 10**6 else _sol(s), tags=["Aho-Corasick", "trie"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5); al = AL[:r.choice([1, 2, 3, 26])]
    ws = _words(r, n, max(1, min(20, 10**5 // n)), al)
    return lines(J(n, r.randint(1, 10**9)), *ws)


def _sol(s):
    t = s.split(); n, k = int(t[0]), int(t[1]); tr = Trie()
    for w in t[2:2 + n]:
        tr.insert(w)
    ch = tr.ch; m = len(ch)
    order = [0]
    for u in order:
        order.extend(ch[u].values())
    win = [False] * m; lose = [False] * m
    for u in reversed(order):
        if not ch[u]:
            win[u] = False; lose[u] = True  # người phải đi ở lá: không đi được → thua; "muốn thua" thì đạt được
        else:
            win[u] = any(not win[v] for v in ch[u].values())
            lose[u] = any(not lose[v] for v in ch[u].values())
    if not win[0]:
        return "Second"
    if lose[0]:
        return "First"
    return "First" if k % 2 else "Second"


add(T, "Trò chơi ghép chữ", 5, """
Cho `n` từ. Hai người chơi lần lượt thêm một chữ cái vào cuối xâu chung (ban đầu rỗng) sao cho xâu luôn là **tiền tố** của ít nhất một từ.
Ai không thêm được thì **thua** ván đó. Chơi `k` ván; người thua ván trước được đi trước ở ván sau; người thắng ván cuối cùng thắng chung cuộc.
Người đi trước ở ván đầu là "First". Ai thắng nếu cả hai chơi tối ưu?

Gợi ý: trên trie, tính `win[u]` (người phải đi ở `u` có **thắng** được không) và `lose[u]` (có **chủ động thua** được không).
Nếu không `win[gốc]` → Second. Nếu `win` và `lose` đều được → First (thua tuỳ ý để giữ quyền đi trước tới ván cuối).
Nếu chỉ `win` → kết quả phụ thuộc tính chẵn lẻ của `k`.
""", "Dòng đầu `n, k` (1 ≤ n ≤ 10^5, 1 ≤ k ≤ 10^9). `n` dòng sau là các từ (tổng độ dài ≤ 10^5).", "`First` hoặc `Second`.",
    ["2 3\na\nb\n", "3 1\na\nb\nc\n", "1 2\nab\n"], _g, _sol, tags=["trie", "lý thuyết trò chơi"])
