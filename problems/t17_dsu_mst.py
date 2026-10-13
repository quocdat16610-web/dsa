"""Chuyên đề 17: Disjoint Set Union (DSU), cây khung nhỏ nhất (Kruskal, Prim)."""
from collections import deque
from bisect import bisect_right
from .base import add, Rd, S, J, L, arr, lines, rgraph, rtree

T = 17


class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1)); self.sz = [1] * (n + 1); self.comps = n

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a; self.sz[a] += self.sz[b]; self.comps -= 1
        return True


def kruskal(n, es):
    """es: list (w, u, v). Trả về (tổng, danh sách cạnh trong cây) hoặc (None, ...) nếu không liên thông."""
    d = DSU(n); tot = 0; used = []
    for w, u, v in sorted(es):
        if d.union(u, v):
            tot += w; used.append((w, u, v))
    return (tot if d.comps == 1 else None), used


def _gw(nmax=10**5, mmax=2 * 10**5, whi=10**9, conn=None):
    def g(r, s):
        n = S(s, 2, nmax); m = S(s, 1, mmax)
        c = conn if conn is not None else r.random() < .8
        es = rgraph(r, n, max(m, n - 1) if c else m, connected=c)
        wh = whi if r.random() < .7 else 10
        return lines(J(n, len(es)), *(J(a, b, r.randint(1, wh)) for a, b in es))
    return g


def _read_wes(rd, m):
    out = []
    for _ in range(m):
        a, b, w = rd.ints(3); out.append((w, a, b))
    return out


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    ops = [J("union" if r.random() < .5 else "get", r.randint(1, n), r.randint(1, n)) for _ in range(q)]
    return lines(J(n, q), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); d = DSU(n); out = []
    for _ in range(q):
        t, a, b = rd.str(), int(rd.str()), int(rd.str())
        if t == "union":
            d.union(a, b)
        else:
            out.append("YES" if d.find(a) == d.find(b) else "NO")
    return out


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); comp = list(range(n + 1)); out = []
    for _ in range(q):
        t, a, b = rd.str(), int(rd.str()), int(rd.str())
        if t == "union":
            ca, cb = comp[a], comp[b]
            comp = [ca if c == cb else c for c in comp]
        else:
            out.append("YES" if comp[a] == comp[b] else "NO")
    return out


add(T, "Hợp nhất và kiểm tra", 1, """
Có `n` phần tử, mỗi phần tử ban đầu là một tập riêng. Thao tác:
- `union a b`: hợp nhất tập chứa `a` và tập chứa `b`;
- `get a b`: `a` và `b` có cùng tập không? In `YES`/`NO`.

Gợi ý: **DSU** — mỗi tập là một cây, `find(x)` đi lên gốc. Hai tối ưu: **nén đường đi** và **hợp theo kích thước** → gần như `O(1)` mỗi thao tác.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `q` dòng sau là các thao tác.", "Kết quả các thao tác `get`.",
    ["4 4\nunion 1 2\nget 1 2\nunion 3 4\nget 2 4\n"], _g, _sol, brute=_br, tags=["DSU"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, m), *(J(r.randint(1, n), r.randint(1, n)) for _ in range(m)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); d = DSU(n); big = 1; out = []
    for _ in range(m):
        a, b = rd.ints(2)
        if d.union(a, b):
            big = max(big, d.sz[d.find(a)])
        out.append(J(d.comps, big))
    return out


add(T, "Xây đường", 1, """
Có `n` thành phố chưa có con đường nào. Lần lượt xây `m` con đường hai chiều. Sau mỗi con đường, in số vùng liên thông
và kích thước vùng lớn nhất.

Gợi ý: DSU lưu kích thước mỗi tập; số vùng giảm 1 mỗi khi hợp nhất hai tập khác nhau.
""", "Dòng đầu `n, m` (1 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `a b`.", "`m` dòng, mỗi dòng hai số.",
    ["5 3\n1 2\n1 3\n4 5\n"], _g, _sol, tags=["DSU"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); tot, _ = kruskal(n, _read_wes(rd, m))
    return tot if tot is not None else "IMPOSSIBLE"


def _prim_dense(n, es):
    INF = float("inf")
    w = {}
    for c, a, b in es:
        k = (min(a, b), max(a, b))
        w[k] = min(w.get(k, INF), c)
    adj = [[] for _ in range(n + 1)]
    for (a, b), c in w.items():
        adj[a].append((b, c)); adj[b].append((a, c))
    import heapq
    seen = [False] * (n + 1); h = [(0, 1)]; tot = 0; cnt = 0
    while h:
        c, u = heapq.heappop(h)
        if seen[u]:
            continue
        seen[u] = True; tot += c; cnt += 1
        for v, cc in adj[u]:
            if not seen[v]:
                heapq.heappush(h, (cc, v))
    return tot if cnt == n else "IMPOSSIBLE"


add(T, "Sửa đường (Kruskal)", 1, """
Có `n` thành phố và `m` con đường hư hỏng, sửa con đường `i` tốn `c_i`. Cần sửa một số con đường sao cho mọi thành phố đều đi được tới nhau,
tổng chi phí nhỏ nhất. In chi phí, hoặc `IMPOSSIBLE`.

Gợi ý (Kruskal): sắp xếp các cạnh theo trọng số tăng dần, lần lượt thêm cạnh nếu nó nối hai thành phần khác nhau (kiểm tra bằng DSU).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^9).", "Chi phí nhỏ nhất hoặc `IMPOSSIBLE`.",
    ["5 6\n1 2 3\n2 3 5\n2 4 2\n3 4 8\n5 1 7\n5 4 4\n"], _gw(), _sol,
    brute=lambda s: (lambda rd: (lambda n, m: _prim_dense(n, _read_wes(rd, m)))(*rd.ints(2)))(Rd(s)), tags=["MST", "Kruskal", "DSU"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); d = DSU(n)
    for i in range(1, m + 1):
        a, b = rd.ints(2)
        if not d.union(a, b):
            return i
    return 0


