"""Chuyên đề 10: Duyệt đồ thị DFS/BFS, BFS 0-1."""
from collections import deque
from .base import add, Rd, S, J, L, arr, lines, rgraph, rdigraph

T = 10
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _read_graph(rd, n, m, directed=False):
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = rd.ints(2)
        adj[a].append(b)
        if not directed:
            adj[b].append(a)
    return adj


def _bfs(adj, src):
    n = len(adj) - 1
    d = [-1] * (n + 1); d[src] = 0; q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1; q.append(v)
    return d


def _ggraph(r, s, connected=None, dens=None):
    n = S(s, 2, 2 * 10**5)
    m = S(s, 1, 2 * 10**5)
    m = int(m * (dens if dens is not None else r.choice([.3, .6, 1.0])))
    if connected is None:
        connected = r.random() < .3
    es = rgraph(r, n, max(m, n - 1 if connected else 0), connected=connected)
    return n, es


def _grid(r, n, m, p, ch="#", base="."):
    return [[ch if r.random() < p else base for _ in range(m)] for _ in range(n)]


# 1 -----------------------------------------------------------------------
def _g_und(r, s):
    n, es = _ggraph(r, s)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _comps(adj):
    n = len(adj) - 1
    seen = [False] * (n + 1); c = 0
    for st in range(1, n + 1):
        if not seen[st]:
            c += 1; seen[st] = True; stack = [st]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True; stack.append(v)
    return c


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    return _comps(_read_graph(rd, n, m))


add(T, "Đếm thành phần liên thông", 1, """
Cho đồ thị vô hướng `n` đỉnh, `m` cạnh. Đếm số thành phần liên thông.

Gợi ý: với mỗi đỉnh chưa thăm, chạy DFS/BFS để đánh dấu cả thành phần của nó và tăng biến đếm.
Lưu đồ thị bằng danh sách kề `vector<int> adj[N]`.
""", "Dòng đầu `n, m` (1 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v` (một cạnh).", "Số thành phần liên thông.",
    ["5 3\n1 2\n2 3\n4 5\n"], _g_und, _sol, tags=["DFS", "liên thông"])


# 2 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 1000), S(s, 1, 1000)
    g = _grid(r, n, m, r.choice([.3, .45, .6]))
    return lines(J(n, m), *("".join(row) for row in g))


def _grid_comps(g, n, m, ch="."):
    seen = [[False] * m for _ in range(n)]
    sizes = []
    for i in range(n):
        for j in range(m):
            if g[i][j] == ch and not seen[i][j]:
                seen[i][j] = True; st = [(i, j)]; c = 0
                while st:
                    x, y = st.pop(); c += 1
                    for dx, dy in DIRS:
                        a, b = x + dx, y + dy
                        if 0 <= a < n and 0 <= b < m and not seen[a][b] and g[a][b] == ch:
                            seen[a][b] = True; st.append((a, b))
                sizes.append(c)
    return sizes


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    return len(_grid_comps(g, n, m))


add(T, "Đếm phòng", 1, """
Bản đồ toà nhà là lưới `n × m`, `.` là sàn và `#` là tường. Hai ô sàn chung cạnh thuộc cùng một phòng. Đếm số phòng.

Gợi ý: loang (flood fill) bằng DFS/BFS trên lưới với 4 hướng di chuyển.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 1000). `n` dòng sau mỗi dòng `m` ký tự.", "Số phòng.",
    ["5 8\n########\n#..#...#\n####.#.#\n#..#...#\n########\n"], _g, _sol, tags=["DFS", "lưới"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    return _bfs(_read_graph(rd, n, m), 1)[n]


add(T, "Đường đi ít cạnh nhất", 1, """
Cho đồ thị vô hướng. Tìm số cạnh ít nhất trên đường đi từ đỉnh `1` tới đỉnh `n`, hoặc `-1` nếu không có đường.

Gợi ý: BFS từ đỉnh 1 — BFS thăm các đỉnh theo thứ tự khoảng cách tăng dần nên `d[v] = d[u] + 1` là khoảng cách ngắn nhất.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng một cạnh `u v`.", "Số cạnh ít nhất hoặc `-1`.",
    ["5 5\n1 2\n1 3\n1 4\n2 3\n5 4\n"], _g_und, _sol, tags=["BFS"])


