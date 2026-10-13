"""Chuyên đề 12: Thành phần liên thông mạnh, DAG, QHĐ trên DAG."""
import heapq
from collections import deque
from .base import add, Rd, S, J, L, arr, lines, rdigraph

T = 12
MOD = 10**9 + 7


def _read_di(rd, n, m, w=False):
    adj = [[] for _ in range(n + 1)]
    es = []
    for _ in range(m):
        if w:
            a, b, c = rd.ints(3)
        else:
            (a, b), c = rd.ints(2), 1
        adj[a].append((b, c)); es.append((a, b, c))
    return adj, es


def scc(n, adj):
    """Kosaraju lặp. Trả về comp[v] (đánh số 0..k-1 theo thứ tự topo của đồ thị nén) và k."""
    order, seen, it = [], [False] * (n + 1), [0] * (n + 1)
    for st in range(1, n + 1):
        if seen[st]:
            continue
        seen[st] = True; stack = [st]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]][0]; it[u] += 1
                if not seen[v]:
                    seen[v] = True; stack.append(v)
            else:
                stack.pop(); order.append(u)
    radj = [[] for _ in range(n + 1)]
    for u in range(1, n + 1):
        for v, _ in adj[u]:
            radj[v].append(u)
    comp = [-1] * (n + 1); k = 0
    for st in reversed(order):
        if comp[st] >= 0:
            continue
        comp[st] = k; stack = [st]
        while stack:
            u = stack.pop()
            for v in radj[u]:
                if comp[v] < 0:
                    comp[v] = k; stack.append(v)
        k += 1
    return comp, k


def topo(n, adj):
    indeg = [0] * (n + 1)
    for u in range(1, n + 1):
        for v, _ in adj[u]:
            indeg[v] += 1
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0); out = []
    while q:
        u = q.popleft(); out.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else None