add(T, "Cạnh tạo chu trình đầu tiên", 2, """
Lần lượt thêm `m` cạnh vào đồ thị vô hướng `n` đỉnh (ban đầu không có cạnh). Cạnh thứ mấy là cạnh **đầu tiên** tạo ra chu trình?
In `0` nếu không có.

Gợi ý: cạnh `(a, b)` tạo chu trình ⇔ `a` và `b` đã cùng tập DSU trước khi thêm.
""", "Dòng đầu `n, m` (1 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `a b`.", "Chỉ số cạnh hoặc `0`.",
    ["4 4\n1 2\n3 4\n2 3\n4 1\n"], lambda r, s: (lambda n: lines(J(n, n), *(J(a, b) for a, b in (rtree(r, n) + [(r.randint(1, n), r.randint(1, n))])[:n])))(S(s, 1, 10**5))
    if r.random() < .7 else _g(r, s), _sol, tags=["DSU"])


# 5 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 1000)
    w = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = r.randint(1, 10**6)
    return lines(str(n), *(L(row) for row in w))


def _sol(s):
    rd = Rd(s); n = rd.int(); w = [rd.ints(n) for _ in range(n)]
    INF = float("inf")
    d = [INF] * n; used = [False] * n; d[0] = 0; tot = 0
    for _ in range(n):
        u = min((d[i], i) for i in range(n) if not used[i])[1]
        used[u] = True; tot += d[u]; wu = w[u]
        for v in range(n):
            if not used[v] and wu[v] < d[v]:
                d[v] = wu[v]
    return tot


