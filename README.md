# Lớp Thuật Toán — công cụ soạn giáo án & luyện tập CTDL-GT

Công cụ web chạy trên máy cá nhân giúp giáo viên dạy (và học sinh tự học) theo **lộ trình 20 chuyên đề**
từ cơ bản đến nâng cao:

| # | Chuyên đề | # | Chuyên đề |
|---|---|---|---|
| 1 | Sàng nguyên tố, các bài toán số học | 11 | Cây DFS, khớp – cầu |
| 2 | Tổng tiền tố | 12 | Thành phần liên thông mạnh, DAG – DP on DAG |
| 3 | Tìm kiếm nhị phân | 13 | Đường đi ngắn nhất |
| 4 | Hai con trỏ | 14 | Max, min trên đoạn tịnh tiến |
| 5 | Map – Set – Heap | 15 | Sparse table |
| 6 | Đệ quy – quay lui, bitwise | 16 | Segment tree / BIT, sweep line |
| 7 | Đệ quy có nhớ, quy hoạch động | 17 | DSU, cây khung nhỏ nhất |
| 8 | QHĐ đếm | 18 | LCA, Euler tour |
| 9 | QHĐ knapsack, LIS/LCS | 19 | Hash |
| 10 | DFS/BFS, BFS 0-1 | 20 | Trie |

## Tính năng

- **430 bài tập** (21–23 bài mỗi chuyên đề), 5 mức độ: Cơ bản → Dễ → Trung bình → Khá → Nâng cao. Đề tiếng Việt,
  có gợi ý thuật toán và ví dụ.
- **Chấm bài kiểu Codeforces**: C++17 và Python 3; chạy lần lượt từng test và dừng ở test sai đầu tiên; kết quả
  `Accepted`, `Wrong answer on test k`, `Time limit exceeded on test k`, `Memory limit exceeded`, `Runtime error`,
  `Compilation error`; báo thời gian/bộ nhớ, hiển thị input – output – đáp án của test sai, thông báo checker
  giống Codeforces. Có **chạy thử với input tự nhập** (custom invocation).
- **Bộ test tự sinh**: mỗi bài có bộ sinh test ngẫu nhiên (cố định seed) + lời giải mẫu. Test lớn nhất đủ để
  phân biệt `O(n log n)` với `O(n²)` (lời giải chậm sẽ bị TLE). Lời giải mẫu được đối chiếu với lời giải trâu
  (`tests/validate.py`).
- **Giáo án** cho từng chuyên đề: mục tiêu, tiến trình 2 buổi × 120 phút (phân bổ thời gian từng hoạt động),
  bài luyện tại lớp / bài về nhà theo mức độ, tiêu chí đánh giá; trang **giáo án toàn khoá**; in / lưu PDF.
- **Lý thuyết** từng chuyên đề kèm code mẫu C++, độ phức tạp, lỗi thường gặp.
- **Mô phỏng trực quan** (20 mô phỏng, chạy từng bước / tự động, nhập dữ liệu tuỳ ý): sàng Eratosthenes, mảng cộng dồn,
  tìm kiếm nhị phân, hai con trỏ, heap, N quân hậu, QHĐ đổi tiền, QHĐ đếm trên lưới, LCS, BFS/DFS trên lưới,
  Tarjan cầu–khớp, sắp xếp topo, Dijkstra, deque đơn điệu, sparse table, segment tree, Kruskal + DSU,
  Euler tour + LCA, hash lăn Rabin–Karp, trie.
- **Video**: kênh tiếng Việt (28tech, VNOI, Big-O Coding) và giảng viên Ấn Độ (take U forward – Striver,
  Aditya Verma, Luv, CodeNCode, Abdul Bari, Kunal Kushwaha, Kartik Arora) theo đúng chủ đề; giáo viên có thể dán
  link video cụ thể để nhúng cho lớp.
- **Tổng hợp đề**: trộn bài theo chuyên đề / thẻ kiến thức liên quan / mức độ, rải đều chuyên đề, sắp xếp dễ → khó;
  làm bài tính giờ (có bảng kết quả) hoặc in đề ra giấy.
- **Luyện thêm**: liên kết bài tương ứng trên CSES, Codeforces EDU, VNOJ.
- Lưu tiến độ, lịch sử bài nộp theo tên học sinh; giáo viên xem bài nộp cả lớp và code từng bài.

## Dùng trên GitHub (GitHub Pages + GitHub Actions)

Trang web: **https://quocdat16610-web.github.io/dsa/** (sau khi bật Pages — xem bước 1).

1. Workflow *Triển khai GitHub Pages* tự dựng trang và đẩy sang nhánh `gh-pages`. Nếu trang chưa hiện, vào
   **Settings của repo → Pages → Source: Deploy from a branch → `gh-pages` / `(root)` → Save**.
