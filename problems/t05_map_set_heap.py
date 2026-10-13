"""Chuyên đề 5: Cấu trúc dữ liệu map, set, heap (priority_queue)."""
import heapq
from bisect import bisect_left, bisect_right, insort
from collections import Counter, defaultdict, deque
from .base import add, Rd, S, J, L, arr, lines, rstr, SortedList

T = 5


# 1 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, r.choice([5, n, 10**9]))))


add(T, "Đếm giá trị phân biệt", 1, """
Cho dãy `n` số. Có bao nhiêu giá trị khác nhau?

Gợi ý: đưa tất cả vào `set<int>` rồi in `size()`; hoặc sắp xếp rồi đếm.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số giá trị phân biệt.",
    ["5\n2 3 2 2 3\n"], _g, lambda s: len(set(s.split()[1:])), tags=["set"])


# 2 -----------------------------------------------------------------------
def _sol(s):
    c = Counter(map(int, s.split()[1:]))
    return [J(k, c[k]) for k in sorted(c)]


add(T, "Bảng tần suất", 1, """
Cho dãy `n` số. Với mỗi giá trị xuất hiện trong dãy, in giá trị đó và số lần xuất hiện, theo thứ tự giá trị tăng dần.

Gợi ý: `map<int,int> cnt; cnt[x]++;` — duyệt `map` sẽ ra thứ tự khoá tăng dần.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (|a_i| ≤ 10^9).", "Mỗi dòng gồm giá trị và số lần xuất hiện.",
    ["6\n5 -1 5 3 3 5\n"],
    lambda r, s: (lambda n: lines(str(n), L(arr(r, n, -r.choice([3, 1000, 10**9]), 10**9 if r.random() < .3 else 1000))))(S(s, 1, 2 * 10**5)),
    _sol, tags=["map"])


# 3 -----------------------------------------------------------------------
def _sol(s):
    c = Counter(map(int, s.split()[1:]))
    m = max(c.values())
    return min(k for k, v in c.items() if v == m)


add(T, "Phần tử phổ biến nhất", 1, """
Tìm giá trị xuất hiện nhiều lần nhất trong dãy. Nếu có nhiều giá trị cùng số lần xuất hiện lớn nhất, in giá trị nhỏ nhất.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Giá trị cần tìm.",
    ["7\n4 1 4 2 1 9 9\n"], _g, _sol, tags=["map"])


# 4 -----------------------------------------------------------------------
def _sol(s):
    seen, out = set(), []
    for x in s.split()[1:]:
        out.append("YES" if x in seen else "NO")
        seen.add(x)
    return out


add(T, "Đã gặp chưa?", 1, """
Duyệt dãy từ trái sang phải. Với mỗi phần tử, in `YES` nếu giá trị này đã xuất hiện ở trước nó, ngược lại in `NO`.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "`n` dòng `YES`/`NO`.",
    ["5\n1 2 1 3 2\n"], _g, _sol, tags=["set"])


# 5 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 2 * 10**5)
    hi = S(s, 10, 10**9)
    ops, live = [], []
    for _ in range(q):
        t = r.random()
        if t < .45 or not live:
            x = r.randint(1, hi); ops.append(J(1, x)); live.append(x)
        elif t < .6:
            x = r.choice(live) if r.random() < .8 else r.randint(1, hi); ops.append(J(2, x))
        else:
            ops.append(J(3, r.randint(1, hi)))
    return lines(str(q), *ops)


def _sol(s):
    rd = Rd(s); q = rd.int()
    st, out = SortedList(), []
    present = set()
    for _ in range(q):
        t, x = rd.ints(2)
        if t == 1:
            if x not in present:
                present.add(x); st.add(x)
        elif t == 2:
            if x in present:
                present.discard(x); st.remove(x)
        else:
            i = st.bisect_left(x)
            out.append(st[i] if i < len(st) else -1)
    return out


add(T, "Tập hợp và lower_bound", 2, """
Ban đầu tập `S` rỗng. Thực hiện `q` thao tác:
- `1 x`: thêm `x` vào `S` (nếu đã có thì bỏ qua);
- `2 x`: xoá `x` khỏi `S` (nếu không có thì bỏ qua);
- `3 x`: in phần tử **nhỏ nhất** trong `S` mà `≥ x`, hoặc `-1` nếu không có.

Gợi ý: `set<int>` và `S.lower_bound(x)`.
""", "Dòng đầu `q` (1 ≤ q ≤ 2·10^5). `q` dòng sau mỗi dòng một thao tác (1 ≤ x ≤ 10^9).",
    "Với mỗi thao tác loại 3 in kết quả trên một dòng.", ["6\n1 5\n1 2\n3 3\n2 5\n3 3\n3 1\n"], _g, _sol, tags=["set"])


