"""Chuyên đề 13: Đường đi ngắn nhất (Dijkstra, Bellman-Ford, Floyd-Warshall)."""
import heapq
from .base import add, Rd, S, J, L, arr, lines, rgraph, rdigraph

T = 13
INF = float("inf")
MOD = 10**9 + 7


def dijkstra(adj, srcs):
    n = len(adj) - 1
    d = [INF] * (n + 1); h = []
    for s_ in srcs:
        d[s_] = 0; h.append((0, s_))
    heapq.heapify(h)
    while h:
        du, u = heapq.heappop(h)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            nd = du + w
            if nd < d[v]:
                d[v] = nd; heapq.heappush(h, (nd, v))
    return d


def _read_w(rd, n, m, directed=True):
    adj = [[] for _ in range(n + 1)]; es = []
    for _ in range(m):
        a, b, w = rd.ints(3)
        adj[a].append((b, w)); es.append((a, b, w))
        if not directed:
            adj[b].append((a, w))
    return adj, es


def _gw(directed=True, wlo=1, whi=10**9, nmax=10**5, mmax=2 * 10**5, connected=None):
    def g(r, s):
        n = S(s, 2, nmax); m = S(s, 1, mmax) // r.choice([1, 2])
        if directed:
            es = rdigraph(r, n, m)
            if r.random() < .6:
                path = list(range(1, n + 1)); r.shuffle(path)
                path.remove(1); path.remove(n); path = [1] + path[:r.randint(0, len(path))] + [n]
                es = list(dict.fromkeys(es + list(zip(path, path[1:]))))
        else:
            es = rgraph(r, n, m, connected=connected if connected is not None else r.random() < .6)
        whi_ = whi if r.random() < .7 else min(whi, 10)
        return lines(J(n, len(es)), *(J(a, b, r.randint(wlo, whi_)) for a, b in es))
    return g


# 1 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m)
    return L(x if x < INF else -1 for x in dijkstra(adj, [1])[1:])


add(T, "Dijkstra", 1, """
Đồ thị **có hướng** với trọng số không âm. Tính độ dài đường đi ngắn nhất từ đỉnh 1 tới mọi đỉnh (`-1` nếu không tới được).

Gợi ý: Dijkstra với `priority_queue<pair<long long,int>>` (min-heap). Bỏ qua phần tử lấy ra nếu khoảng cách đã cũ.
Độ phức tạp `O((n + m) log n)`. Khoảng cách có thể vượt `int` — dùng `long long`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (0 ≤ w ≤ 10^9).", "Một dòng gồm `n` số.",
    ["3 4\n1 2 6\n1 3 2\n3 2 3\n1 3 4\n"], _gw(wlo=0), _sol, tags=["Dijkstra"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m, directed=False)
    d = dijkstra(adj, [1])[n]
    return d if d < INF else -1


add(T, "Đường về nhà", 1, """
Bản đồ có `n` giao lộ và `m` con đường **hai chiều** có độ dài. Tìm quãng đường ngắn nhất từ giao lộ 1 tới giao lộ `n` (`-1` nếu không đi được).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).", "Độ dài ngắn nhất hoặc `-1`.",
    ["4 4\n1 2 1\n2 4 5\n1 3 2\n3 4 2\n"], _gw(directed=False), _sol, tags=["Dijkstra"])


# 3 -----------------------------------------------------------------------
def _floyd(n, es, undirected=True):
    d = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][i] = 0
    for a, b, w in es:
        if w < d[a][b]:
            d[a][b] = w
            if undirected:
                d[b][a] = w
    for k in range(1, n + 1):
        dk = d[k]
        for i in range(1, n + 1):
            di = d[i]; dik = di[k]
            if dik == INF:
                continue
            for j in range(1, n + 1):
                v = dik + dk[j]
                if v < di[j]:
                    di[j] = v
    return d


