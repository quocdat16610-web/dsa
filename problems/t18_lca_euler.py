"""Chuyên đề 18: Tổ tiên chung gần nhất (LCA), Euler tour trên cây."""
from .base import add, Rd, S, J, L, arr, lines, rtree

T = 18


class Tree:
    """Cây gốc `root`: par, depth, tin/tout (duyệt con theo thứ tự tăng dần), nhảy nhị phân."""

    def __init__(self, n, edges, root=1, weights=None):
        self.n = n
        adj = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(edges):
            w = weights[i] if weights else 1
            adj[a].append((b, w)); adj[b].append((a, w))
        for lst in adj:
            lst.sort()
        self.adj = adj
        par = [0] * (n + 1); dep = [0] * (n + 1); dist = [0] * (n + 1); pw = [0] * (n + 1)
        tin = [0] * (n + 1); tout = [0] * (n + 1); order = []
        it = [0] * (n + 1); stack = [root]; par[root] = 0; t = 0
        tin[root] = t; order.append(root)
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v, w = adj[u][it[u]]; it[u] += 1
                if v != par[u]:
                    par[v] = u; dep[v] = dep[u] + 1; dist[v] = dist[u] + w; pw[v] = w
                    t += 1; tin[v] = t; order.append(v); stack.append(v)
            else:
                tout[u] = t; stack.pop()
        self.par, self.dep, self.dist, self.pw, self.tin, self.tout, self.order = par, dep, dist, pw, tin, tout, order
        self.LOG = max(1, n.bit_length())
        up = [par[:]]
        up[0][root] = root
        for _ in range(1, self.LOG):
            p = up[-1]; up.append([p[p[v]] for v in range(n + 1)])
        self.up = up

    def is_anc(self, u, v):
        return self.tin[u] <= self.tin[v] <= self.tout[u]

    def lca(self, u, v):
        if self.is_anc(u, v):
            return u
        if self.is_anc(v, u):
            return v
        up, tin, tout = self.up, self.tin, self.tout
        tv = tin[v]
        for j in range(self.LOG - 1, -1, -1):
            w = up[j][u]
            if not (tin[w] <= tv <= tout[w]):
                u = w
        return self.par[u]

    def kth_anc(self, u, k):
        if k > self.dep[u]:
            return -1
        j = 0
        while k:
            if k & 1:
                u = self.up[j][u]
            k >>= 1; j += 1
        return u

    def d(self, u, v):
        return self.dep[u] + self.dep[v] - 2 * self.dep[self.lca(u, v)]


def _read_tree(rd, n, weighted=False):
    es, ws = [], []
    for _ in range(n - 1):
        if weighted:
            a, b, w = rd.ints(3); ws.append(w)
        else:
            a, b = rd.ints(2)
        es.append((a, b))
    return es, (ws if weighted else None)


def _tree_q(qgen, weighted=False, nmax=2 * 10**5, qmax=2 * 10**5, head=None):
    def g(r, s):
        n, q = S(s, 1, nmax), S(s, 1, qmax)
        es = rtree(r, n)
        rows = [J(a, b, r.randint(1, 10**9)) if weighted else J(a, b) for a, b in es]
        extra = head(r, n) if head else []
        return lines(J(n, q), *extra, *rows, *(qgen(r, n) for _ in range(q)))
    return g


def _br_path(n, es, u, v):
    adj = [[] for _ in range(n + 1)]
    for a, b in es:
        adj[a].append(b); adj[b].append(a)
    par = {u: 0}; st = [u]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in par:
                par[y] = x; st.append(y)
    path = [v]
    while path[-1] != u:
        path.append(par[path[-1]])
    return path[::-1]


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    boss = [r.randint(max(1, i - r.choice([1, 3, i])), i - 1) for i in range(2, n + 1)]
    return lines(J(n, q), L(boss), *(J(r.randint(1, n), r.randint(1, r.choice([3, n]))) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); boss = rd.ints(n - 1)
    tr = Tree(n, [(i + 2, b) for i, b in enumerate(boss)])
    return [tr.kth_anc(*rd.ints(2)) for _ in range(q)]


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); par = [0, 0] + rd.ints(n - 1); out = []
    for _ in range(q):
        x, k = rd.ints(2)
        while k and x:
            x = par[x]; k -= 1
        out.append(x if x else -1)
    return out


