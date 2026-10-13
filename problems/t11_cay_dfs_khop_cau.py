"""Chuyên đề 11: Cây DFS, đỉnh khớp và cầu."""
from collections import deque
from .base import add, Rd, S, J, L, arr, lines, rtree, rgraph, rdigraph

T = 11


def _tree_input(r, s, weighted=False, nmin=1, nmax=2 * 10**5):
    n = S(s, nmin, nmax)
    es = rtree(r, n)
    if weighted:
        return lines(str(n), *(J(a, b, r.randint(1, 10**9)) for a, b in es))
    return lines(str(n), *(J(a, b) for a, b in es))


def _read_tree(rd, n, weighted=False):
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        if weighted:
            a, b, w = rd.ints(3)
        else:
            a, b = rd.ints(2); w = 1
        adj[a].append((b, w)); adj[b].append((a, w))
    return adj


def _order(adj, root=1):
    n = len(adj) - 1
    par = [0] * (n + 1); dist = [0] * (n + 1); order = [root]; par[root] = -1
    for u in order:
        for v, w in adj[u]:
            if v != par[u]:
                par[v] = u; dist[v] = dist[u] + w; order.append(v)
    return order, par, dist


def _far(adj, src):
    order, par, dist = _order(adj, src)
    best = max(order, key=lambda v: dist[v])
    return best, dist


def lowlink(n, edges):
    """Tarjan lặp: trả về (tin, low, parent_edge, order) — đồ thị vô hướng, edges là list (u, v)."""
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, i)); adj[b].append((a, i))
    tin = [0] * (n + 1); low = [0] * (n + 1); pe = [-1] * (n + 1); par = [0] * (n + 1)
    timer = 0; roots = []
    it = [0] * (n + 1)
    for st in range(1, n + 1):
        if tin[st]:
            continue
        roots.append(st)
        timer += 1; tin[st] = low[st] = timer
        stack = [st]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v, eid = adj[u][it[u]]; it[u] += 1
                if eid == pe[u]:
                    continue
                if tin[v]:
                    low[u] = min(low[u], tin[v])
                else:
                    timer += 1; tin[v] = low[v] = timer; pe[v] = eid; par[v] = u
                    stack.append(v)
            else:
                stack.pop()
                if stack:
                    p = stack[-1]
                    low[p] = min(low[p], low[u])
    return tin, low, pe, par, roots


def bridges(n, edges):
    tin, low, pe, par, _ = lowlink(n, edges)
    return [pe[v] for v in range(1, n + 1) if pe[v] >= 0 and low[v] > tin[par[v]]]


def cut_vertices(n, edges):
    tin, low, pe, par, roots = lowlink(n, edges)
    child = [0] * (n + 1); cut = [False] * (n + 1)
    for v in range(1, n + 1):
        if pe[v] >= 0:
            p = par[v]; child[p] += 1
            if pe[p] >= 0 and low[v] >= tin[p]:
                cut[p] = True
    for r in roots:
        cut[r] = child[r] >= 2
    return [v for v in range(1, n + 1) if cut[v]]


