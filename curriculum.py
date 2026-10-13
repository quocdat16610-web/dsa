"""Lộ trình 20 chuyên đề: mục tiêu, giáo án từng buổi, video, liên kết luyện tập thêm.

Phần lý thuyết chi tiết nằm ở content/NN.md (Markdown).
"""
import os
from urllib.parse import quote_plus

from problems import PROBLEMS

ROOT = os.path.dirname(os.path.abspath(__file__))
CAT_COLOR = {"Cơ bản": "#38bdf8", "Thuật toán": "#a78bfa", "CTDL": "#4ade80", "Đồ thị": "#facc15"}


def yt(q):
    return "https://www.youtube.com/results?search_query=" + quote_plus(q)


def cses(i, name):
    return {"name": f"CSES {i} — {name}", "url": f"https://cses.fi/problemset/task/{i}"}


# Kênh tiếng Việt và kênh Ấn Độ (tiếng Anh/Hindi) dạy CTDL & giải thuật nổi tiếng.
VN = ["28tech", "VNOI", "Big-O Coding"]


def vids(vn_q, in_items):
    out = [{"title": f"{ch}: {vn_q}", "url": yt(f"{ch} {vn_q}"), "lang": "vi", "author": ch} for ch in VN]
    out += [{"title": f"{author}: {q}", "url": yt(f"{author} {q}"), "lang": "en/hi", "author": author}
            for author, q in in_items]
    return out