def _g(r, s):
    n = S(s, 2, 200); m = S(s, 1, n * (n - 1) // 2)
    es = rgraph(r, n, m)
    q = S(s, 1, 10**5)
    return lines(J(n, len(es), q), *(J(a, b, r.randint(1, 10**9)) for a, b in es),
                 *(J(r.randint(1, n), r.randint(1, n)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, m, q = rd.ints(3); _, es = _read_w(rd, n, m)
    d = _floyd(n, es)
    out = []
    for _ in range(q):
        a, b = rd.ints(2)
        out.append(d[a][b] if d[a][b] < INF else -1)
    return out


add(T, "Floyd-Warshall", 1, """
Có `n` thành phố, `m` con đường hai chiều và `q` câu hỏi "khoảng cách ngắn nhất giữa `a` và `b`" (`-1` nếu không đi được).

Gợi ý: `n` nhỏ nên tính sẵn khoảng cách mọi cặp bằng Floyd-Warshall `O(n³)`:
`for k: for i: for j: d[i][j] = min(d[i][j], d[i][k] + d[k][j])` — vòng `k` phải ở **ngoài cùng**.
""", "Dòng đầu `n, m, q` (2 ≤ n ≤ 200, 1 ≤ q ≤ 10^5). `m` dòng là các con đường `u v w` (1 ≤ w ≤ 10^9), `q` dòng là câu hỏi.",
    "Mỗi câu hỏi in một dòng.", ["4 3 4\n1 2 5\n1 3 9\n2 3 3\n1 2\n2 1\n1 3\n1 4\n"], _g, _sol, tags=["Floyd"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m)
    d0 = [INF] * (n + 1); d1 = [INF] * (n + 1)
    d0[1] = 0; h = [(0, 1, 0)]
    while h:
        du, u, used = heapq.heappop(h)
        if du > (d1 if used else d0)[u]:
            continue
        for v, w in adj[u]:
            if not used:
                if du + w < d0[v]:
                    d0[v] = du + w; heapq.heappush(h, (d0[v], v, 0))
                if du + w // 2 < d1[v]:
                    d1[v] = du + w // 2; heapq.heappush(h, (d1[v], v, 1))
            elif du + w < d1[v]:
                d1[v] = du + w; heapq.heappush(h, (d1[v], v, 1))
    a = min(d0[n], d1[n])
    return a if a < INF else -1


add(T, "Phiếu giảm giá", 3, """
Có `n` thành phố và `m` chuyến bay một chiều có giá vé. Bạn có **một** phiếu giảm giá dùng cho tối đa một chuyến bay: giá vé chuyến đó
còn `⌊w/2⌋`. Tìm chi phí nhỏ nhất để bay từ thành phố 1 tới thành phố `n` (`-1` nếu không thể).

Gợi ý: Dijkstra trên trạng thái `(đỉnh, đã dùng phiếu chưa)` — đồ thị "hai tầng".
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).", "Chi phí nhỏ nhất.",
    ["3 4\n1 2 3\n2 3 1\n1 3 7\n2 1 5\n"], _gw(), _sol, tags=["Dijkstra", "đồ thị trạng thái"])


# 5 -----------------------------------------------------------------------
def _gneg(r, s):
    n = S(s, 2, 500); m = S(s, 1, 2000)
    es = rdigraph(r, n, m)
    bias = r.choice([0, 3, 10])
    return lines(J(n, len(es)), *(J(a, b, r.randint(-10 + bias, 10**4)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); _, es = _read_w(rd, n, m)
    d = [0] * (n + 1)  # nguồn ảo nối tới mọi đỉnh với trọng số 0
    for _ in range(n):
        ch = False
        for a, b, w in es:
            if d[a] + w < d[b]:
                d[b] = d[a] + w; ch = True
        if not ch:
            return "NO"
    return "YES"


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); _, es = _read_w(rd, n, m)
    d = _floyd(n, es, undirected=False)
    return "YES" if any(d[i][i] < 0 for i in range(1, n + 1)) else "NO"


add(T, "Chu trình âm", 2, """
Đồ thị có hướng có trọng số (có thể âm). Đồ thị có chứa chu trình có tổng trọng số **âm** không?

Gợi ý (Bellman-Ford): khởi tạo `d[v] = 0` cho mọi đỉnh (như có nguồn ảo nối tới tất cả), nới lỏng mọi cung `n` lần.
Nếu lần thứ `n` vẫn còn nới lỏng được thì có chu trình âm.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 500, 1 ≤ m ≤ 2000). `m` dòng sau mỗi dòng `u v w` (|w| ≤ 10^4).", "`YES` hoặc `NO`.",
    ["3 3\n1 2 1\n2 3 -2\n3 1 0\n", "3 3\n1 2 1\n2 3 -2\n3 1 2\n"], _gneg, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 60 else _sol(s), tags=["Bellman-Ford"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 1000); m = S(s, 1, 3000)
    # trọng số âm nhưng không có chu trình âm: dùng thế vị p (w' = w + p[a] - p[b] với w ≥ 0)
    p = [0] + arr(r, n, 0, 10**4)
    es = rdigraph(r, n, m)
    return lines(J(n, len(es)), *(J(a, b, r.randint(0, 100) + p[a] - p[b]) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); _, es = _read_w(rd, n, m)
    d = [INF] * (n + 1); d[1] = 0
    for _ in range(n - 1):
        ch = False
        for a, b, w in es:
            if d[a] + w < d[b]:
                d[b] = d[a] + w; ch = True
        if not ch:
            break
    return L(x if x < INF else "INF" for x in d[1:])


add(T, "Bellman-Ford", 2, """
Đồ thị có hướng, trọng số **có thể âm** nhưng đảm bảo không có chu trình âm. Tính khoảng cách ngắn nhất từ đỉnh 1 tới mọi đỉnh
(`INF` nếu không tới được).

Gợi ý: Dijkstra sai khi có cạnh âm! Dùng Bellman-Ford: lặp `n - 1` lần, mỗi lần nới lỏng tất cả các cung. `O(n·m)`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 1000, 1 ≤ m ≤ 3000). `m` dòng sau mỗi dòng `u v w` (|w| ≤ 2·10^4).", "Một dòng gồm `n` giá trị.",
    ["4 4\n1 2 4\n1 3 2\n3 2 -3\n2 4 1\n"], _g, _sol, tags=["Bellman-Ford"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rgraph(r, n, m, connected=r.random() < .7)
    k = r.randint(1, max(1, n // r.choice([1, 10, 1000])))
    return lines(J(n, len(es), k), L(r.sample(range(1, n + 1), k)), *(J(a, b, r.randint(1, 10**6)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m, k = rd.ints(3); src = rd.ints(k); adj, _ = _read_w(rd, n, m, directed=False)
    return L(x if x < INF else -1 for x in dijkstra(adj, src)[1:])


add(T, "Bệnh viện gần nhất", 2, """
Có `n` khu dân cư, `m` con đường hai chiều và `k` khu có bệnh viện. Với mỗi khu, tính khoảng cách tới bệnh viện **gần nhất** (`-1` nếu không có).

Gợi ý: Dijkstra **đa nguồn** — đưa mọi bệnh viện vào hàng đợi với khoảng cách 0 ngay từ đầu (tương đương thêm đỉnh nguồn ảo).
""", "Dòng đầu `n, m, k`. Dòng hai gồm `k` khu có bệnh viện. `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^6).",
    "Một dòng gồm `n` số.", ["5 4 2\n1 5\n1 2 3\n2 3 1\n3 4 2\n4 5 10\n"], _g, _sol, tags=["Dijkstra", "đa nguồn"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    return lines(J(n, m), *(L(arr(r, m, 0, r.choice([9, 10**6]))) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = [rd.ints(m) for _ in range(n)]
    d = [[INF] * m for _ in range(n)]
    d[0][0] = a[0][0]; h = [(a[0][0], 0, 0)]
    while h:
        du, x, y = heapq.heappop(h)
        if du > d[x][y]:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            i, j = x + dx, y + dy
            if 0 <= i < n and 0 <= j < m and du + a[i][j] < d[i][j]:
                d[i][j] = du + a[i][j]; heapq.heappush(h, (d[i][j], i, j))
    return d[n - 1][m - 1]


add(T, "Đường đi rẻ nhất trên lưới", 2, """
Lưới `n × m`, ô `(i, j)` có phí `a[i][j]` — phải trả mỗi khi đi vào ô đó (kể cả ô xuất phát). Đi 4 hướng từ ô `(1, 1)` tới `(n, m)`.
Tìm tổng phí nhỏ nhất.

Gợi ý: được đi cả lên trên và sang trái nên **không** dùng QHĐ đơn giản được — hãy chạy Dijkstra trên lưới.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 500). `n` dòng sau mỗi dòng `m` số (0 ≤ a ≤ 10^6).", "Tổng phí nhỏ nhất.",
    ["3 3\n1 9 1\n1 9 1\n1 1 1\n", "3 4\n1 1 1 1\n9 9 9 1\n1 1 1 1\n"], _g, _sol, tags=["Dijkstra", "lưới"])


# 9 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m)
    d = [INF] * (n + 1); cnt = [0] * (n + 1); mn = [0] * (n + 1); mx = [0] * (n + 1)
    d[1] = 0; cnt[1] = 1; h = [(0, 1)]
    done = [False] * (n + 1)
    while h:
        du, u = heapq.heappop(h)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            nd = du + w
            if nd < d[v]:
                d[v] = nd; cnt[v] = cnt[u]; mn[v] = mn[u] + 1; mx[v] = mx[u] + 1
                heapq.heappush(h, (nd, v))
            elif nd == d[v]:
                cnt[v] = (cnt[v] + cnt[u]) % MOD
                mn[v] = min(mn[v], mn[u] + 1); mx[v] = max(mx[v], mx[u] + 1)
    return J(d[n], cnt[n], mn[n], mx[n])


def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rdigraph(r, n, m)
    path = list(range(2, n)); r.shuffle(path); path = [1] + path[:r.randint(0, n - 2)] + [n]
    es = list(dict.fromkeys(es + list(zip(path, path[1:]))))
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, r.choice([3, 10**9]))) for a, b in es))


add(T, "Điều tra đường bay", 4, """
Bay từ thành phố 1 tới thành phố `n` (đảm bảo đi được, mọi giá vé dương). Hãy cho biết:
1. giá vé nhỏ nhất;
2. số hành trình đạt giá nhỏ nhất (modulo `10^9 + 7`);
3. số chuyến bay ít nhất trong các hành trình rẻ nhất;
4. số chuyến bay nhiều nhất trong các hành trình rẻ nhất.

Gợi ý: trong Dijkstra, khi tìm được đường bằng `d[v]` thì cộng dồn số cách và cập nhật min/max số cạnh.
Vì trọng số dương nên đỉnh được lấy ra khỏi heap theo thứ tự `d` tăng dần, các giá trị đã chốt khi dùng.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).", "Bốn số trên một dòng.",
    ["4 5\n1 4 5\n1 2 4\n2 4 5\n1 3 2\n3 4 3\n"], _g, _sol, tags=["Dijkstra", "đếm"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(directed=False)(r, s)
    n = int(base.split()[0])
    return base + f"{r.randint(1, n)}\n"


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m, directed=False); k = rd.int()
    dk = dijkstra(adj, [k])
    v = dk[1] + dk[n]
    return v if v < INF else -1


add(T, "Ghé qua trạm xăng", 2, """
Đi từ đỉnh 1 tới đỉnh `n` trên đồ thị vô hướng có trọng số, nhưng bắt buộc phải **ghé qua** đỉnh `k`. Tìm quãng đường ngắn nhất (`-1` nếu không thể).

Gợi ý: đáp án = `dist(1, k) + dist(k, n)` — chỉ cần một lần Dijkstra từ `k` (vì đồ thị vô hướng).
""", "Dòng đầu `n, m`. `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9). Dòng cuối là `k`.", "Độ dài ngắn nhất hoặc `-1`.",
    ["4 4\n1 2 1\n2 4 1\n1 3 5\n3 4 5\n3\n"], _g, _sol, tags=["Dijkstra"])


# 11 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, es = _read_w(rd, n, m, directed=False)
    d1 = dijkstra(adj, [1]); dn = dijkstra(adj, [n])
    D = d1[n]
    if D == INF:
        return 0
    return sum(1 for a, b, w in es if d1[a] + w + dn[b] == D or d1[b] + w + dn[a] == D)


add(T, "Cạnh trên đường đi ngắn nhất", 3, """
Đồ thị vô hướng có trọng số. Đếm số cạnh nằm trên **ít nhất một** đường đi ngắn nhất từ đỉnh 1 tới đỉnh `n`.

Gợi ý: Dijkstra từ 1 và từ `n`. Cạnh `(u, v, w)` thoả mãn ⇔ `d1[u] + w + dn[v] = D` hoặc `d1[v] + w + dn[u] = D`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).", "Số cạnh.",
    ["4 5\n1 2 1\n2 4 1\n1 3 1\n3 4 1\n1 4 3\n"], _gw(directed=False), _sol, tags=["Dijkstra"])