# 6 -----------------------------------------------------------------------
def _g(r, s):
    q = S(s, 1, 2 * 10**5)
    ops, size = [], 0
    for _ in range(q):
        t = r.random()
        if t < .5 or size == 0:
            ops.append(J(1, r.randint(1, 10**9))); size += 1
        elif t < .75:
            ops.append("2"); size -= 1
        else:
            ops.append("3")
    return lines(str(q), *ops)


def _sol(s):
    rd = Rd(s); q = rd.int(); h, out = [], []
    for _ in range(q):
        t = rd.int()
        if t == 1:
            heapq.heappush(h, -rd.int())
        elif t == 2:
            heapq.heappop(h)
        else:
            out.append(-h[0])
    return out


add(T, "Hàng đợi ưu tiên", 2, """
Thực hiện `q` thao tác trên một hàng đợi ưu tiên (ban đầu rỗng):
- `1 x`: thêm `x`;
- `2`: xoá phần tử lớn nhất (đảm bảo hàng đợi khác rỗng);
- `3`: in phần tử lớn nhất (đảm bảo hàng đợi khác rỗng).

Gợi ý: `priority_queue<int>` trong C++ mặc định là max-heap.
""", "Dòng đầu `q` (1 ≤ q ≤ 2·10^5). `q` dòng sau mỗi dòng một thao tác.", "Kết quả các thao tác loại 3.",
    ["5\n1 3\n1 7\n3\n2\n3\n"], _g, _sol, tags=["heap"])