add(T, "Sếp cấp k", 1, """
Công ty có `n` nhân viên, nhân viên 1 là giám đốc, nhân viên `i ≥ 2` có sếp trực tiếp `b_i`. Với truy vấn `(x, k)`: ai là sếp cấp `k` của `x`
(sếp của sếp ... `k` lần)? In `-1` nếu không tồn tại.

Gợi ý (nhảy nhị phân): `up[j][v]` = tổ tiên thứ `2^j` của `v`; `up[j][v] = up[j-1][up[j-1][v]]`. Tách `k` thành tổng luỹ thừa 2 → `O(log n)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `b_2..b_n`. `q` dòng sau mỗi dòng `x k` (1 ≤ k ≤ n).", "Mỗi truy vấn in một dòng.",
    ["5 3\n1 1 3 3\n4 1\n4 2\n4 3\n"], _g, _sol, brute=_br, tags=["nhảy nhị phân"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); boss = rd.ints(n - 1)
    tr = Tree(n, [(i + 2, b) for i, b in enumerate(boss)])
    return [tr.lca(*rd.ints(2)) for _ in range(q)]


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); par = [0, 0] + rd.ints(n - 1); out = []
    for _ in range(q):
        a, b = rd.ints(2); anc = set()
        while a:
            anc.add(a); a = par[a]
        while b not in anc:
            b = par[b]
        out.append(b)
    return out


add(T, "Sếp chung gần nhất (LCA)", 1, """
Với truy vấn `(a, b)`, tìm nhân viên cấp thấp nhất là sếp (trực tiếp hoặc gián tiếp, hoặc chính là) của cả `a` và `b`.

Gợi ý: đưa hai đỉnh về cùng độ sâu rồi cùng nhảy lên bằng nhảy nhị phân; hoặc dùng `tin/tout` để kiểm tra tổ tiên.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `b_2..b_n`. `q` dòng sau mỗi dòng `a b`.", "Mỗi truy vấn in một dòng.",
    ["5 3\n1 1 3 3\n4 5\n2 5\n1 4\n"],
    lambda r, s: (lambda n, q: lines(J(n, q), L(r.randint(max(1, i - r.choice([1, 3, i])), i - 1) for i in range(2, n + 1)),
                                      *(J(r.randint(1, n), r.randint(1, n)) for _ in range(q))))(S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)),
    _sol, brute=_br, tags=["LCA"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es)
    return [tr.d(*rd.ints(2)) for _ in range(q)]


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    return [len(_br_path(n, es, *rd.ints(2))) - 1 for _ in range(q)]


add(T, "Khoảng cách trên cây", 2, """
Cho cây `n` đỉnh và `q` truy vấn `(a, b)`: số cạnh trên đường đi từ `a` tới `b`.

Gợi ý: `dist(a, b) = depth[a] + depth[b] - 2·depth[lca(a, b)]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `n - 1` dòng là các cạnh, `q` dòng là truy vấn.", "Mỗi truy vấn in một dòng.",
    ["5 3\n1 2\n1 3\n3 4\n3 5\n1 3\n2 5\n1 4\n"], _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n))), _sol,
    brute=_br, tags=["LCA"])


# 4 -----------------------------------------------------------------------
def _qg4(r, n):
    return J(1, r.randint(1, n), r.randint(1, 10**9)) if r.random() < .5 else J(2, r.randint(1, n))


def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    es = rtree(r, n)
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *(J(a, b) for a, b in es), *(_qg4(r, n) for _ in range(q)))


class _BIT:
    def __init__(self, n):
        self.n = n; self.t = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.t[i] += v; i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); b = _BIT(n)
    for v in range(1, n + 1):
        b.add(tr.tin[v] + 1, val[v])
    out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            v, x = rd.ints(2); b.add(tr.tin[v] + 1, x - val[v]); val[v] = x
        else:
            v = rd.int(); out.append(b.sum(tr.tout[v] + 1) - b.sum(tr.tin[v]))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            v, x = rd.ints(2); val[v] = x
        else:
            v = rd.int(); out.append(sum(val[u] for u in range(1, n + 1) if tr.is_anc(v, u)))
    return out


add(T, "Tổng cây con", 2, """
Cây gốc 1, mỗi đỉnh có giá trị. Thao tác:
- `1 v x`: đổi giá trị đỉnh `v` thành `x`;
- `2 v`: in tổng giá trị các đỉnh trong cây con gốc `v`.

Gợi ý (**Euler tour**): đánh số các đỉnh theo thứ tự DFS (`tin`). Cây con của `v` là đoạn liên tiếp `[tin[v], tout[v]]` → bài toán
"cập nhật điểm, tổng đoạn" trên mảng — dùng BIT.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` giá trị (1 ≤ v ≤ 10^9). `n - 1` dòng là cạnh, `q` dòng là thao tác.",
    "Kết quả các thao tác loại 2.", ["5 3\n4 2 5 2 1\n1 2\n1 3\n3 4\n3 5\n2 3\n1 5 3\n2 1\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 300 else _sol(s), tags=["Euler tour", "BIT"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); b = _BIT(n + 1)

    def radd(l, r_, x):
        b.add(l + 1, x); b.add(r_ + 2, -x)
    for v in range(1, n + 1):
        radd(tr.tin[v], tr.tout[v], val[v])
    out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            v, x = rd.ints(2); radd(tr.tin[v], tr.tout[v], x - val[v]); val[v] = x
        else:
            v = rd.int(); out.append(b.sum(tr.tin[v] + 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            v, x = rd.ints(2); val[v] = x
        else:
            v = rd.int(); tot = 0
            while v:
                tot += val[v]; v = tr.par[v]
            out.append(tot)
    return out


add(T, "Tổng đường đi tới gốc", 3, """
Cây gốc 1, mỗi đỉnh có giá trị. Thao tác:
- `1 v x`: đổi giá trị đỉnh `v` thành `x`;
- `2 v`: in tổng giá trị các đỉnh trên đường đi từ gốc tới `v`.

Gợi ý: giá trị của `v` đóng góp cho mọi đỉnh trong cây con của `v` — tức đoạn `[tin[v], tout[v]]`. "Cộng đoạn, hỏi điểm" → BIT trên mảng hiệu.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). Dòng hai gồm `n` giá trị (1 ≤ v ≤ 10^9). `n - 1` dòng là cạnh, `q` dòng là thao tác.",
    "Kết quả các thao tác loại 2.", ["5 3\n4 2 5 2 1\n1 2\n1 3\n3 4\n3 5\n2 4\n1 3 2\n2 4\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 3000 else _sol(s), tags=["Euler tour", "BIT"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        a, b, v = rd.ints(3)
        out.append("YES" if tr.d(a, v) + tr.d(v, b) == tr.d(a, b) else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n); out = []
    for _ in range(q):
        a, b, v = rd.ints(3); out.append("YES" if v in _br_path(n, es, a, b) else "NO")
    return out


add(T, "Đỉnh nằm trên đường đi", 2, """
Với truy vấn `(a, b, v)`: đỉnh `v` có nằm trên đường đi từ `a` tới `b` không?

Gợi ý: `v` nằm trên đường `a → b` ⇔ `dist(a, v) + dist(v, b) = dist(a, b)`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n - 1` dòng là cạnh, `q` dòng sau mỗi dòng `a b v`.", "Mỗi truy vấn in `YES`/`NO`.",
    ["5 3\n1 2\n1 3\n3 4\n3 5\n2 4 1\n4 5 1\n4 5 3\n"],
    _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n), r.randint(1, n)), nmax=10**5, qmax=10**5), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA"])