T = [
    dict(id=1, cat="Cơ bản", name="Sàng nguyên tố & Số học", short="Sàng nguyên tố\nCác bài toán số học", viz="sieve",
         goals=["Kiểm tra số nguyên tố O(√n), phân tích thừa số nguyên tố",
                "Cài đặt sàng Eratosthenes, sàng ước nguyên tố nhỏ nhất (SPF), sàng đoạn",
                "UCLN/BCNN, luỹ thừa nhanh, nghịch đảo modulo, tổ hợp C(n, k) mod p",
                "Làm quen hàm phi Euler, bao hàm - loại trừ"],
         b1=["Số nguyên tố, kiểm tra O(√n)", "Sàng Eratosthenes và độ phức tạp O(n log log n)", "Đếm/ liệt kê ước, phân tích thừa số"],
         b2=["Luỹ thừa nhanh & nghịch đảo modulo (Fermat nhỏ)", "Sàng SPF, sàng phi, sàng đoạn", "Tổ hợp modulo & bao hàm - loại trừ"],
         videos=vids("sàng nguyên tố Eratosthenes", [("take U forward", "sieve of eratosthenes"),
                                                     ("Luv", "sieve of eratosthenes competitive programming"),
                                                     ("CodeNCode", "number theory sieve"), ("Kunal Kushwaha", "maths for DSA")]),
         practice=[cses(1713, "Counting Divisors"), cses(1081, "Common Divisors"), cses(1095, "Exponentiation"),
                   cses(1712, "Exponentiation II")]),
    dict(id=2, cat="Cơ bản", name="Tổng tiền tố", short="Tổng tiền tố", viz="prefix",
         goals=["Trả lời truy vấn tổng đoạn O(1) bằng mảng cộng dồn", "Mảng hiệu: cập nhật đoạn O(1)",
                "Tiền tố 2D và mảng hiệu 2D", "Kết hợp tiền tố với map để đếm đoạn con"],
         b1=["Mảng cộng dồn 1D, công thức p[r] - p[l-1]", "Mảng hiệu (difference array)", "Tiền tố XOR, đếm theo tiền tố"],
         b2=["Tiền tố 2D, mảng hiệu 2D", "Đếm đoạn con có tổng k / chia hết cho k bằng map", "Kỹ thuật đóng góp"],
         videos=vids("mảng cộng dồn prefix sum", [("Luv", "prefix sum"), ("take U forward", "prefix sum subarray sum equals k"),
                                                  ("Aditya Verma", "prefix sum"), ("CodeNCode", "prefix sum 2D")]),
         practice=[cses(1646, "Static Range Sum Queries"), cses(1652, "Forest Queries"), cses(1661, "Subarray Sums II"),
                   cses(1662, "Subarray Divisibility")]),
    dict(id=3, cat="Thuật toán", name="Tìm kiếm nhị phân", short="Tìm kiếm nhị phân", viz="bsearch",
         goals=["Tìm kiếm nhị phân trên mảng đã sắp xếp, lower_bound/upper_bound",
                "Chặt nhị phân đáp án với hàm kiểm tra đơn điệu", "Tìm kiếm nhị phân trên số thực",
                "Tránh lặp vô hạn & tràn số"],
         b1=["Tư duy 'đơn điệu' và bất biến [lo, hi]", "lower_bound / upper_bound", "Căn bậc hai nguyên, tìm vị trí"],
         b2=["Chặt nhị phân đáp án (min-max, max-min)", "Tìm kiếm nhị phân số thực", "Đếm phần tử nhỏ thứ k"],
         videos=vids("tìm kiếm nhị phân", [("take U forward", "binary search playlist"), ("Aditya Verma", "binary search"),
                                           ("Luv", "binary search"), ("Kunal Kushwaha", "binary search")]),
         practice=[cses(1620, "Factory Machines"), cses(1085, "Array Division"),
                   {"name": "Codeforces EDU — Binary Search", "url": "https://codeforces.com/edu/course/2/lesson/6"}]),
    dict(id=4, cat="Thuật toán", name="Hai con trỏ", short="Hai con trỏ", viz="twopointers",
         goals=["Nhận diện bài dùng hai con trỏ (cửa sổ trượt)", "Đếm đoạn con thoả điều kiện đơn điệu",
                "Trộn dãy, tìm cặp/bộ ba có tổng cho trước", "Kỹ thuật 'đúng k' = 'không quá k' − 'không quá k-1'"],
         b1=["Hai con trỏ ngược chiều trên dãy đã sắp xếp", "Hai con trỏ cùng chiều (cửa sổ trượt)", "Trộn hai dãy"],
         b2=["Đếm đoạn con thoả mãn", "Cửa sổ với đếm tần suất", "Kỹ thuật atMost(k) − atMost(k−1)"],
         videos=vids("hai con trỏ two pointers", [("take U forward", "two pointers sliding window"),
                                                  ("Aditya Verma", "sliding window"), ("Luv", "two pointers")]),
         practice=[cses(1640, "Sum of Two Values"), cses(1641, "Sum of Three Values"), cses(1141, "Playlist"),
                   {"name": "Codeforces EDU — Two Pointers", "url": "https://codeforces.com/edu/course/2/lesson/9"}]),
    dict(id=5, cat="CTDL", name="Map - Set - Heap", short="Map-Set-Heap", viz="heap",
         goals=["Sử dụng thành thạo map, set, multiset, unordered_map", "priority_queue (min/max heap)",
                "Bài toán tham lam dùng heap", "Duy trì trung vị, phần tử lớn thứ k"],
         b1=["map/set: thao tác & độ phức tạp O(log n)", "multiset và lower_bound/upper_bound", "Đếm tần suất"],
         b2=["Heap: cấu trúc cây nhị phân, push/pop", "Tham lam với heap (nối dây, lập lịch)", "Hai heap — trung vị động"],
         videos=vids("map set priority queue C++", [("Luv", "STL C++ map set"), ("Aditya Verma", "heap playlist"),
                                                    ("Abdul Bari", "heap sort heapify"), ("take U forward", "priority queue")]),
         practice=[cses(1621, "Distinct Numbers"), cses(1091, "Concert Tickets"), cses(1163, "Traffic Lights"),
                   cses(1164, "Room Allocation"), cses(1076, "Sliding Median")]),
    dict(id=6, cat="Cơ bản", name="Đệ quy - Quay lui, Bitwise", short="Đệ quy - Quay lui\nBitwise", viz="nqueens",
         goals=["Viết hàm đệ quy có điểm dừng", "Quay lui sinh hoán vị, tổ hợp, tập con", "Nhánh cận cắt tỉa",
                "Thao tác bit: AND, OR, XOR, dịch bit, bitmask duyệt tập con"],
         b1=["Đệ quy & ngăn xếp lời gọi", "Sinh xâu nhị phân, hoán vị, tổ hợp", "Bài toán N quân hậu"],
         b2=["Toán tử bit và mẹo thường dùng", "Duyệt tập con bằng bitmask", "Meet in the middle"],
         videos=vids("đệ quy quay lui", [("take U forward", "recursion playlist"), ("Aditya Verma", "recursion playlist"),
                                         ("Luv", "bit manipulation"), ("Kunal Kushwaha", "backtracking")]),
         practice=[cses(1622, "Creating Strings"), cses(1623, "Apple Division"), cses(1624, "Chessboard and Queens"),
                   cses(2205, "Gray Code"), cses(1628, "Meet in the Middle")]),
    dict(id=7, cat="Thuật toán", name="Đệ quy có nhớ, Quy hoạch động", short="Đệ quy có nhớ\nQuy hoạch động", viz="dpcoins",
         goals=["Từ đệ quy → đệ quy có nhớ → QHĐ từ dưới lên", "Xác định trạng thái, công thức truy hồi, cơ sở",
                "QHĐ trên lưới, trên đoạn, bitmask, trên cây (giới thiệu)"],
         b1=["Fibonacci: vì sao đệ quy thường chậm?", "Memoization vs tabulation", "Ếch nhảy, đổi tiền"],
         b2=["QHĐ trên lưới", "QHĐ đoạn (nhân dãy ma trận)", "QHĐ bitmask, QHĐ trên cây"],
         videos=vids("quy hoạch động", [("Aditya Verma", "dynamic programming playlist"), ("take U forward", "DP series"),
                                        ("Luv", "dynamic programming"), ("Abdul Bari", "dynamic programming")]),
         practice=[cses(1633, "Dice Combinations"), cses(1634, "Minimizing Coins"), cses(1637, "Removing Digits"),
                   cses(1638, "Grid Paths"), cses(1744, "Rectangle Cutting"), cses(1653, "Elevator Rides")]),
    dict(id=8, cat="Thuật toán", name="QHĐ Đếm", short="QHĐ Đếm", viz="dpgrid",
         goals=["Đếm số cách bằng QHĐ (cộng theo modulo)", "Tránh đếm trùng: thứ tự vòng lặp, trạng thái",
                "QHĐ chữ số (digit DP)", "Kết hợp tổ hợp (giai thừa, nghịch đảo)"],
         b1=["Nguyên lý cộng, nhân; modulo", "Đếm đường đi, lát gạch", "Phân hoạch số"],
         b2=["QHĐ chữ số", "Tối ưu bằng tổng tiền tố", "Đếm với automaton (KMP)"],
         videos=vids("quy hoạch động đếm", [("take U forward", "DP on grids count paths"), ("Luv", "digit dp"),
                                            ("CodeNCode", "digit DP"), ("Aditya Verma", "count subsets DP")]),
         practice=[cses(1093, "Two Sets II"), cses(1746, "Array Description"), cses(2413, "Counting Towers"),
                   cses(2220, "Counting Numbers")]),
    dict(id=9, cat="Thuật toán", name="QHĐ Knapsack, LIS/LCS", short="QHĐ Knapsack\nQHĐ LIS/LCS", viz="lcs",
         goals=["Cái túi 0/1, không giới hạn, giới hạn số lượng, theo nhóm", "LIS O(n²) và O(n log n)",
                "LCS, khoảng cách chỉnh sửa", "Biến đổi bài toán về LIS/LCS"],
         b1=["Cái túi 0/1 & thứ tự duyệt", "Cái túi không giới hạn, đổi vai trò giá trị-khối lượng", "Tách nhị phân"],
         b2=["LIS O(n log n)", "LCS & edit distance", "Bài toán biến thể (LCIS, phong bì)"],
         videos=vids("bài toán cái túi LIS LCS", [("Aditya Verma", "knapsack LCS playlist"), ("take U forward", "LIS LCS DP"),
                                                  ("Abdul Bari", "0/1 knapsack"), ("Luv", "LIS binary search")]),
         practice=[cses(1158, "Book Shop"), cses(1145, "Increasing Subsequence"), cses(1639, "Edit Distance"),
                   cses(1140, "Projects")]),
    dict(id=10, cat="Đồ thị", name="DFS/BFS, BFS 0-1", short="DFS/BFS\nBFS 0-1", viz="bfs",
         goals=["Biểu diễn đồ thị: danh sách kề", "DFS, BFS và ứng dụng: liên thông, đường đi ngắn nhất không trọng số",
                "BFS trên lưới, BFS đa nguồn, BFS trạng thái", "BFS 0-1 với deque"],
         b1=["Danh sách kề, ma trận kề", "DFS: thành phần liên thông, chu trình", "BFS: khoảng cách ngắn nhất"],
         b2=["BFS trên lưới & đa nguồn", "BFS trên không gian trạng thái (bitmask)", "BFS 0-1"],
         videos=vids("DFS BFS đồ thị", [("take U forward", "graph series BFS DFS"), ("Abdul Bari", "BFS DFS"),
                                        ("CodeNCode", "0-1 BFS"), ("Luv", "graph BFS")]),
         practice=[cses(1192, "Counting Rooms"), cses(1193, "Labyrinth"), cses(1666, "Building Roads"),
                   cses(1667, "Message Route"), cses(1668, "Building Teams"), cses(1669, "Round Trip")]),
    dict(id=11, cat="Đồ thị", name="Cây DFS, Khớp - Cầu", short="Cây DFS\nKhớp Cầu", viz="bridges",
         goals=["Cây DFS: tin/tout, cạnh cây – cạnh ngược", "Thuật toán Tarjan tìm cầu, đỉnh khớp",
                "Các bài toán trên cây: đường kính, kích thước cây con, đổi gốc"],
         b1=["Cây DFS, tin/tout, kiểm tra tổ tiên", "Đường kính cây, cây con", "Đổi gốc (rerooting)"],
         b2=["low-link và cầu", "Đỉnh khớp", "Nén thành phần song liên thông cạnh"],
         videos=vids("cầu khớp Tarjan", [("take U forward", "bridges in graph tarjan"), ("take U forward", "articulation point"),
                                         ("CodeNCode", "bridges articulation points"), ("Luv", "tree diameter")]),
         practice=[cses(1674, "Subordinates"), cses(1131, "Tree Diameter"), cses(1132, "Tree Distances I"),
                   cses(1133, "Tree Distances II"), cses(2076, "Necessary Roads"), cses(2077, "Necessary Cities")]),
    dict(id=12, cat="Đồ thị", name="TPLT mạnh, DAG - DP on DAG", short="Thành phần liên thông mạnh\nDAG - DP on DAG", viz="topo",
         goals=["Sắp xếp topo (Kahn, DFS)", "Tìm TPLT mạnh (Tarjan, Kosaraju), đồ thị nén",
                "QHĐ trên DAG: đường đi dài nhất, đếm đường đi", "2-SAT"],
         b1=["DAG và sắp xếp topo", "QHĐ trên DAG", "Trò chơi trên DAG"],
         b2=["Kosaraju / Tarjan", "Đồ thị nén", "2-SAT"],
         videos=vids("sắp xếp topo thành phần liên thông mạnh", [("take U forward", "topological sort kosaraju"),
                                                                 ("Abdul Bari", "strongly connected components"),
                                                                 ("CodeNCode", "2 SAT"), ("Luv", "topological sort")]),
         practice=[cses(1679, "Course Schedule"), cses(1680, "Longest Flight Route"), cses(1681, "Game Routes"),
                   cses(1682, "Flight Routes Check"), cses(1683, "Planets and Kingdoms"), cses(1686, "Coin Collector"),
                   cses(1684, "Giant Pizza")]),
    dict(id=13, cat="Đồ thị", name="Đường đi ngắn nhất", short="Đường đi ngắn nhất", viz="dijkstra",
         goals=["Dijkstra với heap", "Bellman-Ford, phát hiện chu trình âm", "Floyd-Warshall",
                "Đồ thị trạng thái / phân tầng, đếm đường đi ngắn nhất"],
         b1=["Dijkstra & chứng minh tham lam", "Dijkstra đa nguồn, trên lưới", "Đồ thị trạng thái"],
         b2=["Bellman-Ford & chu trình âm", "Floyd-Warshall và biến thể", "Đồ thị đường đi ngắn nhất"],
         videos=vids("thuật toán Dijkstra", [("Abdul Bari", "dijkstra algorithm"), ("take U forward", "dijkstra bellman ford floyd"),
                                             ("Luv", "dijkstra"), ("CodeNCode", "floyd warshall")]),
         practice=[cses(1671, "Shortest Routes I"), cses(1672, "Shortest Routes II"), cses(1195, "Flight Discount"),
                   cses(1197, "Cycle Finding"), cses(1673, "High Score"), cses(1196, "Flight Routes"), cses(1202, "Investigation")]),
    dict(id=14, cat="CTDL", name="Max, Min trên đoạn tịnh tiến", short="Max, Min trên đoạn\ntịnh tiến", viz="deque",
         goals=["Deque đơn điệu: min/max cửa sổ trượt O(n)", "Ngăn xếp đơn điệu: phần tử lớn/nhỏ hơn gần nhất",
                "Kỹ thuật đóng góp", "Tối ưu QHĐ bằng deque"],
         b1=["Ngăn xếp đơn điệu", "Phần tử lớn hơn tiếp theo, hình chữ nhật lớn nhất", "Kỹ thuật đóng góp"],
         b2=["Deque đơn điệu", "Max/min cửa sổ 1D, 2D", "Tối ưu QHĐ với deque"],
         videos=vids("deque cửa sổ trượt max min", [("take U forward", "sliding window maximum"),
                                                    ("Aditya Verma", "sliding window maximum"),
                                                    ("take U forward", "monotonic stack"), ("Aditya Verma", "stack playlist")]),
         practice=[cses(1645, "Nearest Smaller Values"), cses(1644, "Maximum Subarray Sum II"), cses(1142, "Advertisement")]),
    dict(id=15, cat="CTDL", name="Sparse table", short="Sparse table", viz="sparse",
         goals=["Xây bảng thưa O(n log n), truy vấn O(1) cho phép toán luỹ đẳng", "RMQ, GCD, OR/AND trên đoạn",
                "Nhảy nhị phân trên mảng / đồ thị hàm"],
         b1=["Ý tưởng chia đoạn luỹ thừa 2", "RMQ O(1)", "Phép toán luỹ đẳng"],
         b2=["Kết hợp tìm kiếm nhị phân", "Nhảy nhị phân (binary lifting)", "Bảng thưa 2D"],
         videos=vids("sparse table", [("CodeNCode", "sparse table"), ("Luv", "sparse table RMQ"),
                                      ("take U forward", "binary lifting"), ("Kartik Arora", "sparse table")]),
         practice=[cses(1647, "Static Range Minimum Queries"), cses(1750, "Planets Queries I")]),
    dict(id=16, cat="CTDL", name="Segment Tree/BIT, Sweep Line", short="Segment Tree/BIT\nSweep Line", viz="segtree",
         goals=["Cây Fenwick (BIT): cập nhật điểm, tổng tiền tố", "Cây phân đoạn: truy vấn đoạn, đi xuống trên cây",
                "Lan truyền lười (lazy propagation)", "Đường quét + cấu trúc dữ liệu, xử lý offline"],
         b1=["BIT & đếm nghịch thế", "Segment tree cơ bản", "Đi xuống trên cây, phần tử thứ k"],
         b2=["Lazy propagation", "Đường quét (sweep line)", "Offline + nén số"],
         videos=vids("segment tree cây phân đoạn", [("Luv", "segment tree"), ("take U forward", "segment tree"),
                                                    ("CodeNCode", "fenwick tree lazy propagation"), ("Kartik Arora", "sweep line")]),
         practice=[cses(1648, "Dynamic Range Sum Queries"), cses(1649, "Dynamic Range Minimum Queries"), cses(1143, "Hotel Queries"),
                   cses(1749, "List Removals"), cses(1144, "Salary Queries"), cses(1735, "Range Updates and Sums"),
                   cses(1736, "Polynomial Queries"), cses(1734, "Distinct Values Queries"),
                   {"name": "Codeforces EDU — Segment Tree", "url": "https://codeforces.com/edu/course/2/lesson/4"}]),
    dict(id=17, cat="CTDL", name="DSU, Cây khung nhỏ nhất", short="DSU\nCây khung nhỏ nhất", viz="kruskal",
         goals=["DSU với nén đường đi và hợp theo kích thước", "Kruskal, Prim", "DSU có trọng số / parity",
                "Xử lý offline đảo ngược thời gian"],
         b1=["DSU: find/union", "Kruskal", "Prim trên đồ thị dày"],
         b2=["DSU trọng số, DSU parity", "Offline & đảo ngược", "Biến thể MST"],
         videos=vids("DSU cây khung nhỏ nhất Kruskal", [("take U forward", "disjoint set union"), ("Abdul Bari", "kruskal prim"),
                                                        ("Luv", "DSU"), ("CodeNCode", "DSU")]),
         practice=[cses(1675, "Road Reparation"), cses(1676, "Road Construction"),
                   {"name": "Codeforces EDU — DSU", "url": "https://codeforces.com/edu/course/2/lesson/7"}]),
    dict(id=18, cat="Thuật toán", name="LCA, Euler Tour", short="LCA\nEuler Tour", viz="euler",
         goals=["Nhảy nhị phân tìm tổ tiên thứ k, LCA", "Khoảng cách trên cây, truy vấn đường đi",
                "Euler tour: biến cây con thành đoạn", "Mảng hiệu trên cây"],
         b1=["Nhảy nhị phân", "LCA & khoảng cách", "Max trên đường đi"],
         b2=["Euler tour + BIT", "Mảng hiệu trên cây", "LCA bằng RMQ"],
         videos=vids("LCA nhảy nhị phân", [("CodeNCode", "LCA binary lifting"), ("Luv", "LCA"), ("take U forward", "binary lifting"),
                                           ("Kartik Arora", "euler tour")]),
         practice=[cses(1687, "Company Queries I"), cses(1688, "Company Queries II"), cses(1135, "Distance Queries"),
                   cses(1136, "Counting Paths"), cses(1137, "Subtree Queries"), cses(1138, "Path Queries"), cses(1139, "Distinct Colors")]),
    dict(id=19, cat="Thuật toán", name="Hash", short="Hash", viz="hash",
         goals=["Hash đa thức, hash lăn, chọn modulo/cơ số", "So sánh xâu con O(1)", "Kết hợp tìm kiếm nhị phân",
                "Z-function, KMP, Manacher (đối chiếu)"],
         b1=["Hash đa thức & va chạm", "Hash lăn, so khớp xâu", "Chu kỳ, biên"],
         b2=["Hash + tìm kiếm nhị phân", "Hash 2D, hash cây", "Z-function, Manacher"],
         videos=vids("hash xâu rolling hash", [("CodeNCode", "string hashing"), ("take U forward", "rabin karp"),
                                               ("Luv", "string hashing"), ("Abdul Bari", "KMP algorithm")]),
         practice=[cses(1753, "String Matching"), cses(1732, "Finding Borders"), cses(1733, "Finding Periods"),
                   cses(1110, "Minimal Rotation"), cses(1111, "Longest Palindrome"), cses(2420, "Palindrome Queries")]),
    dict(id=20, cat="Thuật toán", name="Trie", short="Trie", viz="trie",
         goals=["Cài đặt trie bằng mảng next[N][26]", "Đếm theo tiền tố, gợi ý tự động",
                "Trie nhị phân cho bài toán XOR", "Giới thiệu Aho-Corasick"],
         b1=["Cấu trúc trie & chèn/tìm", "Đếm tiền tố, LCP", "Trie + QHĐ"],
         b2=["Trie nhị phân: XOR lớn nhất", "Đếm cặp XOR < k", "Aho-Corasick"],
         videos=vids("cây trie", [("take U forward", "trie playlist"), ("Luv", "trie"),
                                  ("CodeNCode", "trie maximum xor"), ("Kartik Arora", "aho corasick")]),
         practice=[cses(1731, "Word Combinations")]),
]