# 4 -----------------------------------------------------------------------
def _g(r, s):
    n, es = _ggraph(r, s)
    return lines(J(n, len(es), r.randint(1, n)), *(J(a, b) for a, b in rdigraph(r, n, len(es))))


def _sol(s):
    rd = Rd(s); n, m, src = rd.ints(3)
    return L(_bfs(_read_graph(rd, n, m, directed=True), src)[1:])


add(T, "Khoảng cách từ một đỉnh", 1, """
Cho đồ thị **có hướng** `n` đỉnh, `m` cung và đỉnh nguồn `s`. Với mỗi đỉnh `v`, in số cung ít nhất trên đường đi từ `s` tới `v`
(`-1` nếu không tới được).
""", "Dòng đầu `n, m, s` (1 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v` (cung từ `u` tới `v`).",
    "Một dòng gồm `n` số.", ["4 4 1\n1 2\n2 3\n3 1\n4 3\n"], _g, _sol, tags=["BFS"])


# 5 -----------------------------------------------------------------------
def _maze(r, s, need=("A", "B")):
    n, m = S(s, 2, 1000), S(s, 2, 1000)
    g = _grid(r, n, m, r.choice([.15, .3, .4]))
    cells = r.sample(range(n * m), len(need))
    for ch, c in zip(need, cells):
        g[c // m][c % m] = ch
    return n, m, g


def _g(r, s):
    n, m, g = _maze(r, s)
    return lines(J(n, m), *("".join(row) for row in g))


def _grid_bfs(g, n, m, sources, wall="#"):
    d = [[-1] * m for _ in range(n)]
    q = deque()
    for x, y in sources:
        d[x][y] = 0; q.append((x, y))
    while q:
        x, y = q.popleft(); nd = d[x][y] + 1
        for dx, dy in DIRS:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < m and d[a][b] < 0 and g[a][b] != wall:
                d[a][b] = nd; q.append((a, b))
    return d


def _find(g, ch):
    return [(i, j) for i, row in enumerate(g) for j, c in enumerate(row) if c == ch]


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    d = _grid_bfs(g, n, m, _find(g, "A"))
    (bx, by), = _find(g, "B")
    return d[bx][by]


add(T, "Mê cung", 2, """
Mê cung là lưới `n × m`: `.` là ô trống, `#` là tường, `A` là điểm xuất phát, `B` là đích. Mỗi bước đi sang ô chung cạnh.
Tìm số bước ít nhất từ `A` tới `B`, hoặc `-1` nếu không thể.

Gợi ý: BFS trên lưới, mỗi ô là một đỉnh.
""", "Dòng đầu `n, m` (2 ≤ n, m ≤ 1000). `n` dòng sau mô tả mê cung (đúng một `A` và một `B`).", "Số bước ít nhất hoặc `-1`.",
    ["5 8\n########\n#.A#...#\n#.##.#B#\n#......#\n########\n"], _g, _sol, tags=["BFS", "lưới"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5)
    m = S(s, 1, 2 * 10**5)
    if r.random() < .5:  # đồ thị hai phía thật sự
        side = [r.randint(0, 1) for _ in range(n + 1)]
        es, seen = [], set()
        for _ in range(m):
            a, b = r.randint(1, n), r.randint(1, n)
            if side[a] != side[b] and (min(a, b), max(a, b)) not in seen:
                seen.add((min(a, b), max(a, b))); es.append((a, b))
    else:
        es = rgraph(r, n, r.randint(0, m))
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj = _read_graph(rd, n, m)
    col = [-1] * (n + 1)
    for st in range(1, n + 1):
        if col[st] < 0:
            col[st] = 0; q = deque([st])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if col[v] < 0:
                        col[v] = col[u] ^ 1; q.append(v)
                    elif col[v] == col[u]:
                        return "NO"
    return "YES"


add(T, "Đồ thị hai phía", 2, """
Có thể chia các đỉnh của đồ thị vô hướng thành hai nhóm sao cho mọi cạnh nối hai đỉnh **khác nhóm** không?
(Ví dụ: chia học sinh thành hai đội sao cho hai bạn "là bạn bè" luôn ở hai đội khác nhau.)

Gợi ý: tô màu 0/1 bằng BFS/DFS: đỉnh kề phải khác màu. Gặp cạnh nối hai đỉnh cùng màu → không phải đồ thị hai phía.
""", "Dòng đầu `n, m` (1 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "`YES` hoặc `NO`.",
    ["4 4\n1 2\n2 3\n3 4\n4 1\n", "3 3\n1 2\n2 3\n3 1\n"], _g, _sol, tags=["BFS", "tô màu"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5)
    from .base import rtree
    es = rtree(r, n) if r.random() < .5 else rtree(r, n)[:r.randint(0, n - 1)]
    if r.random() < .5 and n >= 3:
        es = es + rgraph(r, n, r.randint(1, 3))
        # bỏ cạnh trùng
        seen, out = set(), []
        for a, b in es:
            k = (min(a, b), max(a, b))
            if k not in seen:
                seen.add(k); out.append((a, b))
        es = out
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    # đồ thị đơn vô hướng có chu trình ⇔ m > n - (số thành phần)
    return "YES" if m > n - _comps(_read_graph(rd, n, m)) else "NO"


add(T, "Phát hiện chu trình", 2, """
Đồ thị vô hướng đơn (không cạnh lặp, không khuyên) có chứa chu trình không?

Gợi ý: DFS; nếu gặp một đỉnh kề **đã thăm** mà không phải đỉnh cha → có chu trình.
(Cách khác: đồ thị không có chu trình ⇔ là một rừng ⇔ `m = n - số thành phần`.)
""", "Dòng đầu `n, m` (1 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "`YES` hoặc `NO`.",
    ["4 3\n1 2\n2 3\n3 1\n", "3 2\n1 2\n2 3\n"], _g, _sol, tags=["DFS", "chu trình"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 1000), S(s, 1, 1000)
    g = _grid(r, n, m, r.choice([.4, .55, .7]), ch="0", base="1")
    return lines(J(n, m), *("".join(row) for row in g))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    return max(_grid_comps(g, n, m, "1") + [0])


add(T, "Hòn đảo lớn nhất", 2, """
Bản đồ `n × m` gồm `1` (đất) và `0` (nước). Một hòn đảo là nhóm ô đất liên thông theo 4 hướng. Tìm diện tích (số ô) của đảo lớn nhất
(in 0 nếu không có đất).
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 1000). `n` dòng sau mỗi dòng là xâu `m` ký tự 0/1.", "Diện tích lớn nhất.",
    ["3 4\n1100\n0101\n0111\n"], _g, _sol, tags=["DFS", "lưới"])


# 9 -----------------------------------------------------------------------
add(T, "Xây thêm đường", 2, """
Có `n` thành phố và `m` con đường hai chiều. Cần xây thêm ít nhất bao nhiêu con đường để mọi cặp thành phố đều đi được tới nhau?

Gợi ý: đáp án = số thành phần liên thông − 1 (nối các thành phần thành một chuỗi).
""", "Dòng đầu `n, m` (1 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các con đường.", "Số đường cần xây thêm.",
    ["4 2\n1 2\n3 4\n"], lambda r, s: (lambda n, es: lines(J(n, len(es)), *(J(a, b) for a, b in es)))(*_ggraph(r, s, dens=r.choice([.2, .5]))),
    lambda s: (lambda rd: (lambda n, m: _comps(_read_graph(rd, n, m)) - 1)(*rd.ints(2)))(Rd(s)), tags=["DFS", "liên thông"])


# 10 ----------------------------------------------------------------------
def _sol(s):
    n, x1, y1, x2, y2 = map(int, s.split())
    d = [[-1] * (n + 1) for _ in range(n + 1)]
    d[x1][y1] = 0; q = deque([(x1, y1)])
    while q:
        x, y = q.popleft()
        if (x, y) == (x2, y2):
            return d[x][y]
        for dx, dy in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)):
            a, b = x + dx, y + dy
            if 1 <= a <= n and 1 <= b <= n and d[a][b] < 0:
                d[a][b] = d[x][y] + 1; q.append((a, b))
    return -1


add(T, "Quân mã", 3, """
Trên bàn cờ `n × n`, quân mã đứng ở ô `(x1, y1)`. Mỗi nước đi theo hình chữ L (2 ô theo một hướng và 1 ô theo hướng vuông góc).
Cần ít nhất bao nhiêu nước để tới ô `(x2, y2)`? In `-1` nếu không thể.
""", "Một dòng `n x1 y1 x2 y2` (1 ≤ n ≤ 1000, 1 ≤ toạ độ ≤ n).", "Số nước ít nhất hoặc `-1`.",
    ["8 1 1 8 8\n", "2 1 1 2 2\n"],
    lambda r, s: (lambda n: J(n, r.randint(1, n), r.randint(1, n), r.randint(1, n), r.randint(1, n)))(S(s, 1, 1000)),
    _sol, tags=["BFS"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 2, 1000), S(s, 2, 1000)
    g = _grid(r, n, m, r.choice([.1, .25, .35]))
    for _ in range(r.randint(0, 3)):
        g[r.randrange(n)][r.randrange(m)] = "F"
    g[r.randrange(n)][r.randrange(m)] = "A"
    return lines(J(n, m), *("".join(row) for row in g))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    fire = _grid_bfs(g, n, m, _find(g, "F"))
    (ax, ay), = _find(g, "A")
    d = [[-1] * m for _ in range(n)]
    d[ax][ay] = 0; q = deque([(ax, ay)])
    while q:
        x, y = q.popleft()
        if x in (0, n - 1) or y in (0, m - 1):
            return d[x][y]
        for dx, dy in DIRS:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < m and d[a][b] < 0 and g[a][b] == ".":
                t = d[x][y] + 1
                if fire[a][b] < 0 or fire[a][b] > t:
                    d[a][b] = t; q.append((a, b))
    return -1


add(T, "Thoát khỏi đám cháy", 3, """
Toà nhà là lưới `n × m`: `.` trống, `#` tường, `F` là ô đang cháy, `A` là vị trí của bạn. Mỗi phút bạn đi sang một ô trống kề cạnh,
đồng thời lửa lan từ mọi ô cháy sang mọi ô trống kề cạnh. Bạn chỉ được bước vào ô mà lửa tới **muộn hơn** thời điểm bạn tới.
Bạn thoát được khi đứng ở một ô biên của lưới. Tìm số phút ít nhất để thoát, hoặc `-1`.

Gợi ý: BFS đa nguồn từ mọi ô `F` để biết thời điểm lửa tới mỗi ô; rồi BFS từ `A` chỉ đi vào ô có `thời gian lửa > thời gian của mình`.
""", "Dòng đầu `n, m` (2 ≤ n, m ≤ 1000). `n` dòng mô tả lưới (đúng một `A`).", "Số phút ít nhất hoặc `-1`.",
    ["5 8\n########\n#..A...#\n#.F##..#\n#.#....#\n#####.##\n"], _g, _sol, tags=["BFS đa nguồn", "lưới"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 1000), S(s, 1, 1000)
    g = _grid(r, n, m, r.choice([.001, .05, .3]), ch="1", base="0")
    g[r.randrange(n)][r.randrange(m)] = "1"
    return lines(J(n, m), *("".join(row) for row in g))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    d = _grid_bfs(g, n, m, _find(g, "1"), wall=None)
    return [L(row) for row in d]


add(T, "Khoảng cách tới ô 1 gần nhất", 2, """
Cho lưới nhị phân `n × m` (có ít nhất một ô `1`). Với mỗi ô, tính khoảng cách (số bước đi 4 hướng) tới ô `1` gần nhất.

Gợi ý: BFS **đa nguồn** — đưa tất cả ô `1` vào hàng đợi với khoảng cách 0 ngay từ đầu. Chạy BFS riêng từng ô sẽ quá chậm.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 1000). `n` dòng sau mỗi dòng xâu `m` ký tự 0/1.", "`n` dòng, mỗi dòng `m` số.",
    ["3 3\n000\n010\n000\n"], _g, _sol, tags=["BFS đa nguồn"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 2 * 10**5); m = S(s, 1, 2 * 10**5)
    es = rdigraph(r, n, m)
    return lines(J(n, len(es)), *(J(a, b, r.randint(0, 1)) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b, w = rd.ints(3); adj[a].append((b, w))
    INF = 10**9
    d = [INF] * (n + 1); d[1] = 0; q = deque([1])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                (q.appendleft if w == 0 else q.append)(v)
    return L(x if x < INF else -1 for x in d[1:])


add(T, "BFS 0-1", 3, """
Đồ thị **có hướng**, mỗi cung có trọng số 0 hoặc 1. Tính khoảng cách ngắn nhất từ đỉnh 1 tới mọi đỉnh (`-1` nếu không tới được).

Gợi ý (BFS 0-1): dùng `deque`; khi nới lỏng qua cung trọng số 0 thì đẩy đỉnh vào **đầu** deque, trọng số 1 thì đẩy vào **cuối**.
Độ phức tạp `O(n + m)`, nhanh hơn Dijkstra.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v w` (w ∈ {0, 1}).",
    "Một dòng gồm `n` số.", ["4 4\n1 2 1\n1 3 0\n3 2 0\n2 4 1\n"], _g, _sol, tags=["BFS 0-1"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 2, 10**5); m = S(s, 1, 2 * 10**5)
    es = rdigraph(r, n, m)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2)
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = rd.ints(2); adj[a].append((b, 0)); adj[b].append((a, 1))
    INF = 10**9
    d = [INF] * (n + 1); d[1] = 0; q = deque([1])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                (q.appendleft if w == 0 else q.append)(v)
    return d[n] if d[n] < INF else -1


add(T, "Đảo chiều ít cung nhất", 3, """
Cho đồ thị có hướng. Cần đảo chiều ít nhất bao nhiêu cung để có đường đi từ đỉnh `1` tới đỉnh `n`? In `-1` nếu không thể.

Gợi ý: với mỗi cung `u → v`, thêm cạnh `u → v` trọng số 0 và cạnh `v → u` trọng số 1 (đảo chiều tốn 1). Chạy BFS 0-1.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau mỗi dòng `u v`.", "Số cung ít nhất cần đảo hoặc `-1`.",
    ["7 7\n1 2\n3 2\n3 4\n7 4\n6 2\n5 6\n7 5\n"], _g, _sol, tags=["BFS 0-1"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    g = _grid(r, n, m, r.choice([.2, .4, .6]))
    g[0][0] = g[n - 1][m - 1] = "."
    return lines(J(n, m), *("".join(row) for row in g))


def _zero_one_grid(n, m, cost):
    INF = 10**9
    d = [[INF] * m for _ in range(n)]
    d[0][0] = 0; q = deque([(0, 0)])
    while q:
        x, y = q.popleft(); dx0 = d[x][y]
        for k, (dx, dy) in enumerate(DIRS):
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < m:
                w = cost(x, y, a, b, k)
                if dx0 + w < d[a][b]:
                    d[a][b] = dx0 + w
                    (q.appendleft if w == 0 else q.append)((a, b))
    return d[n - 1][m - 1]


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    return _zero_one_grid(n, m, lambda x, y, a, b, k: 1 if g[a][b] == "#" else 0)


add(T, "Phá tường", 3, """
Lưới `n × m` có tường `#`. Bạn đi từ ô `(1, 1)` tới ô `(n, m)` (hai ô này trống), mỗi bước sang ô kề cạnh; khi bước vào ô tường
bạn phải phá nó (tốn 1 búa). Cần ít nhất bao nhiêu búa?

Gợi ý: bước vào ô trống tốn 0, ô tường tốn 1 → BFS 0-1 trên lưới.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 500). `n` dòng mô tả lưới.", "Số búa ít nhất.",
    ["3 4\n.#..\n.##.\n##..\n"], _g, _sol, tags=["BFS 0-1", "lưới"])


# 16 ----------------------------------------------------------------------
ARROW = {"v": 0, "^": 1, ">": 2, "<": 3}


def _g(r, s):
    n, m = S(s, 1, 500), S(s, 1, 500)
    return lines(J(n, m), *("".join(r.choice("v^><") for _ in range(m)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    return _zero_one_grid(n, m, lambda x, y, a, b, k: 0 if ARROW[g[x][y]] == k else 1)


add(T, "Lưới mũi tên", 3, """
Mỗi ô của lưới `n × m` có một mũi tên: `>` phải, `<` trái, `v` xuống, `^` lên. Từ một ô, đi theo hướng mũi tên **miễn phí**;
đi theo hướng khác tốn chi phí 1 (coi như đổi mũi tên). Không được ra ngoài lưới. Tìm chi phí nhỏ nhất từ `(1, 1)` tới `(n, m)`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 500). `n` dòng sau mỗi dòng `m` ký tự trong `><v^`.", "Chi phí nhỏ nhất.",
    ["3 3\n>>v\n^<v\nv<<\n"], _g, _sol, tags=["BFS 0-1", "lưới"])


# 17 ----------------------------------------------------------------------
def _sol(s):
    a, b = map(int, s.split())
    LIM = 2 * max(a, b) + 2
    d = [-1] * (LIM + 1); d[a] = 0; q = deque([a])
    while q:
        x = q.popleft()
        if x == b:
            return d[x]
        for y in (x * 2, x - 1):
            if 1 <= y <= LIM and d[y] < 0:
                d[y] = d[x] + 1; q.append(y)
    return -1


add(T, "Máy tính hỏng", 2, """
Máy tính chỉ còn hai nút: **nhân đôi** số đang hiển thị, và **trừ 1**. Màn hình đang hiện `a`. Cần ít nhất bao nhiêu lần bấm để màn hình hiện `b`?

Gợi ý: BFS trên các số nguyên — mỗi số là một đỉnh, mỗi nút bấm là một cạnh. Không cần đi quá `2·max(a, b)`.
""", "Một dòng `a, b` (1 ≤ a, b ≤ 10^6).", "Số lần bấm ít nhất.", ["4 6\n", "10 1\n"],
    lambda r, s: J(r.randint(1, S(s, 5, 10**6)), r.randint(1, S(s, 5, 10**6))), _sol, tags=["BFS"])


# 18 ----------------------------------------------------------------------
def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); adj = _read_graph(rd, n, m)
    MOD = 10**9 + 7
    d = [-1] * (n + 1); c = [0] * (n + 1); d[1] = 0; c[1] = 1; q = deque([1])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1; c[v] = c[u]; q.append(v)
            elif d[v] == d[u] + 1:
                c[v] = (c[v] + c[u]) % MOD
    return c[n]


def _g(r, s):
    n, es = _ggraph(r, s, connected=r.random() < .7)
    return lines(J(n, len(es)), *(J(a, b) for a, b in es))


add(T, "Đếm đường đi ngắn nhất", 3, """
Đồ thị vô hướng không trọng số. Đếm số đường đi **ngắn nhất** (ít cạnh nhất) từ đỉnh `1` tới đỉnh `n`, modulo `10^9 + 7`
(in 0 nếu không có đường đi).

Gợi ý: trong lúc BFS, `cnt[v] += cnt[u]` mỗi khi `d[v] = d[u] + 1`.
""", "Dòng đầu `n, m` (2 ≤ n ≤ 2·10^5, 0 ≤ m ≤ 2·10^5). `m` dòng sau là các cạnh.", "Số đường đi modulo 10^9+7.",
    ["4 4\n1 2\n1 3\n2 4\n3 4\n"], _g, _sol, tags=["BFS", "đếm"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 2, 50), S(s, 2, 50)
    g = _grid(r, n, m, r.choice([.2, .3]))
    k = r.randint(0, 6)
    special = ["S", "T"] + [chr(97 + i) for i in range(k)] + [chr(65 + i) for i in range(k)]
    cells = r.sample(range(n * m), min(len(special), n * m))
    for ch, c in zip(special, cells):
        g[c // m][c % m] = ch
    if "T" not in "".join("".join(row) for row in g):
        g[0][0], g[n - 1][m - 1] = "S", "T"
    return lines(J(n, m), *("".join(row) for row in g))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    (sx, sy), = _find(g, "S")
    seen = {(sx, sy, 0)}; q = deque([(sx, sy, 0, 0)])
    while q:
        x, y, keys, d = q.popleft()
        if g[x][y] == "T":
            return d
        for dx, dy in DIRS:
            a, b = x + dx, y + dy
            if not (0 <= a < n and 0 <= b < m):
                continue
            c = g[a][b]
            if c == "#":
                continue
            if "A" <= c <= "F" and not keys >> (ord(c) - 65) & 1:
                continue
            nk = keys | (1 << (ord(c) - 97)) if "a" <= c <= "f" else keys
            if (a, b, nk) not in seen:
                seen.add((a, b, nk)); q.append((a, b, nk, d + 1))
    return -1


add(T, "Mê cung có chìa khoá", 4, """
Mê cung `n × m`: `.` trống, `#` tường, `S` xuất phát, `T` đích; chữ thường `a..f` là chìa khoá, chữ hoa `A..F` là cửa tương ứng.
Đi vào ô có chìa thì nhặt chìa (giữ mãi). Chỉ đi qua cửa `X` khi đã có chìa `x`. Tìm số bước ít nhất từ `S` tới `T`, hoặc `-1`.

Gợi ý: BFS trên trạng thái `(ô, tập chìa khoá đang có)` — tập chìa khoá biểu diễn bằng bitmask 6 bit.
""", "Dòng đầu `n, m` (2 ≤ n, m ≤ 50). `n` dòng mô tả mê cung (đúng một `S`, một `T`, mỗi chìa/cửa xuất hiện tối đa một lần).",
    "Số bước ít nhất hoặc `-1`.", ["3 5\nS.A.T\n.###.\n...a#\n"], _g, _sol, tags=["BFS", "bitmask"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 2, 100), S(s, 2, 100)
    g = _grid(r, n, m, r.choice([.1, .2, .3]))
    k = r.randint(0, S(s, 1, 10))
    cells = r.sample(range(n * m), min(k + 1, n * m))
    for i, c in enumerate(cells):
        g[c // m][c % m] = "S" if i == 0 else "*"
    return lines(J(n, m), *("".join(row) for row in g))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); g = rd.strs(n)
    pts = _find(g, "S") + _find(g, "*")
    k = len(pts)
    dist = []
    for p in pts:
        d = _grid_bfs(g, n, m, [p])
        dist.append([d[x][y] for x, y in pts])
    if any(v < 0 for v in dist[0]):
        return -1
    INF = 10**9
    dp = [[INF] * k for _ in range(1 << k)]
    dp[1][0] = 0
    for mask in range(1 << k):
        for u in range(k):
            cur = dp[mask][u]
            if cur == INF:
                continue
            for v in range(k):
                if not mask >> v & 1:
                    nm = mask | 1 << v
                    if cur + dist[u][v] < dp[nm][v]:
                        dp[nm][v] = cur + dist[u][v]
    return min(dp[-1])


add(T, "Thu thập kho báu", 5, """
Lưới `n × m` có tường `#`, điểm xuất phát `S` và tối đa 10 kho báu `*`. Tìm số bước ít nhất để đi từ `S` và **thu thập hết** kho báu
(không cần quay lại). In `-1` nếu có kho báu không tới được.

Gợi ý: BFS từ `S` và từ mỗi kho báu để có ma trận khoảng cách giữa các điểm quan trọng; sau đó QHĐ bitmask
`dp[mask][u]` như bài người du lịch.
""", "Dòng đầu `n, m` (2 ≤ n, m ≤ 100). `n` dòng mô tả lưới (đúng một `S`, 0..10 ô `*`).", "Số bước ít nhất hoặc `-1`.",
    ["3 5\nS...*\n.###.\n*....\n"], _g, _sol, tags=["BFS", "QHĐ bitmask"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    k = S(s, 0, 500)
    dead = {f"{r.randrange(10000):04d}" for _ in range(k)}
    target = f"{r.randrange(10000):04d}"
    dead.discard(target)
    return lines(target, str(len(dead)), *sorted(dead))


def _sol(s):
    t = s.split()
    target, k = t[0], int(t[1]); dead = set(t[2:2 + k])
    if "0000" in dead:
        return -1
    d = {"0000": 0}; q = deque(["0000"])
    while q:
        u = q.popleft()
        if u == target:
            return d[u]
        for i in range(4):
            for delta in (1, 9):
                v = u[:i] + str((int(u[i]) + delta) % 10) + u[i + 1:]
                if v not in d and v not in dead:
                    d[v] = d[u] + 1; q.append(v)
    return -1


add(T, "Khoá số", 3, """
Ổ khoá có 4 vòng số, mỗi vòng từ 0 đến 9 (quay vòng: 9 → 0 và 0 → 9). Ban đầu khoá ở `0000`. Mỗi bước quay một vòng lên hoặc xuống 1 đơn vị.
Có một danh sách mã "chết": nếu khoá rơi vào mã chết thì bị kẹt. Tìm số bước ít nhất để mở khoá ở mã `target`, hoặc `-1`.

Gợi ý: BFS trên 10^4 trạng thái, mỗi trạng thái có 8 trạng thái kề.
""", "Dòng đầu là `target`. Dòng hai là `k` (0 ≤ k ≤ 500). `k` dòng sau là các mã chết (khác `target`).", "Số bước ít nhất hoặc `-1`.",
    ["0202\n5\n0201\n0101\n0102\n1212\n2002\n"], _g, _sol, tags=["BFS"])