# 7 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, ws = _read_tree(rd, n, True)
    tr = Tree(n, es, weights=ws); out = []
    for _ in range(q):
        a, b = rd.ints(2); out.append(tr.dist[a] + tr.dist[b] - 2 * tr.dist[tr.lca(a, b)])
    return out


add(T, "Khoảng cách có trọng số", 2, """
Cây có trọng số trên cạnh. Với truy vấn `(a, b)`, in tổng trọng số trên đường đi từ `a` tới `b`.

Gợi ý: `dist[v]` = tổng trọng số từ gốc tới `v`; đáp án `dist[a] + dist[b] - 2·dist[lca]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `n - 1` dòng `u v w` (1 ≤ w ≤ 10^9), `q` dòng truy vấn.", "Mỗi truy vấn in một dòng.",
    ["4 2\n1 2 3\n2 3 4\n2 4 5\n3 4\n1 3\n"], _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n)), weighted=True), _sol, tags=["LCA"])


# 8 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); c = [0] * (n + 1)
    for _ in range(m):
        a, b = rd.ints(2); w = tr.lca(a, b)
        c[a] += 1; c[b] += 1; c[w] -= 1
        if tr.par[w]:
            c[tr.par[w]] -= 1
    for v in reversed(tr.order):
        if tr.par[v]:
            c[tr.par[v]] += c[v]
    return L(c[1:])


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es, _ = _read_tree(rd, n); c = [0] * (n + 1)
    for _ in range(m):
        for v in _br_path(n, es, *rd.ints(2)):
            c[v] += 1
    return L(c[1:])


add(T, "Đếm đường đi qua mỗi đỉnh", 3, """
Cho cây và `m` đường đi `(a, b)`. Với mỗi đỉnh, đếm số đường đi chứa đỉnh đó.

Gợi ý (mảng hiệu trên cây): với đường `(a, b)`, `w = lca(a, b)`: `c[a]++, c[b]++, c[w]--, c[cha(w)]--`.
Sau đó cộng dồn từ lá lên gốc: giá trị tại `v` = tổng `c` trong cây con của `v`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). `n - 1` dòng là cạnh, `m` dòng là các đường đi.", "Một dòng gồm `n` số.",
    ["5 3\n1 2\n1 3\n3 4\n3 5\n1 3\n2 5\n1 4\n"], _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n))), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA", "mảng hiệu trên cây"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, ws = _read_tree(rd, n, True)
    tr = Tree(n, es, weights=ws)
    mx = [tr.pw[:]]
    for j in range(1, tr.LOG):
        pm, pu = mx[-1], tr.up[j - 1]
        mx.append([max(pm[v], pm[pu[v]]) for v in range(n + 1)])

    def climb(u, k):
        best, j = 0, 0
        while k:
            if k & 1:
                best = max(best, mx[j][u]); u = tr.up[j][u]
            k >>= 1; j += 1
        return best
    out = []
    for _ in range(q):
        a, b = rd.ints(2); w = tr.lca(a, b)
        out.append(max(climb(a, tr.dep[a] - tr.dep[w]), climb(b, tr.dep[b] - tr.dep[w])))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, ws = _read_tree(rd, n, True)
    wmap = {}
    for (a, b), w in zip(es, ws):
        wmap[(a, b)] = wmap[(b, a)] = w
    out = []
    for _ in range(q):
        p = _br_path(n, es, *rd.ints(2))
        out.append(max([wmap[(p[i], p[i + 1])] for i in range(len(p) - 1)] + [0]))
    return out