add(T, "Prim trên đồ thị dày", 2, """
Có `n` trạm, chi phí nối trực tiếp hai trạm `i, j` là `c[i][j]` (cho dưới dạng ma trận đầy đủ). Tìm tổng chi phí nhỏ nhất để nối mọi trạm.

Gợi ý: đồ thị đầy đủ có `~n²/2` cạnh — thuật toán **Prim** `O(n²)` không dùng heap là tốt nhất: lặp `n` lần, chọn đỉnh chưa thăm
có `d` nhỏ nhất, rồi cập nhật `d` của các đỉnh khác.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). `n` dòng sau là ma trận đối xứng (`c[i][i] = 0`, 1 ≤ c ≤ 10^6).", "Tổng chi phí nhỏ nhất.",
    ["3\n0 1 3\n1 0 2\n3 2 0\n"], _g, _sol, tags=["MST", "Prim"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    ops = [J(1, r.randint(1, n), r.randint(1, n)) if r.random() < .6 else J(2, r.randint(1, n)) for _ in range(q)]
    return lines(J(n, q), *ops)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); d = DSU(n); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            d.union(*rd.ints(2))
        else:
            out.append(d.sz[d.find(rd.int())])
    return out


add(T, "Nhóm bạn", 2, """
Có `n` học sinh. Thao tác:
- `1 a b`: `a` và `b` trở thành bạn (bạn của bạn cũng tính là cùng nhóm);
- `2 a`: nhóm của `a` có bao nhiêu người?

Gợi ý: DSU lưu kích thước tại gốc.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `q` dòng sau là các thao tác.", "Kết quả các thao tác loại 2.",
    ["5 5\n1 1 2\n2 2\n1 3 2\n2 1\n2 5\n"], _g, _sol, tags=["DSU"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rgraph(r, n, m, connected=r.random() < .5)
    k = r.randint(1, len(es)) if es else 0
    dele = r.sample(range(1, len(es) + 1), k)
    return lines(J(n, len(es), k), *(J(a, b) for a, b in es), L(dele))


def _sol(s):
    rd = Rd(s); n, m, k = rd.ints(3); es = [rd.ints(2) for _ in range(m)]; dele = rd.ints(k)
    gone = set(dele); d = DSU(n)
    for i, (a, b) in enumerate(es, 1):
        if i not in gone:
            d.union(a, b)
    res = []
    for i in reversed(dele):
        res.append(d.comps); d.union(*es[i - 1])
    return L(reversed(res))


def _br(s):
    rd = Rd(s); n, m, k = rd.ints(3); es = [rd.ints(2) for _ in range(m)]; dele = rd.ints(k)
    alive = set(range(1, m + 1)); out = []
    for i in dele:
        alive.discard(i); d = DSU(n)
        for j in alive:
            d.union(*es[j - 1])
        out.append(d.comps)
    return L(out)


add(T, "Phá cầu", 3, """
Đồ thị vô hướng `n` đỉnh, `m` cạnh. Lần lượt phá huỷ `k` cạnh (theo chỉ số). Sau **mỗi** lần phá, in số thành phần liên thông.

Gợi ý: DSU không hỗ trợ xoá cạnh — hãy **đảo ngược thời gian**: bắt đầu từ đồ thị cuối cùng (đã xoá hết), rồi thêm dần các cạnh theo thứ tự ngược.
""", "Dòng đầu `n, m, k`. `m` dòng là các cạnh. Dòng cuối gồm `k` chỉ số cạnh phân biệt bị phá theo thứ tự.", "Một dòng gồm `k` số.",
    ["4 4 3\n1 2\n2 3\n3 4\n4 1\n2 4 1\n"], _g, _sol, brute=_br, tags=["DSU", "offline", "đảo ngược"])


# 8 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); tot, used = kruskal(n, _read_wes(rd, m))
    return max(w for w, _, _ in used) if tot is not None and used else (0 if n == 1 else "IMPOSSIBLE")


add(T, "Cây khung có cạnh lớn nhất nhỏ nhất", 2, """
Tìm một cây khung sao cho **cạnh nặng nhất** của nó là nhỏ nhất; in trọng số cạnh đó, hoặc `IMPOSSIBLE` nếu đồ thị không liên thông.

Gợi ý: cây khung nhỏ nhất (Kruskal) cũng chính là cây khung "nút cổ chai" tối ưu.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^9).", "Trọng số cạnh lớn nhất hoặc `IMPOSSIBLE`.",
    ["4 5\n1 2 5\n2 3 1\n3 4 7\n1 4 3\n1 3 10\n"], _gw(), _sol, tags=["MST"])


# 9 -----------------------------------------------------------------------
def _path_max_all(n, tree_es):
    adj = [[] for _ in range(n + 1)]
    for w, a, b in tree_es:
        adj[a].append((b, w)); adj[b].append((a, w))
    mx = [None] * (n + 1)
    for s_ in range(1, n + 1):
        d = [-1] * (n + 1); d[s_] = 0; q = deque([s_])
        while q:
            u = q.popleft()
            for v, w in adj[u]:
                if d[v] < 0:
                    d[v] = max(d[u], w); q.append(v)
        mx[s_] = d
    return mx


def _second_best(n, es):
    tot, used = kruskal(n, es)
    if tot is None:
        return None
    mx = _path_max_all(n, used)
    used_set = set(used); best = None
    # cần max "nhỏ hơn hẳn w" trên đường đi để tổng tăng thực sự: xét cạnh max và cạnh max nhì
    adj = [[] for _ in range(n + 1)]
    for w, a, b in used:
        adj[a].append((b, w)); adj[b].append((a, w))
    for w, a, b in es:
        if (w, a, b) in used_set:
            continue
        # tìm cạnh lớn nhất < w trên đường a-b
        par = {a: (None, 0)}; q = deque([a])
        while q:
            u = q.popleft()
            for v, ww in adj[u]:
                if v not in par:
                    par[v] = (u, ww); q.append(v)
        cur, cand = b, -1
        while par[cur][0] is not None:
            ww = par[cur][1]
            if ww < w:
                cand = max(cand, ww)
            cur = par[cur][0]
        if cand >= 0:
            v = tot - cand + w
            best = v if best is None else min(best, v)
    return best


def _g(r, s):
    n = S(s, 2, 300); m = S(s, 1, 3000)
    es = rgraph(r, n, max(m, n - 1), connected=True)
    wh = r.choice([5, 100, 10**6])
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, wh)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m)
    v = _second_best(n, es)
    return v if v is not None else -1


def _br(s):
    from itertools import combinations
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m)
    sums = set()
    for comb in combinations(es, n - 1):
        d = DSU(n)
        if all(d.union(a, b) for _, a, b in comb):
            sums.add(sum(w for w, _, _ in comb))
    sums = sorted(sums)
    return sums[1] if len(sums) > 1 else -1


add(T, "Cây khung nhỏ nhì", 4, """
Đồ thị liên thông. Tìm tổng trọng số của cây khung có tổng **nhỏ nhất trong các tổng lớn hơn hẳn** tổng của cây khung nhỏ nhất.
In `-1` nếu không tồn tại.

Gợi ý: cây khung nhỏ nhì khác MST đúng một cạnh: thêm cạnh `(u, v, w)` ngoài MST và bỏ cạnh lớn nhất **nhỏ hơn hẳn `w`** trên đường đi `u → v` của MST.
(Với `n` lớn dùng LCA + nhảy nhị phân để lấy max trên đường đi; ở đây `n ≤ 300` nên duyệt trực tiếp được.)
""", "Dòng đầu `n, m` (2 ≤ n ≤ 300, n - 1 ≤ m ≤ 3000). `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^6).", "Tổng nhỏ nhì hoặc `-1`.",
    ["4 5\n1 2 1\n2 3 2\n3 4 3\n4 1 4\n1 3 5\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[1]) <= 10 else _sol(s), tags=["MST"])


# 10 ----------------------------------------------------------------------
class ParityDSU:
    def __init__(self, n):
        self.p = list(range(n + 1)); self.x = [0] * (n + 1); self.sz = [1] * (n + 1)

    def find(self, v):
        path = []
        while self.p[v] != v:
            path.append(v); v = self.p[v]
        root = v; acc = 0
        for u in reversed(path):
            acc ^= self.x[u]; self.x[u] = acc; self.p[u] = root
        return root

    def union(self, a, b, d):  # ràng buộc parity(a) xor parity(b) = d
        ra, rb = self.find(a), self.find(b)
        pa, pb = self.x[a] if a != ra else 0, self.x[b] if b != rb else 0
        if ra == rb:
            return (pa ^ pb) == d
        if self.sz[ra] < self.sz[rb]:
            ra, rb, pa, pb = rb, ra, pb, pa
        self.p[rb] = ra; self.x[rb] = pa ^ pb ^ d; self.sz[ra] += self.sz[rb]
        return True


def _g(r, s):
    n, m = S(s, 2, 10**5), S(s, 1, 2 * 10**5)
    side = [r.randint(0, 1) for _ in range(n + 1)]
    side[1], side[2] = 0, 1  # đảm bảo có cả hai phía
    es = []
    bad_at = r.randint(1, m) if r.random() < .7 else m + 1
    for i in range(1, m + 1):
        while True:
            a, b = r.randint(1, n), r.randint(1, n)
            if a != b and (side[a] != side[b] or i >= bad_at):
                break
        es.append((a, b))
    return lines(J(n, m), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); d = ParityDSU(n); ok = True; out = []
    for _ in range(m):
        a, b = rd.ints(2)
        if ok and not d.union(a, b, 1):
            ok = False
        out.append("1" if ok else "0")
    return "".join(out)


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es = []; out = []
    for _ in range(m):
        es.append(rd.ints(2))
        adj = [[] for _ in range(n + 1)]
        for a, b in es:
            adj[a].append(b); adj[b].append(a)
        col = [-1] * (n + 1); ok = True
        for st in range(1, n + 1):
            if col[st] < 0:
                col[st] = 0; q = [st]
                while q:
                    u = q.pop()
                    for v in adj[u]:
                        if col[v] < 0:
                            col[v] = col[u] ^ 1; q.append(v)
                        elif col[v] == col[u]:
                            ok = False
        out.append("1" if ok else "0")
    return "".join(out)


add(T, "Còn hai phía không?", 4, """
Lần lượt thêm `m` cạnh vào đồ thị `n` đỉnh. Sau mỗi lần thêm, đồ thị có còn là **đồ thị hai phía** không? In xâu `m` ký tự `1`/`0`.

Gợi ý: DSU có "độ lệch chẵn lẻ": mỗi đỉnh lưu parity so với cha. Thêm cạnh `(a, b)` yêu cầu `parity(a) ≠ parity(b)`; nếu `a, b` đã cùng tập
mà cùng parity thì xuất hiện chu trình lẻ (và từ đó trở đi luôn là `0`).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `a b` (a ≠ b).", "Xâu `m` ký tự.",
    ["3 3\n1 2\n2 3\n1 3\n"], _g, _sol, brute=_br, tags=["DSU", "parity"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 1000); m = S(s, 1, 5000)
    es = rgraph(r, n, max(m, n - 1), connected=True)
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, r.choice([5, 10**6]))) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m)
    tot, used = kruskal(n, es)
    mx = _path_max_all(n, used)
    return L(tot - mx[a][b] + w for w, a, b in es)


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m); out = []
    for i, (w, a, b) in enumerate(es):
        d = DSU(n); d.union(a, b); tot = w
        for ww, x, y in sorted(es[:i] + es[i + 1:]):
            if d.union(x, y):
                tot += ww
        out.append(tot)
    return L(out)