# 12 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, es = _read_w(rd, n, m, directed=False)
    d1 = dijkstra(adj, [1]); dn = dijkstra(adj, [n])
    D = d1[n]
    if D == INF:
        return "-1"
    on = [v for v in range(1, n + 1) if d1[v] + dn[v] == D]
    # đỉnh v nằm trên mọi đường đi ngắn nhất ⇔ không có cạnh "đường đi ngắn nhất" nào bắc qua mốc d1[v]
    # (khoảng mở (d1[a], d1[b]) chứa d1[v]) và v là đỉnh duy nhất trên các đường ngắn nhất có khoảng cách d1[v].
    events = []
    for a, b, w in es:
        for x, y in ((a, b), (b, a)):
            if d1[x] + w + dn[y] == D:
                events.append((d1[x], d1[y]))
    from collections import Counter
    layer = Counter(d1[v] for v in on)
    # đánh dấu các mốc bị cạnh bắc qua: dùng sắp xếp + quét
    marks = sorted(set(d1[v] for v in on))
    idx = {x: i for i, x in enumerate(marks)}
    diff = [0] * (len(marks) + 1)
    for x, y in events:
        i, j = idx[x], idx[y]
        if j - i >= 2:
            diff[i + 1] += 1; diff[j] -= 1
    cov, run = [0] * len(marks), 0
    for i in range(len(marks)):
        run += diff[i]; cov[i] = run
    res = sorted(v for v in on if layer[d1[v]] == 1 and cov[idx[d1[v]]] == 0)
    return lines(str(len(res)), L(res)).rstrip("\n")


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); adj, es = _read_w(rd, n, m, directed=False)
    D = dijkstra(adj, [1])[n]
    if D == INF:
        return "-1"
    res = []
    for v in range(1, n + 1):
        if v in (1, n):
            res.append(v); continue
        adj2 = [[(x, w) for x, w in adj[u] if x != v] if u != v else [] for u in range(n + 1)]
        if dijkstra(adj2, [1])[n] > D:
            res.append(v)
    return lines(str(len(res)), L(res)).rstrip("\n")