def _gd(r, s, dag=None, nmax=10**5, mmax=2 * 10**5):
    n = S(s, 2, nmax); m = S(s, 1, mmax) // r.choice([1, 2, 5])
    if dag is None:
        dag = r.random() < .5
    es = rdigraph(r, n, m, dag=dag)
    if not dag and r.random() < .5:
        es = rdigraph(r, n, max(1, n // r.choice([1, 2])), dag=True) + rdigraph(r, n, r.randint(0, 3))
        es = list(dict.fromkeys(es))
    return n, es


def _gs(dag=None, w=None):
    def g(r, s):
        n, es = _gd(r, s, dag)
        if w:
            return lines(J(n, len(es)), *(J(a, b, r.randint(*w)) for a, b in es))
        return lines(J(n, len(es)), *(J(a, b) for a, b in es))
    return g


# 1 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    return "NO" if topo(n, adj) else "YES"


add(T, "Chu trình có hướng", 1, """
Đồ thị có hướng có chứa chu trình không?

Gợi ý: thuật toán Kahn — liên tục lấy ra đỉnh có bậc vào 0. Nếu không lấy ra được hết `n` đỉnh thì có chu trình.
(Hoặc DFS tô 3 màu: gặp đỉnh "đang thăm" → có chu trình.)
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v` (cung `u → v`).", "`YES` nếu có chu trình, ngược lại `NO`.",
    ["3 3\n1 2\n2 3\n3 1\n", "3 2\n1 2\n1 3\n"], _gs(), _sol, tags=["DAG", "sắp xếp topo"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    indeg = [0] * (n + 1)
    for u in range(1, n + 1):
        for v, _ in adj[u]:
            indeg[v] += 1
    h = [v for v in range(1, n + 1) if indeg[v] == 0]; heapq.heapify(h); out = []
    while h:
        u = heapq.heappop(h); out.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    return L(out) if len(out) == n else "IMPOSSIBLE"


add(T, "Thứ tự học các môn", 1, """
Có `n` môn học và `m` điều kiện `u v`: phải học môn `u` trước môn `v`. Hãy in một thứ tự học hợp lệ; nếu có nhiều thứ tự, in thứ tự
**nhỏ nhất theo từ điển**. Nếu không có thứ tự nào in `IMPOSSIBLE`.

Gợi ý: thuật toán Kahn, nhưng thay hàng đợi bằng `priority_queue` (min-heap) để luôn lấy môn có số hiệu nhỏ nhất.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v`.", "Thứ tự học hoặc `IMPOSSIBLE`.",
    ["5 3\n1 2\n3 1\n4 5\n"], _gs(), _sol, tags=["sắp xếp topo", "heap"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    indeg = [0] * (n + 1)
    for u in range(1, n + 1):
        for v, _ in adj[u]:
            indeg[v] += 1
    q = [v for v in range(1, n + 1) if indeg[v] == 0]; cnt = 0
    while q:
        if len(q) > 1:
            return "NO"
        u = q.pop(); cnt += 1
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return "YES" if cnt == n else "NO"


def _g(r, s):
    n = S(s, 2, 10**5)
    perm = list(range(1, n + 1)); r.shuffle(perm)
    es = [(perm[i], perm[i + 1]) for i in range(n - 1)]
    if r.random() < .5 and n > 2:
        es.pop(r.randrange(len(es)))
    extra = S(s, 0, 10**5)
    for _ in range(extra):
        i, j = sorted(r.sample(range(n), 2))
        es.append((perm[i], perm[j]))
    es = list(dict.fromkeys(es)); r.shuffle(es)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


add(T, "Thứ tự topo duy nhất", 2, """
Đồ thị có hướng không chu trình (DAG). Thứ tự topo của nó có **duy nhất** không?

Gợi ý: thứ tự topo duy nhất ⇔ trong suốt thuật toán Kahn, hàng đợi luôn chỉ có đúng một đỉnh
(tương đương: có đường đi Hamilton đi qua mọi đỉnh).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung (đồ thị không có chu trình).", "`YES` hoặc `NO`.",
    ["3 2\n1 2\n2 3\n", "3 2\n1 2\n1 3\n"], _g, _sol, tags=["sắp xếp topo"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    return scc(n, adj)[1]


def _br_reach(n, adj):
    reach = []
    for st in range(1, n + 1):
        seen = {st}; q = [st]
        while q:
            u = q.pop()
            for v, _ in adj[u]:
                if v not in seen:
                    seen.add(v); q.append(v)
        reach.append(seen)
    return reach


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    reach = _br_reach(n, adj)
    return len({frozenset(v for v in range(1, n + 1) if v in reach[u - 1] and u in reach[v - 1]) for u in range(1, n + 1)})


add(T, "Đếm thành phần liên thông mạnh", 2, """
Hai đỉnh `u`, `v` thuộc cùng một thành phần liên thông mạnh (TPLTM) nếu đi được từ `u` tới `v` **và** từ `v` tới `u`.
Đếm số TPLTM của đồ thị có hướng.

Gợi ý: thuật toán Tarjan (một lần DFS, dùng `low`), hoặc Kosaraju (DFS trên đồ thị gốc lấy thứ tự kết thúc,
rồi DFS trên đồ thị ngược theo thứ tự ngược lại).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung.", "Số TPLTM.",
    ["5 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 4\n"], _gs(dag=False), _sol, brute=_br, tags=["TPLTM", "Tarjan"])


# 5 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    comp, k = scc(n, adj)
    lab = {}; out = []
    for v in range(1, n + 1):
        if comp[v] not in lab:
            lab[comp[v]] = len(lab) + 1
        out.append(lab[comp[v]])
    return lines(str(k), L(out)).rstrip("\n")


add(T, "Các vương quốc", 2, """
Có `n` hành tinh và `m` tuyến bay một chiều. Hai hành tinh thuộc cùng vương quốc nếu bay qua lại được với nhau (cùng TPLTM).
Hãy đánh số các vương quốc: vương quốc chứa hành tinh 1 là số 1; lần lượt duyệt hành tinh `2, 3, ...`, gặp vương quốc mới thì
gán số tiếp theo.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các tuyến bay.",
    "Dòng đầu là số vương quốc `k`. Dòng hai gồm `n` số là vương quốc của từng hành tinh.",
    ["5 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 4\n"], _gs(dag=False), _sol, tags=["TPLTM"])


# 6 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    order = topo(n, adj)
    dp = [0] * (n + 1)
    for u in order:
        for v, _ in adj[u]:
            if dp[u] + 1 > dp[v]:
                dp[v] = dp[u] + 1
    return max(dp)


add(T, "Đường đi dài nhất trên DAG", 2, """
Cho DAG. Tìm số cung trên đường đi dài nhất (đường đi có thể bắt đầu và kết thúc ở bất kỳ đâu).

Gợi ý: xét các đỉnh theo thứ tự topo, `dp[v] = max(dp[u] + 1)` với mọi cung `u → v`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung (không có chu trình).", "Độ dài lớn nhất.",
    ["4 5\n1 2\n1 3\n3 2\n2 4\n3 4\n"], _gs(dag=True), _sol, tags=["DAG", "QHĐ trên DAG"])


# 7 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    order = topo(n, adj)
    dp = [0] * (n + 1); dp[1] = 1
    for u in order:
        if dp[u]:
            for v, _ in adj[u]:
                dp[v] = (dp[v] + dp[u]) % MOD
    return dp[n]


add(T, "Đếm đường đi trên DAG", 2, """
Cho DAG. Đếm số đường đi từ đỉnh 1 tới đỉnh `n`, modulo `10^9 + 7`.

Gợi ý: `cnt[v] = Σ cnt[u]` với mọi cung `u → v`, tính theo thứ tự topo.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung (không có chu trình).", "Số đường đi modulo 10^9+7.",
    ["4 5\n1 2\n2 4\n1 3\n3 4\n1 4\n"], _gs(dag=True), _sol, tags=["DAG", "QHĐ đếm"])


# 8 -----------------------------------------------------------------------
add(T, "Liên thông mạnh?", 2, """
Từ mọi đỉnh có đi được tới mọi đỉnh khác không (đồ thị có hướng liên thông mạnh)?

Gợi ý: chỉ cần kiểm tra: từ đỉnh 1 đi tới được mọi đỉnh, **và** trên đồ thị đảo chiều từ đỉnh 1 cũng tới được mọi đỉnh.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung.", "`YES` hoặc `NO`.",
    ["3 3\n1 2\n2 3\n3 1\n", "3 2\n1 2\n2 3\n"],
    lambda r, s: (lambda n: (lambda es: lines(J(n, len(es)), *(J(a, b) for a, b in es)))(
        list(dict.fromkeys([(i, i % n + 1) for i in range(1, n + 1)] + rdigraph(r, n, S(s, 0, 10**5)))) if r.random() < .5
        else rdigraph(r, n, S(s, 1, 2 * 10**5))))(S(s, 2, 10**5)),
    lambda s: (lambda rd: (lambda n, m: "YES" if scc(n, _read_di(rd, n, m)[0])[1] == 1 else "NO")(*rd.ints(2)))(Rd(s)),
    tags=["TPLTM"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    order = topo(n, adj)
    NEG = -1
    dp = [NEG] * (n + 1); dp[1] = 1
    for u in order:
        if dp[u] > 0:
            for v, _ in adj[u]:
                if dp[u] + 1 > dp[v]:
                    dp[v] = dp[u] + 1
    return dp[n] if dp[n] > 0 else "IMPOSSIBLE"


def _g(r, s):
    n, es = _gd(r, s, dag=True)
    # đánh số lại để 1 đứng đầu và n đứng cuối thứ tự topo
    adj = [[] for _ in range(n + 1)]
    for a, b in es:
        adj[a].append((b, 1))
    order = topo(n, adj)
    rank = {v: i + 1 for i, v in enumerate(order)}
    es = [(rank[a], rank[b]) for a, b in es]
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


add(T, "Hành trình dài nhất", 3, """
Có `n` thành phố và `m` chuyến bay một chiều (không có chu trình). Tìm hành trình từ thành phố 1 tới thành phố `n` đi qua
**nhiều thành phố nhất** (tính cả 1 và `n`). In số thành phố đó, hoặc `IMPOSSIBLE` nếu không tới được.

Gợi ý: QHĐ trên DAG, nhưng chỉ cập nhật từ những đỉnh đã tới được từ đỉnh 1.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các chuyến bay.", "Số thành phố hoặc `IMPOSSIBLE`.",
    ["5 5\n1 2\n2 5\n1 3\n3 4\n4 5\n"], _g, _sol, tags=["DAG", "QHĐ trên DAG"])


# 10 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m, w=True)
    order = topo(n, adj)
    INF = float("inf")
    d = [INF] * (n + 1); d[1] = 0
    for u in order:
        if d[u] < INF:
            for v, c in adj[u]:
                if d[u] + c < d[v]:
                    d[v] = d[u] + c
    return L(x if x < INF else "INF" for x in d[1:])


add(T, "Đường đi ngắn nhất trên DAG", 3, """
Cho DAG có trọng số trên cung (có thể **âm**). Tính khoảng cách ngắn nhất từ đỉnh 1 tới mọi đỉnh (in `INF` nếu không tới được).

Gợi ý: trên DAG không cần Dijkstra hay Bellman-Ford: nới lỏng các cung theo thứ tự topo, `O(n + m)`, đúng cả với trọng số âm.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (|w| ≤ 10^9).", "Một dòng gồm `n` giá trị.",
    ["4 4\n1 2 5\n1 3 2\n3 2 -4\n2 4 1\n"], _gs(dag=True, w=(-10**9, 10**9)), _sol, tags=["DAG", "đường đi ngắn nhất"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n, es = _gd(r, s, dag=True)
    return lines(J(n, len(es)), L(arr(r, n, 1, 10**6)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); t = [0] + rd.ints(n); adj, _ = _read_di(rd, n, m)
    order = topo(n, adj)
    start = [0] * (n + 1)
    for u in order:
        for v, _ in adj[u]:
            if start[u] + t[u] > start[v]:
                start[v] = start[u] + t[u]
    return max(start[v] + t[v] for v in range(1, n + 1))


add(T, "Lập lịch dự án", 3, """
Dự án gồm `n` công việc, việc `i` mất `t_i` ngày. Có `m` ràng buộc `u v`: việc `v` chỉ bắt đầu khi việc `u` đã xong.
Các việc không ràng buộc có thể làm song song. Dự án hoàn thành sớm nhất sau bao nhiêu ngày?

Gợi ý: thời điểm bắt đầu sớm nhất của `v` = `max(bắt đầu[u] + t_u)`. Đáp án là đường đi "dài nhất" (đường găng) trên DAG.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). Dòng hai gồm `t_1..t_n` (1 ≤ t ≤ 10^6). `m` dòng sau là các ràng buộc.",
    "Số ngày ít nhất.", ["4 3\n3 2 4 1\n1 2\n1 3\n3 4\n"], _g, _sol, tags=["DAG", "đường găng"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    return lines(J(n, m), *(L(arr(r, m, 1, r.choice([3, 100, 10**9]))) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = [rd.ints(m) for _ in range(n)]
    cells = sorted(((a[i][j], i, j) for i in range(n) for j in range(m)), reverse=True)
    dp = [[1] * m for _ in range(n)]
    for v, i, j in cells:
        best = 1
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = i + di, j + dj
            if 0 <= x < n and 0 <= y < m and a[x][y] > v and dp[x][y] + 1 > best:
                best = dp[x][y] + 1
        dp[i][j] = best
    return max(max(row) for row in dp)


add(T, "Đường đi tăng dài nhất trên lưới", 3, """
Trên lưới số `n × m`, tìm đường đi dài nhất (số ô) sao cho mỗi bước sang ô kề cạnh có giá trị **lớn hơn hẳn** ô hiện tại.

Gợi ý: cung `ô thấp → ô cao` tạo thành DAG. Xử lý các ô theo giá trị giảm dần (đó chính là một thứ tự topo).
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 500). `n` dòng sau mỗi dòng `m` số (1 ≤ a ≤ 10^9).", "Độ dài lớn nhất.",
    ["3 3\n9 9 4\n6 6 8\n2 1 1\n"], _g, _sol, tags=["QHĐ trên DAG", "lưới"])


# 13 ----------------------------------------------------------------------
def _cond(n, adj):
    comp, k = scc(n, adj)
    cadj = [set() for _ in range(k)]
    for u in range(1, n + 1):
        for v, _ in adj[u]:
            if comp[u] != comp[v]:
                cadj[comp[u]].add(comp[v])
    return comp, k, cadj


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    comp, k, cadj = _cond(n, adj)
    indeg = [0] * k
    for c in range(k):
        for d in cadj[c]:
            indeg[d] += 1
    return sum(1 for c in range(k) if indeg[c] == 0)


add(T, "Lan truyền tin đồn", 3, """
Có `n` người; `u v` nghĩa là nếu `u` biết tin thì sẽ kể cho `v`. Cần kể trực tiếp cho ít nhất bao nhiêu người để cuối cùng ai cũng biết tin?

Gợi ý: nén các TPLTM thành một đỉnh (đồ thị nén là DAG). Đáp án = số TPLTM có bậc vào bằng 0.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v`.", "Số người ít nhất.",
    ["5 4\n1 2\n2 1\n3 4\n5 4\n"], _gs(dag=False), _sol, tags=["TPLTM", "đồ thị nén"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n, es = _gd(r, s, dag=False)
    return lines(J(n, len(es)), L(arr(r, n, 1, 10**9)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); coin = [0] + rd.ints(n); adj, _ = _read_di(rd, n, m)
    comp, k, cadj = _cond(n, adj)
    val = [0] * k
    for v in range(1, n + 1):
        val[comp[v]] += coin[v]
    best = val[:]  # Kosaraju đánh số comp theo thứ tự topo → duyệt ngược
    for c in range(k - 1, -1, -1):
        for d in cadj[c]:
            if val[c] + best[d] > best[c]:
                best[c] = val[c] + best[d]
    return max(best)


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); coin = [0] + rd.ints(n); adj, _ = _read_di(rd, n, m)
    reach = _br_reach(n, adj)
    # với đồ thị nhỏ: QHĐ trên các tập TPLTM bằng duyệt mọi đường (memo theo đỉnh trên đồ thị nén)
    comp = {}
    for u in range(1, n + 1):
        comp[u] = frozenset(v for v in reach[u - 1] if u in reach[v - 1])
    from functools import lru_cache

    @lru_cache(None)
    def go(c):
        here = sum(coin[v] for v in c)
        nxt = {comp[v] for u in c for v, _ in adj[u] if comp[v] != c}
        return here + max((go(d) for d in nxt), default=0)
    return max(go(comp[u]) for u in range(1, n + 1))


add(T, "Nhặt xu", 4, """
Có `n` căn phòng và `m` hành lang một chiều; phòng `i` chứa `c_i` đồng xu. Bạn bắt đầu ở phòng bất kỳ, đi theo hành lang bao nhiêu
lần cũng được (có thể quay lại phòng cũ) và nhặt hết xu ở mỗi phòng đi qua. Nhặt được nhiều nhất bao nhiêu xu?

Gợi ý: trong một TPLTM có thể đi hết mọi phòng → nén mỗi TPLTM thành một đỉnh có trọng số = tổng xu, rồi tìm đường đi có tổng
lớn nhất trên DAG nén.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). Dòng hai gồm `c_1..c_n` (1 ≤ c ≤ 10^9). `m` dòng sau là các hành lang.",
    "Số xu lớn nhất.", ["4 4\n4 5 2 7\n1 2\n2 1\n1 3\n4 3\n"], _g, _sol, brute=_br, tags=["TPLTM", "QHĐ trên DAG"])


# 15 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    comp, k, cadj = _cond(n, adj)
    if k == 1:
        return 0
    indeg = [0] * k
    for c in range(k):
        for d in cadj[c]:
            indeg[d] += 1
    src = sum(1 for c in range(k) if indeg[c] == 0)
    snk = sum(1 for c in range(k) if not cadj[c])
    return max(src, snk)


add(T, "Thêm cung để liên thông mạnh", 4, """
Cần thêm ít nhất bao nhiêu cung để đồ thị có hướng trở thành liên thông mạnh?

Gợi ý: nén TPLTM. Nếu chỉ có một TPLTM thì đáp án 0. Ngược lại đáp án = `max(số đỉnh nguồn, số đỉnh hút)` của DAG nén
(nguồn: bậc vào 0, hút: bậc ra 0).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung.", "Số cung ít nhất.",
    ["4 3\n1 2\n2 3\n3 1\n"], _gs(dag=False), _sol, tags=["TPLTM", "đồ thị nén"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2000); m = S(s, 1, 10**4)
    es = rdigraph(r, n, m, dag=r.random() < .5)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    comp, k, cadj = _cond(n, adj)
    bits = [0] * k
    for v in range(1, n + 1):
        bits[comp[v]] |= 1 << v
    reach = bits[:]
    for c in range(k - 1, -1, -1):
        for d in cadj[c]:
            reach[c] |= reach[d]
    return L(bin(reach[comp[v]]).count("1") for v in range(1, n + 1))


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    return L(len(x) for x in _br_reach(n, adj))


add(T, "Số đỉnh tới được", 4, """
Với mỗi đỉnh `v`, đếm số đỉnh tới được từ `v` (tính cả chính nó).

Gợi ý: nén TPLTM; trên DAG nén, tập tới được `reach[c] = các đỉnh của c ∪ reach[con]` — biểu diễn bằng `bitset<2000>`
và tính theo thứ tự topo ngược. Độ phức tạp `O(n·m / 64)`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 2000, 0 ≤ m ≤ 10^4). `m` dòng sau là các cung.", "Một dòng gồm `n` số.",
    ["4 4\n1 2\n2 3\n3 2\n4 1\n"], _g, _sol, brute=_br, tags=["TPLTM", "bitset"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 16)
    es = rdigraph(r, n, r.randint(0, n * (n - 1) // 4), dag=True) if n > 1 else []
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    need = [0] * n
    for _ in range(m):
        a, b = rd.ints(2); need[b - 1] |= 1 << (a - 1)
    dp = [0] * (1 << n); dp[0] = 1
    for mask in range(1 << n):
        if dp[mask]:
            for v in range(n):
                if not mask >> v & 1 and need[v] & mask == need[v]:
                    dp[mask | 1 << v] += dp[mask]
    return dp[-1]


def _br(s):
    from itertools import permutations
    rd = Rd(s); n, m = rd.ints(2); es = [rd.ints(2) for _ in range(m)]
    if n > 8:
        return _sol(s)
    c = 0
    for p in permutations(range(1, n + 1)):
        pos = {v: i for i, v in enumerate(p)}
        c += all(pos[a] < pos[b] for a, b in es)
    return c


add(T, "Đếm số thứ tự topo", 4, """
Đếm số thứ tự topo khác nhau của DAG `n` đỉnh (`n ≤ 16`).

Gợi ý (QHĐ bitmask): `dp[mask]` = số cách sắp xếp tập đỉnh `mask` thành tiền tố của một thứ tự topo. Thêm đỉnh `v` vào sau nếu mọi
đỉnh phải đứng trước `v` đều đã nằm trong `mask`.
""", "Dòng đầu `n, m` (1 ≤ n ≤ 16). `m` dòng sau là các cung (không có chu trình).", "Số thứ tự topo.",
    ["3 1\n1 2\n", "4 0\n"], _g, _sol, brute=_br, tags=["sắp xếp topo", "QHĐ bitmask"])


# 18 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    order = topo(n, adj)
    f = [0] * (n + 1); f[1] = 1
    for u in order:
        if f[u]:
            for v, _ in adj[u]:
                f[v] = (f[v] + f[u]) % MOD
    g = [0] * (n + 1); g[n] = 1
    for u in reversed(order):
        for v, _ in adj[u]:
            g[u] = (g[u] + g[v]) % MOD
    return L(f[v] * g[v] % MOD for v in range(1, n + 1))


add(T, "Số đường đi qua mỗi đỉnh", 4, """
Cho DAG. Với mỗi đỉnh `v`, đếm số đường đi từ đỉnh 1 tới đỉnh `n` **đi qua** `v`, modulo `10^9 + 7`.

Gợi ý: `f[v]` = số đường đi từ 1 tới `v` (theo thứ tự topo), `g[v]` = số đường đi từ `v` tới `n` (theo thứ tự topo ngược).
Đáp án là `f[v] · g[v]`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung (không có chu trình).", "Một dòng gồm `n` số.",
    ["4 4\n1 2\n2 4\n1 3\n3 4\n"], _gs(dag=True), _sol, tags=["DAG", "QHĐ đếm"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    m = S(s, 1, 10**5)
    k = S(s, 1, 10**5)
    out = []
    for _ in range(k):
        a = ("+" if r.random() < .5 else "-") + str(r.randint(1, m))
        b = ("+" if r.random() < .5 else "-") + str(r.randint(1, m))
        out.append(J(a, b))
    return lines(J(k, m), *out)


def _sat(s):
    t = s.split(); k, m = int(t[0]), int(t[1])
    n = 2 * m
    adj = [[] for _ in range(n + 1)]

    def node(lit):
        x = int(lit[1:])
        return 2 * x - 1 if lit[0] == "+" else 2 * x  # 2x-1: x đúng, 2x: x sai

    def neg(v):
        return v + 1 if v % 2 else v - 1
    for i in range(k):
        a, b = node(t[2 + 2 * i]), node(t[3 + 2 * i])
        adj[neg(a)].append((b, 1)); adj[neg(b)].append((a, 1))
    comp, _ = scc(n, adj)
    return "NO" if any(comp[2 * x - 1] == comp[2 * x] for x in range(1, m + 1)) else "YES"


def _br(s):
    t = s.split(); k, m = int(t[0]), int(t[1])
    cl = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(k)]

    def val(lit, mask):
        x = int(lit[1:]) - 1
        return (mask >> x & 1) == (lit[0] == "+")
    return "YES" if any(all(val(a, mk) or val(b, mk) for a, b in cl) for mk in range(1 << m)) else "NO"


add(T, "Chọn món pizza (2-SAT)", 5, """
Có `m` loại topping và `k` thành viên. Mỗi thành viên đưa ra hai mong muốn dạng `+x` (muốn có topping `x`) hoặc `-x` (không muốn có `x`),
và hài lòng nếu **ít nhất một** trong hai mong muốn được đáp ứng. Có cách chọn topping để mọi người hài lòng không?

Gợi ý (2-SAT): mỗi biến `x` có hai đỉnh `x` và `¬x`. Mệnh đề `(a ∨ b)` cho hai cung `¬a → b` và `¬b → a`.
Có nghiệm ⇔ không có biến nào mà `x` và `¬x` cùng một TPLTM.
""", "Dòng đầu `k, m` (1 ≤ k, m ≤ 10^5). `k` dòng sau mỗi dòng hai mong muốn.", "`YES` hoặc `NO`.",
    ["3 5\n+1 +2\n-1 +3\n+4 -2\n", "4 1\n+1 +1\n-1 -1\n+1 -1\n-1 +1\n"], _g, _sat,
    brute=lambda s: _br(s) if int(s.split()[1]) <= 12 else _sat(s), tags=["2-SAT", "TPLTM"])


# 20 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    comp, k, cadj = _cond(n, adj)
    size = [0] * k; bits = [0] * k
    for v in range(1, n + 1):
        size[comp[v]] += 1; bits[comp[v]] |= 1 << v
    reach = bits[:]
    for c in range(k - 1, -1, -1):
        for d in cadj[c]:
            reach[c] |= reach[d]
    return sum(size[c] * (bin(reach[c]).count("1") - 1) for c in range(k))


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    return sum(len(x) - 1 for x in _br_reach(n, adj))


add(T, "Đếm cặp tới được", 5, """
Đếm số cặp có thứ tự `(u, v)` với `u ≠ v` sao cho đi được từ `u` tới `v`.

Gợi ý: nén TPLTM, dùng bitset tập đỉnh tới được cho mỗi thành phần (như bài "Số đỉnh tới được"), rồi cộng
`size[c] · (|reach[c]| - 1)`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 2000, 0 ≤ m ≤ 10^4). `m` dòng sau là các cung.", "Số cặp.",
    ["3 3\n1 2\n2 1\n2 3\n"], (lambda r, s: (lambda n: (lambda es: lines(J(n, len(es)), *(J(a, b) for a, b in es)))(
        rdigraph(r, n, S(s, 1, 10**4), dag=r.random() < .3)))(S(s, 2, 2000))), _sol, brute=_br, tags=["TPLTM", "bitset"])


# 21 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_di(rd, n, m)
    order = topo(n, adj)
    win = [False] * (n + 1)
    for u in reversed(order):
        win[u] = any(not win[v] for v, _ in adj[u])
    return "".join("W" if win[v] else "L" for v in range(1, n + 1))


add(T, "Trò chơi trên DAG", 3, """
Một quân cờ đặt ở một đỉnh của DAG. Hai người luân phiên di chuyển quân cờ theo một cung đi ra; ai không đi được nữa thì thua.
Với mỗi đỉnh xuất phát, người đi trước thắng (`W`) hay thua (`L`) nếu cả hai chơi tối ưu?

Gợi ý: đỉnh không có cung ra là thế thua. Một đỉnh là thế thắng ⇔ có cung tới một thế thua. Tính theo thứ tự topo ngược.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cung (không có chu trình).", "Xâu `n` ký tự `W`/`L`.",
    ["4 3\n1 2\n2 3\n1 4\n"], _gs(dag=True), _sol, tags=["DAG", "lý thuyết trò chơi"])