# 7 -----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    hi = S(s, 10, 10**9)
    return lines(J(n, m), L(arr(r, n, 1, hi)), L(arr(r, m, 1, hi)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); h = sorted(rd.ints(n)); t = rd.ints(m)
    # DSU "nhảy sang trái" để xoá phần tử trong O(α)
    par = list(range(n + 1))  # chỉ số i+1 đại diện vé h[i]; 0 = không còn

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    out = []
    for x in t:
        i = find(bisect_right(h, x))
        if i == 0:
            out.append(-1)
        else:
            out.append(h[i - 1]); par[i] = i - 1
    return out


add(T, "Bán vé xem ca nhạc", 2, """
Có `n` vé với giá `h_1..h_n`, và `m` khách hàng lần lượt đến. Khách thứ `i` sẵn sàng trả tối đa `t_i`; họ sẽ mua vé
**đắt nhất** có giá không vượt quá `t_i` (mỗi vé chỉ bán một lần). In giá vé mỗi khách mua, hoặc `-1` nếu không mua được.

Gợi ý: `multiset<int>`; tìm `upper_bound(t)` rồi lùi lại một phần tử.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). Dòng hai là giá vé, dòng ba là `t_i` (1 ≤ giá trị ≤ 10^9).",
    "`m` dòng là giá vé mỗi khách mua.", ["5 3\n5 3 7 8 5\n4 8 3\n"], _g, _sol, tags=["multiset"])


# 8 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, S(s, 10, 10**9))))


def _sol(s):
    h = list(map(int, s.split()[1:])); heapq.heapify(h); cost = 0
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h)
        cost += a + b; heapq.heappush(h, a + b)
    return cost


add(T, "Nối dây", 2, """
Có `n` sợi dây độ dài `a_i`. Mỗi lần nối hai sợi độ dài `x` và `y` tốn chi phí `x + y` và được một sợi độ dài `x + y`.
Tìm tổng chi phí nhỏ nhất để nối tất cả thành một sợi.

Gợi ý (tham lam kiểu Huffman): luôn nối hai sợi ngắn nhất — dùng min-heap.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Chi phí nhỏ nhất.",
    ["4\n4 3 2 6\n"], _g, _sol, tags=["heap", "tham lam"])


# 9 -----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, min(n, r.choice([1, 3, 100, n])))), L(arr(r, n, 1, 10**9)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); h, out = [], []
    for x in rd.ints(n):
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
        out.append(h[0] if len(h) == k else -1)
    return L(out)


add(T, "Phần tử lớn thứ k trong luồng", 2, """
Các số lần lượt đến. Sau mỗi số, in ra số **lớn thứ k** trong các số đã đến (tính cả lặp), hoặc `-1` nếu chưa đủ `k` số.

Gợi ý: giữ min-heap kích thước `k` chứa `k` số lớn nhất; đỉnh heap chính là đáp án.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["5 2\n3 1 5 4 2\n"], _g, _sol, tags=["heap"])


# 10 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = S(s, 10, 10**9)
    out = []
    for _ in range(n):
        a = r.randint(1, hi); out.append(J(a, min(hi, a + r.randint(0, hi // r.choice([2, 10, 1000]) + 1))))
    return lines(str(n), *out)


def _sol(s):
    rd = Rd(s); n = rd.int()
    ev = sorted(rd.ints(2) for _ in range(n))
    h, best = [], 0
    for a, b in ev:
        if h and h[0] < a:
            heapq.heapreplace(h, b)
        else:
            heapq.heappush(h, b)
        best = max(best, len(h))
    return best


add(T, "Số phòng khách sạn tối thiểu", 3, """
Có `n` khách, khách `i` ở từ ngày `a_i` đến hết ngày `b_i`. Hai khách có thể dùng chung phòng nếu thời gian ở không giao nhau
(khách sau đến **sau** ngày khách trước rời đi). Tìm số phòng tối thiểu.

Gợi ý: sắp xếp theo ngày đến; min-heap lưu ngày rời đi của các phòng đang dùng.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `a b` (1 ≤ a ≤ b ≤ 10^9).", "Số phòng tối thiểu.",
    ["3\n1 2\n2 4\n4 4\n"], _g, _sol, tags=["heap", "sắp xếp"])


# 11 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, 10**9)))


def _sol(s):
    lo, hi, out = [], [], []  # lo: max-heap (đảo dấu), hi: min-heap
    for x in map(int, s.split()[1:]):
        if not lo or x <= -lo[0]:
            heapq.heappush(lo, -x)
        else:
            heapq.heappush(hi, x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        out.append(-lo[0])
    return L(out)


def _br(s):
    a, out = [], []
    for x in map(int, s.split()[1:]):
        insort(a, x); out.append(a[(len(a) - 1) // 2])
    return L(out)


add(T, "Trung vị động", 3, """
Các số lần lượt đến. Sau mỗi số, in trung vị của các số đã có: nếu đang có `m` số đã sắp xếp `b_1 ≤ ... ≤ b_m`
thì trung vị là `b_{⌊(m+1)/2⌋}`.

Gợi ý: hai heap — max-heap chứa nửa nhỏ, min-heap chứa nửa lớn, luôn giữ kích thước chênh nhau không quá 1.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n` số.",
    ["5\n5 15 1 3 8\n"], _g, _sol, brute=_br, tags=["heap"])


# 12 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n)), L(arr(r, n, 1, r.choice([3, 50, 10**9]))))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    c = defaultdict(int); out = []
    for i, x in enumerate(a):
        c[x] += 1
        if i >= k:
            y = a[i - k]; c[y] -= 1
            if c[y] == 0:
                del c[y]
        if i >= k - 1:
            out.append(len(c))
    return L(out)


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return L(len(set(a[i:i + k])) for i in range(n - k + 1))


add(T, "Số giá trị phân biệt trong mỗi cửa sổ", 3, """
Với mỗi đoạn con liên tiếp độ dài `k` (từ trái sang phải), in số giá trị khác nhau trong đoạn đó.

Gợi ý: `map` đếm tần suất; khi trượt cửa sổ thêm phần tử mới và bớt phần tử cũ, xoá khoá khi tần suất về 0.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n - k + 1` số.",
    ["5 3\n1 2 1 3 3\n"], _g, _sol, brute=_br, tags=["map", "cửa sổ trượt"])


# 13 ----------------------------------------------------------------------
def _g(r, s):
    x = S(s, 10, 10**9)
    n = min(x - 1, S(s, 1, 2 * 10**5))
    return lines(J(x, n), L(r.sample(range(1, x), n)))


def _sol(s):
    rd = Rd(s); x, n = rd.ints(2); p = rd.ints(n)
    # xử lý ngược: xoá đèn khỏi tập đầy đủ, theo dõi khoảng lớn nhất (danh sách liên kết)
    pos = sorted(set(p) | {0, x})
    idx = {v: i for i, v in enumerate(pos)}
    prv = list(range(-1, len(pos) - 1)); nxt = list(range(1, len(pos) + 1))
    best = max(pos[i + 1] - pos[i] for i in range(len(pos) - 1))
    out = [best]
    for v in reversed(p[1:]):
        i = idx[v]; a, b = prv[i], nxt[i]
        nxt[a] = b; prv[b] = a
        best = max(best, pos[b] - pos[a])
        out.append(best)
    return L(reversed(out))


def _br(s):
    rd = Rd(s); x, n = rd.ints(2); p = rd.ints(n)
    cur, out = [0, x], []
    for v in p:
        insort(cur, v)
        out.append(max(cur[i + 1] - cur[i] for i in range(len(cur) - 1)))
    return L(out)


add(T, "Đèn giao thông", 3, """
Một con phố có toạ độ từ `0` đến `x`. Lần lượt có `n` đèn giao thông được lắp tại các vị trí phân biệt `p_i`.
Sau mỗi lần lắp, in độ dài đoạn phố dài nhất không có đèn (giữa hai đèn liên tiếp hoặc đèn và đầu phố).

Gợi ý: `set` lưu vị trí đèn, `multiset` lưu độ dài các khoảng. Lắp đèn tại `p` tách khoảng `[a, b]` thành `[a, p]` và `[p, b]`.
""", "Dòng đầu `x, n` (1 ≤ x ≤ 10^9, 1 ≤ n ≤ 2·10^5, n < x). Dòng sau `n` vị trí phân biệt (0 < p_i < x).",
    "Một dòng gồm `n` số.", ["8 3\n3 6 2\n"], _g, _sol, brute=_br, tags=["set", "multiset"])


# 14 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), *(J(r.randint(1, max(1, n // r.choice([1, 3, 20]))), r.randint(1, 10**9)) for _ in range(n)))


def _sol(s):
    rd = Rd(s); n = rd.int()
    jobs = sorted(rd.ints(2) for _ in range(n))
    h = []
    for d, p in jobs:
        heapq.heappush(h, p)
        if len(h) > d:
            heapq.heappop(h)
    return sum(h)


def _br(s):
    rd = Rd(s); n = rd.int()
    jobs = [rd.ints(2) for _ in range(n)]
    best = 0
    for mask in range(1 << n):
        ch = sorted(jobs[i][0] for i in range(n) if mask >> i & 1)
        if all(d >= i + 1 for i, d in enumerate(ch)):
            best = max(best, sum(jobs[i][1] for i in range(n) if mask >> i & 1))
    return best


add(T, "Lập lịch có hạn chót", 4, """
Có `n` công việc, mỗi việc làm trong đúng 1 đơn vị thời gian, việc `i` phải **hoàn thành trước hoặc đúng** thời điểm `d_i`
(bắt đầu từ thời điểm 0) và mang lại lợi nhuận `p_i`. Mỗi thời điểm chỉ làm một việc. Tìm tổng lợi nhuận lớn nhất.

Gợi ý: xét các việc theo hạn chót tăng dần, giữ min-heap các việc đã chọn; nếu số việc vượt quá hạn chót hiện tại,
bỏ việc có lợi nhuận nhỏ nhất.
""", "Dòng đầu `n` (1 ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `d_i p_i` (1 ≤ d_i ≤ 2·10^5, 1 ≤ p_i ≤ 10^9).",
    "Lợi nhuận lớn nhất.", ["4\n2 50\n1 10\n2 20\n1 30\n"], _g, _sol,
    brute=lambda s: _br(s) if int(s.split()[0]) <= 12 else _sol(s), tags=["heap", "tham lam"])


# 15 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 10**5)
    al = "abcde"[:r.choice([2, 3, 5])]
    return lines(str(n), *(rstr(r, r.randint(1, max(1, min(10, 200000 // n))), al) for _ in range(n)))


def _sol(s):
    c = Counter("".join(sorted(w)) for w in s.split()[1:])
    return sum(v * (v - 1) // 2 for v in c.values())


add(T, "Cặp từ đảo chữ", 3, """
Cho `n` từ. Hai từ là **đảo chữ** (anagram) của nhau nếu sắp xếp lại các chữ cái của từ này được từ kia
(ví dụ `listen` và `silent`). Đếm số cặp `i < j` mà từ `i` và từ `j` là đảo chữ của nhau.

Gợi ý: chuẩn hoá mỗi từ bằng cách sắp xếp các ký tự, dùng `map<string,int>` để đếm.
""", "Dòng đầu `n` (1 ≤ n ≤ 10^5). `n` dòng sau mỗi dòng một từ (tổng độ dài ≤ 2·10^5).", "Số cặp.",
    ["4\nabc\nbca\ncab\nab\n"], _g, _sol, tags=["map", "xâu"])


# 16 ----------------------------------------------------------------------
class _LazyHeap:
    def __init__(self, sign):
        self.h, self.dead, self.sz, self.sg = [], defaultdict(int), 0, sign

    def push(self, x):
        heapq.heappush(self.h, self.sg * x); self.sz += 1

    def _clean(self):
        while self.h and self.dead[self.h[0]]:
            self.dead[self.h[0]] -= 1; heapq.heappop(self.h)

    def top(self):
        self._clean(); return self.sg * self.h[0]

    def pop(self):
        self._clean(); self.sz -= 1; return self.sg * heapq.heappop(self.h)

    def remove(self, x):
        self.dead[self.sg * x] += 1; self.sz -= 1


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    lo, hi = _LazyHeap(-1), _LazyHeap(1)
    out = []

    def balance():
        while lo.sz > hi.sz + 1:
            hi.push(lo.pop())
        while hi.sz > lo.sz:
            lo.push(hi.pop())
    for i, x in enumerate(a):
        if lo.sz and x <= lo.top():
            lo.push(x)
        else:
            hi.push(x)
        balance()
        if i >= k:
            y = a[i - k]
            if y <= lo.top():
                lo.remove(y)
            else:
                hi.remove(y)
            balance()
        if i >= k - 1:
            out.append(lo.top())
    return L(out)


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return L(sorted(a[i:i + k])[(k - 1) // 2] for i in range(n - k + 1))


add(T, "Trung vị cửa sổ trượt", 4, """
Với mỗi đoạn con độ dài `k` (từ trái sang phải), in trung vị của đoạn: phần tử thứ `⌊(k+1)/2⌋` sau khi sắp xếp.

Gợi ý: hai `multiset` (nửa nhỏ / nửa lớn) có cân bằng kích thước; khi trượt cửa sổ thì xoá phần tử cũ khỏi tập chứa nó.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Một dòng gồm `n - k + 1` số.",
    ["8 3\n2 4 3 5 8 1 2 1\n"],
    lambda r, s: (lambda n: lines(J(n, r.randint(1, n)), L(arr(r, n, 1, r.choice([5, 10**9])))))(S(s, 1, 2 * 10**5)),
    _sol, brute=_br, tags=["multiset", "heap", "cửa sổ trượt"])


# 17 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = r.choice([10, 1000, 10**9])
    return lines(J(n, r.randint(0, hi // r.choice([1, 5, 50]))), L(arr(r, n, 1, hi)))


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    mx, mn = deque(), deque()
    l = tot = 0
    for r_, x in enumerate(a):
        while mx and a[mx[-1]] <= x:
            mx.pop()
        mx.append(r_)
        while mn and a[mn[-1]] >= x:
            mn.pop()
        mn.append(r_)
        while a[mx[0]] - a[mn[0]] > k:
            l += 1
            if mx[0] < l:
                mx.popleft()
            if mn[0] < l:
                mn.popleft()
        tot += r_ - l + 1
    return tot


def _br(s):
    rd = Rd(s); n, k = rd.ints(2); a = rd.ints(n)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if max(a[i:j]) - min(a[i:j]) <= k)


add(T, "Đoạn ổn định", 4, """
Đếm số đoạn con liên tiếp mà hiệu giữa phần tử lớn nhất và nhỏ nhất trong đoạn không vượt quá `k`.

Gợi ý: hai con trỏ + `multiset` để biết max/min của cửa sổ hiện tại (`*s.begin()`, `*s.rbegin()`).
""", "Dòng đầu `n, k` (1 ≤ n ≤ 2·10^5, 0 ≤ k ≤ 10^9). Dòng sau `n` số (1 ≤ a_i ≤ 10^9).", "Số đoạn.",
    ["5 2\n1 3 2 5 4\n"], _g, _sol, brute=_br, tags=["multiset", "hai con trỏ"])


# 18 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    return lines(J(n, r.randint(1, n), r.randint(0, 10**4)),
                 L(arr(r, n, 0, r.choice([10**4, 10**6]))), L(arr(r, n, 1, 10**4)))


def _sol(s):
    rd = Rd(s); n, k, w = rd.ints(3); c = rd.ints(n); p = rd.ints(n)
    pr = sorted(zip(c, p)); h = []; i = 0
    for _ in range(k):
        while i < n and pr[i][0] <= w:
            heapq.heappush(h, -pr[i][1]); i += 1
        if not h:
            break
        w -= heapq.heappop(h)
    return w


add(T, "Gọi vốn đầu tư", 4, """
Bạn có vốn ban đầu `W` và được làm **tối đa** `k` dự án (mỗi dự án tối đa một lần). Dự án `i` cần vốn tối thiểu `c_i`
để bắt đầu (vốn không bị trừ đi) và khi xong vốn tăng thêm `p_i`. Tìm vốn lớn nhất sau khi kết thúc.

Gợi ý: mỗi bước, đưa mọi dự án có `c_i ≤ vốn hiện tại` vào max-heap theo `p_i`, rồi chọn dự án lời nhất.
""", "Dòng đầu `n, k, W` (1 ≤ k ≤ n ≤ 2·10^5, 0 ≤ W ≤ 10^4). Dòng hai là `c_i` (0 ≤ c_i ≤ 10^6), dòng ba là `p_i` (1 ≤ p_i ≤ 10^4).",
    "Vốn cuối cùng.", ["3 2 0\n0 1 1\n1 2 3\n"], _g, _sol, tags=["heap", "tham lam"])


# 19 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 10**5), S(s, 1, 10**5)
    k = r.randint(1, min(n * m, 10**5))
    return lines(J(n, m, k), L(sorted(arr(r, n, 1, 10**9))), L(sorted(arr(r, m, 1, 10**9))))


def _sol(s):
    rd = Rd(s); n, m, k = rd.ints(3); a = rd.ints(n); b = rd.ints(m)
    h = [(a[i] + b[0], i, 0) for i in range(min(n, k))]
    heapq.heapify(h); out = []
    while len(out) < k:
        v, i, j = heapq.heappop(h)
        out.append(v)
        if j + 1 < m:
            heapq.heappush(h, (a[i] + b[j + 1], i, j + 1))
    return L(out)


def _br(s):
    rd = Rd(s); n, m, k = rd.ints(3); a = rd.ints(n); b = rd.ints(m)
    return L(sorted(x + y for x in a for y in b)[:k])


add(T, "k tổng nhỏ nhất", 4, """
Cho hai dãy không giảm `a` (độ dài `n`) và `b` (độ dài `m`). In `k` giá trị nhỏ nhất trong `n·m` tổng `a_i + b_j`
theo thứ tự không giảm.

Gợi ý: min-heap khởi tạo các cặp `(i, 0)`; mỗi lần lấy cặp `(i, j)` nhỏ nhất thì đẩy cặp `(i, j+1)` vào.
""", "Dòng đầu `n, m, k` (1 ≤ n, m ≤ 10^5, 1 ≤ k ≤ min(n·m, 10^5)). Hai dòng sau là hai dãy không giảm (1 ≤ giá trị ≤ 10^9).",
    "Một dòng gồm `k` số.", ["3 3 4\n1 7 11\n2 4 6\n"], _g, _sol, brute=_br, tags=["heap"])


# 20 ----------------------------------------------------------------------
def _g(r, s):
    n, k = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    k = r.randint(1, max(1, k // r.choice([1, 10, 1000])))
    t, cur = [], 0
    for _ in range(n):
        cur += r.randint(0, 3); t.append(cur)
    return lines(J(k, n), *(J(t[i], r.randint(1, 10)) for i in range(n)))


def _sol(s):
    rd = Rd(s); k, n = rd.ints(2)
    free = list(range(1, k + 1)); busy = []; out = []
    for _ in range(n):
        t, d = rd.ints(2)
        while busy and busy[0][0] <= t:
            _, sv = heapq.heappop(busy); heapq.heappush(free, sv)
        if free:
            sv = heapq.heappop(free); start = t
        else:
            start, sv = heapq.heappop(busy)
        heapq.heappush(busy, (start + d, sv))
        out.append(sv)
    return L(out)


add(T, "Phân phối máy chủ", 4, """
Có `k` máy chủ đánh số `1..k` và `n` yêu cầu đến theo thời gian không giảm; yêu cầu `i` đến lúc `t_i` và cần `d_i` đơn vị thời gian.
Quy tắc phân phối:
- Nếu có máy rảnh tại thời điểm `t_i` (máy rảnh đúng lúc `t_i` cũng tính), giao cho máy rảnh có **số hiệu nhỏ nhất**.
- Nếu không, yêu cầu phải chờ máy **sớm rảnh nhất** (nếu nhiều máy cùng rảnh sớm nhất thì chọn số hiệu nhỏ nhất), và bắt đầu ngay khi máy đó rảnh.

In số hiệu máy xử lý mỗi yêu cầu.

Gợi ý: hai heap — heap máy rảnh (theo số hiệu), heap máy bận (theo thời điểm rảnh, rồi số hiệu).
""", "Dòng đầu `k, n` (1 ≤ k, n ≤ 2·10^5). `n` dòng sau mỗi dòng `t_i d_i` (t không giảm, 0 ≤ t_i ≤ 10^9, 1 ≤ d_i ≤ 10).",
    "Một dòng gồm `n` số.", ["2 4\n0 5\n1 2\n2 1\n3 1\n"], _g, _sol, tags=["heap", "mô phỏng"])


# 21 ----------------------------------------------------------------------
def _g(r, s):
    n = S(s, 1, 2 * 10**5)
    hi = S(s, 10, 10**9)
    out = []
    for _ in range(n):
        a = r.randint(1, hi - 1); out.append(J(a, min(hi, a + r.randint(1, max(1, hi // r.choice([3, 30, 3000]))))))
    return lines(J(n, r.randint(1, max(1, n // r.choice([1, 5, 100])))), *out)


def _sol(s):
    rd = Rd(s); n, k = rd.ints(2)
    mv = sorted((rd.ints(2) for _ in range(n)), key=lambda x: (x[1], x[0]))
    ends = SortedList()  # thời điểm rảnh của những người đã xem ít nhất một phim
    cnt = 0
    for a, b in mv:
        i = ends.bisect_right(a) - 1
        if i >= 0:
            ends.pop(i); ends.add(b); cnt += 1
        elif len(ends) < k:
            ends.add(b); cnt += 1
    return cnt


add(T, "Liên hoan phim", 5, """
Có `n` bộ phim, phim `i` chiếu từ thời điểm `a_i` đến `b_i`. Nhóm có `k` người, mỗi người xem trọn vẹn một số phim
không giao nhau (phim tiếp theo có thể bắt đầu đúng lúc phim trước kết thúc). Mỗi phim chỉ cần tối đa một người xem.
Tổng số phim nhóm xem được nhiều nhất là bao nhiêu?

Gợi ý: xét phim theo thời điểm kết thúc tăng dần; `multiset` lưu thời điểm rảnh của từng người. Với phim `[a, b]`,
giao cho người có thời điểm rảnh **lớn nhất mà ≤ a**; nếu không có ai và vẫn còn người chưa xem phim nào thì giao cho người mới.
""", "Dòng đầu `n, k` (1 ≤ k ≤ n ≤ 2·10^5). `n` dòng sau mỗi dòng `a b` (1 ≤ a < b ≤ 10^9).", "Số phim tối đa.",
    ["5 2\n1 5\n8 10\n3 6\n2 5\n6 9\n"], _g, _sol, tags=["multiset", "tham lam"], tl=1500)


# 22 ----------------------------------------------------------------------
def _g(r, s):
    n, m = S(s, 1, 2 * 10**5), S(s, 1, 2 * 10**5)
    hi = r.choice([20, 1000, 10**9])
    return lines(J(n, m), L(arr(r, n, 1, hi)), L(arr(r, m, 1, hi)))


def _sol(s):
    rd = Rd(s); n, m = rd.ints(2); a = set(rd.ints(n)); b = set(rd.ints(m))
    c = sorted(a & b)
    return L(c) if c else "-1"


add(T, "Phần tử chung", 1, """
Cho hai dãy số. In các giá trị xuất hiện ở **cả hai** dãy theo thứ tự tăng dần, mỗi giá trị một lần. Nếu không có in `-1`.
""", "Dòng đầu `n, m` (1 ≤ n, m ≤ 2·10^5). Hai dòng sau là hai dãy (1 ≤ giá trị ≤ 10^9).", "Một dòng kết quả.",
    ["5 4\n1 2 2 3 9\n2 9 9 7\n"], _g, _sol, tags=["set"])