add(T, "Cây khung bắt buộc chứa cạnh", 4, """
Đồ thị liên thông. Với **mỗi** cạnh `e`, tìm tổng trọng số nhỏ nhất của cây khung bắt buộc phải chứa `e`.

Gợi ý: lấy MST; nếu `e = (u, v, w)` không thuộc MST thì thêm `e` và bỏ cạnh lớn nhất trên đường `u → v` của MST:
đáp án `MST - maxPath(u, v) + w` (công thức này cũng đúng khi `e` thuộc MST).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 1000, n - 1 ≤ m ≤ 5000). `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^6).", "Một dòng gồm `m` số.",
    ["5 7\n1 2 3\n1 3 1\n1 4 5\n2 3 2\n2 5 3\n3 4 2\n4 5 4\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[1]) <= 300 else _sol(s),
    tags=["MST"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 1000)
    hi = r.choice([10, 10**6])
    return lines(str(n), *(J(r.randint(-hi, hi), r.randint(-hi, hi)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int(); p = [rd.ints(2) for _ in range(n)]
    INF = float("inf"); d = [INF] * n; used = [False] * n; d[0] = 0; tot = 0
    for _ in range(n):
        u = -1; best = INF
        for i in range(n):
            if not used[i] and d[i] < best:
                best = d[i]; u = i
        used[u] = True; tot += best; ux, uy = p[u]
        for v in range(n):
            if not used[v]:
                c = abs(ux - p[v][0]) + abs(uy - p[v][1])
                if c < d[v]:
                    d[v] = c
    return tot


add(T, "Nối các điểm", 3, """
Có `n` điểm trên mặt phẳng. Nối hai điểm tốn chi phí bằng khoảng cách Manhattan `|x1 - x2| + |y1 - y2|`. Tìm tổng chi phí nhỏ nhất để mọi điểm được nối.

Gợi ý: đồ thị đầy đủ ẩn — Prim `O(n²)`, tính khoảng cách khi cần thay vì lưu `n²` cạnh.
""", "Dòng đầu `n` (1 ≤ n ≤ 1000). `n` dòng sau mỗi dòng `x y` (|x|, |y| ≤ 10^6).", "Tổng chi phí nhỏ nhất.",
    ["5\n0 0\n2 2\n3 10\n5 2\n7 0\n"], _g, _sol, tags=["MST", "Prim"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(conn=None)(r, s)
    q = S(s, 1, 10**5)
    wh = int(max(base.split()[4::3], key=int)) if len(base.split()) > 2 else 10
    return base + lines(str(q), L(r.randint(0, wh + 1) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = sorted(_read_wes(rd, m)); q = rd.int(); qs = rd.ints(q)
    order = sorted(range(q), key=lambda i: qs[i])
    d = DSU(n); pairs = 0; j = 0; ans = [0] * q
    for i in order:
        while j < m and es[j][0] <= qs[i]:
            _, a, b = es[j]
            ra, rb = d.find(a), d.find(b)
            if ra != rb:
                pairs += d.sz[ra] * d.sz[rb]; d.union(a, b)
            j += 1
        ans[i] = pairs
    return L(ans)


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m); q = rd.int(); out = []
    for k in rd.ints(q):
        d = DSU(n)
        for w, a, b in es:
            if w <= k:
                d.union(a, b)
        from collections import Counter
        c = Counter(d.find(v) for v in range(1, n + 1))
        out.append(sum(x * (x - 1) // 2 for x in c.values()))
    return L(out)


add(T, "Cặp đỉnh đi được với tải trọng", 4, """
Mỗi con đường có **độ nguy hiểm** `c`. Với truy vấn `k`, chỉ được đi trên các con đường có `c ≤ k`.
Với mỗi `k`, đếm số cặp đỉnh `{u, v}` (u ≠ v) đi được tới nhau.

Gợi ý (offline): sắp xếp cạnh theo `c` và truy vấn theo `k`; thêm dần cạnh vào DSU. Khi hợp hai tập kích thước `x`, `y`, số cặp tăng `x·y`.
""", "Dòng đầu `n, m`. `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^9). Tiếp theo `q` (1 ≤ q ≤ 10^5) và một dòng `q` số `k`.",
    "Một dòng gồm `q` số.", ["4 3\n1 2 5\n2 3 3\n3 4 8\n3\n2 5 10\n"], _g, _sol, brute=_br, tags=["DSU", "offline"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(conn=None, whi=10**6)(r, s)
    n = int(base.split()[0])
    return base + L(arr(r, n, 1, r.choice([10, 10**6]))) + "\n"


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m); c = rd.ints(n)
    es += [(c[i], 0, i + 1) for i in range(n)]
    d = DSU(n); tot = 0
    for w, a, b in sorted(es):
        if d.union(a, b):
            tot += w
    return tot


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m); c = rd.ints(n)
    best = None
    for mask in range(1, 1 << n):
        d = DSU(n); tot = sum(c[i] for i in range(n) if mask >> i & 1)
        for i in range(n):
            if mask >> i & 1:
                d.union(0, i + 1)
        for w, a, b in sorted(es):
            if d.union(a, b):
                tot += w
        if d.comps == 0:
            best = tot if best is None else min(best, tot)
    return best


add(T, "Giếng và ống nước", 3, """
Làng có `n` nhà. Đào giếng ở nhà `i` tốn `c_i`; nối ống giữa hai nhà `a, b` tốn `w`. Mỗi nhà cần có nước: hoặc có giếng, hoặc được nối (trực tiếp
hay gián tiếp) tới một nhà có giếng. Tìm tổng chi phí nhỏ nhất.

Gợi ý: thêm đỉnh ảo 0 là "nguồn nước", cạnh `(0, i)` trọng số `c_i`. Đáp án là MST của đồ thị `n + 1` đỉnh.
""", "Dòng đầu `n, m`. `m` dòng sau mỗi dòng `a b w` (1 ≤ w ≤ 10^6). Dòng cuối gồm `n` số `c_i` (1 ≤ c ≤ 10^6).", "Chi phí nhỏ nhất.",
    ["3 2\n1 2 1\n2 3 1\n1 2 2\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 10 else _sol(s), tags=["MST", "đỉnh ảo"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(conn=False, whi=10**6)(r, s)
    n = int(base.split()[0]); q = S(s, 1, 10**5)
    return base + lines(str(q), *(J(r.randint(1, n), r.randint(1, n), r.randint(1, 10**6)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = sorted(_read_wes(rd, m)); q = rd.int()
    qs = [rd.ints(3) for _ in range(q)]
    order = sorted(range(q), key=lambda i: qs[i][2])
    d = DSU(n); j = 0; ans = [""] * q
    for i in order:
        u, v, w = qs[i]
        while j < m and es[j][0] <= w:
            d.union(es[j][1], es[j][2]); j += 1
        ans[i] = "YES" if d.find(u) == d.find(v) else "NO"
    return ans


add(T, "Đi được với giới hạn", 3, """
Đồ thị vô hướng có trọng số. Với truy vấn `(u, v, w)`: có đường đi từ `u` tới `v` chỉ dùng các cạnh trọng số ≤ `w` không?

Gợi ý: xử lý offline theo `w` tăng dần, thêm cạnh vào DSU.
""", "Dòng đầu `n, m`. `m` dòng `a b c` (1 ≤ c ≤ 10^6). Dòng tiếp là `q` (1 ≤ q ≤ 10^5), `q` dòng sau mỗi dòng `u v w`.",
    "Mỗi truy vấn in `YES` hoặc `NO`.", ["3 2\n1 2 4\n2 3 6\n3\n1 3 5\n1 3 6\n2 2 1\n"], _g, _sol, tags=["DSU", "offline"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n, q = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    out = []
    for i in range(q):
        a, b = sorted((r.randint(1, n), r.randint(1, n)))
        if r.random() < .5:
            b = min(n, a + r.randint(0, 10))
        out.append(J(a, b))
    return lines(J(n, q), *out)


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); ops = [rd.ints(2) for _ in range(q)]
    col = [0] * (n + 2); nxt = list(range(n + 2))

    def find(x):
        root = x
        while nxt[root] != root:
            root = nxt[root]
        while nxt[x] != root:
            nxt[x], x = root, nxt[x]
        return root
    for c in range(q, 0, -1):
        l, r_ = ops[c - 1]
        x = find(l)
        while x <= r_:
            col[x] = c; nxt[x] = x + 1; x = find(x + 1)
    return L(col[1:n + 1])


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); col = [0] * (n + 1)
    for c in range(1, q + 1):
        l, r_ = rd.ints(2)
        for i in range(l, r_ + 1):
            col[i] = c
    return L(col[1:])


add(T, "Sơn hàng rào", 3, """
Hàng rào có `n` tấm ván chưa sơn (màu 0). Lần lượt có `q` lượt sơn, lượt thứ `c` sơn màu `c` lên các tấm `l..r` (đè lên màu cũ). In màu cuối cùng của từng tấm.

Gợi ý: xử lý **ngược** từ lượt cuối: mỗi tấm chỉ cần sơn một lần (lần sơn cuối cùng). Dùng DSU "nhảy tới tấm chưa sơn kế tiếp":
`nxt[x]` = tấm chưa sơn đầu tiên `≥ x` → tổng `O(n α(n))`.
""", "Dòng đầu `n, q` (1 ≤ n, q ≤ 2·10^5). `q` dòng sau mỗi dòng `l r`.", "Một dòng gồm `n` số.",
    ["5 3\n1 3\n2 4\n5 5\n"], _g, _sol, brute=_br, tags=["DSU", "đảo ngược"])


# 17 ----------------------------------------------------------------------
class WeightedDSU:
    def __init__(self, n):
        self.p = list(range(n + 1)); self.d = [0] * (n + 1)  # d[v] = x_v - x_parent

    def find(self, v):
        path = []
        while self.p[v] != v:
            path.append(v); v = self.p[v]
        root = v
        for u in reversed(path):
            par = self.p[u]
            if par != root:
                self.d[u] += self.d[par]
            self.p[u] = root
        return root


def _sol(s):
    rd = Rd(s); n, q = rd.ints(2); w = WeightedDSU(n); out = []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            a, b, c = rd.ints(3)  # x_b - x_a = c
            ra, rb = w.find(a), w.find(b)
            da = w.d[a] if a != ra else 0; db = w.d[b] if b != rb else 0
            if ra == rb:
                out.append("OK" if db - da == c else "BAD")
            else:
                w.p[rb] = ra; w.d[rb] = da + c - db; out.append("OK")
        else:
            a, b = rd.ints(2)
            ra, rb = w.find(a), w.find(b)
            if ra != rb:
                out.append("?")
            else:
                out.append((w.d[b] if b != rb else 0) - (w.d[a] if a != ra else 0))
    return out


def _g(r, s):
    n, q = S(s, 2, 10**5), S(s, 1, 2 * 10**5)
    x = [0] + arr(r, n, -10**6, 10**6)
    ops = []
    for _ in range(q):
        a, b = r.randint(1, n), r.randint(1, n)
        if r.random() < .5:
            c = x[b] - x[a] + (r.choice([1, -1]) if r.random() < .1 else 0)
            ops.append(J(1, a, b, c))
        else:
            ops.append(J(2, a, b))
    return lines(J(n, q), *ops)


def _br(s):
    rd = Rd(s); n, q = rd.ints(2); out = []
    adj = [[] for _ in range(n + 1)]

    def diff(a, b):
        val = {a: 0}; st = [a]
        while st:
            u = st.pop()
            for v, c in adj[u]:
                if v not in val:
                    val[v] = val[u] + c; st.append(v)
        return val.get(b)
    for _ in range(q):
        t = rd.int()
        if t == 1:
            a, b, c = rd.ints(3); cur = diff(a, b)
            if cur is None:
                adj[a].append((b, c)); adj[b].append((a, -c)); out.append("OK")
            else:
                out.append("OK" if cur == c else "BAD")
        else:
            a, b = rd.ints(2); cur = diff(a, b)
            out.append("?" if cur is None else cur)
    return out


add(T, "Cân đĩa", 4, """
Có `n` vật với khối lượng `x_1..x_n` chưa biết. Thao tác:
- `1 a b c`: phép cân cho biết `x_b - x_a = c`. In `OK` nếu thông tin này phù hợp với các phép cân **được chấp nhận** trước đó
  (khi đó ghi nhận nó), ngược lại in `BAD` (bỏ qua thông tin);
- `2 a b`: in `x_b - x_a` nếu suy ra được từ các thông tin đã ghi nhận, ngược lại in `?`.

Gợi ý: **DSU có trọng số** — mỗi đỉnh lưu hiệu khối lượng so với cha; khi nén đường đi thì cộng dồn hiệu.
""", "Dòng đầu `n, q` (2 ≤ n ≤ 10^5, 1 ≤ q ≤ 2·10^5). `q` dòng sau là các thao tác (|c| ≤ 2·10^6).", "Mỗi thao tác in một dòng.",
    ["3 5\n1 1 2 5\n2 2 1\n1 2 3 1\n2 1 3\n1 1 3 7\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[1]) <= 400 else _sol(s),
    tags=["DSU có trọng số"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(conn=None, whi=10**6)(r, s)
    n = int(base.split()[0])
    return base + f"{r.randint(1, n)}\n"


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = sorted(_read_wes(rd, m)); k = rd.int()
    d = DSU(n); tot = 0
    for w, a, b in es:
        if d.comps <= k:
            break
        if d.union(a, b):
            tot += w
    return tot if d.comps == k else -1


add(T, "Chia thành k vùng", 3, """
Cần chọn một tập cạnh để đồ thị được chia thành **đúng** `k` vùng liên thông (mỗi vùng là một cây), tổng trọng số nhỏ nhất. In `-1` nếu không thể
(đồ thị ban đầu có hơn `k` thành phần).

Gợi ý: chạy Kruskal nhưng dừng khi còn đúng `k` thành phần (rừng khung nhỏ nhất `k` cây).
""", "Dòng đầu `n, m`. `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^6). Dòng cuối là `k` (1 ≤ k ≤ n).", "Tổng nhỏ nhất hoặc `-1`.",
    ["4 4\n1 2 1\n2 3 5\n3 4 2\n1 4 9\n2\n"], _g, _sol, tags=["MST", "Kruskal"])


# 19 ----------------------------------------------------------------------
def _mst_white(n, es, k):
    """es: (w, a, b, white). Tìm MST có đúng k cạnh trắng (alien trick / Lagrange)."""
    def run(pen):
        d = DSU(n); tot = 0; cnt = 0
        for w, wh, a, b in sorted((w - (pen if wh else 0), 0 if wh else 1, a, b) for w, a, b, wh in es):
            if d.union(a, b):
                tot += w; cnt += 1 if wh == 0 else 0
        return tot, cnt, d.comps
    tot, cnt, comps = run(0)
    if comps != 1:
        return -1
    lo, hi = -2 * 10**6, 2 * 10**6
    # cnt (ưu tiên cạnh trắng khi bằng nhau) tăng theo pen; tìm pen nhỏ nhất có cnt ≥ k
    if run(hi)[1] < k:
        return -1
    while lo < hi:
        mid = (lo + hi) // 2
        if run(mid)[1] >= k:
            hi = mid
        else:
            lo = mid + 1
    t, c, _ = run(lo)
    # số cạnh trắng tối thiểu khi ưu tiên cạnh đen trong các cạnh bằng nhau
    def run_black_first(pen):
        d = DSU(n); cnt_ = 0
        for w, wh, a, b in sorted((w - (pen if wh else 0), 1 if wh else 0, a, b) for w, a, b, wh in es):
            if d.union(a, b):
                cnt_ += 1 if wh == 1 else 0
        return cnt_
    if run_black_first(lo) > k:
        return -1
    return t + lo * k


def _g(r, s):
    n = S(s, 2, 2000); m = S(s, 1, 2 * 10**4)
    es = rgraph(r, n, max(m, n - 1), connected=r.random() < .9)
    return lines(J(n, len(es), r.randint(0, n - 1)), *(J(a, b, r.randint(1, r.choice([5, 10**6])), r.randint(0, 1)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m, k = rd.ints(3)
    es = []
    for _ in range(m):
        a, b, w, c = rd.ints(4); es.append((w, a, b, c))
    return _mst_white(n, es, k)


def _br(s):
    from itertools import combinations
    rd = Rd(s); n, m, k = rd.ints(3)
    es = [rd.ints(4) for _ in range(m)]
    best = None
    for comb in combinations(es, n - 1):
        if sum(c for _, _, _, c in comb) != k:
            continue
        d = DSU(n)
        if all(d.union(a, b) for a, b, _, _ in comb):
            v = sum(w for _, _, w, _ in comb)
            best = v if best is None else min(best, v)
    return -1 if best is None else best


add(T, "Cây khung có đúng k cạnh trắng", 5, """
Mỗi cạnh có trọng số và màu trắng (`1`) hoặc đen (`0`). Tìm cây khung có **đúng** `k` cạnh trắng với tổng trọng số nhỏ nhất (`-1` nếu không có).

Gợi ý (kỹ thuật "Alien" / nhân tử Lagrange): trừ mọi cạnh trắng đi `λ` rồi chạy Kruskal. Khi `λ` tăng, số cạnh trắng trong MST tăng.
Tìm kiếm nhị phân `λ` để MST có đúng (hoặc có thể đạt) `k` cạnh trắng; đáp án = `MST(λ) + λ·k`. Chú ý xử lý các cạnh bằng trọng số.
""", "Dòng đầu `n, m, k` (2 ≤ n ≤ 2000, n - 1 ≤ m ≤ 2·10^4, 0 ≤ k < n). `m` dòng sau mỗi dòng `a b w c` (1 ≤ w ≤ 10^6, c ∈ {0, 1}).",
    "Tổng nhỏ nhất hoặc `-1`.", ["3 3 1\n1 2 1 1\n2 3 1 0\n1 3 3 1\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[1]) <= 12 else _sol(s), tags=["MST", "alien trick"], tl=2000)


# 20 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    es = [(w, a, b, i) for i, (w, a, b) in enumerate(_read_wes(rd, m))]
    res = ["none"] * m; d = DSU(n)
    es.sort(); i = 0
    while i < m:
        j = i
        while j < m and es[j][0] == es[i][0]:
            j += 1
        group = es[i:j]
        # cạnh nối hai thành phần khác nhau → ít nhất một MST; cạnh cầu trong đồ thị nén → mọi MST
        cand = []
        for w, a, b, idx in group:
            ra, rb = d.find(a), d.find(b)
            if ra != rb:
                cand.append((ra, rb, idx)); res[idx] = "at least one"
        if cand:
            nodes = {}
            for ra, rb, _ in cand:
                nodes.setdefault(ra, len(nodes) + 1); nodes.setdefault(rb, len(nodes) + 1)
            from .t11_cay_dfs_khop_cau import bridges as _bridges
            edges = [(nodes[ra], nodes[rb]) for ra, rb, _ in cand]
            # cạnh song song (cùng cặp) không bao giờ là cầu — bridges() xử lý đúng nhờ dùng id cạnh
            for e in _bridges(len(nodes), edges):
                res[cand[e][2]] = "any"
        for w, a, b, idx in group:
            d.union(a, b)
        i = j
    return res


def _br(s):
    from itertools import combinations
    rd = Rd(s); n, m = rd.ints(2); es = _read_wes(rd, m)
    best, trees = None, []
    for comb in combinations(range(m), n - 1):
        d = DSU(n)
        if all(d.union(es[i][1], es[i][2]) for i in comb):
            v = sum(es[i][0] for i in comb)
            if best is None or v < best:
                best, trees = v, [set(comb)]
            elif v == best:
                trees.append(set(comb))
    out = []
    for i in range(m):
        c = sum(1 for t in trees if i in t)
        out.append("any" if c == len(trees) else ("at least one" if c else "none"))
    return out


def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 10**5)
    es = rgraph(r, n, max(m, n - 1), connected=True)
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, r.choice([3, 10, 10**6]))) for a, b in es))


add(T, "Cạnh trong cây khung nhỏ nhất", 5, """
Đồ thị liên thông, có thể có nhiều cây khung nhỏ nhất. Với mỗi cạnh (theo thứ tự nhập), in:
- `any` nếu cạnh thuộc **mọi** cây khung nhỏ nhất;
- `at least one` nếu thuộc ít nhất một nhưng không phải tất cả;
- `none` nếu không thuộc cây khung nhỏ nhất nào.

Gợi ý: xử lý các nhóm cạnh **cùng trọng số**. Cạnh nối hai thành phần DSU khác nhau → ít nhất `at least one`. Trong đồ thị nén (đỉnh = thành phần DSU,
cạnh = các cạnh của nhóm), cạnh nào là **cầu** thì thuộc mọi MST. Sau đó hợp nhất cả nhóm vào DSU.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, n - 1 ≤ m ≤ 10^5). `m` dòng sau mỗi dòng `a b c` (1 ≤ c ≤ 10^6), không có cạnh lặp.",
    "`m` dòng.", ["4 5\n1 2 101\n1 3 100\n2 3 2\n2 4 2\n3 4 1\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[1]) <= 12 else _sol(s), tags=["MST", "cầu", "DSU"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    return lines(J(n, m), *(J(r.randint(1, n), r.randint(1, n)) for _ in range(m)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); d = DSU(n)
    for _ in range(m):
        d.union(*rd.ints(2))
    from collections import Counter
    c = Counter(d.find(v) for v in range(1, n + 1))
    return sum(x * (x - 1) // 2 for x in c.values())


add(T, "Cặp bạn cùng nhóm", 2, """
Có `n` học sinh và `m` cặp bạn thân; bạn của bạn cũng cùng nhóm. Đếm số cặp học sinh (không kể thứ tự) thuộc cùng một nhóm.

Gợi ý: sau khi hợp nhất bằng DSU, mỗi nhóm kích thước `x` đóng góp `x(x-1)/2` cặp.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). `m` dòng sau mỗi dòng `a b`.", "Số cặp.",
    ["5 3\n1 2\n2 3\n4 5\n"], _g, _sol, tags=["DSU"])