add(T, "Cạnh nặng nhất trên đường đi", 4, """
Cây có trọng số. Với truy vấn `(a, b)`, in trọng số lớn nhất trên đường đi từ `a` tới `b` (0 nếu `a = b`).

Gợi ý: song song với `up[j][v]`, lưu `mx[j][v]` = cạnh lớn nhất trên đoạn nhảy `2^j` bước từ `v`. Khi nhảy từ `a` và `b` lên `lca`, lấy max.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n - 1` dòng `u v w` (1 ≤ w ≤ 10^9), `q` dòng truy vấn.", "Mỗi truy vấn in một dòng.",
    ["4 2\n1 2 3\n2 3 4\n2 4 5\n3 4\n1 3\n"], _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n)), weighted=True, nmax=10**5, qmax=10**5),
    _sol, brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA", "nhảy nhị phân"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    es = rtree(r, n)
    return lines(str(n), L(arr(r, n, 1, r.choice([3, 50, n, 10**9]))), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n = rd.int(); col = rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es)
    seq = [0] * n
    for v in range(1, n + 1):
        seq[tr.tin[v]] = col[v - 1]
    # đếm số giá trị phân biệt trên đoạn [tin, tout] — offline theo đầu phải
    qs = sorted(range(1, n + 1), key=lambda v: tr.tout[v])
    b = _BIT(n); last = {}; ans = [0] * (n + 1); j = 0
    for i, x in enumerate(seq, 1):
        if x in last:
            b.add(last[x], -1)
        last[x] = i; b.add(i, 1)
        while j < n and tr.tout[qs[j]] + 1 == i:
            v = qs[j]; ans[v] = b.sum(i) - b.sum(tr.tin[v]); j += 1
    return L(ans[1:])


def _br(s):
    rd = Rd(s); n = rd.int(); col = rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es)
    return L(len({col[u - 1] for u in range(1, n + 1) if tr.is_anc(v, u)}) for v in range(1, n + 1))


add(T, "Số màu trong cây con", 4, """
Cây gốc 1, mỗi đỉnh có một màu. Với mỗi đỉnh `v`, đếm số màu khác nhau trong cây con gốc `v`.

Gợi ý: Euler tour biến cây con thành đoạn `[tin, tout]` → bài "số giá trị phân biệt trên đoạn" (offline + BIT). (Cách khác: gộp tập nhỏ vào lớn — small-to-large.)
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng hai gồm `n` màu (1 ≤ c ≤ 10^9). `n - 1` dòng sau là các cạnh.", "Một dòng gồm `n` số.",
    ["5\n2 3 2 2 1\n1 2\n1 3\n3 4\n3 5\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 400 else _sol(s),
    tags=["Euler tour", "offline", "BIT"])


# 11 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        a, b, k = rd.ints(3)
        w = tr.lca(a, b); da = tr.dep[a] - tr.dep[w]; db = tr.dep[b] - tr.dep[w]
        if k > da + db:
            out.append(-1)
        elif k <= da:
            out.append(tr.kth_anc(a, k))
        else:
            out.append(tr.kth_anc(b, da + db - k))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n); out = []
    for _ in range(q):
        a, b, k = rd.ints(3); p = _br_path(n, es, a, b)
        out.append(p[k] if k < len(p) else -1)
    return out