def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rgraph(r, n, m, connected=r.random() < .8)
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, r.choice([2, 5, 10**9]))) for a, b in es))


add(T, "Điểm kiểm soát bắt buộc", 4, """
Đồ thị vô hướng có trọng số dương. Tìm các đỉnh nằm trên **mọi** đường đi ngắn nhất từ đỉnh 1 tới đỉnh `n` (gồm cả 1 và `n`).
Nếu không có đường đi in `-1`.

Gợi ý: chỉ xét các đỉnh có `d1[v] + dn[v] = D`. Đỉnh `v` bắt buộc ⇔ nó là đỉnh **duy nhất** có khoảng cách `d1[v]` trong số đó,
và không có cạnh nào của đồ thị đường đi ngắn nhất "bắc qua" mốc `d1[v]` (đi từ khoảng cách nhỏ hơn tới lớn hơn `d1[v]`).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).",
    "Dòng đầu là số đỉnh `k`, dòng hai là các đỉnh tăng dần (hoặc chỉ một dòng `-1`).",
    ["5 5\n1 2 1\n2 3 1\n3 5 1\n2 4 1\n4 5 1\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 40 else _sol(s),
    tags=["Dijkstra", "đồ thị đường đi ngắn nhất"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 200); m = S(s, 1, n * (n - 1) // 2)
    es = rgraph(r, n, m)
    q = S(s, 1, 10**5)
    return lines(J(n, len(es), q), *(J(a, b, r.randint(1, 10**9)) for a, b in es),
                 *(J(r.randint(1, n), r.randint(1, n)) for _ in range(q)))


def _sol(s):
    rd = Rd(s); n, m, q = rd.ints(3); _, es = _read_w(rd, n, m)
    d = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][i] = 0
    for a, b, w in es:
        d[a][b] = d[b][a] = min(d[a][b], w)
    for k in range(1, n + 1):
        dk = d[k]
        for i in range(1, n + 1):
            di = d[i]; dik = di[k]
            if dik == INF:
                continue
            for j in range(1, n + 1):
                v = dik if dik > dk[j] else dk[j]
                if v < di[j]:
                    di[j] = v
    out = []
    for _ in range(q):
        a, b = rd.ints(2)
        out.append(d[a][b] if d[a][b] < INF else -1)
    return out


add(T, "Đường đi ít dốc nhất", 3, """
Mỗi con đường hai chiều có độ dốc `w`. Với mỗi câu hỏi `(a, b)`, tìm đường đi từ `a` tới `b` sao cho **độ dốc lớn nhất** trên đường
là nhỏ nhất; in giá trị đó (0 nếu `a = b`, `-1` nếu không đi được).

Gợi ý: biến thể Floyd: `d[i][j] = min(d[i][j], max(d[i][k], d[k][j]))`.
""", "Dòng đầu `n, m, q` (2 ≤ n ≤ 200, 1 ≤ q ≤ 10^5). `m` dòng `u v w` (1 ≤ w ≤ 10^9), `q` dòng câu hỏi.",
    "Mỗi câu hỏi in một dòng.", ["4 4 2\n1 2 5\n2 3 2\n1 3 9\n3 4 1\n1 3\n1 4\n"], _g, _sol, tags=["Floyd", "minimax"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**4); m = S(s, 1, 5 * 10**4)
    es = rdigraph(r, n, m)
    path = list(range(2, n)); r.shuffle(path); path = [1] + path[:r.randint(0, n - 2)] + [n]
    es = list(dict.fromkeys(es + list(zip(path, path[1:]))))
    k = r.randint(1, 10)
    return lines(J(n, len(es), k), *(J(a, b, r.randint(1, r.choice([5, 10**9]))) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m, k = rd.ints(3); adj, _ = _read_w(rd, n, m)
    cnt = [0] * (n + 1); h = [(0, 1)]; out = []
    while h and len(out) < k:
        d, u = heapq.heappop(h)
        if cnt[u] >= k:
            continue
        cnt[u] += 1
        if u == n:
            out.append(d)
        for v, w in adj[u]:
            if cnt[v] < k:
                heapq.heappush(h, (d + w, v))
    while len(out) < k:
        out.append(-1)
    return L(out)


add(T, "k hành trình rẻ nhất", 4, """
Tìm giá của `k` hành trình rẻ nhất từ thành phố 1 tới `n` (hành trình có thể đi qua một thành phố nhiều lần; hai hành trình khác nhau
nếu dãy chuyến bay khác nhau). In `k` giá theo thứ tự không giảm; nếu có ít hơn `k` hành trình thì in `-1` cho phần còn thiếu.

Gợi ý: Dijkstra cải tiến — cho phép mỗi đỉnh được lấy ra khỏi heap tối đa `k` lần. Lần thứ `i` đỉnh `n` được lấy ra chính là hành trình rẻ thứ `i`.
""", "Dòng đầu `n, m, k` (2 ≤ n ≤ 2·10^4, 1 ≤ m ≤ 5·10^4, 1 ≤ k ≤ 10). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).",
    "Một dòng gồm `k` số.", ["4 6 3\n1 2 1\n1 3 3\n2 3 2\n2 4 6\n3 2 8\n3 4 1\n"], _g, _sol, tags=["Dijkstra", "k đường đi"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 500); m = S(s, 1, 2000)
    es = rdigraph(r, n, m)
    path = list(range(2, n)); r.shuffle(path); path = [1] + path[:r.randint(0, n - 2)] + [n]
    es = list(dict.fromkeys(es + list(zip(path, path[1:]))))
    bias = r.choice([0, 0, 5])
    return lines(J(n, len(es)), *(J(a, b, r.randint(-10**4 + bias * 1000, 10**4 - 6000 + bias * 0)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); _, es = _read_w(rd, n, m)
    NEG = -INF
    d = [NEG] * (n + 1); d[1] = 0
    for _ in range(n - 1):
        for a, b, w in es:
            if d[a] > NEG and d[a] + w > d[b]:
                d[b] = d[a] + w
    bad = [False] * (n + 1)
    for _ in range(n):
        for a, b, w in es:
            if d[a] > NEG and (d[a] + w > d[b] or bad[a]):
                if d[a] + w > d[b]:
                    d[b] = d[a] + w
                bad[b] = True
    return -1 if bad[n] else d[n]


add(T, "Điểm cao nhất", 4, """
Trò chơi có `n` phòng và `m` đường hầm một chiều; đi qua đường hầm được cộng `x` điểm (có thể âm). Bắt đầu ở phòng 1, kết thúc ở phòng `n`
(đảm bảo tới được), có thể đi qua một phòng/đường hầm nhiều lần. Tìm điểm cao nhất; nếu điểm có thể lớn tuỳ ý thì in `-1`.

Gợi ý: Bellman-Ford tìm đường đi **dài nhất** (đổi dấu trọng số). Điểm vô hạn khi có chu trình dương nằm trên một đường đi từ 1 tới `n`:
sau `n - 1` vòng, chạy thêm `n` vòng nữa và lan truyền cờ "vô hạn" theo các cung.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 500, 1 ≤ m ≤ 2000). `m` dòng sau mỗi dòng `u v x` (|x| ≤ 10^4).", "Điểm cao nhất hoặc `-1`.",
    ["4 5\n1 2 3\n2 4 -1\n1 3 -2\n3 4 7\n1 4 4\n", "3 3\n1 2 1\n2 1 1\n2 3 0\n"], _g, _sol, tags=["Bellman-Ford", "chu trình dương"])