def _gg(r, s, nmax=10**5, mmax=2 * 10**5):
    n = S(s, 2, nmax)
    mode = r.random()
    if mode < .4:  # cây + vài cạnh (nhiều cầu)
        es = rtree(r, n)
        extra = rgraph(r, n, r.randint(0, max(1, n // 10)))
        seen = {(min(a, b), max(a, b)) for a, b in es}
        es += [e for e in extra if (min(e), max(e)) not in seen]
    elif mode < .7:  # các chuỗi vòng nối nhau
        es, seen = [], set()
        v = 1
        while v < n:
            ln = r.randint(2, 6)
            cyc = list(range(v, min(n, v + ln) + 1))
            for i in range(len(cyc) - 1):
                es.append((cyc[i], cyc[i + 1]))
            if len(cyc) > 2 and r.random() < .7:
                es.append((cyc[-1], cyc[0]))
            v = cyc[-1]
        es = list({(min(a, b), max(a, b)) for a, b in es})
        perm = list(range(1, n + 1)); r.shuffle(perm); perm = [0] + perm
        es = [(perm[a], perm[b]) for a, b in es]
    else:
        es = rgraph(r, n, S(s, 1, mmax) // r.choice([1, 2, 4]), connected=r.random() < .5)
    r.shuffle(es)
    return n, es


def _ggs(r, s):
    n, es = _gg(r, s)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _read_edges(s):
    rd = Rd(s); n, m = rd.ints(2)
    return n, [tuple(rd.ints(2)) for _ in range(m)]


def _comps_without(n, edges, skip_vertex=0, skip_edges=()):
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(edges):
        if i in skip_edges or skip_vertex in (a, b):
            continue
        adj[a].append(b); adj[b].append(a)
    seen = [False] * (n + 1); c = 0
    for st in range(1, n + 1):
        if st == skip_vertex or seen[st]:
            continue
        c += 1; seen[st] = True; q = [st]
        while q:
            u = q.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True; q.append(v)
    return c


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(r.randint(max(1, i - r.choice([1, 5, i])), i - 1) for i in range(2, n + 1)))


def _sol(s):
    rd = Rd(s); n = rd.int(); b = [0, 0] + rd.ints(n - 1)
    sz = [0] * (n + 1)
    for v in range(n, 1, -1):
        sz[b[v]] += sz[v] + 1
    return L(sz[1:])


add(T, "Số nhân viên cấp dưới", 1, """
Công ty có `n` nhân viên, nhân viên 1 là giám đốc; mọi nhân viên khác có đúng một sếp trực tiếp. Với mỗi nhân viên, đếm số
nhân viên cấp dưới (trực tiếp hoặc gián tiếp).

Gợi ý: DFS từ gốc, `sub[u] = Σ (sub[con] + 1)`. Ở bài này sếp luôn có số hiệu nhỏ hơn nên có thể duyệt ngược từ `n` về 2.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau gồm `n - 1` số: sếp của nhân viên `2, 3, ..., n`.", "Một dòng gồm `n` số.",
    ["5\n1 1 2 3\n"], _g, _sol, tags=["cây", "DFS"])


# 2 -----------------------------------------------------------------------
add(T, "Độ sâu các đỉnh", 1, """
Cho cây `n` đỉnh, gốc là đỉnh 1 (độ sâu 0). In độ sâu (số cạnh tới gốc) của từng đỉnh.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh của cây.", "Một dòng gồm `n` số.",
    ["5\n1 2\n1 3\n3 4\n3 5\n"], lambda r, s: _tree_input(r, s),
    lambda s: (lambda rd: L(_order(_read_tree(rd, rd.int()))[2][1:]))(Rd(s)), tags=["cây", "DFS"])


# 3 -----------------------------------------------------------------------
def _diam(s, weighted=False):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n, weighted)
    a, _ = _far(adj, 1)
    b, d = _far(adj, a)
    return d[b]


add(T, "Đường kính cây", 1, """
Đường kính của cây là số cạnh trên đường đi dài nhất giữa hai đỉnh. Tính đường kính.

Gợi ý: DFS/BFS từ đỉnh bất kỳ tới đỉnh xa nhất `a`; DFS lần nữa từ `a` tới đỉnh xa nhất `b`. `dist(a, b)` là đường kính.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Đường kính.",
    ["5\n1 2\n1 3\n3 4\n3 5\n"], lambda r, s: _tree_input(r, s), lambda s: _diam(s), tags=["cây", "đường kính"])


# 4 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    q = S(s, 1, 2 * 10**5)
    es = rtree(r, n)
    return lines(J(n, q), *(J(a, b) for a, b in es), *(J(r.randint(1, n), r.randint(1, n)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); adj = _read_tree(rd, n)
    tin = [0] * (n + 1); tout = [0] * (n + 1); timer = 0
    it = [0] * (n + 1); par = [0] * (n + 1); par[1] = -1
    stack = [1]; timer += 1; tin[1] = timer
    while stack:
        u = stack[-1]
        if it[u] < len(adj[u]):
            v = adj[u][it[u]][0]; it[u] += 1
            if v != par[u]:
                par[v] = u; timer += 1; tin[v] = timer; stack.append(v)
        else:
            stack.pop(); tout[u] = timer
    out = []
    for _ in range(q):
        u, v = rd.ints(2)
        out.append("YES" if tin[u] <= tin[v] <= tout[u] else "NO")
    return out


add(T, "Kiểm tra tổ tiên", 2, """
Cho cây gốc 1 và `q` truy vấn `(u, v)`: `u` có phải tổ tiên của `v` không? (Mỗi đỉnh là tổ tiên của chính nó.)

Gợi ý: trong DFS, ghi thời điểm vào `tin[u]` và thời điểm ra `tout[u]`. `u` là tổ tiên của `v` ⇔ `tin[u] ≤ tin[v] ≤ tout[u]`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `n - 1` dòng là các cạnh, `q` dòng là các truy vấn.", "Mỗi truy vấn `YES` hoặc `NO`.",
    ["5 3\n1 2\n1 3\n3 4\n3 5\n1 4\n3 2\n5 5\n"], _g, _sol, tags=["cây DFS", "tin/tout"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n)
    a, _ = _far(adj, 1)
    b, da = _far(adj, a)
    _, db = _far(adj, b)
    return L(max(da[v], db[v]) for v in range(1, n + 1))


def _br(s):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n)
    return L(max(_order(adj, v)[2][1:]) for v in range(1, n + 1))


add(T, "Đỉnh xa nhất", 2, """
Với mỗi đỉnh của cây, in khoảng cách (số cạnh) tới đỉnh xa nó nhất.

Gợi ý: đỉnh xa nhất của mọi đỉnh luôn là một trong hai đầu mút `a`, `b` của đường kính. Đáp án = `max(dist(v, a), dist(v, b))`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Một dòng gồm `n` số.",
    ["5\n1 2\n1 3\n3 4\n3 5\n"], lambda r, s: _tree_input(r, s), _sol, brute=_br, tags=["cây", "đường kính"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n)
    order, par, dist = _order(adj)
    sz = [1] * (n + 1)
    for u in reversed(order[1:]):
        sz[par[u]] += sz[u]
    ans = [0] * (n + 1); ans[1] = sum(dist[1:])
    for u in order[1:]:
        ans[u] = ans[par[u]] + n - 2 * sz[u]
    return L(ans[1:])


def _br(s):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n)
    return L(sum(_order(adj, v)[2][1:]) for v in range(1, n + 1))


add(T, "Tổng khoảng cách", 3, """
Với mỗi đỉnh `v` của cây, tính tổng khoảng cách từ `v` tới tất cả các đỉnh khác.

Gợi ý (đổi gốc - rerooting): tính `ans[1]` bằng một lần DFS. Khi chuyển gốc từ `p` sang con `u`, có `sz[u]` đỉnh gần thêm 1
và `n - sz[u]` đỉnh xa thêm 1: `ans[u] = ans[p] + n - 2·sz[u]`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Một dòng gồm `n` số.",
    ["5\n1 2\n1 3\n3 4\n3 5\n"], lambda r, s: _tree_input(r, s), _sol, brute=_br, tags=["cây", "đổi gốc"])


# 7 -----------------------------------------------------------------------
def _br_bridges(s):
    n, es = _read_edges(s)
    base = _comps_without(n, es)
    return [i for i in range(len(es)) if _comps_without(n, es, skip_edges={i}) > base]


add(T, "Đếm cầu", 2, """
Cầu là cạnh mà khi xoá đi thì số thành phần liên thông tăng lên. Đếm số cầu của đồ thị vô hướng đơn.

Gợi ý (Tarjan): DFS, tính `tin[u]` và `low[u]` = `tin` nhỏ nhất tới được từ cây con của `u` bằng tối đa một cạnh ngược.
Cạnh cây `(p, u)` là cầu ⇔ `low[u] > tin[p]`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh (không lặp, không khuyên).", "Số cầu.",
    ["6 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n"], _ggs, lambda s: len(bridges(*_read_edges(s))),
    brute=lambda s: len(_br_bridges(s)), tags=["cầu", "Tarjan"])


# 8 -----------------------------------------------------------------------
def _br_cuts(s):
    n, es = _read_edges(s)
    out = []
    for v in range(1, n + 1):
        base = _comps_without(n, es, skip_vertex=v)
        # so với đồ thị gốc bỏ đi đỉnh v nhưng tính v như một thành phần riêng nếu nó cô lập
        deg = sum(1 for a, b in es if v in (a, b))
        if deg and base > _comps_without(n, es) - (0 if deg else 1):
            out.append(v)
    return out


add(T, "Đếm đỉnh khớp", 2, """
Đỉnh khớp là đỉnh mà khi xoá nó (cùng các cạnh kề) thì số thành phần liên thông tăng lên. Đếm số đỉnh khớp.

Gợi ý: với đỉnh `p` không phải gốc DFS, `p` là khớp nếu có con `u` với `low[u] ≥ tin[p]`. Gốc DFS là khớp ⇔ có từ 2 con trở lên trong cây DFS.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "Số đỉnh khớp.",
    ["6 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n"], _ggs, lambda s: len(cut_vertices(*_read_edges(s))),
    brute=lambda s: len(_br_cuts(s)), tags=["khớp", "Tarjan"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    n, es = _read_edges(s)
    out = sorted((min(es[i]), max(es[i])) for i in bridges(n, es))
    return lines(str(len(out)), *(J(a, b) for a, b in out)).rstrip("\n")


def _br(s):
    n, es = _read_edges(s)
    out = sorted((min(es[i]), max(es[i])) for i in _br_bridges(s))
    return lines(str(len(out)), *(J(a, b) for a, b in out)).rstrip("\n")


add(T, "Liệt kê cầu", 3, """
Liệt kê tất cả các cầu. Mỗi cầu in dạng `u v` với `u < v`; các cầu sắp xếp tăng dần theo `u`, rồi theo `v`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.",
    "Dòng đầu là số cầu `k`, `k` dòng sau là các cầu.", ["6 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n"], _ggs, _sol, brute=_br,
    tags=["cầu", "Tarjan"])


# 10 ----------------------------------------------------------------------
add(T, "Liệt kê đỉnh khớp", 3, """
Liệt kê các đỉnh khớp theo thứ tự tăng dần.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.",
    "Dòng đầu là số đỉnh khớp `k`, dòng hai là các đỉnh khớp (bỏ trống nếu `k = 0`).",
    ["6 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n"], _ggs,
    lambda s: (lambda c: lines(str(len(c)), L(c)).rstrip("\n"))(cut_vertices(*_read_edges(s))),
    brute=lambda s: (lambda c: lines(str(len(c)), L(c)).rstrip("\n"))(_br_cuts(s)), tags=["khớp", "Tarjan"])


# 11 ----------------------------------------------------------------------
def _sol(s):
    n, es = _read_edges(s)
    tin, low, pe, par, roots = lowlink(n, es)
    base = len(roots)
    split = [0] * (n + 1)  # số con u với low[u] >= tin[p]
    child = [0] * (n + 1)
    for v in range(1, n + 1):
        if pe[v] >= 0:
            p = par[v]; child[p] += 1
            if low[v] >= tin[p]:
                split[p] += 1
    isroot = [False] * (n + 1)
    for r_ in roots:
        isroot[r_] = True
    out = []
    for v in range(1, n + 1):
        if isroot[v]:
            out.append(base - 1 + child[v])
        else:
            out.append(base + split[v])
    return L(out)


def _br(s):
    n, es = _read_edges(s)
    return L(_comps_without(n, es, skip_vertex=v) for v in range(1, n + 1))


add(T, "Xoá từng đỉnh", 4, """
Với mỗi đỉnh `v`, nếu xoá `v` (cùng các cạnh kề) thì đồ thị còn lại có bao nhiêu thành phần liên thông?

Gợi ý: gọi `C` là số thành phần ban đầu. Với `v` không phải gốc DFS: đáp án `C + (số con u có low[u] ≥ tin[v])`.
Với gốc DFS: `C - 1 + (số con trong cây DFS)`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "Một dòng gồm `n` số.",
    ["5 5\n1 2\n2 3\n3 1\n3 4\n4 5\n"], _ggs, _sol, brute=_br, tags=["khớp", "Tarjan"])


# 12 ----------------------------------------------------------------------
add(T, "Đường kính cây có trọng số", 2, """
Cây có trọng số trên cạnh. Tìm tổng trọng số lớn nhất trên đường đi giữa hai đỉnh.

Gợi ý: hai lần DFS như bài đường kính, nhưng khoảng cách là tổng trọng số (trọng số dương).
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).", "Đường kính.",
    ["4\n1 2 3\n2 3 4\n2 4 10\n"], lambda r, s: _tree_input(r, s, weighted=True), lambda s: _diam(s, True),
    tags=["cây", "đường kính"])


# 13 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n)
    order, par, _ = _order(adj)
    used = [False] * (n + 1); c = 0
    for u in reversed(order):
        p = par[u]
        if p > 0 and not used[u] and not used[p]:
            used[u] = used[p] = True; c += 1
    return c


def _br(s):
    rd = Rd(s); n = rd.int(); es = [rd.ints(2) for _ in range(n - 1)]
    best = 0
    for m in range(1 << len(es)):
        used = set(); ok = True; c = 0
        for i, (a, b) in enumerate(es):
            if m >> i & 1:
                if a in used or b in used:
                    ok = False; break
                used |= {a, b}; c += 1
        if ok:
            best = max(best, c)
    return best


add(T, "Ghép cặp trên cây", 3, """
Chọn nhiều cạnh nhất của cây sao cho không có hai cạnh được chọn chung đỉnh (cặp ghép cực đại).

Gợi ý (tham lam): xét các đỉnh từ lá lên gốc; nếu đỉnh `u` và cha của nó đều chưa được ghép thì ghép cạnh `(u, cha)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Số cạnh tối đa.",
    ["5\n1 2\n1 3\n3 4\n3 5\n"], lambda r, s: _tree_input(r, s), _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 15 else _sol(s), tags=["cây", "tham lam"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n, es = _gg(r, s)
    q = S(s, 1, 10**5)
    qs = [r.choice(es) if es else (1, 2) for _ in range(q)]
    qs = [(b, a) if r.random() < .5 else (a, b) for a, b in qs]
    return lines(J(n, len(es), q), *(J(a, b) for a, b in es), *(J(a, b) for a, b in qs))


def _sol(s):
    rd = Rd(s); n, m, q = rd.ints(3)
    es = [tuple(rd.ints(2)) for _ in range(m)]
    br = {(min(es[i]), max(es[i])) for i in bridges(n, es)}
    out = []
    for _ in range(q):
        a, b = rd.ints(2)
        out.append("YES" if (min(a, b), max(a, b)) in br else "NO")
    return out


add(T, "Cạnh quan trọng", 3, """
Cho đồ thị vô hướng và `q` truy vấn, mỗi truy vấn là một cạnh `(u, v)` có trong đồ thị. Nếu chỉ xoá cạnh đó thì số thành phần
liên thông có tăng không? In `YES` hoặc `NO`.
""", "Dòng đầu `n, m, q` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5, 1 ≤ q ≤ 10^5). `m` dòng là các cạnh, `q` dòng là các truy vấn.",
    "Mỗi truy vấn in một dòng.", ["4 4 2\n1 2\n2 3\n3 1\n3 4\n4 3\n2 1\n"], _g, _sol, tags=["cầu"])


# 15 ----------------------------------------------------------------------
def _sol(s):
    n, es = _read_edges(s)
    br = set(bridges(n, es))
    return _comps_without(n, es, skip_edges=br)


add(T, "Thành phần song liên thông cạnh", 4, """
Hai đỉnh thuộc cùng một **thành phần song liên thông cạnh** nếu giữa chúng có hai đường đi không chung cạnh nào.
Đếm số thành phần như vậy (mỗi đỉnh cô lập là một thành phần).

Gợi ý: xoá tất cả các cầu, mỗi thành phần liên thông còn lại chính là một thành phần song liên thông cạnh.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "Số thành phần.",
    ["6 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n"], _ggs, _sol, tags=["cầu", "song liên thông"])


# 16 ----------------------------------------------------------------------
def _sol(s):
    n, es = _read_edges(s)
    tin, low, pe, par, roots = lowlink(n, es)
    # kích thước cây con DFS và kích thước thành phần
    sz = [1] * (n + 1)
    order = sorted(range(1, n + 1), key=lambda v: -tin[v])
    for v in order:
        if pe[v] >= 0:
            sz[par[v]] += sz[v]
    root_of = [0] * (n + 1)
    for v in sorted(range(1, n + 1), key=lambda v: tin[v]):
        root_of[v] = v if pe[v] < 0 else root_of[par[v]]
    ans = [0] * len(es)
    for v in range(1, n + 1):
        if pe[v] >= 0 and low[v] > tin[par[v]]:
            ans[pe[v]] = sz[v] * (sz[root_of[v]] - sz[v])
    return L(ans)


def _br(s):
    n, es = _read_edges(s)
    out = []
    for i in range(len(es)):
        adj = [[] for _ in range(n + 1)]
        for j, (a, b) in enumerate(es):
            if j != i:
                adj[a].append(b); adj[b].append(a)
        a = es[i][0]; seen = {a}; st = [a]
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); st.append(v)
        if es[i][1] in seen:
            out.append(0); continue
        b = es[i][1]; seen2 = {b}; st = [b]
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in seen2:
                    seen2.add(v); st.append(v)
        out.append(len(seen) * len(seen2))
    return L(out)


add(T, "Thiệt hại khi đứt cáp", 4, """
Mạng cáp gồm `n` máy và `m` sợi cáp hai chiều. Với **mỗi sợi cáp** (theo thứ tự nhập), nếu chỉ sợi đó bị đứt thì có bao nhiêu
cặp máy (không kể thứ tự) đang liên lạc được với nhau sẽ bị mất liên lạc?

Gợi ý: chỉ cầu mới gây thiệt hại. Với cầu `(p, u)` trong cây DFS: thiệt hại = `sz[u] · (kích thước thành phần − sz[u])`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "Một dòng gồm `m` số.",
    ["5 5\n1 2\n2 3\n3 1\n3 4\n4 5\n"], _ggs, _sol, brute=_br, tags=["cầu", "đếm"])


# 17 ----------------------------------------------------------------------
def _sol(s):
    n, es = _read_edges(s)
    if _comps_without(n, es) != 1:
        return "NO"
    return "NO" if bridges(n, es) else "YES"


add(T, "Định hướng đường phố", 3, """
Thành phố có `n` nút giao và `m` con đường hai chiều. Thị trưởng muốn biến mọi con đường thành **một chiều** sao cho vẫn đi được
từ mọi nút giao tới mọi nút giao khác. Có làm được không?

Gợi ý (định lý Robbins): làm được ⇔ đồ thị liên thông và **không có cầu**. (Cách định hướng: cạnh cây DFS hướng xuống, cạnh ngược hướng lên.)
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các con đường.", "`YES` hoặc `NO`.",
    ["3 3\n1 2\n2 3\n3 1\n", "3 2\n1 2\n2 3\n"], _ggs, _sol, tags=["cầu"])


# 18 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n = rd.int(); adj = _read_tree(rd, n)
    order, par, _ = _order(adj)
    sz = [1] * (n + 1)
    for u in reversed(order[1:]):
        sz[par[u]] += sz[u]
    best = []
    for u in range(1, n + 1):
        mx = n - sz[u]
        for v, _ in adj[u]:
            if v != par[u]:
                mx = max(mx, sz[v])
        if mx * 2 <= n:
            best.append(u)
    return min(best)


add(T, "Trọng tâm của cây", 3, """
Trọng tâm (centroid) của cây là đỉnh mà khi xoá đi, mọi cây con còn lại đều có không quá `n/2` đỉnh. Một cây có 1 hoặc 2 trọng tâm.
In trọng tâm có số hiệu nhỏ nhất.

Gợi ý: tính `sz[u]`; khi xoá `u` các phần còn lại có kích thước `sz[con]` và `n - sz[u]`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n - 1` dòng sau là các cạnh.", "Số hiệu trọng tâm.",
    ["5\n1 2\n2 3\n3 4\n4 5\n"], lambda r, s: _tree_input(r, s), _sol, tags=["cây", "trọng tâm"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n, es = _gg(r, s)
    # đảm bảo liên thông: nối thêm các thành phần
    from .base import rtree as _rt
    comp = list(range(n + 1))

    def f(x):
        while comp[x] != x:
            comp[x] = comp[comp[x]]; x = comp[x]
        return x
    for a, b in es:
        comp[f(a)] = f(b)
    roots = sorted({f(v) for v in range(1, n + 1)})
    for i in range(1, len(roots)):
        es.append((roots[i - 1], roots[i]))
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    n, es = _read_edges(s)
    br = set(bridges(n, es))
    # nén thành phần song liên thông cạnh
    comp = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    for i, (a, b) in enumerate(es):
        if i not in br:
            adj[a].append(b); adj[b].append(a)
    c = 0
    for st in range(1, n + 1):
        if not comp[st]:
            c += 1; comp[st] = c; q = [st]
            while q:
                u = q.pop()
                for v in adj[u]:
                    if not comp[v]:
                        comp[v] = c; q.append(v)
    tree = [[] for _ in range(c + 1)]
    for i in br:
        a, b = es[i]
        tree[comp[a]].append((comp[b], 1)); tree[comp[b]].append((comp[a], 1))
    a, _ = _far(tree, 1)
    b, d = _far(tree, a)
    return len(br) - d[b]


def _br(s):
    n, es = _read_edges(s)
    best = len(bridges(n, es))
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            best = min(best, len(bridges(n, es + [(u, v)])))
    return best


add(T, "Thêm một cạnh", 5, """
Cho đồ thị vô hướng **liên thông**. Bạn được thêm đúng một cạnh mới (giữa hai đỉnh bất kỳ, có thể trùng cạnh cũ).
Số cầu ít nhất còn lại là bao nhiêu?

Gợi ý: nén mỗi thành phần song liên thông cạnh thành một đỉnh → được **cây cầu** (bridge tree). Thêm cạnh `(u, v)` sẽ "phá" mọi cầu
trên đường đi giữa chúng trong cây cầu → chọn hai đầu mút đường kính. Đáp án = số cầu − đường kính cây cầu.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "Số cầu ít nhất.",
    ["6 5\n1 2\n2 3\n3 4\n3 5\n5 6\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 12 else _sol(s),
    tags=["cầu", "đường kính", "nén đồ thị"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rdigraph(r, n, m, dag=r.random() < .3)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = rd.ints(2); adj[a].append(b)
    tin = [0] * (n + 1); tout = [0] * (n + 1); timer = 0
    cnt = {"tree": 0, "back": 0, "forward": 0, "cross": 0}
    it = [0] * (n + 1)
    for st in range(1, n + 1):
        if tin[st]:
            continue
        timer += 1; tin[st] = timer; stack = [st]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]; it[u] += 1
                if not tin[v]:
                    cnt["tree"] += 1; timer += 1; tin[v] = timer; stack.append(v)
                elif not tout[v]:
                    cnt["back"] += 1
                elif tin[v] > tin[u]:
                    cnt["forward"] += 1
                else:
                    cnt["cross"] += 1
            else:
                timer += 1; tout[u] = timer; stack.pop()
    return J(cnt["tree"], cnt["back"], cnt["forward"], cnt["cross"])


add(T, "Phân loại cung trong cây DFS", 4, """
Chạy DFS trên đồ thị **có hướng**: duyệt các đỉnh xuất phát theo thứ tự `1, 2, ..., n` (bỏ qua đỉnh đã thăm), và tại mỗi đỉnh duyệt
các cung đi ra **theo thứ tự nhập vào**. Mỗi cung `u → v` thuộc một trong bốn loại:
- **cung cây**: `v` chưa thăm;
- **cung ngược**: `v` là tổ tiên của `u` (đang nằm trên ngăn xếp DFS);
- **cung xuôi**: `v` là hậu duệ đã thăm xong của `u`;
- **cung ngang**: các trường hợp còn lại.

In số lượng cung mỗi loại theo thứ tự trên.

Gợi ý: dùng `tin`/`tout`. Đồ thị có chu trình ⇔ có cung ngược.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v`.", "Bốn số: cây, ngược, xuôi, ngang.",
    ["4 6\n1 2\n2 3\n3 1\n1 3\n4 3\n2 4\n"], _g, _sol, tags=["cây DFS"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, -10**9, 10**9)), *(J(a, b) for a, b in rtree(r, n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); w = rd.ints(n)
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = rd.ints(2); adj[a].append((b, 1)); adj[b].append((a, 1))
    order, par, _ = _order(adj)
    best = [0] * (n + 1)
    for u in reversed(order):
        best[u] += w[u - 1]
        p = par[u]
        if p > 0 and best[u] > 0:
            best[p] += best[u]
    return max(best[1:])


def _br(s):
    rd = Rd(s); n = rd.int(); w = rd.ints(n); es = [rd.ints(2) for _ in range(n - 1)]
    ans = -10**18
    for m in range(1, 1 << n):
        vs = [i + 1 for i in range(n) if m >> i & 1]
        st = {vs[0]}; q = [vs[0]]; S_ = set(vs)
        while q:
            u = q.pop()
            for a, b in es:
                for x, y in ((a, b), (b, a)):
                    if x == u and y in S_ and y not in st:
                        st.add(y); q.append(y)
        if len(st) == len(vs):
            ans = max(ans, sum(w[v - 1] for v in vs))
    return ans


add(T, "Cây con liên thông có tổng lớn nhất", 5, """
Mỗi đỉnh của cây có trọng số (có thể âm). Chọn một tập đỉnh **khác rỗng, liên thông** (tạo thành một cây con) có tổng trọng số lớn nhất.

Gợi ý: `best[u]` = tổng lớn nhất của tập liên thông có đỉnh cao nhất là `u` = `w_u + Σ max(0, best[con])`. Đáp án `max best[u]`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng hai gồm `n` trọng số (|w| ≤ 10^9). `n - 1` dòng sau là các cạnh.", "Tổng lớn nhất.",
    ["5\n-1 3 -2 4 -5\n1 2\n1 3\n2 4\n3 5\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 12 else _sol(s),
    tags=["QHĐ trên cây"])