add(T, "Đỉnh thứ k trên đường đi", 4, """
Với truy vấn `(a, b, k)`: đi từ `a` tới `b`, đỉnh thứ `k` (đỉnh `a` là thứ 0) là đỉnh nào? In `-1` nếu đường đi ngắn hơn.

Gợi ý: gọi `w = lca(a, b)`. Nếu `k ≤ depth[a] - depth[w]` thì đáp án là tổ tiên thứ `k` của `a`; ngược lại là tổ tiên thứ `(độ dài − k)` của `b`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n - 1` dòng là cạnh, `q` dòng sau mỗi dòng `a b k` (0 ≤ k ≤ n).", "Mỗi truy vấn in một dòng.",
    ["5 3\n1 2\n1 3\n3 4\n3 5\n2 4 2\n2 4 3\n4 5 5\n"],
    _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n), r.randint(0, min(n, 20) if r.random() < .5 else n)), nmax=10**5, qmax=10**5),
    _sol, brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA", "nhảy nhị phân"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    es = rtree(r, n)
    ops = [J(1, r.randint(1, n), r.randint(1, 10**4)) if r.random() < .5 else J(2, r.randint(1, n)) for _ in range(q)]
    return lines(J(n, q), *(J(a, b) for a, b in es), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); b = _BIT(n + 1); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            v, x = rd.ints(2); b.add(tr.tin[v] + 1, x); b.add(tr.tout[v] + 2, -x)
        else:
            out.append(b.sum(tr.tin[rd.int()] + 1))
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); val = [0] * (n + 1); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            v, x = rd.ints(2)
            for u in range(1, n + 1):
                if tr.is_anc(v, u):
                    val[u] += x
        else:
            out.append(val[rd.int()])
    return out


add(T, "Cộng cả cây con", 3, """
Cây gốc 1, ban đầu mọi đỉnh có giá trị 0. Thao tác:
- `1 v x`: cộng `x` vào mọi đỉnh trong cây con gốc `v`;
- `2 v`: in giá trị đỉnh `v`.

Gợi ý: Euler tour — cây con là đoạn `[tin[v], tout[v]]`; "cộng đoạn, hỏi điểm" bằng BIT.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `n - 1` dòng là cạnh, `q` dòng là thao tác (1 ≤ x ≤ 10^4).", "Kết quả các thao tác loại 2.",
    ["5 4\n1 2\n1 3\n3 4\n3 5\n1 3 5\n2 4\n1 1 1\n2 2\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["Euler tour", "BIT"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**4)
    es = rtree(r, n)
    qs = []
    for _ in range(q):
        k = r.randint(1, min(n, 20))
        qs.append(J(k, *[r.randint(1, n) for _ in range(k)]))
    return lines(J(n, q), *(J(a, b) for a, b in es), *qs)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        k = rd.int(); vs = rd.ints(k); w = vs[0]
        for v in vs[1:]:
            w = tr.lca(w, v)
        out.append(w)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        k = rd.int(); vs = rd.ints(k)
        best = max((u for u in range(1, n + 1) if all(tr.is_anc(u, v) for v in vs)), key=lambda u: tr.dep[u])
        out.append(best)
    return out


add(T, "Tổ tiên chung của nhóm", 3, """
Với mỗi truy vấn gồm `k` đỉnh, tìm tổ tiên chung sâu nhất của cả nhóm (gốc là 1).

Gợi ý: `lca` có tính kết hợp: `lca(v1, v2, ..., vk) = lca(lca(v1, v2), v3, ...)`.
(Mẹo hay: chỉ cần LCA của hai đỉnh có `tin` nhỏ nhất và lớn nhất.)
""", "Dòng đầu `n, q` (1 ≤ n ≤ 10^5, 1 ≤ q ≤ 10^4). `n - 1` dòng là cạnh. `q` dòng sau, mỗi dòng `k` (1 ≤ k ≤ 20) rồi `k` đỉnh.",
    "Mỗi truy vấn in một dòng.", ["5 2\n1 2\n1 3\n3 4\n3 5\n2 4 5\n3 2 4 5\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA"])


# 14 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); c = [0] * (n + 1)
    for _ in range(m):
        a, b, x = rd.ints(3); w = tr.lca(a, b)
        c[a] += x; c[b] += x; c[w] -= x
        if tr.par[w]:
            c[tr.par[w]] -= x
    for v in reversed(tr.order):
        if tr.par[v]:
            c[tr.par[v]] += c[v]
    return L(c[1:])


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es, _ = _read_tree(rd, n); c = [0] * (n + 1)
    for _ in range(m):
        a, b, x = rd.ints(3)
        for v in _br_path(n, es, a, b):
            c[v] += x
    return L(c[1:])


add(T, "Cộng trên đường đi", 3, """
Cây `n` đỉnh, ban đầu giá trị 0. Thực hiện `m` thao tác `(a, b, x)`: cộng `x` vào mọi đỉnh trên đường đi từ `a` tới `b`. In giá trị cuối cùng các đỉnh.

Gợi ý: mảng hiệu trên cây (như bài đếm đường đi) — `c[a] += x, c[b] += x, c[lca] -= x, c[cha(lca)] -= x`, rồi cộng dồn từ lá lên.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). `n - 1` dòng là cạnh, `m` dòng sau mỗi dòng `a b x` (1 ≤ x ≤ 10^4).", "Một dòng gồm `n` số.",
    ["5 2\n1 2\n1 3\n3 4\n3 5\n2 4 1\n4 5 10\n"],
    _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n), r.randint(1, 10**4))), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA", "mảng hiệu trên cây"])


# 15 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); c = [0] * (n + 1)
    for _ in range(m):
        a, b = rd.ints(2); w = tr.lca(a, b)
        c[a] += 1; c[b] += 1; c[w] -= 2
    for v in reversed(tr.order):
        if tr.par[v]:
            c[tr.par[v]] += c[v]
    return L(c[b] if tr.par[b] == a else c[a] for a, b in es)


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es, _ = _read_tree(rd, n)
    from collections import Counter
    cnt = Counter()
    for _ in range(m):
        p = _br_path(n, es, *rd.ints(2))
        for i in range(len(p) - 1):
            cnt[frozenset((p[i], p[i + 1]))] += 1
    return L(cnt[frozenset(e)] for e in es)


add(T, "Đếm đường đi qua mỗi cạnh", 3, """
Cho cây và `m` đường đi `(a, b)`. Với mỗi cạnh (theo thứ tự nhập), đếm số đường đi đi qua cạnh đó.

Gợi ý: mảng hiệu trên **cạnh** — gán mỗi cạnh cho đỉnh con của nó: `c[a]++, c[b]++, c[lca] -= 2`, cộng dồn lên gốc.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). `n - 1` dòng là cạnh, `m` dòng là các đường đi.", "Một dòng gồm `n - 1` số.",
    ["5 3\n1 2\n1 3\n3 4\n3 5\n1 3\n2 5\n1 4\n"], _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n))), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA", "mảng hiệu trên cây"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    es = rtree(r, n)
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *(J(a, b) for a, b in es),
                 *(J(r.randint(1, n), r.randint(1, 10**9)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es)
    # mx[j][v] = max giá trị trên 2^j tổ tiên đầu tiên của v (không tính v)
    up = tr.up; mx = [[val[up[0][v]] if v != 1 else 0 for v in range(n + 1)]]
    for j in range(1, tr.LOG):
        pm, pu = mx[-1], up[j - 1]
        mx.append([max(pm[v], pm[pu[v]]) for v in range(n + 1)])
    out = []
    for _ in range(q):
        v, x = rd.ints(2)
        if val[v] >= x:
            out.append(v); continue
        u, rem = v, tr.dep[v]
        for j in range(tr.LOG - 1, -1, -1):
            if (1 << j) <= rem and mx[j][u] < x:
                u = up[j][u]; rem -= 1 << j
        out.append(up[0][u] if rem > 0 else -1)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        v, x = rd.ints(2)
        while v and val[v] < x:
            v = tr.par[v]
        out.append(v if v else -1)
    return out


add(T, "Tổ tiên đủ lớn gần nhất", 4, """
Cây gốc 1, đỉnh có giá trị `a_v`. Với truy vấn `(v, x)`: tìm đỉnh `u` **gần `v` nhất** trên đường từ `v` lên gốc (kể cả `v`) mà `a_u ≥ x`; in `-1` nếu không có.

Gợi ý: nhảy nhị phân với `mx[j][v]` = max giá trị trên `2^j` tổ tiên kế tiếp. Nhảy khi đoạn đó vẫn toàn giá trị `< x`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` giá trị (1 ≤ a ≤ 10^9). `n - 1` dòng là cạnh. `q` dòng sau mỗi dòng `v x`.",
    "Mỗi truy vấn in một dòng.", ["5 3\n9 2 5 1 3\n1 2\n1 3\n3 4\n3 5\n4 4\n4 6\n5 10\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["nhảy nhị phân"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 10**5), S(s, 1, 10**5)
    es = rtree(r, n)
    ops = [J(1, r.randint(1, n), r.randint(1, 10**9)) if r.random() < .5 else J(2, r.randint(1, n), r.randint(1, n)) for _ in range(q)]
    return lines(J(n, q), L(arr(r, n, 1, 10**9)), *(J(a, b) for a, b in es), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); b = _BIT(n + 1)

    def radd(v, x):
        b.add(tr.tin[v] + 1, x); b.add(tr.tout[v] + 2, -x)

    def root_sum(v):
        return b.sum(tr.tin[v] + 1)
    for v in range(1, n + 1):
        radd(v, val[v])
    out = []
    for _ in range(q):
        t, x, y = rd.ints(3)
        if t == 1:
            radd(x, y - val[x]); val[x] = y
        else:
            w = tr.lca(x, y)
            out.append(root_sum(x) + root_sum(y) - 2 * root_sum(w) + val[w])
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); val = [0] + rd.ints(n); es, _ = _read_tree(rd, n); out = []
    for _ in range(q):
        t, x, y = rd.ints(3)
        if t == 1:
            val[x] = y
        else:
            out.append(sum(val[v] for v in _br_path(n, es, x, y)))
    return out


add(T, "Tổng trên đường đi có cập nhật", 4, """
Cây có giá trị trên đỉnh. Thao tác:
- `1 v x`: đổi giá trị đỉnh `v` thành `x`;
- `2 a b`: in tổng giá trị các đỉnh trên đường đi từ `a` tới `b`.

Gợi ý: `S(v)` = tổng từ gốc tới `v` (duy trì bằng Euler tour + BIT như bài "Tổng đường đi tới gốc").
Tổng trên đường `a → b` = `S(a) + S(b) - 2·S(lca) + val[lca]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). Dòng hai gồm `n` giá trị. `n - 1` dòng là cạnh, `q` dòng là thao tác (giá trị ≤ 10^9).",
    "Kết quả các thao tác loại 2.", ["5 3\n1 2 3 4 5\n1 2\n1 3\n3 4\n3 5\n2 2 4\n1 1 10\n2 4 5\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 10**6 else _sol(s), tags=["LCA", "Euler tour", "BIT"])


# 18 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es)
    sz = [1] * (n + 1)
    for v in reversed(tr.order):
        if tr.par[v]:
            sz[tr.par[v]] += sz[v]
    out = []
    for _ in range(q):
        a, b = rd.ints(2)
        if a == b:
            out.append(n); continue
        d = tr.d(a, b)
        if d % 2:
            out.append(0); continue
        if tr.dep[a] < tr.dep[b]:
            a, b = b, a
        w = tr.lca(a, b)
        mid = tr.kth_anc(a, d // 2)
        if tr.dep[a] == tr.dep[b]:
            out.append(n - sz[tr.kth_anc(a, d // 2 - 1)] - sz[tr.kth_anc(b, d // 2 - 1)])
        else:
            out.append(sz[mid] - sz[tr.kth_anc(a, d // 2 - 1)])
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        a, b = rd.ints(2)
        out.append(sum(1 for v in range(1, n + 1) if tr.d(a, v) == tr.d(b, v)))
    return out


add(T, "Phòng học cách đều", 5, """
Trường học có `n` phòng nối thành cây. Với truy vấn `(a, b)`: đếm số phòng `v` có khoảng cách tới `a` **bằng** khoảng cách tới `b`.

Gợi ý: nếu `dist(a, b)` lẻ thì đáp án 0. Ngược lại gọi `m` là trung điểm đường đi (giả sử `a` sâu hơn, `m` = tổ tiên thứ `d/2` của `a`).
Nếu `a`, `b` cùng độ sâu thì `m = lca`, đáp án `n - sz[con của m về phía a] - sz[con của m về phía b]`;
ngược lại đáp án `sz[m] - sz[con của m về phía a]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n - 1` dòng là cạnh, `q` dòng là truy vấn.", "Mỗi truy vấn in một dòng.",
    ["4 1\n1 2\n1 3\n2 4\n2 3\n", "4 2\n1 2\n2 3\n2 4\n1 2\n1 3\n"],
    _tree_q(lambda r, n: J(r.randint(1, n), r.randint(1, n)), nmax=10**5, qmax=10**5), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 3 * 10**4 else _sol(s), tags=["LCA", "nhảy nhị phân"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 10**5)
    return lines(str(q), *(str(r.randint(1, 4 + 2 * i if r.random() < .7 else 4)) for i in range(q)))


def _sol(s):
    rd = Rd(s); q = rd.int()
    N = 4 + 2 * q + 1; LOG = max(1, N.bit_length())
    up = [[0] * (N + 1) for _ in range(LOG)]; dep = [0] * (N + 1)
    for v in (2, 3, 4):
        dep[v] = 1
        for j in range(LOG):
            up[j][v] = 1
    for j in range(LOG):
        up[j][1] = 1

    def lca(u, v):
        if dep[u] < dep[v]:
            u, v = v, u
        k = dep[u] - dep[v]; j = 0
        while k:
            if k & 1:
                u = up[j][u]
            k >>= 1; j += 1
        if u == v:
            return u
        for j in range(LOG - 1, -1, -1):
            if up[j][u] != up[j][v]:
                u, v = up[j][u], up[j][v]
        return up[0][u]

    def dist(u, v):
        return dep[u] + dep[v] - 2 * dep[lca(u, v)]
    a, b, d = 2, 3, 2; cnt = 4; out = []
    for _ in range(q):
        v = rd.int()
        for _ in range(2):
            cnt += 1; w = cnt; dep[w] = dep[v] + 1; up[0][w] = v
            for j in range(1, LOG):
                up[j][w] = up[j - 1][up[j - 1][w]]
        w = cnt  # hai lá mới đối xứng, chỉ cần xét một
        da, db = dist(w, a), dist(w, b)
        if da > d and da >= db:
            b, d = w, da
        elif db > d:
            a, d = w, db
        out.append(d)
    return out


def _br(s):
    rd = Rd(s); q = rd.int()
    adj = {1: [2, 3, 4], 2: [1], 3: [1], 4: [1]}; cnt = 4; out = []
    for _ in range(q):
        v = rd.int()
        for _ in range(2):
            cnt += 1; adj[cnt] = [v]; adj[v].append(cnt)

        def far(src):
            d = {src: 0}; st = [src]
            while st:
                u = st.pop()
                for x in adj[u]:
                    if x not in d:
                        d[x] = d[u] + 1; st.append(x)
            best = max(d, key=d.get)
            return best, d[best]
        a, _ = far(1); _, dd = far(a); out.append(dd)
    return out


add(T, "Cây năm mới", 4, """
Ban đầu cây có 4 đỉnh: đỉnh 1 nối với 2, 3, 4. Mỗi thao tác chọn một đỉnh `v` hiện có và gắn thêm hai đỉnh con mới (số hiệu `n + 1` và `n + 2`,
với `n` là số đỉnh hiện tại) vào `v`. Sau mỗi thao tác, in đường kính của cây.

Gợi ý: giữ hai đầu mút `a, b` của đường kính. Khi thêm đỉnh mới `w`, đường kính mới hoặc giữ nguyên, hoặc là `(w, a)` hay `(w, b)`.
Khoảng cách tính bằng LCA với nhảy nhị phân (xây dần khi thêm đỉnh).
""", "Dòng đầu `q` (1 ≤ q ≤ 10^5). `q` dòng sau mỗi dòng là đỉnh `v` được chọn (đã tồn tại tại thời điểm đó).", "Mỗi thao tác in một dòng.",
    ["5\n2\n3\n4\n8\n5\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 300 else _sol(s), tags=["LCA", "đường kính"])


# 20 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n)
    tr = Tree(n, es); out = []
    for _ in range(q):
        a, b, c, d = rd.ints(4)
        # phần chung của hai đường đi (nếu có) nằm giữa hai đỉnh "sâu nhất" trong {lca(a,c), lca(a,d), lca(b,c), lca(b,d)}
        cand = sorted([tr.lca(a, c), tr.lca(a, d), tr.lca(b, c), tr.lca(b, d)], key=lambda v: -tr.dep[v])
        x, y = cand[0], cand[1]
        w1, w2 = tr.lca(a, b), tr.lca(c, d)
        deep = w1 if tr.dep[w1] > tr.dep[w2] else w2
        if tr.dep[x] < tr.dep[deep] or tr.dep[y] < tr.dep[deep]:
            out.append(0)
        else:
            out.append(tr.d(x, y) + 1)
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); es, _ = _read_tree(rd, n); out = []
    for _ in range(q):
        a, b, c, d = rd.ints(4)
        out.append(len(set(_br_path(n, es, a, b)) & set(_br_path(n, es, c, d))))
    return out


add(T, "Giao của hai đường đi", 5, """
Với truy vấn `(a, b, c, d)`: đếm số đỉnh thuộc **cả** đường đi `a → b` và đường đi `c → d` trên cây.

Gợi ý: giao của hai đường đi trên cây (nếu khác rỗng) cũng là một đường đi. Hai đầu mút của nó là hai đỉnh sâu nhất trong
`lca(a,c), lca(a,d), lca(b,c), lca(b,d)`. Giao rỗng nếu các đỉnh này nông hơn `max(lca(a,b), lca(c,d))` (theo độ sâu).
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 10^5). `n - 1` dòng là cạnh, `q` dòng sau mỗi dòng `a b c d`.", "Mỗi truy vấn in một dòng.",
    ["6 2\n1 2\n1 3\n3 4\n3 5\n5 6\n2 6 4 6\n2 4 5 6\n"],
    _tree_q(lambda r, n: J(*(r.randint(1, n) for _ in range(4))), nmax=10**5, qmax=10**5), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) * int(s.split()[1]) <= 3 * 10**5 else _sol(s), tags=["LCA"])


# 21 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); es, _ = _read_tree(rd, n)
    tr = Tree(n, es)
    out = []
    # dựng lại Euler tour (vào/ra) theo thứ tự con tăng dần
    it = [0] * (n + 1); st = [1]; out.append(1)
    while st:
        u = st[-1]
        if it[u] < len(tr.adj[u]):
            v = tr.adj[u][it[u]][0]; it[u] += 1
            if v != tr.par[u]:
                out.append(v); st.append(v)
        else:
            st.pop()
            if st:
                out.append(st[-1])
    return L(out)


add(T, "Hành trình Euler", 1, """
Cho cây gốc 1. Thực hiện DFS từ gốc, tại mỗi đỉnh thăm các con theo thứ tự số hiệu **tăng dần**. Ghi lại đỉnh hiện tại mỗi khi
đi vào một đỉnh và mỗi khi quay về từ một đỉnh con. In dãy ghi được (độ dài `2n - 1`).

Gợi ý: đây là **Euler tour** dùng cho LCA bằng RMQ: `lca(u, v)` là đỉnh có độ sâu nhỏ nhất giữa hai lần xuất hiện đầu tiên của `u` và `v`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Một dòng gồm `2n - 1` số.",
    ["5\n1 2\n1 3\n3 4\n3 5\n"], lambda r, s: (lambda n: lines(str(n), *(J(a, b) for a, b in rtree(r, n))))(S(s, 1, 2 * 10**5)), _sol,
    tags=["Euler tour", "DFS"])