# 16 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(directed=False, nmax=5000, mmax=2 * 10**4)(r, s)
    return base + f"{r.randint(0, 10)}\n"


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m, directed=False); k = rd.int()
    d = [[INF] * (n + 1) for _ in range(k + 1)]
    d[0][1] = 0; h = [(0, 1, 0)]
    while h:
        du, u, j = heapq.heappop(h)
        if du > d[j][u]:
            continue
        for v, w in adj[u]:
            if du + w < d[j][v]:
                d[j][v] = du + w; heapq.heappush(h, (du + w, v, j))
            if j < k and du < d[j + 1][v]:
                d[j + 1][v] = du; heapq.heappush(h, (du, v, j + 1))
    best = min(d[j][n] for j in range(k + 1))
    return best if best < INF else -1


add(T, "Đi miễn phí k lần", 4, """
Đồ thị vô hướng có trọng số. Bạn có `k` vé miễn phí, mỗi vé dùng để đi qua một cạnh với chi phí 0. Tìm chi phí nhỏ nhất từ 1 tới `n` (`-1` nếu không thể).

Gợi ý: đồ thị phân tầng `(đỉnh, số vé đã dùng)` gồm `n·(k+1)` trạng thái; chạy Dijkstra.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 5000, 1 ≤ m ≤ 2·10^4). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9). Dòng cuối là `k` (0 ≤ k ≤ 10).",
    "Chi phí nhỏ nhất.", ["4 4\n1 2 10\n2 4 10\n1 3 1\n3 4 100\n1\n"], _g, _sol, tags=["Dijkstra", "đồ thị phân tầng"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 3, 100); m = S(s, 2, n * (n - 1) // 2)
    es = rgraph(r, n, m)
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, 10**6)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); _, es = _read_w(rd, n, m)
    w = [[INF] * (n + 1) for _ in range(n + 1)]
    for a, b, c in es:
        w[a][b] = w[b][a] = min(w[a][b], c)
    d = [row[:] for row in w]
    for i in range(n + 1):
        d[i][i] = 0
    best = INF
    for k in range(1, n + 1):
        wk = w[k]
        for i in range(1, k):
            if wk[i] == INF:
                continue
            di = d[i]
            for j in range(i + 1, k):
                if di[j] + wk[i] + wk[j] < best:
                    best = di[j] + wk[i] + wk[j]
        dk = d[k]
        for i in range(1, n + 1):
            di = d[i]; dik = di[k]
            if dik == INF:
                continue
            for j in range(1, n + 1):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return best if best < INF else -1


def _br(s):
    rd = Rd(s); n, m = rd.ints(2); _, es = _read_w(rd, n, m)
    best = INF
    for i, (a, b, c) in enumerate(es):
        adj = [[] for _ in range(n + 1)]
        for j, (x, y, z) in enumerate(es):
            if j != i:
                adj[x].append((y, z)); adj[y].append((x, z))
        best = min(best, dijkstra(adj, [a])[b] + c)
    return best if best < INF else -1


add(T, "Chu trình ngắn nhất", 4, """
Tìm chu trình (đơn, ít nhất 3 đỉnh) có tổng trọng số nhỏ nhất trong đồ thị vô hướng đơn. In `-1` nếu đồ thị không có chu trình.

Gợi ý: trong Floyd, ngay trước khi dùng `k` làm đỉnh trung gian, `d[i][j]` là đường đi ngắn nhất chỉ qua các đỉnh `< k`.
Chu trình có đỉnh lớn nhất là `k`: `d[i][j] + w(j, k) + w(k, i)` với `i, j < k`.
""", "Dòng đầu `n, m` (3 ≤ n ≤ 100). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^6).", "Độ dài chu trình ngắn nhất hoặc `-1`.",
    ["4 5\n1 2 1\n2 3 1\n3 4 1\n4 1 1\n1 3 5\n"], _g, _sol, brute=_br, tags=["Floyd", "chu trình"])


# 18 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj, _ = _read_w(rd, n, m, directed=False)
    d1 = [INF] * (n + 1); d2 = [INF] * (n + 1)
    d1[1] = 0; h = [(0, 1)]
    while h:
        du, u = heapq.heappop(h)
        if du > d2[u]:
            continue
        for v, w in adj[u]:
            nd = du + w
            if nd < d1[v]:
                d1[v], nd = nd, d1[v]
                heapq.heappush(h, (d1[v], v))
            if d1[v] < nd < d2[v]:
                d2[v] = nd; heapq.heappush(h, (nd, v))
    return d2[n] if d2[n] < INF else -1


add(T, "Đường đi ngắn nhì", 4, """
Đồ thị vô hướng có trọng số dương. Tìm độ dài đường đi từ 1 tới `n` **ngắn thứ hai**: nhỏ nhất trong các độ dài lớn hơn hẳn độ dài ngắn nhất
(đường đi được phép quay lại đỉnh/cạnh cũ). In `-1` nếu không có.

Gợi ý: Dijkstra lưu hai giá trị cho mỗi đỉnh: `d1` (ngắn nhất) và `d2` (ngắn nhì, lớn hơn hẳn `d1`).
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (1 ≤ w ≤ 10^9).", "Độ dài ngắn nhì hoặc `-1`.",
    ["4 4\n1 2 100\n2 4 200\n2 3 250\n3 4 100\n"], _gw(directed=False), _sol, tags=["Dijkstra"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rgraph(r, n, m, connected=r.random() < .7)
    return lines(J(n, len(es)), *(J(a, b, r.randint(1, 10**4), r.randint(1, 100)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b, c, p = rd.ints(4); adj[a].append((b, c, p)); adj[b].append((a, c, p))
    d = [INF] * (n + 1); d[1] = 0; h = [(0, 1)]
    while h:
        t, u = heapq.heappop(h)
        if t > d[u]:
            continue
        for v, c, p in adj[u]:
            dep = (t + p - 1) // p * p
            if dep + c < d[v]:
                d[v] = dep + c; heapq.heappush(h, (d[v], v))
    return d[n] if d[n] < INF else -1


add(T, "Tàu chạy theo lịch", 5, """
Mạng đường sắt có `m` tuyến hai chiều; tuyến `(u, v, c, p)` có tàu khởi hành từ mỗi đầu tại các thời điểm `0, p, 2p, ...` và chạy hết `c` phút.
Bạn ở ga 1 lúc thời điểm 0, có thể chờ ở ga bao lâu cũng được. Hỏi thời điểm sớm nhất tới ga `n` (`-1` nếu không thể).

Gợi ý: Dijkstra theo thời điểm tới. Từ ga `u` lúc `t`, chuyến kế tiếp khởi hành lúc `⌈t/p⌉·p`. Đến sớm không bao giờ thiệt
(tính chất FIFO) nên Dijkstra vẫn đúng.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 1 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v c p` (1 ≤ c ≤ 10^4, 1 ≤ p ≤ 100).",
    "Thời điểm sớm nhất hoặc `-1`.", ["3 3\n1 2 5 10\n2 3 3 7\n1 3 30 1\n"], _g, _sol, tags=["Dijkstra", "phụ thuộc thời gian"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 100)
    rows = [L(0 if i == j else r.randint(1, 10**5) for j in range(n)) for i in range(n)]
    order = list(range(1, n + 1)); r.shuffle(order)
    return lines(str(n), *rows, L(order))


def _sol(s):
    rd = Rd(s); n = rd.int(); d = [rd.ints(n) for _ in range(n)]; order = [x - 1 for x in rd.ints(n)]
    added = []; res = []
    for k in reversed(order):
        dk = d[k]
        for i in range(n):
            di = d[i]; dik = di[k]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
        added.append(k)
        res.append(sum(d[i][j] for i in added for j in added))
    return L(reversed(res))


def _br(s):
    rd = Rd(s); n = rd.int(); w = [rd.ints(n) for _ in range(n)]; order = [x - 1 for x in rd.ints(n)]
    res = []
    for t in range(n):
        alive = order[t:]
        d = {(i, j): w[i][j] for i in alive for j in alive}
        for k in alive:
            for i in alive:
                for j in alive:
                    d[i, j] = min(d[i, j], d[i, k] + d[k, j])
        res.append(sum(d.values()))
    return L(res)


add(T, "Xoá dần các đỉnh", 5, """
Đồ thị có hướng đầy đủ `n` đỉnh cho bởi ma trận trọng số. Lần lượt xoá các đỉnh `x_1, x_2, ..., x_n`. **Trước** mỗi lần xoá, hãy tính tổng
khoảng cách ngắn nhất giữa mọi cặp có thứ tự các đỉnh còn lại.

Gợi ý: đảo ngược quá trình — thêm đỉnh dần theo thứ tự `x_n, ..., x_1`. Mỗi lần thêm đỉnh `k`, chạy một vòng Floyd với `k` làm trung gian
(chính là vòng ngoài của Floyd!). Tổng `O(n³)`.
""", "Dòng đầu `n` (1 ≤ n ≤ 100). `n` dòng sau là ma trận trọng số (`a[i][i] = 0`, 1 ≤ a[i][j] ≤ 10^5). Dòng cuối là hoán vị `x_1..x_n`.",
    "Một dòng gồm `n` số.", ["2\n0 5\n4 0\n1 2\n"], _g, _sol, brute=lambda s: _br(s) if int(s.split()[0]) <= 25 else _sol(s), tags=["Floyd"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    base = _gw(directed=False, whi=10**6)(r, s)
    n = int(base.split()[0])
    return base + L(arr(r, n, 0, 10**6)) + "\n"


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); es = [rd.ints(3) for _ in range(m)]; c = [0] + rd.ints(n)
    adj = [[] for _ in range(n + 1)]
    for a, b, w in es:
        adj[a].append((b, w + c[b])); adj[b].append((a, w + c[a]))
    d = dijkstra(adj, [1])[n]
    return d + c[1] if d < INF else -1


add(T, "Phí qua trạm", 2, """
Đồ thị vô hướng: cạnh có độ dài `w`, và mỗi đỉnh `v` có phí qua trạm `c_v` (trả khi đi vào đỉnh, kể cả đỉnh 1 và đỉnh `n`).
Tìm tổng chi phí (độ dài + phí) nhỏ nhất để đi từ 1 tới `n` (`-1` nếu không thể).

Gợi ý: chuyển phí đỉnh vào cạnh: đi theo cạnh `u → v` tốn `w + c_v`; cộng thêm `c_1` ở cuối.
""", "Dòng đầu `n, m`. `m` dòng mỗi dòng `u v w` (1 ≤ w ≤ 10^6). Dòng cuối gồm `n` số `c_v` (0 ≤ c ≤ 10^6).", "Chi phí nhỏ nhất hoặc `-1`.",
    ["3 3\n1 2 1\n2 3 1\n1 3 5\n1 10 1\n"], _g, _sol, tags=["Dijkstra"])