def _sessions(t):
    name = t["name"]
    return [
        {"title": f"Buổi 1 — {t['b1'][0]}", "minutes": 120, "items": [
            {"min": 10, "what": "Khởi động: chữa nhanh bài tập về nhà của chuyên đề trước, đặt vấn đề bằng một bài toán thực tế."},
            {"min": 35, "what": "Lý thuyết: " + "; ".join(t["b1"]) + "."},
            {"min": 15, "what": "Mô phỏng trực quan trên công cụ (tab Mô phỏng), cho học sinh dự đoán bước tiếp theo."},
            {"min": 20, "what": "Code mẫu trực tiếp (C++), phân tích độ phức tạp và lỗi thường gặp."},
            {"min": 35, "what": "Luyện tập tại lớp: các bài mức Cơ bản – Dễ của chuyên đề, nộp chấm tự động."},
            {"min": 5, "what": "Tổng kết, giao bài tập về nhà."}]},
        {"title": f"Buổi 2 — {t['b2'][0]}", "minutes": 120, "items": [
            {"min": 15, "what": "Chữa bài tập buổi 1 (chọn bài có nhiều lượt WA/TLE trong bảng nộp bài)."},
            {"min": 30, "what": "Kỹ thuật nâng cao: " + "; ".join(t["b2"]) + "."},
            {"min": 50, "what": "Luyện tập: các bài mức Trung bình – Khá; học sinh khá thử bài Nâng cao."},
            {"min": 15, "what": "Thi nhanh 15 phút (dùng chức năng Tổng hợp đề) để kiểm tra mức độ nắm bài."},
            {"min": 10, "what": f"Tổng kết chuyên đề {name}, giới thiệu video tự học và liên kết luyện thêm."}]},
    ]


TOPICS = []
for _t in T:
    d = dict(_t)
    d["color"] = CAT_COLOR[d["cat"]]
    d["sessions"] = _sessions(d)
    d["count"] = sum(1 for p in PROBLEMS.values() if p.topic == d["id"])
    TOPICS.append(d)


def topic_detail(tid):
    for t in TOPICS:
        if t["id"] == tid:
            d = dict(t)
            path = os.path.join(ROOT, "content", f"{tid:02d}.md")
            d["theory"] = open(path, encoding="utf-8").read() if os.path.exists(path) else "_(Chưa có nội dung lý thuyết)_"
            d["problems"] = sorted((p.summary() for p in PROBLEMS.values() if p.topic == tid),
                                   key=lambda x: (x["level"], x["id"]))
            return d
    return None