2. Workflow *Sinh bộ test* tự sinh sẵn bộ test của 20 chuyên đề và lưu vào cache (chạy lại mỗi 5 ngày).
3. Khi học sinh bấm **Nộp bài** trên trang Pages, trang mở một issue `[DSA] Nộp ...` chứa code; workflow *Chấm bài*
   chạy trên máy chủ GitHub (Ubuntu, g++ / Python), chấm giống Codeforces, trả lời bằng bình luận và đóng issue.
   Trang web tự đọc kết quả và hiển thị (thường 30–90 giây).
   - Cần tài khoản GitHub. Không có token: trang mở tab GitHub, bấm **Create** là xong.
   - Có token (nút **🔑 GitHub**, fine-grained token chỉ cho repo này, quyền *Issues: Read and write*): nộp bằng một
     cú bấm, không mở tab, không bị giới hạn 60 lượt đọc API/giờ.
   - Giáo viên xem bài nộp cả lớp trong mục *Issues* của repo (nhãn `dsa-accepted` / `dsa-rejected`).
4. Code học sinh chạy dưới một người dùng Linux hạn chế, job chấm không có quyền ghi vào repo; job trả lời
   chỉ đọc file kết quả. Repo public thì GitHub Actions miễn phí.

## Cài đặt và chạy trên máy

Yêu cầu: **Python ≥ 3.8** (không cần cài thư viện) và **g++** (để chấm C++). Chạy trên Linux hoặc macOS.

```bash
python3 server.py                 # mở http://localhost:8000
python3 server.py --prebuild      # sinh sẵn toàn bộ bộ test ở nền (lần đầu mất ~15-25 phút)
python3 server.py --host 0.0.0.0 --port 8000   # cho cả lớp truy cập qua mạng LAN
```

**Windows**: dùng WSL (`wsl --install`, rồi chạy các lệnh trên trong Ubuntu) hoặc Docker:

```bash
docker build -t lop-thuat-toan .
docker run -p 8000:8000 -v "$PWD/data:/app/data" lop-thuat-toan
```

Bộ test được sinh ở lần đầu mở / nộp một bài (vài giây tới ~20 giây với bài lớn) rồi lưu nén vào `data/tests/`.
Dung lượng cache mặc định tối đa 2 GB (đổi bằng biến môi trường `DSA_CACHE_GB`), file ít dùng sẽ tự xoá.

> ⚠️ **Bảo mật**: code của học sinh được chạy trực tiếp trên máy (có giới hạn thời gian, bộ nhớ, kích thước file
> bằng `rlimit`) nhưng **không phải sandbox an toàn tuyệt đối**. Chỉ dùng trong lớp học tin cậy; nếu mở ra Internet
> hãy chạy trong Docker.

## Cấu trúc thư mục

```
server.py              máy chủ HTTP (thư viện chuẩn) + API
curriculum.py          lộ trình: mục tiêu, giáo án theo buổi, video, link luyện thêm
content/NN.md          lý thuyết từng chuyên đề (Markdown)
problems/base.py       khung định nghĩa bài + tiện ích sinh test
problems/tNN_*.py      ngân hàng bài của chuyên đề NN
problems/__init__.py   nạp bài, cache bộ test
judge/judge.py         trình chấm; judge/runner.c đo thời gian/bộ nhớ chính xác
tools/build_static.py  xuất bản web tĩnh cho GitHub Pages
tools/gh_judge.py      chấm bài từ issue trên GitHub Actions
tools/build_tests.py   sinh sẵn bộ test (song song)
.github/workflows/     pages.yml (triển khai Pages), judge.yml (chấm), tests-cache.yml (sinh test)
static/                giao diện web (app.js, viz.js – mô phỏng, md.js, style.css)
tests/validate.py      kiểm tra toàn bộ ngân hàng bài
data/                  (tự tạo) cache test, lịch sử nộp bài submissions.jsonl
```

## Thêm / sửa bài tập

Mỗi bài là một lời gọi `add(...)` trong `problems/tNN_*.py`:

```python
def _g(r, s):                 # sinh test: r = random.Random cố định, s ∈ [0, 1] là cỡ test (1 = lớn nhất)
    n = S(s, 1, 2 * 10**5)
    return lines(str(n), L(arr(r, n, 1, 10**9)))

def _sol(s):                  # lời giải mẫu: nhận input (chuỗi), trả về output
    a = list(map(int, s.split()[1:]))
    return max(a)

add(T, "Tên bài", 2, """Đề bài (Markdown)...""", "Mô tả input", "Mô tả output",
    ["3\n1 5 2\n"],           # input ví dụ (output tự tính)
    _g, _sol, brute=None, tags=["thẻ"], tl=1000, ml=256, checker="tokens")   # checker="float" cho số thực
```

Sau khi sửa, chạy `python3 tests/validate.py NN` để kiểm tra (sinh test, đối chiếu `sol` với `brute` nếu có).
Bộ test cũ tự sinh lại khi file đề thay đổi.

Sửa giáo án / video trong `curriculum.py`, sửa lý thuyết trong `content/NN.md`.
